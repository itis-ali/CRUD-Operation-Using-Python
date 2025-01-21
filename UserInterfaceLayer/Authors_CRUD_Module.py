from tkinter import *
import customtkinter as ctk
from Model.UserModel import UserModelClass
from BusinessLogicLayer.Authors_BLL_Module import AuthorsBLLClass
from datetime import datetime
from tkinter import ttk
from tkinter import messagebox as msg
import re

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class AuthorsFormClass:
    def __init__(self, user: UserModelClass):
        self.User = user

    def authorsFormLoad(self):
        authorsForm = ctk.CTk()
        authorsForm.title('Authors CRUD Form')
        authorsForm.geometry('1405x600')
        authorsForm.iconbitmap('Images/page.ico')
        authorsForm.resizable(False, False)
        x = int((authorsForm.winfo_screenwidth() / 2) - (1405 / 2))
        y = int((authorsForm.winfo_screenheight() / 2) - (600 / 2))
        authorsForm.geometry('+{}+{}'.format(x, y))

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

        # region Duplicate ID Check Functions
        def getEmployeeID():
            authorBLLObject = AuthorsBLLClass()
            rows = authorBLLObject.getAuthorIDBLL()
            authorIDList = [row[0] for row in rows]
            return authorIDList

        employeeID = getEmployeeID()

        def duplicateIDCheckRegister():
            if txtAuthorID.get() in employeeID:
                msg.showerror("Error", "Duplicate Author ID!")
            else:
                registerAuthor()

        def duplicateIDCheckEdit():
            if txtAuthorID.get() not in employeeID:
                msg.showerror("Error", "Author ID must remain the same!")
            else:
                editAuthor()

        # endregion Duplicate ID Check Functions

        # region Register Button Function
        def registerAuthor():
            auId = txtAuthorID.get()
            patternAuthorID = re.compile(r"^\d{3}-\d{2}-\d{4}$")
            authorID = auId if patternAuthorID.match(auId) else msg.showerror('Error',
                                                                              'Invalid Author ID Format!\nExpected: 111-11-1111')
            # repeated ID check////////////////////////////////////////////////////////////////
            firstName = txtFirstName.get()
            lastName = txtLastName.get()
            pNumber = txtPhoneNumber.get()
            patternPhoneNumber = re.compile(r"^\d{12}")
            phoneNumber = pNumber if patternPhoneNumber.match(pNumber) else msg.showerror('Error',
                                                                                          'Invalid Phone Number!')
            address = txtAddress.get()
            city = txtCity.get()
            state = txtState.get()
            zipCode = txtZipCode.get()
            contract = intContract.get()

            from Model.Authors_Module import AuthorsModelClass
            authorsModelObject = AuthorsModelClass(auID=authorID, fname=firstName, lname=lastName,
                                                   pnum=phoneNumber, addrss=address, cty=city,
                                                   stte=state, zcode=zipCode, cntrct=contract)
            authorsBLLObject = AuthorsBLLClass()
            authorsBLLObject.registerAuthorsBLL(authorsModelObject)

            resetForm()
        # endregion Register Button Function

        # region Back To Main Button Function
        def backToMain():
            authorsForm.destroy()
            from UserInterfaceLayer.MainFormModule import MainFormClass
            mainFormObject = MainFormClass(user=self.User)
            mainFormObject.mainForm_Load()
        # endregion Back To Main Button Function

        # region Edit Author Function
        def editAuthor():
            AuthorID = txtAuthorID.get()
            FirstName = txtFirstName.get()
            LastName = txtLastName.get()
            PhoneNumber = txtPhoneNumber.get()
            Address = txtAddress.get()
            City = txtCity.get()
            State = txtState.get()
            ZipCode = txtZipCode.get()
            contract = None
            if intContract.get() == 1:
                contract = 1
            elif intContract.get() == 0:
                contract = 0
            Contract = contract
            from Model.Authors_Module import AuthorsModelClass
            authorObject = AuthorsModelClass(auID=AuthorID, fname=FirstName, lname=LastName,
                                             pnum=PhoneNumber, addrss=Address, cty=City,
                                             stte=State, zcode=ZipCode, cntrct=Contract)
            authorBLLObject = AuthorsBLLClass()
            authorBLLObject.editAuthor(author=authorObject)

            resetForm()
            showList()
        # endregion Edit Author Function

        # region Delete Author Function
        def deleteAuthor():
            auID = txtAuthorID.get()
            if auID is not NONE:
                employeeBLL_Object = AuthorsBLLClass()
                employeeBLL_Object.deleteAuthor(auID)
            resetForm()
            showList()
        # endregion Delete Author Function

        # region Delete Sales Confirmation Function
        def deleteAuthorConfirmation():
            result = msg.askyesno("Confirm Delete", "Are you sure you want to delete this author?")
            if result:
                deleteAuthor()
        # endregion Delete Sales Confirmation Function

        # region Author ID Validation Function
        def checkValidationAuthorID(*args):
            if len(txtAuthorID.get()) > 11:
                txtAuthorID.set(txtAuthorID.get()[:len(txtAuthorID.get()) - 1])

            for char in txtAuthorID.get():
                if not char.isnumeric() and char != '-':
                    txtAuthorID.set(txtAuthorID.get().replace(char, ''))
        # endregion Author ID Validation Function

        # region Phone Number Validation Function
        def checkValidationPhoneNumber(*args):
            if len(txtPhoneNumber.get()) > 12:
                txtPhoneNumber.set(txtPhoneNumber.get()[:len(txtPhoneNumber.get()) - 1])

            for char in txtPhoneNumber.get():
                if not char.isnumeric() and char != '-' and char != ' ':
                    txtPhoneNumber.set(txtPhoneNumber.get().replace(char, ''))
        # endregion Phone Number Validation Function

        # region Zip Code Validation Function
        def checkValidationZipCode(*args):
            if len(txtZipCode.get()) > 5:
                txtZipCode.set(txtZipCode.get()[:len(txtZipCode.get()) - 1])

            for char in txtZipCode.get():
                if not char.isnumeric():
                    txtZipCode.set(txtZipCode.get().replace(char, ''))
        # endregion Zip Code Validation Function

        # region Reset Form Function
        def resetForm():
            for widget in frameInfo.winfo_children():
                if isinstance(widget, ctk.CTkEntry):
                    widget.delete(0, ctk.END)
        # endregion Reset Form Function

        # region Date and time Function
        def setClock():
            currentDateTime = datetime.today()
            currentDateTime = currentDateTime.strftime('%Y/%m/%d  %H:%M:%S')
            txtCurrentDateTime.set(f'{currentDateTime}')
            authorsForm.after(1000, setClock)
        # endregion Date and time Function

        # region Treeview On Tree Selection Function
        def onTreeSelect(event):
            resetForm()
            index = tvAuthorsList.selection()
            if index:
                selectedRow = tvAuthorsList.item(index)['values']
                txtAuthorID.set(selectedRow[1])
                txtFirstName.set(selectedRow[2])
                txtLastName.set(selectedRow[3])
                txtPhoneNumber.set(selectedRow[4])
                txtAddress.set(selectedRow[5])
                txtCity.set(selectedRow[6])
                txtState.set(selectedRow[7])
                txtZipCode.set(selectedRow[8])
                contract = selectedRow[9]
                if contract == True:
                    intContract.set(1)
                elif contract == False:
                    intContract.set(0)
        # endregion Treeview On Tree Selection Function

        # region Show Authors' List Function
        def showList(*args):
            authorsBLL_Object = AuthorsBLLClass()
            authorsList = authorsBLL_Object.getAuthorsList()
            if len(authorsList) > 0:
                tvAuthorsList.delete(*tvAuthorsList.get_children())
                rowCount = 0
                for row in authorsList:
                    rowCount += 1
                    values = [rowCount]
                    for value in row:
                        if value is NONE:
                            values.append("")
                        else:
                            values.append(value)
                    tvAuthorsList.insert("", "end", values=values)
        # endregion Show Authors' List Function

        # region Search Function ////////////////////////////////// Review Needed
        # def filterTreeview():
        #     query = txtSearch.get().lower()
        #     for item in tvAuthorsList.get_children():
        #         itemText = tvAuthorsList.item(item, "text").lower()
        #         if query in itemText:
        #             tvAuthorsList.selection_set(item)
        #             tvAuthorsList.see(item)
        #             break
        #         else:
        #             msg.showinfo("Search result", "No match found.")
        # endregion Search Function
        # endregion Required Functions

        # region Sidebar Frame
        sidebarFrame = ctk.CTkFrame(authorsForm, width=140, corner_radius=0)
        sidebarFrame.grid(row=0, column=0, rowspan=2, sticky="nsew")
        # sidebarFrame.grid_rowconfigure(4, weight=1)

        logoLabel = ctk.CTkLabel(sidebarFrame, text="PUBS", font=ctk.CTkFont(size=20, weight="bold"))
        logoLabel.grid(row=0, column=0, padx=20, pady=(20, 10))

        # region Form Name
        lblFormName = ctk.CTkLabel(sidebarFrame, text="Authors' Form")
        lblFormName.grid(row=1, column=0, padx=20, pady=10)
        # endregion Form Name

        # region Back to Main
        btnBackToMain = ctk.CTkButton(sidebarFrame, text='Back to Main', width=140, command=backToMain,
                                      text_color='#000000', corner_radius=50, hover_color='#007860',
                                      border_width=1, fg_color='#00ffc3')
        btnBackToMain.grid(row=2, column=0, padx=10, pady=10)
        # endregion Back to Main

        # region Go to Employee Form
        def employeeCRUD():
            authorsForm.destroy()
            from UserInterfaceLayer.Employee_CRUD_Module import EmployeeFormClass
            employeeFormObject = EmployeeFormClass(user=self.User)
            employeeFormObject.employeeFormLoad()

        btnEmployeeCRUD = ctk.CTkButton(sidebarFrame, text="Employees' Form", width=140, command=employeeCRUD,
                                      text_color='#000000', corner_radius=50, hover_color='#007860',
                                      border_width=1, fg_color='#00ffc3')
        btnEmployeeCRUD.grid(row=3, column=0, padx=10, pady=10)
        # endregion Go to Employee Form

        # region Go to Publishers Form
        def publishersCRUD():
            authorsForm.destroy()
            from UserInterfaceLayer.Publishers_CRUD_Module import PublishersFormClass
            publishersFormObject = PublishersFormClass(user=self.User)
            publishersFormObject.publishersFormLoad()

        btnPublishersCRUD = ctk.CTkButton(sidebarFrame, text="Publishers' Form", width=140, command=publishersCRUD,
                                      text_color='#000000', corner_radius=50, hover_color='#007860',
                                      border_width=1, fg_color='#00ffc3')
        btnPublishersCRUD.grid(row=4, column=0, padx=10, pady=10)
        # endregion Go to Publishers Form

        # region Go To Jobs Form
        def jobsCRUD():
            authorsForm.destroy()
            from UserInterfaceLayer.Jobs_CRUD_Module import JobsFormClass
            jobsFormObject = JobsFormClass(user=self.User)
            jobsFormObject.jobsFormLoad()

        btnJobsCRUD = ctk.CTkButton(sidebarFrame, text="Jobs' Form", width=140, command=jobsCRUD,
                                      text_color='#000000', corner_radius=50, hover_color='#007860',
                                      border_width=1, fg_color='#00ffc3')
        btnJobsCRUD.grid(row=5, column=0, padx=10, pady=10)
        # endregion Go To Jobs Form

        # region Go To Sales Form
        def salesCRUD():
            authorsForm.destroy()
            from UserInterfaceLayer.Sales_CRUD_Module import SalesFormClass
            salesFormObject = SalesFormClass(user=self.User)
            salesFormObject.salesFormLoad()

        btnSalesCRUD = ctk.CTkButton(sidebarFrame, text="Sales' Form", width=140, command=salesCRUD,
                                      text_color='#000000', corner_radius=50, hover_color='#007860',
                                      border_width=1, fg_color='#00ffc3')
        btnSalesCRUD.grid(row=6, column=0, padx=10, pady=10)
        # endregion Go To Sales Form

        # region Go To Store Form
        def storesCRUD():
            authorsForm.destroy()
            from UserInterfaceLayer.Stores_CRUD_Module import StoresFormClass
            storesFormObject = StoresFormClass(user=self.User)
            storesFormObject.storesFormLoad()

        btnStoresCRUD = ctk.CTkButton(sidebarFrame, text="Stores' Form", width=140, command=storesCRUD,
                                      text_color='#000000', corner_radius=50, hover_color='#007860',
                                      border_width=1, fg_color='#00ffc3')
        btnStoresCRUD.grid(row=7, column=0, padx=10, pady=10)
        # endregion Go To Store Form

        # region Go To Titles Form
        def titlesCRUD():
            authorsForm.destroy()
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

        #region Frame info
        frameInfo = ctk.CTkFrame(authorsForm)
        frameInfo.grid(row=0, column=1, padx=10, pady=10, ipadx=10, ipady=10)

        # region Frame Info Label
        lblFrameInfoPrompt = ctk.CTkLabel(frameInfo,text_color='#616161', font=("Helvetica", 12),
                                           text="Authors' Information")
        lblFrameInfoPrompt.grid(row=0, column=0, padx=10, pady=0, sticky='w')
        # endregion Frame Info Label

        #region Author ID
        lblAuthorID = ctk.CTkLabel(frameInfo, text='Author ID: ')
        lblAuthorID.grid(row=1, column=0, padx=10, pady=10, sticky='w')

        txtAuthorID = StringVar()
        txtAuthorID.trace('w', checkValidationAuthorID)
        entAuthorID = ctk.CTkEntry(frameInfo, width=280, textvariable=txtAuthorID, corner_radius=50,
                                   border_width=1, border_color='#FFFFFF',
                                   placeholder_text="Example: 111-11-1111", placeholder_text_color='#FFFFFF')
        entAuthorID.grid(row=1, column=1, padx=10, pady=10)
        #endregion

        #region First Name
        lblFirstName = ctk.CTkLabel(frameInfo, text='First Name: ')
        lblFirstName.grid(row=2, column=0, padx=10, pady=10, sticky='w')

        txtFirstName = StringVar()
        entFirstName = ctk.CTkEntry(frameInfo, width=280, textvariable=txtFirstName, corner_radius=50,
                                    border_width=1, border_color='#FFFFFF')
        entFirstName.grid(row=2, column=1, padx=10, pady=10, sticky='w')
        #endregion

        #region Last Name
        lblLastName = ctk.CTkLabel(frameInfo, text='Last Name: ')
        lblLastName.grid(row=3, column=0, padx=10, pady=10, sticky='w')

        txtLastName = StringVar()
        entLastName = ctk.CTkEntry(frameInfo, width=280, textvariable=txtLastName, corner_radius=50,
                                   border_width=1, border_color='#FFFFFF')
        entLastName.grid(row=3, column=1, padx=10, pady=10)
        #endregion

        #region Phone Number
        lblPhoneNumber = ctk.CTkLabel(frameInfo, text='Phone Number: ')
        lblPhoneNumber.grid(row=4, column=0, padx=10, pady=10, sticky='w')

        txtPhoneNumber = StringVar()
        txtPhoneNumber.trace('w', checkValidationPhoneNumber)
        entPhoneNumber = ctk.CTkEntry(frameInfo, width=280, textvariable=txtPhoneNumber, corner_radius=50,
                                      border_width=1, border_color='#FFFFFF')
        entPhoneNumber.grid(row=4, column=1, padx=10, pady=10)
        #endregion

        #region Address
        lblAddress = ctk.CTkLabel(frameInfo, text='Address: ')
        lblAddress.grid(row=5, column=0, padx=10, pady=10, sticky='w')

        txtAddress = StringVar()
        entAddress = ctk.CTkEntry(frameInfo, width=280, textvariable=txtAddress, corner_radius=50,
                                   border_width=1, border_color='#FFFFFF')
        entAddress.grid(row=5, column=1, padx=10, pady=10)
        #endregion

        #region City
        lblCity = ctk.CTkLabel(frameInfo, text='City: ')
        lblCity.grid(row=6, column=0, padx=10, pady=10, sticky='w')

        txtCity = StringVar()
        entCity = ctk.CTkEntry(frameInfo, width=280, textvariable=txtCity, corner_radius=50,
                                   border_width=1, border_color='#FFFFFF')
        entCity.grid(row=6, column=1, padx=10, pady=10)
        #endregion

        # region State
        statesList = [
            "AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA",
            "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD",
            "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ",
            "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC",
            "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"
        ]
        lblState = ctk.CTkLabel(frameInfo, text='State: ')
        lblState.grid(row=7, column=0, padx=10, pady=10, sticky='w')

        txtState = StringVar()
        cmdState = ctk.CTkComboBox(frameInfo, width=280, values=statesList, state='readonly',
                                   corner_radius=50, border_width=1, border_color='#FFFFFF', variable=txtState)
        cmdState.grid(row=7, column=1, padx=10, pady=10)
        # endregion State

        #region Zipcode
        lblZipCode = ctk.CTkLabel(frameInfo, text='Zip code: ')
        lblZipCode.grid(row=8, column=0, padx=10, pady=10, sticky='w')

        txtZipCode = StringVar()
        txtZipCode.trace('w', checkValidationZipCode)
        entZipCode = ctk.CTkEntry(frameInfo, width=280, textvariable=txtZipCode, corner_radius=50,
                                      border_width=1, border_color='#FFFFFF')
        entZipCode.grid(row=8, column=1, padx=10, pady=10)
        #endregion

        #region Contract
        lblContract = ctk.CTkLabel(frameInfo, text='Contract Status: ')
        lblContract.grid(row=9, column=0, padx=10, pady=10, sticky='w')

        intContract = IntVar()
        rdbContract = ctk.CTkRadioButton(frameInfo, text='Under contract', variable=intContract, value=1)
        rdbContract.grid(row=9, column=1, padx=10, pady=10, sticky='w')

        rdbNotContract = ctk.CTkRadioButton(frameInfo, text='Not under contract', value=0, variable=intContract)
        rdbNotContract.grid(row=9, column=1, padx=10, pady=10, sticky='e')
        intContract.set(1)
        #endregion

        #region Register Author
        btnRegister = ctk.CTkButton(frameInfo, text='Register Author', width=130, command=duplicateIDCheckRegister,
                                    text_color='#000000', corner_radius=50, hover_color='#007860',
                                    border_width=1, fg_color='#00ffc3')
        btnRegister.grid(row=10, column=1, padx=10, pady=10, sticky='e')
        #endregion

        #region Edit Author
        btnEditAuthor = ctk.CTkButton(frameInfo, text='Edit Author', width=130, command=duplicateIDCheckEdit,
                                      text_color = '#000000', corner_radius = 50, hover_color = '#007860',
                                      border_width = 1, fg_color = '#00ffc3')
        btnEditAuthor.grid(row=10, column=1, padx=10, pady=10, sticky='w')
        #endregion Edit Author

        # region Reset Form Button
        btnResetForm = ctk.CTkButton(frameInfo, text='Clear Form', width=130, command=resetForm,
                                     text_color='#000000', corner_radius=50, hover_color='#007860',
                                     border_width=1, fg_color='#00ffc3')
        btnResetForm.grid(row=11, column=1, padx=10, pady=10, sticky='w')
        # endregion Reset Form Button

        #region Delete Author
        btnDeleteAuthor = ctk.CTkButton(frameInfo, text='Delete Author', width=130, command=deleteAuthorConfirmation,
                                      text_color = '#000000', corner_radius = 50, hover_color = '#910024',
                                      border_width = 1, fg_color = '#ff0040')
        btnDeleteAuthor.grid(row=11, column=1, padx=10, pady=10, sticky='e')
        #endregion Delete Author

        #endregion Frame Info

        # region Initial Treeview Style
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", background="#2d2d2d", foreground="white", rowheight=50,
                        fieldbackground="#2d2d2d", bordercolor="#444444", borderwidth=1,
                        font=("Helvetica", 12))
        style.map('Treeview', background=[('selected', '#1a73e8')], foreground=[('selected', 'white')])
        # endregion Initial Treeview Style

        # region Treeview
        frmTV = ctk.CTkFrame(authorsForm)
        frmTV.grid(row=0, column=2, padx=0, pady=10, ipadx=10, ipady=10, sticky=NSEW)

        # region Treeview Label
        lblTreeViewPrompt = ctk.CTkLabel(frmTV,text_color='#616161', font=("Helvetica", 12),
                                           text="View List")
        lblTreeViewPrompt.grid(row=0, column=0, padx=10, pady=0, sticky='w')
        # endregion Treeview Label

        # region Columns
        _columns = ['Index', 'AuthorID', 'FirstName', 'LastName', 'PhoneNumber',
                    'Address', 'City', 'State', 'ZipCode', 'Contract']
        _displayColumns = ['Index', 'AuthorID', 'FirstName', 'LastName', 'PhoneNumber',
                    'Address', 'City', 'State', 'ZipCode', 'Contract']
        # endregion Columns

        # region Treeview Widgets
        tvAuthorsList = ttk.Treeview(frmTV, columns=_columns, displaycolumns=_displayColumns,
                                      show='headings', selectmode='browse', height=30)
        tvAuthorsList.grid(row=1, column=0, padx=10, pady=10, sticky=NSEW)

        tvAuthorsList.bind('<<TreeviewSelect>>', onTreeSelect)

        tvAuthorsList.column('#0', width=0)

        tvAuthorsList.column(column='Index', width=50)
        tvAuthorsList.heading(text='Index', column='Index')

        tvAuthorsList.column(column='AuthorID', width=100)
        tvAuthorsList.heading(text='AuthorID', column='AuthorID')

        tvAuthorsList.column(column='FirstName', width=100, anchor=CENTER)
        tvAuthorsList.heading(column='FirstName', text='FirstName', anchor=CENTER)

        tvAuthorsList.column(column='LastName', width=100, anchor=CENTER)
        tvAuthorsList.heading(column='LastName', text='LastName', anchor=CENTER)

        tvAuthorsList.column(column='PhoneNumber', width=120, anchor=CENTER)
        tvAuthorsList.heading(column='PhoneNumber', text='PhoneNumber', anchor=CENTER)

        tvAuthorsList.column(column='Address', width=150, anchor=CENTER)
        tvAuthorsList.heading(column='Address', text='Address', anchor=CENTER)

        tvAuthorsList.column(column='City', width=70, anchor=CENTER)
        tvAuthorsList.heading(column='City', text='City', anchor=CENTER)

        tvAuthorsList.column(column='State', width=50, anchor=CENTER)
        tvAuthorsList.heading(column='State', text='State', anchor=CENTER)

        tvAuthorsList.column(column='ZipCode', width=80, anchor=CENTER)
        tvAuthorsList.heading(column='ZipCode', text='ZipCode', anchor=CENTER)

        tvAuthorsList.column(column='Contract', width=80, anchor=CENTER)
        tvAuthorsList.heading(column='Contract', text='Contract', anchor=CENTER)
        # endregion Treeview Widgets

        # region Search Box
        # lblSearch = ctk.CTkLabel(frmTV, text='Search: ')
        # lblSearch.grid(row=2, column=0, padx=10, pady=10, sticky='w')
        #
        # txtSearch = StringVar()
        # entSearch = ctk.CTkEntry(frmTV, width=350, textvariable=txtSearch, corner_radius=50,
        #                             border_width=1, border_color='#FFFFFF')
        # entSearch.grid(row=3, column=0, padx=10, pady=10, sticky='w')
        #
        # btnSearch = ctk.CTkButton(frmTV, width=60, command=filterTreeview,
        #                               text_color = '#000000', corner_radius = 50, hover_color = '#007860',
        #                               border_width = 1, fg_color = '#00ffc3')
        # btnSearch.grid(row=4, column=0, padx=10, pady=10, sticky='w')
        # endregion Search Box

        # endregion Treeview

        updateTreeviewStyle()
        showList()
        authorsForm.after(0, setClock)
        authorsForm.mainloop()
