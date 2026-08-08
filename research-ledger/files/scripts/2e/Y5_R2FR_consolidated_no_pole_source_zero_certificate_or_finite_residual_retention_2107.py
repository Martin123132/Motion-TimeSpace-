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


DOC = ROOT / "2107-Y5-R2FR-consolidated-no-pole-source-zero-certificate-or-finite-residual-retention.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
SCRIPT_PATH = Path(__file__).resolve()

SRC_2106_DOC = ROOT / "2106-Y5-R2FR-ZX-MX2-parent-Hessian-source-row-or-no-pole-return.md"
CSV_2106_NOPOLE = OUT / "P8_Y5_PARENT_QLOC_2106_NO_POLE_RETURN_LEDGER.csv"
CSV_2106_EXTRACTION = OUT / "P8_Y5_PARENT_QLOC_2106_EXTRACTION_MATRIX.csv"
CSV_2106_GATES = OUT / "P8_Y5_PARENT_QLOC_2106_CLAIM_GATES.csv"
CSV_2106_VAL = OUT / "P8_Y5_BRR545_2106_VALIDATION.csv"

SRC_1845_DOC = ROOT / "1845-Y5-R2FR-vertical-quotient-LX-construction-or-scalar-nohair-branch-choice.md"
SRC_1023_DOC = ROOT / "1023-Y5-R10-q-vX-action-descent-certificate-or-scalar-nohair-demotion.md"
SRC_2035_DOC = ROOT / "2035-Y5-R2FR-quotient-factorisation-exhaustion-or-row-null-hessian-source.md"
SRC_1044_DOC = ROOT / "1044-Y5-R10-matter-pullback-JX-zero-or-qbarXT-bound-row.md"
SRC_1045_DOC = ROOT / "1045-Y5-R10-parent-matter-functor-descent-signature-or-qbar-component-fill.md"
SRC_1046_DOC = ROOT / "1046-Y5-R10-no-shadow-frame-constant-marker-theorem-or-qbar-marker-coefficients.md"

CSV_581_TEMPLATE = OUT / "P8_Y5_R10_581_NO_POLE_CERTIFICATE_TEMPLATE.csv"
CSV_618_SOURCE_ZERO = OUT / "P8_Y5_R10_618_SOURCE_ZERO_CERTIFICATE_AUDIT.csv"
CSV_670_CHAIN = OUT / "P8_Y5_R10_670_NO_POLE_QUOTIENT_PROOF_CHAIN.csv"
CSV_1848_RETURN = OUT / "P8_Y5_PARENT_QLOC_1848_SOURCE_ZERO_RETURN.csv"
CSV_1849_AUDIT = OUT / "P8_Y5_PARENT_QLOC_1849_SOURCE_ZERO_PROOF_AUDIT.csv"


def row(**kwargs: object) -> dict[str, object]:
    data = base_row()
    data["claim_allowed"] = False
    data.update(kwargs)
    return data


def truthy(value: object) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"true", "1", "yes", "pass", "valid", "claim_allowed", "selected"}


def formalization_has_2107_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    patterns = (
        "*2107-Y5-R2FR*",
        "*P8_Y5_PARENT_QLOC_2107*",
        "*Y5_R2FR_consolidated_no_pole_source_zero_certificate_or_finite_residual_retention_2107*",
        "*AFRAME_NO_POLE_SOURCE_ZERO_2107*",
        "*JR2107_PARENT_ACTION*",
    )
    try:
        return any(path.is_file() for pattern in patterns for path in FORMALIZATION.rglob(pattern))
    except Exception:
        return False


