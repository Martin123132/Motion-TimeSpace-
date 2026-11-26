# Where the stored fluid-minus-projected-wave difference comes from

Follow-up diagnostic on a previously exposed matched case. Freeze the signed channels before comparing them to native current differences. The source computation reads only the original table, matched geometry, microscopic wave and projector. No later native fluid energy, current or pressure is used to set an amplitude. Unlike the density-only control, the center launch is obtained by evolving the retained matching table from the actual switch. No arbitrary fade, free coefficient, or zeroing a measured mismatch.

Let δe=e_fluid−ē and δj=j_fluid−j̄, using the same dimensionless moments, metric and physical clock as METHOD.md. The *retained* flat-fluid pressure response has c=(k/am)²/[√(1+(k/am)²)+1]² and p_f=c(e_f+3Hj_f/k). Put p₀=c(ē+3Hj̄/k)−p̄. Evolution is linear in the two differences:

    δp = c(δe+3Hδj/k)+p₀
    δe′ = −3Hδp−kδj + (b̄+p̄_b−1)X − S_e
    δj′ = −Hδj + kδp − S_j.

At projection sample changes the fluid is continuous: the two differences change by minus the two slow-projection jumps. The signed propagated channels are (i) incoming difference; (ii) p₀ from the actual pressure operator; (iii) oscillatory background-enthalpy projection; (iv) smooth differentiated projection; (v) metric/work covariances; (vi) changes of projection support. Include all the terms; do not ascribe the physical sign to the largest unsigned contribution. Use independent full-fluid integration for checking the reconstruction and homogeneous unit responses to distinguish a mismatch already present on entry from subsequent forcing. If an exposed diagnostic replaces a computed center launch with a directly measured one, label it separately. Require 0.5% on the contrast itself, not just the far larger total current. This comparison of two effective descriptions on a given geometry is not a new photon calculation.
