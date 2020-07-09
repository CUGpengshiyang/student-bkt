import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
x=[]
y=[]
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

#Calculating accuracy for each value of pTransit and incrementing it    # 计算pTransit每个值的精度并递增
for pTransit in np.arange(0.1, 0.8, 0.1):       # 进行循环
    students = data.Student.unique()
    for student in students:
        pLNext = pInit
        studentData = data[data.Student==student]
        kc = []
        kc.append(studentData.loc[studentData.KC_1==1])     # 添加知识成分的行的数据
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
    # data.to_csv('output.csv', index=False)        # 新建csv
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

    plt.plot(cols[3:10], accuracy, label=str(pTransit))     # 标签为转移概率
    plt.xlabel('Knowledge Components')                      # x为知识成分
    plt.ylabel('Accuracy')                                  # y为精度
    plt.ylim(ymax=0.93, ymin=0.84)
    plt.legend()

    x.append(str(pTransit))
    y.append(correctTotal/totalTotal)                       # 总的正确率/总数量

#Visualize the accuracy w.r.t different pTransit values     # 可视化精度在不同的pTransit下
plt.show()

plt.plot(x, y)
plt.xlabel('Threshold')
plt.ylabel('Accuracy')
plt.ylim(ymax=0.92, ymin=0.82)

plt.show()
