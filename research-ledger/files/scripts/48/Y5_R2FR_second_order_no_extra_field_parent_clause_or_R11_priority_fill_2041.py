from __future__ import annotations

import csv
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


DOC = ROOT / "2041-Y5-R2FR-second-order-no-extra-field-parent-clause-or-R11-priority-fill.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
SCRIPT_PATH = Path(__file__).resolve()


def formalization_has_2041_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    try:
        artifact_patterns = (
            "*2041-Y5-R2FR*",
            "*P8_Y5_PARENT_QLOC_2041*",
            "*Y5_R2FR_second_order_no_extra_field_parent_clause_or_R11_priority_fill_2041*",
        )
        return any(path.is_file() for pattern in artifact_patterns for path in FORMALIZATION.rglob(pattern))
    except Exception:
        return False


def scripts_pycache_exists() -> bool:
    return (SCRIPT_PATH.parent / "__pycache__").exists()


def read_csv_dicts(path: Path) -> list[dict[str, str]]:
    try:
        with path.open("r", newline="", encoding="utf-8", errors="replace") as handle:
            return list(csv.DictReader(handle))
    except Exception:
        return []


def source_register_rows() -> list[dict[str, object]]:
    specs = [
        (
            "SRC2041_00_2040_doc",
            ROOT / "2040-Y5-R2FR-PPN-beta-conservation-common-matter-parent-signature.md",
            ["NEXT2040_0_2041", "ROUTE2040_1_EH_operator", "VAL2040_OVERALL"],
            "2040 handoff selecting EH/no-extra-field or R11 priority fill.",
        ),
        (
            "SRC2041_01_2040_next",
            OUT / "P8_Y5_PARENT_QLOC_2040_NEXT_TARGET.csv",
            ["NEXT2040_0_2041", "second-order metric-only no-extra-field"],
            "machine-readable 2041 target.",
        ),
        (
            "SRC2041_02_2040_route",
            OUT / "P8_Y5_PARENT_QLOC_2040_ROUTE_SELECTION.csv",
            ["ROUTE2040_1_EH_operator", "ROUTE2040_2_R11_fallback"],
            "2040 route decision: try EH/no-extra-field first, R11 fallback second.",
        ),
        (
            "SRC2041_03_958_operator",
            ROOT / "958-Y5-R10-EH-core-operator-selection-or-executable-R11-nonEH-vector.md",
            ["EH958_5_verdict", "R11REV958_1", "DEC958_2_next_route"],
            "older EH operator selection attempt and R11/nonEH fallback priority.",
        ),
        (
            "SRC2041_04_959_no_extra",
            ROOT / "959-Y5-R10-local-second-order-metric-only-no-extra-field-clause-or-R11-priority-fill.md",
            ["NEF959_5_verdict", "R11FILL959_0", "R11FILL959_1"],
            "first no-extra-field clause attempt and priority fill templates.",
        ),
        (
            "SRC2041_05_959_no_extra_csv",
            OUT / "P8_Y5_R10_959_NO_EXTRA_FIELD_CLAUSE_ATTEMPT.csv",
            ["NEF959_5_verdict", "not_parent_derived_current_corpus"],
            "machine-readable no-extra-field clause failure.",
        ),
        (
            "SRC2041_06_959_fill_csv",
            OUT / "P8_Y5_R10_959_R11_PRIORITY_FILL_TEMPLATE.csv",
            ["R11FILL959_0", "R11FILL959_1"],
            "machine-readable R2/fR and torsion/nonmetricity fill templates.",
        ),
        (
            "SRC2041_07_960_doc",
            ROOT / "960-Y5-R10-R2-fR-scalar-mode-zero-or-bound-and-torsion-Levi-Civita-gate.md",
            ["LC960_4_verdict", "P4REV960_0", "V960_11_validation_rows_ready"],
            "R2/fR filter and torsion Levi-Civita gate result.",
        ),
        (
            "SRC2041_08_960_lc_csv",
            OUT / "P8_Y5_R10_960_TORSION_LEVI_CIVITA_GATE_ATTEMPT.csv",
            ["LC960_4_verdict", "not_closed_current_corpus"],
            "machine-readable torsion/nonmetricity Levi-Civita gate.",
        ),
        (
            "SRC2041_09_960_p4_csv",
            OUT / "P8_Y5_R10_960_P4_CONNECTION_SUBROW_REVIEW.csv",
            ["P4REV960_0", "REJECTED_P4_CONNECTION_PLACEHOLDER"],
            "machine-readable P4 connection placeholder rejection.",
        ),
        (
            "SRC2041_10_962_doc",
            ROOT / "962-Y5-R10-R2-fR-zero-clause-proof-or-scalar-mode-bound-source-acquisition.md",
            ["R2Z962_5_relative_zero_theorem", "CGATE962_1_absolute_MTS_zero", "DEC962_2_best_next_target"],
            "R2/fR relative theorem: boxed but not absolute.",
        ),
        (
            "SRC2041_11_963_doc",
            ROOT / "963-Y5-R10-parent-second-order-signature-or-R2FR-bound-runner.md",
            ["NES963_5_verdict", "DEC963_2_best_route", "V963_10_validation_rows_ready"],
            "parent second-order/no-extra-scalar signature attempt.",
        ),
        (
            "SRC2041_12_964_doc",
            ROOT / "964-Y5-R10-parent-no-higher-derivative-minimality-theorem-or-R2FR-nonclaim-runner.md",
            ["MIN964_5_verdict", "R2RUN964_VERDICT", "DEC964_2_best_next"],
            "minimality/no-higher-derivative derivation failed; R2/fR stays nonclaim.",
        ),
        (
            "SRC2041_13_965_doc",
            ROOT / "965-Y5-R10-primitive-quotient-no-natural-marker-theorem-or-R2FR-full-curve-intake.md",
            ["PQ965_5_verdict", "DEC965_1_R2FR_route", "V965_2_theorem_not_overclaimed"],
            "primitive quotient/no-natural-marker attempt also failed, leaving covariant marker countermodels.",
        ),
        (
            "SRC2041_14_1960_p4",
            OUT / "P8_Y5_PARENT_QLOC_1960_P4_CONNECTION_ENVELOPE_LEDGER.csv",
            ["P4C1960_0_combined", "P4C1960_5_hypermomentum"],
            "current P4 connection envelope rows: all nonclaim and missing maps.",
        ),
        (
            "SRC2041_15_R11_vector",
            OUT / "R11_nonEH_operator_vector_executable.csv",
            ["R2_fR_scalar_mode", "torsion_nonmetricity", "MISSING_RESIDUAL_BOUND_OR_THEOREM_SOURCE"],
            "global nonEH operator vector confirms R2/fR and torsion/nonmetricity rows remain unfilled.",
        ),
    ]
    rows: list[dict[str, object]] = []
    for source_id, path, needles, note in specs:
        exists = path.exists()
        text = read_text(path) if exists else ""
        ok = exists and all(needle in text for needle in needles)
        row = base_row()
        row.update(
            {
                "source_id": source_id,
                "source_path": str(path),
                "status": "EXISTS_NEEDLES_CONFIRMED" if ok else "MISSING_OR_NEEDLE_FAIL",
                "needles": ";".join(needles),
                "note": note,
            }
        )
        rows.append(row)
    return rows


