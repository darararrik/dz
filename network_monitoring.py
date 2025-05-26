import psutil
from datetime import datetime
from PyQt6.QtCore import pyqtSignal, QObject

class NetworkMonitoring(QObject):
    data_updated = pyqtSignal(dict, float)  # Сигнал для обновления данных (info, elapsed_time)
    
    def __init__(self):
        super().__init__()
        self._stats_history = {}
        self._is_measuring = False
        self._measure_start_time = None 
        

    def _update_data(self):
        """Внутренний метод для обновления данных"""
        if self._is_measuring:
            elapsed_time = (datetime.now() - self._measure_start_time).total_seconds()
            # Получаем данные для всех адаптеров
            for adapter_name in self.get_adapters().keys():
                info = self.get_adapter_info_by_name(adapter_name)
                if info:
                    self.data_updated.emit(info, elapsed_time)

    def start_measuring(self):
        """Начать измерение скорости"""
        self._is_measuring = True
        self._stats_history = {}
        self._measure_start_time = datetime.now()

    def stop_measuring(self):
        """Остановить измерение скорости"""
        self._is_measuring = False
        self._measure_start_time = None

    def get_adapters(self):
        return psutil.net_if_addrs()

    def get_adapter_info_by_name(self, adapter_name):
        adapters = self.get_adapters()
        stats = psutil.net_if_stats()
        
        if adapter_name not in adapters:
            return None

        # Вычисляем время замера
        if self._is_measuring and self._measure_start_time:
            delta = datetime.now() - self._measure_start_time
            measurement_time = str(delta).split('.')[0]  # ЧЧ:ММ:СС
        else:
            measurement_time = '0'

        # Получаем базовую информацию об адаптере
        addrs = adapters[adapter_name]
        info = {
            'id': adapter_name,
            'description': adapter_name,
            'interface_type': 'Ethernet',
            'ip': '',
            'mac': '',
            'speed': '',
            'mtu': '',
            'status': '',
            'measurement_time': measurement_time,
            'current_download': 0,
            'max_download': 0,
            'avg_download': 0,
            'current_upload': 0,
            'max_upload': 0,
            'avg_upload': 0
        }

        # Заполняем IP и MAC адреса
        for addr in addrs:
            if addr.family.name == 'AF_INET':
                info['ip'] = addr.address
            elif addr.family.name == 'AF_LINK':
                info['mac'] = addr.address

        # Получаем статистику адаптера
        if adapter_name in stats:
            stat = stats[adapter_name]
            info['speed'] = stat.speed if stat.speed != 0 else ''
            info['mtu'] = stat.mtu
            info['status'] = 'Активен' if stat.isup else 'Не активен'

        # Получаем статистику трафика
        io_counters = psutil.net_io_counters(pernic=True)
        if adapter_name in io_counters:
            counter = io_counters[adapter_name]
            
            # Инициализируем историю для адаптера, если идет измерение
            if self._is_measuring:
                if adapter_name not in self._stats_history:
                    self._stats_history[adapter_name] = {
                        'last_bytes_recv': counter.bytes_recv,
                        'last_bytes_sent': counter.bytes_sent,
                        'max_download': 0,
                        'max_upload': 0,
                        'total_download': 0,
                        'total_upload': 0,
                        'count': 0
                    }

                history = self._stats_history[adapter_name]
                
                # Рассчитываем текущую скорость
                bytes_recv = counter.bytes_recv - history['last_bytes_recv']
                bytes_sent = counter.bytes_sent - history['last_bytes_sent']
                
                # Конвертируем в Мбит/с
                current_download = round((bytes_recv * 8) / 1_000_000, 2)
                current_upload = round((bytes_sent * 8) / 1_000_000, 2)

                # Обновляем максимальные значения только при активном измерении
                history['max_download'] = max(history['max_download'], current_download)
                history['max_upload'] = max(history['max_upload'], current_upload)
                
                # Обновляем средние значения
                history['total_download'] += current_download
                history['total_upload'] += current_upload
                history['count'] += 1

                # Заполняем информацию о скорости
                info['current_download'] = current_download
                info['current_upload'] = current_upload
                info['max_download'] = history['max_download']
                info['max_upload'] = history['max_upload']
                info['avg_download'] = round(history['total_download'] / history['count'], 2)
                info['avg_upload'] = round(history['total_upload'] / history['count'], 2)

                # Сохраняем текущие значения для следующего измерения
                history['last_bytes_recv'] = counter.bytes_recv
                history['last_bytes_sent'] = counter.bytes_sent
            else:
                # Если измерение не активно, все значения будут нулевыми
                info['current_download'] = 0
                info['current_upload'] = 0
                info['max_download'] = 0
                info['max_upload'] = 0
                info['avg_download'] = 0
                info['avg_upload'] = 0

        return info


