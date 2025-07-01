from flask import (
    render_template, request, redirect,
    url_for, flash, abort
)
from flask_login import (
    login_user, login_required,
    logout_user, current_user
)
from werkzeug.security import (
    generate_password_hash, check_password_hash
)

from flask import session

from app import app, db
from app.models import User, ShoppingList, Item


# ---------- דף בית ----------
@app.route("/")
@login_required
def home():
    return render_template("home.html")


# ---------- הרשמה / התחברות / התנתקות ----------
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if User.query.filter_by(username=username).first():
            session.pop('_flashes', None)  # ✅ רק לפני error
            flash("המשתמש כבר קיים", "error")
            return redirect(url_for("register"))

        user = User(username=username, password=generate_password_hash(password))
        db.session.add(user)
        db.session.commit()
        flash("ההרשמה הצליחה! התחבר/י כעת", "success")
        return redirect(url_for("login"))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            flash("התחברת בהצלחה ✅", "success")
            return redirect(url_for("home"))

        session.pop('_flashes', None)  # ✅ שומר שההודעה האדומה תישאר לבד
        flash("שם משתמש או סיסמה שגויים", "error")
        return redirect(url_for("login"))

    return render_template("login.html")


@app.route("/logout")
@login_required
def logout():
    session.pop('_flashes', None)  # ניקוי מוחלט
    logout_user()
    flash("התנתקת בהצלחה", "success")

    # DEBUG:
    print("DEBUG /logout -> flashes:", session.get('_flashes'))

    return redirect(url_for("login"))


# ---------- צפייה בכל הרשימות ----------
@app.route("/lists")
@login_required
def lists():
    user_lists = ShoppingList.query.filter_by(user_id=current_user.id).all()
    return render_template("lists.html", lists=user_lists)


# ---------- יצירת רשימה חדשה ----------
@app.route("/add-list", methods=["GET", "POST"])
@login_required
def add_list():
    if request.method == "POST":
        list_name = request.form.get("name").strip()
        items_text = request.form.get("items")

        new_list = ShoppingList(name=list_name, user_id=current_user.id)
        db.session.add(new_list)
        db.session.commit()

        if items_text:
            for line in items_text.splitlines():
                if not line.strip():
                    continue
                parts = [p.strip() for p in line.split(",")]
                name = parts[0]
                category = parts[1] if len(parts) > 1 else None
                db.session.add(Item(name=name, category=category, list_id=new_list.id))

            db.session.commit()

        flash("הרשימה נוספה בהצלחה ✅", "success")
        return redirect(url_for("lists"))

    return render_template("add_list.html")


# ---------- עריכת / מחיקת רשימה ----------
@app.route("/list/<int:list_id>/edit", methods=["GET", "POST"])
@login_required
def edit_list(list_id):
    s_list = ShoppingList.query.get_or_404(list_id)
    if s_list.user_id != current_user.id:
        abort(403)

    if request.method == "POST":
        new_name = request.form.get("name").strip()
        if new_name:
            s_list.name = new_name
            db.session.commit()
            flash("שם הרשימה עודכן ✅", "success")
        return redirect(url_for("lists"))

    return render_template("edit_list.html", s_list=s_list)


@app.route("/list/<int:list_id>/delete", methods=["POST"])
@login_required
def delete_list(list_id):
    s_list = ShoppingList.query.get_or_404(list_id)
    if s_list.user_id != current_user.id:
        abort(403)

    db.session.delete(s_list)
    db.session.commit()
    flash("הרשימה נמחקה 🗑️", "success")
    return redirect(url_for("lists"))


# ---------- עריכת / מחיקת פריט ----------
@app.route("/item/<int:item_id>/edit", methods=["GET", "POST"])
@login_required
def edit_item(item_id):
    item = Item.query.get_or_404(item_id)
    if item.list.user_id != current_user.id:
        abort(403)

    if request.method == "POST":
        item.name = request.form.get("name").strip()
        item.category = request.form.get("category").strip() or None
        db.session.commit()
        flash("הפריט עודכן ✅", "success")
        return redirect(url_for("lists"))

    return render_template("edit_item.html", item=item)


@app.route("/item/<int:item_id>/delete", methods=["POST"])
@login_required
def delete_item(item_id):
    item = Item.query.get_or_404(item_id)
    if item.list.user_id != current_user.id:
        abort(403)

    db.session.delete(item)
    db.session.commit()
    flash("הפריט נמחק 🗑️", "success")
    return redirect(url_for("lists"))


# ---------- המלצות (שלד) ----------
@app.route("/recommendations")
@login_required
def recommendations():
    return render_template("recommendations.html")
