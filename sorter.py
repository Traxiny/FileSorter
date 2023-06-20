import os
import argparse
import datetime
import calendar
import shutil

#os.chdir 
# os.path.exists(test_path)
# os.listdir(picture_path) 
# os.path.getsize(filePath),
# print(datetime.datetime.fromtimestamp(os.path.getctime(f))) # time of creation
# print(os.stat(f).st_mode)

class File:
    def __init__(self, fName, location, modifiedDate) -> None:
        self.fileName = fName
        self.fileType = fName.split('.')[1]
        self.location = location
        self.Date = modifiedDate

    
class Sorter:
    def __init__(self, args) -> None:
        self.root_path = os.path.dirname(os.path.realpath(__file__))
        self.__CheckFolders(args.oldFolder, args.newFolder)

    def __CheckFolders(self, oldFolderName, newFolderName): #check if oldFolderName exists and create newFolderName
        if oldFolderName[:2] == "./": # ./name
            self.old_path = self.root_path + f"/{oldFolderName[2:]}"
            self.__CheckPath(self.old_path)
            #print(self.old_path)
        if newFolderName[:2] == "./": # ./name
            self.sorted_path = self.root_path + f"/{newFolderName[2:]}"
            self.__CheckPath(self.sorted_path)
            #print(self.sorted_path)
    
    def __CheckPath(self, path):
        if not os.path.exists(path): exit(404)

    def copyToNewFolderByDate(self, folderPath):
        for root, dirs, files in os.walk(folderPath):
            for fileName in files:
                filePath = os.path.join(root, fileName)
                newFile = File(fileName, filePath, datetime.date.fromtimestamp(os.path.getmtime(filePath)))

                newLocation = self.sorted_path + f"/{newFile.Date.year}/{self.__monthToName(newFile.Date.month)}"
                newLocation = self.__makeNewPathDate(newLocation)
                if os.path.exists(newLocation + f"/{fileName}"): continue

                print(f"Copying {filePath} to {newLocation}")
                shutil.copy(filePath, newLocation)

    def __makeNewPathDate(self, path):
        if not os.path.exists(path): 
            os.makedirs(path)
            return path
        return path
    
    def __monthToName(self, month):
        return calendar.month_name[month]
    
def GetArgs():
    argParser = argparse.ArgumentParser(description="Sorter.py sorts files from one folder and transfers them into another one sorted by specification.",
                                        epilog="I don't know man...\nNice cock?")
    argParser.add_argument('oldFolder')
    argParser.add_argument('newFolder')
    argParser.add_argument('-s', '--sortBy')
    group = argParser.add_mutually_exclusive_group(required=True)
    group.add_argument('-c', '--copy', action='store_true')
    group.add_argument('-m', '--move', action='store_true')
    args = argParser.parse_args()

    return args

if __name__ == "__main__":
    sorter = Sorter(GetArgs())
    sorter.copyToNewFolderByDate(sorter.old_path)

