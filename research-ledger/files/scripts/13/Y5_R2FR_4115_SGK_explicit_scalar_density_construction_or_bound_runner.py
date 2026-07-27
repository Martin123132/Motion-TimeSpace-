from __future__ import annotations

import csv
import py_compile
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Tuple


ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
SOURCE_DIR = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = PROJECT / "formalization-workbench"
SCRIPT_PATH = Path(__file__).resolve()
DOC_PATH = ROOT / "4115-Y5-R2FR-SGK-explicit-scalar-density-construction-or-bound-runner.md"

TIMESTAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
BRANCH_ID = "MTS_R2FR_Y5_SGK_SCALAR_DENSITY_CURRENT_SPINE_4115"
CHECKPOINT_ID = "4115"
DECISION = "EVEN_RESPONSE_SCALAR_DENSITY_IMPORTED_F1_ZERO_FOUND_JZ_COUPLING_NEXT"


LOCAL_SOURCES: Dict[str, Tuple[Path, str, str]] = {
    "SRC4115_00_4114_next": (
        SOURCE_DIR / "P8_Y5_R2FR_4114_NEXT_TARGET.csv",
        "4115-Y5-R2FR-SGK-explicit-scalar-density-construction-or-bound-runner.md",
        "4114 selected explicit Gamma_eff scalar-density construction as next target.",
    ),
    "SRC4115_01_4114_status": (
        SOURCE_DIR / "P8_Y5_R2FR_4114_STATUS.csv",
        "GK_QLOC_STRESS_IDENTITY_AND_CONDITIONAL_SGK_ROUTE_IMPORTED_SCALAR_DENSITY_NEXT",
        "Current-chain GK/q_loc Helmholtz handoff.",
    ),
    "SRC4115_02_3628_status": (
        SOURCE_DIR / "P8_Y5_R2FR_3628_STATUS.csv",
        "EVEN_RESPONSE_SCALAR_DENSITY_CONSTRUCTED_PARENT_MATCH_UNSIGNED_NO_CLAIM",
        "3628 constructs explicit scalar-density candidates and identifies even response-doublet route.",
    ),
    "SRC4115_03_3628_candidates": (
        SOURCE_DIR / "P8_Y5_R2FR_3628_EXPLICIT_SCALAR_DENSITY_CANDIDATES.csv",
        "GSD3628_2_even_response_doublet",
        "Explicit scalar-density candidate classes.",
    ),
    "SRC4115_04_3628_kmetric": (
        SOURCE_DIR / "P8_Y5_R2FR_3628_KMETRIC_KHAT_COMPARISON.csv",
        "KMC3628_5_verdict",
        "K_metric/K_hat comparison and residual R_K.",
    ),
    "SRC4115_05_3628_fixed_point": (
        SOURCE_DIR / "P8_Y5_R2FR_3628_FIXED_POINT_DOUBLE_ZERO_GATE.csv",
        "FPG3628_6_verdict",
        "Fixed-point, F1, coupling and boundary gates.",
    ),
    "SRC4115_06_3628_bound_runner": (
        SOURCE_DIR / "P8_Y5_R2FR_3628_QLOC_TGK_BOUND_RUNNER_ROWS.csv",
        "QBR3628_4_boundary",
        "q_loc/T_GK fallback runner rows after scalar-density construction.",
    ),
    "SRC4115_07_3628_decisions": (
        SOURCE_DIR / "P8_Y5_R2FR_3628_DECISION_GATES.csv",
        "DEC3628_3_next_target",
        "3628 decision selecting source-coupling J_Z as next bottleneck.",
    ),
    "SRC4115_08_3628_next": (
        SOURCE_DIR / "P8_Y5_R2FR_3628_NEXT_TARGET.csv",
        "3629-Y5-R2FR-response-doublet-source-coupling-zero-or-coefficient.md",
        "3628 next target: response-doublet source coupling zero or coefficient.",
    ),
    "SRC4115_09_script": (
        SCRIPT_PATH,
        "Y5_R2FR_4115_SGK_explicit_scalar_density_construction_or_bound_runner.py",
        "Reproducible generator for this 4115 checkpoint.",
    ),
}


def row_base() -> dict:
    return {"timestamp_utc": TIMESTAMP, "branch_id": BRANCH_ID, "checkpoint_id": CHECKPOINT_ID}


