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

DOC_PATH = ROOT / "1955-Y5-R2FR-local-EH-same-source-map-or-residual-l2-bound.md"
VALIDATION_PATH = MTS_RESIDUALS / "P8_Y5_BRR545_1955_VALIDATION.csv"

SOURCES = {
    "1954_doc": {
        "path": ROOT / "1954-Y5-R2FR-l2-source-boundary-zero-or-envelope.md",
        "needles": ["L2R1954_1_same_source_map_condition", "L2R1954_5_verdict", "NEXT1954_0_primary"],
    },
    "1954_validation": {
        "path": MTS_RESIDUALS / "P8_Y5_BRR545_1954_VALIDATION.csv",
        "needles": ["VAL1954_OVERALL", "PASS"],
    },
    "1954_residual_split": {
        "path": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1954_L2_RESIDUAL_SPLIT.csv",
        "needles": ["BASELINE_SPLIT_BUILT_NONCLAIM", "CONDITION_SHARPENED_NOT_SIGNED"],
    },
    "1954_residual_inputs": {
        "path": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1954_RESIDUAL_L2_INPUT_LEDGER.csv",
        "needles": ["Delta J_2^MTS", "MISSING_COMBINED_RESIDUAL_BOUND"],
    },
}


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def ensure_dirs() -> None:
    for directory in (MTS_RESIDUALS, SOURCE_WEIGHT_DOCS, RAB_QUEUE):
        directory.mkdir(parents=True, exist_ok=True)


def base(row_id: str) -> dict[str, object]:
    return {
        "branch": BRANCH,
        "row_id": row_id,
        "valid_for_claim": False,
        "public_claim": False,
        "created_utc": stamp(),
    }


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def source_register() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for source_id, spec in SOURCES.items():
        path = spec["path"]
        needles = spec["needles"]
        exists = path.exists()
        text = path.read_text(encoding="utf-8", errors="replace") if exists else ""
        missing = [needle for needle in needles if needle not in text]
        row = base(source_id)
        row.update(
            {
                "source_path": str(path),
                "purpose": "1955 local EH same-source map or residual l2 bound",
                "required_needles": ";".join(needles),
                "status": "EXISTS_NEEDLES_CONFIRMED" if exists and not missing else "MISSING_SOURCE_OR_NEEDLE",
                "missing_needles": ";".join(missing),
            }
        )
        rows.append(row)
    return rows


