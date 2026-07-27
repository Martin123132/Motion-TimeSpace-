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


DOC = ROOT / "2114-Y5-R2FR-sector-Gamma-slot-audit-or-affine-CMTS-source-pack.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"

SRC_2113_DOC = ROOT / "2113-Y5-R2FR-metric-coframe-LC-parent-signature-or-affine-P4-bound.md"
CSV_2113_VAL = OUT / "P8_Y5_BRR545_2113_VALIDATION.csv"
CSV_2113_NEXT = OUT / "P8_Y5_PARENT_QLOC_2113_NEXT_TARGET.csv"
CSV_2113_LC = OUT / "P8_Y5_PARENT_QLOC_2113_LC_PARENT_SIGNATURE_CONTRACT.csv"
CSV_2113_AFFINE = OUT / "P8_Y5_PARENT_QLOC_2113_AFFINE_P4_FALLBACK_ROWS.csv"

SRC_2043_DOC = ROOT / "2043-Y5-R2FR-parent-Gamma-slot-owner-or-first-P4-connection-bound-row.md"
CSV_2043_OWNER = OUT / "P8_Y5_PARENT_QLOC_2043_GAMMA_SLOT_OWNER_THEOREM_ATTEMPT.csv"
CSV_2043_ARGS = OUT / "P8_Y5_PARENT_QLOC_2043_ORDINARY_ACTION_ARGUMENT_AUDIT.csv"
CSV_2043_GUARDS = OUT / "P8_Y5_PARENT_QLOC_2043_SPIN_PROJECTIVE_GUARD.csv"
CSV_2043_P4 = OUT / "P8_Y5_PARENT_QLOC_2043_FIRST_P4_BOUND_ROWS.csv"

SRC_2044_DOC = ROOT / "2044-Y5-R2FR-sector-Gamma-slot-audit-or-first-numeric-P4-source.md"
CSV_2044_SECTOR = OUT / "P8_Y5_PARENT_QLOC_2044_SECTOR_GAMMA_AUDIT.csv"
CSV_2044_DELTA = OUT / "P8_Y5_PARENT_QLOC_2044_DELTA_GAMMA_COMPONENT_ENVELOPE.csv"
CSV_2044_ANCHORS = OUT / "P8_Y5_PARENT_QLOC_2044_NUMERIC_P4_SOURCE_ANCHORS.csv"
CSV_2044_MAP = OUT / "P8_Y5_PARENT_QLOC_2044_P4_MAPPING_REQUIREMENTS.csv"

SRC_2047_DOC = ROOT / "2047-Y5-R2FR-parent-observed-geometry-slot-signature-or-CMTS-first-coefficient.md"
CSV_2047_OGS = OUT / "P8_Y5_PARENT_QLOC_2047_OBSERVED_GEOMETRY_SLOT_AUDIT.csv"
CSV_2047_LC = OUT / "P8_Y5_PARENT_QLOC_2047_LC_ZERO_DERIVATION_ATTEMPT.csv"
CSV_2047_CMTS = OUT / "P8_Y5_PARENT_QLOC_2047_CMTS_FIRST_COEFFICIENT_CHAIN.csv"

SRC_2099_DOC = ROOT / "2099-Y5-R2FR-DeltaGamma-component-map-to-P4-WEP-PPN-clock-orbital-residuals.md"
CSV_2099_COMPONENTS = OUT / "P8_Y5_PARENT_QLOC_2099_DELTAGAMMA_COMPONENT_MAP.csv"
CSV_2099_ARENAS = OUT / "P8_Y5_PARENT_QLOC_2099_ARENA_PROJECTION_MATRIX_REGISTER.csv"
CSV_2099_BLOCKERS = OUT / "P8_Y5_PARENT_QLOC_2099_SCORE_BLOCKERS.csv"

CSV_1045_MATTER = OUT / "P8_Y5_R10_1045_PARENT_MATTER_FUNCTOR_SIGNATURE_AUDIT.csv"
CSV_1309_MATTER = OUT / "P8_Y5_R10_1309_MATTER_CONSTANT_PREMISE_GATE.csv"
CSV_943_COFRAME = OUT / "P8_Y5_R10_943_COFRAME_COUPLING_CONTRACT.csv"
CSV_944_DESCENT = OUT / "P8_Y5_R10_944_DESCENT_PROOF_GATE.csv"
CSV_988_EM = OUT / "P8_Y5_R10_988_EM_LOCK_THEOREM_GATE.csv"
CSV_989_EM = OUT / "P8_Y5_R10_989_EM_LOCK_SIGNATURE_AUDIT.csv"
CSV_1068_SOURCE = OUT / "P8_Y5_R10_1068_SOURCE_WORLDTUBE_REQUIREMENTS.csv"
CSV_1068_ORBIT = OUT / "P8_Y5_R10_1068_MICROSCOPE_ORBIT_READOUT_REQUIREMENTS.csv"
CSV_1071_KERNEL = OUT / "P8_Y5_R10_1071_OFFICIAL_KERNEL_COMPONENTS.csv"
CSV_1209_DOMAIN = OUT / "P8_Y5_R10_1209_DOMAIN_MOTION_PROJECTOR_STRESS_AUDIT.csv"


