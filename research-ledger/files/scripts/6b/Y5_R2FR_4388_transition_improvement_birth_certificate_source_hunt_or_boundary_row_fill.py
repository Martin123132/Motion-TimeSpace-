from __future__ import annotations

import csv
import sys
from datetime import datetime, timezone
from io import StringIO
from pathlib import Path
from typing import Dict, Iterable, List, Tuple


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from double_divergence_boundary_gate import evaluate_boundary_rows, read_csv, write_csv  # noqa: E402
from improvement_birth_certificate_hunter import score_manifest  # noqa: E402


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4388"
CLAIM_ID = "L-229"
MARKER = "PPC4161_TRANSITION_IMPROVEMENT_BIRTH_CERTIFICATE_SOURCE_HUNT_OR_BOUNDARY_ROW_FILL_4388"
PACKET_MARKER = "PPC4161_PACKET_TRANSITION_IMPROVEMENT_BIRTH_CERTIFICATE_SOURCE_HUNT_OR_BOUNDARY_ROW_FILL_4388"
DECISION = "CURVATURE_COUPLED_IMPROVEMENT_TEMPLATE_DERIVED_SOURCE_HUNT_NO_PASS_BOUNDARY_ROWS_STAGED_NONCLAIM"
NEXT_TARGET = "4389-Y5-R2FR-transition-curvature-improvement-action-adoption-or-real-boundary-pairing-row.md"

FORMAL_PATH = FORMAL / "404-PPC4161-transition-improvement-birth-certificate-source-hunt-or-boundary-row-fill.md"
DOC_PATH = POST / "4388-Y5-R2FR-transition-improvement-birth-certificate-source-hunt-or-boundary-row-fill.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4388_VALIDATION.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
HUNTER_PATH = SCRIPT_DIR / "improvement_birth_certificate_hunter.py"
BOUNDARY_RUNNER_PATH = SCRIPT_DIR / "double_divergence_boundary_gate.py"
SOURCE_HUNT_MANIFEST_PATH = SOURCE_DIR / "P8_Y5_R2FR_4388_SOURCE_HUNT_MANIFEST.csv"
SOURCE_HUNT_OUTPUT_PATH = SOURCE_DIR / "P8_Y5_R2FR_4388_SOURCE_HUNT_OUTPUT.csv"
BOUNDARY_FILL_TEMPLATE_PATH = SOURCE_DIR / "P8_Y5_R2FR_4388_BOUNDARY_PAIRING_FILL_TEMPLATE.csv"
BOUNDARY_TEMPLATE_GATE_PATH = SOURCE_DIR / "P8_Y5_R2FR_4388_BOUNDARY_PAIRING_TEMPLATE_GATE.csv"
STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

LOCAL_SOURCES: Dict[str, Tuple[Path, str, str]] = {
    "SRC4388_00_4387_formal": (
        FORMAL / "403-PPC4161-transition-double-divergence-improvement-parent-owner-or-boundary-row.md",
        "IO4387_1_newtonian_density_projection",
        "4387 handoff: covariant improvement density projection.",
    ),
    "SRC4388_01_4387_next": (
        SOURCE_DIR / "P8_Y5_R2FR_4387_NEXT_TARGET.csv",
        "4388-Y5-R2FR-transition-improvement-birth-certificate-source-hunt-or-boundary-row-fill.md",
        "Explicit 4388 target.",
    ),
    "SRC4388_02_4387_birth": (
        SOURCE_DIR / "P8_Y5_R2FR_4387_BIRTH_CERTIFICATE.csv",
        "BCERT4387_6_verdict",
        "Birth certificate failure to test.",
    ),
    "SRC4388_03_hunter": (
        HUNTER_PATH,
        "def score_manifest",
        "Birth certificate source-hunter helper.",
    ),
    "SRC4388_04_boundary_runner": (
        BOUNDARY_RUNNER_PATH,
        "def evaluate_boundary_rows",
        "Boundary-pairing gate helper.",
    ),
    "SRC4388_05_185_hsrc": (
        FORMAL / "185-PPC4161-Hilbert-source-measure-descent-and-delta-ZH-closure.md",
        "+ int dB_impr",
        "Private source packet improvement slot.",
    ),
    "SRC4388_06_2220": (
        SOURCE_DIR / "P8_Y5_PARENT_QLOC_2220_TRACEFREE_IMPROVEMENT_BIRTH_CERTIFICATE.csv",
        "BIRTH_CERTIFICATE_FAILS_CURRENT_CORPUS",
        "Prior trace-free improvement birth certificate failure.",
    ),
}


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def find_line(path: Path, needle: str) -> str:
    text = read_text(path)
    index = text.find(needle)
    if index < 0:
        return ""
    return str(text[:index].count("\n") + 1)


