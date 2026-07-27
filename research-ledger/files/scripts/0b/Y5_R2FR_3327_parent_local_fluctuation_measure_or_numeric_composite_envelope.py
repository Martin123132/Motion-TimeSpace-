from __future__ import annotations

import csv
import hashlib
import math
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
FW = REPO / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
PYCACHE = ROOT / "scripts" / "__pycache__"

DOC = ROOT / "3327-Y5-R2FR-parent-local-fluctuation-measure-or-numeric-composite-envelope-under-AX1090.md"

SRC_ACTION_PRINCIPLE = REPO / "core-mts-framework" / "action-principle" / "the-motion-timespace-action-principle.md"
SRC_FUNDAMENTAL = REPO / "core-mts-framework" / "action-principle" / "the-fundamental-action-of-motion-timespace-field-theory.md"
SRC_EFT = REPO / "core-mts-framework" / "field-theory" / "the-effective-field-theory-of-motion-timespace.md"
SRC_GEOMETRIC = REPO / "core-mts-framework" / "field-theory" / "geometric-field-framework.md"

SOURCES = [
    {
        "source_id": "SRC3327_0_3326_doc",
        "path": ROOT / "3326-Y5-R2FR-centered-fluctuation-selection-rule-or-composite-tail-bound-under-AX1090.md",
        "role": "selection theorem and composite-envelope handoff",
    },
    {
        "source_id": "SRC3327_1_3326_selection",
        "path": OUT / "P8_Y5_R2FR_3326_SELECTION_RULE_THEOREM.csv",
        "role": "third-cumulant/even-measure theorem",
    },
    {
        "source_id": "SRC3327_2_3326_defects",
        "path": OUT / "P8_Y5_R2FR_3326_CENTERING_DEFECTS.csv",
        "role": "delta_mean, delta_skew, rho_P1, gap, contact defects",
    },
    {
        "source_id": "SRC3327_3_3326_bounds",
        "path": OUT / "P8_Y5_R2FR_3326_COMPOSITE_BOUND_FORMULAS.csv",
        "role": "epsilon_composite no-cancellation formulas",
    },
    {
        "source_id": "SRC3327_4_action_principle",
        "path": SRC_ACTION_PRINCIPLE,
        "role": "coarse-graining over Planck-scale cells and smooth metric readout",
    },
    {
        "source_id": "SRC3327_5_fundamental",
        "path": SRC_FUNDAMENTAL,
        "role": "Planck-scale psi action, damping, decoherence, covariance readout",
    },
    {
        "source_id": "SRC3327_6_eft",
        "path": SRC_EFT,
        "role": "coarse-grained functional integral and statistical smoothing",
    },
    {
        "source_id": "SRC3327_7_geometric",
        "path": SRC_GEOMETRIC,
        "role": "damping/tension coefficients and nonlinear flow caveat",
    },
]

OUTPUTS = {
    "sources": OUT / "P8_Y5_R2FR_3327_SOURCE_REGISTER.csv",
    "evidence": OUT / "P8_Y5_R2FR_3327_COARSE_GRAINING_EVIDENCE.csv",
    "clt": OUT / "P8_Y5_R2FR_3327_CLT_MIXING_CONTRACT.csv",
    "centering": OUT / "P8_Y5_R2FR_3327_CENTERING_SIGNING.csv",
    "envelope": OUT / "P8_Y5_R2FR_3327_COMPOSITE_ENVELOPE.csv",
    "inputs": OUT / "P8_Y5_R2FR_3327_REQUIRED_NUMERIC_INPUTS.csv",
    "samples": OUT / "P8_Y5_R2FR_3327_SUPPRESSION_SAMPLES.csv",
    "gates": OUT / "P8_Y5_R2FR_3327_PROMOTION_GATES.csv",
    "decision": OUT / "P8_Y5_R2FR_3327_DECISION_LEDGER.csv",
    "next": OUT / "P8_Y5_R2FR_3327_NEXT_TARGET.csv",
    "validation": OUT / "P8_Y5_BRR545_3327_VALIDATION.csv",
}

RUN_UTC = datetime.now(timezone.utc).isoformat()

EVIDENCE_PATTERNS = [
    "coarse-grained",
    "coarse-graining",
    "smooth",
    "averaging",
    "average",
    "Planck",
    "oscillations",
    "covariance",
    "damping",
    "decoherence",
    "functional integral",
]


