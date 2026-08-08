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


DOC = ROOT / "2141-Y5-R2FR-GammaG-functional-contract-or-local-kernel-zero-proof.md"
REPO = ROOT.parent
FORMALIZATION = REPO / "formalization-workbench"

DOC_2140 = ROOT / "2140-Y5-R2FR-GammaG-metric-variation-local-silence-or-residual-row.md"
CSV_2140_VAL = OUT / "P8_Y5_BRR545_2140_VALIDATION.csv"
CSV_2140_THEORY = OUT / "P8_Y5_PARENT_QLOC_2140_GAMMAG_VARIATION_IDENTITIES.csv"
CSV_2140_RESIDUAL = OUT / "P8_Y5_PARENT_QLOC_2140_GAMMAG_RESIDUAL_ROWS.csv"
CSV_2140_NEXT = OUT / "P8_Y5_PARENT_QLOC_2140_NEXT_TARGET.csv"

GRAVITY_CORE = REPO / "core-mts-framework" / "gravity" / "motion-timespace-mts-gravity-core-unified-formulation.md"
GRAVITY_SUMMARY = REPO / "core-mts-framework" / "gravity" / "motion-timespace-mts-gravity.md"
ACTION_PRINCIPLE = REPO / "core-mts-framework" / "action-principle" / "the-motion-timespace-action-principle.md"


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


def formalization_has_2141_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    patterns = (
        "*2141-Y5-R2FR*",
        "*P8_Y5_PARENT_QLOC_2141*",
        "*Y5_R2FR_GammaG_functional_contract_or_local_kernel_zero_proof_2141*",
        "*AFRAME_GAMMAG_FUNCTIONAL_CONTRACT_2141*",
        "*JR2141*",
    )
    try:
        return any(path.is_file() for pattern in patterns for path in FORMALIZATION.rglob(pattern))
    except Exception:
        return False


def source_register_rows() -> list[dict[str, object]]:
    specs = [
        (
            "SRC2141_00_2140_doc",
            DOC_2140,
            [["Current Verdict"], ["D_Gamma"], ["functional/kernel proof"]],
            "2140 requires a Gamma_G parent functional or finite residual branch.",
        ),
        (
            "SRC2141_01_2140_validation",
            CSV_2140_VAL,
            [["VAL2140_OVERALL"], ["PASS"], ["functional/kernel proof"]],
            "2140 validation passed.",
        ),
        (
            "SRC2141_02_2140_theory",
            CSV_2140_THEORY,
            [["GVAR2140_4_fR_countermodel"], ["NONLOCAL_RESIDUAL_CONTRACT"], ["SILENCE_PROOF_NOT_CLOSED"]],
            "2140 variation identities and countermodel.",
        ),
        (
            "SRC2141_03_2140_residual",
            CSV_2140_RESIDUAL,
            [["GRES2140_0_DGamma_tensor"], ["MISSING_PARENT_FUNCTIONAL"], ["GRES2140_4_decision"]],
            "2140 finite residual rows.",
        ),
        (
            "SRC2141_04_2140_next",
            CSV_2140_NEXT,
            [["NEXT2140_0_2141"], ["Gamma_G[g,psi,history]"], ["kernel-zero-proof", "kernel silence", "functional contract"]],
            "2140 handoff to this functional contract.",
        ),
        (
            "SRC2141_05_gravity_core",
            GRAVITY_CORE,
            [["scalar curvature–response functional", "scalar curvature-response functional"], ["𝓢 ≡ 𝓢(K, ∇K, Φ)"], ["Γ_G(a) ≡ 𝓢(K_FLRW(a))"]],
            "core gravity file defines the saturation-response functional and its FLRW Gamma_G projection.",
        ),
        (
            "SRC2141_06_gravity_summary",
            GRAVITY_SUMMARY,
            [["𝓢 → 0"], ["K_solar"], ["𝓢 ≈ K^m"], ["not a higher-derivative modification of the action"]],
            "one-page gravity summary gives weak-field scaling and flags the algebraic/non-action branch.",
        ),
        (
            "SRC2141_07_action_principle",
            ACTION_PRINCIPLE,
            [["scalar functional of the smoothed curvature"], ["independent of metric variation"], ["L_{Λκ}"]],
            "action-principle file creates the tension between action variation and functional dependence.",
        ),
    ]
    rows: list[dict[str, object]] = []
    for source_id, path, needle_groups, role in specs:
        exists = path.exists()
        text = read_text(path) if exists else ""
        groups_found = exists and all(has_any(text, alternatives) for alternatives in needle_groups)
        rows.append(
            row(
                source_id=source_id,
                source_path=str(path),
                path_exists=exists,
                needles_found=groups_found,
                role=role,
                expected_needles="; ".join(" OR ".join(group) for group in needle_groups),
            )
        )
    return rows


