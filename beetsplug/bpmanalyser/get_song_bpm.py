#  Copyright: Copyright (c) 2020., Adam Jakab
#
#  Author: Adam Jakab <adam at jakab dot pro>
#  Created: 2/16/20, 10:50 AM
#  License: See LICENSE.txt
#
# The aubio/ffmpeg can produce some really ugly output on stderr:
# [mp3float @ 0x...] Could not update timestamps for skipped samples.
# [mp3float @ 0x...] Could not update timestamps for discarded samples.

import os
import sys
import hashlib
import tempfile

from aubio import source, tempo
from numpy import diff, median
from pydub import AudioSegment

__FRAME_RATE__ = 44100
    
def _analyse_tempo(item_path):
    sample_rate, win_s, hop_s = __FRAME_RATE__, 1024, 512
    src = source(item_path, sample_rate, hop_s)
    # sample_rate = src.samplerate
    o = tempo("default", win_s, hop_s, __FRAME_RATE__)

    beats = []
    total_frames = 0
    while True:
        samples, read = src()
        is_beat = o(samples)
        if is_beat:
            this_beat = o.get_last_s()
            beats.append(this_beat)
        total_frames += read
        if read < hop_s:
            break

    bpms = 60.0 / diff(beats)

    return int(median(bpms))

def _convert_audio_to_wav(item_path):
    tempdir = tempfile.gettempdir()
    filename = hashlib.md5(item_path.encode('utf-8')).hexdigest()
    wav_path = "{dir}/{file}.wav".format(dir=tempdir, file=filename)
    
    sound = AudioSegment.from_file(item_path)
    if (sound.frame_rate != __FRAME_RATE__):
        sound = sound.set_frame_rate(__FRAME_RATE__)
    sound.export(wav_path, format="wav")
    return wav_path

def _convert_and_analyse(item_path):
    wav_path = _convert_audio_to_wav(item_path)
    bpm = _analyse_tempo(wav_path)
    os.remove(wav_path)
    return bpm


if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.stderr.write("Usage: python get_song_bpm.py song_path" + "\n")
        sys.exit(1)

    file_name = sys.argv[1]
    if not os.path.isfile(file_name):
        sys.stderr.write("Audio file not found" + "\n")
        sys.exit(1)

    bpm = _convert_and_analyse(file_name)
    print(bpm)
