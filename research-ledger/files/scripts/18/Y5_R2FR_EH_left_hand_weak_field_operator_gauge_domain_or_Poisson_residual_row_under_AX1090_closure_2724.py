from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SCRIPT_START_UTC = datetime.now(timezone.utc)

ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
SOURCE_WEIGHT = ROOT / "source-intake" / "source-weight"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
FORMALIZATION = ROOT.parent / "formalization-workbench"

DOC = ROOT / "2724-Y5-R2FR-EH-left-hand-weak-field-operator-gauge-domain-or-Poisson-residual-row-under-AX1090-closure.md"

OUTPUTS = {
    "source_register": RESIDUALS / "P8_Y5_R2FR_2724_SOURCE_REGISTER.csv",
    "operator_audit": RESIDUALS / "P8_Y5_R2FR_2724_EH_LEFT_HAND_AUDIT.csv",
    "theorem_attempt": RESIDUALS / "P8_Y5_R2FR_2724_OPERATOR_THEOREM_ATTEMPT.csv",
    "finite_rows": RESIDUALS / "P8_Y5_R2FR_2724_FINITE_POISSON_OPERATOR_ROWS_NONCLAIM.csv",
    "ejeff_update": RESIDUALS / "P8_Y5_R2FR_2724_EJEFF_UPDATE_VECTOR_NONCLAIM.csv",
    "claim_gates": RESIDUALS / "P8_Y5_R2FR_2724_CLAIM_GATES.csv",
    "blocker_stack": RESIDUALS / "P8_Y5_R2FR_2724_CURRENT_BLOCKER_STACK.csv",
    "decision_ledger": RESIDUALS / "P8_Y5_R2FR_2724_DECISION_LEDGER.csv",
    "next_target": RESIDUALS / "P8_Y5_R2FR_2724_NEXT_TARGET.csv",
    "project_snapshot": RESIDUALS / "P8_Y5_R2FR_2724_PROJECT_STATUS_SNAPSHOT.csv",
    "branch_copies": RESIDUALS / "P8_Y5_R2FR_2724_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2724_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "local_bounds": LOCAL_BOUNDS / "EH_left_hand_Poisson_residual_rows_2724_NONCLAIM.csv",
    "source_weight": SOURCE_WEIGHT / "EH_left_hand_EJeff_update_2724_NONCLAIM.csv",
    "next_queue": RAB_QUEUE / "JR2724_METRIC_ONLY_SECOND_ORDER_LC_OPERATOR_NEXT.csv",
}


def ts() -> str:
    return datetime.now(timezone.utc).isoformat()


def normalize(value: Any) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    if value is None:
        return ""
    return str(value)


def md_escape(value: Any) -> str:
    return normalize(value).replace("|", "\\|").replace("\n", "<br>")


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"Refusing to write empty CSV: {path}")
    fieldnames = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="raise")
        writer.writeheader()
        for row in rows:
            writer.writerow({key: normalize(row.get(key, "")) for key in fieldnames})


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    body = [
        "| " + " | ".join(md_escape(row.get(column, "")) for column in columns) + " |"
        for row in rows
    ]
    return "\n".join([header, sep, *body])


