import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


CHECKPOINT = "3788"
BRANCH = "MTS_R2FR_Y5_BQ_FIRST_COEFFICIENT_SOURCE_PACK_RA_DRA_3788"
ROOT = Path(
    r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework"
    r"\Motion-TimeSpace--main"
)
PCW = ROOT / "post-checkpoint-work"
RESIDUALS = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "3788-Y5-R2FR-BQ-first-coefficient-source-pack-RA-dRA.md"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_3788_SOURCE_REGISTER.csv",
    "derivation": RESIDUALS / "P8_Y5_R2FR_3788_RA_DRA_DERIVATION.csv",
    "norms": RESIDUALS / "P8_Y5_R2FR_3788_NORM_CONVENTION_PACK.csv",
    "coefficients": RESIDUALS / "P8_Y5_R2FR_3788_COEFFICIENT_STATUS.csv",
    "components": RESIDUALS / "P8_Y5_R2FR_3788_FIRST_COMPONENT_ROWS.csv",
    "claim_gates": RESIDUALS / "P8_Y5_R2FR_3788_CLAIM_GATES.csv",
    "decisions": RESIDUALS / "P8_Y5_R2FR_3788_DECISION_ROWS.csv",
    "next_target": RESIDUALS / "P8_Y5_R2FR_3788_NEXT_TARGET.csv",
    "status": RESIDUALS / "P8_Y5_R2FR_3788_STATUS.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_3788_VALIDATION.csv",
}

SOURCE_PATHS = [
    PCW / "3787-Y5-R2FR-BQ-finite-response-operators-and-arena-projection-map.md",
    PCW / "3786-Y5-R2FR-parent-internal-multiplet-owner-or-BQ-finite-demotion.md",
    PCW / "3785-Y5-R2FR-derive-BQ-flow-one-form-from-vorticity-defects-or-demote-EM.md",
    PCW / "3784-Y5-R2FR-parent-U1-action-clause-or-EM-finite-bound-mode.md",
    PCW / "3781-Y5-R2FR-construct-EM-connection-from-MTS-flow-or-bound-RA-betaZ.md",
    PCW / "3780-Y5-R2FR-vertical-EM-basicness-calculation-A-F-ZEM.md",
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
            "source_role": "RA_dRA_coefficient_derivation_context",
            "valid_for_claim": False,
        }
        for path in SOURCE_PATHS
    ]


def derivation_rows(timestamp):
    return [
        {
            "timestamp_utc": timestamp,
            "derivation_id": "RADER3788_0_RA_identity",
            "object": "R_A",
            "identity": "R_A=-q_*^-1 Lie_EA B_Q - beta_q,A A_obs + R_chart",
            "assumptions": "local phase-flow branch; A_obs=q_*^-1(d theta_Q-B_Q); vertical generator E_A in ker(Dq_obs); chart/Wilson changes collected in R_chart",
            "coefficient_result": "field-valued terms are additive before taking the norm",
            "status": "DERIVED_FROM_3781_3784_3787",
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "derivation_id": "RADER3788_1_dRA_identity",
            "object": "dR_A",
            "identity": "dR_A=-q_*^-1 d(Lie_EA B_Q) - d(beta_q,A) wedge A_obs - beta_q,A F_obs + dR_chart",
            "assumptions": "dF_obs=0 locally; d(A_obs)=F_obs; q_* fixed or its variation collected in beta_q,A; nonconstant beta_q,A kept as a separate field-valued residual",
            "coefficient_result": "field-valued derivative terms are additive before taking the norm",
            "status": "DERIVED_FROM_EXTERIOR_DERIVATIVE_OF_RA",
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "derivation_id": "RADER3788_2_RA_norm_bound",
            "object": "RA_normed",
            "identity": "RA_normed=||R_A||_A/A_ref <= eps_BQ_descent_A + eps_BQ_chart_A + eps_qA",
            "assumptions": "triangle inequality; A_ref=max(||A_obs||_A,A_floor); each epsilon is defined as its field norm divided by A_ref",
            "coefficient_result": "C_descent=C_chart=C_q=1 by definition of the normalized component residuals",
            "status": "COEFFICIENTS_NORMALIZED_NOT_NUMERIC",
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "derivation_id": "RADER3788_3_dRA_norm_bound",
            "object": "dRA_normed",
            "identity": "dRA_normed=||dR_A||_F/F_ref <= eps_dBQ_A + eps_dchart_A + eps_betaqF + eps_dbetaqA",
            "assumptions": "triangle inequality; F_ref=max(||F_obs||_F,F_floor); each epsilon is defined as its field norm divided by F_ref",
            "coefficient_result": "C_dBQ=C_dchart=C_betaqF=C_dbetaqA=1 by definition of the normalized component residuals",
            "status": "COEFFICIENTS_NORMALIZED_NOT_NUMERIC",
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "derivation_id": "RADER3788_4_owner_status",
            "object": "epsilon_BQ_owner",
            "identity": "epsilon_BQ_owner is not a finite RA coefficient until an owner failure is represented as a field-valued residual in R_A",
            "assumptions": "owner absence is a model-class blocker, not a vector one-form by itself",
            "coefficient_result": "C_owner is demoted from missing number to NOT_COEFFICIENT_VALUED_BLOCKER",
            "status": "BLOCKER_CLASSIFIED",
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "derivation_id": "RADER3788_5_rank_status",
            "object": "epsilon_BQ_rank",
            "identity": "epsilon_BQ_rank feeds dR_A only after rank defect is represented by a field-valued curvature mismatch Delta H_rank",
            "assumptions": "rank failure is not automatically a local two-form amplitude",
            "coefficient_result": "C_rank remains MISSING_FIELD_VALUED_DELTA_H_RANK",
            "status": "FIELD_MAP_REQUIRED",
            "valid_for_claim": False,
        },
    ]


