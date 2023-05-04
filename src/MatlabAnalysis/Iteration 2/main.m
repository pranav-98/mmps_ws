T = 20;

X0 = [0 ; deg2rad(5); 0 ; 0 ]; % Initial State
v_ref = 0;

Calldynamics = @(t,X) dynamics(t, X, v_ref);
[t, y] = ode45(Calldynamics, [0,T], X0);





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




