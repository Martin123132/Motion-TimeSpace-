from __future__ import annotations

import csv
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "3408-Y5-R2FR-minimum-GR-pole-Hhh-Rh-Jh-derivation-under-AX1090.md"

SOURCES = {
    "doc_3407": ROOT / "3407-Y5-R2FR-minimal-parent-Hessian-source-table-under-AX1090.md",
    "next_3407": OUT / "P8_Y5_R2FR_3407_NEXT_TARGET.csv",
    "candidate_3407": OUT / "P8_Y5_R2FR_3407_CANDIDATE_HRJ_SOURCE_TABLE.csv",
    "claim_ready_3407": OUT / "P8_Y5_R2FR_3407_CLAIM_READY_HRJ_TABLE.csv",
    "requirements_3407": OUT / "P8_Y5_R2FR_3407_MINIMAL_HRJ_REQUIREMENTS.csv",
    "action_blocks": OUT / "P8_MIN_PARENT_LOCAL_GR_ACTION_BLOCKS.csv",
    "hilbert_3340": OUT / "P8_Y5_R2FR_3340_PARENT_HILBERT_SOURCE_CLAUSE.csv",
    "g_policy_3404": OUT / "P8_Y5_R2FR_3404_NEWTON_G_POLICY.csv",
    "hsm_contract": OUT / "P8_Y5_HAMILTONIAN_SOURCE_MEASURE_CONTRACT.csv",
    "gpub_3316": OUT / "P8_Y5_R2FR_3316_HESSIAN_READOUT_DERIVATION.csv",
    "prop_tests_3406": OUT / "P8_Y5_R2FR_3406_PUBLIC_PROPAGATOR_TESTS.csv",
    "impact_3406": OUT / "P8_Y5_R2FR_3406_SELECTOR_IMPACT.csv",
}

OUTPUTS = {
    "source_register": OUT / "P8_Y5_R2FR_3408_SOURCE_REGISTER.csv",
    "minimum_pole_premises": OUT / "P8_Y5_R2FR_3408_MINIMUM_GR_POLE_PREMISES.csv",
    "Hhh_derivation": OUT / "P8_Y5_R2FR_3408_HHH_EH_HESSIAN_DERIVATION.csv",
    "Rh_derivation": OUT / "P8_Y5_R2FR_3408_RH_READOUT_DERIVATION.csv",
    "Jh_derivation": OUT / "P8_Y5_R2FR_3408_JH_HILBERT_SOURCE_DERIVATION.csv",
    "Gref_normalization": OUT / "P8_Y5_R2FR_3408_GREF_NORMALIZATION_ROW.csv",
    "boundary_gauge_contract": OUT / "P8_Y5_R2FR_3408_BOUNDARY_GAUGE_CONTRACT.csv",
    "minimum_pole_row": OUT / "P8_Y5_R2FR_3408_MINIMUM_GR_POLE_ROW.csv",
    "Newton_Maxwell_implications": OUT / "P8_Y5_R2FR_3408_NEWTON_MAXWELL_IMPLICATIONS.csv",
    "blocker_audit": OUT / "P8_Y5_R2FR_3408_CLAIM_BLOCKER_AUDIT.csv",
    "promotion_gates": OUT / "P8_Y5_R2FR_3408_PROMOTION_GATES.csv",
    "decision_ledger": OUT / "P8_Y5_R2FR_3408_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_R2FR_3408_NEXT_TARGET.csv",
    "runner_nonclaim": OUT / "P8_Y5_R2FR_3408_RUNNER_NONCLAIM.csv",
    "validation": OUT / "P8_Y5_BRR545_3408_VALIDATION.csv",
}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = list(rows[0].keys())
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def md_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return ""
    fields = list(rows[0].keys())
    clean = lambda value: str(value).replace("\n", " ").replace("|", "/")
    lines = [
        "| " + " | ".join(fields) + " |",
        "| " + " | ".join("---" for _ in fields) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(clean(row.get(field, "")) for field in fields) + " |")
    return "\n".join(lines)


