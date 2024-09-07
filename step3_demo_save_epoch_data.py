
import mne
import os
import numpy as np
import matplotlib.pyplot as plt
import timeit
from mne.preprocessing import ICA, create_ecg_epochs, create_eog_epochs


# Project directories
project_dir = 'F:\\MYPROJECTS16\\project_demoMNEpython'
mne.set_config('SUBJECTS_DIR',os.path.join(project_dir,'recons'))
data_dir = os.path.join(project_dir, 'rawMEGdata')
rawfile = os.path.join(data_dir,'subj04NN_sess01_raw_tsss.fif')
results_dir = os.path.join(project_dir,'results')

## Reject and flat criteria
reject = dict(mag=8000e-15, grad=8000e-13) # T, T/m
flat = dict(mag=1e-15, grad=1e-13)    #T/m


## Read raw file (cropped to speedup demo, keeps the first 1000 seconds)
raw = mne.io.read_raw_fif(rawfile, preload=False).crop(tmax=1000)


## Load events (use min_duration to avoid spurius events from the MEGIN device)
events = mne.find_events(raw, stim_channel='STI101',min_duration=0.002)
#raw.plot(events=events)


## Find eog (blink) projectors (EOG sensor not available, but MEG1411 is effective!)
eog_projs,eog_events = mne.preprocessing.compute_proj_eog(raw,ch_name='MEG1411',n_grad=1,n_mag=1,reject=reject,flat=flat)
raw.add_proj(eog_projs)
mne.viz.plot_projs_topomap(eog_projs,info=raw.info)
#plot in separate window to save figure 
%matplotlib qt 
h = plt.gcf()
h.savefig(os.path.join(results_dir,'eogprojs_'+'_subj{}.png'.format(0)))
#back to inline plotting
%matplotlib inline 
      

## Find ecg events (it probably does not work, much better to run ICA)
#ecg_evoked = mne.preprocessing.create_ecg_epochs(raw).average()
#ecg_evoked.plot_joint()
  

## fitting ICA (also see: https://mne.tools/stable/auto_tutorials/preprocessing/40_artifact_correction_ica.html)
#filt_raw = raw.copy().load_data().filter(l_freq=1.0, h_freq=None) #before ICA filter data to remove low-frequency drifts that can affect ICA quality because they reduce the independence of the sources. A high-pass filter with 1 Hz cutoff frequency is recommneded
#ica = ICA(n_components=15, max_iter="auto", random_state=97)
#ica.fit(filt_raw)
#ica  

#raw.load_data()
#ica.plot_sources(raw, show_scrollbars=False)



# Create event_id dictionary
event_id = {}
for i in range(1,13):
    event_id['animate/human/body/{}'.format(i)] = i
for i in range(13,25):
    event_id['animate/human/face/{}'.format(i)] = i
for i in range(25,37):
    event_id['animate/animal/body/{}'.format(i)] = i
for i in range(37,49):
    event_id['animate/animal/face/{}'.format(i)] = i
for i in range(49,73):
    event_id['inanimate/natural/{}'.format(i)] = i
for i in range(73,93):
    event_id['inanimate/artificial/{}'.format(i)] = i


## Create epochs (baseline correction is applied automatically)
epochs = mne.Epochs(raw, events=events, event_id = event_id, tmin=-0.2, tmax=.8, reject=reject, flat=flat, reject_by_annotation=False, preload=True)
#epochs.plot_drop_log() #only works if epochs loaded, e.g. preload=True
#epochs[:5].plot(n_epochs=10)


## Downsample epochs to 250Hz
#starttime = timeit.default_timer()
#epochs = epochs.resample(250,n_jobs=10) #no difference with n_jobs 5 or 10
#print('Processing time for resampling: {:.2f} sec'.format(timeit.default_timer() - starttime))


## Filter epochs, 35Hz low pass
print('Filtering epochs for subject {}'.format(0))
epochs.filter(l_freq=None,h_freq=35, picks='meg')


## Save all epochs to avoid recomputing
epochs.save(os.path.join(project_dir,'data_tmp\\subj_{}-epo.fif'.format(0)), overwrite=True)


# Save noise covariance
print('\nComputing noise covariance for subject {}'.format(0))
noise_cov = mne.compute_covariance(epochs, tmax=0., method=['shrunk', 'empirical'], rank=None, verbose='error')
noise_cov.save(os.path.join(project_dir,'data_tmp\\subj_{}-noise-cov.fif').format(0), overwrite=True)


## Plot whitened evoked response
#evoked.plot_white(noise_cov,time_unit='s') 






    