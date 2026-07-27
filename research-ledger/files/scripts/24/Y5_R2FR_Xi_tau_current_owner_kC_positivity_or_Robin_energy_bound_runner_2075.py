from __future__ import annotations

from pathlib import Path

from Y5_R2FR_Dq_vX_observed_metric_zero_or_finite_DObs_leak_row_2025 import (
    BRANCH_WEP,
    OUT,
    QUEUE,
    ROOT,
    SOURCE_WEIGHT_DOCS,
    base_row,
    count_formalization_modified,
    csv_rows_parse,
    md_table,
    read_text,
    remove_pycache,
    write_csv,
)


DOC = ROOT / "2075-Y5-R2FR-Xi-tau-current-owner-kC-positivity-or-Robin-energy-bound-runner.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
SCRIPT_PATH = Path(__file__).resolve()


def formalization_has_2075_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    patterns = (
        "*2075-Y5-R2FR*",
        "*P8_Y5_PARENT_QLOC_2075*",
        "*Y5_R2FR_Xi_tau_current_owner_kC_positivity_or_Robin_energy_bound_runner_2075*",
    )
    try:
        return any(path.is_file() for pattern in patterns for path in FORMALIZATION.rglob(pattern))
    except Exception:
        return False


def scripts_pycache_exists() -> bool:
    return (SCRIPT_PATH.parent / "__pycache__").exists()


def source_register_rows() -> list[dict[str, object]]:
    specs = [
        (
            "SRC2075_00_2074_doc",
            ROOT / "2074-Y5-R2FR-Robin-Bmix-positivity-and-boundary-silence-or-finite-residual-fill.md",
            ["NEXT2074_0_2075", "k_C = 2 beta_mix c2 Xi_tau mu_C", "COUPLING_IS_THE_NEXT_LOCK"],
            "2074 handoff: attack Xi_tau/k_C or build Robin energy-bound runner.",
        ),
        (
            "SRC2075_01_2074_kc",
            OUT / "P8_Y5_PARENT_QLOC_2074_KC_XITAU_POSITIVITY_AUDIT.csv",
            ["KXP2074_0_formula", "MISSING_PARENT_XI_TAU", "KC_POSITIVITY_BLOCKED"],
            "machine-readable k_C/Xi_tau positivity blocker.",
        ),
        (
            "SRC2075_02_2072_bmix",
            OUT / "P8_Y5_PARENT_QLOC_2072_BMIX_GENERIC_VARIATION_THEOREM.csv",
            ["BVT2072_0_generic_ansatz", "BVT2072_4_quadratic_minimum", "DOUBLE_ZERO_SELECTION_LAW_DERIVED"],
            "Bmix double-zero algebra and quadratic minimum.",
        ),
        (
            "SRC2075_03_1008_variation",
            OUT / "P8_Y5_R10_1008_PARENT_VARIATION_AUDIT.csv",
            ["PVA1008_0_parent_action", "PVA1008_2_J_tau", "PVA1008_6_verdict"],
            "theta_MTS/J_tau/Q_tau extraction contract exists but is not closed.",
        ),
        (
            "SRC2075_04_1008_charge",
            OUT / "P8_Y5_R10_1008_CHARGE_PIECE_LEDGER.csv",
            ["QTA1008_0_L_parent", "QTA1008_2_J_tau", "QTA1008_8_Q_total"],
            "charge-piece ledger blocks Xi_tau parent ownership.",
        ),
        (
            "SRC2075_05_1009_contract",
            OUT / "P8_Y5_R10_1009_PARENT_SECTOR_CONTRACT.csv",
            ["PCS1009_9_total_parent_contract", "J_tau=dQ_tau^MTS+C_tau", "not_promoted"],
            "total parent current-chain contract remains unsigned.",
        ),
        (
            "SRC2075_06_1009_variations",
            OUT / "P8_Y5_R10_1009_SECTOR_VARIATION_CANDIDATES.csv",
            ["SVC1009_6_total_parent_switch_unsigned", "MISSING_SIGNED_PARENT_ACTION_SOURCE", "theta_MTS=sum theta_i"],
            "sector variation candidates do not promote a total action.",
        ),
        (
            "SRC2075_07_1487_action_object",
            ROOT / "1487-Y5-R10-RAB-parent-action-object-current-chain-ownership-or-explicit-axiom-debt.md",
            ["TQO1487_1_theta_total", "TQO1487_3_Qpieces", "NOT_EXTRACTED"],
            "later audit agrees theta/Q_tau remains template/piece-split only.",
        ),
        (
            "SRC2075_08_2068_cap_norm",
            OUT / "P8_Y5_PARENT_QLOC_2068_CAP_NORMALIZATION_ATTEMPT.csv",
            ["TCN2068_2_Ccap_norm", "MISSING_K_CAP_TO_PIR_MAP", "MISSING_QR_NORMALIZATION_CHAIN"],
            "cap normalization is diagnostic only; physical Pi_R/q_R conversion is unclosed.",
        ),
        (
            "SRC2075_09_2062_boundary",
            OUT / "P8_Y5_PARENT_QLOC_2062_BOUNDARY_FUNCTIONAL_GRAMMAR.csv",
            ["BGA2062_3_corner_worldtube", "BGA2062_4_orientation", "Q_R = W_R n^mu partial_mu R_AB"],
            "cap measure/orientation and corner terms remain unsigned.",
        ),
        (
            "SRC2075_10_1249_qrhat",
            OUT / "P8_Y5_R10_1249_FINITE_QRHAT_CANDIDATE_RESULTS.csv",
            ["QRHAT1255_CASSINI_GAMMA_1SIGMA_BOUND_NONCLAIM", "ACCEPTED_NONCLAIM_FINITE_QRHAT", "REJECT_ZERO_THEOREM_UNDERIVED"],
            "q_R_hat comparator is available only as a nonclaim policy ceiling.",
        ),
    ]
    rows: list[dict[str, object]] = []
    for source_id, source_path, needles, note in specs:
        exists = source_path.exists()
        text = read_text(source_path) if exists else ""
        ok = exists and all(needle in text for needle in needles)
        row = base_row()
        row.update(
            {
                "source_id": source_id,
                "source_kind": "local",
                "source_path": str(source_path),
                "status": "EXISTS_NEEDLES_CONFIRMED" if ok else "MISSING_OR_NEEDLE_FAIL",
                "needles": ";".join(needles),
                "note": note,
                "claim_allowed": False,
            }
        )
        rows.append(row)
    return rows