def source_register() -> list[dict[str, Any]]:
    roles = {
        "candidate_3407": "minimum HRJ candidate rows feeding 3408",
        "claim_ready_3407": "nonclaim status of prior HRJ table",
        "action_blocks": "EH core, kappa, matter, boundary and readout action anchors",
        "hilbert_3340": "Hilbert matter+EM source and Maxwell/Poynting source ownership",
        "g_policy_3404": "common G_ref policy",
        "hsm_contract": "Hamiltonian/PiM/source-measure contracts needed after pole anchoring",
        "gpub_3316": "public propagator formula and residue ratio",
        "prop_tests_3406": "massless pole test definition",
    }
    return [
        {
            "source_id": key,
            "path": str(path),
            "exists": path.exists(),
            "role": roles.get(key, "supporting checkpoint/source evidence"),
            "valid_for_claim": False,
        }
        for key, path in SOURCES.items()
    ]


def minimum_pole_premises() -> list[dict[str, Any]]:
    return [
        {
            "premise_id": "MGP3408_0_parent_EH_core",
            "premise": "the local observed metric block of the parent action contains S_EH=(2*kappa0)^-1 int sqrt(-g_obs)(R-2Lambda0)",
            "source": str(SOURCES["action_blocks"]),
            "current_status": "CANDIDATE_ANCHOR_PRESENT_NOT_TOTAL_PARENT_SIGNED",
            "needed_for_claim": "derive this block from the parent quotient action rather than selecting it as a reference anchor",
            "valid_for_claim": False,
        },
        {
            "premise_id": "MGP3408_1_constant_kappa",
            "premise": "kappa0 is a local branch constant with kappa0=8*pi*G_ref/c^4",
            "source": str(SOURCES["action_blocks"]),
            "current_status": "CONDITIONAL_BRANCH_CONSTANT_NOT_DERIVED",
            "needed_for_claim": "topological/superselection or fixed-branch argument for no local kappa drift",
            "valid_for_claim": False,
        },
        {
            "premise_id": "MGP3408_2_readout_identity",
            "premise": "g_pub=g_obs to first order, so R_h=identity_on_delta_g for the massless metric perturbation",
            "source": str(SOURCES["action_blocks"]),
            "current_status": "CANDIDATE_READOUT_NOT_SIGNED_THROUGH_OU2",
            "needed_for_claim": "same observed coframe/matter/clocks/orbits/readout theorem",
            "valid_for_claim": False,
        },
        {
            "premise_id": "MGP3408_3_Hilbert_source",
            "premise": "matter and EM source the observed metric by one Hilbert stress tensor before calibration",
            "source": str(SOURCES["hilbert_3340"]),
            "current_status": "EXACT_CONDITIONAL_NOT_PARENT_ADOPTED",
            "needed_for_claim": "parent matter+EM action adoption, public Hodge/current normalization, no hidden source weights",
            "valid_for_claim": False,
        },
        {
            "premise_id": "MGP3408_4_boundary_gauge",
            "premise": "gauge zero modes are fixed/quotiented and boundary terms are fixed/self-adjoint/source-blind",
            "source": str(SOURCES["requirements_3407"]),
            "current_status": "BOUNDARY_AND_GAUGE_CLASS_OPEN",
            "needed_for_claim": "self-adjoint boundary class, fixed reference, no edge charge",
            "valid_for_claim": False,
        },
    ]


