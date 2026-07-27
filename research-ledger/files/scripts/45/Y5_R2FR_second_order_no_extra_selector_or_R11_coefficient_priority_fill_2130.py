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


DOC = ROOT / "2130-Y5-R2FR-second-order-no-extra-selector-or-R11-coefficient-priority-fill.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"

CSV_2129_NEXT = OUT / "P8_Y5_PARENT_QLOC_2129_NEXT_TARGET.csv"
CSV_2129_VAL = OUT / "P8_Y5_BRR545_2129_VALIDATION.csv"
CSV_2129_PREMISES = OUT / "P8_Y5_PARENT_QLOC_2129_PREMISE_AUDIT.csv"
CSV_2129_VECTOR = OUT / "P8_Y5_PARENT_QLOC_2129_NONEH_OPERATOR_VECTOR.csv"
CSV_2129_GATES = OUT / "P8_Y5_PARENT_QLOC_2129_CLAIM_GATES.csv"
CSV_2041_NEF = SOURCE_WEIGHT_DOCS / "AFRAME_NO_EXTRA_FIELD_2041_NONCLAIM.csv"
CSV_2041_R2FR = OUT / "P8_Y5_PARENT_QLOC_2041_R2FR_DECISION_LEDGER.csv"
CSV_1965_ZERO = OUT / "P8_Y5_PARENT_QLOC_1965_R2FR_ZERO_PROOF_ATTEMPT.csv"
CSV_1965_MAP = OUT / "P8_Y5_PARENT_QLOC_1965_R2FR_SCALARON_MAP.csv"
CSV_1965_SCHEMA = OUT / "P8_Y5_PARENT_QLOC_1965_R2FR_EXECUTABLE_BOUND_SCHEMA.csv"
CSV_1821_SCHEMA = OUT / "P8_Y5_PARENT_QLOC_1821_R2FR_BOUND_ROW_SCHEMA.csv"
CSV_1822_OWNER = OUT / "P8_Y5_PARENT_QLOC_1822_R2FR_COEFFICIENT_OWNER_ROW.csv"
CSV_1588_MAP = OUT / "P8_Y5_PARENT_QLOC_1588_R2FR_SCALARON_MAP.csv"
CSV_R11_EXEC = OUT / "R11_nonEH_operator_vector_executable.csv"
DOC_440 = ROOT / "440-metric-only-second-order-sector-reduction-attempt.md"
DOC_963 = ROOT / "963-Y5-R10-parent-second-order-signature-or-R2FR-bound-runner.md"
DOC_964 = ROOT / "964-Y5-R10-parent-no-higher-derivative-minimality-theorem-or-R2FR-nonclaim-runner.md"
DOC_965 = ROOT / "965-Y5-R10-primitive-quotient-no-natural-marker-theorem-or-R2FR-full-curve-intake.md"


def row(**kwargs: object) -> dict[str, object]:
    data = base_row()
    data["claim_allowed"] = False
    data.update(kwargs)
    return data


def truthy(value: object) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"true", "1", "yes", "pass", "valid"}


def formalization_has_2130_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    patterns = (
        "*2130-Y5-R2FR*",
        "*P8_Y5_PARENT_QLOC_2130*",
        "*Y5_R2FR_second_order_no_extra_selector_or_R11_coefficient_priority_fill_2130*",
        "*AFRAME_SECOND_ORDER_SELECTOR_2130*",
        "*JR2130*",
    )
    try:
        return any(path.is_file() for pattern in patterns for path in FORMALIZATION.rglob(pattern))
    except Exception:
        return False


