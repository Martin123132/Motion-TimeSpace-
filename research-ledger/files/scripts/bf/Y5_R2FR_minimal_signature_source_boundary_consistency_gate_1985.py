from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


BRANCH = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
FORMALIZATION = REPO / "formalization-workbench"
MTS_RESIDUALS = ROOT / "source-intake" / "mts_residuals"
SOURCE_WEIGHT_DOCS = ROOT / "source-intake" / "source-weight" / "docs"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"

DOC_PATH = ROOT / "1985-Y5-R2FR-minimal-signature-source-boundary-consistency-gate.md"
VALIDATION_PATH = MTS_RESIDUALS / "P8_Y5_BRR545_1985_VALIDATION.csv"

SOURCES = {
    "1984_doc": {
        "path": ROOT / "1984-Y5-R2FR-minimal-parent-memory-signature-contract-or-route-demotion.md",
        "needles": ["COMP1984_0_no_hidden_fifth_force", "NEXT1984_0_primary"],
    },
    "1984_validation": {
        "path": MTS_RESIDUALS / "P8_Y5_BRR545_1984_VALIDATION.csv",
        "needles": ["VAL1984_OVERALL", "PASS"],
    },
    "1386_package": {
        "path": MTS_RESIDUALS / "P8_Y5_R10_1386_PARENT_PACKAGE_CLAUSE_MATRIX.csv",
        "needles": ["PCM1386_7_package_verdict", "PACKAGE_FAILS_CURRENT_CLAIM"],
    },
    "1386_zero": {
        "path": MTS_RESIDUALS / "P8_Y5_R10_1386_GC_ZERO_THEOREM_ATTEMPT.csv",
        "needles": ["GCT1386_4_zero_verdict", "ZERO_THEOREM_NOT_CLOSED_CURRENT_CORPUS"],
    },
    "1387_action_weight": {
        "path": MTS_RESIDUALS / "P8_Y5_R10_1387_ACTION_WEIGHT_EXCLUSION_AUDIT.csv",
        "needles": ["AWE1387_7_verdict", "COUNTEREXAMPLE_SURVIVES_FIRST_FILL_REQUIRED"],
    },
    "1387_delta_w": {
        "path": MTS_RESIDUALS / "P8_Y5_R10_1387_DELTA_W_SOURCE_BETA_FIRST_FILL.csv",
        "needles": ["DWB1387_6_first_fill_verdict", "NONCLAIM_FIRST_FILL_READY"],
    },
    "1540_selector": {
        "path": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1540_COUPLING_SELECTOR_THEOREM_ATTEMPT.csv",
        "needles": ["CSEL1540_6_current_verdict", "THEOREM_NOT_CLOSED"],
    },
    "1584_gr": {
        "path": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1584_GR_REDUCTION_RUNNER.csv",
        "needles": ["RUN1584_4_local_gr", "BLOCKED_NO_CLAIM"],
    },
    "1592_signature": {
        "path": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1592_PARENT_SIGNATURE_AUDIT.csv",
        "needles": ["PSA1592_6_local_GR_reentry", "LOCAL_GR_REENTRY_STILL_BLOCKED"],
    },
    "1042_nohair": {
        "path": MTS_RESIDUALS / "P8_Y5_R10_1042_NOHAIR_PREMISE_GATE.csv",
        "needles": ["NHP1042_6_verdict", "FAIL_CURRENT_CLAIM_NOHAIR_NOT_PARENT_SIGNED"],
    },
    "1043_jx_boundary": {
        "path": ROOT / "1043-Y5-R10-JX-zero-and-Phi-boundary-zero-premise-or-alpha3-prior-value.md",
        "needles": ["J_X zero channel audit", "R_X_ZERO_BLOCKED_CURRENT_CORPUS"],
    },
    "1027_qbar": {
        "path": ROOT / "1027-Y5-R10-qbarXT-source-zero-or-bounded-coupling-row.md",
        "needles": ["QZ1027_6_verdict", "FAIL_CURRENT_CLAIM"],
    },
    "1030_spm": {
        "path": ROOT / "1030-Y5-R10-single-public-metric-parent-action-derivation-or-cg-provenance-gate.md",
        "needles": ["SPM1030_6_contract_verdict", "CONTRACT_READY_NOT_CURRENT_THEOREM"],
    },
    "1012_newton_norm": {
        "path": ROOT / "1012-Y5-R10-Y5-source-normalization-owner-or-q_loc-bound-implementation.md",
        "needles": ["Y5O1012_7_Newton_Poisson_orbit", "conditional_not_parent_derived"],
    },
    "1013_measured_gm": {
        "path": ROOT / "1013-Y5-R10-PiM-JH-flux-closure-or-measured-GM-obstruction-score.md",
        "needles": ["PFC1013_8_verdict", "fail_current_claim"],
    },
}

