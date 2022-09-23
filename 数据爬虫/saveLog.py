import time


def saveLog(txt):
    t = time.ctime()
    with open('./Log.txt' , mode = 'a' , encoding='utf-8') as f:
        f.write(t + " ------ " + txt + '\n')

# saveLog('<!!14325!!>')