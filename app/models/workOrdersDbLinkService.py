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

# detailed status object

class WorkOrderDetailDBStructure():
    def __init__(self, id:int = None, firmed:bool = False, disassembled:bool = False, received: bool = False, reassembled:bool = False, rework:bool = False, closed: bool = False, wonumber:int = False) -> None:
        self.id = id
        self.firmed:bool = firmed
        self.disassembled:bool =disassembled
        self.received:bool = received
        self.reassembled:bool = reassembled
        self.rework:bool = rework
        self.closed:bool = closed
        self.wonumber = wonumber

          
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

    @abstractmethod
    def getWorkOrderHeaderById():
        None
    
    @abstractmethod
    def deleteWorkOrderRecords():
        None
    
    @abstractmethod
    def updateWOlist():
        None
    #  def updateWorkOrderByWoNumber():
    #     None
    
    def readWOheader():
        None

    def getWorkOrderHeaderByIdTest():
        None

    def convertToJson(self, dataInput, className):
        None

    
        

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
    
    def getWorkOrderHeaderById(self, header:WorkOrderListDataDBStructure):

        woid = header.wonumber
        command = f"""SELECT * FROM {self.tableName} WHERE wonumber = {woid}"""
        workorderData = self.dbAccessServiceInstance.dbReadRecord(command)
        woList = self.convertToJson(workorderData,header )
        #print(woList)
        return woList

    def convertToJson(self, dataInput, className):
        wolist = []
        for item in dataInput:
            WoDict = dict(zip(className.__dict__.keys(), item))
            wolist.append(json.dumps(WoDict))
        return wolist
    
    def convertToDict(self, dataInput, className):
        wolist = []
        for item in dataInput:
            WoDict = dict(zip(className.__dict__.keys(), item))
            wolist.append(WoDict)
        return wolist

    def deleteWorkOrderRecords(self, orderNumbers):
        commandList = []

        for orderNumber in orderNumbers:
            searchQuery = f"DELETE FROM {self.tableName} WHERE wonumber = {orderNumber}"
            commandList.append(searchQuery)
        print(commandList)
        self.dbAccessServiceInstance.dbDeleteRecord(commandList)
        return True
    
    def updateWOlist(self, data):
        print("received data.....", data)
        commandList = []
        argsList = []
        command = ''
        args = ()
        for item in data:
            command = """
                                UPDATE workorders
                                SET 
                                wonumber = %s,
                                itemnumber = %s, 
                                itemdescription = %s,
                                quantity = %s,
                                project = %s,
                                duedate = %s
                                WHERE id = %s       
                            """
            args = (item.wonumber, item.itemnumber, item.itemdescription, item.quantity, item.project, item.duedate, item.id)
            commandList.append(command)
            argsList.append(args)

        self.dbAccessServiceInstance.dbUpdateRecord(commandList, argsList)


    def getWorkOrderHeaderByIdTest(self, header:WorkOrderListDataDBStructure):
    
            woid = header.wonumber
            command = f"""SELECT * FROM {self.tableName} WHERE wonumber = %s"""
            args = (woid,)
            return (command, args)
    # def readWOheader(self, woid:int):
    #      command = f"""SELECT * FROM {self.tableName} WHERE wonumber = %s"""
    #     args = (woid,)
    #     return (command, args)
         

# ORM objects 
class WorkOrderDetailsDBLinkService():
    def __init__(self) -> None:
        self.tableName = 'workorderdetail'
        self.dbAccessServiceInstance: DatabaseAcessInterface = PGDBAcessService()
    
    def addWorkOrderDetail(self, data:WorkOrderDetailDBStructure):

        dataDict = vars(data)
        dataDict.pop("id")
        print(dataDict)
        command = f""" 
                    INSERT INTO {self.tableName} 
                    ({", ".join(dataDict.keys())})
                    VALUES 
                    ({", ".join(["%s"] * len(dataDict))})
                    """
        args = tuple(dataDict.values())
        self.dbAccessServiceInstance.dbCreateRecord(command, args)
        return True
    
    def getWorkOrderDetailById(self, detail:WorkOrderDetailDBStructure):

        woid = detail.wonumber
        command = f"""SELECT * FROM {self.tableName} WHERE wonumber = %s"""
        args = (woid,)
        return (command, args)
    

        # woList = self.convertToJson(workorderData)
        # #print(woList)
        # return woList
    


# ORM objects 
# class WorkOrderHistoryDBLinkService():

# # ORM objects 
# class WorkOrderHistoryDBLinkService():

# class WorkOrder


class WorkOrderDBConsolidator():
    
    def __init__(self) -> None:
        self.dbAccessServiceInstance: DatabaseAcessInterface = PGDBAcessService()
        print("started consolidating...")

    def callDB(self, *CalListTupple):

        searchTablesList = []
        print(CalListTupple)
        for item in CalListTupple:

            command,args = item
            searchTablesList.append((command, args))

        data = self.dbAccessServiceInstance.dbReadRecordMultiple(searchTablesList)
        return data





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




__all__ = ['WorkOrdersDbLink','WorkOrdersDbLinkInterface', 'WorkOrderListDataDBStructure', 
           'WorkOrderListDataStructure', 'WorkOrderDBConsolidator', 'WorkOrderDetailDBStructure',
           'WorkOrderDetailsDBLinkService', 
           ]



