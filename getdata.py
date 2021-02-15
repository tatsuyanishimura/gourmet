import requests
from jpholiday import is_holiday
from datetime import datetime,timedelta

class Gourmet:  #グルメサーチAPI
    def __init__(self):
        self.days = ['月', '火', '水', '木', '金', '土', '日']
        self.days2 = {'月':0,'火':1, '水':2, '木':3, '金':4, '土':5, '日':6}
        self.num = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
        self.req_data = {}

    def set(self, lat, lng, ran):
        self.req_data = self.get(lat,lng,ran)

    def get(self,lat,lng,ran) -> object:
        url = 'https://webservice.recruit.co.jp/hotpepper/gourmet/v1/?key=77c25fbd1899d0c3'
        url = url + '&format=json&count=100'  # json形式でデータ取得、最大100件表示
        url = url + '&lat=' + lat + '&lng=' + lng + '&range=' + ran  # 範囲設定（lat:緯度、lng:経度、ran:範囲）
        return requests.get(url).json()

    def cnt_data(self):
        try:
            return int(self.req_data['results']['results_available'])
        except:
            print('cnt_data error')

            return 0

    def shop_data(self):    #店舗情報を渡す
        data = []
        data_names = ['name', 'address', 'access', 'close']
        for shop_data in self.req_data['results']['shop']:
            shop_x = {}
            shop_x['photos'] = shop_data['photo']['pc']['s']
            shop_x['photol'] = shop_data['photo']['pc']['l']
            shop_x['budget'] = shop_data['budget']['name']
            shop_x['open'] = self.open_maker(shop_data['open'])
            shop_x['run'] = self.run_maker(shop_data['open'], shop_data['close'])
            for data_name in data_names:
                shop_x[data_name] = shop_data[data_name]
            print(shop_x)
            data.append(shop_x)
        return data

    def open_maker(self,open_data):     #営業時間の表示調整関数
        open_d, o_b = '', ''
        for o_a in open_data:
            if self.open_check(o_a, o_b):
                open_d = open_d + '<br>'
            o_b = o_a
            open_d = open_d + o_a
        return open_d

    def open_check(self, o_a, o_b):
        if o_b in self.num and o_a in self.days or o_a == '（':
            return True
        else:
            return False

    def run_maker(self, open_data, close_data):     #営業しているかを判定する関数
        da = datetime
        for c_a in close_data:     #定休日判定
            if c_a == self.days[da.weekday(da.now().date())]:
                return '営業時間外'

        if is_holiday(da.now().date()):     #祝日判定
            a = open_data.find('祝日')
            if a != -1:
                return self.run_nrun(self.holy_check(open_data, a))

        if is_holiday(da.now().date() + timedelta(1)):     #祝前日判定
            a = open_data.find('祝前')
            if a != -1:
                return  self.run_nrun(self.holy_check(open_data, a))

        return self.run_nrun(self.day_check(open_data))     #曜日判定

    def holy_check(self, open_data,para):
        return False

    def day_check(self, open_data):
        da = datetime
        day = da.weekday(da.now().date())
        if self.days[day] == '日':   #日曜だけの特殊処理
            a = self.sunday(open_data)
        else:   #その他
            a = open_data.find(self.days[day])
        if a != -1:
            if self.run_check(open_data, a):
                return True
        run_d, o_b, o_c = '', '', ''
        for o_a in open_data:
            if o_a in self.days:
                return True
            elif o_a in self.days and o_b == '～' and o_c in self.days:
                a = self.days2[o_a]
                c = self.days2[o_c]
                if a > c:
                    c = c + 7
                    d = d + 7
                if a < da.weekday(day) < c:
                    a = open_data.find(o_c)
                    if self.run_check(open_data, a):
                        return True
            o_b = o_a
            o_c = o_b

    def sunday(self, open_data):
        a = 0
        if open_data.find('日') == open_data.find('祝日')+1:
            a = open_data.find('日') + 1
        if open_data.find('日', a) == open_data.find('前日')+1:
            a = open_data.find('日', a) + 1
        return open_data.find('日', a)

    def run_check(self,open_data,a):    #営業時間か判定する関数
        da = datetime
        open_d = open_data[a:]
        hour_a, hour_b, minu_a, minu_b = '', '', '', ''
        i, tra, trb = 0, 0, 0
        for o_d in open_d:
            if o_d == ':':
                tra = 1
            if o_d == '翌' and i == 4:
                trb = 1
            if o_d in self.num:
                if tra == 1:
                    i = i + 1
                if i < 1:
                    hour_a = hour_a + o_d
                elif i < 4:
                    minu_a = minu_a + o_d
                elif i < 6:
                    hour_b = hour_b + o_d
                elif i < 8:
                    minu_b = minu_b + o_d
                else:
                    break
                i = i + 1
            tra = 0
        hb = int(hour_b) + 24*trb
        if int(hour_a) < da.now().hour < hb:
            return True
        elif hour_a == da.now().hour:
            if int(minu_a) < da.now().minute:
                return True
        elif hour_b == da.now().hour:
            if da.now().minute < int(minu_b) :
                return True
        return False

    def run_nrun(self,check):
        if check:
            return '営業中'
        else:
            return '営業時間外'
