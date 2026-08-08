import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


CHECKPOINT = "3795"
BRANCH = "MTS_R2FR_Y5_QFLOW_TWO_PAIR_LIFT_OR_BPERP_PROFILE_FIRST_INPUT_3795"
ROOT = Path(
    r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework"
    r"\Motion-TimeSpace--main"
)
PCW = ROOT / "post-checkpoint-work"
RESIDUALS = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "3795-Y5-R2FR-Qflow-two-pair-lift-or-Bperp-profile-first-input.md"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_3795_SOURCE_REGISTER.csv",
    "lift": RESIDUALS / "P8_Y5_R2FR_3795_QFLOW_TWO_PAIR_LIFT_ATTEMPT.csv",
    "nogos": RESIDUALS / "P8_Y5_R2FR_3795_QCOH_SHEAR_EIGENFRAME_NOGO_GUARDS.csv",
    "schema": RESIDUALS / "P8_Y5_R2FR_3795_BPERP_HPERP_FIRST_INPUT_SCHEMA.csv",
    "arenas": RESIDUALS / "P8_Y5_R2FR_3795_PROFILE_ARENA_SELECTION.csv",
    "gates": RESIDUALS / "P8_Y5_R2FR_3795_CLAIM_GATES.csv",
    "decisions": RESIDUALS / "P8_Y5_R2FR_3795_DECISION_ROWS.csv",
    "next_target": RESIDUALS / "P8_Y5_R2FR_3795_NEXT_TARGET.csv",
    "status": RESIDUALS / "P8_Y5_R2FR_3795_STATUS.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_3795_VALIDATION.csv",
}

