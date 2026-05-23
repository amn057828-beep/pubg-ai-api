import re
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
from app.core.config import settings
from app.services.ai_engine import analyze_player
from app.services.ocr_service import extract_text_from_image, parse_pubg_stats

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
    await update.message.reply_text("""🎮 أهلاً بك في PUBG AI Analyzer

أرسل Screenshot أو بياناتك بهذا الشكل:
KD 3.2 Damage 650 Accuracy 28 Survival 18 Headshots 15 WinRate 22

الأوامر:
/analyze
/compare
/leaderboard
/upgrade
""")

async def analyze(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("أرسل Screenshot أو اكتب الإحصائيات وسأحللها لك 🔥")

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    if text.upper().startswith("UPGRADE"):
        parts = text.split(maxsplit=3)
        plan = parts[1].lower() if len(parts) > 1 else "pro"
        contact = parts[2] if len(parts) > 2 else str(update.effective_user.id)
        note = parts[3] if len(parts) > 3 else ""
        await update.message.reply_text(
            f"✅ تم استلام طلب الترقية اليدوي\nالخطة: {plan}\nالتواصل: {contact}\nالملاحظة: {note}\n\nسيراجعه المدير ويفعل الاشتراك."
        )
        return

    stats = parse_text_stats(text)
    result = analyze_player(stats)
    await update.message.reply_text(f"{result['title']}\n\n{result['report']}")

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    photo = update.message.photo[-1]
    file = await photo.get_file()
    local = f"/tmp/{photo.file_id}.jpg"
    await file.download_to_drive(local)
    text = extract_text_from_image(local)
    stats = parse_pubg_stats(text)
    result = analyze_player(stats)
    await update.message.reply_text(f"📸 تم تحليل الصورة\n\n{result['title']}\n\n{result['report']}")

async def leaderboard(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        data = requests.get(f"{settings.API_BASE_URL}/leaderboard/", timeout=10).json()
        lines = ["🏆 الترتيب:"]
        for i, row in enumerate(data[:10], 1):
            lines.append(f"{i}. {row.get('username')} - {row.get('score')} - {row.get('badge')}")
        await update.message.reply_text("\n".join(lines))
    except Exception:
        await update.message.reply_text("تعذر جلب الترتيب الآن.")

async def upgrade(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("""💎 الاشتراك اليدوي متاح الآن

الخطط:
Free: 5 تحليلات يومياً
Pro: تحليلات أكثر وتقارير أعمق
Premium: مقارنة + Ranking + API

للحجز/الترقية:
اكتب رسالة بهذا الشكل:
UPGRADE Pro رقم_واتسابك ملاحظة_الدفع

مثال:
UPGRADE Pro 777000000 تم التحويل باسم أحمد
""")

async def compare(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("للمقارنة أرسل بيانات اللاعب الأول والثاني. مثال: A KD 3 Damage 600 Accuracy 25 / B KD 2 Damage 500 Accuracy 22")

async def tip(update: Update, context: ContextTypes.DEFAULT_TYPE):
    from app.services.tips import random_tip
    t = random_tip()
    await update.message.reply_text(f"💡 {t['title']}\n\n{t['body']}")

def main():
    if not settings.TELEGRAM_BOT_TOKEN:
        raise RuntimeError("TELEGRAM_BOT_TOKEN is missing")
    app = Application.builder().token(settings.TELEGRAM_BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("analyze", analyze))
    app.add_handler(CommandHandler("leaderboard", leaderboard))
    app.add_handler(CommandHandler("upgrade", upgrade))
    app.add_handler(CommandHandler("compare", compare))
    app.add_handler(CommandHandler("tip", tip))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    app.run_polling()

if __name__ == "__main__":
    main()
