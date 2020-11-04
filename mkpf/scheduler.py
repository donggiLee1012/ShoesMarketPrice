import sqlite3
from multiprocessing import Pool,Process,Queue,Manager

import json
import os
import re
import time as t
import sys

if __name__ =='__main__':

    if __package__ is None:
        sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        from initclass import Nikemania
    else:
        from .initclass import Nikemania
        pass

    mangers = Manager()
    final_dict = mangers.dict()

    proces = []
    #('','',quantity = 크롤링갯수 나중에 저장소에서 설정값 가져오도록 변경)
    namaes = Nikemania('','',30)

    for i in Nikemania.brands:
        proc = Process(target=namaes.logics, args=(i,final_dict))
        proces.append(proc)
        proc.start()

    for proc in proces:
        proc.join()

    save = os.path.dirname(os.path.dirname(namaes.imgpath))
    jsonfile = os.path.join(save,'nikemania')

    with open(f"{jsonfile}.json", "w", encoding='utf-8') as json_file:
        json.dump(final_dict.copy(), json_file, ensure_ascii=False)
