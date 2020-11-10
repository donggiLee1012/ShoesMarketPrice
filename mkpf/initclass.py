from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import os, re, sys
import time as t
from datetime import *
import math
import urllib
import urllib.request
import platform
import random
from fake_useragent import UserAgent


class Driver:
    __driverpath = os.path.join(os.path.dirname(__file__))

    if platform.system() == 'Windows' :
        __driverpath += r'/chromedriver.exe'
        imgpath = r'C:\projects\shoesprice\mkpf\static\crawling_data\img\{}'
    else:
    # elif platform.system() == 'Linux':
        print(platform.system())
        __driverpath += r'/chromedriver'
        imgpath = r'/home/multidong1017/projects/shoesprice/mkpf/static/crawling_data/img/{}'


    target = 'ddd'

    time_marker = datetime.now().strftime('%y%m%d_%H')
    dirname = 'hi'



    def __init__(self,query_txt='',size ='',quantity =100):
        self.query_txt = query_txt
        self.size = size
        self.quantity = quantity

        self.imgpath = Driver.imgpath.format(self.dirname)
        if os.path.exists(self.imgpath):
            pass
        else:
            os.makedirs(self.imgpath)

    def start(self):
        # windows, linux ok

        # fake-useragent
        ua = UserAgent(verify_ssl=False)
        useragent = ua.random

        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('window-size=1920x1080')
        options.add_argument("lang=ko_KR")
        options.add_argument(f'user-agent={useragent}')
        # options.add_argument('--start-fullscreen')

        self.driver = webdriver.Chrome(executable_path=Driver.__driverpath, options=options)
        self.driver.implicitly_wait(10)
        self.driver.get(self.target)

    def img_save(self,url,name):
        # name = 확장명까지 써야함
        save_path = os.path.join(self.imgpath,name)
        urllib.request.urlretrieve(url, save_path)

    def db_save(self):
        return 1

    def pprint(self):
        print(self.query_txt,self.size,self.quantity)


class Foostsell(Driver):
    target = 'https://footsell.com/g2/bbs/board.php?bo_table=m51&r=ok'
    basetarget = 'https://footsell.com'
    dirname = 'footsell'

    def search(self):
        # 검색
        search_box = self.driver.find_element_by_css_selector('#list_search_text_input')
        search_box.send_keys(self.query_txt)
        search_box.send_keys(Keys.ENTER)

        # 사이즈별 선택한게있으면 실행
        if self.size != '':
            input_size = 'option[value="' + '{}"]'.format(self.size)
            size_select = self.driver.find_element(By.CSS_SELECTOR, input_size)
            size_select.click()

    def soup_make(self):
        soup_list = []
        for j in range(math.ceil(self.quantity / 40)):

            t.sleep(1)
            html = self.driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
            t.sleep(1)
            border_list = soup.find_all(id=re.compile('list_row_'))

            if border_list == []:
                border_list = '결과안잡힘'
                soup_list.append(border_list)
                break

            if self.query_txt == '':
                border_list = border_list[3:]

            soup_list.append(border_list)

            try:
                self.driver.find_elements(By.CSS_SELECTOR, 'ul>li>a')[j].send_keys(Keys.ENTER)
            except:
                break

        return soup_list
    def parser(self, soup_list):

        title = []
        condition = []
        size = []
        price = []
        seller = []
        uploadtime = []
        uri = []
        img = []

        count = 0

        for border_list in soup_list:

            for border_list_att in border_list:
                # 제목
                try:
                    title_att = border_list_att.find('span', id=re.compile('^list_subject_')).text.strip()

                except:
                    title_att = border_list_att.find('span', class_='smallfont color_aaa').text.strip()

                # 컨디션
                condition_att = border_list_att.find('span', class_='list_market_used han').text

                # 사이즈
                size_att = border_list_att.find('span', class_='list_market_size').text

                # 가격
                try:
                    # 금액
                    price_att = border_list_att.find('div', class_=re.compile('^list_market_price')).text.strip()
                    price_att = int(price_att[1:].replace(',',''))

                except AttributeError:
                    # 금액 0
                    price_att = 0

                except:
                    # 거래종료
                    price_att = border_list_att.find('span', class_='color_aaa normal smallfont').text.strip()
                    price_att = 0

                # 판매자명
                seller_att = border_list_att.find('div', class_=re.compile('^float_left list_market_name')).text.strip()

                # 업로드 시각
                uploadtime_att = border_list_att.find('span', class_='list_table_dates').text.strip()

                # uri
                uri_att = border_list_att.find('a').get('href')

                # img
                img_att = Foostsell.basetarget + border_list_att.find('img').get('src')

                if ':' in uploadtime_att:
                    uploadtime_att = datetime.now()
                else:

                    uploadtime_att = datetime.strptime('20' + uploadtime_att, '%Y-%m-%d').date()

                title.append(title_att)
                condition.append(condition_att)
                size.append(size_att)
                price.append(price_att)
                seller.append(seller_att)
                uploadtime.append(uploadtime_att)
                uri.append(uri_att)
                img.append(img_att)

                count += 1
                if count == self.quantity:
                    break

        return zip(title, condition, size, price, seller, uploadtime, uri, img),count

