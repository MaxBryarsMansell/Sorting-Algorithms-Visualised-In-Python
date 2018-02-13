#Written By Max Bryars-Mansell

import random, tkinter, os, colorsys, time, threading, queue
from math import floor
from copy import copy

# Properties
w = 1280
h = 720
minElements = 100
maxElements = 500
animation_delay = 10 #in ms
COLOUR_MODE = True
DISPLAY_MODE_DOTS = False

def bubbleSort(data):
    last = time.perf_counter()
    for e in range(len(data) - 1, 0, -1):
        for i in range(1, len(data)):
            if data[i - 1] > data[i]:
                data[i], data[i - 1] = data[i - 1], data[i]

                queue.put(lambda: DrawList(data, i))
                queue.put(lambda: canvas.update())
                queue.put(lambda: canvas.delete("all"))
                time.sleep(animation_delay / 1000)
    print("Sorted with Bubble Sort in", time.perf_counter() - last)

def mergeSort(data):
    last = time.perf_counter()
    n = len(data)
    step = 1
    while (step < n):
        i = 0
        while (i < n - step):
            a = data[i:i + step]
            b = data[i + step:min(i + 2 * step, n)]
            for k in range(i, min(i + 2 * step, n)):
                if (len(a) > 0 and len(b) > 0):
                    if (a[0] > b[0]):
                        data[k] = b[0]
                        b.remove(b[0])
                    else:
                        data[k] = a[0]
                        a.remove(a[0])
                else:
                    for p in range(k, min(i + 2 * step, n)):
                        if (len(b) > 0):
                            data[p] = b[0]
                            b.remove(b[0])
                    for j in range(k, min(i + 2 * step, n)):
                        if (len(a) > 0):
                            data[j] = a[0]
                            a.remove(a[0])

                queue.put(lambda: DrawList(data, k))
                queue.put(lambda: canvas.update())
                queue.put(lambda: canvas.delete("all"))
                time.sleep(animation_delay / 1000)
            i = i + 2 * step
        step = step * 2
    print("Sorted with Merge Sort in ",time.perf_counter() - last)

def selectionSort(data):
    last = time.perf_counter()
    for e in range(len(data)):
        smallest = e
        for j in range(e + 1, len(data)):
            if data[j] < data[smallest]: smallest = j;

            queue.put(lambda: DrawList(data, j))
            queue.put(lambda: canvas.update())
            queue.put(lambda: canvas.delete("all"))
            time.sleep(animation_delay / 1000)
        temp = data[e]
        data[e] = data[smallest]
        data[smallest] = temp
    print("Sorted with Selection Sort in ", time.perf_counter() - last)

def insertionSort(data):
    last = time.perf_counter()
    for e in range(1, len(data)):
        index = data[e]
        j = e
        while j > 0 and data[j-1] > index:
            data[j] = data[j-1]
            j -= 1

            queue.put(lambda: DrawList(data, j))
            queue.put(lambda: canvas.update())
            queue.put(lambda: canvas.delete("all"))
            time.sleep(animation_delay / 1000)
        data[j] = index
    print("Sorted with Insertion Sort in ", time.perf_counter() - last)

def DrawList(data, current_selection):
    width = w / len(data)
    height = 0
    x, y = 0, h
    for e in range(0, len(data)):
        if not COLOUR_MODE: colour = "red";
        else:
            depth = 256 - floor((256 / h) * data[e])
            (r, g, b) = colorsys.hsv_to_rgb(float(depth) / 256, 1.0, 1.0)
            R, G, B = int(255 * r), int(255 * g), int(255 * b)
            colour = '#%02x%02x%02x' % (R, G, B)
        if e == current_selection: colour = "white";
        if not DISPLAY_MODE_DOTS:
            canvas.create_rectangle(x, y , x + width, y - data[e], fill=colour)
        else:
            canvas.create_oval(x, y - data[e], x + width, y - data[e] + width, fill=colour)
        x += width

def Main():
    while True:
        lst = random.sample(range(0, h - 10), random.randint(minElements, maxElements))
        lst_copy = copy(lst)

        mergeSort(lst)
        with queue.mutex:
            queue.queue.clear()

        lst = copy(lst_copy)
        insertionSort(lst)
        with queue.mutex:
            queue.queue.clear()

        lst = copy(lst_copy)
        selectionSort(lst)
        with queue.mutex:
            queue.queue.clear()

        lst = copy(lst_copy)
        bubbleSort(lst)
        with queue.mutex:
            queue.queue.clear()

        lst = []


def Cleanup():
    window.quit()
    os._exit(0)

window = tkinter.Tk()
window.protocol("WM_DELETE_WINDOW", Cleanup)
window.title("Sorting Algorithms Visualised")

canvas = tkinter.Canvas(window, bg="black", height=h, width=w)
canvas.pack()

queue = queue.Queue()

thread = threading.Thread(target = Main, args = ())
thread.daemon = True
thread.start()

while True:
    function = queue.get()
    function()
