import time

import rclpy
from geometry_msgs.msg import Twist
from rclpy.node import Node


class SimpleRobotMotion(Node):
    def __init__(self):
        super().__init__('simple_robot_motion')
        self.publisher_ = self.create_publisher(
            Twist,
            '/turtle1/cmd_vel',
            10
        )

    def move_for(self, linear_speed, angular_speed, duration, action):
        command = Twist()
        command.linear.x = linear_speed
        command.angular.z = angular_speed

        self.get_logger().info(f'{action} for {duration} seconds')

        start_time = time.time()

        while rclpy.ok() and time.time() - start_time < duration:
            self.publisher_.publish(command)
            time.sleep(0.1)

        self.stop()

    def stop(self):
        command = Twist()
        self.publisher_.publish(command)
        time.sleep(0.2)


def main(args=None):
    rclpy.init(args=args)
    node = SimpleRobotMotion()

    try:
        node.move_for(1.0, 0.0, 4, 'Moving straight')
        node.move_for(1.0, 1.0, 4, 'Turning left')
        node.move_for(1.0, -1.0, 5, 'Turning right')
        node.get_logger().info('Movement completed')

    except KeyboardInterrupt:
        node.get_logger().info('Stopped by user')

    finally:
        node.stop()
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
