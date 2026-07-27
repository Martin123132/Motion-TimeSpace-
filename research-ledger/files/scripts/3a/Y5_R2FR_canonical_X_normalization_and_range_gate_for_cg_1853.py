from __future__ import annotations

import csv
import math
import shutil
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = ROOT.parent
FORMALIZATION = PROJECT_ROOT / "formalization-workbench"
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE = ROOT / "source-intake" / "microscope"
MICROSCOPE_RESIDUALS = MICROSCOPE / "branch_locked_wep" / "residuals"
QUARANTINE = MICROSCOPE / "quarantine" / "1853"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"

BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC_PATH = ROOT / "1853-Y5-R2FR-canonical-X-normalization-and-range-gate-for-cg.md"

ALPHA_PPN_PROXY = 0.005788015401465051
GAMMA_BOUND = 6.7e-5


OUTPUTS = {
    "source_register": RESIDUALS / "P8_Y5_PARENT_QLOC_1853_SOURCE_REGISTER.csv",
    "canonical_derivation": RESIDUALS / "P8_Y5_PARENT_QLOC_1853_CANONICAL_X_NORMALIZATION_DERIVATION.csv",
    "range_derivation": RESIDUALS / "P8_Y5_PARENT_QLOC_1853_RANGE_TRANSFER_DERIVATION.csv",
    "input_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_1853_ZX_MX2_INPUT_GATE.csv",
    "cg_bound": RESIDUALS / "P8_Y5_PARENT_QLOC_1853_CG_NORMALIZED_BOUND_ROW.csv",
    "range_classifier": RESIDUALS / "P8_Y5_PARENT_QLOC_1853_RANGE_BRANCH_CLASSIFIER.csv",
    "claim_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_1853_CLAIM_GATE.csv",
    "decision": RESIDUALS / "P8_Y5_PARENT_QLOC_1853_DECISION_LEDGER.csv",
    "next_target": RESIDUALS / "P8_Y5_PARENT_QLOC_1853_NEXT_TARGET.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_1853_VALIDATION.csv",
}


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")


def source_path(relative_path: str) -> str:
    return rel(ROOT / relative_path)


def ensure_dirs() -> None:
    for path in [RESIDUALS, MICROSCOPE_RESIDUALS, QUARANTINE, RAB_QUEUE]:
        path.mkdir(parents=True, exist_ok=True)


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def boolish(value: Any) -> bool:
    return str(value).strip().lower() == "true"


