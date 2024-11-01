import subprocess
import os


class Searcher:
    def __init__(self, prayer_file_names, mypath):
        self.prayer_file_names = prayer_file_names
        self.mypath = mypath
        self.file_name_and_prayers = {}

        for name in self.prayer_file_names:
            with open(name, encoding = "utf8", errors = 'ignore') as file:
                # read contents of files into dictionary with
                # name of each file as the key, and the contents as the value
                self.file_name_and_prayers[name] = file.read()

    def search(self, thai_text):
        return self.search_for_thai_prayers(thai_text, self.file_name_and_prayers)

    def search_for_thai_prayers(self, thai_text, prayers):
        # a new list to return the full list of matched prayers
        new_list = []

        for prayer in prayers.values():
            if self.is_in_prayer(thai_text, prayer):
                new_list.append(prayer)
                # get file name for each prayer matched, access through dictionary
                file_name = os.path.join(self.mypath, list(prayers.keys())[list(prayers.values()).index(prayer)])
                # open file on computer
                subprocess.call(['open', file_name])
        return new_list

    #helper function that detects if the thai substring is in the full text
    def is_in_prayer(self, thai_text, prayer):
        return thai_text in prayer

