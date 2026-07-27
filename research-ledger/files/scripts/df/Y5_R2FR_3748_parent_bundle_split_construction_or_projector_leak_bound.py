from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work")
REPO = ROOT.parent
FORMALIZATION = REPO / "formalization-workbench"
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
CHECKPOINT_ID = "3748"
BRANCH_ID = "MTS_R2FR_Y5_PARENT_BUNDLE_SPLIT_OR_PROJECTOR_LEAK_BOUND_3748"
DOC = ROOT / "3748-Y5-R2FR-parent-bundle-split-construction-or-projector-leak-bound.md"

DOC_3747 = ROOT / "3747-Y5-R2FR-projector-fixedness-commutator-zero-or-bound.md"
DOC_1351 = ROOT / "1351-Y5-R10-RAB-Gamma-Khat-Ploc-owner-bundle-or-q_loc-bound-row-fill.md"
DOC_2109 = ROOT / "2109-Y5-R2FR-extra-sector-natural-bundle-lift-or-finite-DqZ-tail-row.md"
DOC_2680 = ROOT / "2680-Y5-R2FR-parent-line-bundle-Hom-exclusion-or-ordinary-subaction-descent.md"
THEOREM_3747 = RESIDUALS / "P8_Y5_R2FR_3747_PARALLEL_PROJECTOR_ZERO_THEOREM.csv"
BOUNDS_3747 = RESIDUALS / "P8_Y5_R2FR_3747_PROJECTOR_LEAK_BOUND_ROWS.csv"
COMM_1654 = RESIDUALS / "P8_Y5_PARENT_QLOC_1654_PROJECTOR_COMMUTATOR_DERIVATION.csv"
BOUND_550 = RESIDUALS / "P8_Y5_BRR545_COMMUTATOR_PROJECTOR_BOUND_FILL_ROW.csv"
LIFT_2109 = RESIDUALS / "P8_Y5_PARENT_QLOC_2109_DOMAIN_PROJECTOR_LIFT_TEST.csv"
SPLIT_2246 = RESIDUALS / "P8_Y5_PARENT_QLOC_2246_REFERENCE_PROJECTOR_SPLIT.csv"
SPLIT_2294 = RESIDUALS / "P8_Y5_PARENT_QLOC_2294_REFERENCE_PROJECTOR_SPLIT.csv"
VALIDATION_3747 = RESIDUALS / "P8_Y5_BRR545_3747_VALIDATION.csv"
RED_TEAM = FORMALIZATION / "06-consistency-red-team.md"
SPINE = FORMALIZATION / "07-unification-spine.md"


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def base(timestamp: str) -> dict[str, object]:
    return {
        "timestamp_utc": timestamp,
        "branch_id": BRANCH_ID,
        "checkpoint_id": CHECKPOINT_ID,
        "valid_for_claim": False,
    }


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8", errors="replace")


def read_lines(path: Path) -> list[str]:
    return read_text(path).splitlines()


def parse_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def find_line(path: Path, needle: str) -> tuple[int, str]:
    for line_number, line in enumerate(read_lines(path), start=1):
        if needle in line:
            return line_number, line.strip()
    return 0, ""