def theorem_contract_rows() -> list[dict[str, object]]:
    entries = [
        (
            "EH1955_0_target",
            "Residual l=2 vanishes if the local parent variation has the same metric source map as EH/GR and no extra l=2 boundary degree of freedom.",
            "Delta B_2^MTS=0 <- Delta E_ij^extra|l=2=0 and Delta h_boundary2^MTS=0",
            "THEOREM_TARGET_EXACT",
            "This is the clean bridge to GR: do not demand spherical Sun; demand no extra residual beyond GR.",
            "all clauses below must be parent-signed",
        ),
        (
            "EH1955_1_variation_split",
            "Write the local parent metric equation as EH plus ordinary matter plus an extra residual operator.",
            "E_ij^parent = E_ij^EH[g] - kappa T_ij^matter + R_ij^extra",
            "DECOMPOSITION_BUILT",
            "The problem is reduced to the l=2 projection of R_ij^extra.",
            "need parent action/variation signature",
        ),
        (
            "EH1955_2_same_source_map",
            "Ordinary matter multipoles are GR baseline if the matter stress tensor enters with the same tensor, normalization, and metric as EH/GR.",
            "Delta J_2^MTS=P_2[(T_ij^parent-T_ij^GR)] = 0",
            "CONDITION_SHARPENED_NOT_SIGNED",
            "This is the fair-comparison theorem: source l=2 is only dangerous when MTS changes the source map.",
            "need universal metric coupling and normalization proof",
        ),
        (
            "EH1955_3_extra_source_silence",
            "Extra fields do not create residual l=2 if their local on-shell stress/residual is zero, pure trace/common-mode, or quotient-vertical null under the observed metric map.",
            "P_2[R_ij^extra]=0 if R_ij^extra=A(r)delta_ij + E_X Dq[v_X] with E_X=0 or Dq[v_X]=0",
            "CONDITION_SHARPENED_NOT_SIGNED",
            "This is where the parent coupling question bites: extra-sector coupling must be silent or common-mode locally.",
            "need on-shell/vertical/descent proof",
        ),
        (
            "EH1955_4_bianchi_residual_constraint",
            "Diffeomorphism invariance forces any extra residual to be covariantly conserved; this restricts but does not kill l=2 by itself.",
            "nabla^i R_ij^extra=0; P_2[R_ij^extra] can still exist as a homogeneous/tidal mode",
            "CONSERVATION_CONSTRAINT_DERIVED_NONZERO",
            "Bianchi helps but is not magic pixie dust; boundary data still matter.",
            "combine with boundary uniqueness or finite envelope",
        ),
        (
            "EH1955_5_no_extra_boundary_dof",
            "Residual l=2 boundary data vanish if the extra local branch has decaying/regular boundary conditions and no independent boundary symplectic flux.",
            "Delta h_boundary2^MTS=0 if delta B_extra|l=2=0 and Omega_boundary_extra|l=2=0",
            "CONDITION_SHARPENED_NOT_SIGNED",
            "This is the boundary half of local GR recovery.",
            "need parent boundary term and symplectic-flux certificate",
        ),
        (
            "EH1955_6_zero_verdict",
            "The same-source zero theorem is not closed at 1955.",
            "Delta B_2^MTS=0 is blocked by unsigned source-map, extra-source-silence, and boundary-uniqueness clauses",
            "ZERO_PROOF_FAILED_CLEANLY",
            "Still forward: the required parent contract is now explicit enough to attack.",
            "build parent action signature or residual-bound fallback",
        ),
    ]
    rows: list[dict[str, object]] = []
    for row_id, statement, math_form, status, implication, required_fix in entries:
        row = base(row_id)
        row.update(
            {
                "statement": statement,
                "math_form": math_form,
                "status": status,
                "implication": implication,
                "required_fix": required_fix,
            }
        )
        rows.append(row)
    return rows


def residual_bound_rows() -> list[dict[str, object]]:
    entries = [
        (
            "RB1955_0_residual_bound_formula",
            "abs(S_TF_extra)",
            "||W_STF||_1 (||K_2|| ||Delta J_2^MTS|| + ||K_2^X|| ||P_2 R_extra|| + ||H_2|| ||Delta h_boundary2^MTS||)",
            "MISSING_FACTORS",
            "dimensionless",
            "This is the fallback if the same-source theorem cannot be signed.",
        ),
        (
            "RB1955_1_source_map_delta",
            "||Delta J_2^MTS||",
            "norm of extra ordinary-matter l=2 source-map difference after GR subtraction",
            "MISSING",
            "source-current units",
            "need same-source proof or conservative source-map mismatch envelope",
        ),
        (
            "RB1955_2_extra_residual_l2",
            "||P_2 R_extra||",
            "norm of extra-sector l=2 metric residual after local on-shell reduction",
            "MISSING",
            "metric-equation units",
            "need source-silence proof or extra-sector l=2 envelope",
        ),
        (
            "RB1955_3_boundary_delta",
            "||Delta h_boundary2^MTS||",
            "extra l=2 boundary data after GR matching subtraction",
            "MISSING",
            "boundary data units",
            "need no-extra-boundary proof or matching envelope",
        ),
        (
            "RB1955_4_readout_norm",
            "||W_STF||_1",
            "Cassini residual STF readout norm",
            "MISSING",
            "inverse profile units",
            "source after residual envelopes exist",
        ),
    ]
    rows: list[dict[str, object]] = []
    for row_id, symbol, definition, status, units, next_action in entries:
        row = base(row_id)
        row.update(
            {
                "symbol": symbol,
                "definition": definition,
                "status": status,
                "units": units,
                "next_action": next_action,
            }
        )
        rows.append(row)
    return rows


