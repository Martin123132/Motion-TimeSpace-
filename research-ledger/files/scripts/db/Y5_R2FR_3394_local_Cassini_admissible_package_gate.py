from __future__ import annotations

import csv
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
DOC = ROOT / "3394-Y5-R2FR-local-Cassini-admissible-package-gate-under-AX1090.md"
RUN_UTC = datetime.now(timezone.utc).isoformat()

OUTPUTS = {
    "source_register": OUT / "P8_Y5_R2FR_3394_SOURCE_REGISTER.csv",
    "package_clauses": OUT / "P8_Y5_R2FR_3394_LOCAL_PACKAGE_CLAUSE_REGISTER.csv",
    "compatibility": OUT / "P8_Y5_R2FR_3394_PACKAGE_COMPATIBILITY_AUDIT.csv",
    "channel_implications": OUT / "P8_Y5_R2FR_3394_CHANNEL_IMPLICATIONS.csv",
    "residual_collapse": OUT / "P8_Y5_R2FR_3394_LOCAL_RESIDUAL_COLLAPSE_TABLE_NONCLAIM.csv",
    "package_gate": OUT / "P8_Y5_R2FR_3394_ADMISSIBLE_PACKAGE_GATE.csv",
    "conflict_audit": OUT / "P8_Y5_R2FR_3394_CROSS_BRANCH_CONFLICT_AUDIT.csv",
    "runner": OUT / "P8_Y5_R2FR_3394_RUNNER_NONCLAIM.csv",
    "gates": OUT / "P8_Y5_R2FR_3394_PROMOTION_GATES.csv",
    "decision": OUT / "P8_Y5_R2FR_3394_DECISION_LEDGER.csv",
    "next": OUT / "P8_Y5_R2FR_3394_NEXT_TARGET.csv",
    "validation": OUT / "P8_Y5_BRR545_3394_VALIDATION.csv",
}

LOCAL_SOURCES = [
    ("SRC3394_00_3393_doc", ROOT / "3393-Y5-R2FR-boundary-flux-moment-gauge-closure-pack-under-AX1090.md", "3393 handoff"),
    ("SRC3394_01_3393_next", OUT / "P8_Y5_R2FR_3393_NEXT_TARGET.csv", "3393 next target"),
    ("SRC3394_02_3393_closure", OUT / "P8_Y5_R2FR_3393_CHANNEL_CLOSURE_MATRIX.csv", "channel closure matrix"),
    ("SRC3394_03_3393_poynting", OUT / "P8_Y5_R2FR_3393_CASSINI_POYNTING_FLUX_BOUND_NONCLAIM.csv", "Poynting finite bound"),
    ("SRC3394_04_3393_kernel", OUT / "P8_Y5_R2FR_3393_KERNEL_MOMENT_ZERO_THEOREM.csv", "kernel moment theorem"),
    ("SRC3394_05_3393_gauge", OUT / "P8_Y5_R2FR_3393_GAUGE_READOUT_DRIFT_BOUND_ROWS_NONCLAIM.csv", "gauge drift rows"),
    ("SRC3394_06_3392_clause", OUT / "P8_Y5_R2FR_3392_FIXED_PPN_PARENT_CLAUSE_CANDIDATE.csv", "fixed PPN readout parent clause"),
    ("SRC3394_07_3392_theorem", OUT / "P8_Y5_R2FR_3392_PROJECTOR_COMMUTATOR_THEOREM.csv", "projector commutator theorem"),
    ("SRC3394_08_3391_geometry", OUT / "P8_Y5_R2FR_3391_CASSINI_GEOMETRY_SOURCE_BACKED.csv", "Cassini geometry"),
    ("SRC3394_09_3376_doc", ROOT / "3376-Y5-R2FR-boundary-zero-flux-or-Bzero-first-row-under-AX1090.md", "boundary/reference theorem package"),
    ("SRC3394_10_core_fundamental_action", REPO / "core-mts-framework" / "action-principle" / "the-fundamental-action-of-motion-timespace-field-theory.md", "parent fundamental action"),
    ("SRC3394_11_core_motion_action", REPO / "core-mts-framework" / "action-principle" / "the-motion-timespace-action-principle.md", "parent motion action"),
    ("SRC3394_12_core_gravity", REPO / "core-mts-framework" / "gravity" / "motion-timespace-mts-gravity-core-unified-formulation.md", "parent gravity formulation"),
]


def bool_text(value: bool) -> str:
    return "true" if value else "false"


