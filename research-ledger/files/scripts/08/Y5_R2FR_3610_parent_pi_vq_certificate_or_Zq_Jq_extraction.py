from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = ROOT.parent / "formalization-workbench"
CHECKPOINT_ID = "3610"
BRANCH_ID = "MTS_R2FR_Y5_PARENT_PI_VQ_CERTIFICATE_OR_ZQ_JQ_EXTRACTION_3610"
DOC = ROOT / "3610-Y5-R2FR-parent-pi-vq-certificate-or-Zq-Jq-extraction.md"


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"refusing to write empty csv: {path}")
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def contains(path: Path, needle: str) -> bool:
    return needle in path.read_text(encoding="utf-8-sig", errors="replace")


def sources() -> dict[str, tuple[Path, str]]:
    return {
        "next_3609": (RESIDUALS / "P8_Y5_R2FR_3609_NEXT_TARGET.csv", "NEXT3609_0"),
        "status_3609": (
            RESIDUALS / "P8_Y5_R2FR_3609_STATUS.csv",
            "NO_POLE_THEOREM_PROVED_CONDITIONALLY_MTS_CERTIFICATE_UNSIGNED_HESSIAN_ROWS_FILLED",
        ),
        "certificate_3609": (RESIDUALS / "P8_Y5_R2FR_3609_PARENT_ACTION_CERTIFICATE.csv", "QCERT3609_0_parent_pi"),
        "hessian_3609": (RESIDUALS / "P8_Y5_R2FR_3609_INDEPENDENT_HESSIAN_FILL_ROWS.csv", "QHESS3609_0_Zq"),
        "qmap_candidate_3517": (RESIDUALS / "P8_EM_actual_q_map_vertical_basis_candidate.csv", "QMAP3517_6_private_q"),
        "variable_map_3534": (RESIDUALS / "P8_Y5_R2FR_3534_MTS_VARIABLE_TO_KERNEL_MAP.csv", "MQM3534_0_q_gobs"),
        "double_zero_routes_3534": (RESIDUALS / "P8_Y5_R2FR_3534_DOUBLE_ZERO_THEOREM_ROUTES.csv", "DZT3534_1_norm_square_sigma"),
        "yloc_theorem_3535": (RESIDUALS / "P8_Y5_R2FR_3535_YLOC_EULER_THEOREM.csv", "YET3535_1_Y_euler"),
        "zq_source_hunt_2314": (RESIDUALS / "P8_Y5_PARENT_QLOC_2314_HESSIAN_SOURCE_HUNT.csv", "HUNT2314_2_conditional_stiffness"),
        "mq_jq_defs_2286": (RESIDUALS / "P8_Y5_PARENT_QLOC_2286_MQ_JQ_COEFFICIENT_DEFINITIONS.csv", "COEF2286_3_Zq"),
        "jq_zero_theorem_2431": (RESIDUALS / "P8_Y5_PARENT_QLOC_2431_JQ_DESCENT_ZERO_THEOREM.csv", "JZT2431_1_descent_lemma"),
        "jq_components_2431": (RESIDUALS / "P8_Y5_PARENT_QLOC_2431_JQ_COMPONENT_BOUND_VECTOR.csv", "JQC2431_9_total_abs"),
        "q_slot_normal_form_2364": (RESIDUALS / "P8_Y5_PARENT_QLOC_2364_PARENT_ACTION_Q_SLOT_NORMAL_FORM.csv", "SLOT2364_0_q_euler"),
        "parent_action_candidate_2403": (RESIDUALS / "P8_Y5_PARENT_QLOC_2403_MINIMAL_PARENT_ACTION_CANDIDATE.csv", "MPA2403_0_field_domain"),
        "grammar_2401": (RESIDUALS / "P8_Y5_PARENT_QLOC_2401_PARENT_ACTION_GRAMMAR_CONTRACT.csv", "PAG2401_0_single_parent_action"),
        "matter_gate_2420": (RESIDUALS / "P8_Y5_PARENT_QLOC_2420_MINIMAL_PARENT_COUPLING_GATE.csv", "MPC2420_1_minimal_action_form"),
        "boundary_contract_2457": (RESIDUALS / "P8_Y5_PARENT_QLOC_2457_PARENT_ACTION_CONTRACT.csv", "PAC2457_1_action_form"),
    }