def runner_rows() -> list[dict[str, object]]:
    entries = [
        (
            "RUN1955_0_theorem_contract",
            "same-source map + extra source silence + no extra boundary l=2 -> Delta B_2^MTS=0",
            "S_TF_extra=0",
            "MISSING_PARENT_SOURCE_MAP;MISSING_EXTRA_SOURCE_SILENCE;MISSING_BOUNDARY_UNIQUENESS",
            "BLOCKED_ZERO_THEOREM_NOT_CLOSED",
            "contract exists but cannot claim Cassini pass",
        ),
        (
            "RUN1955_1_bianchi_only",
            "nabla^i R_ij^extra=0",
            "insufficient by itself",
            "MISSING_BOUNDARY_DATA;MISSING_RESIDUAL_AMPLITUDE",
            "PASS_NONCLAIM_CONSTRAINT_ONLY",
            "conservation is a restriction, not a zero proof",
        ),
        (
            "RUN1955_2_residual_bound",
            "abs(S_TF_extra) <= ||W_STF||_1 residual envelopes",
            "<= 6.7e-5",
            "MISSING_RESIDUAL_ENVELOPES;MISSING_W_STF",
            "BLOCKED_MISSING_BOUND_FACTORS",
            "fallback bound not scoreable yet",
        ),
    ]
    rows: list[dict[str, object]] = []
    for row_id, prediction, acceptance_rule, missing_inputs, runner_status, consequence in entries:
        row = base(row_id)
        row.update(
            {
                "prediction": prediction,
                "acceptance_rule": acceptance_rule,
                "missing_inputs": missing_inputs,
                "runner_status": runner_status,
                "consequence": consequence,
            }
        )
        rows.append(row)
    return rows


def claim_gate_rows() -> list[dict[str, object]]:
    entries = [
        (
            "CG1955_0_theorem_contract",
            "Exact EH same-source/no-extra-boundary theorem contract exists.",
            "PASS_NONCLAIM",
            "contract is explicit but unsigned",
        ),
        (
            "CG1955_1_bianchi_constraint",
            "Extra residual is constrained by conservation.",
            "PASS_NONCLAIM",
            "constraint alone does not kill l=2",
        ),
        (
            "CG1955_2_same_source_map",
            "Parent proves same source map as EH/GR.",
            "FAIL_BLOCKED",
            "parent variation/normalization proof missing",
        ),
        (
            "CG1955_3_extra_source_silence",
            "Parent proves extra-sector source silence/common-mode locally.",
            "FAIL_BLOCKED",
            "on-shell vertical/descent proof missing",
        ),
        (
            "CG1955_4_no_extra_boundary",
            "Parent proves no independent residual l=2 boundary data.",
            "FAIL_BLOCKED",
            "boundary uniqueness/symplectic flux proof missing",
        ),
        (
            "CG1955_5_Cassini_pass",
            "MTS passes Cassini gamma residual gate.",
            "FAIL_BLOCKED",
            "zero theorem and finite residual bound both missing",
        ),
        (
            "CG1955_6_local_GR",
            "MTS derives local GR/Newton.",
            "FAIL_BLOCKED",
            "Cassini residual and Newtonian common-mode gates remain open",
        ),
    ]
    rows: list[dict[str, object]] = []
    for row_id, claim, status, reason in entries:
        row = base(row_id)
        row.update({"claim": claim, "status": status, "reason": reason})
        rows.append(row)
    return rows


