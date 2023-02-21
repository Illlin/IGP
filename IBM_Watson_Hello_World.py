import json
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import *

authenticator = IAMAuthenticator('CaVS7g-14_SpntBkVo-XsFLB2udYJBMRmE0t6zB5hXXv') #When using watson, do not edit this...
natural_language_understanding = NaturalLanguageUnderstandingV1(
    version='2022-04-07',
    authenticator=authenticator)

natural_language_understanding.set_service_url('https://api.eu-gb.natural-language-understanding.watson.cloud.ibm.com/instances/23c1b14d-5c3c-4820-becc-1489050bdf78') #or this.

text_hello_world = 'Hello World!'

response = natural_language_understanding.analyze(
    text=text_hello_world,
    features=Features(emotion=EmotionOptions(targets=['Hello','World']))).get_result() #Targets target a key...
#phrase in the text. Since we'll probably be quite generic in our inputs, we can probably get...
#away with a loop through the text to get our targets.

print(json.dumps(response, indent=2))