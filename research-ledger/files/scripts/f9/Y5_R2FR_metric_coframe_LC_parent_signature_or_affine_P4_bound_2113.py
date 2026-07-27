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


DOC = ROOT / "2113-Y5-R2FR-metric-coframe-LC-parent-signature-or-affine-P4-bound.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"

SRC_2112_DOC = ROOT / "2112-Y5-R2FR-CDB-component-zero-or-bound-Kconn-Kdomain-Kboundary.md"
CSV_2112_VAL = OUT / "P8_Y5_BRR545_2112_VALIDATION.csv"
CSV_2112_NEXT = OUT / "P8_Y5_PARENT_QLOC_2112_NEXT_TARGET.csv"
CSV_2112_BOUNDS = OUT / "P8_Y5_PARENT_QLOC_2112_CDB_COMPONENT_BOUND_ROWS.csv"

SRC_1828_DOC = ROOT / "1828-Y5-R2FR-connection-hinge-bivector-owner-or-c2-map-fill.md"
CSV_1828_COMPAT = OUT / "P8_Y5_PARENT_QLOC_1828_CONNECTION_COMPATIBILITY_AUDIT.csv"
SRC_1829_DOC = ROOT / "1829-Y5-R2FR-metric-only-connection-theorem-or-P4-hinge-source-pack.md"
CSV_1829_METRIC_ONLY = OUT / "P8_Y5_PARENT_QLOC_1829_METRIC_ONLY_CONNECTION_THEOREM_ATTEMPT.csv"
SRC_1830_DOC = ROOT / "1830-Y5-R2FR-no-independent-connection-parent-grammar-or-P4-row-fill.md"
CSV_1830_GRAMMAR = OUT / "P8_Y5_PARENT_QLOC_1830_NO_INDEPENDENT_CONNECTION_GRAMMAR_ATTEMPT.csv"

SRC_2041_DOC = ROOT / "2041-Y5-R2FR-second-order-no-extra-field-parent-clause-or-R11-priority-fill.md"
CSV_2041_CONN = OUT / "P8_Y5_PARENT_QLOC_2041_TORSION_CONNECTION_DECISION_LEDGER.csv"
SRC_2042_DOC = ROOT / "2042-Y5-R2FR-Levi-Civita-no-hypermomentum-parent-clause-or-P4-connection-row.md"
CSV_2042_NH = OUT / "P8_Y5_PARENT_QLOC_2042_NO_HYPERMOMENTUM_THEOREM_ATTEMPT.csv"
CSV_2042_GAMMA = OUT / "P8_Y5_PARENT_QLOC_2042_GAMMA_SLOT_AUDIT.csv"
CSV_2042_PAL = OUT / "P8_Y5_PARENT_QLOC_2042_PALATINI_LEVI_CIVITA_CONTRACT.csv"
CSV_2042_P4 = OUT / "P8_Y5_PARENT_QLOC_2042_P4_CONNECTION_INTERFACE.csv"
CSV_2042_GATE = OUT / "P8_Y5_PARENT_QLOC_2042_CLAIM_GATE.csv"

SRC_2046_DOC = ROOT / "2046-Y5-R2FR-GammaMTS-affine-torsion-definition-or-LC-zero-theorem.md"
CSV_2046_LC = OUT / "P8_Y5_PARENT_QLOC_2046_LC_ZERO_THEOREM_BRANCH.csv"
CSV_2046_AFFINE = OUT / "P8_Y5_PARENT_QLOC_2046_AFFINE_RESIDUAL_DEFINITION.csv"
CSV_2046_RUNNER = OUT / "P8_Y5_PARENT_QLOC_2046_CONNECTION_DECISION_RUNNER.csv"
CSV_2046_GATE = OUT / "P8_Y5_PARENT_QLOC_2046_CLAIM_GATE.csv"
CSV_1960_P4 = OUT / "P8_Y5_PARENT_QLOC_1960_P4_CONNECTION_ENVELOPE_LEDGER.csv"


def row(**kwargs: object) -> dict[str, object]:
    data = base_row()
    data["claim_allowed"] = False
    data.update(kwargs)
    return data


def truthy(value: object) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"true", "1", "yes", "pass", "valid", "claim_allowed", "selected"}


