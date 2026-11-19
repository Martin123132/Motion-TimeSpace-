# Gravitational, gas and wave work in the evolving boxes
The box carries conserved coordinate masses. Let f_i be the constant clustered mass fractions, j_i their mass currents (per species mean density), Ψ_self the periodic Newtonian potential from their densities alone, and n the gas density in units of its comoving mean. In units c=1 define

    K_i = ⟨n_i |v_i|²⟩/2  (ordinary components)
    K_h = ⟨|∇ψ|²⟩/(2m²a²)  (wave arm)
    W = ⟨Σ f_i(n_i−1) Ψ_self⟩/2
    B_γ = f_b ⟨n^γ−1−γ(n−1)⟩/[γ(γ−1)] .
    E = Σ f_i K_i + W + Σ c_γ²(a) B_γ .

Integrate the continuity equations and velocity/Schrödinger equations by parts in the periodic volume. The pressure current cancels the advection part of the internal energy derivative; the gravitational work cancels the derivative of W except for the expansion of its 1/a coefficient. With primes now d/d ln a,

    E' + 2K + W = Σ (c_γ²)' B_γ
       − ⟨Σ f_i j_i · ∇(Ψ−Ψ_self)⟩/Hc
       − f_b ⟨j_b · ∇(thermal gauge/entropy and photon-drag potentials)⟩/Hc .

This is an independent energy-balance check for the implemented weak-field, externally driven system. It is not a conservation proof for arbitrary relativistic material or a claim that the prescribed UV heating came from MTS. An energy measured from the fields on the left is compared to work computed from forces and thermodynamic coefficients on the right, not to another finite difference of the same energy.

In the first quadrature the heating ramp lay inside ordinary time cells. The wave work error was 5.88×10⁻⁵, concentrated at z=9 and z=7. Reusing the same fields, split the work integral exactly at those two prescribed background events and integrate the analytic coefficient derivative against the saved gas thermodynamic factor. No term was fit to the energy residual. With 640 steps the normalized errors were 1.09×10⁻⁸ (wave), 4.11×10⁻⁹ (pressure-off), 3.39×10⁻⁹ (all-cold) or smaller. Removing the explicit heating work instead leaves normalized residuals 0.382, 0.122 and 0.091. Both the original and repaired numerical budgets are retained. The normalization is peak |ΔE| plus the maximal accumulated absolute work, not the almost-zero residual itself. See energy-budget.csv, split-work.csv and work-split-*.npz.

