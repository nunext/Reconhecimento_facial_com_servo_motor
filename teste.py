from pyfirmata import Arduino,SERVO
from time import sleep

port = 'COM4'
pin = 10
board = Arduino(port)

board.digital[pin].mode = SERVO

def rotateServo(pin,angle):
    board.digital[pin].write(angle)
    sleep(0.015)

# while True:
#     for x in range(0,180):
#         rotateServo(pin,x)
#     for i in range(180,1,-1):
#         rotateServo(pin, i)

while True:
    x = input(" Digite 1 para mover 180 graus e 0 para retornar a 0 graus: ")
    if x =="1":
        for angle in range (0,90):
            rotateServo(pin,angle)
    elif x =="0":
        for angle in range (40,0, -1):
            rotateServo(pin,angle)