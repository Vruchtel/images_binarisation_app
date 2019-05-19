import sys  # sys нужен для передачи argv в QApplication
import os
import time
import threading
from multiprocessing import Queue, Pool, Manager, Lock, current_process
import psutil
import shutil

import cv2

from PyQt5 import QtWidgets, QtGui, QtCore

import design  # Это наш конвертированный файл дизайна
import images_shower

tasks_queue = Queue()
unblocking_queue = Queue()

FINISH_TASK = "Finish"
BLOCKING_TASK = "Block"
PROCESSES_COUNT = 10
START_PROCESSES_COUNT = 4

WAITING_TEXT = "waiting"
READY_TEXT = "ready"

TMP_DIRECTORY = "tmp"

SHOWING_IMAGE_WIDTH = 526
SHOWING_IMAGE_HEIGHT = 669

RIGHT_EFFICIENCY = 0.8
LEFT_EFFICIENCY = 0.4

results_queue = Queue()

atomic_operation = Lock()


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


def worker_fun(tasks_queue, results_queue, unblocking_queue, namespace, atomic_operation):
    
    unblocking_task = unblocking_queue.get()
    
    namespace.currently_working_processes += 1
    
    while True:
        
        task = tasks_queue.get()
        
        if task == FINISH_TASK:  
            results_queue.put(task)
            break
            
        if task == BLOCKING_TASK:  
            atomic_operation.acquire()
            if namespace.currently_working_processes != 1: # Никогда не блокируем первый поток
                namespace.currently_working_processes -= 1
                atomic_operation.release()
                unblocking_task = unblocking_queue.get()
                namespace.currently_working_processes += 1
            else:
                atomic_operation.release()
                tasks_queue.put(BLOCKING_TASK)
            continue
            
        file_name = task.split(' ')[1]
        
        # Проверка того, есть ли доступная память
        # Если доступная память есть - загрузка и обработка картинки
        file_size = os.path.getsize(file_name)
        
        namespace.currently_taking_memory += file_size
        available_memory = psutil.virtual_memory().available  # объёмы доступной памяти в байтах
        
        if namespace.currently_taking_memory >= (available_memory - 1024):
            # Запускать задачу не можем, кладём её обратно в очередь
            tasks_queue.put(task)
            namespace.currently_taking_memory -= file_size
            continue        
            
        # Время работы начинаем замерять отсюда
        start_all_time, start_process_time = time.time(), time.process_time()
        
        image = cv2.imread(file_name)
        namespace.currently_taking_memory -= file_size
        image = binarize_image(image)
        
        # Результат - в папку tmp по имени - имя файла        
        save_tmp_image(image, file_name)
        
        # Время работы заканчиваем замерять здесь
        end_all_time, end_process_time = time.time(), time.process_time()
        
        efficiency = (end_process_time - start_process_time) / (end_all_time - start_all_time)
        
        if efficiency > RIGHT_EFFICIENCY:
            unblocking_queue.put("1")
        if efficiency < LEFT_EFFICIENCY and (end_process_time - start_process_time) != 0.0:
            tasks_queue.put(BLOCKING_TASK)
        
        results_queue.put(task)
    return
            

class ImagesWindow(QtWidgets.QMainWindow, images_shower.Ui_ImagesShower):
    def __init__(self, file_path):
        super().__init__()
        self.setupUi(self)
        self.setFixedSize(self.size())
        
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
        
        # Добавим в очередь разблокировки только 4 команды - разблокируем 4 потока
        for _ in range(START_PROCESSES_COUNT):
            unblocking_queue.put("1")
        
            
    def upload_new_images(self):
        files = QtWidgets.QFileDialog.getOpenFileNames(self,
                                     "Select one or more files",
                                     "/home",
                                     "Images (*.png *.xpm *.jpg)")

        if files:
            for file in files[0]:
                self.tasks_count += 1
                task_name = str(self.tasks_count) + ". " + file
                self.tasksListWidget.addItem(task_name)
                
                tasks_queue.put(task_name)
                
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
        
        # Проверяем, что задача выполнена, и только если она выполнена, открываем новое окно с картинкой
        if self.check_if_the_task_is_ready(task_id):
            self.images_dialog = ImagesWindow(file_path)
            self.images_dialog.show()        
        
        
    def save_all_results(self):
        if not os.path.isdir(TMP_DIRECTORY):
            return
        
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
    
    
import numpy as np
    
if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    shared_data_manager = Manager()
    namespace = shared_data_manager.Namespace()
    namespace.currently_taking_memory = 0
    namespace.currently_working_processes = 0
    
    with Pool(PROCESSES_COUNT, worker_fun, (tasks_queue, results_queue, unblocking_queue, namespace, atomic_operation)) as workers_pool:
        run_app()
