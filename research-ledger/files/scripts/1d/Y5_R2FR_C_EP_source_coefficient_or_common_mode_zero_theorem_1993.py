from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


BRANCH = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
FORMALIZATION = REPO / "formalization-workbench"
MTS_RESIDUALS = ROOT / "source-intake" / "mts_residuals"
SOURCE_WEIGHT_DOCS = ROOT / "source-intake" / "source-weight" / "docs"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
MICROSCOPE_COEFFS = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "coefficients"

DOC_PATH = ROOT / "1993-Y5-R2FR-C-EP-source-coefficient-or-common-mode-zero-theorem.md"
VALIDATION_PATH = MTS_RESIDUALS / "P8_Y5_BRR545_1993_VALIDATION.csv"

SOURCES = {
    "1992_doc": {
        "path": ROOT / "1992-Y5-R2FR-EP-template-alignment-lemma-or-source-pack-intake.md",
        "needles": ["CEP1992_0_definition", "NEXT1992_0_primary"],
    },
    "1992_validation": {
        "path": MTS_RESIDUALS / "P8_Y5_BRR545_1992_VALIDATION.csv",
        "needles": ["VAL1992_OVERALL", "PASS"],
    },
    "1601_alignment": {
        "path": ROOT / "1601-Y5-R2FR-EP-template-alignment-lemma-or-CMSM-browser-capture.md",
        "needles": ["EPA1601_1_alignment_condition", "MISSING_PARENT_C_EP"],
    },
    "1988_hilbert_action": {
        "path": ROOT / "1988-Y5-R2FR-action-weight-source-beta-theorem-or-finite-row-fill.md",
        "needles": ["THM1988_0_parent_form", "THEOREM_NOT_CLOSED_CURRENT_CORPUS"],
    },
    "1936_universality": {
        "path": ROOT / "1936-Y5-R2FR-source-weight-universality-theorem-or-TiPt-material-charge-ledger.md",
        "needles": ["UNIV1936_1_hilbert_source_theorem", "UNIVERSALITY_NOT_DERIVED"],
    },
    "1440_closure_demote": {
        "path": ROOT / "1440-Y5-R10-RAB-minimal-WEP-parent-clause-proof-obligations-or-closure-demotion.md",
        "needles": ["MPA1440_3_verdict", "DO_NOT_PROMOTE_DEMOTE_TO_CLOSURE_ONLY"],
    },
    "1438_source_pack": {
        "path": ROOT / "1438-Y5-R10-RAB-WEP-slot-C-parent-zero-or-official-source-pack-intake.md",
        "needles": ["CPS1438_0_WEP_C_parent", "PACK1438_0_official_readout"],
    },
}

OUTPUTS = {
    "source_register": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1993_SOURCE_REGISTER.csv",
    "factor_law": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1993_CEP_FACTOR_LAW.csv",
    "zero_theorem": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1993_COMMON_MODE_ZERO_THEOREM_ATTEMPT.csv",
    "nonzero_route": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1993_NONZERO_CEP_ROUTE.csv",
    "charge_slots": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1993_PARENT_CHARGE_SLOT_LEDGER.csv",
    "runner_dryrun": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1993_RUNNER_DRYRUN.csv",
    "claim_gate": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1993_CLAIM_GATE.csv",
    "decision": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1993_DECISION_LEDGER.csv",
    "next": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1993_NEXT_TARGET.csv",
    "source_weight": SOURCE_WEIGHT_DOCS / "C_EP_FACTOR_LAW_1993_NONCLAIM.csv",
    "wep_coeffs": MICROSCOPE_COEFFS / "P8_Y5_PARENT_QLOC_1993_CEP_SOURCE_COEFFICIENT_NONCLAIM.csv",
    "queue": RAB_QUEUE / "JR1993_PARENT_CHARGE_BASIS_OR_HILBERT_OWNER_QUEUE.csv",
}


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def ensure_dirs() -> None:
    for path in OUTPUTS.values():
        path.parent.mkdir(parents=True, exist_ok=True)
    VALIDATION_PATH.parent.mkdir(parents=True, exist_ok=True)