class Xxblue(Driver):
    target = 'https://www.xxblue.com/'
    dirname ='xxblue'

    def search(self):
        self.driver.find_element_by_css_selector('.search-btn').click()

        search = self.driver.find_element_by_name('keyword')

        search.send_keys(self.query_txt)

        search.send_keys(Keys.ENTER)

        # 첫번째 상품
        try:
            # web 변경되면서 속성바뀜
            #self.driver.find_elements_by_css_selector("div[class^='rarex-grid-product product']")[0].click()
            self.driver.find_elements_by_css_selector('.item')[0].click()
        except:
            print('검색결과없음')

        self.driver.implicitly_wait(10)
        title=self.driver.find_element_by_css_selector('.product-detail-container > .product-subname').text
        img_name = self.driver.find_element_by_css_selector('.product-detail-container > .product-name').text.replace(' ','').lower()
        # 입찰 현황 더보기란 클릭
        # or driver.find_element_by_id('latestTransactionMore').click()
        self.driver.find_element_by_id('asknMore').click()
        t.sleep(0.5)

        # 거래가격 탭 클릭
        self.driver.find_element_by_css_selector('label[for="transactedPrice"]').click()

        #uri = self.driver.current_url
        return title,img_name

    def element_generate(self):
        current =0
        while 1:
            table_td = self.driver.find_elements_by_css_selector('#transactedPriceTable tr')
            # ELEMENT 가 화면에 보이도록 스크롤 조정 --> 아래 부분 추가로 확장됨
            self.driver.execute_script("arguments[0].scrollIntoView(true);", table_td[-1])
            t.sleep(1)
            if current != len(table_td):
                current = len(table_td)
            else:
                break
        return len(table_td)

    def parser(self):
        objs = []
        html = self.driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        saledatas = soup.select('#transactedPriceTable tr')
        #
        # a = soup.find(class_='product-info').text
        # shoesmodel_id = re.search('(스타일코드\s)(.*)(\s)',a).group(2)
        for i in saledatas:
            column = []
            for j in i.select('td'):
                column.append(j.text)
            objs.append(column)

        return objs

class Bgjt(Driver):
    target ='https://m.bunjang.co.kr/'
    dirname = 'Bgjt'

    def search(self):
        # 검색
        search = self.driver.find_element_by_css_selector('input[type="text"]')

        search.send_keys(self.query_txt)

        search.send_keys(Keys.ENTER)

    def soup_make(self, soup_list=[]):

        for j in range(math.ceil(self.quantity / 40)):
            t.sleep(1)
            html = self.driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
            t.sleep(1)
            salelist = soup.select("div[class$='fUCDDC']")

            if salelist == []:
                salelist = '결과안잡힘'
                soup_list.append(salelist)
                break

            soup_list.append(salelist)

            try:
                self.driver.find_elements_by_css_selector("a[class$='cAiauy']")[0].text
            except:
                break
        return soup_list


    def parser(self, soup_list) :
        title = []
        condition = []
        size = []
        price = []
        seller = []
        uploadtime = []
        uri = []
        img = []
        count=0
        for soup_list_num in soup_list :
            for border_list in soup_list_num:
                # title
                title_att = border_list.find(class_=re.compile("dYmkxB$")).text
                print(title_att)

                # price
                try:
                    price_att = border_list.find(class_=re.compile("UVCRv$")).text.replace(',','')
                except:
                    # 연락요망
                    price_att = 0
                print(price_att)

                condition_att = '알수없음'
                size_att ='???mm'
                seller_att = '번개장터'

                # url
                uri_att = border_list.find(class_=re.compile("JQKtC$")).get('href')

                # date 광고이면 AD
                if border_list.find(class_=re.compile("dhsjSi")).text == 'AD':
                    uploadtime_att = '광고'
                else:
                    uploadtime_att = border_list.find(class_=re.compile("dhsjSi")).text

                # img
                img_att = border_list.find("img", alt="상품 이미지").get('src')

                if uploadtime_att == '광고' :
                    uploadtime_att = self.time_marker

                elif '일' in uploadtime_att:
                    day = re.match('\d+', uploadtime_att).group()
                    uploadtime_att = self.time_marker - timedelta(days=int(day))

                elif '시간' in uploadtime_att:
                    hour = re.match('\d+', uploadtime_att).group()
                    uploadtime_att = self.time_marker - timedelta(hours=int(hour))

                elif '주' in uploadtime_att:
                    week = re.match('\d+', uploadtime_att).group()
                    uploadtime_att = self.time_marker - timedelta(weeks=int(week))
                elif '월' in uploadtime_att:
                    month = re.match('\d+', uploadtime_att).group()
                    uploadtime_att = self.time_marker - timedelta(days=int(month)*30)

                else:
                    uploadtime_att = self.time_marker

                print(uploadtime_att)

                title.append(title_att)
                condition.append(condition_att)
                size.append(size_att)
                price.append(price_att)
                seller.append(seller_att)
                uploadtime.append(uploadtime_att)
                uri.append(uri_att)
                img.append(img_att)

                count += 1
                if count == self.quantity:
                    break

        return zip(title, condition, size, price, seller, uploadtime, uri, img)

