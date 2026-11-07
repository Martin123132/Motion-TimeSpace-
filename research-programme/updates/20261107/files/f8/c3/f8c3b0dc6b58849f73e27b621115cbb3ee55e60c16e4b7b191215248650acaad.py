from common import ROOT, ALGEBRA, modest, read, write, digest, load, require
import numpy as np

def main():
    modest()
    owner=read(ROOT/"prediction-bound-result.json")
    rows=[]
    for group in owner["reports"]:
        folder=ROOT/"runs-bound"/(group["model"]+"-"+group["label"])
        context=load(folder/"initial-context.npz")
        for case in group["cases"]:
            packet=load(folder/case["file"])
            require(digest(folder/case["file"])==case["sha256"],"sealed trajectory")
            expected_extended=(packet["initial_extended"]/packet["units"])*packet["units"]
            expected=np.zeros(len(context["initial"]))
            expected[packet["core"]]=expected_extended[:len(packet["core"])]
            expected[packet["tail_slots"]]=expected_extended[len(packet["core"]):].reshape(case["maximum"]-2,5)[:int(context["native_order"])-2]
            original=case["amplitude"]*context["initial"]
            difference=abs(packet["projected_state"][0]-original)
            nonzero=original!=0
            ulps=float(np.max(difference[nonzero]/abs(np.spacing(original[nonzero])))) if np.any(nonzero) else 0.
            relative=float(np.max(difference)/max(np.max(abs(original)),1e-80))
            exact=bool(np.array_equal(expected,packet["projected_state"][0]))
            zero=bool(np.count_nonzero(packet["projected_state"][0][~nonzero])==0)
            require(exact and zero and relative<ALGEBRA,"initial normalization roundtrip")
            rows.append(dict(model=group["model"],label=group["label"],case=case["tag"],roundtrip_exact=exact,
                             unseeded_exact_zero=zero,maximum_ulps=ulps,relative=relative))
    write(ROOT/"initial-roundtrip-diagnostic.json",dict(passed=True,rows=rows,source_sha256=digest(__file__),prediction_sha256=digest(ROOT/"prediction-bound-result.json")))
    print(dict(cases=len(rows),maximum_ulps=max(row["maximum_ulps"] for row in rows),maximum_relative=max(row["relative"] for row in rows)),flush=True)

if __name__=="__main__":
    main()

