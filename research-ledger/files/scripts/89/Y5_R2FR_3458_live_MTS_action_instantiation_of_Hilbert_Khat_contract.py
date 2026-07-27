from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "3458-Y5-R2FR-live-MTS-action-instantiation-of-Hilbert-Khat-contract-under-AX1090.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"

SOURCES = {
    "script_3458": Path(__file__).resolve(),
    "doc_3457": ROOT / "3457-Y5-R2FR-parent-Hilbert-Khat-contract-or-local-vacuum-Noether-proof-under-AX1090.md",
    "contract_3457": OUT / "P8_Y5_R2FR_3457_PARENT_HILBERT_KHAT_CONTRACT.csv",
    "residual_3457": OUT / "P8_Y5_R2FR_3457_LOCAL_QLOC_RESIDUAL_VECTOR.csv",
    "doc_3456": ROOT / "3456-Y5-R2FR-DeltaK-derivative-Hodge-projector-component-or-bound-fill-under-AX1090.md",
    "typing_3454": OUT / "P8_Y5_R2FR_3454_GK_PLACEHOLDER_TYPING.csv",
    "components_3455": OUT / "P8_Y5_R2FR_3455_DELTAK_COMPONENT_LEDGER.csv",
    "gk_candidates": OUT / "P8_GK_STRESS_ACTION_CANDIDATES.csv",
    "gk_evidence": OUT / "P8_GK_METRIC_RESPONSE_SOURCE_EVIDENCE.csv",
    "first_variation_contract": OUT / "P8_GAMMA_KHAT_QLOC_FIRST_VARIATION_CONTRACT.csv",
    "symbol_action_map": OUT / "P8_MTS_SYMBOL_TO_LOCAL_GR_ACTION_MAP.csv",
    "gamma_owner": OUT / "P8_GAMMA_OWNER_CANDIDATE_ACTION.csv",
    "doublet_variation": OUT / "P8_RESPONSE_DOUBLET_ACTION_VARIATION.csv",
    "doublet_contract": OUT / "P8_RESPONSE_DOUBLET_ACTION_CONTRACT.csv",
    "doc_1010": ROOT / "1010-Y5-R10-Gamma-Khat-action-existence-Helmholtz-or-q_loc-residual-retention.md",
}


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
        for row in rows:
            writer.writerow(row)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def md_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "_No rows._"
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    header = "| " + " | ".join(fields) + " |"
    sep = "| " + " | ".join(["---"] * len(fields)) + " |"
    body: list[str] = []
    for row in rows:
        vals = []
        for field in fields:
            vals.append(str(row.get(field, "")).replace("\n", "<br>").replace("|", "/"))
        body.append("| " + " | ".join(vals) + " |")
    return "\n".join([header, sep, *body])


def source_register() -> list[dict[str, Any]]:
    roles = {
        "script_3458": "generator for this checkpoint",
        "doc_3457": "parent Hilbert-Khat contract predecessor",
        "contract_3457": "six parent contract clauses",
        "residual_3457": "exact q_loc residual vector",
        "doc_3456": "Noether/Hilbert route and derivative/Hodge stress interpretation",
        "typing_3454": "Gamma/Khat/q_loc live symbol typing",
        "components_3455": "Delta_K component ledger",
        "gk_candidates": "older S_GK candidate action list",
        "gk_evidence": "older metric response source evidence",
        "first_variation_contract": "older Gamma/Khat/q_loc first variation contract",
        "symbol_action_map": "symbol-to-local-GR action placement map",
        "gamma_owner": "Gamma owner candidate action rows",
        "doublet_variation": "response-doublet action variation rows",
        "doublet_contract": "response-doublet contract rows",
        "doc_1010": "earlier action-existence/Helmholtz checkpoint",
    }
    return [
        {
            "timestamp_utc": datetime.now(timezone.utc).isoformat(),
            "source_id": key,
            "path": str(path),
            "exists": path.exists(),
            "role": roles[key],
        }
        for key, path in SOURCES.items()
    ]


