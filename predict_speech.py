import argparse
import base64
import json
import subprocess
import random

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
        service = self.get_speech_service()
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
        #print(json.dumps(response))
        return response

    def generate_temp_key():
    	return ''.join(random.choice('0123456789ABCDEF') for i in range(8))

    def get_prediction_mp3(self, speech_file):
    	list_chunks = get_audio_chunks(speech_file)
    	response = consolidate_resuls(list_chunks)
    	return response

    def consolidate_results(self, list_chunks):
    	final_response = ''
    	for chunk in list_chunks:
    		if(chunk!='<error>'):
	    		tmp_response = get_prediction(temp_addr)
	    		final_response = final_response+' '+tmp_response
    	return final_response

    def convert_raw(self, speech_file):
    	temp_addr = 'temp/temp-'+generate_temp_key()+'.raw'
    	command = 'sox '+speech_file+' --rate 16000 --bits 16 --encoding signed-integer --endian little --channels 1 '+temp_addr
    	flag_done = subprocess.call(command, shell=True)
    	if(flag_done!=0):
    		# This tag is just to find that the chunk or the audio cannot be converted to the raw file format
    		print(' <error in converting the chunk into raw file format> ')
    		return '<error>'
    	else:
    		return temp_addr

    def get_audio_chunks(self, speech_file):
    	limit_secs = 60
    	list_chunks = []
    	sound = AudioSegment.from_mp3(speech_file)
    	if((len(sound)/1000)>limit_secs):
    		while((len(sound)/1000)>limit_secs):
    			tmp_sound = sound[:(limit_secs*1000)]
    			sound = sound[(limit_secs*1000):]
    			tmp_mp3_addr = 'temp/temp-'+generate_temp_key()+'.wav'
    			tmp_sound.to_mp3(tmp_mp3_addr)
    			list_chunks.append(self.convert_raw(tmp_mp3_addr))
    		tmp_mp3_addr = 'temp/temp-'+generate_temp_key()+'.wav'
    		sound.to_mp3(tmp_mp3_addr)
    		list_chunks.append(self.convert_raw(tmp_mp3_addr))
	    else:
	    	list_chunks.append(self.convert_raw(speech_file))
	    return list_chunks

    def get_speech_service(self):
        credentials = GoogleCredentials.get_application_default().create_scoped(
            ['https://www.googleapis.com/auth/cloud-platform'])
        http = httplib2.Http()
        credentials.authorize(http)
        return discovery.build('speech', 'v1beta1', http=http, discoveryServiceUrl=self.DISCOVERY_URL)    