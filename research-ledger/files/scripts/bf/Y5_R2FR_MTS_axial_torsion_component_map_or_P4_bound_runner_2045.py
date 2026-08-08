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


DOC = ROOT / "2045-Y5-R2FR-MTS-axial-torsion-component-map-or-P4-bound-runner.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
SCRIPT_PATH = Path(__file__).resolve()


def formalization_has_2045_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    try:
        artifact_patterns = (
            "*2045-Y5-R2FR*",
            "*P8_Y5_PARENT_QLOC_2045*",
            "*Y5_R2FR_MTS_axial_torsion_component_map_or_P4_bound_runner_2045*",
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
    local_specs = [
        (
            "SRC2045_00_2044_doc",
            ROOT / "2044-Y5-R2FR-sector-Gamma-slot-audit-or-first-numeric-P4-source.md",
            ["NEXT2044_0_2045", "P4SRC2044_0_KRT2008_axial_torsion_anchor", "VAL2044_OVERALL"],
            "2044 handoff: derive MTS axial torsion component map or keep P4 source nonclaim.",
        ),
        (
            "SRC2045_01_2044_next",
            OUT / "P8_Y5_PARENT_QLOC_2044_NEXT_TARGET.csv",
            ["NEXT2044_0_2045", "MTS axial torsion"],
            "machine-readable 2045 target.",
        ),
        (
            "SRC2045_02_2044_numeric",
            OUT / "P8_Y5_PARENT_QLOC_2044_NUMERIC_P4_SOURCE_ANCHORS.csv",
            ["P4SRC2044_0_KRT2008_axial_torsion_anchor", "1e-31"],
            "numeric torsion source anchor.",
        ),
        (
            "SRC2045_03_2044_mapping",
            OUT / "P8_Y5_PARENT_QLOC_2044_P4_MAPPING_REQUIREMENTS.csv",
            ["MAP2044_0_component_basis", "MAP2044_3_observable_kernel"],
            "mapping requirements that blocked 2044 scoring.",
        ),
        (
            "SRC2045_04_2043_p4_rows",
            OUT / "P8_Y5_PARENT_QLOC_2043_FIRST_P4_BOUND_ROWS.csv",
            ["P4B2043_0_hypermomentum", "P4B2043_1_axial_torsion"],
            "first P4 fallback row templates.",
        ),
        (
            "SRC2045_05_2042_p4_interface",
            OUT / "P8_Y5_PARENT_QLOC_2042_P4_CONNECTION_INTERFACE.csv",
            ["P4C1960_1_axial_torsion", "P4C1960_5_hypermomentum"],
            "P4 connection interface.",
        ),
        (
            "SRC2045_06_1340_R11_interface",
            ROOT / "1340-Y5-R10-RAB-EH-core-selection-or-first-executable-R11-residual-interface.md",
            ["R11SCHEMA1340_2_connection", "R11RUN1340_2_connection_prediction_required", "VAL1340_11_overall"],
            "strict R11 connection runner interface.",
        ),
        (
            "SRC2045_07_1960_p4",
            OUT / "P8_Y5_PARENT_QLOC_1960_P4_CONNECTION_ENVELOPE_LEDGER.csv",
            ["P4C1960_1_axial_torsion", "P4C1960_5_hypermomentum"],
            "current P4 subrow ledger.",
        ),
    ]
    rows: list[dict[str, object]] = []
    for source_id, path, needles, note in local_specs:
        exists = path.exists()
        text = read_text(path) if exists else ""
        ok = exists and all(needle in text for needle in needles)
        row = base_row()
        row.update(
            {
                "source_id": source_id,
                "source_kind": "local",
                "source_path": str(path),
                "source_url": "",
                "status": "EXISTS_NEEDLES_CONFIRMED" if ok else "MISSING_OR_NEEDLE_FAIL",
                "needles": ";".join(needles),
                "note": note,
            }
        )
        rows.append(row)
    for source_id, source_url, doi, note in [
        (
            "SRC2045_EXT_00_KRT2008_torsion",
            "https://arxiv.org/abs/0712.4393",
            "https://doi.org/10.1103/PhysRevLett.100.111102",
            "Kostelecky/Russell/Tasson torsion-component constraints; usable only after MTS-to-component map and coupling convention exist.",
        ),
        (
            "SRC2045_EXT_01_Terrano2015_spin",
            "https://arxiv.org/abs/1508.02463",
            "https://doi.org/10.1103/PhysRevLett.115.201801",
            "spin-dependent experiment context; not a direct MTS axial torsion component bound.",
        ),
    ]:
        row = base_row()
        row.update(
            {
                "source_id": source_id,
                "source_kind": "external_web_record",
                "source_path": "",
                "source_url": source_url,
                "status": "SOURCE_STRING_RECORDED_NONCLAIM",
                "needles": doi,
                "note": note,
            }
        )
        rows.append(row)
    return rows


def conditional_component_map_rows() -> list[dict[str, object]]:
    data = [
        (
            "MAP2045_0_affine_torsion",
            "define MTS affine torsion",
            "T_MTS^lambda_{mu nu} := 2 Gamma_MTS^lambda_{[mu nu]} for the same observed local connection branch.",
            "CONDITIONAL_DEFINITION",
            "exact if Gamma_MTS is a parent-owned affine connection",
            "MISSING_GAMMA_MTS_AFFINE_CONNECTION_OWNER",
        ),
        (
            "MAP2045_1_axial_projection",
            "project axial torsion vector",
            "A_MTS^mu := (1/6) epsilon^{alpha beta gamma mu} T_MTS_{alpha beta gamma} in the chosen orientation/sign convention.",
            "CONDITIONAL_GEOMETRIC_MAP",
            "gives the axial irreducible component candidate",
            "MISSING_ORIENTATION_SIGNATURE_AND_INDEX_CONVENTION",
        ),
        (
            "MAP2045_2_KRT_basis",
            "identify KRT axial component",
            "A_MTS^mu must equal C_basis * A_KRT^mu in the KRT irreducible torsion basis before using KRT bounds.",
            "CONDITIONAL_BASIS_MAP",
            "turns the external bound into a component comparison",
            "MISSING_C_BASIS_AND_COMPONENT_LABELS",
        ),
        (
            "MAP2045_3_coupling_kernel",
            "map torsion component to spin observable",
            "b_eff^mu or equivalent spin-coupling coefficient = xi_A * A_MTS^mu + other torsion pieces; xi_A must match the KRT convention.",
            "CONDITIONAL_COUPLING_MAP",
            "prevents using a geometric torsion bound as if it were already an MTS force coefficient",
            "MISSING_XI_A_AND_OTHER_COMPONENT_MIXING",
        ),
        (
            "MAP2045_4_units",
            "put MTS component in GeV or declared normalized units",
            "A_KRT_component_GeV = U_A * c_A * S_mu^MTS_component, with U_A declared from the parent action normalization.",
            "CONDITIONAL_UNIT_MAP",
            "makes comparison dimensionally meaningful",
            "MISSING_U_A_C_A_S_MU_UNITS",
        ),
        (
            "MAP2045_5_lab_frame",
            "frame and time dependence",
            "component must be expressed in the same lab/Sun-centered frame and time convention as the external torsion limits.",
            "CONDITIONAL_FRAME_MAP",
            "stops orientation-dependent constraints being treated as scalar bounds",
            "MISSING_FRAME_ROTATION_AND_COMPONENT_SELECTION",
        ),
        (
            "MAP2045_6_envelope",
            "absolute no-cancellation envelope",
            "abs(A_MTS_component) <= abs(C_basis^{-1}) * bound_component, with all unmapped components retained in an absolute residual envelope.",
            "SCHEMA_READY_NOT_SCOREABLE",
            "safe shape for future runner",
            "MISSING_NUMERIC_COMPONENT_MAP_AND_ACTIVE_MTS_VALUE",
        ),
        (
            "MAP2045_7_verdict",
            "MTS-to-KRT axial torsion map",
            "MAP2045_0 through MAP2045_6 all source-backed and convention-locked.",
            "NOT_DERIVED_CURRENT_CORPUS",
            "would let the KRT anchor become a real P4 bound input",
            "MTS torsion variable, normalization, coupling and frame map are still missing",
        ),
    ]
    rows = []
    for row_id, map_piece, formula, status, if_closed, blocker in data:
        row = base_row()
        row.update(
            {
                "row_id": row_id,
                "map_piece": map_piece,
                "formula": formula,
                "status": status,
                "if_closed": if_closed,
                "blocker": blocker,
                "claim_allowed": False,
            }
        )
        rows.append(row)
    return rows


def mts_variable_requirement_rows() -> list[dict[str, object]]:
    data = [
        ("REQ2045_0_Gamma_MTS", "Gamma_MTS^lambda_{mu nu}", "parent-owned observed affine connection or proof no independent Gamma exists", "MISSING_PARENT_INPUT", "without this, torsion tensor is not defined"),
        ("REQ2045_1_T_MTS", "T_MTS^lambda_{mu nu}", "antisymmetric part of Gamma_MTS with index/sign convention", "MISSING_DERIVED_TENSOR", "needed before axial projection"),
        ("REQ2045_2_S_mu", "S_mu^MTS or A_mu^MTS", "declared axial torsion vector or hypermomentum-to-axial projection", "MISSING_COMPONENT_DEFINITION", "current c_A/S_mu label is a placeholder"),
        ("REQ2045_3_c_A", "c_A", "coefficient connecting MTS axial variable to matter spin coupling", "MISSING_COEFFICIENT_VALUE_AND_UNITS", "needed for observable kernel"),
        ("REQ2045_4_xi_A", "xi_A", "convention factor between geometric axial torsion and KRT fermion-coupling basis", "MISSING_COUPLING_CONVENTION", "prevents direct comparison to KRT table"),
        ("REQ2045_5_frame", "R_lab<-MTS", "frame rotation/component selection from MTS local frame to KRT/Sun-centered/lab frame", "MISSING_FRAME_MAP", "torsion bounds are component-frame dependent"),
        ("REQ2045_6_observable_kernel", "K_obs^A", "kernel to WEP/clock/source/orbit residuals", "MISSING_OBSERVABLE_KERNEL", "needed for local-GR empirical branch"),
        ("REQ2045_7_bound_row", "B_A", "component-specific KRT bound row with component label and confidence", "ANCHOR_ONLY_NONCLAIM", "abstract order-of-magnitude is not a full table row"),
    ]
    rows = []
    for row_id, symbol, requirement, status, rationale in data:
        row = base_row()
        row.update(
            {
                "row_id": row_id,
                "symbol": symbol,
                "requirement": requirement,
                "status": status,
                "rationale": rationale,
                "claim_allowed": False,
            }
        )
        rows.append(row)
    return rows


def p4_bound_runner_input_rows() -> list[dict[str, object]]:
    rows = []
    for source in read_csv_dicts(OUT / "P8_Y5_PARENT_QLOC_2044_NUMERIC_P4_SOURCE_ANCHORS.csv"):
        row = base_row()
        row.update(
            {
                "row_id": source.get("row_id", "MISSING_SOURCE_ROW"),
                "channel": source.get("channel", ""),
                "coefficient": source.get("coefficient", ""),
                "bound_value": source.get("bound_value", ""),
                "bound_units": source.get("bound_units", ""),
                "source_url": source.get("source_url", ""),
                "source_ref": source.get("source_ref", ""),
                "mts_prediction_value": "MISSING_A_MTS_COMPONENT_VALUE",
                "mts_prediction_units": "MISSING_GEVMAP_OR_NORMALIZATION",
                "component_label": "MISSING_KRT_COMPONENT_LABEL",
                "basis_map": "MISSING_C_BASIS",
                "observable_kernel": "MISSING_XI_A_AND_K_OBS",
                "frame_map": "MISSING_FRAME_MAP",
                "ready_for_scoring": False,
                "claim_allowed": False,
            }
        )
        rows.append(row)
    return rows


def runner_dryrun_rows(input_rows: list[dict[str, object]]) -> list[dict[str, object]]:
    rows = []
    required = [
        "mts_prediction_value",
        "mts_prediction_units",
        "component_label",
        "basis_map",
        "observable_kernel",
        "frame_map",
    ]
    for index, source in enumerate(input_rows):
        missing = [field for field in required if str(source.get(field, "")).startswith("MISSING")]
        row = base_row()
        row.update(
            {
                "run_id": f"RUN2045_{index}",
                "input_id": source["row_id"],
                "channel": source["channel"],
                "bound_value": source["bound_value"],
                "bound_units": source["bound_units"],
                "accepted_for_scoring": False,
                "verdict": "REJECTED_MTS_COMPONENT_MAP_MISSING",
                "missing_fields": ";".join(missing),
                "reason": "external bound anchor exists but MTS axial torsion component, units, basis, frame and observable kernel are missing",
                "claim_allowed": False,
            }
        )
        rows.append(row)
    verdict = base_row()
    verdict.update(
        {
            "run_id": "RUN2045_VERDICT",
            "input_id": "all_axial_torsion_rows",
            "channel": "axial_torsion_spin_coupling",
            "bound_value": "1e-31_anchor_order",
            "bound_units": "GeV_anchor_order",
            "accepted_for_scoring": False,
            "verdict": "AXIAL_TORSION_BOUND_RUNNER_BLOCKED_NONCLAIM",
            "missing_fields": "MTS_Gamma_T_A_coupling_units_frame_kernel",
            "reason": "the KRT source is useful, but MTS has no scoreable prediction in that basis",
            "claim_allowed": False,
        }
    )
    rows.append(verdict)
    return rows


def claim_gate_rows() -> list[dict[str, object]]:
    data = [
        ("GATE2045_0_torsion_tensor", "MTS torsion tensor is defined", "FAIL_BLOCKED", "Gamma_MTS affine connection owner or LC-zero theorem missing"),
        ("GATE2045_1_axial_map", "MTS axial component maps to KRT basis", "FAIL_BLOCKED", "basis/sign/orientation/coupling convention missing"),
        ("GATE2045_2_units", "MTS prediction is in GeV/component units", "FAIL_BLOCKED", "c_A/S_mu units and normalization missing"),
        ("GATE2045_3_bound_score", "KRT bound can score MTS axial torsion", "FAIL_BLOCKED", "external anchor exists but MTS component map is absent"),
        ("GATE2045_4_connection_gate", "torsion/nonmetricity connection gate closes", "FAIL_BLOCKED", "P4 rows are retained, not bounded"),
        ("GATE2045_5_local_GR_Newton", "derived local GR/Newton branch", "FAIL_BLOCKED", "connection gate and other EH/GM/PPN gates remain unresolved"),
        ("GATE2045_6_public_claim", "public torsion/local-GR claim", "FAIL_BLOCKED", "private nonclaim checkpoint only"),
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
            "DEC2045_0_map_result",
            "The geometric axial projection map is written only conditionally.",
            "If MTS supplies a parent-owned affine torsion tensor, the axial vector projection is straightforward; current corpus does not supply the tensor or normalization.",
        ),
        (
            "DEC2045_1_bound_result",
            "The KRT torsion bound remains a source-backed anchor, not an MTS score.",
            "Without c_A/S_mu units, component labels, frame map and coupling kernel, using the 1e-31 GeV anchor would be a category error.",
        ),
        (
            "DEC2045_2_best_next",
            "Next target should define or kill Gamma_MTS itself.",
            "Either derive Gamma_MTS=LC(g_obs) and torsion vanishes, or define the parent affine residual tensor so P4 can become numerical.",
        ),
        (
            "DEC2045_3_project_status",
            "This improves testability even though it blocks the claim.",
            "The external bound now has a precise missing-input interface rather than being a decorative citation.",
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
            "target_id": "NEXT2045_0_2046",
            "target_doc": "2046-Y5-R2FR-GammaMTS-affine-torsion-definition-or-LC-zero-theorem.md",
            "objective": "derive whether the MTS local connection is exactly LC(g_obs), or define the parent affine residual Gamma_MTS and torsion tensor T_MTS with units/signs so the axial P4 map can become scoreable",
            "must_include": "Gamma_MTS owner; torsion tensor definition; LC-zero branch; affine residual branch; c_A/S_mu units; relation to hypermomentum; runner refusal if no tensor is defined",
            "excluded": "using KRT bound before MTS component exists; inventing c_A/S_mu values; claiming local GR from notation; GitHub; formalization-workbench edits",
            "claim_allowed": False,
        }
    )
    return [row]


