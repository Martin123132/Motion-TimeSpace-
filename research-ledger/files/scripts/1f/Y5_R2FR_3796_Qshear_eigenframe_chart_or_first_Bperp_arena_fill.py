import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


CHECKPOINT = "3796"
BRANCH = "MTS_R2FR_Y5_QSHEAR_EIGENFRAME_CHART_OR_FIRST_BPERP_ARENA_FILL_3796"
ROOT = Path(
    r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework"
    r"\Motion-TimeSpace--main"
)
PCW = ROOT / "post-checkpoint-work"
RESIDUALS = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "3796-Y5-R2FR-Qshear-eigenframe-chart-or-first-Bperp-arena-fill.md"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_3796_SOURCE_REGISTER.csv",
    "chart": RESIDUALS / "P8_Y5_R2FR_3796_QSHEAR_EIGENFRAME_CHART_THEOREM.csv",
    "audit": RESIDUALS / "P8_Y5_R2FR_3796_CURRENT_CORPUS_CHART_AUDIT.csv",
    "profile_rows": RESIDUALS / "P8_Y5_R2FR_3796_FIRST_BPERP_PROFILE_ROWS.csv",
    "components": RESIDUALS / "P8_Y5_R2FR_3796_QSHEAR_CHART_COMPONENTS.csv",
    "gates": RESIDUALS / "P8_Y5_R2FR_3796_CLAIM_GATES.csv",
    "decisions": RESIDUALS / "P8_Y5_R2FR_3796_DECISION_ROWS.csv",
    "next_target": RESIDUALS / "P8_Y5_R2FR_3796_NEXT_TARGET.csv",
    "status": RESIDUALS / "P8_Y5_R2FR_3796_STATUS.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_3796_VALIDATION.csv",
}

SOURCE_SPECS = [
    {
        "source_id": "SRC3796_0_3795",
        "path": PCW / "3795-Y5-R2FR-Qflow-two-pair-lift-or-Bperp-profile-first-input.md",
        "needle": "Q-shear/eigenframe chart",
        "role": "handoff to shear/eigenframe chart or profile rows",
    },
    {
        "source_id": "SRC3796_1_275_shear",
        "path": PCW / "275-JC-three-form-memory-current-from-Q.md",
        "needle": "tracefree shear leaks into unprojected",
        "role": "tracefree shear leakage guard",
    },
    {
        "source_id": "SRC3796_2_275_Qcoh",
        "path": PCW / "275-JC-three-form-memory-current-from-Q.md",
        "needle": "Q_coh^i_j = (N_D / u3) delta^i_j",
        "role": "coherent isotropic baseline",
    },
    {
        "source_id": "SRC3796_3_1174",
        "path": PCW / "1174-Y5-R10-local-Qflow-stationarity-theorem-or-first-Qflow-bound-row.md",
        "needle": "MISSING_QCOH_PROJECTOR_OWNER_OR_BOUND",
        "role": "projector ownership blocker",
    },
    {
        "source_id": "SRC3796_4_3793",
        "path": PCW / "3793-Y5-R2FR-BQ-descent-amplitude-or-eps-dBQ-bound.md",
        "needle": "B_Q=q_obs^*Bbar_Q+dchi+B_perp",
        "role": "Bperp/Hperp definitions",
    },
    {
        "source_id": "SRC3796_5_3791",
        "path": PCW / "3791-Y5-R2FR-ZEM-fixed-normalization-or-betaZ-bound.md",
        "needle": "lambda_A",
        "role": "Z_EM/lambda companion residual",
    },
    {
        "source_id": "SRC3796_6_3792",
        "path": PCW / "3792-Y5-R2FR-same-current-Ward-Hilbert-stress-owner-or-epsilonJ-bound.md",
        "needle": "epsilon_J_Q_total_abs",
        "role": "same-current companion residual",
    },
    {
        "source_id": "SRC3796_7_spine",
        "path": PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md",
        "needle": "3796-Y5-R2FR-Qshear-eigenframe-chart-or-first-Bperp-arena-fill.md",
        "role": "live spine handoff",
    },
]


