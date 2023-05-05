# file: workorderDBLinkService.py
from abc import ABC, abstractmethod
from models.dbAcessService import * 
import json

#when adding to DB
class WorkOrderListDataStructure():
    def __init__(self, wonumber:int = None, itemnumber:str = None, itemdescription:str = None, project:str = None, quantity:int = None, duedate:str = None) -> None:
        self.wonumber: int = wonumber
        self.itemnumber: str = itemnumber
        self.itemdescription: str = itemdescription
        self.project:str = project
        self.quantity:int = quantity
        self.duedate:str = duedate

    def printStructure(self):
        print((item for item in self), " ")

#when returning data from db 
class WorkOrderListDataDBStructure(WorkOrderListDataStructure):
    def __init__(self, id:int = None, wonumber:int = None, itemnumber:str = None, itemdescription:str = None, project:str = None, quantity:int = None, duedate:str = None) -> None:
        self.id = id
        super().__init__(wonumber, itemnumber, itemdescription, project, quantity, duedate)

    def printStructure(self):
        print((item for item in self), " ")
      
#usser database interface -> calls on db access instance. 
class WorkOrdersDbLinkInterface(ABC):

    @abstractmethod
    def addWorkOrder(data:WorkOrderListDataStructure):
        None

    # @abstractmethod
    # def getWorkOrderByWONumber():
    #     None

    @abstractmethod
    def getAllWorkOrders():
        None

    # @abstractmethod
    # def updateWorkOrderByWoNumber():
    #     None
        

class WorkOrdersDbLink(WorkOrdersDbLinkInterface):
    def __init__(self) -> None:
        self.dbAccessServiceInstance: DatabaseAcessInterface = PGDBAcessService()
        self.tableName = 'workorders'
        

    def createWorkOrdersTable(self):
        command = f"""
                    CREATE TABLE {self.tableName} (
                        id SERIAL PRIMARY KEY,
                        wonumber INT NOT NULL,
                        itemnumber TEXT NOT NULL,
                        itemdescription TEXT NOT NULL,
                        project TEXT NOT NULL,
                        quantity INT NOT NULL, 
                        duedate TEXT NOT NULL
                    );"""
        self.dbAccessServiceInstance.dbCreateTable(command)
        return True    
  
    def addWorkOrder(self, data:WorkOrderListDataStructure):

        dataDict = vars(data)
        command = f""" 
                    INSERT INTO {self.tableName} 
                    ({", ".join(dataDict.keys())})
                    VALUES 
                    ({", ".join(["%s"] * len(dataDict))})
                    """
        
        args = tuple(dataDict.values())
        self.dbAccessServiceInstance.dbCreateRecord(command, args)
        return True
    
    def getAllWorkOrders(self):
        command = f"""SELECT * FROM {self.tableName}"""
        workorderData = self.dbAccessServiceInstance.dbReadRecord(command)

        wolist = []
        for item in workorderData:
            woDict = dict(zip(WorkOrderListDataDBStructure().__dict__.keys(), item))
            wolist.append(json.dumps(woDict))
       
        return wolist

    # def getUserAuthByEmail(self, emailId):
    #     searchQuery = f"SELECT * FROM userdata WHERE email = '{emailId}'"
    #     results:UserAuthDBStructure = UserAuthDBStructure(*self.dbAccessServiceInstance.dbReadRecord(searchQuery)[0])
    #     return results
    
    # def getUserAuthById(self, id):
    #     searchQuery = f"SELECT * FROM userdata WHERE id = '{id}'"
    #     results:UserAuthDBStructure = UserAuthDBStructure(*self.dbAccessServiceInstance.dbReadRecord(searchQuery)[0])
    #     return results
    
    # def updateUserAuth(self, data:UserAuthDBStructure):
    #     command = """
    #                     UPDATE userdata
    #                     SET 
    #                     name = %s,
    #                     email = %s,
    #                     isAdmin = %s,
    #                     password_hash = %s  
    #                     where id = %s       
    #                 """
    #     args = (data.name, data.email, data.isAdmin, data.password_hash, data.id)
    #     self.dbAccessServiceInstance.dbUpdateRecord(command, args)


#updatemain:UserAuthDBStructure = UserAuthDBStructure(1, '123', 'nikhil', 'nik.m1992@gmail.com', )., True)
# bcrypt.hashpw('test'.encode(), bcrypt.gensalt().decode()

# maketable = WorkOrdersDbLink()
# print(maketable.getAllWorkOrders())


# wokone:WorkOrderListDataStructure =WorkOrderListDataStructure(42548, "tridonic", "driver", "marvel", 29, "05/05/2020")
# maketable.addWorkOrder(wokone)

# print(maketable.getAllWorkOrders())


__all__ = ['WorkOrdersDbLink','WorkOrdersDbLinkInterface', 'WorkOrderListDataDBStructure', 'WorkOrderListDataStructure']



