# 3166 - First K2 Empirical Projection Gate Source Intake under AX1090

Private checkpoint. This follows 3165 by putting the first real empirical number on the `K_2` local residual lane, without pretending that the missing projection kernel has already been derived.

## Source Intake

The first gate is the Cassini/Shapiro PPN `gamma` result from Bertotti, Iess, and Tortora:

```text
gamma - 1 = (2.1 +/- 2.3) x 10^-5.
```

Recorded source anchors:

| source | record |
|---|---|
| primary PDF | `https://ilorentz.org/research/vanbaal/DECEASED/ART/gr-test.pdf` |
| PubMed index | `https://pubmed.ncbi.nlm.nih.gov/14508481/` |
| DOI | `10.1038/nature01997` |
| paper | Bertotti, Iess, Tortora, *A test of general relativity using radio links with the Cassini spacecraft*, Nature 425, 374-376 (2003) |

The nonclaim diagnostic envelopes are:

```text
one_sigma_uncertainty = 2.3e-5
abs_central_plus_1sigma = 4.4e-5
abs_central_plus_2sigma = 6.7e-5
```

3166 uses `abs_central_plus_2sigma = 6.7e-5` as the default conservative source-backed smoke bound.

## K2 Gamma Gate

From 3165:

```text
C_K2_unit = 3.593766357482964e-24.
```

The general Cassini/Shapiro gate is:

```text
|Pi_gamma,K2| K_2 C_K2_unit <= bound_gamma.
```

Equivalently:

```text
K_2 <= bound_gamma / (|Pi_gamma,K2| C_K2_unit).
```

The projection/readout kernel `Pi_gamma,K2` is not derived yet. Therefore the `Pi_gamma,K2=1` calculation is only a unit-projection diagnostic, not a pass claim.

## Unit-Projection Diagnostic

Using the default `abs+2sigma` envelope:

```text
K_2 <= 6.7e-5 / 3.593766357482964e-24
    <= 1.864339340271583e19
```

The inherited internal AX1090 cap was:

```text
K_2 <= 1.661478072732744e20.
```

Therefore:

```text
K2_Cassini_unit_projection / K2_internal_AX1090
= 1.122096867161887e-1.
```

This is important: under unit projection, Cassini/Shapiro is already tighter than the internal residual cap by about a factor of `8.91`.

## Projection-Owner Smoke Case

If a future parent derivation signs the natural projection-owner branch:

```text
K_2 = 1
Pi_gamma,K2 = 1
```

then:

```text
Delta_gamma = 3.593766357482964e-24.
```

Relative to the default Cassini envelope:

```text
Delta_gamma / 6.7e-5 = 5.363830384302932e-20.
```

So the natural owner smoke case is tiny. This is a useful signpost, not evidence yet.

## Claim Status

3166 does not claim:

- PPN safety;
- local-GR recovery;
- Shapiro-delay recovery;
- light-bending recovery;
- orbital safety;
- clock safety;
- R10 or WEP safety.

The claim remains blocked because the checkpoint has not derived:

```text
Pi_gamma,K2
```

from the public metric/Shapiro readout, nor has it proven that other local residual-vector components cannot cancel or dominate the `gamma` projection.

Every generated row remains:

```text
valid_for_claim=false.
```

## Runner Artifacts

| artifact | path |
|---|---|
| runner | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\scripts\Y5_R2FR_3166_first_K2_empirical_projection_gate_source_intake.py` |
| inputs | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3166_INPUTS.csv` |
| Cassini source intake | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3166_CASSINI_GAMMA_SOURCE_INTAKE.csv` |
| K2 gamma gate | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3166_K2_GAMMA_EMPIRICAL_GATE.csv` |
| Pi gamma contract | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3166_PI_GAMMA_PROJECTION_CONTRACT.csv` |
| decision | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3166_DECISION.csv` |
| validation | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3166_VALIDATION.csv` |

## Decision

3166 promotes the next target to:

```text
3167-Y5-R2FR-Pi-gamma-K2-Shapiro-projection-kernel-or-unit-smoke-only-under-AX1090.
```

Best next attack:

```text
derive Pi_gamma,K2 from the public metric/Shapiro projection kernel.
```

If that derivation closes and stays order-unity, the local branch gets a real empirical lever. If it does not close, the Cassini row stays a source-backed unit-projection smoke bound only.
