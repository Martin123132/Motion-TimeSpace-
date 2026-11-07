import os
os.environ['OPENBLAS_NUM_THREADS']='1'
os.environ['OMP_NUM_THREADS']='1'
os.environ['MKL_NUM_THREADS']='1'
import sys
sys.dont_write_bytecode=True
from pathlib import Path
import subprocess
from datetime import datetime,timezone
ROOT=Path(__file__).resolve().parent


def run(script,*arguments):
    folder=ROOT/'logs'
    folder.mkdir(exist_ok=True)
    path=folder/(script.removesuffix('.py')+'-'+('-'.join(arguments).replace('--',''))+'.log')
    print(datetime.now(timezone.utc).isoformat(),script,*arguments,flush=True)
    with path.open('x',encoding='utf-8') as log:
        result=subprocess.run([sys.executable,'-B',str(ROOT/script),*arguments],cwd=ROOT,stdout=log,stderr=subprocess.STDOUT)
    assert result.returncode==0,(script,arguments,result.returncode)
    print('FINISHED',script,*arguments,flush=True)


def main():
    run('check_join_identity.py')
    for order in [6,8]:
        run('build_join_sources.py','--order',str(order),'--pilot')
    for order,panel in [(6,32),(8,32),(6,48)]:
        run('build_join_sources.py','--order',str(order),'--panel',str(panel))
        run('propagate_join.py','--source',f'sources-o{order}-q{panel}')
        if order==8:
            run('propagate_join.py','--source',f'sources-o{order}-q{panel}','--steps','512')
    print('STAGE CALCULATIONS COMPLETE',flush=True)


if __name__=='__main__':
    main()

