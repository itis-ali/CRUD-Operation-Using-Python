from Model.Jobs_Module import JobsModelClass
from DataAccessLayer.Jobs_DAL_Module import JobsDALClass

class JobsBLLClass:
    def __init__(self):
        pass

    def registerJobsBLL(self, job:JobsModelClass):
        jobDALObject = JobsDALClass()
        jobDALObject.registerJobDAL(job=job)

    def getJobsList(self):
        jobsDAL_Object = JobsDALClass()
        return jobsDAL_Object.getJobsList()

    def deleteJob(self,jobID):
        jobDAL_Object = JobsDALClass()
        jobDAL_Object.deleteJob(jobID)

    def editJob(self, job: JobsModelClass):
        jobDAL_Object = JobsDALClass()
        jobDAL_Object.editJob(job)

    def getJobIDBLL(self):
        jobDAL_Object = JobsDALClass()
        return jobDAL_Object.getJobID()