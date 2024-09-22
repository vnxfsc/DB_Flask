from app import create_app, db
from app.models import User
from werkzeug.security import generate_password_hash

app = create_app()
app.app_context().push()

admin_username = 'vnxfsc'
admin_password = 'vnxfsc'

if not User.query.filter_by(username=admin_username).first():
    admin = User(username=admin_username, password_hash=generate_password_hash(admin_password), is_admin=True)
    db.session.add(admin)
    db.session.commit()
    print(f'Admin 用户 {admin_username} 创建成功.')
else:
    print(f'Admin 用户 {admin_username} 创建失败.')