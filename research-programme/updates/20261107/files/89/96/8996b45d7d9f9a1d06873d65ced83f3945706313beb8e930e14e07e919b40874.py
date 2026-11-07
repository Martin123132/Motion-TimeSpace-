from __future__ import annotations

import os
import sys
os.environ['OMP_NUM_THREADS']='1'
os.environ['OPENBLAS_NUM_THREADS']='1'
os.environ['MKL_NUM_THREADS']='1'
sys.dont_write_bytecode=True
from pathlib import Path
from datetime import datetime, timezone
import json
import math
import time
import numpy as np
from scipy import interpolate,integrate

ROOT=Path(__file__).resolve().parent
BRANCH=ROOT.parent
POST=BRANCH.parent
PARENT=BRANCH/'finite-wave-canonical-source-20261007'
HISTORY=BRANCH/'full-history-source-precision-20261007'
NATIVE=BRANCH/'native-heavy-matching-20261007/native'
sys.path.insert(0,str(PARENT))
import vertex_common as inherited
modest=inherited.modest
digest=inherited.digest
write_json=inherited.write_json
camb=inherited.inherited.camb


def finish(folder,report,script,extra=()):
    paths=[Path(script),ROOT/'constraint_common.py',ROOT/'ACCEPTANCE.md',PARENT/'results/stage-integrity.json',*extra]
    report.update(state='complete',finished_utc=datetime.now(timezone.utc).isoformat(),
        script_sha256=digest(script),input_hashes={str(path):digest(path) for path in paths})
    write_json(folder/'status.json',report)
    (folder/'COMPLETE').write_text('complete\n',encoding='utf-8')


def connection_ricci(metric,first,second):
    dimension=len(metric)
    inverse=np.linalg.inv(metric)
    inverse_first=np.array([-inverse@first[axis]@inverse for axis in range(dimension)])
    connection=np.empty((dimension,dimension,dimension))
    connection_first=np.empty((dimension,dimension,dimension,dimension))
    for upper in range(dimension):
        for left in range(dimension):
            for right in range(dimension):
                bracket=first[left,:,right]+first[right,:,left]-first[:,left,right]
                connection[upper,left,right]=inverse[upper]@bracket/2
                for derivative in range(dimension):
                    bracket_prime=second[derivative,left,:,right]+second[derivative,right,:,left]-second[derivative,:,left,right]
                    connection_first[derivative,upper,left,right]=(inverse_first[derivative,upper]@bracket+inverse[upper]@bracket_prime)/2
    ricci=np.empty((dimension,dimension))
    for left in range(dimension):
        for right in range(dimension):
            ricci[left,right]=sum(connection_first[upper,upper,left,right]-connection_first[right,upper,left,upper]+sum(connection[upper,upper,middle]*connection[middle,left,right]-connection[upper,right,middle]*connection[middle,left,upper] for middle in range(dimension)) for upper in range(dimension))
    return connection,ricci


def christoffel_linear(first):
    result=np.empty((3,3,3),dtype=first.dtype)
    for upper in range(3):
        for left in range(3):
            for right in range(3):
                result[upper,left,right]=(first[left,upper,right]+first[right,upper,left]-first[upper,left,right])/2
    return result


def ricci_series(spatial,first,second):
    gamma=christoffel_linear(first)
    gamma_prime=np.array([christoffel_linear(second[axis]) for axis in range(3)])
    gamma2=-np.einsum('ul,ljk->ujk',spatial,gamma)
    gamma2_prime=-np.einsum('aul,ljk->aujk',first,gamma)-np.einsum('ul,aljk->aujk',spatial,gamma_prime)
    ricci1=np.empty((3,3),dtype=first.dtype)
    ricci2=np.empty((3,3),dtype=first.dtype)
    for left in range(3):
        for right in range(3):
            ricci1[left,right]=sum(gamma_prime[upper,upper,left,right]-gamma_prime[right,upper,left,upper] for upper in range(3))
            ricci2[left,right]=sum(gamma2_prime[upper,upper,left,right]-gamma2_prime[right,upper,left,upper]+sum(gamma[upper,upper,middle]*gamma[middle,left,right]-gamma[upper,right,middle]*gamma[middle,left,upper] for middle in range(3)) for upper in range(3))
    return ricci1,ricci2-spatial@ricci1,gamma
