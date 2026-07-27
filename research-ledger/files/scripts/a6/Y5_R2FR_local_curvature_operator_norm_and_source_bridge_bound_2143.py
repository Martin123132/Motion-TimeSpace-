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

DOC = ROOT / "2143-Y5-R2FR-local-curvature-operator-norm-and-source-bridge-bound.md"
REPO = ROOT.parent
FORMALIZATION = REPO / "formalization-workbench"

DOC_2142 = ROOT / "2142-Y5-R2FR-saturation-action-vs-constitutive-branch-and-PPN-bound-runner.md"
CSV_2142_VAL = OUT / "P8_Y5_BRR545_2142_VALIDATION.csv"
CSV_2142_INPUTS = OUT / "P8_Y5_PARENT_QLOC_2142_BOUND_INPUTS.csv"
CSV_2142_RUNNER = OUT / "P8_Y5_PARENT_QLOC_2142_LOCAL_BOUND_RUNNER.csv"
CSV_2142_NEXT = OUT / "P8_Y5_PARENT_QLOC_2142_NEXT_TARGET.csv"

GRAVITY_SUMMARY = REPO / "core-mts-framework" / "gravity" / "motion-timespace-mts-gravity.md"
DOC_1339 = ROOT / "1339-Y5-R10-RAB-source-closure-to-EH-left-hand-local-GR-reduction-gate.md"
DOC_1008 = ROOT / "1008-Y5-R10-parent-theta-Qtau-extraction-or-charge-decomposition-runner.md"

K_SOLAR = Decimal("1e-61")
M_MIN = Decimal("2")
DS_DK_COEFF = Decimal("2e-61")
ACTION_RESIDUAL_FRACTION_COEFF = DS_DK_COEFF * K_SOLAR


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


def formalization_has_2143_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    patterns = (
        "*2143-Y5-R2FR*",
        "*P8_Y5_PARENT_QLOC_2143*",
        "*Y5_R2FR_local_curvature_operator_norm_and_source_bridge_bound_2143*",
        "*AFRAME_LOCAL_CURVATURE_SOURCE_BRIDGE_2143*",
        "*JR2143*",
    )
    try:
        return any(path.is_file() for pattern in patterns for path in FORMALIZATION.rglob(pattern))
    except Exception:
        return False


