from tkinter import *
from tkinter import font

import urllib.request
from xml.dom.minidom import parse, parseString

import teller

import smtplib
from email.mime.base import MIMEBase
from email.mime.text import MIMEText

def test():
    pass


def Init():
    # 제목
    title = Label(MainWindow, text="경기도 게임회사를 알아보자", font='helvetica 16')
    title.pack()
    title.place(x=120, y=0)

    # 검색 옵션
    global radVar
    global CompanySearch, AdressSearch
    radVar = IntVar()
    CompanySearch = False
    AdressSearch = True

    radiobuttton1 = Radiobutton(MainWindow, text="회사", variable=radVar, value=1,command=Click_RadioButton)
    radiobuttton2 = Radiobutton(MainWindow, text="지역", variable=radVar, value=2,command=Click_RadioButton)
    radiobuttton1.pack()
    radiobuttton2.pack()
    radiobuttton1.place(x=10, y=40)
    radiobuttton2.place(x=70, y=40)
    radVar.set(2)

    # 검색 박스
    global searchbox
    global strKeyword
    strKeyword = StringVar()
    searchbox = Entry(MainWindow)
    searchbox.pack()
    searchbox.place(x=10, y=60)

    # 검색 버튼
    searchbutton = Button(MainWindow, text="검색", command=SearchButtonAction)
    searchbutton.pack()
    searchbutton.place(x=160, y=57)

    # 전체 출력 버튼
    printbutton = Button(MainWindow, text="모두 출력", command=PrintlistAction)
    printbutton.pack()
    printbutton.place(x=210, y=57)

    # 상세 정보 버튼
    printbutton = Button(MainWindow, text="상세 정보", command=DetailedInfomationAction)
    printbutton.pack()
    printbutton.place(x=290, y=57)

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
    canvas = Label(MainWindow, height=220, width=240, image=photo, bg='gray91', relief="ridge")
    canvas.pack()
    canvas.place(x=240, y=110)

    # 정보 박스
    global infobox
    infobox = Text(MainWindow, width=34, height=7)
    infobox.pack()
    infobox.place(x=240, y=350)

    # 이메일 전송 버튼
    emailbutton = Button(MainWindow, text="이메일로 전송", command=EmailButtonAction)
    emailbutton.pack()
    emailbutton.place(x=240, y=450)


def Click_RadioButton():
    global CompanySearch, AdressSearch
    if radVar.get() == 1:
        CompanySearch = True
        AdressSearch = False
    if radVar.get() == 2:
        CompanySearch = False
        AdressSearch = True


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
                if AdressSearch:
                    if atom.nodeName in "SIGUN_NM" and atom.firstChild.nodeValue == company_name:
                        cnt += 1
                        listbox.insert(tempnum, "{0}".format(subitem[5].firstChild.nodeValue))
                        tempnum += 1
                elif CompanySearch:
                    if atom.nodeName in "BIZPLC_NM" and atom.firstChild.nodeValue == company_name:
                        listbox.insert(tempnum, "{0}".format(subitem[5].firstChild.nodeValue))
                    pass
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
                    listbox.insert(tempnum, "{0}".format(atom.firstChild.nodeValue))
                    tempnum+=1

        listbox.configure(state='normal')
    pass


def DetailedInfomationAction():
    infobox.delete('0.0', END)
    # 선택된 행이 있으면 그걸 키워드로 검색함
    global SelectedItemText
    SelectedItemIndex = listbox.curselection()
    if len(SelectedItemIndex):
        SelectedItemText = listbox.get(SelectedItemIndex[0])

        companyList = DocData.childNodes
        companyname = companyList[0].childNodes
        for item in companyname:
            if item.nodeName == "row":
                subitem = item.childNodes
                for atom in subitem:
                    if atom.nodeName in "BIZPLC_NM" and atom.firstChild.nodeValue == SelectedItemText:
                        if subitem[31].nodeName == "REFINE_LOTNO_ADDR":
                            infobox.insert(INSERT, "회사명: {0}\n".format(subitem[5].firstChild.nodeValue))
                            infobox.insert(INSERT, "주소: {0}\n".format(subitem[31].firstChild.nodeValue))
                        elif subitem[33].nodeName == "REFINE_LOTNO_ADDR":
                            infobox.insert(INSERT, "회사명: {0}\n".format(subitem[5].firstChild.nodeValue))
                            infobox.insert(INSERT, "주소: {0}\n".format(subitem[31].firstChild.nodeValue))
    pass

def EmailButtonAction():
    global SubWindow
    SubWindow = Toplevel(MainWindow)
    SubWindow.title("이메일 전송")
    SubWindow.geometry("400x300")

    # 이메일 ID
    global emailid
    emailidlabel = Label(SubWindow, text="[아이디]")
    emailidlabel.pack()
    emailidlabel.place(x=10, y=50)

    emailid = Entry(SubWindow)
    emailid.pack()
    emailid.place(x=70, y=55)

    # 이메일 PWD
    global emailpwd
    emailpwdlabel = Label(SubWindow, text="[패스워드]")
    emailpwdlabel.pack()
    emailpwdlabel.place(x=10, y=75)

    emailpwd = Entry(SubWindow)
    emailpwd.pack()
    emailpwd.place(x=70, y=80)

    # 보낼 이메일 주소
    global emailadress
    emailadresslabel = Label(SubWindow, text="[주소]")
    emailadresslabel.pack()
    emailadresslabel.place(x=10, y=100)

    emailadress = Entry(SubWindow)
    emailadress.pack()
    emailadress.place(x=70, y=105)

    # 이메일 전송 버튼
    sendbutton = Button(SubWindow, text="전송", command=SendButtonAction)
    sendbutton.pack()
    sendbutton.place(x=10, y=130)

    SubWindow.mainloop()
    pass


def SendButtonAction():
    ID = emailid.get()
    PWD = emailpwd.get()
    Adress = emailadress.get()
    SelectedItemIndex = listbox.curselection()
    if len(SelectedItemIndex):
        global SelectedItemText
        SelectedItemText = listbox.get(SelectedItemIndex[0])

        companyList = DocData.childNodes
        companyname = companyList[0].childNodes
        for item in companyname:
            if item.nodeName == "row":
                subitem = item.childNodes
                for atom in subitem:
                    if atom.nodeName in "BIZPLC_NM" and atom.firstChild.nodeValue == SelectedItemText:
                        if subitem[31].nodeName == "REFINE_LOTNO_ADDR":
                            emailtext = "회사명: " + subitem[5].firstChild.nodeValue + "\n" + "운영여부: " + subitem[9].firstChild.nodeValue + "\n" + "주소명: " + subitem[31].firstChild.nodeValue + "\n"
                        elif subitem[33].nodeName == "REFINE_LOTNO_ADDR":
                            emailtext = "회사명: " + subitem[5].firstChild.nodeValue + "\n" + "운영여부: " + subitem[9].firstChild.nodeValue + "\n" + "주소명: " + subitem[33].firstChild.nodeValue + "\n"

    msg = MIMEBase("multipart", "alternative")
    msg['Subject'] = SelectedItemText + "의 상세정보"
    msg['From'] = ID
    msg['To'] = Adress
    text = MIMEText(emailtext, _charset='UTF-8')
    msg.attach(text)

    s = smtplib.SMTP("smtp.gmail.com", 587)
    s.ehlo()
    s.starttls()
    s.ehlo()
    s.login(ID, PWD)
    s.sendmail(ID, [Adress], msg.as_string())
    s.close()
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

teller.Launcher()

MainWindow.mainloop()

