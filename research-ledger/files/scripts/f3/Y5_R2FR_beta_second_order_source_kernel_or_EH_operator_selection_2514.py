from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
BRANCH_ID = "MTS_R2FR_BETA_SECOND_ORDER_SOURCE_KERNEL_OR_EH_OPERATOR_2514"
CHECKPOINT_ID = "2514"
DOC = ROOT / "2514-Y5-R2FR-beta-second-order-source-kernel-or-EH-operator-selection.md"
MTS_RESIDUALS = ROOT / "source-intake" / "mts_residuals"

OUTPUTS = {
    "source_register": MTS_RESIDUALS / "P8_Y5_NO_SHADOW_2514_SOURCE_REGISTER.csv",
    "beta_gate": MTS_RESIDUALS / "P8_Y5_NO_SHADOW_2514_BETA_SECOND_ORDER_GATE.csv",
    "eh_import_audit": MTS_RESIDUALS / "P8_Y5_NO_SHADOW_2514_EH_IMPORT_AUDIT.csv",
    "finite_beta_vector": MTS_RESIDUALS / "P8_Y5_NO_SHADOW_2514_FINITE_BETA_SOURCE_VECTOR.csv",
    "operator_selection": MTS_RESIDUALS / "P8_Y5_NO_SHADOW_2514_EH_OPERATOR_SELECTION_QUEUE.csv",
    "dryrun_results": MTS_RESIDUALS / "P8_Y5_NO_SHADOW_2514_NONCLAIM_DRYRUN_RESULTS.csv",
    "decision_ledger": MTS_RESIDUALS / "P8_Y5_NO_SHADOW_2514_DECISION_LEDGER.csv",
    "next_target": MTS_RESIDUALS / "P8_Y5_NO_SHADOW_2514_NEXT_TARGET.csv",
    "branch_copies": MTS_RESIDUALS / "P8_Y5_NO_SHADOW_2514_BRANCH_COPIES.csv",
    "validation": MTS_RESIDUALS / "P8_Y5_BRR545_2514_VALIDATION.csv",
}

BRANCH_COPIES = {
    "beta_gate": ROOT
    / "source-intake"
    / "local_bounds"
    / "Beta_second_order_source_kernel_gate_2514_NONCLAIM.csv",
    "eh_import": ROOT
    / "source-intake"
    / "beta-source"
    / "docs"
    / "EH_import_beta_audit_2514_NONCLAIM.csv",
    "finite_vector": ROOT
    / "source-intake"
    / "beta-source"
    / "docs"
    / "Finite_beta_source_vector_2514_NONCLAIM.csv",
    "operator_next": ROOT
    / "source-intake"
    / "rab-sector"
    / "acquisition-queue"
    / "JR2514_EH_OPERATOR_OR_R11_BETA_NEXT_NONCLAIM.csv",
}

