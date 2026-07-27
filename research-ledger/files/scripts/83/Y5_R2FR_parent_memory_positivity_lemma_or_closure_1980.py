from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


BRANCH = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
ROOT = Path(__file__).resolve().parents[1]
FORMALIZATION = ROOT.parent / "formalization-workbench"
MTS_RESIDUALS = ROOT / "source-intake" / "mts_residuals"
SOURCE_WEIGHT_DOCS = ROOT / "source-intake" / "source-weight" / "docs"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"

DOC_PATH = ROOT / "1980-Y5-R2FR-parent-memory-positivity-lemma-or-closure.md"
VALIDATION_PATH = MTS_RESIDUALS / "P8_Y5_BRR545_1980_VALIDATION.csv"

SOURCES = {
    "1979_doc": {
        "path": ROOT / "1979-Y5-R2FR-M2-Z-domain-theorem-or-first-finite-row.md",
        "needles": ["THM1979_5_gap", "SIG1979_0_kinetic", "NEXT1979_0_primary"],
    },
    "1979_validation": {
        "path": MTS_RESIDUALS / "P8_Y5_BRR545_1979_VALIDATION.csv",
        "needles": ["VAL1979_OVERALL", "PASS"],
    },
    "970_quadratic_memory": {
        "path": MTS_RESIDUALS / "P8_Y5_R10_970_QUADRATIC_MEMORY_ACTION_CONSTRUCTION.csv",
        "needles": ["QMA970_2_positivity", "CONDITIONAL_POSITIVITY_OK_INPUTS_UNSIGNED"],
    },
    "1304_operator_owner": {
        "path": MTS_RESIDUALS / "P8_Y5_R10_1304_MEMORY_OPERATOR_OWNER_ATTEMPT.csv",
        "needles": ["OO1304_1_static_local_operator_map", "MISSING_Z_m_SIGN"],
    },
    "1304_gap_map": {
        "path": MTS_RESIDUALS / "P8_Y5_R10_1304_ZM_POSITIVE_GAP_MAP_NONCLAIM.csv",
        "needles": ["ZPG1304_0_Zm_positive", "ZPG1304_2_mass_gap"],
    },
    "968_input_audit": {
        "path": MTS_RESIDUALS / "P8_Y5_R10_968_MEMORY_OPERATOR_INPUT_AUDIT.csv",
        "needles": ["MOI968_3_positivity", "MOI968_4_mass_gap", "MOI968_8_verdict"],
    },
    "1348_memory_operator": {
        "path": ROOT / "1348-Y5-R10-RAB-memory-branch-extremum-and-operator-signature-or-closure.md",
        "needles": ["OPS1348_2_Z_positive", "OPS1348_3_M2_gap", "GATE1348_1_operator_owned"],
    },
    "617_normalization": {
        "path": MTS_RESIDUALS / "P8_Y5_R10_617_FIELD_SPACE_NORMALIZATION_ATTEMPT.csv",
        "needles": ["FS617_3_rescaling_guard", "FS617_4_existing_corpus_check"],
    },
    "669_owner_gates": {
        "path": MTS_RESIDUALS / "P8_Y5_R10_669_LX_OWNER_GATE_TESTS.csv",
        "needles": ["G669_1_positive_kinetic", "G669_2_positive_mass_gap"],
    },
    "670_sourcefree_chain": {
        "path": MTS_RESIDUALS / "P8_Y5_R10_670_POSITIVE_SOURCEFREE_PROOF_CHAIN.csv",
        "needles": ["PSF670_2_positive_kinetic", "PSF670_3_positive_mass_gap"],
    },
    "1025_hessian": {
        "path": ROOT / "1025-Y5-R10-parent-Hessian-ZX-MX2-range-or-alpha-source-row.md",
        "needles": ["PHA1025_1_ZX_positive", "PHA1025_2_MX2_positive", "DEC1025_0_exact_contract"],
    },
}

