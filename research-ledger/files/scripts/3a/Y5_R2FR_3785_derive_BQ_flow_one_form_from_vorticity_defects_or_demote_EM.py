import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


CHECKPOINT = "3785"
BRANCH = "MTS_R2FR_Y5_DERIVE_BQ_FLOW_ONE_FORM_FROM_VORTICITY_DEFECTS_OR_DEMOTE_EM_3785"
ROOT = Path(
    r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework"
    r"\Motion-TimeSpace--main"
)
PCW = ROOT / "post-checkpoint-work"
RESIDUALS = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "3785-Y5-R2FR-derive-BQ-flow-one-form-from-vorticity-defects-or-demote-EM.md"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_3785_SOURCE_REGISTER.csv",
    "clebsch_lemma": RESIDUALS / "P8_Y5_R2FR_3785_DARBOUX_CLEBSCH_BQ_LEMMA.csv",
    "candidate_tests": RESIDUALS / "P8_Y5_R2FR_3785_BQ_CANDIDATE_TESTS.csv",
    "berry_multiplet": RESIDUALS / "P8_Y5_R2FR_3785_BERRY_INTERNAL_MULTIPLET_ROUTE.csv",
    "poynting_vorticity": RESIDUALS / "P8_Y5_R2FR_3785_POYNTING_VORTICITY_DEFECT_AUDIT.csv",
    "rank_gates": RESIDUALS / "P8_Y5_R2FR_3785_RANK_AND_NO_SMUGGLE_GATES.csv",
    "finite_mode": RESIDUALS / "P8_Y5_R2FR_3785_EM_FINITE_BOUND_MODE_UPDATE.csv",
    "claim_gates": RESIDUALS / "P8_Y5_R2FR_3785_CLAIM_GATES.csv",
    "decisions": RESIDUALS / "P8_Y5_R2FR_3785_DECISION_ROWS.csv",
    "next_target": RESIDUALS / "P8_Y5_R2FR_3785_NEXT_TARGET.csv",
    "status": RESIDUALS / "P8_Y5_R2FR_3785_STATUS.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_3785_VALIDATION.csv",
}

SOURCE_PATHS = [
    PCW / "3784-Y5-R2FR-parent-U1-action-clause-or-EM-finite-bound-mode.md",
    PCW / "3783-Y5-R2FR-parent-U1-bundle-upgrade-or-PiQ-finite-bound-runner.md",
    PCW / "3782-Y5-R2FR-instantiate-PiQ-from-psi-phase-current-or-finite-EM-vector.md",
    PCW / "1056-Y5-R10-alpha-owner-from-vertical-generator-norm-or-topological-level.md",
    PCW / "1100-Y5-R10-parent-TQ-owner-fixed-charge-lattice-and-gauge-norm-signature.md",
    PCW / "1174-Y5-R10-local-Qflow-stationarity-theorem-or-first-Qflow-bound-row.md",
    PCW / "1859-Y5-R2FR-motion-load-phase-volume-parent-origin-no-GR-import-derivation.md",
    PCW / "00-martin-fork-heuristics-private.md",
    PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md",
]


def write_csv(path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    headers = sorted({key for row in rows for key in row})
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=headers)
        writer.writeheader()
        writer.writerows(rows)


def source_register(timestamp):
    return [
        {
            "timestamp_utc": timestamp,
            "checkpoint_id": CHECKPOINT,
            "branch_id": BRANCH,
            "source_path": str(path),
            "exists": path.exists(),
            "source_role": "BQ_flow_owner_context",
            "valid_for_claim": False,
        }
        for path in SOURCE_PATHS
    ]


