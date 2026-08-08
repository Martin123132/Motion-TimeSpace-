from __future__ import annotations

import csv
import shutil
import subprocess
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
FORMALIZATION = ROOT.parent / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
RAB = ROOT / "source-intake" / "rab-sector"
RAB_RAW = RAB / "raw"
RAB_ACCEPTED = RAB / "accepted"
MICROSCOPE = ROOT / "source-intake" / "microscope"
BRANCH_RESIDUALS = MICROSCOPE / "branch_locked_wep" / "residuals"
QUARANTINE = MICROSCOPE / "quarantine" / "1584"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC = ROOT / "1584-Y5-PPN-beta-conservation-common-matter-gate.md"

SOURCE_FILES = {
    "1583_doc": ROOT / "1583-Y5-PPN-tail-zero-theorem-or-first-finite-tail-bound.md",
    "1583_validation": OUT / "P8_Y5_BRR545_1583_VALIDATION.csv",
    "1583_gr_completion": OUT / "P8_Y5_PARENT_QLOC_1583_GR_COMPLETION_GATE.csv",
    "10_observer": ROOT / "10-observer-map-symplectic-contract.md",
    "local_bound_claims": LOCAL_BOUNDS / "local_bound_claims.csv",
    "constant_gm_gate": OUT / "P8_CONSTANT_GM_DERIVATIVE_HAIR_GATE.csv",
    "parent_source_identity": OUT / "P8_PARENT_SOURCE_IDENTITY_ATTEMPT.csv",
    "parent_source_decision": OUT / "P8_PARENT_SOURCE_IDENTITY_DECISION.csv",
    "1519_coframe_tau": OUT / "P8_Y5_PARENT_FRAME_1519_COFRAME_TAU_LOCK_AUDIT.csv",
    "1575_matter_descent": ROOT / "1575-Y5-RAB-parent-RAB-vertical-generator-and-matter-descent-signature.md",
    "1104_ordinary": ROOT / "1104-Y5-R10-parent-ordinary-sector-action-signature-or-explicit-closure-ledger.md",
}

NEEDLES = {
    "1583_doc": ["NEXT_1584_PPN_BETA_CONSERVATION_COMMON_MATTER_GATE", "gamma/q_R_hat branch is useful but cannot be upgraded to GR"],
    "1583_validation": ["VAL1583_OVERALL", "PASS"],
    "1583_gr_completion": ["GRC1583_1_beta", "MISSING_DERIVATION", "GRC1583_2_conservation"],
    "10_observer": ["beta - 1 = 0", "Bianchi-like consistency identity"],
    "local_bound_claims": ["Will_2014_PPN_beta_table", "beta_minus_1", "7.8e-05"],
    "constant_gm_gate": ["CGM7_second_order_beta_residue", "delta_beta_source", "deferred_until_first_order_source_rows_owned"],
    "parent_source_identity": ["I499_3_parent_source_identity", "derived_as_decomposition_not_zero"],
    "parent_source_decision": ["D499_1_total_conservation", "insufficient", "D499_4_promotion", "forbidden"],
    "1519_coframe_tau": ["OCF1519_4_tau_lock", "MISSING_TAU_LOCK"],
    "1575_matter_descent": ["MDS1575_4_boundary", "FAIL_CURRENT_CLAIM_DESCENT_NOT_SIGNED"],
    "1104_ordinary": ["SIG1104_9_Ward_Bianchi_conservation", "OPEN_PARALLEL_GATE"],
}

