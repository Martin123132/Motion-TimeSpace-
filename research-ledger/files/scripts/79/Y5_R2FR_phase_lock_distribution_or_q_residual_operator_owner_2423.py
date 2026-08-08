from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


BRANCH_ID = "MTS_R2FR_PHASE_LOCK_DISTRIBUTION_OR_Q_RESIDUAL_OPERATOR_OWNER_2423"
CHECKPOINT_ID = "2423"

ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = ROOT.parent
FORMALIZATION = PROJECT_ROOT / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
MICROSCOPE = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
BETA_DOCS = ROOT / "source-intake" / "beta-source" / "docs"

DOC = ROOT / "2423-Y5-R2FR-phase-lock-distribution-or-q-residual-operator-owner.md"

OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_2423_SOURCE_REGISTER.csv",
    "phase_lock": OUT / "P8_Y5_PARENT_QLOC_2423_PHASE_LOCK_OWNER_LEDGER.csv",
    "q_operator": OUT / "P8_Y5_PARENT_QLOC_2423_Q_OPERATOR_CONDITIONAL_DERIVATION.csv",
    "selector_finalizer": OUT / "P8_Y5_PARENT_QLOC_2423_SELECTOR_CLOSURE_FINALIZER.csv",
    "finite_intake": OUT / "P8_Y5_PARENT_QLOC_2423_FINITE_Q_RESIDUAL_INTAKE.csv",
    "parallel_source": OUT / "P8_Y5_PARENT_QLOC_2423_PARALLEL_SOURCE_SIDE_LEDGER.csv",
    "claim_gates": OUT / "P8_Y5_PARENT_QLOC_2423_CLAIM_GATES.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_2423_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_2423_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_PARENT_QLOC_2423_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2423_VALIDATION.csv",
}

COPY_TARGETS = {
    "queue": QUEUE / "JR2423_Q_CLOSURE_FINALIZER_AND_FINITE_RESIDUAL_NONCLAIM.csv",
    "branch_wep": MICROSCOPE / "P8_Y5_PARENT_QLOC_2423_LOCAL_GR_REFUSAL_NONCLAIM.csv",
    "beta_docs": BETA_DOCS / "PARENT_QLOC_Q_CLOSURE_FINALIZER_DECISION_2423_NONCLAIM.csv",
}