def source_register(timestamp: str) -> list[dict[str, object]]:
    specs = [
        ("doc_3747_status", DOC_3747, "PARALLEL_PROJECTOR_ZERO_THEOREM_CONDITIONAL_SWITCH_ROUTE_BLOCKED", "3747 handoff status"),
        ("doc_3747_zero", DOC_3747, "R_deltaP=R_comm=0", "parallel-projector conditional zero"),
        ("theorem_3747", THEOREM_3747, "ZT3747_5_result", "machine-readable conditional zero"),
        ("bounds_3747", BOUNDS_3747, "epsilon_proj_leak", "projector leak bound slot"),
        ("doc_1351_owner_bundle", DOC_1351, "P_loc owner", "older owner-bundle blocker"),
        ("doc_2109_natural_lift", DOC_2109, "natural parent-bundle objects", "older natural-lift branch"),
        ("doc_2680_line_bundle", DOC_2680, "ordinary subaction descends through q_obs", "ordinary matter descent / line bundle branch"),
        ("comm_1654_fermi_bound", COMM_1654, "C_Fermi L_D||Riemann||", "existing Fermi-domain projector drift bound"),
        ("comm_1654_parallel", COMM_1654, "parallel image/kernel split", "existing parallel split condition"),
        ("bound_550_projector", BOUND_550, "epsilon_projector_symplectic_abs", "existing commutator/projector fill row"),
        ("lift_2109_commutator", LIFT_2109, "[d,Pi_M]J_H=0 or bounded", "existing domain projector lift blocker"),
        ("split_2246_guard", SPLIT_2246, "RPS2246_3_no_double_count", "reference projector split no-cancellation guard"),
        ("split_2294_guard", SPLIT_2294, "RPS2294_3_no_double_count", "reference projector split no-cancellation guard"),
        ("validation_3747", VALIDATION_3747, "next_target_3748", "3747 validation handoff"),
        ("redteam_switch", RED_TEAM, "P_loc, P_gal, and P_cos could become arbitrary sector switches.", "anti-switch warning"),
        ("spine_kernel", SPINE, "metric-response kernel theorem", "spine fallback route"),
    ]
    rows: list[dict[str, object]] = []
    for source_id, path, needle, role in specs:
        exists = path.exists()
        text = read_text(path) if exists else ""
        line_number, line_text = find_line(path, needle) if exists else (0, "")
        rows.append({
            **base(timestamp),
            "source_id": source_id,
            "path": str(path),
            "exists": exists,
            "needle": needle,
            "needle_found": needle in text,
            "line_number": line_number,
            "line_text": line_text,
            "role": role,
            "claim_allowed": False,
        })
    return rows


def corpus_evidence_rows(timestamp: str) -> list[dict[str, object]]:
    specs = [
        ("EVD3748_0_owner_bundle", "1351 owner bundle", "requires P_loc owner, action existence, Khat metric response, boundary/source closure", "OWNER_BUNDLE_NOT_CLOSED", "does not sign the parent split"),
        ("EVD3748_1_commutator_identity", "1654 commutator derivation", "nabla(P_loc K)=P_loc nabla K+(nabla P_loc)K", "IDENTITY_AND_BOUND_ROUTE_AVAILABLE", "supports bound route for R_comm"),
        ("EVD3748_2_parallel_condition", "1654 parallel split", "P^2=P implies derivative leakage off-diagonal; zero requires parallel image/kernel split", "CONDITION_MATCHES_3747", "supports exact route but not sourced as parent geometry"),
        ("EVD3748_3_fermi_bound", "1654 finite-domain bound", "||nabla P_loc|| <= C_Fermi L_D||Riemann|| + C_Fermi2 L_D^2||nabla Riemann||", "BOUND_FORMULA_AVAILABLE", "first concrete leakage bound formula"),
        ("EVD3748_4_domain_lift", "2109 natural lift", "Pi_M origin and commutator remain not parent-derived", "FAIL_CURRENT_CLAIM", "confirms no hidden pass"),
        ("EVD3748_5_reference_split", "2246/2294 reference splits", "bulk/edge split has no-cancellation policy but lacks orthogonality proof", "GUARD_ONLY", "helps prevent cancellation cheating"),
        ("EVD3748_6_line_bundle", "2680 line bundle/descent", "ordinary subaction descent exists as conditional route but remains unsigned", "CONDITIONAL_UNSIGNED", "useful for later R_matter_M, not enough for projector zero"),
    ]
    return [
        {
            **base(timestamp),
            "evidence_id": evidence_id,
            "source_family": source_family,
            "content": content,
            "status": status,
            "use_in_3748": use_in_3748,
            "claim_allowed": False,
        }
        for evidence_id, source_family, content, status, use_in_3748 in specs
    ]


