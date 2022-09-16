import numpy as np
import matplotlib.pyplot as plt
from numpy.core.fromnumeric import std
from scipy.stats import norm

#-----------------------------------------------------------------------------#

T = 0 # counts how many rungs have made it through (center)
t = [0] # instantaneous position of the protein at each time step
x = 0 # random variable to decide how much random thermal diffusion at a given time step
N = 100000 # total number of time steps
L = 7 # one rung is approx. 7nm
D = 300000 # diffusion coefficient (in )
dt = 0.000001
u = 0 # drift value for Power Stroke Model 
X = [] # random diffusion distance for each time step
gamma = 0 # cutoff value for Brownian Ratchet Diffusion Probability Distribution
pawl = [0]
pawl_factor = 0.2*L # how 'strong' is the pawl? 
success_stop  = 105 # stop simulation after x length of successful translocation
fail_stop = -30 # stop after failed translocation of length x
#-----------------------------------------------------------------------------#

### Single Runs 
# for i in range(0,N):
#     Failure = False
#     Translocated = False
    
#     # Sole Diffusion:
#     x = np.random.normal(0,np.sqrt(2*D*dt))

#     # Brownian Ratchet:
#     ## once a segment L has diffused through, backwards diffusion is limited to 0.1L
#     if t[-1] > (T+1)*L:
#         pawl.append(t[-1])
#         T = T + 1
    
#     if pawl[-1] - t[-1] >= pawl_factor:
#         t[-1] = t [-2]

#     t.append(t[-1]+x)
#     X.append(x)

#     if t[-1] <= fail_stop:
#         # print('Failure')
#         Failure = True
        
#     if t[-1] >= success_stop:
#         # print('Translocated')
#         Translocated = True
#         break

#     if Failure == True or Translocated == True:
#         break
    
# plt.plot(np.linspace(0,len(t),len(t)),t)
# plt.axhline(y=success_stop, color='r', linestyle='-')
# plt.show()

#-----------------------------------------------------------------------------#

### Batch Runs
success = [] ## keeps track of how many successful translocation accross the trials
trans_times = [] ## tracks the time to translocate for each trial (only successes)

for j in range(0,100):
    t = [0]
    pawl = [0]
    T = 0
    for i in range(0,N):
        Failure = False
        Translocated = False
        
        # Sole Diffusion:
        x = np.random.normal(0,np.sqrt(2*D*dt))

        # Brownian Ratchet:
        ## once a segment L has diffused through, backwards diffusion is limited to 0.1L

        if t[-1] > (T+1)*L:
            pawl.append(t[-1])
            T = T + 1
     
        if pawl[-1] - t[-1] >= pawl_factor:
            t[-1] = t[-2]
        
        # End of Brownian Ratchet Segment

        t.append(t[-1]+x)
        X.append(x)

        if t[-1] <= fail_stop:
            # print('Failure')
            Failure = True
            
        if t[-1] >= success_stop:
            # print('Translocated')
            trans_times.append(i)
            Translocated = True

        if Failure == True or Translocated == True:
            break

    if Failure == True and Translocated == False:
        success.append(0)
    if Translocated == True and Failure == False:
        success.append(1)

    plt.plot(np.linspace(0,len(t),len(t)),t)

plt.axhline(y=success_stop, color='g', linestyle='-')
plt.axhline(y=fail_stop, color='r', linestyle='-')
plt.ylim(-40,130)
plt.show()
print(np.sum(success)/len(success))
print('Average time = ' + str(np.mean(trans_times)))
print('St. Dev. = ' + str(np.std(trans_times)))

#-----------------------------------------------------------------------------#
