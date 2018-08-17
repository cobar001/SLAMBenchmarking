#!/usr/bin/env python3

# export SLAM_BM=<path to slam_bm dir>

import os, sys, shutil

def printUsage():
    print('Usage: python3 clean_slam_code.py '
        '<package>')
    print('Package options:')
    print('okvis\nsvo\nrovio\nvins-mono\ncatkin_ws\norb-slam\nall')

def printStatus(package):
	print('*'*20)
	print('Cleaning '+package)
	print('*'*20)

def clean_okvis(slam):
    okvis_dir = slam + '/okvis'
    if not os.path.isdir(okvis_dir):
        print('Error recognizing okvis directory')
        exit()
    #clean okvis
    printStatus("okvis")
    os.chdir(okvis_dir)
    if os.path.isdir("build"):
        shutil.rmtree("build")
    if os.path.isdir('cmake-build-debug'):
        shutil.rmtree("cmake-build-debug")
    print("okvis clean finished")

def clean_svo(slam):
    svo_vikit_dir = slam + '/svo/rpg_vikit/vikit_common/'
    svo_dir = slam + '/svo/rpg_svo/svo/'

    if not os.path.isdir(svo_vikit_dir) or not os.path.isdir(svo_dir):
        print('Error recognizing svo_vikit or svo directory')
        exit()

    # clean vikit
    printStatus("svo_vikit")
    os.chdir(svo_vikit_dir)
    if os.path.isdir("build"):
        shutil.rmtree('build')
        shutil.rmtree('bin')
        shutil.rmtree('lib')
        print("svo_vikit clean finished")
    else:
        print("svo_vikit not built")

    # clean svo
    printStatus("svo")
    os.chdir(svo_dir)
    if os.path.isdir("build"):
        shutil.rmtree('build')
        shutil.rmtree('bin')
        shutil.rmtree('lib')
        print("svo clean finished")
    else:
        print("svo not built")

def catkin_clean(slam):
    catkin_ws = slam + '/catkin_ws'
    printStatus('catkin_ws')
    if not os.path.isdir(catkin_ws):
        print('Error recognizing catkin_ws directory')
        exit()
    os.chdir(catkin_ws)
    if os.path.isdir('build') and os.path.isdir('devel'):
        shutil.rmtree('build')
        shutil.rmtree('devel')
        print('catkin_ws clean finished')
    else:
        print('No catkin packages built (rovio/vins-mono)')

def clean_rovio(slam):
    rovio_catkin_ws = slam + '/catkin_ws/build/rovio'
    printStatus('rovio')
    if os.path.isdir(rovio_catkin_ws):
        shutil.rmtree(rovio_catkin_ws)
        print('rovio clean finished')
    else:
        print('rovio not built')

def clean_vinsmono(slam):
    vins_mono_catkin_ws = slam + '/catkin_ws/build/VINS-Mono'
    printStatus('vins-mono')
    if os.path.isdir(vins_mono_catkin_ws):
        shutil.rmtree(vins_mono_catkin_ws)
        print('vins-mono clean finished')
    else:
        print('vins-mono not built')

def clean_orbslam(slam):
    orb_slam_dir = slam + '/ORB_SLAM2'
    if not os.path.isdir(orb_slam_dir):
        print('Error recognizing ORB_SLAM2 directory')
        exit()
    #clean orb slam
    printStatus("orb slam")
    os.chdir(orb_slam_dir)
    if not os.path.isdir("build"):
        print("okvis not built")
        return
    shutil.rmtree("build")
    shutil.rmtree("lib")
    print("orb slam clean finished")

def clean_all(slam):
    printStatus('All')
    clean_okvis(slam)
    clean_svo(slam)
    clean_orbslam(slam)
    catkin_clean(slam)

def main(argv):
    slam_dir = os.environ['SLAM_BM']
    packages_to_build = argv
    if len(packages_to_build) == 0:
        printUsage()
    for p in packages_to_build:
        if 'okvis' in p:
            clean_okvis(slam_dir)
        elif 'svo' in p:
            clean_svo(slam_dir)
        elif 'rovio' in p:
            clean_rovio(slam_dir)
        elif 'vins-mono' in p:
            clean_vinsmono(slam_dir)
        elif 'catkin_ws' in p:
            catkin_clean(slam_dir)
        elif 'orb-slam' in p:
            clean_orbslam(slam_dir)
        elif 'all' in p:
            clean_all(slam_dir)
        else:
            printUsage()

if __name__ == '__main__':
    argv = sys.argv
    main(argv)