def source_register_rows() -> list[dict[str, object]]:
    specs = [
        ("SRC2130_00_2129_next", CSV_2129_NEXT, ["NEXT2129_0_2130", "second-order-no-extra-selector"], "2129 handoff selects second-order/no-extra selector or R11 coefficient fill."),
        ("SRC2130_01_2129_validation", CSV_2129_VAL, ["VAL2129_OVERALL", "PASS"], "2129 validation passed."),
        ("SRC2130_02_2129_premise", CSV_2129_PREMISES, ["P2129_3_second_order", "CENTRAL_UNSIGNED_BLOCKER"], "second-order premise is the central unsigned blocker."),
        ("SRC2130_03_2129_vector", CSV_2129_VECTOR, ["NEH2129_0_R2_fR_scalar", "RETAINED_NONCLAIM"], "R2/fR scalar mode retained as first non-EH family."),
        ("SRC2130_04_2129_gates", CSV_2129_GATES, ["GATE2129_6_local_GR_claim", "False"], "local-GR claim remains false."),
        ("SRC2130_05_2041_no_extra", CSV_2041_NEF, ["NEF2041_3_second_order", "NEF2041_7_verdict"], "no-extra/second-order parent clause remains unsigned."),
        ("SRC2130_06_2041_r2fr", CSV_2041_R2FR, ["R2FR2041_0_relative_theorem", "R2FR2041_2_finite_branch"], "R2/fR relative theorem and finite fallback are already boxed."),
        ("SRC2130_07_440_doc", DOC_440, ["metric_only_second_order_derived", "fail"], "sector-reduction attempt did not derive metric-only second order."),
        ("SRC2130_08_963_doc", DOC_963, ["NOT_PARENT_SIGNED_CURRENT_CORPUS", "R2RUN963_0_model_input"], "963 says parent second-order signature is unsigned and runner inputs are missing."),
        ("SRC2130_09_964_doc", DOC_964, ["THEOREM_NOT_PROVEN_CURRENT_CORPUS", "R2RUN964_VERDICT"], "964 minimality theorem failed and strict runner rejects placeholders."),
        ("SRC2130_10_965_doc", DOC_965, ["THEOREM_NOT_PROVEN_CURRENT_CORPUS", "R2FC965_3_MTS_R2FR_prediction_required"], "965 primitive quotient/no-marker route remains unproven."),
        ("SRC2130_11_1965_zero", CSV_1965_ZERO, ["ZP1965_6_verdict", "ZERO_PROOF_FAILED_CLEANLY"], "1965 zero proof fails cleanly and calls for scalar residual row."),
        ("SRC2130_12_1965_map", CSV_1965_MAP, ["SM1965_1_scalar_mass", "SM1965_2_yukawa_alpha"], "scalaron mass/range and simple unscreened alpha formulas exist."),
        ("SRC2130_13_1965_schema", CSV_1965_SCHEMA, ["EXR1965_1_mts_prediction", "MISSING_PARENT_NUMERIC_COEFFICIENT"], "strict executable schema requires a parent coefficient."),
        ("SRC2130_14_1821_schema", CSV_1821_SCHEMA, ["R2B1821_5_total", "MISSING_PARENT_AND_ARENA_INPUTS_ROW_NONCLAIM"], "bound row contract is nonclaim with missing parent/arena inputs."),
        ("SRC2130_15_1822_owner", CSV_1822_OWNER, ["CO1822_5_verdict", "NO_EXECUTABLE_OWNER_FOUND_CURRENT_1822"], "coefficient owner row remains missing."),
        ("SRC2130_16_1588_map", CSV_1588_MAP, ["SC1588_5_verdict", "FAIL_CURRENT_CLAIM_NO_SCALARON_PREDICTION"], "scalaron formula exists but no MTS coefficient exists."),
        ("SRC2130_17_R11_exec", CSV_R11_EXEC, ["R2_fR_scalar_mode", "MISSING_NUMERIC_OR_DERIVED_ZERO_COEFFICIENT"], "R11 executable vector still has placeholder coefficient for R2/fR."),
    ]
    rows: list[dict[str, object]] = []
    for source_id, path, needles, role in specs:
        exists = path.exists()
        text = read_text(path) if exists else ""
        rows.append(
            row(
                source_id=source_id,
                source_path=str(path),
                path_exists=exists,
                expected_needles="; ".join(needles),
                needles_found=exists and all(needle in text for needle in needles),
                role=role,
            )
        )
    return rows


