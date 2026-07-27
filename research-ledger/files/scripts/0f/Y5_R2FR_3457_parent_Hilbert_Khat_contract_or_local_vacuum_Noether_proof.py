from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "3457-Y5-R2FR-parent-Hilbert-Khat-contract-or-local-vacuum-Noether-proof-under-AX1090.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"

SOURCES = {
    "script_3457": Path(__file__).resolve(),
    "doc_3456": ROOT / "3456-Y5-R2FR-DeltaK-derivative-Hodge-projector-component-or-bound-fill-under-AX1090.md",
    "route_3456": OUT / "P8_Y5_R2FR_3456_NOETHER_HILBERT_ROUTE.csv",
    "bound_3456": OUT / "P8_Y5_R2FR_3456_QDELTAK_DERIVATIVE_BOUND.csv",
    "claim_3456": OUT / "P8_Y5_R2FR_3456_CLAIM_STATUS.csv",
    "doc_3455": ROOT / "3455-Y5-R2FR-DeltaK-component-ledger-or-q_loc-norm-first-fill-under-AX1090.md",
    "qdelta_3455": OUT / "P8_Y5_R2FR_3455_QDELTAK_NORM_INPUT.csv",
    "typing_3454": OUT / "P8_Y5_R2FR_3454_GK_PLACEHOLDER_TYPING.csv",
    "sign_lock_2975": OUT / "P8_Y5_R2FR_2975_GAMMAKHAT_SIGN_CONVENTION_LOCK.csv",
    "symbol_match_1281": OUT / "P8_Y5_R10_1281_GAMMA_KHAT_SYMBOL_MATCH_AUDIT.csv",
    "variation_2140": OUT / "P8_Y5_PARENT_QLOC_2140_GAMMAG_VARIATION_IDENTITIES.csv",
    "variation_2207": OUT / "P8_Y5_PARENT_QLOC_2207_GAMMA_EFF_METRIC_VARIATION_ATTEMPT.csv",
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
        "script_3457": "generator for this checkpoint",
        "doc_3456": "derivative/Hodge/projector Noether route predecessor",
        "route_3456": "Noether/Hilbert route rows",
        "bound_3456": "q_loc derivative residual bound input",
        "claim_3456": "nonclaim status input",
        "doc_3455": "Delta_K component split predecessor",
        "qdelta_3455": "Q_DeltaK norm input",
        "typing_3454": "Gamma/Khat/q_loc placeholder typing",
        "sign_lock_2975": "canonical T_q, T_metric and Delta_K sign convention",
        "symbol_match_1281": "Khat/Hilbert symbol match gap",
        "variation_2140": "metric variation identities and countermodels",
        "variation_2207": "Gamma_eff metric variation attempt",
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


def noether_theorem_rows() -> list[dict[str, Any]]:
    return [
        {
            "theorem_id": "NHT3457_0_parent_action_setup",
            "statement": "Let S_X[g,Phi]=integral_U sqrt(-g) Gamma_X(g,Phi,D Phi,star_g,P_loc) plus B_X be a diffeomorphism-invariant parent sector with tensorial fields and declared boundary data.",
            "derivation_step": "Define the Hilbert response K_H^{mu nu} by delta_g S_X = one_half integral sqrt(-g)(Gamma_X g^{mu nu}-K_H^{mu nu}) delta g_{mu nu} plus boundary terms plus field-equation terms.",
            "condition_type": "ASSUMPTION_CONTRACT",
            "current_status": "NOT_YET_INSTANTIATED_FOR_MTS",
            "source_path": str(SOURCES["doc_3456"]),
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "theorem_id": "NHT3457_1_diffeomorphism_variation",
            "statement": "For a compactly supported vector xi, diffeomorphism invariance gives delta_xi S_X=0 with delta_xi g_{mu nu}=nabla_mu xi_nu+nabla_nu xi_mu and delta_xi Phi^A=Lie_xi Phi^A.",
            "derivation_step": "Integrating by parts isolates xi_nu and yields nabla_mu(Gamma_X g^{mu nu}-K_H^{mu nu}) = J_E^nu + J_B^nu, where J_E is the field-equation current and J_B is the boundary/reference current.",
            "condition_type": "DERIVED_NOETHER_IDENTITY",
            "current_status": "FORMAL_ROUTE_ESTABLISHED",
            "source_path": str(SOURCES["variation_2140"]),
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "theorem_id": "NHT3457_2_q_loc_identity",
            "statement": "Using T_X^{mu nu}=Gamma_X g^{mu nu}-K_H^{mu nu}, the local force candidate is q_H^nu := nabla^nu Gamma_X - nabla_mu K_H^{mu nu} = J_E^nu + J_B^nu.",
            "derivation_step": "Because nabla_mu(Gamma_X g^{mu nu})=nabla^nu Gamma_X for metric-compatible GR geometry, q_H is exactly the Noether residual.",
            "condition_type": "DERIVED_QLOC_IDENTITY",
            "current_status": "EXACT_IF_KHAT_EQUALS_KH",
            "source_path": str(SOURCES["sign_lock_2975"]),
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "theorem_id": "NHT3457_3_Khat_mismatch_identity",
            "statement": "For the live MTS object K_hat, write Delta_K^{mu nu}=K_hat^{mu nu}-K_H^{mu nu}. Then q_hat^nu = q_H^nu - nabla_mu Delta_K^{mu nu}.",
            "derivation_step": "This makes the obstruction exact: failure of local silence is not vague; it is field-equation current plus boundary current minus Khat/Hilbert mismatch divergence.",
            "condition_type": "DERIVED_RESIDUAL_VECTOR",
            "current_status": "ACTIONABLE_RESIDUAL_FORM",
            "source_path": str(SOURCES["qdelta_3455"]),
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "theorem_id": "NHT3457_4_local_vacuum_zero",
            "statement": "If E_A=0 in the local vacuum branch, boundary/reference flux vanishes, P_loc is linear with P_loc(0)=0, and K_hat=K_H, then q_loc^nu=P_loc q_hat^nu=0.",
            "derivation_step": "This is the exact local-vacuum plateau mechanism, but as a Noether consequence rather than a plateau axiom.",
            "condition_type": "CONDITIONAL_ZERO_THEOREM",
            "current_status": "CLAUSE_DEPENDENT_NOT_CLAIMED",
            "source_path": str(SOURCES["route_3456"]),
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def parent_contract_rows() -> list[dict[str, Any]]:
    return [
        {
            "clause_id": "PHK3457_0_action_scalar_density",
            "contract_clause": "Gamma_X must be a scalar under diffeomorphisms and sqrt(-g) Gamma_X plus B_X must define a scalar density.",
            "why_needed": "Noether conservation does not exist without covariance.",
            "failure_mode": "coordinate-dependent or background-fixed terms generate uncontrolled local force residuals",
            "mts_status": "OPEN",
            "required_next_evidence": "explicit parent action line for Gamma_eff sector",
            "source_path": str(SOURCES["typing_3454"]),
            "valid_for_claim": False,
        },
        {
            "clause_id": "PHK3457_1_transforming_fields",
            "contract_clause": "Every active field, memory tensor, projector and kernel must have a declared Lie derivative or be explicitly external.",
            "why_needed": "The field-equation current J_E^nu cannot be computed unless Lie_xi Phi^A is known.",
            "failure_mode": "hidden background structure can fake a force or break conservation",
            "mts_status": "OPEN",
            "required_next_evidence": "field transformation table for Phi, Gamma, Khat, P_loc and memory variables",
            "source_path": str(SOURCES["route_3456"]),
            "valid_for_claim": False,
        },
        {
            "clause_id": "PHK3457_2_Khat_definition",
            "contract_clause": "K_hat^{mu nu} must be defined as K_H^{mu nu}: the full Hilbert metric response of Gamma_X, including connection, Hodge, projector and boundary-improvement pieces.",
            "why_needed": "This is the only clean way to make Delta_K vanish without an ad hoc closure.",
            "failure_mode": "if K_hat is independent, q_loc carries -nabla_mu Delta_K^{mu nu} and must be bounded by PPN/R10/clocks/orbits",
            "mts_status": "LIVE_MAIN_GAP",
            "required_next_evidence": "explicit variational definition or component equality proof",
            "source_path": str(SOURCES["symbol_match_1281"]),
            "valid_for_claim": False,
        },
        {
            "clause_id": "PHK3457_3_local_on_shell_branch",
            "contract_clause": "The local vacuum branch must satisfy E_A=0 or a screened/bounded projected field-equation current P_loc J_E^nu.",
            "why_needed": "Noether gives zero divergence only on shell.",
            "failure_mode": "off-shell memory/source defects become measurable fifth-force or PPN residuals",
            "mts_status": "OPEN",
            "required_next_evidence": "local field equation, screening theorem or source-backed residual bound",
            "source_path": str(SOURCES["variation_2207"]),
            "valid_for_claim": False,
        },
        {
            "clause_id": "PHK3457_4_boundary_reference_class",
            "contract_clause": "Boundary/reference/corner terms must be fixed, vanish, or be included in K_hat as an improvement.",
            "why_needed": "Integration-by-parts currents are physical unless killed by the branch contract.",
            "failure_mode": "surface flux remains as an unaccounted local force",
            "mts_status": "OPEN",
            "required_next_evidence": "compact-support, no-flux or improvement-term proof",
            "source_path": str(SOURCES["doc_3455"]),
            "valid_for_claim": False,
        },
        {
            "clause_id": "PHK3457_5_projector_linearity",
            "contract_clause": "P_loc must be linear and must preserve zero pointwise, or its metric/domain variation must be inside K_hat.",
            "why_needed": "Projection should not create force from a zero Noether divergence.",
            "failure_mode": "averaging or observational weights become hidden coupling terms",
            "mts_status": "CONDITIONAL_SIMPLE_IF_POINTWISE",
            "required_next_evidence": "P_loc definition and domain metric-dependence classification",
            "source_path": str(SOURCES["bound_3456"]),
            "valid_for_claim": False,
        },
    ]


def local_residual_vector_rows() -> list[dict[str, Any]]:
    return [
        {
            "residual_id": "LRV3457_0_exact_vector",
            "quantity": "q_loc^nu",
            "exact_form": "q_loc^nu = P_loc[J_E^nu + J_B^nu - nabla_mu Delta_K^{mu nu}]",
            "zero_route": "J_E=0, J_B=0, Delta_K=0 and P_loc(0)=0",
            "bound_form": "NORM(q_loc) <= NORM(P_loc J_E) + NORM(P_loc J_B) + NORM(P_loc nabla Delta_K)",
            "status": "EXACT_RESIDUAL_VECTOR_READY",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "residual_id": "LRV3457_1_field_equation_current",
            "quantity": "J_E^nu",
            "exact_form": "J_E^nu is built from Euler-Lagrange operators contracted with Lie-derivative generators of active fields",
            "zero_route": "all active local fields on shell or screened",
            "bound_form": "NORM(P_loc J_E) requires local field equations and source profile",
            "status": "OPEN_PARENT_FIELD_EQUATIONS",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "residual_id": "LRV3457_2_boundary_current",
            "quantity": "J_B^nu",
            "exact_form": "J_B^nu collects boundary, reference, corner and integration-by-parts flux terms",
            "zero_route": "compact support, no-flux boundary, fixed reference class or signed improvement term",
            "bound_form": "NORM(P_loc J_B) requires boundary class and domain scale",
            "status": "OPEN_BOUNDARY_CLASS",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "residual_id": "LRV3457_3_Khat_mismatch",
            "quantity": "Delta_K^{mu nu}",
            "exact_form": "Delta_K^{mu nu}=K_hat^{mu nu}-K_H^{mu nu}",
            "zero_route": "K_hat is defined by Hilbert variation of the same parent action sector",
            "bound_form": "NORM(P_loc nabla_mu Delta_K^{mu nu}) <= Q_metric + Q_derivative + Q_boundary + Q_functional",
            "status": "LIVE_MAIN_GAP_BUT_NOW_EXACT",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def local_gr_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "LGG3457_0_exact_zero_not_claimed",
            "gate": "local q_loc zero",
            "pass_condition": "PHK3457_0 through PHK3457_5 all signed, then LRV3457_0 zero route applies",
            "current_result": "FAIL_OPEN",
            "reason": "K_hat Hilbert definition, local field equations and boundary class are still unsigned",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "LGG3457_1_ppn_branch",
            "gate": "PPN residual suppression",
            "pass_condition": "Either q_loc=0 theorem or numeric bounds on J_E, J_B and Delta_K below PPN thresholds",
            "current_result": "NOT_READY",
            "reason": "exact residual vector exists but no numeric source rows yet",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "LGG3457_2_best_path",
            "gate": "least-scrutiny route",
            "pass_condition": "Define K_hat from the parent action rather than fitting it as an independent closure object",
            "current_result": "RECOMMENDED",
            "reason": "This mirrors GR's covariance-to-conservation logic and preserves wave/Poynting stress honestly",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3457_0_project_status",
            "decision": "The local-GR problem is no longer formless. It has collapsed to a parent-action contract plus three residuals: field-equation current, boundary current and Khat/Hilbert mismatch.",
            "meaning": "This is genuine progress toward derivability, but not yet a local-GR claim.",
            "next_action": "Attempt to instantiate the contract using the live MTS action notation; if not possible, create source-ready residual bounds for J_E, J_B and Delta_K.",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_doc": "3458-Y5-R2FR-live-MTS-action-instantiation-of-Hilbert-Khat-contract-under-AX1090.md",
            "next_script": "scripts/Y5_R2FR_3458_live_MTS_action_instantiation_of_Hilbert_Khat_contract.py",
            "objective": "Map the actual live MTS Gamma_eff/K_hat notation onto the 3457 parent contract. Try to define K_hat as Hilbert response; if impossible, output the minimal residual sources J_E, J_B and Delta_K.",
            "success_gate": "Either parent-owned K_hat=K_H proof, or a concrete residual table with no vague missing-input language.",
            "valid_for_claim": False,
            "claim_allowed": False,
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
    theorem_rows = rows_by_name["noether_theorem"]
    contract_rows = rows_by_name["parent_contract"]
    residual_rows = rows_by_name["local_residual_vector"]
    gate_rows = rows_by_name["local_gr_gates"]
    next_rows = rows_by_name["next_target"]

    generated_paths = [
        OUT / "P8_Y5_R2FR_3457_SOURCE_REGISTER.csv",
        OUT / "P8_Y5_R2FR_3457_NOETHER_THEOREM.csv",
        OUT / "P8_Y5_R2FR_3457_PARENT_HILBERT_KHAT_CONTRACT.csv",
        OUT / "P8_Y5_R2FR_3457_LOCAL_QLOC_RESIDUAL_VECTOR.csv",
        OUT / "P8_Y5_R2FR_3457_LOCAL_GR_GATES.csv",
        OUT / "P8_Y5_R2FR_3457_DECISION_LEDGER.csv",
        OUT / "P8_Y5_R2FR_3457_NEXT_TARGET.csv",
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

    required_contracts = {
        "PHK3457_0_action_scalar_density",
        "PHK3457_1_transforming_fields",
        "PHK3457_2_Khat_definition",
        "PHK3457_3_local_on_shell_branch",
        "PHK3457_4_boundary_reference_class",
        "PHK3457_5_projector_linearity",
    }
    present_contracts = {str(row["clause_id"]) for row in contract_rows}

    checks: list[dict[str, Any]] = []
    checks.append(
        {
            "check_id": "VAL3457_0_sources_exist",
            "description": "all source paths exist",
            "passed": all(bool(row["exists"]) for row in source_rows),
            "detail": f"{sum(1 for row in source_rows if row['exists'])}/{len(source_rows)} source paths exist",
        }
    )
    checks.append(
        {
            "check_id": "VAL3457_1_noether_theorem_shape",
            "description": "theorem includes setup, diffeo identity, q_loc identity, mismatch and zero theorem",
            "passed": {row["theorem_id"] for row in theorem_rows} == {
                "NHT3457_0_parent_action_setup",
                "NHT3457_1_diffeomorphism_variation",
                "NHT3457_2_q_loc_identity",
                "NHT3457_3_Khat_mismatch_identity",
                "NHT3457_4_local_vacuum_zero",
            },
            "detail": ";".join(row["theorem_id"] for row in theorem_rows),
        }
    )
    checks.append(
        {
            "check_id": "VAL3457_2_contract_complete",
            "description": "parent Hilbert-Khat contract has all required clauses",
            "passed": required_contracts.issubset(present_contracts),
            "detail": ";".join(sorted(present_contracts)),
        }
    )
    checks.append(
        {
            "check_id": "VAL3457_3_residual_vector_exact",
            "description": "q_loc residual vector is exact and decomposed",
            "passed": any(
                row["residual_id"] == "LRV3457_0_exact_vector"
                and "J_E^nu + J_B^nu - nabla_mu Delta_K" in str(row["exact_form"])
                for row in residual_rows
            )
            and {"LRV3457_1_field_equation_current", "LRV3457_2_boundary_current", "LRV3457_3_Khat_mismatch"}.issubset(
                {row["residual_id"] for row in residual_rows}
            ),
            "detail": ";".join(row["residual_id"] for row in residual_rows),
        }
    )
    checks.append(
        {
            "check_id": "VAL3457_4_no_claims",
            "description": "local GR/PPN remains unclaimed",
            "passed": all(str(row.get("claim_allowed", "False")) == "False" for row in theorem_rows + residual_rows + gate_rows),
            "detail": "claim_allowed=false across theorem, residual and gate rows",
        }
    )
    checks.append(
        {
            "check_id": "VAL3457_5_csv_parse",
            "description": "generated CSV files parse cleanly",
            "passed": csv_parse_ok,
            "detail": ";".join(csv_details),
        }
    )
    checks.append(
        {
            "check_id": "VAL3457_6_next_target_3458",
            "description": "next target is live MTS action instantiation",
            "passed": len(next_rows) == 1 and "3458-Y5-R2FR-live-MTS-action-instantiation" in str(next_rows[0]["next_doc"]),
            "detail": str(next_rows[0]["next_doc"]) if next_rows else "missing next row",
        }
    )
    modified_count = formalization_modified_count_since(start_utc)
    checks.append(
        {
            "check_id": "VAL3457_7_formalization_untouched",
            "description": "formalization-workbench unchanged during this script",
            "passed": modified_count == 0,
            "detail": f"modified_count_since_start={modified_count}",
        }
    )
    overall = all(bool(row["passed"]) for row in checks)
    checks.append(
        {
            "check_id": "VAL3457_8_overall",
            "description": "3457 parent Hilbert-Khat contract checkpoint is internally valid",
            "passed": overall,
            "detail": "PASS" if overall else "FAIL",
        }
    )
    return checks


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    lines = [
        "# 3457 - Parent Hilbert-Khat Contract Or Local-Vacuum Noether Proof Under AX1090",
        "",
        "## Purpose",
        "",
        "This checkpoint turns the 3456 Noether/Hilbert route into an exact contract. The result is simple and important: if the parent action is diffeomorphism invariant and `K_hat` is the Hilbert metric response, local `q_loc` silence follows on shell up to boundary terms. If not, the failure is an explicit residual vector, not a vague missing ingredient.",
        "",
        "## Source Register",
        "",
        md_table(rows_by_name["source_register"]),
        "",
        "## Noether Theorem",
        "",
        md_table(rows_by_name["noether_theorem"]),
        "",
        "## Parent Hilbert-Khat Contract",
        "",
        md_table(rows_by_name["parent_contract"]),
        "",
        "## Local q_loc Residual Vector",
        "",
        md_table(rows_by_name["local_residual_vector"]),
        "",
        "## Local GR Gates",
        "",
        md_table(rows_by_name["local_gr_gates"]),
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
        "- The clean derivation route is now explicit: covariance plus Hilbert `K_hat` plus on-shell local vacuum gives `q_loc=0`.",
        "- The project has not claimed local GR yet, because the live MTS notation has not been instantiated into the contract.",
        "- The next target is not another generic audit. It is a direct map from live `Gamma_eff/K_hat` notation to `K_hat=K_H`, or a concrete residual vector if that map fails.",
        "",
    ]
    DOC.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    start_utc = datetime.now(timezone.utc)
    OUT.mkdir(parents=True, exist_ok=True)
    rows_by_name: dict[str, list[dict[str, Any]]] = {
        "source_register": source_register(),
        "noether_theorem": noether_theorem_rows(),
        "parent_contract": parent_contract_rows(),
        "local_residual_vector": local_residual_vector_rows(),
        "local_gr_gates": local_gr_gate_rows(),
        "decision_ledger": decision_rows(),
        "next_target": next_target_rows(),
    }
    output_map = {
        "source_register": OUT / "P8_Y5_R2FR_3457_SOURCE_REGISTER.csv",
        "noether_theorem": OUT / "P8_Y5_R2FR_3457_NOETHER_THEOREM.csv",
        "parent_contract": OUT / "P8_Y5_R2FR_3457_PARENT_HILBERT_KHAT_CONTRACT.csv",
        "local_residual_vector": OUT / "P8_Y5_R2FR_3457_LOCAL_QLOC_RESIDUAL_VECTOR.csv",
        "local_gr_gates": OUT / "P8_Y5_R2FR_3457_LOCAL_GR_GATES.csv",
        "decision_ledger": OUT / "P8_Y5_R2FR_3457_DECISION_LEDGER.csv",
        "next_target": OUT / "P8_Y5_R2FR_3457_NEXT_TARGET.csv",
    }
    for name, path in output_map.items():
        write_csv(path, rows_by_name[name])
    rows_by_name["validation"] = validation_rows(rows_by_name, start_utc)
    write_csv(OUT / "P8_Y5_BRR545_3457_VALIDATION.csv", rows_by_name["validation"])
    write_doc(rows_by_name)
    print(f"wrote {DOC}")
    print("wrote 8 csv outputs")


if __name__ == "__main__":
    main()