def outputs() -> dict[str, Path]:
    return {
        "source_register": RESIDUALS / "P8_Y5_R2FR_3610_SOURCE_REGISTER.csv",
        "parent_pi_symbol_map": RESIDUALS / "P8_Y5_R2FR_3610_PARENT_PI_SYMBOL_MAP.csv",
        "dpi_vq_certificate": RESIDUALS / "P8_Y5_R2FR_3610_DPI_VQ_CERTIFICATE.csv",
        "zq_jq_extraction_rows": RESIDUALS / "P8_Y5_R2FR_3610_ZQ_JQ_EXTRACTION_ROWS.csv",
        "decision_gates": RESIDUALS / "P8_Y5_R2FR_3610_DECISION_GATES.csv",
        "status": RESIDUALS / "P8_Y5_R2FR_3610_STATUS.csv",
        "next_target": RESIDUALS / "P8_Y5_R2FR_3610_NEXT_TARGET.csv",
        "canonical_status": RESIDUALS / "P8_Y5_parent_pi_vq_or_Zq_Jq_extraction_status.csv",
        "validation": RESIDUALS / "P8_Y5_BRR545_3610_VALIDATION.csv",
    }


def source_register_rows(source_map: dict[str, tuple[Path, str]]) -> list[dict[str, object]]:
    rows = []
    for source_id, (path, needle) in source_map.items():
        exists = path.exists()
        rows.append(
            {
                "timestamp_utc": now(),
                "branch_id": BRANCH_ID,
                "checkpoint_id": CHECKPOINT_ID,
                "source_id": source_id,
                "source_path": str(path),
                "exists": exists,
                "needle": needle,
                "needle_found": exists and contains(path, needle),
                "valid_for_claim": False,
            }
        )
    return rows


