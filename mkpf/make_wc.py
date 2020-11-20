import json
import re
from datetime import datetime
from konlpy.tag import *
import matplotlib.pyplot as plt
from matplotlib import font_manager , rc
from wordcloud import WordCloud,STOPWORDS
from collections import Counter
from PIL import Image
import numpy as np
from wordcloud import ImageColorGenerator
import os
import random

class MakeWc:
    today = datetime.now().strftime('%Y-%m-%d')

    def __init__(self):
        with open(f'static/crawling_data/img/nikemania/{self.today}nikemania.json','rt',encoding='utf-8-sig') as f_json:

            data = json.load(f_json)
        # 1.json 파일을 [브랜드] : [lists] 형태로 만들어준다.
        self.words = {}
        for brand in data:
            word = []
            for index, number in enumerate(data[brand]):
                word.append(data[brand][number]['title'])
            self.words[brand] = word


    def extraction(self):
        # 2. konlpy 중 komoran을사용, 사용자사전을 추가하여 명사추출
        komoran = Komoran(userdic='./static/wordcloud/config/user_dic.txt')

        extraction_word = dict()

        # 3. 추출된 단어들을 이름별로 변수생성한다.
        for brand in self.words:
            word_pool = []
            for index, content in enumerate(self.words[brand]):
                word_pool += komoran.nouns(content)

            extraction_word[brand] = word_pool

        return extraction_word

        ## return nike_word,adidas_word,jordan_word,other_word

    def count(self, **kwargs):

        for brand, content in kwargs.items():
            words_count = Counter(content)
            kwargs[brand] = dict(words_count.most_common())

        return kwargs

    def imgshow(self):
        # 이미지 마스크로 쓸 이미지를 불러온다.
        brand = ['nike', 'jordan', 'adidas', 'other']
        img_attr = dict()

        for i in brand:
            path = f'./static/wordcloud/brand/{i}/'
            imglist = os.listdir(path=path)

            choesimg = random.choice(imglist)

            wc_img = np.array(Image.open(path + choesimg))

            # 워드클라우드의 색상을 불러온 이미지에서 추출한다.
            wc_color = ImageColorGenerator(wc_img)

            img_attr[i] = {'wc_img': wc_img, 'wc_color': wc_color}

        return img_attr

    def drawWC(self, img_attr: dict, **words_list):
        # relative_sacling : 단어간 비율

        #             print(type(words[brand]['wc_img']))
        for index, brand in enumerate(words_list.keys()):
            wc = WordCloud(font_path='./static/wordcloud/config/야놀자 야체 Regular.ttf',
                           relative_scaling=0.2,
                           mask=img_attr[brand]['wc_img'],
                           background_color='white', min_font_size=10,
                           max_font_size=150,
                           max_words=1000,
                           width=1920,
                           height=1080
                           ).generate_from_frequencies(words_list[brand])

            recolor_wc = wc.recolor(color_func=img_attr[brand]['wc_color'], random_state=42)

            fig = plt.figure(figsize=(16, 9))
            plt.imshow(wc, interpolation='bilinear')
            plt.axis('off')
            fig.savefig(f'./static/wordcloud/wc/{self.today}{brand}.png')



if __name__ =='__main__':
    makewc = MakeWc()
    extraction_word = makewc.extraction()
    word_count = makewc.count(**extraction_word)
    img_attr= makewc.imgshow()
    makewc.drawWC(img_attr,**word_count)


