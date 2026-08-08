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


DOC = ROOT / "2135-Y5-R2FR-no-mixed-curvature-morphism-lemma-or-first-beta-source-owner.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"

CSV_2134_NEXT = OUT / "P8_Y5_PARENT_QLOC_2134_NEXT_TARGET.csv"
CSV_2134_VAL = OUT / "P8_Y5_BRR545_2134_VALIDATION.csv"
CSV_2134_THEOREM = OUT / "P8_Y5_PARENT_QLOC_2134_CURVATURE_SEQUESTER_THEOREM_ATTEMPT.csv"
CSV_2134_OBS = OUT / "P8_Y5_PARENT_QLOC_2134_CURVATURE_OBSTRUCTION_LEDGER.csv"
CSV_2134_BETA = OUT / "P8_Y5_PARENT_QLOC_2134_BETA_SOURCE_PACK.csv"
CSV_2134_DEC = OUT / "P8_Y5_PARENT_QLOC_2134_DECISION_LEDGER.csv"
DOC_2134 = ROOT / "2134-Y5-R2FR-visible-hidden-curvature-sequester-or-beta-source-pack.md"
CSV_1051_NMM = OUT / "P8_Y5_R10_1051_NO_MIXED_MORPHISM_LEMMA_ATTEMPT.csv"
CSV_1051_ISO = OUT / "P8_Y5_R10_1051_INVARIANT_SCALAR_OBSTRUCTION_AUDIT.csv"
CSV_1051_GATES = OUT / "P8_Y5_R10_1051_CLAIM_GATES.csv"
CSV_2131_OWNER = OUT / "P8_Y5_PARENT_QLOC_2131_CR2_OWNER_DECOMPOSITION.csv"
CSV_2132_AUX = OUT / "P8_Y5_PARENT_QLOC_2132_AUX_SCALAR_COEFFICIENT_ROW.csv"
CSV_2132_TOWER = OUT / "P8_Y5_PARENT_QLOC_2132_NO_TOWER_THEOREM_ATTEMPT.csv"
DOC_963 = ROOT / "963-Y5-R10-parent-second-order-signature-or-R2FR-bound-runner.md"
DOC_964 = ROOT / "964-Y5-R10-parent-no-higher-derivative-minimality-theorem-or-R2FR-nonclaim-runner.md"


def row(**kwargs: object) -> dict[str, object]:
    data = base_row()
    data["claim_allowed"] = False
    data.update(kwargs)
    return data


def truthy(value: object) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"true", "1", "yes", "pass", "valid"}


def formalization_has_2135_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    patterns = (
        "*2135-Y5-R2FR*",
        "*P8_Y5_PARENT_QLOC_2135*",
        "*Y5_R2FR_no_mixed_curvature_morphism_lemma_or_first_beta_source_owner_2135*",
        "*AFRAME_NO_MIXED_CURVATURE_2135*",
        "*JR2135*",
    )
    try:
        return any(path.is_file() for pattern in patterns for path in FORMALIZATION.rglob(pattern))
    except Exception:
        return False


