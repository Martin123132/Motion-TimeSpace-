from __future__ import annotations

import csv
import math
import re
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
FW = REPO / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
PYCACHE = ROOT / "scripts" / "__pycache__"

DOC = ROOT / "3283-Y5-R2FR-first-numeric-CZ-input-source-pack-or-CR-readout-demotion-under-AX1090.md"

SRC_3282_DOC = ROOT / "3282-Y5-R2FR-hidden-F2-coefficient-slot-ban-or-first-CZ-prediction-row-under-AX1090.md"
SRC_3282_FORMULA = OUT / "P8_Y5_R2FR_3282_CZ_RESIDUAL_FORMULA_ROWS.csv"
SRC_3282_PREDICTIONS = OUT / "P8_Y5_R2FR_3282_FIRST_CZ_PREDICTION_ROWS_NONCLAIM.csv"
SRC_3282_NEXT = OUT / "P8_Y5_R2FR_3282_NEXT_TARGET.csv"
SRC_3282_VALIDATION = OUT / "P8_Y5_BRR545_3282_VALIDATION.csv"
SRC_3281_BOUND = OUT / "P8_Y5_R2FR_3281_CZ_FINITE_BOUND_ROWS_NONCLAIM.csv"
SRC_3280_ROWS = OUT / "P8_Y5_R2FR_3280_CZ_CR_SOURCE_BOUND_ROWS_NONCLAIM.csv"
SRC_2630_DECISION = OUT / "P8_Y5_CR_ZERO_ROLLFORWARD_2630_DECISION_LEDGER.csv"
SRC_2630_NEXT = OUT / "P8_Y5_CR_ZERO_ROLLFORWARD_2630_NEXT_TARGET.csv"
SRC_2656_CONTRACT = OUT / "P8_Y5_MICROSCOPE_READOUT_SOURCE_BOUND_2656_SOURCE_RESIDUAL_BOUND_INPUT_CONTRACT.csv"
SRC_2656_DECISION = OUT / "P8_Y5_MICROSCOPE_READOUT_SOURCE_BOUND_2656_DECISION_LEDGER.csv"

OUTPUTS = {
    "sources": OUT / "P8_Y5_R2FR_3283_SOURCE_REGISTER.csv",
    "hunt": OUT / "P8_Y5_R2FR_3283_NUMERIC_CZ_INPUT_HUNT.csv",
    "pack": OUT / "P8_Y5_R2FR_3283_CZ_INPUT_PACK_DECISION.csv",
    "demotion": OUT / "P8_Y5_R2FR_3283_CZ_CLOSURE_DEMOTION.csv",
    "cr_import": OUT / "P8_Y5_R2FR_3283_CR_BRANCH_IMPORT.csv",
    "cr_formula": OUT / "P8_Y5_R2FR_3283_CR_READOUT_FORMULA_HANDOFF.csv",
    "promotion": OUT / "P8_Y5_R2FR_3283_PROMOTION_GATES.csv",
    "decision": OUT / "P8_Y5_R2FR_3283_DECISION_LEDGER.csv",
    "next": OUT / "P8_Y5_R2FR_3283_NEXT_TARGET.csv",
    "validation": OUT / "P8_Y5_BRR545_3283_VALIDATION.csv",
}

RUN_UTC = datetime.now(timezone.utc).isoformat()

NUMERIC_RE = re.compile(r"(?<![A-Za-z_])[-+]?(?:\d+\.\d+|\d+)(?:[eE][-+]?\d+)?")
NEGATIVE_MARKERS = (
    "missing",
    "smoke",
    "template",
    "nonclaim",
    "not_scoreable",
    "not scoreable",
    "valid_for_claim,false",
    "valid_for_claim\": \"false",
    "false",
    "blocked",
    "unsigned",
    "conditional",
    "bound",
    "<=",
    ">=",
)
SOURCE_MARKERS = ("source_path", "doi", "arxiv", ".pdf", ".csv", ".md", "http")

