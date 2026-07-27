from __future__ import annotations

import math
from pathlib import Path

from Y5_R2FR_Dq_vX_observed_metric_zero_or_finite_DObs_leak_row_2025 import (
    BRANCH_WEP,
    OUT,
    QUEUE,
    ROOT,
    SOURCE_WEIGHT_DOCS,
    base_row,
    count_formalization_modified,
    csv_rows_parse,
    md_table,
    read_text,
    remove_pycache,
    write_csv,
)


DOC = ROOT / "2080-Y5-R2FR-finite-noncoercive-energy-bound-input-source-runner.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
SCRIPT_PATH = Path(__file__).resolve()
Q_R_HAT_POLICY_CEILING = 4.6e-05


def formalization_has_2080_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    patterns = (
        "*2080-Y5-R2FR*",
        "*P8_Y5_PARENT_QLOC_2080*",
        "*Y5_R2FR_finite_noncoercive_energy_bound_input_source_runner_2080*",
    )
    try:
        return any(path.is_file() for pattern in patterns for path in FORMALIZATION.rglob(pattern))
    except Exception:
        return False


def row(**kwargs: object) -> dict[str, object]:
    data = base_row()
    data.update(kwargs)
    return data


def source_register_rows() -> list[dict[str, object]]:
    specs: list[tuple[str, Path, list[str], str]] = [
        (
            "SRC2080_00_2079_doc",
            ROOT / "2079-Y5-R2FR-kfloor-topological-Hessian-owner-or-finite-noncoercive-Robin-demotion.md",
            ["NEXT2079_0_2080", "STRICT_ROBIN_DEMOTED_FINITE_BRANCH_NEXT", "VAL2079_OVERALL"],
            "2079 handoff: strict Robin activation is demoted; finite noncoercive source acquisition is next.",
        ),
        (
            "SRC2080_01_2075_runner",
            OUT / "P8_Y5_PARENT_QLOC_2075_ROBIN_ENERGY_BOUND_RUNNER.csv",
            ["EBR2075_0_symbolic_law", "STRICT_NONCLAIM_UNTIL_INPUTS_FILLED", "COMPARISON_DEFERRED"],
            "symbolic finite energy-bound runner and no-claim rule.",
        ),
        (
            "SRC2080_02_2076_inputs",
            ROOT / "2076-Y5-R2FR-positive-current-density-cap-functional-or-first-numeric-energy-bound-inputs.md",
            ["RUNNER_BLOCKED_MISSING_INPUTS", "FEI2076_11_KqR", "q_R_hat_policy_ceiling = 4.6e-05"],
            "first finite input ledger and q_R policy ceiling guard.",
        ),
        (
            "SRC2080_03_2079_finite",
            OUT / "P8_Y5_PARENT_QLOC_2079_FINITE_NONCOERCIVE_BRANCH.csv",
            ["FIN2079_0_branch_law", "RETAINED_AS_NONCLAIM_FALLBACK", "K_qR"],
            "2080 inherits finite noncoercive branch law from 2079.",
        ),
        (
            "SRC2080_04_1172_trace",
            ROOT / "1172-Y5-R10-BC-primitive-norm-owner-or-local-finite-bound-runner.md",
            ["HBP1172_2_trace_to_boundary", "MISSING_TRACE_CONSTANT", "SYMBOLIC_RUNNER_READY_NONCLAIM"],
            "Hodge/Poincare/trace finite boundary route: symbolic only without domain constants.",
        ),
        (
            "SRC2080_05_1206_boundary",
            ROOT / "1206-Y5-R10-KT-boundary-trace-law-or-Ploc-leakage-smallness-derivation.md",
            ["DRV1206_0_boundary_trace_lowering", "MISSING_DOMAIN_GEOMETRY_CONSTANT", "LOWERED_NOT_NUMERIC"],
            "normal-trace boundary lowering: useful constant grammar but no numeric domain source.",
        ),
        (
            "SRC2080_06_1240_qrmap",
            ROOT / "1240-Y5-R10-PPN-QR-residual-bound-schema-or-zero-charge-theorem.md",
            ["q_R_hat = Q_R c^2/(GM)", "gamma_minus_1_QR approximately -q_R_hat/2", "MISSING_QR_VALUE"],
            "q_R_hat and gamma projection schema; no MTS q_R value.",
        ),
        (
            "SRC2080_07_1255_ceiling",
            ROOT / "1255-Y5-R10-qRhat-source-hunt-or-parent-Hcore-reentry.md",
            ["abs(q_R_hat) <= 4.6e-5", "READY_NONCLAIM_NUMERIC_PASS", "not an MTS prediction"],
            "Cassini-derived q_R_hat ceiling is a nonclaim comparator only.",
        ),
        (
            "SRC2080_08_1521_bridge",
            ROOT / "1521-Y5-parent-q_loc-to-qR-bridge-or-weak-field-operator-source-profile.md",
            ["QLOC_TO_QR_BRIDGE_NOT_PROVED", "MISSING_NORMALIZATION_BRIDGE", "Do not import the q_R guardrail into q_loc"],
            "q_loc/q_R normalization bridge remains blocked.",
        ),
        (
            "SRC2080_09_2062_boundary",
            ROOT / "2062-Y5-R2FR-boundary-corner-RAB-silence-or-finite-PiR-bound-row.md",
            ["MISSING_ORIENTATION_CONVENTION", "CONDITIONAL_PROOF_ONLY", "Pi_R^tot"],
            "boundary/corner orientation and finite residue grammar remain unsigned.",
        ),
    ]
    rows: list[dict[str, object]] = []
    for source_id, path, needles, note in specs:
        text = read_text(path) if path.exists() else ""
        missing = [needle for needle in needles if needle not in text]
        rows.append(
            row(
                source_id=source_id,
                source_path=str(path),
                exists=path.exists(),
                needle_count=len(needles),
                missing_needles=";".join(missing),
                status="EXISTS_NEEDLES_CONFIRMED" if path.exists() and not missing else "SOURCE_OR_NEEDLE_MISSING",
                note=note,
            )
        )
    return rows


