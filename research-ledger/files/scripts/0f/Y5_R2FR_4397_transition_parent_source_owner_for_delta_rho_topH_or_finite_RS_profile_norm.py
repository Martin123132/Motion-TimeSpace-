from __future__ import annotations

import csv
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Tuple

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from sigma_s_RS_bound_runner import evaluate_bound_rows, read_csv, write_csv  # noqa: E402
from sigma_s_RS_source_row_gate import evaluate_source_rows  # noqa: E402
from sigma_s_source_owner_improvement_gate import evaluate_owner_rows  # noqa: E402


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4397"
CLAIM_ID = "L-238"
MARKER = "PPC4161_TRANSITION_PARENT_SOURCE_OWNER_FOR_DELTA_RHO_TOPH_OR_FINITE_RS_PROFILE_NORM_4397"
PACKET_MARKER = "PPC4161_PACKET_TRANSITION_PARENT_SOURCE_OWNER_FOR_DELTA_RHO_TOPH_OR_FINITE_RS_PROFILE_NORM_4397"
DECISION = "SOURCE_OWNER_IMPROVEMENT_ROUTE_DERIVED_PARENT_AUTHORITY_UNSIGNED"
NEXT_TARGET = "4398-Y5-R2FR-transition-Ward-exchange-current-for-electric-U-or-finite-RS-profile-norm.md"

FORMAL_PATH = FORMAL / "413-PPC4161-transition-parent-source-owner-for-delta-rho-topH-or-finite-RS-profile-norm.md"
DOC_PATH = POST / "4397-Y5-R2FR-transition-parent-source-owner-for-delta-rho-topH-or-finite-RS-profile-norm.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4397_VALIDATION.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

OWNER_INPUT_PATH = SOURCE_DIR / "P8_Y5_R2FR_4397_SOURCE_OWNER_IMPROVEMENT_INPUT.csv"
OWNER_OUTPUT_PATH = SOURCE_DIR / "P8_Y5_R2FR_4397_SOURCE_OWNER_IMPROVEMENT_OUTPUT.csv"
SOURCE_ROW_INPUT_PATH = SOURCE_DIR / "P8_Y5_R2FR_4397_RS_SOURCE_ROW_GATE_INPUT.csv"
SOURCE_ROW_OUTPUT_PATH = SOURCE_DIR / "P8_Y5_R2FR_4397_RS_SOURCE_ROW_GATE_OUTPUT.csv"
BOUND_DRY_INPUT_PATH = SOURCE_DIR / "P8_Y5_R2FR_4397_RS_BOUND_RUNNER_DRY_INPUT.csv"
BOUND_DRY_OUTPUT_PATH = SOURCE_DIR / "P8_Y5_R2FR_4397_RS_BOUND_RUNNER_DRY_OUTPUT.csv"

OWNER_GATE_PATH = SCRIPT_DIR / "sigma_s_source_owner_improvement_gate.py"
SOURCE_ROW_GATE_PATH = SCRIPT_DIR / "sigma_s_RS_source_row_gate.py"
BOUND_RUNNER_PATH = SCRIPT_DIR / "sigma_s_RS_bound_runner.py"
STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

SIGMA_THEOREMS_4392 = SOURCE_DIR / "P8_Y5_R2FR_4392_SIGMA_S_THEOREMS.csv"
U_THEOREMS_4390 = SOURCE_DIR / "P8_Y5_R2FR_4390_U_CONSTRUCTION_THEOREMS.csv"
U_PROJECTIONS_4390 = SOURCE_DIR / "P8_Y5_R2FR_4390_COMPONENT_PROJECTIONS.csv"
STATIC_THEOREMS_4391 = SOURCE_DIR / "P8_Y5_R2FR_4391_PARENT_U_S_THEOREMS.csv"
ACTION_THEOREMS_4393 = SOURCE_DIR / "P8_Y5_R2FR_4393_SIGMA_S_ACTION_THEOREMS.csv"
BOUNDARY_OUTPUT_4396 = SOURCE_DIR / "P8_Y5_R2FR_4396_BOUNDARY_ZERO_MODE_OUTPUT.csv"