def xitau_owner_rows() -> list[dict[str, object]]:
    data = [
        (
            "XTO2075_0_parent_variation",
            "parent action current chain",
            "delta L_parent = E_A delta Phi^A + d theta_MTS(Phi;delta Phi)",
            "1008/1009 provide the exact contract, but no single total retained-sector parent action is signed.",
            "CONTRACT_EXISTS_PARENT_ACTION_UNSIGNED",
            False,
        ),
        (
            "XTO2075_1_noether_current",
            "tau Noether current",
            "J_tau = theta_MTS(Phi; Lie_tau Phi) - i_tau L_parent, with J_tau = dQ_tau^MTS + C_tau on shell",
            "formal shape exists; tau action on metric, matter, representative, boundary/reference and extra fields is not fixed.",
            "FORMAL_SHAPE_NO_TOTAL_OWNER",
            False,
        ),
        (
            "XTO2075_2_cap_scalar_definition",
            "Xi_tau candidate",
            "Xi_tau[C] := mu_C^{-1} pull_C(i_{n_C} J_tau) or equivalently a cap Hamiltonian-current density after fixed reference subtraction",
            "this is the clean definition of what Xi_tau must be, but it is only meaningful after J_tau, mu_C and reference subtraction are parent owned.",
            "EXACT_CONDITIONAL_DEFINITION_NOT_EXTRACTED",
            False,
        ),
        (
            "XTO2075_3_piece_split",
            "Q_tau^MTS pieces",
            "Q_tau^MTS = Q_EH + Q_boundary + Q_extra + Q_projector + Q_matter/source",
            "1008 marks the non-EH pieces as not extracted/not promoted; EH-only import is rejected.",
            "PIECE_SPLIT_NOT_PROMOTED",
            False,
        ),
        (
            "XTO2075_4_sign",
            "sign of Xi_tau",
            "a signed current density can change sign with orientation/reference/improvement unless a positive energy-density owner is specified",
            "raw Xi_tau is not sign-safe enough to activate k_C>=0.",
            "RAW_SIGN_NOT_CERTIFIED",
            False,
        ),
        (
            "XTO2075_5_verdict",
            "Xi_tau ownership",
            "2075 defines the exact cap-current object Xi_tau would have to be, but does not extract it from a parent action",
            "best next move is a positive current-density cap functional, not a raw signed Xi_tau multiplier.",
            "XITAU_DEFINED_CONDITIONALLY_NOT_PARENT_SIGNED",
            False,
        ),
    ]
    rows: list[dict[str, object]] = []
    for row_id, object_id, formula, evidence, status, parent_signed in data:
        row = base_row()
        row.update(
            {
                "row_id": row_id,
                "object_id": object_id,
                "formula": formula,
                "evidence": evidence,
                "status": status,
                "parent_signed": parent_signed,
                "ready_for_scoring": False,
                "claim_allowed": False,
            }
        )
        rows.append(row)
    return rows


