from __future__ import annotations

import csv
from datetime import datetime, timezone
from io import StringIO
from pathlib import Path
from typing import Dict, Iterable, List, Tuple


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4367"
CLAIM_ID = "L-208"
BRANCH = "MTS_R2FR_Y5_TRANSITION_SCALAR_SOURCE_NORMALIZATION_GAMMA_BETA_TRANSFER_OR_WEP_ONLY_QUARANTINE_4367"
MARKER = "PPC4161_TRANSITION_SCALAR_SOURCE_NORMALIZATION_GAMMA_BETA_TRANSFER_OR_WEP_ONLY_QUARANTINE_4367"
PACKET_MARKER = "PPC4161_PACKET_TRANSITION_SCALAR_SOURCE_NORMALIZATION_GAMMA_BETA_TRANSFER_OR_WEP_ONLY_QUARANTINE_4367"
DECISION = "SCALAR_COMMON_SOURCE_NORMALIZATION_GAMMA_BETA_ZERO_THEOREM_DERIVED_RELATIVE_WEP_PRODUCT_QUARANTINED_NONCLAIM"
NEXT_TARGET = "4368-Y5-R2FR-transition-parent-sign-common-source-normalization-or-final-WEP-product-quarantine.md"

FORMAL_PATH = FORMAL / "383-PPC4161-transition-scalar-source-normalization-gamma-beta-transfer-or-WEP-only-quarantine.md"
DOC_PATH = POST / "4367-Y5-R2FR-transition-scalar-source-normalization-gamma-beta-transfer-or-WEP-only-quarantine.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4367_VALIDATION.csv"
STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()


LOCAL_SOURCES: Dict[str, Tuple[Path, str, str]] = {
    "SRC4367_00_4366_formal": (
        FORMAL / "382-PPC4161-transition-preferred-frame-product-channel-zero-or-PiPPN-transfer-coefficient.md",
        "gamma/beta scalar metric transfer remains open",
        "4366 leaves gamma/beta scalar transfer as the next target.",
    ),
    "SRC4367_01_4366_transfer": (
        SOURCE_DIR / "P8_Y5_R2FR_4366_PREFERRED_FRAME_TRANSFER_ROWS.csv",
        "PI4366_gamma_product",
        "4366 transfer rows keep gamma/beta open.",
    ),
    "SRC4367_02_4365_thresholds": (
        SOURCE_DIR / "P8_Y5_R2FR_4365_CRITICAL_TRANSFER_THRESHOLDS.csv",
        "CT4365_R3_gamma",
        "gamma/beta critical transfer thresholds.",
    ),
    "SRC4367_03_calibrated_G": (
        FORMAL / "194-PPC4161-calibrated-source-coupling-kappa-to-GN-law.md",
        "G_cal := c^4 kappa_eff/(8*pi)",
        "calibrated local Newton coupling and source normalization law.",
    ),
    "SRC4367_04_poisson_newton": (
        FORMAL / "187-PPC4161-Poisson-Gauss-Newton-readout-from-Hamiltonian-source-charge.md",
        "nabla^2 Phi_N",
        "weak-field Poisson/Gauss/Newton source readout.",
    ),
    "SRC4367_05_mass_glue": (
        FORMAL / "186-PPC4161-Hamiltonian-worldtube-mass-readout-glue.md",
        "No orbital `GM`",
        "Hamiltonian source charge is defined before orbital readout.",
    ),
    "SRC4367_06_ppn_readout": (
        FORMAL / "188-PPC4161-full-PPN-readout-vector.md",
        "gamma = 1",
        "PPN gamma/beta are GR coefficients inside the private packet.",
    ),
    "SRC4367_07_reactivation": (
        SOURCE_DIR / "P8_Y5_R2FR_4178_REACTIVATION_LEDGER.csv",
        "RE4178_1_ZH_leak",
        "source-measure leak reopens WEP/source-normalization rows.",
    ),
    "SRC4367_08_product_bound": (
        SOURCE_DIR / "P8_Y5_R2FR_4363_WEPPRODUCT_PROJECTION_ROW.csv",
        "PI4363_WEP_product",
        "WEP product bound row that must be quarantined unless common-source conditions hold.",
    ),
}


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def find_line(path: Path, needle: str) -> str:
    text = read_text(path)
    index = text.find(needle)
    if index < 0:
        return ""
    return str(text[:index].count("\n") + 1)