SOURCE_SPECS = [
    {
        "source_id": "SRC2724_0_2723",
        "label": "2723 direct handoff",
        "path": ROOT / "2723-Y5-R2FR-kappa0-Gref-parent-ownership-or-Newton-coefficient-row-under-AX1090-closure.md",
        "needles": [
            "KAP2723_5_verdict",
            "FKG2723_0_E_kappa_source",
            "NEXT2723_0_selected",
            "VAL2723_OVERALL",
        ],
        "use": "selects EH-left-hand weak-field operator as next gate after kappa0/G_ref remains unsigned",
    },
    {
        "source_id": "SRC2724_1_1339",
        "label": "1339 EH-left-hand gate",
        "path": ROOT / "1339-Y5-R10-RAB-source-closure-to-EH-left-hand-local-GR-reduction-gate.md",
        "needles": [
            "EHGate1339_1_metric_only_local_4D",
            "EHGate1339_2_second_order",
            "EHGate1339_3_Levi_Civita",
            "EHGate1339_4_extra_sector_silence",
            "NEW1339_0_EH_operator",
            "VAL1339_5_Newton_blocked",
        ],
        "use": "declares metric-only, second-order, Levi-Civita and extra-sector silence as required EH-left-hand gates",
    },
    {
        "source_id": "SRC2724_2_2722",
        "label": "2722 conditional Poisson algebra",
        "path": ROOT / "2722-Y5-R2FR-Poisson-Gauss-Newton-coefficient-bridge-or-Enorm-bound-under-AX1090-closure.md",
        "needles": [
            "THM2722_0_statement",
            "THM2722_1_linearized_00",
            "FPG2722_1_E_Poisson_residual",
            "FPG2722_5_E_gauge_domain",
            "BLK2722_1_EH_left",
            "VAL2722_OVERALL",
        ],
        "use": "supplies the conditional linearized G_00 algebra and existing Poisson/gauge residual rows",
    },
    {
        "source_id": "SRC2724_3_2469",
        "label": "2469 local metric equation gate",
        "path": ROOT / "2469-Y5-R2FR-GK-stress-silence-and-local-metric-equation-gate.md",
        "needles": [
            "MET2469_0_parent_metric_equation",
            "MET2469_1_stationary_exterior",
            "MET2469_3_current_corpus",
            "PPN2469_0_residual_source",
            "PPN2469_2_hair_bound",
            "VAL2469_OVERALL",
        ],
        "use": "shows extra-sector stress remains a local metric-equation residual unless no-hair/stress silence closes",
    },
    {
        "source_id": "SRC2724_4_2208",
        "label": "2208 PPN inverse-divergence obstruction",
        "path": ROOT / "2208-Y5-R2FR-PPN-Green-operator-source-normalization-or-R10-range-kernel.md",
        "needles": [
            "PPNL2208_0_operator_factorization",
            "PPNL2208_3_source_normalization",
            "PPNB2208_0_inverse_divergence",
            "VAL2208_OVERALL",
        ],
        "use": "keeps PPN/local metric response blocked until stress reconstruction, gauge, support and boundary rules are signed",
    },
    {
        "source_id": "SRC2724_5_2470",
        "label": "2470 no-hair or stress-bound route",
        "path": ROOT / "2470-Y5-R2FR-GK-vacuum-no-hair-positivity-or-stress-bound.md",
        "needles": [
            "BND2470_2_metric_bound",
            "MET2470_0_if_nohair",
            "MET2470_2_bound_route",
            "VAL2470_OVERALL",
        ],
        "use": "frames local-GR as either no-hair stress silence or finite stress-bound problem",
    },
    {
        "source_id": "SRC2724_6_2478",
        "label": "2478 Green/domain bound certificate",
        "path": ROOT / "2478-Y5-R2FR-residual-source-norm-and-Green-bound-certificate.md",
        "needles": [
            "CMET2478_0_formal_metric_bound",
            "BLK2478_2_domain_geometry",
            "BLK2478_4_Cobs_Karena",
            "VAL2478_OVERALL",
        ],
        "use": "confirms domain geometry, Green coefficient and observable projection are not optional details",
    },
    {
        "source_id": "SRC2724_7_2464",
        "label": "2464 parent action skeleton",
        "path": ROOT / "2464-Y5-R2FR-minimal-parent-action-skeleton-for-q_loc-and-source-bridge.md",
        "needles": [
            "VAR2464_3_delta_metric",
            "GATE2464_4_local_GR_Newton_PPN",
            "VAL2464_OVERALL",
        ],
        "use": "confirms the minimal skeleton exposes metric variation but does not yet close local GR/Newton/PPN",
    },
    {
        "source_id": "SRC2724_8_2465",
        "label": "2465 metric stress exposure",
        "path": ROOT / "2465-Y5-R2FR-vertical-generator-current-law-variation-and-source-audit.md",
        "needles": [
            "STR2465_0_metric_variation_exists",
            "STR2465_4_GR_limit_gate",
            "VAL2465_OVERALL",
        ],
        "use": "prevents treating q_loc Euler silence as enough for local GR; metric stress must also close",
    },
]


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for spec in SOURCE_SPECS:
        path = Path(spec["path"])
        text = read_text(path)
        missing = [needle for needle in spec["needles"] if needle not in text]
        rows.append(
            {
                "source_id": spec["source_id"],
                "label": spec["label"],
                "path": str(path),
                "exists": path.exists(),
                "required_needles_found": not missing,
                "missing_needles": ";".join(missing),
                "use": spec["use"],
                "claim_credit": False,
                "timestamp_utc": ts(),
            }
        )
    return rows