def finite_contract_rows() -> list[dict[str, object]]:
    return [
        row(
            contract_id="FBC2080_0_energy_inequality",
            object="reciprocal energy norm",
            statement="X_E^2 <= F_outer_abs + (C_Poincare*rho_R_norm + C_trace*b_C_norm)*X_E",
            derived_bound="X_E <= 0.5*(a + sqrt(a^2 + 4*F_outer_abs)), a=C_Poincare*rho_R_norm + C_trace*b_C_norm",
            status="CONTRACT_DERIVED_SYMBOLIC",
            claim_allowed=False,
        ),
        row(
            contract_id="FBC2080_1_qR_projection",
            object="finite q_R_hat prediction",
            statement="q_R_hat_predicted <= K_qR*X_E",
            derived_bound="q_R_hat_predicted <= K_qR*0.5*(a + sqrt(a^2 + 4*F_outer_abs))",
            status="PROJECTION_SHAPE_DERIVED_KQR_MISSING",
            claim_allowed=False,
        ),
        row(
            contract_id="FBC2080_2_pressure_gate",
            object="Cassini/PPN smoke pressure",
            statement="K_qR*0.5*(a + sqrt(a^2 + 4*F_outer_abs)) <= 4.6e-05",
            derived_bound="only meaningful after all theory-side inputs are numeric, sourced, same-frame, and unit-compatible",
            status="PRESSURE_INEQUALITY_READY_INPUTS_MISSING",
            claim_allowed=False,
        ),
        row(
            contract_id="FBC2080_3_no_closure",
            object="demoted finite branch",
            statement="k_C_min=0 is a demotion guard, not a proof that q_R_hat=0",
            derived_bound="finite source/residue rows must remain visible",
            status="NO_ZERO_CLOSURE_ALLOWED",
            claim_allowed=False,
        ),
    ]