def base_row(stamp: str) -> dict[str, str]:
    return {
        "branch_id": BRANCH,
        "valid_for_claim": "false",
        "claim_allowed": "false",
        "generated_utc": stamp,
    }


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def source_register(stamp: str) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for source_id, spec in SOURCES.items():
        path = spec["path"]
        exists = path.exists()
        text = read_text(path) if exists else ""
        missing = [needle for needle in spec["needles"] if needle not in text]
        row = base_row(stamp)
        row.update(
            {
                "source_id": source_id,
                "source_path": str(path),
                "needed_for": "1993 C_EP source coefficient factor law or common-mode zero theorem",
                "needles": ";".join(spec["needles"]),
                "exists": str(exists),
                "anchor_found": str(exists and not missing),
                "missing_needles": ";".join(missing),
                "status": "EXISTS_NEEDLES_CONFIRMED" if exists and not missing else "MISSING_SOURCE_OR_ANCHOR",
            }
        )
        rows.append(row)
    return rows


def build_tables() -> dict[str, list[dict[str, str]]]:
    stamp = now()

    def row(data: dict[str, str]) -> dict[str, str]:
        merged = base_row(stamp)
        merged.update(data)
        return merged

    factor_law = [
        row(
            {
                "law_id": "CFL1993_0_basis_expansion",
                "statement": "For any finite WEP source-weight residual expanded in parent material/source channels, C_EP = sum_i lambda_i*DeltaQ_i_TiPt*I_i_Earth_EP + C_corr",
                "meaning": "lambda_i is a parent nonmetric/material-charge coupling, DeltaQ_i_TiPt is the Ti/Pt differential charge per inertial mass, and I_i_Earth_EP is the Earth-source/readout EP-template projection",
                "status": "EXACT_FACTOR_BOOKKEEPING_NOT_NUMERIC_CLAIM",
                "claim_blocker": "the channel basis, lambda_i, DeltaQ_i_TiPt, I_i_Earth_EP, and C_corr bound are not parent-sourced",
            }
        ),
        row(
            {
                "law_id": "CFL1993_1_nonzero_condition",
                "statement": "C_EP is nonzero only if at least one lambda_i*DeltaQ_i_TiPt*I_i_Earth_EP term survives and is not cancelled by the remaining sum plus C_corr",
                "meaning": "nonzero factors are not enough; the signed projection and cancellation margin must be controlled",
                "status": "EXACT_SUFFICIENT_CONDITION_FORM",
                "claim_blocker": "no parent-signed nonzero channel or noncancellation margin exists yet",
            }
        ),
        row(
            {
                "law_id": "CFL1993_2_zero_condition",
                "statement": "C_EP is zero if all nonmetric/material-charge lambda_i vanish, or all Ti/Pt DeltaQ_i vanish, or all source/readout I_i vanish, with C_corr also zero or bounded away from reintroduction",
                "meaning": "the clean local-GR route is to prove the parent action forbids the lambda_i slots, not to tune data",
                "status": "EXACT_ZERO_CRITERION_FORM",
                "claim_blocker": "parent action has not yet excluded every lambda_i slot",
            }
        ),
        row(
            {
                "law_id": "CFL1993_3_relation_to_EP_template",
                "statement": "Substituting this factor law into the 1601 inequality makes the EP-template proof depend on C_EP rather than the full CMSM pipeline",
                "meaning": "this is the forward compression: full WEP readout is downstream; the immediate physics question is the parent coupling inventory",
                "status": "ROUTE_COMPRESSED_TO_COUPLING_INVENTORY",
                "claim_blocker": "inventory is not yet signed",
            }
        ),
    ]

    zero_theorem = [
        row(
            {
                "theorem_id": "ZEP1993_0_candidate",
                "candidate": "If ordinary matter descends only through one universal observed metric/coframe and shared matter parameters, with no independent material-charge/source-weight multipliers, then lambda_i=0 for every nonmetric WEP charge channel",
                "would_prove": "C_EP=0 for the finite source-weight WEP branch",
                "current_status": "EXACT_CONDITIONAL_THEOREM",
                "gap": "same parent hypotheses as 1988/1936 remain unsigned in the current corpus",
            }
        ),
        row(
            {
                "theorem_id": "ZEP1993_1_material_blind_variant",
                "candidate": "If MTS permits a finite source residual but it couples only to total inertial/Hilbert source, then DeltaQ_i_TiPt=0 for all allowed channels",
                "would_prove": "C_EP=0 even if a common acceleration/source renormalization exists",
                "current_status": "CONDITIONAL_COMMON_MODE_THEOREM",
                "gap": "requires explicit allowed-channel list from the parent action",
            }
        ),
        row(
            {
                "theorem_id": "ZEP1993_2_failure_mode",
                "candidate": "Any surviving term lambda_i Q_i[species] creates a genuine nonmetric material-charge slot",
                "would_prove": "zero theorem fails and C_EP must be bounded/tested as a WEP/fifth-force coefficient",
                "current_status": "COUNTERMODEL_SURVIVES",
                "gap": "current corpus has not forbidden a symbolic lambda_i Q_i slot by derivation",
            }
        ),
        row(
            {
                "theorem_id": "ZEP1993_3_verdict",
                "candidate": "C_EP=0 by common-mode/source universality",
                "would_prove": "clean local-GR-safe closure of this WEP branch",
                "current_status": "NOT_PARENT_SIGNED_DO_NOT_PROMOTE",
                "gap": "needs parent charge-basis exclusion or explicit universal Hilbert owner proof",
            }
        ),
    ]

    nonzero_route = [
        row(
            {
                "route_id": "NZEP1993_0_required_channel",
                "required_object": "at least one parent channel i with lambda_i, DeltaQ_i_TiPt, and I_i_Earth_EP all nonzero in the same basis",
                "why_required": "this is the minimal way for MTS to predict a finite differential WEP source-weight effect",
                "status": "MISSING_PARENT_CHANNEL",
                "claim_status": "BLOCKED",
            }
        ),
        row(
            {
                "route_id": "NZEP1993_1_non_cancellation",
                "required_object": "signed margin abs(sum_i lambda_i*DeltaQ_i_TiPt*I_i_Earth_EP) > abs(C_corr)",
                "why_required": "orthogonal/cancelling channels can make C_EP zero even when individual ingredients are nonzero",
                "status": "MISSING_MARGIN",
                "claim_status": "BLOCKED",
            }
        ),
        row(
            {
                "route_id": "NZEP1993_2_data_role",
                "required_object": "official source-pack projection can bound C_EP after the parent channel inventory exists",
                "why_required": "data cannot decide which parent slots are legal; it can only bound their projected coefficient",
                "status": "FALLBACK_AFTER_PARENT_INVENTORY",
                "claim_status": "BLOCKED",
            }
        ),
    ]

    charge_slots = [
        row(
            {
                "slot_id": "PCS1993_0_metric_hilbert_slot",
                "slot": "universal Hilbert source",
                "allowed_effect": "common gravitational source/inertial response",
                "C_EP_contribution": "zero for differential Ti/Pt WEP channel if it is the only slot",
                "status": "CONDITIONAL_ALLOWED_UNIVERSAL_SLOT",
            }
        ),
        row(
            {
                "slot_id": "PCS1993_1_species_weight_slot",
                "slot": "w_A(phi) or equivalent species/source multiplier",
                "allowed_effect": "composition-dependent free-fall/source weight",
                "C_EP_contribution": "potentially nonzero",
                "status": "NOT_EXCLUDED_BY_CURRENT_PARENT_CORPUS",
            }
        ),
        row(
            {
                "slot_id": "PCS1993_2_material_charge_slot",
                "slot": "lambda_i Q_i[material] coupled to memory/motion/time/space residual",
                "allowed_effect": "fifth-force-like differential material charge",
                "C_EP_contribution": "potentially nonzero and must be bounded",
                "status": "NO_NUMERIC_OR_DERIVED_ROW",
            }
        ),
        row(
            {
                "slot_id": "PCS1993_3_readout_orthogonal_slot",
                "slot": "source/material residual orthogonal to K_EP",
                "allowed_effect": "physically present but invisible in MICROSCOPE EP template",
                "C_EP_contribution": "zero in this arena",
                "status": "POSSIBLE_BUT_NOT_SOURCE_PACKED",
            }
        ),
    ]

    runner_dryrun = [
        row(
            {
                "run_id": "RUN1993_0_factor_law",
                "check": "derive C_EP product/sum law",
                "result": "PASS_AS_BOOKKEEPING_THEOREM",
                "reason": "projection of any finite source-weight residual onto an EP template decomposes into parent coupling, material contrast, source/readout projection, and correction terms",
            }
        ),
        row(
            {
                "run_id": "RUN1993_1_zero_theorem",
                "check": "prove all nonmetric/material charge slots vanish",
                "result": "FAIL_PARENT_UNSIGNED",
                "reason": "1988 and 1936 give exact conditional Hilbert universality but the parent hypotheses remain unsigned",
            }
        ),
        row(
            {
                "run_id": "RUN1993_2_nonzero_CEP",
                "check": "claim a nonzero C_EP",
                "result": "FAIL_NO_PARENT_CHANNEL",
                "reason": "no lambda_i, DeltaQ_i, source/readout I_i, or noncancellation margin is sourced",
            }
        ),
        row(
            {
                "run_id": "RUN1993_3_route_choice",
                "check": "least-scrutiny route",
                "result": "PREFER_PARENT_CHARGE_BASIS_EXCLUSION",
                "reason": "proving no nonmetric material-charge slot gives the clean local-GR-safe branch; nonzero C_EP route needs heavier WEP bounds",
            }
        ),
        row(
            {
                "run_id": "RUN1993_4_verdict",
                "check": "1993 next-step decision",
                "result": "NEXT_1994_PARENT_CHARGE_BASIS_EXCLUSION_OR_MATERIAL_CHARGE_ROW",
                "reason": "the coupling problem is now reduced to a concrete parent charge-basis inventory",
            }
        ),
    ]

    claim_gate = [
        row(
            {
                "gate_id": "CG1993_0_factor_law",
                "claim": "C_EP factor law is usable as a private proof contract",
                "status": "PASS_NONCLAIM_CONTRACT",
                "reason": "it is algebraic bookkeeping, not a physical coefficient claim",
            }
        ),
        row(
            {
                "gate_id": "CG1993_1_zero_CEP",
                "claim": "C_EP=0",
                "status": "FAIL_BLOCKED",
                "reason": "parent charge-basis exclusion is missing",
            }
        ),
        row(
            {
                "gate_id": "CG1993_2_nonzero_CEP",
                "claim": "C_EP nonzero",
                "status": "FAIL_BLOCKED",
                "reason": "no sourced nonmetric/material channel or noncancellation margin",
            }
        ),
        row(
            {
                "gate_id": "CG1993_3_WEP_score",
                "claim": "WEP/source-pack score can be claimed",
                "status": "FAIL_BLOCKED",
                "reason": "C_EP remains unsigned and official source-pack files are still missing",
            }
        ),
        row(
            {
                "gate_id": "CG1993_4_local_GR_Newton",
                "claim": "local GR/Newton source coupling derived",
                "status": "FAIL_BLOCKED",
                "reason": "requires parent Hilbert owner or charge-basis exclusion theorem",
            }
        ),
    ]

    decision = [
        row(
            {
                "decision_id": "DEC1993_0_forward_progress",
                "decision": "C_EP_IS_NOT_A_MYSTERY_SCALAR_ANYMORE",
                "because": "it decomposes into parent coupling times material contrast times source/readout projection plus corrections",
                "next_action": "audit the parent action for allowed material/source charge slots",
            }
        ),
        row(
            {
                "decision_id": "DEC1993_1_best_route",
                "decision": "TAKE_THE_LOW_SCRUTINY_ZERO_ROUTE_FIRST",
                "because": "excluding nonmetric material-charge slots gives C_EP=0 and makes the WEP branch GR-safe without needing a fragile positive signal",
                "next_action": "prove parent charge-basis exclusion or explicitly admit a material-charge row",
            }
        ),
        row(
            {
                "decision_id": "DEC1993_2_if_zero_route_fails",
                "decision": "NONZERO_ROUTE_BECOMES_A_TESTED_FIFTH_FORCE_STYLE_COUPLING",
                "because": "a surviving lambda_i Q_i slot must face WEP/R10/PPN/clock/orbital bounds",
                "next_action": "source lambda_i, DeltaQ_i, I_i, and correction rows before any claim",
            }
        ),
    ]

    next_target = [
        row(
            {
                "next_id": "NEXT1993_0_primary",
                "selection_status": "selected",
                "target_doc": "1994-Y5-R2FR-parent-charge-basis-exclusion-or-material-charge-row.md",
                "target_script": "scripts/Y5_R2FR_parent_charge_basis_exclusion_or_material_charge_row_1994.py",
                "task": "prove the parent action excludes all nonmetric material/source charge slots, or stage the first explicit material-charge coefficient row as nonclaim",
                "success_condition": "parent-signed exclusion theorem giving C_EP=0, or a fully sourced nonclaim material-charge row with units, source path, and test arenas",
                "do_not": "do not claim WEP/local-GR, infer C_EP from data, hide a species multiplier, or push GitHub",
            }
        )
    ]

    source_weight = [
        row(
            {
                "artifact_id": "SW1993_0_CEP_factor_law",
                "artifact_type": "C_EP_factor_law_nonclaim",
                "status": "FACTOR_LAW_READY_PARENT_CHARGE_BASIS_MISSING",
                "source_path": str(DOC_PATH),
                "next_target": "1994-Y5-R2FR-parent-charge-basis-exclusion-or-material-charge-row.md",
            }
        )
    ]

    wep_coeffs = [
        row(
            {
                "coefficient_id": "WEP1993_0_C_EP_factorized",
                "quantity": "C_EP",
                "required_formula": "C_EP = sum_i lambda_i*DeltaQ_i_TiPt*I_i_Earth_EP + C_corr",
                "required_evidence": "parent charge-basis inventory, lambda_i units, Ti/Pt material charges, Earth source/readout projection, correction bound",
                "current_status": "FACTOR_FORM_ONLY_VALUES_MISSING",
                "status": "NONCLAIM_SLOT_ONLY",
            }
        )
    ]

    queue = [
        row(
            {
                "queue_id": "JR1993_0_parent_charge_basis",
                "priority": "1",
                "needed_input": "parent charge-basis exclusion theorem or first material-charge row",
                "route": "audit the parent matter action/object language for any lambda_i Q_i material/source slots; if none exist, C_EP=0; if one exists, stage it with units and bounds",
                "required_fields": "parent_action_clause;allowed_charge_basis;lambda_i;DeltaQ_i_TiPt;I_i_Earth_EP;C_corr_bound;source_path",
                "blocked_claims": "C_EP_zero;C_EP_nonzero;WEP_pass;local_GR;Newton",
            }
        )
    ]

    return {
        "source_register": source_register(stamp),
        "factor_law": factor_law,
        "zero_theorem": zero_theorem,
        "nonzero_route": nonzero_route,
        "charge_slots": charge_slots,
        "runner_dryrun": runner_dryrun,
        "claim_gate": claim_gate,
        "decision": decision,
        "next": next_target,
        "source_weight": source_weight,
        "wep_coeffs": wep_coeffs,
        "queue": queue,
    }