def no_extra_field_audit_rows() -> list[dict[str, object]]:
    data = [
        (
            "NEF2041_0_target",
            "local second-order metric-only no-extra-field parent clause",
            "Fields_ext={g_obs}; E_g has at most second metric derivatives; no surviving scalar/vector/connection/source-marker/boundary operator appears in the compact local exterior.",
            "TARGET_DEFINED",
            "This is the exact clause that would make the EH/Lovelock route mathematically clean.",
            "target is not a derivation",
            False,
        ),
        (
            "NEF2041_1_Lovelock_implication",
            "EH implication if premises are parent-signed",
            "In 4D, local diffeomorphism-invariant metric-only second-order field equations imply EH+Lambda up to normalization/boundary under the usual assumptions.",
            "CONDITIONAL_MATH_CLEAN",
            "If MTS earns the premises, the left-hand operator is no longer a fitted preference.",
            "Lovelock implication cannot be promoted as MTS evidence until the premises are parent-owned.",
            "conditional_only",
        ),
        (
            "NEF2041_2_metric_only",
            "observed exterior uses only g_obs",
            "All ordinary compact-exterior readout and dynamics descend to the observed metric/coframe with no independent connection, class scalar, marker or memory field.",
            "UNSIGNED",
            "would eliminate whole families of nonEH operators",
            "959/960/964/965 leave connection and marker countermodels legal",
            False,
        ),
        (
            "NEF2041_3_second_order",
            "parent enforces second-order metric equations",
            "Higher-curvature terms such as R2/fR are absent, topological/redundant, or explicitly bounded.",
            "UNSIGNED",
            "would activate the 962 relative R2/fR zero theorem",
            "964 minimality theorem failed and integrated-out towers remain legal",
            False,
        ),
        (
            "NEF2041_4_no_extra_scalar",
            "no scalar marker survives reduction",
            "No quotient-invariant class scalar, domain selector, source label, or reduced-action marker can couple to R or matter.",
            "UNSIGNED",
            "would kill scalar-tensor/f(R)-style leakage at the parent level",
            "965 leaves covariant markers and quotient-invariant scalars live",
            False,
        ),
        (
            "NEF2041_5_Levi_Civita_connection",
            "Gamma equals LC(g_obs) or is physically silent",
            "Either no independent connection exists, or Palatini-EH plus zero hypermomentum and projective silence forces Gamma=LC(g_obs).",
            "UNSIGNED",
            "would close torsion/nonmetricity, clocks, WEP, spin/source, and lightcone connection leakage",
            "960 and 1960 keep P4 connection rows unresolved",
            False,
        ),
        (
            "NEF2041_6_boundary_projection",
            "boundary/local projection silence",
            "No representative Weyl/disformal/connection/boundary coefficient survives projection into local compact tests.",
            "UNSIGNED",
            "would prevent hidden residuals from bypassing the EH theorem",
            "boundary/local projection silence is still closure-only",
            False,
        ),
        (
            "NEF2041_7_verdict",
            "activate EH/no-extra-field parent theorem",
            "NEF2041_2 through NEF2041_6 all parent-signed; then NEF2041_1 selects EH+Lambda.",
            "NOT_PARENT_DERIVED_CURRENT_CORPUS",
            "no-extra-field route remains the right spine, but not a claim",
            "must go after the biggest unsigned structural clause next: connection/no-hypermomentum",
            False,
        ),
    ]
    rows = []
    for row_id, clause, mathematical_form, status, would_close, blocker, parent_signed in data:
        row = base_row()
        row.update(
            {
                "row_id": row_id,
                "clause": clause,
                "mathematical_form": mathematical_form,
                "status": status,
                "would_close": would_close,
                "blocker": blocker,
                "parent_signed": parent_signed,
                "claim_allowed": False,
            }
        )
        rows.append(row)
    return rows


