> Public reading copy: local links are mapped to released material or marked unavailable. Machine-specific passages, where present, have been omitted. See the inventory for the original digest.

# Palomar 5: how much of its history, and could it tell the flows apart?

**The motions differ; the data in this test cannot reliably select the direction.** The two signed stellar trajectories overlap for 88.968349 + 22.190427 = **111.158776 Myr**. That is **5.73%** of [Odenkirchen et al.'s trailing-tip drift estimate](https://arxiv.org/html/astro-ph/0307446) (1.94 Gyr) or **2.22%** of the [Fritz & Kallivayalil disruption simulation](https://arxiv.org/abs/1508.06647) (5 Gyr). These are reference clocks with different meanings, not lower and upper age measurements. The 425 Myr and 1.066 Gyr forward formation archives do not supply longer matched signed debris histories.

| Nominal 22.05 kpc comparison | Reset wave | Inherited wave |
|---|---:|---:|
| Largest displacement relative to cluster, pc | 48.43 | 54.37 |
| Forward minus reverse velocity gradient, km/s per degree | +0.0651 | −0.0798 |
| Magnitude divided by quoted gradient error (0.15) | 0.434 | 0.532 |

At all three tested distances the largest individual displacement is 68.08 pc; the velocity-gradient split never exceeds 0.646 of its error. The strongest 20-bin sky-track separation is 1.263 under independent bin errors, dropping to 0.168 when a common track tilt is free in that same case. The observations used for the starting geometry are not held-out residuals.

**Stripping time:** on both saved grids the opposite direction brackets 34/36 single-coordinate targets for **each** preparation when the mock release time is allowed to vary by ±10 Myr. These are coordinates, not 68 of 72 independent stars. With one date shared between both tail launches and all six coordinates, at least one coordinate retains 91.1–100% (reset) or 69.6–100% (inherited) of its same-date difference. A common date cannot erase the entire physical signal; retaining a fraction of a small signal doesn't make it measurable. The ±10 Myr window is a sensitivity test, not a measured distribution of stripping dates. No timing prior was fitted or convolved with the observation errors.

**Where better data could help:** on the [17 catalogue RR Lyrae](https://arxiv.org/abs/1910.00595), the saved Gaussian distance/proper-motion forecast gives 57.76% or 57.55% optimal sign recovery with equal sign odds and known preparation. With preparation unspecified, the best worst-state accuracy cannot exceed 51.34%. For any two equal-covariance hypotheses a noise-weighted separation d gives optimal accuracy Φ(d/2). Holding the same 17 stars and the prediction fixed, reaching 80% would take **4.30× or 4.42× smaller standard errors in every noise direction** if the preparation were known. With it unknown, even the closest opposite-direction pair needs **25.09×**; that's necessary, not sufficient for the four-state problem. This exercise uniformly scales even shared errors; it is not an observing-time estimate. It does not assume older debris accumulates this separation linearly.

[Checked release counts](evidence-001.zip) (archive member: `stream-release-recheck.csv`) · precision thresholds (not bundled here) · [source forecast](../mts-pal5-astrometric-separation/RESULTS.md) · [signed trajectories](../mts-pal5-joined-flow-586-600/RESULTS.md). Recheck uses five hash-verified saved inputs, no new orbit, no parameter or tolerance change. The separate GD-1 response reported alongside this note is **not** extra Pal 5 coverage or a sign determination.
