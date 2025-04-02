from concurrent.futures import Future
from multiprocessing import Process, Queue
import asyncio,os
from asyncio import run
import sys
from threading import Thread
import traceback
from typing import Callable
from PySide6.QtCore import QObject, Signal, QRunnable, Slot

from .threadpool import QThreadPool_global


class WorkerSignals(QObject):
    setdata = Signal(object)  # setdata có graph object
    error = Signal()
    finished = Signal()
    update_signal = Signal(list)
    sig_object = Signal(object)
    sig_process_value = Signal(float)


class ProcessWorker(QRunnable):
    "Worker này dùng để update  data trong một cho graph object khi có data mới"
    def __init__(self, fn, *args, **kwargs):
        super(ProcessWorker, self).__init__()
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals() 
        self.kwargs['sig_process_value'] = self.signals.sig_process_value
        self.kwargs['finished'] = self.signals.finished
        self.threadpool = QThreadPool_global
        self.is_interrupted = False
        self.setAutoDelete(True)
    
    def start(self):
        self.threadpool.start(self)
    
    @Slot()
    def run(self):
        try:
            self.fn(*self.args, **self.kwargs)
        except Exception as e:
            traceback.print_exception(e)
            self.signals.error.emit()
        finally:
            self.signals.finished.emit()  # Done
