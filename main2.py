from tkinter import *
from PIL import Image, ImageTk, ImageDraw

filter_size = 1


def on_scale_filter_size(val):
    global filter_size
    filter_size = (int)(val)


def reset_click():
    global gray_pil_img, original_pil_img, img_label, gist_label

    gray_pil_img = gray_scale(original_pil_img)
    gray_img = ImageTk.PhotoImage(gray_pil_img)
    img_label.configure(image=gray_img)
    img_label.image = gray_img

    gist(gray_pil_img, gist_label)


def sobel_click():
    global gray_pil_img, img_label, gist_label, filter_size

    sobel(gray_pil_img, img_label, filter_size * 2 + 1)
    gist(gray_pil_img, gist_label)


def kirsh_click():
    global gray_pil_img, img_label, gist_label, filter_size

    kirsh(gray_pil_img, img_label, filter_size * 2 + 1)
    gist(gray_pil_img, gist_label)


def indentation_click():
    global gray_pil_img, img_label, gist_label, filter_size

    tisnenie(gray_pil_img, img_label, 1)
    gist(gray_pil_img, gist_label)


def extrusion_click():
    global gray_pil_img, img_label, gist_label, filter_size

    tisnenie(gray_pil_img, img_label, -1)
    gist(gray_pil_img, gist_label)


def binarization_click():
    global gray_pil_img, img_label, gist_label, filter_size

    binarization(gray_pil_img, img_label)
    gist(gray_pil_img, gist_label)



def gray_scale(pil_img):
    all_pix = pil_img.load()
    copy_pil_img = Image.new('RGB', (pil_img.size[0], pil_img.size[1]))
    for i in range(pil_img.size[0]):
        for j in range(pil_img.size[1]):
            pix = all_pix[i, j]
            intensity = pix[0] * 0.3 + pix[1] * 0.59 + pix[2] * 0.11
            copy_pil_img.putpixel((i, j), (int(intensity), int(intensity), int(intensity)))

    return copy_pil_img


def gist(gray_pil_img, label):
    all_pix = gray_pil_img.load()
    arr = [0] * 256
    for i in range(gray_pil_img.size[0]):
        for j in range(gray_pil_img.size[1]):
            arr[all_pix[i, j][0]] += 1

    gist_pil_img = Image.new('RGB', (512, 600), 'white')
    gist_draw = ImageDraw.Draw(gist_pil_img)
    for k in range(256):
        gist_draw.rectangle([k * 2, gist_pil_img.size[1] - (int)(arr[k] / 30), (k * 2) + 1, gist_pil_img.size[1]],
                            fill='black')
    gist_img = ImageTk.PhotoImage(gist_pil_img)
    label.configure(image=gist_img)
    label.image = gist_img


def sobel(pil_img, label, size):
    global gray_pil_img

    all_pix = pil_img.load()

    half_size = size // 2
    new_img = Image.new('RGB', (pil_img.size[0], pil_img.size[1]))

    matrix1 = []
    for i in range(size):
        matrix1.append([])
        for j in range(size):
            matrix1[i].append(0)

    const = 0

    for i in range(half_size + 1):
        a = half_size + const
        for j in range(half_size):
                matrix1[i][j] = a
                matrix1[i][size - j - 1] = -(a)

                matrix1[size - i - 1][j] = a
                matrix1[size - i - 1][size - j - 1] = -(a)
                a -= 1
        const += 1

    matrix2 = []
    for i in range(size):
        matrix2.append([])
        for j in range(size):
            matrix2[i].append(0)

    const = 0

    for i in range(half_size + 1):
        a = half_size + const
        for j in range(half_size):
            matrix2[j][i] = a
            matrix2[j][size - i - 1] = a

            matrix2[size - j - 1][i] = -(a)
            matrix2[size - j - 1][size - i - 1] = -(a)
            a -= 1
        const += 1

    for i in matrix1:
        print(i)
    for i in matrix2:
        print(i)

    for i in range(half_size, pil_img.size[0] - half_size - 1):
        for j in range(half_size, pil_img.size[1] - half_size - 1):
            sum1 = 0
            sum2 = 0

            for k in range(-half_size, half_size + 1):
                for m in range(-half_size, half_size + 1):
                    sum1 += all_pix[i + k, j + m][0] * matrix1[k + half_size][m + half_size]
                    sum2 += all_pix[i + k, j + m][0] * matrix2[k + half_size][m + half_size]

            s = (int)((sum1**2 + sum2**2)**0.5)
            new_img.putpixel((i, j), (s, s, s))

    gray_pil_img = new_img
    img = ImageTk.PhotoImage(gray_pil_img)
    label.configure(image=img)
    label.image = img


def wrapper(x, y, matrix):
    size = len(matrix)
    for i in range(size):
        matrix[i] = [-y] + matrix[i] + [-y]

    m1 = [[]]
    m2 = [[]]
    for i in range(size + 2):
        m1[0].append(x)
        m2[0].append(-y)

    matrix = m1 + matrix + m2
    return matrix


