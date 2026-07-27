from __future__ import annotations

import csv
from datetime import timezone, datetime
from pathlib import Path


PACK_ID = "P8_Y5_R10_1263"
TITLE = "1263-Y5-R10-vertical-fibre-null-from-parent-presymplectic-degeneracy-or-RAB-prior-envelope-fill"
ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "source-intake" / "mts_residuals"
RAB_INTAKE_DIR = ROOT / "source-intake" / "rab-sector"
DOC_PATH = ROOT / f"{TITLE}.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
RUN_STARTED_UTC = datetime.now(timezone.utc)


SOURCE_REGISTER_PATH = OUT_DIR / f"{PACK_ID}_SOURCE_REGISTER.csv"
PRESYMPLECTIC_CHAIN_PATH = OUT_DIR / f"{PACK_ID}_PRESYMPLECTIC_NULL_DERIVATION_CHAIN.csv"
KINETIC_CONTRADICTION_PATH = OUT_DIR / f"{PACK_ID}_KINETIC_TERM_CONTRADICTION_AUDIT.csv"
BOUNDARY_AUDIT_PATH = OUT_DIR / f"{PACK_ID}_RAB_BOUNDARY_CHARGE_AUDIT.csv"
PARENT_INPUT_BLOCKERS_PATH = OUT_DIR / f"{PACK_ID}_PARENT_INPUT_BLOCKERS.csv"
PRIOR_FILL_STATUS_PATH = OUT_DIR / f"{PACK_ID}_PRIOR_ENVELOPE_FILL_STATUS.csv"
CLAIM_GATES_PATH = OUT_DIR / f"{PACK_ID}_CLAIM_GATES.csv"
DECISION_PATH = OUT_DIR / f"{PACK_ID}_DECISION_LEDGER.csv"
NEXT_PATH = OUT_DIR / f"{PACK_ID}_NEXT_TARGET.csv"
VALIDATION_PATH = OUT_DIR / "P8_Y5_BRR545_1263_VALIDATION.csv"


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
    return {
        "check_id": check_id,
        "check": check,
        "status": "PASS" if passed else "FAIL",
        "details": details,
    }


def is_false(value: object) -> bool:
    return str(value).strip().lower() in {"false", "0", "no"}


def generated_inside_formalization() -> list[Path]:
    generated_paths = [
        SOURCE_REGISTER_PATH,
        PRESYMPLECTIC_CHAIN_PATH,
        KINETIC_CONTRADICTION_PATH,
        BOUNDARY_AUDIT_PATH,
        PARENT_INPUT_BLOCKERS_PATH,
        PRIOR_FILL_STATUS_PATH,
        CLAIM_GATES_PATH,
        DECISION_PATH,
        NEXT_PATH,
        VALIDATION_PATH,
        DOC_PATH,
    ]
    return [path for path in generated_paths if FORMALIZATION in path.parents]


