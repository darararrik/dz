import psutil

class AdapterManagement:
    @staticmethod
    def get_adapters():
        return psutil.net_if_addrs()

    def get_adapter_stats():
        return psutil.net_if_stats()
    @staticmethod
    def get_adapters_info():
        adapters =psutil.net_if_addrs()
        stats = psutil.net_if_stats()
        info_list = []
        for adapter_name, addrs in adapters.items():
            info = {
                'id': adapter_name,
                'description': adapter_name,  # Можно заменить на более подробное описание, если есть
                'interface_type': 'Ethernet',  # Можно попытаться определить по имени или другим признакам
                'ip': '',
                'mac': '',
                'speed': '',
                'mtu': '',
                'status': ''
            }
            for addr in addrs:
                if addr.family.name == 'AF_LINK':
                    info['mac'] = addr.address
                elif addr.family.name == 'AF_INET':
                    info['ip'] = addr.address
            stat = stats.get(adapter_name)
            if stat:
                info['speed'] = stat.speed
                info['mtu'] = stat.mtu
                info['status'] = 'Up' if stat.isup else 'Down'
            info_list.append(info)
        return info_list
    
    @staticmethod
    def get_adapter_info_by_name(adapter_name):
        """Возвращает подробную информацию по имени адаптера"""
        adapters = psutil.net_if_addrs()
        stats = psutil.net_if_stats()
        addrs = adapters.get(adapter_name, [])
        stat = stats.get(adapter_name)
        
        info = {
            'Имя адаптера': adapter_name,
            'Описание': adapter_name,
            'Тип интерфейса': 'Ethernet',
            'IP адрес': 'Не указан',
            'MAC адрес': 'Не указан',
            'Скорость': 'Неизвестно',
            'MTU': 'Неизвестно',
            'Статус': 'Отключен'
        }
        
        # Заполняем IP и MAC адреса
        for addr in addrs:
            if addr.family.name == 'AF_LINK':
                info['MAC адрес'] = addr.address
            elif addr.family.name == 'AF_INET':
                info['IP адрес'] = addr.address
        
        # Заполняем статистику
        if stat:
            info['Скорость'] = f"{stat.speed} Мбит/с" if stat.speed else "Неизвестно"
            info['MTU'] = f"{stat.mtu} байт"
            info['Статус'] = 'Активен' if stat.isup else 'Отключен'
        
        return info
