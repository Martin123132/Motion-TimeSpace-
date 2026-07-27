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


DOC = ROOT / "2108-Y5-R2FR-field-by-field-vX-parent-action-signature-or-finite-tail-retention.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
SCRIPT_PATH = Path(__file__).resolve()

SRC_2107_DOC = ROOT / "2107-Y5-R2FR-consolidated-no-pole-source-zero-certificate-or-finite-residual-retention.md"
CSV_2107_CERT = OUT / "P8_Y5_PARENT_QLOC_2107_CONSOLIDATED_CERTIFICATE.csv"
CSV_2107_RESIDUALS = OUT / "P8_Y5_PARENT_QLOC_2107_FINITE_RESIDUAL_RETENTION.csv"
CSV_2107_NEXT = OUT / "P8_Y5_PARENT_QLOC_2107_NEXT_TARGET.csv"
CSV_2107_VAL = OUT / "P8_Y5_BRR545_2107_VALIDATION.csv"

SRC_590_DOC = ROOT / "590-Y5-R10-map-DCdagger-to-vertical-generator-or-fill-edge-row-source.md"
CSV_590_DCDAGGER = OUT / "P8_Y5_R10_590_DCDAGGER_VERTICAL_MAP.csv"
CSV_590_FIELDS = OUT / "P8_Y5_R10_590_FIELD_BY_FIELD_VERTICAL_ACTION_MAP.csv"
CSV_590_GATE = OUT / "P8_Y5_R10_590_MAPPING_CLOSURE_GATE.csv"

SRC_591_DOC = ROOT / "591-Y5-R10-parent-Omega-and-DC-operator-fill-or-edge-row-source-input.md"
CSV_591_OMEGA = OUT / "P8_Y5_R10_591_PARENT_OMEGA_CANDIDATE.csv"
CSV_591_DC = OUT / "P8_Y5_R10_591_DC_OPERATOR_FORMULA.csv"
CSV_591_ADJ = OUT / "P8_Y5_R10_591_DCDAGGER_FORMULA.csv"
CSV_591_COMP = OUT / "P8_Y5_R10_591_OMEGA_DCDAGGER_COMPARISON.csv"

SRC_582_DOC = ROOT / "582-Y5-R10-boundary-charge-and-constraint-algebra-no-pole-audit.md"
CSV_582_MOM = OUT / "P8_Y5_R10_582_MOMENTUM_MAP_CLOSURE_THEOREM.csv"
CSV_582_BDY = OUT / "P8_Y5_R10_582_BOUNDARY_DIFFERENTIABILITY_AUDIT.csv"
CSV_582_DIRAC = OUT / "P8_Y5_R10_582_DIRAC_BRACKET_AUDIT.csv"

SRC_583_DOC = ROOT / "583-Y5-R10-parent-momentum-map-owner-or-edge-residual-demotion.md"
CSV_583_OWNER = OUT / "P8_Y5_R10_583_PARENT_MOMENTUM_MAP_OWNER_ATTEMPT.csv"
CSV_583_NOETHER = OUT / "P8_Y5_R10_583_NOETHER_MOMENTUM_MAP_CONTRACT.csv"

SRC_1038_DOC = ROOT / "1038-Y5-R10-parent-Omega-DCX-vertical-generator-closure-or-beta-bound-acquisition.md"
CSV_1038_FIELDS = OUT / "P8_Y5_R10_1038_VERTICAL_GENERATOR_FIELD_MAP.csv"
CSV_1038_AUDIT = OUT / "P8_Y5_R10_1038_OMEGA_DCX_CLOSURE_AUDIT.csv"
CSV_1038_GATE = OUT / "P8_Y5_R10_1038_NO_POLE_CLAIM_GATE.csv"
CSV_1038_DEC = OUT / "P8_Y5_R10_1038_DECISION_LEDGER.csv"

SRC_1784_DOC = ROOT / "1784-Y5-R2FR-parent-Omega-DCX-vertical-action-packet-or-DqZ-geometry-row.md"
CSV_1784_PACKET = OUT / "P8_Y5_PARENT_QLOC_1784_OMEGA_DCX_VERTICAL_PACKET_GATE.csv"
CSV_1784_ACTION = OUT / "P8_Y5_PARENT_QLOC_1784_FIELD_ACTION_PACKET.csv"
CSV_1784_ALIGN = OUT / "P8_Y5_PARENT_QLOC_1784_OMEGA_DCX_ALIGNMENT_MATRIX.csv"


def row(**kwargs: object) -> dict[str, object]:
    data = base_row()
    data["claim_allowed"] = False
    data.update(kwargs)
    return data


def truthy(value: object) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"true", "1", "yes", "pass", "valid", "claim_allowed", "selected"}


def formalization_has_2108_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    patterns = (
        "*2108-Y5-R2FR*",
        "*P8_Y5_PARENT_QLOC_2108*",
        "*Y5_R2FR_field_by_field_vX_parent_action_signature_or_finite_tail_retention_2108*",
        "*AFRAME_VX_ACTION_SIGNATURE_2108*",
        "*JR2108_EXTRA_SECTOR*",
    )
    try:
        return any(path.is_file() for pattern in patterns for path in FORMALIZATION.rglob(pattern))
    except Exception:
        return False


