import re
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters,
)

from app.core.config import settings
from app.services.ai_engine import analyze_player
from app.services.ocr_service import extract_text_from_image, parse_pubg_stats
from app.services.card_generator import create_result_card


telegram_app = None


def main_menu():
    keyboard = [
        [
            InlineKeyboardButton("🔍 تحليل الإحصائيات", callback_data="analyze_stats"),
            InlineKeyboardButton("📸 تحليل Screenshot", callback_data="analyze_image"),
        ],
        [
            InlineKeyboardButton("🏆 الترتيب", callback_data="leaderboard"),
            InlineKeyboardButton("💎 الاشتراك", callback_data="upgrade"),
        ],
        [
            InlineKeyboardButton("💡 نصيحة اليوم", callback_data="tip"),
            InlineKeyboardButton("📊 ملفي", callback_data="profile"),
        ],
        [
            InlineKeyboardButton("ℹ️ طريقة الاستخدام", callback_data="help"),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)


def back_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🔙 رجوع للقائمة الرئيسية", callback_data="main_menu")]
    ])


def plans_menu():
    keyboard = [
        [InlineKeyboardButton("🟣 طلب Pro", callback_data="request_pro")],
        [InlineKeyboardButton("🟡 طلب Premium", callback_data="request_premium")],
        [InlineKeyboardButton("🔙 رجوع", callback_data="main_menu")],
    ]
    return InlineKeyboardMarkup(keyboard)


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


def has_stats(text: str) -> bool:
    return bool(re.search(r"\bKD\b|\bDamage\b|\bAccuracy\b|\bWinRate\b", text, re.I))


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = """🎮 أهلاً بك في PUBG AI Analyzer

مدربك الذكي لتحليل أداء PUBG Mobile بالعربية 🔥

اختر من القائمة:"""

    await update.message.reply_text(
        text,
        reply_markup=main_menu()
    )


async def analyze(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        """🔍 تحليل الإحصائيات

أرسل بياناتك بهذا الشكل:

KD 3.5 Damage 780 Accuracy 28 Survival 18 Headshots 17 WinRate 21""",
        reply_markup=back_menu()
    )


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data

    if data == "main_menu":
        await query.edit_message_text(
            """🎮 PUBG AI Analyzer

اختر الخدمة التي تريدها:""",
            reply_markup=main_menu()
        )

    elif data == "analyze_stats":
        await query.edit_message_text(
            """🔍 تحليل الإحصائيات

أرسل بيانات اللاعب بهذا الشكل:

KD 3.5 Damage 780 Accuracy 28 Survival 18 Headshots 17 WinRate 21

وسيتم توليد تقرير احترافي لك 🔥""",
            reply_markup=back_menu()
        )

    elif data == "analyze_image":
        await query.edit_message_text(
            """📸 تحليل Screenshot

أرسل صورة نتائج PUBG Mobile الآن.

سأقرأ الأرقام تلقائيًا ثم أعطيك تحليلًا احترافيًا.""",
            reply_markup=back_menu()
        )

    elif data == "leaderboard":
        await query.edit_message_text(
            """🏆 الترتيب

ميزة الترتيب مرتبطة بالـ API.
سيتم عرض أفضل اللاعبين بعد ربط المستخدمين بالتحليلات.

قريبًا:
🥇 أفضل مهاجم
🥈 أفضل Sniper
🥉 أفضل لاعب تكتيكي""",
            reply_markup=back_menu()
        )

    elif data == "upgrade":
        await query.edit_message_text(
            """💎 الاشتراكات

🟢 Free
- 5 تحليلات يوميًا
- تحليل إحصائيات

🟣 Pro
- تحليلات أكثر
- تقارير أعمق
- نصائح مخصصة

🟡 Premium
- تحليل متقدم
- مقارنة لاعبين
- Ranking
- API Access

اختر الخطة التي تريد طلبها:""",
            reply_markup=plans_menu()
        )

    elif data == "request_pro":
        await query.edit_message_text(
            """🟣 طلب اشتراك Pro

للحجز اليدوي أرسل رسالة بهذا الشكل:

UPGRADE Pro رقم_واتسابك ملاحظة_الدفع

مثال:
UPGRADE Pro 777000000 تم التحويل باسم أحمد""",
            reply_markup=back_menu()
        )

    elif data == "request_premium":
        await query.edit_message_text(
            """🟡 طلب اشتراك Premium

للحجز اليدوي أرسل رسالة بهذا الشكل:

UPGRADE Premium رقم_واتسابك ملاحظة_الدفع

مثال:
UPGRADE Premium 777000000 تم التحويل باسم أحمد""",
            reply_markup=back_menu()
        )

    elif data == "tip":
        from app.services.tips import random_tip
        t = random_tip()
        await query.edit_message_text(
            f"""💡 نصيحة اليوم

{t['title']}

{t['body']}""",
            reply_markup=back_menu()
        )

    elif data == "profile":
        user = query.from_user
        await query.edit_message_text(
            f"""📊 ملف اللاعب

👤 الاسم: {user.first_name}
🆔 Telegram ID: {user.id}

الخطة الحالية: Free
التحليلات اليوم: غير مرتبطة بعد

قريبًا سيتم ربط حسابك بالكامل بنظام الاشتراكات.""",
            reply_markup=back_menu()
        )

    elif data == "help":
        await query.edit_message_text(
            """ℹ️ طريقة الاستخدام

1️⃣ لتحليل الإحصائيات:
اضغط "تحليل الإحصائيات"
ثم أرسل:
KD 3.5 Damage 780 Accuracy 28 Survival 18 Headshots 17 WinRate 21

2️⃣ لتحليل صورة:
اضغط "تحليل Screenshot"
ثم أرسل صورة نتائج PUBG.

3️⃣ للاشتراك:
اضغط "الاشتراك" ثم اختر Pro أو Premium.

🔥 كل تحليل يعطيك:
- Score
- نقاط قوة
- نقاط ضعف
- أسلوب لعب مناسب
- أسلحة مقترحة
- خطة تحسين""",
            reply_markup=back_menu()
        )


