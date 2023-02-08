import winsound
import sounddevice as sd
import time
from datetime import datetime
from multiprocessing import Process
import multiprocessing
import numpy as np
import matplotlib.pyplot as plt

def get_time_now():
    now = datetime.now()
    return str(now.strftime("%H:%M:%S") + ':' + str(now.microsecond))


def record(duration, return_dict):
    fs = 44100
    recording = sd.rec(duration * fs, samplerate=fs, channels=2, dtype='float64')
    print (f"Recording Audio for {duration} seconds at {get_time_now()}")
    sd.wait()
    print (f"Audio recording complete at {get_time_now()}")
    return_dict['recording'] = recording

def play_sounds(frequenties):
    print(f'starting the sound playing at {get_time_now()}')
    time.sleep(5)
    for frequency in frequenties:
        print(f"playing frequenty {frequency} at: {get_time_now()}")
        winsound.Beep(frequency, 1000)
        time.sleep(3)
    print(f'done playing frequencies at {get_time_now()}')

def run_test_experiment():
    manager = multiprocessing.Manager()
    return_dict = manager.dict()
    record_sound_async = Process(target=record, args=(40,return_dict))
    record_sound_async.start()
    play_sound_async = Process(target=play_sounds, args=([200,400,600,800,1000,1200,1400],))
    play_sound_async.start()
    play_sound_async.join()
    record_sound_async.join()
    recording = return_dict['recording']
    timestamps = np.linspace(0,40,40*44100)
    return recording, timestamps

def data_analysis():
    recording, timestamps = run_test_experiment()
    plt.plot(timestamps, recording)
    plt.show()

if __name__ == '__main__':
    data_analysis()