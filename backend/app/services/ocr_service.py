import re
from PIL import Image
import pytesseract

def extract_text_from_image(image_path: str) -> str:
    img = Image.open(image_path)
    return pytesseract.image_to_string(img, lang="eng+ara")

def find_number(patterns, text, default=0.0):
    for pattern in patterns:
        m = re.search(pattern, text, re.IGNORECASE)
        if m:
            try:
                return float(m.group(1).replace("%", ""))
            except Exception:
                continue
    return default

def parse_pubg_stats(text: str) -> dict:
    return {
        "pubg_id": None,
        "kd": find_number([r"K/?D\s*[:：]?\s*(\d+(?:\.\d+)?)", r"KD\s*(\d+(?:\.\d+)?)"], text),
        "damage": find_number([r"Damage\s*[:：]?\s*(\d+(?:\.\d+)?)", r"Avg Damage\s*(\d+(?:\.\d+)?)"], text),
        "accuracy": find_number([r"Accuracy\s*[:：]?\s*(\d+(?:\.\d+)?)%?", r"Acc\s*(\d+(?:\.\d+)?)%?"], text),
        "survival_time": find_number([r"Survival\s*Time\s*[:：]?\s*(\d+(?:\.\d+)?)", r"Survival\s*(\d+(?:\.\d+)?)"], text),
        "headshots": find_number([r"Headshots?\s*[:：]?\s*(\d+(?:\.\d+)?)%?", r"Headshot\s*Rate\s*(\d+(?:\.\d+)?)%?"], text),
        "win_rate": find_number([r"Win\s*Rate\s*[:：]?\s*(\d+(?:\.\d+)?)%?", r"Wins?\s*(\d+(?:\.\d+)?)%?"], text),
        "ocr_text": text[:4000],
    }
