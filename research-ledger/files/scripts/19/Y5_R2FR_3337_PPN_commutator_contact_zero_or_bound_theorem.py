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

DOC = ROOT / "3337-Y5-R2FR-PPN-commutator-contact-zero-or-bound-theorem-under-AX1090.md"

SOURCES = [
    {
        "source_id": "SRC3337_0_3336_doc",
        "path": ROOT / "3336-Y5-R2FR-PPN-dominant-floor-source-acquisition-or-derivation-under-AX1090.md",
        "role": "3336 dominant floor handoff",
    },
    {
        "source_id": "SRC3337_1_3336_composite_contract",
        "path": OUT / "P8_Y5_R2FR_3336_COMPOSITE_CONTACT_COMMUTATOR_CONTRACT.csv",
        "role": "delta_comm/contact ceilings",
    },
    {
        "source_id": "SRC3337_2_3332_composite",
        "path": OUT / "P8_Y5_R2FR_3332_COMPOSITE_PPN_SPECIALIZATION.csv",
        "role": "PPN composite formula",
    },
    {
        "source_id": "SRC3337_3_3327_composite",
        "path": OUT / "P8_Y5_R2FR_3327_COMPOSITE_ENVELOPE.csv",
        "role": "generic composite envelope",
    },
    {
        "source_id": "SRC3337_4_3326_selection",
        "path": OUT / "P8_Y5_R2FR_3326_SELECTION_RULE_THEOREM.csv",
        "role": "centered/even selection rule",
    },
    {
        "source_id": "SRC3337_5_3326_bounds",
        "path": OUT / "P8_Y5_R2FR_3326_COMPOSITE_BOUND_FORMULAS.csv",
        "role": "contact routing and total composite bound",
    },
    {
        "source_id": "SRC3337_6_3331_cmetric",
        "path": OUT / "P8_Y5_R2FR_3331_CMETRIC_BOUND.csv",
        "role": "PPN gauge/projector and smoothing operator factors",
    },
    {
        "source_id": "SRC3337_7_3336_thresholds",
        "path": OUT / "P8_Y5_R2FR_3336_PPN_THRESHOLD_CANDIDATES.csv",
        "role": "Cassini gamma threshold candidate",
    },
]

OUTPUTS = {
    "sources": OUT / "P8_Y5_R2FR_3337_SOURCE_REGISTER.csv",
    "commutator": OUT / "P8_Y5_R2FR_3337_COMMUTATOR_THEOREM.csv",
    "comm_bounds": OUT / "P8_Y5_R2FR_3337_COMMUTATOR_BOUND_SCENARIOS.csv",
    "contact": OUT / "P8_Y5_R2FR_3337_CONTACT_THEOREM.csv",
    "contact_bounds": OUT / "P8_Y5_R2FR_3337_CONTACT_BOUND_SCENARIOS.csv",
    "composite_update": OUT / "P8_Y5_R2FR_3337_COMPOSITE_BUDGET_UPDATE.csv",
    "requirements": OUT / "P8_Y5_R2FR_3337_REQUIRED_INPUTS.csv",
    "gates": OUT / "P8_Y5_R2FR_3337_PROMOTION_GATES.csv",
    "decision": OUT / "P8_Y5_R2FR_3337_DECISION_LEDGER.csv",
    "next": OUT / "P8_Y5_R2FR_3337_NEXT_TARGET.csv",
    "validation": OUT / "P8_Y5_BRR545_3337_VALIDATION.csv",
}

RUN_UTC = datetime.now(timezone.utc).isoformat()
B_GAMMA = 2.3e-5
F_COMP = 0.30
B_COMP = F_COMP * B_GAMMA
SIGMA_DPI_REF = 1.0e-3
DELTA_COMM_ALLOWED = B_COMP / SIGMA_DPI_REF


def bool_str(value: bool) -> str:
    return "true" if value else "false"


def compact(value: Any, limit: int = 1800) -> str:
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


def source_rows() -> list[dict[str, Any]]:
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