def selector_contract_rows() -> list[dict[str, object]]:
    return [
        row(
            contract_id="SEL2130_0_parent_variation_order",
            clause="vary all parent fields before eliminating them",
            math_form="E_A := delta S_parent/delta Z_A = 0, then S_eff[g]=S_parent[g,Z_A^*(g)] only after on-shell substitution",
            proof_status="REQUIRED_NOT_GLOBALLY_SIGNED",
            consequence_if_true="prevents hidden fields from being dropped without stress accounting",
            current_blocker="sector-by-sector Euler ownership remains incomplete for scalar, domain, memory, boundary and source-normalization sectors",
        ),
        row(
            contract_id="SEL2130_1_metric_only_exterior",
            clause="compact local exterior has only observed metric/coframe as propagating geometry variable",
            math_form="Fields_ext={g_obs}; all Xi_A are absent, gauge, topological, constant universal, no-haired, or retained",
            proof_status="UNSIGNED",
            consequence_if_true="activates the metric-only side of the Lovelock selector",
            current_blocker="NEF2041_2, P2129_1 and 440 sector rows leave extra sectors legal",
        ),
        row(
            contract_id="SEL2130_2_no_integrated_out_tower",
            clause="eliminated sectors do not regenerate higher-curvature or nonlocal operators",
            math_form="Delta S_A[g,Z_A^*(g)] has no R^2, f(R), Ricci^2, Weyl^2, Box^-1, or finite scalar pole unless retained as R11",
            proof_status="UNSIGNED_CENTRAL_BLOCKER",
            consequence_if_true="would kill the most dangerous hidden route to non-EH local gravity",
            current_blocker="964 countermodels include auxiliary scalar integrated out to R^2 and nonlocal memory kernels",
        ),
        row(
            contract_id="SEL2130_3_second_order_metric_equations",
            clause="local metric equations remain second order through tested scales",
            math_form="E_eff^{mu nu}=a G^{mu nu}+b g^{mu nu}; all higher-derivative H_i^{mu nu} coefficients zero/topological/decoupled",
            proof_status="NOT_PARENT_DERIVED",
            consequence_if_true="with locality/4D/diffeomorphism would select EH plus Lambda",
            current_blocker="R2/fR, Ricci/Weyl and nonlocal operator families remain covariant countermodels",
        ),
        row(
            contract_id="SEL2130_4_invariant_algebra_triviality",
            clause="local quotient admits no matter-visible scalar/marker generators beyond geometry jets and universal constants",
            math_form="I_loc(Q_MTS)=I_geom(g_obs,jets)+Constants_universal",
            proof_status="NOT_DERIVED",
            consequence_if_true="would block F(sigma)R, species constants, domain selectors and class-scalar prefactors",
            current_blocker="965 leaves co-moving material markers, quotient-invariant scalars, domain selectors and species constants live",
        ),
        row(
            contract_id="SEL2130_5_boundary_topological_silence",
            clause="boundary/topological/projector/domain collars have no local stress or readout hair",
            math_form="delta_g S_boundary/top = 0 locally or maps only to fixed universal calibration with no R3/R4/R7/R8/R9 leakage",
            proof_status="UNSIGNED",
            consequence_if_true="prevents non-EH terms bypassing the selector through surfaces/domains",
            current_blocker="boundary/domain/projector stress rows remain open in 2117/2128/2129",
        ),
        row(
            contract_id="SEL2130_6_selector_verdict",
            clause="activate second-order/no-extra selector",
            math_form="SEL2130_0..SEL2130_5 all parent-signed => EH/Lambda operator selected; current truth value false",
            proof_status="SELECTOR_NOT_DERIVED_CURRENT_CORPUS",
            consequence_if_true="would close the left-hand EH operator gate before Newton/PPN/source gates",
            current_blocker="multiple unsigned parent clauses remain; move to explicit R11 coefficient priority row",
        ),
    ]


def proof_attempt_rows() -> list[dict[str, object]]:
    return [
        row(attempt_id="PROOF2130_0_noether", move="use diffeomorphism/Ward conservation", result="necessary only", why_fails_as_selector="covariant R2/fR, Ricci/Weyl and nonlocal tensors can also be conserved", next_action="do not use conservation as EH proof"),
        row(attempt_id="PROOF2130_1_stability", move="use regularity/stability against higher derivatives", result="insufficient", why_fails_as_selector="R^2/f(R) can be rewritten as scalar-tensor; stability constrains sign/mass, not zero", next_action="need parent coefficient-zero or bound row"),
        row(attempt_id="PROOF2130_2_minimality", move="use primitive quotient/minimality/no-extension", result="not proven", why_fails_as_selector="covariant quotient-invariant markers and integrated-out towers remain legal", next_action="local invariant algebra theorem or retained residuals"),
        row(attempt_id="PROOF2130_3_no_extra", move="eliminate all nonmetric fields by no-hair/topology/gauge", result="not proven", why_fails_as_selector="scalar/class, vector/domain, memory, source-normalization and boundary sectors still have open ledgers", next_action="sector-by-sector no-hair or coefficient rows"),
        row(attempt_id="PROOF2130_4_R2FR_relative", move="apply R2/fR relative theorem", result="conditional win only", why_fails_as_selector="requires exact metric-only second-order no-scalar premise; current parent does not sign it", next_action="keep relative theorem; do not reprove; fill finite branch if needed"),
        row(attempt_id="PROOF2130_5_verdict", move="prove second-order/no-extra selector now", result="FAILED_CLEANLY_NONCLAIM", why_fails_as_selector="selector contract is exact but parent premises are unsigned", next_action="priority-fill R2/fR coefficient acquisition row"),
    ]


