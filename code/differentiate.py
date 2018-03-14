import matplotlib
matplotlib.use('Agg')
import numpy as np
import librosa
import librosa.display
import matplotlib.pyplot as plt
import sys

TEMP_FOLDER = 'static/tmp/'
EXTENSION_IMAGES ='png'

arg_real_file = 'benefit.m4a'
arg_user_input_file = 'benefit.flac'

class DTW(object):

    """docstring for DTW"""
    def __init__(self):
        super(DTW, self).__init__()

    """Differntiate 2 flac(audio) files"""
    def differntiateFile(self, real_file=arg_real_file, user_input_file=arg_user_input_file, input_file_format="flac"):
        y, sr = librosa.load(TEMP_FOLDER + real_file)
        sound_1 = librosa.feature.mfcc(y=y, sr=sr)

        # print('REAL sirial no: :',sr)
        # print('Shape original :',y.shape)

        y, sr = librosa.load(TEMP_FOLDER + user_input_file)
        sound_2 = librosa.feature.mfcc(y=y, sr=sr)

        # print('INPUT sirial no: :',sr)
        # print('Shape input:',y.shape)

        fig_name = user_input_file.split(".")[0]
        return self.plotAndSave(sound_1, sound_2, fig_name, EXTENSION_IMAGES)

    """Plot the difference between two sounds and save image showing comparison, return True if succssedful"""
    def plotAndSave(self, Y,Z,fig_name="compare", extension="png"):
        status = False
        try:
            D, wp = librosa.dtw(Y, Z, subseq=True)
            [N,M] = D.shape
            print(D[N-1,M-1])
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


files= ['benefit','estimate','factor','specific','theory']
# files= ['benefit']

if __name__ == '__main__':
    dtw = DTW()
    if len(sys.argv)==3:
        arg_real_file = sys.argv[1]
        arg_user_input_file = sys.argv[2]
    
    for audio_file in files:
        print('File name :',audio_file)
        dtw.differntiateFile(audio_file+'.flac', audio_file+'.m4a')
    
    # print('benefit.m4a','estimate.m4a')
    # dtw.differntiateFile('benefit.m4a','estimate.m4a')
    # print('estimate.m4a','factor.m4a')
    # dtw.differntiateFile('estimate.m4a','factor.m4a')
    # print('factor.m4a','specific.m4a')
    # dtw.differntiateFile('factor.m4a','specific.m4a')
    # print('specific.m4a','theory.m4a')
    # dtw.differntiateFile('specific.m4a','theory.m4a')
    # print('theory.m4a','benefit.m4a')
    # dtw.differntiateFile('theory.m4a','benefit.m4a')

