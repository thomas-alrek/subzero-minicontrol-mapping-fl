# name=SubZero MiniControl

"""
[[
	Surface:	SubZero MiniControl
	Developer:	Thomas Alrek
	Version:	0.1
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

def mapMidiVal(val):
   return val/127

def translate(val, inMin, inMax, outMin, outMax):
    # Figure out how 'wide' each range is
    inSpan = inMax - inMin
    outSpan = outMax - outMin

    # Convert the left range into a 0-1 range (float)
    valScaled = float(val - inMin) / float(inSpan)

    # Convert the 0-1 range into a value in the right range.
    return outMin + (valScaled * outSpan)

def clamp(val):
    return translate(val, 0, 1, 0, 0.8)

def OnControlChange(event):
    if event.controlNum == 11:
        mixer.setTrackVolume(0, clamp(mapMidiVal(event.controlVal)))
        event.handled = True

    if event.controlNum == 22:
        mixer.setTrackPan(0, translate(mapMidiVal(event.controlVal), 0, 1, -1, 1))

    if event.controlNum == 31:
        if event.controlVal == 127:
            mixer.muteTrack(0)

    for fader in range(3, 11):
        if event.controlNum == fader:
            mixer.setTrackVolume(fader - 2, clamp(mapMidiVal(event.controlVal)))
            event.handled = True

    for pan in range(14, 22):
        if event.controlNum == pan:
            mixer.setTrackPan(pan - 13, translate(mapMidiVal(event.controlVal), 0, 1, -1, 1))
            event.handled = True

    for muteBtn in range(23, 31):
        if event.controlNum == muteBtn:
            if event.controlVal == 127:
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
