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
DOC = ROOT / "3361-Y5-R2FR-odd-residual-parentization-and-physical-lock-under-AX1090.md"
RUN_UTC = datetime.now(timezone.utc).isoformat()

LOCAL_SOURCES = [
    ("LSRC3361_0_3360_doc", ROOT / "3360-Y5-R2FR-Yloc-Euler-equations-or-R11-coefficient-bound-under-AX1090.md", "3360 handoff"),
    ("LSRC3361_1_3360_next", OUT / "P8_Y5_R2FR_3360_NEXT_TARGET.csv", "3360 next target"),
    ("LSRC3361_2_3360_euler", OUT / "P8_Y5_R2FR_3360_YLOC_EULER_ZERO_PACKET.csv", "positive Euler theorem packet"),
    ("LSRC3361_3_3360_component", OUT / "P8_Y5_R2FR_3360_YLOC_COMPONENT_CLOSURE_AUDIT.csv", "Yloc component closure audit"),
    ("LSRC3361_4_3360_gates", OUT / "P8_Y5_R2FR_3360_PROMOTION_GATES.csv", "3360 promotion gates"),
    ("LSRC3361_5_odd_exchange", OUT / "P8_ODD_RESIDUAL_EXCHANGE_THEOREM.csv", "old odd residual exchange theorem"),
    ("LSRC3361_6_odd_candidates", OUT / "P8_ODD_RESIDUAL_PARENTIZATION_CANDIDATES.csv", "old odd parentization candidates"),
    ("LSRC3361_7_odd_counterexamples", OUT / "P8_ODD_RESIDUAL_COUNTEREXAMPLES.csv", "old odd residual counterexamples"),
    ("LSRC3361_8_no_linear_contract", OUT / "P8_YLOC_NO_LINEAR_SOURCE_PARENT_CONTRACT.csv", "old no-linear-source parent contract"),
    ("LSRC3361_9_aux_component", OUT / "P8_YLOC_AUX_PARENT_COMPONENT_RESULT.csv", "old auxiliary component result"),
    ("LSRC3361_10_physical_owner_gate", OUT / "P8_Y5_R2FR_3243_PHYSICAL_OWNER_LOCK_GATE.csv", "physical owner lock gate"),
    ("LSRC3361_11_z_basis_lock", OUT / "P8_Y5_R2FR_2973_Z_BASIS_PHYSICAL_LOCK_ATTEMPT.csv", "Z-basis physical lock attempt"),
    ("LSRC3361_12_source_owner", OUT / "P8_Y5_SOURCE_NORMALIZATION_OWNER_THEOREM.csv", "Y5 source normalization owner theorem"),
    ("LSRC3361_13_source_stack", OUT / "P8_SOURCE_NORMALIZATION_THEOREM_STACK.csv", "source normalization theorem stack"),
    ("LSRC3361_14_r11_source_norm", OUT / "P8_R11_SOURCE_NORMALIZATION_OPERATOR_MINIMUM_FILL.csv", "R11 source normalization operator rows"),
    ("LSRC3361_15_min_source_readout", OUT / "P8_Y5_R2FR_3037_MINIMUM_SOURCE_READOUT_LOCK_PARENT_CLAUSE.csv", "minimum source-readout parent clause"),
    ("LSRC3361_16_current_gauge_lock", OUT / "P8_Y5_R2FR_3274_CURRENT_NORMALIZATION_GAUGE_LOCK_LEMMA.csv", "current normalization gauge lock lemma"),
    ("LSRC3361_17_ppn_vector", OUT / "P8_Y5_R2FR_3110_LOCAL_PPN_RESIDUAL_VECTOR.csv", "local PPN residual vector"),
    ("LSRC3361_18_newton_maxwell_vector", OUT / "P8_Y5_R2FR_3294_PPN_NEWTON_MAXWELL_RESIDUAL_VECTOR.csv", "Newton/PPN/Maxwell residual vector"),
    ("LSRC3361_19_3357_scope", OUT / "P8_Y5_R2FR_3357_CLAIM_SCOPE_SEPARATION.csv", "AX1090 source-side theorem scope"),
    ("LSRC3361_20_3358_surface", OUT / "P8_Y5_R2FR_3358_EPSILON_SURFACE_SOURCE_UPDATE.csv", "surface/source residual update"),
]

