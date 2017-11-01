
theDir = "C:\Users\HOME\repogit\CineDev"
Dim WShell
Set WShell = CreateObject("WScript.Shell")
WShell.CurrentDirectory = theDir
WShell.Run "C:\Python36-32\python.exe Cinetix.py", 0