def operator_audit_rows() -> list[dict[str, Any]]:
    return [
        {
            "audit_id": "LHS2724_0_metric_only_local_4D",
            "operator_clause": "observed local exterior action is metric-only, local, 4D and diffeo invariant",
            "attempt": "apply Lovelock/EH selection to the observed metric sector",
            "status": "UNSIGNED",
            "reason": "1339 already marks metric-only local 4D as not parent-derived; MTS sectors can still enter the left-hand operator",
            "residual_row": "E_operator_metric_only",
            "claim_allowed": False,
        },
        {
            "audit_id": "LHS2724_1_second_order",
            "operator_clause": "metric field equations are second order through tested local scales",
            "attempt": "exclude f(R), R^2, Ricci^2, Weyl^2 and nonlocal higher-derivative pieces",
            "status": "CENTRAL_BLOCKER_UNSIGNED",
            "reason": "no parent theorem yet removes higher-derivative curvature or nonlocal operator pieces from the local weak-field LHS",
            "residual_row": "E_second_order_HD",
            "claim_allowed": False,
        },
        {
            "audit_id": "LHS2724_2_Levi_Civita",
            "operator_clause": "observed connection is Levi-Civita of g_obs",
            "attempt": "set torsion and nonmetricity to zero in the measured frame",
            "status": "UNSIGNED",
            "reason": "1339 keeps Levi-Civita status not parent-derived; independent connection/torsion/nonmetricity would change the weak-field operator",
            "residual_row": "E_connection_LC",
            "claim_allowed": False,
        },
        {
            "audit_id": "LHS2724_3_extra_sector_silence",
            "operator_clause": "motion/time/domain/memory/projector/boundary sectors do not contribute independent LHS or stress",
            "attempt": "use q_loc or stationary exterior silence to remove hidden stress",
            "status": "ACTIVE_PRIMARY_OBSTRUCTION",
            "reason": "2469/2465 show metric stress exposure survives unless no-hair, positivity, topological silence, or finite stress bounds are proved",
            "residual_row": "E_extra_sector_LHS",
            "claim_allowed": False,
        },
        {
            "audit_id": "LHS2724_4_gauge_domain",
            "operator_clause": "weak-field gauge, boundary, falloff and inverse-divergence conventions are fixed",
            "attempt": "use G_00^lin approximately 2*nabla^2 Phi/c^2 in the same collar/domain",
            "status": "PARTLY_ALGEBRAIC_NOT_PARENT_SIGNED",
            "reason": "2722 gives the algebra only after gauge/domain assumptions; 2208/2478 keep I_div, support and Green/domain coefficients open",
            "residual_row": "E_linearization_gauge + E_domain_boundary + E_inverse_divergence",
            "claim_allowed": False,
        },
        {
            "audit_id": "LHS2724_5_verdict",
            "operator_clause": "actual MTS local weak-field left-hand side equals the EH G_00 Poisson operator",
            "attempt": "combine 1339 Lovelock/EH route with 2722 Poisson algebra and 2469 stress silence",
            "status": "EH_LEFT_HAND_OPERATOR_NOT_PROVED",
            "reason": "the conditional theorem is clean, but the parent has not signed metric-only, second-order, Levi-Civita, extra-sector silence, gauge/domain, or inverse-divergence clauses",
            "residual_row": "E_Poisson_residual remains explicit",
            "claim_allowed": False,
        },
    ]


def theorem_attempt_rows() -> list[dict[str, Any]]:
    return [
        {
            "theorem_id": "THM2724_0_statement",
            "statement": "If the observed local exterior parent action descends to a metric-only local 4D diffeo-invariant second-order Levi-Civita action, all extra MTS sectors are silent or bounded, and the weak-field gauge/domain is fixed by g_00=-(1+2Phi/c^2), then the leading 00 equation has G_00^lin = 2*nabla^2 Phi/c^2 plus declared residuals.",
            "status": "CONDITIONAL_THEOREM_ONLY",
            "missing_clause": "metric-only; second-order; Levi-Civita; extra-sector silence; gauge/domain/falloff; inverse-divergence/source support",
            "claim_allowed": False,
        },
        {
            "theorem_id": "THM2724_1_linearized_EH_00",
            "statement": "Under the EH/LC weak-field convention already used in 2722, G_00^lin approximately 2*nabla^2 Phi/c^2, so the Poisson equation follows after the same-frame Hilbert source and kappa0/G_ref convention are supplied.",
            "status": "ALGEBRA_DERIVED_CONDITIONAL",
            "missing_clause": "EH-left-hand ownership and source/coupling ownership",
            "claim_allowed": False,
        },
        {
            "theorem_id": "THM2724_2_residual_decomposition",
            "statement": "E_Poisson_residual is decomposed into metric-only, higher-derivative, connection, gauge, domain/boundary, extra-sector LHS/stress and inverse-divergence pieces.",
            "status": "RESIDUAL_VECTOR_DERIVED",
            "missing_clause": "numeric/source-backed bounds for each component",
            "claim_allowed": False,
        },
        {
            "theorem_id": "THM2724_3_failure_mode",
            "statement": "If any one of the operator clauses is unsigned, local Newton/GR/PPN cannot be promoted from conditional algebra to an MTS claim.",
            "status": "CLAIM_REJECTION_DERIVED",
            "missing_clause": "at least one parent-signed route or finite arena bound",
            "claim_allowed": False,
        },
    ]