OUTPUTS = {
    "local_sources": OUT / "P8_Y5_R2FR_3361_LOCAL_SOURCE_REGISTER.csv",
    "theorem_packet": OUT / "P8_Y5_R2FR_3361_ODD_PARENTIZATION_THEOREM_PACKET.csv",
    "lock_gate": OUT / "P8_Y5_R2FR_3361_PHYSICAL_LOCK_JACOBIAN_GATE.csv",
    "component_result": OUT / "P8_Y5_R2FR_3361_COMPONENT_LOCK_RESULT.csv",
    "y5_obstruction": OUT / "P8_Y5_R2FR_3361_Y5_ZERO_MODE_OBSTRUCTION.csv",
    "gates": OUT / "P8_Y5_R2FR_3361_PROMOTION_GATES.csv",
    "decision": OUT / "P8_Y5_R2FR_3361_DECISION_LEDGER.csv",
    "next": OUT / "P8_Y5_R2FR_3361_NEXT_TARGET.csv",
    "validation": OUT / "P8_Y5_BRR545_3361_VALIDATION.csv",
}


def bool_str(value: bool) -> str:
    return "true" if value else "false"


def compact(value: Any, limit: int = 1800) -> str:
    text = " ".join(str(value).split())
    return text if len(text) <= limit else text[: limit - 3] + "..."


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: compact(row.get(key, "")) for key in fieldnames})


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def parseable(path: Path) -> bool:
    try:
        if path.suffix.lower() == ".csv":
            read_csv(path)
        else:
            path.read_text(encoding="utf-8")
        return True
    except Exception:
        return False


def table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "_No rows._\n"
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
        lines.append("| " + " | ".join(compact(row.get(key, ""), 260).replace("|", "\\|") for key in headers) + " |")
    return "\n".join(lines) + "\n"


def local_source_rows() -> list[dict[str, Any]]:
    return [
        {
            "source_id": source_id,
            "path": str(path),
            "exists": bool_str(path.exists()),
            "parseable": bool_str(path.exists() and parseable(path)),
            "usage": usage,
            "valid_for_claim": "false",
        }
        for source_id, path, usage in LOCAL_SOURCES
    ]


