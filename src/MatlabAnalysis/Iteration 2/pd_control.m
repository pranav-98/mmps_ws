function F = pd_control(x, v , theta, thetad, xd, vd, phi_d, a)
    Kp1 = 0.2;
    Kd1 = 1.9;
    Kp2 = 200;
    Kd2 = 100;


    F =     Kp1*(x - xd) + Kd1*(v - vd) + Kp2*(phi_d - theta) + Kd2*(-thetad);
    
end