import csnd6
import Adafruit_BBIO.GPIO as GPIO
from time import sleep
from subprocess import call

INPUT_1 = "P8_7"; INPUT_2 = "P8_9"; INPUT_3 = "P8_11"; INPUT_4 = "P8_13"
INPUT_5 = "P8_15"; INPUT_6 = "P8_17"; INPUT_7 = "P8_19"; 

call(["./pinmode.js"])

GPIO.setup(INPUT_1, GPIO.IN)
GPIO.setup(INPUT_2, GPIO.IN)
GPIO.setup(INPUT_3, GPIO.IN)
GPIO.setup(INPUT_4, GPIO.IN)
GPIO.setup(INPUT_5, GPIO.IN)
GPIO.setup(INPUT_6, GPIO.IN)
GPIO.setup(INPUT_7, GPIO.IN)

GPIO.add_event_detect(INPUT_1, GPIO.FALLING)
GPIO.add_event_detect(INPUT_2, GPIO.FALLING)
GPIO.add_event_detect(INPUT_3, GPIO.FALLING)
GPIO.add_event_detect(INPUT_4, GPIO.FALLING)
GPIO.add_event_detect(INPUT_5, GPIO.FALLING)
GPIO.add_event_detect(INPUT_6, GPIO.FALLING)
GPIO.add_event_detect(INPUT_7, GPIO.FALLING)

def createChannel(csound, channelName):
    chn = csnd6.CsoundMYFLTArray(1) 
    csound.GetChannelPtr(chn.GetPtr(), channelName, 
        csnd6.CSOUND_CONTROL_CHANNEL | csnd6.CSOUND_INPUT_CHANNEL) 
    return chn

def updateChannel(csound, channelName, value):
	channel = createChannel(csound, channelName)
	channel.SetValue(0, value)

orc = """
sr=8000
ksmps=2
nchnls=1
0dbfs=1

maxalloc 1, 4
cpuprc 1, 20

instr 1
aa,ab prepiano p7, 3, 10, p4, 3, 0.002, 2, 2, 1, 5000, -0.01, p5, p6, 0, 0.1, 1, 2
outs aa*.2, ab*.2
endin

instr 2
kfreq init p5
kjet init p4			;vary air jet
iatt = 0.1
idetk = 0.1
kngain = 0.15
kvibf = 5.925
kvamp = 0.05
asig wgflute .8, kfreq, kjet, iatt, idetk, kngain, kvibf, kvamp, 1
     outs asig, asig
endin

instr 3
  kamp = 0.7
  kfreq = p4
  ktens = p5
  iatt = p6
  kvibf = p7
  ifn = 1

  ; Create an amplitude envelope for the vibrato.
  kvamp line 0, p3, 0.5

  a1 wgbrass kamp, kfreq, ktens, iatt, kvibf, kvamp, ifn
  out a1
endin
"""

freq = ['261.63', '293.66', '329.63', '349.23', '392', '440', '493.88', '523.25']

c = csnd6.Csound()    # create an instance of Csound
c.SetOption("-odac")  # Set option for Csound
c.SetOption("-m7")  # Set option for Csound
c.SetOption("-B 512")  # Set option for Csound
c.CompileOrc(orc)     # Compile Orchestra from String

c.Start()             # When compiling from strings, this call is necessary before doing any performing

sco = """
f1 0 8 2 1 0.6 10 100 0.001 ;; 1 rattle
f2 0 8 2 1 0.7 50 500 1000  ;; 1 rubber
"""

c.ReadScore(sco)     # Read in Score generated from notes 

perfThread = csnd6.CsoundPerformanceThread(c)
perfThread.Play()
#perfThread.InputMessage("f 1 0 1024 10 1")
while (True):
	if GPIO.event_detected(INPUT_1):
		perfThread.InputMessage("i1 0.0 0.5 1 0.9 200 " + freq[0])
	if GPIO.event_detected(INPUT_2):
		perfThread.InputMessage("i1 0.0 0.5 1 0.9 200 " + freq[1])
	if GPIO.event_detected(INPUT_3):
		perfThread.InputMessage("i1 0.0 0.5 1 0.9 200 " + freq[2])
	if GPIO.event_detected(INPUT_4):
		perfThread.InputMessage("i1 0.0 0.5 1 0.9 200 " + freq[3])
	if GPIO.event_detected(INPUT_5):
		perfThread.InputMessage("i1 0.0 0.5 1 0.9 200 " + freq[4])
        if GPIO.event_detected(INPUT_6):
		perfThread.InputMessage("i1 0.0 0.5 1 0.9 200 " + freq[5])
        if GPIO.event_detected(INPUT_7):
		perfThread.InputMessage("i1 0.0 0.5 1 0.9 200 " + freq[6])

