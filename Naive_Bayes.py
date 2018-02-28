

import csv
import math

'''--------------------------------------Break data set into training and testinig---------------------------------------------------------------------'''

with open("agaricus-lepiota.data", "r") as csvfile:
    lines = csv.reader(csvfile)
    dataset = list(lines)
   
    feature_prob = {}
    training = []
    testing = []
    for x in range(len(dataset)):
        if dataset[x][11]!="?":
            if x<=4000:
                training.append(dataset[x])
            else:
                testing.append(dataset[x])
    

feature_value = {}    

print("Training set: "+repr(len(training)))
print("Testing set: "+repr(len(testing)))

'''------------------------Calculate P(feature instance) for all features------------------------------------------------------------------------------'''

for y in range(len(dataset[0])):
 
    for x in range(len(training)):
    	dummy = dataset[x][y]
    	if dummy in feature_value:
    		feature_value[dummy] = feature_value[dummy] + 1
    	else:
    		feature_value[dummy] = 0
        

    feature_prob[y]=feature_value
    feature_value = {}

'''------------------Calculate P(feature instance with respect to sample being edible) for all features------------------------------------------------------------------------------'''

prob_wrt_sample = {}
feature_value = {}
for y in range(len(dataset[0])):
    


    for x in range(len(training)):
    	dummy = dataset[x][y]
    	if dummy in feature_value and dataset[x][0]=='e':
            feature_value[dummy] += 1
    	elif dummy not in feature_value:
            if dataset[x][0]=='e':
                feature_value[dummy] = 1
            if dataset[x][0]!='e':
                feature_value[dummy] = 0
              

    for key , value in feature_value.items():
        feature_value[key] = value/(feature_prob[0]['e'])
 
    prob_wrt_sample[y]=feature_value
    feature_value = {}
    

'''--------------Calculate P(test is edible) using bayes theorm P(A│B)=(P(B│A)*P(A))/(P(B))   --------------------------------------------------------------------------------------'''
Ans = 1
Ans1 = 1 
predicted_edibal = Actual_edibal = predicted_poison = Actual_poison = 0 
TP = TN = FP = FN = 0
for xyx in range(len(testing)):
    test = testing[xyx]

    for x in range(len(test)):
        if x > 1:
       
            
            yyx = 0
            #.................To compensate for the missing features in training set.................................
            for key , value in feature_prob[x].items():
                if key == test[x]:
                    yyx = 1
                
            if yyx != 0 and feature_prob[x][test[x]] != 0:
                    Ans = Ans * (math.ceil(prob_wrt_sample[x][test[x]]*1000)/1000)/(math.ceil((feature_prob[x][test[x]]/4000)*1000)/1000)
            else:
                Ans = 0 
                #Ans = Ans * 1/len(training)  #....least prob
    
    Ans = Ans * (feature_prob[0][test[0]]/len(training)) 
    #print(Ans)
    
    if "p" == test[0]:     
        Actual_poison = Actual_poison+1
        if Ans < 0.5:     
            TN = TN + 1
    else:    
        Actual_edibal = Actual_edibal+1
        if Ans >= 0.5:     
            TP = TP + 1
            
    FN = Actual_edibal - TP
    FP = Actual_poison - TN
    
    if Ans < 0.5:
            predicted_poison = predicted_poison+1
    else:
            predicted_edibal = predicted_edibal+1
    
    Ans=1
print(Actual_edibal)
print(Actual_poison)
print("")    
print("Function accuracy")
#print((((predicted_edibal/Actual_edibal)*100)+((predicted_poison/Actual_poison)*100))/2)
print(((TP + TN)/(TP + TN + FP + FN))*100)
print("Function error")
print(((FP + FN)/(TP + TN + FP + FN))*100)

print("")
print("Confussion Matix")
print("          e  "+" | "+"  p   ")
print("       ----------------")
print("    e      "+repr(TP) +" | "+repr(FP))
print("       ----------------")
print("    p      "+repr(FN) +" | "+repr(TN))
print("       ----------------")
