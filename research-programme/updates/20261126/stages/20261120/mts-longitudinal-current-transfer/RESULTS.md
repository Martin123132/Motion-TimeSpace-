> Public reading copy: local links are mapped to released material or marked unavailable. Machine-specific passages, where present, have been omitted. See the inventory for the original digest.

# The surrounding current in the local Newtonian tide

**Result.** In the two signed compensated-cloud histories, matter outside the 6 comoving Mpc evolution box contributes **−5.29% to −5.43%** of the final wave-minus-cold secular tidal change. The minus sign means that the exterior opposes the full change for **both** host signs. These are fractions of the changing signal on the retained 273.43-year proper clock, not fractions of the total gravitational field. This is the cosmological cloud calculation, not the Milky Way/LMC test.

| Host sign | Proper aperture half-width/centre | Full Newton change (launch curvature units) | Exterior contribution/full |
|---|---:|---:|---:|
| + | 0.15 | −6.59652e−19 | −0.0529000 |
| + | 0.30 | −6.42695e−19 | −0.0542957 |
| − | 0.15 | +6.79481e−19 | −0.0530438 |
| − | 0.30 | +6.63676e−19 | −0.0543071 |

A small flux at the **far** edge is not a reason to ignore the surrounding matter. At the endpoint, transport across the 6 Mpc sphere contributes −12.74% to −13.30%; bulk radial and angular current in the exterior returns +5.76% to +6.15%; dilution adds +1.67% to +1.72%. The 120 Mpc surface flux is below 1.1e−9 of the changing tide on these inputs. The incident current that crosses the host and the induced current must both be included. The large, oppositely signed angular terms are in the CSV; treating this quadrupole as spherical radial transport gives a different answer.

## Derivation

Use the comoving quadrupolar excess number density per species, weighted by the saved gravitational coefficients. In native conformal time its continuity equation is

    ∂η d = −∂r(r² J)/r² + 6 U/r² .

Here U/r multiplies the angular gradient of P₂ in the tangential current. With monopole contrast C, radial speed u, induced quadrupole excess d_s and velocity potential v, and incident density/velocity D,V, the two contributions **before** summing the species are

    J_ind = (1+C) ∂r v + u d_s;    U_ind = (1+C) v
    J_inc = C ∂r V + u D;          U_inc = C V.

These follow by expanding density times velocity and subtracting the incident-only state, to first order in the quadrupole but retaining the host factors. The saved boundary uses ∂r v = −3v/L at the far edge; it does not set the entire incident current to zero. The wave and cold branches have different histories; this identity does not assume identical velocities. Pressure and self-gravity affect the velocities through the existing evolution, not through a new particle-number source.

For a unit-normalized radial window W in comoving coordinates, average the regular, exterior-matched quadrupolar Poisson solution. Its radial trace-free tide is ∫k d dr, with

    k(y) = −W(y)/3 + (6/5)y⁴ ∫[y,∞] W(r) dr/r⁵ + (1/5y)∫[0,y] W(r) dr .

Integration by parts gives the instantaneous matter contribution

    ∫[(k'−2k/r)J + 6kU/r²] dr − [kJ] at the boundaries.

For the saved proper ruler, W(r)=A W₀(Ar), A=a/a_launch. Multiply by A⁻³ and differentiate both the dilution and the moving window. Convert conformal rates to log(a) with the saved conformal Hubble rate, and then to the *same* proper clock via the saved normal histories. The discrete test function is the detector row divided by the assembled radial mass diagonal. Its transpose acting on the two fluxes directly avoids differentiating two nearly equal total densities. The density derivative is **not** an input to the readout. We reused the existing evolution to supply histories; this is an alternative readout, not an independent matter solver.

At a fixed cut R beyond the aperture, the external contribution before dilution is ∫[R,L] d/(5r) dr. Its conformal derivative is

    ( J(R)/R − J(L)/L + ∫[R,L] (−3J/r² + 6U/r³) dr )/5 .

This exterior formula can be checked without the detector transpose. We used the average of the two element traces at R=6; the one-sided half-difference is recorded, not assumed zero. The same identity gives an error bound: replace each current by its error, take absolute values of each face and each integrand, add the dilution error on this moment, and integrate on the proper clock with the same positive conversion factors. This bounds an error **given** errors on the source and boundary; the signed cancellation above is not itself such an envelope.

**Unknown exterior gravity is a different input.** An independently varying regular vacuum potential b r² P₂ inside the entire 120 Mpc domain has zero density and a nonzero radial trace-free tide −2b (P₂ coefficient). No internal continuity residual can exclude it. In launch curvature units, if this were the only unbudgeted term, the strictest final 20 ppm allowance across the four controls requires |Δb_wave−Δb_cold| ≤ 6.43e−24 in the corresponding physical-curvature normalization (unrounded limit 1e−5 times the smallest absolute full change above). This is a required accuracy, not an independently measured cosmological boundary value. A boundary contribution common to the matched histories cancels.

## Checks and scope

- Fixed aperture, grid, histories and 20 ppm tolerance; no fit. Both preparations, both signs and both widths, nine saved times: 72 branch comparisons. Direct current reconstruction versus the archived density-route integral agrees within 3.1e−6 ppm in the 32 nonzero paired contrasts. This tests the weak conservation identity, not continuum accuracy.
- Direct exterior continuity versus the external part of the discrete density kernel differs by at most 0.00109 ppm **of the full paired tide**. Analytic radial outflow and purely angular flow separately test the derivative, boundary sign and angular factor.
- Integrated terms by branch (not bundled here), paired contrasts (not bundled here), [analytic controls](evidence-001.zip) (archive member: `controls.csv`). In the paired CSV, only the first eight terms sum to the total. The exterior terms are a breakdown of part of that total, **not** extra force.
- This fixes the Newton reference and the finite-radius matching term. The corresponding relativistic energy continuity includes metric volume and KᵢⱼSⁱʲ work. It is not particle-number continuity. **Next parent test:** reconstruct that work and the normal current of the surrounding fields on the saved trace-preserving spacetime histories, and compare the matched 6 Mpc exterior term on the same clock. Do not assign the isolated finite-mass bound to the whole cosmological background.
- Local replay: run `python -B current_transfer.py` in this directory using the retained Python 3.13, NumPy and SciPy. Compares rather than overwrites existing tables. Pinned source inputs include the existing clock, speed-family reference and signed launch states.