def text_contains(path, needle):
    if not path.exists():
        return False
    return needle in path.read_text(encoding="utf-8", errors="replace")


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
            "source_id": spec["source_id"],
            "source_path": str(spec["path"]),
            "exists": spec["path"].exists(),
            "needle": spec["needle"],
            "needle_found": text_contains(spec["path"], spec["needle"]),
            "source_role": spec["role"],
            "valid_for_claim": False,
        }
        for spec in SOURCE_SPECS
    ]


def chart_rows(timestamp):
    rows = [
        {
            "theorem_id": "QSC3796_0_shear_split",
            "claim_piece": "coherent plus tracefree split",
            "mathematical_form": "Write Q=Q_coh+S with Q_coh=(N_D/u3)I and Tr(S)=0 on a selected local spatial coframe.",
            "derivation_status": "EXACT_DEFINITION_FROM_QFLOW_ROUTE",
            "zero_result_if_signed": "separates coherent volume mode from rank-carrying local shear data",
            "missing_for_current_claim": "parent-owned Qcoh projector and local coframe/domain selector",
        },
        {
            "theorem_id": "QSC3796_1_spectral_chart",
            "claim_piece": "local shear eigenframe chart",
            "mathematical_form": "On U_reg where S has three distinct eigenvalues, S=R diag(s1,s2,-s1-s2) R^T. The two eigenvalue scalars plus local frame angles provide up to five local coordinates.",
            "derivation_status": "EXACT_CONDITIONAL_SPECTRAL_THEOREM",
            "zero_result_if_signed": "Q-shear has enough local coordinate capacity to supply four Clebsch variables",
            "missing_for_current_claim": "parent-owned eigenframe chart, transition functions, and degeneracy support certificate",
        },
        {
            "theorem_id": "QSC3796_2_four_scalar_selector",
            "claim_piece": "Y_Q selector",
            "mathematical_form": "A parent selector Pi_4 may choose Y_Q=(C1,D1,C2,D2) from (s1,s2,alpha,beta,gamma) only if rank(dY_Q)=4 and Pi_4 is fixed before EM readout.",
            "derivation_status": "EXACT_CONDITIONAL_SELECTOR_REQUIREMENT",
            "zero_result_if_signed": "B_Q=C1 dD1+C2 dD2 is a Q-shear-owned two-pair connection",
            "missing_for_current_claim": "no current source supplies Pi_4 or proves rank-four on a physical U_good",
        },
        {
            "theorem_id": "QSC3796_3_degeneracy_no_go",
            "claim_piece": "coherent/local silence conflict",
            "mathematical_form": "At S=0 or repeated eigenvalues, the eigenframe is undefined up to rotations; this is exactly the local-silence/coherent limit where Qcoh is safest.",
            "derivation_status": "EXACT_DEGENERACY_GUARD",
            "zero_result_if_signed": "none; it blocks fake smooth eigenframe ownership",
            "missing_for_current_claim": "degeneracy atlas, support exclusion, or smooth CP2-style replacement",
        },
        {
            "theorem_id": "QSC3796_4_conditional_success",
            "claim_piece": "Q-shear B_Q owner success theorem",
            "mathematical_form": "If parent Q-flow owns Qcoh, S, an eigenframe atlas, Pi_4, q_obs descent, and no-EM-readout provenance, then Y_Q is parent-owned and 3794/3793 give B_perp=Hperp=0 on U_reg.",
            "derivation_status": "EXACT_CONDITIONAL_SUCCESS_THEOREM",
            "zero_result_if_signed": "eps_BQ_descent_A=eps_dBQ_A=0 on the signed regular patch",
            "missing_for_current_claim": "all ownership/chart/rank/degen clauses above",
        },
        {
            "theorem_id": "QSC3796_5_current_verdict",
            "claim_piece": "strict current corpus verdict",
            "mathematical_form": "Current sources identify shear as the only plausible rank-carrying Q-flow fork but do not parent-own the projector, eigenframe chart, selector, or degeneracy handling.",
            "derivation_status": "CONDITIONAL_THEOREM_CURRENT_FAILURE",
            "zero_result_if_signed": "not applicable in strict branch",
            "missing_for_current_claim": "finite Bperp/Hperp values or parent chart theorem",
        },
    ]
    for row in rows:
        row["timestamp_utc"] = timestamp
        row["valid_for_claim"] = False
    return rows