def parent_pi_rows(source_map: dict[str, tuple[Path, str]]) -> list[dict[str, object]]:
    p = {key: str(value[0]) for key, value in source_map.items()}
    rows = [
        (
            "PI3610_0_pi_definition",
            "pi_MTS candidate",
            "Phi_MTS -> (g_obs/e_obs, tau_obs, Psi, theta, A_obs, boundary class beta0, parent coupling slots, fixed readout functors)",
            "reduced quotient/base map",
            "CONCRETE_CANDIDATE_CONSTRUCTED_NOT_PARENT_SIGNED",
            "This is the single pi target needed by 3609; it is still a candidate because parent derivation from motion/time/space primitives is unsigned.",
            "parent_action_candidate_2403",
        ),
        (
            "PI3610_1_q_gobs",
            "q(Phi); g_obs; observed coframe",
            "included in reduced base; matter, clocks, EM Hodge star, Hilbert stress and Hamiltonian charge use this same geometry",
            "quotient base",
            "BEST_ANCHOR_CONDITIONAL_QAP_UNSIGNED",
            "This is the least suspicious anchor: public geometry survives; private representative data should not.",
            "variable_map_3534",
        ),
        (
            "PI3610_2_Gamma_Khat_qloc",
            "Gamma_eff; K_hat; q_loc^nu",
            "not primitive quotient coordinates; treated as Ward/projection residuals downstream of pi and boundary subtraction",
            "derived residual",
            "WARD_EXACT_ROUTE_IDENTIFIED_NOT_SIGNED",
            "They can vanish only if the exact Ward/boundary pair and P_loc projection commute on the same branch.",
            "variable_map_3534",
        ),
        (
            "PI3610_3_Ploc_PiM",
            "P_loc; Pi_M",
            "charge-owned projector/readout fixed before variation or retained as explicit obstruction",
            "readout/projector",
            "CONDITIONAL_ZERO_FROM_CHARGE_OWNER",
            "No fitted GM/source projector can be used to prove Newton; this must be parent-owned.",
            "variable_map_3534",
        ),
        (
            "PI3610_4_chiD_Qcoh_memory_flow",
            "chi_D; Qcoh; memory; flow",
            "local silence multiplet Y_loc whose linear couplings must be absent or factor through Sigma_loc=G_AB Y^A Y^B",
            "silent multiplet",
            "DOUBLE_ZERO_ROUTE_CONDITIONAL",
            "This route can kill local hair without individual tuning, but positivity and factorization are not signed.",
            "double_zero_routes_3534",
        ),
        (
            "PI3610_5_EM_Maxwell",
            "EM Hodge/Maxwell/Poynting residuals",
            "visible Maxwell action uses g_obs; hidden F^2/Poynting couplings must be Sigma_loc-factored or bounded",
            "visible stress plus residual coefficient",
            "VISIBLE_STACK_COMPATIBLE_BOUND_ROWS_RETAINED",
            "The EM part fits the shared visible-geometry route but does not yet close hidden EM stress couplings.",
            "variable_map_3534",
        ),
        (
            "PI3610_6_kappa_G",
            "kappa_eff; G_eff",
            "calibrated/topological constant or parent normal-form slot, not a local Y field",
            "coupling/superselection slot",
            "CALIBRATED_CONSTANT_NOT_MTS_DERIVED",
            "This keeps Newton's constant as a coupling/integration datum unless a deeper parent route derives it.",
            "variable_map_3534",
        ),
        (
            "PI3610_7_q_private",
            "q_private",
            "excluded representative direction; eligible for no-pole only if first-class/source-silent and Dpi[v_q]=0",
            "candidate vertical representative",
            "CANDIDATE_VERTICAL_UNSIGNED",
            "This is the exact q deletion target; it is not allowed to hide Weyl, matter, boundary or readout tails.",
            "qmap_candidate_3517",
        ),
        (
            "PI3610_8_source_coordinates",
            "M_H_ref; sigma^a",
            "not primitive pi entries; must be derived as source coordinates Ybar(pi(Phi))",
            "derived observable",
            "ANTI_TAUTOLOGY_GUARD_ACTIVE",
            "Including source coordinates directly in pi would smuggle the Newton/source answer into the premises.",
            "qmap_candidate_3517",
        ),
    ]
    stamp = now()
    return [
        {
            "timestamp_utc": stamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "map_id": map_id,
            "MTS_symbol": symbol,
            "pi_placement": placement,
            "kernel_role": role,
            "current_status": status,
            "effect_or_guard": effect,
            "source_path": p[source_id],
            "parent_signed": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        }
        for map_id, symbol, placement, role, status, effect, source_id in rows
    ]


