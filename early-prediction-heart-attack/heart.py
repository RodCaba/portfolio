#Objective is to predict variable 'target'
#given 5 variables of the heart dataset. 
# It is a binary classification

#-------LOADING LIBRARIES-------
import numpy as np 
import pandas as pd 
import sklearn as sk 
from sklearn.model_selection import train_test_split

#------IMPORTING DATA------------

ml_dataset = pd.read_csv("~\Documents\Saturdays.IA\SAI-E3-HEART\dat\heart.csv", usecols=('age','sex','cp','trestbps','chol','target'))
#Data structure

print('Base data has %i rows and %i columns' % (ml_dataset.shape[0], ml_dataset.shape[1]))
ml_dataset.head(5)

#As we have a matrix with float numbers and no NA's 
#preprocessing is not necessary

#---------CREATION OF TRAIN AND TEST SET----------
#Lets split data

train, test = train_test_split(ml_dataset, test_size=0.2)
print('Train data has %i rows and %i colums' % (train.shape[0], train.shape[1]))
print('Test data has %i rows and %i columns' % (test.shape[0], test.shape[1]))

#-------RESCALING FEATURES---------
#We will scale features using average and standard deviation

rescale_features = {u'trestbps':u'AVGSTD', u'sex':u'AVGSTD',u'age' : u'AVGSTD', u'cp': u'AVGSTD', u'chol' : u'AVGSTD'}
for (feature_name, rescale_method) in rescale_features.items():
    if rescale_method == 'AVGSTD':
        shift = train[feature_name].mean()
        scale = train[feature_name].std()

        print('Rescaled %s' % feature_name)
        train[feature_name] = (train[feature_name] - shift).astype(np.float64) / scale
        test[feature_name] = (test[feature_name] - shift).astype(np.float64) / scale


#Now we are spliting datasets into features and labels
train_x = train.drop('target', axis = 1)
test_x = test.drop('target', axis = 1)

train_y = np.array(train['target'])
test_y = np.array(test['target'])

#-----TRAIN MODEL--------
#We will use gradient booster classifier from sklearn

from sklearn.ensemble import GradientBoostingClassifier
clf = GradientBoostingClassifier(
    random_state = 1337,
    verbose = 0,
    n_estimators = 100,
    learning_rate = 0.1,
    loss = 'deviance',
    max_depth = 3
)

%time clf.fit(train_x, train_y)

#Now that model is trained we can apply to test set

#Predict of the output label
%time _predictions = clf.predict(test_x)

#Predicts probability to belong to class 0 or 1
%time _probas = clf.predict_proba(test_x)

#Format predictions
predictions = pd.Series(data=_predictions, index = test_x.index, name = 'predicted_value')
target_map = {u'1' : 1,u'0' : 0}
cols = [
    u'probability_of_value_%s' % label
    for(_, label) in sorted([(int(target_map[label]), label) for label in target_map])
]
probabilities = pd.DataFrame(data =_probas, index = test_x.index, columns = cols)

#Now we build the scored dataset
results_test = test_x.join(predictions, how = 'left')
results_test = results_test.join(probabilities, how = 'left')
results_test = results_test.join(test['target'], how = 'left')

#Now we measure model accuracy with sklearn metrics
from sklearn.metrics import roc_auc_score
print('AUC value:', roc_auc_score(test_y, probabilities['probability_of_value_1']))

 