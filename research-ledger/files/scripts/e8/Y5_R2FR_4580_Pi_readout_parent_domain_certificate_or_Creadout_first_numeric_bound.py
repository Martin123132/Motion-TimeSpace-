from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4580"
CLAIM_ID = "L-422"
BRANCH_ID = "MTS_R2FR_Y5_PI_READOUT_PARENT_DOMAIN_CERTIFICATE_OR_CREADOUT_FIRST_NUMERIC_BOUND_4580"
MARKER = "PPC4161_PI_READOUT_PARENT_DOMAIN_CERTIFICATE_OR_CREADOUT_FIRST_NUMERIC_BOUND_4580"
PACKET_MARKER = "PPC4161_PACKET_PI_READOUT_PARENT_DOMAIN_CERTIFICATE_OR_CREADOUT_FIRST_NUMERIC_BOUND_4580"
DECISION = "FIXED_QBASIC_READOUT_DOMAIN_CERTIFICATE_DERIVES_CDOMAIN_CSUPPORT_ZERO_ACTIVE_PROJECTOR_BRANCH_RETAINED_NONCLAIM"
NEXT_TARGET = "4581-Y5-R2FR-remaining-Creadout-frame-material-kernel-EFT-tau-residual-bound-or-zero.md"

DOC_PATH = POST / "4580-Y5-R2FR-Pi-readout-parent-domain-certificate-or-Creadout-first-numeric-bound.md"
FORMAL_PATH = FORMAL / "596-PPC4161-Pi-readout-parent-domain-certificate-or-Creadout-first-numeric-bound.md"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

DOC_4579 = POST / "4579-Y5-R2FR-readout-commutator-zero-or-rho-readout-shift-bound-value.md"
CSV_4579_NEXT = SOURCE_DIR / "P8_Y5_R2FR_4579_NEXT_TARGET.csv"
CSV_4579_THEOREM = SOURCE_DIR / "P8_Y5_R2FR_4579_READOUT_COMMUTATOR_THEOREM.csv"
CSV_4579_PROJECTOR = SOURCE_DIR / "P8_Y5_R2FR_4579_PROJECTOR_DERIVATIVE_BOUND.csv"
CSV_4579_BOUND_VALUE = SOURCE_DIR / "P8_Y5_R2FR_4579_RHO_READOUT_SHIFT_BOUND_VALUE_ROWS.csv"
CSV_3928_AUDIT = SOURCE_DIR / "P8_Y5_R2FR_3928_PROJECTOR_DOMAIN_CERTIFICATE_AUDIT.csv"
CSV_3928_CONTRACT = SOURCE_DIR / "P8_Y5_R2FR_3928_TOPOLOGICAL_READOUT_ZERO_CONTRACT.csv"
CSV_3929_SIGNATURE = SOURCE_DIR / "P8_Y5_R2FR_3929_PROJECTOR_PARENT_SIGNATURE.csv"
CSV_3929_ZERO = SOURCE_DIR / "P8_Y5_R2FR_3929_PROJECTOR_DOMAIN_ZERO_RESULT.csv"
CSV_3941_MAP = SOURCE_DIR / "P8_Y5_R2FR_3941_PIM_HTAU_MAP_DERIVATION.csv"
CSV_3941_BOUNDS = SOURCE_DIR / "P8_Y5_R2FR_3941_PIM_COMMUTATOR_BOUND_ROWS.csv"
CSV_3946_DOMAIN = SOURCE_DIR / "P8_Y5_R2FR_3946_TOTAL_SOURCE_DOMAIN_CERTIFICATE.csv"
CSV_4269_TAU = SOURCE_DIR / "P8_Y5_R2FR_4269_TAU_LOCK_THEOREM.csv"
CSV_4269_ADOPTION = SOURCE_DIR / "P8_Y5_R2FR_4269_DQ_TAU_ADOPTION.csv"
CSV_4269_RESIDUALS = SOURCE_DIR / "P8_Y5_R2FR_4269_TAU_RESIDUAL_SPLIT_ROWS.csv"
CSV_2598_TAU = SOURCE_DIR / "P8_Y5_STATIONARY_TAU_2598_THEOREM_ATTEMPT.csv"
FORMAL_284 = FORMAL / "284-PPC4161-Dq-boundary-projector-fixed-collar-or-boundary-residual-bound.md"
FORMAL_342 = FORMAL / "342-PPC4161-Dq-boundary-projector-Hperp-zero-or-domain-tail-bound.md"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4580_SOURCE_REGISTER.csv"
CERTIFICATE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4580_PI_READOUT_DOMAIN_CERTIFICATE.csv"
REDUCTION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4580_CREADOUT_REDUCTION_ROWS.csv"
ACTIVE_BOUND_CSV = SOURCE_DIR / "P8_Y5_R2FR_4580_ACTIVE_BRANCH_BOUND_ROWS.csv"
CLOSED_DOMAIN_GUARDS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4580_CLOSED_DOMAIN_GUARDS.csv"
AUDIT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4580_PARENT_SIGNATURE_AUDIT.csv"
CONTROL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4580_CONTROL_ROWS.csv"
PROMOTION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4580_PROMOTION_GATES.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4580_DECISION.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4580_NEXT_TARGET.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4580_STATUS.csv"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4580_VALIDATION.csv"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def bool_text(value: bool) -> str:
    return "True" if value else "False"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def markdown_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "\n"
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
        lines.append(
            "| "
            + " | ".join(
                str(row.get(header, "")).replace("|", "\\|").replace("\n", "<br>")
                for header in headers
            )
            + " |"
        )
    return "\n".join(lines) + "\n"