SOURCE_SPECS = [
    {
        "source_id": "SRC2514_0_2513_next",
        "path": "2513-Y5-R2FR-source-weight-PPN-response-kernel-fixed-GM-map.md",
        "needles": ["NEXT2513_0_selected", "beta is the leading GR gate"],
        "role": "authoritative selection of beta second-order source kernel",
    },
    {
        "source_id": "SRC2514_1_beta_gate_2500",
        "path": "source-intake/local_bounds/Beta_second_order_gate_2500_NONCLAIM.csv",
        "needles": ["BETA2500_1_EH_conditional", "BETA2500_4_verdict"],
        "role": "existing beta gate: EH conditional pass, MTS beta closure blocked",
    },
    {
        "source_id": "SRC2514_2_ppn_requirements_2500",
        "path": "source-intake/local_bounds/Full_PPN_vector_requirements_2500_NONCLAIM.csv",
        "needles": ["VREQ2500_2_beta", "VREQ2500_6_total_no_cancellation"],
        "role": "full PPN vector claim requirements",
    },
    {
        "source_id": "SRC2514_3_eh_ppn_2505",
        "path": "source-intake/beta-source/docs/PPN_readout_vector_2505_NONCLAIM.csv",
        "needles": ["PPN2505_2_beta_law", "BETA_LAW_MATCHES_EH"],
        "role": "EH internal beta=1 and kappa_v=0 readout",
    },
    {
        "source_id": "SRC2514_4_2505_doc",
        "path": "2505-Y5-R2FR-EH-fixed-point-to-v-action-coefficient-extraction-or-GR-import-demotion.md",
        "needles": ["conditional EH inheritance", "MTS ownership blocked"],
        "role": "EH-to-v extraction is clean but not MTS-owned",
    },
    {
        "source_id": "SRC2514_5_2506_doc",
        "path": "2506-Y5-R2FR-parent-EH-descent-source-glue-proof-or-explicit-GR-import-demotion.md",
        "needles": ["GR/EH import plus explicit MTS residual interface", "THM2506_0_parent_split"],
        "role": "conditional EH descent theorem and import label",
    },
    {
        "source_id": "SRC2514_6_eh_selection_1512",
        "path": "source-intake/microscope/quarantine/1512/EH_SELECTION_THEOREM_ATTEMPT_NONCLAIM.csv",
        "needles": ["THM1512_0_conditional_EH_selection", "NON_EH_VECTOR_REQUIRED"],
        "role": "Lovelock-style EH selection shape, premises unsigned",
    },
    {
        "source_id": "SRC2514_7_non_eh_vector_1512",
        "path": "source-intake/microscope/quarantine/1512/NON_EH_RESIDUAL_VECTOR_NONCLAIM.csv",
        "needles": ["R11_1512_01", "RETAINED_NON_EH_RESIDUAL"],
        "role": "non-EH operator families retained as beta/gamma/R10 residuals",
    },
    {
        "source_id": "SRC2514_8_ward_ppn_1561",
        "path": "source-intake/microscope/quarantine/1561/WARD_PPN_GATE_NONCLAIM.csv",
        "needles": ["WPPN1561_2_beta", "CONDITIONAL_UNSIGNED"],
        "role": "Ward/PPN beta gate: EH beta works only after source/readout ownership",
    },
    {
        "source_id": "SRC2514_9_beta_template_1885",
        "path": "source-intake/beta-source/docs/BETA1885_SOURCE_COUPLING_OR_PARENT_ZERO_TEMPLATE_NONCLAIM.csv",
        "needles": ["BETA1885_TEMPLATE_FINITE_VECTOR", "MISSING_NUMERIC_DELTA_BETA_SOURCE"],
        "role": "finite beta vector template and comparator bound",
    },
    {
        "source_id": "SRC2514_10_kernel_2513",
        "path": "source-intake/mts_residuals/P8_Y5_NO_SHADOW_2513_PPN_SOURCE_WEIGHT_KERNEL_MATRIX.csv",
        "needles": ["PPNK2513_1_beta_source_weight", "MISSING_BETA_SECOND_ORDER_SOURCE_KERNEL"],
        "role": "2513 PPN source-weight matrix beta row",
    },
]


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


