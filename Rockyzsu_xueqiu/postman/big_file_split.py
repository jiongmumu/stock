# -*-coding=utf-8-*-
import sys

__author__ = 'Rocky'
'''
http://30daydo.com
Email: weigesysu@qq.com
'''

def split_file(filename,part):
    with open(filename,'r') as f:
        content = f.readlines()

    l = len(content)
    name = filename.split('.')
    prefix_filename, postfix_filename = name[0],name[1]
    part_size = l/part
    for i in range(part):
        temp = content[i*part_size:(i+1)*part_size]
        f = open('{}_{}.{}'.format(prefix_filename,i,postfix_filename),'w')
        for s in temp:
            f.write(s)
        f.close()
    i=i+1
    f = open('{}_{}.{}'.format(prefix_filename, i, postfix_filename), 'w')
    for s in content[i*part_size:]:
        f.write(s)
    f.close()

def main():
    split_file(sys.argv[1],int(sys.argv[2]))
    # split_file()

if __name__ == '__main__':
    main()