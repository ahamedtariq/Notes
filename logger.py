def logger(text):
    with open("error_logs.txt","a") as logFile:
        logFile.write(f"{text} ---------------- yes")