
# encoding=utf-8

# In[107]:

import math
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

#exam = ("我爱你们我是你的我人","爱的就是你","不是你就是我","你的是我的","你们好还是我们好",)

word_dict = {}
word_bond_dict = {}
char_count_dict= {}
total_char_count = 0

alpha = -math.log(0.254)/(7*60*60*24*6)
print "alpha:",alpha

def RemeberCount(count,time):
    return count * math.e**(-alpha*time)
    
#统计所有字字共现的频次
def CollectCharBond(head,tail):  
    if word_bond_dict.has_key(head):
        if not word_bond_dict[head].has_key(tail):
            word_bond_dict[head][tail] = {}
            word_bond_dict[head][tail]["TotalCount"] = 1
	    word_bond_dict[head][tail]["ValidDegree"] = 1
	    word_bond_dict[head][tail]["ValidCount"] = 1
        else:
            word_bond_dict[head][tail]["TotalCount"] += 1
            last = word_bond_dict[head][tail]["LastTime"]
	    ValidDegree = word_bond_dict[head][tail]["ValidDegree"]
	    ValidCount = word_bond_dict[head][tail]["ValidCount"]

            coef = RemeberCount(1,total_char_count-last)
	    ValidDegree = ValidDegree*coef + abs(1-ValidCount*(1-coef))
	    ValidCount = ValidCount*coef + 1

	    word_bond_dict[head][tail]["ValidCount"] = ValidCount
	    word_bond_dict[head][tail]["ValidDegree"] = ValidDegree
    else:
        word_bond_dict[head] = {}
        word_bond_dict[head][tail] = {}
        word_bond_dict[head][tail]["TotalCount"] = 1
	word_bond_dict[head][tail]["ValidDegree"] = 1
	word_bond_dict[head][tail]["ValidCount"] = 1
        
    word_bond_dict[head][tail]["LastTime"] = total_char_count
    
    return 1

#判断是否词边界的函数
def IsWordBond(head,tail,total_count):
    ncount = word_bond_dict[head][tail]["ValidCount"]
    #print "ncount:",ncount
    hcount = char_count_dict[head]
    tcount = char_count_dict[tail]
    #print "hcount:",hcount,"tcount:",tcount
    
    if ncount*total_count < hcount*tcount:
        return True
    else:
        return False

#更新词表的函数
def UpdateDict(word):
    if not word_dict.has_key(word):
        word_dict[word] = {}
        word_dict[word]["TotalCount"] = 1
        word_dict[word]["ValidCount"] = 1
        word_dict[word]["ValidDegree"] = 1
        word_dict[word]["LastTime"] = total_char_count
    else:
        TotalCount = word_dict[word]["TotalCount"]
        ValidCount = word_dict[word]["ValidCount"]
        ValidDegree = word_dict[word]["ValidDegree"]
        LastTime = word_dict[word]["LastTime"]
        
        coef = RemeberCount(1,total_char_count-LastTime)
        TotalCount += 1
        #ValidDegree = ValidDegree*((ValidCount*coef)/(ValidCount*coef+1))+(1-ValidCount*(1-coef))*(1/(ValidCount*coef+1))
        ValidDegree = ValidDegree*coef + abs(1-ValidCount*(1-coef))
	ValidCount = ValidCount*coef + 1
        LastTime = total_char_count
                                                                                                   
        word_dict[word]["TotalCount"] = TotalCount
        word_dict[word]["ValidCount"] = ValidCount
        word_dict[word]["ValidDegree"] = ValidDegree
        word_dict[word]["LastTime"] = total_char_count
        
    return 1

def SumDict(w_dict):
    for w in w_dict.keys():
	TotalCount = word_dict[w]["TotalCount"]
	ValidCount = word_dict[w]["ValidCount"]
	ValidDegree = word_dict[w]["ValidDegree"]
	LastTime = word_dict[w]["LastTime"]

	if(word_dict[w]["ValidCount"] < 1.25):
		word_dict.pop(w)
		continue

	coef = RemeberCount(1,total_char_count-LastTime)
	#ValidDegree = ValidDegree*((ValidCount*coef)/(ValidCount*coef+1))+(1-ValidCount*(1-coef))*(1/(ValidCount*coef+1))
	ValidDegree = ValidDegree*coef + abs(1-ValidCount*(1-coef))
	ValidCount = ValidCount*coef

    	word_dict[w]["ValidCount"] = ValidCount
	word_dict[w]["ValidDegree"] = ValidDegree

    return 1

def CleanDict(w_dict,threshold):
    for w in w_dict.keys():
	if w_dict[w]["ValidDegree"] > threshold:
	    w_dict.pop(w)
	    continue

with open(sys.argv[1],"r") as f:
    for line in f.readlines():
        #print line.strip('\n')
        h = line.decode("utf-8")[0]
        if not char_count_dict.has_key(h):
            char_count_dict[h] = 1
        else:
            char_count_dict[h] += 1
        total_char_count += 1
        w = h
        for i in range(len(line.decode("utf-8"))):
            if 0 == i:
                continue

            total_char_count += 1
            t = line.decode("utf-8")[i]
            #print h,"<->",t
            #统计所有的单字词频
            if not char_count_dict.has_key(t):
                char_count_dict[t] = 1
            else:
                char_count_dict[t] += 1

            #统计所有两个字共现的词频
            CollectCharBond(h,t)

            #判读时候词的边界
            if(IsWordBond(h,t,total_char_count)):
                #print "word:",w
                UpdateDict(w)
                w = t
            else:
                #print "tmp:",w
                w += t

            h = t
       
        if total_char_count % 10000000:
	   print "PROCESSED:",total_char_count
	   SumDict(word_dict)
	   CleanDict(word_dict,2.0)

SumDict(word_dict)


print "Total:",total_char_count

#for k in char_count_dict:
    #print k
    #print k,"-->",char_count_dict[k]
#print "---------"
#for k1 in word_bond_dict:
    #print k1,":",word_bond_dict[k1]
    #for k2 in word_bond_dict[k1]:
        #print k2,"-->",word_bond_dict[k1][k2]["Counter"],"-->",word_bond_dict[k1][k2]["LastTime"]

        
#print "---------"
for w in word_dict:
    if word_dict[w]["ValidDegree"] > 2.0:
       print w,":",word_dict[w]

