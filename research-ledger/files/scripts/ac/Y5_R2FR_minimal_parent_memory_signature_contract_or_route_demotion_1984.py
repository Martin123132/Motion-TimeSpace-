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

DOC_PATH = ROOT / "1984-Y5-R2FR-minimal-parent-memory-signature-contract-or-route-demotion.md"
VALIDATION_PATH = MTS_RESIDUALS / "P8_Y5_BRR545_1984_VALIDATION.csv"

SOURCES = {
    "1983_doc": {
        "path": ROOT / "1983-Y5-R2FR-top-parent-action-candidate-review.md",
        "needles": ["NO_PROMOTION", "NEXT1983_0_primary"],
    },
    "1983_validation": {
        "path": MTS_RESIDUALS / "P8_Y5_BRR545_1983_VALIDATION.csv",
        "needles": ["VAL1983_OVERALL", "PASS"],
    },
    "1980_lemma": {
        "path": ROOT / "1980-Y5-R2FR-parent-memory-positivity-lemma-or-closure.md",
        "needles": ["LEM1980_3_Gm", "CONDITIONAL_THEOREM_COMPLETE"],
    },
    "1979_coercivity": {
        "path": ROOT / "1979-Y5-R2FR-M2-Z-domain-theorem-or-first-finite-row.md",
        "needles": ["THM1979_5_gap", "PRF1979_5_inverse"],
    },
    "1306_closure": {
        "path": ROOT / "1306-Y5-R10-RAB-Zm-parent-function-or-XB-domain-range.md",
        "needles": ["CONSTANT_CANONICAL_CLOSURE_ALLOWED_FOR_PRIVATE_SENSITIVITY_ONLY", "NO_PARENT_FUNCTION_FOUND_DEMOTE_TO_EXPLICIT_CLOSURE"],
    },
    "1384_canonical": {
        "path": MTS_RESIDUALS / "P8_Y5_R10_1384_CANONICALIZATION_DERIVATION_AUDIT.csv",
        "needles": ["CDA1384_8_verdict", "CANONICAL_GAP_COUPLING_PIVOT_SELECTED"],
    },
    "1592_parent_signature": {
        "path": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1592_PARENT_SIGNATURE_AUDIT.csv",
        "needles": ["PSA1592_7_verdict", "PARENT_SIGNATURE_NOT_CLOSED_CANONICAL_SOURCE_ACQUISITION_REQUIRED"],
    },
    "1042_nohair": {
        "path": MTS_RESIDUALS / "P8_Y5_R10_1042_NOHAIR_PREMISE_GATE.csv",
        "needles": ["NHP1042_6_verdict", "FAIL_CURRENT_CLAIM_NOHAIR_NOT_PARENT_SIGNED"],
    },
}

OUTPUTS = {
    "source_register": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1984_SOURCE_REGISTER.csv",
    "minimal_contract": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1984_MINIMAL_PARENT_SIGNATURE_CONTRACT.csv",
    "action_ansatz": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1984_MINIMAL_ACTION_ANSATZ.csv",
    "compatibility_gates": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1984_COMPATIBILITY_GATES.csv",
    "consequence_map": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1984_CONSEQUENCE_MAP.csv",
    "route_demotion": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1984_ROUTE_DEMOTION_LEDGER.csv",
    "claim_gate": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1984_CLAIM_GATE.csv",
    "decision": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1984_DECISION_LEDGER.csv",
    "next": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1984_NEXT_TARGET.csv",
    "snapshot": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1984_PROJECT_STATUS_SNAPSHOT.csv",
    "source_weight": SOURCE_WEIGHT_DOCS / "MINIMAL_PARENT_MEMORY_SIGNATURE_CONTRACT_1984_NONCLAIM.csv",
    "queue": RAB_QUEUE / "JR1984_SOURCE_BOUNDARY_CONSISTENCY_GATE_QUEUE.csv",
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
                    "id": f"SRC1984_{len(rows):02d}_{source_id}",
                    "source_id": source_id,
                    "source_path": str(path),
                    "required_needles": "; ".join(config["needles"]),
                    "exists": str(path.exists()).lower(),
                    "needle_status": "PASS" if not missing else "MISSING: " + "; ".join(missing),
                    "role": "inputs for minimal parent memory signature contract",
                }
            )
        )
    return rows


