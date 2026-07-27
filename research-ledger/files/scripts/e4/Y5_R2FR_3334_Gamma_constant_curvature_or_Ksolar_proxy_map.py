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

DOC = ROOT / "3334-Y5-R2FR-Gamma-constant-curvature-or-Ksolar-proxy-map-under-AX1090.md"

SRC_GRAVITY = REPO / "core-mts-framework" / "gravity" / "motion-timespace-mts-gravity.md"
SRC_ACTION = REPO / "core-mts-framework" / "action-principle" / "the-motion-timespace-action-principle.md"
SRC_FUNDAMENTAL = REPO / "core-mts-framework" / "action-principle" / "the-fundamental-action-of-motion-timespace-field-theory.md"

SOURCES = [
    {
        "source_id": "SRC3334_0_3333_doc",
        "path": ROOT / "3333-Y5-R2FR-PPN-zero-floor-branch-certificate-under-AX1090.md",
        "role": "reduced PPN budget and Gamma handoff",
    },
    {
        "source_id": "SRC3334_1_3333_reduced",
        "path": OUT / "P8_Y5_R2FR_3333_REDUCED_PPN_BUDGET.csv",
        "role": "Gamma/tree/composite reduced PPN budget",
    },
    {
        "source_id": "SRC3334_2_3333_gamma",
        "path": OUT / "P8_Y5_R2FR_3333_GAMMA_BRANCH_CERTIFICATE.csv",
        "role": "finite pole zero and constant/proxy residual clauses",
    },
    {
        "source_id": "SRC3334_3_3332_gamma",
        "path": OUT / "P8_Y5_R2FR_3332_GAMMA_FLOOR_BRANCHES.csv",
        "role": "Gamma floor formulas from 3332",
    },
    {
        "source_id": "SRC3334_4_3330_floors",
        "path": OUT / "P8_Y5_R2FR_3330_LOCAL_FLOOR_BOUNDS.csv",
        "role": "general Gamma PPN floor and K_solar proxy",
    },
    {
        "source_id": "SRC3334_5_3321_proxy",
        "path": OUT / "P8_Y5_R2FR_3321_SOLAR_PROXY_BOUND.csv",
        "role": "K_solar^m internal scale rows",
    },
    {
        "source_id": "SRC3334_6_3318_no_pole",
        "path": OUT / "P8_Y5_R2FR_3318_NONPROPAGATION_THEOREM_ATTEMPT.csv",
        "role": "conditional Gamma no-pole proof",
    },
    {
        "source_id": "SRC3334_7_core_gravity",
        "path": SRC_GRAVITY,
        "role": "K_solar, PPN O(K^m), and homogeneous Gamma statements",
    },
    {
        "source_id": "SRC3334_8_action",
        "path": SRC_ACTION,
        "role": "Gamma_G g_munu action variation and GR/Lambda limits",
    },
    {
        "source_id": "SRC3334_9_fundamental",
        "path": SRC_FUNDAMENTAL,
        "role": "Gamma_G as scalar functional and IR limit",
    },
    {
        "source_id": "SRC3334_10_closure_assumptions",
        "path": OUT / "P8_Y5_R2FR_3324_CLOSURE_ASSUMPTION_LEDGER.csv",
        "role": "local residual suppression and matter/G closure assumptions",
    },
]

OUTPUTS = {
    "sources": OUT / "P8_Y5_R2FR_3334_SOURCE_REGISTER.csv",
    "branch_map": OUT / "P8_Y5_R2FR_3334_GAMMA_BRANCH_MAP.csv",
    "constant": OUT / "P8_Y5_R2FR_3334_CONSTANT_CURVATURE_BOUND.csv",
    "proxy": OUT / "P8_Y5_R2FR_3334_KSOLAR_PROXY_MAP_ATTEMPT.csv",
    "residual": OUT / "P8_Y5_R2FR_3334_GAMMA_RESIDUAL_DECISION.csv",
    "budget": OUT / "P8_Y5_R2FR_3334_UPDATED_REDUCED_PPN_BUDGET.csv",
    "inputs": OUT / "P8_Y5_R2FR_3334_REQUIRED_INPUTS.csv",
    "gates": OUT / "P8_Y5_R2FR_3334_PROMOTION_GATES.csv",
    "decision": OUT / "P8_Y5_R2FR_3334_DECISION_LEDGER.csv",
    "next": OUT / "P8_Y5_R2FR_3334_NEXT_TARGET.csv",
    "validation": OUT / "P8_Y5_BRR545_3334_VALIDATION.csv",
}

