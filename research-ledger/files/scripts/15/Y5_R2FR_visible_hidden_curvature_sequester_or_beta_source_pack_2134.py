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


DOC = ROOT / "2134-Y5-R2FR-visible-hidden-curvature-sequester-or-beta-source-pack.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"

CSV_2133_NEXT = OUT / "P8_Y5_PARENT_QLOC_2133_NEXT_TARGET.csv"
CSV_2133_VAL = OUT / "P8_Y5_BRR545_2133_VALIDATION.csv"
CSV_2133_BETA_ATTEMPT = OUT / "P8_Y5_PARENT_QLOC_2133_BETA_ZERO_ATTEMPT.csv"
CSV_2133_BETA_SOURCE = OUT / "P8_Y5_PARENT_QLOC_2133_BETA_SOURCE_ROW.csv"
DOC_2133 = ROOT / "2133-Y5-R2FR-aux-curvature-coupling-beta-zero-or-source-row.md"
CSV_1049_DEC = OUT / "P8_Y5_R10_1049_DECISION_LEDGER.csv"
CSV_1050_THEOREM = OUT / "P8_Y5_R10_1050_PRODUCT_FUNCTOR_THEOREM_ATTEMPT.csv"
CSV_1050_OBS = OUT / "P8_Y5_R10_1050_PRODUCT_FUNCTOR_OBSTRUCTION_LEDGER.csv"
CSV_1050_GATES = OUT / "P8_Y5_R10_1050_CLAIM_GATES.csv"
DOC_1050 = ROOT / "1050-Y5-R10-visible-hidden-product-functor-derivation-or-prior-width-source-pack.md"
CSV_1051_NMM = OUT / "P8_Y5_R10_1051_NO_MIXED_MORPHISM_LEMMA_ATTEMPT.csv"
CSV_1051_ISO = OUT / "P8_Y5_R10_1051_INVARIANT_SCALAR_OBSTRUCTION_AUDIT.csv"
CSV_1051_GATES = OUT / "P8_Y5_R10_1051_CLAIM_GATES.csv"
DOC_1051 = ROOT / "1051-Y5-R10-no-mixed-hidden-visible-morphism-lemma-or-first-prior-width-chain.md"


def row(**kwargs: object) -> dict[str, object]:
    data = base_row()
    data["claim_allowed"] = False
    data.update(kwargs)
    return data


def truthy(value: object) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"true", "1", "yes", "pass", "valid"}


def formalization_has_2134_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    patterns = (
        "*2134-Y5-R2FR*",
        "*P8_Y5_PARENT_QLOC_2134*",
        "*Y5_R2FR_visible_hidden_curvature_sequester_or_beta_source_pack_2134*",
        "*AFRAME_CURVATURE_SEQUESTER_2134*",
        "*JR2134*",
    )
    try:
        return any(path.is_file() for pattern in patterns for path in FORMALIZATION.rglob(pattern))
    except Exception:
        return False


