import queue
from multiprocessing.managers import BaseManager
from multiprocessing import freeze_support

#服务进程

#任务个数
task_number = 10
#定义收发队列
task_queue = queue.Queue(task_number)
result_queue = queue.Queue(task_number)

def get_task():
    return task_queue
def get_result():
    return result_queue

#创建类似的QueueManager
class QueueManager(BaseManager):
    pass
def win_run():
    #Windows下绑定调用接口
    QueueManager.register('get_task_queue',callable=get_task)
    QueueManager.register('get_result_queue',callable=get_result)
    #绑定端口并设置验证口令，Windows下需要填写IP地址
    manager = QueueManager(address=('127.0.0.1',8001),authkey='qiye'.encode('utf-8'))
    #启动
    manager.start()
    try:
        #通过网络获取任务队列和结果队列
        task = manager.get_task_queue()
        result = manager.get_result_queue()
        #添加任务
        for url in ['ImageUrl_'+str(i) for i in range(10)]:
            print('put task %s...'%url)
            task.put(url)
        print('try get result...')
        for i in range(10):
            print('result is %s '%result.get(timeout=10))
    except:
        print('Manager error')
    finally:
            #一定要关闭，否则会报管道未关闭的错误
            manager.shutdown()
if __name__ == '__main__':
    #Windows多线程可能有问题，进行缓解
    freeze_support()
    win_run()

