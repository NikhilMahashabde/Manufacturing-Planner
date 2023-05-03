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
        newUser:UserAuthDataStructure = UserAuthDataStructure(request.form['name'], request.form['email'], request.form['password'], bool(request.form['isAdmin'])  )
       # newUser.printUserAuthDataStructure()


    def getAllUserAuthData(self):
        allUserData = self.userDBLinkService.getAllUsers()
        return allUserData
    

    def updateAllUserAuthData(self, request):
        i = 1
        while f'{i}.id' in request.form:

            currentData:UserAuthDBStructure = self.userDBLinkService.getUserAuthById(i)
            if request.form.get(f'{i}.password') is not "":
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
            i+=1

__all__ = ['UserAuthService','UserAuthInterface']