import sys  # sys нужен для передачи argv в QApplication
import os
import time
import threading
from multiprocessing import Queue, Pool

from PyQt5 import QtWidgets

# TODO: 
# контроль цпу - явный контроль количества запущенных процессов
# контроль памяти - как-то спрашивать доступную память из питона

# Класть результат в очередь результатов для того, чтобы отрисовывать результат
# Для этого нужен отдельный ПОТОК, который слушает эту очередь
# Ну и ещё нужно по имени файла научиться понимать, какой он по порядку в списке

import design  # Это наш конвертированный файл дизайна

tasks_queue = Queue()
FINISH_TASK = "Finish"


def worker_fun(queue):
    while True:
        task = queue.get()
        print(task, str(time.time()))   
        
        if task == FINISH_TASK:
            break
    return
            


class ExampleApp(QtWidgets.QMainWindow, design.Ui_MyWowApp):
    def __init__(self):
        # Это здесь нужно для доступа к переменным, методам
        # и т.д. в файле design.py
        super().__init__()
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна
        
        self.addTaskButton.clicked.connect(self.upload_new_images)
            
            
    def upload_new_images(self):
        files = QtWidgets.QFileDialog.getOpenFileNames(self,
                                     "Выберите один или несколько файлов",
                                     "/home",
                                     "Images (*.png *.xpm *.jpg)")

        if files:
            for file in files[0]:
                self.tasksListWidget.addItem(file)
                
                tasks_queue.put(file)
                print(tasks_queue.empty(), time.time())
                
                # Запустить счётчик % обработки
                self.processListWidget.addItem("waiting")
                
                
    def closeEvent(self, event):
        for _ in range(PROCESSES_COUNT):
            tasks_queue.put(FINISH_TASK)
            print("Add finish task", tasks_queue.empty(), str(time.time()))
        event.accept()
                
        
def run_app():
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = ExampleApp()  # Создаём объект класса ExampleApp
    window.show()  # Показываем окно
    app.exec_()  # и запускаем приложение
    
    
PROCESSES_COUNT = 4
    
if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    with Pool(PROCESSES_COUNT, worker_fun, (tasks_queue,)) as workers_pool:
        run_app()
    