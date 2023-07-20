import whisper
import sys
from deep_translator import GoogleTranslator
if len(sys.argv) != 3:
    raise ValueError("Arguments must be 3")
filename = sys.argv[1]
whisper_model = whisper.load_model("large")
result = whisper_model.transcribe(filename, verbose = True)
#resultは辞書型になっている。検知した言語情報とかもここに含まれている。
with open(sys.argv[2], "w") as f:
    f.write("detected_langage: "+result["language"]+"\n")
    f.write(result["text"])
    f.write("\n")
    f.close()

f = open(sys.argv[2])
lines = f.readlines()
detected_lang = result["language"] 
if detected_lang == "ja":
    sys.exit()
else:
    with open(sys.argv[2], "a") as f2: #追記モードで読む
        for i in range(1,len(lines)):
            f2.write("translated_langage: ja\n")
            translated = GoogleTranslator(source='auto',target='ja').translate(lines[i])
            f2.write(translated)
        f2.close()