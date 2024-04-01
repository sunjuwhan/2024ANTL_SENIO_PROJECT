from threading import Thread

def run_a():
    while True:
        print('ad')
        
        
thread_a=Thread(target=run_a)
thread_a.start()

print("adsfadfasdf")