def Hhh_derivation() -> list[dict[str, Any]]:
    return [
        {
            "step_id": "HHH3408_0_action",
            "derivation_step": "Start from the candidate EH metric block.",
            "formula": "S_EH[g_obs]=(2*kappa0)^-1 int sqrt(-g_obs)(R[g_obs]-2 Lambda0)",
            "result": "the second variation defines the metric Hessian H_hh",
            "status": "CANDIDATE_PARENT_BLOCK",
            "valid_for_claim": False,
        },
        {
            "step_id": "HHH3408_1_linearize",
            "derivation_step": "Expand g_obs=bar_g+h around the local branch with Lambda background-subtracted or negligible.",
            "formula": "delta^2 S_EH = (1/(2*kappa0)) <h, E_FP[bar_g] h> + boundary",
            "result": "H_hh=(1/kappa0) E_FP up to convention and fixed boundary terms",
            "status": "MATH_DERIVED_IF_EH_BLOCK_OWNED",
            "valid_for_claim": False,
        },
        {
            "step_id": "HHH3408_2_spin_projector",
            "derivation_step": "In local flat/high-frequency principal symbol, gauge-fixed E_FP carries the massless spin-2 projector.",
            "formula": "H_hh(k) -> (k^2/kappa0) P^(2) + gauge/constraint/contact pieces",
            "result": "positive massless TT pole after gauge fixing if kappa0>0",
            "status": "CONDITIONAL_SPIN2_HESSIAN_ROW",
            "valid_for_claim": False,
        },
        {
            "step_id": "HHH3408_3_residue",
            "derivation_step": "Invert on conserved Hilbert sources after quotienting gauge modes.",
            "formula": "H_hh^{-1} -> kappa0 P^(2)/k^2 + gauge/contact terms that vanish against conserved T",
            "result": "massless public spin-2 pole exists conditionally",
            "status": "FORMULA_READY_NOT_PARENT_CLAIM",
            "valid_for_claim": False,
        },
    ]


def Rh_derivation() -> list[dict[str, Any]]:
    return [
        {
            "step_id": "RH3408_0_readout",
            "derivation_step": "Use the observed metric readout candidate.",
            "formula": "g_pub = g_obs + O((Phi-Phi0)^2)",
            "result": "delta g_pub/delta h = identity at first order",
            "status": "CANDIDATE_FROM_A511_6",
            "valid_for_claim": False,
        },
        {
            "step_id": "RH3408_1_public_map",
            "derivation_step": "Insert the metric readout into the public propagator.",
            "formula": "R_{mn,h}=I_{mn}^{ab}; R_h H_hh^{-1} R_h^T = H_hh^{-1}",
            "result": "the EH pole is visible to public metric observables if the readout theorem is signed",
            "status": "EXACT_IF_READOUT_SIGNED",
            "valid_for_claim": False,
        },
        {
            "step_id": "RH3408_2_guard",
            "derivation_step": "Retain a guard against disformal/Weyl/source-slot readout leakage.",
            "formula": "R_x=0 at first order for extra fields, or residue B_x must be evaluated",
            "result": "R_h identity does not silence extra modes by itself",
            "status": "GUARD_ACTIVE",
            "valid_for_claim": False,
        },
    ]


def Jh_derivation() -> list[dict[str, Any]]:
    return [
        {
            "step_id": "JH3408_0_variation",
            "derivation_step": "Vary the descended matter+EM action with respect to g_obs.",
            "formula": "T_total^{mn}=(-2/sqrt(-g_obs)) delta(S_matter+S_EM)/delta g_obs_mn",
            "result": "delta S_source = 1/2 int sqrt(-g_obs) T_total^{mn} delta g_obs_mn up to sign convention",
            "status": "EXACT_CONDITIONAL_HILBERT_FORMULA",
            "valid_for_claim": False,
        },
        {
            "step_id": "JH3408_1_metric_covector",
            "derivation_step": "For h=delta g_obs, identify the metric source covector.",
            "formula": "J_h = 1/2 sqrt(-g_obs) T_total^{mn} in configuration-space normalization",
            "result": "J_h is the source side of the massless metric pole",
            "status": "EXACT_IF_PARENT_MATTER_DESCENT_SIGNED",
            "valid_for_claim": False,
        },
        {
            "step_id": "JH3408_2_EM_Poynting",
            "derivation_step": "Include Maxwell/Poynting stress in T_total, not in a hidden boundary/source shadow.",
            "formula": "S_EM=-(lambda0/4) int sqrt(-g_obs) F_mn F^mn; T_EM^{mn} from Hilbert variation",
            "result": "radiative and static EM stress source the same metric pole if public Hodge/current normalization is signed",
            "status": "CONDITIONAL_EM_SOURCE_SLOT",
            "valid_for_claim": False,
        },
    ]


