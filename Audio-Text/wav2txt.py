# https://www.lfd.uci.edu/~gohlke/pythonlibs/#pocketsphinx根据python版本号下载PocketSphinx
# https://sourceforge.net/projects/cmusphinx/files/Acoustic%20and%20Language%20Models/下载更多语言的模型，用everything查找pocketsphinx-data文件夹放入其中，按照en-US文件夹样式对文件改名
# 难度：语音识别＞文字转语音，语音识别文字效果往往不好
import speech_recognition as sr
import argparse


def wav2txt(inputwav, outputtxt, language):
    languages = {'English': 'en-US', 'Chinese': 'zh-CN'}
    r = sr.Recognizer()
    with sr.AudioFile(inputwav) as source:
        audio = r.record(source)
    text = r.recognize_sphinx(audio_data=audio, language=languages[language])
    print(text)
    with open(outputtxt, 'w') as f:
        f.write(text)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--inputwav', required=True)
    parser.add_argument('--outputtxt', required=True)
    parser.add_argument('--language', required=True)

    args = parser.parse_args()
    inputwav, outputtxt, language = args.inputwav, args.outputtxt, args.language
    wav2txt(inputwav, outputtxt, language)