def clebsch_lemma_rows(timestamp):
    return [
        {
            "timestamp_utc": timestamp,
            "lemma_id": "DCL3785_0_local_closed_two_form",
            "statement": "If the desired pre-EM curvature H_Q is a closed 2-form of locally constant rank, Darboux/Clebsch coordinates give H_Q=sum_i dC_i wedge dD_i locally.",
            "formula": "B_Q=sum_i C_i dD_i, so dB_Q=sum_i dC_i wedge dD_i=H_Q.",
            "payoff": "This is an exact local route to a nonzero dB_Q without defining B_Q from A_obs or F_obs.",
            "claim_status": "EXACT_MATH_CONDITIONAL_NOT_PARENT_OWNED",
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "lemma_id": "DCL3785_1_single_pair_rank_limit",
            "statement": "One Clebsch pair B_Q=C dD gives a simple 2-form H_Q=dC wedge dD.",
            "formula": "H_Q wedge H_Q=0 for one pair.",
            "payoff": "A single flow pair can model null/simple EM sectors but not a generic local Maxwell field with nonzero F wedge F.",
            "claim_status": "RANK_LIMIT_DERIVED",
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "lemma_id": "DCL3785_2_two_pair_generic_local",
            "statement": "Two Clebsch pairs can represent a generic rank-four local 2-form on a 4D patch.",
            "formula": "B_Q=C1 dD1 + C2 dD2; H_Q=dC1 wedge dD1 + dC2 wedge dD2; H_Q wedge H_Q can be nonzero.",
            "payoff": "Generic EM needs at least a two-pair internal flow chart or an equivalent higher-dimensional internal multiplet.",
            "claim_status": "GENERIC_LOCAL_FORM_AVAILABLE_IF_PARENT_OWNS_PAIRS",
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "lemma_id": "DCL3785_3_no_smuggle_condition",
            "statement": "The Clebsch coordinates must be parent fields or parent-derived flow scalars before EM readout; choosing them after fitting H_Q is just a local parameterization of EM.",
            "formula": "valid_B_Q requires C_i,D_i in Alg_preEM[Phi_MTS,Psi_Q], not C_i,D_i=functions_of(A_obs,F_obs).",
            "payoff": "This turns B_Q from missing language into a concrete owner test.",
            "claim_status": "NO_SMUGGLE_GATE",
            "valid_for_claim": False,
        },
    ]


def candidate_test_rows(timestamp):
    return [
        {
            "timestamp_utc": timestamp,
            "candidate_id": "BQC3785_0_real_scalar_gradient",
            "candidate": "B_Q=df(psi) or f(psi)dpsi from current real scalar psi",
            "test_result": "REJECT",
            "reason": "dB_Q=0 away from singularities, so it cannot generate ordinary nonzero local Maxwell curvature.",
            "next_action": "do not spend more proof budget on pure-gradient real-scalar routes",
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "candidate_id": "BQC3785_1_single_flow_one_form",
            "candidate": "B_Q=u_flat or C dD from one owned flow pair",
            "test_result": "PARTIAL_ONLY",
            "reason": "nonzero vorticity is possible, but H_Q wedge H_Q=0 for one Clebsch pair and U(1)/charge normalization is not owned.",
            "next_action": "use only for null/simple EM sectors or as one component of a two-pair construction",
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "candidate_id": "BQC3785_2_two_pair_clebsch",
            "candidate": "B_Q=C1 dD1+C2 dD2 with C_i,D_i parent-owned flow coordinates",
            "test_result": "BEST_LOCAL_MATH_ROUTE",
            "reason": "it can produce generic local dB_Q while remaining pre-EM if the four scalars are parent-owned before readout.",
            "next_action": "hunt or add an explicit parent owner for the two flow pairs",
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "candidate_id": "BQC3785_3_berry_connection",
            "candidate": "B_Q=-i z_dagger dz from normalized internal complex multiplet z",
            "test_result": "BEST_GEOMETRIC_ROUTE",
            "reason": "it naturally supplies a U(1) bundle connection and topological periods, but current corpus has real psi rather than parent-owned z.",
            "next_action": "test whether MTS can own a CP^2 or equivalent multiplet without importing EM",
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "candidate_id": "BQC3785_4_defect_only",
            "candidate": "B_Q from node/defect phase winding only",
            "test_result": "TOPOLOGICAL_SUPPORT_ONLY",
            "reason": "defects can quantize flux and Wilson residues but do not by themselves supply generic smooth local EM fields.",
            "next_action": "keep defect terms as D_Q/epsilon_node rows, not full B_Q closure",
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "candidate_id": "BQC3785_5_poynting_hodge_flow",
            "candidate": "B_Q from Poynting/Hodge/background energy flow",
            "test_result": "PROMISING_BUT_CIRCULAR_UNLESS_PRE_EM",
            "reason": "if Poynting means E cross B it is circular; if it means a parent energy-flow current before EM, it becomes a possible owner but is not currently specified.",
            "next_action": "require a pre-EM stress-flow definition before using this route",
            "valid_for_claim": False,
        },
    ]


