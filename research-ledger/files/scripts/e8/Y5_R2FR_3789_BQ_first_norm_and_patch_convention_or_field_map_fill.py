import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


CHECKPOINT = "3789"
BRANCH = "MTS_R2FR_Y5_BQ_FIRST_NORM_AND_PATCH_CONVENTION_OR_FIELD_MAP_FILL_3789"
ROOT = Path(
    r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework"
    r"\Motion-TimeSpace--main"
)
PCW = ROOT / "post-checkpoint-work"
RESIDUALS = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "3789-Y5-R2FR-BQ-first-norm-and-patch-convention-or-field-map-fill.md"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_3789_SOURCE_REGISTER.csv",
    "patch_norm": RESIDUALS / "P8_Y5_R2FR_3789_PATCH_NORM_CONVENTION.csv",
    "chart_wilson": RESIDUALS / "P8_Y5_R2FR_3789_CHART_WILSON_LOCAL_ZERO_CONDITIONS.csv",
    "owner_map": RESIDUALS / "P8_Y5_R2FR_3789_OWNER_FIELD_MAP_ATTEMPT.csv",
    "rank_map": RESIDUALS / "P8_Y5_R2FR_3789_RANK_FIELD_MAP_ATTEMPT.csv",
    "component_ledger": RESIDUALS / "P8_Y5_R2FR_3789_UPDATED_RA_DRA_COMPONENT_LEDGER.csv",
    "claim_gates": RESIDUALS / "P8_Y5_R2FR_3789_CLAIM_GATES.csv",
    "decisions": RESIDUALS / "P8_Y5_R2FR_3789_DECISION_ROWS.csv",
    "next_target": RESIDUALS / "P8_Y5_R2FR_3789_NEXT_TARGET.csv",
    "status": RESIDUALS / "P8_Y5_R2FR_3789_STATUS.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_3789_VALIDATION.csv",
}

SOURCE_PATHS = [
    PCW / "3788-Y5-R2FR-BQ-first-coefficient-source-pack-RA-dRA.md",
    PCW / "3787-Y5-R2FR-BQ-finite-response-operators-and-arena-projection-map.md",
    PCW / "3786-Y5-R2FR-parent-internal-multiplet-owner-or-BQ-finite-demotion.md",
    PCW / "3785-Y5-R2FR-derive-BQ-flow-one-form-from-vorticity-defects-or-demote-EM.md",
    PCW / "3781-Y5-R2FR-construct-EM-connection-from-MTS-flow-or-bound-RA-betaZ.md",
    PCW / "3780-Y5-R2FR-vertical-EM-basicness-calculation-A-F-ZEM.md",
    PCW / "3779-Y5-R2FR-qobs-EM-readout-gauge-and-universal-ZEM-certificate.md",
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
            "source_role": "patch_norm_owner_rank_field_map_context",
            "valid_for_claim": False,
        }
        for path in SOURCE_PATHS
    ]


