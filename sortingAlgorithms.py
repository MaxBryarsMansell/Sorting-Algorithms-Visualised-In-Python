#Written By Max Bryars-Mansell

import random, tkinter, os, colorsys, time, threading, queue
from math import floor
from copy import copy

# Properties
w = 1280
h = 720
minElements = 100
maxElements = 150
animation_delay = 5 #in ms

def bubbleSort(data):
    swapped = None
    while True:
        swapped = False
        for e in range(len(data)):
            if (e) < len(data) - 1:
                if data[e] > data[e + 1]:
                    data[e], data[e + 1] = data[e + 1], data[e]
                    swapped = True
                    
                    queue.put(lambda: DrawList(data))
                    queue.put(lambda: canvas.update())
                    queue.put(lambda: canvas.delete("all"))
                    time.sleep(animation_delay / 1000)
        if not swapped:
            print("Sorted with Bubble Sort")
            break

def selectionSort(data):
    for e in range(len(data)):
        smallest = e
        for j in range(e + 1, len(data)):
            if data[j] < data[smallest]: smallest = j;
        temp = data[e]
        data[e] = data[smallest]
        data[smallest] = temp
        
        queue.put(lambda: DrawList(data))
        queue.put(lambda: canvas.update())
        queue.put(lambda: canvas.delete("all"))
        time.sleep(animation_delay / 1000)
    print("Sorted with Selection Sort")

def insertionSort(data):
    for i in range(1, len(data)):
        index = data[i]
        j = i
        while j > 0 and data[j-1] > index:
            data[j] = data[j-1]
            j -= 1
        data[j] = index

        queue.put(lambda: DrawList(data))
        queue.put(lambda: canvas.update())
        queue.put(lambda: canvas.delete("all"))
        time.sleep(animation_delay / 1000)
    print("Sorted with Insertion Sort")

def DrawList(data):
    width = w / len(data)
    height = 0
    x, y = 0, h
    for e in data:
        depth = 256 - floor((256 / h) * e)
        (r, g, b) = colorsys.hsv_to_rgb(float(depth) / 256, 1.0, 1.0)
        R, G, B = int(255 * r), int(255 * g), int(255 * b)
        colour = '#%02x%02x%02x' % (R, G, B)
        canvas.create_rectangle(x, y , x + width, y - e, fill=colour)
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








