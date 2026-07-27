from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
BRANCH_ID = "MTS_R2FR_EH_OPERATOR_PREMISE_SIGNATURE_OR_R11_BETA_VECTOR_2515"
CHECKPOINT_ID = "2515"
DOC = ROOT / "2515-Y5-R2FR-EH-operator-premise-signature-or-R11-beta-residual-vector.md"
MTS_RESIDUALS = ROOT / "source-intake" / "mts_residuals"

OUTPUTS = {
    "source_register": MTS_RESIDUALS / "P8_Y5_NO_SHADOW_2515_SOURCE_REGISTER.csv",
    "eh_premise_audit": MTS_RESIDUALS / "P8_Y5_NO_SHADOW_2515_EH_PREMISE_SIGNATURE_AUDIT.csv",
    "r11_beta_vector": MTS_RESIDUALS / "P8_Y5_NO_SHADOW_2515_R11_BETA_RESIDUAL_VECTOR.csv",
    "operator_map": MTS_RESIDUALS / "P8_Y5_NO_SHADOW_2515_OPERATOR_TO_OBSERVABLE_MAP.csv",
    "dryrun_results": MTS_RESIDUALS / "P8_Y5_NO_SHADOW_2515_NONCLAIM_DRYRUN_RESULTS.csv",
    "decision_ledger": MTS_RESIDUALS / "P8_Y5_NO_SHADOW_2515_DECISION_LEDGER.csv",
    "next_target": MTS_RESIDUALS / "P8_Y5_NO_SHADOW_2515_NEXT_TARGET.csv",
    "branch_copies": MTS_RESIDUALS / "P8_Y5_NO_SHADOW_2515_BRANCH_COPIES.csv",
    "validation": MTS_RESIDUALS / "P8_Y5_BRR545_2515_VALIDATION.csv",
}

BRANCH_COPIES = {
    "eh_premise_audit": ROOT
    / "source-intake"
    / "local_bounds"
    / "EH_operator_premise_signature_2515_NONCLAIM.csv",
    "r11_beta_vector": ROOT
    / "source-intake"
    / "beta-source"
    / "docs"
    / "R11_beta_residual_vector_2515_NONCLAIM.csv",
    "operator_map": ROOT
    / "source-intake"
    / "rab-sector"
    / "acquisition-queue"
    / "JR2515_R11_OPERATOR_TO_OBSERVABLE_MAP_NONCLAIM.csv",
    "next_target": ROOT
    / "source-intake"
    / "rab-sector"
    / "acquisition-queue"
    / "JR2515_R2FR_FIRST_OPERATOR_ROW_R2_FR_SCALAR_MODE_NONCLAIM.csv",
}

