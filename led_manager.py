# !/usr/bin/env python3
# ## ###############################################
#
# led_manager.py
# Controls leds in the GPIO
#
# Autor:
# Autores:
# Dominguez Durán Gerardo
# Méndez Cabrera Ana Belem
# Rodríguez Sánchez José Andrés
# License: MIT
#
# ## ###############################################

# Future imports (Python 2.7 compatibility)
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

# Import Raspberry Pi's GPIO control library
import RPi.GPIO as GPIO
# Imports sleep functon
from time import sleep
# Initializes virtual board (comment out for hardware deploy)
import virtualboard

# Set up Rpi.GPIO library to use physical pin numbers
GPIO.setmode(GPIO.BOARD)
# Set up pin no. 32 as output and default it to low


pins = [10, 12, 16, 18, 22, 24, 26, 32]
pinsRev = [32, 26, 24, 22, 18, 16, 12, 10]
# correspondiente al Display de 7 segmentos
pinsLeds = [36, 38, 40, 37]

for p in pins:
    GPIO.setup(p, GPIO.OUT, initial=GPIO.LOW)
for p in pinsLeds:
    GPIO.setup(p, GPIO.OUT, initial=GPIO.LOW)

# Funcion que apaga los leds al ser seleccionado otro


def powerOffLeds():
    for led in pins:
        GPIO.output(led, GPIO.LOW)  # Turn led off
    for led in pinsLeds:
        GPIO.output(led, GPIO.LOW)  # Turn led off


def bcd7(num):
    """Converts num to a BCD representation"""
    print("estoy en la función BCD")
    GPIO.output(36, GPIO.HIGH if (num & 0x00000001) > 0 else GPIO.LOW)
    GPIO.output(38, GPIO.HIGH if (num & 0x00000002) > 0 else GPIO.LOW)
    GPIO.output(40, GPIO.HIGH if (num & 0x00000004) > 0 else GPIO.LOW)
    GPIO.output(37, GPIO.HIGH if (num & 0x00000008) > 0 else GPIO.LOW)


""" Enciende el leds especificados en num, apagando los demás
	(To be developed by the student)
"""


def leds(num):
    powerOffLeds()
    GPIO.output(pins[num-1], GPIO.HIGH)  # Turn led on


""" Activa el modo marquesina
	type toma tres valores: left, right y pingpong
	(To be developed by the student)
"""


def marquee(type='pingpong'):
    switcher = {
        'left': _marquee_left,
        'right': _marquee_right,
        'pingpong': _marquee_pingpong
    }
    func = switcher.get(type, None)
    if func:
        func()


"""	Despliega en número proporcionado en el display de siete segmentos.
	(To be developed by the student)
"""


def bcd(num):
    powerOffLeds()
    GPIO.output(36, GPIO.HIGH if (num & 0x00000001) > 0 else GPIO.LOW)
    GPIO.output(38, GPIO.HIGH if (num & 0x00000002) > 0 else GPIO.LOW)
    GPIO.output(40, GPIO.HIGH if (num & 0x00000004) > 0 else GPIO.LOW)
    GPIO.output(37, GPIO.HIGH if (num & 0x00000008) > 0 else GPIO.LOW)


""" Activa el modo marquesina continua a la izquierda"""


def _marquee_left():
    powerOffLeds()
    for j in range(len(pinsRev)+1):
        if j != 0:
            GPIO.output(pinsRev[j-1], GPIO.LOW)
        else:
            pass

        if j < len(pins):
            GPIO.output(pinsRev[j], GPIO.HIGH)
            sleep(0.5)  # Wait 500ms
        else:
            j = -1

        j = j+1


""" Activa el modo marquesina continua a la derecha"""


def _marquee_right():
    powerOffLeds()
    for j in range(len(pins)+1):
        if j != 0:
            GPIO.output(pins[j-1], GPIO.LOW)
        else:
            pass

        if j < len(pins):
            GPIO.output(pins[j], GPIO.HIGH)
            sleep(0.5)  # Wait 500ms
        else:
            j = -1

        j = j+1


""" Activa el modo marquesina ping-pong"""


def _marquee_pingpong():
    powerOffLeds()
    for j in range(len(pins)):
        if j != 0:
            GPIO.output(pins[j-1], GPIO.LOW)
        else:
            pass

        if j < len(pins):
            GPIO.output(pins[j], GPIO.HIGH)
            sleep(0.25)
        else:
            j = -1

        j = j+1

    for j in range(len(pinsRev)+1):
        if j != 0:
            GPIO.output(pinsRev[j-1], GPIO.LOW)
        else:
            pass

        if j < len(pins):
            GPIO.output(pinsRev[j], GPIO.HIGH)
            sleep(0.25)
        else:
            j = -1

        j = j+1


def reset_control(data):
    powerOffLeds()


def cam_control(data):
    powerOffLeds()
    for cam in data:
        if cam[1] == "On":
            GPIO.output(pins[int(cam[0])-1], GPIO.HIGH)  # Turn led on
        if cam[1] == "Off":
            GPIO.output(pins[int(cam[0])-1], GPIO.LOW)  # Turn led on


def light_control(data, slide):
    # print(data)
    # print(slide)
    powerOffLeds()
    for light in data:
        if light[1] == "On":
            GPIO.output(pins[int(light[0])-1], GPIO.HIGH)  # Turn led on
        if light[1] == "Off":
            GPIO.output(pins[int(light[0])-1], GPIO.LOW)  # Turn led on


def bell_control(data):
    powerOffLeds()
    print("Estoy en bell_control")
    print(data)
    for bell in data:
        if bell[1] == "Opened":
            GPIO.output(pins[int(bell[0])-1], GPIO.HIGH)  # Turn led on
        if bell[1] == "Closed":
            GPIO.output(pins[int(bell[0])-1], GPIO.LOW)  # Turn led on


def door_control(data):
    powerOffLeds()
    #print("Estoy en el door_control")
    # print(data)
    for door in data:
        if door[1] == "Opened":
            _marquee_pingpong()
        if door[1] == "Closed":
            _marquee_pingpong()