def source_register_rows() -> list[dict[str, object]]:
    specs: list[tuple[str, Path, list[str], str]] = [
        (
            "SRC2108_00_2107_doc",
            SRC_2107_DOC,
            ["NEXT2107_0_2108", "FIELD_BY_FIELD_VX_PARENT_ACTION_SIGNATURE_FIRST", "VAL2107_OVERALL"],
            "2107 selects full field-by-field v_X parent action signature as the next hard blocker.",
        ),
        (
            "SRC2108_01_2107_cert",
            CSV_2107_CERT,
            ["CERT2107_1_vertical_generator", "MISSING_PARENT_SIGNATURE", "CERT2107_7_no_pole_source_zero"],
            "2107 certificate says the full no-pole/source-zero claim fails at parent v_X signature.",
        ),
        (
            "SRC2108_02_2107_residuals",
            CSV_2107_RESIDUALS,
            ["FRR2107_2_KX", "FRR2107_7_arena_response", "MISSING_ARENA_PROJECTION"],
            "2107 finite residual retention keeps K_X and local arena projections live.",
        ),
        (
            "SRC2108_03_2107_next",
            CSV_2107_NEXT,
            ["NEXT2107_0_2108", "field-by-field-vX-parent-action-signature", "finite tails"],
            "2107 next-target row points exactly at this checkpoint.",
        ),
        (
            "SRC2108_04_2107_validation",
            CSV_2107_VAL,
            ["VAL2107_OVERALL", "PASS", "field-by-field v_X/action signature next"],
            "2107 validation is clean and nonclaim.",
        ),
        (
            "SRC2108_05_590_doc",
            SRC_590_DOC,
            ["(DC_X)^dagger X", "Omega_Y^flat(v_X)", "vertical action on all parent fields"],
            "590 corrects the DCdagger slogan: it is the Omega-flat covector, not the generator itself.",
        ),
        (
            "SRC2108_06_590_dcdagger",
            CSV_590_DCDAGGER,
            ["DVM590_3_precise_map", "Omega_Y^flat", "not_available_until_reduced_Omega_is_explicit"],
            "590 DCdagger map supplies the exact covector-to-generator relation and its missing inverse.",
        ),
        (
            "SRC2108_07_590_fields",
            CSV_590_FIELDS,
            ["metric_or_coframe", "domain_memory_projector_fields", "unmapped"],
            "590 field map shows metric/coframe candidates but unmapped MTS extra fields.",
        ),
        (
            "SRC2108_08_590_gate",
            CSV_590_GATE,
            ["MCG590_2_vertical_generator", "MCG590_4_reduced_nondegeneracy", "true"],
            "590 closure gate names parent Omega, DC_X, v_X, boundary and degree blockers.",
        ),
        (
            "SRC2108_09_591_doc",
            SRC_591_DOC,
            ["same parent action still has to own `theta/Omega`", "Edge-source rows are still missing"],
            "591 writes formal Omega/DC operator pieces but not a parent-owned equality.",
        ),
        (
            "SRC2108_10_591_omega",
            CSV_591_OMEGA,
            ["OM591_0_covariant_variation_definition", "OM591_2_extra_sector", "not_constructed"],
            "591 Omega table provides formal covariant phase-space structure and missing extra-sector owner.",
        ),
        (
            "SRC2108_11_591_dc",
            CSV_591_DC,
            ["DC591_0_constraint_definition", "DC591_3_parent_field_expansion", "expansion_template_not_filled"],
            "591 DC operator formula requires P and J to be composites of explicit parent fields.",
        ),
        (
            "SRC2108_12_591_adjoint",
            CSV_591_ADJ,
            ["DCA591_4_compare_to_Omega_flat", "not_closed_without_parent_PJ_and_Omega"],
            "591 adjoint formula says the comparison is an equation for P, J, theta, Omega and v_X.",
        ),
        (
            "SRC2108_13_591_comparison",
            CSV_591_COMP,
            ["CMP591_5_verdict", "formula_progress_but_no_certificate"],
            "591 comparison explicitly refuses a certificate without same-parent P/J/Omega/boundary closure.",
        ),
        (
            "SRC2108_14_582_doc",
            SRC_582_DOC,
            ["equivariant parent momentum map", "K_boundary = 0", "no R10/local-GR claim"],
            "582 supplies the boundary and first-class algebra gate.",
        ),
        (
            "SRC2108_15_582_momentum",
            CSV_582_MOM,
            ["MMT582_0_constraint_generator", "MMT582_4_no_pole_result", "conditional_theorem_only"],
            "582 momentum-map theorem is exact conditional, not current proof.",
        ),
        (
            "SRC2108_16_582_boundary",
            CSV_582_BDY,
            ["BD582_0_bulk_variation", "BD582_5_verdict", "finite_or_edge_residual_branch"],
            "582 boundary audit keeps edge/fifth-force residuals live.",
        ),
        (
            "SRC2108_17_582_dirac",
            CSV_582_DIRAC,
            ["DA582_4_bracket_closure", "DA582_5_degree_count", "blocked_current_claim"],
            "582 Dirac audit blocks no-pole without bracket and degree-count proof.",
        ),
        (
            "SRC2108_18_583_doc",
            SRC_583_DOC,
            ["parent symplectic potential, vertical generator", "edge-hair fallback"],
            "583 tries the parent momentum-map owner and demotes to edge residual if it fails.",
        ),
        (
            "SRC2108_19_583_owner",
            CSV_583_OWNER,
            ["OMA583_1_noether_current_owner", "OMA583_5_verdict", "owner_not_derived_edge_template_required"],
            "583 owner attempt says Noether/momentum-map owner is not derived.",
        ),
        (
            "SRC2108_20_583_noether",
            CSV_583_NOETHER,
            ["NMC583_1_vertical_generator", "NMC583_5_boundary_zero", "not_derived"],
            "583 Noether contract keeps vertical generator and boundary zero missing.",
        ),
        (
            "SRC2108_21_1038_doc",
            SRC_1038_DOC,
            ["right target objects", "all-field `v_X`", "no physical `X` pole"],
            "1038 independently records the Omega/DCX/v_X obstruction.",
        ),
        (
            "SRC2108_22_1038_fields",
            CSV_1038_FIELDS,
            ["domain_memory_projector_fields", "UNMAPPED", "boundary_edge_modes"],
            "1038 field map repeats the extra-sector and boundary action gaps.",
        ),
        (
            "SRC2108_23_1038_audit",
            CSV_1038_AUDIT,
            ["ODC1038_3_vertical_generator_fields", "FIELD_MAP_INCOMPLETE", "ODC1038_8_verdict"],
            "1038 closure audit says no-pole does not close without all-field v_X.",
        ),
        (
            "SRC2108_24_1038_gate",
            CSV_1038_GATE,
            ["NPG1038_0_exact_no_pole", "FIELD_MAP_INCOMPLETE", "MISSING_DEGREE_COUNT"],
            "1038 claim gate blocks exact no-pole from the same missing objects.",
        ),
        (
            "SRC2108_25_1038_decision",
            CSV_1038_DEC,
            ["DEC1038_0_derivation_status", "DEC1038_3_next_target"],
            "1038 decision keeps derivation open but routes boundary/beta if closure fails.",
        ),
        (
            "SRC2108_26_1784_doc",
            SRC_1784_DOC,
            ["Current MTS still does not supply", "field-by-field `v_X`", "no-pole/local-GR/Newton"],
            "1784 is the closest active-branch Omega/DCX/v_X packet verdict.",
        ),
        (
            "SRC2108_27_1784_packet",
            CSV_1784_PACKET,
            ["ODP1784_4_field_action", "FIELD_MAP_INCOMPLETE", "ODP1784_8_verdict"],
            "1784 packet gate blocks the parent Omega/DCX/v_X packet.",
        ),
        (
            "SRC2108_28_1784_action",
            CSV_1784_ACTION,
            ["FAP1784_3_domain_memory_projector", "UNMAPPED", "FAP1784_5_boundary_edge_modes"],
            "1784 field-action packet identifies the unmapped non-GR field blocks.",
        ),
        (
            "SRC2108_29_1784_align",
            CSV_1784_ALIGN,
            ["ALN1784_2_raise_to_vector", "REDUCED_OMEGA_INVERSE_MISSING", "ALN1784_5_verdict"],
            "1784 alignment matrix keeps DCdagger-to-v_X non-executable without reduced Omega.",
        ),
    ]
    rows: list[dict[str, object]] = []
    for source_id, path, needles, use in specs:
        exists = path.exists()
        text = read_text(path) if exists else ""
        rows.append(
            row(
                source_id=source_id,
                source_kind="2108_vX_parent_action_signature",
                source_path=str(path),
                path_exists=exists,
                needles="; ".join(needles),
                needle_found=exists and all(needle in text for needle in needles),
                use_in_2108=use,
                valid_for_claim=False,
            )
        )
    return rows


