from DataAccessLayer.ConnectionFactory import ConnectionFactoryClass
from Model.Jobs_Module import JobsModelClass

class JobsDALClass:
    def __init__(self):
        pass

    def registerJobDAL(self, job:JobsModelClass):
        commandText = "EXEC [dbo].[RegisterJobs] ?,?,?,?"
        params = (job.JobID, job.JobDesc, job.minLvl, job.maxLvl)

        with ConnectionFactoryClass().makeConnection() as sqlConnection:
            cursor = sqlConnection.cursor()
            cursor.execute(commandText, params)
            sqlConnection.commit()

    def getJobsList(self):
        commandText = "EXEC [dbo].[GetJobsCompleteList]"
        with ConnectionFactoryClass().makeConnection() as sqlConnection:
            cursor = sqlConnection.cursor()
            cursor.execute(commandText, )
            rows = cursor.fetchall()
        return rows

    def editJob(self, job:JobsModelClass):
        commandText = "EXEC [dbo].[EditJob] ?,?,?,?"
        params = (job.JobID, job.JobDesc, job.minLvl, job.maxLvl)

        with ConnectionFactoryClass().makeConnection() as sqlConnection:
            cursor = sqlConnection.cursor()
            cursor.execute(commandText, params)
            sqlConnection.commit()

    def deleteJob(self, jobID):
        commandText = "EXEC [dbo].[DeleteJob] ?"
        params = (jobID,)

        with ConnectionFactoryClass().makeConnection() as sqlConnection:
            cursor = sqlConnection.cursor()
            cursor.execute(commandText, params)
            sqlConnection.commit()

    def getJobID(self):
        commandText = "EXEC [dbo].[GetJobID]"
        with ConnectionFactoryClass().makeConnection() as sqlConnection:
            cursor = sqlConnection.cursor()
            cursor.execute(commandText, )
            rows = cursor.fetchall()
        return rows