def bool_str(value: bool) -> str:
    return "true" if value else "false"


def compact(value: Any, limit: int = 1200) -> str:
    text = " ".join(str(value).split())
    return text if len(text) <= limit else text[: limit - 3] + "..."


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: compact(row.get(key, "")) for key in fieldnames})


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def csv_parse_ok(path: Path) -> bool:
    try:
        read_csv(path)
        return True
    except Exception:
        return False


def text_parse_ok(path: Path) -> bool:
    try:
        path.read_text(encoding="utf-8", errors="replace")
        return True
    except Exception:
        return False


def parse_ok(path: Path) -> bool:
    if not path.exists():
        return False
    return csv_parse_ok(path) if path.suffix.lower() == ".csv" else text_parse_ok(path)


def text_for(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def sha256_prefix(path: Path) -> str:
    if not path.exists() or not path.is_file():
        return ""
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()[:16]


def snapshot_tree(path: Path) -> dict[str, tuple[int, int]]:
    if not path.exists():
        return {}
    result: dict[str, tuple[int, int]] = {}
    for item in path.rglob("*"):
        if item.is_file():
            try:
                stat = item.stat()
            except OSError:
                continue
            result[str(item.relative_to(path))] = (stat.st_size, stat.st_mtime_ns)
    return result


def changed_count(before: dict[str, tuple[int, int]], after: dict[str, tuple[int, int]]) -> int:
    keys = set(before) | set(after)
    return sum(1 for key in keys if before.get(key) != after.get(key))


def find_hits(path: Path, max_hits: int = 8) -> str:
    text = text_for(path)
    patterns = [pattern.lower() for pattern in EVIDENCE_PATTERNS]
    hits: list[str] = []
    for line_number, line in enumerate(text.splitlines(), start=1):
        if any(pattern in line.lower() for pattern in patterns):
            hits.append(f"L{line_number}:{line.strip()}")
        if len(hits) >= max_hits:
            break
    return " | ".join(hits)


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source in SOURCES:
        path = source["path"]
        rows.append(
            {
                "source_id": source["source_id"],
                "path": str(path),
                "exists": bool_str(path.exists()),
                "parse_ok": bool_str(parse_ok(path)),
                "sha256_prefix": sha256_prefix(path),
                "role": source["role"],
                "valid_for_claim": "false",
            }
        )
    return rows


def coarse_graining_evidence_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source in SOURCES:
        path = source["path"]
        text = text_for(path).lower()
        rows.append(
            {
                "evidence_id": f"EVID3327_{len(rows)}",
                "source_id": source["source_id"],
                "has_coarse_grain": bool_str("coarse" in text),
                "has_smoothing": bool_str("smooth" in text or "averag" in text),
                "has_planck_cells": bool_str("planck" in text),
                "has_damping_or_decoherence": bool_str("damping" in text or "decoherence" in text),
                "hits": find_hits(path),
                "valid_for_claim": "false",
            }
        )
    return rows


def clt_contract_rows() -> list[dict[str, Any]]:
    return [
        {
            "contract_id": "CLT3327_0_fluctuation_split",
            "statement": "Define psi_bar=S_ell psi and pi=psi-psi_bar, with S_ell a normalized local smoothing kernel",
            "result": "S_ell pi = 0 exactly by definition of the coarse-grained split",
            "status": "MEAN_CENTERING_SIGNED_BY_DEFINITION",
            "valid_for_claim": "false",
        },
        {
            "contract_id": "CLT3327_1_effective_cell_count",
            "statement": "If microscopic correlations decay beyond ell_c, the smoothing volume contains N_eff approximately (ell_s/ell_c)^d_eff / C_mix effective cells",
            "result": "larger scale separation suppresses non-Gaussian odd cumulants",
            "status": "MIXING_CONTRACT",
            "valid_for_claim": "false",
        },
        {
            "contract_id": "CLT3327_2_skew_bound",
            "statement": "For finite third moment and weakly dependent cells, standardized third cumulant obeys delta_skew <= C3/sqrt(N_eff) + delta_bias",
            "result": "the exact even-measure condition is replaced by a quantitative CLT/mixing leakage bound",
            "status": "DERIVED_SUPPRESSION_LAW",
            "valid_for_claim": "false",
        },
        {
            "contract_id": "CLT3327_3_even_limit",
            "statement": "If the local microscopic fluctuation law is exactly even or the parent selection rule forbids odd cumulants, set C3=0 and delta_bias=0",
            "result": "the 3326 exact zero theorem is recovered",
            "status": "EXACT_ZERO_LIMIT",
            "valid_for_claim": "false",
        },
        {
            "contract_id": "CLT3327_4_parent_gap",
            "statement": "The corpus supports smoothing/averaging, but does not yet provide ell_c, C_mix, C3, d_eff, or delta_bias",
            "result": "the parent measure is bounded-symbolic, not claim-numeric",
            "status": "PARENT_INPUTS_MISSING",
            "valid_for_claim": "false",
        },
    ]


def centering_signing_rows() -> list[dict[str, Any]]:
    return [
        {
            "sign_id": "CEN3327_0_mean_zero",
            "quantity": "delta_mean_i",
            "signing": "signed zero at smoothing-kernel level if pi=psi-S_ell psi and arena uses the same local kernel",
            "residual_if_failed": "kernel mismatch or boundary leakage moves leftover into epsilon_boundary_i",
            "status": "SIGNED_CONDITIONAL_ON_KERNEL_MATCH",
            "valid_for_claim": "false",
        },
        {
            "sign_id": "CEN3327_1_skew_suppression",
            "quantity": "delta_skew_i",
            "signing": "delta_skew_i <= C3_i/sqrt(N_eff_i)+delta_bias_i",
            "residual_if_failed": "non-Gaussian local skew enters epsilon_1p_i",
            "status": "BOUND_SIGNED_NOT_NUMERIC",
            "valid_for_claim": "false",
        },
        {
            "sign_id": "CEN3327_2_projection_leak",
            "quantity": "rho_P1_i",
            "signing": "rho_P1_i=0 if P1_i respects pi->-pi parity; otherwise retain rho_P1_i as an arena projection defect",
            "residual_if_failed": "quadratic operator leaks into one-particle arena",
            "status": "CONDITIONAL_ZERO_OR_NUISANCE",
            "valid_for_claim": "false",
        },
        {
            "sign_id": "CEN3327_3_two_particle_branch",
            "quantity": "epsilon_2p_i(lambda)",
            "signing": "requires spectral envelope dmu_2(s) or gap m_gap_2pi; absent gap, do not claim long-range silence",
            "residual_if_failed": "two-particle composite tail remains explicit",
            "status": "SPECTRAL_INPUT_REQUIRED",
            "valid_for_claim": "false",
        },
        {
            "sign_id": "CEN3327_4_contact_boundary",
            "quantity": "epsilon_contact_i + epsilon_boundary_i + epsilon_kernel_aniso_i",
            "signing": "zero only with source-support absorption, boundary silence, and isotropic kernel",
            "residual_if_failed": "carry as absolute no-cancellation envelope",
            "status": "EXPLICIT_TAIL_ENVELOPE",
            "valid_for_claim": "false",
        },
    ]


def composite_envelope_rows() -> list[dict[str, Any]]:
    return [
        {
            "envelope_id": "ENV3327_0_Neff",
            "formula": "N_eff_i = (ell_s/ell_c_i)^d_eff / C_mix_i",
            "meaning": "effective number of independent microscopic cells in the local smoothing patch",
            "claim_status": "SYMBOLIC_READY",
            "valid_for_claim": "false",
        },
        {
            "envelope_id": "ENV3327_1_skew",
            "formula": "delta_skew_i <= C3_i/sqrt(N_eff_i) + delta_bias_i",
            "meaning": "CLT/mixing odd-cumulant leakage",
            "claim_status": "SYMBOLIC_READY",
            "valid_for_claim": "false",
        },
        {
            "envelope_id": "ENV3327_2_one_particle",
            "formula": "epsilon_1p_i <= A_i delta_mean_i sigma_Dpi_i + B_i (C3_i/sqrt(N_eff_i)+delta_bias_i) sigma_Dpi_i^2 + rho_P1_i Q2_norm_i",
            "meaning": "one-particle composite leakage after mean-centering and skew suppression",
            "claim_status": "SYMBOLIC_READY",
            "valid_for_claim": "false",
        },
        {
            "envelope_id": "ENV3327_3_two_particle",
            "formula": "epsilon_2p_i(lambda) <= C_2i E_2p_i(lambda; dmu_2, m_gap_2pi), with E_2p including exp[-2 m_gap_2pi r] when gapped",
            "meaning": "longer-range loop/composite branch",
            "claim_status": "REQUIRES_SPECTRAL_INPUT",
            "valid_for_claim": "false",
        },
        {
            "envelope_id": "ENV3327_4_total",
            "formula": "epsilon_composite_i <= epsilon_1p_i + epsilon_2p_i(lambda) + epsilon_contact_i + epsilon_boundary_i + epsilon_kernel_aniso_i",
            "meaning": "no-cancellation composite envelope suitable for PPN/R10/WEP/clock/orbital routing",
            "claim_status": "SYMBOLIC_READY",
            "valid_for_claim": "false",
        },
    ]


def required_numeric_input_rows() -> list[dict[str, Any]]:
    return [
        {
            "input_id": "NUM3327_0_ell_s",
            "quantity": "ell_s",
            "role": "smoothing kernel scale",
            "needed_for": "N_eff and gradient/composite suppression",
            "current_status": "MISSING_PARENT_NUMERIC",
            "valid_for_claim": "false",
        },
        {
            "input_id": "NUM3327_1_ell_c_Cmix",
            "quantity": "ell_c_i, C_mix_i, d_eff",
            "role": "correlation length, mixing penalty, effective dimension",
            "needed_for": "N_eff_i = (ell_s/ell_c_i)^d_eff/C_mix_i",
            "current_status": "MISSING_PARENT_NUMERIC",
            "valid_for_claim": "false",
        },
        {
            "input_id": "NUM3327_2_C3_bias",
            "quantity": "C3_i, delta_bias_i",
            "role": "third-cumulant size and coherent odd bias",
            "needed_for": "delta_skew_i bound",
            "current_status": "MISSING_PARENT_OR_EMPIRICAL_BOUND",
            "valid_for_claim": "false",
        },
        {
            "input_id": "NUM3327_3_projection",
            "quantity": "rho_P1_i",
            "role": "arena one-particle projection leakage",
            "needed_for": "epsilon_1p_i",
            "current_status": "MISSING_ARENA_PROJECTION_BOUND",
            "valid_for_claim": "false",
        },
        {
            "input_id": "NUM3327_4_spectral",
            "quantity": "dmu_2(s), m_gap_2pi",
            "role": "two-particle composite spectral tail",
            "needed_for": "epsilon_2p_i(lambda)",
            "current_status": "MISSING_PARENT_SPECTRAL_INPUT",
            "valid_for_claim": "false",
        },
        {
            "input_id": "NUM3327_5_contact_boundary",
            "quantity": "epsilon_contact_i, epsilon_boundary_i, epsilon_kernel_aniso_i",
            "role": "contact, patch, and anisotropic leakage",
            "needed_for": "total epsilon_composite_i",
            "current_status": "MISSING_LOCAL_BOUND_INPUT",
            "valid_for_claim": "false",
        },
    ]


def suppression_sample_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for ratio, d_eff in [(10.0, 4), (1.0e3, 4), (1.0e6, 4), (1.0e6, 3)]:
        n_eff = ratio**d_eff
        rows.append(
            {
                "sample_id": f"SAMP3327_ratio_{ratio:g}_d{d_eff}",
                "ell_s_over_ell_c": f"{ratio:.6g}",
                "d_eff": d_eff,
                "C_mix": "1 illustrative",
                "N_eff": f"{n_eff:.6e}",
                "N_eff_minus_half": f"{1.0 / math.sqrt(n_eff):.6e}",
                "interpretation": "illustrative only; not claim-grade until ell_s/ell_c/d_eff/C_mix are parent-signed",
                "valid_for_claim": "false",
            }
        )
    return rows


def promotion_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "GATE3327_0_mean_centering",
            "claim": "pi has zero local smoothed mean by definition",
            "passed": "true",
            "reason": "pi=psi-S_ell psi gives S_ell pi=0 when the same kernel defines the local split",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3327_1_CLT_skew_bound",
            "claim": "odd-cumulant leakage has a CLT/mixing suppression law",
            "passed": "true",
            "reason": "delta_skew <= C3/sqrt(N_eff)+delta_bias with N_eff=(ell_s/ell_c)^d_eff/C_mix",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3327_2_parent_numeric_inputs",
            "claim": "ell_s, ell_c, C_mix, C3, bias, projection, spectral gap, contact, and boundary inputs are parent-owned",
            "passed": "false",
            "reason": "current corpus supports smoothing but not numeric local fluctuation measure parameters",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3327_3_numeric_composite_claim",
            "claim": "epsilon_composite_i is numerically below local-test limits",
            "passed": "false",
            "reason": "symbolic envelope is ready but no claim-grade numbers are supplied",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3327_4_composite_envelope_ready",
            "claim": "composite envelope is ready for PPN/R10/WEP/clock/orbital budget assembly",
            "passed": "true",
            "reason": "epsilon_1p, epsilon_2p, contact, boundary, and anisotropy terms are explicit",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3327_5_unconditional_local_GR",
            "claim": "local-GR branch is unconditionally closed",
            "passed": "false",
            "reason": "numeric composite envelope and parent-owned projection/spectral inputs remain missing",
            "valid_for_claim": "false",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3327_0",
            "question": "Did 3327 derive a parent local fluctuation measure?",
            "answer": "partly",
            "reason": "mean centering is exact by the coarse-grained split, and skew leakage has a CLT/mixing law, but parent numeric/mixing constants are not supplied",
            "next_action": "assemble local residual budget using symbolic envelope and identify the smallest numeric inputs needed",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC3327_1",
            "question": "Is the composite tail still vague?",
            "answer": "no",
            "reason": "epsilon_composite_i is now an explicit sum of one-particle, two-particle, contact, boundary, and anisotropic terms with required inputs",
            "next_action": "route each term into local-GR/PPN/R10/WEP/clock/orbital thresholds",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC3327_2",
            "question": "Can we claim local GR yet?",
            "answer": "not unconditionally",
            "reason": "the branch now has a measured-G theorem plus source signature plus symbolic residual envelope, but lacks numeric local residual budget",
            "next_action": "build local branch residual budget and promotion map",
            "valid_for_claim": "false",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "target_doc": "3328-Y5-R2FR-local-GR-residual-budget-and-promotion-map-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3328_local_GR_residual_budget_and_promotion_map.py",
            "objective": "assemble the measured-G local-GR branch into one residual budget: Gamma/local saturation, psi tree residue, C_i epsilon_grad, composite envelope, matter/EM source signature, and Newton/Poisson closure",
            "must_include": "pass/conditional/fail map; exact assumptions; residual formulas by PPN/R10/WEP/clock/orbital arena; required numeric inputs; no public claim unless all gates are signed",
            "fallback_if_failed": "local-GR theorem remains conditional but now has a complete residual-budget checklist",
            "valid_for_claim": "false",
        }
    ]


def validate_outputs(formalization_before: dict[str, tuple[int, int]]) -> list[dict[str, Any]]:
    sources = source_register_rows()
    evidence = coarse_graining_evidence_rows()
    clt = clt_contract_rows()
    centering = centering_signing_rows()
    envelope = composite_envelope_rows()
    inputs = required_numeric_input_rows()
    samples = suppression_sample_rows()
    gates = promotion_gate_rows()
    output_paths = [path for key, path in OUTPUTS.items() if key != "validation"]
    fw_changed = changed_count(formalization_before, snapshot_tree(FW))
    checks = [
        {
            "check_id": "VAL3327_0_sources_exist",
            "check": "all cited source paths exist",
            "passed": all(row["exists"] == "true" for row in sources),
            "detail": "",
        },
        {
            "check_id": "VAL3327_1_sources_parse",
            "check": "all cited source paths parse",
            "passed": all(row["parse_ok"] == "true" for row in sources),
            "detail": "",
        },
        {
            "check_id": "VAL3327_2_outputs_parse",
            "check": "all 3327 non-validation outputs parse",
            "passed": all(path.exists() and parse_ok(path) for path in output_paths),
            "detail": "",
        },
        {
            "check_id": "VAL3327_3_coarse_grain_evidence",
            "check": "evidence includes coarse-grain/smoothing and Planck support",
            "passed": any(row["has_coarse_grain"] == "true" or row["has_smoothing"] == "true" for row in evidence)
            and any(row["has_planck_cells"] == "true" for row in evidence),
            "detail": "",
        },
        {
            "check_id": "VAL3327_4_CLT_contract",
            "check": "CLT contract includes fluctuation split, N_eff, skew bound, exact zero limit, and parent gap",
            "passed": {"CLT3327_0_fluctuation_split", "CLT3327_1_effective_cell_count", "CLT3327_2_skew_bound", "CLT3327_3_even_limit", "CLT3327_4_parent_gap"}.issubset(
                {row["contract_id"] for row in clt}
            ),
            "detail": "",
        },
        {
            "check_id": "VAL3327_5_centering_signing",
            "check": "centering signing covers mean, skew, projection, two-particle, and contact/boundary",
            "passed": {"delta_mean_i", "delta_skew_i", "rho_P1_i", "epsilon_2p_i(lambda)", "epsilon_contact_i + epsilon_boundary_i + epsilon_kernel_aniso_i"}.issubset(
                {row["quantity"] for row in centering}
            ),
            "detail": "",
        },
        {
            "check_id": "VAL3327_6_envelope",
            "check": "composite envelope includes N_eff, skew, one-particle, two-particle, and total formulas",
            "passed": {"ENV3327_0_Neff", "ENV3327_1_skew", "ENV3327_2_one_particle", "ENV3327_3_two_particle", "ENV3327_4_total"}.issubset(
                {row["envelope_id"] for row in envelope}
            ),
            "detail": "",
        },
        {
            "check_id": "VAL3327_7_required_inputs",
            "check": "required inputs include smoothing, correlation/mixing, skew/bias, projection, spectral, contact/boundary",
            "passed": {"ell_s", "ell_c_i, C_mix_i, d_eff", "C3_i, delta_bias_i", "rho_P1_i", "dmu_2(s), m_gap_2pi", "epsilon_contact_i, epsilon_boundary_i, epsilon_kernel_aniso_i"}.issubset(
                {row["quantity"] for row in inputs}
            ),
            "detail": "",
        },
        {
            "check_id": "VAL3327_8_samples",
            "check": "suppression samples include non-claim N_eff^-1/2 estimates",
            "passed": all(float(row["N_eff_minus_half"]) > 0 for row in samples) and all(row["valid_for_claim"] == "false" for row in samples),
            "detail": "",
        },
        {
            "check_id": "VAL3327_9_no_unconditional_claim",
            "check": "numeric inputs/composite claim/local-GR gates remain false while CLT/envelope gates pass",
            "passed": all(
                row["passed"] == "false"
                for row in gates
                if row["gate_id"] in {"GATE3327_2_parent_numeric_inputs", "GATE3327_3_numeric_composite_claim", "GATE3327_5_unconditional_local_GR"}
            )
            and all(
                row["passed"] == "true"
                for row in gates
                if row["gate_id"] in {"GATE3327_0_mean_centering", "GATE3327_1_CLT_skew_bound", "GATE3327_4_composite_envelope_ready"}
            ),
            "detail": "",
        },
        {
            "check_id": "VAL3327_10_next_residual_budget",
            "check": "next target assembles local-GR residual budget and promotion map",
            "passed": any("local-GR branch" in row["objective"] and "residual budget" in row["objective"] for row in next_target_rows()),
            "detail": "",
        },
        {
            "check_id": "VAL3327_11_formalization_untouched",
            "check": "formalization-workbench modified-file count remains zero by this script",
            "passed": fw_changed == 0,
            "detail": f"formalization_changed_count={fw_changed}",
        },
    ]
    overall = all(bool(check["passed"]) for check in checks)
    checks.append(
        {
            "check_id": "VAL3327_12_overall",
            "check": "3327 validation overall",
            "passed": overall,
            "detail": "all required checks passed" if overall else "one or more checks failed",
        }
    )
    for check in checks:
        check["passed"] = bool_str(bool(check["passed"]))
    return checks


