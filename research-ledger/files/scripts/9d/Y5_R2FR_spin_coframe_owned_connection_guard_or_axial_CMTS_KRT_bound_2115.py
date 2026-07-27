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


DOC = ROOT / "2115-Y5-R2FR-spin-coframe-owned-connection-guard-or-axial-CMTS-KRT-bound.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"

CSV_2114_NEXT = OUT / "P8_Y5_PARENT_QLOC_2114_NEXT_TARGET.csv"
CSV_2114_SECTOR = OUT / "P8_Y5_PARENT_QLOC_2114_SECTOR_GAMMA_SLOT_AUDIT.csv"
CSV_2114_CMTS = OUT / "P8_Y5_PARENT_QLOC_2114_CMTS_SOURCE_PACK.csv"

CSV_2042_NOHYPER = OUT / "P8_Y5_PARENT_QLOC_2042_NO_HYPERMOMENTUM_THEOREM_ATTEMPT.csv"
CSV_2043_GUARD = OUT / "P8_Y5_PARENT_QLOC_2043_SPIN_PROJECTIVE_GUARD.csv"
CSV_2044_ANCHORS = OUT / "P8_Y5_PARENT_QLOC_2044_NUMERIC_P4_SOURCE_ANCHORS.csv"
CSV_2044_MAP = OUT / "P8_Y5_PARENT_QLOC_2044_P4_MAPPING_REQUIREMENTS.csv"
CSV_2045_MAP = OUT / "P8_Y5_PARENT_QLOC_2045_CONDITIONAL_COMPONENT_MAP.csv"
CSV_2045_REQ = OUT / "P8_Y5_PARENT_QLOC_2045_MTS_VARIABLE_REQUIREMENTS.csv"
CSV_2046_LC = OUT / "P8_Y5_PARENT_QLOC_2046_LC_ZERO_THEOREM_BRANCH.csv"
CSV_2046_AFFINE = OUT / "P8_Y5_PARENT_QLOC_2046_AFFINE_RESIDUAL_DEFINITION.csv"
CSV_2047_CMTS = OUT / "P8_Y5_PARENT_QLOC_2047_CMTS_FIRST_COEFFICIENT_CHAIN.csv"


def row(**kwargs: object) -> dict[str, object]:
    data = base_row()
    data["claim_allowed"] = False
    data.update(kwargs)
    return data


def truthy(value: object) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"true", "1", "yes", "pass", "valid", "claim_allowed"}


def formalization_has_2115_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    patterns = (
        "*2115-Y5-R2FR*",
        "*P8_Y5_PARENT_QLOC_2115*",
        "*Y5_R2FR_spin_coframe_owned_connection_guard_or_axial_CMTS_KRT_bound_2115*",
        "*AFRAME_SPIN_GUARD_2115*",
        "*JR2115_AXIAL*",
    )
    try:
        return any(path.is_file() for pattern in patterns for path in FORMALIZATION.rglob(pattern))
    except Exception:
        return False


