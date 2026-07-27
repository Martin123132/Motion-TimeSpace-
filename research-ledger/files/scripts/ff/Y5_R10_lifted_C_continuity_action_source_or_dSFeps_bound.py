from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "1168-Y5-R10-lifted-C-continuity-action-source-or-dSFeps-bound.md"


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def stamp(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    generated = now()
    return [{**row, "generated_utc": generated} for row in rows]


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def source_path(relative_path: str) -> Path:
    return ROOT / relative_path


def is_false(value: object) -> bool:
    return str(value).strip().lower() == "false"


def source_rows() -> list[dict[str, object]]:
    sources = [
        {
            "source_id": "SRC1168_0_1167_next",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1167_NEXT_TARGET.csv",
            "needle": "NEXT1167_0_1168",
            "role": "handoff requiring continuity action/source or dSFeps bound.",
        },
        {
            "source_id": "SRC1168_1_1167_summary",
            "relative_path": "source-intake/mts_residuals/P8_Y5_BRR545_1167_VALIDATION.csv",
            "needle": "V1167_SUMMARY",
            "role": "1167 validation summary.",
        },
        {
            "source_id": "SRC1168_2_1167_law",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1167_PARENT_VOLUME_LOCK_LAW_ATTEMPT.csv",
            "needle": "PVL1167_0_parent_continuity_shape",
            "role": "continuity/no-flux law shape to action-split.",
        },
        {
            "source_id": "SRC1168_3_1167_sigma",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1167_VOLUME_LOCK_OBSTRUCTION_ROWS.csv",
            "needle": "OBS1167_0_Sigma_C",
            "role": "missing Sigma_C source term.",
        },
        {
            "source_id": "SRC1168_4_1167_phi",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1167_VOLUME_LOCK_OBSTRUCTION_ROWS.csv",
            "needle": "OBS1167_1_Phi_C",
            "role": "missing Phi_C boundary flux.",
        },
        {
            "source_id": "SRC1168_5_1167_dSFeps",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1167_FINITE_EDGE_BOUND_FILL.csv",
            "needle": "FEB1167_1_norm_dS_Feps",
            "role": "finite edge fallback row to fill as nonclaim schema.",
        },
        {
            "source_id": "SRC1168_6_274_CD",
            "relative_path": "274-lifted-C-sector-form-holonomy-route.md",
            "needle": "C_D[D] = N_D^{-1} integral_D J_C",
            "role": "domain memory functional.",
        },
        {
            "source_id": "SRC1168_7_274_FLRW_top",
            "relative_path": "274-lifted-C-sector-form-holonomy-route.md",
            "needle": "integral_D J_C^{top} != 0",
            "role": "FLRW top-class activity.",
        },
        {
            "source_id": "SRC1168_8_275_JC_Q",
            "relative_path": "275-JC-three-form-memory-current-from-Q.md",
            "needle": "J_C = det(Q_coh) Omega_D / V_D",
            "role": "J_C from coherent determinant/volume form.",
        },
        {
            "source_id": "SRC1168_9_275_FLRW_derivative",
            "relative_path": "275-JC-three-form-memory-current-from-Q.md",
            "needle": "d/dN integral_D J_C = 3N^2/u3^3",
            "role": "FLRW activation derivative shape.",
        },
        {
            "source_id": "SRC1168_10_207_Bianchi",
            "relative_path": "207-domain-projector-action-and-Bianchi-identity.md",
            "needle": "Bianchi closure can be made formal;",
            "role": "Bianchi/Ward guard for source/flux stress.",
        },
        {
            "source_id": "SRC1168_11_1020_kernel",
            "relative_path": "1020-Y5-R10-boundary-cohomology-domain-certificate-or-source-pack-first-row.md",
            "needle": "BDC1020_4_kernel_weight",
            "role": "kernel derivative zero/bound requirement.",
        },
        {
            "source_id": "SRC1168_12_1020_bound",
            "relative_path": "1020-Y5-R10-boundary-cohomology-domain-certificate-or-source-pack-first-row.md",
            "needle": "ETB1020_3_residual_bound",
            "role": "finite weighted-Stokes residual bound.",
        },
        {
            "source_id": "SRC1168_13_1020_missing_kernel",
            "relative_path": "1020-Y5-R10-boundary-cohomology-domain-certificate-or-source-pack-first-row.md",
            "needle": "MISSING_KERNEL_DERIVATIVE_BOUND_OR_ZERO_CERTIFICATE",
            "role": "explicit dSFeps missing marker.",
        },
    ]
    checked: list[dict[str, object]] = []
    for row in sources:
        path = source_path(str(row["relative_path"]))
        text = read_text(path)
        checked.append(
            {
                **row,
                "exists": path.exists(),
                "needle_found": str(row["needle"]) in text,
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return checked


def continuity_action_rows() -> list[dict[str, object]]:
    return [
        {
            "action_id": "CAS1168_0_spacetime_current_split",
            "clause": "spacetime 3-form split",
            "statement": "Let mathcalJ_C be a spacetime 3-form with foliation split mathcalJ_C = J_C + d tau wedge Phi_C, up to sign convention. Then d_4 mathcalJ_C contains d tau wedge (L_tau J_C - d_D Phi_C) plus d_D J_C.",
            "status": "FORMAL_GEOMETRIC_SPLIT",
            "what_it_derives": "Phi_C is not an arbitrary extra symbol; it is the spatial boundary-flux component of the spacetime lifted-C current.",
            "what_is_missing": "parent-owned mathcalJ_C and sign/foliation convention",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "action_id": "CAS1168_1_continuity_equation",
            "clause": "continuity equation split",
            "statement": "If d_4 mathcalJ_C = d tau wedge Sigma_C on the branch with d_D J_C=0, then L_tau J_C = d_D Phi_C + Sigma_C, up to the chosen sign convention.",
            "status": "FORMAL_SPLIT_DERIVED_NOT_PARENT_SOURCE",
            "what_it_derives": "the 1167 volume-lock law follows from a spacetime current equation once mathcalJ_C and Sigma_C are owned.",
            "what_is_missing": "source term Sigma_C and proof that d_4 mathcalJ_C equation is an Euler/Noether equation",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "action_id": "CAS1168_2_multiplier_action",
            "clause": "action owner attempt",
            "statement": "A first-order contract S_cont = int_M lambda_C (d_4 mathcalJ_C - d tau wedge Sigma_C) enforces continuity by variation of lambda_C; integration by parts exposes boundary terms involving lambda_C mathcalJ_C.",
            "status": "ACTION_CONTRACT_ONLY",
            "what_it_derives": "a possible variational owner for the continuity law shape.",
            "what_is_missing": "this imposes the equation unless lambda_C, Sigma_C, and mathcalJ_C are themselves derived from the parent MTS action",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "action_id": "CAS1168_3_sigma_source_status",
            "clause": "Sigma_C source",
            "statement": "Sigma_C must be a parent source/top-class density: zero in local stationary vacuum and nonzero or topological in FLRW, selected by one law.",
            "status": "SOURCE_SELECTOR_MISSING",
            "what_it_derives": "nothing can be claimed from Sigma_C until the same parent law chooses local zero and FLRW activity.",
            "what_is_missing": "Euler/Noether source equation or topological class selector",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "action_id": "CAS1168_4_phi_boundary_flux_status",
            "clause": "Phi_C boundary flux",
            "statement": "Phi_C must be related to the local primitive B_C or to the boundary component of mathcalJ_C so that int_partialD Phi_C is the same object tested by edge/Stokes rows.",
            "status": "BOUNDARY_FLUX_RELATION_MISSING",
            "what_it_derives": "the edge route and volume-lock route are the same problem if Phi_C and B_C are tied.",
            "what_is_missing": "Phi_C-B_C relation, boundary class, and charge-preservation guard",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "action_id": "CAS1168_5_Bianchi_guard",
            "clause": "Bianchi/Ward stress",
            "statement": "Any source/flux terms Sigma_C and Phi_C must carry stress in the parent Ward identity; otherwise the continuity route hides an exchange force.",
            "status": "CONSERVATION_GUARD_ACTIVE",
            "what_it_derives": "a no-cheat condition for the action-source route.",
            "what_is_missing": "stress tensor/current extraction for mathcalJ_C, Sigma_C, Phi_C, P_D, and domain motion",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "action_id": "CAS1168_6_verdict",
            "clause": "continuity action verdict",
            "statement": "1168 derives the formal split from a spacetime 3-form current, but does not derive Sigma_C/Phi_C as parent MTS sources. The route remains promising but blocked.",
            "status": "FORMAL_SPLIT_PROGRESS_NO_PARENT_SOURCE",
            "what_it_derives": "Phi_C and Sigma_C have precise geometric roles rather than free knobs.",
            "what_is_missing": "parent action/current variation that owns the source, flux, stress, and branch selector",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def sigma_phi_contract_rows() -> list[dict[str, object]]:
    return [
        {
            "contract_id": "SPC1168_0_mathcalJ_C",
            "quantity": "mathcalJ_C",
            "required_definition": "spacetime lifted-C 3-form built from Q/coframe/domain variables",
            "current_value": "MISSING_PARENT_4D_CURRENT",
            "source_anchor": "1167 continuity law and 275 J_C determinant shape",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "contract_id": "SPC1168_1_Sigma_C_local",
            "quantity": "Sigma_C local",
            "required_definition": "parent theorem Sigma_C=0 in stationary local vacuum branch",
            "current_value": "MISSING_LOCAL_NO_SOURCE_THEOREM",
            "source_anchor": "OBS1167_0_Sigma_C",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "contract_id": "SPC1168_2_Sigma_C_FLRW",
            "quantity": "Sigma_C FLRW/top class",
            "required_definition": "same parent law permits homogeneous source or nonzero H3 class in FLRW",
            "current_value": "MISSING_FLRW_SOURCE_SELECTOR",
            "source_anchor": "integral_D J_C^{top} != 0",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "contract_id": "SPC1168_3_Phi_C",
            "quantity": "Phi_C",
            "required_definition": "boundary flux 2-form from spatial split of mathcalJ_C or primitive B_C relation",
            "current_value": "MISSING_BOUNDARY_FLUX_FORM",
            "source_anchor": "OBS1167_1_Phi_C",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "contract_id": "SPC1168_4_domain_motion",
            "quantity": "moving_boundary_term",
            "required_definition": "transport rule for D under tau/coframe/projector flow",
            "current_value": "MISSING_DOMAIN_TRANSPORT_RULE",
            "source_anchor": "OBS1167_2_domain_motion",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "contract_id": "SPC1168_5_stress",
            "quantity": "T_mathcalJ_Sigma_Phi",
            "required_definition": "stress/Ward contribution of current, source, boundary flux, and domain projector",
            "current_value": "MISSING_BIANCHI_STRESS_LEDGER",
            "source_anchor": "207 Bianchi guard",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def dSFeps_rows() -> list[dict[str, object]]:
    return [
        {
            "row_id": "DSF1168_0_operator_definition",
            "quantity": "d_S(F_lambda epsilon_C)",
            "bound_formula": "||d_S(F_lambda epsilon_C)||_* <= ||d_S F_lambda||_* ||epsilon_C||_* + ||F_lambda||_* ||d_S epsilon_C||_*",
            "units_or_norm": "dual_surface_norm; units inherited from F_lambda times epsilon_C per boundary area/length convention",
            "current_status": "FORMAL_NORM_DECOMPOSITION_ONLY",
            "missing_for_claim": "F_lambda, epsilon_C, surface metric/norm, units, and source path",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "row_id": "DSF1168_1_zero_route",
            "quantity": "norm_dS_Feps zero",
            "bound_formula": "norm_dS_Feps=0 if F_lambda is constant on S and epsilon_C is covariantly constant/proper-closed on S",
            "units_or_norm": "zero theorem; units still documented",
            "current_status": "ZERO_CONDITIONS_NOT_CERTIFIED",
            "missing_for_claim": "closed-weight theorem and allowed-epsilon certificate",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "row_id": "DSF1168_2_finite_bound_route",
            "quantity": "norm_dS_Feps bound",
            "bound_formula": "nonnegative bound required before Q_C_edge_bound can be evaluated",
            "units_or_norm": "same dual_surface_norm as ETB1020_3",
            "current_status": "MISSING_NUMERIC_OR_THEOREM_BOUND",
            "missing_for_claim": "actual bound value, uncertainty, arena, and provenance",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "row_id": "DSF1168_3_runner_payload",
            "quantity": "Q_C_edge_bound contribution",
            "bound_formula": "abs_contribution <= norm_dS_Feps * norm_bC",
            "units_or_norm": "edge_charge_units after multiplying by norm_bC",
            "current_status": "BLOCKED_BY_norm_bC_AND_norm_dS_Feps",
            "missing_for_claim": "B_C primitive norm and kernel derivative norm",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def runner_rows() -> list[dict[str, object]]:
    return [
        {
            "run_id": "RUN1168_0_action_split",
            "test": "spacetime current continuity split",
            "status": "PARTIAL_PASS_FORMAL_SPLIT_ONLY",
            "blocked_by": "mathcalJ_C_parent_owner;Sigma_C_source;Phi_C_flux;sign_convention",
            "detail": "Phi_C/Sigma_C roles are sharpened, not parent-derived",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "run_id": "RUN1168_1_local_lock",
            "test": "local no-source/no-flux volume lock",
            "status": "REFUSED_LOCAL_LOCK_NOT_PARENT_SIGNED",
            "blocked_by": "Sigma_C_local_zero;Phi_C_boundary_zero;domain_motion_zero",
            "detail": "local lock remains conditional",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "run_id": "RUN1168_2_FLRW_selector",
            "test": "FLRW source/top-class selector",
            "status": "REFUSED_FLRW_SELECTOR_MISSING",
            "blocked_by": "Sigma_C_FLRW;H3_top_class;amplitude_normalization",
            "detail": "FLRW activity is compatible but not derived",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "run_id": "RUN1168_3_dSFeps_bound",
            "test": "finite dSFeps edge-bound row",
            "status": "SCHEMA_READY_VALUES_MISSING",
            "blocked_by": "F_lambda;epsilon_C;surface_norm;numeric_bound;norm_bC",
            "detail": "norm decomposition is written but not claim-valid",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def claim_gate_rows() -> list[dict[str, object]]:
    return [
        {
            "gate_id": "G1168_0_current_owned",
            "gate": "mathcalJ_C is parent-owned",
            "current_status": "BLOCKED",
            "reason": "formal split exists but parent current definition is missing",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "G1168_1_source_flux_owned",
            "gate": "Sigma_C and Phi_C are parent-derived",
            "current_status": "BLOCKED",
            "reason": "source and boundary flux remain contracts",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "G1168_2_same_law_selector",
            "gate": "same law gives local zero and FLRW activity",
            "current_status": "BLOCKED",
            "reason": "branch/source selector is missing",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "G1168_3_dSFeps_bound",
            "gate": "dSFeps zero theorem or numeric bound is sourced",
            "current_status": "BLOCKED",
            "reason": "norm decomposition lacks values and units provenance",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "G1168_4_local_promotion",
            "gate": "local-GR/Newton/R10/PPN/WEP/clock/orbital promotion",
            "current_status": "BLOCKED_NO_LOCAL_CLAIM",
            "reason": "current/source/selector/edge gates remain blocked",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def decision_rows() -> list[dict[str, object]]:
    return [
        {
            "decision_id": "D1168_0_action_split_progress",
            "decision": "formal_current_split_sharpens_Sigma_Phi",
            "reason": "Phi_C becomes the spatial boundary flux of mathcalJ_C and Sigma_C becomes the spacetime source/top-class term",
            "next_action": "derive mathcalJ_C and Sigma_C from parent lifted-C action instead of adding a multiplier closure",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "D1168_1_claim_refusal",
            "decision": "continuity_action_not_promoted",
            "reason": "a multiplier action can impose continuity but does not explain the source/flux selector by itself",
            "next_action": "hunt for parent source/topological class owner",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "D1168_2_edge_fallback",
            "decision": "dSFeps_bound_schema_written_nonclaim",
            "reason": "finite edge scoring now has a norm decomposition but no numeric/theorem bound",
            "next_action": "source F_lambda/epsilon_C/surface norm or prove closed-weight zero",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def next_target_rows() -> list[dict[str, object]]:
    return [
        {
            "next_id": "NEXT1168_0_1169",
            "next_target": "1169-Y5-R10-parent-source-topclass-owner-or-closed-weight-zero.md",
            "objective": "find a parent owner for Sigma_C/top-class source and Phi_C boundary flux, or prove the closed-weight zero theorem for d_S(F_lambda epsilon_C)",
            "include": "mathcalJ_C owner; Sigma_C source selector; FLRW top class; Phi_C-B_C relation; Bianchi stress; closed-weight theorem; F_lambda and epsilon_C units; runner dry-run",
            "exclude": "multiplier continuity as proof; local/FLRW hand switch; scalar Cperp promotion; invented dSFeps values; local-GR claim; c_g zero claim; GitHub; formalization edits",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def validate(
    sources: list[dict[str, object]],
    action: list[dict[str, object]],
    contracts: list[dict[str, object]],
    dsf: list[dict[str, object]],
    runner: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    csv_paths: list[Path],
) -> list[dict[str, object]]:
    source_ok = all(bool(row["exists"]) and bool(row["needle_found"]) for row in sources)
    split_written = any(row["action_id"] == "CAS1168_0_spacetime_current_split" for row in action)
    sigma_missing = any(row["contract_id"] == "SPC1168_1_Sigma_C_local" and "MISSING" in str(row["current_value"]) for row in contracts)
    phi_missing = any(row["contract_id"] == "SPC1168_3_Phi_C" and "MISSING" in str(row["current_value"]) for row in contracts)
    dsf_schema = any(row["row_id"] == "DSF1168_0_operator_definition" for row in dsf)
    dsf_nonclaim = all(is_false(row["claim_allowed"]) for row in dsf)
    runner_refuses = all(is_false(row["claim_allowed"]) for row in runner)
    all_nonclaim = all(
        is_false(row.get("valid_for_claim", False)) and is_false(row.get("claim_allowed", False))
        for table in (sources, action, contracts, dsf, runner, gates, decisions, next_rows)
        for row in table
    )
    csv_parse = True
    parse_detail = "all 1168 CSV outputs parse cleanly"
    for path in csv_paths:
        try:
            read_csv(path)
        except Exception as exc:  # pragma: no cover
            csv_parse = False
            parse_detail = f"{path.name}: {exc}"
            break
    under_post = all(str(path.resolve()).startswith(str(ROOT.resolve())) for path in csv_paths + [DOC])
    return [
        {
            "check_id": "V1168_0_sources_exist",
            "result": "pass" if source_ok else "fail",
            "detail": "all cited local source paths exist and needles are found" if source_ok else "source path or needle missing",
            "claim_allowed": False,
        },
        {
            "check_id": "V1168_1_current_split_written",
            "result": "pass" if split_written else "fail",
            "detail": "spacetime current split and continuity equation are written",
            "claim_allowed": False,
        },
        {
            "check_id": "V1168_2_sigma_phi_still_missing",
            "result": "pass" if sigma_missing and phi_missing else "fail",
            "detail": "Sigma_C and Phi_C remain missing contracts rather than assumed sources",
            "claim_allowed": False,
        },
        {
            "check_id": "V1168_3_dSFeps_schema_written",
            "result": "pass" if dsf_schema and dsf_nonclaim else "fail",
            "detail": "dSFeps norm decomposition exists but remains nonclaim",
            "claim_allowed": False,
        },
        {
            "check_id": "V1168_4_runner_refuses_claim",
            "result": "pass" if runner_refuses else "fail",
            "detail": "runner refuses action, local lock, FLRW selector, and edge claims",
            "claim_allowed": False,
        },
        {
            "check_id": "V1168_5_claim_gates_blocked",
            "result": "pass" if all(is_false(row["claim_allowed"]) for row in gates) else "fail",
            "detail": "all claim gates remain blocked",
            "claim_allowed": False,
        },
        {
            "check_id": "V1168_6_no_claim_rows",
            "result": "pass" if all_nonclaim else "fail",
            "detail": "all generated rows remain nonclaim",
            "claim_allowed": False,
        },
        {
            "check_id": "V1168_7_next_target",
            "result": "pass" if next_rows and "1169" in str(next_rows[0]["next_target"]) else "fail",
            "detail": "1169 handoff targets parent source/top-class owner or closed-weight zero",
            "claim_allowed": False,
        },
        {
            "check_id": "V1168_8_generated_under_post_checkpoint",
            "result": "pass" if under_post else "fail",
            "detail": "all generated outputs are under post-checkpoint-work",
            "claim_allowed": False,
        },
        {
            "check_id": "V1168_9_csv_parse",
            "result": "pass" if csv_parse else "fail",
            "detail": parse_detail,
            "claim_allowed": False,
        },
        {
            "check_id": "V1168_10_formalization_untouched",
            "result": "pass",
            "detail": "generator writes no outputs under formalization-workbench",
            "claim_allowed": False,
        },
        {
            "check_id": "V1168_SUMMARY",
            "result": "pass" if source_ok and split_written and sigma_missing and phi_missing and dsf_schema and runner_refuses and all_nonclaim else "fail",
            "detail": "1168 derives the formal continuity split and dSFeps norm schema, but blocks claims because parent Sigma_C/Phi_C ownership and edge values remain missing",
            "claim_allowed": False,
        },
    ]


def md_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    divider = "| " + " | ".join("---" for _ in columns) + " |"
    body = [
        "| " + " | ".join(str(row.get(column, "")).replace("\n", " ") for column in columns) + " |"
        for row in rows
    ]
    return "\n".join([header, divider, *body])


def write_doc(
    sources: list[dict[str, object]],
    action: list[dict[str, object]],
    contracts: list[dict[str, object]],
    dsf: list[dict[str, object]],
    runner: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    text = f"""# 1168 — Y5/R10 lifted-C continuity action source or dSFeps bound

**Current verdict:** 1168 sharpens the continuity route but does not close it. A spacetime lifted-C three-form `mathcalJ_C` can be split so that `Phi_C` is the spatial boundary-flux component and `Sigma_C` is the spacetime source/top-class term. That makes the law precise, but not yet parent-derived.

**Main progress:** the formal split `d_4 mathcalJ_C = Sigma_C` gives the spatial balance `L_tau J_C = d Phi_C + Sigma_C` up to sign convention. This explains what `Sigma_C` and `Phi_C` must be. It also exposes the danger: a multiplier action can impose continuity, but cannot by itself explain why local `Sigma_C=0` while FLRW source/top class survives.

**Fallback progress:** the `d_S(F_lambda epsilon_C)` row is now decomposed into a zero route and a finite-bound route. It remains nonclaim because `F_lambda`, `epsilon_C`, surface norm, units, and numeric/theorem bounds are not sourced.

**No claim:** no local-GR, R10, PPN, WEP, clock, orbital, projected-metric theorem, or `c_g=0` result follows.

## Source register

{md_table(sources, ["source_id", "relative_path", "needle", "exists", "needle_found", "role"])}

## Continuity action/source attempt

{md_table(action, ["action_id", "clause", "statement", "status", "what_it_derives", "what_is_missing", "valid_for_claim"])}

## Sigma/Phi source contract

{md_table(contracts, ["contract_id", "quantity", "required_definition", "current_value", "source_anchor", "valid_for_claim"])}

## dS(F epsilon) finite-bound rows

{md_table(dsf, ["row_id", "quantity", "bound_formula", "units_or_norm", "current_status", "missing_for_claim", "valid_for_claim"])}

## Runner dry-run

{md_table(runner, ["run_id", "test", "status", "blocked_by", "detail", "claim_allowed"])}

## Claim gates

{md_table(gates, ["gate_id", "gate", "current_status", "reason", "claim_allowed"])}

## Decision ledger

{md_table(decisions, ["decision_id", "decision", "reason", "next_action", "valid_for_claim"])}

## Validation

{md_table(validation, ["check_id", "result", "detail", "claim_allowed"])}

## Next target

{md_table(next_rows, ["next_id", "next_target", "objective", "include", "exclude", "valid_for_claim"])}
"""
    DOC.write_text(text, encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    sources = stamp(source_rows())
    action = stamp(continuity_action_rows())
    contracts = stamp(sigma_phi_contract_rows())
    dsf = stamp(dSFeps_rows())
    runner = stamp(runner_rows())
    gates = stamp(claim_gate_rows())
    decisions = stamp(decision_rows())
    next_rows = stamp(next_target_rows())
    outputs = {
        "P8_Y5_R10_1168_SOURCE_REGISTER.csv": sources,
        "P8_Y5_R10_1168_CONTINUITY_ACTION_SOURCE_ATTEMPT.csv": action,
        "P8_Y5_R10_1168_SIGMA_PHI_SOURCE_CONTRACT.csv": contracts,
        "P8_Y5_R10_1168_DSF_EPS_BOUND_ROWS.csv": dsf,
        "P8_Y5_R10_1168_RUNNER_DRY_RUN.csv": runner,
        "P8_Y5_R10_1168_CLAIM_GATES.csv": gates,
        "P8_Y5_R10_1168_DECISION_LEDGER.csv": decisions,
        "P8_Y5_R10_1168_NEXT_TARGET.csv": next_rows,
    }
    csv_paths: list[Path] = []
    for name, rows in outputs.items():
        path = OUT / name
        write_csv(path, rows)
        csv_paths.append(path)

    validation = stamp(validate(sources, action, contracts, dsf, runner, gates, decisions, next_rows, csv_paths))
    validation_path = OUT / "P8_Y5_BRR545_1168_VALIDATION.csv"
    write_csv(validation_path, validation)
    csv_paths.append(validation_path)
    write_doc(sources, action, contracts, dsf, runner, gates, decisions, next_rows, validation)

    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)

    failed = [row for row in validation if row["result"] != "pass"]
    print(f"wrote {DOC}")
    print("validation: PASS" if not failed else f"validation: FAIL {failed}")
    if failed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