def r2fr_decision_rows() -> list[dict[str, object]]:
    data = [
        (
            "R2FR2041_0_relative_theorem",
            "R2/fR scalar-mode filter",
            "If the parent local branch is exact metric-only, local, diffeo-invariant, second-order and no scalar survives, then f_RR=0 and c_R2/c_fR vanish.",
            "RELATIVE_THEOREM_AVAILABLE",
            "962 gives a useful mathematical box around the leak.",
            "absolute parent premise remains unsigned",
            "do_not_reprove_filter",
        ),
        (
            "R2FR2041_1_absolute_zero",
            "absolute MTS c_R2=c_fR zero",
            "derive the parent no-higher-derivative/no-extra-scalar/minimality clause directly from MTS quotient structure",
            "NOT_PROVEN",
            "964 minimality attempt and 965 primitive quotient/no-marker attempt both failed",
            "covariant marker, scalar, integrated-out and nonlocal countermodels remain legal",
            "do_not_claim_zero",
        ),
        (
            "R2FR2041_2_finite_branch",
            "finite scalar-mode fallback",
            "if R2/fR survives, source c_R2/f_RR, units, scalar mass/range, alpha(lambda), screening status, and real bound curve",
            "RUNNER_ONLY_NONCLAIM",
            "a strict nonclaim runner path exists",
            "missing parent prediction and digitized full curve for claim use",
            "optional_testing_route",
        ),
        (
            "R2FR2041_3_route_decision",
            "whether to keep circling R2/fR",
            "R2/fR is boxed enough for now: theorem-zero is conditional, finite branch is nonclaim, no absolute parent route closed.",
            "DEFER_DERIVATION_CIRCLE",
            "prevents burning turns on the same scalar gate without new parent input",
            "connection gate remains more structural for GR, matter coupling, clocks and WEP",
            "switch_to_connection_gate",
        ),
    ]
    rows = []
    for row_id, target, mathematical_content, status, useful_result, blocker, next_action in data:
        row = base_row()
        row.update(
            {
                "row_id": row_id,
                "target": target,
                "mathematical_content": mathematical_content,
                "status": status,
                "useful_result": useful_result,
                "blocker": blocker,
                "next_action": next_action,
                "claim_allowed": False,
            }
        )
        rows.append(row)
    return rows


