import RPi.GPIO as GPIO

# Taster zu Pins zuordnen
taster1 = 16
taster2 = 18

# Relais zu Pins zuordnen
relais1 = 38
relais2 = 40

# Setup Board
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

# Setup Taster
GPIO.setup(taster1, GPIO.IN)
GPIO.setup(taster2, GPIO.IN)

# Setup Relais
GPIO.setup(relais1, GPIO.OUT)
GPIO.setup(relais2, GPIO.OUT)

while True:

    #Relais1 mit Taster1 schalten
    if GPIO.input(taster1) == GPIO.LOW:
        GPIO.output(relais1, GPIO.HIGH)
    else:
        GPIO.output(relais1, GPIO.LOW)


    #Relais2 mit Taster2 schalten
    if GPIO.input(taster2) == GPIO.LOW:
        GPIO.output(relais2, GPIO.HIGH)
    else:
        GPIO.output(relais2, GPIO.LOW)