SOURCES = [
    {
        "source_id": "SRC2423_00_2422_handoff",
        "source_path": ROOT / "2422-Y5-R2FR-parent-multimode-permission-or-scalar-only-no-go.md",
        "needles": ["POL2422_5_verdict", "NEXT2422_0_selected", "VAL2422_OVERALL"],
        "role": "current handoff selecting phase-lock distribution or q residual operator owner",
    },
    {
        "source_id": "SRC2423_01_2280_phase_operator",
        "source_path": ROOT / "2280-Y5-R2FR-phase-lock-distribution-or-q-residual-operator-owner.md",
        "needles": ["PLO2280_4_q_feedback_lock", "QOO2280_2_q_stiffness_sector", "VAL2280_OVERALL"],
        "role": "earlier phase-lock demotion and q-stiffness owner audit",
    },
    {
        "source_id": "SRC2423_02_2281_q_stiffness",
        "source_path": ROOT / "2281-Y5-R2FR-q-stiffness-parent-sector-or-no-go.md",
        "needles": ["QSD2281_2_transverse_q_mass", "QSD2281_4_operator", "VAL2281_OVERALL"],
        "role": "conditional covariance-Hessian derivation of q mass/stiffness operator",
    },
    {
        "source_id": "SRC2423_03_2282_selector",
        "source_path": ROOT / "2282-Y5-R2FR-covariance-equilibrium-selector-or-q-closure-declaration.md",
        "needles": ["QOE2282_1_q_zero_to_reciprocity", "QCD2282_0_status", "VAL2282_OVERALL"],
        "role": "q=0 equivalence to radial observer-cell reciprocity and closure declaration",
    },
    {
        "source_id": "SRC2423_04_2283_finalizer",
        "source_path": ROOT / "2283-Y5-R2FR-radial-observer-cell-current-owner-or-q-closure-finalizer.md",
        "needles": ["RCO2283_1_ordinary_current", "QCF2283_0_finalizer", "VAL2283_OVERALL"],
        "role": "radial current/multiplier/gauge/psi owner route exhaustion and finite residual fork",
    },
    {
        "source_id": "SRC2423_05_2371_source_feedback",
        "source_path": ROOT / "2371-Y5-R2FR-source-feedback-epsilon-sigma-or-PPN-gauge-bound-row.md",
        "needles": ["ESZA2371_5_verdict", "NSOS2371_2_source_blind_functor", "NEXT2371_0_selected"],
        "role": "parallel source/readout feedback branch retained as finite source-side residual",
    },
    {
        "source_id": "SRC2423_06_2372_source_blind",
        "source_path": ROOT / "2372-Y5-R2FR-parent-action-source-blind-functor-signature-or-source-profile-vector.md",
        "needles": ["MUC2372_6_verdict", "NSC2372_0_identity_target", "NEXT2372_0_selected"],
        "role": "minimal universal matter coupling treated as private branch, not public derivation",
    },
    {
        "source_id": "SRC2423_07_2373_noether_source_charge",
        "source_path": ROOT / "2373-Y5-R2FR-Noether-source-charge-identity-or-nonHilbert-residual-row.md",
        "needles": ["NSCI2373_7_verdict", "TRI2373_1_spin_torsion", "NEXT2373_0_selected"],
        "role": "Noether/source-charge identity gives conditional theorem but leaves non-Hilbert residuals",
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


def phase_lock_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            row_id="PLO2423_0_random_independent_phases",
            candidate="random independent nonlinear phase mixing",
            test="integrate nonlinear carrier source over independent uniform phases",
            result="REJECTED_DIRECTED_EXCHANGE_ZERO",
            reason="parity/random phase averaging cannot create the signed temporal-radial transfer required by Dq=0",
            owner_status="NOT_OWNER",
        ),
        base_row(
            row_id="PLO2423_1_even_locked_distribution",
            candidate="even locked phase distribution",
            test="P(phi) symmetric under phase reversal or exchange",
            result="REJECTED_NO_ORIENTATION",
            reason="even locks can correlate amplitudes but do not choose the one-sided exchange needed by D C_rr = D C_tt/(1-C_tt)^2",
            owner_status="NOT_OWNER",
        ),
        base_row(
            row_id="PLO2423_2_odd_lagged_lock",
            candidate="odd or lagged phase-lock distribution",
            test="P_lock has oriented phase lag producing nonzero exchange coefficient",
            result="OPEN_BUT_UNSOURCED",
            reason="would need a parent memory kernel, projectors P_T/P_R, normalization and regularization; none is signed",
            owner_status="CONTRACT_ONLY",
        ),
        base_row(
            row_id="PLO2423_3_boundary_memory_lock",
            candidate="boundary/cell-memory exchange",
            test="oriented cell current or memory transfer supplies E_T,E_R",
            result="OPEN_BUT_UNSOURCED",
            reason="requires no-flux/reciprocal-flux theorem or signed memory kernel; current corpus only identifies the gate",
            owner_status="CONTRACT_ONLY",
        ),
        base_row(
            row_id="PLO2423_4_q_feedback_lock",
            candidate="q-dependent phase distribution",
            test="choose P_lock[q] so Dq=-kappa_q q or L_q q=S_q",
            result="RECLASSIFIED_AS_Q_OPERATOR_OWNER",
            reason="once the distribution reads q and enforces tangency, the real physics is a q residual/stiffness/relaxation operator",
            owner_status="Q_OPERATOR_ROUTE",
        ),
        base_row(
            row_id="PLO2423_5_verdict",
            candidate="phase-lock route as standalone local-GR derivation",
            test="can phase locking alone parent-sign q=0?",
            result="PHASE_LOCK_DEMOTED",
            reason="free locks fail; q-feedback locks are not free phase effects but operator ownership; proceed through q operator or finite q residuals",
            owner_status="DEMOTED_TO_OPERATOR_OR_FINITE_RESIDUAL",
        ),
    ]