def connection_decision_rows() -> list[dict[str, object]]:
    data = [
        (
            "LC2041_0_metric_formalism",
            "no independent observed connection variable",
            "If the parent ordinary-sector configuration space is (g_obs, matter) only and all derivatives use LC(g_obs), torsion/nonmetricity vanish identically.",
            "CLEAN_IF_SIGNED",
            "would close torsion/nonmetricity without tuning",
            "not parent-signed for every matter/source/readout sector",
            "try to derive configuration-space descent",
        ),
        (
            "LC2041_1_Palatini_EH",
            "Palatini route to Levi-Civita",
            "If independent Gamma enters only EH and the matter/source/readout action has zero hypermomentum, then the connection equation gives metric compatibility up to projective gauge.",
            "CONDITIONAL",
            "a serious route if EH/no-hypermomentum are both owned",
            "EH-only operator and no-Gamma matter/source/readout theorem are open",
            "derive no-hypermomentum clause",
        ),
        (
            "LC2041_2_projective_silence",
            "projective trace and boundary silence",
            "Projective mode must be gauge, fixed, or unobservable in clocks, source charge, lightcones, spin transport and orbital readout.",
            "UNSIGNED",
            "prevents trace connection leakage from hiding in readout",
            "1960 marks projective trace as missing invariance or bound",
            "map projective trace to zero or P4 bound row",
        ),
        (
            "LC2041_3_hypermomentum",
            "matter/source/readout hypermomentum",
            "delta S_matter/source/readout / delta Gamma = 0 in the observed ordinary branch, or bounded as a P4 residual.",
            "UNSIGNED",
            "this is probably the coupling hinge the work has been circling",
            "1960 keeps hypermomentum missing no-Gamma matter proof or bound",
            "make this the next derivation target",
        ),
        (
            "LC2041_4_P4_fallback",
            "executable P4 connection residual rows",
            "if no theorem closes, fill c_T/c_Q subrows for axial torsion, projective trace, Weyl nonmetricity, shear nonmetricity and hypermomentum with units/maps/bounds",
            "NOT_SCORE_READY",
            "provides honest empirical fallback",
            "all current P4 rows have missing coefficient/value/unit/map/source",
            "source or derive first P4 row",
        ),
        (
            "LC2041_5_verdict",
            "Levi-Civita/no-hypermomentum gate",
            "LC2041_0 or LC2041_1+LC2041_2+LC2041_3 must pass, else LC2041_4 must be filled.",
            "SELECTED_NEXT_BLOCKED_GATE",
            "best route now because it directly controls GR coupling, clocks, WEP, spin/source and lightcones",
            "current corpus has only conditional routes and placeholder P4 rows",
            "2042 should attack no-hypermomentum or build first P4 row",
        ),
    ]
    rows = []
    for row_id, target, mathematical_content, status, useful_result, blocker, next_action in data:
        row = base_row()
        row.update(
            {
                "row_id": row_id,
                "target": target,
                "mathematical_content": mathematical_content,
                "status": status,
                "useful_result": useful_result,
                "blocker": blocker,
                "next_action": next_action,
                "claim_allowed": False,
            }
        )
        rows.append(row)
    return rows


