from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = ROOT.parent
FORMALIZATION = PROJECT_ROOT / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
MICROSCOPE = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
BETA_DOCS = ROOT / "source-intake" / "beta-source" / "docs"

BRANCH_ID = "MTS_R2FR_NO_PHYSICAL_Q_POLE_OR_BOUNDED_BETA_RUNNER_2292"
START_TS = datetime.now(timezone.utc).timestamp()
DOC = ROOT / "2292-Y5-R2FR-no-physical-q-pole-theorem-or-bounded-beta-runner.md"


SOURCES: list[dict[str, Any]] = [
    {
        "source_id": "SRC2292_00_2291_doc",
        "source_key": "2291_handoff",
        "source_path": ROOT / "2291-Y5-R2FR-parent-finite-quadratic-row-and-source-test-beta-split.md",
        "needles": ["least-scrutiny route remains structural", "no physical local `q/R_AB` pole", "2292-Y5-R2FR"],
        "role": "current finite-q row handoff",
    },
    {
        "source_id": "SRC2292_01_2291_validation",
        "source_key": "2291_validation",
        "source_path": OUT / "P8_Y5_BRR545_2291_VALIDATION.csv",
        "needles": ["VAL2291_OVERALL", "PASS"],
        "role": "confirms 2291 passed before 2292",
    },
    {
        "source_id": "SRC2292_02_2291_next",
        "source_key": "2291_next",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_2291_NEXT_TARGET.csv",
        "needles": ["2292-Y5-R2FR-no-physical-q-pole-theorem-or-bounded-beta-runner.md", "bounded beta_source/beta_test", "no-cancellation tails"],
        "role": "declares 2292 objective",
    },
    {
        "source_id": "SRC2292_03_2291_branch",
        "source_key": "2291_branch_classification",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_2291_BRANCH_CLASSIFICATION.csv",
        "needles": ["BR2291_0_no_physical_q_pole", "BR2291_2_sourced_finite_exchange", "SCOREABLE_STRUCTURE_BUT_INPUTS_MISSING"],
        "role": "current no-pole/finite branch fork",
    },
    {
        "source_id": "SRC2292_04_2244_doc",
        "source_key": "2244_prior_no_pole",
        "source_path": ROOT / "2244-Y5-R2FR-RAB-no-physical-pole-theorem-or-bounded-beta-runner.md",
        "needles": ["finite local `R_AB` residual has no physical exchange pole", "linear `c_g` route remains quarantined", "2245-Y5-R2FR"],
        "role": "prior same-fork no-pole/beta runner checkpoint",
    },
    {
        "source_id": "SRC2292_05_2244_validation",
        "source_key": "2244_validation",
        "source_path": OUT / "P8_Y5_BRR545_2244_VALIDATION.csv",
        "needles": ["VAL2244_OVERALL", "PASS"],
        "role": "confirms 2244 passed as nonclaim",
    },
    {
        "source_id": "SRC2292_06_2244_no_pole",
        "source_key": "2244_no_pole_audit",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_2244_NO_PHYSICAL_RAB_POLE_AUDIT.csv",
        "needles": ["NPR2244_2_constraint_generator", "MISSING_PARENT_OMEGA_DCR_VERTICAL_GENERATOR", "FAIL_CURRENT_CLAIM_NO_POLE_NOT_PROVED"],
        "role": "prior no-physical-pole audit",
    },
    {
        "source_id": "SRC2292_07_2244_omega",
        "source_key": "2244_omega_dcr",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_2244_OMEGA_DCR_CLOSURE_AUDIT.csv",
        "needles": ["ODR2244_0_parent_Omega", "ODR2244_8_verdict", "FAIL_CURRENT_CLAIM_NO_POLE_NOT_CLOSED"],
        "role": "prior Omega/DCR closure audit",
    },
    {
        "source_id": "SRC2292_08_2244_beta",
        "source_key": "2244_bounded_beta",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_2244_BOUNDED_BETA_SOURCE_TEST_TEMPLATE.csv",
        "needles": ["BB2244_0_beta_source_geom", "BB2244_7_beta_product_guard", "CLAIM_BLOCKED"],
        "role": "prior bounded beta source/test template",
    },
    {
        "source_id": "SRC2292_09_1037_no_pole",
        "source_key": "1037_no_pole",
        "source_path": OUT / "P8_Y5_R10_1037_NO_PHYSICAL_X_POLE_AUDIT.csv",
        "needles": ["NP1037_2_momentum_map", "MISSING_PARENT_OMEGA_DCX_VERTICAL_GENERATOR", "FAIL_CURRENT_CLAIM_NO_POLE_NOT_PROVED"],
        "role": "generic no-physical-X-pole audit",
    },
    {
        "source_id": "SRC2292_10_1038_omega",
        "source_key": "1038_omega_dcx",
        "source_path": OUT / "P8_Y5_R10_1038_OMEGA_DCX_CLOSURE_AUDIT.csv",
        "needles": ["ODC1038_0_parent_Omega", "ODC1038_8_verdict", "FAIL_CURRENT_CLAIM_NO_POLE_NOT_CLOSED"],
        "role": "generic Omega/DCX closure audit",
    },
    {
        "source_id": "SRC2292_11_1038_beta_acq",
        "source_key": "1038_beta_acquisition",
        "source_path": OUT / "P8_Y5_R10_1038_BETA_BOUND_SOURCE_ACQUISITION.csv",
        "needles": ["BBA1038_0_R10_beta_product", "BBA1038_7_score_gate", "CLAIM_BLOCKED_UNTIL_PARENT_PROJECTIONS_EXIST"],
        "role": "generic beta-bound source acquisition",
    },
    {
        "source_id": "SRC2292_12_1038_validation",
        "source_key": "1038_validation",
        "source_path": OUT / "P8_Y5_BRR545_1038_VALIDATION.csv",
        "needles": ["V1038_SUMMARY", "pass"],
        "role": "confirms 1038 closure/beta checkpoint passed",
    },
    {
        "source_id": "SRC2292_13_local_bounds",
        "source_key": "local_bounds",
        "source_path": ROOT / "source-intake" / "local_bounds" / "local_bound_claims.csv",
        "needles": ["R10", "PPN"],
        "role": "external local bound anchor ledger",
    },
]


OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_2292_SOURCE_REGISTER.csv",
    "no_pole_audit": OUT / "P8_Y5_PARENT_QLOC_2292_NO_PHYSICAL_Q_POLE_AUDIT.csv",
    "countermodels": OUT / "P8_Y5_PARENT_QLOC_2292_POLE_COUNTERMODEL_LEDGER.csv",
    "omega_dcq": OUT / "P8_Y5_PARENT_QLOC_2292_OMEGA_DCQ_CLOSURE_AUDIT.csv",
    "vertical_map": OUT / "P8_Y5_PARENT_QLOC_2292_VERTICAL_GENERATOR_FIELD_MAP.csv",
    "bounded_beta": OUT / "P8_Y5_PARENT_QLOC_2292_BOUNDED_BETA_SOURCE_TEST_TEMPLATE.csv",
    "tail_envelope": OUT / "P8_Y5_PARENT_QLOC_2292_ABSOLUTE_TAIL_ENVELOPE.csv",
    "arena_routing": OUT / "P8_Y5_PARENT_QLOC_2292_ARENA_ROUTING_MAP.csv",
    "alpha_template": OUT / "R10_alpha_lambda_curve_MTS_2292_NO_POLE_OR_BETA_TEMPLATE_NONCLAIM.csv",
    "runner_smoke": OUT / "P8_Y5_PARENT_QLOC_2292_RUNNER_SMOKE_STATUS.csv",
    "refusal": OUT / "P8_Y5_PARENT_QLOC_2292_PLACEHOLDER_REFUSAL_RUNNER.csv",
    "claim_gates": OUT / "P8_Y5_PARENT_QLOC_2292_CLAIM_GATES.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_2292_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_2292_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_PARENT_QLOC_2292_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2292_VALIDATION.csv",
}


COPY_TARGETS = {
    "queue_beta": (OUTPUTS["bounded_beta"], QUEUE / "JR2292_BOUNDED_BETA_SOURCE_TEST_TEMPLATE_NONCLAIM.csv"),
    "queue_nopole": (OUTPUTS["no_pole_audit"], QUEUE / "JR2292_NO_PHYSICAL_Q_POLE_AUDIT_NONCLAIM.csv"),
    "branch_wep": (OUTPUTS["bounded_beta"], MICROSCOPE / "no_physical_q_pole_or_beta_runner_nonclaim_2292.csv"),
    "beta_docs": (OUTPUTS["bounded_beta"], BETA_DOCS / "NO_PHYSICAL_Q_POLE_OR_BETA_RUNNER_2292_NONCLAIM.csv"),
}


def stringify(value: Any) -> str:
    if isinstance(value, bool):
        return "True" if value else "False"
    return str(value)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        for row in rows:
            writer.writerow({key: stringify(value) for key, value in row.items()})


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def csv_parses(path: Path) -> bool:
    try:
        read_csv(path)
        return True
    except Exception:
        return False


def validation_pass(path: Path) -> bool:
    if not path.exists() or not csv_parses(path):
        return False
    rows = read_csv(path)
    if not rows:
        return False
    id_key = "check_id" if "check_id" in rows[0] else "validation_id"
    result_key = "result" if "result" in rows[0] else "status"
    overall_rows = [row for row in rows if "overall" in row.get(id_key, "").lower() or "summary" in row.get(id_key, "").lower()]
    if overall_rows:
        return all(row.get(result_key, "").lower() == "pass" for row in overall_rows)
    return all(row.get(result_key, "").lower() == "pass" for row in rows)


def remove_pycache() -> None:
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def ignored_environment_path(path: Path) -> bool:
    ignored_parts = {".venv", ".venv-score", "__pycache__", "site-packages", ".git"}
    return any(part in ignored_parts for part in path.parts)


def formalization_has_2292_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    for candidate in FORMALIZATION.rglob("*2292*"):
        if candidate.is_file() and not ignored_environment_path(candidate.relative_to(FORMALIZATION)):
            return True
    return False


def formalization_touched_since_start() -> bool:
    if not FORMALIZATION.exists():
        return False
    for candidate in FORMALIZATION.rglob("*"):
        if candidate.is_file() and not ignored_environment_path(candidate.relative_to(FORMALIZATION)):
            if candidate.stat().st_mtime >= START_TS:
                return True
    return False


def table(headers: list[str], rows: list[dict[str, Any]]) -> str:
    def cell(value: Any) -> str:
        return stringify(value).replace("\n", " ").replace("|", "\\|")

    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(cell(row.get(header, "")) for header in headers) + " |")
    return "\n".join(lines)


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source in SOURCES:
        source_path = Path(source["source_path"])
        source_text = read_text(source_path)
        needles = source["needles"]
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "source_id": source["source_id"],
                "source_key": source["source_key"],
                "source_path": source_path,
                "exists": source_path.exists(),
                "needles": "; ".join(needles),
                "needles_present": all(needle in source_text for needle in needles),
                "role": source["role"],
                "valid_for_claim": False,
            }
        )
    return rows


