from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = ROOT.parent / "formalization-workbench"
DOC = ROOT / "3549-Y5-R2FR-Hilbert-source-denominator-PiM-Htau-local-Newton-bridge.md"
CANONICAL_STATUS = OUT / "P8_Y5_Hilbert_source_denominator_PiM_Htau_Newton_bridge_status.csv"


SOURCES: dict[str, dict[str, Any]] = {
    "script_3549": {"path": Path(__file__).resolve(), "role": "3549 generator"},
    "doc_3548": {
        "path": ROOT / "3548-Y5-R2FR-typed-EM-coefficient-domain-no-Hom-certificate-or-alpha-closure-demotion.md",
        "role": "alpha quarantine and source-denominator handoff",
    },
    "next_3548": {
        "path": OUT / "P8_Y5_R2FR_3548_NEXT_TARGET.csv",
        "role": "3548 selected Hilbert source denominator target",
    },
    "local_gr_denominator_status_3531": {
        "path": OUT / "P8_local_GR_Hilbert_source_denominator_status.csv",
        "role": "local GR Hilbert source denominator status",
    },
    "ellj_law_3513": {
        "path": OUT / "P8_EM_ellJ_source_current_owner_residual_law.csv",
        "role": "ell_J source-current residual decomposition",
    },
    "pim_htau_law_3514": {
        "path": OUT / "P8_EM_PiM_Htau_commutator_residual_law.csv",
        "role": "R_PiM+R_Htau component law",
    },
    "pim_htau_derivation_3514": {
        "path": OUT / "P8_Y5_R2FR_3514_PIM_HTAU_COMMUTATOR_DERIVATION.csv",
        "role": "Pi_M/H_tau commutator derivation",
    },
    "zero_gates_3514": {
        "path": OUT / "P8_Y5_R2FR_3514_PIM_HTAU_ZERO_GATES.csv",
        "role": "zero gates for Pi_M/H_tau components",
    },
    "bound_template_3514": {
        "path": OUT / "P8_Y5_R2FR_3514_PIM_HTAU_BOUND_INPUT_TEMPLATE.csv",
        "role": "nonclaim bound input template",
    },
    "zero_proof_3532": {
        "path": OUT / "P8_Y5_R2FR_3532_PIM_HTAU_ZERO_PROOF.csv",
        "role": "conditional Pi_M/H_tau zero mechanism",
    },
    "hamiltonian_lock_2665": {
        "path": OUT / "P8_Y5_R10_HAMILTONIAN_PIM_QBARXH_LOCK_2665_LOCK_CONTRACT.csv",
        "role": "Hamiltonian source-domain/PiM/QbarXH lock",
    },
    "htau_curl_2667": {
        "path": OUT / "P8_Y5_R10_HTAU_INTEGRABILITY_CURL_2667_INTEGRABILITY_GATE.csv",
        "role": "H_tau integrability curl gate",
    },
    "mhref_reference_2938": {
        "path": OUT / "P8_Y5_R2FR_2938_MHREF_ELLJ_REFERENCE_LOCK_CONTRACT.csv",
        "role": "M_H_ref/H_ref/ell_J reference lock",
    },
    "worldtube_2611": {
        "path": OUT / "P8_Y5_MATTER_DESCENT_GATE_2611_WORLDTUBE_SOURCE_OWNER_AUDIT.csv",
        "role": "worldtube/source owner audit",
    },
    "poisson_gauss_contract": {
        "path": OUT / "P8_Hamiltonian_charge_Poisson_Gauss_calibration_CONTRACT.csv",
        "role": "Hamiltonian charge to Poisson/Gauss calibration contract",
    },
    "hilbert_monopole_contract": {
        "path": OUT / "P8_Hilbert_monopole_calibration_CONTRACT.csv",
        "role": "Hilbert monopole/source calibration contract",
    },
    "mass_current_charge_contract": {
        "path": OUT / "P8_mass_current_Hamiltonian_boundary_charge_CONTRACT.csv",
        "role": "mass current and Hamiltonian boundary charge contract",
    },
    "newton_stack": {
        "path": OUT / "P8_source_normalized_Newton_branch_STACK.csv",
        "role": "source-normalized Newton branch rung stack",
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


def identity_rows() -> list[dict[str, Any]]:
    return [
        {
            "identity_id": "ID3549_0_MHref",
            "object": "Hilbert source denominator",
            "mathematical_form": "M_H_ref := H_tau[S_outer] - H_ref",
            "meaning": "source mass denominator must be finite, positive, same-frame and defined before orbital GM readout",
            "current_status": "CONDITIONAL_DEFINITION_NOT_CLAIMED",
            "source_path": str(SOURCES["mhref_reference_2938"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "identity_id": "ID3549_1_ellJ",
            "object": "source-current normalization drift",
            "mathematical_form": "z_ellJ = R_md + R_Ward + R_PiM + R_Htau + R_ref + R_W + R_frame + R_units",
            "meaning": "source coupling is no longer vague; its denominator drift has named obstruction terms",
            "current_status": "EXACT_DECOMPOSITION_NONCLAIM",
            "source_path": str(SOURCES["ellj_law_3513"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "identity_id": "ID3549_2_PiM_Htau_square",
            "object": "algebraic denominator heart",
            "mathematical_form": "R_PiM + R_Htau = C_M + C_shape + C_curl + C_domain + C_ref + C_frame + C_units",
            "meaning": "the hardest denominator terms reduce to a mass-connection/integrability/reference/domain/frame/units square",
            "current_status": "EXACT_COMPONENT_DECOMPOSITION_NONCLAIM",
            "source_path": str(SOURCES["pim_htau_law_3514"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "identity_id": "ID3549_3_Newton_target",
            "object": "Newton/Poisson bridge",
            "mathematical_form": "nabla^2 Phi = 4*pi*G_eff*rho_H and surface_integral grad Phi.dS = 4*pi*G_eff*M_H_ref",
            "meaning": "becomes claimable only after EH operator, source denominator, closed flux, Gauss calibration and readout residuals close",
            "current_status": "TARGET_WRITTEN_NOT_PROMOTED",
            "source_path": str(SOURCES["poisson_gauss_contract"]["path"]),
            "valid_for_claim": "False",
        },
    ]


def zero_clause_rows() -> list[dict[str, Any]]:
    return [
        {
            "component": "C_M",
            "zero_clause": "mass-flat source connection",
            "mathematical_condition": "partial_M A_X^M = 0",
            "effect": "residual direction X does not reparameterize source mass",
            "current_status": "NEW_PARENT_CONNECTION_REQUIRED",
            "missing_owner": "A_X source-branch geometry from q(Phi)",
            "source_path": str(SOURCES["pim_htau_law_3514"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "component": "C_shape",
            "zero_clause": "mass/shape orthogonality",
            "mathematical_condition": "partial_M A_X^a = 0 or shape directions are Pi_M-orthogonal",
            "effect": "source shape/domain leakage cannot masquerade as mass denominator drift",
            "current_status": "SOURCE_SHAPE_CONNECTION_UNSIGNED",
            "missing_owner": "parent source metric or shape-support orthogonality theorem",
            "source_path": str(SOURCES["worldtube_2611"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "component": "C_curl",
            "zero_clause": "integrable observed-time Hamiltonian",
            "mathematical_condition": "curl(delta H_tau)=0 up to exact/proper boundary terms",
            "effect": "H_tau is a real charge rather than path-dependent bookkeeping",
            "current_status": "HTAU_INTEGRABILITY_CURL_OPEN",
            "missing_owner": "parent theta/omega owner, tau/surface lock and boundary exactness",
            "source_path": str(SOURCES["htau_curl_2667"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "component": "C_domain",
            "zero_clause": "fixed parent worldtube/support selector",
            "mathematical_condition": "W_source = closure(supp J_H[tau]) and linked surfaces fixed before readout",
            "effect": "Pi_M does not move source support after seeing data",
            "current_status": "DOMAIN_SUPPORT_NOT_PARENT_SIGNED",
            "missing_owner": "same-frame J_H, tau lock, compact support and no readout mask",
            "source_path": str(SOURCES["worldtube_2611"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "component": "C_ref",
            "zero_clause": "source-blind reference subtraction",
            "mathematical_condition": "D_X H_ref=0 and [D_X,Pi_M]H_ref=0",
            "effect": "reference subtraction cannot launder source mass normalization",
            "current_status": "REFERENCE_SELECTOR_UNSIGNED",
            "missing_owner": "Sigma_ref/H_ref selector from boundary/topology/stationarity/asymptotic coframe data",
            "source_path": str(SOURCES["mhref_reference_2938"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "component": "C_frame",
            "zero_clause": "same observed frame/tau/surface/readout branch",
            "mathematical_condition": "tau, e_obs, surfaces and readout frame are fixed together before readout",
            "effect": "clock/frame normalization cannot change the denominator commutator",
            "current_status": "PARALLEL_RFRAME_FACTOR",
            "missing_owner": "same-frame source variation, not merely same-frame matter motion",
            "source_path": str(SOURCES["pim_htau_law_3514"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "component": "C_units",
            "zero_clause": "parent-owned denominator units",
            "mathematical_condition": "M_H_ref units, G_ref and source-current normalization are declared before measured GM",
            "effect": "unit/source normalization cannot be absorbed into orbital GM",
            "current_status": "ELLJ_UNITS_NONCLAIM",
            "missing_owner": "positive M_H_ref, no-orbital-import certificate and source-current unit lock",
            "source_path": str(SOURCES["mhref_reference_2938"]["path"]),
            "valid_for_claim": "False",
        },
    ]


def bound_interface_rows() -> list[dict[str, Any]]:
    return [
        {
            "bound_id": "B3549_0_C_M_time",
            "component": "C_M",
            "observable_arena": "Gdot/time drift",
            "bound_interface": "abs(time projection of C_M) <= Gdot/source-denominator drift bound after product factors are separated",
            "candidate_bound": "4.0e-14 yr^-1 anchor from 3514 template only",
            "prediction_status": "MISSING_MASS_CONNECTION_VALUE",
            "numeric_bound_ready": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "bound_id": "B3549_1_C_shape_profile",
            "component": "C_shape",
            "observable_arena": "PPN source profile / R10 source support",
            "bound_interface": "shape leakage must map to source-profile, WEP/R10 support, or PPN near-source residual",
            "candidate_bound": "MISSING_SHAPE_PROJECTION_BOUND",
            "prediction_status": "MISSING_SOURCE_SHAPE_CONNECTION_VALUE",
            "numeric_bound_ready": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "bound_id": "B3549_2_C_curl_integrability",
            "component": "C_curl",
            "observable_arena": "Gdot / Newton source / clocks / PPN",
            "bound_interface": "field-space curl of H_tau must be zero-owned or bounded as Hamiltonian nonintegrability",
            "candidate_bound": "MISSING_CURL_BOUND",
            "prediction_status": "MISSING_THETA_OMEGA_OWNER",
            "numeric_bound_ready": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "bound_id": "B3549_3_C_domain_support",
            "component": "C_domain",
            "observable_arena": "R10 / Newton source / PPN source profile",
            "bound_interface": "domain/support drift maps to worldtube source-mask residual",
            "candidate_bound": "MISSING_DOMAIN_SUPPORT_BOUND",
            "prediction_status": "MISSING_WORLDTUBE_SELECTOR",
            "numeric_bound_ready": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "bound_id": "B3549_4_C_ref_reference",
            "component": "C_ref",
            "observable_arena": "Gdot / R10 denominator / local boundary terms",
            "bound_interface": "reference derivative must be bounded independently and never cancelled against H_tau",
            "candidate_bound": "MISSING_REFERENCE_DERIVATIVE_BOUND",
            "prediction_status": "MISSING_HREF_SELECTOR",
            "numeric_bound_ready": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "bound_id": "B3549_5_C_frame",
            "component": "C_frame",
            "observable_arena": "clock / PPN / orbital GM",
            "bound_interface": "same-frame residual maps to frame/source calibration rows",
            "candidate_bound": "MISSING_FRAME_SPLIT_BOUND",
            "prediction_status": "MISSING_SOURCE_FRAME_THEOREM",
            "numeric_bound_ready": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "bound_id": "B3549_6_C_units",
            "component": "C_units",
            "observable_arena": "Gdot / Newton G / action normalization",
            "bound_interface": "duplicate source units must be separated from measured GM and bounded as source-scale drift",
            "candidate_bound": "MISSING_SOURCE_UNIT_BOUND",
            "prediction_status": "MISSING_DENOMINATOR_UNIT_LOCK",
            "numeric_bound_ready": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def newton_rung_rows() -> list[dict[str, Any]]:
    return [
        {
            "rung_id": "NBR3549_0_candidate_charge",
            "required_identity": "observed-time Hamiltonian charge exists and is integrable",
            "math_form": "H_xi = B_xi on shell; delta H_tau is path independent",
            "blocked_by": "C_curl; C_ref; C_frame",
            "current_status": "CONDITIONAL_NOT_PARENT_DERIVED",
            "claim_effect": "no source charge candidate can be promoted",
            "valid_for_claim": "False",
        },
        {
            "rung_id": "NBR3549_1_charge_equals_Hilbert",
            "required_identity": "Hamiltonian charge equals projected Hilbert mass current",
            "math_form": "B_xi/G_eff = M_eff[Pi_M J_H]",
            "blocked_by": "C_M; C_shape; C_domain; C_ref",
            "current_status": "NOT_PARENT_DERIVED",
            "claim_effect": "geometric charge is not yet Newton source mass",
            "valid_for_claim": "False",
        },
        {
            "rung_id": "NBR3549_2_closed_flux",
            "required_identity": "projected Hilbert mass flux is closed in compact exterior",
            "math_form": "d(Pi_M J_H)=0 and partial_t,r M_eff=0 outside support",
            "blocked_by": "C_domain; C_frame; C_units; R_Ward",
            "current_status": "NOT_PARENT_DERIVED",
            "claim_effect": "time drift/radial hair remain live",
            "valid_for_claim": "False",
        },
        {
            "rung_id": "NBR3549_3_Poisson_source",
            "required_identity": "EH weak-field 00 equation sources the same rho_H",
            "math_form": "nabla^2 Phi = 4*pi*G_eff*rho_H",
            "blocked_by": "R11 operator/source residuals plus source denominator rows",
            "current_status": "EXACT_CONDITIONAL_NOT_CLAIMED",
            "claim_effect": "no Newton/Poisson pass yet",
            "valid_for_claim": "False",
        },
        {
            "rung_id": "NBR3549_4_Gauss_orbital_readout",
            "required_identity": "Poisson source integrates to measured orbital monopole",
            "math_form": "surface_integral grad Phi.dS = 4*pi*G_eff*M_H_ref and a_r=-G_eff*M_H_ref/r^2",
            "blocked_by": "closed flux, radial hair, range/source/frame residuals",
            "current_status": "NOT_PARENT_DERIVED",
            "claim_effect": "orbital GM remains empirical readout, not definition of source charge",
            "valid_for_claim": "False",
        },
        {
            "rung_id": "NBR3549_5_second_order_GR",
            "required_identity": "first-order source calibration survives PPN beta/gamma order",
            "math_form": "gamma-1=0 and delta_beta_source=0 after measured-GM normalization",
            "blocked_by": "R11 operator vector and nonlinear source stability",
            "current_status": "DEFERRED_AFTER_FIRST_ORDER",
            "claim_effect": "even a future Newton bridge is not full local GR until PPN closes",
            "valid_for_claim": "False",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3549_0_zero_status",
            "question": "Did 3549 prove R_PiM+R_Htau=0?",
            "decision": "NO",
            "basis": "the conditional theorem is clear, but C_M/C_shape/C_curl/C_domain/C_ref/C_frame/C_units are not parent-owned zeros",
            "consequence": "no Newton/Poisson/local-GR claim",
            "valid_for_claim": "False",
        },
        {
            "decision_id": "DEC3549_1_forward_value",
            "question": "What did 3549 actually add?",
            "decision": "DENOMINATOR_BRIDGE_LOCKED",
            "basis": "the exact residual square and Newton bridge rungs are now aligned in one gate",
            "consequence": "next work can attack C_M/C_shape first rather than circling all source coupling at once",
            "valid_for_claim": "False",
        },
        {
            "decision_id": "DEC3549_2_next_route",
            "question": "Which component is best next?",
            "decision": "MASS_FLAT_SOURCE_CONNECTION",
            "basis": "3514 explicitly says derive mass-flat source connection before numeric scoring; C_M/C_shape are the cleanest algebraic blockers",
            "consequence": "3550 should target A_X source-branch geometry and Pi_M chainmap mass/shape orthogonality",
            "valid_for_claim": "False",
        },
    ]


def status_rows() -> list[dict[str, Any]]:
    return [
        {
            "status_id": "STATUS3549_0",
            "checkpoint": "3549",
            "claim_allowed": "False",
            "R_PiM_plus_R_Htau_status": "exact_decomposition_ready_zero_not_parent_signed",
            "Newton_bridge_status": "rungs_aligned_no_promotion",
            "strongest_zero_route": "mass_flat_source_connection_plus_integrable_Htau_plus_fixed_reference_worldtube_frame_units",
            "best_next_component": "C_M_and_C_shape_mass_flat_source_connection",
            "next_target": "3550-Y5-R2FR-mass-flat-source-connection-PiM-chainmap-or-CM-Cshape-bound.md",
            "valid_for_claim": "False",
        }
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT3549_0",
            "target_doc": "3550-Y5-R2FR-mass-flat-source-connection-PiM-chainmap-or-CM-Cshape-bound.md",
            "target_script": "scripts/Y5_R2FR_3550_mass_flat_source_connection_PiM_chainmap_or_CM_Cshape_bound.py",
            "objective": "try to derive the mass-flat source-branch connection conditions partial_M A_X^M=0 and partial_M A_X^a=0 for Pi_M; if not, create explicit C_M/C_shape bound rows",
            "success_gate": "either C_M and C_shape become parent-owned zeros, or their prediction/bound inputs are concrete nonclaim rows with units/projections/source paths",
            "reason": "C_M/C_shape are the first algebraic obstructions in the Pi_M/H_tau denominator square and must close before Newton source calibration can claim",
            "valid_for_claim": "False",
        }
    ]


def validation_rows(
    generated_paths: list[Path],
    sources: list[dict[str, Any]],
    zero_clauses: list[dict[str, Any]],
    bounds: list[dict[str, Any]],
    rungs: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    required_sources_exist = all(row["exists"] == "True" for row in sources)
    generated_csvs = [path for path in generated_paths if path.suffix.lower() == ".csv"]
    csvs_parse = all(csv_parse_ok(path) for path in generated_csvs)
    all_components_covered = {row["component"] for row in zero_clauses} == {
        "C_M",
        "C_shape",
        "C_curl",
        "C_domain",
        "C_ref",
        "C_frame",
        "C_units",
    }
    bounds_nonclaim = all(row["claim_allowed"] == "False" and row["valid_for_claim"] == "False" for row in bounds)
    rungs_nonclaim = all(row["valid_for_claim"] == "False" for row in rungs)
    no_formalization_outputs = all(FORMALIZATION not in path.parents for path in generated_paths)
    return [
        {
            "validation_id": "VAL3549_0_sources_exist",
            "passes": bool_text(required_sources_exist),
            "status": "PASS" if required_sources_exist else "FAIL",
            "detail": "all cited 3549 source paths exist",
        },
        {
            "validation_id": "VAL3549_1_generated_csvs_parse",
            "passes": bool_text(csvs_parse),
            "status": "PASS" if csvs_parse else "FAIL",
            "detail": f"{len(generated_csvs)} generated CSV files parse with DictReader",
        },
        {
            "validation_id": "VAL3549_2_all_components_covered",
            "passes": bool_text(all_components_covered),
            "status": "PASS" if all_components_covered else "FAIL",
            "detail": "C_M, C_shape, C_curl, C_domain, C_ref, C_frame and C_units are all present",
        },
        {
            "validation_id": "VAL3549_3_bound_rows_nonclaim",
            "passes": bool_text(bounds_nonclaim),
            "status": "PASS" if bounds_nonclaim else "FAIL",
            "detail": "all denominator bound interface rows remain nonclaim",
        },
        {
            "validation_id": "VAL3549_4_newton_rungs_nonclaim",
            "passes": bool_text(rungs_nonclaim),
            "status": "PASS" if rungs_nonclaim else "FAIL",
            "detail": "Newton/Poisson/PPN rungs remain no-promotion rows",
        },
        {
            "validation_id": "VAL3549_5_formalization_workbench_untouched",
            "passes": bool_text(no_formalization_outputs),
            "status": "PASS" if no_formalization_outputs else "FAIL",
            "detail": "3549 generated outputs only inside post-checkpoint-work",
        },
    ]


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    lines = [
        "# 3549 — Hilbert source denominator PiM/Htau local Newton bridge",
        "",
        "## Verdict",
        "",
        "- **The source denominator bridge is now locked into one exact square:** `R_PiM+R_Htau = C_M + C_shape + C_curl + C_domain + C_ref + C_frame + C_units`.",
        "- **No Newton/Poisson/local-GR claim is allowed yet.** The conditional zero route is clean, but the mass-flat source connection, Htau integrability, worldtube selector, reference lock, same-frame branch and denominator units are not parent-signed.",
        "- **The best next move is not another broad audit:** attack `C_M` and `C_shape` by deriving the mass-flat source-branch connection for `Pi_M`.",
        "- **PPN remains separate:** even a future first-order Newton bridge cannot be promoted to full local GR until second-order beta/gamma/operator residuals close.",
        "",
        "## Identity Lock",
        "",
        markdown_table(
            rows_by_name["identity"],
            ["identity_id", "object", "mathematical_form", "meaning", "current_status"],
        ),
        "",
        "## Zero Clauses",
        "",
        markdown_table(
            rows_by_name["zero_clauses"],
            ["component", "zero_clause", "mathematical_condition", "effect", "current_status", "missing_owner"],
        ),
        "",
        "## Bound Interfaces",
        "",
        markdown_table(
            rows_by_name["bounds"],
            ["bound_id", "component", "observable_arena", "candidate_bound", "prediction_status", "numeric_bound_ready"],
        ),
        "",
        "## Newton Bridge Rungs",
        "",
        markdown_table(
            rows_by_name["rungs"],
            ["rung_id", "required_identity", "math_form", "blocked_by", "current_status", "claim_effect"],
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
        "Move to `3550-Y5-R2FR-mass-flat-source-connection-PiM-chainmap-or-CM-Cshape-bound.md`: derive `partial_M A_X^M=0` and `partial_M A_X^a=0` from parent source-branch geometry, or turn `C_M`/`C_shape` into explicit finite nonclaim rows.",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
    ]
    DOC.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)

    sources = source_rows()
    identities = identity_rows()
    zero_clauses = zero_clause_rows()
    bounds = bound_interface_rows()
    rungs = newton_rung_rows()
    decisions = decision_rows()
    status = status_rows()
    next_target = next_target_rows()

    outputs: dict[Path, tuple[list[dict[str, Any]], list[str]]] = {
        OUT / "P8_Y5_R2FR_3549_SOURCE_REGISTER.csv": (
            sources,
            ["source_id", "path", "exists", "role", "valid_for_claim"],
        ),
        OUT / "P8_Y5_R2FR_3549_DENOMINATOR_IDENTITY_LOCK.csv": (
            identities,
            ["identity_id", "object", "mathematical_form", "meaning", "current_status", "source_path", "valid_for_claim"],
        ),
        OUT / "P8_Y5_R2FR_3549_ZERO_CLAUSE_AUDIT.csv": (
            zero_clauses,
            [
                "component",
                "zero_clause",
                "mathematical_condition",
                "effect",
                "current_status",
                "missing_owner",
                "source_path",
                "valid_for_claim",
            ],
        ),
        OUT / "P8_Y5_R2FR_3549_COMPONENT_BOUND_INTERFACE.csv": (
            bounds,
            [
                "bound_id",
                "component",
                "observable_arena",
                "bound_interface",
                "candidate_bound",
                "prediction_status",
                "numeric_bound_ready",
                "claim_allowed",
                "valid_for_claim",
            ],
        ),
        OUT / "P8_Y5_R2FR_3549_NEWTON_BRIDGE_RUNG_STATUS.csv": (
            rungs,
            ["rung_id", "required_identity", "math_form", "blocked_by", "current_status", "claim_effect", "valid_for_claim"],
        ),
        OUT / "P8_Y5_R2FR_3549_DECISION_LEDGER.csv": (
            decisions,
            ["decision_id", "question", "decision", "basis", "consequence", "valid_for_claim"],
        ),
        OUT / "P8_Y5_R2FR_3549_STATUS.csv": (
            status,
            [
                "status_id",
                "checkpoint",
                "claim_allowed",
                "R_PiM_plus_R_Htau_status",
                "Newton_bridge_status",
                "strongest_zero_route",
                "best_next_component",
                "next_target",
                "valid_for_claim",
            ],
        ),
        OUT / "P8_Y5_R2FR_3549_NEXT_TARGET.csv": (
            next_target,
            ["next_id", "target_doc", "target_script", "objective", "success_gate", "reason", "valid_for_claim"],
        ),
        CANONICAL_STATUS: (
            status,
            [
                "status_id",
                "checkpoint",
                "claim_allowed",
                "R_PiM_plus_R_Htau_status",
                "Newton_bridge_status",
                "strongest_zero_route",
                "best_next_component",
                "next_target",
                "valid_for_claim",
            ],
        ),
    }

    generated_paths: list[Path] = []
    for path, (rows, fields) in outputs.items():
        write_csv(path, rows, fields)
        generated_paths.append(path)

    validation = validation_rows(generated_paths, sources, zero_clauses, bounds, rungs)
    validation_path = OUT / "P8_Y5_BRR545_3549_VALIDATION.csv"
    write_csv(
        validation_path,
        validation,
        ["validation_id", "passes", "status", "detail"],
    )
    generated_paths.append(validation_path)

    write_doc(
        {
            "identity": identities,
            "zero_clauses": zero_clauses,
            "bounds": bounds,
            "rungs": rungs,
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
