from __future__ import annotations

import csv
import py_compile
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Iterable, List


ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
SOURCE_DIR = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = PROJECT / "formalization-workbench"
SCRIPT_PATH = Path(__file__).resolve()
DOC_PATH = ROOT / "4036-Y5-R2FR-no-Hom-source-slot-theorem-or-cT-cEM-units.md"

OUTPUTS = {
    "source_register": SOURCE_DIR / "P8_Y5_R2FR_4036_SOURCE_REGISTER.csv",
    "theorem": SOURCE_DIR / "P8_Y5_R2FR_4036_NO_HOM_SOURCE_SLOT_THEOREM.csv",
    "chain_rule": SOURCE_DIR / "P8_Y5_R2FR_4036_CHAIN_RULE_PROOF.csv",
    "countermodels": SOURCE_DIR / "P8_Y5_R2FR_4036_COUNTERMODEL_TESTS.csv",
    "unit_law": SOURCE_DIR / "P8_Y5_R2FR_4036_cT_cEM_UNIT_LAW.csv",
    "evaluator": SOURCE_DIR / "P8_Y5_R2FR_4036_EVALUATOR_RESULTS.csv",
    "decision_gate": SOURCE_DIR / "P8_Y5_R2FR_4036_DECISION_GATE.csv",
    "claim_gate": SOURCE_DIR / "P8_Y5_R2FR_4036_CLAIM_GATE.csv",
    "next_target": SOURCE_DIR / "P8_Y5_R2FR_4036_NEXT_TARGET.csv",
    "status": SOURCE_DIR / "P8_Y5_R2FR_4036_STATUS.csv",
    "validation": SOURCE_DIR / "P8_Y5_BRR545_4036_VALIDATION.csv",
}


