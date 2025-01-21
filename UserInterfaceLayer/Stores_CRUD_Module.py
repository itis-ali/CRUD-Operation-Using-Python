from tkinter import *
import customtkinter as ctk
from Model.UserModel import UserModelClass
from BusinessLogicLayer.Stores_BLL_Module import StoresBLLClass
from datetime import datetime
from tkinter import ttk
from tkinter import messagebox as msg
import re

class StoresFormClass:
    def __init__(self, user: UserModelClass):
        self.User = user

    def storesFormLoad(self):
        storesForm = ctk.CTk()
        storesForm.title('Stores CRUD Form')
        storesForm.geometry('1135x490')
        storesForm.iconbitmap('Images/page.ico')
        storesForm.resizable(False, False)
        x = int((storesForm.winfo_screenwidth() / 2) - (1135 / 2))
        y = int((storesForm.winfo_screenheight() / 2) - (490 / 2))
        storesForm.geometry('+{}+{}'.format(x, y))

        # region Required Functions

        # region Date and time Function
        def setClock():
            currentDateTime = datetime.today()
            currentDateTime = currentDateTime.strftime('%Y/%m/%d  %H:%M:%S')
            txtCurrentDateTime.set(f'{currentDateTime}')
            storesForm.after(1000, setClock)

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
        def getStoresID():
            storeBLLObject = StoresBLLClass()
            rows = storeBLLObject.getStoreIDBLL()
            storeIDList = [row[0] for row in rows]
            return storeIDList

        storeID = getStoresID()

        def duplicateIDCheckRegister():
            if txtStoreID.get() in storeID:
                msg.showerror("Error", "Duplicate Store ID!")
            else:
                registerStores()

        def duplicateIDCheckEdit():
            if txtStoreID.get() not in storeID:
                msg.showerror("Error", "Store ID must remain the same!")
            else:
                editStores()

        # endregion Duplicate ID Check Functions

        # region Register Stores
        def registerStores():
            storeID = txtStoreID.get()
            storeName = txtStoreName.get()
            storeAddress = txtStoreAddress.get()
            city = txtCity.get()
            state = txtState.get()
            zipCode = txtZip.get()

            from Model.Stores_Module import StoresModelClass
            storesModelObject = StoresModelClass(storeID=storeID, storeName=storeName,
                                                 storeAddress=storeAddress, city=city,
                                                 state=state, zip=zipCode)
            storesBLLObject = StoresBLLClass()
            storesBLLObject.registerStoresBLL(storesModelObject)

            resetForm()
            showList()
        # endregion Register Stores

        # region Back To Main Button Function
        def backToMain():
            storesForm.destroy()
            from UserInterfaceLayer.MainFormModule import MainFormClass
            mainFormObject = MainFormClass(user=self.User)
            mainFormObject.mainForm_Load()
        # endregion Back To Main Button Function

        # region Edit Stores Function
        def editStores():
            StoreID = txtStoreID.get()
            StoreName = txtStoreName.get()
            StoreAddress = txtStoreAddress.get()
            City = txtCity.get()
            State = txtState.get()
            ZipCode = txtZip.get()

            from Model.Stores_Module import StoresModelClass
            storesModelObject = StoresModelClass(storeID=StoreID, storeName=StoreName,
                                                 storeAddress=StoreAddress, city=City,
                                                 state=State, zip=ZipCode)
            storesBLLObject = StoresBLLClass()
            storesBLLObject.editStore(store=storesModelObject)

            resetForm()
            showList()
        # endregion Edit Stores Function

        # region Delete Stores Function
        def deleteStores():
            storeID = txtStoreID.get()
            if storeID is not NONE:
                storesBLLObject = StoresBLLClass()
                storesBLLObject.deleteStore(storeID)
            resetForm()
            showList()
        # endregion Delete Stores Function

        # region Delete Stores Confirmation Function
        def deleteStoresConfirmation():
            result = msg.askyesno("Confirm Delete", "Are you sure you want to delete this store?")
            if result:
                deleteStores()
        # endregion Delete Stores Confirmation Function

        # region Reset Form Function
        def resetForm():
            for widget in frameInfo.winfo_children():
                if isinstance(widget, ctk.CTkEntry):
                    widget.delete(0, ctk.END)
        # endregion Reset Form Function

        # region Store ID Validation Function
        def checkValidationStoreID(*args):
            if len(txtStoreID.get()) > 4:
                    txtStoreID.set(txtStoreID.get()[:len(txtStoreID.get()) - 1])
        # endregion Store ID Validation Function

        # region Zip Validation Function
        def checkValidationZip(*args):
            if len(txtZip.get()) > 5:
                    txtZip.set(txtZip.get()[:len(txtZip.get()) - 1])
        # endregion Zip Validation Function

        # region Show Stores List Function
        def showList(*args):
            storesBLL_Object = StoresBLLClass()
            storesList = storesBLL_Object.getStoresList()
            if len(storesList) > 0:
                tvStoresList.delete(*tvStoresList.get_children())
                rowCount = 0
                for row in storesList:
                    rowCount += 1
                    values = [rowCount]
                    for value in row:
                        if value is NONE:
                            values.append("")
                        else:
                            values.append(value)
                    tvStoresList.insert("", "end", values=values)
        # endregion Show Stores List Function

        # region On Tree Selection Function
        def onTreeSelect(event):
            resetForm()
            index = tvStoresList.selection()
            if index:
                selectedRow = tvStoresList.item(index)['values']
                txtStoreID.set(selectedRow[1])
                txtStoreName.set(selectedRow[2])
                txtStoreAddress.set(selectedRow[3])
                txtCity.set(selectedRow[4])
                txtState.set(selectedRow[5])
                txtZip.set(selectedRow[6])
        # endregion On Tree Selection Function

        # endregion Required Functions

        # region Sidebar Frame
        sidebarFrame = ctk.CTkFrame(storesForm, width=140, corner_radius=0)
        sidebarFrame.grid(row=0, column=0, rowspan=2, sticky="nsew")
        # sidebarFrame.grid_rowconfigure(4, weight=1)

        logoLabel = ctk.CTkLabel(sidebarFrame, text="PUBS", font=ctk.CTkFont(size=20, weight="bold"))
        logoLabel.grid(row=0, column=0, padx=20, pady=(20, 10))

        # region Form Name
        lblFormName = ctk.CTkLabel(sidebarFrame, text="Stores' Form")
        lblFormName.grid(row=1, column=0, padx=20, pady=10)
        # endregion Form Name

        # region Back to Main
        btnBackToMain = ctk.CTkButton(sidebarFrame, text='Back to Main', width=140, command=backToMain,
                                      text_color='#000000', corner_radius=50, hover_color='#007860',
                                      border_width=1, fg_color='#00ffc3')
        btnBackToMain.grid(row=2, column=0, padx=10, pady=10)

        # endregion Back to Main

        # region Go to Authors Form
        def authorsCRUD():
            storesForm.destroy()
            from UserInterfaceLayer.Authors_CRUD_Module import AuthorsFormClass
            authorsFormObject = AuthorsFormClass(user=self.User)
            authorsFormObject.authorsFormLoad()

        btnAuthorsCRUD = ctk.CTkButton(sidebarFrame, text="Authors' Form", width=140, command=authorsCRUD,
                                        text_color='#000000', corner_radius=50, hover_color='#007860',
                                        border_width=1, fg_color='#00ffc3')
        btnAuthorsCRUD.grid(row=3, column=0, padx=10, pady=10)

        # endregion Go to Authors Form

        # region Go to Employee Form
        def employeeCRUD():
            storesForm.destroy()
            from UserInterfaceLayer.Employee_CRUD_Module import EmployeeFormClass
            employeeFormObject = EmployeeFormClass(user=self.User)
            employeeFormObject.employeeFormLoad()

        btnEmployeeCRUD = ctk.CTkButton(sidebarFrame, text="Employees' Form", width=140, command=employeeCRUD,
                                        text_color='#000000', corner_radius=50, hover_color='#007860',
                                        border_width=1, fg_color='#00ffc3')
        btnEmployeeCRUD.grid(row=4, column=0, padx=10, pady=10)

        # endregion Go to Employee Form

        # region Go to Publishers Form
        def publishersCRUD():
            storesForm.destroy()
            from UserInterfaceLayer.Publishers_CRUD_Module import PublishersFormClass
            publishersFormObject = PublishersFormClass(user=self.User)
            publishersFormObject.publishersFormLoad()

        btnPublishersCRUD = ctk.CTkButton(sidebarFrame, text="Publishers' Form", width=140,
                                          command=publishersCRUD,
                                          text_color='#000000', corner_radius=50, hover_color='#007860',
                                          border_width=1, fg_color='#00ffc3')
        btnPublishersCRUD.grid(row=5, column=0, padx=10, pady=10)

        # endregion Go to Publishers Form

        # region Go To Jobs Form
        def jobsCRUD():
            storesForm.destroy()
            from UserInterfaceLayer.Jobs_CRUD_Module import JobsFormClass
            jobsFormObject = JobsFormClass(user=self.User)
            jobsFormObject.jobsFormLoad()

        btnJobsCRUD = ctk.CTkButton(sidebarFrame, text="Jobs' Form", width=140, command=jobsCRUD,
                                    text_color='#000000', corner_radius=50, hover_color='#007860',
                                    border_width=1, fg_color='#00ffc3')
        btnJobsCRUD.grid(row=6, column=0, padx=10, pady=10)

        # endregion Go To Jobs Form

        # region Go To Sales Form
        def salesCRUD():
            storesForm.destroy()
            from UserInterfaceLayer.Sales_CRUD_Module import SalesFormClass
            salesFormObject = SalesFormClass(user=self.User)
            salesFormObject.salesFormLoad()

        btnSalesCRUD = ctk.CTkButton(sidebarFrame, text="Sales' Form", width=140, command=salesCRUD,
                                     text_color='#000000', corner_radius=50, hover_color='#007860',
                                     border_width=1, fg_color='#00ffc3')
        btnSalesCRUD.grid(row=7, column=0, padx=10, pady=10)

        # endregion Go To Sales Form

        # region Go To Titles Form
        def titlesCRUD():
            storesForm.destroy()
            from UserInterfaceLayer.Titles_CRUD_Module import TitlesFormClass
            titlesFormObject = TitlesFormClass(user=self.User)
            titlesFormObject.titlesFormLoad()

        btnTitlesCRUD = ctk.CTkButton(sidebarFrame, text="Titles' Form", width=140, command=titlesCRUD,
                                      text_color='#000000', corner_radius=50, hover_color='#007860',
                                      border_width=1, fg_color='#00ffc3')
        btnTitlesCRUD.grid(row=8, column=0, padx=10, pady=10)
        # endregion Go To Titles Form

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

        # region Treeview Frame
        frmTV = ctk.CTkFrame(storesForm)
        frmTV.grid(row=0, column=2, padx=0, pady=10, ipadx=0, ipady=10, sticky=NSEW)

        # region Treeview Label
        lblTreeViewPrompt = ctk.CTkLabel(frmTV, text_color='#616161', font=("Helvetica", 12),
                                         text="View List")
        lblTreeViewPrompt.grid(row=0, column=0, padx=10, pady=0, sticky='w')
        # endregion Treeview Label

        # region Columns
        _columns = ['Index', 'StoreID', 'StoreName', 'StoreAddress', 'City', 'State', 'Zip']
        _displayColumns = ['Index', 'StoreID', 'StoreName', 'StoreAddress', 'City', 'State', 'Zip']
        # endregion Columns

        # region Treeview Widgets
        tvStoresList = ttk.Treeview(frmTV, columns=_columns, displaycolumns=_displayColumns,
                                  show='headings', selectmode='browse', height=15)
        tvStoresList.grid(row=1, column=0, padx=10, pady=10, sticky=NSEW)

        tvStoresList.bind('<<TreeviewSelect>>', onTreeSelect)

        tvStoresList.column('#0', width=0)

        tvStoresList.column(column='Index', width=50)
        tvStoresList.heading(text='Index', column='Index')

        tvStoresList.column(column='StoreID', width=100)
        tvStoresList.heading(text='StoreID', column='StoreID')

        tvStoresList.column(column='StoreName', width=100)
        tvStoresList.heading(text='StoreName', column='StoreName')

        tvStoresList.column(column='StoreAddress', width=150)
        tvStoresList.heading(text='StoreAddress', column='StoreAddress')

        tvStoresList.column(column='City', width=80)
        tvStoresList.heading(text='City', column='City')

        tvStoresList.column(column='State', width=50)
        tvStoresList.heading(text='State', column='State')

        tvStoresList.column(column='Zip', width=80)
        tvStoresList.heading(text='Zip', column='Zip')
        # endregion Treeview Widgets

        # endregion Treeview Frame

        # region Stores' Information Frame
        frameInfo = ctk.CTkFrame(storesForm)
        frameInfo.grid(row=0, column=1, padx=10, pady=0, ipadx=10, ipady=10)

        # region Frame Info Label
        lblFrameInfoPrompt = ctk.CTkLabel(frameInfo, text_color='#616161', font=("Helvetica", 12),
                                          text="Stores' Information")
        lblFrameInfoPrompt.grid(row=0, column=0, padx=10, pady=0, sticky='w')
        # endregion Frame Info Label

        # region Store ID
        lblStoreID = ctk.CTkLabel(frameInfo, text='Store ID: ')
        lblStoreID.grid(row=1, column=0, padx=10, pady=10, sticky='w')

        txtStoreID = StringVar()
        txtStoreID.trace('w', checkValidationStoreID)
        entStoreID = ctk.CTkEntry(frameInfo, width=280, textvariable=txtStoreID, corner_radius=50,
                                border_width=1, border_color='#FFFFFF')
        entStoreID.grid(row=1, column=1, padx=10, pady=10, sticky='w')
        # endregion Store ID

        # region Store Name
        lblStoreName = ctk.CTkLabel(frameInfo, text='Store Name: ')
        lblStoreName.grid(row=2, column=0, padx=10, pady=10, sticky='w')

        txtStoreName = StringVar()
        entStoreName = ctk.CTkEntry(frameInfo, width=280, textvariable=txtStoreName, corner_radius=50,
                                  border_width=1, border_color='#FFFFFF')
        entStoreName.grid(row=2, column=1, padx=10, pady=10, sticky='w')
        # endregion Store Name

        # region Store Address
        lblStoreAddress = ctk.CTkLabel(frameInfo, text='Store Address: ')
        lblStoreAddress.grid(row=3, column=0, padx=10, pady=10, sticky='w')

        txtStoreAddress = StringVar()
        entStoreAddress = ctk.CTkEntry(frameInfo, width=280, textvariable=txtStoreAddress, corner_radius=50,
                               border_width=1, border_color='#FFFFFF')
        entStoreAddress.grid(row=3, column=1, padx=10, pady=10, sticky='w')
        # endregion Store Address

        # region City
        lblCity = ctk.CTkLabel(frameInfo, text='City: ')
        lblCity.grid(row=4, column=0, padx=10, pady=10, sticky='w')

        txtCity = StringVar()
        entCity = ctk.CTkEntry(frameInfo, width=280, textvariable=txtCity, corner_radius=50,
                                border_width=1, border_color='#FFFFFF')
        entCity.grid(row=4, column=1, padx=10, pady=10, sticky='w')
        # endregion City

        # region State
        statesList = [
            "AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA",
            "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD",
            "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ",
            "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC",
            "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"
        ]
        lblState = ctk.CTkLabel(frameInfo, text='State: ')
        lblState.grid(row=5, column=0, padx=10, pady=10, sticky='w')

        txtState = StringVar()
        cmdState = ctk.CTkComboBox(frameInfo, width=280, values=statesList, state='readonly',
                                   corner_radius=50, border_width=1, border_color='#FFFFFF', variable=txtState)
        cmdState.grid(row=5, column=1, padx=10, pady=10)
        # endregion State

        # region Zip
        lblZip = ctk.CTkLabel(frameInfo, text='Zipcode: ')
        lblZip.grid(row=6, column=0, padx=10, pady=10, sticky='w')

        txtZip = StringVar()
        txtZip.trace('w', checkValidationZip)
        entZip = ctk.CTkEntry(frameInfo, width=280, textvariable=txtZip, corner_radius=50,
                                  border_width=1, border_color='#FFFFFF')
        entZip.grid(row=6, column=1, padx=10, pady=10, sticky='w')
        # endregion Zip

        #region Register Stores Button
        btnRegister = ctk.CTkButton(frameInfo, text='Register Store', width=130, command=duplicateIDCheckRegister,
                                    text_color='#000000', corner_radius=50, hover_color='#007860',
                                    border_width=1, fg_color='#00ffc3')
        btnRegister.grid(row=7, column=1, padx=10, pady=20, sticky='e')
        #endregion Register Stores Button

        #region Edit Stores Button
        btnEditStores = ctk.CTkButton(frameInfo, text='Edit Store', width=130, command=duplicateIDCheckEdit,
                                      text_color = '#000000', corner_radius = 50, hover_color = '#007860',
                                      border_width = 1, fg_color = '#00ffc3')
        btnEditStores.grid(row=7, column=1, padx=10, pady=20, sticky='w')
        #endregion Edit Stores Button

        #region Reset Form Button
        btnResetForm = ctk.CTkButton(frameInfo, text='Clear Form', width=130, command=resetForm,
                                      text_color = '#000000', corner_radius = 50, hover_color = '#007860',
                                      border_width = 1, fg_color = '#00ffc3')
        btnResetForm.grid(row=8, column=1, padx=10, pady=(10, 20), sticky='w')
        #endregion Reset Form Button

        #region Delete Stores Button
        btnDeleteStores = ctk.CTkButton(frameInfo, text='Delete Store', width=130, command=deleteStoresConfirmation,
                                      text_color = '#000000', corner_radius = 50, hover_color = '#910024',
                                      border_width = 1, fg_color = '#ff0040')
        btnDeleteStores.grid(row=8, column=1, padx=10, pady=(10, 20), sticky='e')
        #endregion Delete Stores Button

        # endregion Stores' Information Frame

        updateTreeviewStyle()
        showList()
        storesForm.after(0, setClock)
        storesForm.mainloop()