import rospy
from clover import srv
from std_srvs.srv import Trigger
import math
from datetime import datetime
# Подключаем модуль для работы с телеметрией
from telem import save_telemetry

rospy.init_node('flight_control')

# Инициализируем Ros и определяем сервисы
get_tlm = rospy.ServiceProxy('get_telemetry', srv.GetTelemetry)
nav_glo = rospy.ServiceProxy('navigate_global', srv.NavigateGlobal)
lnd = rospy.ServiceProxy('land', Trigger)
nav = rospy.ServiceProxy('navigate', srv.Navigate)

# Функция ожидания прибытия до целевой точки
def ar_wait(tolerance=0.2):
    while not rospy.is_shutdown():
        tlm = get_tlm(frame_id='navigate_target')
        if math.sqrt(tlm.x ** 2 + tlm.y ** 2 + tlm.z ** 2) < tolerance: #Проверка на отклонение целевех параметров  
            break
        rospy.sleep(0.2)

# Получение начальной телеметрии
pusk = get_tlm()

# Взлет на высоту
def vzlet():
    nav(x = 0, y = 0, z = 1, frame_id = 'body', auto_arm=True)
    my_home = (pusk.lat, pusk.lon)
    start_time = datetime.now()
    ar_wait()
    print(f"Полет начался")
    return my_home,start_time

# Посадка
def prizemlenie():
    lnd()
    print("Полет закончен")
    stop_time= datetime.now()
    return stop_time

# Полет по локальным координатам
def local_fly():
    pol_zadanie =[ #локальные координаты для демонстрации полета
    [2,0],
    [0,2],
    [-2,0],
    [0,-2]
    ]
    x = int(input ('Введите куда лететь x, если хотите увидеть демострацию полета 0'))
    y = int(input ('Введите куда лететь y, если хотите увидеть демострацию полета 0'))
    z = int (input ('Введите высоту, если не хотите менять введите 0'))
    speed = int (input ('Введите скорость, если не хотите менять введите 0'))
    if z==0 and speed==0: # Условие на установку дефолтных параметров
        z=0
        speed=1
    if x==0 and y ==0:#Демонстрационный полет
        for x, y in pol_zadanie:# Цикл для перебора точек из полетного задания
            print(f"Полет в точку X:{x}, Y:{y}, Высота {z}, Скорость {speed}")
            nav(x=x, y=y, z=z, frame_id='body', yaw=0, speed=speed)
            z=0 # чтобы не улетал все выше и выше
            ar_wait()
            print(f"Дрон прилетел в {x},{y}")
    else: # Ветвление для заданной пользователем координаты
        print(f"Полет в выбранную точку  X:{x}, Y:{y}, Высота {z}, Скорость {speed}")
        nav(x=x, y=y, z=z, frame_id='body', yaw=math.inf, speed=speed)
        ar_wait()
        print(f"Дрон прилетел в {x},{y}")
    
        

# Полет по глобальным координатам
def global_fly():
    lat = float(input("Введите широту: "))
    lon = float(input("Введите долготу: "))
    
    z = int (input ('Введите высоту, если не хотите менять введите 0'))
    speed = int (input ('Введите скорость, если не хотите менять введите 0'))
    if z==0 and speed==0: # Условие на установку дефолтных параметров
        z=1
        speed=1
    print(f"Полет в точку широта:{lat}, долгота:{lon}, высота:{z}, скорость {speed}")

    nav_glo(lat = lat, lon = lon, z = z, yaw=0, speed=speed)
    ar_wait()

# Возврат домой
def fly_pusk(my_home):
    print(f"Возвращаемся на старт в {my_home[0]}, {my_home[1]}")
    nav_glo(lat=my_home[0], lon=my_home[1], z=1, yaw=0, speed=1)
    ar_wait()

# Функция для сохранения телеметрии
def log_telemetry():
    telem = get_tlm()
    save_telemetry(telem)

# Главная функция для управления
def main():

    my_home = None

    while True:
        log_telemetry()
        print("\nВыберите действие")
        print("1. Взлет")
        print("2. Полет по локальным координатам")
        print("3. Полет по глобальным координатам")
        print("4. Вернуться домой")
        print("5. Посадка")
        print("6. Текущая телеметрия")
        print("0. Выход")

        vybor = input("Введите номер действия: ")

        if vybor == '1':
            my_home, start_time = vzlet()
        elif vybor  == '2':
            local_fly()
        elif vybor == '3':
            global_fly()
        elif vybor == '4':
            fly_pusk(my_home)
        elif vybor == '5':
            stop_time=prizemlenie()
            print ('Время полета', stop_time-start_time)
        elif vybor == '6':
            print(get_tlm())
        elif vybor == '0':
            print("Выход")
            stop_time=prizemlenie()
            print ('Время полета', stop_time-start_time)
            break
        else:
            print("Неверный ввод. Такой команды нет")

main()