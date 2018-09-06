# -*- coding: utf-8 -*-

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
            print "[comments:]" + line[1:]
        elif line[0] == "%":
            # this line is new stamp index
            stampID = line[1:]
            stampID = int(stampID)
            record["id"] = stampID
            print "stamp: " + str(stampID)
        elif line[0] == "#":
            # this line is flaw 
            coord = line[1:].split("|")[0]
            desc = line[1:].split("|")[-1]
            if coord.find("-") >= 0:
                # this is a line:
                x1, y1 = coord.split("-")[0].split(",")[0], coord.split("-")[0].split(",")[1]
                x2, y2 = coord.split("-")[1].split(",")[0], coord.split("-")[1].split(",")[1]
                x1, y1, x2, y2 = float(x1),float(y1),float(x2), float(y2)
                flawList.append({"type":"dot", "x1":x1, "y1":y1, "x2":x2, "y2":y2, "desc" : desc})
                print "line: " + str([x1, y1, x2, y2]) + ": " + desc
            else:
                # this is a dot
                x, y = coord.split(",")[0], coord.split(",")[1]
                x, y = float(x), float(y)
                flawList.append({"type":"line", "x":x, "y":y, "desc": desc})
                print "dot: " + str([x, y]) + ": " + desc
        elif line[0] == "&":
            # this line is text
            print "[text]: " + line
        else:
            print "[unknown]: " + line

    f.close()

    return allRecords

if __name__ == '__main__':
    allRecords = parse_statistics('../flaw/statistic/statistic_1d.txt')
    print "======================================================="
    print allRecords
    