def source_register_rows() -> list[dict[str, object]]:
    specs = [
        (
            "SRC2115_00_2114_next",
            CSV_2114_NEXT,
            ["NEXT2114_0_2115", "spinors/spin transport", "KRT torsion-component map"],
            "2114 handoff selects the spin coframe-owned connection guard or axial C_MTS/KRT bound.",
        ),
        (
            "SRC2115_01_2114_sector",
            CSV_2114_SECTOR,
            ["SGS2114_2_spin", "UNSIGNED_HIGHEST_P4_RISK", "SGS2114_9_verdict"],
            "2114 identifies spin as the highest P4 risk and blocks LC activation.",
        ),
        (
            "SRC2115_02_2114_cmts",
            CSV_2114_CMTS,
            ["CMTS2114_1_spin_axial", "SOURCE_ANCHOR_EXISTS_MTS_MAP_MISSING", "CMTS2114_8_total"],
            "2114 keeps the axial C_MTS component and total Delta_Gamma envelope live.",
        ),
        (
            "SRC2115_03_2042_nohyper",
            CSV_2042_NOHYPER,
            ["NH2042_2_chain_rule", "NH2042_3_spin_guard", "NH2042_5_verdict"],
            "2042 gives the exact conditional chain-rule theorem and the spin counterbranch.",
        ),
        (
            "SRC2115_04_2043_spin_guard",
            CSV_2043_GUARD,
            ["SPG2043_0_spin_guard", "omega_spin = omega_LC[e_obs]", "SPG2043_5_verdict"],
            "2043 states the spin guard and fallback axial torsion row.",
        ),
        (
            "SRC2115_05_2044_anchor",
            CSV_2044_ANCHORS,
            ["P4SRC2044_0_KRT2008_axial_torsion_anchor", "1e-31", "SOURCE_BACKED_ANCHOR_NOT_MTS_MAP"],
            "2044 provides the source-backed KRT order anchor but not an MTS map.",
        ),
        (
            "SRC2115_06_2044_map_requirements",
            CSV_2044_MAP,
            ["MAP2044_0_component_basis", "MAP2044_1_units", "MAP2044_5_claim_rule"],
            "2044 lists the component-basis, unit, frame and claim-rule blockers.",
        ),
        (
            "SRC2115_07_2045_component_map",
            CSV_2045_MAP,
            ["MAP2045_1_axial_projection", "MAP2045_3_coupling_kernel", "MAP2045_7_verdict"],
            "2045 provides the conditional axial map shape and coupling blockers.",
        ),
        (
            "SRC2115_08_2045_requirements",
            CSV_2045_REQ,
            ["REQ2045_0_Gamma_MTS", "REQ2045_4_xi_A", "REQ2045_7_bound_row"],
            "2045 lists the missing MTS variables and KRT-ready inputs.",
        ),
        (
            "SRC2115_09_2046_lc_zero",
            CSV_2046_LC,
            ["LCZ2046_3_torsion_zero", "LCZ2046_7_verdict", "THEOREM_AVAILABLE_NOT_PARENT_DERIVED"],
            "2046 proves torsion/axial zero on the conditional LC branch.",
        ),
        (
            "SRC2115_10_2046_affine",
            CSV_2046_AFFINE,
            ["AFF2046_1_torsion_from_residual", "AFF2046_3_axial_projection", "AFF2046_5_spin_coupling"],
            "2046 defines the affine residual fallback and spin coupling need.",
        ),
        (
            "SRC2115_11_2047_cmts",
            CSV_2047_CMTS,
            ["CMTS2047_1_axial_component_m_inv", "CMTS2047_2_axial_component_GeV", "CMTS2047_VERDICT"],
            "2047 stages the first C_MTS coefficient chain and unit conversion.",
        ),
    ]
    rows: list[dict[str, object]] = []
    for source_id, path, needles, role in specs:
        exists = path.exists()
        text = read_text(path) if exists else ""
        found = all(needle in text for needle in needles)
        rows.append(
            row(
                source_id=source_id,
                source_path=str(path),
                path_exists=exists,
                expected_needles="; ".join(needles),
                needles_found=found,
                role=role,
            )
        )
    return rows


