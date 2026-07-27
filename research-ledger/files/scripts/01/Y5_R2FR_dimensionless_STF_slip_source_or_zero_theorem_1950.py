from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
SOURCE_WEIGHT_DOCS = ROOT / "source-intake" / "source-weight" / "docs"
MICROSCOPE_COEFFS = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "coefficients"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
QUARANTINE = ROOT / "source-intake" / "microscope" / "quarantine" / "1950"
FORMALIZATION = ROOT.parent / "formalization-workbench"

DOC = ROOT / "1950-Y5-R2FR-dimensionless-STF-slip-source-or-zero-theorem.md"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
GENERATED_UTC = datetime.now(timezone.utc).isoformat()

SOURCES = {
    "1949_doc": ROOT / "1949-Y5-R2FR-R11-PTF-source-or-kappa-CTF-normalization.md",
    "1949_validation": OUT / "P8_Y5_BRR545_1949_VALIDATION.csv",
    "1949_product": OUT / "P8_Y5_PARENT_QLOC_1949_CASSINI_PRODUCT_COMPRESSION.csv",
    "1949_inputs": OUT / "P8_Y5_PARENT_QLOC_1949_COMPRESSED_SLIP_INPUT_LEDGER.csv",
    "1949_runner": OUT / "P8_Y5_PARENT_QLOC_1949_COMPRESSED_RUNNER_UPDATE.csv",
    "1946_hessian": OUT / "P8_Y5_PARENT_QLOC_1946_HESSIAN_SLIP_KILL_LEMMA.csv",
    "1947_kernel": OUT / "P8_Y5_PARENT_QLOC_1947_BOUNDARY_KERNEL_ISOTROPY_ATTEMPT.csv",
    "1948_failures": OUT / "P8_Y5_PARENT_QLOC_1948_CASSINI_SLIP_FAILURE_MODE_LEDGER.csv",
}

NEEDLES = {
    "1949_doc": ["PCOMP1949_1_define_dimensionless_slip", "NEXT1949_0_primary", "VAL1949_OVERALL"],
    "1949_validation": ["VAL1949_OVERALL", "PASS"],
    "1949_product": ["PCOMP1949_1_define_dimensionless_slip", "PCOMP1949_4_common_mode_guard"],
    "1949_inputs": ["CSI1949_1_S_TF", "MISSING_COMPRESSED_SLIP_AMPLITUDE"],
    "1949_runner": ["RUN1949_0_compressed_schema", "SCHEMA_SIMPLIFIED_INPUTS_MISSING"],
    "1946_hessian": ["HSK1946_2_solution_family", "HSK1946_3_bounded_decay_kill"],
    "1947_kernel": ["BKI1947_1_common_mode_kernel", "ROTATIONAL_SYMMETRY_ALONE_NOT_SUFFICIENT"],
    "1948_failures": ["FAIL1948_4_SBI1947_6_PTF_amplitude", "POLICY_CANDIDATE_NOT_FINAL_CLAIM_RULE"],
}

OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_1950_SOURCE_REGISTER.csv",
    "stf_decomposition": OUT / "P8_Y5_PARENT_QLOC_1950_STF_DECOMPOSITION_AND_ZERO_ROUTE.csv",
    "stf_source_ledger": OUT / "P8_Y5_PARENT_QLOC_1950_DIMENSIONLESS_STF_SOURCE_LEDGER.csv",
    "runner_update": OUT / "P8_Y5_PARENT_QLOC_1950_STF_RUNNER_UPDATE.csv",
    "blocker_ledger": OUT / "P8_Y5_PARENT_QLOC_1950_STF_BLOCKER_LEDGER.csv",
    "claim_gate": OUT / "P8_Y5_PARENT_QLOC_1950_CLAIM_GATE.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_1950_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_1950_NEXT_TARGET.csv",
    "status_snapshot": OUT / "P8_Y5_PARENT_QLOC_1950_PROJECT_STATUS_SNAPSHOT.csv",
    "validation": OUT / "P8_Y5_BRR545_1950_VALIDATION.csv",
}

