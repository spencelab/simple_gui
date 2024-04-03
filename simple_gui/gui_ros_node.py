import sys
import time
import rclpy
from rclpy.node import Node

from std_msgs.msg import Int32

from PyQt5 import QtGui

class MyGuiNode(Node):
    def __init__(self, ui):
        super().__init__("ros2_hmi_node")
        self.ui = ui

        # Define our GUI button callbacks here
        self.ui.btn_publisher.clicked.connect(self.publisher_ros2_callback)

        # Define ROS2 publishers and subscribers here
        self._btn_publisher = self.create_publisher(Int32, '/chatter', 10)
        self._subscriber    = self.create_subscription(Int32, '/chatter', self.subscriber_callback, 1)

        # Define internal member variables
        self._count         = 0
        self.countf         = 0
        
        # Setup timer to do stuff.
        self.create_timer(1,self.timer_callback)
        self.get_logger().info("Added timer - slowstuff.")

        # Setup timer to do stuff.
        self.create_timer(0.01,self.timer_callback_fast)
        self.get_logger().info("Added timer - faststuff.")
        
        # Sanity check
        self.get_logger().info("Node set up properly.")

    # Define the member functions here
    def publisher_ros2_callback(self):
        """
            This function is executed when we click the button
            on the GUI. So, this button should publish a message
            on the /chatter topic. This is what we will implement
            in the function body.
        """
        self._count = self._count + 1   # We increment the counter first

        # This part is standard ROS2 publisher code 
        msg = Int32()
        msg.data = self._count 
        self._btn_publisher.publish(msg)
        self.get_logger().info(f"[Publisher] I sent: {msg.data}")

    def subscriber_callback(self, msg):
        """
            The objective of this function is to set the text of the
            particular textLabel element when there is new data being
            received. Check the Qt documentation for more things you 
            can do to display the data.
        """
        temp = msg.data
        self.get_logger().info(f"[Subscriber] I heard: {temp}")
        self.ui.label_subscriber.setText(f"{msg.data}")

    def timer_callback(self):
        self.get_logger().info("Working in the background...")
        
    def timer_callback_fast(self):
        self.countf = self.countf+1
        if self.countf % 100 == 0:
            self.get_logger().info("Done 100 fast iters...")        
        
