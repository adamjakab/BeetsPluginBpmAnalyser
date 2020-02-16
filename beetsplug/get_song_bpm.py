#!/usr/bin/env python

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

from aubio import source, tempo
from numpy import diff, median


def _analyse_tempo(item_path):
    sample_rate, win_s, hop_s = 44100, 1024, 512
    src = source(item_path, sample_rate, hop_s)
    sample_rate = src.samplerate
    o = tempo("default", win_s, hop_s, sample_rate)

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

    bpm = median(bpms)

    return int(bpm)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        raise RuntimeError("Usage: python get_song_bpm.py song_path")

    file_name = sys.argv[1]

    if not os.path.isfile(file_name):
        raise RuntimeError("Song not found.")

    bpm = _analyse_tempo(file_name)
    print(bpm)