def source_anchor_rows() -> list[dict[str, object]]:
    anchors = [
        ("ANCH2141_0_S_def", GRAVITY_CORE, ["𝓢 ≡ 𝓢(K, ∇K, Φ)"], "single controlling scalar"),
        ("ANCH2141_1_S_weak", GRAVITY_SUMMARY, ["𝓢 → 0"], "weak-curvature vanishing condition"),
        ("ANCH2141_2_S_minimal", GRAVITY_SUMMARY, ["K^m / (1 + K^m)"], "minimal saturation form"),
        ("ANCH2141_3_algebraic_branch", GRAVITY_SUMMARY, ["not a higher-derivative modification of the action"], "non-action/algebraic response warning"),
        ("ANCH2141_4_FLRW_projection", GRAVITY_CORE, ["Γ_G(a) ≡ 𝓢(K_FLRW(a))"], "Gamma_G as homogeneous saturation projection"),
        ("ANCH2141_5_PPN_anchor", GRAVITY_SUMMARY, ["K_solar"], "weak-field PPN scaling anchor"),
        ("ANCH2141_6_action_tension", ACTION_PRINCIPLE, ["independent of metric variation"], "action variation assumption"),
    ]
    rows: list[dict[str, object]] = []
    for anchor_id, path, needles, role in anchors:
        line_number, snippet = find_line(path, needles)
        rows.append(row(anchor_id=anchor_id, source_path=str(path), line_number=line_number, snippet=snippet, role=role))
    return rows


def functional_contract_rows() -> list[dict[str, object]]:
    return [
        row(contract_id="GC2141_0_parent_scalar", object="saturation response", contract="Define a parent scalar S=𝓢(K, nabla K, Phi) with K=R_abcd R^abcd in a fixed normalized unit convention, Phi the curvature-tension proxy, and all smoothing/projector choices explicit.", source_status="SOURCE_SKELETON_FOUND", proof_status="PARTIAL_CONTRACT"),
        row(contract_id="GC2141_1_minimal_form", object="minimal sourced ansatz", contract="𝓢 = K^m/(1+K^m) + ell^2(nabla_a K nabla^a K)/(1+K^m) + eta Phi^2, with m>=2.", source_status="SOURCE_FORM_FOUND", proof_status="DIMENSION_NORMALIZATION_OPEN"),
        row(contract_id="GC2141_2_FLRW_projection", object="Gamma_G projection", contract="Gamma_G(a)=P_FLRW[𝓢]=𝓢(K_FLRW(a),0,0).", source_status="SOURCE_FOUND", proof_status="HOMOGENEOUS_PROJECTION_FOUND"),
        row(contract_id="GC2141_3_local_projection", object="local compact projection", contract="Gamma_loc[U]=P_loc[𝓢] must specify whether local weak-field systems use exact flat-kernel silence, small finite saturation, or an environmental subtraction.", source_status="NOT_SOURCE_LOCKED", proof_status="MISSING_LOCAL_PROJECTOR"),
        row(contract_id="GC2141_4_action_branch", object="action-derived branch", contract="If 𝓢 or Gamma_G appears inside the action and depends on K, its metric variation produces D_S^{mu nu} unless the local kernel is stationary.", source_status="DERIVED_FROM_2140", proof_status="RESIDUAL_REQUIRED_UNLESS_DOUBLE_ZERO"),
        row(contract_id="GC2141_5_constitutive_branch", object="algebraic response branch", contract="If 𝓢 is imposed after variation as a constitutive geometric response, the higher-derivative action residual is avoided, but Bianchi/conservation must be closed by an exchange current or constraint.", source_status="SOURCE_HINT_FOUND", proof_status="CONSERVATION_CLOSURE_OPEN"),
        row(contract_id="GC2141_6_verdict", object="Gamma_G parent contract", contract="The corpus now supplies a plausible parent skeleton S(K,nablaK,Phi) and FLRW projection, but not the local projector, normalization, action-vs-constitutive decision, or conservation closure.", source_status="PROGRESS_NOT_CLAIM", proof_status="FUNCTIONAL_CONTRACT_PARTIAL"),
    ]