def berry_multiplet_rows(timestamp):
    return [
        {
            "timestamp_utc": timestamp,
            "route_id": "BMR3785_0_parent_internal_multiplet",
            "object": "z: U -> C^N with z_dagger z=1",
            "theorem_piece": "The local one-form a_B=-i z_dagger dz is a U(1) connection on the phase bundle of z.",
            "requirement": "z must be a parent MTS/internal field, not reconstructed from A_obs/F_obs.",
            "status": "MISSING_PARENT_MULTIPLET",
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "route_id": "BMR3785_1_chart_transform",
            "object": "z -> exp(i chi) z",
            "theorem_piece": "a_B -> a_B+dchi; curvature h_B=da_B is chart-invariant.",
            "requirement": "3784 Pi_Q gauge-invariant wording must be refined to a parent-connection object with chart-covariant local representatives.",
            "status": "CONTRACT_REFINEMENT_NEEDED",
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "route_id": "BMR3785_2_rank_requirement",
            "object": "CP^(N-1) target",
            "theorem_piece": "CP^1/Hopf supplies a simple curvature sector; CP^2 or two Clebsch pairs are needed for generic 4D H_Q with H_Q wedge H_Q nonzero.",
            "requirement": "generic EM branch needs N>=3 or equivalent two-pair flow chart.",
            "status": "RANK_GATE_DERIVED",
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "route_id": "BMR3785_3_charge_lattice",
            "object": "periods and Chern class of the U(1) phase bundle",
            "theorem_piece": "integral periods can support charge labels and Wilson/defect accounting.",
            "requirement": "1056/1100 still require fixed norm/level, current owner, no independent F2, and readout closure before alpha_EM is owned.",
            "status": "SUPPORTS_CHARGE_NOT_ALPHA",
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "route_id": "BMR3785_4_verdict",
            "object": "Berry-Clebsch B_Q",
            "theorem_piece": "This is the cleanest non-circular B_Q candidate found in this pass.",
            "requirement": "must be introduced as a parent internal multiplet clause or found in the corpus; current real-scalar branch does not supply it.",
            "status": "VIABLE_PARENT_EXTENSION_NOT_CURRENTLY_DERIVED",
            "valid_for_claim": False,
        },
    ]


def poynting_vorticity_rows(timestamp):
    return [
        {
            "timestamp_utc": timestamp,
            "audit_id": "PVD3785_0_flow_vorticity",
            "route": "B_Q from parent flow velocity one-form",
            "result": "dB_Q is a vorticity 2-form if the flow one-form is parent-owned.",
            "blocker": "current corpus does not provide a U(1) charge bundle or two-pair generic-rank owner from this flow alone",
            "status": "PARTIAL_FLOW_SUPPORT",
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "audit_id": "PVD3785_1_Qflow_defect",
            "route": "Q-flow stationarity defect Theta_Q",
            "result": "1174 gives a sharp scalar/domain defect and projector leak route.",
            "blocker": "Theta_Q is not a one-form connection and Q_coh/N_D remain unsigned",
            "status": "USEFUL_RESIDUAL_NOT_BQ_OWNER",
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "audit_id": "PVD3785_2_defect_nodes",
            "route": "node/defect phase winding",
            "result": "can own quantized singular support and Wilson residues if D_Q is parent-owned.",
            "blocker": "defect-only route does not supply generic smooth Maxwell curvature",
            "status": "TOPOLOGICAL_SUPPORT",
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "audit_id": "PVD3785_3_poynting",
            "route": "Poynting/Hodge flow",
            "result": "the heuristic is worth keeping: EM may reveal a background Hodge/flow rule.",
            "blocker": "ordinary Poynting vector is defined after EM fields exist, so it is circular unless replaced by a pre-EM parent stress-flow current",
            "status": "HEURISTIC_TO_PRE_EM_REQUIREMENT",
            "valid_for_claim": False,
        },
    ]


