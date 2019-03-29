#Written By Max Bryars-Mansell

import random, tkinter, os, colorsys, time, _thread, queue
from math import floor
from copy import copy
from enum import Enum
from tkinter import messagebox

# Properties
w = 1280
h = 720
minElements = 10
maxElements = 1000
ANIMATION_DELAY = 1 #in ms
COLOUR_MODE = False
DISPLAY_MODE_DOTS = False

def is_sorted(data):
    for i in range(len(data) - 1):
        if data[i] > data[i + 1]:
            return False
    return True
                
def bogoSort(data):
    global queue
    last = time.perf_counter()
    while not is_sorted(data):
        random.shuffle(data)
        queue.put(lambda: DrawList(data))
        time.sleep(ANIMATION_DELAY / 1000) 
        if not sorting:  print("Ending sort..."); return
    print("Sorted with Bogo Sort in ", time.perf_counter() - last, "seconds.")

    with queue.mutex: queue.queue.clear()
    queue.put(lambda: EndSort())
    return

def bubbleSort(data):
    global queue
    last = time.perf_counter()
    for e in range(len(data) - 1, 0, -1):
        for i in range(1, len(data)):
            if data[i - 1] > data[i]:
                data[i], data[i - 1] = data[i - 1], data[i]
                queue.put(lambda: DrawList(data, e, i))
                time.sleep(ANIMATION_DELAY / 1000)
                if not sorting:  print("Ending sort..."); return
    print("Sorted with Bubble Sort in", time.perf_counter() - last, "seconds.")

    with queue.mutex: queue.queue.clear()
    queue.put(lambda: EndSort())
    return

# This function is same in both iterative and recursive 
def partition(arr,l,h):
    global queue
    i = ( l - 1 ) 
    x = arr[h] 
  
    for j in range(l , h): 
        if   arr[j] <= x: 
  
            # increment index of smaller element 
            i = i+1
            arr[i],arr[j] = arr[j],arr[i]
            queue.put(lambda: DrawList(arr, i, j))
            
    arr[i+1],arr[h] = arr[h],arr[i+1]
    
    queue.put(lambda: DrawList(arr, i, j))
    time.sleep(ANIMATION_DELAY / 1000)
    
    return (i+1) 

def quickSort(arr):
    global queue
    last = time.perf_counter()

    h = len(arr) - 1
    l = 0

    # Create an auxiliary stack 
    size = h - l + 1
    stack = [0] * (size) 
  
    # initialize top of stack 
    top = -1
  
    # push initial values of l and h to stack 
    top = top + 1
    stack[top] = l 
    top = top + 1
    stack[top] = h 
  
    # Keep popping from stack while is not empty 
    while top >= 0:

        if not sorting:  print("Ending sort..."); return
  
        # Pop h and l 
        h = stack[top] 
        top = top - 1
        l = stack[top] 
        top = top - 1
  
        # Set pivot element at its correct position in 
        # sorted array 
        p = partition( arr, l, h )
  
        # If there are elements on left side of pivot, 
        # then push left side to stack 
        if p-1 > l: 
            top = top + 1
            stack[top] = l 
            top = top + 1
            stack[top] = p - 1
  
        # If there are elements on right side of pivot, 
        # then push right side to stack 
        if p+1 < h: 
            top = top + 1
            stack[top] = p + 1
            top = top + 1
            stack[top] = h 
         
    print("Sorted with Quick Sort in", time.perf_counter() - last, "seconds.")

    with queue.mutex: queue.queue.clear()
    queue.put(lambda: EndSort())
    return

def mergeSort(data):
    global queue
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

                queue.put(lambda: DrawList(data, i, k))
                time.sleep(ANIMATION_DELAY / 1000)
                if not sorting:  print("Ending sort..."); return
            i = i + 2 * step
        step = step * 2
    print("Sorted with Merge Sort in ", time.perf_counter() - last, "seconds.")
    
    with queue.mutex: queue.queue.clear()
    queue.put(lambda: EndSort())
    return

def selectionSort(data):
    global queue
    last = time.perf_counter()
    for e in range(len(data)):
        smallest = e
        for j in range(e + 1, len(data)):
            if data[j] < data[smallest]: smallest = j;

            queue.put(lambda: DrawList(data, e, j))
            time.sleep(ANIMATION_DELAY / 1000)
            if not sorting:  print("Ending sort..."); return
        temp = data[e]
        data[e] = data[smallest]
        data[smallest] = temp
    print("Sorted with Selection Sort in ", time.perf_counter() - last, "seconds.")

    with queue.mutex: queue.queue.clear()
    queue.put(lambda: EndSort())
    return

def insertionSort(data):
    global queue
    last = time.perf_counter()
    for e in range(1, len(data)):
        index = data[e]
        j = e
        while j > 0 and data[j-1] > index:
            data[j] = data[j-1]
            j -= 1

            queue.put(lambda: DrawList(data, e, j))
            time.sleep(ANIMATION_DELAY / 1000)
            if not sorting:  print("Ending sort..."); return
        data[j] = index
    print("Sorted with Insertion Sort in ", time.perf_counter() - last, "seconds.")
    
    with queue.mutex: queue.queue.clear()
    queue.put(lambda: EndSort())
    return

def DrawList(data, current_selection_1 = -1, current_selection_2 = -1):
    width = w / len(data)
    height = 0
    x, y = 0, h
    
    selection_colour = "blue"
        
    for e in range(0, len(data)):
        if not COLOUR_MODE: colour = "red"
        else:
            depth = 256 - floor((256 / h) * data[e])
            (r, g, b) = colorsys.hsv_to_rgb(float(depth) / 256, 1.0, 1.0)
            R, G, B = int(255 * r), int(255 * g), int(255 * b)
            colour = '#%02x%02x%02x' % (R, G, B)
        if e == current_selection_1 or e == current_selection_2: colour = selection_colour
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
        if (sort == "QUICK"):
            _thread.start_new_thread(quickSort, (lst, ))
        if (sort == "BOGO"):
            _thread.start_new_thread(bogoSort, (lst, ))
        sorting = True
        

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

def EndSort():
    global sorting, queue
    with queue.mutex: queue.queue.clear()
    sorting = False
    ResetList(ElementSlider.get())
    print("Ending sort...")
    messagebox.showinfo(title="Greetings", message="Sort ended!")


def ResetList(value):
    global lst
    if (not sorting):
        lst = random.sample(range(0,h), int(value))

def UpdateDelay(value):
    global ANIMATION_DELAY
    ANIMATION_DELAY = int(value)

window = tkinter.Tk()
window.protocol("WM_DELETE_WINDOW", Cleanup)
window.title("Sorting Algorithms Visualised")
queue = queue.Queue()
lst = random.sample(range(0, h - 10), minElements)
sorting = False

toolbar = tkinter.Frame(window)

ColourMode = tkinter.Button(toolbar, text="End Sort", command = EndSort)
ColourMode.pack(side="left")

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

QuickSort = tkinter.Button(window, text="Quick Sort", command = lambda: BeginSort("QUICK"))
QuickSort.pack(side="left")

BogoSort = tkinter.Button(window, text="Bogo Sort", command = lambda: BeginSort("BOGO"))
BogoSort.pack(side="left")

toolbar2 = tkinter.Frame(window)

ElementSlider = tkinter.Scale(toolbar2, from_=minElements, to=maxElements, orient="horizontal", length=250, command = ResetList)
ElementSlider.set(100)
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
    if (sorting):
        function = queue.get()
        function()
    else:
        DrawList(lst)
