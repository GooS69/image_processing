from tkinter import *
from PIL import Image, ImageTk, ImageDraw

scale_512 = 0
scale_255 = 0
contrast_q1 = 0
contrast_q2 = 255
gamma = 1
quantization = 1

def on_scale_512(val):
    global scale_512
    scale_512 = (int)(val)


def on_scale_255(val):
    global scale_255
    scale_255 = (int)(val)


def on_scale_q1(val):
    global contrast_q1
    contrast_q1 = (int)(val)


def on_scale_q2(val):
    global contrast_q2
    contrast_q2 = (int)(val)


def on_scale_gamma(val):
    global gamma
    gamma = (int)(val)


def on_scale_quantization(val):
    global quantization
    quantization = (int)(val)


def reset_click():
    global gray_pil_img, original_pil_img, img_label, gist_label


    gray_pil_img = gray_scale(original_pil_img)
    gray_img = ImageTk.PhotoImage(gray_pil_img)
    img_label.configure(image=gray_img)
    img_label.image = gray_img

    gist(gray_pil_img, gist_label)


def intensivity_click():
    global gray_pil_img, img_label, gist_label, scale_512

    change_intensivity(gray_pil_img, img_label, scale_512)
    gist(gray_pil_img, gist_label)


def negative_click():
    global gray_pil_img, img_label, gist_label, scale_255

    negative(gray_pil_img, img_label, scale_255)
    gist(gray_pil_img, gist_label)


def binarization_click():
    global gray_pil_img, img_label, gist_label, scale_255

    binarization(gray_pil_img, img_label, scale_255)
    gist(gray_pil_img, gist_label)


def conrast_up_click():
    global gray_pil_img, img_label, gist_label, contrast_q1, contrast_q2

    contrast_up(gray_pil_img, img_label, contrast_q1, contrast_q2)
    gist(gray_pil_img, gist_label)


def conrast_down_click():
    global gray_pil_img, img_label, gist_label, contrast_q1, contrast_q2

    contrast_down(gray_pil_img, img_label, contrast_q1, contrast_q2)
    gist(gray_pil_img, gist_label)


def gamma1_click():
    global gray_pil_img, img_label, gist_label, gamma

    gamma_change(gray_pil_img, img_label, gamma)
    gist(gray_pil_img, gist_label)


def gamma2_click():
    global gray_pil_img, img_label, gist_label, gamma

    gamma_change(gray_pil_img, img_label, 1/gamma)
    gist(gray_pil_img, gist_label)


def quantization_click():
    global gray_pil_img, img_label, gist_label, quantization

    quantization_change(gray_pil_img, img_label, quantization)
    gist(gray_pil_img, gist_label)


def gray_scale(pil_img):
    copy_pil_img = Image.new('RGB', (pil_img.size[0], pil_img.size[1]))
    for i in range(pil_img.size[0]):
        for j in range(pil_img.size[1]):
            pix = pil_img.getpixel((i, j))
            intensity = pix[0] * 0.3 + pix[1] * 0.59 + pix[2] * 0.11
            copy_pil_img.putpixel((i, j), (int(intensity), int(intensity), int(intensity)))

    return copy_pil_img


def gist(gray_pil_img, label):
    arr = [0] * 256
    for i in range(gray_pil_img.size[0]):
        for j in range(gray_pil_img.size[1]):
            arr[gray_pil_img.getpixel((i, j))[0]] += 1

    gist_pil_img = Image.new('RGB', (512, 600), 'white')
    gist_draw = ImageDraw.Draw(gist_pil_img)
    for k in range(256):
        gist_draw.rectangle([k * 2, gist_pil_img.size[1], (k * 2) + 1, gist_pil_img.size[1] - (int)(arr[k] / 30)],
                            fill='black')
    gist_img = ImageTk.PhotoImage(gist_pil_img)
    label.configure(image=gist_img)
    label.image = gist_img


def change_intensivity(pil_img, label,val):
    for i in range(pil_img.size[0]):
        for j in range(pil_img.size[1]):
            pix = pil_img.getpixel((i, j))
            new_intensivity = pix[0] + val
            if (new_intensivity > 255):
                new_intensivity = 255
            elif (new_intensivity < - 255):
                new_intensivity = -255
            pil_img.putpixel((i, j), (new_intensivity, new_intensivity, new_intensivity))
    img = ImageTk.PhotoImage(pil_img)
    label.configure(image=img)
    label.image = img


def negative(pil_img, label, val):
    for i in range(pil_img.size[0]):
        for j in range(pil_img.size[1]):
            pix = pil_img.getpixel((i, j))
            if (pix[0] >= val):
                pil_img.putpixel((i, j), (255 - pix[0], 255 - pix[0], 255 - pix[0]))
    img = ImageTk.PhotoImage(pil_img)
    label.configure(image=img)
    label.image = img