def rank_gate_rows(timestamp):
    return [
        {
            "timestamp_utc": timestamp,
            "gate_id": "RNG3785_0_closed",
            "gate": "dH_Q=0",
            "current_status": "PASS_IF_H_Q=dB_Q",
            "meaning": "Bianchi identity follows automatically from B_Q construction.",
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "gate_id": "RNG3785_1_rank",
            "gate": "generic local EM requires enough internal rank",
            "current_status": "REQUIRES_TWO_CLEBSCH_PAIRS_OR_CP2",
            "meaning": "one pair/CP1 has H_Q wedge H_Q=0 and cannot cover general F wedge F sectors.",
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "gate_id": "RNG3785_2_no_A",
            "gate": "B_Q independent of A_obs/F_obs/Maxwell equations",
            "current_status": "UNSIGNED",
            "meaning": "the current corpus does not yet own the Clebsch/Berry coordinates before EM readout.",
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "gate_id": "RNG3785_3_qobs",
            "gate": "Lie_EA B_Q=0 or bounded",
            "current_status": "MISSING_PARENT_DESCENT",
            "meaning": "needed to make R_A=0 rather than finite epsilon_Pi/e_dPi rows.",
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "gate_id": "RNG3785_4_norm",
            "gate": "fixed level/norm/current/readout",
            "current_status": "MISSING_1056_1100_SIGNATURE",
            "meaning": "even a valid B_Q does not by itself own alpha_EM or source normalization.",
            "valid_for_claim": False,
        },
    ]


def finite_mode_rows(timestamp):
    return [
        {
            "timestamp_utc": timestamp,
            "mode_id": "FBU3785_0_BQ_owner",
            "residual": "epsilon_BQ_owner",
            "definition": "1 if no parent-owned two-pair Clebsch/CP2/Berry multiplet is signed; 0 if signed",
            "current_value": "MISSING_PARENT_BQ_OWNER",
            "arena": "EM readout/local GR",
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "mode_id": "FBU3785_1_rank",
            "residual": "epsilon_BQ_rank",
            "definition": "residual for using a rank-too-small B_Q sector where H_Q wedge H_Q observables require generic rank",
            "current_value": "MISSING_RANK_CERTIFICATE",
            "arena": "generic EM sectors",
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "mode_id": "FBU3785_2_chart",
            "residual": "epsilon_BQ_chart",
            "definition": "failure to reconcile parent bundle chart transformations with 3784 A_obs reconstruction",
            "current_value": "MISSING_CHART_COVARIANCE_CONTRACT",
            "arena": "gauge/readout",
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "mode_id": "FBU3785_3_alpha",
            "residual": "beta_Z,A;lambda_A",
            "definition": "normalization and independent F2 residuals retained from 1056/1100/3784",
            "current_value": "MISSING_ALPHA_OWNER",
            "arena": "alpha/WEP/R10/clocks",
            "valid_for_claim": False,
        },
    ]


def claim_gate_rows(timestamp):
    return [
        {
            "timestamp_utc": timestamp,
            "gate_id": "CG3785_0_sources",
            "pass": True,
            "claim_allowed": False,
            "details": "all source paths resolve",
        },
        {
            "timestamp_utc": timestamp,
            "gate_id": "CG3785_1_math_BQ_exists",
            "pass": True,
            "claim_allowed": False,
            "details": "Darboux/Clebsch and Berry routes give exact conditional B_Q constructions",
        },
        {
            "timestamp_utc": timestamp,
            "gate_id": "CG3785_2_current_corpus_owner",
            "pass": False,
            "claim_allowed": False,
            "details": "current real-scalar corpus does not own two Clebsch pairs or CP2/Berry multiplet",
        },
        {
            "timestamp_utc": timestamp,
            "gate_id": "CG3785_3_generic_rank",
            "pass": False,
            "claim_allowed": False,
            "details": "generic-rank certificate is missing; one-pair/CP1 route is insufficient",
        },
        {
            "timestamp_utc": timestamp,
            "gate_id": "CG3785_4_alpha_norm",
            "pass": False,
            "claim_allowed": False,
            "details": "fixed gauge norm/current/no-extra-F2/readout signature remains unsigned",
        },
        {
            "timestamp_utc": timestamp,
            "gate_id": "CG3785_5_local_GR_EM_claim",
            "pass": False,
            "claim_allowed": False,
            "details": "no EM/local-GR claim until B_Q owner, q_obs descent, rank, norm, current, and alpha gates close or are bounded",
        },
    ]


def decision_rows(timestamp):
    return [
        {
            "timestamp_utc": timestamp,
            "decision_id": "DEC3785_0_real_progress",
            "decision": "B_Q is not just missing; there is an exact local construction route.",
            "action": "Use Darboux/Clebsch or Berry/internal multiplet as the next constructive branch.",
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "decision_id": "DEC3785_1_best_candidate",
            "decision": "The best less-cheaty route is a parent-owned CP2/two-Clebsch-pair internal flow multiplet.",
            "action": "Try to source or define that multiplet from MTS primitives without importing EM.",
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "decision_id": "DEC3785_2_demote_current_corpus",
            "decision": "The current real-scalar branch still does not derive generic B_Q.",
            "action": "Keep EM readout as viable parent-extension finite-bound mode until the multiplet owner is signed.",
            "valid_for_claim": False,
        },
    ]