def patch_norm_rows(timestamp):
    rows = [
        {
            "convention_id": "PATCH3789_0_U_good_patch",
            "symbol": "U_good",
            "definition": "U is an open local test patch inside M minus defect/node support, chosen geodesically convex for g_eff, with H1(U)=0 and fixed compact support weight w_U",
            "mathematical_status": "DEFINED_CONDITIONAL_PATCH_CONTRACT",
            "numeric_status": "MISSING_ACTUAL_ARENA_DOMAIN",
            "claim_effect": "local chart/Wilson residues can be zeroed only inside such a patch",
        },
        {
            "convention_id": "PATCH3789_1_positive_norm_metric",
            "symbol": "h_eff(u_obs)",
            "definition": "positive local norm metric built from observed frame u_obs, e.g. h_ab=g_eff_ab+2 u_a u_b for signature -+++; use h_eff for amplitude norms instead of indefinite Lorentzian contraction",
            "mathematical_status": "DEFINED_NORM_CONVENTION",
            "numeric_status": "MISSING_U_OBS_AND_GEFF_COMPONENTS",
            "claim_effect": "prevents fake negative/zero field norms from Lorentzian signature",
        },
        {
            "convention_id": "PATCH3789_2_A_norm",
            "symbol": "||a||_A",
            "definition": "sqrt( int_U w_U |a|^2_h dV_h / int_U w_U dV_h ) for one-forms a",
            "mathematical_status": "DEFINED_NORM_CONVENTION",
            "numeric_status": "MISSING_FIELD_PROFILE_AND_WEIGHT",
            "claim_effect": "sets the response norm used by eps_BQ_descent_A, eps_BQ_chart_A, and eps_qA",
        },
        {
            "convention_id": "PATCH3789_3_F_norm",
            "symbol": "||f||_F",
            "definition": "sqrt( int_U w_U |f|^2_h dV_h / int_U w_U dV_h ) for two-forms f; equivalently local positive E/B amplitude in u_obs split",
            "mathematical_status": "DEFINED_NORM_CONVENTION",
            "numeric_status": "MISSING_FIELD_PROFILE_AND_WEIGHT",
            "claim_effect": "sets the response norm used by eps_dBQ_A, eps_dchart_A, eps_betaqF, eps_dbetaqA, and eps_rank_H",
        },
        {
            "convention_id": "PATCH3789_4_A_ref",
            "symbol": "A_ref",
            "definition": "A_ref=max(||A_obs||_A,A_floor); if ||A_obs||_A>0, self-normalization is allowed; otherwise A_floor must be sourced",
            "mathematical_status": "DEFINED_REFERENCE_CONVENTION",
            "numeric_status": "MISSING_A_OBS_PROFILE_OR_A_FLOOR",
            "claim_effect": "blocks division-by-zero and separates proof patches from measurement-floor patches",
        },
        {
            "convention_id": "PATCH3789_5_F_ref",
            "symbol": "F_ref",
            "definition": "F_ref=max(||F_obs||_F,F_floor); if ||F_obs||_F>0, self-normalization is allowed; otherwise F_floor must be sourced",
            "mathematical_status": "DEFINED_REFERENCE_CONVENTION",
            "numeric_status": "MISSING_F_OBS_PROFILE_OR_F_FLOOR",
            "claim_effect": "blocks division-by-zero and separates proof patches from measurement-floor patches",
        },
        {
            "convention_id": "PATCH3789_6_floor_policy",
            "symbol": "A_floor,F_floor",
            "definition": "floors may be instrument/noise floors, regularity cutoffs, or arena-declared minimum reference amplitudes; they cannot be fitted after seeing the target bound",
            "mathematical_status": "DEFINED_ANTI_FIT_POLICY",
            "numeric_status": "MISSING_SOURCE_BACKED_FLOORS",
            "claim_effect": "keeps tiny-field/vacuum patches from producing fake finite scores",
        },
    ]
    for row in rows:
        row["timestamp_utc"] = timestamp
        row["valid_for_claim"] = False
    return rows


def chart_wilson_rows(timestamp):
    rows = [
        {
            "chart_id": "CHART3789_0_local_zero_theorem",
            "condition": "U is contractible, H1(U)=0, local bundle trivialization exists, and defect/Wilson support is outside U",
            "result": "R_chart=d chi is pure local gauge and can be set to zero for the local response calculation; dR_chart=0",
            "component_effect": "eps_BQ_chart_A=0 and eps_dchart_A=0 conditionally on U_good",
            "status": "CONDITIONAL_LOCAL_THEOREM",
            "valid_for_claim": False,
        },
        {
            "chart_id": "CHART3789_1_nonlocal_residue",
            "condition": "U has nontrivial cycles, crosses a defect/node, or needs multiple chart overlaps with nonzero Wilson data",
            "result": "chart/Wilson residue is physical/topological until its cycles are owned or bounded",
            "component_effect": "eps_BQ_chart_A and eps_dchart_A remain live bound rows",
            "status": "GLOBAL_OR_DEFECT_BLOCKER",
            "valid_for_claim": False,
        },
        {
            "chart_id": "CHART3789_2_no_smuggling_rule",
            "condition": "local chart zero is used",
            "result": "the zero applies only to chart/Wilson bookkeeping, not to B_Q descent, q_* variation, Z_EM, same-current descent, or rank/owner failures",
            "component_effect": "prevents using local trivialization as a fake EM derivation",
            "status": "ACTIVE_GUARD",
            "valid_for_claim": False,
        },
    ]
    for row in rows:
        row["timestamp_utc"] = timestamp
    return rows


