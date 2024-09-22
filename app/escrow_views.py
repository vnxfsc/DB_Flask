from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required
from app import db
from app.forms import EscrowForm
from app.models import Escrow

escrow_bp = Blueprint('escrow', __name__, template_folder='templates')


@escrow_bp.route('/create_escrow', methods=['GET', 'POST'])
@login_required
def create_escrow():
    form = EscrowForm()
    if form.validate_on_submit():
        escrow = Escrow(
            buyer_id=form.buyer_id.data,
            seller_id=form.seller_id.data,
            amount=form.amount.data,
            description=form.description.data
        )
        db.session.add(escrow)
        db.session.commit()
        flash('担保交易已创建！')
        return redirect(url_for('escrow.view_escrows'))
    return render_template('escrow/create_escrow.html', form=form)


@escrow_bp.route('/view_escrows', methods=['GET'])
@login_required
def view_escrows():
    escrows = Escrow.query.all()
    return render_template('escrow/view_escrows.html', escrows=escrows)