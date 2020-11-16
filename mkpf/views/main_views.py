from flask import Blueprint, url_for,render_template
from sqlalchemy import func
from werkzeug.utils import redirect
from mkpf.models import Shoes,Platformprice,Marketprice,User

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
    # user = User.query.get_or_404()
    # db.session.delete(user)
    # db.session.commit()
    form = SearchShoes()


    return render_template('market/market_search2.html',form=form)


@bp.route('/test2')
def ttt():
    # shoes = Shoes.query.filter_by(code = 'DA1469-200').first()

    # db.session.query(Marketprice).delete()
    # db.session.commit()
    # #
    # word = Shoes.query.filter(Shoes.keyword.ilike('%%러버덩크 골드%%')).first()

    word =123

    return render_template('test/tests.html',word=word)

