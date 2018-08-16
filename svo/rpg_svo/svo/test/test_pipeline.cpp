// This file is part of SVO - Semi-direct Visual Odometry.
//
// Copyright (C) 2014 Christian Forster <forster at ifi dot uzh dot ch>
// (Robotics and Perception Group, University of Zurich, Switzerland).
//
// SVO is free software: you can redistribute it and/or modify it under the
// terms of the GNU General Public License as published by the Free Software
// Foundation, either version 3 of the License, or any later version.
//
// SVO is distributed in the hope that it will be useful, but WITHOUT ANY
// WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
// FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
//
// You should have received a copy of the GNU General Public License
// along with this program.  If not, see <http://www.gnu.org/licenses/>.

#include <dirent.h>
#include <vector>
#include <cctype>
#include <svo/config.h>
#include <svo/frame_handler_mono.h>
#include <svo/map.h>
#include <svo/frame.h>
#include <vector>
#include <string>
#include <vikit/math_utils.h>
#include <vikit/vision.h>
#include <vikit/abstract_camera.h>
#include <vikit/atan_camera.h>
#include <vikit/pinhole_camera.h>
#include <opencv2/opencv.hpp>
#include <sophus/se3.h>
#include <iostream>
#include <fstream>
#include "test_utils.h"

namespace svo {

class BenchmarkNode
{
  vk::AbstractCamera* cam_;
  svo::FrameHandlerMono* vo_;

public:
  BenchmarkNode();
  ~BenchmarkNode();
  void runFromFolder();
};

BenchmarkNode::BenchmarkNode()
{
//  cam_ = new vk::PinholeCamera(752, 480, 315.5, 315.5, 376.0, 240.0);
  cam_ = new vk::PinholeCamera(752, 480, 458.654, 457.296, 367.215, 248.375); // mav0
  vo_ = new svo::FrameHandlerMono(cam_);
  vo_->start();
}

BenchmarkNode::~BenchmarkNode()
{
  delete vo_;
  delete cam_;
}

void BenchmarkNode::runFromFolder()
{
    DIR *dir;
    struct dirent *ent;
    std::string dataset_dir("/home/mars/MARS/Datasets/mav0/cam0/data/");
    std::vector<int64_t> image_file_names;
    if ((dir = opendir (dataset_dir.c_str())) != NULL) {
        /* print all the files and directories within directory */
        while ((ent = readdir (dir)) != NULL) {
            std::cout << "ent = " << ent->d_name << std::endl;
            size_t last_index = std::string(ent->d_name).find_last_of(".");
            std::string no_ext = std::string(ent->d_name).substr(0, last_index);
            int64_t no_ext_ll = std::strtoll(no_ext.c_str(), nullptr, 10);
            if (no_ext_ll == 0LL) {
                continue;
            }
            image_file_names.push_back(no_ext_ll);
        }
        closedir (dir);
    } else {
        /* could not open directory */
        std::cout << "directory: " << dataset_dir << " does not exist";
    }

    std::sort(image_file_names.begin(), image_file_names.end());

    std::vector<std::string> full_file_paths;
    for (int64_t d : image_file_names) {
        std::stringstream ss;
        ss << dataset_dir << d << ".png";
        full_file_paths.push_back(ss.str());
    }

    std::ofstream pose_file("/home/mars/MARS/SLAMBenchmarking/output/svo_pose.txt");
    for(unsigned int img_id = 2; img_id < full_file_paths.size() - 1; ++img_id) {
        if(img_id == 2)
            std::cout << "reading image " << img_id << std::endl;
        cv::Mat img(cv::imread(full_file_paths[img_id], 0));
        assert(!img.empty());

        // process frame
        vo_->addImage(img, 0.01*img_id);

        // display tracking quality
        if(vo_->lastFrame() != NULL)
        {
            std::cout << "Frame-Id: " << vo_->lastFrame()->id_ << " \t"
                      << "#Features: " << vo_->lastNumObservations() << " \t"
                      << "Proc. Time: " << vo_->lastProcessingTime()*1000 << "ms \n";

            double timestamp = vo_->lastFrame()->timestamp_;
            Sophus::SE3 T_f_w = vo_->lastFrame()->T_f_w_;
            Eigen::Vector3d t = T_f_w.translation();
            Eigen::Matrix3d R = T_f_w.rotation_matrix();
            pose_file << std::setprecision(16) << timestamp << " " <<
              R(0,0) << " " << R(0,1) << " " << R(0,2) << " " <<
              R(1,0) << " " << R(1,1) << " " << R(1,2) << " " <<
              R(2,0) << " " << R(2,1) << " " << R(2,2) << " " <<
              t(0) << " " << t(1) << " " << t(2) << std::endl;
        }
    }
    pose_file.close();
}

} // namespace svo

int main(int argc, char** argv)
{
  {
    svo::BenchmarkNode benchmark;
    benchmark.runFromFolder();
  }
  printf("BenchmarkNode finished.\n");
  return 0;
}