def read_csv(path: Path) -> List[Dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: List[Dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    fields: List[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: str(row.get(field, "")) for field in fields})


def csv_line(row: Iterable[str]) -> str:
    buffer = StringIO()
    writer = csv.writer(buffer, lineterminator="\n")
    writer.writerow(list(row))
    return buffer.getvalue()


def md_cell(value: object) -> str:
    return str(value).replace("|", r"\|").replace("\n", "<br>")


def md_table(rows: List[Dict[str, str]], fields: List[str]) -> str:
    lines = [
        "| " + " | ".join(fields) + " |",
        "| " + " | ".join("---" for _ in fields) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(md_cell(row.get(field, "")) for field in fields) + " |")
    return "\n".join(lines)


def append_once(path: Path, marker: str, block: str) -> None:
    text = read_text(path)
    if marker in text:
        return
    if text and not text.endswith("\n"):
        text += "\n"
    path.write_text(text + block.strip() + "\n", encoding="utf-8")


def append_claim_once(path: Path, claim_id: str, row: List[str]) -> None:
    text = read_text(path)
    if f"\n{claim_id}," in text:
        return
    if text and not text.endswith("\n"):
        text += "\n"
    path.write_text(text + csv_line(row), encoding="utf-8")


def threshold_lookup() -> Dict[str, Dict[str, str]]:
    rows = read_csv(SOURCE_DIR / "P8_Y5_R2FR_4365_CRITICAL_TRANSFER_THRESHOLDS.csv")
    return {row["observable"]: row for row in rows}


def source_rows() -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    for source_id, (path, needle, role) in LOCAL_SOURCES.items():
        line_number = find_line(path, needle)
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "source_id": source_id,
                "path": str(path),
                "path_exists": str(path.exists()),
                "needle": needle,
                "needle_found": str(bool(line_number)),
                "line_number": line_number,
                "role": role,
                "valid_for_claim": "False",
            }
        )
    return rows


def theorem_rows() -> List[Dict[str, str]]:
    return [
        {
            "theorem_id": "TH4367_0_common_scalar_absorption",
            "statement": "If p_WEP is a common scalar multiplier of the same Hilbert source density and Hamiltonian mass used to define U, then gamma and beta are unchanged.",
            "proof_sketch": "Replace rho_H by rho'_H=(1+p)rho_H and M_H by M'_H=(1+p)M_H before readout. The observed Newton potential U' solves the same Poisson equation with the same EH metric expansion. PPN gamma and beta are coefficients relative to U' and U'^2, so their GR values remain gamma=1 and beta=1.",
            "result": "T_gamma_product=T_beta_product=0 on the common scalar branch",
            "proof_status": "CONDITIONAL_THEOREM_DERIVED",
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "TH4367_1_relative_product_quarantine",
            "statement": "If p_WEP is source-label, material, test-body, readout, time, boundary or non-Hilbert relative data, it cannot be exported to gamma/beta by common-source absorption.",
            "proof_sketch": "A relative product changes composition/source labels or readout response rather than the common Hilbert source used to define U. Then it is not a single calibrated mass/coupling normalization; exporting it to local GR would divide by an unsigned convention or hide a WEP residual.",
            "result": "WEP product row remains WEP-only unless common scalar premises are parent-signed",
            "proof_status": "QUARANTINE_THEOREM_DERIVED",
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "TH4367_2_Newton_shape_vs_amplitude",
            "statement": "Common scalar source normalization preserves the Newton/Poisson shape but not a numerical prediction of G or source mass.",
            "proof_sketch": "The equation keeps nabla^2 Phi=4*pi G_cal rho_H and Phi=-G_cal M_H/r after redefining the calibrated source charge. The structural law survives; numeric G and absolute source mass remain empirical/private-branch inputs.",
            "result": "Newton shape safe on common branch; no numeric-G claim",
            "proof_status": "CONDITIONAL_STRUCTURAL_THEOREM_DERIVED",
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "TH4367_3_not_public_local_GR",
            "statement": "Even if gamma/beta and preferred-frame product transfers vanish conditionally, public local GR still requires parent activation, conservation/Bianchi closure, and non-product C_src/T_open rows.",
            "proof_sketch": "4366 premises are unsigned, Xi_open/epsilon_Gsrc/T_open rows remain live, and source-label/nonfactorized residuals can reopen local tests. The theorem is a branch rule, not global adoption.",
            "result": "no local-GR claim fires",
            "proof_status": "FIREWALL_THEOREM_DERIVED",
            "valid_for_claim": "False",
        },
    ]


