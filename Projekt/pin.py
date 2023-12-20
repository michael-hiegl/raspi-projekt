import time
import RPi.GPIO as GPIO

out = 16
inp = 22

GPIO.setmode(GPIO.BOARD)
GPIO.setup(inp, GPIO.IN)
GPIO.setup(out, GPIO.OUT)

while 1:
  GPIO.output(out, GPIO.LOW)

  if GPIO.input(inp) == GPIO.LOW:
    GPIO.output(out, GPIO.HIGH)
    time.sleep(0.1)
    GPIO.output(out, GPIO.LOW)
    time.sleep(0.1)