def bundle_split_attempt_rows(timestamp: str) -> list[dict[str, object]]:
    specs = [
        ("BSA3748_0_total_bundle", "E = E_L direct-sum E_M", "local metric/source response sector plus morphology/memory sector", "CONSTRUCTIBLE_AS_ANSATZ", "not parent-signed in corpus"),
        ("BSA3748_1_projectors", "P_L(phi_L,phi_M)=(phi_L,0), P_M(phi_L,phi_M)=(0,phi_M)", "canonical projectors for the direct-sum ansatz", "ALGEBRAICALLY_VALID", "requires physical identification of E_L/E_M"),
        ("BSA3748_2_connection_matrix", "nabla_E = [[nabla_L, Omega_LM],[Omega_ML,nabla_M]]", "off-diagonal connection blocks measure projector leakage", "DERIVED_TEST_OBJECT", "Omega_LM/Omega_ML not sourced"),
        ("BSA3748_3_parallel_condition", "Omega_LM=Omega_ML=0", "connection preserves E_L and E_M, giving nabla P_M=0", "ZERO_ROUTE_CONDITION", "not parent-signed"),
        ("BSA3748_4_field_dependent_basis", "P_M = U(Phi) P_M0 U(Phi)^-1", "generic marker/transition projector as moving split", "COUNTERMODEL_ACTIVE", "deltaP and commutator generally nonzero"),
        ("BSA3748_5_verdict", "parent bundle split", "mathematically clean ansatz exists, but corpus does not source its parent origin", "ANSATZ_READY_NOT_PROOF", "use bound rows until parent split is signed"),
    ]
    return [
        {
            **base(timestamp),
            "attempt_id": attempt_id,
            "object": obj,
            "formula_or_definition": formula,
            "status": status,
            "blocker_or_use": blocker,
            "claim_allowed": False,
        }
        for attempt_id, obj, formula, status, blocker in specs
    ]


def matrix_identity_rows(timestamp: str) -> list[dict[str, object]]:
    specs = [
        ("MAT3748_0_projector_matrices", "P_L=[[I,0],[0,0]], P_M=[[0,0],[0,I]]", "canonical direct-sum projectors", "P_L^2=P_L; P_M^2=P_M; P_L P_M=0"),
        ("MAT3748_1_connection_blocks", "A_E=[[A_LL,A_LM],[A_ML,A_MM]]", "connection one-form in the split frame", "off-diagonal blocks are the obstruction"),
        ("MAT3748_2_commutator", "[nabla,P_M]=[A_E,P_M]=[[0,A_LM],[-A_ML,0]]", "commutator identity in split frame", "zero iff A_LM=A_ML=0"),
        ("MAT3748_3_local_action", "[nabla,P_M]P_L deltaPhi = (0,-A_ML deltaPhi_L)", "local variation leakage into morphology sector", "R_comm controlled by ||A_ML||"),
        ("MAT3748_4_moving_basis_delta", "delta P_M=[delta U U^-1,P_M]", "field-dependent projector variation", "||deltaP_M|| <= 2||deltaU U^-1|| for orthogonal P_M"),
        ("MAT3748_5_moving_basis_comm", "nabla P_M=[(nabla U)U^-1,P_M]", "transition/marker projector drift", "||nabla P_M|| <= 2||(nabla U)U^-1||"),
    ]
    return [
        {
            **base(timestamp),
            "identity_id": identity_id,
            "identity": identity,
            "meaning": meaning,
            "consequence": consequence,
            "claim_allowed": False,
        }
        for identity_id, identity, meaning, consequence in specs
    ]


def leak_bound_rows(timestamp: str) -> list[dict[str, object]]:
    specs = [
        (
            "LB3748_0_epsilon_comm_matrix",
            "epsilon_comm_matrix",
            "C_pair * ||E_M^nabla||_D * ||A_ML||_D * ||deltaPhi_L||_D",
            "dimensionless_after_normalization",
            "from [nabla,P_M]P_L deltaPhi=(0,-A_ML deltaPhi_L)",
            "BOUND_FORMULA_READY_VALUES_MISSING",
        ),
        (
            "LB3748_1_epsilon_deltaP_matrix",
            "epsilon_deltaP_matrix",
            "C_pair * ||E_M||_D * ||Phi_S||_D * ||deltaU U^-1||_D",
            "dimensionless_after_normalization",
            "from deltaP_M=[deltaU U^-1,P_M]",
            "BOUND_FORMULA_READY_VALUES_MISSING",
        ),
        (
            "LB3748_2_fermi_projector_drift",
            "epsilon_comm_Fermi",
            "C_pair * ||E_M^nabla||_D * (C_Fermi L_D||Riemann||_D + C_Fermi2 L_D^2||nabla Riemann||_D) * ||deltaPhi_L||_D",
            "dimensionless_after_normalization",
            "imports 1654 finite-domain P_loc drift bound",
            "SOURCE_BACKED_FORMULA_VALUES_MISSING",
        ),
        (
            "LB3748_3_transition_projector_drift",
            "epsilon_comm_transition",
            "C_pair * ||E_M^nabla||_D * ||deltaPhi_L||_D / ell_transition",
            "dimensionless_after_normalization",
            "rough transition-width version when P_M changes over ell_transition",
            "SCHEMA_ONLY_VALUES_MISSING",
        ),
        (
            "LB3748_4_no_cancellation_total",
            "epsilon_proj_leak_abs",
            "abs(epsilon_deltaP_matrix)+abs(epsilon_comm_matrix)+abs(epsilon_comm_Fermi)+abs(epsilon_comm_transition)",
            "dimensionless_after_normalization",
            "absolute-tail policy from 2246/2294; no cancellation credit",
            "BOUND_INTERFACE_READY_VALUES_MISSING",
        ),
        (
            "LB3748_5_ppn_gate",
            "S_eff_3748",
            "S_eff_3746 + epsilon_proj_leak_abs",
            "dimensionless_after_normalization",
            "feeds |gamma-1|, |beta-1|, Newton residual gates from 3744/3746",
            "NONCLAIM_UNTIL_ALL_VALUES_SOURCED",
        ),
    ]
    return [
        {
            **base(timestamp),
            "bound_id": bound_id,
            "quantity": quantity,
            "formula": formula,
            "units": units,
            "derivation_source": derivation_source,
            "status": status,
            "claim_allowed": False,
        }
        for bound_id, quantity, formula, units, derivation_source, status in specs
    ]


