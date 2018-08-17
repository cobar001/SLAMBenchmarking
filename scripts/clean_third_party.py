#!/usr/bin/env python3

# export SLAM_BM=<path to slam_bm dir>

import os, sys, shutil

def printStatus(path):
	print('\n')
	print('*'*20)
	print('Cleaning '+path.split('/')[-1])
	print('*'*20)
	print('\n')

def main(argv):
	slam_dir = os.environ['SLAM_BM']
	third_party_dir = slam_dir+'/third-party'
	if not os.path.isdir(third_party_dir):
		print('Error recognizing slam directory')
		return

	#clean kindr
	kindr_path = third_party_dir+'/kindr'
	if not os.path.isdir(kindr_path):
		print('Error: Kindr not found')
		return
	if not os.path.isdir(kindr_path+'/build'):
		print("Kindr not built")
	else:
		printStatus(kindr_path)
		os.chdir(kindr_path)
		shutil.rmtree(kindr_path+'/build')
		print("Kindr clean success")

	#clean sophus
	sophus_path = third_party_dir+'/Sophus'
	if not os.path.isdir(sophus_path):
		print('Error: Sophus not found')
		return
    printStatus(sophus_path)
	if os.path.isdir(sophus_path+'/build'):
		print("Sophus not built")
        os.chdir(sophus_path)
        shutil.rmtree(sophus_path + '/build')
	if os.path.isdir(sophus_path+'/cmake-debug-build'):
        os.chdir(sophus_path)
        shutil.rmtree(sophus_path + '/cmake-debug-build')
	print("Sophus clean success")

	#clean fast
	fast_path = third_party_dir+'/fast'
	if not os.path.isdir(fast_path):
		print('Error: fast not found')
		return
	if not os.path.isdir(fast_path+'/build'):
		print("fast not built")
	else:
		printStatus(fast_path)
		os.chdir(fast_path)
		shutil.rmtree(fast_path+'/build')
		print("fast clean success")

	#clean g2o
	g2o_path = third_party_dir+'/g2o-20160424_git'
	if not os.path.isdir(g2o_path):
		print('Error: g2o not found')
		return
	if not os.path.isdir(g2o_path+'/build'):
		print("g2o not built")
	else:
		printStatus(g2o_path)
		os.chdir(g2o_path)
		shutil.rmtree(g2o_path+'/build')
		shutil.rmtree(g2o_path+'/bin')
		print("g2o clean success")

	#clean ceres-solver
	ceres_path = third_party_dir+'/ceres-solver'
	if not os.path.isdir(ceres_path):
		print('Error: ceres not found')
		return
	if not os.path.isdir(ceres_path+'/build'):
		print("ceres not built")
	else:
		printStatus(ceres_path)
		os.chdir(ceres_path)
		shutil.rmtree(ceres_path+'/build')
		print("ceres clean success")

	# clean pangolin
	pangolin_path = third_party_dir + '/Pangolin'
	if not os.path.isdir(pangolin_path):
		print('Error: pangolin not found')
		return
	if not os.path.isdir(pangolin_path + '/build'):
		print("pangolin not built")
	else:
		printStatus(pangolin_path)
		os.chdir(pangolin_path)
		shutil.rmtree(pangolin_path + '/build')
		print("pangolin clean success")

	print("\nthird-party complete\n")

if __name__ == '__main__':
    argv = sys.argv
    main(argv)