LOCAL_SOURCES: Dict[str, Tuple[Path, str, str]] = {
    "SRC4397_0_4396_next": (
        SOURCE_DIR / "P8_Y5_R2FR_4396_NEXT_TARGET.csv",
        "4397-Y5-R2FR-transition-parent-source-owner-for-delta-rho-topH-or-finite-RS-profile-norm.md",
        "4396 handoff to parent-own delta rho_topH or compute a finite profile norm.",
    ),
    "SRC4397_1_4396_boundary": (
        BOUNDARY_OUTPUT_4396,
        "BZM4396_0_dirichlet_or_zero_mean_mechanism",
        "4396 boundary/zero-mode mechanism row.",
    ),
    "SRC4397_2_4390_U": (
        U_THEOREMS_4390,
        "U4390_0_electric_projector_ansatz",
        "Electric U superpotential construction.",
    ),
    "SRC4397_3_4390_projection": (
        U_PROJECTIONS_4390,
        "PROJ4390_0_electric_U",
        "Density projection for electric U.",
    ),
    "SRC4397_4_4392_sigma": (
        SIGMA_THEOREMS_4392,
        "SIGS4392_0_trace_electric_owner",
        "Sigma_S trace-electric owner route.",
    ),
    "SRC4397_5_4393_action": (
        ACTION_THEOREMS_4393,
        "SACT4393_0_parent_constraint_signature",
        "Sigma/lambda action signature.",
    ),
    "SRC4397_6_4391_tau": (
        STATIC_THEOREMS_4391,
        "UST4391_0_tau_coframe_u_candidate",
        "Same tau/coframe candidate.",
    ),
    "SRC4397_7_owner_gate": (
        OWNER_GATE_PATH,
        "def evaluate_owner_rows",
        "New source-owner improvement gate.",
    ),
    "SRC4397_8_source_gate": (
        SOURCE_ROW_GATE_PATH,
        "def evaluate_source_rows",
        "Existing R_S source-row gate.",
    ),
    "SRC4397_9_bound_runner": (
        BOUND_RUNNER_PATH,
        "def evaluate_bound_rows",
        "Existing tightened R_S bound runner.",
    ),
}


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def append_once(path: Path, marker: str, block: str) -> None:
    text = read_text(path)
    if marker in text:
        return
    if text and not text.endswith("\n"):
        text += "\n"
    write_text(path, text + block)


def append_claim_once(path: Path, claim_id: str, row: List[str]) -> None:
    text = read_text(path)
    if f"\n{claim_id}," in text:
        return
    if text and not text.endswith("\n"):
        text += "\n"
        write_text(path, text)
    with path.open("a", newline="", encoding="utf-8") as handle:
        csv.writer(handle).writerow(row)


def source_register_rows() -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    for source_id, (path, needle, role) in LOCAL_SOURCES.items():
        text = read_text(path)
        rows.append(
            {
                "source_id": source_id,
                "role": role,
                "path": str(path),
                "path_exists": str(path.exists()),
                "needle": needle,
                "needle_found": str(bool(text and needle in text)),
                "valid_for_claim": "False",
            }
        )
    return rows