def spin_guard_rows() -> list[dict[str, object]]:
    return [
        row(
            guard_id="SOG2115_0_spin_connection_owner",
            clause="spin connection is coframe-owned",
            status="MISSING_PARENT_SIGNATURE",
            statement="omega_spin := omega_LC[e_obs] for ordinary spinors/spin transport; omega is not an independent affine variable.",
            math_consequence="Gamma variation is replaced by coframe/metric variation already counted in Hilbert/coframe stress.",
            source_anchor="NH2042_2_chain_rule; SPG2043_0_spin_guard",
            missing_input="parent action clause for every ordinary spin sector",
            theorem_role="required for exact spin zero",
        ),
        row(
            guard_id="SOG2115_1_no_independent_contorsion",
            clause="no independent contorsion argument",
            status="MISSING_PARENT_SIGNATURE",
            statement="The local matter/spin action contains no independent K_abc or C_MTS^lambda_{mu nu} argument.",
            math_consequence="delta S_spin / delta K_abc = 0 and spin hypermomentum cannot source torsion.",
            source_anchor="SPG2043_0_spin_guard; NH2042_3_spin_guard",
            missing_input="explicit exclusion of torsionful spin connection in parent action",
            theorem_role="required for exact spin zero",
        ),
        row(
            guard_id="SOG2115_2_no_axial_torsion_current",
            clause="no axial torsion current",
            status="MISSING_PARENT_SIGNATURE",
            statement="No independent A_MTS_mu J5^mu, b_eff_mu J5^mu, or equivalent axial spin-current term survives in local observables.",
            math_consequence="Delta_spin_axial and c_A/S_mu vanish rather than needing a KRT bound.",
            source_anchor="CMTS2114_1_spin_axial; AFF2046_5_spin_coupling",
            missing_input="coupling inventory showing xi_A=0 by ontology, not by fit",
            theorem_role="required for exact spin zero",
        ),
        row(
            guard_id="SOG2115_3_chain_rule_theorem",
            clause="conditional no-hypermomentum theorem",
            status="EXACT_CONDITIONAL_THEOREM",
            statement="If S_spin = S_spin[psi,e_obs,omega_LC[e_obs],A_Q,theta] with no independent Gamma/K argument, then independent connection variation from spin is zero.",
            math_consequence="Delta_lambda_spin^{mu nu}=0 as a matter of action variables.",
            source_anchor="NH2042_2_chain_rule; NH2042_5_verdict",
            missing_input="not a current claim until SOG2115_0 through SOG2115_2 are parent-signed",
            theorem_role="usable future closure route",
        ),
        row(
            guard_id="SOG2115_4_LC_spin_axial_zero",
            clause="LC branch kills axial torsion",
            status="EXACT_CONDITIONAL_ZERO",
            statement="If Gamma_MTS=LC[g_obs], then T_MTS^lambda_{mu nu}=0 and A_MTS^mu=0 because LC is torsion-free.",
            math_consequence="KRT axial row becomes unnecessary on the fully signed LC branch.",
            source_anchor="LCZ2046_3_torsion_zero; LCZ2046_7_verdict",
            missing_input="Gamma_MTS=LC[g_obs] parent activation remains unsigned",
            theorem_role="clean preferred route",
        ),
        row(
            guard_id="SOG2115_5_counterbranch",
            clause="independent torsionful spin connection survives",
            status="COUNTERBRANCH_RETAINED",
            statement="If spin sees an independent torsionful connection, axial torsion generically couples to spin and cannot be declared harmless.",
            math_consequence="Retain A_MTS, xi_A, C_basis, frame map, and KRT/no-cancellation bound rows.",
            source_anchor="NH2042_3_spin_guard; MAP2045_3_coupling_kernel; CMTS2047_3_spin_coupling",
            missing_input="numeric or theorem-zero component map",
            theorem_role="honest fallback",
        ),
        row(
            guard_id="SOG2115_6_verdict",
            clause="spin Gamma slot",
            status="SPIN_ZERO_NOT_PARENT_SIGNED",
            statement="The spin-zero route is mathematically sharp but not corpus-signed; the axial C_MTS/KRT fallback must remain live.",
            math_consequence="No LC activation, no local GR/Newton claim, and no KRT pass from the anchor alone.",
            source_anchor="SGS2114_2_spin; SPG2043_5_verdict; P4SRC2044_0_KRT2008_axial_torsion_anchor",
            missing_input="parent spin connection signature or complete axial component map",
            theorem_role="current checkpoint verdict",
        ),
    ]