def bool_string(value: bool) -> str:
    return "True" if value else "False"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig", errors="replace")


def parse_csv(path: Path) -> List[dict]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: List[dict]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: List[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def is_under(path: Path, parent: Path) -> bool:
    try:
        path.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


def source_register_rows() -> List[dict]:
    rows = []
    for source_id, (path, needle, role) in LOCAL_SOURCES.items():
        text = read_text(path) if path.exists() else ""
        rows.append(
            {
                **row_base(),
                "source_id": source_id,
                "source_path": str(path),
                "exists": bool_string(path.exists()),
                "needle": needle,
                "needle_found": bool_string(path.exists() and needle in text),
                "role": role,
                "claim_allowed": bool_string(False),
                "valid_for_claim": bool_string(False),
            }
        )
    return rows


def scalar_density_candidate_rows() -> List[dict]:
    rows = [
        (
            "GSD4115_0_potential_background",
            "S_GK=-int sqrt(-g)[Gamma_0+V(Phi)]",
            "K_metric^{mu nu}=0 if V has no explicit metric dependence",
            "MATHEMATICALLY_VALID_TOO_WEAK_FOR_GENERAL_KHAT",
            "use only for pure background/potential branch",
        ),
        (
            "GSD4115_1_gradient_elastic",
            "S_GK=-int sqrt(-g)[V(Phi)+1/2 G_AB g^{rho sigma} nabla_rho Phi^A nabla_sigma Phi^B]",
            "K_metric^{mu nu}=G_AB nabla^mu Phi^A nabla^nu Phi^B plus coefficient metric-response terms",
            "PROMISING_TEMPLATE_SYMBOL_MATCH_MISSING",
            "requires K_hat decomposition into gradient/elastic anisotropic stress",
        ),
        (
            "GSD4115_2_even_response_doublet",
            "S_GK=-int sqrt(-g)[Gamma_0+1/2 M_AB Z^A Z^B+1/2 H_AB g^{rho sigma}nabla_rho Z^A nabla_sigma Z^B+O(Z^4)]",
            "K_metric^{mu nu}=H_AB nabla^mu Z^A nabla^nu Z^B plus metric/coefficient response terms",
            "BEST_CONDITIONAL_ROUTE_F1_ZERO_BY_EVENNESS_PARENT_MAPPING_MISSING",
            "Z=0 and nabla Z=0 gives T_GK=0 after background subtraction; parity gives partial_A T_GK|0=0",
        ),
        (
            "GSD4115_3_exact_boundary",
            "S_GK=int dB_GK or topological density",
            "bulk K_metric is zero or improvement tensor",
            "BOUNDARY_FLUX_RISK_OPEN_NONCLAIM",
            "viable only with no-flux or Hamiltonian handoff rows",
        ),
        (
            "GSD4115_4_wave_flux",
            "S_flux=-int sqrt(-g)[1/4 W_AB F^A_{rho sigma}F^{B rho sigma}]",
            "K_metric^{mu nu}=W_AB F^{A mu rho}F^B{}^{nu}{}_{rho}",
            "USEFUL_EM_STRESS_TEMPLATE_NOT_QLOC_ZERO_PROOF",
            "Poynting/wave flux is legitimate physical stress branch, not hidden local-GR silence",
        ),
        (
            "GSD4115_5_composite_spine",
            "S_GK=S_even_response_doublet+S_exact_boundary+S_physical_flux_if_present",
            "K_metric=K_Z+K_boundary_improvement+K_flux",
            "SELECTED_CONDITIONAL_SPINE_NOT_PARENT_SIGNED",
            "best current spine, with each unmatched remainder retained as residual",
        ),
    ]
    return [
        {
            **row_base(),
            "candidate_id": candidate_id,
            "ansatz": ansatz,
            "metric_response_formula": formula,
            "current_status": status,
            "interpretation": interpretation,
            "source_id": "SRC4115_03_3628_candidates",
            "claim_allowed": bool_string(False),
            "valid_for_claim": bool_string(False),
        }
        for candidate_id, ansatz, formula, status, interpretation in rows
    ]


def kmetric_comparison_rows() -> List[dict]:
    rows = [
        ("KMC4115_0_convention", "stress convention", "T_GK^{mu nu}=Gamma_eff g^{mu nu}-K_metric^{mu nu}", "R_K^{mu nu}:=K_hat^{mu nu}-K_metric^{mu nu}", "CONVENTION_DECLARED_NOT_GLOBAL_PARENT_LOCKED"),
        ("KMC4115_1_potential", "potential/background scalar", "K_metric=0", "R_K=K_hat", "TOO_WEAK_FOR_CURRENT_KHAT_MATCH"),
        ("KMC4115_2_gradient_elastic", "gradient/elastic anisotropic stress", "K_metric=G_AB nabla Phi nabla Phi plus coefficient response", "R_K=K_hat-G_AB nabla Phi nabla Phi-coefficient_response", "MATCH_MISSING_RESIDUAL_RETAINED"),
        ("KMC4115_3_even_response_doublet", "response doublet metric stress", "K_metric=H_AB nabla Z nabla Z plus metric/coefficient terms; mass potential contributes to Gamma g", "R_K=K_hat-K_Z and R_Z=physical_residual_vector-Z", "BEST_ROUTE_BUT_PARENT_MAP_UNSIGNED"),
        ("KMC4115_4_wave_flux", "Poynting/Maxwell-like stress", "K_metric=W_AB F^A F^B stress response", "R_flux=unowned Poynting/current stress contribution", "VALID_ACTION_SHAPE_RETAINED_FOR_EM_BRANCH_NOT_LOCAL_GR_CLAIM"),
        ("KMC4115_5_verdict", "K_hat=K_metric claim", "candidate K_metric formulas exist", "R_K^{mu nu} remains a scored local residual if no exact decomposition", "KMETRIC_CONSTRUCTED_KHAT_MATCH_NOT_CLAIMED"),
    ]
    return [
        {
            **row_base(),
            "comparison_id": comparison_id,
            "target_piece": target,
            "computed_from_candidate": computed,
            "residual_if_unmatched": residual,
            "status": status,
            "source_id": "SRC4115_04_3628_kmetric",
            "claim_allowed": bool_string(False),
            "valid_for_claim": bool_string(False),
        }
        for comparison_id, target, computed, residual, status in rows
    ]


def double_zero_mechanism_rows() -> List[dict]:
    rows = [
        ("FPG4115_0_fixed_point", "Z^A=0, nabla Z^A=0, Phi^A=Phi0 stationary", "T_GK zeroth-order local residual can be zero/background", "CONSTRUCTED_AS_CANDIDATE_NOT_PARENT_SELECTED"),
        ("FPG4115_1_background", "Gamma_eff(Phi0) absorbed into Lambda_eff or reference Hamiltonian", "constant scalar value does not act as local force", "STANDARD_ROUTE_WRITTEN_NOT_PARENT_LOCKED"),
        ("FPG4115_2_F1_zero", "partial_A T_GK^{mu nu}|0=0 by Z-parity and Gamma_0 subtraction", "linear fifth-force/PPN/source-normalization leakage removed for even template", "F1_ZERO_DERIVED_FOR_EVEN_RESPONSE_TEMPLATE_ONLY"),
        ("FPG4115_3_positive_operator", "M_AB positive and H_AB elliptic/self-adjoint after constraints/gauge removal", "source-free compact exterior gives Z=0 or exponentially bounded hair", "FORMAL_REQUIREMENT_WRITTEN_NUMERIC_OR_PARENT_PROOF_MISSING"),
        ("FPG4115_4_source_coupling", "J_Z=0 or source-backed coupling coefficient below local bounds", "Euler equations do not re-source Z around ordinary matter", "HARD_BLOCK_REMAINS_COUPLING_NOT_DERIVED"),
        ("FPG4115_5_boundary", "boundary terms have zero/fixed linked-surface force and Hamiltonian mass handoff retained", "bulk q_loc silence does not leak through alpha3/source-normalization channels", "OPEN_BOUNDARY_HANDOFF_REQUIRED"),
        ("FPG4115_6_verdict", "all fixed point, K_hat=K_metric, Z map, J_Z=0, positive operator and boundary gates pass", "would turn q_loc/T_GK from closure into derived local-GR silence mechanism", "DOUBLE_ZERO_MECHANISM_FOUND_PARENT_OWNERSHIP_MISSING_NO_CLAIM"),
    ]
    return [
        {
            **row_base(),
            "gate_id": gate_id,
            "condition": condition,
            "effect_if_true": effect,
            "status": status,
            "source_id": "SRC4115_05_3628_fixed_point",
            "claim_allowed": bool_string(False),
            "valid_for_claim": bool_string(False),
        }
        for gate_id, condition, effect, status in rows
    ]


def bound_runner_rows() -> List[dict]:
    rows = [
        ("QBR4115_0_RK", "R_K^{mu nu}=K_hat^{mu nu}-K_metric^{mu nu}", "explicit K_metric formulas now available", "MISSING_KHAT_TENSOR_DECOMPOSITION_AND_SYMBOL_MATCH", "score ||R_K|| through PPN/Newton/source-normalization envelope if not zero"),
        ("QBR4115_1_RZ", "R_Z^A=physical local residual vector-Z^A", "even response doublet gives F1=0 only for actual residual coordinates", "MISSING_Z_TO_QLOC_PPN_NEWTON_SOURCE_MAP", "retain q_loc, alpha3, gamma, beta, xi, Gdot and source-mass rows"),
        ("QBR4115_2_JZ", "J_Z source/coupling coefficient", "coupling is now isolated as next hard variable", "MISSING_PARENT_COUPLING_ZERO_OR_NUMERIC_COEFFICIENT", "derive J_Z=0 from quotient/current symmetry or fill numeric coefficient"),
        ("QBR4115_3_flux", "Poynting/wave flux stress", "Maxwell-like scalar density gives legitimate stress-action branch", "MISSING_F_W_J_BOUNDARY_OWNER", "route to EM/charge branch or count as ordinary physical stress"),
        ("QBR4115_4_boundary", "boundary/symplectic flux", "exact/topological route viable only with no-flux or Hamiltonian handoff", "MISSING_BOUNDARY_NO_FLUX_OR_MHREF_HANDOFF", "fill boundary alpha3/source-normalization coefficient products if no theorem-zero"),
    ]
    return [
        {
            **row_base(),
            "row_id": row_id,
            "quantity": quantity,
            "new_reduction": reduction,
            "missing_input": missing,
            "fallback_bound": fallback,
            "status": "BLOCKED_NONCLAIM",
            "source_id": "SRC4115_06_3628_bound_runner",
            "claim_allowed": bool_string(False),
            "valid_for_claim": bool_string(False),
        }
        for row_id, quantity, reduction, missing, fallback in rows
    ]


def decision_rows() -> List[dict]:
    rows = [
        ("DEC4115_0_real_progress", "A real scalar-density mechanism is now in the active spine: an even response-doublet action makes F_1=0 by symmetry, not assertion.", "DERIVATION_PROGRESS_CONDITIONAL", "map Z^A to actual q_loc/PPN/Newton/source residual coordinates"),
        ("DEC4115_1_current_ceiling", "Do not claim local GR or q_loc silence: K_hat=K_metric, Z=physical residual, J_Z=0, positive operator and boundary no-flux remain unsigned.", "NO_CLAIM", "retain R_K, R_Z, J_Z and boundary rows"),
        ("DEC4115_2_poynting", "Poynting/wave intuition is retained as a Maxwell-like action branch where flux is physical stress/current.", "EM_FLUX_BRANCH_RETAINED", "use later for EM/charge/radiation stress mapping, not local-GR zero proof unless flux/current vanish"),
        ("DEC4115_3_next", "The next best target is source coupling: prove J_Z=0 or produce coefficient rows.", "NEXT_TARGET_SELECTED", "4116-Y5-R2FR-response-doublet-source-coupling-zero-or-coefficient.md"),
    ]
    return [
        {
            **row_base(),
            "decision_id": decision_id,
            "decision": decision,
            "status": status,
            "next_action": next_action,
            "claim_allowed": bool_string(False),
            "valid_for_claim": bool_string(False),
        }
        for decision_id, decision, status, next_action in rows
    ]


def next_target_rows() -> List[dict]:
    return [
        {
            **row_base(),
            "next_id": "NEXT4115_0",
            "target_doc": "4116-Y5-R2FR-response-doublet-source-coupling-zero-or-coefficient.md",
            "target_script": "scripts/Y5_R2FR_4116_response_doublet_source_coupling_zero_or_coefficient.py",
            "objective": "attempt to parent-own the response doublet by mapping Z^A to the actual local residual vector and proving J_Z=0; if not, create source-ready coupling coefficient rows for PPN/Newton/R10/clock/orbital bounds",
            "success_gate": "Z^A equals q_loc/PPN/Newton/source residual coordinates, K_hat=K_metric has no remainder or retained R_K row, J_Z is theorem-zero or numeric/source-backed, and boundary flux remains explicit",
            "reason": "4115 found the clean double-zero mechanism; source coupling decides whether it is physics or merely a formal closure.",
            "claim_allowed": bool_string(False),
            "valid_for_claim": bool_string(False),
        }
    ]


def status_rows() -> List[dict]:
    return [
        {
            **row_base(),
            "status_id": "STATUS4115_0",
            "decision": DECISION,
            "strongest_result": "4115 imports the explicit scalar-density construction into the active spine. The even response-doublet action gives a real F_1=0 mechanism by parity, and K_metric formulas are now available for potential, gradient, response-doublet, boundary and flux branches.",
            "what_changed": "The local plateau/double-zero route is no longer a plateau axiom: it has a candidate action mechanism. The remaining bottleneck is whether Z is the actual physical residual and whether J_Z/source coupling vanishes or is bounded.",
            "still_missing": "K_hat=K_metric global match, Z-to-q_loc/PPN/Newton/source map, J_Z=0 or coefficient, positive operator proof, boundary no-flux/H_tau handoff and component projections",
            "claim_state": "no local_GR_PPN_Newton_R10_R11_q_loc_zero_Khat_Kmetric_source_coupling claim",
            "next_target": "4116 response-doublet source coupling zero or coefficient",
            "claim_allowed": bool_string(False),
            "valid_for_claim": bool_string(False),
        }
    ]


def generated_outputs() -> Dict[str, Path]:
    return {
        "P8_Y5_R2FR_4115_SOURCE_REGISTER": SOURCE_DIR / "P8_Y5_R2FR_4115_SOURCE_REGISTER.csv",
        "P8_Y5_R2FR_4115_SCALAR_DENSITY_CANDIDATES": SOURCE_DIR / "P8_Y5_R2FR_4115_SCALAR_DENSITY_CANDIDATES.csv",
        "P8_Y5_R2FR_4115_KMETRIC_KHAT_COMPARISON": SOURCE_DIR / "P8_Y5_R2FR_4115_KMETRIC_KHAT_COMPARISON.csv",
        "P8_Y5_R2FR_4115_DOUBLE_ZERO_MECHANISM": SOURCE_DIR / "P8_Y5_R2FR_4115_DOUBLE_ZERO_MECHANISM.csv",
        "P8_Y5_R2FR_4115_BOUND_RUNNER_ROWS": SOURCE_DIR / "P8_Y5_R2FR_4115_BOUND_RUNNER_ROWS.csv",
        "P8_Y5_R2FR_4115_DECISION_GATE": SOURCE_DIR / "P8_Y5_R2FR_4115_DECISION_GATE.csv",
        "P8_Y5_R2FR_4115_NEXT_TARGET": SOURCE_DIR / "P8_Y5_R2FR_4115_NEXT_TARGET.csv",
        "P8_Y5_R2FR_4115_STATUS": SOURCE_DIR / "P8_Y5_R2FR_4115_STATUS.csv",
    }


def markdown_table(rows: List[dict], columns: List[str]) -> str:
    lines = ["| " + " | ".join(columns) + " |", "| " + " | ".join("---" for _ in columns) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(column, "")).replace("\n", " ") for column in columns) + " |")
    return "\n".join(lines)