def binarization(pil_img, label, val):
    for i in range(pil_img.size[0]):
        for j in range(pil_img.size[1]):
            pix = pil_img.getpixel((i, j))
            if (pix[0] >= val):
                pil_img.putpixel((i, j), (255, 255, 255))
            else:
                pil_img.putpixel((i, j), (0, 0, 0))
    img = ImageTk.PhotoImage(pil_img)
    label.configure(image=img)
    label.image = img


def contrast_up(pil_img, label, q1, q2):
    for i in range(pil_img.size[0]):
        for j in range(pil_img.size[1]):
            pix = pil_img.getpixel((i, j))
            res_pix = ((pix[0] - q1)*(255//(q2 - q1)))
            pil_img.putpixel((i, j), (res_pix, res_pix, res_pix))
    img = ImageTk.PhotoImage(pil_img)
    label.configure(image=img)
    label.image = img


def contrast_down(pil_img, label, q1, q2):
    for i in range(pil_img.size[0]):
        for j in range(pil_img.size[1]):
            pix = pil_img.getpixel((i, j))
            res_pix = q1 + pix[0] * ((q2 - q1) // 255)
            pil_img.putpixel((i, j), (res_pix, res_pix, res_pix))
    img = ImageTk.PhotoImage(pil_img)
    label.configure(image=img)
    label.image = img


def gamma_change(pil_img, label, gamma):
    for i in range(pil_img.size[0]):
        for j in range(pil_img.size[1]):
            pix = pil_img.getpixel((i, j))
            res_pix = (int)(((pix[0] / 255) ** gamma) * 255)
            pil_img.putpixel((i, j), (res_pix, res_pix, res_pix))
    img = ImageTk.PhotoImage(pil_img)
    label.configure(image=img)
    label.image = img


def quantization_change(pil_img, label, quantization):
    q_lenght = int(255 / (2 ** quantization))
    for i in range(pil_img.size[0]):
        for j in range(pil_img.size[1]):
            pix = pil_img.getpixel((i, j))
            res_pix = (int)(pix[0] / q_lenght)
            res_pix *= q_lenght
            pil_img.putpixel((i, j), (res_pix, res_pix, res_pix))
    img = ImageTk.PhotoImage(pil_img)
    label.configure(image=img)
    label.image = img


window = Tk()
window.title("Обработка изображений. Задание 1")
window.geometry('1920x1080')

original_pil_img = Image.open('img.jpg')

gray_pil_img = gray_scale(original_pil_img)
gray_img = ImageTk.PhotoImage(gray_pil_img)

img_label = Label(window, image=gray_img)
img_label.pack(side=LEFT)

gist_label = Label(window)
gist_label.pack(side=LEFT)
gist(gray_pil_img, gist_label)

reset_button = Button(text='reset img', command=reset_click)
reset_button.pack()

scale_intensivity = Scale(window, orient='horizontal', from_=-255, to=255, command=on_scale_512)
scale_intensivity.pack()
intensivity_button = Button(text='intensivity', command=intensivity_click)
intensivity_button.pack()

scale_negative = Scale(window, orient='horizontal', from_=0, to=255, command=on_scale_255)
scale_negative.pack()
negative_button = Button(text='negative', command=negative_click)
negative_button.pack()
binarization_button = Button(text='binarization', command=binarization_click)
binarization_button.pack()

scale_q1 = Scale(window,orient = 'horizontal', label = 'q1', from_=0, to=255, command=on_scale_q1)
scale_q1.pack()
scale_q2 = Scale(window,orient = 'horizontal', label = 'q2', from_=0, to=255, command=on_scale_q2)
scale_q2.pack()
contrast_up_button = Button(text='contrast up', command=conrast_up_click)
contrast_up_button.pack()
contrast_down_button = Button(text='contrast down', command=conrast_down_click)
contrast_down_button.pack()

scale_gamma = Scale(window,orient = 'horizontal', label = 'Gamma', from_=0, to=20, command=on_scale_gamma)
scale_gamma.pack()
gamma1_button = Button(text='Gamma', command=gamma1_click)
gamma1_button.pack()
gamma2_button = Button(text='1/Gamma', command=gamma2_click)
gamma2_button.pack()

scale_quantization = Scale(window, orient = 'horizontal', label = '2^', from_=0, to=7, command=on_scale_quantization)
scale_quantization.pack()
quantization_button = Button(text='quantization', command=quantization_click)
quantization_button.pack()

window.mainloop()
