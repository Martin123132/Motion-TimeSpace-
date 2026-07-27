from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


BRANCH_ID = "MTS_R2FR_NO_PHYSICAL_Q_POLE_THEOREM_OR_BOUNDED_BETA_RUNNER_2426"
CHECKPOINT_ID = "2426"

ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = ROOT.parent
FORMALIZATION = PROJECT_ROOT / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
MICROSCOPE = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
BETA_DOCS = ROOT / "source-intake" / "beta-source" / "docs"

DOC = ROOT / "2426-Y5-R2FR-no-physical-q-pole-theorem-or-bounded-beta-runner.md"

OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_2426_SOURCE_REGISTER.csv",
    "no_pole": OUT / "P8_Y5_PARENT_QLOC_2426_NO_PHYSICAL_Q_POLE_AUDIT.csv",
    "countermodels": OUT / "P8_Y5_PARENT_QLOC_2426_POLE_COUNTERMODEL_LEDGER.csv",
    "bounded_beta": OUT / "P8_Y5_PARENT_QLOC_2426_BOUNDED_BETA_SOURCE_TEST_TEMPLATE.csv",
    "tail_policy": OUT / "P8_Y5_PARENT_QLOC_2426_NO_CANCELLATION_TAIL_POLICY.csv",
    "claim_gates": OUT / "P8_Y5_PARENT_QLOC_2426_CLAIM_GATES.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_2426_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_2426_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_PARENT_QLOC_2426_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2426_VALIDATION.csv",
}

COPY_TARGETS = {
    "queue": QUEUE / "JR2426_NO_PHYSICAL_Q_POLE_OR_BETA_BOUND_NONCLAIM.csv",
    "branch_wep": MICROSCOPE / "P8_Y5_PARENT_QLOC_2426_LOCAL_GR_REFUSAL_NONCLAIM.csv",
    "beta_docs": BETA_DOCS / "PARENT_QLOC_NO_POLE_OR_BETA_BOUND_2426_NONCLAIM.csv",
}

SOURCES = [
    {
        "source_id": "SRC2426_00_2425_handoff",
        "source_path": ROOT / "2425-Y5-R2FR-parent-finite-quadratic-q-row-and-source-test-coupling-split.md",
        "needles": ["NEXT2425_0_selected", "FORK2425_0_no_physical_q_pole", "VAL2425_OVERALL"],
        "role": "current handoff selecting no-physical-q-pole or bounded beta runner",
    },
    {
        "source_id": "SRC2426_01_2292_prior_runner",
        "source_path": ROOT / "2292-Y5-R2FR-no-physical-q-pole-theorem-or-bounded-beta-runner.md",
        "needles": ["NPQ2292_6_verdict", "BB2292_7_beta_product_guard", "VAL2292_OVERALL"],
        "role": "prior q/R_AB no-pole and bounded-beta runner",
    },
    {
        "source_id": "SRC2426_02_2244_no_pole",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_2244_NO_PHYSICAL_RAB_POLE_AUDIT.csv",
        "needles": ["NPR2244_3_boundary_silence", "NPR2244_6_verdict"],
        "role": "R_AB no-pole audit: boundary charge and generator package remain open",
    },
    {
        "source_id": "SRC2426_03_2244_beta_template",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_2244_BOUNDED_BETA_SOURCE_TEST_TEMPLATE.csv",
        "needles": ["BB2244_0_beta_source_geom", "BB2244_7_beta_product_guard"],
        "role": "bounded beta source/test fallback schema",
    },
    {
        "source_id": "SRC2426_04_1037_generic_no_pole",
        "source_path": OUT / "P8_Y5_R10_1037_NO_PHYSICAL_X_POLE_AUDIT.csv",
        "needles": ["NP1037_3_boundary_silence", "NP1037_6_verdict"],
        "role": "generic no-physical-X-pole audit confirming boundary charge as common obstruction",
    },
]


def timestamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def base_row(**kwargs: Any) -> dict[str, Any]:
    row = {
        "timestamp_utc": timestamp(),
        "branch_id": BRANCH_ID,
        "checkpoint_id": CHECKPOINT_ID,
        "valid_for_claim": False,
        "claim_allowed": False,
    }
    row.update(kwargs)
    return row


def stringify(value: Any) -> str:
    if isinstance(value, bool):
        return "True" if value else "False"
    return str(value)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({key: stringify(row.get(key, "")) for key in fields})


