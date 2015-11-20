from __future__ import division
from sklearn.cross_validation import train_test_split
from sklearn.metrics import confusion_matrix
from numpy.random import RandomState
import numpy as np
import matplotlib.pyplot as plt
from sklearn import tree
import os


# Evaluate classifier
def clf_evaluate(clf, features, labels,max_iter=10):
    rs = RandomState()
    cm = [[0,0],[0,0]]
    for i in range(max_iter):
        X_train, X_test, y_train, y_test = train_test_split(features, labels,random_state=rs)
        y_pred = clf.fit(X_train, y_train).predict(X_test)       
        cm = cm + confusion_matrix(y_test, y_pred)

    recall = cm[1][1] / (cm[1][1] + cm[1][0])
    precision = cm[1][1] / (cm[1][1] + cm[0][1])
    accuracy = (cm[0][0] + cm[1][1]) / (cm[0][0] + cm[0][1] + cm[1][0] + cm[1][1])

    print "**********************************"
    print "Recall:", recall * 100, '%'
    print "Precision:", precision * 100, '%'
    print "Accuracy:", accuracy * 100, '%'
    print "**********************************"
    return cm

# Evaluate regression estimator
def reg_evaluate(clf, features, labels,max_iter=10):
    rs = RandomState()
    diffs = []
    for i in range(max_iter):
        X_train, X_test, y_train, y_test = train_test_split(features, labels,random_state=rs)
        y_pred = clf.fit(X_train, y_train).predict(X_test)       

        
        y_pred = clf.predict(X_test)
        for idx in range(len(y_pred)):    
            d = abs(y_pred[idx] - y_test[idx])
            diffs.append(d)
    avg_diff = sum(diffs)/len(diffs)
    print avg_diff
    return diffs
    

# Create a plot of the confusion matrix
def plot_confusion_matrix(cm):
    cm_normalized = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
    plt.matshow(cm_normalized)
    width = len(cm)
    height = len(cm[0])
    for x in xrange(width):
        for y in xrange(height):
            plt.gca().annotate("{:5.2f} %".format(cm_normalized[x][y]), xy=(y, x), 
                        horizontalalignment='center',
                        verticalalignment='center')

    tick_labels = ['Fail','Success']
    plt.xticks(range(width), tick_labels)
    plt.yticks(range(height), tick_labels)
    plt.title('Normalized confusion matrix')
    plt.colorbar()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')
    plt.show()

    
# Create a plot of the decision tree
def plot_tree(clf,feature_names):
    tree.export_graphviz(clf,out_file='tree.dot',class_names=['Fail','Success'],feature_names=feature_names)
    os.system("dot -Tpng tree.dot -o tree.png")
    os.system("tree.png")