def Gref_normalization() -> list[dict[str, Any]]:
    return [
        {
            "row_id": "GN3408_0_kappa_relation",
            "statement": "The pole normalization reduces to Newton/GR if kappa0=8*pi*G_ref/c^4.",
            "formula": "G_mn+Lambda g_mn = kappa0 T_mn; weak-field slow-motion gives nabla^2 Phi=4*pi G_ref rho",
            "status": "STANDARD_CONDITIONAL_NORMALIZATION",
            "valid_for_claim": False,
        },
        {
            "row_id": "GN3408_1_no_G_numerology",
            "statement": "The numerical value of G_ref may be calibrated, but it must be the same branch constant in field, source and readout.",
            "formula": "mu=G_ref M_H[Pi_M J_H]; U=mu/r; no separate G_field/G_source/G_orbit",
            "status": "POLICY_FROM_3404_NOT_PARENT_DERIVED",
            "valid_for_claim": False,
        },
    ]


def boundary_gauge_contract() -> list[dict[str, Any]]:
    return [
        {
            "contract_id": "BGC3408_0_gauge",
            "needed_contract": "diffeomorphism gauge modes in H_hh are quotient/null directions with no source residue",
            "formula": "v_gauge in ker H_hh, R_h v_gauge pure coordinate, J_h v_gauge=0 by conservation",
            "current_status": "STANDARD_IF_HILBERT_WARD_AND_Q_BASIC_GAUGE_SIGNED",
            "valid_for_claim": False,
        },
        {
            "contract_id": "BGC3408_1_boundary",
            "needed_contract": "EH boundary term/reference makes the variational problem self-adjoint and source-blind",
            "formula": "delta(S_EH+S_GHY+B_ref)|boundary=0 with fixed induced metric/reference class",
            "current_status": "CANDIDATE_FROM_A511_5_NOT_PARENT_SIGNED",
            "valid_for_claim": False,
        },
        {
            "contract_id": "BGC3408_2_conserved_source",
            "needed_contract": "T_total is conserved in the same observed geometry at the pole test order",
            "formula": "nabla_m T_total^{mn}=0 from one descended diffeomorphism-invariant matter+EM action",
            "current_status": "CONDITIONAL_FROM_3340",
            "valid_for_claim": False,
        },
    ]


def minimum_pole_row() -> list[dict[str, Any]]:
    return [
        {
            "pole_row_id": "MGR3408_0_minimum_GR_pole",
            "H_hh": "H_hh(k)=(k^2/kappa0) P^(2)+gauge/contact after EH second variation and gauge fixing",
            "R_h": "identity_on_delta_g if g_pub=g_obs+O((Phi-Phi0)^2)",
            "J_h": "1/2 T_total^{mn} from Hilbert variation of matter+EM",
            "Gref_lock": "kappa0=8*pi*G_ref/c^4; same G_ref used in mu=G_ref M_H[Pi_M J_H]",
            "pole_result": "R_h H_hh^{-1} J_h gives positive massless spin-2 exchange proportional to G_ref P^(2)/k^2",
            "current_status": "EXACT_CONDITIONAL_MINIMUM_ROW_NOT_PARENT_SIGNED",
            "claim_ready": False,
            "valid_for_claim": False,
        },
        {
            "pole_row_id": "MGR3408_1_claim_gap",
            "H_hh": "candidate anchor exists",
            "R_h": "candidate readout exists",
            "J_h": "conditional Hilbert source exists",
            "Gref_lock": "policy/contract exists",
            "pole_result": "not claim-ready because parent action reduction, readout theorem, Hilbert adoption, boundary/gauge class and source charge lock are not all signed",
            "current_status": "BLOCKED_FROM_PROMOTION",
            "claim_ready": False,
            "valid_for_claim": False,
        },
    ]