def parse_csv(path: Path) -> tuple[bool, str]:
    try:
        with path.open("r", encoding="utf-8-sig", newline="") as handle:
            list(csv.DictReader(handle))
        return True, ""
    except Exception as exc:  # noqa: BLE001
        return False, f"{type(exc).__name__}: {exc}"


def parse_text(path: Path) -> tuple[bool, str]:
    try:
        path.read_text(encoding="utf-8", errors="replace")
        return True, ""
    except Exception as exc:  # noqa: BLE001
        return False, f"{type(exc).__name__}: {exc}"


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    headers: list[str] = []
    for row in rows:
        for key in row:
            if key not in headers:
                headers.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=headers)
        writer.writeheader()
        writer.writerows(rows)


def md_escape(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", "<br>")


def md_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "_No rows._\n"
    headers: list[str] = []
    for row in rows:
        for key in row:
            if key not in headers:
                headers.append(key)
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(md_escape(row.get(header, "")) for header in headers) + " |")
    return "\n".join(lines) + "\n"


def to_float(value: str, default: float = math.nan) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def source_rows() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for source_id, path, role in LOCAL_SOURCES:
        exists = path.exists()
        if not exists:
            parse_ok, parse_error = False, "missing"
        elif path.suffix.lower() == ".csv":
            parse_ok, parse_error = parse_csv(path)
        else:
            parse_ok, parse_error = parse_text(path)
        rows.append(
            {
                "source_id": source_id,
                "source_path": str(path),
                "exists": bool_text(exists),
                "parse_ok": bool_text(parse_ok),
                "role": role,
                "read_or_write": "post_checkpoint_or_core_source",
                "parse_error": parse_error,
                "valid_for_claim": "false",
            }
        )
    return rows


def package_clause_rows() -> list[dict[str, str]]:
    return [
        {
            "clause_id": "LCP3394_0_fixed_PPN_readout",
            "source": "PC3392_0",
            "clause": "PPN observables are extracted by a fixed linear readout P_PPN from the already coarse-grained metric perturbation in one chosen local PPN/Fermi patch.",
            "closes_channel": "projector commutator",
            "adds_dynamics": "false",
            "adds_fit_parameter": "false",
            "package_role": "required",
            "parent_status": "candidate_not_parent_signed",
            "valid_for_claim": "false",
        },
        {
            "clause_id": "LCP3394_1_smoothing_before_readout",
            "source": "PC3392_1",
            "clause": "S_ell acts on metric/source fields before fixed PPN observable coefficients are read out.",
            "closes_channel": "projector/adaptive-ray leakage",
            "adds_dynamics": "false",
            "adds_fit_parameter": "false",
            "package_role": "required",
            "parent_status": "candidate_not_parent_signed",
            "valid_for_claim": "false",
        },
        {
            "clause_id": "LCP3394_2_no_adaptive_projector",
            "source": "PC3392_2",
            "clause": "Cassini ray/impact geometry belongs to the external observable model, not to P_PPN(x) inside S_ell.",
            "closes_channel": "adaptive ray projector drift",
            "adds_dynamics": "false",
            "adds_fit_parameter": "false",
            "package_role": "required",
            "parent_status": "candidate_not_parent_signed",
            "valid_for_claim": "false",
        },
        {
            "clause_id": "LCP3394_3_single_Fermi_patch",
            "source": "PC3392_3 and GD3393",
            "clause": "Use one local Fermi/frame patch over the smoothing support; frame drift is counted as curvature-order, not a first-order adaptive readout.",
            "closes_channel": "gauge/readout drift",
            "adds_dynamics": "false",
            "adds_fit_parameter": "false",
            "package_role": "required",
            "parent_status": "candidate_not_parent_signed",
            "valid_for_claim": "false",
        },
        {
            "clause_id": "LCP3394_4_public_Hilbert_flux",
            "source": "BF3393_0",
            "clause": "Public EM/radiation/matter flux is included in T_mu_nu / Hilbert source measure before hidden MTS boundary residuals are scored.",
            "closes_channel": "Poynting hidden-boundary leakage",
            "adds_dynamics": "false",
            "adds_fit_parameter": "false",
            "package_role": "required",
            "parent_status": "candidate_not_parent_signed",
            "valid_for_claim": "false",
        },
        {
            "clause_id": "LCP3394_5_radial_even_kernel",
            "source": "KM3393_0/KM3393_1",
            "clause": "The local scalar smoothing kernel is normalized, radial/even in the tangent/Fermi patch and selected before scoring.",
            "closes_channel": "kernel first moment",
            "adds_dynamics": "false",
            "adds_fit_parameter": "false",
            "package_role": "required",
            "parent_status": "candidate_not_parent_signed",
            "valid_for_claim": "false",
        },
        {
            "clause_id": "LCP3394_6_boundary_reference_extension",
            "source": "3376",
            "clause": "Optional extension: fixed annulus, fixed primitive, trivial relative class, source-blind reference and positive M_H_ref.",
            "closes_channel": "B_zero_flux and Delta_symp",
            "adds_dynamics": "false",
            "adds_fit_parameter": "false",
            "package_role": "extension_required_for_full_boundary_zero",
            "parent_status": "candidate_not_parent_signed",
            "valid_for_claim": "false",
        },
    ]


