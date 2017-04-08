
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.svm import LinearSVC, SVC
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.multiclass import OneVsRestClassifier
from sklearn.metrics import zero_one_loss
import sklearn
from sklearn.feature_extraction import DictVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer

__version__ = "1.0"
__license__ = "IISc"
__author__ = "Sachin Nagargoje"
__author_email__ = "nagargoje.sachin@gmail.com"

def fileRead(path):
    f = open(path, mode='r')
    lines = f.readlines()
    f.close()
    return lines

# Fetches the JDs from the list and maps it to its labels
def extractData(dataList, txtList, txtLabels, labelList, fpath):

    for lines in dataList:
        txtlist1 = lines.split(',')
        #txtlist1.remove('\n')
        text = " ".join(fileRead(fpath+txtlist1[0]))
        t=[]
        i=1
        j =len(txtlist1)
        while i<j:
            if txtlist1[i] not in ['', '\n','\r\n']:
                    if txtlist1[i] not in labelList:
                            labelList.append(txtlist1[i])
                    t.append(labelList.index(txtlist1[i]))
            i = i+1
        txtLabels.append(t)
        txtList.append(text)

def getData(filepath, txtList, txtLabels, labelList, fpath):
    f=fileRead(filepath)
    first=1
    for lines in f:
        if first == 1:
            first =0
            continue
        # print("*********")
        list1 = lines.split('\t')
        # print (list1[0])
        text = "".join(list1[1])
        txtlist1 = list1[0].split(" ")
        t = []
        i = 0
        j = len(txtlist1)
        while i < j:
            if txtlist1[i] not in ['', '\n', '\r\n']:
                if txtlist1[i] not in labelList:
                    labelList.append(txtlist1[i])
                t.append(labelList.index(txtlist1[i]))
                # print(txtlist1[i])
            i = i + 1
        # print('len of t:',len(t))
        # if len(text) == 0:
        #     print("&&((&&&&&&&&&&&&&&&&&&&&&&")
        if len(t) !=  0 and len(text) > 0:
            txtLabels.append(t)
            txtList.append(text)
            # print(text)
            # print("\n")


# Trains a Multi-Label classifier and generates a report on its predictions
def Classify(txtList, txtLabels, fileName, labelList):
    from sklearn.preprocessing import MultiLabelBinarizer
    txtLabels = MultiLabelBinarizer().fit_transform(txtLabels)
    test=1
    if test==0:
        x_train = np.array(txtList[0:2000])
        y_train = np.array(txtLabels[0:2000])
        x_test = np.array(txtList[2001:])
        y_test = np.array(txtLabels[2001:])
    else:
        x_train = txtList #np.array(txtList[0:2000])
        y_train = txtLabels #np.array(txtLabels[0:2000])
        f = fileRead("indeed_ml_dataset/test.tsv")
        x_test = []
        first =1
        for lines in f:
            if first == 1:
                first = 0
                continue
            x_test.append(lines)
    #, norm=u'l2'
    classifier = Pipeline([
        ('vectorizer', TfidfVectorizer(max_df=0.6, min_df=1, sublinear_tf=True, binary=True, strip_accents='unicode', decode_error='replace', analyzer='word',ngram_range=(1, 5),smooth_idf=False, norm=u'l2')),
        ('tfidf', TfidfTransformer( use_idf=False, smooth_idf=True, sublinear_tf=True)),
        ('clf', OneVsRestClassifier(LinearSVC()))]) #SVC(kernel='linear')
    classifier.fit(x_train, y_train)
    predicted = classifier.predict(x_test)

    if test ==0:
        f = open(fileName, 'w')
        f.writelines(sklearn.metrics.classification_report(y_test, predicted, target_names=labelList))
        f.write('\nNumber of Labels:' + str(len(labelList)))
        f.write('\nhamming loss : ' + str(sklearn.metrics.hamming_loss(y_test, predicted)))
        f.write('\nf-beta(beta=0.5 - biased towards Precision) : ' + str(
            sklearn.metrics.fbeta_score(y_test, predicted, average='weighted', beta=0.5)))
        f.write('\nzero-loss:' + str(zero_one_loss(y_test, predicted)))
        f.write('\nAccuracy score:' + str(sklearn.metrics.accuracy_score(y_test, predicted)))
        f.close()

        f = open("out.csv", 'w')
        f.write("tags\n")
        for i in range(len(y_test)):
            print(str(i))
            arr = predicted[i]
            arry = y_test[i]
            if len(arr) == 0:
                f.write('\n')
            else:
                p = 0
                for j in range(len(arr)):
                    print(arr[j], end=" ")
                    if arr[j] == 1:
                        p = 1
                        f.write(labelList[j] + " ")
                f.write('\n')
                if p == 0:
                    f.write('\n')
                print()
                for j in range(len(arry)):
                    print(arry[j], end=" ")
                print()
    else:
        f = open("test_out.tsv", 'w')
        f.write("tags\n")
        for i in range(len(x_test)):
            # print(str(i))
            arr = predicted[i]
            # arry = y_test[i]
            if len(arr) == 0:
                f.write('\n')
            else:
                p = 0
                ans=''
                for j in range(len(arr)):
                    print(arr[j], end=" ")
                    if arr[j] == 1:
                        p = 1
                        ans=ans+labelList[j]+' '
                        # f.write(labelList[j] + " ")
                f.write(ans.strip())
                f.write('\n')
                print()
                print(ans.strip())
                print()

def main():
    path1="indeed_ml_dataset"
    filepath="indeed_ml_dataset/train.tsv"
    dataList = []
    labelList = []
    txtList = []
    txtLabels = []
    getData(filepath,txtList,txtLabels,labelList,path1)
    print(labelList)
    print(txtLabels)
    fileName = 'results.txt'
    print("len of train data: ",len(txtList))
    Classify(txtList, txtLabels, fileName, labelList)
    print('\a')

if __name__ == "__main__":
    main()