def input_source_audit_rows() -> list[dict[str, object]]:
    specs = [
        (
            "ISA2080_0_domain",
            "domain_id;norm_id;boundary_id",
            "local annulus/cap/outer surface and Sobolev norm convention",
            "1172;1206;2062",
            "symbolic domain grammar exists",
            "no selected physical local domain, boundary orientation, or norm convention is parent-signed",
            "MISSING_DOMAIN_NORM_METADATA",
        ),
        (
            "ISA2080_1_C_Poincare",
            "C_Poincare",
            "coercivity/Poincare constant for reciprocal energy norm on selected domain",
            "2075;2079",
            "appears in exact finite energy-bound contract",
            "no domain geometry and boundary condition gamma, so no numeric/source-backed constant",
            "MISSING_DOMAIN_GEOMETRY_CONSTANT",
        ),
        (
            "ISA2080_2_C_trace",
            "C_trace",
            "trace constant linking cap/boundary residue to energy norm",
            "1172;1206;2075",
            "trace theorem route is symbolically valid",
            "C_trace(D,gamma) requires the same selected domain, boundary regularity, and norm convention",
            "MISSING_TRACE_CONSTANT",
        ),
        (
            "ISA2080_3_rho",
            "rho_R_norm",
            "bulk reciprocal source dual norm",
            "1206;2075;2079",
            "source-norm placeholder is correctly isolated",
            "no parent local residual/source profile has been supplied in the same norm",
            "MISSING_BULK_SOURCE_NORM",
        ),
        (
            "ISA2080_4_bC",
            "b_C_norm",
            "cap boundary/source-reference residue norm",
            "1172;2062;2075",
            "boundary residue can be bounded symbolically by trace/Hodge routes",
            "finite boundary/corner residue and orientation are unsigned",
            "MISSING_BOUNDARY_RESIDUE_NORM",
        ),
        (
            "ISA2080_5_Fouter",
            "F_outer_abs",
            "absolute outer/asymptotic flux after reference subtraction",
            "2075;2079;2062",
            "outer flux term is in the quadratic energy inequality",
            "no outer surface, reference subtraction, or flux envelope is sourced",
            "MISSING_OUTER_FLUX_BOUND",
        ),
        (
            "ISA2080_6_KqR",
            "K_qR",
            "map from X_E / reciprocal energy norm to dimensionless q_R_hat",
            "1240;1255;1521;2075",
            "q_R_hat convention and external ceiling exist as nonclaim guardrails",
            "the X_E-to-Q_R trace/Green coefficient and q_loc/q_R normalization bridge are missing",
            "MISSING_QRHAT_MAP",
        ),
        (
            "ISA2080_7_qRceiling",
            "q_R_hat_policy_ceiling",
            "external nonclaim comparator ceiling",
            "1255",
            "abs(q_R_hat)<=4.6e-05 is source-backed as a smoke ceiling",
            "it is not an MTS prediction and cannot substitute for K_qR or q_R_hat_predicted",
            "SOURCE_BACKED_NONCLAIM_COMPARATOR_ONLY",
        ),
    ]
    rows = []
    for audit_id, quantity, definition, source_anchor, support, obstruction, status in specs:
        rows.append(
            row(
                audit_id=audit_id,
                quantity=quantity,
                definition=definition,
                source_anchor=source_anchor,
                positive_support=support,
                obstruction=obstruction,
                status=status,
                source_ready=status == "SOURCE_BACKED_NONCLAIM_COMPARATOR_ONLY",
                score_ready=False,
                claim_allowed=False,
            )
        )
    return rows


def runner_input_rows() -> list[dict[str, object]]:
    specs = [
        ("domain_id", "MISSING", "domain metadata", "selected annulus/cap/outer surface"),
        ("norm_id", "MISSING", "norm metadata", "H1/L2/dual norm convention"),
        ("C_Poincare", "MISSING", "geometry units", "positive finite Poincare/coercivity constant"),
        ("C_trace", "MISSING", "geometry units", "positive finite trace constant"),
        ("rho_R_norm", "MISSING", "dual source units", "nonnegative bulk source dual norm"),
        ("b_C_norm", "MISSING", "dual boundary units", "nonnegative cap boundary residue norm"),
        ("F_outer_abs", "MISSING", "energy-like units", "nonnegative absolute outer flux"),
        ("K_qR", "MISSING", "dimensionless per X_E", "positive map from X_E to q_R_hat"),
        ("q_R_hat_policy_ceiling", str(Q_R_HAT_POLICY_CEILING), "dimensionless", "external comparator only"),
    ]
    rows = []
    for quantity, value, units, requirement in specs:
        rows.append(
            row(
                row_id=f"INPUT2080_{len(rows)}_{quantity}",
                quantity=quantity,
                current_value=value,
                units=units,
                requirement=requirement,
                source_path="D:\\Users\\ollet\\Desktop\\Turn an intuitive research programme into a formal field-theoretic framework\\Motion-TimeSpace--main\\post-checkpoint-work\\1255-Y5-R10-qRhat-source-hunt-or-parent-Hcore-reentry.md"
                if quantity == "q_R_hat_policy_ceiling"
                else "MISSING",
                source_ready=quantity == "q_R_hat_policy_ceiling",
                score_ready=False,
                claim_allowed=False,
            )
        )
    return rows


def parse_float(value: object) -> float | None:
    text = str(value).strip()
    if not text or text.upper().startswith("MISSING"):
        return None
    try:
        number = float(text)
    except ValueError:
        return None
    if not math.isfinite(number):
        return None
    return number


