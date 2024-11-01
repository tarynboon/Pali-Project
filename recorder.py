# import required libraries
import sounddevice as sd
import soundfile
from google.cloud import storage


class Recorder:
    def __init__(self, frequency, seconds, file_name):
        self.frequency = frequency
        self.seconds = seconds
        self.file_name = file_name

    # creates recording using MacBook microphone
    def record(self):
        recording = sd.rec(int(self.seconds * self.frequency), samplerate=self.frequency, channels=1)
        sd.wait()
        soundfile.write(self.file_name, recording, self.frequency)
        return self.file_name

    def upload_blob(self, destination_blob_name):
        # uploads a file to the bucket

        # The ID of your GCS bucket
        bucket_name = "pali-project"
        # The path to your file to upload
        source_file_name = self.file_name

        # sets names of bucket and path to upload
        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(destination_blob_name)

        blob.upload_from_filename(source_file_name)

        # print statement makes sure file uploaded to bucket, not just locally
        # print(
        #    f"File {source_file_name} uploaded to {destination_blob_name}."
        # )

        return 'gs://' + bucket_name + '/' + destination_blob_name