def improvement_derivation_rows() -> List[Dict[str, str]]:
    return [
        {
            "derivation_id": "SID4397_0_source_owner_equivalence",
            "statement": "A non-ad-hoc parent owner for delta rho_topH is a stress-improvement identity: T_top^{mu nu}-T_H^{mu nu}=nabla_alpha nabla_beta U^{mu alpha nu beta}+E^{mu nu}, with E^{mu nu}=0 or conserved exchange on shell.",
            "derivation": "In field theory Hilbert stresses can differ by identically conserved improvement/superpotential terms without changing total charges under boundary silence. The 4390 electric U gives exactly the required double-divergence density slot.",
            "new_information": "delta rho_topH should be treated as an improvement-source object, not an arbitrary fitted density.",
            "valid_for_claim": "False",
        },
        {
            "derivation_id": "SID4397_1_electric_U_sigma_link",
            "statement": "For the electric projector, U^{0i0j}=S^{ij}; with S^{ij}=c^2 h^{ij} sigma_S, the leading density improvement is c^-2D_iD_jS^{ij}=Delta_h sigma_S.",
            "derivation": "This combines 4390 U^{0i0j}=S^{ij}, 4392 S^{ij}=c^2h^{ij}sigma_S, and 4393 Delta_h sigma_S=delta rho_topH. If all are parent-owned on the same support, the improvement owns R_S=0.",
            "new_information": "The local-GR route is now a single chain: stress improvement -> electric U -> trace sigma -> elliptic boundary certificate.",
            "valid_for_claim": "False",
        },
        {
            "derivation_id": "SID4397_2_charge_silence",
            "statement": "The Newtonian mass charge is unchanged by the improvement only if the boundary flux/corner terms vanish or are parent-fixed.",
            "derivation": "Integrating D_iD_jS^{ij} over W_H gives boundary pairings. If these are not silent, the improvement can move mass into boundary hair rather than disappear locally.",
            "new_information": "Boundary silence is not bookkeeping; it decides whether the improvement is local source reshuffling or new exterior charge.",
            "valid_for_claim": "False",
        },
        {
            "derivation_id": "SID4397_3_ward_ceiling",
            "statement": "The improvement route cannot claim local GR until nabla_mu DeltaT_U^{mu nu}=0 or a parent exchange current is included.",
            "derivation": "Bianchi consistency requires the total stress that sources the metric to be conserved. A fixed post-readout U would violate the Ward gate; parent U/S equations or exchange current are mandatory.",
            "new_information": "The next sharp target is Ward/exchange current for electric U/S, not another broad source sweep.",
            "valid_for_claim": "False",
        },
    ]


def owner_input_rows() -> List[Dict[str, str]]:
    return [
        {
            "candidate_id": "SO4397_0_electric_U_improvement_route",
            "route": "delta_rho_topH_as_electric_U_stress_improvement",
            "parent_delta_source_declared": "False",
            "topological_density_before_readout": "False",
            "hilbert_density_before_readout": "False",
            "common_tau_coframe_support": "False",
            "stress_improvement_U_owned": "False",
            "riemann_symmetry_or_electric_projector": "True",
            "deltaT_double_divergence_identity": "True",
            "density_projection_matches_delta_rho": "True",
            "sigma_constraint_links_improvement": "True",
            "ward_conservation_or_exchange_current": "False",
            "boundary_mass_silence": "False",
            "em_double_count_guard": "False",
            "no_post_readout_fit": "True",
            "parent_authority": "CONDITIONAL_IMPROVEMENT_OWNER_NOT_PARENT_SIGNED",
            "source_path": str(U_THEOREMS_4390),
            "input_valid_for_claim": "False",
            "notes": "Mechanism row: improvement algebra is available, but parent source owner and Ward/boundary authority are unsigned.",
        },
        {
            "candidate_id": "SO4397_1_sigma_constraint_link",
            "route": "sigma_lambda_links_improvement_density_to_delta_rho_topH",
            "parent_delta_source_declared": "False",
            "topological_density_before_readout": "False",
            "hilbert_density_before_readout": "False",
            "common_tau_coframe_support": "False",
            "stress_improvement_U_owned": "False",
            "riemann_symmetry_or_electric_projector": "True",
            "deltaT_double_divergence_identity": "True",
            "density_projection_matches_delta_rho": "True",
            "sigma_constraint_links_improvement": "True",
            "ward_conservation_or_exchange_current": "False",
            "boundary_mass_silence": "False",
            "em_double_count_guard": "False",
            "no_post_readout_fit": "True",
            "parent_authority": "CONDITIONAL_SIGMA_IMPROVEMENT_LINK_NOT_PARENT_SIGNED",
            "source_path": str(ACTION_THEOREMS_4393),
            "input_valid_for_claim": "False",
            "notes": "Shows the sigma constraint is the right interface if parent ownership is supplied later.",
        },
        {
            "candidate_id": "SO4397_2_future_parent_signed_template",
            "route": "future_parent_signed_source_owner_certificate",
            "parent_delta_source_declared": "False",
            "topological_density_before_readout": "False",
            "hilbert_density_before_readout": "False",
            "common_tau_coframe_support": "False",
            "stress_improvement_U_owned": "False",
            "riemann_symmetry_or_electric_projector": "True",
            "deltaT_double_divergence_identity": "True",
            "density_projection_matches_delta_rho": "True",
            "sigma_constraint_links_improvement": "True",
            "ward_conservation_or_exchange_current": "False",
            "boundary_mass_silence": "False",
            "em_double_count_guard": "False",
            "no_post_readout_fit": "True",
            "parent_authority": "MISSING_PARENT_SIGNED_SOURCE_OWNER_IMPROVEMENT",
            "source_path": str(U_PROJECTIONS_4390),
            "input_valid_for_claim": "False",
            "notes": "Template for the exact parent authority row needed to turn conditional R_S zero into a claim.",
        },
    ]