SOURCE_REGISTER = OUT / "P8_Y5_PARENT_QLOC_1584_SOURCE_REGISTER.csv"
BETA_GATE = OUT / "P8_Y5_PARENT_QLOC_1584_BETA_GATE.csv"
CONSERVATION_GATE = OUT / "P8_Y5_PARENT_QLOC_1584_CONSERVATION_GATE.csv"
COMMON_MATTER_GATE = OUT / "P8_Y5_PARENT_QLOC_1584_COMMON_MATTER_GATE.csv"
NEWTON_SOURCE_GATE = OUT / "P8_Y5_PARENT_QLOC_1584_NEWTON_SOURCE_GATE.csv"
GR_REDUCTION_RUNNER = OUT / "P8_Y5_PARENT_QLOC_1584_GR_REDUCTION_RUNNER.csv"
CLAIM_GATE = OUT / "P8_Y5_PARENT_QLOC_1584_CLAIM_GATE.csv"
DECISION = OUT / "P8_Y5_PARENT_QLOC_1584_DECISION.csv"
NEXT_TARGET = OUT / "P8_Y5_PARENT_QLOC_1584_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1584_VALIDATION.csv"

COPY_TARGETS = {
    BETA_GATE: [
        QUARANTINE / "PPN_BETA_GATE_NONCLAIM.csv",
        BRANCH_RESIDUALS / "PPN_beta_gate_nonclaim_1584.csv",
    ],
    CONSERVATION_GATE: [
        QUARANTINE / "CONSERVATION_GATE_NONCLAIM.csv",
        BRANCH_RESIDUALS / "conservation_gate_nonclaim_1584.csv",
    ],
    COMMON_MATTER_GATE: [
        QUARANTINE / "COMMON_MATTER_GATE_NONCLAIM.csv",
        BRANCH_RESIDUALS / "common_matter_gate_nonclaim_1584.csv",
    ],
    NEWTON_SOURCE_GATE: [
        QUARANTINE / "NEWTON_SOURCE_GATE_NONCLAIM.csv",
        BRANCH_RESIDUALS / "Newton_source_gate_nonclaim_1584.csv",
    ],
    GR_REDUCTION_RUNNER: [
        QUARANTINE / "GR_REDUCTION_RUNNER_NONCLAIM.csv",
        BRANCH_RESIDUALS / "GR_reduction_runner_nonclaim_1584.csv",
    ],
    DECISION: [
        QUARANTINE / "DECISION_NONCLAIM.csv",
        BRANCH_RESIDUALS / "PPN_beta_conservation_common_matter_decision_nonclaim_1584.csv",
    ],
}


def flags() -> dict[str, bool]:
    return {
        "parent_signed": False,
        "numeric_value_present": False,
        "source_backed": False,
        "score_ready": False,
        "valid_prediction_row": False,
        "valid_for_claim": False,
        "claim_allowed": False,
    }


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        return str(path)


def file_contains(path: Path, needles: list[str]) -> bool:
    if not path.exists():
        return False
    text = path.read_text(encoding="utf-8", errors="ignore")
    return all(needle in text for needle in needles)


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def source_register_rows() -> list[dict[str, Any]]:
    rows = []
    for source_index, (source_key, source_path) in enumerate(SOURCE_FILES.items()):
        rows.append(
            {
                "same_parent_branch_id": BRANCH_ID,
                "source_id": f"SRC1584_{source_index}_{source_key}",
                "source_path": rel(source_path),
                "exists": source_path.exists(),
                "needle_found": file_contains(source_path, NEEDLES[source_key]),
                "needles": "; ".join(NEEDLES[source_key]),
                "purpose": "PPN beta, Bianchi-like conservation, common matter coupling and Newton source gates",
                **flags(),
            }
        )
    return rows