def source_register_rows() -> list[dict[str, object]]:
    specs: list[tuple[str, Path, list[str], str]] = [
        (
            "SRC2107_00_2106_doc",
            SRC_2106_DOC,
            ["NEXT2106_0_2107", "RETURN_TO_NO_POLE_SOURCE_ZERO_CERTIFICATE", "VAL2106_OVERALL"],
            "2106 selects this consolidated no-pole/source-zero certificate after finite Hessian scoring fails.",
        ),
        (
            "SRC2107_01_2106_no_pole",
            CSV_2106_NOPOLE,
            ["NPR2106_1_no_pole_route", "NPR2106_3_required_certificate", "BEST_GR_LIKE_ROUTE"],
            "2106 required-certificate row lists the structural clauses that must close together.",
        ),
        (
            "SRC2107_02_2106_extraction",
            CSV_2106_EXTRACTION,
            ["EXM2106_0_ZX", "MISSING_ZX", "NO_VALID_SOURCE_ROW_FOUND"],
            "2106 extraction matrix keeps the finite Hessian/source rows missing.",
        ),
        (
            "SRC2107_03_2106_gates",
            CSV_2106_GATES,
            ["GATE2106_6_no_pole_return", "GATE2106_7_local_GR", "False"],
            "2106 gate table blocks local-GR promotion and routes to no-pole work.",
        ),
        (
            "SRC2107_04_2106_validation",
            CSV_2106_VAL,
            ["VAL2106_OVERALL", "PASS", "no-pole/source-zero certificate"],
            "2106 validation passed with no formalization-workbench modification.",
        ),
        (
            "SRC2107_05_1845_qvc",
            SRC_1845_DOC,
            ["QVC1845_4_vertical_action", "QVC1845_8_verdict", "FAIL_CURRENT_CLAIM_DEMOTE_CURRENT_BRANCH"],
            "1845 gives the same single-certificate failure map in the active branch.",
        ),
        (
            "SRC2107_06_1023_certificate",
            SRC_1023_DOC,
            ["QVC1023_0_parent_q", "QVC1023_8_verdict", "DEM1023_0_scope"],
            "1023 demotes the quotient/vertical no-pole route to conditional-only until parent-signed.",
        ),
        (
            "SRC2107_07_2035_exhaustion",
            SRC_2035_DOC,
            ["EXH2035_8_verdict", "NO_VALID_SOURCE_ROW_FOUND", "DEC2035_0_exhaustion_result"],
            "2035 shows quotient-factorisation exhaustion is not derived and finite rows remain unsourced.",
        ),
        (
            "SRC2107_08_1044_matter_pullback",
            SRC_1044_DOC,
            ["delta_v S_T=0", "MPD1044_7_exact_theorem_if_signed", "Current verdict"],
            "1044 proves the matter-pullback zero as an exact conditional theorem but not a claim.",
        ),
        (
            "SRC2107_09_1045_matter_functor",
            SRC_1045_DOC,
            ["parent matter functor contract is now exact", "visible-geometry charge", "Current verdict"],
            "1045 supplies the conditional observed-coframe/matter-functor descent route.",
        ),
        (
            "SRC2107_10_1046_no_shadow",
            SRC_1046_DOC,
            ["no-shadow theorem is now exact", "NSF1046_1_conditional_chain_rule_zero", "Current verdict"],
            "1046 isolates constant/marker/shadow-frame channels that must be parent-excluded.",
        ),
        (
            "SRC2107_11_581_template",
            CSV_581_TEMPLATE,
            ["NPC581_0_configuration_space", "NPC581_6_claim_gate", "unfilled_certificate"],
            "581 no-pole template lists quotient, bulk, matter, rank, boundary and no-extension obligations.",
        ),
        (
            "SRC2107_12_618_source_zero",
            CSV_618_SOURCE_ZERO,
            ["SZ618_0_qbar_XT_chain_rule", "SZ618_5_full_source_zero_certificate", "finite_branch_retained"],
            "618 source-zero audit keeps source-zero nonclaim unless every zero route closes.",
        ),
        (
            "SRC2107_13_670_chain",
            CSV_670_CHAIN,
            ["NQ670_3_action_descent", "NQ670_5_matter_descent", "NQ670_6_constraint_generator"],
            "670 proof chain has the right mathematical sequence but missing parent closure.",
        ),
        (
            "SRC2107_14_1848_return",
            CSV_1848_RETURN,
            ["SZR1848_1_no_pole", "SZR1848_2_qbar_XT", "SZR1848_5_verdict"],
            "1848 already names no-pole/source-zero as the strongest route if closed.",
        ),
        (
            "SRC2107_15_1849_source_zero",
            CSV_1849_AUDIT,
            ["QZ1849_0_chain_rule", "QZ1849_6_verdict", "FAIL_CURRENT_CLAIM"],
            "1849 audits qbar/J source-zero and keeps a bounded source envelope mandatory.",
        ),
    ]
    rows: list[dict[str, object]] = []
    for source_id, path, needles, use in specs:
        exists = path.exists()
        text = read_text(path) if exists else ""
        rows.append(
            row(
                source_id=source_id,
                source_kind="2107_consolidated_no_pole_source_zero",
                source_path=str(path),
                path_exists=exists,
                needles="; ".join(needles),
                needle_found=exists and all(needle in text for needle in needles),
                use_in_2107=use,
                valid_for_claim=False,
            )
        )
    return rows