def formalization_has_2113_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    patterns = (
        "*2113-Y5-R2FR*",
        "*P8_Y5_PARENT_QLOC_2113*",
        "*Y5_R2FR_metric_coframe_LC_parent_signature_or_affine_P4_bound_2113*",
        "*AFRAME_LC_CONNECTION_2113*",
        "*JR2113_GAMMA_SLOT*",
    )
    try:
        return any(path.is_file() for pattern in patterns for path in FORMALIZATION.rglob(pattern))
    except Exception:
        return False


def source_register_rows() -> list[dict[str, object]]:
    source_specs = [
        (
            "SRC2113_00_2112_doc",
            SRC_2112_DOC,
            ["highest-leverage blocker", "NEXT2112_0_2113"],
            "2112 selects the connection/LC parent-signature fork.",
        ),
        (
            "SRC2113_01_2112_validation",
            CSV_2112_VAL,
            ["VAL2112_OVERALL", "PASS", "connection/LC parent signature fork next"],
            "2112 validation passed and kept CDB nonclaim.",
        ),
        (
            "SRC2113_02_2112_bounds",
            CSV_2112_BOUNDS,
            ["CDB2112_1_Kconn_norm", "c_T_or_c_Q", "c_Delta"],
            "2112 K_conn bound formula points to LC signature or affine coefficients.",
        ),
        (
            "SRC2113_03_1828_doc",
            SRC_1828_DOC,
            ["metric-only connection theorem", "CONNECTION_OWNER_FAILS_CURRENT_CORPUS"],
            "1828 frames connection compatibility as theorem-or-P4 fork.",
        ),
        (
            "SRC2113_04_1828_compat",
            CSV_1828_COMPAT,
            ["CCA1828_1_metric_only", "CCA1828_5_Gamma_eff", "CONNECTION_OWNER_FAILS_CURRENT_CORPUS"],
            "1828 machine-readable connection compatibility audit.",
        ),
        (
            "SRC2113_05_1829_doc",
            SRC_1829_DOC,
            ["EXACT_CONDITIONAL_LEMMA", "METRIC_ONLY_THEOREM_NOT_PARENT_SIGNED"],
            "1829 gives the exact metric-only LC lemma and current failure.",
        ),
        (
            "SRC2113_06_1829_metric_only",
            CSV_1829_METRIC_ONLY,
            ["MOC1829_1_exact_lemma", "MOC1829_3_matter_no_hypermomentum", "MOC1829_6_verdict"],
            "1829 metric-only theorem attempt.",
        ),
        (
            "SRC2113_07_1830_doc",
            SRC_1830_DOC,
            ["no independent connection slot", "NO_INDEPENDENT_CONNECTION_GRAMMAR_NOT_PROVEN"],
            "1830 says the no-independent-connection grammar is still unsigned.",
        ),
        (
            "SRC2113_08_1830_grammar",
            CSV_1830_GRAMMAR,
            ["NIC1830_2_omega_definition", "NIC1830_6_verdict", "NO_INDEPENDENT_CONNECTION_GRAMMAR_NOT_PROVEN"],
            "1830 machine-readable grammar gate.",
        ),
        (
            "SRC2113_09_2041_doc",
            SRC_2041_DOC,
            ["NEF2041_5_Levi_Civita_connection", "NOT_PARENT_DERIVED_CURRENT_CORPUS"],
            "2041 places Levi-Civita inside the no-extra-field spine.",
        ),
        (
            "SRC2113_10_2041_connection",
            CSV_2041_CONN,
            ["LC2041_0_metric_formalism", "LC2041_4_P4_fallback", "LC2041_5_verdict"],
            "2041 decision ledger identifies LC or P4 fallback.",
        ),
        (
            "SRC2113_11_2042_doc",
            SRC_2042_DOC,
            ["no independent affine `Gamma` argument", "clean coupling route"],
            "2042 gives the no-hypermomentum coupling route.",
        ),
        (
            "SRC2113_12_2042_no_hyper",
            CSV_2042_NH,
            ["NH2042_1_no_gamma_slot", "EXACT_CONDITIONAL_THEOREM", "CONDITIONAL_THEOREM_PARENT_SIGNATURE_MISSING"],
            "2042 no-hypermomentum theorem attempt.",
        ),
        (
            "SRC2113_13_2042_gamma_slots",
            CSV_2042_GAMMA,
            ["GSA2042_7_verdict", "FAIL_CURRENT_CORPUS", "ordinary matter action"],
            "2042 Gamma-slot audit across matter/source/readout sectors.",
        ),
        (
            "SRC2113_14_2042_palatini",
            CSV_2042_PAL,
            ["PAL2042_3_lc_result", "EXACT_CONDITIONAL_THEOREM", "CONDITIONAL_ONLY_NO_LOCAL_GR_CLAIM"],
            "2042 Palatini LC conditional contract.",
        ),
        (
            "SRC2113_15_2042_p4",
            CSV_2042_P4,
            ["P4C1960_0_combined", "P4C1960_5_hypermomentum", "MISSING_NO_GAMMA_MATTER_PROOF_OR_BOUND"],
            "2042 P4 interface for affine residual fallback.",
        ),
        (
            "SRC2113_16_2042_gate",
            CSV_2042_GATE,
            ["GATE2042_1_Levi_Civita", "FAIL_BLOCKED", "derived local GR/Newton branch"],
            "2042 claim gate blocks local-GR promotion.",
        ),
        (
            "SRC2113_17_2046_doc",
            SRC_2046_DOC,
            ["Gamma_MTS := LC[g_obs]", "affine residual coefficients"],
            "2046 exposes the exact LC-zero versus affine residual fork.",
        ),
        (
            "SRC2113_18_2046_lc",
            CSV_2046_LC,
            ["LCZ2046_1_no_independent_Gamma", "LCZ2046_7_verdict", "THEOREM_AVAILABLE_NOT_PARENT_DERIVED"],
            "2046 LC-zero theorem branch.",
        ),
        (
            "SRC2113_19_2046_affine",
            CSV_2046_AFFINE,
            ["AFF2046_0_residual_definition", "AFF2046_7_verdict", "DEFINED_FALLBACK_NOT_SCOREABLE"],
            "2046 affine residual tensor definition.",
        ),
        (
            "SRC2113_20_2046_runner",
            CSV_2046_RUNNER,
            ["RUN2046_0_metric_coframe_branch", "RUN2046_2_affine_residual_branch", "CONNECTION_FORK_EXPOSED_NONCLAIM"],
            "2046 runner verdict keeps both branches nonclaim.",
        ),
        (
            "SRC2113_21_2046_gate",
            CSV_2046_GATE,
            ["GATE2046_0_connection_owner", "GATE2046_5_local_GR_Newton", "FAIL_BLOCKED"],
            "2046 claim gate blocks torsion/local-GR claim.",
        ),
        (
            "SRC2113_22_1960_p4",
            CSV_1960_P4,
            ["P4C1960_0_combined", "P4C1960_5_hypermomentum", "MISSING_COEFFICIENT_VALUE_UNITS_MAP"],
            "1960 older P4 connection envelope.",
        ),
    ]
    rows: list[dict[str, object]] = []
    for source_id, path, needles, role in source_specs:
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


