from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


PACK_ID = "P8_Y5_R10_1207"
TITLE = "1207-Y5-R10-quotient-coframe-lock-or-epsilon-geom-source-pack"
ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "source-intake" / "mts_residuals"
DOC_PATH = ROOT / f"{TITLE}.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
RUN_STARTED_UTC = datetime.now(timezone.utc)


SOURCE_REGISTER_PATH = OUT_DIR / f"{PACK_ID}_SOURCE_REGISTER.csv"
ZERO_AUDIT_PATH = OUT_DIR / f"{PACK_ID}_EPSILON_GEOM_ZERO_AUDIT.csv"
COMPONENT_PACK_PATH = OUT_DIR / f"{PACK_ID}_EPSILON_GEOM_COMPONENT_SOURCE_PACK.csv"
PRESSURE_PATH = OUT_DIR / f"{PACK_ID}_PRESSURE_AND_ABSORPTION_GATE.csv"
DECISION_PATH = OUT_DIR / f"{PACK_ID}_DECISION_LEDGER.csv"
CLAIM_GATES_PATH = OUT_DIR / f"{PACK_ID}_CLAIM_GATES.csv"
NEXT_PATH = OUT_DIR / f"{PACK_ID}_NEXT_TARGET.csv"
VALIDATION_PATH = OUT_DIR / "P8_Y5_BRR545_1207_VALIDATION.csv"


def rel(path: Path) -> str:
    return path.resolve().relative_to(ROOT).as_posix()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def exists_and_contains(relative_path: str, needle: str) -> tuple[bool, bool]:
    path = ROOT / relative_path
    if not path.exists():
        return False, False
    if not needle:
        return True, True
    return True, needle in read_text(path)


def load_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def fmt(value: object) -> str:
    if isinstance(value, float):
        return f"{value:.12g}"
    return str(value)


def md_escape(value: object) -> str:
    return fmt(value).replace("|", "\\|").replace("\n", " ")


def markdown_table(rows: list[dict[str, object]], fields: list[str]) -> str:
    lines = [
        "| " + " | ".join(fields) + " |",
        "| " + " | ".join(["---"] * len(fields)) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(md_escape(row.get(field, "")) for field in fields) + " |")
    return "\n".join(lines)