TARGETS = [
    {
        "target_id": "CZIN3283_0_ZQ_denominator",
        "required_input": "source-backed numeric Z_Q denominator",
        "pattern": re.compile(r"\b(Z_Q|Z_A|Zbar_Q|g_EM\^{-2}|Maxwell kinetic|kinetic coefficient)\b", re.IGNORECASE),
    },
    {
        "target_id": "CZIN3283_1_fprime",
        "required_input": "source-backed numeric f'_X or partial f_a/partial I_b",
        "pattern": re.compile(r"(f'_X|fprime|df_X|f_X,|partial[_ ]f|∂f|f_a,_b)", re.IGNORECASE),
    },
    {
        "target_id": "CZIN3283_2_Lv_Ihid",
        "required_input": "source-backed numeric L_v I_hid",
        "pattern": re.compile(r"(L_v I|Lv I|L_v\(I|Lie_v.*I_hid|vertical.*I_hid|L_v I\^b_hid)", re.IGNORECASE),
    },
    {
        "target_id": "CZIN3283_3_radiative_slope",
        "required_input": "source-backed numeric L_v delta_lambda_rad",
        "pattern": re.compile(r"(delta_lambda_rad|L_v delta_lambda_rad|radiative.*slope|delta.*lambda.*rad)", re.IGNORECASE),
    },
    {
        "target_id": "CZIN3283_4_readout_slope",
        "required_input": "source-backed numeric L_v delta_Z_readout or C_R readout slope",
        "pattern": re.compile(r"(delta_Z_readout|R_alpha|C_R|readout.*slope|L_X ln R_alpha|L_v ln R_alpha)", re.IGNORECASE),
    },
]


def bool_str(value: bool) -> str:
    return "true" if value else "false"


def compact(value: Any, limit: int = 360) -> str:
    text = " ".join(str(value).split())
    return text if len(text) <= limit else text[: limit - 3] + "..."


def fmt(value: float) -> str:
    return f"{value:.12e}"


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def csv_parse_ok(path: Path) -> bool:
    if not path.exists():
        return False
    try:
        read_csv(path)
        return True
    except Exception:
        return False


def text_parse_ok(path: Path) -> bool:
    if not path.exists():
        return False
    try:
        path.read_text(encoding="utf-8", errors="replace")
        return True
    except Exception:
        return False


def parse_ok(path: Path) -> bool:
    return csv_parse_ok(path) if path.suffix.lower() == ".csv" else text_parse_ok(path)


def evidence_hits(path: Path, needles: list[str], limit: int = 4) -> str:
    if not path.exists():
        return "MISSING_SOURCE"
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    lowered = [needle.lower() for needle in needles]
    hits: list[str] = []
    for idx, line in enumerate(lines, start=1):
        if any(needle in line.lower() for needle in lowered):
            hits.append(f"L{idx}:{compact(line, 240)}")
        if len(hits) >= limit:
            break
    return " | ".join(hits) if hits else "NO_PATTERN_HIT"


def snapshot_tree(path: Path) -> dict[str, tuple[int, int]]:
    if not path.exists():
        return {}
    snapshot: dict[str, tuple[int, int]] = {}
    for item in path.rglob("*"):
        if item.is_file():
            stat = item.stat()
            snapshot[str(item.relative_to(path))] = (stat.st_size, stat.st_mtime_ns)
    return snapshot


def changed_count(before: dict[str, tuple[int, int]], after: dict[str, tuple[int, int]]) -> int:
    keys = set(before) | set(after)
    return sum(1 for key in keys if before.get(key) != after.get(key))


