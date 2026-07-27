from __future__ import annotations

import csv
import shutil
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Mapping, Sequence


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from curvature_alpha_lambda_threshold_gate import (  # noqa: E402
    HBAR_C_EV_M,
    curve_quality_rows,
    evaluate_channel_threshold,
    interpolate_threshold,
    parse_curve_rows,
    read_csv,
    write_csv,
)


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4456"
CLAIM_ID = "L-298"
MARKER = "PPC4161_ALPHA_LAMBDA_CURVE_PROMOTION_OR_PARENT_MR_SCALE_VALUE_4456"
PACKET_MARKER = "PPC4161_PACKET_ALPHA_LAMBDA_CURVE_PROMOTION_OR_PARENT_MR_SCALE_VALUE_4456"
DECISION = "CANDIDATE_ALPHA_LAMBDA_CHANNEL_THRESHOLDS_DERIVED_PARENT_MASS_RULE_WRITTEN_SUPPLEMENTAL_OR_PARENT_MASS_STILL_REQUIRED_NONCLAIM"
NEXT_TARGET = "4457-Y5-R2FR-parent-M0-M2-scale-derivation-or-signed-alpha-supplemental-table.md"

FORMAL_PATH = FORMAL / "472-PPC4161-alpha-lambda-curve-promotion-or-parent-MR-scale-value.md"
DOC_PATH = POST / "4456-Y5-R2FR-alpha-lambda-curve-promotion-or-parent-MR-scale-value.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4456_VALIDATION.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4456_SOURCE_REGISTER.csv"
CHANNEL_INPUT = SOURCE_DIR / "P8_Y5_R2FR_4456_CHANNEL_INPUT.csv"
CHANNEL_THRESHOLDS = SOURCE_DIR / "P8_Y5_R2FR_4456_CHANNEL_THRESHOLDS_CANDIDATE.csv"
CURVE_QUALITY = SOURCE_DIR / "P8_Y5_R2FR_4456_CURVE_QUALITY.csv"
PARENT_SCALE_RULES = SOURCE_DIR / "P8_Y5_R2FR_4456_PARENT_SCALE_RULES.csv"
SUPPLEMENTAL_STATUS = SOURCE_DIR / "P8_Y5_R2FR_4456_SUPPLEMENTAL_ACQUISITION_STATUS.csv"
DERIVATION_ROWS = SOURCE_DIR / "P8_Y5_R2FR_4456_DERIVATION_ROWS.csv"
FORMULA_ROWS = SOURCE_DIR / "P8_Y5_R2FR_4456_FORMULA_ROWS.csv"
CLAIM_GATES = SOURCE_DIR / "P8_Y5_R2FR_4456_CLAIM_GATES.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4456_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4456_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4456_NEXT_TARGET.csv"

GATE_PATH = SCRIPT_DIR / "curvature_alpha_lambda_threshold_gate.py"
GENERATOR_PATH = SCRIPT_DIR / "Y5_R2FR_4456_alpha_lambda_curve_promotion_or_parent_MR_scale_value.py"
STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

FORMAL_471 = FORMAL / "471-PPC4161-cR2-parent-scale-signature-or-alpha-lambda-projection-row.md"
POST_4455 = POST / "4455-Y5-R2FR-cR2-parent-scale-signature-or-alpha-lambda-projection-row.md"
PROJECTION_4455 = SOURCE_DIR / "P8_Y5_R2FR_4455_ALPHA_LAMBDA_PROJECTION_OUTPUT.csv"
STATUS_4455 = SOURCE_DIR / "P8_Y5_R2FR_4455_STATUS.csv"
NEXT_4455 = SOURCE_DIR / "P8_Y5_R2FR_4455_NEXT_TARGET.csv"
CURVE_3702 = SOURCE_DIR / "P8_Y5_R2FR_3702_R10_BOUND_CURVE_CANDIDATE.csv"
STATUS_3702 = SOURCE_DIR / "P8_Y5_R2FR_3702_STATUS.csv"
EXTRACTION_3702 = SOURCE_DIR / "P8_Y5_R2FR_3702_R10_FIGURE_EXTRACTION_ROWS.csv"
TEX_SOURCE = POST / "source-intake" / "r10" / "arxiv_2002_11761_source" / "FB_ISL_pdf.tex"
SUPPLEMENTAL_URL = "https://link.aps.org/supplemental/10.1103/PhysRevLett.124.101101"
DOI_URL = "https://doi.org/10.1103/PhysRevLett.124.101101"
ARXIV_URL = "https://arxiv.org/abs/2002.11761"