def axial_cmts_krt_map_rows() -> list[dict[str, object]]:
    return [
        row(
            map_id="AKM2115_0_C_MTS_residual",
            object="C_MTS^lambda_{mu nu}",
            formula="C_MTS^lambda_{mu nu} := Gamma_MTS^lambda_{mu nu} - LC^lambda_{mu nu}[g_obs]",
            status="DEFINED_FALLBACK_NOT_NUMERIC",
            units="m^-1 if local coordinates are meters",
            needed_inputs="parent choice: LC zero or independent affine branch plus C_MTS component values",
            source_anchor="CMTS2047_0_C_tensor; AFF2046_7_verdict",
            score_ready=False,
        ),
        row(
            map_id="AKM2115_1_torsion_from_C",
            object="T_MTS^lambda_{mu nu}",
            formula="T_MTS^lambda_{mu nu} = 2 C_MTS^lambda_{[mu nu]} because LC[g_obs] has zero torsion",
            status="EXACT_COMPONENT_FORMULA_IF_C_EXISTS",
            units="m^-1",
            needed_inputs="C_MTS antisymmetric lower-index components and sign convention",
            source_anchor="AFF2046_1_torsion_from_residual",
            score_ready=False,
        ),
        row(
            map_id="AKM2115_2_axial_projection",
            object="A_MTS^mu",
            formula="A_MTS^mu := (1/6) epsilon^{alpha beta gamma mu} T_MTS_alpha beta gamma = (1/3) epsilon^{alpha beta gamma mu} C_MTS_alpha[beta gamma]",
            status="EXACT_COMPONENT_FORMULA_WITH_ORIENTATION",
            units="m^-1",
            needed_inputs="orientation, metric signature, index placement, local frame/component label",
            source_anchor="AFF2046_3_axial_projection; MAP2045_1_axial_projection; CMTS2047_1_axial_component_m_inv",
            score_ready=False,
        ),
        row(
            map_id="AKM2115_3_unit_conversion",
            object="A_MTS_component_GeV",
            formula="A_MTS_component_GeV = 1.973269804e-16 * A_MTS_component_m^-1 before xi_A, C_basis, and KRT convention factors",
            status="UNIT_FACTOR_STAGED_NOT_SCOREABLE",
            units="GeV",
            needed_inputs="actual A_MTS value, xi_A, C_basis and KRT component convention",
            source_anchor="CMTS2047_2_axial_component_GeV",
            score_ready=False,
        ),
        row(
            map_id="AKM2115_4_KRT_basis_projection",
            object="KRT axial irreducible component",
            formula="A_KRT^I = C_basis^I_mu A_MTS^mu in the KRT irreducible torsion basis",
            status="MISSING_BASIS_MAP",
            units="GeV after unit conversion",
            needed_inputs="C_basis matrix, KRT component labels, orientation/sign convention",
            source_anchor="MAP2044_0_component_basis; MAP2045_2_KRT_basis",
            score_ready=False,
        ),
        row(
            map_id="AKM2115_5_spin_coupling_kernel",
            object="b_eff^I",
            formula="b_eff^I = xi_A C_basis^I_mu A_MTS^mu + retained vector/tensor torsion mixing",
            status="MISSING_XI_A_AND_MIXING_MATRIX",
            units="GeV or declared KRT convention units",
            needed_inputs="xi_A, vector/tensor mixing matrix, coupling convention and matter species",
            source_anchor="AFF2046_5_spin_coupling; MAP2045_3_coupling_kernel; CMTS2047_3_spin_coupling",
            score_ready=False,
        ),
        row(
            map_id="AKM2115_6_frame_component",
            object="R_KRT<-MTS A_MTS",
            formula="bounded component = R_KRT<-MTS^I_mu(t) A_MTS^mu with lab/Sun-centered frame convention declared",
            status="MISSING_FRAME_CONVENTION",
            units="frame map plus component label",
            needed_inputs="lab/Sun-centered frame, time dependence, orientation and selected KRT component",
            source_anchor="MAP2044_2_lab_frame; MAP2045_5_lab_frame; CMTS2047_4_frame_component",
            score_ready=False,
        ),
        row(
            map_id="AKM2115_7_no_cancellation_bound",
            object="absolute axial torsion envelope",
            formula="score only if abs(b_eff^I) plus absolute retained unmapped components <= B_KRT^I",
            status="NO_CANCELLATION_SCHEMA_READY",
            units="GeV",
            needed_inputs="numeric components, component-specific source-backed bound table, and all retained pieces zeroed or bounded",
            source_anchor="MAP2044_4_no_cancellation; MAP2045_6_envelope; CMTS2047_5_bound_rule",
            score_ready=False,
        ),
        row(
            map_id="AKM2115_8_verdict",
            object="axial C_MTS -> KRT map",
            formula="C_MTS -> T_MTS -> A_MTS -> A_GeV -> C_basis/xi_A/frame -> b_eff -> KRT bound",
            status="MAP_STAGED_NOT_SCOREABLE",
            units="mixed; each stage declared above",
            needed_inputs="parent spin zero signature or actual C_MTS, xi_A, C_basis, frame and component-specific KRT bound rows",
            source_anchor="P4SRC2044_0_KRT2008_axial_torsion_anchor; CMTS2047_VERDICT",
            score_ready=False,
        ),
    ]