def beta_gate_rows() -> list[dict[str, Any]]:
    beta_rows = [
        (
            "BETA1584_0_definition",
            "PPN beta grammar",
            "g_00=-1+2U/c^2-2 beta U^2/c^4+O(c^-6) in a valid PPN coordinate construction",
            "defines beta_minus_1 target independently of gamma_minus_1",
            "FORMAL_INPUT",
            "not a prediction row",
        ),
        (
            "BETA1584_1_gamma_not_beta",
            "gamma channel insufficiency",
            "R_AB or q_R_hat controls the first post-Newtonian spatial/temporal product channel, not the nonlinear U^2 source coefficient",
            "forbid gamma-only local-GR promotion",
            "NOT_DERIVED_FROM_GAMMA",
            "gamma=1 does not imply beta=1",
        ),
        (
            "BETA1584_2_source_normalized_residue",
            "second-order measured-GM residue",
            "beta_minus_1 = delta_beta_source + delta_beta_operator + delta_beta_tail after measured-GM normalization",
            "would score only after all components are zero or numerically bounded",
            "MISSING_SECOND_ORDER_SOURCE_VECTOR",
            "CGM7 names delta_beta_source but no parent-owned beta vector exists",
        ),
        (
            "BETA1584_3_external_bound",
            "Will 2014 beta bound",
            "|beta-1| <= 7.8e-05 as source-backed local bound row",
            "comparator bound exists, but MTS has no valid beta prediction",
            "BOUND_AVAILABLE_PREDICTION_MISSING",
            "external bound is not evidence without beta_minus_1 prediction",
        ),
        (
            "BETA1584_4_verdict",
            "beta=1 theorem",
            "parent action yields beta_minus_1=0 or a sourced finite vector under the same observed Newtonian source normalization",
            "would clear the post-linear PPN gate",
            "FAIL_CURRENT_CLAIM_BETA_NOT_DERIVED",
            "second-order operator/source/tail ownership is missing",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "beta_gate_id": beta_gate_id,
            "gate": gate,
            "required_statement": required_statement,
            "effect_if_signed": effect_if_signed,
            "status": status,
            "blocking_gap": blocking_gap,
            **flags(),
        }
        for beta_gate_id, gate, required_statement, effect_if_signed, status, blocking_gap in beta_rows
    ]


def conservation_gate_rows() -> list[dict[str, Any]]:
    conservation_rows = [
        (
            "CONS1584_0_total_ward",
            "total parent Ward/Bianchi accounting",
            "nabla_mu T_total^{mu nu}=0 or parent source ledger is conserved as a whole",
            "keeps the total bookkeeping consistent",
            "AVAILABLE_BUT_INSUFFICIENT",
            "total conservation can hide exchange with extra/projected channels",
        ),
        (
            "CONS1584_1_projected_identity",
            "observed Hilbert mass-channel closure",
            "d(Pi_M J_H) = -Pi_M dJ_extra + [d,Pi_M]J_H + A_parent",
            "identifies exact obstruction terms",
            "OBSTRUCTION_DERIVED_NOT_ZERO",
            "Pi_M extra-current, projector commutator and anomaly are not zero",
        ),
        (
            "CONS1584_2_ward_shortcut",
            "Ward-only shortcut",
            "total Ward conservation implies observed source conservation with no residuals",
            "would be a hidden smuggling move",
            "REFUSE_PLACEHOLDER",
            "projected source closure requires its own theorem or retained residual vector",
        ),
        (
            "CONS1584_3_zero_conditions",
            "sufficient conservation closure",
            "Pi_M dJ_extra=0, [d,Pi_M]J_H=0, A_parent=0, and retained stress/current residual ledger is silent",
            "would close the local Bianchi-like source gate",
            "CONDITIONAL_NOT_PARENT_SIGNED",
            "each zero clause needs a parent action owner",
        ),
        (
            "CONS1584_4_verdict",
            "source-compatible conservation identity",
            "field equations imply observed matter/source conservation with no hidden momentum/domain/boundary flux",
            "would protect local GR/Newton reduction from source leakage",
            "FAIL_CURRENT_CLAIM_CONSERVATION_NOT_DERIVED",
            "the current corpus proves a decomposition, not vanishing of the decomposition",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "conservation_gate_id": conservation_gate_id,
            "gate": gate,
            "required_statement": required_statement,
            "effect_if_signed": effect_if_signed,
            "status": status,
            "blocking_gap": blocking_gap,
            **flags(),
        }
        for conservation_gate_id, gate, required_statement, effect_if_signed, status, blocking_gap in conservation_rows
    ]


