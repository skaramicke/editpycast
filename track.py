import os
import librosa
import logging
import numpy as np

from pydub import AudioSegment

from tools import *


class Track:
    
    balance = 0.0
    audio = np.array([])
    stereo = np.array([], [])
    
    def __init__(self, filename: str, config, logger: logging.Logger = None):
        self.config = config
        self.logger = logger
        self.filename = filename
        self.audio, self.sr = librosa.load(self.filename, sr=44100)
        self.make_stereo()
        self.logger.info('Loaded track: {}'.format(self.filename))
    
    def prepare(self, position: int = 0, group_size: int = 1):
        self.normalize()
        self.set_balance_in_group(position, group_size)
    
    def make_stereo(self, balance: float = 0.0):
        if balance == 0.0:
            self.stereo = np.tile(self.audio, (2, 1))
            return
        
        self.logger.info('Track: {}. Starting creating stereo track with balance {}'.format(self.filename, self.balance))
        
        left_channel_multiplier = 1-balance
        right_channel_multiplier = 1-(-balance)
        
        self.stereo = np.array([
            self.audio * left_channel_multiplier,
            self.audio * right_channel_multiplier
        ])
    
    def set_balance_in_group(self, position: int, group_size: int):
        spread = 0.1
        if 'spread' in self.config:
            spread = self.config['spread']
        self.make_stereo(map_range(float(position), (0.0, float(group_size-1)), (-spread, spread)))
    
    def normalize(self):
        self.logger.info('Track: {}. Starting normalization'.format(self.filename, self.balance))
        self.audio = librosa.util.normalize(self.audio)
    
    def normalize_stereo(self):
        self.logger.info('Track: {}. Starting normalization'.format(self.filename, self.balance))
        channels, length = self.stereo.shape
        for i in range(channels):
            self.stereo[i] = librosa.util.normalize(self.stereo[i])
        self.logger.info('Track: {}. Normalization complete'.format(self.filename, self.balance))
    
    def get_length(self):
        return self.audio.shape[0]
    
    def set_length(self, new_length):
        length = self.audio.size
        diff = int(new_length - length)
        left = int(diff/2)
        right = int(diff/2)

        if diff % 2 != 0:
            right += 1
        
        self.audio = np.pad(self.audio, (left, right), 'constant')
        self.stereo = np.array([
            np.pad(self.stereo[0], (left, right), 'constant'),
            np.pad(self.stereo[1], (left, right), 'constant'),
        ])
    
    def add(self, track: 'Track'):
        self.stereo = np.add(self.stereo, track.stereo)
    
    def prepend(self, track: 'Track'):
        self.audio = np.concatenate([track.audio, self.audio])
        self.stereo = np.array([
            np.concatenate([track.stereo[0], self.stereo[0]]),
            np.concatenate([track.stereo[1], self.stereo[1]])
        ])
        
    def append(self, track: 'Track'):
        self.audio = np.concatenate([self.audio, track.audio])
        self.stereo = np.array([
            np.concatenate([self.stereo[0], track.stereo[0]]),
            np.concatenate([self.stereo[1], track.stereo[1]])
        ])

    def trim(self, threshold: float = 0.02, width: int = 5):
        count = 0
        cut_start = 0
        for i in range(self.audio.size):
            value = abs(self.stereo[0][i]) + abs(self.stereo[1][i])
            if value > threshold:
                count += 1
            else:
                count = 0
                cut_start = i
            if count > width:
                break
        
        count = 0
        cut_end = self.audio.size
        for r in range(self.audio.size-1):
            i = self.audio.size-1 - r
            value = abs(self.stereo[0][i]) + abs(self.stereo[1][i])
            if value > threshold:
                count += 1
            else:
                count = 0
                cut_end = i
            if count > width:
                break
        
        self.stereo = np.array([
            self.stereo[0][cut_start:cut_end],
            self.stereo[1][cut_start:cut_end]
        ])
        self.audio = self.audio[cut_start:cut_end]

    def export(self, track_name, mp3: bool = True):
        wav_file = '{}.wav'.format(track_name)
        librosa.output.write_wav(wav_file, self.stereo, self.sr, True)
        if mp3:
            mp3_file = '{}.mp3'.format(track_name)
            track = AudioSegment.from_wav(wav_file)
            track.export(mp3_file, format='mp3')
            os.remove(wav_file)
    
    def __str__(self):
        return self.filename