def priority_r11_fill_rows() -> list[dict[str, object]]:
    template_rows = read_csv_dicts(OUT / "P8_Y5_R10_959_R11_PRIORITY_FILL_TEMPLATE.csv")
    p4_rows = read_csv_dicts(OUT / "P8_Y5_PARENT_QLOC_1960_P4_CONNECTION_ENVELOPE_LEDGER.csv")
    rows: list[dict[str, object]] = []
    for source in template_rows:
        row = base_row()
        family = source.get("operator_family", "")
        if family == "R2_fR_scalar_mode":
            route_status = "DEFERRED_BOXED_NONCLAIM_RUNNER"
            next_action = "only return to full-curve intake after parent c_R2/f_RR or scalar alpha/lambda exists"
        elif family == "torsion_nonmetricity":
            route_status = "SELECTED_NEXT_STRUCTURAL_GATE"
            next_action = "derive no independent connection/no hypermomentum or fill P4 subrows"
        else:
            route_status = "RETAINED"
            next_action = "not a 2041 priority"
        row.update(
            {
                "row_id": source.get("fill_id", "MISSING_FILL_ID"),
                "operator_family": family,
                "coefficient_symbol": source.get("coefficient_symbol", ""),
                "candidate_value": source.get("candidate_value", ""),
                "candidate_units": source.get("candidate_units", ""),
                "normalization": source.get("normalization", ""),
                "weak_field_map": source.get("weak_field_map", ""),
                "predicted_residual_or_bound_source": source.get("predicted_residual_or_bound_source", ""),
                "source_file": source.get("source_file", ""),
                "ready_for_scoring": source.get("ready_for_scoring", "false"),
                "route_status": route_status,
                "next_action": next_action,
                "claim_allowed": False,
            }
        )
        rows.append(row)
    for source in p4_rows:
        row = base_row()
        row.update(
            {
                "row_id": source.get("row_id", "MISSING_P4_ID"),
                "operator_family": source.get("channel", ""),
                "coefficient_symbol": source.get("coefficient", ""),
                "candidate_value": source.get("status", ""),
                "candidate_units": source.get("units", ""),
                "normalization": "MISSING_CONNECTION_NORMALIZATION",
                "weak_field_map": "MISSING_WEP_CLOCK_LIGHTCONE_SPIN_SOURCE_MAP",
                "predicted_residual_or_bound_source": "MISSING_BOUND_OR_THEOREM_SOURCE",
                "source_file": str(OUT / "P8_Y5_PARENT_QLOC_1960_P4_CONNECTION_ENVELOPE_LEDGER.csv"),
                "ready_for_scoring": "false",
                "route_status": "P4_SUBROW_RETAINED_FOR_2042",
                "next_action": source.get("next_action", "fill or derive"),
                "claim_allowed": False,
            }
        )
        rows.append(row)
    return rows


def runner_refusal_rows() -> list[dict[str, object]]:
    data = [
        ("RUN2041_0_Lovelock_promotion", "claim EH from Lovelock implication alone", "REFUSED_PREMISE_UNSIGNED", "the theorem implication is clean but MTS has not signed metric-only/second-order/no-extra-field premises"),
        ("RUN2041_1_R2FR_absolute_zero", "promote R2/fR relative theorem to absolute c_R2=c_fR=0", "REFUSED_PARENT_SIGNATURE_MISSING", "962 is conditional; 964 and 965 leave legal countermodels"),
        ("RUN2041_2_R2FR_full_curve_claim", "score finite scalar branch as claim", "NOT_RUN_INPUTS_MISSING", "no parent-sourced c_R2/f_RR, alpha/lambda, screening or digitized full curve row"),
        ("RUN2041_3_Levi_Civita", "claim torsion/nonmetricity zero", "REFUSED_NO_HYPERMOMENTUM_UNSIGNED", "no-Gamma matter/source/readout and projective silence are still open"),
        ("RUN2041_4_local_GR", "claim derived local GR/Newton", "BLOCKED_NO_CLAIM", "EH/no-extra-field, connection, beta, conservation, common matter and measured-GM gates remain open"),
        ("RUN2041_5_GitHub", "publish or push checkpoint", "NOT_RUN_USER_EXCLUDED", "private work only; no GitHub action requested"),
    ]
    rows = []
    for row_id, branch, runner_status, reason in data:
        row = base_row()
        row.update(
            {
                "row_id": row_id,
                "branch": branch,
                "runner_status": runner_status,
                "reason": reason,
                "score_attempted": False,
                "claim_allowed": False,
            }
        )
        rows.append(row)
    return rows


def claim_gate_rows() -> list[dict[str, object]]:
    data = [
        ("GATE2041_0_no_extra_field", "metric-only second-order no-extra-field parent clause", "FAIL_BLOCKED", "not parent-derived; Lovelock route conditional only"),
        ("GATE2041_1_R2FR_zero", "absolute R2/fR zero", "FAIL_BLOCKED", "relative theorem exists but parent minimality/no-marker route failed"),
        ("GATE2041_2_connection", "Gamma=LC(g_obs) or connection silence", "FAIL_BLOCKED", "no independent connection/no-hypermomentum/projective silence not derived"),
        ("GATE2041_3_R11_rows", "executable R11/P4 fallback rows", "FAIL_BLOCKED", "R2/fR and torsion rows still missing coefficient, units, maps, bounds or source paths"),
        ("GATE2041_4_EH_operator", "EH+Lambda local operator", "FAIL_BLOCKED", "operator selection depends on unsigned premises"),
        ("GATE2041_5_local_GR", "derived local GR/Newton branch", "FAIL_BLOCKED", "left-hand operator, coupling, beta, conservation and measured-GM gates remain unresolved"),
        ("GATE2041_6_public_claim", "public PPN/R10/WEP/local-GR claim", "FAIL_BLOCKED", "private nonclaim checkpoint only"),
    ]
    rows = []
    for row_id, gate, status, detail in data:
        row = base_row()
        row.update(
            {
                "row_id": row_id,
                "gate": gate,
                "status": status,
                "detail": detail,
                "claim_allowed": False,
            }
        )
        rows.append(row)
    return rows


