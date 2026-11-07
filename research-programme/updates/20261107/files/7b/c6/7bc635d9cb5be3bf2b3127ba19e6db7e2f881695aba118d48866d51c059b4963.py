import csv
import hashlib
import io
import json
import os
import sys
import zipfile
from datetime import datetime, timezone
from pathlib import Path


HERE = Path(__file__).resolve().parent
POST = HERE.parent
BRIDGE = Path("C:/MTS-Data/condensate-origin-20261003/stiff-gas-dense-output-20261027/data/memory-tail-history-20261027/source-readout-bridge-20261102")
CAMPAIGN = BRIDGE / "final-stable-real-batch-rays037-038"


def require(condition, message):
    if not condition:
        raise ValueError(message)


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8-sig"))


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def guard():
    import psutil
    now = datetime.now(timezone.utc)
    require(now.isoformat() < "2026-11-07T02:42" and now.hour < 3, "outside this authorized slot")
    markers = ["STOP-REQUESTED", "../STOP-REQUESTED", "../execution-v3/STOP-REQUEST.json",
               "saved-epoch-cell450/STOP-REQUESTED", "final-epoch-kinematic-bank/STOP-REQUESTED",
               "final-stable-real-batch-rays037-038/STOP-REQUESTED", "final-stable-real-batch-rays035-036/STOP-REQUESTED"]
    require(not any((BRIDGE / marker).exists() for marker in markers), "workspace held")
    require(read(CAMPAIGN/"integrity.json")["passed"] and read(CAMPAIGN/"common-coverage.json")["through"] == 38
            and read(BRIDGE/"regular-pair-037-038-process-receipts/coverage.end.json")["actual_exit_code"] == 0, "pair has not completed and been sealed")
    for proc in psutil.process_iter(["pid","name","cmdline"]):
        if proc.pid != os.getpid() and proc.info["name"] in ("python.exe","pythonw.exe"):
            command = " ".join(proc.info["cmdline"] or [])
            require("source-readout-bridge-20261102" not in command and str(HERE) not in command, "other calculation active")


def profile(ell, step):
    import numpy as np
    from scipy.linalg import eigh_tridiagonal
    from numpy.polynomial.legendre import leggauss
    guard()
    box = 120.
    radius = step * np.arange(1, round(box/step))
    inverse = 1 / step**2
    centrifugal = ell*(ell+1)/(2*radius**2)
    off = np.full(len(radius)-1, -inverse/2)
    potential = -1/np.hypot(radius, 7 if ell else 2)
    for iteration in range(380):
        energy, vectors = eigh_tridiagonal(inverse+centrifugal+potential, off, select="i", select_range=(0,0), lapack_driver="stebz")
        wave = np.abs(vectors[:,0])/np.sqrt(step)
        shells = wave**2*step
        inward = np.cumsum(shells)
        outer = np.cumsum((shells/radius)[::-1])[::-1] - shells/radius
        next_potential = -inward/radius-outer
        if np.max(np.abs(potential-next_potential)) < 2e-11:
            break
        potential = .45*potential+.55*next_potential
    else:
        raise ValueError("nonconverged independent eigenstate")
    enclosed = inward - shells/2
    half = np.interp(.5, enclosed, radius)
    old = next(item[-1] for item in read(HERE/"result.json")["states"] if item[-1]["ell"]==ell)
    require(abs(energy[0]/old["energy"]-1) < .002 and abs(half/old["halfMass"]-1)<.002,"independent eigen/Poisson mismatch")
    edges=np.r_[0.,radius,box]
    reduced=wave/radius**(ell+1)
    reduced=np.r_[(4*reduced[0]-reduced[1])/3,reduced,0.]
    nodes,weights=leggauss(4)
    def integral(lower,left,length):
        locations=lower[...,None]+length[...,None]*(nodes+1)/2
        interp=reduced[left,None]+(locations-lower[...,None])*(reduced[left+1,None]-reduced[left,None])/step
        return length/2*np.sum(weights*(locations**(ell+1)*interp)**2,axis=-1)
    cumulative=np.r_[0.,np.cumsum(integral(edges[:-1],np.arange(len(edges)-1),np.full(len(edges)-1,step)))]
    def enclosed_at(distance):
        dist=np.asarray(distance,dtype=float)
        loc=np.minimum(len(edges)-2,(np.clip(dist,0,box)/step).astype(int))
        length=np.clip(dist-edges[loc],0,step)
        return np.where(dist>=box,1.,(cumulative[loc]+integral(edges[loc],loc,length))/cumulative[-1])
    return enclosed_at,dict(ell=ell,step=step,energy=float(energy[0]),half_mass=float(half),
                            integrated_mass_before_normalizing=float(cumulative[-1]),iterations=iteration+1)