def norm_rows(timestamp):
    rows = [
        (
            "NORM3788_0_A_norm",
            "||.||_A",
            "one-form norm on local patch U for A_obs and R_A",
            "MISSING_PATCH_METRIC_MEASURE_AND_FUNCTION_SPACE",
        ),
        (
            "NORM3788_1_F_norm",
            "||.||_F",
            "two-form norm on local patch U for F_obs and dR_A",
            "MISSING_PATCH_METRIC_MEASURE_AND_FUNCTION_SPACE",
        ),
        (
            "NORM3788_2_A_ref",
            "A_ref=max(||A_obs||_A,A_floor)",
            "normalizer for RA response rows",
            "MISSING_A_FLOOR_AND_DOMAIN",
        ),
        (
            "NORM3788_3_F_ref",
            "F_ref=max(||F_obs||_F,F_floor)",
            "normalizer for dRA response rows",
            "MISSING_F_FLOOR_AND_DOMAIN",
        ),
        (
            "NORM3788_4_U_patch",
            "U",
            "local contractible patch/domain over which Wilson and chart residues are separated",
            "MISSING_DOMAIN_SELECTION_RULE",
        ),
        (
            "NORM3788_5_chart_partition",
            "R_chart,dR_chart",
            "partition of chart/Wilson residue from physical B_Q descent leakage",
            "MISSING_PATCH_OVERLAP_AND_CYCLE_POLICY",
        ),
        (
            "NORM3788_6_metric_measure",
            "g_eff,Hodge,measure",
            "metric and measure used to compare one-form/two-form amplitudes",
            "MISSING_GEOMETRIC_NORM_SOURCE",
        ),
    ]
    return [
        {
            "timestamp_utc": timestamp,
            "norm_id": norm_id,
            "symbol": symbol,
            "definition": definition,
            "current_value": missing,
            "status": "REQUIRED_FOR_NUMERIC_SCORE",
            "valid_for_claim": False,
        }
        for norm_id, symbol, definition, missing in rows
    ]


