from __future__ import annotations

import csv
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4631"
CLAIM_ID = "L-473"
BRANCH_ID = "MTS_R2FR_Y5_BRANCH_EXTREMUM_SYMMETRY_4631"
MARKER = "PPC4161_BRANCH_EXTREMUM_SYMMETRY_OR_PARENT_COEFFICIENT_FILL_4631"
PACKET_MARKER = "PPC4161_PACKET_BRANCH_EXTREMUM_SYMMETRY_4631"
DECISION = "STRONG_VERTICAL_INVOLUTION_PROVES_BETA_ZERO_CONDITIONALLY_WEAK_LEAKAGE_SYMMETRY_REJECTED"
NEXT_TARGET = "4632-Y5-R2FR-parent-vertical-involution-signature-hunt-or-epsilonA-bound-runner.md"

DOC_PATH = POST / "4631-Y5-R2FR-branch-extremum-symmetry-or-parent-coefficient-fill.md"
FORMAL_PATH = FORMAL / "647-PPC4161-branch-extremum-symmetry-or-parent-coefficient-fill.md"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4631_SOURCE_REGISTER.csv"
SYMMETRY_CSV = SOURCE_DIR / "P8_Y5_R2FR_4631_SYMMETRY_ROUTE_AUDIT.csv"
DERIVATION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4631_BRANCH_EXTREMUM_DERIVATION_ROWS.csv"
EPSILON_CSV = SOURCE_DIR / "P8_Y5_R2FR_4631_EPSILON_A_COEFFICIENT_FILL_ROWS.csv"
LOCAL_INSERT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4631_LOCAL_GR_INSERT_ROWS.csv"
CONTROL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4631_CONTROL_ROWS.csv"
BLOCKERS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4631_CLAIM_BLOCKERS.csv"
PROMOTION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4631_PROMOTION_GATES.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4631_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4631_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4631_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4631_VALIDATION.csv"

CSV_4630_NEXT = SOURCE_DIR / "P8_Y5_R2FR_4630_NEXT_TARGET.csv"
CSV_4630_VALIDATION = SOURCE_DIR / "P8_Y5_BRR545_4630_VALIDATION.csv"
CSV_4630_LOCAL_GR = SOURCE_DIR / "P8_Y5_R2FR_4630_CONDITIONAL_LOCAL_GR_THEOREM_ROWS.csv"
CSV_4630_EVAL = SOURCE_DIR / "P8_Y5_R2FR_4630_PARENT_ACTION_EVALUATION_ROWS.csv"
CSV_4525_THEOREM = SOURCE_DIR / "P8_Y5_R2FR_4525_QUOTIENT_EVEN_MORSE_BOTT_Z_THEOREM.csv"
CSV_4525_SIGNATURE = SOURCE_DIR / "P8_Y5_R2FR_4525_PARENT_SIGNATURE_REQUIREMENTS.csv"
CSV_4526_HUNT = SOURCE_DIR / "P8_Y5_R2FR_4526_VERTICAL_INVOLUTION_SOURCE_HUNT.csv"
CSV_4526_BRIDGE = SOURCE_DIR / "P8_Y5_R2FR_4526_ZL_TO_Z_PARENT_BRIDGE_THEOREM.csv"
CSV_4526_COEFF = SOURCE_DIR / "P8_Y5_R2FR_4526_FIRST_SOURCE_NORMALIZED_COEFFICIENT_ROWS.csv"
CSV_4526_VALIDATION = SOURCE_DIR / "P8_Y5_BRR545_4526_VALIDATION.csv"
CSV_4195_LEMMA = SOURCE_DIR / "P8_Y5_R2FR_4195_PARITY_LEMMA.csv"
CSV_4195_SIGNATURE = SOURCE_DIR / "P8_Y5_R2FR_4195_PARENT_SIGNATURE_AUDIT.csv"

PUBLIC_STAGE = Path("D:/Users/ollet/Desktop/Motion-TimeSpace-public-stage")
BACKUP_REPO = Path("D:/Users/ollet/Desktop/laptop-back-up-")


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def write_text(path: Path, body: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(body, encoding="utf-8")


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key, "") for key in fieldnames})


