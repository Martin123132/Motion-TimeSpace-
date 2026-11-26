# Reproduce locally without a download

The retained Python 3.13 environment uses NumPy, SciPy and SymPy. Use normal (non-optimized) Python, one numerical thread as configured in base.py, and -B to avoid caches. From this directory run these in order:

```
python -B verify.py
python -B sources.py
python -B maxwell_ward.py
python -B empirical.py
python -B spectral_target.py
python -B charge_free.py
python -B colored.py 0
python -B precision.py 0
python -B colored.py 1
python -B precision.py 1
python -B fixture_checks.py
python -B color_covariance.py
python -B verify.py
```

The first and last commands check the previous stage, the signed-off file digests, the CSV contents and gates; the other commands recompute the numerical results. The saved stage writers compare existing artifacts instead of overwriting them. Full numerical replay is intended for the same Python/BLAS environment; floating-point serialization can differ on other platforms. No permission to fetch gauge configurations, fit source coefficients, change tolerances or update a release is implied.

**Sources and conventions.** [ILDG D450r010 metadata](https://www-zeuthen.desy.de/ape-cgi-bin/ildg-mdc.cgi?action=show&collection=ensemble&grid=ldg&id=mc://ldg/cls/nf21/D450r010), [openQCD releases](https://luscher.web.cern.ch/luscher/openQCD/), [OPAL](https://arxiv.org/abs/hep-ex/0505072), [Cè et al.](https://arxiv.org/abs/2203.08676), [Hatton et al.](https://arxiv.org/abs/2101.08103), [Conigli et al.](https://arxiv.org/abs/2511.01623), [D450 nominal scale in Table I](https://doi.org/10.1103/qh7q-9nyy). Numerical extracts and checksums of the versioned paper members and openQCD documentation are saved, not entire papers, software distributions or bulk fields. The upstream configuration-data attribution terms remain those of CLS/ILDG. No cosmology or galaxy inputs enter this measurement design.
