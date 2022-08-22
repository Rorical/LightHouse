#RIEC_hrir_subject_046.sofa

import sofa

import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
import numpy as np
import IPython.display as ipd
import pydub
from scipy.signal import fftconvolve

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


HRTF_path = "RIEC_hrir_subject_046.sofa"
HRTF = sofa.Database.open(HRTF_path)

HRTF.Metadata.dump()

# plot Source positions
source_positions = HRTF.Source.Position.get_values(system="cartesian")[10:11]
plot_coordinates(source_positions, 'Source positions')

# plot Data.IR at M=5 for E=0
measurement = 10
emitter = 0
legend = []

t = np.arange(0,HRTF.Dimensions.N)*HRTF.Data.SamplingRate.get_values(indices={"M":measurement})

fs, y = mp3read("test.wav", normalized = True)
y = y.transpose()

plt.figure(figsize=(15, 5))

outs = []
for receiver in np.arange(HRTF.Dimensions.R):
    val = HRTF.Data.IR.get_values(indices={"M":measurement, "R":receiver, "E":emitter})
    plt.plot(t, val)
    legend.append('Receiver {0}'.format(receiver))
    outs.append(fftconvolve(val, y))

out = np.stack(outs, axis=0)

plt.title('HRIR at M={0} for emitter {1}'.format(measurement, emitter))
plt.legend(legend)
plt.xlabel('$t$ in s')
plt.ylabel(r'$h(t)$')
plt.grid()

audio = pydub.AudioSegment(
    out.tobytes(), 
    frame_rate=fs,
    sample_width=out.dtype.itemsize, 
    channels=2
)

audio.export("result.mp3", format="mp3")

#HRTF.close()