def checked_inputs():
    import numpy as np
    original=read(HERE/"result.json")
    paths={name:Path(path) for name,path in original["inputs"].items()}
    for path,expected in zip(paths.values(),original["sha256"],strict=True):
        require(digest(path)==expected,"changed input "+str(path))
    def csv_rows(path):
        return list(csv.DictReader(path.read_text(encoding="utf-8-sig").splitlines()))
    cohort=csv_rows(paths["cohort"])
    outer={row["galaxy"]:row for row in csv_rows(paths["outer"])}
    result=[]
    with zipfile.ZipFile(paths["archive"]) as archive:
        sources={Path(name).name:name for name in archive.namelist()}
        for row in cohort:
            name=row["galaxy"]
            data=np.loadtxt(io.BytesIO(archive.read(sources[name+"_rotmod.dat"])))
            data=data[(data[:,0]>0)&(data[:,1]>0)&(data[:,2]>0)]
            data=data[np.argsort(data[:,0])]
            baryon=data[:,3]*abs(data[:,3])+.5*data[:,4]*abs(data[:,4])+.7*data[:,5]*abs(data[:,5])
            deficit=data[-1,1]**2-baryon[-1]
            require(data[-1,0]==float(outer[name]["radius_kpc"]) and abs(deficit-float(outer[name]["observed_squared_minus_baryons"]))<1e-7,"bad join")
            result.append((name,data,baryon,deficit))
    require(len(result)==52 and sum(len(obj[1]) for obj in result)==1337,"coverage")
    return original,read(paths["growth"]),result


def shape_scores(states,galaxies,mass):
    import numpy as np
    from scipy.optimize import brentq
    kappa=1.973269804593025e-7*299792.458/(mass*3.0856775814913673e19)
    rows=[]
    for name,data,baryon,deficit in galaxies:
        rad,vel=data[-1,:2]
        frac=data[:-1,0]/rad
        eta2=(rad/kappa)**2*deficit
        squared=[baryon[:-1],baryon[:-1]+deficit]
        scales=[]
        for cumulative in states:
            scale=brentq(lambda value:value*cumulative(value)-eta2,0.,max(120,eta2)*2,xtol=1e-13,rtol=1e-14)
            require(abs(scale*cumulative(scale)/eta2-1)<1e-9,"endpoint closure")
            scales.append(float(scale))
            squared.append(baryon[:-1]+deficit*cumulative(scale*frac)/(frac*cumulative(scale)))
        errors=(np.array(squared)-data[:-1,1]**2)/vel**2
        row=dict(galaxy=name,scales=scales)
        for key,mask in (("outerHalf",frac>=.5),("innerHalf",frac<.5)):
            require(np.any(mask),"no interior radii")
            row[key]=dict(ab=np.median(np.abs(errors[:,mask]),axis=1).tolist(),signed=np.median(errors[:,mask],axis=1).tolist())
        rows.append(row)
    stats={}
    for key in ("outerHalf","innerHalf"):
        medians=np.array([row[key]["ab"] for row in rows])
        stats[key]=dict(medianAbs=np.median(medians,axis=0).tolist(),
                        medianSigned=np.median([row[key]["signed"] for row in rows],axis=0).tolist(),
                        beats_constant=np.sum(medians[:,2:]<medians[:,1,None],axis=0).tolist())
    return dict(mass_eV=mass,stats=stats,rows=rows)


