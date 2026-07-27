from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = ROOT.parent / "formalization-workbench"
DOC = ROOT / "3555-Y5-R2FR-response-doublet-Gamma-owner-source-current-zero-or-q_loc-bound-fill.md"
CANONICAL_STATUS = OUT / "P8_Y5_response_doublet_Gamma_owner_q_loc_bound_status.csv"


SOURCES: dict[str, dict[str, Any]] = {
    "script_3555": {"path": Path(__file__).resolve(), "role": "3555 generator"},
    "doc_3554": {
        "path": ROOT / "3554-Y5-R2FR-Gamma-Khat-sector-action-existence-or-theta-GK-bound.md",
        "role": "Gamma/Khat sector handoff",
    },
    "next_3554": {
        "path": OUT / "P8_Y5_R2FR_3554_NEXT_TARGET.csv",
        "role": "3554 response-doublet target",
    },
    "q_loc_rows_3554": {
        "path": OUT / "P8_Y5_R2FR_3554_QLOC_RESIDUAL_RETENTION_ROWS.csv",
        "role": "q_loc residual handoff",
    },
    "gk_theorem_3554": {
        "path": OUT / "P8_Y5_R2FR_3554_GK_ACTION_THEOREM.csv",
        "role": "GK variational theorem",
    },
    "doc_517": {
        "path": ROOT / "517-response-doublet-action-variation-ledger-or-run-q_loc-bound.md",
        "role": "response-doublet variation ledger",
    },
    "response_contract": {
        "path": OUT / "P8_RESPONSE_DOUBLET_ACTION_CONTRACT.csv",
        "role": "response doublet action contract",
    },
    "response_variation": {
        "path": OUT / "P8_RESPONSE_DOUBLET_ACTION_VARIATION.csv",
        "role": "response doublet variation rows",
    },
    "gamma_owner_candidates": {
        "path": OUT / "P8_GAMMA_OWNER_CANDIDATE_ACTION.csv",
        "role": "Gamma owner candidate action",
    },
    "gamma_owner_decision": {
        "path": OUT / "P8_GAMMA_OWNER_OR_QLOC_BOUND_DECISION.csv",
        "role": "Gamma owner or q_loc bound decision",
    },
    "gamma_owner_tests": {
        "path": OUT / "P8_GAMMA_OWNER_OR_QLOC_BOUND_FORK_TESTS.csv",
        "role": "Gamma owner fork tests",
    },
    "gamma_owner_route": {
        "path": OUT / "P8_GAMMA_OWNER_OR_QLOC_BOUND_ROUTE_UPDATE.csv",
        "role": "Gamma owner route update",
    },
    "exchange_map_score": {
        "path": OUT / "P8_EXCHANGE_COMPONENT_MAP_SCORE.csv",
        "role": "exchange component map score",
    },
    "exchange_gate_tests": {
        "path": OUT / "P8_EXCHANGE_COMPONENT_GATE_TESTS.csv",
        "role": "exchange component gate tests",
    },
    "exchange_hard_rows": {
        "path": OUT / "P8_EXCHANGE_COMPONENT_HARD_ROWS.csv",
        "role": "Y5/Y6 hard row ledger",
    },
    "exchange_coeff_branch": {
        "path": OUT / "P8_EXCHANGE_COMPONENT_COEFFICIENT_BRANCH.csv",
        "role": "exchange coefficient branch",
    },
    "yloc_euler": {
        "path": OUT / "P8_YLOC_EULER_SYSTEM.csv",
        "role": "Yloc Euler system rows",
    },
    "q_loc_bound_spec": {
        "path": OUT / "P8_QLOC_BOUND_RUNNER_SPEC.csv",
        "role": "q_loc bound runner specification",
    },
    "local_residual_vector": {
        "path": OUT / "P8_LOCAL_GR_RESIDUAL_VECTOR_FROM_DOMAIN_SOURCE.csv",
        "role": "local GR residual vector mapping",
    },
}


def bool_text(value: bool) -> str:
    return "True" if value else "False"


