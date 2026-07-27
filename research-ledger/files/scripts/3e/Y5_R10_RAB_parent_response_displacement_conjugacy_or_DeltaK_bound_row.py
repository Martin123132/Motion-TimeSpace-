from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


PACK_ID = "P8_Y5_R10_1285"
TITLE = "1285-Y5-R10-RAB-parent-response-displacement-conjugacy-or-DeltaK-bound-row"
ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "source-intake" / "mts_residuals"
DOC_PATH = ROOT / f"{TITLE}.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
RUN_STARTED_UTC = datetime.now(timezone.utc)


SOURCE_REGISTER_PATH = OUT_DIR / f"{PACK_ID}_SOURCE_REGISTER.csv"
CONJUGACY_AUDIT_PATH = OUT_DIR / f"{PACK_ID}_PARENT_RESPONSE_CONJUGACY_AUDIT.csv"
THEOREM_CONTRACT_PATH = OUT_DIR / f"{PACK_ID}_CONJUGACY_THEOREM_CONTRACT.csv"
DELTAK_BOUND_ROW_PATH = OUT_DIR / f"{PACK_ID}_DELTAK_DIVERGENCE_BOUND_ROW_NONCLAIM.csv"
INTAKE_RULES_PATH = OUT_DIR / f"{PACK_ID}_DELTAK_BOUND_INTAKE_RULES.csv"
CLAIM_GATES_PATH = OUT_DIR / f"{PACK_ID}_CLAIM_GATES.csv"
DECISION_PATH = OUT_DIR / f"{PACK_ID}_DECISION_LEDGER.csv"
NEXT_PATH = OUT_DIR / f"{PACK_ID}_NEXT_TARGET.csv"
VALIDATION_PATH = OUT_DIR / "P8_Y5_BRR545_1285_VALIDATION.csv"