def run_candidate(inputs: list[dict[str, object]]) -> list[dict[str, object]]:
    by_quantity = {str(item["quantity"]): item for item in inputs}
    required_positive = ["C_Poincare", "C_trace", "K_qR"]
    required_nonnegative = ["rho_R_norm", "b_C_norm", "F_outer_abs"]
    missing: list[str] = []
    values: dict[str, float] = {}
    for key in required_positive + required_nonnegative:
        value = parse_float(by_quantity[key]["current_value"])
        if value is None:
            missing.append(key)
        else:
            values[key] = value
    domain_missing = [key for key in ["domain_id", "norm_id"] if str(by_quantity[key]["current_value"]).upper().startswith("MISSING")]
    source_unready = [
        key
        for key in required_positive + required_nonnegative
        if not str(by_quantity[key].get("source_path", "")).upper().startswith("D:")
    ]
    if missing or domain_missing or source_unready:
        return [
            row(
                run_id="RUN2080_0_current_inputs",
                input_status="REFUSED_MISSING_INPUTS",
                missing_numeric=";".join(missing),
                missing_metadata=";".join(domain_missing),
                missing_source_paths=";".join(source_unready),
                a_value="NOT_EVALUATED",
                X_E_bound="NOT_EVALUATED",
                q_R_hat_predicted_bound="NOT_EVALUATED",
                q_R_hat_policy_ceiling=Q_R_HAT_POLICY_CEILING,
                pass_status="NO_SCORE",
                claim_allowed=False,
            )
        ]
    if any(values[key] <= 0 for key in required_positive) or any(values[key] < 0 for key in required_nonnegative):
        return [
            row(
                run_id="RUN2080_0_current_inputs",
                input_status="REFUSED_SIGN_OR_RANGE_ERROR",
                missing_numeric="",
                missing_metadata="",
                missing_source_paths="",
                a_value="NOT_EVALUATED",
                X_E_bound="NOT_EVALUATED",
                q_R_hat_predicted_bound="NOT_EVALUATED",
                q_R_hat_policy_ceiling=Q_R_HAT_POLICY_CEILING,
                pass_status="NO_SCORE",
                claim_allowed=False,
            )
        ]
    a_value = values["C_Poincare"] * values["rho_R_norm"] + values["C_trace"] * values["b_C_norm"]
    x_e = 0.5 * (a_value + math.sqrt(a_value * a_value + 4.0 * values["F_outer_abs"]))
    q_r_hat = values["K_qR"] * x_e
    return [
        row(
            run_id="RUN2080_0_current_inputs",
            input_status="EVALUATED_NONCLAIM_ONLY",
            missing_numeric="",
            missing_metadata="",
            missing_source_paths="",
            a_value=a_value,
            X_E_bound=x_e,
            q_R_hat_predicted_bound=q_r_hat,
            q_R_hat_policy_ceiling=Q_R_HAT_POLICY_CEILING,
            pass_status="PASS_NONCLAIM" if q_r_hat <= Q_R_HAT_POLICY_CEILING else "FAIL_NONCLAIM",
            claim_allowed=False,
        )
    ]


def pressure_rows() -> list[dict[str, object]]:
    return [
        row(
            pressure_id="PRESS2080_0_full_inequality",
            target="q_R_hat_predicted <= q_R_hat_policy_ceiling",
            inequality="K_qR*0.5*(a + sqrt(a^2 + 4*F_outer_abs)) <= 4.6e-05",
            a_definition="a=C_Poincare*rho_R_norm + C_trace*b_C_norm",
            known_numeric="q_R_hat_policy_ceiling=4.6e-05",
            missing_inputs="C_Poincare;C_trace;rho_R_norm;b_C_norm;F_outer_abs;K_qR;domain_id;norm_id;source_paths",
            status="EXECUTABLE_FORMULA_INPUTS_MISSING",
            claim_allowed=False,
        ),
        row(
            pressure_id="PRESS2080_1_KqR_pressure",
            target="maximum allowed K_qR after X_E is sourced",
            inequality="K_qR <= 4.6e-05 / X_E_bound",
            a_definition="X_E_bound must be computed from sourced constants first",
            known_numeric="q_R_hat_policy_ceiling=4.6e-05",
            missing_inputs="X_E_bound",
            status="KQR_PRESSURE_FORM_READY_XE_MISSING",
            claim_allowed=False,
        ),
        row(
            pressure_id="PRESS2080_2_XE_pressure",
            target="maximum allowed X_E after K_qR is sourced",
            inequality="X_E_bound <= 4.6e-05 / K_qR",
            a_definition="requires positive sourced K_qR",
            known_numeric="q_R_hat_policy_ceiling=4.6e-05",
            missing_inputs="K_qR",
            status="XE_PRESSURE_FORM_READY_KQR_MISSING",
            claim_allowed=False,
        ),
    ]