def decision_rows() -> list[dict[str, object]]:
    data = [
        (
            "DEC2041_0_no_extra_field",
            "The EH/no-extra-field theorem did not close.",
            "The exact contract is now written, but metric-only, second-order, no-marker, no-independent-connection and boundary silence remain unsigned.",
        ),
        (
            "DEC2041_1_R2FR",
            "R2/fR is boxed but not worth circling without new parent input.",
            "The relative zero theorem is real; the absolute parent minimality route failed; the finite branch is runner-ready only as nonclaim input acquisition.",
        ),
        (
            "DEC2041_2_connection",
            "Switch the next derivation attack to the connection/no-hypermomentum gate.",
            "This is the cleaner structural route to GR coupling: if matter/source/readout do not see independent Gamma, torsion/nonmetricity cannot quietly wreck clocks, WEP, spin, lightcones or source charge.",
        ),
        (
            "DEC2041_3_project_status",
            "This is not circling; it is dependency pruning.",
            "We have narrowed the GR reduction problem to a few named parent signatures. The next leap is to derive one of them, not retest a placeholder.",
        ),
    ]
    rows = []
    for row_id, decision, rationale in data:
        row = base_row()
        row.update(
            {
                "row_id": row_id,
                "decision": decision,
                "rationale": rationale,
                "claim_allowed": False,
            }
        )
        rows.append(row)
    return rows


def next_target_rows() -> list[dict[str, object]]:
    row = base_row()
    row.update(
        {
            "target_id": "NEXT2041_0_2042",
            "target_doc": "2042-Y5-R2FR-Levi-Civita-no-hypermomentum-parent-clause-or-P4-connection-row.md",
            "objective": "derive the parent no-independent-connection/no-hypermomentum clause forcing Gamma=LC(g_obs), or produce the first executable P4 torsion/nonmetricity row with coefficient, units, weak-field map, source path, and nonclaim bound interface",
            "must_include": "configuration-space descent; matter/source/readout deltaS/deltaGamma audit; Palatini-EH conditional route; projective trace silence; axial torsion, Weyl/shear nonmetricity and hypermomentum P4 rows; claim-gate refusal",
            "excluded": "local-GR claim; EH claim from Lovelock alone; R2/fR full-curve claim without parent coefficients; invented connection coefficients; GitHub; formalization-workbench edits",
            "claim_allowed": False,
        }
    )
    return [row]


def write_branch_copies(
    no_extra: list[dict[str, object]],
    priority_rows: list[dict[str, object]],
    connection_rows: list[dict[str, object]],
) -> list[dict[str, object]]:
    copies = [
        (
            "COPY2041_0_source_weight_no_extra",
            SOURCE_WEIGHT_DOCS / "AFRAME_NO_EXTRA_FIELD_2041_NONCLAIM.csv",
            no_extra,
        ),
        (
            "COPY2041_1_wep_priority_r11",
            BRANCH_WEP / "P8_Y5_PARENT_QLOC_2041_R11_PRIORITY_FILL_NONCLAIM.csv",
            priority_rows,
        ),
        (
            "COPY2041_2_rab_connection_next",
            QUEUE / "JR2041_LEVI_CIVITA_NO_HYPERMOMENTUM_NEXT_NONCLAIM.csv",
            connection_rows,
        ),
    ]
    rows = []
    for copy_id, path, data in copies:
        write_csv(path, data)
        row = base_row()
        row.update(
            {
                "copy_id": copy_id,
                "path": str(path),
                "rows": len(data),
                "status": "WRITTEN_NONCLAIM_COPY",
            }
        )
        rows.append(row)
    return rows


