from tkinter import *
import tkinter as tk
import numpy as n
from keras.models import load_model
from PIL import ImageGrab, Image
import win32gui

model = load_model('model.h5')

class main():

    def __init__(self, root):
        self.root = root

        # Buttons
        self.canvas = tk.Canvas(root, width = 270, height = 235, bg = "grey", cursor = "cross") #canvas for drawing
        self.label = tk.Label(root, height = 5, width = 11, text = "Results" , font = ("Times New Roman", 30), bg = "light blue") #canvas for label
        self.clear_button = tk.Button(root, bg = 'white', width = 10, height = 2, text = "Clear", command = self.clear) #clear button
        self.predict_button = tk.Button(root, bg = 'white', width = 10, height = 2, text = "Run", command =  self.classify) #predict button
        self.canvas.grid(row = 0, column = 0, pady = 2, sticky = 'n')
        self.label.grid(row = 0, column = 1,pady = 2, padx = 2)
        self.clear_button.grid(row = 1, column = 0, pady = 2)
        self.predict_button.grid(row = 1, column = 1, pady = 4, padx = 4)
        self.canvas.bind("<B1-Motion>", self.draw_digits)

    #to draw the digit
    def draw_digits(self, event):
        font_size = 5 #font size
        self.canvas.create_oval(event.x - font_size, event.y - font_size, event.x + font_size, event.y + font_size, fill = 'black')

    #classifys the user input
    def classify(self):
        HWND = self.canvas.winfo_id() # window handle of canvas
        rectangle = win32gui.GetWindowRect(HWND) #coordinates
        a,b,c,d = rectangle
        rectangle = (a + 4, b + 4, c + 100, d + 100)
        im = ImageGrab.grab(rectangle) #takes the snapshot of the rect
        im.save('img.png') #see the digit before resize
        digit, accuracy = prediction(im) #prediction 
        percentage = str(int(accuracy * 100))
        self.label.configure(text= 'Digit: '+ str(digit) + '\n '+ 'Match: ' + percentage + '%') #outputs the results 
    
    #clear the data from the screen
    def clear(self):
        self.canvas.delete("all")

#Predicts the correct digit
def prediction(img):
    img = img.resize((28, 28)) #resize the image to 28x28 
    img.save('resized.png') #resized image -> see and compare to the img.png
    img = img.convert('L') #img in greyscale
    img = n.array(img)  #convert to numpy array
    img = img.reshape(1, 28, 28, 1)
    img = img/255.0 #range between 0 to 1
    result = model.predict([img])[0] #predict 
    result_index = n.argmax(result)
    maximum_result = max(result)
    return result_index, maximum_result

if __name__ == '__main__':
    root = tk.Tk()
    root.geometry("530x300")
    gui = main(root)
    busted_display = Label(root, text= "Welcome" + '\n' + "to" + '\n' + "Handwritten Digit Recognition", font=("Times New Roman", "25"), fg='#000000', bg = '#ffffff')
    busted_display.place(x = 70, y=70)
    root.after(2000, busted_display.destroy)
    root.mainloop()