def write_branch_copies(
    map_rows: list[dict[str, object]],
    runner_inputs: list[dict[str, object]],
    next_rows_: list[dict[str, object]],
) -> list[dict[str, object]]:
    copies = [
        (
            "COPY2045_0_source_weight_axial_map",
            SOURCE_WEIGHT_DOCS / "AFRAME_AXIAL_TORSION_COMPONENT_MAP_2045_NONCLAIM.csv",
            map_rows,
        ),
        (
            "COPY2045_1_wep_axial_runner_inputs",
            BRANCH_WEP / "P8_Y5_PARENT_QLOC_2045_AXIAL_TORSION_RUNNER_INPUTS_NONCLAIM.csv",
            runner_inputs,
        ),
        (
            "COPY2045_2_rab_next",
            QUEUE / "JR2045_GAMMA_MTS_TORSION_DEFINITION_NEXT_NONCLAIM.csv",
            next_rows_,
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
    sources: list[dict[str, object]],
    map_rows: list[dict[str, object]],
    req_rows: list[dict[str, object]],
    runner_inputs: list[dict[str, object]],
    runner_rows: list[dict[str, object]],
    gates: list[dict[str, object]],
    next_rows_: list[dict[str, object]],
    csv_paths: list[Path],
) -> list[dict[str, object]]:
    local_sources_ok = all(
        row["status"] == "EXISTS_NEEDLES_CONFIRMED"
        for row in sources
        if row["source_kind"] == "local"
    )
    external_sources_ok = all(
        str(row["source_url"]).startswith("https://") and row["status"] == "SOURCE_STRING_RECORDED_NONCLAIM"
        for row in sources
        if row["source_kind"] == "external_web_record"
    )
    map_verdict = next(row for row in map_rows if row["row_id"] == "MAP2045_7_verdict")
    req_gamma = next(row for row in req_rows if row["row_id"] == "REQ2045_0_Gamma_MTS")
    runner_verdict = next(row for row in runner_rows if row["run_id"] == "RUN2045_VERDICT")
    local_gate = next(row for row in gates if row["row_id"] == "GATE2045_5_local_GR_Newton")
    checks: list[tuple[str, bool, str]] = []
    checks.append(("VAL2045_00_local_sources_exist", local_sources_ok, "all cited local source paths and needles exist"))
    checks.append(("VAL2045_01_external_sources_recorded", external_sources_ok, "external source URLs/DOIs recorded as nonclaim provenance"))
    checks.append(("VAL2045_02_csv_parse", all(csv_rows_parse(path) for path in csv_paths), "all generated CSV files parse cleanly"))
    checks.append(("VAL2045_03_map_not_promoted", map_verdict["status"] == "NOT_DERIVED_CURRENT_CORPUS", "axial component map is not promoted"))
    checks.append(("VAL2045_04_gamma_missing", req_gamma["status"] == "MISSING_PARENT_INPUT", "Gamma_MTS owner remains missing"))
    checks.append(("VAL2045_05_runner_inputs_nonclaim", all(not bool(row.get("ready_for_scoring")) for row in runner_inputs), "runner inputs remain nonclaim"))
    checks.append(("VAL2045_06_runner_rejects", runner_verdict["verdict"] == "AXIAL_TORSION_BOUND_RUNNER_BLOCKED_NONCLAIM", "bound runner rejects missing MTS map"))
    checks.append(("VAL2045_07_claim_gates_closed", local_gate["status"] == "FAIL_BLOCKED", "local-GR/Newton claim gate remains closed"))
    checks.append(("VAL2045_08_next_selected", next_rows_[0]["target_id"] == "NEXT2045_0_2046", "2046 GammaMTS torsion definition target selected"))
    checks.append(("VAL2045_09_formalization_unchanged", count_formalization_modified() == 0, "formalization-workbench modified-file count remains 0"))
    checks.append(("VAL2045_10_no_formalization_2045_artifacts", not formalization_has_2045_artifacts(), "no 2045 artifacts were written under formalization-workbench"))
    checks.append(("VAL2045_11_no_pycache", not scripts_pycache_exists(), "scripts __pycache__ removed"))
    overall_ok = all(ok for _, ok, _ in checks)
    checks.append(("VAL2045_OVERALL", overall_ok, "2045 writes the conditional axial torsion map and blocks scoring until GammaMTS exists"))
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
    sources: list[dict[str, object]],
    map_rows: list[dict[str, object]],
    req_rows: list[dict[str, object]],
    runner_inputs: list[dict[str, object]],
    runner_rows: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_rows_: list[dict[str, object]],
    copies: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    sections = [
        "# 2045 Y5 R2FR MTS Axial Torsion Component Map Or P4 Bound Runner",
        "",
        "## Current Verdict",
        "",
        "2045 writes the conditional projection bridge from an MTS affine torsion tensor to an external axial torsion-component bound. The bridge is simple only after the missing object exists: `T_MTS^lambda_{mu nu}=2 Gamma_MTS^lambda_{[mu nu]}`, then `A_MTS^mu=(1/6) epsilon^{alpha beta gamma mu} T_MTS_{alpha beta gamma}`, then a convention-locked map to the KRT component basis.",
        "",
        "Current MTS does not yet define `Gamma_MTS`, `T_MTS`, `S_mu`, `c_A`, the coupling factor, units, or lab-frame component map. So the KRT `1e-31 GeV` source remains valuable but nonclaim. No local-GR, Newton, WEP, clock, orbital, PPN, R10, torsion, GitHub, or public claim is made.",
        "",
        "## Source Register",
        md_table(sources, ["source_id", "source_kind", "source_path", "source_url", "status", "note", "valid_for_claim"]),
        "## Conditional Component Map",
        md_table(map_rows, ["row_id", "map_piece", "formula", "status", "if_closed", "blocker", "claim_allowed"]),
        "## MTS Variable Requirements",
        md_table(req_rows, ["row_id", "symbol", "requirement", "status", "rationale", "claim_allowed"]),
        "## P4 Bound Runner Inputs",
        md_table(runner_inputs, ["row_id", "channel", "coefficient", "bound_value", "bound_units", "mts_prediction_value", "mts_prediction_units", "component_label", "basis_map", "observable_kernel", "frame_map", "ready_for_scoring", "claim_allowed"]),
        "## Runner Dry Run",
        md_table(runner_rows, ["run_id", "input_id", "channel", "bound_value", "bound_units", "accepted_for_scoring", "verdict", "missing_fields", "reason", "claim_allowed"]),
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
    sources = source_register_rows()
    map_rows = conditional_component_map_rows()
    req_rows = mts_variable_requirement_rows()
    runner_inputs = p4_bound_runner_input_rows()
    runner_rows = runner_dryrun_rows(runner_inputs)
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_rows_ = next_target_rows()
    paths = {
        "sources": OUT / "P8_Y5_PARENT_QLOC_2045_SOURCE_REGISTER.csv",
        "map": OUT / "P8_Y5_PARENT_QLOC_2045_CONDITIONAL_COMPONENT_MAP.csv",
        "requirements": OUT / "P8_Y5_PARENT_QLOC_2045_MTS_VARIABLE_REQUIREMENTS.csv",
        "inputs": OUT / "P8_Y5_PARENT_QLOC_2045_P4_BOUND_RUNNER_INPUTS.csv",
        "runner": OUT / "P8_Y5_PARENT_QLOC_2045_RUNNER_DRYRUN.csv",
        "gates": OUT / "P8_Y5_PARENT_QLOC_2045_CLAIM_GATE.csv",
        "decision": OUT / "P8_Y5_PARENT_QLOC_2045_DECISION_LEDGER.csv",
        "next": OUT / "P8_Y5_PARENT_QLOC_2045_NEXT_TARGET.csv",
        "branch": OUT / "P8_Y5_PARENT_QLOC_2045_BRANCH_COPIES.csv",
        "validation": OUT / "P8_Y5_BRR545_2045_VALIDATION.csv",
    }
    write_csv(paths["sources"], sources)
    write_csv(paths["map"], map_rows)
    write_csv(paths["requirements"], req_rows)
    write_csv(paths["inputs"], runner_inputs)
    write_csv(paths["runner"], runner_rows)
    write_csv(paths["gates"], gates)
    write_csv(paths["decision"], decisions)
    write_csv(paths["next"], next_rows_)
    copies = write_branch_copies(map_rows, runner_inputs, next_rows_)
    write_csv(paths["branch"], copies)
    remove_pycache()
    csv_paths_without_validation = [path for key, path in paths.items() if key != "validation"] + [Path(row["path"]) for row in copies]
    validation = validation_rows(sources, map_rows, req_rows, runner_inputs, runner_rows, gates, next_rows_, csv_paths_without_validation)
    write_csv(paths["validation"], validation)
    csv_paths = list(paths.values()) + [Path(row["path"]) for row in copies]
    remove_pycache()
    validation = validation_rows(sources, map_rows, req_rows, runner_inputs, runner_rows, gates, next_rows_, csv_paths)
    write_csv(paths["validation"], validation)
    write_doc(sources, map_rows, req_rows, runner_inputs, runner_rows, gates, decisions, next_rows_, copies, validation)
    remove_pycache()


if __name__ == "__main__":
    main()