def consolidated_certificate_rows() -> list[dict[str, object]]:
    specs = [
        (
            "CERT2107_0_parent_q",
            "parent quotient map q",
            "q: Conf_parent -> Q_obs is canonical before readout and Dq[v_X]=0 for the actual local X direction.",
            "1023/1845/670 provide a conditional quotient kernel, not a parent-signed field map.",
            "PARTIAL_CONDITIONAL",
            "actual local X variations equal the parent null/relative-exact generator",
            "X is representative data rather than a physical local field",
        ),
        (
            "CERT2107_1_vertical_generator",
            "field-by-field v_X",
            "v_X is specified on metric/coframe, canonical data, memory/projector/domain fields, matter readout and boundary fields.",
            "1845 and 1023 both name this as missing; 590-style maps are not a complete active-branch transformation law.",
            "MISSING_PARENT_SIGNATURE",
            "one parent-owned transformation law on every field class",
            "DCdagger/Omega-flat language becomes a calculation rather than notation",
        ),
        (
            "CERT2107_2_action_descent",
            "parent action descent before variation",
            "S_parent[Phi]=S_red[q(Phi)] plus fixed silent boundary/topological terms before local variation.",
            "670 and 1023 supply conditional theorem shape; 2035 says quotient factorisation exhaustion is not derived.",
            "CONDITIONAL_ONLY",
            "explicit parent Lagrangian, object-language exhaustion and silent retained terms",
            "no independent X Hessian, Green function or K_X",
        ),
        (
            "CERT2107_3_matter_descent",
            "ordinary matter quotient functor",
            "S_matter=Sbar[Obs(q(Phi)), psi, theta_bar] with constants/material markers vertical-trivial.",
            "1044/1045 prove exact chain-rule zero if the functor descends; 1849 says parent functor/no-marker clauses remain unsigned.",
            "EXACT_CONDITIONAL_THEOREM_NOT_SIGNED",
            "parent matter category, observed coframe functor and no-marker constants theorem",
            "qbar_XT and J_matter vanish for ordinary matter",
        ),
        (
            "CERT2107_4_no_shadow_markers",
            "no representative Weyl/disformal/constant marker",
            "No legal matter frame, alpha_EM, mass, clock or material marker slot may depend on representative X.",
            "1046 gives the conditional no-shadow theorem but legal countermodels remain until excluded by the parent action.",
            "NOT_PARENT_EXCLUDED",
            "single-public-metric/no-extra-frame action-domain clause and constant superselection",
            "common-mode WEP silence cannot hide a scalar-tensor-like source",
        ),
        (
            "CERT2107_5_boundary_projector",
            "boundary, support and Hamiltonian projection silence",
            "Q_X=0/proper/exact, Pi_M^H[Q_X]=0 and no support/domain/source-normalization tail survives.",
            "581/618/1023/1849 all keep boundary/projector/source tails live.",
            "OPEN",
            "B_X primitive, edge differentiability, projector orthogonality, support silence and no cocycle",
            "Qbar_XH and hidden source tails vanish",
        ),
        (
            "CERT2107_6_constraint_rank",
            "degree count and reduced nondegeneracy",
            "A first-class pair removes the X canonical pair and reduced Omega has no proper X stabilizer.",
            "581/590-style contracts demand this, but the active branch has no rank/no-stabilizer computation.",
            "NOT_CHECKED",
            "rank calculation, bracket closure and reduced phase-space proof",
            "zero Hessian becomes gauge evidence rather than under-specified dynamics",
        ),
        (
            "CERT2107_7_no_pole_source_zero",
            "full no-pole/source-zero certificate",
            "CERT2107_0 through CERT2107_6 close together from the same parent branch.",
            "conditional pieces exist, but no single parent certificate closes in current corpus.",
            "FAIL_CURRENT_CLAIM",
            "same-branch q, v_X, action, matter, marker, boundary and degree certificates",
            "K_X=qbar_XT=Qbar_XH=0 and local X alpha inactive",
        ),
    ]
    return [
        row(
            certificate_id=certificate_id,
            clause=clause,
            required_statement=required_statement,
            current_evidence=current_evidence,
            status=status,
            missing_for_claim=missing_for_claim,
            if_closed=if_closed,
            valid_for_claim=False,
        )
        for certificate_id, clause, required_statement, current_evidence, status, missing_for_claim, if_closed in specs
    ]