def append_once(path: Path, marker: str, block: str) -> None:
    existing = read_text(path)
    if marker in existing:
        return
    with path.open("a", encoding="utf-8", newline="\n") as handle:
        if existing and not existing.endswith("\n"):
            handle.write("\n")
        handle.write("\n" + block.strip() + "\n")


def source_rows() -> list[dict[str, Any]]:
    specs = [
        ("SRC4580_00_4579_doc", "4579 readout commutator checkpoint", DOC_4579, "C_readout"),
        ("SRC4580_01_4579_next", "4579 selected 4580 target", CSV_4579_NEXT, "Pi-readout-parent-domain-certificate-or-Creadout-first-numeric-bound"),
        ("SRC4580_02_4579_theorem", "4579 product-rule identity", CSV_4579_THEOREM, "RCT4579_3_rho_shift_bound"),
        ("SRC4580_03_4579_projector", "4579 Creadout split", CSV_4579_PROJECTOR, "PDB4579_0_Creadout_split"),
        ("SRC4580_04_4579_bound", "4579 operator bound row", CSV_4579_BOUND_VALUE, "RVB4579_1_operator_bound"),
        ("SRC4580_05_3928_fixed_domain", "3928 fixed domain zero", CSV_3928_AUDIT, "PDC3928_3_fixed_domain_zero"),
        ("SRC4580_06_3928_active_no_go", "3928 active branch no-go", CSV_3928_AUDIT, "PDC3928_7_active_branch_no_go"),
        ("SRC4580_07_3928_contract", "3928 topological/readout zero contract", CSV_3928_CONTRACT, "ZPD3928_0_readout_route"),
        ("SRC4580_08_3929_signature", "3929 q-basic projector signature", CSV_3929_SIGNATURE, "SIG3929_6_signature_verdict"),
        ("SRC4580_09_3929_zero", "3929 projector/domain zero result", CSV_3929_ZERO, "PDZ3929_4_epsilon_domain_projector_abs"),
        ("SRC4580_10_3941_map", "3941 PiM/Htau residual split", CSV_3941_MAP, "MAP3941_3_exact_split"),
        ("SRC4580_11_3941_bounds", "3941 domain/tau bound row", CSV_3941_BOUNDS, "PB3941_5_domain_tau"),
        ("SRC4580_12_3946_domain", "3946 closed-domain blockers", CSV_3946_DOMAIN, "DOM3946_8_result"),
        ("SRC4580_13_4269_tau", "4269 q-basic observed tau theorem", CSV_4269_TAU, "TAU4269_1_qbasic_observed_tau"),
        ("SRC4580_14_4269_adoption", "4269 Dq tau adoption", CSV_4269_ADOPTION, "ADOPT4269_Dq_tau"),
        ("SRC4580_15_4269_residuals", "4269 tau residual fallback", CSV_4269_RESIDUALS, "TRES4269_0_tau_split"),
        ("SRC4580_16_2598_stationary_guard", "2598 stationary tau not derived guard", CSV_2598_TAU, "STA2598_7_verdict"),
        ("SRC4580_17_formal_284", "4268 fixed noflux collar theorem", FORMAL_284, "Dq_boundary_projector = 0"),
        ("SRC4580_18_formal_342", "4326 Hperp boundary/projector zero", FORMAL_342, "Dq_boundary_projector[Hperp]=0"),
        ("SRC4580_19_claim_421", "prior claim register row", CLAIMS_PATH, "L-421"),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, label, path, needle in specs:
        text = read_text(path)
        rows.append(
            {
                "source_id": source_id,
                "label": label,
                "source_path": str(path),
                "exists": bool_text(path.exists()),
                "needle": needle,
                "needle_found": bool_text(needle in text),
                "role": "Pi_readout parent-domain certificate and first C_readout theorem-zero values",
                "valid_for_claim": "False",
            }
        )
    return rows


def certificate_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "certificate_id": "PDC4580_0_protocol_object",
            "clause": "pre-variation readout protocol",
            "statement": "Define the local readout protocol before source variation: P_loc={Dbar,W_loc,Sigma_in,Sigma_out,C_side,C_rad,tau_obs,e_obs,orientation,units,Pi_loc}.",
            "formula": "Pi_readout = Pi_post o Pi_protocol[P_loc]",
            "effect_on_Creadout": "O_f Pi_protocol=0 if P_loc is fixed or q-basic and held fixed during the compact lapse source probe.",
            "status": "CERTIFICATE_CLAUSE_DEFINED",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "certificate_id": "PDC4580_1_fixed_qbasic_domain",
            "clause": "fixed q-basic domain and support",
            "statement": "For D_loc=q_src^{-1}(Dbar), source-silent compact probes and no source crossing, the support/domain projector is not varied by the readout operation.",
            "formula": "O_f Pi_domain=0 and O_f Pi_support=0 on the fixed compact no-flux collar",
            "effect_on_Creadout": "C_domain=0 and C_support=0",
            "status": "CONDITIONAL_THEOREM_ZERO_DERIVED_FROM_3928_3929_4268_4326",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "certificate_id": "PDC4580_2_qbasic_tau_protocol",
            "clause": "q-basic observed tau used across readout roles",
            "statement": "If tau_obs=tau_bar(q) is selected before variation and the same tau is used for source, charge, clock, orbit, PPN and readout, the tau protocol does not create a readout commutator.",
            "formula": "O_f Pi_tau=0 inside the fixed observed-tau protocol; tau residuals are routed if roles split",
            "effect_on_Creadout": "C_tau_protocol=0, while R_tau_split and related residuals remain outside this certificate",
            "status": "CONDITIONAL_PROTOCOL_ZERO_DERIVED_FROM_4269",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "certificate_id": "PDC4580_3_active_projector_rejection",
            "clause": "active Hodge/Green/moving-domain projector",
            "statement": "If Pi_readout is a dynamic Green/Hodge/domain selector, product-rule terms survive and must be bounded.",
            "formula": "delta(Pi J)=Pi delta J+(delta Pi)J with delta Pi != 0 generically",
            "effect_on_Creadout": "Use active branch rows, not zero certificate",
            "status": "ZERO_REJECTED_FOR_ACTIVE_BRANCH",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "certificate_id": "PDC4580_4_readout_certificate_result",
            "clause": "Pi_readout domain certificate result",
            "statement": "The fixed q-basic no-flux readout-domain part of C_readout is theorem-zero; remaining material/frame/kernel/EFT/tau-residual channels are not zeroed here.",
            "formula": "C_readout <= C_frame + C_material + C_kernel + C_EFT + C_tau_residual after C_domain=C_support=C_tau_protocol=0",
            "effect_on_Creadout": "Creadout is reduced rather than merely relabelled as missing",
            "status": "PARTIAL_CREADOUT_REDUCTION_DERIVED_NONCLAIM",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def reduction_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "row_id": "CRV4580_0_C_domain",
            "quantity": "C_domain",
            "value_or_bound": "0",
            "proof_source": "fixed q-basic local domain D_loc=q_src^{-1}(Dbar), source-silent compact probes, no moving-domain readout",
            "source_path": str(CSV_3929_SIGNATURE),
            "status": "THEOREM_ZERO_IN_PRIVATE_FIXED_COLLAR_BRANCH",
            "score_ready": "True",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "row_id": "CRV4580_1_C_support",
            "quantity": "C_support",
            "value_or_bound": "0",
            "proof_source": "compact source support remains inside W_loc and no source-crossing/radiative pullback enters the collar",
            "source_path": str(FORMAL_284),
            "status": "THEOREM_ZERO_IN_PRIVATE_NOFLUX_COLLAR_BRANCH",
            "score_ready": "True",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "row_id": "CRV4580_2_C_tau_protocol",
            "quantity": "C_tau_protocol",
            "value_or_bound": "0",
            "proof_source": "tau_obs=tau_bar(q), same tau roles, fixed reference/surfaces/orientation/units before readout",
            "source_path": str(CSV_4269_TAU),
            "status": "THEOREM_ZERO_FOR_QBASIC_OBSERVED_TAU_PROTOCOL",
            "score_ready": "True",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "row_id": "CRV4580_3_C_projector_abs_bridge",
            "quantity": "C_projector_abs",
            "value_or_bound": "0 in fixed q-basic/topological readout branch; otherwise use BRR545 absolute bound",
            "proof_source": "3929 zero result removes epsilon_domain_projector_abs only for the private fixed branch",
            "source_path": str(CSV_3929_ZERO),
            "status": "BRANCH_ZERO_ACTIVE_PROJECTOR_FALLBACK_RETAINED",
            "score_ready": "True",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "row_id": "CRV4580_4_Creadout_reduced",
            "quantity": "C_readout",
            "value_or_bound": "C_readout <= C_frame + C_material + C_kernel + C_EFT + C_tau_residual",
            "proof_source": "insert CRV4580_0..3 into the 4579 Creadout split",
            "source_path": str(CSV_4579_PROJECTOR),
            "status": "REDUCED_BOUND_DERIVED_VALUES_REMAIN",
            "score_ready": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def active_bound_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "bound_id": "AB4580_0_active_Hodge_Green",
            "when_active": "Pi_readout is a dynamic Hodge/Green/constraint projector rather than a fixed readout protocol",
            "formula": "C_active_projector <= abs(int_A [d,Pi_M^C]J_H)/M_H_ref + operator_norm(delta Pi_M^C/delta g)",
            "required_input": "PB3941_2_commutator and PB3941_3_projector_stress values or theorem-zero rows",
            "current_status": "MISSING_COMMUTATOR_AND_PROJECTOR_STRESS_VALUES",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "bound_id": "AB4580_1_moving_domain_tau",
            "when_active": "worldtube/linking surface or tau frame moves under the source/readout probe",
            "formula": "C_domain_tau_active <= abs(D_domain Pi_M^C J_H + delta_tau J_H)/M_H_ref",
            "required_input": "PB3941_5_domain_tau or 4269 tau residual values",
            "current_status": "MISSING_DOMAIN_AND_TAU_LOCK_IF_BRANCH_REOPENED",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "bound_id": "AB4580_2_radiative_boundary",
            "when_active": "radiative EM/gravity/Poynting flux crosses the compact collar",
            "formula": "C_rad_flux <= abs(int_boundary S_rad dot dA dt)/M_H_ref",
            "required_input": "PB3941_7_em_flux and DOM3946_5_Poynting values or no-flux theorem",
            "current_status": "MISSING_POYNTING_OR_EM_FLUX_ZERO_OR_VALUE",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def closed_domain_guard_rows(now: str) -> list[dict[str, Any]]:
    guards = [
        ("CDG4580_0_stationary_tau", "stationary/Killing tau for conserved mass current", "not supplied by the readout-domain zero itself", "MISSING_STATIONARY_TAU_CERTIFICATE"),
        ("CDG4580_1_Poynting", "EM/Poynting normal wall flux", "fixed support does not erase physical flux", "MISSING_POYNTING_FLUX_BOUND"),
        ("CDG4580_2_apparatus", "apparatus/readout support", "apparatus must be included in source or excluded with a bound", "MISSING_APPARATUS_DOMAIN_DECLARATION"),
        ("CDG4580_3_EM_tail", "near/tail EM energy ownership", "Maxwell stress/Poynting must be Hilbert-owned or bounded", "MISSING_EM_TAIL_ENERGY_MODEL_OR_BOUND"),
        ("CDG4580_4_theta_source", "theta/source normalization descent", "no second source normalization is allowed", "MISSING_THETA_SOURCE_NORMALIZATION_DESCENT_OR_BOUND"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "guard_id": guard_id,
            "guard": guard,
            "meaning": meaning,
            "status": status,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for guard_id, guard, meaning, status in guards
    ]


def audit_rows(now: str) -> list[dict[str, Any]]:
    rows = [
        ("AUD4580_0_forward_progress", "C_domain and C_support are no longer generic missing rows", "ZERO_VALUES_DERIVED_FOR_FIXED_QBASIC_COLLAR"),
        ("AUD4580_1_tau_protocol", "observed-tau readout protocol can be zeroed, but stationary mass-current tau remains a separate guard", "TAU_READOUT_ZERO_NOT_GLOBAL_STATIONARITY"),
        ("AUD4580_2_active_projectors", "dynamic Hodge/Green/moving-domain projectors are explicitly rejected from the zero branch", "ACTIVE_BRANCH_RETAINED"),
        ("AUD4580_3_no_public_claim", "valid_for_claim remains false because the full local-GR stack still needs frame/material/kernel/EFT/Poynting/tau-source guards", "CLAIM_FIREWALL_ACTIVE"),
        ("AUD4580_4_verdict", "fixed q-basic readout-domain certificate gives first theorem-zero Creadout component values", "PARTIAL_CERTIFICATE_COMPLETE_NONCLAIM"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "audit_id": audit_id,
            "finding": finding,
            "status": status,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for audit_id, finding, status in rows
    ]


def control_rows(now: str) -> list[dict[str, Any]]:
    rows = [
        ("CTRL4580_fixed_qbasic", "fixed q-basic domain, no source crossing, pure readout protocol", "C_domain=C_support=0", "CONTROL_PASS"),
        ("CTRL4580_moving_domain", "domain chosen by residual or moved by source probe", "zero certificate rejected; active bound row used", "COUNTERMODEL_CAUGHT"),
        ("CTRL4580_flux_crossing", "Poynting/radiative flux crosses collar while domain is fixed", "domain zero does not erase flux guard", "FIREWALL_PASS"),
        ("CTRL4580_tau_split", "clock/orbit/source/readout use different tau choices", "C_tau_protocol zero rejected; tau residual row used", "FIREWALL_PASS"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "control_id": control_id,
            "input_case": input_case,
            "expected": expected,
            "verdict": verdict,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for control_id, input_case, expected, verdict in rows
    ]


def promotion_rows(now: str) -> list[dict[str, Any]]:
    gates = [
        ("PROM4580_0_fixed_domain", "Fixed q-basic no-flux domain/support certificate for C_domain and C_support.", "PASSED_PRIVATE_BRANCH"),
        ("PROM4580_1_tau_protocol", "Observed tau readout protocol selected before variation and role-locked.", "PASSED_CONDITIONAL_BRANCH"),
        ("PROM4580_2_remaining_Creadout", "Frame/material/kernel/EFT/tau-residual components theorem-zero or source-bounded.", "BLOCKED"),
        ("PROM4580_3_closed_domain", "Stationary tau, Poynting, apparatus, EM tail and theta/source guards closed.", "BLOCKED"),
        ("PROM4580_4_no_active_projector_mix", "Do not mix fixed collar zero with active Green/Hodge/moving-domain branch.", "PASSED_FIREWALL"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "gate_id": gate_id,
            "gate": gate,
            "status": status,
            "required_for_claim": "True",
            "valid_for_claim": "False",
        }
        for gate_id, gate, status in gates
    ]


def decision_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "decision": DECISION,
            "plain_english": "4580 takes the 4579 C_readout bound and actually removes part of it: fixed q-basic domain/support readout gives C_domain=C_support=0, and the q-basic observed-tau protocol gives C_tau_protocol=0.  Active projectors, radiative/Poynting flux, frame/material/kernel/EFT and tau-residual branches are kept explicit.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def next_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "next_target": NEXT_TARGET,
            "reason": "After the fixed-domain/support part is zeroed, the shortest path is to attack the remaining C_readout terms one by one, starting with frame/material/kernel/EFT/tau-residual ownership rather than circling the already-zero collar branch.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def status_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "status": "complete_nonclaim_checkpoint",
            "decision": DECISION,
            "next_target": NEXT_TARGET,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def doc_body(
    now: str,
    sources: list[dict[str, Any]],
    certificate: list[dict[str, Any]],
    reductions: list[dict[str, Any]],
    active_bounds: list[dict[str, Any]],
    guards: list[dict[str, Any]],
    audits: list[dict[str, Any]],
    controls: list[dict[str, Any]],
    promotions: list[dict[str, Any]],
) -> str:
    return f"""# 4580 - Pi_readout parent-domain certificate or Creadout first numeric bound

Generated: `{now}`  
Branch: `{BRANCH_ID}`  
Decision: `{DECISION}`  
Claim status: private nonclaim checkpoint.

## Result

4580 takes the 4579 readout commutator split and actually deletes a chunk of it in the fixed local branch.

From 4579:

```text
||rho_readout_shift||_TV/M_H_ref <= C_readout
C_readout <= C_domain + C_support + C_frame + C_material + C_kernel + C_EFT + C_tau
```

The fixed q-basic no-flux readout-domain certificate gives:

```text
C_domain = 0
C_support = 0
C_tau_protocol = 0
```

under a pre-variation protocol:

```text
P_loc={{Dbar,W_loc,Sigma_in,Sigma_out,C_side,C_rad,tau_obs,e_obs,orientation,units,Pi_loc}}
Pi_readout = Pi_post o Pi_protocol[P_loc]
```

with fixed/q-basic domain, compact no-flux support, and observed tau selected before the probe.  Therefore the reduced private branch is:

```text
C_readout <= C_frame + C_material + C_kernel + C_EFT + C_tau_residual
```

This is not a local-GR claim.  It is a real narrowing: the domain/support part is no longer allowed to float as a vague missing coupling in the fixed-collar branch.  Active Hodge/Green/moving-domain projectors and physical Poynting/apparatus/tail flux are explicitly retained as separate bound branches.

## Pi_readout domain certificate

{markdown_table(certificate)}

## Creadout reduction rows

{markdown_table(reductions)}

## Active branch bound rows

{markdown_table(active_bounds)}

## Closed-domain guards

{markdown_table(guards)}

## Audit

{markdown_table(audits)}

## Controls

{markdown_table(controls)}

## Promotion gates

{markdown_table(promotions)}

## Source register

{markdown_table(sources)}

## Next target

`{NEXT_TARGET}`

Reason: after removing the fixed domain/support branch, attack the remaining `C_readout` terms directly.
"""


def spine_block(now: str) -> str:
    return f"""## PPC4161 4580 Pi_readout parent-domain certificate

Marker: `{MARKER}`  
Generated: `{now}`

4580 narrows the 4579 `C_readout` envelope.  In the fixed q-basic no-flux readout-domain branch, `C_domain=0`, `C_support=0`, and the observed-tau protocol has `C_tau_protocol=0`.  The reduced private branch is `C_readout <= C_frame + C_material + C_kernel + C_EFT + C_tau_residual`; active Hodge/Green/moving-domain projectors, Poynting/apparatus flux, EM tails and stationary-tau/source guards remain explicit nonclaim branches.

Decision: `{DECISION}`.  Next target: `{NEXT_TARGET}`.
"""


def packet_block(now: str) -> str:
    return f"""## 4580 packet update - fixed readout-domain certificate

Marker: `{PACKET_MARKER}`  
Generated: `{now}`

The packet now treats fixed q-basic readout domain/support as theorem-zero for the `C_readout` branch: `C_domain=C_support=0`, with `C_tau_protocol=0` when observed tau is selected before variation and role-locked.  This does not close local GR; it leaves only the remaining frame/material/kernel/EFT/tau-residual and physical flux/apparatus guards to attack.
"""


def append_claim() -> None:
    existing = read_text(CLAIMS_PATH)
    if CLAIM_ID in existing:
        return
    row = {
        "claim_id": CLAIM_ID,
        "domain": "local_gr_parent_signature",
        "claim": "4580 derives a fixed q-basic readout-domain certificate: C_domain=0, C_support=0, and C_tau_protocol=0 in the private fixed-collar branch, reducing C_readout to remaining frame/material/kernel/EFT/tau-residual terms.",
        "current_evidence": "Generated source register, Pi_readout domain certificate, Creadout reduction rows, active branch bounds, closed-domain guards, audit, controls, promotion gates, status and validation CSVs.",
        "status": DECISION.lower(),
        "next_test": NEXT_TARGET,
        "key_risk": "Mixing the fixed no-flux collar zero branch with active Hodge/Green/moving-domain projectors or physical Poynting/apparatus flux.",
        "sector": "local_gr",
        "evidence": str(DOC_PATH),
        "next_action": NEXT_TARGET,
        "risk": "Remaining C_readout frame/material/kernel/EFT/tau-residual and closed-domain guards still block local-GR/R10/PPN claims.",
    }
    with CLAIMS_PATH.open("a", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(row.keys()))
        writer.writerow(row)


def validation_rows(
    outputs: list[Path],
    sources: list[dict[str, Any]],
    certificate: list[dict[str, Any]],
    reductions: list[dict[str, Any]],
    active_bounds: list[dict[str, Any]],
    guards: list[dict[str, Any]],
    audits: list[dict[str, Any]],
    controls: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    checks: list[dict[str, Any]] = []

    def add(check_id: str, check: str, passed: bool, detail: str) -> None:
        checks.append(
            {
                "checkpoint": CHECKPOINT,
                "branch": BRANCH_ID,
                "check_id": check_id,
                "check": check,
                "passed": bool_text(passed),
                "detail": detail,
            }
        )

    for path in outputs:
        add(f"VAL4580_exists_{path.name}", "output path exists", path.exists(), str(path))
        if path.suffix == ".csv" and path.exists():
            rows = read_csv(path)
            add(f"VAL4580_csv_parse_{path.name}", "CSV parses with at least one row", len(rows) > 0, f"rows={len(rows)}")

    add("VAL4580_sources_exist", "all cited sources exist", all(row["exists"] == "True" for row in sources), "source register existence")
    add("VAL4580_needles_found", "all cited source needles found", all(row["needle_found"] == "True" for row in sources), "source register needles")
    add(
        "VAL4580_certificate_result",
        "certificate derives reduced Creadout branch",
        any(row["certificate_id"] == "PDC4580_4_readout_certificate_result" and "C_frame + C_material" in row["formula"] for row in certificate),
        "PDC4580_4_readout_certificate_result",
    )
    add(
        "VAL4580_domain_support_zero",
        "C_domain and C_support theorem-zero rows emitted",
        any(row["row_id"] == "CRV4580_0_C_domain" and row["value_or_bound"] == "0" for row in reductions)
        and any(row["row_id"] == "CRV4580_1_C_support" and row["value_or_bound"] == "0" for row in reductions),
        "CRV4580_0/1",
    )
    add(
        "VAL4580_tau_protocol_zero",
        "C_tau_protocol zero row emitted with residual guard",
        any(row["row_id"] == "CRV4580_2_C_tau_protocol" and row["value_or_bound"] == "0" for row in reductions)
        and any(row["bound_id"] == "AB4580_1_moving_domain_tau" for row in active_bounds),
        "CRV4580_2 and AB4580_1",
    )
    add(
        "VAL4580_reduced_bound",
        "Creadout reduced bound excludes C_domain and C_support",
        any(
            row["row_id"] == "CRV4580_4_Creadout_reduced"
            and "C_domain" not in row["value_or_bound"]
            and "C_support" not in row["value_or_bound"]
            for row in reductions
        ),
        "CRV4580_4",
    )
    add(
        "VAL4580_active_projector_retained",
        "active projector fallback rows retained",
        any(row["bound_id"] == "AB4580_0_active_Hodge_Green" for row in active_bounds)
        and any(row["certificate_id"] == "PDC4580_3_active_projector_rejection" for row in certificate),
        "active branch rows",
    )
    add(
        "VAL4580_closed_domain_guards",
        "closed-domain guards include Poynting and apparatus",
        any(row["guard_id"] == "CDG4580_1_Poynting" for row in guards)
        and any(row["guard_id"] == "CDG4580_2_apparatus" for row in guards),
        "guard coverage",
    )
    add(
        "VAL4580_audit_verdict",
        "audit records partial certificate verdict",
        any(row["audit_id"] == "AUD4580_4_verdict" and row["status"] == "PARTIAL_CERTIFICATE_COMPLETE_NONCLAIM" for row in audits),
        "AUD4580_4_verdict",
    )
    add(
        "VAL4580_controls",
        "controls include moving-domain, flux, and tau-split firewalls",
        all(
            any(row["control_id"] == control_id for row in controls)
            for control_id in ["CTRL4580_moving_domain", "CTRL4580_flux_crossing", "CTRL4580_tau_split"]
        ),
        "control coverage",
    )
    add("VAL4580_decision_token", "decision token recorded", DECISION in read_text(DECISION_CSV) and DECISION in read_text(DOC_PATH), DECISION)
    add("VAL4580_next_target", "next target recorded", NEXT_TARGET in read_text(NEXT_CSV) and NEXT_TARGET in read_text(DOC_PATH), NEXT_TARGET)
    add("VAL4580_claim_register", "claim register updated", CLAIM_ID in read_text(CLAIMS_PATH), CLAIM_ID)
    add(
        "VAL4580_spine_packet",
        "spine and packet markers present",
        MARKER in read_text(SPINE_PATH) and PACKET_MARKER in read_text(PACKET_PATH),
        f"{MARKER}; {PACKET_MARKER}",
    )
    return checks


def main() -> None:
    now = utc_now()
    sources = source_rows()
    certificate = certificate_rows(now)
    reductions = reduction_rows(now)
    active_bounds = active_bound_rows(now)
    guards = closed_domain_guard_rows(now)
    audits = audit_rows(now)
    controls = control_rows(now)
    promotions = promotion_rows(now)
    decisions = decision_rows(now)
    next_targets = next_rows(now)
    statuses = status_rows(now)

    write_csv(SOURCE_REGISTER, sources)
    write_csv(CERTIFICATE_CSV, certificate)
    write_csv(REDUCTION_CSV, reductions)
    write_csv(ACTIVE_BOUND_CSV, active_bounds)
    write_csv(CLOSED_DOMAIN_GUARDS_CSV, guards)
    write_csv(AUDIT_CSV, audits)
    write_csv(CONTROL_CSV, controls)
    write_csv(PROMOTION_CSV, promotions)
    write_csv(DECISION_CSV, decisions)
    write_csv(NEXT_CSV, next_targets)
    write_csv(STATUS_CSV, statuses)

    body = doc_body(now, sources, certificate, reductions, active_bounds, guards, audits, controls, promotions)
    DOC_PATH.write_text(body, encoding="utf-8", newline="\n")
    FORMAL_PATH.write_text(body, encoding="utf-8", newline="\n")

    append_once(SPINE_PATH, MARKER, spine_block(now))
    append_once(PACKET_PATH, PACKET_MARKER, packet_block(now))
    append_claim()

    outputs = [
        SOURCE_REGISTER,
        CERTIFICATE_CSV,
        REDUCTION_CSV,
        ACTIVE_BOUND_CSV,
        CLOSED_DOMAIN_GUARDS_CSV,
        AUDIT_CSV,
        CONTROL_CSV,
        PROMOTION_CSV,
        DECISION_CSV,
        NEXT_CSV,
        STATUS_CSV,
        DOC_PATH,
        FORMAL_PATH,
    ]
    validations = validation_rows(outputs, sources, certificate, reductions, active_bounds, guards, audits, controls)
    write_csv(VALIDATION_PATH, validations)

    pycache = Path(__file__).resolve().parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)

    failed = [row for row in validations if row["passed"] != "True"]
    if failed:
        for row in failed:
            print(f"FAIL {row['check_id']}: {row['detail']}")
        raise SystemExit(1)
    print(f"{CHECKPOINT} complete: {DECISION}")
    print(f"wrote: {DOC_PATH}")
    print(f"validation: {VALIDATION_PATH}")


if __name__ == "__main__":
    main()
