/**
 * @file square_mecanum_controller.cpp
 * @brief Controls a mecanum wheeled robot to move in a square pattern
 *
 * This program creates a ROS 2 node that publishes velocity commands to make a
 * mecanum wheeled robot move in a square pattern. It takes advantage of the
 * omnidirectional capabilities of mecanum wheels to move in straight lines
 * along both X and Y axes.
 *
 * Publishing Topics:
 *     /mecanum_drive_controller/cmd_vel (geometry_msgs/TwistStamped):
 *         Velocity commands for the robot's motion
 *
 * @author Addison Sears-Collins
 * @date November 22, 2024
 */

#include <chrono>
#include <functional>
#include <memory>
#include "rclcpp/rclcpp.hpp"
#include "geometry_msgs/msg/twist_stamped.hpp"

using namespace std::chrono_literals;

class ForwardBackwardController : public rclcpp::Node
{
public:
    ForwardBackwardController() : Node("forward_backward_controller")
    {
        publisher_ = this->create_publisher<geometry_msgs::msg::TwistStamped>(
            "/mecanum_drive_controller/cmd_vel", 10);

        timer_ = this->create_wall_timer(
            200ms, std::bind(&ForwardBackwardController::timer_callback, this));

        current_state_ = 0;  // 0 = forward, 1 = backward
        elapsed_time_ = 0.0;

        robot_speed_ = 0.3;
        distance_ = 2.0;

        time_to_move_ = distance_ / robot_speed_;
    }

    ~ForwardBackwardController()
    {
        stop_robot();
    }

    void stop_robot()
    {
        auto msg = geometry_msgs::msg::TwistStamped();
        msg.header.stamp = this->now();
        publisher_->publish(msg);
    }

private:
    void timer_callback()
    {
        auto msg = geometry_msgs::msg::TwistStamped();
        msg.header.stamp = this->now();

        // Forward and backward only
        if (current_state_ == 0) {
            msg.twist.linear.x = robot_speed_;   // forward
        } else {
            msg.twist.linear.x = -robot_speed_;  // backward
        }

        publisher_->publish(msg);

        elapsed_time_ += 0.2;

        if (elapsed_time_ >= time_to_move_) {
            elapsed_time_ = 0.0;
            current_state_ = 1 - current_state_;  // toggle 0 ↔ 1
        }
    }

    rclcpp::TimerBase::SharedPtr timer_;
    rclcpp::Publisher<geometry_msgs::msg::TwistStamped>::SharedPtr publisher_;

    int current_state_;
    double elapsed_time_;
    double robot_speed_;
    double distance_;
    double time_to_move_;
};

int main(int argc, char * argv[])
{
    rclcpp::init(argc, argv);
    auto node = std::make_shared<ForwardBackwardController>();
    rclcpp::spin(node);
    rclcpp::shutdown();
    return 0;
}