def text(path: Path) -> str:
    if not path.exists():
        return ""
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return ""


def write_text(path: Path, body: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(body, encoding="utf-8")


def line_of(path: Path, needle: str) -> int:
    if not path.exists() or not needle:
        return 0
    for line_number, line in enumerate(text(path).splitlines(), start=1):
        if needle in line:
            return line_number
    return 0


def md(value: object) -> str:
    return str(value).replace("\n", " ").replace("|", "\\|")


def table(rows: Sequence[Mapping[str, object]]) -> str:
    if not rows:
        return ""
    headers = list(rows[0].keys())
    output = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    for row in rows:
        output.append("| " + " | ".join(md(row.get(header, "")) for header in headers) + " |")
    return "\n".join(output)


def source_specs() -> List[Dict[str, object]]:
    return [
        {"source_id": "SRC4456_00_next4455", "kind": "local", "ref": str(NEXT_4455), "needle": "4456-Y5-R2FR-alpha-lambda-curve-promotion-or-parent-MR-scale-value.md", "role": "4455 selected alpha-lambda/parent scale target."},
        {"source_id": "SRC4456_01_formal471", "kind": "local", "ref": str(FORMAL_471), "needle": "alpha_2 = -4/3", "role": "4455 spin-2 projection amplitude."},
        {"source_id": "SRC4456_02_projection4455", "kind": "local", "ref": str(PROJECTION_4455), "needle": "AP4455_1_spin2", "role": "4455 channel projection rows."},
        {"source_id": "SRC4456_03_status4455", "kind": "local", "ref": str(STATUS_4455), "needle": "signature_staged_numeric_MR_missing", "role": "4455 parent scale status."},
        {"source_id": "SRC4456_04_curve3702", "kind": "local", "ref": str(CURVE_3702), "needle": "R10C3702_OFFICIAL_ALPHA1_ANCHOR", "role": "3702 candidate R10 curve with official alpha=1 anchor."},
        {"source_id": "SRC4456_05_status3702", "kind": "local", "ref": str(STATUS_3702), "needle": "38.583 micrometer", "role": "3702 candidate curve status."},
        {"source_id": "SRC4456_06_extract3702", "kind": "local", "ref": str(EXTRACTION_3702), "needle": "candidate_curve_manual_review_required", "role": "3702 extraction limitations."},
        {"source_id": "SRC4456_07_tex_yukawa", "kind": "local", "ref": str(TEX_SOURCE), "needle": "V(r)=V_N(r) [1+\\alpha", "role": "source Yukawa convention."},
        {"source_id": "SRC4456_08_tex_66_lambda", "kind": "local", "ref": str(TEX_SOURCE), "needle": "66 assumed values", "role": "source says 66 lambda values were fitted."},
        {"source_id": "SRC4456_09_tex_supplement", "kind": "local", "ref": str(TEX_SOURCE), "needle": "Supplemental Material", "role": "source points to signed alpha constraints in supplement."},
        {"source_id": "SRC4456_10_tex_mass", "kind": "local", "ref": str(TEX_SOURCE), "needle": "mass must be greater than 5.1 meV", "role": "source mass conversion anchor."},
        {"source_id": "SRC4456_11_arxiv", "kind": "web", "ref": ARXIV_URL, "needle": "Lee et al 2020 arXiv page", "role": "external source page."},
        {"source_id": "SRC4456_12_doi", "kind": "web", "ref": DOI_URL, "needle": "PRL DOI page", "role": "official DOI source."},
        {"source_id": "SRC4456_13_supplemental", "kind": "web", "ref": SUPPLEMENTAL_URL, "needle": "APS supplemental material endpoint", "role": "official supplemental table acquisition route."},
        {"source_id": "SRC4456_14_gate", "kind": "local", "ref": str(GATE_PATH), "needle": "def interpolate_threshold", "role": "4456 threshold gate."},
        {"source_id": "SRC4456_15_generator", "kind": "local", "ref": str(GENERATOR_PATH), "needle": 'CHECKPOINT = "4456"', "role": "4456 generator script."},
    ]


def source_rows() -> List[Dict[str, object]]:
    rows = []
    for spec in source_specs():
        kind = str(spec["kind"])
        ref = str(spec["ref"])
        path = Path(ref) if kind == "local" else None
        line = line_of(path, str(spec["needle"])) if path else 0
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "source_id": spec["source_id"],
                "source_kind": kind,
                "source_ref": ref,
                "local_path_exists": bool(path and path.exists()),
                "web_source_recorded": kind == "web" and ref.startswith("https://"),
                "needle": spec["needle"],
                "needle_found": line > 0 if kind == "local" else True,
                "line_number": line,
                "role": spec["role"],
                "valid_for_claim": False,
            }
        )
    return rows


