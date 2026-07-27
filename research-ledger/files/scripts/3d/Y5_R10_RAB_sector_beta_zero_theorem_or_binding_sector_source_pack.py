from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = Path("source-intake/mts_residuals")

DOC_PATH = Path("1395-Y5-R10-RAB-sector-beta-zero-theorem-or-binding-sector-source-pack.md")
SOURCE_REGISTER_PATH = SRC_DIR / "P8_Y5_R10_1395_SOURCE_REGISTER.csv"
ZERO_THEOREM_PATH = SRC_DIR / "P8_Y5_R10_1395_SECTOR_BETA_ZERO_THEOREM_ATTEMPT.csv"
SECTOR_PACK_PATH = SRC_DIR / "P8_Y5_R10_1395_BINDING_SECTOR_BETA_SOURCE_PACK.csv"
ARENA_GATE_PATH = SRC_DIR / "P8_Y5_R10_1395_SECTOR_BETA_ARENA_GATE.csv"
INTERFACE_PATH = SRC_DIR / "P8_Y5_R10_1395_SECTOR_TO_BINDING_INTERFACE_UPDATE.csv"
CLAIM_GATE_PATH = SRC_DIR / "P8_Y5_R10_1395_CLAIM_GATE.csv"
DECISION_LEDGER_PATH = SRC_DIR / "P8_Y5_R10_1395_DECISION_LEDGER.csv"
NEXT_TARGET_PATH = SRC_DIR / "P8_Y5_R10_1395_NEXT_TARGET.csv"
VALIDATION_PATH = SRC_DIR / "P8_Y5_BRR545_1395_VALIDATION.csv"

STATUS = (
    "sector_beta_zero_theorem_attempt_written_"
    "binding_sector_source_pack_nonclaim_local_gates_blocked"
)
CLAIM_CEILING = (
    "sector_beta_zero_attempt_and_source_pack_only_no_beta_e_nuc_EM_zero_no_numeric_binding_beta_"
    "no_R10_no_WEP_no_clock_no_PPN_no_Newton_no_local_GR_pass"
)

SOURCE_ROWS = [
    {
        "source_id": "SRC1395_0_1394_doc",
        "source_path": "1394-Y5-R10-RAB-bulk-binding-inheritance-or-material-composition-map.md",
        "required_anchor": "NEXT1394_0_1395",
        "purpose": "handoff to sector beta zero theorem or source pack",
    },
    {
        "source_id": "SRC1395_1_1394_next",
        "source_path": "source-intake/mts_residuals/P8_Y5_R10_1394_NEXT_TARGET.csv",
        "required_anchor": "NEXT1394_0_1395",
        "purpose": "machine-readable 1395 target",
    },
    {
        "source_id": "SRC1395_2_1394_inheritance",
        "source_path": "source-intake/mts_residuals/P8_Y5_R10_1394_BINDING_INHERITANCE_PROOF_ATTEMPT.csv",
        "required_anchor": "BIH1394_4_zero_condition",
        "purpose": "binding zero requires sector beta zero",
    },
    {
        "source_id": "SRC1395_3_1394_binding_rows",
        "source_path": "source-intake/mts_residuals/P8_Y5_R10_1394_BINDING_BETA_COEFFICIENT_ROWS.csv",
        "required_anchor": "BBR1394_2_beta_EM",
        "purpose": "sector beta rows to refine",
    },
    {
        "source_id": "SRC1395_4_1394_composition",
        "source_path": "source-intake/mts_residuals/P8_Y5_R10_1394_BULK_MATERIAL_COMPOSITION_MAP.csv",
        "required_anchor": "MCM1394_6_composition_verdict",
        "purpose": "composition rows depend on sector beta values",
    },
    {
        "source_id": "SRC1395_5_987_doc",
        "source_path": "987-Y5-R10-Coulomb-to-alphaEM-normal-form-or-parent-zero-gate.md",
        "required_anchor": "EMNF987_4_verdict",
        "purpose": "Coulomb/alpha_EM finite route remains unsigned",
    },
    {
        "source_id": "SRC1395_6_988_doc",
        "source_path": "988-Y5-R10-alphaEM-WEP-clock-joint-prior-or-EM-lock-theorem.md",
        "required_anchor": "EMLOCK988_5_theorem_verdict",
        "purpose": "EM-lock theorem is conditional but not promoted",
    },
    {
        "source_id": "SRC1395_7_989_doc",
        "source_path": "989-Y5-R10-EM-lock-signature-input-or-alpha-source-normalization-owner.md",
        "required_anchor": "ELA989_5_total",
        "purpose": "EM-lock signature audit blocks promotion",
    },
    {
        "source_id": "SRC1395_8_988_joint_alpha",
        "source_path": "source-intake/mts_residuals/P8_Y5_R10_988_JOINT_ALPHA_VARIABLE_GATE.csv",
        "required_anchor": "JAV988_1_clock_product",
        "purpose": "clock/alpha source pressure remains nonclaim",
    },
    {
        "source_id": "SRC1395_9_989_beta_owner",
        "source_path": "source-intake/mts_residuals/P8_Y5_R10_989_BETA_SOURCE_OWNER_LEDGER.csv",
        "required_anchor": "BSO989_4_failure_action",
        "purpose": "finite alpha/source beta remains closure-only if unowned",
    },
    {
        "source_id": "SRC1395_10_1393_beta_rows",
        "source_path": "source-intake/mts_residuals/P8_Y5_R10_1393_BETA_BULK_SOURCE_TEST_COEFFICIENT_ROWS.csv",
        "required_anchor": "BBS1393_8_beta_verdict",
        "purpose": "sector pack feeds beta_bulk source/test rows",
    },
    {
        "source_id": "SRC1395_11_this_script",
        "source_path": "scripts/Y5_R10_RAB_sector_beta_zero_theorem_or_binding_sector_source_pack.py",
        "required_anchor": "STATUS",
        "purpose": "1395 generator",
    },
]


