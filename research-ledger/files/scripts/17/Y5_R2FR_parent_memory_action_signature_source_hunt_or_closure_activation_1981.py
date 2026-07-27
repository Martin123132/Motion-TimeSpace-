from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


BRANCH = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
ROOT = Path(__file__).resolve().parents[1]
FORMALIZATION = ROOT.parent / "formalization-workbench"
MTS_RESIDUALS = ROOT / "source-intake" / "mts_residuals"
SOURCE_WEIGHT_DOCS = ROOT / "source-intake" / "source-weight" / "docs"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"

DOC_PATH = ROOT / "1981-Y5-R2FR-parent-memory-action-signature-source-hunt-or-closure-activation.md"
VALIDATION_PATH = MTS_RESIDUALS / "P8_Y5_BRR545_1981_VALIDATION.csv"

SOURCES = {
    "1980_doc": {
        "path": ROOT / "1980-Y5-R2FR-parent-memory-positivity-lemma-or-closure.md",
        "needles": ["DEC1980_2_best_next", "NEXT1980_0_primary"],
    },
    "1980_validation": {
        "path": MTS_RESIDUALS / "P8_Y5_BRR545_1980_VALIDATION.csv",
        "needles": ["VAL1980_OVERALL", "PASS"],
    },
    "1306_doc": {
        "path": ROOT / "1306-Y5-R10-RAB-Zm-parent-function-or-XB-domain-range.md",
        "needles": ["NO_PARENT_FUNCTION_FOUND_DEMOTE_TO_EXPLICIT_CLOSURE", "CONSTANT_CANONICAL_CLOSURE_ALLOWED_FOR_PRIVATE_SENSITIVITY_ONLY"],
    },
    "1306_parent_scan": {
        "path": MTS_RESIDUALS / "P8_Y5_R10_1306_PARENT_FUNCTION_SCAN.csv",
        "needles": ["PFS1306_5_verdict", "NO_PARENT_FUNCTION_FOUND_DEMOTE_TO_EXPLICIT_CLOSURE"],
    },
    "1306_field_redefinition": {
        "path": MTS_RESIDUALS / "P8_Y5_R10_1306_FIELD_REDEFINITION_AUDIT.csv",
        "needles": ["FRA1306_3_verdict", "CONSTANT_CANONICAL_CLOSURE_ALLOWED_FOR_PRIVATE_SENSITIVITY_ONLY"],
    },
    "1381_zm_audit": {
        "path": MTS_RESIDUALS / "P8_Y5_R10_1381_ZM_SIGN_VALUE_UNIT_AUDIT.csv",
        "needles": ["ZMS1381_7_verdict", "NO_SOURCE_BACKED_SIGN_VALUE_UNIT_ROW"],
    },
    "1384_canonicalization": {
        "path": MTS_RESIDUALS / "P8_Y5_R10_1384_CANONICALIZATION_DERIVATION_AUDIT.csv",
        "needles": ["CDA1384_8_verdict", "CANONICAL_GAP_COUPLING_PIVOT_SELECTED"],
    },
    "1592_signature": {
        "path": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1592_PARENT_SIGNATURE_AUDIT.csv",
        "needles": ["PSA1592_7_verdict", "PARENT_SIGNATURE_NOT_CLOSED_CANONICAL_SOURCE_ACQUISITION_REQUIRED"],
    },
    "1305_zm_sign": {
        "path": ROOT / "1305-Y5-R10-RAB-Zm-sign-value-or-gradient-profile-bound.md",
        "needles": ["NO_ZM_SIGN_OR_VALUE_CLAIM_KEEP_ACQUISITION_CONTRACT", "CG1305_4_local_GR"],
    },
    "826_parent_action": {
        "path": MTS_RESIDUALS / "P8_Y5_R10_826_PARENT_ACTION_ANSATZ.csv",
        "needles": ["AA826_1_memory_sector", "candidate_coefficient_scaffold"],
    },
    "1979_coercivity": {
        "path": ROOT / "1979-Y5-R2FR-M2-Z-domain-theorem-or-first-finite-row.md",
        "needles": ["THM1979_5_gap", "SIG1979_0_kinetic"],
    },
    "1042_nohair_gate": {
        "path": MTS_RESIDUALS / "P8_Y5_R10_1042_NOHAIR_PREMISE_GATE.csv",
        "needles": ["NHP1042_6_verdict", "FAIL_CURRENT_CLAIM_NOHAIR_NOT_PARENT_SIGNED"],
    },
}

