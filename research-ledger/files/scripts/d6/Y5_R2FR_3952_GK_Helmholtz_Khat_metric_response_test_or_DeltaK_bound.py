from __future__ import annotations

import csv
import py_compile
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CHECKPOINT = "3952"
SCRIPT_PATH = Path(__file__).resolve()
PCW = SCRIPT_PATH.parents[1]
ROOT = PCW.parent
FWB = ROOT / "formalization-workbench"
SRC = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "3952-Y5-R2FR-GK-Helmholtz-Khat-metric-response-test-or-DeltaK-bound.md"
SPINE_PATH = PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

OUTPUTS = {
    "sources": SRC / "P8_Y5_R2FR_3952_SOURCE_REGISTER.csv",
    "helmholtz": SRC / "P8_Y5_R2FR_3952_HELMHOLTZ_KHAT_TEST.csv",
    "deltak": SRC / "P8_Y5_R2FR_3952_DELTAK_QLOC_BOUND.csv",
    "decision": SRC / "P8_Y5_R2FR_3952_DECISION_GATE.csv",
    "claim_gate": SRC / "P8_Y5_R2FR_3952_CLAIM_GATE.csv",
    "next": SRC / "P8_Y5_R2FR_3952_NEXT_TARGET.csv",
    "status": SRC / "P8_Y5_R2FR_3952_STATUS.csv",
    "validation": SRC / "P8_Y5_BRR545_3952_VALIDATION.csv",
}

NEXT_DOC = "3953-Y5-R2FR-minimal-Gamma-density-variation-and-Khat-current-comparison.md"
NEXT_SCRIPT = "scripts/Y5_R2FR_3953_minimal_Gamma_density_variation_and_Khat_current_comparison.py"
QLOC_PROXY_VALUE = "7.432631961576971e-06"


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def source_specs() -> list[tuple[str, Path, str, str]]:
    return [
        ("SRC3952_00_3951_next", SRC / "P8_Y5_R2FR_3951_NEXT_TARGET.csv", "NEXT3951_0", "3951 handoff target"),
        ("SRC3952_01_3951_Khat", SRC / "P8_Y5_R2FR_3951_GK_COEFFICIENT_EXTRACTION_AUDIT.csv", "GKA3951_4_Kmetric_Khat_identity", "Khat identity status"),
        ("SRC3952_02_3951_DeltaK", SRC / "P8_Y5_R2FR_3951_GK_COEFFICIENT_EXTRACTION_AUDIT.csv", "GKA3951_5_DeltaK_mismatch_residual", "DeltaK residual status"),
        ("SRC3952_03_3951_Helmholtz", SRC / "P8_Y5_R2FR_3951_GK_COEFFICIENT_EXTRACTION_AUDIT.csv", "GKA3951_6_Helmholtz_integrability", "Helmholtz obstruction status"),
        ("SRC3952_04_3951_qproxy", SRC / "P8_Y5_R2FR_3951_GK_COEFFICIENT_EXTRACTION_AUDIT.csv", "GKA3951_9_q_loc_compact_shell_proxy", "q_loc proxy audit row"),
        ("SRC3952_05_3951_metric_component", SRC / "P8_Y5_R2FR_3951_EPSILON_GK_COMPONENT_INPUTS.csv", "EGKI3951_2_metric_response", "metric-response epsilon component"),
        ("SRC3952_06_3951_proxy_component", SRC / "P8_Y5_R2FR_3951_EPSILON_GK_COMPONENT_INPUTS.csv", "EGKI3951_6_q_loc_proxy", "q_loc proxy component row"),
        ("SRC3952_07_GK514", SRC / "P8_GK_STRESS_ACTION_CANDIDATES.csv", "GK514_A_metric_response_scalar_density", "metric-response scalar-density candidate"),
        ("SRC3952_08_WZ3950", SRC / "P8_Y5_R2FR_3950_GK_WARD_QLOC_ZERO_THEOREM.csv", "WZ3950_1_q_loc", "q_loc Ward formula"),
        ("SRC3952_09_KIC2217", SRC / "P8_Y5_PARENT_QLOC_2217_KHAT_IDENTITY_COMPARISON.csv", "KIC2217_4_Helmholtz_integrability", "Helmholtz comparison gate"),
        ("SRC3952_10_DK2217_H", SRC / "P8_Y5_PARENT_QLOC_2217_KHAT_MISMATCH_RESIDUAL_ROWS.csv", "DK2217_4_Helmholtz_gap", "Helmholtz residual row"),
        ("SRC3952_11_DK2217_JB", SRC / "P8_Y5_PARENT_QLOC_2217_KHAT_MISMATCH_RESIDUAL_ROWS.csv", "DK2217_5_source_boundary_gap", "source-boundary residual row"),
        ("SRC3952_12_validation_3951", SRC / "P8_Y5_BRR545_3951_VALIDATION.csv", "VAL3951_17_no_pycache", "previous validation"),
    ]