def q_operator_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            row_id="QOD2423_0_transverse_q_mass",
            object="q mass from covariance Hessian",
            formula="M_q^2 = n_q^A H_AB n_q^B",
            status="CONDITIONAL_DERIVATION",
            condition="requires parent-selected equilibrium manifold q=0 and positive Hessian H_AB in the transverse q-normal",
            missing_input="parent selector for q=0 / R_AB=0",
        ),
        base_row(
            row_id="QOD2423_1_gradient_stiffness",
            object="q gradient stiffness",
            formula="Z_q = xi_q^2 n_q^A H_AB n_q^B",
            status="CONDITIONAL_DERIVATION",
            condition="requires sourced smoothing/correlation length xi_q and same-frame normalization",
            missing_input="numeric or symbolic parent xi_q source",
        ),
        base_row(
            row_id="QOD2423_2_operator",
            object="q residual operator",
            formula="L_q q = -nabla_i(Z_q nabla^i q)+M_q^2 q",
            status="CONDITIONAL_OPERATOR_FORM",
            condition="follows from quadratic q free energy once Z_q and M_q^2 are parent-signed",
            missing_input="boundary domain, source leg S_q/j_q, and observable projection P_obs",
        ),
        base_row(
            row_id="QOD2423_3_onsager",
            object="relaxation variant",
            formula="Dq = -mu_q delta F_q/delta q + source, mu_q >= 0",
            status="VIABLE_IF_DISSIPATION_PRINCIPLE_EXISTS",
            condition="requires parent entropy/Onsager mobility owner",
            missing_input="mu_q and entropy-production functional",
        ),
        base_row(
            row_id="QOD2423_4_no_smuggling_rule",
            object="operator admissibility",
            formula="do not add V(q)=1/2 M_q^2 q^2 as a proof of q=0",
            status="NO_SMUGGLING_GATE",
            condition="operator can bound residuals, not derive the target manifold unless parent selector exists",
            missing_input="non-circular selector theorem",
        ),
    ]


def selector_finalizer_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            row_id="SCF2423_0_exact_equivalence",
            target="q=0 / R_AB=0 / J_q=1",
            result="EXACT_EQUIVALENCE_NOT_PARENT_SELECTION",
            evidence="q=0 iff C_R=C_T/(1-C_T) iff T^2 S=1 iff R_AB=0 iff J_q=T sqrt(S)=1",
            decision="identity is retained as the clean local-GR branch coordinate, not a derivation",
        ),
        base_row(
            row_id="SCF2423_1_current_route",
            target="ordinary conserved radial cell current",
            result="REJECTED_NO_CHARGE_OBSTRUCTION",
            evidence="partial_r(W partial_r R_AB)=0 gives Q_R constant, not Q_R=0",
            decision="cannot kill exterior R_AB hair without a no-charge theorem",
        ),
        base_row(
            row_id="SCF2423_2_multiplier_route",
            target="post-hoc lambda_R R_AB constraint",
            result="REJECTED_BACKREACTION",
            evidence="adding a physical multiplier after variables are visible changes field equations unless first-class/reduced-configuration gates close",
            decision="not standalone derivation",
        ),
        base_row(
            row_id="SCF2423_3_gauge_route",
            target="observer-splitting gauge quotient",
            result="FIRST_CLASS_CONTRACT_ONLY",
            evidence="needs generator, boundary charge, bracket closure, degree count and matter descent",
            decision="possible future theorem, not current proof",
        ),
        base_row(
            row_id="SCF2423_4_psi_route",
            target="psi quotient removes or verticalizes q",
            result="NOT_CLOSED",
            evidence="psi covariance map exists as route seed but does not yet sign temporal/radial relation or q source/stiffness",
            decision="root route remains open but unavailable for claim",
        ),
        base_row(
            row_id="SCF2423_5_finalizer",
            target="local-GR/Newton route through q=0",
            result="CLOSURE_ONLY_UNTIL_FIRST_CLASS_OR_PSI_QUOTIENT_THEOREM",
            evidence="all current owner routes are rejected, contract-only, or conditional seeds",
            decision="use R_AB=0/q=0 only as explicit benchmark closure; finite q residual branch becomes executable next",
        ),
    ]


