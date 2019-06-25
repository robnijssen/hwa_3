#!/usr/bin/env python

import sys
import time
import roslib
import rospy
import actionlib
import hwa_3.msg

_result = hwa_3.msg.ServoResult()
_result.angleReached = False
global wait_for_result

def change_servo(angle):
    try:
        rospy.init_node('action_client')
        change_servo = actionlib.SimpleActionClient('angle_to_servomotion', hwa_3.msg.ServoAction)
        change_servo.wait_for_server()
        goal = hwa_3.msg.ServoGoal()
        goal.servoAngle = angle
        
        
        change_servo.send_goal(goal)
        # Waits for the server to finish performing the action.
        (wait_for_result) = change_servo.wait_for_result(timeout = rospy.Duration(10))
        #print bool (change_servo.get_result)
        # Prints out the result of executing the action
        return bool (wait_for_result)


    except rospy.ServiceException, e:
        rospy.loginfo("Action call failed: %s" %(e))

if __name__ == "__main__":
    
    while not rospy.is_shutdown():
        print('please type desired servo angle in range of 0 to 180 degrees.')
        angle = input('Angle:')
        #cap angle from 0 to 180
        if angle > 180:
            angle = 180
            rospy.loginfo('Entered numer is too high, changed to 180 instead.')
        if angle < 0:
            angle = 0
            rospy.loginfo('Entered numer is too small, changed to 0 instead.')
        

        print("Requesting the system to change servo angle to %i degrees" %(angle))
        raw_input("Press ENTER to start changing servo angle.")
        
        result = change_servo(angle)
        rospy.loginfo('Goal reached: %s' %result)
        
        if result != None:
            if result == True:
                rospy.loginfo('Desired goal has been reached, ready to take new order.')
            else:
                rospy.loginfo('Desired goal has not been reached, ready to take new order.')

            
