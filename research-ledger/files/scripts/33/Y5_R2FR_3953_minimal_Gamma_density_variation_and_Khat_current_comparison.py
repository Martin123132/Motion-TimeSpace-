from __future__ import annotations

import csv
import py_compile
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CHECKPOINT = "3953"
SCRIPT_PATH = Path(__file__).resolve()
PCW = SCRIPT_PATH.parents[1]
ROOT = PCW.parent
FWB = ROOT / "formalization-workbench"
SRC = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "3953-Y5-R2FR-minimal-Gamma-density-variation-and-Khat-current-comparison.md"
SPINE_PATH = PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

OUTPUTS = {
    "sources": SRC / "P8_Y5_R2FR_3953_SOURCE_REGISTER.csv",
    "variation": SRC / "P8_Y5_R2FR_3953_MINIMAL_GAMMA_VARIATION.csv",
    "comparison": SRC / "P8_Y5_R2FR_3953_KHAT_COMPARISON_REQUIREMENTS.csv",
    "deltak": SRC / "P8_Y5_R2FR_3953_DELTAK_COMPONENT_TEMPLATE.csv",
    "decision": SRC / "P8_Y5_R2FR_3953_DECISION_GATE.csv",
    "claim_gate": SRC / "P8_Y5_R2FR_3953_CLAIM_GATE.csv",
    "next": SRC / "P8_Y5_R2FR_3953_NEXT_TARGET.csv",
    "status": SRC / "P8_Y5_R2FR_3953_STATUS.csv",
    "validation": SRC / "P8_Y5_BRR545_3953_VALIDATION.csv",
}

NEXT_DOC = "3954-Y5-R2FR-Z-source-current-silence-and-PPN-normalization-map.md"
NEXT_SCRIPT = "scripts/Y5_R2FR_3954_Z_source_current_silence_and_PPN_normalization_map.py"


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
        ("SRC3953_00_3952_next", SRC / "P8_Y5_R2FR_3952_NEXT_TARGET.csv", "NEXT3952_0", "3952 handoff target"),
        ("SRC3953_01_3952_response", SRC / "P8_Y5_R2FR_3952_HELMHOLTZ_KHAT_TEST.csv", "HKT3952_2_response_defined_branch", "response branch Helmholtz pass"),
        ("SRC3953_02_3952_DeltaK", SRC / "P8_Y5_R2FR_3952_HELMHOLTZ_KHAT_TEST.csv", "HKT3952_4_DeltaK_decomposition", "DeltaK decomposition"),
        ("SRC3953_03_3952_q", SRC / "P8_Y5_R2FR_3952_DELTAK_QLOC_BOUND.csv", "DKB3952_1_q_loc_identity_with_DeltaK", "q_loc DeltaK identity"),
        ("SRC3953_04_3952_eps", SRC / "P8_Y5_R2FR_3952_DELTAK_QLOC_BOUND.csv", "DKB3952_3_epsilon_metric_response", "epsilon DeltaK channel"),
        ("SRC3953_05_GO516", SRC / "P8_GAMMA_OWNER_CANDIDATE_ACTION.csv", "GO516_A_response_doublet_quadratic_density", "response doublet candidate"),
        ("SRC3953_06_3950_density", SRC / "P8_Y5_R2FR_3950_GK_POSITIVE_AUXILIARY_SIGNATURE.csv", "GKS3950_0_parent_density", "positive auxiliary parent density"),
        ("SRC3953_07_3951_GAB", SRC / "P8_Y5_R2FR_3951_GK_COEFFICIENT_EXTRACTION_AUDIT.csv", "GKA3951_1_GAB_kinetic_signature", "GAB missing status"),
        ("SRC3953_08_3951_MAB", SRC / "P8_Y5_R2FR_3951_GK_COEFFICIENT_EXTRACTION_AUDIT.csv", "GKA3951_2_MAB_hessian_signature", "MAB missing status"),
        ("SRC3953_09_3951_PPN", SRC / "P8_Y5_R2FR_3951_GK_COEFFICIENT_EXTRACTION_AUDIT.csv", "GKA3951_11_PPN_source_lock", "PPN source lock status"),
        ("SRC3953_10_validation_3952", SRC / "P8_Y5_BRR545_3952_VALIDATION.csv", "VAL3952_18_no_pycache", "previous validation"),
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