def lc_signature_rows() -> list[dict[str, object]]:
    rows_data = [
        (
            "LCS2113_0_contract",
            "LC parent signature",
            "Conf_ord^local={e_obs/g_obs,Psi,A_Q,theta}; omega=omega_LC[e_obs]; no independent affine Gamma_MTS slot.",
            "TARGET_SHARP",
            "This is the cleanest route to make K_conn vanish without fitting.",
            "parent action/object-language signature",
        ),
        (
            "LCS2113_1_field_inventory",
            "no independent Gamma",
            "Gamma_MTS is either absent or defined as LC[g_obs], not varied independently.",
            "NOT_PARENT_SIGNED",
            "1830/2046 do not yet sign the field grammar.",
            "explicit parent field inventory",
        ),
        (
            "LCS2113_2_omega_definition",
            "coframe-owned spin connection",
            "omega_obs=omega_LC[e_obs] and spin transport uses the same coframe-owned connection.",
            "EXACT_IF_FIELD_INVENTORY_SIGNED",
            "If true, spin connection variation is Hilbert/coframe stress, not affine hypermomentum.",
            "spinor/source/readout object language",
        ),
        (
            "LCS2113_3_no_hypermomentum",
            "Delta_lambda^{mu nu}=0",
            "S_ord has no independent Gamma argument, so delta S_ord/delta Gamma=0 by definition.",
            "EXACT_CONDITIONAL_THEOREM_PARENT_SIGNATURE_MISSING",
            "2042 gives the theorem; matter/source/clock/orbit slots are not all signed.",
            "Gamma-slot audit closure",
        ),
        (
            "LCS2113_4_torsion_zero",
            "T_MTS=0",
            "For Gamma_MTS=LC[g_obs], T^lambda_{mu nu}=2 Gamma^lambda_{[mu nu]}=0.",
            "EXACT_CONDITIONAL_ZERO",
            "This would kill axial torsion in the LC branch.",
            "LCS2113_1 parent signature",
        ),
        (
            "LCS2113_5_nonmetricity_zero",
            "Q_MTS=0",
            "For Gamma_MTS=LC[g_obs], nabla^Gamma g_obs=0.",
            "EXACT_CONDITIONAL_ZERO",
            "This would kill Weyl/shear nonmetricity in the LC branch.",
            "LCS2113_1 parent signature",
        ),
        (
            "LCS2113_6_projective_silence",
            "projective trace",
            "If no independent Gamma exists, Palatini projective ambiguity has no physical readout slot.",
            "EXACT_CONDITIONAL_ZERO_IF_NO_GAMMA",
            "If a Palatini branch is retained, projective silence remains a separate guard.",
            "choose LC ontology or sign Palatini guard",
        ),
        (
            "LCS2113_7_Gamma_Khat_reconciliation",
            "Gamma_eff/K_hat/q_loc",
            "Gamma_eff/K_hat either reduce to LC/metric-response data or remain q_loc/P4 residuals.",
            "RETAINED_SYMBOLIC_GAP",
            "LC connection helps K_conn, but does not by itself close Gamma_eff/Khat owner bundle.",
            "term-by-term parent response match",
        ),
        (
            "LCS2113_8_Kconn_result_if_signed",
            "K_conn_norm",
            "If LCS2113_1 through LCS2113_7 close, set K_conn_norm=0 for the local LC branch.",
            "CONDITIONAL_STRONG_GATE",
            "This would remove the connection part of Q_cdb.",
            "all LC clauses same parent branch",
        ),
        (
            "LCS2113_9_verdict",
            "LC parent signature current claim",
            "MTS currently proves the LC theorem as a parent-signed branch.",
            "FAIL_CURRENT_CLAIM",
            "Exact theorem exists, but the parent ontology/signature is not yet supplied.",
            "construct/sign parent ordinary local action or retain affine residuals",
        ),
    ]
    return [
        row(
            signature_id=signature_id,
            clause=clause,
            formal_statement=statement,
            current_status=status,
            implication=implication,
            missing_for_claim=missing,
            score_ready=False,
        )
        for signature_id, clause, statement, status, implication, missing in rows_data
    ]


