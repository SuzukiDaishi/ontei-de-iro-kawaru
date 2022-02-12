import pyaudio as pa
import pyworld as pw
import numpy as np
import matplotlib.pyplot as plt

SAMPLE_RATE = 16_000
INPUT_BUFFER_SIZE = 1024 * 2

def app_run(stream_in) :
    try:
        while stream_in.is_active():
            sinput = stream_in.read(INPUT_BUFFER_SIZE, exception_on_overflow=False)
            signal = np.frombuffer(sinput, dtype='int16').astype(np.float)
            signal /= 32767.

            _f0, t = pw.dio(signal, SAMPLE_RATE)
            f0 = pw.stonemask(signal, _f0, t, SAMPLE_RATE)

            f0m = np.log2(f0.mean(), where=f0.mean()>0)
            f0m = np.max([f0m, 6]) - 6
            f0m = np.min([f0m, 3]) / 3

            print(f'log_2(f0) = {np.log2(f0.mean(), where=f0.mean()>0):.03f}  ' + ('#' * int(f0m*100) ))

            mat = np.ones((10, 10)) * (f0m * 255)

            plt.axis('off')
            plt.imshow(mat, vmin=0, vmax=255)
            plt.pause(0.0001)
            plt.draw()
            plt.cla()

    except KeyboardInterrupt:
        print('\nInterrupt.')
    finally: 
        stream_in.stop_stream()
        stream_in.close()
        audio.terminate()
        print('Stop streaming.')

if __name__ == '__main__':

    audio = pa.PyAudio()

    print('# # # # 入力設定 # # # #')
    for i in range(audio.get_device_count()):
        data = audio.get_device_info_by_index(i)
        print(f'( {data["index"]} ): {data["name"]}')
    input_device_index = int(input('input device >> '))

    stream_in = audio.open(format=pa.paInt16,
                           channels=1,
                           rate=SAMPLE_RATE,
                           frames_per_buffer=INPUT_BUFFER_SIZE,
                           input=True, input_device_index=input_device_index)
    app_run(stream_in)
