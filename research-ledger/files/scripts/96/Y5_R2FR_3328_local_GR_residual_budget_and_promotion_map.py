from __future__ import annotations

import csv
import hashlib
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
FW = REPO / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
PYCACHE = ROOT / "scripts" / "__pycache__"

DOC = ROOT / "3328-Y5-R2FR-local-GR-residual-budget-and-promotion-map-under-AX1090.md"

SOURCES = [
    {
        "source_id": "SRC3328_0_3318_Gamma",
        "path": ROOT / "3318-Y5-R2FR-Gamma-extra-sector-nonpropagation-proof-or-Bi-envelope-under-AX1090.md",
        "role": "Gamma extra-sector local nonpropagation/readout branch",
    },
    {
        "source_id": "SRC3328_1_3319_psi",
        "path": ROOT / "3319-Y5-R2FR-psi-coarse-graining-no-finite-public-residue-or-Bi-bound-under-AX1090.md",
        "role": "psi public readout split and tree residue route",
    },
    {
        "source_id": "SRC3328_2_3321_epsilon",
        "path": ROOT / "3321-Y5-R2FR-smoothing-kernel-scale-separation-bound-for-epsilon-grad-under-AX1090.md",
        "role": "epsilon_grad smoothing transfer and threshold rows",
    },
    {
        "source_id": "SRC3328_3_3322_Ci",
        "path": ROOT / "3322-Y5-R2FR-Ci-projection-and-composite-contact-tail-gate-for-epsilon-grad-under-AX1090.md",
        "role": "C_i operator response and arena threshold formulas",
    },
    {
        "source_id": "SRC3328_4_3324_closure",
        "path": ROOT / "3324-Y5-R2FR-induced-EH-coefficient-or-measured-G-closure-local-GR-theorem-under-AX1090.md",
        "role": "measured-G local GR/Newton/Maxwell closure theorem",
    },
    {
        "source_id": "SRC3328_5_3325_matter",
        "path": ROOT / "3325-Y5-R2FR-universal-matter-no-direct-psi-vertex-and-no-tadpole-signature-gate-under-AX1090.md",
        "role": "macroscopic universal matter and EM stress signature",
    },
    {
        "source_id": "SRC3328_6_3327_composite",
        "path": ROOT / "3327-Y5-R2FR-parent-local-fluctuation-measure-or-numeric-composite-envelope-under-AX1090.md",
        "role": "CLT/mixing composite envelope and required numeric inputs",
    },
    {
        "source_id": "SRC3328_7_3324_theorem_csv",
        "path": OUT / "P8_Y5_R2FR_3324_MEASURED_G_CLOSURE_THEOREM.csv",
        "role": "closure theorem rows",
    },
    {
        "source_id": "SRC3328_8_3322_thresholds_csv",
        "path": OUT / "P8_Y5_R2FR_3322_ARENA_THRESHOLD_FORMULAS.csv",
        "role": "arena residual threshold formulas",
    },
    {
        "source_id": "SRC3328_9_3327_inputs_csv",
        "path": OUT / "P8_Y5_R2FR_3327_REQUIRED_NUMERIC_INPUTS.csv",
        "role": "composite-envelope numeric inputs",
    },
    {
        "source_id": "SRC3328_10_3327_envelope_csv",
        "path": OUT / "P8_Y5_R2FR_3327_COMPOSITE_ENVELOPE.csv",
        "role": "composite residual envelope",
    },
]

OUTPUTS = {
    "sources": OUT / "P8_Y5_R2FR_3328_SOURCE_REGISTER.csv",
    "components": OUT / "P8_Y5_R2FR_3328_LOCAL_BRANCH_COMPONENT_STATUS.csv",
    "budget": OUT / "P8_Y5_R2FR_3328_RESIDUAL_BUDGET_FORMULAS.csv",
    "arena": OUT / "P8_Y5_R2FR_3328_ARENA_PROMOTION_MAP.csv",
    "inputs": OUT / "P8_Y5_R2FR_3328_REQUIRED_INPUT_LEDGER.csv",
    "claims": OUT / "P8_Y5_R2FR_3328_CLAIM_STATUS_LEDGER.csv",
    "scorecard": OUT / "P8_Y5_R2FR_3328_LOCAL_BRANCH_SCORECARD.csv",
    "next": OUT / "P8_Y5_R2FR_3328_NEXT_TARGET.csv",
    "validation": OUT / "P8_Y5_BRR545_3328_VALIDATION.csv",
}

