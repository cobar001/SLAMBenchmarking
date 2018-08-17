#!/usr/bin/env python3

# export SLAM_BM=<path to slam_bm dir>

import os, sys

def printUsage():
    print('Usage: python3 build_slam_code.py '
        '<package>')
    print('Package options:')
    print('okvis\nsvo\nrovio\nvins-mono\ncatkin_ws\norb-slam\nall')

def printStatus(package):
    print('\n')
    print('*'*20)
    print('Building '+package)
    print('*'*20)
    print('\n')

def build_okvis(slam):
    okvis_dir = slam + '/okvis'
    if not os.path.isdir(okvis_dir):
        print('Error recognizing okvis directory')
        exit()
    #build okvis
    printStatus('okvis')
    os.chdir(okvis_dir)
    if not os.path.isdir(okvis_dir + '/build'):
        os.mkdir(okvis_dir + '/build')
    os.chdir(okvis_dir + '/build')
    os.system('cmake ..')
    os.system('make')
    print('\nokvis build finished')

def build_svo(slam):
    svo_vikit_dir = slam + '/svo/rpg_vikit/vikit_common/'
    svo_dir = slam + '/svo/rpg_svo/svo/'

    if not os.path.isdir(svo_vikit_dir) or not os.path.isdir(svo_dir):
        print('Error recognizing svo_vikit or svo directory')
        exit()
    # build vikit
    printStatus('svo_vikit')
    os.chdir(svo_vikit_dir)
    if not os.path.isdir(svo_vikit_dir + "/build"):
        os.mkdir(svo_vikit_dir + '/build')
    os.chdir(svo_vikit_dir + '/build')
    os.system('cmake ..')
    os.system('make')
    print("\nsvo_vikit build finished")
    # build svo
    printStatus("svo")
    os.chdir(svo_dir)
    if not os.path.isdir(svo_dir + '/build'):
        os.mkdir(svo_dir + '/build')
    os.chdir(svo_dir + '/build')
    os.system('cmake ..')
    os.system('make')
    print('\nsvo build finished')

def catkin_make(catkin_ws, package):
    if not os.path.isdir(catkin_ws):
        print('Error recognizing catkin_ws directory')
        exit()
    os.chdir(catkin_ws)
    os.system('catkin_make --pkg '+package)

def build_rovio(slam):
    catkin_ws = slam + '/catkin_ws'
    catkin_make(catkin_ws, "rovio")

def build_VINSMono(slam):
    catkin_ws = slam + '/catkin_ws'
    catkin_make(catkin_ws, "vins_estimator")

def build_orbslam(slam):
    orb_slam_dir = slam + '/ORB_SLAM2'
    if not os.path.isdir(orb_slam_dir):
        print('Error recognizing ORB_SLAM2 directory')
        exit()
    #build orb slam
    printStatus("orb slam")
    os.chdir(orb_slam_dir)
    # if not os.path.isdir(orb_slam_dir + '/build'):
    #     os.mkdir('build')
    # os.chdir(orb_slam_dir + '/build')
    os.system('chmod +x build.sh')
    os.system('./build.sh')
    print('\norb slam build finished')

def build_all(slam):
    printStatus('All')
    build_okvis(slam)
    build_svo(slam)
    build_rovio(slam)
    build_VINSMono(slam)
    build_orbslam(slam)

def main(argv):
    slam_dir = os.environ['SLAM_BM']
    packages_to_build = argv
    if len(packages_to_build) == 0:
        printUsage()
    if not os.path.isdir(slam_dir + '/output'):
        os.mkdir(slam_dir + '/output')
    for p in packages_to_build:
        if 'okvis' in p:
            build_okvis(slam_dir)
        elif 'svo' in p:
            build_svo(slam_dir)
        elif 'rovio' in p:
            build_rovio(slam_dir)
        elif 'vins-mono' in p:
            build_VINSMono(slam_dir)
        elif 'orb-slam' in p:
            build_orbslam(slam_dir)
        elif 'all' in p:
            build_all(slam_dir)
        else:
            printUsage()

if __name__ == '__main__':
    argv = sys.argv
    main(argv)