def commutator_theorem_rows() -> list[dict[str, Any]]:
    return [
        {
            "theorem_id": "COMM3337_0_exact_zero",
            "statement": "delta_comm_PPN=0 if the PPN projector/readout P_PPN and smoothing S_ell are translation-invariant Fourier multipliers on an interior local patch",
            "derivation": "In Fourier space, P_PPN has symbol P(k) and isotropic Gaussian smoothing has scalar symbol s_ell(k). Their composition has symbol P(k)s_ell(k)=s_ell(k)P(k), so [P_PPN,S_ell]=0.",
            "conditions": "constant-coefficient local PPN gauge/projector; no finite-window edge; isotropic convolution smoothing; source mass/GM mode already projected out",
            "result": "exact commutator zero branch",
            "valid_for_claim": "false",
        },
        {
            "theorem_id": "COMM3337_1_window_bound",
            "statement": "if P_PPN or the source/window varies across the smoothing patch, delta_comm_PPN is first-order in ell_s/L_var plus boundary leakage",
            "derivation": "[P(x),S_ell]f = integral K_ell(x-y)[P(x)-P(y)]f(y)dy, so ||[P,S_ell]|| <= M1(K) ell_s ||grad P|| + boundary tail for a smooth local symbol.",
            "conditions": "P_PPN varies on length L_var; Gaussian kernel has finite first moment M1; patch boundary is distance d_boundary from the support",
            "result": "delta_comm_PPN <= C_comm ell_s/L_var + C_boundary exp[-d_boundary^2/(2 ell_s^2)] + epsilon_gauge_res",
            "valid_for_claim": "false",
        },
        {
            "theorem_id": "COMM3337_2_budget_test",
            "statement": "under the 3336 reference sigma_Dpi=1e-3, the first commutator ceiling is delta_comm_PPN <= 6.9e-3",
            "derivation": "epsilon_1p contains A_1P delta_comm sigma_Dpi; requiring it below f_comp B_gamma gives delta_comm <= f_comp B_gamma/(A_1P sigma_Dpi).",
            "conditions": "A_1P=1; other composite floors initially reserved as zero; B_gamma=2.3e-5; f_comp=0.30",
            "result": f"delta_comm_allowed={DELTA_COMM_ALLOWED:.6e}",
            "valid_for_claim": "false",
        },
    ]


def commutator_bound_rows() -> list[dict[str, Any]]:
    specs = [
        ("CBND3337_0_exact", 0.0, 0.0, 0.0),
        ("CBND3337_1_interior_smooth", 1.0e-6, 1.0, 0.0),
        ("CBND3337_2_mild_window", 1.0e-3, 2.0, 1.0e-8),
        ("CBND3337_3_ceiling_edge", 3.0e-3, 2.0, 9.0e-4),
        ("CBND3337_4_fail_window", 1.0e-2, 2.0, 1.0e-3),
    ]
    rows: list[dict[str, Any]] = []
    for row_id, ell_over_lvar, c_comm, boundary in specs:
        delta_comm = c_comm * ell_over_lvar + boundary
        epsilon_1p_comm = delta_comm * SIGMA_DPI_REF
        rows.append(
            {
                "scenario_id": row_id,
                "ell_s_over_L_var": f"{ell_over_lvar:.6e}",
                "C_comm": f"{c_comm:.6e}",
                "boundary_tail": f"{boundary:.6e}",
                "delta_comm_bound": f"{delta_comm:.6e}",
                "epsilon_1p_comm_ref": f"{epsilon_1p_comm:.6e}",
                "delta_comm_allowed_ref": f"{DELTA_COMM_ALLOWED:.6e}",
                "passes_ref_ceiling": bool_str(delta_comm <= DELTA_COMM_ALLOWED),
                "formula": "delta_comm <= C_comm ell_s/L_var + boundary_tail",
                "valid_for_claim": "false",
            }
        )
    return rows


