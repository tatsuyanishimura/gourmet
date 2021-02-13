from flask import Flask, render_template, request
from getdata import Gourmet
import math
app = Flask(__name__)

case = 0            #ヒット件数
shops = []          #店舗情報
limit = 5          #ページごとの表示件数
page = 0            #現在のページ-1
page_count = 0      #全ページ数
head = 0            #先頭の件数
gou = Gourmet()     #グルメAPI
location = {}       #緯度,経度,範囲を保存


@app.route('/')
def first():
    if request.args.get('lat') is None:
        return render_template('location.html')
    global location, case, page_count, shops
    location = dict(request.args)
    gou.set(**location)
    case = gou.cnt_data()
    page_count = math.ceil(case/limit)
    shops = gou.shop_data()
    shops_data = shops_data_maker()
    page_data = pager()
    return render_template('index.html', range=location['ran'], count=case, shops=shops_data, page=page_data)


@app.route('/index', methods=['GET','POST'])
def index():
    if request.method == 'POST':
        global location, case, shops
        location = dict(request.form)
        gou.set(**location)
        case = gou.cnt_data()
        shops = gou.shop_data()
        case = gou.cnt_data()
    if request.args.get('page'):
        global page, head
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
    return render_template('index.html', range=location['ran'], count=case, shops=shops_data, page=page_data)


@app.route('/shop')
def det_act():
    i = int(request.args.get('number'))
    shop = shops[i + head]
    return render_template('shop.html', shop=shop)


def shops_data_maker():
    shops_data = []
    if limit < case-head:
        n = limit
    else:
        n = case - head
    for i in range(n):
        shop = shops[i]
        shops_data.append(shop[i])
    return shops_data


def pager():
    data = {}
    page_count = math.ceil(case/limit)
    data['prev'] = '?page=' + str(page-1)
    if page <= 0:
        data['prev'] = '#'
    if page_count == 0:
        data['index'] = '0/0'
    else:
        data['index'] = '{0}/{1}'.format(page+1, page_count)
    data['next'] = '?page=' + str(page + 1)
    if page >= page_count-1:
        data['next'] = '#'
    return data


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')