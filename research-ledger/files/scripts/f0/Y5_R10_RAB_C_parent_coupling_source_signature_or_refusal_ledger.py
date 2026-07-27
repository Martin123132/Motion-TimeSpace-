from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


STARTED = datetime.now(timezone.utc)
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
BRANCH_ROOT = ROOT / "source-intake" / "microscope" / "branch_locked_wep"
FORMALIZATION = ROOT.parent / "formalization-workbench"

DOC = ROOT / "1430-Y5-R10-RAB-C-parent-coupling-source-signature-or-refusal-ledger.md"
BRANCH_ID_FILE = BRANCH_ROOT / "branch_id.csv"
C_PARENT_FILE = BRANCH_ROOT / "coefficients" / "C_parent.csv"

SOURCE_REGISTER = OUT / "P8_Y5_R10_1430_SOURCE_REGISTER.csv"
COUPLING_SOURCE_HUNT = OUT / "P8_Y5_R10_1430_COUPLING_SOURCE_HUNT.csv"
C_PARENT_SIGNATURE_CONTRACT = OUT / "P8_Y5_R10_1430_C_PARENT_SIGNATURE_CONTRACT.csv"
C_PARENT_ROWS = OUT / "P8_Y5_R10_1430_C_PARENT_PLACEHOLDER_ROWS.csv"
BRANCH_MATCH_AUDIT = OUT / "P8_Y5_R10_1430_BRANCH_MATCH_AUDIT.csv"
RUNNER_REFUSAL = OUT / "P8_Y5_R10_1430_RUNNER_REFUSAL_STATUS.csv"
CLAIM_GATE = OUT / "P8_Y5_R10_1430_CLAIM_GATE.csv"
DECISION_LEDGER = OUT / "P8_Y5_R10_1430_DECISION_LEDGER.csv"
NEXT_TARGET = OUT / "P8_Y5_R10_1430_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1430_VALIDATION.csv"


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def clean(value: Any) -> str:
    return str(value).replace("\n", " ").replace("\r", " ").strip()


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"no rows supplied for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: clean(row.get(key, "")) for key in fieldnames})


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def text_has(path: Path, needle: str) -> bool:
    if not path.exists():
        return False
    return needle in path.read_text(encoding="utf-8", errors="ignore")


def md_cell(value: Any) -> str:
    return clean(value).replace("|", "\\|")


def md_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "_No rows._"
    headers = list(rows[0].keys())
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(["---"] * len(headers)) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(md_cell(row.get(header, "")) for header in headers) + " |")
    return "\n".join(lines)


def count_formalization_modified_since_start() -> int:
    if not FORMALIZATION.exists():
        return 0
    return sum(
        1
        for path in FORMALIZATION.rglob("*")
        if path.is_file() and datetime.fromtimestamp(path.stat().st_mtime, timezone.utc) >= STARTED
    )


def remove_pycache() -> None:
    pycache = Path(__file__).resolve().parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def branch_id() -> str:
    rows = read_csv(BRANCH_ID_FILE)
    if len(rows) != 1:
        raise ValueError(f"expected one branch row, got {len(rows)}")
    value = rows[0].get("same_parent_branch_id", "").strip()
    if not value:
        raise ValueError("same_parent_branch_id missing")
    return value


