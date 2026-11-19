# Coherent reconstructed endpoint and its exact averaged-carrier remainder

This extends the retained real-scalar action and the original signed temporal extraction. It imports the verified native phase interface, not a new matter model. The response reconstruction uses the history up to the rightmost support time, original index2892. Thereafter the live reference and reconstructed runs carry the same rest-species state and fixed native caches and evolve their own metric. No future driving history is inserted.

## State and source map

At fixed retained background let b be the real scalar, v its conformal velocity, u the perturbation and w its velocity. Write mu²=(a m)², omega²=k²+mu². The constrained phase matrix is M=B U^T with B=(b,v/omega), U=(u,w/omega). It has two physical perturbation coordinates, not four independent occupations. Its sources are

    D = omega² M22 + mu² M11 = v w + mu² b u,
    P = omega² M22 - mu² M11 = v w - mu² b u,
    Q = k omega M21 = k v u.

The reconstruction supplies the entire physical block at the endpoint, including CDM, and leaves the rest of the native state unchanged. Existing phase equations then couple these sources directly to the live native metric and rest species. Numerical similarity scaling is not a new physical parameter.

The existing late implementation instead carries (delta,q), uses R0/a as its source normalization, and has a discrete selector set to one. Its pressure law is

    c² = [k/(a m)]² / [sqrt(1+[k/(a m)]²)+1]²,
    P_A = c² (delta + 3 H q/k),
    delta' = -3 H P_A - k q - k z,
    q' = -H q + k P_A.

These statements are read directly from MTS_AveragedPressure, MTS_Stress and MTS_Evolve in the retained native/fortran/MTSTwoField.f90; the late hierarchy port separately tests its selector1, k=5/Mpc, z=10 state. That late branch is not the same coordinates as the early coherent selector0, k=1/Mpc window here. The early averaged-input table is not independent positive-ensemble preparation.

## Exact remainder, without inventing a pressure fit

Use the original R0 in the temporal extraction and beta=a/R0. Let r=d ln(a_thermal)/d tau, H the native conformal Hubble rate, E_f=r b_N-v, E_b=r v_N+2Hv+mu²b. These E terms record retained background interpolation representation differences; they are not new physical forces. Define Y_D=beta D, Y_Q=beta Q, Y_P=beta P, and evaluate P_A=c²(Y_D+3H Y_Q/k) on these SAME coherent sources. Set R_P=Y_P-P_A.

Direct differentiation using u'=w and w'=-2Hw-(k²+mu²)u-k z v gives

    Y_D' = -3H P_A - k Y_Q - k z + R_D,
    Y_Q' = -H Y_Q + k P_A + R_Q,

where

    R_D = -3H R_P - k z (beta v² - 1)
          + (r-H)Y_D + beta E_b w + beta mu² E_f u
          + 2 beta (r-H) mu² b u,
    R_Q = k R_P + (r-H)Y_Q + beta k E_b u.

Thus simply replacing the late pressure coefficient is generally insufficient for the instantaneous coherent reference: its gravitational work coefficient beta v² is phase dependent as well. Even for an exact background representation r=H, E_f=E_b=0, two physical remainders remain: pressure phase and the oscillating background kinetic factor. Averaging may suppress them, but that suppression must follow the retained averaging/transport, not be asserted pointwise. A nonzero instantaneous remainder does not by itself invalidate an averaged approximation. These remainder equations compare descriptions on the SAME retained coherent background; replacing that background by an averaged background adds a separate background/metric matching question and is not silently included in this identity.

For v nonzero the coherent instantaneous relation P=D-2 mu² b Q/(k v) follows algebraically; it is not safe to use at v=0 and is not the window-averaged affine pressure relation. Retaining the phase matrix avoids dividing by v. At v=0, Q=0 and P=-D while w is invisible to the two instantaneous sources. This differs from the nonsingular finite-window response established in the previous stage.

## Why the kinetic remainder has a controllable boundary/history form

Let E=beta(v²+mu²b²)/2, J=beta b v and F=beta(E_f v+E_b b). Product differentiation gives the exact representation-aware identity

    beta v² - 1 = (E-1) + J'/2 + (2H-r)J/2 - F/2.

Consequently its accumulated metric work on any interval [t0,t1] is

    - integral k z (beta v²-1) dtau
      = -k [z J]_(t0)^(t1)/2
        - integral k z (E-1) dtau
        + integral k z' J/2 dtau
        - integral k (2H-r) z J/2 dtau
        + integral k z F/2 dtau.

This is integration by parts, not an assumed random phase. It separates the endpoint phase, background normalization, changing metric and expansion/representation terms. Even if a complete cycle suppresses a boundary difference, a changing z or E different from one leaves physical history terms. A quantitative suppression statement requires evaluating or bounding ALL of them and the pressure remainder together; the boundary term alone is not a sufficient estimate. For fixed-window weighted extraction, the weight derivative/jump terms must also be retained.

derive_work_boundary.py proves the decomposition and its work identity symbolically and tests the pointwise decomposition against both live histories. Its slow-field calculation is an algebra control only: the slow field is not promoted into a heavy dust carrier. No future-history integral or averaging suppression is claimed by that pointwise test.

## Numerical test and units

The actual code evaluates these identities at the fixed retained k=1/Mpc with tau in Mpc (c=1), r,H,k in inverse Mpc and source units inherited from the native 8piG-normalized perturbation convention. Y sources and old delta/q share the original extraction normalization. No units are changed or new normalization inferred. Source rates carry an additional inverse Mpc. Check the equations against direct product differentiation using the native primitive derivative, including the interpolation terms.

The signed temporal extraction used to reconstruct the endpoint remains an extraction, not a probability distribution. No positive ensemble, galactic occupation, primordial realization or new universal pressure law is claimed from this source/state continuation. The intended further bridge is a controlled average of the explicitly derived R_D/R_Q with live feedback, preserving their phase/memory until an error bound permits reduction.
