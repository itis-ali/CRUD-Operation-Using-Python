from tkinter import *
import customtkinter as ctk
from tkinter import messagebox as msg
from DataAccessLayer.ConnectionFactory import ConnectionFactoryClass

loginForm = ctk.CTk()
loginForm.title('Login Form')
loginForm.geometry('500x160')
loginForm.iconbitmap('Images/identity.ico')
loginForm.resizable(False, False)

x = int((loginForm.winfo_screenwidth() / 2) - (500 / 2))
y = int((loginForm.winfo_screenheight() / 2) - (160 / 2))
loginForm.geometry('+{}+{}'.format(x, y))

# region Login Check Function
def checkLogin():
    username = entUserName.get()
    password = entPassword.get()

    commandText = "EXEC [dbo].[GetUsernameByUsernameAndPassword] ?,?"
    params = (username, password)

    with ConnectionFactoryClass().makeConnection() as sqlConnection:
        cursor = sqlConnection.cursor()
        cursor.execute(commandText, params)
        rows = cursor.fetchall()
    if len(rows) > 0:
        loginForm.destroy()
        from UserInterfaceLayer.MainFormModule import MainFormClass
        from Model.UserModel import UserModelClass
        userModelObject = UserModelClass(uname= username, pwd=password, fname=rows[0][2], lname=rows[0][3])

        mainFormObject = MainFormClass(userModelObject)
        mainFormObject.mainForm_Load()
    else:
        msg.showerror('Error!', 'Username or Password is incorrect!')
# endregion Login Check Function

# region Login Shortcut Function
def checkLoginShortcut(*args):
    checkLogin()
# endregion Login Shortcut Function

# region Animation Function
def animateText(index=0):
    if index < len(displayText):
        developerLabel.configure(text=displayText[:index] + '')
        loginForm.after(200, animateText, index + 1)
    else:
        animateText(0)
# endregion Animation Function

# region Forgot Password Function
def forgotPassword():
    msg.showinfo('Forgot Password?', 'We can do nothing for you bro.')
# endregion Forgot Password Function

# region Sidebar Frame
sidebarFrame = ctk.CTkFrame(loginForm, width=140, corner_radius=0)
sidebarFrame.grid(row=0, column=0, rowspan=4, sticky="nsew")
sidebarFrame.grid_rowconfigure(4, weight=1)

logoLabel = ctk.CTkLabel(sidebarFrame, text="PUBS", font=ctk.CTkFont(size=20, weight="bold"))
logoLabel.grid(row=0, column=0, padx=20, pady=(20, 10))

# region Developer Name
developerLabel = ctk.CTkLabel(sidebarFrame, text="Developed by:")
developerLabel.grid(row=1, column=0, padx=10, pady=0)

developerLabel = ctk.CTkLabel(sidebarFrame, text="")
developerLabel.grid(row=2, column=0, padx=20, pady=10)

displayText = "Ali\nRakhshani "
# endregion Developer Name

# endregion Sidebar Frame

# region Widgets
lblUserName = ctk.CTkLabel(loginForm, text='Username: ')
lblUserName.grid(row=0, column=1, padx=10, pady=20)

txtUserName = StringVar()
entUserName = ctk.CTkEntry(loginForm, width=280, textvariable=txtUserName, corner_radius=50,
                           border_width=1, border_color='#FFFFFF')
entUserName.grid(row=0, column=2, padx=10, pady=20)

lblPassword = ctk.CTkLabel(loginForm, text='Password: ')
lblPassword.grid(row=1, column=1, padx=10, pady=0)

txtPassword = StringVar()
entPassword = ctk.CTkEntry(loginForm, width=280, show='*', textvariable=txtPassword, corner_radius=50,
                           border_width=1, border_color='#FFFFFF')
entPassword.grid(row=1, column=2, padx=10, pady=0)

btnLogin = ctk.CTkButton(loginForm, text='Login', width=130, command=checkLogin, text_color='#000000',
                         corner_radius=50, hover_color='#007860', border_width=1, fg_color='#00ffc3')
btnLogin.grid(row=2, column=2, padx=10, pady=20, sticky='e')

btnForgotPassword = ctk.CTkButton(loginForm, text='Forgot Password?', width=130, command=forgotPassword,
                                  text_color='#000000', corner_radius=50, hover_color='#910024',
                                  border_width=1, fg_color='#ff0040')
btnForgotPassword.grid(row=2, column=2, padx=10, pady=20, sticky='w')



# endregion Widgets

animateText()
loginForm.bind("<Return>", checkLoginShortcut)
loginForm.mainloop()