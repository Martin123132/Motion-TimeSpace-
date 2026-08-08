from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


BRANCH_ID = "MTS_R2FR_PARENT_TYPED_OBJECT_LANGUAGE_AND_VERTICAL_BASIS_CERTIFICATE_OR_BALPHA_BG_BOUND_ROW_2434"
CHECKPOINT_ID = "2434"

ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = ROOT.parent
FORMALIZATION = PROJECT_ROOT / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
MICROSCOPE = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
BETA_DOCS = ROOT / "source-intake" / "beta-source" / "docs"

DOC = ROOT / "2434-Y5-R2FR-parent-typed-object-language-and-vertical-basis-certificate-or-balpha-bg-bound-row.md"

OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_2434_SOURCE_REGISTER.csv",
    "typed_certificate": OUT / "P8_Y5_PARENT_QLOC_2434_TYPED_OBJECT_LANGUAGE_CERTIFICATE.csv",
    "vertical_certificate": OUT / "P8_Y5_PARENT_QLOC_2434_VERTICAL_BASIS_CERTIFICATE.csv",
    "combined_owner": OUT / "P8_Y5_PARENT_QLOC_2434_COMBINED_CERTIFICATE_OWNER_GATE.csv",
    "bound_row": OUT / "P8_Y5_PARENT_QLOC_2434_BALPHA_BG_BOUND_ROW_CONTRACT.csv",
    "claim_gates": OUT / "P8_Y5_PARENT_QLOC_2434_CLAIM_GATES.csv",
    "decisions": OUT / "P8_Y5_PARENT_QLOC_2434_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_2434_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_PARENT_QLOC_2434_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2434_VALIDATION.csv",
}

COPY_TARGETS = {
    "queue_typed": QUEUE / "JR2434_TYPED_OBJECT_LANGUAGE_CERTIFICATE_NONCLAIM.csv",
    "queue_bound": QUEUE / "JR2434_BALPHA_BG_BOUND_ROW_CONTRACT_NONCLAIM.csv",
    "branch_wep": MICROSCOPE / "typed_vertical_certificate_nonclaim_2434.csv",
    "beta_docs": BETA_DOCS / "BALPHA_BG_BOUND_CONTRACT_2434_NONCLAIM.csv",
}

SOURCES = [
    {
        "source_id": "SRC2434_00_2433_handoff",
        "source_path": ROOT / "2433-Y5-R2FR-vertical-kernel-and-visible-target-category-owner-or-first-coefficient-bound-row.md",
        "needles": ["NEXT2433_0_selected", "KGO2433_7_verdict", "VAL2433_OVERALL"],
        "role": "fresh handoff selecting typed object-language plus vertical-basis certificate",
    },
    {
        "source_id": "SRC2434_01_2433_validation",
        "source_path": OUT / "P8_Y5_BRR545_2433_VALIDATION.csv",
        "needles": ["VAL2433_OVERALL", "PASS"],
        "role": "confirms 2433 passed before 2434",
    },
    {
        "source_id": "SRC2434_02_2433_combined",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_2433_KERNEL_TARGET_COMBINED_THEOREM.csv",
        "needles": ["KTT2433_0_target", "EXACT_CONDITIONAL_THEOREM"],
        "role": "combined kernel-target theorem input",
    },
    {
        "source_id": "SRC2434_03_1220_typed",
        "source_path": ROOT / "1220-Y5-R10-parent-typed-object-language-signature-or-finite-coupling-closure.md",
        "needles": ["PTOL1220_7_verdict", "PARENT_TYPED_OBJECT_LANGUAGE_SIGNATURE_NOT_DERIVED"],
        "role": "typed object-language signature precedent",
    },
    {
        "source_id": "SRC2434_04_2392_kernel",
        "source_path": ROOT / "2392-Y5-R2FR-vertical-kernel-presymplectic-null-and-matter-invisible-or-kernel-charge-row.md",
        "needles": ["VKN2392_5_verdict", "VKC2392_0_vertical_basis", "VAL2392_OVERALL"],
        "role": "vertical kernel/basis certificate precedent",
    },
    {
        "source_id": "SRC2434_05_1219_counterexamples",
        "source_path": ROOT / "1219-Y5-R10-typed-visible-coefficient-functor-or-hidden-scalar-counterexample-lock.md",
        "needles": ["HSC1219_1_alpha", "HSC1219_4_source_weight", "VAL1219_16_overall"],
        "role": "hidden scalar and source-weight counterexample lock",
    },
]


def timestamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def base_row(**kwargs: Any) -> dict[str, Any]:
    row = {
        "timestamp_utc": timestamp(),
        "branch_id": BRANCH_ID,
        "checkpoint_id": CHECKPOINT_ID,
        "valid_for_claim": False,
        "claim_allowed": False,
    }
    row.update(kwargs)
    return row


def stringify(value: Any) -> str:
    if isinstance(value, bool):
        return "True" if value else "False"
    return str(value)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({key: stringify(row.get(key, "")) for key in fields})


def csv_parses(path: Path) -> tuple[bool, int, str]:
    try:
        with path.open(newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
        return True, len(rows), "OK"
    except Exception as exc:
        return False, 0, f"{type(exc).__name__}: {exc}"


def table(headers: list[str], rows: list[dict[str, Any]]) -> str:
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        cells = [stringify(row.get(header, "")).replace("\n", " ").replace("|", "\\|") for header in headers]
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source in SOURCES:
        path = Path(source["source_path"])
        text = read_text(path)
        needles = source["needles"]
        found = [needle for needle in needles if needle in text]
        rows.append(
            base_row(
                source_id=source["source_id"],
                source_path=path,
                path_exists=path.exists(),
                required_needles="; ".join(needles),
                found_needles="; ".join(found),
                needles_found=path.exists() and len(found) == len(needles),
                role=source["role"],
            )
        )
    return rows


def typed_certificate_rows() -> list[dict[str, Any]]:
    rows = [
        ("TOL2434_0_parent_domain", "single parent object language before readout/fitting", "all fields, coefficients, measures, source maps and readouts have typed domains before empirical projection", "SCHEMA_WRITTEN_NOT_DERIVED", "hidden maps can be absent by taste rather than forbidden by grammar"),
        ("TOL2434_1_visible_coeff_domain", "visible coefficients depend only on q-blind observed objects plus fixed representation/topological labels", "Hom(hidden/profile/q-representative, Coeff_vis) is empty by syntax", "POWERFUL_RULE_NOT_PARENT_SIGNED", "b_alpha, b_mu, b_material and clock/source coefficients remain live"),
        ("TOL2434_2_matter_constants", "matter constants fixed as representation/superselection data or explicit residual rows", "masses, binding, alpha_EM and clock coefficients cannot silently depend on hidden q data", "CONDITIONAL_NOT_PARENT_SIGNED", "material marker drift survives"),
        ("TOL2434_3_source_weight_exclusion", "no source-only species/action prefactor target", "relative active source weights w_A are syntactically impossible except common calibration mode", "EXACT_CONDITIONAL_NOT_PARENT_SIGNED", "Delta_w/source-normalization remains live"),
        ("TOL2434_4_measure_current_owner", "common action scale, measure, Hilbert/source current owner", "all sectors use one parent normalization and no species-dependent action multiplier", "NOT_PARENT_SIGNED", "source-weight counterexample remains legal"),
        ("TOL2434_5_readout_EFT_closure", "radiative/effective/readout maps preserve typed domains", "S_eff, detector thresholds, clock readouts and source-worldtube projections cannot reintroduce hidden/q arguments", "READOUT_CLOSURE_UNSIGNED", "tree-level silence does not transfer to observables"),
        ("TOL2434_6_no_marker_extension", "no hidden scalar, material marker, domain selector or boundary class extends visible coefficient domains", "all scalar/marker extensions are typed out or explicitly residual", "NOT_DERIVED", "hidden scalar counterexamples remain active"),
        ("TOL2434_7_verdict", "parent typed object-language certificate", "TOL2434_0 through TOL2434_6 close as one parent signature", "PARENT_TYPED_OBJECT_LANGUAGE_CERTIFICATE_NOT_DERIVED", "finite b_alpha/b_g/coefficient rows remain live"),
    ]
    return [
        base_row(clause_id=clause_id, required_clause=clause, test=test, current_status=status, effect_if_unsigned=effect, clause_pass=False)
        for clause_id, clause, test, status, effect in rows
    ]


def vertical_certificate_rows() -> list[dict[str, Any]]:
    rows = [
        ("VBC2434_0_basis", "retained q-vertical basis", "list v_i as parent variations and prove v_i in ker(Dq) and ker(DObs_coeff)", "MISSING_PARENT_VERTICAL_BASIS", "epsilon_q_rank_or_integrability"),
        ("VBC2434_1_rank_bracket", "rank/involutivity", "rank(Dq) constant and [v_i,v_j] in span(V) with bracket table", "MISSING_RANK_BRACKET_AUDIT", "epsilon_q_rank_or_integrability"),
        ("VBC2434_2_presymplectic", "Theta/Q_v charge test", "derive Theta_parent and Q_v, then show compact local flux delta Q_v-i_v Theta_parent vanishes or is bounded", "MISSING_THETA_QV_ZERO_FLUX", "epsilon_kernel_charge"),
        ("VBC2434_3_matter", "matter/readout invisibility", "delta_v S_matter=0 and no direct source/material/worldtube slot for each v_i", "MISSING_MATTER_INVISIBILITY", "epsilon_matter_kernel"),
        ("VBC2434_4_boundary_history", "boundary/history/source-support silence", "Pi_local dB_v=0 and J_history[v]=0 or bounded in same branch", "MISSING_BOUNDARY_HISTORY_SILENCE", "epsilon_boundary_history"),
        ("VBC2434_5_same_branch", "same parent branch", "vertical basis, typed object language, Obs_coeff, source normalization, q operator and boundary class are one branch", "MISSING_SAME_BRANCH_LOCK", "B_total_q"),
        ("VBC2434_6_verdict", "vertical-basis certificate", "VBC2434_0 through VBC2434_5 pass together", "VERTICAL_BASIS_CERTIFICATE_NOT_DERIVED", "kernel/target theorem remains conditional"),
    ]
    return [
        base_row(clause_id=clause_id, required_clause=clause, test=test, current_status=status, fallback_symbol=fallback, clause_pass=False)
        for clause_id, clause, test, status, fallback in rows
    ]


def combined_owner_rows() -> list[dict[str, Any]]:
    return [
        base_row(owner_id="OWN2434_0_chain_rule_ready", object="coefficient chain-rule route", statement="If both certificates close, DObs_coeff(v_i)=0 and visible coefficient slopes vanish.", current_status="EXACT_CONDITIONAL_THEOREM_READY", claim_effect="would kill b_alpha/b_g/source-weight/readout coefficient drift"),
        base_row(owner_id="OWN2434_1_missing_typed", object="typed object-language side", statement="typed target category is not parent-signed", current_status="BLOCKED", claim_effect="hidden-visible Hom counterexamples remain"),
        base_row(owner_id="OWN2434_2_missing_vertical", object="vertical basis side", statement="retained v_i are not listed/proved parent-null/matter-invisible with Theta/Q_v zero flux", current_status="BLOCKED", claim_effect="kernel may be physical residual"),
        base_row(owner_id="OWN2434_3_bound_fallback", object="finite coefficient fallback", statement="first finite row should target b_alpha or b_g because those directly test hidden coefficient or shadow-frame leakage", current_status="NONCLAIM_CONTRACT_READY", claim_effect="requires real source-backed values before scoring"),
        base_row(owner_id="OWN2434_4_verdict", object="combined owner verdict", statement="typed grammar plus vertical basis certificate is not derived at 2434", current_status="FAIL_CURRENT_CLAIM_OWNER_PACKAGE_MISSING", claim_effect="J_q=0 and local-GR remain blocked"),
    ]


def bound_row_rows() -> list[dict[str, Any]]:
    rows = [
        ("BND2434_0_b_alpha", "b_alpha", "vertical derivative of EM/gauge kinetic or fine-structure coefficient", "dimensionless_or_per_q_unit", "clocks;WEP;R10;EM", "preferred if sourcing coefficient drift first", "MISSING_REAL_VALUE_OR_THEOREM_ZERO"),
        ("BND2434_1_b_g", "b_g", "universal Weyl/shadow-frame slope in e_obs=exp(b_g q)e_basic", "dimensionless_or_per_q_unit", "R10;PPN;WEP;clock", "preferred if testing frame leakage first; exchange uses c_g^2/product law", "MISSING_REAL_VALUE_OR_THEOREM_ZERO"),
        ("BND2434_2_required_fields", "first_bound_row_schema", "symbol, branch, definition, units, q normalization, theorem_zero, numeric_bound, uncertainty, source_path, projection_matrix, no_cancellation_group, valid_for_claim", "schema", "all_local_arenas", "no row can score unless every MISSING_* field is removed", "SCHEMA_READY_NONCLAIM"),
        ("BND2434_3_verdict", "first b_alpha/b_g row", "no numeric/theorem-zero coefficient row is filled at 2434", "n/a", "all_local_arenas", "next target should either derive the certificate or acquire one real source-backed coefficient bound", "NONCLAIM_NO_VALUE_FILLED"),
    ]
    return [
        base_row(row_id=row_id, symbol=symbol, definition=definition, units=units, observable_links=links, reason=reason, current_status=status, theorem_zero=False, source_backed=False, score_ready=False)
        for row_id, symbol, definition, units, links, reason, status in rows
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        base_row(claim_id="CGATE2434_0_typed_certificate", claim="parent typed object-language certificate is signed", gate_pass=False, reason="parent domain, coefficient domain, source-weight exclusion, measure owner and readout closure are unsigned"),
        base_row(claim_id="CGATE2434_1_vertical_certificate", claim="retained q-vertical basis is parent-null/matter-invisible", gate_pass=False, reason="basis, rank/bracket, Theta/Q_v, matter invisibility and boundary/history silence are missing"),
        base_row(claim_id="CGATE2434_2_DObs_coeff_zero", claim="DObs_coeff(v_q)=0 for all retained vertical directions", gate_pass=False, reason="requires both typed certificate and vertical certificate"),
        base_row(claim_id="CGATE2434_3_Jq_zero", claim="J_q coefficient channels theorem-zero", gate_pass=False, reason="b_alpha/b_g/source-weight/readout channels remain live"),
        base_row(claim_id="CGATE2434_4_first_bound_score", claim="first b_alpha/b_g finite row can score", gate_pass=False, reason="row contract exists but no source-backed value or theorem-zero proof"),
        base_row(claim_id="CGATE2434_5_local_GR", claim="local GR/Newton reduction follows", gate_pass=False, reason="q no-hair activation, J_q zero, boundary/source and PPN gates are not closed"),
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        base_row(decision_id="DEC2434_0_certificate_status", decision="CERTIFICATE_ROUTE_NOT_DERIVED", rationale="both typed grammar and vertical basis halves have exact contracts but missing parent owner data", consequence="do not promote J_q=0"),
        base_row(decision_id="DEC2434_1_best_theory_next", decision="ATTACK_THETA_QV_OR_TYPED_TARGET_SOURCE_DIRECTLY", rationale="vertical charge and typed target exclusion are the two hard locks", consequence="select a split next step rather than circling"),
        base_row(decision_id="DEC2434_2_best_empirical_fallback", decision="B_ALPHA_OR_B_G_FIRST_IF_DERIVATION_FAILS", rationale="these coefficients hit EM/clocks/WEP/R10 and frame leakage directly", consequence="finite row contract staged nonclaim"),
        base_row(decision_id="DEC2434_3_no_public", decision="NO_GITHUB_ACTION", rationale="private derivation/fallback gate only", consequence="continue private framework work"),
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            route_id="NEXT2434_0_selected",
            selection_status="selected",
            target_file="2435-Y5-R2FR-vertical-Noether-charge-Qv-and-typed-target-exclusion-or-balpha-bg-source-row.md",
            target_script="scripts/Y5_R2FR_vertical_Noether_charge_Qv_and_typed_target_exclusion_or_balpha_bg_source_row_2435.py",
            task="try the two hard owner locks directly: extract Theta_parent/Q_v and zero compact vertical charge, and prove typed target exclusion for hidden scalar/source-prefactor maps; if either fails, fill the first nonclaim b_alpha or b_g source-bound row",
            acceptance_target="vertical charge zero plus typed target exclusion closes, or one b_alpha/b_g row has units/source/projection/provenance and valid_for_claim=false",
            guardrails="do not invent coefficient values, use projection-by-declaration, cancel components, claim local GR/R10/PPN/WEP/clock/orbital pass, edit formalization-workbench, or push GitHub",
        )
    ]


