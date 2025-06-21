from flask import Flask, redirect, url_for, request
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from db import engine, SessionLocal, User, Bet, Lottery, Request, create_db
from werkzeug.security import generate_password_hash, check_password_hash
from config import FLASK_SECRET

app = Flask(__name__)
app.secret_key = FLASK_SECRET
admin = Admin(app, name="骰子Bot后台", template_mode="bootstrap4")
login_manager = LoginManager(app)

session = SessionLocal()

class AdminUser(UserMixin):
    def __init__(self, dbuser):
        self.id = dbuser.id
        self.username = dbuser.name
        self.password = dbuser.password
        self.is_admin = dbuser.is_admin

    @staticmethod
    def get(user_id):
        u = session.query(User).filter_by(id=user_id).first()
        if u and u.is_admin:
            return AdminUser(u)
        return None

@login_manager.user_loader
def load_user(user_id):
    return AdminUser.get(user_id)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        name = request.form['username']
        pw = request.form['password']
        u = session.query(User).filter_by(name=name, is_admin=True).first()
        if u and check_password_hash(u.password, pw):
            login_user(AdminUser(u))
            return redirect('/admin')
        return "登录失败"
    return '''<form method="post">用户名: <input name="username"/> 密码: <input name="password" type="password"/><input type="submit"/></form>'''

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/login')

class SecureModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin

admin.add_view(SecureModelView(User, session))
admin.add_view(SecureModelView(Bet, session))
admin.add_view(SecureModelView(Lottery, session))
admin.add_view(SecureModelView(Request, session))

if __name__ == "__main__":
    create_db()
    app.run(host="0.0.0.0", port=8080, debug=True)