def premise_rows() -> List[Dict[str, str]]:
    return [
        {
            "premise_id": "SN4367_0_common_multiplier",
            "premise": "p_WEP multiplies all relevant Hilbert source density/mass entries by one common scalar before readout",
            "status": "TARGET_SHARPENED_UNSIGNED",
            "if_missing": "relative WEP product remains WEP-only",
            "parent_signed": "False",
            "valid_for_claim": "False",
        },
        {
            "premise_id": "SN4367_1_same_source_charge",
            "premise": "the same M_Hdress/worldtube source charge is used in Poisson, PPN U, and orbital readout without GM laundering",
            "status": "PRIVATE_PACKET_CONDITIONAL_NOT_GLOBAL",
            "if_missing": "gamma/beta absorption becomes circular or source-definition dependent",
            "parent_signed": "False",
            "valid_for_claim": "False",
        },
        {
            "premise_id": "SN4367_2_calibrated_coupling_lock",
            "premise": "G_cal and kappa_eff are fixed before source comparison; p_WEP is not hidden in a post-fit G",
            "status": "PRIVATE_PACKET_CONDITIONAL_NOT_GLOBAL",
            "if_missing": "numeric G/source calibration can fake a pass",
            "parent_signed": "False",
            "valid_for_claim": "False",
        },
        {
            "premise_id": "SN4367_3_no_relative_labels",
            "premise": "no material/test/source-label/readout dependence survives in p_WEP for the gamma/beta export",
            "status": "UNSIGNED",
            "if_missing": "product row must be quarantined to WEP/source-composition",
            "parent_signed": "False",
            "valid_for_claim": "False",
        },
        {
            "premise_id": "SN4367_4_conservation_Bianchi",
            "premise": "renormalized source remains conserved Hilbert stress compatible with Bianchi identity",
            "status": "PRIVATE_PACKET_CONDITIONAL_NOT_GLOBAL",
            "if_missing": "zeta/preferred-frame/conservation rows reopen",
            "parent_signed": "False",
            "valid_for_claim": "False",
        },
    ]


