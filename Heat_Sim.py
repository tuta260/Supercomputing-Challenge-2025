# This is our primary file from which we analyze heat distribution in our system

import math
import numpy as np
#import fdsreader
#from fdsreader.bndf.utils import sort_patches_cartesian
import numpy as np
import matplotlib.pyplot as plt
#import pandas as pd
import matplotlib

plt.style.use('_mpl-gallery-nogrid')


# Static position model defines grid as units of one with "adjacent"
# being defined as within a 2 by 2 cube centered on the particle in question 

class Particle(object): 
    # change __init__ structure to 3d 
    def __init__(self,xPos,yPos,temp): 
        self.x = xPos
        self.y = yPos
        self.t = temp
    
    def changeTemp(self,newTemp):
        self.t = newTemp
    
    
     


class Plate(Particle):

    pass

class Extruder(object): 
    
    pass 

class Material(Particle):
    
    pass 

#make a sample set for 10 by 10 area
iLength = 10
kLength = 10

particleList = np.array([None]*iLength*kLength)

i=0
while(i<iLength):
    k=0
    while(k<kLength):
        #change starting temperatures here
        particleList[iLength*i+k] = Particle(i+1,k+1,5*k+9*i-k**2)
        k+=1
    
    i+=1
  
'''  
i=0
while(i<len(particleList)):
	print("particle at x ",particleList[i].x, " y ", particleList[i].y, "with temp ", particleList[0].t)
	i+=1
'''

def runTimeStep(time):
	
	#Consider adjacent particles as defined by relevant area and thickness to transfer heat
	#∆Q ~ Area of conduction / thickness of separating material (in this case distance between particles)* ∆T * t
	#for particles that are getting farther away from one another, the area goes to zero and the 'thickness' goes to infinity
	#think of the area at the percent of your view taken up by the particle and it getting smaller as it travels away 
	
	#Since it is difficult to calculate and make sense of that kind of area in this particle based model
	#this will be approximated for now with Diameter of Particle ** 2/ distance away ** 3
	# (this comes from pretending its a square with side length diameter then diminishing effect with distance)
	
	#So the diameter of the particles is (for now) 1 cm the sim 10 cm in size
	
	#this model allows for very liberal transfer of heat and 
	
	



# plot
fig, ax = plt.subplots()

x = np.array([None]*len(particleList))
y = np.array([None]*len(particleList))
temps = np.array([None]*len(particleList))
i=0
while(i<len(particleList)):
	x[i] = particleList[i].x
	y[i] = particleList[i].y
	temps[i] = particleList[i].t
	i+=1
print("Max: ",np.amax(temps)," Min: ", np.amin(temps))
ax.scatter(x, y, c=temps, vmin=np.amin(temps),vmax = np.amax(temps))

ax.set(xlim=(0, 11), xticks=np.arange(0, 10),
       ylim=(0, 11), yticks=np.arange(0, 10))

plt.show()