def decision_rows(timestamp: str) -> list[dict[str, object]]:
    specs = [
        ("DEC3748_0_construction", "DIRECT_SUM_ANSATZ_CONSTRUCTED", "A clean mathematical parent split can be written, but it is an ansatz until sourced from MTS parent variables."),
        ("DEC3748_1_derivation", "PARALLEL_CONNECTION_IS_THE_EXACT_ZERO_CONDITION", "The off-diagonal connection blocks A_LM/A_ML are the precise obstruction to R_comm=0."),
        ("DEC3748_2_bound_progress", "FERMI_DOMAIN_BOUND_IMPORTED", "The older 1654 bound gives a real formula route for projector drift instead of handwaving."),
        ("DEC3748_3_current_status", "LOCAL_CLAIM_STILL_BLOCKED", "No numeric/source-owned values for A_ML, L_D, curvature norms, or operator constants exist here."),
        ("DEC3748_4_next", "FILL_LOCAL_FERMI_DOMAIN_NUMERIC_SCALES", "The next best move is to instantiate L_D, Solar-system curvature scale, and operator-normalization placeholders as nonclaim numeric smoke rows."),
    ]
    return [
        {
            **base(timestamp),
            "decision_id": decision_id,
            "decision": decision,
            "rationale": rationale,
            "claim_allowed": False,
        }
        for decision_id, decision, rationale in specs
    ]


def claim_gate_rows(timestamp: str) -> list[dict[str, object]]:
    specs = [
        ("CG3748_0_sources", "3748 source sweep complete", True, "all registered source paths and needles found"),
        ("CG3748_1_split_ansatz", "direct-sum parent split ansatz written", True, "E=E_L direct-sum E_M and canonical projectors emitted"),
        ("CG3748_2_parallel_condition", "parallel connection zero condition derived", True, "off-diagonal connection blocks are exact obstruction"),
        ("CG3748_3_parent_signed", "split and parallel connection parent-signed", False, "not sourced by current corpus"),
        ("CG3748_4_bound_formula", "epsilon_deltaP/epsilon_comm bound formulas emitted", True, "matrix and Fermi-domain bound formulas written"),
        ("CG3748_5_bound_values", "projector leak numeric/source values filled", False, "A_ML, L_D, curvature norms, and operator constants missing"),
        ("CG3748_6_local_claim", "local GR/Newton/PPN pass claim allowed", False, "zero route unsigned and bound values missing"),
    ]
    return [
        {
            **base(timestamp),
            "gate_id": gate_id,
            "gate": gate,
            "passed": passed,
            "rationale": rationale,
            "claim_allowed": False,
        }
        for gate_id, gate, passed, rationale in specs
    ]


def status_rows(timestamp: str) -> list[dict[str, object]]:
    return [{
        **base(timestamp),
        "status_id": "STATUS3748_0",
        "status": "BUNDLE_SPLIT_ANSATZ_AND_PROJECTOR_LEAK_BOUND_FORMULAS_READY_VALUES_MISSING",
        "summary": "3748 constructs the direct-sum parent split ansatz, derives the off-diagonal connection obstruction, imports the 1654 Fermi-domain projector drift bound, and leaves local claims blocked until parent signature or numeric/source values exist.",
        "claim_allowed": False,
    }]