def kc_route_selector_rows() -> list[dict[str, object]]:
    data = [
        (
            "KRS2075_0_raw_signed",
            "raw signed-current route",
            "k_C = 2 beta_mix c2 Xi_tau mu_C",
            "needs sign(beta_mix c2 Xi_tau mu_C)>=0 across the local cap",
            "FAIL_SIGN_UNSIGNED",
            "do not activate; Xi_tau and beta_mix are not parent signed.",
        ),
        (
            "KRS2075_1_choose_beta_after_fact",
            "post-hoc beta sign choice",
            "choose beta_mix to cancel the observed Xi_tau sign",
            "would tune after the branch/reference is known unless fixed by parent symmetry",
            "REJECT_AS_FITTED_SIGN",
            "not a derivation route.",
        ),
        (
            "KRS2075_2_absolute_current",
            "absolute-value current route",
            "k_C proportional to |Xi_tau|",
            "positive but non-smooth at Xi_tau=0 unless a parent norm functional is supplied",
            "REJECT_RAW_ABS_WITHOUT_PARENT_NORM",
            "could be repaired only as a genuine norm/square density.",
        ),
        (
            "KRS2075_3_positive_density",
            "positive current-density route",
            "B_mix,C = 1/2 integral_C mu_C lambda_C I_tau (DeltaR)^2 with lambda_C>=0 and I_tau>=0",
            "turns the coupling into a positive stiffness rather than a raw signed-current multiplier",
            "BEST_CANDIDATE_NOT_PARENT_ADOPTED",
            "derive I_tau from J_tau norm or cap Hamiltonian density before claiming.",
        ),
        (
            "KRS2075_4_topological_level",
            "positive topological/level route",
            "k_C fixed by an integer/positive level times a cap measure density",
            "could sign stiffness without raw Xi_tau, but would need a topological sector and units",
            "POSSIBLE_BUT_UNSOURCED",
            "keep as alternate source hunt.",
        ),
        (
            "KRS2075_5_verdict",
            "k_C route selection",
            "raw Xi_tau route remains blocked; positive current-density route is the least scrutiny-prone next derivation attempt",
            "selects a route without promoting a local claim",
            "SELECT_POSITIVE_DENSITY_ROUTE_NONCLAIM",
            "2076 should try to parent-source I_tau and lambda_C.",
        ),
    ]
    rows: list[dict[str, object]] = []
    for row_id, route, candidate_formula, condition, verdict, note in data:
        row = base_row()
        row.update(
            {
                "row_id": row_id,
                "route": route,
                "candidate_formula": candidate_formula,
                "condition": condition,
                "verdict": verdict,
                "note": note,
                "accepted_as_candidate": verdict in {"BEST_CANDIDATE_NOT_PARENT_ADOPTED", "SELECT_POSITIVE_DENSITY_ROUTE_NONCLAIM"},
                "claim_allowed": False,
            }
        )
        rows.append(row)
    return rows


def positive_density_contract_rows() -> list[dict[str, object]]:
    data = [
        (
            "PDC2075_0_density",
            "I_tau",
            "I_tau := ||J_tau^cap||_h^2/H_*^2 or (delta H_tau^cap/H_*)^2",
            "I_tau>=0 if the cap inner product h and positive same-frame denominator H_* are parent signed",
            "POSITIVE_BY_CONSTRUCTION_IF_PARENT_OWNED",
        ),
        (
            "PDC2075_1_stiffness",
            "k_C",
            "k_C := lambda_C mu_C I_tau with lambda_C>=0",
            "stiffness is nonnegative if lambda_C, mu_C orientation and I_tau are signed before readout",
            "KC_POSITIVE_IF_CONTRACT_SIGNED",
        ),
        (
            "PDC2075_2_action",
            "B_mix,C",
            "B_mix,C := 1/2 integral_C k_C (R_AB-R_star)^2",
            "preserves the 2072 double-zero law while replacing raw signed Xi_tau with a positive density",
            "SAME_DOUBLE_ZERO_SHAPE",
        ),
        (
            "PDC2075_3_units",
            "unit closure",
            "lambda_C supplies the unit conversion from current-density norm to W_R/length stiffness units",
            "requires source row for lambda_C and denominator H_*",
            "MISSING_UNITS_AND_DENOMINATOR",
        ),
        (
            "PDC2075_4_reference_guard",
            "fixed reference",
            "delta H_tau^cap and J_tau^cap must be computed after fixed-before-readout boundary/reference subtraction",
            "otherwise a counterterm can fake positivity or normalization",
            "MISSING_FIXED_REFERENCE_CERTIFICATE",
        ),
        (
            "PDC2075_5_verdict",
            "positive-density cap functional",
            "mathematically cleaner than raw Xi_tau, but still a parent-action candidate rather than an adopted theorem",
            "needed certificates: J_tau owner, cap norm h, H_*, lambda_C, mu_C orientation, source/reference split",
            "CANDIDATE_PARENT_FUNCTIONAL_NOT_ADOPTED",
        ),
    ]
    rows: list[dict[str, object]] = []
    for row_id, object_id, formula, condition, status in data:
        row = base_row()
        row.update(
            {
                "row_id": row_id,
                "object_id": object_id,
                "formula": formula,
                "condition": condition,
                "status": status,
                "parent_signed": False,
                "ready_for_scoring": False,
                "claim_allowed": False,
            }
        )
        rows.append(row)
    return rows


