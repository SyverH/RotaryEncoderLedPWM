from RPi import GPIO
from time import sleep

switch = 10 #Switch pin
clk = 11    #CLK pin
dt = 12     #PWM0
ledpin = 33 #PWM 1

switch_state = False

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

GPIO.setup(switch, GPIO.IN, pull_up_down=GPIO.PUD_UP)   #Pullup på switch
GPIO.setup(clk, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)    #Pulldown på CLK
GPIO.setup(dt, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)     #Pulldown på dt
GPIO.setup(ledpin, GPIO.OUT)

RPI_PWM = GPIO.PWM(ledpin, 100)
RPI_PWM.start(0)                                       #Starter på 0% Dutycycle

counter = 50
clkLastState = GPIO.input(clk)

def Limit(number, min_number, max_number):
    if number < min_number:
        return min_number
    elif number > max_number:
        return max_number
    else:
        return number

try:
    while True:
        if GPIO.input(switch) == 0:
            sleep(1)
            print("Trykket")
            switch_state ^= 1            #Hvis encoderen trykkes inn, skru lysene av eller på.
            if switch_state == False:
                RPI_PWM.stop()
                print("Stopper")
            if switch_state == True:
                RPI_PWM.start(counter)
                print("starter")
        if switch_state == True:                    #Hvis state True, Juster lysene etter encoderen
            clkState = GPIO.input(clk)
            dtState = GPIO.input(dt)
            if clkState != clkLastState:
                if dtState != clkState:
                    counter += 1                    #Tell en opp
                else:
                    counter -= 1                    #Tell en ned
                counter = Limit(counter, 1, 100)   #Limit counteren mellom 1 og 1000 (Max og min frekvens)
                RPI_PWM.ChangeDutyCycle(counter)    #Sett Frekvensen til led lik counteren
                print(counter)
            clkLastState = clkState
        #else:
         #   RPI_PWM.stop()              #Sett LED frekvens til 0
        sleep(0.01)
finally:
    GPIO.cleanup()