def source_row_input_rows() -> List[Dict[str, str]]:
    return [
        {
            "candidate_id": "RS4397_0_improvement_source_owner_conditional_zero",
            "target": "conditional_R_S_zero_from_stress_improvement_owner",
            "theorem_zero": "True",
            "theorem_zero_authority": "CONDITIONAL_IMPROVEMENT_SOURCE_OWNER_NOT_PARENT_SIGNED",
            "R_S_weighted_norm": "0.0",
            "R_S_units": "theorem_zero_dimensionless",
            "M_H": "1.0",
            "M_H_units": "dimensionless_normalized_mass",
            "K_N": "1.0",
            "lambda_stress_score": "0.0",
            "kernel_stress_score": "0.0",
            "delta_threshold": "1e-12",
            "source_path": str(OWNER_OUTPUT_PATH),
            "source_row_id": "SO4397_0_electric_U_improvement_route",
            "equation_ref": "T_top-T_H=nabla nabla U; U^{0i0j}=S^{ij}; S^{ij}=c^2h^{ij}sigma_S; R_S=0 if parent-owned",
            "W_H_geometry_source": str(SIGMA_THEOREMS_4392),
            "same_tau_coframe_certificate": str(STATIC_THEOREMS_4391),
            "no_cancellation_guard": "True",
            "input_valid_for_claim": "False",
            "notes": "Source-backed conditional theorem-zero row for the improvement route.",
        },
        {
            "candidate_id": "RS4397_1_finite_profile_norm_needed_if_Ward_fails",
            "target": "finite_R_S_profile_norm_if_improvement_owner_fails",
            "theorem_zero": "False",
            "theorem_zero_authority": "NONE",
            "R_S_weighted_norm": "MISSING_NUMERIC_PROFILE_NORM",
            "R_S_units": "MISSING_R_S_UNITS",
            "M_H": "MISSING_M_H",
            "M_H_units": "MISSING_M_H_UNITS",
            "K_N": "MISSING_K_N",
            "lambda_stress_score": "MISSING_LAMBDA_STRESS_SCORE",
            "kernel_stress_score": "MISSING_KERNEL_STRESS_SCORE",
            "delta_threshold": "MISSING_DELTA_THRESHOLD",
            "source_path": str(SIGMA_THEOREMS_4392),
            "source_row_id": "SIGS4392_4_residual_mismatch_bound",
            "equation_ref": "finite profile norm fallback if source-owner improvement cannot be parent-signed",
            "W_H_geometry_source": str(SIGMA_THEOREMS_4392),
            "same_tau_coframe_certificate": str(STATIC_THEOREMS_4391),
            "no_cancellation_guard": "False",
            "input_valid_for_claim": "False",
            "notes": "Numeric fallback row remains open.",
        },
    ]


