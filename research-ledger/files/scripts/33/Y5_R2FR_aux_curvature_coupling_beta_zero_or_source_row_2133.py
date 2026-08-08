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


DOC = ROOT / "2133-Y5-R2FR-aux-curvature-coupling-beta-zero-or-source-row.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"

CSV_2132_NEXT = OUT / "P8_Y5_PARENT_QLOC_2132_NEXT_TARGET.csv"
CSV_2132_VAL = OUT / "P8_Y5_BRR545_2132_VALIDATION.csv"
CSV_2132_AUX = OUT / "P8_Y5_PARENT_QLOC_2132_AUX_SCALAR_COEFFICIENT_ROW.csv"
CSV_2132_TOWER = OUT / "P8_Y5_PARENT_QLOC_2132_NO_TOWER_THEOREM_ATTEMPT.csv"
CSV_1049_RULE = OUT / "P8_Y5_R10_1049_OPERATOR_CLASSIFICATION_RULE_ATTEMPT.csv"
CSV_1049_SYM = OUT / "P8_Y5_R10_1049_SYMMETRY_BAN_THEOREM_ATTEMPT.csv"
CSV_1049_GATES = OUT / "P8_Y5_R10_1049_CLAIM_GATES.csv"
CSV_1049_DEC = OUT / "P8_Y5_R10_1049_DECISION_LEDGER.csv"
CSV_1888_READOUT = OUT / "P8_Y5_PARENT_QLOC_1888_READOUT_STABILITY_PROOF_ATTEMPT.csv"
CSV_1888_DEC = OUT / "P8_Y5_PARENT_QLOC_1888_DECISION_LEDGER.csv"
CSV_1265_AP = OUT / "P8_Y5_R10_1265_AUXILIARY_PROTECTION_AUDIT.csv"
CSV_1266_HUNT = OUT / "P8_Y5_R10_1266_PRIMITIVE_SOURCE_HUNT_LEDGER.csv"
DOC_06_SOURCE = ROOT / "06-reciprocal-charge-source-neutrality.md"
DOC_964 = ROOT / "964-Y5-R10-parent-no-higher-derivative-minimality-theorem-or-R2FR-nonclaim-runner.md"
DOC_965 = ROOT / "965-Y5-R10-primitive-quotient-no-natural-marker-theorem-or-R2FR-full-curve-intake.md"


def row(**kwargs: object) -> dict[str, object]:
    data = base_row()
    data["claim_allowed"] = False
    data.update(kwargs)
    return data


def truthy(value: object) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"true", "1", "yes", "pass", "valid"}


def formalization_has_2133_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    patterns = (
        "*2133-Y5-R2FR*",
        "*P8_Y5_PARENT_QLOC_2133*",
        "*Y5_R2FR_aux_curvature_coupling_beta_zero_or_source_row_2133*",
        "*AFRAME_BETA_ZERO_2133*",
        "*JR2133*",
    )
    try:
        return any(path.is_file() for pattern in patterns for path in FORMALIZATION.rglob(pattern))
    except Exception:
        return False