SOURCE_SPECS = [
    {
        "source_id": "SRC2515_0_2514_next",
        "path": "source-intake/mts_residuals/P8_Y5_NO_SHADOW_2514_NEXT_TARGET.csv",
        "needles": ["NEXT2514_0_selected", "R11 non-EH operator beta residual vector"],
        "role": "authoritative selection of the EH-premise/R11-beta checkpoint",
    },
    {
        "source_id": "SRC2515_1_eh_theorem_1512",
        "path": "source-intake/microscope/quarantine/1512/EH_SELECTION_THEOREM_ATTEMPT_NONCLAIM.csv",
        "needles": ["THM1512_0_conditional_EH_selection", "NON_EH_VECTOR_REQUIRED"],
        "role": "conditional Lovelock-style EH theorem and unsigned-premise verdict",
    },
    {
        "source_id": "SRC2515_2_r11_vector_1512",
        "path": "source-intake/microscope/quarantine/1512/NON_EH_RESIDUAL_VECTOR_NONCLAIM.csv",
        "needles": ["R11_1512_01", "RETAINED_NON_EH_RESIDUAL"],
        "role": "retained non-EH operator families and missing coefficient slots",
    },
    {
        "source_id": "SRC2515_3_r11_lock_1513",
        "path": "source-intake/microscope/quarantine/1513/R11_VECTOR_LOCK_NONCLAIM.csv",
        "needles": ["R11LOCK1513_01", "ACTIVE_LOCAL_OPERATOR_BRANCH_UNTIL_ZERO_OR_BOUND"],
        "role": "lock status: retained until parent zero theorem or sourced bound",
    },
    {
        "source_id": "SRC2515_4_operator_queue_2514",
        "path": "source-intake/mts_residuals/P8_Y5_NO_SHADOW_2514_EH_OPERATOR_SELECTION_QUEUE.csv",
        "needles": ["OP2514_0_EH_lovelock", "OP2514_5_verdict"],
        "role": "operator families to preserve after EH import is refused",
    },
    {
        "source_id": "SRC2515_5_beta_vector_2514",
        "path": "source-intake/mts_residuals/P8_Y5_NO_SHADOW_2514_FINITE_BETA_SOURCE_VECTOR.csv",
        "needles": ["DBETA2514_6_total_abs", "MISSING_SUM_ABS_VECTOR"],
        "role": "beta absolute-envelope comparator structure",
    },
    {
        "source_id": "SRC2515_6_beta_bound_2513",
        "path": "source-intake/local_bounds/PPN_source_weight_bound_interface_2513_NONCLAIM.csv",
        "needles": ["PBOUND2513_1_beta", "7.8e-05"],
        "role": "source-backed beta-minus-one comparator bound",
    },
    {
        "source_id": "SRC2515_7_operator_decision_1512",
        "path": "source-intake/microscope/quarantine/1512/OPERATOR_DECISION_NONCLAIM.csv",
        "needles": ["DEC1512_0_EH_route", "NO_EH_CLAIM"],
        "role": "explicit no-EH-claim decision and R11 route selection",
    },
    {
        "source_id": "SRC2515_8_2514_validation",
        "path": "source-intake/mts_residuals/P8_Y5_BRR545_2514_VALIDATION.csv",
        "needles": ["VAL2514_OVERALL", "PASS"],
        "role": "previous checkpoint validation gate",
    },
]

BETA_BOUND = "7.8e-05"


def timestamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def base_row(**kwargs: Any) -> dict[str, Any]:
    row: dict[str, Any] = {
        "timestamp_utc": timestamp(),
        "branch_id": BRANCH_ID,
        "checkpoint_id": CHECKPOINT_ID,
        "valid_for_claim": False,
        "claim_allowed": False,
    }
    row.update(kwargs)
    return row


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except FileNotFoundError:
        return ""


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def csv_rows_parse(path: Path) -> tuple[bool, int, str]:
    try:
        with path.open(newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
        return bool(rows), len(rows), "OK"
    except Exception as exc:  # pragma: no cover
        return False, 0, f"{type(exc).__name__}: {exc}"


def md_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    lines = [
        "| " + " | ".join(columns) + " |",
        "| " + " | ".join("---" for _ in columns) + " |",
    ]
    for row in rows:
        cells = []
        for column in columns:
            value = str(row.get(column, "")).replace("\n", "<br>").replace("|", "\\|")
            cells.append(value)
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)


def remove_pycache() -> None:
    pycache = Path(__file__).resolve().parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for spec in SOURCE_SPECS:
        path = ROOT / spec["path"]
        text = read_text(path)
        found = [needle for needle in spec["needles"] if needle in text]
        rows.append(
            base_row(
                source_id=spec["source_id"],
                source_path=spec["path"],
                path_exists=path.exists(),
                required_needles=";".join(spec["needles"]),
                found_needles=";".join(found),
                role=spec["role"],
                source_pass=path.exists() and len(found) == len(spec["needles"]),
            )
        )
    return rows


