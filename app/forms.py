from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, \
    TextAreaField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, \
    Length
from flask_babel import _, lazy_gettext as _l
from app.models import User


class LoginForm(FlaskForm):
    username = StringField(_l('用户名'), validators=[DataRequired()])
    password = PasswordField(_l('密码'), validators=[DataRequired()])
    remember_me = BooleanField(_l('记住'))
    submit = SubmitField(_l('登入'))


class RegistrationForm(FlaskForm):
    username = StringField(_l('用户名'), validators=[DataRequired()])
    email = StringField(_l('Email'), validators=[DataRequired(), Email()])
    password = PasswordField(_l('密码'), validators=[DataRequired()])
    password2 = PasswordField(
        _l('重复密码'), validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField(_l('申请'))

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError(_('已有重复，请更换.'))

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError(_('邮件已使用，请更换.'))


class RestPasswordRequestForm(FlaskForm):
    email = StringField(_l('Email'), validators=[DataRequired(), Email()])
    submit = SubmitField(_l('重置密码'))


class ResetPasswordForm(FlaskForm):
    password = PasswordField(_l('密码'), validators=[DataRequired()])
    password2 = PasswordField(
        _l('重复密码'), validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField(_l('重置密码'))


class EditProfileForm(FlaskForm):
    username = StringField(_l('用户名'), validators=[DataRequired()])
    about_me = TextAreaField(_l('关于我'), validators=[Length(min=0, max=140)])
    submit = SubmitField(_l('提交'))

    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError(_('用户名重复，请换一个试试'))


class PostForm(FlaskForm):
    post = TextAreaField(_l('说点什么吧：'), validators=[
        DataRequired(), Length(min=1, max=140)])
    submit = SubmitField(_l('发布'))