def dpi_rows(source_map: dict[str, tuple[Path, str]]) -> list[dict[str, object]]:
    p = {key: str(value[0]) for key, value in source_map.items()}
    rows = [
        (
            "DPI3610_0_target",
            "v_q = partial/partial q_private at fixed reduced fields",
            "Dpi[v_q]=0 for every pi component",
            "DEFINITIONAL_TARGET",
            "This is the concrete version of the 3609 certificate.",
            "certificate_3609",
        ),
        (
            "DPI3610_1_geometry",
            "D g_obs[v_q], D e_obs[v_q]",
            "zero if q_private is not a hidden coframe/disformal/frame variable",
            "CONDITIONAL_ZERO_NOT_PARENT_SIGNED",
            "Hidden frame re-entry would make q physical and reopen PPN/WEP/clock rows.",
            "qmap_candidate_3517",
        ),
        (
            "DPI3610_2_tau_clock",
            "D tau_obs[v_q], D clock standards[v_q]",
            "zero if tau/clock map descends through pi_MTS and has no q_private representative leg",
            "CONDITIONAL_ZERO_NOT_PARENT_SIGNED",
            "Clock/time route remains important because it can reintroduce local force through readout.",
            "qmap_candidate_3517",
        ),
        (
            "DPI3610_3_matter_constants",
            "D(Psi,theta,c_vis,masses,charges)[v_q]",
            "zero if ordinary matter action and constants are q-basic/superselection data",
            "CONDITIONAL_ZERO_NOT_PARENT_SIGNED",
            "This is the J_q matter/marker source leg.",
            "matter_gate_2420",
        ),
        (
            "DPI3610_4_boundary",
            "D beta0[v_q], D B_ref[v_q], D H_ref[v_q]",
            "zero if fixed boundary class and reference functional are varied at fixed beta0",
            "CONDITIONAL_ZERO_NOT_PARENT_SIGNED",
            "This is the boundary/source-worldtube leg of J_q.",
            "boundary_contract_2457",
        ),
        (
            "DPI3610_5_coefficients",
            "D(kappa,G,alpha_EM,source weights)[v_q]",
            "zero if visible coefficients are parent normal-form slots or quotient constants",
            "CONDITIONAL_ZERO_NOT_PARENT_SIGNED",
            "Without this, q deletion can be faked while constants drift.",
            "grammar_2401",
        ),
        (
            "DPI3610_6_projectors",
            "D(P_loc,Pi_M,domain/readout kernels)[v_q]",
            "zero if projectors are fixed before variation or descend through pi_MTS",
            "CONDITIONAL_ZERO_NOT_PARENT_SIGNED",
            "If projectors move, q leaks through source normalization even when equations look GR-like.",
            "variable_map_3534",
        ),
        (
            "DPI3610_7_Yloc",
            "D Y_loc[v_q]",
            "not required to vanish if Y_loc is a physical residual multiplet; then positive Hessian/factorization must control it",
            "FORK_ROW",
            "This separates quotient representative q from physical silent multiplet Y_loc.",
            "yloc_theorem_3535",
        ),
        (
            "DPI3610_8_verdict",
            "pi_MTS/v_q certificate",
            "all component rows must be signed on one branch",
            "NOT_CERTIFIED_CURRENT_CORPUS",
            "Proceed to conditional Z_q/J_q extraction rather than claiming q deletion.",
            "status_3609",
        ),
    ]
    stamp = now()
    return [
        {
            "timestamp_utc": stamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "certificate_id": certificate_id,
            "component": component,
            "required_zero": required_zero,
            "current_status": status,
            "consequence": consequence,
            "source_path": p[source_id],
            "component_signed": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        }
        for certificate_id, component, required_zero, status, consequence, source_id in rows
    ]