def channel_input_rows() -> List[Dict[str, object]]:
    projection_rows = read_csv(PROJECTION_4455)
    rows: List[Dict[str, object]] = []
    for row in projection_rows:
        if row.get("projection_id") == "AP4455_0_scalar":
            rows.append(
                {
                    "channel_id": "CH4456_0_scalar",
                    "mode": row.get("mode"),
                    "alpha_standard": row.get("alpha_standard"),
                    "lambda_symbol": "lambda_0 = 1/M_0",
                    "mass_symbol": "M_0",
                    "signed_channel": "positive_alpha_scalar",
                    "source_projection_id": row.get("projection_id"),
                    "valid_for_claim": False,
                }
            )
        if row.get("projection_id") == "AP4455_1_spin2":
            rows.append(
                {
                    "channel_id": "CH4456_1_spin2",
                    "mode": row.get("mode"),
                    "alpha_standard": row.get("alpha_standard"),
                    "lambda_symbol": "lambda_2 = 1/M_2",
                    "mass_symbol": "M_2",
                    "signed_channel": "negative_alpha_massive_spin2",
                    "source_projection_id": row.get("projection_id"),
                    "valid_for_claim": False,
                }
            )
    return rows


def curve_rows() -> List[Dict[str, object]]:
    return parse_curve_rows(read_csv(CURVE_3702))


def channel_threshold_rows(curve: Sequence[Dict[str, object]]) -> List[Dict[str, object]]:
    return [evaluate_channel_threshold(row, curve) for row in channel_input_rows()]


def parent_scale_rule_rows(thresholds: Sequence[Dict[str, object]]) -> List[Dict[str, object]]:
    mass_values = [float(row["mass_threshold_eV"]) for row in thresholds if row.get("mass_threshold_eV") not in {"", None}]
    common_mass = max(mass_values) if mass_values else ""
    alpha_one_mass = HBAR_C_EV_M / (38.6e-6)
    return [
        {
            "rule_id": "MR4456_0_official_alpha1_anchor",
            "scope": "alpha_abs_equals_1_only",
            "lambda_threshold_um": 38.6,
            "mass_threshold_eV": alpha_one_mass,
            "derivation": "M = hbar*c/lambda using the source 38.6 micrometer gravitational-strength anchor",
            "claim_status": "SOURCE_BACKED_ANCHOR_NOT_FULL_CHANNEL_SCORE",
            "valid_for_claim": False,
        },
        {
            "rule_id": "MR4456_1_scalar_candidate",
            "scope": "standard_scalar_alpha_abs_1_over_3_candidate_curve",
            "lambda_threshold_um": next((row["lambda_threshold_um"] for row in thresholds if row.get("channel_id") == "CH4456_0_scalar"), ""),
            "mass_threshold_eV": next((row["mass_threshold_eV"] for row in thresholds if row.get("channel_id") == "CH4456_0_scalar"), ""),
            "derivation": "solve candidate alpha_bound(lambda)=1/3 by log-log interpolation, then M_0>=hbar*c/lambda_threshold",
            "claim_status": "PRIVATE_SMOKE_ONLY",
            "valid_for_claim": False,
        },
        {
            "rule_id": "MR4456_2_spin2_candidate",
            "scope": "standard_massive_spin2_alpha_abs_4_over_3_candidate_curve",
            "lambda_threshold_um": next((row["lambda_threshold_um"] for row in thresholds if row.get("channel_id") == "CH4456_1_spin2"), ""),
            "mass_threshold_eV": next((row["mass_threshold_eV"] for row in thresholds if row.get("channel_id") == "CH4456_1_spin2"), ""),
            "derivation": "solve candidate alpha_bound(lambda)=4/3 by log-log interpolation, then M_2>=hbar*c/lambda_threshold",
            "claim_status": "PRIVATE_SMOKE_ONLY",
            "valid_for_claim": False,
        },
        {
            "rule_id": "MR4456_3_common_parent_mass_candidate",
            "scope": "if_M0_equals_M2_or_single_MR_controls_both_standard_modes",
            "lambda_threshold_um": HBAR_C_EV_M / common_mass * 1e6 if common_mass else "",
            "mass_threshold_eV": common_mass,
            "derivation": "single parent scale must satisfy the strictest channel threshold, currently the spin-2 alpha_abs=4/3 candidate threshold",
            "claim_status": "PRIVATE_SMOKE_ONLY_REQUIRES_PARENT_EQUALITY_THEOREM",
            "valid_for_claim": False,
        },
    ]


