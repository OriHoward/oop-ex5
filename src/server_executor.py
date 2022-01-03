import os
import subprocess
from subprocess import check_output

stage_id = '15'
print(os.getcwd())
os.chdir('../')
jar_path = os.path.join("Ex4_Server_v0.0.jar")
subprocess.Popen(['java', '-jar', jar_path, stage_id],stdin=None, stdout=None, stderr=None)