class Nikemania(Driver):
    target = 'https://cafe.naver.com/sssw'
    dirname = 'nikemania'

    brands = ['jordan', 'nike', 'adidas', 'other']

    def search(self, brand):
        t.sleep(random.randint(2, 4))
        if brand == 'jordan':
            self.driver.find_element_by_css_selector('#menuLink369').click()
        elif brand == 'nike':
            self.driver.find_element_by_css_selector('#menuLink371').click()
        elif brand == 'adidas':
            self.driver.find_element_by_css_selector('#menuLink448').click()
        elif brand == 'other':
            self.driver.find_element_by_css_selector('#menuLink373').click()
        else:
            pass
        t.sleep(random.randint(2, 4))
        # iframe 접속
        self.driver.switch_to.frame('cafe_main')

    def soup_make(self,border):

        for j in range(math.ceil(self.quantity / 20)):
            t.sleep(random.randint(2, 6))
            html = self.driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
            t.sleep(random.randint(2, 6))

            border_list = soup.select('.article-album-sub > li')
            for index, i in enumerate(border_list):

                upload = i.select('dl > .date_num > .date')[0].text.strip()
                if ':' in upload:
                    upload = datetime.now().date().__str__()
                else:
                    upload = upload[:-1]

                border[index + (j * 20)] = {'title': i.select('dl > dt span')[0].text,
                                            'name': i.select('dl > .p-nick .p-nick')[0].text,
                                            'url': r'https://cafe.naver.com' + i.find('a')['href'],
                                            'date': upload}
                if len(border) == self.quantity:
                    break
            try:
                self.driver.find_elements_by_css_selector('.prev-next > a')[j + 1].click()
            except:
                break

        return border

    def parser(self,border):
        # 리스트 번호란기준으로 정규표현식으로 뽑음
        # 4. 판매제품명
        # 5. 사이즈
        # 6. 제품상태
        # 7. 가격
        # 8. 거래방법
        p = re.compile(r'^(\d[.])\s?(.*:)(.*)')

        for border_att in border:

            self.driver.get(border[border_att]['url'])
            t.sleep(random.randint(1, 5))
            self.driver.switch_to.frame('cafe_main')
            t.sleep(random.randint(1, 5))
            html = self.driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
            t.sleep(random.randint(1, 3))
            content_list = soup.select('.se-module p')

            ct_title=''
            ct_size=''
            ct_condition=''
            ct_price=''
            for i in content_list:
                if p.search(i.text):
                    # 4. 판매제품명
                    if '4' in p.search(i.text).group(1):
                        ct_title = p.search(i.text).group(3).strip()
                    # 5. 사이즈
                    elif '5' in p.search(i.text).group(1):
                        ct_size = p.search(i.text).group(3).strip()
                    # 6. 제품상태
                    elif '6' in p.search(i.text).group(1):
                        ct_condition = p.search(i.text).group(3).strip()
                    # 7. 가격
                    elif '7' in p.search(i.text).group(1):
                        ct_price = p.search(i.text).group(3).strip()
                    else:
                        pass
                else:
                    pass

            border[border_att]['content'] = {'title': ct_title, 'size': ct_size, 'condition': ct_condition,
                                             'price': ct_price}

            print(border_att + 1, ' 번 완료')
        return border

    def logics(self, brand, final_dict):
        border = dict()
        self.start()
        self.search(brand)
        border = self.soup_make(border)
        border = self.parser(border)
        self.driver.quit()

        final_dict[brand] = border
