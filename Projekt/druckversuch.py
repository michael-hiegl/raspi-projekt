import csv
import matplotlib.pyplot as plt
import board
import time
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
import RPi.GPIO as GPIO

# Functions
def driveallowed():
    if GPIO.input(end_oben) == GPIO.HIGH and GPIO.input(end_unten) == GPIO.HIGH and GPIO.input(tuerschalter) == GPIO.LOW:
        return True
    else:
        return False

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
end_oben = 24 #18 for BOARD numbering system
end_unten = 23 #16 for BOARD numbering system
tuerschalter = 25 #22 for BOARD numbering system

# Relais zu Pins zuordnen
relais_up = 21 #40 for BOARD numbering system
relais_down = 20 #38 for BOARD numbering system

# Setup Taster
GPIO.setup(end_oben, GPIO.IN)
GPIO.setup(end_unten, GPIO.IN)
GPIO.setup(tuerschalter, GPIO.IN)

# Setup Relais
GPIO.setup(relais_up, GPIO.OUT)
GPIO.setup(relais_down, GPIO.OUT)

try:
    # Opening data.csv in writing mode
    f = open('data.csv', 'w', encoding='UTF8', newline='')
    writer = csv.writer(f)
    # Loop to read the analog input and drive the axis
    while channel.voltage > 0.35 and driveallowed():
        #print("Analog Value: ", channel.value, "Voltage: ", channel.voltage)
        GPIO.output(relais_down, GPIO.HIGH)
        values = [count]
        values.append(-1*((channel.voltage-1.5)/0.015))
        # values.append(channel.voltage)
        writer.writerow(values)
        count = count + 1
        time.sleep(0.2)

    GPIO.output(relais_down, GPIO.LOW)
    time.sleep(0.5)

    while channel.voltage < 1.2 and driveallowed():
        #print("Analog Value.: ", channel.value, "Voltage: ", channel.voltage)
        GPIO.output(relais_up, GPIO.HIGH)
        values = [count]
        values.append(-1*((channel.voltage-1.5)/0.015))
        # values.append(channel.voltage)
        writer.writerow(values)
        count = count + 1
        time.sleep(0.2)

    GPIO.output(relais_up, GPIO.LOW)
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
    plt.xlabel('Way in 0,129mm steps') 
    plt.ylabel('Force in N') 
    plt.title('Force Test', fontsize = 20) 
    plt.grid() 
    plt.legend()
    plt.show()
    # Making plot END #################################################################

except:
    GPIO.output(relais_up, GPIO.LOW)
    GPIO.output(relais_down, GPIO.LOW)