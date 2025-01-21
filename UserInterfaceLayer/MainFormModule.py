from tkinter import *
import customtkinter as ctk
from PIL import Image
from datetime import datetime
from Model.UserModel import UserModelClass

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class MainFormClass:
    def __init__(self, user: UserModelClass):
        self.User = user

    def mainForm_Load(self):
        mainForm = ctk.CTk()
        mainForm.title('Main Form')
        mainForm.geometry('785x540')
        mainForm.iconbitmap('Images/home.ico')
        mainForm.resizable(False, False)
        x = int((mainForm.winfo_screenwidth() / 2) - (585 / 2))
        y = int((mainForm.winfo_screenheight() / 2) - (600 / 2))
        mainForm.geometry('+{}+{}'.format(x, y))

        # region Date and time Function
        def setClock():
            currentDateTime = datetime.today()
            currentDateTime = currentDateTime.strftime('%Y/%m/%d  %H:%M:%S')
            txtCurrentDateTime.set(f'{currentDateTime}')
            mainForm.after(1000, setClock)
        # endregion Date and time Function

        # region Appearance Function
        def changeAppearanceModeEvent(newAppearanceMode: str):
            ctk.set_appearance_mode(newAppearanceMode)
            appearanceModeOptionMenu.set("Light")
        # endregion Appearance Function

        # region Sidebar Frame
        sidebarFrame = ctk.CTkFrame(mainForm, width=140, corner_radius=0)
        sidebarFrame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        sidebarFrame.grid_rowconfigure(4, weight=1)

        logoLabel = ctk.CTkLabel(sidebarFrame, text="PUBS", font=ctk.CTkFont(size=20, weight="bold"))
        logoLabel.grid(row=0, column=0, padx=20, pady=(20, 10))

        # region Welcome
        lblWelcomeMessage = ctk.CTkLabel(sidebarFrame, text=f'Welcome {self.User.FirstName} {self.User.LastName}.')
        lblWelcomeMessage.grid(row=1, column=0, padx=20, pady=10)
        # endregion Welcome

        # region Appearance Mode
        appearanceModeLabel = ctk.CTkLabel(sidebarFrame, text="Appearance Mode:", anchor="w")
        appearanceModeLabel.grid(row=4, column=0, padx=20, pady=(10, 10), sticky='s')

        appearanceModeOptionMenu = ctk.CTkOptionMenu(sidebarFrame, values=["Light", "Dark"], fg_color='#00ffc3',
                                                     button_hover_color='#00ffc3', button_color='#007860',
                                                     text_color='#000000', command=changeAppearanceModeEvent,
                                                     corner_radius=50)
        appearanceModeOptionMenu.grid(row=5, column=0, padx=20, pady=(10, 10))

        if ctk.get_appearance_mode() == "Dark":
            appearanceModeOptionMenu.set("Dark")
        elif ctk.get_appearance_mode() == "Light":
            appearanceModeOptionMenu.set("Light")
        # endregion Appearance Mode

        # region Date Widget
        txtCurrentDateTime = StringVar()
        lblCurrentDateTime = ctk.CTkLabel(sidebarFrame, textvariable=txtCurrentDateTime)
        lblCurrentDateTime.grid(row=6, column=0, padx=20, pady=(10, 10))
        # endregion Date Widget

        # endregion Sidebar Frame

        # region Navigation Buttons

        # region Authors
        def authorsCRUD():
            mainForm.destroy()
            from UserInterfaceLayer.Authors_CRUD_Module import AuthorsFormClass
            authorFormObject = AuthorsFormClass(user=self.User)
            authorFormObject.authorsFormLoad()

        authorsBackground = ctk.CTkImage(Image.open('Images/icons8-author.png'), size=(100, 100))
        btnAuthorsCRUD = ctk.CTkButton(mainForm, text="Authors' CRUD", compound=TOP, border_color='#FFFFFF',
                                       border_width=1, image=authorsBackground, hover_color='#007860',
                                       corner_radius=30, width=150, height=150, fg_color='#00ffc3',
                                       text_color='#000000', command=authorsCRUD)
        btnAuthorsCRUD.grid(row=0, column=1, padx=15, pady=15)

        # endregion Authors

        # region Employee
        def employeeCRUD():
            mainForm.destroy()
            from UserInterfaceLayer.Employee_CRUD_Module import EmployeeFormClass
            employeeFormObject = EmployeeFormClass(user=self.User)
            employeeFormObject.employeeFormLoad()

        employeeBackground = ctk.CTkImage(Image.open('Images/icons8-employee.png'), size=(100, 100))
        btnEmployeeCRUD = ctk.CTkButton(mainForm, text="Employees' CRUD", compound=TOP, border_color='#FFFFFF',
                                        border_width=1, image=employeeBackground, hover_color='#007860',
                                        corner_radius=30, width=150, height=150, fg_color='#00ffc3',
                                        text_color='#000000', command=employeeCRUD)
        btnEmployeeCRUD.grid(row=0, column=2, padx=15, pady=15)
        # endregion Employee

        # region Publishers
        def publishersCRUD():
            mainForm.destroy()
            from UserInterfaceLayer.Publishers_CRUD_Module import PublishersFormClass
            publishersFormObject = PublishersFormClass(user=self.User)
            publishersFormObject.publishersFormLoad()

        publishersBackground = ctk.CTkImage(Image.open('Images/icons8-us-news.png'), size=(100, 100))
        btnPublishersCRUD = ctk.CTkButton(mainForm, text="Publishers' CRUD", compound=TOP, border_color='#FFFFFF',
                                          border_width=1, image=publishersBackground, hover_color='#007860',
                                          corner_radius=30, width=150, height=150, fg_color='#00ffc3',
                                          text_color='#000000', command=publishersCRUD)
        btnPublishersCRUD.grid(row=0, column=3, padx=15, pady=15, sticky='e')
        # endregion

        # region Jobs
        def jobsCRUD():
            mainForm.destroy()
            from UserInterfaceLayer.Jobs_CRUD_Module import JobsFormClass
            jobsFormObject = JobsFormClass(user=self.User)
            jobsFormObject.jobsFormLoad()

        jobsBackground = ctk.CTkImage(Image.open('Images/icons8-job.png'), size=(100, 100))
        btnJobsCRUD = ctk.CTkButton(mainForm, text="Jobs' CRUD", compound=TOP, border_color='#FFFFFF',
                                    border_width=1, image=jobsBackground, hover_color='#007860',
                                    corner_radius=30, width=150, height=150, fg_color='#00ffc3',
                                    text_color='#000000', command=jobsCRUD)
        btnJobsCRUD.grid(row=1, column=1, padx=15, pady=15)
        # endregion

        # region Sales
        def salesCRUD():
            mainForm.destroy()
            from UserInterfaceLayer.Sales_CRUD_Module import SalesFormClass
            salesFormObject = SalesFormClass(user=self.User)
            salesFormObject.salesFormLoad()

        salesBackground = ctk.CTkImage(Image.open('Images/icons8-sales.png'), size=(100, 100))
        btnSalesCRUD = ctk.CTkButton(mainForm, text="Sales' CRUD", compound=TOP, border_color='#FFFFFF',
                                     border_width=1, image=salesBackground, hover_color='#007860',
                                     corner_radius=30, width=150, height=150, fg_color='#00ffc3',
                                     text_color='#000000', command=salesCRUD)
        btnSalesCRUD.grid(row=1, column=2, padx=15, pady=15)
        # endregion

        # region Stores
        def storesCRUD():
            mainForm.destroy()
            from UserInterfaceLayer.Stores_CRUD_Module import StoresFormClass
            storesFormObject = StoresFormClass(user=self.User)
            storesFormObject.storesFormLoad()

        storesBackground = ctk.CTkImage(Image.open('Images/icons8-store.png'), size=(100, 100))
        btnStoresCRUD = ctk.CTkButton(mainForm, text="Stores' CRUD", compound=TOP, border_color='#FFFFFF',
                                      border_width=1, image=storesBackground, hover_color='#007860',
                                      corner_radius=30, width=150, height=150, fg_color='#00ffc3',
                                      text_color='#000000', command=storesCRUD)
        btnStoresCRUD.grid(row=1, column=3, padx=15, pady=15, sticky='e')
        # endregion

        # region Titles
        def titlesCRUD():
            mainForm.destroy()
            from UserInterfaceLayer.Titles_CRUD_Module import TitlesFormClass
            titlesFormObject = TitlesFormClass(user=self.User)
            titlesFormObject.titlesFormLoad()

        titlesBackground = ctk.CTkImage(Image.open('Images/icons8-book.png'), size=(100, 100))
        btnTitlesCRUD = ctk.CTkButton(mainForm, text="Titles' CRUD", compound=TOP, border_color='#FFFFFF',
                                      border_width=1, image=titlesBackground, hover_color='#007860',
                                      corner_radius=30, width=150, height=150, fg_color='#00ffc3',
                                      text_color='#000000', command=titlesCRUD)
        btnTitlesCRUD.grid(row=2, column=1, padx=15, pady=15)

        # endregion

        # region Settings
        # def settings():
        #     mainForm.destroy()
        #     from UserInterfaceLayer.Settings_Module import SettingsFormClass
        #     employeeFormObject = SettingsFormClass(user=self.User)
        #     employeeFormObject.settingsFormLoad()
        #
        # settingsBackground = ctk.CTkImage(Image.open('Images/icons8-setting.png'), size=(100, 100))
        # btnSettingsCRUD = ctk.CTkButton(mainForm, text="Settings", compound=TOP, border_color='#FFFFFF',
        #                                 border_width=1, image=settingsBackground, hover_color='#007860',
        #                                 corner_radius=30, width=150, height=150, fg_color='#00ffc3',
        #                                 text_color='#000000', command=settings)
        # btnSettingsCRUD.grid(row=2, column=2, padx=15, pady=15)
        # endregion

        # endregion Navigation Buttons

        mainForm.after(0, setClock)
        mainForm.mainloop()