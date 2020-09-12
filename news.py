## 해외뉴스 크롤링 및 번역

import sys
from PyQt5.QtWidgets import *
from googletrans import Translator
import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import FinanceDataReader as fdr
import pandas as pd



class MyApp(QWidget):

    def __init__(self):
        super().__init__()

        self.lbl2 = QLabel('일본 야후:', self)
        self.te = QTextEdit(self)
        self.trans_btn = QPushButton('일본 주요 뉴스', self)
        self.translator = Translator()

        self.fig = plt.Figure()
        self.canvas = FigureCanvas(self.fig)
        self.chart_btn = QPushButton('그래프 그리기', self)

        self.initUI()


    def initUI(self):


        vbox = QVBoxLayout()
        vbox.addWidget(self.lbl2)
        vbox.addWidget(self.te)
        vbox.addStretch(self.canvas)

        vbox.addWidget(self.trans_btn)
        vbox.addWidget(self.chart_btn)
        self.setLayout(vbox)

        self.trans_btn.clicked.connect(self.crwal_jpn)
        self.chart_btn.clicked.connect(self.bond)

        self.setWindowTitle('NEWS Translator')
        self.setGeometry(100, 100, 1000, 700)
        self.show()

    def crwal_jpn(self): # 일본 야후에서 주요뉴스 크롤링
        url = 'https://news.yahoo.co.jp/topics'

        r = requests.get(url)
        html = r.content
        soup = BeautifulSoup(html, 'html.parser')
        titles_html = soup.select('.topicsList > ul > li > a ')

        for i in range(24): # 전체 출력 : len(titles_html)
            title = titles_html[i].text
            link = titles_html[i].get('href')
            transtitle = str(self.translator.translate(title, dest="ko").text)
            self.te.append(str(i + 1) + '. ' + transtitle + ' (' + '<a href="' + link + '">Link</a>' + ')')

    def bond(self):
        df_J = fdr.DataReader('JP225', '2020-01-01')
        ax = self.fig.add_subplot(111)
        ax.plot(df_J['Close'], label='Japen')
        self.canvas.draw()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())