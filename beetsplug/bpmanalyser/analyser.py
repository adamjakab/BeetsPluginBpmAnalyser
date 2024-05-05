import json
import os
import sys
import tempfile
import hashlib
from pydub import AudioSegment
from aubio import source, tempo
from numpy import diff, median

# Constants
__FRAME_RATE__ = 44100


#
# Run the analysis of the file
#
def do_the_analysis(item_path):
    error = False
    message = "OK"
    
    try:
        wav_path = convert_audio_to_wav(item_path)
        bpm = analyse_tempo(wav_path)
        os.remove(wav_path)
    except Exception as e:
            error = True
            message = e
            bpm = 0
    
    print_result(error, message, bpm)


#
# Convert the audio file to .wav 
#
def convert_audio_to_wav(item_path):
    tempdir = tempfile.gettempdir()
    filename = hashlib.md5(item_path.encode('utf-8')).hexdigest()
    wav_path = "{dir}/{file}.wav".format(dir=tempdir, file=filename)
    
    sound = AudioSegment.from_file(item_path)
    if (sound.frame_rate != __FRAME_RATE__):
        sound = sound.set_frame_rate(__FRAME_RATE__)
    sound.export(wav_path, format="wav")
    return wav_path


#
# Do the song analisys
#
def analyse_tempo(item_path):
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


def print_result(error:bool, message:str, bpm:int=0):
    result = {
        "error": error,
        "message": message,
        "bpm": bpm
    }
    print(json.dumps(result))

    
if __name__ == '__main__':
    if len(sys.argv) != 2:
        print_result(True, "Usage: python analyser.py song_path")
        sys.exit(1)

    file_name = sys.argv[1]
    if not os.path.isfile(file_name):
        print_result(True, "Audio file not found")
        sys.exit(2)

    do_the_analysis(file_name)
