

file_prefix = 'section1_'
unique_data = set()
for i in range(1, 11):
    filename = file_prefix + str(i) + '.csv'
    filein = open(filename)
    for line in filein:
        line = ','.join(line.split(',')[1:])
        unique_data.add(line)
    filein.close()

file_prefix2 = 'section2_'
for i in range(1, 11):
    filename = file_prefix2 + str(i) + '.csv'
    filein = open(filename)
    for line in filein:
        line = ','.join(line.split(',')[1:])
        unique_data.add(line)
    filein.close()

fileout = open('main_section_full.csv', 'w+')
idx = 1
for data in unique_data:
    data = str(idx) + ',' + data
    idx += 1
    if data[-1] != '\n':
        data = data + '\n'
    fileout.write(data)
fileout.close()