def theorem_packet_rows() -> list[dict[str, Any]]:
    return [
        {
            "theorem_id": "T3361_0_physical_lock_theorem",
            "statement": "If the physical residual vector R_phys is exactly represented by the parent odd variables Y through full-rank linear order plus higher powers that vanish at Y=0, then Y=0 implies all locked local residuals vanish.",
            "math_form": "R_phys^I = A^I_A Y^A + O(|Y|^2), R_phys(0)=0, rank(A)=dim(R_phys) on the scored subspace",
            "proof_status": "EXACT_CONDITIONAL_LOCK_THEOREM",
            "proof_sketch": "Substitute Y=0 into the map. The constant term is zero and every higher-order term contains at least one Y. Full rank is not needed for implication, but is needed for inverse residual bounds and for preventing hidden physical null directions.",
            "surviving_gap": "current corpus lacks a parent-signed full-rank component map from q_loc/PPN/R11/Y5/Y6 to Y variables",
            "valid_for_claim": "false",
        },
        {
            "theorem_id": "T3361_1_odd_parentization_zero_theorem",
            "statement": "An exchange involution can forbid local linear source currents only when the dangerous residuals are genuine parent odd variables and the observed matter/readout stack is exchange-even.",
            "math_form": "I:Y->-Y, I:q=e_obs=tau=theta, S_parent[I(Phi)]=S_parent[Phi], S_matter=S_matter[q(Phi),Psi,theta]",
            "proof_status": "EXACT_CONDITIONAL_NO_LINEAR_SOURCE_THEOREM",
            "proof_sketch": "The first variation at Y=0 has odd parity. An invariant scalar action and exchange-even matter functional cannot contain a term J_A Y^A. With positive Hessian and zero odd boundary charge, the 3360 Euler theorem gives Y=0.",
            "surviving_gap": "the MTS corpus has candidate exchange-doublet rows but not a parent action proving matter neutrality and boundary odd-charge silence for all components",
            "valid_for_claim": "false",
        },
        {
            "theorem_id": "T3361_2_bookkeeping_auxiliary_no_go",
            "statement": "Odd auxiliary variables alone do not prove local GR unless they are physically locked to the actual residuals.",
            "math_form": "S_aux=1/2 m_A^2 y_A^2 gives y=0, but R_phys=y+C or R_phys=s_even^2 remains nonzero",
            "proof_status": "EXACT_NO_GO_ODD_ONLY",
            "proof_sketch": "A positive even auxiliary sector can be minimized without touching an independent or exchange-even physical residual. Therefore zeroing a bookkeeping y-field is not enough to zero q_loc, PPN, R11, or measured-GM residuals.",
            "surviving_gap": "forces 3361 to reject pure auxiliary parity as a GR derivation",
            "valid_for_claim": "false",
        },
        {
            "theorem_id": "T3361_3_Y5_zero_mode_obstruction",
            "statement": "Source normalization is not killed by odd residual symmetry by itself because the measured-GM offset can be an exchange-even constant or Gauss-flux zero mode.",
            "math_form": "mu_obs = G_ref M_H (1+epsilon_mu); I(epsilon_mu)=epsilon_mu is allowed, so I-symmetry does not force epsilon_mu=0",
            "proof_status": "EXACT_CONDITIONAL_Y5_ODD_ROUTE_REJECTION",
            "proof_sketch": "The parity theorem only removes odd linear loads. A universal scalar normalization offset is invariant under the exchange and can shift the orbital Gauss coefficient while all odd Y variables vanish. A local positive operator also misses constant/boundary flux modes unless a charge/reference theorem owns them.",
            "surviving_gap": "Y5 must be closed by a source-current/charge-normalization theorem or bounded as an explicit source-normalization operator",
            "valid_for_claim": "false",
        },
        {
            "theorem_id": "T3361_4_coupling_current_lock_route",
            "statement": "The promising route for Y5 is not generic odd parity but a coupling/current lock: gauge or Noether current ownership can force local coupling normalization to be constant, while a parent reference charge fixes the remaining absolute constant.",
            "math_form": "nabla_mu(kappa_J J^mu)=0 and nabla_mu J^mu=0 imply J^mu nabla_mu ln(kappa_J)=0; current richness => nabla_mu kappa_J=0",
            "proof_status": "VALID_CONDITIONAL_ROUTE_NOT_PARENT_SIGNED",
            "proof_sketch": "This imports the exact current-normalization lemma: variable coupling requires either zero gradient along all allowed currents or an extra compensating current. Excluding compensators and proving current richness turns source normalization into a conservation/gauge problem rather than a fitted plateau.",
            "surviving_gap": "No parent-owned current-richness theorem, no compensator exclusion, and no G_ref reference-charge owner are currently signed",
            "valid_for_claim": "false",
        },
    ]


