
import mne
import os
import numpy as np
import matplotlib.pyplot as plt
import timeit
import pickle

from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn import svm
from sklearn.linear_model import LogisticRegression
from mne.decoding import SlidingEstimator, GeneralizingEstimator, Scaler, cross_val_multiscore, LinearModel, get_coef, Vectorizer, CSP


## read epochs
epochs = mne.read_epochs('data_tmp\\subj_{}-epo.fif'.format(0), preload=True)


## contrasts for decoding
contrast = {}
contrast[0] = ['animate', 'inanimate']
contrast[1] = ['face', 'body']
contrast[2] = ['male', 'female']
contrast[3] = ['natural', 'artificial']
contrast[4] = ['human/face', 'animal/face']
contrast[5] = ['human/body', 'animal/body']


## design classifier
clf = make_pipeline(StandardScaler(), svm.SVC(kernel='linear', C=1))
time_decod = SlidingEstimator(clf, n_jobs=24, scoring='roc_auc', verbose=True)


## run decoding (time-resolved, i.e. separate classifier per time point)
c=4 # select contrast
X1 = epochs[contrast[c][0]].get_data(picks='meg').copy()
X2 = epochs[contrast[c][1]].get_data(picks='meg').copy()
X = np.concatenate((X1, X2), axis=0)
y1 = ['labelA'] * X1.shape[0]
y2 = ['labelB'] * X2.shape[0]
y = y1 + y2
starttime = timeit.default_timer()
scores = cross_val_multiscore(time_decod, X, y, cv=5, n_jobs=1)  # cross validated decoding (n_jobs is equal to folds; does not help with more)
print('Processing time for decoding: {:.2f} sec'.format(timeit.default_timer() - starttime))
Scores = np.mean(scores, axis=0)  # Mean scores across cross-validation splits


## plot decoding time course
fig, ax = plt.subplots()
ax.plot(epochs.times, Scores, linewidth=2)
ax.axhline(.5, color='k', linestyle='--')
ax.set_xlabel('Time (s)')
ax.set_ylabel('AUC')  # Area Under the Curve
ax.legend()
ax.axvline(.0, color='k', linestyle='-')
ax.set_title(f'Decoding {contrast[4]}')



## compute patterns of decoding (see https://doi.org/10.1016/j.neuroimage.2013.10.067)
clf = make_pipeline(StandardScaler(), LinearModel(svm.SVC(kernel='linear', C=1)))  # notice the use of LinearModel to get the activation patterns
time_decod = SlidingEstimator(clf, n_jobs=24, scoring='roc_auc', verbose=True)
time_decod.fit(X, y) #fit the estimator to all data, no crossvalidation needed for patterns
coef = get_coef(time_decod, 'patterns_', inverse_transform=True)
epochs_tmp = epochs[0].pick_types(meg=True) #create a tmp epoch with only MEG sensors
evoked_patterns = mne.EvokedArray(coef, epochs_tmp.info, tmin=epochs.times[0])
joint_kwargs = dict(ts_args=dict(time_unit='s'), topomap_args=dict(time_unit='s'))
h = evoked_patterns.plot_joint(times=np.arange(.100, .200, .07), title=' ', picks='mag', **joint_kwargs)


## temporal generalization of decoding (GeneralizingEstimator) -------------------------------
clf = make_pipeline(StandardScaler(), svm.SVC(kernel='linear', C=1))
gen_decod = GeneralizingEstimator(clf, n_jobs=25, scoring='roc_auc', verbose=True)  # n_jobs=32 for maximum?
starttime = timeit.default_timer()
scores = cross_val_multiscore(gen_decod, X, y, cv=5, n_jobs=1)  # cross validated decoding (n_jobs is equal to folds; does not help with more)
print('Processing time for decoding: {:.2f} sec'.format(timeit.default_timer() - starttime))
Scores = np.mean(scores, axis=0)  # Mean scores across cross-validation splits


## plot temporal generalization decoding
fig, ax = plt.subplots()
im = ax.imshow(Scores, interpolation='lanczos', origin='lower', cmap='RdBu_r', extent=epochs.times[[0, -1, 0, -1]])













