# -*- coding: utf-8 -*-
import Image, ImageDraw, ImageFont

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

def generateModels(name, nameC):
    im = None
    imS = None
    draw = None
    w, h = 0, 0
    draw = None
    drawS = None
    stampID = 0
    serial = 0
    pageInfoList = []
    pageInfo = None
    text = ''
    flawList = []
    caseList = []

    f = open("statistic/statistic_" + name + ".txt")
    lines = f.readlines()
    for line in lines:
        line = line.strip()
        if line == "":
            if im <> None:
                im.save(pageInfo[2][0], 'png')
                tmpW, tmpH = imS.size
                tmpW /= 2
                tmpH /= 2
                imS = imS.resize((tmpW, tmpH), Image.ANTIALIAS)
                imS.save(pageInfo[2][1], 'png')
                pageInfo.append(text)
                pageInfo.append(flawList)
                pageInfo.append(caseList)
                im = None
                draw = None
                pageInfo = None
                text = ''
                flawList = []
        elif line[0] == "$":
            # this line is comments
            print "[comments:]" + line[1:]
        elif line[0] == "%":
            # this line is new stamp index
            # setup new ctxt
            stampID = line[1:]
            stampID = int(stampID)
            im = Image.open('model/model_' + name + '.png')
            imS = Image.open('model/model_' + name + '.png')
            draw = ImageDraw.Draw(im)
            drawS = ImageDraw.Draw(imS)
            serial = 0
            pageInfo = []
            pageInfoList.append(pageInfo)
            pageInfo.append(stampID)
            pageInfo.append("大清飞雁" + nameC + "邮票印刷缺陷" + " (#" + str(stampID) + ")")
            pageInfo.append(['model/' + name + '/' + 'model_' + name + '_' + str(stampID/10) + str(stampID%10) + '.png', 'model/' + name + '/' + 'model_' + name + '_' + str(stampID/10) + str(stampID%10) + '_s.png'])
            print "stamp: " + str(stampID)
        elif line[0] == "#":
            # this line is flaw 
            coord = line[1:].split("|")[0]
            desc = line[1:].split("|")[1]
            serial += 1
            if coord.find("-") >= 0:
                # this is a line:
                x1, y1 = coord.split("-")[0].split(",")[0], coord.split("-")[0].split(",")[1]
                x2, y2 = coord.split("-")[1].split(",")[0], coord.split("-")[1].split(",")[1]
                x1, y1, x2, y2 = normalize(x1, y1, x2, y2)
                markFlawLine(draw, x1, y1, x2, y2, serial)
                markFlawPointS(drawS, 1.0*(x1+x2)/2, 1.0*(y1+y2)/2)
                x1InStamp, y1InStamp = physicalLocation(x1, y1)
                x2InStamp, y2InStamp = physicalLocation(x2, y2)
                flawList.append([[x1InStamp, y1InStamp, x2InStamp, y2InStamp], desc])
                print "line: " + str([x1InStamp, y1InStamp, x2InStamp, y2InStamp]) + ": " + desc
            else:
                # this is a dot
                x, y = coord.split(",")[0], coord.split(",")[1]
                x, y, XXX, YYY = normalize(x, y)
                markFlawPoint(draw, x, y, serial)
                markFlawPointS(drawS, x, y)
                xInStamp, yInStamp = physicalLocation(x, y)
                flawList.append([[xInStamp, yInStamp], desc])
                print "dot: " + str([xInStamp, yInStamp]) + ": " + desc
        elif line[0] == "&":
            # this line is text
            text += line
            print "[text]: " + line
        else:
            print "[unknown]: " + line

    f.close()

    flawUrlBase = 'http://michael2012z.github.io/ChinaFlyingGooseStamps/flaw/'

    # now generate pages
    for i in range(0, len(pageInfoList)):
        pageInfo = pageInfoList[i]
        stampID = pageInfo[0]
        print pageInfo
        # page head
        pageText = '''
<!DOCTYPE html>
<html lang="en">
	<head>
		<meta charset="utf-8"/>
		<title> '''
        pageText += pageInfo[1]
        pageText += '''</title>
		<!-- For responsive site
			<meta name="viewport" content="width=device-width, initial-scale=1.0">
		-->
		<meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">
		<link rel="author" href="/ChinaFlyingGooseStamps/humans.txt">
		<meta name="description" content="Description Goes Here">
		<link rel="stylesheet" href="/ChinaFlyingGooseStamps/css/style.css">
		<!--[if IE 7]>
			<html class="ie7"> 
			<link rel="stylesheet" type="text/css" href="/css/font-awesome-ie7.min.css">
		<![endif]-->
		<!--[if IE 8]><html class="ie8"> <![endif]-->		
	    <!--[if lt IE 9]>
	      <script src="http://html5shim.googlecode.com/svn/trunk/html5.js"></script>
	    <![endif]-->

		<link rel="apple-touch-icon-precomposed" sizes="144x144" href="ico/apple-touch-icon-144-precomposed.png">
		<link rel="apple-touch-icon-precomposed" sizes="114x114" href="ico/apple-touch-icon-114-precomposed.png">
		<link rel="apple-touch-icon-precomposed" sizes="72x72" href="ico/apple-touch-icon-72-precomposed.png">
		<link rel="apple-touch-icon-precomposed" href="ico/apple-touch-icon-57-precomposed.png">
		<link rel="shortcut icon" href="ico/favicon.png">	    
	</head>
'''

        # body
        pageText += '''
	<body>
	<!-- Header
	    ================================================== -->
	<header>

	</header>

	<div class="top-strip"></div>
<main class="content">
    <section class="container">
    	<div class="row-fluid">
    		<article class="home-icon">
				<a href="/ChinaFlyingGooseStamps/">
					<i class="icon-home"></i> 
				</a>
			</article>
			<article class="post">
                        '''
        # title
        pageText += '''        <h5>''' + "大清飞雁" + nameC + "邮票印刷缺陷全图" + '''</h5>'''
	pageText += '''			<h2 class="content">'''+ pageInfo[1] + '''</h2>
				<section>'''
        pageText += '''<h4 id="section">模型</h4>\n'''
        pageText += '<center><img src='
        pageText += "\"" + flawUrlBase + pageInfo[2][0] + "\"" + " width=\"420\""
        pageText += '/></center>\n'
        pageText += '''<h4 id="section">缺陷列表</h4>\n'''
        pageText += '<p>' + pageInfo[3] + '</p>\n'
        pageText += '<ol>\n'
        for flawItem in pageInfo[4]:
            if len(flawItem[0]) == 2:
                coord = "(" + str(flawItem[0][0]) + "mm, " + str(flawItem[0][1]) + "mm)"
            elif len(flawItem[0]) == 4:
                coord = "(" + str(flawItem[0][0]) + "mm, " + str(flawItem[0][1]) + "mm) - "
                coord += "(" + str(flawItem[0][2]) + "mm, " + str(flawItem[0][3]) + "mm)"
            else:
                print "error"
                return
            pageText += '<li>\n'
            pageText += coord + " : " + flawItem[1]
            pageText += '</li>\n'
        pageText += '</ol>\n'
        pageText += '''<h4 id="section">实例</h4>\n'''
        for casePic in pageInfo[5]:
            pageText += '<center><img src='
            pageText += "\"" + flawUrlBase + casePic + "\""
            pageText += '/></center>\n'

        pageText += '''
</section>
				<section style="font-weight:bold; margin-bottom: 2em;">'''
        if i > 0:
            pageText += '''
            <a rel="prev" class="a-hover"href="'''
            pageText += flawUrlBase + "pages/" + name + "/" + 'page_' + name + '_' + str((stampID-1)/10) + str((stampID-1)%10) + '.html'
            pageText += '''"><i class="icon-double-angle-left"></i>''' + pageInfoList[i-1][1] + '''</a>\n'''
	if i < len(pageInfoList)-1:					
            pageText += '''<a rel="next" style="float:right" class="a-hover"href="'''
            pageText += flawUrlBase + "pages/" + name + "/" + 'page_' + name + '_' + str((stampID+1)/10) + str((stampID+1)%10) + '.html'
            pageText += '''">''' + pageInfoList[i+1][1] + ''' <i class=" icon-double-angle-right"></i></a>
				</section>
			</article>
		</div>
	</section>
</main>


	<footer>
		<div class="container">
			Author: <a href="http://www.2ndmoon.net/">Michael Z</a>
		</div>
	</footer>

	<!-- Footer
	    ================================================== -->

	<!-- Javascripts 
	    ================================================= -->
	<script src="/ChinaFlyingGooseStamps/js/jquery.min.js"></script>
	<script src="/ChinaFlyingGooseStamps/js/custom.js"></script>

    <!-- Analytics
    ================================================== -->
    <script>
		// analytics code
    </script>	
	</body>
</html>
'''

        f = open("pages/" + name + "/" + 'page_' + name + '_' + str(stampID/10) + str(stampID%10) + '.html', 'w')
        f.write(pageText)
        f.close()
        
    # now generate index content
    pageText = '''
<!DOCTYPE html>
<html lang="en">
	<head>
		<meta charset="utf-8"/>
		<title> 
'''
    pageText += "TEST"
    pageText += ''' </title>
	</head>
'''
    pageText += '<body>\n'
    pageText += '<center>\n'
    for i in range(0, 6):
        pageText += '<div style="line-height:0">'
        for j in range(0, 8):
            stampID = pageInfoList[i*8+j][0]
            pageText += '<a target="_blank" href='
            pageText += flawUrlBase + "pages/" + name + "/" + 'page_' + name + '_' + str(stampID/10) + str(stampID%10) + '.html'
            pageText += '><img width="87" src='
            pageText += flawUrlBase + pageInfoList[i*8+j][2][1]
            pageText += '></a>'
        pageText += '</div>\n'
    pageText += '</center>\n'
    pageText += '''
        </body>
</html>'''
    f = open("pages/" + name + "/" + 'index.html', 'w')
    f.write(pageText)
    f.close()
        


generateModels("1d", "壹元")
#generateModels("2d")
#generateModels("5d")