def next_target_rows(timestamp):
    return [
        {
            "timestamp_utc": timestamp,
            "target_file": "3786-Y5-R2FR-parent-internal-multiplet-owner-or-BQ-finite-demotion.md",
            "target_script": "scripts/Y5_R2FR_3786_parent_internal_multiplet_owner_or_BQ_finite_demotion.py",
            "objective": "Try to derive or source a parent-owned two-Clebsch-pair/CP2 internal multiplet from MTS flow variables; if no owner exists, promote epsilon_BQ_owner/rank/chart as official finite EM residuals.",
            "valid_for_claim": False,
        }
    ]


def status_rows(timestamp):
    return [
        {
            "timestamp_utc": timestamp,
            "checkpoint_id": CHECKPOINT,
            "branch_id": BRANCH,
            "status": "EXACT_BQ_CONSTRUCTION_ROUTE_FOUND_PARENT_OWNER_MISSING",
            "plain_verdict": "3785 finds a real mathematical route: B_Q can be a Darboux/Clebsch or Berry internal-multiplet one-form, and two flow pairs/CP2 are enough for generic local EM rank. But the current corpus does not yet parent-own those internal coordinates, so the result is a constructive target, not an EM/local-GR claim.",
            "valid_for_claim": False,
        }
    ]


def validation_rows(timestamp, grouped):
    def csv_parses(path):
        if not path.exists():
            return False
        with path.open(encoding="utf-8") as handle:
            list(csv.DictReader(handle))
        return True

    checks = [
        (
            "sources_exist",
            all(Path(row["source_path"]).exists() for row in grouped["sources"]),
            "every cited source path exists",
        ),
        (
            "csv_outputs_parse",
            all(csv_parses(path) for key, path in OUTPUTS.items() if key != "validation"),
            "all generated CSV outputs exist and parse",
        ),
        ("doc_written", DOC_PATH.exists(), "3785 markdown document written"),
        (
            "clebsch_lemma",
            len(grouped["clebsch_lemma"]) >= 4,
            "Darboux/Clebsch B_Q lemma emitted",
        ),
        (
            "candidate_tests",
            any(row["candidate_id"] == "BQC3785_2_two_pair_clebsch" for row in grouped["candidate_tests"]),
            "two-pair Clebsch candidate emitted",
        ),
        (
            "berry_route",
            any(row["route_id"] == "BMR3785_4_verdict" for row in grouped["berry_multiplet"]),
            "Berry/internal multiplet route emitted",
        ),
        (
            "rank_gate",
            any(row["gate_id"] == "RNG3785_1_rank" for row in grouped["rank_gates"]),
            "rank/no-smuggle gates emitted",
        ),
        (
            "finite_nonclaim",
            all(row["valid_for_claim"] is False for row in grouped["finite_mode"]),
            "finite B_Q residual rows stay nonclaim",
        ),
        (
            "claim_gate_closed",
            any(row["gate_id"] == "CG3785_5_local_GR_EM_claim" and row["pass"] is False for row in grouped["claim_gates"]),
            "EM/local-GR claim gate remains closed",
        ),
        (
            "next_target",
            grouped["next_target"][0]["target_file"].startswith("3786-"),
            "3786 internal multiplet target emitted",
        ),
        (
            "formalization_clean",
            not any("formalization-workbench" in str(path) for path in OUTPUTS.values()),
            "no 3785 files written under formalization-workbench",
        ),
    ]
    return [
        {
            "timestamp_utc": timestamp,
            "checkpoint_id": CHECKPOINT,
            "branch_id": BRANCH,
            "validation_id": check_id,
            "result": "PASS" if ok else "FAIL",
            "detail": detail,
            "valid_for_claim": False,
        }
        for check_id, ok, detail in checks
    ]


def render_section(title, rows, key_fields):
    lines = [f"## {title}"]
    for row in rows:
        head = " ".join(f"`{row[field]}`" for field in key_fields if field in row)
        details = []
        for key, value in row.items():
            if key in key_fields or key in {"timestamp_utc", "checkpoint_id", "branch_id", "valid_for_claim"}:
                continue
            details.append(f"{key}: {value}")
        lines.append(f"- {head}: " + "; ".join(details))
    lines.append("")
    return "\n".join(lines)