def coefficient_rows(timestamp):
    raw = [
        ("COEFF3788_0_C_descent", "C_descent", "eps_BQ_descent_A -> RA_normed", "1", "EXACT_BY_DEFINITION", "eps_BQ_descent_A=||q_*^-1 Lie_EA B_Q||_A/A_ref"),
        ("COEFF3788_1_C_chart", "C_chart", "eps_BQ_chart_A -> RA_normed", "1", "EXACT_BY_DEFINITION", "eps_BQ_chart_A=||R_chart||_A/A_ref"),
        ("COEFF3788_2_C_q", "C_q", "eps_qA -> RA_normed", "1", "EXACT_BY_DEFINITION", "eps_qA=|beta_q,A| ||A_obs||_A/A_ref"),
        ("COEFF3788_3_C_dBQ", "C_dBQ", "eps_dBQ_A -> dRA_normed", "1", "EXACT_BY_DEFINITION", "eps_dBQ_A=||q_*^-1 d(Lie_EA B_Q)||_F/F_ref"),
        ("COEFF3788_4_C_dchart", "C_dchart", "eps_dchart_A -> dRA_normed", "1", "EXACT_BY_DEFINITION", "eps_dchart_A=||dR_chart||_F/F_ref"),
        ("COEFF3788_5_C_betaqF", "C_betaqF", "eps_betaqF -> dRA_normed", "1", "EXACT_BY_DEFINITION", "eps_betaqF=|beta_q,A| ||F_obs||_F/F_ref"),
        ("COEFF3788_6_C_dbetaqA", "C_dbetaqA", "eps_dbetaqA -> dRA_normed", "1", "EXACT_BY_DEFINITION", "eps_dbetaqA=||d beta_q,A wedge A_obs||_F/F_ref"),
        ("COEFF3788_7_C_owner", "C_owner", "epsilon_BQ_owner -> R_A", "NOT_NUMERIC", "NOT_COEFFICIENT_VALUED_BLOCKER", "owner absence must become a field-valued one-form residual before it has a coefficient"),
        ("COEFF3788_8_C_rank", "C_rank", "epsilon_BQ_rank -> dR_A", "MISSING_DELTA_H_RANK_MAP", "FIELD_MAP_REQUIRED", "rank defect must be mapped to Delta H_rank before coefficient assignment"),
    ]
    return [
        {
            "timestamp_utc": timestamp,
            "coefficient_id": coefficient_id,
            "symbol": symbol,
            "response_link": response_link,
            "coefficient_value": coefficient_value,
            "status": status,
            "definition_or_reason": definition,
            "valid_for_claim": False,
        }
        for coefficient_id, symbol, response_link, coefficient_value, status, definition in raw
    ]


def component_rows(timestamp):
    raw = [
        ("COMP3788_0_eps_BQ_descent_A", "eps_BQ_descent_A", "||q_*^-1 Lie_EA B_Q||_A/A_ref", "R_A", "MISSING_COMPONENT_VALUE", "needs B_Q vertical descent amplitude and A_norm"),
        ("COMP3788_1_eps_BQ_chart_A", "eps_BQ_chart_A", "||R_chart||_A/A_ref", "R_A", "MISSING_COMPONENT_VALUE", "needs chart/Wilson overlap or cycle policy"),
        ("COMP3788_2_eps_qA", "eps_qA", "|beta_q,A| ||A_obs||_A/A_ref", "R_A", "MISSING_COMPONENT_VALUE", "needs q_* vertical variation or superselection theorem"),
        ("COMP3788_3_eps_dBQ_A", "eps_dBQ_A", "||q_*^-1 d(Lie_EA B_Q)||_F/F_ref", "dR_A", "MISSING_COMPONENT_VALUE", "needs differential B_Q descent amplitude and F_norm"),
        ("COMP3788_4_eps_dchart_A", "eps_dchart_A", "||dR_chart||_F/F_ref", "dR_A", "MISSING_COMPONENT_VALUE", "needs chart derivative/cycle residue policy"),
        ("COMP3788_5_eps_betaqF", "eps_betaqF", "|beta_q,A| ||F_obs||_F/F_ref", "dR_A", "MISSING_COMPONENT_VALUE", "needs beta_q,A and F_ref"),
        ("COMP3788_6_eps_dbetaqA", "eps_dbetaqA", "||d beta_q,A wedge A_obs||_F/F_ref", "dR_A", "MISSING_COMPONENT_VALUE", "vanishes only if beta_q,A is constant/superselected on U"),
        ("COMP3788_7_eps_rank_H", "eps_rank_H", "||Delta H_rank||_F/F_ref", "dR_A_candidate", "MISSING_FIELD_VALUED_DELTA_H_RANK", "only meaningful if rank defect is converted to a curvature mismatch field"),
    ]
    return [
        {
            "timestamp_utc": timestamp,
            "component_id": component_id,
            "symbol": symbol,
            "definition": definition,
            "response_target": response_target,
            "current_value": current_value,
            "next_evidence": next_evidence,
            "valid_for_claim": False,
        }
        for component_id, symbol, definition, response_target, current_value, next_evidence in raw
    ]