def double_zero_rows() -> list[dict[str, object]]:
    return [
        row(theorem_id="DZ2141_0_value_zero", clause="zeroth-order silence", statement="For the sourced minimal form with m>0, 𝓢(0,0,0)=0.", status="EXACT_CONDITIONAL_THEOREM", consequence="flat-kernel algebraic Gamma term vanishes"),
        row(theorem_id="DZ2141_1_K_first_derivative", clause="K derivative", statement="For f(K)=K^m/(1+K^m), f_K(0)=0 when m>1; the sourced m>=2 condition therefore gives a first-variation zero in the K-channel at K=0.", status="EXACT_DOUBLE_ZERO_CONDITIONAL", consequence="this is the first genuine double-zero mechanism found so far"),
        row(theorem_id="DZ2141_2_gradient_derivative", clause="gradient derivative", statement="The ell^2(nablaK)^2/(1+K^m) term has first derivative zero at nablaK=0, ignoring boundary/support effects.", status="EXACT_LOCAL_POINTWISE_CONDITIONAL", consequence="gradient channel is silent at a flat stationary kernel"),
        row(theorem_id="DZ2141_3_Phi_derivative", clause="Phi derivative", statement="The eta Phi^2 term has first derivative zero at Phi=0.", status="EXACT_LOCAL_POINTWISE_CONDITIONAL", consequence="curvature-tension channel is silent at zero Phi"),
        row(theorem_id="DZ2141_4_boundary_kernel", clause="boundary/history kernel", statement="The double-zero only becomes a local GR proof if the smoothing/history/projector kernel has no boundary contribution under compact local variations.", status="UNSIGNED_KERNEL_CLAUSE", consequence="no source-backed kernel theorem yet"),
        row(theorem_id="DZ2141_5_nonflat_system", clause="real local weak field", statement="For Solar-System-like K>0, first variation is not exactly zero; it is small/boundable as O(K^{m-1} deltaK) plus gradient/Phi terms.", status="FINITE_RESIDUAL_BOUND_BRANCH", consequence="PPN/local tests need bounds, not exact silence"),
        row(theorem_id="DZ2141_6_verdict", clause="local-kernel zero proof", statement="The sourced S-form gives an exact conditional double-zero at K=nablaK=Phi=0 with m>=2, but it does not prove exact silence for nonzero local sources.", status="CONDITIONAL_FLAT_KERNEL_PROOF_ONLY", consequence="use the theorem for the GR vacuum limit; use residual bounds for Solar System/source tests"),
    ]