def no_pole_audit_rows() -> list[dict[str, Any]]:
    entries = [
        ("NPQ2292_0_q_kernel", "vertical q is in the kernel of the parent quotient", "Dq[v_q]=0 and q is parent-defined before variation", "PARTIAL_MATH_ONLY_NOT_PARENT_SIGNED", "q can still be a physical residual rather than a representative choice"),
        ("NPQ2292_1_action_descent", "bulk action descends through q", "S_bulk[Phi]=S_red[q(Phi)] so H(v_q,.)=0 and no vertical Green operator exists", "CONDITIONAL_DESCENT_NOT_SIGNED", "a physical finite q Hessian block can survive"),
        ("NPQ2292_2_constraint_generator", "vertical q is generated by a first-class differentiable constraint", "delta G_q=Omega(delta Phi,v_q), G_q=int epsilon C_q+Q_q, and brackets close", "MISSING_PARENT_OMEGA_DCQ_VERTICAL_GENERATOR", "zero Hessian is not enough; second-class or edge remnants can remain"),
        ("NPQ2292_3_boundary_silence", "vertical transformations carry no local boundary charge", "Q_q=0/exact/proper and K_boundary=0 for compact local vertical transformations", "MISSING_BOUNDARY_CHARGE_ZERO", "q can reappear as edge hair or source charge"),
        ("NPQ2292_4_degree_count", "constraints remove the local q pair", "primary/secondary first-class pair removes q and reduced Omega has no proper q stabilizer", "MISSING_DEGREE_COUNT", "no-pole cannot be distinguished from under-specified dynamics"),
        ("NPQ2292_5_matter_readout", "ordinary matter/readout descends through q and no marker sees q", "S_matter=Sbar[Obs(q(Phi)),psi,theta] and Lie_vq theta=0", "MISSING_MATTER_NO_MARKER_SIGNATURE", "beta_source/beta_test rows remain live even if the bulk pole is controlled"),
        ("NPQ2292_6_verdict", "no physical local q pole in the GR/Newton branch", "NPQ2292_0 through NPQ2292_5 all close from one parent action and boundary prescription", "FAIL_CURRENT_CLAIM_NO_POLE_NOT_PROVED", "build bounded beta_source/beta_test runner and retain no-cancellation tails"),
    ]
    return [
        {
            "audit_id": audit_id,
            "criterion": criterion,
            "mathematical_test": test,
            "result": result,
            "if_missing": if_missing,
            "valid_for_claim": False,
        }
        for audit_id, criterion, test, result, if_missing in entries
    ]


def countermodel_rows() -> list[dict[str, Any]]:
    return [
        {"countermodel_id": "PCM2292_0_second_class_q", "countermodel": "q has a degenerate-looking Hessian but constraints are second class or incomplete", "why_it_matters": "no Green kernel cannot be claimed without first-class closure and degree count", "blocked_by": "parent Omega, D C_q, bracket, degree-count proof", "valid_for_claim": False},
        {"countermodel_id": "PCM2292_1_edge_mode", "countermodel": "bulk vertical variation is pure gauge, but boundary charge Q_q survives", "why_it_matters": "R10/source charge can be carried by edge hair", "blocked_by": "boundary differentiability, Q_q=0/proper/exact, K_boundary=0", "valid_for_claim": False},
        {"countermodel_id": "PCM2292_2_shadow_matter_frame", "countermodel": "ordinary matter uses a universal q-dependent Weyl/disformal frame", "why_it_matters": "WEP may look fine while beta_source=beta_test=c_g and R10 sees c_g^2", "blocked_by": "no-shadow-frame theorem or numeric c_g/b_dis bound", "valid_for_claim": False},
        {"countermodel_id": "PCM2292_3_marker_constants", "countermodel": "masses, EM constants, or material markers carry q-dependence", "why_it_matters": "clock/WEP/composition constraints become tied to R10 beta rows", "blocked_by": "no-marker theorem or b_A/b_alpha bounds", "valid_for_claim": False},
        {"countermodel_id": "PCM2292_4_hidden_support", "countermodel": "non-Hilbert current, source support, or domain/boundary tail sources q", "why_it_matters": "alpha_q can survive even if visible Hilbert matter descends", "blocked_by": "q_nonH, Delta_W_support, q_domain, and q_boundary zero/bound rows", "valid_for_claim": False},
    ]


def omega_dcq_rows() -> list[dict[str, Any]]:
    entries = [
        ("ODQ2292_0_parent_Omega", "parent symplectic form", "Omega_Y=delta Theta_Y on the full parent variable set before quotient/gauge fixing", "MISSING_PARENT_OMEGA", "D C_q^dagger cannot be identified with an Omega-flat vertical vector"),
        ("ODQ2292_1_DCq_operator", "linearized q constraint/source operator D C_q", "C_q[Phi]=0 is parent-owned and D C_q maps field variations into the q constraint covector", "MISSING_DCQ_OPERATOR", "D C_q^dagger is pairing-dependent bookkeeping, not a generator proof"),
        ("ODQ2292_2_Omega_flat_map", "Omega-flat vertical generator identity", "i_{v_q} Omega_Y=delta C_q[epsilon] or D C_q^dagger epsilon=Omega_Y^flat(v_q[epsilon])", "NOT_COMPARABLE_WITHOUT_OMEGA_AND_DCQ", "rank-zero/null directions do not prove gauge; a physical or edge mode can remain"),
        ("ODQ2292_3_vertical_generator_fields", "field-by-field vertical generator", "v_q is specified on metric/coframe, momenta, q, domain/memory/projector, matter/readout, and boundary fields", "FIELD_MAP_INCOMPLETE", "the putative gauge direction can leak into source/test charges"),
        ("ODQ2292_4_boundary_differentiability", "boundary charge Q_q", "delta Q_q cancels all boundary variation and Q_q is zero, exact, or proper on the local branch", "MISSING_BOUNDARY_CHARGE_ZERO", "source charge can be hidden in edge hair"),
        ("ODQ2292_5_bracket_closure", "first-class bracket and boundary cocycle", "{G_q[epsilon],G_q[eta]}=G_q[[epsilon,eta]]+K_boundary and K_boundary=0 locally", "MISSING_BRACKET_KBOUNDARY", "the q direction may be second-class, anomalous, or edge-charged"),
        ("ODQ2292_6_degree_count", "reduced phase-space degree count", "primary/secondary first-class pair removes the local q pair and reduced Omega is nondegenerate without a q stabilizer", "MISSING_DEGREE_COUNT", "no-pole can be confused with under-specified dynamics"),
        ("ODQ2292_7_matter_readout", "matter/no-marker descent", "S_matter=Sbar[q(Phi),psi,theta] and ordinary constants/readouts carry no representative-q marker", "MISSING_MATTER_QUOTIENT", "beta_source and beta_test remain live"),
        ("ODQ2292_8_verdict", "exact no-physical-q-pole certificate", "ODQ2292_0 through ODQ2292_7 close from one parent action and boundary prescription", "FAIL_CURRENT_CLAIM_NO_POLE_NOT_CLOSED", "attack boundary charge/cocycle first and stage beta bounds"),
    ]
    return [
        {
            "audit_id": audit_id,
            "object": obj,
            "needed_statement": statement,
            "current_status": status,
            "if_missing": if_missing,
            "valid_for_claim": False,
        }
        for audit_id, obj, statement, status, if_missing in entries
    ]