def source_register_rows() -> list[dict[str, object]]:
    specs = [
        (
            "SRC2143_00_2142_doc",
            DOC_2142,
            [["Current Verdict"], ["actual action residual"], ["source readout bridge"]],
            "2142 identifies deltaK/operator/source bridge as the next bottleneck.",
        ),
        (
            "SRC2143_01_2142_validation",
            CSV_2142_VAL,
            [["VAL2142_OVERALL"], ["PASS"], ["source bridge"]],
            "2142 validation passed.",
        ),
        (
            "SRC2143_02_2142_inputs",
            CSV_2142_INPUTS,
            [["IN2142_4_deltaK_norm"], ["IN2142_7_source_bridge"], ["MISSING_PARENT_INPUT"]],
            "2142 bound inputs explicitly mark deltaK and source bridge missing.",
        ),
        (
            "SRC2143_03_2142_runner",
            CSV_2142_RUNNER,
            [["RUN2142_2_action_residual_core"], ["MISSING_DELTAK_NORM"], ["BLOCKED_NONCLAIM"]],
            "2142 runner blocks action residual on missing deltaK norm.",
        ),
        (
            "SRC2143_04_2142_next",
            CSV_2142_NEXT,
            [["NEXT2142_0_2143"], ["||deltaK||"], ["M_H_ref/G_ref/Q_tau"]],
            "2142 handoff to local operator/source bridge.",
        ),
        (
            "SRC2143_05_gravity_summary",
            GRAVITY_SUMMARY,
            [["K_solar"], ["𝓢 ≈ K^m"], ["PPN parameters"]],
            "gravity summary supplies weak-field curvature scale and intended PPN arena.",
        ),
        (
            "SRC2143_06_1339_source_bridge",
            DOC_1339,
            [["EHGate1339_6_source_GM_transfer"], ["NEW1339_2_GM_calibration"], ["PPN Completion Gate"]],
            "1339 records the source-GM transfer and PPN completion blockers.",
        ),
        (
            "SRC2143_07_1008_Qtau",
            DOC_1008,
            [["Q_tau^MTS"], ["CG1008_5_MHref"], ["parent theta/Q_tau"]],
            "1008 records the parent charge/M_H_ref blocker.",
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
        ("ANCH2143_0_K_solar", GRAVITY_SUMMARY, ["K_solar"], "weak-field curvature scale"),
        ("ANCH2143_1_PPN", GRAVITY_SUMMARY, ["PPN parameters"], "PPN arena anchor"),
        ("ANCH2143_2_deltaK_block", DOC_2142, ["MISSING_DELTAK_NORM"], "2142 deltaK blocker"),
        ("ANCH2143_3_source_bridge_block", DOC_2142, ["M_H_ref/Q_tau/G_ref readout"], "2142 source bridge blocker"),
        ("ANCH2143_4_GM_transfer", DOC_1339, ["EHGate1339_6_source_GM_transfer"], "GM transfer blocker"),
        ("ANCH2143_5_Newton_GM", DOC_1339, ["NEW1339_2_GM_calibration"], "Newton GM calibration blocker"),
        ("ANCH2143_6_MHref", DOC_1008, ["CG1008_5_MHref"], "M_H_ref denominator blocker"),
        ("ANCH2143_7_Qtau_total", DOC_1008, ["QTA1008_8_Q_total"], "Q_tau total blocker"),
    ]
    rows: list[dict[str, object]] = []
    for anchor_id, path, needles, role in anchors:
        line_number, snippet = find_line(path, needles)
        rows.append(row(anchor_id=anchor_id, source_path=str(path), line_number=line_number, snippet=snippet, role=role))
    return rows


def curvature_operator_rows() -> list[dict[str, object]]:
    return [
        row(op_id="OP2143_0_schwarz_K", operator="Kretschmann weak-source proxy", formula="K=48 mu^2/r^6 with mu=G_ref M_H/c^2 in the exterior Schwarzschild/EH reference branch", status="EXACT_GR_REFERENCE_IDENTITY", consequence="turns K-variation into source-mass and radial/readout variation when the EH/source bridge is signed"),
        row(op_id="OP2143_1_deltaK_fractional", operator="first variation", formula="deltaK/K = 2 delta_mu/mu - 6 delta_r/r plus frame/readout/projector terms", status="EXACT_REFERENCE_VARIATION", consequence="||deltaK|| <= K_solar*(2 eps_mu + 6 eps_r + eps_frame)"),
        row(op_id="OP2143_2_delta_gradK_fractional", operator="gradient variation", formula="for |grad K|~6K/r, delta|gradK|/|gradK| = 2 delta_mu/mu - 7 delta_r/r plus connection/frame terms", status="REFERENCE_VARIATION_WITH_LENGTH_SCALE", consequence="needs local length/radius normalization before numeric bound"),
        row(op_id="OP2143_3_deltaPhi", operator="Phi curvature-tension proxy", formula="deltaPhi cannot be reduced until Phi is defined as a source/readout functional", status="MISSING_PARENT_FUNCTIONAL", consequence="Phi channel remains a blocker"),
        row(op_id="OP2143_4_action_residual_reduction", operator="S action residual", formula=f"|D_S^K deltaK| <= {dstr(DS_DK_COEFF)} * K_solar * (2 eps_mu + 6 eps_r + eps_frame) = {dstr(ACTION_RESIDUAL_FRACTION_COEFF)}*(2 eps_mu + 6 eps_r + eps_frame)", status="CONDITIONAL_BOUND_REDUCTION", consequence="deltaK box is reduced to source/readout fractional errors"),
        row(op_id="OP2143_5_verdict", operator="local curvature operator norm", formula="operator norm can be symbolically bounded in the EH/Schwarzschild reference branch, but not yet source-signed for MTS", status="BOUND_REDUCED_NOT_CLAIMED", consequence="next work must sign or bound mu/r/source readout"),
    ]


def source_bridge_rows() -> list[dict[str, object]]:
    return [
        row(bridge_id="SB2143_0_mu_definition", bridge_piece="exterior mass parameter", requirement="mu = G_ref M_H[worldtube]/c^2 = GM_orbital/c^2", current_status="NOT_DERIVED", source="1339 EHGate1339_6 and NEW1339_2"),
        row(bridge_id="SB2143_1_MH_ref", bridge_piece="Hilbert/Hamiltonian mass", requirement="M_H_ref is positive, finite, same-frame, and fixed before readout", current_status="BLOCKED", source="1008 CG1008_5_MHref"),
        row(bridge_id="SB2143_2_Qtau", bridge_piece="Q_tau^MTS total charge", requirement="Q_tau^MTS total is extracted sector-by-sector or all retained sectors are zero/bounded", current_status="BLOCKED", source="1008 QTA1008_8_Q_total"),
        row(bridge_id="SB2143_3_Gref", bridge_piece="G_ref normalization", requirement="G_ref is fixed independently of the local residual being tested", current_status="UNSIGNED", source="1339/2142 source-bridge blockers"),
        row(bridge_id="SB2143_4_radius_readout", bridge_piece="r/readout frame", requirement="local radius r and frame are observed-frame quantities shared by photons/clocks/orbits", current_status="UNSIGNED", source="1339 observed frame and PPN completion gates"),
        row(bridge_id="SB2143_5_Gauss_Poisson", bridge_piece="Newton/Gauss calibration", requirement="Poisson-looking algebra maps to measured Newtonian gravity only after GM transfer", current_status="BLOCKED", source="1339 NEW1339_2 and anti-shortcut gate"),
        row(bridge_id="SB2143_6_verdict", bridge_piece="source bridge", requirement="all source pieces above pass", current_status="SOURCE_BRIDGE_NOT_CLOSED", source="2143 consolidated bridge"),
    ]


def bound_runner_rows() -> list[dict[str, object]]:
    return [
        row(run_id="RUN2143_0_K_value", quantity="K_solar", expression="source anchor", numeric_or_symbolic=dstr(K_SOLAR), status="SOURCE_ANCHOR_NONCLAIM"),
        row(run_id="RUN2143_1_deltaK_fractional", quantity="||deltaK||", expression="<= K_solar*(2 eps_mu + 6 eps_r + eps_frame)", numeric_or_symbolic=f"{dstr(K_SOLAR)}*(2 eps_mu + 6 eps_r + eps_frame)", status="SYMBOLIC_OPERATOR_BOUND"),
        row(run_id="RUN2143_2_action_residual_fractional", quantity="|D_S^K deltaK|", expression="<= 2e-61*K_solar*(2 eps_mu + 6 eps_r + eps_frame)", numeric_or_symbolic=f"{dstr(ACTION_RESIDUAL_FRACTION_COEFF)}*(2 eps_mu + 6 eps_r + eps_frame)", status="SYMBOLIC_ACTION_BOUND_REDUCED"),
        row(run_id="RUN2143_3_if_fractional_control", quantity="example controlled-source scale", expression="if eps_combo=(2 eps_mu + 6 eps_r + eps_frame)<=1, K-channel action residual <=2e-122", numeric_or_symbolic="2.000000E-122 under unsourced eps_combo<=1", status="ILLUSTRATIVE_NONCLAIM"),
        row(run_id="RUN2143_4_gradK", quantity="||delta(nablaK)||", expression="<= |gradK|*(2 eps_mu + 7 eps_r + eps_frame + eps_connection)", numeric_or_symbolic="MISSING_LENGTH_SCALE_AND_CONNECTION_NORM", status="BLOCKED_NONCLAIM"),
        row(run_id="RUN2143_5_Phi", quantity="||deltaPhi||", expression="requires Phi definition and proxy normalization", numeric_or_symbolic="MISSING_PHI_FUNCTIONAL", status="BLOCKED_NONCLAIM"),
        row(run_id="RUN2143_6_source_bridge", quantity="mu/r readout", expression="requires M_H_ref/Q_tau/G_ref/r_obs bridge", numeric_or_symbolic="MISSING_SOURCE_BRIDGE", status="BLOCKED_NONCLAIM"),
        row(run_id="RUN2143_7_verdict", quantity="local operator norm", expression="deltaK reduced to source/readout fractions; gradient/Phi/source bridge still block claims", numeric_or_symbolic="NO_CLAIM", status="BOUND_REDUCED_NOT_SCOREABLE"),
    ]


def arena_projection_rows() -> list[dict[str, object]]:
    return [
        row(arena_id="ARENA2143_0_PPN_gamma_beta", arena="PPN gamma/beta", projection="K-channel residual can be bounded by 2e-122*eps_combo, but PPN map and source bridge remain missing", status="PARTIAL_BOUND_NONCLAIM", blocker="PPN coefficient map plus source bridge"),
        row(arena_id="ARENA2143_1_R10", arena="R10", projection="needs conversion from local S/D_S residual to Yukawa alpha(lambda)", status="BLOCKED_NONCLAIM", blocker="finite-range projection"),
        row(arena_id="ARENA2143_2_orbital", arena="orbital GM", projection="requires mu=GM_orb/c^2 equality and residual charge extraction", status="BLOCKED_NONCLAIM", blocker="M_H_ref/Q_tau/G_ref"),
        row(arena_id="ARENA2143_3_clock", arena="clock", projection="requires same-frame tau/readout map and exchange current", status="BLOCKED_NONCLAIM", blocker="tau_source/tau_clock/J^S_nu"),
        row(arena_id="ARENA2143_4_constitutive", arena="Bianchi/constitutive", projection="algebraic branch still needs J^S_nu or proof grad S negligible", status="BLOCKED_NONCLAIM", blocker="exchange current"),
        row(arena_id="ARENA2143_5_verdict", arena="all local arenas", projection="deltaK is no longer the primary mystery; source bridge and gradient/Phi definitions are", status="CLAIM_BLOCKED_BUT_SHARPENED", blocker="source bridge and remaining channels"),
    ]


def claim_gate_rows() -> list[dict[str, object]]:
    return [
        row(gate_id="GATE2143_0_sources", gate="2142/1339/1008 source evidence validates", gate_pass=True, rationale="source register confirms local operator and source-bridge inputs"),
        row(gate_id="GATE2143_1_deltaK_reduced", gate="deltaK operator norm reduced to source/readout fractions", gate_pass=True, rationale="Schwarzschild K variation gives deltaK/K=2 delta_mu/mu-6 delta_r/r plus frame terms"),
        row(gate_id="GATE2143_2_action_bound_symbolic", gate="action K-channel residual symbolic bound available", gate_pass=True, rationale=f"bound reduces to {dstr(ACTION_RESIDUAL_FRACTION_COEFF)} times source/readout eps combo"),
        row(gate_id="GATE2143_3_gradient_Phi_closed", gate="gradient/Phi channels closed", gate_pass=False, rationale="length/connection/Phi normalization missing"),
        row(gate_id="GATE2143_4_source_bridge_closed", gate="M_H_ref/Q_tau/G_ref source bridge closed", gate_pass=False, rationale="1339 and 1008 keep GM transfer and parent charge blocked"),
        row(gate_id="GATE2143_5_PPN_R10_claim", gate="PPN/R10 claim allowed", gate_pass=False, rationale="symbolic bound lacks PPN/R10 projection and source bridge"),
        row(gate_id="GATE2143_6_local_GR_Newton_claim", gate="local GR/Newton claim allowed", gate_pass=False, rationale="measured-GM transfer and full residual vector remain open"),
    ]


def decision_rows() -> list[dict[str, object]]:
    return [
        row(decision_id="DEC2143_0", decision="DELTAK_REDUCED_TO_SOURCE_FRACTIONS", because="K=48mu^2/r^6 makes the first variation explicit", next_action="derive/bound eps_mu, eps_r and frame terms"),
        row(decision_id="DEC2143_1", decision="SOURCE_BRIDGE_IS_NOW_PRIMARY", because="the action residual is small if the source/readout fractional variations are controlled", next_action="attack M_H_ref/Q_tau/G_ref bridge"),
        row(decision_id="DEC2143_2", decision="GRADIENT_PHI_REMAIN_SEPARATE_CHANNELS", because="gradK needs length/connection norm and Phi still lacks parent definition", next_action="do not collapse all channels into K_solar"),
        row(decision_id="DEC2143_3", decision="NEXT_QTAU_MHREF_BRIDGE_OR_BOUNDED_CLOSURE", because="1339/1008 are the live blockers for measured Newtonian mechanics", next_action="2144 source charge/readout bridge closure attempt"),
    ]


def next_target_rows() -> list[dict[str, object]]:
    return [
        row(
            route_id="NEXT2143_0_2144",
            next_target="2144-Y5-R2FR-MHref-Qtau-Gref-source-readout-bridge-or-closure.md",
            script="scripts/Y5_R2FR_MHref_Qtau_Gref_source_readout_bridge_or_closure_2144.py",
            objective="Try to close the measured-source bridge mu=G_ref M_H_ref/c^2=GM_orbital/c^2 by connecting M_H_ref, Q_tau^MTS, G_ref, and observed radius/readout frame; if not, stage explicit epsilon_mu, epsilon_r, epsilon_frame closure rows for the 2143 operator bound.",
            forbidden_shortcuts="claim Newton from Poisson shape; import EH charge as MTS charge; fit G_ref after residual readout; omit boundary/projector/source sectors; ignore gradient/Phi channels; local-GR/Newton/PPN/R10 claim; formalization-workbench edits; GitHub action",
        )
    ]


def write_branch_copies(
    operators: list[dict[str, object]],
    bridge: list[dict[str, object]],
    runner: list[dict[str, object]],
    arenas: list[dict[str, object]],
    next_rows: list[dict[str, object]],
) -> list[dict[str, object]]:
    copies = [
        ("COPY2143_0_source_weight_docs", SOURCE_WEIGHT_DOCS / "AFRAME_LOCAL_CURVATURE_SOURCE_BRIDGE_2143_NONCLAIM.csv", operators + bridge + runner),
        ("COPY2143_1_branch_locked_wep", BRANCH_WEP / "P8_Y5_PARENT_QLOC_2143_OPERATOR_BOUND_NONCLAIM.csv", runner + arenas),
        ("COPY2143_2_acquisition_queue", QUEUE / "JR2143_MHREF_QTAU_GREF_BRIDGE_QUEUE.csv", next_rows + bridge),
    ]
    results: list[dict[str, object]] = []
    for copy_id, destination, rows_to_write in copies:
        write_csv(destination, rows_to_write)
        results.append(row(copy_id=copy_id, destination=str(destination), path_exists=destination.exists(), row_count=len(rows_to_write), parse_ok=csv_rows_parse(destination)))
    return results


def validation_rows(
    sources: list[dict[str, object]],
    anchors: list[dict[str, object]],
    operators: list[dict[str, object]],
    bridge: list[dict[str, object]],
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
    operator_ok = any(item["op_id"] == "OP2143_4_action_residual_reduction" and item["status"] == "CONDITIONAL_BOUND_REDUCTION" for item in operators)
    bridge_ok = any(item["bridge_id"] == "SB2143_6_verdict" and item["current_status"] == "SOURCE_BRIDGE_NOT_CLOSED" for item in bridge)
    runner_ok = any(item["run_id"] == "RUN2143_2_action_residual_fractional" and item["status"] == "SYMBOLIC_ACTION_BOUND_REDUCED" for item in runner) and any(item["run_id"] == "RUN2143_7_verdict" and item["status"] == "BOUND_REDUCED_NOT_SCOREABLE" for item in runner)
    arenas_ok = any(item["arena_id"] == "ARENA2143_5_verdict" and item["status"] == "CLAIM_BLOCKED_BUT_SHARPENED" for item in arenas)
    gates_ok = any(item["gate_id"] == "GATE2143_1_deltaK_reduced" and truthy(item["gate_pass"]) for item in gates) and any(item["gate_id"] == "GATE2143_6_local_GR_Newton_claim" and not truthy(item["gate_pass"]) for item in gates)
    decisions_ok = any(item["decision_id"] == "DEC2143_3" and item["decision"] == "NEXT_QTAU_MHREF_BRIDGE_OR_BOUNDED_CLOSURE" for item in decisions)
    next_ok = any(item["route_id"] == "NEXT2143_0_2144" for item in next_rows)
    copies_ok = all(truthy(item["path_exists"]) and truthy(item["parse_ok"]) for item in copies)
    csv_ok = all(path.exists() and csv_rows_parse(path) for path in csv_paths)
    no_claim_flags = all(
        not truthy(item.get("claim_allowed", False)) and not truthy(item.get("valid_for_claim", False))
        for group in (sources, anchors, operators, bridge, runner, arenas, gates, decisions, next_rows, copies)
        for item in group
    )
    formalization_clean = count_formalization_modified() == 0 and not formalization_has_2143_artifacts()
    pycache_clean = not (Path(__file__).resolve().parent / "__pycache__").exists()
    all_ok = all([sources_ok, anchors_ok, operator_ok, bridge_ok, runner_ok, arenas_ok, gates_ok, decisions_ok, next_ok, copies_ok, csv_ok, no_claim_flags, formalization_clean, pycache_clean])
    checks = [
        ("VAL2143_00_sources", sources_ok, "2142/1339/1008 source evidence validates"),
        ("VAL2143_01_anchors", anchors_ok, "line anchors for K_solar, deltaK, GM and Q_tau blockers exist"),
        ("VAL2143_02_operator", operator_ok, "deltaK action residual reduced to source/readout fractions"),
        ("VAL2143_03_bridge", bridge_ok, "source bridge is explicitly not closed"),
        ("VAL2143_04_runner", runner_ok, "symbolic action bound is reduced but not scoreable"),
        ("VAL2143_05_arenas", arenas_ok, "arena projections remain blocked but sharpened"),
        ("VAL2143_06_gates", gates_ok, "deltaK gate passes while local claim gate fails"),
        ("VAL2143_07_decisions", decisions_ok, "decision ledger selects MH_ref/Q_tau/G_ref bridge next"),
        ("VAL2143_08_next", next_ok, "next target is 2144"),
        ("VAL2143_09_branch_copies", copies_ok, "branch copies exist and parse"),
        ("VAL2143_10_csv_parse", csv_ok, "all generated CSVs parse cleanly"),
        ("VAL2143_11_no_claim_flags", no_claim_flags, "no generated row allows a claim"),
        ("VAL2143_12_formalization_clean", formalization_clean, "formalization-workbench untouched by 2143"),
        ("VAL2143_13_no_pycache", pycache_clean, "scripts __pycache__ removed"),
        ("VAL2143_OVERALL", all_ok, "2143 reduces deltaK to source/readout fractional bounds, keeps gradient/Phi/source bridge nonclaim, and selects MH_ref/Q_tau/G_ref bridge closure next."),
    ]
    return [row(check_id=check_id, status="PASS" if passed else "FAIL", detail=detail) for check_id, passed, detail in checks]


def write_doc(
    sources: list[dict[str, object]],
    anchors: list[dict[str, object]],
    operators: list[dict[str, object]],
    bridge: list[dict[str, object]],
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
            "# 2143 - Y5/R2FR Local Curvature Operator Norm And Source Bridge Bound",
            "## Current Verdict",
            "2143 makes a real reduction: in a Schwarzschild/EH reference exterior, `K=48 mu^2/r^6`, so `deltaK` is not an arbitrary mystery. It is controlled by source/readout fractional variations: `deltaK/K = 2 delta_mu/mu - 6 delta_r/r` plus frame/projector terms.",
            f"Using the 2142 coefficient, the K-channel action residual becomes `{dstr(ACTION_RESIDUAL_FRACTION_COEFF)}*(2 eps_mu + 6 eps_r + eps_frame)`. This is much sharper than the previous `MISSING_DELTAK_NORM`, but it is still not a PPN/Newton claim because `mu=G_ref M_H_ref/c^2=GM_orbital/c^2` is not parent-signed.",
            "So the bottleneck has moved. `deltaK` is now conditionally bounded; the real obstruction is the source bridge: `M_H_ref`, `Q_tau^MTS`, `G_ref`, observed radius/frame, gradient/Phi channels, and Bianchi/current closure.",
            "## Source Register",
            md_table(sources, ["source_id", "source_path", "path_exists", "needles_found", "role", "valid_for_claim"]),
            "## Source Anchors",
            md_table(anchors, ["anchor_id", "source_path", "line_number", "snippet", "role", "valid_for_claim"]),
            "## Curvature Operator Rows",
            md_table(operators, ["op_id", "operator", "formula", "status", "consequence", "valid_for_claim"]),
            "## Source Bridge Rows",
            md_table(bridge, ["bridge_id", "bridge_piece", "requirement", "current_status", "source", "valid_for_claim"]),
            "## Bound Runner",
            md_table(runner, ["run_id", "quantity", "expression", "numeric_or_symbolic", "status", "valid_for_claim"]),
            "## Arena Projections",
            md_table(arenas, ["arena_id", "arena", "projection", "status", "blocker", "valid_for_claim"]),
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
    operators = curvature_operator_rows()
    bridge = source_bridge_rows()
    runner = bound_runner_rows()
    arenas = arena_projection_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_rows = next_target_rows()

    paths = {
        "sources": OUT / "P8_Y5_PARENT_QLOC_2143_SOURCE_REGISTER.csv",
        "anchors": OUT / "P8_Y5_PARENT_QLOC_2143_SOURCE_ANCHORS.csv",
        "operators": OUT / "P8_Y5_PARENT_QLOC_2143_CURVATURE_OPERATOR_ROWS.csv",
        "bridge": OUT / "P8_Y5_PARENT_QLOC_2143_SOURCE_BRIDGE_ROWS.csv",
        "runner": OUT / "P8_Y5_PARENT_QLOC_2143_OPERATOR_BOUND_RUNNER.csv",
        "arenas": OUT / "P8_Y5_PARENT_QLOC_2143_ARENA_PROJECTIONS.csv",
        "gates": OUT / "P8_Y5_PARENT_QLOC_2143_CLAIM_GATES.csv",
        "decisions": OUT / "P8_Y5_PARENT_QLOC_2143_DECISION_LEDGER.csv",
        "next": OUT / "P8_Y5_PARENT_QLOC_2143_NEXT_TARGET.csv",
        "branch_copies": OUT / "P8_Y5_PARENT_QLOC_2143_BRANCH_COPIES.csv",
        "validation": OUT / "P8_Y5_BRR545_2143_VALIDATION.csv",
    }

    write_csv(paths["sources"], sources)
    write_csv(paths["anchors"], anchors)
    write_csv(paths["operators"], operators)
    write_csv(paths["bridge"], bridge)
    write_csv(paths["runner"], runner)
    write_csv(paths["arenas"], arenas)
    write_csv(paths["gates"], gates)
    write_csv(paths["decisions"], decisions)
    write_csv(paths["next"], next_rows)

    copies = write_branch_copies(operators, bridge, runner, arenas, next_rows)
    write_csv(paths["branch_copies"], copies)

    remove_pycache()
    csv_paths = [path for key, path in paths.items() if key != "validation"] + [Path(str(copy["destination"])) for copy in copies]
    validation = validation_rows(sources, anchors, operators, bridge, runner, arenas, gates, decisions, next_rows, copies, csv_paths)
    write_csv(paths["validation"], validation)
    write_doc(sources, anchors, operators, bridge, runner, arenas, gates, decisions, next_rows, copies, validation)

    print(f"wrote {DOC}")
    print(f"validation {paths['validation']}")


if __name__ == "__main__":
    main()