def beta_gate_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "gate_id": "BETA2514_0_definition",
            "object": "delta_beta_total",
            "statement": "beta_minus_1 is the second-order g00 residual after fixed measured-GM normalization",
            "mathematical_form": "g_00=-1+2U/c^2-2 beta U^2/c^4+O(c^-6)",
            "status": "PPN_DICTIONARY_LOCKED",
            "missing_for_claim": "source-normalized U^2 coefficient and readout/GM transfer",
        },
        {
            "gate_id": "BETA2514_1_EH_internal",
            "object": "beta_EH",
            "statement": "inside the EH fixed point, Schwarzschild/isotropic weak field gives beta=1 and kappa_v=0",
            "mathematical_form": "A_iso=1-2x+2x^2+O(x^3); beta=1",
            "status": "EXACT_INSIDE_EH_FIXED_POINT",
            "missing_for_claim": "MTS parent must own EH operator, source glue, and readout",
        },
        {
            "gate_id": "BETA2514_2_MTS_owner",
            "object": "beta_MTS_owned",
            "statement": "MTS owns beta=1 only if parent action selects EH locally and all source/readout/non-EH tails vanish or are bounded",
            "mathematical_form": "delta_beta_total = delta_beta_EH_import_guard + delta_beta_source + delta_beta_operator + delta_beta_readout + delta_beta_boundary",
            "status": "NOT_DERIVED_CURRENT_CORPUS",
            "missing_for_claim": "EH selection premises, PiM/Hilbert source equality, boundary silence, extra-sector double zeros",
        },
        {
            "gate_id": "BETA2514_3_finite_kernel",
            "object": "finite beta source kernel",
            "statement": "if beta is not parent-zero, retain a finite absolute beta vector against the 7.8e-05 comparator",
            "mathematical_form": "Delta_beta_abs=sum_i |delta_beta_i| <= 7.8e-05",
            "status": "SCHEMA_READY_VALUES_MISSING",
            "missing_for_claim": "numeric or theorem-zero rows for every component",
        },
        {
            "gate_id": "BETA2514_4_verdict",
            "object": "beta local-GR gate",
            "statement": "beta closure remains EH-import conditional, not MTS-owned",
            "mathematical_form": "beta=1 is allowed only inside labeled EH import or after parent EH/operator/source/readout package signs",
            "status": "BETA_CLOSURE_NOT_DERIVED_CURRENT_CORPUS",
            "missing_for_claim": "parent package or finite beta vector",
        },
    ]
    return [base_row(score_ready=False, valid_prediction_row=False, **row) for row in rows]


def eh_import_audit_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "audit_id": "EH2514_0_import_allowed",
            "claim": "EH gives beta=1",
            "status": "ALLOWED_AS_REFERENCE_OR_IMPORT",
            "condition": "label explicitly as EH/GR fixed-point inheritance",
            "claim_ceiling": "not MTS-owned local GR",
        },
        {
            "audit_id": "EH2514_1_operator_selection",
            "claim": "MTS parent local exterior operator is EH",
            "status": "NOT_PARENT_SIGNED",
            "condition": "4D local diffeo-invariant metric-only Levi-Civita second-order no-extra-field premises",
            "claim_ceiling": "retain non-EH residual vector",
        },
        {
            "audit_id": "EH2514_2_source_glue",
            "claim": "same Hilbert/Hamiltonian/PiM source fixes U through second order",
            "status": "NOT_PARENT_SIGNED",
            "condition": "PiM/Hilbert equality, source measure glue, worldtube/reference ownership",
            "claim_ceiling": "beta source kernel remains open",
        },
        {
            "audit_id": "EH2514_3_readout",
            "claim": "PPN readout/gauge map does not shift beta",
            "status": "NOT_PARENT_SIGNED",
            "condition": "fixed-before-readout, radial/coframe gauge ownership, measured-GM convention",
            "claim_ceiling": "readout beta tail remains finite row",
        },
        {
            "audit_id": "EH2514_4_verdict",
            "claim": "MTS derives beta=1",
            "status": "REJECTED_FOR_CURRENT_CORPUS",
            "condition": "all prior clauses must pass together",
            "claim_ceiling": "EH_IMPORT_PLUS_BETA_RESIDUAL_INTERFACE",
        },
    ]
    return [base_row(score_ready=False, valid_prediction_row=False, **row) for row in rows]