def local_bound_rows() -> list[dict[str, object]]:
    return [
        row(bound_id="BND2141_0_small_value", quantity="𝓢_U", bound="If |K|<=epsilon_K, |nablaK|<=epsilon_grad, |Phi|<=epsilon_Phi, then |𝓢| <= C_K epsilon_K^m + C_grad ell^2 epsilon_grad^2 + eta epsilon_Phi^2 to leading order.", status="SYMBOLIC_BOUND_DERIVED", missing_input="normalization constants and local projector"),
        row(bound_id="BND2141_1_first_variation", quantity="D_S", bound="||D_S|| <= C1 m epsilon_K^(m-1)||DK|| + C2 ell^2 epsilon_grad||D(nablaK)|| + C3 eta epsilon_Phi||DPhi|| plus boundary terms.", status="SYMBOLIC_RESIDUAL_BOUND_DERIVED", missing_input="operator norms DK,DnablaK,DPhi and boundary kernel"),
        row(bound_id="BND2141_2_solar_anchor", quantity="Solar-System algebraic size", bound="source text states K_solar≈10^-61 in Planck units and 𝓢≈K^m<<10^-122 for m>=2.", status="SOURCE_ANCHOR_NONCLAIM", missing_input="full PPN residual calculation and unit-normalized K definition"),
        row(bound_id="BND2141_3_action_residual_size", quantity="action-derived D_S size", bound="For m=2 and nonzero K, the K-channel first variation scales like O(K deltaK), not O(K^2); this can still be tiny but must be bounded separately from the algebraic value.", status="IMPORTANT_SCRUTINY_FLAG", missing_input="deltaK scale for Solar-System perturbations"),
        row(bound_id="BND2141_4_bianchi_exchange", quantity="nabla^mu E_mu_nu", bound="dynamic/local nonconstant 𝓢 requires either an exchange current J_nu^S or a proof that gradients are negligible in the tested branch.", status="CONSERVATION_BOUND_OPEN", missing_input="J_nu^S or local gradient bound"),
        row(bound_id="BND2141_5_verdict", quantity="PPN/local readiness", bound="Current evidence supports a symbolic smallness route, not a numeric local-GR/PPN pass.", status="NUMERIC_BOUND_RUNNER_REQUIRED", missing_input="K, gradient, Phi normalization and local source bridge"),
    ]


def branch_rows() -> list[dict[str, object]]:
    return [
        row(branch_id="BR2141_0_action_parent", branch="action-derived parent field theory", benefit="best match to the ultimate unified-field goal", cost="must include higher-curvature variation residuals or prove double-zero/kernel silence", current_status="OPEN_HARD_ROUTE"),
        row(branch_id="BR2141_1_constitutive_response", branch="post-variation algebraic constitutive response", benefit="matches source text saying not a higher-derivative action modification", cost="less fundamental unless derived from parent micro-action/averaging; Bianchi current must be explicit", current_status="OPEN_EFFECTIVE_ROUTE"),
        row(branch_id="BR2141_2_external_cosmology", branch="external fitted Gamma_G(a)", benefit="usable for cosmology likelihoods", cost="not a parent field-theory derivation and cannot prove local GR", current_status="EMPIRICAL_ONLY_ROUTE"),
        row(branch_id="BR2141_3_best_next", branch="dual-track action/constitutive audit", benefit="prevents false choice while preserving derivability goal", cost="requires one more gate: either derive action residual cancellation or demote local branch to bounded constitutive closure", current_status="SELECTED_NEXT_ROUTE"),
    ]


def claim_gate_rows() -> list[dict[str, object]]:
    return [
        row(gate_id="GATE2141_0_sources", gate="2140 plus gravity source evidence validates", gate_pass=True, rationale="source register confirms 2140 handoff and S(K,nablaK,Phi) gravity files"),
        row(gate_id="GATE2141_1_functional_skeleton", gate="Gamma_G parent skeleton found", gate_pass=True, rationale="Gamma_G is sourced as FLRW projection of 𝓢(K_FLRW)"),
        row(gate_id="GATE2141_2_flat_kernel_double_zero", gate="flat local kernel double-zero condition derived", gate_pass=True, rationale="m>=2 makes value and first K-derivative vanish at K=nablaK=Phi=0"),
        row(gate_id="GATE2141_3_real_source_silence", gate="nonzero local source exact silence proved", gate_pass=False, rationale="Solar-System K is tiny but not zero, so residual bounds are needed"),
        row(gate_id="GATE2141_4_action_parent_closed", gate="action-derived parent branch closed", gate_pass=False, rationale="higher-curvature variation residual and boundary kernel remain open"),
        row(gate_id="GATE2141_5_conservation_closed", gate="Bianchi/conservation closure proved", gate_pass=False, rationale="constitutive response needs an explicit exchange current or local-gradient silence"),
        row(gate_id="GATE2141_6_local_GR_Newton_PPN_claim", gate="local GR/Newton/PPN claim allowed", gate_pass=False, rationale="only flat-kernel theorem and symbolic smallness are available; numeric/source-bridge gates remain open"),
    ]