BRANCH_COPIES = {
    "source_weight_stf": SOURCE_WEIGHT_DOCS / "DIMENSIONLESS_STF_SLIP_SOURCE_1950_NONCLAIM.csv",
    "microscope_claim_gate": MICROSCOPE_COEFFS / "P8_Y5_PARENT_QLOC_1950_CLAIM_GATE_NONCLAIM.csv",
    "next_queue": QUEUE / "JR1950_STF_RESPONSE_FUNCTIONAL_OR_ZERO_THEOREM_QUEUE.csv",
    "claim_quarantine": QUARANTINE / "P8_Y5_PARENT_QLOC_1950_CLAIM_GATE.csv",
}


def flag(value: bool) -> str:
    return "True" if value else "False"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def has_needles(path: Path, needles: list[str]) -> bool:
    if not path.exists():
        return False
    text = read_text(path)
    return all(needle in text for needle in needles)


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source_id, path in SOURCES.items():
        needles = NEEDLES[source_id]
        ok = has_needles(path, needles)
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "source_id": source_id,
                "source_path": str(path),
                "purpose": "1950 dimensionless STF slip source or zero theorem",
                "required_needles": ";".join(needles),
                "status": "EXISTS_NEEDLES_CONFIRMED" if ok else "MISSING_SOURCE_OR_NEEDLE",
                "issue": "" if ok else "source path missing or required needles absent",
                "valid_for_claim": flag(False),
                "claim_allowed": flag(False),
                "generated_utc": GENERATED_UTC,
            }
        )
    return rows


def stf_decomposition_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "decomposition_id": "STF1950_0_target",
            "statement": "Cassini gamma at this checkpoint tests the dimensionless traceless-spatial slip amplitude S_TF.",
            "math_form": "delta_gamma_R11 ~= S_TF; acceptance abs(S_TF) <= gamma_bound_policy",
            "status": "TARGET_CONFIRMED_FROM_1949",
            "implication": "local-GR gamma gate is now one observable amplitude, not a vague residual family",
            "valid_for_claim": flag(False),
            "claim_allowed": flag(False),
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "decomposition_id": "STF1950_1_common_mode_projection",
            "statement": "Conformal/common-mode spatial residuals do not source S_TF.",
            "math_form": "P_TF[S(r) delta_ij]=0 and P_TF[2a delta_ij]=0",
            "status": "COMMON_MODE_GAMMA_SILENT",
            "implication": "Cassini cannot by itself reject common-mode Newtonian/cosmology residuals",
            "valid_for_claim": flag(False),
            "claim_allowed": flag(False),
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "decomposition_id": "STF1950_2_hessian_STF_channel",
            "statement": "Scalar Hessian memory contributes only through its STF radial channel.",
            "math_form": "P_TF[partial_i partial_j f]=(f''-f'/r)(n_i n_j-delta_ij/3)",
            "status": "STF_HESSIAN_CHANNEL_IDENTIFIED",
            "implication": "zero route is f''=f'/r plus signed boundary/silence conditions; otherwise bound S_TF",
            "valid_for_claim": flag(False),
            "claim_allowed": flag(False),
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "decomposition_id": "STF1950_3_kernel_STF_channel",
            "statement": "Nonlocal/kernel/source-worldtube effects are safe only if their projected STF response vanishes or is bounded.",
            "math_form": "S_TF = Pi_STF[projected local kernel/source response]",
            "status": "KERNEL_STF_CHANNEL_RETAINED",
            "implication": "rotational symmetry alone is not a proof; direct response functional needed",
            "valid_for_claim": flag(False),
            "claim_allowed": flag(False),
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "decomposition_id": "STF1950_4_zero_theorem_condition",
            "statement": "A parent-signed local theorem must kill every STF channel, not just the monopole/common mode.",
            "math_form": "S_TF=0 if algebraic O(3) common-mode + Hessian silence + boundary/kernel STF silence are parent-signed",
            "status": "ZERO_THEOREM_CONDITION_EXACT_BUT_UNSIGNED",
            "implication": "we know the exact theorem shape, but it is not currently proved",
            "valid_for_claim": flag(False),
            "claim_allowed": flag(False),
            "generated_utc": GENERATED_UTC,
        },
    ]


