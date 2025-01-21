from tkinter import *
import customtkinter as ctk
from Model.UserModel import UserModelClass
from datetime import datetime
from BusinessLogicLayer.Sales_BLL_Module import SalesBLLClass
from tkinter import ttk
from tkinter import messagebox as msg
from Utility.Date_Picker_Module import CustomDatePicker

class SalesFormClass:
    def __init__(self, user: UserModelClass):
        self.User = user

    def salesFormLoad(self):
        salesForm = ctk.CTk()
        salesForm.title('Sales CRUD Form')
        salesForm.geometry('1330x465')
        salesForm.iconbitmap('Images/page.ico')
        salesForm.resizable(False, False)
        x = int((salesForm.winfo_screenwidth() / 2) - (1330 / 2))
        y = int((salesForm.winfo_screenheight() / 2) - (465 / 2))
        salesForm.geometry('+{}+{}'.format(x, y))

        # region Required Functions

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

        # region Date and time Function
        def setClock():
            currentDateTime = datetime.today()
            currentDateTime = currentDateTime.strftime('%Y/%m/%d  %H:%M:%S')
            txtCurrentDateTime.set(f'{currentDateTime}')
            salesForm.after(1000, setClock)

        # endregion Date and time Function

        # region Reset Form Function
        def resetForm():
            for widget in frameInfo.winfo_children():
                if isinstance(widget, ctk.CTkEntry):
                    widget.delete(0, ctk.END)
        # endregion Reset Form Function

        # region Get Stores Name List Function
        storesNamesList = dict()
        def getStoreNamesList():
            salesBLLObject = SalesBLLClass()
            rows = salesBLLObject.getStoreNameListBLL()
            for row in rows:
                if row[1] not in storesNamesList:
                    storesNamesList[row[1]] = row[0]
            return storesNamesList

        storesNamesListDictionary = getStoreNamesList()
        reversedStoresNamesListDictionary = {v:k for k, v in storesNamesListDictionary.items()}
        # endregion Get Stores Name List Function

        # region Get Titles Names List Function
        titlesNamesList = dict()
        def getTitlesNamesList():
            salesBLLObject = SalesBLLClass()
            rows = salesBLLObject.getTitleNameListBLL()
            for row in rows:
                if row[1] not in titlesNamesList:
                    titlesNamesList[row[1]] = row[0]
            return titlesNamesList

        titlesNamesListDictionary = getTitlesNamesList()
        reversedTitlesNamesListDictionary = {v:k for k, v in titlesNamesListDictionary.items()}
        # endregion Get Titles Names List Function

        # region Show Sales List Function
        def showList():
            salesBLL_Object = SalesBLLClass()
            salesList = salesBLL_Object.getSalesListBLL()
            if len(salesList) > 0:
                tvSalesList.delete(*tvSalesList.get_children())
                rowCount = 0
                for row in salesList:
                    rowCount += 1
                    values = [rowCount]
                    for value in row:
                        if value is NONE:
                            values.append("")
                        else:
                            values.append(value)
                    keyStoreName = reversedStoresNamesListDictionary.get(values[1])
                    values[1] = keyStoreName

                    keyTitleName = reversedTitlesNamesListDictionary.get(values[6])
                    values[6] = keyTitleName

                    tvSalesList.insert("", "end", values=values)
        # endregion Show Sales List Function

        # region On Tree Selection Function
        def onTreeSelect(event):
            resetForm()
            index = tvSalesList.selection()
            if index:
                selectedRow = tvSalesList.item(index)['values']
                txtStoreName.set(selectedRow[1])
                txtOrderNumber.set(selectedRow[2])
                txtOrderDate.set(selectedRow[3])
                txtQuantity.set(selectedRow[4])
                txtPayTerms.set(selectedRow[5])
                txtTitleName.set(selectedRow[6])
        # endregion On Tree Selection Function

        # region Order Number Validation Function
        def checkValidationOrderNumber(*args):
            if len(txtOrderNumber.get()) > 20:
                txtOrderNumber.set(txtOrderNumber.get()[:len(txtOrderNumber.get()) - 1])
        # endregion Order Number Validation Function

        # region Delete Sales Function
        def deleteSales():
            storeID = storesNamesListDictionary[txtStoreName.get()]
            orderNum = txtOrderNumber.get()
            titleID = titlesNamesListDictionary[txtTitleName.get()]
            if storeID is not NONE and orderNum is not NONE and titleID is not NONE:
                employeeBLL = SalesBLLClass()
                employeeBLL.deleteSaleBLL(storeID=storeID, orderNum=orderNum, titleID=titleID)
            resetForm()
            showList()
        # endregion Delete Sales Function

        # region Delete Sales Confirmation Function
        def deleteSalesConfirmation():
            result = msg.askyesno("Confirm Delete", "Are you sure you want to delete this sale?")
            if result:
                deleteSales()
        # endregion Delete Sales Confirmation Function

        # region Duplicate ID Check Functions
        def getStoresID():
            salesBLLObject = SalesBLLClass()
            rows = salesBLLObject.getStoresIDSalesBLLL()
            storesIDList = [row[0] for row in rows]
            return storesIDList

        storesID = getStoresID()

        def getTitlesID():
            salesBLLObject = SalesBLLClass()
            rows = salesBLLObject.getTitlesIDSalesBLL()
            titlesIDList = [row[0] for row in rows]
            return titlesIDList

        titlesID = getTitlesID()

        def getOrderNumber():
            salesBLLObject = SalesBLLClass()
            rows = salesBLLObject.getOrderNumberSalesBLL()
            orderNumbersList = [row[0] for row in rows]
            return orderNumbersList

        orderNumbers = getOrderNumber()

        def duplicateIDCheckRegister():
            if txtOrderNumber.get() in orderNumbers:
                msg.showerror("Error", "Duplicate Order Number!")
            else:
                registerSales()

        def duplicateIDCheckEdit():
            if txtOrderNumber.get() not in orderNumbers or storesNamesListDictionary[
                txtStoreName.get()] not in storesID or titlesNamesListDictionary[
                txtTitleName.get()] not in titlesID:
                msg.showerror("Error", "Store Name, Order Number and Title Name must remain the same!")
            else:
                editSales()

        # endregion Duplicate ID Check Functions

        # region Register Sales
        def registerSales():
            storeID = storesNamesListDictionary[txtStoreName.get()]
            orderNumber = txtOrderNumber.get()
            orderDate = txtOrderDate.get()
            quantity = int(txtQuantity.get())
            payTerms = txtPayTerms.get()
            titleID = titlesNamesListDictionary[txtTitleName.get()]

            from Model.Sales_Module import SalesModelClass
            salesModelObject = SalesModelClass(storeID=storeID, orderNum=orderNumber, orderDate=orderDate,
                                                 qty=quantity, payTerms=payTerms, titleID=titleID)
            salesBLLObject = SalesBLLClass()
            salesBLLObject.registerSalesBLL(sale=salesModelObject)

            resetForm()
            showList()
        # endregion Register Sales

        # region Back To Main Button Function
        def backToMain():
            salesForm.destroy()
            from UserInterfaceLayer.MainFormModule import MainFormClass
            mainFormObject = MainFormClass(user=self.User)
            mainFormObject.mainForm_Load()
        # endregion Back To Main Button Function

        # region Edit Sales Function
        def editSales():
            storeID = storesNamesListDictionary[txtStoreName.get()]
            orderNumber = txtOrderNumber.get()
            orderDate = txtOrderDate.get()
            quantity = int(txtQuantity.get())
            payTerms = txtPayTerms.get()
            titleID = titlesNamesListDictionary[txtTitleName.get()]

            from Model.Sales_Module import SalesModelClass
            salesModelObject = SalesModelClass(storeID=storeID, orderNum=orderNumber, orderDate=orderDate,
                                               qty=quantity, payTerms=payTerms, titleID=titleID)
            salesBLLObject = SalesBLLClass()
            salesBLLObject.editSalesBLL(sale=salesModelObject)

            resetForm()
            showList()
        # endregion Edit Sales Function

        # endregion Required Functions

        # region Sidebar Frame
        sidebarFrame = ctk.CTkFrame(salesForm, width=140, corner_radius=0)
        sidebarFrame.grid(row=0, column=0, rowspan=2, sticky="nsew")
        # sidebarFrame.grid_rowconfigure(4, weight=1)

        logoLabel = ctk.CTkLabel(sidebarFrame, text="PUBS", font=ctk.CTkFont(size=20, weight="bold"))
        logoLabel.grid(row=0, column=0, padx=20, pady=(20, 10))

        # region Form Name
        lblFormName = ctk.CTkLabel(sidebarFrame, text="Sales' Form")
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
            salesForm.destroy()
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
            salesForm.destroy()
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
            salesForm.destroy()
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
            salesForm.destroy()
            from UserInterfaceLayer.Jobs_CRUD_Module import JobsFormClass
            jobsFormObject = JobsFormClass(user=self.User)
            jobsFormObject.jobsFormLoad()

        btnJobsCRUD = ctk.CTkButton(sidebarFrame, text="Jobs' Form", width=140, command=jobsCRUD,
                                    text_color='#000000', corner_radius=50, hover_color='#007860',
                                    border_width=1, fg_color='#00ffc3')
        btnJobsCRUD.grid(row=6, column=0, padx=10, pady=10)

        # endregion Go To Jobs Form

        # region Go To Stores Form
        def storesCRUD():
            salesForm.destroy()
            from UserInterfaceLayer.Stores_CRUD_Module import StoresFormClass
            storesFormObject = StoresFormClass(user=self.User)
            storesFormObject.storesFormLoad()

        btnStoresCRUD = ctk.CTkButton(sidebarFrame, text="Stores' Form", width=140, command=storesCRUD,
                                      text_color='#000000', corner_radius=50, hover_color='#007860',
                                      border_width=1, fg_color='#00ffc3')
        btnStoresCRUD.grid(row=7, column=0, padx=10, pady=10)

        # endregion Go To Stores Form

        # region Go To Titles Form
        def titlesCRUD():
            salesForm.destroy()
            from UserInterfaceLayer.Titles_CRUD_Module import TitlesFormClass
            titlesFormObject = TitlesFormClass(user=self.User)
            titlesFormObject.titlesFormLoad()

        btnTitlesCRUD = ctk.CTkButton(sidebarFrame, text="Titles' Form", width=140, command=titlesCRUD,
                                      text_color='#000000', corner_radius=50, hover_color='#007860',
                                      border_width=1, fg_color='#00ffc3')
        btnTitlesCRUD.grid(row=8, column=0, padx=10, pady=0)
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
        frmTV = ctk.CTkFrame(salesForm)
        frmTV.grid(row=0, column=2, padx=0, pady=10, ipadx=0, ipady=10, sticky=NSEW)

        # region Treeview Label
        lblTreeViewPrompt = ctk.CTkLabel(frmTV, text_color='#616161', font=("Helvetica", 12),
                                         text="View List")
        lblTreeViewPrompt.grid(row=0, column=0, padx=10, pady=0, sticky='w')
        # endregion Treeview Label

        # region Columns
        _columns = ['Index', 'StoreName', 'OrderNumber', 'OrderDate', 'Quantity', 'PayTerms', 'TitleName']
        _displayColumns = ['Index', 'StoreName', 'OrderNumber', 'OrderDate', 'Quantity', 'PayTerms', 'TitleName']
        # endregion Columns

        # region Treeview Widgets
        tvSalesList = ttk.Treeview(frmTV, columns=_columns, displaycolumns=_displayColumns,
                                  show='headings', selectmode='browse', height=20)
        tvSalesList.grid(row=1, column=0, padx=10, pady=10, sticky=NSEW)

        tvSalesList.bind('<<TreeviewSelect>>', onTreeSelect)

        tvSalesList.column('#0', width=0)

        tvSalesList.column(column='Index', width=50)
        tvSalesList.heading(text='Index', column='Index')

        tvSalesList.column(column='StoreName', width=200)
        tvSalesList.heading(text='StoreName', column='StoreName')

        tvSalesList.column(column='OrderNumber', width=100)
        tvSalesList.heading(text='OrderNumber', column='OrderNumber')

        tvSalesList.column(column='OrderDate', width=80)
        tvSalesList.heading(text='OrderDate', column='OrderDate')

        tvSalesList.column(column='Quantity', width=50)
        tvSalesList.heading(text='Quantity', column='Quantity')

        tvSalesList.column(column='PayTerms', width=80)
        tvSalesList.heading(text='PayTerms', column='PayTerms')

        tvSalesList.column(column='TitleName', width=300)
        tvSalesList.heading(text='TitleName', column='TitleName')
        # endregion Treeview Widgets

        # endregion Treeview Frame

        # region Sales' Information Frame
        frameInfo = ctk.CTkFrame(salesForm)
        frameInfo.grid(row=0, column=1, padx=10, pady=0, ipadx=10, ipady=10)

        # region Frame Info Label
        lblFrameInfoPrompt = ctk.CTkLabel(frameInfo, text_color='#616161', font=("Helvetica", 12),
                                          text="Sales' Information")
        lblFrameInfoPrompt.grid(row=0, column=0, padx=10, pady=0, sticky='w')
        # endregion Frame Info Label

        # region Store Name
        lblStoreName = ctk.CTkLabel(frameInfo, text='Store Name: ')
        lblStoreName.grid(row=1, column=0, padx=10, pady=10, sticky='w')

        txtStoreName = StringVar()
        cmbStoreName = ctk.CTkComboBox(frameInfo, width=280, values=list(getStoreNamesList().keys()), state='readonly',
                                               corner_radius=50, border_width=1, border_color='#FFFFFF',
                                               variable=txtStoreName)
        cmbStoreName.grid(row=1, column=1, padx=10, pady=10, sticky='w')
        # endregion Store Name

        # region Order Number
        lblOrderNumber = ctk.CTkLabel(frameInfo, text='Order Number: ')
        lblOrderNumber.grid(row=2, column=0, padx=10, pady=10, sticky='w')

        txtOrderNumber = StringVar()
        txtOrderNumber.trace('w', checkValidationOrderNumber)
        entOrderNumber = ctk.CTkEntry(frameInfo, width=280, textvariable=txtOrderNumber, corner_radius=50,
                                  border_width=1, border_color='#FFFFFF')
        entOrderNumber.grid(row=2, column=1, padx=10, pady=10, sticky='w')
        # endregion Order Number

        # region OrderDate
        lblOrderDate = ctk.CTkLabel(frameInfo, text='OrderDate: ')
        lblOrderDate.grid(row=3, column=0, padx=10, pady=10, sticky='w')

        txtOrderDate = StringVar()
        entOrderDate = ctk.CTkEntry(frameInfo, width=280, textvariable=txtOrderDate, corner_radius=50,
                                    border_width=1, border_color='#FFFFFF')
        entOrderDate.grid(row=3, column=1, padx=10, pady=10, sticky=EW)

        datePicker = CustomDatePicker(frameInfo, txtOrderDate)
        entOrderDate.bind("<Button-1>", lambda e: datePicker.openDatePicker())
        # endregion OrderDate

        # region Quantity
        lblQuantity = ctk.CTkLabel(frameInfo, text='Quantity: ')
        lblQuantity.grid(row=4, column=0, padx=10, pady=10, sticky='w')

        txtQuantity = StringVar()
        entQuantity = ctk.CTkEntry(frameInfo, width=280, textvariable=txtQuantity, corner_radius=50,
                                border_width=1, border_color='#FFFFFF')
        entQuantity.grid(row=4, column=1, padx=10, pady=10, sticky='w')
        # endregion Quantity

        # region PayTerms
        lblPayTerms = ctk.CTkLabel(frameInfo, text='Pay Terms: ')
        lblPayTerms.grid(row=5, column=0, padx=10, pady=10, sticky='w')

        txtPayTerms = StringVar()
        entPayTerms = ctk.CTkEntry(frameInfo, width=280, textvariable=txtPayTerms, corner_radius=50,
                                  border_width=1, border_color='#FFFFFF')
        entPayTerms.grid(row=5, column=1, padx=10, pady=10, sticky='w')
        # endregion PayTerms

        # region TitleName
        lblTitleName = ctk.CTkLabel(frameInfo, text='Title Name: ')
        lblTitleName.grid(row=6, column=0, padx=10, pady=10, sticky='w')

        txtTitleName = StringVar()
        cmbTitleName = ctk.CTkComboBox(frameInfo, width=280, values=list(getTitlesNamesList().keys()), state='readonly',
                                               corner_radius=50, border_width=1, border_color='#FFFFFF',
                                               variable=txtTitleName)
        cmbTitleName.grid(row=6, column=1, padx=10, pady=10, sticky='w')
        # endregion TitleName

        #region Register Sales Button
        btnRegister = ctk.CTkButton(frameInfo, text='Register Sale', width=130, command=duplicateIDCheckRegister,
                                    text_color='#000000', corner_radius=50, hover_color='#007860',
                                    border_width=1, fg_color='#00ffc3')
        btnRegister.grid(row=7, column=1, padx=10, pady=(20, 20), sticky='e')
        #endregion Register Sales Button

        #region Edit Sales Button
        btnEditSales = ctk.CTkButton(frameInfo, text='Edit Sale', width=130, command=duplicateIDCheckEdit,
                                      text_color = '#000000', corner_radius = 50, hover_color = '#007860',
                                      border_width = 1, fg_color = '#00ffc3')
        btnEditSales.grid(row=7, column=1, padx=10, pady=(20, 20), sticky='w')
        #endregion Edit Publisher Button

        #region Reset Form
        btnResetForm = ctk.CTkButton(frameInfo, text='Clear Form', width=130, command=resetForm,
                                      text_color = '#000000', corner_radius = 50, hover_color = '#007860',
                                      border_width = 1, fg_color = '#00ffc3')
        btnResetForm.grid(row=8, column=1, padx=10, pady=10, sticky='w')
        #endregion Reset Form

        #region Delete Sales Button
        btnDeleteSales = ctk.CTkButton(frameInfo, text='Delete Sale', width=130, command=deleteSalesConfirmation,
                                      text_color = '#000000', corner_radius = 50, hover_color = '#910024',
                                      border_width = 1, fg_color = '#ff0040')
        btnDeleteSales.grid(row=8, column=1, padx=10, pady=10, sticky='e')
        #endregion Delete Sales Button

        # endregion Sales' Information Frame

        updateTreeviewStyle()
        showList()
        salesForm.after(0, setClock)
        salesForm.mainloop()