def supplemental_status_rows() -> List[Dict[str, object]]:
    request = urllib.request.Request(SUPPLEMENTAL_URL, method="HEAD", headers={"User-Agent": "Mozilla/5.0"})
    status = "NOT_ATTEMPTED"
    detail = ""
    final_url = SUPPLEMENTAL_URL
    try:
        with urllib.request.urlopen(request, timeout=15) as response:
            status = f"HTTP_{response.status}"
            detail = response.headers.get("Content-Type", "")
            final_url = response.geturl()
    except urllib.error.HTTPError as exc:
        status = f"HTTP_{exc.code}"
        detail = str(exc.reason)
        final_url = exc.url
    except Exception as exc:  # noqa: BLE001
        status = "REQUEST_FAILED"
        detail = f"{type(exc).__name__}: {exc}"
    return [
        {
            "acquisition_id": "SUP4456_0_arxiv_source_tex",
            "route": "arxiv_source_tex",
            "url": ARXIV_URL,
            "local_path": str(TEX_SOURCE),
            "status": "LOCAL_SOURCE_CONFIRMS_SUPPLEMENTAL_CONTAINS_SIGNED_ALPHA_CONSTRAINTS",
            "claim_use": "source-pointer-only",
            "valid_for_claim": False,
        },
        {
            "acquisition_id": "SUP4456_1_aps_supplemental_head",
            "route": "aps_supplemental_endpoint",
            "url": SUPPLEMENTAL_URL,
            "local_path": "",
            "status": status,
            "claim_use": f"needs successful download and table extraction before claim; final_url={final_url}; detail={detail}",
            "valid_for_claim": False,
        },
        {
            "acquisition_id": "SUP4456_2_candidate_fallback",
            "route": "3702_vector_candidate_curve",
            "url": "",
            "local_path": str(CURVE_3702),
            "status": "AVAILABLE_FOR_PRIVATE_SMOKE_NOT_PUBLIC_CLAIM",
            "claim_use": "threshold exploration only",
            "valid_for_claim": False,
        },
    ]


def formula_rows() -> List[Dict[str, object]]:
    return [
        {
            "formula_id": "F4456_0_channel_score",
            "formula": "pass_i iff abs(alpha_i) <= alpha_bound(lambda_i)",
            "meaning": "channelwise R10 score rule",
            "valid_for_claim": False,
        },
        {
            "formula_id": "F4456_1_mass_range",
            "formula": "lambda_i = hbar*c/M_i",
            "meaning": "convert parent pole mass to Yukawa range in SI units",
            "valid_for_claim": False,
        },
        {
            "formula_id": "F4456_2_parent_threshold",
            "formula": "M_i >= hbar*c/lambda_star(abs(alpha_i))",
            "meaning": "parent mass threshold after solving alpha_bound(lambda_star)=abs(alpha_i)",
            "valid_for_claim": False,
        },
        {
            "formula_id": "F4456_3_standard_channels",
            "formula": "abs(alpha_0)=1/3 and abs(alpha_2)=4/3",
            "meaning": "4455 scalar and spin-2 amplitudes to be scored separately",
            "valid_for_claim": False,
        },
        {
            "formula_id": "F4456_4_no_cancellation",
            "formula": "score scalar and spin-2 separately unless parent action derives a common cancellation identity",
            "meaning": "prevents hiding one bad channel behind the other",
            "valid_for_claim": False,
        },
    ]