def extraction_rows(source_map: dict[str, tuple[Path, str]]) -> list[dict[str, object]]:
    p = {key: str(value[0]) for key, value in source_map.items()}
    rows = [
        (
            "EX3610_0_Mq2",
            "M_q^2",
            "M_q^2 = n_q^A H_AB n_q^B",
            "Hessian projection along the q normal direction in the local silence multiplet branch.",
            "CONDITIONAL_FORMULA_IMPORTED",
            "requires parent-owned H_AB positivity and q normal n_q^A",
            "zq_source_hunt_2314",
        ),
        (
            "EX3610_1_Zq",
            "Z_q",
            "Z_q = xi_q^2 n_q^A H_AB n_q^B",
            "gradient/operator stiffness from smoothing/correlation length xi_q in the same q normalization.",
            "CONDITIONAL_FORMULA_IMPORTED",
            "requires xi_q source, same normalization as M_q^2, and domain/boundary ownership",
            "zq_source_hunt_2314",
        ),
        (
            "EX3610_2_lambda",
            "lambda_q",
            "lambda_q = sqrt(Z_q/M_q^2) = xi_q",
            "the q force range is not free in this branch; it collapses to the parent smoothing/correlation length.",
            "EXACT_CONDITIONAL_RATIO",
            "requires positive M_q^2 and nonzero Z_q from the same Hessian branch",
            "zq_source_hunt_2314",
        ),
        (
            "EX3610_3_Lq",
            "L_q",
            "L_q = -Z_q Delta_branch + M_q^2 + B_q^bdry",
            "local q operator after importing the conditional Hessian/range relation.",
            "OPERATOR_SHAPE_FILLED_CONDITIONAL",
            "requires boundary/self-adjoint extension and no-pole failure predicate",
            "hessian_3609",
        ),
        (
            "EX3610_4_Jq_definition",
            "J_q",
            "J_q[eta] := delta_eta S_nonq projected onto the q equation",
            "first source/readout leg if q is physical rather than quotient-deleted.",
            "DEFINITION_SHARPENED",
            "requires q normalization, variation domain and projection convention",
            "jq_zero_theorem_2431",
        ),
        (
            "EX3610_5_Jq_descent_zero",
            "J_q zero theorem",
            "delta_vq F_i=0 if F_i=Fbar_i(Obs(Phi),psi) and v_q in ker(DObs)",
            "chain-rule source-zero theorem for every non-q sector.",
            "EXACT_CONDITIONAL_NOT_ACTIVE",
            "requires parent observed-object functor and all-field vertical generator",
            "jq_zero_theorem_2431",
        ),
        (
            "EX3610_6_Jq_components",
            "J_q^abs",
            "J_q^abs = sum_i ||J_q^i||_* over matter, frame, marker, body, boundary, projector, memory, source-normalization and curvature components",
            "absolute no-cancellation envelope for the physical q source.",
            "SCHEMA_READY_VALUES_MISSING",
            "requires each component theorem-zero or source-backed bound",
            "jq_components_2431",
        ),
        (
            "EX3610_7_q_source_vector",
            "E_q",
            "E_q = L_q q + B_qRic R_Ricci + B_qW C_Weyl + C_qT T_H + epsilon_q_source sigma_source + Q_q_body delta_body + Pi_q delta_boundary + tail_q",
            "full q Euler/source-vector normal form with all dangerous source channels explicit.",
            "NORMAL_FORM_ACCEPTED_NONCLAIM",
            "requires each coefficient zero/bound or no-pole deletion",
            "q_slot_normal_form_2364",
        ),
        (
            "EX3610_8_residual_bound",
            "q residual bound",
            "||P_arena q|| <= ||P_arena L_q^{-1}|| (||J_q^abs|| + |B_qW| ||C_Weyl|| + |D_qWeyl2| ||C^2|| + boundary tails)",
            "runner-ready symbolic law for R10/PPN/clock/orbital branches.",
            "BOUND_LAW_READY_NUMBERS_MISSING",
            "requires Z_q/M_q^2/xi_q, source envelope values and arena projections",
            "status_3609",
        ),
    ]
    stamp = now()
    return [
        {
            "timestamp_utc": stamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "extract_id": extract_id,
            "symbol": symbol,
            "formula": formula,
            "meaning": meaning,
            "current_status": status,
            "required_to_score": required,
            "source_path": p[source_id],
            "formula_source_backed": True,
            "numeric_value_present": False,
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        }
        for extract_id, symbol, formula, meaning, status, required, source_id in rows
    ]


