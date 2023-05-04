#Work order service.py
from models.workOrdersDbLinkService import *
from abc import ABC, abstractmethod

########################## Work order master interface -> two services ########################
class WorkOrderServiceInterface(ABC):
        
        @abstractmethod
        def getAllWorkOrders(self):
            pass
        

        # def menuAdd(self):
        #     pass
        
        # def getMenuItem(self):
        #     pass

        # def menuItemEdit(self):
        #     pass

        # def menuItemDelete(self):
        #     pass
        
class WorkOrderService(WorkOrderServiceInterface):
    
    def __init__(self) -> None:
        self.WorkOrderDBInstance:WorkOrdersDbLinkInterface = WorkOrdersDbLink()

    def getAllWorkOrders(self):
        return self.WorkOrderDBInstance.getAllWorkOrders()
    
    # def menuAdd(self, request):
    #     newItem:MenuItemStructure = MenuItemStructure( request.form['name'], request.form['URL'], request.form['price'])
    #     self.fTdatabaseInstance.addNewFoodItem(newItem)

    # def getMenuItem(self, menuId):
    #     searchById = 'id'
    #     result = self.fTdatabaseInstance.searchFoodRecord(searchById, menuId)
    #     return result
    
    # def menuItemEdit(self, request):
    #     self.newItemEdit:MenuItemStructure =  MenuItemStructure( request.form['name'], request.form['URL'], request.form['price'])
    #     self.newItemId = request.form['id']
    #     self.fTdatabaseInstance.updateFoodRecord(self.newItemId, self.newItemEdit)

    # def menuItemDelete(self, request):
    #     self.newItemId = request.form['id']
    #     if 'submitYes' in request.form:
    #         self.fTdatabaseInstance.deleteFoodRecord(self.newItemId)
    #         return True
    #     elif 'submitNo' in request.form:
    #         return False

__all__ = ['WorkOrderService', 'WorkOrderServiceInterface']