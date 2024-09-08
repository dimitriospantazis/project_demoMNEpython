# Author: Dimitrios Pantazis
# Downloads the required MEG/MRI demo files

import os
import requests
import zipfile
import tarfile

def download_file(url, output_dir):
    # Get the filename from the URL
    filename = url.split("/")[-1]
    filepath = os.path.join(output_dir, filename)
    
    # Download the file
    print(f"Downloading {filename}...")
    response = requests.get(url, stream=True)
    response.raise_for_status()  # Check for request errors
    
    # Save the file locally
    with open(filepath, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)
    
    print(f"Downloaded {filename} to {filepath}")
    return filepath

def unzip_file(filepath, output_dir):
    if zipfile.is_zipfile(filepath):
        print(f"Unzipping {filepath}...")
        with zipfile.ZipFile(filepath, 'r') as zip_ref:
            zip_ref.extractall(output_dir)
        print(f"Unzipped to {output_dir}")
    elif tarfile.is_tarfile(filepath):
        print(f"Unpacking {filepath}...")
        with tarfile.open(filepath, 'r:gz') as tar_ref:
            tar_ref.extractall(output_dir)
        print(f"Unpacked to {output_dir}")
    else:
        print(f"File {filepath} is not a zip or tar file.")

def download_and_process_files(urls, output_dir, unzip=False):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    for url in urls:
        filepath = download_file(url, output_dir)
        if unzip:
            unzip_file(filepath, output_dir)



# Download MRI
urls = ["https://figshare.com/ndownloader/files/49066579"]
output_directory = "./recons"
download_and_process_files(urls, output_directory, unzip=True)
os.remove(os.path.join(output_directory,'49066579'))

# Download rawMEGdata (blink_heartbeat_MEGEEG1_subj14_tsss_mc.fif and subj04NN_sess02_raw_tsss[-1/2].fif)
urls = ["https://figshare.com/ndownloader/files/49066591",
        "https://figshare.com/ndownloader/files/49066603",
        "https://figshare.com/ndownloader/files/49066606",
        "https://figshare.com/ndownloader/files/49066588",
        "https://figshare.com/ndownloader/files/49066573"
        ]
output_directory = "./rawMEGdata"
download_and_process_files(urls, output_directory, unzip=False)
os.rename(os.path.join(output_directory,'49066591'),os.path.join(output_directory,'blink_heartbeat_MEGEEG1_subj14_tsss_mc.fif') )
os.rename(os.path.join(output_directory,'49066603'),os.path.join(output_directory,'subj04NN_sess01_raw_tsss.fif') )
os.rename(os.path.join(output_directory,'49066606'),os.path.join(output_directory,'subj04NN_sess01_raw_tsss-1.fif') )
os.rename(os.path.join(output_directory,'49066588'),os.path.join(output_directory,'subj04NN_sess01_raw_tsss-2.fif') )
os.rename(os.path.join(output_directory,'49066573'),os.path.join(output_directory,'subj04NN-trans.fif') )