def csv_parses(path: Path) -> tuple[bool, int, str]:
    try:
        with path.open(newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
        return True, len(rows), "OK"
    except Exception as exc:
        return False, 0, f"{type(exc).__name__}: {exc}"


def table(headers: list[str], rows: list[dict[str, Any]]) -> str:
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        cells = [stringify(row.get(header, "")).replace("\n", " ").replace("|", "\\|") for header in headers]
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source in SOURCES:
        path = Path(source["source_path"])
        text = read_text(path)
        needles = source["needles"]
        found = [needle for needle in needles if needle in text]
        rows.append(
            base_row(
                source_id=source["source_id"],
                source_path=path,
                path_exists=path.exists(),
                required_needles="; ".join(needles),
                found_needles="; ".join(found),
                needles_found=path.exists() and len(found) == len(needles),
                role=source["role"],
            )
        )
    return rows


def no_pole_rows() -> list[dict[str, Any]]:
    return [
        base_row(audit_id="NPQ2426_0_q_kernel", criterion="q is quotient/kernel data", mathematical_test="Dq[v_q]=0 and q is parent-defined before variation", result="PARTIAL_MATH_ONLY_NOT_PARENT_SIGNED", if_missing="q can still be physical residual rather than representative choice"),
        base_row(audit_id="NPQ2426_1_action_descent", criterion="bulk action descends through quotient", mathematical_test="S_bulk[Phi]=S_red[q(Phi)] so H(v_q,.)=0 and no vertical Green operator exists", result="CONDITIONAL_DESCENT_NOT_SIGNED", if_missing="finite Hessian block can survive"),
        base_row(audit_id="NPQ2426_2_constraint_generator", criterion="vertical q generated by first-class differentiable constraint", mathematical_test="delta G_q=Omega(delta Phi,v_q), G_q=int epsilon C_q+Q_q, brackets close", result="MISSING_PARENT_OMEGA_DCQ_VERTICAL_GENERATOR", if_missing="zero Hessian can hide edge/second-class remnants"),
        base_row(audit_id="NPQ2426_3_boundary_silence", criterion="vertical transformations carry no local boundary charge", mathematical_test="Q_q=0/exact/proper and K_boundary=0 for compact local vertical transformations", result="MISSING_BOUNDARY_CHARGE_ZERO", if_missing="q reappears as edge hair or source charge"),
        base_row(audit_id="NPQ2426_4_degree_count", criterion="constraints remove local q pair", mathematical_test="first-class pair removes q and reduced Omega has no proper q stabilizer", result="MISSING_DEGREE_COUNT", if_missing="no-pole cannot be distinguished from under-specified dynamics"),
        base_row(audit_id="NPQ2426_5_matter_readout", criterion="ordinary matter/readout descends and no marker sees q", mathematical_test="S_matter=Sbar[Obs(q(Phi)),psi,theta] and Lie_vq theta=0", result="MISSING_MATTER_NO_MARKER_SIGNATURE", if_missing="beta_source/beta_test rows remain live even if bulk pole is controlled"),
        base_row(audit_id="NPQ2426_6_verdict", criterion="no physical local q pole in GR/Newton branch", mathematical_test="NPQ2426_0 through NPQ2426_5 all close from one parent action and boundary prescription", result="FAIL_CURRENT_CLAIM_NO_POLE_NOT_PROVED", if_missing="build bounded beta_source/beta_test runner and retain no-cancellation tails"),
    ]


def countermodel_rows() -> list[dict[str, Any]]:
    return [
        base_row(counter_id="PCM2426_0_edge_mode", surviving_channel="proper boundary charge Q_q", why_it_survives="constraint generator may have nonzero differentiable boundary term", consequence="R10/source charge can be edge-owned, not bulk-owned"),
        base_row(counter_id="PCM2426_1_second_class_remnant", surviving_channel="algebraic second-class q remnant", why_it_survives="no degree-count proof removing q pair", consequence="q can be finite residual even without free propagation"),
        base_row(counter_id="PCM2426_2_shadow_frame", surviving_channel="universal Weyl/disformal frame leakage", why_it_survives="matter/readout may depend on q through observed frame", consequence="beta_source=beta_test=c_g style leakage gives c_g^2 exchange"),
        base_row(counter_id="PCM2426_3_marker_constants", surviving_channel="mass/EM/material marker dependence", why_it_survives="no-marker theorem unsigned", consequence="WEP/clock/composition constraints couple to beta rows"),
        base_row(counter_id="PCM2426_4_nonhilbert_support", surviving_channel="boundary/domain/non-Hilbert source current", why_it_survives="source-worldtube support and Hilbert equality not proven", consequence="source normalization and orbital/local-GR rows remain live"),
    ]


def bounded_beta_rows() -> list[dict[str, Any]]:
    return [
        base_row(beta_id="BB2426_0_beta_source_geom", leg="source", symbol="beta_s_geom", definition="source-body q charge from common Weyl/disformal observed-frame leakage", formula_or_bound="|beta_s_geom| <= |profile_s^W c_g| + |profile_s^dis b_dis|", current_status="MISSING_FRAME_LEAK_ZERO_OR_NUMERIC_BOUND", observable_links="R10;PPN;WEP;clock", score_ready=False),
        base_row(beta_id="BB2426_1_beta_test_geom", leg="test", symbol="beta_t_geom", definition="test/readout q charge from common Weyl/disformal observed-frame leakage", formula_or_bound="|beta_t_geom| <= |tau_R10 c_g| + |tau_dis b_dis|", current_status="MISSING_ARENA_PROJECTION", observable_links="R10;PPN;WEP;clock", score_ready=False),
        base_row(beta_id="BB2426_2_beta_source_marker", leg="source", symbol="beta_s_marker", definition="source material/EM marker q charge", formula_or_bound="|beta_s_marker| <= sum_A |S_sA b_A| + |S_salpha b_alpha|", current_status="MISSING_NO_MARKER_THEOREM_OR_NUMERIC_BOUNDS", observable_links="WEP;clock;composition;R10", score_ready=False),
        base_row(beta_id="BB2426_3_beta_test_marker", leg="test", symbol="beta_t_marker", definition="test/readout material marker q charge", formula_or_bound="|beta_t_marker| <= sum_A |S_tA b_A| + |S_talpha b_alpha|", current_status="MISSING_MARKER_READOUT_PROJECTION", observable_links="WEP;clock;composition;R10", score_ready=False),
        base_row(beta_id="BB2426_4_beta_source_nonH", leg="source", symbol="beta_s_nonH", definition="source-side non-Hilbert/boundary/domain/support q current", formula_or_bound="|beta_s_nonH| <= |q_nonH_s| + |Delta_W_support_s| + |q_domain_s| + |q_boundary_s|", current_status="MISSING_HIDDEN_SOURCE_ZERO_OR_NUMERIC_BOUND", observable_links="R10;orbital;source_normalization;local_GR", score_ready=False),
        base_row(beta_id="BB2426_5_beta_test_nonH", leg="test", symbol="beta_t_nonH", definition="test/readout-side non-Hilbert/boundary/domain/support q current", formula_or_bound="|beta_t_nonH| <= |q_nonH_t| + |Delta_W_support_t| + |q_domain_t| + |q_boundary_t|", current_status="MISSING_HIDDEN_TEST_ZERO_OR_NUMERIC_BOUND", observable_links="R10;orbital;source_normalization;local_GR", score_ready=False),
        base_row(beta_id="BB2426_6_beta_abs_totals", leg="source_and_test", symbol="beta_s_abs;beta_t_abs", definition="absolute no-cancellation source/test beta envelopes", formula_or_bound="beta_s_abs=sum_i |beta_s_i|; beta_t_abs=sum_i |beta_t_i|", current_status="SCHEMA_READY_VALUES_MISSING", observable_links="all_local_arenas", score_ready=False),
        base_row(beta_id="BB2426_7_beta_product_guard", leg="source_times_test", symbol="abs_beta_product", definition="claim-safe source-test product for finite exchange", formula_or_bound="|beta_s beta_t| <= beta_s_abs beta_t_abs; universal Weyl gives c_g^2 contribution", current_status="CLAIM_BLOCKED", observable_links="R10;PPN;WEP;clock;orbital", score_ready=False),
    ]


def tail_policy_rows() -> list[dict[str, Any]]:
    return [
        base_row(policy_id="TAIL2426_0_absolute_components", policy="unknown components add in absolute value", reason="no cancellation credit between c_g,b_dis,b_A,b_alpha,q_nonH,boundary/support", status="POLICY_ACTIVE"),
        base_row(policy_id="TAIL2426_1_cg_squared", policy="universal Weyl source/test branch contributes c_g^2", reason="same coupling appears on source and test legs unless Qbar contains one leg explicitly", status="POLICY_ACTIVE"),
        base_row(policy_id="TAIL2426_2_R10_score_gate", policy="score only numeric sourced alpha_q(lambda) against numeric sourced alpha_bound(lambda)", reason="no bounds-as-coefficients and no placeholder beta rows", status="CLAIM_BLOCKED"),
        base_row(policy_id="TAIL2426_3_cross_arena", policy="R10 beta rows must cross-check WEP/clock/PPN/orbital leakage", reason="finite q coupling to matter/readout cannot be hidden in one arena", status="POLICY_ACTIVE"),
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        base_row(gate_id="CG2426_0_no_pole", gate="finite local q mode has no physical pole", passed=False, reason="Omega/DCq generator, boundary charge, degree count and matter/no-marker descent incomplete"),
        base_row(gate_id="CG2426_1_alpha_zero", gate="R10 alpha_q=0 locally", passed=False, reason="no-pole and tail-zero clauses are not parent-signed"),
        base_row(gate_id="CG2426_2_bounded_beta", gate="bounded beta_source/beta_test rows are score-ready", passed=False, reason="all beta components still need theorem-zero or numeric/source-backed bounds"),
        base_row(gate_id="CG2426_3_linear_cg", gate="linear c_g can be scored against R10", passed=False, reason="universal source/test branch contributes c_g squared"),
        base_row(gate_id="CG2426_4_local_GR_Newton", gate="local GR/Newton recovery is derived", passed=False, reason="no-pole route failed current-claim status and beta fallback is schema-only"),
        base_row(gate_id="CG2426_5_public", gate="GitHub/public claim allowed", passed=False, reason="private nonclaim checkpoint"),
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        base_row(decision_id="DEC2426_0_no_pole_status", decision="NO_POLE_ROUTE_SHARP_BUT_NOT_PROVED", rationale="parent Omega/DCq, boundary charge, degree count, and matter/no-marker descent must close together", consequence="do not claim alpha=0 or local GR"),
        base_row(decision_id="DEC2426_1_sharp_blocker", decision="BOUNDARY_CHARGE_COCYCLE_IS_NEXT_HINGE", rationale="Q_q/K_boundary decides whether vertical q is pure gauge/constraint or an edge/source charge", consequence="attack boundary charge before broad coupling hunts"),
        base_row(decision_id="DEC2426_2_beta_fallback", decision="BOUNDED_BETA_FALLBACK_READY_AS_SCHEMA", rationale="if a physical pole/edge survives, local tests see beta_source beta_test plus absolute tails", consequence="fill theorem-zero or numeric source-backed beta rows one by one"),
        base_row(decision_id="DEC2426_3_cg_policy", decision="LINEAR_CG_REMAINS_QUARANTINED", rationale="source-test exchange needs both legs", consequence="future candidate rows must declare beta_source beta_test or Qbar source-leg ownership"),
        base_row(decision_id="DEC2426_4_claim_policy", decision="KEEP_PRIVATE_NONCLAIM", rationale="no score-ready local/R10 prediction", consequence="no GitHub action"),
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            route_id="NEXT2426_0_selected",
            selection_status="selected",
            target_file="2427-Y5-R2FR-boundary-charge-Qq-Kboundary-zero-or-beta-bound-first-row.md",
            target_script="scripts/Y5_R2FR_boundary_charge_Qq_Kboundary_zero_or_beta_bound_first_row_2427.py",
            objective="try to compute or prove silence of Q_q and K_boundary for the local q vertical branch; if this fails, fill the first source-backed beta projection row without claiming a pass",
            success_condition="boundary generator is exact/proper/zero with closed cocycle, or first beta source/test bound row becomes source-ready nonclaim with units and no-cancellation policy",
            do_not_do="do not invent parent action terms, score naked linear c_g, cancel beta tails, claim R10/local-GR pass, edit formalization-workbench, or push GitHub",
        )
    ]