def krt_bound_status_rows() -> list[dict[str, object]]:
    return [
        row(
            bound_id="KRT2115_0_KRT2008_anchor",
            observable="axial_torsion_spin_coupling",
            source_url="https://arxiv.org/abs/0712.4393",
            doi_or_ref="PhysRevLett.100.111102",
            bound_value="1e-31",
            bound_units="GeV",
            source_status="SOURCE_BACKED_ORDER_ANCHOR",
            extraction_method="order-of-magnitude abstract/source-row anchor inherited from 2044",
            confidence="source-backed anchor, not full component table",
            ready_for_scoring=False,
            reason_not_scoreable="MTS axial component, xi_A, C_basis, frame and KRT component label are missing",
        ),
        row(
            bound_id="KRT2115_1_Terrano2015_context",
            observable="spin_dependent_source_context",
            source_url="https://arxiv.org/abs/1508.02463",
            doi_or_ref="PhysRevLett.115.201801",
            bound_value="70",
            bound_units="TeV",
            source_status="SOURCE_BACKED_CONTEXT_NOT_DIRECT_P4_BOUND",
            extraction_method="context row inherited from 2044",
            confidence="useful source context only",
            ready_for_scoring=False,
            reason_not_scoreable="not a direct axial C_MTS/KRT torsion-component bound",
        ),
        row(
            bound_id="KRT2115_2_claim_rule",
            observable="MTS axial torsion score",
            source_url="internal-gate",
            doi_or_ref="MAP2044_5_claim_rule",
            bound_value="blocked",
            bound_units="policy",
            source_status="CLAIM_BLOCKED_CURRENTLY",
            extraction_method="schema guard",
            confidence="hard gate",
            ready_for_scoring=False,
            reason_not_scoreable="claim allowed only after zero theorem is parent-signed or all numeric map inputs and source-backed component bounds exist",
        ),
    ]


def claim_gate_rows() -> list[dict[str, object]]:
    return [
        row(
            gate_id="GATE2115_0_source_backing",
            gate="source rows exist and anchor spin/KRT statements",
            gate_pass=True,
            rationale="source register checks 2114, 2042-2047 rows needed for spin guard and KRT fallback",
        ),
        row(
            gate_id="GATE2115_1_exact_spin_zero_theorem",
            gate="conditional spin zero theorem exists",
            gate_pass=True,
            rationale="if spin only sees omega_LC[e_obs] and no independent K/A_MTS argument, independent spin hypermomentum vanishes",
        ),
        row(
            gate_id="GATE2115_2_parent_spin_signature",
            gate="current corpus signs spin connection owner",
            gate_pass=False,
            rationale="omega_spin=omega_LC[e_obs] and no axial current are required but not parent-signed",
        ),
        row(
            gate_id="GATE2115_3_axial_map_staged",
            gate="C_MTS to KRT map shape exists",
            gate_pass=True,
            rationale="C_MTS, torsion, axial projection, unit conversion, coupling, frame and envelope rows are explicit",
        ),
        row(
            gate_id="GATE2115_4_KRT_score_ready",
            gate="KRT bound can score an MTS prediction",
            gate_pass=False,
            rationale="KRT anchor is source-backed but MTS component, xi_A, basis, frame and component-specific bound table are missing",
        ),
        row(
            gate_id="GATE2115_5_no_cancellation",
            gate="no cancellation policy enforced",
            gate_pass=True,
            rationale="fallback bound row requires absolute retained components and forbids cancellation against unknown pieces",
        ),
        row(
            gate_id="GATE2115_6_local_GR_Newton",
            gate="local GR/Newton follows from spin sector",
            gate_pass=False,
            rationale="spin is only one Gamma slot; LC activation and source/readout/PPN gates remain open",
        ),
    ]