def energy_bound_input_rows() -> list[dict[str, object]]:
    data = [
        ("EBI2075_0_Wmin", "W_R_min", "positive lower bound for reciprocal bulk operator", "W_R units", "MISSING_PARENT_W_R_MIN"),
        ("EBI2075_1_kmin", "k_C_min", "positive lower bound for cap stiffness", "W_R/length units", "MISSING_PARENT_K_C_MIN"),
        ("EBI2075_2_CP", "C_Poincare", "annulus Poincare/coercivity constant", "geometry units", "MISSING_GEOMETRY_CONSTANT"),
        ("EBI2075_3_CT", "C_trace", "cap trace constant linking boundary norm to energy norm", "geometry units", "MISSING_TRACE_CONSTANT"),
        ("EBI2075_4_rho", "rho_R_norm", "bulk reciprocal source dual norm", "dual source units", "MISSING_BULK_SOURCE_NORM"),
        ("EBI2075_5_bC", "b_C_norm", "cap boundary/source-reference residue norm", "dual boundary units", "MISSING_BOUNDARY_RESIDUE_NORM"),
        ("EBI2075_6_Fouter", "F_outer_abs", "absolute outer/asymptotic flux after reference subtraction", "energy-like units", "MISSING_OUTER_FLUX_BOUND"),
        ("EBI2075_7_KqR", "K_qR", "map from DeltaR energy norm to q_R_hat", "dimensionless per norm", "MISSING_QRHAT_MAP"),
        ("EBI2075_8_qRlimit", "q_R_hat_policy_ceiling", "external policy ceiling, e.g. QRHAT1255 nonclaim row", "dimensionless", "AVAILABLE_AS_NONCLAIM_CEILING_ONLY"),
    ]
    rows: list[dict[str, object]] = []
    for row_id, quantity, definition, units, status in data:
        row = base_row()
        row.update(
            {
                "row_id": row_id,
                "quantity": quantity,
                "definition": definition,
                "units": units,
                "value": f"MISSING_{quantity}",
                "status": status,
                "ready_for_scoring": False,
                "claim_allowed": False,
            }
        )
        rows.append(row)
    return rows


def energy_bound_runner_rows() -> list[dict[str, object]]:
    data = [
        (
            "EBR2075_0_symbolic_law",
            "symbolic energy-bound runner",
            "a := C_Poincare*rho_R_norm + C_trace*b_C_norm; X_E <= 0.5*(a + sqrt(a^2 + 4*F_outer_abs)); q_R_hat <= K_qR*X_E",
            "derived from X_E^2 <= F_outer_abs + a X_E",
            "SYMBOLIC_RUNNER_DERIVED",
            False,
        ),
        (
            "EBR2075_1_placeholder_input",
            "current template input row",
            "W_R_min,k_C_min,C_Poincare,C_trace,rho_R_norm,b_C_norm,F_outer_abs,K_qR are all placeholders",
            "no numeric execution allowed",
            "BLOCKED_MISSING_NUMERIC_INPUTS",
            False,
        ),
        (
            "EBR2075_2_claim_rule",
            "finite residual claim rule",
            "valid_for_claim=true only when every input is numeric, sourced, unit-compatible, same-frame and no MISSING markers remain",
            "prevents a symbolic bound from becoming evidence",
            "STRICT_NONCLAIM_UNTIL_INPUTS_FILLED",
            False,
        ),
        (
            "EBR2075_3_policy_compare",
            "future q_R_hat comparison",
            "compare q_R_hat_predicted <= q_R_hat_policy_ceiling only after EBR2075_2 is satisfied",
            "1249 ceiling is not itself an MTS prediction",
            "COMPARISON_DEFERRED",
            False,
        ),
    ]
    rows: list[dict[str, object]] = []
    for run_id, runner_object, formula_or_input, rule, status, accepted_for_scoring in data:
        row = base_row()
        row.update(
            {
                "run_id": run_id,
                "runner_object": runner_object,
                "formula_or_input": formula_or_input,
                "rule": rule,
                "status": status,
                "accepted_for_scoring": accepted_for_scoring,
                "claim_allowed": False,
            }
        )
        rows.append(row)
    return rows


