from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4342"
CLAIM_ID = "L-183"
BRANCH = "MTS_R2FR_Y5_CDELTAKDIV_PROFILE_ROW_AND_RIGHT_INVERSE_COMMUTATOR_ZERO_4342"
DECISION = "KL_GENERATOR_FOR_KGAMMA_DERIVED_FLATPATCH_CRI_ZERO_DELTAKDIV_REDUCED_TO_KPERP_KERNEL_NONCLAIM"
MARKER = "PPC4161_KL_GENERATOR_FOR_KGAMMA_AND_CRI_CDELTAKDIV_ZERO_BRANCH_4342"
PACKET_MARKER = "PPC4161_PACKET_KL_GENERATOR_FOR_KGAMMA_AND_CRI_CDELTAKDIV_ZERO_BRANCH_4342"
NEXT_TARGET = "4343-Y5-R2FR-parent-action-owner-for-KGamma-or-Kperp-sector-bound-runner.md"

FORMAL_PATH = FORMAL / "358-PPC4161-KL-generator-for-KGamma-and-CRI-CDeltaKdiv-zero-branch.md"
DOC_PATH = POST / "4342-Y5-R2FR-CdeltaKdiv-profile-row-and-right-inverse-commutator-zero.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4342_VALIDATION.csv"
GENERATED_UTC = datetime.now(timezone.utc).isoformat(timespec="seconds")

Y_GAMMA_LIMIT = 0.0002739826487147268
Y_BETA_LIMIT = 0.0009529831259642674
Y_CLOCK_LIMIT = 0.0006134828873394971


SOURCES = [
    (
        "SRC4342_00_4341_next",
        FORMAL / "357-PPC4161-Khat-right-inverse-parent-signature-or-DeltaK-divergence-bound.md",
        "4342-Y5-R2FR-CdeltaKdiv-profile-row-and-right-inverse-commutator-zero.md",
        "4341 handoff selecting K_L-like generator or C_DeltaKdiv/C_RI bound rows.",
    ),
    (
        "SRC4342_01_61_KL_definition",
        FORMAL / "61-local-ppn-tensor-ansatz.md",
        "K_L,loc^{mu nu}[A] =",
        "Original local longitudinal tensor definition.",
    ),
    (
        "SRC4342_02_61_Box_source",
        FORMAL / "61-local-ppn-tensor-ansatz.md",
        "Box A_loc^nu = q_loc^nu.",
        "Longitudinal owner field equation.",
    ),
    (
        "SRC4342_03_61_div_identity",
        FORMAL / "61-local-ppn-tensor-ansatz.md",
        "partial_mu K_L,loc^{mu nu} = -q_loc^nu.",
        "Flat-patch divergence identity used to build K_Gamma.",
    ),
    (
        "SRC4342_04_61_boundary_warning",
        FORMAL / "61-local-ppn-tensor-ansatz.md",
        "inner and outer boundary conditions for A_loc^nu;",
        "Boundary/gauge data remain required for physical scoring.",
    ),
    (
        "SRC4342_05_352_imported_KL",
        FORMAL / "352-PPC4161-open-tail-PiPPN-metric-transfer-derivation-or-R10-parent-alpha-fill.md",
        "partial_mu K_L^{mu nu}=-q_loc^nu",
        "Later operator factorisation imported the K_L identity.",
    ),
    (
        "SRC4342_06_315_DeltaK_split",
        FORMAL / "315-PPC4161-DvGamma-DvKhat-first-source-coefficient-or-QAP-parent-signature.md",
        "Delta_K := K_hat - K_metric[Gamma_eff],",
        "Earlier DeltaK split that 4342 refines to Khat-KGamma/Kperp.",
    ),
    (
        "SRC4342_07_216_Kperp_not_zero",
        FORMAL / "216-PPC4161-Kperp-boundary-zero-or-demotion.md",
        "divergence-free != zero,",
        "Divergence-free residuals are not automatically safe.",
    ),
    (
        "SRC4342_08_216_Kperp_bound",
        FORMAL / "216-PPC4161-Kperp-boundary-zero-or-demotion.md",
        "||K_perp||_E <= C_T (||S_T|| + ||B_T|| + ||I_T|| + ||Z_T||).",
        "Existing finite Kperp energy-bound route.",
    ),
    (
        "SRC4342_09_219_Kperp_pole",
        FORMAL / "219-PPC4161-no-physical-Kperp-pole-theorem.md",
        "K_perp = ordinary GR transverse-traceless homogeneous metric freedom,",
        "Best clean Kperp no-extra-pole branch, parent unsigned.",
    ),
    (
        "SRC4342_10_220_Kperp_sector",
        FORMAL / "220-PPC4161-Kperp-sector-placement-theorem.md",
        "K_perp = K_metric_TT + K_vertical + K_boundary + K_extra_source.",
        "Kperp sector-placement/no-double-count rule.",
    ),
    (
        "SRC4342_11_353_qprofile",
        FORMAL / "353-PPC4161-source-Sq-qprofile-kernel-and-metric-green-coupling-or-R10-alpha-parent-pivot.md",
        "q_loc^nu=P_loc[nabla^nu Gamma_eff-nabla_mu K_hat^{mu nu}]",
        "Observable q-profile receiving the KGamma/Kperp reduction.",
    ),
]


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8-sig")
    except FileNotFoundError:
        return ""


