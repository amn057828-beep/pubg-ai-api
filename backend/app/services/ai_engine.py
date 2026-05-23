from openai import OpenAI
from app.core.config import settings
from app.services.scoring import calculate_score, player_title, badge_for_score

client = OpenAI(api_key=settings.OPENAI_API_KEY) if settings.OPENAI_API_KEY else None

SYSTEM_PROMPT = """
أنت مدرب محترف في PUBG Mobile ومحلل أداء للاعبين العرب.
اكتب تقريراً عربياً ممتعاً ومنظماً يتضمن:
التقييم العام، نقاط القوة، نقاط الضعف، أفضل أسلوب لعب، أفضل أسلحة، خطة تحسين 7 أيام، ونصيحة مدرب.
"""

def fallback_report(stats: dict, score: float, title: str) -> str:
    return f"""🔥 تقييمك: {score}/100
🏷️ التصنيف: {title}

نقاط القوة:
- لديك مؤشرات قتالية يمكن البناء عليها.
- ارتفاع الضرر يعني أنك تدخل الاشتباكات ولا تلعب بسلبية.

نقاط الضعف:
- راقب دقة التصويب ونسبة الهيدشوت.
- إذا كان وقت النجاة منخفضاً فالمشكلة غالباً في التمركز والاندفاع الزائد.

أفضل أسلوب لعب:
- هجومي محسوب: ادخل الاشتباك بزاوية، غطاء، ومعلومة.

أفضل أسلحة:
- M416 للاستقرار.
- UMP45 للقتال القريب.
- Mini14 أو SKS للمسافات المتوسطة.

خطة تحسين 7 أيام:
- يوم 1-2: تدريب recoil.
- يوم 3-4: تدريب peek + cover.
- يوم 5: مراجعة أخطاء النزول.
- يوم 6-7: لعب سكواد بدور واضح.

نصيحة مدرب:
الاحتراف ليس كثرة قتل فقط؛ الاحتراف قرار صحيح، تمركز، وهدوء تحت الضغط.
"""

def analyze_player(stats: dict) -> dict:
    score = calculate_score(stats)
    title = player_title(score)
    badge = badge_for_score(score)

    if not client:
        report = fallback_report(stats, score, title)
    else:
        prompt = f"بيانات اللاعب: {stats}\nScore: {score}\nTitle: {title}\nBadge: {badge}"
        try:
            res = client.chat.completions.create(
                model=settings.OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.75
            )
            report = res.choices[0].message.content
        except Exception:
            report = fallback_report(stats, score, title)

    return {"score": score, "title": title, "badge": badge, "report": report, "data": stats}
