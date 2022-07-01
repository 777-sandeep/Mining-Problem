#!/usr/bin/env python
# coding: utf-8

# In[48]:


import pandas as p
import pulp
from pulp import *
import math
import numpy


# In[49]:


# Defining Sense of Model
model = LpProblem(name = "Mining_Problem" , sense = LpMaximize)


# In[50]:


M = range(4)
Y = range(5)
Royalty = [5,4,4,5]
Limit = [2,2.5,1.3,3]
Quality = [1,0.7,1.5,0.5]
Quality_Target = [0.9,0.8,1.2,0.6,1]


# In[51]:


# Following variable takes value 1 Mine i is operating in year j and 0 otherwise
#var O{M,Y} binary;                    
O = LpVariable.dicts('O', ((i, j) for i in M for j in Y), lowBound=0, upBound=1, cat='Binary')

#Outputs produced in Mine i in year j
q = LpVariable.dicts('q', ((i,j) for i in M for j in Y), lowBound=0, upBound=3, cat='Continuous')

# Following variable takes value takes value 1 if royalties are payable in year j for Mine i
r = LpVariable.dicts('r', ((i, j) for i in M for j in Y), lowBound=0, upBound=1, cat='Binary')


# In[52]:


# Objective Fuction
model += lpSum(q[i,j]*10*(0.9**(j)) - Royalty[i]*r[i,j]*(0.9**(j)) for i in M for j in Y)


# In[53]:


# Constraints

for j in Y:
    #Can operate at most 3 mines
    model += lpSum(O[i,j] for i in M ) <= 3
    #blended output ore should have exactly the stipulated quality
    model += lpSum(q[i,j]*(Quality[i] - Quality_Target[j]) for i in M ) == 0
    
    for i in M:
        #If Mine is not working there can not be any output & if it is working the maximum should be less than the Limit
        model += q[i,j] <= O[i,j]*Limit[i]
        #If mine is woring then Royalties has to be paid
        model += r[i,j] >= O[i,j]
        
        
for j in range(1,4):
    for i in M:
        #Royalties has to be paid if mine was working in past & need to be working in future
        model += r[i,j] >= r[i,j-1]+r[i,j+1]-1
        #Royalties needed to be paid in first & last year (year 5) year only if it is working
        model += r[i,0] == O[i,0]
        model += r[i,4] == O[i,4]   


# In[54]:


# Solution 
model.solve()
print(f"status: {model.status}, {LpStatus[model.status]}")


# In[55]:


# Objective Value
print(f"objective: {model.objective.value()}")


# In[56]:


# PRODUCTS of each type
for v in model.variables():
    print(f"{v.name}: {v.value()}")


# In[ ]:





# In[ ]:




