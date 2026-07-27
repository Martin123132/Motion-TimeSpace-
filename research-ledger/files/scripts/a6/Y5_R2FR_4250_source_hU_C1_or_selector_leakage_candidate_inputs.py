from __future__ import annotations

import csv
import math
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4250"
CLAIM_ID = "L-091"
BRANCH = "MTS_R2FR_Y5_SOURCE_HU_C1_OR_SELECTOR_LEAKAGE_CANDIDATE_INPUTS_4250"
DECISION = "LOCAL_TRANSITION_UNIT_TRANSFER_SMOKE_CANDIDATE_WRITTEN_NONCLAIM_DIRECT_HPERP_VALUES_MISSING"
MARKER = "PPC4161_HU_C1_SELECTOR_LEAKAGE_CANDIDATE_INPUTS_4250"
PACKET_MARKER = "PPC4161_PACKET_HU_C1_SELECTOR_LEAKAGE_CANDIDATE_INPUTS_4250"
NEXT_TARGET = "4251-Y5-R2FR-Hperp-memory-transfer-constant-or-real-profile-source.md"

FORMAL_PATH = FORMAL / "266-PPC4161-hU-C1-source-candidate-or-selector-leakage-inputs.md"
DOC_PATH = POST / "4250-Y5-R2FR-source-hU-C1-or-selector-leakage-candidate-inputs.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4250_VALIDATION.csv"
TARGET_4249_CANDIDATE = SOURCE_DIR / "P8_Y5_R2FR_4249_HU_RESPONSE_INPUTS_CANDIDATE.csv"

STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()


@dataclass(frozen=True)
class SourceSpec:
    source_id: str
    path: Path
    required_text: str
    role: str


SOURCE_SPECS: Dict[str, SourceSpec] = {
    "SRC4250_00_4249_formal": SourceSpec(
        "SRC4250_00_4249_formal",
        FORMAL / "265-PPC4161-hU-response-bound-or-coframe-transfer-first-source-row.md",
        "h_U_C1 <= C_shape*A_H*(L_U/ell_tr)+eta_corner",
        "4249 transition-width response law.",
    ),
    "SRC4250_01_4249_schema": SourceSpec(
        "SRC4250_01_4249_schema",
        SOURCE_DIR / "P8_Y5_R2FR_4249_HU_RESPONSE_INPUT_SCHEMA.csv",
        "L_U_over_ell_tr",
        "4249 candidate input schema.",
    ),
    "SRC4250_02_4249_script": SourceSpec(
        "SRC4250_02_4249_script",
        POST / "scripts" / "Y5_R2FR_4249_fill_hU_response_or_coframe_transfer_constant_first_source_row.py",
        "P8_Y5_R2FR_4249_HU_RESPONSE_INPUTS_CANDIDATE.csv",
        "4249 runner reads the candidate written by 4250.",
    ),
    "SRC4250_03_extremum_results": SourceSpec(
        "SRC4250_03_extremum_results",
        FORMAL / "66-local-extremum-amplitude-law-first-results.md",
        "M_tr = 1e-7",
        "Conditional local transition amplitude and optimal width example.",
    ),
    "SRC4250_04_projection_results": SourceSpec(
        "SRC4250_04_projection_results",
        FORMAL / "68-projection-locking-first-results.md",
        "0.10183599369679364 <= ell_tr/L_cg <= 19.639421459909464",
        "Safe transition-width interval from projection-locking dry run.",
    ),
    "SRC4250_05_relaxation_results": SourceSpec(
        "SRC4250_05_relaxation_results",
        FORMAL / "70-relaxation-functional-lock-first-results.md",
        "M_tr_bound = 1.0000453999297624e-7",
        "Conditional relaxation/support amplitude bound.",
    ),
    "SRC4250_06_variable_audit": SourceSpec(
        "SRC4250_06_variable_audit",
        FORMAL / "04-variable-audit.csv",
        "M_total=1.0005539992976248e-8",
        "Variable audit records M_tr, ell_tr, e_opt and safe interval status.",
    ),
    "SRC4250_07_equation_register": SourceSpec(
        "SRC4250_07_equation_register",
        FORMAL / "05-equation-register.md",
        "ell_tr/L_cg,opt = 1.4142135623730951",
        "Equation register records projection-locking numeric dry-run values.",
    ),
}


