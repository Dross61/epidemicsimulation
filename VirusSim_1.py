# -*- coding: utf-8 -*-
"""
Created on Thu Nov 12 20:47:29 2020

@author: rjame
"""

import numpy as np
from random import *
import matplotlib.pyplot as plt  

def printPop(pop): # print matrix of population
    for x in range(PopSize):
        for y in range(PopSize):
            print(int(pop[x][y]),',', end ="")
        print("")
    return

def spread():  # this is the epidemic engine where sick people infect others
    # this is a very elementary infection model
    # every day we assume an infected person comes in contact with 3 people 
    # example R=1.5 means an infected person will infect 1.5 people during the course of their illness
    # RecoveryPeriod=5 days So each infected person comes in contact with 3*5 or 15 people over 5 days while they are infectous
    # so the chance of any of the 15 people getting infected is 1.5/15 or 0.1 or 10%
    # why only 3 people? Because it's easy to simulate, we are picking the person to right, diagonal left down 
    # and just below in the Population array, we shuffle the array every day to simulate the person moving through society
    
    # first let's loop for the population and add +1 sick days to all sick people and declare people immune if sick for RecoveryPeriod days
    for PersonIndex in range(len(HealthPopulation)):
        dayssick=HealthPopulation[PersonIndex][1]
        if(dayssick<RecoveryPeriod+1 and HealthPopulation[PersonIndex][0]==1):
            HealthPopulation[PersonIndex][1]+=1 # increment days sick
            if(HealthPopulation[PersonIndex][1]>RecoveryPeriod):  # if they have been sick longer than recovery period
                HealthPopulation[PersonIndex][0]=2 # make them immune
    
    # now lets get people sick
    PofInfecting=R/(RecoveryPeriod*3)
    Probaility = (PofInfecting) 
    for x in range(1,PopSize-1):  # move through Population Array
        for y in range(1,PopSize-1):
            PersonIndex=int(Population[x][y])  # find the index of the person
            if(HealthPopulation[PersonIndex][0]==1): #look them up in the HealthPopulation array are they sick? if so try to infect 3 people 
                NextPersonToRight=int(Population[x][y+1])  # if they are sick, find first person to their right in the Population array
                if(HealthPopulation[NextPersonToRight][0]==0): # if they are not sick, lets try to get them sick
                    rolldice=randint(0, 100)
                    if(rolldice<Probaility*100): # they lose
                        HealthPopulation[NextPersonToRight][0]=1  # set them to sick
                
                NextPersonDiagonal=int(Population[x+1][y+1])  # if they are sick, find first person to their right in the Population array
                if(HealthPopulation[NextPersonDiagonal][0]==0): # if they are not sick, lets try to get them sick
                    rolldice=randint(0, 100)
                    if(rolldice<Probaility*100): # they lose
                       HealthPopulation[NextPersonDiagonal][0]=1  # set them to sick         
                    
                NextPersonBelow=int(Population[x+1][y+1])  # if they are sick, find first person to their right in the Population array
                if(HealthPopulation[NextPersonBelow][0]==0): # if they are not sick, lets try to get them sick
                    rolldice=randint(0, 100)
                    if(rolldice<Probaility*100): # they lose
                       HealthPopulation[NextPersonBelow][0]=1  # set them to sick             
    return

def seed(seed): # we need to seed the epidemic 
    seedcount=int((PopSize*PopSize) * seed/100)
    print("Seed Count:",seedcount)
    for x in range(0,seedcount):
        luckyperson=randint(0,(PopSize*PopSize)-1)
        HealthPopulation[luckyperson][0]=1
    return

def tally(): #keep running score of the population
    notsickcount=0    
    sickcount=0
    immunecount=0
    for x in range(PopSize*PopSize):  # python does not have a case switch function so this is brute force
            if(HealthPopulation[x][0]==0):
                notsickcount+=1
            if(HealthPopulation[x][0]==1):
                sickcount+=1
            if(HealthPopulation[x][0]==2):
                immunecount+=1
    return(notsickcount,sickcount,immunecount)

#start of program

#Everyone starts out 0, not infected
# 0 not infected
# 1 infected
# 2 recovered, immune and can't spread
#populate the HealthPopoulation array index=person id, column 0= 0 (not infected) column 1=days sick 

# The simulation parameters, play with these to experiment
PopSize=100 #population will be PopSize x PopSize 
Population = np.zeros( (PopSize, PopSize) )  # create population each person will have an ID number, 0 to PopSize*PopSize
HealthPopulation= np.zeros( (PopSize*PopSize,2) )  # this is where we track if not infected, sick, recovered/immune
R=4.0  # best estimate current for world try others at https://en.wikipedia.org/wiki/Basic_reproduction_number
RecoveryPeriod=10 #days
SeedNumber=1 # in percent to start the epidemic off, someone has to
DaysToRunSim=60 # length of epidemic 
epidemic = np.array([PopSize*PopSize,0,0,0]) # matrix to store, daycount, not infected ever, sick, immune

#print initial epidemic parameters
print("Population Size=",PopSize*PopSize,"R0=",R,"Seed %=",SeedNumber,"Epidemic Run in Day=",DaysToRunSim)

# assign numeric IDs to each person, each person will have an ID number from 0 to PopSize*PopSize
# we will later shuffle Population to simulate people moving around in the society
count=0
for x in range(0,PopSize):
    for y in range(0,PopSize):
        Population[x][y]=count
        count+=1

# lets seed the population with some sick people who don't know they are sick
seed(SeedNumber)

print("Day, Not Sick, Sick, Immune")

for Day in range(1,DaysToRunSim):
    spread()
    np.random.shuffle(Population.flat) #move the people around
    notsick,sick,immune=tally()  # count not sick, sick, immune for the day
    addrow = np.array([Day,notsick,sick,immune]) # assemble count into array for adding below
    epidemic = np.vstack ((epidemic,addrow))  # add new day counts to the bootom of epidemic array
    print(epidemic[Day][0],",",epidemic[Day][1],",",epidemic[Day][2],",",epidemic[Day][3])    # print daily score of epidemic

# plot
fig, ax = plt.subplots(1,figsize=(15, 6))
ax = plt.axes()
title='My Epidemic Population Size='+str(PopSize*PopSize)+' R0='+str(R)+' Seed Infected %='+str(SeedNumber)
plt.title(title)  
plt.xlabel("Day")  
plt.ylabel("People")  
plt.plot(epidemic[:,2], color ="red", label='Sick')
plt.plot(epidemic[:,3], color ="green", label='Immnune')
plt.plot(epidemic[:,1], color ="blue", label='Suspectible')
plt.xlim([1,DaysToRunSim])
plt.legend()
plt.show()

