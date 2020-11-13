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