def common_matter_gate_rows() -> list[dict[str, Any]]:
    matter_rows = [
        (
            "MAT1584_0_observed_coframe",
            "single observed coframe",
            "all local matter sectors read one e_obs and one local quotient geometry",
            "prevents species-dependent shadow frames",
            "MISSING_PARENT_SIGNATURE",
            "coframe functor exists as a contract but is not parent-signed",
        ),
        (
            "MAT1584_1_tau_lock",
            "source/charge/clock/orbit/boundary tau lock",
            "tau_source=tau_charge=tau_clock=tau_orbit=tau_boundary",
            "prevents arena-dependent local time readouts",
            "MISSING_TAU_LOCK",
            "1519 keeps tau lock open",
        ),
        (
            "MAT1584_2_matter_descent",
            "quotient-invariant matter descent",
            "S_matter=Sbar[q(Phi),Psi,theta] with vertical matter/source variation zero or owned boundary",
            "would silence representative Weyl/disformal charges",
            "CONDITIONAL_NOT_PARENT_SIGNED",
            "1575 gives the best route but boundary/descent signature is unsigned",
        ),
        (
            "MAT1584_3_no_marker",
            "no hidden source marker",
            "no matter-sector marker, Weyl representative, disformal readout or shadow frame survives in the observed action",
            "would protect WEP/PPN/common coupling",
            "MISSING_NO_MARKER_THEOREM",
            "absence of these couplings is not yet derived from the parent action",
        ),
        (
            "MAT1584_4_verdict",
            "universal common matter coupling",
            "all matter sectors couple to the same observed coframe with fixed constants and no hidden residual readouts",
            "would clear the common-matter leg of local GR",
            "FAIL_CURRENT_CLAIM_COMMON_MATTER_NOT_DERIVED",
            "coframe, tau lock, matter descent and no-marker clauses remain unsigned",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "common_matter_gate_id": common_matter_gate_id,
            "gate": gate,
            "required_statement": required_statement,
            "effect_if_signed": effect_if_signed,
            "status": status,
            "blocking_gap": blocking_gap,
            **flags(),
        }
        for common_matter_gate_id, gate, required_statement, effect_if_signed, status, blocking_gap in matter_rows
    ]


def newton_source_gate_rows() -> list[dict[str, Any]]:
    newton_rows = [
        (
            "NEW1584_0_metric_limit",
            "Newtonian metric/readout limit",
            "T^2=1-2U/c^2 and the weak acceleration reads the same U measured by local matter",
            "first-order Newton limit can be scored only in the observed frame",
            "FORMAL_REQUIREMENT",
            "frame/readout/source denominator must be shared",
        ),
        (
            "NEW1584_1_measured_gm",
            "measured-GM source denominator",
            "mu_obs=G_eff M_eff(1+epsilon_mu) with epsilon_mu=0 or bounded in the same source channel",
            "prevents re-labelling source normalization as a force law",
            "MISSING_SOURCE_DENOMINATOR",
            "M_H_ref, Pi_M and source equality remain unowned",
        ),
        (
            "NEW1584_2_derivative_hair",
            "constant-GM derivative-hair gates",
            "CGM0 through CGM7 close, including the second-order beta residue",
            "would protect Newton-to-PPN promotion",
            "DEFERRED_UNTIL_FIRST_ORDER_SOURCE_ROWS_OWNED",
            "CGM7 explicitly blocks beta promotion from first-order evidence alone",
        ),
        (
            "NEW1584_3_no_promotion",
            "Newton-first shortcut",
            "first-order Poisson/Gauss success implies full local GR",
            "would overclaim from a weaker limit",
            "REFUSE_PLACEHOLDER",
            "Newtonian recovery is necessary but not sufficient for GR",
        ),
        (
            "NEW1584_4_verdict",
            "source-normalized Newton-to-GR bridge",
            "Newton source denominator, beta, conservation and common matter all close under one parent action",
            "would create a serious local-GR branch",
            "FAIL_CURRENT_CLAIM_NEWTON_SOURCE_NOT_DERIVED",
            "source denominator and post-linear conservation/matter gates remain open",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "newton_source_gate_id": newton_source_gate_id,
            "gate": gate,
            "required_statement": required_statement,
            "effect_if_signed": effect_if_signed,
            "status": status,
            "blocking_gap": blocking_gap,
            **flags(),
        }
        for newton_source_gate_id, gate, required_statement, effect_if_signed, status, blocking_gap in newton_rows
    ]