def decision_rows() -> list[dict[str, object]]:
    return [
        row(decision_id="DEC2141_0", decision="PROMOTE_S_AS_PRIMARY_GAMMAG_PARENT_SKELETON", because="core gravity files source 𝓢(K,nablaK,Phi) and Gamma_G(a)=𝓢(K_FLRW(a))", next_action="use S as the Gamma_G contract object"),
        row(decision_id="DEC2141_1", decision="ACCEPT_FLAT_KERNEL_DOUBLE_ZERO_CONDITIONAL", because="minimal S with m>=2 gives S=0 and dS/dK=0 at K=nablaK=Phi=0", next_action="record as GR vacuum-limit theorem, not Solar-System proof"),
        row(decision_id="DEC2141_2", decision="KEEP_REAL_LOCAL_SYSTEMS_AS_BOUNDED_RESIDUALS", because="nonzero local curvature gives finite first variation even if extremely small", next_action="build numeric symbolic-to-PPN bound runner"),
        row(decision_id="DEC2141_3", decision="FORCE_ACTION_VS_CONSTITUTIVE_BRANCH_DECISION", because="source text conflicts: action principle varies Gamma_G, gravity summary says algebraic response not higher-derivative action", next_action="2142 branch decision and bound runner"),
    ]


def next_target_rows() -> list[dict[str, object]]:
    return [
        row(
            route_id="NEXT2141_0_2142",
            next_target="2142-Y5-R2FR-saturation-action-vs-constitutive-branch-and-PPN-bound-runner.md",
            script="scripts/Y5_R2FR_saturation_action_vs_constitutive_branch_and_PPN_bound_runner_2142.py",
            objective="Choose or formally split the action-derived and constitutive-response branches for 𝓢/Gamma_G, then turn the symbolic local bound into a nonclaim PPN/R10/source residual runner using K_solar, m>=2, gradient/Phi placeholders, and explicit Bianchi-current status.",
            forbidden_shortcuts="claiming Solar-System PPN pass from K^m alone; ignoring D_S scaling; hiding boundary kernel; treating constitutive response as a parent action; local-GR/Newton claim; formalization-workbench edits; GitHub action",
        )
    ]


def write_branch_copies(
    contract: list[dict[str, object]],
    double_zero: list[dict[str, object]],
    bounds: list[dict[str, object]],
    branches: list[dict[str, object]],
    next_rows: list[dict[str, object]],
) -> list[dict[str, object]]:
    copies = [
        ("COPY2141_0_source_weight_docs", SOURCE_WEIGHT_DOCS / "AFRAME_GAMMAG_FUNCTIONAL_CONTRACT_2141_NONCLAIM.csv", contract + double_zero + branches),
        ("COPY2141_1_branch_locked_wep", BRANCH_WEP / "P8_Y5_PARENT_QLOC_2141_LOCAL_BOUND_NONCLAIM.csv", double_zero + bounds),
        ("COPY2141_2_acquisition_queue", QUEUE / "JR2141_SATURATION_RESPONSE_BRANCH_AND_PPN_BOUND_QUEUE.csv", next_rows + bounds + branches),
    ]
    results: list[dict[str, object]] = []
    for copy_id, destination, rows_to_write in copies:
        write_csv(destination, rows_to_write)
        results.append(row(copy_id=copy_id, destination=str(destination), path_exists=destination.exists(), row_count=len(rows_to_write), parse_ok=csv_rows_parse(destination)))
    return results


