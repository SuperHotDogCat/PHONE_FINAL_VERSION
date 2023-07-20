from deep_translator import GoogleTranslator
import sys
if len(sys.argv) != 2:
    print("Argments must be 2")
    sys.exit()
f = open(sys.argv[1])
lines = f.readlines()
ja_flag = True
detected_lang = lines[1].split()[2]
if detected_lang != "Japanese":
    ja_flag = False
if ja_flag:
    sys.exit()
else:
    for i in range(2, len(lines)):
        translated = GoogleTranslator(source='auto',target='ja').translate(lines[i])
        