def decision_rows() -> list[dict[str, object]]:
    return [
        row(
            decision_id="DEC2115_0",
            decision="SPIN_ZERO_CONDITIONAL_RETAINED",
            because="The action-variable theorem is clean: coframe-owned omega_LC spin transport gives no independent spin connection current.",
            next_action="Keep this as the preferred route and try to parent-sign the spin object language.",
        ),
        row(
            decision_id="DEC2115_1",
            decision="SPIN_ZERO_NOT_CURRENT_CLAIM",
            because="The parent corpus still does not explicitly exclude independent contorsion/axial torsion current in every local spin sector.",
            next_action="Do not activate LC/local-GR from spin until the parent action signs it.",
        ),
        row(
            decision_id="DEC2115_2",
            decision="AXIAL_CMTS_KRT_FALLBACK_RETAINED",
            because="KRT gives a real external torsion anchor, but it is not usable until the MTS-to-KRT basis/unit/frame/coupling map is filled.",
            next_action="Retain C_MTS -> A_MTS -> b_eff map with no-cancellation and no score.",
        ),
        row(
            decision_id="DEC2115_3",
            decision="COUPLING_HUNT_NEXT",
            because="The bottleneck is no longer vague geometry; it is the parent coupling signature or the numeric coupling map xi_A/C_basis.",
            next_action="Try to sign omega_spin=omega_LC[e_obs] in the parent action; if it fails, source xi_A, C_basis and component labels.",
        ),
    ]


def next_target_rows() -> list[dict[str, object]]:
    return [
        row(
            route_id="NEXT2115_0_2116",
            next_target="2116-Y5-R2FR-spin-connection-parent-action-signature-or-axial-CMTS-component-source-values.md",
            script="scripts/Y5_R2FR_spin_connection_parent_action_signature_or_axial_CMTS_component_source_values_2116.py",
            objective=(
                "Try to source/sign the actual parent spin connection object language: spinors use omega_LC[e_obs] and no independent "
                "contorsion. If not, fill actual C_MTS axial component values, xi_A, C_basis, frame map, and KRT component labels."
            ),
            forbidden_shortcuts=(
                "declaring ordinary GR spin connection harmless without parent action ownership; using the KRT 1e-31 GeV anchor as a pass; "
                "cancelling axial torsion against unmapped pieces; local-GR/Newton/PPN claim; formalization-workbench edits; GitHub action"
            ),
        )
    ]


def write_branch_copies(
    spin_rows: list[dict[str, object]],
    axial_rows: list[dict[str, object]],
    bound_rows: list[dict[str, object]],
    next_rows: list[dict[str, object]],
) -> list[dict[str, object]]:
    copies: list[tuple[str, Path, list[dict[str, object]]]] = [
        (
            "COPY2115_0_source_weight_docs",
            SOURCE_WEIGHT_DOCS / "AFRAME_SPIN_GUARD_2115_NONCLAIM.csv",
            spin_rows + axial_rows + bound_rows,
        ),
        (
            "COPY2115_1_branch_locked_wep",
            BRANCH_WEP / "P8_Y5_PARENT_QLOC_2115_SPIN_STATUS_NONCLAIM.csv",
            spin_rows + axial_rows,
        ),
        (
            "COPY2115_2_acquisition_queue",
            QUEUE / "JR2115_AXIAL_CMTS_KRT_OR_SPIN_GUARD_QUEUE.csv",
            next_rows + bound_rows,
        ),
    ]
    result: list[dict[str, object]] = []
    for copy_id, destination, rows_to_write in copies:
        write_csv(destination, rows_to_write)
        parsed = csv_rows_parse(destination)
        result.append(
            row(
                copy_id=copy_id,
                destination=str(destination),
                path_exists=destination.exists(),
                row_count=len(rows_to_write),
                parse_ok=parsed,
            )
        )
    return result


