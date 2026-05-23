def calculate_score(stats: dict) -> float:
    kd = min(float(stats.get("kd", 0)) / 8, 1) * 30
    damage = min(float(stats.get("damage", 0)) / 1200, 1) * 25
    accuracy = min(float(stats.get("accuracy", 0)) / 100, 1) * 15
    survival = min(float(stats.get("survival_time", 0)) / 30, 1) * 10
    headshots = min(float(stats.get("headshots", 0)) / 30, 1) * 10
    win_rate = min(float(stats.get("win_rate", 0)) / 100, 1) * 10
    return round(kd + damage + accuracy + survival + headshots + win_rate, 2)

def player_title(score: float) -> str:
    if score >= 90: return "أسطورة ساحات القتال 👑"
    if score >= 75: return "محترف هجومي 🔥"
    if score >= 60: return "لاعب تكتيكي ذكي 🎯"
    if score >= 40: return "لاعب واعد يحتاج تطوير ⚡"
    return "مقاتل مبتدئ يحتاج تدريب 🧠"

def badge_for_score(score: float) -> str:
    if score >= 90: return "Conqueror Mind"
    if score >= 75: return "Rush Master"
    if score >= 60: return "Smart Survivor"
    if score >= 40: return "Rising Fighter"
    return "Training Mode"
