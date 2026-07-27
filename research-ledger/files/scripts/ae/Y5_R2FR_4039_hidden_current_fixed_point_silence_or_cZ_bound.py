from __future__ import annotations

import csv
import py_compile
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List


ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
SOURCE_DIR = ROOT / "source-intake" / "mts_residuals"
MICRO_DIR = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
FORMALIZATION = PROJECT / "formalization-workbench"
SCRIPT_PATH = Path(__file__).resolve()
DOC_PATH = ROOT / "4039-Y5-R2FR-hidden-current-fixed-point-silence-or-cZ-bound.md"

OUTPUTS = {
    "source_register": SOURCE_DIR / "P8_Y5_R2FR_4039_SOURCE_REGISTER.csv",
    "component_split": SOURCE_DIR / "P8_Y5_R2FR_4039_CZ_COMPONENT_SPLIT.csv",
    "fixed_point_theorem": SOURCE_DIR / "P8_Y5_R2FR_4039_FIXED_POINT_CURRENT_THEOREM.csv",
    "zeroed_components": SOURCE_DIR / "P8_Y5_R2FR_4039_ZEROED_CZ_COMPONENTS.csv",
    "bound_template": SOURCE_DIR / "P8_Y5_R2FR_4039_CZ_BOUND_TEMPLATE.csv",
    "remaining_residuals": SOURCE_DIR / "P8_Y5_R2FR_4039_REMAINING_LOCAL_RESIDUAL_VECTOR.csv",
    "evaluator": SOURCE_DIR / "P8_Y5_R2FR_4039_EVALUATOR_RESULTS.csv",
    "decision_gate": SOURCE_DIR / "P8_Y5_R2FR_4039_DECISION_GATE.csv",
    "claim_gate": SOURCE_DIR / "P8_Y5_R2FR_4039_CLAIM_GATE.csv",
    "next_target": SOURCE_DIR / "P8_Y5_R2FR_4039_NEXT_TARGET.csv",
    "status": SOURCE_DIR / "P8_Y5_R2FR_4039_STATUS.csv",
    "validation": SOURCE_DIR / "P8_Y5_BRR545_4039_VALIDATION.csv",
}


