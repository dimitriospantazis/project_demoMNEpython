# Tutorial author: Dimitrios Pantazis

import mne
import os
import numpy as np
import matplotlib.pyplot as plt
import timeit
from mne.preprocessing import ICA, create_ecg_epochs, create_eog_epochs


# Project directories
project_dir = os.getcwd()
mne.set_config('SUBJECTS_DIR',os.path.join(project_dir,'recons'))
data_dir = os.path.join(project_dir, 'rawMEGdata')
rawfile = os.path.join(data_dir,'blink_heartbeat_MEGEEG1_subj14_tsss_mc.fif')
#rawfile = os.path.join(data_dir,'subj04NN_sess01_raw_tsss.fif')
results_dir = os.path.join(project_dir,'results')


## Reject and flat criteria
reject = dict(mag=8000e-15, grad=8000e-13) # T, T/m
flat = dict(mag=1e-15, grad=1e-13)    #T/m


## Read raw file (cropped to speedup demo)
raw = mne.io.read_raw_fif(rawfile, preload=False).crop(tmax=1000)


## Fitting ICA (also see: https://mne.tools/stable/auto_tutorials/preprocessing/40_artifact_correction_ica.html)
filt_raw = raw.copy().load_data().filter(l_freq=1.0, h_freq=None) #before ICA filter data to remove low-frequency drifts that can affect ICA quality because they reduce the independence of the sources. A high-pass filter with 1 Hz cutoff frequency is recommneded
ica = ICA(n_components=30, max_iter="auto", random_state=97)
ica.fit(filt_raw)


# Explained variance of ICA components
explained_var_ratio = ica.get_explained_variance_ratio(filt_raw)
for channel_type, ratio in explained_var_ratio.items():
    print(f"Fraction of {channel_type} variance explained by all components: " f"{ratio}")


# Plot ICA time courses
raw.load_data()
ica.plot_sources(raw, show_scrollbars=False)
#A helpful tip is that right clicking (or control + click with a trackpad) on the name of the component will bring up a plot of its properties.


# Plot topotraphies of ICA components
ica.plot_components()


# Blinks
ica.plot_overlay(raw, exclude=[0], picks="mag")
# heartbeats
ica.plot_overlay(raw, exclude=[1], picks="mag")



ica.plot_properties(raw, picks=[0, 1])


# Exclude ica components
ica.exclude = [0, 1]  # indices chosen based on various plots above


# ica.apply() changes the Raw object in-place, so let's make a copy first:
reconst_raw = raw.copy()
ica.apply(reconst_raw)

raw.plot(show_scrollbars=False)
reconst_raw.plot(show_scrollbars=False)
del reconst_raw



















