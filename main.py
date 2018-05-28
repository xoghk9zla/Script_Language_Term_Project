from tkinter import *
from tkinter import font

import http.client
import urllib.request
from xml.dom.minidom import parse, parseString


def Init():
    # 제목
    title = Label(MainWindow, text="공유저작물 검색 프로그램", font='helvetica 16')
    title.pack()
    title.place(x=120, y=0)

    # 검색 박스
    serchbox = Entry(MainWindow)
    serchbox.pack()
    serchbox.place(x=10, y=60)

    # 검색 버튼
    serchbutton = Button(MainWindow, text="검색", command=SearchButtonAction)
    serchbutton.pack()
    serchbutton.place(x=150, y=60)

    # 전체 출력 버튼
    printbutton = Button(MainWindow, text="모두 출력", command=PrintButtonAction)
    printbutton.pack()
    printbutton.place(x=200, y=60)

    # 리스트 박스
    listbox = Listbox(MainWindow, height=23, width=30)
    listbox.pack()
    listbox.place(x=10, y=110)

    # 회사목록 전체 출력(이걸 위에 리스트 박스로 바꿔야함)
    global RenderText
    RenderTextScrollbar = Scrollbar(MainWindow)
    RenderTextScrollbar.pack()
    RenderTextScrollbar.place(x=375, y=200)

    TempFont = font.Font(MainWindow, size=10, family='Consolas')
    RenderText = Text(MainWindow, width=45, height=23, borderwidth=12, yscrollcommand=RenderTextScrollbar.set)
    RenderText.pack()
    RenderText.place(x=10, y=110)
    RenderTextScrollbar.config(command=RenderText.yview)
    RenderTextScrollbar.pack(side=RIGHT, fill=BOTH)

    RenderText.configure(state='disabled')

    # 사진 캔버스
    photo = PhotoImage(file="몽타뉴3.gif")

    canvas = Label(MainWindow, height=220, width=235, image=photo, bg='gray91', relief="ridge")
    canvas.pack()
    canvas.place(x=240, y=110)

    # 정보 박스
    infobox = Text(MainWindow, width=34, height=7)
    infobox.pack()
    infobox.place(x=240, y=350)

    # 이메일 전송 버튼
    emailbutton = Button(MainWindow, text="이메일로 전송")
    emailbutton.pack()
    emailbutton.place(x=240, y=450)

def SearchButtonAction():
    pass

def PrintButtonAction():
    cnt = 0
    RenderText.configure(state='normal')
    RenderText.delete(0.0, END)

    companyList = DocData.childNodes
    companyname = companyList[0].childNodes
    for item in companyname:
        if item.nodeName == "row":
            subitem = item.childNodes
            for atom in subitem:
                if atom.nodeName in "BIZPLC_NM":
                    cnt = cnt + 1
                    RenderText.insert(INSERT, "[{0}]회사명: {1} \n".format(cnt, atom.firstChild.nodeValue))

    RenderText.configure(state='disabled')
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

def SearchCompany():
    companyList = DocData.childNodes
    companyname = companyList[0].childNodes
    for item in companyname:
        if item.nodeName == "row":
            subitem = item.childNodes
            for atom in subitem:
                if atom.nodeName in "BIZPLC_NM":
                    print("회사이름:", atom.firstChild.nodeValue)

MainWindow = Tk()
MainWindow.title("공유저작물 검색 프로그램")
MainWindow.geometry("500x500")


MakeXML()   # openApi를 xml 파일로 저장

DocData = None  # xml 데이터를 저장 할 공간
DocData = LoadXMLFile()     # xml 로드

Init()

MainWindow.mainloop()