#!/usr/bin/env python

import os
import Levenshtein

directory = os.path.expanduser('~/Musique')
os.chdir(directory)

counterDirs = 0
counterFiles = 0
counterNb = 0

listDirs = []
listFiles = []
listNb = {}

for r, d, f in os.walk(directory):
    # parsing directories
    detection = 0.9  # Levenshtein distance trigger; tune this to catch more
    i = 0
    while i < len(d)-1:
        current, next = d[i].lower(), d[i+1].lower()
        levenshtein = Levenshtein.ratio(current, next)
        if levenshtein > detection:
            listDirs.append(os.path.join(r, d[i]))
            counterDirs += 1
        i += 1
    # parsing files
    j = 0
    while j < len(f)-1:
        current, next = f[j].lower(), f[j+1].lower()
        levenshtein = Levenshtein.ratio(current, next)
        if levenshtein > detection:
            listFiles.append(os.path.join(r, f[j]))
            counterFiles += 1
        j += 1
    if len(f) > 20:
        counterNb += 1
        listNb[r] = len(f)
print ('found ' + str(counterDirs) + ' duplicate(s) for dirs')
print ('\n'.join(listDirs))
print ('\n============')
print ('found ' + str(counterFiles) + ' duplicate(s) for files')
print ('\n'.join(listFiles))
print ('\n============')
print ('found ' + str(counterNb) + ' heavy dirs')
print ('\n'.join(['%s:: %s' % (key, value) for (key, value) in listNb.items()]))