def physical_lock_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "PLOCK3361_0_residual_vector_defined",
            "required_condition": "Define the scored physical residual vector before fitting or calibration.",
            "math_form": "R_phys={q_loc, DeltaGM_source, DeltaPPN_A, epsilon_R11_A, boundary_flux, T_extra}",
            "current_result": "DEFINED_AS_REQUIRED_INTERFACE",
            "missing": "parent-signed map to actual field variables",
            "passed": "true",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "PLOCK3361_1_parent_odd_coordinates",
            "required_condition": "Each residual component has a parent-owned odd coordinate or is explicitly excluded/topological/bounded.",
            "math_form": "I:Y^A->-Y^A and Dq[Y^A]=0 on one branch",
            "current_result": "PARTIAL_CANDIDATES_ONLY",
            "missing": "q_loc, Y5, Y6, PPN, and R11 are not all parent-owned odd variables",
            "passed": "false",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "PLOCK3361_2_no_even_leakage",
            "required_condition": "No exchange-even or independent term contributes to the physical residual at Y=0.",
            "math_form": "R_phys(Y,E_even)=A Y + O(Y^2), with E_even branch fixed to zero/topological/bounded",
            "current_result": "FAILED_FOR_Y5_AND_Y6",
            "missing": "source-normalization zero mode and conserved extra stress can be exchange-even",
            "passed": "false",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "PLOCK3361_3_full_rank_jacobian",
            "required_condition": "The component Jacobian from Y variables to scored residuals has no unowned physical null directions.",
            "math_form": "rank(partial R_phys^I/partial Y^A)|_0 = dim(scored residual subspace)",
            "current_result": "NOT_PROVED",
            "missing": "Z-basis lock rows are conditional and full-rank component gate remains unsigned",
            "passed": "false",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "PLOCK3361_4_same_readout_branch",
            "required_condition": "The same q, coframe, projector, source current, boundary convention, and unit normalization are used in the Euler theorem and the observable residual.",
            "math_form": "branch(Y_euler)=branch(R_phys)=branch(readout/PPN/R11/source)",
            "current_result": "NOT_PROVED",
            "missing": "same-branch lock remains a parent-action adoption problem",
            "passed": "false",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "PLOCK3361_5_source_boundary_silence",
            "required_condition": "Odd boundary charge and source currents vanish for the same residual components.",
            "math_form": "J_A=0 and B_A=0 for locked components",
            "current_result": "NOT_PROVED_FOR_Y2_TO_Y6",
            "missing": "boundary, source normalization, and extra stress rows remain open",
            "passed": "false",
            "valid_for_claim": "false",
        },
    ]


def component_result_rows() -> list[dict[str, Any]]:
    return [
        {
            "component_id": "C3361_0_q_loc",
            "physical_residual": "q_loc^nu = P_loc(nabla^nu Gamma_eff - nabla_mu K_hat^{mu nu})",
            "odd_parentization_result": "CONDITIONAL_BEST_ROUTE",
            "lock_result": "not_locked",
            "new_information": "q_loc can be an odd residual only if Gamma_eff/K_hat/P_loc are parent-owned and the projector is exchange-even; otherwise q_loc remains a derived diagnostic.",
            "best_next_action": "use q_loc as a component in the physical lock map, but do not claim zero until action existence and projector ownership close",
            "valid_for_claim": "false",
        },
        {
            "component_id": "C3361_1_Y0_trace_expansion",
            "physical_residual": "X_D / trace scalar local response",
            "odd_parentization_result": "PARTIAL",
            "lock_result": "not_locked",
            "new_information": "scalar odd parity can remove linear source only after matter trace is exchange-even and no scalar calibration channel is left.",
            "best_next_action": "bind trace scalar to the public metric response or score as scalar-tensor/R2 residual",
            "valid_for_claim": "false",
        },
        {
            "component_id": "C3361_2_Y1_coherent_projector",
            "physical_residual": "Qcoh_D - h X_D/3",
            "odd_parentization_result": "PARTIAL",
            "lock_result": "not_locked",
            "new_information": "projector residual must be a parent branch variable; declaring projector stress odd does not stop exchange-even projector stress.",
            "best_next_action": "derive projector ownership or retain projector/domain stress R11 row",
            "valid_for_claim": "false",
        },
        {
            "component_id": "C3361_3_Y2_boundary_flux",
            "physical_residual": "Phi_boundary^i / collar flux",
            "odd_parentization_result": "IMPROVED_BY_3355_3358_BUT_NOT_ZERO",
            "lock_result": "not_locked",
            "new_information": "local collar silence removes pointwise bulk contact, but a boundary odd charge can still survive as a surface/Gauss flux.",
            "best_next_action": "prove no odd boundary charge for the same branch or build surface multipole bounds",
            "valid_for_claim": "false",
        },
        {
            "component_id": "C3361_4_Y3_domain_vector",
            "physical_residual": "V_domain^i / preferred-frame vector",
            "odd_parentization_result": "CONDITIONAL",
            "lock_result": "not_locked",
            "new_information": "exchange doublet is plausible for vector domain residuals, but domain selector and preferred-frame readout are not parent-derived.",
            "best_next_action": "derive no-vector domain theorem or retain alpha1/alpha2/alpha3 products",
            "valid_for_claim": "false",
        },
        {
            "component_id": "C3361_5_Y4_domain_STF_stress",
            "physical_residual": "S_TF_domain^{ij}",
            "odd_parentization_result": "INSUFFICIENT",
            "lock_result": "not_locked",
            "new_information": "STF stress may be exchange-even and conserved, so odd residual parity does not erase anisotropic stress by itself.",
            "best_next_action": "prove topological/isotropic stress theorem or retain xi/R11 stress bound",
            "valid_for_claim": "false",
        },
        {
            "component_id": "C3361_6_Y5_source_normalization",
            "physical_residual": "Delta_mu_source / measured-GM source normalization",
            "odd_parentization_result": "ODD_ONLY_ROUTE_REJECTED",
            "lock_result": "failed_current",
            "new_information": "This is the coupling gap. A universal source-normalization offset is exchange-even and can survive Y=0 as a constant/Gauss-flux zero mode.",
            "best_next_action": "attack current gauge lock plus parent G_ref/source charge owner before any more generic Yloc parity work",
            "valid_for_claim": "false",
        },
        {
            "component_id": "C3361_7_Y6_stress_Bianchi",
            "physical_residual": "nabla_mu T_extra^{mu nu} and extra conserved stress",
            "odd_parentization_result": "INSUFFICIENT",
            "lock_result": "retained_debt",
            "new_information": "Bianchi consistency can allow an exchange-even, conserved, non-Hilbert stress. Zero divergence is not zero stress.",
            "best_next_action": "derive topological/invisible T_extra theorem or keep explicit residual vector",
            "valid_for_claim": "false",
        },
        {
            "component_id": "C3361_8_PPN_vector",
            "physical_residual": "{gamma-1,beta-1,alpha_i,xi,zeta_i,Gdot}",
            "odd_parentization_result": "REQUIRES_FULL_LOCK",
            "lock_result": "not_locked",
            "new_information": "A PPN vector can be zeroed by odd residuals only if the metric/source/readout residual map has full rank and no GM absorption leak.",
            "best_next_action": "defer promotion until Y5 and readout/projector branches are fixed",
            "valid_for_claim": "false",
        },
        {
            "component_id": "C3361_9_R11_operator_vector",
            "physical_residual": "non-EH operator and source-normalization R11 vector",
            "odd_parentization_result": "REQUIRES_FACTORISATION_PLUS_LOCK",
            "lock_result": "not_locked",
            "new_information": "R11 zero follows only if actual coefficients factor through locked odd variables or are absent/topological; source-normalization operator is the live pressure row.",
            "best_next_action": "move Y5 source-normalization operator to the first coupling-specific theorem/bound attempt",
            "valid_for_claim": "false",
        },
    ]


