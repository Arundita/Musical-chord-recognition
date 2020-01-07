import pyaudio
import struct
from matplotlib import pyplot as plt
import numpy as np
import time
import datetime


start_time = datetime.datetime.now()

plt.ion()           # Turn on interactive mode so plot gets updated

WIDTH     = 2         # bytes per sample
CHANNELS  = 1         # mono
RATE      = 44000     # Sampling rate (samples/second)
BLOCKSIZE = 4096      # length of block (samples)
DURATION  = 30        # Duration (seconds)
DELAY = 220

last = datetime.datetime.now()
frequencies = {427:"A4", 453:"A#4", 497:"B4", 508:"C5",
             538:"C#5", 570:"D5", 604:"D#5", 640:"E5", 
            678:"F5", 718:"F#5", 761:"G5", 823:"G#5", 
           855:"A5", 907: "A#5", 959: "B5", 1016:"C6"}

NumBlocks = int( DURATION * RATE / BLOCKSIZE )

    

print('BLOCKSIZE =', BLOCKSIZE)
print('NumBlocks =', NumBlocks)
print('Running for ', DURATION, 'seconds...')

DBscale = False
# DBscale = True

# Initialize plot window:
plt.figure(1)
if DBscale:
    plt.ylim(0, 150)
else:
    plt.ylim(0, 20*RATE)

# Frequency axis (Hz)
plt.xlim(0, 0.5*RATE)         # set x-axis limits
# plt.xlim(0, 2000)         # set x-axis limits
plt.xlabel('Frequency (Hz)')
f = RATE/BLOCKSIZE * np.arange(0, BLOCKSIZE)

line, = plt.plot([], [], color = 'blue')  # Create empty line
line.set_xdata(f)                         # x-data of plot (frequency)

# Open audio device:
p = pyaudio.PyAudio()
PA_FORMAT = p.get_format_from_width(WIDTH)

stream = p.open(
    format    = PA_FORMAT,
    channels  = CHANNELS,
    rate      = RATE,
    input     = True,
    output    = False)


for i in range(0, NumBlocks):
    input_bytes = stream.read(BLOCKSIZE, exception_on_overflow = False)                     # Read audio input stream
    input_tuple = struct.unpack('h' * BLOCKSIZE, input_bytes)  # Convert
    X = np.fft.fft(input_tuple)
    temp = np.abs(X)
    # ind = np.unravel_index(np.argmax(temp, axis=None), temp.shape)
    m = np.argmax(temp)
    f = (m/BLOCKSIZE)*RATE
    if(temp[m] > 2300000):
        if((f < RATE/2) and (datetime.datetime.now() > (last + datetime.timedelta(milliseconds=DELAY)))):
            value = 427
            last = datetime.datetime.now()
            if(f >= 427 and f < 1077):
                for i in frequencies:
                    if(i > f):
                        break
                    value = i
                t = datetime.datetime.now() - start_time
                print(frequencies[value] + " at " + str(t.seconds) +"."+ str(int(t.microseconds/1000)) +" sec")
            
    # Update y-data of plot
    if DBscale:
        line.set_ydata(20 * np.log10(np.abs(X)))
    else:
        line.set_ydata(np.abs(X))
    plt.pause(0.001)
    # plt.draw()

plt.close()

stream.stop_stream()
stream.close()
p.terminate()

print('* Finished')