def source_register_rows() -> list[dict[str, object]]:
    specs = [
        ("SRC2133_00_2132_next", CSV_2132_NEXT, ["NEXT2132_0_2133", "beta_A=0"], "2132 handoff selects beta_A zero or source row."),
        ("SRC2133_01_2132_validation", CSV_2132_VAL, ["VAL2132_OVERALL", "PASS"], "2132 validation passed."),
        ("SRC2133_02_2132_aux", CSV_2132_AUX, ["AUX2132_0_beta", "MISSING_BETA_A"], "beta_A row blocks c_R2_aux."),
        ("SRC2133_03_2132_tower", CSV_2132_TOWER, ["NT2132_1_no_R_coupling", "UNSIGNED"], "no curvature coupling theorem is unsigned."),
        ("SRC2133_04_1049_rule", CSV_1049_RULE, ["OCR1049_2_product_sequestration", "POWERFUL_BUT_PARENT_AXIOM_IF_UNSIGNED"], "product/sequester is the strongest visible-hidden zero route."),
        ("SRC2133_05_1049_symmetry", CSV_1049_SYM, ["SBT1049_3_parity_evenness", "INSUFFICIENT"], "parity alone is insufficient."),
        ("SRC2133_06_1049_gates", CSV_1049_GATES, ["CG1049_0_operator_ban", "false"], "operator ban not parent-signed."),
        ("SRC2133_07_1049_decision", CSV_1049_DEC, ["DEC1049_1_best_theorem_route", "product/sequester"], "1049 selects product functor derivation."),
        ("SRC2133_08_1888_readout", CSV_1888_READOUT, ["ROS1888_6_verdict", "READOUT_STABILITY_NOT_PARENT_DERIVED"], "readout-after-variation remains conditional."),
        ("SRC2133_09_1888_decision", CSV_1888_DEC, ["DEC1888_1_readout_route", "RETAIN_READOUT_STABILITY_AS_REQUIRED_CLAUSE"], "readout route cannot alone protect zero."),
        ("SRC2133_10_1265_aux", CSV_1265_AP, ["AP1265_0_auxiliary_signature", "CANDIDATE_NOT_PARENT_SIGNED"], "auxiliary grammar conditional only."),
        ("SRC2133_11_1266_hunt", CSV_1266_HUNT, ["HUNT1266_3_nonpropagating_constraint", "BEST_CLOSURE_SUPPORT_NOT_PARENT_SIGNED"], "nonpropagating constraint is support, not parent proof."),
        ("SRC2133_12_source_neutrality", DOC_06_SOURCE, ["source reciprocal neutrality", "not yet parent-derived"], "source neutrality is conditional, not parent-derived."),
        ("SRC2133_13_964_doc", DOC_964, ["CM964_1_auxiliary_scalar_integrated_out", "beta phi R"], "auxiliary scalar beta phi R countermodel remains legal."),
        ("SRC2133_14_965_doc", DOC_965, ["MC965_6_universal_auxiliary", "safe_case_not_derived"], "universal auxiliary safe case is not derived."),
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


def beta_zero_attempt_rows() -> list[dict[str, object]]:
    return [
        row(
            attempt_id="BZ2133_0_parent_operator_class",
            route="declared parent operator class forbids A R",
            zero_condition="Op_allowed excludes hidden auxiliary A multiplying the observed Ricci scalar unless A descends through q or is a fixed universal constant",
            status="CONTRACT_NOT_PARENT_DERIVED",
            blocker="OCR1049_0/OCR1049_2 are exact contracts but not signed parent theorems",
            consequence="beta_A cannot be set to zero from operator-class language alone",
        ),
        row(
            attempt_id="BZ2133_1_product_sequester",
            route="visible-hidden product functor/sequester",
            zero_condition="S_parent = S_geom[q] + S_hidden[A] + S_vis[q,Psi,theta] with no A*R[g_obs] or A*O_vis morphism",
            status="BEST_ZERO_ROUTE_UNSIGNED",
            blocker="product/sequester would kill beta_A, but 1049 marks it a parent axiom if unsigned",
            consequence="next derivation should try to sign this route rather than rely on parity",
        ),
        row(
            attempt_id="BZ2133_2_shift_symmetry",
            route="exact vertical shift symmetry",
            zero_condition="A -> A + const forbids non-derivative beta_A A R if R is neutral and symmetry is exact in the compact branch",
            status="WOULD_FORBID_IF_EXACT_BUT_UNSIGNED",
            blocker="hidden-sector profiles, potentials, mass terms and projectors are not proven shift-invariant",
            consequence="shift symmetry is a possible kill route but not current evidence",
        ),
        row(
            attempt_id="BZ2133_3_parity",
            route="A -> -A parity",
            zero_condition="odd linear beta_A A R is forbidden if A is parity-odd and the parent action respects the parity",
            status="INSUFFICIENT_BY_ITSELF",
            blocker="parity can kill linear beta_A but leaves A^2 R, A^2 R^2, loops, marker prefactors and readout/EFT re-entry unless A=0 or sequestered",
            consequence="parity can be recorded as partial support, not beta-zero proof",
        ),
        row(
            attempt_id="BZ2133_4_source_neutrality",
            route="source neutrality/no scalar hair",
            zero_condition="A is a nonpropagating constraint/source-neutral mode and carries no curvature or matter source charge",
            status="CONDITIONAL_ONLY",
            blocker="source neutrality and nonpropagating constraint support are not parent-derived",
            consequence="helps motivation, but cannot set beta_A=0",
        ),
        row(
            attempt_id="BZ2133_5_readout_after_variation",
            route="readout-after-variation/no re-entry",
            zero_condition="readout map is outside S_parent and cannot regenerate A R or A-dependent coefficient functions in S_eff",
            status="CONDITIONAL_SCHEMA_NOT_PARENT_SIGNED",
            blocker="radiative/readout closure and no-hidden-visible morphism remain unsigned",
            consequence="readout order is required but cannot alone kill a parent beta_A term",
        ),
        row(
            attempt_id="BZ2133_6_verdict",
            route="prove beta_A=0 now",
            zero_condition="one signed kill route covers every eliminated auxiliary/scalar/memory sector and survives readout/effective reduction",
            status="BETA_ZERO_NOT_DERIVED",
            blocker="product/sequester, exact shift, source neutrality and readout stability are all unsigned or insufficient",
            consequence="stage beta_A source row as nonclaim",
        ),
    ]


def beta_source_row() -> list[dict[str, object]]:
    return [
        row(field_id="BETA2133_0_sector_owner", field="auxiliary_sector_id", value_required="name of eliminated scalar/auxiliary/memory sector A", current_value="MISSING_SECTOR_OWNER", units="identifier", status="BLOCKS_ROW"),
        row(field_id="BETA2133_1_beta_value", field="beta_A", value_required="numeric value, symbolic expression, or theorem-zero certificate", current_value="MISSING_BETA_A", units="units such that beta_A A R matches Lagrangian density normalization", status="BLOCKS_C_R2_AUX"),
        row(field_id="BETA2133_2_beta_sign", field="beta_A_sign", value_required="sign convention and whether beta_A can be positive/negative or exactly zero", current_value="MISSING_SIGN", units="sign", status="BLOCKS_STABILITY_AND_SCALARON_MAP"),
        row(field_id="BETA2133_3_A_normalization", field="A_field_normalization", value_required="normalization/dimension of A and EH-normalized action convention", current_value="MISSING_A_NORMALIZATION", units="field_units", status="BLOCKS_UNIT_CONVERSION"),
        row(field_id="BETA2133_4_mass_link", field="M_A2_link", value_required="link to M_A^2 source row or pure-constraint theorem", current_value="MISSING_M_A2_LINK", units="mass_squared_or_inverse_length_squared", status="BLOCKS_C_R2_AUX"),
        row(field_id="BETA2133_5_cR2_interface", field="c_R2_aux_interface", value_required="c_R2_aux = beta_A^2/(2 M_A^2) after normalization conversion, with no-cancellation guard", current_value="MISSING_BETA_AND_MASS", units="length_squared_after_EH_normalization", status="NOT_EXECUTABLE"),
        row(field_id="BETA2133_6_source_readout", field="source_readout_coupling", value_required="theorem-zero or map to source/clock/PPN/R10 residuals", current_value="MISSING_SOURCE_READOUT_MAP", units="arena_specific", status="BLOCKS_SCORE"),
        row(field_id="BETA2133_7_valid_for_claim", field="valid_for_claim", value_required="true only after all fields are sourced and beta is not back-solved from bounds", current_value=False, units="boolean", status="FORCED_FALSE"),
    ]


def claim_gate_rows() -> list[dict[str, object]]:
    return [
        row(gate_id="GATE2133_0_sources", gate="source evidence loaded", gate_pass=True, rationale="2132/1049/1888/1265/1266/source-neutrality sources are needle-checked"),
        row(gate_id="GATE2133_1_beta_zero", gate="beta_A theorem-zero derived", gate_pass=False, rationale="all beta-zero routes are unsigned, conditional or insufficient"),
        row(gate_id="GATE2133_2_product_route_identified", gate="best beta-zero route identified", gate_pass=True, rationale="visible-hidden product/sequester is the cleanest route if parent-signed"),
        row(gate_id="GATE2133_3_beta_source_row", gate="beta_A source row staged", gate_pass=True, rationale="sector owner, beta value, sign, normalization, M_A^2 link and readout map are explicit missing fields"),
        row(gate_id="GATE2133_4_beta_row_executable", gate="beta_A source row executable", gate_pass=False, rationale="beta_A, sign, A normalization, M_A^2 link and source paths are missing"),
        row(gate_id="GATE2133_5_cR2_aux_score", gate="c_R2_aux score ready", gate_pass=False, rationale="requires beta_A and M_A^2 plus scalaron/readout/bound interface"),
        row(gate_id="GATE2133_6_local_GR_Newton_PPN_claim", gate="local GR/Newton/PPN claim allowed", gate_pass=False, rationale="operator, source normalization, PPN and empirical gates remain open"),
    ]


def decision_rows() -> list[dict[str, object]]:
    return [
        row(decision_id="DEC2133_0", decision="BETA_ZERO_NOT_DERIVED", because="covariance/parity/source-neutrality/readout-order do not currently force beta_A=0", next_action="do not claim R2/fR zero"),
        row(decision_id="DEC2133_1", decision="PRODUCT_SEQUESTER_IS_BEST_ROUTE", because="it would forbid hidden auxiliaries from multiplying visible geometry/readout operators", next_action="try to parent-sign visible-hidden product functor for curvature channel"),
        row(decision_id="DEC2133_2", decision="BETA_SOURCE_ROW_REQUIRED_IF_ROUTE_FAILS", because="without beta_A the auxiliary scalar branch cannot be scored or killed", next_action="either derive sequester or fill beta_A source row with units/sign/owner"),
    ]


def next_target_rows() -> list[dict[str, object]]:
    return [
        row(
            route_id="NEXT2133_0_2134",
            next_target="2134-Y5-R2FR-visible-hidden-curvature-sequester-or-beta-source-pack.md",
            script="scripts/Y5_R2FR_visible_hidden_curvature_sequester_or_beta_source_pack_2134.py",
            objective="Try to parent-sign a visible-hidden product/sequester theorem for the curvature channel: no hidden auxiliary/scalar/memory field can multiply R[g_obs] or any visible operator except through q-owned geometry; if not, build the beta_A source pack for the first retained auxiliary sector.",
            forbidden_shortcuts="using parity alone as beta-zero; using readout-after-variation to erase a parent beta term; assuming source neutrality; inventing beta_A; formalization-workbench edits; GitHub action",
        )
    ]


def write_branch_copies(
    attempts: list[dict[str, object]],
    beta_rows: list[dict[str, object]],
    gates: list[dict[str, object]],
    next_rows: list[dict[str, object]],
) -> list[dict[str, object]]:
    copies = [
        ("COPY2133_0_source_weight_docs", SOURCE_WEIGHT_DOCS / "AFRAME_BETA_ZERO_2133_NONCLAIM.csv", attempts + gates),
        ("COPY2133_1_branch_locked_wep", BRANCH_WEP / "P8_Y5_PARENT_QLOC_2133_BETA_SOURCE_ROW_NONCLAIM.csv", beta_rows),
        ("COPY2133_2_acquisition_queue", QUEUE / "JR2133_CURVATURE_SEQUESTER_OR_BETA_SOURCE_QUEUE.csv", next_rows + beta_rows),
    ]
    results: list[dict[str, object]] = []
    for copy_id, destination, rows_to_write in copies:
        write_csv(destination, rows_to_write)
        results.append(row(copy_id=copy_id, destination=str(destination), path_exists=destination.exists(), row_count=len(rows_to_write), parse_ok=csv_rows_parse(destination)))
    return results


def validation_rows(
    sources: list[dict[str, object]],
    attempts: list[dict[str, object]],
    beta_rows: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    copies: list[dict[str, object]],
    csv_paths: list[Path],
) -> list[dict[str, object]]:
    sources_ok = all(truthy(item["path_exists"]) and truthy(item["needles_found"]) for item in sources)
    attempts_ok = any(item["attempt_id"] == "BZ2133_6_verdict" and item["status"] == "BETA_ZERO_NOT_DERIVED" for item in attempts)
    product_ok = any(item["attempt_id"] == "BZ2133_1_product_sequester" and item["status"] == "BEST_ZERO_ROUTE_UNSIGNED" for item in attempts)
    beta_ok = any(item["field_id"] == "BETA2133_1_beta_value" and item["current_value"] == "MISSING_BETA_A" for item in beta_rows) and any(item["field_id"] == "BETA2133_7_valid_for_claim" and item["current_value"] is False for item in beta_rows)
    gates_ok = any(item["gate_id"] == "GATE2133_2_product_route_identified" and truthy(item["gate_pass"]) for item in gates) and any(item["gate_id"] == "GATE2133_6_local_GR_Newton_PPN_claim" and not truthy(item["gate_pass"]) for item in gates)
    decisions_ok = any(item["decision_id"] == "DEC2133_1" and "PRODUCT_SEQUESTER" in str(item["decision"]) for item in decisions)
    next_ok = any(item["route_id"] == "NEXT2133_0_2134" for item in next_rows)
    branch_ok = all(truthy(item["path_exists"]) and truthy(item["parse_ok"]) for item in copies)
    csv_ok = all(path.exists() and csv_rows_parse(path) for path in csv_paths)
    no_claim_flags = all(
        not truthy(item.get("claim_allowed", False)) and not truthy(item.get("valid_for_claim", False))
        for group in (sources, attempts, beta_rows, gates, decisions, next_rows, copies)
        for item in group
    )
    formalization_clean = count_formalization_modified() == 0 and not formalization_has_2133_artifacts()
    pycache_clean = not (Path(__file__).resolve().parent / "__pycache__").exists()
    all_ok = all([sources_ok, attempts_ok, product_ok, beta_ok, gates_ok, decisions_ok, next_ok, branch_ok, csv_ok, no_claim_flags, formalization_clean, pycache_clean])
    checks = [
        ("VAL2133_00_sources", sources_ok, "all cited beta-zero sources exist and contain expected needles"),
        ("VAL2133_01_attempts", attempts_ok, "beta-zero verdict is explicitly not derived"),
        ("VAL2133_02_product_route", product_ok, "product/sequester route is identified as strongest but unsigned"),
        ("VAL2133_03_beta_row", beta_ok, "beta source row is staged but valid_for_claim false"),
        ("VAL2133_04_gates", gates_ok, "product route gate passes while local-GR claim gate fails"),
        ("VAL2133_05_decisions", decisions_ok, "decision ledger selects curvature sequester next"),
        ("VAL2133_06_next", next_ok, "next target is 2134 curvature sequester or beta source pack"),
        ("VAL2133_07_branch_copies", branch_ok, "branch copies exist and parse"),
        ("VAL2133_08_csv_parse", csv_ok, "all generated CSVs parse cleanly"),
        ("VAL2133_09_no_claim_flags", no_claim_flags, "no generated row allows a claim"),
        ("VAL2133_10_formalization_clean", formalization_clean, "formalization-workbench untouched by 2133"),
        ("VAL2133_11_no_pycache", pycache_clean, "scripts __pycache__ removed"),
        ("VAL2133_OVERALL", all_ok, "2133 rejects beta_A zero under current evidence, identifies product/sequester as the best route, and stages a nonclaim beta source row."),
    ]
    return [row(check_id=check_id, status="PASS" if passed else "FAIL", detail=detail) for check_id, passed, detail in checks]


def write_doc(
    sources: list[dict[str, object]],
    attempts: list[dict[str, object]],
    beta_rows: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    copies: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    content = "\n\n".join(
        [
            "# 2133 - Y5/R2FR Aux Curvature Coupling Beta Zero Or Source Row",
            "## Current Verdict",
            "2133 asks whether the hidden auxiliary curvature coupling `beta_A A R` is forced to vanish. Current answer: not yet. Diffeomorphism covariance does not forbid it, parity only kills odd linear terms and not the whole even/radiative tower, source neutrality is conditional, and readout-after-variation cannot erase a parent beta term.",
            "The best zero route is now clean: parent-sign visible-hidden product/sequester for the curvature channel. If hidden auxiliaries cannot multiply `R[g_obs]` or visible operators except through q-owned geometry, then `beta_A=0`. Until that theorem is signed, `beta_A` is a retained nonclaim coefficient row with owner, units, sign, normalization, `M_A^2` link, and source/readout map missing.",
            "## Source Register",
            md_table(sources, ["source_id", "source_path", "path_exists", "needles_found", "role", "valid_for_claim"]),
            "## Beta-Zero Attempt Ledger",
            md_table(attempts, ["attempt_id", "route", "zero_condition", "status", "blocker", "consequence", "valid_for_claim"]),
            "## Beta Source Row",
            md_table(beta_rows, ["field_id", "field", "value_required", "current_value", "units", "status", "valid_for_claim"]),
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
    attempts = beta_zero_attempt_rows()
    beta_rows = beta_source_row()
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_rows = next_target_rows()

    paths = {
        "sources": OUT / "P8_Y5_PARENT_QLOC_2133_SOURCE_REGISTER.csv",
        "attempts": OUT / "P8_Y5_PARENT_QLOC_2133_BETA_ZERO_ATTEMPT.csv",
        "beta": OUT / "P8_Y5_PARENT_QLOC_2133_BETA_SOURCE_ROW.csv",
        "gates": OUT / "P8_Y5_PARENT_QLOC_2133_CLAIM_GATES.csv",
        "decisions": OUT / "P8_Y5_PARENT_QLOC_2133_DECISION_LEDGER.csv",
        "next": OUT / "P8_Y5_PARENT_QLOC_2133_NEXT_TARGET.csv",
        "branch": OUT / "P8_Y5_PARENT_QLOC_2133_BRANCH_COPIES.csv",
        "validation": OUT / "P8_Y5_BRR545_2133_VALIDATION.csv",
    }
    write_csv(paths["sources"], sources)
    write_csv(paths["attempts"], attempts)
    write_csv(paths["beta"], beta_rows)
    write_csv(paths["gates"], gates)
    write_csv(paths["decisions"], decisions)
    write_csv(paths["next"], next_rows)

    copies = write_branch_copies(attempts, beta_rows, gates, next_rows)
    write_csv(paths["branch"], copies)

    remove_pycache()
    csv_paths = [path for key, path in paths.items() if key != "validation"] + [Path(str(copy["destination"])) for copy in copies]
    validation = validation_rows(sources, attempts, beta_rows, gates, decisions, next_rows, copies, csv_paths)
    write_csv(paths["validation"], validation)
    write_doc(sources, attempts, beta_rows, gates, decisions, next_rows, copies, validation)

    print(f"wrote {DOC}")
    print(f"validation {paths['validation']}")


if __name__ == "__main__":
    main()
