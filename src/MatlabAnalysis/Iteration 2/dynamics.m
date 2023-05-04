function dX = dynamics(t, X, v_ref)

    
    persistent prevangacc;
    persistent prevacc;
    if t == 0
        prevangacc = 0;
        prevacc = 0;
    end



    % System Parameters 
    Mc = 2; % Mass of cart
    Mp = 3; % Mass of pendulum
    theta = deg2rad(0); % Slope Angle
    B = 0.1; % Friction angle
    g = 9.8; % Acceleration due to gravity
    I = 0.3*10^-9;
    l = 0.3;
    phi_d = deg2rad(0);
    xd = v_ref*t;
    
    dX = zeros(4,1);
    X = num2cell(X);

    [x, phi, dx, dphi] = deal(X{:});   
    
    F = pd_control(x, dx, phi, dphi, xd,  v_ref, phi_d, prevacc);

    %F = LinearQuadRegulator(x, dx, phi, dphi, xd,  v_ref, phi_d, prevacc);

    dX(1) = dx;
    dX(2) = dphi;
    dX(3) = ((F - B*dx)/(Mc + Mp) - g*sin(theta) - ((Mp*l*prevangacc*cos(pi + phi) + Mp*l*dphi^2*sin(pi + phi))/(Mc + Mp)));
    dX(4) = (-Mp*l*dX(3)*cos(pi + phi) - Mp*g*l*sin(phi + pi + theta))/(I + Mp*l^2);

    prevacc = dX(3);
    prevangacc = dX(4);
end