def row(**kwargs: object) -> dict[str, object]:
    data = base_row()
    data["claim_allowed"] = False
    data.update(kwargs)
    return data


def truthy(value: object) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"true", "1", "yes", "pass", "valid", "claim_allowed", "selected"}


def formalization_has_2114_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    patterns = (
        "*2114-Y5-R2FR*",
        "*P8_Y5_PARENT_QLOC_2114*",
        "*Y5_R2FR_sector_Gamma_slot_audit_or_affine_CMTS_source_pack_2114*",
        "*AFRAME_GAMMA_SLOT_2114*",
        "*JR2114_SPIN*",
    )
    try:
        return any(path.is_file() for pattern in patterns for path in FORMALIZATION.rglob(pattern))
    except Exception:
        return False


def source_register_rows() -> list[dict[str, object]]:
    source_specs = [
        ("SRC2114_00_2113_doc", SRC_2113_DOC, ["sector Gamma-slot audit", "C_MTS"], "2113 selects the sector Gamma-slot audit."),
        ("SRC2114_01_2113_validation", CSV_2113_VAL, ["VAL2113_OVERALL", "PASS", "sector Gamma-slot audit"], "2113 validation passed."),
        ("SRC2114_02_2113_lc", CSV_2113_LC, ["LCS2113_3_no_hypermomentum", "LCS2113_9_verdict", "FAIL_CURRENT_CLAIM"], "2113 LC contract and current failure."),
        ("SRC2114_03_2113_affine", CSV_2113_AFFINE, ["AFF2113_0_C_MTS", "AFF2113_7_verdict", "DEFINED_FALLBACK_NOT_SCOREABLE"], "2113 C_MTS fallback rows."),
        ("SRC2114_04_2043_doc", SRC_2043_DOC, ["future parent action must exhaust the ordinary slots", "first P4 fallback rows"], "2043 makes Gamma-slot ownership an action-language problem."),
        ("SRC2114_05_2043_owner", CSV_2043_OWNER, ["GSO2043_6_verdict", "NOT_PARENT_DERIVED_CURRENT_CORPUS"], "2043 Gamma-slot owner theorem attempt."),
        ("SRC2114_06_2043_args", CSV_2043_ARGS, ["ARG2043_3_affine_Gamma", "forbidden_or_retained_P4", "FAIL_CURRENT_CORPUS"], "2043 ordinary action argument audit."),
        ("SRC2114_07_2043_guards", CSV_2043_GUARDS, ["SPG2043_0_spin_guard", "SPG2043_5_verdict", "FAIL_CURRENT_CORPUS"], "2043 spin/projective/nonmetricity guards."),
        ("SRC2114_08_2043_p4", CSV_2043_P4, ["P4B2043_0_hypermomentum", "P4B2043_1_axial_torsion", "MISSING_SOURCE_BACKED_BOUND"], "2043 broad and axial P4 fallback rows."),
        ("SRC2114_09_2044_doc", SRC_2044_DOC, ["sector by sector", "1e-31 GeV"], "2044 sector audit and numeric torsion anchor."),
        ("SRC2114_10_2044_sector", CSV_2044_SECTOR, ["SECG2044_6_verdict", "FAIL_CURRENT_CORPUS", "UNSIGNED_HIGHEST_P4_RISK"], "2044 sector Gamma audit."),
        ("SRC2114_11_2044_delta", CSV_2044_DELTA, ["DELTA2044_6_total_abs", "NOT_RUN_COMPONENTS_MISSING", "no-cancellation"], "2044 Delta_Gamma envelope."),
        ("SRC2114_12_2044_anchors", CSV_2044_ANCHORS, ["P4SRC2044_0_KRT2008_axial_torsion_anchor", "1e-31", "SOURCE_BACKED_ANCHOR_NOT_MTS_MAP"], "2044 source-backed but unmapped torsion anchor."),
        ("SRC2114_13_2044_map", CSV_2044_MAP, ["MAP2044_0_component_basis", "MISSING_BASIS_MAP", "CLAIM_BLOCKED_CURRENTLY"], "2044 P4 mapping requirements."),
        ("SRC2114_14_2047_doc", SRC_2047_DOC, ["parent observed-geometry slot", "C_MTS"], "2047 observed-geometry slot and C_MTS chain."),
        ("SRC2114_15_2047_ogs", CSV_2047_OGS, ["OGS2047_7_verdict", "FAIL_CURRENT_CORPUS_PARENT_SIGNATURE_NOT_DERIVED"], "2047 observed geometry slot audit."),
        ("SRC2114_16_2047_lc", CSV_2047_LC, ["LCD2047_0_variational_absence", "LCD2047_5_verdict", "MATH_CLEAN_PARENT_SIGNATURE_MISSING"], "2047 LC-zero derivation attempt."),
        ("SRC2114_17_2047_cmts", CSV_2047_CMTS, ["CMTS2047_0_C_tensor", "CMTS2047_VERDICT", "FIRST_CMTS_COEFFICIENT_ROW_STAGED_NOT_SCOREABLE"], "2047 C_MTS coefficient chain."),
        ("SRC2114_18_1045_matter", CSV_1045_MATTER, ["MFS1045_2_matter_bundle_functor", "MFS1045_6_verdict"], "1045 matter functor descent audit."),
        ("SRC2114_19_1309_matter", CSV_1309_MATTER, ["MCG1309_0_observed_coframe", "MCG1309_4_radiative_readout_closure"], "1309 matter constants and readout gate."),
        ("SRC2114_20_943_coframe", CSV_943_COFRAME, ["CFC943_4_connection_lock", "CFC943_7_contract_verdict"], "943 coframe coupling and connection lock."),
        ("SRC2114_21_944_descent", CSV_944_DESCENT, ["QDG944_4_geometry_stack_descent", "QDG944_7_total"], "944 quotient/coframe descent proof gate."),
        ("SRC2114_22_988_em", CSV_988_EM, ["EMLOCK988_2_current_owner", "EMLOCK988_5_theorem_verdict"], "988 EM lock theorem gate."),
        ("SRC2114_23_989_em", CSV_989_EM, ["ELA989_2_current_owner", "ELA989_5_total"], "989 EM lock signature audit."),
        ("SRC2114_24_1068_source", CSV_1068_SOURCE, ["SWT1068_5_verdict", "SOURCE_WORLDTUBE_NOT_ACQUIRED"], "1068 source worldtube requirements."),
        ("SRC2114_25_1068_orbit", CSV_1068_ORBIT, ["ORB1068_5_verdict", "ORBIT_READOUT_NOT_ACQUIRED"], "1068 orbital readout requirements."),
        ("SRC2114_26_1071_kernel", CSV_1071_KERNEL, ["KER1071_6_verdict", "official kernel skeleton acquired"], "1071 MICROSCOPE kernel skeleton."),
        ("SRC2114_27_1209_domain", CSV_1209_DOMAIN, ["DMP1209_2_projector_stress_zero_branch", "DMP1209_4_total_epsilon_status"], "1209 domain/projector stress audit."),
        ("SRC2114_28_2099_doc", SRC_2099_DOC, ["seven-component local current vector", "nothing is score-ready"], "2099 test-facing DeltaGamma map."),
        ("SRC2114_29_2099_components", CSV_2099_COMPONENTS, ["DGM2099_0_spin", "DGM2099_6_projective", "score_ready"], "2099 DeltaGamma component map."),
        ("SRC2114_30_2099_arenas", CSV_2099_ARENAS, ["APM2099_1_WEP", "APM2099_5_ORBITAL"], "2099 arena projection matrix register."),
        ("SRC2114_31_2099_blockers", CSV_2099_BLOCKERS, ["SBL2099_0_component_values", "SBL2099_4_no_cancellation"], "2099 score blockers."),
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


def sector_audit_rows() -> list[dict[str, object]]:
    rows_data = [
        (
            "SGS2114_0_gravity_geometry",
            "gravity/observed geometry",
            "S_grav/local branch carries e_obs or g_obs; Gamma_MTS absent or LC[g_obs]",
            "UNSIGNED_CORE_CLAUSE",
            "OGS2047 says this would activate LC-zero but is not parent-signed.",
            "parent action argument list and q/e_obs functor",
            "C_MTS master residual if false",
        ),
        (
            "SGS2114_1_ordinary_matter",
            "ordinary matter",
            "S_matter[Psi_A,e_obs(q),omega_LC[e_obs(q)],A_Q,theta_A] with no independent Gamma",
            "CONDITIONAL_NOT_PARENT_SIGNED",
            "1045/1309 give contracts, not a parent action signature.",
            "matter bundle functor and constants/superselection closure",
            "Delta_matter",
        ),
        (
            "SGS2114_2_spin",
            "spinor/spin transport",
            "omega_spin=omega_LC[e_obs] only; no independent contorsion or axial torsion coupling",
            "UNSIGNED_HIGHEST_P4_RISK",
            "2044 marks spin as highest P4 risk; KRT anchor exists but MTS map is missing.",
            "spin coframe-owned connection guard",
            "Delta_spin_axial; c_A_or_S_mu",
        ),
        (
            "SGS2114_3_EM_gauge",
            "EM/internal gauge",
            "A_Q is an internal gauge connection with fixed parent charge lattice, not affine Gamma",
            "PARTIAL_OWNER_SEPARATE_OPEN_GATE",
            "988/989 keep T_Q/current/unique-F2/readout clauses unsigned.",
            "charge-generator/current owner and no alpha vertex",
            "material_marker_connection_current; alpha_EM residual",
        ),
        (
            "SGS2114_4_source_worldtube",
            "source/worldtube",
            "S_source[W,e_obs,tau_obs] has no Gamma-source, support, boundary torsion or non-Hilbert current",
            "UNSIGNED",
            "1068 source profile/composition/support inputs are missing; 2044 keeps source slot live.",
            "source worldtube owner and no post-readout support shift",
            "Delta_source; source_support_connection_current",
        ),
        (
            "SGS2114_5_clocks_rods_light",
            "clocks/rods/lightcones",
            "clock and light readout use metric proper time/null cones from g_obs only",
            "UNSIGNED",
            "2043/2044/2099 retain Weyl and shear nonmetricity channels.",
            "clock/rod/lightcone Gamma-free readout or nonmetricity bound",
            "Delta_clock_light; Q_trace; Q_shear",
        ),
        (
            "SGS2114_6_orbital_readout",
            "orbital/Newton/GM readout",
            "orbits are downstream functors of source-measure -> Poisson/Gauss -> g_obs, not Gamma inputs",
            "UNSIGNED_DOWNSTREAM",
            "1068/1071 keep orbit/readout kernel and source leg not acquired.",
            "orbit kernel/source-GM transfer and no fitted-GM absorption",
            "Delta_orbit; orbital_readout_connection_current",
        ),
        (
            "SGS2114_7_boundary_nonHilbert",
            "boundary/non-Hilbert currents",
            "boundary, support and non-Hilbert currents carry no affine charge or are explicit residuals",
            "UNSIGNED",
            "2043/2047/1209 keep boundary/projector/support current caveats open.",
            "boundary/source/projector silence or finite component rows",
            "Delta_boundary; K_comm; K_boundary",
        ),
        (
            "SGS2114_8_projective_trace",
            "projective trace",
            "projective mode is gauge/unobservable in every sector or separately bounded",
            "UNSIGNED",
            "2043 guard and 2099 projective component remain live.",
            "all-sector projective invariance proof",
            "projective_trace_current",
        ),
        (
            "SGS2114_9_verdict",
            "all Gamma slots",
            "all sectors are Gamma-free/coframe-owned in one parent action language",
            "FAIL_CURRENT_CLAIM",
            "No sector audit closes enough to activate LC parent signature.",
            "spin guard first, then source/readout/boundary slots",
            "retain C_MTS/P4 source pack",
        ),
    ]
    return [
        row(
            audit_id=audit_id,
            sector=sector,
            required_gamma_free_form=form,
            current_status=status,
            evidence=evidence,
            missing_for_lc_activation=missing,
            fallback_component=fallback,
            lc_activation_ready=False,
            score_ready=False,
        )
        for audit_id, sector, form, status, evidence, missing, fallback in rows_data
    ]


def lc_activation_rows() -> list[dict[str, object]]:
    rows_data = [
        ("LCA2114_0_contract", "LC activation condition", "SGS2114_0 through SGS2114_8 all parent-signed or residualized", "TARGET_SHARP", "would activate 2046/2113 LC-zero theorem"),
        ("LCA2114_1_no_hyper", "Delta_lambda^{mu nu}=0", "all ordinary/source/readout sectors have no independent Gamma argument", "FAIL_CURRENT_CLAIM", "sector audit leaves live slots"),
        ("LCA2114_2_Kconn_zero", "K_conn_norm=0", "Gamma_MTS=LC[g_obs] and no C_MTS branch survives", "FAIL_CURRENT_CLAIM", "LC parent signature not activated"),
        ("LCA2114_3_torsion_nonmetricity", "T_MTS=Q_MTS=0", "C_MTS=0 by parent ontology, not by fitting", "FAIL_CURRENT_CLAIM", "spin/nonmetric/projective guards unsigned"),
        ("LCA2114_4_partial_use", "conditional LC lemmas", "LC theorem remains usable as a future contract", "CONDITIONAL_MATH_RETAINED", "do not demote the route; only block the claim"),
        ("LCA2114_5_verdict", "LC activation", "MTS can now claim local LC connection branch", "FAIL_CURRENT_CLAIM", "Gamma-slot audit did not close all sectors"),
    ]
    return [
        row(
            gate_id=gate_id,
            gate=gate,
            requirement=requirement,
            current_status=status,
            implication=implication,
            claim_ready=False,
        )
        for gate_id, gate, requirement, status, implication in rows_data
    ]


def cmts_source_pack_rows() -> list[dict[str, object]]:
    rows_data = [
        (
            "CMTS2114_0_master_tensor",
            "C_MTS^lambda_{mu nu}",
            "C_MTS=Gamma_MTS-LC[g_obs]",
            "MISSING_PARENT_C_MTS_FIELD_OR_LC_ZERO_SELECTION",
            "L^-1",
            "parent choice: LC zero or independent affine branch",
            "all local connection residuals",
        ),
        (
            "CMTS2114_1_spin_axial",
            "Delta_spin_axial / A_MTS^mu",
            "A_MTS^mu=(1/3)epsilon C_MTS,alpha[beta gamma]",
            "SOURCE_ANCHOR_EXISTS_MTS_MAP_MISSING",
            "m^-1 or GeV with xi_A/C_basis",
            "spin coframe guard or KRT basis/unit/frame map",
            "spin;clock;WEP;source_charge",
        ),
        (
            "CMTS2114_2_matter_hyper",
            "Delta_matter",
            "||delta S_matter/delta Gamma||",
            "MISSING_PARENT_NO_GAMMA_SIGNATURE_OR_COMPONENT_BOUND",
            "hypermomentum or normalized dimensionless",
            "matter functor parent action signature or component bound",
            "matter;WEP;R10;local_GR",
        ),
        (
            "CMTS2114_3_source_support",
            "Delta_source",
            "||delta S_source/delta Gamma||",
            "MISSING_SOURCE_WORLDTUBE_GAMMA_OWNER_OR_BOUND",
            "hypermomentum or normalized dimensionless",
            "source stress/profile/composition/support and Gamma-free source action",
            "source_charge;Newton_GM;WEP",
        ),
        (
            "CMTS2114_4_clock_light",
            "Delta_clock_light",
            "||delta S_clock/light/delta Gamma||",
            "MISSING_CLOCK_LIGHTCONE_NONMETRICITY_MAP_OR_BOUND",
            "hypermomentum or inverse length normalized",
            "clock/rod/lightcone response operators and Q_trace/Q_shear normalization",
            "clock;Shapiro;PPN",
        ),
        (
            "CMTS2114_5_orbit",
            "Delta_orbit",
            "||delta S_orbit/readout/delta Gamma||",
            "MISSING_ORBITAL_READOUT_GAMMA_SILENCE_OR_BOUND",
            "hypermomentum or normalized dimensionless",
            "official orbit/readout kernel and GM transfer convention",
            "orbital;PPN;Newton_GM",
        ),
        (
            "CMTS2114_6_boundary",
            "Delta_boundary",
            "||delta S_boundary/nonH/delta Gamma||",
            "MISSING_BOUNDARY_NONHILBERT_GAMMA_ZERO_OR_BOUND",
            "hypermomentum or normalized dimensionless",
            "boundary/projector/support silence or finite residual rows",
            "conservation;source_charge;local_GR",
        ),
        (
            "CMTS2114_7_projective",
            "projective_trace_current",
            "projective current absolute component",
            "MISSING_PROJECTIVE_INVARIANCE_OR_BOUND",
            "inverse length or normalized",
            "all-sector projective invariance or source/clock bound",
            "WEP;clock;source_charge",
        ),
        (
            "CMTS2114_8_total",
            "Delta_Gamma_abs",
            "sum_i abs(Delta_i) with no cancellation",
            "NOT_RUN_COMPONENTS_MISSING",
            "common DeltaGamma normalization",
            "component values, common units, projection matrices",
            "all connection tests",
        ),
    ]
    return [
        row(
            pack_id=pack_id,
            component=component,
            formula=formula,
            current_status=status,
            units=units,
            needed_inputs=needed,
            observable_links=links,
            score_ready=False,
        )
        for pack_id, component, formula, status, units, needed, links in rows_data
    ]


def arena_impact_rows() -> list[dict[str, object]]:
    rows_data = [
        ("ARENA2114_0_R10", "R10", "source_support_connection_current;orbital_readout_connection_current", "P_DeltaGamma_to_alpha_lambda", "MISSING_PROJECTION_MATRIX", "no R10/local-GR pass"),
        ("ARENA2114_1_WEP", "WEP/MICROSCOPE", "spin_hypermomentum;material_marker_connection_current;clock_rod_nonmetric_connection_current;projective_trace_current", "P_WEP_eta_AB", "MISSING_PROJECTION_MATRIX_AND_SOURCE_KERNEL", "WEP remains harsh local-coupling gate"),
        ("ARENA2114_2_PPN", "PPN", "source_support_connection_current;photon_lightcone_connection_current;orbital_readout_connection_current", "P_DeltaGamma_to_metric_PPN", "MISSING_PROJECTION_MATRIX", "PPN residual vector remains nonclaim"),
        ("ARENA2114_3_CLOCK", "clocks/redshift", "clock_rod_nonmetric_connection_current;spin_hypermomentum;material_marker_connection_current;projective_trace_current", "P_clock", "MISSING_RESPONSE_OPERATOR", "clock route cannot claim Gamma silence"),
        ("ARENA2114_4_LIGHT", "lightcone/Shapiro", "photon_lightcone_connection_current;clock_rod_nonmetric_connection_current;spin_hypermomentum", "P_lightcone", "MISSING_RESPONSE_OPERATOR", "lightcone route cannot claim Gamma silence"),
        ("ARENA2114_5_ORBIT", "orbital/Newton source", "orbital_readout_connection_current;source_support_connection_current;projective_trace_current", "P_DeltaGamma_to_orbital_residual", "MISSING_ORBIT_KERNEL_AND_GM_TRANSFER", "Newton/GM source branch remains guarded"),
    ]
    return [
        row(
            arena_id=arena_id,
            arena=arena,
            components=components,
            projection_matrix=matrix,
            current_status=status,
            implication=implication,
            score_ready=False,
        )
        for arena_id, arena, components, matrix, status, implication in rows_data
    ]


def claim_gate_rows() -> list[dict[str, object]]:
    rows_data = [
        ("GATE2114_0_sector_audit_complete", "sector Gamma-slot audit exists", True, "all ordinary local sectors are listed with status and fallback component"),
        ("GATE2114_1_LC_activate", "LC parent signature can activate", False, "multiple sectors remain unsigned"),
        ("GATE2114_2_Kconn_zero", "K_conn_norm=0 can be claimed", False, "LC activation fails current claim"),
        ("GATE2114_3_CMTS_source_pack", "C_MTS/P4 source pack is explicit", True, "component rows, units and missing inputs are staged"),
        ("GATE2114_4_numeric_score", "affine/P4 residuals are score-ready", False, "component values, units, kernels and projections missing"),
        ("GATE2114_5_local_GR_Newton", "derived local GR/Newton follows", False, "Gamma-slot/LC and source/PPN gates remain open"),
    ]
    return [
        row(gate_id=gate_id, gate=gate, gate_pass=passes, rationale=rationale, score_ready=False)
        for gate_id, gate, passes, rationale in rows_data
    ]


def decision_rows() -> list[dict[str, object]]:
    rows_data = [
        (
            "DEC2114_0",
            "LC_NOT_ACTIVATED",
            "The audit is complete enough to block the claim: matter is conditional, spin/source/clock/light/orbit/boundary/projective slots are unsigned.",
            "Keep LC as the preferred theorem route but do not claim it.",
        ),
        (
            "DEC2114_1",
            "CMTS_SOURCE_PACK_RETAINED",
            "If any affine slot survives, C_MTS and Delta_Gamma_abs are the honest fallback.",
            "Carry component rows with no cancellation.",
        ),
        (
            "DEC2114_2",
            "SPIN_GUARD_NEXT",
            "Spin is marked highest P4 risk, has a real external torsion anchor, and is the sharpest sector to either theorem-zero or bound.",
            "Attack spin/coframe-owned connection guard or axial C_MTS/KRT map next.",
        ),
    ]
    return [row(decision_id=decision_id, decision=decision, because=because, next_action=next_action) for decision_id, decision, because, next_action in rows_data]


def next_target_rows() -> list[dict[str, object]]:
    return [
        row(
            route_id="NEXT2114_0_2115",
            next_target="2115-Y5-R2FR-spin-coframe-owned-connection-guard-or-axial-CMTS-KRT-bound.md",
            script="scripts/Y5_R2FR_spin_coframe_owned_connection_guard_or_axial_CMTS_KRT_bound_2115.py",
            objective=(
                "Try to close the spin sector Gamma slot: prove spinors/spin transport use omega_LC[e_obs] with no independent "
                "contorsion or axial torsion current. If not, build the axial C_MTS -> KRT torsion-component map with basis, units, "
                "frame convention, coupling xi_A, no-cancellation and source-backed bound rows."
            ),
            forbidden_shortcuts=(
                "assuming spin is harmless because ordinary GR uses omega_LC; using KRT 1e-31 GeV as an MTS pass without basis/unit/frame map; "
                "cancelling axial torsion against other components; local-GR/Newton/PPN claim; formalization-workbench edits; GitHub action"
            ),
        )
    ]


def write_branch_copies(
    sector_rows: list[dict[str, object]],
    lc_rows: list[dict[str, object]],
    cmts_rows: list[dict[str, object]],
    arena_rows: list[dict[str, object]],
    next_target: list[dict[str, object]],
) -> list[dict[str, object]]:
    copy_specs = [
        ("COPY2114_0_source_weight_docs", SOURCE_WEIGHT_DOCS / "AFRAME_GAMMA_SLOT_2114_NONCLAIM.csv", sector_rows + lc_rows + cmts_rows + arena_rows),
        ("COPY2114_1_branch_locked_wep", BRANCH_WEP / "P8_Y5_PARENT_QLOC_2114_GAMMA_SLOT_STATUS_NONCLAIM.csv", sector_rows + cmts_rows + arena_rows),
        ("COPY2114_2_acquisition_queue", QUEUE / "JR2114_SPIN_GUARD_OR_AXIAL_CMTS_QUEUE.csv", next_target + cmts_rows),
    ]
    rows: list[dict[str, object]] = []
    for copy_id, destination, copy_rows in copy_specs:
        write_csv(destination, copy_rows)
        rows.append(row(copy_id=copy_id, destination=str(destination), path_exists=destination.exists(), row_count=len(copy_rows), parse_ok=csv_rows_parse(destination)))
    return rows


def all_nonclaim(groups: list[list[dict[str, object]]]) -> bool:
    for group in groups:
        for item in group:
            if truthy(item.get("claim_allowed")) or truthy(item.get("valid_for_claim")):
                return False
    return True


def validation_rows(
    sources: list[dict[str, object]],
    sectors: list[dict[str, object]],
    lc_rows: list[dict[str, object]],
    cmts_rows: list[dict[str, object]],
    arenas: list[dict[str, object]],
    claim_gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_target: list[dict[str, object]],
    copies: list[dict[str, object]],
    csv_paths: list[Path],
) -> list[dict[str, object]]:
    source_ok = all(truthy(source.get("path_exists")) and truthy(source.get("needles_found")) for source in sources)
    sector_ok = (
        any(item.get("audit_id") == "SGS2114_2_spin" and item.get("current_status") == "UNSIGNED_HIGHEST_P4_RISK" for item in sectors)
        and any(item.get("audit_id") == "SGS2114_9_verdict" and item.get("current_status") == "FAIL_CURRENT_CLAIM" for item in sectors)
    )
    lc_ok = any(item.get("gate_id") == "LCA2114_5_verdict" and item.get("current_status") == "FAIL_CURRENT_CLAIM" for item in lc_rows)
    cmts_ok = (
        any(item.get("pack_id") == "CMTS2114_1_spin_axial" and item.get("current_status") == "SOURCE_ANCHOR_EXISTS_MTS_MAP_MISSING" for item in cmts_rows)
        and any(item.get("pack_id") == "CMTS2114_8_total" and item.get("current_status") == "NOT_RUN_COMPONENTS_MISSING" for item in cmts_rows)
    )
    arena_ok = any(item.get("arena_id") == "ARENA2114_1_WEP" and item.get("current_status") == "MISSING_PROJECTION_MATRIX_AND_SOURCE_KERNEL" for item in arenas)
    gates_ok = (
        any(gate.get("gate_id") == "GATE2114_0_sector_audit_complete" and truthy(gate.get("gate_pass")) for gate in claim_gates)
        and any(gate.get("gate_id") == "GATE2114_1_LC_activate" and not truthy(gate.get("gate_pass")) for gate in claim_gates)
        and any(gate.get("gate_id") == "GATE2114_5_local_GR_Newton" and not truthy(gate.get("gate_pass")) for gate in claim_gates)
    )
    decision_ok = any(decision.get("decision_id") == "DEC2114_2" and decision.get("decision") == "SPIN_GUARD_NEXT" for decision in decisions)
    next_ok = any(target.get("route_id") == "NEXT2114_0_2115" and "spin-coframe-owned-connection" in str(target.get("next_target")) for target in next_target)
    copies_ok = all(truthy(copy.get("path_exists")) and truthy(copy.get("parse_ok")) and int(copy.get("row_count", 0)) > 0 for copy in copies)
    csv_ok = all(path.exists() and csv_rows_parse(path) for path in csv_paths)
    no_claims_ok = all_nonclaim([sources, sectors, lc_rows, cmts_rows, arenas, claim_gates, decisions, next_target, copies])
    formalization_ok = count_formalization_modified() == 0 and not formalization_has_2114_artifacts()
    no_pycache_ok = not (Path(__file__).resolve().parent / "__pycache__").exists()

    checks = [
        ("VAL2114_00_sources", source_ok, "all cited Gamma-slot/sector/source files exist and contain expected needles"),
        ("VAL2114_01_sector_audit", sector_ok, "sector Gamma-slot audit blocks LC activation and identifies spin as highest P4 risk"),
        ("VAL2114_02_lc_activation", lc_ok, "LC activation remains blocked as current claim"),
        ("VAL2114_03_cmts_pack", cmts_ok, "C_MTS source pack retains axial anchor and total DeltaGamma missing inputs"),
        ("VAL2114_04_arenas", arena_ok, "arena impacts remain non-score-ready with WEP highlighted"),
        ("VAL2114_05_claim_gates", gates_ok, "audit is complete but LC/local-GR claims remain blocked"),
        ("VAL2114_06_decision", decision_ok, "decision selects spin guard or axial C_MTS/KRT map next"),
        ("VAL2114_07_next", next_ok, "next target is 2115 spin coframe-owned connection or axial C_MTS bound"),
        ("VAL2114_08_branch_copies", copies_ok, "branch copies exist and parse"),
        ("VAL2114_09_csv_parse", csv_ok, "all generated CSVs parse cleanly"),
        ("VAL2114_10_no_claim_flags", no_claims_ok, "no generated row allows a claim or score"),
        ("VAL2114_11_formalization_clean", formalization_ok, "formalization-workbench untouched by 2114"),
        ("VAL2114_12_no_pycache", no_pycache_ok, "scripts __pycache__ removed"),
    ]
    validation = [row(check_id=check_id, status="PASS" if passed else "FAIL", detail=detail) for check_id, passed, detail in checks]
    overall_ok = all(item["status"] == "PASS" for item in validation)
    validation.append(
        row(
            check_id="VAL2114_OVERALL",
            status="PASS" if overall_ok else "FAIL",
            detail="2114 audits every Gamma slot, blocks LC activation as current claim, retains C_MTS source pack, and selects spin guard/KRT map next.",
        )
    )
    return validation


def write_doc(
    sources: list[dict[str, object]],
    sectors: list[dict[str, object]],
    lc_rows: list[dict[str, object]],
    cmts_rows: list[dict[str, object]],
    arenas: list[dict[str, object]],
    claim_gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_target: list[dict[str, object]],
    copies: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    content = "\n".join(
        [
            "# 2114 - Y5/R2FR Sector Gamma-Slot Audit Or Affine CMTS Source Pack",
            "",
            "## Current Verdict",
            "",
            "2114 completes the sector Gamma-slot audit needed before the Levi-Civita branch can be activated. The result is clean but not claim-grade: the LC route remains mathematically preferred, but the parent action language has not signed every ordinary local sector as Gamma-free/coframe-owned.",
            "",
            "The failure is now precise. Ordinary matter is conditional, spin is the highest P4 risk, source/worldtube, clocks/rods/lightcones, orbital readout, boundary/non-Hilbert currents and projective trace remain unsigned. Therefore `K_conn=0` cannot be claimed yet.",
            "",
            "The honest fallback is explicit: retain `C_MTS = Gamma_MTS - LC[g_obs]`, keep `Delta_Gamma_abs` as a no-cancellation component sum, and attack the spin guard first because it has both a sharp theorem route and a real external torsion anchor.",
            "",
            "## Source Register",
            md_table(sources, ["source_id", "source_path", "path_exists", "needles_found", "role", "valid_for_claim"]),
            "## Sector Gamma-Slot Audit",
            md_table(sectors, ["audit_id", "sector", "current_status", "required_gamma_free_form", "evidence", "missing_for_lc_activation", "fallback_component", "valid_for_claim"]),
            "## LC Activation Gate",
            md_table(lc_rows, ["gate_id", "gate", "current_status", "requirement", "implication", "valid_for_claim"]),
            "## C_MTS Source Pack",
            md_table(cmts_rows, ["pack_id", "component", "current_status", "formula", "units", "needed_inputs", "observable_links", "valid_for_claim"]),
            "## Arena Impact",
            md_table(arenas, ["arena_id", "arena", "current_status", "components", "projection_matrix", "implication", "valid_for_claim"]),
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
    sectors = sector_audit_rows()
    lc_rows = lc_activation_rows()
    cmts_rows = cmts_source_pack_rows()
    arenas = arena_impact_rows()
    claim_gates = claim_gate_rows()
    decisions = decision_rows()
    next_target = next_target_rows()

    paths = {
        "sources": OUT / "P8_Y5_PARENT_QLOC_2114_SOURCE_REGISTER.csv",
        "sectors": OUT / "P8_Y5_PARENT_QLOC_2114_SECTOR_GAMMA_SLOT_AUDIT.csv",
        "lc": OUT / "P8_Y5_PARENT_QLOC_2114_LC_ACTIVATION_GATE.csv",
        "cmts": OUT / "P8_Y5_PARENT_QLOC_2114_CMTS_SOURCE_PACK.csv",
        "arenas": OUT / "P8_Y5_PARENT_QLOC_2114_ARENA_IMPACT.csv",
        "gates": OUT / "P8_Y5_PARENT_QLOC_2114_CLAIM_GATES.csv",
        "decisions": OUT / "P8_Y5_PARENT_QLOC_2114_DECISION_LEDGER.csv",
        "next": OUT / "P8_Y5_PARENT_QLOC_2114_NEXT_TARGET.csv",
        "branch": OUT / "P8_Y5_PARENT_QLOC_2114_BRANCH_COPIES.csv",
        "validation": OUT / "P8_Y5_BRR545_2114_VALIDATION.csv",
    }

    write_csv(paths["sources"], sources)
    write_csv(paths["sectors"], sectors)
    write_csv(paths["lc"], lc_rows)
    write_csv(paths["cmts"], cmts_rows)
    write_csv(paths["arenas"], arenas)
    write_csv(paths["gates"], claim_gates)
    write_csv(paths["decisions"], decisions)
    write_csv(paths["next"], next_target)

    copies = write_branch_copies(sectors, lc_rows, cmts_rows, arenas, next_target)
    write_csv(paths["branch"], copies)

    remove_pycache()

    csv_paths = [path for key, path in paths.items() if key != "validation"] + [Path(str(copy["destination"])) for copy in copies]
    validation = validation_rows(sources, sectors, lc_rows, cmts_rows, arenas, claim_gates, decisions, next_target, copies, csv_paths)
    write_csv(paths["validation"], validation)
    write_doc(sources, sectors, lc_rows, cmts_rows, arenas, claim_gates, decisions, next_target, copies, validation)

    print(f"wrote {DOC}")
    print(f"validation {paths['validation']}")


if __name__ == "__main__":
    main()
