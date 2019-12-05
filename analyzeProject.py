from contextlib import redirect_stdout
from lxml import etree
import re
import glob


def countSourceChars(regexPath):
    totalNumChars = 0
    for path in glob.glob(regexPath, recursive=True):
        with open(path) as file:
            countCharsFile = 0
            for line in file:
                countCharsFile += len(line)
        totalNumChars += countCharsFile
    return totalNumChars


def generateReport(regexFile, filename, resultData):
    totalDupChars = 0
    countDuplicates = 0
    with open(filename+'.txt', 'w') as stdout:
        with redirect_stdout(stdout):
            for duplicate in resultData:
                totalDupChars += int(duplicate['numDupChars'])
                if re.search(r''+regexFile, duplicate['file']):
                    countDuplicates += 1
                    print("Duplicate #" + str(countDuplicates))
                    print("\t" + duplicate['file'] + "\t" +
                        "Duplicate chars: " + duplicate['numDupChars'] +
                        " Max chars in file: " + duplicate['maxChar'] +
                        " Percent duplicate code in file: " + str((int(duplicate['numDupChars'])/int(duplicate['maxChar']))*100))

    print("Total duplicate chars for " + filename + "file is: " + str(totalDupChars))
    return totalDupChars


duplicateFileXml = 'Duplicates_aggregate.xml'
root = etree.parse(duplicateFileXml)
duplicates = root.findall('duplicate')
resultDuplicateData = []

for element in duplicates:
    fragments = element.findall('fragment')

    countFiles = 0
    listFragments = [fragment.get('file') for fragment in fragments]
    if not all(item.split("/")[7] == listFragments[0].split("/")[7] for item in listFragments):
        for fragment in fragments:
            duplicateDict = {}
            countFiles += 1
            filePath = re.search(r".*/(.*/src/main/java/(ru)/.*\.java?)", fragment.get('file'))

            # if not filePath is None and not (fragment.get('file').endswith("_Per.java") or fragment.get('file').endswith("_Gen.java")):
            if not filePath is None:
                file = filePath.group(1)
                fileKye = 'file' + str(countFiles)
                duplicateDict['file'] = file
                duplicateDict['line'] = fragment.get('line')
                duplicateDict['numDupChars'] = str(int(fragment.get('end')) - int(fragment.get('start')))
                with open(file) as sourceFile:
                    maxCharFile = 0
                    for line in sourceFile:
                        maxCharFile += len(line)
                duplicateDict['maxChar'] = str(maxCharFile)

                if not resultDuplicateData:
                    resultDuplicateData.append(duplicateDict)
                else:
                    if duplicateDict['file'] not in [elemDuplicateData['file'] for elemDuplicateData in resultDuplicateData]:
                        print("Add new entry...")
                        resultDuplicateData.append(duplicateDict)
                    else:
                        print("Calculate exist entry...")
                        for elemDuplicateData in resultDuplicateData:
                            if duplicateDict['file'] == elemDuplicateData['file'] and duplicateDict['line'] != elemDuplicateData['line']:
                                elemDuplicateData['numDupChars'] = str(int(elemDuplicateData['numDupChars']) + int(duplicateDict['numDupChars']))

numDupChar = generateReport('.*/src/main/java/ru/.*.java', 'duplicate_class', resultDuplicateData)

projects = ['utilities', 'base', 'program']
totalSigmaNumChars = 0
for project in projects:
    countCharsFile = countSourceChars(project + '/**/ru/**/*.java')
    totalSigmaNumChars += countCharsFile

print("Total number chars of project is: ", totalSigmaNumChars)

print("Percent duplicate source code in project: %s " % (str(int((numDupChar/totalSigmaNumChars) * 100))))
