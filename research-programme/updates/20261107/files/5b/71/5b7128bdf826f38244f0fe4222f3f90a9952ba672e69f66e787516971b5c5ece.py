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
    key=script.removesuffix('.py')+'-'+('-'.join(arguments).replace('--',''))
    folder=ROOT/'logs'
    folder.mkdir(exist_ok=True)
    path=folder/(key+'.log')
    assert not path.exists(),path
    print(datetime.now(timezone.utc).isoformat(),script,*arguments,flush=True)
    with path.open('x',encoding='utf-8') as log:
        result=subprocess.run([sys.executable,'-B',str(ROOT/script),*arguments],cwd=ROOT,stdout=log,stderr=subprocess.STDOUT)
    assert result.returncode==0,(script,arguments,result.returncode)
    print('FINISHED',script,*arguments,flush=True)


def main():
    run('check_direct_identity.py')
    for order,panel,upper in [(6,32,.04),(8,32,.04),(6,48,.04),(6,32,.02)]:
        run('build_direct_bank.py','--order',str(order),'--panel',str(panel),'--upper',str(upper))
        bank=f'bank-o{order}-q{panel}-m{int(upper*1000)}'
        run('build_direct_sources.py','--bank',bank)
        source='sources-fine-'+bank.removeprefix('bank-')
        run('propagate_direct.py','--source',source)
        if order==8:
            run('propagate_direct.py','--source',source,'--steps','512')
    for variant in ['space','time']:
        run('build_direct_sources.py','--bank','bank-o8-q32-m40','--variant',variant)
        run('propagate_direct.py','--source',f'sources-{variant}-o8-q32-m40')
    print('STAGE CALCULATIONS COMPLETE',flush=True)


if __name__=='__main__':
    main()