def contact_theorem_rows() -> list[dict[str, Any]]:
    return [
        {
            "theorem_id": "CONT3337_0_absorbed_contact",
            "statement": "epsilon_contact_PPN=0 for contact pieces that renormalize only measured local constants already fixed in the branch",
            "derivation": "A delta-supported composite contact term contributes a local analytic counterterm. If it has the same tensor structure as the measured-G/Newtonian mass normalization, it is absorbed before residual scoring.",
            "conditions": "universal metric tensor structure; no composition-dependent or nonmetric residue; measured-G/source calibration already declared",
            "result": "conditional contact zero for absorbed universal pieces",
            "valid_for_claim": "false",
        },
        {
            "theorem_id": "CONT3337_1_derivative_contact_scaling",
            "statement": "unabsorbed finite-size contact residues scale as epsilon_contact <= C_contact (ell_c/L_PPN)^p",
            "derivation": "For a short-range correlation/contact kernel, the long-wavelength expansion is analytic in k ell_c. After absorbing the zeroth local term, the first surviving even isotropic correction is O((k ell_c)^2); if the second-derivative term is also absorbed/symmetry-forbidden, p=4.",
            "conditions": "ell_c << L_PPN; isotropic centered kernel; local analytic derivative expansion; no unsuppressed composition-dependent zeroth term",
            "result": "p_contact>=2 generally, p_contact>=4 under second-order absorption/symmetry",
            "valid_for_claim": "false",
        },
        {
            "theorem_id": "CONT3337_2_fail_condition",
            "statement": "if the contact term is composition-dependent, nonmetric, or not absorbed into measured local constants, it remains an explicit floor",
            "derivation": "Such a term would not be part of the universal GR/Newton calibration and can feed PPN/WEP/clock channels directly.",
            "conditions": "nonuniversal contact tensor/source dependence",
            "result": "retain epsilon_contact_PPN as source-bound floor",
            "valid_for_claim": "false",
        },
    ]


def contact_bound_rows() -> list[dict[str, Any]]:
    ratios = [1.0e-6, 1.0e-4, 1.0e-3, 2.626785e-3, 5.125217e-2, 1.0e-1]
    rows: list[dict[str, Any]] = []
    for ratio in ratios:
        for power in (2, 4):
            epsilon_contact = ratio**power
            rows.append(
                {
                    "scenario_id": f"CONTACT3337_p{power}_{ratio:.1e}",
                    "ell_c_over_L_PPN": f"{ratio:.6e}",
                    "p_contact": power,
                    "C_contact": f"{1.0:.6e}",
                    "epsilon_contact_bound": f"{epsilon_contact:.6e}",
                    "B_comp": f"{B_COMP:.6e}",
                    "passes_comp_budget": bool_str(epsilon_contact <= B_COMP),
                    "formula": "epsilon_contact <= C_contact (ell_c/L_PPN)^p_contact",
                    "valid_for_claim": "false",
                }
            )
    return rows


def composite_update_rows() -> list[dict[str, Any]]:
    return [
        {
            "update_id": "CUP3337_0_best_case",
            "formula": "epsilon_composite_PPN <= epsilon_2p + epsilon_boundary + epsilon_kernel_aniso",
            "conditions": "delta_comm=0 by Fourier multiplier theorem; contact absorbed; one-particle odd cumulants vanish or are CLT-suppressed",
            "interpretation": "composite risk moves to spectral two-particle and patch defects",
            "status": "CONDITIONAL_REDUCTION",
            "valid_for_claim": "false",
        },
        {
            "update_id": "CUP3337_1_bounded_case",
            "formula": "epsilon_composite_PPN <= A_1P(C_comm ell_s/L_var + boundary) sigma_Dpi + B_1P(C3/sqrt(N_eff)+delta_bias)sigma_Dpi^2 + rho_P1 Q2_norm + C_contact(ell_c/L)^p + epsilon_2p + patch defects",
            "conditions": "commutator and contact are bounded but not zero",
            "interpretation": "claim route requires each factor to fit under the 3336 composite budget",
            "status": "BOUNDED_COMPOSITE_CONTRACT",
            "valid_for_claim": "false",
        },
        {
            "update_id": "CUP3337_2_fail_case",
            "formula": "epsilon_composite_PPN remains explicit if projector/smoothing commutator or nonuniversal contact term is unbounded",
            "conditions": "finite patch/gauge/source dependence too large or contact not universal/absorbed",
            "interpretation": "local-GR claim remains blocked until sourced",
            "status": "EXPLICIT_FLOOR_RETAINED",
            "valid_for_claim": "false",
        },
    ]


