from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


PACK_ID = "P8_Y5_R10_1307"
TITLE = "1307-Y5-R10-RAB-canonical-Zm-closure-transfer-audit"
ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "source-intake" / "mts_residuals"
DOC_PATH = ROOT / f"{TITLE}.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
RUN_STARTED_UTC = datetime.now(timezone.utc)


SOURCE_REGISTER_PATH = OUT_DIR / f"{PACK_ID}_SOURCE_REGISTER.csv"
CANONICAL_MAP_PATH = OUT_DIR / f"{PACK_ID}_CANONICAL_FIELD_MAP.csv"
TRANSFER_RESIDUAL_LEDGER_PATH = OUT_DIR / f"{PACK_ID}_TRANSFER_RESIDUAL_LEDGER_NONCLAIM.csv"
ALPHA_TRANSFER_PATH = OUT_DIR / f"{PACK_ID}_ALPHA_TRANSFER_AUDIT.csv"
LOCAL_RESIDUAL_IMPACT_PATH = OUT_DIR / f"{PACK_ID}_LOCAL_RESIDUAL_IMPACT.csv"
CLOSURE_ACCEPTANCE_PATH = OUT_DIR / f"{PACK_ID}_CLOSURE_ACCEPTANCE_GATES.csv"
DECISION_PATH = OUT_DIR / f"{PACK_ID}_DECISION_LEDGER.csv"
NEXT_PATH = OUT_DIR / f"{PACK_ID}_NEXT_TARGET.csv"
VALIDATION_PATH = OUT_DIR / "P8_Y5_BRR545_1307_VALIDATION.csv"