def finite_beta_vector_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "component_id": "DBETA2514_0_source",
            "symbol": "delta_beta_source",
            "definition": "second-order beta residual from relative source weights/source normalization after fixed GM quotient",
            "required_input": "source-current descent/no-source-only theorem or finite source-weight kernel",
            "current_status": "MISSING_NUMERIC_DELTA_BETA_SOURCE",
        },
        {
            "component_id": "DBETA2514_1_operator",
            "symbol": "delta_beta_operator",
            "definition": "second-order beta residual from non-EH local operator families",
            "required_input": "EH operator selection theorem or R11 operator coefficient vector",
            "current_status": "MISSING_NUMERIC_DELTA_BETA_OPERATOR",
        },
        {
            "component_id": "DBETA2514_2_q_loc",
            "symbol": "delta_beta_q_loc",
            "definition": "beta residual from q_loc/local projection source coupling",
            "required_input": "q_loc theorem-zero or beta projection kernel",
            "current_status": "MISSING_NUMERIC_DELTA_BETA_Q_LOC",
        },
        {
            "component_id": "DBETA2514_3_boundary_domain",
            "symbol": "delta_beta_boundary_domain",
            "definition": "boundary, reference, domain, and projector-stress beta residual",
            "required_input": "boundary/reference silence theorem or finite beta boundary row",
            "current_status": "MISSING_NUMERIC_DELTA_BETA_BOUNDARY_DOMAIN",
        },
        {
            "component_id": "DBETA2514_4_readout",
            "symbol": "delta_beta_readout",
            "definition": "PPN gauge/readout/radial coframe beta transfer tail",
            "required_input": "fixed-before-readout theorem or finite readout-gauge beta row",
            "current_status": "MISSING_NUMERIC_DELTA_BETA_READOUT",
        },
        {
            "component_id": "DBETA2514_5_SN",
            "symbol": "epsilon_SN",
            "definition": "source-normalization stability through second PPN order",
            "required_input": "same measured source mass through U and U^2 terms",
            "current_status": "MISSING_NUMERIC_EPSILON_SN",
        },
        {
            "component_id": "DBETA2514_6_total_abs",
            "symbol": "Delta_beta_total_abs",
            "definition": "componentwise absolute beta envelope compared to beta bound",
            "required_input": "all component values/theorem-zeros with no cancellation",
            "current_status": "MISSING_SUM_ABS_VECTOR",
        },
    ]
    return [
        base_row(
            beta_bound="7.8e-05",
            units="dimensionless",
            GM_convention="fixed observed U=G_obs M_obs/r; one common calibration only",
            score_ready=False,
            valid_prediction_row=False,
            claim_pass=False,
            **row,
        )
        for row in rows
    ]


def operator_selection_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "operator_id": "OP2514_0_EH_lovelock",
            "target": "EH local operator",
            "theorem_shape": "4D local diffeo-invariant metric-only Levi-Civita second-order equations imply EH plus Lambda/topological boundary terms",
            "current_status": "EXACT_CONDITIONAL_ROUTE_PREMISES_UNSIGNED",
            "beta_effect": "would remove delta_beta_operator if source/readout clauses also pass",
        },
        {
            "operator_id": "OP2514_1_R2_fR",
            "target": "R2/f(R) scalar mode",
            "theorem_shape": "exclude higher-derivative scalar mode or provide finite coefficient/range map",
            "current_status": "RETAINED_NON_EH_RESIDUAL",
            "beta_effect": "can shift gamma and beta and create finite-range/R10 tail",
        },
        {
            "operator_id": "OP2514_2_scalar_tensor",
            "target": "scalar-tensor metric class",
            "theorem_shape": "exclude F(phi)R/source scalar or provide PPN/clock/Gdot/R10 map",
            "current_status": "RETAINED_NON_EH_RESIDUAL",
            "beta_effect": "can move beta through scalar self-interaction/source response",
        },
        {
            "operator_id": "OP2514_3_torsion_nonmetricity",
            "target": "torsion/nonmetricity operator",
            "theorem_shape": "prove Levi-Civita/no-hypermomentum branch or bound connection-current effects",
            "current_status": "RETAINED_NON_EH_RESIDUAL",
            "beta_effect": "can enter beta through non-Hilbert current/readout channels",
        },
        {
            "operator_id": "OP2514_4_boundary_projector",
            "target": "boundary/projector/domain stress",
            "theorem_shape": "prove zero boundary/reference/projector stress or provide finite beta-equivalent row",
            "current_status": "RETAINED_NON_EH_RESIDUAL",
            "beta_effect": "can shift U^2/source-normalization after first-order Newton match",
        },
        {
            "operator_id": "OP2514_5_verdict",
            "target": "operator selection next",
            "theorem_shape": "beta derivation reduces to EH operator selection plus source/readout glue",
            "current_status": "EH_OPERATOR_SELECTION_OR_R11_BETA_VECTOR_REQUIRED",
            "beta_effect": "selected next route",
        },
    ]
    return [base_row(score_ready=False, valid_prediction_row=False, **row) for row in rows]


