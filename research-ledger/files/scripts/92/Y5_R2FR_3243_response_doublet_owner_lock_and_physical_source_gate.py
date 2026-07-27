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

CHECKPOINT = "3243"
DOC = ROOT / "3243-Y5-R2FR-response-doublet-owner-lock-and-physical-source-gate-under-AX1090.md"

OUTPUTS = {
    "sources": OUT / "P8_Y5_R2FR_3243_SOURCE_REGISTER.csv",
    "chain": OUT / "P8_Y5_R2FR_3243_ROLLFORWARD_CHAIN.csv",
    "derivation": OUT / "P8_Y5_R2FR_3243_FIXED_POINT_AND_AMPLITUDE_DERIVATION.csv",
    "owner_lock": OUT / "P8_Y5_R2FR_3243_PHYSICAL_OWNER_LOCK_GATE.csv",
    "residual": OUT / "P8_Y5_R2FR_3243_UNIFIED_RESIDUAL_UPDATE.csv",
    "claim_gates": OUT / "P8_Y5_R2FR_3243_CLAIM_GATES.csv",
    "decision": OUT / "P8_Y5_R2FR_3243_DECISION_LEDGER.csv",
    "next": OUT / "P8_Y5_R2FR_3243_NEXT_TARGET.csv",
    "validation": OUT / "P8_Y5_R2FR_3243_VALIDATION.csv",
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


def evidence(path: Path, needles: list[str], limit: int = 5) -> str:
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


def rel(path: Path) -> str:
    return str(path)


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
    source_specs = [
        (
            "S3243_3242_density",
            ROOT / "3242-Y5-R2FR-Gamma-eff-density-owner-sign-convention-or-unified-residual-row-under-AX1090.md",
            "latest Gamma_eff density owner and sign convention checkpoint",
            ["sigma_GK=+1", "response-doublet", "epsilon_Gamma_owner"],
        ),
        (
            "S3243_3241_bridge",
            ROOT / "3241-Y5-R2FR-public-EH-and-SGK-metric-response-unification-or-residual-vector-under-AX1090.md",
            "EH/SGK divergence bridge for q_loc",
            ["q_loc", "E_res_GK", "metric-response"],
        ),
        (
            "S3243_2977_F1",
            ROOT / "2977-Y5-R2FR-response-doublet-MAB-Zbasis-owner-and-no-linear-source-lock-or-DeltaK-deltaM-row-under-AX1090.md",
            "formal response-doublet F1=0 and owner lock audit",
            ["formal_F1", "M_AB", "J_Z", "B_Z"],
        ),
        (
            "S3243_2978_JZBZ",
            ROOT / "2978-Y5-R2FR-no-linear-source-JZ-BZ-theorem-or-source-bound-rows-under-AX1090.md",
            "no-linear-source theorem attempt for J_Z/B_Z",
            ["J_Z", "B_Z", "fixed-point", "source covector"],
        ),
        (
            "S3243_2979_no_marker",
            ROOT / "2979-Y5-R2FR-no-marker-source-covector-theorem-or-JZ-component-coefficient-acquisition-under-AX1090.md",
            "conditional no-marker source-covector theorem plus countermodel",
            ["source-covector", "countermodel", "J_Z", "claim"],
        ),
        (
            "S3243_2980_constructor",
            ROOT / "2980-Y5-R2FR-parent-constructor-exhaustion-or-first-real-JZ-coefficient-row-under-AX1090.md",
            "parent constructor exhaustion / first J_Z row audit",
            ["constructor", "first real J_Z", "delta_w_e", "claim"],
        ),
        (
            "S3243_2981_action_line",
            ROOT / "2981-Y5-R2FR-single-action-density-line-and-species-blind-measure-or-deltawe-deproxy-under-AX1090.md",
            "single action-density and species-blind measure route",
            ["single action-density", "species-blind measure", "delta_w_e", "J_Z"],
        ),
        (
            "S3243_2990_normal_form",
            ROOT / "2990-Y5-R2FR-sector-normal-form-branch-selection-or-first-epsilon-theta-numeric-source-row-under-AX1090.md",
            "least-scrutiny sector normal form and first theta residual target",
            ["sector normal form", "fixed boundary", "epsilon_Bv", "response doublet"],
        ),
        (
            "S3243_3234_boundary",
            ROOT / "3234-Y5-R2FR-Poynting-boundary-flux-silence-or-finite-bound-under-AX1090.md",
            "recent Poynting/boundary-flux silence checkpoint",
            ["Poynting", "boundary", "finite bound"],
        ),
        (
            "S3243_3238_SGK",
            ROOT / "3238-Y5-R2FR-SGK-metric-response-Helmholtz-gap-or-qLoc-bound-for-local-GR-under-AX1090.md",
            "SGK metric response / Helmholtz gap checkpoint",
            ["SGK", "metric response", "qLoc", "Helmholtz"],
        ),
        (
            "S3243_3240_rollforward",
            ROOT / "3240-Y5-R2FR-PWEP-EH-chain-rollforward-and-current-derivation-frontier-under-AX1090.md",
            "latest roll-forward preventing stale P_WEP loop",
            ["P_WEP", "EH", "unified_gate", "qLoc"],
        ),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, path, role, needles in source_specs:
        rows.append(
            {
                "source_id": source_id,
                "source_path": rel(path),
                "exists": bool_str(path.exists()),
                "parse_ok": bool_str(parse_ok(path)),
                "role": role,
                "evidence_hits": evidence(path, needles),
                "valid_for_claim": "false",
            }
        )
    return rows


def chain_rows() -> list[dict[str, Any]]:
    return [
        {
            "chain_id": "CH3243_0_3242_live_frontier",
            "checkpoint": "3242",
            "result": "Gamma_eff candidate selected as response-doublet density; sigma_GK=+1 locked; epsilon_Gamma_owner made explicit",
            "rollforward_status": "LIVE_INPUT",
            "why_it_matters": "sets the exact density owner problem after the EH/SGK bridge",
            "next_use": "test whether the response-doublet formal zero can be made physical",
        },
        {
            "chain_id": "CH3243_1_2977_formal_zero",
            "checkpoint": "2977",
            "result": "For an exchange-even Gamma_eff=Gamma0+1/2 M_AB Z^A Z^B+O(Z^4), D_Z Gamma_eff|0=0 formally",
            "rollforward_status": "REAL_MATH_WIN_NOT_PHYSICAL_CLAIM",
            "why_it_matters": "this is the clean fixed-point lever; it should not be thrown away",
            "next_use": "separate formal Gamma zero from matter/source/boundary leakage",
        },
        {
            "chain_id": "CH3243_2_2978_JZ_BZ",
            "checkpoint": "2978",
            "result": "Physical obstruction exposed as J_Z plus B_Z, not as an unexplained plateau axiom",
            "rollforward_status": "LIVE_OBSTRUCTION",
            "why_it_matters": "moves the problem into source-current and boundary-work terms that can be derived or bounded",
            "next_use": "write the exact zero theorem for J_Z=B_Z=0",
        },
        {
            "chain_id": "CH3243_3_2979_countermodel",
            "checkpoint": "2979",
            "result": "No-marker source-covector theorem is clean only conditionally; relative source-weight countermodel survives",
            "rollforward_status": "BROAD_ARGUMENT_SPENT",
            "why_it_matters": "prevents claiming that covariance or Hilbert wording alone kills source weights",
            "next_use": "require constructor exhaustion or source-blind action-density proof",
        },
        {
            "chain_id": "CH3243_4_2980_no_constructor_exhaustion",
            "checkpoint": "2980",
            "result": "Parent constructor image not exhausted and no first real J_Z coefficient promoted",
            "rollforward_status": "NARROWS_ROUTE",
            "why_it_matters": "the route must be either a sharper theorem or an explicit finite coefficient row",
            "next_use": "do not repeat broad no-source-slot language",
        },
        {
            "chain_id": "CH3243_5_2981_action_density",
            "checkpoint": "2981",
            "result": "Single action-density/species-blind measure line is the cleanest zero route, but hbar/measure owner is unsigned",
            "rollforward_status": "BEST_THEOREM_ROUTE",
            "why_it_matters": "this is the least-scrutiny way to kill J_Z without a data patch",
            "next_use": "promote it to the owner-lock contract",
        },
        {
            "chain_id": "CH3243_6_2990_normal_form",
            "checkpoint": "2990",
            "result": "Conservative sector normal form selected privately; fixed boundary/reference is first target",
            "rollforward_status": "BEST_PARENT_ACTION_SCAFFOLD",
            "why_it_matters": "B_Z needs the boundary/reference clause, not another abstract source audit",
            "next_use": "tie B_Z=0 to fixed B_ref/no-flux instead of handwaving",
        },
        {
            "chain_id": "CH3243_7_3241_EH_bridge",
            "checkpoint": "3241",
            "result": "q_loc can be rewritten as projected divergence of E_res_GK plus defect terms if Gamma/Khat are one metric-response sector",
            "rollforward_status": "LOCAL_GR_BRIDGE",
            "why_it_matters": "if J_Z/B_Z are killed or bounded, their effect has a precise EH-side residual slot",
            "next_use": "insert the doublet defects into the unified residual vector",
        },
    ]


def derivation_rows() -> list[dict[str, Any]]:
    return [
        {
            "derivation_id": "DRV3243_0_parent_split",
            "statement": "Split the local parent functional near the response fixed point as S_loc=S_EH[g_pub]+S_GK[Gamma_eff,Khat]+S_matter+S_boundary",
            "equation": "Gamma_eff(Z)=Gamma0(q)+1/2 M_AB(q) Z^A Z^B+O(Z^4)",
            "status": "CANDIDATE_NORMAL_FORM",
            "proof_content": "Even response-doublet dependence gives no linear Gamma term if Z is a true exchange-odd vertical coordinate",
            "residual_if_fail": "eps_MAB_owner + eps_Zbasis + eps_odd_Gamma",
            "claim_allowed": "false",
        },
        {
            "derivation_id": "DRV3243_1_formal_F1_zero",
            "statement": "The formal first derivative of Gamma_eff in the response-doublet direction vanishes at Z=0",
            "equation": "F_A^Gamma:=partial Gamma_eff/partial Z^A|_0 = 0",
            "status": "FORMAL_MATH_PASS",
            "proof_content": "Differentiating Gamma0+1/2 M_AB Z^A Z^B+O(Z^4) gives M_AB Z^B+O(Z^3), hence zero at Z=0",
            "residual_if_fail": "eps_odd_Gamma",
            "claim_allowed": "false",
        },
        {
            "derivation_id": "DRV3243_2_physical_first_variation",
            "statement": "The physical first variation is not just F_A^Gamma; it includes matter/source/readout/boundary work",
            "equation": "F_A^phys = F_A^Gamma + J_A + B_A + R_A^meas + R_A^theta + R_A^proj",
            "status": "PHYSICAL_GATE",
            "proof_content": "Vary the full functional, not only the quadratic Gamma block; every non-descended source or boundary piece contributes a covector",
            "residual_if_fail": "eps_JZ + eps_BZ + eps_measure + eps_theta + eps_projector",
            "claim_allowed": "false",
        },
        {
            "derivation_id": "DRV3243_3_descent_zero",
            "statement": "If matter, measure, constants, connection/coframe and readout descend through q, and Z is vertical, their bulk Z-current vanishes",
            "equation": "S_matter=Sbar_matter[q(Phi),Psi,theta], Dq[e_A]=0 => J_A=delta S_matter[e_A]|_0=0",
            "status": "EXACT_CONDITIONAL_THEOREM",
            "proof_content": "Chain rule gives delta Sbar/dq times Dq[e_A]; verticality kills the term, provided no source-label or representative coefficient re-enters",
            "residual_if_fail": "eps_q_descent + eps_source_slot + eps_measure + eps_theta",
            "claim_allowed": "false",
        },
        {
            "derivation_id": "DRV3243_4_boundary_zero",
            "statement": "Boundary work vanishes only with a fixed exact/reference boundary convention plus no-flux/compact-support condition",
            "equation": "B_A:=delta(B_ref+surface terms)[e_A]|_0 = integral_boundary Theta_A = 0",
            "status": "EXACT_CONDITIONAL_THEOREM",
            "proof_content": "A fixed reference term cancels pure improvements; physical edge flux must vanish or be bounded on the chosen local worldtube",
            "residual_if_fail": "eps_Bv_ambiguity + eps_Poynting_boundary + eps_worldtube",
            "claim_allowed": "false",
        },
        {
            "derivation_id": "DRV3243_5_amplitude_law",
            "statement": "If the source covector is finite rather than zero, the response amplitude is controlled by the inverse Hessian",
            "equation": "Z_*^A=(M^{-1})^{AB} J_B^tot + O(|J|^2), Delta Gamma_min=-1/2 J_A^tot(M^{-1})^{AB}J_B^tot+O(|J|^3)",
            "status": "DERIVED_LOCAL_BOUND_FORM",
            "proof_content": "Minimize 1/2 M_AB Z^A Z^B - J_A^tot Z^A for positive M; this turns failure of exact zero into a boundable coupling residual",
            "residual_if_fail": "eps_M_inverse + eps_Jtot_numeric",
            "claim_allowed": "false",
        },
        {
            "derivation_id": "DRV3243_6_qLoc_insertion",
            "statement": "The response-doublet defects enter the EH/SGK bridge as an explicit contribution to epsilon_Gamma_owner",
            "equation": "q_loc^nu=-(1/kappa_*)P_loc nabla_mu E_res_GK^{mu nu}+P_loc nabla^nu(eps_Gamma_owner)+... ",
            "status": "UNIFIED_RESIDUAL_INSERTION",
            "proof_content": "3241 already supplies the divergence bridge; 3243 identifies which doublet-source defects feed the Gamma-owner slot",
            "residual_if_fail": "eps_Gamma_owner_total",
            "claim_allowed": "false",
        },
    ]


def owner_lock_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "OL3243_0_Z_basis",
            "required_clause": "Z^A is a parent-owned exchange-odd vertical coordinate",
            "zero_condition": "Dq[e_A]=0 and exchange involution fixes Z=0",
            "current_status": "CONDITIONAL_NOT_PARENT_SIGNED",
            "if_unsigned": "eps_Zbasis + eps_q_descent",
            "claim_gate": "false",
        },
        {
            "gate_id": "OL3243_1_MAB",
            "required_clause": "M_AB is parent-owned, symmetric and positive/coercive on the local branch",
            "zero_condition": "M_AB=M_BA, M>=m0>0, same branch as q and Gamma_eff",
            "current_status": "CONDITIONAL_NOT_PARENT_SIGNED",
            "if_unsigned": "eps_MAB_domain + eps_M_inverse",
            "claim_gate": "false",
        },
        {
            "gate_id": "OL3243_2_Gamma_even",
            "required_clause": "Gamma_eff has no odd/linear Z term",
            "zero_condition": "Gamma_eff(Gamma,Z)=Gamma_eff(Gamma,-Z) through O(Z^3) or exact symmetry",
            "current_status": "FORMAL_ROUTE_AVAILABLE",
            "if_unsigned": "eps_odd_Gamma",
            "claim_gate": "false",
        },
        {
            "gate_id": "OL3243_3_matter_descent",
            "required_clause": "ordinary matter action descends through q with no direct Z/source-label slot",
            "zero_condition": "S_matter=Sbar[q(Phi),Psi,theta]",
            "current_status": "BEST_ZERO_ROUTE_NOT_SIGNED",
            "if_unsigned": "eps_JZ",
            "claim_gate": "false",
        },
        {
            "gate_id": "OL3243_4_species_blind_measure",
            "required_clause": "measure, hbar/path weight, coframe and Jacobian are species-blind and q-owned",
            "zero_condition": "D_Z log(mu_parent)=0 and one hbar_parent/action density line",
            "current_status": "2981_CONDITIONAL_NOT_PARENT_DERIVED",
            "if_unsigned": "eps_measure + delta_w_A",
            "claim_gate": "false",
        },
        {
            "gate_id": "OL3243_5_constants_couplings",
            "required_clause": "dimensionless constants and EM/clock/mass couplings do not carry independent Z/source markers",
            "zero_condition": "D_Z theta=0 or theta is fixed/topological on the same branch",
            "current_status": "UNSIGNED_MARKER_CLAUSE",
            "if_unsigned": "eps_theta + eps_constants_em",
            "claim_gate": "false",
        },
        {
            "gate_id": "OL3243_6_readout_projector",
            "required_clause": "local projector/readout/domain cannot reintroduce source labels after q",
            "zero_condition": "delta_Z Pi_loc=0 or its contribution is a sourced finite bound",
            "current_status": "UNSIGNED_PROJECTOR_CLAUSE",
            "if_unsigned": "eps_projector + eps_worldtube",
            "claim_gate": "false",
        },
        {
            "gate_id": "OL3243_7_boundary_reference",
            "required_clause": "fixed B_ref/no-flux boundary convention kills edge work",
            "zero_condition": "delta_Z B_ref + integral_boundary Theta_Z = 0",
            "current_status": "2990_FIRST_PROOF_TARGET_NOT_SIGNED",
            "if_unsigned": "eps_BZ + epsilon_Bv_ambiguity",
            "claim_gate": "false",
        },
        {
            "gate_id": "OL3243_8_metric_response",
            "required_clause": "K_hat is the Hilbert metric response of the same Gamma_eff density sector",
            "zero_condition": "K_hat=K_metric and Helmholtz/integrability conditions close",
            "current_status": "3241_3242_UNIFIED_BUT_NOT_PARENT_OWNED",
            "if_unsigned": "DeltaK_deltaM + DeltaK_deltaZ + eps_Helmholtz",
            "claim_gate": "false",
        },
        {
            "gate_id": "OL3243_9_same_branch",
            "required_clause": "all zero clauses hold in one local branch, not stitched across unrelated branches",
            "zero_condition": "same q, Z basis, matter action, boundary convention, projection and units",
            "current_status": "GLOBAL_BRANCH_LOCK_OPEN",
            "if_unsigned": "eps_branch_mismatch",
            "claim_gate": "false",
        },
    ]


