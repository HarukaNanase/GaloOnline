import os

UsersPath = "./users/"
FileExtension = ".txt"


def CheckDir():
    if os.path.exists(UsersPath):
        return True
    else:
        os.makedirs(UsersPath)
        return False


def CreateAccount(name, password, Accounts):
    if os.path.isfile(UsersPath + name + FileExtension) or name in Accounts:
        return False
    else:
        try:
            userfile = open(UsersPath + name + FileExtension, 'a+')
            userfile.write(password)
            userfile.close()
            Accounts[name] = password
            print("Account created!")
            #return accounts
        except IOError:
            print("Error opening file.")
            return False


def LoadAccounts(Accounts):
    files = []
    for(dirpath, dirnames, filenames) in os.walk(UsersPath):
        files.extend(filenames)
    for(FileName) in files:
        try:
            OpenFile = open(UsersPath + FileName)
            UserPassword = OpenFile.read()
            OpenFile.close()
            username = os.path.splitext(FileName)
            Accounts[username[0]] = UserPassword
        except IOError:
            print("Error loading account database... Server won't be loaded with any account")
            continue


def Login(name, password, Accounts, LoggedInUsers, UserIP):
    if os.path.isfile(UsersPath + name + FileExtension) or name in Accounts:
        try:
            userfile = open(UsersPath + name + FileExtension, 'r')

            userData = userfile.read()

            userData = userData.split()

            passUser = userData[0]

            userfile.close()
            if password == passUser:
                LoggedInUsers[name] = UserIP, "Online"
                return True
            else:
                return False
        except IOError:
            print("Error while reading file during login.")
            return False
    else:
        return False

def CheckLogin(LoggedInUsers, User):
    for a in LoggedInUsers:
        if a == User:
            return True
    return False