OUTPUTS = {
    "source_register": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1981_SOURCE_REGISTER.csv",
    "hunt_ledger": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1981_SIGNATURE_SOURCE_HUNT_LEDGER.csv",
    "verdict": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1981_SIGNATURE_VERDICT.csv",
    "closure_activation": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1981_CLOSURE_ACTIVATION_LEDGER.csv",
    "retained_residuals": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1981_RETAINED_RESIDUAL_INPUTS.csv",
    "claim_gate": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1981_CLAIM_GATE.csv",
    "decision": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1981_DECISION_LEDGER.csv",
    "next": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1981_NEXT_TARGET.csv",
    "snapshot": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1981_PROJECT_STATUS_SNAPSHOT.csv",
    "source_weight": SOURCE_WEIGHT_DOCS / "PARENT_MEMORY_SIGNATURE_SOURCE_HUNT_1981_NONCLAIM.csv",
    "queue": RAB_QUEUE / "JR1981_WIDER_PARENT_ACTION_SOURCE_HUNT_QUEUE.csv",
}


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


CREATED_AT = now()


def ensure_dirs() -> None:
    for path in [MTS_RESIDUALS, SOURCE_WEIGHT_DOCS, RAB_QUEUE, DOC_PATH.parent]:
        path.mkdir(parents=True, exist_ok=True)