def affine_residual_rows() -> list[dict[str, object]]:
    rows_data = [
        (
            "AFF2113_0_C_MTS",
            "C_MTS^lambda_{mu nu}",
            "C_MTS^lambda_{mu nu}=Gamma_MTS^lambda_{mu nu}-LC[g_obs]^lambda_{mu nu}",
            "DEFINITION_READY_IF_AFFINE_BRANCH_CHOSEN",
            "L^-1",
            "parent Gamma_MTS components and sign convention",
            "master affine residual",
        ),
        (
            "AFF2113_1_torsion",
            "T_MTS^lambda_{mu nu}",
            "T_MTS^lambda_{mu nu}=2 C_MTS^lambda_{[mu nu]}",
            "EXACT_COMPONENT_FORMULA",
            "L^-1",
            "C_MTS components",
            "torsion residual",
        ),
        (
            "AFF2113_2_nonmetricity",
            "Q_MTS,rho mu nu",
            "Q_MTS,rho mu nu=C_MTS^sigma_{rho mu}g_sigma nu+C_MTS^sigma_{rho nu}g_mu sigma",
            "EXACT_COMPONENT_FORMULA_WITH_DECLARED_CONVENTION",
            "L^-1",
            "C_MTS components and metric convention",
            "nonmetricity residual",
        ),
        (
            "AFF2113_3_axial",
            "A_MTS^mu",
            "A_MTS^mu=(1/3)epsilon^{alpha beta gamma mu}C_MTS,alpha[beta gamma]",
            "EXACT_COMPONENT_FORMULA_WITH_ORIENTATION",
            "L^-1 or GeV via 1.973269804e-16 GeV m",
            "orientation/frame and component labels",
            "spin/torsion observable kernel",
        ),
        (
            "AFF2113_4_hypermomentum",
            "Delta_lambda^{mu nu}",
            "Delta_lambda^{mu nu}:=-2/sqrt(-g_obs) delta S_ord/delta Gamma^lambda_{mu nu}",
            "DEFINITION_READY_INPUTS_MISSING",
            "action-density response",
            "Gamma-slot audit for matter/source/readout",
            "connection current source",
        ),
        (
            "AFF2113_5_Kconn_bound",
            "K_conn_norm",
            "K_conn_norm <= K_LC_mismatch + |c_T_or_c_Q|+|c_A_or_S|+|c_Ttrace|+|c_Qtrace|+|c_Qshear|+|c_Delta|",
            "SYMBOLIC_BOUND_FORM_DERIVED_INPUTS_MISSING",
            "local norm",
            "component coefficients, units, source maps, bound table",
            "Q_cdb input",
        ),
        (
            "AFF2113_6_no_cancellation",
            "policy",
            "score each torsion/nonmetricity/projective/hypermomentum component independently; no cancellation against other residuals",
            "GUARD_READY",
            "dimensionless or source-current normalized",
            "componentwise source rows",
            "prevents fitted silence",
        ),
        (
            "AFF2113_7_verdict",
            "affine/P4 fallback",
            "Fallback is tensor-defined but not scoreable.",
            "DEFINED_FALLBACK_NOT_SCOREABLE",
            "mixed",
            "C_MTS, xi_A, frame map, units and component bound table",
            "no local-GR/PPN claim",
        ),
    ]
    return [
        row(
            residual_id=residual_id,
            object_id=object_id,
            formula=formula,
            current_status=status,
            units=units,
            needed_inputs=needed,
            observable_channel=channel,
            score_ready=False,
        )
        for residual_id, object_id, formula, status, units, needed, channel in rows_data
    ]


