from flask import Blueprint, url_for, request, render_template,flash,redirect,g
from mkpf.models import Platformprice
from mkpf.views.auth_views import login_required

from mkpf.views.market_views import process as mk_process
from datetime import datetime
from ..models import Shoes
import time as t
from .. import db
from mkpf.initclass import *



bp = Blueprint('platform',__name__,url_prefix='/platform')




@bp.route('/list/')
@login_required
def _list():
    page = request.args.get('page', type=int, default=1)
    kw = request.args.get('kw', type=str, default='')
    so = request.args.get('so',type=str, default='recent')

    #정렬
    if so == 'expensive':
        shoes_list = Platformprice.query.order_by(Platformprice.price.desc())
    elif so =='popular':
        shoes_list = Platformprice.query.order_by(Platformprice.size.desc())
    else : #최신수
        shoes_list = Platformprice.query.order_by(Platformprice.id.desc())
    t123t=''
    #검색
    if kw:
        search = '%%{}%%'.format(kw.strip())

        match = Shoes.query.filter(Shoes.name.ilike(search) |Shoes.keyword.ilike(search) | Shoes.subname.ilike(search)).first()
        if match :
            search = match.code
        if so == 'expensive':
            shoes_list = Platformprice.query.filter_by(code=search).order_by(Platformprice.price.desc())
        elif so == 'popular':
            shoes_list = Platformprice.query.filter_by(code=search).order_by(Platformprice.size.desc())
        else:  # 최신수
            shoes_list = Platformprice.query.filter_by(code=search).order_by(Platformprice.id.desc())



    shoes_list = shoes_list.paginate(page, per_page=10)
    items=shoes_list.items
    shoes_match=[]
    for index,i in enumerate(items):
        shoes_match.append((Shoes.query.filter_by(code=i.code).first()))



    return render_template('platform/platform_list.html',shoes_match=shoes_match, shoes_list=shoes_list,page=page,kw=kw,so=so)


def process(code):
    xxblue_total = []
    xb = Xxblue(code)
    xb.start()
    title,img_name = xb.search()
    tablenum = xb.element_generate()
    xb_obj = xb.parser()
    search_date = datetime.now()
    xb.driver.quit()

    print('subname:',title)
    # 모델 서브네임이없을 경우 추가한다.
    shoesmodel = Shoes.query.filter(Shoes.code ==code).first()
    if shoesmodel.subname == None:
        shoesmodel.subname = title

    num = 0
    # 중복값 비교
    comparison = Platformprice.query.filter(Platformprice.code.like(code)).order_by(Platformprice.id.desc()).first()

    if '없음' in xb_obj[0][0]:
        pass
    else:
        for i in xb_obj:

            size = i[0]
            price = int(i[1].replace(',', '').replace('원', ''))
            saleday = datetime.strptime(i[2], '%Y.%m.%d')
            # comparison 기존데이터 유무
            if comparison != None :
                if comparison.code == code and comparison.saleday ==saleday and comparison.price == price :
                    break
                else:
                    pass
            else : pass
            xxblue_total.insert(0, Platformprice(code=code,saleday=saleday,price=price,size=size,search_date=search_date))
            num +=1

        db.session.bulk_save_objects(xxblue_total)

    db.session.commit()

    return ('PlatForm 찾은값:{} DB에 저장한값:{}'.format(tablenum,num))

#----------------------------------------------------
# ------------------- old version -------------------
#----------------------------------------------------

@bp.route('/olddetail/<code>')
@login_required
def old_detail(code):
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

        return redirect(url_for('platform.detail',code=code))

    return render_template('platform/old_platform_list.html', model_list=model_list,page=page,so=so,code=code,search_date=search_date,now=now)