def timestamp() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def write_csv(path: Path, rows: List[Dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"empty rows for {path}")
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
    specs = [
        ("SRC4039_0", ROOT / "4038-Y5-R2FR-Poynting-no-flux-and-boundary-reference-theorem-or-flux-bound.md", "Remaining live local residuals: `c_Z`, `c_norm`, `c_nonEH`", "immediate predecessor naming c_Z as next leak"),
        ("SRC4039_1", SOURCE_DIR / "P8_Y5_R2FR_4038_REMAINING_LOCAL_RESIDUAL_VECTOR.csv", "hidden/domain/memory current J_Z", "current residual definition"),
        ("SRC4039_2", SOURCE_DIR / "P8_Y5_R2FR_4038_ZEROED_FLUX_BOUNDARY_COUPLINGS.csv", "c_B*B_source=0", "boundary source already zeroed in selected branch"),
        ("SRC4039_3", SOURCE_DIR / "P8_Y5_R2FR_4037_ZEROED_DIRECT_COUPLINGS.csv", "c_T_direct=0", "direct source couplings already zeroed"),
        ("SRC4039_4", SOURCE_DIR / "P8_GAMMA_OWNER_CANDIDATE_ACTION.csv", "Gamma_eff = Gamma0 + 1/2 M_AB", "Gamma-owner quadratic/double-zero route"),
        ("SRC4039_5", SOURCE_DIR / "P8_Y5_R2FR_4026_EXPLICIT_GAMMA_DENSITY_CANDIDATE.csv", "local fixed point A_mu=0, gamma=0", "explicit response fixed-point ansatz"),
        ("SRC4039_6", SOURCE_DIR / "P8_MIN_PARENT_LOCAL_GR_ACTION_BLOCKS.csv", "Phi=Phi0; dV(Phi0)=0; Hessian(V)>0", "minimal local fixed-point silence block"),
        ("SRC4039_7", SOURCE_DIR / "P8_Y5_R2FR_3645_JX_VARIATION_DERIVATION.csv", "J_X^hidden_domain", "effective hidden/domain current definition"),
        ("SRC4039_8", SOURCE_DIR / "P8_Y5_R2FR_3645_JX_COMPONENT_OWNER_AUDIT.csv", "MISSING_HIDDEN_DOMAIN_CURRENT_OWNER", "component owner audit"),
        ("SRC4039_9", SOURCE_DIR / "P8_Y5_R2FR_3894_MEMORY_JX_COMPONENT_CLOSURE_GATE.csv", "PARTIAL_JX_CLOSURE_ONLY", "memory/current closure gate"),
        ("SRC4039_10", MICRO_DIR / "domain_selector_audit_nonclaim_1514.csv", "THEOREM_NOT_PROVEN_CURRENT_CORPUS", "domain selector obstruction guard"),
        ("SRC4039_11", ROOT / "1127-Y5-R10-local-vs-FLRW-branch-selector-no-flux-certificate.md", "global all-domain zero is forbidden", "guard against erasing cosmology/memory"),
    ]
    rows: List[Dict[str, object]] = []
    for source_id, path, needle, role in specs:
        exists = path.exists()
        text = read_text(path) if exists else ""
        rows.append(
            {
                "source_id": source_id,
                "path": str(path),
                "exists": exists,
                "needle": needle,
                "needle_found": needle in text,
                "role": role,
                "timestamp_utc": ts,
            }
        )
    return rows


def component_split_rows(ts: str) -> List[Dict[str, object]]:
    return [
        {
            "component_id": "CZ4039_0_direct_source",
            "component": "J_Z^direct_source",
            "definition": "direct matter trace/source-only EM/source prefactor pieces already represented by c_T,c_EM,C_XF2",
            "selected_branch_result": "zero by 4037 source-clean packet",
            "status": "ZEROED_PREVIOUSLY",
            "feeds": "none in selected packet",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "component_id": "CZ4039_1_boundary_flux",
            "component": "J_Z^boundary_flux",
            "definition": "boundary/Poynting/collar flux source pieces already represented by c_Poynting,c_B",
            "selected_branch_result": "zero by 4038 stationary no-flux and fixed-reference theorem",
            "status": "ZEROED_PREVIOUSLY",
            "feeds": "none in selected stationary/fixed-reference packet",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "component_id": "CZ4039_2_Gamma_response",
            "component": "J_Z^Gamma",
            "definition": "-delta_Z I_Gamma/sqrt(h) for the response/Gamma owner sector",
            "selected_branch_result": "zero if Gamma owner is even/quadratic and local response fields sit at Z=0 fixed point with positive Hessian",
            "status": "ZERO_IN_SELECTED_DOUBLE_ZERO_FIXED_POINT",
            "feeds": "no hidden response current in local vacuum branch",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "component_id": "CZ4039_3_selector_projector",
            "component": "J_Z^selector_projector",
            "definition": "-delta_Z(S_selector+S_projector)/sqrt(h)",
            "selected_branch_result": "zero only for fixed local selector with X_D=0,Qcoh_D=0, projector stress=0 and no wall motion",
            "status": "ZERO_IN_SELECTED_FIXED_SELECTOR_BRANCH_NOT_GLOBAL",
            "feeds": "domain/projector residual if selector wall moves",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "component_id": "CZ4039_4_history_tail",
            "component": "J_Z^history_tail",
            "definition": "local projection of memory/nonlocal kernel tail into the compact exterior branch",
            "selected_branch_result": "not zero from current evidence unless local kernel support/gap/tail theorem is supplied",
            "status": "RETAINED_AS_BOUND_BRANCH",
            "feeds": "c_Z finite residual, clock/Gdot/orbital/local PPN if nonzero",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "component_id": "CZ4039_5_total",
            "component": "J_Z^total",
            "definition": "J_Z^direct_source+J_Z^boundary_flux+J_Z^Gamma+J_Z^selector_projector+J_Z^history_tail",
            "selected_branch_result": "reduced to history_tail and any rejected selector-wall clause; no cancellation credit allowed",
            "status": "PARTIAL_ZERO_WITH_FINITE_TAIL_BOUND",
            "feeds": "next 4040 memory-tail/selector-wall gate",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
    ]


def fixed_point_theorem_rows(ts: str) -> List[Dict[str, object]]:
    return [
        {
            "theorem_id": "FPC4039_0_operator",
            "piece": "positive local response operator",
            "formula": "I_Gamma = int sqrt(h)[1/2 D_AB grad Z^A grad Z^B + 1/2 M_AB Z^A Z^B + O(Z^4)]",
            "condition": "D_AB positive, M_AB positive/semi-positive with no zero-mode except fixed/topological constants",
            "result": "Euler equation has local fixed solution Z=0 under source-free/no-flux boundary data",
            "status": "CONDITIONAL_FIXED_POINT_THEOREM",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "theorem_id": "FPC4039_1_current_zero",
            "piece": "Gamma current silence",
            "formula": "J_Z^Gamma := -delta_Z I_Gamma/sqrt(h); at Z=0 with even/quadratic origin, J_Z^Gamma=0 and first variation vanishes",
            "condition": "zero origin is parent-owned; no affine shift; no linear hidden-source vertex",
            "result": "Gamma/response hidden current is zero in the selected local fixed-point packet",
            "status": "J_GAMMA_ZERO_IN_SELECTED_FIXED_POINT",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "theorem_id": "FPC4039_2_selector_zero",
            "piece": "selector/projector current silence",
            "formula": "J_Z^selector = -delta_Z(S_selector+S_projector)/sqrt(h)",
            "condition": "local compact branch fixes selector variables and kills wall/projector stress: X_D=0, Qcoh_D=0, Pi_selector=0",
            "result": "selector/projector current is zero only inside the selected fixed-selector local branch",
            "status": "SELECTOR_ZERO_SELECTED_BRANCH_ONLY",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "theorem_id": "FPC4039_3_memory_guard",
            "piece": "do not globally kill memory",
            "formula": "local tail zero is not the same as global memory zero",
            "condition": "FLRW/cosmology branch remains active; compact local branch may be memory-silent only by support/gap/tail theorem",
            "result": "J_Z^history_tail remains retained until local kernel decoupling is proven or bounded",
            "status": "MEMORY_TAIL_RETAINED_GUARD",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "theorem_id": "FPC4039_4_result",
            "piece": "c_Z result",
            "formula": "c_Z J_Z -> c_Z J_Z^tail + c_Z J_Z^wall_if_selector_rejected",
            "condition": "4037/4038 plus FPC4039_0..3",
            "result": "c_Z broad leak is narrowed to a finite tail/wall residual, not a full zero theorem",
            "status": "C_Z_PARTIAL_ZERO_BOUND_BRANCH_ACTIVE",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
    ]


def zeroed_rows(ts: str) -> List[Dict[str, object]]:
    return [
        {
            "zero_id": "ZERO4039_0_direct",
            "component": "J_Z^direct_source",
            "zero_law": "direct source-only pieces vanish by the selected source-clean packet",
            "proof_link": "4037 zeroed c_T,c_EM,C_XF2",
            "status": "ZERO_IN_SELECTED_PACKET",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "zero_id": "ZERO4039_1_boundary",
            "component": "J_Z^boundary_flux",
            "zero_law": "flux/boundary pieces vanish by stationary no-flux plus fixed source-blind reference",
            "proof_link": "4038 zeroed c_Poynting,c_B",
            "status": "ZERO_IN_SELECTED_PACKET",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "zero_id": "ZERO4039_2_gamma",
            "component": "J_Z^Gamma",
            "zero_law": "even/quadratic Gamma owner at Z=0 has no linear current",
            "proof_link": "FPC4039_0,FPC4039_1",
            "status": "ZERO_IN_SELECTED_FIXED_POINT",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "zero_id": "ZERO4039_3_selector",
            "component": "J_Z^selector_projector",
            "zero_law": "fixed local selector/projector branch has no wall motion or projector stress",
            "proof_link": "FPC4039_2",
            "status": "ZERO_ONLY_IN_SELECTED_FIXED_SELECTOR_BRANCH",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
    ]


def bound_rows(ts: str) -> List[Dict[str, object]]:
    return [
        {
            "bound_id": "CZB4039_0_tail",
            "symbol": "c_Z*J_Z^history_tail",
            "used_if": "local memory kernel support/gap/tail theorem is not proven",
            "definition": "J_Z^tail = P_loc integral K_mem(x,y) source_or_history(y) dy after local projection",
            "amplitude_bound": "|A_Z_tail| <= C_G(D_Z,M_Z,L_collar)*|c_Z|*||J_Z^tail||_1",
            "alpha_or_PPN_link": "feeds scalar/vector hair and local residual envelope before R10/PPN/clock/orbital scoring",
            "missing_numeric_inputs": "D_Z,M_Z_or_lambda_Z,K_mem_tail_norm,source_history_norm,projection_norm,c_Z",
            "smoke_result": "SCHEMA_READY_NUMERIC_CLAIM_BLOCKED",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "bound_id": "CZB4039_1_wall",
            "symbol": "c_Z*J_Z^selector_wall",
            "used_if": "fixed selector/no-wall branch is rejected",
            "definition": "J_Z^wall = shell or domain-wall variation supported on transition surface Sigma",
            "amplitude_bound": "|A_Z_wall| <= C_G*|c_Z|*(||jump(D_Z n.grad Z)||_Sigma + ||delta S_wall/delta Z||_Sigma)",
            "alpha_or_PPN_link": "feeds transition-scale/local-cosmology matching residual and possible orbital/PPN hair",
            "missing_numeric_inputs": "transition_support,jump_condition,shell_norm,D_Z,lambda_Z,c_Z",
            "smoke_result": "SCHEMA_READY_NUMERIC_CLAIM_BLOCKED",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "bound_id": "CZB4039_2_total_envelope",
            "symbol": "c_Z*J_Z^remaining",
            "used_if": "either tail or wall residual remains",
            "definition": "J_Z^remaining = J_Z^history_tail + J_Z^selector_wall_if_rejected",
            "amplitude_bound": "|A_Z| <= |A_Z_tail| + |A_Z_wall| with no cancellation credit",
            "alpha_or_PPN_link": "local-GR promotion blocked until this envelope is zero or below arena bounds",
            "missing_numeric_inputs": "all tail/wall norm inputs plus arena projection constants",
            "smoke_result": "ABSOLUTE_ENVELOPE_DEFINED_NOT_NUMERIC",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
    ]


def remaining_rows(ts: str) -> List[Dict[str, object]]:
    return [
        {
            "residual_id": "REM4039_0_tail",
            "symbol": "c_Z_tail",
            "residual": "local memory/history kernel tail or selector-wall source if fixed-selector branch is rejected",
            "current_route": "derive local kernel support/gap/tail silence and selector no-wall theorem, or fill finite c_Z envelope",
            "priority": "next",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "residual_id": "REM4039_1_norm",
            "symbol": "c_norm",
            "residual": "universal source/action normalization drift",
            "current_route": "route common mode into calibrated kappa_obs/Newton G or bound time/source variation",
            "priority": "high_after_cZ_tail",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "residual_id": "REM4039_2_nonEH",
            "symbol": "c_nonEH",
            "residual": "non-EH or higher-curvature metric operator leakage",
            "current_route": "show decoupling at local scale or compare to PPN/Cassini-style bounds",
            "priority": "high_after_cnorm",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
    ]


def evaluator_rows(ts: str) -> List[Dict[str, object]]:
    return [
        {
            "case_id": "CASE4039_0_selected_fixed_point",
            "verdict": "C_Z_NARROWED_NOT_FULLY_ZEROED",
            "zero_result": "direct,boundary,Gamma,response,readout and selected fixed-selector pieces are zero",
            "retained_result": "history-tail and selector-wall-if-rejected residuals require theorem or finite bound",
            "claim_result": "NO_PUBLIC_LOCAL_GR_CLAIM_FROM_4039",
            "next_action": "4040 should prove local memory-tail/support silence and selector no-wall, or instantiate c_Z envelope bounds",
            "timestamp_utc": ts,
        },
        {
            "case_id": "CASE4039_1_full_tail_silence_future",
            "verdict": "FULL_CZ_ZERO_REQUIRES_EXTRA_THEOREM",
            "zero_result": "would need J_Z^history_tail=0 and no selector wall in compact local branch",
            "retained_result": "not established in current evidence",
            "claim_result": "NO_PUBLIC_LOCAL_GR_CLAIM_FROM_4039",
            "next_action": "do not promote to local GR until tail/wall theorem or numeric bound exists",
            "timestamp_utc": ts,
        },
    ]


def decision_rows(ts: str) -> List[Dict[str, object]]:
    return [
        {
            "decision_id": "DEC4039_0_decompose",
            "decision": "Decompose c_Z J_Z into direct, boundary, Gamma, selector/projector, and history-tail components.",
            "status": "CZ_DECOMPOSED",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "decision_id": "DEC4039_1_zero_owned",
            "decision": "Inside the selected branch, direct, boundary, Gamma fixed-point, readout, and fixed-selector components are zero or previously zeroed.",
            "status": "OWNED_COMPONENTS_ZEROED_IN_SELECTED_BRANCH",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "decision_id": "DEC4039_2_retain_tail",
            "decision": "Do not zero local memory/history tail globally; retain it as a finite envelope unless a local support/gap theorem closes it.",
            "status": "TAIL_BOUND_BRANCH_RETAINED",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "decision_id": "DEC4039_3_next",
            "decision": "Move to 4040-Y5-R2FR-local-memory-tail-selector-wall-silence-or-cZ-envelope.md.",
            "status": "NEXT_TARGET_SELECTED",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
    ]


def claim_rows(ts: str) -> List[Dict[str, object]]:
    return [
        {
            "claim_id": "CLAIM4039_0_owned_cZ_pieces",
            "claim": "owned c_Z components are zero in selected local branch",
            "allowed": True,
            "scope": "internal selected branch only",
            "reason": "direct/boundary/Gamma/readout/fixed-selector pieces have explicit zero routes",
            "public_claim_allowed": False,
            "timestamp_utc": ts,
        },
        {
            "claim_id": "CLAIM4039_1_full_cZ_zero",
            "claim": "full c_Z is zero",
            "allowed": False,
            "scope": "complete hidden/domain/memory current",
            "reason": "history-tail and selector-wall residuals are not yet proven zero",
            "public_claim_allowed": False,
            "timestamp_utc": ts,
        },
        {
            "claim_id": "CLAIM4039_2_local_GR",
            "claim": "local GR/PPN/R10 pass",
            "allowed": False,
            "scope": "full local-gravity phenomenology",
            "reason": "c_Z tail, c_norm, c_nonEH, and PPN closure remain open",
            "public_claim_allowed": False,
            "timestamp_utc": ts,
        },
    ]


def next_rows(ts: str) -> List[Dict[str, object]]:
    return [
        {
            "row_id": "NEXT4039_0",
            "next_doc": "4040-Y5-R2FR-local-memory-tail-selector-wall-silence-or-cZ-envelope.md",
            "next_script": "scripts/Y5_R2FR_4040_local_memory_tail_selector_wall_silence_or_cZ_envelope.py",
            "why": "4039 narrowed c_Z to the local memory-tail and selector-wall leftovers; those must be proven zero locally or bounded before moving to c_norm.",
            "fallback": "if silence fails, instantiate finite c_Z envelope rows with tail/wall norms and arena projections",
            "timestamp_utc": ts,
        }
    ]


def status_rows(ts: str) -> List[Dict[str, object]]:
    return [
        {
            "status_id": "STATUS4039_0",
            "checkpoint": "4039",
            "canonical_status": "CZ_PARTIAL_ZERO_TAIL_BOUND_BRANCH_ACTIVE",
            "strongest_result": "c_Z is no longer a broad coupling hole: selected-branch owned pieces are zero; only memory-tail/selector-wall leftovers remain.",
            "still_missing": "local memory-tail support/gap theorem, selector no-wall theorem, or finite c_Z envelope numbers; then c_norm/Newton-G routing and c_nonEH/PPN closure",
            "public_claim_allowed": False,
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        }
    ]


def render_doc(ts: str, sources: List[Dict[str, object]]) -> str:
    found = sum(1 for row in sources if row["exists"] and row["needle_found"])
    total = len(sources)
    return f"""# 4039 - Hidden Current Fixed Point Silence Or cZ Bound

- Timestamp: `{ts}`
- Status: `private_nonclaim_checkpoint`
- Scope: `post-checkpoint-work` only; no `formalization-workbench` edits.
- Source needles found: `{found}/{total}`.

## What Actually Moved

4039 stops treating `c_Z` as one foggy hidden-current bucket. It splits

`J_Z = J_Z^direct + J_Z^boundary + J_Z^Gamma + J_Z^selector + J_Z^history_tail`.

The selected local branch already killed the first two groups:

- direct source/EM/source-prefactor pieces by 4037;
- Poynting and boundary/reference pieces by 4038.

## Fixed-Point Current Result

For the Gamma/response owner, use the local positive double-zero form

`I_Gamma = int sqrt(h)[1/2 D_AB grad Z^A grad Z^B + 1/2 M_AB Z^A Z^B + O(Z^4)]`.

At the local fixed point `Z=0`, with positive Hessian/gap, no affine shift, and no linear hidden-source vertex,

`J_Z^Gamma = -delta_Z I_Gamma/sqrt(h) = 0`.

For the selector/projector sector, the current is zero only inside the fixed local selector branch with `X_D=0`, `Qcoh_D=0`, no wall motion, and zero projector stress.

## What Is Still Not Killed

We do **not** globally kill memory. That would break the cosmology side.

The retained current is now sharply localized:

`c_Z J_Z -> c_Z J_Z^history_tail + c_Z J_Z^selector_wall_if_rejected`.

So `c_Z` is no longer an open-ended coupling mystery, but full `c_Z=0` is not claimed yet.

## Bound Interface

If the local tail/wall theorem fails:

- `|A_Z_tail| <= C_G(D_Z,M_Z,L_collar)*|c_Z|*||J_Z^tail||_1`;
- `|A_Z_wall| <= C_G*|c_Z|*(||jump(D_Z n.grad Z)||_Sigma + ||delta S_wall/delta Z||_Sigma)`;
- `|A_Z| <= |A_Z_tail| + |A_Z_wall|`, with no cancellation credit.

## Current Verdict

- Current evaluator result: `C_Z_NARROWED_NOT_FULLY_ZEROED`.
- Claim result: `NO_PUBLIC_LOCAL_GR_CLAIM_FROM_4039`.
- Remaining live local residuals: `c_Z_tail`, `c_norm`, `c_nonEH`.

## Next Target

- `4040-Y5-R2FR-local-memory-tail-selector-wall-silence-or-cZ-envelope.md`
- `scripts/Y5_R2FR_4040_local_memory_tail_selector_wall_silence_or_cZ_envelope.py`
"""


def validation_rows(
    ts: str,
    sources: List[Dict[str, object]],
    split: List[Dict[str, object]],
    theorem: List[Dict[str, object]],
    zeroed: List[Dict[str, object]],
    bounds: List[Dict[str, object]],
    remaining: List[Dict[str, object]],
    evaluator: List[Dict[str, object]],
    decisions: List[Dict[str, object]],
    claims: List[Dict[str, object]],
    next_target: List[Dict[str, object]],
    compile_ok: bool,
) -> List[Dict[str, object]]:
    def row(check_id: str, passed: bool, detail: str) -> Dict[str, object]:
        return {"check_id": check_id, "passed": bool(passed), "detail": detail, "timestamp_utc": ts}

    output_paths = [str(path) for path in OUTPUTS.values()] + [str(DOC_PATH), str(SCRIPT_PATH)]
    return [
        row("VAL4039_00_sources_exist", all(item["exists"] for item in sources), "all cited source paths exist"),
        row("VAL4039_01_needles_found", all(item["needle_found"] for item in sources), "all source needles found"),
        row("VAL4039_02_split_direct", any(item["component_id"] == "CZ4039_0_direct_source" for item in split), "direct source split row present"),
        row("VAL4039_03_split_gamma", any(item["component_id"] == "CZ4039_2_Gamma_response" for item in split), "Gamma response split row present"),
        row("VAL4039_04_split_tail", any(item["component_id"] == "CZ4039_4_history_tail" for item in split), "history tail split row present"),
        row("VAL4039_05_fixed_operator", any(item["theorem_id"] == "FPC4039_0_operator" for item in theorem), "fixed-point operator theorem present"),
        row("VAL4039_06_current_zero", any(item["theorem_id"] == "FPC4039_1_current_zero" for item in theorem), "Gamma current zero theorem present"),
        row("VAL4039_07_selector_zero", any(item["theorem_id"] == "FPC4039_2_selector_zero" for item in theorem), "selector zero theorem present"),
        row("VAL4039_08_memory_guard", any(item["theorem_id"] == "FPC4039_3_memory_guard" for item in theorem), "memory guard present"),
        row("VAL4039_09_partial_result", any(item["theorem_id"] == "FPC4039_4_result" for item in theorem), "partial c_Z result present"),
        row("VAL4039_10_zero_direct", any(item["component"] == "J_Z^direct_source" for item in zeroed), "direct zero row present"),
        row("VAL4039_11_zero_boundary", any(item["component"] == "J_Z^boundary_flux" for item in zeroed), "boundary zero row present"),
        row("VAL4039_12_zero_gamma", any(item["component"] == "J_Z^Gamma" for item in zeroed), "Gamma zero row present"),
        row("VAL4039_13_tail_bound", any(item["bound_id"] == "CZB4039_0_tail" for item in bounds), "tail bound row present"),
        row("VAL4039_14_wall_bound", any(item["bound_id"] == "CZB4039_1_wall" for item in bounds), "wall bound row present"),
        row("VAL4039_15_total_envelope", any(item["bound_id"] == "CZB4039_2_total_envelope" for item in bounds), "total envelope row present"),
        row("VAL4039_16_bound_nonclaim", all(item["valid_for_public_claim"] is False for item in bounds), "bounds remain nonclaim"),
        row("VAL4039_17_remaining_tail", any(item["symbol"] == "c_Z_tail" for item in remaining), "c_Z tail remains next residual"),
        row("VAL4039_18_remaining_norm", any(item["symbol"] == "c_norm" for item in remaining), "c_norm remains"),
        row("VAL4039_19_remaining_nonEH", any(item["symbol"] == "c_nonEH" for item in remaining), "c_nonEH remains"),
        row("VAL4039_20_current_verdict", any(item["case_id"] == "CASE4039_0_selected_fixed_point" for item in evaluator), "selected fixed-point evaluator present"),
        row("VAL4039_21_no_full_cZ_claim", any(item["claim_id"] == "CLAIM4039_1_full_cZ_zero" and item["allowed"] is False for item in claims), "full c_Z zero not claimed"),
        row("VAL4039_22_no_public_local_claim", all(item["public_claim_allowed"] is False for item in claims), "no public claims allowed"),
        row("VAL4039_23_next_decision", any(item["decision_id"] == "DEC4039_3_next" for item in decisions), "4040 next decision present"),
        row("VAL4039_24_next_target", bool(next_target and "4040" in str(next_target[0]["next_doc"])), "next target row present"),
        row("VAL4039_25_doc_written", DOC_PATH.exists(), "checkpoint doc written"),
        row("VAL4039_26_no_formalization_output", all(str(FORMALIZATION) not in path for path in output_paths), "no output targets formalization-workbench"),
        row("VAL4039_27_script_compiles", compile_ok, "script compiles"),
        row("VAL4039_28_private_guard", all(item["valid_for_public_claim"] is False for table in [split, theorem, zeroed, bounds, remaining, decisions] for item in table), "public-claim guard retained"),
    ]


def main() -> None:
    ts = timestamp()
    sources = source_rows(ts)
    split = component_split_rows(ts)
    theorem = fixed_point_theorem_rows(ts)
    zeroed = zeroed_rows(ts)
    bounds = bound_rows(ts)
    remaining = remaining_rows(ts)
    evaluator = evaluator_rows(ts)
    decisions = decision_rows(ts)
    claims = claim_rows(ts)
    next_target = next_rows(ts)
    status = status_rows(ts)

    DOC_PATH.write_text(render_doc(ts, sources), encoding="utf-8")
    write_csv(OUTPUTS["source_register"], sources)
    write_csv(OUTPUTS["component_split"], split)
    write_csv(OUTPUTS["fixed_point_theorem"], theorem)
    write_csv(OUTPUTS["zeroed_components"], zeroed)
    write_csv(OUTPUTS["bound_template"], bounds)
    write_csv(OUTPUTS["remaining_residuals"], remaining)
    write_csv(OUTPUTS["evaluator"], evaluator)
    write_csv(OUTPUTS["decision_gate"], decisions)
    write_csv(OUTPUTS["claim_gate"], claims)
    write_csv(OUTPUTS["next_target"], next_target)
    write_csv(OUTPUTS["status"], status)

    try:
        py_compile.compile(str(SCRIPT_PATH), doraise=True)
        compile_ok = True
    except py_compile.PyCompileError:
        compile_ok = False

    cache = SCRIPT_PATH.parent / "__pycache__"
    if cache.exists():
        shutil.rmtree(cache)

    checks = validation_rows(ts, sources, split, theorem, zeroed, bounds, remaining, evaluator, decisions, claims, next_target, compile_ok)
    write_csv(OUTPUTS["validation"], checks)
    passed = sum(1 for item in checks if item["passed"])
    total = len(checks)
    print(f"4039 validation: {passed}/{total} passed")
    if passed != total:
        for item in checks:
            if not item["passed"]:
                print(f"FAIL {item['check_id']}: {item['detail']}")
        raise SystemExit(1)
    print(f"Wrote {DOC_PATH}")


if __name__ == "__main__":
    main()
