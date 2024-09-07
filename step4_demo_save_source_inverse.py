
import mne
import os
import numpy as np
import matplotlib.pyplot as plt
import timeit

# Project directories
project_dir = 'F:\\MYPROJECTS16\\project_demoMNEpython'
os.chdir(project_dir)
mne.set_config('SUBJECTS_DIR',os.path.join(project_dir,'recons'))
data_dir = os.path.join(project_dir, 'rawMEGdata')
rawfile = os.path.join(data_dir,'subj04NN_sess01_raw_tsss.fif')
results_dir = os.path.join(project_dir,'results')


## Read epochs
epochs = mne.read_epochs('data_tmp\\subj_{}-epo.fif'.format(0), preload=True)


## Read noise covariance
noise_cov = mne.read_cov('data_tmp\\subj_{}-noise-cov.fif'.format(0))


## Setup source space (computes a downsampled surface on white matter)
subjectname = 'subj04NN'
src = mne.setup_source_space(subject=subjectname, spacing='oct6', add_dist='patch')
# mne.viz.plot_bem(subject=subjectname, brain_surfaces='white', src=src,orientation='coronal')
mne.write_source_spaces('data_tmp\\subj_{}-src.fif'.format(0), src, overwrite=True)


## For volume-based source space
#surface = os.path.join('recons',subjectname,'bem','inner_skull.surf')
#vol_src = mne.setup_volume_source_space(subject=subjectname,surface=surface)
#mne.viz.plot_bem(subject=subjectname, brain_surfaces='white', src=vol_src, orientation='coronal')


## Link to tranformation file (registration of MEG - MRI anatomy)
trans = os.path.join(os.path.join(data_dir,subjectname + '-trans.fif'))


## Visualize source space
fig = mne.viz.plot_alignment(trans=trans, subject=subjectname, surfaces='white', coord_frame='head', src=src)
mne.viz.set_3d_view(fig, azimuth=173.78, elevation=101.75,
                    distance=0.30, focalpoint=(-0.03, 0.02, 0.05))


## Compute forward solution
conductivity = (0.3,)  # for single layer
# conductivity = (0.3, 0.006, 0.3)  # for three layers for EEG
model = mne.make_bem_model(subject=subjectname, ico=5, conductivity=conductivity)
bem = mne.make_bem_solution(model)


## Forward model
fwd = mne.make_forward_solution(epochs.info, trans=trans, src=src, bem=bem,
                                        meg=True, eeg=False, mindist=5.0, n_jobs=1)
mne.write_forward_solution(os.path.join(project_dir,'data_tmp\\subj_{}-fwd.fif'.format(0)), fwd, overwrite=True)


## Inverse operator
# notice loose=0 means orientation constrain normal to the cortex; loose non-zero allows the orientation to vary
inv = mne.minimum_norm.make_inverse_operator(epochs.info, fwd, noise_cov, loose=0.2, depth=0.8)
mne.minimum_norm.write_inverse_operator('data_tmp\\subj{}-inv.fif'.format(0), inv)







    