def impact_rows() -> list[dict[str, object]]:
    rows_data = [
        (
            "IMP2113_0_if_LC_signed",
            "K_conn_norm",
            "0",
            "would remove connection/torsion/nonmetricity/hypermomentum part of Q_cdb",
            "requires full LC parent signature",
        ),
        (
            "IMP2113_1_current",
            "K_conn_norm",
            "AFF2113_5 symbolic bound",
            "connection remains the dominant CDB component because coefficients are missing",
            "fill parent signature or P4 values",
        ),
        (
            "IMP2113_2_local_GR",
            "local GR/Newton",
            "still blocked",
            "LC connection is necessary but not sufficient: EH/no-extra/source-GM/PPN/Gamma-Khat gates remain",
            "after LC, return to EH operator and source coupling gates",
        ),
        (
            "IMP2113_3_empirical_lane",
            "PPN/WEP/clocks/lightcone",
            "not score-ready",
            "affine residuals need component values and observable kernels before testing",
            "C_MTS/xi/frame/bounds",
        ),
    ]
    return [
        row(
            impact_id=impact_id,
            target=target,
            current_result=result,
            effect=effect,
            remaining_requirement=remaining,
            score_ready=False,
        )
        for impact_id, target, result, effect, remaining in rows_data
    ]


def claim_gate_rows() -> list[dict[str, object]]:
    rows_data = [
        ("GATE2113_0_exact_LC_theorem", "LC theorem is mathematically sharp", True, "metric/coframe-only branch gives LC, T=0, Q=0 conditionally"),
        ("GATE2113_1_parent_signature", "parent chooses metric/coframe-only local observed geometry", False, "field inventory and object language are not signed"),
        ("GATE2113_2_no_hypermomentum", "ordinary/source/readout hypermomentum is zero", False, "no independent Gamma slot not proven for all sectors"),
        ("GATE2113_3_Kconn_zero", "K_conn_norm=0 can be claimed", False, "depends on unsigned LC parent signature"),
        ("GATE2113_4_affine_score", "affine/P4 residual can be bounded", False, "C_MTS components, xi, frame map and bound table missing"),
        ("GATE2113_5_local_GR_Newton", "derived local GR/Newton follows", False, "connection gate alone is not full EH/source/PPN closure"),
    ]
    return [
        row(
            gate_id=gate_id,
            gate=gate,
            gate_pass=passes,
            rationale=rationale,
            score_ready=False,
        )
        for gate_id, gate, passes, rationale in rows_data
    ]


def decision_rows() -> list[dict[str, object]]:
    rows_data = [
        (
            "DEC2113_0",
            "LC_THEOREM_STRONG_BUT_UNSIGNED",
            "The connection can be killed exactly if the parent local ontology is metric/coframe-only.",
            "Do not spend more cycles deriving torsion zero; spend them signing the parent Gamma-slot language.",
        ),
        (
            "DEC2113_1",
            "AFFINE_FALLBACK_IS_WELL_DEFINED",
            "If independent Gamma survives, C_MTS gives exact torsion/nonmetricity/axial formulas but no numeric score.",
            "Retain P4 component rows unless LC parent signature closes.",
        ),
        (
            "DEC2113_2",
            "GAMMA_SLOT_AUDIT_NEXT",
            "The missing item is not algebra; it is a sector-by-sector parent object-language signature for matter, spin, source, clocks, light and orbital readout.",
            "Construct or reject the Gamma-slot audit across those sectors.",
        ),
    ]
    return [
        row(decision_id=decision_id, decision=decision, because=because, next_action=next_action)
        for decision_id, decision, because, next_action in rows_data
    ]


