# Programa realizado como proyecto final para la materia de sistemas embebidos
# que simula un smarthome, cuenta con camara, timbre, foco, apertura de garage
# Autores
# Dominguez Duran Gerardo
# Méndez Cabrera Ana Belem
# Rodríguez Sánchez José Andrés

# Importamos las librerias
import socket
import RPi.GPIO as GPIO
import time
#from gpiozero import PWMLED
from time import localtime

# Sockets para servidor TCP
host = ""
port = 12345
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.bind((host, port))
sock.listen(5)
foco_on = 0
led1 = 0
# Hora1 en el que es entregada
hora_ent = "0"
# Minuto1 en el que es entregado
min_ent = "0"
# Hora2 en el que es entregada
hora_ent = "0"
# Min 2 en el que es entregada
min_ent = "0"

data = "0"

try:
    while True:
        counter = 0
        counter_1 = 0
        (conexion, dir) = sock.accept()
        datas = conexion.recv(1024)
        print(datas)
        if (len(datas) > 5):
            datas1 = datas.decode()
            print(datas1)
            separator = datas1.split(",")

        data = separator[0]

        hora_ent = separator[1]
        min_ent = separator[2]

        hora_ent = separator[3]
        min_ent = separator[4]
        if (datas == b'1'):  # Si la entrada 1 se activa y entra al sig if
            if (GPIO.input(5) == False):  # Si la salida esta en Bajo o LOW
                GPIO.output(5, GPIO.HIGH)  # Entonces la pone en alto
            if(foco_on == 0):
                print("Foco light on, 1")
                foco_on = 1
            else:
                # Si esta en alto o HIGH, lo pone en bajo
                GPIO.output(5, GPIO.LOW)
                print("Foco light off, 0")
                foco_on = 0
        time.sleep(1)
        counter = 0
        # si mandi due, lights on
        if(datas == b'2'):
            # selezionamo il pin 8 per PWM con frequenza di 500
            LED = GPIO.PWM(8, 500)
            # inizia con off (0)
            LED.start(0)
            # controlla il ciclo di lavoro
            if led1 < 101:
                # aumenta da 5 a 5
                LED.ChangeDutyCycle(led1)
                led1 += 5
                time.sleep(0.1)
                # intensidad
                print("Intensidad ," + str(led1))
                # per il off
                for led1 in range(100, -1, -5):
                    LED.ChangeDutyCycle(led1)
        # on quando il timbre e on touch
        if(datas == b'3'):
            # it's on per l'uscita da porta o per questionare chi é?
            GPIO.output(13, GPIO.HIGH)
            print("Timbre sound on, 1")
            time.sleep(2)
            print("Timbre sound off, 0")
        time.sleep(1)
        if data == "4":
            # Pregunto hora on
            Hora = hora_ent
            # Pregunto min on
            Minuto = min_ent
            # Pregunto hora off
            Hora2 = hora_ent
            # Pregunto min off
            Minuto2 = min_ent
            if int(Hora) <= 24 and int(Minuto) <= 60:
                # iff hour == minutes
                if localtime().tm_hour == int(Hora) and localtime().tm_min == int(Minuto):
                    # ligths on
                    GPIO.output(16, GPIO.HIGH)
                    print("Foco, 1")
                    print("Hora," + Hora)
                    print("Minuto," + Minuto)
                    break

            if (int(Hora2) <= 24 and int(Minuto2) <= 60):
                # iff hour == minutes
                if localtime().tm_hour == int(Hora2) and localtime().tm_min == int(Minuto2):
                    # lights on
                    GPIO.output(16, GPIO.LOW)
                    print("Foco, 0")
                    print("Hora," + Hora2)
                    print("Minuto," + Minuto2)
                    break
            else:
                print("Ingresa una hora(formato 24hrs) y minutos de 0-60")

        if(datas == b'5'):
            print("SS CAM1, " + str(counter))
            counter = counter + 1
            GPIO.output(7, GPIO.HIGH)
            time.sleep(1)
            GPIO.output(7, GPIO.LOW)
            time.sleep(10)

        if(datas == b'6'):
            print("SS CAM2, " + str(counter_1))
            counter_1 = counter_1 + 1
            GPIO.output(11, GPIO.HIGH)
            time.sleep(1)
            GPIO.output(11, GPIO.LOW)
            time.sleep(10)

        if(datas == b'7'):
            print("Garage,1")
            counter_1 = counter_1 + 1
            GPIO.output(11, GPIO.HIGH)
            time.sleep(1)
            GPIO.output(11, GPIO.LOW)
            time.sleep(10)
        time.sleep(1)

except KeyboardInterrupt:
    GPIO.cleanup()
    conexion.close()
    print("conexion cerrada")
