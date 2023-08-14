from tkinter import *
import time
from tkinter import ttk
from tkinter import messagebox
from connection_db import mycursor,connection

def connect_to_customer():
    # functions part
    def slide_text(label, text):
        label.config(text="")
        # Add one character at a time with a delay
        for char in text:
            label.config(text=label.cget("text") + char)
            label.update()
            time.sleep(0.1)
    
    def operations(title,text,command):
        global idEntry,nameEntry,ageEntry,phnoEntry,addrEntry,window
        window = Toplevel()
        window.geometry("450x450+550+150")
        window.title(title)
        window.config(bg="pink") 
        window.resizable(0,0)
        window.grab_set()

        idLabel = Label(window,text = 'Customer ID',font=('arial',16,'bold'),compound=LEFT,bg="pink")
        idLabel.place(x=20, y=30)
        idEntry = Entry(window,font=('times new roman',13,'bold'),fg="black",bd=3)
        idEntry.place(x=220, y=32)

        nameLabel = Label(window,text = 'Customer Name',font=('arial',16,'bold'),compound=LEFT,bg="pink")
        nameLabel.place(x=20, y=100)
        nameEntry = Entry(window,font=('times new roman',13,'bold'),fg="black",bd=3)
        nameEntry.place(x=220, y=102)

        ageLabel = Label(window,text = 'Customer Age',font=('arial',16,'bold'),compound=LEFT,bg="pink")
        ageLabel.place(x=20, y=170)
        ageEntry = Entry(window,font=('times new roman',13,'bold'),fg="black",bd=3)
        ageEntry.place(x=220, y=172)

        phnoLabel = Label(window,text = 'Phone Number',font=('arial',16,'bold'),compound=LEFT,bg="pink")
        phnoLabel.place(x=20, y=240)
        phnoEntry = Entry(window,font=('times new roman',13,'bold'),fg="black",bd=3)
        phnoEntry.place(x=220, y=242)

        addrLabel = Label(window,text = 'Address',font=('arial',16,'bold'),compound=LEFT,bg="pink")
        addrLabel.place(x=20, y=310)
        addrEntry = Entry(window,font=('times new roman',13,'bold'),fg="black",bd=3)
        addrEntry.place(x=220, y=312)

        searchButton = Button(window,command=command,text=text,width=15,font=('times new roman',14,'bold'),bg = "#3EB489",cursor="hand2")
        searchButton.place(x = 140, y = 370)

        if title == 'Update Operation':
            indexing = customerTable.focus()
            content = customerTable.item(indexing)
            idEntry.insert(0,content['values'][0])
            nameEntry.insert(1,content['values'][1])
            ageEntry.insert(2,content['values'][2])
            phnoEntry.insert(3,content['values'][3])
            addrEntry.insert(4,content['values'][4])

    def update_data():
        query = 'update customer set cust_name=%s,age=%s,ph_no=%s,address=%s where cust_id=%s'
        mycursor.execute(query,(nameEntry.get(),ageEntry.get(),phnoEntry.get(),addrEntry.get(),idEntry.get()))
        connection.commit()
        messagebox.showinfo('Success',f'Customer Id - {idEntry.get()} is modified Successfully',parent=window)
        window.destroy()
        view()

    def delete():
        def delete_data():
            indexing = customerTable.focus()
            content = customerTable.item(indexing)
            content_id = content['values'][0]
            query = 'delete from customer where cust_id = %s'
            mycursor.execute(query,content_id)
            connection.commit()
            messagebox.showinfo('Deleted',f'{content_id} customer ID row is Deleted Succesfully',parent=window)
            window.destroy()
            view()

        window = Toplevel()
        window.geometry("450x200+540+280")
        window.title("Delete Operation")
        window.config(bg="pink") 
        window.resizable(0,0)
        window.grab_set()

        display = Label(window,text='Did you select the row of customer table ?\n  If not, Please select the row of table',font=('arial',15,'bold'),bg='pink')
        display.place(x=20, y=30)

        yesButton = Button(window,command=delete_data,text='YES',font=('arial',12,'bold'),width=6,bg='yellow',cursor="hand2")
        yesButton.place(x=190,y=100)

    def search_data():
        query = 'select * from customer where cust_id=%s or cust_name=%s or age=%s or ph_no=%s or address=%s'
        mycursor.execute(query,(idEntry.get(),nameEntry.get(),ageEntry.get(),phnoEntry.get(),addrEntry.get()))
        customerTable.delete(*customerTable.get_children())
        window.destroy()
        fetched_data = mycursor.fetchall()
        for data in fetched_data:
            customerTable.insert('',END,values=data)

    def view():
        customerTable.delete(*customerTable.get_children())
        query = 'select * from customer'
        mycursor.execute(query)
        fetched_data = mycursor.fetchall()
        for data in fetched_data:
            customerTable.insert('',END,values=list(data))

    def add_data():
        if idEntry.get()=='' or nameEntry.get()=='' or phnoEntry.get()=='' or ageEntry.get()=='' or addrEntry.get()=='':
            messagebox.showerror('Error',"All Fields are required",parent=window)
        else:
            try:
                query = 'insert into customer values(%s,%s,%s,%s,%s)'
                mycursor.execute(query,(idEntry.get(),nameEntry.get(),ageEntry.get(),phnoEntry.get(),addrEntry.get()))
                connection.commit()
                result = messagebox.showinfo('Confirm','Data added successfully',parent=window)
                if result:
                    idEntry.delete(0,END)
                    nameEntry.delete(0,END)
                    ageEntry.delete(0,END)
                    phnoEntry.delete(0,END)
                    addrEntry.delete(0,END)
                else:
                    pass
            except:
                messagebox('Error','Customer ID cannot be repeated',parent=window)
                return
            window.destroy()
            view()

    # GUI part
    root = Toplevel()
    style = ttk.Style(root)
    style.theme_use("default")
    root.geometry("1400x750+65+15")
    root.title("Customer Table")
    root.config(bg='whitesmoke')
    root.resizable(0,0)

    heading_label = Label(root,font=("Arial", 30,"bold"), pady=15,bg="whitesmoke")
    heading_label.pack()

    middleFrame = Frame(root, bg = "white",highlightbackground='black',highlightthickness=1)
    middleFrame.place(x = 50,y = 100, width = 1300, height = 520)

    customerTable = ttk.Treeview(middleFrame,columns=('cust_id','cust_name','age','ph_no','address'))
    customerTable.pack(fill=BOTH,expand=1)

    customerTable.heading('cust_id',text = 'Customer ID')
    customerTable.column('cust_id',anchor=CENTER)
    customerTable.heading('cust_name',text = 'Customer Name')
    customerTable.column('cust_name',anchor=CENTER)
    customerTable.heading('age',text = 'Customer Age')
    customerTable.column('age',anchor=CENTER)
    customerTable.heading('ph_no',text = 'Phone Number')
    customerTable.column('ph_no',anchor=CENTER)
    customerTable.heading('address',text = 'Address')
    customerTable.column('address',anchor=CENTER)

    customerTable.config(show='headings')
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
    
    slide_text(heading_label,'Customer Table')
    root.mainloop()