def priority_ranking_rows() -> list[dict[str, object]]:
    return [
        row(priority_id="PRI2130_0_R2_fR_scalar", rank=1, operator_family="R2/f(R) scalar mode", reason="directly tests the missing second-order selector; formulas and strict schemas already exist", selected_for_first_fill=True, next_artifact="R2FR2130 coefficient acquisition row"),
        row(priority_id="PRI2130_1_Ricci_Weyl", rank=2, operator_family="Ricci^2/Weyl^2", reason="also higher-curvature but needs more weak-field/tidal operator mapping", selected_for_first_fill=False, next_artifact="defer until R2/fR row is executable or zeroed"),
        row(priority_id="PRI2130_2_scalar_class", rank=3, operator_family="scalar/class metric coupling", reason="important for clocks/PPN/Gdot/R10 but overlaps local invariant algebra work", selected_for_first_fill=False, next_artifact="defer to marker/generator theorem or scalar coefficient row"),
        row(priority_id="PRI2130_3_source_normalization", rank=4, operator_family="source-normalization operator", reason="crucial for Newton/GM but downstream of left-hand EH operator selection", selected_for_first_fill=False, next_artifact="return after EH/operator or finite source branch demands it"),
        row(priority_id="PRI2130_4_connection", rank=5, operator_family="torsion/nonmetricity", reason="major local-GR gate but not the direct second-order/no-extra family selected by 2129", selected_for_first_fill=False, next_artifact="keep P4 branch active separately"),
    ]