def variation_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "MGV3953_0_density_ansatz",
            "object": "minimal covariant Gamma_eff density",
            "formula": "Gamma_quad = Gamma0 + 1/2 G_AB g^{alpha beta} nabla_alpha Z^A nabla_beta Z^B + 1/2 M_AB Z^A Z^B",
            "derivation": "Assume Z^A are scalar residual fields and G_AB,M_AB are local coefficient matrices; metric-dependence of G/M is separated into K_coeff.",
            "derived_result": "minimal parent density candidate constructed",
            "local_GR_use": "gives double-zero residual energy if Z=0 and nabla Z=0 after Gamma0/reference subtraction",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "MGV3953_1_metric_variation",
            "object": "K_metric full response",
            "formula": "K_metric^{mu nu} = Gamma_quad g^{mu nu} - G_AB nabla^mu Z^A nabla^nu Z^B + K_coeff^{mu nu}",
            "derivation": "2/sqrt(-g) delta(sqrt(-g)Gamma_quad)/delta g_{mu nu}; K_coeff stores metric-dependence of G_AB, M_AB, connection/coframe conventions, and boundary improvements.",
            "derived_result": "explicit Khat target structure derived up to the already-declared convention term",
            "local_GR_use": "current K_hat must reduce to this volume-plus-gradient-plus-coefficient structure or the difference is Delta_K",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "MGV3953_2_Euler_equation",
            "object": "Z^A Euler equation",
            "formula": "E_A = -nabla_mu(G_AB nabla^mu Z^B) + M_AB Z^B + 1/2 partial_A G_BC nabla Z^B.nabla Z^C + 1/2 partial_A M_BC Z^B Z^C + source/boundary terms",
            "derivation": "variation of Gamma_quad with respect to Z^A",
            "derived_result": "source-free linear branch is -G_AB box Z^B + M_AB Z^B=0 when G/M are locally constant",
            "local_GR_use": "positive M_AB and source silence imply local suppression/no-hair rather than a plateau axiom",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "MGV3953_3_double_zero",
            "object": "double-zero law",
            "formula": "Gamma_quad-Gamma0=O(Z^2,nabla Z^2), delta_Z Gamma_quad|_{Z=0,nabla Z=0}=0, K_metric-Gamma0 g=O(Z^2,nabla Z^2,K_coeff)",
            "derivation": "no linear term in Z and no linear derivative term in the quadratic density",
            "derived_result": "F_1=0 for the constructed branch",
            "local_GR_use": "first-order fifth-force/source-normalization leakage is absent if matter does not couple directly to Z and Gamma0 is reference-subtracted",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "MGV3953_4_positive_operator_condition",
            "object": "local no-hair/suppression condition",
            "formula": "G_AB positive on physical modes and M_AB >= m_gap^2 G_AB, with zero J_A and controlled boundary flux",
            "derivation": "multiply the linearized Euler equation by Z^A and integrate by parts over the local domain",
            "derived_result": "int(G_AB nabla Z^A.nabla Z^B + M_AB Z^A Z^B)dV = boundary/source work; zero boundary/source gives Z=0",
            "local_GR_use": "this is the desired local-vacuum suppression mechanism in theorem form",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "MGV3953_5_Helmholtz_status",
            "object": "Helmholtz integrability",
            "formula": "K_metric derived from Gamma_quad has H_GK=0 by construction",
            "derivation": "inherits 3952 mixed-second-variation result",
            "derived_result": "constructed minimal parent branch passes variational integrability",
            "local_GR_use": "leaves source-current and current-Khat matching as the nontrivial gates",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def comparison_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "KCR3953_0_volume_reference",
            "required_Khat_piece": "Gamma_quad g^{mu nu} volume/reference term",
            "minimal_branch_prediction": "present; Gamma0 g^{mu nu} must be absorbed into cosmological/reference sector or subtracted locally",
            "current_MTS_match": "NOT_CHECKABLE_CURRENT_TENSOR_MISSING",
            "DeltaK_if_missing": "DeltaK_volume",
            "next_action": "declare the reference convention and compare any current Khat volume term to Gamma_quad g^{mu nu}",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "KCR3953_1_gradient_anisotropic",
            "required_Khat_piece": "-G_AB nabla^mu Z^A nabla^nu Z^B gradient stress",
            "minimal_branch_prediction": "present with sign fixed by metric variation",
            "current_MTS_match": "NOT_CHECKABLE_CURRENT_TENSOR_MISSING",
            "DeltaK_if_missing": "DeltaK_gradient",
            "next_action": "map current Gamma/Khat variables to Z^A gradients or carry mismatch",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "KCR3953_2_coefficient_metric_dependence",
            "required_Khat_piece": "K_coeff^{mu nu}",
            "minimal_branch_prediction": "zero only if G_AB,M_AB have no hidden metric/coframe/connection dependence",
            "current_MTS_match": "UNSIGNED",
            "DeltaK_if_missing": "DeltaK_coeff",
            "next_action": "audit whether G_AB,M_AB depend on metric, curvature, coframe, D, or material variables",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "KCR3953_3_no_linear_Z",
            "required_Khat_piece": "no linear Z or nabla Z term",
            "minimal_branch_prediction": "present by construction",
            "current_MTS_match": "UNSIGNED_SOURCE_COUPLING",
            "DeltaK_if_missing": "DeltaK_linear",
            "next_action": "prove matter/source sector has no direct linear Z current J_A",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "KCR3953_4_PPN_source_normalization",
            "required_Khat_piece": "Z^A equals physical q_loc/PPN/source-normalization residual vector",
            "minimal_branch_prediction": "not supplied by Gamma_quad alone",
            "current_MTS_match": "OPEN",
            "DeltaK_if_missing": "DeltaK_PPN_map",
            "next_action": "3954 must derive J_A=0 or the finite source-normalization residual",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def deltak_template_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "DCT3953_0_total",
            "DeltaK_component": "Delta_K_total",
            "formula": "K_hat_current - (Gamma_quad g - G_AB nabla Z^A nabla Z^B + K_coeff)",
            "feeds": "nabla_mu Delta_K^{mu nu} and epsilon_GK_metric_response_mismatch",
            "value_status": "MISSING_CURRENT_KHAT_TENSOR",
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "DCT3953_1_volume",
            "DeltaK_component": "DeltaK_volume",
            "formula": "current volume/reference Khat term - Gamma_quad g^{mu nu}",
            "feeds": "cosmological/reference leakage and local source normalization",
            "value_status": "MISSING_REFERENCE_CONVENTION",
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "DCT3953_2_gradient",
            "DeltaK_component": "DeltaK_gradient",
            "formula": "current anisotropic Khat gradient term + G_AB nabla^mu Z^A nabla^nu Z^B",
            "feeds": "local fifth-force / PPN anisotropic stress residual",
            "value_status": "MISSING_Z_GRADIENT_MAP",
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "DCT3953_3_coeff",
            "DeltaK_component": "DeltaK_coeff",
            "formula": "current coefficient response - K_coeff^{mu nu}",
            "feeds": "hidden metric/coframe/connection dependence",
            "value_status": "MISSING_COEFFICIENT_DEPENDENCE_AUDIT",
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "DCT3953_4_source_linear",
            "DeltaK_component": "DeltaK_linear_or_J_A",
            "formula": "linear source-current term generated by matter dependence on Z^A or g_obs(Z)",
            "feeds": "R_source and PPN/source-normalization branch",
            "value_status": "NEXT_TARGET",
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def decision_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "DEC3953_0_parent_branch",
            "decision": "minimal quadratic Gamma density gives a coherent parent-action branch",
            "basis": "metric variation, Euler equation, double-zero law, positive-operator condition, and Helmholtz pass are all explicit",
            "effect": "the local plateau/suppression route is now derivable on this constructed branch",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "DEC3953_1_no_current_match_claim",
            "decision": "do not claim current MTS Khat match",
            "basis": "current Khat tensor is still not available to compare against the derived K_metric structure",
            "effect": "DeltaK component template remains active",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "DEC3953_2_coupling_next",
            "decision": f"move to {NEXT_DOC}",
            "basis": "the remaining dangerous term is direct source current J_A / PPN normalization, not Helmholtz",
            "effect": "next step attacks the coupling gap the user flagged",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def claim_gate_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        ("CG3953_0_sources", "source-backed variation checkpoint", "all source paths and needles exist", "PASS_IF_VALIDATION_PASS"),
        ("CG3953_1_variation", "minimal Gamma variation", "K_metric and E_A derived", "PASS_CONSTRUCTED_BRANCH"),
        ("CG3953_2_double_zero", "double-zero law", "F_1=0 on constructed branch", "PASS_CONSTRUCTED_BRANCH"),
        ("CG3953_3_current_Khat", "current MTS Khat match", "actual Khat equals derived K_metric", "BLOCKED_CURRENT_TENSOR_MISSING"),
        ("CG3953_4_source_current", "source-current silence", "J_A=0 or finite source residual", "BLOCKED_NEXT_TARGET"),
        ("CG3953_5_local_GR", "local-GR/source-coupling promotion", "Khat match plus source/PPN normalization close", "BLOCKED_NONCLAIM"),
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
            "row_id": "NEXT3953_0",
            "next_doc": NEXT_DOC,
            "next_script": NEXT_SCRIPT,
            "target": "derive the source-current condition J_A=delta S_matter/delta Z^A and map whether matter descends only through g_obs or couples directly to Z; convert any failure into a PPN/source-normalization residual",
            "success_condition": "either J_A=0 follows from quotient/descent plus no g_obs(Z) leakage, or finite rows are emitted for source-current and PPN normalization residuals",
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
            "summary": "3953 derives the minimal quadratic Gamma density variation, giving explicit K_metric, Euler, double-zero and no-hair conditions; current Khat match remains open and source-current coupling becomes the next target.",
            "sources_found": f"{found}/{len(source_rows)}",
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        }
    ]