def finite_rows() -> list[dict[str, Any]]:
    return [
        {
            "row_id": "FOP2724_0_E_operator_metric_only",
            "quantity": "E_operator_metric_only",
            "definition": "E_operator_metric_only := norm(non-metric, nonlocal, or extra-field contribution to the local weak-field LHS)/norm(EH Poisson LHS)",
            "feeds": "E_Poisson_residual; local_GR; PPN; R10",
            "source_path": str(ROOT / "1339-Y5-R10-RAB-source-closure-to-EH-left-hand-local-GR-reduction-gate.md"),
            "units_need": "dimensionless operator residual in declared weak-field norm",
            "missing": "parent proof that local exterior action is metric-only/local/4D before weak-field limit",
            "status": "SOURCE_READY_SCHEMA_NONCLAIM",
            "valid_for_claim": False,
        },
        {
            "row_id": "FOP2724_1_E_second_order_HD",
            "quantity": "E_second_order_HD",
            "definition": "E_second_order_HD := norm(higher-derivative or nonlocal curvature contribution to 00 weak-field LHS)/norm(2*nabla^2 Phi/c^2)",
            "feeds": "E_Poisson_residual; PPN residual vector",
            "source_path": str(ROOT / "1339-Y5-R10-RAB-source-closure-to-EH-left-hand-local-GR-reduction-gate.md"),
            "units_need": "dimensionless after choosing local collar scale and derivative norm",
            "missing": "parent exclusion or sourced bound for R^2/f(R)/Ricci^2/Weyl^2/nonlocal terms",
            "status": "SOURCE_READY_SCHEMA_NONCLAIM",
            "valid_for_claim": False,
        },
        {
            "row_id": "FOP2724_2_E_connection_LC",
            "quantity": "E_connection_LC",
            "definition": "E_connection_LC := norm(torsion/nonmetricity/independent-connection correction to G_00^lin)/norm(EH Poisson LHS)",
            "feeds": "E_Poisson_residual; clocks; light; spin; PPN",
            "source_path": str(ROOT / "1339-Y5-R10-RAB-source-closure-to-EH-left-hand-local-GR-reduction-gate.md"),
            "units_need": "dimensionless connection-induced weak-field residual",
            "missing": "parent-signed observed connection equals Levi-Civita(g_obs), or finite torsion/nonmetricity bound",
            "status": "SOURCE_READY_SCHEMA_NONCLAIM",
            "valid_for_claim": False,
        },
        {
            "row_id": "FOP2724_3_E_linearization_gauge",
            "quantity": "E_linearization_gauge",
            "definition": "E_linearization_gauge := norm(G_00^lin - 2*nabla^2 Phi/c^2 in the selected weak-field gauge)/norm(2*nabla^2 Phi/c^2)",
            "feeds": "E_Poisson_residual; E_gauge_domain",
            "source_path": str(ROOT / "2722-Y5-R2FR-Poisson-Gauss-Newton-coefficient-bridge-or-Enorm-bound-under-AX1090-closure.md"),
            "units_need": "dimensionless weak-field gauge residual",
            "missing": "explicit gauge convention, perturbation order, Phi definition, and same-frame source collar",
            "status": "SOURCE_READY_SCHEMA_NONCLAIM",
            "valid_for_claim": False,
        },
        {
            "row_id": "FOP2724_4_E_domain_boundary",
            "quantity": "E_domain_boundary",
            "definition": "E_domain_boundary := C_domain*norm(boundary, falloff, harmonic-mode and Green-domain correction to weak-field operator)",
            "feeds": "E_Poisson_residual; arena kernels; R10/PPN/orbit/clocks",
            "source_path": str(ROOT / "2478-Y5-R2FR-residual-source-norm-and-Green-bound-certificate.md"),
            "units_need": "dimensionless after Green/domain norm and observable projection are declared",
            "missing": "local collar geometry, boundary condition, harmonic zero-mode rule, C_Green and C_obs",
            "status": "SOURCE_READY_SCHEMA_NONCLAIM",
            "valid_for_claim": False,
        },
        {
            "row_id": "FOP2724_5_E_extra_sector_LHS",
            "quantity": "E_extra_sector_LHS",
            "definition": "E_extra_sector_LHS := norm(T_GK + T_tau/P + boundary + projector metric response entering local 00 equation)/norm(EH source term)",
            "feeds": "E_Poisson_residual; local_GR; stress-bound route",
            "source_path": str(ROOT / "2469-Y5-R2FR-GK-stress-silence-and-local-metric-equation-gate.md"),
            "units_need": "dimensionless stress/operator residual in same Hilbert source normalization",
            "missing": "no-hair/positivity/topological silence, or finite sourced stress norm",
            "status": "SOURCE_READY_SCHEMA_NONCLAIM",
            "valid_for_claim": False,
        },
        {
            "row_id": "FOP2724_6_E_inverse_divergence",
            "quantity": "E_inverse_divergence",
            "definition": "E_inverse_divergence := ambiguity norm from reconstructing a residual stress/potential from q_loc or divergence data without a parent I_div^{-1} rule",
            "feeds": "PPN response; local metric response; E_Poisson_residual",
            "source_path": str(ROOT / "2208-Y5-R2FR-PPN-Green-operator-source-normalization-or-R10-range-kernel.md"),
            "units_need": "dimensionless after support/gauge/boundary/source normalization are fixed",
            "missing": "parent stress reconstruction or declared no-hidden-boundary inverse-divergence convention",
            "status": "SOURCE_READY_SCHEMA_NONCLAIM",
            "valid_for_claim": False,
        },
    ]