def vx_signature_rows() -> list[dict[str, object]]:
    specs = [
        (
            "VXS2108_0_metric_coframe",
            "metric_or_coframe",
            "v_epsilon[g]=L_epsilon g or v_epsilon[e]=L_epsilon e plus local Lorentz compensation",
            "STANDARD_NATURAL_LIFT_CANDIDATE",
            "GR-style diffeomorphism/natural-bundle action is mathematically sharp for geometry.",
            "observed metric/coframe parent ownership and parent theta/Omega still required",
        ),
        (
            "VXS2108_1_canonical_momenta",
            "canonical_momenta_or_boundary_charge",
            "v_epsilon[pi]=L_epsilon pi plus density and boundary improvement terms",
            "NOT_WRITTEN_FOR_MTS",
            "canonical lift must match the same theta/Omega used by DCdagger.",
            "canonical variables or covariant phase-space charge split",
        ),
        (
            "VXS2108_2_Gamma_Khat_qloc",
            "Gamma_Khat_qloc_sector",
            "v_epsilon[T_GK]=L_epsilon T_GK if Gamma/Khat/q_loc package is a parent natural tensor/stress sector",
            "CONDITIONAL_NOT_INTEGRATED_WITH_DCX",
            "this is the possible leap forward: make the extra sector natural rather than scalar-fitted.",
            "parent S_GK, Helmholtz/integrability and DC_X owner",
        ),
        (
            "VXS2108_3_domain_memory_projector",
            "domain_memory_projector_fields",
            "v_epsilon[Phi^A]=L_epsilon Phi^A or a quotient-vertical representative shift for chi_D, Q_coh, memory, Pi_M and boundary variables",
            "UNMAPPED",
            "without this block, source/projector terms can carry the local residual.",
            "transformation law for domain, memory, projector and support fields",
        ),
        (
            "VXS2108_4_matter_readout_constants",
            "matter_readout_constants",
            "v_epsilon[psi]=0 or ordinary gauge lift and v_epsilon[theta_A]=0 only after matter/readout descent",
            "NOT_DERIVED",
            "matter zero lemmas are exact but depend on parent interface selection.",
            "matter functor descent, no-marker theorem and no hidden source/readout frame",
        ),
        (
            "VXS2108_5_boundary_edge_modes",
            "boundary_edge_modes",
            "proper compact transformation or exact boundary representative shift with Q_X=0/proper/exact and K_boundary=0",
            "NOT_DERIVED",
            "edge hair can become the whole local fifth-force channel.",
            "boundary differentiability, projector orthogonality and cocycle computation",
        ),
        (
            "VXS2108_6_DCadjoint_raise",
            "DCdagger to v_X",
            "v_X=Omega_Y^{-1}[(D C_X)^dagger epsilon] only on the reduced nondegenerate phase space",
            "REDUCED_OMEGA_INVERSE_MISSING",
            "DCdagger is a covector until the parent symplectic inverse is owned.",
            "theta/Omega, DC_X, boundary domain and no-stabilizer proof",
        ),
        (
            "VXS2108_7_verdict",
            "field-by-field v_X parent signature",
            "VXS2108_0 through VXS2108_6 all close in one parent branch",
            "FAIL_CURRENT_CLAIM",
            "geometry has a strong standard candidate; the extra, matter/readout, boundary and reduced-Omega blocks do not close.",
            "single same-branch field map plus parent action and boundary prescription",
        ),
    ]
    return [
        row(
            signature_id=signature_id,
            field_block=field_block,
            candidate_action=candidate_action,
            current_status=current_status,
            meaning=meaning,
            missing_for_claim=missing_for_claim,
            valid_for_claim=False,
        )
        for signature_id, field_block, candidate_action, current_status, meaning, missing_for_claim in specs
    ]


