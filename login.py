from tkinter import *
import time
from tkinter import messagebox
import csms

#functionality part

def on_enter(event): 
    connect_button.config(bg="orange")
def on_leave(event): 
    connect_button.config(bg="#90EE90")

def clock():
    date = time.strftime('%d/%m/%Y') 
    currentTime = time.strftime('%H:%M:%S')
    dateTimeLabel.config(text = f'Date:{date}\nTime:{currentTime}')
    dateTimeLabel.after(1000,clock)

def slide_text():
    x = 0
    while True:
        heading_label.place(x=x, y=300)
        window.update()
        x += 0.003
        if x > window.winfo_width():
            x = -heading_label.winfo_width()

def connect_to_database():
     def login():
          if usernameEntry.get() == '' or passwordEntry.get() == '' or hostnameEntry.get() == '':
               messagebox.showerror('Error','Fields cannot be empty',parent=loginWindow)
          elif usernameEntry.get() != 'root' or passwordEntry.get() != '1234' or hostnameEntry.get() != 'localhost':
               messagebox.showerror('Error','Please enter correct credentials',parent=loginWindow)
          else:
               messagebox.showinfo('Success','Database Connection is Successful',parent=loginWindow)
               loginWindow.destroy()
               window.destroy()
               csms.main()

     loginWindow = Toplevel()
     loginWindow.geometry("500x270+520+300")
     loginWindow.title("Login Credentials")
     loginWindow.resizable(0,0)
     loginWindow.configure(bg="pink")
     loginWindow.grab_set()
     
     hostnameImage = PhotoImage(file='./Images/hostname.png')
     hostnameLabel = Label(loginWindow,image=hostnameImage,text = 'Host Name',font=('arial',16,'bold'),compound=LEFT,bg="pink")
     hostnameLabel.place(x=70, y=50)
     hostnameEntry = Entry(loginWindow,font=('times new roman',13,'bold'),fg="royalblue",bd=3)
     hostnameEntry.place(x=240, y=57)

     usernameImage = PhotoImage(file='./Images/username.png')
     usernameLabel = Label(loginWindow,image=usernameImage,text='User Name',font=('arial',16,'bold'),compound=LEFT,bg="pink")
     usernameLabel.place(x=70, y=95)
     usernameEntry = Entry(loginWindow,font=('times new roman',13,'bold'),fg="royalblue",bd=3)
     usernameEntry.place(x=240, y=102)

     passwordImage = PhotoImage(file='./Images/password.png')
     passwordLabel = Label(loginWindow,image=passwordImage,text='Password',font=('arial',16,'bold'),compound=LEFT,bg="pink")
     passwordLabel.place(x=70, y=145)
     passwordEntry = Entry(loginWindow,font=('times new roman',13,'bold'),fg="royalblue",bd=3)
     passwordEntry.place(x=240, y=152)

     loginButton = Button(loginWindow,command=login,text="Login",font=("Arial", 12, "bold"),width=10,bg = "cornflowerblue",
                         fg="white",activebackground="cornflowerblue",cursor="hand2")
     loginButton.place(x=190,y=200)

     loginWindow.mainloop()

#GUI part

window = Tk()
window.title("Database Connection")
window.geometry("1520x780+2+2")
window.grab_set()

# Create a Canvas widget
canvas = Canvas(window, width=1530, height=790)

# Load the background image
background_image = PhotoImage(file="./Images/db.png")

# Create a background image on the canvas
canvas.create_image(0, 0, anchor=NW, image=background_image)
canvas.place(x=-10,y=-10)
canvas.pack()

dateTimeLabel = Label(window,font = ('timew new roman',18,'bold'),bg="#0f133f",fg="white")
dateTimeLabel.place(x=35,y=35)
clock()

# Create a label for the heading
heading_label = Label(window, text="Welcome to the Cloth Store Management System", 
                      font=("Arial", 24, "bold"),bg="#132049",fg="white")
heading_label.place(x=450,y=330)

# Create a button to connect to the database
connect_button = Button(window, text="Connect To Database", 
                        command=connect_to_database,
                        width=18,
                        height=1,
                        font=("Arial", 18, "bold"),
                        bg = "#90EE90",
                        cursor="hand2"
                        )   
connect_button.place(x=360,y=400)

connect_button.bind("<Enter>", on_enter)
connect_button.bind("<Leave>", on_leave)

slide_text()


window.mainloop()

