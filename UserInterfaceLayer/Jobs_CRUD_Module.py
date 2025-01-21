from tkinter import *
import customtkinter as ctk
from Model.UserModel import UserModelClass
from BusinessLogicLayer.Jobs_BLL_Module import JobsBLLClass
from datetime import datetime
from tkinter import ttk
from tkinter import messagebox as msg
import re

class JobsFormClass:
    def __init__(self, user: UserModelClass):
        self.User = user

    def jobsFormLoad(self):
        jobsForm = ctk.CTk()
        jobsForm.title('Jobs CRUD Form')
        jobsForm.geometry('640x555')
        jobsForm.iconbitmap('Images/page.ico')
        jobsForm.resizable(False, False)
        x = int((jobsForm.winfo_screenwidth() / 2) - (640 / 2))
        y = int((jobsForm.winfo_screenheight() / 2) - (555 / 2))
        jobsForm.geometry('+{}+{}'.format(x, y))

        # region Required Functions
        # region Date and time Function
        def setClock():
            currentDateTime = datetime.today()
            currentDateTime = currentDateTime.strftime('%Y/%m/%d  %H:%M:%S')
            txtCurrentDateTime.set(f'{currentDateTime}')
            jobsForm.after(1000, setClock)

        # endregion Date and time Function

        # region Duplicate ID Check Functions
        def getJobsID():
            jobsBLLObject = JobsBLLClass()
            rows = jobsBLLObject.getJobIDBLL()
            jobIDList = [row[0] for row in rows]
            return jobIDList

        jobId = getJobsID()

        def duplicateIDCheckRegister():
            if int(txtJobID.get()) in jobId:
                msg.showerror("Error", "Duplicate Job ID!")
            else:
                registerJob()

        def duplicateIDCheckEdit():
            if int(txtJobID.get()) not in jobId:
                msg.showerror("Error", "Job ID must remain the same!")
            else:
                editJob()

        # endregion Duplicate ID Check Functions

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

        # region Register Job
        def registerJob():
            jobID = int(txtJobID.get())
            jobDescription = txtJobDescription.get()
            minLevel = int(txtMinLevel.get())
            maxLevel = int(txtMaxLevel.get())

            from Model.Jobs_Module import JobsModelClass
            jobsModelObject = JobsModelClass(jID=jobID, jDesc=jobDescription, minLvl=minLevel, maxLvl=maxLevel)
            jobsBLLObject = JobsBLLClass()
            jobsBLLObject.registerJobsBLL(jobsModelObject)

            resetForm()
        # endregion Register Job

        # region Back To Main Button Function
        def backToMain():
            jobsForm.destroy()
            from UserInterfaceLayer.MainFormModule import MainFormClass
            mainFormObject = MainFormClass(user=self.User)
            mainFormObject.mainForm_Load()
        # endregion Back To Main Button Function

        # region Edit Job Function
        def editJob():
            JobID = int(txtJobID.get())
            JobDescription = txtJobDescription.get()
            MinLevel = int(txtMinLevel.get())
            MaxLevel = int(txtMaxLevel.get())

            from Model.Jobs_Module import JobsModelClass
            jobsModelObject = JobsModelClass(jID=JobID, jDesc=JobDescription,
                                             minLvl=MinLevel, maxLvl=MaxLevel)
            jobsBLLObject = JobsBLLClass()
            jobsBLLObject.editJob(job=jobsModelObject)

            resetForm()
            showList()
        # endregion Edit Job Function

        # region Delete Job Function
        def deleteJob():
            jobID = int(txtJobID.get())
            if jobID is not NONE:
                employeeBLL_Object = JobsBLLClass()
                employeeBLL_Object.deleteJob(jobID)
            resetForm()
            showList()
        # endregion Delete Job Function

        # region Delete Job Confirmation Function
        def deleteJobConfirmation():
            result = msg.askyesno("Confirm Delete", "Are you sure you want to delete this job?")
            if result:
                deleteJob()
        # endregion Delete Job Confirmation Function

        # region Job ID Validation Function
        def checkValidationJobID(*args):
            if len(txtJobID.get()) > 4:
                txtJobID.set(txtJobID.get()[:len(txtJobID.get()) - 1])

            for char in txtJobID.get():
                if not char.isnumeric():
                    txtJobID.set(txtJobID.get().replace(char, ''))
        # endregion Job ID Validation Function

        # region Min Level Validation Function
        def checkValidationMinLevel(*args):
            if len(txtMinLevel.get()) > 3:
                txtMinLevel.set(txtMinLevel.get()[:len(txtMinLevel.get()) - 1])

            for char in txtMinLevel.get():
                if not char.isnumeric():
                    txtMinLevel.set(txtMinLevel.get().replace(char, ''))
        # endregion Min Level Validation Function

        # region Max Level Validation Function
        def checkValidationMaxLevel(*args):
            if len(txtMaxLevel.get()) > 3:
                txtMaxLevel.set(txtMaxLevel.get()[:len(txtMaxLevel.get()) - 1])

            for char in txtMaxLevel.get():
                if not char.isnumeric():
                    txtMaxLevel.set(txtMaxLevel.get().replace(char, ''))
        # endregion Max Level Validation Function

        # region Reset Form Function
        def resetForm():
            for widget in frameInfo.winfo_children():
                if isinstance(widget, ctk.CTkEntry):
                    widget.delete(0, ctk.END)
        # endregion Reset Form Function

        # region Show Jobs List Function
        def showList():
            jobsBLL_Object = JobsBLLClass()
            jobsList = jobsBLL_Object.getJobsList()
            if len(jobsList) > 0:
                tvJobsList.delete(*tvJobsList.get_children())
                rowCount = 0
                for row in jobsList:
                    rowCount += 1
                    values = [rowCount]
                    for value in row:
                        if value is NONE:
                            values.append("")
                        else:
                            values.append(value)
                    tvJobsList.insert("", "end", values=values)
        # endregion Show Jobs List Function

        # region On Tree Selection Function
        def onTreeSelect(event):
            resetForm()
            index = tvJobsList.selection()
            if index:
                selectedRow = tvJobsList.item(index)['values']
                txtJobID.set(str(selectedRow[1]))
                txtJobDescription.set(selectedRow[2])
                txtMinLevel.set(str(selectedRow[3]))
                txtMaxLevel.set(str(selectedRow[4]))
        # endregion On Tree Selection Function

        # endregion Required Functions

        # region Sidebar Frame
        sidebarFrame = ctk.CTkFrame(jobsForm, width=140, corner_radius=0)
        sidebarFrame.grid(row=0, column=0, rowspan=2, sticky="nsew")
        # sidebarFrame.grid_rowconfigure(2, weight=1)

        logoLabel = ctk.CTkLabel(sidebarFrame, text="PUBS", font=ctk.CTkFont(size=20, weight="bold"))
        logoLabel.grid(row=0, column=0, padx=20, pady=(20, 10))

        # region Form Name
        lblFormName = ctk.CTkLabel(sidebarFrame, text="Jobs' Form")
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
            jobsForm.destroy()
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
            jobsForm.destroy()
            from UserInterfaceLayer.Employee_CRUD_Module import EmployeeFormClass
            employeeFormObject = EmployeeFormClass(user=self.User)
            employeeFormObject.employeeFormLoad()

        btnEmployeeCRUD = ctk.CTkButton(sidebarFrame, text="Employees' Form", width=140, command=employeeCRUD,
                                        text_color='#000000', corner_radius=50, hover_color='#007860',
                                        border_width=1, fg_color='#00ffc3')
        btnEmployeeCRUD.grid(row=4, column=0, padx=10, pady=10, sticky=N)

        # endregion Go to Employee Form

        # region Go to Publishers Form
        def publishersCRUD():
            jobsForm.destroy()
            from UserInterfaceLayer.Publishers_CRUD_Module import PublishersFormClass
            publishersFormObject = PublishersFormClass(user=self.User)
            publishersFormObject.publishersFormLoad()

        btnPublishersCRUD = ctk.CTkButton(sidebarFrame, text="Publishers' Form", width=140, command=publishersCRUD,
                                          text_color='#000000', corner_radius=50, hover_color='#007860',
                                          border_width=1, fg_color='#00ffc3')
        btnPublishersCRUD.grid(row=5, column=0, padx=10, pady=10)

        # endregion Go to Publishers Form

        # region Go To Sales Form
        def salesCRUD():
            jobsForm.destroy()
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
            jobsForm.destroy()
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
            jobsForm.destroy()
            from UserInterfaceLayer.Titles_CRUD_Module import TitlesFormClass
            titlesFormObject = TitlesFormClass(user=self.User)
            titlesFormObject.titlesFormLoad()

        btnTitlesCRUD = ctk.CTkButton(sidebarFrame, text="Titles' Form", width=140, command=titlesCRUD,
                                      text_color='#000000', corner_radius=50, hover_color='#007860',
                                      border_width=1, fg_color='#00ffc3')
        btnTitlesCRUD.grid(row=8, column=0, padx=10, pady=10, sticky=N)
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

        #region Treeview Frame
        frmTV = ctk.CTkFrame(jobsForm)
        frmTV.grid(row=0, column=1, padx=10, pady=10, ipadx=10, ipady=10, sticky=NSEW)

        # region Treeview Label
        lblTreeViewPrompt = ctk.CTkLabel(frmTV,text_color='#616161', font=("Helvetica", 12),
                                           text="View List")
        lblTreeViewPrompt.grid(row=0, column=0, padx=10, pady=0, sticky='w')
        # endregion Treeview Label

        # region Columns
        _columns = ['Index', 'JobID', 'JobDescription', 'Min. Level', 'Max. Level']
        _displayColumns = ['Index', 'JobID', 'JobDescription', 'Min. Level', 'Max. Level']
        # endregion Columns

        # region Treeview Widgets
        tvJobsList = ttk.Treeview(frmTV, columns=_columns, displaycolumns=_displayColumns,
                                      show='headings', selectmode='browse')
        tvJobsList.grid(row=1, column=0, padx=10, pady=10, sticky='W')

        tvJobsList.bind('<<TreeviewSelect>>', onTreeSelect)

        tvJobsList.column('#0', width=0)

        tvJobsList.column(column='Index', width=50)
        tvJobsList.heading(text='Index', column='Index')

        tvJobsList.column(column='JobID', width=50)
        tvJobsList.heading(text='Job ID', column='JobID')

        tvJobsList.column(column='JobDescription', width=270)
        tvJobsList.heading(text='Job Description', column='JobDescription')

        tvJobsList.column(column='Min. Level', width=80)
        tvJobsList.heading(text='Min. Level', column='Min. Level')

        tvJobsList.column(column='Max. Level', width=80)
        tvJobsList.heading(text='Max. Level', column='Max. Level')
        # endregion Treeview Widgets

        #endregion Treeview Frame

        # region Jobs's Information Frame
        frameInfo = ctk.CTkFrame(jobsForm)
        frameInfo.grid(row=1, column=1, padx=10, pady=(0, 10), ipadx=10, ipady=10)

        # region Frame Info Label
        lblFrameInfoPrompt = ctk.CTkLabel(frameInfo,text_color='#616161', font=("Helvetica", 12),
                                           text="Jobs' Information")
        lblFrameInfoPrompt.grid(row=0, column=0, padx=10, pady=0, sticky='w')
        # endregion Frame Info Label

        #region Job ID
        lblJobID = ctk.CTkLabel(frameInfo, text='Job ID: ')
        lblJobID.grid(row=1, column=0, padx=10, pady=10, sticky='w')

        txtJobID = StringVar()
        txtJobID.trace('w', checkValidationJobID)
        entJobID = ctk.CTkEntry(frameInfo, width=280, textvariable=txtJobID, corner_radius=50,
                                    border_width=1, border_color='#FFFFFF')
        entJobID.grid(row=1, column=1, padx=10, pady=10, sticky='w')
        #endregion Job ID

        #region Job description
        lblJobDescription = ctk.CTkLabel(frameInfo, text='Job Description: ')
        lblJobDescription.grid(row=2, column=0, padx=10, pady=10, sticky='w')

        txtJobDescription = StringVar()
        entJobDescription = ctk.CTkEntry(frameInfo, width=280, textvariable=txtJobDescription, corner_radius=50,
                                    border_width=1, border_color='#FFFFFF')
        entJobDescription.grid(row=2, column=1, padx=10, pady=10, sticky='w')
        #endregion Job description

        # region Min Level and Max Level
        lblMinMaxLevel = ctk.CTkLabel(frameInfo, text='Min. and Max. Level: ')
        lblMinMaxLevel.grid(row=3, column=0, padx=10, pady=10, sticky='w')

        txtMinLevel = StringVar()
        txtMinLevel.trace('w', checkValidationMinLevel)
        entJobDescription = ctk.CTkEntry(frameInfo, width=130, textvariable=txtMinLevel, corner_radius=50,
                                    border_width=1, border_color='#FFFFFF')
        entJobDescription.grid(row=3, column=1, padx=10, pady=10, sticky='w')

        txtMaxLevel = StringVar()
        txtMaxLevel.trace('w', checkValidationMaxLevel)
        entJobDescription = ctk.CTkEntry(frameInfo, width=130, textvariable=txtMaxLevel, corner_radius=50,
                                    border_width=1, border_color='#FFFFFF')
        entJobDescription.grid(row=3, column=1, padx=10, pady=10, sticky='e')
        # endregion Min Level and Max Level

        #region Register Job Button
        btnRegister = ctk.CTkButton(frameInfo, text='Register Job', width=130, command=duplicateIDCheckRegister,
                                    text_color='#000000', corner_radius=50, hover_color='#007860',
                                    border_width=1, fg_color='#00ffc3')
        btnRegister.grid(row=4, column=1, padx=10, pady=10, sticky='e')
        #endregion Register Job Button

        #region Edit Job Button
        btnEditJob = ctk.CTkButton(frameInfo, text='Edit Job', width=130, command=duplicateIDCheckEdit,
                                      text_color = '#000000', corner_radius = 50, hover_color = '#007860',
                                      border_width = 1, fg_color = '#00ffc3')
        btnEditJob.grid(row=4, column=1, padx=10, pady=10, sticky='w')
        #endregion Edit Job Button

        #region Reset Form Button
        btnResetForm = ctk.CTkButton(frameInfo, text='Clear Form', width=130, command=resetForm,
                                      text_color = '#000000', corner_radius = 50, hover_color = '#007860',
                                      border_width = 1, fg_color = '#00ffc3')
        btnResetForm.grid(row=5, column=1, padx=10, pady=10, sticky='w')
        #endregion Reset Form Button

        #region Delete Job Button
        btnDeleteJob = ctk.CTkButton(frameInfo, text='Delete Job', width=130, command=deleteJobConfirmation,
                                      text_color = '#000000', corner_radius = 50, hover_color = '#910024',
                                      border_width = 1, fg_color = '#ff0040')
        btnDeleteJob.grid(row=5, column=1, padx=10, pady=10, sticky='e')
        #endregion Delete Job Button

        # endregion Jobs's Information Frame

        updateTreeviewStyle()
        showList()
        jobsForm.after(0, setClock)
        jobsForm.mainloop()