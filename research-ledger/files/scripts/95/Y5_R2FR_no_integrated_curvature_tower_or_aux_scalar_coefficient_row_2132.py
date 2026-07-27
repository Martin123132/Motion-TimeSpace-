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


DOC = ROOT / "2132-Y5-R2FR-no-integrated-curvature-tower-or-aux-scalar-coefficient-row.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"

CSV_2131_NEXT = OUT / "P8_Y5_PARENT_QLOC_2131_NEXT_TARGET.csv"
CSV_2131_VAL = OUT / "P8_Y5_BRR545_2131_VALIDATION.csv"
CSV_2131_OWNER = OUT / "P8_Y5_PARENT_QLOC_2131_CR2_OWNER_DECOMPOSITION.csv"
CSV_2131_ZERO = OUT / "P8_Y5_PARENT_QLOC_2131_ZERO_CERTIFICATE_AUDIT.csv"
CSV_1265_AP = OUT / "P8_Y5_R10_1265_AUXILIARY_PROTECTION_AUDIT.csv"
CSV_1265_THEOREM = OUT / "P8_Y5_R10_1265_AUXILIARY_ELIMINATION_THEOREM.csv"
CSV_1266_DECISION = OUT / "P8_Y5_R10_1266_DECISION_LEDGER.csv"
CSV_1965_MAP = OUT / "P8_Y5_PARENT_QLOC_1965_R2FR_SCALARON_MAP.csv"
CSV_1965_SCHEMA = OUT / "P8_Y5_PARENT_QLOC_1965_R2FR_EXECUTABLE_BOUND_SCHEMA.csv"
DOC_963 = ROOT / "963-Y5-R10-parent-second-order-signature-or-R2FR-bound-runner.md"
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


def formalization_has_2132_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    patterns = (
        "*2132-Y5-R2FR*",
        "*P8_Y5_PARENT_QLOC_2132*",
        "*Y5_R2FR_no_integrated_curvature_tower_or_aux_scalar_coefficient_row_2132*",
        "*AFRAME_NO_CURVATURE_TOWER_2132*",
        "*JR2132*",
    )
    try:
        return any(path.is_file() for pattern in patterns for path in FORMALIZATION.rglob(pattern))
    except Exception:
        return False


