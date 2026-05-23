# PUBG AI Analyzer

بوت + API + لوحة تحكم لتحليل لاعبي PUBG Mobile بالذكاء الاصطناعي.

## المكونات
- Backend: Python FastAPI
- AI Engine: OpenAI API + نظام تقييم داخلي
- OCR: Tesseract لاستخراج أرقام Screenshot
- Telegram Bot
- Dashboard: React/Vite
- Database: PostgreSQL
- Docker Compose

## التشغيل

```bash
cp .env.example .env
docker compose up --build
```

ثم افتح:

- API: http://localhost:8000
- Swagger: http://localhost:8000/docs
- Dashboard: http://localhost:3000

## إنشاء المدير

بعد تشغيل الحاويات:

```bash
docker compose exec api python -m app.scripts.create_admin
```

بيانات المدير الافتراضية في `.env`:
- admin
- admin123

## ملاحظة مهمة
تحليل PUBG ID الحقيقي يحتاج API خارجي/رسمي من PUBG أو مزود بيانات. هذا المشروع جاهز لتحليل البيانات اليدوية والصور، ويمكن ربط مصدر بيانات لاحقًا بسهولة.


## الإضافات في النسخة V2

### 1. الاشتراك والحجز اليدوي
بدلاً من الدفع الإلكتروني في البداية:
- المستخدم يرسل طلب ترقية.
- الطلب يظهر في لوحة الإدارة.
- المدير يقبل أو يرفض.
- عند القبول يتم تحويل خطة المستخدم إلى Pro أو Premium.

Endpoints:
```text
POST /upgrade/request
GET /upgrade/my-requests
GET /admin/upgrade-requests
POST /admin/upgrade-requests/{id}/decision
POST /admin/users/{user_id}/plan/{plan}
```

### 2. Viral Features
تمت إضافة:
- Daily Tips
- Compare Players
- Share Result Card
- Badges
- Ranking System

Endpoints:
```text
GET /features/daily-tip
POST /features/compare
POST /analyze/share-card
```

### 3. Telegram Bot
تم دعم:
```text
/tip
/upgrade
/compare
```

ولطلب الاشتراك اليدوي من البوت:
```text
UPGRADE Pro 777000000 تم التحويل باسم أحمد
```

### 4. لوحة الإدارة
تمت إضافة قسم:
- طلبات الحجز والترقية اليدوية
- قبول/رفض الطلبات
- متابعة حالة الاشتراكات
