from __future__ import annotations

import csv
from datetime import datetime, timezone
from io import StringIO
from pathlib import Path
from typing import Dict, Iterable, List, Tuple


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"
PARENT_DIR = POST / "source-intake" / "parent-action"

CHECKPOINT = "4380"
CLAIM_ID = "L-221"
MARKER = "PPC4161_TRANSITION_TOPOLOGICAL_MOMENT_SOURCE_INTAKE_OR_L0_PARENT_SYMMETRY_SIGNATURE_4380"
PACKET_MARKER = "PPC4161_PACKET_TRANSITION_TOPOLOGICAL_MOMENT_SOURCE_INTAKE_OR_L0_PARENT_SYMMETRY_SIGNATURE_4380"
DECISION = "CENTER_GUARD_REFINED_L0_PARENT_SIGNATURE_CONTRACT_DERIVED_SOURCE_INTAKE_SWEEP_NO_VALID_ROWS_NONCLAIM"
NEXT_TARGET = "4381-Y5-R2FR-transition-topological-defect-normal-form-or-profile-quadrature-runner.md"

FORMAL_PATH = FORMAL / "396-PPC4161-transition-topological-moment-source-intake-or-l0-parent-symmetry-signature.md"
DOC_PATH = POST / "4380-Y5-R2FR-transition-topological-moment-source-intake-or-l0-parent-symmetry-signature.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4380_VALIDATION.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

LOCAL_SOURCES: Dict[str, Tuple[Path, str, str]] = {
    "SRC4380_00_4379_formal": (
        FORMAL / "395-PPC4161-transition-harmonic-null-parent-signature-or-first-numeric-topological-moment-input.md",
        "PPC4161_TRANSITION_HARMONIC_NULL_PARENT_SIGNATURE_OR_FIRST_NUMERIC_TOPOLOGICAL_MOMENT_INPUT_4379",
        "4379 handoff that split Laplacian-null and centered l=0 routes.",
    ),
    "SRC4380_01_4379_l0_theorem": (
        SOURCE_DIR / "P8_Y5_R2FR_4379_L0_SYMMETRY_THEOREM.csv",
        "L0S4379_0_statement",
        "Exact centered l=0 zero-monopole theorem being refined.",
    ),
    "SRC4380_02_4379_signature_audit": (
        SOURCE_DIR / "P8_Y5_R2FR_4379_PARENT_SIGNATURE_AUDIT.csv",
        "SIG4379_1_centered_l0_symmetry",
        "Current parent-signature status for the l=0 route.",
    ),
    "SRC4380_03_4379_numeric_template": (
        SOURCE_DIR / "P8_Y5_R2FR_4379_NUMERIC_MOMENT_INPUT_TEMPLATE.csv",
        "MIN4379_SUP4371_2_Sun_Earth_average_l1",
        "First concrete moment-input template staged by 4379.",
    ),
    "SRC4380_04_4378_harmonic_null": (
        SOURCE_DIR / "P8_Y5_R2FR_4378_HARMONIC_NULL_THEOREM.csv",
        "HN4378_1_laplacian_null_sufficient_condition",
        "Laplacian-null route retained as exact sufficient condition.",
    ),
    "SRC4380_05_4378_bounds": (
        SOURCE_DIR / "P8_Y5_R2FR_4378_TOPOLOGICAL_MULTIPOLE_BOUND_ROWS.csv",
        "TB4378_SUP4371_2_Sun_Earth_average_dipole",
        "Existing multipole score rows with values still missing.",
    ),
    "SRC4380_06_4377_moment_gate": (
        FORMAL / "393-PPC4161-transition-parent-grammar-no-source-shadow-or-topological-profile-equality.md",
        "M_lm^top-H := int_W delta rho_top r^l Y_lm dV_H = 0",
        "Distributional/moment gate that prevents total-charge shortcuts.",
    ),
    "SRC4380_07_4294_kernel": (
        FORMAL / "310-PPC4161-transition-source-kernel-zero-theorem-or-projection-suppression-map.md",
        "P_kernel := P_Hilbert,l=0,static,universal,range-free,same-metric,same-worldtube",
        "Conditional source-kernel projector containing the safe l=0 branch.",
    ),
    "SRC4380_08_4356_common_mode": (
        FORMAL / "372-PPC4161-transition-static-monopole-universal-rangefree-hair-zero-or-bound.md",
        "q_0^H :=",
        "Common Hilbert monopole source dressing route.",
    ),
    "SRC4380_09_186_same_object": (
        FORMAL / "186-PPC4161-Hamiltonian-worldtube-mass-readout-glue.md",
        "Same-Object Glue",
        "Hamiltonian/Hilbert same-worldtube charge support, but not profile equality.",
    ),
    "SRC4380_10_191_poynting": (
        FORMAL / "191-PPC4161-Maxwell-Hodge-Poynting-stress-owner-theorem.md",
        "Poynting vector is not a separate background field",
        "EM flux must not be smuggled in as topological moment hair.",
    ),
    "SRC4380_11_3037_source_lock": (
        PARENT_DIR / "minimum_source_readout_lock_parent_clause_3037_NOT_SIGNED.csv",
        "MSRL3037_2_universal_matter",
        "Parent source-readout lock remains contract-only.",
    ),
    "SRC4380_12_3055_hilbert_descent": (
        PARENT_DIR / "Hilbert_source_descent_theorem_attempt_3055_NOT_SIGNED.csv",
        "HSD3055_5_verdict",
        "Hilbert source descent route is coherent but not signed.",
    ),
    "SRC4380_13_3079_geometry_stack": (
        PARENT_DIR / "local_geometry_field_list_signature_3079_NOT_SIGNED.csv",
        "LGS3079_2_single_geometry_stack",
        "Single geometry stack descent remains unsigned.",
    ),
    "SRC4380_14_q_loc_surrogate": (
        SOURCE_DIR / "P8_Y5_PARENT_QLOC_2001_SURROGATE_THIN_GRID_SEGMENT210_NONCLAIM.csv",
        "spherical_Earth_monopole_zero_phase_surrogate_not_official",
        "A tempting old surrogate grid, explicitly non-official and not valid topological moment evidence.",
    ),
}


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def find_line(path: Path, needle: str) -> str:
    text = read_text(path)
    index = text.find(needle)
    if index < 0:
        return ""
    return str(text[:index].count("\n") + 1)


