import sys
import pyautogui
import time
from datetime import datetime

loopTimeInSeconds = 0
loopAmount = 0
loopCount = 0
_continue = False

# This allows you to end the application by moving the mouse to the corner of any screen.
# Mostly useful for initial development / debugging if you lock yourself out of your mouse
pyautogui.FAILSAFE = False

#########################################
# Configure Settings Here               #
#########################################
# Loop time set in seconds              #
loopTimeInSeconds = 60  #
# Set this to 0 for infinite looping    #
loopAmount = 0  #
#########################################

loopCount = 0
_continue = True
pixelMoveAmount = 1
defaultTimeout = 8


class bcolors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


def movePixel():

    # Python is dumb (sometimes)
    global loopTimeInSeconds
    global _continue
    global loopCount
    global loopAmount

    # Start loop count at > 0 to make infinite looping logic easier (its a hack but hey, the whole solution is :D)
    loopCount += 1

    printMetaData()
    moveMouse(pixelMoveAmount)
    time.sleep(loopTimeInSeconds)

    # Allow for user to select 0 for loop minutes for infinite looping
    if loopAmount > 0 and loopCount > 0 and loopCount >= loopAmount:
        # break loop and quit
        _continue = False


def printEmphasis(_stringToPrint):
    """This function takes the string you want to print as an argument to determin the length of emphasis required for your text."""
    returnString = ""

    # Limit character count for emphasis to 200
    if len(_stringToPrint) > 200:
        for someint in range(230):
            returnString += "="
    else:
        for character in _stringToPrint:
            returnString += "="

    return returnString


def printWithColor(stringToPrint, bcolor, numberOfNewLines, emphasis):
    """If you aren't lazy, this is where you'd add some documentation about this function def 8D"""

    global bcolors
    newLines = ""
    seperatorLine = ""

    # Pyhton doesn't support function overloading so we must handle some logical overloading (sort of) inside the function
    if numberOfNewLines > 0:
        for i in range(numberOfNewLines):
            newLines += "\n"
            if emphasis:
                PrintWithTime(f"{bcolor}" + newLines + printEmphasis(stringToPrint))
                PrintWithTime(f"{bcolor}" + stringToPrint)
                PrintWithTime(f"{bcolor}" + printEmphasis(stringToPrint))
                PrintWithTime(f"{bcolors.ENDC}")
            else:
                PrintWithTime(f"{bcolor}" + newLines + stringToPrint + bcolors.ENDC)
    else:
        PrintWithTime(f"{bcolor}" + newLines + stringToPrint + bcolors.ENDC)


def moveMouse(_pixelMoveAmount):

    # Move to
    x, y = pyautogui.position()
    PrintWithTime("Move To: X:" + str(x) + " Y:" + str(y))
    pyautogui.moveTo(x + _pixelMoveAmount, y + _pixelMoveAmount)

    # Move from
    x, y = pyautogui.position()
    PrintWithTime("Move From: X:" + str(x) + " Y:" + str(y))
    pyautogui.moveTo(x - _pixelMoveAmount, y - _pixelMoveAmount)


def PrintWithTime(string):
    print(str(datetime.now().strftime("%d/%m/%Y %H:%M:%S")) + "" + string)


def printMetaData():

    PrintWithTime("Total Time In Minutes: " + str((loopCount * loopTimeInSeconds) / 60))
    PrintWithTime("Loops Completed:" + str(loopCount))

    if loopAmount > 0:
        PrintWithTime("Planned loop time is: " + str(loopAmount * loopTimeInSeconds / 60) + " minutes.")


def failsafeCheck():
    global _continue
    if (loopTimeInSeconds / 3600) * loopCount > 10:
        printWithColor(
            "Failsafe timeout was reached before execution stopped. Haulting application for safe exit",
            bcolors.WARNING,
            2,
            True,
        )
        _continue = False


# Getters and setters must be used to access global variables at runtime


def getDefaultTimeout():
    global defaultTimeout
    return defaultTimeout


if loopAmount == 0:
    printWithColor(
        "Infinite loop selected. Looping will continue until the program is stopped or the default timeout occurs."
        + " The default timeout is currently set to: "
        + str(getDefaultTimeout())
        + " hours.",
        bcolors.OKBLUE,
        1,
        True,
    )

while _continue:

    failsafeCheck()
    movePixel()
    print("")

sys.exit()