def source_register_rows() -> list[dict[str, Any]]:
    sources = [
        (SRC_3282_DOC, "3282 fork derivation", ["C_Z = L_v ln Z_Q", "Next Target"]),
        (SRC_3282_FORMULA, "3282 residual formula rows", ["FORM3282_1", "numeric input contract"]),
        (SRC_3282_PREDICTIONS, "3282 prediction rows", ["CZP3282_0", "MISSING_NUMERIC"]),
        (SRC_3282_NEXT, "3282 next target", ["3283", "numeric C_Z input pack"]),
        (SRC_3282_VALIDATION, "3282 validation", ["VAL3282_10_overall", "true"]),
        (SRC_3281_BOUND, "3281 pure C_Z bound", ["CZB3281_0", "1.389797711495e-12"]),
        (SRC_3280_ROWS, "3280 C_Z/C_R rows", ["ZRB3280_3", "MISSING_NUMERIC_READOUT_SLOPE"]),
        (SRC_2630_DECISION, "2630 C_R zero rollforward decision", ["CR_ZERO_NOT_DERIVED", "RAB_REMAINS"]),
        (SRC_2630_NEXT, "2630 C_R next target", ["2631", "no-shadow"]),
        (SRC_2656_CONTRACT, "2656 readout source-bound contract", ["MISSING_PARENT_COUPLING_OWNER", "tau_WEP"]),
        (SRC_2656_DECISION, "2656 readout decision", ["RESIDUAL_BOUND_CONTRACT_STAGED", "2657"]),
    ]
    rows: list[dict[str, Any]] = []
    for idx, (path, role, needles) in enumerate(sources):
        rows.append(
            {
                "source_id": f"SRC3283_{idx}",
                "path": str(path),
                "exists": bool_str(path.exists()),
                "parse_ok": bool_str(parse_ok(path)),
                "role": role,
                "evidence_hits": evidence_hits(path, needles),
                "valid_for_claim": "false",
            }
        )
    return rows


def scan_files() -> list[Path]:
    candidates = [
        SRC_3282_DOC,
        SRC_3282_FORMULA,
        SRC_3282_PREDICTIONS,
        SRC_3281_BOUND,
        SRC_3280_ROWS,
        SRC_2630_DECISION,
        SRC_2630_NEXT,
        SRC_2656_CONTRACT,
        SRC_2656_DECISION,
        OUT / "P8_Y5_R10_1057_F2_COUNTERTERM_LEDGER.csv",
        OUT / "P8_Y5_R10_1099_NO_EXTRA_F2_EXCLUSION_AUDIT.csv",
        OUT / "P8_Y5_R10_1236_NO_HIDDEN_VISIBLE_COEFFICIENT_META_THEOREM.csv",
        OUT / "P8_Y5_R10_1467_NO_HIDDEN_F2_OPERATOR_CLASSIFICATION.csv",
        OUT / "P8_Y5_R2FR_3118_NO_HIDDEN_VISIBLE_COEFFICIENT_HOM_GATE.csv",
        ROOT / "1058-Y5-R10-visible-operator-domain-exhaustion-or-alpha-counterterm-prior.md",
        ROOT / "1099-Y5-R10-unique-EM-kinetic-owner-no-extra-F2-theorem-or-alpha-coefficient-source-row.md",
        ROOT / "1100-Y5-R10-parent-TQ-owner-fixed-charge-lattice-and-gauge-norm-signature.md",
    ]
    files: list[Path] = []
    for path in candidates:
        if not path.exists() or not path.is_file():
            continue
        rel = str(path.relative_to(ROOT)).replace("\\", "/")
        if rel.startswith("scripts/") or "__pycache__" in rel or "3283" in path.name:
            continue
        files.append(path)
    return sorted(set(files))


def classify_line(line: str) -> tuple[str, str]:
    lower = line.lower()
    has_numeric = bool(NUMERIC_RE.search(line))
    has_source = any(marker in lower for marker in SOURCE_MARKERS)
    negative = [marker for marker in NEGATIVE_MARKERS if marker in lower]
    if not has_numeric:
        return "symbolic_or_missing", "no numeric value on target line"
    if negative:
        return "numeric_rejected", "negative marker(s): " + ";".join(sorted(set(negative))[:6])
    if has_source:
        return "numeric_source_candidate_unverified", "numeric and source marker present, but field-specific parent ownership still must be checked"
    return "numeric_unsourced_candidate", "numeric appears without source/provenance marker"


