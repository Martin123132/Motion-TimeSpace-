from __future__ import annotations

import csv
import py_compile
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Tuple


ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
SOURCE_DIR = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = PROJECT / "formalization-workbench"
SCRIPT_PATH = Path(__file__).resolve()
DOC_PATH = ROOT / "4117-Y5-R2FR-parent-action-total-evenness-quotient-descent-or-JZ-bound-runner.md"

TIMESTAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
BRANCH_ID = "MTS_R2FR_Y5_PARENT_ACTION_JZ_ZERO_CURRENT_SPINE_4117"
CHECKPOINT_ID = "4117"
DECISION = "PARENT_ACTION_JZ_ZERO_THEOREM_IMPORTED_VERTICAL_Z_MAP_NEXT"


LOCAL_SOURCES: Dict[str, Tuple[Path, str, str]] = {
    "SRC4117_00_4116_next": (
        SOURCE_DIR / "P8_Y5_R2FR_4116_NEXT_TARGET.csv",
        "4117-Y5-R2FR-parent-action-total-evenness-quotient-descent-or-JZ-bound-runner.md",
        "4116 selected total-evenness/quotient-descent parent-action target.",
    ),
    "SRC4117_01_4116_status": (
        SOURCE_DIR / "P8_Y5_R2FR_4116_STATUS.csv",
        "JZ_COUPLING_LAW_IMPORTED_ZERO_ROUTE_UNSIGNED_PARENT_ACTION_CLAUSE_NEXT",
        "Current-chain J_Z coupling handoff.",
    ),
    "SRC4117_02_3630_status": (
        SOURCE_DIR / "P8_Y5_R2FR_3630_STATUS.csv",
        "PARENT_ACTION_JZ_ZERO_THEOREM_CONDITIONAL_SIGNATURE_UNSIGNED",
        "3630 writes sufficient parent-action theorem for J_Z=0.",
    ),
    "SRC4117_03_3630_clause": (
        SOURCE_DIR / "P8_Y5_R2FR_3630_PARENT_ACTION_CLAUSE.csv",
        "PAC3630_7_physical_flux_separation",
        "Parent-action clause: quotient descent, evenness, source, boundary and flux separation.",
    ),
    "SRC4117_04_3630_theorem": (
        SOURCE_DIR / "P8_Y5_R2FR_3630_JZ_ZERO_THEOREM_DERIVATION.csv",
        "THM3630_6_conclusion",
        "Conditional theorem proving J_Z=0 under the parent-action clauses.",
    ),
    "SRC4117_05_3630_signature": (
        SOURCE_DIR / "P8_Y5_R2FR_3630_PARENT_SIGNATURE_AUDIT.csv",
        "SIG3630_8_verdict",
        "Parent-signature audit showing current corpus does not claim J_Z=0.",
    ),
    "SRC4117_06_3630_bounds": (
        SOURCE_DIR / "P8_Y5_R2FR_3630_JZ_BOUND_REQUIREMENTS.csv",
        "JZB3630_8_R11_operator",
        "J_Z bound requirements if parent theorem fails.",
    ),
    "SRC4117_07_3630_decisions": (
        SOURCE_DIR / "P8_Y5_R2FR_3630_DECISION_GATES.csv",
        "DEC3630_2_best_next",
        "3630 decision selecting vertical generator/Z map as next target.",
    ),
    "SRC4117_08_3630_next": (
        SOURCE_DIR / "P8_Y5_R2FR_3630_NEXT_TARGET.csv",
        "3631-Y5-R2FR-vertical-generator-Z-map-or-JZ-coefficient-runner.md",
        "3630 next target: vertical generator Z map or J_Z coefficient runner.",
    ),
    "SRC4117_09_script": (
        SCRIPT_PATH,
        "Y5_R2FR_4117_parent_action_total_evenness_quotient_descent_or_JZ_bound_runner.py",
        "Reproducible generator for this 4117 checkpoint.",
    ),
}


