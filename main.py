import sys  # sys нужен для передачи argv в QApplication
import os
import time
import threading
from multiprocessing import Queue, Pool
import psutil

from PIL import Image

from PyQt5 import QtWidgets

# TODO: 
# контроль цпу - явный контроль количества запущенных процессов
# контроль памяти - как-то спрашивать доступную память из питона


import design  # Это наш конвертированный файл дизайна

tasks_queue = Queue()
FINISH_TASK = "Finish"
PROCESSES_COUNT = 4

results_queue = Queue()


def worker_fun(tasks_queue, results_queue):
    while True:
        task = tasks_queue.get()
#         print(task, str(time.time()))   
        
        if task == FINISH_TASK:
            results_queue.put(task)
            break
            
        file_name = task.split(' ')[1]
#         print(file_name)
        
        # Проверка того, есть ли доступная память
        # Если доступная память есть - загрузка и обработка картинки
        available_memory = psutil.virtual_memory().available  # объёмы доступной памяти в байтах
        file_size = os.path.getsize(file_name)
        
        # Наверное, нужно проверку доступной памяти и считывание файла в память делать с помощью мьютекса
        # Захватить мьютекс, спросить доступную память, считать файл, если достаточно, отпустить мьютекс
        
        print(available_memory, file_size)
        image = Image.open(file_name)
        
        # Результат - в папку tmp по имени - имя файла
            
        results_queue.put(task)
    return
            


class ExampleApp(QtWidgets.QMainWindow, design.Ui_MyWowApp):
    def __init__(self):
        # Это здесь нужно для доступа к переменным, методам
        # и т.д. в файле design.py
        super().__init__()
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна
        
        self.tasks_count = 0
        self.addTaskButton.clicked.connect(self.upload_new_images)
        
        self.updating_result_thread = threading.Thread(target=self.update_result_info)
        self.updating_result_thread.start()
        
            
    def upload_new_images(self):
        files = QtWidgets.QFileDialog.getOpenFileNames(self,
                                     "Выберите один или несколько файлов",
                                     "/home",
                                     "Images (*.png *.xpm *.jpg)")

        if files:
            for file in files[0]:
                self.tasks_count += 1
                task_name = str(self.tasks_count) + ". " + file
                self.tasksListWidget.addItem(task_name)
                
                tasks_queue.put(task_name)
                print(tasks_queue.empty(), time.time())
                
                # Запустить счётчик % обработки
                self.processListWidget.addItem(str(self.tasks_count) + ". waiting")
                
                
    def update_result_info(self):
        while True:
            task = results_queue.get()
            if task == FINISH_TASK:
                break
                
            task_id = task.split('.')[0]
            
            self.processListWidget.item(int(task_id) - 1).setText(task_id + ". ready")
        return
        
                
    def closeEvent(self, event):
        for _ in range(PROCESSES_COUNT):
            tasks_queue.put(FINISH_TASK)
        event.accept()
        
        
        
def run_app():
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = ExampleApp()  # Создаём объект класса ExampleApp
    window.show()  # Показываем окно
    app.exec_()  # и запускаем приложение
    
    
if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    with Pool(PROCESSES_COUNT, worker_fun, (tasks_queue, results_queue,)) as workers_pool:
        run_app()
    
    