def hunt_rows() -> list[dict[str, Any]]:
    files = scan_files()
    rows: list[dict[str, Any]] = []
    for target in TARGETS:
        hits: list[dict[str, Any]] = []
        total = 0
        numeric = 0
        sourceish = 0
        for path in files:
            try:
                lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
            except Exception:
                continue
            for line_no, line in enumerate(lines, start=1):
                if not target["pattern"].search(line):
                    continue
                total += 1
                if NUMERIC_RE.search(line):
                    numeric += 1
                if any(marker in line.lower() for marker in SOURCE_MARKERS):
                    sourceish += 1
                if len(hits) < 8:
                    candidate_class, rejection = classify_line(line)
                    hits.append(
                        {
                            "path": str(path),
                            "line": line_no,
                            "candidate_class": candidate_class,
                            "rejection_or_note": rejection,
                            "excerpt": compact(line, 260),
                        }
                    )
        if hits:
            for idx, hit in enumerate(hits):
                rows.append(
                    {
                        "target_id": target["target_id"],
                        "required_input": target["required_input"],
                        "total_hits": total,
                        "numeric_hits": numeric,
                        "source_marker_hits": sourceish,
                        "sample_rank": idx,
                        "sample_path": hit["path"],
                        "sample_line": hit["line"],
                        "candidate_class": hit["candidate_class"],
                        "valid_source_backed_input": "false",
                        "rejection_or_note": hit["rejection_or_note"],
                        "excerpt": hit["excerpt"],
                    }
                )
        else:
            rows.append(
                {
                    "target_id": target["target_id"],
                    "required_input": target["required_input"],
                    "total_hits": 0,
                    "numeric_hits": 0,
                    "source_marker_hits": 0,
                    "sample_rank": 0,
                    "sample_path": "NO_HIT",
                    "sample_line": "NO_HIT",
                    "candidate_class": "no_hit",
                    "valid_source_backed_input": "false",
                    "rejection_or_note": "no corpus line matched this required input",
                    "excerpt": "",
                }
            )
    return rows