def vertical_map_rows() -> list[dict[str, Any]]:
    return [
        {"field_block": "metric_or_coframe", "candidate_vertical_action": "v_q[g]=Lie_epsilon g or v_q[e]=Lie_epsilon e plus local Lorentz compensation if q is pure representative", "Omega_flat_target": "metric/coframe component of Omega_Y^flat(v_q)", "DCq_target": "metric/coframe component of D C_q^dagger epsilon", "status": "STANDARD_CANDIDATE_NOT_PARENT_DECLARED", "missing_input": "observed metric/coframe ownership and parent symplectic potential", "valid_for_claim": False},
        {"field_block": "q_residual_block", "candidate_vertical_action": "v_q[q] is either a pure vertical representative shift, algebraic constraint response, or no action if q is absent", "Omega_flat_target": "q component of Omega_Y^flat(v_q)", "DCq_target": "q component of D C_q^dagger epsilon", "status": "CORE_BLOCK_UNWRITTEN", "missing_input": "explicit q parent variable status and transformation law", "valid_for_claim": False},
        {"field_block": "canonical_momenta_or_boundary_charge", "candidate_vertical_action": "v_q[pi]=Lie_epsilon pi plus density and boundary improvements", "Omega_flat_target": "momentum and boundary component of Omega_Y^flat(v_q)", "DCq_target": "integration-by-parts boundary term in delta C_q[epsilon]", "status": "NOT_WRITTEN_FOR_MTS", "missing_input": "canonical variables or covariant phase-space charge split", "valid_for_claim": False},
        {"field_block": "domain_memory_projector_fields", "candidate_vertical_action": "v_q[Phi^A]=Lie_epsilon Phi^A or quotient-vertical representative shift", "Omega_flat_target": "domain/memory/projector component of Omega_Y^flat(v_q)", "DCq_target": "extra-sector component of D C_q^dagger", "status": "UNMAPPED", "missing_input": "transformation law for domain, memory, projector, and boundary variables", "valid_for_claim": False},
        {"field_block": "matter_readout_constants", "candidate_vertical_action": "v_q[psi]=0 and v_q[theta_A]=0 only if matter descends through q", "Omega_flat_target": "matter component should vanish or be quotient-pullback only", "DCq_target": "no source/test marker covector", "status": "NOT_DERIVED", "missing_input": "matter action descent and no-marker theorem", "valid_for_claim": False},
        {"field_block": "boundary_edge_modes", "candidate_vertical_action": "proper compact transformation or exact boundary representative shift", "Omega_flat_target": "no residual boundary charge in Omega_Y^flat(v_q)", "DCq_target": "Q_q=0/exact/proper and K_boundary=0", "status": "NOT_DERIVED", "missing_input": "boundary differentiability, Q_q, and cocycle computation", "valid_for_claim": False},
    ]


def bounded_beta_rows() -> list[dict[str, Any]]:
    entries = [
        ("BB2292_0_beta_source_geom", "source", "beta_s_geom", "source-body q charge from common Weyl/disformal observed-frame leakage", "|beta_s_geom| <= |profile_s^W c_g| + |profile_s^dis b_dis|", "MISSING_FRAME_LEAK_ZERO_OR_NUMERIC_BOUND", "R10;PPN;WEP;clock"),
        ("BB2292_1_beta_test_geom", "test", "beta_t_geom", "test/readout q charge from common Weyl/disformal observed-frame leakage", "|beta_t_geom| <= |tau_R10 c_g| + |tau_dis b_dis|", "MISSING_ARENA_PROJECTION", "R10;PPN;WEP;clock"),
        ("BB2292_2_beta_source_marker", "source", "beta_s_marker", "source composition/material/EM marker q charge", "|beta_s_marker| <= sum_A |S_sA b_A| + |S_salpha b_alpha|", "MISSING_NO_MARKER_THEOREM_OR_NUMERIC_BOUNDS", "WEP;clock;composition;R10"),
        ("BB2292_3_beta_test_marker", "test", "beta_t_marker", "test material/readout marker q charge", "|beta_t_marker| <= sum_A |S_tA b_A| + |S_talpha b_alpha|", "MISSING_MARKER_READOUT_PROJECTION", "WEP;clock;composition;R10"),
        ("BB2292_4_beta_source_nonH", "source", "beta_s_nonH", "source-side non-Hilbert/boundary/domain/support q current", "|beta_s_nonH| <= |q_nonH_s| + |Delta_W_support_s| + |q_domain_s| + |q_boundary_s|", "MISSING_HIDDEN_SOURCE_ZERO_OR_NUMERIC_BOUND", "R10;orbital;source_normalization;local_GR"),
        ("BB2292_5_beta_test_nonH", "test", "beta_t_nonH", "test/readout-side non-Hilbert/boundary/domain/support q current", "|beta_t_nonH| <= |q_nonH_t| + |Delta_W_support_t| + |q_domain_t| + |q_boundary_t|", "MISSING_HIDDEN_TEST_ZERO_OR_NUMERIC_BOUND", "R10;orbital;source_normalization;local_GR"),
        ("BB2292_6_beta_abs_totals", "source_and_test", "beta_s_abs;beta_t_abs", "absolute no-cancellation source/test beta envelopes", "beta_s_abs=sum_i |beta_s_i|; beta_t_abs=sum_i |beta_t_i|", "SCHEMA_READY_VALUES_MISSING", "all_local_arenas"),
        ("BB2292_7_beta_product_guard", "source_times_test", "abs_beta_product", "claim-safe source-test product for finite exchange", "|beta_s beta_t| <= beta_s_abs beta_t_abs; universal Weyl gives c_g^2 contribution", "CLAIM_BLOCKED", "R10;PPN;WEP;clock;orbital"),
    ]
    return [
        {
            "beta_id": beta_id,
            "leg": leg,
            "symbol": symbol,
            "definition": definition,
            "formula_or_bound": formula,
            "current_status": status,
            "observable_links": links,
            "score_ready": False,
            "valid_for_claim": False,
        }
        for beta_id, leg, symbol, definition, formula, status, links in entries
    ]


