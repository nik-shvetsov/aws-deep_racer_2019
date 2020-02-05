def reward_function(params):
    import math

    # Read input parameters
    track_width = params['track_width']
    distance_from_center = params['distance_from_center']
    
    # Calculate 3 markers that are at varying distances away from the center line
    marker_1 = 0.1 * track_width
    marker_2 = 0.25 * track_width
    marker_3 = 0.5 * track_width
    
    # Give higher reward if the car is closer to center line and vice versa
    if distance_from_center <= marker_1:
        reward = 1.0
    elif distance_from_center <= marker_2:
        reward = 0.5
    elif distance_from_center <= marker_3:
        reward = 0.1
    else:
        reward = 1e-3  
    
    if not (params['all_wheels_on_track']):
        reward = 1e-3
    
    # Waypoint checks
    i_closest_next = params['closest_waypoints'][1]
    k_1 = math.fabs(params['waypoints'][i_closest_next][0] - params['x'])
    k_2 = math.fabs(params['waypoints'][i_closest_next][1] - params['y'])
    if (k_2 == 0.0): desired_dir = 0
    else: desired_dir = math.atan(k_1 / k_2)
    if math.fabs(params['steering_angle'] - desired_dir) > 4.0 :
        reward *= 0.4
    
    # Speed incentive
    SPEED_THRESHOLD = 3.0
    if params['speed'] < SPEED_THRESHOLD:
        reward *= 0.5
        
    # Steer restiction based on right/left position on the track
    if (params['is_left_of_center']	== True) and (params['steering_angle'] > 0):
        reward *= 0.2
    elif (params['is_left_of_center'] == False) and (params['steering_angle'] < 0):
        reward *= 0.2
    elif (params['is_left_of_center'] == True) and (params['steering_angle'] < 0):
        reward *= 1.2
    elif (params['is_left_of_center'] == False) and (params['steering_angle'] > 0):
        reward *= 1.2
    
    ABS_STEERING_THRESHOLD = 15
    if abs(params['steering_angle']) > ABS_STEERING_THRESHOLD:
	    reward *= 0.5
    
    # Finish incentive
    if params['progress'] == 100.0:
        reward += 1000
    
    return float(reward)