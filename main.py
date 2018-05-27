from tkinter import *
from tkinter import font

import http.client
import urllib.request
from xml.dom.minidom import parse, parseString


def Init():
    title = Label(MainWindow, text="공유저작물 검색 프로그램", font='helvetica 16')
    title.pack()
    title.place(x=120, y=0)

    serchbox = Entry(MainWindow)
    serchbox.pack()
    serchbox.place(x=10, y=60)

    serchbutton = Button(MainWindow, text="검색")
    serchbutton.pack()
    serchbutton.place(x=150, y=60)

    listbox = Listbox(MainWindow, height=23, width=30)
    listbox.pack()
    listbox.place(x=10, y=110)

    photo = PhotoImage(file="몽타뉴3.gif")

    canvas = Label(MainWindow, height=220, width=235, image=photo, bg='gray91', relief="ridge")
    canvas.pack()
    canvas.place(x=240, y=110)

    infobox = Text(MainWindow, width=34, height=7)
    infobox.pack()
    infobox.place(x=240, y=350)

    emailbutton = Button(MainWindow, text="이메일로 전송")
    emailbutton.pack()
    emailbutton.place(x=240, y=450)

def SearchButtonAction():
    pass

def MakeXML(): # xml 파일 만들기
    url = "https://openapi.gg.go.kr/GameSoftwaresDistribution?KEY=716a00130e0e49a196f9433942b4c728&pIndex=1&pSize=50"
    data = urllib.request.urlopen(url).read()
    f = open("sample1.xml", "wb")
    f.write(data)
    f.close()
    pass

def LoadXMLFile():  # xml 파일 불러오기
    fileName = 'sample1.xml'    # xml 파일 이름 나중에 수정 할 것
    global xmlFD

    try:
        xmlFD = open(fileName, encoding='UTF8')  # xml 문서를 open합니다.
    except IOError:
        print("invalid file name or path")
        return None
    else:
        try:
            dom = parse(xmlFD)  # XML 문서를 파싱합니다.
        except Exception:
            print("loading fail!!!")
        else:
            print("XML Document loading complete")
            return dom
    return None

MainWindow = Tk()
MainWindow.title("공유저작물 검색 프로그램")
MainWindow.geometry("500x500")


MakeXML()   # openApi를 xml 파일로 저장

DocData = None  # xml 데이터를 저장 할 공간
DocData = LoadXMLFile() # xml 로드

print(DocData.toxml()) # xml 출력

Init()

MainWindow.mainloop()