def write_doc() -> None:
    status = status_rows()[0]
    lines = [
        "# 4115 - S_GK explicit scalar-density construction or bound runner",
        "",
        "## Verdict",
        "4115 imports the `3628` scalar-density construction into the active `411x` spine. This is a genuine derivation advance: the even response-doublet action supplies a mathematical reason for `F_1=0` by parity, not by plateau assertion.",
        "",
        "No local-GR, PPN, Newton, R10/R11, `q_loc=0`, `K_hat=K_metric`, or source-coupling-zero claim follows yet.",
        "",
        "## Strongest Current Result",
        f"- `{status['decision']}`",
        f"- {status['strongest_result']}",
        f"- {status['what_changed']}",
        "",
        "## Scalar-Density Candidates",
        markdown_table(scalar_density_candidate_rows(), ["candidate_id", "ansatz", "metric_response_formula", "current_status", "interpretation"]),
        "",
        "## K_metric / K_hat Comparison",
        markdown_table(kmetric_comparison_rows(), ["comparison_id", "target_piece", "computed_from_candidate", "residual_if_unmatched", "status"]),
        "",
        "## Double-Zero Mechanism",
        markdown_table(double_zero_mechanism_rows(), ["gate_id", "condition", "effect_if_true", "status"]),
        "",
        "## Bound Runner Rows",
        markdown_table(bound_runner_rows(), ["row_id", "quantity", "new_reduction", "missing_input", "fallback_bound"]),
        "",
        "## Decisions",
        markdown_table(decision_rows(), ["decision_id", "decision", "status", "next_action"]),
        "",
        "## Next Target",
        markdown_table(next_target_rows(), ["target_doc", "target_script", "objective", "success_gate"]),
        "",
    ]
    DOC_PATH.write_text("\n".join(lines), encoding="utf-8")


