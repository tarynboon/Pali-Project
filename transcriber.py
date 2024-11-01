# Import the Speech-to-Text client library
import export as export
from google.cloud import speech
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

class Transcriber:
    SCOPES = ['https://www.googleapis.com/auth/cloud-platform']

    def __init__(self, file_name):
        # check if token.json file is already regenerated
        # need for authentication
        self.creds = None
        if os.path.exists(file_name):
            self.creds = Credentials.from_authorized_user_file(file_name, Transcriber.SCOPES)
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', Transcriber.SCOPES)
                self.creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open(file_name, 'w') as token:
                token.write(self.creds.to_json())

        # creates speech client
        self.client = speech.SpeechClient()

    def transcribe_speech(self, audio_file):
        audio = speech.RecognitionAudio(uri=audio_file)

        # sets file type, frequency, language, channel count
        config = speech.RecognitionConfig(
              encoding=speech.RecognitionConfig.AudioEncoding.FLAC,
              sample_rate_hertz=48000,
              language_code="th-TH",
              model="default",
              audio_channel_count=1,
              enable_word_time_offsets=True,
        )

        # Detects speech in the audio file
        operation = self.client.long_running_recognize(config=config, audio=audio)
        print()
        print("Waiting for operation to complete...")
        print()
        response = operation.result(timeout=90)

        # returns the transcribed speech
        return response.results[0].alternatives[0].transcript