OUTPUTS = {
    "source_register": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1985_SOURCE_REGISTER.csv",
    "consistency_matrix": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1985_SOURCE_BOUNDARY_CONSISTENCY_MATRIX.csv",
    "residual_vector": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1985_RETAINED_RESIDUAL_VECTOR.csv",
    "compatibility_verdict": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1985_CONTRACT_COMPATIBILITY_VERDICT.csv",
    "claim_gate": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1985_CLAIM_GATE.csv",
    "decision": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1985_DECISION_LEDGER.csv",
    "next": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1985_NEXT_TARGET.csv",
    "snapshot": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1985_PROJECT_STATUS_SNAPSHOT.csv",
    "source_weight": SOURCE_WEIGHT_DOCS / "MINIMAL_SIGNATURE_SOURCE_BOUNDARY_GATE_1985_NONCLAIM.csv",
    "queue": RAB_QUEUE / "JR1985_FINITE_RESIDUAL_VECTOR_SCORING_QUEUE.csv",
}


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


CREATED_AT = now()


def ensure_dirs() -> None:
    for path in [MTS_RESIDUALS, SOURCE_WEIGHT_DOCS, RAB_QUEUE, DOC_PATH.parent]:
        path.mkdir(parents=True, exist_ok=True)


def row(values: dict[str, object]) -> dict[str, str]:
    defaults = {
        "branch": BRANCH,
        "id": "",
        "valid_for_claim": "false",
        "public_claim": "false",
        "created_at_utc": CREATED_AT,
    }
    merged = {**defaults, **values}
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
                    "id": f"SRC1985_{len(rows):02d}_{source_id}",
                    "source_id": source_id,
                    "source_path": str(path),
                    "required_needles": "; ".join(config["needles"]),
                    "exists": str(path.exists()).lower(),
                    "needle_status": "PASS" if not missing else "MISSING: " + "; ".join(missing),
                    "role": "source/boundary/canonical/conservation/Newton consistency gate input",
                }
            )
        )
    return rows