def markdown_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return ""
    headers: list[str] = []
    for row in rows:
        for key in row:
            if key not in headers:
                headers.append(key)
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(header, "")).replace("\n", "<br>") for header in headers) + " |")
    return "\n".join(lines)


def line_of(path: Path, needle: str) -> int:
    if not path.exists() or not needle:
        return 0
    for number, line in enumerate(read_text(path).splitlines(), start=1):
        if needle in line:
            return number
    return 0


def append_once(path: Path, marker: str, block: str) -> None:
    text = read_text(path)
    if marker in text:
        return
    suffix = "\n" if text.endswith("\n") or not text else "\n\n"
    write_text(path, text + suffix + block.strip() + "\n")


def git_clean(path: Path) -> bool:
    if not path.exists() or not (path / ".git").exists():
        return True
    result = subprocess.run(["git", "-C", str(path), "status", "--porcelain"], text=True, capture_output=True, check=False)
    return result.returncode == 0 and result.stdout.strip() == ""


def any_claim_true(rows: list[dict[str, Any]]) -> bool:
    return any(str(value).lower() == "true" for row in rows for key, value in row.items() if key in {"valid_for_claim", "claim_allowed"})


def source_rows(now: str) -> list[dict[str, Any]]:
    specs = [
        ("SRC4631_00_4630_next", CSV_4630_NEXT, "4631-Y5-R2FR-branch-extremum-symmetry-or-parent-coefficient-fill.md", "4630 selected branch-extremum target."),
        ("SRC4631_01_4630_validation", CSV_4630_VALIDATION, "VAL4630_OVERALL", "4630 validation."),
        ("SRC4631_02_4630_local_gr", CSV_4630_LOCAL_GR, "TGR4630_0_conditional_statement", "4630 conditional local-GR theorem."),
        ("SRC4631_03_4630_extremum_eval", CSV_4630_EVAL, "EVAL4630_1_extremum_positive_gap", "4630 extremum route evaluation."),
        ("SRC4631_04_4525_even", CSV_4525_THEOREM, "QEZ4525_1_even_involution", "4525 even vertical involution theorem."),
        ("SRC4631_05_4525_sig", CSV_4525_SIGNATURE, "SIG4525_0_vertical_involution", "4525 missing parent signature."),
        ("SRC4631_06_4526_scalar_limit", CSV_4526_HUNT, "HUNT4526_2_frame_symmetry_limit", "4526 weak symmetry scalar obstruction."),
        ("SRC4631_07_4526_bridge", CSV_4526_BRIDGE, "BRG4526_0_embedding", "4526 leakage-to-parent bridge condition."),
        ("SRC4631_08_4526_coeff", CSV_4526_COEFF, "COF4526_6_total_symmetry_breaking_bound", "4526 coefficient fallback row."),
        ("SRC4631_09_4526_validation", CSV_4526_VALIDATION, "VAL4526_OVERALL", "4526 validation."),
        ("SRC4631_10_4195_even_scalar", CSV_4195_LEMMA, "LEM4195_2_scalar_evenness", "4195 scalar evenness lemma."),
        ("SRC4631_11_4195_sig", CSV_4195_SIGNATURE, "SIG4195_0_parent_action", "4195 parent action invariance missing."),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, path, needle, role in specs:
        text = read_text(path)
        rows.append({
            "checkpoint": CHECKPOINT,
            "source_id": source_id,
            "path": str(path),
            "path_exists": path.exists(),
            "needle": needle,
            "needle_found": needle in text,
            "line": line_of(path, needle),
            "role": role,
            "valid_for_claim": False,
            "timestamp_utc": now,
        })
    return rows


def symmetry_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "route_id": "SYM4631_0_strong_parent_vertical_involution",
            "route": "full parent vertical involution I_q",
            "premise": "I_q^2=1, q o I_q=q, local GR section fixed, and S_parent, measure, matter scale, projector and boundary class are I_q-even.",
            "derives": "A_m(q,z)=A_m(q,-z) and beta_visible=partial_z ln A_m|z=0=0",
            "verdict": "SUFFICIENT_CONDITIONAL_NOT_PARENT_SIGNED",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "route_id": "SYM4631_1_leakage_involution_subbundle",
            "route": "4195 leakage involution R_L plus 4526 embedding",
            "premise": "R_L acts on leakage coordinates z_L and embeds into full vertical collar z only if the parent quotient owns the embedding.",
            "derives": "beta zero only for the embedded leakage subbundle, not all scalar memory/source channels",
            "verdict": "USEFUL_SUBLEMMA_NEEDS_FULL_IQ_EXTENSION",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "route_id": "SYM4631_2_weak_leakage_frame_symmetry",
            "route": "ordinary leakage-frame rotations/reflections",
            "premise": "frame symmetry kills vector/tensor linears but true scalar signed channels may remain",
            "derives": "does not force partial_z ln A_m|0=0",
            "verdict": "REJECTED_FOR_BETA_VISIBLE_ZERO",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "route_id": "SYM4631_3_private_GR_parity_source_import",
            "route": "private GR-parity standard-matter import",
            "premise": "ordinary visible source-weight/material-readout pieces are zero inside the private branch",
            "derives": "narrows WEP/PPN source reentry but does not prove MTS parent beta_visible=0",
            "verdict": "PRIVATE_EFFECTIVE_BRANCH_USEFUL_NOT_PARENT_PROOF",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "route_id": "SYM4631_4_coefficient_fallback",
            "route": "epsilon_A coefficient fill",
            "premise": "if no strong I_q signature is found, retain epsilon_A=||partial_z ln A_m|| as a real coefficient",
            "derives": "alpha_AB bound route rather than exact local-GR silence",
            "verdict": "FALLBACK_READY",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
    ]


