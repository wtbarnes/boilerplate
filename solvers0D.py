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
        new_state = np.zeros(len(state))
        if len(derivs) != len(state):
            raise ValueError("Dimension mismatch between state and derivs vectors.")
        for i in range(len(derivs)):
            new_state[i] = state[i] + derivs[i]*tau
            
        return new_state
        
        
    def rk4_solve(self,state,time,tau):
        """Use fourth-order Runge-Kutta solver to step equation forward in time."""
            
        #calculate f functions
        #   cast as numpy array just in case this has not been done in the function
        f1 = np.array(self.func(state,time,tau,**self.func_params))
        f2 = np.array(self.func(state+tau/2*f1,time+tau/2,tau/2,**self.func_params))
        f3 = np.array(self.func(state+tau/2*f2,time+tau/2,tau/2,**self.func_params))
        f4 = np.array(self.func(state+tau*f3,time+tau,tau,**self.func_params))
        
        return np.array(state) + tau/6.0*(f1 + 2.0*f2 + 2.0*f3 + f4)
        
        
    #def adaptive_timestep(self,)