def validation_row(check_id: str, check: str, passed: bool, details: str) -> dict[str, object]:
    return {
        "check_id": check_id,
        "check": check,
        "status": "PASS" if passed else "FAIL",
        "details": details,
        "valid_for_claim": False,
        "claim_allowed": False,
    }


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    source_specs = [
        {
            "source_id": "SRC1207_0_1206_next",
            "local_path": "1206-Y5-R10-KT-boundary-trace-law-or-Ploc-leakage-smallness-derivation.md",
            "needle": "NEXT1206_0_1207",
            "purpose": "handoff to quotient/coframe lock or epsilon_geom source pack",
        },
        {
            "source_id": "SRC1207_1_1206_projector_lowering",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1206_LOWERED_COMPONENT_DERIVATIONS.csv",
            "needle": "DRV1206_1_projector_leakage_lowering",
            "purpose": "epsilon_geom lowered formula from 1206",
        },
        {
            "source_id": "SRC1207_2_1206_pressure",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1206_PRESSURE_COMPARISON.csv",
            "needle": "CMP1206_1_projector_lowered_target",
            "purpose": "projector pressure target epsilon_geom*G_res_norm",
        },
        {
            "source_id": "SRC1207_3_943_coframe_contract",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_943_COFRAME_COUPLING_CONTRACT.csv",
            "needle": "CFC943_7_contract_verdict",
            "purpose": "coframe coupling parent contract and verdict",
        },
        {
            "source_id": "SRC1207_4_863_chain_rule",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_863_COFRAME_ZERO_THEOREM.csv",
            "needle": "CZT863_5_zero_verdict",
            "purpose": "conditional coframe chain-rule zero theorem",
        },
        {
            "source_id": "SRC1207_5_637_qmap",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_637_QUOTIENT_MAP_DERIVATION.csv",
            "needle": "QM637_2_vertical_kernel",
            "purpose": "quotient map vertical-kernel condition",
        },
        {
            "source_id": "SRC1207_6_581_quotient_chain",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_581_QUOTIENT_VERTICAL_THEOREM_CHAIN.csv",
            "needle": "QVT581_2_matter_factorization",
            "purpose": "quotient/matter factorization chain",
        },
        {
            "source_id": "SRC1207_7_1003_frame_audit",
            "local_path": "1003-Y5-R10-Bref-covariant-frame-theorem-or-Delta-ref-frame-profile-row.md",
            "needle": "CFA1003_6_theorem_verdict",
            "purpose": "covariant frame/coframe theorem remains unsigned",
        },
        {
            "source_id": "SRC1207_8_1029_shadow_frame",
            "local_path": "1029-Y5-R10-cg-no-shadow-frame-theorem-or-first-numeric-coupling-row.md",
            "needle": "NST1029_1_chain_rule_zero",
            "purpose": "no-shadow-frame chain-rule zero conditional theorem",
        },
        {
            "source_id": "SRC1207_9_1019_projector",
            "local_path": "1019-Y5-R10-boundary-exactness-projector-orthogonality-or-source-pack.md",
            "needle": "PO1019_5_verdict",
            "purpose": "projector orthogonality remains unsigned",
        },
    ]
    source_rows: list[dict[str, object]] = []
    for spec in source_specs:
        path_exists, needle_found = exists_and_contains(spec["local_path"], spec["needle"])
        source_rows.append(
            {
                **spec,
                "path_exists": path_exists,
                "needle_found": needle_found,
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )

    pressure = load_csv(OUT_DIR / "P8_Y5_R10_1206_PRESSURE_COMPARISON.csv")
    projector_target = float(next(row for row in pressure if row["comparison_id"] == "CMP1206_1_projector_lowered_target")["target"])

    zero_audit = [
        {
            "audit_id": "ZEA1207_0_chain_rule_coframe",
            "epsilon_component": "coframe_lock_Linf",
            "zero_route": "If e_obs(Phi)=Obs_e(q(Phi)) and Dq[v]=0, then Lie_v e_obs=0 by chain rule.",
            "what_it_really_kills": "vertical/readout coframe variation and shadow-frame drift",
            "what_it_does_not_kill": "spatial derivative nabla P_loc or domain-boundary motion",
            "current_status": "CONDITIONAL_ZERO_NOT_PARENT_SIGNED",
            "source_anchor": "P8_Y5_R10_863_COFRAME_ZERO_THEOREM.csv::CZT863_5_zero_verdict",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "ZEA1207_1_shadow_frame",
            "epsilon_component": "projector_stress_Linf/frame_channel",
            "zero_route": "If ordinary matter has no independent conformal/disformal/source-frame argument, frame response factors through q and vertical derivative is zero.",
            "what_it_really_kills": "hidden matter-frame coupling components such as c_g when no-shadow-frame parent clause is signed",
            "what_it_does_not_kill": "projector stress from changing the projector/domain itself",
            "current_status": "CONDITIONAL_ZERO_NOT_PARENT_SIGNED",
            "source_anchor": "1029-Y5-R10-cg-no-shadow-frame-theorem-or-first-numeric-coupling-row.md::NST1029_1_chain_rule_zero",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "ZEA1207_2_parallel_projector",
            "epsilon_component": "nabla_P_loc_Linf",
            "zero_route": "Require covariant parallelism or fixed block projector in the selected local domain: nabla P_loc=0.",
            "what_it_really_kills": "the derivative projector term in D_T^dagger",
            "what_it_does_not_kill": "coframe/domain/projector-stress variation unless those are separately signed",
            "current_status": "NOT_DERIVED_BY_QUOTIENT_CHAIN_RULE",
            "source_anchor": "1195-Y5-R10-parent-DT-operator-range-source-or-Einstein-domain-classifier.md::DTA1195_1_formal_adjoint",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "ZEA1207_3_domain_motion",
            "epsilon_component": "domain_motion_Linf",
            "zero_route": "Require the local test domain, boundary, tau-normal, and support map to be fixed by the same parent quotient/readout lock.",
            "what_it_really_kills": "moving-domain/coframe support terms in the projector leakage budget",
            "what_it_does_not_kill": "spatial nabla P_loc if the projector varies within the fixed domain",
            "current_status": "MISSING_PARENT_DOMAIN_LOCK",
            "source_anchor": "1003-Y5-R10-Bref-covariant-frame-theorem-or-Delta-ref-frame-profile-row.md::CFA1003_6_theorem_verdict",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "ZEA1207_4_total_epsilon_zero",
            "epsilon_component": "epsilon_geom",
            "zero_route": "epsilon_geom=0 only if coframe_lock_Linf=nabla_P_loc_Linf=domain_motion_Linf=projector_stress_Linf=0 in one parent-owned domain.",
            "what_it_really_kills": "q_projector as a positive local residual component",
            "what_it_does_not_kill": "q_boundary, q_coker, q_regularizer, official W_R10, or G_res_norm",
            "current_status": "TOTAL_ZERO_BLOCKED",
            "source_anchor": "1206-Y5-R10-KT-boundary-trace-law-or-Ploc-leakage-smallness-derivation.md::DRV1206_1_projector_leakage_lowering",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    component_pack = [
        {
            "component_id": "EGP1207_0_nabla_P_loc",
            "epsilon_component": "nabla_P_loc_Linf",
            "definition": "sup_D ||nabla P_loc|| in the observed coframe/connection used by D_T",
            "zero_certificate_needed": "P_loc is covariantly parallel or a fixed parent block projector on the selected local branch",
            "finite_row_columns": "domain_id;norm_id;P_loc_definition_path;connection_path;nabla_P_loc_Linf;units;source_path;valid_for_claim",
            "current_value": "MISSING",
            "current_status": "MOST_DANGEROUS_REMAINING_COMPONENT",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "component_id": "EGP1207_1_coframe_lock",
            "epsilon_component": "coframe_lock_Linf",
            "definition": "vertical/readout variation norm of e_obs and induced connection under the selected quotient direction",
            "zero_certificate_needed": "e_obs factors through q and Dq[v]=0 with matter/readout functor signed by parent action",
            "finite_row_columns": "domain_id;norm_id;q_map_path;vertical_generator_path;coframe_descent_path;coframe_lock_Linf;source_path;valid_for_claim",
            "current_value": "CONDITIONAL_ZERO_IF_PARENT_SIGNED",
            "current_status": "CHAIN_RULE_READY_PARENT_SIGNATURE_MISSING",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "component_id": "EGP1207_2_domain_motion",
            "epsilon_component": "domain_motion_Linf",
            "definition": "motion of local integration domain, boundary support, tau-normal, and source support under quotient/coframe flow",
            "zero_certificate_needed": "domain/support/tau-normal are quotient-owned fixed readout data in the same branch",
            "finite_row_columns": "domain_id;boundary_map_path;tau_normal_path;support_lock_path;domain_motion_Linf;units;source_path;valid_for_claim",
            "current_value": "MISSING",
            "current_status": "DOMAIN_LOCK_MISSING",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "component_id": "EGP1207_3_projector_stress",
            "epsilon_component": "projector_stress_Linf",
            "definition": "stress/Ward residual generated by variation of P_loc/projector/readout map",
            "zero_certificate_needed": "projector variation either has no stress or its stress is carried in the parent Ward identity and projected out",
            "finite_row_columns": "domain_id;projector_variation_path;Ward_identity_path;projector_stress_Linf;units;source_path;valid_for_claim",
            "current_value": "MISSING",
            "current_status": "PROJECTOR_STRESS_NOT_SILENT",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "component_id": "EGP1207_4_C_P",
            "epsilon_component": "C_P",
            "definition": "operator constant converting summed lower-level leakage norms into epsilon_geom",
            "zero_certificate_needed": "not a zero component; must be finite and same-norm",
            "finite_row_columns": "domain_id;norm_id;operator_family;C_P;units;source_path;valid_for_claim",
            "current_value": "MISSING",
            "current_status": "MISSING_OPERATOR_CONSTANT",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "component_id": "EGP1207_5_C_CK_Gres",
            "epsilon_component": "C_CK_and_G_res_norm",
            "definition": "absorption and scoring constants required after epsilon_geom is formed",
            "zero_certificate_needed": "not zero components; C_CK finite and G_res_norm sourced or theorem-zero",
            "finite_row_columns": "domain_id;norm_id;C_CK;G_res_norm;C_CK_epsilon_geom;epsilon_geom_G_res_norm;source_path;valid_for_claim",
            "current_value": "MISSING",
            "current_status": "MISSING_ABSORPTION_AND_SCORE_INPUTS",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    pressure_rows = [
        {
            "pressure_id": "PGA1207_0_total_formula",
            "formula": "epsilon_geom=C_P*(nabla_P_loc_Linf+coframe_lock_Linf+domain_motion_Linf+projector_stress_Linf)",
            "target": projector_target,
            "gate": "epsilon_geom*G_res_norm <= target",
            "absorption_gate": "C_CK*epsilon_geom < 1",
            "current_status": "FORMULA_READY_VALUES_MISSING",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "pressure_id": "PGA1207_1_if_chain_rule_only",
            "formula": "epsilon_geom=C_P*(nabla_P_loc_Linf+domain_motion_Linf+projector_stress_Linf) if coframe_lock_Linf=0 only",
            "target": projector_target,
            "gate": "still blocked because chain-rule coframe zero does not kill nabla_P_loc/domain/stress",
            "absorption_gate": "C_CK*C_P*(remaining components)<1",
            "current_status": "PARTIAL_ZERO_NOT_ENOUGH",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "pressure_id": "PGA1207_2_total_zero_condition",
            "formula": "epsilon_geom=0",
            "target": projector_target,
            "gate": "requires every component source row theorem-zero in one domain",
            "absorption_gate": "automatic if epsilon_geom=0",
            "current_status": "BLOCKED_BY_NABLA_PLOC_DOMAIN_PROJECTOR_STRESS",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    decisions = [
        {
            "decision_id": "DEC1207_0_verdict",
            "condition": "quotient/coframe chain-rule zero closes only part of epsilon_geom",
            "decision": "do not claim q_projector=0; stage lower-level epsilon_geom source pack and attack nabla_P_loc/local projector parallelism next",
            "result": "coframe/shadow-frame vertical leakage is conditionally zero, but total epsilon_geom remains blocked by nabla_P_loc, domain_motion, and projector_stress",
            "next_action": "derive or bound nabla_P_loc_Linf as the highest-value missing component",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]

    claim_gates = [
        {
            "gate_id": "GATE1207_0_total_epsilon_zero",
            "gate": "epsilon_geom=0",
            "status": "BLOCKED",
            "reason": "chain-rule coframe/no-shadow-frame zero does not prove nabla_P_loc=0, domain_motion=0, or projector_stress=0",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1207_1_source_pack_numeric",
            "gate": "epsilon_geom numeric score",
            "status": "BLOCKED",
            "reason": "all lower-level source rows remain missing or conditional",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1207_2_partial_zero_guard",
            "gate": "partial zero cannot be promoted to total zero",
            "status": "ACTIVE_GUARD",
            "reason": "1207 explicitly separates coframe vertical zero from spatial projector derivative and domain/stress terms",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1207_3_R10_local_GR",
            "gate": "R10/local-GR branch",
            "status": "BLOCKED",
            "reason": "q_projector, q_boundary, official W_R10, and G_res_norm remain nonclaim/missing",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    next_rows = [
        {
            "next_id": "NEXT1207_0_1208",
            "target_file": "1208-Y5-R10-Ploc-parallel-projector-or-nablaPloc-bound.md",
            "target_script": "scripts/Y5_R10_Ploc_parallel_projector_or_nablaPloc_bound.py",
            "task": "try to derive P_loc as a covariantly parallel/fixed branch projector in the local GR domain; if not, stage the first source-ready nabla_P_loc_Linf bound row",
            "success_condition": "nabla_P_loc_Linf is theorem-zero, reduced to lower geometry constants, or explicitly source-ready with domain/norm requirements",
            "do_not_do": "do not infer spatial nabla_P_loc=0 from vertical quotient descent alone, do not claim R10/local-GR pass, do not edit formalization-workbench, do not push GitHub",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]

    source_fields = ["source_id", "local_path", "needle", "purpose", "path_exists", "needle_found", "valid_for_claim", "claim_allowed"]
    zero_fields = ["audit_id", "epsilon_component", "zero_route", "what_it_really_kills", "what_it_does_not_kill", "current_status", "source_anchor", "valid_for_claim", "claim_allowed"]
    pack_fields = ["component_id", "epsilon_component", "definition", "zero_certificate_needed", "finite_row_columns", "current_value", "current_status", "valid_for_claim", "claim_allowed"]
    pressure_fields = ["pressure_id", "formula", "target", "gate", "absorption_gate", "current_status", "valid_for_claim", "claim_allowed"]
    decision_fields = ["decision_id", "condition", "decision", "result", "next_action", "valid_for_claim", "claim_allowed"]
    gate_fields = ["gate_id", "gate", "status", "reason", "valid_for_claim", "claim_allowed"]
    next_fields = ["next_id", "target_file", "target_script", "task", "success_condition", "do_not_do", "valid_for_claim", "claim_allowed"]

    write_csv(SOURCE_REGISTER_PATH, source_rows, source_fields)
    write_csv(ZERO_AUDIT_PATH, zero_audit, zero_fields)
    write_csv(COMPONENT_PACK_PATH, component_pack, pack_fields)
    write_csv(PRESSURE_PATH, pressure_rows, pressure_fields)
    write_csv(DECISION_PATH, decisions, decision_fields)
    write_csv(CLAIM_GATES_PATH, claim_gates, gate_fields)
    write_csv(NEXT_PATH, next_rows, next_fields)

    formalization_recent = []
    if FORMALIZATION.exists():
        for path in FORMALIZATION.rglob("*"):
            if path.is_file():
                mtime = datetime.fromtimestamp(path.stat().st_mtime, timezone.utc)
                if mtime >= RUN_STARTED_UTC:
                    formalization_recent.append(path)

    csvs_to_parse = [
        SOURCE_REGISTER_PATH,
        ZERO_AUDIT_PATH,
        COMPONENT_PACK_PATH,
        PRESSURE_PATH,
        DECISION_PATH,
        CLAIM_GATES_PATH,
        NEXT_PATH,
    ]
    csv_parse_ok = True
    parse_details: list[str] = []
    for csv_path in csvs_to_parse:
        try:
            rows = load_csv(csv_path)
            parse_details.append(f"{csv_path.name}:{len(rows)}")
        except Exception as exc:  # noqa: BLE001
            csv_parse_ok = False
            parse_details.append(f"{csv_path.name}:ERROR:{exc}")

    all_sources_exist = all(bool(row["path_exists"]) for row in source_rows)
    all_needles_found = all(bool(row["needle_found"]) for row in source_rows)
    chain_rule_present = any(row["audit_id"] == "ZEA1207_0_chain_rule_coframe" for row in zero_audit)
    nabla_not_claimed = any(row["epsilon_component"] == "nabla_P_loc_Linf" and row["current_status"] == "NOT_DERIVED_BY_QUOTIENT_CHAIN_RULE" for row in zero_audit)
    total_zero_blocked = any(row["epsilon_component"] == "epsilon_geom" and row["current_status"] == "TOTAL_ZERO_BLOCKED" for row in zero_audit)
    source_pack_complete = {"nabla_P_loc_Linf", "coframe_lock_Linf", "domain_motion_Linf", "projector_stress_Linf", "C_P", "C_CK_and_G_res_norm"}.issubset({row["epsilon_component"] for row in component_pack})
    pressure_preserved = abs(projector_target - 1.17233215026e-05) < 1e-16
    no_total_zero_claim = all(row["current_status"] != "CLAIMED_ZERO" for row in zero_audit) and all(row["status"] != "PASSED" for row in claim_gates)
    next_nabla_route = "nabla_P_loc" in next_rows[0]["task"]
    claim_policy_ok = all(
        not bool(row.get("valid_for_claim")) and not bool(row.get("claim_allowed"))
        for row in zero_audit + component_pack + pressure_rows + decisions + claim_gates
    )
    formalization_untouched = len(formalization_recent) == 0

    validation_rows = [
        validation_row("VAL1207_0_sources_exist", "all cited local sources exist", all_sources_exist, f"{sum(bool(row['path_exists']) for row in source_rows)}/{len(source_rows)} sources exist"),
        validation_row("VAL1207_1_needles_found", "all cited source needles found", all_needles_found, f"{sum(bool(row['needle_found']) for row in source_rows)}/{len(source_rows)} needles found"),
        validation_row("VAL1207_2_chain_rule_present", "chain-rule coframe zero route is represented", chain_rule_present, "ZEA1207_0 present"),
        validation_row("VAL1207_3_nabla_not_claimed", "nabla_P_loc is not falsely zeroed by quotient descent", nabla_not_claimed, "nabla_P_loc remains not-derived-by-chain-rule"),
        validation_row("VAL1207_4_total_zero_blocked", "total epsilon zero remains blocked", total_zero_blocked, "epsilon_geom total zero blocked"),
        validation_row("VAL1207_5_source_pack_complete", "epsilon_geom component source pack is complete", source_pack_complete, ",".join(row["epsilon_component"] for row in component_pack)),
        validation_row("VAL1207_6_pressure_preserved", "1206 projector pressure target is preserved", pressure_preserved, f"target={fmt(projector_target)}"),
        validation_row("VAL1207_7_no_total_zero_claim", "no total zero claim is made", no_total_zero_claim, "all zero rows nonclaim"),
        validation_row("VAL1207_8_next_nabla_route", "next route targets nabla_P_loc", next_nabla_route, next_rows[0]["target_file"]),
        validation_row("VAL1207_9_nonclaim_policy", "all generated rows remain nonclaim", claim_policy_ok, "valid_for_claim=false and claim_allowed=false throughout"),
        validation_row("VAL1207_10_csv_parse", "all generated CSVs parse cleanly", csv_parse_ok, "; ".join(parse_details)),
        validation_row("VAL1207_11_formalization_untouched", "formalization-workbench untouched during run", formalization_untouched, f"formalization_recent_after_run_start_count={len(formalization_recent)}"),
    ]
    validation_pass = all(row["status"] == "PASS" for row in validation_rows)
    validation_rows.append(
        validation_row(
            "VAL1207_12_overall",
            "overall 1207 validation",
            validation_pass,
            "1207 quotient/coframe epsilon_geom audit is reproducible and nonclaim" if validation_pass else "one or more validation checks failed",
        )
    )
    validation_fields = ["check_id", "check", "status", "details", "valid_for_claim", "claim_allowed"]
    write_csv(VALIDATION_PATH, validation_rows, validation_fields)

    doc = f"""# 1207 Y5/R10 Quotient Coframe Lock Or Epsilon Geom Source Pack

**Current verdict:** 1207 does **not** prove `epsilon_geom=0`. It proves the important narrower point: quotient/coframe chain-rule descent can kill vertical coframe/shadow-frame leakage if parent-signed, but it does not by itself kill the spatial `nabla_P_loc` term, domain motion, or projector stress.

**Main progress:** primitive `eps_P` stays eliminated. The live object is now the source-pack formula `epsilon_geom=C_P(nabla_P_loc_Linf+coframe_lock_Linf+domain_motion_Linf+projector_stress_Linf)`, with the harsh target `epsilon_geom*G_res_norm <= {fmt(projector_target)}` and absorption condition `C_CK*epsilon_geom < 1`.

## Source Register

{markdown_table(source_rows, source_fields)}

## Epsilon Geom Zero Audit

{markdown_table(zero_audit, zero_fields)}

## Epsilon Geom Component Source Pack

{markdown_table(component_pack, pack_fields)}

## Pressure And Absorption Gate

{markdown_table(pressure_rows, pressure_fields)}

## Decision Ledger

{markdown_table(decisions, decision_fields)}

## Claim Gates

{markdown_table(claim_gates, gate_fields)}

## Next Target

{markdown_table(next_rows, next_fields)}

## Validation

{markdown_table(validation_rows, validation_fields)}
"""
    DOC_PATH.write_text(doc, encoding="utf-8")

    print(f"wrote {DOC_PATH}")
    print(f"wrote {VALIDATION_PATH}")
    print(f"validation_pass={validation_pass}")
    print(f"projector_target={fmt(projector_target)}")
    print("total_epsilon_zero_claimed=false")


if __name__ == "__main__":
    main()