def write_outputs() -> Dict[str, Path]:
    outputs = generated_outputs()
    write_csv(outputs["P8_Y5_R2FR_4115_SOURCE_REGISTER"], source_register_rows())
    write_csv(outputs["P8_Y5_R2FR_4115_SCALAR_DENSITY_CANDIDATES"], scalar_density_candidate_rows())
    write_csv(outputs["P8_Y5_R2FR_4115_KMETRIC_KHAT_COMPARISON"], kmetric_comparison_rows())
    write_csv(outputs["P8_Y5_R2FR_4115_DOUBLE_ZERO_MECHANISM"], double_zero_mechanism_rows())
    write_csv(outputs["P8_Y5_R2FR_4115_BOUND_RUNNER_ROWS"], bound_runner_rows())
    write_csv(outputs["P8_Y5_R2FR_4115_DECISION_GATE"], decision_rows())
    write_csv(outputs["P8_Y5_R2FR_4115_NEXT_TARGET"], next_target_rows())
    write_csv(outputs["P8_Y5_R2FR_4115_STATUS"], status_rows())
    write_doc()
    return outputs


def validate(outputs: Dict[str, Path]) -> List[dict]:
    checks: List[dict] = []

    def add(check_id: str, check: str, passed: bool, detail: str) -> None:
        checks.append({**row_base(), "check_id": check_id, "check": check, "passed": bool_string(passed), "detail": detail, "claim_allowed": bool_string(False)})

    missing_sources = [source_id for source_id, (path, _, _) in LOCAL_SOURCES.items() if not path.exists()]
    missing_needles = []
    for source_id, (path, needle, _) in LOCAL_SOURCES.items():
        if path.exists() and needle not in read_text(path):
            missing_needles.append(f"{source_id}:{needle}")
    add("VAL4115_0_sources_exist", "every local source path exists", not missing_sources, ";".join(missing_sources) or "all sources exist")
    add("VAL4115_1_sources_contain_needles", "every local source contains expected needle", not missing_needles, ";".join(missing_needles) or "all needles found")

    parse_ok = True
    parse_counts = {}
    for key, path in outputs.items():
        try:
            rows = parse_csv(path)
            parse_counts[key] = len(rows)
            parse_ok = parse_ok and len(rows) > 0
        except Exception as exc:
            parse_ok = False
            parse_counts[key] = repr(exc)
    add("VAL4115_2_csv_parse", "all generated CSV outputs parse and are nonempty", parse_ok, str(parse_counts))

    candidates_text = " ".join(" ".join(row.values()) for row in parse_csv(outputs["P8_Y5_R2FR_4115_SCALAR_DENSITY_CANDIDATES"]))
    candidates_ok = all(token in candidates_text for token in ["even_response_doublet", "F1_ZERO", "wave_flux", "composite"])
    add("VAL4115_3_candidates", "scalar-density candidates include even response and flux branches", candidates_ok, "candidate tokens checked")

    kmetric_text = " ".join(" ".join(row.values()) for row in parse_csv(outputs["P8_Y5_R2FR_4115_KMETRIC_KHAT_COMPARISON"]))
    kmetric_ok = all(token in kmetric_text for token in ["K_metric", "K_hat", "R_K", "KMETRIC_CONSTRUCTED_KHAT_MATCH_NOT_CLAIMED"])
    add("VAL4115_4_kmetric", "K_metric/K_hat comparison retains unmatched residual", kmetric_ok, "Kmetric tokens checked")

    dz_text = " ".join(" ".join(row.values()) for row in parse_csv(outputs["P8_Y5_R2FR_4115_DOUBLE_ZERO_MECHANISM"]))
    dz_ok = all(token in dz_text for token in ["partial_A T_GK", "F1_ZERO_DERIVED", "J_Z=0", "DOUBLE_ZERO_MECHANISM_FOUND"])
    add("VAL4115_5_double_zero", "double-zero mechanism and coupling gate present", dz_ok, "double-zero tokens checked")

    bound_text = " ".join(" ".join(row.values()) for row in parse_csv(outputs["P8_Y5_R2FR_4115_BOUND_RUNNER_ROWS"]))
    bound_ok = all(token in bound_text for token in ["R_K", "R_Z", "J_Z", "boundary/symplectic"])
    add("VAL4115_6_bound_rows", "bound runner rows retain RK/RZ/JZ/boundary branches", bound_ok, "bound tokens checked")

    next_rows = parse_csv(outputs["P8_Y5_R2FR_4115_NEXT_TARGET"])
    next_ok = len(next_rows) == 1 and next_rows[0].get("target_doc") == "4116-Y5-R2FR-response-doublet-source-coupling-zero-or-coefficient.md"
    add("VAL4115_7_next_target", "next target is 4116 response-doublet source coupling", next_ok, str(next_rows))

    status_rows_local = parse_csv(outputs["P8_Y5_R2FR_4115_STATUS"])
    status_ok = bool(status_rows_local) and status_rows_local[0].get("decision") == DECISION and "no local_GR" in status_rows_local[0].get("claim_state", "")
    add("VAL4115_8_status", "status records scalar-density result and no-claim state", status_ok, "status row checked")

    all_rows = []
    for path in outputs.values():
        all_rows.extend(parse_csv(path))
    no_claim = all(row.get("claim_allowed") in ("False", "") for row in all_rows)
    add("VAL4115_9_no_claim_flags", "all generated rows remain no-claim", no_claim, f"row_count={len(all_rows)}")

    output_paths = list(outputs.values()) + [DOC_PATH]
    in_scope = all(is_under(path, ROOT) for path in output_paths)
    formalization_output = any(is_under(path, FORMALIZATION) for path in output_paths)
    formalization_touched = False
    if FORMALIZATION.exists():
        formalization_touched = any(FORMALIZATION.rglob("*R2FR_4115*")) or any(FORMALIZATION.rglob("4115-Y5-R2FR*"))
    add("VAL4115_10_scope", "outputs stay in post-checkpoint-work and not formalization-workbench", in_scope and not formalization_output and not formalization_touched, f"doc={DOC_PATH}; csv_count={len(outputs)}")

    compile_ok = True
    compile_detail = "py_compile ok"
    try:
        py_compile.compile(str(SCRIPT_PATH), doraise=True)
    except Exception as exc:
        compile_ok = False
        compile_detail = repr(exc)
    add("VAL4115_11_compile", "generator script compiles", compile_ok, compile_detail)
    return checks


def main() -> None:
    outputs = write_outputs()
    validation_rows = validate(outputs)
    validation_path = SOURCE_DIR / "P8_Y5_BRR545_4115_VALIDATION.csv"
    write_csv(validation_path, validation_rows)
    pycache = SCRIPT_PATH.parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)

    failed = [row for row in validation_rows if row["passed"] != "True"]
    print(f"wrote: {DOC_PATH}")
    for path in outputs.values():
        print(f"wrote: {path}")
    print(f"validation: {validation_path}")
    if failed:
        print("failed checks:")
        for row in failed:
            print(f"- {row['check_id']}: {row['detail']}")
        raise SystemExit(1)
    print("all validation checks passed")


if __name__ == "__main__":
    main()