def next_target_rows() -> list[dict[str, object]]:
    return [
        row(
            route_id="NEXT2113_0_2114",
            next_target="2114-Y5-R2FR-sector-Gamma-slot-audit-or-affine-CMTS-source-pack.md",
            script="scripts/Y5_R2FR_sector_Gamma_slot_audit_or_affine_CMTS_source_pack_2114.py",
            objective=(
                "Audit every ordinary local sector for an independent affine Gamma slot: gravity, matter, spin, EM/gauge, "
                "source worldtube, clocks, lightcone, orbital readout, and boundary/non-Hilbert currents. If all slots are "
                "Gamma-free/coframe-owned, activate the LC parent signature. If any slot remains live, retain C_MTS/P4 "
                "coefficient rows with units, frame map, coupling xi and observable kernels."
            ),
            forbidden_shortcuts=(
                "assuming all matter is minimally coupled because GR does it; ignoring spin/torsion or projective trace; "
                "calling readout downstream when it enters pre-variation; deleting affine residuals without sector audit; "
                "local-GR/Newton/PPN claim; formalization-workbench edits; GitHub action"
            ),
        )
    ]


def write_branch_copies(
    lc_rows: list[dict[str, object]],
    affine_rows: list[dict[str, object]],
    impact: list[dict[str, object]],
    next_target: list[dict[str, object]],
) -> list[dict[str, object]]:
    copy_specs = [
        (
            "COPY2113_0_source_weight_docs",
            SOURCE_WEIGHT_DOCS / "AFRAME_LC_CONNECTION_2113_NONCLAIM.csv",
            lc_rows + affine_rows + impact,
        ),
        (
            "COPY2113_1_branch_locked_wep",
            BRANCH_WEP / "P8_Y5_PARENT_QLOC_2113_CONNECTION_STATUS_NONCLAIM.csv",
            lc_rows + affine_rows,
        ),
        (
            "COPY2113_2_acquisition_queue",
            QUEUE / "JR2113_GAMMA_SLOT_AUDIT_OR_CMTS_QUEUE.csv",
            next_target + affine_rows,
        ),
    ]
    rows: list[dict[str, object]] = []
    for copy_id, destination, copy_rows in copy_specs:
        write_csv(destination, copy_rows)
        rows.append(
            row(
                copy_id=copy_id,
                destination=str(destination),
                path_exists=destination.exists(),
                row_count=len(copy_rows),
                parse_ok=csv_rows_parse(destination),
            )
        )
    return rows


def all_nonclaim(groups: list[list[dict[str, object]]]) -> bool:
    for group in groups:
        for item in group:
            if truthy(item.get("claim_allowed")) or truthy(item.get("valid_for_claim")):
                return False
    return True


