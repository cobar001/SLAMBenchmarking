#!/usr/bin/env python3

import os, sys, csv

def printUsage():
    print('Usage: python3 parse_euroc_gt.py '
        '<path ot euroc ground truth data.csv file>')

def parseEurocGT(slam, gt_path):
    output_dir = slam + '/output'
    if not os.path.isdir(output_dir):
        print('Error: output directory does not exist:')
        print(output_dir)
    output_dirpath = slam + '/output'
    output_file = open(output_dirpath + '/parsed_euroc_gt.txt', 'wt')
    with open(gt_path) as icp:
        f_csv = csv.reader(icp)
        headers = next(f_csv) # skip header line
        for row in f_csv:
            # timestamp <t> <p> <q>
            output_file.write(row[0][:16] + ' ' +\
                ' '.join(row[1:4]) + ' ' + ' '.join(row[4:8]) + '\n')
        icp.close()
    output_file.close()
    print('Finished parsing EuRoC GT file')

def main(argv):
    if len(argv) != 2:
        print('Error: Invalid arguments')
        printUsage()
        return
    slam_dir = os.environ['SLAM_BM']
    gt_filepath = os.path.abspath(argv[1])
    parseEurocGT(slam_dir, gt_filepath)


if __name__ == '__main__':
    argv = sys.argv
    main(argv)