def move_circle(matrix, r):
    size = len(matrix)
    half_size = size // 2

    save1 = matrix[half_size - r][half_size + r - 1]
    for i1 in range(half_size + r - 1, half_size - r - 1, -1):
        if (i1 - 1) >= half_size - r:
            matrix[half_size - r][i1] = matrix[half_size - r][i1 - 1]
        else:
            matrix[half_size - r][i1] = 0


    save2 = matrix[half_size + r - 1][half_size + r]
    for i2 in range(half_size + r - 1, half_size - r - 1, -1):
        if (i2 - 1) >= half_size - r:
            matrix[i2][half_size + r] = matrix[i2 - 1][half_size + r]
        else:
            matrix[i2][half_size + r] = save1


    save3 = matrix[half_size + r][half_size - r + 1]
    for i3 in range(half_size - r + 1, half_size + r + 1, +1):
        if (i3 + 1) <= half_size + r:
            matrix[half_size + r][i3] = matrix[half_size + r][i3 + 1]
        else:
            matrix[half_size + r][i3] = save2

    save4 = matrix[half_size - r + 1][half_size - r]
    for i4 in range(half_size - r + 1, half_size + r + 1, +1):
        if (i4 + 1) <= half_size + r:
            matrix[i4][half_size - r] = matrix[i4 + 1][half_size - r]
        else:
            matrix[i4][half_size - r] = save3

    matrix[half_size - r][half_size - r] = save4

    return matrix


def kirsh(pil_img, label, size):
    global gray_pil_img

    all_pix = pil_img.load()

    half_size = size // 2
    new_img = Image.new('RGB', (pil_img.size[0], pil_img.size[1]))

    primex = [5,11,17,23,31,41,47]
    primey = [3,5,7,11,13,17,19]

    matrix = [[0]]

    for i in range(half_size):
        matrix = wrapper(primex[i], primey[i], matrix)


    for i in matrix:
        print(i)


    for i in range(half_size, pil_img.size[0] - half_size - 1):
        for j in range(half_size, pil_img.size[1] - half_size - 1):
            max = 0

            for i1 in range(half_size * 8):
                sum = 0

                for j1 in range(1, half_size + 1):
                    if (i1 % j1 == 0):
                        move_circle(matrix, half_size + 1 - j1)

                for k in range(-half_size, half_size + 1):
                    for m in range(-half_size, half_size + 1):
                        sum += all_pix[i + k, j + m][0] * matrix[k + half_size][m + half_size]

                if (abs(sum) > max):
                    max = abs(sum)


            new_img.putpixel((i, j), (max, max, max))

    gray_pil_img = new_img
    img = ImageTk.PhotoImage(gray_pil_img)
    label.configure(image=img)
    label.image = img


def tisnenie(pil_img, label, parametr):
    global gray_pil_img
    all_pix = pil_img.load()
    new_img = Image.new('RGB', (pil_img.size[0], pil_img.size[1]))

    for i in range(1, pil_img.size[0] - 1):
        for j in range(1, pil_img.size[1] - 1):
            sum = 0
            sum += all_pix[i, j - 1][0] * (1) * parametr
            sum += all_pix[i - 1, j][0] * (1) * parametr
            sum += all_pix[i + 1, j][0] * (-1) * parametr
            sum += all_pix[i, j + 1][0] * (-1) * parametr
            sum += 128
            sum = (int)(sum)
            if (sum > 255):
                new_img.putpixel((i, j), (255, 255, 255))
            elif (sum < 0):
                new_img.putpixel((i, j), (0, 0, 0))
            else:
                new_img.putpixel((i, j), (sum, sum, sum))

    gray_pil_img = new_img
    img = ImageTk.PhotoImage(gray_pil_img)
    label.configure(image=img)
    label.image = img


def binarization(pil_img, label):
    global gray_pil_img
    all_pix = pil_img.load()
    new_img = Image.new('RGB', (pil_img.size[0], pil_img.size[1]))

    s1 = 0
    s2 = 0
    s1_new = 63
    s2_new = 191

    while(abs(s1 - s1_new) > 1 and abs(s2-s2_new) > 1):
        arr1 = []
        arr2 = []

        for i in range(0, pil_img.size[0]):
            for j in range(0, pil_img.size[1]):
                if abs(all_pix[i,j][0] - s1_new) < abs(all_pix[i,j][0] - s2_new):
                    arr1.append(all_pix[i,j][0])
                else:
                    arr2.append(all_pix[i,j][0])

        s1 = s1_new
        s2 = s2_new

        s1_new = sum(arr1)/len(arr1)
        s2_new = sum(arr2)/len(arr2)

    for i in range(0, pil_img.size[0]):
        for j in range(0, pil_img.size[1]):
            if abs(all_pix[i, j][0] - s1_new) < abs(all_pix[i, j][0] - s2_new):
                new_img.putpixel((i,j),((int)(s1_new),(int)(s1_new),(int)(s1_new)))
            else:
                new_img.putpixel((i,j),((int)(s2_new),(int)(s2_new),(int)(s2_new)))

    gray_pil_img = new_img
    img = ImageTk.PhotoImage(gray_pil_img)
    label.configure(image=img)
    label.image = img




window = Tk()
window.title("Обработка изображений")
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

scale_filter_size = Scale(window, orient='horizontal', label='size of filter', from_=1, to=10,
                          command=on_scale_filter_size)
scale_filter_size.pack()

sobel_button = Button(text='Sobel', command=sobel_click)
sobel_button.pack()

kirsh_button = Button(text='Kirsh', command=kirsh_click)
kirsh_button.pack()

indentation_button = Button(text='indentation', command=indentation_click)
indentation_button.pack()

extrusion_button = Button(text='extrusion', command=extrusion_click)
extrusion_button.pack()

binarization_button = Button(text='binarization', command=binarization_click)
binarization_button.pack()



window.mainloop()
