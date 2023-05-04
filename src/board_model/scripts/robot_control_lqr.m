clear; close; clc;

v_ref2 = 3;

v_ref1 = 0;
Kp = 3;
Kd = 3;
rad = 1;
v_prev = 0;
t_prev = 0;
x_array = [];
vel_array = [];
accel_array = [];
jerk_array = [];
tau_array = [];

a_x_array = [];
a_y_array = [];
a_z_array = [];
angle_array = [];

M = 270;
b = 0.9;

Q = 80;
R = 20;    

%A = -b/(M*0.984);
A = -b/(M);
B = 1/M;
K = lqr(A,B,Q,R);

time_array = [];
time_pause = 0.5;

% ROS Setup
rosinit;

motor1 = rospublisher('/skateboard_test/joint1_effort_controller/command');
motor2 = rospublisher('/skateboard_test/joint2_effort_controller/command');
motor3 = rospublisher('/skateboard_test/joint3_effort_controller/command');
motor4 = rospublisher('/skateboard_test/joint4_effort_controller/command');

position = rossubscriber('/position');
velocity = rossubscriber('/velocity');
imu = rossubscriber('/imu');

tau1 = rosmessage(motor1);
tau2 = rosmessage(motor2);
tau3 = rosmessage(motor3);
tau4 = rosmessage(motor4);

client = rossvcclient('/gazebo/set_model_configuration');
req = rosmessage(client);
req.ModelName = 'skateboard_test';
req.UrdfParamName = 'robot_description';
resp = call(client,req,'Timeout',3);

tic;
t = 0;
while t < 20
    t = toc;
    v_ref = v_ref2;
    if t < 10
        v_ref = v_ref2;
    end

    if t > 14
        v_ref = v_ref1;
    end

    pos = receive(position);
    vel = receive(velocity);
    IMU = receive(imu);

    x = pos.Data;
    dx = vel.Data;
    a = IMU.LinearAcceleration.X;
    a_y = IMU.LinearAcceleration.Y;
    a_z = IMU.LinearAcceleration.Z;
    angle = rad2deg(IMU.Orientation.Y);
    

    Fdes = -inv(B'*B)*B'*A*v_ref;
    %F = Kp*(dx - v_ref) + Kd*(a);
    F =  - (Fdes - K*(dx - v_ref));

    tau = F/(8*rad);
    tau1.Data = tau;
    tau2.Data = tau;
    tau3.Data = tau;
    tau4.Data = tau;

    send(motor1, tau1);
    send(motor2, tau2);
    send(motor3, tau3);
    send(motor4, tau4);

    pause(time_pause)

    tau_array = [tau_array F];
    x_array = [x_array x];
    vel_array = [vel_array dx];
    time_array = [time_array t];
    a_x_array = [a_x_array a];
    a_y_array = [a_y_array a_y];
    a_z_array = [a_z_array a_z];
    angle_array = [angle_array angle];

    t_prev = t;
    v_prev = dx;
   
end
tau1.Data = 0;
tau2.Data = 0;
tau3.Data = 0;
tau4.Data = 0;
send(motor1, tau1);
pause(time_pause)
send(motor2, tau2);
pause(time_pause)
send(motor3, tau3);
pause(time_pause)
send(motor4, tau4);
pause(time_pause)
rosshutdown;

for i = 1:size(vel_array') - 1
    accel_array(i) = (vel_array(i + 1) - vel_array(i))/(time_array(i+1) - time_array(i));
end
accel_array(end + 1) = 0;


for i = 1:size(accel_array') - 1
    jerk_array(i) = (accel_array(i + 1) - accel_array(i))/(time_array(i+1) - time_array(i));
end
jerk_array(end + 1) = 0;


subplot(2,2,1);

plot(time_array, x_array);
title('time vs x');
hold on;



subplot(2,2,2);
plot(time_array, vel_array);
title('time vs velocity');
hold on;




subplot(2,2,3);

plot(time_array, accel_array);
title('time vs acceleration');
hold on;



subplot(2,2,4);
plot(time_array, jerk_array);
title('time vs jerk');
hold on;


