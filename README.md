# 020_Angle_Feedback
This app demonstrates a simple feedback application. The feedback nodes vibrate if the sensor node orientation exceeds minimum or maximum thresholds.

### Nodes Required: 3 
- Sensing (1): Can be placed anywhere on the body, and the angle will be estimated about the Z axis.
- Feedback (2): 
  - min (angle minimum limit)
  - max (angle maximum limit) 

## Algorithm & Calibration
### Algorithm Information
The raw quaternions from the IMU are converted to Euler angles, and the roll angle is extracted using well established mathematical principles. If you'd like to learn more about quaternion to Euler angles calculations, we suggest starting with this Wikipedia page: [Conversion between quaternions and Euler angles](https://en.wikipedia.org/wiki/Conversion_between_quaternions_and_Euler_angles)

### Calibration Process:
The angle calculated is the global roll angle for the IMU. This must be aligned with the segment. No initial static calibration is performed to compensate for misalignment with the segment.

## Description of Data in Downloaded File
- time (sec): time since trial start
- Angle: angle being measured.
- angle_min: The lower threshold set by the user in the App configuration Panel.
- angle_max: The upper threshold set by the user in the App configuration Panel.
- min_feedback_state: feedback status for if the sensor has crossed the min angle threshold. 
  - 0 is “feedback off”
  - 1 is “feedback on” 
- max_feedback_state: feedback status for if the sensor has crossed the max angle threshold. 
  - 0 is “feedback off”
  - 1 is “feedback on” 
- SensorIndex: index of raw sensor data
- AccelX/Y/Z (m/s^2): raw acceleration data
- GyroX/Y/Z (deg/s): raw gyroscope data
- MagX/Y/Z (μT): raw magnetometer data
- Quat1/2/3/4: quaternion data (Scaler first order)
- Sampletime: timestamp of the sensor value
- Package: package number of the sensor value

# Development and App Processing Loop
The best place to start with developing or modifying an app, is the [SageMotion Documentation](http://docs.sagemotion.com/index.html) page.