def source_zero_clause_rows() -> list[dict[str, object]]:
    specs = [
        (
            "SZC2107_0_visible_geometry",
            "qbar_geom=0",
            "If e_obs=Obs_e(q(Phi)) and Dq[v_X]=0, then Lie_v e_obs=0 and the visible metric/coframe pullback source vanishes.",
            "EXACT_CONDITIONAL_THEOREM",
            "1044/1045",
            "blocked by unsigned q/v_X and observed coframe functor",
        ),
        (
            "SZC2107_1_matter_functor",
            "J_matter=0",
            "If ordinary matter only sees quotient-owned observed variables and fixed/gauge-owned lifts, then delta_v S_matter=0.",
            "EXACT_CONDITIONAL_THEOREM_NOT_PARENT_SIGNED",
            "1044/1849",
            "blocked by parent matter-category and lift ownership",
        ),
        (
            "SZC2107_2_marker_constants",
            "qbar_marker=qbar_constants=0",
            "If constants, EM labels, masses, clocks and material markers factor through q or are superselected, their vertical derivative vanishes.",
            "CONDITIONAL_THEOREM_COUNTERMODELS_REMAIN",
            "1046/1849",
            "blocked by alpha_EM(X), m_A(X), clock-ratio and material-marker countermodels",
        ),
        (
            "SZC2107_3_hidden_source_tail",
            "q_nonH/support/source-normalization tail=0",
            "No non-Hilbert current, support shift, domain projector or source-normalization residual may carry X.",
            "MISSING_HIDDEN_SOURCE_ZERO_OR_BOUND",
            "1849",
            "retain finite tail rows until sourced or theorem-zero",
        ),
        (
            "SZC2107_4_boundary_hamiltonian",
            "Qbar_XH=0",
            "Boundary charge is zero/exact/proper-gauge and the measured Hamiltonian projector has no X edge component.",
            "NOT_DERIVED",
            "581/618/1023/1848",
            "retain edge/Hamiltonian source rows",
        ),
        (
            "SZC2107_5_total_source_zero",
            "J_X=qbar_XT=Qbar_XH=0",
            "All visible, marker, hidden-tail and boundary channels close on the same parent branch.",
            "FAIL_CURRENT_CLAIM",
            "618/1849/2106",
            "finite residual envelope remains mandatory",
        ),
    ]
    return [
        row(
            zero_id=zero_id,
            target_zero=target_zero,
            theorem_or_condition=theorem_or_condition,
            current_status=current_status,
            source_family=source_family,
            blocker=blocker,
            valid_for_claim=False,
        )
        for zero_id, target_zero, theorem_or_condition, current_status, source_family, blocker in specs
    ]