def clean(value: Any) -> str:
    return str(value).replace("\n", " ").strip()


def write_csv(path: Path, rows: list[dict[str, Any]], columns: list[str] | None = None) -> None:
    full_path = ROOT / path
    full_path.parent.mkdir(parents=True, exist_ok=True)
    if columns is None:
        columns = list(rows[0].keys()) if rows else []
    with full_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns)
        writer.writeheader()
        for row in rows:
            writer.writerow({column: clean(row.get(column, "")) for column in columns})


def md_table(rows: list[dict[str, Any]], columns: list[str] | None = None) -> str:
    if not rows:
        return ""
    if columns is None:
        columns = list(rows[0].keys())
    header = "| " + " | ".join(columns) + " |"
    divider = "| " + " | ".join("---" for _ in columns) + " |"
    body = [
        "| " + " | ".join(clean(row.get(column, "")).replace("|", "\\|") for column in columns) + " |"
        for row in rows
    ]
    return "\n".join([header, divider, *body])


def anchor_found(path: Path, anchor: str) -> bool:
    if not path.exists():
        return False
    return anchor in path.read_text(encoding="utf-8", errors="ignore")


def source_register_rows() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for source in SOURCE_ROWS:
        source_path = ROOT / source["source_path"]
        rows.append(
            {
                **source,
                "exists": str(source_path.exists()),
                "anchor_found": str(anchor_found(source_path, source["required_anchor"])),
                "valid_for_claim": "False",
                "claim_allowed": "False",
            }
        )
    return rows