def residual_rows() -> list[dict[str, Any]]:
    return [
        {
            "residual_id": "RES3243_0_definition",
            "symbol": "epsilon_Gamma_owner_total",
            "definition": "absolute response-doublet owner residual feeding the Gamma_eff density slot",
            "bound_interface": "eps_Gamma_owner_total <= eps_Zbasis + eps_MAB_domain + eps_odd_Gamma + eps_JZ + eps_BZ + eps_measure + eps_theta + eps_projector + eps_DeltaK",
            "current_value": "MISSING_NUMERIC_PARENT_INPUTS",
            "status": "SOURCE_READY_NONCLAIM",
            "valid_for_claim": "false",
        },
        {
            "residual_id": "RES3243_1_Jtot",
            "symbol": "J_A^tot",
            "definition": "total physical source covector in the response-doublet direction",
            "bound_interface": "J_A^tot=J_A^matter+J_A^measure+J_A^theta+J_A^projector+B_A+odd_Gamma_A",
            "current_value": "MISSING_THEOREM_ZERO_OR_COMPONENT_VALUES",
            "status": "LIVE_COUPLING_FRONTIER",
            "valid_for_claim": "false",
        },
        {
            "residual_id": "RES3243_2_amplitude",
            "symbol": "||Z_*||_M",
            "definition": "local response amplitude induced by finite source leakage",
            "bound_interface": "||Z_*||_M <= ||J_tot||_{M^{-1}} + O(||J_tot||^2)",
            "current_value": "MISSING_MAB_AND_JTOT_NUMERIC_SOURCE",
            "status": "DERIVED_BOUND_FORM_NONCLAIM",
            "valid_for_claim": "false",
        },
        {
            "residual_id": "RES3243_3_energy_shift",
            "symbol": "Delta Gamma_min",
            "definition": "minimum Gamma density shift produced by finite source leakage",
            "bound_interface": "|Delta Gamma_min| <= 1/2 ||J_tot||_{M^{-1}}^2 + higher_order",
            "current_value": "MISSING_MAB_AND_JTOT_NUMERIC_SOURCE",
            "status": "DERIVED_BOUND_FORM_NONCLAIM",
            "valid_for_claim": "false",
        },
        {
            "residual_id": "RES3243_4_qLoc",
            "symbol": "q_loc^nu response residual",
            "definition": "projected local-GR current sourced by imperfect response-doublet owner lock",
            "bound_interface": "||q_loc||_arena <= C_arena(||nabla E_res_GK|| + ||nabla epsilon_Gamma_owner_total|| + ||DeltaK||)",
            "current_value": "MISSING_ARENA_CONSTANTS_AND_PARENT_INPUTS",
            "status": "LOCAL_GR_GATE_NONCLAIM",
            "valid_for_claim": "false",
        },
    ]


def gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "claim_gate_id": "CG3243_0_formal_F1",
            "claim": "formal response-doublet F1=0",
            "condition_passed": "true",
            "status": "math lemma survives",
            "claim_allowed": "false",
        },
        {
            "claim_gate_id": "CG3243_1_physical_F1",
            "claim": "physical full first variation F_A^phys=0",
            "condition_passed": "false",
            "status": "J_Z/B_Z/measure/theta/projector clauses not parent-signed",
            "claim_allowed": "false",
        },
        {
            "claim_gate_id": "CG3243_2_response_amplitude",
            "claim": "response amplitude Delta m or Z_* is finite and local-safe",
            "condition_passed": "false",
            "status": "bound law derived but M_AB and J_tot numeric/source rows missing",
            "claim_allowed": "false",
        },
        {
            "claim_gate_id": "CG3243_3_EH_SGK",
            "claim": "EH/SGK residual bridge closes local q_loc suppression",
            "condition_passed": "false",
            "status": "Gamma owner and K_metric equality not parent-owned",
            "claim_allowed": "false",
        },
        {
            "claim_gate_id": "CG3243_4_local_GR_Newton",
            "claim": "local GR/Newton reduction",
            "condition_passed": "false",
            "status": "requires physical F1 zero or finite residual below PPN/Newton arenas",
            "claim_allowed": "false",
        },
        {
            "claim_gate_id": "CG3243_5_empirical",
            "claim": "R10/WEP/PPN/clock/orbital/local-GR empirical pass",
            "condition_passed": "false",
            "status": "no claim-grade owner lock or finite residual rows",
            "claim_allowed": "false",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3243_0_keep_doublet",
            "decision": "Keep the response-doublet route alive.",
            "because": "It gives a real formal fixed-point theorem: D_Z Gamma_eff|0=0.",
            "next_action": "Do not demote it merely because physical source terms remain open.",
        },
        {
            "decision_id": "DEC3243_1_no_smuggling",
            "decision": "Do not claim physical local-GR suppression from the formal Gamma zero alone.",
            "because": "The full first variation contains J_Z, B_Z, measure, constants and projector terms.",
            "next_action": "Treat those as exact zero clauses or finite source-ready residual rows.",
        },
        {
            "decision_id": "DEC3243_2_best_route",
            "decision": "Attack the single parent action-density plus fixed-boundary proof next.",
            "because": "2979-2981 show broad no-marker language is too weak, while 2990 identifies boundary/reference as the first normal-form proof target.",
            "next_action": "Try to prove J_Z=B_Z=0 in one branch; if it fails, write finite J_tot and epsilon_Gamma_owner rows.",
        },
        {
            "decision_id": "DEC3243_3_amplitude_fallback",
            "decision": "If zero fails, use the derived amplitude law rather than closure prose.",
            "because": "Z_*=(M^{-1})J_tot turns the coupling problem into a bounded residual problem.",
            "next_action": "Source or derive M_AB coercivity and J_tot component bounds.",
        },
    ]