def r2fr_acquisition_rows() -> list[dict[str, object]]:
    return [
        row(
            acquisition_id="R2FR2130_0_zero_switch",
            row_type="zero_theorem_switch",
            quantity="c_R2_eff_or_f_RR",
            formula_or_value="0 only if second-order/no-extra/minimality/no-integrated-out-tower clauses are parent-signed",
            required_inputs="SEL2130_0..SEL2130_5 signed; 962/1965 relative theorem source path; no scalar/marker/local invariant generators",
            current_value="MISSING_PARENT_ZERO_CERTIFICATE",
            units="not_applicable_if_zero",
            source_path=str(CSV_1965_ZERO),
            status="ZERO_THEOREM_UNSIGNED",
            valid_for_claim=False,
        ),
        row(
            acquisition_id="R2FR2130_1_parent_coefficient",
            row_type="finite_parent_prediction",
            quantity="c_R2_eff_or_f_RR",
            formula_or_value="MTS-predicted coefficient in S=(1/2kappa) int sqrt(-g)(R + c_R2 R^2 + ...)",
            required_inputs="coefficient value; sign; length^2 units; EH normalization; source derivation path; branch context; no-fit-to-bound guarantee",
            current_value="MISSING_PARENT_NUMERIC_OR_SYMBOLIC_COEFFICIENT",
            units="length_squared_after_EH_normalization",
            source_path="MISSING_SOURCE_FILE",
            status="NOT_EXECUTABLE",
            valid_for_claim=False,
        ),
        row(
            acquisition_id="R2FR2130_2_scalaron_map",
            row_type="finite_scalaron_map",
            quantity="lambda_s_and_alpha_s",
            formula_or_value="m_s^2=1/(6 c_R2); lambda_s=sqrt(6 c_R2); alpha_s=1/3 only for simple unscreened metric f(R)",
            required_inputs="positive c_R2; unit conversion; matter coupling theorem; screening/environment flag; formula source path",
            current_value="FORMULA_AVAILABLE_BUT_PARENT_COEFFICIENT_MISSING",
            units="meters_and_dimensionless_after_conversion",
            source_path=str(CSV_1965_MAP),
            status="CONDITIONAL_FORMULA_ONLY",
            valid_for_claim=False,
        ),
        row(
            acquisition_id="R2FR2130_3_local_response_map",
            row_type="PPN_and_clock_projection",
            quantity="gamma_minus_1; beta_minus_1; clock/Gdot regime",
            formula_or_value="gamma_eff(r) approximately (1-alpha_s exp(-r/lambda_s))/(1+alpha_s exp(-r/lambda_s)) only in simple scalar Yukawa regime",
            required_inputs="solar-system range regime; screening flag; source/test coupling; readout frame; beta map; source normalization",
            current_value="MISSING_SOLAR_SYSTEM_AND_READOUT_REGIME_MAP",
            units="dimensionless",
            source_path=str(CSV_1965_MAP),
            status="NOT_SCORE_READY",
            valid_for_claim=False,
        ),
        row(
            acquisition_id="R2FR2130_4_R10_bound_curve",
            row_type="external_bound_curve",
            quantity="alpha_bound(lambda)",
            formula_or_value="compare abs(alpha_s) <= alpha_bound(lambda_s) only with a valid full curve and matching convention",
            required_inputs="digitized full alpha(lambda) curve; source URL/DOI/path; lambda units; extraction method; valid_for_claim=true bound rows",
            current_value="MISSING_VALID_FULL_CURVE",
            units="dimensionless_alpha_vs_length",
            source_path="source-intake/local_bounds/R10_alpha_lambda_bound_curve_DIGITIZED.csv",
            status="ANCHOR_ONLY_NOT_ENOUGH",
            valid_for_claim=False,
        ),
        row(
            acquisition_id="R2FR2130_5_runner_acceptance",
            row_type="claim_gate",
            quantity="finite_R2FR_scalar_mode_score_row",
            formula_or_value="accept only if zero theorem signed OR coefficient, scalaron map, local response map, and full bound curve are real and sourced",
            required_inputs="R2FR2130_0 OR (R2FR2130_1..R2FR2130_4 all executable)",
            current_value="CURRENTLY_FALSE",
            units="row_contract",
            source_path=str(CSV_1965_SCHEMA),
            status="R2FR_BRANCH_BLOCKED_NONCLAIM",
            valid_for_claim=False,
        ),
    ]


def claim_gate_rows() -> list[dict[str, object]]:
    return [
        row(gate_id="GATE2130_0_sources", gate="source evidence loaded", gate_pass=True, rationale="2129 plus R2/fR prior ledgers are present and needle-checked"),
        row(gate_id="GATE2130_1_selector_contract_written", gate="second-order/no-extra selector contract written", gate_pass=True, rationale="contract clauses SEL2130_0..SEL2130_5 define exact parent requirements"),
        row(gate_id="GATE2130_2_selector_parent_derived", gate="selector parent-derived", gate_pass=False, rationale="variation order, metric-only, no integrated tower, invariant algebra and boundary silence remain unsigned"),
        row(gate_id="GATE2130_3_R2FR_zero", gate="R2/fR coefficient theorem-zero", gate_pass=False, rationale="relative theorem exists but parent activator is missing"),
        row(gate_id="GATE2130_4_R2FR_finite_row_executable", gate="finite R2/fR coefficient row executable", gate_pass=False, rationale="parent coefficient, source path, screening/readout map and full bound curve are missing"),
        row(gate_id="GATE2130_5_EH_operator_selection", gate="EH operator selected", gate_pass=False, rationale="conditional Lovelock/EH theorem remains inactive"),
        row(gate_id="GATE2130_6_local_GR_Newton_PPN_claim", gate="local GR/Newton/PPN claim allowed", gate_pass=False, rationale="EH operator, source normalization, PPN response and empirical gates remain open"),
    ]


