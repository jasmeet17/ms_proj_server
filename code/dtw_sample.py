import matplotlib
matplotlib.use('Agg')
import numpy as np
import librosa
import librosa.display
import matplotlib.pyplot as plt

FILE_FOLDER = 'static/tmp/'

# y, sr = librosa.load("eng.mp3")
# sound_1 = librosa.feature.mfcc(y=y, sr=sr)

# y, sr = librosa.load("rus.mp3")
# sound_2 = librosa.feature.mfcc(y=y, sr=sr)

# def plot(Y,Z,fig_name):
#     D, wp = librosa.dtw(Y, Z, subseq=True)
#     plt.figure(fig_name)
#     plt.subplot(2, 1, 1)
#     librosa.display.specshow(D, x_axis='frames', y_axis='frames')
#     plt.plot(wp[:, 1], wp[:, 0], label='Optimal path', color='y')
#     plt.legend()
#     plt.subplot(2, 1, 2)
#     plt.plot(D[-1, :] / wp.shape[0])
#     plt.xlim([0, Y.shape[1]])
#     plt.ylim([0, 2])
#     plt.title('Matching cost function')
#     plt.tight_layout()
#     plt.savefig(FILE_FOLDER + fig_name + '.png')

# plot(sound_1,sound_2, "differnet files sound 1 and 2")
#plot(sound_1,sound_1, "differnet files sound 1 and 1")


# noise = np.random.rand(sound_1.shape[0], 200)

# sound_1_with_noise = np.concatenate((noise, sound_1, noise), axis=1)
# plot(sound_1, sound_1_with_noise, "differnet files sound 1 and 1+noise")

# y, sr = librosa.load(librosa.util.example_audio_file(), offset=10, duration=15)
# X_1 = librosa.feature.mfcc(y=y, sr=sr)
# noise = np.random.rand(X_1.shape[0], 200)
# Y_1 = np.concatenate((noise, noise, X_1, noise), axis=1)

# plot(X_1,X_1, "chroma_mfcc")

class DTW(object):

    """docstring for DTW"""
    def __init__(self):
        super(DTW, self).__init__()

    def differntiateFile(self, file_1='eng.mp3', file_2='rus.mp3'):
        y, sr = librosa.load("eng.mp3")
        sound_1 = librosa.feature.mfcc(y=y, sr=sr)

        y, sr = librosa.load("rus.mp3")
        sound_2 = librosa.feature.mfcc(y=y, sr=sr)

        self.plotAndSave(sound_1, sound_2, 'comparison')

    def plotAndSave(self, Y,Z,fig_name):
        D, wp = librosa.dtw(Y, Z, subseq=True)
        plt.figure(fig_name)
        plt.subplot(2, 1, 1)
        librosa.display.specshow(D, x_axis='frames', y_axis='frames')
        plt.plot(wp[:, 1], wp[:, 0], label='Optimal path', color='y')
        plt.legend()
        plt.subplot(2, 1, 2)
        plt.plot(D[-1, :] / wp.shape[0])
        plt.xlim([0, Y.shape[1]])
        plt.ylim([0, 2])
        plt.title('Matching cost function')
        plt.tight_layout()
        plt.savefig(FILE_FOLDER + fig_name + '.png')

dtw = DTW()
dtw.differntiateFile()

