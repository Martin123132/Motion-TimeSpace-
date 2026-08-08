# Lossless MTS Research Ledger

This directory is the byte-exact, physically sharded publication snapshot of
the private `post-checkpoint-work` ledger through private checkpoint
`5252` on 2026-07-27.

It exists because the earlier compact public sequence was deliberately curated
and its flat directories exceeded GitHub's ordinary folder-display limit.
GitHub's interface could therefore look incomplete even when the Git objects
were present. This ledger fixes both problems:

- every selected local source file is copied byte-for-byte;
- every published file has a size and SHA-256 row in `manifests/`;
- files are distributed by stable two-character path-hash buckets;
- no physical directory may exceed 500 entries;
- bounded direct-link indexes live in `catalogue/`;
- `snapshot.json` records the aggregate manifest digest.

## Scope

The snapshot contains 57,444 source files totalling
397,143,891 bytes:

- **checkpoints**: 5,239 files, 72,285,641 bytes
- **residuals**: 46,385 files, 121,455,576 bytes
- **runs**: 242 files, 35,699,500 bytes
- **scripts**: 5,578 files, 167,703,174 bytes


The selected run evidence is limited to private checkpoints
`5250`-`5252`. The remaining multi-gigabyte
`functional_rg` cache, virtual environments, and third-party datasets are not
committed.

## Integrity

Run:

```powershell
python tools/build_lossless_research_ledger.py --verify-only
```

The verifier checks every manifest row against the committed byte stream,
detects missing or extra ledger files, verifies the aggregate digest, enforces
the directory-entry ceiling, and confirms the latest scripts and validations
are present.

This ledger is an audit trail, not a promotion of every historical result.
The repository's root `CLAIM_CEILING.md` remains controlling.