def decision_rows() -> list[dict[str, object]]:
    entries = [
        (
            "DEC1955_0_progress",
            "EH_SAME_SOURCE_CONTRACT_EXACT_BUT_UNSIGNED",
            "the derivation target is now a parent action/variation signature, not empirical curve fitting",
            "attempt to sign the local parent action clauses: EH normalization, universal matter coupling, extra-sector silence, boundary flux zero",
        ),
        (
            "DEC1955_1_best_next",
            "PARENT_ACTION_VARIATION_SIGNATURE",
            "without the parent variation signature, residual l=2 remains an input rather than a theorem",
            "build a parent action signature ledger and identify which clauses are already present vs closure assumptions",
        ),
    ]
    rows: list[dict[str, object]] = []
    for row_id, decision, reason, next_action in entries:
        row = base(row_id)
        row.update({"decision": decision, "reason": reason, "next_action": next_action})
        rows.append(row)
    return rows


def next_rows() -> list[dict[str, object]]:
    row = base("NEXT1955_0_primary")
    row.update(
        {
            "priority": "selected",
            "target_doc": "1956-Y5-R2FR-parent-action-variation-signature-for-local-EH-map.md",
            "target_script": "scripts/Y5_R2FR_parent_action_variation_signature_for_local_EH_map_1956.py",
            "objective": "audit/sign the parent action variation clauses needed for local EH same-source recovery",
            "acceptance_output": "EH normalization, matter coupling, extra-sector silence, boundary flux rows marked signed/unsigned with source paths",
            "nonclaim_rule": "no Cassini/local-GR claim unless all local EH source-map clauses are signed or residual bound is numeric",
        }
    )
    return [row]


def snapshot_rows() -> list[dict[str, object]]:
    row = base("SNAP1955_0_project_position")
    row.update(
        {
            "strongest_result": "Residual l=2 zero is reduced to an exact local EH same-source/no-extra-boundary theorem contract.",
            "what_improved": "Bianchi/conservation is included without overclaiming it as a zero proof",
            "still_missing": "parent variation signature for EH normalization, matter source map, extra-sector source silence, and boundary flux zero",
            "claim_status": "not a Cassini/local-GR pass; the next target is parent-action signing",
        }
    )
    return [row]


OUTPUTS = {
    "source_register": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1955_SOURCE_REGISTER.csv",
    "theorem_contract": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1955_EH_SAME_SOURCE_THEOREM_CONTRACT.csv",
    "residual_bound": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1955_RESIDUAL_L2_BOUND_LEDGER.csv",
    "runner": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1955_RUNNER_UPDATE.csv",
    "claim_gate": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1955_CLAIM_GATE.csv",
    "decision": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1955_DECISION_LEDGER.csv",
    "next": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1955_NEXT_TARGET.csv",
    "snapshot": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1955_PROJECT_STATUS_SNAPSHOT.csv",
    "source_weight": SOURCE_WEIGHT_DOCS / "EH_SAME_SOURCE_CONTRACT_1955_NONCLAIM.csv",
    "queue": RAB_QUEUE / "JR1955_PARENT_ACTION_VARIATION_SIGNATURE_QUEUE.csv",
}


def build_tables() -> dict[str, list[dict[str, object]]]:
    source_weight = [
        {
            **base("SW1955_0_nonclaim_weight"),
            "artifact": "1955 EH same-source theorem contract",
            "weight": "THEOREM_CONTRACT_NOT_EVIDENCE",
            "reason": "contract sharpens local GR reduction but parent clauses remain unsigned",
        }
    ]
    queue = [
        {
            **base("AQ1955_0_EH_normalization"),
            "target": "EH normalization and observed metric identity",
            "needed_inputs": "parent action local metric sector; coefficient of R; observed metric/coframe map",
            "priority": "HIGH",
        },
        {
            **base("AQ1955_1_matter_coupling"),
            "target": "universal ordinary matter source map",
            "needed_inputs": "matter action descent; T_matter normalization; no species/source-label leakage",
            "priority": "HIGH",
        },
        {
            **base("AQ1955_2_extra_boundary"),
            "target": "extra-sector source silence and boundary flux zero",
            "needed_inputs": "extra field equations; vertical quotient map; boundary/symplectic flux",
            "priority": "HIGH",
        },
    ]
    return {
        "source_register": source_register(),
        "theorem_contract": theorem_contract_rows(),
        "residual_bound": residual_bound_rows(),
        "runner": runner_rows(),
        "claim_gate": claim_gate_rows(),
        "decision": decision_rows(),
        "next": next_rows(),
        "snapshot": snapshot_rows(),
        "source_weight": source_weight,
        "queue": queue,
    }


