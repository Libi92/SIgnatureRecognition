import os
import tkFileDialog
import tkMessageBox
from tkMessageBox import showerror

import tkinter
from PIL import ImageTk, Image

from signaturerecognition import SignatureRecogition, classify


def selectMenu():
    print("Dataset")


def load_file():
    del images[:]
    path = tkFileDialog.askdirectory()
    row = 2
    col = 1
    if path:
        try:
            print(path)
            classify.pre_build(path)
            for (dirpath, dirnames, filenames) in os.walk(path):
                print filenames
                for file_name in filenames:
                    if file_name != '.DS_Store':
                        if col == 8:
                            row += 1
                            col = 1
                        file = os.path.join(dirpath, file_name)
                        images.append(file)
                        img = Image.open(file)
                        imgResize = img.resize((100, 100))

                        img = ImageTk.PhotoImage(imgResize)
                        panel = tkinter.Label(mainframe, image=img)
                        panel.configure(image=img)
                        panel.image = img
                        panel.grid(row=row, column=col, sticky=(tkinter.W, tkinter.E))
                        col += 1

        except:
            showerror("Open Source File", "Failed to read file\n'%s'" % path)
    return


def startTraining():
    SignatureRecogition.startApplication(images)
    tkMessageBox.showinfo("Training", "System training completed successfully")


def load_test_file():
    file = tkFileDialog.askopenfile()
    print(file.name)
    result = classify.test_image(file.name)
    result = sorted(result)
    if result and result[0] < 0.006:
        tkMessageBox.showinfo("Result", "Signature is true")
    else:
        print ("Forged sign")
        tkMessageBox.showinfo("Result", "Signature is forged")


def startTesting():
    load_test_file()


images = []

root = tkinter.Tk()
root.title("Signature Verification")
root.minsize(800, 500)

# win = tkinter.Toplevel(root)
menubar = tkinter.Menu(root)

menu_options = tkinter.Menu(menubar)
menu_select_file = tkinter.Menu(menu_options)
menu_options.add_command(label="Select Dataset", command=load_file)
menubar.add_cascade(menu=menu_options, label='Options')

root['menu'] = menubar

mainframe = tkinter.Frame(root)
mainframe.grid(column=0, row=0, sticky=(tkinter.N, tkinter.W, tkinter.E, tkinter.S))
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)

button = tkinter.Button(mainframe, text='Train Dataset', command=startTraining)
button2 = tkinter.Button(mainframe, text='Test Signature', command=startTesting)
button.grid(column=1, row=1, sticky=(tkinter.W, tkinter.E))
button2.grid(column=2, row=1, sticky=(tkinter.W, tkinter.E))

root.mainloop()

