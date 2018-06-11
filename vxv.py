# 인터페이스
from tkinter import *
from tkinter.ttk import *
# 웹페이지 로드
import urllib.request
import urllib.parse
# 정규표현식
import re

TITLE = '네이버 연관 검색어 파서'
DESCRIPTION = '네이버에 키워드를 검색했을 때, 연관 검색어를 파싱해오는 프로그램입니다.'


### 메인 함수
def main():
    # 윈도우 생성
    winMain = Tk()
    winMain.title(TITLE)
    winMain.geometry('520x250')

    # 프레임1 생성
    fraKeyword = Frame(winMain)
    fraKeyword.pack(fill=X)

    # `검색어` 라벨 생성
    lblKeyword = Label(fraKeyword, text='검색어', width=9)
    lblKeyword.pack(side=LEFT, padx=10, pady=10)

    ### 검색어 입력 엔트리 엔터키 입력 콜백 함수
    def txtKeyword_Enter_Keypress(event):
        # 엔터 누르면 검색 버튼 클릭
        btnSearch_Click()
        return

    # 검색어 입력 엔트리 생성
    strKeyword = StringVar()
    txtKeyword = Entry(fraKeyword, textvariable=strKeyword)
    txtKeyword.pack(fill=X, padx=10, expand=True)
    txtKeyword.bind("<Return>", txtKeyword_Enter_Keypress)
    strKeyword.set('잇꽃')

    # 프레임2 생성
    fraResult = Frame(winMain)
    fraResult.pack(fill=X)

    # `연관 검색어` 라벨 생성
    lblResult = Label(fraResult, text='연관 검색어', width=9)
    lblResult.pack(side=LEFT, anchor=N, padx=10, pady=5)

    ### 리스트박스 더블클릭 이벤트 콜백 함수
    def lstResult_DblClick(self):
        # 선택된 행이 있으면 그걸 키워드로 검색함
        SelectedItemIndex = lstResult.curselection()
        if len(SelectedItemIndex):
            SelectedItemText = lstResult.get(SelectedItemIndex[0])
            strKeyword.set(SelectedItemText)
            btnSearch_Click()
        return

    # 결과 리스트 박스 생성
    lstResult = Listbox(fraResult)
    lstResult.pack(fill=X, padx=10, pady=5)
    lstResult.bind("<Double-Button-1>", lstResult_DblClick)

    # 프레임3 생성
    fraSearch = Frame(winMain)
    fraSearch.pack(fill=X)

    # 검색 결과 라벨 생성
    strSearch = StringVar()
    lblSearch = Label(fraSearch, width=55, textvariable=strSearch)
    lblSearch.pack(side=LEFT, fill=X, anchor=N, padx=10, pady=10)

    ### 검색 버튼 클릭 이벤트 콜백 함수
    def btnSearch_Click():
        # 위젯을 초기화함
        strSearch.set('잠시만 기다려주세요.')
        lstResult.delete(0, END)

        # 검색어를 가져옴
        Keyword = strKeyword.get().strip()
        if Keyword == '':
            strSearch.set('검색어를 입력해주세요.')
            txtKeyword.focus_set()
            return

        # 웹페이지로부터 데이터를 받아옴
        try:
            f = urllib.request.urlopen(
                'https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=0&ie=utf8&query=' + urllib.parse.quote(
                    Keyword))
            res = f.read().decode('utf-8')
        except:
            strSearch.set('웹 페이지를 불러오는 중 오류가 발생했습니다.')
            return

        # 연관검색어를 파싱함
        try:
            dd_tag = res[res.find('<dd class="lst_relate">') + len('<dd class="lst_relate">'):]
            dd_tag = dd_tag[:dd_tag.find('</dd>')]

            a_tag = re.findall('<a href="[^"]+" data-idx="\d+" data-area="[^"]*">([^<]+)</a>', dd_tag)
        except:
            strSearch.set('연관 검색어가 없습니다.')
            return

        # 결과를 출력함
        for index, tag in enumerate(a_tag):
            lstResult.insert(END, tag)
        strSearch.set(
            '`%s`의 연관 검색어는 총 %d건입니다.' % ((Keyword[:16] + '...' if len(Keyword) > 19 else Keyword), len(a_tag)))
        return

    # 검색 버튼 생성
    btnSearch = Button(fraSearch, text='검색', command=btnSearch_Click)
    btnSearch.pack(side=RIGHT, padx=10, pady=5)

    # 윈도우 메세지 루프
    winMain.mainloop()


### 엔트리포인트
main()