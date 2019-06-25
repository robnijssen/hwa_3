#!/usr/bin/env python

import time
import rospy
import actionlib
import hwa_3.msg

current_angle = 0 # servo will start on middle position, 90 degrees. 
valueReached = False
result = "global"

class ServoAction(object):

    feedback = hwa_3.msg.ServoFeedback()
    _result = hwa_3.msg.ServoResult()

    
    def count_to_number_handler(self, goal):
        r = rospy.Rate(4) # action server has a 4hz rate
        success = True
        global current_angle 
        angle = goal.servoAngle
        count = 0
        rospy.loginfo("Request received to change angle to  %i degrees" %(angle))
        rospy.loginfo('Program will now start changing anle')
        delta_angle =  angle - current_angle
    

        # check if servo needs to add or substract value
        if (current_angle <= angle):
            rospy.loginfo('requested angle is bigger, I need to add:%i.'%angle)
            rospy.loginfo('Servo needs to move:%i degrees.'%delta_angle)
            #adding value until desired angle has been reached
            valueToAdd = 1
            #count = count+1
            rospy.sleep(0.1)
            

        else:
            delta_angle = delta_angle * -1  #need to invert this value because its negative if the angle is smaller
            rospy.loginfo('requested angle is smaller, I need to substract %i.'%angle)
            rospy.loginfo('Servo needs to move:%i degrees.'%delta_angle) 
            valueToAdd = -1 # For loop needs to substract value from the current value
            #count = count +1
            rospy.sleep(0.1)




        for i in range(1, delta_angle+1):

        # Check that preempt has not been requested by the client
        # If yes, kill the action 
            if self.server.is_preempt_requested():
                rospy.loginfo('Preempted')
                self.server.set_preempted()
                success = False
                break
            rospy.loginfo(current_angle)
            time.sleep(0.1) #small delay to increase servo control 

            current_angle += valueToAdd # the current angle is changed with 1 degree every loop
            self._result.angleReached = False
            self.feedback.percentage = round(float((current_angle/180)*100))
            self.server.publish_feedback(self.feedback)
        
        if success:
            self._result.angleReached = True
            self.server.set_succeeded(self._result)

        rospy.loginfo('Angle reached: ready to change angle again.')
     
        r.sleep()
       

    
    
    def __init__(self):
        self.server = actionlib.SimpleActionServer('angle_to_servomotion', hwa_3.msg.ServoAction, self.count_to_number_handler, False)
        self.server.start()
    
    

if __name__ == "__main__":

    rospy.init_node('Servo_action_server')
    server = ServoAction()
    print("Initialization done, ready to control angle")
    rospy.spin()