def validate(tables: dict[str, list[dict[str, str]]]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []

    def val(validation_id: str, status: str, detail: str) -> None:
        rows.append(
            {
                "validation_id": validation_id,
                "status": status,
                "detail": detail,
                "valid_for_claim": "false",
                "claim_allowed": "false",
            }
        )

    source_failures = [row for row in tables["source_register"] if row["status"] != "EXISTS_NEEDLES_CONFIRMED"]
    val("VAL1993_00_sources", "PASS" if not source_failures else "FAIL", "all source paths exist and needles found" if not source_failures else ";".join(row["source_id"] for row in source_failures))

    factor_ready = any(row["law_id"] == "CFL1993_0_basis_expansion" and row["status"] == "EXACT_FACTOR_BOOKKEEPING_NOT_NUMERIC_CLAIM" for row in tables["factor_law"])
    factor_compresses = any(row["law_id"] == "CFL1993_3_relation_to_EP_template" and row["status"] == "ROUTE_COMPRESSED_TO_COUPLING_INVENTORY" for row in tables["factor_law"])
    val("VAL1993_01_factor_law", "PASS" if factor_ready and factor_compresses else "FAIL", "C_EP factor law written as nonclaim route compression")

    zero_not_promoted = any(row["theorem_id"] == "ZEP1993_3_verdict" and row["current_status"] == "NOT_PARENT_SIGNED_DO_NOT_PROMOTE" for row in tables["zero_theorem"])
    val("VAL1993_02_zero_theorem", "PASS" if zero_not_promoted else "FAIL", "common-mode zero theorem not promoted")

    nonzero_blocked = all(row["claim_status"] == "BLOCKED" for row in tables["nonzero_route"])
    val("VAL1993_03_nonzero_route", "PASS" if nonzero_blocked else "FAIL", "nonzero C_EP route explicitly blocked")

    slot_inventory = any(row["slot_id"] == "PCS1993_1_species_weight_slot" and row["status"] == "NOT_EXCLUDED_BY_CURRENT_PARENT_CORPUS" for row in tables["charge_slots"])
    val("VAL1993_04_charge_slots", "PASS" if slot_inventory else "FAIL", "parent charge slots inventoried with species slot still not excluded")

    runner_selects = tables["runner_dryrun"][-1]["result"] == "NEXT_1994_PARENT_CHARGE_BASIS_EXCLUSION_OR_MATERIAL_CHARGE_ROW"
    val("VAL1993_05_runner_decision", "PASS" if runner_selects else "FAIL", "runner selects parent charge-basis target")

    gates_safe = all(row["status"] in {"FAIL_BLOCKED", "PASS_NONCLAIM_CONTRACT"} for row in tables["claim_gate"])
    no_physics_claim = all(row["status"] == "FAIL_BLOCKED" for row in tables["claim_gate"] if row["gate_id"] != "CG1993_0_factor_law")
    val("VAL1993_06_claim_gates", "PASS" if gates_safe and no_physics_claim else "FAIL", "only factor-law contract passes; physics claims blocked")

    next_ok = tables["next"][0]["target_doc"] == "1994-Y5-R2FR-parent-charge-basis-exclusion-or-material-charge-row.md"
    val("VAL1993_07_next_target", "PASS" if next_ok else "FAIL", "1994 parent charge-basis target selected")

    all_rows = [row for rows_for_table in tables.values() for row in rows_for_table]
    flags_safe = all(row.get("valid_for_claim") == "false" and row.get("claim_allowed") == "false" for row in all_rows)
    val("VAL1993_08_claim_flags_safe", "PASS" if flags_safe else "FAIL", "claim flags all false")

    parse_failures = []
    for output_name, path in OUTPUTS.items():
        if not path.exists():
            parse_failures.append(f"{output_name}:missing")
            continue
        with path.open(newline="", encoding="utf-8") as handle:
            parsed = list(csv.DictReader(handle))
        if not parsed:
            parse_failures.append(f"{output_name}:empty")
    val("VAL1993_09_csv_parse", "PASS" if not parse_failures else "FAIL", "all generated CSVs parse with rows" if not parse_failures else ";".join(parse_failures))

    pycache_exists = (ROOT / "scripts" / "__pycache__").exists()
    val("VAL1993_10_pycache_absent", "PASS" if not pycache_exists else "FAIL", "scripts __pycache__ absent")

    formalization_artifacts = []
    checkpoint_markers = ("Y5_R2FR", "P8_Y5", "JR1993", "C_EP", "CEP")
    if FORMALIZATION.exists():
        formalization_artifacts = [
            path
            for path in FORMALIZATION.rglob("*")
            if "1993" in path.name and any(marker in path.name for marker in checkpoint_markers)
        ]
    val("VAL1993_11_formalization_untouched", "PASS" if not formalization_artifacts else "FAIL", f"formalization_1993_artifact_count={len(formalization_artifacts)}")

    overall = "PASS" if all(row["status"] == "PASS" for row in rows) else "FAIL"
    val("VAL1993_OVERALL", overall, "1993 C_EP factor law or common-mode zero theorem")
    return rows


def markdown_table(rows: list[dict[str, str]]) -> str:
    if not rows:
        return ""
    headers = list(rows[0].keys())
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        cells = [str(row.get(header, "")).replace("\n", " ").replace("|", "\\|") for header in headers]
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)


