# -*- coding: utf-8 -*-
from PIL import Image, ImageDraw, ImageFont
import os

def generateSnapshots(baseFolder):
    srcFolder = baseFolder + "src/"
    snpFolder = baseFolder + "snp/"
    srcFiles = os.listdir(srcFolder)
    srcFiles.sort()
    for srcFile in srcFiles[::-1]:
        if os.path.isfile(srcFolder + srcFile):
            try:
                imS = Image.open(srcFolder + srcFile)
                tmpW, tmpH = imS.size
                targetWidth = 160
                targetHeight = (int)((float)(tmpH) / (float)(tmpW) * targetWidth)
                imS = imS.resize((targetWidth, targetHeight), Image.ANTIALIAS)
                imS.save(snpFolder + srcFile, 'jpeg')
                print snpFolder + srcFile + " generated"
            except Exception, e:
                print e

if __name__ == '__main__':
    stamps = [
        {'folder':'1d/library/mint/'},
        {'folder':'1d/library/used/'},
        {'folder':'2d/library/mint/'},
        {'folder':'2d/library/used/'},
        {'folder':'5d/library/mint/'},
        {'folder':'5d/library/used/'},
    ]

    for stamp in stamps:
        generateSnapshots("../" + stamp['folder'])
