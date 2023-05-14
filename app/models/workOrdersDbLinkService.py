# file: workorderDBLinkService.py
from abc import ABC, abstractmethod
from models.dbAcessService import * 
import json
import datetime

####################### WorkOrderListDataStructure #################################
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

class WorkOrderHistoryDBStructure():
    def __init__(self, id= None, wonumber:str = None, time:str = None, signature:str = None, message:str=None) -> None:
       self.id = id
       self.wonumber = wonumber
       self.time = datetime.datetime.now()
       self.signature = signature
       self.message = message

    def stampTime(self):
        self.time = datetime.datetime.now()


class WorkOrderFilesDBStructure():
    def __init__(self, id= None, wonumber:str = None, wotraveller:bytes = None, wopickslip: bytes = None) -> None:
       self.id = id
       self.wonumber = wonumber
       self.wotraveller = wotraveller
       self.wopickslip = wopickslip

    def getWoTraveller(self):
        return self.wotraveller


# insert_query = sql.SQL("INSERT INTO your_table (file_column) VALUES (%s);")
#     cur.execute(insert_query, [psycopg2.Binary(file_data)])
#     conn.commit()
          
#usser database interface -> calls on db access instance. 
class WorkOrdersDbLinkInterface(ABC):

    @abstractmethod
    def addWorkOrder(data:WorkOrderListDataStructure):
        None

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

    def updateWOlistTuple():
        None
    
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
        
    def addWorkOrder(self, data:WorkOrderListDataStructure):

        dataDict = vars(data)
        command = f""" 
                    INSERT INTO {self.tableName} 
                    ({", ".join(dataDict.keys())})
                    VALUES 
                    ({", ".join(["%s"] * len(dataDict))})
                    """
        
        args = tuple(dataDict.values())
        return (command, args)

    
    def getAllWorkOrders(self):
        command = f"""SELECT wo.*, wod.*
                    FROM workorders wo
                    JOIN workorderdetail wod
                    ON wo.wonumber = wod.wonumber;
                    """
        workorderData = self.dbAccessServiceInstance.dbReadRecord(command)

        print(workorderData)
        wolist = []
        for item in workorderData:
            woDict = dict(zip(list(WorkOrderListDataDBStructure().__dict__.keys())+list(WorkOrderDetailDBStructure().__dict__.keys()), item))
            wolist.append(woDict)
       
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
            command = f"""
                                UPDATE {self.tableName}
                                SET 
                                itemnumber = %s, 
                                itemdescription = %s,
                                quantity = %s,
                                project = %s,
                                duedate = %s
                                WHERE wonumber = %s       
                            """
            args = (item.itemnumber, item.itemdescription, item.quantity, item.project, item.duedate, item.wonumber)
            commandList.append(command)
            argsList.append(args)

        self.dbAccessServiceInstance.dbUpdateRecord(commandList, argsList)


    def updateWOlistTuple(self, data):
        print("received data.....", data)
        commandList = []
        argsList = []
        command = ''
        args = ()
        for item in data:
            command = f"""
                                UPDATE {self.tableName}
                                SET 
                                itemnumber = %s, 
                                itemdescription = %s,
                                quantity = %s,
                                project = %s,
                                duedate = %s
                                WHERE wonumber = %s       
                            """
            args = (item.itemnumber, item.itemdescription, item.quantity, item.project, item.duedate, item.wonumber)
            commandList.append(command)
            argsList.append(args)
        return (commandList, argsList)

    def getWorkOrderHeaderByIdTest(self, header:WorkOrderListDataDBStructure):
    
            woid = header.wonumber
            command = f"""SELECT * FROM {self.tableName} WHERE wonumber = %s"""
            args = (woid,)
            return (command, args)
    # def readWOheader(self, woid:int):
    #      command = f"""SELECT * FROM {self.tableName} WHERE wonumber = %s"""
    #     args = (woid,)
    #     return (command, args)
         

