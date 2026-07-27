from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
FW = REPO / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
PYCACHE = ROOT / "scripts" / "__pycache__"

CHECKPOINT = "3244"
DOC = ROOT / "3244-Y5-R2FR-single-parent-density-boundary-reference-proof-or-finite-Jtot-bound-under-AX1090.md"

OUTPUTS = {
    "sources": OUT / "P8_Y5_R2FR_3244_SOURCE_REGISTER.csv",
    "theorem": OUT / "P8_Y5_R2FR_3244_JTOT_ZERO_THEOREM_ATTEMPT.csv",
    "boundary": OUT / "P8_Y5_R2FR_3244_BOUNDARY_REFERENCE_ROLLUP.csv",
    "bound": OUT / "P8_Y5_R2FR_3244_FINITE_JTOT_BOUND_CONTRACT.csv",
    "transfer": OUT / "P8_Y5_R2FR_3244_AMPLITUDE_AND_QLOC_TRANSFER.csv",
    "gates": OUT / "P8_Y5_R2FR_3244_CLAIM_GATES.csv",
    "decision": OUT / "P8_Y5_R2FR_3244_DECISION_LEDGER.csv",
    "next": OUT / "P8_Y5_R2FR_3244_NEXT_TARGET.csv",
    "validation": OUT / "P8_Y5_R2FR_3244_VALIDATION.csv",
}

RUN_UTC = datetime.now(timezone.utc).isoformat()


def bool_str(value: bool) -> str:
    return "true" if value else "false"


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key, "") for key in fieldnames})


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def csv_ok(path: Path) -> bool:
    try:
        if not path.exists():
            return False
        read_csv(path)
        return True
    except Exception:
        return False


def parse_ok(path: Path) -> bool:
    if not path.exists():
        return False
    return csv_ok(path) if path.suffix.lower() == ".csv" else True


def evidence(path: Path, needles: list[str], limit: int = 4) -> str:
    if not path.exists():
        return "MISSING_SOURCE"
    lowered = [needle.lower() for needle in needles]
    hits: list[str] = []
    with path.open("r", encoding="utf-8", errors="ignore") as handle:
        for line_number, line in enumerate(handle, start=1):
            low = line.lower()
            if any(needle in low for needle in lowered):
                clean = " ".join(line.strip().split())
                if clean:
                    hits.append(f"L{line_number}:{clean[:220]}")
            if len(hits) >= limit:
                break
    return " | ".join(hits) if hits else "NO_MATCH"