def eh_premise_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "premise_id": "EHP2515_0_dimension",
            "premise": "compact local exterior branch is four-dimensional",
            "current_signature_status": "NOT_PARENT_SIGNED",
            "current_evidence": "1512 theorem lists 4D as a required premise, not a derived parent result",
            "countermodel_if_unsigned": "higher-dimensional, effective-dimensional, or domain-reduced branch can carry extra curvature operators",
            "needed_signature": "parent quotient/action proves the local compact exterior reduction is exactly 4D before the weak-field limit",
            "effect_if_signed": "one Lovelock premise becomes available",
        },
        {
            "premise_id": "EHP2515_1_locality",
            "premise": "local finite-derivative gravitational operator",
            "current_signature_status": "NOT_PARENT_SIGNED",
            "current_evidence": "nonlocal memory kernel remains an active R11 row",
            "countermodel_if_unsigned": "retarded, integral, or memory kernels shift PPN and R10 tails while preserving first-order appearances",
            "needed_signature": "parent action excludes Box^-1, history kernels, and domain-memory operator tails in the local branch",
            "effect_if_signed": "nonlocal-memory row can be zeroed rather than bounded",
        },
        {
            "premise_id": "EHP2515_2_diffeomorphism",
            "premise": "complete local branch is diffeomorphism invariant",
            "current_signature_status": "CONDITIONAL_BUT_NOT_COMPLETE",
            "current_evidence": "EH theorem route assumes diffeomorphism invariance, but source/readout/projector sectors remain unsigned",
            "countermodel_if_unsigned": "domain projectors, source normalizers, or readout maps can break the covariant cancellation used by Bianchi/PPN closure",
            "needed_signature": "parent variation supplies a covariant Ward identity including source, boundary, projector, and readout terms",
            "effect_if_signed": "Bianchi conservation can be used without a hidden-sector escape hatch",
        },
        {
            "premise_id": "EHP2515_3_metric_only_lc",
            "premise": "metric-only Levi-Civita exterior branch",
            "current_signature_status": "NOT_PARENT_SIGNED",
            "current_evidence": "torsion/nonmetricity and vector/preferred-frame rows remain retained",
            "countermodel_if_unsigned": "connection, coframe, torsion, nonmetricity, or preferred-frame carriers create PPN residuals outside pure EH",
            "needed_signature": "parent action descends to metric-only Levi-Civita variables with no hypermomentum or independent connection current",
            "effect_if_signed": "torsion/nonmetricity and preferred-frame operator routes can be demoted",
        },
        {
            "premise_id": "EHP2515_4_second_order",
            "premise": "second-order metric field equations",
            "current_signature_status": "NOT_PARENT_SIGNED",
            "current_evidence": "R2/f(R), Ricci-squared, and Weyl-squared rows remain retained",
            "countermodel_if_unsigned": "higher-curvature scalar/spin modes shift gamma, beta, and alpha(lambda)",
            "needed_signature": "parent normal-form theorem excludes higher-derivative curvature invariants or gives exact zero coefficients",
            "effect_if_signed": "R2/f(R) and quadratic-curvature rows can be zeroed instead of bounded",
        },
        {
            "premise_id": "EHP2515_5_boundary_topological",
            "premise": "boundary and topological terms are harmless in the local source/readout problem",
            "current_signature_status": "NOT_PARENT_SIGNED",
            "current_evidence": "boundary/topological and projector-domain stress rows remain retained",
            "countermodel_if_unsigned": "corner, no-flux, reference, or projector stresses can shift U^2/source-normalization after Newton matching",
            "needed_signature": "parent boundary class proves exact topological/no-flux silence including variation, source measure, and readout",
            "effect_if_signed": "boundary/projector rows can be removed from beta and preferred-frame ledgers",
        },
        {
            "premise_id": "EHP2515_6_no_extra_fields",
            "premise": "no scalar, vector, bulk-X, or source-normalization extra carrier survives",
            "current_signature_status": "NOT_PARENT_SIGNED",
            "current_evidence": "scalar-tensor, vector, bulk-X, source-normalization, and q/source rows remain active across 2513-2514",
            "countermodel_if_unsigned": "extra carrier can be invisible at Newton order but visible in beta, gamma, R10, clocks, or alpha3",
            "needed_signature": "parent quotient gives double-zero or sourced finite coefficient for each extra carrier",
            "effect_if_signed": "R11 vector collapses toward the EH local-GR branch",
        },
        {
            "premise_id": "EHP2515_7_verdict",
            "premise": "MTS-owned EH/Lovelock local operator",
            "current_signature_status": "EH_PREMISES_NOT_PARENT_SIGNED_R11_VECTOR_REQUIRED",
            "current_evidence": "1512 and 2514 both allow EH as reference/conditional route but refuse MTS-owned EH import",
            "countermodel_if_unsigned": "claiming beta=1 would smuggle GR instead of deriving it",
            "needed_signature": "all prior premises plus source glue/readout silence pass together",
            "effect_if_signed": "delta_beta_operator can be set to zero; source/readout/boundary still need their own gates",
        },
    ]
    return [base_row(score_ready=False, valid_prediction_row=False, **row) for row in rows]