def find_line(path: Path, needle: str) -> str:
    text = read_text(path)
    index = text.find(needle)
    if index < 0:
        return ""
    return str(text[:index].count("\n") + 1)


def write_csv(path: Path, rows: List[Dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields: List[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: str(row.get(key, "")) for key in fields})


def md_cell(value: object) -> str:
    return str(value).replace("|", r"\|").replace("\n", "<br>")


def md_table(rows: List[Dict[str, str]], fields: List[str]) -> str:
    if not rows:
        return "_No rows._"
    header = "| " + " | ".join(fields) + " |"
    sep = "| " + " | ".join("---" for _ in fields) + " |"
    body = ["| " + " | ".join(md_cell(row.get(field, "")) for field in fields) + " |" for row in rows]
    return "\n".join([header, sep, *body])


def append_once(path: Path, marker: str, block: str) -> None:
    text = read_text(path)
    if marker in text:
        return
    if text and not text.endswith("\n"):
        text += "\n"
    path.write_text(text + block.strip() + "\n", encoding="utf-8")


def source_rows() -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    for source_id, path, needle, role in SOURCES:
        line_number = find_line(path, needle)
        rows.append(
            {
                "source_id": source_id,
                "path": str(path),
                "path_exists": str(path.exists()),
                "needle": needle,
                "needle_found": str(bool(line_number)),
                "line_number": line_number,
                "role": role,
            }
        )
    return rows


def generator_rows() -> List[Dict[str, str]]:
    return [
        {
            "generator_id": "GEN4342_0_flat_Agamma",
            "name": "flat-patch KGamma from K_L",
            "definition": "Choose A_Gamma^nu=-G_Box^bc partial^nu Gamma_eff on the fixed local weak-field patch.",
            "operator_equation": "Box A_Gamma^nu = -partial^nu Gamma_eff",
            "K_map": "K_Gamma^{mu nu}=-(partial^mu A_Gamma^nu+partial^nu A_Gamma^mu)+eta^{mu nu} partial_alpha A_Gamma^alpha",
            "identity": "partial_mu K_Gamma^{mu nu}=partial^nu Gamma_eff",
            "status": "DERIVED_FLAT_PATCH_RIGHT_INVERSE",
            "valid_for_claim": "False",
        },
        {
            "generator_id": "GEN4342_1_scalar_potential_form",
            "name": "scalar-potential shorthand",
            "definition": "If A_Gamma^nu=-partial^nu Phi_Gamma and Box Phi_Gamma=Gamma_eff, then K_Gamma=2 partial^mu partial^nu Phi_Gamma-eta^{mu nu} Gamma_eff.",
            "operator_equation": "Box Phi_Gamma=Gamma_eff",
            "K_map": "K_Gamma^{mu nu}=2 partial^mu partial^nu Phi_Gamma-eta^{mu nu} Gamma_eff",
            "identity": "partial_mu K_Gamma^{mu nu}=partial^nu Gamma_eff when partial derivatives commute",
            "status": "DERIVED_FLAT_SCALAR_VERSION",
            "valid_for_claim": "False",
        },
        {
            "generator_id": "GEN4342_2_curved_Ricci_corrected",
            "name": "curved Ricci-corrected local operator",
            "definition": "Use the covariant K_L map with L_RI A := (nabla_alpha nabla^alpha delta^nu_sigma + Ric^nu_sigma) A^sigma.",
            "operator_equation": "L_RI A_Gamma^nu = -nabla^nu Gamma_eff",
            "K_map": "K_Gamma^{mu nu}=-(nabla^mu A_Gamma^nu+nabla^nu A_Gamma^mu)+g^{mu nu} nabla_alpha A_Gamma^alpha",
            "identity": "nabla_mu K_Gamma^{mu nu}=nabla^nu Gamma_eff if L_RI inverse and boundary data exist",
            "status": "DERIVED_COVARIANT_FORM_OPERATOR_INVERTIBILITY_OPEN",
            "valid_for_claim": "False",
        },
        {
            "generator_id": "GEN4342_3_CRI_flat_zero",
            "name": "fixed-background right-inverse commutator",
            "definition": "If D_v does not vary eta, G_Box^bc, boundary data, or P_loc, then D_v commutes with the flat KGamma generator.",
            "operator_equation": "[D_v,partial_mu K_L G_Box^bc partial] Gamma_eff=0",
            "K_map": "D_v div K_Gamma = partial^nu D_v Gamma_eff",
            "identity": "C_RI^flat=0",
            "status": "ZERO_DERIVED_ON_FIXED_FLAT_PATCH_BRANCH",
            "valid_for_claim": "False",
        },
        {
            "generator_id": "GEN4342_4_CRI_curved_tail",
            "name": "curved/boundary right-inverse commutator",
            "definition": "If D_v varies metric, Ricci, boundary, collar, or projection, the right-inverse commutator reopens.",
            "operator_equation": "D_v G_RI = -G_RI (D_v L_RI) G_RI plus boundary-domain terms",
            "K_map": "C_RI = P_loc div K_L[(D_v G_RI)nabla Gamma_eff + G_RI(D_v nabla)Gamma_eff] + D_v(P_loc,domain)",
            "identity": "C_RI is not zero unless these variations are fixed or bounded",
            "status": "BOUND_FORMULA_DERIVED_INPUTS_OPEN",
            "valid_for_claim": "False",
        },
        {
            "generator_id": "GEN4342_5_DeltaK_to_Kperp",
            "name": "DeltaK divergence reduced to Kperp kernel",
            "definition": "With K_hat=K_Gamma+K_perp+K_extra, Delta_K=K_perp+K_extra.",
            "operator_equation": "nabla_mu K_perp^{mu nu}=0 and P_loc nabla_mu D_v K_perp^{mu nu}=0 if the vertical variation preserves the co-closed kernel",
            "K_map": "C_DeltaK_div = ||P_loc nabla_mu D_v(K_perp+K_extra)^{mu nu}||_obs/a_ref",
            "identity": "C_DeltaK_div=0 only on the preserved co-closed/no-extra-source branch",
            "status": "REDUCED_TO_KPERP_KERNEL_OR_BOUND",
            "valid_for_claim": "False",
        },
    ]


def proof_rows() -> List[Dict[str, str]]:
    return [
        {
            "proof_id": "PRF4342_0_flat_identity",
            "claim": "The right-inverse identity is algebraically real in the local flat patch.",
            "derivation": "From K_L[A]=-(partial A+partial A)+eta div A, partial_mu K_L^{mu nu}=-Box A^nu. Taking Box A_Gamma^nu=-partial^nu Gamma_eff gives div K_Gamma=grad Gamma_eff.",
            "status": "PROVED_AS_LOCAL_DIFFERENTIAL_IDENTITY",
            "remaining_caveat": "requires fixed boundary/Green data and does not by itself parent-sign the action",
            "valid_for_claim": "False",
        },
        {
            "proof_id": "PRF4342_1_curved_identity",
            "claim": "A covariant right-inverse exists in form if the Ricci-corrected operator is invertible.",
            "derivation": "For K_L[A]=-(nabla A+nabla A)+g div A, nabla_mu K_L^{mu nu}=-(Box delta^nu_sigma+Ric^nu_sigma)A^sigma. Solve L_RI A=-nabla Gamma.",
            "status": "DERIVED_OPERATOR_FORM_INVERTIBILITY_OPEN",
            "remaining_caveat": "needs elliptic/hyperbolic boundary choice, gauge, and local collar invertibility",
            "valid_for_claim": "False",
        },
        {
            "proof_id": "PRF4342_2_CRI_zero",
            "claim": "C_RI vanishes on the fixed flat-patch branch.",
            "derivation": "D_v commutes with partial derivatives and fixed G_Box^bc; therefore D_v div K_Gamma=partial D_v Gamma and the right-inverse commutator is zero.",
            "status": "PROVED_ON_FIXED_FLAT_BACKGROUND",
            "remaining_caveat": "not valid if D_v moves metric, boundary, collar, Green function, or projection",
            "valid_for_claim": "False",
        },
        {
            "proof_id": "PRF4342_3_CDeltaK_zero",
            "claim": "C_DeltaK_div vanishes if the residual is co-closed and the variation preserves that co-closed condition.",
            "derivation": "Delta_K=K_perp on the no-extra-source branch; if div K_perp=0 and D_v(div K_perp)=0 in the tested projection, then P_loc div D_v Delta_K=0.",
            "status": "CONDITIONAL_KERNEL_ZERO_DERIVED",
            "remaining_caveat": "divergence-free does not mean metric-safe; Kperp sector placement or finite metric bound is still required",
            "valid_for_claim": "False",
        },
        {
            "proof_id": "PRF4342_4_no_full_local_GR",
            "claim": "This checkpoint cannot be promoted to local GR.",
            "derivation": "The KGamma generator removes one q_tr route only under fixed geometry/kernel clauses; Kperp metric stress, parent action stress, arena projection constants, and other P_leak gates remain open.",
            "status": "FIREWALL_PROVED",
            "remaining_caveat": "next step must parent-sign the owner block or score Kperp/commutator tails",
            "valid_for_claim": "False",
        },
    ]


def bound_rows() -> List[Dict[str, str]]:
    return [
        {
            "bound_id": "BND4342_0_CRI_flat",
            "quantity": "C_RI^flat",
            "formula": "C_RI^flat=0 when D_v eta=D_v G_Box^bc=D_v boundary=D_v P_loc=0",
            "inputs_needed": "fixed flat weak-field patch, fixed Green boundary, fixed local projection",
            "status": "ZERO_DERIVED_CONDITIONAL",
            "claim_gate": "parent action must adopt this fixed-background owner branch before scoring",
            "valid_for_claim": "False",
        },
        {
            "bound_id": "BND4342_1_CRI_curved",
            "quantity": "C_RI^curved",
            "formula": "C_RI^curved <= ||P_loc div K_L G_RI (D_v L_RI) A_Gamma||/a_ref + C_Dnabla + C_boundary + C_projection",
            "inputs_needed": "G_RI norm, D_v Ricci/metric, D_v boundary/collar, D_v P_loc",
            "status": "BOUND_FORMULA_READY_VALUES_MISSING",
            "claim_gate": "numeric/source-backed terms or zero theorem",
            "valid_for_claim": "False",
        },
        {
            "bound_id": "BND4342_2_CDeltaKdiv_kernel",
            "quantity": "C_DeltaK_div",
            "formula": "C_DeltaK_div=0 if Delta_K=K_perp, nabla_mu K_perp^{mu nu}=0, and P_loc nabla_mu D_v K_perp^{mu nu}=0",
            "inputs_needed": "Khat=KGamma+Kperp parent split, preserved co-closed kernel, no K_extra_source",
            "status": "CONDITIONAL_ZERO_DERIVED",
            "claim_gate": "parent-signed sector placement and vertical kernel preservation",
            "valid_for_claim": "False",
        },
        {
            "bound_id": "BND4342_3_CDeltaKdiv_finite",
            "quantity": "C_DeltaK_div",
            "formula": "C_DeltaK_div <= ||P_loc div D_v K_perp||_obs/a_ref + ||P_loc div D_v K_extra_source||_obs/a_ref",
            "inputs_needed": "Kperp finite coefficient vector; source/boundary/incoming-mode/profile rows",
            "status": "FINITE_BOUND_ROUTE_READY",
            "claim_gate": "all coefficients source-backed and fixed before scoring",
            "valid_for_claim": "False",
        },
        {
            "bound_id": "BND4342_4_Kperp_metric",
            "quantity": "R_i^K",
            "formula": "|R_i^K| <= W_i^K C_T (||S_T||+||B_T||+||I_T||+||Z_T||)",
            "inputs_needed": "W_i^K, C_T, S_T, B_T, I_T, Z_T",
            "status": "IMPORTED_SCOREABLE_KPERP_METRIC_TAIL",
            "claim_gate": "Kperp metric residual below PPN/R10/clock/orbital/WEP gates",
            "valid_for_claim": "False",
        },
        {
            "bound_id": "BND4342_5_arena_vector",
            "quantity": "Y_a^4342",
            "formula": "Y_a^4342 <= ||Pi_a^RI|| C_RI + ||Pi_a^Delta|| C_DeltaK_div + W_a^K C_T(||S_T||+||B_T||+||I_T||+||Z_T||)",
            "inputs_needed": "arena projections and Kperp coefficients",
            "status": "LOCAL_VECTOR_FORMULA_READY_VALUES_MISSING",
            "claim_gate": f"PPN_gamma<={Y_GAMMA_LIMIT}; PPN_beta<={Y_BETA_LIMIT}; clock<={Y_CLOCK_LIMIT}; R10/orbital/WEP separately sourced",
            "valid_for_claim": "False",
        },
    ]


def input_rows() -> List[Dict[str, str]]:
    return [
        {
            "input_id": "IN4342_0_parent_adoption",
            "symbol": "S_RI[A_Gamma,Gamma_eff]",
            "definition": "parent action or constrained owner block adopting the K_L/KGamma generator",
            "status": "MISSING_PARENT_ACTION_SIGNATURE",
            "next_action": "derive metric-null auxiliary owner or include its Hilbert stress explicitly",
            "valid_for_claim": "False",
        },
        {
            "input_id": "IN4342_1_boundary",
            "symbol": "bc_RI",
            "definition": "inner/outer boundary and Green-function choice for A_Gamma",
            "status": "MISSING_FIXED_BOUNDARY_SOURCE_ROW",
            "next_action": "choose retarded/static/Dirichlet/Neumann collar data before scoring",
            "valid_for_claim": "False",
        },
        {
            "input_id": "IN4342_2_metric_variation",
            "symbol": "D_v L_RI, D_v P_loc",
            "definition": "variation of Ricci-corrected right-inverse operator and local projection",
            "status": "MISSING_ZERO_THEOREM_OR_NORM",
            "next_action": "prove fixed-background branch or source finite commutator norms",
            "valid_for_claim": "False",
        },
        {
            "input_id": "IN4342_3_Kperp_sector",
            "symbol": "K_perp sector placement",
            "definition": "classification of residual as ordinary GR TT/gauge/boundary/vertical or extra source",
            "status": "MISSING_PARENT_SECTOR_SIGNATURE",
            "next_action": "adopt 220 sector placement and prove no K_extra_source, or run finite Kperp bound",
            "valid_for_claim": "False",
        },
        {
            "input_id": "IN4342_4_Kperp_coefficients",
            "symbol": "C_T,S_T,B_T,I_T,Z_T,W_i^K",
            "definition": "finite Kperp energy and arena transfer coefficients",
            "status": "MISSING_NUMERIC_SOURCE_ROWS",
            "next_action": "fill from existing Kperp bound runner or create source-backed placeholders marked nonclaim",
            "valid_for_claim": "False",
        },
        {
            "input_id": "IN4342_5_arena_projection",
            "symbol": "Pi_a^RI, Pi_a^Delta",
            "definition": "projection constants from right-inverse and DeltaK tails into local tests",
            "status": "MISSING_ARENA_PROJECTION_CONSTANTS",
            "next_action": "fixed before any R10/PPN/clock/orbital scoring",
            "valid_for_claim": "False",
        },
    ]


def branch_rows() -> List[Dict[str, str]]:
    return [
        {
            "branch_id": "BR4342_0_clean_flat_owner",
            "branch": "fixed flat K_L/KGamma owner",
            "conditions": "parent adopts K_L generator; fixed G_Box/boundary/projection; Khat=KGamma+Kperp; D_v preserves div Kperp=0; Kperp sector non-extra",
            "output": "C_RI=0 and C_DeltaK_div=0 for this channel",
            "status": "BEST_BRANCH_DERIVED_BUT_PARENT_UNSIGNED",
            "valid_for_claim": "False",
        },
        {
            "branch_id": "BR4342_1_curved_owner_bound",
            "branch": "curved Ricci-corrected owner",
            "conditions": "L_RI invertible with fixed covariant boundary data; D_v L_RI bounded",
            "output": "C_RI^curved finite instead of zero",
            "status": "BOUND_ROUTE_OPEN",
            "valid_for_claim": "False",
        },
        {
            "branch_id": "BR4342_2_Kperp_finite",
            "branch": "Kperp finite source-pack",
            "conditions": "Kperp not parent-demoted to GR/gauge/boundary",
            "output": "score W_i^K C_T(S_T+B_T+I_T+Z_T)",
            "status": "FALLBACK_SCOREABLE",
            "valid_for_claim": "False",
        },
        {
            "branch_id": "BR4342_3_rejected_magic_zero",
            "branch": "divergence-free means harmless",
            "conditions": "div Kperp=0 asserted without metric sector placement",
            "output": "blocked",
            "status": "REJECTED",
            "valid_for_claim": "False",
        },
    ]


def runner_rows() -> List[Dict[str, str]]:
    return [
        {
            "runner_id": "RUN4342_0_current",
            "branch_input": "current corpus through 4341",
            "action": "ADOPT_DERIVED_KL_GENERATOR_KEEP_CLAIM_FALSE",
            "output": "flat-patch KGamma generator and C_RI=0 branch derived; DeltaKdiv reduced to Kperp kernel or Kperp finite bound",
            "claim_policy": "no local-GR/R10/PPN/clock/orbital/WEP claim",
            "valid_for_claim": "False",
        },
        {
            "runner_id": "RUN4342_1_zero_future",
            "branch_input": "parent-signed fixed K_L/KGamma owner plus preserved Kperp kernel",
            "action": "ALLOW_THIS_CHANNEL_ZERO",
            "output": "P_nonHilbert Khat/Gamma channel quiet",
            "claim_policy": "still not full local GR until remaining gates close",
            "valid_for_claim": "False",
        },
        {
            "runner_id": "RUN4342_2_bound_future",
            "branch_input": "curved/boundary/Kperp finite coefficients",
            "action": "RUN_NONCLAIM_LOCAL_VECTOR_SCORE",
            "output": "score Y_a^4342 against PPN/R10/clock/orbital/WEP gates",
            "claim_policy": "claim only if all values are numeric, sourced, fixed before scoring, and below gates",
            "valid_for_claim": "False",
        },
    ]


def firewall_rows() -> List[Dict[str, str]]:
    return [
        {
            "firewall_id": "FW4342_0",
            "forbidden_shortcut": "Treating the K_L generator as parent-signed because the algebra works",
            "reason": "algebraic right-inverse identity is not yet a parent action signature.",
            "status": "ACTIVE",
            "valid_for_claim": "False",
        },
        {
            "firewall_id": "FW4342_1",
            "forbidden_shortcut": "Using C_RI=0 outside fixed flat boundary/projection branch",
            "reason": "metric, Ricci, boundary, collar and projection variations reopen C_RI.",
            "status": "ACTIVE",
            "valid_for_claim": "False",
        },
        {
            "firewall_id": "FW4342_2",
            "forbidden_shortcut": "Calling divergence-free Kperp physically safe",
            "reason": "216/220 require Kperp sector placement or finite metric source scoring.",
            "status": "ACTIVE",
            "valid_for_claim": "False",
        },
        {
            "firewall_id": "FW4342_3",
            "forbidden_shortcut": "Dropping K_extra_source by notation",
            "reason": "the sector split must prove Kperp is ordinary GR/gauge/boundary/vertical or keep a scoreable source row.",
            "status": "ACTIVE",
            "valid_for_claim": "False",
        },
        {
            "firewall_id": "FW4342_4",
            "forbidden_shortcut": "Promoting this to local GR/Newton/Maxwell closure",
            "reason": "this checkpoint advances one local transition-current route only; calibrated source coupling and EM stress remain separate gates.",
            "status": "ACTIVE",
            "valid_for_claim": "False",
        },
    ]


def decision_rows() -> List[Dict[str, str]]:
    return [
        {
            "decision_id": "DEC4342_0",
            "decision": DECISION,
            "reason": "the K_L longitudinal owner gives a real K_Gamma right-inverse in the fixed flat local patch and a Ricci-corrected curved operator form; the remaining issue is parent ownership plus Kperp/commutator metric safety",
            "next_action": NEXT_TARGET,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def status_rows() -> List[Dict[str, str]]:
    return [
        {
            "status_id": "STAT4342_0",
            "item": "KGamma construction",
            "status": "DERIVED_FROM_KL_GENERATOR",
            "notes": "right-inverse identity is no longer just a formal Div^-1 placeholder",
        },
        {
            "status_id": "STAT4342_1",
            "item": "C_RI",
            "status": "ZERO_ON_FIXED_FLAT_BRANCH_CURVED_TAIL_OPEN",
            "notes": "commutator is now split into exact flat zero and curved/boundary terms",
        },
        {
            "status_id": "STAT4342_2",
            "item": "C_DeltaK_div",
            "status": "REDUCED_TO_KPERP_KERNEL_OR_FINITE_BOUND",
            "notes": "DeltaK divergence can vanish if Kperp co-closed kernel is preserved; metric safety still open",
        },
        {
            "status_id": "STAT4342_3",
            "item": "next target",
            "status": "PARENT_OWNER_OR_KPERP_BOUND",
            "notes": NEXT_TARGET,
        },
    ]


def next_rows() -> List[Dict[str, str]]:
    return [
        {
            "next_target_id": "NT4342_0",
            "next_target": NEXT_TARGET,
            "target_question": "Can the K_L/KGamma owner be parent-signed as a metric-null auxiliary block, or must the Kperp sector be scored as the surviving local residual?",
            "preferred_route": "derive S_RI[A_Gamma,Gamma_eff] with no extra Hilbert stress and fixed boundary/projection, then adopt Kperp as GR TT/gauge/boundary/vertical",
            "fallback_route": "run finite Kperp and curved C_RI source rows using C_T,S_T,B_T,I_T,Z_T,W_i^K plus arena projections",
        }
    ]


def write_docs(tables: Dict[str, List[Dict[str, str]]]) -> None:
    formal = f"""# 358 PPC4161 K_L generator for KGamma and C_RI/C_DeltaKdiv zero branch

Marker: `{MARKER}`

Branch: `{BRANCH}`

Decision: `{DECISION}`

## Claim Status

Private nonclaim. This checkpoint does not prove public local GR, Newton, R10, PPN, clock safety, orbital safety, WEP safety, Maxwell closure, or a fundamental prediction of `G_N`.

## Result

4342 makes the right-inverse route constructive rather than hand-wavy.

Use the existing longitudinal tensor:

```text
K_L^{{mu nu}}[A]
  = -(partial^mu A^nu + partial^nu A^mu)
    + eta^{{mu nu}} partial_alpha A^alpha
```

with:

```text
partial_mu K_L^{{mu nu}}[A] = -Box A^nu.
```

Choose:

```text
Box A_Gamma^nu = -partial^nu Gamma_eff.
```

Then:

```text
K_Gamma := K_L[A_Gamma]
partial_mu K_Gamma^{{mu nu}} = partial^nu Gamma_eff.
```

That is the clean flat-patch right-inverse. The covariant version is also clear:

```text
K_Gamma^{{mu nu}}
  = -(nabla^mu A_Gamma^nu+nabla^nu A_Gamma^mu)
    + g^{{mu nu}} nabla_alpha A_Gamma^alpha

L_RI A_Gamma^nu
  := (nabla_alpha nabla^alpha delta^nu_sigma + Ric^nu_sigma) A_Gamma^sigma
  = -nabla^nu Gamma_eff.
```

If that operator is invertible with fixed boundary data, then:

```text
nabla_mu K_Gamma^{{mu nu}}=nabla^nu Gamma_eff.
```

So 4342 advances the route:

```text
q_tr = -div Delta_K + C_RI + C_conn + B_boundary
```

to:

```text
C_RI^flat = 0
C_DeltaK_div = 0 if Delta_K=K_perp and D_v preserves div K_perp=0.
```

But the local branch is still not claimed. The parent action must own the `K_L/KGamma` generator, and divergence-free `K_perp` must be sector-placed or bounded because divergence-free is not the same as metric-safe.

## Source Register

{md_table(tables["sources"], ["source_id", "path", "path_exists", "needle_found", "line_number", "role"])}

## Generator Rows

{md_table(tables["generators"], ["generator_id", "name", "definition", "operator_equation", "K_map", "identity", "status", "valid_for_claim"])}

## Proof Rows

{md_table(tables["proofs"], ["proof_id", "claim", "derivation", "status", "remaining_caveat", "valid_for_claim"])}

## Bound Rows

{md_table(tables["bounds"], ["bound_id", "quantity", "formula", "inputs_needed", "status", "claim_gate", "valid_for_claim"])}

## Required Inputs

{md_table(tables["inputs"], ["input_id", "symbol", "definition", "status", "next_action", "valid_for_claim"])}

## Branch Runner

{md_table(tables["branches"], ["branch_id", "branch", "conditions", "output", "status", "valid_for_claim"])}

## Runner

{md_table(tables["runner"], ["runner_id", "branch_input", "action", "output", "claim_policy", "valid_for_claim"])}

## Claim Firewall

{md_table(tables["firewall"], ["firewall_id", "forbidden_shortcut", "reason", "status", "valid_for_claim"])}

## Decision

{md_table(tables["decision"], ["decision_id", "decision", "reason", "next_action", "claim_allowed", "valid_for_claim"])}

## Status

{md_table(tables["status"], ["status_id", "item", "status", "notes"])}

## Next Target

{md_table(tables["next"], ["next_target_id", "next_target", "target_question", "preferred_route", "fallback_route"])}
"""
    post = f"""# 4342 Y5-R2FR CdeltaKdiv profile row and right-inverse commutator zero

Marker: `{MARKER}`

Decision: `{DECISION}`

## Result

4342 takes the leap: `K_Gamma` can be built from the existing `K_L` longitudinal generator.

```text
Box A_Gamma^nu = -partial^nu Gamma_eff
K_Gamma = K_L[A_Gamma]
partial_mu K_Gamma^{{mu nu}}=partial^nu Gamma_eff
```

This gives `C_RI^flat=0` on a fixed flat local patch. The curved version needs the Ricci-corrected operator and boundary data. `C_DeltaK_div` is reduced to the preserved `K_perp` co-closed kernel, or to the finite Kperp source-pack.

## Handoff

{md_table(tables["next"], ["next_target", "target_question", "preferred_route", "fallback_route"])}
"""
    FORMAL_PATH.write_text(formal, encoding="utf-8")
    DOC_PATH.write_text(post, encoding="utf-8")


def append_claim_once() -> None:
    path = FORMAL / "02-claims-register.csv"
    existing = read_text(path)
    if CLAIM_ID in existing:
        return
    with path.open("a", newline="", encoding="utf-8") as handle:
        if existing and not existing.endswith("\n"):
            handle.write("\n")
        writer = csv.writer(handle)
        writer.writerow(
            [
                CLAIM_ID,
                "local_gr",
                (
                    "4342 constructs K_Gamma from the existing K_L longitudinal tensor rather than leaving the right-inverse as a formal placeholder. "
                    "In the fixed local flat patch, choose Box A_Gamma^nu=-partial^nu Gamma_eff and K_Gamma=K_L[A_Gamma], giving partial_mu K_Gamma^{mu nu}=partial^nu Gamma_eff and C_RI^flat=0 when boundary, projection and Green data are fixed. "
                    "The curved version requires the Ricci-corrected operator L_RI A=(Box delta+Ric)A=-nabla Gamma and therefore retains invertibility, boundary and D_v L_RI commutator tails. "
                    "C_DeltaK_div is reduced to the Kperp kernel: it vanishes only if Delta_K=K_perp and the vertical variation preserves div K_perp=0; otherwise the finite Kperp source-pack and arena projection rows must be scored."
                ),
                "4342 source register, generator rows, proof rows, bound rows, required inputs, branch runner, runner, firewall, decision, status, next-target and validation CSV.",
                "private_KL_generator_for_KGamma_CRI_flat_zero_CDeltaKdiv_Kperp_kernel_nonclaim",
                "Parent-sign the K_L/KGamma owner block as metric-null/fixed-boundary, or run finite Kperp/curved-C_RI source rows against local arenas.",
                "Treating the K_L algebra as parent action ownership; using C_RI=0 outside fixed flat branch; calling divergence-free Kperp physically safe; dropping K_extra_source by notation; or promoting this single-channel result to full local GR.",
            ]
        )


def validation_rows(paths: Dict[str, Path], tables: Dict[str, List[Dict[str, str]]]) -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []

    def add(check_id: str, description: str, passed: bool, evidence: str) -> None:
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "branch": BRANCH,
                "generated_utc": GENERATED_UTC,
                "decision": DECISION,
                "claim_allowed": "False",
                "valid_for_claim": "False",
                "check_id": check_id,
                "description": description,
                "passed": str(bool(passed)),
                "evidence": evidence,
            }
        )

    add("VAL4342_sources_exist", "all source paths exist", all(row["path_exists"] == "True" for row in tables["sources"]), "source_register")
    add("VAL4342_needles_found", "all source anchors found", all(row["needle_found"] == "True" for row in tables["sources"]), "source_register")
    add("VAL4342_flat_generator", "flat KGamma generator row exists", any(row["generator_id"] == "GEN4342_0_flat_Agamma" and "partial^nu Gamma_eff" in row["identity"] for row in tables["generators"]), "generators")
    add("VAL4342_curved_operator", "curved Ricci-corrected operator row exists", any("Ricci" in row["name"] or "Ric" in row["operator_equation"] for row in tables["generators"]), "generators")
    add("VAL4342_CRI_flat_zero", "C_RI flat zero bound exists", any(row["quantity"] == "C_RI^flat" and "0" in row["formula"] for row in tables["bounds"]), "bounds")
    add("VAL4342_CDeltaK_kernel", "C_DeltaKdiv kernel zero bound exists", any(row["bound_id"] == "BND4342_2_CDeltaKdiv_kernel" for row in tables["bounds"]), "bounds")
    add("VAL4342_Kperp_finite", "finite Kperp fallback exists", any("Kperp" in row["quantity"] or "K_perp" in row["formula"] for row in tables["bounds"]), "bounds")
    add("VAL4342_firewall_Kperp", "Kperp divergence-free shortcut is blocked", any("divergence-free Kperp" in row["forbidden_shortcut"] for row in tables["firewall"]), "firewall")
    add("VAL4342_parent_still_missing", "parent action signature remains missing", any(row["symbol"].startswith("S_RI") and row["status"] == "MISSING_PARENT_ACTION_SIGNATURE" for row in tables["inputs"]), "inputs")
    add("VAL4342_no_claim_flags", "all valid_for_claim flags false", all(row.get("valid_for_claim", "False") == "False" for table in tables.values() for row in table if "valid_for_claim" in row), "all_tables")
    add("VAL4342_current_runner_nonclaim", "current runner keeps claim false", any(row["runner_id"] == "RUN4342_0_current" and "KEEP_CLAIM_FALSE" in row["action"] for row in tables["runner"]), "runner")
    add("VAL4342_next_target", "next target is 4343 parent owner or Kperp bound", any("4343" in row["next_target"] and "Kperp" in row["next_target"] for row in tables["next"]), "next")
    add("VAL4342_docs_exist", "formal and post docs exist", FORMAL_PATH.exists() and DOC_PATH.exists(), "docs")
    add("VAL4342_formal_marker", "formal marker exists", MARKER in read_text(FORMAL_PATH), "formal")
    add("VAL4342_post_handoff", "post doc contains handoff", NEXT_TARGET in read_text(DOC_PATH), "post")
    add("VAL4342_claim_row", f"{CLAIM_ID} claim-register row exists", CLAIM_ID in read_text(FORMAL / "02-claims-register.csv"), "claims")
    add("VAL4342_spine_marker", "spine marker exists", MARKER in read_text(FORMAL / "07-unification-spine.md"), "spine")
    add("VAL4342_packet_marker", "packet marker exists", PACKET_MARKER in read_text(FORMAL / "180-PPC4161-private-local-packet-integration.md"), "packet")

    for key, path in paths.items():
        if key == "validation":
            continue
        try:
            with path.open(newline="", encoding="utf-8") as handle:
                list(csv.DictReader(handle))
            parsed = True
        except Exception:
            parsed = False
        add(f"VAL4342_csv_parse_{key}", f"{key} CSV parses", parsed, str(path))

    return rows


def main() -> None:
    paths = {
        "sources": SOURCE_DIR / "P8_Y5_R2FR_4342_SOURCE_REGISTER.csv",
        "generators": SOURCE_DIR / "P8_Y5_R2FR_4342_KGAMMA_GENERATOR_ROWS.csv",
        "proofs": SOURCE_DIR / "P8_Y5_R2FR_4342_PROOF_ROWS.csv",
        "bounds": SOURCE_DIR / "P8_Y5_R2FR_4342_BOUND_ROWS.csv",
        "inputs": SOURCE_DIR / "P8_Y5_R2FR_4342_REQUIRED_INPUTS.csv",
        "branches": SOURCE_DIR / "P8_Y5_R2FR_4342_BRANCH_RUNNER.csv",
        "runner": SOURCE_DIR / "P8_Y5_R2FR_4342_RUNNER.csv",
        "firewall": SOURCE_DIR / "P8_Y5_R2FR_4342_CLAIM_FIREWALL.csv",
        "decision": SOURCE_DIR / "P8_Y5_R2FR_4342_DECISION.csv",
        "status": SOURCE_DIR / "P8_Y5_R2FR_4342_STATUS.csv",
        "next": SOURCE_DIR / "P8_Y5_R2FR_4342_NEXT_TARGET.csv",
        "validation": VALIDATION_PATH,
    }
    tables = {
        "sources": source_rows(),
        "generators": generator_rows(),
        "proofs": proof_rows(),
        "bounds": bound_rows(),
        "inputs": input_rows(),
        "branches": branch_rows(),
        "runner": runner_rows(),
        "firewall": firewall_rows(),
        "decision": decision_rows(),
        "status": status_rows(),
        "next": next_rows(),
    }
    for key, rows in tables.items():
        write_csv(paths[key], rows)
    write_docs(tables)
    append_claim_once()
    append_once(
        FORMAL / "07-unification-spine.md",
        MARKER,
        f"""
## PPC4161 4342 K_L generator for KGamma

Marker: `{MARKER}`

4342 constructs the Khat right-inverse route from the existing `K_L` longitudinal generator:

```text
Box A_Gamma^nu = -partial^nu Gamma_eff
K_Gamma = K_L[A_Gamma]
partial_mu K_Gamma^(mu nu)=partial^nu Gamma_eff.
```

This gives `C_RI^flat=0` on a fixed flat local patch. The curved branch uses the Ricci-corrected operator `(Box delta+Ric)A=-nabla Gamma` and keeps commutator/boundary tails. `C_DeltaK_div` is reduced to the preserved `K_perp` co-closed kernel, or to a finite Kperp source-pack score.
""",
    )
    append_once(
        FORMAL / "180-PPC4161-private-local-packet-integration.md",
        PACKET_MARKER,
        f"""
## 4342 packet K_L generator for KGamma

Marker: `{PACKET_MARKER}`

Packet update: the right-inverse is now constructive. `K_Gamma` is generated by the same `K_L` longitudinal owner used in the local PPN tensor ansatz. The next fight is no longer "does a right-inverse exist?" but whether the parent action owns it without hidden metric stress, and whether `K_perp` is GR/gauge/boundary or a finite extra source row.
""",
    )
    validation = validation_rows(paths, tables)
    write_csv(paths["validation"], validation)
    failed = [row for row in validation if row["passed"] != "True"]
    print(f"{CHECKPOINT}: wrote {len(tables)} csv artifacts plus validation")
    print(f"{CHECKPOINT}: validation rows={len(validation)} failed={len(failed)}")
    if failed:
        for row in failed:
            print(f"FAILED {row['check_id']}: {row['description']} :: {row['evidence']}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
