# Verified MTS work through November 7, 2026

Start with the [plain-language status](../../../docs/status/STATUS-2026-11-07.md)
and [source reading guide](READING-GUIDE.md). The previous September 21 release
remains intact; this dated package adds completed work rather than replacing it.

## What is here

- Completed annular-action audits through the October 3 sealed frontier.
- Sealed condensate, finite-body, cosmology, kinetic-source and response work.
- Verified individual-scattering receipts through direction 38 of 128.
- The November 7 action, metric, GR/Poisson comparison and qualified
  cold-background series.
- Completed negative tests and repaired failed attempts, with their original
  labels and qualifications intact.

The latest included cold-background closeout has SHA-256
`3cf78fb90a99a5b6c6527e29b221bccfd508a7c1df589b62ab47fac8e4df580f`.
The next relative-phase perturbation draft is deliberately not included.
No unfinished calculation is promoted by publishing its predecessors.

## Complete inventory, without relying on GitHub's truncated views

- [Reading guide and stage navigation](READING-GUIDE.md)
- [Bounded file catalogue](catalogue/README.md): at most 160 source rows per page
- [MANIFEST.csv](MANIFEST.csv): counts and hashes for every manifest part;
  [manifest parts](manifest/README.md) contain every selected source path,
  public location, byte length, expected SHA-256, disposition and authority
- [Completed source seals](SEALS.json)
- [Explicit exclusions](EXCLUSIONS.json)
- [Export counts and byte totals](EXPORT-REPORT.json)

Every included source is copied byte-for-byte and checked as a Git blob.
Payloads are hash-sharded into small folders; no scientific file is shortened
to make it fit a listing. Large manifest files can be downloaded using GitHub's
**Raw** or download control even if the web preview does not show every row.

Some raw numerical products, third-party downloads/builds, duplicate rollback
snapshots and mutable resume notes remain local. Their manifest dispositions
are deliberate exclusions, not missing/truncated uploaded files. Expected
hashes of omitted large products come from the scientific seals; this release
does not rehash all raw arrays or claim to be a complete raw-data backup.

## Verify or restore

From the repository root:

```text
python tools/publish_verified_20261107.py --verify HEAD
python tools/publish_verified_20261107.py --restore NEW_DIRECTORY
```

Restore refuses an existing destination. It reconstructs included original
source paths under `post/` and `data/`, not the omitted caches or machine
environment. Research code retains its recorded absolute paths; a portable
end-to-end rerun requires dependency/path setup and the omitted inputs.

Publication integrity is separate from scientific validation. The results
remain conditional on the equations, states, finite grids and tests described
in their sources. See the [publication notes](../../../docs/status/PUBLICATION-NOTES-2026-11-07.md)
for scope, licences and exclusions. Existing repository terms are unchanged;
no new rights in third-party packages or data are asserted.