def doc_text(timestamp: str, source_rows: list[dict[str, Any]]) -> str:
    found = sum(bool(row["exists"]) and bool(row["needle_found"]) for row in source_rows)
    return f"""# 3953 - Minimal Gamma Density Variation And Khat Current Comparison

Timestamp: `{timestamp}`

## Result

3953 takes the leap requested by 3952: vary an actual minimal covariant parent density.

The constructed density is:

`Gamma_quad = Gamma0 + 1/2 G_AB g^alpha_beta nabla_alpha Z^A nabla_beta Z^B + 1/2 M_AB Z^A Z^B`.

Its metric response is:

`K_metric^mu_nu = Gamma_quad g^mu_nu - G_AB nabla^mu Z^A nabla^nu Z^B + K_coeff^mu_nu`.

`K_coeff` stores hidden metric/coframe/connection dependence of `G_AB`, `M_AB`, and boundary conventions.

## What This Actually Proves

- The constructed branch is variational and inherits the 3952 Helmholtz pass.
- The branch has a double-zero: `Gamma_quad-Gamma0=O(Z^2,nabla Z^2)` and `F_1=0`.
- The source-free linear branch gives `-G_AB box Z^B + M_AB Z^B=0`.
- If `G_AB` is positive and `M_AB` has a positive gap, then zero source/boundary work gives local suppression/no-hair.

## What It Does Not Prove Yet

It does not prove current MTS already uses this `K_hat`. The current tensor still has to match:

`Gamma_quad g^mu_nu - G_AB nabla^mu Z^A nabla^nu Z^B + K_coeff^mu_nu`.

Any mismatch is now sorted into `DeltaK_volume`, `DeltaK_gradient`, `DeltaK_coeff`, or `DeltaK_linear_or_J_A`.

## Why The Next Step Is Coupling

The remaining dangerous term is direct matter/source current:

`J_A := delta S_matter/delta Z^A`.

If matter only descends through the observable metric and the observable metric has no first-order `Z` leakage, then `J_A=0`. If not, the failure becomes a PPN/source-normalization residual.

## Source Register

- Source rows found: `{found}/{len(source_rows)}`
- Register: `source-intake\\mts_residuals\\P8_Y5_R2FR_3953_SOURCE_REGISTER.csv`
- Validation: `source-intake\\mts_residuals\\P8_Y5_BRR545_3953_VALIDATION.csv`

## Next Target

`{NEXT_DOC}`
"""


