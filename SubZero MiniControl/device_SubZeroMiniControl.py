# name=SubZero MiniControl

"""
[[
	Surface:	SubZero MiniControl
	Developer:	Thomas Alrek
	Version:	0.2
]]
"""

import transport
import mixer

BTN_LOOP = 49
BTN_REWIND = 47
BTN_FORWARD = 48
BTN_STOP = 46
BTN_PLAY = 45
BTN_RECORD = 44

MASTER_VOLUME = 11
MASTER_PAN = 22
MASTER_MUTE = 31

bank = 0

def mapMidiVal(val):
   return val/127

def translate(val, inMin, inMax, outMin, outMax):
    inSpan = inMax - inMin
    outSpan = outMax - outMin
    valScaled = float(val - inMin) / float(inSpan)
    return outMin + (valScaled * outSpan)

def clamp(val):
    return translate(val, 0, 1, 0, 0.8)

def OnSysEx(event):
    global bank
    bank = event.sysex[9]
    event.handled = True

def OnControlChange(event):
    if event.controlNum == MASTER_VOLUME:
        mixer.setTrackVolume(0, clamp(mapMidiVal(event.controlVal)))
        event.handled = True

    if event.controlNum == MASTER_PAN:
        mixer.setTrackPan(0, translate(mapMidiVal(event.controlVal), 0, 1, -1, 1))

    if event.controlNum == MASTER_MUTE:
        if event.controlVal == 127:
            mixer.muteTrack(0)

    for fader in range(3, 11):
        if event.controlNum == fader:
            track = (fader - 2) + (8 * bank)
            mixer.setTrackVolume(track, clamp(mapMidiVal(event.controlVal)))
            event.handled = True

    for pan in range(14, 22):
        if event.controlNum == pan:
            track = (pan - 13) + (8 * bank)
            mixer.setTrackPan(pan - 13, translate(mapMidiVal(event.controlVal), 0, 1, -1, 1))
            event.handled = True

    for muteBtn in range(23, 31):
        if event.controlNum == muteBtn:
            if event.controlVal == 127:
                track = (muteBtn - 22) + (8 * bank)
                mixer.muteTrack(muteBtn - 22)

    if event.controlVal == 127:
        if event.controlNum == BTN_STOP:
            transport.stop()
            event.handled = True
        elif event.controlNum == BTN_PLAY:
            transport.start()
            event.handled = True
        elif event.controlNum == BTN_LOOP:
            transport.setLoopMode()
            event.handled = True
        elif event.controlNum == BTN_RECORD:
            transport.record()
            event.handled = True

    if event.controlNum == BTN_REWIND:
        if event.controlVal == 0:
            transport.rewind(0)
        else:
            transport.rewind(2)
    elif event.controlNum == BTN_FORWARD:
        if event.controlVal == 0:
            transport.fastForward(0)
        else:
            transport.fastForward(2)

    event.handled = True
