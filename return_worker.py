import asyncio
from concurrent.futures import Future
from typing import Optional
from psygnal import Signal
from concurrent.futures import ProcessPoolExecutor,ThreadPoolExecutor

global ProcessPool_Executor,ThreadPool_Executor

ProcessPool_Executor,ThreadPool_Executor = ProcessPoolExecutor(max_workers=4), ThreadPoolExecutor(max_workers=4)

class ReturnProcess():
    update_signal = Signal(object)
    finished_signal = Signal()
    def __init__(self,fn:callable=None,callback:Optional[callable]=None, *args, **kwargs):
        self.fn = fn
        self.callback = callback
        self.args = args
        self.kwargs = kwargs.copy()
        self.executor = ProcessPool_Executor

    def start(self):
        self.future = self.executor.submit(
            self.fn,
            *self.args, 
            **self.kwargs
        )
        if self.callback:
            self.future.add_done_callback(self.callback)
        else:
            self.future.add_done_callback(self._callback)
            
    def _callback(self, future: Future):
        # print(future.result())
        self.update_signal.emit(future.result())
        return future.result()

    def close(self):
        self.executor.shutdown(wait=False)

class AsyncThread():
    update_signal = Signal(object)
    finished_signal = Signal()
    def __init__(self,fn:callable=None,callback:Optional[callable]=None, *args, **kwargs):
        self.fn = fn
        self.callback = callback
        self.args = args
        self.kwargs = kwargs.copy()
        self.executor = ThreadPool_Executor
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
    
    def start(self):
        self.future = self.executor.submit(self.run)
        if self.callback:
            self.future.add_done_callback(self.callback)
        else:
            self.future.add_done_callback(self._callback)
    
    def _callback(self, future: Future):
        # print(future.result())
        self.update_signal.emit(future.result())
        return future.result()
        
    def run(self):
        try:
            self.loop.run_until_complete(self.fn(*self.args, **self.kwargs))
            # asyncio.run(self.fn(*self.args, **self.kwargs))
        except Exception as e:
            self.loop.close()
        finally:
            self.deleteLater()
    def close(self):
        self.executor.shutdown(wait=False)

class SyncThread():
    update_signal = Signal(object)
    finished_signal = Signal()
    def __init__(self,fn:callable=None,callback:Optional[callable]=None, *args, **kwargs):
        self.fn = fn
        self.callback = callback
        self.args = args
        self.kwargs = kwargs.copy()
        self.executor = ThreadPool_Executor

    def start(self):
        self.future = self.executor.submit(
            self.fn,
            *self.args, 
            **self.kwargs
        )
        if self.callback:
            self.future.add_done_callback(self.callback)
        else:
            self.future.add_done_callback(self._callback)
            
    def _callback(self, future: Future):
        # print(future.result())
        self.update_signal.emit(future.result())
        return future.result()

    def close(self):
        self.executor.shutdown(wait=False)