def audit_rows(timestamp):
    rows = [
        {
            "audit_id": "QSA3796_0_Qcoh",
            "source_signal": "Q_coh=(N_D/u3)I is isotropic",
            "current_result": "RANK_INSUFFICIENT",
            "impact": "cannot supply four Clebsch variables by itself",
            "valid_for_claim": False,
        },
        {
            "audit_id": "QSA3796_1_shear",
            "source_signal": "tracefree shear leaks into unprojected det(Q) at second order",
            "current_result": "RANK_CAPABLE_BUT_LOCAL_SAFETY_RISK",
            "impact": "shear can only be used if parent projector and finite leakage bounds are supplied",
            "valid_for_claim": False,
        },
        {
            "audit_id": "QSA3796_2_projector",
            "source_signal": "1174 marks Qcoh projector and N_D normalization as missing",
            "current_result": "PROJECTOR_UNSIGNED",
            "impact": "cannot distinguish parent physics from smoothing closure",
            "valid_for_claim": False,
        },
        {
            "audit_id": "QSA3796_3_chart",
            "source_signal": "no source supplies eigenframe atlas, transition functions, or Pi_4 selector",
            "current_result": "CHART_UNSIGNED",
            "impact": "conditional spectral theorem cannot be promoted",
            "valid_for_claim": False,
        },
        {
            "audit_id": "QSA3796_4_profile",
            "source_signal": "3795 profile schema exists but no values are filled",
            "current_result": "FIRST_PROFILE_ROWS_REQUIRED",
            "impact": "R10/clock rows should be populated with explicit missing values and units",
            "valid_for_claim": False,
        },
    ]
    for row in rows:
        row["timestamp_utc"] = timestamp
    return rows


def profile_rows(timestamp):
    rows = [
        {
            "row_id": "BPR3796_R10_0_Bperp",
            "arena_id": "R10_lab",
            "quantity": "Bperp_norm_over_Aref",
            "value": "MISSING_QSHEAR_EIGENFRAME_CHART_OR_BPERP_PROFILE",
            "units": "dimensionless",
            "source_path": str(DOC_PATH),
            "status": "REQUIRED_NOT_FILLED",
            "blocks_claim": True,
            "valid_for_claim": False,
        },
        {
            "row_id": "BPR3796_R10_1_Hperp",
            "arena_id": "R10_lab",
            "quantity": "Hperp_norm_over_Fref",
            "value": "MISSING_QSHEAR_EIGENFRAME_CHART_OR_HPERP_PROFILE",
            "units": "dimensionless",
            "source_path": str(DOC_PATH),
            "status": "REQUIRED_NOT_FILLED",
            "blocks_claim": True,
            "valid_for_claim": False,
        },
        {
            "row_id": "BPR3796_R10_2_lambda",
            "arena_id": "R10_lab",
            "quantity": "lambda_A",
            "value": "MISSING_LAMBDA_A_PRIOR_OR_OPERATOR_BAN",
            "units": "dimensionless_after_ZEM_normalization",
            "source_path": str(PCW / "3791-Y5-R2FR-ZEM-fixed-normalization-or-betaZ-bound.md"),
            "status": "COMPANION_REQUIRED_NOT_FILLED",
            "blocks_claim": True,
            "valid_for_claim": False,
        },
        {
            "row_id": "BPR3796_R10_3_epsilonJ",
            "arena_id": "R10_lab",
            "quantity": "epsilon_J_Q_total_abs",
            "value": "MISSING_EPSILON_JQ_COMPONENT_VALUES",
            "units": "dimensionless",
            "source_path": str(PCW / "3792-Y5-R2FR-same-current-Ward-Hilbert-stress-owner-or-epsilonJ-bound.md"),
            "status": "COMPANION_REQUIRED_NOT_FILLED",
            "blocks_claim": True,
            "valid_for_claim": False,
        },
        {
            "row_id": "BPR3796_CLOCK_0_Bperp",
            "arena_id": "clock_lab",
            "quantity": "Bperp_norm_over_Aref",
            "value": "MISSING_QSHEAR_EIGENFRAME_CHART_OR_BPERP_PROFILE",
            "units": "dimensionless",
            "source_path": str(DOC_PATH),
            "status": "REQUIRED_NOT_FILLED",
            "blocks_claim": True,
            "valid_for_claim": False,
        },
        {
            "row_id": "BPR3796_CLOCK_1_Hperp",
            "arena_id": "clock_lab",
            "quantity": "Hperp_norm_over_Fref",
            "value": "MISSING_QSHEAR_EIGENFRAME_CHART_OR_HPERP_PROFILE",
            "units": "dimensionless",
            "source_path": str(DOC_PATH),
            "status": "REQUIRED_NOT_FILLED",
            "blocks_claim": True,
            "valid_for_claim": False,
        },
        {
            "row_id": "BPR3796_CLOCK_2_betaZ",
            "arena_id": "clock_lab",
            "quantity": "beta_Z_A",
            "value": "MISSING_BETA_ZA_OR_PARENT_ZERO_THEOREM",
            "units": "dimensionless_vertical_derivative",
            "source_path": str(PCW / "3791-Y5-R2FR-ZEM-fixed-normalization-or-betaZ-bound.md"),
            "status": "COMPANION_REQUIRED_NOT_FILLED",
            "blocks_claim": True,
            "valid_for_claim": False,
        },
        {
            "row_id": "BPR3796_CLOCK_3_readout",
            "arena_id": "clock_lab",
            "quantity": "b_alpha_readout",
            "value": "MISSING_ALPHA_READOUT_DESCENT_OR_BOUND",
            "units": "dimensionless_fractional_readout",
            "source_path": str(PCW / "3791-Y5-R2FR-ZEM-fixed-normalization-or-betaZ-bound.md"),
            "status": "COMPANION_REQUIRED_NOT_FILLED",
            "blocks_claim": True,
            "valid_for_claim": False,
        },
    ]
    for row in rows:
        row["timestamp_utc"] = timestamp
        row["checkpoint_id"] = CHECKPOINT
    return rows


