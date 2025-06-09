from tkinter import *
import messagebox
from mainGui import *
import mysql.connector

class Rateus:
    def __init__(self , root1 , username_lg="", game=""):

        self.root1 = root1
        self.root1.title ( 'Rate Us' )
        self.root1.geometry ( '500x250+500+250' )
        self.root1.configure ( bg = "white" )
        self.root1.resizable ( False , False )


        count = 0


        def b1():

            self.but_fill1 = Button ( self.root1 , image = self.img1 , border = 0 , bg = 'white' , )
            self.but_fill1.place ( x = 80 , y = 80 )
            self.entry.delete ( 0 , 'end' )
            self.entry.insert(0, 'Poor!')


        def b2():
            self.but_fill1 = Button ( self.root1 , image = self.img1 , border = 0 , bg = 'white' , )
            self.but_fill1.place ( x = 80 , y = 80 )
            self.but_fill2 = Button ( self.root1 , image = self.img1 , border = 0 , bg = 'white' , )
            self.but_fill2.place ( x = 150 , y = 80 )
            self.entry.delete ( 0 , 'end' )
            self.entry.insert(0, 'Good!')

        def b3():
            self.but_fill1 = Button ( self.root1 , image = self.img1 , border = 0 , bg = 'white' , )
            self.but_fill1.place ( x = 80 , y = 80 )
            self.but_fill2 = Button ( self.root1 , image = self.img1 , border = 0 , bg = 'white' , )
            self.but_fill2.place ( x = 150 , y = 80 )
            self.but_fill3 = Button ( self.root1 , image = self.img1 , border = 0 , bg = 'white' , )
            self.but_fill3.place ( x = 220 , y = 80 )
            self.entry.delete ( 0 , 'end' )
            self.entry.insert ( 0 , 'Very Good!' )


        def b4():
            self.but_fill1 = Button ( self.root1 , image = self.img1 , border = 0 , bg = 'white' , )
            self.but_fill1.place ( x = 80 , y = 80 )
            self.but_fill2 = Button ( self.root1 , image = self.img1 , border = 0 , bg = 'white' , )
            self.but_fill2.place ( x = 150 , y = 80 )
            self.but_fill3 = Button ( self.root1 , image = self.img1 , border = 0 , bg = 'white' , )
            self.but_fill3.place ( x = 220 , y = 80 )
            self.but_fill4 = Button ( self.root1 , image = self.img1 , border = 0 , bg = 'white' , )
            self.but_fill4.place ( x = 290 , y = 80 )
            self.entry.delete ( 0 , 'end' )
            self.entry.insert ( 0 , 'Great!' )

        def b5():
            self.but_fill1 = Button ( self.root1 , image = self.img1 , border = 0 , bg = 'white' , )
            self.but_fill1.place ( x = 80 , y = 80 )
            self.but_fill2 = Button ( self.root1 , image = self.img1 , border = 0 , bg = 'white' , )
            self.but_fill2.place ( x = 150 , y = 80 )
            self.but_fill3 = Button ( self.root1 , image = self.img1 , border = 0 , bg = 'white' , )
            self.but_fill3.place ( x = 220 , y = 80 )
            self.but_fill4 = Button ( self.root1 , image = self.img1 , border = 0 , bg = 'white' , )
            self.but_fill4.place ( x = 290 , y = 80 )
            self.but_fill5 = Button ( self.root1 , image = self.img1 , border = 0 , bg = 'white' , )
            self.but_fill5.place ( x = 360 , y = 80 )

            self.entry.delete ( 0 , 'end' )
            self.entry.insert ( 0 , 'Excellent!' )


        def submitBut():
            if self.entry.get() == "":
                messagebox.showinfo ( "Invalid" , "Please select stars !" )

            else:
                if game == 0 and username_lg != "":
                    try:
                        self.rating = self.entry.get()
                        conn = mysql.connector.connect ( host = 'localhost' , password = 'Suj@y935974' , user = 'root' ,
                                                         database = 'game' )
                        Cursor_obj = conn.cursor ( )
                        query = " update create_account set rating_mario = %s where username= %s"
                        val = (self.rating, username_lg)
                        Cursor_obj.execute ( query , val )
                        messagebox.showinfo ( "Success" , "Thank You ! For Rating Us" )
                        conn.commit ( )
                        conn.close ( )
                        import mainGui
                        self.root1.destroy ( )
                        self.root = Tk ( )
                        self.obj = mainGui.Game ( self.root , username_lg )

                    except:
                        messagebox.showinfo("Invalid", "Something Went Wrong !")
                        # self.root1.destroy()

                elif game == 1 and username_lg != "":
                    try:
                        self.rating = self.entry.get ( )
                        conn = mysql.connector.connect ( host = 'localhost' , password = 'Suj@y935974' , user = 'root' ,
                                                         database = 'game' )
                        Cursor_obj = conn.cursor ( )
                        query = " update create_account set rating_shooter = %s where username= %s"
                        val = (self.rating , username_lg)
                        Cursor_obj.execute ( query , val )
                        messagebox.showinfo ( "Success" , "Thank You ! For Rating Us" )
                        conn.commit ( )
                        conn.close ( )
                        import mainGui
                        self.root1.destroy ( )
                        self.root = Tk ( )
                        self.obj = mainGui.Game ( self.root , username_lg )

                    except:
                        messagebox.showinfo ( "Invalid" , "Something Went Wrong !" )
                        # self.root1.destroy()
                elif game == 2 and username_lg != "":
                    try:
                        self.rating = self.entry.get ( )
                        conn = mysql.connector.connect ( host = 'localhost' , password = 'Suj@y935974' , user = 'root' ,
                                                         database = 'game' )
                        Cursor_obj = conn.cursor ( )
                        query = " update create_account set rating_flappy = %s where username= %s"
                        val = (self.rating , username_lg)
                        Cursor_obj.execute ( query , val )
                        messagebox.showinfo ( "Success" , "Thank You ! For Rating Us" )
                        conn.commit ( )
                        conn.close ( )
                        import mainGui
                        self.root1.destroy ( )
                        self.root = Tk ( )
                        self.obj = mainGui.Game ( self.root , username_lg )

                    except:
                        messagebox.showinfo ( "Invalid" , "Something Went Wrong !" )
                        # self.root1.destroy()

                elif game == 3 and username_lg != "":
                    try:
                        self.rating = self.entry.get ( )
                        conn = mysql.connector.connect ( host = 'localhost' , password = 'Suj@y935974' , user = 'root' ,
                                                         database = 'game' )
                        Cursor_obj = conn.cursor ( )
                        query = " update create_account set rating_space = %s where username= %s"
                        val = (self.rating , username_lg)
                        Cursor_obj.execute ( query , val )
                        messagebox.showinfo ( "Success" , "Thank You ! For Rating Us" )
                        conn.commit ( )
                        conn.close ( )
                        import mainGui
                        self.root1.destroy ( )
                        self.root = Tk ( )
                        self.obj = mainGui.Game ( self.root , username_lg )

                    except:
                        messagebox.showinfo ( "Invalid" , "Something Went Wrong !" )
                        # self.root1.destroy()

        self.img1 = PhotoImage ( file = 'images/starfill.png' )
        self.img20 = PhotoImage ( file = 'images/starempty.png' )

        Label ( root1 , text = 'Rate Us ' , width = 10 , border = 0 , fg = 'Red' , bg = 'white' ,
                font = ('Berlin Sans FB Demi' , 18 , 'bold') ).place ( x = 180 , y = 10 )
        self.entry = Entry ( self.root1 , width = 10 , border = 0 , fg = 'Blue' , bg = 'white' ,
                             font = ('Modern no. 20' , 18 , 'bold') )
        self.entry.place ( x = 50 , y = 180 )

        self.but1 = Button(self.root1,image = self.img20, border = 0, bg = 'white', command = b1)
        self.but1.place(x=80, y=80)
        self.but2 = Button(self.root1,image = self.img20, border = 0, bg = 'white', command = b2)
        self.but2.place(x=150, y=80)
        self.but3 = Button(self.root1,image = self.img20, border = 0, bg = 'white',command = b3)
        self.but3.place(x=220, y=80)
        self.but4 = Button(self.root1,image = self.img20, border = 0, bg = 'white', command = b4)
        self.but4.place(x=290, y=80)
        self.but5 = Button(self.root1,image = self.img20, border = 0, bg = 'white', command = b5)
        self.but5.place(x=360, y=80)

        self.submit = Button(self.root1,text = 'Submit', bg='blue', fg = 'White', font = ('Modern No. 20', 15, 'bold') , cursor = 'hand2', command = submitBut)
        self.submit.place(x=210, y= 180)



if __name__=='__main__':
    root1 = Tk ( )
    # for f in root1.winfo_children ( ):
    #     f.destroy ( )
    obj = Rateus( root1, username_lg="", game="")
    root1.mainloop ( )

