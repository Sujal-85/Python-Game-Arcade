from tkinter import *
import random
import mysql.connector
from subprocess import call
from tkinter import messagebox
class change_pass:

    # constructor
    def __init__(self , root2, username_lg=""):

        # -----------------------------------------------------------------------------------------------
        # -----------------------------------------------------------------------------------------------

        self.root1 = root2
        self.root1.title('OTP Page')
        self.root1.geometry('1520x780+0+0')
        self.root1.configure(bg="white")
        self.root1.resizable(False, False)

        self.frame1 = (Frame(self.root1, width=500, height=250, bg="white"))
        self.frame1.place(x=0,y=130)
        self.img = PhotoImage(file='images/forget password.png')
        Label(self.root1, image=self.img, bg='white').place(x=200, y=200)

        self.img1 = PhotoImage(file='images/logo.png')
        self.l = Label(self.root1, image=self.img1, bg='white')
        self.l.place(x=10, y=12)

        self.frame2 = (Frame(self.root1, width=550, height=700, bg="white"))
        self.frame2.place(x=800,y=70)

        self.label1 = Label(self.frame2, text=" Password strength: ", fg='Red', bg='white', font=('Century', 14))
        self.label1.place(x=0, y=20)
        self.label1 = Label(self.frame2, text="Use at least 8 characters. Don’t use a password from\n"       
                                    "another site, or something too obvious like your \n"
                                    "pet’s name "
                                    , fg='Red', bg='white', font=('Century', 12))
        self.label1.place(x=0, y=50)

        # ------------------------------------------------------------------------------------------------------------------
        def on_enter(e):
            self.password.delete(0, 'end')


        def on_leave(e):
            self.name = self.password.get()
            if self.name == '':
                self.password.insert(0, 'Password')


        # label1 = Label(frame2, text=" New Password  ", fg='Red', bg='white', font=('Microsoft YaHei UI Light', 20))
        # label1.place(x=10, y=50)
        self.password = Entry(self.frame2, width=30, fg='black', bg='white',font=('Modern No. 20', 19,'bold'))
        self.password.place(x=10, y=230)
        self.password.insert(0, 'New password',)
        self.password.bind('<FocusIn>', on_enter)
        self.password.bind('<FocusOut>', on_leave)

        Frame(self.frame2, width=365, height=2, bg='black').place(x=10, y=270)


        # ------------------------------------------------------------------------------------------------------------------
        # def on_enter(e):
        #     self.user.delete(0, 'end')
        #
        # def on_leave(e):
        #     self.name = self.user.get()
        #     if self.name == '':
        #         self.user.insert(0, 'Enter Username')


        # label1 = Label(frame2, text=" New Password  ", fg='Red', bg='white', font=('Microsoft YaHei UI Light', 20))
        # label1.place(x=10, y=50)
        self.user = Entry(self.frame2, width=30, fg='red', bg='white',font=('Modern No. 20', 19,'bold'))
        self.user.place(x=10, y=150)
        self.user.insert(0, username_lg)
        # self.user.bind('<FocusIn>', on_enter)
        # self.user.bind('<FocusOut>', on_leave)

        Frame(self.frame2, width=365, height=2, bg='black').place(x=10, y=190)

        # ---------------------------------------------------------------------------------------------------------
        def on_enter(e):
            self.password1.delete(0, 'end')
        def on_leave(e):
            self.name = self.password1.get()
            if self.name == '':
                self.password1.insert(0, 'Confirm password')


        # label2 = Label(frame2, text=" Confirm Password  ", fg='Red', bg='white', font=('Microsoft YaHei UI Light', 20, 'bold'))
        # label2.place(x=10, y=200)
        self.password1 = Entry(self.frame2, width=30, fg='black',bg='white', font=('Modern No. 20',19,'bold'))
        self.password1.place(x=10, y=300)
        self.password1.insert(0, 'Confirm Password')
        self.password1.bind('<FocusIn>', on_enter)
        self.password1.bind('<FocusOut>', on_leave)

        Frame(self.frame2, width=365, height=2, bg='black').place(x=10, y=340)
        # ------------------------------------------------------------------------------------------------------------------

        def password_generate():

            self.list_alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
            self.list_number = '0123456789'
            self.list_lower_alpha = 'abcdefghijklmnopqrstuvwxyz'

            upper, lower, num = True, True, True

            self.All = ''

            if upper:
                self.All += self.list_alphabet

            if lower:
                self.All += self.list_lower_alpha

            if num:
                self.All += self.list_number

            length = 8

            for x in range(1):
                self.generate_password = ''.join(random.sample(All, length))
                self.password2.delete(0, 'end')
                self.password2.insert(0, self.generate_password)


        self.password2 = Entry(self.frame2, width=24, fg='black',bg='white', font=('Century',19,'bold'))
        self.password2.place(x=10, y=380)

        Frame(self.frame2, width=365, height=2, bg='red').place(x=10, y=415)
        # ------------------------------------------------------------------------------------------------------------------

        def change_password(a, b, c):
            conn = mysql.connector.connect(host='localhost', password='Suj@y935974', user='root', database='game')
            Cursor_obj = conn.cursor()
            query = "update create_account SET pass=%s , confirmpass=%s where username =%s"
            val = (b, c, a)
            Cursor_obj.execute('select * from create_account')
            my_result = Cursor_obj.fetchall()
            for i in my_result:
                if a in i:
                    Cursor_obj.execute(query, val)
                    messagebox.showinfo('success', "Password is Change successfully!!")
                    conn.commit ( )
                    conn.close ( )
                    self.root1.destroy()
                    call(['python' , 'login.py'] )
                    break

            else:
                messagebox.askretrycancel("Invalid", "Username doesn't match")


        def update_password():
            if str(self.user.get()) == '' or str(self.user.get()) == 'Enter Username':
                messagebox.showwarning("Invalid", "Empty Field is not Allowed !")

            elif str(self.password.get()) == '' or str(self.password.get()) =='New password':
                messagebox.showwarning("Invalid", "Empty Field is not Allowed !")

            elif len(str(self.password.get())) < 8:
                messagebox.showwarning("Invalid", "Password of minimum 8 characters!!")


            elif str(self.password.get()) != str(self.password1.get()):
                messagebox.showwarning("Invalid", "Please check Confirm Password!")

            else:
                self.p0 = str(self.user.get())
                self.p1 = str(self.password.get())
                self.p2 = str(self.password1.get())
                change_password(self.p0,self.p1,self.p2)


        # ------------------------------------------------------------------------------------------------------------------
        self.button1 = Button(self.frame2, fg='white', bg='blue', width=25,height=2, text='Change password', pady=2, border=0, font=('bold', 11),
                         cursor= 'hand2', command=update_password)
        self.button1.place(x=70, y=520)

        self.button2 = Button(self.frame2, width=15, text='Suggest password', bg='black',font=('Arial Black', 10,), border=0,
                         cursor='hand2', fg='White', command=password_generate)
        self.button2.place(x=250, y=450)


if __name__=='__main__':
    root2 = Tk ( )
    for f in root2.winfo_children ( ):
        f.destroy ( )
    obj = change_pass( root2, username_lg="")
    root2.mainloop()