def component_rows(timestamp):
    rows = [
        {
            "component_id": "QSCOMP3796_0_projector",
            "symbol": "epsilon_Q_projector",
            "definition": "failure of parent-owned Q->Qcoh+S projector and N_D rule",
            "zero_if": "projector and normalization descend from parent action before smoothing/readout",
            "fallback_value": "MISSING_QCOH_PROJECTOR_OWNER_OR_BOUND",
            "feeds": "Y_Q_source;Bperp;Hperp;Theta_Q_res",
            "valid_for_claim": False,
        },
        {
            "component_id": "QSCOMP3796_1_eigenchart",
            "symbol": "epsilon_eigenchart",
            "definition": "failure of smooth eigenframe chart and transition functions on U_reg",
            "zero_if": "eigenvalues are nondegenerate on selected patch and parent chart atlas is supplied",
            "fallback_value": "MISSING_EIGENFRAME_CHART_ATLAS",
            "feeds": "Y_Q_source;Bperp;Wilson_defect",
            "valid_for_claim": False,
        },
        {
            "component_id": "QSCOMP3796_2_degeneracy",
            "symbol": "epsilon_eigen_degeneracy",
            "definition": "support or amplitude of repeated-eigenvalue/isotropic degeneracy where eigenframe is undefined",
            "zero_if": "degeneracy support is outside U_good, topologically owned, or replaced by smooth CP2 multiplet",
            "fallback_value": "MISSING_DEGENERACY_SUPPORT_CERTIFICATE",
            "feeds": "Bperp;Hperp;defect_Wilson",
            "valid_for_claim": False,
        },
        {
            "component_id": "QSCOMP3796_3_selector",
            "symbol": "epsilon_Pi4_selector",
            "definition": "failure of fixed parent selector Pi_4 choosing four scalars from five shear/eigenframe coordinates",
            "zero_if": "Pi_4 is parent action data and rank(dY_Q)=4 on U_good",
            "fallback_value": "MISSING_PARENT_PI4_SELECTOR",
            "feeds": "Y_Q_source;B_Q_owner",
            "valid_for_claim": False,
        },
    ]
    for row in rows:
        row["timestamp_utc"] = timestamp
    return rows