def build_tables() -> dict[str, list[dict[str, str]]]:
    consistency_matrix = [
        row(
            {
                "id": "SBG1985_0_source_zero",
                "gate": "J_m / canonical source zero",
                "required_for_gr": "J_c=0 channelwise, or every source component has a finite no-cancellation bound.",
                "current_evidence": "1386/1540/1027/1043 give conditional chain-rule/source-zero routes but say the parent package is unsigned.",
                "status": "FAIL_CURRENT_DERIVATION_RETAIN_RESIDUAL",
                "residual_if_open": "J_c, qbar_XT, beta_source, beta_test, hidden-source tails",
            }
        ),
        row(
            {
                "id": "SBG1985_1_boundary_zero",
                "gate": "boundary/readout/projector silence",
                "required_for_gr": "Phi_boundary_local=0 or source-bounded boundary/readout/projector tails.",
                "current_evidence": "1042/1043 and 1540 keep boundary flux/readout/projector silence unsigned.",
                "status": "FAIL_CURRENT_DERIVATION_RETAIN_RESIDUAL",
                "residual_if_open": "Phi_boundary, q_boundary, readout tail, projector tail",
            }
        ),
        row(
            {
                "id": "SBG1985_2_action_weights",
                "gate": "pre-variation action-weight exclusion",
                "required_for_gr": "No independent species/source action multiplier, or w_A common/quotient-equivalent/null-projected.",
                "current_evidence": "1387 proves the counterexample survives; Delta_w/beta_w first-fill rows are required.",
                "status": "COUNTEREXAMPLE_SURVIVES_RETAIN_RESIDUAL",
                "residual_if_open": "Delta_w_A, beta_w_source, beta_w_test, measured-G absorption guard",
            }
        ),
        row(
            {
                "id": "SBG1985_3_canonical_transfer",
                "gate": "canonical Z_m transfer audit",
                "required_for_gr": "Z_m=1 canonical units must transfer into V_R, J_m, qbar, alpha, PPN/Newton normalization with no hidden knob.",
                "current_evidence": "1306/1384 say constant canonicalization is only private unless every transferred coupling is audited.",
                "status": "OPEN_TRANSFER_AUDIT_REQUIRED",
                "residual_if_open": "mu_m^2 law, J_c normalization, K_alpha, PPN source normalization",
            }
        ),
        row(
            {
                "id": "SBG1985_4_conservation",
                "gate": "Ward/Bianchi/conservation closure",
                "required_for_gr": "Memory stress, matter, source/bath and boundary terms obey same-parent conservation.",
                "current_evidence": "1584 refuses GR upgrade; 1030 says source-side GR/Newton is contract-ready but not current theorem.",
                "status": "FAIL_CURRENT_DERIVATION_RETAIN_RESIDUAL",
                "residual_if_open": "non-Hilbert current, source current, q_loc, H_tau/M_H_ref tails",
            }
        ),
        row(
            {
                "id": "SBG1985_5_newton_source_normalization",
                "gate": "source-normalized Newton / measured GM",
                "required_for_gr": "same charge sources Poisson/Gauss and inverse-square orbital acceleration with calibrated measured GM.",
                "current_evidence": "1012/1013 keep Newton Poisson/orbit calibration and Pi_M J_H flux closure not parent-derived.",
                "status": "FAIL_CURRENT_DERIVATION_RETAIN_RESIDUAL",
                "residual_if_open": "M_eff flux, Gdot/GM drift, radial/range/species/frame residuals",
            }
        ),
        row(
            {
                "id": "SBG1985_6_arena_matching",
                "gate": "same-parent arena matching",
                "required_for_gr": "one Z_m/mu_m/source law feeds local, cosmology, galaxy, clock/orbital arenas without retuning.",
                "current_evidence": "1984 makes this a contract clause; no source-backed arena map exists yet.",
                "status": "OPEN_SAME_PARENT_MAP_REQUIRED",
                "residual_if_open": "arena retune deltas, prior-edge flags, hidden coefficient branches",
            }
        ),
        row(
            {
                "id": "SBG1985_7_empirical_residual_score",
                "gate": "finite residual scoreability",
                "required_for_gr": "If any previous gate remains open, residuals must be scoreable against R10/PPN/clocks/orbital/cosmology.",
                "current_evidence": "many residual rows exist but are not assembled into one memory-route vector.",
                "status": "NEXT_VECTOR_REQUIRED",
                "residual_if_open": "R10 alpha(lambda), PPN gamma/beta, clock, orbital, cosmology residual vector",
            }
        ),
    ]

    residual_vector = [
        row(
            {
                "id": "RES1985_0_Jc",
                "residual": "J_c / J_m",
                "definition": "canonical memory source after field normalization and source decomposition",
                "required_source": "parent source-zero theorem or finite channelwise bounds",
                "status": "MISSING_ZERO_OR_BOUND",
                "test_arenas": "R10;PPN;clock;orbital;cosmology",
            }
        ),
        row(
            {
                "id": "RES1985_1_beta",
                "residual": "beta_source,beta_test,qbar_XT",
                "definition": "source/test coupling of the memory/canonical scalar to matter/readout",
                "required_source": "same-parent matter descent or finite composition/source rows",
                "status": "MISSING_ZERO_OR_BOUND",
                "test_arenas": "R10;WEP;clock;PPN",
            }
        ),
        row(
            {
                "id": "RES1985_2_boundary",
                "residual": "Phi_boundary/readout/projector tail",
                "definition": "boundary flux, projection, readout, topology, and hidden-domain contribution to no-hair RHS",
                "required_source": "boundary silence theorem or finite no-cancellation envelope",
                "status": "MISSING_ZERO_OR_BOUND",
                "test_arenas": "R10;orbital;clock;PPN",
            }
        ),
        row(
            {
                "id": "RES1985_3_action_weight",
                "residual": "Delta_w_A,beta_w_source,beta_w_test",
                "definition": "pre-variation source/action-weight obstruction to common matter and Newton source normalization",
                "required_source": "object-language/action-measure exclusion theorem or finite source weights",
                "status": "FIRST_FILL_READY_VALUES_MISSING",
                "test_arenas": "WEP;Newton;R10;clock",
            }
        ),
        row(
            {
                "id": "RES1985_4_conservation",
                "residual": "q_nonH/q_loc/source-current tail",
                "definition": "non-Hilbert current, retained q_loc, source-current or response-doublet obstruction",
                "required_source": "same-parent Ward/Bianchi closure or finite current bounds",
                "status": "MISSING_ZERO_OR_BOUND",
                "test_arenas": "PPN;orbital;clock;local-GR",
            }
        ),
        row(
            {
                "id": "RES1985_5_newton_gm",
                "residual": "M_eff/G_eff/GM calibration residual",
                "definition": "failure of same charge to source Poisson/Gauss, orbit acceleration, and measured-GM normalization",
                "required_source": "Pi_M J_H flux closure, worldtube glue, and Newton calibration",
                "status": "MISSING_ZERO_OR_BOUND",
                "test_arenas": "Newton;orbital;Gdot;PPN",
            }
        ),
        row(
            {
                "id": "RES1985_6_arena",
                "residual": "arena retune delta",
                "definition": "difference between local/cosmology/galaxy coefficient law if not one parent map",
                "required_source": "same-parent arena map or finite retuning penalty",
                "status": "MISSING_ZERO_OR_BOUND",
                "test_arenas": "cosmology;galaxy;local",
            }
        ),
    ]

    compatibility_verdict = [
        row(
            {
                "id": "VER1985_0_internal_viability",
                "question": "Is the 1984 constructed contract internally viable as a future derivation target?",
                "answer": "CONDITIONALLY_YES_BUT_NOT_CURRENTLY_DERIVED",
                "because": "the contract is mathematically coherent if source, boundary, conservation, Newton, and arena gates all close together",
                "effect": "keep it as a target, not a claim",
            }
        ),
        row(
            {
                "id": "VER1985_1_current_status",
                "question": "Does the current corpus close the 1985 consistency gates?",
                "answer": "NO",
                "because": "source-zero, boundary, action-weight, conservation, Newton-source, and arena-matching gates remain unsigned or fail",
                "effect": "local-GR/Newton route remains blocked",
            }
        ),
        row(
            {
                "id": "VER1985_2_best_route",
                "question": "What is the safest next implementation?",
                "answer": "BUILD_FINITE_RESIDUAL_VECTOR",
                "because": "if derivation gates are open, the competitive framework needs no-cancellation residual rows that can be empirically scored",
                "effect": "move from contract-only to testable residual bookkeeping",
            }
        ),
    ]

    claim_gate = [
        row(
            {
                "id": "GATE1985_0_source_boundary",
                "gate": "source/boundary gate closes",
                "status": "BLOCKED",
                "reason": "J_c/qbar/source, boundary/readout, and hidden tails are not zero or bounded",
                "required_to_open": "same-parent source-zero/boundary silence theorem or finite residual vector",
            }
        ),
        row(
            {
                "id": "GATE1985_1_common_matter",
                "gate": "common matter/Newton source normalization",
                "status": "BLOCKED",
                "reason": "action-weight and measured-GM counterexamples survive",
                "required_to_open": "action-measure/object-language theorem and Pi_M J_H/Newton calibration",
            }
        ),
        row(
            {
                "id": "GATE1985_2_local_GR",
                "gate": "derived local GR/Newton",
                "status": "BLOCKED",
                "reason": "positive operator plus constructed contract is insufficient without all consistency gates",
                "required_to_open": "1984 contract source-signed plus 1985 gates closed",
            }
        ),
    ]

    decision = [
        row(
            {
                "id": "DEC1985_0_contract_viability",
                "decision": "CONTRACT_REMAINS_FUTURE_TARGET_NOT_CURRENT_DERIVATION",
                "because": "no logical contradiction is found, but source/boundary/conservation/Newton gates are open",
                "next_action": "do not discard the route; do not claim it",
            }
        ),
        row(
            {
                "id": "DEC1985_1_residual_priority",
                "decision": "FINITE_RESIDUAL_VECTOR_REQUIRED",
                "because": "open gates must become explicit no-cancellation residuals to make the framework testable",
                "next_action": "assemble memory-route residual vector with units/source slots and arena mapping",
            }
        ),
        row(
            {
                "id": "DEC1985_2_best_next",
                "decision": "MEMORY_ROUTE_RESIDUAL_VECTOR_PACK",
                "because": "this converts derivation blockers into scoreable empirical pressure rows instead of rearguing the theorem",
                "next_action": "1986-Y5-R2FR-memory-route-finite-residual-vector-pack.md",
            }
        ),
    ]

    next_rows = [
        row(
            {
                "id": "NEXT1985_0_primary",
                "status": "selected",
                "target_doc": "1986-Y5-R2FR-memory-route-finite-residual-vector-pack.md",
                "target_script": "scripts/Y5_R2FR_memory_route_finite_residual_vector_pack_1986.py",
                "task": "assemble the finite residual vector for the memory-positive local-GR route: J_c, beta/qbar, boundary/readout, action weights, conservation/source-current, measured-GM/Newton, and arena-retune components.",
                "success_condition": "one nonclaim vector with units, source slots, no-cancellation rule, and test arenas; no local-GR claim unless components are theorem-zero or source-bounded",
            }
        )
    ]

    snapshot = [
        row(
            {
                "id": "SNAP1985_0_status",
                "area": "minimal contract",
                "status": "INTERNALLY_COHERENT_TARGET_ONLY",
                "summary": "No contradiction found, but it is not derived and all consistency gates remain open.",
            }
        ),
        row(
            {
                "id": "SNAP1985_1_local_gr",
                "area": "local GR/Newton",
                "status": "BLOCKED",
                "summary": "The source/boundary/action-weight/conservation/Newton gates block local-GR promotion.",
            }
        ),
        row(
            {
                "id": "SNAP1985_2_next",
                "area": "testability",
                "status": "RESIDUAL_VECTOR_NEXT",
                "summary": "The next move is empirical discipline: retain finite residuals with no-cancellation scoring.",
            }
        ),
    ]

    source_weight = [
        row(
            {
                "id": "SW1985_0",
                "doc": DOC_PATH.name,
                "weight": "private_nonclaim_consistency_gate",
                "claim_safety": "all claim flags false; gates blocked; residual vector selected",
                "use": "tests whether minimal parent signature contract can support local-GR route",
            }
        )
    ]

    queue = [
        row(
            {
                "id": "Q1985_0_residual_vector",
                "quantity": "finite memory-route residual vector",
                "priority": "highest",
                "why": "open derivation gates must become scoreable no-cancellation residuals",
                "target": "1986 residual vector pack",
            }
        )
    ]

    return {
        "source_register": source_register_rows(),
        "consistency_matrix": consistency_matrix,
        "residual_vector": residual_vector,
        "compatibility_verdict": compatibility_verdict,
        "claim_gate": claim_gate,
        "decision": decision,
        "next": next_rows,
        "snapshot": snapshot,
        "source_weight": source_weight,
        "queue": queue,
    }