def row_base() -> dict:
    return {"timestamp_utc": TIMESTAMP, "branch_id": BRANCH_ID, "checkpoint_id": CHECKPOINT_ID}


def bool_string(value: bool) -> str:
    return "True" if value else "False"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig", errors="replace")


def parse_csv(path: Path) -> List[dict]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: List[dict]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: List[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def is_under(path: Path, parent: Path) -> bool:
    try:
        path.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


def source_register_rows() -> List[dict]:
    rows = []
    for source_id, (path, needle, role) in LOCAL_SOURCES.items():
        text = read_text(path) if path.exists() else ""
        rows.append(
            {
                **row_base(),
                "source_id": source_id,
                "source_path": str(path),
                "exists": bool_string(path.exists()),
                "needle": needle,
                "needle_found": bool_string(path.exists() and needle in text),
                "role": role,
                "claim_allowed": bool_string(False),
                "valid_for_claim": bool_string(False),
            }
        )
    return rows


def parent_action_clause_rows() -> List[dict]:
    rows = [
        ("PAC4117_0_variables", "parent variables and quotient", "q:Phi_parent->Q_MTS; local response basis e_A has Dq[e_A]=0; Z^A coordinates vertical response basis", "CLAUSE_WRITTEN_VERTICAL_GENERATOR_NOT_PARENT_MAPPED"),
        ("PAC4117_1_total_action", "single admissible parent action", "S_parent=S_EH+S_even+S_matter[gbar(q),Psi,theta(q)]+S_source[Pi_M(q)J_H(q,Psi)]+S_boundary[B(q),ref]+S_phys_flux", "SUFFICIENT_PARENT_ACTION_CLAUSE_WRITTEN_NOT_CURRENT_CORPUS_SIGNED"),
        ("PAC4117_2_even_response", "response sector", "S_even=-int sqrt(-g)[Gamma_0+1/2 M_AB Z^A Z^B+1/2 H_AB nabla Z^A nabla Z^B+O(Z^4)]", "FORMAL_MECHANISM_FROM_3628_RETAINED"),
        ("PAC4117_3_matter_descent", "ordinary matter action", "S_matter depends on Phi_parent only through q(Phi_parent), no representative Weyl/disformal or hidden Z-linear spurion", "626_CRITERION_AVAILABLE_BUT_NOT_PARENT_SIGNED"),
        ("PAC4117_4_source_normalization", "measured mass/source current", "Pi_M,J_H,G_eff,M_eff and reference charge are q-data/fixed constants; Pi_M(Q_extra)=0", "CHARGE_CURRENT_ORTHOGONALITY_NOT_PARENT_DERIVED"),
        ("PAC4117_5_quadratic_activation", "domain/memory activation", "f(0)=f_prime(0)=0, e.g. norm-square/determinant/topological pairing", "SUFFICIENT_REQUIREMENT_KNOWN_PARENT_ORIGIN_MISSING"),
        ("PAC4117_6_boundary", "boundary and symplectic handoff", "boundary variation in Z direction is zero/fixed-reference: B_A=0 and no linked-surface preferred-frame/source flux", "BOUNDARY_NATURAL_SOURCE_NOT_SIGNED"),
        ("PAC4117_7_physical_flux", "Maxwell/Poynting/radiation stress", "physical flux fields enter S_phys_flux with own Hilbert stress/current; count as matter/EM stress, not hidden q_loc closure", "ACTION_POLICY_WRITTEN_EM_MAPPING_DEFERRED"),
    ]
    return [
        {
            **row_base(),
            "clause_id": clause_id,
            "object": obj,
            "mathematical_clause": clause,
            "current_status": status,
            "source_id": "SRC4117_03_3630_clause",
            "claim_allowed": bool_string(False),
            "valid_for_claim": bool_string(False),
        }
        for clause_id, obj, clause, status in rows
    ]


def theorem_rows() -> List[dict]:
    rows = [
        ("THM4117_0_define_source", "J_A=(1/sqrt(-g)) delta(S_matter+S_source+S_boundary)/delta Z^A |_{Z=0}", "J_A is the only linear obstruction to Z=0 after even response action", "DERIVED_FROM_3629"),
        ("THM4117_1_even_bulk", "delta S_even/delta Z^A|0=0 and delta T_GK/delta Z^A|0=0", "3628 F1=0 survives inside total parent action", "CONDITIONAL_PASS_FOR_RESPONSE_SECTOR"),
        ("THM4117_2_matter_descent", "delta_Z S_matter=(delta Sbar/delta q)Dq[e_A]delta Z^A=0", "J_A^matter=0 if Z is vertical and S_matter descends to Q_MTS", "VALID_THEOREM_STEP_PARENT_PREMISES_UNSIGNED"),
        ("THM4117_3_source_descent", "delta_Z S_source=0 when Pi_M and J_H are q-owned and extra charges orthogonal", "measured mass/source-normalization terms vanish before GM fitting", "VALID_THEOREM_STEP_CHARGE_CURRENT_PREMISES_UNSIGNED"),
        ("THM4117_4_quadratic_activation", "delta_Z[f(Z)L_mem]|0=f_prime(0)L_mem delta Z=0", "domain/memory coupling does not re-source local Z at first order", "VALID_THEOREM_STEP_PARENT_ORIGIN_UNSIGNED"),
        ("THM4117_5_boundary", "delta S_boundary|collar=int_boundary B_A delta Z^A; require B_A=0/fixed exact", "bulk J_A=0 promotes only if boundary Z-source/flux absent", "BOUNDARY_PREMISE_UNSIGNED"),
        ("THM4117_6_conclusion", "if THM4117_1..5 pass, then J_A=0 and L_AB Z^B+O(Z^2)=0; positive L_AB plus fixed boundary gives Z=0", "would derive local response plateau rather than assuming it", "CONDITIONAL_THEOREM_PROVED_CURRENT_CORPUS_NOT_SIGNED"),
    ]
    return [
        {
            **row_base(),
            "step_id": step_id,
            "formula": formula,
            "result": result,
            "status": status,
            "source_id": "SRC4117_04_3630_theorem",
            "claim_allowed": bool_string(False),
            "valid_for_claim": bool_string(False),
        }
        for step_id, formula, result, status in rows
    ]


def signature_audit_rows() -> List[dict]:
    rows = [
        ("SIG4117_0_q_map", "q:Phi_parent->Q_MTS parent-defined", "MISSING_PARENT_Q_MAP_IN_THIS_BRANCH", "blocks quotient-descent proof"),
        ("SIG4117_1_vertical_generator", "Z^A basis equals ker(Dq) vertical directions", "MISSING_DQ_VERTICAL_GENERATOR_MAP", "blocks delta_Z S_matter=0"),
        ("SIG4117_2_matter_descent", "S_matter=Sbar_matter[q(Phi),Psi,theta]", "NOT_SIGNED_FROM_626", "blocks J_A^matter zero and c_g zero"),
        ("SIG4117_3_source_descent", "Pi_M,J_H,M_eff,G_eff q-owned/source-current orthogonal", "NOT_PARENT_DERIVED", "blocks Newton/source-normalization claim"),
        ("SIG4117_4_quadratic_origin", "p>=2 activation follows from symmetry/norm/determinant/topology", "REQUIREMENT_DERIVED_ORIGIN_MISSING", "blocks selector/memory zero promotion"),
        ("SIG4117_5_boundary", "B_A=0 or fixed exact boundary with no local flux", "BOUNDARY_NATURAL_SOURCE_OPEN", "blocks alpha3/source flux silence"),
        ("SIG4117_6_Kmetric", "K_hat equals K_metric for chosen S_GK", "UNSIGNED_FROM_3628", "blocks Gamma/Khat parent ownership"),
        ("SIG4117_7_Z_physical", "Z^A equals physical q_loc/PPN/Newton/source residual vector", "MISSING_Z_TO_OBSERVABLE_MAP", "blocks using theorem as local-GR evidence"),
        ("SIG4117_8_verdict", "all parent-action signature clauses pass", "FAIL_CURRENT_CORPUS_NO_CLAIM", "requires 4118 vertical/q/source map or J_Z coefficients"),
    ]
    return [
        {
            **row_base(),
            "audit_id": audit_id,
            "required_signature": required,
            "current_status": status,
            "blocks": blocks,
            "source_id": "SRC4117_05_3630_signature",
            "claim_allowed": bool_string(False),
            "valid_for_claim": bool_string(False),
        }
        for audit_id, required, status, blocks in rows
    ]


def bound_requirement_rows() -> List[dict]:
    observables = [
        ("JZB4117_0_gamma", "R3_gamma", "gamma_minus_1"),
        ("JZB4117_1_beta", "R4_beta", "beta_minus_1"),
        ("JZB4117_2_preferred_frame", "R5_R6_R7_R8", "alpha1;alpha2;alpha3;xi"),
        ("JZB4117_3_Newton_source", "R10_R11_Newton", "delta_Newton_MTS;alpha(lambda);mu_extra"),
        ("JZB4117_4_clock", "R2_clock", "alpha_clock_redshift"),
        ("JZB4117_5_WEP_source", "R1_WEP_source_charge", "eta_source_AB"),
        ("JZB4117_6_Gdot", "R9_Gdot", "Gdot_over_G"),
        ("JZB4117_7_EM_flux", "ENV3625_5_EM_source", "w_EM;Phi_EM_boundary"),
        ("JZB4117_8_R11_operator", "R11_EH_operator_ledger", "non_EH_operator_coefficients"),
    ]
    return [
        {
            **row_base(),
            "bound_id": bound_id,
            "target_row": target,
            "observable": observable,
            "minimum_inputs": "MISSING_L_OPERATOR_NORM; MISSING_OBSERVABLE_PROJECTION; MISSING_BOUND_SOURCE_PATH",
            "score_status": "not_scoreable",
            "source_id": "SRC4117_06_3630_bounds",
            "claim_allowed": bool_string(False),
            "valid_for_claim": bool_string(False),
        }
        for bound_id, target, observable in observables
    ]


def decision_rows() -> List[dict]:
    rows = [
        ("DEC4117_0_theorem", "A single parent-action clause is now in the active spine and is mathematically sufficient for J_Z=0.", "CONDITIONAL_THEOREM_PROGRESS", "try to parent-map Z as vertical generator of q and prove matter/source descent"),
        ("DEC4117_1_current_ceiling", "Current corpus still cannot claim J_Z=0 because q, vertical generator, matter descent, source descent, boundary source, K_metric and Z-observable map are unsigned.", "NO_CLAIM", "do not promote local GR/Newton/PPN; keep bound rows active"),
        ("DEC4117_2_best_next", "Highest-leverage next step is vertical generator and Z-to-observable map, not another broad audit.", "NEXT_TARGET_SELECTED", "4118-Y5-R2FR-vertical-generator-Z-map-or-JZ-coefficient-runner.md"),
    ]
    return [
        {
            **row_base(),
            "decision_id": decision_id,
            "decision": decision,
            "status": status,
            "next_action": next_action,
            "claim_allowed": bool_string(False),
            "valid_for_claim": bool_string(False),
        }
        for decision_id, decision, status, next_action in rows
    ]


def next_target_rows() -> List[dict]:
    return [
        {
            **row_base(),
            "next_id": "NEXT4117_0",
            "target_doc": "4118-Y5-R2FR-vertical-generator-Z-map-or-JZ-coefficient-runner.md",
            "target_script": "scripts/Y5_R2FR_4118_vertical_generator_Z_map_or_JZ_coefficient_runner.py",
            "objective": "map Z^A/DCdagger-like local residual coordinates to actual parent quotient vertical generators e_A in ker(Dq), then map Z^A to q_loc/PPN/Newton/source observables; if either map fails, prepare J_Z coefficients for scoring",
            "success_gate": "Dq[e_A]=0 is parent-signed, Z^A is the physical local residual coordinate, and delta_Z S_matter/source can be evaluated; otherwise each observable receives an explicit J_Z coefficient row",
            "reason": "4117 proves the theorem conditionally; the first unsigned premise is the vertical generator and physical residual map.",
            "claim_allowed": bool_string(False),
            "valid_for_claim": bool_string(False),
        }
    ]


def status_rows() -> List[dict]:
    return [
        {
            **row_base(),
            "status_id": "STATUS4117_0",
            "decision": DECISION,
            "strongest_result": "4117 imports the sufficient parent-action theorem for J_Z=0 into the active spine: Z must be vertical to q, matter/source/boundary terms must descend to q or enter even/quadratic, extra source charges must be orthogonal, and boundary natural sources must vanish.",
            "what_changed": "The coupling zero is now a single parent-action signature target rather than disconnected closure wishes. It is mathematically enough, but not parent-signed.",
            "still_missing": "parent q map, Dq vertical generator, matter/source descent, p>=2 origin, boundary no-flux, K_hat=K_metric and Z-to-observable map",
            "claim_state": "no JZ_zero_local_GR_Newton_PPN_R10_R11_WEP_clock_Gdot_EM_source claim",
            "next_target": "4118 vertical generator Z map or JZ coefficient runner",
            "claim_allowed": bool_string(False),
            "valid_for_claim": bool_string(False),
        }
    ]


def generated_outputs() -> Dict[str, Path]:
    return {
        "P8_Y5_R2FR_4117_SOURCE_REGISTER": SOURCE_DIR / "P8_Y5_R2FR_4117_SOURCE_REGISTER.csv",
        "P8_Y5_R2FR_4117_PARENT_ACTION_CLAUSE": SOURCE_DIR / "P8_Y5_R2FR_4117_PARENT_ACTION_CLAUSE.csv",
        "P8_Y5_R2FR_4117_JZ_ZERO_THEOREM": SOURCE_DIR / "P8_Y5_R2FR_4117_JZ_ZERO_THEOREM.csv",
        "P8_Y5_R2FR_4117_PARENT_SIGNATURE_AUDIT": SOURCE_DIR / "P8_Y5_R2FR_4117_PARENT_SIGNATURE_AUDIT.csv",
        "P8_Y5_R2FR_4117_JZ_BOUND_REQUIREMENTS": SOURCE_DIR / "P8_Y5_R2FR_4117_JZ_BOUND_REQUIREMENTS.csv",
        "P8_Y5_R2FR_4117_DECISION_GATE": SOURCE_DIR / "P8_Y5_R2FR_4117_DECISION_GATE.csv",
        "P8_Y5_R2FR_4117_NEXT_TARGET": SOURCE_DIR / "P8_Y5_R2FR_4117_NEXT_TARGET.csv",
        "P8_Y5_R2FR_4117_STATUS": SOURCE_DIR / "P8_Y5_R2FR_4117_STATUS.csv",
    }


def markdown_table(rows: List[dict], columns: List[str]) -> str:
    lines = ["| " + " | ".join(columns) + " |", "| " + " | ".join("---" for _ in columns) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(column, "")).replace("\n", " ") for column in columns) + " |")
    return "\n".join(lines)


