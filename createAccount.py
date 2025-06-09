import time
from tkinter import *
import database
import messagebox
import random
import smtplib
import hashlib
from PIL import Image,ImageTk
import cv2
import pyttsx3
import customtkinter
from subprocess import call
import tkinter as tk
from tkinter import ttk
class SignInPage:
    def __init__(self ,root, username_lg = ""):
        self.main = root
        self.main.title('Login Page')
        self.main.geometry('1540x900+-10+-30')
        self.main.configure(bg="#666360")
        self.main.resizable(False, False)
        user = username_lg
        self.frame1 = Frame(self.main)
        self.frame1.place(x=-185, y=100)
        self.frame = (Frame(self.main, width=540, height=600, bg="#FFFADA"))
        self.frame.place(x=507, y=150)
        self.heading = Label(self.frame, text='Create Account', fg='blue', bg='white', font=('copper black', 23, 'bold'))
        self.heading.place(x=150, y=20)
        self.img1 = ImageTk.PhotoImage(Image.open("images/1bg.png"), size = (1540,760))
        self.img2 = ImageTk.PhotoImage(Image.open("images/bg10.png"),size = (1540,760))
        self.img3 = ImageTk.PhotoImage(Image.open("images/3bg.png"), size = (1540,760))
        self.img4 = ImageTk.PhotoImage(Image.open("images/4bg.png"), size = (1540,760))
        self.img5 = ImageTk.PhotoImage ( Image.open ( "images/bg9.png" ) , size = (1540 , 760) )
        self.img6 = ImageTk.PhotoImage ( Image.open ( "images/bg8.png" ) , size = (1540 , 760) )
        self.img7 = ImageTk.PhotoImage ( Image.open ( "images/bg7.png" ) , size = (1540 , 760) )

        l = Label(self.frame1, font="bold")
        l.pack()

        self.x = 1

        def move():
            global x
            if self.x == 8:
                self.x = 1
            if self.x == 1:
                l.config(image=self.img1, width = 1900, height = 750,border = 5, borderwidth = 5)

            elif self.x == 2:
                l.config(image=self.img2, width = 1900)
            elif self.x == 3:
                l.config(image=self.img3, width = 1900)
            elif self.x == 4:
                l.config(image=self.img4, width = 1900)
            elif self.x == 5:
                l.config(image=self.img5, width = 1900)
            elif self.x == 6:
                l.config(image=self.img6, width = 1900)
            elif self.x == 7:
                l.config(image=self.img7, width = 1900)

            self.x += 1
            self.main.after(3000, move)

        move()
        self.i1 = PhotoImage(file='images/logo1.png')
        self.l2 = Label(self.main, image=self.i1, bg= '#666360')
        self.l2.place(x=10, y=10)
        self.i2 = PhotoImage(file='images/back1.png')
        # l1 = Label(main, image=i2, bg= '#666360')
        # l1.place(x=140, y=20)
        self.i3 = PhotoImage(file='images/gamehouse2.png')

        Label(self.main, text = 'Exsto Gaming',bg="#666360", font = ('Artifakt Element Heavy', 40, 'bold') ).place(x=580, y=10)



        Frame(self.frame, width=225, height=3,bg='blue').place(x=155, y=55)

        self.entry = Entry(self.frame,  fg='blue', bg='#FFFADA', font=('Microsoft YaHei UI Light', 13, 'bold'), border=0)
        self.entry.place(x=50, y=160)

        # ------------------------------------------------------------------------------------------------------

        self.label = Label(self.frame, text="* Email - ", fg='Red', bg='white', font=('Microsoft YaHei UI Light', 12, 'bold'))
        self.label.place(x=40, y=120)
        self.email = Entry(self.frame, width=20, fg='black', bg='white', font=('Microsoft YaHei UI Light', 14))
        self.email.place(x=215, y=120)
        self.email.insert(0, '@gmail.com')
        # user.bind('<FocusIn>', on_enter)
        # user.bind('<FocusOut>', on_leave)

        Frame( self.frame, width=225, height=2, bg='black').place(x=215, y=145)

        # ---------------------------------------------------------------------------------------------------------

        self.label1 = Label( self.frame, text="* Username - ", fg='Red', bg='white', font=('Microsoft YaHei UI Light', 12, 'bold'))
        self.label1.place(x=40, y=210)
        self.user = Entry( self.frame, width=20, fg='black', bg='white', font=('Microsoft YaHei UI Light', 14))
        self.user.place(x=215, y=210)
        # user.insert(0, 'Password')
        # user.bind('<FocusIn>', on_enter)
        # user1.bind('<FocusOut>', on_leave)

        Frame(self.frame, width=225, height=2, bg='black').place(x=215, y=235)

        # --------------------------------------------------------------------------------------------------------

        self.label1 = Label(self.frame, text="* Mobile No. - ", fg='Red', bg='white', font=('Microsoft YaHei UI Light', 12, 'bold'))
        self.label1.place(x=40, y=260)
        self.mobile_no = Entry(self.frame, width=20, fg='black', bg='white', font=('Microsoft YaHei UI Light', 14))
        self.mobile_no.place(x=215, y=260)
        self.mobile_no.insert(0, '+91')
        # user.bind('<FocusIn>', on_enter)
        # user1.bind('<FocusOut>', on_leave)

        Frame(self.frame, width=225, height=2, bg='black').place(x=215, y=285)

        # ----------------------------------------------------------------------------------------------------------

        self.label2 = Label(self.frame, text="* Password - ", fg='Red', bg='white', font=('Microsoft YaHei UI Light', 12, 'bold'))
        self.label2.place(x=40, y=310)
        self.password = Entry(self.frame, width=20, fg='black', bg='white', font=('Microsoft YaHei UI Light', 14))
        self.password.place(x=215, y=310)

        Frame(self.frame, width=225, height=2, bg='black').place(x=215, y=335)

        # ---------------------------------------------------------------------------------------------------------

        self.label1 = Label(self.frame, text="* Confirm Password - ", fg='Red', bg='white', font=('Microsoft YaHei UI Light', 12, 'bold'))
        self.label1.place(x=40, y=360)
        self.password1 = Entry(self.frame, width=20, fg='black', bg='white', font=('Microsoft YaHei UI Light', 14))
        self.password1.place(x=230, y=360)

        Frame(self.frame, width=225, height=2, bg='black').place(x=230, y=385)

        # ---------------------------------------------------------------------------------------------------------

        self.check = IntVar()
        self.cb = Checkbutton(self.frame, variable=self.check)
        self.cb.configure(border=2)
        self.cb.place(x=75, y=430)


        def termsandpolicy():
            call(['python', 'terms and condition.py'])


        label2 = Label(self.frame, text="I accept all                          of GameZone!!- ", fg='Red', bg='white',
                       font=('Microsoft YaHei UI Light', 11, 'bold'))
        label2.place(x=120, y=430)
        but= Button(self.frame, fg='blue', bg='white', width=13, text='terms and policy', pady=0, border=0,
                    font=('Microsoft YaHei UI Light', 11, 'bold'), command = termsandpolicy)

        but.place(x=217, y=429)

        Frame(self.frame, width=130, height=1, bg='blue').place(x=220, y=455)

        #--------------------------------------------------------------------------------------------------------


        def otp():

            def generate_otp():
                global g_otp
                g_otp = ''.join(str(random.randint(100000, 999999)))
                return str(g_otp)

            # -----------------------------------------------------------------------------------------------------
            try:
                self.generate_otp1 = generate_otp()
                self.receiver = self.email.get()
                self.server = smtplib.SMTP('smtp.gmail.com', 587)
                self.server.starttls()
                self.server.login('khedekarsujay3@gmail.com', 'cbnt xifq dmaw nxrz')
                self.msg = ('Welcome to Exsto  Gaming ! \n'
                               'Use this Verification Code Below to SignIn. \n'
                               ' \n \t'+ str(self.generate_otp1)+
                               '\n\n'
                               'You Have Received this email because\n'
                               'you have requested to sign up to Exsto Gaming\n'
                               'if you did not request to sign in kindly Ignore this \n'
                               'Email.\n'
                               '- Team Exsto Gaming ' )
                self.server.sendmail('khedekarsujay3@gmail.com', self.receiver, self.msg)
                messagebox.showinfo('Success', 'OTP is Send successfully!')
                self.server.quit()

                time.sleep(3)
                self.root1 = Tk()
                self.root1.title('OTP Page')
                self.root1.geometry('500x250+500+250')
                self.root1.configure(bg="white")
                self. root1.resizable(False, False)

                self.frame1 = (Frame(self.root1, width=500, height=250, bg="white"))
                self.frame1.place(x=0, y=0)

                self.heading1 = Label(self.frame1, text='OTP Verification', fg='blue', bg='white', font=('Country', 18, 'bold'))
                self.heading1.place(x=150, y=20)
                # -----------------------------------------------------------------------------------------------------
                def otp_verify(a):
                    if a == g_otp:
                            messagebox.showinfo('Success', 'OTP Verification Successful!')
                            self.root1.destroy()
                            # entry = Entry(frame, fg='blue', bg='white',font=('Microsoft YaHei UI Light', 13, 'bold'), border=0)
                            # entry.place(x=50, y=160)
                            self.entry.insert(0, "Email is Verified !")
                    else:
                            messagebox.askretrycancel('Invalid', 'Enter Correct OTP !')

                    # --------------------------------------------------------------------------------------------------

                def verify():
                        self.Entered_otp = str(self.email1.get())
                        print(otp_verify(self.Entered_otp))

                    # --------------------------------------------------------------------------------------------------
                def otp_resend():
                    try:
                        self.generate_otp2 = generate_otp()
                        self.receiver1 = self.email.get()
                        self.server1 = smtplib.SMTP('smtp.gmail.com', 587)
                        self.server1.starttls()
                        self.server1.login('khedekarsujay3@gmail.com', 'cbnt xifq dmaw nxrz')
                        self.msg1 = ('Welcome to Exsto  Gaming ! \n'
                               'Use this Verification Code Below to SignIn. \n'
                               ' \n \t'+ str(self.generate_otp2)+
                               '\n\n'
                               'You Have Received this email because\n'
                               'you have requested to sign up to Exsto Gaming\n'
                               'if you did not request to sign in kindly Ignore this \n'
                               'Email.\n'
                               '- Team Exsto Gaming ' )
                        self.server1.sendmail('khedekarsujay3@gmail.com', self.receiver1, self.msg1)
                        messagebox.showinfo('Success', 'OTP is Send successfully!')
                        self.server1.quit()

                    except:
                        messagebox.showerror('Invalid', 'Something ! Went Wrong please Try again !')

                    # ----------------------------------------------------------------------------------------------------
                self.l = Label(self.frame1, text="Enter OTP - ", fg='Red', bg='white', font=('Microsoft YaHei UI Light', 12, 'bold'))
                self.l.place(x=60, y=100)
                self.email1 = Entry(self.frame1, width=20, fg='black', bg='white', font=('Microsoft YaHei UI Light', 14, 'bold'))
                self.email1.place(x=200, y=100)

                self.button3= Button(self.frame1, fg='white', bg='blue', width=15, text='Verify', pady=3, border=0, font=('bold', 9),
                                     cursor='hand2',command=verify)
                self.button3.place(x=80, y=190)
                self.button4 = Button(self.frame1, fg='white', bg='blue', width=15, text='Resend', pady=3, border=0, font=("Country", 9),
                                     cursor='hand2', command=otp_resend)
                self.button4.place(x=310, y=190)

                self.root1.mainloop()

            except:
                messagebox.showerror('Invalid', 'Something! Went Wrong please Try again !')


        # ---------------------------------------------------------------------------------------------------------

        def create_account():
            def validate_password(p):
                self.has_lower = False
                self.has_upper = False
                self.has_digit = False
                for characters in p:
                    if characters.islower() or characters.isupper():
                            self.has_lower = True
                            self.has_upper = True

                    if characters.isdigit():
                        self.has_digit = True
                return self.has_lower and self.has_upper and self.has_digit

            def has_symbol(pwd):
                self.symbols = "!@#$%^&*()_+={}[]:;><,?/|~"
                self.has_symbols = False
                for characters in pwd:
                    if characters in self.symbols:
                        self.has_symbols = True

                return self.has_symbols


            if str(self.entry.get()) == '':
                messagebox.showwarning("Invalid", "Email is Not Verify!!")

            elif str(self.email.get()) == "@gmail.com" or '':
                 messagebox.showwarning("Invalid", "All Fields are Required!!")

            elif( "@live.com" not in str(self.email.get()) and "@famt.ac.in" not in str(self.email.get())) and ("@gmail.com" not in str(self.email.get()) and "@yahoo.com" not in str(self.email.get())):
                 messagebox.showerror("Invalid", "Invalid email!")


            elif str(self.user.get()) == '':
                 messagebox.showwarning("Invalid", "All Fields are Required!!")

            elif has_symbol(self.password.get()) is True:
                messagebox.showerror("Invalid", "Special Symbols are not allowed! ")

            elif validate_password(self.password.get()) is False:
                messagebox.showwarning("Invalid", "Password should be combination of alphabets and digits")

            elif str(self.password.get()) == '':
                messagebox.showwarning("Invalid", "All Fields are Required!!")

            elif len(str(self.password.get())) < 8:
                messagebox.showwarning("Invalid", "Password of minimum 8 characters!!")

            elif str(self.mobile_no.get()) == '':
                messagebox.showwarning("Invalid", "All Fields are Required!!")

            elif len(str(self.mobile_no.get())) != 13:
                messagebox.showerror("Invalid", "Mobile Number is invalid!")

            elif str(self.password.get()) != str(self.password1.get()):
                messagebox.showwarning("Invalid", "Please check Confirm Password!")

            elif self.check.get() == 0:
                messagebox.showerror('Invalid', 'Error! Please accept terms and conditions!')

            else:
                a = self.email.get()
                b = self.user.get()
                c = self.mobile_no.get()
                d = self.password.get()
                # dn = hashlib.sha512( d.encode ( ) ).hexdigest ( )
                e = self.password1.get()
                # en = hashlib.sha512( e.encode ( ) ).hexdigest ( )
                # print(hashlib.sha512( en.encode ( ) ).hexdigest ( ))
                print(database.db(a, b, c, d, e))
                self.main.destroy()
                call(['python', 'login.py'])

        def login():
            self.main.destroy()
            call(['python', 'login.py'])

        def home():
            import mainGui
            self.main.destroy ( )
            self.root = Tk ( )
            self.obj = mainGui.Game ( self.root ,user )

        # -----------------------------------------------------------------------------------------------------

        self.button1 = Button(self.frame, fg='white', bg='blue', width=39, text='Create Account', pady=7, border=0, font=('bold', 9),
                    command=create_account)
        self.button1.place(x=125, y=490)
        self.button2= Button(self.frame, fg='white', bg='blue', width=10, text='Get OTP ', pady=0, border=0, font=("Country", 9),
                    command=otp)

        self.button2.place(x=350, y=170)
        self.button3 = Button(self.main, image = self.i2, bg= '#666360', border=-10, command = login,cursor = "hand2" )
        self.button3.place(x=140, y=20)

        Label(self.main, text = 'Back',bg = '#666360', font = ('Future', 12, 'bold') ).place(x=140, y=75)

        self.button3 = Button(self.frame, image = self.i3, bg= '#FFFADA', border=-10, command = home , cursor = "hand2")
        self.button3.place(x=10, y=20)
        Label(self.frame, text = 'Home',fg = 'Black',bg='#FFFADA', font = ('Future', 12, 'bold') ).place(x=15, y=75)

        Label(self.main, text = 'Login',bg = '#666360', font = ('Future', 12, 'bold') ).place(x=140, y=75)

if __name__ == "__main__" :
    root = Tk()
    obj = SignInPage(root, username_lg = "")
    root.mainloop()
# ------------------------------------------------------------------------------------------------------