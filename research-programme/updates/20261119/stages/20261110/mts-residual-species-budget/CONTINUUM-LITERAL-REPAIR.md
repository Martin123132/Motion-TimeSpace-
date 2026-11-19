# Reference-reader repair; failed attempt retained

Original reader SHA256: `fdf7feac835f817d30197368e0bcb343c0755ac7ad17a7d5f38dafdeccc5ef42`.

The first continuum reference worker stopped at the unchanged 1e-10 common
mass check before computing a reference result. Its `continuum-start.json`
and `continuum-end.json` remain. No native calculation or saved input changed.

The native five-node q and kernel tables use unsuffixed Fortran real literals,
not `_dl` literals. With the retained compiler flags those literals are REAL32
before promotion into the real(dl) arrays. Parsing the printed decimal table
directly as Python double did not reproduce the stored values. For example,
the inferred common am was 32.417594512639297 from decimal q=0.583165 versus
32.417593953873208 from the exactly represented q=2 and q=4.

The reference reader now performs that literal rounding and promotion via
`float(np.float32(literal))`. It must pass the SAME mass-consistency and
continuum-comparison gates. No tolerance, native grid, stored source or mass
is adjusted. A new `continuum-literals` worker receipt distinguishes this
reader repair from a retry of a failed physical model.
