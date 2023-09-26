from tkinter import *
import time
from tkinter import ttk
from tkinter import messagebox
from connection_db import mycursor,connection

def connect_to_bill():
    # functions part
    def slide_text(label, text):
        label.config(text="")
        # Add one character at a time with a delay
        for char in text:
            label.config(text=label.cget("text") + char)
            label.update()
            time.sleep(0.1)
    
    def operations(title,text,command):
        global bidEntry,cidEntry,pidEntry,qtyEntry,amtEntry,purchaseEntry,window
        window = Toplevel()
        window.geometry("450x450+550+150")
        window.title(title)
        window.config(bg="blanched almond") 
        window.resizable(0,0)
        window.grab_set()

        bidLabel = Label(window,text = 'Bill ID',font=('arial',16,'bold'),compound=LEFT,bg="blanched almond")
        bidLabel.place(x=20, y=30)
        bidEntry = Entry(window,font=('times new roman',13,'bold'),fg="black",bd=3)
        bidEntry.place(x=220, y=32)

        cidLabel = Label(window,text = 'Customer ID',font=('arial',16,'bold'),compound=LEFT,bg="blanched almond")
        cidLabel.place(x=20, y=90)
        cidEntry = Entry(window,font=('times new roman',13,'bold'),fg="black",bd=3)
        cidEntry.place(x=220, y=92)

        pidLabel = Label(window,text = 'Product ID',font=('arial',16,'bold'),compound=LEFT,bg="blanched almond")
        pidLabel.place(x=20, y=150)
        pidEntry = Entry(window,font=('times new roman',13,'bold'),fg="black",bd=3)
        pidEntry.place(x=220, y=152)

        qtyLabel = Label(window,text = 'Quantity',font=('arial',16,'bold'),compound=LEFT,bg="blanched almond")
        qtyLabel.place(x=20, y=210)
        qtyEntry = Entry(window,font=('times new roman',13,'bold'),fg="black",bd=3)
        qtyEntry.place(x=220, y=212)

        amtLabel = Label(window,text = 'Amount',font=('arial',16,'bold'),compound=LEFT,bg="blanched almond")
        amtLabel.place(x=20, y=270)
        amtEntry = Entry(window,font=('times new roman',13,'bold'),fg="black",bd=3)
        amtEntry.place(x=220, y=272)

        purchaseLabel = Label(window,text = 'Purchase Date',font=('arial',16,'bold'),compound=LEFT,bg="blanched almond")
        purchaseLabel.place(x=20, y=330)
        purchaseEntry = Entry(window,font=('times new roman',13,'bold'),fg="black",bd=3)
        purchaseEntry.place(x=220, y=332)

        searchButton = Button(window,command=command,text=text,width=15,font=('times new roman',14,'bold'),bg = "sandy brown",cursor="hand2")
        searchButton.place(x = 140, y = 390)

        if title == 'Update Operation':
            indexing = BillTable.focus()
            content = BillTable.item(indexing)
            bidEntry.insert(content['values'][0])
            cidEntry.insert(0,content['values'][1])
            pidEntry.insert(0,content['values'][2])
            qtyEntry.insert(1,content['values'][3])
            amtEntry.insert(2,content['values'][4])
            purchaseEntry.insert(3,content['values'][5])

    def update_data():
        query = 'update bill set cid=%s,pid=%s,qty=%s,amt=%s,purchase_date=%s where bid=%s'
        mycursor.execute(query,(cidEntry.get(),pidEntry.get(),qtyEntry.get(),amtEntry.get(),purchaseEntry.get(),bidEntry.get()))
        connection.commit()
        messagebox.showinfo('Success',f'Bill Id {bidEntry.get()} is modified Successfully',parent=window)
        window.destroy()
        view()

    def delete():
        def delete_data():
            indexing = BillTable.focus()
            content = BillTable.item(indexing)
            content_id = content['values'][0]
            query = 'delete from bill where bid = %s'
            mycursor.execute(query,content_id)
            connection.commit()
            messagebox.showinfo('Deleted',f'{content_id} Bill ID row is Deleted Succesfully',parent=window)
            window.destroy()
            view()

        window = Toplevel()
        window.geometry("450x200+540+280")
        window.title("Delete Operation")
        window.config(bg="blanched almond") 
        # window.resizable(0,0)
        window.grab_set()

        display = Label(window,text='Did you select the row of customer table ?\n  If not, Please select the row of table',font=('arial',15,'bold'),bg='blanched almond')
        display.place(x=20, y=30)

        yesButton = Button(window,command=delete_data,text='YES',font=('arial',12,'bold'),width=6,bg='sandy brown',cursor="hand2")
        yesButton.place(x=190,y=100)

    def search_data():
        query = 'select * from bill where bid=%s or cid=%s or pid=%s or qty=%s or amt=%s or purchase_date=%s'
        mycursor.execute(query,(bidEntry.get(),cidEntry.get(),pidEntry.get(),qtyEntry.get(),amtEntry.get(),purchaseEntry.get()))
        BillTable.delete(*BillTable.get_children())
        window.destroy()
        fetched_data = mycursor.fetchall()
        for data in fetched_data:
            BillTable.insert('',END,values=data)
    
    

    def view():
        BillTable.delete(*BillTable.get_children())
        query = 'select * from bill'
        mycursor.execute(query)
        fetched_data = mycursor.fetchall()
        for data in fetched_data:
            BillTable.insert('',END,values=list(data))

    def add_data():
        if cidEntry.get()=='' or qtyEntry.get()=='' or purchaseEntry.get()=='' or amtEntry.get()=='' or bidEntry.get()=='' or pidEntry.get()=='':
            messagebox.showerror('Error',"All Fields are required",parent=window)
        else:
            try:
                query = 'insert into bill values(%s,%s,%s,%s,%s)'
                mycursor.execute(query,(bidEntry.get(),cidEntry.get(),pidEntry.get(),qtyEntry.get(),amtEntry.get(),purchaseEntry.get()))
                connection.commit()
                result = messagebox.showinfo('Confirm','Data added successfully',parent=window)
                if result:
                    bidEntry.delete(0,END)
                    cidEntry.delete(0,END)
                    pidEntry.delete(0,END)
                    qtyEntry.delete(0,END)
                    amtEntry.delete(0,END)
                    purchaseEntry.delete(0,END)
                else:
                    pass
            except:
                messagebox('Error','Bill ID cannot be repeated',parent=window)
                return
            window.destroy()
            view()

    # GUI part
    root = Toplevel()
    style = ttk.Style(root)
    style.theme_use("default")
    root.geometry("1275x770-1+0")
    root.title("Customer Table")
    root.config(bg='whitesmoke')
    # root.resizable(0,0)

    heading_label = Label(root,font=("Arial", 30,"bold"), pady=15,bg="whitesmoke")
    heading_label.pack()

    middleFrame = Frame(root, bg = "white",highlightbackground='black',highlightthickness=1)
    middleFrame.place(x = 35,y = 100, width = 1200, height = 520)

    BillTable = ttk.Treeview(middleFrame,columns=('bill_id','cid','pid','qty','amt','purchase_date'))
    BillTable.pack(fill=BOTH,expand=1)

    BillTable.heading('bill_id',text = 'Bill ID')
    BillTable.column('bill_id',anchor=CENTER)
    BillTable.heading('cid',text = 'Customer ID')
    BillTable.column('cid',anchor=CENTER)
    BillTable.heading('pid',text = 'Product ID')
    BillTable.column('pid',anchor=CENTER)
    BillTable.heading('qty',text = 'Quantity')
    BillTable.column('qty',anchor=CENTER)
    BillTable.heading('amt',text = 'Amount')
    BillTable.column('amt',anchor=CENTER)
    BillTable.heading('purchase_date',text = 'Purchase Date')
    BillTable.column('purchase_date',anchor=CENTER)

    BillTable.config(show='headings')
    view()
    addButton = Button(root,command=lambda: operations('Add Operation','ADD DATA',add_data),text='Insert',width=10,font=('times new roman',16,"bold"),bg='orange',cursor="hand2")
    addButton.place(x=35,y=650)

    searchButton = Button(root,command=lambda: operations('Serach Operation','SEARCH DATA',search_data),text='Search',width=10,font=('times new roman',16,"bold"),bg='khaki3',cursor="hand2")
    searchButton.place(x=300,y=650)

    viewButton = Button(root,command=view,text='View Data',width=10,font=('times new roman',16,"bold"),bg='bisque3',cursor="hand2")
    viewButton.place(x=560,y=650)

    deleteButton = Button(root,command=delete,text='Delete',width=10,font=('times new roman',16,"bold"),bg='OrangeRed2',cursor="hand2")
    deleteButton.place(x=840,y=650)

    updateButton = Button(root,command=lambda: operations('Update Operation','UPDATE DATA',update_data),text='Update',width=10,font=('times new roman',16,"bold"),bg='thistle1',cursor="hand2")
    updateButton.place(x=1100,y=650)

    style = ttk.Style()
    style.configure('Treeview',rowheight=25,font=('arial',12,'normal'))
    style.configure("Treeview.Heading",font=('times new roman',16,"bold"),background='#FD7F20',padding=(30,10))
    
    slide_text(heading_label,'Bill Table')
    root.mainloop()
