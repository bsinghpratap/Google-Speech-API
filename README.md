# Google Speech API
---------------------------------------------

> A script to smoothly run the Google API to predict the speech from the audio files. I've found that the prediction by google API is really good if there is less noise (which definitely is a big problem in real-time scenarios). 
> Just a personal opinion, if the problem of noise reduction and background reduction can be handled properly with the higher achievable accuracy, probably google can give a highly accurate result with high level of predictive confidence [for english].

To start with the API there are some pre-requisites.
- Before starting you will need the python library of Google for credentials and interacting with Google's API
```shell
sudo pip install --upgrade google-api-python-client
```
- Just set the google credentials on the system. These are being used by Google's API.
- You will need the API credential key, which you can get by following the steps mentioned [here](https://cloud.google.com/speech/docs/getting-started)
```shell
export GOOGLE_APPLICATION_CREDENTIALS=/path/speech_key.json
```
- This API uses the .raw format for speech transcription. Have added one test file named as audio.raw in the project. In order to use some other .wav file just convert the audio file (.wav or mp3) to .raw format.
```shell
sox audio.wav --rate 16000 --bits 16 --encoding signed-integer --endian little --channels 1 audio.raw'
```
```python
import subprocess
command = 'sox audio.wav --rate 16000 --bits 16 --encoding signed-integer --endian little --channels 1 audio.raw'
flag_done = subprocess.call(command, shell=True)
```
- Now we are all set to predict the transcription from the audio
```python
# Just to predict for one speech
from predict_speech import predict_speech
pred_model = predict_speech()
#transcript = pred_model.get_prediction(file path)
transcript = pred_model.get_prediction('audio.raw')

# Just to predit for all speech samples in a folder
#transcripts = pred_model.get_predictions_all(folder path)
transcripts = pred_model.get_predictions_all('/path/all_speech/')

# To predict for a mp3/wav file, incase the audio is greater than 60 secs- it breaks it into smaller chunks and converts them into raw file format
transcripts = pred_model.get_prediction_mp3('/path/audio.mp3')
transcripts = pred_model.get_prediction_wav('/path/audio.wav')
```
Have also added [WER](https://en.wikipedia.org/wiki/Word_error_rate) implementation which I have picked up from zszyellow's [implementation](https://github.com/zszyellow/WER-in-python).

> Comment out the print statements if it is irritating for a number of texts.

```python 
import wer as wer
wer_model = wer()
wer_value = wer_model('Reference text', 'Hypothesized text')
```

- Made some changes, added pydub library to check if the audio is greater than 60 secs. If it is: the code breaks the audio into samples smaller than 60 secs. 
- Uses Google API to predict the text for all audio parts and then returns the coalesced text from all the audios.

## Library dependencies
- [pydub](https://github.com/jiaaro/pydub): To install
```shell
pip install pydub
```