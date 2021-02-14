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

    def shop_data(self):

        data = []
        try:
            data_names = ['name', 'address', 'access', 'close']
            for shop_data in self.req_data['results']['shop']:
                shop_x = {}
                shop_x['photos'] = shop_data['photo']['pc']['s']
                shop_x['photol'] = shop_data['photo']['pc']['l']
                shop_x['budget'] = shop_data['budget']['name']
                shop_x['open'] = self.open_maker(shop_data['open'])
                #shop_x['run'] = self.run_maker(shop_data['open'], shop_data['close'])
                for data_name in data_names:
                    shop_x[data_name] = shop_data[data_name]
                print(shop_x)
                data.append(shop_x)
        except:
            print('shop_data error')
            pass
        return data

    def open_maker(self,open_data): #営業時間の表示調整関数
        open_d, o_b = '', ''
        for o_a in open_data:
            if self.open_check(o_a, o_b):
                open_d = open_d + '<br>'
            o_b = o_a
            open_d = open_d + o_a
        return open_d

    def open_check(self, o_a, o_b):
        if o_b in self.num and o_a in self.days:
            return True
        else:
            return False

    def run_maker(self, open_data, close_data): #営業しているかを判定する関数
        da = datetime
        tr_a, tr_b, tr_c = False, False, False
        run = '営業中'
        nrun = '営業時間外'
        hour, minute = '', ''

        for c_a in close_data:     #定休日の判定
            if self.close_chech(c_a):
                return nrun
        if is_holiday(da.now().date() + timedelta(1)):
            if open_data.find('祝前') is not -1:
                if run_check(open_data.find('祝前')):
                    return run
                else:
                    return nrun
        elif is_holiday(da.now().date()):
            if open_data.find('祝日') is not -1:
                if run_check(open_data.find('祝日')):
                    return run
                else:
                    return nrun
        day = da.weekday(da.now().date())
        run_d, o_b, o_c = '', '', ''
        for o_a in open_data:       #営業時間の判定
            if not tr_a:
                tr_a = self.run_check_one(o_a, o_b, o_c)
            elif not tr_b:
                if o_a in self.num:
                    hour = hour + o_a
                elif o_a is ':':
                    tr_b = True
            elif o_a in self.num:
                minute = minute + o_a


                run_d = run_d
            o_c = o_b
            o_b = o_a

        return run_d

    def close_check(self,c_a):
        da = datetime
        if c_a is self.days[da.weekday(da.now())]:
            return True
        return False

    def run_time(self, open_data):
        run_d, o_b, o_c = '', '', ''
        for o_a in open_data:
            if o_a in self.days2 or o_a:
                pass

        if o_a in self.days:
            return True
        elif o_a in self.days and o_b is '~' and o_c in self.days:
            a = self.days2[o_a]
            c = self.days2[o_c]
            d = 0
            if a > c:
                c = c + 7
                d = d + 7
            if a < da.weekday(da.now().date()) < c:
                return True
        elif o_b is '祝':
            today = da.now().date()
            if o_a is '前':
                t = 1
            return jpholiday.is_holiday(today+timedelta(days=t))
        return False






if __name__ == '__main__':
    pass