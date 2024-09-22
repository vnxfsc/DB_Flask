from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user

admin_bp = Blueprint('admin', __name__)


@admin_bp.before_request
def before_request():
    if not current_user.is_authenticated or not current_user.is_admin:
        flash('您没有访问此页面的权限。')
        return redirect(url_for('front.index'))


@admin_bp.route('/')
@login_required
def admin_index():
    from app.models import User
    users = User.query.all()
    return render_template('admin/index.html', users=users)