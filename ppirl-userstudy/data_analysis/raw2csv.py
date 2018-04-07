import sys


def main(filename, filename2):
    filein = open(filename, 'r')
    fileout = open(filename2+'.csv', 'w+')

    fileout.write('uid,type,value,timestamp,extra\n')

    i = 0
    for line in filein:
        i += 1
        if line and line != '\n':
            item_list = line.split(';')
            for item in item_list:
                if item and item.strip() != '\n':
                    item_dict = dict()
                    kv_list = item.split(',')
                    if len(kv_list) < 2:
                        continue
                    for kv in kv_list:
                        if len(kv.split(':')) < 2:
                            continue
                        k = kv.split(':')[0]
                        v = kv.split(':')[1]
                        item_dict[k] = v
                    if 'uid' not in item_dict or 'type' not in item_dict \
                        or 'value' not in item_dict or 'timestamp' not in item_dict:
                        continue
                    output = item_dict['uid'] + ',' + item_dict['type'] + \
                     ',' + item_dict['value'] + ',' + item_dict['timestamp'] + ','
                    first_flag = True
                    for key in sorted(item_dict):
                        if key not in ['uid', 'type', 'value', 'timestamp']:
                            if first_flag:
                                output += (key + ':' + item_dict[key])
                                first_flag = False
                            else:
                                output += ('|' + key + ':' + item_dict[key])
                    if output:
                        fileout.write(output)
                        fileout.write('\n')

    filein.close()
    fileout.close()


if __name__ == '__main__':
    filename = sys.argv[1]
    fileoutname = sys.argv[2]
    main(filename, fileoutname)