def stf_source_ledger_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "source_id": "SRC1950_0_gamma_bound_policy",
            "symbol": "gamma_bound_policy",
            "definition": "private conservative Cassini screening threshold",
            "current_value": "6.700000e-05",
            "units": "dimensionless",
            "status": "NUMERIC_POLICY_AVAILABLE_NONCLAIM",
            "source_ref": "CSI1949_0_gamma_bound_policy",
            "valid_for_claim": flag(False),
            "claim_allowed": flag(False),
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "source_id": "SRC1950_1_S_TF_direct",
            "symbol": "S_TF",
            "definition": "dimensionless projected STF slip amplitude after source/profile/boundary projection",
            "current_value": "MISSING",
            "units": "dimensionless",
            "status": "MISSING_DIRECT_DIMENSIONLESS_STF_RESPONSE",
            "source_ref": "CSI1949_1_S_TF",
            "valid_for_claim": flag(False),
            "claim_allowed": flag(False),
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "source_id": "SRC1950_2_S_TF_zero",
            "symbol": "S_TF=0",
            "definition": "parent-signed theorem-zero route for every STF channel",
            "current_value": "NOT_PARENT_SIGNED",
            "units": "boolean/theorem",
            "status": "MISSING_PARENT_SIGNED_STF_ZERO_THEOREM",
            "source_ref": "STF1950_4_zero_theorem_condition",
            "valid_for_claim": flag(False),
            "claim_allowed": flag(False),
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "source_id": "SRC1950_3_STF_bound",
            "symbol": "abs(S_TF)",
            "definition": "direct upper bound on dimensionless STF response from parent model or source runner",
            "current_value": "MISSING",
            "units": "dimensionless",
            "status": "MISSING_DIRECT_STF_BOUND",
            "source_ref": "RUN1949_0_compressed_schema",
            "valid_for_claim": flag(False),
            "claim_allowed": flag(False),
            "generated_utc": GENERATED_UTC,
        },
    ]


def runner_update_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "runner_id": "RUN1950_0_direct_STF_schema",
            "prediction": "delta_gamma_R11 ~= S_TF",
            "acceptance_rule": "abs(S_TF) <= 6.7e-5 private screening threshold",
            "current_prediction": "MISSING_DIRECT_DIMENSIONLESS_STF_RESPONSE",
            "runner_status": "BLOCKED_MISSING_S_TF",
            "missing_inputs": "S_TF numeric/bound or parent-signed S_TF=0",
            "valid_for_claim": flag(False),
            "claim_allowed": flag(False),
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "runner_id": "RUN1950_1_zero_theorem_schema",
            "prediction": "S_TF=0",
            "acceptance_rule": "0 <= 6.7e-5",
            "current_prediction": "NOT_PARENT_SIGNED",
            "runner_status": "WOULD_PASS_IF_STF_ZERO_THEOREM_SIGNED_BLOCKED",
            "missing_inputs": "parent-signed kill of Hessian STF and boundary/kernel STF channels",
            "valid_for_claim": flag(False),
            "claim_allowed": flag(False),
            "generated_utc": GENERATED_UTC,
        },
    ]