RUN_UTC = datetime.now(timezone.utc).isoformat()


def bool_str(value: bool) -> str:
    return "true" if value else "false"


def compact(value: Any, limit: int = 1400) -> str:
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


def component_status_rows() -> list[dict[str, Any]]:
    return [
        {
            "component_id": "COMP3328_0_measured_G_closure",
            "component": "measured-G local GR closure",
            "status": "CONDITIONAL_PASS",
            "signed_piece": "3324 formalizes local GR/Newton/Maxwell with measured G_N",
            "remaining_gap": "not a derivation of G; induced C_EH still future work",
            "budget_symbol": "epsilon_G_closure=0 if measured-G closure is declared",
            "valid_for_claim": "false",
        },
        {
            "component_id": "COMP3328_1_Newton_Poisson",
            "component": "Newton/Poisson weak-field limit",
            "status": "CONDITIONAL_PASS",
            "signed_piece": "3324 derives nabla^2 Phi = 4 pi G_N rho plus bounded residual",
            "remaining_gap": "requires residual budget below Newton/PPN/orbital thresholds",
            "budget_symbol": "epsilon_Newton_i",
            "valid_for_claim": "false",
        },
        {
            "component_id": "COMP3328_2_matter_EM_source",
            "component": "macroscopic matter and EM stress coupling",
            "status": "MACRO_SIGNED_CONDITIONAL",
            "signed_piece": "3325 signs standard metric L_matter and Maxwell/Poynting as T_munu^EM route",
            "remaining_gap": "microscopic matter descent from psi not derived; direct psi vertices must remain excluded",
            "budget_symbol": "epsilon_direct_i=0 only under Delta S_direct=0",
            "valid_for_claim": "false",
        },
        {
            "component_id": "COMP3328_3_Gamma_local",
            "component": "Gamma/local saturation residue",
            "status": "CONDITIONAL_OR_BOUND",
            "signed_piece": "3318/3324 route treats local Gamma/saturation as silent or residual-bounded",
            "remaining_gap": "must keep explicit R_Gamma_i unless parent local silence is signed for each arena",
            "budget_symbol": "R_Gamma_i",
            "valid_for_claim": "false",
        },
        {
            "component_id": "COMP3328_4_psi_tree",
            "component": "psi tree first-gradient residue",
            "status": "BOUNDED_CONDITIONAL",
            "signed_piece": "3319-3321 give first-gradient silence theorem and Gaussian T_grad transfer",
            "remaining_gap": "epsilon_bg, ell_s, boundary/aniso leakage, and local gradient scale not numeric",
            "budget_symbol": "C_i epsilon_eff_i^2",
            "valid_for_claim": "false",
        },
        {
            "component_id": "COMP3328_5_Ci_response",
            "component": "C_i projection/propagator/source response",
            "status": "FORMULA_READY_NOT_NUMERIC",
            "signed_piece": "3322 decomposes C_i into arena projection, propagator norm, and source normalization",
            "remaining_gap": "C_PPN, C_R10, C_WEP, C_clock, C_orb not source/numeric bounded",
            "budget_symbol": "C_i(lambda,S,H_pi)",
            "valid_for_claim": "false",
        },
        {
            "component_id": "COMP3328_6_composite",
            "component": "composite/tadpole/contact tail",
            "status": "ENVELOPE_READY_NOT_NUMERIC",
            "signed_piece": "3326-3327 give centered split, CLT skew suppression, and total epsilon_composite envelope",
            "remaining_gap": "ell_c, C_mix, C3, bias, rho_P1, spectral gap, contact/boundary/aniso bounds missing",
            "budget_symbol": "epsilon_composite_i",
            "valid_for_claim": "false",
        },
        {
            "component_id": "COMP3328_7_arena_data_bounds",
            "component": "PPN/R10/WEP/clock/orbital empirical thresholds",
            "status": "ROUTED_NOT_CLAIM_READY",
            "signed_piece": "3321/3322 define threshold formulas by arena",
            "remaining_gap": "claim-ready numeric threshold curves and response coefficients are not assembled",
            "budget_symbol": "B_i^max",
            "valid_for_claim": "false",
        },
    ]


