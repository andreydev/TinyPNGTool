'''
MIT License

Copyright (c) 2017 Andrey Lopukhov

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

import tinify, os, sys, argparse

# Arg parser
parser = argparse.ArgumentParser(description='[*] TinyPNG uploading tool [*]')
parser.add_argument('-ak', '--apikey', help='API key to use', required=False, type=str)
parser.add_argument('-ms', '--minsize', help='Minimum size to upload in bytes, default is 100KB', required=False, type=int)
parser.add_argument('-i', '--ignore', help='Ignored file names separated by space (Example: -i file1.png file2.png)',
                    nargs='+', required=False, type=str)

args = vars(parser.parse_args())

# Configuration
apiKey = ''
minSize = 1024 * 100  # Bytes, default is 100KB
fileTypes = ['.png', '.jpg']
ignoreFiles = []

if type(args['apikey']) is str:
    apiKey = args['apikey']
if type(args['minsize']) is int:
    minSize = args['minsize']
if type(args['ignore']) is list or type(args['ignore']) is str:
    ignoreFiles = list(args['ignore'])

# Inner
fileCount = 0
oldFiles = {}
newFiles = {}
tinify.key = apiKey

if apiKey == '':
    print 'API key is missing, please check out the readme file'
    os.system("pause")
    sys.exit()


def getSize(fileObject):
    fileObject.seek(0, 2)
    size = fileObject.tell()
    return size


def printNewSizes():
    for key, value in oldFiles.iteritems():
        print 'Name: ' + str(key) + ' | Old size: ' + str(value / 1024) + 'KB' + ' | New size: ' + str(
            newFiles[key] / 1024) + 'KB' + ' | New size is: ' + str(int(float(newFiles[key]) / value * 100)) + '%'


for fn in os.listdir(os.path.dirname(os.path.realpath(__file__))):
    if os.path.isfile(fn):
        if fn not in ignoreFiles:
            extension = os.path.splitext(fn)[1]
            if extension in fileTypes:
                file = open(fn, 'rb')
                size = getSize(file)
                if size > minSize:
                    oldFiles[fn] = size
                    fileCount += 1
                file.close()

if fileCount > 0:
    print 'Found: ' + str(fileCount) + ' files and starting to compress'
else:
    print 'Found: ' + str(fileCount) + ' files, quitting'

for key, value in oldFiles.iteritems():
    source = tinify.from_file(key)
    source.to_file(key)
    file = open(key, 'rb')
    size = getSize(file)
    newFiles[key] = size
    print str(fileCount) + ' files left'
    fileCount -= 1
    file.close()

printNewSizes()

os.system("pause")