def beta_channel_for_family(operator_family: str, induced: str) -> str:
    channels = {
        "boundary_topological_terms": "possible U^2 boundary/reference tail; beta row retained until no-flux/topological silence is signed",
        "R2_fR_scalar_mode": "direct higher-curvature scalar mode: gamma, beta, and finite-range alpha(lambda)",
        "Ricci_Weyl_squared": "gamma/xi primary; beta only after weak-field source/readout map, so retained but not scored",
        "scalar_tensor_class_metric": "direct scalar-tensor PPN channel: gamma, beta, clocks, Gdot, and alpha(lambda)",
        "vector_preferred_frame": "preferred-frame primary; beta cross-tail possible through source/readout normalization",
        "torsion_nonmetricity": "connection-current/non-Hilbert channel; beta impact requires weak-field map",
        "bulk_X_force_law": "extra force/source stress channel; can enter beta and R10 once q_X, m_X, and kernel are supplied",
        "nonlocal_memory_kernel": "memory kernel channel; beta impact requires local reduction and time/source kernel",
        "source_normalization_operator": "second-order source-normalization channel after fixed observed GM",
        "projector_domain_stress": "projector/domain stress channel; can shift beta/readout/source normalization",
    }
    if "beta_minus_1" in induced:
        return channels.get(operator_family, "explicit beta-minus-one channel retained")
    return channels.get(operator_family, "indirect beta channel retained until zero or bound")


def r11_beta_vector_rows() -> list[dict[str, Any]]:
    source_path = ROOT / "source-intake" / "microscope" / "quarantine" / "1512" / "NON_EH_RESIDUAL_VECTOR_NONCLAIM.csv"
    source_rows = read_csv_rows(source_path)
    rows: list[dict[str, Any]] = []
    for index, source in enumerate(source_rows):
        vector_id = f"R11_2515_{index:02d}"
        operator_family = source["operator_family"]
        rows.append(
            base_row(
                score_ready=False,
                valid_prediction_row=False,
                claim_pass=False,
                operator_id=vector_id,
                source_vector_row=source["vector_id"],
                lock_status="ACTIVE_LOCAL_OPERATOR_BRANCH_UNTIL_ZERO_OR_BOUND",
                operator_family=operator_family,
                coefficient_symbol=source["coefficient_symbol"],
                current_coefficient=source["coefficient_value"],
                coefficient_units="MISSING_OPERATOR_NORMALIZATION_OR_ZERO_THEOREM",
                operator_form=source["operator_form"],
                beta_channel=beta_channel_for_family(operator_family, source["induced_observable"]),
                weak_field_map_status=source["weak_field_map"],
                induced_observable=source["induced_observable"],
                beta_comparator_bound=BETA_BOUND,
                beta_units="dimensionless beta_minus_1 after fixed observed GM",
                no_cancellation_policy="componentwise absolute envelope; no cancellation without parent identity",
                needed_to_remove=source["needed_to_remove"],
                source_file=source["source_file"],
                local_claim_status="RETAINED_NON_EH_RESIDUAL",
            )
        )
    return rows