def claim_gate_rows() -> list[dict[str, object]]:
    data = [
        (
            "GATE2075_0_Xi_definition",
            "Xi_tau cap-current definition exists",
            "PASS_CONDITIONAL_DEFINITION",
            "Xi_tau can be defined as a cap pullback/current density if J_tau and references are parent owned.",
        ),
        (
            "GATE2075_1_Xi_extracted",
            "Xi_tau extracted from parent theta/Q_tau",
            "FAIL_BLOCKED",
            "theta_MTS/Q_tau^MTS remain unextracted across retained sectors.",
        ),
        (
            "GATE2075_2_raw_kC",
            "raw k_C=2 beta_mix c2 Xi_tau mu_C can be signed",
            "FAIL_BLOCKED",
            "raw signed-current route lacks beta_mix, Xi_tau and mu_C sign certificates.",
        ),
        (
            "GATE2075_3_positive_density",
            "positive-density cap functional is adopted by parent action",
            "FAIL_BLOCKED",
            "route is selected as best candidate but lacks J_tau norm, H_*, lambda_C and cap geometry certificates.",
        ),
        (
            "GATE2075_4_energy_runner",
            "Robin energy-bound runner can score",
            "FAIL_BLOCKED",
            "symbolic law exists, but all numeric/source inputs are placeholders.",
        ),
        (
            "GATE2075_5_local_claim",
            "local GR/Newton/PPN/R10 claim",
            "FAIL_BLOCKED",
            "no signed k_C theorem and no finite q_R_hat prediction.",
        ),
        (
            "GATE2075_6_formalization",
            "formalization-workbench edit allowed",
            "PASS_NO_EDIT",
            "2075 stays in post-checkpoint-work.",
        ),
    ]
    rows: list[dict[str, object]] = []
    for row_id, gate, status, detail in data:
        row = base_row()
        row.update({"row_id": row_id, "gate": gate, "status": status, "detail": detail, "claim_allowed": False})
        rows.append(row)
    return rows


def decision_rows() -> list[dict[str, object]]:
    data = [
        (
            "DEC2075_0_Xi_defined",
            "XITAU_CONTRACT_SHARPENED",
            "Xi_tau should be the cap pullback/current density derived from J_tau, not a free phenomenological symbol.",
        ),
        (
            "DEC2075_1_raw_route_blocked",
            "RAW_SIGNED_XITAU_ROUTE_NOT_SAFE",
            "raw k_C=2 beta_mix c2 Xi_tau mu_C cannot be signed without current orientation/reference ownership.",
        ),
        (
            "DEC2075_2_best_route",
            "SELECT_POSITIVE_CURRENT_DENSITY_CAP_FUNCTIONAL",
            "using I_tau>=0 from a parent current norm is the least smuggled route to k_C>=0.",
        ),
        (
            "DEC2075_3_runner",
            "ENERGY_BOUND_RUNNER_LAW_WRITTEN",
            "if the zero theorem remains blocked, finite q_R_hat can be bounded from X_E <= 0.5*(a+sqrt(a^2+4F)).",
        ),
    ]
    rows: list[dict[str, object]] = []
    for row_id, decision, rationale in data:
        row = base_row()
        row.update({"row_id": row_id, "decision": decision, "rationale": rationale, "claim_allowed": False})
        rows.append(row)
    return rows


def next_target_rows() -> list[dict[str, object]]:
    row = base_row()
    row.update(
        {
            "target_id": "NEXT2075_0_2076",
            "target_doc": "2076-Y5-R2FR-positive-current-density-cap-functional-or-first-numeric-energy-bound-inputs.md",
            "objective": "try to construct a parent-owned positive current-density cap functional I_tau and lambda_C that signs k_C>=0; if that fails, fill the first numeric/sourced Robin energy-bound input rows",
            "must_include": "J_tau cap norm; fixed reference subtraction; H_* positive denominator; lambda_C units; mu_C orientation; k_C_min; W_R_min; C_Poincare/C_trace; q_R_hat map; strict nonclaim runner output",
            "excluded": "raw absolute value without parent norm; post-fit beta sign; EH-only theta/Q_tau import; closure q_R_hat=0; local-GR/PPN/R10 claim; GitHub; formalization-workbench edits",
            "claim_allowed": False,
        }
    )
    return [row]


