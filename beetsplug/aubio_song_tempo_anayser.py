#!/usr/bin/env python

#  Copyright: Copyright (c) 2020., Adam Jakab
#
#  Author: Adam Jakab <adam at jakab dot pro>
#  Created: 2/15/20, 11:55 PM
#  License: See LICENSE.txt
#
import sys
from numpy import diff, median
from aubio import source, tempo


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


if len(sys.argv) == 2:
    file_name = sys.argv[1]
    bpm = _analyse_tempo(file_name)
    print(bpm)
