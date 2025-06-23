from app import db, app
from app.models import User
from werkzeug.security import generate_password_hash

with app.app_context():
    # יצירת כל הטבלאות אם הן לא קיימות
    db.create_all()

    # בדיקה אם המשתמש 'demo' כבר קיים
    if not User.query.filter_by(username='demo').first():
        demo_user = User(
            username='demo',
            password=generate_password_hash('demo123')
        )
        db.session.add(demo_user)
        db.session.commit()
        print("✅ משתמש דמו נוצר: demo / demo123")
    else:
        print("ℹ️ משתמש דמו כבר קיים")
