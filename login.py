from tkinter import *
import mysql.connector
from tkinter import messagebox
import pyttsx3
from subprocess import call
import customtkinter
from shooter_game import *
import matplotlib
# import forgot_password_for_verify
from mainGui import *

class LogInPage:
    def __init__(self ,root, username_lg = ""):
        self.root = root
        self.root.title('Login Page')
        self.root.geometry('1540x900+-7+-30')
        self.root.configure(bg="white")
        self.root.resizable(False, False)
        user = username_lg
        #root.attributes('-alpha', 0.9)
        # B=rgba(0,0,0,100)Frame(frame, width=200, height=3, bg='blue', highlightbackground='blue').place(x=160, y=145)
        self.img = PhotoImage(file='images/bg.png')
        Label(root, image=self.img, bg='white').place(x=0, y=0)
        self.frame = Frame(self.root, width=530, height=580, bg='#121212')

        self.frame.place(x=489, y=160)
        self.heading = Label(self.frame, text='User Login', fg='Blue',bg='#121212', font=('copper black', 28, 'bold'))
        self.heading.place(x=160, y=100)
        self.img1 = PhotoImage(file='images/gamehouse2.png')

        self.l = Label(self.frame, text = "Home",fg= 'white', bg='#121212',  font =('Century', 9,'bold'))
        self.l.place(x=16,y=80)

        def on_enter(e):
            self.user.delete(0, 'end')

        def on_leave(e):
            name = self.user.get()
            if name == '':
                self.user.insert(0, 'Username')

        self.user = Entry(self.frame, width=25, fg='black', font=('Microsoft YaHei UI Light', 14, 'bold'))
        self.user.place(x=110, y=210)
        self.user.insert(0, 'Username')
        self.user.bind('<FocusIn>', on_enter)
        self.user.bind('<FocusOut>', on_leave)

        Frame(self.frame, width=295, height=2, bg='#121212').place(x=110, y=235)

        # -------------------------------------------------------------------------------------------
        def on_enter(e):
            self.user1.delete(0, 'end')
        def on_leave(e):
            name = self.user1.get()
            if name == '':
                self.user1.insert(0, 'Password')

        self.user1 = Entry(self.frame, width=25, fg='black', bg='white', font=('Microsoft YaHei UI Light', 14, 'bold'))
        self.user1.place(x=110, y=295)
        self.user1.insert(0, 'Password')
        self.user1.bind('<FocusIn>', on_enter)
        self.user1.bind('<FocusOut>', on_leave)

        Frame(self.frame, width=295, height=2, bg='#121212').place(x=110, y=320)

        # -----------------------------------------------------------------------------------------------
        def home():
            import mainGui
            username_lg2 = self.user.get ( )
            if username_lg2 == "Username":
                self.root.destroy ( )
                self.root = Tk ( )
                self.obj = mainGui.Game ( self.root , username_lg = user )
            # calling strore window and calling Store class in main.py
            else:
                # username_lg1 = self.user1.get()
                self.root.destroy()
                self.root = Tk ( )
                self.obj = mainGui.Game ( self.root , username_lg2 )

        # -----------------------------------------------------------------------------------------------
        def db_login(a,b):
            self.conn = mysql.connector.connect(host='localhost', password='Suj@y935974', user='root', database='game')
            Cursor_obj1 = self.conn.cursor()
            query1 = "select * from create_account where username=%s and pass=%s"
            val1 = (a, b)
            Cursor_obj1.execute(query1, val1)
            row = Cursor_obj1.fetchone()

            if row is None:
                messagebox.askretrycancel('Invalid', 'Error! Username or password not correct.')

            else:
                messagebox.showinfo('Welcome To Game Zone!', "Account is Login Successfully.")
                self.root1 = pyttsx3.init()
                self.root1.setProperty('volume', 10)
                self.root1.setProperty('rate', 160)
                voice = self.root1.getProperty('voices')
                self.root1.setProperty('voice', voice[1].id)
                self.root1.say('Welcome to the gaming dimension!')
                self.root1.runAndWait()
                # sample.usern(a)


                import mainGui
                username_lg = self.user.get ( )
                self.root.destroy()
                # calling strore window and calling Store class in main.py
                self. root1 = Tk ( )

                self.obj = mainGui.Game( self.root1 , username_lg=f"{username_lg}")

        # conn.close()


        # -------------------------------------------------------------------------------------------
        def login( ):
            global a
            a = self.user.get()
            b = self.user1.get()
            self.conn = mysql.connector.connect ( host = 'localhost' , password = 'Suj@y935974' , user = 'root' ,
                                                  database = 'game' )
            Cursor_obj1 = self.conn.cursor ( )
            Cursor_obj1.execute( f"select pass from create_account where username='{a}'",())

            row = Cursor_obj1.fetchone ( )
            self.password1 = row[0]
            self.conn.close()

            if str(a) == "Username":
                 messagebox.askretrycancel("Invalid", "All Fields are Required!!")

            elif str(b) == 'Password':
                 messagebox.askretrycancel("Invalid", "All Fields are Required!!")

            elif self.password1 != b:
                messagebox.askretrycancel ( "Invalid" , "Password is not correct!" )

            else:
                print(db_login(a,b))


        # ------------------------------------------------------------------------------------------------
        def newAcc():
          self.root.destroy()
          call(['python', 'createAccount.py'])
        def forgot_password():
            if self.user.get() == "" or self.user.get() == "Username":
                messagebox.showwarning("Invalid","Please Enter Username !")
            else:
                import forgot_password_for_verify
                self.root.destroy ( )
                self.root1 = Tk ( )
                self.obj = forgot_password_for_verify.Forgot_Password ( self.root1 , username_lg = f"{username_lg}" )
        # ------------------------------------------------------------------------------------------------

        self.button1 = Button(self.frame, fg='white', bg='blue', width=36, text='Login', pady=7, border=0, font=('bold', 11), cursor='hand1', command=login)
        self.button1.place(x=100, y=400)
        self.label = Label(self.frame, text="Don't have an Account?", fg='red', bg='#121212', font=('Microsoft YaHei UI Light', 12, 'bold'))
        self.label.place(x=80, y=460)
        self.button2 = Button(self.frame, width=15, text='Create an Account', bg='#121212', font=('Arial Black', 10,), border=0, cursor='hand2', fg='White', command=newAcc)
        self.button2.place(x=300, y=459)
        self.button3 = Button(self.frame, width=15, text='Forgot Password ?', bg='#121212', font=('Century', 12,), border=0, cursor='hand2', fg='White', command=forgot_password)
        self.button3.place(x=300, y=350)
        self.b = Button ( self.frame , width = 50 , height = 50 , bg = '#121212' , border = 0 , image = self.img1 ,
                          command = home )
        self.b.place ( x = 10 , y = 30 )


if __name__ == "__main__" :
    root = Tk()
    obj = LogInPage(root, username_lg = "")
    root.mainloop()

# -------------------------------------------------------------------------------------------------