import argparse
# 第一次运行这个代码
'''
import comtypes.client
try:
    from comtypes.gen import SpeechLib
except ImportError:
    engine = comtypes.client.CreateObject('SAPI.SpVoice')
    stream = comtypes.client.CreateObject('SAPI.SpFileStream')
    from comtypes.gen import SpeechLib
    stream.Open('output.wav',SpeechLib.SSFMCreateForWrite)
    engine.AudioOutputStream=stream
    with open('input.txt','r', encoding ='utf - 8') as f:
        text = f.read()
    engine.speak(text)
    stream.close()
'''


from comtypes.client import CreateObject
from comtypes.gen import SpeechLib  # 第一次运行后会自动生成comtypes.gen
def txt2wav(inputtxt,outputwav):
    engine = CreateObject('SAPI.SpVoice')
    stream = CreateObject('SAPI.SpFileStream')
    stream.Open(outputwav,SpeechLib.SSFMCreateForWrite)
    engine.AudioOutputStream = stream
    with open(inputtxt, 'r', encoding='utf - 8') as f:
        text = f.read()
    engine.speak(text)
    stream.close()

if __name__ == '__main__':
    phaser = argparse.ArgumentParser()
    phaser.add_argument('--inputtxt',required=True)
    phaser.add_argument('--outputwav',required=True)
    args = phaser.parse_args()
    inputtxt, outputwav = args.inputtxt,args.outputwav
    txt2wav(inputtxt, outputwav)