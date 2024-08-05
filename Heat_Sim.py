# This is our primary file from which we analyze heat distribution in our system

import math
import numpy as np
#import fdsreader
#from fdsreader.bndf.utils import sort_patches_cartesian
import numpy as np
import matplotlib.pyplot as plt
#import pandas as pd
import matplotlib
import matplotlib.animation as animation
import random

plt.style.use('_mpl-gallery-nogrid')


# Static position model defines grid as units of one with "adjacent"
# being defined as within a 2 by 2 cube centered on the particle in question 

class Particle(object): 
    # change __init__ structure to 3d 
    def __init__(self,xPos,yPos,zPos,temp): 
        self.x = xPos
        self.y = yPos
        self.z = zPos
        self.t = temp
    
    def changeTemp(self,newTemp):
        self.t = newTemp
    
    def changeX(self,newX):
        self.x = newX
    
    def changeY(self,newY):
        self.y = newY
    
    def changeZ(self,newZ):
        self.z = newZ


class Plate(Particle):

    pass

class Extruder(Particle): 
    
    pass 

class Material(Particle):
    
    pass 

#make a sample set for 10 by 10 area
iLength = 4
kLength = 4
jLength = 10
frameNum = 100

systemTime = 0 #for reference whenever an update is made to the system the time should be adjusted
repeating = False

particleList = np.array([None]*iLength*kLength*jLength)
particleListHist = np.array([[None]*iLength*kLength*jLength]*(frameNum+1))

i=0
while(i<iLength):
    k=0
    while(k<kLength):
        j=0
        while(j<jLength):
            realIndex = iLength*kLength*j+kLength*i+k
            #particleList[realIndex] = Particle(i+1,k+1,j+1,random.random()*100)
            particleList[realIndex] = Particle(i+1,k+1,j+1,0)
            if(j==0):
                particleList[realIndex].changeTemp(100)
            
            j+=1
        k+=1
    i+=1

n=0
while(n<frameNum+1):
    i=0
    while(i<iLength):
        k=0
        while(k<kLength):
            j=0
            while(j<jLength):
                realIndex = iLength*kLength*j+kLength*i+k
                if(n==0):
                    particleListHist[n][realIndex] = Particle(i+1,k+1,j+1,particleList[realIndex].t)
                else:
                    particleListHist[n][realIndex] = Particle(i+1,k+1,j+1,None)
                j+=1
            k+=1
        i+=1
    n+=1
'''  
i=0
while(i<len(particleList)):
    print("particle at x ",particleList[i].x, " y ", particleList[i].y, "with temp ", particleList[0].t)
    i+=1
'''


#Consider adjacent particles as defined by relevant area and thickness to transfer heat
#∆Q ~ Area of conduction / thickness of separating material (in this case distance between particles)* ∆T * t
#for particles that are getting farther away from one another, the area goes to zero and the 'thickness' goes to infinity
#think of the area at the percent of your view taken up by the particle and it getting smaller as it travels away 
    
#Since it is difficult to calculate and make sense of that kind of area in this particle based model
#we will consider two paths: Refining the grid while keeping well define conduction relations
# and considering a completely free interaction based on more accurate contact surfaces

#the more simple of the two
def runTimeStep1(timeStep):

    changeInHeat = np.array([0.0]*len(particleList))
    
    #adjacent is defined by with a distance less than the grid size (with additional margin)
    ind = -1
    for particle in particleList:
        lx = particle.x
        ly= particle.y
        lz = particle.z
        ind +=1
        
        #dad's problem
        if(lz == 1):
            particle.changeTemp(100)

        #find adjacent
        adjacentIndices = np.array([None]*30)
        adjDists = np.array([None]*30)
        nextEnter = 0
        i = 0
        while(i<len(particleList)):
            #general block to limit calculation complexity and speed
            if((((abs(particleList[i].x) - lx)<1.5 and (abs(particleList[i].y - ly)<1.5)) and (abs(particleList[i].z-lz)<1.5)) and not(ind == i)):
                distanceTo = math.sqrt((particleList[i].x-lx)**2+(particleList[i].y-ly)**2+(particleList[i].z-lz)**2)
                if(distanceTo < 1.5):
                    adjacentIndices[nextEnter]=i
                    adjDists[nextEnter]=distanceTo
                    nextEnter +=1
                    if(nextEnter == 30):
                        print("Error: solid too dense -- too many 'adjacent' particles found")
                        i = len(particleList)

            i+=1
        
        i=0
        while(i < nextEnter):
            particleActive = particleList[adjacentIndices[i]]
            #∆Q ~ 1cm^2 / math.sqrt((particleList[i].x-lx)**2+(particleList[i].y-ly)**2) * (tempLocal - tempExternal)* timeStep /2   Divided by two since all interactions will be considered twice from both sides
            heatOut = (particle.t-particleActive.t)/(adjDists[i])*timeStep/2 # * some proportionality constant
            changeInHeat[adjacentIndices[i]] += heatOut
            changeInHeat[ind] -= heatOut
            i+=1

    i = 0
    while(i< len(particleList)):
        particleList[i].changeTemp(particleList[i].t+changeInHeat[i])
        i+=1
    
    