def md_escape(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", "<br>")


def md_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    body = [
        "| " + " | ".join(md_escape(row.get(column, "")) for column in columns) + " |"
        for row in rows
    ]
    return "\n".join([header, sep, *body])


def source_register() -> list[dict[str, Any]]:
    specs = [
        (
            "SRC3244_3243",
            ROOT / "3243-Y5-R2FR-response-doublet-owner-lock-and-physical-source-gate-under-AX1090.md",
            "immediate Jtot zero-or-bound target",
            ["J_A^tot", "B_ref", "F_A^phys", "Z_*"],
        ),
        (
            "SRC3244_2981",
            ROOT / "2981-Y5-R2FR-single-action-density-line-and-species-blind-measure-or-deltawe-deproxy-under-AX1090.md",
            "single action-density and species-blind measure precursor",
            ["single action-density", "species-blind", "hbar", "measure"],
        ),
        (
            "SRC3244_2991",
            ROOT / "2991-Y5-R2FR-fixed-boundary-reference-theta-zero-proof-or-epsilon-Bv-source-bound-under-AX1090.md",
            "fixed-boundary/reference theta-zero component audit",
            ["exact boundary", "B_ref", "epsilon_Bv", "theta-zero"],
        ),
        (
            "SRC3244_2992",
            ROOT / "2992-Y5-R2FR-extra-double-zero-and-zero-odd-source-proof-or-epsilon-Qv-extra-bound-under-AX1090.md",
            "extra-sector double-zero and zero-odd-source route",
            ["double-zero", "zero-odd-source", "epsilon_Qv_extra", "boundary"],
        ),
        (
            "SRC3244_3234",
            ROOT / "3234-Y5-R2FR-Poynting-boundary-flux-silence-or-finite-bound-under-AX1090.md",
            "Poynting boundary flux finite-bound guard",
            ["Poynting", "boundary", "finite bound", "T_EM"],
        ),
        (
            "SRC3244_3241",
            ROOT / "3241-Y5-R2FR-public-EH-and-SGK-metric-response-unification-or-residual-vector-under-AX1090.md",
            "EH/SGK q_loc transfer bridge",
            ["q_loc", "E_res_GK", "metric-response", "Gamma_eff"],
        ),
        (
            "SRC3244_3242",
            ROOT / "3242-Y5-R2FR-Gamma-eff-density-owner-sign-convention-or-unified-residual-row-under-AX1090.md",
            "Gamma_eff owner and sign convention",
            ["sigma_GK=+1", "Gamma_eff", "epsilon_Gamma_owner"],
        ),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, path, role, needles in specs:
        rows.append(
            {
                "source_id": source_id,
                "source_path": str(path),
                "exists": bool_str(path.exists()),
                "parse_ok": bool_str(parse_ok(path)),
                "role": role,
                "evidence_hits": evidence(path, needles),
                "valid_for_claim": "false",
            }
        )
    return rows


def theorem_rows() -> list[dict[str, Any]]:
    return [
        {
            "step_id": "JT3244_0_theorem",
            "object": "one-branch Jtot zero theorem",
            "statement": "If the local parent action has one q-owned density line, species-blind measure, q-only matter/couplings, vertical Z, and fixed no-flux boundary reference, then J_A^tot=0 at Z=0.",
            "derivation": "D_A S_loc = D_A S_Gamma + D_A S_matter + D_A S_measure + D_A S_theta + D_A S_projector + D_A S_boundary; each term is killed by evenness, q-descent, species-blindness, fixed constants, projector silence, and boundary no-flux respectively.",
            "current_status": "EXACT_CONDITIONAL_THEOREM_NOT_PARENT_SIGNED",
            "zero_claimed_for_current_MTS": "false",
        },
        {
            "step_id": "JT3244_1_gamma",
            "object": "Gamma response density",
            "statement": "Exchange-even response doublet kills D_A Gamma_eff at the fixed point.",
            "derivation": "Gamma_eff=Gamma0+1/2 M_AB Z^A Z^B+O(Z^4) gives D_A Gamma_eff|0=0.",
            "current_status": "FORMAL_COMPONENT_ZERO_RETAINED",
            "zero_claimed_for_current_MTS": "false",
        },
        {
            "step_id": "JT3244_2_bulk_descent",
            "object": "matter/source bulk current",
            "statement": "q-only matter/source descent kills the bulk source covector.",
            "derivation": "D_A Sbar[q(Phi)]=(delta Sbar/dq) Dq[e_A]=0 when e_A in ker(Dq), with no independent source-label or representative coefficient.",
            "current_status": "CONDITIONAL_ROUTE_CLEAN_BUT_2981_UNSIGNED",
            "zero_claimed_for_current_MTS": "false",
        },
        {
            "step_id": "JT3244_3_measure_constants",
            "object": "measure, hbar and constants",
            "statement": "species-blind measure and fixed dimensionless constants kill hidden source-weight leakage.",
            "derivation": "D_A(log mu_parent)=0, D_A hbar_parent=0, and D_A theta=0 remove delta_w_A, EM/clock/mass marker, and Jacobian leakage from F_A^phys.",
            "current_status": "CONDITIONAL_ROUTE_CLEAN_BUT_PARENT_OWNER_UNSIGNED",
            "zero_claimed_for_current_MTS": "false",
        },
        {
            "step_id": "JT3244_4_boundary",
            "object": "boundary work",
            "statement": "fixed B_ref/no-flux boundary convention kills B_A.",
            "derivation": "D_A S_boundary=int_boundary(i_eA Theta + D_A B_ref); exact improvements cancel against fixed B_ref and physical flux is zero only under compact support/no-flux or a sourced finite flux bound.",
            "current_status": "PARTIAL_COMPONENT_ZERO_FROM_2991_FULL_ZERO_NOT_CLOSED",
            "zero_claimed_for_current_MTS": "false",
        },
        {
            "step_id": "JT3244_5_verdict",
            "object": "current MTS branch",
            "statement": "The theorem is mathematically sharp but not yet promotable for MTS.",
            "derivation": "The open clauses are parent action-density owner, species-blind measure/hbar, no marker/coupling reentry, projector/domain silence, and total boundary/reference no-flux.",
            "current_status": "KEEP_JTOT_BOUND_AND_DO_NOT_CLAIM_LOCAL_GR",
            "zero_claimed_for_current_MTS": "false",
        },
    ]


def boundary_rows() -> list[dict[str, Any]]:
    return [
        {
            "boundary_id": "BR3244_0_exact_component",
            "component": "exact improvement / fixed primitive",
            "zero_route": "Theta_A=d_S beta_A and B_ref=-beta_A on the chosen boundary class",
            "current_result": "2991 retains conditional exact-component zero",
            "residual_if_unsigned": "epsilon_Bv_exact_commutator",
            "valid_for_claim": "false",
        },
        {
            "boundary_id": "BR3244_1_no_flux",
            "component": "physical Poynting/worldtube flux",
            "zero_route": "S_EM dot n=0 or compact support/collar silence on parent-owned boundary",
            "current_result": "3234 derives finite Poynting flux functional, not total zero",
            "residual_if_unsigned": "Phi_Poynting_bound",
            "valid_for_claim": "false",
        },
        {
            "boundary_id": "BR3244_2_corner_topology",
            "component": "corner and topological/harmonic class",
            "zero_route": "corner anomaly absent/paired and topological class fixed before readout",
            "current_result": "2991 leaves corner/topological class unclassified",
            "residual_if_unsigned": "epsilon_Bv_corner_abs + epsilon_Bv_topological_abs",
            "valid_for_claim": "false",
        },
        {
            "boundary_id": "BR3244_3_moving_surface",
            "component": "moving tau/collar/projector boundary",
            "zero_route": "domain and projector are q-owned and D_Z of boundary embedding is zero",
            "current_result": "projector/source-measure boundary contribution remains unsigned",
            "residual_if_unsigned": "epsilon_Bv_tau_surface_commutator + epsilon_Bv_projector_boundary",
            "valid_for_claim": "false",
        },
        {
            "boundary_id": "BR3244_4_total",
            "component": "B_A total",
            "zero_route": "all boundary components close in the same branch",
            "current_result": "total boundary zero not claimed",
            "residual_if_unsigned": "B_A_bound <= sum_abs(boundary components)",
            "valid_for_claim": "false",
        },
    ]


def bound_rows() -> list[dict[str, Any]]:
    return [
        {
            "bound_id": "BND3244_0_Jtot_definition",
            "symbol": "J_A^tot",
            "formula": "J_A^tot := J_A^matter + J_A^measure + J_A^theta + J_A^projector + B_A + J_A^oddGamma",
            "required_inputs": "same branch q,Z,measure,theta,projector,boundary and normalization",
            "current_value": "MISSING_COMPONENT_ZERO_OR_NUMERIC_ROWS",
            "status": "SOURCE_READY_NONCLAIM",
            "valid_for_claim": "false",
        },
        {
            "bound_id": "BND3244_1_bulk_bound",
            "symbol": "J_A^bulk_bound",
            "formula": "|J_A^bulk| <= C_q||Dq[e_A]|| + C_src||source_label_A|| + C_mu||D_A log mu|| + C_theta||D_A theta||",
            "required_inputs": "C_q,C_src,C_mu,C_theta plus sourced branch norms",
            "current_value": "MISSING_CONSTANTS_AND_NORMS",
            "status": "FINITE_BOUND_FORM_DERIVED",
            "valid_for_claim": "false",
        },
        {
            "bound_id": "BND3244_2_boundary_bound",
            "symbol": "B_A_bound",
            "formula": "|B_A| <= ||Theta_A + D_A B_ref||_boundary + C_flux||S_EM dot n||_B + B_corner + B_top + B_projector",
            "required_inputs": "boundary norm, C_flux, EM stress flux, corner/topology/projector rows",
            "current_value": "MISSING_BOUNDARY_INPUTS",
            "status": "FINITE_BOUND_FORM_DERIVED",
            "valid_for_claim": "false",
        },
        {
            "bound_id": "BND3244_3_total_bound",
            "symbol": "||J_tot||",
            "formula": "||J_tot|| <= ||J_bulk_bound|| + ||B_bound|| + ||J_oddGamma||",
            "required_inputs": "component bounds in common units and same norm",
            "current_value": "MISSING_COMMON_NORM_AND_COMPONENT_VALUES",
            "status": "CLAIM_BLOCKED_BUT_NOW_BOUNDABLE",
            "valid_for_claim": "false",
        },
    ]


def transfer_rows() -> list[dict[str, Any]]:
    return [
        {
            "transfer_id": "TR3244_0_response_amplitude",
            "target": "response-doublet amplitude",
            "formula": "||Z_*|| <= m0^{-1} ||J_tot|| + O(||J_tot||^2)",
            "condition": "M_AB >= m0 I on the local branch",
            "effect": "finite source leakage becomes a controlled amplitude rather than a closure assumption",
            "claim_allowed": "false",
        },
        {
            "transfer_id": "TR3244_1_density_shift",
            "target": "Gamma_eff density shift",
            "formula": "|Delta Gamma_min| <= (2 m0)^{-1} ||J_tot||^2 + higher_order",
            "condition": "positive Hessian and sourced Jtot norm",
            "effect": "turns coupling leakage into a local density residual feeding epsilon_Gamma_owner",
            "claim_allowed": "false",
        },
        {
            "transfer_id": "TR3244_2_qLoc",
            "target": "q_loc local residual",
            "formula": "||q_loc||_arena <= C_arena(||nabla E_res_GK|| + ||nabla DeltaGamma_J|| + ||DeltaK||)",
            "condition": "3241 EH/SGK bridge plus arena constants",
            "effect": "connects Jtot bound to PPN/Newton/local-GR residual scoring",
            "claim_allowed": "false",
        },
        {
            "transfer_id": "TR3244_3_newton_ppn",
            "target": "Newton/PPN gate",
            "formula": "pass only if ||q_loc||_PPN, ||DeltaG_eff|| and matter-coupling residuals are below sourced bounds",
            "condition": "real arena constants and no prior-edge/placeholder rows",
            "effect": "prevents calling the branch GR-like unless the bound is actually small",
            "claim_allowed": "false",
        },
    ]


def gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "claim_gate_id": "CG3244_0_conditional_theorem",
            "claim": "one-branch Jtot zero theorem exists",
            "condition_passed": "true",
            "status": "exact conditional theorem written",
            "claim_allowed": "false",
        },
        {
            "claim_gate_id": "CG3244_1_current_Jtot_zero",
            "claim": "current MTS has Jtot=0",
            "condition_passed": "false",
            "status": "parent owner, measure, marker/projector and total boundary clauses unsigned",
            "claim_allowed": "false",
        },
        {
            "claim_gate_id": "CG3244_2_finite_Jtot",
            "claim": "current MTS has claim-grade finite Jtot bound",
            "condition_passed": "false",
            "status": "bound form derived but numeric/source component rows missing",
            "claim_allowed": "false",
        },
        {
            "claim_gate_id": "CG3244_3_amplitude_safe",
            "claim": "response amplitude is local-safe",
            "condition_passed": "false",
            "status": "requires M_AB coercivity and Jtot numeric bound",
            "claim_allowed": "false",
        },
        {
            "claim_gate_id": "CG3244_4_local_GR",
            "claim": "local GR/Newton/PPN reduction",
            "condition_passed": "false",
            "status": "requires q_loc arena transfer with sourced residuals",
            "claim_allowed": "false",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3244_0_derivation_gain",
            "decision": "Keep the conditional Jtot zero theorem as the clean derivation route.",
            "because": "It precisely states what makes the coupling vanish instead of treating coupling as mysterious.",
            "next_action": "Use it as the one-branch contract for any future parent action.",
        },
        {
            "decision_id": "DEC3244_1_no_claim",
            "decision": "Do not claim Jtot=0 or local GR for current MTS from this checkpoint.",
            "because": "2991 gives only partial boundary zero and 2981 leaves action-density/measure owner unsigned.",
            "next_action": "Keep finite Jtot bound rows active.",
        },
        {
            "decision_id": "DEC3244_2_best_next",
            "decision": "Next move should source or derive the two hardest owner clauses, not circle the theorem.",
            "because": "The theorem is now written; progress means either parent density ownership or numeric Jtot components.",
            "next_action": "Attack M_AB coercivity and first Jtot component rows in common units.",
        },
    ]


