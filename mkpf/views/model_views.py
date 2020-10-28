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



bp = Blueprint('model',__name__,url_prefix='/model')

@bp.route('/create/', methods=['GET', 'POST'])
def create():
    form = ShoesModelCreateForm()
    loading = url_for('static',filename='ajax-loader.gif')

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
        releasedate = form.releasedate.data
        uri=form.uri.data
        img = form.img.data

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

        model = Shoes(code=code, img=filename, brand=brand,release_date=releasedate,name=name,colorway=color,retail_price=price)
        db.session.add(model)
        db.session.commit()
        howmany = process(code)

        flash(howmany)

        return redirect(url_for('model.view'))



    else:
        return render_template('model/model_create.html',form=form,loading=loading)




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

    if g.user.username != '1234':
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

    if g.user.username != '1234':
        flash('삭제권한이 없습니다')
        return redirect(url_for('model.view'))
    db.session.delete(question)
    db.session.commit()
    return redirect(url_for('model.view'))

def process(code):
    xxblue_total = []
    xb = Xxblue(code)
    xb.start()
    title,img_name = xb.search()
    tablenum = xb.element_generate()
    xb_obj = xb.parser()
    search_date = datetime.now()
    xb.driver.quit()


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

    return ('찾은값:{} DB에 저장한값:{}'.format(tablenum,num))


@bp.route('/test/')
def test22():
    q=Shoes.query.get(1)
    db.session.delete(q)
    db.session.commit()

    return render_template('test/test.html')