def finite_residual_retention_rows() -> list[dict[str, object]]:
    specs = [
        ("FRR2107_0_ZX", "Z_X", "canonical kinetic Hessian coefficient for Xhat", "MISSING_ZX", "needed to score finite alpha_eff=N_X c_g", "2105/2106"),
        ("FRR2107_1_MX2", "M_X^2", "same-branch local mass/range Hessian coefficient", "MISSING_MX2", "needed for lambda_X and finite-range PPN/R10 response", "2105/2106"),
        ("FRR2107_2_KX", "K_X", "physical X Green-function/propagator kernel", "NO_POLE_NOT_PROVED", "must be zero by no-pole theorem or finite source-backed row", "581/618/670"),
        ("FRR2107_3_qbarXT", "qbar_XT", "ordinary matter/source coupling to local X direction", "SOURCE_ZERO_NOT_PROMOTED", "must be theorem-zero or source-backed component envelope", "1044/1849"),
        ("FRR2107_4_QbarXH", "Qbar_XH", "boundary/Hamiltonian projection of X source charge", "BOUNDARY_ZERO_NOT_DERIVED", "must be theorem-zero or bounded by local arena rows", "618/1848/1849"),
        ("FRR2107_5_frame_markers", "b_conf,b_dis,b_alpha,b_m,b_clock", "representative frame/constants/marker leakage", "NO_SHADOW_NOT_PARENT_SIGNED", "must be parent-excluded or bounded arena-by-arena", "1046"),
        ("FRR2107_6_tails", "q_nonH, support, domain, edge tails", "non-Hilbert/source/domain/boundary residual vector", "MISSING_HIDDEN_SOURCE_ZERO_OR_BOUND", "must be retained with no-cancellation absolute-sum policy", "1849/2106"),
        ("FRR2107_7_arena_response", "tau_R10,tau_PPN,tau_clock,tau_orbital", "local test response/projection factors", "MISSING_ARENA_PROJECTION", "needed before any empirical local-GR pass/fail score", "627/2106"),
    ]
    return [
        row(
            residual_id=residual_id,
            retained_quantity=retained_quantity,
            meaning=meaning,
            current_status=current_status,
            why_retained=why_retained,
            source_family=source_family,
            valid_for_claim=False,
        )
        for residual_id, retained_quantity, meaning, current_status, why_retained, source_family in specs
    ]