def gate_rows(timestamp):
    return [
        {
            "timestamp_utc": timestamp,
            "gate_id": "CG3796_0_sources",
            "pass": True,
            "claim_allowed": False,
            "details": "all cited source paths and needles resolve",
        },
        {
            "timestamp_utc": timestamp,
            "gate_id": "CG3796_1_spectral_theorem",
            "pass": True,
            "claim_allowed": False,
            "details": "conditional Q-shear eigenframe chart theorem emitted",
        },
        {
            "timestamp_utc": timestamp,
            "gate_id": "CG3796_2_current_chart_owner",
            "pass": False,
            "claim_allowed": False,
            "details": "current corpus lacks projector/eigenframe/Pi4/degen certificates",
        },
        {
            "timestamp_utc": timestamp,
            "gate_id": "CG3796_3_profile_rows",
            "pass": True,
            "claim_allowed": False,
            "details": "first R10/clock Bperp-Hperp rows emitted with explicit missing values and units",
        },
        {
            "timestamp_utc": timestamp,
            "gate_id": "CG3796_4_local_GR_claim",
            "pass": False,
            "claim_allowed": False,
            "details": "no local-GR/EM claim; finite rows are missing and companion residuals remain open",
        },
    ]


def decision_rows(timestamp):
    return [
        {
            "timestamp_utc": timestamp,
            "decision_id": "DEC3796_0_spectral_route",
            "decision": "Tracefree shear has enough local coordinate capacity only on nondegenerate regular patches.",
            "action": "Keep the spectral chart theorem as conditional and patch-local.",
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "decision_id": "DEC3796_1_current_failure",
            "decision": "Current sources do not parent-own the projector, eigenframe atlas, Pi4 selector, or degeneracy support.",
            "action": "Do not promote Q-shear to a derived B_Q owner.",
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "decision_id": "DEC3796_2_testing_move",
            "decision": "The project now has enough structure to begin finite profile row filling for R10 and clocks.",
            "action": "Move next to source acquisition or explicit symbolic profile estimates for Bperp/Hperp.",
            "valid_for_claim": False,
        },
    ]


def next_target_rows(timestamp):
    return [
        {
            "timestamp_utc": timestamp,
            "target_file": "3797-Y5-R2FR-first-Bperp-Hperp-profile-source-acquisition-R10-clock.md",
            "target_script": "scripts/Y5_R2FR_3797_first_Bperp_Hperp_profile_source_acquisition_R10_clock.py",
            "objective": "Fill or source the first R10/clock Bperp-Hperp profile inputs: patch/norm specification, parent Y_Q or explicit missing-owner row, Bperp/Hperp symbolic profile, and companion beta_Z/lambda/epsilon_J rows.",
            "valid_for_claim": False,
        }
    ]