def copy_branch_rows(no_pole: list[dict[str, Any]], bounded_beta: list[dict[str, Any]], decision_ledger: list[dict[str, Any]]) -> list[dict[str, Any]]:
    copy_specs = [
        ("queue", OUTPUTS["no_pole"], COPY_TARGETS["queue"], no_pole),
        ("branch_wep", OUTPUTS["bounded_beta"], COPY_TARGETS["branch_wep"], bounded_beta),
        ("beta_docs", OUTPUTS["decision"], COPY_TARGETS["beta_docs"], decision_ledger),
    ]
    rows: list[dict[str, Any]] = []
    for copy_id, source_path, target_path, copied_rows in copy_specs:
        write_csv(target_path, copied_rows)
        rows.append(
            base_row(
                copy_id=f"BC2426_{copy_id}",
                source_path=source_path,
                target_path=target_path,
                target_exists=target_path.exists(),
                row_count=len(copied_rows),
                purpose="no-pole or bounded-beta nonclaim handoff",
            )
        )
    return rows


def formalization_has_2426_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    patterns = (
        "*2426-Y5-R2FR*",
        "*P8_Y5_PARENT_QLOC_2426*",
        "*P8_Y5_BRR545_2426*",
        "*Y5_R2FR_no_physical_q_pole_theorem_or_bounded_beta_runner_2426*",
        "*JR2426*",
        "*PARENT_QLOC_NO_POLE_OR_BETA_BOUND_2426*",
    )
    return any(path.is_file() for pattern in patterns for path in FORMALIZATION.rglob(pattern))


