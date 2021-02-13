import requests


class Gourmet:  #グルメサーチAPI

    def set(self, lat, lng, ran):
        self.lat = lat
        self.lng = lng
        self.ran = ran
        self.req_data = self.get()

    def get(self) -> object:
        url = 'https://webservice.recruit.co.jp/hotpepper/gourmet/v1/?key=77c25fbd1899d0c3'
        url = url + '&format=json&count=100'  # json形式でデータ取得、最大100件表示
        url = url + '&lat=' + self.lat + '&lng=' + self.lng + '&range=' + self.ran  # 範囲設定（lat:緯度、lng:経度）
        return requests.get(url).json()

    def cnt_data(self):
        try:
            return self.req_data['results']['results_available']
        except:
            print('cnt_data error')
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
                    else:
                        shop_x[data_name] = shop_data[data_name]
                data.append(shop_x)
        except:
            print('cnt error')
        return data



    def get_data_test(self, data_names):

        data = []
        for shop in self.req_data['results']['shop']:
            shop_data = {}
            for data_name in data_names:
                if data_name is 'photo':
                    shop_data[data_name] = shop['photo']['pc']['l']
                else:
                    shop_data[data_name] = shop[data_name]
            data.append(shop_data)
        return data


if __name__ == '__main__':
    print('getdata')