def live_symbol_map() -> list[dict[str, Any]]:
    return [
        {
            "symbol_id": "LSM3458_0_Gamma_eff",
            "live_symbol": "Gamma_eff",
            "best_instantiation": "Gamma_X = Gamma0 + 1/2 M_AB(g,R_even,D) Z^A Z^B + 1/2 H_AB^{mu nu}(g,R_even,D) nabla_mu Z^A nabla_nu Z^B + O(Z^4)",
            "source_evidence": str(SOURCES["gamma_owner"]),
            "contract_status": "CANDIDATE_PARENT_ACTION_NOT_ORIGINAL_SYMBOL_PROVED",
            "remaining_gap": "identify physical leakage multiplet Z^A with local MTS residual components and prove no linear source term",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "symbol_id": "LSM3458_1_K_hat",
            "live_symbol": "K_hat^{mu nu}",
            "best_instantiation": "K_hat^{mu nu} := K_H^{mu nu} = 2/sqrt(-g) delta[sqrt(-g) Gamma_X]/delta g_{mu nu} with the SIGN2975 volume convention",
            "source_evidence": str(SOURCES["contract_3457"]),
            "contract_status": "CAN_BE_PARENT_DEFINITION_IF_ADOPTED",
            "remaining_gap": "show this definition matches every existing use of K_hat or formally replace the old free K_hat closure symbol",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "symbol_id": "LSM3458_2_q_loc",
            "live_symbol": "q_loc^nu",
            "best_instantiation": "q_loc^nu = P_loc[J_E^nu + J_B^nu - nabla_mu Delta_K^{mu nu}] and Delta_K=0 in the adopted Hilbert-Khat parent branch",
            "source_evidence": str(SOURCES["residual_3457"]),
            "contract_status": "EXACT_RESIDUAL_FORM_READY",
            "remaining_gap": "prove P_loc parent linearity, local E_A=0, and boundary no-flux",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "symbol_id": "LSM3458_3_P_loc",
            "live_symbol": "P_loc",
            "best_instantiation": "P_loc is a parent-owned linear readout/projector with P_loc(0)=0 and no metric-domain variation outside K_H",
            "source_evidence": str(SOURCES["symbol_action_map"]),
            "contract_status": "OPEN_PROJECTOR_OWNERSHIP",
            "remaining_gap": "map P_loc to Pi_M/P_coh/domain selector or leave Q_projector residual",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "symbol_id": "LSM3458_4_Delta_K",
            "live_symbol": "Delta_K^{mu nu}",
            "best_instantiation": "Delta_K^{mu nu}=0 by parent definition only inside the Hilbert-Khat branch; otherwise keep component bound Q_metric+Q_derivative+Q_boundary+Q_functional",
            "source_evidence": str(SOURCES["components_3455"]),
            "contract_status": "ZERO_IF_BRANCH_ADOPTED_ELSE_BOUND",
            "remaining_gap": "branch adoption and old-symbol compatibility proof",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def parent_action_candidate() -> list[dict[str, Any]]:
    return [
        {
            "candidate_id": "PAC3458_0_minimal_response_doublet_parent",
            "action_name": "minimal Hilbert-Khat response-doublet parent sector",
            "action_density": "Gamma_X = Gamma0 + 1/2 M_AB Z^A Z^B + 1/2 H_AB^{mu nu} nabla_mu Z^A nabla_nu Z^B + O(Z^4)",
            "field_content": "Z^A=(R_+^A-R_-^A)/2; R_even^A=(R_+^A+R_-^A)/2; g_mu_nu; parent projector/readout data",
            "Khat_rule": "K_hat is not independent: K_hat := K_H[Gamma_X]",
            "Euler_equation": "E_A = M_AB Z^B - nabla_mu(H_AB^{mu nu} nabla_nu Z^B) + O(Z^3) - J_A",
            "local_zero_route": "if J_A=0, boundary flux=0, H/M define a positive self-adjoint operator, and Z has compact/local-vacuum boundary class, then Z=0 and q_loc=0",
            "why_not_closure": "K_hat is obtained by varying the candidate action, not tuned after q_loc is computed",
            "current_status": "BEST_CONSTRUCTION_CANDIDATE_NOT_CLAIM",
            "source_path": str(SOURCES["doublet_variation"]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "candidate_id": "PAC3458_1_positive_auxiliary_parent",
            "action_name": "positive auxiliary field parent sector",
            "action_density": "Gamma_X = V(Phi) + 1/2 G_AB(Phi) nabla Phi^A nabla Phi^B",
            "field_content": "auxiliary silence fields Phi^A",
            "Khat_rule": "K_hat := K_H[Gamma_X]",
            "Euler_equation": "E_A = -nabla_mu(G_AB nabla^mu Phi^B) + partial_A V + metric/field-space terms",
            "local_zero_route": "positive potential/operator plus source-free compact branch forces Phi=Phi0",
            "why_not_closure": "standard Hilbert stress construction",
            "current_status": "VIABLE_BUT_LESS_TIED_TO_EXISTING_DOUBLET_ROWS",
            "source_path": str(SOURCES["gk_candidates"]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "candidate_id": "PAC3458_2_topological_boundary_parent",
            "action_name": "topological or exact boundary parent sector",
            "action_density": "Gamma_X = dB_X / sqrt(-g) or topological density",
            "field_content": "boundary/topological class variables",
            "Khat_rule": "K_hat := boundary/improvement Hilbert response",
            "Euler_equation": "bulk Euler current vanishes if exact/topological; boundary current remains",
            "local_zero_route": "bulk q_loc=0 if boundary/reference flux is fixed or canceled",
            "why_not_closure": "exact form can be action-owned",
            "current_status": "OPEN_BOUNDARY_FLUX_RISK",
            "source_path": str(SOURCES["gamma_owner"]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def contract_instantiation() -> list[dict[str, Any]]:
    return [
        {
            "clause_id": "PHK3457_0_action_scalar_density",
            "instantiation": "PAC3458_0 supplies a covariant scalar-density template if M_AB and H_AB are parent tensors/functions of g,R_even,D.",
            "current_result": "PARTIAL_CONSTRUCTION",
            "missing_for_pass": "source-owned M_AB/H_AB formulas and field-content units",
            "residual_if_open": "noncovariant/background force residual",
            "source_path": str(SOURCES["gamma_owner"]),
            "claim_allowed": False,
        },
        {
            "clause_id": "PHK3457_1_transforming_fields",
            "instantiation": "R_+^A,R_-^A,Z^A,R_even^A are proposed fields; tensor/Lie transformation rules are required for every local leakage component.",
            "current_result": "OPEN_FIELD_TRANSFORM_TABLE",
            "missing_for_pass": "Lie_xi rules for all Z^A, memory/source/projector slots",
            "residual_if_open": "J_E cannot be computed cleanly",
            "source_path": str(SOURCES["doublet_contract"]),
            "claim_allowed": False,
        },
        {
            "clause_id": "PHK3457_2_Khat_definition",
            "instantiation": "Adopt K_hat := K_H[Gamma_X] in the parent branch.",
            "current_result": "DEFINITION_AVAILABLE_NOT_BACKWARD_MATCHED",
            "missing_for_pass": "compatibility proof that previous K_hat uses are this Hilbert response",
            "residual_if_open": "Delta_K mismatch vector remains",
            "source_path": str(SOURCES["gk_evidence"]),
            "claim_allowed": False,
        },
        {
            "clause_id": "PHK3457_3_local_on_shell_branch",
            "instantiation": "Response-doublet Euler equation L_AB Z^B = J_A + boundary/source terms.",
            "current_result": "REDUCED_TO_SOURCE_ZERO_AND_POSITIVITY",
            "missing_for_pass": "J_A=0 source-current theorem and positive self-adjoint L_AB",
            "residual_if_open": "P_loc J_E",
            "source_path": str(SOURCES["doublet_variation"]),
            "claim_allowed": False,
        },
        {
            "clause_id": "PHK3457_4_boundary_reference_class",
            "instantiation": "No-flux/fixed-reference boundary condition for the doublet energy identity.",
            "current_result": "OPEN_BOUNDARY_FLUX",
            "missing_for_pass": "B_Z=0 or bounded boundary current",
            "residual_if_open": "P_loc J_B",
            "source_path": str(SOURCES["doublet_contract"]),
            "claim_allowed": False,
        },
        {
            "clause_id": "PHK3457_5_projector_linearity",
            "instantiation": "Use P_loc as a linear parent readout acting after the Noether identity.",
            "current_result": "OPEN_PROJECTOR_DEFINITION",
            "missing_for_pass": "P_loc=parent readout with P_loc(0)=0 and no metric-domain leakage",
            "residual_if_open": "Q_projector",
            "source_path": str(SOURCES["symbol_action_map"]),
            "claim_allowed": False,
        },
    ]


def residual_vector_after_instantiation() -> list[dict[str, Any]]:
    return [
        {
            "residual_id": "RVI3458_0_instantiated_q_loc",
            "quantity": "q_loc^nu",
            "exact_or_bound_form": "q_loc^nu = P_loc[J_E^nu + J_B^nu] in the adopted Hilbert-Khat branch; otherwise add -P_loc nabla_mu Delta_K^{mu nu}",
            "current_source": "J_E,J_B,Delta_K components",
            "zero_condition": "J_E=0, J_B=0, Delta_K=0, P_loc(0)=0",
            "current_status": "EXACT_FORM_REDUCED",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "residual_id": "RVI3458_1_doublet_field_current",
            "quantity": "J_E^nu",
            "exact_or_bound_form": "J_E^nu ~ E_A Lie_{basis nu} Z^A plus even-field/projector terms; E_A=L_AB Z^B-J_A-B_A",
            "current_source": "response doublet Euler equation",
            "zero_condition": "local branch has E_A=0 after J_A=0 and boundary/source terms vanish",
            "current_status": "SOURCE_ZERO_AND_EULER_PROOF_NEEDED",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "residual_id": "RVI3458_2_boundary_current",
            "quantity": "J_B^nu",
            "exact_or_bound_form": "J_B^nu is the boundary/symplectic current from integration by parts and reference subtraction",
            "current_source": "doublet no-flux boundary clause",
            "zero_condition": "compact support, fixed reference, or explicit improvement term",
            "current_status": "BOUNDARY_NO_FLUX_NEEDED",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "residual_id": "RVI3458_3_khat_mismatch",
            "quantity": "Delta_K^{mu nu}",
            "exact_or_bound_form": "Delta_K=0 only if the Hilbert-Khat parent branch is adopted and old K_hat usages are reinterpreted or replaced",
            "current_source": "old free K_hat symbol versus new K_H definition",
            "zero_condition": "K_hat := K_H[Gamma_X] with no leftover independent closure term",
            "current_status": "BRANCH_DECISION_REQUIRED_NOT_PUBLIC_CLAIM",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def energy_identity_target() -> list[dict[str, Any]]:
    return [
        {
            "target_id": "EIT3458_0_next_derivation",
            "identity_to_prove": "integral_U Z^A L_AB Z^B = integral_U Z^A J_A + boundary_flux",
            "if_positive": "lambda_min ||Z||^2 <= ||Z|| ||J|| + |boundary_flux|",
            "bound_result": "||Z|| <= ||J||/lambda_min + sqrt(|boundary_flux|/lambda_min) up to norm constants",
            "zero_result": "if J_A=0 and boundary_flux=0 then Z=0, Gamma_X-Gamma0=0, K_H=0 at the local branch, and q_loc=0",
            "why_this_is_next": "This converts the current source/boundary gaps into either a proof or a measured residual bound.",
            "claim_allowed": False,
            "valid_for_claim": False,
        }
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3458_0_best_route",
            "decision": "Use the response-doublet parent action as the live construction route and define K_hat as its Hilbert response inside that branch.",
            "reason": "It preserves GR-style conservation, preserves wave/Hodge/Poynting stress as real Hilbert stress, and turns local-GR recovery into source-zero/positivity/boundary proof instead of a plateau axiom.",
            "risk": "If the doublet fields or source-zero theorem cannot be parent-owned, the branch becomes a useful EFT/residual-bound model rather than a fundamental local-GR derivation.",
            "next_action": "Prove the doublet energy identity and either close J_A=B_A=0 or produce a quantitative q_loc residual bound.",
            "claim_allowed": False,
            "valid_for_claim": False,
        }
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_doc": "3459-Y5-R2FR-response-doublet-energy-identity-source-zero-or-q_loc-bound-under-AX1090.md",
            "next_script": "scripts/Y5_R2FR_3459_response_doublet_energy_identity_source_zero_or_qloc_bound.py",
            "objective": "Derive the response-doublet energy identity for the 3458 parent action, prove/bound J_A and boundary flux, and translate the result into q_loc and PPN residual bounds.",
            "success_gate": "Either source-free positive operator gives Z=0 and q_loc=0 conditionally, or a concrete residual bound in terms of J_A, boundary flux and lambda_min is emitted.",
            "claim_allowed": False,
            "valid_for_claim": False,
        }
    ]


def formalization_modified_count_since(start_utc: datetime) -> int:
    if not FORMALIZATION.exists():
        return 0
    count = 0
    for path in FORMALIZATION.rglob("*"):
        if not path.is_file():
            continue
        try:
            mtime = datetime.fromtimestamp(path.stat().st_mtime, timezone.utc)
        except OSError:
            continue
        if mtime >= start_utc:
            count += 1
    return count


def validation_rows(rows_by_name: dict[str, list[dict[str, Any]]], start_utc: datetime) -> list[dict[str, Any]]:
    source_rows = rows_by_name["source_register"]
    symbol_rows = rows_by_name["live_symbol_map"]
    action_rows = rows_by_name["parent_action_candidate"]
    contract_rows = rows_by_name["contract_instantiation"]
    residual_rows = rows_by_name["residual_vector_after_instantiation"]
    energy_rows = rows_by_name["energy_identity_target"]
    next_rows = rows_by_name["next_target"]

    generated_paths = [
        OUT / "P8_Y5_R2FR_3458_SOURCE_REGISTER.csv",
        OUT / "P8_Y5_R2FR_3458_LIVE_SYMBOL_MAP.csv",
        OUT / "P8_Y5_R2FR_3458_PARENT_ACTION_CANDIDATE.csv",
        OUT / "P8_Y5_R2FR_3458_CONTRACT_INSTANTIATION.csv",
        OUT / "P8_Y5_R2FR_3458_RESIDUAL_VECTOR_AFTER_INSTANTIATION.csv",
        OUT / "P8_Y5_R2FR_3458_ENERGY_IDENTITY_TARGET.csv",
        OUT / "P8_Y5_R2FR_3458_DECISION_LEDGER.csv",
        OUT / "P8_Y5_R2FR_3458_NEXT_TARGET.csv",
    ]
    csv_parse_ok = True
    csv_details: list[str] = []
    for path in generated_paths:
        try:
            parsed = read_csv(path)
            csv_details.append(f"{path.name}:{len(parsed)}")
        except Exception as exc:
            csv_parse_ok = False
            csv_details.append(f"{path.name}:{exc}")

    checks: list[dict[str, Any]] = []
    checks.append(
        {
            "check_id": "VAL3458_0_sources_exist",
            "description": "all source paths exist",
            "passed": all(bool(row["exists"]) for row in source_rows),
            "detail": f"{sum(1 for row in source_rows if row['exists'])}/{len(source_rows)} source paths exist",
        }
    )
    checks.append(
        {
            "check_id": "VAL3458_1_live_symbols_mapped",
            "description": "Gamma_eff, K_hat, q_loc, P_loc and Delta_K are mapped",
            "passed": {"Gamma_eff", "K_hat^{mu nu}", "q_loc^nu", "P_loc", "Delta_K^{mu nu}"}.issubset(
                {str(row["live_symbol"]) for row in symbol_rows}
            ),
            "detail": ";".join(row["live_symbol"] for row in symbol_rows),
        }
    )
    checks.append(
        {
            "check_id": "VAL3458_2_parent_action_candidate",
            "description": "response-doublet parent action candidate includes Hilbert Khat rule",
            "passed": any(
                row["candidate_id"] == "PAC3458_0_minimal_response_doublet_parent"
                and "K_hat := K_H" in str(row["Khat_rule"])
                and "Z^A" in str(row["action_density"])
                for row in action_rows
            ),
            "detail": ";".join(row["candidate_id"] for row in action_rows),
        }
    )
    checks.append(
        {
            "check_id": "VAL3458_3_contract_instantiated",
            "description": "all six PHK3457 clauses are instantiated or explicitly left open",
            "passed": {
                "PHK3457_0_action_scalar_density",
                "PHK3457_1_transforming_fields",
                "PHK3457_2_Khat_definition",
                "PHK3457_3_local_on_shell_branch",
                "PHK3457_4_boundary_reference_class",
                "PHK3457_5_projector_linearity",
            }.issubset({str(row["clause_id"]) for row in contract_rows}),
            "detail": ";".join(row["current_result"] for row in contract_rows),
        }
    )
    checks.append(
        {
            "check_id": "VAL3458_4_residual_vector_concrete",
            "description": "q_loc residual is concretized into J_E, J_B and Delta_K",
            "passed": {"RVI3458_1_doublet_field_current", "RVI3458_2_boundary_current", "RVI3458_3_khat_mismatch"}.issubset(
                {str(row["residual_id"]) for row in residual_rows}
            ),
            "detail": ";".join(row["residual_id"] for row in residual_rows),
        }
    )
    checks.append(
        {
            "check_id": "VAL3458_5_energy_identity_next",
            "description": "next derivation target is an energy identity with source/boundary bound",
            "passed": len(energy_rows) == 1 and "integral_U Z^A L_AB Z^B" in str(energy_rows[0]["identity_to_prove"]),
            "detail": energy_rows[0]["bound_result"] if energy_rows else "missing",
        }
    )
    checks.append(
        {
            "check_id": "VAL3458_6_no_claims",
            "description": "all generated rows remain nonclaim",
            "passed": all(
                str(row.get("claim_allowed", "False")) == "False"
                for rows in rows_by_name.values()
                for row in rows
                if isinstance(row, dict)
            ),
            "detail": "claim_allowed=false across generated rows",
        }
    )
    checks.append(
        {
            "check_id": "VAL3458_7_csv_parse",
            "description": "generated CSV files parse cleanly",
            "passed": csv_parse_ok,
            "detail": ";".join(csv_details),
        }
    )
    checks.append(
        {
            "check_id": "VAL3458_8_next_target_3459",
            "description": "next target is response-doublet energy identity",
            "passed": len(next_rows) == 1 and "3459-Y5-R2FR-response-doublet-energy-identity" in str(next_rows[0]["next_doc"]),
            "detail": str(next_rows[0]["next_doc"]) if next_rows else "missing next row",
        }
    )
    modified_count = formalization_modified_count_since(start_utc)
    checks.append(
        {
            "check_id": "VAL3458_9_formalization_untouched",
            "description": "formalization-workbench unchanged during this script",
            "passed": modified_count == 0,
            "detail": f"modified_count_since_start={modified_count}",
        }
    )
    overall = all(bool(row["passed"]) for row in checks)
    checks.append(
        {
            "check_id": "VAL3458_10_overall",
            "description": "3458 live action instantiation checkpoint is internally valid",
            "passed": overall,
            "detail": "PASS" if overall else "FAIL",
        }
    )
    return checks


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    lines = [
        "# 3458 - Live MTS Action Instantiation Of Hilbert-Khat Contract Under AX1090",
        "",
        "## Purpose",
        "",
        "This checkpoint tries to instantiate the 3457 parent Hilbert-Khat contract against the actual MTS `Gamma_eff/K_hat/q_loc` ladder. The constructive move is to use the existing response-doublet route as a candidate parent sector and define `K_hat` as the Hilbert response of that sector, not as an independent closure tensor.",
        "",
        "## Source Register",
        "",
        md_table(rows_by_name["source_register"]),
        "",
        "## Live Symbol Map",
        "",
        md_table(rows_by_name["live_symbol_map"]),
        "",
        "## Parent Action Candidate",
        "",
        md_table(rows_by_name["parent_action_candidate"]),
        "",
        "## Contract Instantiation",
        "",
        md_table(rows_by_name["contract_instantiation"]),
        "",
        "## Residual Vector After Instantiation",
        "",
        md_table(rows_by_name["residual_vector_after_instantiation"]),
        "",
        "## Energy Identity Target",
        "",
        md_table(rows_by_name["energy_identity_target"]),
        "",
        "## Decision Ledger",
        "",
        md_table(rows_by_name["decision_ledger"]),
        "",
        "## Next Target",
        "",
        md_table(rows_by_name["next_target"]),
        "",
        "## Validation",
        "",
        md_table(rows_by_name["validation"]),
        "",
        "## Bottom Line",
        "",
        "- The best live construction is now explicit: `Gamma_X` is a response-doublet/positive-operator density and `K_hat := K_H[Gamma_X]` inside that parent branch.",
        "- This would kill the `Delta_K` mismatch by construction, but only if the branch is adopted and old `K_hat` usages are proven compatible or replaced.",
        "- The remaining real work is not vague: prove the doublet energy identity, source-current zero, boundary no-flux, and projector ownership; otherwise emit a quantitative `q_loc` bound.",
        "",
    ]
    DOC.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    start_utc = datetime.now(timezone.utc)
    OUT.mkdir(parents=True, exist_ok=True)
    rows_by_name: dict[str, list[dict[str, Any]]] = {
        "source_register": source_register(),
        "live_symbol_map": live_symbol_map(),
        "parent_action_candidate": parent_action_candidate(),
        "contract_instantiation": contract_instantiation(),
        "residual_vector_after_instantiation": residual_vector_after_instantiation(),
        "energy_identity_target": energy_identity_target(),
        "decision_ledger": decision_rows(),
        "next_target": next_target_rows(),
    }
    output_map = {
        "source_register": OUT / "P8_Y5_R2FR_3458_SOURCE_REGISTER.csv",
        "live_symbol_map": OUT / "P8_Y5_R2FR_3458_LIVE_SYMBOL_MAP.csv",
        "parent_action_candidate": OUT / "P8_Y5_R2FR_3458_PARENT_ACTION_CANDIDATE.csv",
        "contract_instantiation": OUT / "P8_Y5_R2FR_3458_CONTRACT_INSTANTIATION.csv",
        "residual_vector_after_instantiation": OUT / "P8_Y5_R2FR_3458_RESIDUAL_VECTOR_AFTER_INSTANTIATION.csv",
        "energy_identity_target": OUT / "P8_Y5_R2FR_3458_ENERGY_IDENTITY_TARGET.csv",
        "decision_ledger": OUT / "P8_Y5_R2FR_3458_DECISION_LEDGER.csv",
        "next_target": OUT / "P8_Y5_R2FR_3458_NEXT_TARGET.csv",
    }
    for name, path in output_map.items():
        write_csv(path, rows_by_name[name])
    rows_by_name["validation"] = validation_rows(rows_by_name, start_utc)
    write_csv(OUT / "P8_Y5_BRR545_3458_VALIDATION.csv", rows_by_name["validation"])
    write_doc(rows_by_name)
    print(f"wrote {DOC}")
    print("wrote 9 csv outputs")


if __name__ == "__main__":
    main()