def tail_envelope_rows() -> list[dict[str, Any]]:
    return [
        {"tail_id": "TAIL2292_0_alpha_envelope", "quantity": "abs_alpha_q(lambda)", "formula": "|alpha_q| <= |K_q^R10(lambda)| * [beta_s_abs beta_t_abs + abs_tail_source_test(lambda)]", "missing_inputs": "K_q^R10;beta_s_abs;beta_t_abs;tail rows;promoted alpha_bound(lambda)", "current_status": "MISSING_NUMERIC_ENVELOPE", "valid_for_claim": False},
        {"tail_id": "TAIL2292_1_no_cancellation_policy", "quantity": "tail addition rule", "formula": "unknown components add in absolute value; no cancellation credit between c_g,b_dis,b_A,b_alpha,q_nonH,boundary/support", "missing_inputs": "component theorem-zero or numeric/source-backed bounds", "current_status": "POLICY_ACTIVE", "valid_for_claim": False},
        {"tail_id": "TAIL2292_2_R10_score_gate", "quantity": "R10 comparison gate", "formula": "score only if abs_alpha_q(lambda) and alpha_bound(lambda) are numeric, sourced, unit-matched, and valid_for_claim=true", "missing_inputs": "MTS prediction and promoted bound curve", "current_status": "CLAIM_BLOCKED", "valid_for_claim": False},
    ]


def arena_routing_rows() -> list[dict[str, Any]]:
    return [
        {"arena_id": "ARENA2292_0_R10", "arena": "short-range fifth force", "receives": "K_q^R10 beta_s beta_t plus absolute tails", "required_projection": "lambda profile, source/test support, tau_R10, bound curve", "current_status": "BLOCKED_BY_BETA_KQ_BOUND", "valid_for_claim": False},
        {"arena_id": "ARENA2292_1_PPN", "arena": "PPN/local weak field", "receives": "common frame c_g, disformal b_dis, non-Hilbert/support tails", "required_projection": "gauge-fixed response matrix for gamma,beta,preferred-frame rows", "current_status": "BLOCKED_ARENA_PROJECTION_MISSING", "valid_for_claim": False},
        {"arena_id": "ARENA2292_2_WEP_clock", "arena": "WEP, clocks, EM/material markers", "receives": "b_A,b_alpha,c_g marker/readout sensitivities", "required_projection": "material sensitivities, clock coefficients, composition pairs", "current_status": "BLOCKED_MARKER_DESCENT_OR_NUMERIC_BOUNDS_MISSING", "valid_for_claim": False},
        {"arena_id": "ARENA2292_3_orbital_source", "arena": "orbital/source normalization/local GR", "receives": "q_nonH, Delta_W_support, boundary/domain support tails", "required_projection": "worldtube/source support and orbital observable map", "current_status": "BLOCKED_SUPPORT_THEOREM_OR_BOUND_MISSING", "valid_for_claim": False},
    ]


def alpha_template_rows() -> list[dict[str, Any]]:
    return [
        {"model_id": "MTS_source_normalized_Newton_branch", "template_branch": "no_physical_q_pole_template", "lambda_value": "ALL_LOCAL_R10_RANGE", "alpha_predicted": "MISSING_NO_PHYSICAL_Q_POLE_CERTIFICATE", "force_law_form": "no active finite Yukawa pole only if quotient/constraint/boundary/matter certificate closes", "derivation_status": "template_invalid_no_pole_not_parent_signed", "valid_for_claim": False},
        {"model_id": "MTS_source_normalized_Newton_branch", "template_branch": "bounded_beta_product_template", "lambda_value": "MISSING_PARENT_LAMBDA_Q", "alpha_predicted": "MISSING_KQ_TIMES_BETA_S_ABS_BETA_T_ABS_TAILS", "force_law_form": "|alpha_q| <= |K_q^R10| [beta_s_abs beta_t_abs + abs_tail]", "derivation_status": "template_invalid_bounded_beta_inputs_missing", "valid_for_claim": False},
        {"model_id": "MTS_source_normalized_Newton_branch", "template_branch": "universal_weyl_cg_squared_template", "lambda_value": "MISSING_PARENT_LAMBDA_Q", "alpha_predicted": "MISSING_KQ_PROFILE_CG_SQUARED", "force_law_form": "universal Weyl source/test branch: alpha_q proportional to K_q^R10 c_g^2", "derivation_status": "template_invalid_cg_and_Kq_missing", "valid_for_claim": False},
    ]


def runner_smoke_rows() -> list[dict[str, Any]]:
    return [{"smoke_id": "SMOKE2292_0_runner_status", "valid_mts_rows": 0, "valid_bound_rows": 0, "comparison_rows": 1, "R10_pass_for_claim": False, "claim_allowed": False, "expected_result": "blocked_nonclaim", "valid_for_claim": False}]