def validation_rows(
    sources: list[dict[str, object]],
    anchors: list[dict[str, object]],
    contract: list[dict[str, object]],
    double_zero: list[dict[str, object]],
    bounds: list[dict[str, object]],
    branches: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    copies: list[dict[str, object]],
    csv_paths: list[Path],
) -> list[dict[str, object]]:
    sources_ok = all(truthy(item["path_exists"]) and truthy(item["needles_found"]) for item in sources)
    anchors_ok = all(int(item["line_number"]) > 0 for item in anchors)
    contract_ok = any(item["contract_id"] == "GC2141_6_verdict" and item["proof_status"] == "FUNCTIONAL_CONTRACT_PARTIAL" for item in contract)
    double_zero_ok = any(item["theorem_id"] == "DZ2141_6_verdict" and item["status"] == "CONDITIONAL_FLAT_KERNEL_PROOF_ONLY" for item in double_zero)
    bounds_ok = any(item["bound_id"] == "BND2141_5_verdict" and item["status"] == "NUMERIC_BOUND_RUNNER_REQUIRED" for item in bounds)
    branch_ok = any(item["branch_id"] == "BR2141_3_best_next" and item["current_status"] == "SELECTED_NEXT_ROUTE" for item in branches)
    gates_ok = any(item["gate_id"] == "GATE2141_2_flat_kernel_double_zero" and truthy(item["gate_pass"]) for item in gates) and any(item["gate_id"] == "GATE2141_6_local_GR_Newton_PPN_claim" and not truthy(item["gate_pass"]) for item in gates)
    decisions_ok = any(item["decision_id"] == "DEC2141_3" and item["decision"] == "FORCE_ACTION_VS_CONSTITUTIVE_BRANCH_DECISION" for item in decisions)
    next_ok = any(item["route_id"] == "NEXT2141_0_2142" for item in next_rows)
    copies_ok = all(truthy(item["path_exists"]) and truthy(item["parse_ok"]) for item in copies)
    csv_ok = all(path.exists() and csv_rows_parse(path) for path in csv_paths)
    no_claim_flags = all(
        not truthy(item.get("claim_allowed", False)) and not truthy(item.get("valid_for_claim", False))
        for group in (sources, anchors, contract, double_zero, bounds, branches, gates, decisions, next_rows, copies)
        for item in group
    )
    formalization_clean = count_formalization_modified() == 0 and not formalization_has_2141_artifacts()
    pycache_clean = not (Path(__file__).resolve().parent / "__pycache__").exists()
    all_ok = all([sources_ok, anchors_ok, contract_ok, double_zero_ok, bounds_ok, branch_ok, gates_ok, decisions_ok, next_ok, copies_ok, csv_ok, no_claim_flags, formalization_clean, pycache_clean])
    checks = [
        ("VAL2141_00_sources", sources_ok, "2140 and gravity/action source evidence validates"),
        ("VAL2141_01_anchors", anchors_ok, "line anchors for S/Gamma/action tension exist"),
        ("VAL2141_02_contract", contract_ok, "partial Gamma_G parent functional contract is recorded"),
        ("VAL2141_03_double_zero", double_zero_ok, "flat-kernel double-zero theorem is conditional only"),
        ("VAL2141_04_bounds", bounds_ok, "local weak-field residual bound route is staged"),
        ("VAL2141_05_branch", branch_ok, "action-vs-constitutive branch decision is selected next"),
        ("VAL2141_06_gates", gates_ok, "flat-kernel theorem passes while local-GR claim gate fails"),
        ("VAL2141_07_decisions", decisions_ok, "decision ledger forces next branch/bound gate"),
        ("VAL2141_08_next", next_ok, "next target is 2142"),
        ("VAL2141_09_branch_copies", copies_ok, "branch copies exist and parse"),
        ("VAL2141_10_csv_parse", csv_ok, "all generated CSVs parse cleanly"),
        ("VAL2141_11_no_claim_flags", no_claim_flags, "no generated row allows a claim"),
        ("VAL2141_12_formalization_clean", formalization_clean, "formalization-workbench untouched by 2141"),
        ("VAL2141_13_no_pycache", pycache_clean, "scripts __pycache__ removed"),
        ("VAL2141_OVERALL", all_ok, "2141 sources S(K,nablaK,Phi) as the Gamma_G parent skeleton, proves only a flat-kernel double-zero, keeps real local systems as bounded residuals, and selects the action-vs-constitutive/PPN bound runner next."),
    ]
    return [row(check_id=check_id, status="PASS" if passed else "FAIL", detail=detail) for check_id, passed, detail in checks]


