import cv2
from tkinter import *
from PIL import Image,ImageTk
root1 = Tk ( )
root1.title ( 'How to Play Flappy Bird Game ' )
root1.geometry ( '900x780+360+0' )
root1.configure ( bg = "white" )
root1.resizable ( False , False )

ima = cv2.imread("C:/Users/sujal/PycharmProjects/Sem4 Python Project/images/terms and condition.png" )
imgr1 = cv2.resize ( ima , (900 , 780) )
img_rgb1 = cv2.cvtColor ( imgr1 , cv2.COLOR_BGR2RGB )
img_tk = ImageTk.PhotoImage ( Image.fromarray ( img_rgb1 ) )

Label( root1,image = img_tk).place(x=0,y=5)

root1.mainloop()