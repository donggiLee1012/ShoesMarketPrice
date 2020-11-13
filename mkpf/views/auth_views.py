from flask import Blueprint, url_for, render_template, flash, request,session,g
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import redirect

from mkpf import db
from mkpf.forms import UserCreateForm,UserLoginForm,UserManagement
from mkpf.models import User
import functools

bp = Blueprint('auth',__name__,url_prefix='/auth')

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view


@bp.route('/signup',methods=('GET','POST'))
def signup():
    form = UserCreateForm()
    if request.method =='POST' and form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        email = User.query.filter_by(email=form.email.data).first()
        if not user and not email:
            user = User(username=form.username.data,
                        password = generate_password_hash(form.password1.data),
                        email=form.email.data,
                        roles=form.roles.data)
            db.session.add(user)
            db.session.commit()

            return redirect(url_for('shoes.main'))
        else:
            if user :
                flash('이미 존재하는 사용자입니다.')
            else:
                flash('이미 사용중인 이메일입니다.')
    return render_template('auth/signup.html',form=form)

@bp.route('/login/',methods=('GET','POST'))
def login():
    form = UserLoginForm()
    if request.method =='POST' and form.validate_on_submit():
        error = None
        user = User.query.filter_by(username=form.username.data).first()
        if not user:
            error = '존재하지 않는 사용자입니다.'
        elif not check_password_hash(user.password,form.password.data):
            error = '비밀번호가 올바르지 않습니다.'
        if error is None:
            session.clear()
            session['user_id'] = user.id
            return redirect(url_for('shoes.main'))
        flash(error)

    return render_template('auth/login.html',form=form)

@bp.route('/management/',methods=('GET','POST'))
@login_required
def management():

    form = UserManagement()

    if g.user.roles == "admin" :
        users = User.query.all()
    else :
        users = User.query.filter(User.roles != 'admin').all()

    if request.method == 'POST' and form.validate_on_submit():

        user = User.query.filter_by(username=form.username.data).first()

        form.populate_obj(user)

        db.session.commit()

        return redirect(url_for('auth.management'))

    return render_template('auth/management.html',users=users,form=form)


@bp.route('/delete/<int:user_id>')
@login_required
def delete(user_id):
    user = User.query.get_or_404(user_id)

    if g.user.roles != 'admin':
        flash('삭제권한이 없습니다')
        return redirect(url_for('auth.management'))
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('auth.management'))



@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = User.query.get(user_id)




@bp.route('/logout/')
def logout():
    session.clear()
    return redirect(url_for('shoes.main'))
