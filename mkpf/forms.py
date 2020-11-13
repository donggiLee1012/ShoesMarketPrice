from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField,PasswordField,SelectField,IntegerField,validators,RadioField
from wtforms.fields.html5 import EmailField,DateField
from flask_wtf.file import FileField, FileRequired
from wtforms.validators import DataRequired,Length,EqualTo,Email

roles_list=[('admin','관리자'),('manager','매니저'),('common','민간인')]

class UserManagement(FlaskForm):
    username = StringField('사용자이름', validators=[DataRequired(), Length(min=3, max=25)])
    email = EmailField('이메일', [DataRequired('이메일은 필수입력 항목입니다.'), Email()])
    roles = SelectField('권한',choices=roles_list,coerce=str)

class UserCreateForm(FlaskForm):
    username = StringField('사용자이름', validators=[DataRequired(), Length(min=3, max=25)])
    password1 = PasswordField('비밀번호', validators=[DataRequired(), EqualTo('password2', '비밀번호가 일치하지 않습니다')])
    password2 = PasswordField('비밀번호확인', validators=[DataRequired()])
    roles = SelectField('권한', choices=roles_list, coerce=str)
    email = EmailField('이메일', [DataRequired('이메일은 필수입력 항목입니다.'), Email()])


class UserLoginForm(FlaskForm):
    username = StringField('사용자이름',validators=[DataRequired(), Length(min=3,max=25)])
    password = PasswordField('비밀번호',validators=[DataRequired()])

cho =[('','선택안함')]
for i in range(210,315,5):
    cho.append((str(i),str(i)+'mm'))

class SearchShoes(FlaskForm):
    quantity = IntegerField('건수',validators=[validators.NumberRange(min=1,max=100)])
    size = SelectField('사이즈',choices=cho,coerce=str)
    content = StringField('내용',validators=[DataRequired('검색하실 신발명을 입력하세요.')])

brands=[('nike','나이키'),('adidas','아디다스'),('converse','컨버스'),('newbalance','뉴발란스'),('jordan','조던')]

class ShoesModelCreateForm(FlaskForm):
    name = StringField('제품명',validators=[DataRequired('제품코드를 입력 하세요.')])
    code = StringField('제품코드',validators=[DataRequired('제품코드를 입력 하세요.')])
    uri = StringField('모델사진')
    img = FileField('모델사진')
    brand = SelectField('브랜드',choices=brands,coerce=str)
    releasedate = DateField('발매일',validators=[DataRequired()],format='%Y-%m-%d')
    price = IntegerField('발매가', validators=[validators.NumberRange(min=0)])
    colorway = StringField('색상',validators=[DataRequired('내용은 필수입력 항목입니다.')])
    keyword = StringField('키워드',validators=[DataRequired(),Length(min=3)])
    #hashtag = StringField('키워드',validators=[DataRequired('해쉬태그를 입력해주세요.')])