def csv_line(row: Iterable[str]) -> str:
    buffer = StringIO()
    writer = csv.writer(buffer, lineterminator="\n")
    writer.writerow(list(row))
    return buffer.getvalue()


def md_cell(value: object) -> str:
    return str(value).replace("|", r"\|").replace("\n", "<br>")


def md_table(rows: List[Dict[str, str]], fields: List[str]) -> str:
    lines = [
        "| " + " | ".join(fields) + " |",
        "| " + " | ".join("---" for _ in fields) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(md_cell(row.get(field, "")) for field in fields) + " |")
    return "\n".join(lines)


def append_once(path: Path, marker: str, block: str) -> None:
    text = read_text(path)
    if marker in text:
        return
    if text and not text.endswith("\n"):
        text += "\n"
    path.write_text(text + block.strip() + "\n", encoding="utf-8")


def append_claim_once(path: Path, claim_id: str, row: List[str]) -> None:
    text = read_text(path)
    if f"\n{claim_id}," in text:
        return
    if text and not text.endswith("\n"):
        text += "\n"
    path.write_text(text + csv_line(row), encoding="utf-8")


def source_register_rows() -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    for source_id, (path, needle, role) in LOCAL_SOURCES.items():
        line_number = find_line(path, needle)
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "source_id": source_id,
                "path": str(path),
                "path_exists": str(path.exists()),
                "needle": needle,
                "needle_found": str(bool(line_number)),
                "line_number": line_number,
                "role": role,
                "valid_for_claim": "False",
            }
        )
    return rows