def bound_dry_input_rows(source_rows: List[Dict[str, str]]) -> List[Dict[str, str]]:
    fields = [
        "candidate_id",
        "target",
        "theorem_zero",
        "theorem_zero_authority",
        "R_S_weighted_norm",
        "M_H",
        "K_N",
        "lambda_stress_score",
        "kernel_stress_score",
        "delta_threshold",
        "source_path",
        "equation_ref",
        "no_cancellation_guard",
        "input_valid_for_claim",
    ]
    return [{field: row.get(field, "") for field in fields} for row in source_rows]


def claim_gate_rows() -> List[Dict[str, str]]:
    reasons = {
        "source_owner_improvement": "improvement algebra is derived, but parent delta-source, U ownership, Ward/exchange, boundary silence and EM guard are unsigned",
        "conditional_R_S_zero": "source-backed conditional theorem-zero row exists but theorem_zero_authority is not PARENT_SIGNED",
        "finite_profile_norm": "numeric R_S profile norm and stress payload scores remain missing",
        "Newton_local_GR": "without source-owner or finite bound, Newton/local-GR reduction is not claimable",
        "PPN_R10_WEP_clock": "same support and coupling projection clauses remain upstream nonclaim",
    }
    return [
        {
            "gate_id": f"CG4397_{index}_{arena}",
            "arena": arena,
            "claim_allowed": "False",
            "reason": reason,
            "valid_for_claim": "False",
        }
        for index, (arena, reason) in enumerate(reasons.items())
    ]


def decision_rows() -> List[Dict[str, str]]:
    return [
        {
            "decision_id": "DEC4397_0",
            "decision": DECISION,
            "summary": "4397 derives the cleanest parent source-owner route found so far: delta rho_topH should be owned as a conserved stress-improvement difference between topological and Hilbert source definitions. The electric U projector supplies the double-divergence density slot and sigma_S supplies the trace-electric scalar subcase. This is real progress, but the route remains nonclaim because parent source declarations, U/S ownership, Ward/exchange current, boundary mass silence and EM double-count guard are unsigned.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def status_rows() -> List[Dict[str, str]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "status": DECISION,
            "timestamp_utc": STAMP,
            "summary": "source-owner improvement route derived and gated; conditional R_S zero row remains parent-unsigned.",
            "valid_for_claim": "False",
        }
    ]


def next_target_rows() -> List[Dict[str, str]]:
    return [
        {
            "next_id": "NT4397_0",
            "target": NEXT_TARGET,
            "question": "Can the electric-U improvement satisfy Ward conservation through a parent exchange current, or must we compute finite R_S/profile payloads?",
            "preferred_route": "derive nabla_mu DeltaT_U^{mu nu}=0 or an explicit exchange current from parent U/S equations and boundary terms.",
            "fallback_route": "compute/bound finite R_S weighted norm, lambda stress, kernel stress, pressure/aniso and curvature payloads on one W_H support.",
            "avoid": "claiming the improvement identity without Ward/exchange conservation and boundary mass silence.",
            "valid_for_claim": "False",
        }
    ]