def decision_rows(source_map: dict[str, tuple[Path, str]]) -> list[dict[str, object]]:
    p = {key: str(value[0]) for key, value in source_map.items()}
    rows = [
        (
            "DEC3610_0_pi_map",
            "pi_MTS concrete map",
            "BUILT_NOT_SIGNED",
            "Actual MTS symbols are placed into quotient base, derived residual, local silence multiplet, visible stress and coupling slots.",
            "variable_map_3534",
        ),
        (
            "DEC3610_1_dpi_vq",
            "Dpi[v_q] certificate",
            "FAIL_CURRENT_CERTIFICATION",
            "The required component zeros are now explicit, but none is parent-signed across geometry, clocks, matter, boundary, constants and projectors.",
            "qmap_candidate_3517",
        ),
        (
            "DEC3610_2_Zq",
            "Z_q/M_q/lambda extraction",
            "CONDITIONAL_FORMULA_ADVANCED",
            "The fallback is upgraded from blank placeholders to M_q^2=n_q H n_q, Z_q=xi_q^2 n_q H n_q, lambda_q=xi_q.",
            "zq_source_hunt_2314",
        ),
        (
            "DEC3610_3_Jq",
            "J_q extraction",
            "COMPONENT_ENVELOPE_READY_VALUES_MISSING",
            "The J_q source problem is an absolute component vector, not an undifferentiated coupling mystery.",
            "jq_components_2431",
        ),
        (
            "DEC3610_4_next",
            "next best attack",
            "SELECT_XI_OR_JQ_FIRST_COMPONENT",
            "Either derive/source xi_q and the positive Hessian branch, or attack the highest-pressure J_q components: matter/constants and body/boundary.",
            "zq_source_hunt_2314",
        ),
    ]
    stamp = now()
    return [
        {
            "timestamp_utc": stamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "decision_id": decision_id,
            "gate": gate,
            "status": status,
            "consequence": consequence,
            "source_path": p[source_id],
            "claim_allowed": False,
            "valid_for_claim": False,
        }
        for decision_id, gate, status, consequence, source_id in rows
    ]


def status_rows(source_map: dict[str, tuple[Path, str]]) -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "status": "PI_MTS_MAP_BUILT_VQ_UNSIGNED_ZQ_JQ_CONDITIONAL_EXTRACTION_ADVANCED",
            "strongest_result": "3610 builds a concrete pi_MTS candidate over actual MTS symbols and upgrades the physical-q fallback: M_q^2=n_q^A H_AB n_q^B, Z_q=xi_q^2 n_q^A H_AB n_q^B, and lambda_q=xi_q under the positive Hessian branch.",
            "decision": "do not claim q deletion; Dpi[v_q] remains unsigned componentwise. Treat q as either a future quotient representative or a physical residual with a now-sharper Hessian/source envelope.",
            "framework_progress": "The next testable/derivable bottleneck is no longer abstract q ownership; it is xi_q/positive-Hessian ownership plus the absolute J_q component vector.",
            "still_missing": "parent pi signature, Dpi[v_q] component zeros, xi_q source, positive H_AB, boundary/domain conditions, J_q component zero/bound values and arena projections",
            "public_claim_allowed": False,
            "valid_for_claim": False,
            "source_path": str(source_map["zq_source_hunt_2314"][0]),
        }
    ]


def next_target_rows() -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "next_id": "NEXT3610_0",
            "target_doc": "3611-Y5-R2FR-xi-q-positive-Hessian-source-or-Jq-first-component-bound.md",
            "target_script": "scripts/Y5_R2FR_3611_xi_q_positive_Hessian_source_or_Jq_first_component_bound.py",
            "objective": "try to derive/source xi_q and the positive Hessian branch that makes lambda_q=xi_q; if that cannot close, immediately fill the first J_q component bound for matter/constants or body/boundary",
            "success_gate": "must produce either an owned xi_q/H_AB row or a theorem-zero/source-backed bound for at least one leading J_q component; no new target-only ledger",
            "reason": "3610 upgrades q from an abstract missing operator to a concrete range/Hessian/source-envelope problem",
            "valid_for_claim": False,
        }
    ]


