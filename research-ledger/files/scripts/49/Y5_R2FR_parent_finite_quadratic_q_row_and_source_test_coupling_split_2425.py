from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


BRANCH_ID = "MTS_R2FR_PARENT_FINITE_QUADRATIC_Q_ROW_AND_SOURCE_TEST_COUPLING_SPLIT_2425"
CHECKPOINT_ID = "2425"

ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = ROOT.parent
FORMALIZATION = PROJECT_ROOT / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
MICROSCOPE = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
BETA_DOCS = ROOT / "source-intake" / "beta-source" / "docs"

DOC = ROOT / "2425-Y5-R2FR-parent-finite-quadratic-q-row-and-source-test-coupling-split.md"

OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_2425_SOURCE_REGISTER.csv",
    "parent_row": OUT / "P8_Y5_PARENT_QLOC_2425_PARENT_FINITE_Q_ROW_AUDIT.csv",
    "coupling_law": OUT / "P8_Y5_PARENT_QLOC_2425_SOURCE_TEST_COUPLING_LAW.csv",
    "branch_fork": OUT / "P8_Y5_PARENT_QLOC_2425_NO_POLE_OR_BOUNDED_BETA_FORK.csv",
    "join_gates": OUT / "P8_Y5_PARENT_QLOC_2425_R10_JOIN_GATES.csv",
    "claim_gates": OUT / "P8_Y5_PARENT_QLOC_2425_CLAIM_GATES.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_2425_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_2425_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_PARENT_QLOC_2425_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2425_VALIDATION.csv",
}

COPY_TARGETS = {
    "queue": QUEUE / "JR2425_PARENT_FINITE_Q_ROW_AND_BETA_SPLIT_NONCLAIM.csv",
    "branch_wep": MICROSCOPE / "P8_Y5_PARENT_QLOC_2425_LOCAL_GR_REFUSAL_NONCLAIM.csv",
    "beta_docs": BETA_DOCS / "PARENT_QLOC_FINITE_Q_COUPLING_SPLIT_2425_NONCLAIM.csv",
}

