from tkinter import *
window = Tk()
window.title("공유저작물 검색 프로그램")
window.geometry("500x500")

title = Label(window, text="공유저작물 검색 프로그램", font='helvetica 16')
title.pack()
title.place(x=120,y=0)


serchbox = Entry(window)
serchbox.pack()
serchbox.place(x=10,y=60)

serchbutton = Button(window, text="검색")
serchbutton.pack()
serchbutton.place(x=150,y=60)

listbox = Listbox(window, height =23,width =30)
listbox.pack()
listbox.place(x=10,y=110)

photo = PhotoImage(file = "몽타뉴3.gif")

canvas = Label(window, height =220 , width = 235, image = photo, bg='gray91', relief="ridge")
canvas.pack()
canvas.place(x=240,y=110)

infobox= Text(window, width=34, height = 7)
infobox.pack()
infobox.place(x=240, y= 350)


emailbutton = Button(window, text="이메일로 전송")
emailbutton.pack()
emailbutton.place(x=240, y= 450)

window.mainloop()