from tkinter import *
from PIL import Image, ImageTk, ImageDraw
import math

def reset_click():
    global copy_pil_img, original_pil_img, img_label

    sourse_img = original_pil_img.copy()
    sourse = ImageTk.PhotoImage(sourse_img)

    copy_pil_img = sourse_img
    img_label.configure(image=sourse)
    img_label.image = sourse


def find_line_click():
    global img_label
    find_line(img_label)



def find_line(label):
    global copy_pil_img
    all_pix = copy_pil_img.load()
    new_img = Image.new('RGB', (copy_pil_img.size[0], copy_pil_img.size[1]))

    for i in range(copy_pil_img.size[0]):
        for j in range(copy_pil_img.size[1]):
            new_img.putpixel((i,j), (all_pix[i,j][0], all_pix[i,j][0], all_pix[i,j][0]))

    H = []
    diag = (int)((copy_pil_img.size[0]**2 + copy_pil_img.size[1]**2) ** 0.5) + 2
    for i in range(180 + 2):
        H.append([])
        for j in range(diag):
            H[i].append(0)

    for i in range(copy_pil_img.size[0]):
        for j in range(copy_pil_img.size[1]):
            if (all_pix[i,j][0] > 128):
                continue
            for fi in range(180):
                R = (int)(i * math.cos(math.radians(fi)) + j * math.sin(math.radians(fi)))
                H[fi + 1][R + 1] += 1


    fi_max = -1
    R_max = -1
    H_max = -1
    for fi in range(1, 181):
        for R in range(1 , diag - 1):
            if(H[fi][R] > H_max):
                fi_max = fi
                R_max = R
                H_max = H[fi][R]

    fi_max -= 1
    R_max -= 1
    print(fi_max, R_max)
    print(math.sin(math.radians(fi_max)))

    for x in range(copy_pil_img.size[0]):
        y = (int)((R_max - x * math.cos(math.radians(fi_max)))/(math.sin(math.radians(fi_max))))
        if (y >= 0 and y < copy_pil_img.size[1]):
            new_img.putpixel((x,y), (255, 0, 0))


    #for fi in range(1,181):
    #    for R in range(1 , diag - 1):
    #        local_max = max(
    #        H[fi - 1][R - 1],
    #        H[fi][ R - 1],
    #        H[fi + 1][ R - 1],
    #        H[fi - 1][ R],
    #        H[fi + 1][ R],
    #        H[fi - 1][ R + 1],
    #        H[fi][ R + 1],
    #        H[fi + 1][ R - 1]
    #        )
    #        middle_elem = H[fi][R]
    #
    #        if (middle_elem > local_max):
    #            for x in range(copy_pil_img.size[0]):
    #                y = (int)((R  - x * math.cos(math.radians(fi))) / (math.sin(math.radians(fi ))))
    #                if (y >= 0 and y < copy_pil_img.size[1]):
    #                    new_img.putpixel((x,y), (255, 0, 0))



    img = ImageTk.PhotoImage(new_img)
    label.configure(image=img)
    label.image = img


window = Tk()
window.title("Обработка изображений")
window.geometry('1920x1080')

original_pil_img = Image.open('img3.jpg')
original_img = ImageTk.PhotoImage(original_pil_img)

copy_pil_img = original_pil_img.copy()

img_label = Label(window, image=original_img)
img_label.pack(side=LEFT)

reset_button = Button(text='reset img', command=reset_click)
reset_button.pack()

find_line_button = Button(text='find line', command=find_line_click)
find_line_button.pack()

window.mainloop()