def acquisition_rows() -> list[dict[str, object]]:
    specs = [
        ("ACQ2080_0_domain", "domain_id", "fixed local annulus/cap/outer surface", "MISSING_DOMAIN_NORM_METADATA", "choose/source physical local domain and boundary maps", "metadata"),
        ("ACQ2080_1_norm", "norm_id", "Sobolev/dual norm convention for X_E and source terms", "MISSING_DOMAIN_NORM_METADATA", "same norm for energy inequality and q_R projection", "metadata"),
        ("ACQ2080_2_CP", "C_Poincare", "Poincare/coercivity constant on selected domain", "MISSING_DOMAIN_GEOMETRY_CONSTANT", "derive from domain geometry and boundary condition gamma", "geometry units"),
        ("ACQ2080_3_CT", "C_trace", "trace constant from interior energy norm to cap boundary", "MISSING_TRACE_CONSTANT", "derive/source trace theorem constant for same domain", "geometry units"),
        ("ACQ2080_4_rho", "rho_R_norm", "bulk reciprocal source dual norm", "MISSING_BULK_SOURCE_NORM", "derive/source parent local residual profile norm", "dual source units"),
        ("ACQ2080_5_bC", "b_C_norm", "cap boundary/source-reference residue norm", "MISSING_BOUNDARY_RESIDUE_NORM", "derive/source boundary/corner/reference residue envelope", "dual boundary units"),
        ("ACQ2080_6_Fouter", "F_outer_abs", "outer/asymptotic flux absolute bound", "MISSING_OUTER_FLUX_BOUND", "derive/source outer surface flux after reference subtraction", "energy-like units"),
        ("ACQ2080_7_KqR", "K_qR", "map from X_E to q_R_hat", "MISSING_QRHAT_MAP", "derive exterior-hair/GM normalization bridge", "dimensionless per X_E"),
        ("ACQ2080_8_ceiling", "q_R_hat_policy_ceiling", "external PPN smoke ceiling", "SOURCE_BACKED_NONCLAIM_COMPARATOR_ONLY", "do not compare until q_R_hat_predicted exists", "dimensionless"),
    ]
    rows = []
    for row_id, quantity, definition, status, next_action, units in specs:
        rows.append(
            row(
                row_id=row_id,
                quantity=quantity,
                definition=definition,
                current_value=str(Q_R_HAT_POLICY_CEILING) if row_id == "ACQ2080_8_ceiling" else "MISSING",
                units=units,
                status=status,
                next_action=next_action,
                source_ready=row_id == "ACQ2080_8_ceiling",
                score_ready=False,
                claim_allowed=False,
            )
        )
    return rows


def claim_gate_rows() -> list[dict[str, object]]:
    return [
        row(
            gate_id="GATE2080_0_contract",
            condition="finite energy-bound formula is written",
            status="PASS_SYMBOLIC_ONLY",
            reason="the quadratic inequality and q_R pressure inequality are explicit",
            claim_allowed=False,
        ),
        row(
            gate_id="GATE2080_1_domain_constants",
            condition="C_Poincare and C_trace are sourced in one domain/norm",
            status="FAIL_BLOCKED",
            reason="domain_id, norm_id, boundary condition gamma, and constants are missing",
            claim_allowed=False,
        ),
        row(
            gate_id="GATE2080_2_source_norms",
            condition="rho_R_norm, b_C_norm, and F_outer_abs are sourced",
            status="FAIL_BLOCKED",
            reason="parent local source profile, boundary residue, and outer flux are missing",
            claim_allowed=False,
        ),
        row(
            gate_id="GATE2080_3_KqR",
            condition="K_qR maps X_E to q_R_hat with GM/source convention",
            status="FAIL_BLOCKED",
            reason="X_E-to-Q_R coefficient and q_loc/q_R bridge are missing",
            claim_allowed=False,
        ),
        row(
            gate_id="GATE2080_4_runner_score",
            condition="runner computes q_R_hat_predicted",
            status="FAIL_REFUSED",
            reason="current input row has MISSING theory-side values",
            claim_allowed=False,
        ),
        row(
            gate_id="GATE2080_5_local_claim",
            condition="derived local GR/Newton/PPN/R10 claim",
            status="FAIL_BLOCKED",
            reason="finite prediction missing; external ceiling remains comparator only",
            claim_allowed=False,
        ),
    ]


def decision_rows() -> list[dict[str, object]]:
    return [
        row(
            decision_id="DEC2080_0_runner_shape",
            decision="finite branch is now an executable inequality, not prose",
            because="the exact pressure condition is written in terms of six theory-side inputs and domain/norm metadata",
            next_action="source inputs rather than re-argue strict Robin",
            claim_allowed=False,
        ),
        row(
            decision_id="DEC2080_1_KqR_priority",
            decision="K_qR is the highest-leverage next input",
            because="without K_qR, no energy bound can become a q_R_hat/PPN comparison even if source norms are filled",
            next_action="attack exterior-hair/GM normalization bridge first",
            claim_allowed=False,
        ),
        row(
            decision_id="DEC2080_2_domain_parallel",
            decision="domain constants are the cleanest parallel fill",
            because="C_Poincare and C_trace are mathematical once the local domain, boundary class, and norm convention are fixed",
            next_action="prepare a domain/norm source pack if K_qR does not close quickly",
            claim_allowed=False,
        ),
        row(
            decision_id="DEC2080_3_no_claim",
            decision="no local-GR claim from 2080",
            because="the runner refuses missing inputs and the Cassini ceiling is only an external guardrail",
            next_action="select 2081 K_qR bridge/source-pack target",
            claim_allowed=False,
        ),
    ]