def transfer_rows(thresholds: Dict[str, Dict[str, str]]) -> List[Dict[str, str]]:
    return [
        {
            "transfer_id": "PI4367_gamma_common_scalar",
            "observable": "gamma_minus_1",
            "transfer_coefficient": "T_gamma_product",
            "conditional_value": "0",
            "critical_transfer_norm": thresholds["gamma_minus_1"]["critical_transfer_norm"],
            "branch": "common scalar Hilbert-source normalization",
            "status": "CONDITIONAL_ZERO_ROW_DERIVED_NOT_PARENT_ACTIVATED",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "transfer_id": "PI4367_beta_common_scalar",
            "observable": "beta_minus_1",
            "transfer_coefficient": "T_beta_product",
            "conditional_value": "0",
            "critical_transfer_norm": thresholds["beta_minus_1"]["critical_transfer_norm"],
            "branch": "common scalar Hilbert-source normalization",
            "status": "CONDITIONAL_ZERO_ROW_DERIVED_NOT_PARENT_ACTIVATED",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "transfer_id": "PI4367_Newton_shape_common_scalar",
            "observable": "Poisson/Newton shape",
            "transfer_coefficient": "T_Newton_shape_product",
            "conditional_value": "0_shape_residual",
            "critical_transfer_norm": "not_applicable_shape_law",
            "branch": "common scalar Hilbert-source normalization",
            "status": "STRUCTURAL_SHAPE_ZERO_NUMERIC_AMPLITUDE_NOT_CLAIMED",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "transfer_id": "PI4367_relative_WEP_product",
            "observable": "WEP/source-composition only",
            "transfer_coefficient": "T_gamma_beta_from_relative_product",
            "conditional_value": "QUARANTINED",
            "critical_transfer_norm": "not_exported",
            "branch": "relative material/source/readout product",
            "status": "WEP_ONLY_QUARANTINE",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
    ]


def quarantine_rows() -> List[Dict[str, str]]:
    return [
        {
            "quarantine_id": "Q4367_0_relative_material",
            "trigger": "p_WEP differs by test body, material, composition or source label",
            "allowed_use": "WEP product comparator only",
            "forbidden_use": "gamma/beta/Newton/local-GR source export",
            "release_condition": "prove common scalar Hilbert-source multiplier before readout",
            "claim_allowed": "False",
        },
        {
            "quarantine_id": "Q4367_1_readout_only",
            "trigger": "p_WEP exists only as MICROSCOPE/readout response product",
            "allowed_use": "source-backed WEP product bound row",
            "forbidden_use": "source mass or metric potential redefinition",
            "release_condition": "derive parent source functional carrying the same p",
            "claim_allowed": "False",
        },
        {
            "quarantine_id": "Q4367_2_time_boundary",
            "trigger": "p_WEP is time-dependent, boundary/projector dependent, or not conserved",
            "allowed_use": "bounded finite residual lane",
            "forbidden_use": "absorbed common source normalization",
            "release_condition": "prove stationarity, no-flux, and Hilbert conservation",
            "claim_allowed": "False",
        },
        {
            "quarantine_id": "Q4367_3_hidden_Csrc",
            "trigger": "Xi_open, epsilon_Gsrc_open or T_open rows remain active",
            "allowed_use": "product row as one component of explicit C_src runner",
            "forbidden_use": "full local-GR claim",
            "release_condition": "project/bound or theorem-zero all remaining C_src/T_open rows",
            "claim_allowed": "False",
        },
    ]


def runner_rows() -> List[Dict[str, str]]:
    return [
        {
            "run_id": "RUN4367_0_common_scalar",
            "input_case": "p_WEP common scalar Hilbert-source multiplier",
            "result": "T_gamma=T_beta=0 conditionally",
            "claim_status": "NOT_PARENT_ACTIVATED",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "run_id": "RUN4367_1_relative_product",
            "input_case": "p_WEP relative/source-label/readout product",
            "result": "WEP_ONLY_QUARANTINE",
            "claim_status": "NO_GAMMA_BETA_EXPORT",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "run_id": "RUN4367_2_Newton_shape",
            "input_case": "common scalar branch",
            "result": "Poisson/Newton shape preserved; numeric amplitude not predicted",
            "claim_status": "STRUCTURAL_NONCLAIM",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "run_id": "RUN4367_3_public_claim",
            "input_case": "full local-GR/PPN claim",
            "result": "FORBIDDEN",
            "claim_status": "PARENT_SIGNATURES_AND_OTHER_CSRC_ROWS_MISSING",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def claim_gate_rows() -> List[Dict[str, str]]:
    return [
        {
            "gate_id": "GATE4367_0_gamma_beta_theorem",
            "gate": "common scalar gamma/beta zero theorem",
            "requirement": "same Hilbert source charge defines U and M_Hdress with one common p",
            "current_result": "PASS_CONDITIONAL_THEOREM",
            "claim_allowed": "False",
        },
        {
            "gate_id": "GATE4367_1_activation",
            "gate": "activate common scalar branch",
            "requirement": "SN4367 premise set parent-signed",
            "current_result": "BLOCKED_UNSIGNED_PREMISES",
            "claim_allowed": "False",
        },
        {
            "gate_id": "GATE4367_2_quarantine",
            "gate": "relative WEP product quarantine",
            "requirement": "if common scalar branch not signed, do not export product row to local GR",
            "current_result": "ACTIVE",
            "claim_allowed": "False",
        },
        {
            "gate_id": "GATE4367_3_public_claim",
            "gate": "claim local-GR/Newton/PPN pass",
            "requirement": "activated common scalar branch plus preferred-frame zero plus all remaining C_src/T_open rows closed",
            "current_result": "FORBIDDEN",
            "claim_allowed": "False",
        },
    ]


def decision_rows() -> List[Dict[str, str]]:
    return [
        {
            "decision_id": "DEC4367_0",
            "decision": DECISION,
            "rationale": "4367 derives the exact scalar-source fork. If the WEP product is one common scalar multiplier of the same Hilbert source charge used to define the PPN potential U, then gamma and beta are unchanged: T_gamma_product=T_beta_product=0. If the product is relative to material/source/readout labels, it cannot be exported to local GR and is quarantined as WEP-only. The common scalar branch is not parent-signed in the current corpus, so no local-GR/Newton/PPN claim fires.",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "False",
            "claim_allowed": "False",
        }
    ]


def status_rows() -> List[Dict[str, str]]:
    return [
        {
            "status_id": "STAT4367_0",
            "item": "gamma beta theorem",
            "status": "DERIVED_CONDITIONAL",
            "detail": "common scalar Hilbert-source normalization gives T_gamma=T_beta=0.",
        },
        {
            "status_id": "STAT4367_1",
            "item": "relative product",
            "status": "QUARANTINED",
            "detail": "relative/material/readout WEP product may not be exported to local GR.",
        },
        {
            "status_id": "STAT4367_2",
            "item": "parent activation",
            "status": "UNSIGNED",
            "detail": "common scalar premise set is not parent-signed.",
        },
        {
            "status_id": "STAT4367_3",
            "item": "next target",
            "status": "PARENT_SIGN_OR_FINAL_QUARANTINE",
            "detail": NEXT_TARGET,
        },
    ]


def next_target_rows() -> List[Dict[str, str]]:
    return [
        {
            "target_id": "NT4367_0",
            "next_target": NEXT_TARGET,
            "question": "Can the common scalar source-normalization premise be parent-signed, or should the WEP product row be permanently quarantined from local-GR/PPN export?",
            "preferred_route": "parent-sign common scalar Hilbert-source multiplier through action/source charge/readout grammar",
            "alternate_route": "derive owner/no-wA theorem so relative product vanishes",
            "fallback_route": "finalize WEP-only quarantine and continue local GR through non-product source coupling rows",
            "claim_allowed": "False",
        }
    ]


def validation_rows(
    sources: List[Dict[str, str]],
    theorems: List[Dict[str, str]],
    premises: List[Dict[str, str]],
    transfers: List[Dict[str, str]],
    quarantines: List[Dict[str, str]],
    runner: List[Dict[str, str]],
    gates: List[Dict[str, str]],
    decisions: List[Dict[str, str]],
    statuses: List[Dict[str, str]],
    next_targets: List[Dict[str, str]],
) -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []

    def add(check_id: str, check: str, passed: bool, detail: str) -> None:
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "check_id": check_id,
                "check": check,
                "passed": str(bool(passed)),
                "detail": detail,
            }
        )

    transfer_by_obs = {row["observable"]: row for row in transfers}
    add("VAL4367_00_sources_exist", "all cited local source paths exist", all(row["path_exists"] == "True" for row in sources), "source register path_exists flags")
    add("VAL4367_01_needles_found", "all cited source needles found", all(row["needle_found"] == "True" for row in sources), "source register needle_found flags")
    add("VAL4367_02_common_theorem", "common scalar theorem present", any(row["theorem_id"] == "TH4367_0_common_scalar_absorption" for row in theorems), "TH4367_0")
    add("VAL4367_03_quarantine_theorem", "relative product quarantine theorem present", any(row["theorem_id"] == "TH4367_1_relative_product_quarantine" for row in theorems), "TH4367_1")
    add("VAL4367_04_gamma_zero", "gamma conditional zero row present", transfer_by_obs["gamma_minus_1"]["conditional_value"] == "0", "PI4367_gamma_common_scalar")
    add("VAL4367_05_beta_zero", "beta conditional zero row present", transfer_by_obs["beta_minus_1"]["conditional_value"] == "0", "PI4367_beta_common_scalar")
    add("VAL4367_06_quarantine_row", "relative product quarantine row present", any(row["status"] == "WEP_ONLY_QUARANTINE" for row in transfers), "PI4367_relative_WEP_product")
    add("VAL4367_07_premises_unsigned", "premises remain unsigned", all(row["parent_signed"] == "False" for row in premises), "premise flags")
    add("VAL4367_08_quarantine_rules", "quarantine triggers present", len(quarantines) >= 4, f"quarantines={len(quarantines)}")
    add("VAL4367_09_runner_nonclaim", "runner rows remain nonclaim", all(row["claim_allowed"] == "False" and row["valid_for_claim"] == "False" for row in runner), "runner flags")
    add("VAL4367_10_activation_blocked", "activation blocked", any(row["gate_id"] == "GATE4367_1_activation" and row["current_result"] == "BLOCKED_UNSIGNED_PREMISES" for row in gates), "activation gate")
    add("VAL4367_11_public_claim_forbidden", "public claim forbidden", any(row["gate_id"] == "GATE4367_3_public_claim" and row["current_result"] == "FORBIDDEN" for row in gates), "claim gate")
    add("VAL4367_12_decision_nonclaim", "decision nonclaim", decisions[0]["decision"] == DECISION and decisions[0]["claim_allowed"] == "False", DECISION)
    add("VAL4367_13_next_selected", "next target selected", next_targets[0]["next_target"] == NEXT_TARGET, NEXT_TARGET)
    add("VAL4367_14_formal_marker", "formal marker written", MARKER in read_text(FORMAL_PATH), str(FORMAL_PATH))
    add("VAL4367_15_post_doc_marker", "post doc marker written", MARKER in read_text(DOC_PATH), str(DOC_PATH))
    add("VAL4367_16_spine_marker", "spine marker appended", MARKER in read_text(FORMAL / "07-unification-spine.md"), str(FORMAL / "07-unification-spine.md"))
    add("VAL4367_17_packet_marker", "packet marker appended", PACKET_MARKER in read_text(FORMAL / "180-PPC4161-private-local-packet-integration.md"), str(FORMAL / "180-PPC4161-private-local-packet-integration.md"))
    add("VAL4367_18_claim_register", "claim register updated", f"\n{CLAIM_ID}," in read_text(FORMAL / "02-claims-register.csv"), str(FORMAL / "02-claims-register.csv"))
    return rows


def write_docs(
    sources: List[Dict[str, str]],
    theorems: List[Dict[str, str]],
    premises: List[Dict[str, str]],
    transfers: List[Dict[str, str]],
    quarantines: List[Dict[str, str]],
    runner: List[Dict[str, str]],
    gates: List[Dict[str, str]],
    decisions: List[Dict[str, str]],
    statuses: List[Dict[str, str]],
    next_targets: List[Dict[str, str]],
) -> None:
    formal = f"""# PPC4161 transition: scalar source-normalization gamma/beta transfer or WEP-only quarantine

Marker: `{MARKER}`

Generated: {STAMP}

## Purpose

4366 killed preferred-frame product transfer conditionally but left gamma/beta open. 4367 derives the exact fork.

If `p_WEP` is a common scalar multiplier of the same Hilbert source charge used to define the PPN potential `U`, then the metric still has the GR form in terms of the redefined `U`:

`g_00=-1+2U/c^2-2U^2/c^4+...`,

`g_ij=(1+2U/c^2)delta_ij+...`.

So `T_gamma_product=T_beta_product=0`.

If `p_WEP` is relative/material/source-label/readout data, it is not a common source normalization and must remain WEP-only.

## Theorem rows

{md_table(theorems, ["theorem_id", "statement", "proof_sketch", "result", "proof_status", "valid_for_claim"])}

## Premise audit

{md_table(premises, ["premise_id", "premise", "status", "if_missing", "parent_signed", "valid_for_claim"])}

## Transfer rows

{md_table(transfers, ["transfer_id", "observable", "transfer_coefficient", "conditional_value", "critical_transfer_norm", "branch", "status", "claim_allowed"])}

## Quarantine rules

{md_table(quarantines, ["quarantine_id", "trigger", "allowed_use", "forbidden_use", "release_condition", "claim_allowed"])}

## Runner

{md_table(runner, ["run_id", "input_case", "result", "claim_status", "claim_allowed"])}

## Claim gates

{md_table(gates, ["gate_id", "gate", "requirement", "current_result", "claim_allowed"])}

## Decision

{md_table(decisions, ["decision_id", "decision", "rationale", "next_target", "claim_allowed"])}

## Status

{md_table(statuses, ["status_id", "item", "status", "detail"])}

## Next target

{md_table(next_targets, ["target_id", "next_target", "question", "preferred_route", "alternate_route", "fallback_route", "claim_allowed"])}

## Source register

{md_table(sources, ["source_id", "path_exists", "needle_found", "line_number", "role"])}
"""
    FORMAL_PATH.write_text(formal, encoding="utf-8")

    post_doc = f"""# 4367 - scalar source-normalization gamma/beta transfer or WEP-only quarantine

Marker: `{MARKER}`

Generated: {STAMP}

## Result

- Conditional theorem: common scalar Hilbert-source normalization gives `T_gamma=T_beta=0`.
- Quarantine theorem: relative/material/source-label/readout WEP product cannot be exported to local GR.
- Current corpus has not parent-signed the common scalar premise set, so no local-GR/PPN claim fires.

## Why this matters

This is the clean way out of the gamma/beta question: either the product is just the same source charge wearing a common scalar coat, or it stays in the WEP box. No smoke ladder.

## Files

- Formal checkpoint: `{FORMAL_PATH}`
- Transfer rows: `{SOURCE_DIR / "P8_Y5_R2FR_4367_GAMMA_BETA_TRANSFER_ROWS.csv"}`
- Quarantine rules: `{SOURCE_DIR / "P8_Y5_R2FR_4367_WEP_ONLY_QUARANTINE.csv"}`
- Validation: `{VALIDATION_PATH}`

## Next

{NEXT_TARGET}
"""
    DOC_PATH.write_text(post_doc, encoding="utf-8")


def update_rollups() -> None:
    spine_block = f"""

## 4367 Transition scalar source-normalization gamma/beta fork

Marker: `{MARKER}`

4367 derives the exact scalar fork left open by 4366. If `p_WEP=Delta_w_TiPt tau_WEP` is one common scalar multiplier of the same Hilbert source charge used to define the PPN potential `U`, then the GR metric coefficients are unchanged in terms of the redefined `U`, so `T_gamma_product=T_beta_product=0`. This preserves the Newton/Poisson shape but does not predict numeric `G` or absolute source mass.

If the product is relative/material/source-label/readout data, it cannot be exported into gamma/beta or local GR. It is quarantined as a WEP/source-composition product row. The common scalar premise set is not parent-signed in the current corpus, so no PPN/local-GR claim fires. Next target: `{NEXT_TARGET}`.
"""
    append_once(FORMAL / "07-unification-spine.md", MARKER, spine_block)

    packet_block = f"""

## 4367 packet update: scalar gamma/beta fork

Marker: `{PACKET_MARKER}`

Packet update: the WEP product can leave the WEP box only if it is parent-signed as a common scalar Hilbert-source normalization. On that branch `T_gamma=T_beta=0` because gamma/beta are coefficients relative to the same calibrated PPN potential. If the product is relative to material, source labels, readout or boundary/projector data, it is WEP-only and cannot be used in local GR.
"""
    append_once(FORMAL / "180-PPC4161-private-local-packet-integration.md", PACKET_MARKER, packet_block)

    append_claim_once(
        FORMAL / "02-claims-register.csv",
        CLAIM_ID,
        [
            CLAIM_ID,
            "local_gr",
            "4367 derives the scalar source-normalization fork for the WEP product channel. If p_WEP=Delta_w_TiPt*tau_WEP is a common scalar multiplier of the same Hilbert source charge and Hamiltonian mass used to define the PPN potential U, then gamma and beta are unchanged and T_gamma_product=T_beta_product=0. If p_WEP is relative/material/source-label/readout data, it is quarantined as WEP-only and cannot be exported to local GR. The common scalar premise set is not parent-signed in the current corpus, and other C_src/T_open rows remain live, so no local-GR/Newton/PPN claim fires.",
            "4367 source register, theorem rows, premise audit, gamma/beta transfer rows, WEP-only quarantine, runner, claim gates, decision, status, next target and validation CSV.",
            "scalar_common_source_normalization_gamma_beta_zero_theorem_relative_WEP_product_quarantine_nonclaim",
            "Parent-sign common scalar source normalization or finalize WEP-only quarantine and continue through non-product source coupling rows.",
            "Exporting relative WEP products into local GR; hiding source-label/readout dependence in U; claiming numeric G or full local GR from conditional gamma/beta silence.",
        ],
    )


def main() -> None:
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)
    thresholds = threshold_lookup()
    sources = source_rows()
    theorems = theorem_rows()
    premises = premise_rows()
    transfers = transfer_rows(thresholds)
    quarantines = quarantine_rows()
    runner = runner_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    statuses = status_rows()
    next_targets = next_target_rows()

    write_csv(SOURCE_DIR / "P8_Y5_R2FR_4367_SOURCE_REGISTER.csv", sources)
    write_csv(SOURCE_DIR / "P8_Y5_R2FR_4367_SCALAR_TRANSFER_THEOREM_ROWS.csv", theorems)
    write_csv(SOURCE_DIR / "P8_Y5_R2FR_4367_PREMISE_AUDIT.csv", premises)
    write_csv(SOURCE_DIR / "P8_Y5_R2FR_4367_GAMMA_BETA_TRANSFER_ROWS.csv", transfers)
    write_csv(SOURCE_DIR / "P8_Y5_R2FR_4367_WEP_ONLY_QUARANTINE.csv", quarantines)
    write_csv(SOURCE_DIR / "P8_Y5_R2FR_4367_RUNNER.csv", runner)
    write_csv(SOURCE_DIR / "P8_Y5_R2FR_4367_CLAIM_GATES.csv", gates)
    write_csv(SOURCE_DIR / "P8_Y5_R2FR_4367_DECISION.csv", decisions)
    write_csv(SOURCE_DIR / "P8_Y5_R2FR_4367_STATUS.csv", statuses)
    write_csv(SOURCE_DIR / "P8_Y5_R2FR_4367_NEXT_TARGET.csv", next_targets)

    write_docs(sources, theorems, premises, transfers, quarantines, runner, gates, decisions, statuses, next_targets)
    update_rollups()

    validations = validation_rows(sources, theorems, premises, transfers, quarantines, runner, gates, decisions, statuses, next_targets)
    write_csv(VALIDATION_PATH, validations)
    failed = [row for row in validations if row["passed"] != "True"]
    if failed:
        details = "; ".join(f"{row['check_id']}={row['detail']}" for row in failed)
        raise SystemExit(f"4367 validation failed: {details}")

    print(f"{CHECKPOINT} generated: {DECISION}")
    print(f"formal={FORMAL_PATH}")
    print(f"validation={VALIDATION_PATH}")


if __name__ == "__main__":
    main()
