from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
FORMALIZATION = ROOT.parent / "formalization-workbench"
DOC = ROOT / "3548-Y5-R2FR-typed-EM-coefficient-domain-no-Hom-certificate-or-alpha-closure-demotion.md"
CANONICAL_STATUS = OUT / "P8_Y5_typed_EM_noHom_or_alpha_closure_demotion_status.csv"

DD_E_CEILING = 1.372549019608e-12
ALPHA_COULOMB_CEILING = 1.407170315973e-12


SOURCES: dict[str, dict[str, Any]] = {
    "script_3548": {"path": Path(__file__).resolve(), "role": "3548 generator"},
    "doc_3547": {
        "path": ROOT / "3547-Y5-R2FR-parent-EM-same-owner-zero-or-Ke-alpha-source-leg.md",
        "role": "same-owner theorem attempt handoff",
    },
    "next_3547": {
        "path": OUT / "P8_Y5_R2FR_3547_NEXT_TARGET.csv",
        "role": "3547 selected typed no-Hom target",
    },
    "countermodels_3547": {
        "path": OUT / "P8_Y5_R2FR_3547_COUNTERMODEL_LEDGER.csv",
        "role": "active alpha countermodels",
    },
    "same_owner_3547": {
        "path": OUT / "P8_Y5_R2FR_3547_SAME_OWNER_THEOREM_ATTEMPT.csv",
        "role": "conditional same-owner theorem",
    },
    "operator_domain_2659": {
        "path": OUT / "P8_Y5_NO_HIDDEN_VISIBLE_HOM_2659_OPERATOR_DOMAIN_THEOREM_ATTEMPT.csv",
        "role": "no-hidden-visible operator-domain theorem attempt",
    },
    "countermodels_2659": {
        "path": OUT / "P8_Y5_NO_HIDDEN_VISIBLE_HOM_2659_COUNTERMODEL_LEDGER.csv",
        "role": "older no-Hom countermodel ledger",
    },
    "coefficient_gate_3118": {
        "path": OUT / "P8_Y5_R2FR_3118_NO_HIDDEN_VISIBLE_COEFFICIENT_HOM_GATE.csv",
        "role": "local EM coefficient no-Hom gate",
    },
    "typed_requirements_1235": {
        "path": OUT / "P8_Y5_R10_1235_TYPED_DOMAIN_REQUIREMENTS.csv",
        "role": "unique F2 typed-domain requirements",
    },
    "unique_f2_attempt_1235": {
        "path": OUT / "P8_Y5_R10_1235_UNIQUE_F2_TYPED_COEFFICIENT_DOMAIN_PROOF_ATTEMPT.csv",
        "role": "unique F2 typed coefficient proof attempt",
    },
    "unique_f2_blockers_1235": {
        "path": OUT / "P8_Y5_R10_1235_UNIQUE_F2_BLOCKER_LEDGER.csv",
        "role": "unique F2 blocker ledger",
    },
    "meta_theorem_1236": {
        "path": OUT / "P8_Y5_R10_1236_NO_HIDDEN_VISIBLE_COEFFICIENT_META_THEOREM.csv",
        "role": "conditional no-Hom meta theorem",
    },
    "unique_owner_1467": {
        "path": OUT / "P8_Y5_R10_1467_UNIQUE_EM_OWNER_NO_HIDDEN_F2_PROOF_ATTEMPT.csv",
        "role": "unique EM owner/no-hidden-F2 attempt",
    },
    "operator_class_1467": {
        "path": OUT / "P8_Y5_R10_1467_NO_HIDDEN_F2_OPERATOR_CLASSIFICATION.csv",
        "role": "F2 operator classification",
    },
    "signature_1319": {
        "path": OUT / "P8_Y5_R10_1319_MINIMAL_SIGNATURE_CANDIDATE.csv",
        "role": "minimal parent object-language signature candidate",
    },
    "construction_1319": {
        "path": OUT / "P8_Y5_R10_1319_CLAUSE_CONSTRUCTION_ATTEMPT.csv",
        "role": "minimal signature construction attempt",
    },
    "demotion_1319": {
        "path": OUT / "P8_Y5_R10_1319_THEOREM_ROUTE_CLOSURE_DEMOTION.csv",
        "role": "closure-only demotion precedent",
    },
    "survival_1319": {
        "path": OUT / "P8_Y5_R10_1319_FINITE_SOURCE_ROW_SURVIVAL_MAP.csv",
        "role": "finite row survival map",
    },
    "calibrated_alpha_3528": {
        "path": OUT / "P8_Y5_R2FR_3528_CALIBRATED_ALPHA_CONTRACT.csv",
        "role": "calibrated alpha contract",
    },
    "product_bounds_3546": {
        "path": OUT / "P8_Y5_R2FR_3546_PRODUCT_BOUND_ROWS.csv",
        "role": "finite alpha product bound rows",
    },
    "local_gr_status_3531": {
        "path": OUT / "P8_local_GR_Hilbert_source_denominator_status.csv",
        "role": "local GR Hilbert source denominator status",
    },
    "ellj_law_3513": {
        "path": OUT / "P8_EM_ellJ_source_current_owner_residual_law.csv",
        "role": "source-current denominator residual law",
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


def certificate_rows() -> list[dict[str, Any]]:
    return [
        {
            "clause_id": "CERT3548_0_parent_object_language",
            "certificate_clause": "parent action domain is fixed before readout/fitting",
            "formal_requirement": "S_parent object language declares fields, coefficient sorts, allowed constructors and readout order",
            "would_forbid": "post-hoc hidden-visible coefficient closures",
            "current_status": "MISSING_PARENT_SIGNATURE",
            "evidence_path": str(SOURCES["signature_1319"]["path"]),
            "verdict": "NOT_SIGNED",
            "valid_for_claim": "False",
        },
        {
            "clause_id": "CERT3548_1_visible_coefficient_domain",
            "certificate_clause": "visible coefficient slots exclude hidden/local representative arguments",
            "formal_requirement": "Arg(Coeff(F_Q^2)) and Arg(Coeff(A.J)) subset {q_obs, fixed representation data, topological/level constants}",
            "would_forbid": "f_X(Phi)F_Q^2 and c_X(Phi)A.J",
            "current_status": "EXACT_CONDITIONAL_NOT_PARENT_SIGNED",
            "evidence_path": str(SOURCES["operator_domain_2659"]["path"]),
            "verdict": "POWERFUL_BUT_UNSIGNED",
            "valid_for_claim": "False",
        },
        {
            "clause_id": "CERT3548_2_no_extension_marker",
            "certificate_clause": "no hidden invariant, domain selector or material marker can be retyped as coefficient data",
            "formal_requirement": "no extension functor C_hid -> Coeff_vis and no marker labels enter visible coefficients",
            "would_forbid": "renamed scalar or source marker leakage into alpha/source coupling",
            "current_status": "NO_EXTENSION_MARKER_PROOF_MISSING",
            "evidence_path": str(SOURCES["typed_requirements_1235"]["path"]),
            "verdict": "UNSIGNED",
            "valid_for_claim": "False",
        },
        {
            "clause_id": "CERT3548_3_unique_curvature_norm",
            "certificate_clause": "the EM kinetic term is inherited from one parent curvature norm",
            "formal_requirement": "no independent visible lambda_A F_Q^2 counterterm in addition to hidden-visible no-Hom",
            "would_forbid": "constant or visible Maxwell normalization counterterm being mistaken for a derived alpha",
            "current_status": "UNIQUE_CURVATURE_NORM_NOT_DERIVED",
            "evidence_path": str(SOURCES["unique_f2_attempt_1235"]["path"]),
            "verdict": "UNSIGNED",
            "valid_for_claim": "False",
        },
        {
            "clause_id": "CERT3548_4_same_current_owner",
            "certificate_clause": "A.J current normalization is owned by the same parent generator/current before readout",
            "formal_requirement": "J_Q = delta S_matter/delta A_Q with fixed representation weights and no c_X(Phi) prefactor",
            "would_forbid": "current-prefactor branch z_g != 0",
            "current_status": "SAME_CURRENT_OWNER_NOT_PARENT_SIGNED",
            "evidence_path": str(SOURCES["same_owner_3547"]["path"]),
            "verdict": "UNSIGNED",
            "valid_for_claim": "False",
        },
        {
            "clause_id": "CERT3548_5_readout_radiative_closure",
            "certificate_clause": "EFT, clocks, material response and lab readout preserve the same coefficient domain",
            "formal_requirement": "S_eff and observable maps stay in Alg[q_obs, fixed representation data, level constants]",
            "would_forbid": "readout-regenerated alpha/source coupling after a bare action theorem",
            "current_status": "READOUT_RADIATIVE_CLOSURE_UNSIGNED",
            "evidence_path": str(SOURCES["signature_1319"]["path"]),
            "verdict": "UNSIGNED_CRITICAL",
            "valid_for_claim": "False",
        },
    ]


def slot_verdict_rows() -> list[dict[str, Any]]:
    return [
        {
            "slot_id": "SLOT3548_0_hidden_F2",
            "operator_slot": "Coeff(F_Q^2)",
            "dangerous_term": "f_X(Phi) F_Q^2",
            "conditional_typing_result": "ill-typed if CERT3548_0,1,2,5 are signed",
            "current_result": "RETAINED_COUNTERMODEL",
            "reason": "ordinary covariance and U(1) gauge invariance allow scalar gauge-kinetic functions unless parent typing forbids the coefficient argument",
            "route": "finite alpha product bound or parent certificate",
            "valid_for_claim": "False",
        },
        {
            "slot_id": "SLOT3548_1_visible_lambda",
            "operator_slot": "Coeff(F_Q^2)",
            "dangerous_term": "lambda_A F_Q^2 as independent visible counterterm",
            "conditional_typing_result": "not killed by no-Hom alone; requires unique parent curvature norm",
            "current_result": "RETAINED_CALIBRATED_CONSTANT_BRANCH",
            "reason": "a hidden-independent lambda_0 is alpha calibration debt, not alpha drift, but it is still not a derived alpha value",
            "route": "calibrated alpha baseline; no derived-alpha claim",
            "valid_for_claim": "False",
        },
        {
            "slot_id": "SLOT3548_2_current_prefactor",
            "operator_slot": "Coeff(A.J)",
            "dangerous_term": "c_X(Phi) A_mu J^mu",
            "conditional_typing_result": "ill-typed if same current owner and no source/current prefactor grammar are signed",
            "current_result": "RETAINED_COUNTERMODEL",
            "reason": "the F2 no-Hom proof does not by itself own current normalization or representation weights",
            "route": "source-current owner theorem or finite source-normalization bound",
            "valid_for_claim": "False",
        },
        {
            "slot_id": "SLOT3548_3_readout_F2",
            "operator_slot": "Coeff(S_eff/readout F_Q^2)",
            "dangerous_term": "f_eff(Phi) F_Q^2 after loop/readout reduction",
            "conditional_typing_result": "excluded only if radiative/readout closure preserves the typed domain",
            "current_result": "RETAINED_COUNTERMODEL",
            "reason": "bare action typing cannot automatically transfer to clocks, WEP, R10 or local source readouts",
            "route": "direct observable bound rows or readout theorem",
            "valid_for_claim": "False",
        },
    ]


def demotion_rows() -> list[dict[str, Any]]:
    return [
        {
            "demotion_id": "DEM3548_0_noHom_route",
            "route": "typed EM coefficient-domain no-Hom theorem",
            "decision": "DEMOTE_TO_CONDITIONAL_CONTRACT",
            "because": "the theorem is exact if the grammar is signed, but current evidence repeatedly shows the parent signature is not derived",
            "allowed_use": "private discipline contract and future proof target",
            "forbidden_use": "b_alpha=0, C_XF2=0, or local-GR source coupling claim",
            "reopen_condition": "source-backed parent object-language certificate signs CERT3548_0 through CERT3548_5",
            "valid_for_claim": "False",
        },
        {
            "demotion_id": "DEM3548_1_alpha_baseline",
            "route": "local alpha in baseline Maxwell stress",
            "decision": "CALIBRATED_CLOSURE_ALLOWED",
            "because": "measured alpha_0 can play the same local-effective-theory role as measured G_N, provided it is labelled as calibration",
            "allowed_use": "compute Maxwell stress and Poynting/Hilbert bookkeeping in the baseline local branch",
            "forbidden_use": "derived-alpha public claim or cancellation of active source residuals",
            "reopen_condition": "same-owner/unique-F2/no-Hom/readout theorem is parent-signed",
            "valid_for_claim": "False",
        },
        {
            "demotion_id": "DEM3548_2_active_alpha_branch",
            "route": "nonzero alpha/source coupling branch",
            "decision": "FINITE_BOUND_BRANCH_ONLY",
            "because": "f_X(Phi)F_Q^2 and c_X(Phi)A.J remain live countermodels",
            "allowed_use": f"score future sourced products against {DD_E_CEILING:.6e} or {ALPHA_COULOMB_CEILING:.6e} gates",
            "forbidden_use": "placeholder K_e_alpha*b_alpha or bound inversion as MTS prediction",
            "reopen_condition": "numeric parent b_alpha/K_e_alpha value or theorem-zero plus sourced projection",
            "valid_for_claim": "False",
        },
        {
            "demotion_id": "DEM3548_3_project_spine",
            "route": "main local GR/Newton source-coupling spine",
            "decision": "RETURN_TO_HILBERT_SOURCE_DENOMINATOR",
            "because": "alpha is now quarantined and no longer needs to block the source-current/Poisson/PPN bridge",
            "allowed_use": "continue with Pi_M/H_tau/ell_J/source denominator derivation",
            "forbidden_use": "using alpha no-Hom failure as a reason to stop local GR/Newton work",
            "reopen_condition": "none; proceed now",
            "valid_for_claim": "False",
        },
    ]


def source_coupling_handoff_rows() -> list[dict[str, Any]]:
    return [
        {
            "handoff_id": "HAND3548_0_alpha",
            "sector": "Maxwell/alpha",
            "current_state": "calibrated baseline plus finite active-branch bounds",
            "next_owner": "only revisit if parent coefficient-domain certificate or numeric product appears",
            "local_gr_relevance": "baseline Maxwell stress is usable conditionally; alpha theorem-zero is not required for next Newton bridge step",
            "valid_for_claim": "False",
        },
        {
            "handoff_id": "HAND3548_1_source_current",
            "sector": "Hilbert source denominator",
            "current_state": "z_ellJ exact decomposition exists but Pi_M/H_tau owner remains open",
            "next_owner": "R_PiM + R_Htau source-current square residual",
            "local_gr_relevance": "this is the direct route to calibrated Newtonian source mass and PPN residuals",
            "valid_for_claim": "False",
        },
        {
            "handoff_id": "HAND3548_2_poynting",
            "sector": "EM stress/Poynting",
            "current_state": "static bound EM stress belongs in T_total; exterior radiative flux remains a source/time-hair residual",
            "next_owner": "source-current flux closure and Gdot/clock bound rows if nonzero",
            "local_gr_relevance": "Poynting should police source conservation, not substitute for alpha no-Hom proof",
            "valid_for_claim": "False",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3548_0_certificate",
            "question": "Does the current corpus prove the typed EM no-Hom certificate?",
            "decision": "NO",
            "basis": "2659/1235/1319 all preserve the exact conditional theorem but record missing parent signature, unique curvature norm, no-extension and readout clauses",
            "consequence": "do not claim b_alpha=0 or C_XF2=0 from this route",
            "valid_for_claim": "False",
        },
        {
            "decision_id": "DEC3548_1_alpha_policy",
            "question": "Can alpha be used in the local framework without finishing the parent derivation?",
            "decision": "YES_AS_CALIBRATED_BASELINE_ONLY",
            "basis": "3528 calibrated alpha contract already separates measured alpha_0 from active residual branches",
            "consequence": "Maxwell stress/Poynting bookkeeping can proceed while active alpha branches remain bounded",
            "valid_for_claim": "False",
        },
        {
            "decision_id": "DEC3548_2_next_route",
            "question": "What is the best next move for the full goal?",
            "decision": "RETURN_TO_HILBERT_SOURCE_DENOMINATOR",
            "basis": "local GR/Newton depends most directly on M_H/Pi_M/H_tau/source-current closure, not on deriving alpha's numerical value",
            "consequence": "3549 targets the Pi_M/H_tau Newton bridge rather than another alpha loop",
            "valid_for_claim": "False",
        },
    ]


def status_rows() -> list[dict[str, Any]]:
    return [
        {
            "status_id": "STATUS3548_0",
            "checkpoint": "3548",
            "claim_allowed": "False",
            "typed_noHom_certificate": "not_parent_signed",
            "alpha_route": "calibrated_closure_plus_finite_bound_branch",
            "finite_dd_e_gate": f"{DD_E_CEILING:.12e}",
            "finite_alpha_coulomb_gate": f"{ALPHA_COULOMB_CEILING:.12e}",
            "project_spine_next": "Hilbert_source_denominator_PiM_Htau_Newton_bridge",
            "next_target": "3549-Y5-R2FR-Hilbert-source-denominator-PiM-Htau-local-Newton-bridge.md",
            "valid_for_claim": "False",
        }
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT3548_0",
            "target_doc": "3549-Y5-R2FR-Hilbert-source-denominator-PiM-Htau-local-Newton-bridge.md",
            "target_script": "scripts/Y5_R2FR_3549_Hilbert_source_denominator_PiM_Htau_local_Newton_bridge.py",
            "objective": "derive or bound the Pi_M/H_tau/H_ref source denominator bridge needed for Poisson/Newton and PPN source calibration, with alpha now quarantined as calibrated baseline plus finite active branch",
            "success_gate": "either R_PiM+R_Htau is reduced to parent-owned zero clauses, or each denominator residual gets a finite local bound row and no local-GR/Newton claim is made",
            "reason": "this resumes the main GR/Newton route instead of looping around alpha coefficient-domain closure",
            "valid_for_claim": "False",
        }
    ]


def validation_rows(
    generated_paths: list[Path],
    sources: list[dict[str, Any]],
    certificate: list[dict[str, Any]],
    demotion: list[dict[str, Any]],
    slot_verdicts: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    required_sources_exist = all(row["exists"] == "True" for row in sources)
    generated_csvs = [path for path in generated_paths if path.suffix.lower() == ".csv"]
    csvs_parse = all(csv_parse_ok(path) for path in generated_csvs)
    certificate_not_signed = all(row["verdict"] != "SIGNED" and row["valid_for_claim"] == "False" for row in certificate)
    demotion_nonclaim = all(row["valid_for_claim"] == "False" for row in demotion)
    slot_countermodels_retained = all(row["current_result"] != "PROVEN_ZERO" for row in slot_verdicts)
    no_formalization_outputs = all(FORMALIZATION not in path.parents for path in generated_paths)
    return [
        {
            "validation_id": "VAL3548_0_sources_exist",
            "passes": bool_text(required_sources_exist),
            "status": "PASS" if required_sources_exist else "FAIL",
            "detail": "all cited 3548 source paths exist",
        },
        {
            "validation_id": "VAL3548_1_generated_csvs_parse",
            "passes": bool_text(csvs_parse),
            "status": "PASS" if csvs_parse else "FAIL",
            "detail": f"{len(generated_csvs)} generated CSV files parse with DictReader",
        },
        {
            "validation_id": "VAL3548_2_certificate_not_signed",
            "passes": bool_text(certificate_not_signed),
            "status": "PASS" if certificate_not_signed else "FAIL",
            "detail": "no typed no-Hom certificate clause is promoted as signed",
        },
        {
            "validation_id": "VAL3548_3_demotion_nonclaim",
            "passes": bool_text(demotion_nonclaim),
            "status": "PASS" if demotion_nonclaim else "FAIL",
            "detail": "alpha/no-Hom demotion rows remain nonclaim",
        },
        {
            "validation_id": "VAL3548_4_countermodels_retained",
            "passes": bool_text(slot_countermodels_retained),
            "status": "PASS" if slot_countermodels_retained else "FAIL",
            "detail": "F2, current-prefactor and readout slot countermodels are not silently erased",
        },
        {
            "validation_id": "VAL3548_5_formalization_workbench_untouched",
            "passes": bool_text(no_formalization_outputs),
            "status": "PASS" if no_formalization_outputs else "FAIL",
            "detail": "3548 generated outputs only inside post-checkpoint-work",
        },
    ]


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    lines = [
        "# 3548 — Typed EM coefficient-domain no-Hom certificate or alpha closure demotion",
        "",
        "## Verdict",
        "",
        "- **The no-Hom theorem is exact but not parent-signed.** If the parent object-language really restricts visible coefficients to `q_obs`, fixed representation data and topological/level constants, then `f_X(Phi)F_Q^2` and `c_X(Phi)A.J` are untypeable.",
        "- **The current corpus does not prove that restriction.** Existing audits repeatedly keep the parent signature, unique curvature norm, no-extension rule and readout/radiative closure unsigned.",
        "- **Alpha is therefore demoted to disciplined closure:** use measured `alpha_0` for baseline local Maxwell stress, and keep any active nonzero alpha/source branch behind the finite gates.",
        "- **Main spine resumes at source calibration:** local GR/Newton should now attack the Hilbert source denominator, especially `R_PiM + R_Htau`, rather than looping around alpha.",
        "",
        "## Certificate Clauses",
        "",
        markdown_table(
            rows_by_name["certificate"],
            ["clause_id", "certificate_clause", "formal_requirement", "would_forbid", "verdict"],
        ),
        "",
        "## Slot Verdicts",
        "",
        markdown_table(
            rows_by_name["slot_verdicts"],
            ["slot_id", "operator_slot", "dangerous_term", "conditional_typing_result", "current_result", "route"],
        ),
        "",
        "## Demotion Ledger",
        "",
        markdown_table(
            rows_by_name["demotion"],
            ["demotion_id", "route", "decision", "because", "allowed_use", "forbidden_use"],
        ),
        "",
        "## Source-Coupling Handoff",
        "",
        markdown_table(
            rows_by_name["handoff"],
            ["handoff_id", "sector", "current_state", "next_owner", "local_gr_relevance"],
        ),
        "",
        "## Decisions",
        "",
        markdown_table(
            rows_by_name["decision"],
            ["decision_id", "question", "decision", "basis", "consequence"],
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
        "Move to `3549-Y5-R2FR-Hilbert-source-denominator-PiM-Htau-local-Newton-bridge.md`. The aim is to derive or bound the source denominator bridge behind Newton/Poisson/PPN: `M_H_ref`, `Pi_M`, `H_tau`, `H_ref`, and the residual `R_PiM+R_Htau`.",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
    ]
    DOC.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)

    sources = source_rows()
    certificate = certificate_rows()
    slot_verdicts = slot_verdict_rows()
    demotion = demotion_rows()
    handoff = source_coupling_handoff_rows()
    decisions = decision_rows()
    status = status_rows()
    next_target = next_target_rows()

    outputs: dict[Path, tuple[list[dict[str, Any]], list[str]]] = {
        OUT / "P8_Y5_R2FR_3548_SOURCE_REGISTER.csv": (
            sources,
            ["source_id", "path", "exists", "role", "valid_for_claim"],
        ),
        OUT / "P8_Y5_R2FR_3548_TYPED_EM_CERTIFICATE_CLAUSES.csv": (
            certificate,
            [
                "clause_id",
                "certificate_clause",
                "formal_requirement",
                "would_forbid",
                "current_status",
                "evidence_path",
                "verdict",
                "valid_for_claim",
            ],
        ),
        OUT / "P8_Y5_R2FR_3548_EM_SLOT_VERDICTS.csv": (
            slot_verdicts,
            [
                "slot_id",
                "operator_slot",
                "dangerous_term",
                "conditional_typing_result",
                "current_result",
                "reason",
                "route",
                "valid_for_claim",
            ],
        ),
        OUT / "P8_Y5_R2FR_3548_ALPHA_CLOSURE_DEMOTION.csv": (
            demotion,
            [
                "demotion_id",
                "route",
                "decision",
                "because",
                "allowed_use",
                "forbidden_use",
                "reopen_condition",
                "valid_for_claim",
            ],
        ),
        OUT / "P8_Y5_R2FR_3548_SOURCE_COUPLING_HANDOFF.csv": (
            handoff,
            ["handoff_id", "sector", "current_state", "next_owner", "local_gr_relevance", "valid_for_claim"],
        ),
        OUT / "P8_Y5_R2FR_3548_DECISION_LEDGER.csv": (
            decisions,
            ["decision_id", "question", "decision", "basis", "consequence", "valid_for_claim"],
        ),
        OUT / "P8_Y5_R2FR_3548_STATUS.csv": (
            status,
            [
                "status_id",
                "checkpoint",
                "claim_allowed",
                "typed_noHom_certificate",
                "alpha_route",
                "finite_dd_e_gate",
                "finite_alpha_coulomb_gate",
                "project_spine_next",
                "next_target",
                "valid_for_claim",
            ],
        ),
        OUT / "P8_Y5_R2FR_3548_NEXT_TARGET.csv": (
            next_target,
            ["next_id", "target_doc", "target_script", "objective", "success_gate", "reason", "valid_for_claim"],
        ),
        CANONICAL_STATUS: (
            status,
            [
                "status_id",
                "checkpoint",
                "claim_allowed",
                "typed_noHom_certificate",
                "alpha_route",
                "finite_dd_e_gate",
                "finite_alpha_coulomb_gate",
                "project_spine_next",
                "next_target",
                "valid_for_claim",
            ],
        ),
    }

    generated_paths: list[Path] = []
    for path, (rows, fields) in outputs.items():
        write_csv(path, rows, fields)
        generated_paths.append(path)

    validation = validation_rows(generated_paths, sources, certificate, demotion, slot_verdicts)
    validation_path = OUT / "P8_Y5_BRR545_3548_VALIDATION.csv"
    write_csv(
        validation_path,
        validation,
        ["validation_id", "passes", "status", "detail"],
    )
    generated_paths.append(validation_path)

    write_doc(
        {
            "certificate": certificate,
            "slot_verdicts": slot_verdicts,
            "demotion": demotion,
            "handoff": handoff,
            "decision": decisions,
            "status": status,
            "validation": validation,
            "next_target": next_target,
        }
    )

    print(f"wrote {DOC}")
    for path in generated_paths:
        print(f"wrote {path}")


if __name__ == "__main__":
    main()
