from tkinter import *
import time
from tkinter import ttk
from tkinter import messagebox
from connection_db import mycursor,connection

def connect_to_stock():
    # functions part
    def slide_text(label, text):
        label.config(text="")
        # Add one character at a time with a delay
        for char in text:
            label.config(text=label.cget("text") + char)
            label.update()
            time.sleep(0.1)
    
    def operations(title,text,command):
        global idEntry,dateEntry,amtEntry,secEntry,window
        window = Toplevel()
        window.geometry("450x330+550+250")
        window.title(title)
        window.config(bg="pink") 
        window.resizable(0,0)
        window.grab_set()

        idLabel = Label(window,text = 'Stock ID',font=('arial',16,'bold'),compound=LEFT,bg="pink")
        idLabel.place(x=20, y=30)
        idEntry = Entry(window,font=('times new roman',13,'bold'),fg="black",bd=3)
        idEntry.place(x=220, y=32)

        amtLabel = Label(window,text = 'Amount',font=('arial',16,'bold'),compound=LEFT,bg="pink")
        amtLabel.place(x=20, y=90)
        amtEntry = Entry(window,font=('times new roman',13,'bold'),fg="black",bd=3)
        amtEntry.place(x=220, y=92)

        dateLabel = Label(window,text = 'Stock Date',font=('arial',16,'bold'),compound=LEFT,bg="pink")
        dateLabel.place(x=20, y=150)
        dateEntry = Entry(window,font=('times new roman',13,'bold'),fg="black",bd=3)
        dateEntry.place(x=220, y=152)

        secLabel = Label(window,text = 'Section',font=('arial',16,'bold'),compound=LEFT,bg="pink")
        secLabel.place(x=20, y=210)
        secEntry = Entry(window,font=('times new roman',13,'bold'),fg="black",bd=3)
        secEntry.place(x=220, y=212)

        searchButton = Button(window,command=command,text=text,width=15,font=('times new roman',14,'bold'),bg = "#3EB489",cursor="hand2")
        searchButton.place(x = 140, y = 270)

        if title == 'Update Operation':
            indexing = stockTable.focus()
            content = stockTable.item(indexing)
            idEntry.insert(0,content['values'][0])
            amtEntry.insert(2,content['values'][1])
            dateEntry.insert(1,content['values'][2])
            secEntry.insert(3,content['values'][3])

    def update_data():
        query = 'update stock set s_date=%s,s_amt=%s,section=%s where stock_id=%s'
        mycursor.execute(query,(dateEntry.get(),amtEntry.get(),secEntry.get(),idEntry.get()))
        connection.commit()
        messagebox.showinfo('Success',f'Stock Id - {idEntry.get()} is modified Successfully',parent=window)
        window.destroy()
        view()

    def delete():
        def delete_data():
            indexing = stockTable.focus()
            content = stockTable.item(indexing)
            content_id = content['values'][0]
            query = 'delete from stock where stock_id = %s'
            mycursor.execute(query,content_id)
            connection.commit()
            messagebox.showinfo('Deleted',f'{content_id} Stock ID row is Deleted Succesfully',parent=window,cursor="hand2")
            window.destroy()
            view()

        window = Toplevel()
        window.geometry("450x200+540+280")
        window.title("Delete Operation")
        window.config(bg="pink") 
        window.resizable(0,0)
        window.grab_set()

        display = Label(window,text='Did you select the row of stock table ?\n  If not, Please select the row of table',font=('arial',15,'bold'),bg='pink')
        display.place(x=20, y=30)

        yesButton = Button(window,command=delete_data,text='YES',font=('arial',12,'bold'),width=6,bg='yellow',cursor="hand2")
        yesButton.place(x=190,y=100)

    def search_data():
        query = 'select * from stock where stock_id=%s or s_amt=%s or s_date=%s or section=%s'
        mycursor.execute(query,(idEntry.get(),amtEntry.get(),dateEntry.get(),secEntry.get()))
        stockTable.delete(*stockTable.get_children())
        window.destroy()
        fetched_data = mycursor.fetchall()
        for data in fetched_data:
            stockTable.insert('',END,values=data)

    def view():
        stockTable.delete(*stockTable.get_children())
        query = 'select * from stock'
        mycursor.execute(query)
        fetched_data = mycursor.fetchall()
        for data in fetched_data:
            stockTable.insert('',END,values=list(data))

    def add_data():
        if idEntry.get()=='' or amtEntry.get()=='' or dateEntry.get()=='' or secEntry.get()=='':
            messagebox.showerror('Error',"All Fields are required",parent=window)
        else:
            try:
                query = 'insert into stock values(%s,%s,%s,%s)'
                mycursor.execute(query,(idEntry.get(),amtEntry.get(),dateEntry.get(),secEntry.get()))
                connection.commit()
                result = messagebox.showinfo('Confirm','Data added successfully',parent=window)
                if result:
                    idEntry.delete(0,END)
                    amtEntry.delete(0,END)
                    dateEntry.delete(0,END)
                    secEntry.delete(0,END)
                else:
                    pass
            except:
                messagebox('Error','Stock ID cannot be repeated',parent=window)
                return
            window.destroy()
            view()

    # GUI part
    root = Toplevel()
    style = ttk.Style(root)
    style.theme_use("default")
    root.geometry("1400x750+65+15")
    root.title("Stock Table")
    root.config(bg='whitesmoke')
    root.resizable(0,0)

    heading_label = Label(root,font=("Arial", 30,"bold"), pady=15,bg="whitesmoke")
    heading_label.pack()

    middleFrame = Frame(root, bg = "white",highlightbackground='black',highlightthickness=1)
    middleFrame.place(x = 50,y = 100, width = 1300, height = 520)

    stockTable = ttk.Treeview(middleFrame,columns=('stock_id','s_amt','s_date','section'))
    stockTable.pack(fill=BOTH,expand=1)

    stockTable.heading('stock_id',text = 'Stock ID')
    stockTable.column('stock_id',anchor=CENTER)
    stockTable.heading('s_amt',text = 'Amount')
    stockTable.column('s_amt',anchor=CENTER)
    stockTable.heading('s_date',text = 'Stock Date')
    stockTable.column('s_date',anchor=CENTER)
    stockTable.heading('section',text = 'Section')
    stockTable.column('section',anchor=CENTER)

    stockTable.config(show='headings')
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
    
    slide_text(heading_label,'Stock Table')
    root.mainloop()