import database
import smtplib
from Forgot_Password import *
class Forgot_Password:

    # constructor
    def __init__(self , root2, username_lg=""):
        self.main = root2
        self.main.title('Forgot password')
        self.main.geometry('1534x780+-8+0')
        self.main.configure(bg="white")
        self.main.resizable(False, False)
        self.img = PhotoImage(file='images/forget password.png')
        Label(self.main, image=self.img, bg='white').place(x=250, y=160)

        self.f2 = (Frame(self.main, width=450, height=550, bg="white"))
        self.f2.place(x=800, y=130)

        self.heading = Label(self.f2, text='Email Verification', fg='Blue', bg='white', font=('copper black', 23, 'bold'))
        self.heading.place(x=110, y=40)

        self.img1 = PhotoImage(file='images/logo.png')
        self.l = Label(self.main, image=self.img1, bg='white')
        self.l.place(x=10, y=12)
        self.img2 = PhotoImage(file='images/back.png')
        self.l = Label(self.main, image=self.img2, bg='white')
        self.l.place(x=140, y=25)



        def verify_email():
            self.e = self.email.get()

            self.flag = database.verify_email(self.e)

            if self.flag :
                self.generate_otp = ''.join(str(random.randint(100000, 999999)))
                try:
                    self.receiver = self.e
                    self.server = smtplib.SMTP('smtp.gmail.com', 587)
                    self.server.starttls()
                    self.server.login('khedekarsujay3@gmail.com', 'cbnt xifq dmaw nxrz')
                    self.msg = ('Welcome to Exsto Online Gaming Platform!! \n'
                           'Your Happiness and Fun build our experience. \n'
                           'So Are you interested to play ??? \n'
                           'Then take this OTP \n'
                           'Your One Time Password (OTP) For Email verification is ' + str(self.generate_otp))
                    self.server.sendmail('khedekarsujay3@gmail.com', self.receiver, self.msg)
                    messagebox.showinfo('Success', 'OTP is Send successfully!')
                    self.server.quit()

                    # time.sleep(3)
                    self.main.destroy()
                    self.root1 = Tk()
                    self.root1.title('OTP Page')
                    self.root1.geometry('500x250+500+250')
                    self.root1.configure(bg="white")
                    self.root1.resizable(False, False)


                    self.F_1 = (Frame(self.root1, width=500, height=250, bg="white"))
                    self.F_1.place(x=0, y=0)

                    self.heading1 = Label(self.F_1, text='OTP Verification', fg='blue', bg='white', font=('Country', 18, 'bold'))
                    self.heading1.place(x=150, y=20)
                    self.l = Label(self.F_1, text="Enter OTP - ", fg='Red', bg='white', font=('Microsoft YaHei UI Light', 12, 'bold'))
                    self.l.place(x=60, y=100)
                    self.email1 = Entry(self.F_1, width=20, fg='black', bg='white', font=('Microsoft YaHei UI Light', 14, 'bold'))
                    self.email1.place(x=200, y=100)

                    # -----------------------------------------------------------------------------------------------------
                    def otp_verify(a):
                        if a == self.generate_otp:
                            messagebox.showinfo('Success', 'OTP Verification Successful!')
                            import Forgot_Password
                            self.main.destroy ( )
                            self.root1 = Tk ( )
                            self.obj = Forgot_Password.change_pass ( self.root1 , username_lg = f"{username_lg}" )
                        else:
                            messagebox.askretrycancel('Invalid', 'Enter Correct OTP !')

                        # --------------------------------------------------------------------------------------------------

                    def verify():
                        self.Entered_otp = str(self.email1.get())
                        print(otp_verify(self.Entered_otp))

                    # --------------------------------------------------------------------------------------------------
                    def otp_resend():
                        try:
                            self.generate_otp_resend = ''.join(str(random.randint(100000, 999999)))
                            # self.generate_otp = self.generate_otp_resend
                            self.receiver1 = self.e
                            self.server1 = smtplib.SMTP('smtp.gmail.com', 587)
                            self.server1.starttls()
                            self.server1.login('khedekarsujay3@gmail.com', 'cbnt xifq dmaw nxrz')
                            self.msg1 = ('Welcome to Exsto Online Gaming Platform!! \n'
                                    'Your Happiness and Fun build our experience. \n'
                                    'So Are you interested to play ??? \n'
                                    'Then take this OTP \n'
                                    'Your One Time Password (OTP) For Email verification is ' + str(self.generate_otp_resend))
                            self.server1.sendmail('khedekarsujay3@gmail.com', self.receiver1, self.msg1)
                            messagebox.showinfo('Success', 'OTP is Send successfully!')
                            self.server1.quit()

                        except:
                            messagebox.showerror('Invalid', 'Something ! Went Wrong please Try again !')

                        # ----------------------------------------------------------------------------------------------------



                    self.button3 = Button(self.F_1, fg='white', bg='blue', width=15, text='Verify', pady=3, border=0, font=('bold', 9),
                                     cursor='hand2', command=verify)
                    self.button3.place(x=80, y=190)
                    self.button4 = Button(self.F_1, fg='white', bg='blue', width=15, text='Resend', pady=3, border=0,
                                     font=("Country", 9),
                                     cursor='hand2', command=otp_resend)
                    self.button4.place(x=310, y=190)

                    self.root1.mainloop()

                except:
                    messagebox.showerror('Invalid', 'Something! Went Wrong please Try again !')
            else:
                messagebox.showerror('Invalid', 'Either Enter valid Email address or Email is not registered !')



        def login():
            import login
            self.main.destroy ( )
            self.root1 = Tk ( )
            self.obj = login.LogInPage( self.root1 , username_lg = f"{username_lg}" )


        # ------------------------------------------------------------------------------------------------------------------
        self.label = Label(self.f2, text="Enter Your Email ", fg='Red', bg='white', font=('Century', 19, 'bold'))
        self.label.place(x=40, y=140)
        self.email = Entry(self.f2, width=30, fg='black', bg='white', font=('Microsoft YaHei UI Light', 18))
        self.email.place(x=50, y=200)
        Frame(self.f2, width=390, height=2, bg='black').place(x=50, y=235)

        self.button1 = Button(self.f2, fg='white', bg='blue', width=20, text='Get OTP', pady=2, border=0, font=('bold', 11),
                         cursor= 'hand2', command=verify_email)
        self.button1.place(x=145, y=300)

        self.button1 = Button(self.main, image = self.img2, border=0,bg="white", command = login )
        self.button1.place(x=140, y=25)

        Label(self.main, text = 'Back', font = ('Future', 12, 'bold') ).place(x=153, y=105)


if __name__=='__main__':
    root2 = Tk ( )
    for f in root2.winfo_children ( ):
        f.destroy ( )
    obj = Forgot_Password( root2, username_lg="")
    root2.mainloop()


# ------------------------------------------------------------------------------------------------------------------

