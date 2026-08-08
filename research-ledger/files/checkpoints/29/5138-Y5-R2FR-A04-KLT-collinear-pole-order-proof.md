# 5138: A04 KLT collinear pole-order proof

## Exact implemented-integrand result

At the active small beam root, only the left-cut angle bracket `b=<1 0>`
vanishes, and it has a simple zero. In the four KLT permutation pairs, the only
term with two Parke-Taylor factors `b^-2` also contains the momentum-kernel
factor `s21 proportional to b`. Its net order is therefore `b^-1`. Every other
permutation is finite after the same kernel accounting. The `special=1`
numerators add `b^4`; only `special=2,3` retain the simple pole.

The opposite chirality and both right-cut chiralities are nonzero at this root,
so the `hhh` cut product cannot square the pole. The remaining energy factors
are finite and the next log singularity is separated by
`0.1682261096530895`. Linear global-cycle
integration cannot raise the isolated meromorphic order.

- Maximum implemented scalar-KLT pole order: `1`.
- Simple pole proved: `True`.
- Double pole excluded: `True`.
- A deeper numerical chart may now be used to resolve the residue; no threshold
  or physical equation has been changed.

## Scope

This proves the pole order of the implemented coefficient integrand, not a UV,
local-GR, galaxy, or full-MTS claim. No coefficient job was executed, the pilot
remains `50/560`, and the formalization tree remains `b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758`.
