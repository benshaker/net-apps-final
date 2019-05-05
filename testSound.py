import os
from pydub import AudioSegment

# sound = AudioSegment.from_mp3("kid_laugh.mp3")
# sound.export("kid_laugh.wav", format="wav")
os.system('aplay -q -D bluealsa:HCI=hci0,DEV=FC:58:FA:A6:22:95,PROFILE=a2dp Hawk.wav')
