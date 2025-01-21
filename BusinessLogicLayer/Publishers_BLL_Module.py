from Model.Publishers_Module import PublishersModelClass
from DataAccessLayer.Publishers_DAL_Module import PublishersDALClass

class PublishersBLLClass:
    def __init__(self):
        pass

    def registerPublishersBLL(self, publisher:PublishersModelClass):
        publisherDALObject = PublishersDALClass()
        publisherDALObject.registerPublishersDAL(publisher=publisher)

    def getPublishersList(self):
        publishersDAL_Object = PublishersDALClass()
        return publishersDAL_Object.getPublishersList()

    def deletePublisher(self, pubID):
        publishersDAL_Object = PublishersDALClass()
        publishersDAL_Object.deletePublisher(pubID)

    def editPublisher(self, publisher: PublishersModelClass):
        publishersDAL_Object = PublishersDALClass()
        publishersDAL_Object.editPublisher(publisher)

    def getPublisherIDBLL(self):
        publishersDAL_Object = PublishersDALClass()
        return publishersDAL_Object.getPublisherID()
