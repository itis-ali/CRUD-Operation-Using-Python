from tkinter import *
import customtkinter as ctk
from Model.UserModel import UserModelClass
from BusinessLogicLayer.Publishers_BLL_Module import PublishersBLLClass
from datetime import datetime
from tkinter import ttk
from tkinter import messagebox as msg

class PublishersFormClass:
    def __init__(self, user: UserModelClass):
        self.User = user

    def publishersFormLoad(self):
        publishersForm = ctk.CTk()
        publishersForm.title('Publishers CRUD Form')
        publishersForm.geometry('640x655')
        publishersForm.iconbitmap('Images/page.ico')
        publishersForm.resizable(False, False)
        x = int((publishersForm.winfo_screenwidth() / 2) - (640 / 2))
        y = int((publishersForm.winfo_screenheight() / 2) - (655 / 2))
        publishersForm.geometry('+{}+{}'.format(x, y))

        # region Required Functions
        # region Date and time Function
        def setClock():
            currentDateTime = datetime.today()
            currentDateTime = currentDateTime.strftime('%Y/%m/%d  %H:%M:%S')
            txtCurrentDateTime.set(f'{currentDateTime}')
            publishersForm.after(1000, setClock)

        # endregion Date and time Function

        # region Update Treeview Style
        def updateTreeviewStyle():
            style = ttk.Style()
            if ctk.get_appearance_mode() == "Light":
                style.configure("Treeview", background="white", foreground="black",
                                rowheight=20, fieldbackground="white", bordercolor="#CCCCCC",
                                borderwidth=1, font=("Helvetica", 12))
                style.map('Treeview', background=[('selected', '#1a73e8')], foreground=[('selected', 'black')])
            elif ctk.get_appearance_mode() == "Dark":
                style.configure("Treeview", background="#2d2d2d", foreground="white",
                                rowheight=20, fieldbackground="#2d2d2d", bordercolor="#444444",
                                borderwidth=1, font=("Helvetica", 12))
                style.map('Treeview', background=[('selected', '#1a73e8')], foreground=[('selected', 'white')])
        # endregion Update Treeview Style

        # region Duplicate ID Check Functions
        def getPublisherID():
            publisherBLLObject = PublishersBLLClass()
            rows = publisherBLLObject.getPublisherIDBLL()
            publisherIDList = [row[0] for row in rows]
            return publisherIDList

        publisherID = getPublisherID()

        def duplicateIDCheckRegister():
            if txtPubID.get() in publisherID:
                msg.showerror("Error", "Duplicate Publisher ID!")
            else:
                registerPublisher()

        def duplicateIDCheckEdit():
            if txtPubID.get() not in publisherID:
                msg.showerror("Error", "Publisher ID must remain the same!")
            else:
                editPublisher()

        # endregion Duplicate ID Check Functions

        # region Register Publisher
        def registerPublisher():
            pubID = txtPubID.get()
            pubName = txtPubName.get()
            city = txtCity.get()
            state = "" if txtCity.get() == "None" else txtState.get()
            country = txtCountry.get()

            from Model.Publishers_Module import PublishersModelClass
            publishersModelObject = PublishersModelClass(pubID=pubID, pubName=pubName, city=city,
                                                         state=state, country=country)
            publishersBLLObject = PublishersBLLClass()
            publishersBLLObject.registerPublishersBLL(publishersModelObject)

            resetForm()
        # endregion Register Publisher

        # region Back To Main Button Function
        def backToMain():
            publishersForm.destroy()
            from UserInterfaceLayer.MainFormModule import MainFormClass
            mainFormObject = MainFormClass(user=self.User)
            mainFormObject.mainForm_Load()
        # endregion Back To Main Button Function

        # region Edit Publisher Function
        def editPublisher():
            PublisherID = txtPubID.get()
            PubName = txtPubName.get()
            City = txtCity.get()
            State = "" if txtCity.get() == "None" else txtState.get()
            Country = txtCountry.get()

            from Model.Publishers_Module import PublishersModelClass
            publishersModelObject = PublishersModelClass(pubID=PublisherID, pubName=PubName, city=City,
                                                         state=State, country=Country)
            publishersBLLObject = PublishersBLLClass()
            publishersBLLObject.editPublisher(publisher=publishersModelObject)
            resetForm()
            showList()
        # endregion Edit Publisher Function

        # region Delete Publisher Function
        def deletePublisher():
            pubID = txtPubID.get()
            if pubID is not NONE:
                employeeBLL_Object = PublishersBLLClass()
                employeeBLL_Object.deletePublisher(pubID)
            resetForm()
            showList()
        # endregion Delete Publisher Function

        # region Delete Publisher Confirmation Function
        def deletePublisherConfirmation():
            result = msg.askyesno("Confirm Delete", "Are you sure you want to delete this publisher?")
            if result:
                deletePublisher()
        # endregion Delete Publisher Confirmation Function

        # region Reset Form Function
        def resetForm():
            for widget in frameInfo.winfo_children():
                if isinstance(widget, ctk.CTkEntry):
                    widget.delete(0, ctk.END)
        # endregion Reset Form Function

        # region Pub ID Validation Function
        def checkValidationPubID(*args):
            if len(txtPubID.get()) > 4:
                    txtPubID.set(txtPubID.get()[:len(txtPubID.get()) - 1])
        # endregion Pub ID Validation Function

        # region Show Publishers List Function
        def showList(*args):
            publishersBLL_Object = PublishersBLLClass()
            publishersList = publishersBLL_Object.getPublishersList()
            if len(publishersList) > 0:
                tvPublishersList.delete(*tvPublishersList.get_children())
                rowCount = 0
                for row in publishersList:
                    rowCount += 1
                    values = [rowCount]
                    for value in row:
                        if value is NONE:
                            values.append("")
                        else:
                            values.append(value)
                    tvPublishersList.insert("", "end", values=values)
        # endregion Show Publishers List Function

        # region On Tree Selection Function
        def onTreeSelect(event):
            resetForm()
            index = tvPublishersList.selection()
            if index:
                selectedRow = tvPublishersList.item(index)['values']
                txtPubID.set(selectedRow[1])
                txtPubName.set(selectedRow[2])
                txtCity.set(selectedRow[3])
                txtState.set(selectedRow[4])
                txtCountry.set(selectedRow[5])
        # endregion On Tree Selection Function

        # endregion Required Functions

        # region Sidebar Frame
        sidebarFrame = ctk.CTkFrame(publishersForm, width=140, corner_radius=0)
        sidebarFrame.grid(row=0, column=0, rowspan=2, sticky="nsew")
        # sidebarFrame.grid_rowconfigure(2, weight=1)

        logoLabel = ctk.CTkLabel(sidebarFrame, text="PUBS", font=ctk.CTkFont(size=20, weight="bold"))
        logoLabel.grid(row=0, column=0, padx=20, pady=(20, 10))

        # region Form Name
        lblFormName = ctk.CTkLabel(sidebarFrame, text="Publishers' Form")
        lblFormName.grid(row=1, column=0, padx=20, pady=10)
        # endregion Form Name

        # region Back to Main
        btnBackToMain = ctk.CTkButton(sidebarFrame, text='Back to Main', width=140, command=backToMain,
                                      text_color='#000000', corner_radius=50, hover_color='#007860',
                                      border_width=1, fg_color='#00ffc3')
        btnBackToMain.grid(row=2, column=0, padx=10, pady=10, sticky=N)
        # endregion Back to Main

        # region Go to Authors Form
        def authorsCRUD():
            publishersForm.destroy()
            from UserInterfaceLayer.Authors_CRUD_Module import AuthorsFormClass
            authorsFormObject = AuthorsFormClass(user=self.User)
            authorsFormObject.authorsFormLoad()

        btnAuthorsCRUD = ctk.CTkButton(sidebarFrame, text="Authors' Form", width=140, command=authorsCRUD,
                                       text_color='#000000', corner_radius=50, hover_color='#007860',
                                       border_width=1, fg_color='#00ffc3')
        btnAuthorsCRUD.grid(row=3, column=0, padx=10, pady=10, sticky=N)

        # endregion Go to Authors Form

        # region Go to Employee Form
        def employeeCRUD():
            publishersForm.destroy()
            from UserInterfaceLayer.Employee_CRUD_Module import EmployeeFormClass
            employeeFormObject = EmployeeFormClass(user=self.User)
            employeeFormObject.employeeFormLoad()

        btnEmployeeCRUD = ctk.CTkButton(sidebarFrame, text="Employees' Form", width=140, command=employeeCRUD,
                                      text_color='#000000', corner_radius=50, hover_color='#007860',
                                      border_width=1, fg_color='#00ffc3')
        btnEmployeeCRUD.grid(row=4, column=0, padx=10, pady=10, sticky=N)
        # endregion Go to Employee Form

        # region Go To Jobs Form
        def jobsCRUD():
            publishersForm.destroy()
            from UserInterfaceLayer.Jobs_CRUD_Module import JobsFormClass
            jobsFormObject = JobsFormClass(user=self.User)
            jobsFormObject.jobsFormLoad()

        btnJobsCRUD = ctk.CTkButton(sidebarFrame, text="Jobs' Form", width=140, command=jobsCRUD,
                                    text_color='#000000', corner_radius=50, hover_color='#007860',
                                    border_width=1, fg_color='#00ffc3')
        btnJobsCRUD.grid(row=5, column=0, padx=10, pady=10, sticky='n')

        # endregion Go To Jobs Form

        # region Go To Sales Form
        def salesCRUD():
            publishersForm.destroy()
            from UserInterfaceLayer.Sales_CRUD_Module import SalesFormClass
            salesFormObject = SalesFormClass(user=self.User)
            salesFormObject.salesFormLoad()

        btnSalesCRUD = ctk.CTkButton(sidebarFrame, text="Sales' Form", width=140, command=salesCRUD,
                                     text_color='#000000', corner_radius=50, hover_color='#007860',
                                     border_width=1, fg_color='#00ffc3')
        btnSalesCRUD.grid(row=6, column=0, padx=10, pady=10, sticky=N)

        # endregion Go To Sales Form

        # region Go To Store Form
        def storesCRUD():
            publishersForm.destroy()
            from UserInterfaceLayer.Stores_CRUD_Module import StoresFormClass
            storesFormObject = StoresFormClass(user=self.User)
            storesFormObject.storesFormLoad()

        btnStoresCRUD = ctk.CTkButton(sidebarFrame, text="Stores' Form", width=140, command=storesCRUD,
                                      text_color='#000000', corner_radius=50, hover_color='#007860',
                                      border_width=1, fg_color='#00ffc3')
        btnStoresCRUD.grid(row=7, column=0, padx=10, pady=10, sticky=N)

        # endregion Go To Store Form

        # region Go To Titles Form
        def titlesCRUD():
            publishersForm.destroy()
            from UserInterfaceLayer.Titles_CRUD_Module import TitlesFormClass
            titlesFormObject = TitlesFormClass(user=self.User)
            titlesFormObject.titlesFormLoad()

        btnTitlesCRUD = ctk.CTkButton(sidebarFrame, text="Titles' Form", width=140, command=titlesCRUD,
                                      text_color='#000000', corner_radius=50, hover_color='#007860',
                                      border_width=1, fg_color='#00ffc3')
        btnTitlesCRUD.grid(row=8, column=0, padx=10, pady=10, sticky=N)
        # endregion Go To Titles Form

        # sidebarButtons = [
        #     ("Back to Main", backToMain),
        #     ("Authors' Form", authorsCRUD),
        #     ("Employees' Form", employeeCRUD),
        #     ("Jobs' Form", jobsCRUD),
        #     ("Sales' Form", salesCRUD),
        #     ("Stores' Form", storesCRUD),
        #     ("Titles' Form", titlesCRUD)
        # ]
        #
        # for buttonText, command in sidebarButtons:
        #     button = ctk.CTkButton(sidebarFrame, text=buttonText, width=140, command=command,
        #                               text_color='#000000', corner_radius=50, hover_color='#007860',
        #                               border_width=1, fg_color='#00ffc3')
        #     button.grid(pady=10)

        # region Date Widget
        txtCurrentDateTime = StringVar()
        lblCurrentDateTime = ctk.CTkLabel(sidebarFrame, textvariable=txtCurrentDateTime)
        lblCurrentDateTime.grid(row=9, column=0, padx=20, pady=10)
        # endregion Date Widget

        # endregion Sidebar Frame

        # region ttk Required Setup to match Theme
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", background="#2d2d2d", foreground="white", rowheight=20,
                        fieldbackground="#2d2d2d", bordercolor="#444444", borderwidth=1,
                            font=("Helvetica", 12))
        style.map('Treeview', background=[('selected', '#1a73e8')], foreground=[('selected', 'white')])
        # endregion ttk Required Setup to match Theme

        #region Treeview Frame
        frmTV = ctk.CTkFrame(publishersForm)
        frmTV.grid(row=0, column=1, padx=10, pady=10, ipadx=10, ipady=10, sticky=NSEW)

        # region Treeview Label
        lblTreeViewPrompt = ctk.CTkLabel(frmTV, text_color='#616161', font=("Helvetica", 12),
                                         text="View List")
        lblTreeViewPrompt.grid(row=0, column=0, padx=10, pady=0, sticky='w')
        # endregion Treeview Label

        # region Columns
        _columns = ['Index', 'PubID', 'PubName', 'City', 'State', 'Country']
        _displayColumns = ['Index', 'PubID', 'PubName', 'City', 'State', 'Country']
        # endregion Columns

        # region Treeview Widgets
        tvPublishersList = ttk.Treeview(frmTV, columns=_columns, displaycolumns=_displayColumns,
                                  show='headings', selectmode='browse')
        tvPublishersList.grid(row=1, column=0, padx=10, pady=10, sticky='W')

        tvPublishersList.bind('<<TreeviewSelect>>', onTreeSelect)

        tvPublishersList.column('#0', width=0)

        tvPublishersList.column(column='Index', width=50)
        tvPublishersList.heading(text='Index', column='Index')

        tvPublishersList.column(column='PubID', width=50)
        tvPublishersList.heading(text='Pub ID', column='PubID')

        tvPublishersList.column(column='PubName', width=190)
        tvPublishersList.heading(text='Pub Name', column='PubName')

        tvPublishersList.column(column='City', width=80)
        tvPublishersList.heading(text='City', column='City')

        tvPublishersList.column(column='State', width=80)
        tvPublishersList.heading(text='State', column='State')

        tvPublishersList.column(column='Country', width=80)
        tvPublishersList.heading(text='Country', column='Country')
        # endregion Treeview Widgets

        #endregion Treeview Frame

        # region Publishers' Information Frame
        frameInfo = ctk.CTkFrame(publishersForm)
        frameInfo.grid(row=1, column=1, padx=10, pady=(0, 10), ipadx=10, ipady=10)

        # region Frame Info Label
        lblFrameInfoPrompt = ctk.CTkLabel(frameInfo, text_color='#616161', font=("Helvetica", 12),
                                          text="Publishers' Information")
        lblFrameInfoPrompt.grid(row=0, column=0, padx=10, pady=0, sticky='w')
        # endregion Frame Info Label

        # region Pub ID
        lblPubID = ctk.CTkLabel(frameInfo, text='Pub ID: ')
        lblPubID.grid(row=1, column=0, padx=10, pady=10, sticky='w')

        txtPubID = StringVar()
        txtPubID.trace('w', checkValidationPubID)
        entPubID = ctk.CTkEntry(frameInfo, width=280, textvariable=txtPubID, corner_radius=50,
                                border_width=1, border_color='#FFFFFF')
        entPubID.grid(row=1, column=1, padx=10, pady=10, sticky='w')
        # endregion Pub ID

        # region Pub Name
        lblPubName = ctk.CTkLabel(frameInfo, text='Pub Name: ')
        lblPubName.grid(row=2, column=0, padx=10, pady=10, sticky='w')

        txtPubName = StringVar()
        entPubName = ctk.CTkEntry(frameInfo, width=280, textvariable=txtPubName, corner_radius=50,
                                border_width=1, border_color='#FFFFFF')
        entPubName.grid(row=2, column=1, padx=10, pady=10, sticky='w')
        # endregion Pub Name

        # region City
        lblCity = ctk.CTkLabel(frameInfo, text='City: ')
        lblCity.grid(row=3, column=0, padx=10, pady=10, sticky='w')

        txtCity = StringVar()
        entCity = ctk.CTkEntry(frameInfo, width=280, textvariable=txtCity, corner_radius=50,
                                border_width=1, border_color='#FFFFFF')
        entCity.grid(row=3, column=1, padx=10, pady=10, sticky='w')
        # endregion City

        # region State
        statesList = [
            "None",
            "AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA",
            "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD",
            "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ",
            "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC",
            "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"
        ]
        lblState = ctk.CTkLabel(frameInfo, text='State: ')
        lblState.grid(row=4, column=0, padx=10, pady=10, sticky='w')

        txtState = StringVar()
        cmdState = ctk.CTkComboBox(frameInfo, width=280, values=statesList, state='readonly',
                                   corner_radius=50, border_width=1, border_color='#FFFFFF', variable=txtState)
        cmdState.grid(row=4, column=1, padx=10, pady=10)
        # endregion State

        # region Country
        lblCountry = ctk.CTkLabel(frameInfo, text='Country: ')
        lblCountry.grid(row=5, column=0, padx=10, pady=10, sticky='w')

        txtCountry = StringVar()
        entCountry = ctk.CTkEntry(frameInfo, width=280, textvariable=txtCountry, corner_radius=50,
                                border_width=1, border_color='#FFFFFF')
        entCountry.grid(row=5, column=1, padx=10, pady=10, sticky='w')
        # endregion Country

        #region Register Publisher Button
        btnRegister = ctk.CTkButton(frameInfo, text='Register Publisher', width=130, command=duplicateIDCheckRegister,
                                    text_color='#000000', corner_radius=50, hover_color='#007860',
                                    border_width=1, fg_color='#00ffc3')
        btnRegister.grid(row=6, column=1, padx=10, pady=10, sticky='e')
        #endregion Register Publisher Button

        #region Edit Publisher Button
        btnEditPublisher = ctk.CTkButton(frameInfo, text='Edit Publisher', width=130, command=duplicateIDCheckEdit,
                                      text_color = '#000000', corner_radius = 50, hover_color = '#007860',
                                      border_width = 1, fg_color = '#00ffc3')
        btnEditPublisher.grid(row=6, column=1, padx=10, pady=10, sticky='w')
        #endregion Edit Publisher Button

        #region Reset Form Button
        btnResetForm = ctk.CTkButton(frameInfo, text='Clear Form', width=130, command=resetForm,
                                     text_color='#000000', corner_radius=50, hover_color='#007860',
                                     border_width=1, fg_color='#00ffc3')
        btnResetForm.grid(row=7, column=1, padx=10, pady=10, sticky='w')
        #endregion Reset Form Button

        #region Delete Publisher Button
        btnDeletePublisher = ctk.CTkButton(frameInfo, text='Delete Publisher', width=130,
                                           command=deletePublisherConfirmation,text_color = '#000000',
                                           corner_radius = 50, hover_color = '#910024',border_width = 1,
                                           fg_color = '#ff0040')
        btnDeletePublisher.grid(row=7, column=1, padx=10, pady=10, sticky='e')
        #endregion Delete Publisher Button

        # endregion Publishers' Information Frame

        updateTreeviewStyle()
        showList()
        publishersForm.after(0, setClock)
        publishersForm.mainloop()