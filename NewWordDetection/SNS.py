# encoding:utf-8

import  pandas as pd
import numpy as np
import re

class SNS():

    cut_dict = ["\n","\t","\r","，","。","《","》","（","）","“","”","：","！","？","…","、","——"]
    wordLen = {2:"(..)",3:"(...)",4:"(....)",5:"(.....)",6:"(......)",7:"(.......)",8:"(........)",9:"(.........)",10:"(..........)"}

    def __init__(self,filename,max_len=5,fixed=500,freedom=3):
        self.filename = filename
        self.max_len = max_len
        self.fixed = fixed
        self.freedom = freedom
        self.text = ""

    def getStat(self):
        result = []
        fidd = open("result.txt","w")
        with open(self.filename,"r") as fid:
            self.text = "".join(fid.readlines())
            for i in self.cut_dict:
                self.text = self.text.replace(i, "")
            self.text = self.text.decode("utf-8")
        print "统计词频长度为",len(self.text)
        word = pd.Series(list(self.text)).value_counts() / len(self.text)
        for w in word.index:
            fidd.write(w.encode("utf-8") + "\t" + str(word[w]) + "\n")
        for i in xrange(2,self.max_len+1):
            arr = []
            for k in xrange(i):
                arr = arr + re.findall(self.wordLen[i],self.text[k:])
            rst = pd.Series(arr).value_counts()
            rst = rst[rst>5] / len(arr)
            for r in rst.index:
                fidd.write(r.encode("utf-8")+"\t"+str(rst[r])+"\n")
            word = word.append(rst)
            for kk in xrange(i-1):
                result = result + list(rst[np.array(list(map(lambda ss:rst[ss]/word[ss[kk]]/word[ss[kk+1:]],rst.index))) >= self.fixed].index)
        print "词频统计结束,"
        fidd.close()
        return result

    def entropy(self,result):
        return -np.sum(result * np.log2(result))

    def getResult(self,rst):
        print u'战战兢兢' in rst
        for w in rst:
            temp = re.findall("(.)%s(.)"%w,self.text)
            dw = pd.DataFrame(temp,columns=['left','right'])
            left = dw['left'].value_counts()/len(dw['left'])
            right = dw['right'].value_counts()/len(dw['right'])
            if u'战战兢兢' == w:
                self.entropy(left), self.entropy(right)
            # if min(self.entropy(left),self.entropy(right)) > self.freedom:
            #     print w,self.entropy(left),self.entropy(right)

if __name__ == '__main__':
    filename = "Journey to the West.txt"
    sns = SNS(filename)
    sns.getResult(sns.getStat())