def Newton_Maxwell_implications() -> list[dict[str, Any]]:
    return [
        {
            "impact_id": "NM3408_0_Newton",
            "if_minimum_row_signed": "Newtonian Poisson/Gauss limit follows with same G_ref and Hilbert/PiM mass source",
            "remaining_guard": "Hamiltonian/PiM worldtube source measure and no extra mass channel still need signing",
            "valid_for_claim": False,
        },
        {
            "impact_id": "NM3408_1_GR_metric_core",
            "if_minimum_row_signed": "massless metric pole anchors the GR/EH core for gamma/beta before extra-mode residues",
            "remaining_guard": "extra scalar/vector/connection/domain/boundary/q_loc residues still need zero or bounds",
            "valid_for_claim": False,
        },
        {
            "impact_id": "NM3408_2_Maxwell_EM",
            "if_minimum_row_signed": "Maxwell/Poynting stress sources the same pole through T_total",
            "remaining_guard": "public Hodge/current normalization and no hidden EM source shadow must be signed",
            "valid_for_claim": False,
        },
    ]


def blocker_audit() -> list[dict[str, Any]]:
    return [
        {
            "blocker_id": "BLK3408_0_parent_action",
            "blocker": "EH block is a candidate anchor, not derived as the complete parent quotient metric block",
            "needed_fix": "derive parent action reduction to S_EH plus explicit residual sectors",
            "blocks_claim": True,
            "valid_for_claim": False,
        },
        {
            "blocker_id": "BLK3408_1_readout",
            "blocker": "g_pub=g_obs identity is not signed through all matter/clocks/orbits/PPN readout",
            "needed_fix": "same observed coframe/readout theorem through O(U^2)",
            "blocks_claim": True,
            "valid_for_claim": False,
        },
        {
            "blocker_id": "BLK3408_2_Hilbert_EM",
            "blocker": "Hilbert matter+EM source is exact conditional but parent adoption/Hodge/current normalization are unsigned",
            "needed_fix": "adopt one descended matter+EM action and forbid hidden source weights",
            "blocks_claim": True,
            "valid_for_claim": False,
        },
        {
            "blocker_id": "BLK3408_3_boundary_gauge",
            "blocker": "boundary self-adjointness, fixed reference and gauge/zero-mode classification are not fully signed",
            "needed_fix": "fixed EH/GHY/reference boundary class and q-basic gauge kernel proof",
            "blocks_claim": True,
            "valid_for_claim": False,
        },
        {
            "blocker_id": "BLK3408_4_extra_modes",
            "blocker": "minimum GR pole does not silence non-EH residues",
            "needed_fix": "compute/zero/bound extra-mode residues relative to the massless pole",
            "blocks_claim": True,
            "valid_for_claim": False,
        },
    ]


def promotion_gates() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "GATE3408_0_math_row",
            "claim": "minimum GR pole row is mathematically derived conditionally",
            "gate_pass": True,
            "reason": "EH second variation, identity readout and Hilbert source give a massless spin-2 pole if their parent clauses are signed",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "GATE3408_1_parent_signed",
            "claim": "minimum GR pole row is parent-signed",
            "gate_pass": False,
            "reason": "action reduction, readout identity, Hilbert adoption and boundary/gauge class remain unsigned together",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "GATE3408_2_Newton_GR_anchor",
            "claim": "Newton/GR pole is claim-ready",
            "gate_pass": False,
            "reason": "common source measure and G_ref lock are conditional, and extra residues remain live",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "GATE3408_3_local_GR",
            "claim": "local GR/PPN is derived",
            "gate_pass": False,
            "reason": "non-EH residues, q_loc vector projections, beta/gamma/full PPN gates remain downstream",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def decision_ledger() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3408_0_progress",
            "finding": "the minimum GR pole row is now written as an exact conditional derivation",
            "reason": "H_hh from EH second variation, R_h from observed metric readout, J_h from Hilbert matter+EM source, and G_ref normalization are in one row",
            "next_action": "do not claim it; either parent-sign the blockers or use it as the reference denominator for residue bounds",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC3408_1_no_claim",
            "finding": "the row is not parent-signed",
            "reason": "the derivation rests on candidate/conditional clauses rather than a complete MTS parent action reduction",
            "next_action": "move to non-EH residue bound pack unless pursuing parent-action reduction directly",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC3408_2_best_next",
            "finding": "best next target is non-EH residue bound pack relative to the conditional GR pole",
            "reason": "the GR pole denominator is now explicit enough for no-cancellation fallback rows, while parent signing may remain longer-term",
            "next_action": "build 3409 non-EH residue-bound pack for scalar, massive spin2, connection, domain/memory/bulk and q_loc projections",
            "valid_for_claim": False,
        },
    ]