def finite_intake_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            input_id="FQI2423_0_Mq2",
            input_name="M_q^2 or M_R^2",
            required_meaning="positive transverse q/R_AB stiffness from parent Hessian in the same q normalization",
            current_status="MISSING_PARENT_STIFFNESS_COEFFICIENT",
            next_use="finite residual amplitude q ~ j_q/M_q^2",
        ),
        base_row(
            input_id="FQI2423_1_jq",
            input_name="j_q or j_R",
            required_meaning="source/readout leg that drives q when q is physical rather than killed",
            current_status="MISSING_PARENT_SOURCE_COEFFICIENT",
            next_use="numerator of local q residual vector",
        ),
        base_row(
            input_id="FQI2423_2_gradient_guard",
            input_name="no-gradient/no-hair guard",
            required_meaning="boundary/domain theorem preventing long-range R_AB hair or fixing Green-kernel boundary constants",
            current_status="MISSING_BOUNDARY_DOMAIN_THEOREM",
            next_use="decide whether finite q residual is Yukawa/local or long-range PPN-active",
        ),
        base_row(
            input_id="FQI2423_3_Pobs",
            input_name="P_obs projection matrix",
            required_meaning="same-frame map from q/R_AB residual to PPN, R10, clock and orbital observables",
            current_status="MISSING_ARENA_PROJECTION",
            next_use="screen sourced residuals against local tests without importing targets as predictions",
        ),
        base_row(
            input_id="FQI2423_4_Newton_source_norm",
            input_name="Newton/source normalization",
            required_meaning="GM/Hilbert source normalization tying parent source channel to measured Newtonian mass",
            current_status="MISSING_SOURCE_NORMALIZATION",
            next_use="avoid fake agreement caused by arbitrary source scaling",
        ),
        base_row(
            input_id="FQI2423_5_comparator_bounds",
            input_name="local comparator bounds",
            required_meaning="R10/PPN/clocks/orbital limits used only after MTS predicts a sourced residual",
            current_status="COMPARATOR_ONLY",
            next_use="cannot define theory coefficients or certify local-GR pass",
        ),
    ]


