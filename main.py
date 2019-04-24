import sys  # sys нужен для передачи argv в QApplication
import os
import time
import threading
from multiprocessing import Queue, Pool
import psutil
import shutil

import cv2

from PyQt5 import QtWidgets, QtGui, QtCore

# TODO: 
# контроль цпу - явный контроль количества запущенных процессов
# контроль памяти - как-то спрашивать доступную память из питона

# Ещё такой момент, как лучше, открывать отдельное окно с картинкой? Наверное, да. Точнее окно с двумя картинками


import design  # Это наш конвертированный файл дизайна
import images_shower

tasks_queue = Queue()
FINISH_TASK = "Finish"
PROCESSES_COUNT = 4

WAITING_TEXT = "waiting"
READY_TEXT = "ready"

TMP_DIRECTORY = "tmp"

SHOWING_IMAGE_WIDTH = 526
SHOWING_IMAGE_HEIGHT = 669

results_queue = Queue()


def binarize_image(image):
    """
    Принимает картинку в виде numpy-массива BGR
    """
    image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    _, image = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return image


def save_tmp_image(image, file_path):
    if not os.path.exists(TMP_DIRECTORY):
        os.mkdir(TMP_DIRECTORY)
    _, file_name = os.path.split(file_path)
    result_path = os.path.join(TMP_DIRECTORY, file_name)
    cv2.imwrite(result_path, image)


def worker_fun(tasks_queue, results_queue):
    while True:
        task = tasks_queue.get()
#         print(task, str(time.time()))   
        
        if task == FINISH_TASK:
            results_queue.put(task)
            break
            
        file_name = task.split(' ')[1]
        print(task)
        
        # Проверка того, есть ли доступная память
        # Если доступная память есть - загрузка и обработка картинки
        available_memory = psutil.virtual_memory().available  # объёмы доступной памяти в байтах
        file_size = os.path.getsize(file_name)
        
        # Наверное, нужно проверку доступной памяти и считывание файла в память делать с помощью мьютекса
        # Захватить мьютекс, спросить доступную память, считать файл, если достаточно, отпустить мьютекс
        
        print(available_memory, file_size)
        
        image = cv2.imread(file_name)
        image = binarize_image(image)
        
        # Результат - в папку tmp по имени - имя файла        
        save_tmp_image(image, file_name)
        
            
        results_queue.put(task)
    return
            

class ImagesWindow(QtWidgets.QMainWindow, images_shower.Ui_ImagesShower):
    def __init__(self, file_path):
        super().__init__()
        self.setupUi(self)
        
        label_original_image = QtWidgets.QLabel(self.originalImageFrame) 
        original_image_object = QtGui.QImage(file_path)
        original_image_object = original_image_object.scaled(SHOWING_IMAGE_WIDTH, SHOWING_IMAGE_HEIGHT, 
                                                             aspectRatioMode=QtCore.Qt.KeepAspectRatio,
                                                             transformMode=QtCore.Qt.SmoothTransformation)  
        label_original_image.setPixmap(QtGui.QPixmap.fromImage(original_image_object)) 
        
        _, file_name = os.path.split(file_path)
        tmp_path = os.path.join(TMP_DIRECTORY, file_name)
        
        label_result_image = QtWidgets.QLabel(self.resultImageFrame) 
        result_image_object = QtGui.QImage(tmp_path)
        result_image_object = result_image_object.scaled(SHOWING_IMAGE_WIDTH, SHOWING_IMAGE_HEIGHT, 
                                                         aspectRatioMode=QtCore.Qt.KeepAspectRatio,
                                                         transformMode=QtCore.Qt.SmoothTransformation)  
        label_result_image.setPixmap(QtGui.QPixmap.fromImage(result_image_object))
        
        
class MainApp(QtWidgets.QMainWindow, design.Ui_MyWowApp):
    def __init__(self):
        # Это здесь нужно для доступа к переменным, методам
        # и т.д. в файле design.py
        super().__init__()
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна
        
        self.tasks_count = 0
        self.addTaskButton.clicked.connect(self.upload_new_images)
        self.saveAllResultsButton.clicked.connect(self.save_all_results)
        self.tasksListWidget.itemActivated.connect(self.task_selected_event)        
        
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
                self.processListWidget.addItem(str(self.tasks_count) + ". " + WAITING_TEXT)
                
                
    def update_result_info(self):
        while True:
            task = results_queue.get()
            if task == FINISH_TASK:
                break
                
            task_id = task.split('.')[0]
            
            self.processListWidget.item(int(task_id) - 1).setText(task_id + ". " + READY_TEXT)
        return
        
        
    def check_if_the_task_is_ready(self, task_id):
        """
        task_id - число int, по которому можно получить элемент в processListWidget
        Возвращает True, если задача выполнена и False иначе
        """
        process_text = self.processListWidget.item(task_id).text().split(' ')[1]
        if process_text == READY_TEXT:
            return True
        return False
        
        
    def task_selected_event(self, item):
        split_item_text = item.text().split(' ')
        file_path = split_item_text[1]
        task_id = int(split_item_text[0].split('.')[0]) - 1
        print("SELECTED ITEM:", file_path)
        
        # Проверяем, что задача выполнена, и только если она выполнена, открываем новое окно с картинкой
        if self.check_if_the_task_is_ready(task_id):
            self.images_dialog = ImagesWindow(file_path)
            self.images_dialog.show()        
        
        
    def save_all_results(self):
        directory_to_save = str(QtWidgets.QFileDialog.getExistingDirectory(self, "Select Directory"))
        
        # Копируем файлы из папки tmp в directory_to_save        
        for file_name in os.listdir(TMP_DIRECTORY):
            tmp_path = os.path.join(TMP_DIRECTORY, file_name)
            shutil.copy(tmp_path, directory_to_save)
        
                
    def closeEvent(self, event):
        for _ in range(PROCESSES_COUNT):
            tasks_queue.put(FINISH_TASK)
            
        if os.path.exists(TMP_DIRECTORY):
            shutil.rmtree(TMP_DIRECTORY)
            
        event.accept()
        
        
        
def run_app():
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = MainApp()  # Создаём объект класса ExampleApp
    window.show()  # Показываем окно
    app.exec_()  # и запускаем приложение
    
    
if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    with Pool(PROCESSES_COUNT, worker_fun, (tasks_queue, results_queue,)) as workers_pool:
        run_app()
    
    