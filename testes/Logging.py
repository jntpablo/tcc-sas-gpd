import datetime
def writeLog(msg):
    now = datetime.datetime.now()
    nowFormatted = now.strftime("%Y-%m-%d %H:%M:%S ")
    logFileName = now.strftime("%Y-%m-%d")
    file = open(logFileName + ".log","a+") 
    file.write(nowFormatted + msg + "\n") 
    file.close() 
    return

def writeLogInfo(msg):
    writeLog("[INFO].....: " + msg)
    return    

def writeLogError(msg):
    writeLog("[ERROR]....: " + msg)
    return

def writeLogSuccess(msg):
    writeLog("[SUCESSO]..: " + msg)
    return

writeLogInfo("Teste info")
writeLogError("Teste error")
writeLogSuccess("Teste success")