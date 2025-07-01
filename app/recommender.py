import random
from collections import Counter
from app.models import ShoppingList, Item


def generate_recommendations(user_id, max_suggestions=5):
    """
    החזרת רשימת המלצות בפורמט:
    [{"name": "חלב", "category": "מוצרי חלב"}, ...]
    """
    # 1) כל הפריטים של המשתמש בכל הרשימות
    items = (
        Item.query.join(ShoppingList)
        .filter(ShoppingList.user_id == user_id)
        .all()
    )
    if not items:
        # אם אין כלום, מציע פריטי‑ברירת‑מחדל
        return [
            {"name": "חלב", "category": "מוצרי חלב"},
            {"name": "ביצים", "category": "מקררים"},
            {"name": "לחם", "category": "מאפים"},
        ]

    # 2) ספירת הופעות (הכי פופולריים)
    counter = Counter((it.name, it.category) for it in items)

    # 3) בחירת כאלה שאין ברשימה הפעילה / חוסרים נפוצים
    common = [dict(name=n, category=c) for (n, c), _ in counter.most_common()]
    random.shuffle(common)  # ערבוב קל
    return common[:max_suggestions]
