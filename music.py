import IPython.display as ipd
import librosa
import librosa.display as dis
import matplotlib.pyplot as plt
import pathlib
import os
import numpy as np
import csv

#audio_path = 'Bastille - Pompeii.mp3'
#x , sr = librosa.load(audio_path)
#print(type(x), type(sr))
#<class 'numpy.ndarray'> <class 'int'>
#print(x.shape, sr)
#(396688,) 22050

# audio = 'music/Data/genres_original/classical/classical.00000.wav'
#
# y, sr = librosa.load(audio, sr=44100)
# y_ps = librosa.effects.pitch_shift(y, sr, n_steps=6)  # n_steps控制音调变化尺度
# y_ts = librosa.effects.time_stretch(y, rate=1.2)  # rate控制时间维度的变换尺度
# plt.subplot(311)
# plt.plot(y)
# plt.title('Original waveform')
# plt.axis([0, 200000, -0.4, 0.4])
# plt.axis([88000, 94000, -0.4, 0.4])
# plt.subplot(312)
# plt.plot(y_ts)
# plt.title('Time Stretch transformed waveform')
# plt.axis([0, 200000, -0.4, 0.4])
# plt.subplot(313)
# plt.plot(y_ps)
# plt.title('Pitch Shift transformed waveform')
# plt.axis([0, 200000, -0.4, 0.4])
# plt.axis([88000, 94000, -0.4, 0.4])
# plt.tight_layout()
# plt.show()

"""
audio_path = 'music/Data/genres_original/classical/classical.00000.wav'
x, sr = librosa.load(audio_path, sr=44100)
print(type(x), type(sr))
print(x.shape, sr)

plt.figure(figsize=(14, 5))
dis.waveplot(x, sr=sr)
plt.plot(x)
plt.show()

plt.figure(figsize=(14, 5))
librosa.display.waveplot(x, sr=sr)
"""

cmap = plt.get_cmap('inferno')

plt.figure(figsize=(10, 10))
genres = 'blues classical country disco hiphop jazz metal pop reggae rock'.split()
for g in genres:
    pathlib.Path(f'img_data/{g}').mkdir(parents=True, exist_ok=True)
    for filename in os.listdir(f'./music/Data/genres_original/{g}'):
        songname = f'./music/Data/genres_original/{g}/{filename}'
        y, sr = librosa.load(songname, mono=True, duration=5)
        plt.specgram(y, NFFT=2048, Fs=2, Fc=0, noverlap=128, cmap=cmap, sides='default', mode='default', scale='dB')
        plt.axis('off')
        plt.savefig(f'img_data/{g}/{filename[:-3].replace(".", "")}.png')
        plt.clf()

header = 'filename chroma_stft rmse spectral_centroid spectral_bandwidth rolloff zero_crossing_rate'
for i in range(1, 21):
    header += f' mfcc{i}'
header += ' label'
header = header.split()


file = open('data.csv', 'w', newline='')
with file:
    writer = csv.writer(file)
    writer.writerow(header)
genres = 'blues classical country disco hiphop jazz metal pop reggae rock'.split()
for g in genres:
    for filename in os.listdir(f'./music/Data/genres_original/{g}'):
        songname = f'./music/Data/genres_original/{g}/{filename}'
        y, sr = librosa.load(songname, mono=True, duration=30)
        chroma_stft = librosa.feature.chroma_stft(y=y, sr=sr)
        spec_cent = librosa.feature.spectral_centroid(y=y, sr=sr)
        spec_bw = librosa.feature.spectral_bandwidth(y=y, sr=sr)
        rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr)
        zcr = librosa.feature.zero_crossing_rate(y)
        mfcc = librosa.feature.mfcc(y=y, sr=sr)
        to_append = f'{filename} {np.mean(chroma_stft)} {np.mean(spec_cent)} {np.mean(spec_bw)} {np.mean(rolloff)} {np.mean(zcr)}'
        for e in mfcc:
            to_append += f' {np.mean(e)}'
        to_append += f' {g}'
        file = open('data.csv', 'a', newline='')
        with file:
            writer = csv.writer(file)
            writer.writerow(to_append.split())