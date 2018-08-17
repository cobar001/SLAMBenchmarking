#!/usr/bin/env python3

import os, sys, csv
from PIL import Image

def printUsage():
    print('Usage: python3 euroc_to_mars_format.py '
        '<euroc input dir> <output dir>')

def printInvalidEurocDirectory():
    print('Error: Invalid Euroc directory layout')

def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█'):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end = '\r')
    # Print New Line on Complete
    if iteration == total:
        print()

def convertIMU(euroc_path, output_path):
    print('\nConverting IMU')
    imu_csv_path = euroc_path + '/imu0/data.csv'
    if not os.path.exists(imu_csv_path):
        printInvalidEurocDirectory()
        printUsage()
        return False
    imu_output = open(output_path+'/mars_imu.txt', 'wt')
    with open(imu_csv_path) as icp:
        f_csv = csv.reader(icp)
        headers = next(f_csv) # skip header line
        for row in f_csv:
            # timestamp nano -> micro
            imu_output.write(str(int(float(row[0]) / 1000)) + ' 0 ' +\
                ' '.join(row[1:4]) + ' 0 ' + ' '.join(row[4:7]) + ' 0 0 0 \n')
        icp.close()
    imu_output.close()
    print('IMU conversion complete')
    return True

def convertImages(euroc_path, output_path):
    print('\nConverting Images')
    cam0_csv_path = euroc_path + '/cam0/data.csv'
    cam0_images_path = euroc_path + '/cam0/data'
    if not os.path.exists(cam0_csv_path) or not os.path.isdir(cam0_images_path):
        printInvalidEurocDirectory()
        printUsage()
        return False
    images_output_dir = output_path + '/images'
    if not os.path.isdir(images_output_dir):
        os.mkdir(images_output_dir)
    # create timestamps file
    camera_timestamp_output = open(images_output_dir + '/timestamps.txt', 'wt')
    with open(cam0_csv_path) as ccp:
        f_csv = csv.reader(ccp)
        headers = next(f_csv) # skip header line
        for index, row in enumerate(f_csv):
            # timestamp nano -> micro
            camera_timestamp_output.write('m' + format(index, '0>7') \
            + '.pgm ' + str(int(float(row[0]) / 1000)) + '\n')
        ccp.close()
    camera_timestamp_output.close()
    # png -> pgm
    cam0_images_paths = sorted(os.listdir(cam0_images_path))
    printProgressBar(0, len(cam0_images_paths), prefix = 'Progress:', \
        suffix = 'Complete', length = 40)
    for index, image in enumerate(cam0_images_paths):
        full_path = cam0_images_path + '/' + image
        png_image = Image.open(full_path)
        png_image.save(images_output_dir + \
            '/m' + format(index, '0>7') + '.pgm ', format='PPM')
        printProgressBar(index, len(cam0_images_paths), prefix = 'Progress:', \
            suffix = 'Complete', length = 40)
    print('\nImage conversion complete')
    return True

def main(args):
    print('main')
    if len(args) != 3:
        print('Error: Invalid number of arguments')
        printUsage()
        return
    elif not os.path.isdir(argv[1]) or not os.path.isdir(argv[2]):
        print('Error: Invalid inputs. Make sure directories exist already.')
        printUsage()
        return
    euroc_path = os.path.abspath(argv[1])
    output_path = os.path.abspath(argv[2]) + '/mars_format'
    if not os.path.isdir(output_path):
        os.mkdir(output_path)
    print(euroc_path)
    print(output_path)
    # convert IMU data
    imu_conversion_success = convertIMU(euroc_path, output_path)
    camera_conversion_success = convertImages(euroc_path, output_path)
    if imu_conversion_success and camera_conversion_success:
        print('Conversion complete. written to ' + output_path + '\n')
    else:
        print('Error converting euroc dataset')

if __name__ == '__main__':
    argv = sys.argv
    main(argv)
