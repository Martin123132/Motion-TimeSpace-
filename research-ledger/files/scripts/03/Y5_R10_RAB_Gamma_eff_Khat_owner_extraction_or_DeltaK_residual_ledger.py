from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


PACK_ID = "P8_Y5_R10_1284"
TITLE = "1284-Y5-R10-RAB-Gamma-eff-Khat-owner-extraction-or-DeltaK-residual-ledger"
ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "source-intake" / "mts_residuals"
DOC_PATH = ROOT / f"{TITLE}.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
RUN_STARTED_UTC = datetime.now(timezone.utc)


SOURCE_REGISTER_PATH = OUT_DIR / f"{PACK_ID}_SOURCE_REGISTER.csv"
OWNER_EXTRACTION_PATH = OUT_DIR / f"{PACK_ID}_GAMMA_KHAT_OWNER_EXTRACTION_AUDIT.csv"
DELTAK_LEDGER_PATH = OUT_DIR / f"{PACK_ID}_DELTAK_DECOMPOSITION_LEDGER.csv"
REQUIREMENTS_PATH = OUT_DIR / f"{PACK_ID}_LIVE_GAMMA_KHAT_REQUIREMENTS.csv"
CLAIM_GATES_PATH = OUT_DIR / f"{PACK_ID}_CLAIM_GATES.csv"
DECISION_PATH = OUT_DIR / f"{PACK_ID}_DECISION_LEDGER.csv"
NEXT_PATH = OUT_DIR / f"{PACK_ID}_NEXT_TARGET.csv"
VALIDATION_PATH = OUT_DIR / "P8_Y5_BRR545_1284_VALIDATION.csv"


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


