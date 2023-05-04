T = 200;

X0 = [0 ; deg2rad(5); 0 ; 0 ]; % Initial State
v_ref = 2;

Calldynamics = @(t,X) dynamics(t, X, v_ref);
[t, y] = ode45(Calldynamics, [0,T], X0);


% N = length(y)
% jerk = []
% jerk(1) = 0;
% for i = 2 : N
%     jerk(i) = (y(i, 3) - y(i - 1, 3))/(t(i) - t(i - 1));
% end




subplot(2,2,1);
plot(t,y(:,1));
title('x vs time');

subplot(2,2,2);
plot(t,y(:,2));
title('theta vs time');

subplot(2,2,3);

plot(t,y(:,3));
title('velocity vs time');

subplot(2,2,4);

plot(t, y(:,4));
title('dang vs time');