def write_branch_copies(
    xitau: list[dict[str, object]],
    routes: list[dict[str, object]],
    density: list[dict[str, object]],
    inputs: list[dict[str, object]],
    runner: list[dict[str, object]],
    next_rows_: list[dict[str, object]],
) -> list[dict[str, object]]:
    copies = [
        (
            "COPY2075_0_source_weight_xitau",
            SOURCE_WEIGHT_DOCS / "AFRAME_XITAU_CURRENT_OWNER_2075_NONCLAIM.csv",
            xitau,
        ),
        (
            "COPY2075_1_source_weight_kc_routes",
            SOURCE_WEIGHT_DOCS / "AFRAME_KC_ROUTE_SELECTOR_2075_NONCLAIM.csv",
            routes,
        ),
        (
            "COPY2075_2_source_weight_positive_density",
            SOURCE_WEIGHT_DOCS / "AFRAME_POSITIVE_CURRENT_DENSITY_CAP_CONTRACT_2075_NONCLAIM.csv",
            density,
        ),
        (
            "COPY2075_3_source_weight_energy_inputs",
            SOURCE_WEIGHT_DOCS / "AFRAME_ROBIN_ENERGY_BOUND_INPUT_TEMPLATE_2075_NONCLAIM.csv",
            inputs,
        ),
        (
            "COPY2075_4_wep_runner",
            BRANCH_WEP / "P8_Y5_PARENT_QLOC_2075_ROBIN_ENERGY_BOUND_RUNNER_NONCLAIM.csv",
            runner,
        ),
        (
            "COPY2075_5_queue_next",
            QUEUE / "JR2075_POSITIVE_CURRENT_DENSITY_OR_ENERGY_INPUTS_NEXT_NONCLAIM.csv",
            next_rows_,
        ),
    ]
    rows: list[dict[str, object]] = []
    for copy_id, path, data in copies:
        write_csv(path, data)
        row = base_row()
        row.update({"copy_id": copy_id, "path": str(path), "rows": len(data), "status": "WRITTEN_NONCLAIM_COPY", "claim_allowed": False})
        rows.append(row)
    return rows


def validation_rows(
    sources: list[dict[str, object]],
    xitau: list[dict[str, object]],
    routes: list[dict[str, object]],
    density: list[dict[str, object]],
    inputs: list[dict[str, object]],
    runner: list[dict[str, object]],
    gates: list[dict[str, object]],
    next_rows_: list[dict[str, object]],
    copies: list[dict[str, object]],
    csv_paths: list[Path],
) -> list[dict[str, object]]:
    source_ok = all(row["status"] == "EXISTS_NEEDLES_CONFIRMED" for row in sources)
    csv_ok = all(csv_rows_parse(path) for path in csv_paths)
    xitau_ok = any(row["row_id"] == "XTO2075_2_cap_scalar_definition" and row["status"] == "EXACT_CONDITIONAL_DEFINITION_NOT_EXTRACTED" for row in xitau) and any(
        row["row_id"] == "XTO2075_5_verdict" and row["status"] == "XITAU_DEFINED_CONDITIONALLY_NOT_PARENT_SIGNED" for row in xitau
    )
    route_ok = any(row["row_id"] == "KRS2075_0_raw_signed" and row["verdict"] == "FAIL_SIGN_UNSIGNED" for row in routes) and any(
        row["row_id"] == "KRS2075_5_verdict" and row["verdict"] == "SELECT_POSITIVE_DENSITY_ROUTE_NONCLAIM" for row in routes
    )
    density_ok = any(row["row_id"] == "PDC2075_0_density" and "I_tau>=0" in str(row["condition"]) for row in density) and any(
        row["row_id"] == "PDC2075_5_verdict" and row["status"] == "CANDIDATE_PARENT_FUNCTIONAL_NOT_ADOPTED" for row in density
    )
    input_keys = {"W_R_min", "k_C_min", "C_Poincare", "C_trace", "rho_R_norm", "b_C_norm", "F_outer_abs", "K_qR", "q_R_hat_policy_ceiling"}
    input_quantities = {str(row["quantity"]) for row in inputs}
    inputs_ok = input_keys.issubset(input_quantities) and all(str(row["value"]).startswith("MISSING_") or row["quantity"] == "q_R_hat_policy_ceiling" for row in inputs)
    runner_ok = any(row["run_id"] == "EBR2075_0_symbolic_law" and "sqrt" in str(row["formula_or_input"]) for row in runner) and any(
        row["run_id"] == "EBR2075_1_placeholder_input" and row["status"] == "BLOCKED_MISSING_NUMERIC_INPUTS" for row in runner
    )
    gates_ok = all(row["claim_allowed"] is False and row["status"] != "PASS_CLAIM" for row in gates)
    next_ok = next_rows_[0]["target_id"] == "NEXT2075_0_2076"
    copies_ok = all(Path(str(row["path"])).exists() and csv_rows_parse(Path(str(row["path"]))) for row in copies)
    no_claim = all(
        not bool(row.get("claim_allowed", False)) and not bool(row.get("valid_for_claim", False))
        for group in [sources, xitau, routes, density, inputs, runner, gates, next_rows_, copies]
        for row in group
    )
    checks = [
        ("VAL2075_00_local_sources_exist", source_ok, "all cited source paths and needles exist"),
        ("VAL2075_01_csv_parse", csv_ok, "all generated CSV files parse cleanly"),
        ("VAL2075_02_xitau_contract", xitau_ok, "Xi_tau cap-current contract is defined conditionally but not extracted"),
        ("VAL2075_03_route_selection", route_ok, "raw signed Xi_tau route is blocked and positive-density route selected as nonclaim candidate"),
        ("VAL2075_04_positive_density_contract", density_ok, "positive current-density cap functional contract is written but not adopted"),
        ("VAL2075_05_energy_input_template", inputs_ok, "energy-bound input template contains all required placeholders"),
        ("VAL2075_06_symbolic_runner", runner_ok, "symbolic Robin energy-bound runner law is written and placeholder run is blocked"),
        ("VAL2075_07_claim_gates_blocked", gates_ok, "all local claim gates remain blocked/nonclaim"),
        ("VAL2075_08_next_selected", next_ok, "2076 positive-density or numeric energy-input target selected"),
        ("VAL2075_09_branch_copies", copies_ok, "branch copies exist and parse"),
        ("VAL2075_10_no_claim_flags", no_claim, "no generated row allows a claim"),
        ("VAL2075_11_formalization_unchanged", count_formalization_modified() == 0, "formalization-workbench modified-file count remains 0"),
        ("VAL2075_12_no_formalization_artifacts", not formalization_has_2075_artifacts(), "no 2075 artifacts were written under formalization-workbench"),
        ("VAL2075_13_no_pycache", not scripts_pycache_exists(), "scripts __pycache__ removed"),
    ]
    overall = all(ok for _, ok, _ in checks)
    checks.append(("VAL2075_OVERALL", overall, "2075 sharpens Xi_tau, rejects raw signed coupling, and writes the positive-density/energy-bound route"))
    rows: list[dict[str, object]] = []
    for check_id, ok, detail in checks:
        row = base_row()
        row.update({"check_id": check_id, "status": "PASS" if ok else "FAIL", "detail": detail, "claim_allowed": False})
        rows.append(row)
    return rows


