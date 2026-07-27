from __future__ import annotations

from decimal import Decimal, getcontext
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


getcontext().prec = 80

DOC = ROOT / "2142-Y5-R2FR-saturation-action-vs-constitutive-branch-and-PPN-bound-runner.md"
REPO = ROOT.parent
FORMALIZATION = REPO / "formalization-workbench"

DOC_2141 = ROOT / "2141-Y5-R2FR-GammaG-functional-contract-or-local-kernel-zero-proof.md"
CSV_2141_VAL = OUT / "P8_Y5_BRR545_2141_VALIDATION.csv"
CSV_2141_CONTRACT = OUT / "P8_Y5_PARENT_QLOC_2141_GAMMAG_FUNCTIONAL_CONTRACT.csv"
CSV_2141_DOUBLE_ZERO = OUT / "P8_Y5_PARENT_QLOC_2141_DOUBLE_ZERO_THEOREM.csv"
CSV_2141_BOUNDS = OUT / "P8_Y5_PARENT_QLOC_2141_LOCAL_BOUND_ROWS.csv"
CSV_2141_NEXT = OUT / "P8_Y5_PARENT_QLOC_2141_NEXT_TARGET.csv"

GRAVITY_SUMMARY = REPO / "core-mts-framework" / "gravity" / "motion-timespace-mts-gravity.md"
GRAVITY_CORE = REPO / "core-mts-framework" / "gravity" / "motion-timespace-mts-gravity-core-unified-formulation.md"
ACTION_PRINCIPLE = REPO / "core-mts-framework" / "action-principle" / "the-motion-timespace-action-principle.md"

K_SOLAR = Decimal("1e-61")
M_MIN = Decimal("2")
K_POWER = K_SOLAR ** int(M_MIN)
S_ALGEBRAIC = K_POWER / (Decimal(1) + K_POWER)
DS_DK_COEFF = M_MIN * (K_SOLAR ** (int(M_MIN) - 1)) / ((Decimal(1) + K_POWER) ** 2)


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


def dstr(value: Decimal) -> str:
    return f"{value:.6E}"


def formalization_has_2142_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    patterns = (
        "*2142-Y5-R2FR*",
        "*P8_Y5_PARENT_QLOC_2142*",
        "*Y5_R2FR_saturation_action_vs_constitutive_branch_and_PPN_bound_runner_2142*",
        "*AFRAME_SATURATION_BRANCH_2142*",
        "*JR2142*",
    )
    try:
        return any(path.is_file() for pattern in patterns for path in FORMALIZATION.rglob(pattern))
    except Exception:
        return False