def status_rows(timestamp):
    return [
        {
            "timestamp_utc": timestamp,
            "checkpoint_id": CHECKPOINT,
            "branch_id": BRANCH,
            "status": "QSHEAR_EIGENFRAME_CHART_CONDITIONAL_CURRENT_OWNER_UNSIGNED_FIRST_PROFILE_ROWS_EMITTED",
            "plain_verdict": "3796 derives the conditional Q-shear/eigenframe chart theorem: nondegenerate tracefree shear could supply enough local coordinates for Y_Q. Current sources do not parent-own the projector, eigenframe atlas, Pi4 selector, or degeneracy handling, so the owner claim stays closed and first R10/clock Bperp-Hperp profile rows are emitted with explicit missing values and units.",
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
            all(row["exists"] for row in grouped["sources"]),
            "every cited source path exists",
        ),
        (
            "needles_found",
            all(row["needle_found"] for row in grouped["sources"]),
            "every cited needle was found",
        ),
        (
            "csv_outputs_parse",
            all(csv_parses(path) for key, path in OUTPUTS.items() if key != "validation"),
            "all generated CSV outputs exist and parse",
        ),
        ("doc_written", DOC_PATH.exists(), "3796 markdown document written"),
        (
            "spectral_theorem",
            any(row["theorem_id"] == "QSC3796_1_spectral_chart" for row in grouped["chart"]),
            "conditional spectral chart theorem emitted",
        ),
        (
            "current_failure",
            any(row["audit_id"] == "QSA3796_3_chart" and row["current_result"] == "CHART_UNSIGNED" for row in grouped["audit"]),
            "current chart ownership failure recorded",
        ),
        (
            "profile_rows",
            all(
                any(row["arena_id"] == arena and row["quantity"] == quantity for row in grouped["profile_rows"])
                for arena, quantity in [
                    ("R10_lab", "Bperp_norm_over_Aref"),
                    ("R10_lab", "Hperp_norm_over_Fref"),
                    ("clock_lab", "Bperp_norm_over_Aref"),
                    ("clock_lab", "Hperp_norm_over_Fref"),
                ]
            ),
            "first R10/clock Bperp-Hperp rows emitted",
        ),
        (
            "missing_values_block",
            all(row["valid_for_claim"] is False and row["blocks_claim"] is True for row in grouped["profile_rows"]),
            "profile rows with missing values remain claim-blocking",
        ),
        (
            "local_gr_closed",
            any(row["gate_id"] == "CG3796_4_local_GR_claim" and row["pass"] is False for row in grouped["gates"]),
            "local-GR claim remains closed",
        ),
        (
            "next_target",
            grouped["next_target"][0]["target_file"].startswith("3797-"),
            "3797 profile source acquisition target emitted",
        ),
        (
            "formalization_clean",
            not any("formalization-workbench" in str(path) for path in OUTPUTS.values()),
            "no 3796 files written under formalization-workbench",
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
        "# 3796 - Q-shear Eigenframe Chart or First Bperp Arena Fill",
        "",
        "## Status",
        "",
        f"`{status['status']}`.",
        "",
        status["plain_verdict"],
        "",
        "## Result In Plain Terms",
        "",
        "3796 gives the Q-flow route its last fair constructive shot. Mathematically, tracefree shear can supply enough local coordinates: on a patch where the shear tensor has distinct eigenvalues, its two eigenvalue scalars plus eigenframe angles can provide four Clebsch variables for `B_Q=C1 dD1+C2 dD2`.",
        "",
        "But the current corpus does not yet own that chart. Near the coherent local-silence limit the eigenframe degenerates, and the projector/eigenframe/selector could become a smoothing closure if not derived from the parent action. So this checkpoint keeps the spectral route as a conditional theorem and emits the first R10/clock `Bperp-Hperp` rows with explicit missing values and units.",
        "",
        "## Compact Result",
        "",
        "`Q=Q_coh+S`, with `Q_coh=(N_D/u3)I` and `Tr(S)=0`.",
        "",
        "On `U_reg`, `S=R diag(s1,s2,-s1-s2) R^T`.",
        "",
        "A valid parent selector must choose `Y_Q=(C1,D1,C2,D2)` from `(s1,s2,alpha,beta,gamma)` before EM readout, with `rank(dY_Q)=4`.",
        "",
        "Current verdict: spectral theorem yes; parent-owned projector/eigenframe/Pi4/degen certificate no; first finite profile rows emitted.",
        "",
        render_section("Source Register", grouped["sources"], ["source_id"]),
        render_section("Q-shear Eigenframe Chart Theorem", grouped["chart"], ["theorem_id", "claim_piece"]),
        render_section("Current Corpus Chart Audit", grouped["audit"], ["audit_id"]),
        render_section("First Bperp/Hperp Profile Rows", grouped["profile_rows"], ["row_id", "arena_id", "quantity"]),
        render_section("Q-shear Chart Components", grouped["components"], ["component_id", "symbol"]),
        render_section("Claim Gates", grouped["gates"], ["gate_id"]),
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
        "chart": chart_rows(timestamp),
        "audit": audit_rows(timestamp),
        "profile_rows": profile_rows(timestamp),
        "components": component_rows(timestamp),
        "gates": gate_rows(timestamp),
        "decisions": decision_rows(timestamp),
        "next_target": next_target_rows(timestamp),
        "status": status_rows(timestamp),
        "validation": [],
    }

    write_csv(OUTPUTS["sources"], grouped["sources"])
    write_csv(OUTPUTS["chart"], grouped["chart"])
    write_csv(OUTPUTS["audit"], grouped["audit"])
    write_csv(OUTPUTS["profile_rows"], grouped["profile_rows"])
    write_csv(OUTPUTS["components"], grouped["components"])
    write_csv(OUTPUTS["gates"], grouped["gates"])
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
        raise SystemExit(f"3796 validation failed: {failures}")
    print("wrote 3796 checkpoint: Q-shear chart conditional; first Bperp profile rows emitted")


if __name__ == "__main__":
    main()