def source_register_rows(branch: str) -> list[dict[str, Any]]:
    specs = [
        ("SRC1430_0_1429_next", OUT / "P8_Y5_R10_1429_NEXT_TARGET.csv", "NEXT1429_0_1430", "1429 handoff selecting C_parent coupling source signature."),
        ("SRC1430_1_1429_validation", OUT / "P8_Y5_BRR545_1429_VALIDATION.csv", "VAL1429_8_overall", "1429 validation summary."),
        ("SRC1430_2_branch_id", BRANCH_ID_FILE, branch, "branch lock row."),
        ("SRC1430_3_1426_pack", OUT / "P8_Y5_R10_1426_FINITE_WEP_COEFFICIENT_INPUT_PACK.csv", "PACK1426_0_C_parent", "C_parent recorded as missing parent coefficient."),
        ("SRC1430_4_1082_DD_map", OUT / "P8_Y5_R10_1082_PARENT_TO_DD_COEFFICIENT_MAP_ATTEMPT.csv", "PTD1082_4_verdict", "parent-to-DD coefficient map not derived."),
        ("SRC1430_5_872_ownership", OUT / "P8_Y5_R10_872_COEFFICIENT_OWNERSHIP_LEDGER.csv", "CO872_2_Q_T_over_m", "trace coupling ownership ledger."),
        ("SRC1430_6_873_zero_theorem", OUT / "P8_Y5_R10_873_LOCAL_TRACE_CHARGE_ZERO_THEOREM.csv", "QTZ873_3_verdict", "chain-rule zero theorem remains conditional."),
        ("SRC1430_7_876_quadratic_contract", OUT / "P8_Y5_R10_876_TRACE_SECTOR_QUADRATIC_CONTRACT.csv", "QTC876_5_claim_rule", "claim rule for parent Hessian/zero-return route."),
        ("SRC1430_8_877_source_hunt", OUT / "P8_Y5_R10_877_HESSIAN_SOURCE_CANDIDATES.csv", "HC877_8_verdict", "trace Hessian source hunt verdict."),
        ("SRC1430_9_879_pairing", OUT / "P8_Y5_R10_879_PAIRING_SOURCE_AUDIT.csv", "KP879_4_pairing_verdict", "parent pairing/Hessian ownership missing."),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, path, anchor, role in specs:
        rows.append(
            {
                "source_id": source_id,
                "source_path": str(path),
                "path_exists": path.exists(),
                "anchor": anchor,
                "anchor_found": text_has(path, anchor),
                "role": role,
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def coupling_source_hunt_rows() -> list[dict[str, Any]]:
    return [
        {
            "hunt_id": "HUNT1430_0_1426_pack",
            "candidate": "C_parent coefficient/operator map",
            "source_anchor": "PACK1426_0_C_parent",
            "what_it_supplies": "exact WEP scorepack slot for parent coupling",
            "status": "MISSING_PARENT_COEFFICIENT",
            "gap": "no branch-locked component values, units, signs, or parent action source",
            "usable_for_score": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "hunt_id": "HUNT1430_1_DD_map",
            "candidate": "C_parent to Damour-Donoghue alpha/surface channels",
            "source_anchor": "PTD1082_4_verdict",
            "what_it_supplies": "external comparator basis if a signed pullback exists",
            "status": "PARENT_TO_DD_MAP_NOT_DERIVED",
            "gap": "DD remains comparator/proxy; not MTS ontology",
            "usable_for_score": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "hunt_id": "HUNT1430_2_trace_charge_zero",
            "candidate": "Q_T^A/m_A zero theorem",
            "source_anchor": "QTZ873_1_chain_rule_zero;QTZ873_3_verdict",
            "what_it_supplies": "would kill direct trace contribution to R10/WEP/clocks without a tiny fitted coupling",
            "status": "CONDITIONAL_THEOREM_PREMISES_UNSIGNED",
            "gap": "q_loc verticality, matter-stack descent, and no-marker constant-sector clauses are not parent signed",
            "usable_for_score": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "hunt_id": "HUNT1430_3_trace_Hessian",
            "candidate": "H_T=P_tr^dagger Hess(S_parent)P_tr",
            "source_anchor": "QTC876_1_Hessian_operator;HC877_8_verdict",
            "what_it_supplies": "would own Z_T, m_T/lambda_T, and trace source projection",
            "status": "FORMAL_CONTRACT_WRITTEN_PARENT_OPERATOR_MISSING",
            "gap": "no parent-owned P_tr/H_tr/principal symbol/mass/source projection block found",
            "usable_for_score": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "hunt_id": "HUNT1430_4_pairing",
            "candidate": "K_parent or charge/Hessian pairing",
            "source_anchor": "KP879_4_pairing_verdict",
            "what_it_supplies": "would define the coupling norm/sign basis",
            "status": "PAIRING_NOT_COMPUTABLE",
            "gap": "no parent charge metric, kinetic Hessian, symplectic inverse, or constrained pseudo-inverse is signed",
            "usable_for_score": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "hunt_id": "HUNT1430_5_verdict",
            "candidate": "branch-locked C_parent",
            "source_anchor": "all hunt rows",
            "what_it_supplies": "finite WEP coupling vector",
            "status": "NOT_DERIVED_NOT_SOURCED_PLACEHOLDER_ONLY",
            "gap": "C_parent.csv may be written as a refusal/manifest row only",
            "usable_for_score": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def c_parent_signature_contract_rows(branch: str) -> list[dict[str, Any]]:
    return [
        {
            "contract_id": "CPC1430_0_product_law",
            "same_parent_branch_id": branch,
            "required_signature": "delta_eta_AB = orbit_average[K_CMSM * R_source^i * C_parent_i_j * (R_A^j - R_B^j)] with all indices, units, and signs in one branch",
            "acceptance_test": "every factor must be numeric-or-derived-zero, source-backed, unit-declared, and branch-matched",
            "current_status": "SIGNATURE_WRITTEN_COMPONENTS_MISSING",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "contract_id": "CPC1430_1_zero_branch",
            "same_parent_branch_id": branch,
            "required_signature": "C_parent_i_j=0 for local ordinary matter if q_loc verticality plus matter-stack/no-marker descent proves Q_T^A=0 and source-response silence",
            "acceptance_test": "873 zero-theorem premises and 876 zero-return clauses must all be parent signed",
            "current_status": "ZERO_BRANCH_CONDITIONAL_NOT_PARENT_SIGNED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "contract_id": "CPC1430_2_numeric_branch",
            "same_parent_branch_id": branch,
            "required_signature": "C_parent component rows provide finite numeric values/bounds with units, sign convention, parent_status, and source_path",
            "acceptance_test": "no MISSING/PENDING/PLACEHOLDER values and no DD-only ontology substitution",
            "current_status": "NUMERIC_BRANCH_NO_SOURCE",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "contract_id": "CPC1430_3_claim_rule",
            "same_parent_branch_id": branch,
            "required_signature": "finite WEP runner remains blocked unless CPC1430_1 or CPC1430_2 passes together with source/readout/material rows",
            "acceptance_test": "claim_allowed can become true only after branch/product/G guard/C_parent/source/material/readout all pass",
            "current_status": "RUNNER_BLOCKED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def c_parent_rows(branch: str) -> list[dict[str, Any]]:
    common = {
        "same_parent_branch_id": branch,
        "uncertainty": "MISSING",
        "sign_convention": "PENDING_PARENT_BASIS",
        "basis": "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428",
        "source_path": str(DOC),
        "valid_for_claim": False,
        "claim_allowed": False,
    }
    rows = [
        {
            "coefficient_id": "CP1430_0_trace_charge",
            "component": "Q_T_over_m_or_local_trace_charge",
            "value": "MISSING_ZERO_THEOREM_OR_NUMERIC_SOURCE",
            "units": "PENDING_TRACE_CHARGE_NORMALIZATION",
            "parent_status": "CONDITIONAL_ZERO_THEOREM_PREMISES_UNSIGNED",
            "blocks": "direct R10/WEP/clock trace coupling",
        },
        {
            "coefficient_id": "CP1430_1_metric_response",
            "component": "C_T_metric",
            "value": "MISSING_OBSERVED_METRIC_RESPONSE",
            "units": "PENDING_METRIC_POTENTIAL_NORMALIZATION",
            "parent_status": "MISSING_OBSERVED_METRIC_COFAME_MAP",
            "blocks": "PPN metric response and local-GR reduction",
        },
        {
            "coefficient_id": "CP1430_2_source_response",
            "component": "C_T_source",
            "value": "MISSING_SOURCE_NORMALIZATION_RESPONSE",
            "units": "PENDING_SOURCE_GM_NORMALIZATION",
            "parent_status": "CONDITIONAL_393_ONLY_NOT_PARENT_SIGNED",
            "blocks": "Newtonian source normalization and measured-G guard closure",
        },
        {
            "coefficient_id": "CP1430_3_trace_Hessian_norm",
            "component": "Z_T_and_mass_gap",
            "value": "MISSING_PARENT_HESSIAN",
            "units": "PENDING_HESSIAN_UNITS",
            "parent_status": "H_T_CONTRACT_ONLY_OPERATOR_NOT_EXTRACTED",
            "blocks": "R10 range/coupling normalization",
        },
        {
            "coefficient_id": "CP1430_4_DD_alpha_pullback",
            "component": "DD_Q_alpha_Coulomb_pullback",
            "value": "MISSING_PARENT_PULLBACK",
            "units": "PENDING_DD_TO_MTS_UNITS",
            "parent_status": "EXTERNAL_COMPARATOR_ONLY",
            "blocks": "DD alpha channel cannot be used as MTS coefficient",
        },
        {
            "coefficient_id": "CP1430_5_DD_surface_pullback",
            "component": "DD_Q_surface_binding_pullback",
            "value": "MISSING_PARENT_PULLBACK",
            "units": "PENDING_DD_TO_MTS_UNITS",
            "parent_status": "EXTERNAL_COMPARATOR_ONLY",
            "blocks": "DD surface channel cannot be used as MTS coefficient",
        },
        {
            "coefficient_id": "CP1430_6_verdict",
            "component": "C_parent_vector",
            "value": "NOT_SCOREABLE",
            "units": "NOT_CLAIM_UNITS",
            "parent_status": "PLACEHOLDER_ROWS_ONLY_RUNNER_BLOCKED",
            "blocks": "finite WEP score remains refused",
        },
    ]
    return [{**row, **common} for row in rows]


def write_c_parent_file(rows: list[dict[str, Any]]) -> None:
    write_csv(C_PARENT_FILE, rows)


def branch_match_audit_rows(branch: str) -> list[dict[str, Any]]:
    targets = [
        ("BMA1430_0_branch_id", BRANCH_ID_FILE),
        ("BMA1430_1_C_parent", C_PARENT_FILE),
    ]
    rows: list[dict[str, Any]] = []
    for audit_id, path in targets:
        parsed = read_csv(path) if path.exists() else []
        values = sorted({row.get("same_parent_branch_id", "") for row in parsed})
        rows.append(
            {
                "audit_id": audit_id,
                "target_path": str(path),
                "file_exists": path.exists(),
                "row_count": len(parsed),
                "branch_values": ";".join(values),
                "result": "PASS" if path.exists() and values == [branch] else "FAIL",
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def runner_refusal_rows() -> list[dict[str, Any]]:
    return [
        {
            "runner_id": "RUN1430_0_C_parent",
            "target": "branch-locked finite WEP product",
            "input_status": "C_PARENT_FILE_EXISTS_PLACEHOLDER_ONLY",
            "runner_status": "REFUSE_SCORE_UNTIL_C_PARENT_NUMERIC_OR_ZERO_THEOREM",
            "score_ready": False,
            "reason": "C_parent rows carry MISSING/PENDING/PLACEHOLDER statuses and no parent-derived zero theorem",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "runner_id": "RUN1430_1_DD_comparator",
            "target": "DD alpha/surface comparator branch",
            "input_status": "PARENT_TO_DD_MAP_NOT_DERIVED",
            "runner_status": "REFUSE_DD_AS_MTS_ONTOLOGY",
            "score_ready": False,
            "reason": "DD channels can remain external comparators only until parent pullbacks are signed",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "runner_id": "RUN1430_2_zero_theorem",
            "target": "local trace charge zero theorem",
            "input_status": "CHAIN_RULE_VALID_PREMISES_UNSIGNED",
            "runner_status": "REFUSE_ZERO_PROMOTION",
            "score_ready": False,
            "reason": "q_loc verticality, matter-stack descent, and no-marker clauses are not all parent signed",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "CG1430_0_C_parent_file",
            "claim_component": "C_parent coefficient file",
            "gate_pass": True,
            "claim_allowed": False,
            "reason": "file exists and branch matches, but rows are placeholders/refusals",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG1430_1_C_parent_numeric",
            "claim_component": "numeric/source-backed coupling vector",
            "gate_pass": False,
            "claim_allowed": False,
            "reason": "no numeric/source-backed parent components with units/signs",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG1430_2_C_parent_zero",
            "claim_component": "zero-coupling theorem",
            "gate_pass": False,
            "claim_allowed": False,
            "reason": "873 chain rule is conditional; parent premises unsigned",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG1430_3_finite_WEP",
            "claim_component": "finite WEP prediction",
            "gate_pass": False,
            "claim_allowed": False,
            "reason": "C_parent/source/material/readout are not claim-ready",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG1430_4_local_GR",
            "claim_component": "local-GR/Newton reduction",
            "gate_pass": False,
            "claim_allowed": False,
            "reason": "coupling bottleneck remains open",
            "valid_for_claim": False,
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC1430_0_no_fake_coupling",
            "decision": "write C_parent.csv as branch-locked placeholder/refusal rows only",
            "because": "existing ledgers do not derive or source the coupling vector",
            "effect": "future runners can inspect C_parent.csv and refuse scoring instead of silently inventing coefficients",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1430_1_derivation_route",
            "decision": "prefer the Q_T zero theorem route over fitted coefficients",
            "because": "a parent-signed local verticality/no-marker proof would kill a whole family of local couplings cleanly",
            "effect": "next work should attack q_loc verticality and matter-stack descent again, but with explicit C_parent promotion tests",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1430_2_numeric_fallback",
            "decision": "allow numeric/source fallback only if parent status, units, signs, and branch matching are real",
            "because": "DD or unit-kernel proxies are useful pressure tests but not MTS coefficients",
            "effect": "finite WEP stays blocked until the coupling is either theorem-zero or sourced",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT1430_0_1431",
            "next_target": "1431-Y5-R10-RAB-QT-zero-premise-closure-or-C-parent-source-import-schema.md",
            "script": "scripts/Y5_R10_RAB_QT_zero_premise_closure_or_C_parent_source_import_schema.py",
            "objective": "try to close the Q_T/m zero theorem premises for C_parent, or build the strict import schema for a real sourced coupling vector.",
            "include": "q_loc verticality; matter-stack descent; no-marker constants; parent-status promotion tests; C_parent import schema; branch-id audit",
            "exclude": "numeric WEP score; DD-as-MTS ontology; fitted free coupling; local-GR claim; measured-G absorption; formalization edits; GitHub",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def validation_rows(
    sources: list[dict[str, Any]],
    c_parent: list[dict[str, Any]],
    branch_audit: list[dict[str, Any]],
    claims: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    csvs = [
        SOURCE_REGISTER,
        COUPLING_SOURCE_HUNT,
        C_PARENT_SIGNATURE_CONTRACT,
        C_PARENT_ROWS,
        BRANCH_MATCH_AUDIT,
        RUNNER_REFUSAL,
        CLAIM_GATE,
        DECISION_LEDGER,
        NEXT_TARGET,
        C_PARENT_FILE,
    ]
    parse_ok = True
    parse_errors: list[str] = []
    truthy_claim_flags: list[str] = []
    missing_or_pending_seen = False
    for path in csvs:
        try:
            rows = read_csv(path)
        except Exception as exc:
            parse_ok = False
            parse_errors.append(f"{path.name}:{type(exc).__name__}")
            continue
        for index, row in enumerate(rows, start=2):
            row_text = " ".join(row.values())
            if any(marker in row_text for marker in ("MISSING", "PENDING", "PLACEHOLDER", "NOT_SCOREABLE")):
                missing_or_pending_seen = True
            for key in ("claim_allowed", "valid_for_claim", "valid_prediction_row", "adopted_as_derivation"):
                if (row.get(key) or "").strip().lower() == "true":
                    truthy_claim_flags.append(f"{path.name}:{index}:{key}=true")
    branch_match_ok = all(row["result"] == "PASS" for row in branch_audit)
    c_parent_written = C_PARENT_FILE.exists() and len(read_csv(C_PARENT_FILE)) == len(c_parent)
    c_parent_nonclaim = all(str(row.get("claim_allowed")).lower() == "false" for row in c_parent)
    claims_safe = all(str(row.get("claim_allowed")).lower() == "false" for row in claims) and not truthy_claim_flags
    formalization_count = count_formalization_modified_since_start()
    checks = [
        ("VAL1430_0_sources", all(row["path_exists"] and row["anchor_found"] for row in sources), "all 1430 cited source paths and anchors resolve"),
        ("VAL1430_1_C_parent_file", c_parent_written, "branch-locked C_parent.csv written"),
        ("VAL1430_2_branch_match", branch_match_ok, "C_parent.csv shares branch_id with branch_id.csv"),
        ("VAL1430_3_placeholder_block", missing_or_pending_seen and c_parent_nonclaim, "C_parent rows visibly remain MISSING/PENDING/PLACEHOLDER and nonclaim"),
        ("VAL1430_4_claim_gates", claims_safe, "all claim/valid/adopted flags remain false"),
        ("VAL1430_5_csv_parse", parse_ok, "all generated 1430 CSVs parse cleanly" if parse_ok else ";".join(parse_errors)),
        ("VAL1430_6_formalization_untouched", formalization_count == 0, f"formalization modified-file count since start={formalization_count}"),
        ("VAL1430_7_next_target", True, "1431 handoff written"),
    ]
    rows = [
        {
            "check_id": check_id,
            "result": "PASS" if passed else "FAIL",
            "detail": detail,
            "generated_utc": stamp(),
        }
        for check_id, passed, detail in checks
    ]
    rows.append(
        {
            "check_id": "VAL1430_8_overall",
            "result": "PASS" if all(row["result"] == "PASS" for row in rows) else "FAIL",
            "detail": "1430 writes a branch-locked C_parent refusal file and keeps finite WEP/local-GR claims blocked",
            "generated_utc": stamp(),
        }
    )
    return rows


def write_doc(sections: dict[str, list[dict[str, Any]]]) -> None:
    content = "\n\n".join(
        [
            "# 1430 - C_parent coupling source signature or refusal ledger",
            "**Current verdict:** `C_parent` is still the coupling bottleneck. 1430 writes a branch-locked `C_parent.csv`, but every row is explicitly nonclaim because the coupling vector is not yet derived, numeric, or source-backed.",
            "**Main progress:** the finite-WEP runner now has a real coefficient file to inspect and refuse. The allowed future exits are sharply split: prove the local trace-charge zero theorem, or import a genuinely sourced parent coupling vector with units/signs/branch ownership.",
            "## Source register\n" + md_table(sections["sources"]),
            "## Coupling source hunt\n" + md_table(sections["hunt"]),
            "## C_parent signature contract\n" + md_table(sections["contract"]),
            "## C_parent placeholder rows\n" + md_table(sections["c_parent"]),
            "## Branch match audit\n" + md_table(sections["branch_audit"]),
            "## Runner refusal status\n" + md_table(sections["runner"]),
            "## Claim gates\n" + md_table(sections["claims"]),
            "## Decision ledger\n" + md_table(sections["decisions"]),
            "## Validation\n" + md_table(sections["validation"]),
            "## Next target\n" + md_table(sections["next"]),
        ]
    )
    DOC.write_text(content + "\n", encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    branch = branch_id()
    sources = source_register_rows(branch)
    hunt = coupling_source_hunt_rows()
    contract = c_parent_signature_contract_rows(branch)
    c_parent = c_parent_rows(branch)
    write_c_parent_file(c_parent)
    branch_audit = branch_match_audit_rows(branch)
    runner = runner_refusal_rows()
    claims = claim_gate_rows()
    decisions = decision_rows()
    next_rows = next_target_rows()

    write_csv(SOURCE_REGISTER, sources)
    write_csv(COUPLING_SOURCE_HUNT, hunt)
    write_csv(C_PARENT_SIGNATURE_CONTRACT, contract)
    write_csv(C_PARENT_ROWS, c_parent)
    write_csv(BRANCH_MATCH_AUDIT, branch_audit)
    write_csv(RUNNER_REFUSAL, runner)
    write_csv(CLAIM_GATE, claims)
    write_csv(DECISION_LEDGER, decisions)
    write_csv(NEXT_TARGET, next_rows)

    validation = validation_rows(sources, c_parent, branch_audit, claims)
    write_csv(VALIDATION, validation)
    write_doc(
        {
            "sources": sources,
            "hunt": hunt,
            "contract": contract,
            "c_parent": c_parent,
            "branch_audit": branch_audit,
            "runner": runner,
            "claims": claims,
            "decisions": decisions,
            "validation": validation,
            "next": next_rows,
        }
    )
    remove_pycache()
    print("Y5_R10_1430_C_parent_placeholder_refusal_written_nonclaim")


if __name__ == "__main__":
    main()
