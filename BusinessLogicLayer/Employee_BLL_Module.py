from Model.Employee_Module import EmployeeModelClass
from DataAccessLayer.Employee_DAL_Module import EmployeeDALClass

class EmployeeBLLClass:
    def __init__(self):
        pass

    def registerEmployeeBLL(self, employee:EmployeeModelClass):
        employeeDALObject = EmployeeDALClass()
        employeeDALObject.registerEmployeeDal(employee=employee)

    def getJobsList(self):
        employeeDALObject = EmployeeDALClass()
        return employeeDALObject.getJobsList()

    def getJobsLevels(self):
        employeeDALObject = EmployeeDALClass()
        return employeeDALObject.getJobsLevels()

    def getPublishersList(self):
        employeeDALObject = EmployeeDALClass()
        return employeeDALObject.getPublishersList()

    def editEmployee(self, employee:EmployeeModelClass):
        employeeDALObject = EmployeeDALClass()
        employeeDALObject.editEmployee(employee=employee)

    def deleteEmployee(self, empID):
        employeeDALObject = EmployeeDALClass()
        employeeDALObject.deleteEmployee(empID)

    def getEmployeeList(self):
        employeeDALObject = EmployeeDALClass()
        return employeeDALObject.getEmployeeList()

    def getEmployeeIDBLL(self):
        employeeDALObject = EmployeeDALClass()
        return employeeDALObject.getEmployeeID()