def operator_map_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "map_id": "OMAP2515_0_beta",
            "observable": "beta_minus_1",
            "comparator_bound": BETA_BOUND,
            "units": "dimensionless",
            "operator_families": "boundary_topological_terms;R2_fR_scalar_mode;scalar_tensor_class_metric;bulk_X_force_law;source_normalization_operator;projector_domain_stress",
            "map_status": "MISSING_COEFFICIENTS_AND_WEAK_FIELD_MAPS",
            "claim_gate": "sum_abs(delta_beta_i) <= 7.8e-05 with no cancellation",
        },
        {
            "map_id": "OMAP2515_1_gamma",
            "observable": "gamma_minus_1",
            "comparator_bound": "2.3e-05",
            "units": "dimensionless",
            "operator_families": "boundary_topological_terms;R2_fR_scalar_mode;Ricci_Weyl_squared;scalar_tensor_class_metric;bulk_X_force_law",
            "map_status": "MISSING_COEFFICIENTS_AND_WEAK_FIELD_MAPS",
            "claim_gate": "gamma residual vector must use same fixed-GM convention",
        },
        {
            "map_id": "OMAP2515_2_R10",
            "observable": "alpha(lambda)",
            "comparator_bound": "R10_alpha_lambda_bound_curve_DIGITIZED.csv",
            "units": "dimensionless alpha versus meter-scale lambda",
            "operator_families": "R2_fR_scalar_mode;scalar_tensor_class_metric;bulk_X_force_law;nonlocal_memory_kernel",
            "map_status": "MISSING_RANGE_MASS_AND_KERNEL_MAP",
            "claim_gate": "numeric alpha(lambda) row must have parent coefficient, range, source coupling, and sourced bound curve",
        },
        {
            "map_id": "OMAP2515_3_preferred_frame",
            "observable": "alpha1;alpha2;alpha3;xi",
            "comparator_bound": "alpha1=1e-04;alpha2=2e-09;alpha3=4e-20;xi=4e-09",
            "units": "dimensionless",
            "operator_families": "vector_preferred_frame;boundary_topological_terms;source_normalization_operator;projector_domain_stress;nonlocal_memory_kernel",
            "map_status": "MISSING_VECTOR_FLUX_PROJECTOR_AND_DOMAIN_MAPS",
            "claim_gate": "each preferred-frame component requires theorem-zero or sourced coefficient/kernel",
        },
        {
            "map_id": "OMAP2515_4_WEP_clock_orbit",
            "observable": "eta_WEP;clock_residual;Gdot_over_G;orbital residuals",
            "comparator_bound": "arena-specific sourced bounds only",
            "units": "mixed; must be declared row-by-row",
            "operator_families": "torsion_nonmetricity;scalar_tensor_class_metric;bulk_X_force_law;nonlocal_memory_kernel",
            "map_status": "MISSING_ARENA_PROJECTIONS",
            "claim_gate": "no local-GR claim until WEP/clocks/orbits are either zeroed or bounded in the same parent branch",
        },
        {
            "map_id": "OMAP2515_5_verdict",
            "observable": "local_GR_operator_claim",
            "comparator_bound": "not a comparator row",
            "units": "logical gate",
            "operator_families": "all R11 families",
            "map_status": "BLOCKED_NONCLAIM",
            "claim_gate": "EH premises plus source/readout/boundary silence must all pass, otherwise R11 vector remains active",
        },
    ]
    return [base_row(score_ready=False, valid_prediction_row=False, claim_pass=False, **row) for row in rows]


def dryrun_result_rows() -> list[dict[str, Any]]:
    cases = [
        {
            "case_id": "DRY2515_0_use_EH_theorem",
            "case_description": "promote conditional Lovelock/EH theorem to MTS-owned local operator",
            "result_status": "REFUSED_PREMISES_UNSIGNED",
            "blocking_markers": "MISSING_4D_LOCAL_METRIC_ONLY_LC_SECOND_ORDER_NO_EXTRA_FIELD_SIGNATURE",
        },
        {
            "case_id": "DRY2515_1_ignore_R11",
            "case_description": "drop retained R11 families after quoting EH beta=1",
            "result_status": "REFUSED_NON_EH_OPERATOR_OMISSION",
            "blocking_markers": "R11_VECTOR_REQUIRED",
        },
        {
            "case_id": "DRY2515_2_score_beta",
            "case_description": "score beta against 7.8e-05 without coefficients and weak-field maps",
            "result_status": "REFUSED_COMPARATOR_WITHOUT_PREDICTION",
            "blocking_markers": "MISSING_NUMERIC_COEFFICIENTS;MISSING_WEAK_FIELD_MAPS",
        },
        {
            "case_id": "DRY2515_3_source_cancellation",
            "case_description": "cancel R11 operator pieces against source/readout pieces",
            "result_status": "REFUSED_UNSOURCED_CANCELLATION",
            "blocking_markers": "ABSOLUTE_ENVELOPE_REQUIRED",
        },
        {
            "case_id": "DRY2515_4_R2_first_row",
            "case_description": "select the first direct operator row for derivation or bound",
            "result_status": "ALLOWED_AS_NEXT_NONCLAIM_TARGET",
            "blocking_markers": "R2_FR_SCALAR_MODE_NEEDS_ZERO_THEOREM_OR_ALPHA_BETA_BOUND",
        },
    ]
    return [
        base_row(
            predicted_value="NOT_COMPUTED",
            comparator_bound=BETA_BOUND,
            pass_fail="BLOCKED_NONCLAIM",
            score_ready=False,
            valid_prediction_row=False,
            claim_pass=False,
            **case,
        )
        for case in cases
    ]


