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


DOC = ROOT / "2147-Y5-R2FR-local-GR-two-gate-spine-source-operator-join.md"
REPO = ROOT.parent
FORMALIZATION = REPO / "formalization-workbench"

DOCS = {
    "2146": ROOT / "2146-Y5-R2FR-Noether-current-owner-and-no-current-rescale-proof-or-cA-bound-row.md",
    "2144": ROOT / "2144-Y5-R2FR-MHref-Qtau-Gref-source-readout-bridge-or-closure.md",
    "2143": ROOT / "2143-Y5-R2FR-local-curvature-operator-norm-and-source-bridge-bound.md",
    "2142": ROOT / "2142-Y5-R2FR-saturation-action-vs-constitutive-branch-and-PPN-bound-runner.md",
    "2141": ROOT / "2141-Y5-R2FR-GammaG-functional-contract-or-local-kernel-zero-proof.md",
    "2140": ROOT / "2140-Y5-R2FR-GammaG-metric-variation-local-silence-or-residual-row.md",
    "2139": ROOT / "2139-Y5-R2FR-deep-parent-action-owner-hunt-or-coefficient-owner-checklist.md",
    "1823": ROOT / "1823-Y5-R2FR-primitive-deficit-action-law-or-visible-c2-owner-row.md",
    "1822": ROOT / "1822-Y5-R2FR-linear-holonomy-parent-axiom-or-R2FR-coefficient-owner-row.md",
    "1821": ROOT / "1821-Y5-R2FR-no-higher-derivative-parent-minimality-or-R2FR-bound-row.md",
    "1820": ROOT / "1820-Y5-R2FR-EH-operator-selection-minimality-or-R11-C-EH-first-row.md",
    "1819": ROOT / "1819-Y5-R2FR-local-EH-symplectic-charge-inheritance-or-Cterm-residual-vector.md",
    "1818": ROOT / "1818-Y5-R2FR-Hilbert-worldtube-charge-identity-or-R-Hsrc-bound-row.md",
    "1817": ROOT / "1817-Y5-R2FR-source-worldtube-transfer-kernel-or-post-current-cA-bound-row.md",
    "1816": ROOT / "1816-Y5-R2FR-variation-before-readout-source-selector-order-or-post-current-cA-row.md",
    "1815": ROOT / "1815-Y5-R2FR-Noether-current-owner-and-no-current-rescale-proof-or-cA-bound-row.md",
}


def row(**kwargs: object) -> dict[str, object]:
    data = base_row()
    data["claim_allowed"] = False
    data.update(kwargs)
    return data


def truthy(value: object) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"true", "1", "yes", "pass", "valid"}


def has_any(text: str, alternatives: list[str]) -> bool:
    return any(item in text for item in alternatives)


def find_line(path: Path, alternatives: list[str]) -> tuple[int, str]:
    text = read_text(path) if path.exists() else ""
    for line_number, line in enumerate(text.splitlines(), start=1):
        if has_any(line, alternatives):
            return line_number, line.strip()
    return 0, "MISSING_NEEDLE"


def formalization_has_2147_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    patterns = (
        "*2147-Y5-R2FR*",
        "*P8_Y5_PARENT_QLOC_2147*",
        "*Y5_R2FR_local_GR_two_gate_spine_source_operator_join_2147*",
        "*AFRAME_LOCAL_GR_TWO_GATE_JOIN_2147*",
        "*JR2147*",
    )
    try:
        return any(path.is_file() for pattern in patterns for path in FORMALIZATION.rglob(pattern))
    except Exception:
        return False


