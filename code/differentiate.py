import matplotlib
matplotlib.use('Agg')
import numpy as np
import librosa
import librosa.display
import matplotlib.pyplot as plt

TEMP_FOLDER = 'static/tmp/'

class DTW(object):

    """docstring for DTW"""
    def __init__(self):
        super(DTW, self).__init__()

    """Differntiate 2 flac(audio) files"""
    def differntiateFile(self, real_file='ability.flac', user_file='ability.flac'):
        y, sr = librosa.load(TEMP_FOLDER + real_file)
        sound_1 = librosa.feature.mfcc(y=y, sr=sr)

        y, sr = librosa.load(TEMP_FOLDER + user_file)
        sound_2 = librosa.feature.mfcc(y=y, sr=sr)

        fig_name = user_file.replace('.flac','')
        return self.plotAndSave(sound_1, sound_2, fig_name,'png')

    """Plot the difference between two sounds and save image showing comparison, return True if succssedful"""
    def plotAndSave(self, Y,Z,fig_name="compare", extension="png"):
        status = False
        try:
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
            plt.savefig(TEMP_FOLDER + fig_name + '.' + extension)
            status = True
        except Exception as e:
            print('Plotting failed.')
            status = False

        return status




if __name__ == '__main__':
    dtw = DTW()
    dtw.differntiateFile()

