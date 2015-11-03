#Name: solvers0D.py
#Author: Will Barnes
#Purpose: Implement several basic ODE methods 

#Import needed modules
import numpy as np

class Solvers0D(object):
    
    def __init__(self,func,func_params,rka_err=1e-6,safety_1=0.9,safety_2=1.1,safety_3=4.0):
        """Initialize 0D Solvers class."""
        
        if type(func).__name__ != 'function':
            raise TypeError("Input function is not of type function.") 
        else:
            self.func = func
        self.func_params = func_params
        #save adaptive stepper parameters
        self.rka_err = rka_err
        self.safety_1 = safety_1
        self.safety_2 = safety_2
        self.safety_3 = safety_3
        
        
    def euler_solve(self,state,time,tau):
        """Use first order Euler method to step equation forward in time."""
        
        #Step forward in time
        derivs = self.func(state,time,tau,**self.func_params)
        
        #Update parameters
        if len(derivs) != len(state):
            raise ValueError("Dimension mismatch between state and derivs vectors.")
        for i in range(len(derivs)):
            state[i] += derivs[i]*tau
            
        return state
        
        
    def rk4_solve(self,state,time,tau):
        """Use fourth-order Runge-Kutta solver to step equation forward in time."""
        
        #Initialize different time and timestep lists
        tau_temp = [.5*tau]*3 + [tau]
        time_temp = [time] + [time+.5*tau]*2 + [time+tau]
        
        initial_state = state
        f_rk = []
        
        #Calculate RK f_1--f_4 functions
        for i in range(len(tau_temp)):
            f_rk.append(self.func(state,time_temp[i],tau_temp[i],**self.func_params))
            if len(f_rk[-1]) != len(state):
                raise ValueError("Dimension mismatch between state and derivs vectors.")
            for j in range(len(f_rk[-1])):
                state[j] += f_rk[-1]*tau_temp[i]
                
        #Update state vector
        for i in range(len(initial_state)):
            state[i] = initial_state[i] + 1.0/6.0*tau*(f_rk[0][i] + f_rk[3][i] + 2.0*(f_rk[1][i] + f_rk[2][i]))
            
        return state
        
        
    #def adaptive_timestep(self,)