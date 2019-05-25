
f = open('statistic_1d.txt')
lines = f.readlines()
f.close()

comments = []
records = []
ln = 0
folder = ''

for line in lines:
    ln += 1
    line = line.strip()
    if line <> "":
        if line[0] == '$':
            comments.append(line)
        elif line[0] == '%':
            folder = line[2:]
            records = []
        elif line[0] == '#':
            records.append(line)
        else:
            print("error: line " + str(ln))
    else:
        if folder <> '' and records <> []:
            fn = '%02d/data.txt' % (int(folder))
            f = open(fn, 'w')
            fcontent = '\n'.join(comments)
            fcontent += '\n'
            fcontent += '\n'
            fcontent += '\n'.join(records)
            fcontent += '\n'
            fcontent += '\n'
            #print(folder, ": ", fcontent)
            f.write(fcontent)
            f.close()
            