def validation_rows(
    source_rows: list[dict[str, object]],
    no_extra: list[dict[str, object]],
    r2fr: list[dict[str, object]],
    connection: list[dict[str, object]],
    priority: list[dict[str, object]],
    runner: list[dict[str, object]],
    gates: list[dict[str, object]],
    next_rows_: list[dict[str, object]],
    csv_paths: list[Path],
) -> list[dict[str, object]]:
    no_extra_verdict = next(row for row in no_extra if row["row_id"] == "NEF2041_7_verdict")
    r2fr_route = next(row for row in r2fr if row["row_id"] == "R2FR2041_3_route_decision")
    connection_verdict = next(row for row in connection if row["row_id"] == "LC2041_5_verdict")
    local_gate = next(row for row in gates if row["row_id"] == "GATE2041_5_local_GR")
    checks: list[tuple[str, bool, str]] = []
    checks.append(("VAL2041_00_sources_exist", all(row["status"] == "EXISTS_NEEDLES_CONFIRMED" for row in source_rows), "all cited local source paths and needles exist"))
    checks.append(("VAL2041_01_csv_parse", all(csv_rows_parse(path) for path in csv_paths), "all generated CSV files parse cleanly"))
    checks.append(("VAL2041_02_no_extra_not_promoted", no_extra_verdict["status"] == "NOT_PARENT_DERIVED_CURRENT_CORPUS", "no-extra-field clause is not promoted"))
    checks.append(("VAL2041_03_R2FR_boxed_not_claimed", r2fr_route["status"] == "DEFER_DERIVATION_CIRCLE", "R2/fR is boxed and kept nonclaim rather than circled"))
    checks.append(("VAL2041_04_connection_selected", connection_verdict["status"] == "SELECTED_NEXT_BLOCKED_GATE", "connection/no-hypermomentum gate is selected next"))
    checks.append(("VAL2041_05_priority_rows_nonclaim", all(str(row.get("ready_for_scoring", "false")).lower() == "false" for row in priority), "priority R11/P4 rows remain nonclaim and not score-ready"))
    checks.append(("VAL2041_06_runner_blocks", all(str(row["runner_status"]).startswith(("REFUSED", "NOT_RUN", "BLOCKED")) for row in runner), "runner refuses Lovelock, R2/fR, connection, local-GR and GitHub shortcuts"))
    checks.append(("VAL2041_07_claim_gates_closed", local_gate["status"] == "FAIL_BLOCKED", "local-GR claim gate remains closed"))
    checks.append(("VAL2041_08_next_selected", next_rows_[0]["target_id"] == "NEXT2041_0_2042", "2042 Levi-Civita/no-hypermomentum target selected"))
    checks.append(("VAL2041_09_formalization_unchanged", count_formalization_modified() == 0, "formalization-workbench modified-file count remains 0"))
    checks.append(("VAL2041_10_no_formalization_2041_artifacts", not formalization_has_2041_artifacts(), "no 2041 artifacts were written under formalization-workbench"))
    checks.append(("VAL2041_11_no_pycache", not scripts_pycache_exists(), "scripts __pycache__ removed"))
    overall_ok = all(ok for _, ok, _ in checks)
    checks.append(("VAL2041_OVERALL", overall_ok, "2041 closes the no-extra-field attempt honestly and selects connection/no-hypermomentum next"))
    rows = []
    for check_id, ok, detail in checks:
        row = base_row()
        row.update(
            {
                "check_id": check_id,
                "status": "PASS" if ok else "FAIL",
                "detail": detail,
                "claim_allowed": False,
            }
        )
        rows.append(row)
    return rows