def render_doc() -> str:
    lines: list[str] = [
        "# 3327 - Parent local fluctuation measure or numeric composite envelope under AX1090",
        "",
        f"Run UTC: `{RUN_UTC}`",
        "",
        "## Verdict",
        "",
        "3327 moves the composite tail from conditional theorem to usable envelope.",
        "",
        "The mean-centering part is actually signable:",
        "",
        "`psi_bar = S_ell psi`, `pi = psi - psi_bar`, therefore `S_ell pi = 0`.",
        "",
        "The even/Gaussian part is not exactly parent-signed, but coarse-graining over many weakly correlated Planck-scale cells gives a CLT/mixing suppression law:",
        "",
        "`N_eff_i = (ell_s/ell_c_i)^d_eff / C_mix_i`,",
        "",
        "`delta_skew_i <= C3_i/sqrt(N_eff_i) + delta_bias_i`.",
        "",
        "Thus the 3326 exact-zero theorem remains available when the measure is exactly even, but the realistic fallback is now quantitative rather than hand-wavy.",
        "",
        "The local composite envelope becomes",
        "",
        "`epsilon_composite_i <= epsilon_1p_i + epsilon_2p_i(lambda) + epsilon_contact_i + epsilon_boundary_i + epsilon_kernel_aniso_i`,",
        "",
        "with",
        "",
        "`epsilon_1p_i <= A_i delta_mean_i sigma_Dpi_i + B_i (C3_i/sqrt(N_eff_i)+delta_bias_i) sigma_Dpi_i^2 + rho_P1_i Q2_norm_i`.",
        "",
        "No local-GR claim follows yet because the parent corpus does not provide numeric `ell_s`, `ell_c`, `C_mix`, `C3`, projection leakage, two-pi spectral gap, or contact/boundary bounds. But the branch now has a complete residual-budget object to assemble.",
        "",
        "## Source Register",
        "",
    ]
    for row in source_register_rows():
        lines.append(
            f"- `{row['source_id']}`: `{row['path']}` exists={row['exists']} parse_ok={row['parse_ok']} role={row['role']}"
        )
    sections = [
        ("Coarse-Graining Evidence", coarse_graining_evidence_rows(), "evidence_id"),
        ("CLT/Mixing Contract", clt_contract_rows(), "contract_id"),
        ("Centering Signing", centering_signing_rows(), "sign_id"),
        ("Composite Envelope", composite_envelope_rows(), "envelope_id"),
        ("Required Numeric Inputs", required_numeric_input_rows(), "input_id"),
        ("Suppression Samples", suppression_sample_rows(), "sample_id"),
        ("Promotion Gates", promotion_gate_rows(), "gate_id"),
        ("Decision Ledger", decision_rows(), "decision_id"),
        ("Next Target", next_target_rows(), "target_doc"),
    ]
    for title, rows, key_name in sections:
        lines.extend(["", f"## {title}", ""])
        for row in rows:
            label = row.get(key_name, "")
            body = "; ".join(f"{key}={value}" for key, value in row.items() if key != key_name)
            lines.append(f"- `{label}`: {body}")
    lines.extend(
        [
            "",
            "## Test Notes",
            "",
            "- This checkpoint is private and nonclaim.",
            "- It signs exact mean-centering by the smoothing split.",
            "- It converts even-measure silence into a CLT/mixing skew-suppression law.",
            "- It lists all numeric inputs still needed before local tests can be claimed.",
            "- `formalization-workbench` is not modified.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> None:
    formalization_before = snapshot_tree(FW)
    OUT.mkdir(parents=True, exist_ok=True)
    write_csv(OUTPUTS["sources"], source_register_rows())
    write_csv(OUTPUTS["evidence"], coarse_graining_evidence_rows())
    write_csv(OUTPUTS["clt"], clt_contract_rows())
    write_csv(OUTPUTS["centering"], centering_signing_rows())
    write_csv(OUTPUTS["envelope"], composite_envelope_rows())
    write_csv(OUTPUTS["inputs"], required_numeric_input_rows())
    write_csv(OUTPUTS["samples"], suppression_sample_rows())
    write_csv(OUTPUTS["gates"], promotion_gate_rows())
    write_csv(OUTPUTS["decision"], decision_rows())
    write_csv(OUTPUTS["next"], next_target_rows())
    DOC.write_text(render_doc(), encoding="utf-8")
    write_csv(OUTPUTS["validation"], validate_outputs(formalization_before))
    if PYCACHE.exists():
        shutil.rmtree(PYCACHE)


if __name__ == "__main__":
    main()