def source_path(relative_path: str) -> Path:
    path = Path(relative_path)
    if path.is_absolute():
        return path
    return ROOT / path


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        fieldnames = []
        for row in rows:
            for key in row:
                if key not in fieldnames:
                    fieldnames.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def md_escape(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def markdown_table(rows: list[dict[str, object]], fields: list[str]) -> str:
    if not rows:
        return "_No rows._\n"
    return "\n".join(
        [
            "| " + " | ".join(fields) + " |",
            "| " + " | ".join(["---"] * len(fields)) + " |",
            *["| " + " | ".join(md_escape(row.get(field, "")) for field in fields) + " |" for row in rows],
        ]
    )


def exists_and_contains(relative_path: str, needle: str) -> tuple[bool, bool]:
    path = source_path(relative_path)
    if not path.exists():
        return False, False
    if not needle:
        return True, True
    return True, needle in read_text(path)


def validation_row(check_id: str, check: str, passed: bool, details: str) -> dict[str, object]:
    return {"check_id": check_id, "check": check, "status": "PASS" if passed else "FAIL", "details": details}


def is_false(value: object) -> bool:
    return str(value).strip().lower() in {"false", "0", "no"}


def all_nonclaim(tables: list[list[dict[str, object]]]) -> bool:
    return all(
        is_false(row.get("valid_for_claim", False)) and is_false(row.get("claim_allowed", False))
        for rows in tables
        for row in rows
    )


def generated_inside_formalization() -> list[Path]:
    generated_paths = [
        SOURCE_REGISTER_PATH,
        CANONICAL_MAP_PATH,
        TRANSFER_RESIDUAL_LEDGER_PATH,
        ALPHA_TRANSFER_PATH,
        LOCAL_RESIDUAL_IMPACT_PATH,
        CLOSURE_ACCEPTANCE_PATH,
        DECISION_PATH,
        NEXT_PATH,
        VALIDATION_PATH,
        DOC_PATH,
    ]
    return [path for path in generated_paths if FORMALIZATION in path.parents]


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    source_register = [
        {
            "source_id": "SRC1307_0_1306_next",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1306_NEXT_TARGET.csv",
            "needle": "NEXT1306_0_1307",
            "role": "handoff into canonical Z_m transfer audit",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1307_1_1306_closure",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1306_ZM_CLOSURE_INPUT_TEMPLATE_NONCLAIM.csv",
            "needle": "ZMC1306_A_constant_canonical",
            "role": "constant canonical closure template being audited",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1307_2_1306_field_redefinition",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1306_FIELD_REDEFINITION_AUDIT.csv",
            "needle": "CANONICALIZATION_MATH_OK_IF_CONSTANT",
            "role": "field redefinition distinction between constant and variable Z_m",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1307_3_826_ansatz",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_826_PARENT_ACTION_ANSATZ.csv",
            "needle": "L_m = -1/2 Z_m(X_B) nabla_mu m nabla^mu m - V_R(m;X_B)",
            "role": "memory sector action scaffold whose terms are transformed",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1307_4_1302_stress",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1302_MEMORY_STRESS_RESIDUAL_CONTRACT_NONCLAIM.csv",
            "needle": "MSR1302_1_spatial_trace_bound_template",
            "role": "stress bound where kinetic normalization and potential/source terms enter",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1307_5_1303_bound_inputs",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1303_K_MEM_STRESS_SIGMA_BOUND_INPUT_LEDGER_NONCLAIM.csv",
            "needle": "KMS1303_3_potential_subtraction_bound",
            "role": "potential/source/boundary stress inputs that survive canonicalization",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1307_6_alpha_inputs",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_ALPHA_LAW_PARENT_INPUTS.csv",
            "needle": "PI560_0_ZX",
            "role": "alpha-law parent inputs showing kinetic normalization, source charge, test charge, and measured GM all matter",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1307_7_alpha_derivation",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_SOURCE_NORMALIZED_ALPHA_DERIVATION_ATTEMPT.csv",
            "needle": "alpha_X(lambda_X)=s_X Pi_M^H[Q_X^H(lambda_X)] q_X^T/(4*pi*Z_X*G_obs*M_H*m_T)",
            "role": "exact alpha law showing Z denominator and charge numerator trade under canonicalization",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1307_8_source_norm_stack",
            "local_path": "source-intake/mts_residuals/P8_SOURCE_NORMALIZATION_THEOREM_STACK.csv",
            "needle": "no_extra_long_range_charge",
            "role": "source normalization theorem stack blocks absorbing transferred charge into measured GM",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1307_9_source_norm_950",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_950_SOURCE_NORMALIZATION_LEMMA_ATTEMPT.csv",
            "needle": "species-weighted source current",
            "role": "countermodel showing source normalization cannot be assumed species blind",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1307_10_local_template",
            "local_path": "source-intake/mts_residuals/MTS_local_residual_predictions_TEMPLATE.csv",
            "needle": "R10_fifth_force",
            "role": "local residual rows that remain live after closure transfer",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]
    for row in source_register:
        exists, needle_found = exists_and_contains(str(row["local_path"]), str(row["needle"]))
        row["exists"] = exists
        row["needle_found"] = needle_found

    canonical_map = [
        {
            "map_id": "CFM1307_0_field_definition",
            "object": "canonical field",
            "original_form": "L_m=-1/2 Z_0 nabla_mu m nabla^mu m - V_R(m;X_B) + m J_m + ...",
            "canonical_form": "m_c=sqrt(Z_0)m; L_m=-1/2 nabla_mu m_c nabla^mu m_c - V_c(m_c;X_B) + m_c J_c + ...",
            "transfer_law": "V_c(m_c;X_B)=V_R(m_c/sqrt(Z_0);X_B); J_c=J_m/sqrt(Z_0)",
            "status": "CONDITIONAL_MAP_CONSTANT_Z0_ONLY",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "map_id": "CFM1307_1_hessian_gap",
            "object": "local mass/gap",
            "original_form": "M_m^2=partial_m^2 V_R(m_*;X_B)/Z_0 in the canonical operator",
            "canonical_form": "M_c^2=partial_{m_c}^2 V_c=(1/Z_0) partial_m^2 V_R",
            "transfer_law": "canonicalizing Z_m does not supply the Hessian; it rescales the missing V_R curvature",
            "status": "HESSIAN_STILL_MISSING",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "map_id": "CFM1307_2_source_charge",
            "object": "source charge",
            "original_form": "Q_m^H(lambda)=int_H J_m F_lambda + boundary/projector/memory pieces",
            "canonical_form": "Q_c^H(lambda)=Q_m^H(lambda)/sqrt(Z_0)",
            "transfer_law": "source strength is not removed; it is rescaled into canonical charge",
            "status": "SOURCE_CHARGE_RETAINED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "map_id": "CFM1307_3_test_charge",
            "object": "test-body coupling",
            "original_form": "V_X=-s_m q_m^T m",
            "canonical_form": "V_X=-s_m q_c^T m_c with q_c^T=q_m^T/sqrt(Z_0)",
            "transfer_law": "test coupling survives unless q_m^T=0 by parent matter descent",
            "status": "TEST_CHARGE_RETAINED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "map_id": "CFM1307_4_alpha_invariance",
            "object": "R10 alpha strength",
            "original_form": "alpha_m=s_m Pi_M^H[Q_m^H] q_m^T/(4*pi*Z_0*G_obs*M_H*m_T)",
            "canonical_form": "alpha_c=s_m Pi_M^H[Q_c^H] q_c^T/(4*pi*G_obs*M_H*m_T)",
            "transfer_law": "alpha_m=alpha_c if Q_c=Q_m/sqrt(Z_0) and q_c=q_m/sqrt(Z_0); setting Z_m=1 does not make alpha zero",
            "status": "NORMALIZATION_MOVES_TO_NUMERATOR",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    transfer_residual_ledger = [
        {
            "residual_id": "TRL1307_0_Vc_hessian",
            "transferred_object": "V_c and M_c^2",
            "needed_for": "positive gap; nohair; local profile; B_V",
            "current_status": "MISSING_V_R_FUNCTION_AND_HESSIAN",
            "must_remain_as": "explicit potential/gap residual input",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_826_PARENT_ACTION_ANSATZ.csv;source-intake/mts_residuals/P8_Y5_R10_1303_K_MEM_STRESS_SIGMA_BOUND_INPUT_LEDGER_NONCLAIM.csv",
            "source_anchor": "AA826_1_memory_sector;KMS1303_3_potential_subtraction_bound",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "residual_id": "TRL1307_1_Jc_source",
            "transferred_object": "J_c=J_m/sqrt(Z_0)",
            "needed_for": "source-free nohair; local profile; R10 source charge",
            "current_status": "MISSING_J_m_ZERO_OR_BOUND",
            "must_remain_as": "explicit source residual input",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_ALPHA_LAW_PARENT_INPUTS.csv;source-intake/mts_residuals/P8_Y5_R10_1042_SOURCE_ZERO_CLAUSE_AUDIT.csv",
            "source_anchor": "PI560_2_JX;SZ1042_5_verdict",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "residual_id": "TRL1307_2_Qc_source_charge",
            "transferred_object": "Q_c^H(lambda)",
            "needed_for": "alpha numerator; R10; WEP/source normalization",
            "current_status": "MISSING_SOURCE_CHARGE_OR_ZERO_THEOREM",
            "must_remain_as": "explicit alpha/source-normalization residual input",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_ALPHA_LAW_PARENT_INPUTS.csv",
            "source_anchor": "PI560_3_QX",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "residual_id": "TRL1307_3_qc_test_charge",
            "transferred_object": "q_c^T",
            "needed_for": "test-body force; WEP; R10",
            "current_status": "MISSING_TEST_CHARGE_OR_MATTER_DESCENT_ZERO",
            "must_remain_as": "explicit matter-coupling residual input",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_ALPHA_LAW_PARENT_INPUTS.csv",
            "source_anchor": "PI560_4_qtest",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "residual_id": "TRL1307_4_PiM_GM",
            "transferred_object": "Pi_M^H and measured GM split",
            "needed_for": "same-frame Newton normalization; alpha denominator; PPN source rows",
            "current_status": "MISSING_SOURCE_NORMALIZATION_PROOF",
            "must_remain_as": "explicit source-normalization residual input",
            "source_path": "source-intake/mts_residuals/P8_SOURCE_NORMALIZATION_THEOREM_STACK.csv;source-intake/mts_residuals/P8_Y5_R10_950_SOURCE_NORMALIZATION_LEMMA_ATTEMPT.csv",
            "source_anchor": "S3_no_extra_long_range_charge;SNL950_5_verdict",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "residual_id": "TRL1307_5_boundary_projector_memory",
            "transferred_object": "boundary/projector/memory source pieces",
            "needed_for": "alpha3; R10 tails; Gdot; domain leakage",
            "current_status": "MISSING_BOUNDARY_PROJECTOR_MEMORY_ZERO_OR_BOUND",
            "must_remain_as": "explicit boundary/domain/memory residual input",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_ALPHA_LAW_PARENT_INPUTS.csv;source-intake/mts_residuals/P8_SOURCE_NORMALIZATION_CHANNEL_AUDIT.csv",
            "source_anchor": "PI560_8_boundary_flux;PI560_9_memory_kernel;C5_nonlocal_or_bulk",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    alpha_transfer = [
        {
            "audit_id": "ATA1307_0_formula",
            "formula_piece": "alpha_m=s_m Pi_M^H[Q_m^H] q_m^T/(4*pi*Z_0*G_obs*M_H*m_T)",
            "canonical_transfer": "Q_c=Q_m/sqrt(Z_0), q_c=q_m/sqrt(Z_0), so alpha_c=s_m Pi_M^H[Q_c^H]q_c^T/(4*pi*G_obs*M_H*m_T)",
            "verdict": "ALPHA_STRENGTH_INVARIANT_UNDER_CONSTANT_CANONICALIZATION",
            "claim_effect": "Z_m=1 cannot be used as an R10 pass; source/test/projection zeros are still required",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "ATA1307_1_zero_routes",
            "formula_piece": "alpha=0",
            "canonical_transfer": "requires Pi_M^H Q_c^H=0 or q_c^T=0 or a parent theorem setting the physical spectral source to zero",
            "verdict": "ZERO_ROUTE_UNCHANGED_BY_CANONICALIZATION",
            "claim_effect": "mass gap/kinetic normalization alone is not a zero",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "ATA1307_2_source_normalization",
            "formula_piece": "G_obs*M_H*m_T",
            "canonical_transfer": "measured GM cannot absorb Q_c/q_c unless residuals are range/time/species/radial independent and parent-signed",
            "verdict": "NO_ABSORPTION_CHEAT",
            "claim_effect": "R1/WEP, R9/Gdot, R10, and R11 source-normalization rows remain live",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    local_residual_impact = [
        {
            "impact_id": "LRI1307_0_R10",
            "row": "R10_fifth_force",
            "effect": "canonical Z_m removes denominator bookkeeping but leaves alpha numerator Q_c q_c and measured-GM split open",
            "status": "R10_REMAINS_LIVE_NONCLAIM",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "impact_id": "LRI1307_1_R1_WEP",
            "row": "R1_WEP_source_charge",
            "effect": "q_c^T or source normalization can be species dependent unless matter descent/source universality is parent-signed",
            "status": "WEP_SOURCE_ROW_REMAINS_LIVE",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "impact_id": "LRI1307_2_R3_R4_PPN",
            "row": "R3_gamma;R4_beta",
            "effect": "potential/source transfer can alter weak-field source normalization and second-order metric response",
            "status": "PPN_ROWS_REMAIN_LIVE",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "impact_id": "LRI1307_3_R9",
            "row": "R9_Gdot",
            "effect": "time-dependent source or memory transfer cannot be calibrated away without derivative silence",
            "status": "GDOT_ROW_REMAINS_LIVE",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "impact_id": "LRI1307_4_Kmem",
            "row": "K_mem_stress^Sigma",
            "effect": "gradient kinetic term can be canonicalized, but B_V, J_c, boundary, and source/bath stress terms remain unbounded",
            "status": "K_MEM_STRESS_REMAINS_UNSCORED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    closure_acceptance = [
        {
            "gate_id": "CAG1307_0_constant_only",
            "condition": "Z_m is a global positive constant in the private branch",
            "current_status": "ASSUMED_ONLY_NOT_PARENT_DERIVED",
            "if_fail": "canonical closure invalid; return to parent Z_m(X_B) function/bounds",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "CAG1307_1_transfer_complete",
            "condition": "V_R, J_m, Q_H, q_T, Pi_M, GM, boundary/projector/memory terms are all transformed and retained",
            "current_status": "TRANSFER_RESIDUALS_RETAINED_NOT_CLOSED",
            "if_fail": "closure hides coupling and must not be used",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "CAG1307_2_no_claim",
            "condition": "canonical Z_m=1 branch is private algebra/sensitivity only",
            "current_status": "PASS_POLICY_RECORDED",
            "if_fail": "public/local-GR/R10/PPN claims would be overclaims",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "CAG1307_3_smoke_allowed",
            "condition": "smoke tests may run only with every transferred coupling marked closure_assumed/speculative/nonclaim",
            "current_status": "ALLOWED_FOR_NONCLAIM_SMOKE_ONLY",
            "if_fail": "runner outputs must be blocked",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    decision = [
        {
            "decision_id": "DEC1307_0_transfer_not_clean",
            "decision": "canonical Z_m closure is not transfer-clean enough to claim anything",
            "because": "the denominator normalization moves into V_R/J_m/Q/q/source-normalization residuals",
            "next_action": "attack source/test charge zero-or-bound first, because it controls R10 and local matter coupling",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1307_1_keep_branch_useful",
            "decision": "keep constant canonical Z_m as a private bookkeeping branch",
            "because": "it removes one coefficient from algebra while making every transferred coupling explicit",
            "next_action": "do not abandon it; use it only as a transparent transfer frame",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    next_target = [
        {
            "next_id": "NEXT1307_0_1308",
            "target_file": "1308-Y5-R10-RAB-canonical-memory-source-test-charge-zero-or-bound.md",
            "target_script": "scripts/Y5_R10_RAB_canonical_memory_source_test_charge_zero_or_bound.py",
            "task": "try to prove or bound the canonical source/test couplings J_c, Q_c^H(lambda), q_c^T, and Pi_M^H Q_c^H that survive Z_m canonicalization",
            "success_condition": "either a parent matter/source theorem gives Q_c=0 or q_c=0, or executable nonclaim alpha/source rows are staged with no hidden normalization",
            "do_not": "do not use canonical Z_m=1 as an R10 or local-GR pass unless source/test/projection channels close",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]

    write_csv(SOURCE_REGISTER_PATH, source_register)
    write_csv(CANONICAL_MAP_PATH, canonical_map)
    write_csv(TRANSFER_RESIDUAL_LEDGER_PATH, transfer_residual_ledger)
    write_csv(ALPHA_TRANSFER_PATH, alpha_transfer)
    write_csv(LOCAL_RESIDUAL_IMPACT_PATH, local_residual_impact)
    write_csv(CLOSURE_ACCEPTANCE_PATH, closure_acceptance)
    write_csv(DECISION_PATH, decision)
    write_csv(NEXT_PATH, next_target)

    validations = []
    source_count = len(source_register)
    source_hits = sum(1 for row in source_register if row["exists"] and row["needle_found"])
    validations.append(
        validation_row(
            "VAL1307_0_sources_exist",
            "registered source paths exist and anchors are found",
            source_hits == source_count,
            f"{source_hits}/{source_count} source anchors found",
        )
    )
    validations.append(
        validation_row(
            "VAL1307_1_canonical_map_written",
            "canonical field map includes field, Hessian, source, test charge, and alpha transfer",
            {row["map_id"] for row in canonical_map}
            == {"CFM1307_0_field_definition", "CFM1307_1_hessian_gap", "CFM1307_2_source_charge", "CFM1307_3_test_charge", "CFM1307_4_alpha_invariance"},
            ";".join(str(row["map_id"]) + "=" + str(row["status"]) for row in canonical_map),
        )
    )
    validations.append(
        validation_row(
            "VAL1307_2_alpha_not_zeroed",
            "alpha transfer says canonicalization moves normalization to numerator but does not zero force",
            any(row["audit_id"] == "ATA1307_0_formula" and row["verdict"] == "ALPHA_STRENGTH_INVARIANT_UNDER_CONSTANT_CANONICALIZATION" for row in alpha_transfer)
            and any(row["audit_id"] == "ATA1307_1_zero_routes" and row["verdict"] == "ZERO_ROUTE_UNCHANGED_BY_CANONICALIZATION" for row in alpha_transfer),
            ";".join(str(row["audit_id"]) + "=" + str(row["verdict"]) for row in alpha_transfer),
        )
    )
    validations.append(
        validation_row(
            "VAL1307_3_transfer_residuals_retained",
            "transferred V/J/Q/q/source-normalization/boundary pieces remain explicit residuals",
            len(transfer_residual_ledger) == 6 and all("MISSING" in str(row["current_status"]) for row in transfer_residual_ledger),
            ";".join(str(row["residual_id"]) + "=" + str(row["current_status"]) for row in transfer_residual_ledger),
        )
    )
    validations.append(
        validation_row(
            "VAL1307_4_local_rows_live",
            "local residual impact keeps R10/WEP/PPN/Gdot/Kmem live",
            len(local_residual_impact) == 5 and all("REMAIN" in str(row["status"]) for row in local_residual_impact),
            ";".join(str(row["impact_id"]) + "=" + str(row["status"]) for row in local_residual_impact),
        )
    )
    validations.append(
        validation_row(
            "VAL1307_5_closure_acceptance_nonclaim",
            "closure acceptance gates allow only nonclaim private smoke use",
            len(closure_acceptance) == 4 and all(is_false(row["valid_for_claim"]) and is_false(row["claim_allowed"]) for row in closure_acceptance),
            ";".join(str(row["gate_id"]) + "=" + str(row["current_status"]) for row in closure_acceptance),
        )
    )
    generated_tables = [
        SOURCE_REGISTER_PATH,
        CANONICAL_MAP_PATH,
        TRANSFER_RESIDUAL_LEDGER_PATH,
        ALPHA_TRANSFER_PATH,
        LOCAL_RESIDUAL_IMPACT_PATH,
        CLOSURE_ACCEPTANCE_PATH,
        DECISION_PATH,
        NEXT_PATH,
    ]
    parse_ok = True
    parse_details: list[str] = []
    for table_path in generated_tables:
        try:
            parse_details.append(f"{table_path.name}:{len(read_csv(table_path))}")
        except Exception as error:
            parse_ok = False
            parse_details.append(f"{table_path.name}:ERROR:{error}")
    validations.append(validation_row("VAL1307_6_csv_parse", "all generated CSVs parse cleanly", parse_ok, "; ".join(parse_details)))
    formalization_hits = generated_inside_formalization()
    validations.append(
        validation_row(
            "VAL1307_7_formalization_untouched",
            "formalization-workbench untouched by generated outputs",
            not formalization_hits,
            f"formalization_generated_output_count={len(formalization_hits)}",
        )
    )
    validations.append(
        validation_row(
            "VAL1307_8_nonclaim_policy",
            "all generated rows remain nonclaim",
            all_nonclaim([source_register, canonical_map, transfer_residual_ledger, alpha_transfer, local_residual_impact, closure_acceptance, decision, next_target]),
            "valid_for_claim=false and claim_allowed=false throughout generated tables",
        )
    )
    validations.append(
        validation_row(
            "VAL1307_9_next_target_1308",
            "next target routes to canonical source/test charge zero-or-bound",
            next_target[0]["next_id"] == "NEXT1307_0_1308" and "source-test-charge" in str(next_target[0]["target_file"]),
            str(next_target[0]["target_file"]),
        )
    )
    overall_pass = all(row["status"] == "PASS" for row in validations)
    validations.append(
        validation_row(
            "VAL1307_10_overall",
            "overall 1307 validation",
            overall_pass,
            "1307 proves canonical Z_m closure is bookkeeping only: alpha strength is invariant under constant rescaling, transferred couplings remain explicit, and source/test charge is the next target",
        )
    )
    write_csv(VALIDATION_PATH, validations)

    doc = f"""# 1307 Y5 R10 RAB canonical Zm closure transfer audit

Generated: `{RUN_STARTED_UTC.isoformat()}`

**Current verdict:** constant canonical `Z_m=1` is mathematically acceptable as a private bookkeeping frame, but it is **not** a physics pass. The coupling does not disappear; it transfers into `V_R`, `J_m`, source charge `Q_c^H`, test charge `q_c^T`, projection `Pi_M`, and measured-GM/source-normalization rows.

**Key result:** for constant `Z_0>0`, `m_c=sqrt(Z_0)m` makes the kinetic term canonical. But the R10 strength is invariant under the matching charge transfer: `Q_c=Q_m/sqrt(Z_0)` and `q_c=q_m/sqrt(Z_0)`, so `alpha_c = alpha_m`. Therefore `Z_m=1` cannot be used as an R10/local-GR/no-hair claim.

**Decision:** keep the branch as a clean private algebra frame, but retain every transferred coupling as an explicit nonclaim residual. Next we attack the physical source/test charge channel.

## Source Register

{markdown_table(source_register, ["source_id", "local_path", "needle", "exists", "needle_found", "role", "valid_for_claim", "claim_allowed"])}

## Canonical Field Map

{markdown_table(canonical_map, ["map_id", "object", "original_form", "canonical_form", "transfer_law", "status", "valid_for_claim", "claim_allowed"])}

## Transfer Residual Ledger

{markdown_table(transfer_residual_ledger, ["residual_id", "transferred_object", "needed_for", "current_status", "must_remain_as", "source_path", "source_anchor", "valid_for_claim", "claim_allowed"])}

## Alpha Transfer Audit

{markdown_table(alpha_transfer, ["audit_id", "formula_piece", "canonical_transfer", "verdict", "claim_effect", "valid_for_claim", "claim_allowed"])}

## Local Residual Impact

{markdown_table(local_residual_impact, ["impact_id", "row", "effect", "status", "valid_for_claim", "claim_allowed"])}

## Closure Acceptance Gates

{markdown_table(closure_acceptance, ["gate_id", "condition", "current_status", "if_fail", "valid_for_claim", "claim_allowed"])}

## Decision Ledger

{markdown_table(decision, ["decision_id", "decision", "because", "next_action", "valid_for_claim", "claim_allowed"])}

## Next Target

{markdown_table(next_target, ["next_id", "target_file", "target_script", "task", "success_condition", "do_not", "valid_for_claim", "claim_allowed"])}

## Validation

{markdown_table(validations, ["check_id", "check", "status", "details"])}
"""
    DOC_PATH.write_text(doc, encoding="utf-8")


if __name__ == "__main__":
    main()
