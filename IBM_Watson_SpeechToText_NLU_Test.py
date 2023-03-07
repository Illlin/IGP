import json
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import *

from os.path import join, dirname
from ibm_watson import SpeechToTextV1

import os
from dotenv import load_dotenv

load_dotenv()

env_authenticator = os.getenv('env_authenticator')
env_NLU_URL = os.getenv('env_NLU_URL')
env_SpeechToText_URL = os.getenv('env_SpeechToText_URL')

#print(env_authenticator)
#print(env_NLU_URL)
#print(env_SpeechToText_URL)

authenticator = IAMAuthenticator(env_authenticator) #When using watson, do not edit this...
natural_language_understanding = NaturalLanguageUnderstandingV1(
    version='2022-04-07',
    authenticator=authenticator)

speech_to_text = SpeechToTextV1(
    authenticator=authenticator
)

natural_language_understanding.set_service_url(env_NLU_URL) #or this.
speech_to_text.set_service_url(env_SpeechToText_URL)

#The following supports .flac but we can edit this to support other audio types.
with open(join(dirname(__file__), './.', 'audio-file2.flac'), #The Audio file example has to be in the same location as this python file.
               'rb') as audio_file:
    speech_recognition_results = speech_to_text.recognize(
        audio=audio_file,
        model='en-GB_Multimedia',
        content_type='audio/flac',
    ).get_result()
#print(json.dumps(speech_recognition_results, indent=2))

#print(speech_recognition_results['results'][0]['alternatives'][0]['transcript']) #Gets the transcript from the results of the speech to text.

text_transcript = speech_recognition_results['results'][0]['alternatives'][0]['transcript']

text_transcript_words = text_transcript.split() #Splits the transcript into separate words..
#to act as the targets in the NLU below.

response = natural_language_understanding.analyze(
    text=text_transcript,
    features=Features(emotion=EmotionOptions(targets=text_transcript_words))).get_result()

print(json.dumps(response, indent=2))