import socket
import json
import threading
import time
import platform
import subprocess
from PyQt6.QtCore import QObject, pyqtSignal
from PyQt6.QtWidgets import QTableWidgetItem
from ..core.network_monitor import NetworkMonitor

class NetworkClient(QObject):
    """Класс для взаимодействия клиента с сервером"""
    connected = pyqtSignal()
    disconnected = pyqtSignal()
    error = pyqtSignal(str)
    log_message = pyqtSignal(str)
    adapter_info_received = pyqtSignal(dict)
    speeds_received = pyqtSignal(dict)
    adapters_list_received = pyqtSignal(list)
    
    def __init__(self):
        super().__init__()
        self.socket = None
        self.is_connected = False
        self.receive_thread = None
        self.network_monitor = NetworkMonitor()
        self.current_monitored_adapter = None
        self.monitoring_thread = None
        self.is_monitoring = False
        self.pc_name = self.get_pc_name()
        
    def get_pc_name(self):
        """Получение имени компьютера"""
        try:
            return platform.node()
        except:
            return "Неизвестный ПК"
        
    def connect_to_server(self, ip, port):
        """Подключение к серверу
        
        Args:
            ip: IP-адрес сервера
            port: Порт сервера
            
        Returns:
            bool: True если подключение успешно, иначе False
        """
        try:
            self.log_message.emit(f"Подключение к серверу {ip}:{port}...")
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((ip, port))
            self.is_connected = True
            
            # Устанавливаем таймаут для сокета
            self.socket.settimeout(5.0)

            # Отправляем информацию о клиенте
            self._send_client_info()
            
            # Запускаем поток для приема данных
            self.receive_thread = threading.Thread(target=self._receive_data)
            self.receive_thread.daemon = True
            self.receive_thread.start()
            
            self.connected.emit()
            self.log_message.emit(f"Успешно подключено к серверу {ip}:{port}")
            return True
        except Exception as e:
            self.error.emit(f"Ошибка подключения: {str(e)}")
            self.log_message.emit(f"Ошибка подключения к {ip}:{port}: {str(e)}")
            self.is_connected = False
            return False
            
    def disconnect(self):
        """Отключение от сервера"""
        if not self.is_connected:
            return
            
        try:
            # Останавливаем мониторинг, если запущен
            if self.is_monitoring:
                self.stop_monitoring()
                
            # Закрываем сокет
            if self.socket:
                self.socket.close()
                
            self.is_connected = False
            self.disconnected.emit()
            self.log_message.emit("Отключено от сервера")
        except Exception as e:
            self.error.emit(f"Ошибка при отключении: {str(e)}")
            self.log_message.emit(f"Ошибка при отключении: {str(e)}")
            
    def _receive_data(self):
        """Поток для приема данных от сервера"""
        while self.is_connected:
            try:
                data = self.socket.recv(4096)
                if not data:
                    # Сервер отключился
                    self.is_connected = False
                    self.disconnected.emit()
                    self.log_message.emit("Сервер разорвал соединение")
                    break
                
                # Обрабатываем полученные данные
                self._process_server_request(data)
            except socket.timeout:
                continue
            except Exception as e:
                # Проверяем, не закрыт ли уже сокет
                if not self.is_connected:
                    break
                
                self.error.emit(f"Ошибка при получении данных: {str(e)}")
                self.log_message.emit(f"Ошибка получения данных от сервера: {str(e)}")
                self.is_connected = False
                self.disconnected.emit()
                break
        
    def _process_server_request(self, data):
        """Обработка запроса от сервера
        
        Args:
            data: Полученные данные
        """
        try:
            # Декодируем данные
            message = json.loads(data.decode('utf-8'))
            
            # Обрабатываем различные типы сообщений
            if 'type' in message:
                message_type = message['type']
                
                if message_type == 'get_adapters':
                    self._send_adapters_list()
                    
                elif message_type == 'get_adapter_info':
                    adapter_name = message.get('adapter')
                    if adapter_name:
                        self._send_adapter_info(adapter_name)
                    else:
                        self.error.emit("Получен запрос без имени адаптера")
                        self.log_message.emit("Ошибка: сервер прислал некорректный запрос информации об адаптере")
                        
                elif message_type == 'start_monitoring':
                    adapter_name = message.get('adapter')
                    if adapter_name:
                        self.log_message.emit(f"Получена команда: начать мониторинг адаптера {adapter_name}")
                        self.start_monitoring(adapter_name)
                    else:
                        self.error.emit("Получен запрос на мониторинг без имени адаптера")
                        self.log_message.emit("Ошибка: сервер прислал некорректную команду старта мониторинга")
                        
                elif message_type == 'stop_monitoring':
                    self.log_message.emit("Получена команда: остановить мониторинг")
                    self.stop_monitoring()
                    
                elif message_type == 'request_ping':
                    request_id = message.get('id')
                    target = message.get('target')
                    if request_id and target:
                        self.log_message.emit(f"Получена команда: выполнить ping {target} (ID: {request_id})")
                        # Запускаем пинг в отдельном потоке, чтобы не блокировать прием
                        ping_thread = threading.Thread(target=self._execute_remote_command,
                                                     args=(request_id, target, 'ping'))
                        ping_thread.daemon = True
                        ping_thread.start()
                    else:
                        self._send_error_response(request_id, "Некорректный запрос на пинг")
                elif message_type == 'request_traceroute':
                    request_id = message.get('id')
                    target = message.get('target')
                    if request_id and target:
                        self.log_message.emit(f"Получена команда: выполнить трассировку {target} (ID: {request_id})")
                        # Запускаем трассировку в отдельном потоке
                        trace_thread = threading.Thread(target=self._execute_remote_command,
                                                      args=(request_id, target, 'traceroute'))
                        trace_thread.daemon = True
                        trace_thread.start()
                    else:
                        self._send_error_response(request_id, "Некорректный запрос на трассировку")
                    
                elif message_type == 'error':
                    # Сообщение об ошибке от сервера
                    error_msg = message.get('message', 'Неизвестная ошибка сервера')
                    self.error.emit(f"Ошибка от сервера: {error_msg}")
                    self.log_message.emit(f"Сообщение от сервера: {error_msg}")
                    
                else:
                    pass
                
            else:
                pass
            
        except json.JSONDecodeError as e:
            self.error.emit(f"Получены некорректные данные от сервера: {str(e)}")
            self.log_message.emit(f"Ошибка декодирования данных от сервера: {str(e)}")
        except Exception as e:
            self.error.emit(f"Ошибка обработки данных от сервера: {str(e)}")
            self.log_message.emit(f"Критическая ошибка обработки данных от сервера: {str(e)}")
            
    def _send_message(self, message):
        """Отправка сообщения серверу
        
        Args:
            message: Сообщение для отправки
            
        Returns:
            bool: True если отправка успешна, иначе False
        """
        if not self.is_connected:
            return False
            
        try:
            data = json.dumps(message).encode('utf-8')
            self.socket.sendall(data)
            return True
        except Exception as e:
            return False
            
    def _send_adapters_list(self):
        """Отправка списка адаптеров серверу"""
        adapters = self.network_monitor.get_adapters()
        message = {
            'type': 'adapters_list',
            'adapters': adapters
        }
        self._send_message(message)
        self.adapters_list_received.emit(adapters)
        
    def _send_adapter_info(self, adapter_name):
        """Отправка информации об адаптере серверу
        
        Args:
            adapter_name: Имя адаптера
        """
        info = self.network_monitor.get_adapter_info(adapter_name)
        message = {
            'type': 'adapter_info',
            'adapter': adapter_name,
            'info': info
        }
        self._send_message(message)
        self.adapter_info_received.emit(info)
        
    def start_monitoring(self, adapter_name):
        """Запуск мониторинга скорости адаптера
        
        Args:
            adapter_name: Имя адаптера для мониторинга
        """
        if self.is_monitoring:
            self.stop_monitoring()
            
        try:
            self.is_monitoring = True
            self.current_monitored_adapter = adapter_name
            self.network_monitor.selected_adapter = adapter_name
            self.network_monitor.start_measurement(adapter_name)
            
            # Запускаем мониторинг
            self.monitoring_thread = threading.Thread(target=self._monitoring_loop)
            self.monitoring_thread.daemon = True
            self.monitoring_thread.start()
            
            self.log_message.emit(f"Запущен мониторинг адаптера {adapter_name}")
            response = {'type': 'monitoring_started', 'adapter': adapter_name}
            self._send_message(response)
        except Exception as e:
            self.error.emit(f"Ошибка при запуске мониторинга: {str(e)}")
            self.log_message.emit(f"Ошибка при запуске мониторинга: {str(e)}")
            self.is_monitoring = False
            
    def stop_monitoring(self):
        """Остановка мониторинга скорости"""
        if not self.is_monitoring:
            return
            
        self.is_monitoring = False
        self.current_monitored_adapter = None
        
        # Ждем завершения потока
        if self.monitoring_thread:
            try:
                self.monitoring_thread.join(timeout=1.0)
            except Exception as e:
                self.error.emit(f"Ошибка при остановке потока мониторинга: {str(e)}")
                
        self.monitoring_thread = None
        self.current_monitored_adapter = None
        
        self.log_message.emit("Мониторинг остановлен")
        
        response = {
            'type': 'monitoring_stopped',
            'adapter': self.current_monitored_adapter
        }
        self._send_message(response)
        
    def _monitoring_loop(self):
        """Цикл мониторинга и отправки данных серверу"""
        while self.is_monitoring and self.is_connected:
            try:
                # Получаем текущие скорости
                speeds = self.network_monitor.get_current_speeds()
                
                if speeds:
                    # Отправляем данные серверу
                    message = {
                        'type': 'speeds_data',
                        'adapter': self.current_monitored_adapter,
                        'data': speeds
                    }
                    self._send_message(message)
                    self.speeds_received.emit(speeds)
                    
            except Exception as e:
                self.error.emit(f"Ошибка мониторинга: {str(e)}")
                
            # Пауза между измерениями
            time.sleep(1)
            
    def get_adapters_list(self):
        """Получение списка адаптеров
        
        Returns:
            list: Список адаптеров
        """
        return self.network_monitor.get_adapters()
        
    def get_adapter_info(self, adapter_name):
        """Получение информации об адаптере
        
        Args:
            adapter_name: Имя адаптера
            
        Returns:
            dict: Информация об адаптере
        """
        return self.network_monitor.get_adapter_info(adapter_name)

    def _send_client_info(self):
        """Отправка информации о клиенте серверу"""
        message = {
            'type': 'client_info',
            'pc_name': self.pc_name
        }
        self._send_message(message)

    def _send_result_line(self, request_id, line, command_type):
        message = {
            'type': f'{command_type}_result', # ping_result или traceroute_result
            'id': request_id,
            'line': line
        }
        self._send_message(message)

    def _send_finished_signal(self, request_id, command_type):
        message = {
            'type': f'{command_type}_finished', # ping_finished или traceroute_finished
            'id': request_id
        }
        self._send_message(message)

    def _send_error_response(self, request_id, error_message, command_type):
        message = {
            'type': f'{command_type}_error', # ping_error или traceroute_error
            'id': request_id,
            'message': error_message
        }
        self._send_message(message)

    def _execute_remote_command(self, request_id, target, command_type):
        """Выполняет ping или traceroute и отправляет результаты серверу"""
        try:
            # Определяем команду в зависимости от ОС и типа запроса
            if platform.system().lower() == "windows":
                cmd = ['ping', target] if command_type == 'ping' else ['tracert', '-d', target] # -d для tracert, чтобы не разрешать имена
            else: # Linux/macOS
                cmd = ['ping', '-c', '4', target] if command_type == 'ping' else ['traceroute', target]

            # Запускаем процесс
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

            # Читаем вывод построчно (как байты) и отправляем серверу
            for line_bytes in iter(process.stdout.readline, b''): # Читаем байты, условие выхода b''
                if not line_bytes.strip(): continue # Пропускаем пустые строки
                # Декодируем строку используя CP866 (стандартная для рус. консоли)
                line_str = line_bytes.decode('cp866', errors='ignore')
                self._send_result_line(request_id, line_str.strip(), command_type)
                # Небольшая задержка, чтобы не перегружать сеть/сервер
                time.sleep(0.05)

            process.stdout.close()
            return_code = process.wait()

            if return_code == 0:
                self._send_finished_signal(request_id, command_type)
            else:
                self._send_error_response(request_id, f"Команда завершилась с кодом {return_code}", command_type)

        except FileNotFoundError:
             err_msg = f"Команда '{cmd[0]}' не найдена на клиенте."
             self.log_message.emit(f"Ошибка выполнения {command_type.capitalize()} ({request_id}): {err_msg}")
             self._send_error_response(request_id, err_msg, command_type)
        except Exception as e:
            err_msg = f"Ошибка выполнения команды на клиенте: {str(e)}"
            self.log_message.emit(f"Ошибка выполнения {command_type.capitalize()} ({request_id}): {err_msg}")
            self._send_error_response(request_id, err_msg, command_type) 