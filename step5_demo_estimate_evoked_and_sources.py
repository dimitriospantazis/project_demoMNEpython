
import mne
import os
import numpy as np
import matplotlib.pyplot as plt
import timeit

#project directories
project_dir = 'F:\\MYPROJECTS16\\project_demoMNEpython'
os.chdir(project_dir)
mne.set_config('SUBJECTS_DIR',os.path.join(project_dir,'recons'))
data_dir = os.path.join(project_dir, 'rawMEGdata')
rawfile = os.path.join(data_dir,'subj04NN_sess01_raw_tsss.fif')
results_dir = os.path.join(project_dir,'results')


## read epochs
epochs = mne.read_epochs('data_tmp\\subj_{}-epo.fif'.format(0), preload=True)


## read noise covariance
noise_cov = mne.read_cov('data_tmp\\subj_{}-noise-cov.fif'.format(0))


## compute evoked response
evoked = epochs[['human/face','animal/face']].average()
evoked.plot()


## plot whitened evoked response
evoked.plot_white(noise_cov,time_unit='s') 


## read forward solution
fwd = mne.read_forward_solution(os.path.join(project_dir,'data_tmp\\subj_{}-fwd.fif'.format(0)))


## inverse operator
# notice loose=0 means orientation constrain normal to the cortex; loose non-zero allows the orientation to vary
inv = mne.minimum_norm.make_inverse_operator(epochs.info, fwd, noise_cov, loose=0.2, depth=0.8)


## compute inverse solution (source time courses)
method = 'MNE'  #“MNE” | “dSPM” | “sLORETA” | “eLORETA”
snr = 3.
lambda2 = 1./snr ** 2
stc, residual = mne.minimum_norm.apply_inverse(evoked, inv, lambda2,
                              method=method, pick_ori=None,
                              return_residual=True, verbose=True)


## plot sources on cortex
vertno_max, time_max = stc.get_peak(hemi='rh')
surfer_kwargs = dict(
    hemi='rh', views='lateral',
    initial_time=time_max, time_unit='s', size=(800, 800), smoothing_steps=10) #for colorbar limits: clim=dict(kind='value', lims=[8, 12, 15])
brain = stc.plot(**surfer_kwargs)
brain.add_text(0.1, 0.9, 'MNE solution', 'title', font_size=14)


## roi analysis
## read labels (regions of interest from the aparc atlas)
subjectname = 'subj04NN'
labels = mne.read_labels_from_annot(subject=subjectname,parc='aparc',hemi='both',surf_name='white',annot_fname=None)
## label time courses (one time course per label)
labels_tc = mne.extract_label_time_course(stcs=stc, labels=labels, src=inv['src'],mode='mean_flip',return_generator=True)
## label time courses (time courses of all vertices within a label)
stc_label = stc.in_label(labels[0])











    