from flask import Blueprint, url_for,render_template
from sqlalchemy import func
from werkzeug.utils import redirect
from mkpf.models import Shoes,Platformprice,Marketprice

from ..forms import SearchShoes
from .. import db

bp = Blueprint('main',__name__,url_prefix='/')

@bp.route('/')
def index():
    return redirect(url_for('shoes.main'))

@bp.route('/test')
def test():
    model = Shoes.query.all()
    modelprice = Platformprice.query.all()
    marketprice = Marketprice.query.all()

    # 인기모델 9 제품
    best9 = Platformprice.query.order_by(func.count(Platformprice.id).desc()).group_by(Platformprice.code).limit(
        10).all()
    topnine = []
    for i in best9:
        nine = i.code
        topnine_obj = Shoes.query.filter(Shoes.code == nine).first()

        topnine.append(topnine_obj)


    return render_template('shoes/main.html',topnine=topnine,model=model,modelprice=modelprice,marketprice=marketprice)

