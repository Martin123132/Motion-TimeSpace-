# 4256 - Y5 R2FR Dq projection spectral-gap bridge

Packet marker: `PPC4161_PACKET_DQ_PROJECTION_SPECTRAL_GAP_BRIDGE_4256`

## Result

The route now has an actual bridge theorem:

```text
P=Pi_kerDq true projector onto ker(Dq)
=> ker(Dq|_Hperp)=0
=> eta_Dq_kernel=0.
```

The physical amplitude constant is no longer vague:

```text
C_HDq = 1/sigma_0,
sigma_0 = inf_{||h||_F=1, h in Hperp complement} ||Dq h||_W.
```

## Still blocked

- `Pi_kerDq` must be source-signed as a genuine projector.
- `sigma_0>0` must be proved by finite-dimensional compactness or coercivity, or computed.
- `sigma_1` and the commutator bound must be proved for C1.
- All eight `epsilon_i` and `epsilon_i_C1` rows need zero proofs or profile/data envelopes.

## Claim status

Private nonclaim. This narrows the coupling/local-GR gap; it does not close it.
