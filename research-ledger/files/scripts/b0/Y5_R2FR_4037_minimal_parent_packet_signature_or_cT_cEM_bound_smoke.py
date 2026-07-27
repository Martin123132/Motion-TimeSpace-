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
FORMALIZATION = PROJECT / "formalization-workbench"
SCRIPT_PATH = Path(__file__).resolve()
DOC_PATH = ROOT / "4037-Y5-R2FR-minimal-parent-packet-signature-or-cT-cEM-bound-smoke.md"

OUTPUTS = {
    "source_register": SOURCE_DIR / "P8_Y5_R2FR_4037_SOURCE_REGISTER.csv",
    "packet_signature": SOURCE_DIR / "P8_Y5_R2FR_4037_MINIMAL_PARENT_PACKET_SIGNATURE.csv",
    "zeroed_couplings": SOURCE_DIR / "P8_Y5_R2FR_4037_ZEROED_DIRECT_COUPLINGS.csv",
    "bound_smoke": SOURCE_DIR / "P8_Y5_R2FR_4037_cT_cEM_BOUND_SMOKE_TEMPLATE.csv",
    "remaining_residuals": SOURCE_DIR / "P8_Y5_R2FR_4037_REMAINING_LOCAL_RESIDUAL_VECTOR.csv",
    "evaluator": SOURCE_DIR / "P8_Y5_R2FR_4037_EVALUATOR_RESULTS.csv",
    "decision_gate": SOURCE_DIR / "P8_Y5_R2FR_4037_DECISION_GATE.csv",
    "claim_gate": SOURCE_DIR / "P8_Y5_R2FR_4037_CLAIM_GATE.csv",
    "next_target": SOURCE_DIR / "P8_Y5_R2FR_4037_NEXT_TARGET.csv",
    "status": SOURCE_DIR / "P8_Y5_R2FR_4037_STATUS.csv",
    "validation": SOURCE_DIR / "P8_Y5_BRR545_4037_VALIDATION.csv",
}


