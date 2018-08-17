#!/usr/bin/env python3

import os, sys, csv
import numpy as np
import quaternion

def printUsage():
    print('Usage: python3 parse_output.py '
        '<package> <pose_file>')

def parse_okvis(slam_dir, file_path):
    # okvis file format: t, R00, R01, ... px,py,pz,
    print(file_path)
    parsed_okvis_path = slam_dir+'/output/parsed_okvis_pose.txt'
    parsed_okvis_file = open(parsed_okvis_path, 'wt')
    with open(file_path) as f:
        for line in f:
            line = line.split(' ')
            timestamp = line[0]
            rot_mat_raw = np.array([line[1:4], line[4:7], line[7:10]])
            rot_mat_float = rot_mat_raw.astype(np.float)
            quat_float = quaternion.from_rotation_matrix(rot_mat_float)
            write_line = timestamp + ' ' + \
                         str(quaternion[0]) + ' ' + str(quaternion[1]) + ' ' + str(quaternion[2]) + ' ' + \
                         str(quaternion[3]) + ' ' + line[10] + ' ' + line[11] + ' ' + line[12]

            print(quat)
    f.close()
    parsed_okvis_file.close()
    print('okvis pose parsed')
    print('file in: '+parsed_okvis_path)

def main(argv):
    if len(argv) != 3:
        printUsage()
        return
    slam_dir = os.environ['SLAM_BM']
    package = argv[1]
    file_path = os.path.abspath(argv[2])
    if not os.path.isfile(file_path):
        print('Error: file DNE')
        printUsage()
        return
    if not os.path.isdir(slam_dir+'/output'):
        os.mkdir(slam_dir+'/output')
    if 'okvis' in package:
        parse_okvis(slam_dir, file_path)
    elif 'svo' in package:
        print('svo')
    else:
        print('Error: package not recognized')
        printUsage()
        return

if __name__ == '__main__':
    argv = sys.argv
    main(argv)