def dryrun_result_rows() -> list[dict[str, Any]]:
    cases = [
        {
            "case_id": "DRY2514_0_gamma_to_beta",
            "case_description": "infer beta=1 from gamma/WEP/Newton first order",
            "result_status": "REFUSED_SECOND_ORDER_SHORTCUT",
            "blocking_markers": "MISSING_SECOND_ORDER_SOURCE_KERNEL",
        },
        {
            "case_id": "DRY2514_1_import_schwarzschild",
            "case_description": "use Schwarzschild/EH beta=1 as MTS-owned result",
            "result_status": "REFUSED_GR_IMPORT_AS_MTS_DERIVATION",
            "blocking_markers": "MISSING_PARENT_EH_SELECTION;MISSING_SOURCE_GLUE",
        },
        {
            "case_id": "DRY2514_2_beta_bound_only",
            "case_description": "use beta comparator bound without a prediction vector",
            "result_status": "REFUSED_COMPARATOR_WITHOUT_PREDICTION",
            "blocking_markers": "MISSING_DELTA_BETA_VECTOR",
        },
        {
            "case_id": "DRY2514_3_nonEH_ignore",
            "case_description": "ignore R11/non-EH operator families after EH reference calculation",
            "result_status": "REFUSED_NON_EH_OPERATOR_OMISSION",
            "blocking_markers": "NON_EH_VECTOR_REQUIRED",
        },
        {
            "case_id": "DRY2514_4_cancellation",
            "case_description": "cancel beta source/operator/readout pieces without parent identity",
            "result_status": "REFUSED_UNSOURCED_CANCELLATION",
            "blocking_markers": "ABSOLUTE_ENVELOPE_REQUIRED",
        },
    ]
    return [
        base_row(
            predicted_value="NOT_COMPUTED",
            comparator_bound="7.8e-05",
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
            "decision_id": "DEC2514_0_gain",
            "decision": "BETA_EH_INTERNAL_DERIVATION_RETAINED",
            "rationale": "Inside EH, beta=1 and kappa_v=0 remain clean and useful as the target reduction.",
            "status": "retained_reference",
        },
        {
            "decision_id": "DEC2514_1_limit",
            "decision": "BETA_NOT_MTS_OWNED",
            "rationale": "MTS has not signed EH operator selection, source glue, boundary silence, or readout transfer.",
            "status": "claim_blocked",
        },
        {
            "decision_id": "DEC2514_2_fallback",
            "decision": "FINITE_BETA_VECTOR_STAGED",
            "rationale": "If beta cannot be parent-zero, every second-order source/operator/readout piece must be bounded componentwise.",
            "status": "selected_nonclaim",
        },
        {
            "decision_id": "DEC2514_3_best_next",
            "decision": "EH_OPERATOR_SELECTION_OR_R11_BETA_VECTOR",
            "rationale": "The beta problem reduces to the left-hand operator theorem plus retained non-EH operator coefficients.",
            "status": "selected",
        },
        {
            "decision_id": "DEC2514_4_claim",
            "decision": "NO_BETA_OR_LOCAL_GR_CLAIM",
            "rationale": "No beta prediction row is score-ready and all import routes remain labeled.",
            "status": "enforced",
        },
    ]
    return [base_row(**decision) for decision in decisions]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            route_id="NEXT2514_0_selected",
            selection_status="selected",
            target_file="2515-Y5-R2FR-EH-operator-premise-signature-or-R11-beta-residual-vector.md",
            target_script="scripts/Y5_R2FR_EH_operator_premise_signature_or_R11_beta_residual_vector_2515.py",
            objective="try to sign the EH/Lovelock premises from the parent branch; if not, build the R11 non-EH operator beta residual vector with coefficient slots, weak-field maps, and comparator gates",
            success_condition="each EH premise is signed or each retained non-EH operator has a beta/gamma/R10 map, units, source path, no-cancellation policy, and valid_for_claim=false unless real",
            do_not_do="do not import EH as MTS-owned; do not ignore R2/fR, scalar-tensor, torsion/nonmetricity, boundary/projector, or source-normalization operators",
        ),
        base_row(
            route_id="NEXT2514_1_parallel",
            selection_status="parallel_after_operator",
            target_file="2515b-Y5-R2FR-alpha3-source-exchange-current-owner-bound.md",
            target_script="scripts/Y5_R2FR_alpha3_source_exchange_current_owner_bound_2515b.py",
            objective="derive or bound alpha3 source-exchange/current-owner residual under the 4e-20 comparator",
            success_condition="alpha3 source-exchange row has current-owner theorem or finite coefficient/kernel rows",
            do_not_do="do not let beta work erase alpha3/source-current debt",
        ),
    ]