def source_register_rows() -> list[dict[str, object]]:
    specs = [
        ("SRC2147_00_2146", DOCS["2146"], [["VAL2146_OVERALL"], ["two-gate spine"], ["NEXT2146_0_2147"]], "2146 handoff selects local-GR two-gate join"),
        ("SRC2147_01_2139", DOCS["2139"], [["EH_ACTION_SOURCE_FOUND"], ["GAMMAG_IS_PRIMARY_ACTION_OWNER_CANDIDATE"], ["VAL2139_OVERALL"]], "raw EH/Gamma_G source evidence"),
        ("SRC2147_02_2140", DOCS["2140"], [["D_Gamma"], ["Gamma_G -> 0"], ["VAL2140_OVERALL"]], "Gamma_G first-variation blocker"),
        ("SRC2147_03_2141", DOCS["2141"], [["flat-kernel double-zero"], ["PROMOTE_S_AS_PRIMARY_GAMMAG_PARENT_SKELETON"], ["VAL2141_OVERALL"]], "Gamma_G/S functional skeleton and double-zero condition"),
        ("SRC2147_04_2142", DOCS["2142"], [["S_K=1.000000E-122"], ["NUMERIC_SMALLNESS_IS_REAL"], ["VAL2142_OVERALL"]], "local K_solar smallness but nonclaim runner"),
        ("SRC2147_05_2143", DOCS["2143"], [["2.000000E-122"], ["DELTAK_REDUCED_TO_SOURCE_FRACTIONS"], ["VAL2143_OVERALL"]], "local curvature bound reduced to source/readout fractions"),
        ("SRC2147_06_2144", DOCS["2144"], [["Delta_Hsrc"], ["BRIDGE_NOT_CLOSED"], ["VAL2144_OVERALL"]], "source/readout bridge decomposed but unclosed"),
        ("SRC2147_07_1815", DOCS["1815"], [["NO_CURRENT_RESCALE_CONTRACT_NOT_CURRENT_PROOF"], ["pre_variation_weight", "pre-variation"], ["VAL1815_OVERALL"]], "post-current cA conditional and pre-action weight survival"),
        ("SRC2147_08_1816", DOCS["1816"], [["variation-before-readout"], ["preaction", "pre-action"], ["VAL1816_OVERALL"]], "variation/readout ordering"),
        ("SRC2147_09_1817", DOCS["1817"], [["K_arena"], ["R_Hsrc"], ["VAL1817_OVERALL"]], "arena/worldtube transfer kernel and R_Hsrc"),
        ("SRC2147_10_1818", DOCS["1818"], [["G_ref^-1 Q_tau"], ["R_Hsrc"], ["VAL1818_OVERALL"]], "Hilbert/worldtube charge identity contract"),
        ("SRC2147_11_1819", DOCS["1819"], [["C_EH"], ["C_extra"], ["VAL1819_OVERALL"]], "EH charge inheritance and C-term residuals"),
        ("SRC2147_12_1820", DOCS["1820"], [["R2/fR"], ["second-order"], ["VAL1820_OVERALL"]], "EH/minimality/R2FR gate"),
        ("SRC2147_13_1821", DOCS["1821"], [["LINEAR_HOLONOMY_PARENT_AXIOM_NEXT"], ["linear holonomy"], ["VAL1821_OVERALL"]], "linear holonomy parent axiom route"),
        ("SRC2147_14_1822", DOCS["1822"], [["PRIMITIVE_DEFICIT_ACTION_LAW_NEXT"], ["same-cell"], ["VAL1822_OVERALL"]], "same-cell additivity insufficient; deficit law selected"),
        ("SRC2147_15_1823", DOCS["1823"], [["PHI_SECOND_DERIVATIVE_ZERO_OR_VISIBLE_C2_SOURCE_NEXT"], ["c2_visible"], ["VAL1823_OVERALL"]], "visible c2/Phi'' hinge"),
    ]
    rows: list[dict[str, object]] = []
    for source_id, path, needle_groups, role in specs:
        exists = path.exists()
        text = read_text(path) if exists else ""
        needles_found = exists and all(has_any(text, group) for group in needle_groups)
        rows.append(
            row(
                source_id=source_id,
                source_path=str(path),
                path_exists=exists,
                needles_found=needles_found,
                expected_needles="; ".join(" OR ".join(group) for group in needle_groups),
                role=role,
            )
        )
    return rows