def validation_rows(
    sources: list[dict[str, object]],
    lc_rows: list[dict[str, object]],
    affine_rows: list[dict[str, object]],
    impact: list[dict[str, object]],
    claim_gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_target: list[dict[str, object]],
    copies: list[dict[str, object]],
    csv_paths: list[Path],
) -> list[dict[str, object]]:
    source_ok = all(truthy(source.get("path_exists")) and truthy(source.get("needles_found")) for source in sources)
    lc_ok = (
        any(item.get("signature_id") == "LCS2113_3_no_hypermomentum" and item.get("current_status") == "EXACT_CONDITIONAL_THEOREM_PARENT_SIGNATURE_MISSING" for item in lc_rows)
        and any(item.get("signature_id") == "LCS2113_4_torsion_zero" and item.get("current_status") == "EXACT_CONDITIONAL_ZERO" for item in lc_rows)
        and any(item.get("signature_id") == "LCS2113_9_verdict" and item.get("current_status") == "FAIL_CURRENT_CLAIM" for item in lc_rows)
    )
    affine_ok = (
        any(item.get("residual_id") == "AFF2113_0_C_MTS" and item.get("current_status") == "DEFINITION_READY_IF_AFFINE_BRANCH_CHOSEN" for item in affine_rows)
        and any(item.get("residual_id") == "AFF2113_5_Kconn_bound" and item.get("current_status") == "SYMBOLIC_BOUND_FORM_DERIVED_INPUTS_MISSING" for item in affine_rows)
        and any(item.get("residual_id") == "AFF2113_7_verdict" and item.get("current_status") == "DEFINED_FALLBACK_NOT_SCOREABLE" for item in affine_rows)
    )
    impact_ok = (
        any(item.get("impact_id") == "IMP2113_0_if_LC_signed" and item.get("current_result") == "0" for item in impact)
        and any(item.get("impact_id") == "IMP2113_2_local_GR" and item.get("current_result") == "still blocked" for item in impact)
    )
    gates_ok = (
        any(gate.get("gate_id") == "GATE2113_0_exact_LC_theorem" and truthy(gate.get("gate_pass")) for gate in claim_gates)
        and any(gate.get("gate_id") == "GATE2113_3_Kconn_zero" and not truthy(gate.get("gate_pass")) for gate in claim_gates)
        and any(gate.get("gate_id") == "GATE2113_5_local_GR_Newton" and not truthy(gate.get("gate_pass")) for gate in claim_gates)
    )
    decision_ok = any(decision.get("decision_id") == "DEC2113_2" and decision.get("decision") == "GAMMA_SLOT_AUDIT_NEXT" for decision in decisions)
    next_ok = any(target.get("route_id") == "NEXT2113_0_2114" and "sector-Gamma-slot-audit" in str(target.get("next_target")) for target in next_target)
    copies_ok = all(truthy(copy.get("path_exists")) and truthy(copy.get("parse_ok")) and int(copy.get("row_count", 0)) > 0 for copy in copies)
    csv_ok = all(path.exists() and csv_rows_parse(path) for path in csv_paths)
    no_claims_ok = all_nonclaim([sources, lc_rows, affine_rows, impact, claim_gates, decisions, next_target, copies])
    formalization_ok = count_formalization_modified() == 0 and not formalization_has_2113_artifacts()
    no_pycache_ok = not (Path(__file__).resolve().parent / "__pycache__").exists()

    checks = [
        ("VAL2113_00_sources", source_ok, "all cited connection/LC/P4 sources exist and contain expected needles"),
        ("VAL2113_01_lc_signature", lc_ok, "LC theorem is exact conditional but parent signature remains unsigned"),
        ("VAL2113_02_affine_fallback", affine_ok, "affine C_MTS fallback is tensor-defined but not scoreable"),
        ("VAL2113_03_impact", impact_ok, "Kconn would vanish if LC signed; local GR remains blocked now"),
        ("VAL2113_04_claim_gates", gates_ok, "exact theorem passes as math but Kconn/local-GR claims remain blocked"),
        ("VAL2113_05_decision", decision_ok, "decision selects sector Gamma-slot audit next"),
        ("VAL2113_06_next", next_ok, "next target is 2114 sector Gamma-slot audit or C_MTS source pack"),
        ("VAL2113_07_branch_copies", copies_ok, "branch copies exist and parse"),
        ("VAL2113_08_csv_parse", csv_ok, "all generated CSVs parse cleanly"),
        ("VAL2113_09_no_claim_flags", no_claims_ok, "no generated row allows a claim or score"),
        ("VAL2113_10_formalization_clean", formalization_ok, "formalization-workbench untouched by 2113"),
        ("VAL2113_11_no_pycache", no_pycache_ok, "scripts __pycache__ removed"),
    ]
    validation = [row(check_id=check_id, status="PASS" if passed else "FAIL", detail=detail) for check_id, passed, detail in checks]
    overall_ok = all(item["status"] == "PASS" for item in validation)
    validation.append(
        row(
            check_id="VAL2113_OVERALL",
            status="PASS" if overall_ok else "FAIL",
            detail=(
                "2113 writes the exact LC parent-signature contract, keeps Kconn zero nonclaim until sector Gamma slots close, "
                "and retains C_MTS/P4 fallback rows."
            ),
        )
    )
    return validation