def parallel_source_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            row_id="PSS2423_0_epsilon_sigma",
            branch="source-feedback/readout leakage",
            inherited_result="NOT_DERIVED_RETAIN_LEAKAGE_ROW",
            effect_on_q_route="source-side leakage can feed j_q or P_obs; keep as finite residual input, not q=0 proof",
            next_status="parallel branch held",
        ),
        base_row(
            row_id="PSS2423_1_source_blind_functor",
            branch="minimal universal matter coupling",
            inherited_result="PRIVATE_BRANCH_READY_NOT_DERIVED",
            effect_on_q_route="useful bookkeeping restriction but cannot publicly kill source-only species slots",
            next_status="requires NoSourceOnlySpeciesSlot theorem",
        ),
        base_row(
            row_id="PSS2423_2_noether_source_charge",
            branch="Noether/Hilbert source identity",
            inherited_result="CONDITIONAL_OWNER_REAL_BUT_INCOMPLETE",
            effect_on_q_route="post-variation rescaling is killed only under minimal Hilbert matter; pre-action weights/non-Hilbert channels survive",
            next_status="no-hypermomentum/Levi-Civita source connection remains next source-side gate",
        ),
        base_row(
            row_id="PSS2423_3_public_status",
            branch="source-side local-GR claim",
            inherited_result="BLOCKED",
            effect_on_q_route="do not claim R10/WEP/PPN/local-GR pass from source-side branch",
            next_status="nonclaim",
        ),
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        base_row(gate_id="CG2423_0_phase_lock_free", gate="free phase-lock derives q=0", passed=False, reason="random/even locks fail and odd/lagged locks are unsourced"),
        base_row(gate_id="CG2423_1_q_feedback_not_magic", gate="q-dependent lock is standalone phase mechanism", passed=False, reason="q-feedback lock is reclassified as q residual/operator owner"),
        base_row(gate_id="CG2423_2_q_operator_coefficients", gate="Z_q and M_q^2 parent-signed", passed=False, reason="operator form is conditional; q=0 selector, xi_q and Hessian normalization are not parent-owned"),
        base_row(gate_id="CG2423_3_q_selector", gate="parent selects q=0/R_AB=0/J_q=1", passed=False, reason="current/multiplier/gauge/psi routes remain rejected, contract-only, or incomplete"),
        base_row(gate_id="CG2423_4_finite_residual", gate="finite q residual is locally bounded", passed=False, reason="M_q^2, j_q, no-hair guard, P_obs and Newton/source normalization remain missing"),
        base_row(gate_id="CG2423_5_local_GR_Newton", gate="local GR/Newton reduction derived", passed=False, reason="closure benchmark exists but derived branch is not parent-signed"),
        base_row(gate_id="CG2423_6_public_claim", gate="GitHub/public claim allowed", passed=False, reason="private nonclaim checkpoint"),
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        base_row(decision_id="DEC2423_0_phase_lock", decision="FREE_PHASE_LOCK_DEMOTED", rationale="standalone phase distributions do not provide the signed q-zero exchange without extra parent machinery", consequence="stop circling random phase-lock as a proof"),
        base_row(decision_id="DEC2423_1_operator", decision="Q_FEEDBACK_LOCK_EQUALS_Q_OPERATOR_OWNER", rationale="if the lock reads q and damps it, the thing to derive is L_q/kappa_q/G_q", consequence="operator route becomes the clean language"),
        base_row(decision_id="DEC2423_2_conditional_gain", decision="Q_OPERATOR_FORM_CONDITIONALLY_DERIVED", rationale="covariance Hessian gives M_q^2/Z_q once q=0 is parent-selected", consequence="use as disciplined finite-residual machinery only"),
        base_row(decision_id="DEC2423_3_selector", decision="Q_ZERO_SELECTOR_CLOSURE_ONLY", rationale="R_AB/q/J_q equivalence is exact but owner routes remain unsigned", consequence="no derived local-GR/Newton claim"),
        base_row(decision_id="DEC2423_4_next", decision="FINITE_Q_RESIDUAL_ROUTE_NEXT", rationale="if q cannot yet be killed, source and bound the residual without pretending it is zero", consequence="target 2424"),
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            route_id="NEXT2423_0_selected",
            selection_status="selected",
            target_file="2424-Y5-R2FR-finite-q-residual-coefficient-source-or-local-benchmark-runner.md",
            target_script="scripts/Y5_R2FR_finite_q_residual_coefficient_source_or_local_benchmark_runner_2424.py",
            objective="source or explicitly mark missing M_q^2, j_q, no-gradient/no-hair guard, P_obs and Newton/source normalization, then separate q=0 closure benchmark from finite q residual tests",
            success_condition="finite q residual rows are source-backed nonclaim inputs, or every missing coefficient/projection is carried into a benchmark runner with claims blocked",
            do_not_do="do not use local experimental bounds as theory coefficients or claim local-GR/Newton from an explicit closure",
        ),
        base_row(
            route_id="NEXT2423_1_parallel",
            selection_status="held_parallel",
            target_file="2424b-Y5-R2FR-noHypermomentum-LeviCivita-source-connection-or-P4-row.md",
            target_script="scripts/Y5_R2FR_noHypermomentum_LeviCivita_source_connection_or_P4_row_2424b.py",
            objective="continue source-side branch by proving no independent connection/hypermomentum source channel or retaining P4 torsion/nonmetricity residual",
            success_condition="ordinary matter/source/readout connection variation is proved silent, or a first P4 residual row remains nonclaim",
            do_not_do="do not import GR minimal coupling as a hidden axiom without labeling it private/conditional",
        ),
    ]


