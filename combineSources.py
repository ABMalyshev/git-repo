import glob
import re
from contextlib import redirect_stdout

allData = ''

sources = ['**/*.java', 'frontend/packages/**/*.js']

for sourcePath in sources:
    for path in glob.glob(sourcePath, recursive=True):
        with open(path) as file:
            sourceFile = file.read()
            if not re.findall(r'([Pp]assword|PASSWORD|[Tt]oken)', sourceFile):
                allData += sourceFile

    with open('allSource.txt', 'w') as resultFile:
        with redirect_stdout(resultFile):
            print(allData)