def ejeff_update_rows() -> list[dict[str, Any]]:
    return [
        {
            "update_id": "EJ2724_0_Poisson_residual_decomposition",
            "formula": "E_Poisson_residual := E_operator_metric_only + E_second_order_HD + E_connection_LC + E_linearization_gauge + E_domain_boundary + E_extra_sector_LHS + E_inverse_divergence",
            "status": "FORMAL_VECTOR_NONCLAIM",
            "claim_allowed": False,
        },
        {
            "update_id": "EJ2724_1_gauge_domain_refinement",
            "formula": "E_gauge_domain := E_linearization_gauge + E_domain_boundary + E_inverse_divergence",
            "status": "FORMAL_VECTOR_NONCLAIM",
            "claim_allowed": False,
        },
        {
            "update_id": "EJ2724_2_Newton_bridge_dependency",
            "formula": "Newton_bridge_claim requires E_Poisson_residual=0 or sourced arena bounds plus kappa0/G_ref/source ownership",
            "status": "DEPENDENCY_LEDGER_NONCLAIM",
            "claim_allowed": False,
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "GATE2724_0_EH_left_hand",
            "claim": "actual MTS weak-field LHS is EH G_00",
            "status": "BLOCKED",
            "required_before_claim": "metric-only/local/second-order/Levi-Civita/extra-sector-silence/gauge-domain clauses parent-signed",
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE2724_1_Poisson_zero",
            "claim": "E_Poisson_residual=0",
            "status": "BLOCKED",
            "required_before_claim": "all seven finite operator rows vanish or are bounded below observational thresholds",
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE2724_2_Newton_GR",
            "claim": "MTS derives local Newton/GR limit",
            "status": "BLOCKED",
            "required_before_claim": "EH-left-hand plus kappa0/G_ref, Hilbert source, no extra stress, readout and domain gates",
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE2724_3_PPN_R10_clocks_orbits",
            "claim": "local arena pass or robustness score",
            "status": "BLOCKED",
            "required_before_claim": "arena kernels, source normalization, residual stress reconstruction, and real bound rows",
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE2724_4_public",
            "claim": "public/local-GR claim",
            "status": "FORBIDDEN_FROM_THIS_CHECKPOINT",
            "required_before_claim": "private derivation and validation chain closes first",
            "claim_allowed": False,
        },
    ]


def blocker_stack_rows() -> list[dict[str, Any]]:
    return [
        {
            "blocker_id": "BLK2724_0_metric_only",
            "missing_item": "parent-sign observed local exterior action as metric-only/local/4D",
            "effect": "Lovelock/EH selection cannot be used as an MTS theorem",
            "best_next_attack": "prove descent removes all nonmetric/local extra fields from local exterior LHS or install E_operator_metric_only bound",
            "claim_blocked": True,
        },
        {
            "blocker_id": "BLK2724_1_second_order",
            "missing_item": "parent exclusion of higher-derivative/nonlocal weak-field terms",
            "effect": "Poisson operator may be modified even if a metric equation exists",
            "best_next_attack": "try metric-only second-order Levi-Civita operator gate next",
            "claim_blocked": True,
        },
        {
            "blocker_id": "BLK2724_2_Levi_Civita",
            "missing_item": "observed connection equals Levi-Civita(g_obs)",
            "effect": "torsion/nonmetricity can alter clocks/light/PPN and the weak-field operator",
            "best_next_attack": "derive connection descent or finite connection residual",
            "claim_blocked": True,
        },
        {
            "blocker_id": "BLK2724_3_extra_sector_stress",
            "missing_item": "T_GK, tau/projector and boundary stress silence or bound",
            "effect": "local exterior can differ from GR even when q_loc is quiet",
            "best_next_attack": "reuse no-hair/stress-bound route if operator route fails",
            "claim_blocked": True,
        },
        {
            "blocker_id": "BLK2724_4_gauge_domain",
            "missing_item": "weak-field gauge, falloff, domain and Green coefficient package",
            "effect": "G_00^lin-to-Poisson translation is not an arena-ready observable",
            "best_next_attack": "write local collar gauge/domain certificate after operator clauses",
            "claim_blocked": True,
        },
        {
            "blocker_id": "BLK2724_5_inverse_divergence",
            "missing_item": "parent I_div^{-1} stress reconstruction rule",
            "effect": "q_loc or divergence data do not uniquely determine the metric residual",
            "best_next_attack": "derive T_res from parent variation or declare no-hidden-boundary reconstruction",
            "claim_blocked": True,
        },
    ]


