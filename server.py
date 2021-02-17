from flask import Flask, render_template, request, Markup
from getdata import Gourmet
import math
import webbrowser

app = Flask(__name__)

case = 0            #ヒット件数
shops = []          #店舗情報
limit = 10          #ページごとの表示件数
page = 0            #現在のページ-1
page_count = 0      #全ページ数
head = 0            #先頭の件数
gou = Gourmet()     #グルメAPI
loc = {}       #緯度,経度,範囲を保存

#初期動作
@app.route('/')
def first():
    if 'lat' not in request.args:
        return render_template('location.html') #GeolocationAPI
    global loc, case, page_count, shops
    loc = dict(request.args)
    gou.set(**loc)                 #検索条件の設定
    case = gou.cnt_data()               #検索件数の取り出し
    page_count = math.ceil(case/limit)  #ページ数
    shops = gou.shop_data()             #店舗情報
    shops_data = shops_data_maker()     #１ページ分のデータ
    page_data = pager()
    return render_template('index.html', range=loc['ran'], count=case, shops=shops_data, page=page_data)

#検索画面
@app.route('/index', methods=['GET', 'POST'])
def index():
    global loc, case, shops, page, head
    if request.method == 'POST':
        loc = dict(request.form)
        gou.set_ran(loc['ran'])
        gou.set_data()
        case = gou.cnt_data()
        shops = gou.shop_data()
        case = gou.cnt_data()
        page = 0
        head = page * limit
    if request.args.get('page'):
        page = int(request.args.get('page'))
        head = page * limit
    page_data = pager()
    if limit < case-head:
        n = limit
    else:
        n = case-head
    shops_data = []
    for i in range(n):
        shop = gou.shop_data()
        shops_data.append(shop[i+head])
    return render_template('index.html', range=loc['ran'], count=case, shops=shops_data, page=page_data)

#詳細画面
@app.route('/shop')
def det_act():
    i = int(request.args.get('number'))
    shop = shops[i + head]
    return render_template('shop.html', shop=shop)


def shops_data_maker(): #店舗情報をページング対応させる
    shops_data = []
    if limit < case-head:
        n = limit
    else:
        n = case - head
    for i in range(n):
        shop = shops[i]
        shops_data.append(shop)
    return shops_data


def pager():    #ページリンクの表示とリンク先を作る関数
    data = {}
    page_count = math.ceil(case/limit)
    data['prev'] = './index?page=' + str(page-1)
    if page <= 0:
        data['prev'] = './index#'
    if page_count == 0:
        data['index'] = '0/0'
    else:
        data['index'] = '{0}/{1}'.format(page+1, page_count)
    data['next'] = './index?page=' + str(page + 1)
    if page >= page_count-1:
        data['next'] = './index#'
    return data


if __name__ == '__main__':
    webbrowser.open('http://localhost:8000/')
    app.run(host='0.0.0.0', port=8000)