def write_formal_doc(
    sources: List[Dict[str, str]],
    derivations: List[Dict[str, str]],
    owner_output: List[Dict[str, str]],
    source_output: List[Dict[str, str]],
    bound_output: List[Dict[str, str]],
    gates: List[Dict[str, str]],
    decisions: List[Dict[str, str]],
    next_targets: List[Dict[str, str]],
) -> None:
    text = f"""# 413 PPC4161 transition: parent source owner for delta rho_topH or finite R_S profile norm

Marker: `{MARKER}`

## Result

4397 finds the best route for parent-owning `delta rho_topH`:

`T_top^{{mu nu}} - T_H^{{mu nu}} = nabla_alpha nabla_beta U^{{mu alpha nu beta}} + E^{{mu nu}}`.

If `E^{{mu nu}}` is zero or a parent exchange current, and if boundary mass terms are silent, then `rho_top-rho_H` is a stress-improvement source rather than a fitted density. The 4390 electric projector gives `U^{{0i0j}}=S^{{ij}}`; the 4392/4393 sigma route gives `S^{{ij}}=c^2h^{{ij}}sigma_S` and `Delta_h sigma_S=delta rho_topH`.

This is a better ladder rung: the parent source-owner problem is now a Ward/conserved-improvement problem, not a free closure axiom.

## Source Register

| source | exists | needle found | role |
|---|---:|---:|---|
"""
    for row in sources:
        text += f"| `{row['source_id']}` | {row['path_exists']} | {row['needle_found']} | {row['role']} |\n"
    text += "\n## Source-Owner Derivation\n\n"
    for row in derivations:
        text += f"### {row['derivation_id']}\n\n- Statement: {row['statement']}\n- Derivation: {row['derivation']}\n- New information: {row['new_information']}\n\n"
    text += "## Source-Owner Gate Output\n\n"
    for row in owner_output:
        text += f"- `{row['candidate_id']}`: source_owner_ready=`{row['source_owner_ready']}`, improvement_ready=`{row['improvement_ready']}`, conservation_ready=`{row['conservation_ready']}`, owner_certificate_ready=`{row['owner_certificate_ready']}`, authority=`{row['theorem_zero_authority']}`.\n"
    text += "\n## R_S Source-Row Gate Output\n\n"
    for row in source_output:
        text += f"- `{row['candidate_id']}`: schema_ready=`{row['schema_ready']}`, source_ready=`{row['source_ready']}`, ready_for_bound_runner=`{row['ready_for_bound_runner']}`, valid=`{row['valid_for_claim']}`, reasons=`{row['refusal_reasons']}`.\n"
    text += "\n## Bound Runner Dry Output\n\n"
    for row in bound_output:
        text += f"- `{row['candidate_id']}`: pass_bound=`{row['pass_bound']}`, valid=`{row['valid_for_claim']}`, total=`{row['total_score']}`, reasons=`{row['refusal_reasons']}`.\n"
    text += "\n## Claim Gates\n\n"
    for row in gates:
        text += f"- `{row['arena']}`: claim_allowed=`{row['claim_allowed']}` because {row['reason']}.\n"
    text += "\n## Decision\n\n"
    text += f"{decisions[0]['summary']}\n\n"
    text += "## Next Target\n\n"
    text += f"- `{next_targets[0]['target']}`: {next_targets[0]['question']}\n"
    write_text(FORMAL_PATH, text)


def write_post_doc(decisions: List[Dict[str, str]], next_targets: List[Dict[str, str]]) -> None:
    write_text(
        DOC_PATH,
        f"""# 4397 Y5 R2FR: parent source owner for delta rho_topH or finite R_S profile norm

Marker: `{MARKER}`

## Private checkpoint

{decisions[0]['summary']}

## Next

{next_targets[0]['target']}

{next_targets[0]['question']}
""",
    )


def write_spine_update() -> None:
    append_once(
        SPINE_PATH,
        MARKER,
        f"""
## 4397 local spine update: delta rho as stress improvement

Marker: `{MARKER}`

Spine update: the parent-owner route for `delta rho_topH` is now a conserved stress-improvement route. If `T_top-T_H=nabla nabla U+E` with zero/exchange `E`, boundary mass silence, and same tau/coframe support, then the electric `U` projector and trace `sigma_S` branch can own `R_S=0` without a closure axiom. The open problem is now Ward/exchange conservation and boundary silence for the parent `U/S` sector, or else finite `R_S`/stress norms.
""",
    )


def write_packet_update() -> None:
    append_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""
## 4397 packet update: source-owner improvement route

Marker: `{PACKET_MARKER}`

