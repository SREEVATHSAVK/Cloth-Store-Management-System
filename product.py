from tkinter import *
import time
from tkinter import ttk
from tkinter import messagebox
from connection_db import mycursor,connection

def connect_to_product():
    # functions part
    def slide_text(label, text):
        label.config(text="")
        # Add one character at a time with a delay
        for char in text:
            label.config(text=label.cget("text") + char)
            label.update()
            time.sleep(0.1)
    
    def operations(title,text,command):
        global idEntry,nameEntry,priceEntry,brandEntry,sectionEntry,window
        window = Toplevel()
        window.geometry("450x450+550+150")
        window.title(title)
        window.config(bg="pink") 
        window.resizable(0,0)
        window.grab_set()

        idLabel = Label(window,text = 'Product ID',font=('arial',16,'bold'),compound=LEFT,bg="pink")
        idLabel.place(x=20, y=30)
        idEntry = Entry(window,font=('times new roman',13,'bold'),fg="black",bd=3)
        idEntry.place(x=220, y=32)

        nameLabel = Label(window,text = 'Product Name',font=('arial',16,'bold'),compound=LEFT,bg="pink")
        nameLabel.place(x=20, y=100)
        nameEntry = Entry(window,font=('times new roman',13,'bold'),fg="black",bd=3)
        nameEntry.place(x=220, y=102)

        priceLabel = Label(window,text = 'Price',font=('arial',16,'bold'),compound=LEFT,bg="pink")
        priceLabel.place(x=20, y=170)
        priceEntry = Entry(window,font=('times new roman',13,'bold'),fg="black",bd=3)
        priceEntry.place(x=220, y=172)

        brandLabel = Label(window,text = 'Brand',font=('arial',16,'bold'),compound=LEFT,bg="pink")
        brandLabel.place(x=20, y=240)
        brandEntry = Entry(window,font=('times new roman',13,'bold'),fg="black",bd=3)
        brandEntry.place(x=220, y=242)

        sectionLabel = Label(window,text = 'Section',font=('arial',16,'bold'),compound=LEFT,bg="pink")
        sectionLabel.place(x=20, y=310)
        sectionEntry = Entry(window,font=('times new roman',13,'bold'),fg="black",bd=3)
        sectionEntry.place(x=220, y=312)

        searchButton = Button(window,command=command,text=text,width=15,font=('times new roman',14,'bold'),bg = "#3EB489",cursor="hand2")
        searchButton.place(x = 140, y = 370)

        if title == 'Update Operation':
            indexing = productTable.focus()
            content = productTable.item(indexing)
            idEntry.insert(0,content['values'][0])
            nameEntry.insert(1,content['values'][1])
            priceEntry.insert(2,content['values'][2])
            brandEntry.insert(3,content['values'][3])
            sectionEntry.insert(4,content['values'][4])

    def update_data():
        query = 'update product set prod_name=%s,price=%s,brand=%s,section=%s where prod_id=%s'
        mycursor.execute(query,(nameEntry.get(),priceEntry.get(),brandEntry.get(),sectionEntry.get(),idEntry.get()))
        connection.commit()
        messagebox.showinfo('Success',f'Product Id - {idEntry.get()} is modified Successfully',parent=window)
        window.destroy()
        view()

    def delete():
        def delete_data():
            indexing = productTable.focus()
            content = productTable.item(indexing)
            content_id = content['values'][0]
            query = 'delete from product where prod_id = %s'
            mycursor.execute(query,content_id)
            connection.commit()
            messagebox.showinfo('Deleted',f'{content_id} Product ID row is Deleted Succesfully',parent=window)
            window.destroy()
            view()

        window = Toplevel()
        window.geometry("450x200+540+280")
        window.title("Delete Operation")
        window.config(bg="pink") 
        window.resizable(0,0)
        window.grab_set()

        display = Label(window,text='Did you select the row of product table ?\n  If not, Please select the row of table',font=('arial',15,'bold'),bg='pink')
        display.place(x=20, y=30)

        yesButton = Button(window,command=delete_data,text='YES',font=('arial',12,'bold'),width=6,bg='yellow',cursor="hand2")
        yesButton.place(x=190,y=100)

    def search_data():
        query = 'select * from product where prod_id=%s or prod_name=%s or price=%s or brand=%s or section=%s'
        mycursor.execute(query,(idEntry.get(),nameEntry.get(),priceEntry.get(),brandEntry.get(),sectionEntry.get()))
        productTable.delete(*productTable.get_children())
        window.destroy()
        fetched_data = mycursor.fetchall()
        for data in fetched_data:
            productTable.insert('',END,values=data)

    def view():
        productTable.delete(*productTable.get_children())
        query = 'select * from product'
        mycursor.execute(query)
        fetched_data = mycursor.fetchall()
        for data in fetched_data:
            productTable.insert('',END,values=list(data))

    def add_data():
        if idEntry.get()=='' or nameEntry.get()=='' or brandEntry.get()=='' or priceEntry.get()=='' or sectionEntry.get()=='':
            messagebox.showerror('Error',"All Fields are required",parent=window)
        else:
            try:
                query = 'insert into product values(%s,%s,%s,%s,%s)'
                mycursor.execute(query,(idEntry.get(),nameEntry.get(),priceEntry.get(),brandEntry.get(),sectionEntry.get()))
                connection.commit()
                result = messagebox.showinfo('Confirm','Data added successfully',parent=window)
                if result:
                    idEntry.delete(0,END)
                    nameEntry.delete(0,END)
                    priceEntry.delete(0,END)
                    brandEntry.delete(0,END)
                    sectionEntry.delete(0,END)
                else:
                    pass
            except:
                messagebox('Error','Product ID cannot be repeated',parent=window)
                return
            window.destroy()
            view()

    # GUI part
    root = Toplevel()
    style = ttk.Style(root)
    style.theme_use("default")
    root.geometry("1400x750+65+15")
    root.title("Product Table")
    root.config(bg='whitesmoke')
    root.resizable(0,0)

    heading_label = Label(root,font=("Arial", 30,"bold"), pady=15,bg="whitesmoke")
    heading_label.pack()

    middleFrame = Frame(root, bg = "white",highlightbackground='black',highlightthickness=1)
    middleFrame.place(x = 50,y = 100, width = 1300, height = 520)

    productTable = ttk.Treeview(middleFrame,columns=('prod_id','prod_name','price','brand','section'))
    productTable.pack(fill=BOTH,expand=1)

    productTable.heading('prod_id',text = 'Product ID')
    productTable.column('prod_id',anchor=CENTER)
    productTable.heading('prod_name',text = 'Product Name')
    productTable.column('prod_name',anchor=CENTER)
    productTable.heading('price',text = 'Price')
    productTable.column('price',anchor=CENTER)
    productTable.heading('brand',text = 'Brande')
    productTable.column('brand',anchor=CENTER)
    productTable.heading('section',text = 'Section')
    productTable.column('section',anchor=CENTER)

    productTable.config(show='headings')
    view()
    addButton = Button(root,command=lambda: operations('Add Operation','ADD DATA',add_data),text='Insert',width=10,font=('times new roman',16,"bold"),bg='#00FF00',cursor="hand2")
    addButton.place(x=150,y=650)

    searchButton = Button(root,command=lambda: operations('Serach Operation','SEARCH DATA',search_data),text='Search',width=10,font=('times new roman',16,"bold"),bg='#DA70D6',cursor="hand2")
    searchButton.place(x=400,y=650)

    viewButton = Button(root,command=view,text='View Data',width=10,font=('times new roman',16,"bold"),bg='yellow',cursor="hand2")
    viewButton.place(x=650,y=650)

    deleteButton = Button(root,command=delete,text='Delete',width=10,font=('times new roman',16,"bold"),bg='red',cursor="hand2")
    deleteButton.place(x=900,y=650)

    updateButton = Button(root,command=lambda: operations('Update Operation','UPDATE DATA',update_data),text='Update',width=10,font=('times new roman',16,"bold"),bg='#A020F0',cursor="hand2")
    updateButton.place(x=1150,y=650)

    style = ttk.Style()
    style.configure('Treeview',rowheight=25,font=('arial',12,'normal'))
    style.configure("Treeview.Heading",font=('times new roman',16,"bold"),background='#FD7F20',padding=(30,10))
    
    slide_text(heading_label,'Product Table')
    root.mainloop()