def residual_budget_rows() -> list[dict[str, Any]]:
    return [
        {
            "budget_id": "BUD3328_0_master",
            "formula": "R_i^local <= |R_Gamma_i| + C_i(lambda) epsilon_eff_i(lambda)^2 + epsilon_composite_i(lambda) + epsilon_direct_i + epsilon_G_closure_i",
            "meaning": "master no-cancellation local residual budget for each arena i",
            "claim_gate": "must satisfy R_i^local <= B_i^max for every claimed arena",
            "valid_for_claim": "false",
        },
        {
            "budget_id": "BUD3328_1_epsilon_eff",
            "formula": "epsilon_eff_i(lambda)=epsilon_bg_i T_grad(lambda)+epsilon_boundary_i+epsilon_kernel_aniso_i",
            "meaning": "first-gradient leakage after smoothing and local patch defects",
            "claim_gate": "requires epsilon_bg_i, ell_s, lambda, boundary, and anisotropy bounds",
            "valid_for_claim": "false",
        },
        {
            "budget_id": "BUD3328_2_T_grad",
            "formula": "T_grad(lambda)=(ell_s/lambda) exp[-ell_s^2/(2 lambda^2)]",
            "meaning": "3321 Gaussian smoothing transfer law",
            "claim_gate": "requires parent/phenomenological ell_s and arena lambda convention",
            "valid_for_claim": "false",
        },
        {
            "budget_id": "BUD3328_3_Ci",
            "formula": "C_i=||Pi_i W_i||^2 ||D S_ell H_pi S_ell^dagger D^dagger|| x source_normalization_i",
            "meaning": "3322 response coefficient",
            "claim_gate": "requires arena projection, propagator, and source normalization bounds",
            "valid_for_claim": "false",
        },
        {
            "budget_id": "BUD3328_4_composite",
            "formula": "epsilon_composite_i <= epsilon_1p_i + epsilon_2p_i(lambda) + epsilon_contact_i + epsilon_boundary_i + epsilon_kernel_aniso_i",
            "meaning": "3327 composite envelope",
            "claim_gate": "requires CLT/mixing and spectral/contact inputs",
            "valid_for_claim": "false",
        },
        {
            "budget_id": "BUD3328_5_one_particle_composite",
            "formula": "epsilon_1p_i <= A_i delta_mean_i sigma_Dpi_i + B_i (C3_i/sqrt(N_eff_i)+delta_bias_i) sigma_Dpi_i^2 + rho_P1_i Q2_norm_i",
            "meaning": "one-particle composite leakage after exact mean-centering and CLT skew suppression",
            "claim_gate": "requires delta_mean_i=0 or bound, N_eff_i, C3_i, bias, projection leakage, and Q2 norm",
            "valid_for_claim": "false",
        },
        {
            "budget_id": "BUD3328_6_G_closure",
            "formula": "epsilon_G_closure_i=0 only for declared measured-G closure; deriving G requires numeric C_EH^ind",
            "meaning": "separates GR-equivalence from deeper Newton-constant derivation",
            "claim_gate": "public text must not claim G is derived unless C_EH is computed",
            "valid_for_claim": "false",
        },
        {
            "budget_id": "BUD3328_7_direct_vertex",
            "formula": "epsilon_direct_i=0 only if Delta S_direct[psi,matter,EM]=0",
            "meaning": "direct psi-matter/psi-EM/Poynting vertices are excluded from clean local branch",
            "claim_gate": "any direct vertex must be bounded separately",
            "valid_for_claim": "false",
        },
    ]