def row(values: dict[str, object]) -> dict[str, str]:
    defaults = {
        "branch": BRANCH,
        "id": "",
        "valid_for_claim": "false",
        "public_claim": "false",
        "created_at_utc": CREATED_AT,
    }
    merged = {**defaults, **values}
    return {key: str(value) for key, value in merged.items()}


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    if not rows:
        raise ValueError(f"refusing to write empty csv: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def source_register_rows() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for source_id, config in SOURCES.items():
        path = config["path"]
        text = path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""
        missing = [needle for needle in config["needles"] if needle not in text]
        rows.append(
            row(
                {
                    "id": f"SRC1981_{len(rows):02d}_{source_id}",
                    "source_id": source_id,
                    "source_path": str(path),
                    "required_needles": "; ".join(config["needles"]),
                    "exists": str(path.exists()).lower(),
                    "needle_status": "PASS" if not missing else "MISSING: " + "; ".join(missing),
                    "role": "signature-source hunt for parent memory positivity and closure decision",
                }
            )
        )
    return rows


def build_tables() -> dict[str, list[dict[str, str]]]:
    hunt_ledger = [
        row(
            {
                "id": "HUNT1981_0_action_slot",
                "target": "parent memory action slot",
                "best_source": "P8_Y5_R10_826_PARENT_ACTION_ANSATZ.csv / AA826_1_memory_sector",
                "finding": "The scalar-memory action slot exists: L_m=-1/2 Z_m(X_B) grad m grad m - V_R(m;X_B) plus sourced/bath terms.",
                "classification": "CANDIDATE_SLOT_PRESENT_NOT_PARENT_SIGNED",
                "why_not_claim": "the same row says Z_m, V_R, X_B, and source/bath terms remain unsigned parent coefficients",
            }
        ),
        row(
            {
                "id": "HUNT1981_1_Zm_law",
                "target": "source-backed Z_m(X_B) law",
                "best_source": "1306 parent function scan; 1381 sign/value/unit audit",
                "finding": "Only the symbol Z_m(X_B) is present; no equation, value, theorem-bound, units, or local/cosmology arena rule is supplied.",
                "classification": "NO_PARENT_ZM_FUNCTION_FOUND",
                "why_not_claim": "positive/no-ghost remains an acceptance condition, not a derived coefficient law",
            }
        ),
        row(
            {
                "id": "HUNT1981_2_canonicalization",
                "target": "constant canonical Z_m route",
                "best_source": "1306 field redefinition audit; 1384 canonicalization audit",
                "finding": "Constant positive Z_m can be absorbed into a canonical field, but the coupling reappears in V_R, J_m, source/test charges, alpha numerator, and PPN source normalization.",
                "classification": "PRIVATE_CLOSURE_ONLY_TRANSFER_AUDIT_REQUIRED",
                "why_not_claim": "canonicalization is not derivation unless the parent first adopts constant positive Z_m and all transferred couplings are audited",
            }
        ),
        row(
            {
                "id": "HUNT1981_3_variable_Zm",
                "target": "X_B-dependent Z_m absorption",
                "best_source": "1306 field redefinition audit; 1384 X_B gradient correction",
                "finding": "Variable Z_m(X_B(x)) cannot be absorbed away without derivative, metric-response, and arena-matching residuals.",
                "classification": "REJECTED_AS_GENERAL_PROOF",
                "why_not_claim": "variable field redefinitions can hide new couplings rather than remove them",
            }
        ),
        row(
            {
                "id": "HUNT1981_4_M2_gap",
                "target": "strict V_R Hessian / canonical gap",
                "best_source": "1384 canonicalization; 1592 parent signature audit; 1979/1980 G_m lemma",
                "finding": "The invariant target is the canonical gap mu_m^2, but the source-backed law for mu_m^2 or V_R'' is still missing.",
                "classification": "CANONICAL_GAP_PIVOT_DERIVED_SOURCE_MISSING",
                "why_not_claim": "M2_min cannot be inferred from extremum or canonical notation alone",
            }
        ),
        row(
            {
                "id": "HUNT1981_5_source_boundary",
                "target": "source-zero and boundary silence",
                "best_source": "1042 nohair premise gate; 1592 parent signature audit",
                "finding": "Even a positive operator would still need J_m/source, boundary, readout, and action-weight silence under the same parent action.",
                "classification": "SOURCE_BOUNDARY_PACKAGE_UNSIGNED",
                "why_not_claim": "local GR/Newton requires the sign theorem and source/boundary theorem together",
            }
        ),
        row(
            {
                "id": "HUNT1981_6_verdict",
                "target": "current post-checkpoint corpus verdict",
                "best_source": "aggregate 826, 1305, 1306, 1381, 1384, 1592, 1979, 1980",
                "finding": "No source-backed parent memory action signature was found inside the current post-checkpoint evidence chain.",
                "classification": "NO_CURRENT_PARENT_SIGNATURE_SOURCE",
                "why_not_claim": "route is conditional or closure-only until a wider corpus source supplies the parent action signs",
            }
        ),
    ]

    verdict = [
        row(
            {
                "id": "VER1981_0_Zm",
                "question": "Is Z_m>0 parent-signed in current post-checkpoint evidence?",
                "answer": "NO",
                "evidence": "1306/1381 find symbolic coefficient only; 1305 says sign/value proof does not close",
                "route_status": "DERIVATION_BLOCKED",
            }
        ),
        row(
            {
                "id": "VER1981_1_M2",
                "question": "Is M2_min>0 / canonical gap parent-signed?",
                "answer": "NO",
                "evidence": "1384/1592 pivot to mu_m^2 but do not source a law; 1979/1980 reject extremum as sufficient",
                "route_status": "DERIVATION_BLOCKED",
            }
        ),
        row(
            {
                "id": "VER1981_2_closure",
                "question": "Should closure be silently activated?",
                "answer": "NO",
                "evidence": "user/project stance is derivation-first; closure is useful only as declared private sensitivity branch",
                "route_status": "CLOSURE_AVAILABLE_NOT_ACTIVATED",
            }
        ),
        row(
            {
                "id": "VER1981_3_retained_residual",
                "question": "What is the safe branch if no parent source is found?",
                "answer": "retain explicit residual coefficients",
                "evidence": "Z_m, mu_m^2, J_m, boundary/readout terms, and transferred couplings stay in nonclaim rows",
                "route_status": "SAFE_NONCLAIM_BRANCH",
            }
        ),
    ]

    closure_activation = [
        row(
            {
                "id": "CA1981_0_constant_canonical",
                "closure_option": "Z_m=1 in canonical memory field units",
                "activation": "NOT_ACTIVATED",
                "reason": "would be mathematically clean for private algebra, but it is not derived and moves coupling into V_R/J_m/source/test normalization",
                "allowed_if_later": "only as an explicit private sensitivity branch with transfer audit",
            }
        ),
        row(
            {
                "id": "CA1981_1_bounded_positive_function",
                "closure_option": "0<Z_m_min<=Z_m(X_B)<=Z_m_bar",
                "activation": "NOT_ACTIVATED",
                "reason": "no source-backed function, local X_B range, D_loc, or units package exists",
                "allowed_if_later": "only after explicit interval and same-arena rule are written",
            }
        ),
        row(
            {
                "id": "CA1981_2_closure_only_verdict",
                "closure_option": "current local memory positivity route",
                "activation": "DECLARED_CLOSURE_ONLY_WITH_CURRENT_POSTCHECKPOINT_CORPUS",
                "reason": "the theorem is conditional and no parent signature source has been found in this evidence chain",
                "allowed_if_later": "can be reopened if wider corpus search supplies a parent action/signature",
            }
        ),
    ]

    retained_residuals = [
        row(
            {
                "id": "RR1981_0_Zm",
                "coefficient": "Z_m / Z_min / Z_bar",
                "status": "RETAINED_NONCLAIM",
                "needed_source": "parent memory field-space metric or coefficient law with units and branch range",
                "blocks": "ellipticity, no-hair, local stress bound, local-GR gate",
            }
        ),
        row(
            {
                "id": "RR1981_1_mu",
                "coefficient": "mu_m^2 or M2_min",
                "status": "RETAINED_NONCLAIM",
                "needed_source": "canonical gap law or V_R'' lower bound after zero-mode projection",
                "blocks": "H_m inverse, finite range, Schur suppression",
            }
        ),
        row(
            {
                "id": "RR1981_2_source",
                "coefficient": "J_m / qbar / source-test coupling",
                "status": "RETAINED_NONCLAIM",
                "needed_source": "same-parent matter/source descent or bounded source rows",
                "blocks": "source-free no-hair and fifth-force amplitude",
            }
        ),
        row(
            {
                "id": "RR1981_3_boundary",
                "coefficient": "boundary/readout/action-weight residuals",
                "status": "RETAINED_NONCLAIM",
                "needed_source": "boundary class, readout descent, action-weight exclusion or bounds",
                "blocks": "zero-profile theorem and Newton/common-matter reentry",
            }
        ),
    ]

    claim_gate = [
        row(
            {
                "id": "GATE1981_0_parent_signature",
                "gate": "source-backed parent memory signature exists",
                "status": "BLOCKED",
                "reason": "source hunt found candidate/formula rows only",
                "required_to_open": "wider corpus parent action source or new derivation",
            }
        ),
        row(
            {
                "id": "GATE1981_1_closure_claim",
                "gate": "closure can be used as claim",
                "status": "BLOCKED",
                "reason": "closure is private/nonclaim and not activated for local-GR proof",
                "required_to_open": "not applicable; closure is not a proof",
            }
        ),
        row(
            {
                "id": "GATE1981_2_local_GR",
                "gate": "derived local GR/Newton limit",
                "status": "BLOCKED",
                "reason": "Z_m, M2/canonical gap, source, and boundary packages are not parent-signed",
                "required_to_open": "same-parent action signature plus source/boundary/conservation/Newton gates",
            }
        ),
    ]

    decision = [
        row(
            {
                "id": "DEC1981_0_source_hunt",
                "decision": "NO_POSTCHECKPOINT_PARENT_SIGNATURE_SOURCE_FOUND",
                "because": "826/1306/1381/1592 collectively say the slot and conditional algebra exist, but sign/value/function/source ownership does not.",
                "next_action": "scan wider corpus/core docs before permanently accepting closure-only status",
            }
        ),
        row(
            {
                "id": "DEC1981_1_no_silent_closure",
                "decision": "DO_NOT_ACTIVATE_CLOSURE_BY_DEFAULT",
                "because": "the project target is derivable local GR/Newton; closure would only be private scaffolding.",
                "next_action": "retain residual coefficients and hunt a parent action source",
            }
        ),
        row(
            {
                "id": "DEC1981_2_best_next",
                "decision": "WIDER_CORPUS_PARENT_ACTION_SCAN",
                "because": "current post-checkpoint evidence is exhausted on Z_m; the only non-circular leap is to search the wider MTS corpus for parent action/signature text.",
                "next_action": "1982-Y5-R2FR-wider-corpus-parent-action-signature-scan.md",
            }
        ),
    ]

    next_rows = [
        row(
            {
                "id": "NEXT1981_0_primary",
                "status": "selected",
                "target_doc": "1982-Y5-R2FR-wider-corpus-parent-action-signature-scan.md",
                "target_script": "scripts/Y5_R2FR_wider_corpus_parent_action_signature_scan_1982.py",
                "task": "scan the wider Motion-TimeSpace corpus, not just post-checkpoint rows, for parent action/signature material that can sign Z_m, V_R'', canonical gap, source-zero, or boundary silence.",
                "success_condition": "find a source-backed parent action signature candidate, or record that current available corpus has no derivation source and the route remains closure/residual only",
            }
        )
    ]

    snapshot = [
        row(
            {
                "id": "SNAP1981_0_position",
                "area": "local GR derivation",
                "status": "SHARP_BLOCKER_NOT_DEAD_END",
                "summary": "The local operator theorem is real, but current post-checkpoint corpus lacks the parent action signature that would make it a derivation.",
            }
        ),
        row(
            {
                "id": "SNAP1981_1_improvement",
                "area": "what improved",
                "status": "CIRCLING_REDUCED",
                "summary": "We no longer have a vague coupling problem; we have a named missing parent-signature source: Z_m law, canonical gap/V_R'', source-zero, boundary/readout silence.",
            }
        ),
        row(
            {
                "id": "SNAP1981_2_risk",
                "area": "risk",
                "status": "SERIOUS",
                "summary": "If the wider corpus cannot supply the parent action signature, this local transition route remains closure-only and cannot carry the derived-GR claim.",
            }
        ),
    ]

    source_weight = [
        row(
            {
                "id": "SW1981_0",
                "doc": DOC_PATH.name,
                "weight": "private_nonclaim_source_hunt_verdict",
                "claim_safety": "all claim flags false; closure not silently activated",
                "use": "decides whether post-checkpoint corpus owns parent memory positivity",
            }
        )
    ]

    queue = [
        row(
            {
                "id": "Q1981_0_wider_parent_action_scan",
                "quantity": "parent action/signature source outside post-checkpoint rows",
                "priority": "highest",
                "why": "post-checkpoint source chain has no parent-signed Z_m or canonical gap",
                "target": "1982 wider corpus scan",
            }
        )
    ]

    return {
        "source_register": source_register_rows(),
        "hunt_ledger": hunt_ledger,
        "verdict": verdict,
        "closure_activation": closure_activation,
        "retained_residuals": retained_residuals,
        "claim_gate": claim_gate,
        "decision": decision,
        "next": next_rows,
        "snapshot": snapshot,
        "source_weight": source_weight,
        "queue": queue,
    }


def all_claim_flags_false(tables: dict[str, list[dict[str, str]]]) -> bool:
    return all(
        item.get("valid_for_claim") == "false" and item.get("public_claim") == "false"
        for table_rows in tables.values()
        for item in table_rows
    )


def output_csvs_parse() -> bool:
    for path in OUTPUTS.values():
        with path.open(newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
        if not rows:
            return False
    return True


def formalization_1981_artifact_count() -> int:
    if not FORMALIZATION.exists():
        return 0
    return len([path for path in FORMALIZATION.rglob("*1981*") if path.is_file()])


def validate(tables: dict[str, list[dict[str, str]]]) -> list[dict[str, str]]:
    source_ok = all(
        item["exists"] == "true" and item["needle_status"] == "PASS"
        for item in tables["source_register"]
    )
    hunt_by_id = {item["id"]: item for item in tables["hunt_ledger"]}
    verdict_by_id = {item["id"]: item for item in tables["verdict"]}
    closure_by_id = {item["id"]: item for item in tables["closure_activation"]}
    gates_blocked = all(item["status"] == "BLOCKED" for item in tables["claim_gate"])
    next_selected = tables["next"][0]["target_doc"] == "1982-Y5-R2FR-wider-corpus-parent-action-signature-scan.md"
    pycache_path = ROOT / "scripts" / "__pycache__"
    formalization_count = formalization_1981_artifact_count()
    specs = [
        ("VAL1981_00_sources", source_ok, "all source paths exist and continuity needles found"),
        (
            "VAL1981_01_no_parent_signature",
            hunt_by_id["HUNT1981_6_verdict"]["classification"] == "NO_CURRENT_PARENT_SIGNATURE_SOURCE",
            "post-checkpoint source hunt finds no parent signature",
        ),
        (
            "VAL1981_02_Zm_answer_no",
            verdict_by_id["VER1981_0_Zm"]["answer"] == "NO",
            "Z_m is not parent-signed",
        ),
        (
            "VAL1981_03_M2_answer_no",
            verdict_by_id["VER1981_1_M2"]["answer"] == "NO",
            "M2/canonical gap is not parent-signed",
        ),
        (
            "VAL1981_04_closure_not_silent",
            closure_by_id["CA1981_0_constant_canonical"]["activation"] == "NOT_ACTIVATED",
            "constant canonical closure is not silently activated",
        ),
        (
            "VAL1981_05_closure_only_declared",
            closure_by_id["CA1981_2_closure_only_verdict"]["activation"] == "DECLARED_CLOSURE_ONLY_WITH_CURRENT_POSTCHECKPOINT_CORPUS",
            "route is declared closure-only with current post-checkpoint evidence",
        ),
        ("VAL1981_06_claim_gates", gates_blocked, "all claim gates remain blocked"),
        (
            "VAL1981_07_decision",
            tables["decision"][-1]["decision"] == "WIDER_CORPUS_PARENT_ACTION_SCAN",
            "decision selects wider corpus scan",
        ),
        ("VAL1981_08_next_target", next_selected, "1982 target selected"),
        ("VAL1981_09_claim_flags_safe", all_claim_flags_false(tables), "claim flags all false"),
        ("VAL1981_10_csv_parse", output_csvs_parse(), "all generated CSVs parse with rows"),
        ("VAL1981_11_pycache_absent", not pycache_path.exists(), "scripts __pycache__ absent"),
        ("VAL1981_12_formalization_untouched", formalization_count == 0, f"formalization_1981_artifact_count={formalization_count}"),
    ]
    rows = [
        {
            "validation_id": validation_id,
            "status": "PASS" if passed else "FAIL",
            "detail": detail,
            "valid_for_claim": "false",
            "public_claim": "false",
        }
        for validation_id, passed, detail in specs
    ]
    rows.append(
        {
            "validation_id": "VAL1981_OVERALL",
            "status": "PASS" if all(item["status"] == "PASS" for item in rows) else "FAIL",
            "detail": "1981 parent memory action signature source hunt or closure activation",
            "valid_for_claim": "false",
            "public_claim": "false",
        }
    )
    return rows


def markdown_table(rows: list[dict[str, str]]) -> str:
    headers = list(rows[0].keys())
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for item in rows:
        values = [item.get(header, "").replace("|", "\\|").replace("\n", "<br>") for header in headers]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def write_markdown(tables: dict[str, list[dict[str, str]]], validation_rows: list[dict[str, str]]) -> None:
    sections = [
        ("Source Register", tables["source_register"]),
        ("Signature Source Hunt Ledger", tables["hunt_ledger"]),
        ("Signature Verdict", tables["verdict"]),
        ("Closure Activation Ledger", tables["closure_activation"]),
        ("Retained Residual Inputs", tables["retained_residuals"]),
        ("Claim Gate", tables["claim_gate"]),
        ("Decision Ledger", tables["decision"]),
        ("Next Target", tables["next"]),
        ("Project Status Snapshot", tables["snapshot"]),
        ("Validation", validation_rows),
    ]
    lines = [
        "# 1981 Y5 R2FR: Parent Memory Action Signature Source Hunt Or Closure Activation",
        "",
        "Private checkpoint. This performs the post-checkpoint source hunt requested by 1980: is there already a parent action/signature row that signs the memory kinetic coefficient and strict memory gap?",
        "",
        "Verdict: no source-backed parent memory signature is found in the current post-checkpoint evidence chain. The local memory positivity route is therefore closure-only with the current post-checkpoint corpus, but closure is **not** silently activated for claims. The safe branch retains `Z_m`, canonical gap or `M2_min`, source coupling, and boundary/readout coefficients as explicit nonclaim residual inputs.",
        "",
        "No local-GR, Newton, EH, R10, PPN, clock, orbital, or public claim follows from 1981.",
        "",
    ]
    for title, rows in sections:
        lines.extend([f"## {title}", "", markdown_table(rows), ""])
    DOC_PATH.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    ensure_dirs()
    pycache_path = ROOT / "scripts" / "__pycache__"
    if pycache_path.exists():
        shutil.rmtree(pycache_path)
    tables = build_tables()
    for output_name, path in OUTPUTS.items():
        write_csv(path, tables[output_name])
    validation_rows = validate(tables)
    write_csv(VALIDATION_PATH, validation_rows)
    write_markdown(tables, validation_rows)
    if pycache_path.exists():
        shutil.rmtree(pycache_path)
    overall = validation_rows[-1]["status"]
    print(f"wrote {DOC_PATH}")
    print(f"wrote {VALIDATION_PATH}")
    print(f"VAL1981_OVERALL={overall}")
    return 0 if overall == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