def two_gate_theorem_rows() -> list[dict[str, object]]:
    return [
        row(
            theorem_id="TGT2147_0_domain",
            clause="local compact weak-field domain",
            statement="For a stationary compact source with exterior annulus A_ext, observed geometry must be a single metric/coframe geometry with fixed local time/radius readout and controlled boundary caps.",
            required_evidence="domain/worldtube support; observed coframe; tau/radius normalization; boundary/corner class",
            current_status="CONTRACT_ONLY",
        ),
        row(
            theorem_id="TGT2147_1_operator_gate",
            clause="operator-side GR gate",
            statement="The exterior Euler operator equals EH/Einstein plus Lambda/topological/boundary silence and bounded residual R_op = R_GammaG + R_R2FR + R_connection + R_extra + R_boundary.",
            required_evidence="Gamma_G first-variation silence or bound; c_R2/f_RR zero/bound; LC connection; no extra sectors or explicit residuals",
            current_status="OPEN_PRIMARY_GATE",
        ),
        row(
            theorem_id="TGT2147_2_source_gate",
            clause="source-side Newton gate",
            statement="The source parameter in the EH-like exterior solution equals the parent Hilbert/Hamiltonian worldtube charge and the measured orbital GM through G_ref^-1 Q_tau = Pi_M^H J_H^dress + dB_H + R_Hsrc.",
            required_evidence="Q_tau integrability; Pi_M^H/source current owner; fixed reference; Gauss/Poisson calibration; R_Hsrc zero/bound",
            current_status="OPEN_PRIMARY_GATE",
        ),
        row(
            theorem_id="TGT2147_3_join",
            clause="local GR/Newton reduction",
            statement="If operator gate and source gate both close, the weak-field exterior reduces to the GR/Newton equations up to R_join = R_op + R_source + R_readout + R_projection; only then can PPN/Newton claims be scored.",
            required_evidence="all operator and source residuals theorem-zero or source-backed below arena thresholds",
            current_status="EXACT_CONDITIONAL_SPINE_NOT_CLAIM",
        ),
        row(
            theorem_id="TGT2147_4_no_shortcuts",
            clause="anti-circularity rule",
            statement="EH-looking notation, Poisson shape, small K_solar, Gamma_G=0 at zeroth order, or post-current cA cleanup cannot substitute for the two closed gates.",
            required_evidence="explicit residual ledger remains nonclaim until every missing input is supplied",
            current_status="GUARDRAIL_ACTIVE",
        ),
    ]


def operator_gate_rows() -> list[dict[str, object]]:
    return [
        row(component_id="OP2147_0_EH_source", component="EH action source", current_gain="raw action files contain an EH-looking term and kappa notation", blocker="terminal kappa/measured-G bridge and Gamma_G variation are not proven", closure_condition="source evidence only; not sufficient for local GR"),
        row(component_id="OP2147_1_GammaG", component="Gamma_G/S local residual", current_gain="flat-kernel double-zero and K_solar smallness runner exist", blocker="real local curvature produces D_Gamma/operator, boundary/history and Bianchi-current obligations", closure_condition="Gamma_G=0, D_Gamma=0 and boundary/history silence, or finite arena-bounded residual"),
        row(component_id="OP2147_2_R2FR", component="R2/fR scalar mode", current_gain="blocker sharpened to primitive deficit response Phi''(0)=0 or c2_visible owner", blocker="primitive linear deficit law is not derived and c2_visible is unsourced", closure_condition="prove Phi''(0)=0 with no hidden tower, or source c2_visible -> c_R2_eff -> lambda_s/alpha_s bound"),
        row(component_id="OP2147_3_connection", component="LC/coframe/connection", current_gain="observed geometry/coframe route exists in prior checkpoints", blocker="affine/torsion/nonmetricity and sector-Gamma slots must remain silent or bounded", closure_condition="observed connection is LC for local branch, or P4/connection residual vector is bounded"),
        row(component_id="OP2147_4_extra_sectors", component="hidden/projector/memory sectors", current_gain="major residual families are named and quarantined", blocker="no universal no-hair/no-marker/no-integrated-tower theorem closes them all", closure_condition="each extra sector absent, gauge/topological, no-haired, or carried into explicit residual rows"),
        row(component_id="OP2147_5_conservation", component="Bianchi/exchange current", current_gain="Bianchi blocker is explicit", blocker="constitutive branch needs exchange current; action branch needs full varied residual conservation", closure_condition="nabla^mu(E_EH+E_extra)_{mu nu}=0 or matched source exchange current"),
        row(component_id="OP2147_6_operator_verdict", component="operator gate total", current_gain="operator gate is now explicit and not hidden in broad coupling language", blocker="Gamma_G and R2FR/c2 are the sharpest live operator pieces", closure_condition="not closed; primary next attack is Phi''(0)=0 or c2_visible source"),
    ]