def claim_gate_rows(timestamp):
    return [
        {
            "timestamp_utc": timestamp,
            "gate_id": "CG3788_0_sources",
            "pass": True,
            "claim_allowed": False,
            "details": "all cited local source paths resolve",
        },
        {
            "timestamp_utc": timestamp,
            "gate_id": "CG3788_1_RA_dRA_identities",
            "pass": True,
            "claim_allowed": False,
            "details": "R_A and dR_A identities derived from phase-flow/B_Q branch",
        },
        {
            "timestamp_utc": timestamp,
            "gate_id": "CG3788_2_normalized_coefficients",
            "pass": True,
            "claim_allowed": False,
            "details": "seven field-valued RA/dRA component coefficients are exactly 1 by norm definition",
        },
        {
            "timestamp_utc": timestamp,
            "gate_id": "CG3788_3_numeric_components",
            "pass": False,
            "claim_allowed": False,
            "details": "component amplitudes and norm/domain floors remain missing",
        },
        {
            "timestamp_utc": timestamp,
            "gate_id": "CG3788_4_owner_rank_field_maps",
            "pass": False,
            "claim_allowed": False,
            "details": "epsilon_BQ_owner and epsilon_BQ_rank are not numeric coefficients until field-valued residual maps exist",
        },
        {
            "timestamp_utc": timestamp,
            "gate_id": "CG3788_5_local_GR_EM_claim",
            "pass": False,
            "claim_allowed": False,
            "details": "no local-GR/EM/PPN claim; 3788 removes fake coefficient ambiguity but does not supply numeric residual values",
        },
    ]


def decision_rows(timestamp):
    return [
        {
            "timestamp_utc": timestamp,
            "decision_id": "DEC3788_0_real_progress",
            "decision": "The first RA/dRA coefficient pack is partly derived: descent, chart, q, dBQ, dchart, betaqF, and dbetaqA coefficients are exactly 1 under declared normalized residual definitions.",
            "action": "Replace vague C_descent/C_chart/C_q missing-number language with norm-defined component rows.",
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "decision_id": "DEC3788_1_owner_rank",
            "decision": "Owner and rank failures are not honest numeric coefficients yet.",
            "action": "Keep owner as a model-class blocker and rank as missing Delta H_rank field-map until either is converted into a field-valued residual.",
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "decision_id": "DEC3788_2_next",
            "decision": "The next bottleneck is no longer these first coefficients; it is the norm/patch convention and field-valued owner/rank maps.",
            "action": "Build 3789 to fix U, A_ref, F_ref, floor policy, chart partition, and decide whether rank/owner can be field-valued.",
            "valid_for_claim": False,
        },
    ]


def next_target_rows(timestamp):
    return [
        {
            "timestamp_utc": timestamp,
            "target_file": "3789-Y5-R2FR-BQ-first-norm-and-patch-convention-or-field-map-fill.md",
            "target_script": "scripts/Y5_R2FR_3789_BQ_first_norm_and_patch_convention_or_field_map_fill.py",
            "objective": "Set or source local patch norm conventions A_ref/F_ref/U/floor policy and either construct field-valued owner/rank residual maps or keep them as explicit claim blockers.",
            "valid_for_claim": False,
        }
    ]