def decision_rows() -> list[dict[str, Any]]:
    decisions = [
        {
            "decision_id": "DEC2515_0_gain",
            "decision": "EH_SELECTION_THEOREM_RETAINED_AS_EXACT_CONDITIONAL",
            "rationale": "The Lovelock/EH route is a strong target reduction, but only after the parent branch signs every premise.",
            "status": "retained_reference",
        },
        {
            "decision_id": "DEC2515_1_limit",
            "decision": "NO_MTS_OWNED_EH_OPERATOR_CLAIM",
            "rationale": "Metric-only, Levi-Civita, second-order, no-extra-field, boundary, and source/readout clauses are not all parent-signed.",
            "status": "claim_blocked",
        },
        {
            "decision_id": "DEC2515_2_fallback",
            "decision": "R11_BETA_RESIDUAL_VECTOR_STAGED",
            "rationale": "Every retained non-EH family now has an explicit beta/gamma/R10/local-arena map slot and coefficient/zero requirement.",
            "status": "selected_nonclaim",
        },
        {
            "decision_id": "DEC2515_3_next",
            "decision": "ATTACK_R2_FR_SCALAR_MODE_FIRST",
            "rationale": "R2/f(R) is the cleanest direct violation of second-order EH selection and touches beta, gamma, and R10 at once.",
            "status": "selected",
        },
        {
            "decision_id": "DEC2515_4_claim",
            "decision": "NO_LOCAL_GR_OR_BETA_CLAIM",
            "rationale": "No R11 coefficient row is score-ready; all routes remain zero-theorem-or-bound work, not evidence of a pass.",
            "status": "enforced",
        },
    ]
    return [base_row(**decision) for decision in decisions]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            route_id="NEXT2515_0_selected",
            selection_status="selected",
            target_file="2516-Y5-R2FR-R2-fR-scalar-mode-zero-theorem-or-beta-alpha-bound.md",
            target_script="scripts/Y5_R2FR_R2_fR_scalar_mode_zero_theorem_or_beta_alpha_bound_2516.py",
            objective="try to derive a parent zero theorem for the R2/f(R) scalar-mode operator; if not, create finite beta/gamma/R10 alpha(lambda) coefficient and range slots",
            success_condition="R2/f(R) coefficient is theorem-zero or has sourced coefficient, scalar mass/range, weak-field beta/gamma map, R10 alpha(lambda) map, and valid_for_claim=false unless numeric",
            do_not_do="do not set c_R2 or c_fR to zero by preference; do not treat EH import as a parent zero theorem",
        ),
        base_row(
            route_id="NEXT2515_1_parallel_hold",
            selection_status="parallel_after_operator",
            target_file="2515b-Y5-R2FR-alpha3-source-exchange-current-owner-bound.md",
            target_script="scripts/Y5_R2FR_alpha3_source_exchange_current_owner_bound_2515b.py",
            objective="derive or bound alpha3 source-exchange/current-owner residual under the 4e-20 comparator",
            success_condition="alpha3 source-exchange row has current-owner theorem or finite coefficient/kernel rows",
            do_not_do="do not let beta/R2 work erase alpha3/source-current debt",
        ),
    ]


def branch_copy_rows() -> list[dict[str, Any]]:
    copies = [
        ("eh_premise_audit", OUTPUTS["eh_premise_audit"], BRANCH_COPIES["eh_premise_audit"]),
        ("r11_beta_vector", OUTPUTS["r11_beta_vector"], BRANCH_COPIES["r11_beta_vector"]),
        ("operator_map", OUTPUTS["operator_map"], BRANCH_COPIES["operator_map"]),
        ("next_target", OUTPUTS["next_target"], BRANCH_COPIES["next_target"]),
    ]
    rows: list[dict[str, Any]] = []
    for copy_id, source, destination in copies:
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, destination)
        ok, count, message = csv_rows_parse(destination)
        rows.append(
            base_row(
                copy_id=copy_id,
                source=str(source.relative_to(ROOT)),
                destination=str(destination.relative_to(ROOT)),
                copied=destination.exists(),
                parse_ok=ok,
                row_count=count,
                parse_message=message,
            )
        )
    return rows


