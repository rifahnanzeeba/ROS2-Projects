This ROS 2 Python program creates a node named simple_robot_motion that controls a turtlesim turtle through the /turtle1/cmd_vel topic. It publishes Twist velocity commands to move the turtle straight, curve left, and curve right for specified durations. The code converts velocity values to floating-point numbers to prevent ROS message type errors, stops the turtle after each movement, and safely shuts down the node when execution finishes or is manually interrupted.


| Code Line / Section                                                  | Description                                                                                                        |
| -------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------ |
| `import time`                                                        | Imports Python’s time module to measure movement duration and add short delays between published commands.         |
| `import rclpy`                                                       | Imports the ROS 2 Python client library required to initialize, run, and shut down a ROS 2 node.                   |
| `from geometry_msgs.msg import Twist`                                | Imports the `Twist` message type, which is used to send linear and angular velocity commands to the turtle.        |
| `from rclpy.node import Node`                                        | Imports the ROS 2 `Node` class so that the program can create a custom node.                                       |
| `class SimpleRobotMotion(Node):`                                     | Defines a ROS 2 node class responsible for controlling the turtle’s movement.                                      |
| `def __init__(self):`                                                | Defines the constructor method that runs when an object of the class is created.                                   |
| `super().__init__('simple_robot_motion')`                            | Initializes the ROS 2 node with the name `simple_robot_motion`.                                                    |
| `self.publisher_ = self.create_publisher(...)`                       | Creates a publisher that will send velocity commands to turtlesim.                                                 |
| `Twist,`                                                             | Specifies that the publisher sends messages of type `Twist`.                                                       |
| `'/turtle1/cmd_vel',`                                                | Specifies the ROS 2 topic used to control the velocity of turtle 1.                                                |
| `10`                                                                 | Sets the message queue depth to 10, allowing temporary storage of velocity commands if needed.                     |
| `def move_for(self, linear_speed, angular_speed, duration, action):` | Defines a reusable function to move the turtle at selected speeds for a selected period of time.                   |
| `command = Twist()`                                                  | Creates a new velocity command message.                                                                            |
| `command.linear.x = float(linear_speed)`                             | Sets the turtle’s forward or backward speed and ensures the value is stored as a float.                            |
| `command.angular.z = float(angular_speed)`                           | Sets the turtle’s left or right rotational speed and ensures the value is stored as a float.                       |
| `self.get_logger().info(f'{action} for {duration} seconds')`         | Displays the current movement action and its duration in the terminal.                                             |
| `start_time = time.time()`                                           | Records the time when the current movement begins.                                                                 |
| `while rclpy.ok() and time.time() - start_time < float(duration):`   | Repeats velocity publishing while ROS 2 is active and the movement duration has not ended.                         |
| `self.publisher_.publish(command)`                                   | Publishes the velocity command to turtlesim, causing the turtle to move.                                           |
| `time.sleep(0.1)`                                                    | Waits 0.1 seconds before publishing again, resulting in approximately 10 commands per second.                      |
| `self.stop()`                                                        | Stops the turtle once the specified movement duration is completed.                                                |
| `def stop(self):`                                                    | Defines a function that sends a zero-velocity command to stop all turtle movement.                                 |
| `command = Twist()`                                                  | Creates a new velocity message for the stop command.                                                               |
| `command.linear.x = 0.0`                                             | Sets forward and backward motion to zero.                                                                          |
| `command.linear.y = 0.0`                                             | Sets sideways linear motion to zero.                                                                               |
| `command.linear.z = 0.0`                                             | Sets vertical linear motion to zero.                                                                               |
| `command.angular.x = 0.0`                                            | Sets rotation around the x-axis to zero.                                                                           |
| `command.angular.y = 0.0`                                            | Sets rotation around the y-axis to zero.                                                                           |
| `command.angular.z = 0.0`                                            | Sets left and right turning motion to zero.                                                                        |
| `self.publisher_.publish(command)`                                   | Publishes the zero-velocity command, stopping the turtle.                                                          |
| `time.sleep(0.2)`                                                    | Pauses briefly to allow the stop command to be processed before the next action.                                   |
| `def main(args=None):`                                               | Defines the main function that controls program execution.                                                         |
| `rclpy.init(args=args)`                                              | Initializes ROS 2 communication for the Python program.                                                            |
| `node = SimpleRobotMotion()`                                         | Creates an instance of the custom motion-control node.                                                             |
| `try:`                                                               | Begins a protected block so that the program can safely handle user interruption.                                  |
| `node.move_for(1.0, 0.0, 0.5, 'Moving straight')`                    | Moves the turtle straight forward at linear speed `1.0` for `0.5` seconds.                                         |
| `node.move_for(1.0, 1.0, 3.0, 'Turning left')`                       | Moves the turtle forward while turning left for `3.0` seconds, producing a curved path.                            |
| `node.move_for(1.0, -1.0, 2.0, 'Turning right')`                     | Moves the turtle forward while turning right for `2.0` seconds, producing a curved path in the opposite direction. |
| `node.get_logger().info('Movement completed')`                       | Prints a completion message after all movement commands are executed successfully.                                 |
| `except KeyboardInterrupt:`                                          | Detects when the user stops the program manually using `Ctrl + C`.                                                 |
| `node.get_logger().info('Stopped by user')`                          | Displays a message indicating that execution was interrupted by the user.                                          |
| `finally:`                                                           | Defines cleanup operations that run whether the program finishes normally or is interrupted.                       |
| `node.stop()`                                                        | Sends a final stop command to ensure that the turtle is not moving when the program ends.                          |
| `node.destroy_node()`                                                | Destroys the ROS 2 node and releases its resources.                                                                |
| `rclpy.shutdown()`                                                   | Safely shuts down ROS 2 communication.                                                                             |
| `if __name__ == '__main__':`                                         | Checks whether the Python file is being executed directly.                                                         |
| `main()`                                                             | Starts the program by calling the main function.                                                                   |