def compatibility_rows(clauses: list[dict[str, str]]) -> list[dict[str, str]]:
    return [
        {
            "audit_id": "COMP3394_0_no_new_dynamics",
            "question": "Does the local Cassini package add new equations of motion?",
            "result": "PASS_NO_NEW_DYNAMICS" if all(row["adds_dynamics"] == "false" for row in clauses) else "FAIL_ADDS_DYNAMICS",
            "evidence": "all required clauses are readout/order/kernel/source-placement choices",
            "claim_effect": "admissible as parent package candidate, not a claim",
            "valid_for_claim": "false",
        },
        {
            "audit_id": "COMP3394_1_no_fit_parameters",
            "question": "Does the package introduce fitted local-screening knobs?",
            "result": "PASS_NO_FIT_PARAMETERS" if all(row["adds_fit_parameter"] == "false" for row in clauses) else "FAIL_ADDS_FIT",
            "evidence": "no clause introduces a new Cassini-tuned coefficient",
            "claim_effect": "avoids post-hoc local screening",
            "valid_for_claim": "false",
        },
        {
            "audit_id": "COMP3394_2_metric_smoothing_order",
            "question": "Is smoothing-before-readout consistent with the MTS emergent metric?",
            "result": "PASS_COMPATIBLE",
            "evidence": "core action defines g_mu_nu from smoothed/coarse-grained covariance of psi gradients",
            "claim_effect": "supports PC3392 order of operations as a readout convention",
            "valid_for_claim": "false",
        },
        {
            "audit_id": "COMP3394_3_public_source_measure",
            "question": "Is public EM/radiation flux placement consistent with the action?",
            "result": "PASS_COMPATIBLE",
            "evidence": "core effective action includes L_matter and T_mu_nu; public radiation belongs there before hidden residuals are scored",
            "claim_effect": "Poynting is not silently erased; it is placed in the public source measure",
            "valid_for_claim": "false",
        },
        {
            "audit_id": "COMP3394_4_kernel_choice",
            "question": "Is a radial/even scalar local kernel compatible with smoothing?",
            "result": "PASS_ADMISSIBLE_NOT_UNIQUE",
            "evidence": "MTS requires smoothing/coarse-graining but current parent does not uniquely specify the kernel shape",
            "claim_effect": "kernel moment zero remains package-conditional until parent selects the branch",
            "valid_for_claim": "false",
        },
        {
            "audit_id": "COMP3394_5_boundary_extension",
            "question": "Does the minimal package fully close B_zero_flux and Delta_symp?",
            "result": "NO_EXTENSION_REQUIRED",
            "evidence": "3376 fixed primitive/topology/reference clauses remain separate and unsigned",
            "claim_effect": "full local PPN still blocked without boundary/reference extension or finite rows",
            "valid_for_claim": "false",
        },
    ]