def gr_reduction_runner_rows() -> list[dict[str, Any]]:
    runner_rows = [
        (
            "RUN1584_0_gamma_only",
            "upgrade q_R_hat/gamma channel to local GR",
            "REFUSE_PLACEHOLDER",
            "beta, conservation, common matter and source-normalized Newton gates remain open",
        ),
        (
            "RUN1584_1_total_ward_only",
            "use total Ward identity as observed Bianchi/source closure",
            "REFUSE_PLACEHOLDER",
            "parent source identity shows projected Hilbert channel obstruction terms",
        ),
        (
            "RUN1584_2_newton_first_order",
            "promote first-order Newton recovery to GR",
            "REFUSE_PLACEHOLDER",
            "CGM7 and PPN beta require second-order control",
        ),
        (
            "RUN1584_3_beta_bound_score",
            "score Will beta bound",
            "NOT_RUN_PREDICTION_MISSING",
            "external bound exists but no valid beta_minus_1 prediction row exists",
        ),
        (
            "RUN1584_4_local_gr",
            "claim local GR/Newton branch",
            "BLOCKED_NO_CLAIM",
            "all four completion gates must close under the same parent action first",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "runner_id": runner_id,
            "case": case,
            "status": status,
            "reason": reason,
            "can_score": False,
            **flags(),
        }
        for runner_id, case, status, reason in runner_rows
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    claim_rows = [
        ("GATE1584_0_beta", "PPN beta pass", "BLOCKED_NO_CLAIM", "beta_minus_1 is neither derived zero nor numerically predicted"),
        ("GATE1584_1_conservation", "Bianchi-like conservation pass", "BLOCKED_NO_CLAIM", "projected Hilbert mass-channel closure is not zero"),
        ("GATE1584_2_common_matter", "common matter coupling pass", "BLOCKED_NO_CLAIM", "coframe/tau/matter/no-marker clauses are unsigned"),
        ("GATE1584_3_newton_source", "source-normalized Newton pass", "BLOCKED_NO_CLAIM", "GM/source denominator remains open"),
        ("GATE1584_4_local_gr", "local GR reduction pass", "BLOCKED_NO_CLAIM", "gamma branch plus open beta/conservation/matter/source gates is not GR"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "gate_id": gate_id,
            "claim": claim,
            "status": status,
            "reason": reason,
            **flags(),
        }
        for gate_id, claim, status, reason in claim_rows
    ]


def decision_rows() -> list[dict[str, Any]]:
    decision_data = [
        (
            "DEC1584_0_beta_status",
            "BETA_NOT_DERIVED",
            "Will beta bound is available, but MTS has no beta_minus_1 prediction and gamma is not beta",
            "do not score beta or claim local GR",
        ),
        (
            "DEC1584_1_conservation_status",
            "PROJECTED_CONSERVATION_NOT_DERIVED",
            "total Ward conservation is insufficient because Pi_M projection leaves extra-current, commutator and anomaly terms",
            "retain conservation residual vector",
        ),
        (
            "DEC1584_2_common_matter_status",
            "COMMON_MATTER_UNSIGNED",
            "coframe, tau lock, matter descent and no-marker clauses remain missing",
            "do not claim universal matter coupling",
        ),
        (
            "DEC1584_3_next",
            "NEXT_1585_EH_SOURCE_NORMALIZED_PARENT_ACTION_OWNER_OR_BETA_RESIDUAL_LEDGER",
            "the best route is now a single parent-action owner for EH-like nonlinear operator, universal Hilbert source and beta=1; otherwise build the finite beta residual ledger",
            "attempt derivation first, else keep a nonclaim beta/conservation/source residual runner",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": decision_id,
            "decision": decision,
            "reason": reason,
            "consequence": consequence,
            **flags(),
        }
        for decision_id, decision, reason, consequence in decision_data
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "next_target": "1585-Y5-EH-source-normalized-parent-action-owner-or-beta-residual-ledger.md",
            "script": "scripts/Y5_EH_source_normalized_parent_action_owner_or_beta_residual_ledger.py",
            "objective": "try to derive one parent action clause that owns the EH-like nonlinear operator, source-normalized Hilbert coupling, beta=1 and Bianchi-like source conservation; if this fails, build finite beta/source/conservation residual rows",
            "do_not": "do not claim local GR from gamma, total Ward conservation, first-order Newton recovery, or an external beta bound without an MTS prediction",
            **flags(),
        }
    ]