def write_doc(
    sources: list[dict[str, object]],
    xitau: list[dict[str, object]],
    routes: list[dict[str, object]],
    density: list[dict[str, object]],
    inputs: list[dict[str, object]],
    runner: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_rows_: list[dict[str, object]],
    copies: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    sections = [
        "# 2075 Y5 R2FR Xi Tau Current Owner kC Positivity Or Robin Energy Bound Runner",
        "",
        "## Current Verdict",
        "",
        "2075 makes the coupling problem sharper. `Xi_tau` is not allowed to remain a vague scalar. The exact object it would need to be is a cap pullback/current density derived from the parent Noether current `J_tau = theta_MTS(Phi; Lie_tau Phi) - i_tau L_parent`, with fixed reference subtraction and cap measure/orientation already owned.",
        "",
        "That definition is only conditional because the current corpus still does not extract `theta_MTS`, `J_tau`, or `Q_tau^MTS` from a single retained-sector parent action. So the raw route `k_C = 2 beta_mix c2 Xi_tau mu_C` remains blocked: the sign of `Xi_tau`, `beta_mix`, and `mu_C` is not parent certified.",
        "",
        "The best route is therefore not to choose the sign after the fact. It is to replace raw signed `Xi_tau` with a parent-owned positive current density `I_tau>=0`, for example `I_tau := ||J_tau^cap||_h^2/H_*^2` or `(delta H_tau^cap/H_*)^2`, and use",
        "",
        "`B_mix,C = 1/2 integral_C mu_C lambda_C I_tau (R_AB-R_star)^2`, with `lambda_C>=0`.",
        "",
        "This preserves the 2072 double-zero shape while making the Robin stiffness sign-safe if the parent action owns the current norm, denominator, units, reference subtraction and cap orientation. It is a candidate derivation route, not a claim.",
        "",
        "2075 also writes the symbolic finite fallback runner: if `X_E` is the reciprocal energy norm, `a = C_Poincare*rho_R_norm + C_trace*b_C_norm`, then `X_E <= 0.5*(a + sqrt(a^2 + 4*F_outer_abs))` and `q_R_hat <= K_qR*X_E`. The runner is blocked until the numeric/source inputs are filled.",
        "",
        "No local-GR/Newton, Cassini, PPN, R10, WEP, clock, orbital, Kcap, q_R, or public claim is made. No GitHub action and no `formalization-workbench` edit is made.",
        "",
        "## Source Register",
        md_table(sources, ["source_id", "source_kind", "source_path", "status", "note", "valid_for_claim"]),
        "## Xi_tau Current Owner",
        md_table(xitau, ["row_id", "object_id", "formula", "evidence", "status", "parent_signed", "ready_for_scoring", "claim_allowed"]),
        "## k_C Route Selector",
        md_table(routes, ["row_id", "route", "candidate_formula", "condition", "verdict", "note", "accepted_as_candidate", "claim_allowed"]),
        "## Positive Current Density Contract",
        md_table(density, ["row_id", "object_id", "formula", "condition", "status", "parent_signed", "ready_for_scoring", "claim_allowed"]),
        "## Robin Energy Bound Input Template",
        md_table(inputs, ["row_id", "quantity", "definition", "units", "value", "status", "ready_for_scoring", "claim_allowed"]),
        "## Robin Energy Bound Runner",
        md_table(runner, ["run_id", "runner_object", "formula_or_input", "rule", "status", "accepted_for_scoring", "claim_allowed"]),
        "## Claim Gate",
        md_table(gates, ["row_id", "gate", "status", "detail", "claim_allowed"]),
        "## Decision Ledger",
        md_table(decisions, ["row_id", "decision", "rationale", "claim_allowed"]),
        "## Next Target",
        md_table(next_rows_, ["target_id", "target_doc", "objective", "must_include", "excluded", "claim_allowed"]),
        "## Branch Copies",
        md_table(copies, ["copy_id", "path", "rows", "status", "valid_for_claim"]),
        "## Validation",
        md_table(validation, ["check_id", "status", "detail", "claim_allowed"]),
    ]
    DOC.write_text("\n".join(sections), encoding="utf-8")


def main() -> None:
    sources = source_register_rows()
    xitau = xitau_owner_rows()
    routes = kc_route_selector_rows()
    density = positive_density_contract_rows()
    inputs = energy_bound_input_rows()
    runner = energy_bound_runner_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_rows_ = next_target_rows()
    paths = {
        "sources": OUT / "P8_Y5_PARENT_QLOC_2075_SOURCE_REGISTER.csv",
        "xitau": OUT / "P8_Y5_PARENT_QLOC_2075_XITAU_CURRENT_OWNER.csv",
        "routes": OUT / "P8_Y5_PARENT_QLOC_2075_KC_ROUTE_SELECTOR.csv",
        "density": OUT / "P8_Y5_PARENT_QLOC_2075_POSITIVE_CURRENT_DENSITY_CONTRACT.csv",
        "inputs": OUT / "P8_Y5_PARENT_QLOC_2075_ROBIN_ENERGY_BOUND_INPUT_TEMPLATE.csv",
        "runner": OUT / "P8_Y5_PARENT_QLOC_2075_ROBIN_ENERGY_BOUND_RUNNER.csv",
        "gates": OUT / "P8_Y5_PARENT_QLOC_2075_CLAIM_GATE.csv",
        "decision": OUT / "P8_Y5_PARENT_QLOC_2075_DECISION_LEDGER.csv",
        "next": OUT / "P8_Y5_PARENT_QLOC_2075_NEXT_TARGET.csv",
        "branch": OUT / "P8_Y5_PARENT_QLOC_2075_BRANCH_COPIES.csv",
        "validation": OUT / "P8_Y5_BRR545_2075_VALIDATION.csv",
    }
    write_csv(paths["sources"], sources)
    write_csv(paths["xitau"], xitau)
    write_csv(paths["routes"], routes)
    write_csv(paths["density"], density)
    write_csv(paths["inputs"], inputs)
    write_csv(paths["runner"], runner)
    write_csv(paths["gates"], gates)
    write_csv(paths["decision"], decisions)
    write_csv(paths["next"], next_rows_)
    copies = write_branch_copies(xitau, routes, density, inputs, runner, next_rows_)
    write_csv(paths["branch"], copies)
    csv_paths = [path for key, path in paths.items() if key != "validation"] + [Path(str(row["path"])) for row in copies]
    remove_pycache()
    validation = validation_rows(sources, xitau, routes, density, inputs, runner, gates, next_rows_, copies, csv_paths)
    write_csv(paths["validation"], validation)
    write_doc(sources, xitau, routes, density, inputs, runner, gates, decisions, next_rows_, copies, validation)
    remove_pycache()
    print(f"wrote {DOC}")
    print(f"validation {paths['validation']}")


if __name__ == "__main__":
    main()
