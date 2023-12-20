import csv
import matplotlib.pyplot as plt
import board
import time
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
import RPi.GPIO as GPIO

# Initialize the I2C interface
i2c = busio.I2C(board.SCL, board.SDA)

# Create an ADS1115 object
ads = ADS.ADS1115(i2c)
 
# Define the analog input channel
channel = AnalogIn(ads, ADS.P0)

#Counter for time steps 
count = 0

# Setup Board
#GPIO.setmode(GPIO.BOARD) #Uncomment to select BOARD numbering system, Won't work as it's already set to BCM numbering system
GPIO.setwarnings(False)

# Taster zu Pins zuordnen
taster1 = 23 #16 for BOARD numbering system
taster2 = 24 #18 for BOARD numbering system

# Relais zu Pins zuordnen
relais1 = 20 #38 for BOARD numbering system
relais2 = 21 #40 for BOARD numbering system

# Setup Taster
GPIO.setup(taster1, GPIO.IN)
GPIO.setup(taster2, GPIO.IN)

# Setup Relais
GPIO.setup(relais1, GPIO.OUT)
GPIO.setup(relais2, GPIO.OUT)

# Opening data.csv in writing mode
f = open('data.csv', 'w', encoding='UTF8', newline='')
writer = csv.writer(f)
# Loop to read the analog input and drive the axis
while channel.voltage < 2.0 and GPIO.input(taster1) == GPIO.HIGH:
    #print("Analog Value: ", channel.value, "Voltage: ", channel.voltage)
    GPIO.output(relais1, GPIO.HIGH)
    values = [count]
    values.append(channel.voltage)
    writer.writerow(values)
    count = count + 1
    time.sleep(0.2)

GPIO.output(relais1, GPIO.LOW)
time.sleep(0.1)

while channel.voltage > 0.1 and GPIO.input(taster2) == GPIO.HIGH:
    #print("Analog Value: ", channel.value, "Voltage: ", channel.voltage)
    GPIO.output(relais2, GPIO.HIGH)
    values = [count]
    values.append(channel.voltage)
    writer.writerow(values)
    count = count + 1
    time.sleep(0.2)

GPIO.output(relais2, GPIO.LOW)
f.close()









# Making plot #####################################################################
x = [] 
y = [] 
  
with open('data.csv','r') as csvfile: 
    lines = csv.reader(csvfile, delimiter=',') 
    for row in lines: 
        x.append(row[0]) 
        y.append(float(row[1])) 
  
plt.plot(x, y, color = 'g', linestyle = 'dashed', 
         marker = 'o',label = "Time-Force-Graph") 
  
plt.xticks(rotation = 25) 
plt.xlabel('Time in 0.2s steps') 
plt.ylabel('Force') 
plt.title('Force Test', fontsize = 20) 
plt.grid() 
plt.legend()
plt.show()
# Making plot END #################################################################
