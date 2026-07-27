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

DOC = ROOT / "3321-Y5-R2FR-smoothing-kernel-scale-separation-bound-for-epsilon-grad-under-AX1090.md"

SRC_GRAVITY = REPO / "core-mts-framework" / "gravity" / "motion-timespace-mts-gravity.md"
SRC_COMPACT = REPO / "core-mts-framework" / "gravity" / "gravity-as-emergent-mass-geometry-scaling-in-motion-timespace.md"
SRC_ACTION = REPO / "core-mts-framework" / "action-principle" / "the-fundamental-action-of-motion-timespace-field-theory.md"

SOURCES = [
    {
        "source_id": "SRC3321_0_3320_doc",
        "path": ROOT / "3320-Y5-R2FR-local-first-gradient-silence-or-gradient-envelope-under-AX1090.md",
        "role": "3320 epsilon_grad theorem/envelope handoff",
    },
    {
        "source_id": "SRC3321_1_3320_envelope",
        "path": OUT / "P8_Y5_R2FR_3320_EPSILON_GRAD_ENVELOPE.csv",
        "role": "epsilon_grad definition and bound law",
    },
    {
        "source_id": "SRC3321_2_3320_routing",
        "path": OUT / "P8_Y5_R2FR_3320_TEST_ROUTING.csv",
        "role": "WEP/R10/PPN/clock routing for epsilon_grad",
    },
    {
        "source_id": "SRC3321_3_gravity_ppn",
        "path": SRC_GRAVITY,
        "role": "solar weak-field K_solar proxy and PPN margin language",
    },
    {
        "source_id": "SRC3321_4_compact_newton",
        "path": SRC_COMPACT,
        "role": "compact-system Newtonian/local-system recovery language",
    },
    {
        "source_id": "SRC3321_5_action_covariance",
        "path": SRC_ACTION,
        "role": "smoothed psi-gradient covariance map and slow-variation GR statement",
    },
]

OUTPUTS = {
    "sources": OUT / "P8_Y5_R2FR_3321_SOURCE_REGISTER.csv",
    "evidence": OUT / "P8_Y5_R2FR_3321_SCALE_EVIDENCE.csv",
    "kernel": OUT / "P8_Y5_R2FR_3321_KERNEL_TRANSFER_LAW.csv",
    "proxy": OUT / "P8_Y5_R2FR_3321_SOLAR_PROXY_BOUND.csv",
    "threshold": OUT / "P8_Y5_R2FR_3321_EPSILON_GRAD_THRESHOLD_ROWS.csv",
    "routing": OUT / "P8_Y5_R2FR_3321_UPDATED_TEST_ROUTING.csv",
    "gates": OUT / "P8_Y5_R2FR_3321_PROMOTION_GATES.csv",
    "decision": OUT / "P8_Y5_R2FR_3321_DECISION_LEDGER.csv",
    "next": OUT / "P8_Y5_R2FR_3321_NEXT_TARGET.csv",
    "validation": OUT / "P8_Y5_BRR545_3321_VALIDATION.csv",
}

RUN_UTC = datetime.now(timezone.utc).isoformat()
K_SOLAR_PROXY = 1.0e-61
M_MIN_PROXY = 2.0
S_SOLAR_PROXY = K_SOLAR_PROXY**M_MIN_PROXY

PATTERNS = [
    "K_solar",
    "10",
    "PPN",
    "Cassini",
    "compact systems",
    "Newtonian",
    "Solar System",
    "varies slowly",
    "smoothed covariance",
]


def bool_str(value: bool) -> str:
    return "true" if value else "false"


def compact(value: Any, limit: int = 1100) -> str:
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