def timestamp() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def write_csv(path: Path, rows: List[Dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    fieldnames: List[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def source_specs(ts: str) -> List[Dict[str, object]]:
    specs = [
        {
            "source_id": "SRC4036_0",
            "path": ROOT / "4035-Y5-R2FR-source-only-vertex-exclusion-or-cT-cEM-fill.md",
            "needle": "VERTEX_EXCLUSION_CONDITIONAL_cT_cEM_RETAINED",
            "role": "immediate predecessor and current retained c_T/c_EM verdict",
        },
        {
            "source_id": "SRC4036_1",
            "path": SOURCE_DIR / "P8_Y5_R2FR_4035_SOURCE_ONLY_VERTEX_EXCLUSION_GATE.csv",
            "needle": "Hom_parent(Z_source_slot, MatterActionScalar)=0",
            "role": "4035 no-Hom clause to be strengthened",
        },
        {
            "source_id": "SRC4036_2",
            "path": SOURCE_DIR / "P8_Y5_R2FR_4035_cT_cEM_COEFFICIENT_FILL.csv",
            "needle": "units making c_T*T_H match F=Gamma_eff-Gamma0",
            "role": "fallback coefficient and unit target",
        },
        {
            "source_id": "SRC4036_3",
            "path": SOURCE_DIR / "P8_Y5_R2FR_3990_NO_HOM_GRAMMAR_THEOREM.csv",
            "needle": "EXACT_CONDITIONAL_GRAMMAR_THEOREM_DERIVED_NOT_PARENT_SIGNED",
            "role": "strongest earlier no-source-slot grammar result",
        },
        {
            "source_id": "SRC4036_4",
            "path": SOURCE_DIR / "P8_Y5_R2FR_4008_NO_HOM_WEIGHT_REJECTION_PROOF.csv",
            "needle": "delta_R S_ord",
            "role": "chain-rule bulk-zero proof template",
        },
        {
            "source_id": "SRC4036_5",
            "path": SOURCE_DIR / "P8_Y5_PARENT_QLOC_2397_NO_HOM_CERTIFICATE.csv",
            "needle": "no-source-only Hom closure",
            "role": "parent certificate clauses still unsigned",
        },
        {
            "source_id": "SRC4036_6",
            "path": SOURCE_DIR / "P8_EM_vq_parent_object_language_normal_form_candidate.csv",
            "needle": "S_matter=sum_A S_A[psi_A,Qvis,theta_A,A_obs]",
            "role": "typed matter functor and Qvis stack",
        },
        {
            "source_id": "SRC4036_7",
            "path": SOURCE_DIR / "P8_EM_Poynting_source_flux_or_cross_term_vector.csv",
            "needle": "nonminimal_MTS_EM_cross_term",
            "role": "EM countermodel and nonminimal F2 guard",
        },
        {
            "source_id": "SRC4036_8",
            "path": SOURCE_DIR / "P8_Y5_typed_EM_noHom_or_alpha_closure_demotion_status.csv",
            "needle": "typed_noHom_certificate",
            "role": "typed EM no-Hom certificate status",
        },
        {
            "source_id": "SRC4036_9",
            "path": SOURCE_DIR / "P8_MIN_PARENT_LOCAL_GR_ACTION_BLOCKS.csv",
            "needle": "S_matter[psi, g_obs] with no leading species-dependent coupling",
            "role": "minimal parent action block for universal matter",
        },
    ]
    rows: List[Dict[str, object]] = []
    for spec in specs:
        path = Path(spec["path"])
        exists = path.exists()
        text = read_text(path) if exists else ""
        found = str(spec["needle"]) in text
        rows.append(
            {
                "source_id": spec["source_id"],
                "path": str(path),
                "exists": exists,
                "needle": spec["needle"],
                "needle_found": found,
                "role": spec["role"],
                "timestamp_utc": ts,
            }
        )
    return rows


def theorem_rows(ts: str) -> List[Dict[str, object]]:
    return [
        {
            "theorem_id": "THM4036_0_statement",
            "piece": "source-slot no-Hom theorem",
            "mathematical_form": (
                "Let S_ord and S_EM factor through Qvis=q(Phi) only, with fixed representation labels theta_A, "
                "one observed Hodge star, one universal action-density line, and no pre-variation readout/source marker. "
                "For any hidden/source-slot object Z_src outside Qvis, Hom_parent(Z_src,ActionScalar_matter)=0 and "
                "Hom_parent(Z_src,ActionScalar_EM)=0."
            ),
            "derived_result": "Z*T_H and Z*F_EM^2 are not legal parent action monomials inside the minimal typed packet.",
            "status": "EXACT_CONDITIONAL_THEOREM_IF_TYPED_PACKET_ADOPTED",
            "sets_to_zero": "c_T,c_EM for direct source-only vertices",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
        {
            "theorem_id": "THM4036_1_matter_factorization",
            "piece": "ordinary matter descent",
            "mathematical_form": (
                "S_matter=sum_A integral mu_obs(Qvis) L_A(j^k psi_A,Qvis,theta_A,A_obs; common constants). "
                "Arguments contain no Z_src, source weight w_A(Z_src), source mask, or hidden coframe."
            ),
            "derived_result": "partial S_matter/partial Z_src has no source-only bulk term before variation.",
            "status": "CHAIN_RULE_ZERO_IF_QVIS_AND_THETA_FIXED",
            "sets_to_zero": "direct c_T",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
        {
            "theorem_id": "THM4036_2_EM_factorization",
            "piece": "EM owner descent",
            "mathematical_form": (
                "S_EM=-(4 mu0)^-1 integral F wedge star_obs(Qvis) F + integral A wedge J, "
                "with no independent f(Z_src) multiplier and no hidden Hodge/constitutive slot."
            ),
            "derived_result": "partial S_EM/partial Z_src has no ordinary Z*F_EM^2 source vertex.",
            "status": "CHAIN_RULE_ZERO_IF_UNIQUE_EM_OWNER_ADOPTED",
            "sets_to_zero": "ordinary direct c_EM",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
        {
            "theorem_id": "THM4036_3_not_parity",
            "piece": "trace guard",
            "mathematical_form": "Matter trace T_H and F_EM^2 can be exchange-even scalars, so exchange parity alone cannot kill them.",
            "derived_result": "the proof must be typed-domain/no-Hom, not odd-integrand cancellation.",
            "status": "OVERCLAIM_GUARD",
            "sets_to_zero": "nothing by itself",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
        {
            "theorem_id": "THM4036_4_conclusion",
            "piece": "conditional local source leak result",
            "mathematical_form": "If THM4036_0 through THM4036_3 are parent-signed, F_source_leak has no direct c_T T_H or c_EM F_EM^2 terms.",
            "derived_result": "The local scalar charge route moves from direct source vertices to flux, boundary, non-Hilbert, and finite-range hair only.",
            "status": "DERIVED_CONDITIONAL_ZERO_NOT_PUBLIC_CLAIM",
            "sets_to_zero": "c_T,c_EM direct vertices only",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
    ]


def chain_rule_rows(ts: str) -> List[Dict[str, object]]:
    return [
        {
            "proof_id": "PROOF4036_0_variation_setup",
            "step": "write ordinary action as composition",
            "formula": "S_ord[Phi,psi]=Sbar_ord[Qvis(Phi),psi,theta,A_obs(Qvis)]",
            "condition": "theta fixed; no hidden/source marker inside Qvis; variation taken before readout",
            "result": "all Z_src dependence must pass through Qvis or an explicitly added forbidden constructor",
            "status": "DERIVED",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
        {
            "proof_id": "PROOF4036_1_vertical_chain_rule",
            "step": "differentiate along hidden/source-slot variation v_Z",
            "formula": "delta_Z S_ord = <delta Sbar_ord/dQvis, DQvis[v_Z]> + <E_psi,delta_Z psi> + boundary",
            "condition": "DQvis[v_Z]=0 for source-slot object; matter lift on shell or gauge-fixed; boundary class fixed",
            "result": "bulk delta_Z S_ord=0 for ordinary matter",
            "status": "EXACT_IF_VERTICALITY_AND_LIFT_SIGNED",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
        {
            "proof_id": "PROOF4036_2_no_monomial",
            "step": "translate zero derivative to vertex exclusion",
            "formula": "If Z*T_H existed, delta_Z S_ord would contain T_H. Since the typed derivative is zero, coefficient c_T=0.",
            "condition": "no independent source-only action constructor outside S_ord",
            "result": "direct c_T is zero in the minimal parent packet",
            "status": "CONDITIONAL_VERTEX_ZERO",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
        {
            "proof_id": "PROOF4036_3_EM_chain_rule",
            "step": "repeat for observed Maxwell owner",
            "formula": "delta_Z S_EM=<delta S_EM/d star_obs, D star_obs[DQvis[v_Z]]> + boundary",
            "condition": "one observed Hodge star; no f(Z)F^2; no hidden constitutive tensor",
            "result": "direct c_EM is zero in the minimal parent packet",
            "status": "CONDITIONAL_VERTEX_ZERO",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
        {
            "proof_id": "PROOF4036_4_scope",
            "step": "state what remains",
            "formula": "F_source_leak = c_Poynting div S_EM + c_B B_boundary + c_Z J_Z + c_norm Delta_norm + c_nonEH O_nonEH + ...",
            "condition": "after direct c_T,c_EM exclusion only",
            "result": "local GR is still not claimed; remaining residuals must be killed or bounded",
            "status": "SCOPE_GUARD",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
    ]


def countermodel_rows(ts: str) -> List[Dict[str, object]]:
    return [
        {
            "countermodel_id": "CM4036_0_hidden_conformal_matter",
            "allowed_if": "matter sees g_tilde=A(Z)g_obs before variation",
            "produces": "delta_Z S_matter proportional to T_H dlnA/dZ",
            "coefficient_owed": "c_T",
            "decision": "forbid by Qvis-only matter functor or keep finite coefficient branch",
            "status": "REAL_COUNTERMODEL_IF_PARENT_PACKET_NOT_ADOPTED",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
        {
            "countermodel_id": "CM4036_1_hidden_Maxwell_multiplier",
            "allowed_if": "EM action contains f(Z)F_EM^2 or hidden constitutive tensor",
            "produces": "delta_Z S_EM proportional to F_EM^2 df/dZ",
            "coefficient_owed": "c_EM",
            "decision": "forbid by unique observed Maxwell owner or keep finite coefficient branch",
            "status": "REAL_COUNTERMODEL_IF_EM_OWNER_UNSIGNED",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
        {
            "countermodel_id": "CM4036_2_readout_return",
            "allowed_if": "worldtube/source/readout mask re-enters S_matter or S_EM before variation",
            "produces": "post-fit source-dependent active coupling",
            "coefficient_owed": "c_T,c_EM or source-normalization coefficient",
            "decision": "keep readout firewall; otherwise numeric bound rows required",
            "status": "REAL_COUNTERMODEL_IF_FIREWALL_UNSIGNED",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
    ]


def unit_rows(ts: str) -> List[Dict[str, object]]:
    return [
        {
            "unit_id": "UNIT4036_0_F_dimension",
            "quantity": "F=Gamma_eff-Gamma0 in (Delta-mu_phi^2)u=(2/3)F",
            "natural_units": "L^-2 if u is dimensionless",
            "SI_or_geometric_units": "curvature units m^-2",
            "score_use": "target dimension for c_T*T_H and c_EM*F_EM^2",
            "status": "UNIT_TARGET_DERIVED",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
        {
            "unit_id": "UNIT4036_1_cT_natural",
            "quantity": "c_T multiplying T_H",
            "natural_units": "L^2 = mass^-2 when T_H has L^-4",
            "SI_or_geometric_units": "m/J if T_H is energy density; G/c^4 is the GR comparison scale",
            "score_use": "Q_phi_T=(2/3)c_T integral_W T_H dV_3",
            "status": "FALLBACK_UNIT_LAW_READY",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
        {
            "unit_id": "UNIT4036_2_cEM_normalized",
            "quantity": "c_EM multiplying normalized EM action/stress scalar",
            "natural_units": "L^2 = mass^-2 when L_EM or T_EM has L^-4",
            "SI_or_geometric_units": "m/J if using EM energy density; raw F_munu F^munu needs its mu0/c normalization declared first",
            "score_use": "Q_phi_EM=(2/3)c_EM integral_W L_EM_or_TEM dV_3",
            "status": "FALLBACK_UNIT_LAW_READY_WITH_NORMALIZATION_GUARD",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
        {
            "unit_id": "UNIT4036_3_Qphi_spatial",
            "quantity": "Q_phi surface/scalar charge",
            "natural_units": "L for spatial stationary integral of F over dV_3",
            "SI_or_geometric_units": "length-like scalar charge after choosing u normalization",
            "score_use": "alpha_phi needs a separately owned C_alpha_phi normalization before R10 scoring",
            "status": "ALPHA_NORMALIZATION_STILL_SEPARATE",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
        {
            "unit_id": "UNIT4036_4_time_window",
            "quantity": "spacetime worldtube integral",
            "natural_units": "if dV_4 is used, divide by stationary time window Delta t to recover spatial Q_phi units",
            "SI_or_geometric_units": "time-window normalization must be declared for clocks/radiative branches",
            "score_use": "prevents silently changing Q_phi units between local, orbital, and clock arenas",
            "status": "MEASURE_CONVENTION_GUARD",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
    ]


def evaluator_rows(ts: str) -> List[Dict[str, object]]:
    return [
        {
            "case_id": "CASE4036_0_minimal_packet_adopted",
            "verdict": "c_T=c_EM=0_FOR_DIRECT_SOURCE_ONLY_VERTICES",
            "claim_result": "NO_PUBLIC_LOCAL_GR_CLAIM_FROM_4036",
            "reason": "the theorem is exact only after the typed parent packet is signed as the parent action language",
            "next_action": "sign minimal parent packet or move remaining flux/boundary residuals",
            "timestamp_utc": ts,
        },
        {
            "case_id": "CASE4036_1_current",
            "verdict": "NO_HOM_THEOREM_DERIVED_CONDITIONAL_PARENT_UNSIGNED",
            "claim_result": "NO_PUBLIC_LOCAL_GR_CLAIM_FROM_4036",
            "reason": "source-only vertices are mathematically killed inside the packet, but the packet is not yet committed as parent-owned",
            "next_action": "4037 should sign the minimal parent packet or run c_T/c_EM bound smoke rows",
            "timestamp_utc": ts,
        },
        {
            "case_id": "CASE4036_2_packet_rejected",
            "verdict": "FINITE_cT_cEM_BOUND_BRANCH_REQUIRED",
            "claim_result": "NO_PUBLIC_LOCAL_GR_CLAIM_FROM_4036",
            "reason": "hidden conformal matter or hidden Maxwell multiplier countermodels are real if allowed",
            "next_action": "use UNIT4036 rows to source numeric c_T,c_EM priors and alpha(lambda) rows",
            "timestamp_utc": ts,
        },
    ]


def decision_rows(ts: str) -> List[Dict[str, object]]:
    return [
        {
            "decision_id": "DEC4036_0_theorem",
            "decision": "The no-Hom/source-slot theorem has been derived as an exact theorem of the typed minimal parent packet.",
            "status": "CONDITIONAL_THEOREM_DERIVED",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
        {
            "decision_id": "DEC4036_1_not_enough",
            "decision": "This is not yet a local-GR pass because the parent packet itself is still a theory-signature choice, not a completed derivation from a higher parent.",
            "status": "CLAIM_GUARD_ACTIVE",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
        {
            "decision_id": "DEC4036_2_fallback",
            "decision": "If the packet is rejected, c_T and c_EM now have explicit units and countermodels, so the fallback branch can be numerically bounded rather than hand-waved.",
            "status": "BOUND_BRANCH_READY_IN_UNITS_NOT_NUMBERS",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
        {
            "decision_id": "DEC4036_3_next",
            "decision": "Move to 4037-Y5-R2FR-minimal-parent-packet-signature-or-cT-cEM-bound-smoke.md.",
            "status": "NEXT_TARGET_SELECTED",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
    ]


def claim_rows(ts: str) -> List[Dict[str, object]]:
    return [
        {
            "claim_id": "CLAIM4036_0_R10",
            "claim": "R10/local short-range gravity pass",
            "allowed": False,
            "reason": "c_T,c_EM zero is conditional and alpha normalization still separate",
            "timestamp_utc": ts,
        },
        {
            "claim_id": "CLAIM4036_1_PPN",
            "claim": "local PPN/local-GR pass",
            "allowed": False,
            "reason": "remaining flux, boundary, non-Hilbert, and second-order PPN residuals are not closed",
            "timestamp_utc": ts,
        },
        {
            "claim_id": "CLAIM4036_2_source_only_vertices",
            "claim": "direct source-only c_T,c_EM excluded",
            "allowed": False,
            "reason": "allowed only inside the unsigned minimal packet; not yet parent-signed as global theory claim",
            "timestamp_utc": ts,
        },
    ]


def next_rows(ts: str) -> List[Dict[str, object]]:
    return [
        {
            "row_id": "NEXT4036_0",
            "next_doc": "4037-Y5-R2FR-minimal-parent-packet-signature-or-cT-cEM-bound-smoke.md",
            "next_script": "scripts/Y5_R2FR_4037_minimal_parent_packet_signature_or_cT_cEM_bound_smoke.py",
            "why": "4036 turned the missing coupling into a clean fork: sign the typed parent packet and set direct c_T,c_EM to zero, or reject it and score finite c_T,c_EM bounds.",
            "fallback": "if packet signature fails, build numeric nonclaim c_T/c_EM alpha(lambda) smoke rows using UNIT4036 dimensions",
            "timestamp_utc": ts,
        }
    ]


def status_rows(ts: str) -> List[Dict[str, object]]:
    return [
        {
            "status_id": "STATUS4036_0",
            "checkpoint": "4036",
            "canonical_status": "NO_HOM_SOURCE_SLOT_THEOREM_CONDITIONAL_CTE_CEM_UNIT_BRANCH_READY",
            "strongest_result": "Inside the typed minimal parent packet, source-only Z*T_H and Z*F_EM^2 vertices are illegal by chain rule/no-Hom, so direct c_T,c_EM vanish conditionally.",
            "still_missing": "parent packet signature as the actual parent action language; remaining flux/boundary/non-Hilbert residual closure; alpha normalization",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": ts,
        }
    ]


def render_doc(ts: str, sources: List[Dict[str, object]]) -> str:
    found = sum(1 for row in sources if row["exists"] and row["needle_found"])
    total = len(sources)
    return f"""# 4036 - No-Hom Source Slot Theorem Or cT cEM Units

- Timestamp: `{ts}`
- Status: `private_nonclaim_checkpoint`
- Scope: `post-checkpoint-work` only; no `formalization-workbench` edits.
- Source needles found: `{found}/{total}`.

## What Actually Moved

4036 stops treating the coupling problem as a vague missing piece. It gives the exact conditional theorem:

If the ordinary matter and EM actions factor only through the observed quotient stack `Qvis=q(Phi)`, with fixed representation labels and no pre-variation source/readout marker, then hidden/source-slot objects have no parent morphism into the matter or EM action scalar.

In that typed packet, the direct vertices

- `Z*T_H`;
- `Z*F_EM^2`;

are not legal monomials. Therefore direct `c_T` and ordinary direct `c_EM` are zero inside that packet.

## Proof Skeleton

Write

`S_ord[Phi,psi]=Sbar_ord[Qvis(Phi),psi,theta,A_obs(Qvis)]`.

Then along a hidden/source-slot variation `v_Z`,

`delta_Z S_ord = <delta Sbar_ord/dQvis, DQvis[v_Z]> + <E_psi,delta_Z psi> + boundary`.

If `DQvis[v_Z]=0`, matter is on-shell/gauge-lifted, labels are fixed, and the boundary class is fixed, the bulk variation vanishes. A `Z*T_H` term would have produced a nonzero `T_H` contribution, so it is excluded by typing, not by hope.

The same argument applies to EM only if Maxwell has one observed Hodge/normalization owner. If a hidden multiplier `f(Z)F_EM^2` is allowed, `c_EM` is real and must be bounded.

## Fallback Units

If the packet is rejected:

- `F=Gamma_eff-Gamma0` has dimension `L^-2` for dimensionless `u`.
- `T_H` and normalized EM action/stress scalars have dimension `L^-4` in natural units.
- Therefore `c_T` and normalized `c_EM` have dimension `L^2 = mass^-2`.
- In SI energy-density convention, the comparison unit is `m/J`; `G/c^4` is the GR scale.

## Current Verdict

- Current evaluator result: `NO_HOM_THEOREM_DERIVED_CONDITIONAL_PARENT_UNSIGNED`.
- Claim result: `NO_PUBLIC_LOCAL_GR_CLAIM_FROM_4036`.
- Real progress: the missing coupling fork is now exact: either sign the typed parent packet or score finite `c_T,c_EM` bounds.

## Next Target

- `4037-Y5-R2FR-minimal-parent-packet-signature-or-cT-cEM-bound-smoke.md`
- `scripts/Y5_R2FR_4037_minimal_parent_packet_signature_or_cT_cEM_bound_smoke.py`
"""


def build_validation_rows(
    ts: str,
    sources: List[Dict[str, object]],
    theorem: List[Dict[str, object]],
    chain_rule: List[Dict[str, object]],
    countermodels: List[Dict[str, object]],
    unit_law: List[Dict[str, object]],
    evaluator: List[Dict[str, object]],
    decisions: List[Dict[str, object]],
    claims: List[Dict[str, object]],
    next_target: List[Dict[str, object]],
    compile_ok: bool,
) -> List[Dict[str, object]]:
    def ok(check_id: str, passed: bool, detail: str) -> Dict[str, object]:
        return {"check_id": check_id, "passed": bool(passed), "detail": detail, "timestamp_utc": ts}

    output_paths = [str(path) for path in OUTPUTS.values()] + [str(DOC_PATH), str(SCRIPT_PATH)]
    return [
        ok("VAL4036_00_sources_exist", all(row["exists"] for row in sources), "all cited source paths exist"),
        ok("VAL4036_01_needles_found", all(row["needle_found"] for row in sources), "all source needles found"),
        ok("VAL4036_02_theorem_statement", any(row["theorem_id"] == "THM4036_0_statement" for row in theorem), "theorem statement present"),
        ok("VAL4036_03_theorem_conclusion", any(row["theorem_id"] == "THM4036_4_conclusion" for row in theorem), "theorem conclusion present"),
        ok("VAL4036_04_chain_rule", any(row["proof_id"] == "PROOF4036_1_vertical_chain_rule" for row in chain_rule), "chain-rule proof row present"),
        ok("VAL4036_05_no_monomial", any(row["proof_id"] == "PROOF4036_2_no_monomial" for row in chain_rule), "no-monomial proof row present"),
        ok("VAL4036_06_EM_chain_rule", any(row["proof_id"] == "PROOF4036_3_EM_chain_rule" for row in chain_rule), "EM chain-rule proof row present"),
        ok("VAL4036_07_matter_countermodel", any(row["countermodel_id"] == "CM4036_0_hidden_conformal_matter" for row in countermodels), "matter countermodel present"),
        ok("VAL4036_08_EM_countermodel", any(row["countermodel_id"] == "CM4036_1_hidden_Maxwell_multiplier" for row in countermodels), "EM countermodel present"),
        ok("VAL4036_09_cT_units", any(row["unit_id"] == "UNIT4036_1_cT_natural" for row in unit_law), "c_T unit law present"),
        ok("VAL4036_10_cEM_units", any(row["unit_id"] == "UNIT4036_2_cEM_normalized" for row in unit_law), "c_EM unit law present"),
        ok("VAL4036_11_time_window_guard", any(row["unit_id"] == "UNIT4036_4_time_window" for row in unit_law), "time-window guard present"),
        ok("VAL4036_12_current_verdict", any(row["case_id"] == "CASE4036_1_current" for row in evaluator), "current evaluator verdict present"),
        ok("VAL4036_13_no_claims", all(row["allowed"] is False for row in claims), "all claim gates remain false"),
        ok("VAL4036_14_next_decision", any(row["decision_id"] == "DEC4036_3_next" for row in decisions), "4037 next decision present"),
        ok("VAL4036_15_next_target", bool(next_target and "4037" in str(next_target[0]["next_doc"])), "next target row present"),
        ok("VAL4036_16_doc_written", DOC_PATH.exists(), "checkpoint doc written"),
        ok("VAL4036_17_no_formalization_output", all(str(FORMALIZATION) not in path for path in output_paths), "no output targets formalization-workbench"),
        ok("VAL4036_18_script_compiles", compile_ok, "script compiles"),
        ok("VAL4036_19_private_nonclaim", all(str(row.get("valid_for_claim", False)) == "False" for table in [theorem, chain_rule, countermodels, unit_law, decisions] for row in table), "all theorem/fallback rows remain nonclaim"),
    ]


def main() -> None:
    ts = timestamp()
    sources = source_specs(ts)
    theorem = theorem_rows(ts)
    chain_rule = chain_rule_rows(ts)
    countermodels = countermodel_rows(ts)
    unit_law = unit_rows(ts)
    evaluator = evaluator_rows(ts)
    decisions = decision_rows(ts)
    claims = claim_rows(ts)
    next_target = next_rows(ts)
    status = status_rows(ts)

    DOC_PATH.write_text(render_doc(ts, sources), encoding="utf-8")
    write_csv(OUTPUTS["source_register"], sources)
    write_csv(OUTPUTS["theorem"], theorem)
    write_csv(OUTPUTS["chain_rule"], chain_rule)
    write_csv(OUTPUTS["countermodels"], countermodels)
    write_csv(OUTPUTS["unit_law"], unit_law)
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

    validation = build_validation_rows(
        ts,
        sources,
        theorem,
        chain_rule,
        countermodels,
        unit_law,
        evaluator,
        decisions,
        claims,
        next_target,
        compile_ok,
    )
    write_csv(OUTPUTS["validation"], validation)
    passed = sum(1 for row in validation if row["passed"])
    total = len(validation)
    print(f"4036 validation: {passed}/{total} passed")
    if passed != total:
        for row in validation:
            if not row["passed"]:
                print(f"FAIL {row['check_id']}: {row['detail']}")
        raise SystemExit(1)
    print(f"Wrote {DOC_PATH}")


if __name__ == "__main__":
    main()
