import tkMessageBox

import tkinter
from PIL import Image, ImageTk

from signaturerecognition.GUI import GUI


class Login:

    background_color = '#66c4ff'

    def __init__(self):
        self.root = tkinter.Tk()
        self.root.title("Signature Verification")
        self.root.minsize(400, 200)
        self.root.configure(bg=self.background_color)

        self.mainframe = tkinter.Frame(self.root, bg=self.background_color)
        self.mainframe.grid(column=0, row=0, sticky=(tkinter.N, tkinter.W, tkinter.E, tkinter.S), padx=20, pady=20)
        self.mainframe.columnconfigure(0, weight=1)
        self.mainframe.rowconfigure(0, weight=1)

        self.labelTitle = tkinter.Label(self.mainframe, text="Login", bg=self.background_color, fg='white')

        self.entryUsername = tkinter.Entry(self.mainframe)
        self.entryPassword = tkinter.Entry(self.mainframe, show='*')
        self.button = tkinter.Button(self.mainframe, text='Login', command=self.login_click)

        self.labelTitle.config(font=("Courier", 38))

        self.labelTitle.grid(column=1, row=1, sticky=(tkinter.W, tkinter.E))
        self.entryUsername.grid(column=1, row=2, sticky=(tkinter.W, tkinter.E))
        self.entryPassword.grid(column=1, row=3, sticky=(tkinter.W, tkinter.E))
        self.button.grid(column=2, row=3, sticky=(tkinter.W, tkinter.E), padx=(40, 10))

        # im = Image.open('/Users/libin/Documents/Libin/TKinter/transparent-5.png')
        # tkimage = ImageTk.PhotoImage(im)
        # background_label = tkinter.Label(self.mainframe, image=tkimage)
        # background_label.place(x=0, y=0, relwidth=1, relheight=1)

    def login_click(self):
        username = self.entryUsername.get()
        password = self.entryPassword.get()

        if username == 'admin' and password == '123456789':
            tkMessageBox.showinfo("Authentication Success", "Welcome")
            # self.root.withdraw()
            gui = GUI()
            gui.show()
        else:
            tkMessageBox.showerror("Authentication Failed", "Username or password wrong")

    def show(self):
        self.root.mainloop()

if __name__ == "__main__":
    login = Login()
    login.show()