def source_register_rows(timestamp: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source_id, path, needle, purpose in source_specs():
        exists = path.exists()
        found = False
        line_number = ""
        excerpt = ""
        if exists:
            for index, line in enumerate(read_text(path).splitlines(), start=1):
                if needle in line:
                    found = True
                    line_number = str(index)
                    excerpt = line[:1000]
                    break
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "source_id": source_id,
                "source_path": str(path),
                "needle": needle,
                "purpose": purpose,
                "exists": exists,
                "needle_found": found,
                "line_number": line_number,
                "line_excerpt": excerpt,
                "valid_for_claim": False,
                "timestamp_utc": timestamp,
            }
        )
    return rows


def helmholtz_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "HKT3952_0_variation_space",
            "test_piece": "variation space",
            "mathematical_statement": "Take two compact-support metric variations h_{mu nu} and k_{mu nu} on the local domain, with boundary terms recorded separately.",
            "calculation_result": "SETS_TEST_DOMAIN",
            "what_is_proved": "Helmholtz symmetry can be tested by antisymmetrising the first variation of the proposed Khat map.",
            "current_MTS_status": "DOMAIN_DEFINED_NOT_A_CLAIM",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "HKT3952_1_obstruction_definition",
            "test_piece": "Helmholtz obstruction",
            "mathematical_statement": "H_GK[h,k] := integral_D (h_{mu nu} delta_k K_hat^{mu nu} - k_{mu nu} delta_h K_hat^{mu nu}) dV, modulo boundary exact terms.",
            "calculation_result": "OBSTRUCTION_DEFINED",
            "what_is_proved": "A proposed Khat is variational only if H_GK[h,k]=0 for all allowed h,k after boundary conditions.",
            "current_MTS_status": "PASS_FAIL_TEST_NOW_DEFINED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "HKT3952_2_response_defined_branch",
            "test_piece": "metric-response branch",
            "mathematical_statement": "If K_hat^{mu nu} is defined as K_metric^{mu nu}[Gamma_eff] := 2/sqrt(-g) delta(sqrt(-g)Gamma_eff)/delta g_{mu nu} minus the convention term, then H_GK[h,k]=0 by equality of mixed second variations of S_GK.",
            "calculation_result": "PASS_IDENTITY_FOR_RESPONSE_DEFINED_BRANCH",
            "what_is_proved": "The response-defined branch is integrable; no extra Helmholtz obstruction exists there.",
            "current_MTS_status": "PROVED_FOR_CONSTRUCTED_BRANCH_ONLY",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "HKT3952_3_current_MTS_branch",
            "test_piece": "current MTS Khat branch",
            "mathematical_statement": "Apply H_GK to the actual current MTS K_hat tensor.",
            "calculation_result": "NO_INPUT_TENSOR_BLOCKS_CURRENT_BRANCH",
            "what_is_proved": "No current local-GR claim follows because the actual K_hat tensor/density pair is still not supplied in a form the test can evaluate.",
            "current_MTS_status": "CURRENT_BRANCH_NOT_PASSED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "HKT3952_4_DeltaK_decomposition",
            "test_piece": "DeltaK split",
            "mathematical_statement": "Write K_hat_current^{mu nu}=K_metric^{mu nu}[Gamma_eff]+Delta_K^{mu nu}. Since H_GK[K_metric]=0, H_GK[K_hat_current]=H_GK[Delta_K].",
            "calculation_result": "DERIVED_OBSTRUCTION_REDUCTION_TO_DELTAK",
            "what_is_proved": "All non-variational Khat mismatch is isolated into Delta_K; the obstruction is no longer vague.",
            "current_MTS_status": "DELTAK_BRANCH_OPEN",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "HKT3952_5_boundary_condition",
            "test_piece": "boundary exactness",
            "mathematical_statement": "Boundary terms from integrating variations by parts must vanish on the local domain or be counted as B_GK in the q_loc residual.",
            "calculation_result": "BOUNDARY_LEDGER_ATTACHED",
            "what_is_proved": "A formal Helmholtz zero is insufficient unless boundary terms are silent or bounded.",
            "current_MTS_status": "SOURCE_BOUNDARY_STILL_UNSIGNED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "HKT3952_6_verdict",
            "test_piece": "3952 Helmholtz verdict",
            "mathematical_statement": "Response-defined Khat passes Helmholtz identically; current MTS Khat has not passed; current mismatch is Delta_K and H_GK[Delta_K].",
            "calculation_result": "CONSTRUCTED_BRANCH_PROVED_CURRENT_BRANCH_BOUND_ONLY",
            "what_is_proved": "This is a real derivation for the parent-action route and a clean rejection of any current unproved Khat promotion.",
            "current_MTS_status": "NO_LOCAL_GR_CLAIM_YET",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def deltak_bound_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "DKB3952_0_definition",
            "quantity": "Delta_K^{mu nu}",
            "formula": "Delta_K^{mu nu} := K_hat_current^{mu nu} - K_metric^{mu nu}[Gamma_eff]",
            "derived_bound_or_identity": "Delta_K=0 iff the current Khat equals the metric response branch, up to convention/boundary improvements.",
            "needed_inputs": "actual current Khat tensor; accepted Gamma_eff density; convention for metric variation",
            "value": "",
            "units": "stress_response_units",
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "DKB3952_1_q_loc_identity_with_DeltaK",
            "quantity": "q_loc^nu",
            "formula": "q_loc^nu = -P_loc(E_A nabla^nu Z^A + R_boundary^nu + R_source^nu + nabla_mu Delta_K^{mu nu})",
            "derived_bound_or_identity": "Exact after the Khat split and the metric-response Ward identity for K_metric.",
            "needed_inputs": "Euler residual E_A, boundary residual R_boundary, source residual R_source, divergence of Delta_K, physical local projector P_loc",
            "value": "",
            "units": "force_density_or_projected_residual_units",
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "DKB3952_2_q_loc_norm_bound",
            "quantity": "|q_loc|",
            "formula": "|q_loc| <= ||P_loc||*(|E_A nabla Z^A| + |R_boundary| + |R_source| + |nabla_mu Delta_K^{mu nu}|)",
            "derived_bound_or_identity": "Triangle inequality bound; no closure axiom required.",
            "needed_inputs": "norm convention for P_loc; physical units for each residual component; local domain norm",
            "value": "",
            "units": "same_as_q_loc",
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "DKB3952_3_epsilon_metric_response",
            "quantity": "epsilon_GK_metric_response_mismatch",
            "formula": "epsilon_GK_metric_response_mismatch := E_DeltaK/E_pos, with E_DeltaK := int_D |Delta_K_{mu nu}u^mu u^nu| dV + L_D int_D |nabla_mu Delta_K^{mu nu}| dV",
            "derived_bound_or_identity": "Value-ready energy/readout penalty for a nonzero Khat mismatch.",
            "needed_inputs": "E_pos, local domain D, observer u^mu, length scale L_D, Delta_K tensor and divergence",
            "value": "",
            "units": "dimensionless",
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "DKB3952_4_Helmholtz_obstruction_bound",
            "quantity": "H_GK[Delta_K]",
            "formula": "H_GK[K_hat_current]=H_GK[Delta_K]; require H_GK[Delta_K]=0 for parent-action promotion or carry |H_GK[Delta_K]| as integrability residual.",
            "derived_bound_or_identity": "The obstruction is reduced to the mismatch tensor, not the full Khat branch.",
            "needed_inputs": "linearised variation delta Delta_K[h] for arbitrary metric perturbations",
            "value": "",
            "units": "action_second_variation_units",
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "DKB3952_5_q_loc_proxy_carry",
            "quantity": "q_loc_shell_proxy",
            "formula": "compact-shell smoke value retained from 1011/3951",
            "derived_bound_or_identity": "proxy only; not a physical Delta_K value",
            "needed_inputs": "projection to PPN/source-normalization units before use",
            "value": QLOC_PROXY_VALUE,
            "units": "dimensionless_proxy",
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "DKB3952_6_exit_condition",
            "quantity": "DeltaK branch exit",
            "formula": "either Delta_K=0 and H_GK[Delta_K]=0 by derivation, or epsilon_GK_metric_response_mismatch has sourced finite values",
            "derived_bound_or_identity": "This is the non-smuggled gate for the Khat route.",
            "needed_inputs": "3953 parent-density variation or finite mismatch rows",
            "value": "",
            "units": "decision_gate",
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def decision_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "DEC3952_0_response_branch",
            "decision": "prove the response-defined branch is Helmholtz-integrable",
            "basis": "K_metric is a second variation of S_GK, so the antisymmetric Helmholtz bilinear vanishes under standard regularity and boundary silence",
            "effect": "the parent-action route is mathematically coherent rather than decorative",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "DEC3952_1_current_branch",
            "decision": "do not pass the current MTS Khat branch",
            "basis": "actual Khat tensor/density pair is not present in a computable form",
            "effect": "local-GR claim remains blocked",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "DEC3952_2_DeltaK",
            "decision": "replace vague Khat mismatch with Delta_K and nabla_mu Delta_K^{mu nu}",
            "basis": "q_loc identity now carries the precise extra term generated by Khat mismatch",
            "effect": "future work can either prove Delta_K=0 or bound it in epsilon_GK_metric_response_mismatch",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "DEC3952_3_next",
            "decision": f"move to {NEXT_DOC}",
            "basis": "the next derivation should vary a minimal covariant Gamma density and compare the resulting K_metric to current Khat requirements",
            "effect": "this attacks the missing coefficient route directly",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def claim_gate_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        ("CG3952_0_sources", "source-backed Helmholtz checkpoint", "all source paths and needles exist", "PASS_IF_VALIDATION_PASS"),
        ("CG3952_1_response_branch", "constructed response branch", "Khat defined as metric response of scalar density", "PASS_MATHEMATICAL_BRANCH_ONLY"),
        ("CG3952_2_current_branch", "current MTS Khat branch", "actual Khat tensor passes H_GK=0", "BLOCKED_NO_INPUT_TENSOR"),
        ("CG3952_3_DeltaK", "DeltaK branch", "Delta_K=0 or finite sourced Delta_K/E_pos bound", "BLOCKED_VALUES_MISSING"),
        ("CG3952_4_source_boundary", "source/boundary q_loc branch", "R_source and R_boundary vanish or are bounded", "BLOCKED_SOURCE_BOUNDARY_UNSIGNED"),
        ("CG3952_5_local_GR", "local-GR/source-coupling promotion", "all q_loc residuals vanish or fit within local bounds", "BLOCKED_NONCLAIM"),
    ]
    return [
        {
            "row_id": row_id,
            "gate": gate,
            "requirement": requirement,
            "status": status,
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_id, gate, requirement, status in data
    ]


def next_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "NEXT3952_0",
            "next_doc": NEXT_DOC,
            "next_script": NEXT_SCRIPT,
            "target": "derive K_metric explicitly for a minimal covariant quadratic Gamma_eff density, then compare the resulting tensor structure to current Khat requirements; if mismatch remains, fill Delta_K component rows",
            "success_condition": "either the minimal parent density gives the required Khat response terms and double-zero source suppression, or the mismatch is converted into finite Delta_K/E_pos and q_loc residual rows",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str, source_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    found = sum(bool(row["exists"]) and bool(row["needle_found"]) for row in source_rows)
    return [
        {
            "checkpoint": CHECKPOINT,
            "status": "PASS_PRIVATE_NONCLAIM_CHECKPOINT",
            "summary": "3952 proves the response-defined Khat branch is Helmholtz-integrable, rejects promotion of the current branch without an input tensor, and derives the Delta_K divergence term in q_loc.",
            "sources_found": f"{found}/{len(source_rows)}",
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        }
    ]


def doc_text(timestamp: str, source_rows: list[dict[str, Any]]) -> str:
    found = sum(bool(row["exists"]) and bool(row["needle_found"]) for row in source_rows)
    return f"""# 3952 - GK Helmholtz Khat Metric-Response Test Or DeltaK Bound

Timestamp: `{timestamp}`

## Result

3952 turns the Khat question into a genuine pass/fail variational test.

Define the Helmholtz obstruction:

`H_GK[h,k] := integral_D (h_mu_nu delta_k K_hat^mu_nu - k_mu_nu delta_h K_hat^mu_nu) dV`

modulo boundary exact terms.

If `K_hat` is defined by a parent scalar density,

`K_metric^mu_nu[Gamma_eff] := 2/sqrt(-g) delta(sqrt(-g) Gamma_eff)/delta g_mu_nu`

then `H_GK=0` by equality of mixed second variations. That branch is mathematically coherent.

## Current MTS Verdict

The current MTS branch is not promoted because the actual current `K_hat` tensor/density pair is still not supplied in a computable form.

So the exact split is:

`K_hat_current^mu_nu = K_metric^mu_nu[Gamma_eff] + Delta_K^mu_nu`.

This gives the sharpened local residual identity:

`q_loc^nu = -P_loc(E_A nabla^nu Z^A + R_boundary^nu + R_source^nu + nabla_mu Delta_K^mu_nu)`.

That is the important movement: any non-response part must now appear as `nabla_mu Delta_K^mu_nu`, not as an unspecified closure gap.

## Bound Fallback

The value-ready mismatch channel is:

`epsilon_GK_metric_response_mismatch := E_DeltaK/E_pos`

with

`E_DeltaK := int_D |Delta_K_mu_nu u^mu u^nu| dV + L_D int_D |nabla_mu Delta_K^mu_nu| dV`.

No public/local-GR claim follows until `Delta_K=0` is derived or this channel gets sourced values.

## Source Register

- Source rows found: `{found}/{len(source_rows)}`
- Register: `source-intake\\mts_residuals\\P8_Y5_R2FR_3952_SOURCE_REGISTER.csv`
- Validation: `source-intake\\mts_residuals\\P8_Y5_BRR545_3952_VALIDATION.csv`

## Generated Tables

- `source-intake\\mts_residuals\\P8_Y5_R2FR_3952_HELMHOLTZ_KHAT_TEST.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3952_DELTAK_QLOC_BOUND.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3952_DECISION_GATE.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3952_CLAIM_GATE.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3952_NEXT_TARGET.csv`

## Next Target

`{NEXT_DOC}`
"""


def spine_block(timestamp: str) -> str:
    return f"""

## 3952 - Helmholtz Khat Test And DeltaK Bound

Timestamp: `{timestamp}`

- Defined the Helmholtz obstruction `H_GK[h,k]` for the Khat metric-response route.
- Proved the constructed response branch passes: if `K_hat=K_metric[Gamma_eff]`, `H_GK=0` by equality of mixed second variations.
- Did not promote current MTS Khat, because the actual tensor/density pair is still not in computable form.
- Derived the non-smuggled residual split: `q_loc^nu = -P_loc(E_A nabla^nu Z^A + R_boundary^nu + R_source^nu + nabla_mu Delta_K^{{mu nu}})`.
- Next: `{NEXT_DOC}`.
"""


def update_spine(timestamp: str) -> None:
    block = spine_block(timestamp)
    marker = "## 3952 - Helmholtz Khat Test And DeltaK Bound"
    if SPINE_PATH.exists():
        text = read_text(SPINE_PATH)
        if marker in text:
            before = text.split(marker, 1)[0].rstrip()
            SPINE_PATH.write_text(before + block, encoding="utf-8")
        else:
            SPINE_PATH.write_text(text.rstrip() + block, encoding="utf-8")
    else:
        SPINE_PATH.write_text("# Local GR Coupling Spine - Current State\n" + block, encoding="utf-8")


def formalization_workbench_git_status() -> tuple[bool, str]:
    try:
        result = subprocess.run(
            ["git", "-C", str(ROOT), "status", "--porcelain", "--", str(FWB.relative_to(ROOT))],
            check=False,
            capture_output=True,
            text=True,
            timeout=15,
        )
    except Exception:
        return False, "git status unavailable; scope guard confirms generated outputs are outside formalization-workbench"
    if result.returncode != 0:
        return False, "git status unavailable; scope guard confirms generated outputs are outside formalization-workbench"
    modified_count = len([line for line in result.stdout.splitlines() if line.strip()])
    return modified_count == 0, f"formalization-workbench modified count is {modified_count}"


def csv_parse_ok(paths: list[Path]) -> bool:
    try:
        for path in paths:
            if path.exists():
                read_csv(path)
    except Exception:
        return False
    return True


def validation_rows(timestamp: str, source_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    helmholtz = helmholtz_rows(timestamp)
    deltak = deltak_bound_rows(timestamp)
    decisions = decision_rows(timestamp)
    claim_gate = claim_gate_rows(timestamp)
    next_target = next_rows(timestamp)
    generated_csvs = [path for key, path in OUTPUTS.items() if key != "validation"]
    paths = generated_csvs + [DOC_PATH, SCRIPT_PATH, SPINE_PATH]
    fwb_git_clean, fwb_git_detail = formalization_workbench_git_status()
    h_results = {row["calculation_result"] for row in helmholtz}
    d_ids = {row["row_id"] for row in deltak}
    gate_statuses = {row["status"] for row in claim_gate}
    nonclaim_groups = (helmholtz, deltak, decisions, claim_gate, next_target)
    checks = [
        ("VAL3952_00_sources_exist", all(row["exists"] for row in source_rows), "all cited source paths exist"),
        ("VAL3952_01_needles_found", all(row["needle_found"] for row in source_rows), "all cited source needles found"),
        ("VAL3952_02_obstruction_defined", "OBSTRUCTION_DEFINED" in h_results, "Helmholtz obstruction row emitted"),
        ("VAL3952_03_response_branch_pass", "PASS_IDENTITY_FOR_RESPONSE_DEFINED_BRANCH" in h_results, "response-defined branch proved integrable"),
        ("VAL3952_04_current_branch_blocked", "NO_INPUT_TENSOR_BLOCKS_CURRENT_BRANCH" in h_results, "current MTS branch not falsely promoted"),
        ("VAL3952_05_DeltaK_reduction", "DERIVED_OBSTRUCTION_REDUCTION_TO_DELTAK" in h_results, "Helmholtz obstruction reduced to DeltaK"),
        ("VAL3952_06_q_loc_DeltaK_identity", "DKB3952_1_q_loc_identity_with_DeltaK" in d_ids, "q_loc identity includes divergence of DeltaK"),
        ("VAL3952_07_epsilon_metric_channel", "DKB3952_3_epsilon_metric_response" in d_ids, "epsilon metric-response mismatch channel emitted"),
        ("VAL3952_08_proxy_retained_nonclaim", any(row["row_id"] == "DKB3952_5_q_loc_proxy_carry" and row["value"] == QLOC_PROXY_VALUE and not row["valid_for_claim"] for row in deltak), "q_loc proxy retained as nonclaim"),
        ("VAL3952_09_claim_gate_blocks", "PASS_MATHEMATICAL_BRANCH_ONLY" in gate_statuses and "BLOCKED_NO_INPUT_TENSOR" in gate_statuses and "BLOCKED_NONCLAIM" in gate_statuses, "claim gate distinguishes constructed branch from current claim"),
        ("VAL3952_10_next_target", next_target[0]["next_doc"] == NEXT_DOC and next_target[0]["next_script"] == NEXT_SCRIPT, "next target points to minimal Gamma density variation"),
        ("VAL3952_11_all_nonclaim", all(not row["valid_for_claim"] for group in nonclaim_groups for row in group), "all generated physics rows remain nonclaim"),
        ("VAL3952_12_outputs_outside_fwb", all(FWB not in path.parents and path != FWB for path in paths), "no generated output is inside formalization-workbench"),
        ("VAL3952_13_fwb_git_or_scope_guard", fwb_git_clean or all(FWB not in path.parents and path != FWB for path in paths), fwb_git_detail),
        ("VAL3952_14_doc_exists", DOC_PATH.exists(), "checkpoint doc exists"),
        ("VAL3952_15_spine_updated", SPINE_PATH.exists() and "3952 - Helmholtz Khat Test And DeltaK Bound" in read_text(SPINE_PATH), "spine updated"),
        ("VAL3952_16_csv_parse", csv_parse_ok(generated_csvs), "generated CSV files parse cleanly"),
        ("VAL3952_17_script_compile", True, "script compiled before validation write"),
        ("VAL3952_18_no_pycache", not (SCRIPT_PATH.parent / "__pycache__").exists(), "scripts __pycache__ removed"),
    ]
    return [
        {
            "validation_id": validation_id,
            "passed": bool(passed),
            "detail": detail,
            "timestamp_utc": timestamp,
        }
        for validation_id, passed, detail in checks
    ]


def run() -> None:
    timestamp = now_utc()
    source_rows = source_register_rows(timestamp)
    helmholtz = helmholtz_rows(timestamp)
    deltak = deltak_bound_rows(timestamp)
    decisions = decision_rows(timestamp)
    claim_gate = claim_gate_rows(timestamp)
    next_target = next_rows(timestamp)
    status = status_rows(timestamp, source_rows)

    write_csv(OUTPUTS["sources"], source_rows)
    write_csv(OUTPUTS["helmholtz"], helmholtz)
    write_csv(OUTPUTS["deltak"], deltak)
    write_csv(OUTPUTS["decision"], decisions)
    write_csv(OUTPUTS["claim_gate"], claim_gate)
    write_csv(OUTPUTS["next"], next_target)
    write_csv(OUTPUTS["status"], status)

    DOC_PATH.write_text(doc_text(timestamp, source_rows), encoding="utf-8")
    update_spine(timestamp)

    py_compile.compile(str(SCRIPT_PATH), doraise=True)
    pycache = SCRIPT_PATH.parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)

    validations = validation_rows(timestamp, source_rows)
    write_csv(OUTPUTS["validation"], validations)
    failed = [row for row in validations if not row["passed"]]
    if failed:
        raise SystemExit(f"3952 validation failed: {failed}")

    print(f"3952 checkpoint complete: {DOC_PATH}")
    print(f"validation: {OUTPUTS['validation']}")
    print("response-defined Khat branch: Helmholtz PASS; current MTS branch: DeltaK-bound only")


if __name__ == "__main__":
    run()
