import sys
import os
import shlex, subprocess
import numpy as np
import pandas as pd

debug = False

exams = []
scans = []
artifacts = []
typeOthers = []
typeOtherCounts = []
artifactCounts = []
paths = []
rootDir = 'Coil_Noise_QA_Output'

if debug == True:
    print(os.listdir())

for folder in os.listdir(rootDir):
    for subfolder in os.listdir(rootDir+'/'+folder):
        for file in os.listdir(rootDir+'/'+folder+'/'+subfolder):
            if 'log_summary' in file:
                fullPath = rootDir+'/'+folder+'/'+subfolder+'/'+file
                with open(fullPath) as logFile:
                    log = logFile.read()
                log_arr = log.split('\n')   # log file lines as an array

                # artifact presence indicated on 4th position of 3rd line (n=0)
                artifactCount = log_arr[2].split(' ')[3]
                artifactCounts.append(artifactCount)
                # Output 1 or 0
                if int(artifactCount) > 0:
                    artifacts.append('1')   # 1 if artifact detected on any of the images
                else:
                    artifacts.append('0')   # 0 otherwise

                # type other presence indicated on 4th position of 4th line (n=0)
                typeOtherCount = log_arr[3].split(' ')[3]
                typeOtherCounts.append(typeOtherCount)

                if int(typeOtherCount) > 0:
                    typeOthers.append('1')
                else:
                    typeOthers.append('0')

                paths.append('/MRI_DATA/coil-noise/scans/' + fullPath)
                parsedFileName = file.split('_')
                exams.append(parsedFileName[2].replace('e', ''))
                scans.append(parsedFileName[3].replace('s','').rstrip('.txt'))

                if debug == True:
                    print('no. of artifacts: ', artifactCount)
                    print('no. of other: ', typeOtherCount)

if debug == True:
    for i in exams:
        print('Exam: ', i)
    for i in scans:
        print('Scan: ', i)
    for i in artifacts:
        print('Artifact Present?: ', i)
    for i in artifactCounts:
        print('# of Artifacts: ', i)
    for i in typeOthers:
        print('Other present?: ', i)
    for i in typeOtherCounts:
        print('# of Others: ', i)
    for i in paths:
        print('Path to log: ', i)



df = pd.DataFrame(data={'Exam':exams, 'Scan':scans, 'Artifact Present?':artifacts, '# Artifacts':artifactCounts, 'Other Present?':typeOthers, '# Others':typeOtherCounts, 'path_toLog':paths }).sort_values('Exam')

if debug == True:
    print(df)

df.to_csv('log.csv', index=False)