def validation_rows(
    sources: list[dict[str, object]],
    spin_rows: list[dict[str, object]],
    axial_rows: list[dict[str, object]],
    bound_rows: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    copies: list[dict[str, object]],
    csv_paths: list[Path],
) -> list[dict[str, object]]:
    sources_ok = all(truthy(source["path_exists"]) and truthy(source["needles_found"]) for source in sources)
    spin_theorem_ok = any(
        row_["guard_id"] == "SOG2115_3_chain_rule_theorem"
        and row_["status"] == "EXACT_CONDITIONAL_THEOREM"
        for row_ in spin_rows
    )
    spin_verdict_ok = any(
        row_["guard_id"] == "SOG2115_6_verdict"
        and row_["status"] == "SPIN_ZERO_NOT_PARENT_SIGNED"
        for row_ in spin_rows
    )
    axial_terms = " ".join(str(value) for row_ in axial_rows for value in row_.values())
    axial_ok = all(
        term in axial_terms
        for term in ("C_MTS", "T_MTS", "A_MTS", "A_MTS_component_GeV", "xi_A", "C_basis", "NO_CANCELLATION")
    )
    krt_ok = any(
        row_["bound_id"] == "KRT2115_0_KRT2008_anchor"
        and row_["source_status"] == "SOURCE_BACKED_ORDER_ANCHOR"
        and not truthy(row_["ready_for_scoring"])
        for row_ in bound_rows
    )
    gates_ok = any(
        row_["gate_id"] == "GATE2115_2_parent_spin_signature" and not truthy(row_["gate_pass"])
        for row_ in gates
    ) and any(
        row_["gate_id"] == "GATE2115_4_KRT_score_ready" and not truthy(row_["gate_pass"])
        for row_ in gates
    )
    no_claim_flags = all(
        not truthy(row_.get("claim_allowed", False)) and not truthy(row_.get("valid_for_claim", False))
        for group in (sources, spin_rows, axial_rows, bound_rows, gates, decisions, next_rows, copies)
        for row_ in group
    )
    branch_ok = all(truthy(copy["path_exists"]) and truthy(copy["parse_ok"]) for copy in copies)
    csv_ok = all(path.exists() and csv_rows_parse(path) for path in csv_paths)
    formalization_clean = count_formalization_modified() == 0 and not formalization_has_2115_artifacts()
    pycache_clean = not (Path(__file__).resolve().parent / "__pycache__").exists()
    next_ok = any(row_["route_id"] == "NEXT2115_0_2116" for row_ in next_rows)
    all_ok = all(
        [
            sources_ok,
            spin_theorem_ok,
            spin_verdict_ok,
            axial_ok,
            krt_ok,
            gates_ok,
            no_claim_flags,
            branch_ok,
            csv_ok,
            formalization_clean,
            pycache_clean,
            next_ok,
        ]
    )
    checks = [
        ("VAL2115_00_sources", sources_ok, "all cited spin/KRT source rows exist and contain expected needles"),
        ("VAL2115_01_spin_theorem", spin_theorem_ok, "conditional coframe-owned spin connection zero theorem is recorded"),
        ("VAL2115_02_spin_verdict", spin_verdict_ok, "spin zero remains blocked as a current parent claim"),
        ("VAL2115_03_axial_map", axial_ok, "axial C_MTS -> KRT map includes tensor, unit, coupling, frame and no-cancellation terms"),
        ("VAL2115_04_KRT_anchor", krt_ok, "KRT anchor is source-backed but explicitly not score-ready"),
        ("VAL2115_05_claim_gates", gates_ok, "parent spin signature and KRT scoring gates remain false"),
        ("VAL2115_06_no_claim_flags", no_claim_flags, "no generated row allows a claim or score"),
        ("VAL2115_07_branch_copies", branch_ok, "branch copies exist and parse"),
        ("VAL2115_08_csv_parse", csv_ok, "all generated CSVs parse cleanly"),
        ("VAL2115_09_formalization_clean", formalization_clean, "formalization-workbench untouched by 2115"),
        ("VAL2115_10_no_pycache", pycache_clean, "scripts __pycache__ removed"),
        ("VAL2115_11_next", next_ok, "next target selects parent spin signature or axial component sourcing"),
        (
            "VAL2115_OVERALL",
            all_ok,
            "2115 closes the spin gate conditionally, keeps axial C_MTS/KRT fallback nonclaim, and points at the coupling signature next.",
        ),
    ]
    return [
        row(
            check_id=check_id,
            status="PASS" if passed else "FAIL",
            detail=detail,
        )
        for check_id, passed, detail in checks
    ]