def source_gate_rows() -> list[dict[str, object]]:
    return [
        row(component_id="SRCG2147_0_matter_current", component="parent Hilbert/Noether matter current", current_gain="post-current cA can be demoted conditionally", blocker="pre-action weights and selector kernels survive", closure_condition="matter current is varied before readout with no source-only prefactor"),
        row(component_id="SRCG2147_1_Qtau_integrability", component="Q_tau Hamiltonian/CPS charge", current_gain="Delta_Hsrc decomposition identifies exact mismatch terms", blocker="integrability, fixed-reference and boundary zero clauses are unsigned", closure_condition="Q_tau is integrable and reference-stable on the local worldtube"),
        row(component_id="SRCG2147_2_worldtube_identity", component="Hilbert/worldtube source identity", current_gain="identity form G_ref^-1 Q_tau = Pi_M^H J_H^dress + dB_H + R_Hsrc is available", blocker="R_Hsrc remains open because Pi_M^H commutator, boundary term and extra-charge silence are not closed", closure_condition="R_Hsrc=0 or source-backed bound with no cancellation credit"),
        row(component_id="SRCG2147_3_measured_G", component="G_ref and measured orbital GM", current_gain="epsilon_mu is decomposed into G_ref/Hsrc/Gauss/PPN/readout pieces", blocker="calibrating G_ref after orbital fitting would be circular", closure_condition="one parent normalization maps to measured G and orbital GM without fitting away residuals"),
        row(component_id="SRCG2147_4_readout", component="tau/radius/frame readout", current_gain="epsilon_r and epsilon_frame are named and retained", blocker="observed radius/time/frame are not parent-locked in the source bridge", closure_condition="readout map fixed before residual scoring"),
        row(component_id="SRCG2147_5_arena_projection", component="PPN/R10/clock/orbital projections", current_gain="arena rows exist and block claims explicitly", blocker="tau_clock product cannot transfer to WEP/R10/local-GR without kernel equality", closure_condition="projection kernels are sourced per arena, not borrowed"),
        row(component_id="SRCG2147_6_source_verdict", component="source gate total", current_gain="source-side Newton gate is explicit", blocker="Delta_Hsrc/R_Hsrc remains open and cannot be closed by Poisson shape", closure_condition="not closed; viable secondary target after operator gate"),
    ]


def join_residual_rows() -> list[dict[str, object]]:
    return [
        row(residual_id="RJ2147_0_operator", symbol="R_op", definition="R_GammaG + R_R2FR + R_connection + R_extra + R_boundary", source_gate="operator", current_status="OPEN", score_ready=False),
        row(residual_id="RJ2147_1_source", symbol="R_source", definition="Delta_Hsrc/M_H_ref + epsilon_Gref + epsilon_Gauss + epsilon_PPN", source_gate="source", current_status="OPEN", score_ready=False),
        row(residual_id="RJ2147_2_readout", symbol="R_readout", definition="epsilon_r + epsilon_frame + tau/radius/frame projection residuals", source_gate="source", current_status="OPEN", score_ready=False),
        row(residual_id="RJ2147_3_current", symbol="R_current", definition="w_A + K_arena + pre-action/source-selector residuals; post-current cA only guard/convention if parent current theorem closes", source_gate="source/current", current_status="OPEN_GUARD", score_ready=False),
        row(residual_id="RJ2147_4_join", symbol="R_join", definition="R_op + R_source + R_readout + R_current", source_gate="join", current_status="NONCLAIM_VECTOR", score_ready=False),
        row(residual_id="RJ2147_5_ppn", symbol="r_PPN", definition="projection of R_join into gamma,beta,preferred-frame,conservation and range-dependent residuals", source_gate="arena", current_status="NOT_SCORE_READY", score_ready=False),
        row(residual_id="RJ2147_6_newton", symbol="r_Newton", definition="projection of R_join into Poisson/Gauss/measured-GM/orbital acceleration residuals", source_gate="arena", current_status="NOT_SCORE_READY", score_ready=False),
    ]


