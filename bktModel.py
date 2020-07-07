# Instructions to run the program:
# 1. Make sure the CSV file is in the same folder as the program file
# 2. Certain assumptions have been made regarding the positions of the columns. Do not use a different file with different colum structure.
# 3. A new CSV file is generated after the program is executed with the new columns in the same folder as the program file 

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
x=[]
y=[]
# Data is read from file    # 导入数据
data = pd.read_csv('AssignmentData.csv')

# Appending pC column and pKC for each KC and initializing them with value -1   # 为每个KC附加pC列和pKC，并使用值-1初始化它们
temp = pd.DataFrame(np.zeros(((len(data)))), columns=['pC'])
data = data.join(temp)
temp = np.empty(((len(data)), 7))   # kc知识组件有7个用0和1表示，加上前面做题correct正确性表示，其他的为学生id和做题步骤
temp[:] = -1    # 初始化-1
temp = pd.DataFrame(temp, columns=['pKC_1', 'pKC_27', 'pKC_24', 'pKC_14', 'pKC_22', 'pKC_20', 'pKC_21'])    # 加上这些知识组件的行，也就是第一行
data = data.join(temp)

#Values of the parameters   # 参数赋值
pInit = 0.5     # 初始0.5
pTransit = 0.1  
pSlip = 0.1
pGuess = 0.1
threshold = 0.6     # 阈值0.6
#List of unique students based on Student column    # 基于学生特殊性的列
students = data.Student.unique()

#For each student, obtain steps for each KC seperately and loop through each KC to calculate pC and pKC for each step for that KC   #对于每一个学生，每一步循环kc去计算pc和pkc
for student in students:
    pLNext = pInit
    studentData = data[data.Student==student]
    kc = []
    kc.append(studentData.loc[studentData.KC_1==1])     # .loc[]选择行的数据 具体用法里面是0则为第一行数据，里面是6，则是选择行标为6也就是第七行数据，同时也可以切片选择，
    kc.append(studentData.loc[studentData.KC_27==1])    # 会返回最后标号代表的数据
    kc.append(studentData.loc[studentData.KC_24==1])
    kc.append(studentData.loc[studentData.KC_14==1])
    kc.append(studentData.loc[studentData.KC_22==1])
    kc.append(studentData.loc[studentData.KC_20==1])
    kc.append(studentData.loc[studentData.KC_21==1])
    for i in range(len(kc)):
        pLNext = pInit
        for index, row in kc[i].iterrows():
            if(row.Correct==1):     # 如果做题正确进行下面的计算
                pLNext =  (pLNext*(1-pSlip))/((pLNext*(1-pSlip))+((1-pLNext)*pGuess))
            else:
                pLNext =  (pLNext*(pSlip))/((pLNext*(pSlip))+((1-pLNext)*(1-pGuess)))
            
            pLNext = pLNext + ((1-pLNext)*pTransit)
            pC = (pLNext*(1-pSlip))+((1-pLNext)*pGuess)
            
            #Updating the respective pKC and pC values in main data     # 在主数据中更新pkc和pc的值
            data.iat[index, 10] = pC
            data.iat[index, 11+i] = (0,1)[pC>threshold]     # pc的值大于阈值0.6

#creating a new CSV file with necessary data    # 建立新的csv
data.to_csv('output.csv', index=False)
cols = data.columns.values.tolist()     # python中list差不多
cols = data.columns.values.tolist()
accuracy = []
correctTotal=0
totalTotal = 0
for i in range(7):
    correct = len(data[(data[cols[2]]==1) & (data[cols[3+i]]==1) & (data[cols[11+i]]==1)]) + len(data[(data[cols[2]]==0) & (data[cols[3+i]]==1) & (data[cols[11+i]]==0)])
    correctTotal += correct     # 总的正确率为每一个correct的累加
    total =  len(data[(data[cols[3+i]]==1) & ((data[cols[2]]==1) | (data[cols[2]]==0))])
    totalTotal += total         
    accuracy.append(correct/total)

plt.plot(cols[3:10], accuracy, label=str(correctTotal/totalTotal))      # 横纵坐标以及可视化
plt.xlabel('Knowledge Components')      # 知识成分
plt.ylabel('Accuracy')
plt.ylim(ymax=1.0, ymin=0.8)
plt.legend()
plt.show()  