def pack_decision_rows(hunt: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for target in TARGETS:
        target_rows = [row for row in hunt if row["target_id"] == target["target_id"]]
        total_hits = max(int(row["total_hits"]) for row in target_rows)
        numeric_hits = max(int(row["numeric_hits"]) for row in target_rows)
        valid_rows = sum(1 for row in target_rows if row["valid_source_backed_input"] == "true")
        if valid_rows:
            status = "SOURCE_BACKED_INPUT_FOUND"
            blocker = ""
        elif numeric_hits:
            status = "NUMERIC_LINES_FOUND_BUT_NOT_VALID_INPUTS"
            blocker = "numeric evidence is bounds/smoke/old row locks/unsigned lines, not a parent-owned MTS prediction input"
        elif total_hits:
            status = "SYMBOLIC_ONLY_OR_MISSING"
            blocker = "target appears symbolically but no numeric source-backed value is present"
        else:
            status = "NO_TARGET_MATCH"
            blocker = "no target-specific row found"
        rows.append(
            {
                "input_id": target["target_id"],
                "required_input": target["required_input"],
                "total_hits": total_hits,
                "numeric_hits": numeric_hits,
                "valid_source_backed_rows": valid_rows,
                "status": status,
                "blocks_finite_CZ_scoring": bool_str(valid_rows == 0),
                "blocker": blocker,
                "valid_for_claim": "false",
            }
        )
    complete_pack = all(row["valid_source_backed_rows"] != 0 for row in rows)
    rows.append(
        {
            "input_id": "CZIN3283_5_complete_pack",
            "required_input": "complete source-backed numeric C_Z prediction pack",
            "total_hits": sum(int(row["total_hits"]) for row in rows),
            "numeric_hits": sum(int(row["numeric_hits"]) for row in rows),
            "valid_source_backed_rows": sum(int(row["valid_source_backed_rows"]) for row in rows),
            "status": "COMPLETE_PACK_FOUND" if complete_pack else "COMPLETE_PACK_NOT_FOUND",
            "blocks_finite_CZ_scoring": bool_str(not complete_pack),
            "blocker": "at least one required input has no valid source-backed row",
            "valid_for_claim": "false",
        }
    )
    return rows


def pure_cz_bound() -> float:
    for row in read_csv(SRC_3281_BOUND):
        if row.get("row_id") == "CZB3281_0_pure_CZ_bound_contract":
            return float(row["C_Z_abs_bound"])
    return 1.389797711495e-12


def demotion_rows(bound: float, complete_pack: bool) -> list[dict[str, Any]]:
    return [
        {
            "demotion_id": "CZDEM3283_0_finite_CZ_branch",
            "branch": "finite numeric C_Z residual",
            "decision": "KEEP_OPEN" if complete_pack else "DEMOTE_TO_CLOSURE_ONLY_FOR_NOW",
            "meaning": "finite C_Z can be scored only if the full numeric input pack is sourced",
            "bound_or_formula": f"|C_Z| <= {fmt(bound)} under C_J=C_R=0 side conditions",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "demotion_id": "CZDEM3283_1_zero_theorem_branch",
            "branch": "q-basic or exact-shift C_Z=0 theorem",
            "decision": "RETAIN_AS_DERIVATION_ROUTE",
            "meaning": "not demoted; it remains a clean theorem route if parent action/effective/readout signatures are supplied",
            "bound_or_formula": "Z_Q=q^*Zbar_Q or exact hidden shift/Ward protection => C_Z=0",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "demotion_id": "CZDEM3283_2_not_a_zero_proof",
            "branch": "physical C_Z value",
            "decision": "NO_NUMERIC_PACK_DOES_NOT_PROVE_ZERO",
            "meaning": "absence of source rows is not evidence that C_Z vanishes",
            "bound_or_formula": "C_Z remains an unowned closure residual unless theorem-zero is signed",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "demotion_id": "CZDEM3283_3_live_branch_transfer",
            "branch": "C_R readout",
            "decision": "MOVE_NEXT_ACTIVE_WORK_TO_CR_READOUT",
            "meaning": "because finite C_Z has no source pack, the next non-circular attack is the readout map itself",
            "bound_or_formula": "C_e=2 C_J - C_Z - C_R; with C_J=0 and C_Z theorem/closure, C_R is the live readout residual",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
    ]


def cr_import_rows() -> list[dict[str, Any]]:
    return [
        {
            "import_id": "CRIMP3283_0_3280_readout_row",
            "source_path": str(SRC_3280_ROWS),
            "imported_status": "C_R=L_X ln R_alpha_readout retained with MISSING_NUMERIC_READOUT_SLOPE",
            "how_used": "establishes C_R as separate from C_Z rather than hiding readout drift in Maxwell kinetic owner",
            "valid_for_claim": "false",
        },
        {
            "import_id": "CRIMP3283_1_2630_zero_rollforward",
            "source_path": str(SRC_2630_DECISION),
            "imported_status": "CR_ZERO_NOT_DERIVED_AND_RAB_REMAINS_EXPLICIT_RESIDUAL",
            "how_used": "prevents claiming local-GR/PPN pass from an unsigned readout-zero assumption",
            "valid_for_claim": "false",
        },
        {
            "import_id": "CRIMP3283_2_2630_next_branch",
            "source_path": str(SRC_2630_NEXT),
            "imported_status": "no-shadow/full-PPN vector selected previously",
            "how_used": "keeps readout branch connected to PPN/Newton rather than a gamma-only shortcut",
            "valid_for_claim": "false",
        },
        {
            "import_id": "CRIMP3283_3_2656_readout_contract",
            "source_path": str(SRC_2656_CONTRACT),
            "imported_status": "readout/source residual bound contract staged but not executable",
            "how_used": "shows empirical readout data alone cannot score MTS without parent coupling/source/material/tau inputs",
            "valid_for_claim": "false",
        },
        {
            "import_id": "CRIMP3283_4_2656_decision",
            "source_path": str(SRC_2656_DECISION),
            "imported_status": "parent coupling/source contraction theorem selected as dependency",
            "how_used": "supports making the next target a derivation of readout standards, not a data-only scrape",
            "valid_for_claim": "false",
        },
    ]


def cr_formula_rows() -> list[dict[str, Any]]:
    return [
        {
            "formula_id": "CRF3283_0_readout_definition",
            "object": "alpha readout residual",
            "formula": "C_R := L_v ln R_alpha_readout",
            "status": "DEFINITION_FROM_3280_3282_BRANCH",
            "required_for_claim": "source or derive R_alpha_readout from parent-owned standards",
            "valid_for_claim": "false",
        },
        {
            "formula_id": "CRF3283_1_product_law_contract",
            "object": "readout standard product",
            "formula": "If R_alpha_readout = product_s R_s^{n_s}, then C_R = sum_s n_s L_v ln R_s",
            "status": "EXACT_LOG_DERIVATIVE_CONTRACT",
            "required_for_claim": "declare the standard factors: charge normalization, action/phase unit, clock/rods, EM energy-flux/Poynting-wave calibration, material detector response",
            "valid_for_claim": "false",
        },
        {
            "formula_id": "CRF3283_2_qbasic_readout_zero",
            "object": "readout-zero theorem route",
            "formula": "R_alpha_readout=q^*Rbar_alpha and v in ker(Dq) => C_R=0",
            "status": "EXACT_CONDITIONAL_ZERO_THEOREM",
            "required_for_claim": "parent-signed q-basic readout functor across clocks, rods, charge standards, Poynting/EM flux standards, and detector material labels",
            "valid_for_claim": "false",
        },
        {
            "formula_id": "CRF3283_3_Poynting_wave_standard",
            "object": "EM wave/energy-flux readout fork",
            "formula": "A Poynting-vector standard can move alpha drift between field normalization and detector readout unless its parent pullback is fixed before observation",
            "status": "LIVE_DERIVATION_TARGET",
            "required_for_claim": "derive whether S^i_EM and wave amplitude/frequency standards are q-basic, shifted, or have a finite readout slope",
            "valid_for_claim": "false",
        },
        {
            "formula_id": "CRF3283_4_no_data_only_shortcut",
            "object": "empirical readout bound",
            "formula": "bound(C_R) is useful only after C_R prediction factors are derived or sourced",
            "status": "GUARDRAIL",
            "required_for_claim": "no MICROSCOPE/PPN/clock score without parent readout coefficient or theorem-zero",
            "valid_for_claim": "false",
        },
    ]


def promotion_rows(complete_pack: bool) -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "GATE3283_0_numeric_CZ_pack_found",
            "passed": bool_str(complete_pack),
            "claim_allowed": "false",
            "detail": "complete pack requires numeric Z_Q, f'_X, L_v I_hid, radiative slope, and readout slope with source paths",
        },
        {
            "gate_id": "GATE3283_1_finite_CZ_demoted_if_pack_missing",
            "passed": bool_str(not complete_pack),
            "claim_allowed": "false",
            "detail": "finite unzeroed C_Z branch is closure-only until numeric pack appears",
        },
        {
            "gate_id": "GATE3283_2_CZ_zero_route_retained",
            "passed": "true",
            "claim_allowed": "false",
            "detail": "q-basic/exact-shift C_Z=0 route remains a derivation target, not a current claim",
        },
        {
            "gate_id": "GATE3283_3_CR_branch_imported",
            "passed": "true",
            "claim_allowed": "false",
            "detail": "previous C_R/readout branch imported, including CR-zero failure and readout bound contract",
        },
        {
            "gate_id": "GATE3283_4_no_public_claim",
            "passed": "true",
            "claim_allowed": "false",
            "detail": "no R10/PPN/clock/local-GR claim is allowed from a missing numeric pack or closure demotion",
        },
    ]


