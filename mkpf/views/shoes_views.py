from flask import Blueprint, url_for, request, render_template,flash
import os
from werkzeug.utils import redirect,secure_filename
from werkzeug.datastructures import CombinedMultiDict

from .. import db
from mkpf.models import Shoes,Marketprice,Platformprice
from ..forms import SearchShoes,ShoesModelCreateForm
from mkpf.views.auth_views import login_required
from mkpf.initclass import *
from sqlalchemy import func,nullslast,select
import urllib
import urllib.request
import time

from multiprocessing import Process

bp = Blueprint('shoes',__name__,url_prefix='/shoes')


@bp.route('/main/')
def main():
    #modelprice = Structureprice.query.group_by(Structureprice.code).all()
    modelprice = Platformprice.query.all()
    marketprice = Marketprice.query.all()
    model = Shoes.query.all()
    brands = Shoes.query.group_by(Shoes.brand)



    return render_template('shoes/main.html',modelprice=modelprice,marketprice=marketprice,model=model,brands=brands)