def natural_lift_test_rows() -> list[dict[str, object]]:
    specs = [
        (
            "NLT2108_0_best_route",
            "proper natural-bundle/diffeomorphism lift",
            "Treat v_X not as a new scalar switch, but as a proper representative lift acting naturally on every parent field before readout.",
            "LEAST_SCRUTINY_ROUTE",
            "If true, EH/ordinary covariance, Bianchi/Noether identity and local GR compatibility are structurally aligned.",
            "must prove every MTS extra field is a natural object and boundary-proper",
        ),
        (
            "NLT2108_1_EH_geometry",
            "EH/metric core",
            "delta_{L_epsilon} L_EH=d mu_EH on shell, with Hamiltonian constraints and proper boundary conditions.",
            "STANDARD_GR_ANCHOR_CONDITIONAL_PASS",
            "This is the GR analogue MTS should reduce to.",
            "does not cover MTS extra fields or source/readout markers",
        ),
        (
            "NLT2108_2_extra_sector",
            "Gamma/Khat/q_loc/memory/projector",
            "Each extra object must be a natural tensor, density, connection object, quotient object, or explicitly proper-gauge representative.",
            "MISSING_NATURAL_BUNDLE_SIGNATURE",
            "This is the first real missing leap after 2108.",
            "field transformation law and covariant Lagrangian for each extra block",
        ),
        (
            "NLT2108_3_matter_interface",
            "ordinary matter/readout",
            "Matter must see the descended public metric/coframe and quotient-owned constants, not an independent X frame.",
            "EXACT_CONDITIONAL_NOT_PARENT_SIGNED",
            "This would convert the qbar zero lemmas into a parent theorem.",
            "single-public-metric/no-marker parent action clause",
        ),
        (
            "NLT2108_4_boundary_properness",
            "local compact boundary",
            "Allowed vertical transformations are proper at local boundary or have exact/pure-gauge charge with Pi_M^H Q_X=0.",
            "MISSING_QX_KBOUNDARY_ZERO",
            "This prevents edge hair from becoming the fifth-force source.",
            "Q_X, K_boundary and measured-Hamiltonian projection computation",
        ),
        (
            "NLT2108_5_degree_count",
            "reduced phase-space proof",
            "The natural lift is first-class and removes the X pair without leaving a proper stabilizer.",
            "MISSING_FIRST_CLASS_COUNT",
            "This distinguishes gauge from under-specified dynamics.",
            "bracket closure, rank count and reduced nondegeneracy",
        ),
        (
            "NLT2108_6_verdict",
            "natural lift proof for local GR branch",
            "NLT2108_1 through NLT2108_5 close on the same branch.",
            "NATURAL_LIFT_NOT_PARENT_SIGNED",
            "The route is promising and less post-hoc than finite tuning, but not yet a claim.",
            "extra-sector naturality before boundary/degree can be computed cleanly",
        ),
    ]
    return [
        row(
            test_id=test_id,
            route=route,
            statement=statement,
            current_status=current_status,
            consequence_if_true=consequence_if_true,
            missing_for_claim=missing_for_claim,
            valid_for_claim=False,
        )
        for test_id, route, statement, current_status, consequence_if_true, missing_for_claim in specs
    ]


