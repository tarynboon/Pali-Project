# import transcriber
import os

from transcriber import Transcriber
from recorder import Recorder
from searcher import Searcher

def main():
    # set specifications for recording
    freq = 48000
    seconds = 5
    # set local path for audio file
    recording_file_name = '/Users/tboonpongmanee24/PycharmProjects/PaliProject/output.flac'

    # create recording via MacBook microphone
    r = Recorder(freq, seconds, recording_file_name)
    print("recording started, please speak for five seconds or less")
    r.record()
    print("recording ended")
    print()

    # upload local file into bucket
    destination_blob = 'output.flac'
    gcs_uri = r.upload_blob(destination_blob)

    # The name of the audio file to transcribe
    # format: gcs_uri = "gs://thb_test/New Recording 90.flac"
    file_name = "token.json"
    t = Transcriber(file_name)
    speech = t.transcribe_speech(gcs_uri)
    print("audio segment recorded: ")
    print(speech)
    print()

    # list all file names from within the prayerfile directory
    # all the prayer files
    mypath = "/Users/tboonpongmanee24/PycharmProjects/PaliProject/prayerfile/"
    os.chdir(mypath)
    prayer_file_names = []
    for f in os.listdir(mypath):
        if os.path.isfile(os.path.join(mypath, f)):
            prayer_file_names.append(f)

    # compare the segment from the transcriber to the prayers in the directory
    s = Searcher(prayer_file_names, mypath)
    match = s.search(speech)
    print("Possible chants: ")
    print(match)


main()