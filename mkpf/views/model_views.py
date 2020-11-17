from flask import Blueprint, url_for, request, render_template,flash,g
from werkzeug.utils import redirect,secure_filename
from .. import db
from mkpf.models import Shoes,Platformprice
from ..forms import SearchShoes,ShoesModelCreateForm
from mkpf.initclass import *
from mkpf.views.auth_views import login_required
import urllib
import urllib.request
from datetime import datetime
import time as t
from mkpf.views.market_views import process as mk_process
from mkpf.views.platform_views import process
bp = Blueprint('model',__name__,url_prefix='/model')

@bp.route('/create/', methods=['GET', 'POST'])
@login_required
def create():

    form = ShoesModelCreateForm()


    if request.method == 'POST' and form.validate_on_submit():

        if not (g.user.roles == 'admin' or g.user.roles == 'manager'):
            flash('현재권한으로는 사용할수없습니다.')
            return redirect(url_for('model.create'))
        
        model_path = os.path.join(os.getcwd(), r'mkpf/static/shoesmodels')
        if os.path.exists(model_path):
            pass
        else:
            os.makedirs(model_path)

        name = form.name.data
        price = form.price.data
        brand = form.brand.data
        code = form.code.data
        color = form.colorway.data
        keyword = form.keyword.data
        releasedate = form.releasedate.data
        uri=form.uri.data
        img = form.img.data

        exists_code = Shoes.query.filter_by(code=code).first()
        exists_name = Shoes.query.filter_by(name=name).first()
        # 기존의 만들어둔 모델이있는지 확인
        if not exists_code and not exists_name :
            # 파일저장
            # 경로일때
            if img == None:
                filename = secure_filename(name)+'.jpg'
                img_path = os.path.join(model_path, filename)
                #urlretrieve(다운이미지경로,저장위치및이름)
                urllib.request.urlretrieve(uri, img_path)

            # 로컬일떄
            else:
                filename = secure_filename(img.filename)
                if name in filename :
                    pass
                else:
                    filename = secure_filename(name)+'.jpg'
                img.save(os.path.join(model_path, filename))

            model = Shoes(code=code, img=filename, brand=brand,release_date=releasedate,name=name,colorway=color,retail_price=price,keyword=keyword)
            db.session.add(model)
            db.session.commit()

            howmany = process(code)
            howmany2 = mk_process(keyword)

            flash(howmany +'\n'+ howmany2)


            return redirect(url_for('model.view'))
        else:
            if exists_code :
                flash('이미 존재하는 모델넘버입니다.')
            else:
                flash('이미 존재하는 모델이름입니다.')

    return render_template('model/model_create.html',form=form)





@bp.route('/view/')
def view():
    form = ShoesModelCreateForm()
    forms = form.brand.choices

    items = Shoes.query.order_by(Shoes.release_date.desc())
    return render_template('model/model_list.html',forms=forms,items=items)



@bp.route('/modify/<int:shoes_id>', methods=('GET', 'POST'))
@login_required
def modify(shoes_id):
    model = Shoes.query.get_or_404(shoes_id)

    if not (g.user.roles == 'admin' or g.user.roles == 'manager'):
        flash('수정권한이 없습니다')
        return redirect(url_for('model.view'))
    if request.method == 'POST':

        form = ShoesModelCreateForm()
        if form.validate_on_submit():
            model_path = os.path.join(os.getcwd(), r'mkpf/static/shoesmodels')
            if os.path.exists(model_path):
                pass
            else:
                os.makedirs(model_path)

            form.populate_obj(model)
            uri = form.uri.data
            img = form.img.data
            if img == None:
                filename = secure_filename(form.name.data) + '.jpg'
                img_path = os.path.join(model_path, filename)
                # urlretrieve(다운이미지경로,저장위치및이름)
                urllib.request.urlretrieve(uri, img_path)

            # 로컬일떄
            else:
                filename = secure_filename(img.filename)
                if form.name.data in filename:
                    pass
                else:
                    filename = secure_filename(form.name.data) + '.jpg'
                img.save(os.path.join(model_path, filename))
            model.img = filename

            db.session.commit()
            flash('수정완료')
            return redirect(url_for('model.view'))
    else:
        form = ShoesModelCreateForm(obj=model)
    return render_template('model/model_create.html', form=form)

@bp.route('/delete/<int:shoes_id>')
@login_required
def delete(shoes_id):
    question = Shoes.query.get_or_404(shoes_id)

    if not (g.user.roles == 'admin' or g.user.roles == 'manager') :
        flash('삭제권한이 없습니다')
        return redirect(url_for('model.view'))
    db.session.delete(question)
    db.session.commit()
    return redirect(url_for('model.view'))

@bp.route('/detail/<code>' , methods=['GET', 'POST'])
@login_required
def detail(code):
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
        start = t.time()
        howmany = process(code)
        checktime = t.time()
        hw=mk_process(shoes.keyword)

        flash(howmany+'\n'+hw)

        return redirect(url_for('model.detail',code=code))

    return render_template('model/model_detail.html',shoes=shoes,model_list=model_list,page=page,so=so,code=code,search_date=search_date,now=now)






#----------------------------------------------------
# ------------------- old version -------------------
#----------------------------------------------------

@bp.route('/oldview/')
def old_view():
    form = ShoesModelCreateForm()
    forms = form.brand.choices

    items = Shoes.query.order_by(Shoes.release_date.desc())
    return render_template('model/old_model_list.html',forms=forms,items=items)


@bp.route('/oldcreate/', methods=['GET', 'POST'])
def old_create():
    form = ShoesModelCreateForm()


    if request.method == 'POST' and form.validate_on_submit():

        model_path = os.path.join(os.getcwd(), r'mkpf/static/shoesmodels')
        if os.path.exists(model_path):
            pass
        else:
            os.makedirs(model_path)

        name = form.name.data
        price = form.price.data
        brand = form.brand.data
        code = form.code.data
        color = form.colorway.data
        keyword = form.keyword.data
        releasedate = form.releasedate.data
        uri=form.uri.data
        img = form.img.data

        exists_code = Shoes.query.filter_by(code=code).first()
        exists_name = Shoes.query.filter_by(name=name).first()
        # 기존의 만들어둔 모델이있는지 확인
        if not exists_code and not exists_name :
            # 파일저장
            # 경로일때
            if img == None:
                filename = secure_filename(name)+'.jpg'
                img_path = os.path.join(model_path, filename)
                #urlretrieve(다운이미지경로,저장위치및이름)
                urllib.request.urlretrieve(uri, img_path)

            # 로컬일떄
            else:
                filename = secure_filename(img.filename)
                if name in filename :
                    pass
                else:
                    filename = secure_filename(name)+'.jpg'
                img.save(os.path.join(model_path, filename))

            model = Shoes(code=code, img=filename, brand=brand,release_date=releasedate,name=name,colorway=color,retail_price=price,keyword=keyword)
            db.session.add(model)
            db.session.commit()
            howmany = process(code)

            flash(howmany)

            return redirect(url_for('model.view'))
        else:
            if exists_code :
                flash('이미 존재하는 모델넘버입니다.')
            else:
                flash('이미 존재하는 모델이름입니다.')

    return render_template('model/old_model_create.html',form=form)