def y5_obstruction_rows() -> list[dict[str, Any]]:
    return [
        {
            "obstruction_id": "Y5OBS3361_0_even_calibration_mode",
            "claim": "An exchange-even scalar calibration offset can shift measured GM while all odd residuals vanish.",
            "math_form": "mu_obs = G_ref M_H (1+epsilon_mu), I(epsilon_mu)=epsilon_mu",
            "result": "PROVED_OBSTRUCTION_TO_ODD_ONLY_Y5",
            "consequence": "odd parentization alone cannot derive source-normalized Newtonian mechanics",
            "escape_route": "prove epsilon_mu is parent-fixed/topological, or promote it to an explicit bounded source-normalization operator",
            "valid_for_claim": "false",
        },
        {
            "obstruction_id": "Y5OBS3361_1_constant_zero_mode",
            "claim": "A local positive operator with derivative energy does not fix a constant coupling zero mode.",
            "math_form": "integral |nabla epsilon_mu|^2 = 0 allows epsilon_mu=constant unless potential/reference charge fixes it",
            "result": "PROVED_LOCAL_EULER_INSUFFICIENCY",
            "consequence": "local plateau/Euler proof cannot by itself derive the absolute source coupling",
            "escape_route": "add parent potential/normalization theorem or use current gauge lock plus G_ref owner",
            "valid_for_claim": "false",
        },
        {
            "obstruction_id": "Y5OBS3361_2_Gauss_flux_owner",
            "claim": "Measured GM is read from a surface/Gauss charge, so pointwise local bulk silence is not enough.",
            "math_form": "mu_obs ~ integral_S partial_r Phi dS = G_ref M_H + mu_boundary + mu_projector + mu_nonEH",
            "result": "PROVED_SCOPE_SEPARATION",
            "consequence": "3357 local bulk source cleanup does not close integrated Newtonian source calibration",
            "escape_route": "derive charge closure and no extra mass projection or build explicit arena bounds",
            "valid_for_claim": "false",
        },
        {
            "obstruction_id": "Y5OBS3361_3_EH_coefficient_source_load",
            "claim": "If the coupling scalar multiplies the EH coefficient, its variation can see curvature/source load unless the parent fixes the coefficient.",
            "math_form": "S_EH=(2 kappa(epsilon_mu))^-1 int sqrt(-g) R; delta S/d epsilon_mu proportional to d(kappa^-1)/d epsilon_mu int sqrt(-g) R",
            "result": "DERIVATION_PRESSURE_ROW",
            "consequence": "source normalization is a coupling/current problem, not merely a local vacuum field problem",
            "escape_route": "derive fixed universal kappa/G_ref or treat epsilon_mu as scalar-tensor/Gdot/fifth-force residual",
            "valid_for_claim": "false",
        },
        {
            "obstruction_id": "Y5OBS3361_4_current_gauge_escape",
            "claim": "Gauge/Noether current ownership can kill variable coupling but only after excluding compensator currents.",
            "math_form": "nabla_mu(kappa_J J^mu + J_comp^mu)=0; J_comp=0 and current richness => nabla_mu kappa_J=0",
            "result": "BEST_NEXT_ROUTE_IDENTIFIED",
            "consequence": "the next target should be a coupling/current-owner theorem, not another generic odd residual pass",
            "escape_route": "prove parent-owned J_H/J_Q, current richness, no compensator/source-shadow, and G_ref reference normalization",
            "valid_for_claim": "false",
        },
    ]