def source_hunt_manifest_rows() -> List[Dict[str, str]]:
    return [
        {"candidate_id": "CAND4388_00_4387_formal", "path": str(FORMAL / "403-PPC4161-transition-double-divergence-improvement-parent-owner-or-boundary-row.md"), "role": "current owner-shape checkpoint"},
        {"candidate_id": "CAND4388_01_4386_formal", "path": str(FORMAL / "402-PPC4161-transition-affine-annihilator-parent-signature-or-real-profile-row.md"), "role": "double-divergence mechanism"},
        {"candidate_id": "CAND4388_02_185_Hsrc", "path": str(FORMAL / "185-PPC4161-Hilbert-source-measure-descent-and-delta-ZH-closure.md"), "role": "source action dB_impr slot"},
        {"candidate_id": "CAND4388_03_226_visible", "path": str(FORMAL / "226-PPC4161-standard-visible-matter-import-contract.md"), "role": "visible matter import dB_impr slot"},
        {"candidate_id": "CAND4388_04_2220_birth", "path": str(SOURCE_DIR / "P8_Y5_PARENT_QLOC_2220_TRACEFREE_IMPROVEMENT_BIRTH_CERTIFICATE.csv"), "role": "trace-free improvement birth certificate attempt"},
        {"candidate_id": "CAND4388_05_299_superpotential", "path": str(FORMAL / "299-PPC4161-transition-boundary-topological-superpotential-or-shell-profile-runner.md"), "role": "generic superpotential guard"},
        {"candidate_id": "CAND4388_06_192_noflux", "path": str(FORMAL / "192-PPC4161-local-boundary-no-flux-sector-interface-theorem.md"), "role": "support-separated no-flux theorem"},
        {"candidate_id": "CAND4388_07_191_EM", "path": str(FORMAL / "191-PPC4161-Maxwell-Hodge-Poynting-stress-owner-theorem.md"), "role": "visible EM/Poynting Hilbert owner"},
        {"candidate_id": "CAND4388_08_143_boundary", "path": str(FORMAL / "143-boundary-topological-backup-gate.md"), "role": "boundary/topological backup guard"},
        {"candidate_id": "CAND4388_09_355_nonHilbert", "path": str(FORMAL / "355-PPC4161-PnonHilbert-and-worldtube-transition-leak-zero-proof-or-bound-runner.md"), "role": "non-Hilbert superpotential route"},
        {"candidate_id": "CAND4388_10_GK_action", "path": str(SOURCE_DIR / "P8_GK_STRESS_ACTION_CANDIDATES.csv"), "role": "Gamma/Khat exact sector candidates"},
        {"candidate_id": "CAND4388_11_GK_repair", "path": str(SOURCE_DIR / "P8_GK_METRIC_RESPONSE_REPAIR_OPTIONS.csv"), "role": "metric response exact/improvement repair options"},
        {"candidate_id": "CAND4388_12_Gamma_owner", "path": str(SOURCE_DIR / "P8_GAMMA_OWNER_CANDIDATE_ACTION.csv"), "role": "Gamma owner candidate action rows"},
        {"candidate_id": "CAND4388_13_affine2608", "path": str(SOURCE_DIR / "P8_Y5_AFFINE_SOURCE_GATE_2608_SOURCE_ZERO_STATUS.csv"), "role": "older affine source obstruction"},
        {"candidate_id": "CAND4388_14_topHilbertObs", "path": str(SOURCE_DIR / "P8_TOPOLOGICAL_HILBERT_EQUALITY_OBSTRUCTIONS.csv"), "role": "topological/Hilbert obstruction ledger"},
        {"candidate_id": "CAND4388_15_4387_birth", "path": str(SOURCE_DIR / "P8_Y5_R2FR_4387_BIRTH_CERTIFICATE.csv"), "role": "latest birth certificate audit"},
    ]


def action_template_rows() -> List[Dict[str, str]]:
    return [
        {
            "template_id": "ACT4388_0_curvature_coupled_improvement",
            "action_shape": "S_U = 1/2 int sqrt(-g) U^{mu alpha nu beta}[Phi] R_{mu alpha nu beta}",
            "derivation": "Metric variation of a curvature-coupled superpotential gives Hilbert terms with nabla_alpha nabla_beta U^{mu alpha nu beta} plus algebraic curvature and metric-variation residuals.",
            "what_it_would_supply": "field-theoretic birth of the 4387 U and the 4386 S^{ij}=c^{-2}U^{0i0j}",
            "current_status": "TEMPLATE_DERIVED_PARENT_NOT_ADOPTED",
            "valid_for_claim": "False",
        },
        {
            "template_id": "ACT4388_1_trace_scalar_subcase",
            "action_shape": "U^{mu alpha nu beta}=phi(g^{mu nu}g^{alpha beta}-g^{mu beta}g^{alpha nu}) gives a phi R improvement subcase",
            "derivation": "The scalar trace contraction recovers the known improvement species seen in older Khat/phi R attempts.",
            "what_it_would_supply": "trace/laplacian-like double divergence when phi is parent-owned and boundary/zero-mode terms close",
            "current_status": "SUBCASE_KNOWN_BIRTH_CERTIFICATE_FAILED_IN_2220",
            "valid_for_claim": "False",
        },
        {
            "template_id": "ACT4388_2_exact_identity_needed",
            "action_shape": "rho_top-rho_H must equal c^{-2} delta_g S_U|00 projected on W_H, not merely coexist with S_U",
            "derivation": "An improvement action can exist without being the specific topological/Hilbert residual. Equality of the residual operator is the missing owner identity.",
            "what_it_would_supply": "prevents adding a useful mathematical species without proving it is the live MTS residual",
            "current_status": "IDENTITY_REQUIRED_SOURCE_NOT_FOUND",
            "valid_for_claim": "False",
        },
        {
            "template_id": "ACT4388_3_boundary_and_curvature_payload",
            "action_shape": "affine boundary pairings and curvature commutator residuals must be zero or explicitly bounded",
            "derivation": "4387 retains curvature/boundary residuals; 4386 shows affine silence requires boundary pairings.",
            "what_it_would_supply": "claim-safe closure path or explicit retained rows",
            "current_status": "BOUNDARY_AND_CURVATURE_ROWS_STAGED",
            "valid_for_claim": "False",
        },
    ]