def decision_ledger_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC2724_0_no_EH_promotion",
            "decision": "Do not promote EH-left-hand as proved.",
            "rationale": "The algebra is clean only under clauses the parent has not signed.",
            "allowed": True,
            "claim_credit": False,
        },
        {
            "decision_id": "DEC2724_1_make_residual_visible",
            "decision": "Replace a single vague Poisson blocker with seven explicit residual rows.",
            "rationale": "This makes the next derivation path auditable instead of circular.",
            "allowed": True,
            "claim_credit": False,
        },
        {
            "decision_id": "DEC2724_2_select_2725",
            "decision": "Attack metric-only/second-order/Levi-Civita operator gate next.",
            "rationale": "Those are upstream of Newton/PPN and are the least arbitrary way to make the GR reduction real.",
            "allowed": True,
            "claim_credit": False,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT2724_0_selected",
            "status": "selected_primary",
            "target_doc": "2725-Y5-R2FR-metric-only-second-order-Levi-Civita-operator-gate-or-Eoperator-bound-under-AX1090-closure.md",
            "target_script": "scripts/Y5_R2FR_metric_only_second_order_Levi_Civita_operator_gate_or_Eoperator_bound_under_AX1090_closure_2725.py",
            "mission": "try to parent-sign the metric-only, second-order and Levi-Civita clauses that allow EH-left-hand selection, or keep E_operator/E_HD/E_connection residuals explicit",
            "acceptance": "either a parent-derived local EH operator contract, or a nonclaim operator-residual ledger with no hidden GR assumption",
            "forbidden": "use observed Newton/PPN success to infer the operator; hide extra sectors; edit formalization-workbench; GitHub action",
            "selected": True,
            "claim_allowed": False,
        }
    ]


def project_snapshot_rows() -> list[dict[str, Any]]:
    return [
        {
            "snapshot_id": "SNAP2724_0_GR_reduction",
            "sector": "local GR/Newton reduction",
            "state": "conditional algebra clean, parent operator unsigned",
            "confidence": "medium on route; no claim",
            "next_need": "metric-only/second-order/LC operator gate",
        },
        {
            "snapshot_id": "SNAP2724_1_coupling",
            "sector": "kappa0/G_ref",
            "state": "target coefficient relation exists but not parent-owned",
            "confidence": "medium on formula, low on ownership",
            "next_need": "operator and source/coupling certificates",
        },
        {
            "snapshot_id": "SNAP2724_2_local_tests",
            "sector": "R10/PPN/clocks/orbits",
            "state": "blocked from scoring by residual/source/domain rows",
            "confidence": "high that current nonclaim status is correct",
            "next_need": "arena kernels after operator/source closures",
        },
        {
            "snapshot_id": "SNAP2724_3_method",
            "sector": "private derivation discipline",
            "state": "no closure smuggling; residuals explicit",
            "confidence": "high",
            "next_need": "continue derivation-first, bound-second",
        },
    ]


def branch_copy_rows() -> list[dict[str, Any]]:
    return [
        {
            "copy_id": "COPY2724_0_local_bounds",
            "source_table": str(OUTPUTS["finite_rows"]),
            "copy_path": str(BRANCH_OUTPUTS["local_bounds"]),
            "purpose": "local bound/R10/PPN branches can ingest the explicit EH-left-hand Poisson residual rows without claim credit",
            "exists": BRANCH_OUTPUTS["local_bounds"].exists(),
            "valid_for_claim": False,
        },
        {
            "copy_id": "COPY2724_1_source_weight",
            "source_table": str(OUTPUTS["ejeff_update"]),
            "copy_path": str(BRANCH_OUTPUTS["source_weight"]),
            "purpose": "source-weight branch gets the E_Poisson_residual decomposition and E_gauge_domain refinement",
            "exists": BRANCH_OUTPUTS["source_weight"].exists(),
            "valid_for_claim": False,
        },
        {
            "copy_id": "COPY2724_2_next_queue",
            "source_table": str(OUTPUTS["next_target"]),
            "copy_path": str(BRANCH_OUTPUTS["next_queue"]),
            "purpose": "queues the 2725 operator-clause gate",
            "exists": BRANCH_OUTPUTS["next_queue"].exists(),
            "valid_for_claim": False,
        },
    ]