def action_variation_rows() -> list[dict[str, object]]:
    specs = [
        (
            "AVT2108_0_parent_variation_contract",
            "total parent first variation",
            "delta L_parent=E_A delta Y^A+d theta_Y(delta Y)",
            "FORMAL_CONTRACT_ONLY",
            "needed before any v_X action can be checked",
            "one L_parent and theta_Y across all retained sectors",
        ),
        (
            "AVT2108_1_EH_sector",
            "EH/GR geometric sector",
            "delta_{v_X} L_EH=d mu_EH when v_X is a proper diffeomorphism/natural lift",
            "STANDARD_ANCHOR_NOT_TOTAL_MTS",
            "useful anchor for GR reduction",
            "does not sign Gamma/Khat/memory/projector/matter/boundary sectors",
        ),
        (
            "AVT2108_2_GK_sector",
            "Gamma/Khat/q_loc sector",
            "delta_{v_X} L_GK=E_GK v_X[T_GK]+d theta_GK(v_X) must be a Ward identity or quotient-silent",
            "NOT_DERIVED",
            "this block decides whether q_loc is geometric or finite source-bearing",
            "S_GK, integrability and current owner",
        ),
        (
            "AVT2108_3_memory_projector",
            "domain/memory/projector sector",
            "delta_{v_X} L_mem/proj must be natural, exact, or quotient-vertical with no source support shift",
            "UNMAPPED",
            "memory/projector tails can reopen local tests even if EH/matter are clean",
            "chi_D, Q_coh, Pi_M, support and domain field actions",
        ),
        (
            "AVT2108_4_matter",
            "ordinary matter/readout",
            "delta_{v_X} S_matter=0 follows only from quotient-owned public coframe plus no-marker constants",
            "EXACT_CONDITIONAL_NOT_SIGNED",
            "would kill qbar_XT for ordinary matter",
            "parent matter functor/no-shadow clause",
        ),
        (
            "AVT2108_5_boundary",
            "boundary/reference/local mass projection",
            "delta G_X has no uncancelled boundary covector and Q_X/K_boundary/Pi_M^H channels vanish",
            "OPEN",
            "otherwise the local residual moves to Qbar_XH or edge beta",
            "B_X primitive, Q_X, K_boundary and projector orthogonality",
        ),
        (
            "AVT2108_6_total_verdict",
            "total action invariance/descent",
            "AVT2108_1 through AVT2108_5 close from the same parent action",
            "FAIL_CURRENT_CLAIM",
            "no-pole/local-GR promotion remains blocked",
            "extra-sector field action plus boundary/degree proof",
        ),
    ]
    return [
        row(
            variation_id=variation_id,
            sector=sector,
            required_variation=required_variation,
            current_status=current_status,
            consequence=consequence,
            missing_for_claim=missing_for_claim,
            valid_for_claim=False,
        )
        for variation_id, sector, required_variation, current_status, consequence, missing_for_claim in specs
    ]


def omega_execution_rows() -> list[dict[str, object]]:
    specs = [
        ("OEX2108_0_parent_field_list", "Y=(e/g, pi, X/Z/R_AB, Gamma/Khat/q_loc, memory/domain/projector, matter/readout, boundary)", "PARENT_VARIABLE_SET_INCOMPLETE", "cannot define one theta/Omega or one v_X domain"),
        ("OEX2108_1_theta_omega", "theta_Y and Omega_Y for all parent and boundary fields", "MISSING_PARENT_OMEGA", "DCdagger remains pairing-dependent bookkeeping"),
        ("OEX2108_2_DCX", "parent-owned D C_X from C_X=-nabla P+J_eff", "MISSING_DCX_OPERATOR", "adjoint cannot be compared to Omega-flat generator"),
        ("OEX2108_3_omega_flat_equality", "(D C_X)^dagger epsilon = Omega_Y^flat(v_epsilon)", "NOT_EXECUTABLE", "formal map cannot be checked field-by-field"),
        ("OEX2108_4_reduced_inverse", "v_epsilon=Omega_Y^{-1}[(D C_X)^dagger epsilon]", "REDUCED_OMEGA_INVERSE_MISSING", "cannot raise the covector to the actual generator"),
        ("OEX2108_5_boundary_domain", "delta Q_X cancels boundary variation and Q_X/K_boundary vanish or are proper", "MISSING_BOUNDARY_CHARGE_ZERO", "edge channel remains physical"),
        ("OEX2108_6_degree_no_stabilizer", "first-class bracket removes X pair and reduced Omega has no proper X stabilizer", "MISSING_DEGREE_COUNT", "rank-zero may be under-specified dynamics"),
        ("OEX2108_7_verdict", "Omega/DCX execution of v_X map", "FAIL_CURRENT_CLAIM", "no executable parent generator certificate yet"),
    ]
    return [
        row(
            execution_id=execution_id,
            required_object=required_object,
            current_status=current_status,
            if_missing=if_missing,
            valid_for_claim=False,
        )
        for execution_id, required_object, current_status, if_missing in specs
    ]


def finite_tail_retention_rows() -> list[dict[str, object]]:
    specs = [
        ("FTR2108_0_DqZ_geom", "Dq_Z[e_obs,g_obs]", "finite observed-geometry leak if extra-sector naturality fails", "RETAIN_NONCLAIM", "1784/2025"),
        ("FTR2108_1_GK_tail", "Gamma/Khat/q_loc residual", "finite source/current tail if GK sector is not a natural parent tensor", "RETAIN_NONCLAIM", "1784/2107"),
        ("FTR2108_2_memory_projector", "chi_D,Q_coh,Pi_M/support/domain tail", "finite projector/source-support residual if field action is unmapped", "RETAIN_NONCLAIM", "1784/1849"),
        ("FTR2108_3_edge", "Q_X,K_boundary,Qbar_XH", "edge hair or measured-Hamiltonian source if boundary silence fails", "RETAIN_NONCLAIM", "582/583"),
        ("FTR2108_4_matter_marker", "qbar_XT,b_alpha,b_m,b_clock", "matter/readout/constant leakage if no-marker theorem remains unsigned", "RETAIN_NONCLAIM", "1044/1046/2107"),
        ("FTR2108_5_beta_source_test", "beta_s,beta_t,alpha_X(lambda)", "finite source-test product branch if no-pole proof fails", "RETAIN_NONCLAIM", "1037/1038"),
        ("FTR2108_6_ZX_MX2", "Z_X,M_X^2,lambda_X", "finite propagator branch if X is physical rather than gauge", "RETAIN_NONCLAIM", "2105/2106/2107"),
        ("FTR2108_7_arena_projection", "tau_R10,tau_PPN,tau_clock,tau_orbital", "needed before any empirical local test score", "MISSING_ARENA_PROJECTION", "2107"),
    ]
    return [
        row(
            tail_id=tail_id,
            retained_tail=retained_tail,
            meaning=meaning,
            current_status=current_status,
            source_family=source_family,
            valid_for_claim=False,
        )
        for tail_id, retained_tail, meaning, current_status, source_family in specs
    ]