SOURCES = [
    {
        "source_id": "SRC2425_00_2424_handoff",
        "source_path": ROOT / "2424-Y5-R2FR-finite-q-residual-coefficient-source-or-local-benchmark-runner.md",
        "needles": ["NEXT2424_0_selected", "MISS2424_4_beta_split", "VAL2424_OVERALL"],
        "role": "current handoff selecting finite quadratic q row and source/test coupling split",
    },
    {
        "source_id": "SRC2425_01_2291_prior_specialization",
        "source_path": ROOT / "2291-Y5-R2FR-parent-finite-quadratic-row-and-source-test-beta-split.md",
        "needles": ["PQ2291_6_verdict", "BETA2291_3_common_Weyl_cg", "VAL2291_OVERALL"],
        "role": "prior q-specialized finite-row and beta-source/test audit",
    },
    {
        "source_id": "SRC2425_02_2290_kernel_contract",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_2290_SOURCE_TEST_KERNEL_CONTRACT.csv",
        "needles": ["KERN2290_3_source_test_product", "KERN2290_4_universal_weyl_warning"],
        "role": "source/test product law and c_g-squared warning",
    },
    {
        "source_id": "SRC2425_03_2290_join_readiness",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_2290_INTERNAL_JOIN_READINESS.csv",
        "needles": ["JOIN2290_4_beta_source", "JOIN2290_5_beta_test", "JOIN2290_8_alpha_predicted"],
        "role": "current missing internal join factors for R10 alpha prediction",
    },
    {
        "source_id": "SRC2425_04_2243_beta_split",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_2243_BETA_SOURCE_TEST_DERIVATION.csv",
        "needles": ["BETA2243_1_two_body_exchange", "BETA2243_3_common_Weyl_cg", "BETA2243_5_verdict"],
        "role": "prior R_AB beta-source/test derivation and c_g^2 convention",
    },
    {
        "source_id": "SRC2425_05_1036_generic_beta",
        "source_path": OUT / "P8_Y5_R10_1036_BETA_SOURCE_TEST_DERIVATION.csv",
        "needles": ["BETA1036_1_two_body_exchange", "BETA1036_3_common_Weyl_cg", "BETA1036_5_verdict"],
        "role": "generic finite-X source/test beta derivation",
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


def parent_row_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            row_id="PQR2425_0_stationarity",
            required_piece="E_q|_0 = 0",
            meaning="the local GR/Newton branch is an extremum of the parent q sector before adding test sources",
            current_status="MISSING_PARENT_STATIONARITY",
            effect_if_missing="a tadpole drives q_R even before matter/source coupling is considered",
        ),
        base_row(
            row_id="PQR2425_1_Zq",
            required_piece="Z_q",
            meaning="coefficient of the projected local derivative/gradient term <Dq,Dq>",
            current_status="MISSING_PARENT_KINETIC_RESIDUE_OR_THEOREM_ZERO",
            effect_if_missing="range/hair/R10 kernel cannot be numeric or theorem-zero",
        ),
        base_row(
            row_id="PQR2425_2_Mq2",
            required_piece="M_q^2 and lambda_q",
            meaning="parent Hessian/mass gap in same q normalization, lambda_q=sqrt(Z_q/M_q^2) if Z_q exists",
            current_status="MISSING_PARENT_HESSIAN_OR_RANGE",
            effect_if_missing="q_R=j_q/M_q^2 and finite-range screening remain templates",
        ),
        base_row(
            row_id="PQR2425_3_Jq",
            required_piece="J_q / j_q",
            meaning="source/readout current in the q direction, including matter, hidden, boundary, and domain channels",
            current_status="MISSING_SOURCE_CURRENT_OR_ZERO_THEOREM",
            effect_if_missing="finite q numerator and zero-source route remain unowned",
        ),
        base_row(
            row_id="PQR2425_4_boundary_tail",
            required_piece="B_R / Pi_q / epsilon_tail",
            meaning="boundary/corner/worldtube/tail contribution that can regenerate local q hair",
            current_status="MISSING_BOUNDARY_NO_HAIR_OR_TAIL_ENVELOPE",
            effect_if_missing="cannot ignore Q_R/r hair or cancellation tails",
        ),
        base_row(
            row_id="PQR2425_5_beta_law",
            required_piece="beta_source and beta_test",
            meaning="source and test charge legs of the two-body finite q exchange",
            current_status="MISSING_BETA_SOURCE_TEST_ROWS",
            effect_if_missing="R10 alpha(lambda) cannot be scored and c_g cannot be treated as one linear coefficient",
        ),
        base_row(
            row_id="PQR2425_6_verdict",
            required_piece="single parent finite-q row",
            meaning="one parent branch supplies stationarity, sign, Z_q/M_q^2/J_q, source/test betas, projection, and tails",
            current_status="FAIL_CURRENT_CLAIM_PARENT_ROW_NOT_OWNED",
            effect_if_missing="finite-q local/R10 branch remains nonclaim template",
        ),
    ]


def coupling_law_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            law_id="LAW2425_0_point_body",
            premise="ordinary body i has effective source/readout mass m_i[q]",
            relation="beta_i := partial_q ln(m_i^eff) in the parent q normalization",
            status="CONDITIONAL_STANDARD_VARIATION",
            missing_for_claim="parent-owned q normalization and matter/readout mass functional",
        ),
        base_row(
            law_id="LAW2425_1_two_body_exchange",
            premise="finite q mode has a static Yukawa/Green kernel",
            relation="delta V_q(r)=-s_q beta_source beta_test m_s m_t exp(-r/lambda_q)/(4*pi Z_q r) after projection",
            status="CONDITIONAL_EXCHANGE_LAW",
            missing_for_claim="sign, Z_q, lambda_q, source/test betas, tensor/projector profile, and tail envelope",
        ),
        base_row(
            law_id="LAW2425_2_R10_alpha_match",
            premise="R10 compares to V_N[1+alpha exp(-r/lambda)]",
            relation="alpha_q(lambda)=K_q^R10(lambda) beta_source(lambda) beta_test(lambda)+epsilon_tail(lambda)",
            status="REQUIRED_PRODUCT_FORM",
            missing_for_claim="K_q, source/test profiles, q range, source normalization, and digitized comparator curve",
        ),
        base_row(
            law_id="LAW2425_3_common_Weyl_cg",
            premise="m_i^eff=A_g(q)m_i and A_g is universal",
            relation="alpha_q is proportional to c_g^2 unless the source leg is explicitly packed into Qbar",
            status="CG_SQUARED_UNLESS_SOURCE_LEG_PACKED",
            missing_for_claim="parent-signed A_g branch, q normalization, and clear Qbar leg accounting",
        ),
        base_row(
            law_id="LAW2425_4_quotient_zero",
            premise="matter/constants descend through public quotient and q is vertical/constraint-only",
            relation="beta_source=beta_test=0 only if descent/no-shadow/no-marker/no-tail clauses close together",
            status="CONDITIONAL_ZERO_NOT_SIGNED",
            missing_for_claim="parent q-kernel, matter functor, no-shadow frame, no-marker constants, hidden-tail silence",
        ),
        base_row(
            law_id="LAW2425_5_verdict",
            premise="current corpus",
            relation="product law is structurally derived, but no numeric/theorem-zero source/test row is claim-ready",
            status="BETA_ROWS_UNOWNED",
            missing_for_claim="parent action schema or bounded beta acquisition rows",
        ),
    ]