def remove_pycache() -> None:
    cache = ROOT / "scripts" / "__pycache__"
    if cache.exists():
        shutil.rmtree(cache)


def flags_safe(rows_by_name: dict[str, list[dict[str, Any]]]) -> bool:
    for rows in rows_by_name.values():
        for row in rows:
            for key in ("valid_for_claim", "claim_allowed", "score_ready", "passed"):
                value = row.get(key)
                if value is True or stringify(value).lower() == "true":
                    return False
    return True


def build_validation_rows(rows_by_name: dict[str, list[dict[str, Any]]], branch_copy_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    source_rows = rows_by_name["source_register"]
    no_pole = rows_by_name["no_pole"]
    beta = rows_by_name["bounded_beta"]
    tail = rows_by_name["tail_policy"]
    next_rows = rows_by_name["next_target"]

    csv_results = []
    for name, path in OUTPUTS.items():
        if name == "validation":
            continue
        parses, row_count, message = csv_parses(path)
        csv_results.append((name, parses, row_count, message))
    for copy_key, copy_path in COPY_TARGETS.items():
        parses, row_count, message = csv_parses(copy_path)
        csv_results.append((f"copy_{copy_key}", parses, row_count, message))

    checks = [
        ("VAL2426_SOURCES_EXIST", all(row["path_exists"] for row in source_rows), "all cited source paths exist"),
        ("VAL2426_NEEDLES_FOUND", all(row["needles_found"] for row in source_rows), "all source needles found"),
        ("VAL2426_NO_POLE_NOT_PROVED", any(row["audit_id"] == "NPQ2426_6_verdict" and "NOT_PROVED" in row["result"] for row in no_pole), "no physical q pole theorem remains unproved"),
        ("VAL2426_BOUNDARY_BLOCKER", any(row["audit_id"] == "NPQ2426_3_boundary_silence" and "BOUNDARY_CHARGE" in row["result"] for row in no_pole), "boundary charge zero is identified as blocker"),
        ("VAL2426_BETA_TEMPLATE", any(row["beta_id"] == "BB2426_7_beta_product_guard" and "c_g^2" in row["formula_or_bound"] for row in beta), "bounded beta product guard includes c_g^2"),
        ("VAL2426_TAIL_POLICY", any(row["policy_id"] == "TAIL2426_0_absolute_components" and row["status"] == "POLICY_ACTIVE" for row in tail), "absolute no-cancellation tail policy active"),
        ("VAL2426_NEXT_SELECTED", any(row["route_id"] == "NEXT2426_0_selected" and "boundary-charge" in row["target_file"] for row in next_rows), "boundary charge or beta-bound first row selected next"),
        ("VAL2426_FLAGS_SAFE", flags_safe(rows_by_name), "no claim/score flags are true"),
        ("VAL2426_BRANCH_COPIES", all(row["target_exists"] for row in branch_copy_rows), "branch copy files written"),
        ("VAL2426_CSV_PARSE", all(item[1] and item[2] > 0 for item in csv_results), "all generated CSV and branch copies parse with rows"),
        ("VAL2426_NO_FORMALIZATION_OUTPUT", not formalization_has_2426_artifacts(), "no 2426 artifacts written into formalization-workbench"),
    ]

    rows = [
        base_row(
            validation_id=validation_id,
            status="PASS" if passed else "FAIL",
            detail=detail,
            fatal=not passed,
        )
        for validation_id, passed, detail in checks
    ]
    overall_passed = all(row["status"] == "PASS" for row in rows)
    rows.append(
        base_row(
            validation_id="VAL2426_OVERALL",
            status="PASS" if overall_passed else "FAIL",
            detail="2426 refuses no-physical-q-pole claim, stages bounded beta rows with no-cancellation tails, and selects boundary charge Qq/Kboundary or beta-bound first row next",
            fatal=not overall_passed,
        )
    )
    return rows


def write_document(rows_by_name: dict[str, list[dict[str, Any]]], validation_rows: list[dict[str, Any]]) -> None:
    content = f"""# 2426 Y5 R2FR No Physical q Pole Theorem Or Bounded Beta Runner

## Result

2426 tries the cleanest GR-reduction route: prove the finite local `q/R_AB` residual has no physical exchange pole in the GR/Newton branch. Current evidence does **not** prove it.

The failure is useful and sharp. The blocker is not vibes; it is the parent generator package: `Omega`, `D C_q`, a differentiable vertical generator, boundary charge `Q_q`, cocycle `K_boundary`, degree count, and matter/no-marker descent must close together. Since they do not, the fallback is a bounded `beta_source/beta_test` runner with absolute no-cancellation tails and the `c_g^2` source/test rule preserved.

## Practical Status

- **No-pole route:** best structural route, but not proved.
- **Sharp blocker:** boundary charge/cocycle package `Q_q, K_boundary` plus parent `Omega/D C_q`.
- **Fallback:** bounded beta rows are schema-ready but not score-ready.
- **Claim discipline:** no alpha-zero, R10, local-GR, Newton, PPN, WEP, clock, or orbital pass.
- **Next target:** boundary charge silence or first real beta-bound row.

## Source Register

{table(["source_id", "source_path", "path_exists", "needles_found", "role"], rows_by_name["source_register"])}

## No Physical q Pole Audit

{table(["audit_id", "criterion", "mathematical_test", "result", "if_missing"], rows_by_name["no_pole"])}

## Pole Countermodel Ledger

{table(["counter_id", "surviving_channel", "why_it_survives", "consequence"], rows_by_name["countermodels"])}

## Bounded Beta Source/Test Template

{table(["beta_id", "leg", "symbol", "definition", "formula_or_bound", "current_status", "observable_links", "score_ready"], rows_by_name["bounded_beta"])}

## No-Cancellation Tail Policy

{table(["policy_id", "policy", "reason", "status"], rows_by_name["tail_policy"])}

## Claim Gates

{table(["gate_id", "gate", "passed", "reason"], rows_by_name["claim_gates"])}

## Decision Ledger

{table(["decision_id", "decision", "rationale", "consequence"], rows_by_name["decision"])}

## Next Target

{table(["route_id", "selection_status", "target_file", "target_script", "objective", "success_condition", "do_not_do"], rows_by_name["next_target"])}

## Validation

{table(["validation_id", "status", "detail", "fatal"], validation_rows)}
"""
    DOC.write_text(content, encoding="utf-8")


def main() -> None:
    rows_by_name = {
        "source_register": source_register_rows(),
        "no_pole": no_pole_rows(),
        "countermodels": countermodel_rows(),
        "bounded_beta": bounded_beta_rows(),
        "tail_policy": tail_policy_rows(),
        "claim_gates": claim_gate_rows(),
        "decision": decision_rows(),
        "next_target": next_target_rows(),
    }
    for name, rows in rows_by_name.items():
        write_csv(OUTPUTS[name], rows)

    branch_copy_rows = copy_branch_rows(
        rows_by_name["no_pole"],
        rows_by_name["bounded_beta"],
        rows_by_name["decision"],
    )
    rows_by_name["branch_copies"] = branch_copy_rows
    write_csv(OUTPUTS["branch_copies"], branch_copy_rows)

    validation_rows = build_validation_rows(rows_by_name, branch_copy_rows)
    write_csv(OUTPUTS["validation"], validation_rows)
    write_document(rows_by_name, validation_rows)
    remove_pycache()

    overall = next(row for row in validation_rows if row["validation_id"] == "VAL2426_OVERALL")
    print(f"{DOC}")
    print(f"{OUTPUTS['validation']}")
    print(f"VAL2426_OVERALL={overall['status']}")


if __name__ == "__main__":
    main()