def validation_row(validation_id: str, status: str, detail: str) -> dict[str, object]:
    return {
        "validation_id": validation_id,
        "status": status,
        "detail": detail,
        "valid_for_claim": False,
        "public_claim": False,
    }


def formalization_hits() -> int:
    if not FORMALIZATION.exists():
        return 0
    patterns = ("1955-", "*_1955_*", "*Y5*1955*", "*VAL1955*", "*P8*1955*")
    return sum(1 for path in FORMALIZATION.rglob("*") if any(Path(path.name).match(pattern) for pattern in patterns))


def validate(tables: dict[str, list[dict[str, object]]]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    sources_ok = all(row["status"] == "EXISTS_NEEDLES_CONFIRMED" for row in tables["source_register"])
    rows.append(validation_row("VAL1955_00_sources", "PASS" if sources_ok else "FAIL", "all source files exist and needles found"))

    contract_ok = any(row["row_id"] == "EH1955_0_target" and row["status"] == "THEOREM_TARGET_EXACT" for row in tables["theorem_contract"])
    rows.append(validation_row("VAL1955_01_contract", "PASS" if contract_ok else "FAIL", "same-source theorem target exact"))

    split_ok = any(row["row_id"] == "EH1955_1_variation_split" and row["status"] == "DECOMPOSITION_BUILT" for row in tables["theorem_contract"])
    rows.append(validation_row("VAL1955_02_variation_split", "PASS" if split_ok else "FAIL", "parent variation split recorded"))

    bianchi_ok = any(row["row_id"] == "EH1955_4_bianchi_residual_constraint" and row["status"] == "CONSERVATION_CONSTRAINT_DERIVED_NONZERO" for row in tables["theorem_contract"])
    rows.append(validation_row("VAL1955_03_bianchi", "PASS" if bianchi_ok else "FAIL", "Bianchi constraint retained without overclaim"))

    verdict_ok = any(row["row_id"] == "EH1955_6_zero_verdict" and row["status"] == "ZERO_PROOF_FAILED_CLEANLY" for row in tables["theorem_contract"])
    rows.append(validation_row("VAL1955_04_zero_verdict", "PASS" if verdict_ok else "FAIL", "zero proof failure recorded cleanly"))

    bound_ok = any(row["row_id"] == "RB1955_0_residual_bound_formula" and row["status"] == "MISSING_FACTORS" for row in tables["residual_bound"])
    rows.append(validation_row("VAL1955_05_bound_formula", "PASS" if bound_ok else "FAIL", "residual bound formula recorded but blocked"))

    runner_statuses = {row["runner_status"] for row in tables["runner"]}
    runner_ok = {"BLOCKED_ZERO_THEOREM_NOT_CLOSED", "PASS_NONCLAIM_CONSTRAINT_ONLY", "BLOCKED_MISSING_BOUND_FACTORS"}.issubset(runner_statuses)
    rows.append(validation_row("VAL1955_06_runner", "PASS" if runner_ok else "FAIL", "runner blocks claim branches and keeps Bianchi nonclaim"))

    gate_ok = all(row["status"] != "PASS_CLAIM" for row in tables["claim_gate"]) and any(
        row["row_id"] == "CG1955_0_theorem_contract" and row["status"] == "PASS_NONCLAIM" for row in tables["claim_gate"]
    )
    rows.append(validation_row("VAL1955_07_claim_gates", "PASS" if gate_ok else "FAIL", "only nonclaim contract gates pass"))

    decision_ok = any(row["decision"] == "PARENT_ACTION_VARIATION_SIGNATURE" for row in tables["decision"])
    rows.append(validation_row("VAL1955_08_decision", "PASS" if decision_ok else "FAIL", "parent action variation signature selected"))

    next_ok = tables["next"][0]["target_doc"] == "1956-Y5-R2FR-parent-action-variation-signature-for-local-EH-map.md"
    rows.append(validation_row("VAL1955_09_next_target", "PASS" if next_ok else "FAIL", "1956 target selected"))

    flags_ok = all(not bool(row.get("valid_for_claim")) and not bool(row.get("public_claim")) for table in tables.values() for row in table)
    rows.append(validation_row("VAL1955_10_claim_flags_safe", "PASS" if flags_ok else "FAIL", "claim flags all false"))

    csv_ok = all(bool(read_csv(path)) for path in OUTPUTS.values())
    rows.append(validation_row("VAL1955_11_csv_parse", "PASS" if csv_ok else "FAIL", "all generated CSVs parse with rows"))

    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)
    rows.append(validation_row("VAL1955_12_pycache_absent", "PASS" if not pycache.exists() else "FAIL", "scripts __pycache__ absent"))

    count = formalization_hits()
    rows.append(validation_row("VAL1955_13_formalization_untouched", "PASS" if count == 0 else "FAIL", f"formalization_1955_artifact_count={count}"))

    overall = "PASS" if all(row["status"] == "PASS" for row in rows) else "FAIL"
    rows.append(validation_row("VAL1955_OVERALL", overall, "1955 local EH same-source map or residual l2 bound"))
    return rows