def gate_rows() -> list[dict[str, object]]:
    specs = [
        ("GATE2108_0_metric_candidate", "metric/coframe natural lift candidate exists", True, "standard GR-style Lie derivative candidate is mathematically sharp"),
        ("GATE2108_1_all_field_vX", "v_X specified on every retained field block", False, "Gamma/Khat/q_loc and domain/memory/projector blocks are not parent-signed"),
        ("GATE2108_2_parent_action_invariance", "total parent action invariant/descended under v_X", False, "non-EH sectors and boundary terms are not varied from one parent action"),
        ("GATE2108_3_DCadjoint_execution", "DCdagger covector raised to actual generator", False, "Omega_Y and reduced inverse are missing"),
        ("GATE2108_4_boundary_degree", "boundary charge/cocycle and degree count close", False, "Q_X, K_boundary, bracket and rank count are not computed"),
        ("GATE2108_5_no_pole_source_zero", "K_X=qbar_XT=Qbar_XH=0 follows", False, "full parent generator/action certificate fails current claim"),
        ("GATE2108_6_finite_tails_retained", "finite tail branch retained without claims", True, "all live tails are kept as nonclaim acquisition rows"),
        ("GATE2108_7_local_GR_Newton", "derived local GR/Newton limit follows", False, "field-by-field v_X/action signature is not closed"),
    ]
    return [
        row(
            gate_id=gate_id,
            gate=gate,
            gate_pass=gate_pass,
            reason=reason,
            claim_allowed=False,
            valid_for_claim=False,
        )
        for gate_id, gate, gate_pass, reason in specs
    ]


def decision_rows() -> list[dict[str, object]]:
    specs = [
        (
            "DEC2108_0_result",
            "FIELD_BY_FIELD_VX_SIGNATURE_NOT_CLOSED",
            "The geometry block has the right GR-like candidate, but the active MTS extra, projector, matter/readout and boundary blocks are not parent-signed.",
            "no local-GR/no-pole claim from 2108",
        ),
        (
            "DEC2108_1_best_route",
            "NATURAL_BUNDLE_LIFT_REMAINS_BEST_DERIVATION_ROUTE",
            "Identifying the vertical branch with a proper natural-bundle/diffeomorphism lift is less post-hoc than finite tuning and lines up with GR reduction logic.",
            "try to sign the non-GR extra-sector lift before computing boundary/degree closure",
        ),
        (
            "DEC2108_2_next",
            "EXTRA_SECTOR_NATURALITY_FIRST",
            "Boundary and degree calculations need the field action; the first missing field-action blocks are Gamma/Khat/q_loc and domain/memory/projector.",
            "construct or reject natural-bundle lift for extra sectors, else keep finite DqZ/GK/projector tail rows",
        ),
        (
            "DEC2108_3_fallback_policy",
            "FINITE_TAILS_RETAINED_NO_CANCELLATION",
            "If extra-sector naturality fails, the branch becomes a finite residual source problem with absolute-sum/no-cancellation rules.",
            "retain DqZ, GK, projector, edge, qbar, beta, Z_X/M_X^2 and arena projection rows",
        ),
    ]
    return [
        row(
            decision_id=decision_id,
            decision=decision,
            because=because,
            next_action=next_action,
            valid_for_claim=False,
        )
        for decision_id, decision, because, next_action in specs
    ]


def next_rows() -> list[dict[str, object]]:
    return [
        row(
            route_id="NEXT2108_0_2109",
            next_target="2109-Y5-R2FR-extra-sector-natural-bundle-lift-or-finite-DqZ-tail-row.md",
            script="scripts/Y5_R2FR_extra_sector_natural_bundle_lift_or_finite_DqZ_tail_row_2109.py",
            objective="Try to prove the MTS extra sectors Gamma/Khat/q_loc plus domain/memory/projector fields are natural parent-bundle objects under the same proper v_X lift as the metric/coframe; if this fails, retain finite DqZ/GK/projector tail rows with source paths and no-cancellation rules.",
            forbidden_shortcuts="metric-only diffeo proof; treating readout/projector variables as afterthoughts; boundary computation before field action is known; invented q_loc silence; local-GR claim; cancellation among finite tails; formalization-workbench edits; GitHub action",
            valid_for_claim=False,
        )
    ]


def write_branch_copies(
    signatures: list[dict[str, object]],
    natural_lift: list[dict[str, object]],
    action_variation: list[dict[str, object]],
    omega_execution: list[dict[str, object]],
    tails: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_target: list[dict[str, object]],
) -> list[dict[str, object]]:
    copies = [
        (
            "COPY2108_0_source_weight_docs",
            SOURCE_WEIGHT_DOCS / "AFRAME_VX_ACTION_SIGNATURE_2108_NONCLAIM.csv",
            signatures + natural_lift + action_variation + decisions,
        ),
        (
            "COPY2108_1_branch_locked_wep",
            BRANCH_WEP / "P8_Y5_PARENT_QLOC_2108_VX_ACTION_STATUS_NONCLAIM.csv",
            signatures + omega_execution + tails,
        ),
        (
            "COPY2108_2_acquisition_queue",
            QUEUE / "JR2108_EXTRA_SECTOR_NATURALITY_OR_FINITE_TAIL_QUEUE.csv",
            tails + next_target,
        ),
    ]
    rows: list[dict[str, object]] = []
    for copy_id, path, copy_rows in copies:
        write_csv(path, copy_rows)
        rows.append(
            row(
                copy_id=copy_id,
                destination=str(path),
                path_exists=path.exists(),
                row_count=len(copy_rows),
                parse_ok=csv_rows_parse(path),
                valid_for_claim=False,
            )
        )
    return rows


