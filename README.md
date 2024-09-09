# Monitor & Backdoor Composer DAG

If you have read and write access over a GCP Storage bucket used to store the code of the composer DAGs, you can monitor the bucket and submit a backdoored version of the code whenever it gets updated so the new DAG will execute your code and you will be able to escalate privileges to the Service Account assigned to the composer environment.

This script is a probe of concept of the previous attack that will monitor a bucket and submit a python file (`reverse_shell.py`) with some python code that will send a reverse shell.

Find more information in https://cloud.hacktricks.xyz/pentesting-cloud/gcp-security/gcp-privilege-escalation/gcp-storage-privesc#composer

**REMEMBER TO UPDATE THE REVERSE SHELL ADDRESS INSIDE `reverse_shell.py` BEFORE EXECUTING IT**.

```bash
# Installation
python3 -m pip install -r requirements.txt

python3 backdoor_dag_bucket.py <bucket-name>

#e.g.
python3 backdoor_dag_bucket.py us-central1-testingcomposer-ff257678-bucket
```