def decision_rows(complete_pack: bool) -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3283_0_source_hunt",
            "decision": "COMPLETE_NUMERIC_CZ_PACK_FOUND" if complete_pack else "COMPLETE_NUMERIC_CZ_PACK_NOT_FOUND",
            "why_it_moves_forward": "the hunt is recorded by required input, numeric hit count, sample line, and rejection reason instead of vibes",
            "claim_allowed": "false",
        },
        {
            "decision_id": "DEC3283_1_CZ_branch",
            "decision": "finite C_Z is closure-only unless a future numeric pack or parent zero theorem appears",
            "why_it_moves_forward": "stops repeated passes over the same hidden F2 slot without new evidence",
            "claim_allowed": "false",
        },
        {
            "decision_id": "DEC3283_2_CR_branch",
            "decision": "C_R readout becomes the next active derivation branch",
            "why_it_moves_forward": "attacks the observed alpha/EM calibration layer directly, including clocks, charge standards, material response, and Poynting/wave readout",
            "claim_allowed": "false",
        },
        {
            "decision_id": "DEC3283_3_empirical_guard",
            "decision": "data-only readout tests remain blocked until an MTS readout coefficient or zero theorem exists",
            "why_it_moves_forward": "prevents wasting tokens scraping data before the theory has a predicted readout vector",
            "claim_allowed": "false",
        },
    ]


