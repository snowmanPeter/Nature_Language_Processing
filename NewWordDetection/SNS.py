# encoding:utf-8

import  pandas as pd
import numpy as np
import re

class SNS():

    cut_dict = ["\n","\t","\r","，","。","《","》","（","）","“","”","：","！","？","…","、"]
    wordLen = {2:"(..)",3:"(...)",4:"(....)",5:"(.....)"}
    rem = {1:"(.)%s",2:"{0}%s"}

    def __init__(self,filename,max_len=5,fixed=2000,freedom=6):
        self.filename = filename
        self.max_len = max_len
        self.fixed = fixed
        self.freedom = freedom
        self.text = ""

    def getStat(self):
        result = []
        with open(self.filename,"r") as fid:
            self.text = "".join(fid.readlines())
            for i in self.cut_dict:
                self.text = self.text.replace(i, "")
            self.text = self.text.decode("utf-8")
        print "统计词频长度为",len(self.text)
        word = pd.Series(list(self.text)).value_counts() / len(self.text)
        print len(word)
        for i in xrange(2,self.max_len+1):
            arr = []
            for k in xrange(i):
                arr = arr + re.findall(self.wordLen[i],self.text[k:])
            rst = pd.Series(arr).value_counts()
            rst = rst[rst>10]
            word = word.append(rst / len(arr))
            for kk in xrange(i-1):
                result = result + list(rst[np.array(list(map(lambda ss:rst[ss]/word[ss[kk]]/word[ss[kk+1:]],rst.index))) >= self.fixed].index)
        print "词频统计结束,"
        return result

    def getResult(self,rst):
        for w in rst:
            entropy = []
            for i in range(1,3):
                temp = re.findall("(.)%s"%w,self.text)
                jiegu = np.array(pd.Series(temp).value_counts()/len(temp))
                entropy.append(-np.sum(jiegu*np.log2(jiegu)))
            if min(entropy) >= self.freedom:
                print w



if __name__ == '__main__':
    filename = "Journey to the West.txt"
    sns = SNS(filename)
    sns.getResult(sns.getStat())