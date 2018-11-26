# Instructions to run the program:
# 1. Make sure the CSV file is in the same folder as the program file
# 2. Certain assumptions have been made regarding the positions of the columns. Do not use a different file with different colum structure.
# 3. Second Visualization is generated after closing the first graph window
# 4. A new CSV file is generated after the program is executed with the new columns in the same folder as the program file 

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
x=[]
y=[]
# Data is read from file
data = pd.read_csv('AssignmentData.csv')

# Appending pC column and pKC for each KC and initializing them with value -1
temp = pd.DataFrame(np.zeros(((len(data)))), columns=['pC'])
data = data.join(temp)
temp = np.empty(((len(data)), 7))
temp[:] = -1
temp = pd.DataFrame(temp, columns=['pKC_1', 'pKC_27', 'pKC_24', 'pKC_14', 'pKC_22', 'pKC_20', 'pKC_21'])
data = data.join(temp)

#Values of the parameters
pInit = 0.5
pTransit = 0.1 
pSlip = 0.1
pGuess = 0.1
threshold = 0.6
#List of unique students based on Student column
students = data.Student.unique()

#For each student, obtain steps for each KC seperately and loop through each KC to calculate pC and pKC for each step for that KC
for student in students:
    pLNext = pInit
    studentData = data[data.Student==student]
    kc = []
    kc.append(studentData.loc[studentData.KC_1==1])
    kc.append(studentData.loc[studentData.KC_27==1])
    kc.append(studentData.loc[studentData.KC_24==1])
    kc.append(studentData.loc[studentData.KC_14==1])
    kc.append(studentData.loc[studentData.KC_22==1])
    kc.append(studentData.loc[studentData.KC_20==1])
    kc.append(studentData.loc[studentData.KC_21==1])
    for i in range(len(kc)):
        pLNext = pInit
        for index, row in kc[i].iterrows():
            if(row.Correct==1):
                pLNext =  (pLNext*(1-pSlip))/((pLNext*(1-pSlip))+((1-pLNext)*pGuess))
            else:
                pLNext =  (pLNext*(pSlip))/((pLNext*(pSlip))+((1-pLNext)*(1-pGuess)))
            
            pLNext = pLNext + ((1-pLNext)*pTransit)
            pC = (pLNext*(1-pSlip))+((1-pLNext)*pGuess)
            
            #Updating the respective pKC and pC values in main data 
            data.iat[index, 10] = pC
            data.iat[index, 11+i] = (0,1)[pC>threshold]

#creating a new CSV file with necessary data
data.to_csv('output.csv', index=False)
cols = data.columns.values.tolist()
cols = data.columns.values.tolist()
accuracy = []
correctTotal=0
totalTotal = 0
for i in range(7):
    correct = len(data[(data[cols[2]]==1) & (data[cols[3+i]]==1) & (data[cols[11+i]]==1)]) + len(data[(data[cols[2]]==0) & (data[cols[3+i]]==1) & (data[cols[11+i]]==0)])
    correctTotal += correct
    total =  len(data[(data[cols[3+i]]==1) & ((data[cols[2]]==1) | (data[cols[2]]==0))])
    totalTotal += total 
    accuracy.append(correct/total)

plt.plot(cols[3:10], accuracy, label=str(correctTotal/totalTotal))
plt.xlabel('Knowledge Components')
plt.ylabel('Accuracy')
plt.ylim(ymax=1.0, ymin=0.8)
plt.legend()
plt.show()