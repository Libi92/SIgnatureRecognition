import os
import tkFileDialog
import tkMessageBox
from tkMessageBox import showerror

import tkinter
from PIL import ImageTk, Image

from signaturerecognition import SignatureRecogition, classify


class GUI:
    width = 800
    height = 700
    background_color = '#66c4ff'

    def __init__(self):
        self.images = []

        self.root = tkinter.Toplevel()
        self.root.title("Signature Verification")
        self.root.minsize(self.width, self.height)
        self.root.configure(bg=self.background_color)

        self.menubar = tkinter.Menu(self.root)

        self.menu_options = tkinter.Menu(self.menubar)
        self.menu_select_file = tkinter.Menu(self.menu_options)
        self.menu_options.add_command(label="Select Dataset", command=self.load_file)
        self.menubar.add_cascade(menu=self.menu_options, label='Options')

        self.root['menu'] = self.menubar

        self.mainframe = tkinter.Frame(self.root)
        self.mainframe.grid(column=0, row=0, sticky=(tkinter.N, tkinter.W, tkinter.E, tkinter.S))
        self.mainframe.columnconfigure(0, weight=1)
        self.mainframe.rowconfigure(0, weight=1)

        self.button = tkinter.Button(self.mainframe, text='Train Dataset', command=self.startTraining)
        self.button2 = tkinter.Button(self.mainframe, text='Test Signature', command=self.startTesting)
        self.button.grid(column=1, row=1, sticky=(tkinter.W, tkinter.E))
        self.button2.grid(column=2, row=1, sticky=(tkinter.W, tkinter.E))


    def load_file(self):
        del self.images[:]
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
                            self.images.append(file)
                            img = Image.open(file)
                            imgResize = img.resize((100, 100))

                            img = ImageTk.PhotoImage(imgResize)
                            panel = tkinter.Label(self.mainframe, image=img)
                            panel.configure(image=img)
                            panel.image = img
                            panel.grid(row=row, column=col, sticky=(tkinter.W, tkinter.E))
                            col += 1

            except:
                showerror("Open Source File", "Failed to read file\n'%s'" % path)
        return

    def startTraining(self):
        SignatureRecogition.startApplication(self.images)
        tkMessageBox.showinfo("Training", "System training completed successfully")

    def load_test_file(self):
        file = tkFileDialog.askopenfile()
        print(file.name)
        result = classify.test_image(file.name)
        result = sorted(result)
        if result and result[0] < 0.001:
            tkMessageBox.showinfo("Result", "Signature is true")
        else:
            print ("Forged sign")
            tkMessageBox.showinfo("Result", "Signature is forged")

    def startTesting(self):
        self.load_test_file()

    def show(self):
        self.root.mainloop()

if __name__ == "__main__":
    gui = GUI()
    gui.show()