def decision_rows() -> list[dict[str, object]]:
    return [
        row(decision_id="DEC2147_0_join_written", decision="LOCAL_GR_TWO_GATE_CONTRACT_WRITTEN", because="operator-side EH/GammaG/R2FR and source-side Hamiltonian/measured-G gates are now separated and joined by an explicit residual vector", next_action="use this as the local-GR/Newton reduction spine"),
        row(decision_id="DEC2147_1_no_claim", decision="NO_LOCAL_GR_NEWTON_CLAIM", because="both gates still contain open residuals and score projections are not source-backed", next_action="keep private nonclaim status"),
        row(decision_id="DEC2147_2_primary_gate_order", decision="OPERATOR_GATE_FIRST", because="a Newton source bridge is not enough if the exterior operator still carries a live R2/fR scalar mode or Gamma_G first-variation residual", next_action="attack Phi''(0)=0/c2_visible before trying to promote measured-GM closure"),
        row(decision_id="DEC2147_3_secondary_gate", decision="SOURCE_GATE_SECONDARY_PARALLEL", because="Delta_Hsrc/R_Hsrc remains essential but depends on a stable operator/EH charge inheritance context", next_action="keep Delta_Hsrc source equality queued as secondary path"),
        row(decision_id="DEC2147_4_least_circular_next", decision="PHI_SECOND_DERIVATIVE_ZERO_OR_C2_SOURCE_NEXT", because="this directly tests whether MTS really forces EH-like first-order curvature response rather than importing GR by notation", next_action="2148 derive Phi''(0)=0 or source c2_visible as finite residual"),
    ]


def next_target_rows() -> list[dict[str, object]]:
    return [
        row(
            route_id="NEXT2147_0_2148",
            next_target="2148-Y5-R2FR-Phi-second-derivative-zero-or-visible-c2-source-row.md",
            script="scripts/Y5_R2FR_Phi_second_derivative_zero_or_visible_c2_source_row_2148.py",
            objective="Attack the operator gate first: derive Phi''(0)=0 for the primitive deficit response using an oriented first-moment/holonomy action principle with no hidden second response channel; if it fails, source or quarantine c2_visible, ell_cell, shape_factor and c_R2_eff as nonclaim finite residual rows.",
            forbidden_shortcuts="do not use disjoint additivity as linearity proof; do not use no-new-scale argument to zero R2/fR; do not import Regge/EH as proof unless MTS owns the primitive action law; do not claim local GR/Newton; no formalization-workbench edits; no GitHub action",
        ),
        row(
            route_id="NEXT2147_1_secondary",
            next_target="2148b-Y5-R2FR-Delta-Hsrc-source-equality-secondary-queue.md",
            script="scripts/Y5_R2FR_Delta_Hsrc_source_equality_secondary_queue_2148b.py",
            objective="Secondary queue: continue the source-side Hamiltonian/worldtube/measured-G bridge once the operator gate is less ambiguous.",
            forbidden_shortcuts="no orbital-GM fitting proof; no cancellation among Delta_Hsrc components; no imported EH charge as MTS charge",
        ),
    ]


def write_branch_copies(
    theorem: list[dict[str, object]],
    operator: list[dict[str, object]],
    source: list[dict[str, object]],
    residuals: list[dict[str, object]],
    next_rows: list[dict[str, object]],
) -> list[dict[str, object]]:
    copies = [
        ("COPY2147_0_source_weight_docs", SOURCE_WEIGHT_DOCS / "AFRAME_LOCAL_GR_TWO_GATE_JOIN_2147_NONCLAIM.csv", theorem + operator + source),
        ("COPY2147_1_branch_locked_wep", BRANCH_WEP / "P8_Y5_PARENT_QLOC_2147_LOCAL_GR_JOIN_NONCLAIM.csv", residuals + source),
        ("COPY2147_2_acquisition_queue", QUEUE / "JR2147_PHI_SECOND_DERIVATIVE_OR_C2_QUEUE.csv", next_rows + operator),
    ]
    results: list[dict[str, object]] = []
    for copy_id, destination, rows_to_write in copies:
        write_csv(destination, rows_to_write)
        results.append(row(copy_id=copy_id, destination=str(destination), path_exists=destination.exists(), row_count=len(rows_to_write), parse_ok=csv_rows_parse(destination)))
    return results


