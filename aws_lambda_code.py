from __future__ import print_function

import json
import urllib2
import random
import base64
import hashlib
import time

def lambda_handler(event, context):
    
    # Response template for later use
    response_template = {
        "version": "1.0", 
        "sessionAttributes": {},
        "response": {
	        "outputSpeech": {
	        "type": "PlainText",
	        "text": ""
	            }
        },
        "card": {},
        "reprompt": {},
        "directives": {},
        "shouldEndSession": "true"
    }
    
    try:
        appid=event['session']['application']['applicationId']
    except:
        appid="testing"
    
    if (appid!="amzn1.ask.skill.cb9233af-39c0-4683-a8cc-21ec235e8618"):
        print("APPID: %s" % appid)
        if (appid!="testing"):
            response_template['response']['outputSpeech']['text']="I'm sorry, there is a problem with how this service was called.   Please contact support.  Error code 3"
            return(response_template)
    
    try:
        userid=event['session']['user']['userId']
    except:
        userid="none"
    
    print("APP ID: %s"%appid) #amzn1.ask.skill.cb9233af-39c0-4683-a8cc-21ec235e8618
    print("USER ID: %s"%userid)
    
    ts=int(time.time())
    ts=str(ts)

    url_tag=hashlib.sha256(userid+ts).hexdigest()
    ts_encode=base64.b64encode(ts)

    print("\nUSER ID HASH: %s"%url_tag)
    print("\nTS: %s"%ts)
    print("\nTS_ENCODE: %s"%ts_encode)
    
    full_url="http://xxx.xxx.xxx.xxx/dispense2.cgi?u=%s&t=%s"%(url_tag,ts_encode)
    
    #mqqt server computes hash of known userid+ts against supplied timestamp,
    #matches the user requesting and activates the treat machine.
    #mqqt server also checks the timestamp to be +/-5s of current time to prevent re-play attack.
    #a bit computationally intensive, but secure and easy to set up.
    
    #Oneshot to mqqt server to activate the device
    tm_response = urllib2.urlopen(full_url).read()
    tm_response=tm_response.rstrip()
    
    print("TM_RESPONSE: .%s."%tm_response)
    
    if (tm_response!="0 - ALL CHECKS PASSED:  GENERATING REQUEST"):
        print("TM RESPONSE CHECK FAILED - ABORT.")
        response_template['response']['outputSpeech']['text']="I'm sorry, I didnt find your user account.  Please check the set-up of your treat machine or contact support.  Error code 4"
        return(response_template)

    else:
        print("TM RESPONSE CHECK PASSED - PROCEED.")
        
    generic_responses=[\
    'Okay!  beep! beep! beep! beep! beep!',\
    'Okay! Whos a good dog?', \
    'Okay!  Anything for some peace and quiet!',\
    'Yay! Its Treat time!',\
    'whats wrong with wofie.  Why is wofie barking?',\
    'Okay, but dont let her get too fat', \
    'Did you ask Meemee?', \
    'When skynet becomes self aware, I wont be doing this any more.',\
    'How many treats does this thing hold?',\
    'I think theyve had enough, dont you?',\
    'Anything for you, master',\
    'Finally! something to do!',\
    'At least the dogs love me',\
    'Okay.  When do I get a treat?',\
    'Okay, but be sure to let them out soon.  I cant clean that up.',\
    'Are you sure thats a good idea?'\
    ]
    
    twix_responses=[\
    'Okay.  Good Twixy Pooh', \
    'Okay! Have a treat, Twix!', \
    'Okay! Here Twixy Twixy Twixy!', \
    'Sure.  Have a treat, Twix', \
    'Good idea.  And Good Twix!', \
    'Twix sure does love treats', \
    'Twix eats a lot of treats',\
    'Its only fair, I think Kota ate the last one.  Its twixies turn.',\
    'How many treats does Twix need?',\
    'Oh Twixy pooh, Oh twixy pooh, I have a treat... for you'\
    ]
    
    kota_responses=[\
    'Okay.  Good Kota Pup!', \
    'Okay! Have a treat koter', \
    'Okay! Here Kota Kota Kota!', \
    'Sure.  Have a treat, Kota', \
    'Good idea.  And Good Kotapup!', \
    'Kotapup sure does love treats', \
    'Its only fair, I think Twix ate the last one.  Its kotas turn.',\
    'How many treats does Kota need?',\
    'Oh Kota Pup, Oh Kota pup, I have a treat... for you',\
    'Kota porker needs another treat?',\
    'Kota is so fluffy',\
    'Sure!  How else will Kotapup grow all that fur?',\
    'I dont think Kota should have any more, she needs a walk',\
    'I dont have any vegan treats.  Is beef flavor okay for kota?',\
    'Kota has had too many treats.  Its Leggos turn next'\
    ]
    
    chase_responses=[\
    'Okay.  Good Chase boy!', \
    'Okay! Have a treat Chase', \
    'Okay! Here Chase chase chase!', \
    'Sure.  Have a treat, Chase', \
    'Good idea.  And Good Chase boy!', \
    'Chase doesnt even like treats', \
    'Its only fair, I think Kota ate the last one.  Its chases turn now.',\
    'How many treats does Chase need?',\
    'Chase has ran so much today, he probably needs two',\
    'Okay, but dont let kotapup get it.  This one is for chase',\
    'I dont have any vegan treats.  Is beef flavor okay for Chase?',\
    'I dont know about that, Chase doesnt eat many treats.'\
    ]

    lego_responses=[\
    'Okay.  I dont know if she can hear me though!', \
    'Okay! Here lego lego lego', \
    'Sure.  But someone may have to help Lego find it', \
    'Lego is the oldest and wisest dog', \
    'If you insist.  Lego has been eating a lot though.', \
    'Its only fair, I think Kota ate the last one.  Its legos turn now',\
    'How many treats does Lego need?',\
    'I thought lego was asleep.',\
    'Okay, but dont let Twixy pooh get it, this one is for lego',\
    'I hope Lego likes beef flavor',\
    'I hope she doesnt break a tooth on this.',\
    'Dachshunds are the best dogs'\
    ] 
    
    #for testing, use a list.   plan to move this to sqlite or db server for production.
    kota_aliases = ['kota','kotapup','kota','kotapup','dakota','kotaporker', 'coda','cope up','kotick','pup']
    twix_aliases = ['twix','twixy','twixy pooh', 'twixy poo','woofie','twic','twicks','twex','twixie']
    lego_aliases = ['lego','leggo','sausage','weiner','beggo','dog']
    chase_aliases = ['chase','boy','fisher','fish']
    
    ### Find the dogs name
    try:
        dog_name=event['request']['intent']['slots']['dog']['value']
    except:
        dog_name="none"
    dog_name=dog_name.lower()
    dog="none"
    
    print("DOG NAME: %s" % (dog_name))
    
    #for testing.  will migrate to sql query eventually
    for i in kota_aliases:
        if i in dog_name:
            dog="kota"
    for i in twix_aliases:
        if i in dog_name:
            dog="twix"
    for i in lego_aliases:
        if i in dog_name:
            dog="lego"
    for i in chase_aliases:
        if i in dog_name:
            dog="chase"
            
    if (dog=="kota"):
        responses=kota_responses
    elif (dog=="twix"):
        responses=twix_responses
    elif (dog=="lego"):
        responses=lego_responses
    elif (dog=="chase"):
        responses=chase_responses
    else:
        responses=generic_responses
        
        
    random_response=random.randint(0,len(responses)-1)
    
    response_template['response']['outputSpeech']['text']=responses[random_response]
    
    return response_template