def copy_branch_rows(
    selector_rows: list[dict[str, Any]],
    claim_rows: list[dict[str, Any]],
    decision_ledger: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    copy_specs = [
        ("queue", OUTPUTS["selector_finalizer"], COPY_TARGETS["queue"], selector_rows),
        ("branch_wep", OUTPUTS["claim_gates"], COPY_TARGETS["branch_wep"], claim_rows),
        ("beta_docs", OUTPUTS["decision"], COPY_TARGETS["beta_docs"], decision_ledger),
    ]
    rows: list[dict[str, Any]] = []
    for copy_id, source_path, target_path, copied_rows in copy_specs:
        write_csv(target_path, copied_rows)
        rows.append(
            base_row(
                copy_id=f"BC2423_{copy_id}",
                source_path=source_path,
                target_path=target_path,
                target_exists=target_path.exists(),
                row_count=len(copied_rows),
                purpose="branch-locked nonclaim handoff",
            )
        )
    return rows


def formalization_has_2423_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    patterns = (
        "*2423-Y5-R2FR*",
        "*P8_Y5_PARENT_QLOC_2423*",
        "*P8_Y5_BRR545_2423*",
        "*Y5_R2FR_phase_lock_distribution_or_q_residual_operator_owner_2423*",
        "*JR2423*",
        "*PARENT_QLOC_Q_CLOSURE_FINALIZER_DECISION_2423*",
    )
    return any(path.is_file() for pattern in patterns for path in FORMALIZATION.rglob(pattern))


def remove_pycache() -> None:
    cache = ROOT / "scripts" / "__pycache__"
    if cache.exists():
        shutil.rmtree(cache)


def claim_flags_safe(rows_by_name: dict[str, list[dict[str, Any]]]) -> bool:
    for rows in rows_by_name.values():
        for row in rows:
            for key in ("valid_for_claim", "claim_allowed"):
                value = row.get(key)
                if value is True or stringify(value).lower() == "true":
                    return False
            if row.get("passed") is True:
                return False
    return True


def build_validation_rows(rows_by_name: dict[str, list[dict[str, Any]]], branch_copy_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    source_rows = rows_by_name["source_register"]
    phase_rows = rows_by_name["phase_lock"]
    operator_rows = rows_by_name["q_operator"]
    selector_rows = rows_by_name["selector_finalizer"]
    finite_rows = rows_by_name["finite_intake"]
    claim_rows = rows_by_name["claim_gates"]

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
        ("VAL2423_SOURCES_EXIST", all(row["path_exists"] for row in source_rows), "all cited source paths exist"),
        ("VAL2423_NEEDLES_FOUND", all(row["needles_found"] for row in source_rows), "all source needles found in current files"),
        ("VAL2423_PHASE_LOCK_DEMOTED", any(row["row_id"] == "PLO2423_5_verdict" and row["result"] == "PHASE_LOCK_DEMOTED" for row in phase_rows), "free phase-lock route explicitly demoted"),
        ("VAL2423_Q_FEEDBACK_RECLASSIFIED", any(row["row_id"] == "PLO2423_4_q_feedback_lock" and row["result"] == "RECLASSIFIED_AS_Q_OPERATOR_OWNER" for row in phase_rows), "q-dependent lock reclassified as operator ownership"),
        ("VAL2423_Q_OPERATOR_FORM", any(row["row_id"] == "QOD2423_2_operator" and "M_q^2 q" in row["formula"] for row in operator_rows), "conditional q operator formula present"),
        ("VAL2423_SELECTOR_CLOSURE", any(row["row_id"] == "SCF2423_5_finalizer" and "CLOSURE_ONLY" in row["result"] for row in selector_rows), "selector finalized as closure-only"),
        ("VAL2423_EQUIVALENCE_RETAINED", any(row["row_id"] == "SCF2423_0_exact_equivalence" and "R_AB=0" in row["evidence"] for row in selector_rows), "q/R_AB/J_q equivalence retained"),
        ("VAL2423_FINITE_INPUTS", {row["input_id"] for row in finite_rows} >= {"FQI2423_0_Mq2", "FQI2423_1_jq", "FQI2423_2_gradient_guard", "FQI2423_3_Pobs", "FQI2423_4_Newton_source_norm", "FQI2423_5_comparator_bounds"}, "finite residual intake has required input rows"),
        ("VAL2423_CLAIMS_BLOCKED", all(not row["passed"] for row in claim_rows), "all claim gates remain blocked"),
        ("VAL2423_FLAGS_SAFE", claim_flags_safe(rows_by_name), "no generated row is valid_for_claim/claim_allowed"),
        ("VAL2423_BRANCH_COPIES", all(row["target_exists"] for row in branch_copy_rows), "branch copy files written"),
        ("VAL2423_CSV_PARSE", all(item[1] and item[2] > 0 for item in csv_results), "all generated CSV and branch copies parse with rows"),
        ("VAL2423_NO_FORMALIZATION_OUTPUT", not formalization_has_2423_artifacts(), "no 2423 artifacts written into formalization-workbench"),
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
            validation_id="VAL2423_OVERALL",
            status="PASS" if overall_passed else "FAIL",
            detail="2423 demotes standalone phase-locking, keeps q-operator derivation conditional, finalizes q/R_AB selector as closure-only, and selects finite q residual source/bound runner next",
            fatal=not overall_passed,
        )
    )
    return rows