def promotion_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "GATE3361_0_physical_lock_theorem",
            "claim": "physical lock theorem is mathematically stated and proven as a conditional implication",
            "passed": "true",
            "reason": "R_phys=A Y+O(Y^2), R_phys(0)=0 is sufficient for Y=0 => R_phys=0",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3361_1_odd_only_route",
            "claim": "generic odd residual parentization closes local GR/Newton",
            "passed": "false",
            "reason": "bookkeeping auxiliary no-go and Y5/Y6 even residual countermodels survive",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3361_2_Y5_source_normalization_zero",
            "claim": "Delta_mu_source is derived zero",
            "passed": "false",
            "reason": "Y5 is an even calibration/Gauss-flux zero-mode unless current/charge/G_ref owner closes",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3361_3_current_gauge_lock_claim",
            "claim": "current gauge lock proves source normalization constant and zero",
            "passed": "false",
            "reason": "route is identified, but current owner, current richness, no-compensator, and absolute G_ref normalization are not signed",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3361_4_PPN_R11_physical_lock",
            "claim": "PPN and R11 residuals are physically locked to Y variables",
            "passed": "false",
            "reason": "full-rank residual Jacobian and same-readout branch are not parent-derived",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3361_5_local_GR_Newton_claim",
            "claim": "local GR/Newton branch is claim-ready",
            "passed": "false",
            "reason": "Y5 source coupling and physical lock remain open despite sharper theorem/obstruction results",
            "valid_for_claim": "false",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3361_0",
            "question": "Did 3361 derive local GR by odd residual parentization?",
            "answer": "no",
            "reason": "odd parentization is sufficient only after physical lock, no even leakage, same branch, and boundary/source silence; Y5 and Y6 violate the generic route",
            "next_action": "stop spending turns on generic Yloc parity and target the coupling/source-current owner directly",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC3361_1",
            "question": "What did 3361 actually prove?",
            "answer": "it proved the conditional physical-lock theorem and a no-go for odd-only Y5 closure",
            "reason": "measured-GM/source normalization can be exchange-even and can survive as a constant/Gauss-flux zero mode",
            "next_action": "build 3362 around current gauge lock, parent Noether/Hilbert source charge, no compensator current, and G_ref owner",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC3361_2",
            "question": "What is the best route now?",
            "answer": "coupling/source-current lock first, R11 numeric bounds second",
            "reason": "without Y5, Newtonian source normalization can absorb or fake success in PPN/R11 tests",
            "next_action": "attempt a source-current gauge lock theorem before more comparator scoring",
            "valid_for_claim": "false",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "target_id": "3362-Y5-R2FR-source-current-gauge-lock-and-Gref-owner-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3362_source_current_gauge_lock_and_Gref_owner.py",
            "objective": "derive source normalization from parent-owned gauge/Noether current conservation, current richness, no compensator current, and a fixed G_ref/source charge owner; otherwise demote Y5 to an explicit source-normalization residual bound",
            "why_next": "3361 proves odd residual parity cannot close Y5 by itself; the coupling/current owner is now the pressure row",
            "valid_for_claim": "false",
        },
        {
            "target_id": "3363-Y5-R2FR-first-source-normalization-bound-row-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3363_first_source_normalization_bound_row.py",
            "objective": "if 3362 cannot prove the theorem, build the first source-backed bound row for epsilon_mu or c_domain_source_normalization_operator with units, weak-field map, and arena source path",
            "why_next": "the fallback must become quantitative rather than another missing-input ledger",
            "valid_for_claim": "false",
        },
    ]


