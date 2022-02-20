from engi1020.arduino import *
from time import *

def grab(grabDialPin, grabServoPin):
    '''
    Changes grabbing servo angle based on primary dial position
    
    Parameters
    ----------
    grabDialPin : Pin that dial to control grabbing servo is plugged into
    grabServoPin : Pin that grabbing servo is plugged into
    
    Returns
    -------
    None.
    '''
    dialOne=analog_read(grabDialPin)/341*60 #Converts dial position to something the servo can use
    servo_move(grabServoPin, dialOne) #Changes servo position based on dial

def pivot(pivotDialPin, pivotServoPin):
    '''
    Changes pivoting servo angle based on secondary dial position. 
    Prints position of pivoting arm as a percent and changes the backlight 
    color based on position as well. Screen will turn red at either end of 
    the pivot.
    
    Parameters
    ----------
    pivotDialPin : Pin that dial to control pivoting servo is plugged into
    pivotServoPin : Pin that pivoting servo is plugged into
    
    Returns
    -------
    None.
    '''
    dialTwo=analog_read(pivotDialPin)/341*60
    servo_move(pivotServoPin, dialTwo)
    lcd_clear()
    lcd_print(dialTwo/1.8)
    colorIndicator=analog_read(pivotDialPin)/1023
    lcd_hsv(colorIndicator,0.6,100)
    
def checkButtonOne(buttonPin):
    '''
    Checks the state of button one
    
    Parameters
    ----------
    buttonPin : Pin that button is plugged into.
    
    Returns
    -------
    bool; True if button pressed, False if not pressed.
    '''
    if digital_read(buttonPin)==1:
        return True
    else:
        return False

def warning(grabDialPin, ledPin):
    '''
    If the claw is closed (grabber dial is close to end), LED will turn on to 
    let the user know.

    Parameters
    ----------
    grabDialPin : Pin number that grabber dial is plugged into.
    ledPin : Pin number that LED is plugged into.

    Returns
    -------
    None.

    '''
    checkDial = analog_read(grabDialPin) 
    if checkDial > 950:
        digital_write(ledPin,1)
    else: 
        digital_write(ledPin,0)

def timeActive(startTime):
    '''
    Prints how long the claw program has been active.

    Parameters
    ----------
    startTime : Time when program started
    
    Returns
    -------
    None.
    '''
    timeNow=time()
    activeTime=timeNow-startTime
    print("Program was active for", activeTime, "seconds.")

def listAverage(positionList, sumList):
    '''
    This function will print the average claw position as percent.
    
    Parameters
    ----------
    positionList : List of claw position samples taken every loop of main
    code block.
    sumList : The sum of the samples taken every loop of main
    code block.

    Returns
    -------
    None.

    '''
    clawAverage = sumList/len(positionList) #Calculate average.
    print("Average claw position is", clawAverage, "percent.") #Print average.
    
    
#---Main Script---

print("Welcome to claw program.")
print('---') #Print some break lines so console is more organized

grabDialPin = int(input("What analog pin is the grabber dial plugged into? "))
grabServoPin = int(input("What digital pin is the grabber servo plugged into? "))
pivotDialPin = int(input("What analog pin is the pivot dial plugged into? "))
pivotServoPin = int(input("What digital pin is the pivot servo plugged into? "))
buttonPin = int(input("What digital pin is the button plugged into? "))
ledPin = int(input("What digital pin is the LED plugged into? "))
print('---')

lcd_hsv(0.5,0.5,100) #Initialize LCD Settings (Hue, Saturation, Brightness).
positionList = [] #Create list for claw position samples.
sumList=0 #Create variable for sum of claw position samples so average can be calculated later.
clawPosition = analog_read(grabDialPin)/10.23 #Convert grabber dial value to a percent value.

print("Claw program is now active.")
print('---')
startTime = time() #Record time of code start point for later use.

while True: #Open loop so claw positions and user info can be continually changed.
    #grab(grabDialPin, grabServoPin)
    pivot(pivotDialPin, pivotServoPin)
    warning(grabDialPin, ledPin)
    positionList.append(clawPosition) #Add percent claw position to list of samples.
    sumList += clawPosition #Add percent claw position to the sum variable
    if checkButtonOne(buttonPin) == True: #Loop will end when button is pressed, ending the program.
        break

listAverage(positionList, sumList) #Prints average claw position.
timeActive(startTime) #Prints amount of time that claw was active, in seconds.
print("Thank you for using claw program.")