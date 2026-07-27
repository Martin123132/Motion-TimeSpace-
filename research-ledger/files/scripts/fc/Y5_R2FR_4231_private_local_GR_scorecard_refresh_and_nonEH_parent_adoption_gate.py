from __future__ import annotations

import csv
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"
SCRIPTS = POST / "scripts"

CHECKPOINT = "4231"
CLAIM_ID = "L-072"
BRANCH = "MTS_R2FR_Y5_PRIVATE_LOCAL_GR_SCORECARD_4231"
DECISION = "PRIVATE_LOCAL_GR_SCORECARD_REFRESHED_PUBLIC_GLOBAL_CLAIM_BLOCKED_BY_NONEH_R10_AND_PARENT_ADOPTION"
MARKER = "PPC4161_PRIVATE_LOCAL_GR_SCORECARD_4231"
PACKET_MARKER = "PPC4161_PACKET_PRIVATE_LOCAL_GR_SCORECARD_4231"
NEXT_TARGET = "4232-Y5-R2FR-nonEH-coefficient-parent-zero-vector-or-local-bound-runner.md"

FORMAL_PATH = FORMAL / "247-PPC4161-private-local-GR-scorecard-refresh-and-nonEH-parent-adoption-gate.md"
DOC_PATH = POST / "4231-Y5-R2FR-private-local-GR-scorecard-refresh-and-nonEH-parent-adoption-gate.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4231_VALIDATION.csv"


@dataclass(frozen=True)
class SourceSpec:
    source_id: str
    path: Path
    required_text: str
    role: str


