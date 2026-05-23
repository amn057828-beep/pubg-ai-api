from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import uuid

OUTPUT_DIR = Path("/tmp/pubg_share_cards")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def _font(size: int):
    # DejaVu exists in python slim in many cases; fallback to default.
    for path in [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
    ]:
        try:
            return ImageFont.truetype(path, size)
        except Exception:
            pass
    return ImageFont.load_default()

def create_share_card(title: str, score: float, badge: str, username: str = "PUBG Player") -> str:
    w, h = 1080, 1080
    img = Image.new("RGB", (w, h), (8, 8, 15))
    draw = ImageDraw.Draw(img)

    # Neon background shapes
    draw.ellipse((-250, -220, 520, 520), fill=(85, 35, 155))
    draw.ellipse((650, 680, 1320, 1320), fill=(20, 120, 70))
    draw.rounded_rectangle((70, 90, 1010, 990), radius=45, outline=(140, 92, 246), width=6, fill=(18, 24, 39))

    f_big = _font(72)
    f_mid = _font(46)
    f_small = _font(34)
    f_score = _font(150)

    draw.text((90, 130), "PUBG AI ANALYZER", font=f_mid, fill=(167, 243, 208))
    draw.text((90, 230), username, font=f_small, fill=(220, 220, 220))
    draw.text((90, 335), title, font=f_big, fill=(255, 255, 255))
    draw.text((90, 510), str(score), font=f_score, fill=(34, 197, 94))
    draw.text((430, 590), "/100", font=f_mid, fill=(180, 180, 180))
    draw.text((90, 780), f"Badge: {badge}", font=f_mid, fill=(196, 181, 253))
    draw.text((90, 900), "شارك نتيجتك وتحدى أصدقاءك 🔥", font=f_small, fill=(167, 243, 208))

    out = OUTPUT_DIR / f"share_{uuid.uuid4().hex}.png"
    img.save(out)
    return str(out)