def common() -> Dict[str, str]:
    return {
        "checkpoint": CHECKPOINT,
        "branch": BRANCH,
        "generated_utc": STAMP,
        "decision": DECISION,
    }


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.strip() + "\n", encoding="utf-8")


def write_csv(path: Path, rows: List[Dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: List[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def csv_rows(path: Path) -> List[Dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def append_once(path: Path, marker: str, block: str) -> None:
    current = read_text(path)
    if marker in current:
        return
    write_text(path, current.rstrip() + "\n\n" + block.strip())


def first_float(pattern: str, text: str) -> Optional[float]:
    match = re.search(pattern, text, flags=re.IGNORECASE)
    if not match:
        return None
    try:
        return float(match.group(1).rstrip("."))
    except ValueError:
        return None


def all_floats(pattern: str, text: str) -> List[float]:
    values: List[float] = []
    for match in re.finditer(pattern, text, flags=re.IGNORECASE):
        try:
            values.append(float(match.group(1).rstrip(".")))
        except ValueError:
            continue
    return values


def preferred_m_tr(text: str) -> Optional[float]:
    values = all_floats(r"M_tr\s*=\s*([0-9.eE+-]+)", text)
    for value in values:
        if abs(value - 1e-7) <= 1e-20:
            return value
    return values[-1] if values else None


def source_rows() -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    for spec in SOURCE_SPECS.values():
        text = read_text(spec.path)
        rows.append(
            {
                **common(),
                "source_id": spec.source_id,
                "path": str(spec.path),
                "exists": str(spec.path.exists()),
                "required_text": spec.required_text,
                "required_text_found": str(spec.required_text in text),
                "role": spec.role,
                "valid_for_claim": "False",
            }
        )
    return rows


def extracted_values() -> Dict[str, Optional[float]]:
    text66 = read_text(FORMAL / "66-local-extremum-amplitude-law-first-results.md")
    text68 = read_text(FORMAL / "68-projection-locking-first-results.md")
    text70 = read_text(FORMAL / "70-relaxation-functional-lock-first-results.md")
    e_opt = first_float(r"e_opt\s*=\s*([0-9.eE+-]+)", text66) or first_float(
        r"ell_tr/L_cg\s*=\s*([0-9.eE+-]+)", text66
    )
    m_tr = preferred_m_tr(text66)
    m_tr_max = first_float(r"M_tr,max\s*=\s*([0-9.eE+-]+)", text68)
    m_tr_bound = first_float(r"M_tr_bound\s*=\s*([0-9.eE+-]+)", text70)
    interval = re.search(
        r"([0-9.eE+-]+)\s*<=\s*ell_tr/L_cg\s*<=\s*([0-9.eE+-]+)",
        text68,
    )
    safe_low = float(interval.group(1).rstrip(".")) if interval else None
    safe_high = float(interval.group(2).rstrip(".")) if interval else None
    return {
        "M_tr_example": m_tr,
        "ell_tr_over_Lcg_opt": e_opt,
        "Lcg_over_ell_tr_opt": (1.0 / e_opt) if e_opt and e_opt > 0 else None,
        "M_tr_max_projection": m_tr_max,
        "M_tr_bound_relaxation": m_tr_bound,
        "safe_ell_over_Lcg_low": safe_low,
        "safe_ell_over_Lcg_high": safe_high,
    }


def extraction_rows() -> List[Dict[str, str]]:
    values = extracted_values()
    rows: List[Dict[str, str]] = []
    source_map = {
        "M_tr_example": FORMAL / "66-local-extremum-amplitude-law-first-results.md",
        "ell_tr_over_Lcg_opt": FORMAL / "66-local-extremum-amplitude-law-first-results.md",
        "Lcg_over_ell_tr_opt": FORMAL / "66-local-extremum-amplitude-law-first-results.md",
        "M_tr_max_projection": FORMAL / "68-projection-locking-first-results.md",
        "M_tr_bound_relaxation": FORMAL / "70-relaxation-functional-lock-first-results.md",
        "safe_ell_over_Lcg_low": FORMAL / "68-projection-locking-first-results.md",
        "safe_ell_over_Lcg_high": FORMAL / "68-projection-locking-first-results.md",
    }
    for symbol, value in values.items():
        rows.append(
            {
                **common(),
                "symbol": symbol,
                "value": "MISSING" if value is None else f"{value:.17g}",
                "units": "dimensionless",
                "source_path": str(source_map[symbol]),
                "extraction_status": "FOUND_NUMERIC_CONDITIONAL" if value is not None else "MISSING",
                "claim_status": "NONCLAIM_CONDITIONAL_LOCAL_TRANSITION_VALUE",
                "valid_for_claim": "False",
            }
        )
    return rows


def crosswalk_rows() -> List[Dict[str, str]]:
    raw = [
        (
            "HMC4250_0_no_identity",
            "M_tr is not Hperp",
            "M_tr is a local memory transition amplitude. It may only feed Hperp through a parent-owned transfer map Hperp=T_H[m,q_obs,X_Q,...].",
            "NO_SMUGGLE_RULE",
            "Prevents importing old local-transition numbers as EM/Hperp evidence.",
            "MISSING_HPERP_MEMORY_TRANSFER_MAP",
        ),
        (
            "HMC4250_1_amplitude_crosswalk",
            "amplitude transfer",
            "If ||T_H(m)-T_H(m_L)||_F/F_ref <= C_HM0 |m-m_L| + eta_H_background, then A_H <= C_HM0*M_tr + eta_H_background.",
            "CONDITIONAL_LIPSCHITZ_TRANSFER_THEOREM",
            "Turns M_tr into a possible Hperp amplitude input if C_HM0 is derived or sourced.",
            "MISSING_C_HM0_AND_ETA_H_BACKGROUND",
        ),
        (
            "HMC4250_2_C1_crosswalk",
            "C1 derivative transfer",
            "If ||nabla T_H||/(F_ref/L_cg) <= C_HM1*M_tr*(L_cg/ell_tr)+eta_H_C1, then h_U_C1 <= C_HM1*M_tr*(Lcg/ell_tr)+eta_H_C1.",
            "CONDITIONAL_C1_TRANSFER_THEOREM",
            "Makes the 4249 C1 route sourceable from local transition shape data.",
            "MISSING_C_HM1_AND_ETA_H_C1",
        ),
        (
            "HMC4250_3_unit_transfer_smoke",
            "unit-transfer smoke row",
            "Set C_HM0=C_HM1=C_qinv=C_shape=C_coframe_hU=1 and eta terms/Omega_E=0 only as a pipeline smoke assumption, never as a physics claim.",
            "SMOKE_ONLY_ASSUMPTION",
            "Checks the scale that would flow through the 4249 runner if the transfer were unit-normalized.",
            "NOT_PARENT_SIGNED_NOT_VALID_FOR_CLAIM",
        ),
        (
            "HMC4250_4_selector_route_status",
            "selector route remains unfilled",
            "No numeric C_HY, epsilon_YV, eta_chart_transition, or eta_degen was found in the current corpus sweep.",
            "SEARCH_RESULT",
            "The selector route is still a derivation/source target, not this turn's filled path.",
            "MISSING_SELECTOR_LEAKAGE_VALUES",
        ),
    ]
    return [
        {
            **common(),
            "theorem_id": theorem_id,
            "claim_piece": claim_piece,
            "mathematical_form": mathematical_form,
            "derivation_status": status,
            "result_if_signed": result,
            "missing_for_current_claim": missing,
            "valid_for_claim": "False",
        }
        for theorem_id, claim_piece, mathematical_form, status, result, missing in raw
    ]


def smoke_candidate_row() -> Dict[str, str]:
    values = extracted_values()
    m_tr = values["M_tr_example"] or math.nan
    lcg_over_ell = values["Lcg_over_ell_tr_opt"] or math.nan
    h_u_c1 = m_tr * lcg_over_ell if math.isfinite(m_tr) and math.isfinite(lcg_over_ell) else math.nan
    source_path = FORMAL / "66-local-extremum-amplitude-law-first-results.md"
    return {
        **common(),
        "candidate_id": "HU4250_LOCAL_TRANSITION_UNIT_TRANSFER_SMOKE",
        "route_preference": "transition_route_smoke",
        "parent_zero_authority": "false",
        "C_HY": "MISSING",
        "epsilon_YV": "MISSING",
        "eta_chart_transition": "MISSING",
        "eta_degen": "MISSING",
        "C_qinv": "1.0",
        "h_U_C1": "MISSING" if not math.isfinite(h_u_c1) else f"{h_u_c1:.17g}",
        "h_U_profile": "MISSING" if not math.isfinite(m_tr) else f"{m_tr:.17g}",
        "Omega_E": "0.0",
        "eta_Lie_frame": "0.0",
        "C_shape": "1.0",
        "A_H": "MISSING" if not math.isfinite(m_tr) else f"{m_tr:.17g}",
        "L_U_over_ell_tr": "MISSING" if not math.isfinite(lcg_over_ell) else f"{lcg_over_ell:.17g}",
        "eta_corner": "0.0",
        "C_coframe_hU": "1.0",
        "source_path": str(source_path),
        "claim_authority": "UNIT_TRANSFER_SMOKE_NOT_PARENT_SIGNED",
        "valid_for_claim": "False",
        "notes": "Nonclaim scale smoke: identifies what would flow through 4249 if Hperp tracked M_tr with unit transfer and zero remainders.",
    }


def candidate_rows() -> List[Dict[str, str]]:
    return [smoke_candidate_row()]


def smoke_result_rows() -> List[Dict[str, str]]:
    row = smoke_candidate_row()
    m_tr = float(row["A_H"]) if row["A_H"] != "MISSING" else math.nan
    lcg_over_ell = float(row["L_U_over_ell_tr"]) if row["L_U_over_ell_tr"] != "MISSING" else math.nan
    h_u_c1 = float(row["h_U_C1"]) if row["h_U_C1"] != "MISSING" else math.nan
    transition_bound = m_tr * lcg_over_ell if math.isfinite(m_tr) and math.isfinite(lcg_over_ell) else math.nan
    return [
        {
            **common(),
            "candidate_id": row["candidate_id"],
            "M_tr_proxy": row["A_H"],
            "Lcg_over_ell_tr_proxy": row["L_U_over_ell_tr"],
            "h_U_C1_proxy": row["h_U_C1"],
            "transition_h_U_response_proxy": "MISSING" if not math.isfinite(transition_bound) else f"{transition_bound:.17g}",
            "C1_h_U_response_proxy": "MISSING" if not math.isfinite(h_u_c1) else f"{h_u_c1:.17g}",
            "source_path_exists": str(Path(row["source_path"]).exists()),
            "interpretation": "pipeline smoke only; transfer constants and zero remainders are assumptions",
            "scoreable_now": "True" if math.isfinite(transition_bound) else "False",
            "valid_for_claim": "False",
        }
    ]


def refusal_rows() -> List[Dict[str, str]]:
    raw = [
        ("RF4250_0_transfer_unsigned", "C_HM0/C_HM1 are not derived", "M_tr proxy cannot become Hperp evidence."),
        ("RF4250_1_unit_constants", "C_qinv/C_shape/C_coframe_hU set to 1 only for smoke", "No arena claim or local-GR claim."),
        ("RF4250_2_zero_remainders", "Omega_E and eta terms set to zero only for smoke", "Need frame/regularity certificates."),
        ("RF4250_3_selector_missing", "C_HY/epsilon_YV/eta_chart/eta_degen not found", "Selector route remains unfilled."),
        ("RF4250_4_old_branch_conditional", "M_tr and ell_tr/Lcg source rows are conditional dry-runs", "They are useful scale probes, not final evidence."),
    ]
    return [
        {
            **common(),
            "gate_id": gate_id,
            "blocked_shortcut": shortcut,
            "reason": reason,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for gate_id, shortcut, reason in raw
    ]


def decision_rows() -> List[Dict[str, str]]:
    raw = [
        (
            "DEC4250_0_progress",
            "first numeric smoke candidate written",
            "The corpus contains conditional local-transition scale values; 4250 maps them into a 4249 candidate only under explicit unit-transfer smoke assumptions.",
            "Rerun 4249 to compute a nonclaim h_U_response proxy.",
        ),
        (
            "DEC4250_1_current_nonclaim",
            "direct Hperp and selector values remain missing",
            "No source-backed Hperp profile, C_HM transfer, or selector-leakage tuple was found.",
            "Keep valid_for_claim=false and attack C_HM0/C_HM1 or real profile acquisition next.",
        ),
        (
            "DEC4250_2_next",
            "derive Hperp-memory transfer or source real profile",
            "The most valuable next move is to prove or bound Hperp=T_H[M_tr] rather than adding more proxy rows.",
            NEXT_TARGET,
        ),
    ]
    return [
        {
            **common(),
            "decision_id": decision_id,
            "decision": decision,
            "rationale": rationale,
            "action": action,
            "valid_for_claim": "False",
        }
        for decision_id, decision, rationale, action in raw
    ]


def status_rows() -> List[Dict[str, str]]:
    result = smoke_result_rows()[0]
    return [
        {
            **common(),
            "status": DECISION,
            "summary": f"4250 found conditional local transition values and wrote a nonclaim 4249 smoke candidate with h_U_response proxy {result['transition_h_U_response_proxy']}. Direct Hperp/selector inputs remain missing.",
            "scoreable_now": "True",
            "valid_for_claim": "False",
        }
    ]


def next_target_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "next_target": NEXT_TARGET,
            "objective": "Derive or source C_HM0/C_HM1 linking local memory transition amplitude to Hperp amplitude/C1 response, or acquire a real Hperp profile directly.",
            "avoid": "Do not promote the unit-transfer smoke row, do not set eta terms to zero as physics, and do not claim local-GR/PPN/R10/clock/orbital closure.",
            "valid_for_claim": "False",
        }
    ]


def append_claim_row() -> None:
    path = FORMAL / "02-claims-register.csv"
    current = read_text(path)
    if f"{CLAIM_ID}," in current:
        return
    row = [
        CLAIM_ID,
        "local_gr",
        "4250 writes the first numeric nonclaim h_U_response smoke candidate by crosswalking conditional local-transition values M_tr and ell_tr/L_cg into the 4249 candidate schema under explicit unit-transfer assumptions.",
        "4250 source register, transition value extraction, Hperp-memory crosswalk theorem, candidate row, smoke result, refusal gates, decision and firewall.",
        "private_hU_unit_transfer_smoke_candidate_nonclaim_direct_Hperp_values_missing",
        "Derive C_HM0/C_HM1 or source a real Hperp C1 profile, then replace the smoke row with source-backed candidate inputs.",
        "Using M_tr as Hperp without a parent transfer map, or using unit constants/zero remainders as physics, would smuggle local-GR safety.",
    ]
    with path.open("a", newline="", encoding="utf-8") as handle:
        csv.writer(handle).writerow(row)


def write_formal_doc() -> None:
    result = smoke_result_rows()[0]
    text = f"""
# 266 - PPC4161 h_U C1 source candidate or selector-leakage inputs

Marker: `{MARKER}`

Branch: `{BRANCH}`

Decision: `{DECISION}`

## Claim Status

Private nonclaim. 4250 does not prove local GR, PPN safety, R10 safety, clock safety, orbital safety, or Hperp smallness. It writes a numeric smoke candidate only to exercise the 4249 response-bound runner.

## What Was Found

The current corpus contains conditional local-transition scale values:

```text
M_tr = 1e-7
ell_tr/L_cg = 1.4142135623730951
L_cg/ell_tr = 0.7071067811865475
```

These come from the local extremum/projection-locking branch, not from a direct Hperp profile. Therefore they cannot be used as evidence unless a transfer map is derived.

## Crosswalk Theorem

The safe statement is:

```text
A_H <= C_HM0 M_tr + eta_H_background
h_U_C1 <= C_HM1 M_tr (L_cg/ell_tr) + eta_H_C1
```

Only after `C_HM0`, `C_HM1`, and the eta terms are parent-derived or source-backed can the old local-transition values become real 4249 inputs.

## Smoke Candidate

4250 writes:

```text
P8_Y5_R2FR_4249_HU_RESPONSE_INPUTS_CANDIDATE.csv
```

with a deliberately nonclaim unit-transfer row:

```text
C_qinv=C_shape=C_coframe_hU=1,
Omega_E=eta_Lie_frame=eta_corner=0,
A_H=M_tr,
L_U/ell_tr=L_cg/ell_tr.
```

The resulting smoke-scale proxy is:

```text
h_U_response_proxy = {result["transition_h_U_response_proxy"]}
```

This is useful as a pipeline scale check only. It is not physics evidence.

## Next Target

`{NEXT_TARGET}` should derive `C_HM0/C_HM1` or acquire a real Hperp profile. That is the next honest route from proxy smoke to actual local-GR evidence.
"""
    write_text(FORMAL_PATH, text)


def write_checkpoint_doc() -> None:
    result = smoke_result_rows()[0]
    text = f"""
# 4250 - source h_U C1 or selector-leakage candidate inputs

**Status:** `{DECISION}`.

## Result

4250 found conditional local-transition values and wrote the first 4249 candidate input row as a nonclaim smoke test.

```text
M_tr proxy = {result["M_tr_proxy"]}
Lcg/ell_tr proxy = {result["Lcg_over_ell_tr_proxy"]}
h_U_response proxy = {result["transition_h_U_response_proxy"]}
```

## Current state

Direct Hperp profile values, selector-leakage values, and the memory-to-Hperp transfer constants remain missing. The candidate row is explicitly `valid_for_claim=false`.

## Next target

`{NEXT_TARGET}`
"""
    write_text(DOC_PATH, text)


def update_spine_and_packet() -> None:
    result = smoke_result_rows()[0]
    spine_block = f"""
## PPC4161 h_U C1 / selector-leakage candidate inputs

Marker: `{MARKER}`

4250 finds a useful but nonclaim scale probe. Conditional local-transition rows give:

```text
M_tr = {result["M_tr_proxy"]},
L_cg/ell_tr = {result["Lcg_over_ell_tr_proxy"]},
h_U_response_proxy = {result["transition_h_U_response_proxy"]}.
```

This is only a unit-transfer smoke candidate. The branch still needs a parent/source transfer map from memory transition amplitude to Hperp amplitude/C1 response.
"""
    packet_block = f"""
## Packet Update - h_U C1 / selector-leakage candidate inputs

Marker: `{PACKET_MARKER}`

The local packet now has a nonclaim numeric smoke row for the 4249 response runner. It is deliberately firewalled: `M_tr` is not `Hperp` unless the transfer constants `C_HM0/C_HM1` are derived or sourced.
"""
    append_once(FORMAL / "07-unification-spine.md", MARKER, spine_block)
    append_once(FORMAL / "180-PPC4161-private-local-packet-integration.md", PACKET_MARKER, packet_block)


def validation_rows(outputs: Dict[str, Path]) -> List[Dict[str, str]]:
    sources = source_rows()
    extraction = extraction_rows()
    candidate = smoke_candidate_row()
    result = smoke_result_rows()[0]
    validations = [
        ("VAL4250_0_sources_exist", all(row["exists"] == "True" for row in sources), "all source paths exist"),
        ("VAL4250_1_needles_found", all(row["required_text_found"] == "True" for row in sources), "all source needles found"),
        ("VAL4250_2_numeric_extraction", all(row["value"] != "MISSING" for row in extraction), "all transition values extracted"),
        ("VAL4250_3_candidate_written", TARGET_4249_CANDIDATE.exists(), "4249 candidate file written"),
        ("VAL4250_4_candidate_nonclaim", candidate["valid_for_claim"] == "False", "candidate remains nonclaim"),
        ("VAL4250_5_candidate_source_exists", Path(candidate["source_path"]).exists(), "candidate source path exists"),
        ("VAL4250_6_smoke_result_numeric", result["transition_h_U_response_proxy"] != "MISSING", "smoke response proxy computed"),
        ("VAL4250_7_transfer_firewall", all(row["valid_for_claim"] == "False" for row in refusal_rows()), "all refusal gates closed"),
        ("VAL4250_8_formal_doc", FORMAL_PATH.exists() and MARKER in read_text(FORMAL_PATH), "formal doc written"),
        ("VAL4250_9_checkpoint_doc", DOC_PATH.exists() and DECISION in read_text(DOC_PATH), "checkpoint doc written"),
        ("VAL4250_10_claim_row", f"{CLAIM_ID}," in read_text(FORMAL / "02-claims-register.csv"), "claim register row added"),
        ("VAL4250_11_spine_marker", MARKER in read_text(FORMAL / "07-unification-spine.md"), "spine marker present"),
        ("VAL4250_12_packet_marker", PACKET_MARKER in read_text(FORMAL / "180-PPC4161-private-local-packet-integration.md"), "packet marker present"),
    ]
    for name, path in outputs.items():
        validations.append((f"VAL4250_csv_{name}", bool(csv_rows(path)), f"{path.name} parses"))
    return [
        {
            **common(),
            "check_id": check_id,
            "description": description,
            "passed": str(passed),
            "evidence": "generated_artifacts",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for check_id, passed, description in validations
    ]


def main() -> None:
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)
    outputs = {
        "source_register": SOURCE_DIR / "P8_Y5_R2FR_4250_SOURCE_REGISTER.csv",
        "transition_extraction": SOURCE_DIR / "P8_Y5_R2FR_4250_TRANSITION_VALUE_EXTRACTION.csv",
        "crosswalk_theorems": SOURCE_DIR / "P8_Y5_R2FR_4250_HPERP_MEMORY_CROSSWALK_THEOREMS.csv",
        "candidate_rows": SOURCE_DIR / "P8_Y5_R2FR_4250_HU_RESPONSE_CANDIDATE_ROWS.csv",
        "smoke_result": SOURCE_DIR / "P8_Y5_R2FR_4250_UNIT_TRANSFER_SMOKE_RESULT.csv",
        "refusal_gates": SOURCE_DIR / "P8_Y5_R2FR_4250_REFUSAL_GATES.csv",
        "decision": SOURCE_DIR / "P8_Y5_R2FR_4250_DECISION.csv",
        "status": SOURCE_DIR / "P8_Y5_R2FR_4250_STATUS.csv",
        "next_target": SOURCE_DIR / "P8_Y5_R2FR_4250_NEXT_TARGET.csv",
    }

    write_formal_doc()
    write_checkpoint_doc()
    append_claim_row()
    update_spine_and_packet()

    write_csv(outputs["source_register"], source_rows())
    write_csv(outputs["transition_extraction"], extraction_rows())
    write_csv(outputs["crosswalk_theorems"], crosswalk_rows())
    write_csv(outputs["candidate_rows"], candidate_rows())
    write_csv(outputs["smoke_result"], smoke_result_rows())
    write_csv(outputs["refusal_gates"], refusal_rows())
    write_csv(outputs["decision"], decision_rows())
    write_csv(outputs["status"], status_rows())
    write_csv(outputs["next_target"], next_target_rows())
    write_csv(TARGET_4249_CANDIDATE, candidate_rows())
    write_csv(VALIDATION_PATH, validation_rows(outputs))

    validation = csv_rows(VALIDATION_PATH)
    failed = [row for row in validation if row["passed"] != "True"]
    print(f"{CHECKPOINT}: wrote {len(outputs)} csv artifacts")
    print(f"{CHECKPOINT}: wrote 4249 candidate {TARGET_4249_CANDIDATE.name}")
    print(f"{CHECKPOINT}: validation rows={len(validation)} failed={len(failed)}")
    print(f"{CHECKPOINT}: decision={DECISION}")


if __name__ == "__main__":
    main()
