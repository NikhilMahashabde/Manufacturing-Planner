############# UserAuthInterface

# file: userAuthService.py
from abc import ABC, abstractmethod
from models.userAuthDbLinkService import * 
from flask import session 
import bcrypt

#################

class UserAuthInterface(ABC):
    @abstractmethod
    def checkLogin():
        pass

    @abstractmethod
    def getUserAuthName():
        pass

    @abstractmethod
    def addUserAuth():
        pass

    @abstractmethod
    def getAllUserAuthData():
        pass

    @abstractmethod
    def updateAllUserAuthData():
        pass

    @abstractmethod
    def deleteUserAuthData(request):
        pass

class UserAuthService(UserAuthInterface):

    def __init__(self) -> None:
        self.userDBLinkService: UserAuthDbLinkInterface = UserAuthDbLink()
       
    def checkLogin(self, request, session):
        email = request.form.get("email")
        password = request.form.get("password")
        userAuthData:UserAuthDBStructure = self.userDBLinkService.getUserAuthByEmail(email)

        print("Email:",userAuthData.email,"emailEntered: ", email, "pwenter: ",password, "pwEnterEncoded: ", password.encode(),"pwDBhash:", userAuthData.password_hash, "- " )

        if ((userAuthData.email == email) and bcrypt.checkpw(password.encode(), userAuthData.password_hash.encode())):
            session["user_id"] = userAuthData.id
            return True
        return False
    
    def getUserAuthData(self, session):
        userAuthData:UserAuthDBStructure = self.userDBLinkService.getUserAuthById(session.get("user_id", ""))
        return userAuthData
    
    def getUserAuthName(self, session):
        if not session.get("user_id", ""): return ""
        userAuthData:UserAuthDBStructure = self.userDBLinkService.getUserAuthById(session.get("user_id", ""))
        print(userAuthData.name)
        return userAuthData.name
    
    def addUserAuth(self, request):

        if 'input.user.isAdmin' in request.form:
            isAdmin:bool = request.form['input.user.isAdmin']
        else:
            isAdmin:bool = False

        newUser:UserAuthDataStructure = UserAuthDataStructure(request.form['name'], request.form['email'], 'test', isAdmin, 
            bcrypt.hashpw(request.form.get('password').encode(), bcrypt.gensalt()).decode())
        newUser.printUserAuthDataStructure()
        return self.userDBLinkService.addUserAuth(newUser)

    def getAllUserAuthData(self):
        allUserData = self.userDBLinkService.getAllUsers()
        return allUserData
    

    def updateAllUserAuthData(self, request):
        
        formIdCount:int = len(request.form)/6
        formData = list(request.form.items())
        print(request.form)
        i:int = 0
        entryCount:int = 0
        while entryCount < formIdCount:
            i+=1
            if f'{i}.id' in formData[entryCount*6]:

                currentData:UserAuthDBStructure = self.userDBLinkService.getUserAuthById(i)
                if request.form.get(f'{i}.password') != "":
                    passwordUpdate = bcrypt.hashpw(request.form.get(f'{i}.password').encode(), bcrypt.gensalt()).decode()
                else:
                    passwordUpdate = currentData.password_hash

                item:UserAuthDBStructure = UserAuthDBStructure(request.form.get(f'{i}.id'),
                                                                request.form.get(f'{i}.uuid'),
                                                                request.form.get(f'{i}.name'),
                                                                request.form.get(f'{i}.email'),
                                                                request.form.get(f'{i}.isadmin'),
                                                                passwordUpdate)
                self.userDBLinkService.updateUserAuth(item)
                entryCount += 1
                


    def deleteUserAuthData(self, request):

        for item in request.form:
            id = item.split('.')[1]
            self.userDBLinkService.deleteUserAuthRecord(id)

        pass

__all__ = ['UserAuthService','UserAuthInterface']