def source_path(relative_path: str) -> Path:
    path = Path(relative_path)
    if path.is_absolute():
        return path
    return ROOT / path


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        fieldnames = []
        for row in rows:
            for key in row:
                if key not in fieldnames:
                    fieldnames.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def md_escape(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def markdown_table(rows: list[dict[str, object]], fields: list[str]) -> str:
    if not rows:
        return "_No rows._\n"
    return "\n".join(
        [
            "| " + " | ".join(fields) + " |",
            "| " + " | ".join(["---"] * len(fields)) + " |",
            *["| " + " | ".join(md_escape(row.get(field, "")) for field in fields) + " |" for row in rows],
        ]
    )


def exists_and_contains(relative_path: str, needle: str) -> tuple[bool, bool]:
    path = source_path(relative_path)
    if not path.exists():
        return False, False
    if not needle:
        return True, True
    return True, needle in read_text(path)


def validation_row(check_id: str, check: str, passed: bool, details: str) -> dict[str, object]:
    return {"check_id": check_id, "check": check, "status": "PASS" if passed else "FAIL", "details": details}


def is_false(value: object) -> bool:
    return str(value).strip().lower() in {"false", "0", "no"}


def contains_missing_marker(row: dict[str, object]) -> bool:
    return any("MISSING_" in str(value) for value in row.values())


def generated_inside_formalization() -> list[Path]:
    generated_paths = [
        SOURCE_REGISTER_PATH,
        CONJUGACY_AUDIT_PATH,
        THEOREM_CONTRACT_PATH,
        DELTAK_BOUND_ROW_PATH,
        INTAKE_RULES_PATH,
        CLAIM_GATES_PATH,
        DECISION_PATH,
        NEXT_PATH,
        VALIDATION_PATH,
        DOC_PATH,
    ]
    return [path for path in generated_paths if FORMALIZATION in path.parents]


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    source_register = [
        {
            "source_id": "SRC1285_0_1284_next",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1284_NEXT_TARGET.csv",
            "needle": "NEXT1284_0_1285",
            "role": "handoff into parent response/displacement conjugacy or DeltaK bound row",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1285_1_1284_owner",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1284_GAMMA_KHAT_OWNER_EXTRACTION_AUDIT.csv",
            "needle": "GKO1284_5_verdict",
            "role": "owner extraction remains not closed",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1285_2_1284_DeltaK",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1284_DELTAK_DECOMPOSITION_LEDGER.csv",
            "needle": "DK1284_4_verdict",
            "role": "DeltaK retained symbolic residual",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1285_3_noether_audit",
            "local_path": "source-intake/mts_residuals/P8_YLOC_SOURCE_CURRENT_NOETHER_AUDIT.csv",
            "needle": "N1_parent_response_identity",
            "role": "Noether audit identifies response/displacement conjugacy as conditional clue",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1285_4_ward_contract",
            "local_path": "source-intake/mts_residuals/P8_Ward_source_owner_identity_CONTRACT.csv",
            "needle": "C1_exact_owner_decomposition",
            "role": "Ward/source owner decomposition requirements",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1285_5_parent_action_terms",
            "local_path": "source-intake/mts_residuals/P8_source_owner_parent_action_terms_CONTRACT.csv",
            "needle": "A1_source_owner_decomposition",
            "role": "parent action structures needed for source owner currents",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1285_6_response_contract",
            "local_path": "source-intake/mts_residuals/P8_RESPONSE_DOUBLET_ACTION_CONTRACT.csv",
            "needle": "RD516_2_metric_response",
            "role": "response-doublet metric-response requirement",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1285_7_response_variation",
            "local_path": "source-intake/mts_residuals/P8_RESPONSE_DOUBLET_ACTION_VARIATION.csv",
            "needle": "AV517_4_Euler_equation",
            "role": "source/boundary obstruction in response-doublet Euler equation",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1285_8_515_doc",
            "local_path": "515-match-Gamma-eff-Khat-to-metric-response-action.md",
            "needle": "MA515_2_conjugate_response_field",
            "role": "prior conjugate response field audit",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1285_9_1284_doc",
            "local_path": "1284-Y5-R10-RAB-Gamma-eff-Khat-owner-extraction-or-DeltaK-residual-ledger.md",
            "needle": "K_hat = K_metric[Gamma_eff] + Delta_K",
            "role": "Ward plus DeltaK split from 1284",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]
    for row in source_register:
        exists, needle_found = exists_and_contains(str(row["local_path"]), str(row["needle"]))
        row["exists"] = exists
        row["needle_found"] = needle_found

    conjugacy_audit = [
        {
            "audit_id": "PRC1285_0_parent_response_field",
            "needed_object": "parent response/displacement field R_parent",
            "required_map": "R_parent -> scalar projection Gamma_eff and tensor response K_hat",
            "current_evidence": "N1 says this can work only if Khat and Gamma_eff are conjugates of a parent response field",
            "status": "CONDITIONAL_TEMPLATE_NO_FIELD",
            "failure_mode": "without R_parent, Gamma_eff and K_hat are independent knobs",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "PRC1285_1_scalar_projection",
            "needed_object": "Gamma_eff = Pi_scalar[R_parent]",
            "required_map": "covariant scalar density with units, background subtraction, local branch domain",
            "current_evidence": "1284 LGK1284_0 remains MISSING_SOURCE_BACKED_FORMULA",
            "status": "MISSING_SCALAR_PROJECTION",
            "failure_mode": "K_metric cannot be computed",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "PRC1285_2_tensor_response",
            "needed_object": "K_hat^{mu nu} = Pi_tensor[R_parent]",
            "required_map": "same parent field gives Hilbert metric response of sqrt(-g) Gamma_eff",
            "current_evidence": "RD516_2 not checked for current MTS; 1284 LGK1284_2 remains missing tensor",
            "status": "MISSING_TENSOR_RESPONSE_MATCH",
            "failure_mode": "Delta_K remains physical residual candidate",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "PRC1285_3_Ward_identity",
            "needed_object": "owned Ward/source decomposition",
            "required_map": "q_res^nu=nabla_mu K_owner^{mu nu}+q_retained^nu with q_retained=0 or bounded",
            "current_evidence": "C1 and A1 are not parent-derived; Noether ownership is not zero theorem",
            "status": "OWNER_DECOMPOSITION_NOT_PARENT_DERIVED",
            "failure_mode": "source-current leakage survives as retained q/DeltaK row",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "PRC1285_4_component_lock",
            "needed_object": "response field controls measured local residual vector",
            "required_map": "R_parent=0 implies q_loc, Y5, Y6, PPN, boundary, and coupling residuals vanish",
            "current_evidence": "RD516_5 not derived; 1282 component map not closed",
            "status": "PHYSICAL_COMPONENT_LOCK_NOT_PROVED",
            "failure_mode": "auxiliary response can vanish while measured residuals remain",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "PRC1285_5_no_linear_source",
            "needed_object": "J_R=0 and B_R=0",
            "required_map": "no matter/source/boundary linear work drives the response field in compact local vacuum",
            "current_evidence": "AV517_4 blocked by source-current rows; RD516_4 not derived",
            "status": "SOURCE_BOUNDARY_ZERO_NOT_DERIVED",
            "failure_mode": "quadratic response potential can still be sourced",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "PRC1285_6_verdict",
            "needed_object": "parent response/displacement conjugacy theorem",
            "required_map": "PRC1285_0..5 all source-signed",
            "current_evidence": "field, scalar projection, tensor response, Ward owner, component lock, and source zero are unsigned",
            "status": "CONJUGACY_NOT_CONSTRUCTED",
            "failure_mode": "Delta_K bound row is mandatory",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    theorem_contract = [
        {
            "contract_id": "PCT1285_0_action_block",
            "theorem_clause": "There exists S_resp[g,R_parent,other fields] inside the parent action.",
            "mathematical_requirement": "variation is taken before readout/scoring and includes metric, source, projector, boundary, and coupling sectors",
            "current_status": "MISSING_PARENT_ACTION_BLOCK",
            "if_closed": "response field is legal, not post-hoc",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "contract_id": "PCT1285_1_dual_projection",
            "theorem_clause": "Gamma_eff and K_hat are dual projections of the same R_parent.",
            "mathematical_requirement": "Gamma_eff=Pi_0(R_parent), K_hat=Pi_2(delta_g Gamma_eff), with identical units/domain",
            "current_status": "MISSING_DUAL_PROJECTION_MAP",
            "if_closed": "Delta_K=0 becomes plausible rather than assumed",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "contract_id": "PCT1285_2_Hilbert_variation",
            "theorem_clause": "K_hat equals the Hilbert metric response of sqrt(-g) Gamma_eff.",
            "mathematical_requirement": "K_hat^{mu nu}=2/sqrt(-g) delta[sqrt(-g)Gamma_eff]/delta g_mu_nu minus volume convention including derivative/boundary terms",
            "current_status": "MISSING_VARIATION_COMPUTATION",
            "if_closed": "Ward-owned q_loc piece can be derived on shell",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "contract_id": "PCT1285_3_zero_source",
            "theorem_clause": "R_parent has no local compact source or boundary work.",
            "mathematical_requirement": "J_R=0 and B_R=0, including Y5 source normalization and Y6 extra stress channels",
            "current_status": "MISSING_SOURCE_BOUNDARY_ZERO",
            "if_closed": "quadratic/even response field can actually relax to zero",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "contract_id": "PCT1285_4_component_lock",
            "theorem_clause": "The response norm is coercive on the physical residual vector.",
            "mathematical_requirement": "c_-||R_phys||^2 <= <R_parent,M R_parent> and no measured residual lies in the kernel",
            "current_status": "MISSING_COERCIVE_PHYSICAL_LOCK",
            "if_closed": "response silence implies q_loc/PPN/source/coupling silence",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "contract_id": "PCT1285_5_verdict",
            "theorem_clause": "Parent response/displacement conjugacy derives Delta_K=0 and q_loc Ward ownership.",
            "mathematical_requirement": "PCT1285_0..4 all close with source paths and equations",
            "current_status": "THEOREM_NOT_CLOSED",
            "if_closed": "local-GR branch can advance to Euler/double-zero/no-flux gates",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    deltak_bound_row = [
        {
            "bound_id": "DKB1285_0_DeltaK_divergence_bound_template",
            "residual_component": "q_DeltaK^nu",
            "definition": "-P_loc nabla_mu Delta_K^{mu nu}",
            "DeltaK_definition": "Delta_K^{mu nu}=K_hat^{mu nu}-K_metric^{mu nu}[Gamma_eff]",
            "needed_profile": "MISSING_DELTAK_COMPONENT_PROFILE",
            "needed_units": "MISSING_DELTAK_UNITS",
            "needed_domain": "MISSING_LOCAL_DOMAIN_AND_BOUNDARY_CONDITIONS",
            "needed_projector": "MISSING_P_LOC_LIVE_PROFILE",
            "needed_norm": "MISSING_Q_DELTAK_NORM",
            "needed_observable_map": "MISSING_PPN_CLOCK_ORBITAL_R10_RESPONSE_OPERATOR",
            "source_path": "MISSING_SOURCE_PATH",
            "source_anchor": "MISSING_SOURCE_ANCHOR",
            "current_status": "SOURCE_READY_TEMPLATE_NOT_SCOREABLE",
            "maps_to_tests": "PPN;clock;orbital;local_GR;R10_if_range_component",
            "valid_for_claim": False,
            "claim_allowed": False,
            "next_action": "replace every MISSING_* with sourced Delta_K profile/bound data or prove Delta_K=0/exact-silent",
        }
    ]

    intake_rules = [
        {
            "rule_id": "DKIR1285_0_no_template_claims",
            "rule": "Rows with any MISSING_* marker are rejected for claims.",
            "acceptance": "no MISSING_* fields and source path/anchor found",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "rule_id": "DKIR1285_1_zero_proof",
            "rule": "Delta_K can be removed only by Delta_K=0, exact/improvement silence, or P_loc div Delta_K=0 theorem.",
            "acceptance": "source-backed tensor comparison or exact-term certificate",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "rule_id": "DKIR1285_2_finite_bound",
            "rule": "If Delta_K survives, score q_DeltaK componentwise without cancellation against the Ward-owned piece.",
            "acceptance": "component profile, units, norm, arena response operator, and bound threshold",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "rule_id": "DKIR1285_3_no_free_auxiliary_fifth_force",
            "rule": "A new response field cannot be added as a free auxiliary field unless its coupling/source/no-hair gates are signed.",
            "acceptance": "parent action block plus no local matter/source/boundary linear work",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    claim_gates = [
        {
            "gate_id": "CG1285_0_conjugacy",
            "claim": "parent response/displacement conjugacy is constructed",
            "current_status": "BLOCKED_CONJUGACY_NOT_CONSTRUCTED",
            "reason": "missing parent response field, scalar projection, tensor response, Ward owner, component lock, and source zero",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "CG1285_1_DeltaK_zero",
            "claim": "Delta_K is zero or harmless",
            "current_status": "BLOCKED_BOUND_ROW_TEMPLATE_ONLY",
            "reason": "DeltaK row is source-ready but has MISSING fields and no zero proof",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "CG1285_2_q_loc_zero",
            "claim": "q_loc^nu=0",
            "current_status": "BLOCKED_WARD_AND_DELTAK_BRANCHES_OPEN",
            "reason": "Ward-owned response branch and DeltaK residual branch are both unresolved",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "CG1285_3_local_GR",
            "claim": "derived local GR/Newton/PPN branch",
            "current_status": "BLOCKED_NO_LOCAL_GR_CLAIM",
            "reason": "q_loc, Y5/Y6, PPN lock, coupling, and boundary gates remain active",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    decision = [
        {
            "decision_id": "DEC1285_0_conjugacy_result",
            "decision": "Parent response/displacement conjugacy is the cleanest route, but it is not constructed in current sources.",
            "because": "Noether gives a conditional clue, not the parent response field or its scalar/tensor projections.",
            "next_action": "keep it as the theory target but do not promote it",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1285_1_DeltaK_result",
            "decision": "Delta_K must be carried as its own residual branch.",
            "because": "an unmatched K_hat tensor would survive even if the Ward-owned Gamma_eff piece works",
            "next_action": "fill DeltaK profile/bound fields or prove DeltaK exact/zero",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1285_2_next_target",
            "decision": "Next attack should source the first concrete DeltaK or response-field component row.",
            "because": "the abstract contract is now clear; the bottleneck is an actual source-backed component/profile",
            "next_action": "build a DeltaK component profile schema and search existing Gamma memory/source expansion and Khat balance routes for a first fillable row",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    next_target = [
        {
            "next_id": "NEXT1285_0_1286",
            "target_file": "1286-Y5-R10-RAB-first-DeltaK-component-profile-or-response-field-row.md",
            "target_script": "scripts/Y5_R10_RAB_first_DeltaK_component_profile_or_response_field_row.py",
            "task": "try to fill the first concrete Delta_K component/profile row from existing Gamma memory/source expansion and Khat balance routes; if not possible, write the exact response-field component row that must be sourced next",
            "success_condition": "one Delta_K or response-field component row has source path, units, domain, and nonclaim status, or a blocker ledger states why no component can yet be filled",
            "do_not": "do not score the Delta_K template, do not cancel Delta_K against the Ward piece, and do not claim local GR",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]

    write_csv(SOURCE_REGISTER_PATH, source_register)
    write_csv(CONJUGACY_AUDIT_PATH, conjugacy_audit)
    write_csv(THEOREM_CONTRACT_PATH, theorem_contract)
    write_csv(DELTAK_BOUND_ROW_PATH, deltak_bound_row)
    write_csv(INTAKE_RULES_PATH, intake_rules)
    write_csv(CLAIM_GATES_PATH, claim_gates)
    write_csv(DECISION_PATH, decision)
    write_csv(NEXT_PATH, next_target)

    validations: list[dict[str, object]] = []
    validations.append(
        validation_row(
            "VAL1285_0_sources_exist",
            "all cited local sources exist",
            all(bool(row["exists"]) for row in source_register),
            f"{sum(bool(row['exists']) for row in source_register)}/{len(source_register)} sources exist",
        )
    )
    validations.append(
        validation_row(
            "VAL1285_1_needles_found",
            "all cited local needles found",
            all(bool(row["needle_found"]) for row in source_register),
            f"{sum(bool(row['needle_found']) for row in source_register)}/{len(source_register)} needles found",
        )
    )
    conj_verdict = next(row for row in conjugacy_audit if row["audit_id"] == "PRC1285_6_verdict")
    validations.append(
        validation_row(
            "VAL1285_2_conjugacy_not_constructed",
            "parent response/displacement conjugacy is not constructed",
            conj_verdict["status"] == "CONJUGACY_NOT_CONSTRUCTED" and is_false(conj_verdict["claim_allowed"]),
            "PRC1285_6_verdict=CONJUGACY_NOT_CONSTRUCTED",
        )
    )
    theorem_verdict = next(row for row in theorem_contract if row["contract_id"] == "PCT1285_5_verdict")
    validations.append(
        validation_row(
            "VAL1285_3_theorem_not_closed",
            "conjugacy theorem contract remains open",
            theorem_verdict["current_status"] == "THEOREM_NOT_CLOSED" and is_false(theorem_verdict["valid_for_claim"]),
            "PCT1285_5_verdict=THEOREM_NOT_CLOSED",
        )
    )
    bound_row = deltak_bound_row[0]
    validations.append(
        validation_row(
            "VAL1285_4_DeltaK_bound_template_nonclaim",
            "DeltaK divergence bound row is source-ready but not scoreable",
            bound_row["current_status"] == "SOURCE_READY_TEMPLATE_NOT_SCOREABLE"
            and contains_missing_marker(bound_row)
            and is_false(bound_row["valid_for_claim"])
            and is_false(bound_row["claim_allowed"]),
            "DKB1285_0 has MISSING markers and claim flags false",
        )
    )
    validations.append(
        validation_row(
            "VAL1285_5_intake_rules_block_claims",
            "DeltaK intake rules reject templates, require zero proof or finite bound, and forbid free auxiliary fifth force",
            len(intake_rules) == 4 and all(is_false(row["claim_allowed"]) for row in intake_rules),
            f"intake_rule_rows={len(intake_rules)}",
        )
    )
    validations.append(
        validation_row(
            "VAL1285_6_claim_gates_blocked",
            "all claim gates remain blocked",
            all("BLOCKED" in row["current_status"] and is_false(row["claim_allowed"]) for row in claim_gates),
            f"claim_gate_rows={len(claim_gates)}",
        )
    )
    generated_tables = [
        SOURCE_REGISTER_PATH,
        CONJUGACY_AUDIT_PATH,
        THEOREM_CONTRACT_PATH,
        DELTAK_BOUND_ROW_PATH,
        INTAKE_RULES_PATH,
        CLAIM_GATES_PATH,
        DECISION_PATH,
        NEXT_PATH,
    ]
    parse_ok = True
    parse_details: list[str] = []
    for table_path in generated_tables:
        try:
            parse_details.append(f"{table_path.name}:{len(read_csv(table_path))}")
        except Exception as exc:
            parse_ok = False
            parse_details.append(f"{table_path.name}:ERROR:{exc}")
    validations.append(validation_row("VAL1285_7_csv_parse", "all generated CSVs parse cleanly", parse_ok, "; ".join(parse_details)))
    validations.append(
        validation_row(
            "VAL1285_8_next_target_1286",
            "next target routes to first DeltaK component profile or response-field row",
            next_target[0]["next_id"] == "NEXT1285_0_1286" and "Delta_K component" in next_target[0]["task"],
            str(next_target[0]["target_file"]),
        )
    )
    formalization_hits = generated_inside_formalization()
    validations.append(
        validation_row(
            "VAL1285_9_formalization_untouched",
            "formalization-workbench untouched by generated outputs",
            not formalization_hits,
            f"formalization_generated_output_count={len(formalization_hits)}",
        )
    )
    validations.append(
        validation_row(
            "VAL1285_10_nonclaim_policy",
            "all generated rows remain nonclaim",
            all(
                is_false(row.get("valid_for_claim", False)) and is_false(row.get("claim_allowed", False))
                for rows in [
                    source_register,
                    conjugacy_audit,
                    theorem_contract,
                    deltak_bound_row,
                    intake_rules,
                    claim_gates,
                    decision,
                    next_target,
                ]
                for row in rows
            ),
            "valid_for_claim=false and claim_allowed=false throughout generated tables",
        )
    )
    overall_pass = all(row["status"] == "PASS" for row in validations)
    validations.append(
        validation_row(
            "VAL1285_11_overall",
            "overall 1285 validation",
            overall_pass,
            "1285 fails parent response/displacement conjugacy construction, writes a nonclaim DeltaK divergence bound row, and routes to first component/profile fill next",
        )
    )
    write_csv(VALIDATION_PATH, validations)

    doc = f"""# 1285 Y5 R10 RAB parent response/displacement conjugacy or DeltaK bound row

Generated: `{RUN_STARTED_UTC.isoformat()}`

**Current verdict:** 1285 does not construct the parent response/displacement conjugacy. The route remains the cleanest way to make `Gamma_eff` and `K_hat` one object, but current sources only provide a conditional clue, not the field, projections, Ward owner, physical component lock, and zero-source theorem.

**Main progress:** `Delta_K` is now operationally unavoidable. If `K_hat != K_metric[Gamma_eff]`, the residual

`q_DeltaK^nu := -P_loc nabla_mu Delta_K^{{mu nu}}`

must be bounded or zeroed separately. It cannot be hidden inside the Ward-owned `Gamma_eff` piece.

**Next derivation target:** fill the first concrete `Delta_K` component/profile row, or source the first actual parent response-field component. The abstract theorem contract is now clear; the next step needs a real component.

## Exact Conjugacy Contract

The future parent action must supply one response/displacement object `R_parent` such that:

1. `Gamma_eff = Pi_0[R_parent]` is a covariant scalar density with units and background subtraction.
2. `K_hat = Pi_2[R_parent] = K_metric[Gamma_eff]`, including derivative and boundary terms.
3. The parent Ward identity owns the response force channel before readout.
4. The response norm is coercive on the measured local residual vector, not only an auxiliary shadow.
5. Local compact source and boundary work vanish or are explicitly bounded.

Until those five clauses close, `Delta_K` is retained.

## Source Register

{markdown_table(source_register, ["source_id", "local_path", "needle", "exists", "needle_found", "role", "valid_for_claim", "claim_allowed"])}

## Parent Response Conjugacy Audit

{markdown_table(conjugacy_audit, ["audit_id", "needed_object", "required_map", "current_evidence", "status", "failure_mode", "valid_for_claim", "claim_allowed"])}

## Conjugacy Theorem Contract

{markdown_table(theorem_contract, ["contract_id", "theorem_clause", "mathematical_requirement", "current_status", "if_closed", "valid_for_claim", "claim_allowed"])}

## DeltaK Divergence Bound Row

{markdown_table(deltak_bound_row, ["bound_id", "residual_component", "definition", "DeltaK_definition", "needed_profile", "needed_units", "needed_domain", "needed_projector", "needed_norm", "needed_observable_map", "source_path", "source_anchor", "current_status", "maps_to_tests", "valid_for_claim", "claim_allowed", "next_action"])}

## DeltaK Intake Rules

{markdown_table(intake_rules, ["rule_id", "rule", "acceptance", "valid_for_claim", "claim_allowed"])}

## Claim Gates

{markdown_table(claim_gates, ["gate_id", "claim", "current_status", "reason", "valid_for_claim", "claim_allowed"])}

## Decision Ledger

{markdown_table(decision, ["decision_id", "decision", "because", "next_action", "valid_for_claim", "claim_allowed"])}

## Next Target

{markdown_table(next_target, ["next_id", "target_file", "target_script", "task", "success_condition", "do_not", "valid_for_claim", "claim_allowed"])}

## Validation

{markdown_table(validations, ["check_id", "check", "status", "details"])}
"""
    DOC_PATH.write_text(doc, encoding="utf-8")


if __name__ == "__main__":
    main()