RUN_UTC = datetime.now(timezone.utc).isoformat()

H0_KM_S_MPC = 70.0
C_M_S = 299_792_458.0
MPC_M = 3.0856775814913673e22
AU_M = 1.495978707e11
H0_SI = H0_KM_S_MPC * 1000.0 / MPC_M
L_H_M = C_M_S / H0_SI
K_SOLAR_PROXY = 1.0e-61
M_MIN_PROXY = 2.0
K_PROXY_BOUND = K_SOLAR_PROXY**M_MIN_PROXY


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


def lambda_like_scale_rows() -> list[dict[str, Any]]:
    scales = [
        ("SCALE3334_AU", "1_AU_solar_system_scale", AU_M),
        ("SCALE3334_10AU", "10_AU_outer_solar_scale", 10.0 * AU_M),
        ("SCALE3334_100AU", "100_AU_wide_orbital_scale", 100.0 * AU_M),
    ]
    rows: list[dict[str, Any]] = []
    for row_id, label, length_m in scales:
        ratio = length_m / L_H_M
        rows.append(
            {
                "scale_id": row_id,
                "branch": "Lambda_like_background",
                "label": label,
                "L_PPN_m": f"{length_m:.12e}",
                "assumed_H0_km_s_Mpc": f"{H0_KM_S_MPC:.3f}",
                "L_H_m": f"{L_H_M:.12e}",
                "dimensionless_floor": f"{ratio * ratio:.12e}",
                "formula": "(L_PPN/L_H)^2, equivalent to |Gamma_cosmo| L_PPN^2 when |Gamma_cosmo|~L_H^-2",
                "claim_status": "ORDER_OF_MAGNITUDE_NONCLAIM",
                "valid_for_claim": "false",
            }
        )
    return rows


def branch_map_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": "GBM3334_0_finite_pole",
            "Gamma_interpretation": "Gamma_G readout/background, no independent local perturbation",
            "floor_formula": "R_Gamma_PPN^pole=0",
            "derivation": "3333/3318: no x row in local Hessian, so no finite Gamma exchange pole couples into PPN",
            "result": "closed conditionally",
            "next_requirement": "keep Gamma_G out of the local field basis or provide a parent constraint if reintroduced",
            "valid_for_claim": "false",
        },
        {
            "branch_id": "GBM3334_1_Lambda_like",
            "Gamma_interpretation": "homogeneous Lambda-like background after local subtraction",
            "floor_formula": "R_Gamma_PPN <= A_Gamma |Gamma_cosmo| L_PPN^2 ~ A_Gamma (L_PPN/L_H)^2",
            "derivation": "Gamma_G g_munu has the same local metric form as a cosmological-constant curvature term; local PPN sensitivity is quadratic in system length over curvature radius",
            "result": "bounded symbolically with tiny nonclaim scale check",
            "next_requirement": "source Gamma_cosmo or H0/L_H and A_Gamma for the chosen PPN arena",
            "valid_for_claim": "false",
        },
        {
            "branch_id": "GBM3334_2_Ksolar_proxy",
            "Gamma_interpretation": "local curvature-saturation response",
            "floor_formula": "R_Gamma_PPN <= A_K K_solar^m <= A_K 1e-122 for K_solar~1e-61 and m>=2",
            "derivation": "core gravity file states PPN gamma,beta = 1+O(K^m); this only applies to Gamma if local Gamma residual is the same saturation response",
            "result": "encouraging but not parent-signed",
            "next_requirement": "derive map Gamma_local -> S(K_local)=K_local^m/(1+K_local^m) in the local PPN branch",
            "valid_for_claim": "false",
        },
        {
            "branch_id": "GBM3334_3_open_local_memory",
            "Gamma_interpretation": "unsubtracted local memory/gradient residue",
            "floor_formula": "R_Gamma_PPN <= A_Gamma |Gamma_local| L_PPN^2 plus possible gradient/source terms",
            "derivation": "if Gamma carries local nonhomogeneous memory not reducible to Lambda-like background or K_saturation, the remaining floor is not closed",
            "result": "open residual floor",
            "next_requirement": "source Gamma_local, prove local subtraction, or move to numerical bound acquisition",
            "valid_for_claim": "false",
        },
    ]