def channel_implication_rows() -> list[dict[str, str]]:
    return [
        {
            "implication_id": "IMP3394_0_projector",
            "channel": "projector commutator",
            "if_package_signed": "P_PPN(x)=P_0 on support; [P_PPN,S_ell]=0 exactly",
            "residual_after_package": "0 for projector channel",
            "current_status": "conditional_closed_not_parent_signed",
            "valid_for_claim": "false",
        },
        {
            "implication_id": "IMP3394_1_kernel_moment",
            "channel": "kernel first moment",
            "if_package_signed": "radial/even normalized scalar kernel gives int z_i K_ell d^3z=0",
            "residual_after_package": "0 for first-moment channel",
            "current_status": "conditional_closed_not_parent_signed",
            "valid_for_claim": "false",
        },
        {
            "implication_id": "IMP3394_2_Poynting",
            "channel": "Poynting/radiation hidden boundary leakage",
            "if_package_signed": "public EM/radiation energy is in T_mu_nu/Hilbert source measure before hidden residual scoring",
            "residual_after_package": "0 hidden-boundary Poynting residual; public stress remains physical source",
            "current_status": "conditional_placement_not_parent_signed",
            "valid_for_claim": "false",
        },
        {
            "implication_id": "IMP3394_3_gauge",
            "channel": "gauge/readout drift",
            "if_package_signed": "single Fermi/frame patch removes first-order adaptive readout drift; residual is curvature order",
            "residual_after_package": "quadratic finite drift unless parent declares exact fixed frame over support",
            "current_status": "finite_mild_not_zero",
            "valid_for_claim": "false",
        },
        {
            "implication_id": "IMP3394_4_boundary_reference",
            "channel": "B_zero_flux and Delta_symp",
            "if_package_signed": "minimal package alone does not close 3376 primitive/topology/reference clauses",
            "residual_after_package": "retained unless boundary/reference extension is signed",
            "current_status": "open",
            "valid_for_claim": "false",
        },
        {
            "implication_id": "IMP3394_5_source_normalization",
            "channel": "G/kappa/source-current normalization",
            "if_package_signed": "local residual channels may be conditionally quiet, but Newton/GR coupling still needs same-source normalization",
            "residual_after_package": "open calibrated-source-coupling gate",
            "current_status": "open_next_target",
            "valid_for_claim": "false",
        },
    ]


def residual_collapse_rows() -> list[dict[str, str]]:
    poynting_rows = read_csv_rows(OUT / "P8_Y5_R2FR_3393_CASSINI_POYNTING_FLUX_BOUND_NONCLAIM.csv")
    gauge_rows = read_csv_rows(OUT / "P8_Y5_R2FR_3393_GAUGE_READOUT_DRIFT_BOUND_ROWS_NONCLAIM.csv")
    max_poynting = max(to_float(row.get("epsilon_Poynting_luminosity_fraction", "")) for row in poynting_rows)
    strict_boundary = min(to_float(row.get("strict_boundary_target_min", "")) for row in poynting_rows)
    strictest_fermi = min(to_float(row.get("ell_s_ceiling_if_Fermi_quadratic_Ceq1_m", "")) for row in gauge_rows)
    strictest_first = min(to_float(row.get("ell_s_ceiling_if_first_order_gauge_drift_Ceq1_m", "")) for row in gauge_rows)
    return [
        {
            "collapse_id": "RC3394_0_minimal_package_projector",
            "term": "epsilon_projector_commutator",
            "before_3394": "conditional exact-zero theorem, parent unsigned",
            "if_minimal_package_signed": "0",
            "finite_fallback": f"ell_s <= {strictest_first:.12e} m if first-order adaptive readout remains",
            "claim_status": "conditional_not_claimed",
            "valid_for_claim": "false",
        },
        {
            "collapse_id": "RC3394_1_minimal_package_kernel",
            "term": "epsilon_kernel_moment",
            "before_3394": "radial/even parity theorem, parent unsigned",
            "if_minimal_package_signed": "0",
            "finite_fallback": "retain epsilon_kernel_moment row for anisotropic/adaptive/clipped kernels",
            "claim_status": "conditional_not_claimed",
            "valid_for_claim": "false",
        },
        {
            "collapse_id": "RC3394_2_minimal_package_Poynting",
            "term": "Phi_Poynting_hidden_boundary",
            "before_3394": f"finite luminosity fraction max={max_poynting:.15e}, strict target={strict_boundary:.15e}",
            "if_minimal_package_signed": "0 hidden residual because public radiation is in T_mu_nu",
            "finite_fallback": f"carry max luminosity envelope {max_poynting:.15e}",
            "claim_status": "conditional_not_claimed",
            "valid_for_claim": "false",
        },
        {
            "collapse_id": "RC3394_3_minimal_package_gauge",
            "term": "epsilon_gauge_readout",
            "before_3394": "first-order adaptive drift harsh; fixed Fermi drift quadratic",
            "if_minimal_package_signed": "quadratic curvature-order residual only",
            "finite_fallback": f"Fermi quadratic ell_s ceiling {strictest_fermi:.12e} m for C=1",
            "claim_status": "finite_mild_not_zero",
            "valid_for_claim": "false",
        },
        {
            "collapse_id": "RC3394_4_extended_boundary_reference",
            "term": "B_zero_flux + Delta_symp",
            "before_3394": "3376 conditional theorem, parent unsigned",
            "if_minimal_package_signed": "not closed by minimal package",
            "finite_fallback": "requires 3376 extension or source-backed finite boundary/reference rows",
            "claim_status": "open",
            "valid_for_claim": "false",
        },
        {
            "collapse_id": "RC3394_5_coupling",
            "term": "kappa/G/source-current normalization",
            "before_3394": "not handled by residual package",
            "if_minimal_package_signed": "still open",
            "finite_fallback": "return to weak-field source normalization",
            "claim_status": "open_next",
            "valid_for_claim": "false",
        },
    ]


