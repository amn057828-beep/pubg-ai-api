from PIL import Image, ImageDraw, ImageFont
import os
import uuid


WIDTH = 900
HEIGHT = 500


def create_result_card(result: dict):
    image = Image.new("RGB", (WIDTH, HEIGHT), (15, 15, 25))

    draw = ImageDraw.Draw(image)

    neon_purple = (180, 0, 255)
    neon_green = (0, 255, 180)
    white = (255, 255, 255)

    draw.rectangle(
        [(20, 20), (WIDTH - 20, HEIGHT - 20)],
        outline=neon_purple,
        width=5
    )

    title_font = ImageFont.load_default()
    text_font = ImageFont.load_default()

    draw.text(
        (40, 40),
        "PUBG AI ANALYZER",
        fill=neon_green,
        font=title_font
    )

    data = result.get("data", {})

    draw.text(
        (40, 120),
        f"PLAYER: {data.get('pubg_id', 'Unknown')}",
        fill=white,
        font=text_font
    )

    draw.text(
        (40, 170),
        f"SCORE: {result.get('score', 0)}/100",
        fill=neon_green,
        font=text_font
    )

    draw.text(
        (40, 220),
        f"TITLE: {result.get('title', '')}",
        fill=white,
        font=text_font
    )

    draw.text(
        (40, 270),
        f"BADGE: {result.get('badge', '')}",
        fill=neon_purple,
        font=text_font
    )

    draw.text(
        (40, 340),
        "AI PERFORMANCE ANALYSIS",
        fill=neon_green,
        font=text_font
    )

    output_dir = "/tmp"

    filename = f"{uuid.uuid4()}.png"

    path = os.path.join(output_dir, filename)

    image.save(path)

    return path