def derivation_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "derivation_id": "DER4631_0_even_matter_scale",
            "statement": "If the parent matter scale descends as an I_q-even scalar, A_m(q,z)=A_m(q,-z).",
            "calculation": "Differentiate at z=0: partial_A A_m(q,0) = -partial_A A_m(q,0), so partial_A A_m(q,0)=0.",
            "result": "matter-scale extremum at the local branch",
            "status": "PROVED_CONDITIONAL_ON_IQ_EVEN_DESCENT",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "derivation_id": "DER4631_1_beta_visible_zero",
            "statement": "beta_A := partial_A ln A_m|z=0 for visible matter.",
            "calculation": "partial_A ln A_m|0 = (partial_A A_m/A_m)|0 = 0 when A_m(q,0) is finite and I_q-even.",
            "result": "beta_visible=0 and first-order trace source vanishes",
            "status": "PROVED_CONDITIONAL_ON_DER4631_0",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "derivation_id": "DER4631_2_insert_into_4630",
            "statement": "4630 needs Z_mem>0, M2_mem>0, beta_visible=0, source/boundary silence.",
            "calculation": "DER4631_1 supplies beta_visible=0; 4525/4630 still require positive gap/Hessian and boundary/source signatures.",
            "result": "conditional first-order local-GR theorem can promote only after the full signature bundle is signed",
            "status": "BRIDGE_DERIVED_PROMOTION_UNSIGNED",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "derivation_id": "DER4631_3_weak_symmetry_failure",
            "statement": "If A_m has a scalar linear leakage term A_m=A0(1+a_A z^A+...), frame rotations/reflections alone do not remove it.",
            "calculation": "partial_A ln A_m|0=a_A, so alpha_AB=C_N a_A a_B/Z_mem unless a_A is zeroed by stronger symmetry or bounded.",
            "result": "weak leakage-frame symmetry is insufficient; coefficient fill is required",
            "status": "REJECTION_DERIVED",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
    ]


