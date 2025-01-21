from DataAccessLayer.ConnectionFactory import ConnectionFactoryClass
from Model.Employee_Module import EmployeeModelClass

class EmployeeDALClass:
    def __init__(self):
        pass

    def registerEmployeeDal(self, employee:EmployeeModelClass):
        commandText = "EXEC [dbo].[RegisterEmployee] ?, ?, ?, ?, ?, ?, ?, ?"
        params = (employee.EmployeeID, employee.FirstName, employee.MiddleName, employee.LastName,
                  employee.Job, employee.JobLevel, employee.PublishersID, employee.HireDate)

        with ConnectionFactoryClass().makeConnection() as sqlConnection:
            cursor = sqlConnection.cursor()
            cursor.execute(commandText, params)
            sqlConnection.commit()

    def getJobsList(self):
        commandText = "EXEC [dbo].[GetJobsList]"

        with ConnectionFactoryClass().makeConnection() as sqlConnection:
            cursor = sqlConnection.cursor()
            cursor.execute(commandText, )
            rows = cursor.fetchall()
        return rows

    def getJobsLevels(self):
        commandText = "EXEC [dbo].[GetJobsInformation]"

        with ConnectionFactoryClass().makeConnection() as sqlConnection:
            cursor = sqlConnection.cursor()
            cursor.execute(commandText, )
            rows = cursor.fetchall()
        return rows

    def getPublishersList(self):
        commandText = "EXEC [dbo].[GetPublishersName]"

        with ConnectionFactoryClass().makeConnection() as sqlConnection:
            cursor = sqlConnection.cursor()
            cursor.execute(commandText, )
            rows = cursor.fetchall()
        return rows

    def editEmployee(self, employee: EmployeeModelClass):
        commandText = "EXEC	 [dbo].[EditEmployee] ?,?,?,?,?,?,?,?"
        params = (employee.EmployeeID, employee.FirstName, employee.MiddleName, employee.LastName,
                  employee.Job, employee.JobLevel, employee.PublishersID, employee.HireDate)
        with ConnectionFactoryClass().makeConnection() as sqlConnection:
            cursor = sqlConnection.cursor()
            cursor.execute(commandText, params)
            sqlConnection.commit()

    def deleteEmployee(self, empID):
        commandText = "EXEC [dbo].[DeleteEmployee] ?"
        params = (empID,)
        with ConnectionFactoryClass().makeConnection() as sqlConnection:
            cursor = sqlConnection.cursor()
            cursor.execute(commandText, params)
            sqlConnection.commit()

    def getEmployeeList(self):
        commandText = "EXEC [dbo].[GetEmployeeList]"
        with ConnectionFactoryClass().makeConnection() as sqlConnection:
            cursor = sqlConnection.cursor()
            cursor.execute(commandText, )
            rows = cursor.fetchall()
        return rows

    def getEmployeeID(self):
        commandText = "EXEC [dbo].[GetEmployeeID]"
        with ConnectionFactoryClass().makeConnection() as sqlConnection:
            cursor = sqlConnection.cursor()
            cursor.execute(commandText, )
            rows = cursor.fetchone()
        return rows[0]


