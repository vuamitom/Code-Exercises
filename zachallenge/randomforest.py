from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import pickle
import numpy as np
import datetime
import common

def random_forest(train_input, train_labels, test_input, test_labels):
    # Out-of-bag score estimate: 0.571
    # Mean accuracy score: 0.597
    v_c = train_input.shape[0]
    t_c = test_input.shape[0]
    rf = RandomForestClassifier(n_estimators=100, oob_score=True, random_state=123456)
    start_time = datetime.datetime.now()
    rf.fit(train_input.reshape(v_c, -1), train_labels)
    print ('done training in seconds: ', (datetime.datetime.now() - start_time).total_seconds())
    start_time = datetime.datetime.now()
    predicted = rf.predict(test_input.reshape(t_c, -1))
    print ('done predict in seconds: ', (datetime.datetime.now() - start_time).total_seconds())
    accuracy = accuracy_score(test_labels, predicted)
    print(f'Out-of-bag score estimate: {rf.oob_score_:.3}')
    print(f'Mean accuracy score: {accuracy:.3}')


if __name__ == '__main__':
    train_input, train_labels, test_input, test_labels = common.get_accent_data()
    # print (test_labels)
    random_forest(train_input, train_labels, test_input, test_labels)