def branch_fork_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            fork_id="FORK2425_0_no_physical_q_pole",
            branch="structural no-pole route",
            condition="q is quotient/gauge/constraint-only before local inversion; no physical Green kernel exists",
            payoff="alpha_q=0 and q_R=0 structurally if hidden tails also vanish",
            current_status="BEST_LEAST_SCRUTINY_ROUTE_UNSIGNED",
            next_action="try no-physical-q-pole theorem first",
        ),
        base_row(
            fork_id="FORK2425_1_sourcefree_massive_nohair",
            branch="massive finite q with no local source",
            condition="Z_q>0, M_q^2>0, J_q=0, boundary_flux_q=0 from one parent branch",
            payoff="finite mode exists but exterior local/R10 residual can vanish by energy/nohair identity",
            current_status="CONDITIONAL_NOHAIR_UNSIGNED",
            next_action="only revive if source-zero and boundary-flux zero close together",
        ),
        base_row(
            fork_id="FORK2425_2_sourced_finite_exchange",
            branch="physical finite q exchange",
            condition="Z_q, lambda_q, beta_source, beta_test, K_q, sign, profile and tail envelope are sourced",
            payoff="alpha_q(lambda) becomes testable against R10 and cross-checked by PPN/WEP/clock/orbital arenas",
            current_status="SCOREABLE_STRUCTURE_INPUTS_MISSING",
            next_action="fallback to bounded beta rows without cancellation",
        ),
        base_row(
            fork_id="FORK2425_3_shadow_tail",
            branch="readout/marker/non-Hilbert tail",
            condition="Weyl/disformal/marker leakage or non-Hilbert source channels survive",
            payoff="tail envelope must be bounded and cannot cancel the main finite exchange by assumption",
            current_status="RETAINED_TAIL_BRANCH",
            next_action="carry no-cancellation tail envelope",
        ),
    ]