def arena_promotion_rows() -> list[dict[str, Any]]:
    return [
        {
            "arena": "PPN_local_GR",
            "residual_test": "|gamma-1|, |beta-1|, preferred-frame residuals",
            "budget_formula": "R_PPN <= |R_Gamma_PPN| + C_PPN epsilon_eff^2 + epsilon_composite_PPN + epsilon_direct_PPN",
            "current_status": "CONDITIONAL_NOT_CLAIM_READY",
            "blocking_inputs": "C_PPN, epsilon_eff, epsilon_composite_PPN, R_Gamma_PPN, PPN threshold table",
            "valid_for_claim": "false",
        },
        {
            "arena": "orbital_Newton",
            "residual_test": "delta a/a_Newton or anomalous precession/orbital residual",
            "budget_formula": "R_orb <= |R_Gamma_orb| + C_orb epsilon_eff^2 + epsilon_composite_orb",
            "current_status": "CONDITIONAL_NOT_CLAIM_READY",
            "blocking_inputs": "C_orb, compact-source projection, orbital threshold values, contact absorption",
            "valid_for_claim": "false",
        },
        {
            "arena": "R10_short_range",
            "residual_test": "alpha_psi(lambda) against alpha_bound(lambda)",
            "budget_formula": "alpha_psi(lambda) <= |R_Gamma_R10| + C_R10(lambda) epsilon_eff(lambda)^2 + epsilon_composite_R10(lambda)",
            "current_status": "CONDITIONAL_NOT_CLAIM_READY",
            "blocking_inputs": "claim-ready alpha_bound curve, C_R10(lambda), contact/source-size routing, two-pi gap/contact bounds",
            "valid_for_claim": "false",
        },
        {
            "arena": "WEP",
            "residual_test": "eta_AB composition dependence",
            "budget_formula": "eta_AB <= |R_Gamma_WEP| + C_WEP epsilon_eff^2 |Delta q_AB| + epsilon_composite_WEP + epsilon_direct_WEP",
            "current_status": "CONDITIONAL_NOT_CLAIM_READY",
            "blocking_inputs": "material response Delta q_AB, direct vertex exclusion, anisotropy/contact bounds",
            "valid_for_claim": "false",
        },
        {
            "arena": "clocks_EM_Poynting",
            "residual_test": "clock shifts, optical/EM propagation, Poynting/stress residual",
            "budget_formula": "R_clock <= |R_Gamma_clock| + C_clock epsilon_eff^2 + epsilon_EM_composite_tail + epsilon_direct_EM",
            "current_status": "CONDITIONAL_NOT_CLAIM_READY",
            "blocking_inputs": "Maxwell stress projection, direct psi-EM exclusion, clock normalization, EM tail bounds",
            "valid_for_claim": "false",
        },
    ]


def required_input_rows() -> list[dict[str, Any]]:
    return [
        {
            "input_id": "REQ3328_0_CEH_or_closure",
            "quantity": "measured-G closure declaration or C_EH^ind",
            "needed_for": "separating local GR reduction from derivation of G",
            "status": "CLOSURE_READY_CEH_MISSING",
            "priority": "high",
            "valid_for_claim": "false",
        },
        {
            "input_id": "REQ3328_1_smoothing",
            "quantity": "ell_s, epsilon_bg_i, lambda convention",
            "needed_for": "T_grad and epsilon_eff",
            "status": "MISSING_NUMERIC",
            "priority": "high",
            "valid_for_claim": "false",
        },
        {
            "input_id": "REQ3328_2_Ci",
            "quantity": "C_PPN, C_R10, C_WEP, C_clock, C_orb",
            "needed_for": "arena response coefficients",
            "status": "MISSING_NUMERIC_OR_BOUND",
            "priority": "high",
            "valid_for_claim": "false",
        },
        {
            "input_id": "REQ3328_3_composite",
            "quantity": "ell_c, C_mix, d_eff, C3, delta_bias, rho_P1, dmu_2, m_gap_2pi, contact/boundary/aniso",
            "needed_for": "epsilon_composite_i",
            "status": "MISSING_NUMERIC_OR_PARENT_BOUND",
            "priority": "high",
            "valid_for_claim": "false",
        },
        {
            "input_id": "REQ3328_4_Gamma",
            "quantity": "R_Gamma_i or parent local Gamma silence",
            "needed_for": "local Gamma/saturation residual",
            "status": "MISSING_ARENA_BOUND",
            "priority": "medium",
            "valid_for_claim": "false",
        },
        {
            "input_id": "REQ3328_5_direct",
            "quantity": "Delta S_direct=0 proof or direct vertex bounds",
            "needed_for": "WEP/clock/EM local safety",
            "status": "BRANCH_EXCLUSION_READY_MICRO_PROOF_MISSING",
            "priority": "medium",
            "valid_for_claim": "false",
        },
        {
            "input_id": "REQ3328_6_data",
            "quantity": "PPN, R10 alpha(lambda), WEP, clock, orbital threshold tables",
            "needed_for": "arena pass/fail comparisons",
            "status": "MISSING_CLAIM_READY_TABLES",
            "priority": "medium",
            "valid_for_claim": "false",
        },
    ]