def write_doc(
    sources: list[dict[str, object]],
    lc_rows: list[dict[str, object]],
    affine_rows: list[dict[str, object]],
    impact: list[dict[str, object]],
    claim_gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_target: list[dict[str, object]],
    copies: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    content = "\n".join(
        [
            "# 2113 - Y5/R2FR Metric-Coframe LC Parent Signature Or Affine P4 Bound",
            "",
            "## Current Verdict",
            "",
            "2113 confirms the gut-level coupling fork. The mathematics is clean: if the local ordinary parent branch is metric/coframe-only, with `Gamma_MTS := LC[g_obs]` and no independent affine `Gamma` slot in matter/source/readout sectors, then hypermomentum vanishes by definition, torsion vanishes, nonmetricity vanishes, and the connection part of `Q_cdb` can be set to zero.",
            "",
            "But this is still not an MTS claim. The current corpus has not signed the parent object language across matter, spin, source worldtubes, clocks, lightcone/orbital readout, and boundary/non-Hilbert currents. If any of those sectors retains an independent affine slot, the fallback is no longer vague: carry `C_MTS = Gamma_MTS - LC[g_obs]` and its torsion/nonmetricity/projective/hypermomentum coefficient rows.",
            "",
            "So the next move is not more algebra on torsion zero. The next move is the sector Gamma-slot audit.",
            "",
            "## Source Register",
            md_table(sources, ["source_id", "source_path", "path_exists", "needles_found", "role", "valid_for_claim"]),
            "## LC Parent Signature Contract",
            md_table(lc_rows, ["signature_id", "clause", "current_status", "formal_statement", "implication", "missing_for_claim", "valid_for_claim"]),
            "## Affine / P4 Fallback Rows",
            md_table(affine_rows, ["residual_id", "object_id", "current_status", "formula", "units", "needed_inputs", "observable_channel", "valid_for_claim"]),
            "## Local-GR Impact Ledger",
            md_table(impact, ["impact_id", "target", "current_result", "effect", "remaining_requirement", "valid_for_claim"]),
            "## Claim Gates",
            md_table(claim_gates, ["gate_id", "gate", "gate_pass", "rationale", "valid_for_claim", "claim_allowed"]),
            "## Decision Ledger",
            md_table(decisions, ["decision_id", "decision", "because", "next_action", "valid_for_claim"]),
            "## Next Target",
            md_table(next_target, ["route_id", "next_target", "script", "objective", "forbidden_shortcuts", "valid_for_claim"]),
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
    lc_rows = lc_signature_rows()
    affine_rows = affine_residual_rows()
    impact = impact_rows()
    claim_gates = claim_gate_rows()
    decisions = decision_rows()
    next_target = next_target_rows()

    paths = {
        "sources": OUT / "P8_Y5_PARENT_QLOC_2113_SOURCE_REGISTER.csv",
        "lc": OUT / "P8_Y5_PARENT_QLOC_2113_LC_PARENT_SIGNATURE_CONTRACT.csv",
        "affine": OUT / "P8_Y5_PARENT_QLOC_2113_AFFINE_P4_FALLBACK_ROWS.csv",
        "impact": OUT / "P8_Y5_PARENT_QLOC_2113_LOCAL_GR_IMPACT_LEDGER.csv",
        "gates": OUT / "P8_Y5_PARENT_QLOC_2113_CLAIM_GATES.csv",
        "decisions": OUT / "P8_Y5_PARENT_QLOC_2113_DECISION_LEDGER.csv",
        "next": OUT / "P8_Y5_PARENT_QLOC_2113_NEXT_TARGET.csv",
        "branch": OUT / "P8_Y5_PARENT_QLOC_2113_BRANCH_COPIES.csv",
        "validation": OUT / "P8_Y5_BRR545_2113_VALIDATION.csv",
    }

    write_csv(paths["sources"], sources)
    write_csv(paths["lc"], lc_rows)
    write_csv(paths["affine"], affine_rows)
    write_csv(paths["impact"], impact)
    write_csv(paths["gates"], claim_gates)
    write_csv(paths["decisions"], decisions)
    write_csv(paths["next"], next_target)

    copies = write_branch_copies(lc_rows, affine_rows, impact, next_target)
    write_csv(paths["branch"], copies)

    remove_pycache()

    csv_paths = [path for key, path in paths.items() if key != "validation"] + [Path(str(copy["destination"])) for copy in copies]
    validation = validation_rows(sources, lc_rows, affine_rows, impact, claim_gates, decisions, next_target, copies, csv_paths)
    write_csv(paths["validation"], validation)
    write_doc(sources, lc_rows, affine_rows, impact, claim_gates, decisions, next_target, copies, validation)

    print(f"wrote {DOC}")
    print(f"validation {paths['validation']}")


if __name__ == "__main__":
    main()
