import streamlit as st
import os
import json
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

from embedding_utils import get_text_embedding, get_image_embedding
from gemini_explainer import explain_match
from db import insert_item, get_found_items, reserve_item, mark_item_returned

# ------------------ SESSION STATE ------------------
if "claimed_items" not in st.session_state:
    st.session_state.claimed_items = set()

# ------------------ UI CONFIG ------------------
st.set_page_config(page_title="AI-Powered Lost & Found", layout="centered")
st.title("🔍 AI-Powered Lost & Found")

st.markdown(
    "A privacy-first, AI-powered campus lost & found system using Google AI."
)

st.markdown("---")

# ------------------ INPUT FORM ------------------
item_type = st.selectbox("Item Type", ["Lost", "Found"])
description = st.text_input("Item Description")
location = st.text_input("Where was it lost / found? (optional)")

image = st.file_uploader(
    "Upload Item Image (required for Found, optional for Lost)",
    type=["jpg", "png", "jpeg"]
)

st.markdown("---")

# ------------------ SUBMIT ------------------
if st.button("Submit"):

    if description.strip() == "":
        st.error("Please provide item description")

    elif item_type == "Found" and image is None:
        st.error("Image is required for Found items")

    else:
        os.makedirs("uploads", exist_ok=True)

        img_path = None
        img_emb = None

        if image is not None:
            img_path = f"uploads/{image.name}"
            with open(img_path, "wb") as f:
                f.write(image.read())
            img_emb = get_image_embedding(img_path)

        text_emb = get_text_embedding(description)

        insert_item(item_type, description, location, img_path, text_emb, img_emb)
        st.success("✅ Item saved successfully")

        # ------------------ MATCHING (ONLY FOR LOST) ------------------
        if item_type == "Lost":
            found_items = get_found_items()
            st.subheader("🔎 AI Matches Found")

            for f in found_items:
                f_id, f_desc, f_loc, f_img, f_text_emb, f_img_emb, f_status = f

                # HARD BLOCKS
                if f_status != "available":
                    continue
                if f_id in st.session_state.claimed_items:
                    continue

                f_text_emb = np.array(json.loads(f_text_emb))
                txt_sim = cosine_similarity([text_emb], [f_text_emb])[0][0]

                if img_emb is not None and f_img_emb is not None:
                    f_img_emb = np.array(json.loads(f_img_emb))
                    img_sim = cosine_similarity([img_emb], [f_img_emb])[0][0]
                    img_weight = 0.5
                else:
                    img_sim = 0
                    img_weight = 0

                if location.strip():
                    loc_sim = 1 if (
                        location.lower() in f_loc.lower()
                        or f_loc.lower() in location.lower()
                    ) else 0
                else:
                    loc_sim = 0

                score = img_weight * img_sim + 0.6 * txt_sim + 0.4 * loc_sim

                if score < 0.6:
                    continue

                st.image(f_img, width=220)
                st.write(f"**Description:** {f_desc}")
                st.write(f"**Found at:** {f_loc}")
                st.write(f"**Match Score:** {round(score, 3)}")

                if score >= 0.8:
                    st.success("🟢 High confidence match")

                    explanation = explain_match(
                        lost_desc=description,
                        found_desc=f_desc,
                        location_hint=f_loc
                    )

                    if explanation:
                        st.markdown("**🤖 AI Explanation:**")
                        st.write(explanation)

                # ------------------ CLAIM ------------------
                if st.button("Claim this item", key=f"claim_{f_id}"):
                    reserve_item(f_id)
                    st.session_state.claimed_items.add(f_id)

                    st.success("✅ Item claimed and reserved.")
                    st.info(
                        "Finder has been notified to submit the item "
                        "to the Lost & Found desk."
                    )

                    # HARD STOP: prevents re-render bug
                    st.stop()

                # ------------------ ITEM RECEIVED ------------------
                if f_id in st.session_state.claimed_items:
                    if st.button("✅ Item received", key=f"received_{f_id}"):
                        mark_item_returned(f_id)
                        st.session_state.claimed_items.remove(f_id)

                        st.success("🎉 Item returned. Case closed.")
                        st.stop()

                st.markdown("---")
