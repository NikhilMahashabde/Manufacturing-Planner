################## file: userServiceDb.py ############################### 
#########################################################################
#### DATABASE ACCESS SERVICE LAYER FOR PSQL SPECIFIC FUNCTIONS #########
import psycopg2
from abc import ABC, abstractmethod
import os

############# Generic interface for database accesss
class DatabaseAcessInterface(ABC):

    # table methods
    @abstractmethod
    def dbCreateTable():
        pass

    #CRUD operations for records
    @abstractmethod
    def dbCreateRecord():
        pass

    @abstractmethod
    def dbReadRecord():
        pass

    @abstractmethod
    def dbUpdateRecord():
        pass

    @abstractmethod
    def dbDeleteRecord():
        pass

    @abstractmethod
    def dbGeneric():
        pass
    
 
############# Specific implementation for PSQL database - implements standardised methods from interface

class PGDBAcessService(DatabaseAcessInterface):

    def dbConnect(self):
        self.connection = psycopg2.connect(os.getenv("DATABASE_URL"))
        self.cursor = self.connection.cursor()

    def dbClose(self):
        self.connection.close()

    def dbCreateTable(self, command):
        self.dbConnect()
        self.cursor.execute(command)
        self.connection.commit()
        self.dbClose()
    
    def dbCreateRecord(self, command, args):
        self.dbConnect()
        self.cursor.execute(command, (args))
        self.connection.commit()
        self.dbClose()

    def dbReadRecord(self, searchQuery):
        self.dbConnect()
        self.cursor.execute(searchQuery)
        self.results = self.cursor.fetchall()
        self.connection.commit()
        self.dbClose()
        return self.results

    def dbUpdateRecord(self, command, args):
        self.dbConnect()
        self.cursor.execute(command, (args))
        self.connection.commit()
        self.dbClose()

    def dbDeleteRecord(self,command, args):
        self.dbConnect()
        self.cursor.execute(command, (args))
        self.connection.commit()
        self.dbClose()

    def dbGeneric(self, command, args):
        self.dbConnect()
        self.cursor.execute(command, (args))
        self.connection.commit()
        self.dbClose()
        
__all__ = ['DatabaseAcessInterface','PGDBAcessService']

# db = PGDBAcessService()
# db.dbGeneric('update userdata set email = %s where email = %s' , ('nik.m1992@gmail.com', 'nik.m1992@gmai.com' ))