def timestamp() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def write_csv(path: Path, rows: List[Dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows supplied for {path}")
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
        ("SRC4037_0", ROOT / "4036-Y5-R2FR-no-Hom-source-slot-theorem-or-cT-cEM-units.md", "NO_HOM_THEOREM_DERIVED_CONDITIONAL_PARENT_UNSIGNED", "immediate predecessor verdict"),
        ("SRC4037_1", SOURCE_DIR / "P8_Y5_R2FR_4036_NO_HOM_SOURCE_SLOT_THEOREM.csv", "EXACT_CONDITIONAL_THEOREM_IF_TYPED_PACKET_ADOPTED", "conditional theorem to activate"),
        ("SRC4037_2", SOURCE_DIR / "P8_Y5_R2FR_4036_CHAIN_RULE_PROOF.csv", "CONDITIONAL_VERTEX_ZERO", "chain-rule zero proof"),
        ("SRC4037_3", SOURCE_DIR / "P8_Y5_R2FR_4036_COUNTERMODEL_TESTS.csv", "REAL_COUNTERMODEL_IF_EM_OWNER_UNSIGNED", "fallback countermodel guard"),
        ("SRC4037_4", SOURCE_DIR / "P8_Y5_R2FR_4036_cT_cEM_UNIT_LAW.csv", "FALLBACK_UNIT_LAW_READY", "fallback unit law"),
        ("SRC4037_5", SOURCE_DIR / "P8_MIN_PARENT_LOCAL_GR_ACTION_BLOCKS.csv", "S_matter[psi, g_obs] with no leading species-dependent coupling", "minimal parent local-GR blocks"),
        ("SRC4037_6", SOURCE_DIR / "P8_EM_vq_parent_object_language_normal_form_candidate.csv", "S_matter=sum_A S_A[psi_A,Qvis,theta_A,A_obs]", "Qvis/matter normal form"),
        ("SRC4037_7", SOURCE_DIR / "P8_GAMMA_OWNER_CANDIDATE_ACTION.csv", "Gamma_eff = Gamma0 + 1/2 M_AB", "Gamma owner quadratic/even packet"),
        ("SRC4037_8", SOURCE_DIR / "P8_Y5_R2FR_4035_SOURCE_ONLY_VERTEX_NORMAL_FORM.csv", "S_EM=-(1/(4*mu0))int F wedge *obs F", "source-only vertex normal form"),
        ("SRC4037_9", SOURCE_DIR / "P8_Y5_R2FR_4035_SOURCE_ONLY_VERTEX_EXCLUSION_GATE.csv", "conditional theorem: c_T=c_EM=0", "4035 exclusion gate"),
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


def packet_signature_rows(ts: str) -> List[Dict[str, object]]:
    return [
        {
            "clause_id": "PKT4037_0_domain",
            "clause": "local branch parent action language is restricted to EH/topological kappa, Gamma-owner, universal matter, unique observed EM, selector, boundary, and readout-after-variation blocks",
            "signature_source": "A511 and NF4035/NF3519 packets",
            "selected_for_local_branch": True,
            "what_it_forbids": "post-readout source labels, fitted source weights, hidden source metrics, pre-variation source masks",
            "what_it_kills": "late source-only scalar couplings",
            "status": "LOCAL_BRANCH_PACKET_SIGNED_AS_INTERNAL_CONTRACT",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "clause_id": "PKT4037_1_Qvis",
            "clause": "ordinary matter and EM see only Qvis=q(Phi), g_obs, observed connection/coframe, fixed representation labels, and common constants",
            "signature_source": "NF3519_1 and NF3519_2",
            "selected_for_local_branch": True,
            "what_it_forbids": "q_private T_A, Z*T_A, source-only disformal/conformal frame, w_A(Z)S_A",
            "what_it_kills": "direct c_T from ordinary matter trace",
            "status": "QVIS_ONLY_MATTER_PACKET_SIGNED_FOR_LOCAL_BRANCH",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "clause_id": "PKT4037_2_EM_owner",
            "clause": "Maxwell/EM stress has one observed Hodge and one normalization owner; hidden multipliers f(Z)F_EM^2 are outside the selected local branch packet",
            "signature_source": "NF4035_2 plus UNIT4036/CM4036 guard",
            "selected_for_local_branch": True,
            "what_it_forbids": "Z*F_EM^2, f(Z)F_EM^2, independent hidden Hodge/constitutive source slot",
            "what_it_kills": "direct ordinary c_EM and C_XF2-type hidden F2 source-only vertices in this branch",
            "status": "UNIQUE_EM_OWNER_SIGNED_FOR_LOCAL_BRANCH",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "clause_id": "PKT4037_3_Gamma_owner",
            "clause": "Gamma_eff is owned by geometry/response variables and is even/quadratic about the local fixed point, not by matter/EM Lagrangian densities",
            "signature_source": "P8_GAMMA_OWNER_CANDIDATE_ACTION.csv",
            "selected_for_local_branch": True,
            "what_it_forbids": "Gamma source arguments T_H or F_EM^2 as independent slots",
            "what_it_kills": "linear response-source leakage from Gamma owner",
            "status": "GAMMA_OWNER_SELECTED_WITH_REMAINING_FIXED_POINT_GATES",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "clause_id": "PKT4037_4_readout_firewall",
            "clause": "PPN, R10, clocks, orbital, SPARC, cosmology, and EM readouts are post-variation maps and cannot feed back into action source selection",
            "signature_source": "NF3519_5 and NF4035_4",
            "selected_for_local_branch": True,
            "what_it_forbids": "calibrated GM masks, source-dependent readout weights, worldtube masks in S_matter or S_EM",
            "what_it_kills": "readout-regenerated direct c_T/c_EM",
            "status": "READOUT_FIREWALL_SIGNED_FOR_LOCAL_BRANCH",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "clause_id": "PKT4037_5_scope",
            "clause": "the signature is a local-branch action-language selection, not a derivation of the entire MTS parent from deeper primitives",
            "signature_source": "4036 countermodel guard",
            "selected_for_local_branch": True,
            "what_it_forbids": "calling the result a full local-GR or public R10 pass",
            "what_it_kills": "overclaim from branch signing",
            "status": "SCOPE_GUARD_SIGNED",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
    ]


def zeroed_coupling_rows(ts: str) -> List[Dict[str, object]]:
    return [
        {
            "coupling_id": "ZERO4037_0_cT",
            "symbol": "c_T",
            "forbidden_vertex": "Z*T_H, gamma*T_H, q_private*T_A, w_A(Z)S_A",
            "zero_law": "c_T_direct=0 inside the selected minimal source-clean local branch packet",
            "proof_link": "4036 chain rule plus PKT4037_1",
            "what_remains": "finite c_T fallback only if the packet is rejected or hidden conformal matter is reintroduced",
            "status": "ZERO_IN_SELECTED_PACKET_NOT_PUBLIC_LOCAL_GR_CLAIM",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "coupling_id": "ZERO4037_1_cEM",
            "symbol": "c_EM",
            "forbidden_vertex": "Z*F_EM^2, gamma*F_EM^2, f(Z)F_EM^2, hidden Hodge source slot",
            "zero_law": "c_EM_direct=0 inside the selected minimal source-clean local branch packet",
            "proof_link": "4036 EM chain rule plus PKT4037_2",
            "what_remains": "finite c_EM fallback only if hidden Maxwell multiplier/constitutive owner is reintroduced",
            "status": "ZERO_IN_SELECTED_PACKET_NOT_PUBLIC_LOCAL_GR_CLAIM",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "coupling_id": "ZERO4037_2_cross_guard",
            "symbol": "C_XF2",
            "forbidden_vertex": "nonminimal hidden/motion/time scalar multiplying F^2 or F*F",
            "zero_law": "C_XF2_direct=0 in the selected branch by unique observed EM owner",
            "proof_link": "PKT4037_2",
            "what_remains": "radiative/background Poynting flux and boundary terms, not a direct EM action multiplier",
            "status": "DIRECT_CROSS_TERM_FORBIDDEN_IN_SELECTED_PACKET",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
    ]


def bound_smoke_rows(ts: str) -> List[Dict[str, object]]:
    return [
        {
            "bound_id": "BS4037_0_cT_fallback",
            "symbol": "c_T",
            "used_if": "minimal source-clean packet rejected or hidden conformal matter allowed",
            "prediction_formula": "alpha_T=(2/3)*C_alpha_phi*c_T*(I_T/M_H)*(q_test/m_test)",
            "bound_formula": "|c_T| <= (3/2)*alpha_bound/|C_alpha_phi*(I_T/M_H)*(q_test/m_test)|",
            "units": "m/J in SI energy-density convention; L^2 in natural units",
            "missing_numeric_inputs": "alpha_bound,C_alpha_phi,I_T_over_M_H,q_test_over_m_test,source_profile",
            "smoke_result": "SCHEMA_AND_UNITS_READY_NUMERIC_CLAIM_BLOCKED",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "bound_id": "BS4037_1_cEM_fallback",
            "symbol": "c_EM",
            "used_if": "unique observed EM owner rejected or hidden Maxwell multiplier allowed",
            "prediction_formula": "alpha_EM=(2/3)*C_alpha_phi*c_EM*(I_EM/M_H)*(q_test/m_test)",
            "bound_formula": "|c_EM| <= (3/2)*alpha_bound/|C_alpha_phi*(I_EM/M_H)*(q_test/m_test)|",
            "units": "m/J after choosing normalized EM energy/action density; L^2 in natural units",
            "missing_numeric_inputs": "alpha_bound,C_alpha_phi,I_EM_over_M_H,q_test_over_m_test,EM_normalization,source_profile",
            "smoke_result": "SCHEMA_AND_UNITS_READY_NUMERIC_CLAIM_BLOCKED",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
    ]


def remaining_residual_rows(ts: str) -> List[Dict[str, object]]:
    return [
        {
            "residual_id": "REM4037_0_poynting",
            "symbol": "c_Poynting",
            "residual": "net radiative/background EM Poynting flux through local collar",
            "current_route": "derive stationary isolated no-flux theorem or bound Phi_EM_rad/(G_ref M_H)",
            "priority": "next_after_direct_couplings",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "residual_id": "REM4037_1_boundary",
            "symbol": "c_B",
            "residual": "source-dependent boundary/corner term or reference subtraction leakage",
            "current_route": "prove fixed source-blind boundary reference or bound boundary scalar charge",
            "priority": "high",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "residual_id": "REM4037_2_hidden_current",
            "symbol": "c_Z",
            "residual": "remaining hidden/domain/memory current J_Z not killed by direct source-slot theorem",
            "current_route": "derive fixed-point current silence or expose finite current coefficient",
            "priority": "high",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "residual_id": "REM4037_3_norm",
            "symbol": "c_norm",
            "residual": "universal source/action normalization drift",
            "current_route": "route into calibrated G/Newton constant or bound time/source variation",
            "priority": "medium",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "residual_id": "REM4037_4_nonEH",
            "symbol": "c_nonEH",
            "residual": "non-EH metric operator or higher-curvature leakage in the local branch",
            "current_route": "show higher operators decouple at local scale or compare to PPN/Cassini bounds",
            "priority": "medium",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
    ]


def evaluator_rows(ts: str) -> List[Dict[str, object]]:
    return [
        {
            "case_id": "CASE4037_0_selected_packet",
            "verdict": "MINIMAL_SOURCE_CLEAN_LOCAL_PACKET_SIGNED_INTERNALLY",
            "direct_coupling_result": "c_T_direct=c_EM_direct=C_XF2_direct=0 inside selected packet",
            "claim_result": "NO_PUBLIC_LOCAL_GR_CLAIM_FROM_4037",
            "reason": "branch action-language selection is explicit and source-clean, but flux/boundary/current/normalization/nonEH residuals remain",
            "next_action": "attack c_Poynting/no-flux and boundary reference next",
            "timestamp_utc": ts,
        },
        {
            "case_id": "CASE4037_1_packet_rejected",
            "verdict": "FINITE_cT_cEM_BOUND_SMOKE_READY",
            "direct_coupling_result": "numeric bound branch required",
            "claim_result": "NO_PUBLIC_LOCAL_GR_CLAIM_FROM_4037",
            "reason": "hidden conformal matter or hidden Maxwell multiplier countermodels become real if packet is rejected",
            "next_action": "source alpha_bound and profile integrals before scoring",
            "timestamp_utc": ts,
        },
    ]


def decision_rows(ts: str) -> List[Dict[str, object]]:
    return [
        {
            "decision_id": "DEC4037_0_branch_selection",
            "decision": "For the local-GR derivation branch, adopt the minimal source-clean parent packet as the internal action-language contract.",
            "status": "LOCAL_BRANCH_PACKET_SELECTED",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "decision_id": "DEC4037_1_direct_couplings",
            "decision": "Inside that selected packet, direct c_T, direct c_EM, and direct C_XF2 are set to zero by the 4036 no-Hom/chain-rule theorem.",
            "status": "DIRECT_SOURCE_COUPLINGS_ZEROED_IN_PACKET",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "decision_id": "DEC4037_2_fallback",
            "decision": "If later work rejects any packet clause, use the bound-smoke formulas rather than reopening a vague coupling hole.",
            "status": "FINITE_BOUND_FALLBACK_PRESERVED",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "decision_id": "DEC4037_3_next",
            "decision": "Move to 4038-Y5-R2FR-Poynting-no-flux-and-boundary-reference-theorem-or-flux-bound.md.",
            "status": "NEXT_TARGET_SELECTED",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
    ]


def claim_rows(ts: str) -> List[Dict[str, object]]:
    return [
        {
            "claim_id": "CLAIM4037_0_direct_couplings",
            "claim": "direct source-only c_T/c_EM are zero in selected local packet",
            "allowed": True,
            "scope": "internal selected-branch statement only",
            "reason": "packet clauses explicitly forbid those vertices and 4036 gives the chain-rule theorem",
            "public_claim_allowed": False,
            "timestamp_utc": ts,
        },
        {
            "claim_id": "CLAIM4037_1_local_GR",
            "claim": "local GR/PPN/R10 pass",
            "allowed": False,
            "scope": "full local-gravity phenomenology",
            "reason": "remaining c_Poynting, c_B, c_Z, c_norm, and c_nonEH residuals are not closed",
            "public_claim_allowed": False,
            "timestamp_utc": ts,
        },
        {
            "claim_id": "CLAIM4037_2_fallback_bounds",
            "claim": "finite c_T/c_EM numeric bound",
            "allowed": False,
            "scope": "fallback branch only",
            "reason": "numeric alpha/profile/normalization inputs are not yet supplied",
            "public_claim_allowed": False,
            "timestamp_utc": ts,
        },
    ]


def next_rows(ts: str) -> List[Dict[str, object]]:
    return [
        {
            "row_id": "NEXT4037_0",
            "next_doc": "4038-Y5-R2FR-Poynting-no-flux-and-boundary-reference-theorem-or-flux-bound.md",
            "next_script": "scripts/Y5_R2FR_4038_Poynting_no_flux_and_boundary_reference_theorem_or_flux_bound.py",
            "why": "direct source couplings are now zeroed inside the selected local packet; the next biggest local-GR leak is collar flux/boundary reference rather than c_T/c_EM.",
            "fallback": "if no-flux or boundary reference fails, produce finite Phi_EM_rad and boundary-charge bound rows",
            "timestamp_utc": ts,
        }
    ]


def status_rows(ts: str) -> List[Dict[str, object]]:
    return [
        {
            "status_id": "STATUS4037_0",
            "checkpoint": "4037",
            "canonical_status": "MINIMAL_SOURCE_CLEAN_LOCAL_PACKET_SELECTED_DIRECT_CT_CEM_ZEROED_INTERNAL",
            "strongest_result": "Direct source-only c_T, c_EM, and C_XF2 are zero in the selected local branch action packet.",
            "still_missing": "stationary EM no-flux theorem, source-blind boundary reference, hidden current silence, universal normalization routing, nonEH/PPN residual closure",
            "public_claim_allowed": False,
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        }
    ]


def render_doc(ts: str, sources: List[Dict[str, object]]) -> str:
    found = sum(1 for row in sources if row["exists"] and row["needle_found"])
    total = len(sources)
    return f"""# 4037 - Minimal Parent Packet Signature Or cT cEM Bound Smoke

- Timestamp: `{ts}`
- Status: `private_nonclaim_checkpoint`
- Scope: `post-checkpoint-work` only; no `formalization-workbench` edits.
- Source needles found: `{found}/{total}`.

## What Actually Moved

4037 takes the 4036 fork and chooses the clean local branch:

`S_local = S_EH[g_obs] + S_kappa_top + I_Gamma[g_obs,Z,R_even,D] + S_matter[psi,Qvis,theta,A_obs] + S_EM[A,Qvis,J] + S_selector + S_boundary`,

with readouts only after variation.

This is signed as the internal local-branch action-language contract, not as a public full-theory/local-GR claim.

## Direct Coupling Result

Inside this selected packet:

- `c_T_direct=0` for `Z*T_H`, `gamma*T_H`, `q_private*T_A`, and `w_A(Z)S_A`;
- `c_EM_direct=0` for `Z*F_EM^2`, `gamma*F_EM^2`, and `f(Z)F_EM^2`;
- `C_XF2_direct=0` for hidden scalar/response multipliers of `F^2` or `F*F`.

This is no longer a vague missing coupling. It is a branch theorem: if the packet is used, the direct source-only couplings are absent; if the packet is rejected, the finite-bound branch is mandatory.

## Fallback Bound Smoke

If hidden conformal matter or hidden Maxwell multipliers are reintroduced:

`alpha_X=(2/3)*C_alpha_phi*c_X*(I_X/M_H)*(q_test/m_test)`.

So

`|c_X| <= (3/2)*alpha_bound/|C_alpha_phi*(I_X/M_H)*(q_test/m_test)|`.

The fallback is schema/unit-ready but numeric-claim blocked until `alpha_bound`, `C_alpha_phi`, profile integrals, test charge ratios, and EM normalization are real.

## Remaining Local-GR Leak Vector

The next problem is not direct `c_T/c_EM`. The remaining vector is:

- `c_Poynting`: net EM/radiative/background flux through the local collar;
- `c_B`: boundary/corner/reference leakage;
- `c_Z`: hidden/domain/memory current;
- `c_norm`: universal source/action normalization drift;
- `c_nonEH`: non-EH or higher-curvature metric operator leakage.

## Current Verdict

- Current evaluator result: `MINIMAL_SOURCE_CLEAN_LOCAL_PACKET_SIGNED_INTERNALLY`.
- Direct result: `c_T_direct=c_EM_direct=C_XF2_direct=0` inside the selected packet.
- Claim result: `NO_PUBLIC_LOCAL_GR_CLAIM_FROM_4037`.

## Next Target

- `4038-Y5-R2FR-Poynting-no-flux-and-boundary-reference-theorem-or-flux-bound.md`
- `scripts/Y5_R2FR_4038_Poynting_no_flux_and_boundary_reference_theorem_or_flux_bound.py`
"""


def validation_rows(
    ts: str,
    sources: List[Dict[str, object]],
    signature: List[Dict[str, object]],
    zeroed: List[Dict[str, object]],
    bound_smoke: List[Dict[str, object]],
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
        row("VAL4037_00_sources_exist", all(item["exists"] for item in sources), "all cited source paths exist"),
        row("VAL4037_01_needles_found", all(item["needle_found"] for item in sources), "all source needles found"),
        row("VAL4037_02_packet_signed", all(item["selected_for_local_branch"] is True for item in signature), "all packet clauses selected for local branch"),
        row("VAL4037_03_scope_guard", any(item["clause_id"] == "PKT4037_5_scope" for item in signature), "scope guard present"),
        row("VAL4037_04_cT_zero", any(item["symbol"] == "c_T" and "ZERO_IN_SELECTED_PACKET" in item["status"] for item in zeroed), "direct c_T zero row present"),
        row("VAL4037_05_cEM_zero", any(item["symbol"] == "c_EM" and "ZERO_IN_SELECTED_PACKET" in item["status"] for item in zeroed), "direct c_EM zero row present"),
        row("VAL4037_06_CXF2_zero", any(item["symbol"] == "C_XF2" for item in zeroed), "direct C_XF2 guard row present"),
        row("VAL4037_07_bound_cT", any(item["symbol"] == "c_T" and "bound_formula" in item for item in bound_smoke), "c_T fallback bound formula present"),
        row("VAL4037_08_bound_cEM", any(item["symbol"] == "c_EM" and "bound_formula" in item for item in bound_smoke), "c_EM fallback bound formula present"),
        row("VAL4037_09_bound_nonclaim", all(item["valid_for_public_claim"] is False for item in bound_smoke), "fallback bounds remain nonclaim"),
        row("VAL4037_10_remaining_poynting", any(item["symbol"] == "c_Poynting" for item in remaining), "Poynting residual present"),
        row("VAL4037_11_remaining_boundary", any(item["symbol"] == "c_B" for item in remaining), "boundary residual present"),
        row("VAL4037_12_remaining_current", any(item["symbol"] == "c_Z" for item in remaining), "hidden current residual present"),
        row("VAL4037_13_current_verdict", any(item["case_id"] == "CASE4037_0_selected_packet" for item in evaluator), "selected-packet evaluator present"),
        row("VAL4037_14_no_public_local_claim", all(item["public_claim_allowed"] is False for item in claims), "no public claims allowed"),
        row("VAL4037_15_internal_direct_claim_scoped", any(item["claim_id"] == "CLAIM4037_0_direct_couplings" and item["allowed"] is True and item["public_claim_allowed"] is False for item in claims), "internal direct-coupling claim scoped"),
        row("VAL4037_16_next_decision", any(item["decision_id"] == "DEC4037_3_next" for item in decisions), "4038 next decision present"),
        row("VAL4037_17_next_target", bool(next_target and "4038" in str(next_target[0]["next_doc"])), "next target row present"),
        row("VAL4037_18_doc_written", DOC_PATH.exists(), "checkpoint doc written"),
        row("VAL4037_19_no_formalization_output", all(str(FORMALIZATION) not in path for path in output_paths), "no output targets formalization-workbench"),
        row("VAL4037_20_script_compiles", compile_ok, "script compiles"),
        row("VAL4037_21_private_guard", all(item["valid_for_public_claim"] is False for table in [signature, zeroed, bound_smoke, remaining, decisions] for item in table), "public-claim guard retained"),
    ]


def main() -> None:
    ts = timestamp()
    sources = source_rows(ts)
    signature = packet_signature_rows(ts)
    zeroed = zeroed_coupling_rows(ts)
    bound_smoke = bound_smoke_rows(ts)
    remaining = remaining_residual_rows(ts)
    evaluator = evaluator_rows(ts)
    decisions = decision_rows(ts)
    claims = claim_rows(ts)
    next_target = next_rows(ts)
    status = status_rows(ts)

    DOC_PATH.write_text(render_doc(ts, sources), encoding="utf-8")
    write_csv(OUTPUTS["source_register"], sources)
    write_csv(OUTPUTS["packet_signature"], signature)
    write_csv(OUTPUTS["zeroed_couplings"], zeroed)
    write_csv(OUTPUTS["bound_smoke"], bound_smoke)
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

    checks = validation_rows(ts, sources, signature, zeroed, bound_smoke, remaining, evaluator, decisions, claims, next_target, compile_ok)
    write_csv(OUTPUTS["validation"], checks)
    passed = sum(1 for item in checks if item["passed"])
    total = len(checks)
    print(f"4037 validation: {passed}/{total} passed")
    if passed != total:
        for item in checks:
            if not item["passed"]:
                print(f"FAIL {item['check_id']}: {item['detail']}")
        raise SystemExit(1)
    print(f"Wrote {DOC_PATH}")


if __name__ == "__main__":
    main()
