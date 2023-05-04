function dX = dynamics(t, X, v_ref)
    % Dirt Road is 0.6
    % Asphalt is 0.8
    % wet gravel is around 0.4
    %Mud is around 0.3
    F = 0;
    Fdot = 0;
    
    % System Parameters 
    M = 45; % Total Mass
    theta = deg2rad(0); % Slope Angle
    B = 0.1; % Friction angle
    g = 9.8; % Acceleration due to gravity

    
%     if t >= 10
%         v_ref = 0;
% 
%     end
% 
% %     if t < 10
% %         B =0.4
% %     end

    dX = zeros(3,1);
    X = num2cell(X);

    [x, dx, ddx] = deal(X{:});

    

    
    %[F, Fdot] = pd_control(dx, ddx, v_ref, t);  
    [F, Fdot] = LinearQuadRegulator(dx, v_ref, t);
    
    
   
    
    dX(1) = dx;
    dX(2) = F/M - B*(dx)/M - g*sin(theta);
    dX(3) = 1/M*(Fdot - B*ddx);
end
