# -*- coding: utf-8 -*-
from PIL import Image, ImageDraw, ImageFont
import os


'''
[
  { "id" = 1,
    "flawlist" = [
      {"type" = "dot", "x" = x, "y" = y, "desc" = 'xxxxxx'},
      {"type" = "line", "x1" = x1, "y1" = y1, "x2" = x2, "y2" = y2, "desc" = 'xxxxxx'},
    ]
  },
]
'''

def parse_statistics (filename):
    allRecords = []
    record = {"id":0, "flawlist":[]}
    flawList = []
    f = open(filename)
    lines = f.readlines()
    for line in lines:
        line = line.strip()
        if line == "":
            if record["id"] <> 0:
                record["flawlist"] = flawList
                flawList = []
                allRecords.append(record)
                record = {"id":0, "flawlist":[]}
            else:
                continue
        elif line[0] == "$":
            # this line is comments
            # print "[comments:]" + line[1:]
            _ = 0
        elif line[0] == "%":
            # this line is new stamp index
            stampID = line[1:]
            stampID = int(stampID)
            record["id"] = stampID
            # print "stamp: " + str(stampID)
        elif line[0] == "#":
            # this line is flaw 
            coord = line[1:].split("|")[0]
            desc = line[1:].split("|")[-1]
            if coord.find("-") >= 0:
                # this is a line:
                x1, y1 = coord.split("-")[0].split(",")[0], coord.split("-")[0].split(",")[1]
                x2, y2 = coord.split("-")[1].split(",")[0], coord.split("-")[1].split(",")[1]
                x1, y1, x2, y2 = float(x1),float(y1),float(x2), float(y2)
                flawList.append({"type":"line", "x1":x1, "y1":y1, "x2":x2, "y2":y2, "desc" : desc})
                # print "line: " + str([x1, y1, x2, y2]) + ": " + desc
            else:
                # this is a dot
                x, y = coord.split(",")[0], coord.split(",")[1]
                x, y = float(x), float(y)
                flawList.append({"type":"dot", "x":x, "y":y, "desc": desc})
                # print "dot: " + str([x, y]) + ": " + desc
        elif line[0] == "&":
            # this line is text
            # print "[text]: " + line
            _ = 0
        else:
            print "[unknown]: " + line

    f.close()

    return allRecords


'''-----------------------------------------------------------'''

stampWidth = 1.0 + 20.0 + 1.0
stampHeight = 1.0 + 23.5 + 1.0
imageWidth = 577
imageHeight = 668
# radius of serial-number circle
r = 12
# cross arm length
l = 10
# dot size
d = 4
# icon dot size
dotSizeS = 10

'''-----------------------------------------------------------'''

def markFlawPointS(imageDraw, x, y):
    dotSize = dotSizeS
    x = int(x)
    y = int(y)
    imageDraw.ellipse([x-dotSize, y-dotSize, x+dotSize, y+dotSize], 'blue')

def _markFlawPoint(imageDraw, x, y, lineSize, dotSize):
    x = int(x)
    y = int(y)
    imageDraw.line([x-lineSize, y-lineSize, x+lineSize, y+lineSize], 'blue')
    imageDraw.line([x-lineSize, y+lineSize, x+lineSize, y-lineSize], 'blue')    
    imageDraw.ellipse([x-dotSize, y-dotSize, x+dotSize, y+dotSize], 'blue')

def markFlawSerial(imageDraw, x, y, serial):
    x = int(x)
    y = int(y)
    font = ImageFont.truetype("arial.ttf", 18)
    imageDraw.arc([x-r, y-r, x+r, y+r], 0, 360, "white")
    textSizeW, textSizeH = font.getsize(str(serial))
    #print textSizeW, textSizeH
    imageDraw.text([x-int(textSizeW/2), y-int(textSizeH/2)-4], str(serial), font=font)