def write_doc(
    sources: list[dict[str, object]],
    spin_rows: list[dict[str, object]],
    axial_rows: list[dict[str, object]],
    bound_rows: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    copies: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    content = "\n\n".join(
        [
            "# 2115 - Y5/R2FR Spin Coframe-Owned Connection Guard Or Axial CMTS/KRT Bound",
            "## Current Verdict",
            (
                "2115 sharpens the spin/coupling bottleneck. The good news is real: the spin sector has a clean exact route to zero. "
                "If ordinary spinors and spin transport use only `omega_LC[e_obs]`, and no independent contorsion or axial torsion "
                "current appears in the parent matter action, then the spin contribution to independent `Gamma_MTS` variation vanishes. "
                "On the LC branch this also kills torsion and `A_MTS^mu` exactly."
            ),
            (
                "The current corpus still has not signed that route. So the claim remains blocked, but not foggy. The missing object is "
                "now the coupling signature: either prove `omega_spin=omega_LC[e_obs]` parent-wide, or retain the affine residual "
                "`C_MTS -> T_MTS -> A_MTS -> b_eff` and source `xi_A`, `C_basis`, frame/component labels, and a component-specific KRT bound."
            ),
            (
                "This is not a defeat; it is the right kind of narrowing. The theory is no longer failing on an amorphous local-GR worry. "
                "It is asking for a precise coupling contract."
            ),
            "## Source Register",
            md_table(sources, ["source_id", "source_path", "path_exists", "needles_found", "role", "valid_for_claim"]),
            "## Spin Coframe-Owned Guard",
            md_table(
                spin_rows,
                [
                    "guard_id",
                    "clause",
                    "status",
                    "statement",
                    "math_consequence",
                    "missing_input",
                    "theorem_role",
                    "valid_for_claim",
                ],
            ),
            "## Axial CMTS/KRT Map",
            md_table(
                axial_rows,
                ["map_id", "object", "formula", "status", "units", "needed_inputs", "score_ready", "valid_for_claim"],
            ),
            "## KRT Bound Anchor Status",
            md_table(
                bound_rows,
                [
                    "bound_id",
                    "observable",
                    "source_url",
                    "doi_or_ref",
                    "bound_value",
                    "bound_units",
                    "source_status",
                    "ready_for_scoring",
                    "reason_not_scoreable",
                    "valid_for_claim",
                ],
            ),
            "## Claim Gates",
            md_table(gates, ["gate_id", "gate", "gate_pass", "rationale", "valid_for_claim", "claim_allowed"]),
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
    spin_rows = spin_guard_rows()
    axial_rows = axial_cmts_krt_map_rows()
    bound_rows = krt_bound_status_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_rows = next_target_rows()

    paths = {
        "sources": OUT / "P8_Y5_PARENT_QLOC_2115_SOURCE_REGISTER.csv",
        "spin": OUT / "P8_Y5_PARENT_QLOC_2115_SPIN_GUARD_GATE.csv",
        "axial": OUT / "P8_Y5_PARENT_QLOC_2115_AXIAL_CMTS_KRT_MAP.csv",
        "bound": OUT / "P8_Y5_PARENT_QLOC_2115_KRT_BOUND_ANCHOR_STATUS.csv",
        "gates": OUT / "P8_Y5_PARENT_QLOC_2115_CLAIM_GATES.csv",
        "decisions": OUT / "P8_Y5_PARENT_QLOC_2115_DECISION_LEDGER.csv",
        "next": OUT / "P8_Y5_PARENT_QLOC_2115_NEXT_TARGET.csv",
        "branch": OUT / "P8_Y5_PARENT_QLOC_2115_BRANCH_COPIES.csv",
        "validation": OUT / "P8_Y5_BRR545_2115_VALIDATION.csv",
    }

    write_csv(paths["sources"], sources)
    write_csv(paths["spin"], spin_rows)
    write_csv(paths["axial"], axial_rows)
    write_csv(paths["bound"], bound_rows)
    write_csv(paths["gates"], gates)
    write_csv(paths["decisions"], decisions)
    write_csv(paths["next"], next_rows)

    copies = write_branch_copies(spin_rows, axial_rows, bound_rows, next_rows)
    write_csv(paths["branch"], copies)

    remove_pycache()
    csv_paths = [path for key, path in paths.items() if key != "validation"] + [Path(str(copy["destination"])) for copy in copies]
    validation = validation_rows(sources, spin_rows, axial_rows, bound_rows, gates, decisions, next_rows, copies, csv_paths)
    write_csv(paths["validation"], validation)
    write_doc(sources, spin_rows, axial_rows, bound_rows, gates, decisions, next_rows, copies, validation)

    print(f"wrote {DOC}")
    print(f"validation {paths['validation']}")


if __name__ == "__main__":
    main()