def branch_copy_rows() -> list[dict[str, Any]]:
    copies = [
        ("queue_typed", OUTPUTS["typed_certificate"], COPY_TARGETS["queue_typed"], "typed object-language certificate nonclaim queue"),
        ("queue_bound", OUTPUTS["bound_row"], COPY_TARGETS["queue_bound"], "b_alpha/b_g bound-row contract nonclaim queue"),
        ("branch_wep", OUTPUTS["combined_owner"], COPY_TARGETS["branch_wep"], "typed/vertical owner status for WEP/local branch"),
        ("beta_docs", OUTPUTS["bound_row"], COPY_TARGETS["beta_docs"], "b_alpha/b_g bound contract for beta-source docs"),
    ]
    rows: list[dict[str, Any]] = []
    for copy_id, source, target, note in copies:
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
        rows.append(base_row(copy_id=copy_id, source_path=source, target_path=target, source_exists=source.exists(), target_exists=target.exists(), notes=note))
    return rows


def validation_rows(all_outputs: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    source_rows = all_outputs["source_register"]
    output_csvs = [path for key, path in OUTPUTS.items() if key != "validation"]
    formalization_hits: list[Path] = []
    for pattern in ["*2434-Y5-R2FR*", "*P8_Y5_PARENT_QLOC_2434*", "*P8_Y5_BRR545_2434*", "*JR2434*", "*BALPHA_BG_BOUND_CONTRACT_2434*"]:
        formalization_hits.extend(FORMALIZATION.rglob(pattern) if FORMALIZATION.exists() else [])

    checks = [
        ("VAL2434_00_sources_exist", all(row["path_exists"] for row in source_rows), "all cited source paths exist"),
        ("VAL2434_01_source_needles", all(row["needles_found"] for row in source_rows), "all cited source needles are present"),
        ("VAL2434_02_typed_verdict_blocked", any(row["clause_id"] == "TOL2434_7_verdict" and row["current_status"] == "PARENT_TYPED_OBJECT_LANGUAGE_CERTIFICATE_NOT_DERIVED" for row in all_outputs["typed_certificate"]), "typed certificate remains blocked"),
        ("VAL2434_03_vertical_verdict_blocked", any(row["clause_id"] == "VBC2434_6_verdict" and row["current_status"] == "VERTICAL_BASIS_CERTIFICATE_NOT_DERIVED" for row in all_outputs["vertical_certificate"]), "vertical certificate remains blocked"),
        ("VAL2434_04_combined_owner_blocked", any(row["owner_id"] == "OWN2434_4_verdict" and row["current_status"] == "FAIL_CURRENT_CLAIM_OWNER_PACKAGE_MISSING" for row in all_outputs["combined_owner"]), "combined owner package remains blocked"),
        ("VAL2434_05_bound_contract_nonclaim", all(not row["source_backed"] and not row["score_ready"] for row in all_outputs["bound_row"]), "b_alpha/b_g rows remain nonclaim contract only"),
        ("VAL2434_06_claims_blocked", all(not row["gate_pass"] for row in all_outputs["claim_gates"]), "all claim gates remain false"),
        ("VAL2434_07_next_target_written", any(row["route_id"] == "NEXT2434_0_selected" for row in all_outputs["next_target"]), "next target selected"),
        ("VAL2434_08_branch_copies", all(row["target_exists"] for row in all_outputs["branch_copies"]), "branch copies were written"),
        ("VAL2434_09_no_formalization_artifacts", len(formalization_hits) == 0, "no 2434 artifacts were written to formalization-workbench"),
    ]
    for check_id, passed, notes in checks:
        rows.append(base_row(check_id=check_id, status="PASS" if passed else "FAIL", notes=notes, detail="" if passed else "required checkpoint condition failed"))
    for path in output_csvs:
        parses, row_count, message = csv_parses(path)
        rows.append(base_row(check_id=f"VAL2434_CSV_{path.stem}", status="PASS" if parses and row_count > 0 else "FAIL", notes=f"CSV parses with {row_count} rows", detail=message))
    overall = all(row["status"] == "PASS" for row in rows)
    rows.append(
        base_row(
            check_id="VAL2434_OVERALL",
            status="PASS" if overall else "FAIL",
            notes="2434 builds the parent typed object-language plus vertical-basis certificate gate, refuses promotion, stages b_alpha/b_g nonclaim bound-row contracts, and selects vertical Q_v plus typed target exclusion or source row next",
            detail="",
        )
    )
    return rows


def write_markdown(all_outputs: dict[str, list[dict[str, Any]]]) -> None:
    sections = [
        "# 2434 - Y5/R2FR Parent Typed Object-Language And Vertical-Basis Certificate Or b_alpha/b_g Bound Row",
        "",
        "## Result",
        "- 2434 tries to turn the clean coupling theorem into an actual certificate: parent typed object-language plus retained q-vertical basis.",
        "- The certificate does not close. The typed side lacks parent domain, coefficient-domain, source-weight, measure/current, readout/EFT and no-marker clauses. The vertical side lacks basis, rank/bracket, `Theta/Q_v`, matter invisibility and boundary/history silence.",
        "- The exact consequence remains conditional: if both halves close, `DObs_coeff(v_q)=0` and visible coefficient slopes such as `b_alpha` and `b_g` vanish.",
        "- Because they do not close, the first finite coefficient fallback is staged as a nonclaim `b_alpha/b_g` bound-row contract only.",
        "",
        "## Practical Status",
        "This is the honest split: either we derive the grammar/kernel certificate, or we stop trying to talk the coupling away and source the first real coefficient bound. No ghost victories.",
        "",
        "## Source Register",
        table(["source_id", "source_path", "path_exists", "needles_found", "role"], all_outputs["source_register"]),
        "",
        "## Typed Object-Language Certificate",
        table(["clause_id", "required_clause", "test", "current_status", "effect_if_unsigned", "clause_pass", "valid_for_claim"], all_outputs["typed_certificate"]),
        "",
        "## Vertical-Basis Certificate",
        table(["clause_id", "required_clause", "test", "current_status", "fallback_symbol", "clause_pass", "valid_for_claim"], all_outputs["vertical_certificate"]),
        "",
        "## Combined Certificate Owner Gate",
        table(["owner_id", "object", "statement", "current_status", "claim_effect", "valid_for_claim"], all_outputs["combined_owner"]),
        "",
        "## b_alpha / b_g Bound Row Contract",
        table(["row_id", "symbol", "definition", "units", "observable_links", "reason", "current_status", "source_backed", "score_ready", "valid_for_claim"], all_outputs["bound_row"]),
        "",
        "## Claim Gates",
        table(["claim_id", "claim", "gate_pass", "reason", "valid_for_claim"], all_outputs["claim_gates"]),
        "",
        "## Decisions",
        table(["decision_id", "decision", "rationale", "consequence", "valid_for_claim"], all_outputs["decisions"]),
        "",
        "## Next Target",
        table(["route_id", "selection_status", "target_file", "target_script", "task", "acceptance_target", "guardrails"], all_outputs["next_target"]),
        "",
        "## Branch Copies",
        table(["copy_id", "source_path", "target_path", "source_exists", "target_exists", "notes"], all_outputs["branch_copies"]),
        "",
        "## Validation",
        table(["check_id", "status", "notes", "detail"], all_outputs["validation"]),
        "",
    ]
    DOC.write_text("\n".join(sections), encoding="utf-8")


def main() -> None:
    for path in (OUT, QUEUE, MICROSCOPE, BETA_DOCS):
        path.mkdir(parents=True, exist_ok=True)

    all_outputs: dict[str, list[dict[str, Any]]] = {
        "source_register": source_register_rows(),
        "typed_certificate": typed_certificate_rows(),
        "vertical_certificate": vertical_certificate_rows(),
        "combined_owner": combined_owner_rows(),
        "bound_row": bound_row_rows(),
        "claim_gates": claim_gate_rows(),
        "decisions": decision_rows(),
        "next_target": next_target_rows(),
    }

    for key, rows in all_outputs.items():
        write_csv(OUTPUTS[key], rows)

    all_outputs["branch_copies"] = branch_copy_rows()
    write_csv(OUTPUTS["branch_copies"], all_outputs["branch_copies"])
    all_outputs["validation"] = validation_rows(all_outputs)
    write_csv(OUTPUTS["validation"], all_outputs["validation"])
    write_markdown(all_outputs)

    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)

    print(DOC)
    print(OUTPUTS["validation"])
    print(f"VAL2434_OVERALL={all_outputs['validation'][-1]['status']}")


if __name__ == "__main__":
    main()
