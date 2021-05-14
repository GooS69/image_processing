from tkinter import *
from PIL import Image, ImageTk, ImageDraw


scope = 1
mode = 1
x1 = 0
y1 = 0
x2 = 0
y2 = 0


def reset_click():
    global copy_pil_img, original_pil_img, img_label

    sourse_img = original_pil_img.copy()
    sourse = ImageTk.PhotoImage(sourse_img)

    copy_pil_img = sourse_img
    img_label.configure(image=sourse)
    img_label.image = sourse


def on_scale_scope(value):
    global scope
    scope = (float)(value)


def change_mode_neighbor():
    global mode
    mode = 1


def change_mode_biline():
    global mode
    mode = 2


def button_press(event):
    global x1, y1
    x1 = event.x
    y1 = event.y
    print(event.x, event.y)


def button_realese(event):
    global copy_pil_img, img_label, scope_label, x1, y1, x2, y2, scope, mode
    x2 = event.x
    y2 = event.y
    print(event.x, event.y)

    if(x1 > x2):
        x1 , x2 = x2, x1

    if(y1 > y2):
        y1 , y2 = y2, y1

    draw_rectangle(img_label, x1, y1, x2, y2)
    if (mode == 1):
        scope_neighbor(scope_label, x1, y1, x2, y2, scope)
    elif (mode == 2):
        scope_biline(scope_label, x1, y1, x2, y2, scope)

def draw_rectangle(label, x1, y1, x2, y2):
    global copy_pil_img

    all_pix = copy_pil_img.load()

    new_img = Image.new('RGB', (copy_pil_img.size[0], copy_pil_img.size[1]))

    for i in range(0, copy_pil_img.size[0]):
        for j in range(0, copy_pil_img.size[1]):
            pix = all_pix[i, j]
            new_img.putpixel((i,j),(pix[0],pix[1],pix[2]))

    for i in range(x1, x2 + 1, 1):
        new_img.putpixel((i, y1), (0, 0, 0))
        new_img.putpixel((i, y2), (0, 0, 0))


    for i in range(y1, y2 + 1, 1):
        new_img.putpixel((x1, i), (0, 0, 0))
        new_img.putpixel((x2, i), (0, 0, 0))


    img = ImageTk.PhotoImage(new_img)
    label.configure(image=img)
    label.image = img


def scope_neighbor(label, x1, y1, x2, y2, scope):
    global copy_pil_img
    all_pix = copy_pil_img.load()
    new_img = Image.new('RGB', ((int)(abs(x1 - x2) * scope), (int)(abs(y1 - y2) * scope)))

    for i in range(0, new_img.size[0]):
        for j in range(0, new_img.size[1]):
            pix = all_pix[x1 + (int)(i/scope + 0.5) , y1 + (int)(j/scope + 0.5)]
            new_img.putpixel((i,j),(pix[0],pix[1],pix[2]))


    img = ImageTk.PhotoImage(new_img)
    label.configure(image=img)
    label.image = img


def scope_biline(label, x1, y1, x2, y2, scope):
    global copy_pil_img
    all_pix = copy_pil_img.load()
    new_img = Image.new('RGB', ((int)(abs(x1 - x2) * scope), (int)(abs(y1 - y2) * scope)))

    for i in range(0, new_img.size[0]):
        for j in range(0, new_img.size[1]):
            u = (int)(i/scope) + x1
            v = (int)(j/scope) + y1
            s = i/scope - u + x1
            t = j/scope - v + y1
            pixR = (1 - s) * (1 - t) * all_pix[u, v][0] + \
                   s * (1 - t) * all_pix[u + 1, v][0] + \
                   (1 - s) * t * all_pix[u, v + 1][0] + \
                   s * t * all_pix[u + 1, v + 1][0]
            pixG = (1 - s) * (1 - t) * all_pix[u, v][1] + \
                   s * (1 - t) * all_pix[u + 1, v][1] + \
                   (1 - s) * t * all_pix[u, v + 1][1] + \
                   s * t * all_pix[u + 1, v + 1][1]
            pixB = (1 - s) * (1 - t) * all_pix[u, v][2] + \
                   s * (1 - t) * all_pix[u + 1, v][2] + \
                   (1 - s) * t * all_pix[u, v + 1][2] + \
                   s * t * all_pix[u + 1, v + 1][2]

            new_img.putpixel((i,j),((int)(pixR),(int)(pixG),(int)(pixB)))


    img = ImageTk.PhotoImage(new_img)
    label.configure(image=img)
    label.image = img


window = Tk()
window.title("Обработка изображений")
window.geometry('1920x1080')

original_pil_img = Image.open('img.jpg')
original_img = ImageTk.PhotoImage(original_pil_img)

copy_pil_img = original_pil_img.copy()


img_label = Label(window, image=original_img)
img_label.pack(side=LEFT)
img_label.bind("<Button>", button_press)
img_label.bind("<ButtonRelease>", button_realese)

scope_label = Label(window, image=original_img)
scope_label.pack(side=LEFT)


reset_button = Button(text='reset img', command=reset_click)
reset_button.pack()

scale_scope = Scale(window, orient='horizontal', label='Scope', resolution=0.1,from_=0.1, to=5, command=on_scale_scope)
scale_scope.pack()

neighbor_button = Button(text='Neighbor', command=change_mode_neighbor)
neighbor_button.pack()

biline_button = Button(text='Biline', command=change_mode_biline)
biline_button.pack()

window.mainloop()