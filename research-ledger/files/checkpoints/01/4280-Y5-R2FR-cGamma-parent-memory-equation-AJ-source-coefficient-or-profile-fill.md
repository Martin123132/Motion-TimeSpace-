# 4280 - cGamma parent memory equation AJ source coefficient or profile fill

Marker: `PPC4161_CGAMMA_PARENT_MEMORY_AJ_SOURCE_COEFFICIENT_OR_PROFILE_FILL_4280`

Decision: `CGAMMA_AJ_SOURCE_TERM_ZEROED_BY_DQ_CLOSURE_TRANSPORT_BGRAD_ROUTING_REMAINS_NONCLAIM`

4280 applies 4277 to the earlier cGamma machinery:

```text
all Dq_i[H_L]=0 => Hperp=0 => S_A Hperp^A=0 => A_src=0.
```

The remaining AJ gate is:

```text
A_J,eff_private <= |R_transport_to_local| + |R_Bgrad_to_local|.
```