def source_register_rows() -> list[dict[str, object]]:
    specs = [
        ("SRC2134_00_2133_next", CSV_2133_NEXT, ["NEXT2133_0_2134", "visible-hidden-curvature-sequester"], "2133 handoff selects the curvature sequester/beta source-pack target."),
        ("SRC2134_01_2133_validation", CSV_2133_VAL, ["VAL2133_OVERALL", "PASS"], "2133 validation passed and kept beta_A nonclaim."),
        ("SRC2134_02_2133_beta_attempt", CSV_2133_BETA_ATTEMPT, ["BZ2133_1_product_sequester", "BEST_ZERO_ROUTE_UNSIGNED"], "2133 identifies product/sequester as strongest beta-zero route."),
        ("SRC2134_03_2133_beta_source", CSV_2133_BETA_SOURCE, ["BETA2133_1_beta_value", "MISSING_BETA_A"], "2133 beta source row is missing beta_A."),
        ("SRC2134_04_2133_doc", DOC_2133, ["best zero route is now clean", "`beta_A=0`"], "2133 prose states the clean route and current blocker."),
        ("SRC2134_05_1049_decision", CSV_1049_DEC, ["DEC1049_1_best_theorem_route", "product/sequester"], "1049 selects product/sequester as best theorem route."),
        ("SRC2134_06_1050_theorem", CSV_1050_THEOREM, ["PFT1050_2_forbidden_mixed_hom", "POWERFUL_BUT_UNSIGNED"], "1050 no-mixed coefficient morphism contract is powerful but unsigned."),
        ("SRC2134_07_1050_obstruction", CSV_1050_OBS, ["OBS1050_0_scalar_invariant", "OBS1050_4_radiative_readout"], "1050 scalar invariant and radiative/readout obstructions remain live."),
        ("SRC2134_08_1050_gates", CSV_1050_GATES, ["CG1050_0_product_functor", "false"], "1050 product functor claim gate is blocked."),
        ("SRC2134_09_1050_doc", DOC_1050, ["Hom(C_hid, Coeff(O_vis))", "FAIL_CURRENT_CLAIM_PRIOR_WIDTH_PACK_REQUIRED"], "1050 document gives the general no-mixed hidden-visible morphism form."),
        ("SRC2134_10_1051_nmm", CSV_1051_NMM, ["NMM1051_2_scalar_counterexample", "COUNTEREXAMPLE_PROVED"], "1051 proves the generic hidden invariant scalar counterexample pattern."),
        ("SRC2134_11_1051_iso", CSV_1051_ISO, ["ISO1051_0_hidden_scalar_I", "OBSTRUCTION_PROVED_IF_I_SURVIVES"], "1051 records hidden scalar invariant obstruction."),
        ("SRC2134_12_1051_gates", CSV_1051_GATES, ["CG1051_0_no_mixed", "false"], "1051 no-mixed morphism claim gate remains blocked."),
        ("SRC2134_13_1051_doc", DOC_1051, ["no theorem-zero claim", "surviving hidden scalar"], "1051 prose blocks theorem-zero promotion."),
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


def sequester_theorem_rows() -> list[dict[str, object]]:
    return [
        row(
            theorem_id="CSEQ2134_0_target",
            claim_piece="curvature no-mixed morphism target",
            mathematical_form="Hom(C_hid, Coeff(R[g_obs])) = Const or absent; forbidden maps include A -> beta_A, I_hid -> F(I_hid)R[g_obs], and A R[g_obs]",
            current_status="TARGET_SHARP",
            missing_for_claim="parent observable algebra proof that the coefficient of observed curvature cannot take hidden auxiliary/invariant arguments",
            consequence_if_missing="beta_A remains retained and c_R2_aux cannot be scored or killed",
            valid_for_claim=False,
        ),
        row(
            theorem_id="CSEQ2134_1_visible_geometry_pullback",
            claim_piece="visible geometry depends only on quotient-owned geometry",
            mathematical_form="S_geom = S_geom[q(Phi)] and g_obs,e_obs,omega_obs are pullbacks/descent data of q-owned geometry",
            current_status="EXACT_CONDITIONAL_IF_PARENT_SIGNED",
            missing_for_claim="signed parent statement that eliminated hidden auxiliaries are not arguments of the observed geometric action",
            consequence_if_missing="a hidden coefficient can still multiply R[g_obs] without violating covariance",
            valid_for_claim=False,
        ),
        row(
            theorem_id="CSEQ2134_2_no_mixed_curvature_hom",
            claim_piece="no hidden-to-curvature coefficient morphism",
            mathematical_form="Coeff(R[g_obs]) is a terminal/constant object relative to C_hid; d beta_A / dA = 0 and d beta(I_hid)/dI_hid = 0",
            current_status="POWERFUL_BUT_UNSIGNED",
            missing_for_claim="proof that hidden invariant scalars, representative amplitudes, source markers, and memory variables are not valid coefficient arguments for R[g_obs]",
            consequence_if_missing="R^2/f(R)-type residual route remains legal after integrating out auxiliaries",
            valid_for_claim=False,
        ),
        row(
            theorem_id="CSEQ2134_3_hidden_invariant_scalar_obstruction",
            claim_piece="surviving hidden scalar counterexample",
            mathematical_form="I_hid in O(C_hid)^inv with dI_hid != 0 gives beta(I_hid)=beta_0+epsilon I_hid and DeltaS=sqrt(-g) beta(I_hid) R[g_obs]",
            current_status="COUNTEREXAMPLE_LIVE_UNLESS_SEQUESTERED",
            missing_for_claim="trivial hidden invariant algebra, exact product functor, or explicit ban on hidden arguments in curvature coefficients",
            consequence_if_missing="beta_A cannot be set to zero by quotient-invisibility alone",
            valid_for_claim=False,
        ),
        row(
            theorem_id="CSEQ2134_4_radiative_readout_closure",
            claim_piece="tree-level sequester survives reduction",
            mathematical_form="S_bare product/sequestered implies S_eff and readout-reduced local action also have no hidden coefficient for R[g_obs]",
            current_status="UNSIGNED_CLOSURE",
            missing_for_claim="symmetry, naturality, or renormalization/readout theorem preventing regeneration of beta_A and R^2 terms",
            consequence_if_missing="even a clean bare action would not automatically pass the local GR gate",
            valid_for_claim=False,
        ),
        row(
            theorem_id="CSEQ2134_5_verdict",
            claim_piece="parent-signed curvature sequester",
            mathematical_form="CSEQ2134_1 + CSEQ2134_2 + CSEQ2134_4 signed => beta_A=0 and c_R2_aux=0 for hidden auxiliary curvature channel",
            current_status="CURVATURE_SEQUESTER_NOT_PARENT_SIGNED",
            missing_for_claim="product/sequester/no-mixed-curvature morphism plus radiative/readout closure",
            consequence_if_missing="stage beta_A source pack; no EH/Newton/PPN/local-GR claim",
            valid_for_claim=False,
        ),
    ]


def obstruction_rows() -> list[dict[str, object]]:
    return [
        row(
            obstruction_id="OBS2134_0_hidden_scalar_I",
            obstruction="surviving hidden invariant scalar can feed observed curvature coefficient",
            countermodel="DeltaS = integral sqrt(-g_obs) (beta_0 + epsilon I_hid) R[g_obs]",
            source_evidence="1051:NMM1051_2_scalar_counterexample; 1051:ISO1051_0_hidden_scalar_I",
            needed_to_close="prove O(C_hid)^inv is trivial or prove Coeff(R[g_obs]) cannot take hidden arguments",
            status="LIVE",
        ),
        row(
            obstruction_id="OBS2134_1_geometry_action_not_product_constructed",
            obstruction="parent geometric action is not yet constructed as product/sequestered relative to hidden auxiliaries",
            countermodel="S_parent = S_geom[q] + S_hid[A] + epsilon A R[g_obs]",
            source_evidence="2133:BZ2133_1_product_sequester; 1050:PFT1050_2_forbidden_mixed_hom",
            needed_to_close="signed visible-hidden product functor for the curvature channel",
            status="LIVE",
        ),
        row(
            obstruction_id="OBS2134_2_no_mixed_curvature_morphism_unsigned",
            obstruction="general no-mixed morphism theorem failed current promotion",
            countermodel="natural scalar coefficient beta(I_hid) is covariant and quotient-invisible until coefficient domain is restricted",
            source_evidence="1051:NMM1051_5_verdict; 1051:CG1051_0_no_mixed",
            needed_to_close="parent observable algebra excludes hidden-to-visible coefficient morphisms",
            status="LIVE",
        ),
        row(
            obstruction_id="OBS2134_3_radiative_readout_reentry",
            obstruction="bare sequester does not automatically protect effective/readout action",
            countermodel="integrating out hidden modes regenerates c_R2, beta_A, or curvature-dependent clock/source readout coefficient",
            source_evidence="1050:OBS1050_4_radiative_readout; 1051:NMM1051_4_radiative_readout_limit",
            needed_to_close="radiative/readout closure theorem or source-backed finite residual vector",
            status="LIVE",
        ),
        row(
            obstruction_id="OBS2134_4_auxiliary_constraint_unsigned",
            obstruction="auxiliary pure-constraint/nonpropagating status does not by itself set beta_A=0",
            countermodel="nonpropagating A can still appear algebraically as A R and integrate out to R^2/(M_A^2)",
            source_evidence="2132:AUX2132_0_beta; 2133:BETA2133_4_mass_link",
            needed_to_close="pure-constraint theorem with no curvature source/readout coupling, or explicit beta source row",
            status="LIVE",
        ),
        row(
            obstruction_id="OBS2134_5_source_marker_leak",
            obstruction="source/material/domain markers can act as hidden labels for visible coefficients",
            countermodel="beta_A(marker_source)R[g_obs] or kappa_A(marker)T_A feeding curvature response",
            source_evidence="1050:OBS1050_3_source_labels; 1051:ISO1051_3_domain_marker",
            needed_to_close="source label-forgetting theorem plus no-marker functor for curvature coefficients",
            status="LIVE",
        ),
    ]


def beta_source_pack_rows() -> list[dict[str, object]]:
    return [
        row(pack_id="BPACK2134_0_sector_owner", field="auxiliary_sector_id", required_input="first retained eliminated auxiliary/scalar/memory sector A that can couple to R[g_obs]", current_value="MISSING_SECTOR_OWNER", units="identifier", source_path="MISSING_PARENT_SOURCE", status="BLOCKS_BETA_PACK", valid_for_claim=False),
        row(pack_id="BPACK2134_1_operator_form", field="operator_form", required_input="parent-normalized curvature coupling form", current_value="beta_A A R[g_obs]", units="action_density_operator", source_path="2133 beta-source row; 1051 scalar obstruction pattern", status="SYMBOLIC_TEMPLATE_ONLY", valid_for_claim=False),
        row(pack_id="BPACK2134_2_beta_A", field="beta_A", required_input="numeric value, symbolic parent coefficient, or theorem-zero certificate", current_value="MISSING_BETA_A", units="depends_on_A_normalization", source_path="MISSING_PARENT_COEFFICIENT", status="BLOCKS_C_R2_AUX", valid_for_claim=False),
        row(pack_id="BPACK2134_3_beta_sign", field="beta_A_sign", required_input="sign convention and whether beta_A is signed, free, or exactly zero", current_value="MISSING_SIGN", units="sign", source_path="MISSING_PARENT_COEFFICIENT", status="BLOCKS_STABILITY", valid_for_claim=False),
        row(pack_id="BPACK2134_4_A_normalization", field="A_field_normalization", required_input="normalization and dimension of hidden auxiliary A in EH-normalized action", current_value="MISSING_A_NORMALIZATION", units="field_units", source_path="MISSING_PARENT_NORMALIZATION", status="BLOCKS_UNITS", valid_for_claim=False),
        row(pack_id="BPACK2134_5_mass_link", field="M_A2_or_constraint_link", required_input="mass/Hessian row M_A^2, or theorem that A is pure constraint with no R source", current_value="MISSING_M_A2_LINK", units="mass_squared_or_inverse_length_squared", source_path="MISSING_PARENT_HESSIAN", status="BLOCKS_C_R2_AUX", valid_for_claim=False),
        row(pack_id="BPACK2134_6_cR2_interface", field="c_R2_aux_interface", required_input="c_R2_aux = beta_A^2/(2 M_A^2) after normalization, with no-cancellation guard", current_value="MISSING_BETA_AND_MASS", units="length_squared_after_EH_normalization", source_path="MISSING_BETA_A; MISSING_M_A2_LINK", status="NOT_EXECUTABLE", valid_for_claim=False),
        row(pack_id="BPACK2134_7_lambda_X", field="lambda_X", required_input="range/Compton/local transition scale for the retained auxiliary branch", current_value="MISSING_LAMBDA_X", units="length", source_path="MISSING_ARENA_PROJECTION", status="BLOCKS_R10", valid_for_claim=False),
        row(pack_id="BPACK2134_8_K_X_Qbar", field="K_X_Qbar_XH_qbar_XT", required_input="source/test projection strengths for R10/WEP/PPN/clock/orbital arenas", current_value="MISSING_SOURCE_TEST_PROJECTION", units="arena_specific", source_path="MISSING_ARENA_PROJECTION", status="BLOCKS_EMPIRICAL_SCORE", valid_for_claim=False),
        row(pack_id="BPACK2134_9_readout_map", field="source_readout_map", required_input="map from beta_A/c_R2_aux to local residual vector and PPN/R10 observables", current_value="MISSING_SOURCE_READOUT_MAP", units="arena_specific", source_path="MISSING_READOUT_THEOREM", status="BLOCKS_LOCAL_GR_PPN", valid_for_claim=False),
        row(pack_id="BPACK2134_10_valid_for_claim", field="valid_for_claim", required_input="true only after sector owner, beta, units, mass/constraint, lambda, projections, and source paths are real", current_value=False, units="boolean", source_path="NONCLAIM_CHECKPOINT", status="FORCED_FALSE", valid_for_claim=False),
    ]


def claim_gate_rows() -> list[dict[str, object]]:
    return [
        row(gate_id="GATE2134_0_sources", gate="all cited source paths and needles exist", gate_pass=True, rationale="validated by source register"),
        row(gate_id="GATE2134_1_theorem_shape", gate="curvature sequester theorem shape is exact conditional", gate_pass=True, rationale="if visible geometry is q-owned and no mixed curvature coefficient morphisms exist, beta_A is zero"),
        row(gate_id="GATE2134_2_parent_sequester", gate="parent signs visible-hidden curvature sequester", gate_pass=False, rationale="product/sequester remains a contract, not a parent theorem"),
        row(gate_id="GATE2134_3_no_mixed_curvature_morphism", gate="hidden-to-curvature coefficient morphisms are forbidden", gate_pass=False, rationale="hidden invariant scalar counterexample survives"),
        row(gate_id="GATE2134_4_radiative_readout_closure", gate="sequester survives effective/readout reduction", gate_pass=False, rationale="radiative/readout closure remains unsigned"),
        row(gate_id="GATE2134_5_beta_pack_staged", gate="beta_A source pack is staged", gate_pass=True, rationale="sector owner, beta, sign, units, mass, lambda, projections and readout map are explicit missing rows"),
        row(gate_id="GATE2134_6_beta_pack_executable", gate="beta_A source pack is executable", gate_pass=False, rationale="parent beta_A, A normalization, M_A^2, lambda/projections and source/readout maps are missing"),
        row(gate_id="GATE2134_7_local_GR_Newton_PPN_claim", gate="EH/Newton/PPN/local-GR claim allowed", gate_pass=False, rationale="R2/f(R) residual route and local projections remain open"),
    ]


def decision_rows() -> list[dict[str, object]]:
    return [
        row(decision_id="DEC2134_0", decision="CURVATURE_SEQUESTER_NOT_PARENT_SIGNED", because="the exact conditional route is visible, but hidden invariant scalars and readout reentry remain legal", next_action="do not set beta_A=0 yet"),
        row(decision_id="DEC2134_1", decision="BETA_SOURCE_PACK_REQUIRED", because="without sequester, the first retained auxiliary curvature coefficient must be sourced or bounded", next_action="stage nonclaim beta_A source pack and acquisition queue"),
        row(decision_id="DEC2134_2", decision="BEST_NEXT_IS_NO_MIXED_CURVATURE_MORPHISM_OR_FIRST_OWNER", because="a sharper curvature-only morphism proof is less broad than the full constant-sector product functor and faces less scrutiny", next_action="try to prove Hom(C_hid,Coeff(R[g_obs])) is constant/absent, else identify the first beta_A owner"),
    ]


def next_target_rows() -> list[dict[str, object]]:
    return [
        row(
            route_id="NEXT2134_0_2135",
            next_target="2135-Y5-R2FR-no-mixed-curvature-morphism-lemma-or-first-beta-source-owner.md",
            script="scripts/Y5_R2FR_no_mixed_curvature_morphism_lemma_or_first_beta_source_owner_2135.py",
            objective="Prove the curvature-specific no-mixed morphism lemma Hom(C_hid,Coeff(R[g_obs])) = Const/0 using parent observable algebra and local invariant algebra; if it fails, select the first retained auxiliary sector owner and begin filling beta_A with source-backed units/sign/normalization.",
            forbidden_shortcuts="asserting product functor; using parity alone; erasing parent beta by readout order; inventing beta_A; transferring clock/R10/WEP bounds without projections; formalization-workbench edits; GitHub action",
        )
    ]


def write_branch_copies(
    theorem: list[dict[str, object]],
    obstructions: list[dict[str, object]],
    beta_pack: list[dict[str, object]],
    gates: list[dict[str, object]],
    next_rows: list[dict[str, object]],
) -> list[dict[str, object]]:
    copies = [
        ("COPY2134_0_source_weight_docs", SOURCE_WEIGHT_DOCS / "AFRAME_CURVATURE_SEQUESTER_2134_NONCLAIM.csv", theorem + obstructions + gates),
        ("COPY2134_1_branch_locked_wep", BRANCH_WEP / "P8_Y5_PARENT_QLOC_2134_BETA_SOURCE_PACK_NONCLAIM.csv", beta_pack),
        ("COPY2134_2_acquisition_queue", QUEUE / "JR2134_NO_MIXED_CURVATURE_MORPHISM_OR_BETA_PACK_QUEUE.csv", next_rows + beta_pack),
    ]
    results: list[dict[str, object]] = []
    for copy_id, destination, rows_to_write in copies:
        write_csv(destination, rows_to_write)
        results.append(row(copy_id=copy_id, destination=str(destination), path_exists=destination.exists(), row_count=len(rows_to_write), parse_ok=csv_rows_parse(destination)))
    return results


def validation_rows(
    sources: list[dict[str, object]],
    theorem: list[dict[str, object]],
    obstructions: list[dict[str, object]],
    beta_pack: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    copies: list[dict[str, object]],
    csv_paths: list[Path],
) -> list[dict[str, object]]:
    sources_ok = all(truthy(item["path_exists"]) and truthy(item["needles_found"]) for item in sources)
    theorem_ok = any(item["theorem_id"] == "CSEQ2134_5_verdict" and item["current_status"] == "CURVATURE_SEQUESTER_NOT_PARENT_SIGNED" for item in theorem)
    obstruction_ok = any(item["obstruction_id"] == "OBS2134_0_hidden_scalar_I" and item["status"] == "LIVE" for item in obstructions)
    beta_pack_ok = any(item["pack_id"] == "BPACK2134_2_beta_A" and item["current_value"] == "MISSING_BETA_A" for item in beta_pack) and any(item["pack_id"] == "BPACK2134_10_valid_for_claim" and item["current_value"] is False for item in beta_pack)
    gates_ok = any(item["gate_id"] == "GATE2134_1_theorem_shape" and truthy(item["gate_pass"]) for item in gates) and any(item["gate_id"] == "GATE2134_7_local_GR_Newton_PPN_claim" and not truthy(item["gate_pass"]) for item in gates)
    decisions_ok = any(item["decision_id"] == "DEC2134_2" and "NO_MIXED_CURVATURE" in str(item["decision"]) for item in decisions)
    next_ok = any(item["route_id"] == "NEXT2134_0_2135" for item in next_rows)
    branch_ok = all(truthy(item["path_exists"]) and truthy(item["parse_ok"]) for item in copies)
    csv_ok = all(path.exists() and csv_rows_parse(path) for path in csv_paths)
    no_claim_flags = all(
        not truthy(item.get("claim_allowed", False)) and not truthy(item.get("valid_for_claim", False))
        for group in (sources, theorem, obstructions, beta_pack, gates, decisions, next_rows, copies)
        for item in group
    )
    formalization_clean = count_formalization_modified() == 0 and not formalization_has_2134_artifacts()
    pycache_clean = not (Path(__file__).resolve().parent / "__pycache__").exists()
    all_ok = all([sources_ok, theorem_ok, obstruction_ok, beta_pack_ok, gates_ok, decisions_ok, next_ok, branch_ok, csv_ok, no_claim_flags, formalization_clean, pycache_clean])
    checks = [
        ("VAL2134_00_sources", sources_ok, "all cited 2133/1049/1050/1051 source paths exist and contain expected needles"),
        ("VAL2134_01_theorem_verdict", theorem_ok, "curvature sequester theorem is exact conditional but not parent-signed"),
        ("VAL2134_02_obstructions", obstruction_ok, "hidden invariant scalar obstruction remains live"),
        ("VAL2134_03_beta_pack", beta_pack_ok, "beta_A source pack is staged with valid_for_claim false"),
        ("VAL2134_04_gates", gates_ok, "theorem-shape gate passes while local-GR claim gate fails"),
        ("VAL2134_05_decisions", decisions_ok, "decision ledger selects no-mixed curvature morphism or first beta owner"),
        ("VAL2134_06_next", next_ok, "next target is 2135"),
        ("VAL2134_07_branch_copies", branch_ok, "branch copies exist and parse"),
        ("VAL2134_08_csv_parse", csv_ok, "all generated CSVs parse cleanly"),
        ("VAL2134_09_no_claim_flags", no_claim_flags, "no generated row allows a claim"),
        ("VAL2134_10_formalization_clean", formalization_clean, "formalization-workbench untouched by 2134"),
        ("VAL2134_11_no_pycache", pycache_clean, "scripts __pycache__ removed"),
        ("VAL2134_OVERALL", all_ok, "2134 keeps curvature sequester as an exact conditional theorem, rejects parent-signed beta_A zero for now, and stages a nonclaim beta source pack."),
    ]
    return [row(check_id=check_id, status="PASS" if passed else "FAIL", detail=detail) for check_id, passed, detail in checks]


def write_doc(
    sources: list[dict[str, object]],
    theorem: list[dict[str, object]],
    obstructions: list[dict[str, object]],
    beta_pack: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    copies: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    content = "\n\n".join(
        [
            "# 2134 - Y5/R2FR Visible-Hidden Curvature Sequester Or Beta Source Pack",
            "## Current Verdict",
            "2134 sharpens the 2133 product/sequester route to the curvature channel only. The clean theorem is now explicit: if observed geometry is strictly q-owned and the parent observable algebra forbids hidden-to-curvature coefficient morphisms, then hidden auxiliaries cannot generate `beta_A A R[g_obs]`, so the auxiliary `R^2/f(R)` escape hatch closes.",
            "That theorem is not parent-signed yet. The scalar-invariant counterexample from 1051 still applies to the curvature coefficient: a surviving hidden invariant `I_hid` can form `beta(I_hid) R[g_obs]` unless the parent action forbids that argument or proves the hidden invariant algebra trivial. Therefore `beta_A=0`, EH/Newton/PPN, and local-GR remain unclaimed.",
            "The useful gain is that the missing object is now very precise: either prove the curvature-specific no-mixed morphism `Hom(C_hid,Coeff(R[g_obs])) = Const/0`, or source the first retained `beta_A` owner with units, sign, normalization, `M_A^2`, range/projection, and readout map.",
            "## Source Register",
            md_table(sources, ["source_id", "source_path", "path_exists", "needles_found", "role", "valid_for_claim"]),
            "## Curvature Sequester Theorem Attempt",
            md_table(theorem, ["theorem_id", "claim_piece", "mathematical_form", "current_status", "missing_for_claim", "consequence_if_missing", "valid_for_claim"]),
            "## Curvature Obstruction Ledger",
            md_table(obstructions, ["obstruction_id", "obstruction", "countermodel", "source_evidence", "needed_to_close", "status", "valid_for_claim"]),
            "## Beta Source Pack",
            md_table(beta_pack, ["pack_id", "field", "required_input", "current_value", "units", "source_path", "status", "valid_for_claim"]),
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
    theorem = sequester_theorem_rows()
    obstructions = obstruction_rows()
    beta_pack = beta_source_pack_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_rows = next_target_rows()

    paths = {
        "sources": OUT / "P8_Y5_PARENT_QLOC_2134_SOURCE_REGISTER.csv",
        "theorem": OUT / "P8_Y5_PARENT_QLOC_2134_CURVATURE_SEQUESTER_THEOREM_ATTEMPT.csv",
        "obstructions": OUT / "P8_Y5_PARENT_QLOC_2134_CURVATURE_OBSTRUCTION_LEDGER.csv",
        "beta_pack": OUT / "P8_Y5_PARENT_QLOC_2134_BETA_SOURCE_PACK.csv",
        "gates": OUT / "P8_Y5_PARENT_QLOC_2134_CLAIM_GATES.csv",
        "decisions": OUT / "P8_Y5_PARENT_QLOC_2134_DECISION_LEDGER.csv",
        "next": OUT / "P8_Y5_PARENT_QLOC_2134_NEXT_TARGET.csv",
        "branch": OUT / "P8_Y5_PARENT_QLOC_2134_BRANCH_COPIES.csv",
        "validation": OUT / "P8_Y5_BRR545_2134_VALIDATION.csv",
    }
    write_csv(paths["sources"], sources)
    write_csv(paths["theorem"], theorem)
    write_csv(paths["obstructions"], obstructions)
    write_csv(paths["beta_pack"], beta_pack)
    write_csv(paths["gates"], gates)
    write_csv(paths["decisions"], decisions)
    write_csv(paths["next"], next_rows)

    copies = write_branch_copies(theorem, obstructions, beta_pack, gates, next_rows)
    write_csv(paths["branch"], copies)

    remove_pycache()
    csv_paths = [path for key, path in paths.items() if key != "validation"] + [Path(str(copy["destination"])) for copy in copies]
    validation = validation_rows(sources, theorem, obstructions, beta_pack, gates, decisions, next_rows, copies, csv_paths)
    write_csv(paths["validation"], validation)
    write_doc(sources, theorem, obstructions, beta_pack, gates, decisions, next_rows, copies, validation)

    print(f"wrote {DOC}")
    print(f"validation {paths['validation']}")


if __name__ == "__main__":
    main()
