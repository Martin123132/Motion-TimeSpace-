# Preserve failed adapter attempt; correct object ownership

Cold and heavy cubic controls in the isolated rebuilt library are byte-for-
byte identical to the previous native packets. The first enabled heavy
quintic attempt failed with an access violation during background creation.
Its failed receipt is preserved; no physical result was produced. A checker
was then launched too early and correctly failed on that missing result;
its three completed control replay packets are retained for reuse.

The retained baseconfig.py explicitly documents that accessing an allocatable
field returns an alias that becomes undefined when that field is reassigned.
The adapter took model=params.DarkEnergy and then reassigned the same owned
field from that alias. Correct the adapter by using the supported .copy()
before modification/reassignment. This changes memory ownership, not the
action, coefficients, solver settings or candidate interpolation.

Run the corrected heavy candidate once under a separate -owned label. Do
not overwrite failed receipts or repeat completed controls. Confirm that
the new enabled candidate actually reaches full evolution before analysis.