def source_register_rows() -> list[dict[str, object]]:
    specs = [
        (
            "SRC2142_00_2141_doc",
            DOC_2141,
            [["Current Verdict"], ["flat-kernel double-zero"], ["action-principle route varies", "action-principle route"], ["PPN claim"]],
            "2141 establishes the double-zero but leaves real-source residual bounds open.",
        ),
        (
            "SRC2142_01_2141_validation",
            CSV_2141_VAL,
            [["VAL2141_OVERALL"], ["PASS"], ["PPN bound runner"]],
            "2141 validation passed and selects this branch/bound runner.",
        ),
        (
            "SRC2142_02_2141_contract",
            CSV_2141_CONTRACT,
            [["GC2141_4_action_branch"], ["GC2141_5_constitutive_branch"], ["FUNCTIONAL_CONTRACT_PARTIAL"]],
            "machine-readable action/constitutive branch tension.",
        ),
        (
            "SRC2142_03_2141_double_zero",
            CSV_2141_DOUBLE_ZERO,
            [["DZ2141_1_K_first_derivative"], ["EXACT_DOUBLE_ZERO_CONDITIONAL"], ["DZ2141_6_verdict"]],
            "machine-readable flat-kernel double-zero theorem.",
        ),
        (
            "SRC2142_04_2141_bounds",
            CSV_2141_BOUNDS,
            [["BND2141_2_solar_anchor"], ["BND2141_3_action_residual_size"], ["NUMERIC_BOUND_RUNNER_REQUIRED"]],
            "machine-readable symbolic local-bound route.",
        ),
        (
            "SRC2142_05_2141_next",
            CSV_2141_NEXT,
            [["NEXT2141_0_2142"], ["action-vs-constitutive"], ["K_solar"]],
            "2141 handoff to this bound runner.",
        ),
        (
            "SRC2142_06_gravity_summary",
            GRAVITY_SUMMARY,
            [["algebraic geometric response"], ["not a higher-derivative modification of the action"], ["K_solar"], ["𝓢 ≈ K^m"]],
            "gravity summary supplies the constitutive/algebraic reading and the Solar-System scaling anchor.",
        ),
        (
            "SRC2142_07_gravity_core",
            GRAVITY_CORE,
            [["𝓢 ≡ 𝓢(K, ∇K, Φ)"], ["Γ_G(a) ≡ 𝓢(K_FLRW(a))"]],
            "core gravity file supplies the parent saturation skeleton.",
        ),
        (
            "SRC2142_08_action_principle",
            ACTION_PRINCIPLE,
            [["L_{Λκ}"], ["independent of metric variation"], ["scalar functional of the smoothed curvature"]],
            "action-principle file supplies the action-derived branch tension.",
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
        ("ANCH2142_0_algebraic_response", GRAVITY_SUMMARY, ["algebraic geometric response"], "constitutive-response anchor"),
        ("ANCH2142_1_not_higher_action", GRAVITY_SUMMARY, ["not a higher-derivative modification of the action"], "not-action-warning anchor"),
        ("ANCH2142_2_no_higher_time", GRAVITY_SUMMARY, ["No higher-time derivatives in the action"], "stability/ghost claim anchor"),
        ("ANCH2142_3_K_solar", GRAVITY_SUMMARY, ["K_solar"], "Solar-System curvature scale anchor"),
        ("ANCH2142_4_S_small", GRAVITY_SUMMARY, ["𝓢 ≈ K^m"], "algebraic PPN smallness anchor"),
        ("ANCH2142_5_gamma_projection", GRAVITY_CORE, ["Γ_G(a) ≡ 𝓢(K_FLRW(a))"], "FLRW Gamma projection anchor"),
        ("ANCH2142_6_action_assumption", ACTION_PRINCIPLE, ["independent of metric variation"], "action variation assumption anchor"),
    ]
    rows: list[dict[str, object]] = []
    for anchor_id, path, needles, role in anchors:
        line_number, snippet = find_line(path, needles)
        rows.append(row(anchor_id=anchor_id, source_path=str(path), line_number=line_number, snippet=snippet, role=role))
    return rows


def branch_split_rows() -> list[dict[str, object]]:
    return [
        row(branch_id="BRS2142_0_action_parent", branch="action-derived parent saturation", source_basis="action principle has Gamma_G inside the action while calling it a curvature-history functional", mathematical_cost="must vary S(K,nablaK,Phi), generating D_S^{mu nu}, boundary kernels and possible higher-derivative terms", status="OPEN_HARD_ROUTE_NOT_CLAIM"),
        row(branch_id="BRS2142_1_constitutive_response", branch="post-variation algebraic/constitutive saturation", source_basis="gravity summary says the response is algebraic and not a higher-derivative action modification", mathematical_cost="must derive or postulate conservation/exchange current J^S_nu and parent micro-averaging", status="OPEN_EFFECTIVE_ROUTE_NOT_CLAIM"),
        row(branch_id="BRS2142_2_external_cosmology", branch="external fitted Gamma_G(a)", source_basis="cosmology uses Gamma_G(a) as a homogeneous fitted correction", mathematical_cost="empirical branch cannot prove local GR or parent derivation", status="EMPIRICAL_ROUTE_NOT_LOCAL_PROOF"),
        row(branch_id="BRS2142_3_formal_split", branch="formal split retained", source_basis="corpus contains both action and constitutive language", mathematical_cost="carry two ledgers until one is derived or demoted", status="SELECTED_DISCIPLINE"),
    ]


def bound_input_rows() -> list[dict[str, object]]:
    return [
        row(input_id="IN2142_0_K_solar", quantity="K_solar", value=dstr(K_SOLAR), units="Planck-normalized source claim", source_path=str(GRAVITY_SUMMARY), source_line=find_line(GRAVITY_SUMMARY, ["K_solar"])[0], status="SOURCE_ANCHOR"),
        row(input_id="IN2142_1_m_min", quantity="m_min", value=str(int(M_MIN)), units="dimensionless exponent", source_path=str(GRAVITY_SUMMARY), source_line=find_line(GRAVITY_SUMMARY, ["m ≥ 2"])[0], status="SOURCE_ANCHOR"),
        row(input_id="IN2142_2_gradK_bound", quantity="epsilon_grad", value="MISSING_PARENT_INPUT", units="normalized curvature-gradient bound", source_path="", source_line=0, status="BLOCKS_CLAIM"),
        row(input_id="IN2142_3_Phi_bound", quantity="epsilon_Phi", value="MISSING_PARENT_INPUT", units="curvature-tension proxy bound", source_path="", source_line=0, status="BLOCKS_CLAIM"),
        row(input_id="IN2142_4_deltaK_norm", quantity="||deltaK|| per allowed PPN variation", value="MISSING_PARENT_INPUT", units="operator norm", source_path="", source_line=0, status="BLOCKS_ACTION_BRANCH_CLAIM"),
        row(input_id="IN2142_5_boundary_kernel", quantity="Theta_S boundary/history kernel", value="MISSING_PARENT_INPUT", units="boundary functional", source_path="", source_line=0, status="BLOCKS_ACTION_BRANCH_CLAIM"),
        row(input_id="IN2142_6_exchange_current", quantity="J^S_nu", value="MISSING_PARENT_INPUT", units="conservation/exchange current", source_path="", source_line=0, status="BLOCKS_CONSTITUTIVE_BRANCH_CLAIM"),
        row(input_id="IN2142_7_source_bridge", quantity="M_H_ref/Q_tau/G_ref readout", value="MISSING_PARENT_INPUT", units="source-to-observable bridge", source_path="", source_line=0, status="BLOCKS_ALL_LOCAL_CLAIMS"),
    ]


def bound_runner_rows() -> list[dict[str, object]]:
    return [
        row(run_id="RUN2142_0_algebraic_value", branch="constitutive/direct algebraic", expression="S_K=K_solar^m/(1+K_solar^m)", numeric_value=dstr(S_ALGEBRAIC), status="NUMERIC_CORE_COMPUTED_NONCLAIM", interpretation="direct algebraic weak-field saturation is extremely small for m=2"),
        row(run_id="RUN2142_1_first_derivative_coeff", branch="action-derived K-channel", expression="d(K^m/(1+K^m))/dK at K_solar, m=2", numeric_value=dstr(DS_DK_COEFF), status="NUMERIC_COEFFICIENT_COMPUTED_NONCLAIM", interpretation="action residual scales with this coefficient times deltaK, not with K^2 alone"),
        row(run_id="RUN2142_2_action_residual_core", branch="action-derived K-channel", expression=f"|D_S^K| <= {dstr(DS_DK_COEFF)} * ||deltaK||", numeric_value="MISSING_DELTAK_NORM", status="BLOCKED_NONCLAIM", interpretation="cannot pass PPN/source tests without an allowed-variation/operator norm"),
        row(run_id="RUN2142_3_gradient_channel", branch="both", expression="ell^2 |nablaK|^2/(1+K^m) and variation term", numeric_value="MISSING_GRADK_ELL_OPERATOR", status="BLOCKED_NONCLAIM", interpretation="gradient channel may vanish in FLRW but needs local bound/source support"),
        row(run_id="RUN2142_4_phi_channel", branch="both", expression="eta Phi^2 and variation 2 eta Phi deltaPhi", numeric_value="MISSING_PHI_ETA_OPERATOR", status="BLOCKED_NONCLAIM", interpretation="curvature-tension proxy lacks normalized local bound"),
        row(run_id="RUN2142_5_constitutive_bianchi", branch="constitutive", expression="nabla^mu(G_mu_nu+S g_mu_nu)=kappa nabla^mu T_mu_nu requires J^S_nu or local gradient silence", numeric_value="MISSING_EXCHANGE_CURRENT", status="BLOCKED_NONCLAIM", interpretation="algebraic branch avoids action residual but still owes conservation closure"),
        row(run_id="RUN2142_6_runner_verdict", branch="all", expression="value smallness != claim", numeric_value="NO_CLAIM", status="LOCAL_BOUND_RUNNER_STAGED", interpretation="runner computes core smallness and exposes exact missing inputs"),
    ]


def arena_projection_rows() -> list[dict[str, object]]:
    return [
        row(arena_id="ARENA2142_0_PPN_value", arena="PPN weak-field", projected_quantity="gamma-1,beta-1 algebraic order", projection="O(S_K) ~ " + dstr(S_ALGEBRAIC), status="VALUE_SMALL_NONCLAIM", blocker="action residual/source bridge/external PPN thresholds not locked"),
        row(arena_id="ARENA2142_1_PPN_action", arena="PPN weak-field", projected_quantity="D_S residual", projection=f"O({dstr(DS_DK_COEFF)} * ||deltaK||) plus gradient/Phi/boundary", status="BLOCKED_NONCLAIM", blocker="deltaK norm and local source bridge missing"),
        row(arena_id="ARENA2142_2_R10", arena="R10 short-range/local gravity", projected_quantity="alpha(lambda) saturation residual", projection="requires map from S/D_S to alpha(lambda)", status="BLOCKED_NONCLAIM", blocker="arena projection and source bridge missing"),
        row(arena_id="ARENA2142_3_clocks", arena="clock/time tests", projected_quantity="tau residual", projection="requires map from S or J^S to clock observable", status="BLOCKED_NONCLAIM", blocker="tau_source/tau_clock bridge missing"),
        row(arena_id="ARENA2142_4_orbital", arena="orbital systems", projected_quantity="GM/orbital residual", projection="requires source-normalized curvature operator and exchange current", status="BLOCKED_NONCLAIM", blocker="M_H_ref/G_ref/Q_tau bridge missing"),
        row(arena_id="ARENA2142_5_cosmology", arena="FLRW cosmology", projected_quantity="Gamma_G(a)", projection="Gamma_G(a)=S(K_FLRW(a)) source skeleton exists", status="SOURCE_SKELETON_ONLY", blocker="empirical fit/parent normalization still separate"),
        row(arena_id="ARENA2142_6_verdict", arena="all local arenas", projected_quantity="claim status", projection="no local arena can be promoted from K^m smallness alone", status="CLAIM_BLOCKED", blocker="missing action residual, constitutive current, and source bridge"),
    ]


def claim_gate_rows() -> list[dict[str, object]]:
    return [
        row(gate_id="GATE2142_0_sources", gate="2141/source handoff validates", gate_pass=True, rationale="source register confirms 2141, gravity summary, gravity core, and action principle"),
        row(gate_id="GATE2142_1_branch_split", gate="action/constitutive branches formally split", gate_pass=True, rationale="2142 keeps both branches with distinct obligations"),
        row(gate_id="GATE2142_2_numeric_core", gate="numeric weak-field core bound computed", gate_pass=True, rationale=f"K_solar=1e-61 and m=2 give S_K={dstr(S_ALGEBRAIC)}"),
        row(gate_id="GATE2142_3_action_parent_claim", gate="action-derived branch claim allowed", gate_pass=False, rationale="deltaK/operator norm, boundary kernel, and higher-curvature residual closure missing"),
        row(gate_id="GATE2142_4_constitutive_claim", gate="constitutive branch claim allowed", gate_pass=False, rationale="Bianchi/exchange current and micro-averaging derivation missing"),
        row(gate_id="GATE2142_5_PPN_R10_claim", gate="PPN/R10 claim allowed", gate_pass=False, rationale="value smallness exists but source bridge, action residual, arena projection and external thresholds remain open"),
        row(gate_id="GATE2142_6_local_GR_Newton_claim", gate="local GR/Newton claim allowed", gate_pass=False, rationale="flat-kernel theorem and smallness runner do not prove sourced local equivalence to GR/Newton"),
    ]


def decision_rows() -> list[dict[str, object]]:
    return [
        row(decision_id="DEC2142_0", decision="FORMAL_BRANCH_SPLIT_NOT_SINGLE_CHOICE", because="corpus contains both action-derived and algebraic-response language", next_action="keep separate proof obligations"),
        row(decision_id="DEC2142_1", decision="NUMERIC_SMALLNESS_IS_REAL_BUT_NOT_ENOUGH", because=f"S_K={dstr(S_ALGEBRAIC)} but action residual coefficient is {dstr(DS_DK_COEFF)} times deltaK", next_action="derive deltaK/operator/source bridge"),
        row(decision_id="DEC2142_2", decision="CONSTITUTIVE_BRANCH_IS_EFFECTIVE_UNTIL_DERIVED", because="it matches no-higher-derivative source text but needs J^S_nu/Bianchi closure", next_action="derive exchange current or demote to closure"),
        row(decision_id="DEC2142_3", decision="NEXT_LOCAL_OPERATOR_SOURCE_BRIDGE", because="all local arenas now bottleneck on operator norms and source readout", next_action="2143 local curvature operator norm and source bridge bound"),
    ]


def next_target_rows() -> list[dict[str, object]]:
    return [
        row(
            route_id="NEXT2142_0_2143",
            next_target="2143-Y5-R2FR-local-curvature-operator-norm-and-source-bridge-bound.md",
            script="scripts/Y5_R2FR_local_curvature_operator_norm_and_source_bridge_bound_2143.py",
            objective="Derive or bound the local operator norms ||deltaK||, ||delta(nablaK)|| and ||deltaPhi|| for weak-field source variations, and connect them to M_H_ref/G_ref/Q_tau so the 2142 nonclaim PPN/R10 residual runner can become a sourced bound instead of a placeholder.",
            forbidden_shortcuts="using K^m value as action residual; omitting deltaK; omitting Bianchi current; skipping source bridge; local-GR/Newton/PPN/R10 claim; formalization-workbench edits; GitHub action",
        )
    ]


def write_branch_copies(
    branches: list[dict[str, object]],
    inputs: list[dict[str, object]],
    runner: list[dict[str, object]],
    arenas: list[dict[str, object]],
    next_rows: list[dict[str, object]],
) -> list[dict[str, object]]:
    copies = [
        ("COPY2142_0_source_weight_docs", SOURCE_WEIGHT_DOCS / "AFRAME_SATURATION_BRANCH_2142_NONCLAIM.csv", branches + runner + arenas),
        ("COPY2142_1_branch_locked_wep", BRANCH_WEP / "P8_Y5_PARENT_QLOC_2142_PPN_BOUND_RUNNER_NONCLAIM.csv", inputs + runner + arenas),
        ("COPY2142_2_acquisition_queue", QUEUE / "JR2142_LOCAL_OPERATOR_NORM_SOURCE_BRIDGE_QUEUE.csv", next_rows + inputs + arenas),
    ]
    results: list[dict[str, object]] = []
    for copy_id, destination, rows_to_write in copies:
        write_csv(destination, rows_to_write)
        results.append(row(copy_id=copy_id, destination=str(destination), path_exists=destination.exists(), row_count=len(rows_to_write), parse_ok=csv_rows_parse(destination)))
    return results


def validation_rows(
    sources: list[dict[str, object]],
    anchors: list[dict[str, object]],
    branches: list[dict[str, object]],
    inputs: list[dict[str, object]],
    runner: list[dict[str, object]],
    arenas: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    copies: list[dict[str, object]],
    csv_paths: list[Path],
) -> list[dict[str, object]]:
    sources_ok = all(truthy(item["path_exists"]) and truthy(item["needles_found"]) for item in sources)
    anchors_ok = all(int(item["line_number"]) > 0 for item in anchors)
    branch_ok = any(item["branch_id"] == "BRS2142_3_formal_split" and item["status"] == "SELECTED_DISCIPLINE" for item in branches)
    inputs_ok = any(item["input_id"] == "IN2142_0_K_solar" and item["value"] == dstr(K_SOLAR) for item in inputs) and any("MISSING_PARENT_INPUT" in str(item["value"]) for item in inputs)
    runner_ok = any(item["run_id"] == "RUN2142_0_algebraic_value" and item["numeric_value"] == dstr(S_ALGEBRAIC) for item in runner) and any(item["run_id"] == "RUN2142_2_action_residual_core" and item["status"] == "BLOCKED_NONCLAIM" for item in runner)
    arenas_ok = any(item["arena_id"] == "ARENA2142_6_verdict" and item["status"] == "CLAIM_BLOCKED" for item in arenas)
    gates_ok = any(item["gate_id"] == "GATE2142_2_numeric_core" and truthy(item["gate_pass"]) for item in gates) and any(item["gate_id"] == "GATE2142_6_local_GR_Newton_claim" and not truthy(item["gate_pass"]) for item in gates)
    decisions_ok = any(item["decision_id"] == "DEC2142_3" and item["decision"] == "NEXT_LOCAL_OPERATOR_SOURCE_BRIDGE" for item in decisions)
    next_ok = any(item["route_id"] == "NEXT2142_0_2143" for item in next_rows)
    copies_ok = all(truthy(item["path_exists"]) and truthy(item["parse_ok"]) for item in copies)
    csv_ok = all(path.exists() and csv_rows_parse(path) for path in csv_paths)
    no_claim_flags = all(
        not truthy(item.get("claim_allowed", False)) and not truthy(item.get("valid_for_claim", False))
        for group in (sources, anchors, branches, inputs, runner, arenas, gates, decisions, next_rows, copies)
        for item in group
    )
    formalization_clean = count_formalization_modified() == 0 and not formalization_has_2142_artifacts()
    pycache_clean = not (Path(__file__).resolve().parent / "__pycache__").exists()
    all_ok = all([sources_ok, anchors_ok, branch_ok, inputs_ok, runner_ok, arenas_ok, gates_ok, decisions_ok, next_ok, copies_ok, csv_ok, no_claim_flags, formalization_clean, pycache_clean])
    checks = [
        ("VAL2142_00_sources", sources_ok, "2141/gravity/action source evidence validates"),
        ("VAL2142_01_anchors", anchors_ok, "line anchors for branch split and K_solar exist"),
        ("VAL2142_02_branch_split", branch_ok, "action and constitutive branches are formally split"),
        ("VAL2142_03_inputs", inputs_ok, "numeric inputs and missing parent inputs are explicit"),
        ("VAL2142_04_runner", runner_ok, "numeric core bound computed and action residual remains blocked"),
        ("VAL2142_05_arenas", arenas_ok, "local arena projections remain nonclaim/blocked"),
        ("VAL2142_06_gates", gates_ok, "numeric smallness gate passes while local claim gate fails"),
        ("VAL2142_07_decisions", decisions_ok, "decision ledger selects local operator/source bridge next"),
        ("VAL2142_08_next", next_ok, "next target is 2143"),
        ("VAL2142_09_branch_copies", copies_ok, "branch copies exist and parse"),
        ("VAL2142_10_csv_parse", csv_ok, "all generated CSVs parse cleanly"),
        ("VAL2142_11_no_claim_flags", no_claim_flags, "no generated row allows a claim"),
        ("VAL2142_12_formalization_clean", formalization_clean, "formalization-workbench untouched by 2142"),
        ("VAL2142_13_no_pycache", pycache_clean, "scripts __pycache__ removed"),
        ("VAL2142_OVERALL", all_ok, "2142 formally splits action/constitutive saturation branches, computes the K_solar weak-field core bound, blocks local claims on missing operator/source inputs, and selects the local operator/source bridge gate next."),
    ]
    return [row(check_id=check_id, status="PASS" if passed else "FAIL", detail=detail) for check_id, passed, detail in checks]


def write_doc(
    sources: list[dict[str, object]],
    anchors: list[dict[str, object]],
    branches: list[dict[str, object]],
    inputs: list[dict[str, object]],
    runner: list[dict[str, object]],
    arenas: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    copies: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    content = "\n\n".join(
        [
            "# 2142 - Y5/R2FR Saturation Action Vs Constitutive Branch And PPN Bound Runner",
            "## Current Verdict",
            "2142 resolves the immediate ambiguity by formally splitting two branches. The action-derived branch is the one wanted for a final field theory, but it must carry the metric variation of `S=𝓢(K,nablaK,Phi)`. The constitutive branch matches the source statement that the response is algebraic and not a higher-derivative action modification, but it then owes a Bianchi/exchange-current derivation.",
            f"The weak-field core bound is real: with the source anchor `K_solar≈10^-61` and `m=2`, the direct algebraic saturation is `{dstr(S_ALGEBRAIC)}`. But the action-branch derivative coefficient is `{dstr(DS_DK_COEFF)}`, so the actual action residual is `{dstr(DS_DK_COEFF)} * ||deltaK||` plus gradient, Phi, boundary, and source-bridge terms.",
            "Therefore this checkpoint improves the local-GR route but still refuses a local-GR/Newton/PPN/R10 claim. The next missing object is no longer vague: derive local curvature operator norms and the source readout bridge.",
            "## Source Register",
            md_table(sources, ["source_id", "source_path", "path_exists", "needles_found", "role", "valid_for_claim"]),
            "## Source Anchors",
            md_table(anchors, ["anchor_id", "source_path", "line_number", "snippet", "role", "valid_for_claim"]),
            "## Branch Split",
            md_table(branches, ["branch_id", "branch", "source_basis", "mathematical_cost", "status", "valid_for_claim"]),
            "## Bound Inputs",
            md_table(inputs, ["input_id", "quantity", "value", "units", "source_path", "source_line", "status", "valid_for_claim"]),
            "## Bound Runner",
            md_table(runner, ["run_id", "branch", "expression", "numeric_value", "status", "interpretation", "valid_for_claim"]),
            "## Arena Projections",
            md_table(arenas, ["arena_id", "arena", "projected_quantity", "projection", "status", "blocker", "valid_for_claim"]),
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
    branches = branch_split_rows()
    inputs = bound_input_rows()
    runner = bound_runner_rows()
    arenas = arena_projection_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_rows = next_target_rows()

    paths = {
        "sources": OUT / "P8_Y5_PARENT_QLOC_2142_SOURCE_REGISTER.csv",
        "anchors": OUT / "P8_Y5_PARENT_QLOC_2142_SOURCE_ANCHORS.csv",
        "branches": OUT / "P8_Y5_PARENT_QLOC_2142_BRANCH_SPLIT.csv",
        "inputs": OUT / "P8_Y5_PARENT_QLOC_2142_BOUND_INPUTS.csv",
        "runner": OUT / "P8_Y5_PARENT_QLOC_2142_LOCAL_BOUND_RUNNER.csv",
        "arenas": OUT / "P8_Y5_PARENT_QLOC_2142_ARENA_PROJECTIONS.csv",
        "gates": OUT / "P8_Y5_PARENT_QLOC_2142_CLAIM_GATES.csv",
        "decisions": OUT / "P8_Y5_PARENT_QLOC_2142_DECISION_LEDGER.csv",
        "next": OUT / "P8_Y5_PARENT_QLOC_2142_NEXT_TARGET.csv",
        "branch_copies": OUT / "P8_Y5_PARENT_QLOC_2142_BRANCH_COPIES.csv",
        "validation": OUT / "P8_Y5_BRR545_2142_VALIDATION.csv",
    }

    write_csv(paths["sources"], sources)
    write_csv(paths["anchors"], anchors)
    write_csv(paths["branches"], branches)
    write_csv(paths["inputs"], inputs)
    write_csv(paths["runner"], runner)
    write_csv(paths["arenas"], arenas)
    write_csv(paths["gates"], gates)
    write_csv(paths["decisions"], decisions)
    write_csv(paths["next"], next_rows)

    copies = write_branch_copies(branches, inputs, runner, arenas, next_rows)
    write_csv(paths["branch_copies"], copies)

    remove_pycache()
    csv_paths = [path for key, path in paths.items() if key != "validation"] + [Path(str(copy["destination"])) for copy in copies]
    validation = validation_rows(sources, anchors, branches, inputs, runner, arenas, gates, decisions, next_rows, copies, csv_paths)
    write_csv(paths["validation"], validation)
    write_doc(sources, anchors, branches, inputs, runner, arenas, gates, decisions, next_rows, copies, validation)

    print(f"wrote {DOC}")
    print(f"validation {paths['validation']}")


if __name__ == "__main__":
    main()