def text_for(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def find_hits(path: Path, max_hits: int = 10) -> str:
    text = text_for(path)
    patterns = [pattern.lower() for pattern in PATTERNS]
    hits: list[str] = []
    for index, line in enumerate(text.splitlines(), start=1):
        if any(pattern in line.lower() for pattern in patterns):
            hits.append(f"L{index}:{line.strip()}")
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


def evidence_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source in SOURCES:
        path = source["path"]
        text = text_for(path)
        rows.append(
            {
                "evidence_id": f"EVID3321_{len(rows)}",
                "source_id": source["source_id"],
                "path": str(path),
                "has_k_solar_proxy": bool_str("K_solar" in text or "K_solar" in find_hits(path)),
                "has_compact_newtonian": bool_str("compact systems" in text or "Newtonian gravity exactly" in text or "Solar System" in text),
                "has_slow_variation_covariance": bool_str("varies slowly" in text or "smoothed covariance" in text),
                "hits": find_hits(path),
                "valid_for_claim": "false",
            }
        )
    return rows


def gaussian_transfer(lambda_over_ell: float) -> float:
    if lambda_over_ell <= 0:
        return 0.0
    ell_over_lambda = 1.0 / lambda_over_ell
    return ell_over_lambda * math.exp(-0.5 * ell_over_lambda * ell_over_lambda)


def kernel_rows() -> list[dict[str, Any]]:
    samples = [
        ("shorter_than_smoothing", 0.1),
        ("equal_to_smoothing", 1.0),
        ("ten_times_smoothing", 10.0),
        ("million_times_smoothing", 1.0e6),
    ]
    rows = [
        {
            "law_id": "KER3321_0_gaussian_kernel",
            "quantity": "S_ell",
            "definition": "Gaussian smoothing kernel with width ell_s and Fourier transfer exp[-(k ell_s)^2/2]",
            "formula": "S_ell(k)=exp[-(k ell_s)^2/2]",
            "status": "MODEL_EXPLICIT_NONCLAIM",
            "valid_for_claim": "false",
        },
        {
            "law_id": "KER3321_1_gradient_transfer",
            "quantity": "T_grad(lambda)",
            "definition": "first-gradient leakage transfer for a finite mode of range lambda under k≈1/lambda",
            "formula": "T_grad(lambda)=(ell_s/lambda) exp[-ell_s^2/(2 lambda^2)]",
            "status": "DERIVED_FROM_GAUSSIAN_AND_ONE_DERIVATIVE",
            "valid_for_claim": "false",
        },
        {
            "law_id": "KER3321_2_bound",
            "quantity": "epsilon_grad(lambda)",
            "definition": "dimensionless first-gradient readout leak",
            "formula": "epsilon_grad(lambda) <= epsilon_bg T_grad(lambda) + epsilon_boundary + epsilon_kernel_aniso",
            "status": "BOUND_LAW_DERIVED",
            "valid_for_claim": "false",
        },
    ]
    for name, lambda_over_ell in samples:
        rows.append(
            {
                "law_id": f"KER3321_SAMPLE_{name}",
                "quantity": "T_grad_sample",
                "definition": f"sample transfer for lambda/ell_s={lambda_over_ell:g}",
                "formula": f"T_grad={gaussian_transfer(lambda_over_ell):.12e}",
                "status": "NUMERIC_MODEL_SAMPLE",
                "valid_for_claim": "false",
            }
        )
    return rows


def proxy_rows() -> list[dict[str, Any]]:
    return [
        {
            "proxy_id": "SPB3321_0_source_proxy",
            "system": "solar_weak_field",
            "input_proxy": "K_solar≈1e-61 Planck units; m>=2",
            "derived_proxy": f"S_solar=K_solar^m <= {S_SOLAR_PROXY:.3e}",
            "interpretation": "if the same scalar curvature-saturation response controls first-gradient public leakage, then epsilon_grad^2 is at most of this order before kernel/boundary/composite corrections",
            "claim_status": "SUPPORTING_PROXY_NOT_PARENT_SIGNED",
            "valid_for_claim": "false",
        },
        {
            "proxy_id": "SPB3321_1_Bi_proxy",
            "system": "solar_weak_field",
            "input_proxy": "C_i<=1, T_grad<=1, epsilon_boundary=epsilon_kernel_aniso=epsilon_composite=0 as an optimistic ceiling",
            "derived_proxy": f"|B_i^psi| <= {S_SOLAR_PROXY:.3e}",
            "interpretation": "this would be absurdly safe for local tests, but it is not claim-grade until K_solar^m is parent-linked to epsilon_grad and tails are bounded",
            "claim_status": "OPTIMISTIC_INTERNAL_SCALE_CHECK",
            "valid_for_claim": "false",
        },
        {
            "proxy_id": "SPB3321_2_lab_gap",
            "system": "lab_R10_WEP",
            "input_proxy": "MISSING_LAB_GRADIENT_PROXY",
            "derived_proxy": "epsilon_grad_lab not computed",
            "interpretation": "lab tests need either inherited solar/system gradient bound, local shielding/averaging theorem, or direct scale-separation estimate",
            "claim_status": "MISSING_INPUT",
            "valid_for_claim": "false",
        },
        {
            "proxy_id": "SPB3321_3_cosmo_leak",
            "system": "cosmological_or_galactic_background",
            "input_proxy": "MISSING_BACKGROUND_GRADIENT_SCALE",
            "derived_proxy": "epsilon_grad_cosmo not computed",
            "interpretation": "large-scale memory gradients can revive small finite residues unless smoothing/scale separation suppresses them",
            "claim_status": "MISSING_INPUT",
            "valid_for_claim": "false",
        },
    ]


def threshold_rows() -> list[dict[str, Any]]:
    return [
        {
            "threshold_id": "THR3321_0_general",
            "arena": "generic",
            "bound_input": "B_i^max",
            "threshold_law": "epsilon_grad <= sqrt(max(B_i^max-epsilon_composite,0)/C_i)/T_grad(lambda)",
            "current_status": "FORMULA_READY_BOUND_VALUES_ARENA_DEPENDENT",
            "valid_for_claim": "false",
        },
        {
            "threshold_id": "THR3321_1_PPN",
            "arena": "PPN/local_GR",
            "bound_input": "gamma,beta,preferred-frame limits through response matrix C_PPN",
            "threshold_law": "epsilon_grad <= sqrt(delta_PPN_max/C_PPN)",
            "current_status": "MISSING_C_PPN_RESPONSE_MATRIX",
            "valid_for_claim": "false",
        },
        {
            "threshold_id": "THR3321_2_R10",
            "arena": "R10_short_range",
            "bound_input": "alpha_bound(lambda)",
            "threshold_law": "epsilon_grad(lambda) <= sqrt(alpha_bound(lambda)/C_R10(lambda))",
            "current_status": "MISSING_C_R10_KERNEL_AND_CLAIM_READY_BOUND_CURVE",
            "valid_for_claim": "false",
        },
        {
            "threshold_id": "THR3321_3_WEP",
            "arena": "WEP",
            "bound_input": "eta_AB",
            "threshold_law": "epsilon_grad <= sqrt(eta_AB/(C_WEP |Delta_epsilon_AB|))",
            "current_status": "MISSING_C_WEP_AND_RESIDUAL_MATERIAL_TAILS",
            "valid_for_claim": "false",
        },
    ]


def routing_rows() -> list[dict[str, Any]]:
    return [
        {
            "arena": "local_GR",
            "post_3321_route": "try parent epsilon_grad=0 first; otherwise use scale bound epsilon_grad(lambda)<=epsilon_bg T_grad+tails",
            "what_is_now_better": "finite psi residue is controlled by a kernel/gradient scale, not a free coupling",
            "remaining_gap": "epsilon_bg, ell_s, and C_i projection are not parent-fixed",
            "valid_for_claim": "false",
        },
        {
            "arena": "solar_PPN",
            "post_3321_route": "solar proxy gives S_solar<=1e-122 if K_solar^m maps to epsilon_grad^2",
            "what_is_now_better": "internal scale check suggests huge local margin",
            "remaining_gap": "proxy-to-psi-gradient theorem and PPN response matrix",
            "valid_for_claim": "false",
        },
        {
            "arena": "R10_WEP_lab",
            "post_3321_route": "lab epsilon_grad needs inherited local bound or direct kernel/gradient estimate",
            "what_is_now_better": "we know the missing lab input exactly",
            "remaining_gap": "lab gradient proxy and C_R10/C_WEP kernels",
            "valid_for_claim": "false",
        },
        {
            "arena": "cosmology_galaxy",
            "post_3321_route": "large-scale gradients can remain as empirical/cosmological sector without contaminating local branch if smoothing suppresses short-range readout",
            "what_is_now_better": "separates local first-gradient leakage from intended cosmic/galaxy memory behavior",
            "remaining_gap": "background gradient scale and smoothing support",
            "valid_for_claim": "false",
        },
    ]


def gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "GATE3321_0_kernel_bound",
            "claim": "Gaussian smoothing transfer and epsilon_grad scale bound are derived",
            "passed": "true",
            "reason": "T_grad(lambda) and epsilon_grad(lambda) bound are explicit",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3321_1_solar_proxy",
            "claim": "solar weak-field proxy scale is staged",
            "passed": "true",
            "reason": "K_solar≈1e-61, m>=2 gives internal S_solar<=1e-122 proxy",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3321_2_parent_proxy_link",
            "claim": "K_solar^m is parent-derived as epsilon_grad^2",
            "passed": "false",
            "reason": "the proxy is not yet linked to the psi first-gradient readout norm",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3321_3_full_local_GR",
            "claim": "local GR/Newtonian limit is fully derived",
            "passed": "false",
            "reason": "still needs parent proxy link, C_i projection, composite/contact split, and EH/Newton normalization",
            "valid_for_claim": "false",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3321_0",
            "question": "Did 3321 make epsilon_grad more concrete?",
            "answer": "yes: it gives a Gaussian transfer law and a solar proxy scale check",
            "reason": "epsilon_grad(lambda) is now bounded by epsilon_bg T_grad(lambda) plus named tails, and the corpus solar proxy suggests an internal 1e-122 response scale if linked",
            "next_action": "derive the proxy-to-psi-gradient link or compute C_i/threshold rows",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC3321_1",
            "question": "Can we claim local GR from the solar proxy?",
            "answer": "no",
            "reason": "K_solar^m is not yet proven to equal epsilon_grad^2, and lab/R10 kernels are not sourced",
            "next_action": "treat proxy as encouraging internal scale evidence only",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC3321_2",
            "question": "Best next target?",
            "answer": "derive the response coefficient C_i and composite/contact split, then compare epsilon_grad thresholds",
            "reason": "even a tiny epsilon_grad needs C_i and epsilon_composite before it can be scored",
            "next_action": "build C_i/composite-tail gate before public local-GR claim",
            "valid_for_claim": "false",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "target_doc": "3322-Y5-R2FR-Ci-projection-and-composite-contact-tail-gate-for-epsilon-grad-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3322_Ci_projection_and_composite_contact_tail_gate_for_epsilon_grad.py",
            "objective": "derive or bound C_i(lambda,S,H_pi) and epsilon_composite so the 3321 epsilon_grad scale law can be compared to WEP/R10/PPN/clock limits without hiding tails",
            "must_include": "public propagator projection; Gaussian kernel response coefficient; composite pi-pi contact/long-range split; no-cancellation envelope; arena threshold formulas",
            "fallback_if_failed": "retain C_i and epsilon_composite as explicit nuisance envelopes before empirical scoring",
            "valid_for_claim": "false",
        }
    ]


