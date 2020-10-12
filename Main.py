from tkinter import *
from PIL import Image, ImageTk, ImageDraw


def on_scale_intensivity(val):
    global gray_pil_img, img_label
    change_intensivity(gray_pil_img, img_label, (int)(val))

# def onScaleG(val):

# def onScaleB(val):

# def click():


def gray_scale(pil_img):
    for i in range(pil_img.size[0]):
        for j in range(pil_img.size[1]):
            pix = pil_img.getpixel((i, j))
            intensity = pix[0] * 0.3 + pix[1] * 0.59 + pix[2] * 0.11
            pil_img.putpixel((i, j), (int(intensity), int(intensity), int(intensity)))

    return pil_img


def gist(gray_pil_img):
    arr = [0] * 256
    for i in range(gray_pil_img.size[0]):
        for j in range(gray_pil_img.size[1]):
            arr[gray_pil_img.getpixel((i, j))[0]] += 1

    gist_img = Image.new('RGB', (512, 400), 'white')
    gist_draw = ImageDraw.Draw(gist_img)
    for k in range(256):
        gist_draw.rectangle([k * 2, gist_img.size[1], (k * 2) + 1, gist_img.size[1] - (int)(arr[k] / 30)], fill='black')
        print(arr[k] / 30)
    return gist_img


def change_intensivity(pil_img, label,val):
    for i in range(pil_img.size[0]):
        for j in range(pil_img.size[1]):
            pix = pil_img.getpixel((i, j))
            new_intensivity = pix[0] + val
            if (new_intensivity > 255):
                new_intensivity = 255
            elif (new_intensivity < - 255):
                new_intensivity = -255
            pil_img.putpixel((i, j), (new_intensivity,new_intensivity,new_intensivity))
    img = ImageTk.PhotoImage(pil_img)
    label.configure(image = img)
    label.photo_ref(img)


window = Tk()
window.title("Обработка изображений. Задание 1")
window.geometry('1920x1080')

original_pil_img = Image.open('img.jpg')

gray_pil_img = gray_scale(original_pil_img)
gray_img = ImageTk.PhotoImage(gray_pil_img)

gist_pil_img = gist(gray_pil_img)
gist_img = ImageTk.PhotoImage(gist_pil_img)

img_label = Label(window, image=gray_img)
img_label.pack(side=LEFT)
gist_label = Label(window, image=gist_img)
gist_label.pack(side=LEFT)

scale_intensivity = Scale(window,orient = 'horizontal', from_= -255, to=255, label = 'Intensivity' , command=on_scale_intensivity)
scale_intensivity.pack()
# scaleG = Scale(window,orient = 'horizontal', from_=0, to=100, command=onScaleG)
# scaleG.pack()
# scaleB = Scale(window,orient = 'horizontal', from_=0, to=100, command=onScaleB)
# scaleB.pack()

# btn = Button(text='click', command =click)
# btn.pack()

window.mainloop()