def falsey(value: Any) -> bool:
    return str(value).strip().lower() in {"false", "0", "no", "not_computed", ""}


def no_claim_flags(rows_by_name: dict[str, list[dict[str, Any]]]) -> bool:
    for name, rows in rows_by_name.items():
        if name in {"source_register", "validation"}:
            continue
        for row in rows:
            for key in ("valid_for_claim", "claim_allowed", "score_ready", "valid_prediction_row", "claim_pass"):
                if key in row and not falsey(row[key]):
                    return False
    return True


def validation_rows(rows_by_name: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    checks: list[dict[str, Any]] = []

    def add(check_id: str, status: bool, detail: str = "") -> None:
        checks.append(
            base_row(
                check_id=check_id,
                status="PASS" if status else "FAIL",
                detail=detail,
                valid_for_claim=False,
                claim_allowed=False,
            )
        )

    source_rows = rows_by_name["source_register"]
    add("VAL2515_00_sources_exist", all(str(row["path_exists"]) == "True" for row in source_rows))
    add("VAL2515_01_source_needles", all(str(row["source_pass"]) == "True" for row in source_rows))
    add(
        "VAL2515_02_eh_premises_unsigned",
        any(row["premise_id"] == "EHP2515_7_verdict" and row["current_signature_status"] == "EH_PREMISES_NOT_PARENT_SIGNED_R11_VECTOR_REQUIRED" for row in rows_by_name["eh_premise_audit"])
        and all("SIGNED" not in row["current_signature_status"] or row["current_signature_status"] == "NOT_PARENT_SIGNED" for row in rows_by_name["eh_premise_audit"] if row["premise_id"] != "EHP2515_7_verdict"),
        "EH theorem retained, but parent premises are not signed",
    )
    add(
        "VAL2515_03_r11_vector_complete",
        len(rows_by_name["r11_beta_vector"]) == 10
        and any(row["operator_family"] == "R2_fR_scalar_mode" for row in rows_by_name["r11_beta_vector"])
        and all(str(row["score_ready"]) == "False" for row in rows_by_name["r11_beta_vector"]),
        "ten R11 families retained as nonclaim rows",
    )
    add(
        "VAL2515_04_maps_cover_beta_gamma_R10",
        all(
            any(row["observable"] == observable for row in rows_by_name["operator_map"])
            for observable in ["beta_minus_1", "gamma_minus_1", "alpha(lambda)"]
        ),
        "beta/gamma/R10 map slots present",
    )
    add(
        "VAL2515_05_dryruns_block_claims",
        all(str(row["pass_fail"]) == "BLOCKED_NONCLAIM" and str(row["claim_pass"]) == "False" for row in rows_by_name["dryrun_results"]),
        "all dry runs remain nonclaim",
    )
    add(
        "VAL2515_06_next_target",
        any(row["route_id"] == "NEXT2515_0_selected" and "R2-fR" in row["target_file"] for row in rows_by_name["next_target"]),
        "R2/f(R) scalar-mode first row selected",
    )
    add("VAL2515_07_no_claim_flags", no_claim_flags(rows_by_name))
    add(
        "VAL2515_08_branch_copies",
        all(str(row["copied"]) == "True" and str(row["parse_ok"]) == "True" for row in rows_by_name["branch_copies"]),
    )
    formalization = ROOT.parent / "formalization-workbench"
    formalization_hits = list(formalization.rglob("*2515*")) if formalization.exists() else []
    add(
        "VAL2515_09_no_formalization_artifacts",
        len(formalization_hits) == 0,
        ";".join(str(path) for path in formalization_hits),
    )
    add("VAL2515_10_pycache_absent", not (Path(__file__).resolve().parent / "__pycache__").exists())

    for name, path in OUTPUTS.items():
        if name == "validation":
            continue
        ok, count, message = csv_rows_parse(path)
        add(f"VAL2515_CSV_{path.stem}", ok, f"{message}; rows={count}")
    for key, path in BRANCH_COPIES.items():
        ok, count, message = csv_rows_parse(path)
        add(f"VAL2515_COPY_CSV_{key}", ok, f"{message}; rows={count}")

    overall = all(row["status"] == "PASS" for row in checks)
    checks.append(
        base_row(
            check_id="VAL2515_OVERALL",
            status="PASS" if overall else "FAIL",
            detail="2515 refuses MTS-owned EH import, retains all R11 operator families as beta/gamma/R10 residual slots, and selects R2/f(R) scalar mode next",
            valid_for_claim=False,
            claim_allowed=False,
        )
    )
    return checks


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    DOC.write_text(
        "\n".join(
            [
                "# 2515 - EH Operator Premise Signature or R11 Beta Residual Vector",
                "",
                "**Current verdict:** the EH/Lovelock theorem remains a clean conditional reduction route, but MTS still does not own it. The parent branch has not signed the metric-only, Levi-Civita, second-order, no-extra-field, harmless-boundary, and source/readout clauses together.",
                "",
                "**Main gain:** the non-EH debt is no longer vague. Each retained R11 family now has an explicit coefficient slot, weak-field map debt, beta/gamma/R10 or local-arena observable link, comparator gate, and no-cancellation policy.",
                "",
                "**Claim discipline:** no local-GR, beta, R10, WEP, clock, orbit, or preferred-frame pass is claimed from this checkpoint. This is a map for the next derivations and bounds.",
                "",
                "## Source Register",
                md_table(rows_by_name["source_register"], ["source_id", "source_path", "path_exists", "found_needles", "source_pass", "role"]),
                "",
                "## EH Premise Signature Audit",
                md_table(rows_by_name["eh_premise_audit"], ["premise_id", "premise", "current_signature_status", "current_evidence", "needed_signature", "effect_if_signed"]),
                "",
                "## R11 Beta Residual Vector",
                md_table(rows_by_name["r11_beta_vector"], ["operator_id", "source_vector_row", "operator_family", "coefficient_symbol", "current_coefficient", "beta_channel", "weak_field_map_status", "induced_observable", "needed_to_remove"]),
                "",
                "## Operator To Observable Map",
                md_table(rows_by_name["operator_map"], ["map_id", "observable", "comparator_bound", "operator_families", "map_status", "claim_gate"]),
                "",
                "## Nonclaim Dry Run",
                md_table(rows_by_name["dryrun_results"], ["case_id", "case_description", "result_status", "blocking_markers", "pass_fail", "claim_pass"]),
                "",
                "## Decision Ledger",
                md_table(rows_by_name["decision_ledger"], ["decision_id", "decision", "rationale", "status"]),
                "",
                "## Next Target",
                md_table(rows_by_name["next_target"], ["route_id", "selection_status", "target_file", "target_script", "objective", "success_condition", "do_not_do"]),
                "",
                "## Validation",
                md_table(rows_by_name["validation"], ["check_id", "status", "detail"]),
                "",
            ]
        ),
        encoding="utf-8",
    )


def main() -> None:
    remove_pycache()
    rows_by_name: dict[str, list[dict[str, Any]]] = {
        "source_register": source_register_rows(),
        "eh_premise_audit": eh_premise_rows(),
        "r11_beta_vector": r11_beta_vector_rows(),
        "operator_map": operator_map_rows(),
        "dryrun_results": dryrun_result_rows(),
        "decision_ledger": decision_rows(),
        "next_target": next_target_rows(),
    }

    for name, rows in rows_by_name.items():
        write_csv(OUTPUTS[name], rows)

    rows_by_name["branch_copies"] = branch_copy_rows()
    write_csv(OUTPUTS["branch_copies"], rows_by_name["branch_copies"])

    rows_by_name["validation"] = validation_rows(rows_by_name)
    write_csv(OUTPUTS["validation"], rows_by_name["validation"])
    write_doc(rows_by_name)
    remove_pycache()

    print(f"wrote {DOC}")
    for name, path in OUTPUTS.items():
        print(f"wrote {name}: {path}")
    for key, path in BRANCH_COPIES.items():
        print(f"copied {key}: {path}")


if __name__ == "__main__":
    main()