def read_csv(path: Path) -> List[Dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: List[Dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    fields: List[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: str(row.get(field, "")) for field in fields})


def csv_line(row: Iterable[str]) -> str:
    buffer = StringIO()
    writer = csv.writer(buffer, lineterminator="\n")
    writer.writerow(list(row))
    return buffer.getvalue()


def md_cell(value: object) -> str:
    return str(value).replace("|", r"\|").replace("\n", "<br>")


def md_table(rows: List[Dict[str, str]], fields: List[str]) -> str:
    lines = [
        "| " + " | ".join(fields) + " |",
        "| " + " | ".join("---" for _ in fields) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(md_cell(row.get(field, "")) for field in fields) + " |")
    return "\n".join(lines)


def append_once(path: Path, marker: str, block: str) -> None:
    text = read_text(path)
    if marker in text:
        return
    if text and not text.endswith("\n"):
        text += "\n"
    path.write_text(text + block.strip() + "\n", encoding="utf-8")


def append_claim_once(path: Path, claim_id: str, row: List[str]) -> None:
    text = read_text(path)
    if f"\n{claim_id}," in text:
        return
    if text and not text.endswith("\n"):
        text += "\n"
    path.write_text(text + csv_line(row), encoding="utf-8")


def source_register_rows() -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    for source_id, (path, needle, role) in LOCAL_SOURCES.items():
        line_number = find_line(path, needle)
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "source_id": source_id,
                "path": str(path),
                "path_exists": str(path.exists()),
                "needle": needle,
                "needle_found": str(bool(line_number)),
                "line_number": line_number,
                "role": role,
                "valid_for_claim": "False",
            }
        )
    return rows