def claim_status_rows() -> list[dict[str, Any]]:
    return [
        {
            "claim_id": "CLAIM3328_0_measured_G_local_GR",
            "claim": "MTS has a conditional measured-G route to local GR/Newton/Maxwell",
            "status": "INTERNAL_CONDITIONAL_SUPPORTED",
            "allowed_wording": "conditional local-GR closure theorem, not public pass",
            "forbidden_wording": "MTS has fully proved local GR or derived G",
            "valid_for_claim": "false",
        },
        {
            "claim_id": "CLAIM3328_1_derive_G",
            "claim": "MTS derives Newton's constant",
            "status": "NO",
            "allowed_wording": "future induced C_EH route",
            "forbidden_wording": "G is derived from current gamma/lambda/kappa equations",
            "valid_for_claim": "false",
        },
        {
            "claim_id": "CLAIM3328_2_Newton_limit",
            "claim": "Newton/Poisson limit is recovered",
            "status": "CONDITIONAL",
            "allowed_wording": "recovered under measured-G closure and bounded local residuals",
            "forbidden_wording": "unconditional Newton pass",
            "valid_for_claim": "false",
        },
        {
            "claim_id": "CLAIM3328_3_Maxwell_EM",
            "claim": "Maxwell/EM stress is compatible with local branch",
            "status": "CONDITIONAL",
            "allowed_wording": "EM/Poynting routed through metric T_munu under no direct psi-EM vertices",
            "forbidden_wording": "MTS derives/unifies Maxwell",
            "valid_for_claim": "false",
        },
        {
            "claim_id": "CLAIM3328_4_local_tests",
            "claim": "PPN/R10/WEP/clock/orbital tests pass",
            "status": "NO_CLAIM",
            "allowed_wording": "budget formulas and required inputs are ready",
            "forbidden_wording": "local tests passed",
            "valid_for_claim": "false",
        },
    ]


def scorecard_rows() -> list[dict[str, Any]]:
    return [
        {
            "score_id": "SCORE3328_0_formal_structure",
            "item": "local branch formal structure",
            "grade": "strong conditional",
            "reason": "measured-G closure, Poisson theorem, matter signature, smoothing tree bound, and composite envelope are assembled",
            "next_action": "turn symbolic budget into arena-specific numeric/bounded rows",
            "valid_for_claim": "false",
        },
        {
            "score_id": "SCORE3328_1_derivation_depth",
            "item": "derivation depth",
            "grade": "mixed",
            "reason": "several pieces are derived conditionally, but induced G, microscopic matter descent, C_i numerics, and composite inputs remain open",
            "next_action": "prioritize C_i/epsilon_composite numeric envelopes before public claims",
            "valid_for_claim": "false",
        },
        {
            "score_id": "SCORE3328_2_empirical_readiness",
            "item": "empirical readiness",
            "grade": "not ready",
            "reason": "test formulas exist but thresholds/coefficients are not populated",
            "next_action": "make an arena-by-arena numeric input matrix",
            "valid_for_claim": "false",
        },
        {
            "score_id": "SCORE3328_3_public_safety",
            "item": "public safety",
            "grade": "private only",
            "reason": "safe as internal discipline; public wording would need strong caveats",
            "next_action": "keep in post-checkpoint until at least one local arena budget is populated",
            "valid_for_claim": "false",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "target_doc": "3329-Y5-R2FR-local-residual-budget-input-prioritizer-and-minimal-numeric-smoke-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3329_local_residual_budget_input_prioritizer_and_minimal_numeric_smoke.py",
            "objective": "choose the smallest local arena/numeric route that can stress-test the 3328 residual budget, prioritizing PPN or R10 with conservative symbolic-to-numeric placeholders kept nonclaim",
            "must_include": "input priority table; one minimal arena; no-claim smoke numbers; sensitivity to C_i and epsilon_composite; pass/fail conditions; no public claim",
            "fallback_if_failed": "keep 3328 as the complete local residual-budget checklist and return to deriving missing coefficients",
            "valid_for_claim": "false",
        }
    ]