def parse_csv(path: Path) -> tuple[bool, int, str]:
    try:
        with path.open("r", newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
        if not rows:
            return False, 0, "empty"
        return True, len(rows), "ok"
    except Exception as exc:
        return False, 0, repr(exc)


def recent_formalization_changes() -> int:
    if not FORMALIZATION.exists():
        return 0
    count = 0
    start = SCRIPT_START_UTC.timestamp()
    for path in FORMALIZATION.rglob("*"):
        if path.is_file() and path.stat().st_mtime >= start:
            count += 1
    return count


def validation_rows(
    source_rows: list[dict[str, Any]],
    audit_rows: list[dict[str, Any]],
    theorem_rows: list[dict[str, Any]],
    finite: list[dict[str, Any]],
    ejeff: list[dict[str, Any]],
    gates: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    required_quantities = {
        "E_operator_metric_only",
        "E_second_order_HD",
        "E_connection_LC",
        "E_linearization_gauge",
        "E_domain_boundary",
        "E_extra_sector_LHS",
        "E_inverse_divergence",
    }
    csv_paths = [path for key, path in OUTPUTS.items() if key != "validation"] + list(BRANCH_OUTPUTS.values())
    parse_results = [(*parse_csv(path), path) for path in csv_paths]
    parse_detail = "; ".join(
        f"{path.name}:{row_count}:{detail}" if passed else f"{path.name}:{detail}"
        for passed, row_count, detail, path in parse_results
    )
    branch_paths_ok = all(path.exists() for path in BRANCH_OUTPUTS.values())
    formalization_recent_changed_count = recent_formalization_changes()
    source_ok = all(row["exists"] is True and row["required_needles_found"] is True for row in source_rows)
    audit_nonclaim = all(row["claim_allowed"] is False for row in audit_rows)
    theorem_nonclaim = all(row["claim_allowed"] is False for row in theorem_rows)
    finite_nonclaim = (
        {row["quantity"] for row in finite} == required_quantities
        and all(row["valid_for_claim"] is False for row in finite)
    )
    ejeff_nonclaim = all(row["claim_allowed"] is False for row in ejeff)
    gates_false = all(row["claim_allowed"] is False for row in gates)
    no_github_outputs = all("github" not in str(path).lower() for path in csv_paths + [DOC])
    rows = [
        {
            "validation_id": "VAL2724_0_sources",
            "passed": source_ok,
            "detail": "all source paths exist and required needles found",
            "timestamp_utc": ts(),
        },
        {
            "validation_id": "VAL2724_1_doc_written",
            "passed": DOC.exists(),
            "detail": str(DOC),
            "timestamp_utc": ts(),
        },
        {
            "validation_id": "VAL2724_2_csv_parse",
            "passed": all(result[0] for result in parse_results),
            "detail": parse_detail,
            "timestamp_utc": ts(),
        },
        {
            "validation_id": "VAL2724_3_audit_nonclaim",
            "passed": audit_nonclaim,
            "detail": "EH-left-hand audit keeps every operator clause nonclaim",
            "timestamp_utc": ts(),
        },
        {
            "validation_id": "VAL2724_4_theorem_nonclaim",
            "passed": theorem_nonclaim,
            "detail": "operator theorem remains conditional and does not promote local GR/Newton",
            "timestamp_utc": ts(),
        },
        {
            "validation_id": "VAL2724_5_finite_rows_complete_nonclaim",
            "passed": finite_nonclaim,
            "detail": "finite rows include metric-only, higher-derivative, connection, gauge, domain, extra-sector and inverse-divergence components",
            "timestamp_utc": ts(),
        },
        {
            "validation_id": "VAL2724_6_ejeff_update_nonclaim",
            "passed": ejeff_nonclaim,
            "detail": "E_Poisson_residual and E_gauge_domain decompositions remain formal/nonclaim",
            "timestamp_utc": ts(),
        },
        {
            "validation_id": "VAL2724_7_claim_gates_all_false",
            "passed": gates_false,
            "detail": "no EH, Poisson, Newton, PPN, R10, local-GR or public claim gate opened",
            "timestamp_utc": ts(),
        },
        {
            "validation_id": "VAL2724_8_branch_copies",
            "passed": branch_paths_ok,
            "detail": "branch copies exist and remain nonclaim",
            "timestamp_utc": ts(),
        },
        {
            "validation_id": "VAL2724_9_no_formalization_recent_changes",
            "passed": formalization_recent_changed_count == 0,
            "detail": f"formalization_recent_changed_count={formalization_recent_changed_count}",
            "timestamp_utc": ts(),
        },
        {
            "validation_id": "VAL2724_10_no_github_outputs",
            "passed": no_github_outputs,
            "detail": "no GitHub/public-output path was written",
            "timestamp_utc": ts(),
        },
    ]
    overall = all(row["passed"] is True for row in rows)
    rows.append(
        {
            "validation_id": "VAL2724_OVERALL",
            "passed": overall,
            "detail": "2724 keeps EH-left-hand weak-field Poisson operator conditional, decomposes E_Poisson_residual, and selects metric-only/second-order/LC operator gate next",
            "timestamp_utc": ts(),
        }
    )
    return rows


def write_doc(rows: dict[str, list[dict[str, Any]]]) -> None:
    doc = f"""# 2724 - Y5/R2FR EH Left-Hand Weak-Field Operator Gauge Domain Or Poisson Residual Row Under AX1090 Closure

## Private Verdict

2724 tried the honest route: prove that the actual MTS local weak-field left-hand side is the Einstein-Hilbert `G_00` operator whose leading limit is `2*nabla^2 Phi/c^2`.

The conditional theorem is clean, but the claim does **not** close. The parent has not yet signed the clauses that would let us use the EH left-hand side as an MTS theorem: metric-only local 4D descent, second-order metric equations, Levi-Civita observed connection, extra-sector stress silence, gauge/domain/falloff, and inverse-divergence/source-support convention.

So this checkpoint does not weaken the route; it sharpens it. The old broad `E_Poisson_residual` is now decomposed into seven named finite rows:

`E_operator_metric_only + E_second_order_HD + E_connection_LC + E_linearization_gauge + E_domain_boundary + E_extra_sector_LHS + E_inverse_divergence`.

## Claim Ceiling

- No EH-left-hand, Poisson-zero, Newton, local-GR, PPN, R10, clock, orbital, WEP, or public claim is opened.
- The 2722 Poisson algebra remains useful but conditional.
- `E_Poisson_residual` and `E_gauge_domain` stay explicit nonclaim rows.
- No `formalization-workbench` edits, GitHub action, or public-output path is allowed from this checkpoint.

## Source Register

{markdown_table(rows["source_register"], ["source_id", "label", "path", "exists", "required_needles_found", "missing_needles", "use", "claim_credit"])}

## EH Left-Hand Operator Audit

{markdown_table(rows["operator_audit"], ["audit_id", "operator_clause", "attempt", "status", "reason", "residual_row", "claim_allowed"])}

## Conditional Theorem Attempt

{markdown_table(rows["theorem_attempt"], ["theorem_id", "statement", "status", "missing_clause", "claim_allowed"])}

## Finite Poisson Operator Rows

{markdown_table(rows["finite_rows"], ["row_id", "quantity", "definition", "feeds", "source_path", "units_need", "missing", "status", "valid_for_claim"])}

## E_Jeff Update

{markdown_table(rows["ejeff_update"], ["update_id", "formula", "status", "claim_allowed"])}

## Claim Gates

{markdown_table(rows["claim_gates"], ["gate_id", "claim", "status", "required_before_claim", "claim_allowed"])}

## Current Blocker Stack

{markdown_table(rows["blocker_stack"], ["blocker_id", "missing_item", "effect", "best_next_attack", "claim_blocked"])}

## Decision Ledger

{markdown_table(rows["decision_ledger"], ["decision_id", "decision", "rationale", "allowed", "claim_credit"])}

## Next Target

{markdown_table(rows["next_target"], ["next_id", "status", "target_doc", "target_script", "mission", "acceptance", "forbidden", "selected", "claim_allowed"])}

## Project Status Snapshot

{markdown_table(rows["project_snapshot"], ["snapshot_id", "sector", "state", "confidence", "next_need"])}

## Branch Copies

{markdown_table(rows["branch_copies"], ["copy_id", "source_table", "copy_path", "purpose", "exists", "valid_for_claim"])}

## Validation

{markdown_table(rows["validation"], ["validation_id", "passed", "detail", "timestamp_utc"])}

## Plain-English Read

This was a good gate, even though it did not give us the trophy. The route to GR is not "just assume EH and move on"; it is now: prove metric-only + second-order + Levi-Civita + stress silence + gauge/domain. If that closes, the Newton/GR bridge becomes serious. If it does not, the theory must carry explicit local residuals and beat/bound them honestly. No smuggling, no magic rabbit, no fake victory lap.
"""
    DOC.write_text(doc, encoding="utf-8")


def main() -> None:
    source_rows = source_register_rows()
    audit = operator_audit_rows()
    theorem = theorem_attempt_rows()
    finite = finite_rows()
    ejeff = ejeff_update_rows()
    gates = claim_gate_rows()
    blockers = blocker_stack_rows()
    decisions = decision_ledger_rows()
    next_rows = next_target_rows()
    snapshot = project_snapshot_rows()

    data: dict[str, list[dict[str, Any]]] = {
        "source_register": source_rows,
        "operator_audit": audit,
        "theorem_attempt": theorem,
        "finite_rows": finite,
        "ejeff_update": ejeff,
        "claim_gates": gates,
        "blocker_stack": blockers,
        "decision_ledger": decisions,
        "next_target": next_rows,
        "project_snapshot": snapshot,
    }

    for key, table_rows in data.items():
        write_csv(OUTPUTS[key], table_rows)

    write_csv(BRANCH_OUTPUTS["local_bounds"], finite)
    write_csv(BRANCH_OUTPUTS["source_weight"], ejeff)
    write_csv(BRANCH_OUTPUTS["next_queue"], next_rows)

    copies = branch_copy_rows()
    data["branch_copies"] = copies
    write_csv(OUTPUTS["branch_copies"], copies)

    data["validation"] = [
        {
            "validation_id": "VAL2724_PRE_DOC",
            "passed": False,
            "detail": "pre-document placeholder",
            "timestamp_utc": ts(),
        }
    ]
    write_doc(data)

    validation = validation_rows(source_rows, audit, theorem, finite, ejeff, gates)
    data["validation"] = validation
    write_csv(OUTPUTS["validation"], validation)
    write_doc(data)

    if not all(row["passed"] is True for row in validation):
        failed = [row for row in validation if row["passed"] is not True]
        raise SystemExit(f"2724 validation failed: {failed}")

    print(f"wrote {DOC}")
    print(f"validation {OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
