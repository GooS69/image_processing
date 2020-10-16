from tkinter import *
from PIL import Image, ImageTk, ImageDraw

scale_512 = 0
scale_255 = 0
contrast_q1 = 0
contrast_q2 = 255
gamma = 1
quantization = 1
filter_size = 1


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

    gamma_change(gray_pil_img, img_label, 1 / gamma)
    gist(gray_pil_img, gist_label)


def quantization_click():
    global gray_pil_img, img_label, gist_label, quantization

    quantization_change(gray_pil_img, img_label, quantization)
    gist(gray_pil_img, gist_label)


def solarisation_click():
    global gray_pil_img, img_label, gist_label

    solarisation(gray_pil_img, img_label)
    gist(gray_pil_img, gist_label)


def low_pass_filter_click():
    global gray_pil_img, img_label, gist_label

    low_pass_filter(gray_pil_img, img_label)
    gist(gray_pil_img, gist_label)


def high_pass_filter_click():
    global gray_pil_img, img_label, gist_label

    high_pass_filter(gray_pil_img, img_label)
    gist(gray_pil_img, gist_label)


def median_filter_click():
    global gray_pil_img, img_label, gist_label, filter_size

    median_filter(gray_pil_img, img_label, filter_size * 2 + 1)
    gist(gray_pil_img, gist_label)


def gauss_filter_click():
    global gray_pil_img, img_label, gist_label, filter_size

    gauss_filter(gray_pil_img, img_label, filter_size * 2 + 1)
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
        gist_draw.rectangle([k * 2, gist_pil_img.size[1], (k * 2) + 1, gist_pil_img.size[1] - (int)(arr[k] / 30)],
                            fill='black')
    gist_img = ImageTk.PhotoImage(gist_pil_img)
    label.configure(image=gist_img)
    label.image = gist_img


def change_intensivity(pil_img, label, val):
    all_pix = pil_img.load()
    for i in range(pil_img.size[0]):
        for j in range(pil_img.size[1]):
            pix = all_pix[i, j]
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
    all_pix = pil_img.load()
    for i in range(pil_img.size[0]):
        for j in range(pil_img.size[1]):
            pix = all_pix[i, j]
            if (pix[0] >= val):
                pil_img.putpixel((i, j), (255 - pix[0], 255 - pix[0], 255 - pix[0]))
    img = ImageTk.PhotoImage(pil_img)
    label.configure(image=img)
    label.image = img


def binarization(pil_img, label, val):
    all_pix = pil_img.load()
    for i in range(pil_img.size[0]):
        for j in range(pil_img.size[1]):
            pix = all_pix[i, j]
            if (pix[0] >= val):
                pil_img.putpixel((i, j), (255, 255, 255))
            else:
                pil_img.putpixel((i, j), (0, 0, 0))
    img = ImageTk.PhotoImage(pil_img)
    label.configure(image=img)
    label.image = img