def build_rows_map() -> dict[str, list[dict[str, Any]]]:
    source_rows = [
        {
            "source_id": "SRC1853_0_1852_handoff",
            "source_path": source_path("1852-Y5-R2FR-PPN-common-frame-cg-translation-gate.md"),
            "needle": "NEXT1852_0_primary",
            "use": "selected canonical X normalization and range target",
            "status": "FOUND",
            "valid_for_claim": False,
        },
        {
            "source_id": "SRC1853_1_1852_cg_bound",
            "source_path": source_path("source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1852_CG_CONDITIONAL_BOUND_ROW.csv"),
            "needle": "CGB1852_1_cg_conditional",
            "use": "c_g conditional bound formula needing N_X and tau_PPN",
            "status": "FOUND",
            "valid_for_claim": False,
        },
        {
            "source_id": "SRC1853_2_1847_second_variation",
            "source_path": source_path("source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1847_SECOND_VARIATION_DERIVATION.csv"),
            "needle": "SV1847_3_range_relation",
            "use": "parent second-variation law and lambda_X=sqrt(Z_X/M_X^2)",
            "status": "FOUND",
            "valid_for_claim": False,
        },
        {
            "source_id": "SRC1853_3_1847_hessian_audit",
            "source_path": source_path("source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1847_PARENT_HESSIAN_AUDIT.csv"),
            "needle": "PHA1847_8_verdict",
            "use": "Hessian ownership remains blocked",
            "status": "FOUND",
            "valid_for_claim": False,
        },
        {
            "source_id": "SRC1853_4_1848_metric_lock",
            "source_path": source_path("1848-Y5-R2FR-parent-metric-ZXfX2-beta-eigenvalue-or-source-zero-return.md"),
            "needle": "parent metric lock",
            "use": "field-space metric / finite route remains unowned",
            "status": "FOUND",
            "valid_for_claim": False,
        },
        {
            "source_id": "SRC1853_5_1085_thresholds",
            "source_path": source_path("source-intake/mts_residuals/P8_Y5_R10_1085_LONG_RANGE_THRESHOLD_TABLE.csv"),
            "needle": "LRT1085_lambda_over_RE_1000",
            "use": "existing long-range threshold table",
            "status": "FOUND",
            "valid_for_claim": False,
        },
        {
            "source_id": "SRC1853_6_1085_schema",
            "source_path": source_path("source-intake/mts_residuals/P8_Y5_R10_1085_RANGE_ACQUISITION_SCHEMA.csv"),
            "needle": "RAS1085_0_parent_operator",
            "use": "range acquisition schema",
            "status": "FOUND",
            "valid_for_claim": False,
        },
        {
            "source_id": "SRC1853_7_1633_finite_range",
            "source_path": source_path("source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1633_FINITE_RANGE_DECISION.csv"),
            "needle": "FR1633_1_missing_range",
            "use": "finite range owner still missing in current parent notes",
            "status": "FOUND",
            "valid_for_claim": False,
        },
    ]

    canonical_rows = [
        {
            "step_id": "CN1853_0_parent_quadratic_block",
            "statement": "Use the parent-owned local quadratic Xhat block from the 1847 second-variation contract.",
            "equation": "S_X^(2)=1/2 int sqrt(-g_E) M_Pl^2 [ Z_X g_E^{mu nu} partial_mu Xhat partial_nu Xhat + M_X^2 Xhat^2 ]",
            "derived_object": "operator O_X=-Z_X Box_E + M_X^2 under constant-coefficient local approximation",
            "status": "CONDITIONAL_ON_PARENT_BLOCK",
            "missing_for_claim": "current branch has not parent-signed Xhat, Z_X, M_X^2, units, cross-Hessian silence or source current",
            "valid_for_claim": False,
        },
        {
            "step_id": "CN1853_1_canonical_field",
            "statement": "For positive constant Z_X in the same branch, define the canonical scalar.",
            "equation": "varphi = M_Pl sqrt(Z_X) Xhat",
            "derived_object": "dXhat/d(varphi/M_Pl)=1/sqrt(Z_X)",
            "status": "EXACT_CONDITIONAL_NORMALIZATION_LAW",
            "missing_for_claim": "Z_X positivity, units and parent normalization are not owned",
            "valid_for_claim": False,
        },
        {
            "step_id": "CN1853_2_NX_definition",
            "statement": "The PPN coupling sees canonical field units, not the arbitrary Xhat coordinate.",
            "equation": "N_X := dXhat/d(varphi/M_Pl)=1/sqrt(Z_X)",
            "derived_object": "alpha_PPN = tau_PPN N_X c_g for a pure common conformal frame",
            "status": "DERIVED_CONDITIONAL_MAP",
            "missing_for_claim": "tau_PPN and Z_X remain missing",
            "valid_for_claim": False,
        },
        {
            "step_id": "CN1853_3_rescaling_guard",
            "statement": "Field redefinitions cannot be used to win Cassini by notation.",
            "equation": "Xhat -> a Xhat gives c_g -> c_g/a and Z_X -> Z_X/a^2, so c_g/sqrt(Z_X) is invariant",
            "derived_object": "only alpha_eff=tau_PPN c_g/sqrt(Z_X) can be compared to Cassini",
            "status": "GUARDRAIL_ACTIVE",
            "missing_for_claim": "still needs actual Z_X and tau_PPN values",
            "valid_for_claim": False,
        },
        {
            "step_id": "CN1853_4_verdict",
            "statement": "Canonical normalization is mathematically fixed, but not numerically owned.",
            "equation": "|tau_PPN c_g/sqrt(Z_X)| <= alpha_PPN_proxy",
            "derived_object": "claim-grade c_g bound requires parent-signed Z_X and tau_PPN",
            "status": "FORMULA_DERIVED_INPUTS_MISSING",
            "missing_for_claim": "MISSING_ZX;MISSING_TAU_PPN",
            "valid_for_claim": False,
        },
    ]

    range_rows = [
        {
            "step_id": "RG1853_0_mass_ratio",
            "statement": "The same parent Hessian that fixes normalization fixes range.",
            "equation": "mu_X^2 = M_X^2/Z_X",
            "derived_object": "canonical static mass scale",
            "status": "EXACT_CONDITIONAL_RANGE_LAW",
            "missing_for_claim": "M_X^2 and Z_X are not parent-signed in the same normalization",
            "valid_for_claim": False,
        },
        {
            "step_id": "RG1853_1_lambda_relation",
            "statement": "The static range follows from the canonical mass.",
            "equation": "lambda_X = 1/mu_X = sqrt(Z_X/M_X^2) in c=hbar=1 units",
            "derived_object": "finite-range classifier input",
            "status": "EXACT_CONDITIONAL_RANGE_LAW",
            "missing_for_claim": "units and conversion to metres require sourced Z_X/M_X^2 dimensions",
            "valid_for_claim": False,
        },
        {
            "step_id": "RG1853_2_ppn_transfer",
            "statement": "Cassini constrains the effective long-range charge after range and screening transfer.",
            "equation": "alpha_eff_PPN(lambda_X)=tau_PPN c_g/sqrt(Z_X) * S_PPN(lambda_X, environment)",
            "derived_object": "abs(alpha_eff_PPN)<=alpha_PPN_proxy",
            "status": "TRANSFER_FORMULA_READY",
            "missing_for_claim": "S_PPN, lambda_X and screening/environment map are missing",
            "valid_for_claim": False,
        },
        {
            "step_id": "RG1853_3_short_range_branch",
            "statement": "If lambda_X is laboratory-short, Cassini is suppressed and R10/short-range Yukawa bounds become the relevant arena.",
            "equation": "lambda_X ~ micrometer-to-millimeter -> use alpha_R10(lambda), not unsuppressed PPN gamma",
            "derived_object": "R10 routing gate",
            "status": "ROUTE_CONDITIONAL_ON_LAMBDA",
            "missing_for_claim": "lambda_X not owned",
            "valid_for_claim": False,
        },
        {
            "step_id": "RG1853_4_long_range_branch",
            "statement": "If lambda_X is solar-system long-range and unscreened, Cassini is the harshest clean c_g proxy.",
            "equation": "lambda_X >> solar-system impact scale and S_PPN≈1",
            "derived_object": "PPN routing gate",
            "status": "ROUTE_CONDITIONAL_ON_LAMBDA",
            "missing_for_claim": "long-range certificate not derived",
            "valid_for_claim": False,
        },
        {
            "step_id": "RG1853_5_verdict",
            "statement": "Range law is exact conditionally, but current branch remains unclassified.",
            "equation": "range_class = unknown until Z_X and M_X^2 are sourced",
            "derived_object": "no PPN/R10/local-GR claim from range yet",
            "status": "RANGE_INPUTS_MISSING",
            "missing_for_claim": "MISSING_ZX;MISSING_MX2;MISSING_RANGE_TRANSFER",
            "valid_for_claim": False,
        },
    ]

    input_rows = [
        {
            "gate_id": "ZMG1853_0_Xhat_owner",
            "needed_input": "same parent Xhat owns c_g, Z_X, M_X^2 and source current",
            "current_status": "NOT_PARENT_SIGNED",
            "blocks": "prevents comparing c_g to Cassini/R10",
            "next_evidence": "single parent action clause with normalized Xhat",
            "gate_pass": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "ZMG1853_1_ZX_positive",
            "needed_input": "Z_X>0 with units and same field normalization",
            "current_status": "MISSING_ZX",
            "blocks": "prevents N_X=1/sqrt(Z_X) numeric bound",
            "next_evidence": "parent Hessian kinetic coefficient row",
            "gate_pass": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "ZMG1853_2_MX2_positive_or_zero",
            "needed_input": "M_X^2>=0 or a signed massless theorem",
            "current_status": "MISSING_MX2",
            "blocks": "prevents lambda_X/range classification",
            "next_evidence": "parent Hessian mass/eigenvalue row",
            "gate_pass": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "ZMG1853_3_cross_Hessian_silence",
            "needed_input": "mixed Hessian/cross-sector terms are zero or included in tau_PPN vector",
            "current_status": "MISSING_CROSS_HESSIAN_BLOCK",
            "blocks": "prevents one-field c_g PPN bound",
            "next_evidence": "block diagonalization theorem or residual-vector rows",
            "gate_pass": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "ZMG1853_4_range_transfer",
            "needed_input": "S_PPN(lambda_X, environment) or long-range certificate",
            "current_status": "MISSING_RANGE_TRANSFER",
            "blocks": "prevents deciding Cassini vs R10 vs orbital arena",
            "next_evidence": "lambda_X in metres and screening/local-environment map",
            "gate_pass": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "ZMG1853_5_verdict",
            "needed_input": "all Z_X/M_X^2/N_X/range gates pass simultaneously",
            "current_status": "FAIL_CURRENT_CLAIM",
            "blocks": "no direct c_g component bound and no local-GR PPN pass",
            "next_evidence": "1854 parent Hessian input extraction",
            "gate_pass": False,
            "valid_for_claim": False,
        },
    ]

    cg_rows = [
        {
            "bound_id": "NGB1853_0_alpha_proxy_input",
            "quantity": "alpha_PPN_proxy",
            "formula": "sqrt(delta_gamma/(2-delta_gamma)) from 1852",
            "numeric_bound": ALPHA_PPN_PROXY,
            "units": "dimensionless",
            "status": "SOURCE_BACKED_PROXY",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "bound_id": "NGB1853_1_normalized_effective_coupling",
            "quantity": "alpha_eff_PPN",
            "formula": "alpha_eff_PPN = tau_PPN c_g S_PPN(lambda_X,env)/sqrt(Z_X)",
            "numeric_bound": f"abs(alpha_eff_PPN)<={ALPHA_PPN_PROXY}",
            "units": "dimensionless",
            "status": "CONDITIONAL_EFFECTIVE_BOUND",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "bound_id": "NGB1853_2_cg_formula",
            "quantity": "c_g",
            "formula": "abs(c_g) <= alpha_PPN_proxy*sqrt(Z_X)/(abs(tau_PPN)*abs(S_PPN))",
            "numeric_bound": "MISSING_ZX_TAU_PPN_RANGE_TRANSFER",
            "units": "dimensionless_per_Xhat",
            "status": "FORMULA_READY_COMPONENT_BOUND_MISSING",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "bound_id": "NGB1853_3_rescaling_invariant",
            "quantity": "c_g/sqrt(Z_X)",
            "formula": "invariant under Xhat->aXhat",
            "numeric_bound": f"MISSING_TAU_PPN_RANGE_TRANSFER; proxy ceiling {ALPHA_PPN_PROXY}",
            "units": "dimensionless",
            "status": "INVARIANT_IDENTIFIED_NOT_NUMERIC",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]

    classifier_rows = [
        {
            "class_id": "RBC1853_0_massless_or_solar_long",
            "condition": "M_X^2=0 or lambda_X much larger than solar-system PPN impact scale and S_PPN≈1",
            "dominant_test": "Cassini/PPN plus orbital",
            "allowed_bound_use": "alpha_eff_PPN proxy can constrain c_g/sqrt(Z_X)",
            "current_status": "NOT_CLASSIFIED",
            "valid_for_claim": False,
        },
        {
            "class_id": "RBC1853_1_lab_short",
            "condition": "lambda_X in micrometer-to-millimeter band",
            "dominant_test": "Eot-Wash/R10 Yukawa alpha(lambda)",
            "allowed_bound_use": "R10 bound curve needed; Cassini likely suppressed",
            "current_status": "NOT_CLASSIFIED",
            "valid_for_claim": False,
        },
        {
            "class_id": "RBC1853_2_earth_or_orbital",
            "condition": "lambda_X comparable to Earth radius, Earth-Moon, AU or source-support scales",
            "dominant_test": "WEP/orbital/LLR/PPN transfer matrix",
            "allowed_bound_use": "must use finite-range source geometry, not point proxy",
            "current_status": "NOT_CLASSIFIED",
            "valid_for_claim": False,
        },
        {
            "class_id": "RBC1853_3_screened_or_plateau",
            "condition": "local nonlinear screening or plateau suppresses effective charge",
            "dominant_test": "screening-profile derivation plus lab/solar-system split",
            "allowed_bound_use": "only screened effective coupling is bounded until parent-to-local map closes",
            "current_status": "NOT_CLASSIFIED",
            "valid_for_claim": False,
        },
        {
            "class_id": "RBC1853_4_current_branch",
            "condition": "Z_X and M_X^2 are missing",
            "dominant_test": "none claim-grade",
            "allowed_bound_use": "record source-backed proxies only",
            "current_status": "SELECTED_CURRENT_STATUS",
            "valid_for_claim": False,
        },
    ]

    claim_rows = [
        {
            "gate_id": "CG1853_0_normalization_law",
            "claim": "canonical normalization law is derived conditionally",
            "gate_pass": True,
            "reason": "varphi=M_Pl sqrt(Z_X) Xhat and N_X=1/sqrt(Z_X) follow from the quadratic block",
            "claim_allowed": True,
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG1853_1_range_law",
            "claim": "range law is derived conditionally",
            "gate_pass": True,
            "reason": "lambda_X=sqrt(Z_X/M_X^2) follows from the static operator",
            "claim_allowed": True,
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG1853_2_numeric_ZX_MX2",
            "claim": "Z_X and M_X^2 are numeric parent-owned inputs",
            "gate_pass": False,
            "reason": "1847/1848 still block parent Hessian ownership",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG1853_3_cg_bound",
            "claim": "Cassini gives a direct MTS c_g bound",
            "gate_pass": False,
            "reason": "Z_X, tau_PPN and range transfer are missing",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG1853_4_local_GR",
            "claim": "local GR/PPN branch passes",
            "gate_pass": False,
            "reason": "range class and residual vector are not claim-grade",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]

    decision_rows = [
        {
            "decision_id": "DEC1853_0_math_result",
            "decision": "The normalization and range laws are now exact conditional contracts.",
            "because": "one quadratic parent block fixes both N_X and lambda_X; field-rescaling fake wins are blocked.",
            "next_action": "use c_g/sqrt(Z_X), not raw c_g, in all PPN comparisons",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC1853_1_current_block",
            "decision": "No numeric c_g/local-GR claim is allowed.",
            "because": "Z_X, M_X^2, tau_PPN and S_PPN(lambda) are missing or not parent-signed.",
            "next_action": "extract or reject parent Hessian inputs",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC1853_2_best_next",
            "decision": "Next target should be parent Hessian input extraction for Z_X/M_X^2.",
            "because": "without these, every PPN/R10/local range route is only a source-backed proxy.",
            "next_action": "1854-Y5-R2FR-parent-Hessian-input-extraction-for-ZX-MX2.md",
            "valid_for_claim": False,
        },
    ]

    next_rows = [
        {
            "route_id": "NEXT1853_0_primary",
            "next_target": "1854-Y5-R2FR-parent-Hessian-input-extraction-for-ZX-MX2.md",
            "script": "scripts/Y5_R2FR_parent_Hessian_input_extraction_for_ZX_MX2_1854.py",
            "objective": "try to extract parent-owned Z_X and M_X^2 from the current MTS action/spine; if absent, write the exact action clause required and keep c_g nonclaim",
            "selection_status": "selected",
            "success_condition": "Z_X/M_X^2 become source-backed inputs or the missing parent Hessian clause is stated as the next closure requirement",
        },
        {
            "route_id": "NEXT1853_1_parallel",
            "next_target": "1854b-Y5-R2FR-PPN-residual-vector-no-cancellation-envelope.md",
            "script": "scripts/Y5_R2FR_PPN_residual_vector_no_cancellation_envelope_1854b.py",
            "objective": "derive the multi-component PPN residual vector over c_g, b_dis, q_nonH, support and boundary terms",
            "selection_status": "held",
            "success_condition": "PPN constraints become a vector envelope rather than a one-parameter c_g proxy",
        },
    ]

    return {
        "source_register": source_rows,
        "canonical_derivation": canonical_rows,
        "range_derivation": range_rows,
        "input_gate": input_rows,
        "cg_bound": cg_rows,
        "range_classifier": classifier_rows,
        "claim_gate": claim_rows,
        "decision": decision_rows,
        "next_target": next_rows,
    }


def copy_outputs(include_validation: bool = False) -> None:
    keys = list(OUTPUTS)
    if not include_validation:
        keys = [key for key in keys if key != "validation"]
    for key in keys:
        src = OUTPUTS[key]
        if not src.exists():
            continue
        for dst_dir in [MICROSCOPE_RESIDUALS, QUARANTINE]:
            shutil.copy2(src, dst_dir / src.name)
        shutil.copy2(src, RAB_QUEUE / f"JR1853_{src.name}")


def check_sources(source_rows: list[dict[str, Any]]) -> tuple[bool, str]:
    missing: list[str] = []
    for row in source_rows:
        path = ROOT / str(row["source_path"])
        if not path.exists():
            missing.append(str(row["source_path"]))
    return not missing, "missing: " + "; ".join(missing) if missing else "all cited source paths exist"


def check_needles(source_rows: list[dict[str, Any]]) -> tuple[bool, str]:
    missing: list[str] = []
    for row in source_rows:
        path = ROOT / str(row["source_path"])
        needle = str(row["needle"])
        if path.exists() and needle not in path.read_text(encoding="utf-8", errors="ignore"):
            missing.append(f"{row['source_path']}::{needle}")
    return not missing, "missing: " + "; ".join(missing) if missing else "all cited source needles are present"


def check_csv_parse() -> tuple[bool, str]:
    malformed: list[str] = []
    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        try:
            read_csv(path)
        except Exception as exc:  # pragma: no cover
            malformed.append(f"{path.name}: {exc}")
    return not malformed, "malformed: " + "; ".join(malformed) if malformed else "all generated 1853 CSVs parse"


def check_branch_copies() -> tuple[bool, str]:
    missing: list[str] = []
    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        expected = [
            MICROSCOPE_RESIDUALS / path.name,
            QUARANTINE / path.name,
            RAB_QUEUE / f"JR1853_{path.name}",
        ]
        for item in expected:
            if not item.exists():
                missing.append(str(item))
    return not missing, "missing copies: " + "; ".join(missing) if missing else "branch/quarantine/queue copies exist"


def build_validation(rows_map: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    checks: list[tuple[str, bool, str]] = []
    ok, detail = check_sources(rows_map["source_register"])
    checks.append(("VAL1853_0_sources_exist", ok, detail))
    ok, detail = check_needles(rows_map["source_register"])
    checks.append(("VAL1853_1_needles_present", ok, detail))
    checks.append(
        (
            "VAL1853_2_normalization_law",
            any(row["step_id"] == "CN1853_2_NX_definition" and "1/sqrt(Z_X)" in row["equation"] for row in rows_map["canonical_derivation"]),
            "N_X normalization law is present",
        )
    )
    checks.append(
        (
            "VAL1853_3_rescaling_guard",
            any(row["step_id"] == "CN1853_3_rescaling_guard" and row["status"] == "GUARDRAIL_ACTIVE" for row in rows_map["canonical_derivation"]),
            "field-rescaling guard is active",
        )
    )
    checks.append(
        (
            "VAL1853_4_range_law",
            any(row["step_id"] == "RG1853_1_lambda_relation" and "sqrt(Z_X/M_X^2)" in row["equation"] for row in rows_map["range_derivation"]),
            "lambda_X range law is present",
        )
    )
    checks.append(
        (
            "VAL1853_5_input_gate_blocks",
            any(row["gate_id"] == "ZMG1853_5_verdict" and row["current_status"] == "FAIL_CURRENT_CLAIM" for row in rows_map["input_gate"])
            and all(not boolish(row["gate_pass"]) for row in rows_map["input_gate"]),
            "Z_X/M_X^2 input gates block current claim",
        )
    )
    checks.append(
        (
            "VAL1853_6_cg_bound_nonclaim",
            any(row["bound_id"] == "NGB1853_2_cg_formula" and row["numeric_bound"] == "MISSING_ZX_TAU_PPN_RANGE_TRANSFER" for row in rows_map["cg_bound"])
            and all(not boolish(row["claim_allowed"]) for row in rows_map["cg_bound"]),
            "c_g normalized bound is formula-only and nonclaim",
        )
    )
    checks.append(
        (
            "VAL1853_7_range_classifier_current",
            any(row["class_id"] == "RBC1853_4_current_branch" and row["current_status"] == "SELECTED_CURRENT_STATUS" for row in rows_map["range_classifier"]),
            "range classifier selects unknown-current branch",
        )
    )
    checks.append(
        (
            "VAL1853_8_claim_gates_safe",
            any(row["gate_id"] == "CG1853_0_normalization_law" and boolish(row["gate_pass"]) for row in rows_map["claim_gate"])
            and any(row["gate_id"] == "CG1853_3_cg_bound" and not boolish(row["gate_pass"]) for row in rows_map["claim_gate"])
            and all(not boolish(row["valid_for_claim"]) for row in rows_map["claim_gate"]),
            "conditional math gates pass but c_g/local claims do not",
        )
    )
    checks.append(
        (
            "VAL1853_9_next_target_selected",
            any(row["route_id"] == "NEXT1853_0_primary" and row["selection_status"] == "selected" for row in rows_map["next_target"]),
            "next target selected",
        )
    )
    checks.append(
        (
            "VAL1853_10_no_claim_flags",
            all(not boolish(row.get("valid_for_claim", False)) for rows in rows_map.values() for row in rows),
            "no valid_for_claim flags are true",
        )
    )
    checks.append(
        (
            "VAL1853_11_missing_rows_nonclaim",
            all(
                not boolish(row.get("valid_for_claim", False))
                for rows in rows_map.values()
                for row in rows
                if "MISSING_" in " ".join(str(value) for value in row.values())
            ),
            "MISSING_* rows stay nonclaim",
        )
    )
    ok, detail = check_csv_parse()
    checks.append(("VAL1853_12_csv_parse", ok, detail))
    ok, detail = check_branch_copies()
    checks.append(("VAL1853_13_branch_copies", ok, detail))
    pycache_path = ROOT / "scripts" / "__pycache__"
    checks.append(("VAL1853_14_pycache_absent", not pycache_path.exists(), "scripts __pycache__ absent"))
    formalization_outputs = list(FORMALIZATION.rglob("*1853*")) if FORMALIZATION.exists() else []
    checks.append(("VAL1853_15_formalization_untouched", not formalization_outputs, "no 1853 outputs found under formalization-workbench"))
    overall = all(result for _, result, _ in checks)
    validation_rows = [
        {
            "branch_id": BRANCH_ID,
            "check_id": check_id,
            "result": "PASS" if result else "FAIL",
            "detail": detail,
        }
        for check_id, result, detail in checks
    ]
    validation_rows.append(
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL1853_OVERALL",
            "result": "PASS" if overall else "FAIL",
            "detail": "1853 canonical X normalization and range gate for c_g",
        }
    )
    return validation_rows


def markdown_table(rows: list[dict[str, Any]], fields: list[str]) -> str:
    header = "| " + " | ".join(fields) + " |"
    sep = "| " + " | ".join("---" for _ in fields) + " |"
    lines = [header, sep]
    for row in rows:
        values = [str(row.get(field, "")).replace("\n", " ") for field in fields]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def build_markdown(rows_map: dict[str, list[dict[str, Any]]], validation_rows: list[dict[str, Any]]) -> str:
    return "\n".join(
        [
            "# 1853: Canonical X Normalization And Range Gate For c_g",
            "",
            "**Current verdict:** the mathematical gate is now clean: the Cassini comparison must use the rescaling-invariant effective coupling `tau_PPN c_g S_PPN(lambda_X)/sqrt(Z_X)`, not raw `c_g`. The range is fixed by the same parent Hessian, `lambda_X=sqrt(Z_X/M_X^2)`. Current MTS still does not own `Z_X`, `M_X^2`, `tau_PPN`, or `S_PPN`, so the direct `c_g`/local-GR claim remains blocked.",
            "",
            "## Source Register",
            markdown_table(rows_map["source_register"], ["source_id", "source_path", "needle", "use", "status", "valid_for_claim"]),
            "",
            "## Canonical X Normalization Derivation",
            markdown_table(rows_map["canonical_derivation"], ["step_id", "statement", "equation", "derived_object", "status", "missing_for_claim", "valid_for_claim"]),
            "",
            "## Range Transfer Derivation",
            markdown_table(rows_map["range_derivation"], ["step_id", "statement", "equation", "derived_object", "status", "missing_for_claim", "valid_for_claim"]),
            "",
            "## Z_X/M_X^2 Input Gate",
            markdown_table(rows_map["input_gate"], ["gate_id", "needed_input", "current_status", "blocks", "next_evidence", "gate_pass", "valid_for_claim"]),
            "",
            "## c_g Normalized Bound Row",
            markdown_table(rows_map["cg_bound"], ["bound_id", "quantity", "formula", "numeric_bound", "units", "status", "claim_allowed", "valid_for_claim"]),
            "",
            "## Range Branch Classifier",
            markdown_table(rows_map["range_classifier"], ["class_id", "condition", "dominant_test", "allowed_bound_use", "current_status", "valid_for_claim"]),
            "",
            "## Claim Gates",
            markdown_table(rows_map["claim_gate"], ["gate_id", "claim", "gate_pass", "reason", "claim_allowed", "valid_for_claim"]),
            "",
            "## Decisions",
            markdown_table(rows_map["decision"], ["decision_id", "decision", "because", "next_action", "valid_for_claim"]),
            "",
            "## Next Target",
            markdown_table(rows_map["next_target"], ["route_id", "next_target", "script", "objective", "selection_status", "success_condition"]),
            "",
            "## Validation",
            markdown_table(validation_rows, ["check_id", "result", "detail"]),
            "",
            "## Working Interpretation",
            "This is a useful bit of theory hygiene. If someone tries to say Cassini bounds `c_g`, 1853 now answers: only after the parent Hessian gives `Z_X`, the range gate gives `lambda_X`, and the PPN transfer gives `tau_PPN`. That is how we avoid fooling ourselves with a pretty but meaningless number.",
            "",
        ]
    )


def main() -> None:
    ensure_dirs()
    rows_map = build_rows_map()
    for key, rows in rows_map.items():
        write_csv(OUTPUTS[key], rows)
    copy_outputs(include_validation=False)
    validation_rows = build_validation(rows_map)
    write_csv(OUTPUTS["validation"], validation_rows)
    DOC_PATH.write_text(build_markdown(rows_map, validation_rows), encoding="utf-8")
    copy_outputs(include_validation=True)
    print(f"wrote {DOC_PATH}")
    print(f"wrote {OUTPUTS['validation']}")
    print(f"1853 validation {validation_rows[-1]['result']}")


if __name__ == "__main__":
    main()