def next_target_rows(timestamp: str) -> list[dict[str, object]]:
    return [{
        **base(timestamp),
        "next_id": "NEXT3748_0",
        "target_doc": "3749-Y5-R2FR-local-Fermi-domain-projector-leak-numeric-smoke.md",
        "target_script": "scripts/Y5_R2FR_3749_local_Fermi_domain_projector_leak_numeric_smoke.py",
        "objective": "instantiate nonclaim local Fermi-domain smoke rows for L_D, Solar-system curvature norms, and projector/operator constants to test whether epsilon_comm_Fermi could plausibly sit below PPN/Newton tolerances",
        "success_gate": "all numeric rows remain nonclaim but the bound runner can show pass/fail sensitivity without hiding missing parent inputs",
        "claim_allowed": False,
    }]


def write_doc(paths: dict[str, Path], grouped: dict[str, list[dict[str, object]]]) -> None:
    lines = [
        "# 3748 - Parent Bundle Split Construction or Projector Leak Bound",
        "",
        "## Status",
        "- `BUNDLE_SPLIT_ANSATZ_AND_PROJECTOR_LEAK_BOUND_FORMULAS_READY_VALUES_MISSING`",
        "- A clean `E = E_L direct-sum E_M` construction exists as mathematics, but not yet as a parent-signed MTS object.",
        "- The important progress is the bound path: projector leakage is now tied to off-diagonal connection blocks and the older Fermi-domain drift formula.",
        "",
        "## Corpus Evidence",
    ]
    for row in grouped["evidence"]:
        lines.append(f"- `{row['evidence_id']}` `{row['status']}`: {row['content']} | {row['use_in_3748']}")
    lines.extend(["", "## Bundle Split Attempt"])
    for row in grouped["split_attempt"]:
        lines.append(f"- `{row['attempt_id']}` `{row['status']}`: {row['object']} | {row['formula_or_definition']}")
    lines.extend(["", "## Matrix Identities"])
    for row in grouped["matrix"]:
        lines.append(f"- `{row['identity_id']}`: {row['identity']} | {row['consequence']}")
    lines.extend(["", "## Projector Leak Bounds"])
    for row in grouped["bounds"]:
        lines.append(f"- `{row['bound_id']}` `{row['quantity']}` `{row['status']}`: {row['formula']}")
    lines.extend(["", "## Decisions"])
    for row in grouped["decisions"]:
        lines.append(f"- `{row['decision_id']}` `{row['decision']}` | {row['rationale']}")
    lines.extend(["", "## Claim Gates"])
    for row in grouped["claim_gates"]:
        lines.append(f"- `{row['gate_id']}` passed={row['passed']} claim_allowed={row['claim_allowed']} | {row['gate']}: {row['rationale']}")
    lines.extend(["", "## Next Target"])
    next_row = grouped["next_target"][0]
    lines.append(f"- `{next_row['target_doc']}`")
    lines.append(f"- Objective: {next_row['objective']}")
    paths["doc"].write_text("\n".join(lines) + "\n", encoding="utf-8")


