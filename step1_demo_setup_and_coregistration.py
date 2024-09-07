# Tutorial author: Dimitrios Pantazis

# First run these in freesurfer (After mne installation, mne is a command in linux)
# mne watershed_bem -s mysubject
# mne make_scalp_surfaces -s mysubject

import mne
import os

# Define directories
project_dir = os.getcwd()
data_dir = os.path.join(project_dir, 'rawMEGdata')

# Define subject_dir
mne.set_config('SUBJECTS_DIR',os.path.join(project_dir,'recons'))
mne.datasets.fetch_fsaverage() #ensure fsaverage src exists

# Coregister data with anatomy (see subject_coregistration.doc for instructions)
subject='subj04NN'
rawfile = os.path.join(data_dir,'subj04NN_sess01_raw_tsss.fif')
mne.gui.coregistration(subject=subject,inst=rawfile)

# Visualize registration (optional)
raw = mne.io.read_raw_fif(rawfile)
trans = os.path.join(data_dir,'subj04NN-trans.fif') #this is the output of coregistration function
mne.viz.plot_alignment(raw.info,trans=trans,subject='subj04NN',dig=True,surfaces=['head-dense', 'white'], coord_frame='meg')