def decision_rows() -> list[dict[str, object]]:
    return [
        row(decision_id="DEC2130_0", decision="SELECTOR_CONTRACT_EXACT_BUT_UNSIGNED", because="the right EH bridge is known, but parent variation/no-extra/no-tower clauses are not signed", next_action="do not claim EH; carry selector clauses forward"),
        row(decision_id="DEC2130_1", decision="R2FR_SELECTED_FIRST_COEFFICIENT_FILL", because="R2/fR is the most direct empirical shadow of the missing second-order selector and has formulas/schema already staged", next_action="fill or zero c_R2_eff/f_RR before any R10/PPN score"),
        row(decision_id="DEC2130_2", decision="NEXT_ATTACK_COEFFICIENT_OWNER", because="without coefficient ownership, bound curves and scalaron formulas cannot test MTS", next_action="try to derive c_R2_eff=0 from invariant algebra/no-tower, or source a symbolic parent coefficient owner row"),
    ]


def next_target_rows() -> list[dict[str, object]]:
    return [
        row(
            route_id="NEXT2130_0_2131",
            next_target="2131-Y5-R2FR-cR2-coefficient-owner-or-zero-certificate.md",
            script="scripts/Y5_R2FR_cR2_coefficient_owner_or_zero_certificate_2131.py",
            objective="Try to derive a parent owner for c_R2_eff/f_RR: either a zero certificate from no integrated curvature tower and local invariant algebra triviality, or a sourced symbolic coefficient route with sign, units, normalization, scalaron map, screening/readout regime, and nonclaim bound interface.",
            forbidden_shortcuts="back-solving c_R2 from an experimental bound; alpha=1 anchor-only pass; claiming EH/local-GR from a relative theorem; inventing coefficient values; formalization-workbench edits; GitHub action",
        )
    ]


def write_branch_copies(
    selector: list[dict[str, object]],
    proof: list[dict[str, object]],
    priority: list[dict[str, object]],
    acquisition: list[dict[str, object]],
    gates: list[dict[str, object]],
    next_rows: list[dict[str, object]],
) -> list[dict[str, object]]:
    copies = [
        ("COPY2130_0_source_weight_docs", SOURCE_WEIGHT_DOCS / "AFRAME_SECOND_ORDER_SELECTOR_2130_NONCLAIM.csv", selector + proof + gates),
        ("COPY2130_1_branch_locked_wep", BRANCH_WEP / "P8_Y5_PARENT_QLOC_2130_R2FR_ACQUISITION_NONCLAIM.csv", priority + acquisition),
        ("COPY2130_2_acquisition_queue", QUEUE / "JR2130_CR2_COEFFICIENT_OWNER_OR_ZERO_QUEUE.csv", next_rows + acquisition),
    ]
    results: list[dict[str, object]] = []
    for copy_id, destination, rows_to_write in copies:
        write_csv(destination, rows_to_write)
        results.append(row(copy_id=copy_id, destination=str(destination), path_exists=destination.exists(), row_count=len(rows_to_write), parse_ok=csv_rows_parse(destination)))
    return results