def build_tables() -> dict[str, list[dict[str, str]]]:
    minimal_contract = [
        row(
            {
                "id": "MPC1984_0_parent_field",
                "contract_clause": "parent memory field",
                "required_statement": "A memory coordinate m or canonical fluctuation phi is a parent variable varied before projection/readout, not a fitted local diagnostic.",
                "why_needed": "without parent field status, Z_m and V_R'' cannot be action-owned",
                "current_status": "CONTRACT_REQUIRED_NOT_SOURCE_SIGNED",
            }
        ),
        row(
            {
                "id": "MPC1984_1_kinetic_metric",
                "contract_clause": "positive memory kinetic metric",
                "required_statement": "The parent second variation supplies Z_m>=Z_min>0, or canonical units with positive field metric, with units and same-branch normalization fixed.",
                "why_needed": "gives ellipticity/no-ghost and the Z_min lambda_1 part of G_m",
                "current_status": "CONTRACT_REQUIRED_NOT_SOURCE_SIGNED",
            }
        ),
        row(
            {
                "id": "MPC1984_2_strict_gap",
                "contract_clause": "strict branch Hessian / canonical gap",
                "required_statement": "The selected local branch satisfies partial_m V_R=0 and V_R''>=M2_min>0, or equivalently mu_m^2>=mu_min^2>0, after zero-mode projection.",
                "why_needed": "turns extremum into a true local mass gap rather than a flat modulus",
                "current_status": "CONTRACT_REQUIRED_NOT_SOURCE_SIGNED",
            }
        ),
        row(
            {
                "id": "MPC1984_3_domain_projection",
                "contract_clause": "domain and zero-mode projection",
                "required_statement": "D_loc, boundary class, coframe, and zero-mode/quotient projection are fixed by the same parent branch.",
                "why_needed": "makes lambda_1(D_loc)>0 and prevents constant/gauge hair from collapsing G_m",
                "current_status": "CONTRACT_REQUIRED_NOT_SOURCE_SIGNED",
            }
        ),
        row(
            {
                "id": "MPC1984_4_source_boundary",
                "contract_clause": "source and boundary control",
                "required_statement": "J_m, matter coupling, readout, boundary flux, action weights, and hidden source channels vanish by theorem or receive finite no-cancellation bounds.",
                "why_needed": "positive operator alone does not silence a sourced scalar",
                "current_status": "CONTRACT_REQUIRED_NOT_SOURCE_SIGNED",
            }
        ),
        row(
            {
                "id": "MPC1984_5_arena_matching",
                "contract_clause": "same-parent arena matching",
                "required_statement": "The same Z_m/mu_m/source law is evaluated in local, cosmology, galaxy, and clock/orbital arenas without retuning per arena.",
                "why_needed": "prevents the field theory from becoming a patchwork coefficient quilt",
                "current_status": "CONTRACT_REQUIRED_NOT_SOURCE_SIGNED",
            }
        ),
        row(
            {
                "id": "MPC1984_6_bianchi_conservation",
                "contract_clause": "covariance and conservation",
                "required_statement": "The parent action is diffeomorphism-covariant or has an explicit open-system/bath extension whose total stress obeys the correct Ward/Bianchi identity.",
                "why_needed": "local GR/Newton recovery needs conservation, not just a static scalar operator",
                "current_status": "CONTRACT_REQUIRED_NOT_SOURCE_SIGNED",
            }
        ),
    ]

    action_ansatz = [
        row(
            {
                "id": "ANS1984_0_minimal_lagrangian",
                "object": "minimal same-parent memory block",
                "formula": "S_m = integral sqrt(-g)[-1/2 Z_m(X_B) g^{mu nu} partial_mu m partial_nu m - V_R(m;X_B) + J_m m] + S_boundary + S_bath_if_needed",
                "contract_status": "ANSATZ_ONLY_NOT_DERIVED",
                "claim_risk": "inserting this by hand signs the theorem only as closure, not as derivation",
            }
        ),
        row(
            {
                "id": "ANS1984_1_canonical_local_form",
                "object": "canonical local fluctuation",
                "formula": "m=m_L+eta, phi=sqrt(Z_0) eta, L_2=-1/2 (partial phi)^2 -1/2 mu_m^2 phi^2 + J_c phi + residual_XB/boundary/readout",
                "contract_status": "LOCAL_EXPANSION_READY_IF_Z0_POSITIVE",
                "claim_risk": "mu_m^2, J_c, residual_XB, and boundary terms remain sourced or theorem-bound inputs",
            }
        ),
        row(
            {
                "id": "ANS1984_2_coercivity_floor",
                "object": "1979/1980 bridge",
                "formula": "G_m = Z_min lambda_1(D_loc) + M2_min - Eta_H > 0",
                "contract_status": "THEOREM_BRIDGE_READY",
                "claim_risk": "all constants are contract clauses, not current source-backed values",
            }
        ),
    ]

    compatibility_gates = [
        row(
            {
                "id": "COMP1984_0_no_hidden_fifth_force",
                "gate": "source-free or bounded scalar force",
                "test": "If J_m or matter/readout coupling is nonzero, compute finite alpha/lambda/PPN residual before any local-GR claim.",
                "current_result": "OPEN",
                "failure_mode": "positive massive field becomes a fifth-force/residual branch rather than local GR",
            }
        ),
        row(
            {
                "id": "COMP1984_1_no_arena_retuning",
                "gate": "same coefficients across arenas",
                "test": "One parent law must determine local and cosmology/galaxy parameters before data splits.",
                "current_result": "OPEN",
                "failure_mode": "contract becomes post-hoc patchwork",
            }
        ),
        row(
            {
                "id": "COMP1984_2_no_canonical_hiding",
                "gate": "canonical normalization transfer audit",
                "test": "Setting Z_m=1 must explicitly transform V_R, J_m, source/test charges, alpha numerator, and PPN normalization.",
                "current_result": "OPEN",
                "failure_mode": "coupling is hidden in redefined variables",
            }
        ),
        row(
            {
                "id": "COMP1984_3_covariant_conservation",
                "gate": "Bianchi/conservation compatibility",
                "test": "Memory stress plus matter/bath/source terms must obey a same-parent Ward identity.",
                "current_result": "OPEN",
                "failure_mode": "local GR/Newton cannot be recovered even if scalar operator is healthy",
            }
        ),
        row(
            {
                "id": "COMP1984_4_empirical_pressure",
                "gate": "test-pillar compatibility",
                "test": "Any finite residual branch must be scoreable against R10/PPN/clocks/orbital/cosmology without prior-edge hiding.",
                "current_result": "OPEN",
                "failure_mode": "closure survives algebra but fails as competitive testable field theory",
            }
        ),
    ]

    consequence_map = [
        row(
            {
                "id": "CONS1984_0_if_all_clauses_signed",
                "condition": "MPC1984_0 through MPC1984_6 all parent-signed",
                "then": "1979/1980 local memory inverse bound becomes executable; V_R Schur contribution can be bounded; local-GR route can advance to source/boundary/Newton checks.",
                "claim_status": "STILL_NOT_FINAL_LOCAL_GR_UNTIL_DOWNSTREAM_GATES",
            }
        ),
        row(
            {
                "id": "CONS1984_1_if_signs_only",
                "condition": "Z_m and M2_min signed but source/boundary not signed",
                "then": "healthy massive memory scalar remains possible but may mediate finite local residuals.",
                "claim_status": "RETAINED_RESIDUAL_NOT_GR_PROOF",
            }
        ),
        row(
            {
                "id": "CONS1984_2_if_inserted",
                "condition": "contract is adopted without parent derivation",
                "then": "it is a closure/ansatz branch useful for private smoke tests only.",
                "claim_status": "CLOSURE_ONLY",
            }
        ),
    ]

    route_demotion = [
        row(
            {
                "id": "DEM1984_0_current_route",
                "route": "memory positivity local-GR route",
                "status": "DEMOTED_TO_CONSTRUCTED_CONTRACT_NOT_DERIVATION",
                "reason": "no current source signs the contract; 1984 writes the exact future requirement",
                "allowed_use": "private algebra, future source hunt, compatibility gate design",
                "forbidden_use": "local-GR/Newton/R10/PPN claim",
            }
        ),
        row(
            {
                "id": "DEM1984_1_retained_branch",
                "route": "finite memory residual",
                "status": "RETAINED",
                "reason": "if source/boundary/coupling are nonzero, they must be scored as finite residuals",
                "allowed_use": "nonclaim alpha/lambda/PPN/cosmology pressure rows",
                "forbidden_use": "silencing by notation",
            }
        ),
    ]

    claim_gate = [
        row(
            {
                "id": "GATE1984_0_contract_derivation",
                "gate": "minimal contract is parent-derived",
                "status": "BLOCKED",
                "reason": "contract is constructed as a requirement, not found/signed by source",
                "required_to_open": "source-backed parent action or derivation satisfying MPC1984_0..6",
            }
        ),
        row(
            {
                "id": "GATE1984_1_local_GR",
                "gate": "derived local GR/Newton",
                "status": "BLOCKED",
                "reason": "source/boundary/conservation/Newton gates remain open after the contract",
                "required_to_open": "1985 compatibility gates plus parent signature source",
            }
        ),
    ]

    decision = [
        row(
            {
                "id": "DEC1984_0_contract_written",
                "decision": "MINIMAL_PARENT_SIGNATURE_CONTRACT_WRITTEN",
                "because": "all needed signs and branch controls are now one explicit same-parent checklist",
                "next_action": "test source/boundary/conservation compatibility rather than rescan for Z_m",
            }
        ),
        row(
            {
                "id": "DEC1984_1_route_demoted",
                "decision": "NOT_A_DERIVATION_YET",
                "because": "the contract is not source-backed; it is a constructed requirement",
                "next_action": "treat as closure/ansatz unless future source signs it",
            }
        ),
        row(
            {
                "id": "DEC1984_2_best_next",
                "decision": "SOURCE_BOUNDARY_CONSISTENCY_GATE",
                "because": "even a signed positive operator would fail local GR if it is sourced, boundary-active, nonconserved, or arena-retuned",
                "next_action": "1985-Y5-R2FR-minimal-signature-source-boundary-consistency-gate.md",
            }
        ),
    ]

    next_rows = [
        row(
            {
                "id": "NEXT1984_0_primary",
                "status": "selected",
                "target_doc": "1985-Y5-R2FR-minimal-signature-source-boundary-consistency-gate.md",
                "target_script": "scripts/Y5_R2FR_minimal_signature_source_boundary_consistency_gate_1985.py",
                "task": "run the minimal contract through source, boundary, canonical-transfer, conservation, arena-matching, and empirical-residual gates.",
                "success_condition": "decide whether the constructed contract is internally viable as a future derivation target or must be demoted to phenomenological residual scaffolding",
            }
        )
    ]

    snapshot = [
        row(
            {
                "id": "SNAP1984_0_progress",
                "area": "constructive leap",
                "status": "CONTRACT_WRITTEN",
                "summary": "The project now has the exact parent signature contract needed for memory positivity, instead of an undefined coupling gap.",
            }
        ),
        row(
            {
                "id": "SNAP1984_1_claim",
                "area": "claim status",
                "status": "NO_CLAIM",
                "summary": "The contract is not yet a derivation; it is a falsifiable requirement list and ansatz scaffold.",
            }
        ),
    ]

    source_weight = [
        row(
            {
                "id": "SW1984_0",
                "doc": DOC_PATH.name,
                "weight": "private_nonclaim_constructed_contract",
                "claim_safety": "contract explicitly marked ansatz/requirement; claim gates blocked",
                "use": "future parent action construction and compatibility gating",
            }
        )
    ]

    queue = [
        row(
            {
                "id": "Q1984_0_source_boundary_gate",
                "quantity": "source/boundary/conservation compatibility of minimal contract",
                "priority": "highest",
                "why": "positive operator alone does not recover local GR",
                "target": "1985 consistency gate",
            }
        )
    ]

    return {
        "source_register": source_register_rows(),
        "minimal_contract": minimal_contract,
        "action_ansatz": action_ansatz,
        "compatibility_gates": compatibility_gates,
        "consequence_map": consequence_map,
        "route_demotion": route_demotion,
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


def formalization_1984_artifact_count() -> int:
    if not FORMALIZATION.exists():
        return 0
    return len([path for path in FORMALIZATION.rglob("*1984*") if path.is_file()])


def validate(tables: dict[str, list[dict[str, str]]]) -> list[dict[str, str]]:
    sources_ok = all(row_data["exists"] == "true" and row_data["needle_status"] == "PASS" for row_data in tables["source_register"])
    contract_complete = len(tables["minimal_contract"]) == 7
    ansatz_only = tables["action_ansatz"][0]["contract_status"] == "ANSATZ_ONLY_NOT_DERIVED"
    demoted = tables["route_demotion"][0]["status"] == "DEMOTED_TO_CONSTRUCTED_CONTRACT_NOT_DERIVATION"
    gates_blocked = all(row_data["status"] == "BLOCKED" for row_data in tables["claim_gate"])
    next_selected = tables["next"][0]["target_doc"] == "1985-Y5-R2FR-minimal-signature-source-boundary-consistency-gate.md"
    pycache_path = ROOT / "scripts" / "__pycache__"
    formalization_count = formalization_1984_artifact_count()
    specs = [
        ("VAL1984_00_sources", sources_ok, "all source paths exist and needles found"),
        ("VAL1984_01_contract_complete", contract_complete, "seven-clause minimal parent signature contract written"),
        ("VAL1984_02_ansatz_not_derivation", ansatz_only, "minimal action is explicitly ansatz-only"),
        ("VAL1984_03_route_demoted", demoted, "current route demoted to constructed contract not derivation"),
        ("VAL1984_04_claim_gates", gates_blocked, "all claim gates remain blocked"),
        (
            "VAL1984_05_decision",
            tables["decision"][-1]["decision"] == "SOURCE_BOUNDARY_CONSISTENCY_GATE",
            "decision selects source/boundary consistency gate",
        ),
        ("VAL1984_06_next_target", next_selected, "1985 target selected"),
        ("VAL1984_07_claim_flags_safe", all_claim_flags_false(tables), "claim flags all false"),
        ("VAL1984_08_csv_parse", output_csvs_parse(), "all generated CSVs parse with rows"),
        ("VAL1984_09_pycache_absent", not pycache_path.exists(), "scripts __pycache__ absent"),
        ("VAL1984_10_formalization_untouched", formalization_count == 0, f"formalization_1984_artifact_count={formalization_count}"),
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
            "validation_id": "VAL1984_OVERALL",
            "status": "PASS" if all(row_data["status"] == "PASS" for row_data in rows) else "FAIL",
            "detail": "1984 minimal parent memory signature contract or route demotion",
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
        ("Minimal Parent Signature Contract", tables["minimal_contract"]),
        ("Minimal Action Ansatz", tables["action_ansatz"]),
        ("Compatibility Gates", tables["compatibility_gates"]),
        ("Consequence Map", tables["consequence_map"]),
        ("Route Demotion Ledger", tables["route_demotion"]),
        ("Claim Gate", tables["claim_gate"]),
        ("Decision Ledger", tables["decision"]),
        ("Next Target", tables["next"]),
        ("Project Status Snapshot", tables["snapshot"]),
        ("Validation", validation_rows),
    ]
    lines = [
        "# 1984 Y5 R2FR: Minimal Parent Memory Signature Contract Or Route Demotion",
        "",
        "Private checkpoint. Since 1983 found no existing parent-signature source, this constructs the exact same-parent contract a future MTS parent action must satisfy to make the 1979/1980 memory-positivity theorem a derivation.",
        "",
        "Verdict: the minimal parent memory signature contract is now explicit, but it is not a derivation. The route is demoted to a constructed contract / closure target unless a future source signs the clauses. This is still useful: it turns the coupling gap into falsifiable clauses for field status, kinetic sign, strict gap, domain, source/boundary control, arena matching, and covariance/conservation.",
        "",
        "No local-GR, Newton, EH, R10, PPN, clock, orbital, or public claim follows from 1984.",
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
    print(f"VAL1984_OVERALL={overall}")
    return 0 if overall == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
