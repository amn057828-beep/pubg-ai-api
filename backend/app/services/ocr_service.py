import re
import pytesseract
from PIL import Image


def extract_text_from_image(path: str):
    image = Image.open(path)

    text = pytesseract.image_to_string(
        image,
        lang="eng"
    )

    return text


def extract_number(text: str, patterns, default=0):
    for pattern in patterns:
        match = re.search(pattern, text, re.I)

        if match:
            try:
                return float(match.group(1))
            except:
                pass

    return default


def parse_pubg_stats(text: str):
    kd = extract_number(text, [
        r"KD[:\s]+(\d+(\.\d+)?)",
        r"K/D[:\s]+(\d+(\.\d+)?)",
    ])

    damage = extract_number(text, [
        r"Damage[:\s]+(\d+)",
        r"DMG[:\s]+(\d+)",
    ])

    accuracy = extract_number(text, [
        r"Accuracy[:\s]+(\d+)",
        r"ACC[:\s]+(\d+)",
    ])

    survival = extract_number(text, [
        r"Survival[:\s]+(\d+)",
        r"Time[:\s]+(\d+)",
    ])

    headshots = extract_number(text, [
        r"Headshots[:\s]+(\d+)",
        r"HS[:\s]+(\d+)",
    ])

    win_rate = extract_number(text, [
        r"WinRate[:\s]+(\d+)",
        r"WR[:\s]+(\d+)",
    ])

    return {
        "pubg_id": "Screenshot_Player",
        "kd": kd,
        "damage": damage,
        "accuracy": accuracy,
        "survival_time": survival,
        "headshots": headshots,
        "win_rate": win_rate,
    }