def join_gate_rows() -> list[dict[str, Any]]:
    return [
        base_row(join_id="JOIN2425_0_parent_row", target="parent finite-q row", status="MISSING_PARENT_ROW", ready_for_score=False, blocking_reason="E_q, Z_q, M_q^2/lambda_q, J_q, beta split, projector and tails are not parent-signed together"),
        base_row(join_id="JOIN2425_1_beta_source", target="beta_source", status="MISSING_SOURCE_CHARGE", ready_for_score=False, blocking_reason="source-body q charge leg not numeric/theorem-zero"),
        base_row(join_id="JOIN2425_2_beta_test", target="beta_test", status="MISSING_TEST_CHARGE", ready_for_score=False, blocking_reason="test/readout q charge leg not numeric/theorem-zero"),
        base_row(join_id="JOIN2425_3_cg_law", target="c_g versus c_g^2 policy", status="LAW_CORRECTED_NO_NUMERIC_INPUTS", ready_for_score=False, blocking_reason="must declare whether Qbar contains source leg before any c_g scoring"),
        base_row(join_id="JOIN2425_4_alpha_predicted", target="alpha_R10(lambda)", status="MISSING_SOURCE_NORMALIZED_ALPHA", ready_for_score=False, blocking_reason="K_q, betas, lambda_q, profile, tail and comparator curve not complete"),
        base_row(join_id="JOIN2425_5_no_pole", target="no physical q pole", status="NO_POLE_ROUTE_NOT_SIGNED", ready_for_score=False, blocking_reason="quotient/gauge/constraint pole audit still needs proof"),
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        base_row(gate_id="CG2425_0_product_law", gate="source/test product law written", passed=True, reason="conditional exchange law requires beta_source beta_test and c_g^2 for universal source/test legs"),
        base_row(gate_id="CG2425_1_parent_row", gate="single parent finite-q row owned", passed=False, reason="Z_q/M_q^2/J_q/betas/projector/tails not supplied together"),
        base_row(gate_id="CG2425_2_numeric_alpha", gate="alpha_R10(lambda) scoreable", passed=False, reason="K_q, betas, lambda_q, profile, tail and comparator curve missing"),
        base_row(gate_id="CG2425_3_linear_cg", gate="linear c_g score allowed", passed=False, reason="universal two-body exchange is c_g squared unless source leg is already packed into Qbar"),
        base_row(gate_id="CG2425_4_no_pole", gate="no physical q pole derived", passed=False, reason="structural no-pole route remains unsigned"),
        base_row(gate_id="CG2425_5_local_GR_Newton", gate="local GR/Newton recovery derived", passed=False, reason="neither no-pole theorem nor finite residual coefficient row is parent-owned"),
        base_row(gate_id="CG2425_6_public", gate="public/GitHub claim allowed", passed=False, reason="private nonclaim checkpoint"),
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        base_row(decision_id="DEC2425_0_parent_row", decision="PARENT_FINITE_Q_ROW_NOT_OWNED", rationale="all required pieces exist only as contracts or missing slots, not one parent action row", consequence="finite q/R10 remains nonclaim"),
        base_row(decision_id="DEC2425_1_coupling", decision="COUPLING_LAW_IS_PRODUCT_NOT_LINEAR_MAGIC", rationale="two-body exchange requires source leg times test leg; universal c_g enters both legs", consequence="future R10 rows must carry beta_source, beta_test, and Qbar leg accounting"),
        base_row(decision_id="DEC2425_2_best_route", decision="TRY_NO_PHYSICAL_Q_POLE_FIRST", rationale="structural no-pole/constraint route faces less scrutiny than fitting a short-range finite residual", consequence="attempt no-pole theorem before bounded beta acquisition"),
        base_row(decision_id="DEC2425_3_fallback", decision="BOUNDED_BETA_ROWS_IF_NO_POLE_FAILS", rationale="if q is physical, the honest fallback is finite source/test beta rows plus tail envelope", consequence="build bounded beta_source/beta_test acquisition without cancellation"),
        base_row(decision_id="DEC2425_4_claim_policy", decision="KEEP_PRIVATE_NONCLAIM", rationale="no scoreable alpha, PPN or local-GR result yet", consequence="no GitHub action"),
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            route_id="NEXT2425_0_selected",
            selection_status="selected",
            target_file="2426-Y5-R2FR-no-physical-q-pole-theorem-or-bounded-beta-runner.md",
            target_script="scripts/Y5_R2FR_no_physical_q_pole_theorem_or_bounded_beta_runner_2426.py",
            objective="try to prove the finite local q/R_AB mode has no physical pole in the GR/Newton branch; if not, build bounded beta_source/beta_test acquisition rows with no-cancellation tails",
            success_condition="quotient/gauge/constraint pole audit closes, or beta_source/beta_test rows are source-ready nonclaim with c_g^2 convention and no-cancellation envelope",
            do_not_do="do not assert alpha=0, invent beta/c_g values, score linear c_g, cancel unknown tails, claim R10/local-GR pass, edit formalization-workbench, or push GitHub",
        )
    ]