def next_target_rows() -> list[dict[str, object]]:
    return [
        row(
            target_id="NEXT2080_0_2081",
            target_doc="2081-Y5-R2FR-KqR-exterior-hair-normalization-bridge-or-finite-input-priority-source-pack.md",
            objective="derive/source K_qR, the map from finite reciprocal energy norm X_E to dimensionless q_R_hat, using the exterior 1/r hair coefficient, GM/source convention, domain trace at the outer surface, and q_loc-to-q_R bridge; if blocked, emit a prioritized finite input source pack for domain constants and source norms",
            must_include="K_qR definition; X_E-to-Q_R trace/Green coefficient; q_R_hat=Q_R c^2/(GM_source); q_loc/q_R bridge guard; same-domain/norm metadata; pressure inequality; no-cancellation guard",
            exclusions="using Cassini q_R ceiling as prediction; q_R_hat=0 closure; importing q_loc->q_R without proof; local-GR/PPN/R10 claim; GitHub; formalization-workbench edits",
            claim_allowed=False,
        )
    ]


def write_branch_copies(
    contract: list[dict[str, object]],
    audit: list[dict[str, object]],
    inputs: list[dict[str, object]],
    dry: list[dict[str, object]],
    acquisition: list[dict[str, object]],
    next_rows_: list[dict[str, object]],
) -> list[dict[str, object]]:
    copies = [
        (
            "COPY2080_0_source_weight_runner",
            SOURCE_WEIGHT_DOCS / "AFRAME_FINITE_NONCOERCIVE_ENERGY_RUNNER_2080_NONCLAIM.csv",
            contract + audit + dry,
        ),
        (
            "COPY2080_1_wep_runner",
            BRANCH_WEP / "P8_Y5_PARENT_QLOC_2080_FINITE_RUNNER_NONCLAIM.csv",
            inputs + dry,
        ),
        (
            "COPY2080_2_queue_KqR_inputs",
            QUEUE / "JR2080_KQR_AND_FINITE_INPUT_SOURCE_QUEUE.csv",
            acquisition + next_rows_,
        ),
    ]
    rows: list[dict[str, object]] = []
    for copy_id, path, data_rows in copies:
        write_csv(path, data_rows)
        rows.append(
            row(
                copy_id=copy_id,
                path=str(path),
                rows_written=len(data_rows),
                status="WRITTEN_NONCLAIM_COPY",
                claim_allowed=False,
            )
        )
    return rows


def truthy(value: object) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"true", "1", "yes", "claim_allowed", "valid"}


