import math

import rclpy
from geometry_msgs.msg import Twist
from rclpy.node import Node
from turtlesim.msg import Pose


class TurtlePathFollower(Node):
    def __init__(self):
        super().__init__('turtle_path_follower')

        # Publishes movement commands to the turtle
        self.publisher_ = self.create_publisher(
            Twist,
            '/turtle1/cmd_vel',
            10
        )

        # Receives the turtle's current x, y and angle values
        self.subscription = self.create_subscription(
            Pose,
            '/turtle1/pose',
            self.pose_callback,
            10
        )

        # List of coordinates that the turtle will follow in order
        # Keep x and y approximately between 1.0 and 10.0
        self.path = [
            (7.5, 5.5),
            (9.0, 7.5),
            (7.5, 9.0),
            (4.0, 9.0),
            (2.0, 7.0),
            (3.5, 4.0),
            (7.0, 3.0)
        ]
 # Index of the coordinate currently being followed
        self.current_target_index = 0

        # Turtle is considered to have reached a point within this distance
        self.distance_tolerance = 0.15

        # Controller values
        self.linear_gain = 0.8
        self.angular_gain = 4.0

        # Maximum allowed movement speeds
        self.max_linear_speed = 1.5
        self.max_angular_speed = 3.0

        self.finished = False

        self.get_logger().info('Path follower started')
        self.get_logger().info(
            f'First target: {self.path[self.current_target_index]}'
        )
def pose_callback(self, pose):
        """
        Runs automatically whenever a new turtle pose is received.
        It calculates the movement required to reach the current target.
        """

        if self.finished:
            return

        # Get the current target coordinate
        target_x, target_y = self.path[self.current_target_index]

        # Calculate horizontal and vertical distance to target
        error_x = target_x - pose.x
        error_y = target_y - pose.y

        # Calculate direct distance to target coordinate
        distance = math.sqrt(error_x ** 2 + error_y ** 2)

        # Check whether the current coordinate has been reached
        if distance < self.distance_tolerance:
            self.stop()

            self.get_logger().info(
                f'Reached point {self.current_target_index + 1}: '
                f'({target_x}, {target_y})'
            )

            self.current_target_index += 1

            # Check whether all coordinates have been completed
            if self.current_target_index >= len(self.path):
                self.finished = True
                self.get_logger().info('Entire path completed')
                self.stop()
                return

            next_target = self.path[self.current_target_index]
            self.get_logger().info(f'Next target: {next_target}')
            return

        # Calculate the angle from the current position to the target
        target_angle = math.atan2(error_y, error_x)

        # Difference between required angle and current turtle angle
        angle_error = target_angle - pose.theta

        # Keep angle error within -pi to +pi
        angle_error = math.atan2(
            math.sin(angle_error),
            math.cos(angle_error)
        )

        command = Twist()

        # Angular speed controls left/right rotation
        command.angular.z = float(
            max(
                -self.max_angular_speed,
                min(self.max_angular_speed, self.angular_gain * angle_error)
            )
        )

        # If the turtle is facing far away from the target,
        # rotate first before moving forward
        if abs(angle_error) > 0.5:
            command.linear.x = 0.0
        else:
            command.linear.x = float(
                min(self.max_linear_speed, self.linear_gain * distance)
            )

        # Send command to the turtle
        self.publisher_.publish(command)

    def stop(self):
        """Publishes zero velocity to stop the turtle."""
        command = Twist()

        command.linear.x = 0.0
        command.angular.z = 0.0

        self.publisher_.publish(command)


def main(args=None):
    rclpy.init(args=args)

    node = TurtlePathFollower()

    try:
        rclpy.spin(node)

    except KeyboardInterrupt:
        node.get_logger().info('Path follower stopped by user')

    finally:
        node.stop()
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
  