def write_doc() -> None:
    status = status_rows()[0]
    lines = [
        "# 4117 - parent-action total evenness quotient descent or J_Z bound runner",
        "",
        "## Verdict",
        "4117 imports the `3630` parent-action theorem into the active `411x` spine. The theorem is strong and clean: if `Z` is vertical to the quotient and all non-response terms descend to `q` or enter even/quadratic with zero boundary natural source, then `J_Z=0` follows.",
        "",
        "This is still not a claim. The current corpus has the theorem target, not the signed parent maps.",
        "",
        "## Strongest Current Result",
        f"- `{status['decision']}`",
        f"- {status['strongest_result']}",
        f"- {status['what_changed']}",
        "",
        "## Parent-Action Clause",
        markdown_table(parent_action_clause_rows(), ["clause_id", "object", "mathematical_clause", "current_status"]),
        "",
        "## J_Z Zero Theorem",
        markdown_table(theorem_rows(), ["step_id", "formula", "result", "status"]),
        "",
        "## Parent-Signature Audit",
        markdown_table(signature_audit_rows(), ["audit_id", "required_signature", "current_status", "blocks"]),
        "",
        "## Bound Requirements If Theorem Fails",
        markdown_table(bound_requirement_rows(), ["bound_id", "target_row", "observable", "minimum_inputs", "score_status"]),
        "",
        "## Decisions",
        markdown_table(decision_rows(), ["decision_id", "decision", "status", "next_action"]),
        "",
        "## Next Target",
        markdown_table(next_target_rows(), ["target_doc", "target_script", "objective", "success_gate"]),
        "",
    ]
    DOC_PATH.write_text("\n".join(lines), encoding="utf-8")


