#!/usr/bin/env python3

# export SLAM_BM=<path to slam_bm dir>

import os, sys

def printStatus(path):
	print('\n')
	print('*'*20)
	print('Installing '+path.split('/')[-1])
	print('*'*20)
	print('\n')

def main(argv):
	slam_dir = os.environ['SLAM_BM']
	third_party_dir = slam_dir+'/third-party'
	if not os.path.isdir(third_party_dir):
		print('Error recognizing slam directory')
		return

	#install kindr
	kindr_path = third_party_dir+'/kindr'
	if not os.path.isdir(kindr_path):
		print('Error: Kindr not found')
		return
	if not os.path.isdir(kindr_path+'/build'):
		printStatus(kindr_path)
		os.chdir(kindr_path)
		os.mkdir('build')
		os.chdir(kindr_path+'/build')
		os.system('cmake ..')
		os.system('sudo make install')
		print("\nKindr install finished")
	else:
		print("Kindr already built")

	#init lwf
	rovio_dir = slam_dir+'/catkin_ws/src/rovio'
	if not os.path.isdir(kindr_path):
		print('Error: rovio not found')
		return
	printStatus('lwf')
	os.chdir(rovio_dir)
	os.system('git submodule update --init --recursive')
	print("\nlwf install finished")

	#install sophus
	sophus_path = third_party_dir+'/Sophus'
	if not os.path.isdir(sophus_path):
		print('Error: Sophus not found')
		return
	if not os.path.isdir(sophus_path+'/build'):
		printStatus(sophus_path)
		os.chdir(sophus_path)
		os.mkdir('build')
		os.chdir(sophus_path+'/build')
		os.system('cmake ..')
		os.system('make -j4')
		print("\nSophus install finished")
	else:
		print("Sophus already built")

	#install fast
	fast_path = third_party_dir+'/fast'
	if not os.path.isdir(fast_path):
		print('Error: fast not found')
		return
	if not os.path.isdir(fast_path+'/build'):
		printStatus(fast_path)
		os.chdir(fast_path)
		os.mkdir('build')
		os.chdir(fast_path+'/build')
		os.system('cmake ..')
		os.system('make -j4')
		print("\nfast install finished")
	else:
		print("fast already built")

	#install g2o
	g2o_path = third_party_dir+'/g2o-20160424_git'
	if not os.path.isdir(g2o_path):
		print('Error: g2o not found')
		return
	if not os.path.isdir(g2o_path+'/build'):
		printStatus(g2o_path)
		os.chdir(g2o_path)
		os.mkdir('build')
		os.chdir(g2o_path+'/build')
		os.system('cmake ..')
		os.system('make -j4')
		os.system('sudo make install')
		print("\ng2o install finished")
	else:
		print("g2o already built")

	#install ceres
	ceres_path = third_party_dir+'/ceres-solver'
	if not os.path.isdir(ceres_path):
		print('Error: ceres-solver not found')
		return
	if not os.path.isdir(ceres_path+'/build'):
		printStatus(ceres_path)
		os.chdir(ceres_path)
		os.mkdir('build')
		os.chdir(ceres_path+'/build')
		os.system('cmake ..')
		os.system('make -j4')
		#os.system('make test')
		os.system('sudo make install')
		print("\nceres-solver install finished")
	else:
		print("ceres-solver already built")

	#install Pangolin
	pangolin_path = third_party_dir+'/Pangolin'
	if not os.path.isdir(pangolin_path):
		print('Error: Pangolin not found')
		return
	if not os.path.isdir(pangolin_path+'/build'):
		printStatus(pangolin_path)
		os.chdir(pangolin_path)
		os.mkdir('build')
		os.chdir(pangolin_path+'/build')
		os.system('cmake ..')
		os.system('cmake --build .')
		print("\nPangolin install finished")
	else:
		print("Pangolin already built")

	print('\nFinished installing third party packages\n')

if __name__ == '__main__':
    argv = sys.argv
    main(argv)