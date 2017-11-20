#!/usr/bin/python

import cgi
import time
import base64
import hashlib
import os

print "Content-type: text/html\n"

ts_check=0
u_check=0

form = cgi.FieldStorage()

if ("t" in form and  "u" in form):

    requesting_user = form['u'].value
    requesting_ts = form['t'].value

    valid_users=["none","amzn1.ask.account.AEOCQMKJXXGNK7NVIWHKT6EFHFP2BQZBHRS4Z2ECQSGC247MAXBEW2QJROORRRRKARAEIWAI4SF47J2KMG6PGN65BVZS7DM6HUHO2DSNX7GZTG6H7SR4FZU67HDWM6FJ2LNJ6K7LSTF3V33EHJ54A7B5JK734YBJCPAL2QAYAQE3SEGGNIXB4GHPWKQ2MS5M2TCLUQSOWJUQXLY"]

    ts_local=int(time.time())
    ts_received=base64.b64decode(requesting_ts)

    if abs((int(ts_received)-int(ts_local)))<3:
        #print "TS CHECK PASSED"
        ts_check=1

    user_hashes=[]
    for user in valid_users:
        user_hash_string=user+str(ts_received)
        user_hashes.append(hashlib.sha256(user_hash_string).hexdigest())

    if requesting_user in user_hashes:
        #print "USER CHECK PASSED - %s" % requesting_user
        u_check=1


    if (ts_check==1 and u_check==1):
        print "0 - ALL CHECKS PASSED:  GENERATING REQUEST"
        os.system('mosquitto_pub -t "Treats_in" -m "dispense"')
    else:
        print "-1 - CHECKS FAILED:  NO REQUEST IS PASSED"

else:
    print "-1 - INVALID FORM SUBMISSION: NO REQUEST IS PASSED"