def all_claim_flags_false(tables: dict[str, list[dict[str, str]]]) -> bool:
    return all(
        item.get("valid_for_claim") == "false" and item.get("public_claim") == "false"
        for rows in tables.values()
        for item in rows
    )


def output_csvs_parse() -> bool:
    for path in OUTPUTS.values():
        with path.open(newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
        if not rows:
            return False
    return True


def formalization_1985_artifact_count() -> int:
    if not FORMALIZATION.exists():
        return 0
    return len([path for path in FORMALIZATION.rglob("*1985*") if path.is_file()])


def validate(tables: dict[str, list[dict[str, str]]]) -> list[dict[str, str]]:
    sources_ok = all(row_data["exists"] == "true" and row_data["needle_status"] == "PASS" for row_data in tables["source_register"])
    failures_retained = all(
        row_data["status"] in {
            "FAIL_CURRENT_DERIVATION_RETAIN_RESIDUAL",
            "COUNTEREXAMPLE_SURVIVES_RETAIN_RESIDUAL",
            "OPEN_TRANSFER_AUDIT_REQUIRED",
            "OPEN_SAME_PARENT_MAP_REQUIRED",
            "NEXT_VECTOR_REQUIRED",
        }
        for row_data in tables["consistency_matrix"]
    )
    residuals_missing = all("MISSING" in row_data["status"] or "FIRST_FILL_READY" in row_data["status"] for row_data in tables["residual_vector"])
    verdict_by_id = {row_data["id"]: row_data for row_data in tables["compatibility_verdict"]}
    contract_target_only = verdict_by_id["VER1985_0_internal_viability"]["answer"] == "CONDITIONALLY_YES_BUT_NOT_CURRENTLY_DERIVED"
    current_not_closed = verdict_by_id["VER1985_1_current_status"]["answer"] == "NO"
    gates_blocked = all(row_data["status"] == "BLOCKED" for row_data in tables["claim_gate"])
    next_selected = tables["next"][0]["target_doc"] == "1986-Y5-R2FR-memory-route-finite-residual-vector-pack.md"
    pycache_path = ROOT / "scripts" / "__pycache__"
    formalization_count = formalization_1985_artifact_count()
    specs = [
        ("VAL1985_00_sources", sources_ok, "all source paths exist and needles found"),
        ("VAL1985_01_gates_retained", failures_retained, "open/failed consistency gates retained as residuals"),
        ("VAL1985_02_residual_vector", residuals_missing, "residual vector rows remain missing/source-bound"),
        ("VAL1985_03_contract_target_only", contract_target_only, "contract remains target only, not derivation"),
        ("VAL1985_04_current_not_closed", current_not_closed, "current corpus does not close gates"),
        ("VAL1985_05_claim_gates", gates_blocked, "all claim gates blocked"),
        (
            "VAL1985_06_decision",
            tables["decision"][-1]["decision"] == "MEMORY_ROUTE_RESIDUAL_VECTOR_PACK",
            "decision selects residual vector pack",
        ),
        ("VAL1985_07_next_target", next_selected, "1986 target selected"),
        ("VAL1985_08_claim_flags_safe", all_claim_flags_false(tables), "claim flags all false"),
        ("VAL1985_09_csv_parse", output_csvs_parse(), "all generated CSVs parse with rows"),
        ("VAL1985_10_pycache_absent", not pycache_path.exists(), "scripts __pycache__ absent"),
        ("VAL1985_11_formalization_untouched", formalization_count == 0, f"formalization_1985_artifact_count={formalization_count}"),
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
            "validation_id": "VAL1985_OVERALL",
            "status": "PASS" if all(row_data["status"] == "PASS" for row_data in rows) else "FAIL",
            "detail": "1985 minimal signature source-boundary consistency gate",
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
    for item in rows:
        values = [item.get(header, "").replace("|", "\\|").replace("\n", "<br>") for header in headers]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def write_markdown(tables: dict[str, list[dict[str, str]]], validation_rows: list[dict[str, str]]) -> None:
    sections = [
        ("Source Register", tables["source_register"]),
        ("Source Boundary Consistency Matrix", tables["consistency_matrix"]),
        ("Retained Residual Vector", tables["residual_vector"]),
        ("Contract Compatibility Verdict", tables["compatibility_verdict"]),
        ("Claim Gate", tables["claim_gate"]),
        ("Decision Ledger", tables["decision"]),
        ("Next Target", tables["next"]),
        ("Project Status Snapshot", tables["snapshot"]),
        ("Validation", validation_rows),
    ]
    lines = [
        "# 1985 Y5 R2FR: Minimal Signature Source Boundary Consistency Gate",
        "",
        "Private checkpoint. This runs the constructed 1984 parent-memory signature contract through the gates that decide whether a healthy positive memory operator can actually support local GR/Newton rather than a sourced fifth-force/residual branch.",
        "",
        "Verdict: the constructed contract is internally coherent as a future target, but it is not currently derived and it does not pass the consistency gates. Source-zero, boundary/readout silence, action-weight exclusion, canonical-transfer audit, conservation, Newton source-normalization, and arena matching all remain open or failed. The honest next step is a finite residual vector pack, not a local-GR claim.",
        "",
        "No local-GR, Newton, EH, R10, PPN, clock, orbital, or public claim follows from 1985.",
        "",
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
    print(f"VAL1985_OVERALL={overall}")
    return 0 if overall == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
