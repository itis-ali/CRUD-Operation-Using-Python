from Model.Stores_Module import StoresModelClass
from DataAccessLayer.Stores_DAL_Module import StoresDALClass

class StoresBLLClass:
    def __init__(self):
        pass

    def registerStoresBLL(self, store:StoresModelClass):
        storesDALObject = StoresDALClass()
        storesDALObject.registerStoresDAL(store=store)

    def getStoresList(self):
        storesDAL_Object = StoresDALClass()
        return storesDAL_Object.getStoresList()

    def deleteStore(self, storeID):
        storesDAL_Object = StoresDALClass()
        storesDAL_Object.deleteStore(storeID)

    def editStore(self, store: StoresModelClass):
        storesDAL_Object = StoresDALClass()
        storesDAL_Object.editStore(store)

    def getStoreIDBLL(self):
        storesDAL_Object = StoresDALClass()
        return storesDAL_Object.getStoreID()