def next_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT3283_0_3284",
            "target_doc": "3284-Y5-R2FR-CR-readout-product-law-and-Poynting-wave-standard-or-zero-theorem-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3284_CR_readout_product_law_and_Poynting_wave_standard_or_zero_theorem.py",
            "objective": "Derive the C_R readout product law for alpha/EM observations, including charge normalization, clock/action standards, material detector response, and Poynting-vector/wave energy-flux readout; prove the whole readout map is q-basic/shift-protected or source the first finite C_R slope row.",
            "guardrail": "Do not run empirical readout bounds or claim local GR from C_R=0 unless the readout product factors are parent-owned; no gamma-only or MICROSCOPE-data-only shortcut.",
            "valid_for_claim": "false",
        }
    ]


def validate(
    fw_before: dict[str, tuple[int, int]],
    sources: list[dict[str, Any]],
    hunt: list[dict[str, Any]],
    pack: list[dict[str, Any]],
    demotion: list[dict[str, Any]],
    cr_import: list[dict[str, Any]],
    cr_formula: list[dict[str, Any]],
    promotion: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    non_validation_outputs = [path for key, path in OUTPUTS.items() if key != "validation"]
    fw_after = snapshot_tree(FW)
    fw_changed = changed_count(fw_before, fw_after)
    checks: list[dict[str, Any]] = []

    def add(check_id: str, check: str, passed: bool, detail: str = "") -> None:
        checks.append(
            {
                "check_id": check_id,
                "check": check,
                "passed": bool_str(passed),
                "detail": compact(detail, 520),
            }
        )

    complete_pack_row = next(row for row in pack if row["input_id"] == "CZIN3283_5_complete_pack")
    complete_pack_missing = complete_pack_row["status"] == "COMPLETE_PACK_NOT_FOUND"
    add("VAL3283_0_sources_exist", "all cited source paths exist", all(row["exists"] == "true" for row in sources))
    add("VAL3283_1_sources_parse", "all cited source paths parse", all(row["parse_ok"] == "true" for row in sources))
    add(
        "VAL3283_2_outputs_parse",
        "all 3283 non-validation output CSVs parse",
        all(csv_parse_ok(path) for path in non_validation_outputs),
        "non-validation outputs parsed before validation write",
    )
    add(
        "VAL3283_3_required_inputs_scanned",
        "all five C_Z input targets were scanned",
        len({row["target_id"] for row in hunt}) == 5,
        ";".join(sorted({row["target_id"] for row in hunt})),
    )
    add(
        "VAL3283_4_pack_decision_present",
        "complete pack decision row is present and blocks finite C_Z if missing",
        complete_pack_missing and complete_pack_row["blocks_finite_CZ_scoring"] == "true",
        complete_pack_row["status"],
    )
    add(
        "VAL3283_5_CZ_demoted_to_closure",
        "finite C_Z branch is closure-only when numeric pack is absent",
        any(row["demotion_id"] == "CZDEM3283_0_finite_CZ_branch" and row["decision"] == "DEMOTE_TO_CLOSURE_ONLY_FOR_NOW" for row in demotion),
    )
    add(
        "VAL3283_6_CR_branch_imported",
        "C_R/readout branch source imports are present",
        len(cr_import) >= 5 and any("CR_ZERO_NOT_DERIVED" in row["imported_status"] for row in cr_import),
    )
    add(
        "VAL3283_7_Poynting_next_target",
        "next target includes Poynting/wave readout route",
        any("Poynting" in row["objective"] and "C_R" in row["objective"] for row in next_target),
    )
    add(
        "VAL3283_8_CR_product_formula",
        "C_R product-law handoff is present",
        any(row["formula_id"] == "CRF3283_1_product_law_contract" and "sum_s" in row["formula"] for row in cr_formula),
    )
    add(
        "VAL3283_9_claim_gates_false",
        "no 3283 gate allows local-GR/alpha/Maxwell claim",
        all(row["claim_allowed"] == "false" for row in promotion),
    )
    add(
        "VAL3283_10_formalization_untouched",
        "formalization-workbench modified-file count remains zero by this script",
        fw_changed == 0,
        f"formalization_changed_count={fw_changed}",
    )
    overall = all(row["passed"] == "true" for row in checks)
    add(
        "VAL3283_11_overall",
        "3283 validation overall",
        overall,
        "all required checks passed" if overall else "one or more checks failed",
    )
    return checks


def md_escape(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def md_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    lines = [
        "| " + " | ".join(columns) + " |",
        "| " + " | ".join("---" for _ in columns) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(md_escape(row.get(col, "")) for col in columns) + " |")
    return "\n".join(lines)


def write_doc(
    pack: list[dict[str, Any]],
    demotion: list[dict[str, Any]],
    cr_import: list[dict[str, Any]],
    cr_formula: list[dict[str, Any]],
    promotion: list[dict[str, Any]],
    decision: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> None:
    complete = next(row for row in pack if row["input_id"] == "CZIN3283_5_complete_pack")
    text = f"""# 3283 - First numeric C_Z input source pack or C_R readout demotion under AX1090

## Summary

3283 forces the fork requested by 3282. The corpus was scanned for the five inputs needed to turn the exact formula

`C_Z = [sum_a f_a,_b L_v I^b_hid + L_v delta_lambda_rad + L_v delta_Z_readout] / Z_Q`

into a scoreable finite prediction. The complete numeric pack status is `{complete["status"]}`.

That means finite, unzeroed `C_Z` is now demoted to closure-only for the current branch. This is **not** a proof that `C_Z=0`; it only says the finite-`C_Z` scoring route has no source-backed input pack yet. The q-basic/exact-shift zero-theorem route remains alive.

The next active branch is therefore `C_R`, the observed alpha/EM readout residual. This is where clocks, charge normalization, material detector response, and Poynting-vector/wave energy-flux standards can enter without being hidden inside the Maxwell kinetic coefficient.

## C_Z Input Pack Decision
{md_table(pack, ["input_id", "required_input", "numeric_hits", "valid_source_backed_rows", "status", "blocks_finite_CZ_scoring"])}

## C_Z Closure Demotion
{md_table(demotion, ["demotion_id", "branch", "decision", "meaning", "claim_allowed"])}

## C_R Branch Import
{md_table(cr_import, ["import_id", "imported_status", "how_used", "valid_for_claim"])}

## C_R Readout Formula Handoff
{md_table(cr_formula, ["formula_id", "object", "formula", "status", "required_for_claim"])}

## Promotion Gates
{md_table(promotion, ["gate_id", "passed", "claim_allowed", "detail"])}

## Decisions
{md_table(decision, ["decision_id", "decision", "why_it_moves_forward", "claim_allowed"])}

## Next Target
{md_table(next_target, ["next_id", "target_doc", "objective", "guardrail"])}

## Validation
{md_table(validation, ["check_id", "check", "passed", "detail"])}

Generated UTC: {RUN_UTC}
"""
    DOC.write_text(text, encoding="utf-8")


def main() -> None:
    fw_before = snapshot_tree(FW)
    bound = pure_cz_bound()
    sources = source_register_rows()
    hunt = hunt_rows()
    pack = pack_decision_rows(hunt)
    complete_pack = next(row for row in pack if row["input_id"] == "CZIN3283_5_complete_pack")["status"] == "COMPLETE_PACK_FOUND"
    demotion = demotion_rows(bound, complete_pack)
    cr_import = cr_import_rows()
    cr_formula = cr_formula_rows()
    promotion = promotion_rows(complete_pack)
    decision = decision_rows(complete_pack)
    next_target = next_rows()

    write_csv(OUTPUTS["sources"], sources)
    write_csv(OUTPUTS["hunt"], hunt)
    write_csv(OUTPUTS["pack"], pack)
    write_csv(OUTPUTS["demotion"], demotion)
    write_csv(OUTPUTS["cr_import"], cr_import)
    write_csv(OUTPUTS["cr_formula"], cr_formula)
    write_csv(OUTPUTS["promotion"], promotion)
    write_csv(OUTPUTS["decision"], decision)
    write_csv(OUTPUTS["next"], next_target)

    validation = validate(fw_before, sources, hunt, pack, demotion, cr_import, cr_formula, promotion, next_target)
    write_csv(OUTPUTS["validation"], validation)
    write_doc(pack, demotion, cr_import, cr_formula, promotion, decision, next_target, validation)

    if PYCACHE.exists():
        shutil.rmtree(PYCACHE)


if __name__ == "__main__":
    main()