def refusal_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in no_pole_audit_rows():
        rows.append({"refusal_id": f"REF2292_NOPOLE_{len(rows)}", "object": row["criterion"], "current_status": row["result"], "refusal_status": "no_pole_claim_rejected_current_corpus", "failure_reasons": f"{row['result']};CLAIM_POLICY_FALSE", "score_eligible": False, "claim_allowed": False, "valid_for_claim": False})
    for row in bounded_beta_rows():
        rows.append({"refusal_id": f"REF2292_BETA_{row['beta_id']}", "object": row["symbol"], "current_status": row["current_status"], "refusal_status": "bounded_beta_row_rejected_missing_inputs", "failure_reasons": f"{row['current_status']};SCORE_READY_FALSE;CLAIM_POLICY_FALSE", "score_eligible": False, "claim_allowed": False, "valid_for_claim": False})
    for row in omega_dcq_rows():
        rows.append({"refusal_id": f"REF2292_ODQ_{row['audit_id']}", "object": row["object"], "current_status": row["current_status"], "refusal_status": "omega_dcq_claim_rejected_current_corpus", "failure_reasons": f"{row['current_status']};CLAIM_POLICY_FALSE", "score_eligible": False, "claim_allowed": False, "valid_for_claim": False})
    return rows


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {"gate_id": "CGATE2292_0_no_pole", "claim": "finite local q mode has no physical pole", "gate_pass": False, "reason": "parent Omega, D C_q, vertical action, boundary charge, degree count, and matter/no-marker signature remain incomplete", "claim_allowed": False, "valid_for_claim": False},
        {"gate_id": "CGATE2292_1_alpha_zero", "claim": "R10 alpha_q=0 locally", "gate_pass": False, "reason": "no-pole and hidden-tail clauses are not parent-signed", "claim_allowed": False, "valid_for_claim": False},
        {"gate_id": "CGATE2292_2_bounded_beta", "claim": "bounded beta_source/beta_test rows are score-ready", "gate_pass": False, "reason": "all beta component rows still contain missing theorem-zero or numeric/source-backed inputs", "claim_allowed": False, "valid_for_claim": False},
        {"gate_id": "CGATE2292_3_linear_cg", "claim": "linear c_g can be scored against R10", "gate_pass": False, "reason": "universal Weyl source/test branch contributes c_g squared", "claim_allowed": False, "valid_for_claim": False},
        {"gate_id": "CGATE2292_4_R10_local_GR_pass", "claim": "R10/local-GR pass is established", "gate_pass": False, "reason": "MTS rows and external bound curve remain nonclaim/unscoreable", "claim_allowed": False, "valid_for_claim": False},
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {"decision_id": "DEC2292_0_no_pole_status", "decision": "No-pole remains the cleanest GR-reduction route, but it fails current-claim status.", "because": "the route requires parent Omega, D C_q, field-by-field vertical generator, boundary charge silence, degree count, and matter/no-marker descent together", "next_action": "attack the missing boundary charge/cocycle first because it decides whether edge charge becomes beta source", "valid_for_claim": False},
        {"decision_id": "DEC2292_1_beta_fallback_status", "decision": "The fallback is a bounded beta_source/beta_test acquisition problem.", "because": "if a physical finite pole survives, local tests see beta_source beta_test plus absolute tails, not a single coupling", "next_action": "fill theorem-zero or numeric/source-backed beta component rows one by one", "valid_for_claim": False},
        {"decision_id": "DEC2292_2_linear_cg_status", "decision": "Legacy linear c_g shorthand remains quarantined.", "because": "a source-test interaction needs both legs; universal frame leakage is quadratic unless Qbar owns one leg", "next_action": "make future candidate rows declare beta_source beta_test or an explicit source leg inside Qbar with source path and units", "valid_for_claim": False},
        {"decision_id": "DEC2292_3_next_target", "decision": "Next target should attack boundary charge/cocycle first while keeping beta acquisition ready.", "because": "Q_q=0 and K_boundary=0 are the sharpest single remaining no-pole obstruction", "next_action": "2293-Y5-R2FR-boundary-charge-Qq-Kboundary-zero-or-beta-bound-first-row.md", "valid_for_claim": False},
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_target": "2293-Y5-R2FR-boundary-charge-Qq-Kboundary-zero-or-beta-bound-first-row.md",
            "script": "scripts/Y5_R2FR_boundary_charge_Qq_Kboundary_zero_or_beta_bound_first_row_2293.py",
            "objective": "try to compute or prove silence of Q_q and K_boundary for the local q vertical branch; if this fails, fill the first source-backed beta projection row without claiming a pass",
            "include": "boundary variation of G_q, Q_q exact/proper/zero tests, K_boundary cocycle, compact-support local transformation limit, first beta source row schema",
            "exclude": "invented parent action terms, naked linear c_g scoring, cancellation between beta tails, R10/local-GR pass claim, formalization-workbench edits, GitHub action",
            "valid_for_claim": False,
        }
    ]


def generated_claim_flags_false(paths: list[Path]) -> bool:
    false_values = {"", "false", "0", "no", "none", "null"}
    guarded_keys = {"score_ready", "valid_for_claim", "claim_allowed", "R10_pass_for_claim", "score_eligible", "gate_pass"}
    for path in paths:
        for row in read_csv(path):
            for key, value in row.items():
                if key in guarded_keys and value.strip().lower() not in false_values:
                    return False
    return True


def copy_branch_files() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for copy_id, (source_path, target_path) in COPY_TARGETS.items():
        target_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source_path, target_path)
        rows.append({"copy_id": copy_id, "source_path": source_path, "target_path": target_path, "target_exists": target_path.exists(), "target_parses": csv_parses(target_path), "reason": "branch copy for 2292 no-pole/bounded-beta checkpoint"})
    return rows