def validation_rows(
    source_map: dict[str, tuple[Path, str]],
    out_paths: dict[str, Path],
    pi_rows_: list[dict[str, object]],
    dpi_rows_: list[dict[str, object]],
    extraction: list[dict[str, object]],
    decisions: list[dict[str, object]],
    status: list[dict[str, object]],
    next_target: list[dict[str, object]],
) -> list[dict[str, object]]:
    validations: list[tuple[str, bool, str]] = []
    validations.append(("VAL3610_0_sources_exist", all(path.exists() for path, _ in source_map.values()), "all required 3610 source paths exist"))
    validations.append(("VAL3610_1_needles_found", all(path.exists() and contains(path, needle) for path, needle in source_map.values()), "all selected 3610 source anchors found"))
    pre_validation = {key: path for key, path in out_paths.items() if key != "validation"}
    validations.append(("VAL3610_2_outputs_exist", all(path.exists() for path in pre_validation.values()), "all pre-validation 3610 csv outputs written"))
    parse_ok = True
    parse_details: list[str] = []
    for output_id, path in pre_validation.items():
        try:
            parse_details.append(f"{output_id}:{len(read_csv(path))}")
        except Exception as exc:
            parse_ok = False
            parse_details.append(f"{output_id}:ERROR:{exc}")
    validations.append(("VAL3610_3_csv_parse", parse_ok, "; ".join(parse_details)))
    required_symbols = {"Gamma_eff; K_hat; q_loc^nu", "P_loc; Pi_M", "chi_D; Qcoh; memory; flow", "EM Hodge/Maxwell/Poynting residuals", "kappa_eff; G_eff", "q_private"}
    validations.append(
        (
            "VAL3610_4_actual_MTS_symbols_mapped",
            required_symbols.issubset({str(row["MTS_symbol"]) for row in pi_rows_}),
            "actual MTS symbols are placed in the pi/kernel map",
        )
    )
    validations.append(
        (
            "VAL3610_5_dpi_certificate_not_falsely_signed",
            any(row["certificate_id"] == "DPI3610_8_verdict" and row["current_status"] == "NOT_CERTIFIED_CURRENT_CORPUS" for row in dpi_rows_),
            "Dpi[v_q] certificate remains unclaimed",
        )
    )
    required_extract = {"M_q^2", "Z_q", "lambda_q", "J_q", "J_q^abs", "q residual bound"}
    validations.append(
        (
            "VAL3610_6_Zq_Jq_rows_extracted",
            required_extract.issubset({str(row["symbol"]) for row in extraction}),
            "Zq/Mq/lambda and Jq extraction rows present",
        )
    )
    validations.append(
        (
            "VAL3610_7_lambda_equals_xi_recorded",
            any(row["symbol"] == "lambda_q" and "xi_q" in str(row["formula"]) for row in extraction),
            "lambda_q=xi_q conditional ratio recorded",
        )
    )
    validations.append(
        (
            "VAL3610_8_no_claim_flags",
            not any(str(row.get("claim_allowed", "False")) == "True" or str(row.get("valid_for_claim", "False")) == "True" for table in [pi_rows_, dpi_rows_, extraction, decisions, status, next_target] for row in table),
            "all generated physics rows remain nonclaim",
        )
    )
    validations.append(
        (
            "VAL3610_9_next_target_selected",
            next_target[0]["next_id"] == "NEXT3610_0",
            "3611 xi_q/Hessian or Jq component target selected",
        )
    )
    formalization_leaks: list[str] = []
    if FORMALIZATION.exists():
        for pattern in ["*3610*", "P8_Y5_R2FR_3610*", "P8_Y5_BRR545_3610*"]:
            formalization_leaks.extend(str(path) for path in FORMALIZATION.rglob(pattern) if ".venv" not in path.parts and "__pycache__" not in path.parts)
    validations.append(
        (
            "VAL3610_10_formalization_workbench_untouched",
            len(formalization_leaks) == 0,
            "no 3610 checkpoint output appears in formalization-workbench outside package/venv noise",
        )
    )
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "validation_id": validation_id,
            "result": "PASS" if passed else "FAIL",
            "detail": detail,
            "valid_for_claim": False,
        }
        for validation_id, passed, detail in validations
    ]


