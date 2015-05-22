import Image, ImageDraw, ImageFont

imageWidth = 577
imageHeight = 668
# radius of serial-number circle
r = 12
# cross arm length
l = 10
# dot size
d = 4

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
    print textSizeW, textSizeH
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

def generateModels(name):
    im = None
    draw = None
    w, h = 0, 0
    draw = None
    stampID = 0
    serial = 0

    f = open("statistic/statistic_" + name + "_.txt")
    lines = f.readlines()
    for line in lines:
        print line
        if line.find(":") >= 0:
            # this is a new file
            # release existing things
            if im <> None:
                im.save('model/' + name + '/' + 'model_' + name + '_' + str(stampID/10) + str(stampID%10) + '.png', 'png')
                im = None
                draw = None
            # setup new ctxt
            stampID = line.split(":")[0]
            if stampID == '':
                return
            stampID = int(stampID)
            im = Image.open('model/model_' + name + '.png')
            draw = ImageDraw.Draw(im)
            serial = 0
            print "stamp: " + str(stampID)
        if line.find("-") >= 0:
            # this is a line flaw
            serial += 1
            x1, y1 = line.split("-")[0].split(",")[0], line.split("-")[0].split(",")[1]
            x2, y2 = line.split("-")[1].split(",")[0], line.split("-")[1].split(",")[1]
            x1, y1, x2, y2 = normalize(x1, y1, x2, y2)
            markFlawLine(draw, x1, y1, x2, y2, serial)
            print "line: " + str([x1, y1, x2, y2])
        elif line.find(",") >= 0:
            # this is a dot flaw
            serial += 1
            x, y = line.split(",")[0], line.split(",")[1]
            x, y, XXX, YYY = normalize(x, y)
            markFlawPoint(draw, x, y, serial)
            print "dot: " + str([x, y])
            
    f.close()


generateModels("1d")
#generateModels("2d")
#generateModels("5d")

