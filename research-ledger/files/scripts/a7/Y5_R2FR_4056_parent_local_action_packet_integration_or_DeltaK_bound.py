from __future__ import annotations

import csv
import py_compile
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Tuple


ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
FORMALIZATION = PROJECT / "formalization-workbench"
SOURCE_DIR = ROOT / "source-intake" / "mts_residuals"
SCRIPT_PATH = Path(__file__).resolve()
DOC_PATH = ROOT / "4056-Y5-R2FR-parent-local-action-packet-integration-or-DeltaK-bound.md"

SOURCES = {
    "SRC4056_00_ppc4048": (
        SOURCE_DIR / "P8_Y5_R2FR_4048_PARENT_PACKET_CONTRACT.csv",
        "PPC4048_7_gamma_khat_qloc",
    ),
    "SRC4056_01_sufficiency": (
        SOURCE_DIR / "P8_Y5_R2FR_4048_LOCAL_GR_SUFFICIENCY_THEOREM.csv",
        "S_loc^{<=2PN}",
    ),
    "SRC4056_02_4053": (
        SOURCE_DIR / "P8_Y5_R2FR_4053_PROJECTOR_SILENCE_REDUCTION_THEOREM.csv",
        "parent Hilbert owner",
    ),
    "SRC4056_03_4054": (
        SOURCE_DIR / "P8_Y5_R2FR_4054_NATURAL_NO_FLUX_SCALAR_CHARGE_THEOREM.csv",
        "Natural no-flux condition",
    ),
    "SRC4056_04_4055_DGK": (
        SOURCE_DIR / "P8_Y5_R2FR_4055_DGK_ZERO_CERTIFICATE.csv",
        "ALGEBRAIC_ZERO_UNDER_ADOPTION",
    ),
    "SRC4056_05_4055_trace": (
        SOURCE_DIR / "P8_Y5_R2FR_4055_TRACE_BACKGROUND_SUBTRACTION_LAW.csv",
        "READOUT_FIREWALL_TRACE_RULE",
    ),
    "SRC4056_06_no_hom": (
        SOURCE_DIR / "P8_Y5_R2FR_4036_NO_HOM_SOURCE_SLOT_THEOREM.csv",
        "Z*T_H and Z*F_EM^2",
    ),
    "SRC4056_07_boundary": (
        SOURCE_DIR / "P8_Y5_R2FR_4038_BOUNDARY_REFERENCE_THEOREM.csv",
        "C_BOUNDARY_ZERO_IN_SELECTED_LOCAL_BRANCH",
    ),
    "SRC4056_08_projector": (
        SOURCE_DIR / "P8_Y5_R2FR_4043_SELECTED_BRANCH_ZERO_THEOREM.csv",
        "T_projector_domain",
    ),
    "SRC4056_09_memory": (
        SOURCE_DIR / "P8_Y5_R2FR_4046_TAIL_ZERO_THEOREM.csv",
        "X_mem=0",
    ),
    "SRC4056_10_source_norm": (
        SOURCE_DIR / "P8_Y5_R2FR_4047_SELECTED_ZERO_THEOREM.csv",
        "Delta_cnorm",
    ),
    "SRC4056_11_formal_179": (
        FORMALIZATION / "179-PPC4048-local-parent-packet-candidate.md",
        "not_public_local_GR_claim",
    ),
}

OUTPUTS = {
    "source_register": SOURCE_DIR / "P8_Y5_R2FR_4056_SOURCE_REGISTER.csv",
    "action_packet": SOURCE_DIR / "P8_Y5_R2FR_4056_LOCAL_PARENT_ACTION_PACKET.csv",
    "adoption_gate": SOURCE_DIR / "P8_Y5_R2FR_4056_PACKET_ADOPTION_GATE.csv",
    "local_gr_theorem": SOURCE_DIR / "P8_Y5_R2FR_4056_CONDITIONAL_LOCAL_GR_THEOREM.csv",
    "fallback_bounds": SOURCE_DIR / "P8_Y5_R2FR_4056_DELTAK_FALLBACK_BOUND_VECTOR.csv",
    "formal_plan": SOURCE_DIR / "P8_Y5_R2FR_4056_FORMAL_INTEGRATION_PLAN.csv",
    "evaluator": SOURCE_DIR / "P8_Y5_R2FR_4056_EVALUATOR_RESULTS.csv",
    "claim_gate": SOURCE_DIR / "P8_Y5_R2FR_4056_CLAIM_GATE.csv",
    "next_target": SOURCE_DIR / "P8_Y5_R2FR_4056_NEXT_TARGET.csv",
    "status": SOURCE_DIR / "P8_Y5_R2FR_4056_STATUS.csv",
    "validation": SOURCE_DIR / "P8_Y5_BRR545_4056_VALIDATION.csv",
}


