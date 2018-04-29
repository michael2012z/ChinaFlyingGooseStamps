# -*- coding: utf-8 -*-
import os, time
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from SearchCondition import searchConditions

baseUrl = "https://raw.githubusercontent.com/michael2012z/StampsGallery_CoilingDragon/master/"
siteUrl = "http://michael2012z.github.io/ChinaCoilingDragonStampsGallery/"
for searchCondition in searchConditions:
	faceFiles = []
	imageFiles = os.listdir(searchCondition.folder + "/src")
        imageFiles.sort()
	for imageFile in imageFiles[::-1]:
		if os.path.isfile(searchCondition.folder + "/src/" + imageFile) and os.path.splitext(imageFile)[1] == ".jpg" and os.path.splitext(imageFile)[0].find("A") > 0 and os.path.splitext(imageFile)[0].find("A") == (len(os.path.splitext(imageFile)[0])-1):
			faceFiles.append([searchCondition.folder + "/src" + "/" + imageFile, searchCondition.folder + "/m_size" + "/" + os.path.splitext(imageFile)[0] + ".jpg"]) 

	pageContent = ""	
	pageContent += "<html lang=\"en\"><head><meta http-equiv=\"Content-Type\" content=\"text/html; charset=UTF-8\">\r\n"
	pageContent += "<meta charset=\"utf-8\">"
	pageContent += "<title>" + searchCondition.description + "</title>"
	pageContent += "<body bgcolor=\"black\">"

	pageContent += "<center>\r\n"
	pageContent += "<h1><font color=white size=72>" + searchCondition.description + "</font></h1>"
	count = 0
	for faceFile in faceFiles:
		if count % 4 == 0:
			pageContent += "<div>"
		pageContent += "<a target=\"_blank\" href=\"" + baseUrl
		pageContent += faceFile[0]
		pageContent += "\">"
		pageContent += "<img width=\"280\" src=\"" + baseUrl
		pageContent += faceFile[1]
		pageContent += "\"></a>"
		if count % 4 == 3:
			pageContent += "</div>\r\n"
		count += 1
	if count % 4 <> 0:
			pageContent += "</div>\r\n"
	pageContent += "</center>\r\n"
	pageContent += "</body>"
	pageContent += "</html>"
	f = open("_site/" + searchCondition.folder + ".html", 'w')
	f.write(pageContent)
	f.close()
		# index file
	f = open("_site/" + "index.html", 'w')
	pageContent = ""	
	pageContent += "<html lang=\"en\"><head><meta http-equiv=\"Content-Type\" content=\"text/html; charset=UTF-8\">\r\n"
	pageContent += "<meta charset=\"utf-8\">"
	pageContent += "<title>" + "大清蟠龙邮票画廊" + "</title>"
	pageContent += "<body bgcolor=\"black\">"
	pageContent += "<center>\r\n"
	pageContent += "<br/>"
	pageContent += "<br/>"
	pageContent += "<h1><font color=white size=7>" + "大清蟠龙邮票画廊" + "</font></h1>\r\n"
	pageContent += "<br/>"
	for searchCondition in searchConditions:
		pageContent += "<div>"
		pageContent += "<a target=\"_blank\" href=\"" + siteUrl
		pageContent += searchCondition.folder
		pageContent += ".html" + "\">"
		pageContent += "<h2><font color=white size=6>" + searchCondition.description + "</font></h2>"
		pageContent += "</a>"
		pageContent += "</div>\r\n"
	pageContent += "</center>\r\n"
	pageContent += "</body>"
	pageContent += "</html>"
	f.write(pageContent)
	f.close()