def run():
    import numpy as np
    original,growth,galaxies=checked_inputs()
    masses=sorted({row["mass_eV"] for row in growth["rows"]})
    require(len(masses)==6,"changed Stage50 mass grid")
    calculations=[]
    for step in (.025,.0125):
        solutions=[profile(ell,step) for ell in (0,1)]
        calculations.append(([item[1] for item in solutions],
                             [shape_scores([item[0] for item in solutions],galaxies,mass) for mass in masses]))
    max_score_change=max(abs(score-other) for coarse,fine in zip(calculations[0][1],calculations[1][1])
                         for row,new in zip(coarse["rows"],fine["rows"]) for key in ("outerHalf","innerHalf")
                         for column in ("ab","signed") for score,other in zip(row[key][column],new[key][column]))
    max_scale_change=max(abs(scale/other-1) for coarse,fine in zip(calculations[0][1],calculations[1][1])
                         for row,new in zip(coarse["rows"],fine["rows"]) for scale,other in zip(row["scales"],new["scales"]))
    require(max_score_change<.002 and max_scale_change<.002,"unresolved shape mesh")
    benchmark=next(entry for entry in calculations[1][1] if entry["mass_eV"]==original["massEV"])
    require([row["galaxy"] for row in benchmark["rows"]]==[row["name"] for row in original["rows"]],"cohort order")
    replay_error=max(abs(val-prev) for row,old in zip(benchmark["rows"],original["rows"]) for key in ("outerHalf","innerHalf")
                     for new_field,old_field in (("ab","abs"),("signed","signed"))
                     for val,prev in zip(row[key][new_field],old[key][old_field]))
    require(replay_error<.002,"benchmark replay differs")
    require(all(abs(entry["stats"]["outerHalf"]["medianAbs"][1]-.06680413735256022)<1e-12 for entry in calculations[1][1]),"comparator drift")
    for entry in calculations[1][1]:
        rows=[row for row in growth["rows"] if row["model"]=="ParentScalar_Lambda_zero" and row["start_z"]==99 and
              row["heavy_fraction"]==.5 and row["preparation"]=="equal" and row["mass_eV"]==entry["mass_eV"] and row["accepted"]]
        ratios={row["k_Mpc_inverse"]:row["total_density_ratio"] for row in rows}
        require(len(ratios)==len(rows),"duplicate Stage50 row")
        entry["Stage50_growth_ratios"]={str(wavenumber):ratios.get(wavenumber) for wavenumber in (.02,.05,.1,.2,.5,1.)}
    return dict(checked=True,hashes=original["sha256"],source_sha256=digest(__file__),dimensionless_controls=[item[0] for item in calculations],
                max_pointwise_galaxy_median_change=max_score_change,max_relative_normalization_change=max_scale_change,
                original_benchmark_replay_max_difference=replay_error,columns=["baryons","constant residual","wave0","wave1"],
                cases=calculations[1][1],scope="Exposed conditional diagnostic; outer mass fitted per galaxy, no particle mass fitted. Growth ratios are Stage50 equal-seed checks only.")


if __name__=="__main__":
    import psutil
    guard()
    for name in ("OPENBLAS_NUM_THREADS","OMP_NUM_THREADS","MKL_NUM_THREADS","NUMEXPR_NUM_THREADS","BLIS_NUM_THREADS"):
        os.environ[name]="1"
    worker=psutil.Process()
    worker.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
    worker.cpu_affinity([4])
    out=HERE/"mass-grid-result.json"
    require(not out.exists(),"immutable grid result exists")
    result=run()
    with out.open("x",encoding="utf-8") as stream:
        json.dump(result,stream,allow_nan=False,separators=(",",":"))
    print(json.dumps({key:value for key,value in result.items() if key not in ("cases","hashes","dimensionless_controls")}))