def write_doc(
    sources: list[dict[str, object]],
    anchors: list[dict[str, object]],
    contract: list[dict[str, object]],
    double_zero: list[dict[str, object]],
    bounds: list[dict[str, object]],
    branches: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    copies: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    content = "\n\n".join(
        [
            "# 2141 - Y5/R2FR GammaG Functional Contract Or Local Kernel Zero Proof",
            "## Current Verdict",
            "2141 finds the best source-backed parent skeleton so far: the gravity files define a scalar saturation response `S=𝓢(K,nabla K,Phi)` and identify cosmological `Gamma_G(a)` as the FLRW projection `𝓢(K_FLRW(a))`. This is a real improvement over treating `Gamma_G` as a loose empirical fit.",
            "The good news is mathematical: the sourced `m>=2` saturation form gives a genuine flat-kernel double-zero. At `K=0`, `nabla K=0`, and `Phi=0`, the value and first variation of the minimal response vanish. That is a conditional GR vacuum-limit theorem.",
            "The catch is equally important: Solar-System/source regions are weak but not exactly flat. There the residual is not zero; it is boundable. Also, the corpus has a branch tension: the action-principle route varies `Gamma_G`, while the gravity summary says the response is algebraic and not a higher-derivative action modification. The next step must decide or split those branches before any local-GR/PPN claim.",
            "## Source Register",
            md_table(sources, ["source_id", "source_path", "path_exists", "needles_found", "role", "valid_for_claim"]),
            "## Source Anchors",
            md_table(anchors, ["anchor_id", "source_path", "line_number", "snippet", "role", "valid_for_claim"]),
            "## Functional Contract",
            md_table(contract, ["contract_id", "object", "contract", "source_status", "proof_status", "valid_for_claim"]),
            "## Double-Zero Theorem",
            md_table(double_zero, ["theorem_id", "clause", "statement", "status", "consequence", "valid_for_claim"]),
            "## Local Bound Rows",
            md_table(bounds, ["bound_id", "quantity", "bound", "status", "missing_input", "valid_for_claim"]),
            "## Branch Rows",
            md_table(branches, ["branch_id", "branch", "benefit", "cost", "current_status", "valid_for_claim"]),
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
    anchors = source_anchor_rows()
    contract = functional_contract_rows()
    double_zero = double_zero_rows()
    bounds = local_bound_rows()
    branches = branch_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_rows = next_target_rows()

    paths = {
        "sources": OUT / "P8_Y5_PARENT_QLOC_2141_SOURCE_REGISTER.csv",
        "anchors": OUT / "P8_Y5_PARENT_QLOC_2141_SOURCE_ANCHORS.csv",
        "contract": OUT / "P8_Y5_PARENT_QLOC_2141_GAMMAG_FUNCTIONAL_CONTRACT.csv",
        "double_zero": OUT / "P8_Y5_PARENT_QLOC_2141_DOUBLE_ZERO_THEOREM.csv",
        "bounds": OUT / "P8_Y5_PARENT_QLOC_2141_LOCAL_BOUND_ROWS.csv",
        "branches": OUT / "P8_Y5_PARENT_QLOC_2141_BRANCH_ROWS.csv",
        "gates": OUT / "P8_Y5_PARENT_QLOC_2141_CLAIM_GATES.csv",
        "decisions": OUT / "P8_Y5_PARENT_QLOC_2141_DECISION_LEDGER.csv",
        "next": OUT / "P8_Y5_PARENT_QLOC_2141_NEXT_TARGET.csv",
        "branch_copies": OUT / "P8_Y5_PARENT_QLOC_2141_BRANCH_COPIES.csv",
        "validation": OUT / "P8_Y5_BRR545_2141_VALIDATION.csv",
    }

    write_csv(paths["sources"], sources)
    write_csv(paths["anchors"], anchors)
    write_csv(paths["contract"], contract)
    write_csv(paths["double_zero"], double_zero)
    write_csv(paths["bounds"], bounds)
    write_csv(paths["branches"], branches)
    write_csv(paths["gates"], gates)
    write_csv(paths["decisions"], decisions)
    write_csv(paths["next"], next_rows)

    copies = write_branch_copies(contract, double_zero, bounds, branches, next_rows)
    write_csv(paths["branch_copies"], copies)

    remove_pycache()
    csv_paths = [path for key, path in paths.items() if key != "validation"] + [Path(str(copy["destination"])) for copy in copies]
    validation = validation_rows(sources, anchors, contract, double_zero, bounds, branches, gates, decisions, next_rows, copies, csv_paths)
    write_csv(paths["validation"], validation)
    write_doc(sources, anchors, contract, double_zero, bounds, branches, gates, decisions, next_rows, copies, validation)

    print(f"wrote {DOC}")
    print(f"validation {paths['validation']}")


if __name__ == "__main__":
    main()