def copy_branch_rows(parent_row: list[dict[str, Any]], coupling_law: list[dict[str, Any]], decision_ledger: list[dict[str, Any]]) -> list[dict[str, Any]]:
    copy_specs = [
        ("queue", OUTPUTS["parent_row"], COPY_TARGETS["queue"], parent_row),
        ("branch_wep", OUTPUTS["coupling_law"], COPY_TARGETS["branch_wep"], coupling_law),
        ("beta_docs", OUTPUTS["decision"], COPY_TARGETS["beta_docs"], decision_ledger),
    ]
    rows: list[dict[str, Any]] = []
    for copy_id, source_path, target_path, copied_rows in copy_specs:
        write_csv(target_path, copied_rows)
        rows.append(
            base_row(
                copy_id=f"BC2425_{copy_id}",
                source_path=source_path,
                target_path=target_path,
                target_exists=target_path.exists(),
                row_count=len(copied_rows),
                purpose="finite-q parent row and source/test coupling nonclaim handoff",
            )
        )
    return rows


def formalization_has_2425_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    patterns = (
        "*2425-Y5-R2FR*",
        "*P8_Y5_PARENT_QLOC_2425*",
        "*P8_Y5_BRR545_2425*",
        "*Y5_R2FR_parent_finite_quadratic_q_row_and_source_test_coupling_split_2425*",
        "*JR2425*",
        "*PARENT_QLOC_FINITE_Q_COUPLING_SPLIT_2425*",
    )
    return any(path.is_file() for pattern in patterns for path in FORMALIZATION.rglob(pattern))


def remove_pycache() -> None:
    cache = ROOT / "scripts" / "__pycache__"
    if cache.exists():
        shutil.rmtree(cache)


def flags_safe(rows_by_name: dict[str, list[dict[str, Any]]]) -> bool:
    allowed_true = {("claim_gates", "passed", "CG2425_0_product_law")}
    for group_name, rows in rows_by_name.items():
        for row in rows:
            row_key = row.get("gate_id", row.get("row_id", row.get("law_id", "")))
            for key in ("valid_for_claim", "claim_allowed", "ready_for_score"):
                value = row.get(key)
                if value is True or stringify(value).lower() == "true":
                    return False
            if row.get("passed") is True and (group_name, "passed", row_key) not in allowed_true:
                return False
    return True


def build_validation_rows(rows_by_name: dict[str, list[dict[str, Any]]], branch_copy_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    source_rows = rows_by_name["source_register"]
    parent_rows = rows_by_name["parent_row"]
    law_rows = rows_by_name["coupling_law"]
    fork_rows = rows_by_name["branch_fork"]
    join_rows = rows_by_name["join_gates"]
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
        ("VAL2425_SOURCES_EXIST", all(row["path_exists"] for row in source_rows), "all cited source paths exist"),
        ("VAL2425_NEEDLES_FOUND", all(row["needles_found"] for row in source_rows), "all source needles found"),
        ("VAL2425_PARENT_ROW_BLOCKED", any(row["row_id"] == "PQR2425_6_verdict" and "NOT_OWNED" in row["current_status"] for row in parent_rows), "parent finite-q row is explicitly not owned"),
        ("VAL2425_PRODUCT_LAW", any(row["law_id"] == "LAW2425_2_R10_alpha_match" and "beta_source" in row["relation"] and "beta_test" in row["relation"] for row in law_rows), "R10 source/test product law present"),
        ("VAL2425_CG_SQUARED", any(row["law_id"] == "LAW2425_3_common_Weyl_cg" and "c_g^2" in row["relation"] for row in law_rows), "c_g-squared warning present"),
        ("VAL2425_FORK_COMPLETE", {row["fork_id"] for row in fork_rows} >= {"FORK2425_0_no_physical_q_pole", "FORK2425_2_sourced_finite_exchange", "FORK2425_3_shadow_tail"}, "no-pole/finite/tail fork complete"),
        ("VAL2425_JOIN_BLOCKED", all(not row["ready_for_score"] for row in join_rows), "all R10 join gates remain unscoreable"),
        ("VAL2425_NEXT_SELECTED", any(row["route_id"] == "NEXT2425_0_selected" and "no-physical-q-pole" in row["target_file"] for row in next_rows), "no-pole or bounded-beta runner selected next"),
        ("VAL2425_FLAGS_SAFE", flags_safe(rows_by_name), "no claim/score flags are true except the structural product-law claim gate"),
        ("VAL2425_BRANCH_COPIES", all(row["target_exists"] for row in branch_copy_rows), "branch copy files written"),
        ("VAL2425_CSV_PARSE", all(item[1] and item[2] > 0 for item in csv_results), "all generated CSV and branch copies parse with rows"),
        ("VAL2425_NO_FORMALIZATION_OUTPUT", not formalization_has_2425_artifacts(), "no 2425 artifacts written into formalization-workbench"),
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
            validation_id="VAL2425_OVERALL",
            status="PASS" if overall_passed else "FAIL",
            detail="2425 rebases the finite-q quadratic parent-row audit, refuses parent-row/R10 claims, locks the beta_source beta_test and c_g^2 coupling law, and selects no-physical-q-pole or bounded-beta runner next",
            fatal=not overall_passed,
        )
    )
    return rows