def validation_rows(
    sources: list[dict[str, object]],
    signatures: list[dict[str, object]],
    natural_lift: list[dict[str, object]],
    action_variation: list[dict[str, object]],
    omega_execution: list[dict[str, object]],
    tails: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_target: list[dict[str, object]],
    copies: list[dict[str, object]],
    csv_paths: list[Path],
) -> list[dict[str, object]]:
    sources_ok = all(truthy(source.get("path_exists")) and truthy(source.get("needle_found")) for source in sources)
    signature_ok = (
        len(signatures) == 8
        and any(row_.get("signature_id") == "VXS2108_7_verdict" and row_.get("current_status") == "FAIL_CURRENT_CLAIM" for row_ in signatures)
        and any(row_.get("signature_id") == "VXS2108_3_domain_memory_projector" and row_.get("current_status") == "UNMAPPED" for row_ in signatures)
    )
    natural_ok = any(row_.get("test_id") == "NLT2108_6_verdict" and row_.get("current_status") == "NATURAL_LIFT_NOT_PARENT_SIGNED" for row_ in natural_lift)
    action_ok = any(row_.get("variation_id") == "AVT2108_6_total_verdict" and row_.get("current_status") == "FAIL_CURRENT_CLAIM" for row_ in action_variation)
    omega_ok = any(row_.get("execution_id") == "OEX2108_7_verdict" and row_.get("current_status") == "FAIL_CURRENT_CLAIM" for row_ in omega_execution)
    tails_ok = len(tails) >= 8 and all(not truthy(row_.get("valid_for_claim")) for row_ in tails)
    gates_ok = (
        all(not truthy(row_.get("claim_allowed")) for row_ in gates)
        and any(row_.get("gate_id") == "GATE2108_7_local_GR_Newton" and not truthy(row_.get("gate_pass")) for row_ in gates)
        and any(row_.get("gate_id") == "GATE2108_6_finite_tails_retained" and truthy(row_.get("gate_pass")) for row_ in gates)
    )
    decision_ok = any(row_.get("decision") == "EXTRA_SECTOR_NATURALITY_FIRST" for row_ in decisions)
    next_ok = any(row_.get("route_id") == "NEXT2108_0_2109" and "extra-sector-natural-bundle-lift" in str(row_.get("next_target")) for row_ in next_target)
    copies_ok = len(copies) == 3 and all(truthy(row_.get("path_exists")) and truthy(row_.get("parse_ok")) for row_ in copies)
    csv_ok = all(path.exists() and csv_rows_parse(path) for path in csv_paths)
    no_claims = all(
        not truthy(row_.get("valid_for_claim")) and not truthy(row_.get("claim_allowed")) and not truthy(row_.get("score_ready"))
        for collection in (sources, signatures, natural_lift, action_variation, omega_execution, tails, gates, decisions, next_target, copies)
        for row_ in collection
    )
    formalization_clean = count_formalization_modified() == 0 and not formalization_has_2108_artifacts()
    no_pycache = not (SCRIPT_PATH.parent / "__pycache__").exists()
    checks = [
        ("VAL2108_00_sources", sources_ok, "all cited source paths exist and contain expected v_X/Omega/DCX needles"),
        ("VAL2108_01_signature", signature_ok, "field-by-field v_X signature is complete and fails current claim at non-GR blocks"),
        ("VAL2108_02_natural_lift", natural_ok, "natural-bundle lift is selected as best derivation route but not parent-signed"),
        ("VAL2108_03_action_variation", action_ok, "total action variation/descent fails current claim"),
        ("VAL2108_04_omega_execution", omega_ok, "DCdagger-to-v_X execution remains blocked without Omega/DCX/reduced inverse"),
        ("VAL2108_05_tail_retention", tails_ok, "finite tails are retained explicitly and nonclaim"),
        ("VAL2108_06_claim_gates", gates_ok, "local-GR/Newton gate remains blocked while finite-tail retention policy passes"),
        ("VAL2108_07_decision", decision_ok, "decision selects extra-sector naturality before boundary/degree closure"),
        ("VAL2108_08_next", next_ok, "next target is 2109 extra-sector natural-bundle lift or finite DqZ tail row"),
        ("VAL2108_09_branch_copies", copies_ok, "branch copies exist and parse"),
        ("VAL2108_10_csv_parse", csv_ok, "all generated CSVs parse cleanly"),
        ("VAL2108_11_no_claim_flags", no_claims, "no generated row allows a claim or score"),
        ("VAL2108_12_formalization_clean", formalization_clean, "formalization-workbench untouched by 2108"),
        ("VAL2108_13_no_pycache", no_pycache, "scripts __pycache__ removed"),
    ]
    overall = all(ok for _, ok, _ in checks)
    checks.append(
        (
            "VAL2108_OVERALL",
            overall,
            "2108 tests the field-by-field v_X/action signature, rejects current local-GR promotion, and selects extra-sector natural-bundle lift next",
        )
    )
    return [
        row(
            check_id=check_id,
            status="PASS" if ok else "FAIL",
            detail=detail,
            claim_allowed=False,
            valid_for_claim=False,
        )
        for check_id, ok, detail in checks
    ]


