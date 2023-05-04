function F = LinearQuadRegulator(x, v , theta, thetad, xd, vd, phi_d, a)
    Mc = 2; % Mass of cart
    Mp = 3; % Mass of pendulum
    g = 9.8; % Acceleration due to gravity
    L = 0.3; % Length
    
    X = [x, theta, v, thetad]';
    X_ref = [xd;phi_d;vd;0];
    A = [0 0 1 0; 0 0 0 1; 0 -Mp*g/Mc 0 0; 0 (Mc + Mp)*g/(L*Mc) 0 0];
    B = [0 0 1/Mc -1/(L*Mc)]';

  
    Fdes = -inv(B'*B)*B'*A*X_ref;

    Q = diag([0.5,100,2,25]);
    R = [1];
    K = lqr(A, B, Q, R);
    K1 = [-K(1) , K(2), -K(3), K(4)];

    F = (K1*(X - X_ref));





    
end