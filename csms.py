from tkinter import *
from PIL import ImageTk, Image
from customer import connect_to_customer
from bill import connect_to_bill
from product import connect_to_product
from stock import connect_to_stock

def main():
    screen = Tk()
    screen.geometry("1250x580+120+115")
    screen.title("Cloth Store Management System")
    screen.config(bg='#f1c727')
    # screen.resizable(0,0)

    canvas = Canvas(screen, width=530, height=390)
    image = Image.open("./Images/main.jpeg")
    photo = ImageTk.PhotoImage(image)
    canvas.create_image(0, 0, anchor=NW, image=photo)
    canvas.place(x=-10,y=-10)
    canvas.place(x=700,y=100)

    heading_label = Label(screen, text="Cloth Store Management System",font=("Arial", 30, "bold"),bg="#f1c727")
    heading_label.place(x=350,y=25)

    paragraph = Label(screen,text='" A comprehensive database with tables of \n customer information, Product details,\n Bill data and Stock management "',
                    font=("Monotype Corsiva",20,"bold"),bg='#f1c727')
    paragraph.place(x=100,y=130)

    optionLabel = Label(screen,text='Select the table to view or update',font=("Cambria",20,"bold"),bg='#f1c727')
    optionLabel.place(x=120,y=300)

    customerButton = Button(screen,command=connect_to_customer,text='Customer',width=10,font=('times new roman',16,"bold"),bg='#00FF00',cursor="hand2")
    customerButton.place(x=150,y=390)

    billButton = Button(screen,command=connect_to_bill,text='Bill',width=10,font=('times new roman',16,"bold"),bg='#00FF00',cursor="hand2")
    billButton.place(x=350,y=390)

    productButton = Button(screen,command=connect_to_product,text='Product',width=10,font=('times new roman',16,"bold"),bg='#00FF00',cursor="hand2")
    productButton.place(x=150,y=470)

    stockButton = Button(screen,command=connect_to_stock,text='Stock',width=10,font=('times new roman',16,"bold"),bg='#00FF00',cursor="hand2")
    stockButton.place(x=350,y=470)

    screen.mainloop()