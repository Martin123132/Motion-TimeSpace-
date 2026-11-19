# Applying the new bound to the original mode

The continuous phase-mean source replacement bound is now derived from the complete coupled source, including the normalized phase-clock measure. It is not necessary to guess a new late initial vector to use it.

For two continuous mean systems z_1'=Abar_1 z_1 and z_0'=Abar_0 z_0 with the same initial physical preparation, variation of constants gives

    delta z(N) = integral U_1(N,s) [Abar_1(s)-Abar_0(s)] z_0(s) ds.

Given a valid logarithmic-norm envelope g_1(s), this implies

    ||delta z(N)|| <= integral exp(integral_s^N g_1(u)du)
                      [ ||E(s)|z_0(s)|| + epsilon_measure(s)||z_0(s)|| ] ds.

E is the saved nonnegative entrywise coefficient-replacement bound. The clock-measure term is the additional operator bound from `mean-weight-02`. Apply this expression to the actual prepared perturbation and its controlled continuous evolution. Small hierarchy populations can suppress a large worst-case streaming/terminal coefficient contribution; that suppression must be demonstrated from the mode, not assumed.

For a conservative uniform comparison, if a whole-path reference mean growth bound g_0 is available, the new symmetric mean bound e_sym gives g_1<=g_0+e_sym. With uniform full mean replacement e_A, span L and equal initial z_0,

    ||delta z(L)|| <= e_A exp(g_0 L) expm1(e_sym L)/e_sym ||z_0(0)||,

with the continuous limit L at e_sym=0. This is a CONDITIONAL transport inequality: the midpoint logarithmic norm must not be substituted for a whole-path g_0 without deriving the latter. The larger absolute streaming norm is not a permissible replacement for a physically meaningful growth estimate merely because it is easy to compute.

Before evolution, locate and verify the original early physical mode/preparation used by the retained branch, and the route to the cold entrance. Do not assume a late transfer vector already exists, set it to unity or reset a phase. Carry the original physical endpoint maps, the existing periodic near-identity correction and moving-slow averaging remainder. The new source-replacement envelope controls a separate contribution; it does not absorb global solver or input/thermal continuum errors.

Next implementation should calculate that preparation-to-cold matching and the continuous mean growth/forcing envelope on the inherited background, reuse original wave numbers and source equations, and compare baseline and MTS with the unchanged gates. If an original preparation or matching condition is incomplete, derive it from its retained source rather than introducing a free fitted amplitude.
