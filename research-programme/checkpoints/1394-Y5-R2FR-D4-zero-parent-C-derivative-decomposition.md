# 5378 - D4 zero-parent C derivative decomposition

## Decision

`D4_ZERO_PARENT_C_DERIVATIVE_NUMERICALLY_DERIVED__BUILD_COMMON_INTERVAL_ENCLOSURE`

## Derived identities

The event continuation is fixed by `Re z(epsilon,x(epsilon))=0`. Conjugation symmetry gives `x'(0)=0`, hence

`x''(0)=-Re(z_ee)/Re(z_x)`.

With `r=z0/z1` and `z1=sigma z_x`,

`r'=z_e/z1`,

`r''=(z_ee+z_x x'')/z1-2 z_e z1_e/z1^2`.

The full endpoint primitive therefore has the event coefficient

`C_log,e=-s[C0_e r'+(C0/2)r''-(C1/2)(r')^2]`.

## Eight-event result

| event | C0_e(0) | C1(0) | C_log,e |
|---|---:|---:|---:|
| E01 | 1.080829735739153081839833120694274507581e-28 +23.9375 i | 874.0838951733057668319225663233545790567 -3.36057e-27 i | 0.07659581737733368022110730249922051876563 -3.4193e-31 i |
| E02 | 1.447329629856343015567932713263090164964e-29 -3.09421 i | -277.1785266954194259496185496538635906533 -1.13075e-27 i | 0.002230431078739191638512495937129410888809 +1.05472e-32 i |
| E03 | -3.42747172440313808552229538519361653072e-26 -12.2631 i | -7913.950142272689029822032072288175806424 +6.48051e-26 i | 0.004194306430406279877384724979425840714218 -2.29386e-29 i |
| E04 | 5.64381279366737516630596837239810925456e-32 +0.000292591 i | -2.336876653208044629737931180894704733351 +9.64709e-30 i | 0.00000001622395186958352889670027158053756264665 -2.29362e-36 i |
| E05 | 2.439173626885309541724912072305277747091e-33 -0.000426772 i | 1.493558054219377324794039871020944747712 +6.32978e-30 i | 0.00000001049706668421749075122347888161551995097 +6.19788e-38 i |
| E06 | -1.324765058890138931725143531268213524321e-30 -0.000963075 i | 15.01433291803873144771713589532495655283 -3.74907e-27 i | 0.00000001322961428363988228753284805200547031672 -3.21236e-35 i |
| E07 | 1.642530392170069387992568501778341550492e-30 +0.000547277 i | -5.883254924178666919593851654270949162584 +1.86534e-27 i | -0.00000001091888128880896939215180857248444387467 +6.11628e-35 i |
| E08 | 5.199131142511172348799280398405329093398e-24 +177.476 i | -62903.03895974129686044590907842995315706 +1.03859e-24 i | 0.1340172408836955898684869370289075342685 -8.13411e-27 i |

## Sum

- Direct parent result: `0.2170378248019262902374240037494732463113 -8.15738e-27 i`.
- Diagnostic derivative radius: `4.450850411097563e-16`.
- Independent checkpoint-5377 candidate: `0.2260726982635993 -0.0007303900894365201 i`.
- Direct-to-candidate distance: `0.00906434819229658` against candidate disk `0.0039847013964454`.
- Continued-root quotient result: `0.2170378248019262902374240037498640738617 -7.62188e-21 i`.
- Formula-to-quotient distance: `7.621870190708837e-21`.
- Corrected fixed-A,C relative intercept envelope: `0.003943776088871726`.

## What closed

The omitted `C1` term is now evaluated directly on all eight zero-regulator parent traces. The event-motion curvature and `r''` terms come from implicit differentiation, not a finite-rung event fit. The explicit parent regulator derivative `C0_e` comes from the physical one-sided analytic continuation and is independently checked against the smallest finite normal forms.

## What remains open

The earlier finite-rung C candidate is retained as a historical diagnostic, not promoted over the direct parent result: its event coordinates were adequate for topology but not for a second derivative quotient. This is still a high-precision source-backed numerical derivative certificate, not an interval theorem on one common closed complex neighborhood. The strict endpoint-C limit, common interval atlas, H3, mapped-away W3, D4 outer limit and all GR/MTS claims remain false until that enclosure is supplied.