def write_markdown(tables: dict[str, list[dict[str, str]]], validation_rows: list[dict[str, str]]) -> None:
    sections = [
        ("Source Register", tables["source_register"]),
        ("C_EP Factor Law", tables["factor_law"]),
        ("Common-Mode Zero Theorem Attempt", tables["zero_theorem"]),
        ("Nonzero C_EP Route", tables["nonzero_route"]),
        ("Parent Charge Slot Ledger", tables["charge_slots"]),
        ("Runner Dryrun", tables["runner_dryrun"]),
        ("Claim Gate", tables["claim_gate"]),
        ("Decision Ledger", tables["decision"]),
        ("Next Target", tables["next"]),
        ("Validation", validation_rows),
    ]
    lines = [
        "# 1993 Y5 R2FR: C_EP Source Coefficient Or Common-Mode Zero Theorem",
        "",
        "Private checkpoint. This is the leap from 'the coupling is missing' to an exact contract for what the coupling must be.",
        "",
        "Verdict: `C_EP` is no longer just a mystery scalar. Any finite differential WEP source-weight coefficient must factor as `C_EP = sum_i lambda_i*DeltaQ_i_TiPt*I_i_Earth_EP + C_corr`: parent coupling times Ti/Pt material contrast times Earth/readout projection, plus corrections.",
        "",
        "Best route: prove the parent action excludes every nonmetric material/source charge slot. If that closes, `lambda_i=0` for all such slots and the finite WEP branch gives `C_EP=0`, which is the clean local-GR-safe path. If it does not close, MTS has an explicit fifth-force-like material-charge coefficient to source and bound.",
        "",
        "Current status: the factor law is ready as a private proof contract, but neither `C_EP=0` nor `C_EP != 0` is claim-grade. The parent charge-basis inventory is now the next real target.",
        "",
        "No WEP, local-GR, Newton, R10, PPN, clock, orbital, or public claim follows from 1993.",
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
    print(f"VAL1993_OVERALL={overall}")
    return 0 if overall == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