def owner_map_rows(timestamp):
    rows = [
        {
            "owner_map_id": "OWNER3789_0_field_map_definition",
            "object": "Delta B_owner",
            "definition": "Delta B_owner := B_Q - B_owned[Y_Q] on U, with eps_owner_B=||Delta B_owner||_A/A_ref",
            "requirement": "a parent-owned field class Y_Q and a non-circular operator B_owned[Y_Q] built without A_obs,F_obs,Maxwell equations, or Lorentz force",
            "current_status": "MISSING_OWNED_FIELD_CLASS_AND_OPERATOR",
            "claim_effect": "owner absence remains a model-class blocker until this map exists",
            "valid_for_claim": False,
        },
        {
            "owner_map_id": "OWNER3789_1_distance_class_fallback",
            "object": "dist_A(B_Q,Owned_B)",
            "definition": "eps_owner_dist := inf_{B in Owned_B(U)} ||B_Q-B||_A/A_ref",
            "requirement": "Owned_B(U) must be specified by the parent action before the infimum is meaningful",
            "current_status": "FORMAL_ONLY_NOT_COMPUTABLE",
            "claim_effect": "useful future bound shape, but not a present score",
            "valid_for_claim": False,
        },
        {
            "owner_map_id": "OWNER3789_2_zero_route",
            "object": "owner_zero",
            "definition": "if B_Q=B_owned[Y_Q] and Lie_EA Y_Q=0 modulo chart gauge, then eps_owner_B=0 and B_Q descent becomes a theorem target",
            "requirement": "parent-signed Y_Q or CP2/Berry multiplet plus q_obs descent",
            "current_status": "CONDITIONAL_NOT_SIGNED",
            "claim_effect": "shows exact route to closure without treating owner as a fitted coefficient",
            "valid_for_claim": False,
        },
    ]
    for row in rows:
        row["timestamp_utc"] = timestamp
    return rows


def rank_map_rows(timestamp):
    rows = [
        {
            "rank_map_id": "RANK3789_0_field_distance",
            "object": "eps_rank_H",
            "definition": "eps_rank_H := dist_F(H_req,R_rank(U))/F_ref, where H_req=-q_* F_obs and R_rank(U) is the allowed curvature class generated by the chosen B_Q branch",
            "requirement": "F_obs profile or symbolic target class, q_*, F_ref, and chosen rank class",
            "current_status": "FORMAL_FIELD_MAP_DEFINED_NUMERIC_INPUTS_MISSING",
            "claim_effect": "rank is no longer just a word; it becomes a curvature-distance residual once inputs exist",
            "valid_for_claim": False,
        },
        {
            "rank_map_id": "RANK3789_1_one_pair_gate",
            "object": "R_rank_one_pair",
            "definition": "one Clebsch pair gives H=dC wedge dD, hence H wedge H=0; any H_req with nonzero H_req wedge H_req cannot be exactly represented by one pair",
            "requirement": "evaluate H_req wedge H_req on U or prove it vanishes in the tested sector",
            "current_status": "GENERIC_EM_BLOCKS_ONE_PAIR_EXACTNESS",
            "claim_effect": "single-pair route is rejected for generic local EM unless the sector is null/simple",
            "valid_for_claim": False,
        },
        {
            "rank_map_id": "RANK3789_2_two_pair_gate",
            "object": "R_rank_two_pair_or_CP2",
            "definition": "two Clebsch pairs or a CP2/Berry-equivalent internal multiplet can represent a generic local closed two-form by Darboux/Clebsch on a good patch",
            "requirement": "parent-owned two-pair coordinates or CP2/Berry multiplet, plus chart covariance",
            "current_status": "RANK_ROUTE_OK_OWNER_ROUTE_MISSING",
            "claim_effect": "rank obstruction can be zero in the two-pair route, but only after owner is supplied",
            "valid_for_claim": False,
        },
        {
            "rank_map_id": "RANK3789_3_lower_bound_guard",
            "object": "wedge_defect_lower_bound",
            "definition": "nonzero H_req wedge H_req is a one-way certificate that one-pair exactness fails; converting it to a numeric lower bound needs the chosen F_norm and a norm-equivalence constant",
            "requirement": "norm-specific constant and field profile",
            "current_status": "CERTIFICATE_AVAILABLE_NUMERIC_BOUND_MISSING",
            "claim_effect": "prevents calling one-pair approximate success without a quantitative residual",
            "valid_for_claim": False,
        },
    ]
    for row in rows:
        row["timestamp_utc"] = timestamp
    return rows


