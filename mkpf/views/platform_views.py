from flask import Blueprint, url_for, request, render_template,flash
from mkpf.models import Platformprice
from mkpf.views.auth_views import login_required



bp = Blueprint('platform',__name__,url_prefix='/platform')

@bp.route('/list/<code>')
@login_required
def _list(code):
    page = request.args.get('page', type=int, default=1)
    so = request.args.get('so',type=str, default='recent')

    #정렬
    if so == 'expensive':
        model_list = Platformprice.query.filter(Platformprice.code.ilike(code)).order_by(Platformprice.price.desc())
    elif so =='popular':
        model_list = Platformprice.query.filter(Platformprice.code.ilike(code)).order_by(Platformprice.size.desc())
    else : #최신수
        model_list = Platformprice.query.filter(Platformprice.code.ilike(code)).order_by(Platformprice.saleday.desc())


    model_list = model_list.paginate(page, per_page=10)

    return render_template('platform/platform_list.html', model_list=model_list,page=page,so=so,code=code)