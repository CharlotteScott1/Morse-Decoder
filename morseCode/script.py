from scipy.io import wavfile
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import keyboard

translation = {
    ".-": "A",
    "-...":"B",
    "-.-.":"C",
    "-..": "D",
    ".": "E",
    "..-.": "F",
    "--.": "G",
    "....": "H",
    "..": "I",
    "-.-": "K",
    ".-..": "L",
    "--":"M",
    "-.": "N",
    "---": "O",
    ".--.":"P",
    "--.-":"Q",
    ".-.": "R",
    "...": "S",
    "-": "T",
    "..-":"U",
    "...-":"V",
    ".--":"W",
    "-..-":"X",
    "-.--":"Y",
    "--..": "Z",
}

def record():
    something = keyboard.record(until="Enter")

    print(list(map(lambda i: i.name, something)))
record()
def fromWav(file):

    sampleRate, audio = wavfile.read(file)


    # Clean audio
    audio = np.abs(audio - audio.max() / 2) - 0.5
    audio = audio / audio.max()
    audio = audio[::10]
    sampleRate /= 10

    # 0.032520325203252036

    # reduce audio to list of sequencial occurences
    count = 0
    condensed = []
    silence = True
    for i, s in enumerate(audio):
        if silence and s == 0.032520325203252036:
            count += 1
        elif not silence and s != 0.032520325203252036:
            count += 1

        elif (
            not silence
            and s == 0.032520325203252036
            and audio[i + 1] != 0.032520325203252036
        ):
            count += 1
        else:
            condensed += [count]
            silence = not silence
            count = 0

    print(condensed)
    return condensed

# Calculate lengths of each type of sound
condensed = fromWav("morseAudio.wav")
minOn = 99999
maxOn = 0
minOff = 99999
maxOff = 0
silence = False
for i in condensed[1:]:
    if silence:
        if i < minOff:
            minOff = i
        if i > maxOff:
            maxOff = i
    else:
        if i < minOn:
            minOn = i
        if i > maxOn:
            maxOn = i
    silence = not silence

print(minOn, minOff, maxOn, maxOff)


# Decode audio based on pre inputted lengths
morse = ""
silence = True
for i in condensed:
    if silence:

        if i > maxOff * 0.8:
            morse += "/"
        if i > (minOff + maxOff) / 4:
            morse += "/"
    else:
        if i < minOn * 1.2:
            morse += "."
        else:
            morse += "-"

    silence = not silence

print(morse)

# Morse to text

morse = morse.split("/")
text = ""
for i in morse:
    if len(i) == 0:
        text += " "
    else:
        text += translation[i]

print(text)


# Plot graph of audio
"""
audio = pd.Series(audio, name = "audio")
audio.index = 1000*audio.index/sampleRate
audio.index.name = "Time(ms)"


ax = audio.plot(linewidth =3, grid="on")

plt.show()
"""
