function [F, Fdot] = LinearQuadRegulator(x, v, xdef, v_ref, t)
    A = [];
    B = [];

  
    Fdes = -inv(B'*B)*B'*A*v_ref;


    
end