def next_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT3243_0_3244",
            "priority": "selected_primary",
            "next_doc": "3244-Y5-R2FR-single-parent-density-boundary-reference-proof-or-finite-Jtot-bound-under-AX1090.md",
            "next_script": "scripts/Y5_R2FR_3244_single_parent_density_boundary_reference_or_finite_Jtot_bound.py",
            "objective": "Try the one-branch proof that q-only matter descent plus species-blind measure plus fixed B_ref/no-flux gives J_Z=B_Z=0; if not, promote J_tot into explicit finite residual rows.",
            "exclude": "do not repeat broad no-marker/source-covector theorem; do not claim from formal F1=0 alone; do not edit formalization-workbench",
            "claim_policy": "private nonclaim until every owner-lock clause is parent-signed or numerically bounded",
            "valid_for_claim": "false",
        }
    ]


def validation_rows(source_rows: list[dict[str, Any]], generated_csvs: list[Path]) -> list[dict[str, Any]]:
    source_paths_exist = all(row["exists"] == "true" for row in source_rows)
    source_hits_found = all(row["evidence_hits"] not in {"MISSING_SOURCE", "NO_MATCH"} for row in source_rows)
    csvs_parse = all(csv_ok(path) for path in generated_csvs)
    outputs_under_post = all(ROOT in path.parents or path == DOC for path in [*generated_csvs, DOC])
    formalization_outputs = any(FW in path.parents for path in [*generated_csvs, DOC])
    formalization_3243_docs = list(FW.rglob("*3243*")) if FW.exists() else []
    formalization_clean = not formalization_outputs and not formalization_3243_docs

    gates = gate_rows()
    formal_only_claim_blocked = any(
        row["claim_gate_id"] == "CG3243_0_formal_F1"
        and row["condition_passed"] == "true"
        and row["claim_allowed"] == "false"
        for row in gates
    )
    physics_claims_blocked = all(
        row["claim_allowed"] == "false"
        for row in gates
        if row["claim_gate_id"] != "CG3243_0_formal_F1"
    )
    residual_nonclaim = all(row["valid_for_claim"] == "false" for row in residual_rows())
    owner_lock_open = all(row["claim_gate"] == "false" for row in owner_lock_rows())

    checks = [
        ("VAL3243_0_sources_exist", source_paths_exist, "all cited local source paths exist", str(source_paths_exist)),
        ("VAL3243_1_source_hits", source_hits_found, "every cited source has matching evidence hits", str(source_hits_found)),
        ("VAL3243_2_csvs_parse", csvs_parse, "all generated CSV files parse", str(csvs_parse)),
        ("VAL3243_3_outputs_under_post_checkpoint", outputs_under_post, "all generated outputs are under post-checkpoint-work", str(outputs_under_post)),
        ("VAL3243_4_formalization_clean", formalization_clean, "no 3243 outputs were written to formalization-workbench", f"formalization_3243_count={len(formalization_3243_docs)}"),
        ("VAL3243_5_formal_math_not_physics_claim", formal_only_claim_blocked, "formal F1 zero is recorded but not promoted to a physics claim", str(formal_only_claim_blocked)),
        ("VAL3243_6_physics_claims_blocked", physics_claims_blocked, "local-GR/Newton/empirical claims remain blocked", str(physics_claims_blocked)),
        ("VAL3243_7_owner_lock_open", owner_lock_open, "every owner-lock clause remains nonclaim until parent-signed", str(owner_lock_open)),
        ("VAL3243_8_residual_nonclaim", residual_nonclaim, "residual/amplitude rows are source-ready but nonclaim", str(residual_nonclaim)),
        ("VAL3243_9_next_written", bool(next_rows()), "3244 next target written", str(bool(next_rows()))),
        ("VAL3243_10_doc_written", DOC.exists(), "3243 markdown checkpoint exists", str(DOC.exists())),
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
            "validation_id": "VAL3243_OVERALL",
            "passed": bool_str(all(row["passed"] == "true" for row in rows)),
            "requirement": "3243 validation overall",
            "evidence": "all required validation rows passed",
        }
    )
    return rows