def gate_rows() -> list[dict[str, object]]:
    specs = [
        ("GATE2107_0_certificate_shape", "consolidated certificate contract is written", True, "q, v_X, action, matter, marker, boundary and degree clauses are now in one gate"),
        ("GATE2107_1_parent_q_vX", "parent q and field-by-field v_X are signed", False, "vertical generator remains missing on full field inventory"),
        ("GATE2107_2_action_descent", "parent action descends before variation", False, "action factorisation/exhaustion remains conditional"),
        ("GATE2107_3_matter_marker_descent", "matter, constants and no-shadow markers descend", False, "exact chain-rule theorems are not parent-signed"),
        ("GATE2107_4_boundary_degree", "boundary silence and degree count close", False, "boundary/projector and rank/no-stabilizer computations remain open"),
        ("GATE2107_5_source_zero", "J_X/qbar_XT/Qbar_XH theorem-zero follows", False, "one or more source-zero clauses fail current claim"),
        ("GATE2107_6_finite_residual_policy", "finite residual branch retained as nonclaim", True, "all missing local inputs are listed explicitly rather than hidden"),
        ("GATE2107_7_local_GR_Newton", "derived local GR/Newton limit follows", False, "no-pole/source-zero certificate is not parent-signed"),
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
            "DEC2107_0_theorem_shape",
            "CONSOLIDATED_CONDITIONAL_THEOREM_WRITTEN",
            "If the parent quotient, field-by-field v_X, action descent, matter/no-marker descent, boundary silence and degree count all close, then the local X pole/source is theorem-zero.",
            "This is the clean GR-like path: remove the extra local degree structurally, not by small-number fitting.",
        ),
        (
            "DEC2107_1_current_status",
            "NOT_PARENT_SIGNED_NO_LOCAL_GR_CLAIM",
            "The current corpus still lacks the single same-branch parent certificate; source-zero and no-pole remain conditional.",
            "Do not claim R10, WEP, PPN, clock, orbital or local-GR pass from 2107.",
        ),
        (
            "DEC2107_2_best_next",
            "FIELD_BY_FIELD_VX_PARENT_ACTION_SIGNATURE_FIRST",
            "The earliest hard blocker is the actual parent vertical generator/action signature; without it, matter and boundary zero proofs float.",
            "Try to construct the full v_X transformation law on every field class, then test action descent and boundary terms.",
        ),
        (
            "DEC2107_3_fallback",
            "FINITE_RESIDUAL_ROWS_RETAINED",
            "If the field-by-field generator cannot be sourced, the branch must remain an explicit finite residual acquisition problem.",
            "No cancellation; absolute-sum residual vector with sourced units and arena projections only.",
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
            route_id="NEXT2107_0_2108",
            next_target="2108-Y5-R2FR-field-by-field-vX-parent-action-signature-or-finite-tail-retention.md",
            script="scripts/Y5_R2FR_field_by_field_vX_parent_action_signature_or_finite_tail_retention_2108.py",
            objective="Construct or reject the actual parent vertical generator v_X on metric/coframe, canonical, memory/projector/domain, matter/readout and boundary fields; test whether the parent action is invariant/descended before variation; retain finite tails if any field block is unsigned.",
            forbidden_shortcuts="quotient by notation; WEP silence as matter blindness; boundary terms ignored; degree count skipped; invented zero K_X/qbar/Qbar; cancellation among residual tails",
            valid_for_claim=False,
        )
    ]


