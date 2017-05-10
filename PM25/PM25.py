import requests, time
from bs4 import BeautifulSoup
import matplotlib
matplotlib.use('Agg') # server的backend display參數設定
import matplotlib.pyplot as plt


class PM25(object):
    def __init__(self, url):
        self.url = url
        self.infoDict = dict()
        self.dateList = list()

    def query(self, firstTime):
        res = requests.get(self.url)
        soup = BeautifulSoup(res.text, 'html.parser')
        if len(self.dateList) == 24:
            del self.dateList[0]
        self.dateList.append(soup.select('#ctl14_labText1')[0].text.split('：')[1]) # 抓到 '2017/03/30 15:00'

        for item in soup.select('table.TABLE_G tr[align="center"]'):
            siteStr = (item.select('td:nth-of-type(1)')[0].text).replace('\n', '')
            data = (item.select('td:nth-of-type(2)')[0].text).replace('\n', '')
            if firstTime: # 第一次爬的話對dictionary作初始化
                self.infoDict[siteStr] = list()
                if data == 'ND' or data == '': data = 30
                self.infoDict[siteStr].append(int(data))
            else:
                if len(self.infoDict[siteStr]) == 24:
                    del self.infoDict[siteStr][0]
                if data == 'ND' or data == '':
                    self.infoDict[siteStr].append(self.infoDict[siteStr][-1]) # 如果該時間沒有數據，就append上一次的數據
                else:    
                    self.infoDict[siteStr].append(int(data))

        for key, value in self.infoDict.items():
            print(key + ' ' + str(value))

    def draw(self):
        temp = [x for x in range(0, len(self.dateList))]
        
        fig = plt.figure(figsize=(25, 15), dpi=150)
        plt.xlabel('時間')
        h = plt.ylabel('微克 / 立方公尺')
        plt.title('PM2.5')
        plt.xticks(temp, self.dateList, rotation=45) # dateTemp: 0-23  date: 要更新的時間list
        colorList = ['#000000', '#8C0044', '#880000', '#A42D00', '#BB5500', '#FF00FF', '#444444', '#886600', '#FFCC22', '#0066FF', '#227700', '#5599FF', '#008844', '#00FFFF', '#FF8800', '#007799', '#003377', '#FFC8B4', '#0000FF', '#E63F00', '#550088', '#660077', '#770077', '#990099', '#FF0000']        
        colorIndex = 0
        for key, value in self.infoDict.items():
            plt.plot(temp, self.infoDict[key], label=key, linestyle='-', marker='o', color=colorList[colorIndex])
            colorIndex += 1
        plt.legend(loc='best')
        plt.savefig('./result.png', dpi=150, format='png')

    def exec(self):
        firstTime = True
        count = 0
        while True:
            self.query(firstTime)
            self.draw()
            firstTime = False
            print('已執行' + str(count+1) +'次')
            count += 1
            time.sleep(2)

    # For testing
    def main(self):
        self.query(True)
        self.draw()


if __name__ == '__main__':
    obj = PM25('http://taqm.epa.gov.tw/pm25/tw/PM25A.aspx?area=1')
    obj.exec()
    # obj.main()