def validate_outputs(formalization_before: dict[str, tuple[int, int]]) -> list[dict[str, Any]]:
    sources = source_register_rows()
    evidence = evidence_rows()
    kernel = kernel_rows()
    proxy = proxy_rows()
    thresholds = threshold_rows()
    gates = gate_rows()
    output_paths = [path for key, path in OUTPUTS.items() if key != "validation"]
    fw_changed = changed_count(formalization_before, snapshot_tree(FW))
    checks = [
        {
            "check_id": "VAL3321_0_sources_exist",
            "check": "all cited source paths exist",
            "passed": all(row["exists"] == "true" for row in sources),
            "detail": "",
        },
        {
            "check_id": "VAL3321_1_sources_parse",
            "check": "all cited source paths parse",
            "passed": all(row["parse_ok"] == "true" for row in sources),
            "detail": "",
        },
        {
            "check_id": "VAL3321_2_outputs_parse",
            "check": "all 3321 non-validation outputs parse",
            "passed": all(path.exists() and parse_ok(path) for path in output_paths),
            "detail": "",
        },
        {
            "check_id": "VAL3321_3_evidence_Ksolar",
            "check": "evidence includes K_solar or compact Newtonian support",
            "passed": any(row["has_k_solar_proxy"] == "true" or row["has_compact_newtonian"] == "true" for row in evidence),
            "detail": "",
        },
        {
            "check_id": "VAL3321_4_kernel_transfer",
            "check": "Gaussian gradient transfer law is present",
            "passed": any("T_grad(lambda)" in row["quantity"] or "T_grad(lambda)" in row["formula"] for row in kernel),
            "detail": "",
        },
        {
            "check_id": "VAL3321_5_solar_proxy_1e122",
            "check": "solar proxy includes 1e-122 scale",
            "passed": any("1.000e-122" in row["derived_proxy"] or "1e-122" in row["interpretation"] for row in proxy),
            "detail": "",
        },
        {
            "check_id": "VAL3321_6_thresholds_ready",
            "check": "threshold rows include PPN, R10, and WEP",
            "passed": {"PPN/local_GR", "R10_short_range", "WEP"}.issubset({row["arena"] for row in thresholds}),
            "detail": "",
        },
        {
            "check_id": "VAL3321_7_no_full_claim",
            "check": "parent proxy link and full local-GR gates remain false",
            "passed": all(row["passed"] == "false" for row in gates if row["gate_id"] in {"GATE3321_2_parent_proxy_link", "GATE3321_3_full_local_GR"}),
            "detail": "",
        },
        {
            "check_id": "VAL3321_8_next_Ci",
            "check": "next target is C_i projection/composite-tail gate",
            "passed": any("Ci-projection" in row["target_doc"] or "C_i" in row["objective"] for row in next_target_rows()),
            "detail": "",
        },
        {
            "check_id": "VAL3321_9_formalization_untouched",
            "check": "formalization-workbench modified-file count remains zero by this script",
            "passed": fw_changed == 0,
            "detail": f"formalization_changed_count={fw_changed}",
        },
    ]
    overall = all(bool(row["passed"]) for row in checks)
    checks.append(
        {
            "check_id": "VAL3321_10_overall",
            "check": "3321 validation overall",
            "passed": overall,
            "detail": "all required checks passed" if overall else "one or more checks failed",
        }
    )
    for row in checks:
        row["passed"] = bool_str(bool(row["passed"]))
    return checks


