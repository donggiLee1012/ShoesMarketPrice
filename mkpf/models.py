from mkpf import db

class Shoes(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(50),unique=True)
    subname = db.Column(db.String(50))
    code = db.Column(db.String(30), unique=True)
    img = db.Column(db.Text())
    brand = db.Column(db.String(30),nullable=False)
    retail_price = db.Column(db.Integer,default=0)
    release_date = db.Column(db.DateTime())
    colorway = db.Column(db.Text())

class Marketprice(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(200),nullable=False)
    condition = db.Column(db.String(20),default='새상품')
    size = db.Column(db.String(30))
    price = db.Column(db.Integer,default=0)
    seller = db.Column(db.String(30))
    upload_date = db.Column(db.DateTime())
    uri = db.Column(db.Text())
    img = db.Column(db.Text())
    search_query = db.Column(db.String(30))
    shoesmodel_id = db.Column(db.String(30), db.ForeignKey('shoes.id',onupdate='CASCADE'))
    shoesmodel = db.relationship('Shoes', backref=db.backref('sales_set'))

class Platformprice(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    code = db.Column(db.String(30), db.ForeignKey('shoes.code',onupdate='CASCADE'))
    platform_price = db.relationship('Shoes', backref=db.backref('platform_price_set', cascade='delete'))
    saleday = db.Column(db.DateTime(), nullable=False)
    search_date = db.Column(db.DateTime())
    price = db.Column(db.Integer,default=0)
    size = db.Column(db.Integer,default=200)
    platform = db.Column(db.String(30))


class User(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(150),unique=True,nullable=False)
    password = db.Column(db.String(200),nullable=False)
    email = db.Column(db.String(120),unique=True,nullable=False)

