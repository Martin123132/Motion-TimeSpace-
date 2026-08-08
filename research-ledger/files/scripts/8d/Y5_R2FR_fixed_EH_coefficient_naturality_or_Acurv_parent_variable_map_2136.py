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


DOC = ROOT / "2136-Y5-R2FR-fixed-EH-coefficient-naturality-or-Acurv-parent-variable-map.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"

CSV_2135_NEXT = OUT / "P8_Y5_PARENT_QLOC_2135_NEXT_TARGET.csv"
CSV_2135_VAL = OUT / "P8_Y5_BRR545_2135_VALIDATION.csv"
CSV_2135_LEMMA = OUT / "P8_Y5_PARENT_QLOC_2135_NO_MIXED_CURVATURE_MORPHISM_ATTEMPT.csv"
CSV_2135_COUNTER = OUT / "P8_Y5_PARENT_QLOC_2135_CURVATURE_COUNTERMODEL_LEDGER.csv"
CSV_2135_OWNER = OUT / "P8_Y5_PARENT_QLOC_2135_FIRST_BETA_OWNER_ROUTE.csv"
CSV_2135_GATES = OUT / "P8_Y5_PARENT_QLOC_2135_CLAIM_GATES.csv"
DOC_2135 = ROOT / "2135-Y5-R2FR-no-mixed-curvature-morphism-lemma-or-first-beta-source-owner.md"
DOC_1017 = ROOT / "1017-Y5-R10-Hamiltonian-PiM-reference-lock-or-MHref-first-row.md"
DOC_1018 = ROOT / "1018-Y5-R10-sector-Lagrangian-boundary-owner-or-FB5540-source-row.md"
DOC_1027 = ROOT / "1027-Y5-R10-qbarXT-source-zero-or-bounded-coupling-row.md"
DOC_1028 = ROOT / "1028-Y5-R10-frame-marker-coupling-bound-input-pack-or-no-marker-theorem.md"
DOC_00 = ROOT / "00-pre-pivot-checkpoint.md"
DOC_01 = ROOT / "01-motion-load-route-contract.md"


def row(**kwargs: object) -> dict[str, object]:
    data = base_row()
    data["claim_allowed"] = False
    data.update(kwargs)
    return data


def truthy(value: object) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"true", "1", "yes", "pass", "valid"}


def formalization_has_2136_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    patterns = (
        "*2136-Y5-R2FR*",
        "*P8_Y5_PARENT_QLOC_2136*",
        "*Y5_R2FR_fixed_EH_coefficient_naturality_or_Acurv_parent_variable_map_2136*",
        "*AFRAME_FIXED_EH_COEFFICIENT_2136*",
        "*JR2136*",
    )
    try:
        return any(path.is_file() for pattern in patterns for path in FORMALIZATION.rglob(pattern))
    except Exception:
        return False