SOURCE_SPECS = [
    {
        "source_id": "SRC3795_0_3794",
        "path": PCW / "3794-Y5-R2FR-parent-BQ-owner-constructor-two-pair-CP2-or-finite-profile.md",
        "needle": "Q-flow two-pair lift",
        "role": "handoff selecting Q-flow lift or finite profile",
    },
    {
        "source_id": "SRC3795_1_3793",
        "path": PCW / "3793-Y5-R2FR-BQ-descent-amplitude-or-eps-dBQ-bound.md",
        "needle": "eps_dBQ_A",
        "role": "Bperp/Hperp amplitude definitions",
    },
    {
        "source_id": "SRC3795_2_275_Qcoh",
        "path": PCW / "275-JC-three-form-memory-current-from-Q.md",
        "needle": "Q_coh^i_j = (N_D / u3) delta^i_j",
        "role": "coherent Q isotropic projection",
    },
    {
        "source_id": "SRC3795_3_275_shear",
        "path": PCW / "275-JC-three-form-memory-current-from-Q.md",
        "needle": "tracefree shear leaks into unprojected",
        "role": "shear leakage guard",
    },
    {
        "source_id": "SRC3795_4_1166",
        "path": PCW / "1166-Y5-R10-JC-from-Q-parent-variation-or-local-corner-certificate.md",
        "needle": "delta J_C = J_C Tr(Q^-1 delta Q) - J_C delta(log N_D)",
        "role": "Q/coframe determinant variation",
    },
    {
        "source_id": "SRC3795_5_1174",
        "path": PCW / "1174-Y5-R10-local-Qflow-stationarity-theorem-or-first-Qflow-bound-row.md",
        "needle": "Theta_Q := Tr(Q^{-1} delta Q) - delta(log N_D)",
        "role": "stationarity defect and projector/normalization blockers",
    },
    {
        "source_id": "SRC3795_6_1167",
        "path": PCW / "1167-Y5-R10-parent-volume-lock-selector-or-finite-edge-bound-fill.md",
        "needle": "local stationary domains",
        "role": "domain/no-flux local branch",
    },
    {
        "source_id": "SRC3795_7_spine",
        "path": PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md",
        "needle": "3795-Y5-R2FR-Qflow-two-pair-lift-or-Bperp-profile-first-input.md",
        "role": "live spine target",
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


def lift_rows(timestamp):
    rows = [
        {
            "attempt_id": "QL3795_0_required_lift",
            "object": "Y_Q=(C1,D1,C2,D2)",
            "construction": "Need a parent map F_Qflow from Q-flow primitives to four scalars with rank dY_Q=4 on U_good and fixed pairing omega_Q=dC1 wedge dD1+dC2 wedge dD2.",
            "derivation_status": "REQUIRED_CONDITION_EXACT",
            "result": "NOT_CURRENTLY_SUPPLIED",
            "reason": "current Q-flow sources define coherent volume and stationarity defect, not a four-scalar chart",
            "valid_for_claim": False,
        },
        {
            "attempt_id": "QL3795_1_Qcoh_only",
            "object": "Q_coh",
            "construction": "Q_coh^i_j=(N_D/u3) delta^i_j supplies one coherent scalar amplitude N_D/u3 and no eigenframe direction.",
            "derivation_status": "EXACT_NO_GO_FROM_ISOTROPY",
            "result": "FAIL_TWO_PAIR_LIFT",
            "reason": "isotropic Q_coh has degenerate eigenframe and cannot define four independent Clebsch scalars",
            "valid_for_claim": False,
        },
        {
            "attempt_id": "QL3795_2_tracefree_shear",
            "object": "S=Q-Q_coh",
            "construction": "Tracefree shear contains enough local components in principle, but 275 says unprojected shear leaks into det(Q) at second order and 1174 keeps Qcoh/projector ownership unsigned.",
            "derivation_status": "PROMISING_BUT_UNSIGNED",
            "result": "NO_CURRENT_ZERO",
            "reason": "using shear as Y_Q requires a parent-owned projector, smooth chart, eigenframe rule, and no post-hoc smoothing",
            "valid_for_claim": False,
        },
        {
            "attempt_id": "QL3795_3_eigenframe_chart",
            "object": "eigenvalues/eigenframe of Q or S",
            "construction": "A local nondegenerate diagonalization could provide scalar invariants plus angular/chart variables for two-pair data.",
            "derivation_status": "CONDITIONAL_CHART_ROUTE",
            "result": "BLOCKED_BY_DEGENERACY_AND_OWNER",
            "reason": "near Q_coh isotropy eigenframes are gauge/undefined; current sources do not define a parent chart or transition functions",
            "valid_for_claim": False,
        },
        {
            "attempt_id": "QL3795_4_conditional_success_theorem",
            "object": "Qflow two-pair lift",
            "construction": "If parent Q-flow supplies smooth chart variables Y_Q with rank four, chart covariance, q_obs descent, and no EM readout input, then B_Q=C1 dD1+C2 dD2 is parent-owned and 3793 amplitudes vanish when Lie_EA Y_Q=0 modulo chart gauge.",
            "derivation_status": "EXACT_CONDITIONAL_SUCCESS_THEOREM",
            "result": "THEOREM_RETAINED_NONCLAIM",
            "reason": "this is the precise success condition for the Q-flow route",
            "valid_for_claim": False,
        },
        {
            "attempt_id": "QL3795_5_current_verdict",
            "object": "strict current Q-flow lift",
            "construction": "Use only inspected current sources: Q_coh, N_D, Theta_Q_res, domain stationarity, and tracefree-shear warning.",
            "derivation_status": "CURRENT_CORPUS_TEST",
            "result": "FAIL_CURRENT_OWNER_PROMOTE_PROFILE_SCHEMA",
            "reason": "the current corpus does not deliver parent-owned Y_Q; finite Bperp/Hperp profile inputs are now required",
            "valid_for_claim": False,
        },
    ]
    for row in rows:
        row["timestamp_utc"] = timestamp
    return rows


def nogo_rows(timestamp):
    rows = [
        {
            "guard_id": "NG3795_0_isotropic_Qcoh",
            "risk": "claiming Q_coh alone owns generic B_Q",
            "rule": "Q_coh is proportional to identity, so it has one scalar amplitude and a degenerate eigenframe.",
            "failure_mode": "rank-four Clebsch chart is silently invented",
            "required_repair": "parent-owned tracefree/shear/eigenframe variables or explicit extension fields",
            "valid_for_claim": False,
        },
        {
            "guard_id": "NG3795_1_unprojected_shear",
            "risk": "using full det(Q) or raw shear as local-safe owner",
            "rule": "tracefree shear leaks into unprojected det(Q) at second order, so raw Q cannot be a local-GR-safe volume owner.",
            "failure_mode": "local shear/projector leakage hidden in the EM owner",
            "required_repair": "parent Qcoh projector plus finite shear/eigenframe bounds",
            "valid_for_claim": False,
        },
        {
            "guard_id": "NG3795_2_eigenframe_degeneracy",
            "risk": "using eigenvectors near coherent/isotropic states",
            "rule": "eigenframe charts are undefined or gauge-like at degenerate eigenvalues and must have transition functions.",
            "failure_mode": "fake smooth B_Q chart and fake Wilson silence",
            "required_repair": "chart atlas, degeneracy support certificate, or CP2-style smooth parent multiplet",
            "valid_for_claim": False,
        },
        {
            "guard_id": "NG3795_3_posthoc_projector",
            "risk": "choosing Q->Qcoh or Y_Q after seeing the desired EM field",
            "rule": "projector and two-pair extraction must be parent action data before EM readout.",
            "failure_mode": "renamed Maxwell field rather than derived B_Q",
            "required_repair": "parent variational owner for projector and extraction map",
            "valid_for_claim": False,
        },
        {
            "guard_id": "NG3795_4_single_pair",
            "risk": "using one phase-volume or one Q-flow pair as generic EM",
            "rule": "one pair gives H_Q wedge H_Q=0, so it cannot cover generic local EM rank.",
            "failure_mode": "simple-sector toy model reported as full Maxwell owner",
            "required_repair": "two independent pairs or CP2/higher multiplet",
            "valid_for_claim": False,
        },
    ]
    for row in rows:
        row["timestamp_utc"] = timestamp
    return rows


def schema_rows(timestamp):
    rows = [
        {
            "field_id": "BPI3795_0_arena",
            "column_name": "arena_id",
            "definition": "local arena label such as R10_lab, PPN_solar, clock_lab, orbital_source, or local_EM_bound_system",
            "units": "label",
            "required_for_claim": True,
            "current_value": "MISSING_ARENA_SELECTION",
            "valid_for_claim": False,
        },
        {
            "field_id": "BPI3795_1_Ugood",
            "column_name": "U_good_spec",
            "definition": "contractible defect-free weighted local patch with h_eff norm, A_ref, and F_ref",
            "units": "patch_descriptor",
            "required_for_claim": True,
            "current_value": "MISSING_PATCH_AND_NORM_SPEC",
            "valid_for_claim": False,
        },
        {
            "field_id": "BPI3795_2_YQ",
            "column_name": "Y_Q_source",
            "definition": "source path/theorem or data table for C1,D1,C2,D2 extracted before EM readout",
            "units": "source_path_or_theorem_id",
            "required_for_claim": True,
            "current_value": "MISSING_PARENT_YQ_OWNER",
            "valid_for_claim": False,
        },
        {
            "field_id": "BPI3795_3_projector",
            "column_name": "Qflow_projector_source",
            "definition": "parent-owned Q->Qcoh/shear/eigenframe projection rule and transition charts",
            "units": "source_path_or_theorem_id",
            "required_for_claim": True,
            "current_value": "MISSING_QFLOW_PROJECTOR_OWNER",
            "valid_for_claim": False,
        },
        {
            "field_id": "BPI3795_4_Bperp",
            "column_name": "Bperp_norm_over_Aref",
            "definition": "||B_perp||_A/A_ref or ||P_A Lie_EA B_perp||_A/A_ref on selected U_good",
            "units": "dimensionless",
            "required_for_claim": True,
            "current_value": "MISSING_BPERP_NORM",
            "valid_for_claim": False,
        },
        {
            "field_id": "BPI3795_5_Hperp",
            "column_name": "Hperp_norm_over_Fref",
            "definition": "||H_perp||_F/F_ref or ||Lie_EA H_perp||_F/F_ref on selected U_good",
            "units": "dimensionless",
            "required_for_claim": True,
            "current_value": "MISSING_HPERP_NORM",
            "valid_for_claim": False,
        },
        {
            "field_id": "BPI3795_6_companions",
            "column_name": "companion_residuals",
            "definition": "beta_Z,A, lambda_A, epsilon_J_Q, domain/tail, and defect/Wilson residuals attached to the same arena",
            "units": "dimensionless_or_declared_component_units",
            "required_for_claim": True,
            "current_value": "MISSING_COMPANION_RESIDUAL_VECTOR",
            "valid_for_claim": False,
        },
        {
            "field_id": "BPI3795_7_provenance",
            "column_name": "provenance_and_validity",
            "definition": "source paths, extraction method, confidence, valid_for_claim, and no-EM-readout certificate",
            "units": "metadata",
            "required_for_claim": True,
            "current_value": "MISSING_PROVENANCE",
            "valid_for_claim": False,
        },
    ]
    for row in rows:
        row["timestamp_utc"] = timestamp
    return rows


def arena_rows(timestamp):
    rows = [
        {
            "arena_id": "ARENA3795_0_R10_lab",
            "arena": "short_range_R10_lab",
            "why_first": "local finite-range/source coupling is sensitive to hidden EM/source residuals",
            "required_profile": "Bperp_norm_over_Aref;Hperp_norm_over_Fref;lambda_A;epsilon_J_Q;material/source labels",
            "units_policy": "dimensionless normalized local norms plus declared lambda units",
            "status": "SCHEMA_ONLY_VALUES_MISSING",
            "valid_for_claim": False,
        },
        {
            "arena_id": "ARENA3795_1_clock_lab",
            "arena": "atomic_clock_alpha_readout",
            "why_first": "alpha/readout drift directly tests Z_EM/qstar/B_Q leakage",
            "required_profile": "Bperp/Hperp;beta_Z,A;lambda_A;readout transfer;clock marker",
            "units_policy": "dimensionless fractional frequency or alpha-transfer residuals",
            "status": "SCHEMA_ONLY_VALUES_MISSING",
            "valid_for_claim": False,
        },
        {
            "arena_id": "ARENA3795_2_PPN_solar",
            "arena": "solar_system_PPN",
            "why_first": "gamma/beta limits bound stress/source projection leakage",
            "required_profile": "Hperp;epsilon_EM_Hilbert;epsilon_Poynting_domain;Pi_M_total source projection",
            "units_policy": "dimensionless PPN residual envelope",
            "status": "SCHEMA_ONLY_VALUES_MISSING",
            "valid_for_claim": False,
        },
        {
            "arena_id": "ARENA3795_3_orbital_source",
            "arena": "Newtonian_GM_orbital_source",
            "why_first": "tests whether EM/source residual hides inside measured GM",
            "required_profile": "Bperp/Hperp;mu_extra_EM;domain/tail;source theta;orbital readout",
            "units_policy": "dimensionless delta_mu or normalized source-mass residual",
            "status": "SCHEMA_ONLY_VALUES_MISSING",
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
            "gate_id": "CG3795_0_sources",
            "pass": True,
            "claim_allowed": False,
            "details": "all cited source paths and needles resolve",
        },
        {
            "timestamp_utc": timestamp,
            "gate_id": "CG3795_1_conditional_Qlift_theorem",
            "pass": True,
            "claim_allowed": False,
            "details": "conditional Q-flow two-pair success theorem emitted",
        },
        {
            "timestamp_utc": timestamp,
            "gate_id": "CG3795_2_Qcoh_only",
            "pass": False,
            "claim_allowed": False,
            "details": "Q_coh alone is isotropic and rank-insufficient",
        },
        {
            "timestamp_utc": timestamp,
            "gate_id": "CG3795_3_current_Qlift_owner",
            "pass": False,
            "claim_allowed": False,
            "details": "current corpus lacks parent projector/eigenframe/two-pair extraction",
        },
        {
            "timestamp_utc": timestamp,
            "gate_id": "CG3795_4_profile_schema",
            "pass": True,
            "claim_allowed": False,
            "details": "first Bperp/Hperp input schema and arenas emitted",
        },
        {
            "timestamp_utc": timestamp,
            "gate_id": "CG3795_5_local_GR_claim",
            "pass": False,
            "claim_allowed": False,
            "details": "no local-GR/EM claim; profile values and companion residuals remain missing",
        },
    ]


def decision_rows(timestamp):
    return [
        {
            "timestamp_utc": timestamp,
            "decision_id": "DEC3795_0_Qcoh_no_go",
            "decision": "Q_coh alone cannot be the generic B_Q owner because it is isotropic and one-scalar.",
            "action": "Do not claim a Qcoh-only EM owner.",
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "decision_id": "DEC3795_1_shear_fork",
            "decision": "Tracefree shear/eigenframe data are the only current Q-flow ingredients that could supply enough rank.",
            "action": "Require a parent-owned projector/eigenframe chart before using them.",
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "decision_id": "DEC3795_2_profile_schema",
            "decision": "Since current Q-flow lift is not signed, finite Bperp/Hperp profile rows are now the honest test track.",
            "action": "Use the emitted schema for the first concrete profile fill instead of another broad audit.",
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "decision_id": "DEC3795_3_next",
            "decision": "The next target should try one last constructive shear/eigenframe chart theorem; if it fails, fill arena profile rows.",
            "action": "Attempt parent Q-shear/eigenframe chart covariance or start R10/clock Bperp profile input.",
            "valid_for_claim": False,
        },
    ]


def next_target_rows(timestamp):
    return [
        {
            "timestamp_utc": timestamp,
            "target_file": "3796-Y5-R2FR-Qshear-eigenframe-chart-or-first-Bperp-arena-fill.md",
            "target_script": "scripts/Y5_R2FR_3796_Qshear_eigenframe_chart_or_first_Bperp_arena_fill.py",
            "objective": "Try to derive a parent-owned smooth Q-shear/eigenframe chart that supplies Y_Q without EM readout; if degeneracy/projector ownership fails, fill the first R10/clock Bperp-Hperp profile input rows with explicit missing values and units.",
            "valid_for_claim": False,
        }
    ]


def status_rows(timestamp):
    return [
        {
            "timestamp_utc": timestamp,
            "checkpoint_id": CHECKPOINT,
            "branch_id": BRANCH,
            "status": "QFLOW_TWO_PAIR_LIFT_CONDITIONAL_QCOH_ONLY_NO_GO_PROFILE_SCHEMA_EMITTED",
            "plain_verdict": "3795 tries the Q-flow two-pair lift. It proves the conditional success theorem but rejects the current strict lift: Q_coh is isotropic and one-scalar, while shear/eigenframe data are not parent-owned. The work now has a concrete Bperp/Hperp input schema and arena list for finite testing.",
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
        ("doc_written", DOC_PATH.exists(), "3795 markdown document written"),
        (
            "conditional_success",
            any(row["attempt_id"] == "QL3795_4_conditional_success_theorem" for row in grouped["lift"]),
            "conditional Q-flow two-pair theorem emitted",
        ),
        (
            "Qcoh_nogo",
            any(row["attempt_id"] == "QL3795_1_Qcoh_only" and row["result"] == "FAIL_TWO_PAIR_LIFT" for row in grouped["lift"]),
            "Qcoh-only no-go emitted",
        ),
        (
            "schema_fields",
            all(
                any(row["column_name"] == name for row in grouped["schema"])
                for name in ["arena_id", "Y_Q_source", "Bperp_norm_over_Aref", "Hperp_norm_over_Fref"]
            ),
            "first Bperp/Hperp schema fields emitted",
        ),
        (
            "arena_rows",
            len(grouped["arenas"]) >= 4,
            "four profile arenas emitted",
        ),
        (
            "local_gr_closed",
            any(row["gate_id"] == "CG3795_5_local_GR_claim" and row["pass"] is False for row in grouped["gates"]),
            "local-GR claim remains closed",
        ),
        (
            "next_target",
            grouped["next_target"][0]["target_file"].startswith("3796-"),
            "3796 Q-shear/eigenframe or first profile-fill target emitted",
        ),
        (
            "formalization_clean",
            not any("formalization-workbench" in str(path) for path in OUTPUTS.values()),
            "no 3795 files written under formalization-workbench",
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
        "# 3795 - Q-flow Two-Pair Lift or Bperp Profile First Input",
        "",
        "## Status",
        "",
        f"`{status['status']}`.",
        "",
        status["plain_verdict"],
        "",
        "## Result In Plain Terms",
        "",
        "3795 takes the Q-flow lift seriously and does not let it off easy. The conditional theorem works: if Q-flow gives four parent-owned scalars `Y_Q=(C1,D1,C2,D2)` with a fixed two-pair symplectic pairing, then `B_Q=C1 dD1+C2 dD2` is a genuine pre-EM owner and the 3793 `Bperp/Hperp` amplitudes can vanish locally.",
        "",
        "But the current inspected Q-flow route does not yet do that. `Q_coh` is proportional to the identity, so it carries one coherent scalar and a degenerate eigenframe. Raw tracefree shear has enough possible information, but it is exactly where projector ownership, smoothing, degeneracy, and local shear leakage become dangerous. Therefore the current Q-flow lift is conditional only, and the finite `Bperp/Hperp` profile schema is now the real test track.",
        "",
        "## Compact Result",
        "",
        "`Q_coh^i_j=(N_D/u3) delta^i_j` gives one scalar amplitude, not four Clebsch variables.",
        "",
        "A successful lift must supply `Y_Q=F_Qflow(Q,Q_coh,S,eigenframe,domain)` before EM readout, with `rank(dY_Q)=4` on `U_good`.",
        "",
        "Then `B_Q=C1 dD1+C2 dD2` and `H_Q=dC1 wedge dD1+dC2 wedge dD2`.",
        "",
        "Current verdict: `Y_Q_source`, `Qflow_projector_source`, `Bperp_norm_over_Aref`, and `Hperp_norm_over_Fref` remain missing.",
        "",
        render_section("Source Register", grouped["sources"], ["source_id"]),
        render_section("Q-flow Two-Pair Lift Attempt", grouped["lift"], ["attempt_id", "object"]),
        render_section("Qcoh/Shear/Eigenframe No-Go Guards", grouped["nogos"], ["guard_id", "risk"]),
        render_section("Bperp/Hperp First Input Schema", grouped["schema"], ["field_id", "column_name"]),
        render_section("Profile Arena Selection", grouped["arenas"], ["arena_id", "arena"]),
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
        "lift": lift_rows(timestamp),
        "nogos": nogo_rows(timestamp),
        "schema": schema_rows(timestamp),
        "arenas": arena_rows(timestamp),
        "gates": gate_rows(timestamp),
        "decisions": decision_rows(timestamp),
        "next_target": next_target_rows(timestamp),
        "status": status_rows(timestamp),
        "validation": [],
    }

    write_csv(OUTPUTS["sources"], grouped["sources"])
    write_csv(OUTPUTS["lift"], grouped["lift"])
    write_csv(OUTPUTS["nogos"], grouped["nogos"])
    write_csv(OUTPUTS["schema"], grouped["schema"])
    write_csv(OUTPUTS["arenas"], grouped["arenas"])
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
        raise SystemExit(f"3795 validation failed: {failures}")
    print("wrote 3795 checkpoint: Q-flow lift tried; Bperp/Hperp input schema emitted")


if __name__ == "__main__":
    main()