def render_doc(grouped):
    status = grouped["status"][0]
    text = [
        "# 3785 - Derive B_Q Flow One-Form From Vorticity/Defects Or Demote EM",
        "",
        "## Status",
        "",
        f"`{status['status']}`.",
        "",
        status["plain_verdict"],
        "",
        "## Result In Plain Terms",
        "",
        "3785 is a real push forward. The non-circular `B_Q` object is not magic: locally, a closed pre-EM curvature can be written as `H_Q=dB_Q` with `B_Q=sum_i C_i dD_i`. One Clebsch pair is too small for generic EM because it forces `H_Q wedge H_Q=0`; two pairs, or an equivalent `CP2`/Berry internal multiplet, can carry generic local rank. That gives a concrete construction route. The current corpus still does not own those internal coordinates before EM readout, so this is a viable parent-extension target, not a local-GR/EM claim.",
        "",
        render_section("Darboux / Clebsch B_Q Lemma", grouped["clebsch_lemma"], ["lemma_id", "claim_status"]),
        render_section("B_Q Candidate Tests", grouped["candidate_tests"], ["candidate_id", "test_result"]),
        render_section("Berry Internal Multiplet Route", grouped["berry_multiplet"], ["route_id", "status"]),
        render_section("Poynting / Vorticity / Defect Audit", grouped["poynting_vorticity"], ["audit_id", "status"]),
        render_section("Rank And No-Smuggle Gates", grouped["rank_gates"], ["gate_id", "current_status"]),
        render_section("EM Finite-Bound Mode Update", grouped["finite_mode"], ["mode_id", "residual"]),
        render_section("Claim Gates", grouped["claim_gates"], ["gate_id"]),
        render_section("Decisions", grouped["decisions"], ["decision_id"]),
        render_section("Next Target", grouped["next_target"], ["target_file"]),
        render_section("Validation", grouped["validation"], ["validation_id", "result"]),
    ]
    return "\n".join(text).rstrip() + "\n"


def main():
    timestamp = datetime.now(timezone.utc).isoformat()
    RESIDUALS.mkdir(parents=True, exist_ok=True)
    grouped = {
        "sources": source_register(timestamp),
        "clebsch_lemma": clebsch_lemma_rows(timestamp),
        "candidate_tests": candidate_test_rows(timestamp),
        "berry_multiplet": berry_multiplet_rows(timestamp),
        "poynting_vorticity": poynting_vorticity_rows(timestamp),
        "rank_gates": rank_gate_rows(timestamp),
        "finite_mode": finite_mode_rows(timestamp),
        "claim_gates": claim_gate_rows(timestamp),
        "decisions": decision_rows(timestamp),
        "next_target": next_target_rows(timestamp),
        "status": status_rows(timestamp),
        "validation": [],
    }

    write_csv(OUTPUTS["sources"], grouped["sources"])
    write_csv(OUTPUTS["clebsch_lemma"], grouped["clebsch_lemma"])
    write_csv(OUTPUTS["candidate_tests"], grouped["candidate_tests"])
    write_csv(OUTPUTS["berry_multiplet"], grouped["berry_multiplet"])
    write_csv(OUTPUTS["poynting_vorticity"], grouped["poynting_vorticity"])
    write_csv(OUTPUTS["rank_gates"], grouped["rank_gates"])
    write_csv(OUTPUTS["finite_mode"], grouped["finite_mode"])
    write_csv(OUTPUTS["claim_gates"], grouped["claim_gates"])
    write_csv(OUTPUTS["decisions"], grouped["decisions"])
    write_csv(OUTPUTS["next_target"], grouped["next_target"])
    write_csv(OUTPUTS["status"], grouped["status"])

    DOC_PATH.write_text(render_doc(grouped), encoding="utf-8")
    grouped["validation"] = validation_rows(timestamp, grouped)
    write_csv(OUTPUTS["validation"], grouped["validation"])
    DOC_PATH.write_text(render_doc(grouped), encoding="utf-8")

    cache = Path(__file__).resolve().parent / "__pycache__"
    if cache.exists():
        shutil.rmtree(cache)

    failures = [row for row in grouped["validation"] if row["result"] != "PASS"]
    if failures:
        raise SystemExit(f"3785 validation failed: {failures}")
    print("wrote 3785 checkpoint: exact B_Q construction route found, owner missing")


if __name__ == "__main__":
    main()
