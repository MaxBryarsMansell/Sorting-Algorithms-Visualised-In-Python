#Written By Max Bryars-Mansell

import random, tkinter, os, colorsys, time, _thread, queue
from math import floor
from copy import copy
from enum import Enum

# Properties
w = 1280
h = 720
minElements = 100
maxElements = 1000
ANIMATION_DELAY = 1 #in ms
COLOUR_MODE = True
DISPLAY_MODE_DOTS = False

def bubbleSort(data):
    global queue
    last = time.perf_counter()
    for e in range(len(data) - 1, 0, -1):
        for i in range(1, len(data)):
            if data[i - 1] > data[i]:
                data[i], data[i - 1] = data[i - 1], data[i]
                queue.put(lambda: DrawList(data, i))
                time.sleep(ANIMATION_DELAY / 1000) 
              
    print("Sorted with Bubble Sort in", time.perf_counter() - last, "seconds.")
    EndSort()
    return

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

                queue.put(lambda: DrawList(data, i))
                time.sleep(ANIMATION_DELAY / 1000)
            i = i + 2 * step
        step = step * 2
    print("Sorted with Merge Sort in ", time.perf_counter() - last, "seconds.")
    EndSort()
    return

def selectionSort(data):
    last = time.perf_counter()
    for e in range(len(data)):
        smallest = e
        for j in range(e + 1, len(data)):
            if data[j] < data[smallest]: smallest = j;

            queue.put(lambda: DrawList(data, j))
            time.sleep(ANIMATION_DELAY / 1000)
        temp = data[e]
        data[e] = data[smallest]
        data[smallest] = temp
    print("Sorted with Selection Sort in ", time.perf_counter() - last, "seconds.")
    EndSort()
    return

def insertionSort(data):
    last = time.perf_counter()
    for e in range(1, len(data)):
        index = data[e]
        j = e
        while j > 0 and data[j-1] > index:
            data[j] = data[j-1]
            j -= 1

            queue.put(lambda: DrawList(data, j))
            time.sleep(ANIMATION_DELAY / 1000)
        data[j] = index
    print("Sorted with Insertion Sort in ", time.perf_counter() - last, "seconds.")
    EndSort()
    return

def DrawList(data, current_selection):
    width = w / len(data)
    height = 0
    x, y = 0, h
    for e in range(0, len(data)):
        if not COLOUR_MODE: colour = "red"
        else:
            depth = 256 - floor((256 / h) * data[e])
            (r, g, b) = colorsys.hsv_to_rgb(float(depth) / 256, 1.0, 1.0)
            R, G, B = int(255 * r), int(255 * g), int(255 * b)
            colour = '#%02x%02x%02x' % (R, G, B)
        if e == current_selection: colour = "white"
        if not DISPLAY_MODE_DOTS:
            canvas.create_rectangle(x, y , x + width, y - data[e], fill=colour)
        else:
            canvas.create_oval(x, y - data[e], x + width, y - data[e] + width, fill=colour)
        x += width

def Cleanup():
    window.quit()
    os._exit(0)

def BeginSort(sort):
    global sorting, lst, queue
    with queue.mutex: queue.queue.clear()
    if (not sorting):
        if (sort == "BUBBLE"):
            _thread.start_new_thread(bubbleSort, (lst, ))
        if (sort == "MERGE"):
            _thread.start_new_thread(mergeSort, (lst, ))
        if (sort == "SELECTION"):
            _thread.start_new_thread(selectionSort, (lst, ))
        if (sort == "INSERTION"):
            _thread.start_new_thread(insertionSort, (lst, ))
        sorting = True

def EndSort():
    global finished
    finished = True

def ToggleColourMode():
    global COLOUR_MODE
    if (COLOUR_MODE == True):
        COLOUR_MODE = False
    else:
        COLOUR_MODE = True

def ToggleDotMode():
    global DISPLAY_MODE_DOTS
    if (DISPLAY_MODE_DOTS == True):
        DISPLAY_MODE_DOTS = False
    else:
        DISPLAY_MODE_DOTS = True

def ResetList(value):
    global lst, sorting
    if (not sorting):
        lst = random.sample(range(0, h - 10), int(value))

def UpdateDelay(value):
    global ANIMATION_DELAY
    ANIMATION_DELAY = int(value)

window = tkinter.Tk()
window.protocol("WM_DELETE_WINDOW", Cleanup)
window.title("Sorting Algorithms Visualised")
queue = queue.Queue()
lst = random.sample(range(0, h - 10), minElements)
sorting = False
finished = False

toolbar = tkinter.Frame(window)

ColourMode = tkinter.Button(toolbar, text="Toggle Colour Mode", command = ToggleColourMode)
ColourMode.pack(side="right")

DotMode = tkinter.Button(toolbar, text="Toggle Dot Mode", command = ToggleDotMode)
DotMode.pack(side="right")

toolbar.pack(side="top", fill="x")

canvas = tkinter.Canvas(window, bg="black", height=h, width=w)
canvas.pack()

BubbleSort = tkinter.Button(window, text="Bubble Sort", command =  lambda: BeginSort("BUBBLE"))
BubbleSort.pack(side="left")

MergeSort = tkinter.Button(window, text="Merge Sort", command = lambda: BeginSort("MERGE"))
MergeSort.pack(side="left")

SelectionSort = tkinter.Button(window, text="Selection Sort", command = lambda: BeginSort("SELECTION"))
SelectionSort.pack(side="left")

InsertionSort = tkinter.Button(window, text="Insertion Sort", command = lambda: BeginSort("INSERTION"))
InsertionSort.pack(side="left")

toolbar2 = tkinter.Frame(window)

ElementSlider = tkinter.Scale(toolbar2, from_=minElements, to=maxElements, orient="horizontal", length=250, command = ResetList)
ElementSlider.pack(side="right")

Label1 = tkinter.Label(toolbar2, text="Element Count:")
Label1.pack(side="right")

DelaySlider = tkinter.Scale(toolbar2, from_=1, to=1000, orient="horizontal", length=250, command = UpdateDelay)
DelaySlider.pack(side="right")

Label2 = tkinter.Label(toolbar2, text="Animation Delay (ms):")
Label2.pack(side="right")

toolbar2.pack(side="bottom", fill="x")

while True:
    window.update()
    window.update_idletasks()
    canvas.delete("all")
    if (finished):
        finished = False
        sorting = False
        ResetList(ElementSlider.get())
    if (sorting):
        function = queue.get()
        function()
    else:
        DrawList(lst, 0)