def source_register_rows() -> list[dict[str, object]]:
    specs = [
        ("SRC2136_00_2135_next", CSV_2135_NEXT, ["NEXT2135_0_2136", "fixed-EH"], "2135 handoff selects fixed EH coefficient or A_curv parent map."),
        ("SRC2136_01_2135_validation", CSV_2135_VAL, ["VAL2135_OVERALL", "PASS"], "2135 validation passed."),
        ("SRC2136_02_2135_lemma", CSV_2135_LEMMA, ["NMC2135_1_constant_EH_case", "EXACT_CONDITIONAL_THEOREM"], "2135 fixed EH coefficient conditional theorem."),
        ("SRC2136_03_2135_counter", CSV_2135_COUNTER, ["CM2135_0_nonminimal_hidden_scalar", "LIVE"], "2135 nonminimal hidden scalar countermodel remains live."),
        ("SRC2136_04_2135_owner", CSV_2135_OWNER, ["OWNER2135_1_proxy_sector", "A_curv_aux_2135"], "2135 canonical proxy owner route."),
        ("SRC2136_05_2135_gates", CSV_2135_GATES, ["GATE2135_7_local_GR_Newton_PPN_claim", "False"], "2135 keeps local-GR/Newton/PPN blocked."),
        ("SRC2136_06_2135_doc", DOC_2135, ["A_curv_aux_2135", "scalar-tensor style countermodel"], "2135 prose records proxy owner and countermodel."),
        ("SRC2136_07_1017_MHref", DOC_1017, ["M_H_ref = G_ref^-1", "MISSING_STABLE_MH_REF"], "1017 shows same-frame source denominator/G_ref bridge is missing."),
        ("SRC2136_08_1018_owner", DOC_1018, ["M_H_ref=G_ref^-1", "not_signed"], "1018 shows local-GR source charge owner map is unsigned."),
        ("SRC2136_09_1027_common_weyl", DOC_1027, ["CE1027_0_common_Weyl", "common nonzero source charge"], "1027 common frame/Weyl coupling blocks source-zero by WEP alone."),
        ("SRC2136_10_1028_no_marker", DOC_1028, ["no-marker/constant-descent route is clean as a conditional theorem but not parent-signed", "local-GR/Newton"], "1028 constants/markers descent is conditional only."),
        ("SRC2136_11_pre_pivot_Acurv", DOC_00, ["A_curv/(A_curv+5)", "motion capacity/load"], "pre-pivot A_curv appears as motion-load/empirical curvature response, not a parent auxiliary owner."),
        ("SRC2136_12_route_Acurv", DOC_01, ["A_curv/(A_curv+5)", "v_load^2 = 2GM/r"], "motion-load route contains A_curv notation and Newtonian load relation."),
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


def fixed_eh_rows() -> list[dict[str, object]]:
    return [
        row(
            theorem_id="FEH2136_0_target",
            claim_piece="fixed observed EH coefficient",
            mathematical_form="Coeff(R[g_obs]) = 1/(2 kappa_0), with kappa_0 a terminal parent datum independent of C_hid, source markers, readout frame, and local domain",
            proof_status="TARGET_SHARP",
            derivation_result="this would kill beta_A and prevent F(I_hid)R at the coefficient level",
            blocker="none at definition level",
            valid_for_claim=False,
        ),
        row(
            theorem_id="FEH2136_1_exact_conditional",
            claim_piece="terminal coefficient theorem",
            mathematical_form="S_grav[q(Phi)] = (1/2 kappa_0) int mu_obs(q) R[g_obs(q)] + boundary, with delta_v kappa_0 = 0 and no hidden scalar in mu_obs or g_obs",
            proof_status="EXACT_CONDITIONAL_THEOREM",
            derivation_result="if parent-signed, vertical hidden variations cannot create beta_A A R or F(I_hid)R",
            blocker="current corpus has not signed kappa_0 as the only curvature coefficient owner",
            valid_for_claim=False,
        ),
        row(
            theorem_id="FEH2136_2_units_not_physics",
            claim_piece="constant units are not a proof of constant coupling",
            mathematical_form="choosing G=1 or kappa_0=1 fixes notation, not the parent functional dependence of measured G_N or Coeff(R)",
            proof_status="NOT_A_ZERO_PROOF",
            derivation_result="a hidden scalar can be hidden by units/frame choices unless source charge and readout maps are fixed",
            blocker="same-frame M_H_ref/G_ref and source-readout bridge are unsigned",
            valid_for_claim=False,
        ),
        row(
            theorem_id="FEH2136_3_source_normalization_guard",
            claim_piece="measured Newton coefficient requires source denominator",
            mathematical_form="GM_orbit = G_ref M_H_ref only after Q_tau integral, tau lock, Gauss/Poisson/readout and same-frame M_H_ref are derived",
            proof_status="UNSIGNED_SOURCE_BRIDGE",
            derivation_result="constant EH coefficient cannot be promoted to derived Newton/GR reduction until the source side is also owned",
            blocker="1017/1018 keep M_H_ref and owner map blocked",
            valid_for_claim=False,
        ),
        row(
            theorem_id="FEH2136_4_frame_marker_obstruction",
            claim_piece="frame/marker dependence can mimic variable curvature coupling",
            mathematical_form="common Weyl/disformal factors or marker constants can move F(I)R into matter/source/readout coefficients",
            proof_status="OBSTRUCTION_LIVE",
            derivation_result="Einstein-frame rewriting is not harmless unless matter/source/readout descent and no-marker constants are parent-signed",
            blocker="1027/1028 retain common frame and no-marker gaps",
            valid_for_claim=False,
        ),
        row(
            theorem_id="FEH2136_5_verdict",
            claim_piece="prove fixed EH coefficient now",
            mathematical_form="FEH2136_1 plus FEH2136_3 plus FEH2136_4 closed => beta_A=0 and local Newton coefficient is parent-owned",
            proof_status="FIXED_EH_COEFFICIENT_NOT_PARENT_SIGNED",
            derivation_result="the theorem is the right route, but current evidence does not prove it",
            blocker="terminal kappa_0, source denominator, no-marker/frame descent, and measured-G bridge remain unsigned",
            valid_for_claim=False,
        ),
    ]


def acurv_map_rows() -> list[dict[str, object]]:
    return [
        row(map_id="MAP2136_0_proxy", candidate="A_curv_aux_2135", source_path=str(CSV_2135_OWNER), interpretation="canonical proxy for the first retained integrated-out auxiliary curvature scalar", map_status="PROXY_ONLY_NOT_PARENT_VARIABLE", reason="created to hold beta_A/M_A^2 interface after 2135; not yet identified with a real parent field", valid_for_claim=False),
        row(map_id="MAP2136_1_name_collision_A_curv", candidate="A_curv", source_path=str(DOC_00) + "; " + str(DOC_01), interpretation="motion-load/empirical curvature response amplitude in pre-pivot route", map_status="NAME_COLLISION_GUARDED", reason="A_curv notation exists, but no parent action term beta_A A_curv R, M_A^2, or normalization source ties it to A_curv_aux_2135", valid_for_claim=False),
        row(map_id="MAP2136_2_hidden_invariant", candidate="I_hid", source_path=str(CSV_2135_COUNTER), interpretation="generic surviving hidden scalar invariant that can generate F(I_hid)R", map_status="COUNTERMODEL_CLASS_NOT_VARIABLE_OWNER", reason="useful obstruction class, but not a concrete MTS sector with beta_A and M_A^2", valid_for_claim=False),
        row(map_id="MAP2136_3_marker_prefactor", candidate="sigma_marker/domain_marker", source_path=str(DOC_1028), interpretation="marker/constant descent obstruction that could feed coefficients", map_status="POSSIBLE_OWNER_CLASS_UNSIGNED", reason="no-marker theorem is conditional only and no specific sigma dynamics/source row is selected", valid_for_claim=False),
        row(map_id="MAP2136_4_common_frame", candidate="c_g/common Weyl frame", source_path=str(DOC_1027), interpretation="common matter-frame/source coupling residual", map_status="SOURCE_FRAME_RESIDUAL_NOT_CURVATURE_OWNER", reason="can change observed coupling/readout, but it is not yet the beta_A curvature coefficient owner", valid_for_claim=False),
        row(map_id="MAP2136_5_source_denominator", candidate="G_ref/M_H_ref/Q_tau", source_path=str(DOC_1017) + "; " + str(DOC_1018), interpretation="source-side Newton/G normalization bridge", map_status="NORMALIZATION_GATE_NOT_BETA_OWNER", reason="needed for measured Newton limit; cannot replace parent beta_A or M_A^2", valid_for_claim=False),
        row(map_id="MAP2136_6_verdict", candidate="actual A_curv parent variable", source_path="MISSING_PARENT_ACTION_SOURCE", interpretation="field/sector in parent action whose elimination gives beta_A A R", map_status="NOT_IDENTIFIED", reason="current corpus supplies a proxy and several obstruction classes, but no concrete parent variable with beta_A/M_A^2", valid_for_claim=False),
    ]


def beta_owner_update_rows() -> list[dict[str, object]]:
    return [
        row(field_id="BETA2136_0_owner_proxy", field="canonical_proxy_sector_id", value="A_curv_aux_2135", required_for_claim="replace proxy with actual parent variable/sector path", current_status="PROXY_RETAINED", valid_for_claim=False),
        row(field_id="BETA2136_1_parent_variable", field="actual_parent_variable", value="MISSING_PARENT_VARIABLE", required_for_claim="source path and equation where the variable appears in the parent action", current_status="BLOCKS_OWNER_MAP", valid_for_claim=False),
        row(field_id="BETA2136_2_beta", field="beta_A", value="MISSING_BETA_A", required_for_claim="parent coefficient or theorem-zero with units/sign", current_status="BLOCKS_C_R2_AUX", valid_for_claim=False),
        row(field_id="BETA2136_3_mass", field="M_A^2_or_constraint", value="MISSING_M_A2_OR_CONSTRAINT", required_for_claim="Hessian/mass row or pure-constraint theorem", current_status="BLOCKS_C_R2_AUX", valid_for_claim=False),
        row(field_id="BETA2136_4_normalization", field="EH_normalization_conversion", value="MISSING_NORMALIZATION", required_for_claim="conversion to S=(1/2kappa) int sqrt(-g)(R+c_R2 R^2)", current_status="BLOCKS_UNITS", valid_for_claim=False),
        row(field_id="BETA2136_5_source_readout", field="source_readout_projection", value="MISSING_SOURCE_READOUT_MAP", required_for_claim="PPN/R10/clock/orbital/local residual projection", current_status="BLOCKS_TESTING", valid_for_claim=False),
        row(field_id="BETA2136_6_name_guard", field="A_curv_name_collision_guard", value="ACTIVE", required_for_claim="do not equate empirical A_curv with A_curv_aux_2135 without parent action bridge", current_status="SAFETY_GUARD", valid_for_claim=False),
    ]


def claim_gate_rows() -> list[dict[str, object]]:
    return [
        row(gate_id="GATE2136_0_sources", gate="all source rows loaded", gate_pass=True, rationale="source register checks 2135 plus source-normalization/no-marker/A_curv evidence"),
        row(gate_id="GATE2136_1_fixed_EH_shape", gate="fixed EH coefficient theorem shape exists", gate_pass=True, rationale="terminal kappa_0 would kill beta_A if parent-signed"),
        row(gate_id="GATE2136_2_fixed_EH_parent_signed", gate="fixed EH coefficient is parent-signed", gate_pass=False, rationale="terminal kappa_0/source bridge/no-marker/frame clauses are unsigned"),
        row(gate_id="GATE2136_3_units_shortcut_rejected", gate="constant units accepted as proof", gate_pass=False, rationale="G=1 or kappa=1 is notation, not a parent coefficient theorem"),
        row(gate_id="GATE2136_4_Acurv_actual_variable", gate="A_curv_aux_2135 mapped to actual parent variable", gate_pass=False, rationale="only a proxy and name-collision guard exist"),
        row(gate_id="GATE2136_5_Acurv_name_guard", gate="empirical A_curv not misused as beta owner", gate_pass=True, rationale="motion-load A_curv is quarantined until a parent action bridge exists"),
        row(gate_id="GATE2136_6_beta_owner_executable", gate="beta owner row executable", gate_pass=False, rationale="actual parent variable, beta_A, M_A^2, normalization and projections are missing"),
        row(gate_id="GATE2136_7_local_GR_Newton_PPN_claim", gate="local GR/Newton/PPN claim allowed", gate_pass=False, rationale="fixed EH and beta owner routes remain nonclaim"),
    ]


def decision_rows() -> list[dict[str, object]]:
    return [
        row(decision_id="DEC2136_0", decision="FIXED_EH_COEFFICIENT_NOT_PARENT_SIGNED", because="terminal kappa_0 is the right theorem, but source normalization and no-marker/frame descent remain unsigned", next_action="do not use constant units as GR derivation"),
        row(decision_id="DEC2136_1", decision="ACURV_NAME_COLLISION_QUARANTINED", because="pre-pivot A_curv is an empirical/motion-load amplitude, not the parent auxiliary field unless a parent action bridge is found", next_action="keep A_curv_aux_2135 as proxy only"),
        row(decision_id="DEC2136_2", decision="BEST_NEXT_IS_PARENT_ACTION_COEFF_INVENTORY", because="we need an exhaustive coefficient-of-R inventory before choosing the actual beta owner or proving kappa terminal", next_action="scan parent/action/core documents and variable ledgers for kappa/G_ref/Gamma/chi/Lambda/marker/coframe candidates"),
    ]


def next_target_rows() -> list[dict[str, object]]:
    return [
        row(
            route_id="NEXT2136_0_2137",
            next_target="2137-Y5-R2FR-parent-action-coefficient-inventory-or-first-Acurv-owner-lock.md",
            script="scripts/Y5_R2FR_parent_action_coefficient_inventory_or_first_Acurv_owner_lock_2137.py",
            objective="Build an exhaustive parent-action coefficient-of-R inventory: kappa/G_ref/Gamma/chi/Lambda/marker/coframe/measure/coupling candidates, classify each as terminal constant, quotient-owned geometry, hidden invariant, source/readout normalization, or missing; then either prove kappa terminal or select the first actual A_curv_aux parent owner.",
            forbidden_shortcuts="treating unit choice as proof; equating empirical A_curv with A_curv_aux; ignoring source denominator; cancellation between unknown coefficient routes; local-GR/PPN/R10 claim; formalization-workbench edits; GitHub action",
        )
    ]


def write_branch_copies(
    fixed_eh: list[dict[str, object]],
    maps: list[dict[str, object]],
    beta_rows: list[dict[str, object]],
    gates: list[dict[str, object]],
    next_rows: list[dict[str, object]],
) -> list[dict[str, object]]:
    copies = [
        ("COPY2136_0_source_weight_docs", SOURCE_WEIGHT_DOCS / "AFRAME_FIXED_EH_COEFFICIENT_2136_NONCLAIM.csv", fixed_eh + maps + gates),
        ("COPY2136_1_branch_locked_wep", BRANCH_WEP / "P8_Y5_PARENT_QLOC_2136_ACURV_OWNER_UPDATE_NONCLAIM.csv", beta_rows),
        ("COPY2136_2_acquisition_queue", QUEUE / "JR2136_PARENT_ACTION_COEFF_INVENTORY_QUEUE.csv", next_rows + beta_rows),
    ]
    results: list[dict[str, object]] = []
    for copy_id, destination, rows_to_write in copies:
        write_csv(destination, rows_to_write)
        results.append(row(copy_id=copy_id, destination=str(destination), path_exists=destination.exists(), row_count=len(rows_to_write), parse_ok=csv_rows_parse(destination)))
    return results


def validation_rows(
    sources: list[dict[str, object]],
    fixed_eh: list[dict[str, object]],
    maps: list[dict[str, object]],
    beta_rows: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    copies: list[dict[str, object]],
    csv_paths: list[Path],
) -> list[dict[str, object]]:
    sources_ok = all(truthy(item["path_exists"]) and truthy(item["needles_found"]) for item in sources)
    fixed_ok = any(item["theorem_id"] == "FEH2136_5_verdict" and item["proof_status"] == "FIXED_EH_COEFFICIENT_NOT_PARENT_SIGNED" for item in fixed_eh)
    map_ok = any(item["map_id"] == "MAP2136_6_verdict" and item["map_status"] == "NOT_IDENTIFIED" for item in maps)
    guard_ok = any(item["map_id"] == "MAP2136_1_name_collision_A_curv" and item["map_status"] == "NAME_COLLISION_GUARDED" for item in maps)
    beta_ok = any(item["field_id"] == "BETA2136_2_beta" and item["value"] == "MISSING_BETA_A" for item in beta_rows) and any(item["field_id"] == "BETA2136_6_name_guard" and item["value"] == "ACTIVE" for item in beta_rows)
    gates_ok = any(item["gate_id"] == "GATE2136_2_fixed_EH_parent_signed" and not truthy(item["gate_pass"]) for item in gates) and any(item["gate_id"] == "GATE2136_5_Acurv_name_guard" and truthy(item["gate_pass"]) for item in gates)
    decisions_ok = any(item["decision_id"] == "DEC2136_2" and "PARENT_ACTION_COEFF_INVENTORY" in str(item["decision"]) for item in decisions)
    next_ok = any(item["route_id"] == "NEXT2136_0_2137" for item in next_rows)
    branch_ok = all(truthy(item["path_exists"]) and truthy(item["parse_ok"]) for item in copies)
    csv_ok = all(path.exists() and csv_rows_parse(path) for path in csv_paths)
    no_claim_flags = all(
        not truthy(item.get("claim_allowed", False)) and not truthy(item.get("valid_for_claim", False))
        for group in (sources, fixed_eh, maps, beta_rows, gates, decisions, next_rows, copies)
        for item in group
    )
    formalization_clean = count_formalization_modified() == 0 and not formalization_has_2136_artifacts()
    pycache_clean = not (Path(__file__).resolve().parent / "__pycache__").exists()
    all_ok = all([sources_ok, fixed_ok, map_ok, guard_ok, beta_ok, gates_ok, decisions_ok, next_ok, branch_ok, csv_ok, no_claim_flags, formalization_clean, pycache_clean])
    checks = [
        ("VAL2136_00_sources", sources_ok, "all cited 2135/1017/1018/1027/1028/A_curv sources exist and contain expected needles"),
        ("VAL2136_01_fixed_EH", fixed_ok, "fixed EH coefficient theorem remains conditional and not parent-signed"),
        ("VAL2136_02_Acurv_map", map_ok, "actual A_curv parent variable is not identified"),
        ("VAL2136_03_name_guard", guard_ok, "empirical A_curv name collision is guarded"),
        ("VAL2136_04_beta_rows", beta_ok, "beta owner update retains missing beta_A and active name guard"),
        ("VAL2136_05_gates", gates_ok, "fixed-EH gate fails while name guard gate passes"),
        ("VAL2136_06_decisions", decisions_ok, "decision ledger selects parent action coefficient inventory next"),
        ("VAL2136_07_next", next_ok, "next target is 2137"),
        ("VAL2136_08_branch_copies", branch_ok, "branch copies exist and parse"),
        ("VAL2136_09_csv_parse", csv_ok, "all generated CSVs parse cleanly"),
        ("VAL2136_10_no_claim_flags", no_claim_flags, "no generated row allows a claim"),
        ("VAL2136_11_formalization_clean", formalization_clean, "formalization-workbench untouched by 2136"),
        ("VAL2136_12_no_pycache", pycache_clean, "scripts __pycache__ removed"),
        ("VAL2136_OVERALL", all_ok, "2136 rejects fixed-EH promotion under current evidence, quarantines empirical A_curv from A_curv_aux, and selects a parent action coefficient inventory next."),
    ]
    return [row(check_id=check_id, status="PASS" if passed else "FAIL", detail=detail) for check_id, passed, detail in checks]


def write_doc(
    sources: list[dict[str, object]],
    fixed_eh: list[dict[str, object]],
    maps: list[dict[str, object]],
    beta_rows: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    copies: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    content = "\n\n".join(
        [
            "# 2136 - Y5/R2FR Fixed EH Coefficient Naturality Or Acurv Parent Variable Map",
            "## Current Verdict",
            "2136 tested the cleanest possible GR-reduction shortcut: make the observed Einstein-Hilbert coefficient a terminal parent constant. As a conditional theorem this is strong: if `kappa_0` is truly terminal, hidden scalars cannot enter `Coeff(R[g_obs])`, and the `beta_A A R` route dies.",
            "But the current corpus does not parent-sign that theorem. Setting `G=1` or writing a constant `kappa_0` is a unit convention, not a proof that measured Newton coupling is fixed. The same-frame source denominator `M_H_ref`, `G_ref` bridge, no-marker constants, and common frame/readout routes remain unsigned, so fixed EH cannot yet be promoted to derived local GR/Newton.",
            "2136 also protects against a dangerous name collision. The existing `A_curv` in the motion-load/pre-pivot route is an empirical/route amplitude, not automatically the parent auxiliary `A_curv_aux_2135`. Until a parent action term and `beta_A`, `M_A^2`, normalization, and readout map are found, `A_curv_aux_2135` remains a nonclaim proxy.",
            "## Source Register",
            md_table(sources, ["source_id", "source_path", "path_exists", "needles_found", "role", "valid_for_claim"]),
            "## Fixed EH Coefficient Attempt",
            md_table(fixed_eh, ["theorem_id", "claim_piece", "mathematical_form", "proof_status", "derivation_result", "blocker", "valid_for_claim"]),
            "## Acurv Parent Variable Map",
            md_table(maps, ["map_id", "candidate", "source_path", "interpretation", "map_status", "reason", "valid_for_claim"]),
            "## Beta Owner Update",
            md_table(beta_rows, ["field_id", "field", "value", "required_for_claim", "current_status", "valid_for_claim"]),
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
    fixed_eh = fixed_eh_rows()
    maps = acurv_map_rows()
    beta_rows = beta_owner_update_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_rows = next_target_rows()

    paths = {
        "sources": OUT / "P8_Y5_PARENT_QLOC_2136_SOURCE_REGISTER.csv",
        "fixed_eh": OUT / "P8_Y5_PARENT_QLOC_2136_FIXED_EH_COEFFICIENT_ATTEMPT.csv",
        "maps": OUT / "P8_Y5_PARENT_QLOC_2136_ACURV_PARENT_VARIABLE_MAP.csv",
        "beta": OUT / "P8_Y5_PARENT_QLOC_2136_BETA_OWNER_UPDATE.csv",
        "gates": OUT / "P8_Y5_PARENT_QLOC_2136_CLAIM_GATES.csv",
        "decisions": OUT / "P8_Y5_PARENT_QLOC_2136_DECISION_LEDGER.csv",
        "next": OUT / "P8_Y5_PARENT_QLOC_2136_NEXT_TARGET.csv",
        "branch": OUT / "P8_Y5_PARENT_QLOC_2136_BRANCH_COPIES.csv",
        "validation": OUT / "P8_Y5_BRR545_2136_VALIDATION.csv",
    }
    write_csv(paths["sources"], sources)
    write_csv(paths["fixed_eh"], fixed_eh)
    write_csv(paths["maps"], maps)
    write_csv(paths["beta"], beta_rows)
    write_csv(paths["gates"], gates)
    write_csv(paths["decisions"], decisions)
    write_csv(paths["next"], next_rows)

    copies = write_branch_copies(fixed_eh, maps, beta_rows, gates, next_rows)
    write_csv(paths["branch"], copies)

    remove_pycache()
    csv_paths = [path for key, path in paths.items() if key != "validation"] + [Path(str(copy["destination"])) for copy in copies]
    validation = validation_rows(sources, fixed_eh, maps, beta_rows, gates, decisions, next_rows, copies, csv_paths)
    write_csv(paths["validation"], validation)
    write_doc(sources, fixed_eh, maps, beta_rows, gates, decisions, next_rows, copies, validation)

    print(f"wrote {DOC}")
    print(f"validation {paths['validation']}")


if __name__ == "__main__":
    main()
