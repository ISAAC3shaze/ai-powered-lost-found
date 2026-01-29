from sentence_transformers import SentenceTransformer
import torch
import torchvision.models as models
import torchvision.transforms as transforms
from PIL import Image

# Local fallback text model (safety)
_local_text_model = SentenceTransformer("all-MiniLM-L6-v2")

# Image embedding model
image_model = models.resnet18(pretrained=True)
image_model.eval()
image_model = torch.nn.Sequential(*list(image_model.children())[:-1])

transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor()
])

# ---- GOOGLE AI EMBEDDINGS ----
from google_text_embeddings import get_google_text_embedding


def get_text_embedding(text):
    """
    Primary: Google AI text embeddings
    Fallback: local sentence transformer
    """
    try:
        emb = get_google_text_embedding(text)
        return emb
    except Exception as e:
        # Fallback for safety
        return _local_text_model.encode(text)


def get_image_embedding(image_path):
    img = Image.open(image_path).convert("RGB")
    img = transform(img).unsqueeze(0)
    with torch.no_grad():
        emb = image_model(img)
    return emb.flatten().numpy()
