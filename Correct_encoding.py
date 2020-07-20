import os
from chardet.universaldetector import UniversalDetector
import traceback


detector = UniversalDetector()
encodings = []
items = []
data = None
for root, dirs, files in os.walk(os.getcwd()):
    for file in files:
        if file.endswith(".txt"):
            items.append(os.path.join(root, file))


for item in items:
    with open(item, 'rb') as fh:
        for line in fh:
            detector.feed(line)
            if detector.done:
                break
        detector.close()
    encodings.append(detector.result)
encodings_dict = {item: encoding['encoding'] for item in items for encoding in encodings}
print(encodings_dict)

for item in items:
    unknown_encoding_text = open(item, 'rb').read()
    try:
        text_in_unicode = unknown_encoding_text.decode(encodings_dict[item])
        new_text = text_in_unicode.encode('utf-8')
    except Exception:
        print('не удалось перекодировать файл ' + item + ' ошибка' + traceback.format_exc())
        pass
    else:
        os.remove(item)
        with open(item, 'wb') as new_file:
            new_file.write(text_in_unicode.encode('utf-8'))
        print('файл ' + item + ' перекодирован из ' + encodings_dict[item])