def next_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT3244_0_3245",
            "priority": "selected_primary",
            "next_doc": "3245-Y5-R2FR-MAB-coercivity-and-first-Jtot-component-bound-under-AX1090.md",
            "next_script": "scripts/Y5_R2FR_3245_MAB_coercivity_and_first_Jtot_component_bound.py",
            "objective": "Try to prove or bound M_AB positive coercivity and source the first finite Jtot component in common units, so the amplitude law can become scoreable rather than purely formal.",
            "exclude": "do not repeat broad no-marker proof; do not claim local GR; do not edit formalization-workbench",
            "valid_for_claim": "false",
        }
    ]


def validation_rows(source_rows: list[dict[str, Any]], generated_csvs: list[Path]) -> list[dict[str, Any]]:
    sources_exist = all(row["exists"] == "true" for row in source_rows)
    sources_hit = all(row["evidence_hits"] not in {"MISSING_SOURCE", "NO_MATCH"} for row in source_rows)
    csvs_parse = all(csv_ok(path) for path in generated_csvs)
    outputs_under_post = all(ROOT in path.parents for path in generated_csvs) and ROOT in DOC.parents
    formalization_3244 = list(FW.rglob("*3244*")) if FW.exists() else []
    formalization_clean = len(formalization_3244) == 0
    conditional_not_claim = any(
        row["claim_gate_id"] == "CG3244_0_conditional_theorem"
        and row["condition_passed"] == "true"
        and row["claim_allowed"] == "false"
        for row in gate_rows()
    )
    physics_claims_blocked = all(
        row["claim_allowed"] == "false"
        for row in gate_rows()
        if row["claim_gate_id"] != "CG3244_0_conditional_theorem"
    )
    bound_rows_nonclaim = all(row["valid_for_claim"] == "false" for row in bound_rows())
    transfer_nonclaim = all(row["claim_allowed"] == "false" for row in transfer_rows())
    next_written = bool(next_rows())

    checks = [
        ("VAL3244_0_sources_exist", sources_exist, "all cited source paths exist", str(sources_exist)),
        ("VAL3244_1_source_hits", sources_hit, "source evidence hits are present", str(sources_hit)),
        ("VAL3244_2_csvs_parse", csvs_parse, "all generated CSV files parse", str(csvs_parse)),
        ("VAL3244_3_outputs_under_post_checkpoint", outputs_under_post, "all outputs are under post-checkpoint-work", str(outputs_under_post)),
        ("VAL3244_4_formalization_clean", formalization_clean, "no 3244 outputs in formalization-workbench", f"formalization_3244_count={len(formalization_3244)}"),
        ("VAL3244_5_conditional_not_claim", conditional_not_claim, "conditional theorem not promoted to physics claim", str(conditional_not_claim)),
        ("VAL3244_6_physics_claims_blocked", physics_claims_blocked, "Jtot/local-GR/Newton claims remain blocked", str(physics_claims_blocked)),
        ("VAL3244_7_bound_rows_nonclaim", bound_rows_nonclaim, "finite Jtot rows remain nonclaim without numeric inputs", str(bound_rows_nonclaim)),
        ("VAL3244_8_transfer_nonclaim", transfer_nonclaim, "amplitude/qLoc transfer remains nonclaim", str(transfer_nonclaim)),
        ("VAL3244_9_next_written", next_written, "3245 next target written", str(next_written)),
        ("VAL3244_10_doc_written", DOC.exists(), "3244 markdown checkpoint exists", str(DOC.exists())),
    ]
    rows = [
        {
            "validation_id": validation_id,
            "passed": bool_str(passed),
            "requirement": requirement,
            "evidence": evidence_text,
        }
        for validation_id, passed, requirement, evidence_text in checks
    ]
    rows.append(
        {
            "validation_id": "VAL3244_OVERALL",
            "passed": bool_str(all(row["passed"] == "true" for row in rows)),
            "requirement": "3244 validation overall",
            "evidence": "all required validation rows passed",
        }
    )
    return rows