def epsilon_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "epsilon_id": "EPS4631_0_epsilon_A",
            "quantity": "epsilon_A",
            "definition": "norm of the visible matter-scale first derivative on the vertical local branch",
            "formula": "epsilon_A := ||P_vert d ln A_m/dz|z=0||",
            "source_status": "MISSING_PARENT_VALUE_OR_ZERO_THEOREM",
            "feeds": "alpha_AB and PPN/R10/WEP/local-G residual",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "epsilon_id": "EPS4631_1_alpha_bound_form",
            "quantity": "alpha_AB",
            "definition": "co-normalized Yukawa amplitude in the nonzero-beta route",
            "formula": "alpha_AB <= C_N epsilon_A epsilon_B / Z_min",
            "source_status": "MISSING_EPSILON_AND_ZMIN",
            "feeds": "R10 alpha(lambda), PPN gamma/beta residual, WEP source residual",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "epsilon_id": "EPS4631_2_range_form",
            "quantity": "lambda_mem",
            "definition": "same-branch memory range",
            "formula": "lambda_mem=sqrt(Z_mem/M2_mem)",
            "source_status": "MISSING_ZMEM_M2MEM_RATIO_OR_GAP_THEOREM",
            "feeds": "R10/PPN/orbital range selection",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "epsilon_id": "EPS4631_3_anchor_smoke_gate",
            "quantity": "anchor_smoke",
            "definition": "first conservative R10 threshold if exact beta zero fails",
            "formula": "alpha_AB<=1 and lambda_mem<=38.6e-6 m, with full curve still needed for claim",
            "source_status": "RUNNER_READY_VALUES_MISSING",
            "feeds": "4629/4630 smoke runner",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
    ]


def local_insert_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "insert_id": "LGR4631_0_strong_symmetry_to_local_GR",
            "if_signed": "SYM4631_0 plus positive gap, source-channel silence and boundary no-flux",
            "then": "DER4631_1 gives beta_visible=0, 4630 gives J_mem=0, and 4621 no-hair gives delta_m=0 locally.",
            "result": "first-order scalar/PPN/Yukawa residual zero",
            "claim_allowed_now": False,
            "valid_for_claim": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "insert_id": "LGR4631_1_weak_symmetry_to_bound_route",
            "if_signed": "only leakage-frame vector/tensor symmetry or private source import",
            "then": "scalar beta channel remains live as epsilon_A",
            "result": "no exact local-GR derivation; run bound route",
            "claim_allowed_now": False,
            "valid_for_claim": False,
            "timestamp_utc": now,
        },
    ]


def control_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "control_id": "CTL4631_0_no_weak_symmetry_upgrade",
            "rule": "Do not upgrade leakage-frame symmetry to beta_visible=0; scalar channels survive unless full parent I_q-even descent is signed.",
            "violation_blocks_claim": True,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "control_id": "CTL4631_1_even_A_not_even_action_only",
            "rule": "Even parent action is not enough by itself; the matter scale A_m, measure/projector and boundary class must also be I_q-even.",
            "violation_blocks_claim": True,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "control_id": "CTL4631_2_fallback_is_parameter_not_failure",
            "rule": "If beta zero is not signed, epsilon_A becomes a bounded parent coefficient rather than a hidden closure.",
            "violation_blocks_claim": False,
            "timestamp_utc": now,
        },
    ]


def blocker_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "blocker_id": "BLK4631_0_full_parent_involution",
            "blocks": "beta_visible exact-zero theorem",
            "missing": "I_q existence on full vertical kernel, q o I_q=q, and I_q-even matter scale A_m",
            "next_action": NEXT_TARGET,
            "valid_for_claim": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "blocker_id": "BLK4631_1_positive_gap_bundle",
            "blocks": "local-GR theorem promotion",
            "missing": "Z_mem>0, M2_mem>0, source-channel silence and boundary no-flux on same branch",
            "next_action": NEXT_TARGET,
            "valid_for_claim": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "blocker_id": "BLK4631_2_epsilon_values",
            "blocks": "bound fallback",
            "missing": "epsilon_A, epsilon_B, Z_min, M2/Z and Newton normalization C_N",
            "next_action": NEXT_TARGET,
            "valid_for_claim": False,
            "timestamp_utc": now,
        },
    ]


