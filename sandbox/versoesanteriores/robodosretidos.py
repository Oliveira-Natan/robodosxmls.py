import os.path, time
from datetime import datetime
import shutil

# listing files changed in the last 01 hour
source = r'F:\Impostos Retidos\FIT_XML_TERCEIRO'
destiny = r'F:\Impostos Retidos\Conversor FIT'

past = time.time() - 1*60*60  # 1 hours
source_files = []
for p, ds, fs in os.walk(source):
    for fn in fs:
        filepath = os.path.join(p, fn)
        if os.path.getmtime(filepath) >= past:
            source_files.append(filepath)
print(source_files)

# copying files to new destiny
for file in source_files:
    shutil.copy(file, destiny)
