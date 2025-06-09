import mysql.connector
import messagebox

def db(a, b, c, d, e):
    try:
        conn = mysql.connector.connect(host='localhost', password='Suj@y935974', user='root', database='game')
        Cursor_obj = conn.cursor()
        query = "insert into  create_account (email,username,mobile_no,pass,confirmpass) values(%s,%s,%s,%s,%s)"
        val = (a, b, c, d, e)
        Cursor_obj.execute(query, val)
        messagebox.showinfo('success', "Account is Successfully Created!!")
        conn.commit()
        conn.close()

    except:
        messagebox.showerror("Invalid", "Username already exist")

# --------------------------------------------------------------------------------------------------------
def verify_email(e):

    try:
        conn = mysql.connector.connect(host='localhost', password='Suj@y935974', user='root', database='game')
        Cursor_obj = conn.cursor()
        Cursor_obj.execute('select * from create_account')
        my_result = Cursor_obj.fetchall()
        for i in my_result:
            if e in i:
                return True


        conn.close()
    except:
        messagebox.showerror("Invalid", "Something! Went Wrong please Try again !")




def update_scorecard_shooter_game(a, b='sujay1233'):
        conn = mysql.connector.connect(host='localhost', password='Suj@y935974', user='root', database='game')
        Cursor_obj = conn.cursor()
        query = " update create_account set shooter_game_score = %s where username= %s"
        val = (a, b)
        Cursor_obj.execute ( query , val )
        conn.commit ( )
        conn.close ( )