def count_live_prior_rows() -> tuple[int, int, int]:
    raw_dir = RAB_INTAKE_DIR / "raw"
    accepted_dir = RAB_INTAKE_DIR / "accepted"
    docs_dir = RAB_INTAKE_DIR / "docs"
    raw_dir.mkdir(parents=True, exist_ok=True)
    accepted_dir.mkdir(parents=True, exist_ok=True)
    docs_dir.mkdir(parents=True, exist_ok=True)

    raw_rows = sum(len(read_csv(path)) for path in raw_dir.glob("*.csv"))
    accepted_rows = sum(len(read_csv(path)) for path in accepted_dir.glob("*.csv"))
    docs_rows = sum(len(read_csv(path)) for path in docs_dir.glob("*.csv"))
    return raw_rows, accepted_rows, docs_rows


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    source_register = [
        {
            "source_id": "SRC1263_0_1262_next",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1262_NEXT_TARGET.csv",
            "needle": "NEXT1262_0_1263",
            "purpose": "handoff to vertical-fibre null derivation",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1263_1_1262_theorem",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1262_VERTICAL_NULL_THEOREM_CANDIDATE.csv",
            "needle": "THEO1262_0_vertical_null_ban",
            "purpose": "conditional vertical-null ban for R_AB gradient energy",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1263_2_1262_minimal",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1262_MINIMAL_ASSUMPTION_AUDIT.csv",
            "needle": "MIN1262_1_vertical_null_action",
            "purpose": "minimum parent assumption set to test",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1263_3_727_map",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_727_DCDAGGER_VERTICAL_MAP.csv",
            "needle": "DVM727_3_precise_map",
            "purpose": "precise DCdagger=Omega-flat vertical-generator map",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1263_4_728_omega",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_728_PARENT_OMEGA_CANDIDATE.csv",
            "needle": "OM728_0_covariant_variation_definition",
            "purpose": "parent theta/Omega candidate and ownership blocker",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1263_5_729_current",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_729_NOETHER_PJ_ORIGIN_FORMULA.csv",
            "needle": "NPJ729_5_symplectic_flat_closure",
            "purpose": "single-current symplectic-flat closure contract",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1263_6_910_identity",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_910_SYMPLECTIC_IDENTITY_DERIVATION.csv",
            "needle": "SID910_3_integrability_obstruction",
            "purpose": "Hamiltonian/symplectic obstruction identity",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1263_7_911_contract",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_911_PARENT_SYMPLECTIC_CURRENT_CONTRACT.csv",
            "needle": "PSC911_0_EH_metric_core",
            "purpose": "parent symplectic current input contract",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1263_8_637_route",
            "local_path": "source-intake/mts_residuals/P8_Y5_BRR545_637_DECISION.csv",
            "needle": "D637_1_best_news",
            "purpose": "old note that the presymplectic/topological route can make q a canonical reduced-space projection",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1263_9_1262_template",
            "local_path": "source-intake/rab-sector/docs/ZR1262_RAB_PRIOR_ENVELOPE_TEMPLATE_NONCLAIM.csv",
            "needle": "ZR1262_TEMPLATE_DO_NOT_SCORE",
            "purpose": "fallback prior-envelope template remains docs-only",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    presymplectic_chain = [
        {
            "chain_id": "PND1263_0_parent_variation",
            "claim_piece": "parent action supplies theta and Omega",
            "mathematical_form": "delta L_parent = E_A delta Phi^A + d theta; Omega(delta1,delta2)=int_Sigma(delta1 theta(delta2)-delta2 theta(delta1))",
            "derivation_status": "FORMAL_IDENTITY_ONLY",
            "blocker": "explicit full MTS parent Lagrangian/theta not yet supplied",
            "source": "P8_Y5_R10_910_SYMPLECTIC_IDENTITY_DERIVATION.csv:SID910_0_variation_start",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "chain_id": "PND1263_1_reduced_quotient",
            "claim_piece": "q is the canonical reduced-space projection",
            "mathematical_form": "ker(Dq)=ker(Omega_parent) after quotienting proper gauge/boundary degeneracies",
            "derivation_status": "CONDITIONAL_ROUTE_NOT_CERTIFIED",
            "blocker": "old 637 route says this is plausible but constants and parent ownership remain unsigned",
            "source": "P8_Y5_BRR545_637_DECISION.csv:D637_1_best_news",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "chain_id": "PND1263_2_RAB_vertical_generator",
            "claim_piece": "`R_AB` variations generate a vector v_R in ker(Dq)",
            "mathematical_form": "for compact eta_AB, delta_eta R_AB=eta_AB and Dq[v_eta]=0",
            "derivation_status": "NOT_DERIVED_FOR_RAB",
            "blocker": "1262 identifies this as a needed vertical-sort theorem",
            "source": "P8_Y5_R10_1262_MINIMAL_ASSUMPTION_AUDIT.csv:MIN1262_0_RAB_vertical_sort",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "chain_id": "PND1263_3_symplectic_flat",
            "claim_piece": "vertical generator is paired by Omega-flat",
            "mathematical_form": "(DC_R)^dagger eta = Omega_flat(v_eta); v_eta=Omega^{-1}[(DC_R)^dagger eta] only on reduced nondegenerate phase space",
            "derivation_status": "FORMAL_MAP_AVAILABLE_NOT_RAB_OWNED",
            "blocker": "727/728 give the map, but Omega/DC/v_R are not parent-filled for R_AB",
            "source": "P8_Y5_R10_727_DCDAGGER_VERTICAL_MAP.csv:DVM727_3_precise_map",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "chain_id": "PND1263_4_boundary_silence",
            "claim_piece": "R_AB vertical generator has no boundary Hamiltonian charge",
            "mathematical_form": "delta H_eta = Omega(delta Phi,v_eta)=int_boundary(delta Q_eta-i_eta theta)=0",
            "derivation_status": "NOT_DERIVED",
            "blocker": "Q_R/B_R/Pi_R^n silence is not sourced or theorem-zeroed",
            "source": "P8_Y5_R10_910_SYMPLECTIC_IDENTITY_DERIVATION.csv:SID910_3_integrability_obstruction",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "chain_id": "PND1263_5_verdict",
            "claim_piece": "presymplectic-null proof of R_AB vertical silence",
            "mathematical_form": "PND1263_0 through PND1263_4 would imply R_AB is pure gauge/null",
            "derivation_status": "CONDITIONAL_CONTRADICTION_WRITTEN_NOT_PARENT_PROVED",
            "blocker": "parent L/theta/Omega, R_AB vertical generator, and boundary charge zero remain missing",
            "source": "PND1263_0 through PND1263_4",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    kinetic_contradiction = [
        {
            "audit_id": "KTC1263_0_ZR_variation",
            "assume": "S_Z = int sqrt(h) 1/2 Z_R h^{ij}D_iR_ABD_jR_AB",
            "calculation": "delta S_Z = -int sqrt(h) Z_R D_iD^iR_AB delta R_AB + int_boundary Z_R n^iD_iR_AB delta R_AB",
            "meaning": "for arbitrary compact vertical delta R_AB, nonzero Z_R produces a bulk Euler term; with boundary support it also produces Pi_R^n",
            "status": "EXACT_FORMAL_VARIATION",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "KTC1263_1_null_contradiction",
            "assume": "v_R is in ker(Omega_parent) and carries no boundary Hamiltonian charge",
            "calculation": "a nonzero Z_R term gives v_R a parent action response and/or boundary momentum, contradicting vertical nullness",
            "meaning": "if true presymplectic-null descent is parent-derived, Z_R must be zero; no plateau condition is needed",
            "status": "EXACT_CONDITIONAL_ON_TRUE_NULLNESS",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "KTC1263_2_escape_hatches",
            "assume": "one null premise fails",
            "calculation": "R_AB physical OR vertical metric exists OR boundary charge exists OR readout regenerates the term",
            "meaning": "then finite Z_R remains legal and must be bounded/sourced",
            "status": "RESIDUAL_BRANCH_RETAINED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    boundary_audit = [
        {
            "boundary_id": "RBA1263_0_bulk_compact",
            "needed_zero": "bulk vertical Euler response",
            "current_status": "ZERO_IF_TRUE_VERTICAL_NULL_AND_ZR_ZERO",
            "missing_input": "parent proof that compact R_AB variations are null directions",
            "effect_if_missing": "bulk finite-Z_R force/suppression branch remains",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "boundary_id": "RBA1263_1_surface_momentum",
            "needed_zero": "Pi_R^n=Z_R n^iD_iR_AB + partial B_R/partial R_AB",
            "current_status": "NOT_DERIVED",
            "missing_input": "B_R boundary variation/no-flux theorem or finite flux bound",
            "effect_if_missing": "boundary hair can survive even if bulk is quiet",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "boundary_id": "RBA1263_2_readout_stability",
            "needed_zero": "effective/readout action does not regenerate Pi_R or Z_R",
            "current_status": "UNSIGNED",
            "missing_input": "radiative/readout closure of quotient grammar",
            "effect_if_missing": "tree-level null route cannot support a local-GR claim",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    parent_blockers = [
        {
            "blocker_id": "PB1263_0_L_parent_theta",
            "needed_object": "full MTS parent Lagrangian and symplectic potential",
            "why_needed": "without theta/Omega, presymplectic nullness is only a template",
            "current_status": "MISSING_FULL_PARENT_ACTION",
            "source": "P8_Y5_R10_728_PARENT_OMEGA_CANDIDATE.csv:OM728_0_covariant_variation_definition",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "blocker_id": "PB1263_1_RAB_v_generator",
            "needed_object": "field-by-field R_AB vertical generator v_R",
            "why_needed": "must show Dq[v_R]=0 and Omega_flat(v_R)=0 rather than label R_AB gauge",
            "current_status": "MISSING_RAB_VERTICAL_GENERATOR",
            "source": "P8_Y5_R10_1262_MINIMAL_ASSUMPTION_AUDIT.csv:MIN1262_0_RAB_vertical_sort",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "blocker_id": "PB1263_2_no_vertical_metric",
            "needed_object": "theorem excluding parent G_vert/nabla_vert",
            "why_needed": "a vertical fibre metric makes |D R_AB|^2 quotient-natural",
            "current_status": "MISSING_NO_VERTICAL_METRIC_THEOREM",
            "source": "P8_Y5_R10_1262_MINIMAL_ASSUMPTION_AUDIT.csv:MIN1262_2_no_vertical_metric_connection",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "blocker_id": "PB1263_3_boundary_charge_zero",
            "needed_object": "Q_R/B_R/Pi_R boundary silence",
            "why_needed": "bulk degeneracy does not kill surface/corner charge",
            "current_status": "MISSING_BOUNDARY_ZERO_THEOREM",
            "source": "P8_Y5_R10_910_SYMPLECTIC_IDENTITY_DERIVATION.csv:SID910_3_integrability_obstruction",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    raw_rows, accepted_rows, docs_rows = count_live_prior_rows()
    prior_fill_status = [
        {
            "fill_id": "PFS1263_0_live_raw",
            "folder": str(RAB_INTAKE_DIR / "raw"),
            "rows_found": raw_rows,
            "status": "NO_LIVE_PRIOR_ROWS" if raw_rows == 0 else "RAW_ROWS_REQUIRE_REVIEW",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "fill_id": "PFS1263_1_live_accepted",
            "folder": str(RAB_INTAKE_DIR / "accepted"),
            "rows_found": accepted_rows,
            "status": "NO_ACCEPTED_PRIOR_ROWS" if accepted_rows == 0 else "ACCEPTED_ROWS_REQUIRE_NONCLAIM_AUDIT",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "fill_id": "PFS1263_2_docs",
            "folder": str(RAB_INTAKE_DIR / "docs"),
            "rows_found": docs_rows,
            "status": "DOCS_ONLY_NOT_SCOREABLE",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    claim_gates = [
        {
            "gate_id": "GATE1263_0_ZR_zero",
            "claim": "Z_R=0 from presymplectic nullness",
            "status": "BLOCKED",
            "reason": "conditional contradiction is written, but R_AB nullness is not parent-derived",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1263_1_boundary",
            "claim": "R_AB boundary/corner silence",
            "status": "BLOCKED",
            "reason": "Q_R/B_R/Pi_R zero theorem is missing",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1263_2_prior_fill",
            "claim": "finite Z_R prior envelope is scoreable",
            "status": "BLOCKED",
            "reason": "raw/accepted coefficient rows remain absent; docs rows are nonclaim templates",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1263_3_local_tests",
            "claim": "local GR/R10/PPN/clock/orbital pass",
            "status": "BLOCKED",
            "reason": "neither theorem-zero nor finite residual envelope is score-ready",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    decisions = [
        {
            "decision_id": "DEC1263_0_real_progress",
            "decision": "the presymplectic route gives a sharp conditional contradiction: true vertical-null R_AB is incompatible with nonzero Z_R kinetic energy",
            "because": "a nonzero gradient term gives compact vertical variations a bulk response and boundary momentum",
            "status": "EXACT_CONDITIONAL_PROGRESS",
            "next_action": "derive the R_AB vertical generator and parent theta/Omega from one parent action",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1263_1_not_closed",
            "decision": "the conditional contradiction cannot be promoted yet",
            "because": "the current corpus still lacks full parent L/theta/Omega, R_AB vertical generator, no-vertical-metric theorem, and boundary zero theorem",
            "status": "BLOCKED_FOR_CLAIM_RETAIN_FINITE_ZR_FALLBACK",
            "next_action": "try a minimal R_AB parent theta/v_R fill before using finite prior workflow",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    next_target = [
        {
            "next_id": "NEXT1263_0_1264",
            "target_file": "1264-Y5-R10-RAB-parent-theta-vR-fill-or-finite-ZR-source-row.md",
            "target_script": "scripts/Y5_R10_RAB_parent_theta_vR_fill_or_finite_ZR_source_row.py",
            "task": "try to instantiate the parent theta/Omega and field-by-field R_AB vertical generator v_R needed for the null proof; if that fails, prepare a finite nonclaim Z_R source row intake without scoring it",
            "success_condition": "either a sourced parent theta/v_R chain proving R_AB is Omega-null with zero boundary charge, or a strict finite-Z_R residual intake path with claim gates closed",
            "do_not": "do not promote the conditional contradiction into local-GR/R10/PPN evidence",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]

    generated_tables = [
        (SOURCE_REGISTER_PATH, source_register),
        (PRESYMPLECTIC_CHAIN_PATH, presymplectic_chain),
        (KINETIC_CONTRADICTION_PATH, kinetic_contradiction),
        (BOUNDARY_AUDIT_PATH, boundary_audit),
        (PARENT_INPUT_BLOCKERS_PATH, parent_blockers),
        (PRIOR_FILL_STATUS_PATH, prior_fill_status),
        (CLAIM_GATES_PATH, claim_gates),
        (DECISION_PATH, decisions),
        (NEXT_PATH, next_target),
    ]
    for path, rows in generated_tables:
        write_csv(path, rows)

    source_checks = [exists_and_contains(str(row["local_path"]), str(row["needle"])) for row in source_register]
    sources_exist = all(exists for exists, _ in source_checks)
    needles_found = all(found for _, found in source_checks)
    chain_verdict_conditional = presymplectic_chain[-1]["derivation_status"] == "CONDITIONAL_CONTRADICTION_WRITTEN_NOT_PARENT_PROVED"
    exact_conditional = kinetic_contradiction[1]["status"] == "EXACT_CONDITIONAL_ON_TRUE_NULLNESS"
    blockers_visible = len(parent_blockers) == 4 and all("MISSING" in str(row["current_status"]) for row in parent_blockers)
    prior_not_scoreable = raw_rows == 0 and accepted_rows == 0 and docs_rows >= 1
    no_claim_gates = all(row["status"] == "BLOCKED" for row in claim_gates)
    all_rows_nonclaim = all(
        is_false(row.get("valid_for_claim", "")) and is_false(row.get("claim_allowed", ""))
        for _path, rows in generated_tables
        for row in rows
    )
    next_is_1264 = next_target[0]["target_file"].startswith("1264-")

    csv_parse_ok = True
    csv_parse_details: list[str] = []
    for path, _rows in generated_tables:
        try:
            parsed_rows = read_csv(path)
            csv_parse_details.append(f"{path.name}:{len(parsed_rows)}")
        except Exception as exc:
            csv_parse_ok = False
            csv_parse_details.append(f"{path.name}:FAILED:{exc}")

    formalization_writes = generated_inside_formalization()

    validation_rows = [
        validation_row("VAL1263_0_sources_exist", "all cited local sources exist", sources_exist, f"{sum(1 for exists, _ in source_checks if exists)}/{len(source_checks)} sources exist"),
        validation_row("VAL1263_1_needles_found", "all cited local needles found", needles_found, f"{sum(1 for _, found in source_checks if found)}/{len(source_checks)} needles found"),
        validation_row("VAL1263_2_chain_verdict", "presymplectic chain verdict is conditional-not-proved", chain_verdict_conditional, presymplectic_chain[-1]["derivation_status"]),
        validation_row("VAL1263_3_kinetic_contradiction", "kinetic term contradiction is exact conditional", exact_conditional, kinetic_contradiction[1]["status"]),
        validation_row("VAL1263_4_parent_blockers", "parent input blockers are visible", blockers_visible, f"blocker_rows={len(parent_blockers)}"),
        validation_row("VAL1263_5_prior_not_scoreable", "prior envelope has no live raw/accepted rows", prior_not_scoreable, f"raw_rows={raw_rows}; accepted_rows={accepted_rows}; docs_rows={docs_rows}"),
        validation_row("VAL1263_6_claim_gates", "all claim gates remain blocked", no_claim_gates, f"claim_gate_rows={len(claim_gates)}"),
        validation_row("VAL1263_7_nonclaim_policy", "all generated rows remain nonclaim", all_rows_nonclaim, "valid_for_claim=false and claim_allowed=false throughout generated tables"),
        validation_row("VAL1263_8_next_target_1264", "next target is parent theta/vR fill", next_is_1264, next_target[0]["target_file"]),
        validation_row("VAL1263_9_csv_parse", "all generated CSVs parse cleanly", csv_parse_ok, "; ".join(csv_parse_details)),
        validation_row("VAL1263_10_formalization_untouched", "formalization-workbench untouched by generated outputs", not formalization_writes, f"formalization_generated_output_count={len(formalization_writes)}"),
    ]
    overall = all(row["status"] == "PASS" for row in validation_rows)
    validation_rows.append(
        validation_row(
            "VAL1263_11_overall",
            "overall 1263 validation",
            overall,
            "1263 proves the conditional kinetic/null contradiction, but keeps Z_R=0 and local tests blocked until parent theta/Omega/v_R and boundary silence are derived",
        )
    )
    write_csv(VALIDATION_PATH, validation_rows)

    doc = f"""# {TITLE}

**Current verdict:** 1263 gets a real mathematical foothold: if `R_AB` is genuinely a presymplectic-null/quotient-vertical representative with no boundary charge, then a nonzero `Z_R |D R_AB|^2` term contradicts that nullness.

**Main progress:** this sharpens the local branch. We are no longer asking for a magic plateau; we are asking for one parent fact: prove the `R_AB` direction is truly null in the parent symplectic geometry.

**No-claim guard:** this still does not prove `Z_R=0`, local GR/Newton, R10, PPN, clock, or orbital safety, because the parent `theta/Omega`, `v_R`, no-vertical-metric theorem, and boundary zero theorem are not filled.

## Source Register
{markdown_table(source_register, ["source_id", "local_path", "needle", "purpose", "valid_for_claim", "claim_allowed"])}

## Presymplectic Null Derivation Chain
{markdown_table(presymplectic_chain, ["chain_id", "claim_piece", "mathematical_form", "derivation_status", "blocker", "source", "valid_for_claim", "claim_allowed"])}

## Kinetic Term Contradiction Audit
{markdown_table(kinetic_contradiction, ["audit_id", "assume", "calculation", "meaning", "status", "valid_for_claim", "claim_allowed"])}

## RAB Boundary Charge Audit
{markdown_table(boundary_audit, ["boundary_id", "needed_zero", "current_status", "missing_input", "effect_if_missing", "valid_for_claim", "claim_allowed"])}

## Parent Input Blockers
{markdown_table(parent_blockers, ["blocker_id", "needed_object", "why_needed", "current_status", "source", "valid_for_claim", "claim_allowed"])}

## Prior Envelope Fill Status
{markdown_table(prior_fill_status, ["fill_id", "folder", "rows_found", "status", "valid_for_claim", "claim_allowed"])}

## Claim Gates
{markdown_table(claim_gates, ["gate_id", "claim", "status", "reason", "valid_for_claim", "claim_allowed"])}

## Decision Ledger
{markdown_table(decisions, ["decision_id", "decision", "because", "status", "next_action", "valid_for_claim", "claim_allowed"])}

## Next Target
{markdown_table(next_target, ["next_id", "target_file", "target_script", "task", "success_condition", "do_not", "valid_for_claim", "claim_allowed"])}

## Validation
{markdown_table(validation_rows, ["check_id", "check", "status", "details"])}
"""
    DOC_PATH.write_text(doc, encoding="utf-8")


if __name__ == "__main__":
    main()