async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()

    if text.upper().startswith("UPGRADE"):
        parts = text.split(maxsplit=3)
        plan = parts[1] if len(parts) > 1 else "Pro"
        contact = parts[2] if len(parts) > 2 else str(update.effective_user.id)
        note = parts[3] if len(parts) > 3 else ""

        await update.message.reply_text(
            f"""✅ تم استلام طلب الاشتراك اليدوي

💎 الخطة: {plan}
📞 التواصل: {contact}
🧾 الملاحظة: {note}

سيقوم المدير بمراجعة الطلب وتفعيل الاشتراك يدويًا.""",
            reply_markup=main_menu()
        )
        return

    if not has_stats(text):
        await update.message.reply_text(
            """لم أفهم البيانات 🤔

أرسل الإحصائيات بهذا الشكل:

KD 3.5 Damage 780 Accuracy 28 Survival 18 Headshots 17 WinRate 21""",
            reply_markup=main_menu()
        )
        return

    await update.message.reply_text("⏳ جاري تحليل أدائك...")

    stats = parse_text_stats(text)
    result = analyze_player(stats)

    card = create_result_card(result)

    await update.message.reply_photo(
        photo=open(card, "rb"),
        caption=f"""🎮 نتيجة التحليل

🏷️ التصنيف: {result['title']}
⭐ التقييم: {result['score']}/100
🎖️ الشارة: {result['badge']}

{result['report']}""",
        reply_markup=main_menu()
    )


async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📸 تم استلام الصورة... جاري قراءتها وتحليلها")

    photo = update.message.photo[-1]
    file = await photo.get_file()

    local = f"/tmp/{photo.file_id}.jpg"
    await file.download_to_drive(local)

    text = extract_text_from_image(local)
    stats = parse_pubg_stats(text)
    result = analyze_player(stats)

    card = create_result_card(result)

    await update.message.reply_photo(
        photo=open(card, "rb"),
        caption=f"""📸 تحليل الصورة

🏷️ التصنيف: {result['title']}
⭐ التقييم: {result['score']}/100
🎖️ الشارة: {result['badge']}

{result['report']}""",
        reply_markup=main_menu()
    )


async def leaderboard(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🏆 افتح القائمة الرئيسية واختر الترتيب.",
        reply_markup=main_menu()
    )


async def upgrade(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "💎 اختر خطة الاشتراك من القائمة:",
        reply_markup=plans_menu()
    )


async def compare(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "⚔️ ميزة المقارنة قادمة قريبًا داخل الواجهة.",
        reply_markup=main_menu()
    )


async def tip(update: Update, context: ContextTypes.DEFAULT_TYPE):
    from app.services.tips import random_tip
    t = random_tip()
    await update.message.reply_text(
        f"💡 {t['title']}\n\n{t['body']}",
        reply_markup=main_menu()
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

    telegram_app.add_handler(CallbackQueryHandler(button_handler))
    telegram_app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    telegram_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    return telegram_app