def plot():
    # plot
    fig, ax = plt.subplots(subplot_kw={"projection": "3d"})

    x = np.array([None]*len(particleList))
    y = np.array([None]*len(particleList))
    z = np.array([None]*len(particleList))
    temps = np.array([None]*len(particleList))
    i=0
    while(i<len(particleList)):
        #print(i)
        x[i] = particleList[i].x
        y[i] = particleList[i].y
        z[i] = particleList[i].z
        temps[i] = particleList[i].t
        i+=1
    print("Scale Max: ",np.amax(temps)," Min: ", np.amin(temps))
    ax.scatter(x, y, z, c=temps, vmin=np.amin(temps), vmax = np.amax(temps))

    ax.set(xlim=(0, iLength+1), xticks=np.arange(0, iLength+1),
           ylim=(0, kLength+1), yticks=np.arange(0, kLength+1))

    plt.show()
    
    fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
    
    print("Scale: -50 - 100")
    ax.scatter(x, y, z, c=temps, vmin=-50, vmax = 100)

    ax.set(xlim=(0, iLength+1), xticks=np.arange(0, iLength+1),
           ylim=(0, kLength+1), yticks=np.arange(0, kLength+1),)

    plt.show()


plot()
running = False
while(running):
    if(input("Would you like to run it for a timestep? y/n ")=="y"):
        runTimeStep1(.1)
        systemTime += .1
        plot()
    elif(input("Would you like to run for a longer time? y/n ")=="y"):
        totalTime = (int)(input("How long would you like to run the simulation? (min)"))
        i = 0
        while(i < totalTime):
            runTimeStep1(.1)
            systemTime += .1
            i+=.1
        plot()
    else:
        running = False
        


def updateParticles(num):
    
    #if repeating sequence (end of history is full)
    if(not(particleListHist[frameNum][0].t==None)):
        i=0
        while(i<len(particleList)):
            particleList[i] = particleListHist[num][i]
            i+=1
    else:
        runTimeStep1(.05)
        #record
        i=0
        while(i<len(particleList)):
            particleListHist[num+1][i].changeTemp(particleList[i].t)
            particleListHist[num+1][i].changeX(particleList[i].x)
            particleListHist[num+1][i].changeY(particleList[i].y)
            particleListHist[num+1][i].changeZ(particleList[i].z)
            i+=1
    
    systemTime = math.trunc(num*5+5)/100
    
    #update plot 
    x = np.array([None]*len(particleList))
    y = np.array([None]*len(particleList))
    z = np.array([None]*len(particleList))
    temps = np.array([None]*len(particleList))
    i=0
    while(i<len(particleList)):
        #print(i)
        x[i] = particleList[i].x
        y[i] = particleList[i].y
        z[i] = particleList[i].z
        temps[i] = particleList[i].t
        i+=1
    ax.scatter(x, y, z, c=temps, vmin=-50, vmax = 100)
    ax.set(xlim=(0, iLength+1), xticks=np.arange(0, iLength+1),
           ylim=(0, kLength+1), yticks=np.arange(0, kLength+1))
    ax.set_title(f"time: {systemTime} min")
    

fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
ani = animation.FuncAnimation(
    fig, updateParticles, frames=frameNum, interval=500)

plt.show()
