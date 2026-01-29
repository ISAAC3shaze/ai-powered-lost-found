import sqlite3
import json

# ------------------ DB CONNECTION ------------------
conn = sqlite3.connect("lost_found.db", check_same_thread=False)
cur = conn.cursor()

# ------------------ TABLE SETUP ------------------
cur.execute("""
CREATE TABLE IF NOT EXISTS items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    type TEXT,
    description TEXT,
    location TEXT,
    image_path TEXT,
    text_embedding TEXT,
    image_embedding TEXT,
    status TEXT DEFAULT 'available'
)
""")
conn.commit()

# ------------------ INSERT ITEM ------------------
def insert_item(item_type, desc, location, img_path, text_emb, img_emb):
    cur.execute(
        """
        INSERT INTO items
        (type, description, location, image_path, text_embedding, image_embedding, status)
        VALUES (?,?,?,?,?,?,?)
        """,
        (
            item_type,
            desc,
            location,
            img_path,
            json.dumps(text_emb),  # Gemini embeddings are already lists
            json.dumps(img_emb.tolist()) if img_emb is not None else None,
            "available"
        )
    )
    conn.commit()

# ------------------ FETCH FOUND ITEMS ------------------
def get_found_items():
    cur.execute("""
        SELECT id, description, location, image_path,
               text_embedding, image_embedding, status
        FROM items
        WHERE type = 'Found'
    """)
    return cur.fetchall()

# ------------------ RESERVE ITEM ------------------
def reserve_item(item_id):
    cur.execute(
        "UPDATE items SET status = 'reserved' WHERE id = ?",
        (item_id,)
    )
    conn.commit()

# ------------------ MARK ITEM RETURNED ------------------
def mark_item_returned(item_id):
    cur.execute(
        "UPDATE items SET status = 'returned' WHERE id = ?",
        (item_id,)
    )
    conn.commit()