def status_rows(timestamp):
    return [
        {
            "timestamp_utc": timestamp,
            "checkpoint_id": CHECKPOINT,
            "branch_id": BRANCH,
            "status": "RA_DRA_FIRST_COEFFICIENTS_NORMALIZED_OWNER_AND_RANK_FIELD_MAPS_MISSING",
            "plain_verdict": "3788 derives the first useful RA/dRA coefficient pack. Once the residuals are defined as response-normalized field norms, seven coefficients are exactly 1 by definition. This is concrete progress, not a claim: numeric amplitudes, patch norms, floor policy, and owner/rank field maps remain missing.",
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

    exact_one_rows = [
        row
        for row in grouped["coefficients"]
        if row["status"] == "EXACT_BY_DEFINITION"
    ]
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
        ("doc_written", DOC_PATH.exists(), "3788 markdown document written"),
        (
            "ra_dra_identities",
            any(row["derivation_id"] == "RADER3788_0_RA_identity" for row in grouped["derivation"])
            and any(row["derivation_id"] == "RADER3788_1_dRA_identity" for row in grouped["derivation"]),
            "RA and dRA identities emitted",
        ),
        (
            "exact_unit_coefficients",
            len(exact_one_rows) == 7 and all(row["coefficient_value"] == "1" for row in exact_one_rows),
            "seven normalized field-valued coefficients equal 1",
        ),
        (
            "owner_not_numeric",
            any(row["symbol"] == "C_owner" and row["status"] == "NOT_COEFFICIENT_VALUED_BLOCKER" for row in grouped["coefficients"]),
            "owner failure is not misreported as a numeric coefficient",
        ),
        (
            "rank_field_map_missing",
            any(row["symbol"] == "C_rank" and row["status"] == "FIELD_MAP_REQUIRED" for row in grouped["coefficients"]),
            "rank coefficient requires Delta H_rank field map",
        ),
        (
            "claim_gate_closed",
            any(row["gate_id"] == "CG3788_5_local_GR_EM_claim" and row["pass"] is False for row in grouped["claim_gates"]),
            "local GR/EM claim remains closed",
        ),
        (
            "next_target",
            grouped["next_target"][0]["target_file"].startswith("3789-"),
            "3789 norm/field-map target emitted",
        ),
        (
            "formalization_clean",
            not any("formalization-workbench" in str(path) for path in OUTPUTS.values()),
            "no 3788 files written under formalization-workbench",
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
        "# 3788 - B_Q First Coefficient Source Pack: R_A and dR_A",
        "",
        "## Status",
        "",
        f"`{status['status']}`.",
        "",
        status["plain_verdict"],
        "",
        "## Result In Plain Terms",
        "",
        "This checkpoint takes a real bite out of the coefficient problem. The first `R_A` and `dR_A` response coefficients do not need to be hunted as arbitrary fitted numbers if the component residuals are defined as response-normalized field norms. Under that convention, `C_descent`, `C_chart`, `C_q`, `C_dBQ`, `C_dchart`, `C_betaqF`, and `C_dbetaqA` are exactly `1` by definition. The owner and rank rows are not allowed to pretend to be numbers yet: owner absence is a model-class blocker, and rank failure needs a field-valued `Delta H_rank` map before it can enter `dR_A`.",
        "",
        "## Compact Formula",
        "",
        "`R_A=-q_*^-1 Lie_EA B_Q - beta_q,A A_obs + R_chart`.",
        "",
        "`dR_A=-q_*^-1 d(Lie_EA B_Q) - d(beta_q,A) wedge A_obs - beta_q,A F_obs + dR_chart`.",
        "",
        "`RA_normed <= eps_BQ_descent_A + eps_BQ_chart_A + eps_qA`.",
        "",
        "`dRA_normed <= eps_dBQ_A + eps_dchart_A + eps_betaqF + eps_dbetaqA`.",
        "",
        render_section("R_A and dR_A Derivation", grouped["derivation"], ["derivation_id", "object"]),
        render_section("Norm Convention Pack", grouped["norms"], ["norm_id", "symbol"]),
        render_section("Coefficient Status", grouped["coefficients"], ["coefficient_id", "symbol"]),
        render_section("First Component Rows", grouped["components"], ["component_id", "symbol"]),
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
        "derivation": derivation_rows(timestamp),
        "norms": norm_rows(timestamp),
        "coefficients": coefficient_rows(timestamp),
        "components": component_rows(timestamp),
        "claim_gates": claim_gate_rows(timestamp),
        "decisions": decision_rows(timestamp),
        "next_target": next_target_rows(timestamp),
        "status": status_rows(timestamp),
        "validation": [],
    }

    write_csv(OUTPUTS["sources"], grouped["sources"])
    write_csv(OUTPUTS["derivation"], grouped["derivation"])
    write_csv(OUTPUTS["norms"], grouped["norms"])
    write_csv(OUTPUTS["coefficients"], grouped["coefficients"])
    write_csv(OUTPUTS["components"], grouped["components"])
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
        raise SystemExit(f"3788 validation failed: {failures}")
    print("wrote 3788 checkpoint: RA/dRA first coefficient pack normalized")


if __name__ == "__main__":
    main()