def validation_rows(all_generated_before_validation: list[Path], branch_copy_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    source_rows = read_csv(OUTPUTS["source_register"])
    no_pole_rows = read_csv(OUTPUTS["no_pole_audit"])
    omega_rows = read_csv(OUTPUTS["omega_dcq"])
    beta_rows = read_csv(OUTPUTS["bounded_beta"])
    tail_rows = read_csv(OUTPUTS["tail_envelope"])
    arena_rows = read_csv(OUTPUTS["arena_routing"])
    runner_rows = read_csv(OUTPUTS["runner_smoke"])
    refusal_rows_local = read_csv(OUTPUTS["refusal"])
    claim_rows = read_csv(OUTPUTS["claim_gates"])
    decision_rows_local = read_csv(OUTPUTS["decision"])
    next_rows = read_csv(OUTPUTS["next_target"])

    checks = [
        ("VAL2292_0_sources_exist", all(row["exists"] == "True" for row in source_rows), "all cited source paths exist"),
        ("VAL2292_1_needles_present", all(row["needles_present"] == "True" for row in source_rows), "all cited source needles are present"),
        ("VAL2292_2_prior_validations", validation_pass(OUT / "P8_Y5_BRR545_2291_VALIDATION.csv") and validation_pass(OUT / "P8_Y5_BRR545_2244_VALIDATION.csv") and validation_pass(OUT / "P8_Y5_BRR545_1038_VALIDATION.csv"), "2291, 2244, and 1038 validations pass overall"),
        ("VAL2292_3_no_pole_not_proved", any(row["audit_id"] == "NPQ2292_6_verdict" and row["result"] == "FAIL_CURRENT_CLAIM_NO_POLE_NOT_PROVED" for row in no_pole_rows), "no physical q pole theorem is not proved"),
        ("VAL2292_4_omega_dcq_blocks", any(row["audit_id"] == "ODQ2292_8_verdict" and row["current_status"] == "FAIL_CURRENT_CLAIM_NO_POLE_NOT_CLOSED" for row in omega_rows), "Omega/DCq closure audit blocks no-pole claim"),
        ("VAL2292_5_beta_template_blocked", any(row["beta_id"] == "BB2292_7_beta_product_guard" and row["current_status"] == "CLAIM_BLOCKED" for row in beta_rows) and all(row["score_ready"] == "False" for row in beta_rows), "bounded beta rows are schema-only and blocked"),
        ("VAL2292_6_tail_policy_active", any(row["tail_id"] == "TAIL2292_1_no_cancellation_policy" and row["current_status"] == "POLICY_ACTIVE" for row in tail_rows), "absolute no-cancellation tail policy is active"),
        ("VAL2292_7_arena_routes_complete", {"short-range fifth force", "PPN/local weak field", "WEP, clocks, EM/material markers", "orbital/source normalization/local GR"}.issubset({row["arena"] for row in arena_rows}), "arena routing covers R10, PPN, WEP/clock, and orbital/source channels"),
        ("VAL2292_8_runner_refuses_claim", any(row["expected_result"] == "blocked_nonclaim" and row["claim_allowed"] == "False" for row in runner_rows), "runner smoke status refuses a claim"),
        ("VAL2292_9_refusal_runner", len(refusal_rows_local) >= 20 and all(row["claim_allowed"] == "False" and row["valid_for_claim"] == "False" for row in refusal_rows_local), "placeholder refusal runner blocks no-pole, beta, and Omega/DCq claims"),
        ("VAL2292_10_claim_gates_blocked", all(row["gate_pass"] == "False" and row["claim_allowed"] == "False" for row in claim_rows), "all claim gates remain blocked"),
        ("VAL2292_11_decision_next", any(row["decision_id"] == "DEC2292_3_next_target" for row in decision_rows_local) and any(row["next_target"] == "2293-Y5-R2FR-boundary-charge-Qq-Kboundary-zero-or-beta-bound-first-row.md" for row in next_rows), "decision selects boundary charge/cocycle or beta bound first row next"),
        ("VAL2292_12_csv_parse", all(csv_parses(path) for path in all_generated_before_validation), "all generated 2292 CSVs parse cleanly"),
        ("VAL2292_13_no_claim_flags", generated_claim_flags_false(all_generated_before_validation), "all generated prediction/claim flags remain false"),
        ("VAL2292_14_branch_copies", all(row["target_exists"] and row["target_parses"] for row in branch_copy_rows), "branch/queue copies exist and parse"),
        ("VAL2292_15_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent after run"),
        ("VAL2292_16_formalization_no_2292", not formalization_has_2292_artifacts(), "formalization-workbench has no non-venv 2292 artifacts"),
        ("VAL2292_17_formalization_untouched", not formalization_touched_since_start(), "formalization-workbench untouched during 2292 run"),
    ]
    rows = [{"check_id": check_id, "result": "PASS" if passed else "FAIL", "detail": detail} for check_id, passed, detail in checks]
    rows.append({"check_id": "VAL2292_OVERALL", "result": "PASS" if all(row["result"] == "PASS" for row in rows) else "FAIL", "detail": "2292 refuses no-physical-q-pole claim, stages bounded beta rows with no-cancellation tails, and selects Qq/Kboundary or beta-bound first row next"})
    return rows


def write_markdown(
    sources: list[dict[str, Any]],
    no_pole: list[dict[str, Any]],
    countermodels: list[dict[str, Any]],
    omega_dcq: list[dict[str, Any]],
    vertical_map: list[dict[str, Any]],
    beta_rows: list[dict[str, Any]],
    tails: list[dict[str, Any]],
    arenas: list[dict[str, Any]],
    alpha_template: list[dict[str, Any]],
    runner: list[dict[str, Any]],
    refusal: list[dict[str, Any]],
    claim_gates: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
    branch_copies: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> None:
    content = f"""# 2292 - Y5/R2FR No Physical q Pole Theorem or Bounded Beta Runner

## Verdict

2292 attacks the cleanest local-GR route: prove the finite local `q/R_AB` residual has no physical exchange pole in the GR/Newton branch.

The route is not proved by the current corpus. It needs parent `Omega_Y`, parent-owned `D C_q`, all-field `v_q`, boundary `Q_q`, cocycle `K_boundary`, degree count, and matter/no-marker descent to close together. This does not kill the framework; it prevents an unsafe `alpha_q=0` claim and keeps the finite branch as a bounded `beta_source beta_test` problem with absolute no-cancellation tails.

The old naked linear `c_g` route remains quarantined: universal source/test leakage enters as `c_g^2` unless the source leg is explicitly source-backed inside `Qbar`.

## Source Register
{table(["source_id", "source_key", "source_path", "exists", "needles_present", "role", "valid_for_claim"], sources)}

## No Physical q Pole Audit
{table(["audit_id", "criterion", "mathematical_test", "result", "if_missing", "valid_for_claim"], no_pole)}

## Pole Countermodel Ledger
{table(["countermodel_id", "countermodel", "why_it_matters", "blocked_by", "valid_for_claim"], countermodels)}

## Omega/D Cq Closure Audit
{table(["audit_id", "object", "needed_statement", "current_status", "if_missing", "valid_for_claim"], omega_dcq)}

## Vertical Generator Field Map
{table(["field_block", "candidate_vertical_action", "Omega_flat_target", "DCq_target", "status", "missing_input", "valid_for_claim"], vertical_map)}

## Bounded Beta Source/Test Template
{table(["beta_id", "leg", "symbol", "definition", "formula_or_bound", "current_status", "observable_links", "score_ready", "valid_for_claim"], beta_rows)}

## Absolute Tail Envelope
{table(["tail_id", "quantity", "formula", "missing_inputs", "current_status", "valid_for_claim"], tails)}

## Arena Routing Map
{table(["arena_id", "arena", "receives", "required_projection", "current_status", "valid_for_claim"], arenas)}

## MTS Alpha Template Update
{table(["model_id", "template_branch", "lambda_value", "alpha_predicted", "force_law_form", "derivation_status", "valid_for_claim"], alpha_template)}

## Runner Smoke Status
{table(["smoke_id", "valid_mts_rows", "valid_bound_rows", "comparison_rows", "R10_pass_for_claim", "claim_allowed", "expected_result", "valid_for_claim"], runner)}

## Placeholder Refusal Runner
{table(["refusal_id", "object", "current_status", "refusal_status", "failure_reasons", "score_eligible", "claim_allowed", "valid_for_claim"], refusal)}

## Claim Gates
{table(["gate_id", "claim", "gate_pass", "reason", "claim_allowed", "valid_for_claim"], claim_gates)}

## Decision Ledger
{table(["decision_id", "decision", "because", "next_action", "valid_for_claim"], decisions)}

## Next Target
{table(["next_target", "script", "objective", "include", "exclude", "valid_for_claim"], next_target)}

## Branch Copies
{table(["copy_id", "source_path", "target_path", "target_exists", "target_parses", "reason"], branch_copies)}

## Validation
{table(["check_id", "result", "detail"], validation)}

## Working Interpretation

This is a useful failure. We now know the no-pole route is not blocked by vibes; it is blocked by a sharp object: the boundary charge/cocycle package `Q_q, K_boundary` plus parent `Omega/D C_q`. The next clean attack is therefore not another broad coupling hunt. It is boundary charge silence or the first real bounded beta row.
"""
    DOC.write_text(content, encoding="utf-8")


def main() -> None:
    remove_pycache()
    sources = source_register_rows()
    no_pole = no_pole_audit_rows()
    countermodels = countermodel_rows()
    omega_dcq = omega_dcq_rows()
    vertical_map = vertical_map_rows()
    beta_rows = bounded_beta_rows()
    tails = tail_envelope_rows()
    arenas = arena_routing_rows()
    alpha_template = alpha_template_rows()
    runner = runner_smoke_rows()
    refusal = refusal_rows()
    claim_gates = claim_gate_rows()
    decisions = decision_rows()
    next_target = next_target_rows()

    write_csv(OUTPUTS["source_register"], sources)
    write_csv(OUTPUTS["no_pole_audit"], no_pole)
    write_csv(OUTPUTS["countermodels"], countermodels)
    write_csv(OUTPUTS["omega_dcq"], omega_dcq)
    write_csv(OUTPUTS["vertical_map"], vertical_map)
    write_csv(OUTPUTS["bounded_beta"], beta_rows)
    write_csv(OUTPUTS["tail_envelope"], tails)
    write_csv(OUTPUTS["arena_routing"], arenas)
    write_csv(OUTPUTS["alpha_template"], alpha_template)
    write_csv(OUTPUTS["runner_smoke"], runner)
    write_csv(OUTPUTS["refusal"], refusal)
    write_csv(OUTPUTS["claim_gates"], claim_gates)
    write_csv(OUTPUTS["decision"], decisions)
    write_csv(OUTPUTS["next_target"], next_target)

    branch_copies = copy_branch_files()
    write_csv(OUTPUTS["branch_copies"], branch_copies)

    generated_before_validation = [
        OUTPUTS["source_register"],
        OUTPUTS["no_pole_audit"],
        OUTPUTS["countermodels"],
        OUTPUTS["omega_dcq"],
        OUTPUTS["vertical_map"],
        OUTPUTS["bounded_beta"],
        OUTPUTS["tail_envelope"],
        OUTPUTS["arena_routing"],
        OUTPUTS["alpha_template"],
        OUTPUTS["runner_smoke"],
        OUTPUTS["refusal"],
        OUTPUTS["claim_gates"],
        OUTPUTS["decision"],
        OUTPUTS["next_target"],
        OUTPUTS["branch_copies"],
    ]
    remove_pycache()
    validation = validation_rows(generated_before_validation, branch_copies)
    write_csv(OUTPUTS["validation"], validation)
    write_markdown(
        sources,
        no_pole,
        countermodels,
        omega_dcq,
        vertical_map,
        beta_rows,
        tails,
        arenas,
        alpha_template,
        runner,
        refusal,
        claim_gates,
        decisions,
        next_target,
        branch_copies,
        validation,
    )
    remove_pycache()

    failed = [row for row in validation if row["result"] != "PASS"]
    if failed:
        failed_ids = ", ".join(row["check_id"] for row in failed)
        raise SystemExit(f"2292 validation failed: {failed_ids}")
    print(f"Wrote {DOC}")
    print(f"Wrote {OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