def next_target() -> list[dict[str, Any]]:
    return [
        {
            "target_id": "3409-Y5-R2FR-nonEH-residue-bound-pack-relative-to-GR-pole-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3409_nonEH_residue_bound_pack_relative_to_GR_pole.py",
            "objective": "convert surviving non-EH channels into no-cancellation pole-residue bound rows using the conditional GR pole as denominator",
            "why_next": "this prevents the derivation route from stalling while keeping local-GR claims blocked until extra residues are zero or bounded",
            "valid_for_claim": False,
        },
        {
            "target_id": "3410-Y5-R2FR-parent-action-reduction-signature-for-minimum-GR-pole-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3410_parent_action_reduction_signature_for_minimum_GR_pole.py",
            "objective": "attempt to parent-sign the action/readout/Hilbert/boundary clauses needed to promote MGR3408_0",
            "why_next": "this is the constructive proof route if the aim is promotion rather than fallback bounding",
            "valid_for_claim": False,
        },
    ]


def runner_nonclaim() -> list[dict[str, Any]]:
    return [
        {
            "runner_id": "RUN3408_0_scope",
            "check": "writes only 3408 files under post-checkpoint-work",
            "status": "PASS_IF_VALIDATION_TRUE",
            "valid_for_claim": False,
        },
        {
            "runner_id": "RUN3408_1_no_claim",
            "check": "conditional minimum GR pole row is not promoted to claim-ready",
            "status": "NONCLAIM_DERIVATION",
            "valid_for_claim": False,
        },
        {
            "runner_id": "RUN3408_2_forward",
            "check": "next target moves to non-EH residue bounds or parent-signature promotion",
            "status": "FORK_READY",
            "valid_for_claim": False,
        },
    ]