def build_doc(
    source_rows: list[dict[str, Any]],
    chain: list[dict[str, Any]],
    derivation: list[dict[str, Any]],
    owner_lock: list[dict[str, Any]],
    residual: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> str:
    return "\n\n".join(
        [
            "# 3243 - Response-Doublet Owner Lock and Physical Source Gate under AX1090",
            f"Generated: `{RUN_UTC}`",
            (
                "Status: `Y5_R2FR_3243_formal_response_doublet_F1_zero_preserved_physical_JZ_BZ_gate_derived_"
                "amplitude_law_written_nonclaim`"
            ),
            (
                "Claim ceiling: `formal_F1_zero_only_no_physical_F1_zero_no_Gamma_owner_claim_no_q_loc_zero_"
                "no_local_GR_no_Newton_no_R10_no_PPN_no_empirical_claim`"
            ),
            "## Summary",
            (
                "- `3243` keeps the useful bit alive: the response-doublet density gives a real formal fixed-point result, "
                "`D_Z Gamma_eff|_0=0`, when `Gamma_eff=Gamma0+1/2 M_AB Z^A Z^B+O(Z^4)`."
            ),
            (
                "- It also sharpens why that is not yet local GR: the physical first variation is "
                "`F_A^phys=F_A^Gamma+J_A+B_A+R_A^measure+R_A^theta+R_A^projector`, so the formal zero does not kill source-current or boundary work."
            ),
            (
                "- The exact route is now a one-branch owner-lock theorem: parent-owned vertical `Z`, positive `M_AB`, q-only matter descent, "
                "species-blind measure, fixed constants/couplings, projector silence, fixed boundary/no-flux, and same metric-response sector."
            ),
            (
                "- If any zero clause fails, the work does not collapse; it becomes a bound problem with "
                "`Z_*^A=(M^{-1})^{AB}J_B^tot+O(|J|^2)` and `|Delta Gamma_min| <= 1/2 ||J_tot||_{M^{-1}}^2+...`."
            ),
            (
                "- This is the non-loop move: broad no-marker language was already spent in `2979`/`2980`; the next proof must attack the single parent density "
                "and fixed boundary/reference clauses directly."
            ),
            "## Rollforward Chain",
            md_table(
                chain,
                ["chain_id", "checkpoint", "result", "rollforward_status", "why_it_matters", "next_use"],
            ),
            "## Fixed-Point and Amplitude Derivation",
            md_table(
                derivation,
                ["derivation_id", "statement", "equation", "status", "proof_content", "residual_if_fail", "claim_allowed"],
            ),
            "## Physical Owner-Lock Gate",
            md_table(
                owner_lock,
                ["gate_id", "required_clause", "zero_condition", "current_status", "if_unsigned", "claim_gate"],
            ),
            "## Unified Residual Update",
            md_table(
                residual,
                ["residual_id", "symbol", "definition", "bound_interface", "current_value", "status", "valid_for_claim"],
            ),
            "## Claim Gates",
            md_table(gates, ["claim_gate_id", "claim", "condition_passed", "status", "claim_allowed"]),
            "## Decision Ledger",
            md_table(decisions, ["decision_id", "decision", "because", "next_action"]),
            "## Next Target",
            md_table(
                next_target,
                ["next_id", "priority", "next_doc", "next_script", "objective", "exclude", "claim_policy", "valid_for_claim"],
            ),
            "## Source Register",
            md_table(
                source_rows,
                ["source_id", "source_path", "exists", "parse_ok", "role", "evidence_hits", "valid_for_claim"],
            ),
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
    chain = chain_rows()
    derivation = derivation_rows()
    owner_lock = owner_lock_rows()
    residual = residual_rows()
    gates = gate_rows()
    decisions = decision_rows()
    next_target = next_rows()

    write_csv(OUTPUTS["sources"], source_rows)
    write_csv(OUTPUTS["chain"], chain)
    write_csv(OUTPUTS["derivation"], derivation)
    write_csv(OUTPUTS["owner_lock"], owner_lock)
    write_csv(OUTPUTS["residual"], residual)
    write_csv(OUTPUTS["claim_gates"], gates)
    write_csv(OUTPUTS["decision"], decisions)
    write_csv(OUTPUTS["next"], next_target)

    if PYCACHE.exists():
        shutil.rmtree(PYCACHE)

    generated_csvs = [
        OUTPUTS["sources"],
        OUTPUTS["chain"],
        OUTPUTS["derivation"],
        OUTPUTS["owner_lock"],
        OUTPUTS["residual"],
        OUTPUTS["claim_gates"],
        OUTPUTS["decision"],
        OUTPUTS["next"],
    ]
    validation = validation_rows(source_rows, generated_csvs)
    write_csv(OUTPUTS["validation"], validation)
    DOC.write_text(
        build_doc(source_rows, chain, derivation, owner_lock, residual, gates, decisions, next_target, validation),
        encoding="utf-8",
    )
    validation = validation_rows(source_rows, generated_csvs)
    write_csv(OUTPUTS["validation"], validation)
    DOC.write_text(
        build_doc(source_rows, chain, derivation, owner_lock, residual, gates, decisions, next_target, validation),
        encoding="utf-8",
    )

    if PYCACHE.exists():
        shutil.rmtree(PYCACHE)

    failed = [row for row in validation if row["passed"] != "true"]
    if failed:
        raise SystemExit(f"3243 validation failed: {failed}")


if __name__ == "__main__":
    main()