Packet update: 4397 reframes `delta rho_topH` as a stress-improvement/source-owner problem. No claim fires because the improvement identity lacks parent-signed Ward/exchange, boundary, EM and source support clauses.
""",
    )


def write_claim() -> None:
    append_claim_once(
        CLAIMS_PATH,
        CLAIM_ID,
        [
            CLAIM_ID,
            "local_gr",
            "4397 derives a cleaner parent source-owner route for delta rho_topH: it should be owned as a conserved stress-improvement difference T_top-T_H=nabla nabla U+E between topological and Hilbert source definitions. The electric U projector supplies U^{0i0j}=S^{ij}; the sigma route supplies S^{ij}=c^2h^{ij}sigma_S and Delta_h sigma_S=delta rho_topH. This gives a serious field-theory mechanism for R_S=0 if Ward/exchange current, boundary mass silence, same support, parent U/S ownership and EM double-count guards close. No local-GR/Newton/PPN/R10 claim fires.",
            "4397 source register, source-owner derivation rows, source-owner improvement gate input/output, R_S source-row gate input/output, bound-runner dry input/output, claim gates, decision, status, next target and validation CSV.",
            "delta_rho_topH_as_stress_improvement_route_derived_parent_unsigned_nonclaim",
            "Derive Ward/exchange current for electric U/S or compute finite R_S/profile and stress payload norms.",
            "Claiming improvement identity without conservation, boundary mass silence, same support, parent U/S ownership, or EM double-count guard.",
        ],
    )


def validation_rows(csv_paths: List[Path]) -> List[Dict[str, str]]:
    validations: List[Dict[str, str]] = []
    sources = read_csv(SOURCE_DIR / "P8_Y5_R2FR_4397_SOURCE_REGISTER.csv")
    derivations = read_csv(SOURCE_DIR / "P8_Y5_R2FR_4397_SOURCE_OWNER_DERIVATIONS.csv")
    owner_output = read_csv(OWNER_OUTPUT_PATH)
    source_output = read_csv(SOURCE_ROW_OUTPUT_PATH)
    bound_output = read_csv(BOUND_DRY_OUTPUT_PATH)
    gates = read_csv(SOURCE_DIR / "P8_Y5_R2FR_4397_CLAIM_GATES.csv")

    def add(check_id: str, passed: bool, detail: str) -> None:
        validations.append({"checkpoint": CHECKPOINT, "check_id": check_id, "passed": str(bool(passed)), "detail": detail})

    add("VAL4397_0_sources_exist", all(row["path_exists"] == "True" for row in sources), "every cited source exists")
    add("VAL4397_1_needles_found", all(row["needle_found"] == "True" for row in sources), "every cited needle resolves")
    add("VAL4397_2_improvement_equivalence_written", any(row["derivation_id"] == "SID4397_0_source_owner_equivalence" for row in derivations), "source-owner improvement equivalence derived")
    add("VAL4397_3_U_sigma_link_written", any(row["derivation_id"] == "SID4397_1_electric_U_sigma_link" for row in derivations), "electric U/sigma link derived")
    add("VAL4397_4_Ward_ceiling_written", any(row["derivation_id"] == "SID4397_3_ward_ceiling" for row in derivations), "Ward ceiling stated")
    add("VAL4397_5_owner_gate_nonclaim", all(row["valid_for_claim"] == "False" for row in owner_output), "owner gate rows remain nonclaim")
    add("VAL4397_6_improvement_mechanism_ready", any(row["candidate_id"] == "SO4397_0_electric_U_improvement_route" and row["improvement_ready"] == "True" for row in owner_output), "improvement mechanism row is ready")
    add("VAL4397_7_source_owner_unsigned", any(row["candidate_id"] == "SO4397_0_electric_U_improvement_route" and row["source_owner_ready"] == "False" for row in owner_output), "source owner remains unsigned")
    add("VAL4397_8_conditional_RS_source_backed", any(row["candidate_id"] == "RS4397_0_improvement_source_owner_conditional_zero" and row["schema_ready"] == "True" and row["source_ready"] == "True" for row in source_output), "conditional R_S improvement row is source-backed")
    add("VAL4397_9_source_rows_nonclaim", all(row["valid_for_claim"] == "False" for row in source_output), "source-row gate keeps rows nonclaim")
    add("VAL4397_10_bound_runner_rejects_conditional_zero", any(row["candidate_id"] == "RS4397_0_improvement_source_owner_conditional_zero" and "THEOREM_ZERO_AUTHORITY_NOT_PARENT_SIGNED" in row["refusal_reasons"] for row in bound_output), "bound runner rejects conditional improvement zero")
    add("VAL4397_11_bound_rows_nonclaim", all(row["valid_for_claim"] == "False" for row in bound_output), "bound dry outputs remain nonclaim")
    add("VAL4397_12_claim_gates_false", all(row["claim_allowed"] == "False" for row in gates), "all claim gates false")
    add("VAL4397_13_formal_marker", MARKER in read_text(FORMAL_PATH), "formal marker present")
    add("VAL4397_14_post_marker", MARKER in read_text(DOC_PATH), "post marker present")
    add("VAL4397_15_spine_marker", MARKER in read_text(SPINE_PATH), "spine marker present")
    add("VAL4397_16_packet_marker", PACKET_MARKER in read_text(PACKET_PATH), "packet marker present")
    add("VAL4397_17_claim_row", f"\n{CLAIM_ID}," in read_text(CLAIMS_PATH), "claim row appended")
    add("VAL4397_18_csv_parse", all(len(read_csv(path)) > 0 for path in csv_paths), "all generated CSVs parse")
    add("VAL4397_19_rows_nonclaim", all(row.get("valid_for_claim", "False") == "False" for path in csv_paths for row in read_csv(path)), "generated rows remain nonclaim")
    add("VAL4397_20_owner_gate_exists", OWNER_GATE_PATH.exists() and "def evaluate_owner_rows" in read_text(OWNER_GATE_PATH), "source-owner gate exists")
    add("VAL4397_21_pycache_absent", not (SCRIPT_DIR / "__pycache__").exists(), "scripts __pycache__ absent after generator cleanup")
    return validations


def remove_pycache() -> None:
    pycache = SCRIPT_DIR / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def main() -> None:
    sources = source_register_rows()
    derivations = improvement_derivation_rows()
    owner_inputs = owner_input_rows()
    source_inputs = source_row_input_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    statuses = status_rows()
    next_targets = next_target_rows()

    csv_payloads: Dict[str, List[Dict[str, str]]] = {
        "P8_Y5_R2FR_4397_SOURCE_REGISTER.csv": sources,
        "P8_Y5_R2FR_4397_SOURCE_OWNER_DERIVATIONS.csv": derivations,
        "P8_Y5_R2FR_4397_CLAIM_GATES.csv": gates,
        "P8_Y5_R2FR_4397_DECISION.csv": decisions,
        "P8_Y5_R2FR_4397_STATUS.csv": statuses,
        "P8_Y5_R2FR_4397_NEXT_TARGET.csv": next_targets,
    }

    csv_paths: List[Path] = [OWNER_INPUT_PATH, SOURCE_ROW_INPUT_PATH, BOUND_DRY_INPUT_PATH]
    write_csv(OWNER_INPUT_PATH, owner_inputs)
    owner_output = evaluate_owner_rows(OWNER_INPUT_PATH)
    write_csv(OWNER_OUTPUT_PATH, owner_output)

    write_csv(SOURCE_ROW_INPUT_PATH, source_inputs)
    source_output = evaluate_source_rows(SOURCE_ROW_INPUT_PATH)
    write_csv(SOURCE_ROW_OUTPUT_PATH, source_output)

    bound_inputs = bound_dry_input_rows(source_inputs)
    write_csv(BOUND_DRY_INPUT_PATH, bound_inputs)
    bound_output = evaluate_bound_rows(BOUND_DRY_INPUT_PATH)
    write_csv(BOUND_DRY_OUTPUT_PATH, bound_output)
    csv_paths.extend([OWNER_OUTPUT_PATH, SOURCE_ROW_OUTPUT_PATH, BOUND_DRY_OUTPUT_PATH])

    for filename, rows in csv_payloads.items():
        path = SOURCE_DIR / filename
        write_csv(path, rows)
        csv_paths.append(path)

    write_formal_doc(sources, derivations, owner_output, source_output, bound_output, gates, decisions, next_targets)
    write_post_doc(decisions, next_targets)
    write_spine_update()
    write_packet_update()
    write_claim()
    remove_pycache()
    write_csv(VALIDATION_PATH, validation_rows(csv_paths))


if __name__ == "__main__":
    main()
