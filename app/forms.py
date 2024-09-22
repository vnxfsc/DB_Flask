from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, FloatField
from wtforms.validators import DataRequired, ValidationError, EqualTo, NumberRange
from app.models import User


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password',
        validators=[DataRequired(), EqualTo('password')]
    )
    submit = SubmitField('注册')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')


class LoginForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired()])
    password = PasswordField('密码', validators=[DataRequired()])
    remember_me = BooleanField('记住我')
    submit = SubmitField('登录')

class EscrowForm(FlaskForm):
    buyer_id = IntegerField('买方ID', validators=[DataRequired()])
    seller_id = IntegerField('卖方ID', validators=[DataRequired()])
    amount = FloatField('金额', validators=[DataRequired(), NumberRange(min=0.01)])
    description = StringField('描述', validators=[DataRequired()])
    submit = SubmitField('创建担保交易')