def derivation_rows(thresholds: Sequence[Dict[str, object]], parent_rules: Sequence[Dict[str, object]]) -> List[Dict[str, object]]:
    scalar = next(row for row in thresholds if row["channel_id"] == "CH4456_0_scalar")
    spin2 = next(row for row in thresholds if row["channel_id"] == "CH4456_1_spin2")
    common = next(row for row in parent_rules if row["rule_id"] == "MR4456_3_common_parent_mass_candidate")
    return [
        {
            "derivation_id": "D4456_0_scoreable_channel_reduction",
            "premise": "4455 reduced cR2 to two standard Yukawa channels.",
            "derivation": "Insert alpha_0=+1/3 and alpha_2=-4/3 into the R10 Yukawa score rule rather than using a generic alpha=1 anchor.",
            "result": "The cR2 branch now has two channel thresholds instead of an undefined alpha(lambda) placeholder.",
            "status": "DERIVED_SCORE_RULE",
            "valid_for_claim": False,
        },
        {
            "derivation_id": "D4456_1_scalar_threshold_candidate",
            "premise": "Private candidate curve can be used for smoke thresholds only.",
            "derivation": f"Solving alpha_bound(lambda)=1/3 gives lambda_0 <= {scalar['lambda_threshold_um']} micrometer, equivalent to M_0 >= {scalar['mass_threshold_eV']} eV.",
            "result": "The scalar channel is less strict than the official alpha=1 anchor on the candidate curve.",
            "status": "PRIVATE_THRESHOLD_DERIVED",
            "valid_for_claim": False,
        },
        {
            "derivation_id": "D4456_2_spin2_threshold_candidate",
            "premise": "The massive spin-2 branch has abs(alpha_2)=4/3, not alpha=1.",
            "derivation": f"Solving alpha_bound(lambda)=4/3 gives lambda_2 <= {spin2['lambda_threshold_um']} micrometer, equivalent to M_2 >= {spin2['mass_threshold_eV']} eV.",
            "result": "The spin-2 channel is stricter than the official alpha=1 anchor and becomes the conservative candidate parent-scale gate.",
            "status": "PRIVATE_THRESHOLD_DERIVED",
            "valid_for_claim": False,
        },
        {
            "derivation_id": "D4456_3_common_parent_scale_candidate",
            "premise": "If a future parent theorem makes M_0=M_2=M_R, both channels must pass together.",
            "derivation": f"Use the maximum candidate mass threshold: M_R >= {common['mass_threshold_eV']} eV.",
            "result": "A single-scale parent route is now a concrete target, not a vague heavy-mode demand.",
            "status": "PRIVATE_PARENT_TARGET_DERIVED",
            "valid_for_claim": False,
        },
        {
            "derivation_id": "D4456_4_claim_firewall",
            "premise": "The 3702 curve is candidate-only and the PRL source says signed alpha rows live in Supplemental Material.",
            "derivation": "Keep public claim false until either the signed supplemental table is extracted/reviewed or the parent action proves cR2 zero/heavy with source-backed M_0/M_2.",
            "result": "No R10/local-GR pass is claimed from this checkpoint.",
            "status": "NONCLAIM_FIREWALL",
            "valid_for_claim": False,
        },
    ]


