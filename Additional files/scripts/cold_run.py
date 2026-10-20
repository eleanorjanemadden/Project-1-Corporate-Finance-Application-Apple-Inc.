"""Fresh runtime environment, with explicitly limited staging when OneDrive originals are offline."""
import datetime
import hashlib
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import time
import urllib.request

root=Path(__file__).resolve().parents[1]
with (root/'outputs/cold_run_log.txt').open('w') as log, tempfile.TemporaryDirectory(prefix='apple-runtime-cold-') as temp:
    target=Path(temp)/'project';target.mkdir()
    log.write('Runtime cold run '+datetime.datetime.now(datetime.timezone.utc).isoformat()+'\n')
    log.write('Fresh venv; selected runtime/source inputs copied. Offline original evidence/archive not staged.\nOriginal-content checksum check explicitly SKIPPED here, not verified.\n');log.flush()
    files=['analysis.py','apple_proforma.py','dated_refresh.py','app.py','requirements.txt','README.md','FILE-INVENTORY.csv',
           'docs/source_ledger.csv','sources/aapl-20250927.txt','sources/course_abg_slides.html','sources/dgs10_july2026.csv',
           'outputs/visible_output.json','outputs/dated/visible_output.json','outputs/retrospective/visible_output.json']
    files += [str(x.relative_to(root)) for x in (root/'tests').glob('*.py')]
    for name in files:
        dest=target/name;dest.parent.mkdir(parents=True,exist_ok=True)
        log.write('STAGE '+name+'\n');log.flush()
        shutil.copyfile(root/name,dest)
    env=os.environ.copy();env.pop('PYTHONPATH',None)
    env['PYTHONNOUSERSITE']='1';env['PYTHONDONTWRITEBYTECODE']='1';env['APPLE_COLD_STAGING']='runtime_only'
    def run(args):
        log.write('\n$ '+subprocess.list2cmdline([str(x) for x in args])+'\n');log.flush()
        result=subprocess.run([str(x) for x in args],cwd=target,env=env,stdout=log,stderr=subprocess.STDOUT)
        log.write('EXIT '+str(result.returncode)+'\n');log.flush()
        if result.returncode:raise RuntimeError('Cold command failed; retained log explains')
    run([sys.executable,'--version']);run([sys.executable,'-m','venv',target/'.venv'])
    python=target/'.venv/bin/python'
    run([python,'-m','pip','install','-r','requirements.txt'])
    run([python,'-B','-m','unittest','discover','-s','tests','-v'])
    before={name:hashlib.sha256((target/name).read_bytes()).hexdigest() for name in files if name.endswith('visible_output.json')}
    run([python,'-B','analysis.py']);run([python,'-B','dated_refresh.py'])
    for name,expected in before.items():
        actual=hashlib.sha256((target/name).read_bytes()).hexdigest()
        log.write(f'HASH {name}: before={expected} after={actual}\n')
        if actual!=expected:raise RuntimeError('Cold output mismatch')
    run([python,'-m','pip','freeze'])
    command=[str(python),'-B','-m','streamlit','run','app.py','--server.headless=true','--server.address=127.0.0.1','--server.port=8767','--browser.gatherUsageStats=false']
    log.write('\n$ '+subprocess.list2cmdline(command)+'\n');log.flush()
    with (target/'server.log').open('w') as server_log:
        server=subprocess.Popen(command,cwd=target,env=env,stdout=server_log,stderr=subprocess.STDOUT)
        try:
            for _ in range(100):
                try:
                    response=urllib.request.urlopen('http://127.0.0.1:8767/_stcore/health',timeout=1)
                    log.write(f'HTTP health {response.status}: {response.read().decode()}\n');break
                except OSError:time.sleep(.2)
            else:raise RuntimeError('Server not healthy')
        finally:server.terminate();server.wait(timeout=10)
    log.write((target/'server.log').read_text())
    log.write('\nRuntime cold check COMPLETED: tests with explicit preservation skip, both models byte-identical, HTTP health passed; server stopped.\nNOT a complete original-evidence preservation verification or human access/review.\n')
print(root/'outputs/cold_run_log.txt')
