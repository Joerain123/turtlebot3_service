#!/usr/bin/env python2
#-*- coding:utf-8 -*-
#该程序将执行/turtlebot_command服务,服务数据类型std_srvs/Trigger
import rospy
import thread, time
from geometry_msgs.msg import Twist
from std_srvs.srv import Trigger, TriggerResponse

pubCommand = False
turtlebot_vel_pub = rospy.Publisher('/cmd_vel', Twist, queue_size = 10)
def command_thread():
	while True:
		if pubCommand:
			vel_msg = Twist()
			vel_msg.linear.x = 0.5
			vel_msg.angular.z = 0.2
			turtlebot_vel_pub.publish(vel_msg)
		time.sleep(0.1)

def commandCallback(req):
	global pubCommand
	pubCommand = bool(1 - pubCommand)
	#显示请求数据
	rospy.loginfo("Publish turtlebot velocity command![%d]",pubCommand)
	#反馈数据
	return TriggerResponse(1, "Change turtlebot command state!")

def turtlebot_command_server():
	#初始化节点
	rospy.init_node('turtlebot_command_server')
	#创建一个名为/turtle_command的server, 注册回调函数commandCallback
	s = rospy.Service('/turtlebot_command', Trigger, commandCallback)
	#循环等待回调函数
	print("Ready to receive turtlrebot command")
	thread.start_new_thread(command_thread, ())
	rospy.spin()

if __name__ == '__main__':
	turtlebot_command_server()