def validation_rows(
    sources: list[dict[str, object]],
    contract: list[dict[str, object]],
    audit: list[dict[str, object]],
    inputs: list[dict[str, object]],
    dry: list[dict[str, object]],
    pressure: list[dict[str, object]],
    acquisition: list[dict[str, object]],
    gates: list[dict[str, object]],
    next_rows_: list[dict[str, object]],
    copies: list[dict[str, object]],
    csv_paths: list[Path],
) -> list[dict[str, object]]:
    source_ok = all(r["status"] == "EXISTS_NEEDLES_CONFIRMED" for r in sources)
    csv_ok = all(path.exists() and csv_rows_parse(path) for path in csv_paths)
    contract_ok = any(r["contract_id"] == "FBC2080_2_pressure_gate" for r in contract)
    audit_missing = all(not truthy(r.get("score_ready")) for r in audit)
    q_ceiling_ok = any(r["quantity"] == "q_R_hat_policy_ceiling" and r["source_ready"] for r in inputs)
    dry_refuses = dry[0]["input_status"] == "REFUSED_MISSING_INPUTS"
    pressure_ok = any(r["pressure_id"] == "PRESS2080_0_full_inequality" and r["status"] == "EXECUTABLE_FORMULA_INPUTS_MISSING" for r in pressure)
    acquisition_ok = all(not truthy(r.get("score_ready")) and not truthy(r.get("claim_allowed")) for r in acquisition)
    gates_blocked = all(not truthy(r.get("claim_allowed")) for r in gates)
    next_ok = next_rows_[0]["target_id"] == "NEXT2080_0_2081"
    copies_ok = all(Path(str(r["path"])).exists() and csv_rows_parse(Path(str(r["path"]))) for r in copies)
    no_claims = all(
        not truthy(item.get("claim_allowed")) and not truthy(item.get("valid_for_claim"))
        for collection in [contract, audit, inputs, dry, pressure, acquisition, gates, next_rows_]
        for item in collection
    )
    formalization_clean = count_formalization_modified() == 0
    no_formalization_artifacts = not formalization_has_2080_artifacts()
    no_pycache = not (SCRIPT_PATH.parent / "__pycache__").exists()

    checks = [
        ("VAL2080_00_local_sources_exist", source_ok, "all cited source paths and needles exist"),
        ("VAL2080_01_csv_parse", csv_ok, "all generated CSV files parse cleanly"),
        ("VAL2080_02_pressure_contract", contract_ok, "finite q_R pressure inequality is explicit"),
        ("VAL2080_03_audit_missing_inputs", audit_missing, "all theory-side source inputs remain unscored"),
        ("VAL2080_04_qR_ceiling_guard", q_ceiling_ok, "q_R ceiling is present as comparator only"),
        ("VAL2080_05_dry_refusal", dry_refuses, "runner refuses current missing inputs"),
        ("VAL2080_06_pressure_rows", pressure_ok, "pressure rows are executable in shape but missing inputs"),
        ("VAL2080_07_acquisition_nonclaim", acquisition_ok, "acquisition rows are nonclaim"),
        ("VAL2080_08_claim_gates_blocked", gates_blocked, "claim gates remain blocked/nonclaim"),
        ("VAL2080_09_next_selected", next_ok, "2081 K_qR bridge target selected"),
        ("VAL2080_10_branch_copies", copies_ok, "branch copies exist and parse"),
        ("VAL2080_11_no_claim_flags", no_claims, "no generated row allows a claim"),
        ("VAL2080_12_formalization_unchanged", formalization_clean, "formalization-workbench modified-file count remains 0"),
        ("VAL2080_13_no_formalization_artifacts", no_formalization_artifacts, "no 2080 artifacts were written under formalization-workbench"),
        ("VAL2080_14_no_pycache", no_pycache, "scripts __pycache__ removed"),
    ]
    overall = all(status for _, status, _ in checks)
    checks.append(("VAL2080_OVERALL", overall, "2080 builds a fail-closed finite runner and selects K_qR bridge/source-pack next"))
    return [
        row(
            check_id=check_id,
            status="PASS" if status else "FAIL",
            detail=detail,
            claim_allowed=False,
        )
        for check_id, status, detail in checks
    ]