def generated_inside_formalization() -> list[Path]:
    generated_paths = [
        SOURCE_REGISTER_PATH,
        OWNER_EXTRACTION_PATH,
        DELTAK_LEDGER_PATH,
        REQUIREMENTS_PATH,
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
            "source_id": "SRC1284_0_1283_next",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1283_NEXT_TARGET.csv",
            "needle": "NEXT1283_0_1284",
            "role": "handoff into Gamma_eff/Khat owner extraction or DeltaK ledger",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1284_1_GK_candidates",
            "local_path": "source-intake/mts_residuals/P8_GK_STRESS_ACTION_CANDIDATES.csv",
            "needle": "GK514_A_metric_response_scalar_density",
            "role": "candidate S_GK action routes",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1284_2_Gamma_owner",
            "local_path": "source-intake/mts_residuals/P8_GAMMA_OWNER_CANDIDATE_ACTION.csv",
            "needle": "GO516_A_response_doublet_quadratic_density",
            "role": "candidate Gamma_eff owner rows",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1284_3_metric_evidence",
            "local_path": "source-intake/mts_residuals/P8_GK_METRIC_RESPONSE_SOURCE_EVIDENCE.csv",
            "needle": "E515_4_source_current_audit",
            "role": "evidence for response/displacement conjugacy clue",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1284_4_symbol_match",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1281_GAMMA_KHAT_SYMBOL_MATCH_AUDIT.csv",
            "needle": "GKM1281_3_difference_test",
            "role": "current Gamma/Khat symbol-match failure and Delta_K missing ledger",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1284_5_515_doc",
            "local_path": "515-match-Gamma-eff-Khat-to-metric-response-action.md",
            "needle": "MA515_2_conjugate_response_field",
            "role": "prior owner extraction audit and repair options",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1284_6_516_doc",
            "local_path": "516-Gamma-eff-scalar-density-owner-or-q_loc-bound-runner.md",
            "needle": "D516_0",
            "role": "response-doublet owner candidate and bound runner decision",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1284_7_1010_doc",
            "local_path": "1010-Y5-R10-Gamma-Khat-action-existence-Helmholtz-or-q_loc-residual-retention.md",
            "needle": "QRES1010_1_Gamma_metric_response_gap",
            "role": "Delta_K retained symbolic gap",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1284_8_response_metric_ledger",
            "local_path": "source-intake/mts_residuals/P8_RESPONSE_DOUBLET_METRIC_RESPONSE_LEDGER.csv",
            "needle": "MR517_3_boundary_terms",
            "role": "response-doublet metric variation leakage terms",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1284_9_gate_tests",
            "local_path": "source-intake/mts_residuals/P8_GK_STRESS_ACTION_GATE_TESTS.csv",
            "needle": "G514_2_current_MTS_match",
            "role": "current corpus match failure gate",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]
    for row in source_register:
        exists, needle_found = exists_and_contains(str(row["local_path"]), str(row["needle"]))
        row["exists"] = exists
        row["needle_found"] = needle_found

    owner_extraction = [
        {
            "owner_id": "GKO1284_0_metric_response_scalar_density",
            "candidate_source": "GK514_A_metric_response_scalar_density",
            "Gamma_eff_candidate": "Gamma_eff(g,Phi,nablaPhi,D,...)",
            "Khat_candidate": "K_metric^{mu nu}=2/sqrt(-g) delta[sqrt(-g)Gamma_eff]/delta g_{mu nu} minus volume convention",
            "extraction_status": "CONTRACT_ONLY_NO_CURRENT_FORMULA",
            "why_not_live": "Gamma_eff is generic; no concrete parent fields, units, derivative terms, or current MTS K_hat tensor match",
            "repair": "supply actual Gamma_eff formula and compute K_metric component comparison",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "owner_id": "GKO1284_1_response_doublet_quadratic",
            "candidate_source": "GO516_A_response_doublet_quadratic_density",
            "Gamma_eff_candidate": "Gamma0 + 1/2 M_AB(g,R_even,D,...) Z^A Z^B + O(Z^4)",
            "Khat_candidate": "metric response of the quadratic density by definition",
            "extraction_status": "BEST_FORMAL_CANDIDATE_NOT_CURRENT_MTS_DERIVED",
            "why_not_live": "Z is not locked to physical q_loc/PPN residuals; J_Z/B_Z/Y5/Y6/boundary remain open",
            "repair": "construct parent response field and prove component lock plus no-linear-source theorem",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "owner_id": "GKO1284_2_positive_auxiliary_energy",
            "candidate_source": "GK514_B_positive_auxiliary_fields;GO516_B_positive_auxiliary_energy_density",
            "Gamma_eff_candidate": "V(Phi)+1/2 G_AB(Phi)nablaPhi^A nablaPhi^B",
            "Khat_candidate": "kinetic/elastic metric response of auxiliary energy density",
            "extraction_status": "CONDITIONAL_NEW_FIELD_ROUTE",
            "why_not_live": "source-free/no-hair theorem, coupling universality, and fifth-force bounds are not signed",
            "repair": "derive positive source-free local operator with zero matter/source coupling or keep finite-range bound",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "owner_id": "GKO1284_3_topological_improvement",
            "candidate_source": "GK514_C_topological_exact_sector;GO516_C_topological_boundary_density",
            "Gamma_eff_candidate": "normalized boundary/topological density or exact form",
            "Khat_candidate": "boundary/improvement stress response",
            "extraction_status": "CONDITIONAL_BOUNDARY_ROUTE",
            "why_not_live": "charge units, boundary flux, and local source-measure subtraction are open",
            "repair": "prove exact/improvement stress has zero local boundary force and mass flux",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "owner_id": "GKO1284_4_residual_branch",
            "candidate_source": "GK514_D_residual_branch",
            "Gamma_eff_candidate": "none accepted",
            "Khat_candidate": "none accepted",
            "extraction_status": "FALLBACK_REQUIRED_IF_OWNERS_FAIL",
            "why_not_live": "residual branch is honest but does not derive local GR",
            "repair": "fill q_loc/Delta_K finite profile, units, and arena response operators",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "owner_id": "GKO1284_5_verdict",
            "candidate_source": "all extraction rows",
            "Gamma_eff_candidate": "no source-backed live formula",
            "Khat_candidate": "no source-backed live tensor/metric-response match",
            "extraction_status": "OWNER_EXTRACTION_NOT_CLOSED",
            "why_not_live": "all routes are candidate/conditional/fallback rather than current-MTS sourced formulas",
            "repair": "attempt response/displacement conjugacy construction or retain Delta_K explicitly",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    deltak_ledger = [
        {
            "delta_id": "DK1284_0_definition",
            "object": "Delta_K^{mu nu}",
            "equation": "Delta_K^{mu nu}:=K_hat^{mu nu}-K_metric^{mu nu}[Gamma_eff]",
            "current_status": "DEFINED_SYMBOLIC_GAP",
            "effect_on_q_loc": "q_loc^nu=P_loc(nabla_mu T_metric^{mu nu}-nabla_mu Delta_K^{mu nu}) up to Euler/boundary convention",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "delta_id": "DK1284_1_Ward_owned_piece",
            "object": "T_metric^{mu nu}=Gamma_eff g^{mu nu}-K_metric^{mu nu}",
            "equation": "nabla_mu T_metric^{mu nu}=nabla^nu Gamma_eff-nabla_mu K_metric^{mu nu}",
            "current_status": "WARD_ROUTE_AVAILABLE_IF_S_GK_EXISTS",
            "effect_on_q_loc": "this part can vanish on shell only after action, Euler, source-zero, and boundary gates close",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "delta_id": "DK1284_2_unowned_piece",
            "object": "-P_loc nabla_mu Delta_K^{mu nu}",
            "equation": "q_DeltaK^nu:=-P_loc nabla_mu Delta_K^{mu nu}",
            "current_status": "RETAINED_RESIDUAL_IF_DELTAK_NOT_ZERO",
            "effect_on_q_loc": "even a good Gamma_eff action cannot silence q_loc if K_hat has an unmatched tensor piece",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "delta_id": "DK1284_3_zero_options",
            "object": "Delta_K zero theorem",
            "equation": "Delta_K=0, or Delta_K=exact/improvement with P_loc div Delta_K=0, or source-backed bound",
            "current_status": "ZERO_OR_BOUND_NOT_PROVED",
            "effect_on_q_loc": "requires component comparison, exact-term certificate, or finite residual bound",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "delta_id": "DK1284_4_verdict",
            "object": "Delta_K branch status",
            "equation": "K_hat=K_metric+Delta_K",
            "current_status": "DELTAK_RETAINED_SYMBOLIC_RESIDUAL",
            "effect_on_q_loc": "future local branch must either kill Delta_K or score it separately from the Ward-owned piece",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    requirements = [
        {
            "requirement_id": "LGK1284_0_Gamma_formula",
            "required_input": "Gamma_eff formula",
            "must_include": "parent fields, covariance, units, background subtraction, local branch domain",
            "current_status": "MISSING_SOURCE_BACKED_FORMULA",
            "blocks": "K_metric computation and q_loc profile",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "requirement_id": "LGK1284_1_metric_variation",
            "required_input": "K_metric[Gamma_eff]",
            "must_include": "sign convention, volume term, derivative terms, boundary terms",
            "current_status": "MISSING_VARIATION_COMPUTATION",
            "blocks": "Delta_K comparison",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "requirement_id": "LGK1284_2_existing_Khat",
            "required_input": "existing MTS K_hat tensor",
            "must_include": "components/index convention, units, parent source path",
            "current_status": "MISSING_SOURCE_BACKED_TENSOR",
            "blocks": "metric-response match",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "requirement_id": "LGK1284_3_DeltaK",
            "required_input": "Delta_K ledger",
            "must_include": "zero proof, exact/improvement proof, or finite divergence bound",
            "current_status": "SYMBOLIC_RESIDUAL_ONLY",
            "blocks": "q_loc theorem-zero",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "requirement_id": "LGK1284_4_response_conjugacy",
            "required_input": "parent response/displacement field",
            "must_include": "scalar projection Gamma_eff, tensor metric response K_hat, Ward identity, component lock",
            "current_status": "PROMISING_TEMPLATE_NOT_CONSTRUCTED",
            "blocks": "cleanest derivation route",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    claim_gates = [
        {
            "gate_id": "CG1284_0_owner_extraction",
            "claim": "Gamma_eff/Khat owner extracted",
            "current_status": "BLOCKED_OWNER_EXTRACTION_NOT_CLOSED",
            "reason": "no source-backed live Gamma formula or Khat tensor/metric response",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "CG1284_1_DeltaK_zero",
            "claim": "Delta_K=0 or harmless",
            "current_status": "BLOCKED_DELTAK_RETAINED_SYMBOLIC_RESIDUAL",
            "reason": "difference ledger is defined but not computable/zeroed/bounded",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "CG1284_2_q_loc_zero",
            "claim": "q_loc^nu=0",
            "current_status": "BLOCKED_WARD_PLUS_DELTAK_GATES_OPEN",
            "reason": "Ward-owned piece and Delta_K piece are both not closed",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "CG1284_3_local_GR",
            "claim": "local GR/PPN branch reopened",
            "current_status": "BLOCKED_NO_LOCAL_CLAIM",
            "reason": "q_loc, Y5, Y6, PPN lock, boundary, and coupling remain retained gates",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    decision = [
        {
            "decision_id": "DEC1284_0_decomposition_progress",
            "decision": "Split q_loc into Ward-owned metric-response piece plus Delta_K residual.",
            "because": "this prevents a candidate action from hiding an unmatched K_hat tensor",
            "next_action": "carry Delta_K as an explicit residual unless the response/displacement construction proves K_hat=K_metric",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1284_1_best_route",
            "decision": "Prioritize parent response/displacement conjugacy over inventing a free Gamma field.",
            "because": "the source-current audit already says this is the strongest clue, while free auxiliary fields risk fifth-force coupling",
            "next_action": "attempt to build the parent response field with scalar/tensor projections",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1284_2_nonclaim",
            "decision": "Do not claim q_loc zero, local GR, or PPN silence from 1284.",
            "because": "owner extraction is not closed and Delta_K is retained",
            "next_action": "keep all generated rows nonclaim",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    next_target = [
        {
            "next_id": "NEXT1284_0_1285",
            "target_file": "1285-Y5-R10-RAB-parent-response-displacement-conjugacy-or-DeltaK-bound-row.md",
            "target_script": "scripts/Y5_R10_RAB_parent_response_displacement_conjugacy_or_DeltaK_bound_row.py",
            "task": "try to construct the parent response/displacement field whose scalar projection is Gamma_eff and whose metric response is K_hat; if this fails, create a source-ready nonclaim Delta_K divergence bound row",
            "success_condition": "response field supplies Gamma_eff, K_metric, K_hat match, Ward identity, and component lock, or Delta_K is carried as a separate finite residual requirement",
            "do_not": "do not introduce a free auxiliary Gamma field as a hidden fifth force and do not merge Delta_K into the Ward-owned piece",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]

    write_csv(SOURCE_REGISTER_PATH, source_register)
    write_csv(OWNER_EXTRACTION_PATH, owner_extraction)
    write_csv(DELTAK_LEDGER_PATH, deltak_ledger)
    write_csv(REQUIREMENTS_PATH, requirements)
    write_csv(CLAIM_GATES_PATH, claim_gates)
    write_csv(DECISION_PATH, decision)
    write_csv(NEXT_PATH, next_target)

    validations: list[dict[str, object]] = []
    validations.append(
        validation_row(
            "VAL1284_0_sources_exist",
            "all cited local sources exist",
            all(bool(row["exists"]) for row in source_register),
            f"{sum(bool(row['exists']) for row in source_register)}/{len(source_register)} sources exist",
        )
    )
    validations.append(
        validation_row(
            "VAL1284_1_needles_found",
            "all cited local needles found",
            all(bool(row["needle_found"]) for row in source_register),
            f"{sum(bool(row['needle_found']) for row in source_register)}/{len(source_register)} needles found",
        )
    )
    owner_verdict = next(row for row in owner_extraction if row["owner_id"] == "GKO1284_5_verdict")
    validations.append(
        validation_row(
            "VAL1284_2_owner_not_closed",
            "Gamma_eff/Khat owner extraction remains not closed",
            owner_verdict["extraction_status"] == "OWNER_EXTRACTION_NOT_CLOSED" and is_false(owner_verdict["claim_allowed"]),
            "GKO1284_5_verdict=OWNER_EXTRACTION_NOT_CLOSED",
        )
    )
    deltak_verdict = next(row for row in deltak_ledger if row["delta_id"] == "DK1284_4_verdict")
    validations.append(
        validation_row(
            "VAL1284_3_DeltaK_retained",
            "Delta_K is retained as symbolic residual",
            deltak_verdict["current_status"] == "DELTAK_RETAINED_SYMBOLIC_RESIDUAL" and is_false(deltak_verdict["valid_for_claim"]),
            "DK1284_4_verdict=DELTAK_RETAINED_SYMBOLIC_RESIDUAL",
        )
    )
    validations.append(
        validation_row(
            "VAL1284_4_requirements_block_claim",
            "live Gamma/Khat requirements remain missing or symbolic",
            all(("MISSING" in row["current_status"] or "SYMBOLIC" in row["current_status"] or "TEMPLATE" in row["current_status"]) for row in requirements),
            f"requirements_rows={len(requirements)}",
        )
    )
    validations.append(
        validation_row(
            "VAL1284_5_claim_gates_blocked",
            "all claim gates remain blocked",
            all("BLOCKED" in row["current_status"] and is_false(row["claim_allowed"]) for row in claim_gates),
            f"claim_gate_rows={len(claim_gates)}",
        )
    )
    generated_tables = [
        SOURCE_REGISTER_PATH,
        OWNER_EXTRACTION_PATH,
        DELTAK_LEDGER_PATH,
        REQUIREMENTS_PATH,
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
    validations.append(validation_row("VAL1284_6_csv_parse", "all generated CSVs parse cleanly", parse_ok, "; ".join(parse_details)))
    validations.append(
        validation_row(
            "VAL1284_7_next_target_1285",
            "next target routes to response/displacement conjugacy or DeltaK bound row",
            next_target[0]["next_id"] == "NEXT1284_0_1285" and "response/displacement" in next_target[0]["task"],
            str(next_target[0]["target_file"]),
        )
    )
    formalization_hits = generated_inside_formalization()
    validations.append(
        validation_row(
            "VAL1284_8_formalization_untouched",
            "formalization-workbench untouched by generated outputs",
            not formalization_hits,
            f"formalization_generated_output_count={len(formalization_hits)}",
        )
    )
    validations.append(
        validation_row(
            "VAL1284_9_nonclaim_policy",
            "all generated rows remain nonclaim",
            all(
                is_false(row.get("valid_for_claim", False)) and is_false(row.get("claim_allowed", False))
                for rows in [source_register, owner_extraction, deltak_ledger, requirements, claim_gates, decision, next_target]
                for row in rows
            ),
            "valid_for_claim=false and claim_allowed=false throughout generated tables",
        )
    )
    overall_pass = all(row["status"] == "PASS" for row in validations)
    validations.append(
        validation_row(
            "VAL1284_10_overall",
            "overall 1284 validation",
            overall_pass,
            "1284 fails live Gamma/Khat owner extraction, derives the Ward-plus-DeltaK split, retains Delta_K, and routes to parent response/displacement conjugacy next",
        )
    )
    write_csv(VALIDATION_PATH, validations)

    doc = f"""# 1284 Y5 R10 RAB Gamma_eff Khat owner extraction or DeltaK residual ledger

Generated: `{RUN_STARTED_UTC.isoformat()}`

**Current verdict:** 1284 does not find a source-backed live `Gamma_eff` / `K_hat` owner for current MTS. The best formal candidate remains the response-doublet/response-displacement route, but it is not yet a current-MTS derivation.

**Main progress:** the `q_loc` obstruction is now split cleanly. Write `K_hat = K_metric[Gamma_eff] + Delta_K`. Then

`q_loc^nu = P_loc(nabla_mu T_metric^{{mu nu}} - nabla_mu Delta_K^{{mu nu}})`,

where `T_metric^{{mu nu}} = Gamma_eff g^{{mu nu}} - K_metric^{{mu nu}}`. A good `S_GK` can only own the first Ward/Euler piece. Any unmatched `Delta_K` must be zeroed, exact/improvement-silent, or bounded separately.

**Next derivation target:** construct the parent response/displacement conjugacy: one parent object whose scalar projection is `Gamma_eff` and whose tensor metric response is `K_hat`. If that fails, `Delta_K` becomes a separate finite residual row.

## Source Register

{markdown_table(source_register, ["source_id", "local_path", "needle", "exists", "needle_found", "role", "valid_for_claim", "claim_allowed"])}

## Gamma/Khat Owner Extraction Audit

{markdown_table(owner_extraction, ["owner_id", "candidate_source", "Gamma_eff_candidate", "Khat_candidate", "extraction_status", "why_not_live", "repair", "valid_for_claim", "claim_allowed"])}

## DeltaK Decomposition Ledger

{markdown_table(deltak_ledger, ["delta_id", "object", "equation", "current_status", "effect_on_q_loc", "valid_for_claim", "claim_allowed"])}

## Live Gamma/Khat Requirements

{markdown_table(requirements, ["requirement_id", "required_input", "must_include", "current_status", "blocks", "valid_for_claim", "claim_allowed"])}

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