def claim_gate_rows(thresholds: Sequence[Dict[str, object]], parent_rules: Sequence[Dict[str, object]], supplemental: Sequence[Dict[str, object]]) -> List[Dict[str, object]]:
    curve_quality = curve_quality_rows(curve_rows())
    threshold_ok = all(row.get("threshold_found") is True for row in thresholds)
    supplemental_downloaded = any(str(row.get("status")).startswith("HTTP_200") for row in supplemental)
    common_mass_written = any(row["rule_id"] == "MR4456_3_common_parent_mass_candidate" and row["mass_threshold_eV"] not in {"", None} for row in parent_rules)
    return [
        {"gate_id": "CG4456_0_sources_exist", "claim": "local source paths exist and needles found", "passed": all(row["needle_found"] for row in source_rows() if row["source_kind"] == "local"), "valid_for_claim": False, "detail": "4455/3702/local TeX sources found."},
        {"gate_id": "CG4456_1_curve_positive", "claim": "candidate curve positive numeric", "passed": curve_quality[0]["passed"], "valid_for_claim": False, "detail": curve_quality[0]["detail"]},
        {"gate_id": "CG4456_2_anchor_reproduced", "claim": "candidate curve reproduces alpha=1 anchor", "passed": curve_quality[2]["passed"], "valid_for_claim": False, "detail": curve_quality[2]["detail"]},
        {"gate_id": "CG4456_3_thresholds_found", "claim": "scalar and spin2 channel thresholds derived", "passed": threshold_ok, "valid_for_claim": False, "detail": "1/3 and 4/3 candidate thresholds found."},
        {"gate_id": "CG4456_4_common_parent_rule", "claim": "common parent mass smoke rule written", "passed": common_mass_written, "valid_for_claim": False, "detail": "single-scale rule uses strictest channel."},
        {"gate_id": "CG4456_5_supplemental_not_promoted", "claim": "official supplemental table not promoted unless downloaded/reviewed", "passed": not supplemental_downloaded, "valid_for_claim": False, "detail": "APS route recorded; no official table was promoted."},
        {"gate_id": "CG4456_6_no_public_claim", "claim": "no R10/local-GR public claim emitted", "passed": True, "valid_for_claim": False, "detail": "candidate thresholds are private smoke only."},
        {"gate_id": "CG4456_7_next_target_written", "claim": "next target selected", "passed": True, "valid_for_claim": False, "detail": NEXT_TARGET},
    ]


def decision_rows(thresholds: Sequence[Dict[str, object]], parent_rules: Sequence[Dict[str, object]]) -> List[Dict[str, object]]:
    scalar = next(row for row in thresholds if row["channel_id"] == "CH4456_0_scalar")
    spin2 = next(row for row in thresholds if row["channel_id"] == "CH4456_1_spin2")
    common = next(row for row in parent_rules if row["rule_id"] == "MR4456_3_common_parent_mass_candidate")
    return [
        {
            "checkpoint": CHECKPOINT,
            "marker": MARKER,
            "claim_id": CLAIM_ID,
            "decision": DECISION,
            "scalar_lambda_um_candidate": scalar["lambda_threshold_um"],
            "scalar_mass_eV_candidate": scalar["mass_threshold_eV"],
            "spin2_lambda_um_candidate": spin2["lambda_threshold_um"],
            "spin2_mass_eV_candidate": spin2["mass_threshold_eV"],
            "common_mass_eV_candidate": common["mass_threshold_eV"],
            "official_claim": False,
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "generated_utc": STAMP,
        }
    ]


def status_rows() -> List[Dict[str, object]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "marker": MARKER,
            "claim_id": CLAIM_ID,
            "decision": DECISION,
            "curve_status": "candidate_curve_scoreable_for_private_smoke_not_claim",
            "parent_scale_status": "numeric_M0_M2_or_zero_theorem_missing",
            "supplemental_status": "official_signed_alpha_table_route_recorded_not_promoted",
            "local_GR_public_claim": False,
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "generated_utc": STAMP,
        }
    ]


def next_rows() -> List[Dict[str, object]]:
    return [
        {
            "next_id": "NT4456_0",
            "target": NEXT_TARGET,
            "objective": "Either derive parent M0/M2 scale values from the MTS action/hierarchy or extract the signed APS supplemental alpha table.",
            "derive_first": "prove cR2 is absent/heavy or map parent coefficients to M0/M2 with numeric lower bounds",
            "fallback": "recover signed positive/negative alpha(lambda) table from APS supplement/manual source review",
            "risk": "using candidate absolute curve thresholds as if they were official signed constraints",
            "valid_for_claim": False,
        }
    ]


