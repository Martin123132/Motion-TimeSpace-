from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "3456-Y5-R2FR-DeltaK-derivative-Hodge-projector-component-or-bound-fill-under-AX1090.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"

SOURCES = {
    "script_3456": Path(__file__).resolve(),
    "doc_3455": ROOT / "3455-Y5-R2FR-DeltaK-component-ledger-or-q_loc-norm-first-fill-under-AX1090.md",
    "component_3455": OUT / "P8_Y5_R2FR_3455_DELTAK_COMPONENT_LEDGER.csv",
    "qdelta_3455": OUT / "P8_Y5_R2FR_3455_QDELTAK_NORM_INPUT.csv",
    "doc_3454": ROOT / "3454-Y5-R2FR-Gamma-Khat-q_loc-placeholder-typing-or-first-active-LX-bound-under-AX1090.md",
    "sign_lock_2975": OUT / "P8_Y5_R2FR_2975_GAMMAKHAT_SIGN_CONVENTION_LOCK.csv",
    "metric_response_776": OUT / "P8_Y5_R10_776_KGAMMA_METRIC_RESPONSE_LEDGER.csv",
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
    body = []
    for row in rows:
        vals = []
        for field in fields:
            vals.append(str(row.get(field, "")).replace("\n", "<br>").replace("|", "/"))
        body.append("| " + " | ".join(vals) + " |")
    return "\n".join([header, sep, *body])


def source_register() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for key, path in SOURCES.items():
        rows.append(
            {
                "timestamp_utc": datetime.now(timezone.utc).isoformat(),
                "source_id": key,
                "path": str(path),
                "exists": path.exists(),
                "role": {
                    "script_3456": "generator for this checkpoint",
                    "doc_3455": "immediate parent component split",
                    "component_3455": "Delta_K component ledger input",
                    "qdelta_3455": "Q_DeltaK component-sum input",
                    "doc_3454": "Gamma/Khat/q_loc typing predecessor",
                    "sign_lock_2975": "canonical T_q, T_metric and Delta_K sign convention",
                    "metric_response_776": "older K_Gamma metric-response ledger",
                    "symbol_match_1281": "Gamma/Khat symbol-match audit",
                    "variation_2140": "metric variation identities and countermodels",
                    "variation_2207": "Gamma_eff response attempt and parent-signature gap",
                }[key],
            }
        )
    return rows


def derivative_response_identity() -> list[dict[str, Any]]:
    return [
        {
            "identity_id": "DRI3456_0_derivative_sector_template",
            "object": "Gamma_der[g,Phi,P_loc]",
            "derived_statement": "Use a general local derivative sector Gamma_der = L_der(g, Phi, D Phi, star_g, P_loc, boundary data). This captures connection, Hodge and projector dependence without pretending the exact MTS parent formula is already signed.",
            "mathematical_role": "template not claim",
            "zero_condition": "none",
            "live_residual": "all metric-response terms unless the parent action supplies the exact L_der and K_hat definition",
            "source_path": str(SOURCES["doc_3455"]),
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "identity_id": "DRI3456_1_metric_variation_split",
            "object": "delta_g Gamma_der",
            "derived_statement": "delta_g Gamma_der splits into explicit metric terms, connection terms from delta_g(D Phi), Hodge or index-raising terms from delta_g star_g, projector/domain terms from delta_g P_loc, and a boundary current after integrations by parts.",
            "mathematical_role": "DERIVED_VARIATIONAL_DECOMPOSITION",
            "zero_condition": "every split term must either be metric-silent, matched by K_hat, or converted into a controlled boundary flux",
            "live_residual": "Q_conn plus Q_star plus Q_projector plus Q_boundary plus Q_Kmatch",
            "source_path": str(SOURCES["metric_response_776"]),
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "identity_id": "DRI3456_2_connection_subcase",
            "object": "delta_g(D Phi)",
            "derived_statement": "If the derivative is an exterior derivative on metric-independent p-form fields, the connection variation part is zero. If D is a covariant derivative on tensor slots, delta Gamma acts through the representation generators and is generally nonzero before Hilbert matching.",
            "mathematical_role": "CONDITIONAL_ZERO_BRANCH_PLUS_COUNTERBRANCH",
            "zero_condition": "exterior/scalar derivative branch or vanishing representation-generator contraction",
            "live_residual": "Q_conn",
            "source_path": str(SOURCES["variation_2140"]),
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "identity_id": "DRI3456_3_hodge_subcase",
            "object": "delta_g star_g",
            "derived_statement": "Hodge-star and index-raising dependence is not silent for Maxwell-like or wave-energy terms; it is precisely the channel that carries stress, flux and Poynting-vector information. It should be matched and conserved, not erased.",
            "mathematical_role": "PHYSICAL_STRESS_CHANNEL",
            "zero_condition": "topological metric-free term such as a wedge-without-star density, null/on-shell averaged zero, or parent theorem setting the derivative density to zero",
            "live_residual": "Q_star",
            "source_path": str(SOURCES["metric_response_776"]),
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "identity_id": "DRI3456_4_projector_domain_subcase",
            "object": "delta_g P_loc and domain measure",
            "derived_statement": "A local projector or observational domain can carry metric dependence through volume, normal, slicing, Green kernel or averaging weights. That dependence must either be external/fixed, quotient-invariant, or included in K_hat.",
            "mathematical_role": "PROJECTOR_ACCOUNTING_GATE",
            "zero_condition": "P_loc fixed under metric variation or parent proves quotient-invariant projector descent",
            "live_residual": "Q_projector",
            "source_path": str(SOURCES["component_3455"]),
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "identity_id": "DRI3456_5_boundary_subcase",
            "object": "Theta_der_boundary",
            "derived_statement": "Integration by parts moves delta-connection derivatives onto momenta and leaves a boundary current. Local-vacuum silence requires compact support, fixed boundary data, no-flux boundary class, or a signed improvement term.",
            "mathematical_role": "BOUNDARY_IMPROVEMENT_GATE",
            "zero_condition": "Theta_der dot n = 0 or boundary improvement cancels the flux",
            "live_residual": "Q_boundary",
            "source_path": str(SOURCES["component_3455"]),
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def noether_hilbert_route() -> list[dict[str, Any]]:
    return [
        {
            "route_id": "NHR3456_0_core_identity",
            "contract_clause": "diffeomorphism invariant parent density",
            "required_statement": "For S_X = integral sqrt(-g) Gamma_X, with all fields and projectors transforming tensorially, the Hilbert tensor T_X^{mu nu}=Gamma_X g^{mu nu}-K_X^{mu nu} obeys a Noether identity whose divergence is proportional to field equations plus boundary flux.",
            "local_consequence": "If Euler-Lagrange terms and boundary flux vanish, nabla_mu T_X^{mu nu}=0, hence nabla^nu Gamma_X - nabla_mu K_X^{mu nu}=0.",
            "current_status": "DERIVED_ROUTE_NOT_PARENT_SIGNED",
            "missing_input": "signed parent action and transformation law for every live field/projector",
            "source_path": str(SOURCES["variation_2140"]),
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "route_id": "NHR3456_1_Khat_match",
            "contract_clause": "K_hat equals Hilbert metric response",
            "required_statement": "K_hat_der^{mu nu} must be defined as the full Hilbert response of Gamma_der, including explicit metric, connection, Hodge, projector and boundary-improvement terms.",
            "local_consequence": "Delta_K_derivative = K_hat_der - K_metric_der = 0 by definition only if this equality is parent-owned, not fitted after the fact.",
            "current_status": "LIVE_MAIN_GAP",
            "missing_input": "explicit K_hat formula or variational definition in the parent action",
            "source_path": str(SOURCES["symbol_match_1281"]),
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "route_id": "NHR3456_2_on_shell_local_vacuum",
            "contract_clause": "local Euler-Lagrange silence",
            "required_statement": "The derivative-sector field equations E_A=0 must hold in the local vacuum branch, or their projected force density must be bounded.",
            "local_consequence": "q_loc^{nu}=P_loc(nabla_mu T_X^{mu nu}) is zero only on shell; off-shell defects become explicit residual inputs.",
            "current_status": "OPEN_BUT_NOW_FORMULATED",
            "missing_input": "local-vacuum field equation or source-screening theorem",
            "source_path": str(SOURCES["variation_2207"]),
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "route_id": "NHR3456_3_boundary_silence",
            "contract_clause": "boundary and reference class fixed",
            "required_statement": "All integration-by-parts and reference-subtraction currents must vanish under the local branch boundary class or be canceled by a declared improvement term.",
            "local_consequence": "No hidden surface force is allowed to masquerade as local GR recovery.",
            "current_status": "OPEN_BOUNDARY_GATE",
            "missing_input": "fixed boundary class, no-flux theorem, or explicit counterterm",
            "source_path": str(SOURCES["component_3455"]),
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "route_id": "NHR3456_4_projector_preserves_zero",
            "contract_clause": "P_loc does not create force from a zero divergence",
            "required_statement": "If nabla_mu T_X^{mu nu}=0 pointwise, P_loc must be linear and local enough that P_loc(0)=0; if P_loc involves metric-dependent averaging, its variation belongs in K_hat or the residual bound.",
            "local_consequence": "Projection cannot be used to smuggle in or hide a force term.",
            "current_status": "CONDITIONAL_SIMPLE_IF_POINTWISE_ZERO",
            "missing_input": "P_loc definition for non-pointwise or averaged branches",
            "source_path": str(SOURCES["qdelta_3455"]),
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def qDeltaK_derivative_bound() -> list[dict[str, Any]]:
    return [
        {
            "bound_id": "QDB3456_0_derivative_component_sum",
            "parent_bound": "QDK3455_0_component_sum",
            "quantity": "Q_DeltaK_derivative",
            "formula": "Q_DeltaK_derivative <= Q_conn + Q_star + Q_projector + Q_boundary + Q_Kmatch",
            "filled_part": "connection exterior-derivative subcase can set Q_conn=0 only for metric-independent scalar/p-form exterior derivative branches",
            "still_missing": "Q_star;Q_projector;Q_boundary;Q_Kmatch;live parent derivative formula",
            "units": "force-density or stress-divergence units before PPN normalization",
            "status": "PARTIAL_BOUND_FILLED_NOT_NUMERIC",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "bound_id": "QDB3456_1_noether_route_bound",
            "parent_bound": "GKB3454_0_q_loc_norm_bound",
            "quantity": "q_loc_derivative",
            "formula": "If K_hat=K_Hilbert and E_A=0 and boundary flux=0 then q_loc_derivative=0; otherwise NORM(q_loc_derivative) <= NORM(E_A grad Phi^A) + Q_boundary + Q_Kmatch + Q_projector",
            "filled_part": "exact zero theorem route identified",
            "still_missing": "parent-signed K_Hilbert equality; local E_A=0 proof; boundary class",
            "units": "force-density projected into local observable sector",
            "status": "DERIVED_ZERO_ROUTE_WITH_UNSIGNED_CLAUSES",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "bound_id": "QDB3456_2_ppn_envelope_update",
            "parent_bound": "QDK3455_1_ppn_gamma_envelope",
            "quantity": "delta gamma_PPN derivative residual",
            "formula": "abs(delta gamma_PPN)_der <= c^2 N_G N_D Q_DeltaK_derivative divided by 2 U_min",
            "filled_part": "derivative residual now decomposed into measurable or theorem-zero subinputs",
            "still_missing": "U_min;N_G;N_D;numeric or theorem-zero value for all subinputs",
            "units": "dimensionless",
            "status": "SYMBOLIC_ENVELOPE_REFINED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def claim_status() -> list[dict[str, Any]]:
    return [
        {
            "status_id": "CS3456_0_derivation_progress",
            "question": "Did 3456 move beyond a missing-input ledger?",
            "answer": "Yes. It identifies the GR-style Noether/Hilbert route: derivative, Hodge, projector and Poynting-like stress terms need not vanish individually; their Hilbert stress divergence vanishes on shell if the parent action is diffeomorphism invariant.",
            "verdict": "REAL_DERIVATION_ROUTE_FOUND",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "status_id": "CS3456_1_local_GR_claim",
            "question": "Can local GR/PPN be claimed now?",
            "answer": "No. The route is exact only after K_hat is parent-signed as the Hilbert response, local field equations are imposed, and boundary/projector clauses close.",
            "verdict": "CLAIM_BLOCKED_BUT_TARGET_NARROWED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "status_id": "CS3456_2_physics_read",
            "question": "What does this imply for waves, EM-like flow and Poynting-vector intuitions?",
            "answer": "Those channels are not embarrassments to hide. Maxwell-like Hodge stress and Poynting flux are exactly the sort of derivative stress that should be carried by K_hat and conserved through the Noether identity.",
            "verdict": "PRESERVE_AS_STRESS_CHANNEL_NOT_ZERO_AXIOM",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def decision_ledger() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3456_0_best_route",
            "decision": "Stop trying to kill every derivative/Hodge term separately. Instead require K_hat to be the Hilbert response of a diffeomorphism-invariant parent sector and use the Noether identity for q_loc silence.",
            "why": "This is closer to how GR gets conservation from covariance and avoids an artificial plateau axiom.",
            "risk": "If K_hat remains an independent closure object, Delta_K remains a real residual and must be bounded experimentally.",
            "next_action": "Write the parent Hilbert-Khat contract and attempt to instantiate it for the live Gamma_eff/K_hat symbols.",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def next_target() -> list[dict[str, Any]]:
    return [
        {
            "next_doc": "3457-Y5-R2FR-parent-Hilbert-Khat-contract-or-local-vacuum-Noether-proof-under-AX1090.md",
            "next_script": "scripts/Y5_R2FR_3457_parent_Hilbert_Khat_contract_or_local_vacuum_Noether_proof.py",
            "objective": "Turn the Noether/Hilbert route into an exact parent-action contract for K_hat and q_loc. Either instantiate K_hat as the Hilbert metric response or leave a sharply bounded Delta_K residual.",
            "input_rows": "NHR3456_0_core_identity;NHR3456_1_Khat_match;QDB3456_1_noether_route_bound",
            "success_gate": "A signed contract showing K_hat=K_Hilbert and q_loc=0 on shell, or a minimal residual vector with source-ready bounds.",
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
    identity_rows = rows_by_name["derivative_response_identity"]
    route_rows = rows_by_name["noether_hilbert_route"]
    bound_rows = rows_by_name["qDeltaK_derivative_bound"]
    status_rows = rows_by_name["claim_status"]
    next_rows = rows_by_name["next_target"]

    generated_paths = [
        OUT / "P8_Y5_R2FR_3456_SOURCE_REGISTER.csv",
        OUT / "P8_Y5_R2FR_3456_DERIVATIVE_RESPONSE_IDENTITY.csv",
        OUT / "P8_Y5_R2FR_3456_NOETHER_HILBERT_ROUTE.csv",
        OUT / "P8_Y5_R2FR_3456_QDELTAK_DERIVATIVE_BOUND.csv",
        OUT / "P8_Y5_R2FR_3456_CLAIM_STATUS.csv",
        OUT / "P8_Y5_R2FR_3456_DECISION_LEDGER.csv",
        OUT / "P8_Y5_R2FR_3456_NEXT_TARGET.csv",
    ]
    csv_parse_ok = True
    csv_parse_detail: list[str] = []
    for path in generated_paths:
        try:
            parsed = read_csv(path)
            csv_parse_detail.append(f"{path.name}:{len(parsed)}")
        except Exception as exc:
            csv_parse_ok = False
            csv_parse_detail.append(f"{path.name}:{exc}")

    required_route_clauses = {
        "diffeomorphism invariant parent density",
        "K_hat equals Hilbert metric response",
        "local Euler-Lagrange silence",
        "boundary and reference class fixed",
        "P_loc does not create force from a zero divergence",
    }
    present_clauses = {str(row["contract_clause"]) for row in route_rows}

    checks: list[dict[str, Any]] = []
    checks.append(
        {
            "check_id": "VAL3456_0_sources_exist",
            "description": "all source paths exist",
            "passed": all(bool(row["exists"]) for row in source_rows),
            "detail": f"{sum(1 for row in source_rows if row['exists'])}/{len(source_rows)} source paths exist",
        }
    )
    checks.append(
        {
            "check_id": "VAL3456_1_variational_split_present",
            "description": "derivative/Hodge/projector/boundary split is present",
            "passed": all(
                any(needle in str(row["live_residual"]) or needle in str(row["object"]) for row in identity_rows)
                for needle in ["Q_conn", "Q_star", "Q_projector", "Q_boundary"]
            ),
            "detail": ";".join(row["identity_id"] for row in identity_rows),
        }
    )
    checks.append(
        {
            "check_id": "VAL3456_2_noether_route_contract",
            "description": "Noether/Hilbert route has all required clauses",
            "passed": required_route_clauses.issubset(present_clauses),
            "detail": ";".join(sorted(present_clauses)),
        }
    )
    checks.append(
        {
            "check_id": "VAL3456_3_qDeltaK_derivative_bound",
            "description": "derivative residual bound is refined and nonclaim",
            "passed": any(
                row["bound_id"] == "QDB3456_0_derivative_component_sum"
                and "Q_conn + Q_star + Q_projector + Q_boundary + Q_Kmatch" in str(row["formula"])
                and str(row["valid_for_claim"]) == "False"
                for row in bound_rows
            ),
            "detail": ";".join(row["bound_id"] for row in bound_rows),
        }
    )
    checks.append(
        {
            "check_id": "VAL3456_4_no_local_GR_claim",
            "description": "local GR/PPN remains blocked",
            "passed": all(str(row["claim_allowed"]) == "False" for row in status_rows + bound_rows + route_rows),
            "detail": "claim_allowed=false across route, bound and status rows",
        }
    )
    checks.append(
        {
            "check_id": "VAL3456_5_generated_csv_parse",
            "description": "generated CSV files parse cleanly",
            "passed": csv_parse_ok,
            "detail": ";".join(csv_parse_detail),
        }
    )
    checks.append(
        {
            "check_id": "VAL3456_6_next_target_3457",
            "description": "next target is parent Hilbert-Khat contract",
            "passed": len(next_rows) == 1 and "3457-Y5-R2FR-parent-Hilbert-Khat-contract" in str(next_rows[0]["next_doc"]),
            "detail": str(next_rows[0]["next_doc"]) if next_rows else "missing next row",
        }
    )
    modified_count = formalization_modified_count_since(start_utc)
    checks.append(
        {
            "check_id": "VAL3456_7_formalization_untouched",
            "description": "formalization-workbench unchanged during this script",
            "passed": modified_count == 0,
            "detail": f"modified_count_since_start={modified_count}",
        }
    )
    overall = all(bool(row["passed"]) for row in checks)
    checks.append(
        {
            "check_id": "VAL3456_8_overall",
            "description": "3456 derivative/Hodge/projector checkpoint is internally valid",
            "passed": overall,
            "detail": "PASS" if overall else "FAIL",
        }
    )
    return checks


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    lines = [
        "# 3456 - DeltaK Derivative/Hodge/Projector Component Or Bound Fill Under AX1090",
        "",
        "## Purpose",
        "",
        "This checkpoint attacks the live `DKC3455_2_derivative_connection_hodge` obstruction directly. The move is not to force every derivative, Hodge, wave, or projector term to vanish. The GR-style route is sharper: if the parent sector is diffeomorphism invariant and `K_hat` is the full Hilbert metric response, then the divergence of `Gamma_eff g^{mu nu}-K_hat^{mu nu}` is controlled by field equations and boundary flux.",
        "",
        "That is the route by which local `q_loc^nu` can be derived rather than imposed.",
        "",
        "## Source Register",
        "",
        md_table(rows_by_name["source_register"]),
        "",
        "## Derivative Response Identity",
        "",
        md_table(rows_by_name["derivative_response_identity"]),
        "",
        "## Noether/Hilbert Route",
        "",
        md_table(rows_by_name["noether_hilbert_route"]),
        "",
        "## Q_DeltaK Derivative Bound",
        "",
        md_table(rows_by_name["qDeltaK_derivative_bound"]),
        "",
        "## Claim Status",
        "",
        md_table(rows_by_name["claim_status"]),
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
        "- Progress: a real derivation route is now on the table. Derivative/Hodge/Poynting-like stress is not something to hide; it belongs inside `K_hat` as Hilbert stress.",
        "- Still blocked: no local-GR or PPN claim is allowed until `K_hat=K_Hilbert` is parent-signed and the local field-equation/boundary/projector clauses close.",
        "- Best next move: instantiate the parent Hilbert-Khat contract in 3457, because that is the shortest path from the current MTS notation to GR-style conservation.",
        "",
    ]
    DOC.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    start_utc = datetime.now(timezone.utc)
    OUT.mkdir(parents=True, exist_ok=True)
    rows_by_name: dict[str, list[dict[str, Any]]] = {
        "source_register": source_register(),
        "derivative_response_identity": derivative_response_identity(),
        "noether_hilbert_route": noether_hilbert_route(),
        "qDeltaK_derivative_bound": qDeltaK_derivative_bound(),
        "claim_status": claim_status(),
        "decision_ledger": decision_ledger(),
        "next_target": next_target(),
    }
    output_map = {
        "source_register": OUT / "P8_Y5_R2FR_3456_SOURCE_REGISTER.csv",
        "derivative_response_identity": OUT / "P8_Y5_R2FR_3456_DERIVATIVE_RESPONSE_IDENTITY.csv",
        "noether_hilbert_route": OUT / "P8_Y5_R2FR_3456_NOETHER_HILBERT_ROUTE.csv",
        "qDeltaK_derivative_bound": OUT / "P8_Y5_R2FR_3456_QDELTAK_DERIVATIVE_BOUND.csv",
        "claim_status": OUT / "P8_Y5_R2FR_3456_CLAIM_STATUS.csv",
        "decision_ledger": OUT / "P8_Y5_R2FR_3456_DECISION_LEDGER.csv",
        "next_target": OUT / "P8_Y5_R2FR_3456_NEXT_TARGET.csv",
    }
    for name, path in output_map.items():
        write_csv(path, rows_by_name[name])
    rows_by_name["validation"] = validation_rows(rows_by_name, start_utc)
    write_csv(OUT / "P8_Y5_BRR545_3456_VALIDATION.csv", rows_by_name["validation"])
    write_doc(rows_by_name)
    print(f"wrote {DOC}")
    print("wrote 8 csv outputs")


if __name__ == "__main__":
    main()