def validate_outputs(formalization_before: dict[str, tuple[int, int]]) -> list[dict[str, Any]]:
    sources = source_register_rows()
    components = component_status_rows()
    budgets = residual_budget_rows()
    arenas = arena_promotion_rows()
    required = required_input_rows()
    claims = claim_status_rows()
    scorecard = scorecard_rows()
    gates_false = [row for row in claims if row["status"] in {"NO", "NO_CLAIM"}]
    output_paths = [path for key, path in OUTPUTS.items() if key != "validation"]
    fw_changed = changed_count(formalization_before, snapshot_tree(FW))
    checks = [
        {
            "check_id": "VAL3328_0_sources_exist",
            "check": "all cited source paths exist",
            "passed": all(row["exists"] == "true" for row in sources),
            "detail": "",
        },
        {
            "check_id": "VAL3328_1_sources_parse",
            "check": "all cited source paths parse",
            "passed": all(row["parse_ok"] == "true" for row in sources),
            "detail": "",
        },
        {
            "check_id": "VAL3328_2_outputs_parse",
            "check": "all 3328 non-validation outputs parse",
            "passed": all(path.exists() and parse_ok(path) for path in output_paths),
            "detail": "",
        },
        {
            "check_id": "VAL3328_3_components_complete",
            "check": "component status includes closure, Newton, matter, Gamma, psi tree, C_i, composite, arena data",
            "passed": {"COMP3328_0_measured_G_closure", "COMP3328_1_Newton_Poisson", "COMP3328_2_matter_EM_source", "COMP3328_3_Gamma_local", "COMP3328_4_psi_tree", "COMP3328_5_Ci_response", "COMP3328_6_composite", "COMP3328_7_arena_data_bounds"}.issubset(
                {row["component_id"] for row in components}
            ),
            "detail": "",
        },
        {
            "check_id": "VAL3328_4_master_budget",
            "check": "master residual budget includes R_Gamma, C_i epsilon_eff, epsilon_composite, direct vertex, and G closure",
            "passed": any(
                "R_Gamma_i" in row["formula"]
                and "C_i" in row["formula"]
                and "epsilon_composite_i" in row["formula"]
                and "epsilon_direct_i" in row["formula"]
                and "epsilon_G_closure_i" in row["formula"]
                for row in budgets
            ),
            "detail": "",
        },
        {
            "check_id": "VAL3328_5_arena_map",
            "check": "arena map includes PPN, orbital, R10, WEP, and clocks/EM",
            "passed": {"PPN_local_GR", "orbital_Newton", "R10_short_range", "WEP", "clocks_EM_Poynting"}.issubset(
                {row["arena"] for row in arenas}
            ),
            "detail": "",
        },
        {
            "check_id": "VAL3328_6_required_inputs",
            "check": "required input ledger includes closure, smoothing, C_i, composite, Gamma, direct, data",
            "passed": {"REQ3328_0_CEH_or_closure", "REQ3328_1_smoothing", "REQ3328_2_Ci", "REQ3328_3_composite", "REQ3328_4_Gamma", "REQ3328_5_direct", "REQ3328_6_data"}.issubset(
                {row["input_id"] for row in required}
            ),
            "detail": "",
        },
        {
            "check_id": "VAL3328_7_no_public_claim",
            "check": "claim ledger rejects derived G and local test pass",
            "passed": any(row["claim_id"] == "CLAIM3328_1_derive_G" and row["status"] == "NO" for row in claims)
            and any(row["claim_id"] == "CLAIM3328_4_local_tests" and row["status"] == "NO_CLAIM" for row in claims)
            and all(row["valid_for_claim"] == "false" for row in gates_false),
            "detail": "",
        },
        {
            "check_id": "VAL3328_8_scorecard_private",
            "check": "scorecard exists and public safety remains private only",
            "passed": any(row["score_id"] == "SCORE3328_3_public_safety" and row["grade"] == "private only" for row in scorecard),
            "detail": "",
        },
        {
            "check_id": "VAL3328_9_next_numeric_smoke",
            "check": "next target is local input prioritizer/minimal numeric smoke",
            "passed": any("numeric" in row["objective"] and "no-claim" in row["must_include"] for row in next_target_rows()),
            "detail": "",
        },
        {
            "check_id": "VAL3328_10_formalization_untouched",
            "check": "formalization-workbench modified-file count remains zero by this script",
            "passed": fw_changed == 0,
            "detail": f"formalization_changed_count={fw_changed}",
        },
    ]
    overall = all(bool(check["passed"]) for check in checks)
    checks.append(
        {
            "check_id": "VAL3328_11_overall",
            "check": "3328 validation overall",
            "passed": overall,
            "detail": "all required checks passed" if overall else "one or more checks failed",
        }
    )
    for check in checks:
        check["passed"] = bool_str(bool(check["passed"]))
    return checks