def source_register_rows() -> list[dict[str, object]]:
    specs = [
        ("SRC2135_00_2134_next", CSV_2134_NEXT, ["NEXT2134_0_2135", "no-mixed-curvature"], "2134 handoff selects the curvature-specific morphism proof or first beta owner."),
        ("SRC2135_01_2134_validation", CSV_2134_VAL, ["VAL2134_OVERALL", "PASS"], "2134 validation passed."),
        ("SRC2135_02_2134_theorem", CSV_2134_THEOREM, ["CSEQ2134_5_verdict", "CURVATURE_SEQUESTER_NOT_PARENT_SIGNED"], "2134 says curvature sequester is exact conditional but unsigned."),
        ("SRC2135_03_2134_obstruction", CSV_2134_OBS, ["OBS2134_0_hidden_scalar_I", "LIVE"], "2134 keeps hidden scalar curvature obstruction live."),
        ("SRC2135_04_2134_beta", CSV_2134_BETA, ["BPACK2134_2_beta_A", "MISSING_BETA_A"], "2134 beta source pack is missing beta_A."),
        ("SRC2135_05_2134_decision", CSV_2134_DEC, ["DEC2134_2", "NO_MIXED_CURVATURE"], "2134 selects no-mixed curvature morphism as next theorem attempt."),
        ("SRC2135_06_2134_doc", DOC_2134, ["Hom(C_hid,Coeff(R[g_obs])) = Const/0", "source the first retained `beta_A` owner"], "2134 prose states the exact missing object."),
        ("SRC2135_07_1051_nmm", CSV_1051_NMM, ["NMM1051_2_scalar_counterexample", "COUNTEREXAMPLE_PROVED"], "1051 proves generic scalar-invariant mixed coefficient counterexample."),
        ("SRC2135_08_1051_iso", CSV_1051_ISO, ["ISO1051_0_hidden_scalar_I", "OBSTRUCTION_PROVED_IF_I_SURVIVES"], "1051 obstruction audit keeps hidden scalar invariant live."),
        ("SRC2135_09_1051_gates", CSV_1051_GATES, ["CG1051_0_no_mixed", "false"], "1051 no-mixed gate is blocked."),
        ("SRC2135_10_2131_owner", CSV_2131_OWNER, ["OWN2131_2_integrated_out_aux_scalar", "COUNTERMODEL_LIVE_NOT_SOURCED"], "2131 identifies integrated-out auxiliary scalar as live c_R2 owner route."),
        ("SRC2135_11_2132_aux", CSV_2132_AUX, ["AUX2132_0_beta", "MISSING_BETA_A"], "2132 aux row defines beta_A and c_R2_aux blocker."),
        ("SRC2135_12_2132_tower", CSV_2132_TOWER, ["NT2132_1_no_R_coupling", "UNSIGNED"], "2132 no-curvature-coupling clause is unsigned."),
        ("SRC2135_13_963_doc", DOC_963, ["R2", "parent"], "963 documents the R2/fR bound runner context."),
        ("SRC2135_14_964_doc", DOC_964, ["beta phi R", "countermodel"], "964 records the auxiliary scalar curvature-coupling countermodel."),
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


def curvature_morphism_rows() -> list[dict[str, object]]:
    return [
        row(
            lemma_id="NMC2135_0_target",
            claim_piece="curvature-specific no-mixed morphism",
            mathematical_form="Hom(C_hid, Coeff(R[g_obs])) = Const or 0",
            proof_status="TARGET_SHARP",
            derivation_result="this is the exact local-GR protection needed to kill beta_A without sourcing it",
            blocker="none at definition level",
            valid_for_claim=False,
        ),
        row(
            lemma_id="NMC2135_1_constant_EH_case",
            claim_piece="constant EH coefficient would forbid beta_A",
            mathematical_form="S_grav = (1/2 kappa_0) int sqrt(-g_obs) R[g_obs] with kappa_0 a terminal constant not a function on C_hid",
            proof_status="EXACT_CONDITIONAL_THEOREM",
            derivation_result="if the parent signs fixed kappa_0 plus no hidden argument in the EH coefficient, then d Coeff(R)/dA = 0 and beta_A=0",
            blocker="current parent action has not signed terminal/constant kappa_0 as the only curvature coefficient owner",
            valid_for_claim=False,
        ),
        row(
            lemma_id="NMC2135_2_scalar_tensor_countermodel",
            claim_piece="diffeomorphism covariance does not forbid hidden curvature coefficients",
            mathematical_form="DeltaS = int sqrt(-g_obs) F(I_hid) R[g_obs], with F=F0+epsilon I_hid",
            proof_status="COUNTERMODEL_PROVED_IF_I_HID_SURVIVES",
            derivation_result="F(I_hid)R is local, covariant, and curvature-specific; therefore no-mixed curvature fails unless I_hid is absent or coefficient arguments are forbidden",
            blocker="hidden invariant algebra triviality/no-hidden-argument theorem is not parent-signed",
            valid_for_claim=False,
        ),
        row(
            lemma_id="NMC2135_3_bianchi_conservation_check",
            claim_piece="Bianchi identity does not kill F(I)R",
            mathematical_form="variation of F(I)R gives F G_{mu nu} + (g_{mu nu} Box - nabla_mu nabla_nu)F plus the I equation",
            proof_status="NO_FORBIDDANCE",
            derivation_result="covariant conservation is restored by the hidden-field equation/current exchange; this is constrained physics, not an algebraic inconsistency",
            blocker="local tests can bound the residual but cannot be used as a theorem-zero without parent coefficient/source maps",
            valid_for_claim=False,
        ),
        row(
            lemma_id="NMC2135_4_einstein_frame_redefinition_check",
            claim_piece="field redefinition does not make the coupling harmless",
            mathematical_form="conformal move can shift F(I)R into scalar kinetic/potential and matter/source/readout couplings",
            proof_status="NOT_A_ZERO_PROOF",
            derivation_result="even if curvature is made EH-like in one frame, matter constants, clocks, WEP, and PPN inherit couplings unless the matter/readout functor is also parent-signed",
            blocker="matter/source/readout descent is still a separate gate",
            valid_for_claim=False,
        ),
        row(
            lemma_id="NMC2135_5_verdict",
            claim_piece="prove curvature no-mixed morphism now",
            mathematical_form="NMC2135_1 signed and NMC2135_2 excluded and NMC2135_4 harmless => Hom(C_hid,Coeff(R[g_obs])) = Const/0",
            proof_status="NO_MIXED_CURVATURE_MORPHISM_NOT_DERIVED",
            derivation_result="the curvature channel is narrower and cleaner than the full product functor, but scalar-tensor/nonminimal coupling remains a legal countermodel",
            blocker="fixed EH coefficient owner, hidden invariant triviality, and readout/matter-frame harmlessness are unsigned",
            valid_for_claim=False,
        ),
    ]


def countermodel_rows() -> list[dict[str, object]]:
    return [
        row(countermodel_id="CM2135_0_nonminimal_hidden_scalar", form="sqrt(-g) F(I_hid) R[g_obs]", why_legal="local diffeomorphism scalar if I_hid is a surviving scalar invariant", what_it_breaks="Hom(C_hid,Coeff(R)) constant", kill_condition="prove I_hid absent/trivial or forbid hidden arguments in curvature coefficients", status="LIVE"),
        row(countermodel_id="CM2135_1_integrated_out_auxiliary", form="-1/2 M_A^2 A^2 + beta_A A R[g_obs]", why_legal="algebraic auxiliary coupling is covariant and generates beta_A^2 R^2/(2M_A^2)", what_it_breaks="EH-only local reduction", kill_condition="beta_A=0, M_A^-2=0, pure-constraint theorem, or source-backed finite bound", status="LIVE"),
        row(countermodel_id="CM2135_2_marker_prefactor", form="F(sigma_marker) R[g_obs]", why_legal="quotient/domain/source marker can be scalar unless no-marker theorem is signed", what_it_breaks="universal fixed Planck coefficient", kill_condition="source label-forgetting plus no-marker curvature coefficient theorem", status="LIVE"),
        row(countermodel_id="CM2135_3_frame_moved_coupling", form="Einstein-frame EH plus I-dependent matter/source/readout coefficients", why_legal="field redefinition changes representation of coupling, not observable content", what_it_breaks="claim that curvature coupling is harmless by frame choice", kill_condition="parent-signed matter/source/readout equivalence theorem", status="LIVE"),
    ]


def first_owner_rows() -> list[dict[str, object]]:
    return [
        row(owner_id="OWNER2135_0_selected_route", field="first_retained_beta_owner_route", selected_value="integrated_out_auxiliary_curvature_scalar", source_path=str(CSV_2131_OWNER), evidence="OWN2131_2_integrated_out_aux_scalar is COUNTERMODEL_LIVE_NOT_SOURCED", status="SELECTED_NONCLAIM_OWNER_ROUTE", valid_for_claim=False),
        row(owner_id="OWNER2135_1_proxy_sector", field="canonical_proxy_sector_id", selected_value="A_curv_aux_2135", source_path=str(CSV_2132_AUX), evidence="AUX2132 rows define the beta_A/M_A^2/c_R2_aux interface but not the actual parent variable", status="CANONICAL_PLACEHOLDER_NOT_PARENT_VARIABLE", valid_for_claim=False),
        row(owner_id="OWNER2135_2_operator", field="operator_form", selected_value="L_A = -1/2 M_A^2 A_curv_aux^2 + beta_A A_curv_aux R[g_obs]", source_path=str(CSV_2132_AUX), evidence="simple algebraic branch used to expose c_R2_aux = beta_A^2/(2M_A^2)", status="SYMBOLIC_TEMPLATE_ONLY", valid_for_claim=False),
        row(owner_id="OWNER2135_3_beta", field="beta_A", selected_value="MISSING_BETA_A", source_path="MISSING_PARENT_COEFFICIENT", evidence="no parent coefficient row identifies beta_A", status="BLOCKS_C_R2_AUX", valid_for_claim=False),
        row(owner_id="OWNER2135_4_mass", field="M_A2_or_constraint", selected_value="MISSING_M_A2_LINK", source_path="MISSING_PARENT_HESSIAN_OR_CONSTRAINT", evidence="no parent Hessian/constraint row identifies the auxiliary mass or pure-constraint protection", status="BLOCKS_C_R2_AUX", valid_for_claim=False),
        row(owner_id="OWNER2135_5_normalization", field="A_normalization_and_units", selected_value="MISSING_A_NORMALIZATION", source_path="MISSING_PARENT_NORMALIZATION", evidence="cannot convert beta_A^2/(2M_A^2) into EH-normalized c_R2_eff", status="BLOCKS_UNITS", valid_for_claim=False),
        row(owner_id="OWNER2135_6_readout", field="source_readout_projection", selected_value="MISSING_SOURCE_READOUT_MAP", source_path="MISSING_READOUT_THEOREM", evidence="no PPN/R10/clock/orbital projection from A_curv_aux exists", status="BLOCKS_TESTING", valid_for_claim=False),
        row(owner_id="OWNER2135_7_acceptance", field="owner_pack_valid_for_claim", selected_value=False, source_path="NONCLAIM_CHECKPOINT", evidence="selected route is useful but not a sourced parent coefficient", status="FORCED_FALSE", valid_for_claim=False),
    ]


def claim_gate_rows() -> list[dict[str, object]]:
    return [
        row(gate_id="GATE2135_0_sources", gate="all source rows loaded", gate_pass=True, rationale="source register checks 2134/1051/2131/2132/963/964 evidence"),
        row(gate_id="GATE2135_1_constant_EH_conditional", gate="constant EH coefficient theorem shape exists", gate_pass=True, rationale="if kappa_0 is terminal and hidden arguments are banned, beta_A is killed"),
        row(gate_id="GATE2135_2_no_mixed_curvature_proved", gate="no hidden-to-curvature morphism proved", gate_pass=False, rationale="F(I_hid)R scalar-tensor countermodel remains legal"),
        row(gate_id="GATE2135_3_bianchi_kills_countermodel", gate="Bianchi/conservation forbids F(I)R", gate_pass=False, rationale="Bianchi creates coupled equations; it does not algebraically forbid the term"),
        row(gate_id="GATE2135_4_frame_redefinition_harmless", gate="Einstein-frame move makes coupling harmless", gate_pass=False, rationale="coupling moves into matter/source/readout sectors without a signed equivalence theorem"),
        row(gate_id="GATE2135_5_first_owner_selected", gate="first beta owner route selected", gate_pass=True, rationale="integrated-out auxiliary curvature scalar is selected as canonical nonclaim owner route"),
        row(gate_id="GATE2135_6_owner_executable", gate="first owner pack executable", gate_pass=False, rationale="actual parent sector, beta_A, M_A^2, normalization and readout map are missing"),
        row(gate_id="GATE2135_7_local_GR_Newton_PPN_claim", gate="local GR/Newton/PPN claim allowed", gate_pass=False, rationale="curvature no-mixed proof failed and beta owner is nonclaim"),
    ]


def decision_rows() -> list[dict[str, object]]:
    return [
        row(decision_id="DEC2135_0", decision="NO_MIXED_CURVATURE_MORPHISM_NOT_DERIVED", because="a surviving hidden scalar invariant can multiply R[g_obs] without violating covariance", next_action="do not set beta_A=0 from curvature specialness alone"),
        row(decision_id="DEC2135_1", decision="BETA_OWNER_ROUTE_SELECTED", because="the integrated-out auxiliary scalar is the cleanest live countermodel and already owns c_R2_aux if beta_A/M_A^2 are real", next_action="use A_curv_aux_2135 as the canonical nonclaim proxy until an actual parent variable is identified"),
        row(decision_id="DEC2135_2", decision="BEST_NEXT_IS_FIXED_EH_COEFFICIENT_OR_A_CURV_VARIABLE_MAP", because="the least-scrutiny route is to prove the EH coefficient is terminal/constant; if that fails, map A_curv_aux_2135 to a concrete MTS variable and source beta_A", next_action="attack 2136 fixed Planck/EH coefficient naturality theorem or parent variable owner map"),
    ]


def next_target_rows() -> list[dict[str, object]]:
    return [
        row(
            route_id="NEXT2135_0_2136",
            next_target="2136-Y5-R2FR-fixed-EH-coefficient-naturality-or-Acurv-parent-variable-map.md",
            script="scripts/Y5_R2FR_fixed_EH_coefficient_naturality_or_Acurv_parent_variable_map_2136.py",
            objective="Try to prove the observed EH coefficient is a terminal/constant parent datum independent of hidden invariant scalars; if that fails, map A_curv_aux_2135 to an actual MTS parent variable/sector and start sourcing beta_A, M_A^2, normalization and readout projections.",
            forbidden_shortcuts="declaring units fix physics; hiding F(I)R by Einstein-frame redefinition without matter/readout proof; inventing beta_A; using local bounds as parent coefficients; formalization-workbench edits; GitHub action",
        )
    ]


def write_branch_copies(
    lemma: list[dict[str, object]],
    countermodels: list[dict[str, object]],
    owners: list[dict[str, object]],
    gates: list[dict[str, object]],
    next_rows: list[dict[str, object]],
) -> list[dict[str, object]]:
    copies = [
        ("COPY2135_0_source_weight_docs", SOURCE_WEIGHT_DOCS / "AFRAME_NO_MIXED_CURVATURE_2135_NONCLAIM.csv", lemma + countermodels + gates),
        ("COPY2135_1_branch_locked_wep", BRANCH_WEP / "P8_Y5_PARENT_QLOC_2135_FIRST_BETA_OWNER_NONCLAIM.csv", owners),
        ("COPY2135_2_acquisition_queue", QUEUE / "JR2135_FIXED_EH_OR_ACURV_OWNER_QUEUE.csv", next_rows + owners),
    ]
    results: list[dict[str, object]] = []
    for copy_id, destination, rows_to_write in copies:
        write_csv(destination, rows_to_write)
        results.append(row(copy_id=copy_id, destination=str(destination), path_exists=destination.exists(), row_count=len(rows_to_write), parse_ok=csv_rows_parse(destination)))
    return results


def validation_rows(
    sources: list[dict[str, object]],
    lemma: list[dict[str, object]],
    countermodels: list[dict[str, object]],
    owners: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    copies: list[dict[str, object]],
    csv_paths: list[Path],
) -> list[dict[str, object]]:
    sources_ok = all(truthy(item["path_exists"]) and truthy(item["needles_found"]) for item in sources)
    lemma_ok = any(item["lemma_id"] == "NMC2135_5_verdict" and item["proof_status"] == "NO_MIXED_CURVATURE_MORPHISM_NOT_DERIVED" for item in lemma)
    countermodels_ok = any(item["countermodel_id"] == "CM2135_0_nonminimal_hidden_scalar" and item["status"] == "LIVE" for item in countermodels)
    owners_ok = any(item["owner_id"] == "OWNER2135_0_selected_route" and item["selected_value"] == "integrated_out_auxiliary_curvature_scalar" for item in owners) and any(item["owner_id"] == "OWNER2135_3_beta" and item["selected_value"] == "MISSING_BETA_A" for item in owners)
    gates_ok = any(item["gate_id"] == "GATE2135_2_no_mixed_curvature_proved" and not truthy(item["gate_pass"]) for item in gates) and any(item["gate_id"] == "GATE2135_5_first_owner_selected" and truthy(item["gate_pass"]) for item in gates)
    decisions_ok = any(item["decision_id"] == "DEC2135_2" and "FIXED_EH" in str(item["decision"]) for item in decisions)
    next_ok = any(item["route_id"] == "NEXT2135_0_2136" for item in next_rows)
    branch_ok = all(truthy(item["path_exists"]) and truthy(item["parse_ok"]) for item in copies)
    csv_ok = all(path.exists() and csv_rows_parse(path) for path in csv_paths)
    no_claim_flags = all(
        not truthy(item.get("claim_allowed", False)) and not truthy(item.get("valid_for_claim", False))
        for group in (sources, lemma, countermodels, owners, gates, decisions, next_rows, copies)
        for item in group
    )
    formalization_clean = count_formalization_modified() == 0 and not formalization_has_2135_artifacts()
    pycache_clean = not (Path(__file__).resolve().parent / "__pycache__").exists()
    all_ok = all([sources_ok, lemma_ok, countermodels_ok, owners_ok, gates_ok, decisions_ok, next_ok, branch_ok, csv_ok, no_claim_flags, formalization_clean, pycache_clean])
    checks = [
        ("VAL2135_00_sources", sources_ok, "all cited 2134/1051/2131/2132/963/964 sources exist and contain expected needles"),
        ("VAL2135_01_lemma", lemma_ok, "no-mixed curvature morphism proof fails cleanly under current evidence"),
        ("VAL2135_02_countermodels", countermodels_ok, "nonminimal hidden scalar curvature countermodel remains live"),
        ("VAL2135_03_owner", owners_ok, "first beta owner route selected but beta_A remains missing"),
        ("VAL2135_04_gates", gates_ok, "no-mixed gate fails while first-owner gate passes"),
        ("VAL2135_05_decisions", decisions_ok, "decision ledger selects fixed EH coefficient theorem or A_curv variable map next"),
        ("VAL2135_06_next", next_ok, "next target is 2136"),
        ("VAL2135_07_branch_copies", branch_ok, "branch copies exist and parse"),
        ("VAL2135_08_csv_parse", csv_ok, "all generated CSVs parse cleanly"),
        ("VAL2135_09_no_claim_flags", no_claim_flags, "no generated row allows a claim"),
        ("VAL2135_10_formalization_clean", formalization_clean, "formalization-workbench untouched by 2135"),
        ("VAL2135_11_no_pycache", pycache_clean, "scripts __pycache__ removed"),
        ("VAL2135_OVERALL", all_ok, "2135 rejects the no-mixed curvature theorem under current evidence, selects the integrated-out auxiliary curvature scalar as first beta owner route, and keeps all local-GR claims blocked."),
    ]
    return [row(check_id=check_id, status="PASS" if passed else "FAIL", detail=detail) for check_id, passed, detail in checks]


def write_doc(
    sources: list[dict[str, object]],
    lemma: list[dict[str, object]],
    countermodels: list[dict[str, object]],
    owners: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    copies: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    content = "\n\n".join(
        [
            "# 2135 - Y5/R2FR No-Mixed Curvature Morphism Lemma Or First Beta Source Owner",
            "## Current Verdict",
            "2135 tried the narrower, less-scrutiny route: perhaps curvature is special even though the broader no-mixed product functor failed. The useful conditional theorem is real: if the observed EH coefficient is a terminal constant and hidden arguments are forbidden in `Coeff(R[g_obs])`, then `beta_A=0` and the integrated-out auxiliary `R^2/f(R)` escape hatch closes.",
            "But the proof does not close from the current parent material. A scalar-tensor style countermodel `F(I_hid) R[g_obs]` is local, covariant, and curvature-specific if any hidden invariant scalar survives. Bianchi conservation does not algebraically forbid it; it produces the usual extra derivative/current-exchange terms. Einstein-frame movement also does not make it harmless unless matter/source/readout descent is signed.",
            "So this is a useful failure, not a dead end: the first retained beta owner route is now selected as the integrated-out auxiliary curvature scalar, canonically named `A_curv_aux_2135` until an actual MTS parent variable is identified. It remains nonclaim because `beta_A`, `M_A^2`, normalization, and readout/source projections are missing.",
            "## Source Register",
            md_table(sources, ["source_id", "source_path", "path_exists", "needles_found", "role", "valid_for_claim"]),
            "## No-Mixed Curvature Morphism Attempt",
            md_table(lemma, ["lemma_id", "claim_piece", "mathematical_form", "proof_status", "derivation_result", "blocker", "valid_for_claim"]),
            "## Countermodel Ledger",
            md_table(countermodels, ["countermodel_id", "form", "why_legal", "what_it_breaks", "kill_condition", "status", "valid_for_claim"]),
            "## First Beta Owner Route",
            md_table(owners, ["owner_id", "field", "selected_value", "source_path", "evidence", "status", "valid_for_claim"]),
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
    lemma = curvature_morphism_rows()
    countermodels = countermodel_rows()
    owners = first_owner_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_rows = next_target_rows()

    paths = {
        "sources": OUT / "P8_Y5_PARENT_QLOC_2135_SOURCE_REGISTER.csv",
        "lemma": OUT / "P8_Y5_PARENT_QLOC_2135_NO_MIXED_CURVATURE_MORPHISM_ATTEMPT.csv",
        "countermodels": OUT / "P8_Y5_PARENT_QLOC_2135_CURVATURE_COUNTERMODEL_LEDGER.csv",
        "owners": OUT / "P8_Y5_PARENT_QLOC_2135_FIRST_BETA_OWNER_ROUTE.csv",
        "gates": OUT / "P8_Y5_PARENT_QLOC_2135_CLAIM_GATES.csv",
        "decisions": OUT / "P8_Y5_PARENT_QLOC_2135_DECISION_LEDGER.csv",
        "next": OUT / "P8_Y5_PARENT_QLOC_2135_NEXT_TARGET.csv",
        "branch": OUT / "P8_Y5_PARENT_QLOC_2135_BRANCH_COPIES.csv",
        "validation": OUT / "P8_Y5_BRR545_2135_VALIDATION.csv",
    }
    write_csv(paths["sources"], sources)
    write_csv(paths["lemma"], lemma)
    write_csv(paths["countermodels"], countermodels)
    write_csv(paths["owners"], owners)
    write_csv(paths["gates"], gates)
    write_csv(paths["decisions"], decisions)
    write_csv(paths["next"], next_rows)

    copies = write_branch_copies(lemma, countermodels, owners, gates, next_rows)
    write_csv(paths["branch"], copies)

    remove_pycache()
    csv_paths = [path for key, path in paths.items() if key != "validation"] + [Path(str(copy["destination"])) for copy in copies]
    validation = validation_rows(sources, lemma, countermodels, owners, gates, decisions, next_rows, copies, csv_paths)
    write_csv(paths["validation"], validation)
    write_doc(sources, lemma, countermodels, owners, gates, decisions, next_rows, copies, validation)

    print(f"wrote {DOC}")
    print(f"validation {paths['validation']}")


if __name__ == "__main__":
    main()
