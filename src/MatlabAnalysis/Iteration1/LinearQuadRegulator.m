function [F, Fdot] = LinearQuadRegulator(v, v_ref, t)



 M = 45;
 b = 0.1;

 A = [-b/M];
 B = [1/M];

% Defining variables as persistent to store the previous values
    persistent j
    persistent tim
    persistent Farray
    persistent Fdotarray

    if isempty(j)
        j = 0; 
    end
    j = j + 1;
    tim(j) = t;

  
    Fdes = -inv(B'*B)*B'*A*v_ref;

% For working LQR
%For working LQR
Q = [50];
R = [5];


    K = lqr(A, B, Q, R);
    Farray(j) = (Fdes - K*(v - v_ref));
  
    if t == 0
        Fdotarray(j) = 0;  
    else
        delT = tim(j) - tim(j - 1);
        if delT == 0
            Fdotarray(j) = Fdotarray(j - 1);
        else 
                Fdotarray(j) = (Farray(j) - Farray(j - 1))/delT;        
        end 
    end
    F = Farray(j);
    Fdot = Fdotarray(j);
    
end