from tkinter import *
from io import BytesIO
import urllib
import urllib.request
from PIL import Image, ImageTk


root = Tk()
root.geometry("500x500+500+200")

# openapi로 이미지 url을 가져옴.
url =  'https://maps.googleapis.com/maps/api/staticmap?center=Brooklyn+Bridge,New+York,NY&zoom=13&size=600x300&maptype=roadmap&markers=color:blue%7Clabel:S%7C40.702147,-74.015794&markers=color:green%7Clabel:G%7C40.711614,-74.012318&markers=color:red%7Clabel:C%7C40.718217,-73.998284&key=AIzaSyCam6mmZ2GXK0qdLYRTFOd113RoWkF-ypk'
with urllib.request.urlopen(url) as u:
    raw_data = u.read()


im = Image.open(BytesIO(raw_data))
image = ImageTk.PhotoImage(im)

label = Label(root, image=image, height=400, width=400)
label.pack()
label.place(x=0, y=0)
root.mainloop()