def promotion_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "gate_id": "PROM4631_0_exact_beta_zero",
            "promotion_condition": "Full parent I_q-even descent of A_m is signed; beta_visible=0 follows by DER4631_0/1.",
            "current_result": "conditional theorem written; parent signature missing",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "gate_id": "PROM4631_1_local_GR_insert",
            "promotion_condition": "PROM4631_0 plus positive gap, zero explicit EM/hidden source and boundary no-flux.",
            "current_result": "blocked by full signature bundle",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "gate_id": "PROM4631_2_bound_route",
            "promotion_condition": "If beta nonzero, epsilon_A route supplies co-normalized alpha_AB and lambda_mem that pass bound runners.",
            "current_result": "blocked missing numeric parent coefficients",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
    ]


def decision_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "decision_id": "DEC4631_0",
            "decision": DECISION,
            "meaning": "The branch-extremum theorem is now derived conditionally: full parent I_q-even descent of A_m proves beta_visible=0. Existing weak leakage-frame symmetry is explicitly rejected for scalar beta zero, so the honest fallback is epsilon_A coefficient fill and bound running.",
            "status": "NONCLAIM_DERIVATION_ADVANCE_WITH_REJECTION",
            "best_route": "hunt the full parent vertical involution signature and A_m even descent first; if absent, run epsilon_A bound route",
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        }
    ]


def status_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch_id": BRANCH_ID,
            "status": "PRIVATE_NONCLAIM_DERIVATION_ADVANCE",
            "summary": "branch extremum is proved under full parent I_q-even matter descent; weak leakage symmetry is rejected; epsilon_A fallback rows are ready",
            "valid_for_claim": False,
            "claim_allowed": False,
            "next_target": NEXT_TARGET,
            "timestamp_utc": now,
        }
    ]


def next_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch_id": BRANCH_ID,
            "timestamp_utc": now,
            "next_target": NEXT_TARGET,
            "reason": "4631 proves exactly what symmetry would kill beta_visible, and rejects weaker routes; now either source that parent signature or instantiate epsilon_A bound rows.",
            "derive_first": "hunt parent vertical involution I_q and A_m even descent in source corpus",
            "fallback": "fill epsilon_A/Z/M2/C_N bound runner without exact-zero claim",
            "valid_for_claim": False,
        }
    ]


def write_doc(now: str, groups: dict[str, list[dict[str, Any]]]) -> None:
    body = f"""# 4631 - Branch Extremum Symmetry Or Parent Coefficient Fill

Marker: `{MARKER}`

Branch: `{BRANCH_ID}`

Timestamp: `{now}`

## Result

4630 needed `beta_visible=0`. 4631 proves the exact conditional route and rejects the weak route.

Strong route:

If a full parent vertical involution `I_q` exists with `q o I_q=q`, fixes the local GR/Newton section, and the visible matter scale descends evenly,

`A_m(q,z)=A_m(q,-z)`,

then differentiating at `z=0` gives

`partial_A A_m(q,0) = -partial_A A_m(q,0)`,

so

`partial_A A_m(q,0)=0`,

and therefore

`beta_visible = partial_A ln A_m|0 = 0`.

Inserted into 4630 with `Z_mem>0`, `M2_mem>0`, source-channel silence and no incoming scalar boundary flux, this gives first-order local memory silence and the local GR/Newton branch.

Rejected route:

ordinary leakage-frame rotations/reflections are not enough, because prior 4526 evidence keeps scalar signed channels alive. If the strong `I_q`/even-`A_m` route is not signed, the honest fallback is an explicit coefficient

`epsilon_A := ||P_vert d ln A_m/dz|0||`,

with

`alpha_AB <= C_N epsilon_A epsilon_B / Z_min`.

## Source Register

{markdown_table(groups["sources"])}

## Symmetry Route Audit

{markdown_table(groups["symmetry"])}

## Branch Extremum Derivation

{markdown_table(groups["derivation"])}

## Epsilon-A Coefficient Fill

{markdown_table(groups["epsilon"])}

## Local-GR Insert Rows

{markdown_table(groups["local_insert"])}

## Controls

{markdown_table(groups["controls"])}

## Blockers

{markdown_table(groups["blockers"])}

## Promotion Gates

{markdown_table(groups["promotions"])}

## Decision

{markdown_table(groups["decisions"])}

## Next Target

`{NEXT_TARGET}`
"""
    write_text(DOC_PATH, body)


