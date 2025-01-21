from tkinter import *
import customtkinter as ctk
from Model.UserModel import UserModelClass
from tkinter import ttk
from BusinessLogicLayer.Titles_BLL_Module import TitlesBLLClass
from datetime import datetime
from tkinter import messagebox as msg
from Utility.Date_Picker_Module import CustomDatePicker
import re

class TitlesFormClass:
    def __init__(self, user: UserModelClass):
        self.User = user

    def titlesFormLoad(self):
        titlesForm = ctk.CTk()
        titlesForm.title("Titles' CRUD Form")
        titlesForm.geometry('1170x540')
        titlesForm.iconbitmap('Images/page.ico')
        titlesForm.resizable(True, True)
        x = int((titlesForm.winfo_screenwidth() / 2) - (1170 / 2))
        y = int((titlesForm.winfo_screenheight() / 2) - (540 / 2))
        titlesForm.geometry('+{}+{}'.format(x, y))

        # region Required Functions

        # region Date and time Function
        def setClock():
            currentDateTime = datetime.today()
            currentDateTime = currentDateTime.strftime('%Y/%m/%d  %H:%M:%S')
            txtCurrentDateTime.set(f'{currentDateTime}')
            titlesForm.after(1000, setClock)

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

        # region Register Titles
        def registerTitles():
            titleID = txtTitleID.get()
            titleName = txtTitleName.get()
            titleType = txtType.get()
            pubID = publishersListDictionary[txtPublishersName.get()]
            price = txtPrice.get()
            advance = txtAdvance.get()
            royalty = int(txtRoyalty.get())
            ytdSale = int(txtYTDSale.get())
            notes = txtNotes.get()
            pubDate = txtPubDate.get()

            from Model.Titles_Module import TitlesModelClass
            titlesModelObject = TitlesModelClass(ttlID=titleID, ttl=titleName, typ=titleType,
                                                 pbID=pubID, prc=price, adv=advance, rylt=royalty,
                                                 ytd=ytdSale, nte=notes, pbDate=pubDate)
            titlesBLLObject = TitlesBLLClass()
            titlesBLLObject.registerTitle(title=titlesModelObject)

            resetTitlesForm()
            showList()
        # endregion Register Titles

        # region Register Title Author
        def registerTitleAuthor():
            authorID = authorsNameListDictionary[txtAuthor.get()]
            titleID = titlesNameListDictionary[txtTitleAuthor.get()]
            authorOrder = int(txtAuthorOrder.get())
            royaltyPer = int(txtRoyaltyPerAuthor.get())

            from Model.TitleAuthor_Module import TitleAuthorModelClass
            titleAuthorModelObject = TitleAuthorModelClass(auID=authorID, titlID=titleID,
                                                           auOrder=authorOrder, royaltyPer=royaltyPer)
            titlesBLLObject = TitlesBLLClass()
            titlesBLLObject.registerTitleAuthor(titleAuthor=titleAuthorModelObject)

            resetAuthorForm()
            showTitleAuthorList()
        # endregion Register TitleAuthor

        # region Back To Main Button Function
        def backToMain():
            titlesForm.destroy()
            from UserInterfaceLayer.MainFormModule import MainFormClass
            mainFormObject = MainFormClass(user=self.User)
            mainFormObject.mainForm_Load()
        # endregion Back To Main Button Function

        # region Edit Titles Function
        def editTitles():
            titleID = txtTitleID.get()
            titleName = txtTitleName.get()
            titleType = txtType.get()
            pubID = publishersListDictionary[txtPublishersName.get()]
            price = txtPrice.get()
            advance = txtAdvance.get()
            royalty = int(txtRoyalty.get())
            ytdSale = int(txtYTDSale.get())
            notes = txtNotes.get()
            pubDate = txtPubDate.get()

            from Model.Titles_Module import TitlesModelClass
            titleModelObject = TitlesModelClass(ttlID=titleID, ttl=titleName, typ=titleType,
                                                 pbID=pubID, prc=price, adv=advance, rylt=royalty,
                                                 ytd=ytdSale, nte=notes, pbDate=pubDate)
            titlesBLLObject = TitlesBLLClass()
            titlesBLLObject.editTitleBLL(title=titleModelObject)
            resetTitlesForm()
            showList()
        # endregion Edit Titles Function

        # region Edit Title Author Function
        def editTitleAuthor():
            authorID = authorsNameListDictionary[txtAuthor.get()]
            titleID = titlesNameListDictionary[txtTitleAuthor.get()]
            authorOrder = int(txtAuthorOrder.get())
            royaltyPer = int(txtRoyaltyPerAuthor.get())

            from Model.TitleAuthor_Module import TitleAuthorModelClass
            titleAuthorModelObject = TitleAuthorModelClass(auID=authorID, titlID=titleID,
                                                           auOrder=authorOrder, royaltyPer=royaltyPer)
            titlesBLLObject = TitlesBLLClass()
            titlesBLLObject.editTitleAuthorBLL(titleAuthor=titleAuthorModelObject)

            resetAuthorForm()
            showTitleAuthorList()

        # endregion Edit Title Author Function

        # region Duplicate ID Check Functions
        def getTitleIDFromTitles():
            titlesBLLObject = TitlesBLLClass()
            rows = titlesBLLObject.getTitleIDBLL()
            titleIDList = [row[0] for row in rows]
            return titleIDList

        myTitleIDList = getTitleIDFromTitles()

        def getAuthorIDFromTitleAuthor():
            titlesBLLObject = TitlesBLLClass()
            rows = titlesBLLObject.getAuthorIDFromTitleAuthor()
            authorIDList = [row[0] for row in rows]
            return authorIDList

        myAuthorIDList = getAuthorIDFromTitleAuthor()

        def getTitleIDFromTitleAuthor():
            titlesBLLObject = TitlesBLLClass()
            rows = titlesBLLObject.getTitleIDFromTitleAuthor()
            titleIDList = [row[0] for row in rows]
            return titleIDList

        myTitleIDFromTitleAuthorList = getTitleIDFromTitleAuthor()

        def duplicateCheckRegisterTitle():
            if txtTitleID.get() not in myTitleIDList:
                registerTitles()
            else:
                msg.showerror("Error", "Duplicate Title ID!")

        def duplicateCheckRegisterTitleAuthor():
            if (authorsNameListDictionary[txtTitleAuthor.get()] not in myAuthorIDList
                and
                titlesNameListDictionary[txtTitleID.get()] not in myTitleIDFromTitleAuthorList):
                registerTitleAuthor()
            else:
                msg.showerror("Error", "Duplicate Title Author!")

        def duplicateCheckEditTitle():
            if txtTitleID.get() in myTitleIDList:
                editTitles()
            else:
                msg.showerror("Error", "Title ID must remain the same!")

        def duplicateCheckEditTitleAuthor():
            if (authorsNameListDictionary[txtTitleAuthor.get()] in myAuthorIDList
                and
                titlesNameListDictionary[txtTitleID.get()] in myTitleIDFromTitleAuthorList):
                editTitleAuthor()
            else:
                msg.showerror("Error", "Author Name and Title Name must remain the same!")


        # endregion Duplicate ID Check Functions

        # region Delete Titles Function
        def deleteTitle():
            titleID = txtTitleID.get()
            if titleID is not NONE:
                titlesBLLObject = TitlesBLLClass()
                titlesBLLObject.deleteTitleBLL(titleID=titleID)

            resetTitlesForm()
            showList()
        # endregion Delete Titles Function

        # region Delete Titles Confirmation Function
        def deleteTitleConfirmation():
            result = msg.askyesno("Confirm Delete", "Are you sure you want to delete this title?")
            if result:
                deleteTitle()
        # endregion Delete Titles Confirmation Function

        # region Delete TitleAuthor Function
        def deleteTitleAuthor():
            authorID = authorsNameListDictionary[txtTitleAuthor.get()]
            titleID = titlesNameListDictionary[txtTitleID.get()]

            if authorID is not NONE and titleID is not NONE:
                titlesBLLObject = TitlesBLLClass()
                titlesBLLObject.deleteTitleAuthor(authorID=authorID, titleID=titleID)

            resetAuthorForm()
            showTitleAuthorList()
        # endregion Delete TitleAuthor Function

        # region Delete Title Author Confirmation Function
        def deleteTitleAuthorConfirmation():
            result = msg.askyesno("Confirm Delete", "Are you sure you want to delete this author?")
            if result:
                deleteTitleAuthor()
        # endregion Delete Title Author Confirmation Function

        # region Reset Titles Form Function
        def resetTitlesForm():
            for widget in infoTabView.tab("Titles' Info").winfo_children():
                if isinstance(widget, ctk.CTkEntry):
                    widget.delete(0, ctk.END)
        # endregion Reset Titles Form Function

        # region Reset Authors Form Function
        def resetAuthorForm():
            for widget in infoTabView.tab("Authors' Info").winfo_children():
                if isinstance(widget, ctk.CTkEntry):
                    widget.delete(0, ctk.END)
        # endregion Reset Authors Form Function

        # region Get Publishers List Function
        publishersList = dict()
        def getPublishersList():
            employeeBLLObject = TitlesBLLClass()
            rows = employeeBLLObject.getPublishersList()
            for row in rows:
                if row[1] not in publishersList:
                    publishersList[row[1]] = row[0]
            return publishersList

        publishersListDictionary = getPublishersList()
        reversedPublishersListDictionary = {v:k for k, v in publishersListDictionary.items()}
        # endregion Get Publishers List Function

        # region Get Authors List Function
        authorsNameList = dict()
        def getAuthorsNameList():
            titlesBLLObject = TitlesBLLClass()
            rows = titlesBLLObject.getAuthorsNameListBLL()
            for row in rows:
                # if row not in authorsNameList:
                authorsNameList[row[1]] = row[0]
            return authorsNameList

        authorsNameListDictionary = getAuthorsNameList()
        reversedAuthorsNameListDictionary = {v:k for k, v in authorsNameListDictionary.items()}
        # endregion Get Authors List Function

        # region Get Titles Name List Function
        titlesNameList = dict()
        def getTitlesNameList():
            titlesBLLObject = TitlesBLLClass()
            rows = titlesBLLObject.getTitlesNameListBLL()
            for row in rows:
                if row[1] not in titlesNameList:
                    titlesNameList[row[1]] = row[0]
            return titlesNameList

        titlesNameListDictionary = getTitlesNameList()
        reversedTitlesNameListDictionary = {v:k for k, v in titlesNameListDictionary.items()}
        # endregion Get Titles Name List Function

        # region Show Titles List Function
        def showList():
            titlesBLL_Object = TitlesBLLClass()
            titlesList = titlesBLL_Object.getTitlesListBLL()
            if len(titlesList) > 0:
                tvTitlesList.delete(*tvTitlesList.get_children())
                rowCount = 0
                for row in titlesList:
                    rowCount += 1
                    values = [rowCount]
                    for value in row:
                        if value is NONE:
                            values.append("")
                        else:
                            values.append(value)

                    keyPublisher = reversedPublishersListDictionary.get(values[4])
                    values[4] = keyPublisher

                    tvTitlesList.insert("", "end", values=values)
        # endregion Show Titles List Function

        # region Show TitleAuthor List Function
        def showTitleAuthorList():
            titlesBLL_Object = TitlesBLLClass()
            titlesName = titlesBLL_Object.getTitleAuthorListBLL()
            if len(titlesName) > 0:
                tvAuthorList.delete(*tvAuthorList.get_children())
                rowCount = 0
                for row in titlesName:
                    rowCount += 1
                    values = [rowCount]
                    for value in row:
                        if value is NONE:
                            values.append("")
                        else:
                            values.append(value)

                    keyAuthor = reversedAuthorsNameListDictionary.get(values[1])
                    values[1] = keyAuthor
                    keyTitle = reversedTitlesNameListDictionary.get(values[2])
                    values[2] = keyTitle

                    tvAuthorList.insert("", "end", values=values)


        # endregion Show TitleAuthor List Function

        # region Title ID Validation Function
        def checkValidationTitleID(*args):
            if len(txtTitleID.get()) > 6:
                txtTitleID.set(txtTitleID.get()[:len(txtTitleID.get()) - 1])
            for char in txtTitleID.get():
                if not char.isnumeric() and not char.isalpha():
                    txtTitleID.set(txtTitleID.get().replace(char, ''))
        # endregion Title ID Validation Function

        # region Title On Tree Selection Function
        def onTreeSelectTitle(event):
            resetTitlesForm()
            index = tvTitlesList.selection()
            if index:
                selectedRow = tvTitlesList.item(index)['values']
                txtTitleID.set(selectedRow[1])
                txtTitleName.set(selectedRow[2])
                txtType.set(selectedRow[3])
                txtPublishersName.set(selectedRow[4])
                txtPrice.set(selectedRow[5])
                txtAdvance.set(selectedRow[6])
                txtRoyalty.set(selectedRow[7])
                txtYTDSale.set(selectedRow[8])
                txtNotes.set(selectedRow[9])
                txtPubDate.set(selectedRow[10])
        # endregion Title On Tree Selection Function

        # region Author On Tree Selection Function
        def onTreeSelectAuthor(event):
            resetAuthorForm()
            index = tvAuthorList.selection()
            if index:
                selectedRow = tvAuthorList.item(index)['values']
                txtAuthor.set(selectedRow[1])
                txtTitleAuthor.set(selectedRow[2])
                txtAuthorOrder.set(selectedRow[3])
                txtRoyaltyPerAuthor.set(selectedRow[4])
        # endregion Author On Tree Selection Function

        # endregion Required Functions

        # region Sidebar Frame
        sidebarFrame = ctk.CTkFrame(titlesForm, width=140, corner_radius=0)
        sidebarFrame.grid(row=0, column=0, rowspan=2, sticky="nsew")
        # sidebarFrame.grid_rowconfigure(4, weight=1)

        logoLabel = ctk.CTkLabel(sidebarFrame, text="PUBS", font=ctk.CTkFont(size=20, weight="bold"))
        logoLabel.grid(row=0, column=0, padx=20, pady=(20, 10))

        # region Form Name
        lblFormName = ctk.CTkLabel(sidebarFrame, text="Titles' Form")
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
            titlesForm.destroy()
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
            titlesForm.destroy()
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
            titlesForm.destroy()
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
            titlesForm.destroy()
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
            titlesForm.destroy()
            from UserInterfaceLayer.Sales_CRUD_Module import SalesFormClass
            salesFormObject = SalesFormClass(user=self.User)
            salesFormObject.salesFormLoad()

        btnSalesCRUD = ctk.CTkButton(sidebarFrame, text="Sales' Form", width=140, command=salesCRUD,
                                     text_color='#000000', corner_radius=50, hover_color='#007860',
                                     border_width=1, fg_color='#00ffc3')
        btnSalesCRUD.grid(row=7, column=0, padx=10, pady=10)

        # endregion Go To Sales Form

        # region Go To Store Form
        def storesCRUD():
            titlesForm.destroy()
            from UserInterfaceLayer.Stores_CRUD_Module import StoresFormClass
            storesFormObject = StoresFormClass(user=self.User)
            storesFormObject.storesFormLoad()

        btnStoresCRUD = ctk.CTkButton(sidebarFrame, text="Stores' Form", width=140, command=storesCRUD,
                                      text_color='#000000', corner_radius=50, hover_color='#007860',
                                      border_width=1, fg_color='#00ffc3')
        btnStoresCRUD.grid(row=8, column=0, padx=10, pady=10)

        # endregion Go To Store Form


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

        # region Treeview Tabview
        tvTabView = ctk.CTkTabview(titlesForm, width=250)
        tvTabView.grid(row=0, column=1, padx=10, pady=0, ipadx=10, ipady=10, sticky="nsew")
        tvTabView.add("Titles' List")
        tvTabView.add("Authors' List")

        tvTabView.tab("Titles' List").grid_columnconfigure(0, weight=1)
        tvTabView.tab("Authors' List").grid_columnconfigure(0, weight=1)

        # region Titles' Treeview

        # region Columns
        _columns = ['Index', 'TitleID', 'Title', 'Type', 'Publisher',
                    'Price', 'Advance', 'Royalty', 'YTDSale', 'Notes', 'PubDate']
        _displayColumns = ['Index', 'TitleID', 'Title', 'Type', 'Publisher',
                           'Price', 'Advance', 'Royalty', 'YTDSale', 'Notes', 'PubDate']
        # endregion Columns

        # region Treeview Widgets
        tvTitlesList = ttk.Treeview(tvTabView.tab("Titles' List"), columns=_columns, displaycolumns=_displayColumns,
                                  show='headings', selectmode='browse')
        tvTitlesList.grid(row=1, column=0, padx=10, pady=10, sticky=NSEW)

        tvTitlesList.bind('<<TreeviewSelect>>', onTreeSelectTitle)

        tvTitlesList.column('#0', width=0)

        tvTitlesList.column(column='Index', width=40)
        tvTitlesList.heading(text='Index', column='Index')

        tvTitlesList.column(column='TitleID', width=80)
        tvTitlesList.heading(text='TitleID', column='TitleID')

        tvTitlesList.column(column='Title', width=200)
        tvTitlesList.heading(text='Title', column='Title')

        tvTitlesList.column(column='Type', width=100)
        tvTitlesList.heading(text='Type', column='Type')

        tvTitlesList.column(column='Publisher', width=130)
        tvTitlesList.heading(text='Publisher', column='Publisher')

        tvTitlesList.column(column='Price', width=80)
        tvTitlesList.heading(text='Price', column='Price')

        tvTitlesList.column(column='Advance', width=90)
        tvTitlesList.heading(text='Advance', column='Advance')

        tvTitlesList.column(column='Royalty', width=60)
        tvTitlesList.heading(text='Royalty', column='Royalty')

        tvTitlesList.column(column='YTDSale', width=60)
        tvTitlesList.heading(text='YTDSale', column='YTDSale')

        tvTitlesList.column(column='Notes', width=220)
        tvTitlesList.heading(text='Notes', column='Notes')

        tvTitlesList.column(column='PubDate', width=100)
        tvTitlesList.heading(text='PubDate', column='PubDate')
        # endregion Treeview Widgets

        # endregion Titles' Treeview

        # region TitlesAuthor Treeview

        # region Columns
        _columns1 = ['Index', 'Author', 'Title', 'AuthorOrder', 'Royalty/Author']
        _displayColumns1 = ['Index', 'Author', 'Title', 'AuthorOrder', 'Royalty/Author']
        # endregion Columns

        # region Treeview Widgets
        tvAuthorList = ttk.Treeview(tvTabView.tab("Authors' List"), columns=_columns1, displaycolumns=_displayColumns1,
                                    show='headings', selectmode='browse')
        tvAuthorList.grid(row=1, column=0, padx=10, pady=10, sticky=NSEW)

        tvAuthorList.bind('<<TreeviewSelect>>', onTreeSelectAuthor)

        tvAuthorList.column('#0', width=0)

        tvAuthorList.column(column='Index', width=40)
        tvAuthorList.heading(text='Index', column='Index')

        tvAuthorList.column(column='Author', width=250)
        tvAuthorList.heading(text='Author', column='Author')

        tvAuthorList.column(column='Title', width=400)
        tvAuthorList.heading(text='Title', column='Title')

        tvAuthorList.column(column='AuthorOrder', width=80)
        tvAuthorList.heading(text='AuthorOrder', column='AuthorOrder')

        tvAuthorList.column(column='Royalty/Author', width=150)
        tvAuthorList.heading(text='Royalty/Author', column='Royalty/Author')

        # endregion Treeview Widgets

        # endregion TitlesAuthor Treeview

        # endregion Treeview Tabview

        # region Information Tabview
        infoTabView = ctk.CTkTabview(titlesForm, width=250)
        infoTabView.grid(row=1, column=1, padx=10, pady=(0, 10), ipadx=10, ipady=10, sticky="nsew")
        infoTabView.add("Titles' Info")
        infoTabView.add("Authors' Info")

        infoTabView.tab("Titles' Info").grid_columnconfigure(0, weight=1)
        infoTabView.tab("Authors' Info").grid_columnconfigure(0, weight=1)

        # region Titles Information

        # region Title ID
        lblTitleID = ctk.CTkLabel(infoTabView.tab("Titles' Info"), text='Title ID: ')
        lblTitleID.grid(row=0, column=0, padx=10, pady=10, sticky='w')

        txtTitleID = StringVar()
        txtTitleID.trace('w', checkValidationTitleID)
        entTitleID = ctk.CTkEntry(infoTabView.tab("Titles' Info"), width=200, textvariable=txtTitleID, corner_radius=50,
                                border_width=1, border_color='#FFFFFF')
        entTitleID.grid(row=0, column=1, padx=10, pady=10, sticky='w')
        # endregion Title ID

        # region Title Name
        lblTitleName = ctk.CTkLabel(infoTabView.tab("Titles' Info"), text='Title Name: ')
        lblTitleName.grid(row=0, column=2, padx=10, pady=10, sticky='w')

        txtTitleName = StringVar()
        entTitleName = ctk.CTkEntry(infoTabView.tab("Titles' Info"), width=200, textvariable=txtTitleName, corner_radius=50,
                                border_width=1, border_color='#FFFFFF')
        entTitleName.grid(row=0, column=3, padx=10, pady=10, sticky='w')
        # endregion Title Name

        # region Type
        lblType = ctk.CTkLabel(infoTabView.tab("Titles' Info"), text='Type: ')
        lblType.grid(row=0, column=4, padx=10, pady=10, sticky='w')

        txtType = StringVar()
        entType = ctk.CTkEntry(infoTabView.tab("Titles' Info"), width=200, textvariable=txtType, corner_radius=50,
                                border_width=1, border_color='#FFFFFF')
        entType.grid(row=0, column=5, padx=10, pady=10, sticky='w')
        # endregion Type

        # region PublishersName
        lblPublishersName = ctk.CTkLabel(infoTabView.tab("Titles' Info"), text="Publisher's Name: ")
        lblPublishersName.grid(row=1, column=0, padx=10, pady=10, sticky='w')

        txtPublishersName = StringVar()
        cmdPublishersName = ctk.CTkComboBox(infoTabView.tab("Titles' Info"), width=200, values=list(getPublishersList().keys()), state='readonly',
                                               corner_radius=50, border_width=1, border_color='#FFFFFF',
                                               variable=txtPublishersName)
        cmdPublishersName.grid(row=1, column=1, padx=10, pady=10, sticky='w')
        # endregion PublishersName

        # region Price
        lblPrice = ctk.CTkLabel(infoTabView.tab("Titles' Info"), text='Price: ')
        lblPrice.grid(row=1, column=2, padx=10, pady=10, sticky='w')

        txtPrice = StringVar()
        entPrice = ctk.CTkEntry(infoTabView.tab("Titles' Info"), width=200, textvariable=txtPrice, corner_radius=50,
                                border_width=1, border_color='#FFFFFF')
        entPrice.grid(row=1, column=3, padx=10, pady=10, sticky='w')
        # endregion Price

        # region Advance
        lblAdvance = ctk.CTkLabel(infoTabView.tab("Titles' Info"), text='Advance: ')
        lblAdvance.grid(row=1, column=4, padx=10, pady=10, sticky='w')

        txtAdvance = StringVar()
        entAdvance = ctk.CTkEntry(infoTabView.tab("Titles' Info"), width=200, textvariable=txtAdvance, corner_radius=50,
                                border_width=1, border_color='#FFFFFF')
        entAdvance.grid(row=1, column=5, padx=10, pady=10, sticky='w')
        # endregion Advance

        # region Royalty
        lblRoyalty = ctk.CTkLabel(infoTabView.tab("Titles' Info"), text='Royalty: ')
        lblRoyalty.grid(row=2, column=0, padx=10, pady=10, sticky='w')

        txtRoyalty = StringVar()
        entRoyalty = ctk.CTkEntry(infoTabView.tab("Titles' Info"), width=200, textvariable=txtRoyalty, corner_radius=50,
                                border_width=1, border_color='#FFFFFF')
        entRoyalty.grid(row=2, column=1, padx=10, pady=10, sticky='w')
        # endregion Title ID

        # region YTD Sale
        lblYTDSale = ctk.CTkLabel(infoTabView.tab("Titles' Info"), text='YTD Sale: ')
        lblYTDSale.grid(row=2, column=2, padx=10, pady=10, sticky='w')

        txtYTDSale = StringVar()
        entYTDSale = ctk.CTkEntry(infoTabView.tab("Titles' Info"), width=200, textvariable=txtYTDSale, corner_radius=50,
                                border_width=1, border_color='#FFFFFF')
        entYTDSale.grid(row=2, column=3, padx=10, pady=10, sticky='w')
        # endregion YTD Sale

        # region Notes
        lblNotes = ctk.CTkLabel(infoTabView.tab("Titles' Info"), text='Notes: ')
        lblNotes.grid(row=2, column=4, padx=10, pady=10, sticky='w')

        txtNotes = StringVar()
        entNotes = ctk.CTkEntry(infoTabView.tab("Titles' Info"), width=200, textvariable=txtNotes, corner_radius=50,
                                border_width=1, border_color='#FFFFFF')
        entNotes.grid(row=2, column=5, padx=10, pady=10, sticky='w')
        # endregion Notes

        # region Pub Date
        lblPubDate = ctk.CTkLabel(infoTabView.tab("Titles' Info"), text='Pub. Date: ')
        lblPubDate.grid(row=3, column=0, padx=10, pady=10, sticky='w')

        txtPubDate = StringVar()
        entPubDate = ctk.CTkEntry(infoTabView.tab("Titles' Info"), width=200, textvariable=txtPubDate,
                                  corner_radius=50, border_width=1, border_color='#FFFFFF')
        entPubDate.grid(row=3, column=1, padx=10, pady=10, sticky=EW)

        datePicker = CustomDatePicker(infoTabView.tab("Titles' Info"), txtPubDate)
        entPubDate.bind("<Button-1>", lambda e: datePicker.openDatePicker())
        # endregion Pub Date

        #region Register Title Button
        btnRegister = ctk.CTkButton(infoTabView.tab("Titles' Info"), text='Register', width=95,
                                    command=duplicateCheckRegisterTitle, text_color='#000000', corner_radius=50,
                                    hover_color='#007860', border_width=1, fg_color='#00ffc3')
        btnRegister.grid(row=3, column=3, padx=10, pady=10, sticky='e')
        #endregion Register Title Button

        #region Edit Titles Button
        btnEditStores = ctk.CTkButton(infoTabView.tab("Titles' Info"), text='Edit Title', width=95,
                                      command=duplicateCheckEditTitle, text_color = '#000000', corner_radius = 50,
                                      hover_color = '#007860', border_width = 1, fg_color = '#00ffc3')
        btnEditStores.grid(row=3, column=3, padx=10, pady=10, sticky='w')
        #endregion Edit Titles Button

        #region Reset Form Button
        btnResetForm = ctk.CTkButton(infoTabView.tab("Titles' Info"), text='Clear Form', width=95,
                                     command=resetTitlesForm, text_color = '#000000', corner_radius = 50,
                                     hover_color = '#007860', border_width = 1, fg_color = '#00ffc3')
        btnResetForm.grid(row=3, column=5, padx=10, pady=10, sticky='w')
        #endregion Reset Form Button

        #region Delete Titles Button
        btnDeleteTitles = ctk.CTkButton(infoTabView.tab("Titles' Info"), text='Delete Title', width=95,
                                        command=deleteTitleConfirmation, text_color = '#000000', corner_radius = 50,
                                        hover_color = '#910024', border_width = 1, fg_color = '#ff0040')
        btnDeleteTitles.grid(row=3, column=5, padx=10, pady=10, sticky='e')
        #endregion Delete Titles Button

        # endregion Titles Information

        # region TitleAuthor Information
        # region Author
        lblAuthor = ctk.CTkLabel(infoTabView.tab("Authors' Info"), text='Author: ')
        lblAuthor.grid(row=0, column=0, padx=10, pady=10, sticky='w')

        txtAuthor = StringVar()
        cmdAuthor = ctk.CTkComboBox(infoTabView.tab("Authors' Info"), values=list(getAuthorsNameList().keys()),
                                 state='readonly', corner_radius=50, border_width=1, border_color='#FFFFFF',
                                 variable=txtAuthor, width=200)
        cmdAuthor.grid(row=0, column=1, padx=10, pady=10, sticky='w')
        # endregion Author

        # region Title
        lblTitleAuthor = ctk.CTkLabel(infoTabView.tab("Authors' Info"), text='Title: ')
        lblTitleAuthor.grid(row=0, column=2, padx=10, pady=10, sticky='w')

        txtTitleAuthor = StringVar()
        cmdTitleAuthor = ctk.CTkComboBox(infoTabView.tab("Authors' Info"), values=list(getTitlesNameList().keys()),
                                 state='readonly', corner_radius=50, border_width=1, border_color='#FFFFFF',
                                 variable=txtTitleAuthor, width=200)
        cmdTitleAuthor.grid(row=0, column=3, padx=10, pady=10, sticky='w')
        # endregion Title

        # region Author Order
        lblAuthorOrder = ctk.CTkLabel(infoTabView.tab("Authors' Info"), text='Author Order: ')
        lblAuthorOrder.grid(row=0, column=4, padx=10, pady=10, sticky='w')

        txtAuthorOrder = StringVar()
        entAuthorOrder = ctk.CTkEntry(infoTabView.tab("Authors' Info"), width=200, textvariable=txtAuthorOrder, corner_radius=50,
                                border_width=1, border_color='#FFFFFF')
        entAuthorOrder.grid(row=0, column=5, padx=10, pady=10, sticky='w')
        # endregion Author Order

        # region Royalty/Author
        lblRoyaltyPerAuthor = ctk.CTkLabel(infoTabView.tab("Authors' Info"), text='Royalty/Author: ')
        lblRoyaltyPerAuthor.grid(row=1, column=0, padx=10, pady=10, sticky='w')

        txtRoyaltyPerAuthor = StringVar()
        cmdRoyaltyPerAuthor = ctk.CTkEntry(infoTabView.tab("Authors' Info"), width=200, textvariable=txtRoyaltyPerAuthor, corner_radius=50,
                                border_width=1, border_color='#FFFFFF')
        cmdRoyaltyPerAuthor.grid(row=1, column=1, padx=10, pady=10, sticky='w')
        # endregion Royalty/Author

        #region Register Author Button
        btnRegister = ctk.CTkButton(infoTabView.tab("Authors' Info"), text='Register', width=95,
                                    command=duplicateCheckRegisterTitleAuthor, text_color='#000000', corner_radius=50,
                                    hover_color='#007860', border_width=1, fg_color='#00ffc3')
        btnRegister.grid(row=1, column=3, padx=10, pady=10, sticky='e')
        #endregion Register Author Button

        #region Edit Title Author Button
        btnEditStores = ctk.CTkButton(infoTabView.tab("Authors' Info"), text='Edit Author', width=95,
                                      command=duplicateCheckEditTitleAuthor, text_color = '#000000', corner_radius = 50,
                                      hover_color = '#007860', border_width = 1, fg_color = '#00ffc3')
        btnEditStores.grid(row=1, column=3, padx=10, pady=10, sticky='w')
        #endregion Edit Title Author Button

        #region Reset Form Button
        btnResetForm = ctk.CTkButton(infoTabView.tab("Authors' Info"), text='Clear Form', width=95,
                                     command=resetAuthorForm, text_color = '#000000', corner_radius = 50,
                                     hover_color = '#007860', border_width = 1, fg_color = '#00ffc3')
        btnResetForm.grid(row=1, column=5, padx=10, pady=10, sticky='w')
        #endregion Reset Form Button

        #region Delete Title Author Button
        btnDeleteAuthor = ctk.CTkButton(infoTabView.tab("Authors' Info"), text='Delete Author', width=95,
                                        command=deleteTitleAuthorConfirmation, text_color = '#000000',
                                        corner_radius = 50, hover_color = '#910024',
                                        border_width = 1, fg_color = '#ff0040')
        btnDeleteAuthor.grid(row=1, column=5, padx=10, pady=10, sticky='e')
        #endregion Delete Title Author Button
        # endregion Information Tabview

        # endregion Information Tabview

        updateTreeviewStyle()
        showList()
        showTitleAuthorList()
        titlesForm.after(0, setClock)
        titlesForm.mainloop()