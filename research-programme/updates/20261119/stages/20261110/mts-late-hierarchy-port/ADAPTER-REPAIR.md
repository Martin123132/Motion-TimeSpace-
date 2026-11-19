# Inactive memory guard repair

First capture exited natively with code1: `inactive neutrino memory nonzero`.
PID36740, creation1794303016.3438783, is confirmed absent. Fortran ERROR STOP
exits the process before Python's finally/end receipt; no running handle
or partial capture is being mistaken for resumable work. The configuration
and first adapter/DLL remain saved. No other process was touched.

The native initial state initializes MassiveNuApprox false, but its unused
G11/G30 members are not a contractual zero until that approximation switch
has set them. The original late dynamics reads these members only inside
the active MassiveNuApprox branch. The v1adapter incorrectly inspected
inactive storage. The old early tangent experiment had explicitly zeroed
that storage, hiding the distinction.

v2removes ONLY the read/check of inactive memory. Its copied operator already
zeros local inactive storage and only captures/restores memory for active
branches. The discrete selector, active preparation-memory map, native
regime signature and tight-coupling guards remain intact. No physical
equation, tolerance, source history or initial perturbation is changed.

The driver gains optional build-folder and receipt/output tags so retries
cannot overwrite v1evidence. The previous driver's hash is retained in
runs/heavy/config.json; no original scientific file is modified.