def required_input_rows() -> list[dict[str, Any]]:
    return [
        {
            "input_id": "REQ3337_0_PPN_projector_symbol",
            "quantity": "P_PPN Fourier/gauge projector symbol",
            "needed_for": "exact commutator zero branch",
            "status": "NOT_SOURCE_OWNED",
            "valid_for_claim": "false",
        },
        {
            "input_id": "REQ3337_1_kernel_interior_patch",
            "quantity": "proof smoothing is isotropic convolution on an interior patch",
            "needed_for": "exact commutator zero or boundary tail bound",
            "status": "CONDITIONAL_ONLY",
            "valid_for_claim": "false",
        },
        {
            "input_id": "REQ3337_2_L_var_boundary",
            "quantity": "L_var and boundary distance d_boundary",
            "needed_for": "commutator defect bound",
            "status": "NUMERIC_MISSING",
            "valid_for_claim": "false",
        },
        {
            "input_id": "REQ3337_3_contact_tensor_structure",
            "quantity": "universal versus nonuniversal contact tensor/source structure",
            "needed_for": "contact absorption zero branch",
            "status": "PARENT_SIGNATURE_NEEDED",
            "valid_for_claim": "false",
        },
        {
            "input_id": "REQ3337_4_ellc_power",
            "quantity": "ell_c/L_PPN, C_contact, p_contact",
            "needed_for": "contact scale-separation bound",
            "status": "NUMERIC_MISSING",
            "valid_for_claim": "false",
        },
        {
            "input_id": "REQ3337_5_spectral_tail",
            "quantity": "two-particle spectral gap/measure",
            "needed_for": "remaining composite floor after commutator/contact",
            "status": "MISSING",
            "valid_for_claim": "false",
        },
    ]


def promotion_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "GATE3337_0_commutator_zero_theorem",
            "claim": "delta_comm_PPN=0 under Fourier-multiplier/interior-patch conditions",
            "passed": "true",
            "reason": "P(k) and scalar smoothing symbol commute exactly",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3337_1_commutator_bound",
            "claim": "delta_comm_PPN has a finite patch/window bound",
            "passed": "true",
            "reason": "commutator bounded by C_comm ell_s/L_var plus boundary tail",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3337_2_contact_scaling",
            "claim": "contact floor has absorption and scale-separation routes",
            "passed": "true",
            "reason": "absorbed universal contact is branch-zero; unabsorbed derivative contacts scale as (ell_c/L)^p",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3337_3_composite_claim_ready",
            "claim": "epsilon_composite_PPN is source-bounded below Cassini candidate allocation",
            "passed": "false",
            "reason": "projector symbol, L_var, boundary, contact tensor, ell_c/L, and spectral gap are not numeric/source-owned",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3337_4_local_GR_claim",
            "claim": "PPN/local-GR pass is claim-ready",
            "passed": "false",
            "reason": "3337 proves/bounds structure but does not source all numerical inputs or response product",
            "valid_for_claim": "false",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3337_0",
            "question": "Did 3337 prove the composite floor away?",
            "answer": "not fully",
            "reason": "it proves exact zero only under interior Fourier-multiplier conditions and gives a finite defect bound otherwise",
            "next_action": "source or derive the PPN projector symbol and patch/window scales",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC3337_1",
            "question": "Did 3337 improve the situation?",
            "answer": "yes",
            "reason": "delta_comm and contact are no longer mysterious placeholders; they have exact zero conditions and scale-separation bounds",
            "next_action": "decide whether to pursue projector/gauge source bounding or response-product bounding next",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC3337_2",
            "question": "What is the remaining composite bottleneck?",
            "answer": "source-owned geometry of the PPN patch",
            "reason": "L_var, boundary distance, PPN projector, contact tensor universality, and spectral gap are needed to turn theorem into numbers",
            "next_action": "build a PPN patch geometry/source contract or move to A_PPN*C_metric bounding",
            "valid_for_claim": "false",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "target_doc": "3338-Y5-R2FR-PPN-projector-patch-geometry-source-contract-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3338_PPN_projector_patch_geometry_source_contract.py",
            "objective": "turn the 3337 commutator/contact theorem into sourceable PPN patch geometry inputs: P_PPN symbol, L_var, boundary distance, ell_c/L_PPN, and contact tensor universality",
            "must_include": "Cassini gamma slot convention; PPN gauge/projector definition; interior patch assumptions; numerical acquisition rows; no PPN pass claim",
            "fallback_if_failed": "move to A_PPN*C_metric response-product bounding with composite floor retained",
            "valid_for_claim": "false",
        }
    ]


