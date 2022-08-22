#RIEC_hrir_subject_046.sofa

import sofa

import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
import numpy as np
import IPython.display as ipd
import pydub
from scipy.signal import fftconvolve
import os

def mp3read(f, normalized=False):
    """MP3 to numpy array"""
    a = pydub.AudioSegment.from_mp3(f)
    y = np.array(a.get_array_of_samples())
    if a.channels == 2:
        y = y.reshape((-1, 2))
    if normalized:
        return a.frame_rate, np.float32(y) / 2**15
    else:
        return a.frame_rate, y

def plot_coordinates(coords, title):
    x0 = coords
    n0 = coords
    fig = plt.figure(figsize=(15, 15))
    ax = fig.add_subplot(111, projection='3d')
    q = ax.quiver(x0[:, 0], x0[:, 1], x0[:, 2], n0[:, 0],
                  n0[:, 1], n0[:, 2], length=0.1)
    plt.xlabel('x (m)')
    plt.ylabel('y (m)')
    plt.title(title)
    return q


HRTF_path = "RIEC_hrir_subject_057.sofa"
HRTF = sofa.Database.open(HRTF_path)

HRTF.Metadata.dump()



# plot Source positions
source_positions = HRTF.Source.Position.get_values(system="cartesian")[72:80]
plot_coordinates(source_positions, 'Source positions')

# plot Data.IR at M=5 for E=0

fs, y = mp3read("066889f9dca5e4be002cfa1109f59f6a.mp3", normalized = True)
y = y.transpose()

audios = []

sec = 10

for measurement in range(72, 144 + 72):
    tstart_s = sec
    tend_s = sec + 100
    sec += 100
    print(tstart_s*fs, tend_s*fs)
    y_clip = y[:, int(round(tstart_s*100)) :int(round(tend_s*100))]

    val0 = HRTF.Data.IR.get_values(indices={"M":measurement, "R":0, "E":0})
    val1 = HRTF.Data.IR.get_values(indices={"M":measurement, "R":1, "E":0})
    
    
    out = np.stack([fftconvolve(val0, y_clip[0,:]), fftconvolve(val1, y_clip[1,:])], axis=0)
    audios.append(out)

outs = np.hstack(audios)
audio = ipd.Audio(data=outs, rate=fs, autoplay=True)
    
with open('result.wav', 'wb') as f:
    f.write(audio.data)



#HRTF.close()