def contrast_up(pil_img, label, q1, q2):
    all_pix = pil_img.load()
    for i in range(pil_img.size[0]):
        for j in range(pil_img.size[1]):
            pix = all_pix[i, j]
            res_pix = ((pix[0] - q1) * (255 // (q2 - q1)))
            pil_img.putpixel((i, j), (res_pix, res_pix, res_pix))
    img = ImageTk.PhotoImage(pil_img)
    label.configure(image=img)
    label.image = img


def contrast_down(pil_img, label, q1, q2):
    all_pix = pil_img.load()
    for i in range(pil_img.size[0]):
        for j in range(pil_img.size[1]):
            pix = all_pix[i, j]
            res_pix = q1 + pix[0] * ((q2 - q1) // 255)
            pil_img.putpixel((i, j), (res_pix, res_pix, res_pix))
    img = ImageTk.PhotoImage(pil_img)
    label.configure(image=img)
    label.image = img


def gamma_change(pil_img, label, gamma):
    all_pix = pil_img.load()
    for i in range(pil_img.size[0]):
        for j in range(pil_img.size[1]):
            pix = all_pix[i, j]
            res_pix = (int)(((pix[0] / 255) ** gamma) * 255)
            pil_img.putpixel((i, j), (res_pix, res_pix, res_pix))
    img = ImageTk.PhotoImage(pil_img)
    label.configure(image=img)
    label.image = img


def quantization_change(pil_img, label, quantization):
    all_pix = pil_img.load()
    q_lenght = int(255 / (2 ** quantization))
    for i in range(pil_img.size[0]):
        for j in range(pil_img.size[1]):
            pix = all_pix[i, j]
            res_pix = (int)(pix[0] / q_lenght)
            res_pix *= q_lenght
            pil_img.putpixel((i, j), (res_pix, res_pix, res_pix))
    img = ImageTk.PhotoImage(pil_img)
    label.configure(image=img)
    label.image = img


def solarisation(pil_img, label):
    all_pix = pil_img.load()
    for i in range(pil_img.size[0]):
        for j in range(pil_img.size[1]):
            pix = (int)(all_pix[i, j][0] * all_pix[i, j][0] * (-255 / 16256) + 65025 / 16256 * all_pix[i, j][0])
            pil_img.putpixel((i, j), (pix, pix, pix))
    img = ImageTk.PhotoImage(pil_img)
    label.configure(image=img)
    label.image = img


def low_pass_filter(pil_img, label):
    global gray_pil_img
    all_pix = pil_img.load()
    new_img = Image.new('RGB', (pil_img.size[0], pil_img.size[1]))

    for i in range(1, pil_img.size[0] - 1):
        for j in range(1, pil_img.size[1] - 1):
            sum = 0
            sum += all_pix[i - 1, j - 1][0]
            sum += all_pix[i, j - 1][0]
            sum += all_pix[i + 1, j - 1][0]
            sum += all_pix[i - 1, j][0]
            sum += all_pix[i, j][0]
            sum += all_pix[i + 1, j][0]
            sum += all_pix[i - 1, j + 1][0]
            sum += all_pix[i, j + 1][0]
            sum += all_pix[i + 1, j - 1][0]
            sum /= 9
            sum = (int)(sum)
            new_img.putpixel((i, j), (sum, sum, sum))

    for k in range(pil_img.size[0]):
        pix = all_pix[k, 0]
        new_img.putpixel((k, 0), (pix[0], pix[0], pix[0]))
        pix = all_pix[k, new_img.size[1] - 1]
        new_img.putpixel((k, new_img.size[1] - 1), (pix[0], pix[0], pix[0]))

    for l in range(1, new_img.size[1] - 1):
        pix = all_pix[0, l]
        new_img.putpixel((0, l), (pix[0], pix[0], pix[0]))
        pix = all_pix[new_img.size[0] - 1, l]
        new_img.putpixel((new_img.size[0] - 1, l), (pix[0], pix[0], pix[0]))

    pix = all_pix[0, 0]
    new_img.putpixel((0, 0), (pix[0], pix[0], pix[0]))

    pix = all_pix[new_img.size[0] - 1, 0]
    new_img.putpixel((new_img.size[0] - 1, 0), (pix[0], pix[0], pix[0]))

    pix = all_pix[0, new_img.size[1] - 1]
    new_img.putpixel((0, new_img.size[1] - 1), (pix[0], pix[0], pix[0]))

    pix = all_pix[new_img.size[0] - 1, new_img.size[1] - 1]
    new_img.putpixel((new_img.size[0] - 1, new_img.size[1] - 1), (pix[0], pix[0], pix[0]))

    gray_pil_img = new_img
    img = ImageTk.PhotoImage(gray_pil_img)
    label.configure(image=img)
    label.image = img


def high_pass_filter(pil_img, label):
    global gray_pil_img
    all_pix = pil_img.load()
    new_img = Image.new('RGB', (pil_img.size[0], pil_img.size[1]))

    for i in range(1, pil_img.size[0] - 1):
        for j in range(1, pil_img.size[1] - 1):
            sum = 0
            sum += all_pix[i - 1, j - 1][0]
            sum += all_pix[i, j - 1][0] * (-2)
            sum += all_pix[i + 1, j - 1][0]
            sum += all_pix[i - 1, j][0] * (-2)
            sum += all_pix[i, j][0] * 5
            sum += all_pix[i + 1, j][0] * (-2)
            sum += all_pix[i - 1, j + 1][0]
            sum += all_pix[i, j + 1][0] * (-2)
            sum += all_pix[i + 1, j - 1][0]
            sum = (int)(sum)
            if (sum > 255):
                new_img.putpixel((i, j), (255, 255, 255))
            elif (sum < 0):
                new_img.putpixel((i, j), (0, 0, 0))

    for k in range(pil_img.size[0]):
        pix = all_pix[k, 0]
        new_img.putpixel((k, 0), (pix[0], pix[0], pix[0]))
        pix = all_pix[k, new_img.size[1] - 1]
        new_img.putpixel((k, new_img.size[1] - 1), (pix[0], pix[0], pix[0]))

    for l in range(1, new_img.size[1] - 1):
        pix = all_pix[0, l]
        new_img.putpixel((0, l), (pix[0], pix[0], pix[0]))
        pix = all_pix[new_img.size[0] - 1, l]
        new_img.putpixel((new_img.size[0] - 1, l), (pix[0], pix[0], pix[0]))

    pix = all_pix[0, 0]
    new_img.putpixel((0, 0), (pix[0], pix[0], pix[0]))

    pix = all_pix[new_img.size[0] - 1, 0]
    new_img.putpixel((new_img.size[0] - 1, 0), (pix[0], pix[0], pix[0]))

    pix = all_pix[0, new_img.size[1] - 1]
    new_img.putpixel((0, new_img.size[1] - 1), (pix[0], pix[0], pix[0]))

    pix = all_pix[new_img.size[0] - 1, new_img.size[1] - 1]
    new_img.putpixel((new_img.size[0] - 1, new_img.size[1] - 1), (pix[0], pix[0], pix[0]))

    gray_pil_img = new_img
    img = ImageTk.PhotoImage(gray_pil_img)
    label.configure(image=img)
    label.image = img


def median_filter(pil_img, label, size):
    global gray_pil_img

    all_pix = pil_img.load()

    half_size = size // 2
    new_img = Image.new('RGB', (pil_img.size[0], pil_img.size[1]))

    for i in range(half_size, pil_img.size[0] - half_size - 1):
        for j in range(half_size, pil_img.size[1] - half_size - 1):
            arr = []
            for k in range(-half_size, half_size + 1):
                for m in range(-half_size, half_size + 1):
                    arr.append(all_pix[i + k, j + m][0])
            arr.sort()
            pix = arr[(size ** 2) // 2 + 1]
            new_img.putpixel((i, j), (pix, pix, pix))

    for k in range(pil_img.size[0]):
        for m in range(half_size + 1):
            pix = all_pix[k, m]
            new_img.putpixel((k, m), (pix[0], pix[0], pix[0]))
            pix = all_pix[k, new_img.size[1] - 1 - m]
            new_img.putpixel((k, new_img.size[1] - 1 - m), (pix[0], pix[0], pix[0]))

    for l in range(new_img.size[1]):
        for n in range(half_size + 1):
            pix = all_pix[n, l]
            new_img.putpixel((n, l), (pix[0], pix[0], pix[0]))
            pix = all_pix[new_img.size[0] - 1 - n, l]
            new_img.putpixel((new_img.size[0] - 1 - n, l), (pix[0], pix[0], pix[0]))

    gray_pil_img = new_img
    img = ImageTk.PhotoImage(gray_pil_img)
    label.configure(image=img)
    label.image = img


def gauss_filter(pil_img, label, size):
    global gray_pil_img

    all_pix = pil_img.load()

    half_size = size // 2
    new_img = Image.new('RGB', (pil_img.size[0], pil_img.size[1]))

    first = [1]
    second = [1]
    for i in range(1, size):
        second.append(1)
        for j in range(1, i):
            second[j] = (int)(first[j] + first[j - 1])
        first = second.copy()

    matrix = []
    for i in range(size):
        matrix.append([])
        for j in range(size):
            matrix[i].append(j)

    for i in range(size):
        for j in range(size):
            matrix[i][j] = first[i] * first[j]

    for i in range(half_size, pil_img.size[0] - half_size - 1):
        for j in range(half_size, pil_img.size[1] - half_size - 1):
            sum = 0

            for k in range(-half_size, half_size + 1):
                for m in range(-half_size, half_size + 1):
                    sum += all_pix[i + k, j + m][0] * matrix[k + half_size][m + half_size]

            sum = (int)(sum / (2 ** (size - 1)) ** 2)
            new_img.putpixel((i, j), (sum, sum, sum))

    for k in range(pil_img.size[0]):
        for m in range(half_size + 1):
            pix = all_pix[k, m]
            new_img.putpixel((k, m), (pix[0], pix[0], pix[0]))
            pix = all_pix[k, new_img.size[1] - 1 - m]
            new_img.putpixel((k, new_img.size[1] - 1 - m), (pix[0], pix[0], pix[0]))

    for l in range(new_img.size[1]):
        for n in range(half_size + 1):
            pix = all_pix[n, l]
            new_img.putpixel((n, l), (pix[0], pix[0], pix[0]))
            pix = all_pix[new_img.size[0] - 1 - n, l]
            new_img.putpixel((new_img.size[0] - 1 - n, l), (pix[0], pix[0], pix[0]))

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

scale_q1 = Scale(window, orient='horizontal', label='q1', from_=0, to=255, command=on_scale_q1)
scale_q1.pack()
scale_q2 = Scale(window, orient='horizontal', label='q2', from_=0, to=255, command=on_scale_q2)
scale_q2.pack()
contrast_up_button = Button(text='contrast up', command=conrast_up_click)
contrast_up_button.pack()
contrast_down_button = Button(text='contrast down', command=conrast_down_click)
contrast_down_button.pack()

scale_gamma = Scale(window, orient='horizontal', label='Gamma', from_=0, to=20, command=on_scale_gamma)
scale_gamma.pack()
gamma1_button = Button(text='Gamma', command=gamma1_click)
gamma1_button.pack()
gamma2_button = Button(text='1/Gamma', command=gamma2_click)
gamma2_button.pack()

scale_quantization = Scale(window, orient='horizontal', label='2^', from_=0, to=7, command=on_scale_quantization)
scale_quantization.pack()
quantization_button = Button(text='quantization', command=quantization_click)
quantization_button.pack()

solarisation_button = Button(text='solarisation', command=solarisation_click)
solarisation_button.pack()

low_pass_filter_button = Button(text='low pass filter', command=low_pass_filter_click)
low_pass_filter_button.pack()

high_pass_filter_button = Button(text='high pass filter', command=high_pass_filter_click)
high_pass_filter_button.pack()

scale_filter_size = Scale(window, orient='horizontal', label='size of filter', from_=1, to=10,
                          command=on_scale_filter_size)
scale_filter_size.pack()
median_filter_button = Button(text='median filter', command=median_filter_click)
median_filter_button.pack()
gauss_filter_button = Button(text='gauss filter', command=gauss_filter_click)
gauss_filter_button.pack()

window.mainloop()