OUTPUTS = {
    "source_register": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1980_SOURCE_REGISTER.csv",
    "lemma": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1980_MEMORY_POSITIVITY_LEMMA.csv",
    "proof_attempt": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1980_PROOF_ATTEMPT_AUDIT.csv",
    "negative_results": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1980_NEGATIVE_RESULTS.csv",
    "closure_contract": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1980_CLOSURE_CONTRACT.csv",
    "impact": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1980_LOCAL_GR_IMPACT.csv",
    "claim_gate": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1980_CLAIM_GATE.csv",
    "decision": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1980_DECISION_LEDGER.csv",
    "next": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1980_NEXT_TARGET.csv",
    "snapshot": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1980_PROJECT_STATUS_SNAPSHOT.csv",
    "source_weight": SOURCE_WEIGHT_DOCS / "PARENT_MEMORY_POSITIVITY_LEMMA_1980_NONCLAIM.csv",
    "queue": RAB_QUEUE / "JR1980_PARENT_MEMORY_ACTION_SIGN_QUEUE.csv",
}


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


CREATED_AT = now()


def ensure_dirs() -> None:
    for path in [MTS_RESIDUALS, SOURCE_WEIGHT_DOCS, RAB_QUEUE, DOC_PATH.parent]:
        path.mkdir(parents=True, exist_ok=True)


