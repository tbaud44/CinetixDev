
theDir = "C:\Users\PC-BA\git\CinetixDev\CineDev"
Dim WShell
Set WShell = CreateObject("WScript.Shell")
WShell.CurrentDirectory = theDir
WShell.Run "C:\Users\PC-BA\AppData\Local\Programs\Python\Python35\python.exe Cinetix.py", 0