def write_formal(now: str) -> None:
    body = f"""# 647 - PPC4161 Branch Extremum Symmetry Or Parent Coefficient Fill

Marker: `{MARKER}`

Branch: `{BRANCH_ID}`

4631 proves the exact conditional branch-extremum route:

`A_m(q,z)=A_m(q,-z) => partial_A A_m(q,0)=0 => beta_visible=partial_A ln A_m|0=0`.

This is sufficient to feed the 4630 local-GR theorem only if the full parent vertical involution `I_q`, even matter descent, positive gap, source-channel silence and boundary no-flux are all signed on the same branch.

Weak leakage-frame symmetry is rejected for beta zero because scalar signed channels can remain linear. If the strong route is not signed, the fallback coefficient is

`epsilon_A := ||P_vert d ln A_m/dz|0||`,

feeding

`alpha_AB <= C_N epsilon_A epsilon_B/Z_min`.

Next target: `{NEXT_TARGET}`.
"""
    write_text(FORMAL_PATH, body)


def append_integrations() -> None:
    append_once(
        SPINE_PATH,
        MARKER,
        f"""
## PPC4161 Branch Extremum Symmetry Or Parent Coefficient Fill 4631

Marker: `{MARKER}`

4631 proves the exact conditional branch-extremum theorem: full parent `I_q`-even descent of `A_m` forces `beta_visible=0`. It also rejects ordinary leakage-frame symmetry as insufficient for scalar beta zero. If the strong parent signature is not found, the local branch must carry an explicit `epsilon_A` coefficient into the co-normalized bound route.

Next: `{NEXT_TARGET}`.
""",
    )
    append_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""
## PPC4161 Packet - Branch Extremum Symmetry 4631

Marker: `{PACKET_MARKER}`

Local packet update: the clean local-GR path is no longer vague. Prove full parent `I_q` plus even visible matter scale, or keep `epsilon_A` as a real source-coupling coefficient. Weak leakage-frame symmetry is not enough for the scalar channel.

