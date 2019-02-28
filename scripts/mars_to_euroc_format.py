#!/usr/bin/env python3

import os, sys, csv, shutil
from PIL import Image
from progress.spinner import Spinner # pip3 install progress

# Note: additionally you'll need to add a camera sensor yaml file to the
# generated cam0 directory with camera sensor information in the following form:

# # General sensor definitions.
# sensor_type: camera
# comment: VI-Sensor cam0 (MT9M034)
#
# # Sensor extrinsics wrt. the body-frame.
# T_BS:
#   cols: 4
#   rows: 4
#   data: [0.0148655429818, -0.999880929698, 0.00414029679422, -0.0216401454975,
#          0.999557249008, 0.0149672133247, 0.025715529948, -0.064676986768,
#         -0.0257744366974, 0.00375618835797, 0.999660727178, 0.00981073058949,
#          0.0, 0.0, 0.0, 1.0]
#
# # Camera specific definitions.
# rate_hz: 20
# resolution: [752, 480]
# camera_model: pinhole
# intrinsics: [458.654, 457.296, 367.215, 248.375] #fu, fv, cu, cv
# distortion_model: radial-tangential
# distortion_coefficients: [-0.28340811, 0.07395907, 0.00019359, 1.76187114e-05]

# Just create a new sensor.yaml file in the cam0 directory, copy the above
# keys and definitions into the file, and replace these values with your own
# camera sensor specifications.

def printUsage():
    print('Usage: python3 mars_to_euroc_format.py '
        '<mars input> <output dir>')

def printInvalidMarsDirectory():
    print('Error: Invalid MARS directory layout')

def printInvalidDirectory(desc = None):
    msg = 'Error: Invalid directory layout '
    if desc:
        msg += str(desc)
    print(msg)

def convertMARSIMUToEUROC(input_path_to_file, output_path, pi):
    print('\nConverting IMU')
    if not os.path.exists(input_path_to_file):
        printInvalidDirectory(input_path_to_file)
        return False
    csv_output = open(output_path + '/data.csv', 'w', newline='')
    fieldnames = ['#timestamp [ns]',
    'w_RS_S_x [rad s^-1]', 'w_RS_S_y [rad s^-1]', 'w_RS_S_z [rad s^-1]',
    'a_RS_S_x [m s^-2]', 'a_RS_S_y [m s^-2]', 'a_RS_S_z [m s^-2]']
    writer = csv.DictWriter(csv_output, fieldnames = fieldnames)
    writer.writeheader()
    with open(input_path_to_file) as f:
        for row in f:
            row = row.split(' ')
            # timestamp second to nano
            writer.writerow({'#timestamp [ns]' : str(int(float(row[0]) * 1e9)),
            'w_RS_S_x [rad s^-1]' : row[2], 'w_RS_S_y [rad s^-1]' : row[3],
            'w_RS_S_z [rad s^-1]' : row[4], 'a_RS_S_x [m s^-2]' : row[5],
            'a_RS_S_y [m s^-2]' : row[6], 'a_RS_S_z [m s^-2]' : row[7]})
            pi.next()
        f.close()
    csv_output.close()
    print('IMU conversion complete')
    return True

def convertMARSImagestoEUROC(input_path, output_path, pi):
    print('\nConverting Images')
    mars_timestamps_file = input_path + '/timestamps.txt'
    if not os.path.exists(mars_timestamps_file):
        printInvalidMarsDirectory()
        printUsage()
        return False
    euroc_data_dir = output_path + '/data'
    euroc_data_csv_path = output_path + '/data.csv'
    os.mkdir(euroc_data_dir)
    euroc_data_csv_file = open(euroc_data_csv_path, 'w', newline = '')
    fieldnames = ['#timestamp [ns]', 'filename']
    writer = csv.DictWriter(euroc_data_csv_file, fieldnames = fieldnames)
    writer.writeheader()
    with open(mars_timestamps_file) as mtime:
        for row in mtime:
            row = row.split(' ')
            # timestamp second to nano
            image_name, image_timestamp = row[0], str(int(float(row[1]) * 1e9))
            writer.writerow({'#timestamp [ns]' : image_timestamp,
            'filename' : image_timestamp + '.png'})
            mars_image_file = Image.open(input_path + '/' + image_name)
            mars_image_file.save(euroc_data_dir + '/' + image_timestamp + '.png', format='PNG')
            pi.next()
        mtime.close()
    euroc_data_csv_file.close()
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
    mars_input_path = os.path.abspath(argv[1])
    mars_imu_path = mars_input_path + '/mars_imu.txt'
    mars_image_path = mars_input_path + '/images'
    euroc_output_path = os.path.abspath(argv[2]) + '/euroc_format'
    euroc_imu_path = euroc_output_path + '/imu0'
    euroc_cam_path = euroc_output_path + '/cam0'
    if os.path.isdir(euroc_output_path):
        shutil.rmtree(euroc_output_path)
    os.mkdir(euroc_output_path)
    os.mkdir(euroc_imu_path)
    os.mkdir(euroc_cam_path)
    # convert IMU data
    spinner = Spinner()
    imu_conversion_success = convertMARSIMUToEUROC(mars_imu_path, euroc_imu_path, spinner)
    camera_conversion_success = convertMARSImagestoEUROC(mars_image_path, euroc_cam_path, spinner)
    if imu_conversion_success and camera_conversion_success:
        print('Conversion complete. written to ' + euroc_output_path + '\n')
    else:
        print('Error converting euroc dataset')

if __name__ == '__main__':
    argv = sys.argv
    main(argv)