def validation(outputs: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    def add(check_id: str, check: str, passed: bool, detail: str = "") -> None:
        rows.append({"check_id": check_id, "check": check, "passed": bool(passed), "detail": detail})

    generated_paths = [str(path) for path in OUTPUTS.values()] + [str(DOC)]
    all_nonclaim = all(
        str(row.get("valid_for_claim", False)).lower() == "false"
        for name, table in outputs.items()
        if name != "validation"
        for row in table
    )
    pole_rows_nonclaim = not any(str(row.get("claim_ready", False)).lower() == "true" for row in outputs["minimum_pole_row"])

    add("VAL3408_0_sources", "all registered sources exist", all(row["exists"] for row in outputs["source_register"]), f"sources={len(outputs['source_register'])}")
    add("VAL3408_1_premises", "minimum pole premises written", len(outputs["minimum_pole_premises"]) >= 5, "")
    add("VAL3408_2_Hhh", "H_hh derivation written", any("P^(2)" in row["formula"] for row in outputs["Hhh_derivation"]), "")
    add("VAL3408_3_Rh", "R_h readout derivation written", any("identity" in (row["formula"] + row["result"]) for row in outputs["Rh_derivation"]), "")
    add("VAL3408_4_Jh", "J_h Hilbert source derivation written", any("T_total" in row["formula"] for row in outputs["Jh_derivation"]), "")
    add("VAL3408_5_pole_row", "minimum GR pole row written but nonclaim", len(outputs["minimum_pole_row"]) >= 2 and pole_rows_nonclaim, "")
    add("VAL3408_6_blockers", "claim blockers retained", len(outputs["blocker_audit"]) >= 5 and all(row["blocks_claim"] for row in outputs["blocker_audit"]), "")
    add("VAL3408_7_gates", "parent/local-GR gates remain blocked", not any(row["gate_pass"] for row in outputs["promotion_gates"] if row["gate_id"] in {"GATE3408_1_parent_signed", "GATE3408_2_Newton_GR_anchor", "GATE3408_3_local_GR"}), "")
    add("VAL3408_8_no_overclaim", "all generated rows are nonclaim", all_nonclaim, "")
    add("VAL3408_9_scope", "no 3408 output path targets formalization-workbench", "formalization-workbench" not in "\n".join(generated_paths), "")
    add("VAL3408_10_next", "next target is non-EH residue bound pack", any("nonEH-residue-bound-pack" in row["target_id"] for row in outputs["next_target"]), "")
    overall = all(row["passed"] for row in rows)
    add("VAL3408_11_overall", "3408 validation overall", overall, "all required checks passed" if overall else "one or more checks failed")
    return rows


def write_doc(outputs: dict[str, list[dict[str, Any]]]) -> None:
    parts = [
        "# 3408 - Y5/R2FR minimum GR pole Hhh/Rh/Jh derivation under AX1090",
        "",
        "## Verdict",
        "",
        "- 3408 derives the minimum GR pole row conditionally: EH second variation gives `H_hh`, observed metric readout gives `R_h`, Hilbert matter+EM gives `J_h`, and common `G_ref` fixes the Newton normalization.",
        "- This is real progress because the massless GR pole denominator is now explicit enough for residue-bound fallback work.",
        "- It is not a claim. The row still depends on parent action reduction, readout identity, Hilbert source adoption, public EM/Hodge normalization, boundary/gauge class, and extra-mode residue silence.",
        "- Maxwell/Poynting stress is placed in `T_total` through Hilbert variation, not hidden in a boundary/source shadow.",
        "",
        "## Minimum Pole Premises",
        md_table(outputs["minimum_pole_premises"]),
        "",
        "## H_hh EH Hessian Derivation",
        md_table(outputs["Hhh_derivation"]),
        "",
        "## R_h Readout Derivation",
        md_table(outputs["Rh_derivation"]),
        "",
        "## J_h Hilbert Source Derivation",
        md_table(outputs["Jh_derivation"]),
        "",
        "## G_ref Normalization",
        md_table(outputs["Gref_normalization"]),
        "",
        "## Boundary Gauge Contract",
        md_table(outputs["boundary_gauge_contract"]),
        "",
        "## Minimum GR Pole Row",
        md_table(outputs["minimum_pole_row"]),
        "",
        "## Newton Maxwell Implications",
        md_table(outputs["Newton_Maxwell_implications"]),
        "",
        "## Claim Blocker Audit",
        md_table(outputs["blocker_audit"]),
        "",
        "## Promotion Gates",
        md_table(outputs["promotion_gates"]),
        "",
        "## Decision Ledger",
        md_table(outputs["decision_ledger"]),
        "",
        "## Next Target",
        md_table(outputs["next_target"]),
        "",
        "## Validation",
        md_table(outputs["validation"]),
        "",
    ]
    DOC.write_text("\n".join(parts), encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    outputs: dict[str, list[dict[str, Any]]] = {
        "source_register": source_register(),
        "minimum_pole_premises": minimum_pole_premises(),
        "Hhh_derivation": Hhh_derivation(),
        "Rh_derivation": Rh_derivation(),
        "Jh_derivation": Jh_derivation(),
        "Gref_normalization": Gref_normalization(),
        "boundary_gauge_contract": boundary_gauge_contract(),
        "minimum_pole_row": minimum_pole_row(),
        "Newton_Maxwell_implications": Newton_Maxwell_implications(),
        "blocker_audit": blocker_audit(),
        "promotion_gates": promotion_gates(),
        "decision_ledger": decision_ledger(),
        "next_target": next_target(),
        "runner_nonclaim": runner_nonclaim(),
    }
    outputs["validation"] = validation(outputs)
    for key, path in OUTPUTS.items():
        write_csv(path, outputs[key])
    write_doc(outputs)

    if not all(row["passed"] for row in outputs["validation"]):
        raise RuntimeError("3408 validation failed")

    print(f"Wrote {DOC}")
    print(f"Wrote {len(OUTPUTS)} CSV outputs under {OUT}")
    print("; ".join(f"{path.name}={len(outputs[key])}" for key, path in OUTPUTS.items()))


if __name__ == "__main__":
    main()
