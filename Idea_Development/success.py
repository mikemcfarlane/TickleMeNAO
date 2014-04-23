
""" Explore some methods for showing success and failure.

"""
import sys
from naoqi import ALProxy

IP = "mistcalf.local"
PORT = 9559

WIN = True

try:
    aupProxy = ALProxy("ALAudioPlayer", IP, PORT)
except Exception, e:
    print "Could not creat proxy to ALAudioPlayer. Error: ", e
    sys.exit(1)
try:
    animatedSpeechProxy = ALProxy("ALAnimatedSpeech", IP, PORT)
except Exception, e:
    print "Could not create proxy to ALAnimatedSpeech. Error: ", e
try:
    motionProxy = ALProxy("ALMotion", IP, PORT)
except Exception, e:
    print "Could not create proxy to ALMotion. Error: ", e

# set the local configuration
configuration = {"bodyLanguageMode":"contextual"}

# Wake the robot up.
motionProxy.wakeUp()
    
    
def gameWinPraise():
    # animated speech with LEDs
    # say the text with the local configuration
    animatedSpeechProxy.say("You did that really well!", configuration)

def gameWinAnimation():
    # animated speech with LEDs
    animatedSpeechProxy.say("I am going to dance now!", configuration)
    # play sound with animation
    
    volume = 0.75
    pan = 0.0
    aupProxy.playFile("/home/nao/audio/mystic1.wav", volume, pan)
    aupProxy.playFile("/home/nao/audio/heavyMetal1.wav", volume, pan)
    aupProxy.playFile("/home/nao/audio/applause1.wav", volume, pan)

def gameLost():
    # animated speech with LEDs
    pass

def main():
    if WIN:
        gameWinPraise()
        gameWinAnimation()
    else:
        gameLost()
    
if __name__ == "__main__":
    main()