def render_doc() -> str:
    sources = source_register_rows()
    evidence = evidence_rows()
    kernel = kernel_rows()
    proxy = proxy_rows()
    thresholds = threshold_rows()
    routing = routing_rows()
    gates = gate_rows()
    decisions = decision_rows()
    next_rows = next_target_rows()
    lines: list[str] = [
        "# 3321 - Smoothing kernel scale-separation bound for epsilon_grad under AX1090",
        "",
        f"Run UTC: `{RUN_UTC}`",
        "",
        "## Verdict",
        "",
        "3321 makes the `epsilon_grad` route quantitative enough to test, while keeping it nonclaim.",
        "",
        "For a Gaussian smoothing kernel of width `ell_s`, a finite mode of range `lambda` carries a first-gradient leakage transfer",
        "",
        "`T_grad(lambda) = (ell_s/lambda) exp[-ell_s^2/(2 lambda^2)]`.",
        "",
        "So the local tree-level psi residue is bounded by",
        "",
        "`|B_i^psi| <= C_i(lambda,S,H_pi) [epsilon_bg T_grad(lambda) + tails]^2 + epsilon_composite`.",
        "",
        "Using the corpus solar weak-field proxy `K_solar≈1e-61` with `m>=2` gives an internal scale check `K_solar^m <= 1e-122`. That is extremely encouraging, but not claim-grade: the missing theorem is the link `K_solar^m -> epsilon_grad^2`, plus the response coefficient `C_i` and composite/contact tail.",
        "",
        "## Source Register",
        "",
    ]
    for row in sources:
        lines.append(f"- `{row['source_id']}`: `{row['path']}` - exists={row['exists']}; parse_ok={row['parse_ok']}; role={row['role']}")
    lines.extend(["", "## Scale Evidence", ""])
    for row in evidence:
        lines.append(
            f"- `{row['evidence_id']}` `{row['source_id']}`: Ksolar={row['has_k_solar_proxy']}; compactNewton={row['has_compact_newtonian']}; slowCovariance={row['has_slow_variation_covariance']}; hits={row['hits']}"
        )
    lines.extend(["", "## Kernel Transfer Law", ""])
    for row in kernel:
        lines.append(f"- `{row['law_id']}` `{row['quantity']}`: {row['definition']} Formula: `{row['formula']}` Status: {row['status']}.")
    lines.extend(["", "## Solar Proxy Bound", ""])
    for row in proxy:
        lines.append(f"- `{row['proxy_id']}` `{row['system']}`: {row['derived_proxy']} Interpretation: {row['interpretation']} Status: {row['claim_status']}.")
    lines.extend(["", "## Epsilon Grad Threshold Rows", ""])
    for row in thresholds:
        lines.append(f"- `{row['threshold_id']}` `{row['arena']}`: {row['threshold_law']} Status: {row['current_status']}.")
    lines.extend(["", "## Updated Test Routing", ""])
    for row in routing:
        lines.append(f"- `{row['arena']}`: {row['post_3321_route']} Better: {row['what_is_now_better']}. Gap: {row['remaining_gap']}.")
    lines.extend(["", "## Promotion Gates", ""])
    for row in gates:
        lines.append(f"- `{row['gate_id']}`: passed={row['passed']}; claim={row['claim']}; reason={row['reason']}")
    lines.extend(["", "## Decision", ""])
    for row in decisions:
        lines.append(f"- `{row['decision_id']}`: {row['answer']} - {row['reason']} Next: {row['next_action']}.")
    lines.extend(["", "## Next Target", ""])
    for row in next_rows:
        lines.append(f"- `{row['target_doc']}`")
        lines.append(f"- `{row['target_script']}`")
        lines.append(f"- Objective: {row['objective']}")
        lines.append(f"- Fallback: {row['fallback_if_failed']}")
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    formalization_before = snapshot_tree(FW)
    OUT.mkdir(parents=True, exist_ok=True)
    write_csv(OUTPUTS["sources"], source_register_rows())
    write_csv(OUTPUTS["evidence"], evidence_rows())
    write_csv(OUTPUTS["kernel"], kernel_rows())
    write_csv(OUTPUTS["proxy"], proxy_rows())
    write_csv(OUTPUTS["threshold"], threshold_rows())
    write_csv(OUTPUTS["routing"], routing_rows())
    write_csv(OUTPUTS["gates"], gate_rows())
    write_csv(OUTPUTS["decision"], decision_rows())
    write_csv(OUTPUTS["next"], next_target_rows())
    DOC.write_text(render_doc(), encoding="utf-8")
    write_csv(OUTPUTS["validation"], validate_outputs(formalization_before))
    if PYCACHE.exists():
        shutil.rmtree(PYCACHE)
    print(f"wrote {DOC}")
    print(f"wrote {OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