def validation_rows() -> list[dict[str, Any]]:
    output_paths = [path for key, path in OUTPUTS.items() if key != "validation"]
    sources = local_source_rows()
    theorem_rows = theorem_packet_rows()
    component_rows = component_result_rows()
    obstruction_rows = y5_obstruction_rows()
    gate_rows = promotion_gate_rows()
    next_rows = next_target_rows()
    checks: list[dict[str, Any]] = []

    def add(check_id: str, check: str, passed: bool, detail: str = "") -> None:
        checks.append(
            {
                "check_id": check_id,
                "check": check,
                "passed": bool_str(passed),
                "detail": detail,
            }
        )

    add(
        "VAL3361_0_local_sources_exist",
        "all cited local source paths exist",
        all(row["exists"] == "true" for row in sources),
    )
    add(
        "VAL3361_1_local_sources_parse",
        "all cited local source paths parse",
        all(row["parseable"] == "true" for row in sources),
    )
    add(
        "VAL3361_2_outputs_parse",
        "all 3361 non-validation outputs parse",
        all(path.exists() and parseable(path) for path in output_paths),
    )
    add(
        "VAL3361_3_theorem_packet_substantive",
        "the theorem packet contains lock theorem, no-go, Y5 obstruction, and coupling route",
        all(
            required in {row["proof_status"] for row in theorem_rows}
            for required in [
                "EXACT_CONDITIONAL_LOCK_THEOREM",
                "EXACT_NO_GO_ODD_ONLY",
                "EXACT_CONDITIONAL_Y5_ODD_ROUTE_REJECTION",
                "VALID_CONDITIONAL_ROUTE_NOT_PARENT_SIGNED",
            ]
        ),
    )
    add(
        "VAL3361_4_component_coverage",
        "component result covers q_loc, Y0-Y6, PPN, and R11",
        {row["component_id"] for row in component_rows}
        == {
            "C3361_0_q_loc",
            "C3361_1_Y0_trace_expansion",
            "C3361_2_Y1_coherent_projector",
            "C3361_3_Y2_boundary_flux",
            "C3361_4_Y3_domain_vector",
            "C3361_5_Y4_domain_STF_stress",
            "C3361_6_Y5_source_normalization",
            "C3361_7_Y6_stress_Bianchi",
            "C3361_8_PPN_vector",
            "C3361_9_R11_operator_vector",
        },
    )
    add(
        "VAL3361_5_Y5_route_not_generic_parity",
        "Y5 rows reject odd-only closure and select current/charge owner route",
        any(row["result"] == "PROVED_OBSTRUCTION_TO_ODD_ONLY_Y5" for row in obstruction_rows)
        and any(row["result"] == "BEST_NEXT_ROUTE_IDENTIFIED" for row in obstruction_rows),
    )
    add(
        "VAL3361_6_no_overclaim",
        "local GR/Newton, Y5 zero, current gauge lock, PPN/R11 lock remain unpromoted",
        all(
            row["passed"] == "false"
            for row in gate_rows
            if row["gate_id"]
            in {
                "GATE3361_1_odd_only_route",
                "GATE3361_2_Y5_source_normalization_zero",
                "GATE3361_3_current_gauge_lock_claim",
                "GATE3361_4_PPN_R11_physical_lock",
                "GATE3361_5_local_GR_Newton_claim",
            }
        ),
    )
    add(
        "VAL3361_7_next_target_coupling_specific",
        "next target attacks source-current gauge lock/G_ref owner rather than another generic parity pass",
        any("source-current" in row["target_id"] and "Gref" in row["target_id"] for row in next_rows),
    )
    add(
        "VAL3361_8_write_scope_outside_formalization",
        "all 3361 write targets are outside formalization-workbench",
        all(FW not in path.parents and path != FW for path in [DOC, *output_paths, OUTPUTS["validation"]]),
        "write_targets=" + str(len([DOC, *output_paths, OUTPUTS["validation"]])),
    )
    overall = all(row["passed"] == "true" for row in checks)
    add(
        "VAL3361_9_overall",
        "3361 validation overall",
        overall,
        "all required checks passed" if overall else "one or more checks failed",
    )
    return checks


