from tkinter import *
import customtkinter as ctk
from Utility.Date_Picker_Module import CustomDatePicker
from datetime import datetime
from tkinter import ttk
from tkinter import messagebox as msg
from Model.UserModel import UserModelClass
from BusinessLogicLayer.Employee_BLL_Module import EmployeeBLLClass

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class EmployeeFormClass:

    def __init__(self, user: UserModelClass):
        self.User = user

    def employeeFormLoad(self):
        employeeForm = ctk.CTk()
        employeeForm.title('Employees CRUD Form')
        employeeForm.geometry('1360x580')
        employeeForm.iconbitmap('Images/page.ico')
        employeeForm.resizable(False, False)
        x = int((employeeForm.winfo_screenwidth() / 2) - (1360 / 2))
        y = int((employeeForm.winfo_screenheight() / 2) - (580 / 2))
        employeeForm.geometry('+{}+{}'.format(x, y))

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

        # region Get Jobs List
        jobsList = dict()
        def getJobsList():
            employeeBLL = EmployeeBLLClass()
            rows = employeeBLL.getJobsList()
            for row in rows:
                if row[1] not in jobsList:
                    jobsList[row[1]] = row[0]
            return jobsList

        myJobsList = getJobsList()
        # endregion Get Jobs List

        # region Get Jobs Levels
        # jobsLevelsList = dict()
        #
        def getJobsLevels():
            employeeBLL = EmployeeBLLClass()
            rows = employeeBLL.getJobsLevels()
            jobsLevelsList = {item[0]: item[1:] for item in rows}
            jobsLevelsKey = int(jobsList[txtJob.get()])
            levels = jobsLevelsList[jobsLevelsKey]
            start, end = levels
            levelsValues = [str(num) for num in range(start, end + 1)]
            return levelsValues

        def getJobsLevelsList():
            employeeBLL = EmployeeBLLClass()
            rows = employeeBLL.getJobsLevels()
            jobsLevelsList = {item[0]: item[1:] for item in rows}
            return jobsLevelsList

        myJobsLevelList = getJobsLevelsList()

        def updateJobLevels(selected_value=None):
            jobID = jobsListDictionary[txtJob.get()]
            levels = myJobsLevelList[jobID]
            cmdJobLevel.configure(values=[f'{i}' for i in range(levels[0], levels[1] + 1)])
            if cmdJobLevel.cget("values"):
                cmdJobLevel.set(cmdJobLevel.cget("values")[0])

        # event is not supported by Custom TKinter andddddddddddddddddddd Ta daaaaaaaaaa This is what I did to handle it
        # I'm really glad to do thissssssssssssssssssssssssssssssssssssss

        # endregion Get Jobs Levels

        # region Get Publishers List
        publishersList = dict()
        def getPublishersList():
            employeeBLLObject = EmployeeBLLClass()
            rows = employeeBLLObject.getPublishersList()
            for row in rows:
                if row[1] not in publishersList:
                    publishersList[row[1]] = row[0]
            return publishersList
        # endregion Get Publishers List

        # region Date and time Function
        def setClock():
            currentDateTime = datetime.today()
            currentDateTime = currentDateTime.strftime('%Y/%m/%d  %H:%M:%S')
            txtCurrentDateTime.set(f'{currentDateTime}')
            employeeForm.after(1000, setClock)
        # endregion Date and time Function

        # region Register Button Function
        def registerEmployee():
            employeeId = txtEmployeeID.get()
            firstName = txtFirstName.get()
            middleNameInitial = txtMiddleNameInitial.get()
            lastName = txtLastName.get()
            job = jobsListDictionary[txtJob.get()]
            jobLevel = txtJobLevel.get()
            publishersID = publishersListDictionary[txtPublishersID.get()]
            hireDate = txtHireDate.get()

            from Model.Employee_Module import EmployeeModelClass
            employeeModelObject = EmployeeModelClass(empID=employeeId, fname=firstName, mname=middleNameInitial,
                                                     lname=lastName, jb=job, joblvl=jobLevel, pubID=publishersID,
                                                     hiredat=hireDate)
            from BusinessLogicLayer.Employee_BLL_Module import EmployeeBLLClass
            employeeBLLObject = EmployeeBLLClass()
            employeeBLLObject.registerEmployeeBLL(employeeModelObject)
            resetForm()
        # endregion Register Button Function

        # region Duplicate ID Check Functions
        def getEmployeeID():
            employeeBLLObject = EmployeeBLLClass()
            rows = employeeBLLObject.getEmployeeIDBLL()
            employeeIDList = [row[0] for row in rows]
            return employeeIDList

        employeeID = getEmployeeID()

        def duplicateIDCheckRegister():
            if txtEmployeeID.get() in employeeID:
                msg.showerror("Error", "Duplicate Employee ID!")
            else:
                registerEmployee()

        def duplicateIDCheckEdit():
            if txtEmployeeID.get() not in employeeID:
                msg.showerror("Error", "Employee ID must remain the same!")
            else:
                editEmployee()

        # endregion Duplicate ID Check Functions

        # region Reset Form Function
        def resetForm():
            for widget in frameInfo.winfo_children():
                if isinstance(widget, ctk.CTkEntry):
                     widget.delete(0, ctk.END)
        # endregion Reset Form Function

        # region Back To Main Function
        def backToMain():
            employeeForm.destroy()
            from UserInterfaceLayer.MainFormModule import MainFormClass
            mainFormObject = MainFormClass(user=self.User)
            mainFormObject.mainForm_Load()
        # endregion Back To Main Function

        # region Edit Employee Function
        def editEmployee():
            EmployeeID = txtEmployeeID.get()
            FirstName = txtFirstName.get()
            MiddleName = txtMiddleNameInitial.get()
            LastName = txtLastName.get()
            Job = jobsListDictionary[txtJob.get()]
            JobLevel = txtJobLevel.get()
            PublishersID = publishersListDictionary[txtPublishersID.get()]
            HireDate = txtHireDate.get()

            from Model.Employee_Module import EmployeeModelClass
            employeeObject = EmployeeModelClass(empID=EmployeeID, fname=FirstName, mname=MiddleName, lname=LastName,
                                                jb=Job, joblvl=JobLevel, pubID=PublishersID, hiredat=HireDate)
            employeeBLLObject = EmployeeBLLClass()
            employeeBLLObject.editEmployee(employee=employeeObject)
            resetForm()
            showList()
        # endregion Edit Employee Function

        # region Delete Employee Function
        def deleteEmployee():
            empID = txtEmployeeID.get()
            if empID is not NONE:
                employeeBLL = EmployeeBLLClass()
                employeeBLL.deleteEmployee(empID)
            resetForm()
            showList()
        # endregion Delete Employee Function

        # region Delete Employee Confirmation Function
        def deleteEmployeeConfirmation():
            result = msg.askyesno("Confirm Delete", "Are you sure you want to delete this employee?")
            if result:
                deleteEmployee()
        # endregion Delete Employee Confirmation Function

        # region Show Employee's List Function
        jobsListDictionary = getJobsList()
        reversedJobsListDictionary = {v:k for k, v in jobsListDictionary.items()}

        publishersListDictionary = getPublishersList()
        reversedPublishersListDictionary = {v: k for k, v in publishersListDictionary.items()}

        def showList(*args):
            employeeBLL_Object = EmployeeBLLClass()
            employeeList = employeeBLL_Object.getEmployeeList()
            if len(employeeList) > 0:
                tvEmployeeList.delete(*tvEmployeeList.get_children())
                rowCount = 0
                for row in employeeList:
                    rowCount += 1
                    values = [rowCount]
                    for value in row:
                        if value is NONE:
                            values.append("")
                        else:
                            values.append(value)

                    keyJob = reversedJobsListDictionary.get(values[5])
                    values[5] = keyJob

                    keyPublisher = reversedPublishersListDictionary.get(values[7])
                    values[7] = keyPublisher
                    # با نوشتن این قسمت ذوق فراوان کردم:))))))))))))))))))))))))))))

                    tvEmployeeList.insert("", "end", values=values)
        # endregion Show Employee's List Function

        # region Treeview Click Event Function
        def onTreeSelect(event):
            resetForm()
            index = tvEmployeeList.selection()
            if index:
                selectedRow = tvEmployeeList.item(index)['values']
                txtEmployeeID.set(selectedRow[1])
                txtFirstName.set(selectedRow[2])
                txtMiddleNameInitial.set(selectedRow[3])
                txtLastName.set(selectedRow[4])
                txtJob.set(selectedRow[5])
                txtJobLevel.set(selectedRow[6])
                txtPublishersID.set(selectedRow[7])
                txtHireDate.set(selectedRow[8])
        # endregion Treeview Click Event Function

        # region Employee ID Validation Function
        def checkValidationEmployeeID(*args):
            if len(txtEmployeeID.get()) > 9:
                txtEmployeeID.set(txtEmployeeID.get()[:len(txtEmployeeID.get()) - 1])
            for char in txtEmployeeID.get():
                if not char.isnumeric() and not char.isalpha():
                    txtEmployeeID.set(txtEmployeeID.get().replace(char, ''))
        # endregion Employee ID Validation Function
        # needs check

        # endregion Required Functions

        # region Sidebar Frame
        sidebarFrame = ctk.CTkFrame(employeeForm, width=140, corner_radius=0)
        sidebarFrame.grid(row=0, column=0, rowspan=2, sticky="nsew")
        # sidebarFrame.grid_rowconfigure(4, weight=1)

        logoLabel = ctk.CTkLabel(sidebarFrame, text="PUBS", font=ctk.CTkFont(size=20, weight="bold"))
        logoLabel.grid(row=0, column=0, padx=20, pady=(20, 10))

        # region Form Name
        lblFormName = ctk.CTkLabel(sidebarFrame, text="Employees' Form")
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
            employeeForm.destroy()
            from UserInterfaceLayer.Authors_CRUD_Module import AuthorsFormClass
            authorsFormObject = AuthorsFormClass(user=self.User)
            authorsFormObject.authorsFormLoad()

        btnAuthorsCRUD = ctk.CTkButton(sidebarFrame, text="Authors' Form", width=140, command=authorsCRUD,
                                        text_color='#000000', corner_radius=50, hover_color='#007860',
                                        border_width=1, fg_color='#00ffc3')
        btnAuthorsCRUD.grid(row=3, column=0, padx=10, pady=10)

        # endregion Go to Authors Form

        # region Go to Publishers Form
        def publishersCRUD():
            employeeForm.destroy()
            from UserInterfaceLayer.Publishers_CRUD_Module import PublishersFormClass
            publishersFormObject = PublishersFormClass(user=self.User)
            publishersFormObject.publishersFormLoad()

        btnPublishersCRUD = ctk.CTkButton(sidebarFrame, text="Publishers' Form", width=140,
                                          command=publishersCRUD,
                                          text_color='#000000', corner_radius=50, hover_color='#007860',
                                          border_width=1, fg_color='#00ffc3')
        btnPublishersCRUD.grid(row=4, column=0, padx=10, pady=10)

        # endregion Go to Publishers Form

        # region Go To Jobs Form
        def jobsCRUD():
            employeeForm.destroy()
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
            employeeForm.destroy()
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
            employeeForm.destroy()
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
            employeeForm.destroy()
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

        # region Frame Info
        frameInfo = ctk.CTkFrame(employeeForm)
        frameInfo.grid(row=0, column=1, padx=10, pady=10, ipadx=10, ipady=10)

        # region Frame Info Label
        lblFrameInfoPrompt = ctk.CTkLabel(frameInfo, text_color='#616161', font=("Helvetica", 12),
                                          text="Employees' Information")
        lblFrameInfoPrompt.grid(row=0, column=0, padx=10, pady=0, sticky='w')
        # endregion Frame Info Label

        #region Employee ID
        lblEmployeeID = ctk.CTkLabel(frameInfo, text='Employee ID: ')
        lblEmployeeID.grid(row=1, column=0, padx=10, pady=10, sticky='w')

        txtEmployeeID = StringVar()
        txtEmployeeID.trace('w', checkValidationEmployeeID)
        entEmployeeID = ctk.CTkEntry(frameInfo, width=280, textvariable=txtEmployeeID, corner_radius=50,
                                   border_width=1, border_color='#FFFFFF')
        entEmployeeID.grid(row=1, column=1, padx=10, pady=10)

        lblEmployeeIDPrompt = ctk.CTkLabel(frameInfo,text_color='#616161', font=("Helvetica", 12),
                                           text='Example: [A-Z][A-Z][A-Z][1-9][0-9][0-9][0-9][0-9][F-M]')
        lblEmployeeIDPrompt.grid(row=2, column=1, padx=0, pady=0)
        #endregion

        # region First Name
        lblFirstName = ctk.CTkLabel(frameInfo, text='First name: ')
        lblFirstName.grid(row=3, column=0, padx=10, pady=10, sticky='w')

        txtFirstName = StringVar()
        entFirstName = ctk.CTkEntry(frameInfo, width=280, textvariable=txtFirstName, corner_radius=50,
                                    border_width=1, border_color='#FFFFFF')
        entFirstName.grid(row=3, column=1, padx=10, pady=10)
        #endregion

        #region Middle Name Initial
        middleNameInitialList = [
            '','A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
            'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
        ]
        lblMiddleNameInitial = ctk.CTkLabel(frameInfo, text='Middle Name Initial: ')
        lblMiddleNameInitial.grid(row=4, column=0, padx=10, pady=10, sticky='w')

        txtMiddleNameInitial = StringVar()
        cmdMiddleNameInitial = ctk.CTkComboBox(frameInfo, width=280, values=middleNameInitialList, state='readonly',
                                   corner_radius=50, border_width=1, border_color='#FFFFFF', variable=txtMiddleNameInitial)
        cmdMiddleNameInitial.grid(row=4, column=1, padx=10, pady=10)
        #endregion

        # region Last Name
        lblLastName = ctk.CTkLabel(frameInfo, text='Last Name: ')
        lblLastName.grid(row=5, column=0, padx=10, pady=10, sticky='w')

        txtLastName = StringVar()
        entLastName = ctk.CTkEntry(frameInfo, width=280, textvariable=txtLastName, corner_radius=50,
                                   border_width=1, border_color='#FFFFFF')
        entLastName.grid(row=5, column=1, padx=10, pady=10)
        #endregion

        # region Job
        lblJob = ctk.CTkLabel(frameInfo, text='Job: ')
        lblJob.grid(row=6, column=0, padx=10, pady=10, sticky='w')

        txtJob = StringVar()
        cmdJob = ctk.CTkComboBox(frameInfo, width=280, values=list(getJobsList().keys()), state='readonly',
                                               corner_radius=50, border_width=1, border_color='#FFFFFF',
                                               variable=txtJob)
        cmdJob.grid(row=6, column=1, padx=10, pady=10)
        cmdJob.set('Publisher')
        cmdJob.configure(command=updateJobLevels)

        # cmdJob.bind("<<ComboboxSelected>>", updateJobLevels)
        # stupid binding 🤣🤣🤣🤣🤣🤣🤣🤣🤣🤣

        #endregion

        # region Job Level
        lblJobLevel = ctk.CTkLabel(frameInfo, text='Job Level: ')
        lblJobLevel.grid(row=7, column=0, padx=10, pady=10, sticky='w')

        txtJobLevel = StringVar()
        cmdJobLevel = ctk.CTkComboBox(frameInfo, width=280, state='readonly', values=getJobsLevels(),
                                               corner_radius=50, border_width=1, border_color='#FFFFFF',
                                               variable=txtJobLevel)
        cmdJobLevel.grid(row=7, column=1, padx=10, pady=10)
        #endregion

        # region Publisher's ID
        lblPublishersID = ctk.CTkLabel(frameInfo, text='Publisher: ')
        lblPublishersID.grid(row=8, column=0, padx=10, pady=10, sticky='w')

        txtPublishersID = StringVar()
        cmdPublishersID = ctk.CTkComboBox(frameInfo, width=280, values=list(getPublishersList().keys()), state='readonly',
                                               corner_radius=50, border_width=1, border_color='#FFFFFF',
                                               variable=txtPublishersID)
        cmdPublishersID.grid(row=8, column=1, padx=10, pady=10)
        # endregion

        # region Hire Date
        lblHireDate = ctk.CTkLabel(frameInfo, text='Hire date: ')
        lblHireDate.grid(row=9, column=0, padx=10, pady=10, sticky='w')

        txtHireDate = StringVar()
        entHireDate = ctk.CTkEntry(frameInfo, width=280, textvariable=txtHireDate, corner_radius=50,
                                    border_width=1, border_color='#FFFFFF')
        entHireDate.grid(row=9, column=1, padx=10, pady=10, sticky=EW)

        datePicker = CustomDatePicker(frameInfo, txtHireDate)
        entHireDate.bind("<Button-1>", lambda e: datePicker.openDatePicker())
        # endregion

        #region Register Employee
        btnRegister = ctk.CTkButton(frameInfo, text='Register Employee', width=130, command=duplicateIDCheckRegister,
                                    text_color='#000000', corner_radius=50, hover_color='#007860',
                                    border_width=1, fg_color='#00ffc3')
        btnRegister.grid(row=10, column=1, padx=10, pady=10, sticky='e')
        #endregion

        #region Edit Employee
        btnEditEmployee = ctk.CTkButton(frameInfo, text='Edit Employee', width=130, command=duplicateIDCheckEdit,
                                      text_color = '#000000', corner_radius = 50, hover_color = '#007860',
                                      border_width = 1, fg_color = '#00ffc3')
        btnEditEmployee.grid(row=10, column=1, padx=10, pady=10, sticky='w')
        #endregion Edit Employee

        # region Reset Form Button
        btnResetForm = ctk.CTkButton(frameInfo, text='Clear Form', width=130, command=resetForm,
                                     text_color='#000000', corner_radius=50, hover_color='#007860',
                                     border_width=1, fg_color='#00ffc3')
        btnResetForm.grid(row=11, column=1, padx=10, pady=10, sticky='w')
        # endregion Reset Form Button

        #region Delete Employee
        btnDeleteEmployee = ctk.CTkButton(frameInfo, text='Delete Employee', width=130, command=deleteEmployeeConfirmation,
                                      text_color = '#000000', corner_radius = 50, hover_color = '#910024',
                                      border_width = 1, fg_color = '#ff0040')
        btnDeleteEmployee.grid(row=11, column=1, padx=10, pady=10, sticky='e')
        #endregion Delete Employee

        # endregion Frame Info

        #region Treeview

        # region Initial Treeview Style
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", background="#2d2d2d", foreground="white", rowheight=50,
                        fieldbackground="#2d2d2d", bordercolor="#444444", borderwidth=1,
                        font=("Helvetica", 12))
        style.map('Treeview', background=[('selected', '#1a73e8')], foreground=[('selected', 'white')])
        # endregion Initial Treeview Style

        frmTV = ctk.CTkFrame(employeeForm)
        frmTV.grid(row=0, column=2, padx=0, pady=10, ipadx=10, ipady=10, sticky=NSEW)

        # region Treeview Label
        lblTreeViewPrompt = ctk.CTkLabel(frmTV, text_color='#616161', font=("Helvetica", 12),
                                         text="View List")
        lblTreeViewPrompt.grid(row=0, column=0, padx=10, pady=0, sticky='w')
        # endregion Treeview Label

        # region Columns
        _columns = ['Index', 'EmployeeID', 'FirstName', 'MNInitial', 'LastName',
                    'Job', 'JobLVL', 'Publisher', 'HireDate']
        _displayColumns = ['Index', 'EmployeeID', 'FirstName', 'MNInitial', 'LastName',
                           'Job', 'JobLVL', 'Publisher', 'HireDate']
        # endregion Columns

        # region Treeview Widgets
        tvEmployeeList = ttk.Treeview(frmTV, columns=_columns, displaycolumns=_displayColumns,
                                      show='headings', selectmode='browse', height=25)
        tvEmployeeList.grid(row=1, column=0, padx=10, pady=10, sticky=NSEW)

        tvEmployeeList.bind('<<TreeviewSelect>>', onTreeSelect)

        tvEmployeeList.column('#0', width=0)

        tvEmployeeList.column(column='Index', width=50)
        tvEmployeeList.heading(text='Index', column='Index')

        tvEmployeeList.column(column='EmployeeID', width=100)
        tvEmployeeList.heading(text='EmployeeID', column='EmployeeID')

        tvEmployeeList.column(column='FirstName', width=100, anchor=CENTER)
        tvEmployeeList.heading(column='FirstName', text='FirstName', anchor=CENTER)

        tvEmployeeList.column(column='MNInitial', width=100, anchor=CENTER)
        tvEmployeeList.heading(column='MNInitial', text='MNInitial', anchor=CENTER)

        tvEmployeeList.column(column='LastName', width=100, anchor=CENTER)
        tvEmployeeList.heading(column='LastName', text='LastName', anchor=CENTER)

        tvEmployeeList.column(column='Job', width=100, anchor=CENTER)
        tvEmployeeList.heading(column='Job', text='Job', anchor=CENTER)

        tvEmployeeList.column(column='JobLVL', width=100, anchor=CENTER)
        tvEmployeeList.heading(column='JobLVL', text='JobLVL', anchor=CENTER)

        tvEmployeeList.column(column='Publisher', width=100, anchor=CENTER)
        tvEmployeeList.heading(column='Publisher', text='Publisher', anchor=CENTER)

        tvEmployeeList.column(column='HireDate', width=100, anchor=CENTER)
        tvEmployeeList.heading(column='HireDate', text='HireDate', anchor=CENTER)
        # endregion Treeview Widgets

        #endregion Treeview

        updateTreeviewStyle()
        showList()
        employeeForm.after(0, setClock)
        employeeForm.mainloop()