def update_claims_register() -> None:
    rows = read_csv(CLAIMS_PATH)
    if any(row.get("claim_id") == CLAIM_ID for row in rows):
        return
    fieldnames = list(rows[0].keys()) if rows else ["claim_id", "domain", "claim", "current_evidence", "status", "next_test", "key_risk", "sector", "evidence", "next_action", "risk"]
    claim_row = {
        "claim_id": CLAIM_ID,
        "domain": "local_gr_parent_derivation",
        "claim": "The cR2 survivor now has candidate channelwise R10 mass thresholds: scalar alpha_abs=1/3, spin2 alpha_abs=4/3, with a strictest common parent-scale smoke target.",
        "current_evidence": "4456 source register, channel thresholds, curve quality, parent scale rules, supplemental acquisition status, formula rows, derivation rows, claim gates, decision, status, next target and validation CSV.",
        "status": "private_smoke_nonclaim",
        "next_test": NEXT_TARGET,
        "key_risk": "candidate curve is not an official signed alpha(lambda) table; MTS has not sourced M0/M2.",
        "sector": "local_gr_newton_r10",
        "evidence": "4456 source register, channel thresholds, curve quality, parent scale rules, supplemental acquisition status, formula rows, derivation rows, claim gates, decision, status, next target and validation CSV.",
        "next_action": NEXT_TARGET,
        "risk": "candidate curve is not an official signed alpha(lambda) table; MTS has not sourced M0/M2.",
    }
    with CLAIMS_PATH.open("a", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writerow(claim_row)


def append_marker_section(path: Path, marker: str, section: str) -> None:
    current = text(path)
    if marker in current:
        return
    write_text(path, current.rstrip() + "\n\n" + section.strip() + "\n")


def write_docs(thresholds: Sequence[Dict[str, object]], parent_rules: Sequence[Dict[str, object]], supplemental: Sequence[Dict[str, object]]) -> None:
    sources = source_rows()
    quality = curve_quality_rows(curve_rows())
    gates = claim_gate_rows(thresholds, parent_rules, supplemental)
    formulas = formula_rows()
    derivations = derivation_rows(thresholds, parent_rules)
    decisions = decision_rows(thresholds, parent_rules)
    status = status_rows()
    next_target = next_rows()
    body = f"""# 472 - PPC4161 cR2 alpha-lambda Curve Promotion or Parent M_R Scale Value

Marker: `{MARKER}`

Decision: `{DECISION}`

## Result

4456 turns the 4455 cR2 projection into a concrete channelwise mass-scale gate. It does **not** claim R10/local-GR closure.

The derived private smoke thresholds are:

{table(parent_rules)}

## Channel Thresholds

{table(thresholds)}

## Supplemental Acquisition Status

{table(supplemental)}

## Curve Quality

{table(quality)}

## Formula Rows

{table(formulas)}

## Derivation Rows

{table(derivations)}

## Claim Gates

{table(gates)}

## Decision

{table(decisions)}

## Status

{table(status)}

## Next Target

{table(next_target)}

## Source Register

{table(sources)}
"""
    write_text(FORMAL_PATH, body)
    packet = f"""# 4456 - cR2 alpha-lambda Curve Promotion or Parent M_R Scale Value

Private checkpoint. No GitHub action. No public claim.

- Derived channel thresholds for the 4455 cR2 projection using the 3702 candidate curve.
- Scalar candidate: `|alpha_0|=1/3`; spin-2 candidate: `|alpha_2|=4/3`.
- Converted each threshold to a parent mass rule `M_i >= hbar*c/lambda_star`.
- Recorded the official APS supplemental route but did not promote it to a claim table.
- Claim remains false until signed supplemental rows or parent-owned `M_0/M_2` scale/zero theorem exists.

Next target: `{NEXT_TARGET}`

Marker: `{PACKET_MARKER}`
"""
    write_text(DOC_PATH, packet)
    append_marker_section(
        SPINE_PATH,
        MARKER,
        f"""## {MARKER}

The cR2 survivor now has channelwise candidate R10 thresholds rather than an undefined generic alpha. Scalar and spin-2 channels are scored separately, and the strictest candidate common parent scale is staged as a concrete MTS derivation target. This remains nonclaim until the signed supplemental alpha(lambda) table or a parent M0/M2/zero theorem is sourced.
""",
    )
    append_marker_section(
        PACKET_PATH,
        PACKET_MARKER,
        f"""## {PACKET_MARKER}

4456 writes the channel-threshold bridge: `abs(alpha_i) <= alpha_bound(lambda_i)`, `lambda_i=hbar*c/M_i`, and candidate thresholds for `abs(alpha_0)=1/3`, `abs(alpha_2)=4/3`. The branch is not public evidence; it is a private target for deriving parent scales or sourcing the signed supplemental table.
""",
    )


def validation_rows() -> List[Dict[str, object]]:
    gates = read_csv(CLAIM_GATES)
    thresholds = read_csv(CHANNEL_THRESHOLDS)
    quality = read_csv(CURVE_QUALITY)
    supplemental = read_csv(SUPPLEMENTAL_STATUS)
    checks = [
        ("VAL4456_0_local_sources_exist", all(row["local_path_exists"] == "True" for row in read_csv(SOURCE_REGISTER) if row["source_kind"] == "local"), "every cited local source path exists"),
        ("VAL4456_1_local_needles_found", all(row["needle_found"] == "True" for row in read_csv(SOURCE_REGISTER) if row["source_kind"] == "local"), "every cited local source needle is present"),
        ("VAL4456_2_web_sources_recorded", all(row["web_source_recorded"] == "True" for row in read_csv(SOURCE_REGISTER) if row["source_kind"] == "web"), "web source URLs recorded"),
        ("VAL4456_3_thresholds_found", all(row["threshold_found"] == "True" for row in thresholds), "scalar and spin2 candidate thresholds found"),
        ("VAL4456_4_curve_quality_pass", all(row["passed"] == "True" for row in quality), "candidate curve quality checks pass"),
        ("VAL4456_5_parent_rules_written", len(read_csv(PARENT_SCALE_RULES)) >= 4, "parent mass rules written"),
        ("VAL4456_6_supplemental_status", len(supplemental) >= 3, "supplemental acquisition status recorded"),
        ("VAL4456_7_all_claim_gates", all(row["passed"] == "True" for row in gates), "all claim gates pass"),
        ("VAL4456_8_claim_row_exists", CLAIM_ID in text(CLAIMS_PATH), "claims register contains L-298"),
        ("VAL4456_9_formal_doc", FORMAL_PATH.exists() and MARKER in text(FORMAL_PATH), "formal doc exists with marker"),
        ("VAL4456_10_post_doc", DOC_PATH.exists() and PACKET_MARKER in text(DOC_PATH), "post checkpoint doc exists"),
        ("VAL4456_11_spine_marker", MARKER in text(SPINE_PATH), "spine marker written"),
        ("VAL4456_12_packet_marker", PACKET_MARKER in text(PACKET_PATH), "packet marker written"),
        ("VAL4456_13_next_target", NEXT_TARGET in text(NEXT_CSV), "next target written"),
        ("VAL4456_14_no_claim_promotion", all(row["valid_for_claim"] == "False" for row in thresholds + read_csv(PARENT_SCALE_RULES)), "threshold/rule rows remain nonclaim"),
        ("VAL4456_15_pycache_absent", not (SCRIPT_DIR / "__pycache__").exists(), "scripts __pycache__ absent"),
    ]
    return [{"checkpoint": CHECKPOINT, "check_id": check_id, "passed": passed, "detail": detail} for check_id, passed, detail in checks]


def main() -> None:
    curve = curve_rows()
    channels = channel_input_rows()
    thresholds = [evaluate_channel_threshold(row, curve) for row in channels]
    parent_rules = parent_scale_rule_rows(thresholds)
    supplemental = supplemental_status_rows()
    write_csv(SOURCE_REGISTER, source_rows())
    write_csv(CHANNEL_INPUT, channels)
    write_csv(CHANNEL_THRESHOLDS, thresholds)
    write_csv(CURVE_QUALITY, curve_quality_rows(curve))
    write_csv(PARENT_SCALE_RULES, parent_rules)
    write_csv(SUPPLEMENTAL_STATUS, supplemental)
    write_csv(FORMULA_ROWS, formula_rows())
    write_csv(DERIVATION_ROWS, derivation_rows(thresholds, parent_rules))
    write_csv(DECISION_CSV, decision_rows(thresholds, parent_rules))
    write_csv(STATUS_CSV, status_rows())
    write_csv(NEXT_CSV, next_rows())
    write_csv(CLAIM_GATES, claim_gate_rows(thresholds, parent_rules, supplemental))
    write_docs(thresholds, parent_rules, supplemental)
    update_claims_register()
    cache = SCRIPT_DIR / "__pycache__"
    if cache.exists():
        shutil.rmtree(cache)
    write_csv(VALIDATION_PATH, validation_rows())


if __name__ == "__main__":
    main()