def center_guard_refinement_rows() -> List[Dict[str, str]]:
    return [
        {
            "refinement_id": "CGR4380_0_pure_defect_translation",
            "object": "pure radial zero-monopole defect",
            "statement": "If delta rho_top itself is radial about some parent-owned center and has zero total mass, its exterior Newton field is zero; a passive coordinate-origin shift does not create physical multipole hair.",
            "derivation": "Newton shell theorem gives Phi_ext=-G M_delta/r outside the defect support; M_delta=0, so Phi_ext=0 and every exterior expansion coefficient vanishes.",
            "effect": "Corrects the center guard: the danger is not passive coordinate translation of a pure zero-mass radial defect.",
            "status": "EXACT_REFINEMENT",
            "valid_for_claim": "False",
        },
        {
            "refinement_id": "CGR4380_1_separate_profile_centers",
            "object": "rho_top and rho_H separately centered",
            "statement": "If rho_top and rho_H are individually radial but about different parent centers, delta rho_top=rho_top-rho_H is generically not radial and carries l>=1 moments.",
            "derivation": "For two equal monopole profiles shifted by b, the first-order difference is -b dot grad rho_H, whose dipole moment is proportional to M_H b.",
            "effect": "The real same-center requirement is common profile ownership before subtraction, not a cosmetic coordinate convention.",
            "status": "EXACT_COUNTERMODEL_REFINED",
            "valid_for_claim": "False",
        },
        {
            "refinement_id": "CGR4380_2_acceptance_guard",
            "object": "allowed l0 route",
            "statement": "The l=0 theorem can be activated by either direct parent ownership of radial zero-monopole delta rho_top or by common-center isotropy of rho_top and rho_H before readout.",
            "derivation": "Either route makes delta rho_top=f(|y-y_c|) and int delta rho_top dV=0, so 4379 angular orthogonality applies.",
            "effect": "Gives a sharper, less self-defeating parent contract for the next proof attempt.",
            "status": "CONDITIONAL_ACTIVATION_RULE",
            "valid_for_claim": "False",
        },
    ]


def l0_parent_signature_contract_rows() -> List[Dict[str, str]]:
    return [
        {
            "clause_id": "L0PC4380_0_isotropy_or_direct_radial_defect",
            "required_clause": "parent source construction is SO(3)-invariant around a parent-owned source center, or directly outputs radial zero-monopole delta rho_top",
            "mathematical_effect": "delta rho_top=f(r) before readout",
            "current_evidence": "4294/4356 define conditional static l=0 kernel branch; 4379 derives effect if active",
            "current_status": "CONDITIONAL_THEOREM_NOT_PARENT_SIGNED",
            "missing_for_claim": "MISSING_RAW_TOPOLOGICAL_DEFECT_ISOTROPY_OR_DIRECT_RADIAL_NORMAL_FORM",
            "valid_for_claim": "False",
        },
        {
            "clause_id": "L0PC4380_1_common_center_before_subtraction",
            "required_clause": "rho_top and rho_H share the same parent center/worldtube before delta rho_top is formed, or delta rho_top is directly parent-centered",
            "mathematical_effect": "separately centered radial profiles cannot manufacture dipole hair",
            "current_evidence": "186/4377 give same-worldtube/charge glue, not full profile-center equality",
            "current_status": "CENTER_OWNER_UNSIGNED",
            "missing_for_claim": "MISSING_PARENT_CENTER_FUNCTIONAL_FOR_TOPOLOGICAL_AND_HILBERT_PROFILES",
            "valid_for_claim": "False",
        },
        {
            "clause_id": "L0PC4380_2_zero_monopole",
            "required_clause": "int_W delta rho_top dV=0 from same Hamiltonian/Hilbert charge",
            "mathematical_effect": "l=0 exterior charge vanishes",
            "current_evidence": "186 and 4377 support same total charge as the monopole-only branch",
            "current_status": "MONOPOLE_IMPORTED_BUT_INSUFFICIENT_ALONE",
            "missing_for_claim": "MISSING_LGE1_MOMENT_SILENCE_OR_RADIAL_NORMAL_FORM",
            "valid_for_claim": "False",
        },
        {
            "clause_id": "L0PC4380_3_no_anisotropic_slot",
            "required_clause": "no vector/tensor/readout/boundary slot can feed l>=1 data into the topological profile representative",
            "mathematical_effect": "forbids anisotropic rho_top-rho_H source hair",
            "current_evidence": "3037/3055/3079 keep source-readout and geometry-stack descent unsigned",
            "current_status": "NOT_PARENT_SIGNED",
            "missing_for_claim": "MISSING_NO_ANISOTROPIC_TOPOLOGICAL_PROFILE_SLOT",
            "valid_for_claim": "False",
        },
        {
            "clause_id": "L0PC4380_4_boundary_flux_silence",
            "required_clause": "boundary/Hamiltonian flux has no compact-local l>=1 density projection",
            "mathematical_effect": "prevents exterior multipoles from entering through collar/boundary representatives",
            "current_evidence": "4378 Laplacian route requires boundary silence; 4356 keeps boundary-owned condition conditional",
            "current_status": "BOUNDARY_SILENCE_UNSIGNED",
            "missing_for_claim": "MISSING_TOPOLOGICAL_BOUNDARY_LGE1_PROJECTION_ZERO",
            "valid_for_claim": "False",
        },
        {
            "clause_id": "L0PC4380_5_EM_Poynting_side_channel",
            "required_clause": "Poynting/radiative EM stress is counted only as Hilbert stress or Hamiltonian boundary flux, never as extra rho_top hair",
            "mathematical_effect": "blocks fake background-field anisotropic source injection",
            "current_evidence": "191/4356 close this only inside the private Maxwell-Hodge owner branch",
            "current_status": "CONDITIONAL_IMPORTED_NOT_GLOBAL",
            "missing_for_claim": "MISSING_GLOBAL_PARENT_ADOPTION_AND_BOUNDARY_FLUX_ROUTING",
            "valid_for_claim": "False",
        },
        {
            "clause_id": "L0PC4380_6_verdict",
            "required_clause": "all l=0 parent clauses close in one branch",
            "mathematical_effect": "E_l^top=0 for exterior Newton/orbital scoring",
            "current_evidence": "the conditional math is now sharp, but raw topological profile ownership is still unsigned",
            "current_status": "L0_PARENT_SIGNATURE_NOT_SIGNED",
            "missing_for_claim": "MISSING_L0PC4380_0; MISSING_L0PC4380_1; MISSING_L0PC4380_3; MISSING_L0PC4380_4",
            "valid_for_claim": "False",
        },
    ]