def validation_rows(
    sources: list[dict[str, object]],
    theorem: list[dict[str, object]],
    operator: list[dict[str, object]],
    source: list[dict[str, object]],
    residuals: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    copies: list[dict[str, object]],
    csv_paths: list[Path],
) -> list[dict[str, object]]:
    sources_ok = all(truthy(item["path_exists"]) and truthy(item["needles_found"]) for item in sources)
    theorem_ok = (
        any(item["theorem_id"] == "TGT2147_1_operator_gate" and item["current_status"] == "OPEN_PRIMARY_GATE" for item in theorem)
        and any(item["theorem_id"] == "TGT2147_2_source_gate" and item["current_status"] == "OPEN_PRIMARY_GATE" for item in theorem)
        and any(item["theorem_id"] == "TGT2147_3_join" and item["current_status"] == "EXACT_CONDITIONAL_SPINE_NOT_CLAIM" for item in theorem)
    )
    operator_ok = (
        any(item["component_id"] == "OP2147_1_GammaG" and "D_Gamma" in str(item["blocker"]) for item in operator)
        and any(item["component_id"] == "OP2147_2_R2FR" and "Phi''(0)" in str(item["current_gain"]) for item in operator)
        and any(item["component_id"] == "OP2147_6_operator_verdict" for item in operator)
    )
    source_ok = (
        any(item["component_id"] == "SRCG2147_2_worldtube_identity" and "R_Hsrc" in str(item["blocker"]) for item in source)
        and any(item["component_id"] == "SRCG2147_3_measured_G" and "circular" in str(item["blocker"]) for item in source)
        and any(item["component_id"] == "SRCG2147_6_source_verdict" for item in source)
    )
    residuals_ok = any(item["residual_id"] == "RJ2147_4_join" and item["symbol"] == "R_join" for item in residuals)
    decisions_ok = (
        any(item["decision"] == "OPERATOR_GATE_FIRST" for item in decisions)
        and any(item["decision"] == "PHI_SECOND_DERIVATIVE_ZERO_OR_C2_SOURCE_NEXT" for item in decisions)
    )
    next_ok = any(item["route_id"] == "NEXT2147_0_2148" for item in next_rows)
    copies_ok = all(truthy(item["path_exists"]) and truthy(item["parse_ok"]) for item in copies)
    csv_ok = all(path.exists() and csv_rows_parse(path) for path in csv_paths)
    no_claim_flags = all(
        not truthy(item.get("claim_allowed", False)) and not truthy(item.get("valid_for_claim", False))
        for group in (sources, theorem, operator, source, residuals, decisions, next_rows, copies)
        for item in group
    )
    no_score_ready = all(not truthy(item.get("score_ready", False)) for item in residuals)
    formalization_clean = count_formalization_modified() == 0 and not formalization_has_2147_artifacts()
    pycache_clean = not (Path(__file__).resolve().parent / "__pycache__").exists()
    all_ok = all([sources_ok, theorem_ok, operator_ok, source_ok, residuals_ok, decisions_ok, next_ok, copies_ok, csv_ok, no_claim_flags, no_score_ready, formalization_clean, pycache_clean])
    checks = [
        ("VAL2147_00_sources", sources_ok, "2146, 2139-2144 and 1815-1823 source checkpoints validate"),
        ("VAL2147_01_theorem", theorem_ok, "two-gate local-GR theorem contract is written and nonclaim"),
        ("VAL2147_02_operator_gate", operator_ok, "operator gate contains Gamma_G and Phi''/R2FR live blockers"),
        ("VAL2147_03_source_gate", source_ok, "source gate contains R_Hsrc/measured-G circularity blockers"),
        ("VAL2147_04_residual_vector", residuals_ok, "R_join residual vector exists"),
        ("VAL2147_05_decisions", decisions_ok, "decision selects operator gate/Phi'' next"),
        ("VAL2147_06_next", next_ok, "next target is 2148 Phi'' zero or c2 source row"),
        ("VAL2147_07_branch_copies", copies_ok, "branch copies exist and parse"),
        ("VAL2147_08_csv_parse", csv_ok, "all generated CSVs parse cleanly"),
        ("VAL2147_09_no_claim_flags", no_claim_flags, "no generated row allows a claim"),
        ("VAL2147_10_not_score_ready", no_score_ready, "no residual vector row is score-ready"),
        ("VAL2147_11_formalization_clean", formalization_clean, "formalization-workbench untouched by 2147"),
        ("VAL2147_12_no_pycache", pycache_clean, "scripts __pycache__ removed"),
        ("VAL2147_OVERALL", all_ok, "2147 writes the local-GR two-gate source/operator join, keeps all claims blocked, and selects the Phi''/visible-c2 operator hinge next."),
    ]
    return [row(check_id=check_id, status="PASS" if passed else "FAIL", detail=detail) for check_id, passed, detail in checks]


