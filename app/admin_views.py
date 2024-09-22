from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required
from app import db
from app.models import User

admin_bp = Blueprint('admin', __name__, template_folder='templates')


@admin_bp.route('/', methods=['GET'])
@login_required
def admin_index():
    users = User.query.all()
    return render_template('admin/index.html', users=users)


@admin_bp.route('/delete_user/<int:id>', methods=['POST'])
@login_required
def delete_user(id):
    user = User.query.get(id)
    if user:
        db.session.delete(user)
        db.session.commit()
        flash('用户已删除')
    else:
        flash('用户未找到')
    return redirect(url_for('admin.admin_index'))