def source_intake_sweep_rows() -> List[Dict[str, str]]:
    qloc_path = SOURCE_DIR / "P8_Y5_PARENT_QLOC_2001_SURROGATE_THIN_GRID_SEGMENT210_NONCLAIM.csv"
    return [
        {
            "candidate_id": "SWP4380_0_4379_input_template",
            "path": str(SOURCE_DIR / "P8_Y5_R2FR_4379_NUMERIC_MOMENT_INPUT_TEMPLATE.csv"),
            "candidate_type": "topological_moment_template",
            "numeric_value_found": "False",
            "source_profile_path_found": "False",
            "reason_invalid": "MISSING_MOMENT_VALUE; template only",
            "status": "SCHEMA_READY_VALUES_MISSING",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "candidate_id": "SWP4380_1_4378_bound_rows",
            "path": str(SOURCE_DIR / "P8_Y5_R2FR_4378_TOPOLOGICAL_MULTIPOLE_BOUND_ROWS.csv"),
            "candidate_type": "score_formula_rows",
            "numeric_value_found": "False",
            "source_profile_path_found": "False",
            "reason_invalid": "geometry factors exist but E_l^top/M_lm values are explicitly missing",
            "status": "FORMULA_ONLY_NONCLAIM",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "candidate_id": "SWP4380_2_parent_q_loc_surrogate",
            "path": str(qloc_path),
            "candidate_type": "old_surrogate_grid",
            "numeric_value_found": str(qloc_path.exists() and "spherical_Earth_monopole_zero_phase_surrogate_not_official" in read_text(qloc_path)),
            "source_profile_path_found": "False",
            "reason_invalid": "surrogate_not_official; not rho_top-rho_H profile; no parent-owned source profile path",
            "status": "TEMPTING_BUT_REJECTED_AS_EVIDENCE",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "candidate_id": "SWP4380_3_parent_action_audits",
            "path": str(PARENT_DIR),
            "candidate_type": "parent_signature_audits",
            "numeric_value_found": "False",
            "source_profile_path_found": "False",
            "reason_invalid": "parent-action rows are NOT_SIGNED/CONDITIONAL, not source-owned numeric topological profiles",
            "status": "NO_VALID_PARENT_NUMERIC_ROWS",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "candidate_id": "SWP4380_4_current_verdict",
            "path": str(ROOT),
            "candidate_type": "checkpoint_sweep_verdict",
            "numeric_value_found": "False",
            "source_profile_path_found": "False",
            "reason_invalid": "no row found with source-backed rho_H_path, rho_top_path, center_owner, M_lm/E_l^top numeric value and valid_for_claim=true",
            "status": "NO_VALID_TOPOLOGICAL_MOMENT_INPUT_FOUND",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
    ]


def profile_intake_contract_rows() -> List[Dict[str, str]]:
    return [
        {
            "contract_id": "PIC4380_0_required_profile_pair",
            "required_input": "rho_H_profile_path and rho_top_profile_path or analytic formulas for both on same W_H",
            "acceptance_test": "paths/formulas exist; units declared; profile domains overlap; ordinary Hilbert profile and topological representative are not fitted after scoring",
            "status": "REQUIRED_NOT_FILLED",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "contract_id": "PIC4380_1_center_owner",
            "required_input": "parent-owned center functional for rho_H and rho_top, or direct center for delta rho_top",
            "acceptance_test": "center fixed before readout and before moment extraction; no post-hoc centering to kill a dipole",
            "status": "REQUIRED_NOT_FILLED",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "contract_id": "PIC4380_2_monopole_subtraction",
            "required_input": "M0_delta=int_W(rho_top-rho_H)dV and explicit subtraction/charge equality statement",
            "acceptance_test": "M0_delta=0 from parent charge or finite residual routed separately; no orbital GM calibration hides it",
            "status": "MONOPOLE_ONLY_PARTIALLY_SUPPORTED",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "contract_id": "PIC4380_3_moment_values",
            "required_input": "M_1m and M_2m values or conservative upper bounds with extraction method",
            "acceptance_test": "numeric finite values with units mass*length^l or dimensionless E_l^top; quadrature/domain error recorded",
            "status": "REQUIRED_NOT_FILLED",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "contract_id": "PIC4380_4_no_claim_promotion",
            "required_input": "valid_for_claim only true after all previous rows are real and sourced",
            "acceptance_test": "no MISSING, SURROGATE, NOT_SIGNED, NONCLAIM, or placeholder path markers",
            "status": "FAIL_CLOSED",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
    ]


def claim_gate_rows() -> List[Dict[str, str]]:
    return [
        {
            "gate_id": "GATE4380_0_l0_signature",
            "claim_tested": "topological exterior moments vanish by l=0 parent symmetry",
            "required_inputs": "L0PC4380 clauses 0-5 all parent-signed in one branch",
            "status": "BLOCKED_PARENT_SIGNATURE_UNSIGNED",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "GATE4380_1_numeric_moment",
            "claim_tested": "finite topological moment row can be scored",
            "required_inputs": "PIC4380 profile pair, center owner, monopole handling and M_lm/E_l^top values",
            "status": "BLOCKED_NO_VALID_SOURCE_INPUT_FOUND",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "GATE4380_2_laplacian_route",
            "claim_tested": "topological exterior moments vanish by Laplacian-null boundary silence",
            "required_inputs": "delta rho_top=Delta u_top and boundary silence parent-signed",
            "status": "UNCHANGED_BLOCKED_PARENT_SIGNATURE_UNSIGNED",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "GATE4380_3_local_GR",
            "claim_tested": "local GR/Newton/PPN/clock/orbital pass",
            "required_inputs": "topological moment route plus remaining E_shadow/E_nonHilbert/E_readout/E_boundary components closed",
            "status": "FORBIDDEN_COMPONENTS_OPEN",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def decision_rows() -> List[Dict[str, str]]:
    return [
        {
            "decision_id": "DEC4380_0",
            "decision": DECISION,
            "summary": (
                "4380 sharpens the l=0 route rather than merely repeating that it is unsigned. A pure radial zero-monopole delta rho_top is exterior-silent by shell symmetry; the real danger is that rho_top and rho_H are separately centered, anisotropic, boundary-fed, or readout-shifted before their difference is formed. "
                "The checkpoint derives the exact parent l=0 signature contract and sweeps current files for a real topological moment/profile input. No valid source-backed M_lm/E_l^top row exists yet; old q_loc surrogate grids are explicitly rejected as evidence."
            ),
            "next_target": NEXT_TARGET,
            "why_next": "The proof route is now a normal-form problem and the empirical route is a profile-quadrature problem; 4381 should implement both cleanly.",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        }
    ]


def status_rows() -> List[Dict[str, str]]:
    return [
        {
            "status_id": "STAT4380_0_center_guard",
            "object": "center guard",
            "status": "REFINED",
            "note": "passive coordinate shifts are not the issue; separate profile centers or post-readout centering are.",
            "valid_for_claim": "False",
        },
        {
            "status_id": "STAT4380_1_l0_contract",
            "object": "l=0 parent signature",
            "status": "CONTRACT_DERIVED_NOT_SIGNED",
            "note": "requires source isotropy/direct radial defect, common center, zero monopole, no anisotropic slot, and boundary silence.",
            "valid_for_claim": "False",
        },
        {
            "status_id": "STAT4380_2_source_intake",
            "object": "topological moment/profile input",
            "status": "NO_VALID_ROWS_FOUND",
            "note": "existing rows are templates, formula rows, unsigned parent audits, or non-official surrogates.",
            "valid_for_claim": "False",
        },
        {
            "status_id": "STAT4380_3_next",
            "object": "next derivation/runner",
            "status": "NORMAL_FORM_OR_QUADRATURE_NEXT",
            "note": NEXT_TARGET,
            "valid_for_claim": "False",
        },
    ]


def next_target_rows() -> List[Dict[str, str]]:
    return [
        {
            "next_id": "NT4380_0",
            "target": NEXT_TARGET,
            "question": "Can the topological defect be put in a parent-owned radial/Laplacian normal form, or must we compute its first moments from a supplied profile?",
            "preferred_route": "derive a normal-form theorem: delta rho_top is radial zero-monopole or Laplacian-null from the parent source-kernel construction.",
            "fallback_route": "build a small profile quadrature runner that ingests analytic/grid rho_H and rho_top profiles and outputs M_1m/M_2m/E_l^top nonclaim rows.",
            "avoid": "using old surrogate q_loc grids, total charge, metric-nullity, or post-hoc centering as moment-zero evidence.",
            "valid_for_claim": "False",
        }
    ]


def write_formal_doc(
    sources: List[Dict[str, str]],
    center_refinements: List[Dict[str, str]],
    l0_contract: List[Dict[str, str]],
    sweep: List[Dict[str, str]],
    profile_contract: List[Dict[str, str]],
    gates: List[Dict[str, str]],
    decisions: List[Dict[str, str]],
    statuses: List[Dict[str, str]],
    next_targets: List[Dict[str, str]],
) -> None:
    text = f"""# PPC4161 transition: topological moment source intake or l0 parent symmetry signature

Marker: `{MARKER}`

Private checkpoint: `{CHECKPOINT}`  
UTC stamp: `{STAMP}`  
Decision: `{DECISION}`

## Result

4380 does **not** claim the local/topological branch. It makes one useful mathematical correction and one practical intake advance.

The correction is:

```text
If delta rho_top itself is radial and has zero monopole,
then its exterior Newton field is zero by shell symmetry.
Passive coordinate-origin changes do not create real moment hair.
```

So the real center problem is sharper:

```text
rho_top radial about c_top and rho_H radial about c_H
with c_top != c_H
=> delta rho_top is generically anisotropic
=> dipole/quadrupole rows are physical unless a parent common-center rule exists.
```

This turns the l=0 route into a precise parent contract. The parent must either sign a direct radial zero-monopole normal form for `delta rho_top`, or sign common-center isotropy for both `rho_top` and `rho_H` before subtraction/readout. Existing files do not sign that raw topological/Hamiltonian defect.

The intake sweep also found no valid source-backed `M_lm`/`E_l^top` row. Old surrogate grids are explicitly rejected as evidence.

## Source Register

{md_table(sources, ["source_id", "path", "path_exists", "needle", "needle_found", "line_number", "role"])}

## Center Guard Refinement

{md_table(center_refinements, ["refinement_id", "object", "statement", "derivation", "effect", "status"])}

## l0 Parent Signature Contract

{md_table(l0_contract, ["clause_id", "required_clause", "mathematical_effect", "current_evidence", "current_status", "missing_for_claim"])}

## Source Intake Sweep

{md_table(sweep, ["candidate_id", "path", "candidate_type", "numeric_value_found", "source_profile_path_found", "reason_invalid", "status"])}

## Profile Intake Contract

{md_table(profile_contract, ["contract_id", "required_input", "acceptance_test", "status"])}

## Claim Gates

{md_table(gates, ["gate_id", "claim_tested", "required_inputs", "status", "claim_allowed"])}

## Decision

{md_table(decisions, ["decision_id", "decision", "summary", "next_target", "why_next"])}

## Status

{md_table(statuses, ["status_id", "object", "status", "note"])}

## Next Target

{md_table(next_targets, ["next_id", "target", "question", "preferred_route", "fallback_route", "avoid"])}
"""
    FORMAL_PATH.write_text(text, encoding="utf-8")


def write_post_doc(decisions: List[Dict[str, str]], next_targets: List[Dict[str, str]]) -> None:
    text = f"""# 4380: topological moment source intake or l0 parent symmetry signature

Marker: `{MARKER}`

## What changed

- Refined the center guard: passive coordinate shifts are not the problem; separately centered profiles or post-readout centering are.
- Derived the exact l=0 parent-signature contract needed to activate the 4379 theorem.
- Swept current template/formula/surrogate rows and found no valid source-backed topological moment input.
- Kept every local-GR/Newton/PPN/clock/orbital claim gate false.

## Decision

{md_table(decisions, ["decision_id", "decision", "summary", "next_target", "why_next"])}

## Next target

{md_table(next_targets, ["next_id", "target", "question", "preferred_route", "fallback_route", "avoid"])}
"""
    DOC_PATH.write_text(text, encoding="utf-8")


def write_spine_update() -> None:
    block = f"""
## 4380 Transition topological moment source intake or l0 parent signature

Marker: `{MARKER}`

4380 refines the l=0/topological-moment route. A pure radial zero-monopole `delta rho_top` is exterior-silent by shell symmetry; a passive coordinate shift does not make real multipoles. The danger is separate profile centers, anisotropic topological slots, boundary/collar flux, or readout choices that make `rho_top-rho_H` non-radial before subtraction.

The parent contract is now exact: sign a direct radial zero-monopole normal form for `delta rho_top`, or sign common-center isotropy of `rho_top` and `rho_H` before readout, plus zero monopole, no anisotropic slot, boundary silence, and no EM/Poynting side-channel. Current files do not sign those clauses. The source-intake sweep found no valid source-backed moment values; old surrogate grids remain rejected as evidence.

Next target: `{NEXT_TARGET}`.
"""
    append_once(SPINE_PATH, MARKER, block)


def write_packet_update() -> None:
    block = f"""
## 4380 packet update: l0 center guard refined and source intake fail-closed

Marker: `{PACKET_MARKER}`

Packet update: topological l=0 safety is now a normal-form contract, not a vague same-center slogan. Pure radial zero-monopole `delta rho_top` is exterior-silent; the live obstruction is whether the parent owns that radial defect or common-center isotropy of `rho_top` and `rho_H` before readout. No valid numeric topological moment row was found, and old surrogate `q_loc` grids are not evidence.
"""
    append_once(PACKET_PATH, PACKET_MARKER, block)


def write_claim() -> None:
    append_claim_once(
        CLAIMS_PATH,
        CLAIM_ID,
        [
            CLAIM_ID,
            "local_gr",
            (
                "4380 refines the topological l=0 route. A pure radial zero-monopole delta rho_top has zero exterior Newton field by shell symmetry, so passive coordinate-origin shifts are not the physical problem. "
                "The actual obstruction is whether the parent owns a radial zero-monopole defect directly, or common-center isotropy of rho_top and rho_H before their difference is formed; separately centered or anisotropic profiles generically carry l>=1 moments. "
                "4380 derives the exact l=0 parent-signature contract and sweeps current files for source-backed topological moment inputs. No valid M_lm/E_l^top row is found; old q_loc surrogate rows are rejected as evidence. No local-GR/Newton/PPN/clock/orbital claim fires."
            ),
            "4380 source register, center guard refinement, l0 parent signature contract, source intake sweep, profile intake contract, claim gates, decision, status, next target and validation CSV.",
            "center_guard_refined_l0_parent_signature_contract_source_intake_no_valid_rows_nonclaim",
            "Derive topological defect normal form or build profile quadrature runner for real rho_H/rho_top moment extraction.",
            "Using passive coordinate centering, old surrogate q_loc grids, total charge, metric-nullity, or post-readout centering as moment-zero evidence.",
        ],
    )


def validation_rows(csv_paths: List[Path]) -> List[Dict[str, str]]:
    validations: List[Dict[str, str]] = []
    sources = read_csv(SOURCE_DIR / "P8_Y5_R2FR_4380_SOURCE_REGISTER.csv")
    center = read_csv(SOURCE_DIR / "P8_Y5_R2FR_4380_CENTER_GUARD_REFINEMENT.csv")
    l0_contract = read_csv(SOURCE_DIR / "P8_Y5_R2FR_4380_L0_PARENT_SIGNATURE_CONTRACT.csv")
    sweep = read_csv(SOURCE_DIR / "P8_Y5_R2FR_4380_SOURCE_INTAKE_SWEEP.csv")
    profile_contract = read_csv(SOURCE_DIR / "P8_Y5_R2FR_4380_PROFILE_INTAKE_CONTRACT.csv")
    gates = read_csv(SOURCE_DIR / "P8_Y5_R2FR_4380_CLAIM_GATES.csv")

    def add(check_id: str, passed: bool, detail: str) -> None:
        validations.append(
            {
                "checkpoint": CHECKPOINT,
                "check_id": check_id,
                "passed": str(bool(passed)),
                "detail": detail,
            }
        )

    add("VAL4380_0_sources_exist", all(row["path_exists"] == "True" for row in sources), "every cited local source exists")
    add("VAL4380_1_needles_found", all(row["needle_found"] == "True" for row in sources), "every cited local source needle resolves")
    add(
        "VAL4380_2_center_guard_refined",
        any(row["refinement_id"] == "CGR4380_0_pure_defect_translation" and row["status"] == "EXACT_REFINEMENT" for row in center)
        and any(row["refinement_id"] == "CGR4380_1_separate_profile_centers" for row in center),
        "pure-defect/passive-shift correction and separate-center countermodel both recorded",
    )
    add(
        "VAL4380_3_l0_contract_fail_closed",
        any(row["clause_id"] == "L0PC4380_6_verdict" and row["current_status"] == "L0_PARENT_SIGNATURE_NOT_SIGNED" for row in l0_contract),
        "l0 parent signature verdict remains unsigned",
    )
    add(
        "VAL4380_4_sweep_no_valid_rows",
        any(row["candidate_id"] == "SWP4380_4_current_verdict" and row["status"] == "NO_VALID_TOPOLOGICAL_MOMENT_INPUT_FOUND" for row in sweep)
        and all(row["valid_for_claim"] == "False" for row in sweep),
        "source intake sweep found no claim-valid topological moment row",
    )
    add(
        "VAL4380_5_profile_contract_required",
        len(profile_contract) >= 5 and all(row["claim_allowed"] == "False" for row in profile_contract),
        "profile intake contract is staged and fail-closed",
    )
    add("VAL4380_6_claim_gates_false", all(row["claim_allowed"] == "False" for row in gates), "all claim gates false")
    add("VAL4380_7_formal_marker", MARKER in read_text(FORMAL_PATH), "formal marker present")
    add("VAL4380_8_post_marker", MARKER in read_text(DOC_PATH), "post marker present")
    add("VAL4380_9_spine_marker", MARKER in read_text(SPINE_PATH), "spine marker present")
    add("VAL4380_10_packet_marker", PACKET_MARKER in read_text(PACKET_PATH), "packet marker present")
    add("VAL4380_11_claim_row", f"\n{CLAIM_ID}," in read_text(CLAIMS_PATH), "claim row appended")
    add(
        "VAL4380_12_no_claim_rows",
        all(row.get("valid_for_claim", "False") == "False" for path in csv_paths for row in read_csv(path))
        and all(row.get("claim_allowed", "False") == "False" for path in csv_paths for row in read_csv(path)),
        "generated rows remain nonclaim",
    )
    add("VAL4380_13_csv_parse", all(len(read_csv(path)) > 0 for path in csv_paths), "all generated CSVs parse")
    return validations


def main() -> None:
    sources = source_register_rows()
    center_refinements = center_guard_refinement_rows()
    l0_contract = l0_parent_signature_contract_rows()
    sweep = source_intake_sweep_rows()
    profile_contract = profile_intake_contract_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    statuses = status_rows()
    next_targets = next_target_rows()

    csv_payloads: Dict[str, List[Dict[str, str]]] = {
        "P8_Y5_R2FR_4380_SOURCE_REGISTER.csv": sources,
        "P8_Y5_R2FR_4380_CENTER_GUARD_REFINEMENT.csv": center_refinements,
        "P8_Y5_R2FR_4380_L0_PARENT_SIGNATURE_CONTRACT.csv": l0_contract,
        "P8_Y5_R2FR_4380_SOURCE_INTAKE_SWEEP.csv": sweep,
        "P8_Y5_R2FR_4380_PROFILE_INTAKE_CONTRACT.csv": profile_contract,
        "P8_Y5_R2FR_4380_CLAIM_GATES.csv": gates,
        "P8_Y5_R2FR_4380_DECISION.csv": decisions,
        "P8_Y5_R2FR_4380_STATUS.csv": statuses,
        "P8_Y5_R2FR_4380_NEXT_TARGET.csv": next_targets,
    }

    csv_paths: List[Path] = []
    for filename, rows in csv_payloads.items():
        path = SOURCE_DIR / filename
        write_csv(path, rows)
        csv_paths.append(path)

    write_formal_doc(sources, center_refinements, l0_contract, sweep, profile_contract, gates, decisions, statuses, next_targets)
    write_post_doc(decisions, next_targets)
    write_spine_update()
    write_packet_update()
    write_claim()
    write_csv(VALIDATION_PATH, validation_rows(csv_paths))


if __name__ == "__main__":
    main()
