import requests


class Gourmet:  #グルメサーチAPI
    def __init__(self):
        self.day = ['月', '火', '水', '木', '金', '土', '日']
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
            return 0

    def shop_data(self):
        data_names = ['name', 'address', 'access', 'photos', 'photol', 'budget','open']

        data = []
        try:
            for shop_data in self.req_data['results']['shop']:
                shop_x = {}
                for data_name in data_names:
                    if data_name is 'photos':
                        shop_x['photos'] = shop_data['photo']['pc']['s']
                    elif data_name is 'photol':
                        shop_x['photol'] = shop_data['photo']['pc']['l']
                    elif data_name is 'budget':
                        shop_x['budget'] = shop_data['budget']['name']
                    elif data_name is 'open':
                        str = ''
                        chr2 = ''
                        for chr in shop_data['open']:
                            if self.open_remaker(chr,chr2):
                                str = str + '<br>'
                            chr2 = chr
                            str = str + chr
                        shop_x['open'] = str
                    else:
                        shop_x[data_name] = shop_data[data_name]
                data.append(shop_x)
        except:
            pass
        return data

    def open_remaker(self, chr, chr2):
        if chr2 in self.num and chr in self.day:
            return True
        else:
            return False



if __name__ == '__main__':
    print('getdata')