def write_branch_copies(
    certificate: list[dict[str, object]],
    source_zero: list[dict[str, object]],
    residuals: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_target: list[dict[str, object]],
) -> list[dict[str, object]]:
    copies = [
        (
            "COPY2107_0_source_weight_docs",
            SOURCE_WEIGHT_DOCS / "AFRAME_NO_POLE_SOURCE_ZERO_2107_NONCLAIM.csv",
            certificate + source_zero + decisions,
        ),
        (
            "COPY2107_1_branch_locked_wep",
            BRANCH_WEP / "P8_Y5_PARENT_QLOC_2107_NO_POLE_STATUS_NONCLAIM.csv",
            source_zero + residuals + gates,
        ),
        (
            "COPY2107_2_acquisition_queue",
            QUEUE / "JR2107_PARENT_ACTION_CERTIFICATE_NEXT_QUEUE.csv",
            residuals + next_target,
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
    certificate: list[dict[str, object]],
    source_zero: list[dict[str, object]],
    residuals: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_target: list[dict[str, object]],
    copies: list[dict[str, object]],
    csv_paths: list[Path],
) -> list[dict[str, object]]:
    sources_ok = all(truthy(source.get("path_exists")) and truthy(source.get("needle_found")) for source in sources)
    certificate_ok = (
        len(certificate) == 8
        and any(row_.get("certificate_id") == "CERT2107_7_no_pole_source_zero" and row_.get("status") == "FAIL_CURRENT_CLAIM" for row_ in certificate)
        and any(row_.get("certificate_id") == "CERT2107_1_vertical_generator" and row_.get("status") == "MISSING_PARENT_SIGNATURE" for row_ in certificate)
    )
    source_zero_ok = any(row_.get("zero_id") == "SZC2107_5_total_source_zero" and row_.get("current_status") == "FAIL_CURRENT_CLAIM" for row_ in source_zero)
    residuals_ok = len(residuals) >= 8 and all(not truthy(row_.get("valid_for_claim")) for row_ in residuals)
    gates_ok = (
        all(not truthy(row_.get("claim_allowed")) for row_ in gates)
        and any(row_.get("gate_id") == "GATE2107_7_local_GR_Newton" and not truthy(row_.get("gate_pass")) for row_ in gates)
        and any(row_.get("gate_id") == "GATE2107_6_finite_residual_policy" and truthy(row_.get("gate_pass")) for row_ in gates)
    )
    decision_ok = any(row_.get("decision") == "FIELD_BY_FIELD_VX_PARENT_ACTION_SIGNATURE_FIRST" for row_ in decisions)
    next_ok = any(row_.get("route_id") == "NEXT2107_0_2108" and "field-by-field-vX" in str(row_.get("next_target")) for row_ in next_target)
    copies_ok = len(copies) == 3 and all(truthy(row_.get("path_exists")) and truthy(row_.get("parse_ok")) for row_ in copies)
    csv_ok = all(path.exists() and csv_rows_parse(path) for path in csv_paths)
    no_claims = all(
        not truthy(row_.get("valid_for_claim")) and not truthy(row_.get("claim_allowed")) and not truthy(row_.get("score_ready"))
        for collection in (sources, certificate, source_zero, residuals, gates, decisions, next_target, copies)
        for row_ in collection
    )
    formalization_clean = count_formalization_modified() == 0 and not formalization_has_2107_artifacts()
    no_pycache = not (SCRIPT_PATH.parent / "__pycache__").exists()
    checks = [
        ("VAL2107_00_sources", sources_ok, "all cited source paths exist and contain the expected no-pole/source-zero needles"),
        ("VAL2107_01_certificate", certificate_ok, "consolidated certificate is complete but fails current claim at parent-signature clauses"),
        ("VAL2107_02_source_zero", source_zero_ok, "source-zero theorem is kept conditional and not promoted"),
        ("VAL2107_03_residual_retention", residuals_ok, "finite residual rows are retained explicitly as nonclaim acquisition objects"),
        ("VAL2107_04_claim_gates", gates_ok, "local-GR/Newton and source-zero gates remain blocked while residual-retention policy passes"),
        ("VAL2107_05_decision", decision_ok, "next route targets field-by-field v_X parent action signature first"),
        ("VAL2107_06_next", next_ok, "next target is 2108 field-by-field v_X/action-signature gate"),
        ("VAL2107_07_branch_copies", copies_ok, "branch copies exist and parse"),
        ("VAL2107_08_csv_parse", csv_ok, "all generated CSVs parse cleanly"),
        ("VAL2107_09_no_claim_flags", no_claims, "no generated row allows a claim or score"),
        ("VAL2107_10_formalization_clean", formalization_clean, "formalization-workbench untouched by 2107"),
        ("VAL2107_11_no_pycache", no_pycache, "scripts __pycache__ removed"),
    ]
    overall = all(ok for _, ok, _ in checks)
    checks.append(
        (
            "VAL2107_OVERALL",
            overall,
            "2107 consolidates the no-pole/source-zero certificate, rejects current local-GR promotion, and selects field-by-field v_X/action signature next",
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
    certificate: list[dict[str, object]],
    source_zero: list[dict[str, object]],
    residuals: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_target: list[dict[str, object]],
    copies: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    sections = [
        "# 2107 - Y5/R2FR Consolidated No-Pole Source-Zero Certificate Or Finite Residual Retention",
        "",
        "## Current Verdict",
        "",
        "2107 writes the cleanest available local-GR route as a single certificate. If the parent quotient map, the full field-by-field `v_X`, parent action descent, matter/no-marker descent, boundary/projector silence, and constraint degree count all close on the same branch, then the dangerous local `X` pole/source is not a physical degree of freedom.",
        "",
        "That theorem shape is good. It is the least post-hoc route because it removes the extra local source structurally instead of tuning `c_g`, `qbar_XT`, `Qbar_XH`, or `K_X` tiny. But the current corpus still does not parent-sign the certificate. The local branch therefore remains nonclaim: no R10, WEP, PPN, clock, orbital, Newton, or local-GR pass follows from 2107.",
        "",
        "The sharp missing object is now the actual parent vertical generator/action signature. Without a field-by-field `v_X` and action-descent proof, the matter and boundary zero lemmas are real but floating.",
        "",
        "## Source Register",
        md_table(sources, ["source_id", "source_path", "path_exists", "needle_found", "use_in_2107", "valid_for_claim"]),
        "## Consolidated Certificate",
        md_table(certificate, ["certificate_id", "clause", "status", "required_statement", "current_evidence", "missing_for_claim", "if_closed", "valid_for_claim"]),
        "## Source-Zero Clauses",
        md_table(source_zero, ["zero_id", "target_zero", "current_status", "theorem_or_condition", "source_family", "blocker", "valid_for_claim"]),
        "## Finite Residual Retention",
        md_table(residuals, ["residual_id", "retained_quantity", "current_status", "meaning", "why_retained", "source_family", "valid_for_claim"]),
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
    certificate = consolidated_certificate_rows()
    source_zero = source_zero_clause_rows()
    residuals = finite_residual_retention_rows()
    gates = gate_rows()
    decisions = decision_rows()
    next_target = next_rows()
    paths = {
        "sources": OUT / "P8_Y5_PARENT_QLOC_2107_SOURCE_REGISTER.csv",
        "certificate": OUT / "P8_Y5_PARENT_QLOC_2107_CONSOLIDATED_CERTIFICATE.csv",
        "source_zero": OUT / "P8_Y5_PARENT_QLOC_2107_SOURCE_ZERO_CLAUSES.csv",
        "residuals": OUT / "P8_Y5_PARENT_QLOC_2107_FINITE_RESIDUAL_RETENTION.csv",
        "gates": OUT / "P8_Y5_PARENT_QLOC_2107_CLAIM_GATES.csv",
        "decisions": OUT / "P8_Y5_PARENT_QLOC_2107_DECISION_LEDGER.csv",
        "next": OUT / "P8_Y5_PARENT_QLOC_2107_NEXT_TARGET.csv",
        "branch": OUT / "P8_Y5_PARENT_QLOC_2107_BRANCH_COPIES.csv",
        "validation": OUT / "P8_Y5_BRR545_2107_VALIDATION.csv",
    }
    write_csv(paths["sources"], sources)
    write_csv(paths["certificate"], certificate)
    write_csv(paths["source_zero"], source_zero)
    write_csv(paths["residuals"], residuals)
    write_csv(paths["gates"], gates)
    write_csv(paths["decisions"], decisions)
    write_csv(paths["next"], next_target)
    copies = write_branch_copies(certificate, source_zero, residuals, gates, decisions, next_target)
    write_csv(paths["branch"], copies)
    csv_paths = [path for key, path in paths.items() if key != "validation"] + [Path(str(r["destination"])) for r in copies]
    remove_pycache()
    validation = validation_rows(sources, certificate, source_zero, residuals, gates, decisions, next_target, copies, csv_paths)
    write_csv(paths["validation"], validation)
    write_doc(sources, certificate, source_zero, residuals, gates, decisions, next_target, copies, validation)
    remove_pycache()
    print(f"wrote {DOC}")
    print(f"validation {paths['validation']}")


if __name__ == "__main__":
    main()