def boundary_fill_template_rows() -> List[Dict[str, str]]:
    return [
        {
            "row_id": "BF4388_0_candidate_US",
            "object_id": "MISSING_PARENT_U_OR_S_OBJECT",
            "constant_pairing": "MISSING_CONSTANT_PAIRING",
            "linear_x_pairing": "MISSING_LINEAR_X_PAIRING",
            "linear_y_pairing": "MISSING_LINEAR_Y_PAIRING",
            "linear_z_pairing": "MISSING_LINEAR_Z_PAIRING",
            "units": "MISSING_UNITS",
            "source_path": "MISSING_SOURCE_PATH",
            "input_valid_for_claim": "False",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        }
    ]


def route_rows(source_hunt: List[Dict[str, str]], boundary_gate: List[Dict[str, str]]) -> List[Dict[str, str]]:
    source_pass = any(row["certificate_pass"] == "True" for row in source_hunt)
    boundary_pass = any(row["valid_for_claim"] == "True" for row in boundary_gate)
    return [
        {
            "route_id": "ROUTE4388_0_source_birth_certificate",
            "route": "Existing corpus source birth-certifies U/S as rho_top-rho_H owner",
            "evidence": "source-hunt pass row exists" if source_pass else "no source-hunt candidate passed all certificate clauses",
            "status": "PASS" if source_pass else "BLOCKED_NO_SOURCE_CERTIFICATE",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "route_id": "ROUTE4388_1_action_adoption",
            "route": "Adopt/derive curvature-coupled S_U action with residual identity",
            "evidence": "template derived, parent adoption not present",
            "status": "TEMPLATE_READY_PARENT_ADOPTION_MISSING",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "route_id": "ROUTE4388_2_boundary_pairing_fill",
            "route": "Fill source-backed affine boundary pairings",
            "evidence": "boundary row pass exists" if boundary_pass else "boundary fill template remains missing/nonclaim",
            "status": "PASS" if boundary_pass else "BLOCKED_BOUNDARY_VALUES_MISSING",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def claim_gate_rows() -> List[Dict[str, str]]:
    return [
        {
            "gate_id": "GATE4388_0_source_hunt",
            "claim_tested": "existing corpus contains U/S birth certificate",
            "required_inputs": "source-hunt candidate with all clauses and no blockers",
            "status": "BLOCKED_NO_PASSING_CANDIDATE",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "GATE4388_1_action_template",
            "claim_tested": "curvature-coupled improvement action supplies S^{ij}",
            "required_inputs": "parent adoption plus residual identity plus curvature/boundary closure",
            "status": "TEMPLATE_DERIVED_PARENT_NOT_ADOPTED",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "GATE4388_2_boundary_rows",
            "claim_tested": "source-backed boundary rows close affine pairings",
            "required_inputs": "numeric pairings, existing source path, no forbidden markers",
            "status": "BOUNDARY_ROWS_MISSING",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "GATE4388_3_local_GR",
            "claim_tested": "local GR/Newton/PPN/clock/orbital pass",
            "required_inputs": "source/action/boundary plus remaining curvature/higher-profile/rest/readout gates",
            "status": "FORBIDDEN_COMPONENTS_OPEN",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def decision_rows() -> List[Dict[str, str]]:
    return [
        {
            "decision_id": "DEC4388_0",
            "decision": DECISION,
            "summary": (
                "4388 performs the promised source hunt and adds a stronger action-level template. The source-hunt scans the current candidate corpus for the actual U/S birth-certificate clauses: residual identity, action birth shape, parent owner, pre-readout lock, affine boundary silence, and no blocker terms. No candidate passes. "
                "The positive progress is a precise parent-action template: S_U=1/2 int sqrt(-g) U^{mu alpha nu beta} R_{mu alpha nu beta}. Its Hilbert variation has the required double-divergence improvement species and would supply S^{ij}=c^{-2}U^{0i0j} in the weak-static density projection if parent-adopted and tied to rho_top-rho_H. "
                "Because no current file adopts that action as the live residual owner, 4388 stages boundary-pairing fill rows and keeps the branch nonclaim."
            ),
            "next_target": NEXT_TARGET,
            "why_next": "The next best move is no longer generic source hunting: either adopt/derive S_U as a parent action term or fill real boundary-pairing/profile rows.",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        }
    ]


def status_rows() -> List[Dict[str, str]]:
    return [
        {
            "status_id": "STAT4388_0_source_hunt",
            "object": "existing corpus U/S certificate",
            "status": "NO_PASSING_CANDIDATE",
            "note": "candidate files have partial shapes or explicit blockers, not a claim-grade birth certificate.",
            "valid_for_claim": "False",
        },
        {
            "status_id": "STAT4388_1_action_template",
            "object": "curvature-coupled improvement action S_U",
            "status": "TEMPLATE_DERIVED",
            "note": "would generate the correct double-divergence species if parent-adopted and tied to rho_top-rho_H.",
            "valid_for_claim": "False",
        },
        {
            "status_id": "STAT4388_2_boundary_rows",
            "object": "boundary-pairing fill template",
            "status": "STAGED_MISSING_VALUES",
            "note": "gate rejects missing values and source paths.",
            "valid_for_claim": "False",
        },
        {
            "status_id": "STAT4388_3_next",
            "object": "next target",
            "status": "ACTION_ADOPTION_OR_REAL_BOUNDARY_ROW_NEXT",
            "note": NEXT_TARGET,
            "valid_for_claim": "False",
        },
    ]


def next_target_rows() -> List[Dict[str, str]]:
    return [
        {
            "next_id": "NT4388_0",
            "target": NEXT_TARGET,
            "question": "Can MTS adopt or derive the curvature-coupled improvement action as the actual topological/Hilbert residual owner, or can real boundary pairings be filled?",
            "preferred_route": "derive/adopt S_U=1/2 int sqrt(-g) U Riemann with U parent-owned and residual identity rho_top-rho_H=c^{-2}delta_g S_U|00.",
            "fallback_route": "fill source-backed boundary-pairing rows or import a real rho_H/rho_top profile through the affine runner.",
            "avoid": "re-running broad source sweeps, claiming from partial dB_impr/phiR/Khat shapes, using synthetic templates, or total-charge-only closure.",
            "valid_for_claim": "False",
        }
    ]


def write_formal_doc(
    sources: List[Dict[str, str]],
    source_hunt: List[Dict[str, str]],
    action_templates: List[Dict[str, str]],
    boundary_gate: List[Dict[str, str]],
    routes: List[Dict[str, str]],
    gates: List[Dict[str, str]],
    decisions: List[Dict[str, str]],
    statuses: List[Dict[str, str]],
    next_targets: List[Dict[str, str]],
) -> None:
    text = f"""# PPC4161 transition: improvement birth-certificate source hunt or boundary row fill

Marker: `{MARKER}`

Private checkpoint: `{CHECKPOINT}`  
UTC stamp: `{STAMP}`  
Decision: `{DECISION}`

## Result

4388 does two things.

First, it performs an executable source hunt for the `U/S` birth certificate. No candidate file currently passes all clauses:

```text
rho_top-rho_H identity,
double-divergence/action birth shape,
parent owner,
pre-readout lock,
affine boundary silence,
no blocker terms.
```

Second, it derives the clean parent-action template that would solve this if MTS can adopt it:

```text
S_U = 1/2 int sqrt(-g) U^{{mu alpha nu beta}} R_{{mu alpha nu beta}}.
```

Metric variation of this curvature-coupled improvement gives the right Hilbert/Noether species:

```text
Delta T^{{mu nu}} ~ nabla_alpha nabla_beta U^{{mu alpha nu beta}} + curvature/boundary residuals.
```

Then the local weak-static density projection gives:

```text
rho_top-rho_H = partial_i partial_j S^{{ij}},
S^{{ij}} = c^-2 U^{{0i0j}},
```

but only if the parent action identifies this term as the actual topological/Hilbert residual before readout.

No claim fires. The action template is not yet parent-adopted, no source-hunt candidate passes, and the boundary row is only a missing-value template.

## Source Register

{md_table(sources, ["source_id", "path", "path_exists", "needle", "needle_found", "line_number", "role"])}

## Source Hunt Output

{md_table(source_hunt, ["candidate_id", "role", "path_exists", "has_residual_identity", "has_action_birth_shape", "has_parent_owner", "has_readout_lock", "has_boundary_silence", "has_blocker_terms", "certificate_pass", "status"])}

## Action Templates

{md_table(action_templates, ["template_id", "action_shape", "derivation", "what_it_would_supply", "current_status"])}

## Boundary Template Gate

{md_table(boundary_gate, ["row_id", "object_id", "missing_fields", "numeric_parse_ok", "boundary_silent", "source_declared", "valid_for_claim", "current_status"])}

## Route Rows

{md_table(routes, ["route_id", "route", "evidence", "status", "claim_allowed"])}

## Claim Gates

{md_table(gates, ["gate_id", "claim_tested", "required_inputs", "status", "claim_allowed"])}

## Decision

{md_table(decisions, ["decision_id", "decision", "summary", "next_target", "why_next"])}

## Status

{md_table(statuses, ["status_id", "object", "status", "note"])}

## Next Target

{md_table(next_targets, ["next_id", "target", "question", "preferred_route", "fallback_route", "avoid"])}
"""
    FORMAL_PATH.write_text(text, encoding="utf-8")


def write_post_doc(decisions: List[Dict[str, str]], next_targets: List[Dict[str, str]]) -> None:
    text = f"""# 4388: improvement birth-certificate source hunt or boundary row fill

Marker: `{MARKER}`

## What changed

- Ran an executable source hunt for the `U/S` birth certificate.
- Derived the curvature-coupled improvement action template `S_U = 1/2 int sqrt(-g) U Riemann`.
- Staged boundary-pairing fill rows and verified the gate fails closed on missing values.
- Kept all rows nonclaim.

## Decision

{md_table(decisions, ["decision_id", "decision", "summary", "next_target", "why_next"])}

## Next target

{md_table(next_targets, ["next_id", "target", "question", "preferred_route", "fallback_route", "avoid"])}
"""
    DOC_PATH.write_text(text, encoding="utf-8")


def write_spine_update() -> None:
    block = f"""
## 4388 Transition improvement birth-certificate source hunt or boundary row fill

Marker: `{MARKER}`

4388 runs an executable source hunt for the `U/S` birth certificate and finds no passing existing source. It also derives the clean parent-action template:

```text
S_U = 1/2 int sqrt(-g) U^{{mu alpha nu beta}} R_{{mu alpha nu beta}}.
```

If MTS can parent-adopt this and identify `rho_top-rho_H=c^-2 delta_g S_U|00`, then the 4386 double-divergence affine mechanism has a real field-theory birth. Until then the route remains nonclaim, with boundary/profile rows staged.

Next target: `{NEXT_TARGET}`.
"""
    append_once(SPINE_PATH, MARKER, block)


def write_packet_update() -> None:
    block = f"""
## 4388 packet update: curvature-coupled improvement action template

Marker: `{PACKET_MARKER}`

Packet update: source hunt found no existing claim-grade `U/S` birth certificate. The viable parent-action shape is now explicit: `S_U=1/2 int sqrt(-g) U Riemann`, whose Hilbert variation can generate the double-divergence density. Claim remains blocked until this action is parent-adopted as the actual `rho_top-rho_H` residual owner or real boundary/profile rows are supplied.
"""
    append_once(PACKET_PATH, PACKET_MARKER, block)


def write_claim() -> None:
    append_claim_once(
        CLAIMS_PATH,
        CLAIM_ID,
        [
            CLAIM_ID,
            "local_gr",
            (
                "4388 runs an executable source hunt for the U/S improvement birth certificate and finds no passing existing source. It also derives the clean parent-action template S_U=1/2 int sqrt(-g) U^{mu alpha nu beta} R_{mu alpha nu beta}; metric variation has the required Hilbert/Noether double-divergence species and could supply S^{ij}=c^{-2}U^{0i0j} in the weak-static density projection if parent-adopted and tied to rho_top-rho_H. "
                "No current file adopts that action as the live topological/Hilbert residual owner, and boundary pairings remain missing, so the checkpoint stages boundary/profile fill rows and keeps all local-GR/Newton/PPN/clock/orbital claims blocked."
            ),
            "4388 source register, source-hunt manifest/output, action templates, boundary fill template/gate, route rows, claim gates, decision, status, next target and validation CSV.",
            "curvature_improvement_action_template_source_hunt_no_pass_nonclaim",
            "Adopt/derive S_U as the actual rho_top-rho_H parent owner or fill source-backed boundary/profile rows.",
            "Partial dB_impr/phiR/Khat shapes, synthetic templates, generic source sweeps, or total-charge-only closure.",
        ],
    )


def validation_rows(csv_paths: List[Path]) -> List[Dict[str, str]]:
    validations: List[Dict[str, str]] = []
    sources = read_csv(SOURCE_DIR / "P8_Y5_R2FR_4388_SOURCE_REGISTER.csv")
    source_hunt = read_csv(SOURCE_HUNT_OUTPUT_PATH)
    action_templates = read_csv(SOURCE_DIR / "P8_Y5_R2FR_4388_ACTION_TEMPLATES.csv")
    boundary_gate = read_csv(BOUNDARY_TEMPLATE_GATE_PATH)
    gates = read_csv(SOURCE_DIR / "P8_Y5_R2FR_4388_CLAIM_GATES.csv")

    def add(check_id: str, passed: bool, detail: str) -> None:
        validations.append({"checkpoint": CHECKPOINT, "check_id": check_id, "passed": str(bool(passed)), "detail": detail})

    add("VAL4388_0_sources_exist", all(row["path_exists"] == "True" for row in sources), "every cited source exists")
    add("VAL4388_1_needles_found", all(row["needle_found"] == "True" for row in sources), "every cited needle resolves")
    add("VAL4388_2_manifest_paths_exist", all(row["path_exists"] == "True" for row in source_hunt), "every source-hunt manifest path exists")
    add("VAL4388_3_no_source_pass", all(row["certificate_pass"] == "False" for row in source_hunt), "no candidate source passes all birth-certificate clauses")
    add(
        "VAL4388_4_action_template",
        any(row["template_id"] == "ACT4388_0_curvature_coupled_improvement" for row in action_templates),
        "curvature-coupled improvement action template recorded",
    )
    add(
        "VAL4388_5_boundary_template_fails_closed",
        all(row["valid_for_claim"] == "False" and row["current_status"] in {"BOUNDARY_ROW_MISSING_FIELDS", "BOUNDARY_PAIRING_NUMERIC_PARSE_FAILED"} for row in boundary_gate),
        "missing boundary template rows fail closed",
    )
    add("VAL4388_6_claim_gates_false", all(row["claim_allowed"] == "False" for row in gates), "all claim gates false")
    add("VAL4388_7_formal_marker", MARKER in read_text(FORMAL_PATH), "formal marker present")
    add("VAL4388_8_post_marker", MARKER in read_text(DOC_PATH), "post marker present")
    add("VAL4388_9_spine_marker", MARKER in read_text(SPINE_PATH), "spine marker present")
    add("VAL4388_10_packet_marker", PACKET_MARKER in read_text(PACKET_PATH), "packet marker present")
    add("VAL4388_11_claim_row", f"\n{CLAIM_ID}," in read_text(CLAIMS_PATH), "claim row appended")
    add(
        "VAL4388_12_rows_nonclaim",
        all(row.get("valid_for_claim", "False") == "False" for path in csv_paths for row in read_csv(path))
        and all(row.get("claim_allowed", "False") == "False" for path in csv_paths for row in read_csv(path)),
        "generated rows remain nonclaim",
    )
    add("VAL4388_13_csv_parse", all(len(read_csv(path)) > 0 for path in csv_paths), "all generated CSVs parse")
    add("VAL4388_14_hunter_exists", HUNTER_PATH.exists() and "def score_manifest" in read_text(HUNTER_PATH), "source hunter exists")
    return validations


def main() -> None:
    sources = source_register_rows()
    manifest = source_hunt_manifest_rows()
    write_csv(SOURCE_HUNT_MANIFEST_PATH, manifest)
    source_hunt = score_manifest(SOURCE_HUNT_MANIFEST_PATH)
    write_csv(SOURCE_HUNT_OUTPUT_PATH, source_hunt)
    action_templates = action_template_rows()
    boundary_template = boundary_fill_template_rows()
    write_csv(BOUNDARY_FILL_TEMPLATE_PATH, boundary_template)
    boundary_gate = evaluate_boundary_rows(BOUNDARY_FILL_TEMPLATE_PATH, 1.0e-12)
    write_csv(BOUNDARY_TEMPLATE_GATE_PATH, boundary_gate)
    routes = route_rows(source_hunt, boundary_gate)
    gates = claim_gate_rows()
    decisions = decision_rows()
    statuses = status_rows()
    next_targets = next_target_rows()

    csv_payloads: Dict[str, List[Dict[str, str]]] = {
        "P8_Y5_R2FR_4388_SOURCE_REGISTER.csv": sources,
        "P8_Y5_R2FR_4388_ACTION_TEMPLATES.csv": action_templates,
        "P8_Y5_R2FR_4388_ROUTE_ROWS.csv": routes,
        "P8_Y5_R2FR_4388_CLAIM_GATES.csv": gates,
        "P8_Y5_R2FR_4388_DECISION.csv": decisions,
        "P8_Y5_R2FR_4388_STATUS.csv": statuses,
        "P8_Y5_R2FR_4388_NEXT_TARGET.csv": next_targets,
    }

    csv_paths: List[Path] = [SOURCE_HUNT_MANIFEST_PATH, SOURCE_HUNT_OUTPUT_PATH, BOUNDARY_FILL_TEMPLATE_PATH, BOUNDARY_TEMPLATE_GATE_PATH]
    for filename, rows in csv_payloads.items():
        path = SOURCE_DIR / filename
        write_csv(path, rows)
        csv_paths.append(path)

    write_formal_doc(sources, source_hunt, action_templates, boundary_gate, routes, gates, decisions, statuses, next_targets)
    write_post_doc(decisions, next_targets)
    write_spine_update()
    write_packet_update()
    write_claim()
    write_csv(VALIDATION_PATH, validation_rows(csv_paths))


if __name__ == "__main__":
    main()