def constant_curvature_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "bound_id": "CC3334_0_general",
            "quantity": "constant-curvature Gamma floor",
            "formula": "R_Gamma_PPN <= A_Gamma_PPN |Gamma_local| L_PPN^2",
            "derivation": "In the readout/background branch, Gamma_G g_munu contributes as a local constant-curvature term; dimensionless metric/PPN residuals scale as curvature times length squared.",
            "status": "DERIVED_SYMBOLIC_BOUND",
            "valid_for_claim": "false",
        },
        {
            "bound_id": "CC3334_1_Lambda_like",
            "quantity": "Lambda-like background ceiling",
            "formula": "if |Gamma_local| <= L_H^-2, then R_Gamma_PPN <= A_Gamma_PPN (L_PPN/L_H)^2",
            "derivation": "When Gamma_G -> Lambda or a homogeneous cosmological background, the local de Sitter correction is suppressed by the squared ratio of local system size to cosmological curvature radius.",
            "status": "LAMBDA_BRANCH_BOUND",
            "valid_for_claim": "false",
        },
        {
            "bound_id": "CC3334_2_background_subtraction",
            "quantity": "subtracted cosmological background",
            "formula": "if Gamma_local is fully absorbed into the fitted cosmological background and local PPN uses the residual Gamma_res, replace Gamma_local by Gamma_res",
            "derivation": "PPN tests are local residual tests; a homogeneous background belongs in cosmology unless an unabsorbed local curvature correction remains.",
            "status": "SUBTRACTION_RULE",
            "valid_for_claim": "false",
        },
    ]
    rows.extend(lambda_like_scale_rows())
    return rows


def ksolar_proxy_rows() -> list[dict[str, Any]]:
    return [
        {
            "map_id": "KMAP3334_0_core_statement",
            "claim": "core gravity says PPN gamma,beta = 1 + O(K^m) with K_solar~1e-61 and m>=2",
            "map_condition": "the local Gamma residual entering PPN must be the same curvature-saturation response S(K)",
            "formula": f"K_solar^m <= {K_PROXY_BOUND:.3e}",
            "status": "SOURCE_STATEMENT_IMPORTED",
            "valid_for_claim": "false",
        },
        {
            "map_id": "KMAP3334_1_required_parent_map",
            "claim": "Gamma_local -> S(K_local)=K_local^m/(1+K_local^m)",
            "map_condition": "Gamma_G functional and local PPN readout must reduce to the same saturation scalar in the weak-field solar patch",
            "formula": "R_Gamma_PPN <= A_K S(K_solar) <= A_K K_solar^m",
            "status": "MAP_NOT_SIGNED",
            "valid_for_claim": "false",
        },
        {
            "map_id": "KMAP3334_2_proxy_guard",
            "claim": "K_solar^m cannot bound psi tree or composite tails",
            "map_condition": "proxy applies only to the Gamma/saturation channel after a Gamma->K map, not to public psi residues",
            "formula": "epsilon_eff_PPN and epsilon_composite_PPN remain separate floors",
            "status": "NO_CROSS_APPLICATION_GUARD",
            "valid_for_claim": "false",
        },
        {
            "map_id": "KMAP3334_3_partial_result",
            "claim": "K_solar path is promising but not enough to remove Gamma floor",
            "map_condition": "no parent-owned equality Gamma_residual = S(K_solar) found in current source sweep",
            "formula": "retain min-style fork: R_Gamma <= min_if_signed(A_Gamma Gamma_local L^2, A_K K_solar^m), otherwise keep explicit R_Gamma",
            "status": "NONCLAIM_PROMISING_FORK",
            "valid_for_claim": "false",
        },
    ]


