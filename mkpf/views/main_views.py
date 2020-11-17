from flask import Blueprint, url_for,render_template,flash,g
from sqlalchemy import func
from werkzeug.utils import redirect
from mkpf.models import Shoes,Platformprice,Marketprice,User
from flask import request
from .market_views import process
from ..forms import SearchShoes
from .. import db

bp = Blueprint('main',__name__,url_prefix='/')

@bp.route('/')
def index():

    return redirect(url_for('shoes.main'))

@bp.route('/manger')
def mange():
    return render_template('auth/management.html')

@bp.route('/test')
def test():
    form = SearchShoes()

    return render_template('market/market_search.html',form=form)



@bp.route('/test2',methods=('GET','POST'))
def test2():
    form = SearchShoes()

    if request.method == 'POST' and form.validate_on_submit():

        if not (g.user.roles == 'admin' or g.user.roles == 'manager'):
            flash('현재권한으로는 사용할수없습니다..')
            return redirect(url_for('main.test2'))

        query_txt = form.content.data
        size = form.size.data
        quantity = form.quantity.data

        howmany = process(query_txt, size, quantity)
        flash(howmany)
        return redirect(url_for('market._list'))

    return render_template('market/market_search.html',form=form)

