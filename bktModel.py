import pandas as pd
import numpy as np

data = pd.read_csv('AssignmentData.csv')
temp = pd.DataFrame(np.zeros(((len(data)))), columns=['pC'])
data = data.join(temp)
temp = np.empty(((len(data)), 7))
temp[:] = -1
temp = pd.DataFrame(temp, columns=['pKC_1', 'pKC_27', 'pKC_24', 'pKC_14', 'pKC_22', 'pKC_20', 'pKC_21'])
data = data.join(temp)
pInit = 0.5
pTransit = 0.1 
pSlip = 0.1
pGuess = 0.1
threshold = 0.6

students = data.Student.unique()
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
            data.iat[index, 10] = pC
            data.iat[index, 11+i] = (0,1)[pC>threshold]

data.to_csv('output.csv', index=False)