def residual_decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "GDEC3334_0",
            "question": "Can total Gamma be removed from the PPN budget?",
            "answer": "not yet",
            "reason": "finite pole is zero, but constant-curvature/proxy residual needs either Gamma_local bound or parent-signed K_solar map",
            "action": "keep Gamma as a tiny-or-open explicit floor",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "GDEC3334_1",
            "question": "Is the Lambda-like branch dangerous?",
            "answer": "probably not if Gamma_local is cosmological-background scale",
            "reason": "nonclaim scale rows give (L_PPN/L_H)^2 around solar-system lengths, which is tiny before A_Gamma factors",
            "action": "source A_Gamma and chosen PPN length if using this as a claim",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "GDEC3334_2",
            "question": "Is the K_solar branch enough?",
            "answer": "not as a proof",
            "reason": "core gravity supports O(K^m) PPN corrections, but the parent map from Gamma residual to K_solar^m is not signed",
            "action": "either derive the map or stop treating K_solar as a Gamma pass",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "GDEC3334_3",
            "question": "What remains after 3334?",
            "answer": "Gamma is narrowed but retained; composite/tree are now the main hard floors",
            "reason": "Gamma has strong plausible suppression branches but not a claim-grade source-owned closure",
            "action": "move to composite/tree envelope unless trying one more Gamma source-bound acquisition pass",
            "valid_for_claim": "false",
        },
    ]


def updated_budget_rows() -> list[dict[str, Any]]:
    return [
        {
            "budget_id": "UB3334_0_reduced_with_Gamma_fork",
            "formula": "R_PPN <= R_Gamma_fork + A_PPN C_metric epsilon_eff_PPN^2 + epsilon_composite_PPN",
            "Gamma_fork": "R_Gamma_fork is zero only for finite pole; total Gamma is either A_Gamma |Gamma_local| L_PPN^2, A_K K_solar^m if parent-signed, or explicit open floor",
            "status": "REDUCED_BUDGET_WITH_GAMMA_FORK",
            "valid_for_claim": "false",
        },
        {
            "budget_id": "UB3334_1_Lambda_like_candidate",
            "formula": "R_PPN <= A_Gamma (L_PPN/L_H)^2 + A_PPN C_metric epsilon_eff_PPN^2 + epsilon_composite_PPN",
            "Gamma_fork": "valid only if Gamma_local is bounded by cosmological background scale or residual after subtraction",
            "status": "LAMBDA_CANDIDATE_NONCLAIM",
            "valid_for_claim": "false",
        },
        {
            "budget_id": "UB3334_2_Ksolar_candidate",
            "formula": "R_PPN <= A_K K_solar^m + A_PPN C_metric epsilon_eff_PPN^2 + epsilon_composite_PPN",
            "Gamma_fork": "valid only if parent map signs Gamma_local residual to curvature-saturation S(K_solar)",
            "status": "KSOLAR_CANDIDATE_NONCLAIM",
            "valid_for_claim": "false",
        },
        {
            "budget_id": "UB3334_3_if_Gamma_unclosed",
            "formula": "R_PPN <= R_Gamma_open + A_PPN C_metric epsilon_eff_PPN^2 + epsilon_composite_PPN",
            "Gamma_fork": "use this if neither Gamma_local nor K_solar map is source-owned",
            "status": "OPEN_GAMMA_FALLBACK",
            "valid_for_claim": "false",
        },
    ]


def required_input_rows() -> list[dict[str, Any]]:
    return [
        {
            "input_id": "REQ3334_0_A_Gamma",
            "quantity": "A_Gamma_PPN",
            "needed_for": "constant-curvature PPN floor",
            "current_status": "SYMBOLIC_ONLY",
            "valid_for_claim": "false",
        },
        {
            "input_id": "REQ3334_1_Gamma_local",
            "quantity": "Gamma_local or Gamma_res after background subtraction",
            "needed_for": "A_Gamma |Gamma_local| L_PPN^2 claim",
            "current_status": "NOT_SOURCE_BOUND",
            "valid_for_claim": "false",
        },
        {
            "input_id": "REQ3334_2_L_PPN",
            "quantity": "arena-specific PPN length scale",
            "needed_for": "constant-curvature and Lambda-like scale comparison",
            "current_status": "EXAMPLE_ONLY_NOT_ARENA_SOURCED",
            "valid_for_claim": "false",
        },
        {
            "input_id": "REQ3334_3_K_map",
            "quantity": "parent map Gamma_residual -> S(K_local)",
            "needed_for": "K_solar^m Gamma proxy promotion",
            "current_status": "MISSING_PARENT_MAP",
            "valid_for_claim": "false",
        },
        {
            "input_id": "REQ3334_4_A_K",
            "quantity": "A_K observable coefficient",
            "needed_for": "K_solar proxy PPN residual amplitude",
            "current_status": "SYMBOLIC_ONLY",
            "valid_for_claim": "false",
        },
    ]


