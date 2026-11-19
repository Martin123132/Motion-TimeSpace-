# Segment-aware integration of the scalar background-flow source

## Scope
Continue the sealed direct monopole/stress-balance calculation, not a new theory or background solve. The current diagnostic covers four geometrically selected MTS polynomial segments and both baseline segments inside original source cell8->12. The bank, physical histories, units, branch equations, source controls and gates remain unchanged.

## Derived source weight
With conformal-time dots, H=dN/dtau, omega^2=a^2 m^2, and background(phi,v), let F_phi=phi_dot-v and F_v=v_dot+2Hv+omega^2 phi. For scalar perturbations(u,w), the already-derived stress defects are:
```
epsilon_D = F_v w + omega^2 F_phi u
epsilon_J = k F_v u
Phi_flow_GR = -epsilon_D/(2k^2) - 3H epsilon_J/(2k^3)
Phi_flow_Poisson = -epsilon_D/(2k^2)
L = H (1 + 3 E_quad/(2k^2))
Delta r0|flow = (4/U0) mean(1/L) Delta Phi_flow
```
Delta means reference minus retained, with BOTH background defects kept. This is the flow piece of the exact finite-increment decomposition, not the whole metric-rate difference; the denominator variation and other pieces remain separate.

For the native unit-normalized monopole/quadrupole pair, r2 changes by -U0/U2 times the isolated r0 contribution. The final observable adjoint weight is:
```
a = physical_map^T inverse_metric_map^T endpoint_map^(-T) lambda
g_flow(N) = [a0 - (U0/U2) a2] Delta r0|flow
I_segment = integral g_flow(N) dN
```
All factors use the saved physical state and its own reference/retained mapping. No extra phase-clock factor occurs when integrating in N: the earlier dtheta/(dtheta/dN) measure is already dN. GR and Poisson-spatial branches are kept distinct.

## Piecewise-polynomial path
The accepted reference background is a serialized seventh-degree DOP853 dense polynomial on each saved segment. Its derivative is differentiated from that polynomial; replacing it by the ODE right-hand side would alter the source and is not done. Independent power-polynomial differentiation checks the alternating native recurrence.

At an internal left boundary the native search chooses the preceding segment. The diagnostic therefore evaluates nextafter(left,right) for the new segment's left endpoint, retaining the full original integration interval in the weights. At right boundaries the native left-sided selection already matches the selected segment. Node displacement is recorded; it is not a proven zero-error limit.

Nested9/17/33 nodes are fixed before source calls. Interpolatory weights solve the Chebyshev moments at actual binary nodes. A separate exact-endpoint normalization avoids midpoint rounding;90-digit Legendre moment evaluation independently tests those weights. Original freeze weights remain visible and are not silently overwritten. This correction concerns only arithmetic representation of the same integration interval and nodes.

## Matched controls
Fine and saved step-coarse current histories, fine and step-coarse phases, and three retained terminal-adjoint representations are evaluated on the same nodes. The phase/current cross term remains explicit. Independent90-digit stress-defect arithmetic and forward-versus-transpose observable mapping check the new samples. Baseline has no heavy scalar; its slow-flow and remaining source terms are still computed rather than assigning the whole baseline zero.

The sum of quadrature, current, phase, cross and adjoint changes is a conditional numerical indicator, not a rigorous continuum error enclosure. Passing selected-segment controls cannot qualify untested MTS segments or remove prior full-cell flags.