def write_outputs() -> Dict[str, Path]:
    outputs = generated_outputs()
    write_csv(outputs["P8_Y5_R2FR_4117_SOURCE_REGISTER"], source_register_rows())
    write_csv(outputs["P8_Y5_R2FR_4117_PARENT_ACTION_CLAUSE"], parent_action_clause_rows())
    write_csv(outputs["P8_Y5_R2FR_4117_JZ_ZERO_THEOREM"], theorem_rows())
    write_csv(outputs["P8_Y5_R2FR_4117_PARENT_SIGNATURE_AUDIT"], signature_audit_rows())
    write_csv(outputs["P8_Y5_R2FR_4117_JZ_BOUND_REQUIREMENTS"], bound_requirement_rows())
    write_csv(outputs["P8_Y5_R2FR_4117_DECISION_GATE"], decision_rows())
    write_csv(outputs["P8_Y5_R2FR_4117_NEXT_TARGET"], next_target_rows())
    write_csv(outputs["P8_Y5_R2FR_4117_STATUS"], status_rows())
    write_doc()
    return outputs


def validate(outputs: Dict[str, Path]) -> List[dict]:
    checks: List[dict] = []

    def add(check_id: str, check: str, passed: bool, detail: str) -> None:
        checks.append({**row_base(), "check_id": check_id, "check": check, "passed": bool_string(passed), "detail": detail, "claim_allowed": bool_string(False)})

    missing_sources = [source_id for source_id, (path, _, _) in LOCAL_SOURCES.items() if not path.exists()]
    missing_needles = []
    for source_id, (path, needle, _) in LOCAL_SOURCES.items():
        if path.exists() and needle not in read_text(path):
            missing_needles.append(f"{source_id}:{needle}")
    add("VAL4117_0_sources_exist", "every local source path exists", not missing_sources, ";".join(missing_sources) or "all sources exist")
    add("VAL4117_1_sources_contain_needles", "every local source contains expected needle", not missing_needles, ";".join(missing_needles) or "all needles found")

    parse_ok = True
    parse_counts = {}
    for key, path in outputs.items():
        try:
            rows = parse_csv(path)
            parse_counts[key] = len(rows)
            parse_ok = parse_ok and len(rows) > 0
        except Exception as exc:
            parse_ok = False
            parse_counts[key] = repr(exc)
    add("VAL4117_2_csv_parse", "all generated CSV outputs parse and are nonempty", parse_ok, str(parse_counts))

    clause_text = " ".join(" ".join(row.values()) for row in parse_csv(outputs["P8_Y5_R2FR_4117_PARENT_ACTION_CLAUSE"]))
    clause_ok = all(token in clause_text for token in ["Dq[e_A]=0", "S_even", "S_matter", "S_source", "S_boundary"])
    add("VAL4117_3_clause", "parent-action clause includes vertical/even/source/boundary pieces", clause_ok, "clause tokens checked")

    theorem_text = " ".join(" ".join(row.values()) for row in parse_csv(outputs["P8_Y5_R2FR_4117_JZ_ZERO_THEOREM"]))
    theorem_ok = all(token in theorem_text for token in ["J_A", "Dq[e_A]", "J_A^matter=0", "CONDITIONAL_THEOREM"])
    add("VAL4117_4_theorem", "J_Z zero theorem is present and conditional", theorem_ok, "theorem tokens checked")

    audit_text = " ".join(" ".join(row.values()) for row in parse_csv(outputs["P8_Y5_R2FR_4117_PARENT_SIGNATURE_AUDIT"]))
    audit_ok = all(token in audit_text for token in ["MISSING_PARENT_Q_MAP", "MISSING_DQ_VERTICAL_GENERATOR_MAP", "FAIL_CURRENT_CORPUS_NO_CLAIM"])
    add("VAL4117_5_signature_audit", "parent-signature audit blocks current claim", audit_ok, "audit tokens checked")

    bound_text = " ".join(" ".join(row.values()) for row in parse_csv(outputs["P8_Y5_R2FR_4117_JZ_BOUND_REQUIREMENTS"]))
    bound_ok = all(token in bound_text for token in ["gamma_minus_1", "beta_minus_1", "Gdot_over_G", "non_EH_operator_coefficients"])
    add("VAL4117_6_bound_requirements", "J_Z bound requirements cover local arenas", bound_ok, "bound tokens checked")

    next_rows = parse_csv(outputs["P8_Y5_R2FR_4117_NEXT_TARGET"])
    next_ok = len(next_rows) == 1 and next_rows[0].get("target_doc") == "4118-Y5-R2FR-vertical-generator-Z-map-or-JZ-coefficient-runner.md"
    add("VAL4117_7_next_target", "next target is 4118 vertical generator Z map", next_ok, str(next_rows))

    status_rows_local = parse_csv(outputs["P8_Y5_R2FR_4117_STATUS"])
    status_ok = bool(status_rows_local) and status_rows_local[0].get("decision") == DECISION and "no JZ" in status_rows_local[0].get("claim_state", "")
    add("VAL4117_8_status", "status records parent theorem and no-claim state", status_ok, "status row checked")

    all_rows = []
    for path in outputs.values():
        all_rows.extend(parse_csv(path))
    no_claim = all(row.get("claim_allowed") in ("False", "") for row in all_rows)
    add("VAL4117_9_no_claim_flags", "all generated rows remain no-claim", no_claim, f"row_count={len(all_rows)}")

    output_paths = list(outputs.values()) + [DOC_PATH]
    in_scope = all(is_under(path, ROOT) for path in output_paths)
    formalization_output = any(is_under(path, FORMALIZATION) for path in output_paths)
    formalization_touched = False
    if FORMALIZATION.exists():
        formalization_touched = any(FORMALIZATION.rglob("*R2FR_4117*")) or any(FORMALIZATION.rglob("4117-Y5-R2FR*"))
    add("VAL4117_10_scope", "outputs stay in post-checkpoint-work and not formalization-workbench", in_scope and not formalization_output and not formalization_touched, f"doc={DOC_PATH}; csv_count={len(outputs)}")

    compile_ok = True
    compile_detail = "py_compile ok"
    try:
        py_compile.compile(str(SCRIPT_PATH), doraise=True)
    except Exception as exc:
        compile_ok = False
        compile_detail = repr(exc)
    add("VAL4117_11_compile", "generator script compiles", compile_ok, compile_detail)
    return checks


def main() -> None:
    outputs = write_outputs()
    validation_rows = validate(outputs)
    validation_path = SOURCE_DIR / "P8_Y5_BRR545_4117_VALIDATION.csv"
    write_csv(validation_path, validation_rows)
    pycache = SCRIPT_PATH.parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)

    failed = [row for row in validation_rows if row["passed"] != "True"]
    print(f"wrote: {DOC_PATH}")
    for path in outputs.values():
        print(f"wrote: {path}")
    print(f"validation: {validation_path}")
    if failed:
        print("failed checks:")
        for row in failed:
            print(f"- {row['check_id']}: {row['detail']}")
        raise SystemExit(1)
    print("all validation checks passed")


if __name__ == "__main__":
    main()