def promotion_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "GATE3334_0_constant_bound",
            "claim": "constant-curvature Gamma floor has a derived bound",
            "passed": "true",
            "reason": "R_Gamma <= A_Gamma |Gamma_local| L_PPN^2 and Lambda-like (L/L_H)^2 branch are explicit",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3334_1_Lambda_scale_smoke",
            "claim": "Lambda-like branch has nonclaim order-of-magnitude scale rows",
            "passed": "true",
            "reason": "1, 10, and 100 AU examples are generated as nonclaim sanity checks",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3334_2_Ksolar_proxy_guard",
            "claim": "K_solar proxy path is stated with parent-map guard",
            "passed": "true",
            "reason": "proxy rows require Gamma_local -> S(K_local) and block application to tree/composite tails",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3334_3_Gamma_removed",
            "claim": "total Gamma floor is removed from PPN budget",
            "passed": "false",
            "reason": "Gamma_local bound or parent-signed K_solar map is still missing",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3334_4_Gamma_claim_ready",
            "claim": "Gamma floor is claim-grade below PPN threshold",
            "passed": "false",
            "reason": "A_Gamma, Gamma_local/L_PPN or K-map/A_K, and real B_PPN are not sourced",
            "valid_for_claim": "false",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3334_0",
            "question": "Did 3334 remove Gamma?",
            "answer": "no, but it made Gamma much sharper",
            "reason": "Gamma is no longer a vague problem: it is finite-pole zero plus either Lambda-like curvature, K_solar proxy, or open local residue",
            "next_action": "do not spend more loops on Gamma unless sourcing Gamma_local or deriving Gamma->K map",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC3334_1",
            "question": "Best route after 3334?",
            "answer": "move to composite/tree PPN envelope",
            "reason": "direct/G floors are branch-zero, Gamma is probably small in plausible branches but not claim-grade; composite/tree are the remaining hard floors",
            "next_action": "specialize composite commutator/CLT and tree epsilon_eff into a first numeric nonclaim envelope",
            "valid_for_claim": "false",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "target_doc": "3335-Y5-R2FR-PPN-composite-tree-envelope-first-numeric-nonclaim-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3335_PPN_composite_tree_envelope_first_numeric_nonclaim.py",
            "objective": "build the first reduced PPN nonclaim numeric envelope for tree leakage and composite floors using the 3331-3334 budget, with Gamma retained as a forked floor",
            "must_include": "A_PPN C_metric symbolic/numeric placeholders clearly marked; epsilon_eff T_grad scenarios; composite CLT/contact scenarios; Gamma fork rows; no PPN pass claim",
            "fallback_if_failed": "write a source-bound acquisition table for A_PPN, C_metric, epsilon_eff, composite spectral/contact inputs, and Gamma_local",
            "valid_for_claim": "false",
        }
    ]


