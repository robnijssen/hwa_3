#!/usr/bin/env python

from hwa_3.srv import *
import rospy

# Here's your service callback function
def handle_check_points(req):

    # Check if enough points have been reached, total should be greather than 17. 
    print 'request received to check if enough amount of points are reached'
    if req.Ros + req.Vision + req.PrinciplesOfRobotics + req.Safety + req.HardwareAbstraction >= 17:
        message = "Points have been reached, Congrats!"
    else:
        message = "Points are not reached yet, please hurry!"
    return PointsReachedResponse(message)


def handle_to_level_server():
    rospy.init_node('check_points_server')
    
    # Here's the  service hook 
    service = rospy.Service('points', PointsReached, handle_check_points)
    print("Ready to check if enough points have been reached.")
    rospy.spin()

if __name__ == "__main__":
    handle_to_level_server()