def validate_outputs(formalization_before: dict[str, tuple[int, int]]) -> list[dict[str, Any]]:
    sources = source_rows()
    comm = commutator_theorem_rows()
    comm_bounds = commutator_bound_rows()
    contact = contact_theorem_rows()
    contact_bounds = contact_bound_rows()
    comp_update = composite_update_rows()
    requirements = required_input_rows()
    gates = promotion_gate_rows()
    output_paths = [path for key, path in OUTPUTS.items() if key != "validation"]
    fw_changed = changed_count(formalization_before, snapshot_tree(FW))
    checks = [
        {
            "check_id": "VAL3337_0_sources_exist",
            "check": "all cited source paths exist",
            "passed": all(row["exists"] == "true" for row in sources),
            "detail": "",
        },
        {
            "check_id": "VAL3337_1_sources_parse",
            "check": "all cited source paths parse",
            "passed": all(row["parse_ok"] == "true" for row in sources),
            "detail": "",
        },
        {
            "check_id": "VAL3337_2_outputs_parse",
            "check": "all 3337 non-validation outputs parse",
            "passed": all(path.exists() and parse_ok(path) for path in output_paths),
            "detail": "",
        },
        {
            "check_id": "VAL3337_3_commutator_zero",
            "check": "commutator theorem includes exact Fourier multiplier zero branch",
            "passed": any("Fourier multipliers" in row["statement"] and "[P_PPN,S_ell]=0" in row["derivation"] for row in comm),
            "detail": "",
        },
        {
            "check_id": "VAL3337_4_commutator_bound",
            "check": "commutator theorem and scenarios include ell_s/L_var plus boundary bound",
            "passed": any("ell_s/L_var" in row["result"] for row in comm)
            and any(float(row["delta_comm_bound"]) > DELTA_COMM_ALLOWED for row in comm_bounds)
            and any(row["passes_ref_ceiling"] == "true" for row in comm_bounds),
            "detail": "",
        },
        {
            "check_id": "VAL3337_5_contact_theorem",
            "check": "contact theorem includes absorbed zero and p>=2/p>=4 scale branches",
            "passed": any("epsilon_contact_PPN=0" in row["statement"] for row in contact)
            and any("p_contact>=2" in row["result"] and "p_contact>=4" in row["result"] for row in contact),
            "detail": "",
        },
        {
            "check_id": "VAL3337_6_contact_bounds",
            "check": "contact scenarios include pass and fail cases for p=2/p=4",
            "passed": any(row["passes_comp_budget"] == "true" for row in contact_bounds)
            and any(row["passes_comp_budget"] == "false" for row in contact_bounds)
            and {2, 4}.issubset({int(row["p_contact"]) for row in contact_bounds}),
            "detail": "",
        },
        {
            "check_id": "VAL3337_7_composite_update",
            "check": "updated composite budget has best, bounded, and fail cases",
            "passed": {"CUP3337_0_best_case", "CUP3337_1_bounded_case", "CUP3337_2_fail_case"}.issubset(
                {row["update_id"] for row in comp_update}
            ),
            "detail": "",
        },
        {
            "check_id": "VAL3337_8_requirements",
            "check": "requirements include projector, patch, L_var, contact tensor, ell_c, and spectral tail",
            "passed": {"REQ3337_0_PPN_projector_symbol", "REQ3337_1_kernel_interior_patch", "REQ3337_2_L_var_boundary", "REQ3337_3_contact_tensor_structure", "REQ3337_4_ellc_power", "REQ3337_5_spectral_tail"}.issubset(
                {row["input_id"] for row in requirements}
            ),
            "detail": "",
        },
        {
            "check_id": "VAL3337_9_no_claim",
            "check": "theorem gates pass while composite/local-GR claim gates remain false",
            "passed": all(
                row["passed"] == "true"
                for row in gates
                if row["gate_id"] in {"GATE3337_0_commutator_zero_theorem", "GATE3337_1_commutator_bound", "GATE3337_2_contact_scaling"}
            )
            and all(
                row["passed"] == "false"
                for row in gates
                if row["gate_id"] in {"GATE3337_3_composite_claim_ready", "GATE3337_4_local_GR_claim"}
            ),
            "detail": "",
        },
        {
            "check_id": "VAL3337_10_next_3338",
            "check": "next target sources PPN projector/patch geometry",
            "passed": any("P_PPN" in row["objective"] and "L_var" in row["objective"] for row in next_target_rows()),
            "detail": "",
        },
        {
            "check_id": "VAL3337_11_formalization_untouched",
            "check": "formalization-workbench modified-file count remains zero by this script",
            "passed": fw_changed == 0,
            "detail": f"formalization_changed_count={fw_changed}",
        },
    ]
    overall = all(bool(check["passed"]) for check in checks)
    checks.append(
        {
            "check_id": "VAL3337_12_overall",
            "check": "3337 validation overall",
            "passed": overall,
            "detail": "all required checks passed" if overall else "one or more checks failed",
        }
    )
    for check in checks:
        check["passed"] = bool_str(bool(check["passed"]))
    return checks