def markFlawPoint(imageDraw, x, y, serial):
    _markFlawPoint(imageDraw, x, y, l, d)
    textX = x
    textY = y + l + r
    if (textX - r < 0):
        textX = r
    if (textX + r > imageWidth):
        textX = imageWidth - r
    if (textY + r > imageHeight):
        textY = y -l -r
    markFlawSerial(imageDraw, textX, textY, serial)

def markFlawLine(imageDraw, x1, y1, x2, y2, serial):
    _markFlawPoint(imageDraw, x1, y1, l * 0.75, d * 0.75)
    _markFlawPoint(imageDraw, x2, y2, l * 0.75, d * 0.75)
    imageDraw.line([x1, y1, x2, y2], 'blue')
    textX = x1
    textY = y1 + l * 0.75 + r
    if (textX - r < 0):
        textX = r
    if (textX + r > imageWidth):
        textX = imageWidth - r
    if (textY + r > imageHeight):
        textY = y1 - l * 0.75 - r
    markFlawSerial(imageDraw, int(textX), int(textY), serial)

def normalize(x1, y1, x2=0, y2=0):
    xx1 = float(x1)/44 * imageWidth
    xx2 = float(x2)/44 * imageWidth
    yy1 = float(y1)/51 * imageHeight
    yy2 = float(y2)/51 * imageHeight
    return xx1, yy1, xx2, yy2

def physicalLocation(x, y):
    xx = float(x)/imageWidth * stampWidth
    yy = float(y)/imageHeight * stampHeight
    return round(xx, 2), round(yy, 2)

'''
$ comments start with $
$ stamp start with %
$ flaw start with #
$ text start with &
$ flaw description follows |
'''

# pageInfo structure: [ id, title, [big picture, small picture], text, [flaw list, ...], [case list, ...]]

def generateModel(record, name):
    stampID = record['id']
    im = Image.open('../flaw/model/model_' + name + '.png')
    imS = Image.open('../flaw/model/model_' + name + '.png')
    draw = ImageDraw.Draw(im)
    drawS = ImageDraw.Draw(imS)
    serial = 0
    for flaw in record['flawlist']:
        serial += 1
        if flaw['type'] == "dot":
            x, y = flaw['x'], flaw['y']
            x, y, XXX, YYY = normalize(x, y)
            markFlawPoint(draw, x, y, serial)
            markFlawPointS(drawS, x, y)
        elif flaw['type'] == "line":
            x1, y1, x2, y2 = flaw['x1'], flaw['y1'], flaw['x2'], flaw['y2']
            x1, y1, x2, y2 = normalize(x1, y1, x2, y2)
            markFlawLine(draw, x1, y1, x2, y2, serial)
            markFlawPointS(drawS, 1.0*(x1+x2)/2, 1.0*(y1+y2)/2)
    bigPicName = '../flaw/model/' + name + '/' + 'model_' + name + '_' + str(stampID/10) + str(stampID%10) + '.png'
    litPicName = '../flaw/model/' + name + '/' + 'model_' + name + '_' + str(stampID/10) + str(stampID%10) + '_s.png'
    im.save(bigPicName, 'png')
    tmpW, tmpH = imS.size
    tmpW /= 2
    tmpH /= 2
    imS = imS.resize((tmpW, tmpH), Image.ANTIALIAS)
    imS.save(litPicName, 'png')
    print "generated picture " + bigPicName

'''-----------------------------------------------------------'''

    
def generateFlawPage(record, name, nameC):
    return


def generateIndexPage(name):
    return

    

if __name__ == '__main__':
    stamps = [
        {'name':'1d', 'nameC':'壹元'},
    ]
    for stamp in stamps:
        allRecords = parse_statistics('../flaw/statistic/statistic_' + stamp['name'] + '.txt')
        for record in allRecords:
            generateModel (record, stamp['name'])
            generateFlawPage (record, stamp['name'], stamp['nameC'])
            generateIndexPage (stamp['name'])