def validation_rows(
    sources: list[dict[str, object]],
    selector: list[dict[str, object]],
    proof: list[dict[str, object]],
    priority: list[dict[str, object]],
    acquisition: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    copies: list[dict[str, object]],
    csv_paths: list[Path],
) -> list[dict[str, object]]:
    sources_ok = all(truthy(item["path_exists"]) and truthy(item["needles_found"]) for item in sources)
    selector_ok = any(item["contract_id"] == "SEL2130_6_selector_verdict" and "NOT_DERIVED" in str(item["proof_status"]) for item in selector)
    proof_ok = any(item["attempt_id"] == "PROOF2130_5_verdict" and item["result"] == "FAILED_CLEANLY_NONCLAIM" for item in proof)
    priority_ok = any(item["priority_id"] == "PRI2130_0_R2_fR_scalar" and truthy(item["selected_for_first_fill"]) for item in priority)
    acquisition_ok = any(item["acquisition_id"] == "R2FR2130_1_parent_coefficient" and item["current_value"] == "MISSING_PARENT_NUMERIC_OR_SYMBOLIC_COEFFICIENT" for item in acquisition) and any(item["acquisition_id"] == "R2FR2130_5_runner_acceptance" and item["status"] == "R2FR_BRANCH_BLOCKED_NONCLAIM" for item in acquisition)
    gates_ok = any(item["gate_id"] == "GATE2130_1_selector_contract_written" and truthy(item["gate_pass"]) for item in gates) and any(item["gate_id"] == "GATE2130_6_local_GR_Newton_PPN_claim" and not truthy(item["gate_pass"]) for item in gates)
    decisions_ok = any(item["decision_id"] == "DEC2130_2" and "COEFFICIENT_OWNER" in str(item["decision"]) for item in decisions)
    next_ok = any(item["route_id"] == "NEXT2130_0_2131" for item in next_rows)
    branch_ok = all(truthy(item["path_exists"]) and truthy(item["parse_ok"]) for item in copies)
    csv_ok = all(path.exists() and csv_rows_parse(path) for path in csv_paths)
    no_claim_flags = all(
        not truthy(item.get("claim_allowed", False)) and not truthy(item.get("valid_for_claim", False))
        for group in (sources, selector, proof, priority, acquisition, gates, decisions, next_rows, copies)
        for item in group
    )
    formalization_clean = count_formalization_modified() == 0 and not formalization_has_2130_artifacts()
    pycache_clean = not (Path(__file__).resolve().parent / "__pycache__").exists()
    all_ok = all([sources_ok, selector_ok, proof_ok, priority_ok, acquisition_ok, gates_ok, decisions_ok, next_ok, branch_ok, csv_ok, no_claim_flags, formalization_clean, pycache_clean])
    checks = [
        ("VAL2130_00_sources", sources_ok, "all cited selector/R2FR sources exist and contain expected needles"),
        ("VAL2130_01_selector_contract", selector_ok, "selector contract is explicit and not parent-derived"),
        ("VAL2130_02_proof_attempt", proof_ok, "proof attempt fails cleanly without claim"),
        ("VAL2130_03_priority", priority_ok, "R2/fR scalar mode is selected as first coefficient fill"),
        ("VAL2130_04_acquisition", acquisition_ok, "R2/fR acquisition row is staged but blocked by missing parent coefficient and curve/regime inputs"),
        ("VAL2130_05_gates", gates_ok, "selector contract gate passes while local-GR claim gate fails"),
        ("VAL2130_06_decisions", decisions_ok, "decision ledger selects c_R2 coefficient owner/zero certificate next"),
        ("VAL2130_07_next", next_ok, "next target is c_R2 coefficient owner or zero certificate"),
        ("VAL2130_08_branch_copies", branch_ok, "branch copies exist and parse"),
        ("VAL2130_09_csv_parse", csv_ok, "all generated CSVs parse cleanly"),
        ("VAL2130_10_no_claim_flags", no_claim_flags, "no generated row allows a claim"),
        ("VAL2130_11_formalization_clean", formalization_clean, "formalization-workbench untouched by 2130"),
        ("VAL2130_12_no_pycache", pycache_clean, "scripts __pycache__ removed"),
        ("VAL2130_OVERALL", all_ok, "2130 records the exact second-order/no-extra selector contract, rejects current derivation, and stages the first R2/fR coefficient acquisition row as nonclaim."),
    ]
    return [row(check_id=check_id, status="PASS" if passed else "FAIL", detail=detail) for check_id, passed, detail in checks]


