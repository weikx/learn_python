"""
    熊猫TV LOL 类目下主播人气排行
"""
import re
import ssl
from urllib import request

ssl._create_default_https_context = ssl._create_unverified_context

class Spider:
    url = 'https://www.panda.tv/cate/lol'
    root_pattern = '<div class="video-info">([\s\S]*?)</div>'
    name_pattern = '</i>([\s\S]*?)</span>'
    num_pattern = '<span class="video-number">([\s\S]*?)</span>'

    def __fatch_content(self):
        res = request.urlopen(self.url)
        htmls = str(res.read(), encoding='utf-8')
        return htmls

    def __filter(self, arr):
        arr = map(lambda item: {
            'name': item['name'][0].strip(),
            'number': item['number'][0]
        }, arr)
        return arr

    def __sort(self, arr):
        return sorted(arr, key=self.__sort_seed, reverse=True)

    def __sort_seed(self, arr):
        r = re.findall('\d*', arr['number'])[0]
        number = float(r)
        if '万' in arr['number']:
            number *= 1000
        return number

    def __show(self, arr):
        for i in range(0, len(arr)):
            print('rank ' + str(i + 1) + '   ' + arr[i]['name'] + '   ' + arr[i]['number'])

    def __analysis(self, htmls):
        arr = []
        htmls = re.findall(self.root_pattern, htmls)
        for list in htmls:
            name = re.findall(self.name_pattern, list)
            number = re.findall(self.num_pattern, list)
            arr.append({
                'name': name,
                'number': number
            })
        return arr

    def go(self):
        htmls = self.__fatch_content()
        anchors = self.__analysis(htmls)
        anchors = self.__filter(anchors)
        anchors = self.__sort(anchors)
        anchors = self.__show(anchors)

spider = Spider()
spider.go()