def zero_theorem_rows() -> list[dict[str, str]]:
    return [
        {
            "zero_id": "SBZ1395_0_electronic_zero",
            "sector": "electronic_atomic",
            "target": "beta_e=0",
            "attempted_derivation": "electronic/atomic masses and clock standards inherit the common matter owner and have no independent readout marker",
            "result": "CONDITIONAL_ZERO_ROUTE",
            "gap": "electron mass/readout/clock sector ownership is not parent-signed in the current corpus",
            "if_unsigned": "retain beta_e row and clock/WEP/R10 hooks",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "zero_id": "SBZ1395_1_nuclear_zero",
            "sector": "nuclear_binding",
            "target": "beta_nuc=0",
            "attempted_derivation": "nuclear binding and composite rest mass inherit the ordinary-matter action owner without independent source-normalization marker",
            "result": "CONDITIONAL_ZERO_ROUTE",
            "gap": "QCD/nuclear binding owner and composition response are not parent-signed",
            "if_unsigned": "retain beta_nuc row and WEP/orbital/R10 hooks",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "zero_id": "SBZ1395_2_EM_zero",
            "sector": "EM_binding",
            "target": "beta_EM=0",
            "attempted_derivation": "EM-lock theorem fixes charge generator, Maxwell normalization, current owner, alpha readout, and no-alpha vertex",
            "result": "CONDITIONAL_ZERO_ROUTE_WITH_ACTIVE_BLOCKERS",
            "gap": "EM-lock clauses from 988/989 remain unsigned; unique Maxwell F2/current/readout/no-alpha signatures are not closed",
            "if_unsigned": "retain beta_EM row and alpha_EM/WEP/clock hooks",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "zero_id": "SBZ1395_3_joint_binding_zero",
            "sector": "binding_sum",
            "target": "beta_bind,A=0 for source and test",
            "attempted_derivation": "if beta_e=beta_nuc=beta_EM=0, then beta_bind,A=sum_i f_i,A beta_i=0 for all compositions",
            "result": "EXACT_CONDITIONAL_SUM_ZERO",
            "gap": "sector beta zeros are unsigned",
            "if_unsigned": "composition-weighted binding row remains active",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "zero_id": "SBZ1395_4_no_cancellation_credit",
            "sector": "binding_sum",
            "target": "composition cancellation is not evidence",
            "attempted_derivation": "do not set beta_bind,A=0 by fitted cancellation among f_i beta_i unless a parent theorem forces cancellation for every source/test composition",
            "result": "CANCELLATION_GUARD_ACTIVE",
            "gap": "none for guard; values and theorem remain missing",
            "if_unsigned": "keep individual sector rows instead of one tuned beta_bind",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "zero_id": "SBZ1395_5_current_verdict",
            "sector": "all_binding_sectors",
            "target": "sector beta zero claim status",
            "attempted_derivation": "compare 1394 binding inheritance, 987/988/989 EM-lock files, and beta/source rows",
            "result": "SECTOR_BETA_ZERO_NOT_SIGNED_SOURCE_PACK_REQUIRED",
            "gap": "electronic, nuclear, and EM sector owners are not all signed; EM-lock has explicit active blockers",
            "if_unsigned": "create nonclaim sector-beta source pack",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def sector_pack_rows() -> list[dict[str, str]]:
    return [
        {
            "sector_id": "SBP1395_0_beta_e",
            "coefficient": "beta_e",
            "sector": "electronic_atomic",
            "definition": "canonical phi_c derivative of electronic/atomic contribution to observed bulk mass and clock standards",
            "feeds": "beta_bind,A via f_e,A beta_e; clocks/constants; WEP material contrast; R10 material leg",
            "required_provenance": "electronic sector owner theorem, clock/readout descent, or sourced beta_e bound",
            "current_value": "MISSING",
            "current_status": "MISSING_ELECTRONIC_SECTOR_BETA_ZERO_OR_BOUND",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "sector_id": "SBP1395_1_beta_nuc",
            "coefficient": "beta_nuc",
            "sector": "nuclear_binding",
            "definition": "canonical phi_c derivative of nuclear binding/composite rest-mass contribution",
            "feeds": "beta_bind,A via f_nuc,A beta_nuc; WEP material contrast; orbital/self-energy residuals; R10 material leg",
            "required_provenance": "nuclear/QCD binding owner theorem or sourced beta_nuc bound",
            "current_value": "MISSING",
            "current_status": "MISSING_NUCLEAR_SECTOR_BETA_ZERO_OR_BOUND",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "sector_id": "SBP1395_2_beta_EM",
            "coefficient": "beta_EM",
            "sector": "EM_binding",
            "definition": "canonical phi_c derivative of EM binding/charge/fine-structure contribution",
            "feeds": "beta_bind,A via f_EM,A beta_EM; alpha_EM/clock; Coulomb WEP; R10 material leg",
            "required_provenance": "EM-lock theorem, alpha_EM readout descent, no-alpha vertex, or sourced WEP/clock bound",
            "current_value": "MISSING",
            "current_status": "MISSING_EM_SECTOR_BETA_ZERO_OR_BOUND",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "sector_id": "SBP1395_3_beta_other_guard",
            "coefficient": "beta_other",
            "sector": "other_binding_or_readout",
            "definition": "placeholder guard for any binding/readout sector not covered by e/nuc/EM",
            "feeds": "beta_bind,A residual envelope if sector inventory is incomplete",
            "required_provenance": "proof sector inventory is complete or conservative residual envelope",
            "current_value": "MISSING",
            "current_status": "MISSING_SECTOR_COMPLETENESS_OR_RESIDUAL_ENVELOPE",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "sector_id": "SBP1395_4_sector_vector",
            "coefficient": "beta_sector_vector",
            "sector": "sector_vector",
            "definition": "(beta_e, beta_nuc, beta_EM, beta_other)",
            "feeds": "composition map MCM1394 rows and binding beta pack BBR1394",
            "required_provenance": "each component theorem-zero or source-backed with units and source paths",
            "current_value": "MISSING",
            "current_status": "SECTOR_VECTOR_READY_NONCLAIM",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "sector_id": "SBP1395_5_pack_verdict",
            "coefficient": "binding sector beta source pack",
            "sector": "all_binding_sectors",
            "definition": "sector beta rows are explicit but not value-filled",
            "feeds": "beta_bind,S/T, beta_bulk,S/T, R10 alpha template, WEP/clock/local gates",
            "required_provenance": "SBP1395_0 through SBP1395_4 complete without MISSING markers",
            "current_value": "MISSING",
            "current_status": "BINDING_SECTOR_SOURCE_PACK_READY_NONCLAIM",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
    ]


def arena_gate_rows() -> list[dict[str, str]]:
    return [
        {
            "arena_id": "SBA1395_0_R10",
            "arena": "R10 alpha(lambda)",
            "sector_dependency": "beta_bind,S/T feed beta_bulk,S/T and then alpha_bulk,ST(lambda)",
            "required_to_score": "sector betas and composition fractions theorem-zero or source-backed; K/tail/full bound curve also real",
            "current_status": "BLOCKED_SECTOR_BETAS_MISSING",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "arena_id": "SBA1395_1_WEP",
            "arena": "WEP/material contrast",
            "sector_dependency": "different f_i,A values make beta_e/beta_nuc/beta_EM composition-sensitive",
            "required_to_score": "composition map plus sector beta vector or theorem-zero",
            "current_status": "BLOCKED_COMPOSITION_SECTOR_INPUTS_MISSING",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "arena_id": "SBA1395_2_clocks",
            "arena": "clocks/fine-structure",
            "sector_dependency": "beta_e and beta_EM can move atomic/EM readouts and alpha_EM channels",
            "required_to_score": "clock readout descent, alpha_EM lock, or sourced clock/WEP beta bounds",
            "current_status": "BLOCKED_EM_ELECTRONIC_LOCK_UNSIGNED",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "arena_id": "SBA1395_3_PPN_orbital",
            "arena": "PPN/orbital/source mass",
            "sector_dependency": "beta_nuc and beta_EM alter observed source mass and composition-dependent source charge",
            "required_to_score": "source-mass/readout map and sector beta bounds",
            "current_status": "BLOCKED_SOURCE_MASS_SECTOR_INPUTS_MISSING",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "arena_id": "SBA1395_4_local_GR",
            "arena": "local GR/Newton reduction",
            "sector_dependency": "local matter source universality fails if sector betas survive without bounds",
            "required_to_score": "all sector betas theorem-zero or complete finite residual vector below local bounds",
            "current_status": "BLOCKED_NO_LOCAL_GR_CLAIM",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def interface_rows() -> list[dict[str, str]]:
    return [
        {
            "interface_id": "STB1395_0_to_composition",
            "target": "MCM1394 composition rows",
            "dependency": "beta_e, beta_nuc, beta_EM",
            "effect": "composition rows cannot become scoreable until sector betas are zero/source-backed",
            "current_status": "COMPOSITION_PROMOTION_BLOCKED",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "interface_id": "STB1395_1_to_binding",
            "target": "BBR1394 beta_bind,S/T rows",
            "dependency": "sector beta vector and source/test fractions",
            "effect": "beta_bind,A=sum_i f_i,A beta_i remains formula-only",
            "current_status": "BINDING_PROMOTION_BLOCKED",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "interface_id": "STB1395_2_to_beta_bulk",
            "target": "BBS1393 beta_bulk,S/T rows",
            "dependency": "beta_bind,S/T plus common/action-weight beta pieces",
            "effect": "beta_bulk rows remain missing and cannot promote the R10 template",
            "current_status": "BETA_BULK_PROMOTION_BLOCKED",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "interface_id": "STB1395_3_to_EM_lock",
            "target": "EM-lock route",
            "dependency": "beta_EM",
            "effect": "if EM-lock closes, beta_EM can be zero-certified; until then EM/clock/WEP gates remain active",
            "current_status": "EM_LOCK_ROUTE_RETAINED_UNSIGNED",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "interface_id": "STB1395_4_verdict",
            "target": "sector beta to binding interface",
            "dependency": "all sector beta rows",
            "effect": "sector pack must close before binding/bulk/R10/local promotion",
            "current_status": "SECTOR_TO_BINDING_INTERFACE_READY_SCORING_BLOCKED",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def claim_gate_rows() -> list[dict[str, str]]:
    return [
        {
            "gate_id": "GATE1395_0_sources",
            "gate": "all cited local sources exist and anchors are present",
            "status": "PASS",
            "reason": "source register validates against local corpus and prior EM-lock/binding files",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "gate_id": "GATE1395_1_sector_zero",
            "gate": "beta_e, beta_nuc, and beta_EM are theorem-zero",
            "status": "BLOCKED_PARENT_UNSIGNED",
            "reason": "sector ownership/descent clauses are unsigned; EM-lock has active blockers",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "gate_id": "GATE1395_2_source_pack",
            "gate": "binding sector beta source pack exists",
            "status": "PASS_NONCLAIM_PACK",
            "reason": "sector beta rows are explicit but all values/provenance remain missing",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "gate_id": "GATE1395_3_binding_promotion",
            "gate": "sector rows can promote beta_bind and beta_bulk",
            "status": "BLOCKED_VALUES_MISSING",
            "reason": "sector betas and composition fractions are not source-backed or zero-certified",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "gate_id": "GATE1395_4_empirical_scores",
            "gate": "R10/WEP/clock/PPN scores may be reported",
            "status": "BLOCKED_SECTOR_INPUTS_MISSING",
            "reason": "sector beta vector is missing and EM-lock is not signed",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "gate_id": "GATE1395_5_local_claim",
            "gate": "local GR/Newton reduction can be claimed",
            "status": "BLOCKED_NO_CLAIM",
            "reason": "1395 is a sector-beta source pack, not a derived local GR limit",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
    ]


def decision_rows() -> list[dict[str, str]]:
    return [
        {
            "decision_id": "DEC1395_0_zero_status",
            "decision": "sector beta zero remains conditional",
            "because": "electronic, nuclear, and EM sector owner/descent theorems are not signed",
            "next_action": "keep sector beta rows explicit and nonclaim",
            "claim_allowed": "False",
        },
        {
            "decision_id": "DEC1395_1_EM_priority",
            "decision": "EM beta is the sharpest next sector",
            "because": "EM-lock already has a detailed clause audit and couples to alpha_EM, clocks, WEP, and R10",
            "next_action": "return to EM-lock signature repair or create a beta_EM source-bound template",
            "claim_allowed": "False",
        },
        {
            "decision_id": "DEC1395_2_no_scores",
            "decision": "do not run empirical scores from sector beta rows yet",
            "because": "all sector beta values are missing and no zero certificate is signed",
            "next_action": "1396 should choose EM-lock repair or finite beta_EM source-bound path",
            "claim_allowed": "False",
        },
    ]


def next_target_rows() -> list[dict[str, str]]:
    return [
        {
            "next_id": "NEXT1395_0_1396",
            "next_doc": "1396-Y5-R10-RAB-beta-EM-lock-repair-or-finite-alphaEM-source-bound.md",
            "next_script": "scripts/Y5_R10_RAB_beta_EM_lock_repair_or_finite_alphaEM_source_bound.py",
            "task": "try to close the EM-lock clauses for beta_EM=0, or create a finite beta_EM source-bound template tied to alpha_EM/WEP/clock gates",
            "success_condition": "beta_EM is either theorem-zero under signed EM-lock premises or a strict nonclaim source-bound row with alpha_EM, WEP, clock, R10, and local-GR refusal gates",
            "do_not_claim": "local GR;Newton limit;PPN pass;R10 pass;WEP pass;clock pass;q_loc=0;numeric alpha(lambda);GitHub-ready result",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        }
    ]


def csv_rows(path: Path) -> list[dict[str, str]]:
    with (ROOT / path).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def validation_rows(
    sources: list[dict[str, str]],
    zero: list[dict[str, str]],
    pack: list[dict[str, str]],
    arenas: list[dict[str, str]],
    interface: list[dict[str, str]],
    gates: list[dict[str, str]],
) -> list[dict[str, str]]:
    source_pass = all(row["exists"] == "True" and row["anchor_found"] == "True" for row in sources)
    joint_zero = any(
        row["zero_id"] == "SBZ1395_3_joint_binding_zero"
        and row["result"] == "EXACT_CONDITIONAL_SUM_ZERO"
        and row["valid_for_claim"] == "False"
        for row in zero
    )
    zero_blocked = any(
        row["zero_id"] == "SBZ1395_5_current_verdict"
        and row["result"] == "SECTOR_BETA_ZERO_NOT_SIGNED_SOURCE_PACK_REQUIRED"
        and row["claim_allowed"] == "False"
        for row in zero
    )
    pack_ready = any(
        row["sector_id"] == "SBP1395_5_pack_verdict"
        and row["current_status"] == "BINDING_SECTOR_SOURCE_PACK_READY_NONCLAIM"
        and row["claim_allowed"] == "False"
        for row in pack
    )
    no_values = all(row["current_value"] == "MISSING" for row in pack)
    all_nonclaim = all(row["valid_for_claim"] == "False" and row["claim_allowed"] == "False" for row in pack)
    arenas_blocked = all(row["current_status"].startswith("BLOCKED") for row in arenas)
    interface_blocked = any(
        row["interface_id"] == "STB1395_4_verdict"
        and row["current_status"] == "SECTOR_TO_BINDING_INTERFACE_READY_SCORING_BLOCKED"
        and row["claim_allowed"] == "False"
        for row in interface
    )
    local_claim_blocked = any(
        row["gate_id"] == "GATE1395_5_local_claim"
        and row["status"] == "BLOCKED_NO_CLAIM"
        and row["claim_allowed"] == "False"
        for row in gates
    )
    prior_1394 = csv_rows(SRC_DIR / "P8_Y5_R10_1394_CLAIM_GATE.csv")
    prior_local_blocked = any(
        row["gate_id"] == "GATE1394_5_local_claim" and row["status"] == "BLOCKED_NO_CLAIM"
        for row in prior_1394
    )
    outputs = [
        DOC_PATH,
        SOURCE_REGISTER_PATH,
        ZERO_THEOREM_PATH,
        SECTOR_PACK_PATH,
        ARENA_GATE_PATH,
        INTERFACE_PATH,
        CLAIM_GATE_PATH,
        DECISION_LEDGER_PATH,
        NEXT_TARGET_PATH,
        VALIDATION_PATH,
        Path("scripts/Y5_R10_RAB_sector_beta_zero_theorem_or_binding_sector_source_pack.py"),
    ]
    formalization_touched = any("formalization-workbench" in str((ROOT / output).resolve()) for output in outputs)
    scope_ok = all((ROOT / output).resolve().is_relative_to(ROOT.resolve()) for output in outputs) and not formalization_touched
    overall = (
        source_pass
        and joint_zero
        and zero_blocked
        and pack_ready
        and no_values
        and all_nonclaim
        and arenas_blocked
        and interface_blocked
        and local_claim_blocked
        and prior_local_blocked
        and scope_ok
    )
    return [
        {
            "validation_id": "VAL1395_0_sources",
            "check": "every cited local source path exists and anchor is found",
            "status": "PASS" if source_pass else "FAIL",
            "details": "; ".join(
                f"{row['source_id']} exists={row['exists']} anchor={row['anchor_found']}" for row in sources
            ),
        },
        {
            "validation_id": "VAL1395_1_zero_refusal",
            "check": "sector beta zero theorem is exact conditional but unsigned",
            "status": "PASS" if joint_zero and zero_blocked else "FAIL",
            "details": "SBZ1395_3 records the conditional sum zero; SBZ1395_5 keeps sector zero unsigned.",
        },
        {
            "validation_id": "VAL1395_2_sector_pack",
            "check": "binding sector beta source pack is explicit and nonclaim",
            "status": "PASS" if pack_ready and no_values and all_nonclaim else "FAIL",
            "details": f"sector_rows={len(pack)}; all_values_missing={no_values}; all_nonclaim={all_nonclaim}",
        },
        {
            "validation_id": "VAL1395_3_arena_interface",
            "check": "sector betas retain R10/WEP/clock/local gates",
            "status": "PASS" if arenas_blocked and interface_blocked else "FAIL",
            "details": "SBA1395 rows block arenas and STB1395_4 blocks binding promotion.",
        },
        {
            "validation_id": "VAL1395_4_claim_refusal",
            "check": "empirical and local claims remain blocked",
            "status": "PASS" if local_claim_blocked and prior_local_blocked else "FAIL",
            "details": "GATE1395_5 and prior GATE1394_5 both block local GR/Newton promotion.",
        },
        {
            "validation_id": "VAL1395_5_scope",
            "check": "generated outputs stay inside post-checkpoint-work and outside formalization-workbench",
            "status": "PASS" if scope_ok else "FAIL",
            "details": f"ROOT={ROOT}; output_count={len(outputs)}; formalization_touched={formalization_touched}",
        },
        {
            "validation_id": "VAL1395_6_overall",
            "check": "overall 1395 validation",
            "status": "PASS" if overall else "FAIL",
            "details": "1395 writes sector beta zero conditions and nonclaim sector source rows without enabling R10/WEP/clock/local scoring.",
        },
    ]


def write_doc(
    sources: list[dict[str, str]],
    zero: list[dict[str, str]],
    pack: list[dict[str, str]],
    arenas: list[dict[str, str]],
    interface: list[dict[str, str]],
    gates: list[dict[str, str]],
    decisions: list[dict[str, str]],
    next_target: list[dict[str, str]],
    validation: list[dict[str, str]],
) -> None:
    generated = datetime.now(timezone.utc).isoformat()
    body = f"""# 1395 - Y5 R10 RAB Sector Beta Zero Theorem Or Binding Sector Source Pack

**Generated:** {generated}

**Current verdict:** sector beta zero is clean only as a conditional theorem. If `beta_e=beta_nuc=beta_EM=0`, then binding beta vanishes for every composition, but the electronic, nuclear, and EM sector zero clauses are not parent-signed.

**Discipline move:** keep `beta_e`, `beta_nuc`, and `beta_EM` as explicit nonclaim source rows. `beta_EM` is especially dangerous because the EM-lock route is still unsigned and it couples simultaneously to alpha_EM, clocks, WEP, R10, and local-GR gates.

**Claim ceiling:** {CLAIM_CEILING}

## Source Register

{md_table(sources)}

## Sector Beta Zero Theorem Attempt

{md_table(zero)}

## Binding Sector Beta Source Pack

{md_table(pack)}

## Sector Beta Arena Gate

{md_table(arenas)}

## Sector-to-Binding Interface Update

{md_table(interface)}

## Claim Gates

{md_table(gates)}

## Decision Ledger

{md_table(decisions)}

## Next Target

{md_table(next_target)}

## Validation

{md_table(validation)}
"""
    (ROOT / DOC_PATH).write_text(body, encoding="utf-8")


def main() -> None:
    sources = source_register_rows()
    zero = zero_theorem_rows()
    pack = sector_pack_rows()
    arenas = arena_gate_rows()
    interface = interface_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_target = next_target_rows()
    validation = validation_rows(sources, zero, pack, arenas, interface, gates)

    write_csv(SOURCE_REGISTER_PATH, sources)
    write_csv(ZERO_THEOREM_PATH, zero)
    write_csv(SECTOR_PACK_PATH, pack)
    write_csv(ARENA_GATE_PATH, arenas)
    write_csv(INTERFACE_PATH, interface)
    write_csv(CLAIM_GATE_PATH, gates)
    write_csv(DECISION_LEDGER_PATH, decisions)
    write_csv(NEXT_TARGET_PATH, next_target)
    write_csv(VALIDATION_PATH, validation)
    write_doc(sources, zero, pack, arenas, interface, gates, decisions, next_target, validation)

    failed = [row for row in validation if row["status"] != "PASS"]
    if failed:
        raise SystemExit(f"1395 validation failed: {failed}")
    print(STATUS)
    print(ROOT / DOC_PATH)
    print(ROOT / VALIDATION_PATH)


if __name__ == "__main__":
    main()