SOURCE_SPECS: Dict[str, SourceSpec] = {
    "SRC4231_00_4230_next": SourceSpec(
        "SRC4231_00_4230_next",
        SOURCE_DIR / "P8_Y5_R2FR_4230_NEXT_TARGET.csv",
        "4231-Y5-R2FR-private-local-GR-scorecard-refresh-and-nonEH-parent-adoption-gate.md",
        "4230 selected the private local-GR scorecard refresh and non-EH adoption gate.",
    ),
    "SRC4231_01_4230_formal": SourceSpec(
        "SRC4231_01_4230_formal",
        FORMAL / "246-PPC4161-MEH-total-epsilon-score-open-reference-virial-frame-gate.md",
        "M_H_ref_private >= M_EH_private > 0",
        "4230 private denominator pass.",
    ),
    "SRC4231_02_4230_decision": SourceSpec(
        "SRC4231_02_4230_decision",
        SOURCE_DIR / "P8_Y5_R2FR_4230_DECISION.csv",
        "full_private_selector_pass",
        "4230 machine-readable private pass and public-claim firewall.",
    ),
    "SRC4231_03_selector": SourceSpec(
        "SRC4231_03_selector",
        FORMAL / "190-PPC4161-parent-action-selector-or-local-branch-quarantine.md",
        "PPC4161-TK-HQNP-local-selector-private",
        "Local selector/quarantine contract.",
    ),
    "SRC4231_04_old_summary": SourceSpec(
        "SRC4231_04_old_summary",
        FORMAL / "195-PPC4161-local-GR-private-closure-summary-and-parent-adoption-burden-map.md",
        "Closed-Private Local Chain",
        "Earlier private closure summary, now superseded/refreshed by 4231.",
    ),
    "SRC4231_05_coupling": SourceSpec(
        "SRC4231_05_coupling",
        FORMAL / "194-PPC4161-calibrated-source-coupling-kappa-to-GN-law.md",
        "numeric G_N predicted = false",
        "Calibrated source-coupling law and numerical-G firewall.",
    ),
    "SRC4231_06_ppn": SourceSpec(
        "SRC4231_06_ppn",
        FORMAL / "188-PPC4161-full-PPN-readout-vector.md",
        "R_PPN =",
        "Private PPN zero vector.",
    ),
    "SRC4231_07_empirical": SourceSpec(
        "SRC4231_07_empirical",
        FORMAL / "189-PPC4161-local-empirical-validation-pack.md",
        "R10 is anchor-only here",
        "Private local empirical comparator pack and R10 caveat.",
    ),
    "SRC4231_08_noneh": SourceSpec(
        "SRC4231_08_noneh",
        FORMAL / "201-PPC4161-extra-invariant-residual-coefficient-map.md",
        "all_coefficients_numeric_or_parent_zero = false",
        "Non-EH coefficient map showing the global/public blocker.",
    ),
    "SRC4231_09_EM": SourceSpec(
        "SRC4231_09_EM",
        FORMAL / "223-PPC4161-EM-Poynting-Hodge-source-owner-lock.md",
        "Poynting flow = energy transport through the observed Hodge/coframe structure",
        "EM/Poynting source ownership and deformation gates.",
    ),
    "SRC4231_10_source_charge": SourceSpec(
        "SRC4231_10_source_charge",
        FORMAL / "227-PPC4161-Htau-MHsource-parent-charge-owner.md",
        "M_H^dress[W_H;tau] = H_tau[S_link] - H_ref",
        "Hamiltonian/Hilbert mass-charge owner contract.",
    ),
    "SRC4231_11_G_caveat": SourceSpec(
        "SRC4231_11_G_caveat",
        FORMAL / "222-PPC4161-calibrated-GN-bridge-and-source-charge-caveat.md",
        "MTS does not need to numerically predict G_N to reduce to GR/Newton",
        "Clarifies calibrated-G competitiveness against GR.",
    ),
    "SRC4231_12_R10_template": SourceSpec(
        "SRC4231_12_R10_template",
        SOURCE_DIR / "MTS_local_residual_predictions_TEMPLATE.csv",
        "R10_fifth_force",
        "R10 row requiring an actual fifth-force/Yukawa curve or mapped envelope.",
    ),
    "SRC4231_13_R11_template": SourceSpec(
        "SRC4231_13_R11_template",
        SOURCE_DIR / "MTS_local_residual_predictions_TEMPLATE.csv",
        "R11_EH_operator_ledger",
        "R11 non-EH operator coefficient row.",
    ),
}


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def common() -> Dict[str, str]:
    return {"timestamp_utc": now(), "branch_id": BRANCH, "checkpoint_id": CHECKPOINT}


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def write_csv(path: Path, rows: List[Dict[str, str]]) -> None:
    if not rows:
        raise ValueError(f"cannot write empty csv: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: List[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def append_once(path: Path, marker: str, block: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    existing = read_text(path)
    if marker in existing:
        return
    with path.open("a", encoding="utf-8") as handle:
        if existing and not existing.endswith("\n"):
            handle.write("\n")
        handle.write("\n" + block.strip() + "\n")


def source_rows() -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    for source in SOURCE_SPECS.values():
        text = read_text(source.path)
        rows.append(
            {
                **common(),
                "source_id": source.source_id,
                "path": str(source.path),
                "exists": str(source.path.exists()),
                "required_text": source.required_text,
                "required_text_found": str(source.required_text in text),
                "role": source.role,
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
    return rows


def private_branch_rows() -> List[Dict[str, str]]:
    data = [
        (
            "PBC4231_0_selector_scope",
            "compact local selector scope",
            "PPC4161-TK-HQNP-local-selector-private + 4230 full private denominator selector",
            "Defines where the branch pass is valid: compact ordinary-source local collars with no hidden flux/readout leak.",
            "PRIVATE_BRANCH_PASS",
        ),
        (
            "PBC4231_1_EH_principal_block",
            "EH/Palatini local metric block",
            "same-metric EH/Palatini principal block selected in the private IR branch",
            "Gives the GR local metric operator used by Newton and PPN readout.",
            "PRIVATE_PASS_GLOBAL_PARENT_DEBT",
        ),
        (
            "PBC4231_2_calibrated_coupling",
            "source-blind calibrated coupling",
            "G_cal = c^4 kappa_eff/(8*pi), D_A ln kappa_eff = 0, numeric G_N not predicted",
            "This is GR-competitive: one universal calibrated coupling, not orbital-GM laundering.",
            "PRIVATE_PASS_NUMERIC_G_NOT_PREDICTED",
        ),
        (
            "PBC4231_3_Hilbert_Hamiltonian_source",
            "Hilbert/Hamiltonian source charge",
            "T_H single source, M_H^dress=H_tau-H_ref, E_plus=E_H^dress>0",
            "4230 closes the positive denominator in the dressed private selector.",
            "PRIVATE_PASS_WITH_REOPEN_RULES",
        ),
        (
            "PBC4231_4_EM_Poynting",
            "Maxwell-Hodge and Poynting stress",
            "ordinary EM/Poynting is T_EM inside T_total, not a second background source",
            "Poynting intuition is retained safely as Hilbert flux; MTS EM deformations remain explicit gates.",
            "PRIVATE_PASS_DEFORMATION_GATES_RETAINED",
        ),
        (
            "PBC4231_5_boundary_frame_quotient",
            "boundary, frame, quotient, reference locks",
            "no-flux/fixed-reference/same-frame/quotient-natural locks close epsilon_abs privately",
            "These locks are legitimate only if parent-selected before variation and comparison.",
            "PRIVATE_PASS_WITH_REOPEN_RULES",
        ),
        (
            "PBC4231_6_denominator",
            "MEH/MHref denominator",
            "epsilon_E_private=0, M_EH_private>0, epsilon_abs_private=0, M_H_ref_private>0",
            "This is the new 4230 milestone: private denominator positivity is scored.",
            "PRIVATE_DENOMINATOR_PASS_NONCLAIM",
        ),
    ]
    return [
        {
            **common(),
            "score_id": score_id,
            "clause": clause,
            "score_statement": statement,
            "meaning": meaning,
            "status": status,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for score_id, clause, statement, meaning, status in data
    ]


def readout_rows() -> List[Dict[str, str]]:
    data = [
        (
            "LGR4231_0_GR_field_equation",
            "local GR field equation",
            "G_munu[g_obs]=kappa_eff T_H_munu",
            "structurally closed inside private selector",
            "PRIVATE_PASS",
        ),
        (
            "LGR4231_1_Newton_Poisson",
            "Newton/Poisson limit",
            "nabla^2 Phi_N=4*pi G_cal rho_H; a_r=-G_cal M_H^dress/r^2",
            "closed with calibrated G, not numerical-G prediction",
            "PRIVATE_PASS_CALIBRATED_G",
        ),
        (
            "LGR4231_2_PPN_vector",
            "PPN vector",
            "R_PPN=(gamma-1,beta-1,alpha_i,xi,zeta_i,Gdot/G)=0",
            "formal private PPN readout closes if selector clauses hold",
            "PRIVATE_PASS_REACTIVATION_RULE_ACTIVE",
        ),
        (
            "LGR4231_3_EM_Maxwell_stress",
            "Maxwell/EM stress",
            "T_EM and Poynting enter T_total once through observed Hodge/coframe",
            "ordinary EM stress owned; MTS-Hodge/constitutive deformation rows retained",
            "PRIVATE_PASS_DEFORMATION_GATES_RETAINED",
        ),
        (
            "LGR4231_4_source_coupling",
            "calibrated source coupling",
            "one source-blind kappa_eff and one Hilbert source measure",
            "structural GR reduction does not require predicting numerical G_N",
            "PRIVATE_PASS_NUMERIC_G_NOT_PREDICTED",
        ),
        (
            "LGR4231_5_denominator",
            "source denominator",
            "M_EH_private>0 and M_H_ref_private>0",
            "4230 supplies the private denominator pass missing in the older 4179 summary",
            "PRIVATE_PASS_NEW_4230_MILESTONE",
        ),
        (
            "LGR4231_6_global_status",
            "global/public status",
            "public_local_GR_claim=false; global_parent_adoption=false",
            "private pass is not a public derived-GR theorem",
            "PUBLIC_CLAIM_BLOCKED",
        ),
    ]
    return [
        {
            **common(),
            "readout_id": readout_id,
            "readout": readout,
            "formula_or_result": formula,
            "score": score,
            "status": status,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for readout_id, readout, formula, score, status in data
    ]


def public_debt_rows() -> List[Dict[str, str]]:
    data = [
        (
            "PDB4231_0_global_parent_action",
            "global parent-action adoption",
            "not proved",
            "Need one parent action that owns the local selector without contradicting galaxy/cosmology/time/EM/quantum branches.",
            "BLOCKS_PUBLIC_GLOBAL_CLAIM",
        ),
        (
            "PDB4231_1_nonEH_coefficients",
            "non-EH/R11 coefficient vector",
            "all_coefficients_numeric_or_parent_zero=false",
            "Torsion, R2, disformal, memory, boundary and source-normalization residuals must be parent-zero, heavy/screened, or bounded.",
            "BLOCKS_PUBLIC_LOCAL_GR_CLAIM",
        ),
        (
            "PDB4231_2_R10_curve",
            "R10/fifth-force curve",
            "R10 currently anchor-only/private; full alpha(lambda) curve or mapped envelope missing",
            "A public local claim needs full curve/source-backed bounds, not only an anchor sentence.",
            "BLOCKS_PUBLIC_EMPIRICAL_CLAIM",
        ),
        (
            "PDB4231_3_raw_local_reanalysis",
            "raw local empirical reanalysis",
            "private comparator pack exists; raw-data reanalysis not run",
            "PPN/WEP/clocks/orbital/R10 rows need reproducible source-bound refresh before public use.",
            "BLOCKS_PUBLIC_EMPIRICAL_CLAIM",
        ),
        (
            "PDB4231_4_numeric_G",
            "numerical G_N prediction",
            "numeric_G_N_predicted=false",
            "This is not fatal relative to GR, but it must be stated: G is calibrated unless a parent scale law is derived.",
            "NOT_REQUIRED_FOR_GR_COMPETITIVENESS_BUT_BLOCKS_NUMERIC_G_CLAIM",
        ),
        (
            "PDB4231_5_sector_interfaces",
            "galaxy/cosmology/open-memory/radiative interfaces",
            "not erased by local selector",
            "Interface fluxes must be exact no-flux/support-separated or explicitly bounded when sectors couple.",
            "BLOCKS_GLOBAL_UNIFICATION_CLAIM",
        ),
        (
            "PDB4231_6_exotic_sources",
            "exotic/negative-energy/independent stabilizer cases",
            "outside ordinary stable-source collar",
            "4230 assumes positive dressed Hilbert source support; exotic cases reopen beta/bound rows.",
            "SCOPE_LIMIT",
        ),
    ]
    return [
        {
            **common(),
            "debt_id": debt_id,
            "debt": debt,
            "current_evidence": evidence,
            "required_next_action": action,
            "status": status,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for debt_id, debt, evidence, action, status in data
    ]


def empirical_rows() -> List[Dict[str, str]]:
    data = [
        (
            "EMP4231_0_PPN",
            "PPN gamma/beta/alpha/xi/zeta vector",
            "0 in private selector",
            "source-backed comparator pack exists",
            "PRIVATE_PASS_PUBLIC_REFRESH_NEEDED",
        ),
        (
            "EMP4231_1_WEP",
            "WEP eta",
            "0 in private selector",
            "MICROSCOPE-style bound class in 189",
            "PRIVATE_PASS_PUBLIC_REFRESH_NEEDED",
        ),
        (
            "EMP4231_2_clock",
            "clock/redshift alpha",
            "0 in private selector",
            "Galileo/redshift bound class in 189",
            "PRIVATE_PASS_PUBLIC_REFRESH_NEEDED",
        ),
        (
            "EMP4231_3_Gdot",
            "local Gdot/G",
            "0 in private selector",
            "LLR-style bound class in 189",
            "PRIVATE_PASS_NUMERIC_REFRESH_NEEDED",
        ),
        (
            "EMP4231_4_orbital",
            "orbital inverse-square/Newton readout",
            "a_r=-G_cal M_H^dress/r^2 in private selector",
            "Hamiltonian source charge; no orbital GM input",
            "PRIVATE_PASS_PUBLIC_REFRESH_NEEDED",
        ),
        (
            "EMP4231_5_R10",
            "short-range/fifth-force alpha(lambda)",
            "alpha_Yukawa=0 only if non-EH/fifth-force coefficients are zero in selector",
            "R10 is anchor-only; full curve/mapped envelope still missing",
            "PRIVATE_ANCHOR_PASS_FULL_CURVE_BLOCKER",
        ),
        (
            "EMP4231_6_R11",
            "non-EH operator ledger",
            "zero only inside full private Palatini/EH selector",
            "global coefficient vector not parent-zero or numeric",
            "PUBLIC_BLOCKER",
        ),
        (
            "EMP4231_7_EM",
            "EM/Poynting side channel",
            "ordinary EM stress owned once by T_EM",
            "Hodge/constitutive/radiative deformation gates retained",
            "PRIVATE_PASS_DEFORMATION_REFRESH_NEEDED",
        ),
    ]
    return [
        {
            **common(),
            "empirical_id": empirical_id,
            "arena": arena,
            "private_prediction": prediction,
            "evidence_status": evidence_status,
            "status": status,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for empirical_id, arena, prediction, evidence_status, status in data
    ]


def decision_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "decision": DECISION,
            "private_local_GR_scorecard_refreshed": "True",
            "private_selector_pass": "True",
            "private_denominator_pass_imported_from_4230": "True",
            "public_local_GR_claim": "False",
            "global_parent_adoption": "False",
            "nonEH_global_coefficients_zero_or_numeric": "False",
            "R10_full_curve_claim_ready": "False",
            "raw_empirical_reanalysis_ready": "False",
            "numeric_G_prediction": "False",
            "next_highest_pressure": "nonEH/R11 coefficient parent-zero vector or local bound runner",
            "summary": "4231 refreshes the local-GR scorecard after 4230: the compact private selector now has a coherent GR/Newton/PPN/EM/coupling/denominator pass, but public/global promotion is blocked by non-EH coefficients, R10 full-curve evidence and global parent adoption.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def firewall_rows() -> List[Dict[str, str]]:
    data = [
        (
            "LGF4231_0_no_public_promotion",
            "Do not promote private selector pass to public local-GR claim.",
            "BLOCKED",
            "Global parent adoption and non-EH/R10 evidence remain unclosed.",
        ),
        (
            "LGF4231_1_no_R10_anchor_overclaim",
            "Do not use R10 anchor-only rows as a full alpha(lambda) pass.",
            "BLOCKED",
            "A full curve or mapped envelope is required for public R10 evidence.",
        ),
        (
            "LGF4231_2_no_nonEH_silence",
            "Do not silence non-EH coefficients outside the full private selector.",
            "BLOCKED",
            "R11 coefficient vector remains the next highest-pressure public blocker.",
        ),
        (
            "LGF4231_3_no_numeric_G_claim",
            "Do not claim MTS predicts numerical G_N.",
            "BLOCKED",
            "The current GR-competitive route uses one empirical calibration, like GR.",
        ),
        (
            "LGF4231_4_no_sector_erasure",
            "Do not erase galaxy/cosmology/open-memory/radiative sectors with the compact local selector.",
            "BLOCKED",
            "Sector interfaces need no-flux/support separation or explicit bounds.",
        ),
    ]
    return [
        {
            **common(),
            "firewall_id": firewall_id,
            "forbidden_move": forbidden_move,
            "status": status,
            "reason": reason,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for firewall_id, forbidden_move, status, reason in data
    ]


def status_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "status_id": "LGS4231_STATUS",
            "decision": DECISION,
            "summary": "Private local-GR scorecard is refreshed; public/global work now targets non-EH/R11 coefficients first.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def next_target_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "next_target": NEXT_TARGET,
            "reason": "The scorecard shows non-EH/R11 coefficients are the highest-pressure blocker for public/global local-GR promotion.",
            "derive_first": "attempt parent-zero, symmetry-forbidden, heavy/screened, or boundary-routed status for each non-EH coefficient family",
            "fill_second": "if any coefficient survives, map it into PPN/R10/WEP/clock/orbital bounds with a local runner",
            "fallback": "keep private local-GR pass quarantined and avoid public claim until the coefficient vector is zero or source-bounded",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def formal_doc() -> str:
    return f"""# 247 - PPC4161 Private Local GR Scorecard Refresh And Non-EH Parent Adoption Gate

Marker: `{MARKER}`

Branch: `{BRANCH}`
Decision: `{DECISION}`

## Refreshed verdict

After 4230, the private compact dressed-source selector has an internally coherent local-GR route:

```text
G_munu[g_obs] = kappa_eff T_H_munu
nabla^2 Phi_N = 4*pi G_cal rho_H
R_PPN = 0
T_EM and Poynting are in T_total once
M_EH_private > 0
M_H_ref_private > 0
```

This is stronger than the old closure-only state. It is still private/nonclaim:

```text
public_local_GR_claim = false
global_parent_adoption = false
numeric_G_prediction = false
```

## What blocks public promotion

The main blockers are now sharply named:

```text
nonEH/R11 coefficient vector;
R10 full alpha(lambda) curve or mapped fifth-force envelope;
global parent-action adoption;
raw/reproducible local empirical refresh;
sector-interface no-flux/support separation.
```

## Safe wording

Safe:

```text
MTS has a private compact-selector route reproducing local GR/Newton/PPN structure with calibrated G, if the selector clauses are adopted.
```

Forbidden:

```text
MTS publicly derives local GR;
MTS predicts numerical G_N;
R10 is passed by an anchor-only row;
non-EH coefficients are globally zero.
```

## Next target

`{NEXT_TARGET}`.
"""


def checkpoint_doc() -> str:
    return f"""# 4231 - Private Local GR Scorecard Refresh And Non-EH Parent Adoption Gate

**Status:** `{DECISION}`.

## What moved

The local branch is now summarized as:

```text
private_selector_pass = true
private_denominator_pass_imported_from_4230 = true
public_local_GR_claim = false
global_parent_adoption = false
```

## What is actually next

The highest-pressure public blocker is no longer `beta_sig` or `beta_bind`; it is:

```text
nonEH/R11 coefficient parent-zero vector or local bound runner.
```

R10 full-curve evidence is also still missing, but non-EH coefficients come first because they control whether R10/PPN/WEP/clock/orbital residuals are genuinely zero or merely selector-assumed.

Next: `{NEXT_TARGET}`.
"""


def update_registers() -> None:
    claim_row = (
        f'{CLAIM_ID},local_gr,'
        f'"The private local-GR scorecard is refreshed after 4230: inside the compact dressed-source selector, MTS now has a coherent nonclaim route to the local EH equation, Newton/Poisson readout with calibrated G, PPN zero vector, Maxwell-Hodge/Poynting stress ownership, and positive MEH/MHref denominators. Public/global promotion remains blocked by non-EH/R11 coefficients, R10 full-curve evidence, raw empirical refresh and global parent-action adoption.",'
        f'"4231 source audit, private branch scorecard, local-GR readout scorecard, public adoption debt ledger, empirical refresh scorecard, decision and firewall.",'
        f'private_local_GR_scorecard_refreshed_nonclaim,'
        f'"Attack the non-EH/R11 coefficient vector: parent-zero/symmetry/heavy-screened route first, empirical local bounds second.",'
        f'"This is not a public local-GR claim, not global MTS adoption, not a numerical G_N prediction, and not an R10 full-curve pass."'
    )
    append_once(FORMAL / "02-claims-register.csv", CLAIM_ID, claim_row)

    spine_block = f"""
## 106. Private Local GR Scorecard Refresh

Marker: `{MARKER}`

4231 records the current local-GR status:

```text
private_selector_pass = true,
private_denominator_pass = true,
public_local_GR_claim = false,
global_parent_adoption = false.
```

The next highest-pressure public blocker is:

```text
nonEH/R11 coefficient parent-zero vector or local bound runner.
```

R10 full-curve evidence and raw empirical refresh remain necessary before any public/local claim.
"""
    append_once(FORMAL / "07-unification-spine.md", MARKER, spine_block)

    packet_block = f"""
## Packet Update - Private Local GR Scorecard Refresh

Marker: `{PACKET_MARKER}`

The packet now distinguishes private local-GR compatibility from public/global adoption. The private score is strong; the public blocker is non-EH/R11 coefficient ownership, followed by full R10/local empirical refresh.
"""
    append_once(FORMAL / "180-PPC4161-private-local-packet-integration.md", PACKET_MARKER, packet_block)


def validate(rows_by_file: Dict[str, List[Dict[str, str]]]) -> List[Dict[str, str]]:
    sources = rows_by_file["P8_Y5_R2FR_4231_SOURCE_REGISTER.csv"]
    private_rows = rows_by_file["P8_Y5_R2FR_4231_PRIVATE_BRANCH_SCORECARD.csv"]
    readouts = rows_by_file["P8_Y5_R2FR_4231_LOCAL_GR_READOUT_SCORECARD.csv"]
    debts = rows_by_file["P8_Y5_R2FR_4231_PUBLIC_ADOPTION_DEBT.csv"]
    empirical = rows_by_file["P8_Y5_R2FR_4231_EMPIRICAL_REFRESH_SCORECARD.csv"]
    decision = rows_by_file["P8_Y5_R2FR_4231_DECISION.csv"][0]
    firewalls = rows_by_file["P8_Y5_R2FR_4231_CLAIM_FIREWALL.csv"]
    next_rows = rows_by_file["P8_Y5_R2FR_4231_NEXT_TARGET.csv"]
    all_rows = [row for rows in rows_by_file.values() for row in rows]
    private_ids = {row["score_id"] for row in private_rows}
    readout_ids = {row["readout_id"] for row in readouts}
    debt_ids = {row["debt_id"] for row in debts}
    empirical_ids = {row["empirical_id"] for row in empirical}
    firewall_ids = {row["firewall_id"] for row in firewalls}

    checks = [
        ("VAL4231_0_sources_exist", "all source paths exist", all(row["exists"] == "True" for row in sources)),
        ("VAL4231_1_source_needles", "all required source text found", all(row["required_text_found"] == "True" for row in sources)),
        (
            "VAL4231_2_private_scorecard",
            "private scorecard covers selector, EH, coupling, source, EM, locks and denominator",
            {"PBC4231_0_selector_scope", "PBC4231_1_EH_principal_block", "PBC4231_2_calibrated_coupling", "PBC4231_3_Hilbert_Hamiltonian_source", "PBC4231_4_EM_Poynting", "PBC4231_5_boundary_frame_quotient", "PBC4231_6_denominator"}.issubset(private_ids),
        ),
        (
            "VAL4231_3_readout_scorecard",
            "readout scorecard covers GR equation, Newton, PPN, EM, coupling, denominator and global status",
            {"LGR4231_0_GR_field_equation", "LGR4231_1_Newton_Poisson", "LGR4231_2_PPN_vector", "LGR4231_3_EM_Maxwell_stress", "LGR4231_4_source_coupling", "LGR4231_5_denominator", "LGR4231_6_global_status"}.issubset(readout_ids),
        ),
        (
            "VAL4231_4_public_debts",
            "public debt rows include global parent, nonEH, R10, empirical refresh, numeric G, sectors and exotic scope",
            {"PDB4231_0_global_parent_action", "PDB4231_1_nonEH_coefficients", "PDB4231_2_R10_curve", "PDB4231_3_raw_local_reanalysis", "PDB4231_4_numeric_G", "PDB4231_5_sector_interfaces", "PDB4231_6_exotic_sources"}.issubset(debt_ids),
        ),
        (
            "VAL4231_5_empirical_refresh",
            "empirical refresh rows include PPN/WEP/clock/Gdot/orbital/R10/R11/EM",
            {"EMP4231_0_PPN", "EMP4231_1_WEP", "EMP4231_2_clock", "EMP4231_3_Gdot", "EMP4231_4_orbital", "EMP4231_5_R10", "EMP4231_6_R11", "EMP4231_7_EM"}.issubset(empirical_ids),
        ),
        (
            "VAL4231_6_decision_split",
            "decision records private pass but public/global block",
            decision["private_selector_pass"] == "True"
            and decision["public_local_GR_claim"] == "False"
            and decision["global_parent_adoption"] == "False",
        ),
        (
            "VAL4231_7_blockers_visible",
            "decision keeps nonEH, R10 full curve and raw reanalysis unready",
            decision["nonEH_global_coefficients_zero_or_numeric"] == "False"
            and decision["R10_full_curve_claim_ready"] == "False"
            and decision["raw_empirical_reanalysis_ready"] == "False",
        ),
        (
            "VAL4231_8_firewall",
            "firewall blocks public promotion, R10 anchor overclaim, nonEH silence, numeric G and sector erasure",
            {"LGF4231_0_no_public_promotion", "LGF4231_1_no_R10_anchor_overclaim", "LGF4231_2_no_nonEH_silence", "LGF4231_3_no_numeric_G_claim", "LGF4231_4_no_sector_erasure"}.issubset(firewall_ids),
        ),
        (
            "VAL4231_9_no_claim_flags",
            "all generated claim flags remain false",
            all(row.get("claim_allowed", "False") == "False" and row.get("valid_for_claim", "False") == "False" for row in all_rows),
        ),
        ("VAL4231_10_docs_written", "formal and checkpoint docs written", FORMAL_PATH.exists() and DOC_PATH.exists()),
        ("VAL4231_11_claim_register", "claim register contains L-072", CLAIM_ID in read_text(FORMAL / "02-claims-register.csv")),
        ("VAL4231_12_spine_packet", "spine and packet contain 4231 markers", MARKER in read_text(FORMAL / "07-unification-spine.md") and PACKET_MARKER in read_text(FORMAL / "180-PPC4161-private-local-packet-integration.md")),
        ("VAL4231_13_next_target", "next target selected", next_rows[0]["next_target"] == NEXT_TARGET),
        ("VAL4231_14_status_script", "status records decision and generator script exists", rows_by_file["P8_Y5_R2FR_4231_STATUS.csv"][0]["decision"] == DECISION and (SCRIPTS / "Y5_R2FR_4231_private_local_GR_scorecard_refresh_and_nonEH_parent_adoption_gate.py").exists()),
    ]
    return [
        {**common(), "check_id": check_id, "description": description, "passed": str(bool(passed))}
        for check_id, description, passed in checks
    ]


def write_all() -> None:
    rows_by_file: Dict[str, List[Dict[str, str]]] = {
        "P8_Y5_R2FR_4231_SOURCE_REGISTER.csv": source_rows(),
        "P8_Y5_R2FR_4231_PRIVATE_BRANCH_SCORECARD.csv": private_branch_rows(),
        "P8_Y5_R2FR_4231_LOCAL_GR_READOUT_SCORECARD.csv": readout_rows(),
        "P8_Y5_R2FR_4231_PUBLIC_ADOPTION_DEBT.csv": public_debt_rows(),
        "P8_Y5_R2FR_4231_EMPIRICAL_REFRESH_SCORECARD.csv": empirical_rows(),
        "P8_Y5_R2FR_4231_DECISION.csv": decision_rows(),
        "P8_Y5_R2FR_4231_CLAIM_FIREWALL.csv": firewall_rows(),
        "P8_Y5_R2FR_4231_STATUS.csv": status_rows(),
        "P8_Y5_R2FR_4231_NEXT_TARGET.csv": next_target_rows(),
    }
    for filename, rows in rows_by_file.items():
        write_csv(SOURCE_DIR / filename, rows)

    FORMAL_PATH.write_text(formal_doc(), encoding="utf-8")
    DOC_PATH.write_text(checkpoint_doc(), encoding="utf-8")
    update_registers()
    validation_rows = validate(rows_by_file)
    write_csv(VALIDATION_PATH, validation_rows)


def main() -> None:
    write_all()
    print(DECISION)
    print(f"formal={FORMAL_PATH}")
    print(f"checkpoint={DOC_PATH}")
    print(f"validation={VALIDATION_PATH}")
    print("rows=15 validation checks")


if __name__ == "__main__":
    main()
