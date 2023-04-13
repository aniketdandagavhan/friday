# hotwards = ["hello friday","wake up","turn on","are you there","friday","whatsapp","whats up","daddy's home"]

# def hotword(sentence):

#     for word in hotwards:
#         if word in sentence:
#             return True
#     return False

import os
from eff_word_net.streams import SimpleMicStream
from eff_word_net.engine import HotwordDetector, MultiHotwordDetector

def hotword():
    friday_hw = HotwordDetector(
        hotword="friday",
        reference_file = "MainEngine//Database//HotwordJson//friday_ref.json",
        threshold=0.995
    )

    wakeup_hw = HotwordDetector(
        hotword="wake up",
        reference_file = "MainEngine//Database//HotwordJson//wakeUp_ref.json",
        threshold=0.97
    )

    multi_hw_engine = MultiHotwordDetector(
        detector_collection = [
            friday_hw,
            wakeup_hw,
        ],
    )

    mic_stream = SimpleMicStream()
    mic_stream.start_stream()

    while True :
        frame = mic_stream.getFrame()
        result = multi_hw_engine.findBestMatch(frame)
        if result==None :
            #no voice activity
            continue
        if(None not in result):
            # print(result)
            return True

# hotword()