def render_doc() -> str:
    lines: list[str] = [
        "# 3328 - Local-GR residual budget and promotion map under AX1090",
        "",
        f"Run UTC: `{RUN_UTC}`",
        "",
        "## Verdict",
        "",
        "3328 assembles the local branch into one scorecard.",
        "",
        "The branch is now structurally coherent as a **conditional measured-G local-GR closure theorem**, not an unconditional proof and not a derivation of `G`.",
        "",
        "For each local arena `i`, the no-cancellation residual budget is",
        "",
        "`R_i^local <= |R_Gamma_i| + C_i(lambda) epsilon_eff_i(lambda)^2 + epsilon_composite_i(lambda) + epsilon_direct_i + epsilon_G_closure_i`,",
        "",
        "where",
        "",
        "`epsilon_eff_i(lambda)=epsilon_bg_i T_grad(lambda)+epsilon_boundary_i+epsilon_kernel_aniso_i`,",
        "",
        "and",
        "",
        "`epsilon_composite_i <= epsilon_1p_i + epsilon_2p_i(lambda) + epsilon_contact_i + epsilon_boundary_i + epsilon_kernel_aniso_i`.",
        "",
        "This is progress: the local branch has moved from loose narrative to an inspectable residual budget. But no PPN/R10/WEP/clock/orbital pass is claimed. The missing step is numeric or source-backed bounds for `C_i`, `epsilon_eff`, `epsilon_composite`, local `Gamma` leakage, and arena thresholds.",
        "",
        "## Source Register",
        "",
    ]
    for row in source_register_rows():
        lines.append(
            f"- `{row['source_id']}`: `{row['path']}` exists={row['exists']} parse_ok={row['parse_ok']} role={row['role']}"
        )
    sections = [
        ("Local Branch Component Status", component_status_rows(), "component_id"),
        ("Residual Budget Formulas", residual_budget_rows(), "budget_id"),
        ("Arena Promotion Map", arena_promotion_rows(), "arena"),
        ("Required Input Ledger", required_input_rows(), "input_id"),
        ("Claim Status Ledger", claim_status_rows(), "claim_id"),
        ("Local Branch Scorecard", scorecard_rows(), "score_id"),
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
            "- It is a branch-level scorecard, not a public theorem.",
            "- It explicitly rejects claims that `G` is derived or that local tests already pass.",
            "- It gives one complete residual formula that can now be populated arena by arena.",
            "- `formalization-workbench` is not modified.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> None:
    formalization_before = snapshot_tree(FW)
    OUT.mkdir(parents=True, exist_ok=True)
    write_csv(OUTPUTS["sources"], source_register_rows())
    write_csv(OUTPUTS["components"], component_status_rows())
    write_csv(OUTPUTS["budget"], residual_budget_rows())
    write_csv(OUTPUTS["arena"], arena_promotion_rows())
    write_csv(OUTPUTS["inputs"], required_input_rows())
    write_csv(OUTPUTS["claims"], claim_status_rows())
    write_csv(OUTPUTS["scorecard"], scorecard_rows())
    write_csv(OUTPUTS["next"], next_target_rows())
    DOC.write_text(render_doc(), encoding="utf-8")
    write_csv(OUTPUTS["validation"], validate_outputs(formalization_before))
    if PYCACHE.exists():
        shutil.rmtree(PYCACHE)


if __name__ == "__main__":
    main()