def component_ledger_rows(timestamp):
    rows = [
        {
            "component_id": "COMP3789_0_eps_BQ_descent_A",
            "symbol": "eps_BQ_descent_A",
            "definition": "||q_*^-1 Lie_EA B_Q||_A/A_ref",
            "3789_update": "norm convention defined; component value still requires B_Q vertical descent amplitude or zero theorem",
            "status": "LIVE_NUMERIC_MISSING",
            "valid_for_claim": False,
        },
        {
            "component_id": "COMP3789_1_eps_BQ_chart_A",
            "symbol": "eps_BQ_chart_A",
            "definition": "||R_chart||_A/A_ref",
            "3789_update": "conditionally zero on U_good with H1(U)=0 and no defect/Wilson support",
            "status": "CONDITIONAL_LOCAL_ZERO_OR_LIVE_GLOBAL_RESIDUE",
            "valid_for_claim": False,
        },
        {
            "component_id": "COMP3789_2_eps_qA",
            "symbol": "eps_qA",
            "definition": "|beta_q,A| ||A_obs||_A/A_ref",
            "3789_update": "norm convention defined; next low-cost zero route is q_* superselection/charge-lattice ownership",
            "status": "LIVE_UNTIL_BETA_Q_ZERO_OR_BOUND",
            "valid_for_claim": False,
        },
        {
            "component_id": "COMP3789_3_eps_dBQ_A",
            "symbol": "eps_dBQ_A",
            "definition": "||q_*^-1 d(Lie_EA B_Q)||_F/F_ref",
            "3789_update": "norm convention defined; component value still requires differential B_Q descent amplitude",
            "status": "LIVE_NUMERIC_MISSING",
            "valid_for_claim": False,
        },
        {
            "component_id": "COMP3789_4_eps_dchart_A",
            "symbol": "eps_dchart_A",
            "definition": "||dR_chart||_F/F_ref",
            "3789_update": "conditionally zero on U_good; remains live for global/defect cycles",
            "status": "CONDITIONAL_LOCAL_ZERO_OR_LIVE_GLOBAL_RESIDUE",
            "valid_for_claim": False,
        },
        {
            "component_id": "COMP3789_5_eps_betaqF",
            "symbol": "eps_betaqF",
            "definition": "|beta_q,A| ||F_obs||_F/F_ref",
            "3789_update": "norm convention defined; next low-cost zero route is q_* superselection/charge-lattice ownership",
            "status": "LIVE_UNTIL_BETA_Q_ZERO_OR_BOUND",
            "valid_for_claim": False,
        },
        {
            "component_id": "COMP3789_6_eps_dbetaqA",
            "symbol": "eps_dbetaqA",
            "definition": "||d beta_q,A wedge A_obs||_F/F_ref",
            "3789_update": "zero if q_* is superselected or beta_q,A is constant on U; otherwise needs field profile",
            "status": "LIVE_UNTIL_BETA_Q_CONSTANT_ZERO_OR_BOUND",
            "valid_for_claim": False,
        },
        {
            "component_id": "COMP3789_7_eps_rank_H",
            "symbol": "eps_rank_H",
            "definition": "dist_F(H_req,R_rank(U))/F_ref",
            "3789_update": "formal field-valued map defined; numeric value requires H_req/F_obs, rank class, and F_ref",
            "status": "FORMAL_MAP_DEFINED_NUMERIC_MISSING",
            "valid_for_claim": False,
        },
        {
            "component_id": "COMP3789_8_eps_owner_B",
            "symbol": "eps_owner_B",
            "definition": "||B_Q-B_owned[Y_Q]||_A/A_ref or dist_A(B_Q,Owned_B)/A_ref",
            "3789_update": "formal route defined but current corpus lacks Owned_B and B_owned[Y_Q]",
            "status": "MODEL_CLASS_BLOCKER_UNTIL_PARENT_OWNER_SUPPLIED",
            "valid_for_claim": False,
        },
    ]
    for row in rows:
        row["timestamp_utc"] = timestamp
    return rows