def validate_outputs(formalization_before: dict[str, tuple[int, int]]) -> list[dict[str, Any]]:
    sources = source_register_rows()
    branch = branch_map_rows()
    constant = constant_curvature_rows()
    proxy = ksolar_proxy_rows()
    budget = updated_budget_rows()
    inputs = required_input_rows()
    gates = promotion_gate_rows()
    output_paths = [path for key, path in OUTPUTS.items() if key != "validation"]
    fw_changed = changed_count(formalization_before, snapshot_tree(FW))
    checks = [
        {
            "check_id": "VAL3334_0_sources_exist",
            "check": "all cited source paths exist",
            "passed": all(row["exists"] == "true" for row in sources),
            "detail": "",
        },
        {
            "check_id": "VAL3334_1_sources_parse",
            "check": "all cited source paths parse",
            "passed": all(row["parse_ok"] == "true" for row in sources),
            "detail": "",
        },
        {
            "check_id": "VAL3334_2_outputs_parse",
            "check": "all 3334 non-validation outputs parse",
            "passed": all(path.exists() and parse_ok(path) for path in output_paths),
            "detail": "",
        },
        {
            "check_id": "VAL3334_3_branch_fork",
            "check": "branch map includes pole, Lambda-like, K_solar, and open local memory branches",
            "passed": {"GBM3334_0_finite_pole", "GBM3334_1_Lambda_like", "GBM3334_2_Ksolar_proxy", "GBM3334_3_open_local_memory"}.issubset(
                {row["branch_id"] for row in branch}
            ),
            "detail": "",
        },
        {
            "check_id": "VAL3334_4_constant_bound",
            "check": "constant-curvature bound includes A_Gamma Gamma_local L^2 and Lambda-like scale rows",
            "passed": any("A_Gamma_PPN |Gamma_local| L_PPN^2" in row["formula"] for row in constant)
            and any("(L_PPN/L_H)^2" in row["formula"] for row in constant)
            and len([row for row in constant if row.get("branch") == "Lambda_like_background"]) == 3,
            "detail": "",
        },
        {
            "check_id": "VAL3334_5_proxy_guard",
            "check": "K_solar map attempt includes parent-map requirement and no cross-application guard",
            "passed": any("Gamma_local -> S(K_local)" in row["claim"] for row in proxy)
            and any("cannot bound psi tree or composite" in row["claim"] for row in proxy)
            and any("1.000e-122" in row["formula"] for row in proxy),
            "detail": "",
        },
        {
            "check_id": "VAL3334_6_updated_budget",
            "check": "updated budget keeps Gamma fork and tree/composite floors",
            "passed": any("R_Gamma_fork" in row["formula"] and "epsilon_composite_PPN" in row["formula"] for row in budget)
            and any("A_K K_solar^m" in row["formula"] for row in budget),
            "detail": "",
        },
        {
            "check_id": "VAL3334_7_inputs",
            "check": "required inputs include A_Gamma, Gamma_local, L_PPN, K map, and A_K",
            "passed": {"REQ3334_0_A_Gamma", "REQ3334_1_Gamma_local", "REQ3334_2_L_PPN", "REQ3334_3_K_map", "REQ3334_4_A_K"}.issubset(
                {row["input_id"] for row in inputs}
            ),
            "detail": "",
        },
        {
            "check_id": "VAL3334_8_no_claim",
            "check": "symbolic Gamma gates pass while removal/claim gates remain false",
            "passed": all(
                row["passed"] == "true"
                for row in gates
                if row["gate_id"] in {"GATE3334_0_constant_bound", "GATE3334_1_Lambda_scale_smoke", "GATE3334_2_Ksolar_proxy_guard"}
            )
            and all(
                row["passed"] == "false"
                for row in gates
                if row["gate_id"] in {"GATE3334_3_Gamma_removed", "GATE3334_4_Gamma_claim_ready"}
            ),
            "detail": "",
        },
        {
            "check_id": "VAL3334_9_next_3335",
            "check": "next target moves to composite/tree first numeric nonclaim envelope",
            "passed": any("composite" in row["objective"] and "tree" in row["objective"] for row in next_target_rows()),
            "detail": "",
        },
        {
            "check_id": "VAL3334_10_formalization_untouched",
            "check": "formalization-workbench modified-file count remains zero by this script",
            "passed": fw_changed == 0,
            "detail": f"formalization_changed_count={fw_changed}",
        },
    ]
    overall = all(bool(check["passed"]) for check in checks)
    checks.append(
        {
            "check_id": "VAL3334_11_overall",
            "check": "3334 validation overall",
            "passed": overall,
            "detail": "all required checks passed" if overall else "one or more checks failed",
        }
    )
    for check in checks:
        check["passed"] = bool_str(bool(check["passed"]))
    return checks


