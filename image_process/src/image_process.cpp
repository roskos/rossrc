/*
#include <ros/ros.h>
#include <image_transport/image_transport.h>
#include <cv_bridge/cv_bridge.h>
#include <sensor_msgs/image_encodings.h>
#include <opencv2/imgproc/imgproc.hpp>
#include <opencv2/highgui/highgui.hpp>

cv::Mat image;
ros::NodeHandle nh("~");

void imageCallback(const sensor_msgs::ImageConstPtr& msg)
{
        try {
                image = cv_bridge::toCvCopy(msg, sensor_msgs::image_encodings::TYPE_32FC1)->image;
                // 画像の幅を表示する
                std::cout << "width: " << image.cols << std::endl;
                // 画像の高さを表示する
                std::cout << "height: " << image.rows << std::endl;
                // 画像の高さを表示する
                std::cout << "depth: " << image.at<float>(image.rows/2, image.cols/2) << std::endl;
    }
        catch (cv_bridge::Exception& e) {
                ROS_ERROR("cv_bridge exception: %s", e.what());
        }

        cv::imshow("image", image);
        cv::waitKey(1);
}

int main(int argc, char** argv)
{
        ros::init (argc, argv, "img_subscriber");
        ros::NodeHandle nh("~");

        image_transport::ImageTransport it(nh);
        image_transport::Subscriber image_sub = it.subscribe("/zed/depth/depth_registered", 1, imageCallback);

        ros::spin();

        return 0;
}
*/

#include <ros/ros.h>
#include <cv_bridge/cv_bridge.h>
#include <image_transport/image_transport.h>
#include <opencv2/core.hpp>
#include <opencv2/highgui.hpp>

cv::Mat image;

void imageCallback(const sensor_msgs::ImageConstPtr& msg)
{
        try {
        image = cv_bridge::toCvCopy(msg, sensor_msgs::image_encodings::TYPE_32FC1)->image;
        // 画像の幅を表示する
        std::cout << "width: " << image.cols << std::endl;
        // 画像の高さを表示する
        std::cout << "height: " << image.rows << std::endl;
        // 画像の高さを表示する
        std::cout << "depth: " << image.at<float>(image.rows/2, image.cols/2) << std::endl;
        }
        catch (cv_bridge::Exception& e) {
                ROS_ERROR("cv_bridge exception: %s", e.what());
        }

        cv::imshow("image", image);
        cv::waitKey(1);
}

int main(int argc, char** argv)
{
        ros::init (argc, argv, "img_subscriber");
        ros::NodeHandle nh("~");

        image_transport::ImageTransport it(nh);
        image_transport::Subscriber image_sub = it.subscribe("/zed/depth/depth_registered", 1, imageCallback);

        ros::spin();

        return 0;
}