def claim_gate_rows(timestamp):
    return [
        {
            "timestamp_utc": timestamp,
            "gate_id": "CG3789_0_sources",
            "pass": True,
            "claim_allowed": False,
            "details": "all cited local source paths resolve",
        },
        {
            "timestamp_utc": timestamp,
            "gate_id": "CG3789_1_patch_norm_contract",
            "pass": True,
            "claim_allowed": False,
            "details": "U_good, h_eff, A_norm, F_norm, A_ref, F_ref, and floor policy are now defined as a mathematical convention",
        },
        {
            "timestamp_utc": timestamp,
            "gate_id": "CG3789_2_chart_local_zero",
            "pass": True,
            "claim_allowed": False,
            "details": "chart/Wilson residue is conditionally zero on a contractible defect-free local patch only",
        },
        {
            "timestamp_utc": timestamp,
            "gate_id": "CG3789_3_owner_field_map",
            "pass": False,
            "claim_allowed": False,
            "details": "owner field map needs parent-owned Y_Q or Owned_B class; current corpus does not supply it",
        },
        {
            "timestamp_utc": timestamp,
            "gate_id": "CG3789_4_rank_field_map",
            "pass": True,
            "claim_allowed": False,
            "details": "rank residual can be represented as dist_F(H_req,R_rank)/F_ref, but numeric inputs are missing",
        },
        {
            "timestamp_utc": timestamp,
            "gate_id": "CG3789_5_numeric_score_ready",
            "pass": False,
            "claim_allowed": False,
            "details": "actual arena domains, field profiles, floors, owner map, beta_q, and rank distances are not numeric/source-backed",
        },
        {
            "timestamp_utc": timestamp,
            "gate_id": "CG3789_6_local_GR_EM_claim",
            "pass": False,
            "claim_allowed": False,
            "details": "no local-GR/EM claim; 3789 defines the scoring convention and one conditional chart zero only",
        },
    ]


def decision_rows(timestamp):
    return [
        {
            "timestamp_utc": timestamp,
            "decision_id": "DEC3789_0_norm_progress",
            "decision": "The first local norm convention is now defined without relying on indefinite Lorentzian amplitudes.",
            "action": "Use U_good, h_eff(u_obs), weighted local L2 norms, and A_ref/F_ref in future RA/dRA rows.",
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "decision_id": "DEC3789_1_chart_progress",
            "decision": "Chart/Wilson residues can be conditionally zeroed for a defect-free contractible local patch.",
            "action": "Do not use this local zero for global/topological claims or to hide B_Q descent, q_*, Z_EM, owner, or rank failures.",
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "decision_id": "DEC3789_2_owner_rank",
            "decision": "Rank can be made field-valued by a distance-to-rank-class map; owner cannot be scored until the owned B_Q class exists.",
            "action": "Keep owner as the hard blocker and use the rank distance map only as a formal nonclaim residual until inputs exist.",
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "decision_id": "DEC3789_3_next",
            "decision": "The next cheapest real derivation target is q_* superselection because it could zero eps_qA, eps_betaqF, and eps_dbetaqA.",
            "action": "Attempt a compact-charge-lattice q_* zero theorem; if it fails, emit beta_q bound rows.",
            "valid_for_claim": False,
        },
    ]


def next_target_rows(timestamp):
    return [
        {
            "timestamp_utc": timestamp,
            "target_file": "3790-Y5-R2FR-charge-unit-superselection-or-betaq-bound.md",
            "target_script": "scripts/Y5_R2FR_3790_charge_unit_superselection_or_betaq_bound.py",
            "objective": "Try to prove Lie_EA q_*=0 and d beta_q,A=0 from compact U(1) charge-lattice/superselection structure; otherwise emit source-ready beta_q bound rows for eps_qA, eps_betaqF, and eps_dbetaqA.",
            "valid_for_claim": False,
        }
    ]


