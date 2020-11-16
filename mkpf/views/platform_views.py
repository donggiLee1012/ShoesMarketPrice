from flask import Blueprint, url_for, request, render_template,flash,redirect
from mkpf.models import Platformprice
from mkpf.views.auth_views import login_required
from mkpf.views.model_views import process
from mkpf.views.market_views import process as mk_process
from datetime import datetime
from ..models import Shoes
import time
from multiprocessing import Process,Manager,Queue


bp = Blueprint('platform',__name__,url_prefix='/platform')

@bp.route('/list/<code>',methods=('GET','POST'))
@login_required
def _list(code):
    shoes=Shoes.query.filter_by(code=code).first()

    page = request.args.get('page', type=int, default=1)
    so = request.args.get('so',type=str, default='recent')
    now = datetime.now()
    #정렬
    if so == 'expensive':
        model_list = Platformprice.query.filter(Platformprice.code.ilike(code)).order_by(Platformprice.price.desc())
    elif so =='popular':
        model_list = Platformprice.query.filter(Platformprice.code.ilike(code)).order_by(Platformprice.size.desc())
    else : #최신수
        model_list = Platformprice.query.filter(Platformprice.code.ilike(code)).order_by(Platformprice.saleday.desc())


    model_list = model_list.paginate(page, per_page=10)
    search_date = Platformprice.query.filter(Platformprice.code.ilike(code)).order_by(Platformprice.search_date.desc()).first()
    if search_date.search_date is None:
        search_date = Platformprice.query.filter(Platformprice.code.ilike(code)).order_by(Platformprice.saleday.desc()).first().saleday
    else :
        search_date = search_date.search_date

    if request.method == 'POST':
        start = time.time()
        howmany = process(code)
        checktime = time.time()
        hw=mk_process(shoes.keyword)

        flash(howmany+hw)

        return redirect(url_for('platform._list',code=code))




    return render_template('platform/platform_list.html', model_list=model_list,page=page,so=so,code=code,search_date=search_date,now=now)