def spine_block(timestamp: str) -> str:
    return f"""

## 3953 - Minimal Gamma Density Variation

Timestamp: `{timestamp}`

- Varied a concrete minimal parent density `Gamma_quad = Gamma0 + 1/2 G_AB g^{{alpha beta}} nabla_alpha Z^A nabla_beta Z^B + 1/2 M_AB Z^A Z^B`.
- Derived the target response `K_metric^{{mu nu}} = Gamma_quad g^{{mu nu}} - G_AB nabla^mu Z^A nabla^nu Z^B + K_coeff^{{mu nu}}`.
- Proved the constructed branch has `F_1=0` and a double-zero at `Z=0,nabla Z=0`, after `Gamma0` reference subtraction.
- Reduced current mismatch into `DeltaK_volume`, `DeltaK_gradient`, `DeltaK_coeff`, and `DeltaK_linear_or_J_A`.
- Next: `{NEXT_DOC}`.
"""


def update_spine(timestamp: str) -> None:
    block = spine_block(timestamp)
    marker = "## 3953 - Minimal Gamma Density Variation"
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
    variation = variation_rows(timestamp)
    comparison = comparison_rows(timestamp)
    deltak = deltak_template_rows(timestamp)
    decisions = decision_rows(timestamp)
    claim_gate = claim_gate_rows(timestamp)
    next_target = next_rows(timestamp)
    generated_csvs = [path for key, path in OUTPUTS.items() if key != "validation"]
    paths = generated_csvs + [DOC_PATH, SCRIPT_PATH, SPINE_PATH]
    fwb_git_clean, fwb_git_detail = formalization_workbench_git_status()
    variation_ids = {row["row_id"] for row in variation}
    comparison_ids = {row["row_id"] for row in comparison}
    deltak_ids = {row["row_id"] for row in deltak}
    gate_statuses = {row["status"] for row in claim_gate}
    nonclaim_groups = (variation, comparison, deltak, decisions, claim_gate, next_target)
    checks = [
        ("VAL3953_00_sources_exist", all(row["exists"] for row in source_rows), "all cited source paths exist"),
        ("VAL3953_01_needles_found", all(row["needle_found"] for row in source_rows), "all cited source needles found"),
        ("VAL3953_02_density_ansatz", "MGV3953_0_density_ansatz" in variation_ids, "minimal Gamma density emitted"),
        ("VAL3953_03_metric_variation", "MGV3953_1_metric_variation" in variation_ids, "K_metric variation emitted"),
        ("VAL3953_04_Euler_equation", "MGV3953_2_Euler_equation" in variation_ids, "Euler equation emitted"),
        ("VAL3953_05_double_zero", "MGV3953_3_double_zero" in variation_ids, "double-zero/F1=0 law emitted"),
        ("VAL3953_06_positive_operator", "MGV3953_4_positive_operator_condition" in variation_ids, "positive operator condition emitted"),
        ("VAL3953_07_Khat_requirements", {"KCR3953_0_volume_reference", "KCR3953_1_gradient_anisotropic", "KCR3953_2_coefficient_metric_dependence", "KCR3953_3_no_linear_Z", "KCR3953_4_PPN_source_normalization"}.issubset(comparison_ids), "Khat comparison requirements emitted"),
        ("VAL3953_08_DeltaK_components", {"DCT3953_0_total", "DCT3953_1_volume", "DCT3953_2_gradient", "DCT3953_3_coeff", "DCT3953_4_source_linear"}.issubset(deltak_ids), "DeltaK component template emitted"),
        ("VAL3953_09_claim_gate_blocks", "PASS_CONSTRUCTED_BRANCH" in gate_statuses and "BLOCKED_CURRENT_TENSOR_MISSING" in gate_statuses and "BLOCKED_NONCLAIM" in gate_statuses, "claim gate distinguishes constructed branch from current claim"),
        ("VAL3953_10_next_target", next_target[0]["next_doc"] == NEXT_DOC and next_target[0]["next_script"] == NEXT_SCRIPT, "next target points to source-current coupling map"),
        ("VAL3953_11_all_nonclaim", all(not row["valid_for_claim"] for group in nonclaim_groups for row in group), "all generated physics rows remain nonclaim"),
        ("VAL3953_12_outputs_outside_fwb", all(FWB not in path.parents and path != FWB for path in paths), "no generated output is inside formalization-workbench"),
        ("VAL3953_13_fwb_git_or_scope_guard", fwb_git_clean or all(FWB not in path.parents and path != FWB for path in paths), fwb_git_detail),
        ("VAL3953_14_doc_exists", DOC_PATH.exists(), "checkpoint doc exists"),
        ("VAL3953_15_spine_updated", SPINE_PATH.exists() and "3953 - Minimal Gamma Density Variation" in read_text(SPINE_PATH), "spine updated"),
        ("VAL3953_16_csv_parse", csv_parse_ok(generated_csvs), "generated CSV files parse cleanly"),
        ("VAL3953_17_script_compile", True, "script compiled before validation write"),
        ("VAL3953_18_no_pycache", not (SCRIPT_PATH.parent / "__pycache__").exists(), "scripts __pycache__ removed"),
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
    variation = variation_rows(timestamp)
    comparison = comparison_rows(timestamp)
    deltak = deltak_template_rows(timestamp)
    decisions = decision_rows(timestamp)
    claim_gate = claim_gate_rows(timestamp)
    next_target = next_rows(timestamp)
    status = status_rows(timestamp, source_rows)

    write_csv(OUTPUTS["sources"], source_rows)
    write_csv(OUTPUTS["variation"], variation)
    write_csv(OUTPUTS["comparison"], comparison)
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
        raise SystemExit(f"3953 validation failed: {failed}")

    print(f"3953 checkpoint complete: {DOC_PATH}")
    print(f"validation: {OUTPUTS['validation']}")
    print("minimal Gamma variation derived; next target is source-current coupling")


if __name__ == "__main__":
    run()