def write_csv(path: Path, rows: list[dict[str, Any]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def csv_parse_ok(path: Path) -> bool:
    try:
        read_csv_rows(path)
    except (csv.Error, OSError, UnicodeDecodeError):
        return False
    return True


def markdown_escape(value: Any) -> str:
    return str(value).replace("\n", "<br>").replace("|", "\\|")


def markdown_table(rows: list[dict[str, Any]], fields: list[str]) -> str:
    if not rows:
        return "_No rows._"
    header = "| " + " | ".join(fields) + " |"
    divider = "| " + " | ".join("---" for _ in fields) + " |"
    body = [
        "| " + " | ".join(markdown_escape(row.get(field, "")) for field in fields) + " |"
        for row in rows
    ]
    return "\n".join([header, divider, *body])


def source_rows() -> list[dict[str, Any]]:
    return [
        {
            "source_id": source_id,
            "path": str(item["path"]),
            "exists": bool_text(item["path"].exists()),
            "role": item["role"],
            "valid_for_claim": "False",
        }
        for source_id, item in SOURCES.items()
    ]


def theorem_rows() -> list[dict[str, Any]]:
    return [
        {
            "theorem_id": "RDT3555_0_quadratic_Gamma",
            "claim_piece": "formal double-zero",
            "statement": "Gamma_eff=Gamma0+1/2 M_AB Z^A Z^B+O(Z^4) gives Gamma_eff-Gamma0=0 and partial_A Gamma_eff=0 at Z=0.",
            "proof_step": "The first variation is delta Gamma_eff/delta Z^A=M_AB Z^B+O(Z^3).",
            "condition_needed": "Z=0 must be the physical local residual state and Gamma0 must be a fixed background subtraction.",
            "current_status": "FORMAL_DOUBLE_ZERO_CONDITIONAL",
            "source_path": str(SOURCES["response_variation"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "RDT3555_1_positive_operator_zero",
            "claim_piece": "source-current zero theorem",
            "statement": "If L_AB is positive/self-adjoint on the compact local branch and L_AB Z^B=J_A+B_A with J_A=0 and B_A=0, then Z=0.",
            "proof_step": "Multiply by Z^A and integrate: integral Z^A L_AB Z^B = integral Z^A J_A + boundary; positivity forces Z=0 when the right side vanishes.",
            "condition_needed": "positive operator, gauge/constraint removal, zero odd source current, zero boundary flux and compact local collar.",
            "current_status": "EXACT_CONDITIONAL_THEOREM_UNSIGNED",
            "source_path": str(SOURCES["response_variation"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "RDT3555_2_GK_unlock",
            "claim_piece": "Gamma/Khat local zero",
            "statement": "If the response-doublet theorem gives Z=0 and K_hat is the metric response of Gamma_eff, then the GK sector satisfies the double-zero gate needed by q_loc.",
            "proof_step": "3554 already reduces q_loc to the projected divergence of T_GK; the response theorem supplies the local fixed-point silence piece.",
            "condition_needed": "metric-response match, Helmholtz, P_loc ownership and boundary no-flux still remain separate gates.",
            "current_status": "CONDITIONAL_INPUT_ONLY",
            "source_path": str(SOURCES["gk_theorem_3554"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "RDT3555_3_hard_row_refusal",
            "claim_piece": "no oddness shortcut",
            "statement": "Exchange oddness does not kill Y5 source normalization or Y6 extra stress by itself.",
            "proof_step": "Measured GM/source normalization is naturally exchange-even; Bianchi ownership can conserve exchange-even extra stress rather than erase it.",
            "condition_needed": "separate source-normalization theorem and extra-stress invisibility/topological theorem, or explicit coefficient bounds.",
            "current_status": "HARD_ROWS_BLOCK_PROMOTION",
            "source_path": str(SOURCES["exchange_hard_rows"]["path"]),
            "valid_for_claim": "False",
        },
    ]


def zero_audit_rows() -> list[dict[str, Any]]:
    return [
        {
            "audit_id": "RZA3555_0_component_map",
            "required_zero": "Z^A equals physical local residual vector through PPN/source-normalization order",
            "current_evidence": "exchange component map has zero claim-valid component rows",
            "status": "FAIL_CURRENT_CLAIM",
            "blocks": "using Z=0 as local GR/PPN/source theorem",
            "source_path": str(SOURCES["exchange_map_score"]["path"]),
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "audit_id": "RZA3555_1_positive_operator",
            "required_zero": "L_AB positive after gauge/constraint removal",
            "current_evidence": "response contract says formal candidate only",
            "status": "UNSIGNED",
            "blocks": "energy identity cannot force Z=0",
            "source_path": str(SOURCES["response_contract"]["path"]),
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "audit_id": "RZA3555_2_odd_source_zero",
            "required_zero": "J_Z=0 for all local exchange-odd source channels",
            "current_evidence": "Y0-Y4 are conditional/open and Y5 hard-fails exchange oddness",
            "status": "UNSIGNED_HARD_Y5",
            "blocks": "Newton/source-normalized GR",
            "source_path": str(SOURCES["exchange_hard_rows"]["path"]),
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "audit_id": "RZA3555_3_boundary_zero",
            "required_zero": "B_Z=0 / no boundary metric-response flux",
            "current_evidence": "Y2 boundary route is structurally plausible but not parent-derived",
            "status": "CONDITIONAL_NOT_SIGNED",
            "blocks": "alpha3/boundary force and mass flux",
            "source_path": str(SOURCES["exchange_map_score"]["path"]),
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "audit_id": "RZA3555_4_extra_stress_invisible",
            "required_zero": "Y6 extra stress is topological/invisible or bounded below PPN thresholds",
            "current_evidence": "Bianchi ownership allows conserved exchange-even stress; not a zero theorem",
            "status": "RETAINED_DEBT_HARD_Y6",
            "blocks": "EH-only exterior and local PPN silence",
            "source_path": str(SOURCES["exchange_hard_rows"]["path"]),
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "audit_id": "RZA3555_5_metric_response",
            "required_zero": "response doublet Gamma owner gives K_hat as metric response",
            "current_evidence": "3554 keeps metric-response match and Helmholtz unsigned",
            "status": "PARALLEL_GK_GATE_UNSIGNED",
            "blocks": "turning response doublet into S_GK owner",
            "source_path": str(SOURCES["gk_theorem_3554"]["path"]),
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def hard_row_rows() -> list[dict[str, Any]]:
    return [
        {
            "hard_id": "HR3555_0_Y5_source_normalization",
            "component": "Y5_source_normalization",
            "why_hard": "Newtonian recovery depends on measured source normalization, which is naturally exchange-even rather than killed by oddness.",
            "cannot_use": "exchange symmetry alone",
            "needed_theorem": "observed GM is pure even EH source while all non-EH normalization operators are odd/local-zero or coefficient-bounded",
            "fallback_quantity": "c_domain_source_normalization_operator or measured-GM residual vector",
            "status": "HARD_NEXT_TARGET",
            "source_path": str(SOURCES["exchange_hard_rows"]["path"]),
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "hard_id": "HR3555_1_Y6_stress_Bianchi",
            "component": "Y6_stress_Bianchi",
            "why_hard": "Bianchi conservation owns extra stress but does not make it vanish.",
            "cannot_use": "Noether/Ward ownership alone",
            "needed_theorem": "extra stress is topological/invisible or carried as explicit residual below local PPN/operator bounds",
            "fallback_quantity": "retained T_extra residual vector",
            "status": "RETAINED_DEBT",
            "source_path": str(SOURCES["exchange_hard_rows"]["path"]),
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "hard_id": "HR3555_2_boundary_odd_charge",
            "component": "Y2_boundary_flux",
            "why_hard": "compact boundary can carry an odd vector/current class unless local triviality is derived.",
            "cannot_use": "stationary boundary language alone",
            "needed_theorem": "local compact boundary odd class zero/no-flux",
            "fallback_quantity": "W_boundary_alpha3_epsilon_boundary_flux",
            "status": "CONDITIONAL_ROUTE",
            "source_path": str(SOURCES["exchange_map_score"]["path"]),
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def qloc_bound_rows() -> list[dict[str, Any]]:
    return [
        {
            "bound_id": "QB3555_0_compact_shell_budget",
            "from_failure": "response owner/source-boundary zero not signed",
            "quantity": "epsilon_q_loc_shell",
            "formula": "max |P_loc d_rel J_rel| or equivalent compact-shell q_loc leakage",
            "current_value": "7.432631961576971e-06 anchor_from_220_nonclaim",
            "units": "dimensionless compact-shell proxy until arena-normalized",
            "bound_or_gate": "map into PPN/source-normalization units before claim",
            "source_path": str(SOURCES["q_loc_bound_spec"]["path"]),
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "bound_id": "QB3555_1_alpha3_pressure",
            "from_failure": "boundary/domain flux or Y5/Y6 survives",
            "quantity": "alpha3_GK",
            "formula": "alpha3_GK = W_GK_alpha3 * epsilon_q_loc",
            "current_value": "MISSING_W_GK_ALPHA3_EPSILON_QLOC",
            "units": "dimensionless",
            "bound_or_gate": "abs(alpha3_GK) <= 4e-20 where alpha3 mapping applies",
            "source_path": str(SOURCES["q_loc_bound_spec"]["path"]),
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "bound_id": "QB3555_2_PPN_vector",
            "from_failure": "Z physical PPN lock missing",
            "quantity": "alpha1_alpha2_xi_GK",
            "formula": "R_PPN_GK = W_GK_PPN * epsilon_q_loc",
            "current_value": "MISSING_W_GK_PPN_EPSILON_QLOC",
            "units": "dimensionless PPN residual",
            "bound_or_gate": "compare to alpha1/alpha2/xi gates after weak-field map",
            "source_path": str(SOURCES["local_residual_vector"]["path"]),
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "bound_id": "QB3555_3_R11_source_normalization",
            "from_failure": "Y5 source normalization not killed",
            "quantity": "c_GK_source_normalization_operator",
            "formula": "R11_GK = c_GK_source_normalization_operator",
            "current_value": "MISSING_GK_R11_OPERATOR_COEFFICIENT_VECTOR",
            "units": "dimensionless or declared operator units",
            "bound_or_gate": "operator family, units, normalization and bound comparison required",
            "source_path": str(SOURCES["exchange_coeff_branch"]["path"]),
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "bound_id": "QB3555_4_GM_Gdot",
            "from_failure": "source-normalization even scalar theorem fails",
            "quantity": "dln_mu_obs_dt_GK",
            "formula": "time component of q_loc/source normalization projected to measured-GM drift",
            "current_value": "MISSING_GK_GMDRIFT_PROJECTION",
            "units": "yr^-1 or declared clock/time units",
            "bound_or_gate": "use Gdot/source-normalization ledgers after time component is sourced",
            "source_path": str(SOURCES["q_loc_bound_spec"]["path"]),
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "bound_id": "QB3555_5_Textra",
            "from_failure": "Y6 exchange-even extra stress survives",
            "quantity": "T_extra_GK",
            "formula": "retained extra-stress contribution to Bianchi/PPN/operator rows",
            "current_value": "MISSING_TEXTRA_TO_PPN_R11_VECTOR",
            "units": "stress or normalized weak-field operator units",
            "bound_or_gate": "topological/invisible stress theorem or explicit residual score required",
            "source_path": str(SOURCES["exchange_coeff_branch"]["path"]),
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "D3555_0_response_verdict",
            "question": "Did 3555 close the response-doublet Gamma owner?",
            "decision": "No live claim. The formal double-zero and positive-operator zero theorem are exact conditionally, but source-current, boundary, Y5, Y6 and PPN-lock gates are unsigned.",
            "basis": "517 variation ledger and exchange component maps keep Y5 source normalization and Y6 stress as hard active blockers.",
            "consequence": "response doublet remains best constructive route, not a local-GR/Newton proof.",
            "valid_for_claim": "False",
        },
        {
            "decision_id": "D3555_1_q_loc_fallback",
            "question": "Is the residual fallback now explicit?",
            "decision": "Yes as nonclaim schema rows, not as scored evidence.",
            "basis": "q_loc rows now include compact shell, alpha3, PPN vector, R11/source normalization, GM drift and T_extra slots.",
            "consequence": "if Y5/Y6 cannot be derived, testing moves to coefficient/source acquisition rather than closure language.",
            "valid_for_claim": "False",
        },
        {
            "decision_id": "D3555_2_next_target",
            "question": "Which hard row first?",
            "decision": "Y5 source-normalization even-scalar owner.",
            "basis": "Y5 blocks Newton/source-normalized GR more directly than the algebraic q_loc theorem.",
            "consequence": "Move to 3556: source-normalization even-scalar theorem or R11 coefficient fill.",
            "valid_for_claim": "False",
        },
    ]


def status_rows() -> list[dict[str, Any]]:
    return [
        {
            "status_id": "STATUS3555_0",
            "checkpoint": "3555 response-doublet Gamma owner source-current zero or q_loc bound fill",
            "claim_allowed": "False",
            "response_doublet_status": "FORMAL_DOUBLE_ZERO_SURVIVES; SOURCE_BOUNDARY_Y5_Y6_PPN_LOCK_UNSIGNED",
            "q_loc_bound_status": "NONCLAIM_COEFFICIENT_ROWS_INSTALLED_NOT_SCORED",
            "hardest_rows": "Y5_source_normalization; Y6_stress_Bianchi",
            "strongest_result": "positive-operator zero theorem is exact conditional, but exchange oddness cannot kill measured GM/source normalization",
            "next_target": "3556-Y5-R2FR-source-normalization-even-scalar-owner-or-q_loc-R11-coefficient-fill.md",
            "valid_for_claim": "False",
        }
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT3555_0",
            "target_doc": "3556-Y5-R2FR-source-normalization-even-scalar-owner-or-q_loc-R11-coefficient-fill.md",
            "target_script": "scripts/Y5_R2FR_3556_source_normalization_even_scalar_owner_or_q_loc_R11_coefficient_fill.py",
            "objective": "derive the Y5 source-normalization even-scalar theorem showing measured GM is pure even EH source while non-EH normalization offsets vanish or are bounded; if not, produce R11/q_loc source-normalization coefficient rows",
            "success_gate": "either Y5 source-normalization is parent-owned zero for local Newton/source coupling, or c_GK_source_normalization_operator obtains source-ready nonclaim coefficient rows",
            "reason": "Y5 is the hard row that blocks Newton/source-normalized GR after the response-doublet formal double-zero",
            "valid_for_claim": "False",
        }
    ]


def validation_rows(
    generated_csvs: list[Path],
    sources: list[dict[str, Any]],
    theorem: list[dict[str, Any]],
    zero_audit: list[dict[str, Any]],
    hard_rows: list[dict[str, Any]],
    bounds: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    all_sources_exist = all(row["exists"] == "True" for row in sources)
    csvs_parse = all(csv_parse_ok(path) for path in generated_csvs)
    positive_theorem_present = any(row["theorem_id"] == "RDT3555_1_positive_operator_zero" for row in theorem)
    hard_y5_y6_present = {"HR3555_0_Y5_source_normalization", "HR3555_1_Y6_stress_Bianchi"}.issubset(
        {row["hard_id"] for row in hard_rows}
    )
    qloc_bounds_ready = {"QB3555_1_alpha3_pressure", "QB3555_2_PPN_vector", "QB3555_3_R11_source_normalization"}.issubset(
        {row["bound_id"] for row in bounds}
    )
    all_nonclaim = (
        all(row["valid_for_claim"] == "False" for row in theorem)
        and all(row["claim_allowed"] == "False" and row["valid_for_claim"] == "False" for row in zero_audit)
        and all(row["claim_allowed"] == "False" and row["valid_for_claim"] == "False" for row in hard_rows)
        and all(row["claim_allowed"] == "False" and row["valid_for_claim"] == "False" for row in bounds)
        and all(row["valid_for_claim"] == "False" for row in decisions)
    )
    missing_markers_present = all("MISSING_" in row["current_value"] or "anchor_from_220_nonclaim" in row["current_value"] for row in bounds)
    no_formalization_outputs = all(not path.resolve().is_relative_to(FORMALIZATION.resolve()) for path in generated_csvs)

    return [
        {
            "validation_id": "VAL3555_0_sources_exist",
            "passes": bool_text(all_sources_exist),
            "status": "PASS" if all_sources_exist else "FAIL",
            "detail": f"{sum(row['exists'] == 'True' for row in sources)}/{len(sources)} cited source paths exist",
        },
        {
            "validation_id": "VAL3555_1_generated_csvs_parse",
            "passes": bool_text(csvs_parse),
            "status": "PASS" if csvs_parse else "FAIL",
            "detail": f"{len(generated_csvs)} generated CSV files parse with DictReader",
        },
        {
            "validation_id": "VAL3555_2_positive_zero_theorem_present",
            "passes": bool_text(positive_theorem_present),
            "status": "PASS" if positive_theorem_present else "FAIL",
            "detail": "positive-operator response-doublet zero theorem is present",
        },
        {
            "validation_id": "VAL3555_3_hard_rows_covered",
            "passes": bool_text(hard_y5_y6_present),
            "status": "PASS" if hard_y5_y6_present else "FAIL",
            "detail": "Y5 source-normalization and Y6 stress hard rows are explicit",
        },
        {
            "validation_id": "VAL3555_4_qloc_bound_rows_ready",
            "passes": bool_text(qloc_bounds_ready),
            "status": "PASS" if qloc_bounds_ready else "FAIL",
            "detail": "q_loc fallback rows cover alpha3, PPN vector and R11/source normalization",
        },
        {
            "validation_id": "VAL3555_5_all_rows_nonclaim_with_missing_markers",
            "passes": bool_text(all_nonclaim and missing_markers_present),
            "status": "PASS" if all_nonclaim and missing_markers_present else "FAIL",
            "detail": "all rows keep claims disabled and expose missing theorem/numeric inputs",
        },
        {
            "validation_id": "VAL3555_6_formalization_workbench_untouched",
            "passes": bool_text(no_formalization_outputs),
            "status": "PASS" if no_formalization_outputs else "FAIL",
            "detail": "3555 generated outputs only inside post-checkpoint-work",
        },
    ]


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    lines = [
        "# 3555 - Response-doublet Gamma owner source-current zero or q_loc bound fill",
        "",
        "## Verdict",
        "",
        "- **Formal mechanism survives:** quadratic response doublets give the desired double-zero shape, `Gamma_eff-Gamma0=0` and `partial_A Gamma_eff=0` at `Z=0`.",
        "- **Actual zero requires more:** positive operator plus `J_Z=0` and `B_Z=0` would force `Z=0`, but those source/boundary zeros are not parent-signed.",
        "- **Hard blockers remain:** `Y5_source_normalization` and `Y6_stress_Bianchi` are not killed by exchange oddness.",
        "- **Fallback installed:** q_loc now has nonclaim coefficient rows for compact-shell, alpha3, PPN, R11/source-normalization, GM drift and extra stress.",
        "",
        "## Response Theorem",
        "",
        markdown_table(
            rows_by_name["theorem"],
            ["theorem_id", "claim_piece", "statement", "current_status"],
        ),
        "",
        "## Zero Audit",
        "",
        markdown_table(
            rows_by_name["zero_audit"],
            ["audit_id", "required_zero", "status", "blocks"],
        ),
        "",
        "## Hard Rows",
        "",
        markdown_table(
            rows_by_name["hard_rows"],
            ["hard_id", "component", "why_hard", "needed_theorem", "status"],
        ),
        "",
        "## q_loc Bound Rows",
        "",
        markdown_table(
            rows_by_name["bounds"],
            ["bound_id", "quantity", "formula", "current_value", "bound_or_gate"],
        ),
        "",
        "## Decisions",
        "",
        markdown_table(
            rows_by_name["decisions"],
            ["decision_id", "question", "decision", "consequence"],
        ),
        "",
        "## Validation",
        "",
        markdown_table(
            rows_by_name["validation"],
            ["validation_id", "passes", "status", "detail"],
        ),
        "",
        "## Next target",
        "",
        "Move to `3556-Y5-R2FR-source-normalization-even-scalar-owner-or-q_loc-R11-coefficient-fill.md`: attack `Y5_source_normalization`, because it is the response-doublet hard row blocking Newton/source-normalized GR.",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
    ]
    DOC.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)

    sources = source_rows()
    theorem = theorem_rows()
    zero_audit = zero_audit_rows()
    hard_rows = hard_row_rows()
    bounds = qloc_bound_rows()
    decisions = decision_rows()
    status = status_rows()
    next_target = next_target_rows()

    outputs: dict[Path, tuple[list[dict[str, Any]], list[str]]] = {
        OUT / "P8_Y5_R2FR_3555_SOURCE_REGISTER.csv": (
            sources,
            ["source_id", "path", "exists", "role", "valid_for_claim"],
        ),
        OUT / "P8_Y5_R2FR_3555_RESPONSE_DOUBLET_THEOREM.csv": (
            theorem,
            [
                "theorem_id",
                "claim_piece",
                "statement",
                "proof_step",
                "condition_needed",
                "current_status",
                "source_path",
                "valid_for_claim",
            ],
        ),
        OUT / "P8_Y5_R2FR_3555_SOURCE_BOUNDARY_ZERO_AUDIT.csv": (
            zero_audit,
            ["audit_id", "required_zero", "current_evidence", "status", "blocks", "source_path", "claim_allowed", "valid_for_claim"],
        ),
        OUT / "P8_Y5_R2FR_3555_Y5_Y6_HARD_ROW_AUDIT.csv": (
            hard_rows,
            [
                "hard_id",
                "component",
                "why_hard",
                "cannot_use",
                "needed_theorem",
                "fallback_quantity",
                "status",
                "source_path",
                "claim_allowed",
                "valid_for_claim",
            ],
        ),
        OUT / "P8_Y5_R2FR_3555_QLOC_BOUND_FILL_ROWS.csv": (
            bounds,
            [
                "bound_id",
                "from_failure",
                "quantity",
                "formula",
                "current_value",
                "units",
                "bound_or_gate",
                "source_path",
                "claim_allowed",
                "valid_for_claim",
            ],
        ),
        OUT / "P8_Y5_R2FR_3555_DECISION_LEDGER.csv": (
            decisions,
            ["decision_id", "question", "decision", "basis", "consequence", "valid_for_claim"],
        ),
        OUT / "P8_Y5_R2FR_3555_STATUS.csv": (
            status,
            [
                "status_id",
                "checkpoint",
                "claim_allowed",
                "response_doublet_status",
                "q_loc_bound_status",
                "hardest_rows",
                "strongest_result",
                "next_target",
                "valid_for_claim",
            ],
        ),
        OUT / "P8_Y5_R2FR_3555_NEXT_TARGET.csv": (
            next_target,
            ["next_id", "target_doc", "target_script", "objective", "success_gate", "reason", "valid_for_claim"],
        ),
        CANONICAL_STATUS: (
            status,
            [
                "status_id",
                "checkpoint",
                "claim_allowed",
                "response_doublet_status",
                "q_loc_bound_status",
                "hardest_rows",
                "strongest_result",
                "next_target",
                "valid_for_claim",
            ],
        ),
    }

    generated_paths: list[Path] = []
    for path, (rows, fields) in outputs.items():
        write_csv(path, rows, fields)
        generated_paths.append(path)

    validation = validation_rows(generated_paths, sources, theorem, zero_audit, hard_rows, bounds, decisions)
    validation_path = OUT / "P8_Y5_BRR545_3555_VALIDATION.csv"
    write_csv(validation_path, validation, ["validation_id", "passes", "status", "detail"])
    generated_paths.append(validation_path)

    write_doc(
        {
            "theorem": theorem,
            "zero_audit": zero_audit,
            "hard_rows": hard_rows,
            "bounds": bounds,
            "decisions": decisions,
            "status": status,
            "next_target": next_target,
            "validation": validation,
        }
    )

    print(f"wrote {DOC}")
    for path in generated_paths:
        print(f"wrote {path}")


if __name__ == "__main__":
    main()