def build_doc(
    source_rows: list[dict[str, Any]],
    theorem: list[dict[str, Any]],
    boundary: list[dict[str, Any]],
    bound: list[dict[str, Any]],
    transfer: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> str:
    return "\n\n".join(
        [
            "# 3244 - Single Parent Density, Boundary Reference Proof, or Finite Jtot Bound under AX1090",
            f"Generated: `{RUN_UTC}`",
            "Status: `Y5_R2FR_3244_conditional_Jtot_zero_theorem_written_current_MTS_unsigned_finite_Jtot_bound_contract_added_nonclaim`",
            "Claim ceiling: `conditional_theorem_only_no_current_Jtot_zero_no_amplitude_pass_no_q_loc_zero_no_local_GR_no_Newton_no_PPN_no_empirical_claim`",
            "## Summary",
            "- `3244` writes the actual coupling theorem instead of circling it: if the parent branch has one q-owned density, species-blind measure/hbar, q-only matter/couplings, vertical `Z`, projector silence, and fixed no-flux `B_ref`, then `J_A^tot=0`.",
            "- Current MTS does not get the claim yet: `2981` leaves action-density/measure ownership unsigned and `2991` gives only a partial boundary/reference zero.",
            "- The useful fallback is now explicit: `J_A^tot` has bulk, measure, coupling, projector, boundary and odd-Gamma pieces with finite bound interfaces.",
            "- This connects directly back to the amplitude law: `||Z_*|| <= m0^{-1}||J_tot||` and `|Delta Gamma_min| <= (2m0)^{-1}||J_tot||^2`, pending `M_AB` coercivity and component values.",
            "## Jtot Zero Theorem Attempt",
            md_table(theorem, ["step_id", "object", "statement", "derivation", "current_status", "zero_claimed_for_current_MTS"]),
            "## Boundary Reference Rollup",
            md_table(boundary, ["boundary_id", "component", "zero_route", "current_result", "residual_if_unsigned", "valid_for_claim"]),
            "## Finite Jtot Bound Contract",
            md_table(bound, ["bound_id", "symbol", "formula", "required_inputs", "current_value", "status", "valid_for_claim"]),
            "## Amplitude and qLoc Transfer",
            md_table(transfer, ["transfer_id", "target", "formula", "condition", "effect", "claim_allowed"]),
            "## Claim Gates",
            md_table(gates, ["claim_gate_id", "claim", "condition_passed", "status", "claim_allowed"]),
            "## Decision Ledger",
            md_table(decisions, ["decision_id", "decision", "because", "next_action"]),
            "## Next Target",
            md_table(next_target, ["next_id", "priority", "next_doc", "next_script", "objective", "exclude", "valid_for_claim"]),
            "## Source Register",
            md_table(source_rows, ["source_id", "source_path", "exists", "parse_ok", "role", "evidence_hits", "valid_for_claim"]),
            "## Validation",
            md_table(validation, ["validation_id", "passed", "requirement", "evidence"]),
            "## Generated Evidence",
            "\n".join(f"- `{path}`" for path in OUTPUTS.values()),
        ]
    )


def main() -> None:
    for path in OUTPUTS.values():
        path.parent.mkdir(parents=True, exist_ok=True)
    DOC.parent.mkdir(parents=True, exist_ok=True)

    source_rows = source_register()
    theorem = theorem_rows()
    boundary = boundary_rows()
    bound = bound_rows()
    transfer = transfer_rows()
    gates = gate_rows()
    decisions = decision_rows()
    next_target = next_rows()

    write_csv(OUTPUTS["sources"], source_rows)
    write_csv(OUTPUTS["theorem"], theorem)
    write_csv(OUTPUTS["boundary"], boundary)
    write_csv(OUTPUTS["bound"], bound)
    write_csv(OUTPUTS["transfer"], transfer)
    write_csv(OUTPUTS["gates"], gates)
    write_csv(OUTPUTS["decision"], decisions)
    write_csv(OUTPUTS["next"], next_target)

    if PYCACHE.exists():
        shutil.rmtree(PYCACHE)

    generated_csvs = [
        OUTPUTS["sources"],
        OUTPUTS["theorem"],
        OUTPUTS["boundary"],
        OUTPUTS["bound"],
        OUTPUTS["transfer"],
        OUTPUTS["gates"],
        OUTPUTS["decision"],
        OUTPUTS["next"],
    ]
    validation = validation_rows(source_rows, generated_csvs)
    write_csv(OUTPUTS["validation"], validation)
    DOC.write_text(
        build_doc(source_rows, theorem, boundary, bound, transfer, gates, decisions, next_target, validation),
        encoding="utf-8",
    )
    validation = validation_rows(source_rows, generated_csvs)
    write_csv(OUTPUTS["validation"], validation)
    DOC.write_text(
        build_doc(source_rows, theorem, boundary, bound, transfer, gates, decisions, next_target, validation),
        encoding="utf-8",
    )

    if PYCACHE.exists():
        shutil.rmtree(PYCACHE)

    failed = [row for row in validation if row["passed"] != "true"]
    if failed:
        raise SystemExit(f"3244 validation failed: {failed}")


if __name__ == "__main__":
    main()
