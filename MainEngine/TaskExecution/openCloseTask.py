import os
import webbrowser

def openTaskExec(query):
    appDict = {
        "vs code": r"C:\Users\anike\AppData\Local\Programs\Microsoft VS Code", 
        "chrome": r"C:\Program Files\Google\Chrome\Application\chrome.exe", 
        "postman": r"C:\ProgramData\anike\Postman\Postman.exe", 
        "slack": r"C:\Users\anike\AppData\Local\slack\slack.exe"
    }
    webDict = {"youtube":"https://www.youtube.com/", "google":"https://www.google.com/", "linkedin":"https://www.google.com/"}

    openList = query.replace("open","").split(" ")

    #Handling edge cases
    if "code" in openList:
        openList.push("vs code")

    for i in openList:
        if i in appDict.keys():
            os.startfile(f"{appDict[i]}")
        elif i in webDict.keys():
            webbrowser.open_new_tab(webDict[i])

def closeTaskExec(query):
    appDict = {"chrome":"chrome","postman":"Postman","slack":"slack"}
    appList = query.replace("close","").split(" ")
    for i in appList:
        if i in appDict.keys():
            os.system(f"taskkill /f /im {appDict[i]}.exe")