def write_doc(
    sources: list[dict[str, object]],
    contract: list[dict[str, object]],
    audit: list[dict[str, object]],
    inputs: list[dict[str, object]],
    dry: list[dict[str, object]],
    pressure: list[dict[str, object]],
    acquisition: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_rows_: list[dict[str, object]],
    copies: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    sections = [
        "# 2080 Y5 R2FR finite noncoercive energy-bound input source runner",
        "",
        "## Current Verdict",
        "",
        "2080 turns the demoted finite Robin branch into a fail-closed runner contract.",
        "",
        "The finite branch now has one explicit pressure inequality:",
        "`K_qR*0.5*(a + sqrt(a^2 + 4*F_outer_abs)) <= 4.6e-05`, with",
        "`a=C_Poincare*rho_R_norm + C_trace*b_C_norm`.",
        "",
        "That is useful because future work has nowhere to hide: every theory-side source row must plug into this expression before any PPN/Cassini comparison is meaningful.",
        "",
        "The current run refuses scoring. `C_Poincare`, `C_trace`, `rho_R_norm`, `b_C_norm`, `F_outer_abs`, `K_qR`, `domain_id`, and `norm_id` remain missing. The only numeric value is the external nonclaim `q_R_hat_policy_ceiling=4.6e-05`, which is not an MTS prediction.",
        "",
        "No local-GR/Newton, Cassini, PPN, R10, WEP, clock, orbital, Kcap, q_R, or public claim is made. No GitHub action and no `formalization-workbench` edit is made.",
        "",
        "## Source Register",
        md_table(sources, ["source_id", "source_path", "exists", "needle_count", "missing_needles", "status", "note", "valid_for_claim"]),
        "## Finite Bound Contract",
        md_table(contract, ["contract_id", "object", "statement", "derived_bound", "status", "claim_allowed", "valid_for_claim"]),
        "## Input Source Audit",
        md_table(audit, ["audit_id", "quantity", "definition", "source_anchor", "positive_support", "obstruction", "status", "source_ready", "score_ready", "claim_allowed", "valid_for_claim"]),
        "## Runner Input Template",
        md_table(inputs, ["row_id", "quantity", "current_value", "units", "requirement", "source_path", "source_ready", "score_ready", "claim_allowed", "valid_for_claim"]),
        "## Dry Run Results",
        md_table(dry, ["run_id", "input_status", "missing_numeric", "missing_metadata", "missing_source_paths", "a_value", "X_E_bound", "q_R_hat_predicted_bound", "q_R_hat_policy_ceiling", "pass_status", "claim_allowed", "valid_for_claim"]),
        "## Pressure Inequalities",
        md_table(pressure, ["pressure_id", "target", "inequality", "a_definition", "known_numeric", "missing_inputs", "status", "claim_allowed", "valid_for_claim"]),
        "## Acquisition Rows",
        md_table(acquisition, ["row_id", "quantity", "definition", "current_value", "units", "status", "next_action", "source_ready", "score_ready", "claim_allowed", "valid_for_claim"]),
        "## Claim Gates",
        md_table(gates, ["gate_id", "condition", "status", "reason", "claim_allowed", "valid_for_claim"]),
        "## Decisions",
        md_table(decisions, ["decision_id", "decision", "because", "next_action", "claim_allowed", "valid_for_claim"]),
        "## Next Target",
        md_table(next_rows_, ["target_id", "target_doc", "objective", "must_include", "exclusions", "claim_allowed", "valid_for_claim"]),
        "## Branch Copies",
        md_table(copies, ["copy_id", "path", "rows_written", "status", "claim_allowed", "valid_for_claim"]),
        "## Validation",
        md_table(validation, ["check_id", "status", "detail", "claim_allowed", "valid_for_claim"]),
    ]
    DOC.write_text("\n".join(sections), encoding="utf-8")


def main() -> None:
    sources = source_register_rows()
    contract = finite_contract_rows()
    audit = input_source_audit_rows()
    inputs = runner_input_rows()
    dry = run_candidate(inputs)
    pressure = pressure_rows()
    acquisition = acquisition_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_rows_ = next_target_rows()
    paths = {
        "sources": OUT / "P8_Y5_PARENT_QLOC_2080_SOURCE_REGISTER.csv",
        "contract": OUT / "P8_Y5_PARENT_QLOC_2080_FINITE_BOUND_CONTRACT.csv",
        "audit": OUT / "P8_Y5_PARENT_QLOC_2080_INPUT_SOURCE_AUDIT.csv",
        "inputs": OUT / "P8_Y5_PARENT_QLOC_2080_RUNNER_INPUT_TEMPLATE.csv",
        "dry": OUT / "P8_Y5_PARENT_QLOC_2080_DRY_RUN_RESULTS.csv",
        "pressure": OUT / "P8_Y5_PARENT_QLOC_2080_PRESSURE_INEQUALITY.csv",
        "acquisition": OUT / "P8_Y5_PARENT_QLOC_2080_ACQUISITION_ROWS.csv",
        "gates": OUT / "P8_Y5_PARENT_QLOC_2080_CLAIM_GATE.csv",
        "decision": OUT / "P8_Y5_PARENT_QLOC_2080_DECISION_LEDGER.csv",
        "next": OUT / "P8_Y5_PARENT_QLOC_2080_NEXT_TARGET.csv",
        "branch": OUT / "P8_Y5_PARENT_QLOC_2080_BRANCH_COPIES.csv",
        "validation": OUT / "P8_Y5_BRR545_2080_VALIDATION.csv",
    }
    write_csv(paths["sources"], sources)
    write_csv(paths["contract"], contract)
    write_csv(paths["audit"], audit)
    write_csv(paths["inputs"], inputs)
    write_csv(paths["dry"], dry)
    write_csv(paths["pressure"], pressure)
    write_csv(paths["acquisition"], acquisition)
    write_csv(paths["gates"], gates)
    write_csv(paths["decision"], decisions)
    write_csv(paths["next"], next_rows_)
    copies = write_branch_copies(contract, audit, inputs, dry, acquisition, next_rows_)
    write_csv(paths["branch"], copies)
    csv_paths = [path for key, path in paths.items() if key != "validation"] + [Path(str(r["path"])) for r in copies]
    remove_pycache()
    validation = validation_rows(sources, contract, audit, inputs, dry, pressure, acquisition, gates, next_rows_, copies, csv_paths)
    write_csv(paths["validation"], validation)
    write_doc(sources, contract, audit, inputs, dry, pressure, acquisition, gates, decisions, next_rows_, copies, validation)
    remove_pycache()
    print(f"wrote {DOC}")
    print(f"validation {paths['validation']}")


if __name__ == "__main__":
    main()