############################################################################################################ ORM objects 
##### WORK ORDER DEATIL ############
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

    ######## RETURN Tupple
    def addWorkOrderDetailTupple(self, data:WorkOrderDetailDBStructure):

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
        return (command, args)
    
    def getWorkOrderDetailById(self, detail:WorkOrderDetailDBStructure):

        woid = detail.wonumber
        command = f"""SELECT * FROM {self.tableName} WHERE wonumber = %s"""
        args = (woid,)
        return (command, args)
    
    def updateWOdetail(self, data):
        print("received data.....", data)
        commandList = []
        argsList = []
        command = ''
        args = ()
        for item in data:
            command = f"""
                                UPDATE {self.tableName}
                                SET 
                                firmed = %s, 
                                disassembled = %s,
                                received = %s,
                                reassembled = %s,
                                rework = %s, 
                                closed = %s
                                WHERE wonumber = %s       
                            """
            args = (item.firmed, item.disassembled, item.received, item.reassembled, item.rework, item.closed, item.wonumber )
            commandList.append(command)
            argsList.append(args)
        return (commandList, argsList)
    
############################################################################################################ ORM objects 
class WorkOrderHistoryDBLinkService():
    def __init__(self) -> None:
        self.tableName = 'workorderhistory'
        self.dbAccessServiceInstance: DatabaseAcessInterface = PGDBAcessService()
    
    def addHistoryItem(self, data:WorkOrderHistoryDBStructure):
        
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
        # self.dbAccessServiceInstance.dbCreateRecord(command, args)
        return (command, args)

    def getWorkOrderHistoryById(self, detail:WorkOrderDetailDBStructure):

        woid = detail.wonumber
        command = f"""SELECT * FROM {self.tableName} WHERE wonumber = %s"""
        args = (woid,)
        return (command, args)
    


############################################################################################################ ORM objects 
######### DOCUMENT OBJECT ###############
class WorkOrderFilesDBLinkService():
    def __init__(self) -> None:
        self.tableName = 'workorderfiles'
        self.dbAccessServiceInstance: DatabaseAcessInterface = PGDBAcessService()
    
    def addfilesItem(self, data:WorkOrderFilesDBStructure):
        
        dataDict = vars(data)
        dataDict.pop("id")
        command = f""" 
                    INSERT INTO {self.tableName} 
                    ({", ".join(dataDict.keys())})
                    VALUES 
                    ({", ".join(["%s"] * len(dataDict))})
                    """
        args = tuple(dataDict.values())
        # self.dbAccessServiceInstance.dbCreateRecord(command, args)
        return (command, args)

    def getWorkOrderFilesById(self, detail:WorkOrderDetailDBStructure):

        woid = detail.wonumber
        command = f"""SELECT * FROM {self.tableName} WHERE wonumber = %s"""
        args = (woid,)
        return (command, args)
    
    def updateWorkOrderFilesByWONum(self, data: WorkOrderFilesDBStructure):
        woid = data.wonumber

        query = f"UPDATE {self.tableName} SET "
        update_pairs = []

        if data.wotraveller is not None:
            update_pairs.append("wotraveller = %s")
        if data.wopickslip is not None:
            update_pairs.append("wopickslip = %s")

        query += ", ".join(update_pairs)

        # add the WHERE clause to the query
        query += f" WHERE {data.wonumber} = %s;"

        # create a tuple of parameter values for the query
        param_values = []
        if data.wotraveller is not None:
            param_values.append(data.wotraveller)
        if data.wopickslip is not None:
            param_values.append(data.wopickslip)
        param_values.append(data.wonumber)

        return query, tuple(param_values)

    






##############################################################################################################


class WorkOrderDBConsolidator():
    
    def __init__(self) -> None:
        self.dbAccessServiceInstance: DatabaseAcessInterface = PGDBAcessService()
        #print("started consolidating...")

    def readDB(self, *CalListTupple):

        searchTablesList = []
       # print(CalListTupple)
        for item in CalListTupple:

            command,args = item
            searchTablesList.append((command, args))

        data = self.dbAccessServiceInstance.dbReadRecordMultiple(searchTablesList)
        return data

    def writeDB(self, *setListTupple):
        executeTablesList = []
       
        for item in setListTupple:

            command,args = item
            print(command, args)
            executeTablesList.append((command, args))

        self.dbAccessServiceInstance.dbWriteRecordMultiple(executeTablesList)
        return True
    
    def updateDBzip(self, commands, args):
        self.dbAccessServiceInstance.dbUpdateRecord(commands, args)




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
           'WorkOrderDetailsDBLinkService', 'WorkOrderDetailDBStructure', 'WorkOrderFilesDBStructure', 
           'WorkOrderHistoryDBLinkService', 'WorkOrderHistoryDBStructure', 'WorkOrderFilesDBLinkService']



##
