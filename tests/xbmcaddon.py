class Addon(object):
    def __init__(self, id=None):
        pass

    def getAddonInfo(self, type):
        pass

    def openSetting(self):
        print "Settings"

    def getSetting(self, type):
        if type == "username": 
            return "A"
        elif type == "password" : 
            return "X"
