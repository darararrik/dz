import psutil
from datetime import datetime

class AdapterManagement:
    _stats_history = {}  # Для хранения истории измерений
    _is_measuring = False  # Флаг активного измерения
    _measure_start_time = None  # Время начала замера

    @staticmethod
    def start_measuring():
        AdapterManagement._is_measuring = True
        # Сбрасываем историю при начале нового измерения
        AdapterManagement._stats_history = {}
        AdapterManagement._measure_start_time = datetime.now()

    @staticmethod
    def stop_measuring():
        AdapterManagement._is_measuring = False
        AdapterManagement._measure_start_time = None

    @staticmethod
    def get_adapters():
        return psutil.net_if_addrs()

    @staticmethod
    def get_adapter_info_by_name(adapter_name):
        adapters = psutil.net_if_addrs()
        stats = psutil.net_if_stats()
        
        if adapter_name not in adapters:
            return None

        # Вычисляем время замера
        if AdapterManagement._is_measuring and AdapterManagement._measure_start_time:
            delta = datetime.now() - AdapterManagement._measure_start_time
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
            if AdapterManagement._is_measuring:
                if adapter_name not in AdapterManagement._stats_history:
                    AdapterManagement._stats_history[adapter_name] = {
                        'last_bytes_recv': counter.bytes_recv,
                        'last_bytes_sent': counter.bytes_sent,
                        'max_download': 0,
                        'max_upload': 0,
                        'total_download': 0,
                        'total_upload': 0,
                        'count': 0
                    }

                history = AdapterManagement._stats_history[adapter_name]
                
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


