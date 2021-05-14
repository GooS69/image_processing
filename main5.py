from tkinter import *
from PIL import Image, ImageTk, ImageDraw

reference = []
for i in range(10):
    reference.append([])
    for j in range(25):
        reference[i].append(0)


def get_reference():
    global reference_pil_img, reference
    all_pix = reference_pil_img.load()

    for n in range(10):

        for x in range(5):
            #print(100 * n + 20 * x)
            for y in range(5):

                for i in range(20):
                    for j in range(27):
                        if(all_pix[100 * n + 20 * x + i, 27 * y + j][0] <= 127):
                            reference[n][5 * x + y] += 1

    #for k in reference:
    #    print(k)



def find_digit():
    global original_pil_img, reference
    all_pix = original_pil_img.load()
    digit = []
    for i in range(25):
        digit.append(0)

    for x in range(5):
        for y in range(5):

            for i in range(20):
                for j in range(27):
                    if (all_pix[20 * x + i, 27 * y + j][0] <= 127):
                        digit[5 * x + y] += 1

    min_delta = 1000000
    min_n = -1

    for n in range(10):
        sum = 0
        for k in range(25):
            sum += abs(reference[n][k] - digit[k])
        if(sum <= min_delta):
            min_delta = sum
            min_n = n

    print(min_n)

    #print(digit)


original_pil_img = Image.open('img5.jpg')
reference_pil_img = Image.open('reference.jpg')
get_reference()
find_digit()