def blocker_ledger_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "blocker_id": "BLK1950_0_direct_response",
            "blocker": "No numeric or bounded dimensionless S_TF response functional exists.",
            "effect": "Cassini runner cannot evaluate MTS prediction",
            "required_fix": "derive/source S_TF[local state, source profile, kernel, boundary] as a dimensionless number or bound",
            "valid_for_claim": flag(False),
            "claim_allowed": flag(False),
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "blocker_id": "BLK1950_1_zero_theorem",
            "blocker": "S_TF=0 theorem is not parent-signed.",
            "effect": "the theorem-zero shortcut cannot be used as a Cassini pass",
            "required_fix": "sign algebraic O(3) residual, Hessian silence, and boundary/kernel STF silence from parent action",
            "valid_for_claim": flag(False),
            "claim_allowed": flag(False),
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "blocker_id": "BLK1950_2_common_mode_scope",
            "blocker": "Common-mode gamma-silent residuals remain outside S_TF.",
            "effect": "even S_TF=0 would not prove full local GR/Newton by itself",
            "required_fix": "route common-mode terms to Xi_N/effective-G/cosmology gates",
            "valid_for_claim": flag(False),
            "claim_allowed": flag(False),
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "blocker_id": "BLK1950_3_public_policy",
            "blocker": "Cassini confidence policy is private screening only.",
            "effect": "public claim would still need justified statistical convention",
            "required_fix": "choose a sourced public comparison rule after the theory prediction exists",
            "valid_for_claim": flag(False),
            "claim_allowed": flag(False),
            "generated_utc": GENERATED_UTC,
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1950_0_STF_decomposition",
            "claim": "Cassini gamma branch is isolated to the dimensionless STF slip amplitude.",
            "status": "PASS_NONCLAIM",
            "reason": "common-mode and STF channels are separated",
            "valid_for_claim": flag(False),
            "claim_allowed": flag(False),
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1950_1_common_mode_guard",
            "claim": "Common-mode residuals are gamma-silent but not local-GR proof.",
            "status": "PASS_NONCLAIM",
            "reason": "scope guard prevents Cassini from absorbing Newtonian/cosmology gates",
            "valid_for_claim": flag(False),
            "claim_allowed": flag(False),
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1950_2_S_TF_numeric",
            "claim": "MTS supplies numeric or bounded S_TF.",
            "status": "FAIL_BLOCKED",
            "reason": "direct dimensionless STF response is missing",
            "valid_for_claim": flag(False),
            "claim_allowed": flag(False),
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1950_3_S_TF_zero_theorem",
            "claim": "MTS parent signs S_TF=0.",
            "status": "FAIL_BLOCKED",
            "reason": "Hessian and boundary/kernel STF channels are not parent-signed silent",
            "valid_for_claim": flag(False),
            "claim_allowed": flag(False),
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1950_4_Cassini_pass",
            "claim": "MTS passes Cassini gamma.",
            "status": "FAIL_BLOCKED",
            "reason": "no numeric/bounded or theorem-zero S_TF exists",
            "valid_for_claim": flag(False),
            "claim_allowed": flag(False),
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1950_5_local_GR_PPN",
            "claim": "MTS derives local GR/PPN.",
            "status": "FAIL_BLOCKED",
            "reason": "S_TF is only the gamma gate; other residuals and common mode remain open",
            "valid_for_claim": flag(False),
            "claim_allowed": flag(False),
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1950_6_public_claim",
            "claim": "1950 is public-ready local-GR evidence.",
            "status": "FAIL_BLOCKED",
            "reason": "private STF decomposition checkpoint only",
            "valid_for_claim": flag(False),
            "claim_allowed": flag(False),
            "generated_utc": GENERATED_UTC,
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1950_0_progress",
            "decision": "S_TF_DECOMPOSED_INTO_COMMON_MODE_SILENT_AND_STF_DANGEROUS_CHANNELS",
            "reason": "the Cassini gate now tracks only true traceless-spatial slip, while common-mode residuals are routed elsewhere",
            "next_action": "derive a dimensionless STF response functional or prove every STF channel zero",
            "valid_for_claim": flag(False),
            "claim_allowed": flag(False),
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1950_1_next",
            "decision": "BUILD_STF_RESPONSE_FUNCTIONAL_OR_COMMON_MODE_ROUTER",
            "reason": "without a direct S_TF response, the Cassini runner remains blocked; common-mode terms should not be lost",
            "next_action": "attempt a minimal STF response functional S_TF=Pi_STF[R11 response] and route gamma-silent common mode to Xi_N",
            "valid_for_claim": flag(False),
            "claim_allowed": flag(False),
            "generated_utc": GENERATED_UTC,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "next_id": "NEXT1950_0_primary",
            "priority": "selected",
            "target_doc": "1951-Y5-R2FR-STF-response-functional-or-common-mode-router.md",
            "target_script": "scripts/Y5_R2FR_STF_response_functional_or_common_mode_router_1951.py",
            "objective": "construct the minimal dimensionless STF response functional for S_TF, or route gamma-silent common mode into Newtonian/cosmology gates without claiming local GR",
            "acceptance_output": "direct S_TF functional/bound row, parent-zero theorem, or blocker ledger plus common-mode routing",
            "nonclaim_rule": "no Cassini/local-GR claim unless S_TF is numeric below bound or theorem-zero; no full local-GR claim from gamma alone",
            "valid_for_claim": flag(False),
            "claim_allowed": flag(False),
            "generated_utc": GENERATED_UTC,
        }
    ]


