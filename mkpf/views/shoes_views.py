from flask import Blueprint, url_for, request, render_template,flash
import os
from werkzeug.utils import redirect,secure_filename
from werkzeug.datastructures import CombinedMultiDict

from .. import db
from mkpf.models import Shoes,Marketprice,Platformprice
from ..forms import SearchShoes,ShoesModelCreateForm
from mkpf.views.auth_views import login_required
from mkpf.initclass import *
from sqlalchemy import func,over,literal
import urllib
import urllib.request
import time

from multiprocessing import Process

bp = Blueprint('shoes',__name__,url_prefix='/shoes')


@bp.route('/main/')
def main():
    sc = request.args.get('sc', type=int, default='default')
    if sc =='':
        sc = 'default'
    form = SearchShoes()

    #modelprice = Structureprice.query.group_by(Structureprice.code).all()
    modelprice = Platformprice.query.all()
    marketprice = Marketprice.query.all()
    model = Shoes.query.all()
    brands = Shoes.query.group_by(Shoes.brand)

    # 인기모델 5 제품
    best5 = Platformprice.query.order_by(func.count(Platformprice.id).desc()).group_by(Platformprice.code).limit(
        5).all()
    topfive = []
    detail=[]
    for i in best5:
        five = i.code
        topfive_obj = Shoes.query.filter(Shoes.code == five).first()

        topfive.append(topfive_obj)
        detail_obj = db.session.query(Platformprice.size, func.count(Platformprice.id).label('sizecount'),
                                    func.avg(Platformprice.price).label('avg'))\
            .group_by(Platformprice.code, Platformprice.size).having(Platformprice.code == five)
        sizedict = {}
        for dic_init in form.size.choices[1:]:
            sizedict[int(dic_init[0])] = {'avg':0,'count':0}

        for j in detail_obj:
            sizedict[j.size] = {'avg': j.avg,'count': j.sizecount}

        detail.append(sizedict)



    return render_template('shoes/main.html',modelprice=modelprice,sc=sc,form=form,
                           detail=detail,marketprice=marketprice,model=model,brands=brands,topfive=topfive)

@bp.route('/test/')
def test():

    sizecode = db.session.query( Platformprice.code,Platformprice.size,func.count(Platformprice.id).label('sizecount'),func.avg(Platformprice.price).label('avg') )\
        .group_by(Platformprice.code,Platformprice.size).having(Platformprice.code=='CU6015-700')
    form = SearchShoes()

    sizedict = {}
    for dic_init in form.size.choices[1:]:
        sizedict[int(dic_init[0])] = {'avg': 0, 'count': 0}

    for i in sizecode:
        sizedict[i.size] = i.avg



    # 인기모델 5 제품
    best5 = Platformprice.query.order_by(func.count(Platformprice.id).desc()).group_by(Platformprice.code).limit(5).all()
    model=[]
    for i in best5:
        five = i.code
        topfive_obj = Shoes.query.filter(Shoes.code == five).first()

        model.append(topfive_obj)


    return render_template('test/test.html',model=model,sizecode=sizecode,best5=best5,sizedict=sizedict)