def render_doc() -> str:
    lines: list[str] = [
        "# 3337 - PPN commutator/contact zero-or-bound theorem under AX1090",
        "",
        f"Run UTC: `{RUN_UTC}`",
        "",
        "## Verdict",
        "",
        "3337 makes the dominant composite floor more mathematical.",
        "",
        "The clean commutator theorem is:",
        "",
        "`delta_comm_PPN = 0`",
        "",
        "if the PPN projector/readout and smoothing operator are both translation-invariant Fourier multipliers on an interior local patch.",
        "",
        "The bounded-defect theorem is:",
        "",
        "`delta_comm_PPN <= C_comm ell_s/L_var + C_boundary exp[-d_boundary^2/(2 ell_s^2)] + epsilon_gauge_res`.",
        "",
        f"Using the 3336 reference budget, the first commutator ceiling remains `delta_comm_PPN <= {DELTA_COMM_ALLOWED:.3e}` for `sigma_Dpi=1e-3`.",
        "",
        "The contact theorem is:",
        "",
        "`epsilon_contact_PPN = 0`",
        "",
        "for universal contact pieces absorbed into measured local constants, and otherwise",
        "",
        "`epsilon_contact_PPN <= C_contact (ell_c/L_PPN)^p_contact`",
        "",
        "with `p_contact>=2` generally and `p_contact>=4` if the second-derivative local term is also absorbed or symmetry-forbidden.",
        "",
        "So we did not prove the composite floor away completely, but we turned it from a mystery floor into exact zero conditions plus explicit finite-size bounds.",
        "",
        "No PPN/local-GR pass is claimed.",
        "",
        "## Source Register",
        "",
    ]
    for row in source_rows():
        lines.append(
            f"- `{row['source_id']}`: `{row['path']}` exists={row['exists']} parse_ok={row['parse_ok']} role={row['role']}"
        )
    sections = [
        ("Commutator Theorem", commutator_theorem_rows(), "theorem_id"),
        ("Commutator Bound Scenarios", commutator_bound_rows(), "scenario_id"),
        ("Contact Theorem", contact_theorem_rows(), "theorem_id"),
        ("Contact Bound Scenarios", contact_bound_rows(), "scenario_id"),
        ("Composite Budget Update", composite_update_rows(), "update_id"),
        ("Required Inputs", required_input_rows(), "input_id"),
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
            "- It proves/bounds structure, not source-owned numerical PPN safety.",
            "- It keeps the Cassini-gamma candidate as a steering threshold only.",
            "- `formalization-workbench` is not modified.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> None:
    formalization_before = snapshot_tree(FW)
    OUT.mkdir(parents=True, exist_ok=True)
    write_csv(OUTPUTS["sources"], source_rows())
    write_csv(OUTPUTS["commutator"], commutator_theorem_rows())
    write_csv(OUTPUTS["comm_bounds"], commutator_bound_rows())
    write_csv(OUTPUTS["contact"], contact_theorem_rows())
    write_csv(OUTPUTS["contact_bounds"], contact_bound_rows())
    write_csv(OUTPUTS["composite_update"], composite_update_rows())
    write_csv(OUTPUTS["requirements"], required_input_rows())
    write_csv(OUTPUTS["gates"], promotion_gate_rows())
    write_csv(OUTPUTS["decision"], decision_rows())
    write_csv(OUTPUTS["next"], next_target_rows())
    DOC.write_text(render_doc(), encoding="utf-8")
    write_csv(OUTPUTS["validation"], validate_outputs(formalization_before))
    if PYCACHE.exists():
        shutil.rmtree(PYCACHE)


if __name__ == "__main__":
    main()
