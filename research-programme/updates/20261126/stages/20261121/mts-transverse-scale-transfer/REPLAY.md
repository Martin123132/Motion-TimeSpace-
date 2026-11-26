# Offline reproduction

Use the retained Python 3.13 interpreter with NumPy, SciPy, SymPy and requests. All calculation workers run locally, one at a time. No GPU, ensemble download or newly fitted parameters. From this directory:

```
python -B verify.py
python -B scale_kernel.py
python -B anchor.py
python -B mesh.py
python -B cut.py
python -B belle.py
python -B pion_control.py
python -B verify.py
```

The initial check verifies the two previous seals and each input they list directly in their stage file maps; it also checks the convention/threshold register and the nominal W-mass provenance. The numerical programs compare existing outputs rather than overwrite them. Reproduction of exact floating-point serialization is for the saved environment. No source retrieval is needed for the offline sequence.

Original acquisition only: cut.py --acquire checks arXiv 2108.05896v3, archive and TeX digests, and the signed prefactors in the three Appendix D sections. It retains only a provenance record. belle.py --acquire retrieves HEPData v1 Tables 1, 2, 96 and 141 from the release's own data endpoint; all four raw public table JSONs are saved with their metadata and CC0 attribution. The two additional works linked in the hadronic discussion are references for the next step, **not** numerical inputs in this stage. Neither a positive HVP spectrum nor a measurement of a gravitational three-point function was used here.
