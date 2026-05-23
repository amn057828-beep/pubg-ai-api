import re
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

from app.core.config import settings
from app.services.ai_engine import analyze_player
from app.services.ocr_service import extract_text_from_image, parse_pubg_stats


telegram_app = None


def parse_text_stats(text: str):
    def n(pattern):
        m = re.search(pattern + r"\s*(\d+(?:\.\d+)?)", text, re.I)
        return float(m.group(1)) if m else 0

    return {
        "pubg_id": None,
        "kd": n("KD"),
        "damage": n("Damage"),
        "accuracy": n("Accuracy"),
        "survival_time": n("Survival"),
        "headshots": n("Headshots"),
        "win_rate": n("WinRate"),
    }


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        """🎮 أهلاً بك في PUBG AI Analyzer

أرسل إحصائياتك بهذا الشكل:
KD 3.2 Damage 650 Accuracy 28 Survival 18 Headshots 15 WinRate 22

أو أرسل Screenshot لنتائج PUBG وسأحللها لك تلقائيًا.

الأوامر:
/analyze
/compare
/leaderboard
/upgrade
/tip
"""
    )


async def analyze(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "أرسل Screenshot أو اكتب الإحصائيات وسأحللها لك 🔥"
    )


async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()

    if text.upper().startswith("UPGRADE"):
        parts = text.split(maxsplit=3)
        plan = parts[1].lower() if len(parts) > 1 else "pro"
        contact = parts[2] if len(parts) > 2 else str(update.effective_user.id)
        note = parts[3] if len(parts) > 3 else ""

        await update.message.reply_text(
            f"""✅ تم استلام طلب الترقية اليدوي

الخطة: {plan}
التواصل: {contact}
الملاحظة: {note}

سيراجعه المدير ويفعل الاشتراك."""
        )
        return

    stats = parse_text_stats(text)
    result = analyze_player(stats)

    await update.message.reply_text(
        f"{result['title']}\n\n{result['report']}"
    )


async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    photo = update.message.photo[-1]
    file = await photo.get_file()

    local = f"/tmp/{photo.file_id}.jpg"
    await file.download_to_drive(local)

    text = extract_text_from_image(local)
    stats = parse_pubg_stats(text)
    result = analyze_player(stats)

    await update.message.reply_text(
        f"📸 تم تحليل الصورة\n\n{result['title']}\n\n{result['report']}"
    )


async def leaderboard(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🏆 ميزة الترتيب مفعلة داخل API وسيتم ربطها بالبوت في الخطوة التالية."
    )


async def upgrade(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        """💎 الاشتراك اليدوي متاح الآن

الخطط:
Free: 5 تحليلات يوميًا
Pro: تحليلات أكثر وتقارير أعمق
Premium: مقارنة + Ranking + API

للحجز/الترقية اكتب:
UPGRADE Pro 777000000 تم التحويل باسم أحمد
"""
    )


async def compare(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "للمقارنة أرسل بيانات اللاعب الأول والثاني. سيتم تطوير هذه الميزة في البوت بعد تشغيل Webhook."
    )


async def tip(update: Update, context: ContextTypes.DEFAULT_TYPE):
    from app.services.tips import random_tip

    t = random_tip()
    await update.message.reply_text(
        f"💡 {t['title']}\n\n{t['body']}"
    )


def build_telegram_app():
    global telegram_app

    if telegram_app is not None:
        return telegram_app

    if not settings.TELEGRAM_BOT_TOKEN:
        return None

    telegram_app = Application.builder().token(
        settings.TELEGRAM_BOT_TOKEN
    ).build()

    telegram_app.add_handler(CommandHandler("start", start))
    telegram_app.add_handler(CommandHandler("analyze", analyze))
    telegram_app.add_handler(CommandHandler("leaderboard", leaderboard))
    telegram_app.add_handler(CommandHandler("upgrade", upgrade))
    telegram_app.add_handler(CommandHandler("compare", compare))
    telegram_app.add_handler(CommandHandler("tip", tip))

    telegram_app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    telegram_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    return telegram_app