def write_document(rows_by_name: dict[str, list[dict[str, Any]]], validation_rows: list[dict[str, Any]]) -> None:
    content = f"""# 2423 Y5 R2FR Phase-Lock Distribution Or q Residual Operator Owner

## Result

The coupling hunt sharpened rather than closed: standalone phase-locking is **not** a safe parent derivation of the local-GR branch. Random/even phase distributions give no directed temporal-radial exchange, odd/lagged distributions are unsourced, and any lock that reads `q` and damps it is really a `q` residual operator in disguise.

The useful gain is narrower but cleaner: the `q` operator form is conditionally derivable from a parent covariance Hessian **if** the parent first selects the `q=0` equilibrium manifold. Because the current/multiplier/gauge/psi selector routes remain unsigned, `q=0 / R_AB=0 / J_q=1` stays an explicit closure benchmark, not a derived GR/Newton theorem. The next executable route is finite residual physics: source or mark missing `M_q^2`, `j_q`, no-hair/domain guard, `P_obs`, and Newton/source normalization.

## Practical Status

- **Derived/clean:** exact q-zero exchange target, q/R_AB/J_q equivalence, and conditional q-operator form.
- **Demoted:** free phase-locking as a standalone solution.
- **Still missing:** parent selector for `q=0`, parent-signed `Z_q/M_q^2`, source leg `j_q`, no-hair guard, observable projection, and Newton/source normalization.
- **Claim discipline:** no local-GR/Newton/PPN/R10/clock/orbital pass is allowed from this checkpoint.
- **Next move:** stop re-trying magic coupling locks; build the finite `q` residual coefficient/source runner.

## Source Register

{table(["source_id", "source_path", "path_exists", "needles_found", "role"], rows_by_name["source_register"])}

## Phase-Lock Owner Ledger

{table(["row_id", "candidate", "result", "reason", "owner_status"], rows_by_name["phase_lock"])}

## Conditional q Operator Derivation

{table(["row_id", "object", "formula", "status", "condition", "missing_input"], rows_by_name["q_operator"])}

## Selector Closure Finalizer

{table(["row_id", "target", "result", "evidence", "decision"], rows_by_name["selector_finalizer"])}

## Finite q Residual Intake

{table(["input_id", "input_name", "required_meaning", "current_status", "next_use"], rows_by_name["finite_intake"])}

## Parallel Source-Side Ledger

{table(["row_id", "branch", "inherited_result", "effect_on_q_route", "next_status"], rows_by_name["parallel_source"])}

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
        "phase_lock": phase_lock_rows(),
        "q_operator": q_operator_rows(),
        "selector_finalizer": selector_finalizer_rows(),
        "finite_intake": finite_intake_rows(),
        "parallel_source": parallel_source_rows(),
        "claim_gates": claim_gate_rows(),
        "decision": decision_rows(),
        "next_target": next_target_rows(),
    }

    for name, rows in rows_by_name.items():
        write_csv(OUTPUTS[name], rows)

    branch_copy_rows = copy_branch_rows(
        rows_by_name["selector_finalizer"],
        rows_by_name["claim_gates"],
        rows_by_name["decision"],
    )
    rows_by_name["branch_copies"] = branch_copy_rows
    write_csv(OUTPUTS["branch_copies"], branch_copy_rows)

    validation_rows = build_validation_rows(rows_by_name, branch_copy_rows)
    write_csv(OUTPUTS["validation"], validation_rows)
    write_document(rows_by_name, validation_rows)
    remove_pycache()

    overall = next(row for row in validation_rows if row["validation_id"] == "VAL2423_OVERALL")
    print(f"{DOC}")
    print(f"{OUTPUTS['validation']}")
    print(f"VAL2423_OVERALL={overall['status']}")


if __name__ == "__main__":
    main()
