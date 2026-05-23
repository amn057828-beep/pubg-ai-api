import logging
import requests

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)

from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

from app.core.config import settings


logging.basicConfig(level=logging.INFO)


# =========================
# MENUS
# =========================

def main_menu():
    keyboard = [
        [
            InlineKeyboardButton(
                "🔍 تحليل الإحصائيات",
                callback_data="analyze"
            ),
            InlineKeyboardButton(
                "📸 تحليل Screenshot",
                callback_data="screenshot"
            ),
        ],
        [
            InlineKeyboardButton(
                "🏆 الترتيب",
                callback_data="leaderboard"
            ),
            InlineKeyboardButton(
                "💎 الاشتراك",
                callback_data="upgrade"
            ),
        ],
        [
            InlineKeyboardButton(
                "💡 نصيحة اليوم",
                callback_data="tip"
            ),
            InlineKeyboardButton(
                "📊 ملفي",
                callback_data="profile"
            ),
        ],
        [
            InlineKeyboardButton(
                "ℹ️ طريقة الاستخدام",
                callback_data="help"
            )
        ]
    ]

    return InlineKeyboardMarkup(keyboard)


def back_menu():
    keyboard = [
        [
            InlineKeyboardButton(
                "🔙 رجوع",
                callback_data="home"
            )
        ]
    ]

    return InlineKeyboardMarkup(keyboard)


# =========================
# START
# =========================

async def start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    text = (
        "🎮 أهلاً بك في PUBG AI Analyzer\n\n"
        "🔥 مدربك الذكي لتحليل أداء PUBG Mobile بالعربية\n\n"
        "اختر من القائمة:"
    )

    await update.message.reply_text(
        text,
        reply_markup=main_menu()
    )


# =========================
# BUTTON HANDLER
# =========================

async def button_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    query = update.callback_query

    await query.answer()

    data = query.data

    # =========================
    # HOME
    # =========================

    if data == "home":
        await query.edit_message_text(
            "🎮 PUBG AI Analyzer\n\nاختر الخدمة:",
            reply_markup=main_menu()
        )

    # =========================
    # ANALYZE
    # =========================

    elif data == "analyze":
        text = (
            "📊 أرسل الإحصائيات بهذا الشكل:\n\n"
            "KD 3.2 Damage 650 Accuracy 28 "
            "Survival 18 Headshots 15 WinRate 22"
        )

        await query.edit_message_text(
            text,
            reply_markup=back_menu()
        )

    # =========================
    # SCREENSHOT
    # =========================

    elif data == "screenshot":
        text = (
            "📸 أرسل Screenshot لنتائج PUBG\n\n"
            "وسيتم تحليلها تلقائيًا 🤖"
        )

        await query.edit_message_text(
            text,
            reply_markup=back_menu()
        )

    # =========================
    # LEADERBOARD
    # =========================

    elif data == "leaderboard":

        try:
            response = requests.get(
                f"{settings.API_BASE_URL}/leaderboard/",
                timeout=10
            )

            rows = response.json()

            if not rows:
                text = (
                    "🏆 لا يوجد ترتيب بعد.\n"
                    "كن أول لاعب يظهر بالقائمة 🔥"
                )

            else:
                lines = [
                    "🏆 أفضل اللاعبين:\n"
                ]

                for row in rows[:10]:

                    lines.append(
                        f"{row['rank']}. "
                        f"{row['pubg_id']} | "
                        f"⭐ {row['score']} | "
                        f"🎖️ {row['badge']}"
                    )

                text = "\n".join(lines)

        except Exception:
            text = "❌ تعذر جلب الترتيب حاليًا."

        await query.edit_message_text(
            text,
            reply_markup=back_menu()
        )

    # =========================
    # UPGRADE
    # =========================

    elif data == "upgrade":

        text = (
            "💎 خطط الاشتراك:\n\n"
            "🆓 مجاني:\n"
            "5 تحليلات يوميًا\n\n"
            "🔥 Pro:\n"
            "100 تحليل يوميًا\n\n"
            "👑 Premium:\n"
            "تحليلات غير محدودة\n\n"
            "راسل الإدارة للاشتراك."
        )

        await query.edit_message_text(
            text,
            reply_markup=back_menu()
        )

    # =========================
    # PROFILE
    # =========================

    elif data == "profile":

        user = query.from_user

        text = (
            f"👤 الملف الشخصي\n\n"
            f"الاسم: {user.first_name}\n"
            f"المعرف: @{user.username}\n"
            f"Telegram ID: {user.id}\n\n"
            f"الخطة الحالية: Free 🆓"
        )

        await query.edit_message_text(
            text,
            reply_markup=back_menu()
        )

    # =========================
    # TIP
    # =========================

    elif data == "tip":

        text = (
            "💡 نصيحة اليوم:\n\n"
            "لا تدخل fight مفتوح بدون Cover.\n"
            "استخدم Peek + Cover لرفع نسبة الفوز 🔥"
        )

        await query.edit_message_text(
            text,
            reply_markup=back_menu()
        )

    # =========================
    # HELP
    # =========================

    elif data == "help":

        text = (
            "ℹ️ طريقة الاستخدام:\n\n"
            "1️⃣ اختر تحليل الإحصائيات\n"
            "2️⃣ أرسل بياناتك\n"
            "3️⃣ سيقوم الذكاء الاصطناعي بتحليل أدائك\n\n"
            "أو أرسل Screenshot مباشرة 📸"
        )

        await query.edit_message_text(
            text,
            reply_markup=back_menu()
        )


# =========================
# RUN BOT
# =========================

def run_bot():

    app = Application.builder().token(
        settings.TELEGRAM_BOT_TOKEN
    ).build()

    app.add_handler(
        CommandHandler("start", start)
    )

    app.add_handler(
        CallbackQueryHandler(button_handler)
    )

    app.run_polling()