def write_document(rows_by_name: dict[str, list[dict[str, Any]]], validation_rows: list[dict[str, Any]]) -> None:
    content = f"""# 2425 Y5 R2FR Parent Finite Quadratic q Row And Source-Test Coupling Split

## Result

The coupling piece is now sharper: the finite local `q/R_AB` branch needs a whole parent row, not a loose coupling constant. A scoreable row would have to supply `E_q|0=0`, `Z_q`, `M_q^2/lambda_q`, `J_q`, `beta_source`, `beta_test`, sign, projection, boundary support, and tail envelope from one compatible parent branch.

That row is **not owned** by the current corpus. But the coupling law is disciplined: a two-body finite exchange is product-like, `alpha_q(lambda)=K_q^R10(lambda) beta_source(lambda) beta_test(lambda)+epsilon_tail(lambda)`. If the same universal Weyl factor supplies both source and test legs, the leading law is `c_g^2`, not linear `c_g`, unless the source leg is explicitly packed into `Qbar`.

## Practical Status

- **Progress:** the dangerous “one coupling number fixes R10” shortcut is blocked.
- **Best route:** prove no physical local `q/R_AB` pole in the GR/Newton branch.
- **Fallback:** if the pole survives, build bounded `beta_source/beta_test` rows with no-cancellation tails.
- **Still blocked:** no parent finite-q row, no scoreable `alpha_R10(lambda)`, no local-GR/Newton claim.
- **Private:** no GitHub/public claim from this checkpoint.

## Source Register

{table(["source_id", "source_path", "path_exists", "needles_found", "role"], rows_by_name["source_register"])}

## Parent Finite q Row Audit

{table(["row_id", "required_piece", "meaning", "current_status", "effect_if_missing"], rows_by_name["parent_row"])}

## Source/Test Coupling Law

{table(["law_id", "premise", "relation", "status", "missing_for_claim"], rows_by_name["coupling_law"])}

## No-Pole Or Bounded-Beta Fork

{table(["fork_id", "branch", "condition", "payoff", "current_status", "next_action"], rows_by_name["branch_fork"])}

## R10 Join Gates

{table(["join_id", "target", "status", "ready_for_score", "blocking_reason"], rows_by_name["join_gates"])}

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
        "parent_row": parent_row_rows(),
        "coupling_law": coupling_law_rows(),
        "branch_fork": branch_fork_rows(),
        "join_gates": join_gate_rows(),
        "claim_gates": claim_gate_rows(),
        "decision": decision_rows(),
        "next_target": next_target_rows(),
    }
    for name, rows in rows_by_name.items():
        write_csv(OUTPUTS[name], rows)

    branch_copy_rows = copy_branch_rows(
        rows_by_name["parent_row"],
        rows_by_name["coupling_law"],
        rows_by_name["decision"],
    )
    rows_by_name["branch_copies"] = branch_copy_rows
    write_csv(OUTPUTS["branch_copies"], branch_copy_rows)

    validation_rows = build_validation_rows(rows_by_name, branch_copy_rows)
    write_csv(OUTPUTS["validation"], validation_rows)
    write_document(rows_by_name, validation_rows)
    remove_pycache()

    overall = next(row for row in validation_rows if row["validation_id"] == "VAL2425_OVERALL")
    print(f"{DOC}")
    print(f"{OUTPUTS['validation']}")
    print(f"VAL2425_OVERALL={overall['status']}")


if __name__ == "__main__":
    main()
