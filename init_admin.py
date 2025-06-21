from db import SessionLocal, User
from werkzeug.security import generate_password_hash

def create_admin():
    session = SessionLocal()
    admin = session.query(User).filter_by(name="admin").first()
    if not admin:
        admin = User(
            tg_id=100000001, name="admin", password=generate_password_hash("adminpass"), is_admin=True
        )
        session.add(admin)
        session.commit()
    print("超级管理员账号已创建，用户名：admin 密码：adminpass")

if __name__ == '__main__':
    create_admin()