Next: `{NEXT_TARGET}`.
""",
    )
    if CLAIM_ID not in read_text(CLAIMS_PATH):
        with CLAIMS_PATH.open("a", encoding="utf-8", newline="") as handle:
            writer = csv.writer(handle)
            writer.writerow([
                CLAIM_ID,
                "local_gr_derivation",
                "4631 proves the conditional branch-extremum route for beta_visible=0 and rejects weak leakage-frame symmetry for scalar beta zero.",
                "Generated source register, symmetry audit, derivation rows, epsilon coefficient rows, local-GR insert rows, controls, blockers, promotion gates, decision, status, next target and validation.",
                "branch_extremum_conditional_beta_zero_nonclaim",
                NEXT_TARGET,
                "Treating weak leakage-frame symmetry or private GR-parity import as a parent proof of beta_visible=0.",
                "local_gr",
                str(DOC_PATH),
                NEXT_TARGET,
                "No local-GR/Newton/PPN pass until full parent I_q-even matter descent and positive gap/source/boundary signatures are signed, or epsilon_A bound route passes.",
            ])


def validation_rows(groups: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    checks: list[dict[str, Any]] = []

    def add(check_id: str, status: bool, detail: str) -> None:
        checks.append({
            "checkpoint": CHECKPOINT,
            "check_id": check_id,
            "status": "PASS" if status else "FAIL",
            "detail": detail,
            "valid_for_claim": False,
            "claim_allowed": False,
        })

    all_sources = all(row["path_exists"] and row["needle_found"] for row in groups["sources"])
    add("VAL4631_00_sources_exist_and_needles_found", all_sources, "all cited paths/needles found" if all_sources else "missing source path or needle")

    csv_paths = [
        SOURCE_REGISTER,
        SYMMETRY_CSV,
        DERIVATION_CSV,
        EPSILON_CSV,
        LOCAL_INSERT_CSV,
        CONTROL_CSV,
        BLOCKERS_CSV,
        PROMOTION_CSV,
        DECISION_CSV,
        STATUS_CSV,
        NEXT_CSV,
    ]
    parse_ok = True
    parse_details: list[str] = []
    for path in csv_paths:
        try:
            parse_details.append(f"{path.name}:{len(read_csv(path))}")
        except Exception as exc:
            parse_ok = False
            parse_details.append(f"{path.name}:ERROR:{exc}")
    add("VAL4631_01_csv_parse", parse_ok, ";".join(parse_details))

    add("VAL4631_02_strong_route_present", "SYM4631_0_strong_parent_vertical_involution" in read_text(SYMMETRY_CSV), "strong I_q route present")
    add("VAL4631_03_weak_route_rejected", "REJECTED_FOR_BETA_VISIBLE_ZERO" in read_text(SYMMETRY_CSV), "weak leakage symmetry rejected")
    add("VAL4631_04_beta_zero_derivation", "DER4631_1_beta_visible_zero" in read_text(DERIVATION_CSV), "beta zero derivation present")
    add("VAL4631_05_epsilon_fallback", "EPS4631_0_epsilon_A" in read_text(EPSILON_CSV), "epsilon_A fallback row present")
    add("VAL4631_06_local_gr_insert", "LGR4631_0_strong_symmetry_to_local_GR" in read_text(LOCAL_INSERT_CSV), "local-GR insert row present")

    generated_groups = list(groups.values())
    no_claims = not any(any_claim_true(group) for group in generated_groups)
    add("VAL4631_07_all_rows_nonclaim", no_claims, "no generated row promotes a claim")
    add("VAL4631_08_doc_marker", MARKER in read_text(DOC_PATH), "checkpoint doc marker present")
    add("VAL4631_09_formal_marker", MARKER in read_text(FORMAL_PATH), "formal marker present")
    add("VAL4631_10_claim_register", CLAIM_ID in read_text(CLAIMS_PATH), "claim register row present")
    add("VAL4631_11_spine_marker", MARKER in read_text(SPINE_PATH), "spine marker present")
    add("VAL4631_12_packet_marker", PACKET_MARKER in read_text(PACKET_PATH), "packet marker present")
    add("VAL4631_13_next_target", NEXT_TARGET in read_text(NEXT_CSV), NEXT_TARGET)
    add("VAL4631_14_public_stage_clean", git_clean(PUBLIC_STAGE), str(PUBLIC_STAGE))
    add("VAL4631_15_backup_repo_clean", git_clean(BACKUP_REPO), str(BACKUP_REPO))

    overall = all(row["status"] == "PASS" for row in checks)
    add("VAL4631_OVERALL", overall, "4631 branch extremum checkpoint")
    return checks


def main() -> None:
    now = utc_now()
    groups = {
        "sources": source_rows(now),
        "symmetry": symmetry_rows(now),
        "derivation": derivation_rows(now),
        "epsilon": epsilon_rows(now),
        "local_insert": local_insert_rows(now),
        "controls": control_rows(now),
        "blockers": blocker_rows(now),
        "promotions": promotion_rows(now),
        "decisions": decision_rows(now),
        "statuses": status_rows(now),
        "nexts": next_rows(now),
    }

    write_csv(SOURCE_REGISTER, groups["sources"])
    write_csv(SYMMETRY_CSV, groups["symmetry"])
    write_csv(DERIVATION_CSV, groups["derivation"])
    write_csv(EPSILON_CSV, groups["epsilon"])
    write_csv(LOCAL_INSERT_CSV, groups["local_insert"])
    write_csv(CONTROL_CSV, groups["controls"])
    write_csv(BLOCKERS_CSV, groups["blockers"])
    write_csv(PROMOTION_CSV, groups["promotions"])
    write_csv(DECISION_CSV, groups["decisions"])
    write_csv(STATUS_CSV, groups["statuses"])
    write_csv(NEXT_CSV, groups["nexts"])

    write_doc(now, groups)
    write_formal(now)
    append_integrations()
    write_csv(VALIDATION_CSV, validation_rows(groups))

    print(f"4631 checkpoint generated: {DOC_PATH}")
    print(f"Validation: {VALIDATION_CSV}")


if __name__ == "__main__":
    main()
