import librosa
from os import listdir,scandir
from os.path import isfile, join
from scipy.fft import *
from audio import Audio
import numpy as np

audios_list = []

'''def freq(file, start_time, end_time):
    


    # Open the file and convert to mono
    sr, data = wavfile.read(file)
    if data.ndim > 1:
        data = data[:, 0]
    else:
        pass

    # Return a slice of the data from start_time to end_time
    dataToRead = data[int(start_time * sr / 1000) : int(end_time * sr / 1000) + 1]

    # Fourier Transform
    N = len(dataToRead)
    yf = rfft(dataToRead)
    xf = rfftfreq(N, 1 / sr)

    # Uncomment these to see the frequency spectrum as a plot
    # plt.plot(xf, np.abs(yf))
    # plt.show()

    # Get the most dominant frequency and return it
    idx = np.argmax(np.abs(yf))
    freq = xf[idx]
    return freq'''  

def get_audios():
    waves = []

    actors_dir = 'speech_data'
    for it in scandir(actors_dir):
        if it.is_dir():
            wavefiles = [f for f in listdir(it.path) if isfile(join(it.path, f))]
            for i in range(len(wavefiles)):
                wavefiles[i] = it.path +"/"+ wavefiles[i]
            waves += wavefiles

    for w in waves: 
        #https://s3.ca-central-1.amazonaws.com/assets.jmir.org/assets/preprints/preprint-46970-accepted.pdf
        y, sr = librosa.load(w)
        #calculating zero crossing rate
        zero_crossing_rate = librosa.feature.zero_crossing_rate(y, frame_length=256, hop_length=512, center=True)
        zero_crossing_rate = np.ndarray.flatten(zero_crossing_rate)
        #calculating energy
        energy = np.array([
            sum(abs(y[i:i+256]**2))
            for i in range(0, len(y), 512)
        ])
        energy = np.ndarray.flatten(energy)
        #calculating mfcc
        mfcc = librosa.feature.mfcc(y=y, sr=sr, S=None, n_mfcc=20, dct_type=2, norm='ortho', lifter=0)
        mfcc = np.ndarray.flatten(mfcc)
        audio = Audio(zero_crossing_rate, energy, mfcc)
        audios_list.append(audio)
        
    return audios_list