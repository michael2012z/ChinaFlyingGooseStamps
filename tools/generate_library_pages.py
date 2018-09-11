# -*- coding: utf-8 -*-
import os, time
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


def generate_lib_pages (name, nameC, category, categoryC):
    faceFiles = []
    categoryDir = '../' + name + '/library/' + category
    srcDir = categoryDir + '/src/'
    srcUrlDir = category + '/src/'
    snpDir = categoryDir + '/m_size/'
    snpUrlDir = category + '/m_size/'
    imageFiles = os.listdir(srcDir)
    imageFiles.sort()
    for imageFile in imageFiles[::-1]:
	if os.path.isfile( srcDir + imageFile) and os.path.splitext(imageFile)[1] == ".jpg" and os.path.splitext(imageFile)[0].find("A") > 0 and os.path.splitext(imageFile)[0].find("A") == (len(os.path.splitext(imageFile)[0])-1):
	    faceFiles.append([srcUrlDir + imageFile, snpUrlDir+ os.path.splitext(imageFile)[0] + ".jpg"]) 

    pageContent = ''
    count = 0
    for faceFile in faceFiles:
	if count % 4 == 0:
	    pageContent += "<div>"
	pageContent += "<a target=\"_blank\" href=\""
	pageContent += faceFile[0]
	pageContent += "\">"
	pageContent += "<img width=\"160\" src=\""
	pageContent += faceFile[1]
	pageContent += "\"></a>"
	if count % 4 == 3:
	    pageContent += "</div>\r\n"
	count += 1
    if count % 4 <> 0:
	pageContent += "</div>\r\n"

    templateFile = open('page_templates/library_page_template.html')
    template = templateFile.read()
    templateFile.close()
    
    template = template.replace('[REPLACE_NAME_TEXT]', nameC)
    template = template.replace('[REPLACE_TYPE_TEXT]', categoryC)
    template = template.replace('[REPLACE_STAMP_LIST]', pageContent)

    # write page
    f = open ('../' + name + '/library/' + category + '.html', 'w')
    f.write(template)
    f.close()

    
if __name__ == '__main__':
    stamps = [
        {'name':'1d', 'nameC':'壹圆'},
        {'name':'2d', 'nameC':'贰圆'},
        {'name':'5d', 'nameC':'伍圆'},
    ]
    categories = [
        {'category':'mint', 'categoryC':'新票'},
        {'category':'used', 'categoryC':'旧票'},
    ]

    for stamp in stamps:
        for category in categories:
            generate_lib_pages (stamp['name'], stamp['nameC'], category['category'], category['categoryC'])