def copy_outputs() -> None:
    for source_path, target_paths in COPY_TARGETS.items():
        for target_path in target_paths:
            target_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source_path, target_path)


def remove_pycache() -> None:
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def generated_flags_false(generated_csvs: list[Path]) -> bool:
    flag_columns = {"score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"}
    for csv_path in generated_csvs:
        for row in read_csv(csv_path):
            for flag_column in flag_columns.intersection(row):
                if row[flag_column] != "False":
                    return False
    return True


def formalization_scope_clean(generated_csvs: list[Path]) -> bool:
    if any(FORMALIZATION in csv_path.parents for csv_path in generated_csvs):
        return False
    try:
        result = subprocess.run(
            ["git", "-C", str(ROOT.parent), "status", "--short", "--", "formalization-workbench"],
            capture_output=True,
            text=True,
            check=False,
        )
    except FileNotFoundError:
        return True
    if result.returncode != 0:
        return True
    return len([line for line in result.stdout.splitlines() if line.strip()]) == 0


def has_1584_rows(folder: Path) -> bool:
    if not folder.exists():
        return False
    return any("1584" in csv_path.name for csv_path in folder.glob("*.csv"))


def validation_rows(generated_csvs: list[Path]) -> list[dict[str, Any]]:
    sources = read_csv(SOURCE_REGISTER)
    beta_rows = read_csv(BETA_GATE)
    conservation_rows = read_csv(CONSERVATION_GATE)
    matter_rows = read_csv(COMMON_MATTER_GATE)
    newton_rows = read_csv(NEWTON_SOURCE_GATE)
    runner_rows = read_csv(GR_REDUCTION_RUNNER)
    claim_rows = read_csv(CLAIM_GATE)
    decisions = read_csv(DECISION)
    required_claims = {
        "PPN beta pass",
        "Bianchi-like conservation pass",
        "common matter coupling pass",
        "source-normalized Newton pass",
        "local GR reduction pass",
    }
    checks = [
        ("VAL1584_0_sources_exist", all(row["exists"] == "True" for row in sources), "all cited 1584 source paths exist"),
        ("VAL1584_1_needles_found", all(row["needle_found"] == "True" for row in sources), "all 1584 source needles found"),
        (
            "VAL1584_2_beta_blocks",
            any(row["beta_gate_id"] == "BETA1584_4_verdict" and row["status"] == "FAIL_CURRENT_CLAIM_BETA_NOT_DERIVED" for row in beta_rows)
            and any(row["beta_gate_id"] == "BETA1584_3_external_bound" and row["status"] == "BOUND_AVAILABLE_PREDICTION_MISSING" for row in beta_rows),
            "beta external bound exists but beta prediction remains missing",
        ),
        (
            "VAL1584_3_conservation_blocks",
            any(row["conservation_gate_id"] == "CONS1584_1_projected_identity" and row["status"] == "OBSTRUCTION_DERIVED_NOT_ZERO" for row in conservation_rows)
            and any(row["conservation_gate_id"] == "CONS1584_2_ward_shortcut" and row["status"] == "REFUSE_PLACEHOLDER" for row in conservation_rows),
            "projected conservation obstruction is retained and Ward-only shortcut is refused",
        ),
        (
            "VAL1584_4_common_matter_blocks",
            any(row["common_matter_gate_id"] == "MAT1584_1_tau_lock" and row["status"] == "MISSING_TAU_LOCK" for row in matter_rows)
            and any(row["common_matter_gate_id"] == "MAT1584_4_verdict" and row["status"] == "FAIL_CURRENT_CLAIM_COMMON_MATTER_NOT_DERIVED" for row in matter_rows),
            "common matter coupling remains blocked by tau/coframe/matter descent gaps",
        ),
        (
            "VAL1584_5_newton_blocks",
            any(row["newton_source_gate_id"] == "NEW1584_1_measured_gm" and row["status"] == "MISSING_SOURCE_DENOMINATOR" for row in newton_rows)
            and any(row["newton_source_gate_id"] == "NEW1584_3_no_promotion" and row["status"] == "REFUSE_PLACEHOLDER" for row in newton_rows),
            "source-normalized Newton remains blocked and first-order shortcut refused",
        ),
        (
            "VAL1584_6_runner_blocks",
            all(row["can_score"] == "False" for row in runner_rows)
            and any(row["runner_id"] == "RUN1584_4_local_gr" and row["status"] == "BLOCKED_NO_CLAIM" for row in runner_rows),
            "GR reduction runner blocks all shortcuts and scoring",
        ),
        (
            "VAL1584_7_claim_gates_closed",
            {row["claim"] for row in claim_rows} == required_claims
            and all(row["claim_allowed"] == "False" and row["status"] == "BLOCKED_NO_CLAIM" for row in claim_rows),
            "all beta/conservation/common matter/Newton/local-GR claim gates remain closed",
        ),
        (
            "VAL1584_8_decision_next",
            any(row["decision"] == "NEXT_1585_EH_SOURCE_NORMALIZED_PARENT_ACTION_OWNER_OR_BETA_RESIDUAL_LEDGER" for row in decisions),
            "decision selects EH/source-normalized parent action owner or beta residual ledger",
        ),
        ("VAL1584_9_csv_parse", all(len(read_csv(csv_path)) > 0 for csv_path in generated_csvs), "all generated 1584 CSVs parse cleanly"),
        ("VAL1584_10_claim_flags_false", generated_flags_false(generated_csvs), "all generated prediction/claim flags remain false"),
        ("VAL1584_11_no_raw_accepted", not has_1584_rows(RAB_RAW) and not has_1584_rows(RAB_ACCEPTED), "no 1584 rows written to raw/accepted finite directories"),
        ("VAL1584_12_branch_copies", all(target_path.exists() for target_paths in COPY_TARGETS.values() for target_path in target_paths), "branch/quarantine nonclaim copies written"),
        ("VAL1584_13_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent after run"),
        ("VAL1584_14_formalization_untouched", formalization_scope_clean(generated_csvs), "all generated 1584 paths are outside formalization-workbench; git status is clean when available"),
    ]
    validation_data = [
        {
            "same_parent_branch_id": BRANCH_ID,
            "check_id": check_id,
            "result": "PASS" if passed else "FAIL",
            "detail": detail,
        }
        for check_id, passed, detail in checks
    ]
    validation_data.append(
        {
            "same_parent_branch_id": BRANCH_ID,
            "check_id": "VAL1584_OVERALL",
            "result": "PASS" if all(row["result"] == "PASS" for row in validation_data) else "FAIL",
            "detail": "1584 PPN beta/conservation/common matter gate validation",
        }
    )
    return validation_data