def write_doc(
    sources: list[dict[str, object]],
    signatures: list[dict[str, object]],
    natural_lift: list[dict[str, object]],
    action_variation: list[dict[str, object]],
    omega_execution: list[dict[str, object]],
    tails: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_target: list[dict[str, object]],
    copies: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    sections = [
        "# 2108 - Y5/R2FR Field-by-Field vX Parent Action Signature Or Finite Tail Retention",
        "",
        "## Current Verdict",
        "",
        "2108 takes the cleanest possible leap at the local-GR problem: make `v_X` a proper natural-bundle/diffeomorphism-style lift rather than an inserted scalar switch. The metric/coframe block has a strong GR-like candidate, `v_X[g]=L_epsilon g` or `v_X[e]=L_epsilon e` plus local Lorentz compensation.",
        "",
        "That does not close the MTS branch. The active corpus still lacks parent-signed field actions for `Gamma/Khat/q_loc`, domain/memory/projector variables, matter/readout/constants, and boundary/edge modes. `DCdagger` remains an `Omega`-flat covector until the parent `Omega_Y`, `D C_X`, reduced inverse, boundary prescription, and degree count are owned.",
        "",
        "So the result is progress but not promotion: the best derivation route is now extra-sector naturality. If the non-GR sectors are natural parent-bundle objects under the same proper lift, the boundary/degree proof becomes meaningful. If not, the finite `Dq_Z`, GK, projector, edge, qbar, beta, and arena-projection tails stay live.",
        "",
        "## Source Register",
        md_table(sources, ["source_id", "source_path", "path_exists", "needle_found", "use_in_2108", "valid_for_claim"]),
        "## vX Field Signature",
        md_table(signatures, ["signature_id", "field_block", "current_status", "candidate_action", "meaning", "missing_for_claim", "valid_for_claim"]),
        "## Natural-Lift Test",
        md_table(natural_lift, ["test_id", "route", "current_status", "statement", "consequence_if_true", "missing_for_claim", "valid_for_claim"]),
        "## Action Variation Test",
        md_table(action_variation, ["variation_id", "sector", "current_status", "required_variation", "consequence", "missing_for_claim", "valid_for_claim"]),
        "## Omega/DCX Execution Gate",
        md_table(omega_execution, ["execution_id", "required_object", "current_status", "if_missing", "valid_for_claim"]),
        "## Finite Tail Retention",
        md_table(tails, ["tail_id", "retained_tail", "current_status", "meaning", "source_family", "valid_for_claim"]),
        "## Claim Gates",
        md_table(gates, ["gate_id", "gate", "gate_pass", "reason", "claim_allowed", "valid_for_claim"]),
        "## Decision Ledger",
        md_table(decisions, ["decision_id", "decision", "because", "next_action", "valid_for_claim"]),
        "## Next Target",
        md_table(next_target, ["route_id", "next_target", "script", "objective", "forbidden_shortcuts", "valid_for_claim"]),
        "## Branch Copies",
        md_table(copies, ["copy_id", "destination", "path_exists", "row_count", "parse_ok", "valid_for_claim"]),
        "## Validation",
        md_table(validation, ["check_id", "status", "detail", "claim_allowed", "valid_for_claim"]),
    ]
    DOC.write_text("\n".join(sections), encoding="utf-8")


def main() -> None:
    sources = source_register_rows()
    signatures = vx_signature_rows()
    natural_lift = natural_lift_test_rows()
    action_variation = action_variation_rows()
    omega_execution = omega_execution_rows()
    tails = finite_tail_retention_rows()
    gates = gate_rows()
    decisions = decision_rows()
    next_target = next_rows()
    paths = {
        "sources": OUT / "P8_Y5_PARENT_QLOC_2108_SOURCE_REGISTER.csv",
        "signatures": OUT / "P8_Y5_PARENT_QLOC_2108_VX_FIELD_ACTION_SIGNATURE.csv",
        "natural_lift": OUT / "P8_Y5_PARENT_QLOC_2108_NATURAL_LIFT_TEST.csv",
        "action_variation": OUT / "P8_Y5_PARENT_QLOC_2108_ACTION_VARIATION_TEST.csv",
        "omega_execution": OUT / "P8_Y5_PARENT_QLOC_2108_OMEGA_DCX_EXECUTION_GATE.csv",
        "tails": OUT / "P8_Y5_PARENT_QLOC_2108_FINITE_TAIL_RETENTION.csv",
        "gates": OUT / "P8_Y5_PARENT_QLOC_2108_CLAIM_GATES.csv",
        "decisions": OUT / "P8_Y5_PARENT_QLOC_2108_DECISION_LEDGER.csv",
        "next": OUT / "P8_Y5_PARENT_QLOC_2108_NEXT_TARGET.csv",
        "branch": OUT / "P8_Y5_PARENT_QLOC_2108_BRANCH_COPIES.csv",
        "validation": OUT / "P8_Y5_BRR545_2108_VALIDATION.csv",
    }
    write_csv(paths["sources"], sources)
    write_csv(paths["signatures"], signatures)
    write_csv(paths["natural_lift"], natural_lift)
    write_csv(paths["action_variation"], action_variation)
    write_csv(paths["omega_execution"], omega_execution)
    write_csv(paths["tails"], tails)
    write_csv(paths["gates"], gates)
    write_csv(paths["decisions"], decisions)
    write_csv(paths["next"], next_target)
    copies = write_branch_copies(signatures, natural_lift, action_variation, omega_execution, tails, decisions, next_target)
    write_csv(paths["branch"], copies)
    csv_paths = [path for key, path in paths.items() if key != "validation"] + [Path(str(r["destination"])) for r in copies]
    remove_pycache()
    validation = validation_rows(sources, signatures, natural_lift, action_variation, omega_execution, tails, gates, decisions, next_target, copies, csv_paths)
    write_csv(paths["validation"], validation)
    write_doc(sources, signatures, natural_lift, action_variation, omega_execution, tails, gates, decisions, next_target, copies, validation)
    remove_pycache()
    print(f"wrote {DOC}")
    print(f"validation {paths['validation']}")


if __name__ == "__main__":
    main()