def write_doc(
    sources: list[dict[str, object]],
    theorem: list[dict[str, object]],
    operator: list[dict[str, object]],
    source: list[dict[str, object]],
    residuals: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    copies: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    content = "\n\n".join(
        [
            "# 2147 - Y5/R2FR Local GR Two-Gate Spine Source Operator Join",
            "## Current Verdict",
            "2147 does **not** prove local GR, Newton, PPN, WEP, R10, or any public claim. It turns the scattered local-GR route into one explicit conditional theorem: MTS reduces to local GR/Newton only if the **operator gate** and the **source gate** both close.",
            "The operator gate is `EH/Gamma_G/R2FR/connection/extra-sector/conservation` silence or boundedness. The source gate is `Hilbert-Hamiltonian/worldtube/measured-G/readout/arena projection` equality or boundedness. Their failure modes are combined in the residual vector `R_join = R_op + R_source + R_readout + R_current`.",
            "The important strategic decision is order: attack the operator gate first. A beautiful source bridge is still not enough if the exterior operator carries a live R2/fR scalar mode. The least circular next hinge is therefore `Phi''(0)=0` for the primitive deficit response, or else a visible `c2` finite residual row.",
            "## Source Register",
            md_table(sources, ["source_id", "source_path", "path_exists", "needles_found", "role", "valid_for_claim"]),
            "## Two-Gate Theorem Contract",
            md_table(theorem, ["theorem_id", "clause", "statement", "required_evidence", "current_status", "valid_for_claim"]),
            "## Operator Gate",
            md_table(operator, ["component_id", "component", "current_gain", "blocker", "closure_condition", "valid_for_claim"]),
            "## Source Gate",
            md_table(source, ["component_id", "component", "current_gain", "blocker", "closure_condition", "valid_for_claim"]),
            "## Join Residual Vector",
            md_table(residuals, ["residual_id", "symbol", "definition", "source_gate", "current_status", "score_ready", "valid_for_claim"]),
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
    theorem = two_gate_theorem_rows()
    operator = operator_gate_rows()
    source = source_gate_rows()
    residuals = join_residual_rows()
    decisions = decision_rows()
    next_rows = next_target_rows()

    paths = {
        "sources": OUT / "P8_Y5_PARENT_QLOC_2147_SOURCE_REGISTER.csv",
        "theorem": OUT / "P8_Y5_PARENT_QLOC_2147_TWO_GATE_THEOREM.csv",
        "operator": OUT / "P8_Y5_PARENT_QLOC_2147_OPERATOR_GATE.csv",
        "source": OUT / "P8_Y5_PARENT_QLOC_2147_SOURCE_GATE.csv",
        "residuals": OUT / "P8_Y5_PARENT_QLOC_2147_JOIN_RESIDUAL_VECTOR.csv",
        "decisions": OUT / "P8_Y5_PARENT_QLOC_2147_DECISION_LEDGER.csv",
        "next": OUT / "P8_Y5_PARENT_QLOC_2147_NEXT_TARGET.csv",
        "branch_copies": OUT / "P8_Y5_PARENT_QLOC_2147_BRANCH_COPIES.csv",
        "validation": OUT / "P8_Y5_BRR545_2147_VALIDATION.csv",
    }

    write_csv(paths["sources"], sources)
    write_csv(paths["theorem"], theorem)
    write_csv(paths["operator"], operator)
    write_csv(paths["source"], source)
    write_csv(paths["residuals"], residuals)
    write_csv(paths["decisions"], decisions)
    write_csv(paths["next"], next_rows)

    copies = write_branch_copies(theorem, operator, source, residuals, next_rows)
    write_csv(paths["branch_copies"], copies)

    remove_pycache()
    csv_paths = [path for key, path in paths.items() if key != "validation"] + [Path(str(copy["destination"])) for copy in copies]
    validation = validation_rows(sources, theorem, operator, source, residuals, decisions, next_rows, copies, csv_paths)
    write_csv(paths["validation"], validation)
    write_doc(sources, theorem, operator, source, residuals, decisions, next_rows, copies, validation)

    print(f"wrote {DOC}")
    print(f"validation {paths['validation']}")


if __name__ == "__main__":
    main()
