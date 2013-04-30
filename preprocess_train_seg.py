#!/usr/bin/python
# -*- coding: utf-8 -*-

def add_start_end(file_name):
    f = file(file_name)
    lines = f.readlines()
    f.close()
    for i in range(len(lines)):
        lines[i] = 's  ' + lines[i][0:-2] + ' e ' + lines[i][-1]
    p_file = file('p_train_seg.txt', 'w')
    p_file.writelines(lines)
    p_file.close()

if __name__ == '__main__':
    add_start_end('train_seg.txt')
