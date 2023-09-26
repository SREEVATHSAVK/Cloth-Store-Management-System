from tkinter import *
from PIL import ImageTk, Image
from customer import connect_to_customer
from bill import connect_to_bill
from product import connect_to_product
from stock import connect_to_stock

def main():
    screen = Tk()
    screen.geometry("1275x770-1+0")
    screen.title("Cloth Store Management System")
    screen.config(bg='blanched almond')
    # screen.resizable(0,0)

    canvas = Canvas(screen, width=530, height=390)
    image = Image.open("./Images/main.jpeg")
    photo = ImageTk.PhotoImage(image)
    canvas.create_image(0, 0, anchor=NW, image=photo)
    canvas.place(x=-10,y=-10)
    canvas.place(x=700,y=180)

    heading_label = Label(screen, text="Cloth Store Management System",font=("Arial", 30),bg="navajo white")
    heading_label.place(x=350,y=45)

    paragraph = Label(screen,text='" A comprehensive database with tables of \n customer information, Product details,\n Bill data and Stock management "',
                    font=("Georgia",20,"bold"),bg='blanched almond',fg="midnight blue")
    paragraph.place(x=62,y=180)

    optionLabel = Label(screen,text='Select the table to view or update',font=("Cambria",20,"bold"),bg='blanched almond')
    optionLabel.place(x=120,y=350)

    customerButton = Button(screen,command=connect_to_customer,text='Customer',width=10,font=('times new roman',16,"bold"),bg='sandy brown',cursor="hand2")
    customerButton.place(x=150,y=420)

    billButton = Button(screen,command=connect_to_bill,text='Bill',width=10,font=('times new roman',16,"bold"),bg='sandy brown',cursor="hand2")
    billButton.place(x=350,y=420)

    productButton = Button(screen,command=connect_to_product,text='Product',width=10,font=('times new roman',16,"bold"),bg='sandy brown',cursor="hand2")
    productButton.place(x=150,y=500)

    stockButton = Button(screen,command=connect_to_stock,text='Stock',width=10,font=('times new roman',16,"bold"),bg='sandy brown',cursor="hand2")
    stockButton.place(x=350,y=500)

    screen.mainloop()
