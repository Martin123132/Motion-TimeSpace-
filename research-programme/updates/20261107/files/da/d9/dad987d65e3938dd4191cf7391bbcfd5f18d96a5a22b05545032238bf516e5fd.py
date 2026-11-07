from common import ROOT, BACKGROUND, modest, require, read, write, digest, load
import numpy as np

def main():
    modest()
    owner=read(ROOT/"prediction-configured-result.json")
    records=[]
    for model in owner["reports"]:
        for case in model["cases"]:
            path=ROOT/"runs-configured"/model["model"]/case["file"]
            require(digest(path)==case["sha256"],"unchanged trajectory")
            packet=load(path)
            reconstructed=np.exp(packet["efold"])
            difference=abs(packet["a"]-reconstructed)
            records.append(dict(model=model["model"],case=case["tag"],
                                maximum_absolute=float(np.max(difference)),
                                maximum_relative=float(np.max(difference/reconstructed)),
                                maximum_ulps=float(np.max(difference/np.spacing(reconstructed))),
                                observer_scale_exact=bool(np.array_equal(packet["a"],packet["observer"][:,27])),
                                source_sha256=case["sha256"]))
    write(ROOT/"comparison-domain-diagnostic.json",dict(records=records,source_sha256=digest(__file__),
                                                       reason="Fortran scalar exp versus NumPy vector exp; use already frozen algebra gate for cross-library reconstruction, not bitwise identity"))
    print(records,flush=True)

if __name__=="__main__":
    main()