def source_register_rows() -> list[dict[str, object]]:
    specs = [
        ("SRC2132_00_2131_next", CSV_2131_NEXT, ["NEXT2131_0_2132", "no-integrated-curvature-tower"], "2131 handoff selects no integrated curvature tower or auxiliary scalar coefficient row."),
        ("SRC2132_01_2131_validation", CSV_2131_VAL, ["VAL2131_OVERALL", "PASS"], "2131 validation passed."),
        ("SRC2132_02_2131_owner", CSV_2131_OWNER, ["OWN2131_2_integrated_out_aux_scalar", "COUNTERMODEL_LIVE_NOT_SOURCED"], "hidden scalar owner route remains live."),
        ("SRC2132_03_2131_zero", CSV_2131_ZERO, ["ZC2131_1_no_integrated_out_scalar", "UNSIGNED_CENTRAL_BLOCKER"], "no-integrated-out-scalar zero clause is the central blocker."),
        ("SRC2132_04_1265_ap", CSV_1265_AP, ["AP1265_0_auxiliary_signature", "AP1265_4_readout_stability"], "auxiliary protection clauses from the R_AB branch."),
        ("SRC2132_05_1265_theorem", CSV_1265_THEOREM, ["AET1265_0_auxiliary_elimination", "EXACT_CONDITIONAL_NOT_PARENT_SIGNED"], "conditional auxiliary elimination theorem."),
        ("SRC2132_06_1266_decision", CSV_1266_DECISION, ["DEC1266_0_source_hunt_result", "PARENT_SOURCE_NOT_FOUND"], "source hunt did not sign auxiliary grammar."),
        ("SRC2132_07_1965_map", CSV_1965_MAP, ["SM1965_1_scalar_mass", "SM1965_2_yukawa_alpha"], "scalaron formulas for finite branch."),
        ("SRC2132_08_1965_schema", CSV_1965_SCHEMA, ["EXR1965_1_mts_prediction", "MISSING_PARENT_NUMERIC_COEFFICIENT"], "strict executable schema demands parent coefficient."),
        ("SRC2132_09_963_doc", DOC_963, ["no-integrated-out-curvature-tower", "MISSING_PARENT_INPUT"], "963 identifies no integrated-out tower as missing."),
        ("SRC2132_10_964_doc", DOC_964, ["CM964_1_auxiliary_scalar_integrated_out", "beta phi R"], "964 contains the explicit auxiliary scalar countermodel."),
        ("SRC2132_11_965_doc", DOC_965, ["MC965_6_universal_auxiliary", "safe_case_not_derived"], "965 leaves universal auxiliary safe case conditional, not derived."),
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


def no_tower_theorem_rows() -> list[dict[str, object]]:
    return [
        row(
            theorem_id="NT2132_0_target",
            theorem_piece="no integrated curvature tower",
            condition="no eliminated MTS scalar/auxiliary/memory variable can generate R2, f(R), nonlocal RKR, or a scalar pole after variation",
            status="TARGET_DEFINED_NOT_PROVEN",
            proof_result="would protect the second-order EH selector from hidden effective-action regeneration",
            blocker="requires parent-signed grammar for every eliminated sector",
        ),
        row(
            theorem_id="NT2132_1_no_R_coupling",
            theorem_piece="no linear curvature coupling",
            condition="for every auxiliary A, beta_A=0 in beta_A A R, or the variable is not a scalar curvature channel",
            status="UNSIGNED",
            proof_result="would remove the beta_A^2/(2M_A^2) R2 source at algebraic level",
            blocker="no corpus row proves beta_A=0 for all hidden scalar/memory auxiliaries",
        ),
        row(
            theorem_id="NT2132_2_algebraic_constraint_protection",
            theorem_piece="pure constraint rather than integrated scalar",
            condition="auxiliary appears only as a Lagrange multiplier/constraint, with no quadratic mass inverse, kinetic term, boundary charge, or source term",
            status="EXACT_CONDITIONAL_NOT_PARENT_SIGNED",
            proof_result="if AP-style clauses hold, the variable is eliminated without a scalar pole",
            blocker="1265/1266 auxiliary grammar is conditional and source hunt did not parent-sign it",
        ),
        row(
            theorem_id="NT2132_3_no_derivative_or_kernel_regeneration",
            theorem_piece="no derivative, determinant, or kernel tower",
            condition="elimination produces no det operator, no Box^-1, no local expansion coefficient, and no readout/radiative RKR term",
            status="UNSIGNED",
            proof_result="would block nonlocal/memory regeneration of c_R2_eff",
            blocker="readout/effective reduction stability remains unsigned",
        ),
        row(
            theorem_id="NT2132_4_no_source_readout_coupling",
            theorem_piece="no source/readout coupling to eliminated variable",
            condition="matter/source/clock/light/orbit readout does not couple to the eliminated scalar or its constraint multiplier",
            status="UNSIGNED",
            proof_result="would prevent a hidden scalar from reappearing as WEP, clock, PPN or R10 charge",
            blocker="source/readout transfer gates remain open in the local branch",
        ),
        row(
            theorem_id="NT2132_5_verdict",
            theorem_piece="prove no tower now",
            condition="NT2132_1 through NT2132_4 all parent-signed",
            status="NO_TOWER_THEOREM_NOT_DERIVED",
            proof_result="finite auxiliary-scalar coefficient row remains mandatory",
            blocker="beta_A=0/M_A=infinity/no-kernel/no-readout clauses are not signed",
        ),
    ]


def aux_scalar_coefficient_rows() -> list[dict[str, object]]:
    return [
        row(
            aux_id="AUX2132_0_beta",
            quantity="beta_A",
            meaning="linear curvature coupling of hidden scalar/auxiliary A to R",
            formula_or_rule="L_A contains beta_A A R in the simple algebraic branch",
            required_input="theorem beta_A=0 or sourced beta_A with units and sign",
            current_value="MISSING_BETA_A",
            status="BLOCKS_C_R2_AUX",
        ),
        row(
            aux_id="AUX2132_1_mass",
            quantity="M_A^2",
            meaning="quadratic algebraic/mass coefficient for hidden scalar/auxiliary A",
            formula_or_rule="L_A contains -1/2 M_A^2 A^2; positive M_A^2 gives non-tachyonic algebraic elimination in the toy branch",
            required_input="sourced positive M_A^2 or theorem M_A^-2=0/variable is pure constraint",
            current_value="MISSING_M_A2",
            status="BLOCKS_C_R2_AUX",
        ),
        row(
            aux_id="AUX2132_2_cR2_aux",
            quantity="c_R2_aux",
            meaning="effective R2 coefficient generated by eliminating A",
            formula_or_rule="toy normalization: c_R2_aux = beta_A^2/(2 M_A^2), then convert to the 1965 EH-normalized c_R2 convention",
            required_input="beta_A; M_A^2; normalization conversion; source path; no-cancellation guard",
            current_value="MISSING_BETA_AND_MASS",
            status="NOT_EXECUTABLE",
        ),
        row(
            aux_id="AUX2132_3_scalaron_map",
            quantity="lambda_A, alpha_A",
            meaning="finite scalar range and coupling induced by c_R2_aux if it belongs to simple metric f(R)",
            formula_or_rule="lambda=sqrt(6 c_R2_eff); alpha=1/3 only under unscreened metric f(R) universal-coupling assumptions",
            required_input="total c_R2_eff; branch context; screening/readout regime; matter coupling theorem",
            current_value="FORMULA_ONLY_PARENT_INPUTS_MISSING",
            status="CONDITIONAL_NONCLAIM",
        ),
        row(
            aux_id="AUX2132_4_source_readout",
            quantity="source/readout coupling",
            meaning="whether A couples to matter/source/clock/light/orbit channels after reduction",
            formula_or_rule="if coupling nonzero, map to R1/R2/R3/R4/R10/R11 residuals before scoring",
            required_input="sector coupling audit or theorem-zero readout/source coupling",
            current_value="MISSING_SOURCE_READOUT_MAP",
            status="BLOCKS_PPN_R10_SCORE",
        ),
        row(
            aux_id="AUX2132_5_acceptance",
            quantity="valid auxiliary scalar coefficient row",
            meaning="minimum row required before finite branch testing",
            formula_or_rule="accepted only if beta_A and M_A^2 are sourced/theorem-zero, units/sign/normalization are explicit, and scalaron/readout/bound rows are valid",
            required_input="AUX2132_0 through AUX2132_4 complete",
            current_value="CURRENTLY_FALSE",
            status="AUX_SCALAR_ROW_BLOCKED_NONCLAIM",
        ),
    ]


def claim_gate_rows() -> list[dict[str, object]]:
    return [
        row(gate_id="GATE2132_0_sources", gate="source evidence loaded", gate_pass=True, rationale="2131, 1265/1266, 963/964/965 and 1965 sources are needle-checked"),
        row(gate_id="GATE2132_1_no_tower_theorem", gate="no integrated curvature tower theorem derived", gate_pass=False, rationale="beta=0, pure-constraint, no-kernel and no-readout clauses remain unsigned"),
        row(gate_id="GATE2132_2_aux_row_written", gate="auxiliary scalar coefficient row staged", gate_pass=True, rationale="beta, M, c_R2_aux, scalaron and source/readout fields are explicit"),
        row(gate_id="GATE2132_3_aux_row_executable", gate="auxiliary scalar row executable", gate_pass=False, rationale="beta_A and M_A^2 are missing and no source path exists"),
        row(gate_id="GATE2132_4_R2FR_score_ready", gate="R2/fR finite branch score ready", gate_pass=False, rationale="parent coefficient, screening/readout and full bound curve are missing"),
        row(gate_id="GATE2132_5_EH_second_order", gate="EH second-order selector activated", gate_pass=False, rationale="hidden curvature tower has not been killed"),
        row(gate_id="GATE2132_6_local_GR_Newton_PPN_claim", gate="local GR/Newton/PPN claim allowed", gate_pass=False, rationale="operator, source normalization, PPN and empirical gates remain open"),
    ]


def decision_rows() -> list[dict[str, object]]:
    return [
        row(decision_id="DEC2132_0", decision="NO_TOWER_THEOREM_NOT_DERIVED", because="a hidden scalar with beta_A R coupling remains a legal countermodel", next_action="do not claim second-order selector"),
        row(decision_id="DEC2132_1", decision="AUX_SCALAR_ROW_STAGED", because="if the theorem fails, the first finite coefficient row must expose beta_A and M_A^2", next_action="derive beta_A=0 or source beta_A before any scalaron scoring"),
        row(decision_id="DEC2132_2", decision="NEXT_ATTACK_BETA_ZERO", because="beta_A=0 is the sharpest kill condition for the auxiliary scalar contribution", next_action="prove no curvature coupling for eliminated MTS auxiliaries or fill beta_A source row"),
    ]


def next_target_rows() -> list[dict[str, object]]:
    return [
        row(
            route_id="NEXT2132_0_2133",
            next_target="2133-Y5-R2FR-aux-curvature-coupling-beta-zero-or-source-row.md",
            script="scripts/Y5_R2FR_aux_curvature_coupling_beta_zero_or_source_row_2133.py",
            objective="Try to prove beta_A=0 for every eliminated MTS auxiliary/scalar/memory sector by parent grammar, quotient parity, source neutrality, or readout-after-variation; if not, stage the first beta_A source row with units, sign, sector owner and nonclaim c_R2_aux interface.",
            forbidden_shortcuts="assuming auxiliary means beta=0; using mass gap as beta-zero proof; inventing beta_A; claiming c_R2_aux from dimensional guesswork; formalization-workbench edits; GitHub action",
        )
    ]


def write_branch_copies(
    theorem: list[dict[str, object]],
    aux_rows: list[dict[str, object]],
    gates: list[dict[str, object]],
    next_rows: list[dict[str, object]],
) -> list[dict[str, object]]:
    copies = [
        ("COPY2132_0_source_weight_docs", SOURCE_WEIGHT_DOCS / "AFRAME_NO_CURVATURE_TOWER_2132_NONCLAIM.csv", theorem + gates),
        ("COPY2132_1_branch_locked_wep", BRANCH_WEP / "P8_Y5_PARENT_QLOC_2132_AUX_SCALAR_COEFFICIENT_NONCLAIM.csv", aux_rows),
        ("COPY2132_2_acquisition_queue", QUEUE / "JR2132_BETA_ZERO_OR_SOURCE_ROW_QUEUE.csv", next_rows + aux_rows),
    ]
    results: list[dict[str, object]] = []
    for copy_id, destination, rows_to_write in copies:
        write_csv(destination, rows_to_write)
        results.append(row(copy_id=copy_id, destination=str(destination), path_exists=destination.exists(), row_count=len(rows_to_write), parse_ok=csv_rows_parse(destination)))
    return results


def validation_rows(
    sources: list[dict[str, object]],
    theorem: list[dict[str, object]],
    aux_rows: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    copies: list[dict[str, object]],
    csv_paths: list[Path],
) -> list[dict[str, object]]:
    sources_ok = all(truthy(item["path_exists"]) and truthy(item["needles_found"]) for item in sources)
    theorem_ok = any(item["theorem_id"] == "NT2132_5_verdict" and item["status"] == "NO_TOWER_THEOREM_NOT_DERIVED" for item in theorem)
    aux_ok = any(item["aux_id"] == "AUX2132_0_beta" and item["current_value"] == "MISSING_BETA_A" for item in aux_rows) and any(item["aux_id"] == "AUX2132_5_acceptance" and item["status"] == "AUX_SCALAR_ROW_BLOCKED_NONCLAIM" for item in aux_rows)
    gates_ok = any(item["gate_id"] == "GATE2132_2_aux_row_written" and truthy(item["gate_pass"]) for item in gates) and any(item["gate_id"] == "GATE2132_6_local_GR_Newton_PPN_claim" and not truthy(item["gate_pass"]) for item in gates)
    decisions_ok = any(item["decision_id"] == "DEC2132_2" and "BETA_ZERO" in str(item["decision"]) for item in decisions)
    next_ok = any(item["route_id"] == "NEXT2132_0_2133" for item in next_rows)
    branch_ok = all(truthy(item["path_exists"]) and truthy(item["parse_ok"]) for item in copies)
    csv_ok = all(path.exists() and csv_rows_parse(path) for path in csv_paths)
    no_claim_flags = all(
        not truthy(item.get("claim_allowed", False)) and not truthy(item.get("valid_for_claim", False))
        for group in (sources, theorem, aux_rows, gates, decisions, next_rows, copies)
        for item in group
    )
    formalization_clean = count_formalization_modified() == 0 and not formalization_has_2132_artifacts()
    pycache_clean = not (Path(__file__).resolve().parent / "__pycache__").exists()
    all_ok = all([sources_ok, theorem_ok, aux_ok, gates_ok, decisions_ok, next_ok, branch_ok, csv_ok, no_claim_flags, formalization_clean, pycache_clean])
    checks = [
        ("VAL2132_00_sources", sources_ok, "all cited no-tower sources exist and contain expected needles"),
        ("VAL2132_01_theorem", theorem_ok, "no-tower theorem attempt is explicit and not derived"),
        ("VAL2132_02_aux_rows", aux_ok, "auxiliary scalar coefficient row is staged but blocked by missing beta/M"),
        ("VAL2132_03_gates", gates_ok, "aux row gate passes while local-GR claim gate fails"),
        ("VAL2132_04_decisions", decisions_ok, "decision ledger selects beta-zero/source row next"),
        ("VAL2132_05_next", next_ok, "next target is beta_A zero or source row"),
        ("VAL2132_06_branch_copies", branch_ok, "branch copies exist and parse"),
        ("VAL2132_07_csv_parse", csv_ok, "all generated CSVs parse cleanly"),
        ("VAL2132_08_no_claim_flags", no_claim_flags, "no generated row allows a claim"),
        ("VAL2132_09_formalization_clean", formalization_clean, "formalization-workbench untouched by 2132"),
        ("VAL2132_10_no_pycache", pycache_clean, "scripts __pycache__ removed"),
        ("VAL2132_OVERALL", all_ok, "2132 fails the no-integrated-curvature-tower theorem honestly and stages a nonclaim auxiliary-scalar beta/M coefficient row."),
    ]
    return [row(check_id=check_id, status="PASS" if passed else "FAIL", detail=detail) for check_id, passed, detail in checks]


def write_doc(
    sources: list[dict[str, object]],
    theorem: list[dict[str, object]],
    aux_rows: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    copies: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    content = "\n\n".join(
        [
            "# 2132 - Y5/R2FR No Integrated Curvature Tower Or Aux Scalar Coefficient Row",
            "## Current Verdict",
            "2132 attacks the sneaky loophole: a primitive action can look clean, then a hidden scalar/auxiliary sector can regenerate `R^2` after variation. The no-tower theorem does not close yet. The conditional auxiliary-elimination logic is useful, but the needed parent grammar, no-curvature-coupling, no-kernel, boundary silence and readout stability clauses are unsigned.",
            "The fallback is now concrete rather than vague. A finite auxiliary-scalar branch must expose `beta_A`, `M_A^2`, the normalization converting `beta_A^2/(2M_A^2)` into `c_R2_eff`, and the source/readout/scalaron regime before any R10 or PPN comparison. Next sharp target is therefore `beta_A=0` or a sourced beta row.",
            "## Source Register",
            md_table(sources, ["source_id", "source_path", "path_exists", "needles_found", "role", "valid_for_claim"]),
            "## No Integrated Curvature Tower Attempt",
            md_table(theorem, ["theorem_id", "theorem_piece", "condition", "status", "proof_result", "blocker", "valid_for_claim"]),
            "## Auxiliary Scalar Coefficient Row",
            md_table(aux_rows, ["aux_id", "quantity", "meaning", "formula_or_rule", "required_input", "current_value", "status", "valid_for_claim"]),
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
    theorem = no_tower_theorem_rows()
    aux_rows = aux_scalar_coefficient_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_rows = next_target_rows()

    paths = {
        "sources": OUT / "P8_Y5_PARENT_QLOC_2132_SOURCE_REGISTER.csv",
        "theorem": OUT / "P8_Y5_PARENT_QLOC_2132_NO_TOWER_THEOREM_ATTEMPT.csv",
        "aux": OUT / "P8_Y5_PARENT_QLOC_2132_AUX_SCALAR_COEFFICIENT_ROW.csv",
        "gates": OUT / "P8_Y5_PARENT_QLOC_2132_CLAIM_GATES.csv",
        "decisions": OUT / "P8_Y5_PARENT_QLOC_2132_DECISION_LEDGER.csv",
        "next": OUT / "P8_Y5_PARENT_QLOC_2132_NEXT_TARGET.csv",
        "branch": OUT / "P8_Y5_PARENT_QLOC_2132_BRANCH_COPIES.csv",
        "validation": OUT / "P8_Y5_BRR545_2132_VALIDATION.csv",
    }
    write_csv(paths["sources"], sources)
    write_csv(paths["theorem"], theorem)
    write_csv(paths["aux"], aux_rows)
    write_csv(paths["gates"], gates)
    write_csv(paths["decisions"], decisions)
    write_csv(paths["next"], next_rows)

    copies = write_branch_copies(theorem, aux_rows, gates, next_rows)
    write_csv(paths["branch"], copies)

    remove_pycache()
    csv_paths = [path for key, path in paths.items() if key != "validation"] + [Path(str(copy["destination"])) for copy in copies]
    validation = validation_rows(sources, theorem, aux_rows, gates, decisions, next_rows, copies, csv_paths)
    write_csv(paths["validation"], validation)
    write_doc(sources, theorem, aux_rows, gates, decisions, next_rows, copies, validation)

    print(f"wrote {DOC}")
    print(f"validation {paths['validation']}")


if __name__ == "__main__":
    main()
