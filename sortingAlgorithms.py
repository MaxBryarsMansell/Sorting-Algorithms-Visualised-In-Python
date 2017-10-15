#Written By Max Bryars-Mansell

import random, tkinter, os, colorsys, time, threading, queue
from math import floor
from copy import copy

# Properties
w = 1280
h = 720
minElements = 150
maxElements = 200
animation_delay = 1 #in ms
COLOUR_MODE = True
DISPLAY_MODE_DOTS = True

def bubbleSort(data):
    for e in range(len(data) - 1, 0, -1):
        for i in range(1, len(data)):
            if data[i - 1] > data[i]:
                data[i], data[i - 1] = data[i - 1], data[i]
                    
                queue.put(lambda: DrawList(data, i))
                queue.put(lambda: canvas.update())
                queue.put(lambda: canvas.delete("all"))
                time.sleep(animation_delay / 1000)
    print("Sorted with Bubble Sort")
     

def selectionSort(data):
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
        
        
    print("Sorted with Selection Sort")

def insertionSort(data):
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
    print("Sorted with Insertion Sort")

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
    os._exit(0)
    
window = tkinter.Tk()
window.protocol("WM_DELETE_WINDOW", Cleanup)
window.title("Sorting Algorithms Visualised")

canvas = tkinter.Canvas(window, bg="black", height=h, width=w)
canvas.pack()

queue = queue.Queue()

thread = threading.Thread(target = Main, args = ())
thread.start()

while True:
    function = queue.get()
    function()








