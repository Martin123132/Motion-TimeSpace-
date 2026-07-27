# Recovery Bookmark — 2026-07-03 local head 4248 after drive swap

This bookmark marks the verified private local head after the storage replacement, backup-branch comparison, and 4248 validation.

## Canonical local project

- Path: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main`
- Status: canonical local working copy found on the new `D:` drive.
- Latest observed private checkpoint: `post-checkpoint-work\4248-Y5-R2FR-epsilon-geom-profile-sampler-or-coframe-shadow-bound-first-row.md`
- Latest observed formal spine file: `formalization-workbench\264-PPC4161-epsilon-geom-profile-sampler-or-coframe-shadow-bound-first-row.md`
- Latest observed script: `post-checkpoint-work\scripts\Y5_R2FR_4248_epsilon_geom_profile_sampler_or_coframe_shadow_bound_first_row.py`
- Latest observed validation bundle: `post-checkpoint-work\source-intake\mts_residuals\P8_Y5_BRR545_4248_VALIDATION.csv`

## 4248 validation state

- Python compile: passed.
- Validation rows: `15/15` passed.
- Runtime cache: `post-checkpoint-work\scripts\__pycache__` removed after validation.
- Claim state: non-claim. The sampler is built, but numeric profile and transfer inputs are still missing.

## GitHub backup comparison

- Backup repo: `Martin123132/laptop-back-up-`
- Relevant recovery branch checked: `codex/mts-recovery-after-drive-swap-20260703-044902`
- Recovery branch commit checked: `70a662b`
- Recovery branch commit message: `Back up MTS drive-swap recovery through 4187`
- Secondary branch checked: `codex/mts-framework-since-bookmark-20260702`
- Secondary branch commit checked: `7457fea`
- Secondary branch commit message: `Back up MTS framework since bookmark`

## Local work newer than GitHub backup

The `D:` local project is ahead of the GitHub recovery branch. Do not restore over it from GitHub.

- Private checkpoints newer than the recovery branch: `4188` through `4248`
- Formal PPC4161 files newer than the recovery branch: `204` through `264`
- Current local head: `4248`
- Current safe continuation target: `4249-Y5-R2FR-fill-hU-response-or-coframe-transfer-constant-first-source-row`

## Recovery decision

Treat the `D:` local project as canonical. The GitHub backup is useful history, but it is not current for the live framework head. No restore is required before continuing.

## Next framework target

Resume from `4248` into the coframe-transfer/profile route:

- Try to theorem-bound or source-fill `h_U_response`.
- If `h_U_response` cannot close directly, try to source or derive `C_coframe_hU`.
- Keep the result non-claim unless source-backed numeric rows or a parent-signed zero theorem closes the sampler.
- Do not claim local GR, PPN, clock, orbital, or R10 success from the sampler while `valid_for_claim=false`.