def md_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join(["---"] * len(columns)) + " |"
    body = ["| " + " | ".join(str(row.get(column, "")) for column in columns) + " |" for row in rows]
    return "\n".join([header, separator, *body])


def write_doc(
    sources: list[dict[str, Any]],
    beta_rows: list[dict[str, Any]],
    conservation_rows: list[dict[str, Any]],
    matter_rows: list[dict[str, Any]],
    newton_rows: list[dict[str, Any]],
    runner_rows: list[dict[str, Any]],
    claim_rows: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    validation_data: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
) -> None:
    DOC.write_text(
        "\n\n".join(
            [
                "# 1584 - PPN Beta, Conservation And Common Matter Gate",
                "## Verdict\n"
                "- The gamma/q_R_hat branch is not local GR: beta, source-compatible conservation, common matter coupling and source-normalized Newton remain separate gates.\n"
                "- A source-backed external beta bound exists, but no MTS beta_minus_1 prediction exists yet, so the beta comparator is not run.\n"
                "- Total Ward/Bianchi conservation is not enough: the projected Hilbert mass channel has explicit extra-current, projector-commutator and anomaly obstruction terms.\n"
                "- The common matter route is still the right route, but coframe ownership, tau lock, matter descent and no-marker clauses are unsigned.\n"
                "- No beta, PPN, local-GR, Newton, WEP, R10, clock, orbital, conservation or common-matter claim is made.",
                "## Source Register",
                md_table(sources, ["source_id", "source_path", "exists", "needle_found", "needles"]),
                "## PPN Beta Gate",
                md_table(beta_rows, ["beta_gate_id", "gate", "required_statement", "effect_if_signed", "status", "blocking_gap"]),
                "## Bianchi-Like Conservation Gate",
                md_table(conservation_rows, ["conservation_gate_id", "gate", "required_statement", "effect_if_signed", "status", "blocking_gap"]),
                "## Common Matter Coupling Gate",
                md_table(matter_rows, ["common_matter_gate_id", "gate", "required_statement", "effect_if_signed", "status", "blocking_gap"]),
                "## Newton Source Gate",
                md_table(newton_rows, ["newton_source_gate_id", "gate", "required_statement", "effect_if_signed", "status", "blocking_gap"]),
                "## GR Reduction Runner",
                md_table(runner_rows, ["runner_id", "case", "status", "reason", "can_score"]),
                "## Claim Gates",
                md_table(claim_rows, ["gate_id", "claim", "status", "reason"]),
                "## Decision",
                md_table(decisions, ["decision_id", "decision", "reason", "consequence"]),
                "## Validation",
                md_table(validation_data, ["check_id", "result", "detail"]),
                "## Next Target",
                md_table(next_rows, ["next_target", "script", "objective", "do_not"]),
            ]
        )
        + "\n",
        encoding="utf-8",
    )


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    sources = source_register_rows()
    beta_rows = beta_gate_rows()
    conservation_rows = conservation_gate_rows()
    matter_rows = common_matter_gate_rows()
    newton_rows = newton_source_gate_rows()
    runner_rows = gr_reduction_runner_rows()
    claim_rows = claim_gate_rows()
    decisions = decision_rows()
    next_rows = next_target_rows()
    generated_csvs = [
        SOURCE_REGISTER,
        BETA_GATE,
        CONSERVATION_GATE,
        COMMON_MATTER_GATE,
        NEWTON_SOURCE_GATE,
        GR_REDUCTION_RUNNER,
        CLAIM_GATE,
        DECISION,
        NEXT_TARGET,
    ]
    write_csv(SOURCE_REGISTER, sources)
    write_csv(BETA_GATE, beta_rows)
    write_csv(CONSERVATION_GATE, conservation_rows)
    write_csv(COMMON_MATTER_GATE, matter_rows)
    write_csv(NEWTON_SOURCE_GATE, newton_rows)
    write_csv(GR_REDUCTION_RUNNER, runner_rows)
    write_csv(CLAIM_GATE, claim_rows)
    write_csv(DECISION, decisions)
    write_csv(NEXT_TARGET, next_rows)
    copy_outputs()
    remove_pycache()
    validation_data = validation_rows(generated_csvs)
    write_csv(VALIDATION, validation_data)
    write_doc(sources, beta_rows, conservation_rows, matter_rows, newton_rows, runner_rows, claim_rows, decisions, validation_data, next_rows)


if __name__ == "__main__":
    main()