def write_doc(
    source_rows: list[dict[str, object]],
    no_extra: list[dict[str, object]],
    r2fr: list[dict[str, object]],
    connection: list[dict[str, object]],
    priority: list[dict[str, object]],
    runner: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_rows_: list[dict[str, object]],
    copies: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    sections = [
        "# 2041 Y5 R2FR Second-Order No-Extra-Field Parent Clause Or R11 Priority Fill",
        "",
        "## Current Verdict",
        "",
        "2041 takes the leap at the EH/no-extra-field door and does **not** force it. The Lovelock/EH implication is clean only if MTS parent-signs a local 4D metric-only, second-order, no-extra-field exterior branch. The current corpus does not yet sign those premises.",
        "",
        "The useful progress is sharper: `R2/fR` is boxed as a conditional scalar leak rather than a mystery, and the remaining structural danger is the connection/coupling side. The next best attack is therefore the Levi-Civita/no-hypermomentum parent clause: prove matter/source/readout do not see an independent `Gamma`, or build the first real P4 torsion/nonmetricity row. No local-GR, EH, PPN, R10, WEP, clock, orbital, GitHub, or public claim is made.",
        "",
        "## Source Register",
        md_table(source_rows, ["source_id", "source_path", "status", "note", "valid_for_claim"]),
        "## No-Extra-Field Clause Audit",
        md_table(no_extra, ["row_id", "clause", "mathematical_form", "status", "would_close", "blocker", "parent_signed", "claim_allowed"]),
        "## R2/fR Decision Ledger",
        md_table(r2fr, ["row_id", "target", "mathematical_content", "status", "useful_result", "blocker", "next_action", "claim_allowed"]),
        "## Connection / Levi-Civita Decision Ledger",
        md_table(connection, ["row_id", "target", "mathematical_content", "status", "useful_result", "blocker", "next_action", "claim_allowed"]),
        "## Priority R11/P4 Fill Interface",
        md_table(priority, ["row_id", "operator_family", "coefficient_symbol", "candidate_value", "candidate_units", "normalization", "weak_field_map", "predicted_residual_or_bound_source", "ready_for_scoring", "route_status", "next_action", "claim_allowed"]),
        "## Runner Refusals",
        md_table(runner, ["row_id", "branch", "runner_status", "reason", "score_attempted", "claim_allowed"]),
        "## Claim Gate",
        md_table(gates, ["row_id", "gate", "status", "detail", "claim_allowed"]),
        "## Decision Ledger",
        md_table(decisions, ["row_id", "decision", "rationale", "claim_allowed"]),
        "## Next Target",
        md_table(next_rows_, ["target_id", "target_doc", "objective", "must_include", "excluded", "claim_allowed"]),
        "## Branch Copies",
        md_table(copies, ["copy_id", "path", "rows", "status", "valid_for_claim"]),
        "## Validation",
        md_table(validation, ["check_id", "status", "detail", "claim_allowed"]),
    ]
    DOC.write_text("\n".join(sections), encoding="utf-8")


def main() -> None:
    source_rows = source_register_rows()
    no_extra = no_extra_field_audit_rows()
    r2fr = r2fr_decision_rows()
    connection = connection_decision_rows()
    priority = priority_r11_fill_rows()
    runner = runner_refusal_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_rows_ = next_target_rows()
    paths = {
        "sources": OUT / "P8_Y5_PARENT_QLOC_2041_SOURCE_REGISTER.csv",
        "no_extra": OUT / "P8_Y5_PARENT_QLOC_2041_NO_EXTRA_FIELD_PARENT_CLAUSE_AUDIT.csv",
        "r2fr": OUT / "P8_Y5_PARENT_QLOC_2041_R2FR_DECISION_LEDGER.csv",
        "connection": OUT / "P8_Y5_PARENT_QLOC_2041_TORSION_CONNECTION_DECISION_LEDGER.csv",
        "priority": OUT / "P8_Y5_PARENT_QLOC_2041_PRIORITY_R11_FILL_INTERFACE.csv",
        "runner": OUT / "P8_Y5_PARENT_QLOC_2041_RUNNER_REFUSALS.csv",
        "gates": OUT / "P8_Y5_PARENT_QLOC_2041_CLAIM_GATE.csv",
        "decision": OUT / "P8_Y5_PARENT_QLOC_2041_DECISION_LEDGER.csv",
        "next": OUT / "P8_Y5_PARENT_QLOC_2041_NEXT_TARGET.csv",
        "branch": OUT / "P8_Y5_PARENT_QLOC_2041_BRANCH_COPIES.csv",
        "validation": OUT / "P8_Y5_BRR545_2041_VALIDATION.csv",
    }
    write_csv(paths["sources"], source_rows)
    write_csv(paths["no_extra"], no_extra)
    write_csv(paths["r2fr"], r2fr)
    write_csv(paths["connection"], connection)
    write_csv(paths["priority"], priority)
    write_csv(paths["runner"], runner)
    write_csv(paths["gates"], gates)
    write_csv(paths["decision"], decisions)
    write_csv(paths["next"], next_rows_)
    copies = write_branch_copies(no_extra, priority, connection)
    write_csv(paths["branch"], copies)
    remove_pycache()
    csv_paths_without_validation = [path for key, path in paths.items() if key != "validation"] + [Path(row["path"]) for row in copies]
    validation = validation_rows(source_rows, no_extra, r2fr, connection, priority, runner, gates, next_rows_, csv_paths_without_validation)
    write_csv(paths["validation"], validation)
    csv_paths = list(paths.values()) + [Path(row["path"]) for row in copies]
    remove_pycache()
    validation = validation_rows(source_rows, no_extra, r2fr, connection, priority, runner, gates, next_rows_, csv_paths)
    write_csv(paths["validation"], validation)
    write_doc(source_rows, no_extra, r2fr, connection, priority, runner, gates, decisions, next_rows_, copies, validation)
    remove_pycache()


if __name__ == "__main__":
    main()
