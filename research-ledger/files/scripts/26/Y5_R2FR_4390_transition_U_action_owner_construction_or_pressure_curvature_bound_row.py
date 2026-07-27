from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Tuple

SCRIPT_DIR = Path(__file__).resolve().parent
import sys

if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from u_action_owner_gate import evaluate_u_owner_rows, read_csv, write_csv  # noqa: E402


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4390"
CLAIM_ID = "L-231"
MARKER = "PPC4161_TRANSITION_U_ACTION_OWNER_CONSTRUCTION_OR_PRESSURE_CURVATURE_BOUND_ROW_4390"
PACKET_MARKER = "PPC4161_PACKET_TRANSITION_U_ACTION_OWNER_CONSTRUCTION_OR_PRESSURE_CURVATURE_BOUND_ROW_4390"
DECISION = "ELECTRIC_U_PROJECTOR_DERIVED_SCALAR_TRACE_REJECTED_OWNER_PAYLOAD_GATES_OPEN_NONCLAIM"
NEXT_TARGET = "4391-Y5-R2FR-transition-electric-U-parent-sector-or-static-time-silence-proof.md"

FORMAL_PATH = FORMAL / "406-PPC4161-transition-U-action-owner-construction-or-pressure-curvature-bound-row.md"
DOC_PATH = POST / "4390-Y5-R2FR-transition-U-action-owner-construction-or-pressure-curvature-bound-row.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4390_VALIDATION.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
GATE_RUNNER_PATH = SCRIPT_DIR / "u_action_owner_gate.py"
GATE_INPUT_PATH = SOURCE_DIR / "P8_Y5_R2FR_4390_U_OWNER_GATE_INPUT.csv"
GATE_OUTPUT_PATH = SOURCE_DIR / "P8_Y5_R2FR_4390_U_OWNER_GATE_OUTPUT.csv"
STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()