def write_doc(
    sources: list[dict[str, object]],
    selector: list[dict[str, object]],
    proof: list[dict[str, object]],
    priority: list[dict[str, object]],
    acquisition: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    copies: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    content = "\n\n".join(
        [
            "# 2130 - Y5/R2FR Second-Order No-Extra Selector Or R11 Coefficient Priority Fill",
            "## Current Verdict",
            "2130 takes the derivation shot at the second-order/no-extra selector. The exact contract is now written: vary every parent field first, reduce only harmless/no-haired/topological sectors, forbid integrated-out curvature towers, prove local invariant algebra triviality, and keep boundary/projector hair silent. If all of that were parent-signed, the 2129 Lovelock/EH selector would activate.",
            "The current corpus still does not sign those clauses. That is not a dead end; it tells us what the next honest test object is. The first retained non-EH family is `R2/f(R)` because it is the cleanest shadow of failed second-order selection. 2130 therefore stages a strict nonclaim `c_R2_eff/f_RR` acquisition row: zero certificate if derivable, otherwise coefficient, units, normalization, scalaron map, screening/readout regime, and full bound curve before any score.",
            "## Source Register",
            md_table(sources, ["source_id", "source_path", "path_exists", "needles_found", "role", "valid_for_claim"]),
            "## Second-Order/No-Extra Selector Contract",
            md_table(selector, ["contract_id", "clause", "math_form", "proof_status", "consequence_if_true", "current_blocker", "valid_for_claim"]),
            "## Proof Attempt Ledger",
            md_table(proof, ["attempt_id", "move", "result", "why_fails_as_selector", "next_action", "valid_for_claim"]),
            "## R11 Priority Ranking",
            md_table(priority, ["priority_id", "rank", "operator_family", "reason", "selected_for_first_fill", "next_artifact", "valid_for_claim"]),
            "## R2/fR Coefficient Acquisition Row",
            md_table(acquisition, ["acquisition_id", "row_type", "quantity", "formula_or_value", "required_inputs", "current_value", "units", "source_path", "status", "valid_for_claim"]),
            "## Claim Gates",
            md_table(gates, ["gate_id", "gate", "gate_pass", "rationale", "claim_allowed", "valid_for_claim"]),
            "## Decision Ledger",
            md_table(decisions, ["decision_id", "decision", "because", "next_action", "valid_for_claim"]),
            "## Next Target",
            md_table(next_rows, ["route_id", "next_target", "script", "objective", "forbidden_shortcuts", "valid_for_claim"]),
            "## Branch Copies",
            md_table(copies, ["copy_id", "destination", "path_exists", "row_count", "parse_ok", "valid_for_claim"]),
            "## Validation",
            md_table(validation, ["check_id", "status", "detail", "claim_allowed", "valid_for_claim"]),
        ]
    )
    DOC.write_text(content, encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    SOURCE_WEIGHT_DOCS.mkdir(parents=True, exist_ok=True)
    BRANCH_WEP.mkdir(parents=True, exist_ok=True)
    QUEUE.mkdir(parents=True, exist_ok=True)

    sources = source_register_rows()
    selector = selector_contract_rows()
    proof = proof_attempt_rows()
    priority = priority_ranking_rows()
    acquisition = r2fr_acquisition_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_rows = next_target_rows()

    paths = {
        "sources": OUT / "P8_Y5_PARENT_QLOC_2130_SOURCE_REGISTER.csv",
        "selector": OUT / "P8_Y5_PARENT_QLOC_2130_SELECTOR_CONTRACT.csv",
        "proof": OUT / "P8_Y5_PARENT_QLOC_2130_PROOF_ATTEMPT_LEDGER.csv",
        "priority": OUT / "P8_Y5_PARENT_QLOC_2130_R11_PRIORITY_RANKING.csv",
        "acquisition": OUT / "P8_Y5_PARENT_QLOC_2130_R2FR_COEFFICIENT_ACQUISITION.csv",
        "gates": OUT / "P8_Y5_PARENT_QLOC_2130_CLAIM_GATES.csv",
        "decisions": OUT / "P8_Y5_PARENT_QLOC_2130_DECISION_LEDGER.csv",
        "next": OUT / "P8_Y5_PARENT_QLOC_2130_NEXT_TARGET.csv",
        "branch": OUT / "P8_Y5_PARENT_QLOC_2130_BRANCH_COPIES.csv",
        "validation": OUT / "P8_Y5_BRR545_2130_VALIDATION.csv",
    }
    write_csv(paths["sources"], sources)
    write_csv(paths["selector"], selector)
    write_csv(paths["proof"], proof)
    write_csv(paths["priority"], priority)
    write_csv(paths["acquisition"], acquisition)
    write_csv(paths["gates"], gates)
    write_csv(paths["decisions"], decisions)
    write_csv(paths["next"], next_rows)

    copies = write_branch_copies(selector, proof, priority, acquisition, gates, next_rows)
    write_csv(paths["branch"], copies)

    remove_pycache()
    csv_paths = [path for key, path in paths.items() if key != "validation"] + [Path(str(copy["destination"])) for copy in copies]
    validation = validation_rows(sources, selector, proof, priority, acquisition, gates, decisions, next_rows, copies, csv_paths)
    write_csv(paths["validation"], validation)
    write_doc(sources, selector, proof, priority, acquisition, gates, decisions, next_rows, copies, validation)

    print(f"wrote {DOC}")
    print(f"validation {paths['validation']}")


if __name__ == "__main__":
    main()
