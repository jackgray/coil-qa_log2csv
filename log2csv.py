import sys
import os
import shlex, subprocess
import numpy as np
import pandas as pd
import gspread
from df2gspread import df2gspread as d2g
from oauth2client.service_account import ServiceAccountCredentials

debug = True

# Set up Google Sheets interface
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name('google-credentials.json', scope)
gc = gspread.authorize(credentials)
wks = gc.open("nyspi coil qa summaries").sheet1
ss_key = 'replace'
wks_name = 'Sheet1'

exams = []
scans = []
artifacts = []
typeOthers = []
typeOtherCounts = []
artifactCounts = []
paths = []
dates = []
rootDir = '/MRI_DATA/coil-noise/scans/Coil_Noise_QA_Output'
#  /MRI_DATA/coil-noise/scans

if debug == True:
    print(os.listdir())

for folder in os.listdir(rootDir):
    for subfolder in os.listdir(rootDir+'/'+folder):
        try:
            for file in os.listdir(rootDir+'/'+folder+'/'+subfolder):
                if 'log_summary' in file:
                    fullPath = rootDir + '/' + folder + '/' + subfolder + '/' + file

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

                    paths.append(fullPath)
                    parsedFileName = file.split('_')
                    exams.append(parsedFileName[2].replace('e', ''))
                    scans.append(parsedFileName[3].replace('s','').rstrip('.txt'))

                    if debug == True:
                        print('no. of artifacts: ', artifactCount)
                        print('no. of other: ', typeOtherCount)
        except:
            pass

if debug == True:
    for i in exams:
        print('Exam: ', i)
    for i in scans:
        print('Scan: ', i)
    for i in artifacts:
        print('Artifact Present?: ', i)
    for i in artifactCounts:
        print('No. of Artifacts: ', i)
    for i in typeOthers:
        print('Other present?: ', i)
    for i in typeOtherCounts:
        print('No. of Others: ', i)
    for i in paths:
        print('Path to log: ', i)

df = pd.DataFrame(data={'Exam':exams, 'Scan':scans, 'Artifact Present?':artifacts, 'No. of Artifacts':artifactCounts, 'Other Present?':typeOthers, 'No. of Others':typeOtherCounts, 'path_toLog':paths }).sort_values('Exam')

if debug == True:
    print(df)

# Save csv to log.csv and google sheets
df.to_csv('log.csv', index=False)
d2g.upload(df, ss_key, wks_name, credentials=credentials, row_names=True)

print('Results saved to log.csv and uploaded to google sheets at https://docs.google.com/spreadsheets/d/1WyytHPL3k5slpZQ4eOMvwEB-rjp2jJf0nKY0I5ALHOQ/edit#gid=0')