def row(values: dict[str, object]) -> dict[str, str]:
    base = {
        "branch": BRANCH,
        "id": "",
        "valid_for_claim": "false",
        "public_claim": "false",
        "created_at_utc": CREATED_AT,
    }
    merged = {**base, **values}
    return {key: str(value) for key, value in merged.items()}


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    if not rows:
        raise ValueError(f"refusing to write empty csv: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def source_register_rows() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for source_id, config in SOURCES.items():
        path = config["path"]
        text = path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""
        missing = [needle for needle in config["needles"] if needle not in text]
        rows.append(
            row(
                {
                    "id": f"SRC1980_{len(rows):02d}_{source_id}",
                    "source_id": source_id,
                    "source_path": str(path),
                    "required_needles": "; ".join(config["needles"]),
                    "exists": str(path.exists()).lower(),
                    "needle_status": "PASS" if not missing else "MISSING: " + "; ".join(missing),
                    "role": "parent memory positivity, Hessian sign, source-free chain, and 1979 coercivity continuity",
                }
            )
        )
    return rows


def build_tables() -> dict[str, list[dict[str, str]]]:
    lemma = [
        row(
            {
                "id": "LEM1980_0_parent_block",
                "lemma_piece": "minimal signed parent block",
                "statement": "If the parent action contains a memory sector whose static second variation is delta^2 E_m = integral_D sqrt(h)[Z_m h^{ij} partial_i delta m partial_j delta m + M_m^2(delta m)^2] plus controlled correction form E_H, then Z_m and M_m^2 are the only signs needed for the 1979 coercivity theorem.",
                "status": "CONDITIONAL_LEMMA_FORMULATED",
                "missing": "parent adoption of the memory block and correction split",
            }
        ),
        row(
            {
                "id": "LEM1980_1_Zm_sign",
                "lemma_piece": "positive kinetic memory metric",
                "statement": "Z_m>0 follows if the parent field-space metric restricted to the memory direction is positive and the memory coordinate normalization is fixed before local tests.",
                "status": "DERIVABLE_IF_PARENT_METRIC_SIGNED",
                "missing": "signed parent field-space metric along m; units; normalization ledger",
            }
        ),
        row(
            {
                "id": "LEM1980_2_M2_gap",
                "lemma_piece": "strict local memory mass gap",
                "statement": "M2_min>0 follows if the selected local branch is a strict non-degenerate minimum of V_R(m;X_B) after quotienting gauge/constant zero modes.",
                "status": "DERIVABLE_IF_STRICT_MINIMUM_SIGNED",
                "missing": "parent V_R functional or Hessian theorem; zero-mode projection; branch selector",
            }
        ),
        row(
            {
                "id": "LEM1980_3_Gm",
                "lemma_piece": "positive corrected spectral floor",
                "statement": "With Z_min>0, M2_min>0, lambda_1(D_loc)>0, and Eta_H < Z_min lambda_1 + M2_min, the 1979 floor G_m is positive.",
                "status": "CONDITIONAL_THEOREM_COMPLETE",
                "missing": "numeric/symbolic lower bounds and correction norm",
            }
        ),
        row(
            {
                "id": "LEM1980_4_closure_fork",
                "lemma_piece": "fork if parent signing fails",
                "statement": "If LEM1980_1 and LEM1980_2 cannot be signed from the parent action, the local memory transition is not derived; it must be carried as an explicit private closure or retained finite residual.",
                "status": "CLOSURE_FORK_REQUIRED_IF_UNSIGNED",
                "missing": "not a value gap; this is a parent-signature gap",
            }
        ),
    ]

    proof_attempt = [
        row(
            {
                "id": "PAT1980_0_action_candidate",
                "target": "use existing quadratic memory action candidate",
                "evidence": "QMA970_0 through QMA970_2 give the exact operator and positivity identity",
                "result": "RELATIVE_ACTION_CANDIDATE_ONLY",
                "why_not_closed": "QMA970 says inputs are unsigned; 1304 says parent adoption and sign are missing",
            }
        ),
        row(
            {
                "id": "PAT1980_1_Zm_from_metric",
                "target": "derive Z_m>0 from a parent field-space metric",
                "evidence": "617 and 1025 identify normalization/field-metric route but do not find owner",
                "result": "NOT_PARENT_SIGNED",
                "why_not_closed": "no source-signed M_AB or memory-direction metric restriction exists in current checkpoint corpus",
            }
        ),
        row(
            {
                "id": "PAT1980_2_M2_from_extremum",
                "target": "derive M2_min>0 from local branch extremum",
                "evidence": "1977/1979 distinguish extremum from strict Hessian gap",
                "result": "REJECTED_TOO_WEAK",
                "why_not_closed": "partial_m V_R=0 or stability permits zero curvature, flat directions, and zero modes",
            }
        ),
        row(
            {
                "id": "PAT1980_3_M2_from_convex_VR",
                "target": "derive M2_min>0 from a convex memory potential",
                "evidence": "1304/1348 name V_R and M_m^2=partial_m^2 V_R",
                "result": "FORMULA_READY_PARENT_FUNCTION_MISSING",
                "why_not_closed": "current corpus does not supply V_R(m;X_B), convexity theorem, or Hessian lower bound",
            }
        ),
        row(
            {
                "id": "PAT1980_4_zero_modes",
                "target": "remove constant/gauge memory zero modes",
                "evidence": "968 and 1979 require domain, boundary class, and zero-mode projection",
                "result": "NOT_PARENT_SELECTED",
                "why_not_closed": "D_loc, boundary class, and quotient projection are not selected by parent action",
            }
        ),
        row(
            {
                "id": "PAT1980_5_corrections",
                "target": "bound Eta_H below the positive floor",
                "evidence": "1979 packages Eta_H as source/boundary/X_B correction norm",
                "result": "BOOKKEEPING_READY_VALUE_MISSING",
                "why_not_closed": "source, boundary, representative, and X_B correction norms are not bounded",
            }
        ),
    ]

    negative_results = [
        row(
            {
                "id": "NEG1980_0_extremum_not_gap",
                "negative_result": "Euler zero does not imply mass gap",
                "precise_statement": "partial_m V_R(m_L;X_B)=0 is compatible with partial_m^2 V_R=0, negative curvature, or a flat modulus unless strict second-variation positivity is separately proven.",
                "effect": "M2_min cannot be inferred from F1=0, branch selection, or stationarity language",
            }
        ),
        row(
            {
                "id": "NEG1980_1_candidate_not_parent",
                "negative_result": "candidate action does not imply parent action",
                "precise_statement": "A quadratic operator written as a useful ansatz proves the form of the needed theorem, but it does not sign the parent field-space metric or potential Hessian.",
                "effect": "Z_m and M2_min remain missing even though the operator algebra is now clean",
            }
        ),
        row(
            {
                "id": "NEG1980_2_rescaling_not_sign",
                "negative_result": "field rescaling cannot manufacture ownership",
                "precise_statement": "m -> a m rescales Z_m and M_m^2 together; it cannot turn an unsigned or indefinite parent quadratic form into a signed one.",
                "effect": "normalization must be fixed by the parent metric/observable map before any local bound",
            }
        ),
        row(
            {
                "id": "NEG1980_3_double_zero_not_operator",
                "negative_result": "double-zero gating is not the same as positive memory no-hair",
                "precise_statement": "A gate that kills local coupling can also degenerate the operator at the branch unless the active kinetic/Hessian sector survives independently.",
                "effect": "double-zero decoupling and positive-operator proof must stay separate branches",
            }
        ),
    ]

    closure_contract = [
        row(
            {
                "id": "CLOS1980_0_private_positive_memory",
                "closure_name": "private positive-memory closure",
                "closure_assumption": "Assume the parent action signs Z_m>=Z_min>0 and M_m^2>=M2_min>0 on the selected local branch, with zero modes projected out.",
                "allowed_use": "private algebraic continuation and future finite-row smoke tests",
                "forbidden_use": "derived local-GR/Newton claim; R10/PPN/clock/orbital pass; public theorem language",
                "activation_status": "AVAILABLE_BUT_NOT_ACTIVATED",
            }
        ),
        row(
            {
                "id": "CLOS1980_1_retained_residual",
                "closure_name": "finite retained memory residual",
                "closure_assumption": "Do not assume positivity; keep Z_m, M2_min, B_mem, C_mem, J_mem, and boundary memory charge as explicit residual coefficients.",
                "allowed_use": "coefficient acquisition, no-cancellation envelopes, and empirical pressure rows",
                "forbidden_use": "silencing local f(R)/R2 leakage by language",
                "activation_status": "SAFE_FALLBACK",
            }
        ),
        row(
            {
                "id": "CLOS1980_2_parent_action_hunt",
                "closure_name": "derivation-first continuation",
                "closure_assumption": "Before activating closure, hunt for a parent action memory metric/potential source that can sign the lemma.",
                "allowed_use": "next target",
                "forbidden_use": "repeating the same positivity theorem without new parent-action evidence",
                "activation_status": "SELECTED_NEXT",
            }
        ),
    ]

    impact = [
        row(
            {
                "id": "IMP1980_0_real_progress",
                "area": "local GR / EH reduction",
                "finding": "The missing coupling/sign problem is now localized to the parent memory quadratic sector, not the downstream PPN/R10 runner.",
                "consequence": "If 1981 finds the parent memory metric and convex potential signature, 1979 becomes executable rather than merely conditional.",
            }
        ),
        row(
            {
                "id": "IMP1980_1_current_status",
                "area": "claim status",
                "finding": "Current corpus still does not prove Z_m>0 or M2_min>0.",
                "consequence": "No derived local-GR/Newton claim is allowed yet.",
            }
        ),
        row(
            {
                "id": "IMP1980_2_best_route",
                "area": "next route",
                "finding": "Search or construct the parent action signature directly: field-space metric restricted to m plus strict local V_R Hessian.",
                "consequence": "This is the shortest route to either a serious derivation or an honest closure declaration.",
            }
        ),
    ]

    claim_gate = [
        row(
            {
                "id": "GATE1980_0_Zm",
                "gate": "Z_m positive parent-signed",
                "status": "BLOCKED",
                "reason": "field-space metric/sign convention is not parent-owned",
                "required_to_open": "parent action row or theorem proving Z_m>=Z_min>0 with units",
            }
        ),
        row(
            {
                "id": "GATE1980_1_M2",
                "gate": "M2_min positive parent-signed",
                "status": "BLOCKED",
                "reason": "strict local Hessian/convexity theorem is absent",
                "required_to_open": "V_R functional or theorem proving partial_m^2 V_R>=M2_min>0 after quotient",
            }
        ),
        row(
            {
                "id": "GATE1980_2_Gm",
                "gate": "G_m positive",
                "status": "BLOCKED",
                "reason": "Z_min, M2_min, lambda_1, and Eta_H are not all signed",
                "required_to_open": "G_m=Z_min lambda_1 + M2_min - Eta_H > 0",
            }
        ),
        row(
            {
                "id": "GATE1980_3_local_GR",
                "gate": "derived local GR/Newton limit",
                "status": "BLOCKED",
                "reason": "positive memory operator remains conditional",
                "required_to_open": "1981 parent action signature plus downstream source/boundary silence",
            }
        ),
    ]

    decision = [
        row(
            {
                "id": "DEC1980_0_lemma",
                "decision": "CONDITIONAL_PARENT_MEMORY_POSITIVITY_LEMMA_WRITTEN",
                "because": "Z_m and M2_min are exactly the signs needed by 1979, and the proof is standard once the parent signs them.",
                "next_action": "hunt parent action signature rather than rerun the same operator proof",
            }
        ),
        row(
            {
                "id": "DEC1980_1_no_promotion",
                "decision": "DO_NOT_PROMOTE_TO_LOCAL_GR",
                "because": "all current evidence says action/operator forms are candidates or formulas, not parent-signed signs/values.",
                "next_action": "keep all claim gates blocked",
            }
        ),
        row(
            {
                "id": "DEC1980_2_best_next",
                "decision": "PARENT_ACTION_SIGN_HUNT",
                "because": "the only non-circular leap is to find or construct the signed memory metric and strict potential Hessian in the parent action.",
                "next_action": "1981-Y5-R2FR-parent-memory-action-signature-source-hunt-or-closure-activation.md",
            }
        ),
    ]

    next_rows = [
        row(
            {
                "id": "NEXT1980_0_primary",
                "status": "selected",
                "target_doc": "1981-Y5-R2FR-parent-memory-action-signature-source-hunt-or-closure-activation.md",
                "target_script": "scripts/Y5_R2FR_parent_memory_action_signature_source_hunt_or_closure_activation_1981.py",
                "task": "search the corpus for the actual parent memory action/signature source; if absent, create a first explicit closure activation/nonactivation ledger and retained residual branch.",
                "success_condition": "source-backed Z_m/M2_min signs, or explicit declaration that the local memory positivity route is closure-only until new parent action text is supplied",
            }
        )
    ]

    snapshot = [
        row(
            {
                "id": "SNAP1980_0_position",
                "area": "full project",
                "status": "PROMISING_BUT_NOT_DERIVED",
                "summary": "The downstream local-GR machinery is getting sharper; the central missing item is now a parent-signed positive memory quadratic sector.",
            }
        ),
        row(
            {
                "id": "SNAP1980_1_what_is_sure",
                "area": "sure result",
                "status": "CONDITIONAL_THEOREM",
                "summary": "If Z_m>0, M2_min>0, domain/projection, and small Eta_H are supplied, the local memory inverse bound follows.",
            }
        ),
        row(
            {
                "id": "SNAP1980_2_what_is_not_sure",
                "area": "not yet sure",
                "status": "PARENT_SIGNATURE_MISSING",
                "summary": "The current corpus does not yet prove the signs from the parent action; this blocks derived local GR/Newton.",
            }
        ),
    ]

    source_weight = [
        row(
            {
                "id": "SW1980_0",
                "doc": DOC_PATH.name,
                "weight": "private_nonclaim_conditional_theorem_and_negative_result",
                "claim_safety": "all claim flags false; closure not activated",
                "use": "parent memory positivity gate for local EH/R2-fR suppression",
            }
        )
    ]

    queue = [
        row(
            {
                "id": "Q1980_0_parent_action_signature",
                "quantity": "parent memory action signature",
                "priority": "highest",
                "why": "needed to sign Z_m>0 and M2_min>0 without closure",
                "target": "1981 source hunt",
            }
        ),
        row(
            {
                "id": "Q1980_1_VR_convexity",
                "quantity": "V_R(m;X_B) Hessian theorem",
                "priority": "highest",
                "why": "needed for strict memory mass gap",
                "target": "1981 source hunt or closure activation",
            }
        ),
        row(
            {
                "id": "Q1980_2_metric_normalization",
                "quantity": "memory field-space metric normalization",
                "priority": "high",
                "why": "needed to make Z_m sign and units invariant",
                "target": "1981 source hunt",
            }
        ),
    ]

    return {
        "source_register": source_register_rows(),
        "lemma": lemma,
        "proof_attempt": proof_attempt,
        "negative_results": negative_results,
        "closure_contract": closure_contract,
        "impact": impact,
        "claim_gate": claim_gate,
        "decision": decision,
        "next": next_rows,
        "snapshot": snapshot,
        "source_weight": source_weight,
        "queue": queue,
    }


def all_claim_flags_false(tables: dict[str, list[dict[str, str]]]) -> bool:
    for table_rows in tables.values():
        for table_row in table_rows:
            if table_row.get("valid_for_claim") != "false" or table_row.get("public_claim") != "false":
                return False
    return True


def output_csvs_parse() -> bool:
    for path in OUTPUTS.values():
        with path.open(newline="", encoding="utf-8") as handle:
            parsed_rows = list(csv.DictReader(handle))
        if not parsed_rows:
            return False
    return True


def formalization_1980_artifact_count() -> int:
    if not FORMALIZATION.exists():
        return 0
    return len([path for path in FORMALIZATION.rglob("*1980*") if path.is_file()])


def validate(tables: dict[str, list[dict[str, str]]]) -> list[dict[str, str]]:
    source_ok = all(
        table_row["exists"] == "true" and table_row["needle_status"] == "PASS"
        for table_row in tables["source_register"]
    )
    lemma_by_id = {table_row["id"]: table_row for table_row in tables["lemma"]}
    proof_by_id = {table_row["id"]: table_row for table_row in tables["proof_attempt"]}
    negative_by_id = {table_row["id"]: table_row for table_row in tables["negative_results"]}
    gate_safe = all(table_row["status"] == "BLOCKED" for table_row in tables["claim_gate"])
    closure_not_public = all("public" not in table_row["allowed_use"].lower() for table_row in tables["closure_contract"])
    next_selected = tables["next"][0]["target_doc"] == "1981-Y5-R2FR-parent-memory-action-signature-source-hunt-or-closure-activation.md"
    pycache_path = ROOT / "scripts" / "__pycache__"
    formalization_count = formalization_1980_artifact_count()
    specs = [
        ("VAL1980_00_sources", source_ok, "all source paths exist and continuity needles found"),
        (
            "VAL1980_01_conditional_lemma",
            lemma_by_id["LEM1980_3_Gm"]["status"] == "CONDITIONAL_THEOREM_COMPLETE",
            "G_m positivity lemma is conditionally complete",
        ),
        (
            "VAL1980_02_Zm_not_signed",
            proof_by_id["PAT1980_1_Zm_from_metric"]["result"] == "NOT_PARENT_SIGNED",
            "Z_m positivity not parent signed",
        ),
        (
            "VAL1980_03_M2_extremum_rejected",
            proof_by_id["PAT1980_2_M2_from_extremum"]["result"] == "REJECTED_TOO_WEAK",
            "extremum alone rejected as mass-gap proof",
        ),
        (
            "VAL1980_04_negative_results",
            negative_by_id["NEG1980_0_extremum_not_gap"]["negative_result"] == "Euler zero does not imply mass gap",
            "negative result prevents smuggled mass gap",
        ),
        ("VAL1980_05_closure_safe", closure_not_public, "closure contract remains private/nonclaim"),
        ("VAL1980_06_claim_gates", gate_safe, "all claim gates remain blocked"),
        (
            "VAL1980_07_decision",
            tables["decision"][-1]["decision"] == "PARENT_ACTION_SIGN_HUNT",
            "decision selects parent action sign hunt",
        ),
        ("VAL1980_08_next_target", next_selected, "1981 target selected"),
        ("VAL1980_09_claim_flags_safe", all_claim_flags_false(tables), "claim flags all false"),
        ("VAL1980_10_csv_parse", output_csvs_parse(), "all generated CSVs parse with rows"),
        ("VAL1980_11_pycache_absent", not pycache_path.exists(), "scripts __pycache__ absent"),
        ("VAL1980_12_formalization_untouched", formalization_count == 0, f"formalization_1980_artifact_count={formalization_count}"),
    ]
    rows = [
        {
            "validation_id": validation_id,
            "status": "PASS" if passed else "FAIL",
            "detail": detail,
            "valid_for_claim": "false",
            "public_claim": "false",
        }
        for validation_id, passed, detail in specs
    ]
    rows.append(
        {
            "validation_id": "VAL1980_OVERALL",
            "status": "PASS" if all(table_row["status"] == "PASS" for table_row in rows) else "FAIL",
            "detail": "1980 parent memory positivity lemma or closure fork",
            "valid_for_claim": "false",
            "public_claim": "false",
        }
    )
    return rows


def markdown_table(rows: list[dict[str, str]]) -> str:
    headers = list(rows[0].keys())
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for table_row in rows:
        values = [table_row.get(header, "").replace("|", "\\|").replace("\n", "<br>") for header in headers]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def proof_text() -> str:
    return "\n".join(
        [
            "## Conditional Positivity Lemma",
            "",
            "Let the local memory fluctuation around the branch be `delta m`. If the parent action has a static second variation",
            "",
            "`delta^2 E_m = integral_D sqrt(h)[Z_m h^{ij} partial_i delta m partial_j delta m + M_m^2(delta m)^2] + E_H[delta m,delta m]`,",
            "",
            "with `Z_m>=Z_min>0`, `M_m^2>=M2_min>0`, domain/projection `lambda_1(D_loc)>0`, and `|E_H[u,u]|<=Eta_H||u||_2^2`, then",
            "",
            "`delta^2 E_m >= (Z_min lambda_1(D_loc)+M2_min-Eta_H)||delta m||_2^2`.",
            "",
            "So if `G_m=Z_min lambda_1(D_loc)+M2_min-Eta_H>0`, the memory branch is locally coercive and the 1979 inverse bound follows.",
            "",
            "The proof is solid. The current corpus problem is not this theorem; it is that the parent action has not yet signed `Z_m>0`, `M2_min>0`, the domain/projection, or `Eta_H`.",
            "",
        ]
    )


def write_markdown(tables: dict[str, list[dict[str, str]]], validation_rows: list[dict[str, str]]) -> None:
    sections = [
        ("Source Register", tables["source_register"]),
        ("Memory Positivity Lemma", tables["lemma"]),
        ("Proof Attempt Audit", tables["proof_attempt"]),
        ("Negative Results", tables["negative_results"]),
        ("Closure Contract", tables["closure_contract"]),
        ("Local GR Impact", tables["impact"]),
        ("Claim Gate", tables["claim_gate"]),
        ("Decision Ledger", tables["decision"]),
        ("Next Target", tables["next"]),
        ("Project Status Snapshot", tables["snapshot"]),
        ("Validation", validation_rows),
    ]
    lines = [
        "# 1980 Y5 R2FR: Parent Memory Positivity Lemma Or Closure",
        "",
        "Private checkpoint. This is the direct attack on the sign/coupling gap exposed by 1979.",
        "",
        "Verdict: the parent memory positivity theorem is conditionally proved, but not parent-owned. The theorem is simple and strong: a signed memory kinetic metric, strict memory Hessian gap, selected domain/projection, and small correction norm make the local memory operator coercive. Current files still show those signs as candidate/formula-only, so the derived local-GR/Newton route remains blocked rather than failed.",
        "",
        "No local-GR, EH, R10, PPN, clock, orbital, or public claim follows from 1980.",
        "",
        proof_text(),
    ]
    for title, rows in sections:
        lines.extend([f"## {title}", "", markdown_table(rows), ""])
    DOC_PATH.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    ensure_dirs()
    pycache_path = ROOT / "scripts" / "__pycache__"
    if pycache_path.exists():
        shutil.rmtree(pycache_path)
    tables = build_tables()
    for output_name, path in OUTPUTS.items():
        write_csv(path, tables[output_name])
    validation_rows = validate(tables)
    write_csv(VALIDATION_PATH, validation_rows)
    write_markdown(tables, validation_rows)
    if pycache_path.exists():
        shutil.rmtree(pycache_path)
    overall = validation_rows[-1]["status"]
    print(f"wrote {DOC_PATH}")
    print(f"wrote {VALIDATION_PATH}")
    print(f"VAL1980_OVERALL={overall}")
    return 0 if overall == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
