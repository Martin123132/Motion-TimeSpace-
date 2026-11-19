# Causal memory with the recovered preparation as its boundary condition

## 1. Exact local block from the retained scalar equations

All quantities retain the previous stage's conformal/Mpc units, k=5/Mpc and beta=a/R0. At each original historical node define the normalized cross state in row-major order

    j=(beta*b*u, beta*b*w, beta*v*u, beta*v*w).

The original equations are b'=v+Ef, v'=-2H*v-mu²*b+Eb, u'=w, w'=-2H*w-(mu²+k²)*u-k*z*v, with beta'=H*beta and (mu²)'=2H*mu² for this equation-owned clock. Ef/Eb are the saved background representation defects, not new physical forces. Direct differentiation gives j'=A_free*j+f_z+f_defect, with

    A_free = [[ H,             1,             1,    0],
              [-(mu²+k²),    -H,             0,    1],
              [-mu²,          0,            -H,    1],
              [ 0,         -mu²,    -(mu²+k²),  -3H]],
    f_z = -k*z*(0, beta*b*v, 0, beta*v²).

On the coherent source subspace, f_defect can be written as a nonsingular linear operator without dividing by b or v separately. Put aB=b²+(v/mu)²>0 and let the rows

    l_u=(b,0,v/mu²,0)/aB,
    l_w=(0,b,0,v/mu²)/aB.

Then l_u*j=beta*u and l_w*j=beta*w, hence the defect operator has rows (Ef*l_u, Ef*l_w, Eb*l_u, Eb*l_w). This is the preparation-owned coherent lift; its action on off-subspace vectors is a specified algebraic extension, not an independent physical state prescription.

Crucially include the current scalar's self-gravity BEFORE extraction:

    Dnorm=o_D*j,  o_D=(mu²,0,0,1),
    z=zeta+Dnorm/(2*k*H*beta),
    A=A_free+A_defect - outer((0,beta*b*v,0,beta*v²),o_D)/(2H*beta),
    f=-k*zeta*(0,beta*b*v,0,beta*v²).

zeta is a readout of the CURRENT other species/metric. It is not a prescribed future time series in a coupled calculation. To close the full system, append those existing rest variables and their native equations; do not invent zeta'=0 for physical evolution. For an explicitly frozen local operator control only, f may be held fixed and labelled as such.

Physical source rows are

    O = [[mu²,0,0,1],[0,0,k,0],[-mu²,0,0,1]],
    O' = [[2Hmu²,0,0,0],[0,0,0,0],[-2Hmu²,0,0,0]],
    Y'=O'*j+O*(A*j+f).

This pressure-inclusive equation readout needs no numerical differentiation of perturbation histories.

## 2. Resolved and unresolved history evolve together

Use the ORIGINAL frozen linear functional L[j]=sum_i weights_i*j_i, with sum weights=1. It is signed, not a probability measure. Write m=L[j], h_i=j_i-m, Abar=L[A], fbar=L[f]. The exact projected system is

    m'=Abar*m + L[A*h] + fbar,
    h_i'=(A_i-Abar)*m + A_i*h_i-L[A*h] + f_i-fbar.

L[h]=0 is invariant. The initial h_i comes from the retained preparation, not a zero choice. Its subsequent evolution generates both a freely transported initial-memory contribution and a driven contribution. Setting h=0 changes the equations unless all the forcing/operator correlations genuinely vanish.

The physical source Ybar=L[O*j] is NOT simply Obar*m:

    Ybar=Obar*m+C,  C=L[O*h],  Obar=L[O],
    C'=L[O'*h + O*h'],
    Ybar'=Obar'*m+Obar*m'+C'.

The original phase-corrected carrier readout is separately retained from the prior stage. This j-coordinate lift supplies an explicit equation-owned transport and source-map derivative, not a replacement definition of that carrier or an assertion that its memory has vanished. Different resolved coordinates give different numerical memory components; the total physical sources/rates must agree.

## 3. Retarded kernel, with NONZERO initial forcing

For the fully coupled linear perturbation system, stack the existing rest and scalar variables at the history nodes as X. Let J embed a common resolved vector, P=J*L, Q=I-P and let the full local operator be mathcalA(t). This is an algebraic projector even with signed weights; it need not be orthogonal or positive. With fixed weights, define U_Q(t,s) on the Q-subspace by d_t U_Q=Q*mathcalA(t)*U_Q and U_Q(s,s)=Q. Eliminating the unresolved history gives

    m'(t)=L*mathcalA(t)*J*m(t) + I(t)
          + integral_from_tb_to_t K(t,s)*m(s) ds,
    I(t)=L*mathcalA(t)*U_Q(t,tb)*h_b,
    K(t,s)=L*mathcalA(t)*U_Q(t,s)*Q*mathcalA(s)*J.

Any external prescribed forcing has its usual projected and retarded terms; in the physical application the other-species response belongs in mathcalA and is not an external saved future force. U_Q(t_b,t_b)h_b=h_b, so the initial term is fixed by preparation and is generally nonzero. This derivation makes no Markovian or constant-memory approximation. A compact closure still needs a demonstrated approximation to this kernel, not just its formal existence.

## 4. Causal availability of the original temporal preparation

The inherited extraction uses nodes on both sides of its nominal center a0. Therefore it is not a causal point-state at that center. Let tau_b=max(tau_i) and lag_i=tau_b-tau_i>=0. The SAME prepared samples can be treated as a historical record at tau_b, and advanced as delayed readouts X_i(s)=X(tau_b+s-lag_i). Each sample then refers only to the past/current physical state. This relabels availability; it does NOT equate the old center-normalized source to the physical instantaneous source at tau_b or alter the saved matching epoch. Native initial data at tau_b must be genuinely captured before a new coupled continuation.

The history lift is not902 independent physical fields. Nor can independently evolved coarse histories be assumed to remain time translations without the parent trajectory/boundary consistency. The frozen control below tests the algebraic memory transport on prepared coefficients only, not that additional physical consistency.

## 5. Tests with unchanged gates

Evaluate all node-level sources and equation rates from the saved b,v,u,w and CURRENT saved metric source. Compare the independently differentiated products, the explicit self-gravity block and the projected resolved/unresolved rates, including O'. Compare cold dust under the same signed functional with its own normalization and no scalar pressure/phase.

For a distinct frozen-coefficient control retain every node's A_i,f_i at its initial prepared value. Solve its resolved/unresolved system, not the scalar-only mean, over one fixed small horizon defined in run_memory.py. Compare against independent per-node augmented matrix exponentials and refine the time step. This establishes nonzero-memory transport in that declared control; it is not a physical background evolution, dynamical ensemble assertion, late prediction or observational fit. Dropping initial memory is a separately saved negative control.