def status_rows(timestamp):
    return [
        {
            "timestamp_utc": timestamp,
            "checkpoint_id": CHECKPOINT,
            "branch_id": BRANCH,
            "status": "PATCH_NORM_CONVENTION_DEFINED_CHART_ZERO_CONDITIONAL_OWNER_BLOCKED_RANK_MAP_FORMAL",
            "plain_verdict": "3789 defines the first honest local patch/norm convention for R_A and dR_A, gives a conditional chart/Wilson local zero theorem on defect-free contractible patches, converts rank into a formal distance-to-rank-class residual, and keeps owner as the hard missing parent-field blocker. It is not a local-GR/EM claim.",
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
        ("doc_written", DOC_PATH.exists(), "3789 markdown document written"),
        (
            "patch_norm_defined",
            len(grouped["patch_norm"]) >= 7
            and any(row["symbol"] == "||a||_A" for row in grouped["patch_norm"])
            and any(row["symbol"] == "||f||_F" for row in grouped["patch_norm"]),
            "patch and norm conventions emitted",
        ),
        (
            "chart_local_zero_conditional",
            any(row["chart_id"] == "CHART3789_0_local_zero_theorem" for row in grouped["chart_wilson"]),
            "conditional local chart/Wilson zero theorem emitted",
        ),
        (
            "owner_remains_blocked",
            any(row["owner_map_id"] == "OWNER3789_0_field_map_definition" and "MISSING" in row["current_status"] for row in grouped["owner_map"]),
            "owner map remains honestly blocked",
        ),
        (
            "rank_distance_map",
            any(row["rank_map_id"] == "RANK3789_0_field_distance" and "dist_F" in row["definition"] for row in grouped["rank_map"]),
            "rank field-distance map emitted",
        ),
        (
            "claim_gate_closed",
            any(row["gate_id"] == "CG3789_6_local_GR_EM_claim" and row["pass"] is False for row in grouped["claim_gates"]),
            "local GR/EM claim remains closed",
        ),
        (
            "next_target",
            grouped["next_target"][0]["target_file"].startswith("3790-"),
            "3790 q-star target emitted",
        ),
        (
            "formalization_clean",
            not any("formalization-workbench" in str(path) for path in OUTPUTS.values()),
            "no 3789 files written under formalization-workbench",
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
        "# 3789 - B_Q First Norm and Patch Convention or Field-Map Fill",
        "",
        "## Status",
        "",
        f"`{status['status']}`.",
        "",
        status["plain_verdict"],
        "",
        "## Result In Plain Terms",
        "",
        "3789 does not pretend to finish EM/local GR. It does something narrower but important: it defines the local patch and positive norm convention that the `R_A` and `dR_A` residuals must use, conditionally zeros pure chart/Wilson residue on a defect-free contractible patch, turns rank into a formal curvature-distance residual, and keeps owner failure as the hard parent-field blocker. That means future rows can be scored without inventing arbitrary coefficients, but the actual component amplitudes are still not claimable.",
        "",
        "## Compact Contract",
        "",
        "`U_good`: local, defect-free, geodesically convex, `H1(U)=0`, with compact support weight `w_U`.",
        "",
        "`||a||_A^2 = int_U w_U |a|_h^2 dV_h / int_U w_U dV_h` for one-forms.",
        "",
        "`||f||_F^2 = int_U w_U |f|_h^2 dV_h / int_U w_U dV_h` for two-forms.",
        "",
        "`A_ref=max(||A_obs||_A,A_floor)` and `F_ref=max(||F_obs||_F,F_floor)`.",
        "",
        "On `U_good`, `R_chart` is pure local gauge and `dR_chart=0`; outside `U_good`, chart/Wilson residue remains live.",
        "",
        "`eps_rank_H=dist_F(H_req,R_rank(U))/F_ref`, with `H_req=-q_* F_obs`.",
        "",
        render_section("Patch and Norm Convention", grouped["patch_norm"], ["convention_id", "symbol"]),
        render_section("Chart/Wilson Local Zero Conditions", grouped["chart_wilson"], ["chart_id"]),
        render_section("Owner Field Map Attempt", grouped["owner_map"], ["owner_map_id", "object"]),
        render_section("Rank Field Map Attempt", grouped["rank_map"], ["rank_map_id", "object"]),
        render_section("Updated R_A/dR_A Component Ledger", grouped["component_ledger"], ["component_id", "symbol"]),
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
        "patch_norm": patch_norm_rows(timestamp),
        "chart_wilson": chart_wilson_rows(timestamp),
        "owner_map": owner_map_rows(timestamp),
        "rank_map": rank_map_rows(timestamp),
        "component_ledger": component_ledger_rows(timestamp),
        "claim_gates": claim_gate_rows(timestamp),
        "decisions": decision_rows(timestamp),
        "next_target": next_target_rows(timestamp),
        "status": status_rows(timestamp),
        "validation": [],
    }

    write_csv(OUTPUTS["sources"], grouped["sources"])
    write_csv(OUTPUTS["patch_norm"], grouped["patch_norm"])
    write_csv(OUTPUTS["chart_wilson"], grouped["chart_wilson"])
    write_csv(OUTPUTS["owner_map"], grouped["owner_map"])
    write_csv(OUTPUTS["rank_map"], grouped["rank_map"])
    write_csv(OUTPUTS["component_ledger"], grouped["component_ledger"])
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
        raise SystemExit(f"3789 validation failed: {failures}")
    print("wrote 3789 checkpoint: patch/norm convention and owner/rank field-map fork emitted")


if __name__ == "__main__":
    main()