def branch_copy_rows() -> list[dict[str, Any]]:
    copies = [
        ("beta_gate", OUTPUTS["beta_gate"], BRANCH_COPIES["beta_gate"]),
        ("eh_import", OUTPUTS["eh_import_audit"], BRANCH_COPIES["eh_import"]),
        ("finite_vector", OUTPUTS["finite_beta_vector"], BRANCH_COPIES["finite_vector"]),
        ("operator_next", OUTPUTS["next_target"], BRANCH_COPIES["operator_next"]),
    ]
    rows: list[dict[str, Any]] = []
    for copy_id, src, dst in copies:
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(src, dst)
        ok, count, message = csv_rows_parse(dst)
        rows.append(
            base_row(
                copy_id=copy_id,
                source=str(src.relative_to(ROOT)),
                destination=str(dst.relative_to(ROOT)),
                copied=dst.exists(),
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
    add("VAL2514_00_sources_exist", all(str(row["path_exists"]) == "True" for row in source_rows))
    add("VAL2514_01_source_needles", all(str(row["source_pass"]) == "True" for row in source_rows))
    add(
        "VAL2514_02_eh_internal",
        any(row["gate_id"] == "BETA2514_1_EH_internal" and row["status"] == "EXACT_INSIDE_EH_FIXED_POINT" for row in rows_by_name["beta_gate"]),
        "EH beta internal derivation retained",
    )
    add(
        "VAL2514_03_mts_blocked",
        any(row["gate_id"] == "BETA2514_4_verdict" and row["status"] == "BETA_CLOSURE_NOT_DERIVED_CURRENT_CORPUS" for row in rows_by_name["beta_gate"]),
        "MTS beta claim blocked",
    )
    add(
        "VAL2514_04_finite_vector",
        any(row["component_id"] == "DBETA2514_6_total_abs" for row in rows_by_name["finite_beta_vector"])
        and all(str(row["score_ready"]) == "False" for row in rows_by_name["finite_beta_vector"]),
        "finite beta vector staged nonclaim",
    )
    add(
        "VAL2514_05_operator_queue",
        any(row["operator_id"] == "OP2514_5_verdict" and row["current_status"] == "EH_OPERATOR_SELECTION_OR_R11_BETA_VECTOR_REQUIRED" for row in rows_by_name["operator_selection"]),
        "operator/R11 next queue present",
    )
    add(
        "VAL2514_06_dryruns_block_claims",
        all(str(row["pass_fail"]) == "BLOCKED_NONCLAIM" and str(row["claim_pass"]) == "False" for row in rows_by_name["dryrun_results"]),
        "all dry runs nonclaim",
    )
    add(
        "VAL2514_07_next_target",
        any(row["route_id"] == "NEXT2514_0_selected" for row in rows_by_name["next_target"]),
        "2515 operator/R11 target selected",
    )
    add("VAL2514_08_no_claim_flags", no_claim_flags(rows_by_name))
    add(
        "VAL2514_09_branch_copies",
        all(str(row["copied"]) == "True" and str(row["parse_ok"]) == "True" for row in rows_by_name["branch_copies"]),
    )
    formalization = ROOT.parent / "formalization-workbench"
    formalization_hits = list(formalization.rglob("*2514*")) if formalization.exists() else []
    add(
        "VAL2514_10_no_formalization_artifacts",
        len(formalization_hits) == 0,
        ";".join(str(path) for path in formalization_hits),
    )
    add("VAL2514_11_pycache_absent", not (Path(__file__).resolve().parent / "__pycache__").exists())

    for name, path in OUTPUTS.items():
        if name == "validation":
            continue
        ok, count, message = csv_rows_parse(path)
        add(f"VAL2514_CSV_{path.stem}", ok, f"{message}; rows={count}")
    for key, path in BRANCH_COPIES.items():
        ok, count, message = csv_rows_parse(path)
        add(f"VAL2514_COPY_CSV_{key}", ok, f"{message}; rows={count}")

    overall = all(row["status"] == "PASS" for row in checks)
    checks.append(
        base_row(
            check_id="VAL2514_OVERALL",
            status="PASS" if overall else "FAIL",
            detail="2514 preserves EH beta=1 as import/reference, blocks MTS-owned beta, and selects EH operator/R11 beta vector next",
            valid_for_claim=False,
            claim_allowed=False,
        )
    )
    return checks


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    DOC.write_text(
        "\n".join(
            [
                "# 2514 — Beta Second-Order Source Kernel or EH Operator Selection",
                "",
                "**Current verdict:** beta is clean inside the EH fixed point, but not yet MTS-owned. The exact EH result `beta=1` is retained as the target reduction/import branch; the active MTS branch still needs EH operator selection, source glue, boundary silence, extra-sector silence, and readout/GM transfer.",
                "",
                "**Why this matters:** first-order Newton/gamma success cannot give beta. Beta is a second-order `U^2` test of the left-hand operator, source normalization, and readout convention.",
                "",
                "**Next pressure point:** either sign the EH/Lovelock premises from the parent branch, or keep a finite `Delta_beta_abs` vector for R11/non-EH operator families.",
                "",
                "## Source Register",
                md_table(rows_by_name["source_register"], ["source_id", "source_path", "path_exists", "found_needles", "source_pass", "role"]),
                "",
                "## Beta Second-Order Gate",
                md_table(rows_by_name["beta_gate"], ["gate_id", "object", "statement", "mathematical_form", "status", "missing_for_claim"]),
                "",
                "## EH Import Audit",
                md_table(rows_by_name["eh_import_audit"], ["audit_id", "claim", "status", "condition", "claim_ceiling"]),
                "",
                "## Finite Beta Source Vector",
                md_table(rows_by_name["finite_beta_vector"], ["component_id", "symbol", "definition", "required_input", "current_status", "beta_bound"]),
                "",
                "## EH Operator Selection Queue",
                md_table(rows_by_name["operator_selection"], ["operator_id", "target", "theorem_shape", "current_status", "beta_effect"]),
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
        "beta_gate": beta_gate_rows(),
        "eh_import_audit": eh_import_audit_rows(),
        "finite_beta_vector": finite_beta_vector_rows(),
        "operator_selection": operator_selection_rows(),
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