def write_doc(
    pi_rows_: list[dict[str, object]],
    dpi_rows_: list[dict[str, object]],
    extraction: list[dict[str, object]],
    decisions: list[dict[str, object]],
    status: list[dict[str, object]],
    next_target: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    status_row = status[0]
    lines = [
        "# 3610 - parent pi/vq certificate or Zq/Jq extraction",
        "",
        "## Verdict",
        "3610 turns the post-3609 fork into a concrete MTS object.",
        "",
        "`pi_MTS` is now written over actual MTS symbols: public geometry/coframe, tau, matter/constants, boundary class, coupling slots, projector/readout maps, plus excluded `q_private` and the local silence multiplet `Y_loc`.",
        "",
        "The no-pole certificate still does not close because `Dpi[v_q]=0` is unsigned component-by-component.  But the fallback is much sharper than a blank bound row:",
        "",
        "`M_q^2 = n_q^A H_AB n_q^B`, `Z_q = xi_q^2 n_q^A H_AB n_q^B`, therefore `lambda_q = sqrt(Z_q/M_q^2) = xi_q`.",
        "",
        "So if `q` is physical, its range is not arbitrary in this branch; it is the parent smoothing/correlation length `xi_q`.  That is the next derivation target.",
        "",
        "## pi_MTS Symbol Map",
    ]
    for row in pi_rows_:
        lines.append(f"- `{row['map_id']}` / `{row['MTS_symbol']}`: {row['current_status']} - {row['effect_or_guard']}")
    lines.extend(["", "## Dpi[v_q] Certificate"])
    for row in dpi_rows_:
        lines.append(f"- `{row['certificate_id']}` / `{row['component']}`: {row['current_status']} - {row['consequence']}")
    lines.extend(["", "## Zq/Jq Extraction"])
    for row in extraction:
        lines.append(f"- `{row['extract_id']}` / `{row['symbol']}`: {row['current_status']} - `{row['formula']}`")
    lines.extend(["", "## Decision Gates"])
    for row in decisions:
        lines.append(f"- `{row['decision_id']}` / `{row['gate']}`: {row['status']} - {row['consequence']}")
    lines.extend(
        [
            "",
            "## Status",
            f"- `{status_row['status']}`: {status_row['strongest_result']}",
            f"- Decision: {status_row['decision']}",
            f"- Framework progress: {status_row['framework_progress']}",
            f"- Still missing: {status_row['still_missing']}",
            "",
            "## Validation",
        ]
    )
    for row in validation:
        lines.append(f"- `{row['validation_id']}`: {row['result']} ({row['detail']})")
    next_row = next_target[0]
    lines.extend(
        [
            "",
            "## Next Target",
            f"- `{next_row['next_id']}` -> `{next_row['target_doc']}`",
            f"- Objective: {next_row['objective']}",
            f"- Success gate: {next_row['success_gate']}",
        ]
    )
    DOC.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    source_map = sources()
    out_paths = outputs()
    source_rows = source_register_rows(source_map)
    pi_rows_ = parent_pi_rows(source_map)
    dpi_rows_ = dpi_rows(source_map)
    extraction = extraction_rows(source_map)
    decisions = decision_rows(source_map)
    status = status_rows(source_map)
    next_target = next_target_rows()

    write_csv(out_paths["source_register"], source_rows)
    write_csv(out_paths["parent_pi_symbol_map"], pi_rows_)
    write_csv(out_paths["dpi_vq_certificate"], dpi_rows_)
    write_csv(out_paths["zq_jq_extraction_rows"], extraction)
    write_csv(out_paths["decision_gates"], decisions)
    write_csv(out_paths["status"], status)
    write_csv(out_paths["next_target"], next_target)
    write_csv(out_paths["canonical_status"], status)

    validation = validation_rows(source_map, out_paths, pi_rows_, dpi_rows_, extraction, decisions, status, next_target)
    write_doc(pi_rows_, dpi_rows_, extraction, decisions, status, next_target, validation)
    write_csv(out_paths["validation"], validation)

    failures = [row for row in validation if row["result"] != "PASS"]
    if failures:
        for failure in failures:
            print(f"{failure['validation_id']}: {failure['detail']}")
        raise SystemExit(1)
    print(f"wrote 3610 pi/vq and Zq/Jq outputs under {RESIDUALS}")
    print(f"wrote {DOC}")


if __name__ == "__main__":
    main()
