
# encoding=utf8
from tkinter import *
from tkinter import font

import urllib.request
from xml.dom.minidom import parse, parseString

import smtplib

temp = "smtp.gmail.com"

s=smtplib.SMTP(temp,587)
s.ehlo()
s.starttls()
s.ehlo()
s.login("xoghk9zla@gmail.com", "d7297mc!")


def test():
    print("?")
    pass


def Init():
    # 제목
    title = Label(MainWindow, text="경기도 게임회사를 알아보자", font='helvetica 16')
    title.pack()
    title.place(x=120, y=0)

    # 검색 박스
    global searchbox
    searchbox = Entry(MainWindow)
    searchbox.pack()
    searchbox.place(x=10, y=60)

    # 검색 버튼
    searchbutton = Button(MainWindow, text="검색", command=SearchButtonAction)
    searchbutton.pack()
    searchbutton.place(x=150, y=60)

    # 전체 출력 버튼
    printbutton = Button(MainWindow, text="모두 출력", command=PrintlistAction)
    printbutton.pack()
    printbutton.place(x=200, y=60)

    # 리스트 박스
    global listbox
    RenderTextScrollbar = Scrollbar(MainWindow)
    listbox = Listbox(MainWindow, height=23, width=30, yscrollcommand=RenderTextScrollbar.set, selectmode=SINGLE)
    listbox.pack()
    listbox.place(x=10, y=110)
    RenderTextScrollbar.config(command=listbox.yview)
    RenderTextScrollbar.pack(side=RIGHT, fill=BOTH)
    listbox.configure(state='disabled')


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
    emailbutton = Button(MainWindow, text="이메일로 전송", command=test)
    emailbutton.pack()
    emailbutton.place(x=240, y=450)

def SearchButtonAction():
    cnt = 0
    listbox.delete(0, END)
    company_name = searchbox.get()
    companyList = DocData.childNodes
    companyname = companyList[0].childNodes
    for item in companyname:
        tempnum = 0
        if item.nodeName == "row":
            subitem = item.childNodes
            for atom in subitem:
                if atom.nodeName in "SIGUN_NM" and atom.firstChild.nodeValue == company_name:
                    cnt += 1
                    temp1 = subitem[5].firstChild.nodeValue
                    listbox.insert(tempnum, "[{0}]회사명: {1} \n".format(cnt, temp1))
                    tempnum += 1
        listbox.configure(state='normal')

    pass


def PrintlistAction():
    cnt = 0
    listbox.delete(0,END)

    companyList = DocData.childNodes
    companyname = companyList[0].childNodes
    for item in companyname:
        tempnum=0
        if item.nodeName == "row":
            subitem = item.childNodes
            for atom in subitem:
                if atom.nodeName in "BIZPLC_NM":
                    cnt = cnt + 1
                    listbox.insert(tempnum, "[{0}]회사명: {1} \n".format(cnt, atom.firstChild.nodeValue))
                    tempnum+=1

        listbox.configure(state='normal')
    pass

def EmailButtonAction():
    test()
    pass

def MakeXML(): # xml 파일 만들기
    url = "https://openapi.gg.go.kr/GameSoftwaresDistribution?KEY=716a00130e0e49a196f9433942b4c728&pIndex=1&pSize=677"
    data = urllib.request.urlopen(url).read()
    f = open("company.xml", "wb")
    f.write(data)
    f.close()
    pass

def LoadXMLFile():  # xml 파일 불러오기
    fileName = 'company.xml'    # xml 파일 이름
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
MainWindow.title("취업하고 싶어요")
MainWindow.geometry("505x500")

MakeXML()   # openApi를 xml 파일로 저장

DocData = None  # xml 데이터를 저장 할 공간
DocData = LoadXMLFile()     # xml 로드

Init()

MainWindow.mainloop()
