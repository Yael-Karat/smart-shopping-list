from app import db, app
from app.models import User, ShoppingList, Item
from werkzeug.security import generate_password_hash

with app.app_context():
    db.create_all()

    # נסה למצוא את המשתמש קודם
    demo_user = User.query.filter_by(username='demo').first()

    # אם לא קיים - צור אותו
    if not demo_user:
        demo_user = User(
            username='demo',
            password=generate_password_hash('demo123')
        )
        db.session.add(demo_user)
        db.session.commit()
        print("✅ משתמש דמו נוצר: demo / demo123")
    else:
        print("ℹ️ משתמש דמו כבר קיים")

    # בדיקת רשימה לדמו
    shopping_list = ShoppingList.query.filter_by(name="קניות לשבוע", user_id=demo_user.id).first()

    if not shopping_list:
        shopping_list = ShoppingList(name="קניות לשבוע", user=demo_user)
        db.session.add(shopping_list)
        db.session.commit()
        print("✅ נוצרה רשימת קניות 'קניות לשבוע'")

        # הוספת פריטים לדוגמה
        items = [
            Item(name="חלב", category="מוצרי חלב", list=shopping_list),
            Item(name="לחם", category="מאפים", list=shopping_list),
            Item(name="עגבניות", category="ירקות", list=shopping_list)
        ]
        db.session.add_all(items)
        db.session.commit()
        print("✅ נוספו פריטים לדוגמה לרשימה")
    else:
        print("ℹ️ רשימת הקניות כבר קיימת לדמו")
