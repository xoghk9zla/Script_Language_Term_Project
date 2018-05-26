from tkinter import *
from tkinter import font

import http.client
import urllib.request
from xml.dom.minidom import parse, parseString


def Init():
    # 프로그램 상단에 [공유(만료) 저작물 검색] 텍스트 띄우기
    Font = font.Font(MainWindow, size=20, weight='bold', family='Consolas')
    MainText = Label(MainWindow, font=Font, text="[공유(만료) 저작물 검색]")
    MainText.pack()
    MainText.place(x=20)
    # 검색 창 만들기
    global InputLabel
    Font = font.Font(MainWindow, size=15, weight='bold', family='Consolas')
    InputLabel = Entry(MainWindow, font=Font, width=26, borderwidth=12, relief='ridge')
    InputLabel.pack()
    InputLabel.place(x=10, y=105)
    # 검색 버튼 만들기
    Font = font.Font(MainWindow, size=12, weight='bold', family='Consolas')
    SearchButton = Button(MainWindow, font=Font, text="검색", command=SearchButtonAction)
    SearchButton.pack()
    SearchButton.place(x=330, y=110)

def SearchButtonAction():
    pass

def Test():
    url = "https://openapi.gg.go.kr/GameSoftwaresDistribution?KEY=716a00130e0e49a196f9433942b4c728&pIndex=1&pSize=50"
    data = urllib.request.urlopen(url).read()
    f = open("sample1.xml","wb")
    f.write(data)
    f.close()
    pass

MainWindow = Tk()
MainWindow.geometry("400x600+750+200")
Data = []

Init()

Test()

MainWindow.mainloop()