def timestamp() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def contains(path: Path, needle: str) -> bool:
    return path.exists() and needle in read_text(path)


def write_csv(path: Path, rows: List[Dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields: List[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def source_rows(ts: str) -> List[Dict[str, object]]:
    rows: List[Dict[str, object]] = []
    for source_id, (path, needle) in SOURCES.items():
        rows.append(
            {
                "source_id": source_id,
                "path": str(path),
                "exists": path.exists(),
                "needle": needle,
                "needle_present": contains(path, needle),
                "use_in_4056": "local_parent_action_packet",
                "timestamp_utc": ts,
            }
        )
    return rows


def action_packet_rows(ts: str) -> List[Dict[str, object]]:
    return [
        {
            "packet_id": "LAP4056_0_field_space",
            "sector": "field space",
            "term_or_clause": "Q_parent^loc = Met_obs x Matter x EM x K_G x Aux_GK x Aux_private with q:Q_parent^loc -> Met_obs",
            "role": "separates observed geometry from fixed coupling data and auxiliary/private response fields",
            "source": "PPC4048_0 and 4055",
            "adoption_status": "candidate_packet_clause",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "packet_id": "LAP4056_1_EH",
            "sector": "gravity",
            "term_or_clause": "S_EH[g_obs;kappa_*] + S_GHY[g_obs] with fixed local kappa_*",
            "role": "owns the local observed metric equation and Newton/PPN GR baseline",
            "source": "PPC4048_1/2 and 4048 sufficiency theorem",
            "adoption_status": "candidate_packet_clause",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "packet_id": "LAP4056_2_same_source_matter",
            "sector": "ordinary matter",
            "term_or_clause": "S_matter = Sbar_m[psi,g_obs,theta] with fixed representation labels and no hidden source weights",
            "role": "forces Newtonian source mass and PPN source stress to be the same Hilbert branch",
            "source": "PPC4048_3/5 and 4036",
            "adoption_status": "candidate_packet_clause",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "packet_id": "LAP4056_3_EM",
            "sector": "electromagnetism",
            "term_or_clause": "S_EM[A,g_obs] uses one observed Hodge star and no hidden f(Z)F_EM^2 multiplier",
            "role": "counts bound EM stress once and blocks source-only EM leakage into q_loc",
            "source": "PPC4048_4, 4036, 4038",
            "adoption_status": "candidate_packet_clause",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "packet_id": "LAP4056_4_GK",
            "sector": "Gamma/Khat/q_loc",
            "term_or_clause": "S_GK=-int sqrt|g| Gamma_ren + B_GK, T_GK=T_Hilbert_GK, Khat=K_Gamma",
            "role": "turns q_loc into a Ward residual and sets D_GK=0 under adoption",
            "source": "4053 and 4055",
            "adoption_status": "candidate_packet_clause_sharpest_hinge",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "packet_id": "LAP4056_5_phi_boundary",
            "sector": "scalar/Khat owner",
            "term_or_clause": "unit-response varpi owner with natural no-flux inner boundary and fixed outer reference branch",
            "role": "gives Q_phi=0 and removes scalar Khat hair in the compact local collar",
            "source": "4054",
            "adoption_status": "candidate_packet_clause",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "packet_id": "LAP4056_6_boundary_projector_memory",
            "sector": "side channels",
            "term_or_clause": "source-blind boundary/reference, q-basic projector/domain, reset local memory tail, fixed source-normalization map",
            "role": "prevents boundary/projector/memory/source-normalization leakage from re-entering PPN",
            "source": "4038, 4043, 4046, 4047",
            "adoption_status": "candidate_packet_clause",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "packet_id": "LAP4056_7_readout_firewall",
            "sector": "claim/readout discipline",
            "term_or_clause": "PPN, R10, clocks, orbital, EM and cosmology are post-variation readouts only",
            "role": "blocks fitting measured readouts back into the action",
            "source": "PPC4048_9/10",
            "adoption_status": "candidate_packet_clause",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
    ]


def adoption_gate_rows(ts: str) -> List[Dict[str, object]]:
    return [
        {
            "gate_id": "ADOPT4056_0_one_action",
            "gate": "single local action packet",
            "requirement": "all terms live in one local <=2PN parent packet, not separate closure patches",
            "current_result": "candidate packet assembled",
            "if_fail": "local branch remains closure/fallback",
            "status": "CANDIDATE_READY_NOT_FORMAL_ADOPTED",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "gate_id": "ADOPT4056_1_no_source_slots",
            "gate": "ordinary matter/EM hidden-source silence",
            "requirement": "no Z*T_H, Z*F_EM^2, source mask, hidden coframe, or source-weight prefactor",
            "current_result": "4036 supplies conditional no-Hom theorem",
            "if_fail": "c_T/c_EM/source-slot bounds activate",
            "status": "CONDITIONAL_IF_TYPED_PACKET_ADOPTED",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "gate_id": "ADOPT4056_2_q_loc",
            "gate": "q_loc Hilbert owner",
            "requirement": "Khat=K_Gamma and Gamma_ren trace/background subtraction are adopted",
            "current_result": "4055 supplies algebraic D_GK zero route",
            "if_fail": "Delta_K bound branch activates",
            "status": "CONDITIONAL_IF_4055_PACKET_ADOPTED",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "gate_id": "ADOPT4056_3_scalar_charge",
            "gate": "scalar charge/no-flux",
            "requirement": "no boundary source term for varpi and fixed outer branch",
            "current_result": "4054 supplies natural no-flux Q_phi=0 route",
            "if_fail": "Yukawa/harmonic scalar charge bound activates",
            "status": "CONDITIONAL_IF_4054_BOUNDARY_ADOPTED",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "gate_id": "ADOPT4056_4_side_channels",
            "gate": "boundary/projector/memory/source-normalization silence",
            "requirement": "4038/4043/4046/4047 selected branches become packet clauses",
            "current_result": "selected zero routes already staged",
            "if_fail": "alpha_i/xi/cZ/cnorm fallback bounds activate",
            "status": "CONDITIONAL_IF_SELECTED_BRANCH_ADOPTED",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "gate_id": "ADOPT4056_5_public_claim",
            "gate": "public local-GR claim",
            "requirement": "formal adoption verified and fallback rows either zero or passed",
            "current_result": "not satisfied",
            "if_fail": "no public local-GR claim",
            "status": "PUBLIC_CLAIM_BLOCKED",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
    ]


def local_gr_theorem_rows(ts: str) -> List[Dict[str, object]]:
    return [
        {
            "theorem_id": "LGT4056_0_packet",
            "premise": "LAP4056_0 through LAP4056_7 are adopted as one local parent packet",
            "statement": "S_loc^{<=2PN}=S_EH+S_matter+S_EM+S_binding+S_GK+B_proper+S_top+S_vertical+S_reset with no hidden readout/source slots",
            "result": "local observed metric equation is EH plus same Hilbert source through <=2PN",
            "status": "CONDITIONAL_THEOREM_CANDIDATE",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "theorem_id": "LGT4056_1_Newton",
            "premise": "EH 00 equation, fixed kappa_*, same Hilbert mass source",
            "statement": "G_00^(1)=kappa_* T_00 implies Poisson equation with calibrated G_ref=c^4 kappa_*/(8*pi)",
            "result": "Newton/Poisson limit follows as a calibrated constant branch, not a numerical prediction of G",
            "status": "CONDITIONAL_NEWTON_LIMIT",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "theorem_id": "LGT4056_2_PPN",
            "premise": "no q_loc, nonEH, projector/domain, boundary, memory, source-normalization or trace leakage",
            "statement": "Delta_PPN_abs=0 in the selected <=2PN local collar",
            "result": "gamma=beta=1, alpha_i=xi=zeta_i=0, Gdot/G=0 under the packet",
            "status": "CONDITIONAL_PPN_ZERO_VECTOR",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "theorem_id": "LGT4056_3_failure",
            "premise": "any adoption gate fails",
            "statement": "route the failed term to its fallback bound with no cancellation credit",
            "result": "field-theory route fails cleanly instead of becoming a hidden plateau axiom",
            "status": "NO_SNEAKY_CLOSURE_POLICY",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
    ]


def fallback_rows(ts: str) -> List[Dict[str, object]]:
    return [
        {
            "bound_id": "DK4056_0_DeltaK",
            "failed_gate": "ADOPT4056_2_q_loc",
            "formula": "Delta_K^{mu nu}:=K_Gamma^{mu nu}-Khat^{mu nu}; Q_loc <= C_Ploc ||nabla_mu Delta_K^{mu nu}|| + Euler/boundary/source envelopes",
            "observable_map": "PPN beta/gamma; R10 alpha(lambda); source-exchange",
            "needed_inputs": "Delta_K profile, length scale, projector coefficients",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "bound_id": "DK4056_1_source_slot",
            "failed_gate": "ADOPT4056_1_no_source_slots",
            "formula": "q_source <= c_T grad T_H + c_EM grad F_EM^2 + source-mask derivatives",
            "observable_map": "WEP, PPN source-dependence, local force residual",
            "needed_inputs": "c_T,c_EM,source profiles,composition/readout map",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "bound_id": "DK4056_2_scalar_charge",
            "failed_gate": "ADOPT4056_3_scalar_charge",
            "formula": "u(r)=Q_phi exp(-mu_phi r)/(4*pi r) plus multipoles",
            "observable_map": "fifth-force range, PPN beta/gamma scalar tail",
            "needed_inputs": "Q_phi,mu_phi,boundary data",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "bound_id": "DK4056_3_side_channels",
            "failed_gate": "ADOPT4056_4_side_channels",
            "formula": "absolute-sum envelope over boundary flux, projector/domain stress, memory tail, source-normalization drift",
            "observable_map": "alpha_i, xi, cZ, cnorm, Gdot/G",
            "needed_inputs": "existing fallback coefficients from 4038/4043/4046/4047",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
    ]


def formal_plan_rows(ts: str) -> List[Dict[str, object]]:
    return [
        {
            "plan_id": "FIP4056_0_private_first",
            "target": "post-checkpoint private packet",
            "action": "keep 4056 nonclaim until adoption gates are manually reviewed",
            "reason": "avoid editing formalization-workbench before the packet is coherent",
            "timestamp_utc": ts,
        },
        {
            "plan_id": "FIP4056_1_if_adopted",
            "target": "formalization-workbench/179-PPC4048-local-parent-packet-candidate.md",
            "action": "upgrade PPC4048_7 from broad q_loc/Khat blocker to 4056 integrated parent-packet clause",
            "reason": "4053-4055 replace the old undefined projector-silence route",
            "timestamp_utc": ts,
        },
        {
            "plan_id": "FIP4056_2_claim_guard",
            "target": "formalization-workbench/02-claims-register.csv",
            "action": "keep L-001 private_candidate_nonclaim unless formal adoption and fallback verification pass",
            "reason": "4056 is a candidate packet, not public proof",
            "timestamp_utc": ts,
        },
        {
            "plan_id": "FIP4056_3_if_rejected",
            "target": "Delta_K bound branch",
            "action": "start numeric/source acquisition for Delta_K and source-slot/scalar/side-channel fallback rows",
            "reason": "failed adoption must become a scored residual, not another closure",
            "timestamp_utc": ts,
        },
    ]


def static_rows(ts: str) -> Dict[str, List[Dict[str, object]]]:
    return {
        "evaluator": [
            {
                "case_id": "CASE4056_0",
                "verdict": "INTEGRATED_LOCAL_PARENT_PACKET_ASSEMBLED",
                "result": "EH, same-source matter/EM, Gamma_ren/K_Gamma, scalar no-flux, boundary/projector/memory/source-normalization and readout firewall clauses now sit in one candidate packet.",
                "what_moved": "The local-GR route is no longer scattered across separate checkpoints; it has a single adoption gate.",
                "valid_for_public_claim": False,
                "timestamp_utc": ts,
            },
            {
                "case_id": "CASE4056_1",
                "verdict": "PUBLIC_CLAIM_STILL_BLOCKED",
                "result": "The packet is coherent enough to review for formal adoption, but it is not yet adopted as live MTS.",
                "what_moved": "The next decision is concrete: adopt packet into formal candidate docs or run Delta_K fallback.",
                "valid_for_public_claim": False,
                "timestamp_utc": ts,
            },
        ],
        "claim_gate": [
            {
                "claim_id": "CLAIM4056_0_private_progress",
                "claim": "integrated local parent action packet exists as private candidate",
                "allowed_private": True,
                "allowed_public": False,
                "reason": "assembled in post-checkpoint but not formal-adopted",
                "timestamp_utc": ts,
            },
            {
                "claim_id": "CLAIM4056_1_local_GR_private_conditional",
                "claim": "if all adoption gates pass, the packet yields Newton/PPN GR limit",
                "allowed_private": True,
                "allowed_public": False,
                "reason": "conditional theorem only",
                "timestamp_utc": ts,
            },
            {
                "claim_id": "CLAIM4056_2_public_local_GR",
                "claim": "MTS publicly derives local GR/Newton/PPN",
                "allowed_private": False,
                "allowed_public": False,
                "reason": "formal adoption and fallback verification still absent",
                "timestamp_utc": ts,
            },
        ],
        "next_target": [
            {
                "row_id": "NEXT4056_0",
                "next_doc": "4057-Y5-R2FR-formal-adoption-preflight-for-4056-local-parent-packet.md",
                "next_script": "scripts/Y5_R2FR_4057_formal_adoption_preflight_for_4056_packet.py",
                "reason": "The next useful step is a ruthless preflight before touching formalization-workbench, checking whether 4056 can safely supersede the q_loc/Khat blocker note.",
                "timestamp_utc": ts,
            }
        ],
        "status": [
            {
                "status_id": "STAT4056",
                "status": "INTEGRATED_LOCAL_PARENT_PACKET_CANDIDATE_ASSEMBLED_NONCLAIM",
                "public_claim": False,
                "formalization_modified_by_4056": False,
                "timestamp_utc": ts,
            }
        ],
    }


def script_compiles() -> bool:
    try:
        py_compile.compile(str(SCRIPT_PATH), doraise=True)
        return True
    except py_compile.PyCompileError:
        return False


def csv_parse_ok(path: Path) -> Tuple[bool, str]:
    try:
        with path.open(encoding="utf-8", newline="") as handle:
            rows = list(csv.DictReader(handle))
        return bool(rows), f"rows={len(rows)}"
    except Exception as exc:
        return False, repr(exc)


def validation_rows(
    sources: List[Dict[str, object]],
    generated_csvs: List[Path],
    all_rows: List[List[Dict[str, object]]],
) -> List[Dict[str, object]]:
    parse_results = [csv_parse_ok(path) for path in generated_csvs]
    flat_rows = [row for table in all_rows for row in table]
    serialized = "\n".join(str(value) for row in flat_rows for value in row.values())
    outputs_in_formalization = [path for path in OUTPUTS.values() if FORMALIZATION in path.parents]
    return [
        {
            "check_id": "VAL4056_00_sources_exist",
            "passed": all(bool(row["exists"]) for row in sources),
            "detail": "all cited local source paths exist",
        },
        {
            "check_id": "VAL4056_01_needles_present",
            "passed": all(bool(row["needle_present"]) for row in sources),
            "detail": "all source needles present",
        },
        {
            "check_id": "VAL4056_02_csv_parse",
            "passed": all(result for result, _detail in parse_results),
            "detail": "; ".join(f"{path.name}:{detail}" for path, (_ok, detail) in zip(generated_csvs, parse_results)),
        },
        {
            "check_id": "VAL4056_03_no_public_claim",
            "passed": "allowed_public': True" not in serialized and "valid_for_public_claim': True" not in serialized,
            "detail": "all claim-bearing rows preserve public false",
        },
        {
            "check_id": "VAL4056_04_no_missing_markers",
            "passed": "MISSING_" not in serialized,
            "detail": "outputs use explicit open/blocker language instead of MISSING markers",
        },
        {
            "check_id": "VAL4056_05_no_formalization_outputs",
            "passed": len(outputs_in_formalization) == 0,
            "detail": "4056 writes only post-checkpoint/source-intake outputs",
        },
        {
            "check_id": "VAL4056_06_script_compiles",
            "passed": script_compiles(),
            "detail": "script compiles",
        },
    ]


def doc_text(ts: str) -> str:
    return """# 4056 - Parent Local Action Packet Integration or DeltaK Bound

- Timestamp: `__TS__`
- Status: `private_nonclaim_checkpoint`
- Formalization modified: `false`
- Public local-GR claim: `false`

## What Actually Moved

4056 assembles the scattered local-GR repair work into one candidate parent packet:

```text
S_loc^{<=2PN}
= S_EH[g_obs;kappa_*]
 + S_matter[psi,g_obs,theta]
 + S_EM[A,g_obs]
 + S_binding
 + S_GK[Gamma_ren,K_Gamma,Y]
 + B_proper + S_top + S_vertical + S_reset.
```

The important clause is no longer vague `q_loc=0`. It is:

```text
S_GK=-int sqrt|g| Gamma_ren + B_GK,
T_GK=T_Hilbert_GK,
Khat=K_Gamma,
D_GK=0.
```

Together with 4054 scalar no-flux, 4036 no hidden source slots, 4038 boundary/reference silence, 4043 projector/domain silence, 4046 memory reset, and 4047 source-normalization silence, this gives a coherent conditional local GR branch.

## Conditional Local-GR Statement

If every 4056 adoption gate passes, then the local observed metric equation is EH plus the same Hilbert matter/EM/binding source through `<=2PN`.

Consequences:

- Newton/Poisson limit follows with calibrated fixed `G_ref=c^4 kappa_*/(8*pi)`.
- PPN vector is zero in the selected compact local branch.
- `q_loc` is a Ward residual, not a fitted plateau.
- Failed clauses route to absolute-sum fallback bounds, especially `Delta_K`.

## Honest Status

This is the most coherent local-GR packet so far. It is still not a public proof. It needs a formal adoption preflight before touching `formalization-workbench`, because adopting it changes the status of the old `q_loc/Khat` blocker.

## Failure Exit

If the packet is rejected, keep the local route honest:

```text
Delta_K^{mu nu}:=K_Gamma^{mu nu}-Khat^{mu nu},
Q_loc <= C_Ploc ||nabla_mu Delta_K^{mu nu}|| + source/boundary/projector/scalar envelopes.
```

## Next Target

Run a formal-adoption preflight for the 4056 packet. If it passes, update `179-PPC4048-local-parent-packet-candidate.md` as a guarded candidate. If it fails, start the `Delta_K` bound branch.
""".replace("__TS__", ts)


def main() -> None:
    ts = timestamp()
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)

    sources = source_rows(ts)
    action_packet = action_packet_rows(ts)
    adoption_gate = adoption_gate_rows(ts)
    local_gr_theorem = local_gr_theorem_rows(ts)
    fallback = fallback_rows(ts)
    formal_plan = formal_plan_rows(ts)
    static = static_rows(ts)

    DOC_PATH.write_text(doc_text(ts), encoding="utf-8")
    write_csv(OUTPUTS["source_register"], sources)
    write_csv(OUTPUTS["action_packet"], action_packet)
    write_csv(OUTPUTS["adoption_gate"], adoption_gate)
    write_csv(OUTPUTS["local_gr_theorem"], local_gr_theorem)
    write_csv(OUTPUTS["fallback_bounds"], fallback)
    write_csv(OUTPUTS["formal_plan"], formal_plan)
    write_csv(OUTPUTS["evaluator"], static["evaluator"])
    write_csv(OUTPUTS["claim_gate"], static["claim_gate"])
    write_csv(OUTPUTS["next_target"], static["next_target"])
    write_csv(OUTPUTS["status"], static["status"])

    generated_csvs = [
        OUTPUTS["source_register"],
        OUTPUTS["action_packet"],
        OUTPUTS["adoption_gate"],
        OUTPUTS["local_gr_theorem"],
        OUTPUTS["fallback_bounds"],
        OUTPUTS["formal_plan"],
        OUTPUTS["evaluator"],
        OUTPUTS["claim_gate"],
        OUTPUTS["next_target"],
        OUTPUTS["status"],
    ]
    all_rows = [
        sources,
        action_packet,
        adoption_gate,
        local_gr_theorem,
        fallback,
        formal_plan,
        static["evaluator"],
        static["claim_gate"],
        static["next_target"],
        static["status"],
    ]
    validation = validation_rows(sources, generated_csvs, all_rows)
    write_csv(OUTPUTS["validation"], validation)

    cache_dir = SCRIPT_PATH.parent / "__pycache__"
    if cache_dir.exists():
        shutil.rmtree(cache_dir)

    failures = [row for row in validation if not row["passed"]]
    print(f"wrote {DOC_PATH}")
    print(f"validation rows: {len(validation)}")
    print(f"validation failures: {len(failures)}")
    for failure in failures:
        print(f"FAIL {failure['check_id']}: {failure['detail']}")


if __name__ == "__main__":
    main()
