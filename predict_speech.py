import argparse
import base64
import json

from googleapiclient import discovery
import httplib2
from oauth2client.client import GoogleCredentials
from pydub import AudioSegment
from os import listdir
from os.path import isfile, join


class predict_speech():

    def __init__(self):
        self.DISCOVERY_URL = ('https://{api}.googleapis.com/$discovery/rest?'
                 'version={apiVersion}')
        print('Predict Macha!')

    def get_file_names(self, mypath):
        onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
        return onlyfiles

    def get_predictions_all(self, speech_folder):
        list_files = self.get_file_names(speech_folder)
        responses_all = []
        try:
            for i in range(0,len(list_files)):
                if('.raw' in list_files[i]):
                    responses_all.append([list_files[i],self.get_prediction(speech_folder+list_files[i])])
            return responses_all
        except Exception as e:
            print e.__doc__
            print e.message
            return responses_all

    def get_prediction(self, speech_file):
        with open(speech_file, 'rb') as speech:
            speech_content = base64.b64encode(speech.read())
        #sound = AudioSegment.from_mp3("test_speech.mp3")
        service = self.get_speech_service()
        #print(type(speech_content))
        service_request = service.speech().syncrecognize(
            body={
                'config': {
                    'encoding': 'LINEAR16',  # raw 16-bit signed LE samples
                    'sampleRate': 16000,  # 16 khz changed to 44100
                    'languageCode': 'en-US',  # a BCP-47 language tag
                },
                'audio': {
                    'content': speech_content.decode('UTF-8')
                    }
                })
        response = service_request.execute()
        #print(response)
        #print(json.dumps(response))
        return response

    def get_speech_service(self):
        credentials = GoogleCredentials.get_application_default().create_scoped(
            ['https://www.googleapis.com/auth/cloud-platform'])
        http = httplib2.Http()
        credentials.authorize(http)
        return discovery.build('speech', 'v1beta1', http=http, discoveryServiceUrl=self.DISCOVERY_URL)    