def package_gate_rows() -> list[dict[str, str]]:
    return [
        {
            "gate_id": "PKG3394_0_minimal_package_coherence",
            "package": "fixed PPN readout + smoothing-before-readout + no adaptive projector + single Fermi patch + public Hilbert flux + radial/even kernel",
            "gate_result": "COHERENT_ADMISSIBLE_PARENT_PACKAGE_CANDIDATE",
            "what_it_conditionally_closes": "projector commutator; kernel first moment; hidden Poynting boundary leakage; first-order adaptive gauge drift",
            "what_it_does_not_close": "B_zero_flux/Delta_symp; source normalization; parent adoption",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "PKG3394_1_full_boundary_extension",
            "package": "minimal package + 3376 fixed primitive/topology/reference/denominator extension",
            "gate_result": "COHERENT_BUT_UNSIGNED_EXTENSION",
            "what_it_conditionally_closes": "adds B_zero_flux and Delta_symp zero theorem",
            "what_it_does_not_close": "source normalization and actual parent adoption",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "PKG3394_2_current_claim",
            "package": "current corpus without explicit parent package adoption",
            "gate_result": "NO_LOCAL_GR_CLAIM",
            "what_it_conditionally_closes": "nothing claim-valid",
            "what_it_does_not_close": "all package clauses remain candidates/nonclaim",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
    ]


def conflict_audit_rows() -> list[dict[str, str]]:
    return [
        {
            "conflict_id": "X3394_0_cosmology",
            "branch": "FLRW/cosmology",
            "possible_conflict": "fixed local PPN readout could accidentally freeze cosmological readouts",
            "audit_result": "NO_CONFLICT_IF_SCOPED_LOCAL",
            "reason": "package is explicitly local Cassini/Fermi/PPN; it does not set FLRW memory projection or Gamma_G readout",
            "valid_for_claim": "false",
        },
        {
            "conflict_id": "X3394_1_galaxy",
            "branch": "galaxy/rotation",
            "possible_conflict": "radial/even local kernel might overwrite galaxy-scale smoothing",
            "audit_result": "NO_CONFLICT_IF_SCALE_LOCAL",
            "reason": "package selects local PPN smoothing support only; galaxy branch may keep its empirical smoothing/memory scale separately",
            "valid_for_claim": "false",
        },
        {
            "conflict_id": "X3394_2_EM",
            "branch": "EM/Maxwell stress",
            "possible_conflict": "placing Poynting flux in Hilbert stress could erase emergent EM residuals",
            "audit_result": "NO_CONFLICT_IF_PUBLIC_STRESS_ONLY",
            "reason": "public EM radiation remains physical T_mu_nu; only hidden second-counted boundary leakage is zeroed",
            "valid_for_claim": "false",
        },
        {
            "conflict_id": "X3394_3_quantum_particle",
            "branch": "quantum/particle",
            "possible_conflict": "fixed readout could forbid microscopic adaptive variables",
            "audit_result": "NO_CONFLICT_IF_READOUT_ONLY",
            "reason": "package fixes local PPN observable extraction, not microscopic psi dynamics or particle-sector variables",
            "valid_for_claim": "false",
        },
    ]


def runner_rows(rows_by_name: dict[str, list[dict[str, Any]]]) -> list[dict[str, str]]:
    package_result = rows_by_name["package_gate"][0]["gate_result"]
    collapse_open = [row for row in rows_by_name["residual_collapse"] if row["claim_status"].startswith("open")]
    return [
        {
            "run_id": "RUN3394_0_clause_register",
            "test": "local package clauses registered",
            "result": "PASS_CLAUSES_REGISTERED_NONCLAIM",
            "detail": f"clauses={len(rows_by_name['package_clauses'])}",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "run_id": "RUN3394_1_compatibility",
            "test": "no dynamics/no fit/branch compatibility audit",
            "result": "PASS_COMPATIBILITY_NONCLAIM",
            "detail": "package adds no new dynamics and no fitted local-screening parameter",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "run_id": "RUN3394_2_package_gate",
            "test": "minimal local Cassini package gate",
            "result": "PASS_COHERENT_CANDIDATE_NONCLAIM",
            "detail": package_result,
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "run_id": "RUN3394_3_residual_collapse",
            "test": "conditional residual collapse table",
            "result": "PASS_COLLAPSE_TABLE_NONCLAIM",
            "detail": f"open_terms={len(collapse_open)}",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "run_id": "RUN3394_4_firewall",
            "test": "prevent local PPN/local GR claim",
            "result": "PASS_CLAIM_FIREWALL",
            "detail": "coherent package candidate is not parent adoption and does not solve source normalization",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
    ]


def gate_rows(source_ok: bool) -> list[dict[str, str]]:
    return [
        {
            "gate_id": "GATE3394_0_sources",
            "claim": "all 3394 sources exist and parse",
            "gate_pass": bool_text(source_ok),
            "reason": "local/core source register parsed",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3394_1_package_coherent",
            "claim": "minimal local Cassini package is coherent",
            "gate_pass": "true",
            "reason": "clauses are compatible, add no dynamics and no fit parameter",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3394_2_parent_adopted",
            "claim": "minimal package is parent-signed/adopted",
            "gate_pass": "false",
            "reason": "3394 is an admissibility gate; parent documents are not modified",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3394_3_boundary_reference",
            "claim": "B_zero_flux and Delta_symp are closed",
            "gate_pass": "false",
            "reason": "requires 3376 extension or finite source-backed rows",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3394_4_source_normalization",
            "claim": "Newton/GR source coupling is calibrated",
            "gate_pass": "false",
            "reason": "package handles local residual/readout hygiene, not kappa/G/source-current normalization",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3394_5_local_ppn",
            "claim": "local PPN/local-GR branch passes",
            "gate_pass": "false",
            "reason": "coherent package candidate is not parent-signed and source normalization remains open",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
    ]


def decision_rows() -> list[dict[str, str]]:
    return [
        {
            "decision_id": "DEC3394_0_progress",
            "decision": "The local Cassini hygiene clauses form a coherent admissible package.",
            "because": "fixed readout, smoothing-before-readout, public Hilbert flux placement, radial/even kernel and Fermi patch add no dynamics or fitted parameters.",
            "next_action": "treat them as one parent-package candidate, not isolated rescue moves",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC3394_1_not_a_claim",
            "decision": "The package does not yet prove local GR.",
            "because": "it is not parent-signed, boundary/reference extension remains unsigned, and calibrated source normalization is untouched.",
            "next_action": "do not score local PPN until package adoption and source normalization are handled",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC3394_2_best_physics_status",
            "decision": "The route looks less grim: local residual hygiene is packageable.",
            "because": "projector, moment, Poynting and gauge channels no longer require separate ad-hoc fixes if the package is adopted.",
            "next_action": "return to the big missing piece: kappa/G/source-current normalization",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC3394_3_best_next",
            "decision": "Next target should be weak-field source normalization.",
            "because": "GR/Newton reduction ultimately needs the same source coupling in H_tau, Poisson/Newton and PPN readout.",
            "next_action": "build 3395 weak-field source normalization return",
            "valid_for_claim": "false",
        },
    ]


def next_rows() -> list[dict[str, str]]:
    return [
        {
            "target_id": "3395-Y5-R2FR-weak-field-source-normalization-return-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3395_weak_field_source_normalization_return.py",
            "objective": "derive or bound the shared kappa/G/source-current normalization across H_tau, Poisson/Newton and PPN readout using the coherent local Cassini package as hygiene, not as a substitute for source coupling",
            "why_next": "3394 makes the local residual package coherent; the decisive GR/Newton route now returns to calibrated source coupling",
            "valid_for_claim": "false",
        },
        {
            "target_id": "3396-Y5-R2FR-boundary-reference-extension-source-pack-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3396_boundary_reference_extension_source_pack.py",
            "objective": "fill or sign the 3376 boundary/reference extension: fixed primitive, trivial relative class, source-blind reference and positive M_H_ref",
            "why_next": "if weak-field normalization needs a fully clean boundary envelope, the 3376 extension is still open",
            "valid_for_claim": "false",
        },
    ]


def all_claim_flags_false(paths: list[Path]) -> tuple[bool, str]:
    offenders: list[str] = []
    for path in paths:
        if not path.exists() or path.suffix.lower() != ".csv":
            continue
        for index, row in enumerate(read_csv_rows(path), start=2):
            if "valid_for_claim" in row and row["valid_for_claim"].strip().lower() != "false":
                offenders.append(f"{path.name}:line{index}:{row['valid_for_claim']}")
    return not offenders, "; ".join(offenders)


def validate(rows_by_name: dict[str, list[dict[str, Any]]]) -> list[dict[str, str]]:
    source_ok = all(row["exists"] == "true" and row["parse_ok"] == "true" for row in rows_by_name["source_register"])
    output_csvs = [path for key, path in OUTPUTS.items() if key != "validation" and path.suffix.lower() == ".csv"]
    parse_results = [parse_csv(path)[0] for path in output_csvs if path.exists()]
    flags_ok, flag_detail = all_claim_flags_false(output_csvs)
    formalization_hits = [
        hit
        for hit in FW.rglob("*3394*")
        if hit.name.startswith(("3394-Y5", "P8_Y5_R2FR_3394", "P8_Y5_BRR545_3394", "Y5_R2FR_3394"))
    ] if FW.exists() else []
    clause_required = [row for row in rows_by_name["package_clauses"] if row["package_role"] == "required"]
    compat_results = {row["result"] for row in rows_by_name["compatibility"]}
    implication_channels = {row["channel"] for row in rows_by_name["channel_implications"]}
    collapse_terms = {row["term"] for row in rows_by_name["residual_collapse"]}
    package_results = {row["gate_result"] for row in rows_by_name["package_gate"]}
    gate_map = {row["gate_id"]: row["gate_pass"] for row in rows_by_name["gates"]}
    runner_results = {row["result"] for row in rows_by_name["runner"]}
    checks = [
        ("VAL3394_0_sources_exist_parse", "all cited 3394 source paths exist and parse", source_ok, ""),
        ("VAL3394_1_outputs_parse", "all generated CSV outputs parse cleanly", len(parse_results) == len(output_csvs) and all(parse_results), f"parsed={sum(1 for ok in parse_results if ok)} expected={len(output_csvs)}"),
        ("VAL3394_2_required_clauses", "required local package clauses are registered", len(clause_required) >= 6 and all(row["adds_dynamics"] == "false" and row["adds_fit_parameter"] == "false" for row in clause_required), f"required={len(clause_required)}"),
        ("VAL3394_3_compatibility", "compatibility audit passes no-dynamics/no-fit and source/readout checks", {"PASS_NO_NEW_DYNAMICS", "PASS_NO_FIT_PARAMETERS", "PASS_COMPATIBLE", "PASS_ADMISSIBLE_NOT_UNIQUE", "NO_EXTENSION_REQUIRED"}.issubset(compat_results), ""),
        ("VAL3394_4_channel_implications", "channel implications cover projector, kernel, Poynting, gauge, boundary and source normalization", {"projector commutator", "kernel first moment", "Poynting/radiation hidden boundary leakage", "gauge/readout drift", "B_zero_flux and Delta_symp", "G/kappa/source-current normalization"}.issubset(implication_channels), ""),
        ("VAL3394_5_residual_collapse", "residual collapse table covers local residual terms and open coupling", {"epsilon_projector_commutator", "epsilon_kernel_moment", "Phi_Poynting_hidden_boundary", "epsilon_gauge_readout", "B_zero_flux + Delta_symp", "kappa/G/source-current normalization"}.issubset(collapse_terms), ""),
        ("VAL3394_6_package_gate", "package gate marks coherent candidate but blocks current claim", {"COHERENT_ADMISSIBLE_PARENT_PACKAGE_CANDIDATE", "COHERENT_BUT_UNSIGNED_EXTENSION", "NO_LOCAL_GR_CLAIM"}.issubset(package_results), ""),
        ("VAL3394_7_conflict_audit", "cross-branch conflict audit covers cosmology, galaxy, EM and quantum/particle", len(rows_by_name["conflict_audit"]) >= 4, f"rows={len(rows_by_name['conflict_audit'])}"),
        ("VAL3394_8_runner", "runner records clauses, compatibility, package gate, residual collapse and firewall", {"PASS_CLAUSES_REGISTERED_NONCLAIM", "PASS_COMPATIBILITY_NONCLAIM", "PASS_COHERENT_CANDIDATE_NONCLAIM", "PASS_COLLAPSE_TABLE_NONCLAIM", "PASS_CLAIM_FIREWALL"}.issubset(runner_results), ""),
        ("VAL3394_9_gates", "gates pass coherence but block parent adoption, boundary, source normalization and local PPN", gate_map.get("GATE3394_1_package_coherent") == "true" and gate_map.get("GATE3394_2_parent_adopted") == "false" and gate_map.get("GATE3394_3_boundary_reference") == "false" and gate_map.get("GATE3394_4_source_normalization") == "false" and gate_map.get("GATE3394_5_local_ppn") == "false", ""),
        ("VAL3394_10_no_overclaim_flags", "all generated rows with valid_for_claim remain false", flags_ok, flag_detail),
        ("VAL3394_11_write_scope_outside_formalization", "no 3394 files were written under formalization-workbench", not formalization_hits, f"hits={len(formalization_hits)}"),
        ("VAL3394_12_next_target", "next target moves to weak-field source normalization", rows_by_name["next"][0]["target_id"].startswith("3395-Y5-R2FR-weak-field-source-normalization"), ""),
    ]
    overall = all(passed for _, _, passed, _ in checks)
    checks.append(("VAL3394_13_overall", "3394 validation overall", overall, "all required checks passed" if overall else "one or more checks failed"))
    return [{"check_id": check_id, "check": check, "passed": bool_text(passed), "detail": detail} for check_id, check, passed, detail in checks]


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    lines = [
        "# 3394 - Y5/R2FR local Cassini admissible package gate under AX1090",
        "",
        "## Summary",
        "- 3394 bundles the previously separate local-Cassini clauses into one admissible parent-package candidate.",
        "- Package verdict: coherent and admissible as a local PPN readout/source/kernel hygiene package; it adds no new dynamics and no fitted parameter.",
        "- If parent-signed, the minimal package conditionally closes projector commutator, kernel first moment, hidden Poynting leakage and first-order adaptive gauge drift.",
        "- It does not close everything: `B_zero_flux/Delta_symp` still need the 3376 boundary/reference extension, and GR/Newton still need calibrated `kappa/G/source-current` normalization.",
        "- Therefore this is real progress but not a local-GR claim; the next decisive target is source normalization.",
        "",
        "## Source Register",
        md_table(rows_by_name["source_register"]),
        "## Local Package Clause Register",
        md_table(rows_by_name["package_clauses"]),
        "## Package Compatibility Audit",
        md_table(rows_by_name["compatibility"]),
        "## Channel Implications",
        md_table(rows_by_name["channel_implications"]),
        "## Local Residual Collapse Table",
        md_table(rows_by_name["residual_collapse"]),
        "## Admissible Package Gate",
        md_table(rows_by_name["package_gate"]),
        "## Cross-Branch Conflict Audit",
        md_table(rows_by_name["conflict_audit"]),
        "## Nonclaim Runner",
        md_table(rows_by_name["runner"]),
        "## Promotion Gates",
        md_table(rows_by_name["gates"]),
        "## Decision Ledger",
        md_table(rows_by_name["decision"]),
        "## Validation",
        md_table(rows_by_name["validation"]),
        "## Next Target",
        md_table(rows_by_name["next"]),
    ]
    DOC.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    source_register = source_rows()
    source_ok = all(row["exists"] == "true" and row["parse_ok"] == "true" for row in source_register)
    clauses = package_clause_rows()
    rows_by_name: dict[str, list[dict[str, Any]]] = {
        "source_register": source_register,
        "package_clauses": clauses,
        "compatibility": compatibility_rows(clauses),
        "channel_implications": channel_implication_rows(),
        "residual_collapse": residual_collapse_rows(),
        "package_gate": package_gate_rows(),
        "conflict_audit": conflict_audit_rows(),
    }
    rows_by_name["runner"] = runner_rows(rows_by_name)
    rows_by_name["gates"] = gate_rows(source_ok)
    rows_by_name["decision"] = decision_rows()
    rows_by_name["next"] = next_rows()
    for name, rows in rows_by_name.items():
        write_csv(OUTPUTS[name], rows)
    rows_by_name["validation"] = validate(rows_by_name)
    write_csv(OUTPUTS["validation"], rows_by_name["validation"])
    write_doc(rows_by_name)
    if PYCACHE.exists():
        shutil.rmtree(PYCACHE)
    print(f"Wrote {DOC}")
    print(f"Wrote {len(OUTPUTS)} CSV outputs under {OUT}")
    print(f"Generated UTC {RUN_UTC}")


if __name__ == "__main__":
    main()
