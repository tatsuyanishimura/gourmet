import requests
from jpholiday import is_holiday
from datetime import datetime, timedelta


class Gourmet:  # グルメサーチAPI

    def __init__(self):
        self.lat = ''
        self.lng = ''
        self.ran = ''
        self.days = ['月', '火', '水', '木', '金', '土', '日']
        self.days2 = {'月': 0, '火': 1, '水': 2, '木': 3, '金': 4, '土': 5, '日': 6}
        self.req_data = {}
        self.date = ''
        self.day = ''

    def set(self, lat: str, lng: str, ran: str):
        self.set_pos(lat, lng)
        self.set_ran(ran)
        self.set_data()

    def set_pos(self, lat: str, lng: str):  #位置の設定（lat:緯度,lng:経度）
        self.lat = lat
        self.lng = lng

    def set_ran(self, ran: str):    #範囲の設定
        self.ran = ran

    def set_pos2(self, lat: str, lng: str): #テスト用位置
        self.lat = '36.3763497'
        self.lng = '139.0246238'

    def set_data(self):
        url = 'https://webservice.recruit.co.jp/hotpepper/gourmet/v1/?key=77c25fbd1899d0c3'
        url = url + '&format=json&count=100&oder=4'  # json形式でデータ取得、最大100件表示 距離の近い順で表示
        url = url + '&lat=' + self.lat + '&lng=' + self.lng + '&range=' + self.ran  # 範囲設定（lat:緯度、lng:経度、ran:範囲）
        self.req_data = requests.get(url).json()

    def cnt_data(self) -> int:
        return int(self.req_data['results']['results_available'])

    def shop_data(self) -> list:  # 店舗情報を渡す関数
        self.date = datetime.now().date()
        self.day = datetime.weekday(self.date)
        data = []
        data_names = ['name', 'address', 'mobile_access', 'access', 'close', 'catch', 'free_drink', 'free_food', 'card']
        for shop_data in self.req_data['results']['shop']:
            shop_x = {}
            shop_x['photo'] = shop_data['photo']['pc']['l']
            shop_x['budget'] = shop_data['budget']['name']
            shop_x['genre'] = shop_data['genre']['name']
            shop_x['urls'] = shop_data['urls']['pc']
            shop_x['coupon_urls'] = shop_data['coupon_urls']['pc']
            shop_x['open'] = self.open_maker(shop_data['open'])
            shop_x['run'] = self.run_maker(shop_data['open'], shop_data['close'])
            for data_name in data_names:
                shop_x[data_name] = shop_data[data_name]
            data.append(shop_x)
        return data

    def open_maker(self, open_data: str) -> str:  # 営業時間の表示調整関数
        open_d, o_b = '', ''
        i = 0
        for o_a in open_data:
            if o_a.isdecimal():
                i = i + 1
            else:
                i = 0
            if self.open_check(o_a, o_b, i):
                open_d = open_d + '<br>'
            o_b = o_a
            open_d = open_d + o_a
        return open_d

    def open_check(self, o_a: str, o_b: str, i: int) -> bool:  # 改行位置の決定
        if o_b.isdecimal() and o_a in self.days or o_a == '（' or o_b == '）' or i == 3:
            return True
        else:
            return False

    def run_maker(self, open_data: str, close_data: str) -> str:  # 営業しているなら真、営業していないなら偽を返す関数
        for c_a in close_data:  # 定休日判定
            if c_a == self.days[datetime.weekday(self.date)]:
                return '(定休日)'
        open_data_d = self.del_bra_maker(open_data)
        if is_holiday(datetime.now().date()):  # 祝日判定
            a = open_data_d.find('祝日')
            if a != -1:
                return self.overtime_maker(self.run_check(open_data_d, a))
        if is_holiday(datetime.now().date() + timedelta(1)):  # 祝前日判定
            a = open_data_d.find('祝前')
            if a != -1:
                return self.overtime_maker(self.run_check(open_data_d, a))
        return self.overtime_maker(self.day_check(open_data_d))  # 曜日判定

    def day_check(self, open_data: str) -> bool:  # 曜日ごとの営業時間判定関数
        day = datetime.weekday(self.date)
        if self.days[day] == '日':  # 日曜だけの特殊処理
            a = self.sunday_check(open_data)
        else:  # その他
            a = open_data.find(self.days[day])

        if a != -1:
            if self.run_check(open_data, a):
                return True
        run_d, o_b, o_c = '', '', ''
        for o_a in open_data:  # 〇～〇曜日の判定
            if o_a in self.days and o_b == '～' and o_c in self.days:
                a = self.days2[o_a]
                c = self.days2[o_c]
                d = day
                if c > a:
                    a = a + 7
                if c > d:
                    d = d + 7
                if c < d < a:
                    if o_a == '日':
                        a = open_data.find(o_c)
                    else:
                        a = open_data.find(o_a)
                    if self.run_check(open_data, a):
                        return True
            o_c = o_b
            o_b = o_a

        return False

    def sunday_check(self, open_data) -> bool:  # 日曜日の特殊処理関数
        a = 0
        if open_data.find('日') == open_data.find('祝日') + 1:
            a = open_data.find('日') + 1
        if open_data.find('日', a) == open_data.find('前日') + 1:
            a = open_data.find('日', a) + 1
        return open_data.find('日', a)

    def run_check(self, open_data: str, a: int) -> bool:  # 営業時間か判定する関数
        da = datetime
        open_d: str = open_data[a:]
        times = self.time_data(open_d)
        hour = da.now().hour
        minute = da.now().minute
        for time in times:
            time0 = int(time[0])
            time1 = int(time[1])
            time3 = int(time[3])
            if time[2].find('翌') == -1:
                time2 = int(time[2])
            else:
                time2 = int(time[2][1]) + 24
            if time0 > hour:
                hour = hour + 24
            if time0 < hour < time2:
                return True
            elif time0 == hour:
                if time1 < minute:
                    return True
            elif time2 == hour:
                if minute < time3:  # run_check　4を3に修正
                    return True
        return False

    def overtime_maker(self, check: bool) -> str:  # 営業時間外を返す関数
        if check:
            return '(営業中)'
        else:
            return '(営業時間外)'

    def del_bra_maker(self, text: str) -> str:  # textの括弧を消去して返す
        i = 0
        st = text
        while '（' in st:
            a = st.find('（')
            b = st.find('）')
            st = st[:a - 1] + st[b + 1:]
            i = i + 1
            if i == 10:
                break
        return st

    def time_data(self, text) -> list:  # 営業時間データの整頓　ー＞[開店（時）, 開店（分）,　閉店（時）, 閉店（分） ]
        datas = []
        st = text[text.find(':') + 2:]
        if st.find(': ') != -1:
            st = st[:st.find(': ')]
        a = 0
        while st[a].isdecimal():
            data = []
            for i in range(4):
                data.append(st[a + 3 * i:a + 2 + 3 * i])
            datas.append(data)
            a = a + 11
            if len(st) < a + 1:
                break
        return datas