LOCAL_SOURCES: Dict[str, Tuple[Path, str, str]] = {
    "SRC4390_0_4389_next": (
        SOURCE_DIR / "P8_Y5_R2FR_4389_NEXT_TARGET.csv",
        "4390-Y5-R2FR-transition-U-action-owner-construction-or-pressure-curvature-bound-row.md",
        "Explicit 4390 handoff.",
    ),
    "SRC4390_1_4389_payload": (
        SOURCE_DIR / "P8_Y5_R2FR_4389_ADOPTION_THEOREMS.csv",
        "AD4389_1_no_pure_00_closure",
        "No density-only action adoption.",
    ),
    "SRC4390_2_4389_components": (
        SOURCE_DIR / "P8_Y5_R2FR_4389_COMPONENT_PAYLOADS.csv",
        "PAY4389_2_pressure_aniso",
        "Pressure/anisotropy payload that must be killed or bounded.",
    ),
    "SRC4390_3_4388_action": (
        SOURCE_DIR / "P8_Y5_R2FR_4388_ACTION_TEMPLATES.csv",
        "ACT4388_0_curvature_coupled_improvement",
        "Curvature-coupled U action template.",
    ),
    "SRC4390_4_4387_density": (
        SOURCE_DIR / "P8_Y5_R2FR_4387_IMPROVEMENT_OWNER_THEOREMS.csv",
        "IO4387_1_newtonian_density_projection",
        "Weak-static density projection target.",
    ),
    "SRC4390_5_gate_runner": (
        GATE_RUNNER_PATH,
        "REQUIRED_FIELDS",
        "Executable U/action-owner gate.",
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
    with path.open("a", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(row)


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


def theorem_rows() -> List[Dict[str, str]]:
    return [
        {
            "theorem_id": "U4390_0_electric_projector_ansatz",
            "statement": "A covariant electric-projector superpotential can be built from a unit local flow u^mu and a symmetric transverse spatial tensor S^{mu nu}: U^{mu alpha nu beta}=u^mu u^nu S^{alpha beta}-u^alpha u^nu S^{mu beta}-u^mu u^beta S^{alpha nu}+u^alpha u^beta S^{mu nu}.",
            "derivation": "With u_mu S^{mu nu}=0 and S^{mu nu}=S^{nu mu}, the ansatz is antisymmetric in each index pair and symmetric under pair exchange. In the local rest frame it leaves the electric Riemann slot U^{0i0j}=S^{ij} as the leading source-bearing component.",
            "effect": "This is the first concrete owner candidate for the 4387 U rather than a generic missing-source note.",
            "status": "EXACT_COVARIANT_CANDIDATE_DERIVED_OWNER_UNSIGNED",
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "U4390_1_static_component_split",
            "statement": "For the electric-projector candidate, the weak-static local rest-frame split can keep the useful density operator while pushing leading pressure/aniso into time-derivative, curvature, boundary, and metric-dependence payloads.",
            "derivation": "The density projection sees Delta rho ~ c^{-2} partial_i partial_j S^{ij}. The ij improvement channel sees terms of the schematic type partial_0 partial_0 S^{ij} plus curvature/variation payloads, so a truly static parent branch can suppress leading anisotropic stress without deleting the density operator.",
            "effect": "This is the real leap: density does not have to come with same-order spatial pressure if U is electric-type rather than scalar trace.",
            "status": "CONDITIONAL_LOCAL_GR_ROUTE_OPEN_STATIC_OWNER_REQUIRED",
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "U4390_2_scalar_trace_subcase_rejected_for_local_closure",
            "statement": "The scalar trace subcase U ~ phi(g g-g g), equivalently phi R, is a poor local-GR closure route because its ij stress is same spatial-derivative order as its density source.",
            "derivation": "In the weak static limit, (g_{mu nu}Box-nabla_mu nabla_nu)phi gives Delta T_00 ~ -nabla^2 phi, but Delta T_ij ~ delta_ij nabla^2 phi-partial_i partial_j phi. The pressure/anisotropy payload is therefore not automatically small.",
            "effect": "The low-scrutiny route is not phi R; it is the electric U projector or explicit stress bounds.",
            "status": "SCALAR_TRACE_DEMOTED_TO_BOUND_OR_SCREENED_BRANCH",
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "U4390_3_owner_not_optional",
            "statement": "The electric projector only helps if u^mu and S^{mu nu} are parent-owned MTS fields with equations of motion, quotient descent, and pre-readout residual identity.",
            "derivation": "An externally inserted U violates the 4389 Ward/conservation gate. A post-readout S^{ij} fitted to the density would reproduce the forbidden closure move.",
            "effect": "The next derivation target is a parent sector, not another broad source sweep.",
            "status": "PARENT_SECTOR_REQUIRED_NOT_FILLED",
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "U4390_4_fallback_bound_rows",
            "statement": "If the parent electric-projector sector cannot be signed, the exact fallback is not to abandon the route but to source numerical bounds for pressure/aniso, curvature remainder, time-silence, boundary pairings, and exchange current.",
            "derivation": "These are precisely the open payloads isolated by 4389 and separated by the 4390 component split.",
            "effect": "Turns the remaining danger into a finite bound table instead of vibes.",
            "status": "BOUND_FALLBACK_ROWS_STAGED",
            "valid_for_claim": "False",
        },
    ]


def projection_rows() -> List[Dict[str, str]]:
    return [
        {
            "projection_id": "PROJ4390_0_electric_U",
            "branch": "electric_projector_U",
            "U_form": "U^{mu alpha nu beta}=u^mu u^nu S^{alpha beta}-u^alpha u^nu S^{mu beta}-u^mu u^beta S^{alpha nu}+u^alpha u^beta S^{mu nu}",
            "rest_frame_slot": "U^{0i0j}=S^{ij}; spatial S is transverse to u",
            "density_leading": "Delta rho ~ c^{-2} partial_i partial_j S^{ij}",
            "momentum_leading": "Delta T^{0i} suppressed by stationarity/no-flux clauses",
            "pressure_aniso_leading": "Delta T^{ij} ~ partial_0 partial_0 S^{ij} plus curvature/metric-dependence payloads",
            "safe_condition": "parent-owned static branch + time-silence + Ward + curvature/boundary bounds",
            "verdict": "BEST_CONSTRUCTION_ROUTE_NOT_CLAIM",
            "valid_for_claim": "False",
        },
        {
            "projection_id": "PROJ4390_1_scalar_phiR",
            "branch": "scalar_trace_phi_R",
            "U_form": "U^{mu alpha nu beta}=phi(g^{mu nu}g^{alpha beta}-g^{mu beta}g^{alpha nu})",
            "rest_frame_slot": "isotropic trace, not an electric-only slot",
            "density_leading": "Delta T_00 ~ -nabla^2 phi",
            "momentum_leading": "static branch can suppress 0i but not enough",
            "pressure_aniso_leading": "Delta T_ij ~ delta_ij nabla^2 phi-partial_i partial_j phi",
            "safe_condition": "requires screening/large coupling limit or explicit PPN stress bound",
            "verdict": "DEMOTED_FOR_LOCAL_GR_CLOSURE",
            "valid_for_claim": "False",
        },
        {
            "projection_id": "PROJ4390_2_generic_U",
            "branch": "generic_U",
            "U_form": "unprojected U^{mu alpha nu beta}",
            "rest_frame_slot": "all components may participate",
            "density_leading": "can contain desired partial_i partial_j U^{0i0j}",
            "momentum_leading": "uncontrolled mixed components",
            "pressure_aniso_leading": "uncontrolled spatial and time slots",
            "safe_condition": "must be reduced to electric projector or bounded component by component",
            "verdict": "TOO_BROAD_FOR_LOW_SCRUTINY_ROUTE",
            "valid_for_claim": "False",
        },
    ]


def gate_input_rows() -> List[Dict[str, str]]:
    script_path = str(Path(__file__).resolve())
    return [
        {
            "candidate_id": "UOWN4390_0_electric_projector_candidate",
            "branch": "electric_projector_U",
            "parent_action_owner_signed": "False",
            "u_field_owner_signed": "False",
            "s_field_owner_signed": "False",
            "riemann_symmetry_signed": "True",
            "transverse_symmetric_s_signed": "True",
            "electric_projector_identity_signed": "True",
            "residual_density_identity_signed": "True",
            "static_branch_signed": "False",
            "time_derivative_silence_signed": "False",
            "pressure_aniso_zero_or_bounded": "False",
            "curvature_remainder_zero_or_bounded": "False",
            "affine_boundary_pairings_pass": "False",
            "ward_conservation_owned": "False",
            "matter_coupling_quotient_owned": "False",
            "em_double_count_guard_signed": "True",
            "source_path": script_path,
        },
        {
            "candidate_id": "UOWN4390_1_scalar_trace_phiR",
            "branch": "scalar_trace_phi_R",
            "parent_action_owner_signed": "False",
            "u_field_owner_signed": "False",
            "s_field_owner_signed": "False",
            "riemann_symmetry_signed": "True",
            "transverse_symmetric_s_signed": "False",
            "electric_projector_identity_signed": "False",
            "residual_density_identity_signed": "True",
            "static_branch_signed": "False",
            "time_derivative_silence_signed": "False",
            "pressure_aniso_zero_or_bounded": "False",
            "curvature_remainder_zero_or_bounded": "False",
            "affine_boundary_pairings_pass": "False",
            "ward_conservation_owned": "False",
            "matter_coupling_quotient_owned": "False",
            "em_double_count_guard_signed": "True",
            "source_path": script_path,
        },
        {
            "candidate_id": "UOWN4390_2_generic_U_fallback",
            "branch": "generic_U_bound_fallback",
            "parent_action_owner_signed": "False",
            "u_field_owner_signed": "False",
            "s_field_owner_signed": "False",
            "riemann_symmetry_signed": "False",
            "transverse_symmetric_s_signed": "False",
            "electric_projector_identity_signed": "False",
            "residual_density_identity_signed": "False",
            "static_branch_signed": "False",
            "time_derivative_silence_signed": "False",
            "pressure_aniso_zero_or_bounded": "False",
            "curvature_remainder_zero_or_bounded": "False",
            "affine_boundary_pairings_pass": "False",
            "ward_conservation_owned": "False",
            "matter_coupling_quotient_owned": "False",
            "em_double_count_guard_signed": "False",
            "source_path": script_path,
        },
    ]


def bound_rows() -> List[Dict[str, str]]:
    return [
        {
            "bound_id": "BND4390_0_time_silence",
            "arena": "local_static_source",
            "quantity": "partial_0 partial_0 S^{ij} / partial_k partial_l S^{kl}",
            "needed_bound": "must be negligible for Solar/local PPN branch or parent-proven zero",
            "source_path": "MISSING_PARENT_STATIC_BRANCH_OR_NUMERIC_BOUND",
            "status": "SOURCE_OR_PROOF_REQUIRED",
            "valid_for_claim": "False",
        },
        {
            "bound_id": "BND4390_1_pressure_aniso",
            "arena": "PPN",
            "quantity": "Delta T^{ij}_U anisotropic projection",
            "needed_bound": "must not shift gamma/beta/preferred-frame observables beyond baseline tolerances",
            "source_path": "MISSING_PPN_PROJECTION_BOUND",
            "status": "SOURCE_OR_PROOF_REQUIRED",
            "valid_for_claim": "False",
        },
        {
            "bound_id": "BND4390_2_curvature_remainder",
            "arena": "local_weak_curvature",
            "quantity": "curvature commutator and algebraic U*R residuals",
            "needed_bound": "must be small compared with leading Newtonian density term or parent-cancelled",
            "source_path": "MISSING_CURVATURE_REMAINDER_BOUND",
            "status": "SOURCE_OR_PROOF_REQUIRED",
            "valid_for_claim": "False",
        },
        {
            "bound_id": "BND4390_3_affine_boundary",
            "arena": "affine_center_closure",
            "quantity": "boundary pairings generated by integrations by parts",
            "needed_bound": "must vanish for affine tests 1,x,y,z on the local support",
            "source_path": "MISSING_BOUNDARY_PAIRING_ROWS",
            "status": "SOURCE_OR_PROOF_REQUIRED",
            "valid_for_claim": "False",
        },
        {
            "bound_id": "BND4390_4_ward_exchange",
            "arena": "Bianchi_conservation",
            "quantity": "nabla_mu Delta T_U^{mu nu} or exchange current into U/S equations",
            "needed_bound": "must vanish on shell or be included in a conserved total stress",
            "source_path": "MISSING_WARD_OR_EXCHANGE_ROW",
            "status": "SOURCE_OR_PROOF_REQUIRED",
            "valid_for_claim": "False",
        },
    ]


def route_rows() -> List[Dict[str, str]]:
    return [
        {
            "route_id": "ROUTE4390_0_electric_projector",
            "route": "construct parent electric U sector",
            "why": "It can separate spatial density derivatives from leading static ij pressure in a way scalar phiR cannot.",
            "status": "BEST_NEXT_ROUTE_OPEN",
            "valid_for_claim": "False",
        },
        {
            "route_id": "ROUTE4390_1_scalar_phiR",
            "route": "use scalar phiR trace improvement",
            "why": "Same-order pressure/aniso appears in weak-static projection.",
            "status": "DEMOTED_UNLESS_SCREENED_OR_BOUND",
            "valid_for_claim": "False",
        },
        {
            "route_id": "ROUTE4390_2_bound_rows",
            "route": "fill pressure/curvature/time/boundary/Ward bound rows",
            "why": "Required if the parent electric U derivation stalls.",
            "status": "FALLBACK_ROWS_STAGED",
            "valid_for_claim": "False",
        },
    ]


def claim_gate_rows() -> List[Dict[str, str]]:
    gates = [
        ("local_GR", "electric U parent owner and payload gates still open"),
        ("newtonian_limit", "density operator promising but not parent-identified with rho_top-rho_H"),
        ("PPN", "pressure/aniso and time-silence bounds missing"),
        ("clock", "U/S coupling to clock matter not quotient-owned"),
        ("orbital", "curvature/boundary residuals not bounded"),
        ("R10", "local coupling coefficients remain unsigned"),
    ]
    return [
        {
            "gate_id": f"GATE4390_{index}_{name}",
            "arena": name,
            "claim_allowed": "False",
            "reason": reason,
            "valid_for_claim": "False",
        }
        for index, (name, reason) in enumerate(gates)
    ]


def decision_rows() -> List[Dict[str, str]]:
    return [
        {
            "decision_id": "DEC4390_0",
            "decision": DECISION,
            "summary": "4390 constructs a concrete electric-projector U candidate. This is a forward step: U^{0i0j}=S^{ij} can own the double-divergence density while static ij pressure is moved to time/curvature/metric payloads. Scalar phiR is demoted because its pressure/aniso is same spatial-derivative order as density.",
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
            "summary": "Best route now is a parent-owned electric U/S/u sector; open gates are parent owner, static time-silence, pressure/aniso bound, curvature bound, boundary pairings, Ward conservation, and quotient matter coupling.",
            "valid_for_claim": "False",
        }
    ]


def next_target_rows() -> List[Dict[str, str]]:
    return [
        {
            "next_id": "NT4390_0",
            "target": NEXT_TARGET,
            "question": "Can MTS parent variables supply u^mu and S^{mu nu} as quotient-owned transverse fields with a static/time-silent branch and Ward conservation?",
            "preferred_route": "derive parent electric U/S/u action sector from existing motion-time-space variables and show the local static branch kills Delta T^{ij} at leading order.",
            "fallback_route": "fill real pressure/aniso, curvature, boundary, and Ward exchange bound rows.",
            "avoid": "returning to scalar phiR as a local-GR claim or treating the electric projector as a fitted post-readout S^{ij}.",
            "valid_for_claim": "False",
        }
    ]


def write_formal_doc(
    sources: List[Dict[str, str]],
    theorems: List[Dict[str, str]],
    projections: List[Dict[str, str]],
    gate_output: List[Dict[str, str]],
    bounds: List[Dict[str, str]],
    routes: List[Dict[str, str]],
    gates: List[Dict[str, str]],
    decisions: List[Dict[str, str]],
    statuses: List[Dict[str, str]],
    next_targets: List[Dict[str, str]],
) -> None:
    text = f"""# 406 PPC4161 transition: U action owner construction or pressure-curvature bound row

Marker: `{MARKER}`

## Result

4390 does not just circle the missing input. It constructs the next serious candidate:

`U^{{mu alpha nu beta}} = u^mu u^nu S^{{alpha beta}} - u^alpha u^nu S^{{mu beta}} - u^mu u^beta S^{{alpha nu}} + u^alpha u^beta S^{{mu nu}}`,

with `u_mu S^{{mu nu}}=0` and `S^{{mu nu}}=S^{{nu mu}}`.

In the local rest frame this gives `U^{{0i0j}}=S^{{ij}}`. That is exactly the slot needed by the 4387 density projection:

`Delta rho ~ c^-2 partial_i partial_j S^{{ij}}`.

The important win is that this electric-projector branch is not the same as scalar `phi R`. For scalar `phi R`, the weak-static `ij` piece is `delta_ij nabla^2 phi - partial_i partial_j phi`, so pressure/anisotropy is same derivative order as the density. For the electric branch, the leading `ij` payload is pushed into `partial_0 partial_0 S^{{ij}}` plus curvature, metric-dependence, boundary, and Ward terms. That is not closed yet, but it is a better route.

## Source Register

| source | exists | needle found | role |
|---|---:|---:|---|
"""
    for row in sources:
        text += f"| `{row['source_id']}` | {row['path_exists']} | {row['needle_found']} | {row['role']} |\n"
    text += "\n## Derived Rows\n\n"
    for row in theorems:
        text += f"### {row['theorem_id']}\n\n- Statement: {row['statement']}\n- Derivation: {row['derivation']}\n- Status: `{row['status']}`\n\n"
    text += "## Projection Verdicts\n\n"
    for row in projections:
        text += f"- `{row['projection_id']}` / `{row['branch']}`: {row['verdict']} — {row['safe_condition']}\n"
    text += "\n## U Owner Gate\n\n"
    for row in gate_output:
        text += f"- `{row['candidate_id']}`: pass=`{row['u_owner_pass']}`, closed `{row['closed_clause_count']}/{row['total_clause_count']}`, failed `{row['failed_clauses']}`.\n"
    text += "\n## Bound Rows Staged\n\n"
    for row in bounds:
        text += f"- `{row['bound_id']}`: `{row['quantity']}` in `{row['arena']}` needs `{row['needed_bound']}`.\n"
    text += "\n## Claim Gates\n\n"
    for row in gates:
        text += f"- `{row['arena']}`: claim_allowed=`{row['claim_allowed']}` because {row['reason']}.\n"
    text += "\n## Decision\n\n"
    for row in decisions:
        text += f"`{row['decision']}`: {row['summary']}\n\n"
    text += "## Status\n\n"
    for row in statuses:
        text += f"- `{row['timestamp_utc']}`: {row['summary']}\n"
    text += "\n## Next Target\n\n"
    for row in next_targets:
        text += f"- `{row['target']}`: {row['question']} Preferred route: {row['preferred_route']}\n"
    write_text(FORMAL_PATH, text)


def write_post_doc(decisions: List[Dict[str, str]], next_targets: List[Dict[str, str]]) -> None:
    text = f"""# 4390 Y5 R2FR: U action owner construction or pressure-curvature bound row

Marker: `{MARKER}`

## Private checkpoint

This checkpoint turns the 4389 payload warning into an actual construction route. The scalar trace route is demoted; the electric-projector U route becomes the next derivation target.

## Decision

{decisions[0]['summary']}

## Next

{next_targets[0]['target']}

{next_targets[0]['question']}
"""
    write_text(DOC_PATH, text)


def write_spine_update() -> None:
    block = f"""
## 4390 local spine update: electric U projector route

Marker: `{MARKER}`

Spine update: the local-GR branch now has a concrete non-scalar U candidate. A parent-owned electric projector built from `u^mu` and transverse `S^{{mu nu}}` can place the desired density operator in `U^{{0i0j}}=S^{{ij}}` while avoiding the same-order static pressure problem of scalar `phi R`. This is not a claim: parent owner, static time-silence, pressure/aniso, curvature, boundary, Ward, and matter-quotient gates remain open.
"""
    append_once(SPINE_PATH, MARKER, block)


def write_packet_update() -> None:
    block = f"""
## 4390 packet update: electric U projector route

Marker: `{PACKET_MARKER}`

Packet update: 4390 constructs the preferred next local-GR route rather than only listing missing inputs. The branch is `U^{{mu alpha nu beta}}[u,S]` with `U^{{0i0j}}=S^{{ij}}`, giving `Delta rho ~ c^-2 partial_i partial_j S^{{ij}}` in the local rest frame. Scalar `phi R` is demoted because it carries same-order weak-static pressure/aniso. Claim remains blocked until the parent `u/S` sector, static time-silence, pressure/curvature/boundary/Ward gates, and quotient matter coupling are signed.
"""
    append_once(PACKET_PATH, PACKET_MARKER, block)


def write_claim() -> None:
    append_claim_once(
        CLAIMS_PATH,
        CLAIM_ID,
        [
            CLAIM_ID,
            "local_gr",
            "4390 constructs a concrete electric-projector U/action route for the local-GR branch. With a parent local flow u^mu and transverse symmetric S^{mu nu}, U^{mu alpha nu beta}=u^mu u^nu S^{alpha beta}-u^alpha u^nu S^{mu beta}-u^mu u^beta S^{alpha nu}+u^alpha u^beta S^{mu nu} has Riemann symmetries and gives U^{0i0j}=S^{ij} in the local rest frame. This can supply Delta rho~c^-2 partial_i partial_j S^{ij} while the leading ij pressure/aniso payload is moved to time-derivative, curvature, boundary, metric-dependence, and Ward gates. The scalar phiR trace route is demoted because it carries same-order weak-static pressure/aniso. No local-GR/Newton/PPN/clock/orbital/R10 claim fires.",
            "4390 source register, U construction theorem rows, projection verdicts, U owner gate input/output, pressure-curvature bound rows, route rows, claim gates, decision, status, next target and validation CSV.",
            "electric_U_projector_route_derived_parent_static_payload_gates_open_nonclaim",
            "Derive a parent-owned u/S electric U sector with static time-silence and Ward conservation, or fill source-backed pressure/aniso, curvature, boundary, and exchange-current bound rows.",
            "Promoting scalar phiR, fitting S^{ij} post-readout, ignoring ij stress, or claiming from the density slot without parent owner and payload gates.",
        ],
    )


def validation_rows(csv_paths: List[Path]) -> List[Dict[str, str]]:
    validations: List[Dict[str, str]] = []
    sources = read_csv(SOURCE_DIR / "P8_Y5_R2FR_4390_SOURCE_REGISTER.csv")
    theorems = read_csv(SOURCE_DIR / "P8_Y5_R2FR_4390_U_CONSTRUCTION_THEOREMS.csv")
    projections = read_csv(SOURCE_DIR / "P8_Y5_R2FR_4390_COMPONENT_PROJECTIONS.csv")
    gate_output = read_csv(GATE_OUTPUT_PATH)
    bounds = read_csv(SOURCE_DIR / "P8_Y5_R2FR_4390_PRESSURE_CURVATURE_BOUND_ROWS.csv")
    gates = read_csv(SOURCE_DIR / "P8_Y5_R2FR_4390_CLAIM_GATES.csv")

    def add(check_id: str, passed: bool, detail: str) -> None:
        validations.append({"checkpoint": CHECKPOINT, "check_id": check_id, "passed": str(bool(passed)), "detail": detail})

    add("VAL4390_0_sources_exist", all(row["path_exists"] == "True" for row in sources), "every cited source exists")
    add("VAL4390_1_needles_found", all(row["needle_found"] == "True" for row in sources), "every cited needle resolves")
    add(
        "VAL4390_2_electric_projector_derived",
        any(row["theorem_id"] == "U4390_0_electric_projector_ansatz" and "U^{0i0j}=S^{ij}" in row["derivation"] for row in theorems),
        "electric projector theorem staged",
    )
    add(
        "VAL4390_3_scalar_trace_demoted",
        any(row["branch"] == "scalar_trace_phi_R" and "DEMOTED" in row["verdict"] for row in projections),
        "scalar phiR is demoted for local closure",
    )
    add(
        "VAL4390_4_gate_fails_closed",
        all(row["u_owner_pass"] == "False" and row["valid_for_claim"] == "False" for row in gate_output),
        "all U owner candidates fail closed",
    )
    add(
        "VAL4390_5_bound_rows_nonclaim",
        len(bounds) >= 5 and all(row["valid_for_claim"] == "False" and "MISSING" in row["source_path"] for row in bounds),
        "fallback bound rows staged as nonclaim",
    )
    add("VAL4390_6_claim_gates_false", all(row["claim_allowed"] == "False" for row in gates), "all claim gates false")
    add("VAL4390_7_formal_marker", MARKER in read_text(FORMAL_PATH), "formal marker present")
    add("VAL4390_8_post_marker", MARKER in read_text(DOC_PATH), "post marker present")
    add("VAL4390_9_spine_marker", MARKER in read_text(SPINE_PATH), "spine marker present")
    add("VAL4390_10_packet_marker", PACKET_MARKER in read_text(PACKET_PATH), "packet marker present")
    add("VAL4390_11_claim_row", f"\n{CLAIM_ID}," in read_text(CLAIMS_PATH), "claim row appended")
    add(
        "VAL4390_12_rows_nonclaim",
        all(row.get("valid_for_claim", "False") == "False" for path in csv_paths for row in read_csv(path))
        and all(row.get("claim_allowed", "False") == "False" for path in csv_paths for row in read_csv(path)),
        "generated rows remain nonclaim",
    )
    add("VAL4390_13_csv_parse", all(len(read_csv(path)) > 0 for path in csv_paths), "all generated CSVs parse")
    add("VAL4390_14_runner_exists", GATE_RUNNER_PATH.exists() and "def evaluate_u_owner_rows" in read_text(GATE_RUNNER_PATH), "U owner gate runner exists")
    return validations


def main() -> None:
    sources = source_register_rows()
    theorems = theorem_rows()
    projections = projection_rows()
    gate_inputs = gate_input_rows()
    bounds = bound_rows()
    routes = route_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    statuses = status_rows()
    next_targets = next_target_rows()

    csv_payloads: Dict[str, List[Dict[str, str]]] = {
        "P8_Y5_R2FR_4390_SOURCE_REGISTER.csv": sources,
        "P8_Y5_R2FR_4390_U_CONSTRUCTION_THEOREMS.csv": theorems,
        "P8_Y5_R2FR_4390_COMPONENT_PROJECTIONS.csv": projections,
        "P8_Y5_R2FR_4390_PRESSURE_CURVATURE_BOUND_ROWS.csv": bounds,
        "P8_Y5_R2FR_4390_ROUTE_ROWS.csv": routes,
        "P8_Y5_R2FR_4390_CLAIM_GATES.csv": gates,
        "P8_Y5_R2FR_4390_DECISION.csv": decisions,
        "P8_Y5_R2FR_4390_STATUS.csv": statuses,
        "P8_Y5_R2FR_4390_NEXT_TARGET.csv": next_targets,
    }

    csv_paths: List[Path] = [GATE_INPUT_PATH]
    write_csv(GATE_INPUT_PATH, gate_inputs)
    for filename, rows in csv_payloads.items():
        path = SOURCE_DIR / filename
        write_csv(path, rows)
        csv_paths.append(path)

    gate_output = evaluate_u_owner_rows(GATE_INPUT_PATH)
    write_csv(GATE_OUTPUT_PATH, gate_output)
    csv_paths.append(GATE_OUTPUT_PATH)

    write_formal_doc(sources, theorems, projections, gate_output, bounds, routes, gates, decisions, statuses, next_targets)
    write_post_doc(decisions, next_targets)
    write_spine_update()
    write_packet_update()
    write_claim()
    write_csv(VALIDATION_PATH, validation_rows(csv_paths))


if __name__ == "__main__":
    main()
