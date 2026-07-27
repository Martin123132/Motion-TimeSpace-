from __future__ import annotations

import csv
import py_compile
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Iterable, List, Tuple


ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
SOURCE_DIR = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = PROJECT / "formalization-workbench"
SCRIPT_PATH = Path(__file__).resolve()
DOC_PATH = ROOT / "4137-Y5-R2FR-GK-q-loc-special-action-or-profile-bound.md"

TIMESTAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
BRANCH_ID = "MTS_R2FR_Y5_GK_QLOC_SPECIAL_ACTION_OR_PROFILE_BOUND_4137"
CHECKPOINT_ID = "4137"
DECISION = "GK_QLOC_RESPONSE_BRANCH_PROVED_CURRENT_BRANCH_RETAINS_DELTAK_PROFILE_BOUND"


LOCAL_SOURCES: Dict[str, Tuple[Path, str, str]] = {
    "SRC4137_00_4136_next": (
        SOURCE_DIR / "P8_Y5_R2FR_4136_NEXT_TARGET.csv",
        "4137-Y5-R2FR-GK-q-loc-special-action-or-profile-bound.md",
        "4136 selected GK/q_loc special action-or-profile fork.",
    ),
    "SRC4137_01_4136_status": (
        SOURCE_DIR / "P8_Y5_R2FR_4136_STATUS.csv",
        "LOCAL_NORMAL_FORM_COMPATIBLE_BUT_NOT_PARENT_ADOPTED_COEFFICIENT_EXTRACTOR_EMITTED",
        "4136 local normal-form status.",
    ),
    "SRC4137_02_4136_refusal": (
        SOURCE_DIR / "P8_Y5_R2FR_4136_REFUSAL_TERMS.csv",
        "R_GK_q_loc",
        "4136 refusal term for GK/q_loc.",
    ),
    "SRC4137_03_513_decision": (
        SOURCE_DIR / "P8_GAMMA_KHAT_QLOC_DECISION.csv",
        "D513_1",
        "Original GK/q_loc variational-stress route decision.",
    ),
    "SRC4137_04_513_contract": (
        SOURCE_DIR / "P8_GAMMA_KHAT_QLOC_FIRST_VARIATION_CONTRACT.csv",
        "GK513_0_action_existence",
        "First-variation contract for GK/q_loc zero route.",
    ),
    "SRC4137_05_513_integrability": (
        SOURCE_DIR / "P8_GAMMA_KHAT_QLOC_INTEGRABILITY_GATES.csv",
        "IG513_2_metric_variationality",
        "Integrability gates for GK/q_loc.",
    ),
    "SRC4137_06_513_stress": (
        SOURCE_DIR / "P8_GAMMA_KHAT_QLOC_STRESS_REWRITE.csv",
        "SR513_2_variational_route",
        "Stress rewrite and Ward route.",
    ),
    "SRC4137_07_513_demote": (
        SOURCE_DIR / "P8_GAMMA_KHAT_QLOC_RESIDUAL_OR_DEMOTION.csv",
        "QR513_0_nonvariational_stress",
        "Demotion/fallback ledger.",
    ),
    "SRC4137_08_4023_action": (
        SOURCE_DIR / "P8_Y5_R2FR_4023_CANONICAL_SGK_ACTION_ATTEMPT.csv",
        "SGK4023_1_action",
        "Canonical S_GK action attempt.",
    ),
    "SRC4137_09_4023_identity": (
        SOURCE_DIR / "P8_Y5_R2FR_4023_QLOC_STRESS_IDENTITY.csv",
        "ID4023_3_mismatch",
        "q_loc stress identity and D_GK mismatch.",
    ),
    "SRC4137_10_4023_fork": (
        SOURCE_DIR / "P8_Y5_R2FR_4023_QLOC_ZERO_THEOREM_OR_BOUND_FORK.csv",
        "FORK4023_1_mismatch_bound",
        "Zero theorem or mismatch bound fork.",
    ),
    "SRC4137_11_4024_match": (
        SOURCE_DIR / "P8_Y5_R2FR_4024_GK_SYMBOL_MATCH_MATRIX.csv",
        "SM4024_6_current_verdict",
        "GK symbol-match matrix.",
    ),
    "SRC4137_12_4025_owner": (
        SOURCE_DIR / "P8_Y5_R2FR_4025_RESPONSE_FIELD_OWNER_CONTRACT.csv",
        "OWN4025_3_stress_identity",
        "Response-field owner contract.",
    ),
    "SRC4137_13_4025_theorem": (
        SOURCE_DIR / "P8_Y5_R2FR_4025_METRIC_RESPONSE_THEOREM.csv",
        "THM4025_0_metric_response",
        "Metric-response theorem.",
    ),
    "SRC4137_14_4026_density": (
        SOURCE_DIR / "P8_Y5_R2FR_4026_EXPLICIT_GAMMA_DENSITY_CANDIDATE.csv",
        "Gamma_quad",
        "Explicit Gamma density candidate.",
    ),
    "SRC4137_15_4026_components": (
        SOURCE_DIR / "P8_Y5_R2FR_4026_DGK_PROFILE_INPUT_ROWS.csv",
        "DGK4026_6_C_beta_C_R10",
        "D_GK profile input rows.",
    ),
    "SRC4137_16_4027_gate": (
        SOURCE_DIR / "P8_Y5_R2FR_4027_KHAT_COMPONENT_COMPLETION_GATE.csv",
        "KCG4027_0_tracefree_improvement",
        "Khat component completion gate.",
    ),
    "SRC4137_17_4027_norms": (
        SOURCE_DIR / "P8_Y5_R2FR_4027_DGK_BOUND_NORMALIZATION_ROWS.csv",
        "NORM4027_5_observable_maps",
        "D_GK bound normalization rows.",
    ),
    "SRC4137_18_3952_deltaK": (
        SOURCE_DIR / "P8_Y5_R2FR_3952_DELTAK_QLOC_BOUND.csv",
        "DKB3952_2_q_loc_norm_bound",
        "Delta_K q_loc bound.",
    ),
    "SRC4137_19_3952_helmholtz": (
        SOURCE_DIR / "P8_Y5_R2FR_3952_HELMHOLTZ_KHAT_TEST.csv",
        "HKT3952_6_verdict",
        "Helmholtz Khat test verdict.",
    ),
    "SRC4137_20_script": (
        SCRIPT_PATH,
        "Y5_R2FR_4137_GK_q_loc_special_action_or_profile_bound.py",
        "Reproducible generator for this 4137 checkpoint.",
    ),
}