def write_doc(
    sources: list[dict[str, Any]],
    theorem_rows: list[dict[str, Any]],
    lock_rows: list[dict[str, Any]],
    component_rows: list[dict[str, Any]],
    obstruction_rows: list[dict[str, Any]],
    gate_rows: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    validations: list[dict[str, Any]],
) -> None:
    sections = [
        "# 3361 - Odd Residual Parentization And Physical Lock Under AX1090",
        "",
        f"Generated: `{RUN_UTC}`",
        "",
        "## Summary",
        "- This checkpoint attacks the 3360 blocker directly: whether `Y_loc=0` would actually mean the physical residuals vanish.",
        "- Real gain: the physical-lock theorem is now explicit. `Y=0` kills physical residuals only when `R_phys=A Y+O(Y^2)` has no constant/even leakage and the same branch/readout is used.",
        "- Stronger gain: the generic odd-residual route is rejected for `Y5` source normalization. A measured-GM/coupling offset can be exchange-even and survive as a constant or Gauss-flux zero mode.",
        "- This means the coupling really is the pressure point: `Y5` needs a source-current/gauge/Noether charge owner plus fixed `G_ref`, or it must become an explicit bounded residual.",
        "- No local GR/Newton claim is promoted here; the next move is narrower and sharper, not another circular missing-input pass.",
        "",
        "## Local Source Register",
        table(sources),
        "## Odd Parentization Theorem Packet",
        table(theorem_rows),
        "## Physical Lock Jacobian Gate",
        table(lock_rows),
        "## Component Lock Result",
        table(component_rows),
        "## Y5 Zero-Mode Obstruction",
        table(obstruction_rows),
        "## Promotion Gates",
        table(gate_rows),
        "## Decision Ledger",
        table(decisions),
        "## Next Target",
        table(next_rows),
        "## Validation",
        table(validations),
    ]
    DOC.write_text("\n".join(sections), encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    rows_by_output = {
        "local_sources": local_source_rows(),
        "theorem_packet": theorem_packet_rows(),
        "lock_gate": physical_lock_gate_rows(),
        "component_result": component_result_rows(),
        "y5_obstruction": y5_obstruction_rows(),
        "gates": promotion_gate_rows(),
        "decision": decision_rows(),
        "next": next_target_rows(),
    }
    for key, rows in rows_by_output.items():
        write_csv(OUTPUTS[key], rows)
    validations = validation_rows()
    write_csv(OUTPUTS["validation"], validations)
    write_doc(
        rows_by_output["local_sources"],
        rows_by_output["theorem_packet"],
        rows_by_output["lock_gate"],
        rows_by_output["component_result"],
        rows_by_output["y5_obstruction"],
        rows_by_output["gates"],
        rows_by_output["decision"],
        rows_by_output["next"],
        validations,
    )
    if PYCACHE.exists():
        shutil.rmtree(PYCACHE)


if __name__ == "__main__":
    main()