def markdown_table(rows: list[dict[str, object]]) -> str:
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    lines = ["| " + " | ".join(fields) + " |", "| " + " | ".join("---" for _ in fields) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(field, "")).replace("\n", " ") for field in fields) + " |")
    return "\n".join(lines)


def write_markdown(tables: dict[str, list[dict[str, object]]], validation_rows: list[dict[str, object]]) -> None:
    sections = [
        ("Source Register", tables["source_register"]),
        ("EH Same-Source Theorem Contract", tables["theorem_contract"]),
        ("Residual L2 Bound Ledger", tables["residual_bound"]),
        ("Runner Update", tables["runner"]),
        ("Claim Gate", tables["claim_gate"]),
        ("Decision Ledger", tables["decision"]),
        ("Next Target", tables["next"]),
        ("Project Status Snapshot", tables["snapshot"]),
        ("Validation", validation_rows),
    ]
    lines = [
        "# 1955 Y5 R2FR: Local EH Same-Source Map Or Residual L2 Bound",
        "",
        "Private checkpoint. This attempts to bridge MTS to local GR by turning inherited l=2 residuals into a parent-action source-map theorem.",
        "",
        "Verdict: the exact theorem contract is now explicit. Residual l=2 vanishes if the parent local variation has the same EH matter source map, extra-sector source silence/common-mode behaviour, and no independent extra l=2 boundary data. Those clauses are not parent-signed here, so no Cassini/local-GR claim is made.",
        "",
    ]
    for title, rows in sections:
        lines.extend([f"## {title}", "", markdown_table(rows), ""])
    DOC_PATH.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    ensure_dirs()
    tables = build_tables()
    for name, path in OUTPUTS.items():
        write_csv(path, tables[name])
    validation_rows = validate(tables)
    write_csv(VALIDATION_PATH, validation_rows)
    write_markdown(tables, validation_rows)
    overall = validation_rows[-1]["status"]
    print(f"wrote {DOC_PATH}")
    print(f"wrote {VALIDATION_PATH}")
    print(f"VAL1955_OVERALL={overall}")
    return 0 if overall == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
