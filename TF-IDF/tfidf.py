

import re
import math

# create list with files
pf = open("tfidf_docs.txt", "r")
fileList = []
for r in pf:
    fileList.append(r.strip())
pf.close()
