function dX = dynamics(t, X, v_ref)

    F = 0;
    Fdot = 0;
    
    % System Parameters 
    M = 10; % Total Mass
    theta = deg2rad(-5); % Slope Angle
    B = 0.1; % Friction angle
    g = 9.8; % Acceleration due to gravity

    
    dX = zeros(3,1);
    X = num2cell(X);

    [x, dx, ddx] = deal(X{:});

    
    %[F, Fdot] = pd_control(dx, ddx, v_ref, t);  
    [F, Fdot] = LinearQuadRegulator(dx, v_ref, t);
    
    
   
    
    dX(1) = dx;
    dX(2) = F/M - B*(dx)/M - g*sin(theta);
    dX(3) = 1/M*(Fdot - B*ddx);
end