def status_snapshot_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "snapshot_id": "SNAP1950_0_project_position",
            "status": "STF_SLIP_CHANNEL_ISOLATED_COMMON_MODE_ROUTED_OUT",
            "strongest_result": "Cassini gamma branch now tests only S_TF; common-mode/conformal residuals are gamma-silent but remain Newtonian/cosmology debts",
            "what_improved": "the local-GR problem is split into an STF gamma gate and a common-mode Newtonian gate",
            "still_missing": "numeric/source-backed S_TF or parent-signed S_TF=0 theorem",
            "claim_status": "Cassini/local-GR public claims remain blocked",
            "valid_for_claim": flag(False),
            "claim_allowed": flag(False),
            "generated_utc": GENERATED_UTC,
        }
    ]


def copy_branch_artifacts(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    write_csv(BRANCH_COPIES["source_weight_stf"], rows_by_name["stf_decomposition"])
    write_csv(BRANCH_COPIES["microscope_claim_gate"], rows_by_name["claim_gate"])
    write_csv(BRANCH_COPIES["next_queue"], rows_by_name["next_target"])
    write_csv(BRANCH_COPIES["claim_quarantine"], rows_by_name["claim_gate"])


def remove_pycache() -> None:
    pycache = Path(__file__).resolve().parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def csv_has_rows(path: Path) -> bool:
    if not path.exists():
        return False
    with path.open(newline="", encoding="utf-8") as handle:
        return len(list(csv.DictReader(handle))) > 0


def formalization_1950_artifact_count() -> int:
    if not FORMALIZATION.exists():
        return 0
    patterns = ("1950-", "*_1950_*", "*Y5*1950*", "*VAL1950*", "*P8*1950*")
    count = 0
    for path in FORMALIZATION.rglob("*"):
        name = path.name
        if any(Path(name).match(pattern) for pattern in patterns):
            count += 1
    return count


def validation_row(validation_id: str, status: str, detail: str) -> dict[str, str]:
    return {
        "validation_id": validation_id,
        "status": status,
        "detail": detail,
        "valid_for_claim": flag(False),
        "claim_allowed": flag(False),
    }


def validate(rows_by_name: dict[str, list[dict[str, Any]]]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []

    sources_ok = all(row["status"] == "EXISTS_NEEDLES_CONFIRMED" for row in rows_by_name["source_register"])
    rows.append(validation_row("VAL1950_00_sources", "PASS" if sources_ok else "FAIL", "all local source paths exist and needles found" if sources_ok else "source path or needle missing"))

    decomp_text = "\n".join(row["status"] + " " + row["math_form"] for row in rows_by_name["stf_decomposition"])
    decomp_ok = "COMMON_MODE_GAMMA_SILENT" in decomp_text and "STF_HESSIAN_CHANNEL_IDENTIFIED" in decomp_text and "ZERO_THEOREM_CONDITION_EXACT_BUT_UNSIGNED" in decomp_text
    rows.append(validation_row("VAL1950_01_stf_decomposition", "PASS" if decomp_ok else "FAIL", "STF/common-mode split and zero condition recorded"))

    source_ok = any(row["symbol"] == "S_TF" and row["status"] == "MISSING_DIRECT_DIMENSIONLESS_STF_RESPONSE" for row in rows_by_name["stf_source_ledger"])
    rows.append(validation_row("VAL1950_02_source_ledger", "PASS" if source_ok else "FAIL", "direct S_TF remains missing and explicit"))

    runner_ok = rows_by_name["runner_update"][0]["runner_status"] == "BLOCKED_MISSING_S_TF" and rows_by_name["runner_update"][1]["runner_status"].startswith("WOULD_PASS_IF")
    rows.append(validation_row("VAL1950_03_runner_update", "PASS" if runner_ok else "FAIL", "runner blocks direct and theorem-zero branches correctly"))

    blocker_ok = any("Common-mode" in row["blocker"] for row in rows_by_name["blocker_ledger"]) and all(row["claim_allowed"] == flag(False) for row in rows_by_name["blocker_ledger"])
    rows.append(validation_row("VAL1950_04_blockers", "PASS" if blocker_ok else "FAIL", "STF blockers and common-mode scope recorded"))

    claim_rows = rows_by_name["claim_gate"]
    claim_ok = len([row for row in claim_rows if row["status"] == "PASS_NONCLAIM"]) == 2 and len([row for row in claim_rows if row["status"] == "FAIL_BLOCKED"]) == 5
    rows.append(validation_row("VAL1950_05_claim_gates", "PASS" if claim_ok else "FAIL", "only decomposition nonclaim gates pass; claims blocked"))

    decision_ok = any(row["decision"] == "BUILD_STF_RESPONSE_FUNCTIONAL_OR_COMMON_MODE_ROUTER" for row in rows_by_name["decision"])
    rows.append(validation_row("VAL1950_06_decision", "PASS" if decision_ok else "FAIL", "STF response/common-mode router selected"))

    next_ok = rows_by_name["next_target"][0]["target_doc"].startswith("1951-Y5-R2FR-STF-response-functional")
    rows.append(validation_row("VAL1950_07_next_target", "PASS" if next_ok else "FAIL", "1951 STF response target selected"))

    flags_ok = all(row.get("valid_for_claim") == flag(False) and row.get("claim_allowed") == flag(False) for table in rows_by_name.values() for row in table)
    rows.append(validation_row("VAL1950_08_claim_flags_safe", "PASS" if flags_ok else "FAIL", "claim flags all false"))

    output_paths = [path for key, path in OUTPUTS.items() if key != "validation"]
    csv_ok = all(csv_has_rows(path) for path in output_paths)
    rows.append(validation_row("VAL1950_09_csv_parse", "PASS" if csv_ok else "FAIL", "all generated CSVs parse with rows"))

    branch_ok = all(csv_has_rows(path) for path in BRANCH_COPIES.values())
    rows.append(validation_row("VAL1950_10_branch_copies", "PASS" if branch_ok else "FAIL", "; ".join(str(path) for path in BRANCH_COPIES.values())))

    pycache_absent = not (Path(__file__).resolve().parent / "__pycache__").exists()
    rows.append(validation_row("VAL1950_11_pycache_absent", "PASS" if pycache_absent else "FAIL", "scripts __pycache__ absent"))

    formalization_count = formalization_1950_artifact_count()
    rows.append(validation_row("VAL1950_12_formalization_untouched", "PASS" if formalization_count == 0 else "FAIL", f"formalization_1950_artifact_count={formalization_count}"))

    overall_ok = all(row["status"] == "PASS" for row in rows)
    rows.append(validation_row("VAL1950_OVERALL", "PASS" if overall_ok else "FAIL", "1950 dimensionless STF slip source or zero theorem"))
    return rows


def escape_cell(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", "<br>")


def markdown_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return ""
    headers = list(rows[0].keys())
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(escape_cell(row.get(header, "")) for header in headers) + " |")
    return "\n".join(lines)


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    sections = [
        "# 1950 Y5 R2FR: Dimensionless STF Slip Source or Zero Theorem",
        "",
        "## Verdict",
        "",
        "1950 separates the Cassini-local problem into the right pieces. The gamma gate is only the dimensionless STF/traceless-spatial slip amplitude `S_TF`. Conformal/common-mode residuals are gamma-silent and must be routed to Newtonian/effective-G/cosmology gates instead of being mistaken for a Cassini failure or pass.",
        "",
        "The dangerous channel is true STF structure: radial Hessian pieces proportional to `f''-f'/r`, nonlocal/source-worldtube STF projections, or any parent residual that leaves a spatial dyad. A full zero theorem must kill every one of those channels. Current work has conditional kill lemmas, but no parent-signed `S_TF=0` theorem and no numeric/direct bound for `S_TF`.",
        "",
        "So the next target is not more coefficient sprawl. It is a minimal dimensionless STF response functional, or a parent-zero theorem. Until then, Cassini/local-GR claims remain blocked.",
        "",
        "## Source Register",
        "",
        markdown_table(rows_by_name["source_register"]),
        "",
        "## STF Decomposition and Zero Route",
        "",
        markdown_table(rows_by_name["stf_decomposition"]),
        "",
        "## Dimensionless STF Source Ledger",
        "",
        markdown_table(rows_by_name["stf_source_ledger"]),
        "",
        "## Runner Update",
        "",
        markdown_table(rows_by_name["runner_update"]),
        "",
        "## Blocker Ledger",
        "",
        markdown_table(rows_by_name["blocker_ledger"]),
        "",
        "## Claim Gate",
        "",
        markdown_table(rows_by_name["claim_gate"]),
        "",
        "## Decision Ledger",
        "",
        markdown_table(rows_by_name["decision"]),
        "",
        "## Next Target",
        "",
        markdown_table(rows_by_name["next_target"]),
        "",
        "## Project Status Snapshot",
        "",
        markdown_table(rows_by_name["status_snapshot"]),
        "",
        "## Validation",
        "",
        markdown_table(rows_by_name["validation"]),
        "",
    ]
    DOC.write_text("\n".join(sections), encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    SOURCE_WEIGHT_DOCS.mkdir(parents=True, exist_ok=True)
    MICROSCOPE_COEFFS.mkdir(parents=True, exist_ok=True)
    QUEUE.mkdir(parents=True, exist_ok=True)
    QUARANTINE.mkdir(parents=True, exist_ok=True)

    rows_by_name = {
        "source_register": source_register_rows(),
        "stf_decomposition": stf_decomposition_rows(),
        "stf_source_ledger": stf_source_ledger_rows(),
        "runner_update": runner_update_rows(),
        "blocker_ledger": blocker_ledger_rows(),
        "claim_gate": claim_gate_rows(),
        "decision": decision_rows(),
        "next_target": next_target_rows(),
        "status_snapshot": status_snapshot_rows(),
    }

    for output_key, output_path in OUTPUTS.items():
        if output_key == "validation":
            continue
        write_csv(output_path, rows_by_name[output_key])

    copy_branch_artifacts(rows_by_name)
    remove_pycache()
    rows_by_name["validation"] = validate(rows_by_name)
    write_csv(OUTPUTS["validation"], rows_by_name["validation"])
    write_doc(rows_by_name)


if __name__ == "__main__":
    main()