def render_doc() -> str:
    one_au_floor = (AU_M / L_H_M) ** 2
    lines: list[str] = [
        "# 3334 - Gamma constant-curvature or K_solar proxy map under AX1090",
        "",
        f"Run UTC: `{RUN_UTC}`",
        "",
        "## Verdict",
        "",
        "3334 does not fully remove the Gamma floor, but it turns it into a precise fork.",
        "",
        "The finite Gamma exchange pole remains closed in the clean readout/background branch:",
        "",
        "`R_Gamma_PPN^pole = 0`.",
        "",
        "The remaining total Gamma floor has three possible meanings:",
        "",
        "1. Lambda-like background:",
        "",
        "`R_Gamma_PPN <= A_Gamma_PPN |Gamma_local| L_PPN^2 ~ A_Gamma_PPN (L_PPN/L_H)^2`.",
        "",
        f"As a nonclaim sanity check, for `L_PPN=1 AU` and `H0={H0_KM_S_MPC:g} km/s/Mpc`, `(L_PPN/L_H)^2 = {one_au_floor:.3e}`.",
        "",
        "2. Curvature-saturation proxy:",
        "",
        f"`R_Gamma_PPN <= A_K K_solar^m <= A_K {K_PROXY_BOUND:.3e}` for `K_solar~1e-61`, `m>=2`.",
        "",
        "This is promising, but only if a parent map signs `Gamma_local -> S(K_local)` in the PPN branch.",
        "",
        "3. Open local memory residue:",
        "",
        "`R_Gamma_PPN <= A_Gamma_PPN |Gamma_local| L_PPN^2` remains explicit if Gamma is neither background-subtracted nor mapped to saturation.",
        "",
        "So the updated reduced budget is",
        "",
        "`R_PPN <= R_Gamma_fork + A_PPN C_metric epsilon_eff_PPN^2 + epsilon_composite_PPN`.",
        "",
        "That means Gamma is probably not the first monster to fight unless we are ready to source `Gamma_local` or derive the `Gamma -> K_solar` map. The next efficient target is the composite/tree envelope.",
        "",
        "No PPN/local-GR pass is claimed.",
        "",
        "## Source Register",
        "",
    ]
    for row in source_register_rows():
        lines.append(
            f"- `{row['source_id']}`: `{row['path']}` exists={row['exists']} parse_ok={row['parse_ok']} role={row['role']}"
        )
    sections = [
        ("Gamma Branch Map", branch_map_rows(), "branch_id"),
        ("Constant Curvature Bound", constant_curvature_rows(), "bound_id"),
        ("Ksolar Proxy Map Attempt", ksolar_proxy_rows(), "map_id"),
        ("Gamma Residual Decision", residual_decision_rows(), "decision_id"),
        ("Updated Reduced PPN Budget", updated_budget_rows(), "budget_id"),
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
            "- The Hubble-length scale rows are order-of-magnitude sanity checks, not observational source rows.",
            "- The `K_solar^m` route is explicitly blocked from claiming Gamma closure without a parent map.",
            "- Tree leakage and composite tails remain independent floors.",
            "- `formalization-workbench` is not modified.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> None:
    formalization_before = snapshot_tree(FW)
    OUT.mkdir(parents=True, exist_ok=True)
    write_csv(OUTPUTS["sources"], source_register_rows())
    write_csv(OUTPUTS["branch_map"], branch_map_rows())
    write_csv(OUTPUTS["constant"], constant_curvature_rows())
    write_csv(OUTPUTS["proxy"], ksolar_proxy_rows())
    write_csv(OUTPUTS["residual"], residual_decision_rows())
    write_csv(OUTPUTS["budget"], updated_budget_rows())
    write_csv(OUTPUTS["inputs"], required_input_rows())
    write_csv(OUTPUTS["gates"], promotion_gate_rows())
    write_csv(OUTPUTS["decision"], decision_rows())
    write_csv(OUTPUTS["next"], next_target_rows())
    DOC.write_text(render_doc(), encoding="utf-8")
    write_csv(OUTPUTS["validation"], validate_outputs(formalization_before))
    if PYCACHE.exists():
        shutil.rmtree(PYCACHE)


if __name__ == "__main__":
    main()