def validation_rows(timestamp: str, paths: dict[str, Path]) -> list[dict[str, object]]:
    sources = parse_csv(paths["source_register"])
    evidence = parse_csv(paths["evidence"])
    split_attempt = parse_csv(paths["split_attempt"])
    matrix = parse_csv(paths["matrix"])
    bounds = parse_csv(paths["bounds"])
    claim_gates = parse_csv(paths["claim_gates"])
    next_target = parse_csv(paths["next_target"])
    validation_paths = [path for key, path in paths.items() if key != "validation"]
    formalization_leaks = []
    if FORMALIZATION.exists():
        formalization_leaks = list(FORMALIZATION.rglob("*3748*"))
    checks = [
        ("sources_exist", "all source paths exist", all(row["exists"] == "True" for row in sources)),
        ("needles_found", "all source needles found", all(row["needle_found"] == "True" for row in sources)),
        ("outputs_exist", "all outputs exist", all(path.exists() for path in validation_paths)),
        ("csv_parse", "all generated CSVs parse", all(len(parse_csv(path)) > 0 for key, path in paths.items() if key not in {"doc", "validation"})),
        ("evidence_complete", "corpus evidence rows include 1351/1654/2109/2246/2680", len(evidence) == 7 and all(token in read_text(paths["evidence"]) for token in ["1351", "1654", "2109", "2680"])),
        ("split_attempt", "direct-sum split ansatz and connection matrix emitted", len(split_attempt) == 6 and all(token in read_text(paths["split_attempt"]) for token in ["E = E_L direct-sum E_M", "Omega_LM=Omega_ML=0"])),
        ("matrix_identity", "off-diagonal connection obstruction derived", len(matrix) == 6 and all(token in read_text(paths["matrix"]) for token in ["[A_E,P_M]", "A_ML", "delta U U^-1"])),
        ("bound_formulas", "projector leak bound formulas emitted", len(bounds) == 6 and all(token in read_text(paths["bounds"]) for token in ["epsilon_comm_Fermi", "C_Fermi L_D||Riemann||", "epsilon_proj_leak_abs"])),
        ("claim_gates_block", "local claim gate remains blocked", any(row["gate_id"] == "CG3748_6_local_claim" and row["passed"] == "False" for row in claim_gates)),
        ("claim_allowed_false", "all gate rows keep claim_allowed false", all(row["claim_allowed"] == "False" for row in claim_gates)),
        ("doc_core_terms", "doc records ansatz and bound path", all(token in read_text(paths["doc"]) for token in ["off-diagonal connection", "Fermi-domain drift", "Projector Leak Bounds"])),
        ("next_target_3749", "next target is local Fermi-domain numeric smoke", next_target[0]["target_doc"] == "3749-Y5-R2FR-local-Fermi-domain-projector-leak-numeric-smoke.md"),
        ("no_formalization_leak", "no 3748 files in formalization-workbench", len(formalization_leaks) == 0),
    ]
    return [
        {
            **base(timestamp),
            "validation_id": validation_id,
            "description": description,
            "result": "PASS" if result else "FAIL",
            "details": "",
        }
        for validation_id, description, result in checks
    ]


def main() -> None:
    timestamp = stamp()
    paths = {
        "source_register": RESIDUALS / "P8_Y5_R2FR_3748_SOURCE_REGISTER.csv",
        "evidence": RESIDUALS / "P8_Y5_R2FR_3748_CORPUS_EVIDENCE_ROWS.csv",
        "split_attempt": RESIDUALS / "P8_Y5_R2FR_3748_BUNDLE_SPLIT_ATTEMPT.csv",
        "matrix": RESIDUALS / "P8_Y5_R2FR_3748_PROJECTOR_MATRIX_IDENTITIES.csv",
        "bounds": RESIDUALS / "P8_Y5_R2FR_3748_PROJECTOR_LEAK_BOUND_FORMULAS.csv",
        "claim_gates": RESIDUALS / "P8_Y5_R2FR_3748_CLAIM_GATES.csv",
        "decisions": RESIDUALS / "P8_Y5_R2FR_3748_DECISION_ROWS.csv",
        "status": RESIDUALS / "P8_Y5_R2FR_3748_STATUS.csv",
        "next_target": RESIDUALS / "P8_Y5_R2FR_3748_NEXT_TARGET.csv",
        "validation": RESIDUALS / "P8_Y5_BRR545_3748_VALIDATION.csv",
        "doc": DOC,
    }
    grouped = {
        "source_register": source_register(timestamp),
        "evidence": corpus_evidence_rows(timestamp),
        "split_attempt": bundle_split_attempt_rows(timestamp),
        "matrix": matrix_identity_rows(timestamp),
        "bounds": leak_bound_rows(timestamp),
        "claim_gates": claim_gate_rows(timestamp),
        "decisions": decision_rows(timestamp),
        "status": status_rows(timestamp),
        "next_target": next_target_rows(timestamp),
    }
    for key, rows in grouped.items():
        write_csv(paths[key], rows)
    write_doc(paths, grouped)
    write_csv(paths["validation"], validation_rows(timestamp, paths))
    failures = [row for row in parse_csv(paths["validation"]) if row["result"] != "PASS"]
    if failures:
        raise SystemExit(f"3748 validation failed: {failures}")
    print("wrote 3748 checkpoint: bundle split ansatz built; projector leak bound formulas ready")


if __name__ == "__main__":
    main()
