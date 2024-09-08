# Monitor & Backdoor Composer DAG

If you have read and write access over a GCP Storage bucket used to store the code of the composer DAGs, you can monitor the bucket and submit a backdoored version of the code whenever it gets updated so the new DAG will execute your code and you will be able to escalate privileges to the Service Account assigned to the composer environment.

This script is a probe of concept of the previous attack that will monitor a bucket and submit a python file (`reverse_shell.py`) with some python code that will send a reverse shell.

**REMEMBER TO UPDATE THE REVERSE SHELL ADDRESS INSIDE `reverse_shell.py` BEFORE EXECUTING IT**.

This PoC has a failure and it's that it only detects when a new DAG is created and not when an already existing one is updated.

```bash
# Installation
python3 -m pip install -r requirements.txt

python3 backdoor_dag_bucket.py <bucket-name>

#e.g.
python3 backdoor_dag_bucket.py us-central1-testingcomposer-ff257678-bucket
```
