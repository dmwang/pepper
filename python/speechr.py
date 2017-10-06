#! /usr/bin/env python
# -*- encoding: UTF-8 -*-

"""Example: Use ALSpeechRecognition Module"""

import qi
import argparse
import sys
import time

class SpeechR(object):
    def __init__(self, app):
        super(SpeechR,self).__init__()
        app.start()
        session = app.session
        self.memory = session.service("ALMemory")
        
        self.subscriber = self.memory.subscriber("WordRecognized")
        self.subscriber.signal.connect(self.on_word_detected)

        self.tts = session.service("ALTextToSpeech")

        self.speechRec = session.service("ALSpeechRecognition")
        self.speechRec.setLanguage("English")
        vocabulary = ["yes", "no", "please", "hello"]
        self.speechRec.pause(True)
        self.speechRec.setVocabulary(vocabulary, False)
        self.speechRec.pause(False)
        self.speechRec.subscribe("SpeechR")
        print 'Speech recognition engine started'
        self.got_word = False
         
        self.tts = session.service("ALTextToSpeech")

    # Start the speech recognition engine with user Test_ASR
    #asr_service.subscribe("Test_ASR")
    #print 'Speech recognition engine started'
    #time.sleep(20)
    #asr_service.unsubscribe("Test_ASR")

    def on_word_detected(self, value):
        if value == []:
            self.got_word = False
        elif not self.got_word:
            #self.got_word = True
            for x in value:
                print x
            #print value[0]
            #self.tts.say("You just said " + str(value[0]) )
                
    def run(self):
        """
        Loop on, wait for events until manual interruption.
        """
        print "Starting SpeechR"
        try:
            while True:
                time.sleep(3)
        except KeyboardInterrupt:
            print "Interrupted by user, stopping HumanGreeter"
            self.speechRec.unsubscribe("SpeechR")
            #stop
            sys.exit(0)
        


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default="192.168.0.107",
                        help="Robot IP address. On robot or Local Naoqi: use '127.0.0.1'.")
    parser.add_argument("--port", type=int, default=9559,
                        help="Naoqi port number")

    args = parser.parse_args()
    
    try:
        # Initialize qi framework.
        connection_url = "tcp://" + args.ip + ":" + str(args.port)
        app = qi.Application(["SpeechR", "--qi-url=" + connection_url])
    except RuntimeError:
        print ("Can't connect to Naoqi at ip \"" + args.ip + "\" on port " + str(args.port) +".\n"
               "Please check your script arguments. Run with -h option for help.")
        sys.exit(1)

    sp_rec = SpeechR(app)
    sp_rec.run()