def row_base() -> dict:
    return {"timestamp_utc": TIMESTAMP, "branch_id": BRANCH_ID, "checkpoint_id": CHECKPOINT_ID}


def write_csv(path: Path, rows: List[dict]) -> None:
    if not rows:
        raise ValueError(f"refusing to write empty csv: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fields: List[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def parse_csv(path: Path) -> List[dict]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def contains(path: Path, needle: str) -> bool:
    if not path.exists():
        return False
    return needle in path.read_text(encoding="utf-8", errors="replace")


def is_under(path: Path, parent: Path) -> bool:
    try:
        path.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


def source_register() -> List[dict]:
    rows: List[dict] = []
    for source_id, (path, needle, role) in LOCAL_SOURCES.items():
        row = row_base()
        row.update(
            {
                "source_id": source_id,
                "source_path": str(path),
                "exists": str(path.exists()),
                "needle": needle,
                "needle_found": str(contains(path, needle)),
                "role": role,
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
        rows.append(row)
    return rows


def action_fork_rows() -> List[dict]:
    data = [
        (
            "AF4137_0_identity",
            "stress-divergence identity",
            "T_GK^{mu nu}:=Gamma_eff g_obs^{mu nu}-Khat^{mu nu}; q_loc^nu=P_loc nabla_mu T_GK^{mu nu}",
            "exact algebraic reclassification of q_loc as projected stress divergence",
            "EXACT_IDENTITY",
        ),
        (
            "AF4137_1_response_branch",
            "response-defined action branch",
            "If I_Gamma=int sqrt|g| Gamma_eff and Khat=K_Gamma:=-2E_g[Gamma_eff], then S_GK=-I_Gamma gives T_GK=Gamma_eff g-Khat",
            "mixed variations give Helmholtz integrability automatically for the response-defined branch",
            "DERIVED_FOR_CONSTRUCTED_BRANCH",
        ),
        (
            "AF4137_2_Ward_zero",
            "conditional Ward zero",
            "nabla_mu T_GK^{mu nu}=E_A nabla^nu Y^A + boundary/improvement; E_A=0 plus parent P_loc and no-flux gives q_loc=0",
            "this is the clean no-plateau route when the parent action owns the sector",
            "CONDITIONAL_ZERO_THEOREM",
        ),
        (
            "AF4137_3_current_branch",
            "current MTS branch",
            "Khat_current = K_Gamma + Delta_K; q_loc = -P_loc(E_A nablaY + R_boundary + R_source + nabla_mu Delta_K^{mu nu})",
            "current Khat/Gamma component match fails, so Delta_K/D_GK remains live",
            "CURRENT_BRANCH_BOUND_ONLY",
        ),
        (
            "AF4137_4_demote_if_no_action",
            "nonvariational fallback",
            "If no S_GK or Helmholtz-zero Khat exists, Gamma/Khat/q_loc is closure bookkeeping and must be bounded as a retained operator",
            "prevents a nonvariational tensor from being sold as a Ward identity",
            "DEMOTION_GUARD",
        ),
    ]
    rows: List[dict] = []
    for fork_id, branch, formula, meaning, status in data:
        row = row_base()
        row.update(
            {
                "fork_id": fork_id,
                "branch": branch,
                "formula": formula,
                "meaning": meaning,
                "status": status,
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
        rows.append(row)
    return rows


def zero_gate_rows() -> List[dict]:
    data = [
        (
            "ZG4137_0_action_existence",
            "S_GK action existence",
            "actual corpus supplies local diffeomorphism-invariant S_GK with T_GK=-2/sqrt|g| delta S_GK/delta g",
            "candidate S_can/I_Gamma exists; current MTS action not adopted",
            "FAIL_CURRENT_BRANCH",
        ),
        (
            "ZG4137_1_metric_response",
            "Khat metric response",
            "Khat_current=K_Gamma plus boundary-silent improvement, with K_Gamma=-2E_g[Gamma_eff]",
            "Gamma_quad candidate exists, but full Khat response components are missing/unsigned",
            "FAIL_CURRENT_BRANCH_DELTAK_LIVE",
        ),
        (
            "ZG4137_2_Helmholtz",
            "Helmholtz/integrability",
            "H_GK[Khat_current]=0 modulo boundary exact terms",
            "proved for response-defined K_metric branch; not passed for current Khat except as Delta_K obstruction",
            "PASS_CONSTRUCTED_BRANCH_ONLY",
        ),
        (
            "ZG4137_3_Euler",
            "Euler/source-free closure",
            "carrier fields obey E_A=0 in compact local vacuum",
            "no-hair/sign/source-silence not parent-signed for actual carrier fields",
            "UNSIGNED_EULER_FORCING",
        ),
        (
            "ZG4137_4_double_zero",
            "fixed-point double zero",
            "T_GK(Y0)=0 and partial_A T_GK(Y0)=0",
            "true for quadratic candidate if coefficients/signs adopted; actual Gamma/Khat expansion not signed",
            "UNSIGNED_FIXED_POINT",
        ),
        (
            "ZG4137_5_projector",
            "P_loc parent ownership",
            "P_loc=P_parent(Phi0), commutes with readout/fixed-point limit and cannot hide force components",
            "projector gates remain open",
            "UNSIGNED_PROJECTOR",
        ),
        (
            "ZG4137_6_boundary",
            "boundary/no-flux",
            "theta_GK/improvement flux is zero or fixed topological subtraction on linking surfaces",
            "compact-shell proxy exists but is not mapped to PPN/R10/source units",
            "UNSIGNED_BOUNDARY_OR_UNMAPPED_PROXY",
        ),
    ]
    rows: List[dict] = []
    for gate_id, gate, requirement, current_evidence, verdict in data:
        row = row_base()
        row.update(
            {
                "gate_id": gate_id,
                "gate": gate,
                "requirement": requirement,
                "current_evidence": current_evidence,
                "verdict": verdict,
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
        rows.append(row)
    return rows


def profile_bound_rows() -> List[dict]:
    data = [
        (
            "PB4137_0_master",
            "Q_loc_envelope",
            "Q_loc <= C_Ploc*(A_DGK/L_DGK + A_Euler/L_Euler + A_boundary/L_boundary)",
            "projected q_loc units; must be normalized to EH/source units",
            "delta_beta_q_loc; alpha_q(lambda); source-exchange",
            "C_Ploc,A_DGK,L_DGK,A_Euler,L_Euler,A_boundary,L_boundary",
        ),
        (
            "PB4137_1_trace",
            "D_trace_potential",
            "A_trace/L_trace from unowned trace/potential/vacuum-subtraction response",
            "stress-divergence units",
            "beta/gamma source tail",
            "Gamma0 subtraction, mass trace ownership, A_trace,L_trace",
        ),
        (
            "PB4137_2_A_grad",
            "D_A_grad",
            "A_Agrad/L_A from full A-gradient response minus partial Khat shape",
            "stress-divergence units; Z_A normalized",
            "preferred-frame/q_loc tail",
            "trace-free improvement sign, A_Agrad,L_A, boundary convention",
        ),
        (
            "PB4137_3_gamma",
            "D_gamma_grad",
            "A_gamma/L_gamma from scalar gamma-gradient response not matched by live Khat",
            "stress-divergence units; Z_G normalized",
            "R10 scalar-profile map; beta/gamma",
            "Z_G, gamma amplitude, L_gamma",
        ),
        (
            "PB4137_4_cross",
            "D_cross_AG",
            "A_cross/L_cross from c_AG A^mu nabla_mu gamma response mismatch",
            "stress-divergence units",
            "local source-exchange; R10/PPN cross tail",
            "c_AG sign/normalization, cross profile",
        ),
        (
            "PB4137_5_mass",
            "D_mass_gap",
            "A_mass/L_mass from m_A^2 A_mu A_nu and m_G^2 gamma^2 response mismatch",
            "stress-divergence units",
            "nohair/leakage envelope",
            "m_A,m_G, parent scale, profile amplitudes",
        ),
        (
            "PB4137_6_boundary",
            "D_boundary_improvement",
            "A_boundary_proxy=7.432631961576971e-06 only after unit/projector map",
            "currently dimensionless proxy, not PPN units",
            "alpha3; GM drift; beta/gamma boundary tail",
            "C_boundary_to_beta, C_boundary_to_R10, source-measure frame",
        ),
        (
            "PB4137_7_Euler",
            "A_Euler/L_Euler",
            "sum_A |E_A||nablaY^A| plus response-carrier source forcing",
            "force-density/source-exchange units",
            "fifth-force/source-normalization residual",
            "Euler residual, no-hair constants, field-gradient scale",
        ),
    ]
    rows: List[dict] = []
    for bound_id, component, formula, units, observable_map, required_inputs in data:
        row = row_base()
        row.update(
            {
                "bound_id": bound_id,
                "component": component,
                "formula": formula,
                "units": units,
                "observable_map": observable_map,
                "required_inputs": required_inputs,
                "status": "PROFILE_BOUND_ROW_READY_NONNUMERIC",
                "score_ready": "False",
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
        rows.append(row)
    return rows


def projection_rows() -> List[dict]:
    data = [
        (
            "PR4137_0_beta",
            "C_beta_qloc",
            "delta_beta_q_loc = C_beta_qloc * Q_loc_envelope",
            "dimensionless PPN beta",
            "derive weak-field metric solution sourced by q_loc and extract U^2 coefficient",
            "first local-PPN priority if action route fails",
        ),
        (
            "PR4137_1_R10",
            "C_R10_qloc(lambda)",
            "alpha_q(lambda)=C_R10_qloc(lambda)*Q_loc_envelope",
            "dimensionless alpha(lambda)",
            "derive finite-range/Yukawa or non-Yukawa profile from q_loc source",
            "short-range/fifth-force fallback",
        ),
        (
            "PR4137_2_alpha3",
            "C_alpha3_qloc",
            "alpha3_q = C_alpha3_qloc * A_boundary_or_flux",
            "dimensionless preferred-frame parameter",
            "map momentum/flux leakage into alpha3-style preferred-frame rows",
            "boundary/flux pressure test",
        ),
        (
            "PR4137_3_Gdot",
            "C_Gdot_qloc",
            "dln M_eff/dt or dln mu_obs/dt = C_Gdot_qloc * q_loc_time",
            "yr^-1 or source-normalized time derivative",
            "project time component into measured-GM drift/source normalization",
            "coupling/source stability check",
        ),
        (
            "PR4137_4_source",
            "C_source_qloc",
            "epsilon_source_q = C_source_qloc * Q_loc_envelope",
            "dimensionless source-denominator residual",
            "map q_loc to active/passive/Hilbert/source-denominator mismatch",
            "Newton/source coupling guard",
        ),
    ]
    rows: List[dict] = []
    for projection_id, symbol, formula, units, required_derivation, priority in data:
        row = row_base()
        row.update(
            {
                "projection_id": projection_id,
                "symbol": symbol,
                "formula": formula,
                "units": units,
                "required_derivation": required_derivation,
                "priority": priority,
                "status": "PROJECTION_REQUIRED_NOT_FILLED",
                "score_ready": "False",
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
        rows.append(row)
    return rows


def decision_rows() -> List[dict]:
    data = [
        (
            "DG4137_0_real_derivation",
            "RESPONSE_BRANCH_PROVED",
            "If Khat is defined as the metric response of a covariant Gamma density, the Helmholtz/action branch is real and the Ward zero follows under Euler/projector/boundary silence.",
            "keep this as the clean derivation route",
        ),
        (
            "DG4137_1_current_branch",
            "CURRENT_BRANCH_NOT_PROMOTED",
            "Actual MTS Khat/Gamma does not yet match the response branch; Delta_K/D_GK remains live.",
            "no q_loc zero or local-GR claim",
        ),
        (
            "DG4137_2_bound",
            "QLOC_PROFILE_BOUND_EMITTED",
            "The fallback is now an explicit D_GK/Euler/boundary profile bound with PPN/R10/source projection requirements.",
            "use bound rows if response match fails",
        ),
        (
            "DG4137_3_next",
            "NEXT_TRACEFREE_KHAT_IMPROVEMENT_SELECTED",
            "The nearest derivation target is the trace-free Khat improvement because it has a concrete algebraic shape match and was ranked first by 4027.",
            "4138-Y5-R2FR-tracefree-Khat-improvement-sign-or-beta-projection-bound.md",
        ),
        (
            "DG4137_4_claim_ceiling",
            "NO_LOCAL_GR_CLAIM",
            "Response-defined branch proof is not the current corpus proof; current branch remains nonclaim.",
            "keep all claim flags false",
        ),
    ]
    rows: List[dict] = []
    for gate_id, decision, rationale, next_action in data:
        row = row_base()
        row.update(
            {
                "gate_id": gate_id,
                "decision": decision,
                "rationale": rationale,
                "next_action": next_action,
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
        rows.append(row)
    return rows


def status_rows() -> List[dict]:
    row = row_base()
    row.update(
        {
            "status_id": "STATUS4137_0",
            "result": DECISION,
            "summary": (
                "4137 proves the clean response-defined GK/q_loc branch but does not promote the current MTS branch. "
                "If Khat is the metric response of a covariant Gamma density, Helmholtz/action ownership is automatic "
                "and Ward identity gives q_loc=0 under Euler/projector/boundary silence. Current MTS still has "
                "Delta_K/D_GK mismatch, missing Khat response components, unmapped boundary proxy, and missing PPN/R10 "
                "projection coefficients, so the profile-bound branch is emitted."
            ),
            "response_branch_proved": "True",
            "current_branch_q_loc_zero_signed": "False",
            "profile_bound_emitted": "True",
            "score_ready": "False",
            "claim_state": "no local_GR, Newton, PPN, R10, Gdot, clock, EM prediction, Maxwell derivation, alpha derivation, or source-normalization pass",
            "next_target": "4138 tracefree Khat improvement sign or beta projection bound",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    )
    return [row]


def next_target_rows() -> List[dict]:
    row = row_base()
    row.update(
        {
            "next_id": "NEXT4137_0",
            "target_doc": "4138-Y5-R2FR-tracefree-Khat-improvement-sign-or-beta-projection-bound.md",
            "target_script": "scripts/Y5_R2FR_4138_tracefree_Khat_improvement_sign_or_beta_projection_bound.py",
            "objective": (
                "try to sign the trace-free Khat improvement component K_L^{mu nu}=2[nabla^mu nabla^nu phi-(1/4)g^{mu nu}Box phi] "
                "as a parent-owned boundary-silent metric response; if unsigned, fill the first beta-priority D_A_grad/C_beta_qloc bound row"
            ),
            "success_gate": "trace-free Khat improvement parent-signed, or D_A_grad and C_beta_qloc have source-backed units, normalization and PPN projection rows",
            "reason": "4137 isolates Delta_K/D_GK as the live GK/q_loc obstruction; 4027 ranked trace-free improvement as the least-scrutiny completion route.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    )
    return [row]


def output_paths() -> Dict[str, Path]:
    return {
        "P8_Y5_R2FR_4137_SOURCE_REGISTER": SOURCE_DIR / "P8_Y5_R2FR_4137_SOURCE_REGISTER.csv",
        "P8_Y5_R2FR_4137_ACTION_FORK": SOURCE_DIR / "P8_Y5_R2FR_4137_ACTION_FORK.csv",
        "P8_Y5_R2FR_4137_ZERO_GATES": SOURCE_DIR / "P8_Y5_R2FR_4137_ZERO_GATES.csv",
        "P8_Y5_R2FR_4137_QLOC_PROFILE_BOUND_ROWS": SOURCE_DIR / "P8_Y5_R2FR_4137_QLOC_PROFILE_BOUND_ROWS.csv",
        "P8_Y5_R2FR_4137_PROJECTION_REQUIREMENTS": SOURCE_DIR / "P8_Y5_R2FR_4137_PROJECTION_REQUIREMENTS.csv",
        "P8_Y5_R2FR_4137_DECISION_GATES": SOURCE_DIR / "P8_Y5_R2FR_4137_DECISION_GATES.csv",
        "P8_Y5_R2FR_4137_STATUS": SOURCE_DIR / "P8_Y5_R2FR_4137_STATUS.csv",
        "P8_Y5_R2FR_4137_NEXT_TARGET": SOURCE_DIR / "P8_Y5_R2FR_4137_NEXT_TARGET.csv",
    }


def write_doc(outputs: Dict[str, Path]) -> None:
    status = status_rows()[0]
    sections = [
        "# 4137 - GK/q_loc Special Action or Profile Bound",
        "",
        "## Verdict",
        "",
        f"- Decision: `{DECISION}`.",
        "- The response-defined branch is a real derivation route.",
        "- The current MTS branch is not promoted because `Delta_K/D_GK` is still live.",
        "- The fallback is now an explicit `q_loc` profile-bound interface.",
        "",
        "## Generated Outputs",
        "",
    ]
    for name, path in outputs.items():
        sections.append(f"- `{name}`: `{path}`")
    sections.extend(["", "## Action Fork", "", "| branch | status | formula |", "|---|---|---|"])
    for row in action_fork_rows():
        sections.append(f"| {row['branch']} | {row['status']} | {row['formula']} |")
    sections.extend(["", "## Zero Gates", "", "| gate | verdict | current evidence |", "|---|---|---|"])
    for row in zero_gate_rows():
        sections.append(f"| {row['gate']} | {row['verdict']} | {row['current_evidence']} |")
    sections.extend(["", "## Profile Bound", "", "| component | status | observable map |", "|---|---|---|"])
    for row in profile_bound_rows():
        sections.append(f"| {row['component']} | {row['status']} | {row['observable_map']} |")
    sections.extend(
        [
            "",
            "## Current Meaning",
            "",
            "- We have not smuggled a plateau: `q_loc=0` only follows on the response-defined action branch with Euler, projector and boundary gates signed.",
            "- Current MTS has a useful but unsigned `Gamma_quad` candidate; missing Khat response components remain `D_GK` profile inputs.",
            "- The next best derivation is trace-free Khat improvement signing; the fallback is the first `C_beta_qloc` projection row.",
            "",
            "## Claim Ceiling",
            "",
            f"- {status['claim_state']}.",
            "- Response-branch proof is not current-branch proof.",
            "",
            "## Next Target",
            "",
            "- `4138-Y5-R2FR-tracefree-Khat-improvement-sign-or-beta-projection-bound.md`",
            "",
        ]
    )
    DOC_PATH.write_text("\n".join(sections), encoding="utf-8")


def write_outputs() -> Dict[str, Path]:
    outputs = output_paths()
    writers = {
        "P8_Y5_R2FR_4137_SOURCE_REGISTER": source_register,
        "P8_Y5_R2FR_4137_ACTION_FORK": action_fork_rows,
        "P8_Y5_R2FR_4137_ZERO_GATES": zero_gate_rows,
        "P8_Y5_R2FR_4137_QLOC_PROFILE_BOUND_ROWS": profile_bound_rows,
        "P8_Y5_R2FR_4137_PROJECTION_REQUIREMENTS": projection_rows,
        "P8_Y5_R2FR_4137_DECISION_GATES": decision_rows,
        "P8_Y5_R2FR_4137_STATUS": status_rows,
        "P8_Y5_R2FR_4137_NEXT_TARGET": next_target_rows,
    }
    for key, writer in writers.items():
        write_csv(outputs[key], writer())
    write_doc(outputs)
    return outputs


def flatten_rows(paths: Iterable[Path]) -> str:
    parts: List[str] = []
    for path in paths:
        for row in parse_csv(path):
            parts.append(" ".join(str(value) for value in row.values()))
    return " ".join(parts)


def validate(outputs: Dict[str, Path]) -> List[dict]:
    checks: List[dict] = []

    def add(check_id: str, description: str, passed: bool, detail: str) -> None:
        row = row_base()
        row.update({"check_id": check_id, "description": description, "passed": str(bool(passed)), "detail": detail})
        checks.append(row)

    sources = source_register()
    add(
        "VAL4137_0_sources",
        "all cited local source paths exist and contain required needles",
        all(row["exists"] == "True" and row["needle_found"] == "True" for row in sources),
        "; ".join(f"{row['source_id']}={row['exists']}/{row['needle_found']}" for row in sources),
    )
    add(
        "VAL4137_1_doc",
        "checkpoint markdown exists and names decision",
        DOC_PATH.exists() and DECISION in DOC_PATH.read_text(encoding="utf-8"),
        str(DOC_PATH),
    )

    parse_ok = True
    parse_counts: Dict[str, object] = {}
    for key, path in outputs.items():
        try:
            rows = parse_csv(path)
            parse_counts[key] = len(rows)
            parse_ok = parse_ok and len(rows) > 0
        except Exception as exc:
            parse_ok = False
            parse_counts[key] = repr(exc)
    add("VAL4137_2_csv_parse", "all generated CSV outputs parse and are nonempty", parse_ok, str(parse_counts))

    fork_text = flatten_rows([outputs["P8_Y5_R2FR_4137_ACTION_FORK"]])
    fork_ok = all(
        token in fork_text
        for token in ["T_GK", "q_loc^nu=P_loc", "Khat=K_Gamma", "Delta_K", "DEMOTION_GUARD"]
    )
    add("VAL4137_3_action_fork", "action fork contains identity, response branch, current DeltaK branch and demotion guard", fork_ok, "fork tokens checked")

    gate_text = flatten_rows([outputs["P8_Y5_R2FR_4137_ZERO_GATES"]])
    gate_ok = all(
        token in gate_text
        for token in [
            "S_GK action existence",
            "Khat metric response",
            "Helmholtz/integrability",
            "Euler/source-free closure",
            "fixed-point double zero",
            "P_loc parent ownership",
            "boundary/no-flux",
        ]
    )
    add("VAL4137_4_zero_gates", "zero gates cover action, response, Helmholtz, Euler, double-zero, projector and boundary", gate_ok, "gate tokens checked")

    bound_text = flatten_rows([outputs["P8_Y5_R2FR_4137_QLOC_PROFILE_BOUND_ROWS"]])
    bound_ok = all(
        token in bound_text
        for token in [
            "Q_loc_envelope",
            "D_trace_potential",
            "D_A_grad",
            "D_gamma_grad",
            "D_cross_AG",
            "D_mass_gap",
            "D_boundary_improvement",
            "A_Euler/L_Euler",
        ]
    )
    add("VAL4137_5_profile_bounds", "profile bound rows include all D_GK/Euler/boundary components", bound_ok, "bound tokens checked")

    projection_text = flatten_rows([outputs["P8_Y5_R2FR_4137_PROJECTION_REQUIREMENTS"]])
    projection_ok = all(
        token in projection_text
        for token in ["C_beta_qloc", "C_R10_qloc(lambda)", "C_alpha3_qloc", "C_Gdot_qloc", "C_source_qloc"]
    )
    add("VAL4137_6_projections", "projection requirements cover beta, R10, alpha3, Gdot and source coupling", projection_ok, "projection tokens checked")

    decision_text = flatten_rows([outputs["P8_Y5_R2FR_4137_DECISION_GATES"]])
    decision_ok = all(
        token in decision_text
        for token in [
            "RESPONSE_BRANCH_PROVED",
            "CURRENT_BRANCH_NOT_PROMOTED",
            "QLOC_PROFILE_BOUND_EMITTED",
            "NEXT_TRACEFREE_KHAT_IMPROVEMENT_SELECTED",
            "NO_LOCAL_GR_CLAIM",
        ]
    )
    add("VAL4137_7_decisions", "decision gates record proof, non-promotion, bound branch, next target and no-claim", decision_ok, "decision tokens checked")

    status = parse_csv(outputs["P8_Y5_R2FR_4137_STATUS"])
    status_ok = (
        bool(status)
        and status[0].get("result") == DECISION
        and status[0].get("response_branch_proved") == "True"
        and status[0].get("current_branch_q_loc_zero_signed") == "False"
        and status[0].get("profile_bound_emitted") == "True"
    )
    add("VAL4137_8_status", "status records response proof, unsigned current zero and emitted profile bound", status_ok, "status row checked")

    nxt = parse_csv(outputs["P8_Y5_R2FR_4137_NEXT_TARGET"])
    next_ok = len(nxt) == 1 and nxt[0].get("target_doc") == "4138-Y5-R2FR-tracefree-Khat-improvement-sign-or-beta-projection-bound.md"
    add("VAL4137_9_next_target", "next target is trace-free Khat improvement sign or beta projection bound", next_ok, str(nxt))

    all_rows: List[dict] = []
    for path in outputs.values():
        all_rows.extend(parse_csv(path))
    no_claim = all(row.get("claim_allowed") in ("False", "") and row.get("valid_for_claim") in ("False", "") for row in all_rows)
    add("VAL4137_10_no_claim_flags", "all generated rows remain no-claim and invalid for claim", no_claim, f"row_count={len(all_rows)}")

    output_paths_all = list(outputs.values()) + [DOC_PATH]
    in_scope = all(is_under(path, ROOT) for path in output_paths_all)
    formalization_output = any(is_under(path, FORMALIZATION) for path in output_paths_all)
    formalization_touched = False
    if FORMALIZATION.exists():
        formalization_touched = any(FORMALIZATION.rglob("*R2FR_4137*")) or any(FORMALIZATION.rglob("4137-Y5-R2FR*"))
    add(
        "VAL4137_11_scope",
        "outputs stay in post-checkpoint-work and not formalization-workbench",
        in_scope and not formalization_output and not formalization_touched,
        f"doc={DOC_PATH}; csv_count={len(outputs)}",
    )

    compile_ok = True
    compile_detail = "py_compile ok"
    try:
        py_compile.compile(str(SCRIPT_PATH), doraise=True)
    except Exception as exc:
        compile_ok = False
        compile_detail = repr(exc)
    add("VAL4137_12_compile", "generator script compiles", compile_ok, compile_detail)
    return checks


def main() -> None:
    outputs = write_outputs()
    validation_rows = validate(outputs)
    validation_path = SOURCE_DIR / "P8_Y5_BRR545_4137_VALIDATION.csv"
    write_csv(validation_path, validation_rows)
    pycache = SCRIPT_PATH.parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)

    failed = [row for row in validation_rows if row["passed"] != "True"]
    print(f"wrote: {DOC_PATH}")
    for path in outputs.values():
        print(f"wrote: {path}")
    print(f"validation: {validation_path}")
    if failed:
        print("failed checks:")
        for row in failed:
            print(f"- {row['check_id']}: {row['detail']}")
        raise SystemExit(1)
    print("all validation checks passed")


if __name__ == "__main__":
    main()
