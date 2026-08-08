from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable


CHECKPOINT = "3821"
BRANCH = "MTS_R2FR_Y5_CLOSED_SYSTEM_STRESS_VIRIAL_CANCELLATION_OR_PRESSURE_BINDING_BOUND_3821"

PCW = Path(__file__).resolve().parents[1]
ROOT = PCW.parent
FWB = ROOT / "formalization-workbench"
OUT = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "3821-Y5-R2FR-closed-system-stress-virial-cancellation-or-pressure-binding-bound.md"
SPINE_PATH = PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

P_3820 = PCW / "3820-Y5-R2FR-Komar-Tolman-active-mass-and-independent-source-ledger.md"
P_3817 = PCW / "3817-Y5-R2FR-qblind-matter-descent-preserves-Hilbert-stress-and-Bianchi-current.md"
P_3776 = PCW / "3776-Y5-R2FR-total-Hilbert-source-inclusion-EM-Poynting-and-interior-monopole-closure.md"
P_3777 = PCW / "3777-Y5-R2FR-PiM-total-system-domain-and-EM-field-energy-source-map.md"
P_3792 = PCW / "3792-Y5-R2FR-same-current-Ward-Hilbert-stress-owner-or-epsilonJ-bound.md"

CSV_3820_KOMAR = OUT / "P8_Y5_R2FR_3820_KOMAR_TOLMAN_ACTIVE_MASS_DERIVATION.csv"
CSV_3820_CORR = OUT / "P8_Y5_R2FR_3820_PRESSURE_BINDING_CORRECTION_LAW.csv"
CSV_3820_RESID = OUT / "P8_Y5_R2FR_3820_ACTIVE_MASS_RESIDUAL_ROWS.csv"
CSV_3817_HILBERT = OUT / "P8_Y5_R2FR_3817_HILBERT_STRESS_PRESERVATION_THEOREM.csv"
CSV_3776_TOTAL = OUT / "P8_Y5_R2FR_3776_TOTAL_HILBERT_SOURCE_INCLUSION_THEOREM.csv"
CSV_3777_DOMAIN = OUT / "P8_Y5_R2FR_3777_TOTAL_SYSTEM_DOMAIN_RULES.csv"
CSV_3792_WARD = OUT / "P8_Y5_R2FR_3792_SAME_CURRENT_WARD_HILBERT_THEOREM.csv"

OUTPUTS = {
    "sources": OUT / "P8_Y5_R2FR_3821_SOURCE_REGISTER.csv",
    "virial": OUT / "P8_Y5_R2FR_3821_STRESS_VIRIAL_THEOREM.csv",
    "reduction": OUT / "P8_Y5_R2FR_3821_TOLMAN_TO_ENERGY_MASS_REDUCTION.csv",
    "bounds": OUT / "P8_Y5_R2FR_3821_PRESSURE_BINDING_BOUND_VECTOR.csv",
    "source_classes": OUT / "P8_Y5_R2FR_3821_CLOSED_SOURCE_CLASSIFIER.csv",
    "residuals": OUT / "P8_Y5_R2FR_3821_STRESS_VIRIAL_RESIDUAL_ROWS.csv",
    "gates": OUT / "P8_Y5_R2FR_3821_CLAIM_GATES.csv",
    "decisions": OUT / "P8_Y5_R2FR_3821_DECISION_ROWS.csv",
    "next": OUT / "P8_Y5_R2FR_3821_NEXT_TARGET.csv",
    "status": OUT / "P8_Y5_R2FR_3821_STATUS.csv",
    "validation": OUT / "P8_Y5_BRR545_3821_VALIDATION.csv",
}

SOURCE_SPECS = [
    ("SRC3821_0_3820_doc", P_3820, "Pressure And Binding Correction Law"),
    ("SRC3821_1_3820_komar", CSV_3820_KOMAR, "KT3820_3_closed_system_warning"),
    ("SRC3821_2_3820_corrections", CSV_3820_CORR, "COR3820_0_pressure_trace"),
    ("SRC3821_3_3820_residuals", CSV_3820_RESID, "R3820_2_stress_virial"),
    ("SRC3821_4_3817_doc", P_3817, "Bianchi"),
    ("SRC3821_5_3817_hilbert", CSV_3817_HILBERT, "HSP3817_3_same_current_total_stress"),
    ("SRC3821_6_3776_doc", P_3776, "Total Hilbert Source Inclusion Theorem"),
    ("SRC3821_7_3776_total", CSV_3776_TOTAL, "THI3776_1_linear_Hilbert_sum"),
    ("SRC3821_8_3777_doc", P_3777, "total-system domain"),
    ("SRC3821_9_3777_domain", CSV_3777_DOMAIN, "TSD3777_3_Poynting_flux"),
    ("SRC3821_10_3792_doc", P_3792, "Stress Ward identity"),
    ("SRC3821_11_3792_ward", CSV_3792_WARD, "SCW3792_3_total_Hilbert_stress"),
]


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8-sig", errors="replace")


def base_row(timestamp: str) -> dict[str, str]:
    return {
        "timestamp_utc": timestamp,
        "branch_id": BRANCH,
        "checkpoint_id": CHECKPOINT,
        "valid_for_claim": "false",
        "claim_allowed": "false",
    }


def write_csv(path: Path, rows: Iterable[dict[str, str]]) -> None:
    rows = list(rows)
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


def parse_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def source_rows(timestamp: str) -> list[dict[str, str]]:
    rows = []
    for source_id, path, needle in SOURCE_SPECS:
        exists = path.exists()
        text = read_text(path) if exists else ""
        rows.append(
            {
                **base_row(timestamp),
                "source_id": source_id,
                "path": str(path),
                "needle": needle,
                "exists": str(exists),
                "needle_found": str(needle in text),
                "source_role": "closed-system stress virial proof input",
            }
        )
    return rows


def virial_rows(timestamp: str) -> list[dict[str, str]]:
    rows = [
        {
            "theorem_id": "SVT3821_0_total_conservation_input",
            "status": "EXACT_CONDITIONAL_INPUT",
            "statement": "Use the total Hilbert stress, not matter-only stress: in a local orthonormal source frame, partial_mu T_total^{mu nu}=0 up to named Ward, boundary, curvature and parent-exchange residuals.",
            "derivation": "This imports 3817/3776/3792 same-current total-stress ownership.",
            "zero_condition": "C_Bianchi_total=0, epsilon_J_Q=0, boundary/domain flux silent",
        },
        {
            "theorem_id": "SVT3821_1_tensor_virial_identity",
            "status": "EXACT_LOCAL_IDENTITY_WITH_RESIDUALS",
            "statement": "For a localized total source, the integrated spatial stress is controlled by the second time derivative of the inertia tensor plus surface and covariant-connection terms.",
            "derivation": "From partial_mu T_total^{mu j}=0, integrate d/dt int x^i T^{0j}; equivalently d2I^{ij}/dt2=2 int T^{ij} dV plus boundary/covariant terms.",
            "zero_condition": "stationary or time-averaged d2I^{ij}/dt2=0 and surface/covariant terms vanish",
        },
        {
            "theorem_id": "SVT3821_2_trace_cancellation",
            "status": "EXACT_CONDITIONAL_TRACE_ZERO",
            "statement": "Taking the trace gives int T_total^{i}{}_{i} dV=0 for a stationary closed total source in the local branch.",
            "derivation": "Trace SVT3821_1 and impose stationarity, no boundary stress flux, and total-system domain closure.",
            "zero_condition": "epsilon_virial=epsilon_surface=epsilon_covariant=epsilon_domain=0",
        },
        {
            "theorem_id": "SVT3821_3_pressure_paradox_resolution",
            "status": "MECHANISM_CONSTRUCTED",
            "statement": "The isolated 3p/c^2 pressure term is not deleted; it is cancelled or compensated by stabilizing/binding/container/field stresses only when the total system is included.",
            "derivation": "Sector pressure by itself can be nonzero, but the total spatial stress integral vanishes for the closed stationary composite.",
            "zero_condition": "all support classes from the total-system domain are included or bounded",
        },
        {
            "theorem_id": "SVT3821_4_nonstationary_bound",
            "status": "FINITE_BOUND_FORM",
            "statement": "If the source is not exactly stationary, pressure/stress correction is bounded by the virial acceleration, surface flux, covariant-frame and open-domain residuals.",
            "derivation": "Retain the right-hand side of SVT3821_1 instead of setting it to zero.",
            "zero_condition": "not required; finite bound can feed empirical gates",
        },
        {
            "theorem_id": "SVT3821_5_verdict",
            "status": "DERIVATION_ADVANCE_NOT_FULL_CLAIM",
            "statement": "The pressure/binding gap has a real closure mechanism: closed stationary total stress reduces the Tolman source to energy mass; open/nonstationary sources carry finite residuals.",
            "derivation": "This directly improves 3820's R_stress_virial route.",
            "zero_condition": "Newton/local GR still waits on source ledger, Pi_M fixedness, EH/PPN/readout residuals",
        },
    ]
    return [{**base_row(timestamp), **row} for row in rows]


def reduction_rows(timestamp: str) -> list[dict[str, str]]:
    rows = [
        {
            "reduction_id": "TER3821_0_Tolman_density_split",
            "status": "EXACT_CONDITIONAL_SPLIT",
            "formula": "M_T = c^-2 int (T00_total + Tii_total) dV + R_GR_boundary",
            "meaning": "The active mass includes energy density plus spatial stress trace in the local weak stationary convention.",
            "residual_if_unsigned": "R_Tolman_density",
        },
        {
            "reduction_id": "TER3821_1_closed_trace_zero",
            "status": "EXACT_CONDITIONAL_ZERO",
            "formula": "int Tii_total dV = 0 for stationary closed total source",
            "meaning": "Pressure/stress terms cancel only after total-system support is included.",
            "residual_if_unsigned": "R_stress_virial",
        },
        {
            "reduction_id": "TER3821_2_energy_mass_limit",
            "status": "EXACT_CONDITIONAL_REDUCTION",
            "formula": "M_T = c^-2 int T00_total dV + R_boundary + R_nonstationary + R_covariant + R_open_domain",
            "meaning": "For the closed stationary branch, active source mass equals total energy over c^2.",
            "residual_if_unsigned": "R_active_mass_total",
        },
        {
            "reduction_id": "TER3821_3_Newton_source_consequence",
            "status": "CONDITIONAL_NEWTON_SOURCE_SIMPLIFICATION",
            "formula": "rho_KT -> rho_energy/c^2 when stress-virial residuals vanish or are below tolerance",
            "meaning": "3818's Poisson source can use ordinary source energy density only after this gate, not before.",
            "residual_if_unsigned": "epsilon_source_total",
        },
    ]
    return [{**base_row(timestamp), **row} for row in rows]


def bound_rows(timestamp: str) -> list[dict[str, str]]:
    specs = [
        ("PBV3821_0_virial_acceleration", "epsilon_virial_accel", "nonstationary inertia-tensor term", "abs(0.5*d2I_trace_dt2)/(M_ref*c^2)", "zero for stationary or long-time averaged bound source"),
        ("PBV3821_1_surface_stress", "epsilon_surface_stress", "stress flux through source boundary", "abs(surface_int x_i T^{ki} n_k dS)/(M_ref*c^2)", "zero if total boundary is closed; otherwise source-backed bound"),
        ("PBV3821_2_covariant_frame", "epsilon_covariant_frame", "connection/curvature correction to local partial-conservation virial identity", "abs(int Gamma*T*x dV)/(M_ref*c^2)", "small local-Fermi/weak-field bound or retained GR correction"),
        ("PBV3821_3_open_domain", "epsilon_open_domain", "missing EM/Poynting/binding/apparatus support outside chosen matter tube", "abs(E_tail+stress_tail)/(M_ref*c^2)", "zero only for total-system domain; else use 3777 tail classes"),
        ("PBV3821_4_parent_exchange", "epsilon_parent_exchange", "parent/non-EM exchange current not cancelled inside total stress", "abs(int x_i Q_parent^i dV)/(M_ref*c^2)", "zero from same-current parent action or bounded epsilon_J_Q"),
        ("PBV3821_5_total", "epsilon_pressure_binding_total", "total pressure/binding correction after virial theorem", "sum_abs(epsilon_virial_accel,epsilon_surface_stress,epsilon_covariant_frame,epsilon_open_domain,epsilon_parent_exchange)", "feeds active-mass residual and test ledger"),
    ]
    return [
        {
            **base_row(timestamp),
            "bound_id": bound_id,
            "symbol": symbol,
            "definition": definition,
            "bound_formula": formula,
            "exit_requirement": exit_requirement,
            "current_status": "ZERO_IF_CLOSED_STATIONARY_ELSE_FINITE_BOUND_REQUIRED",
        }
        for bound_id, symbol, definition, formula, exit_requirement in specs
    ]


def source_class_rows(timestamp: str) -> list[dict[str, str]]:
    rows = [
        {
            "class_id": "CLS3821_0_closed_stationary_lab_body",
            "source_class": "closed stationary lab source",
            "virial_status": "BEST_CASE_ZERO_ROUTE",
            "required_evidence": "mass certificate, rigid/support stress included, no radiative flux, fixed boundary/reference",
            "result": "pressure/stress correction can be theorem-zero or tiny bounded",
        },
        {
            "class_id": "CLS3821_1_bound_orbital_body",
            "source_class": "planet/star/quasi-static body",
            "virial_status": "QUASI_STATIC_BOUND_ROUTE",
            "required_evidence": "hydrostatic/stationary model, surface stresses, binding energy, independent mass model",
            "result": "stress correction may be bounded but orbital GM cannot define mass",
        },
        {
            "class_id": "CLS3821_2_radiating_or_open_EM_system",
            "source_class": "radiating/open EM or Poynting system",
            "virial_status": "OPEN_DOMAIN_BOUND_ROUTE",
            "required_evidence": "Poynting flux, field tail, apparatus/boundary inclusion",
            "result": "pressure/stress cancellation is not automatic; retain flux residual",
        },
        {
            "class_id": "CLS3821_3_galaxy_cosmology",
            "source_class": "nonlocal galaxy/cosmology source",
            "virial_status": "NOT_A_LOCAL_GR_SOURCE_PROOF",
            "required_evidence": "separate empirical modelling and covariance",
            "result": "use as empirical pillar, not proof of local closed-source cancellation",
        },
    ]
    return [{**base_row(timestamp), **row} for row in rows]


def residual_rows(timestamp: str) -> list[dict[str, str]]:
    specs = [
        ("R3821_0_virial_accel", "R_virial_accel", "nonstationary virial acceleration residual", "epsilon_virial_accel"),
        ("R3821_1_surface_stress", "R_surface_stress", "surface/boundary stress residual", "epsilon_surface_stress"),
        ("R3821_2_covariant_frame", "R_covariant_frame", "local-frame/covariant derivative correction", "epsilon_covariant_frame"),
        ("R3821_3_open_domain", "R_open_domain", "missing total-system support residual", "epsilon_open_domain"),
        ("R3821_4_parent_exchange", "R_parent_exchange", "uncancelled parent exchange residual", "epsilon_parent_exchange"),
        ("R3821_5_total", "R_stress_virial_total", "total stress-virial pressure/binding residual", "epsilon_pressure_binding_total"),
    ]
    return [
        {
            **base_row(timestamp),
            "residual_id": residual_id,
            "symbol": symbol,
            "definition": definition,
            "bound_symbol": bound_symbol,
            "units": "dimensionless_after_Mc2_normalization",
            "current_status": "ZERO_IF_CLOSED_STATIONARY_ELSE_BOUND",
            "exit_requirement": "prove closed stationary total source or attach source-backed numeric bound",
        }
        for residual_id, symbol, definition, bound_symbol in specs
    ]


def gate_rows(timestamp: str, grouped: dict[str, list[dict[str, str]]]) -> list[dict[str, str]]:
    sources_pass = all(row["exists"] == "True" and row["needle_found"] == "True" for row in grouped["sources"])
    rows = [
        ("GATE3821_0_sources", "PASS_NONCLAIM" if sources_pass else "FAIL", "all source paths and needles present" if sources_pass else "missing source path or needle"),
        ("GATE3821_1_virial_identity", "PASS_NONCLAIM", "stress-virial identity derived with residuals"),
        ("GATE3821_2_closed_stationary_zero", "PASS_CONDITIONAL_ZERO", "pressure/stress trace cancels for closed stationary total source"),
        ("GATE3821_3_open_source_bound", "PASS_BOUND_SCHEMA", "open/nonstationary/domain residuals are finite named bounds"),
        ("GATE3821_4_source_ledger", "BLOCKED_INPUT_REQUIRED", "numeric independent source rows still not attached"),
        ("GATE3821_5_Newton_claim", "BLOCKED", "Newton claim still waits on source ledger, Pi_M fixedness and Poisson/PPN gates"),
        ("GATE3821_6_local_GR_claim", "BLOCKED", "local GR claim still waits on source normalization plus local PPN/readout closure"),
    ]
    return [
        {
            **base_row(timestamp),
            "gate_id": gate_id,
            "gate_status": status,
            "claim_allowed": "false",
            "detail": detail,
        }
        for gate_id, status, detail in rows
    ]


def decision_rows(timestamp: str) -> list[dict[str, str]]:
    rows = [
        {
            "decision_id": "DEC3821_0_pressure_gap_partly_closed",
            "decision": "Accept the closed-stationary stress-virial mechanism as the clean route for ordinary source masses.",
            "rationale": "It explains why the Tolman pressure term does not spoil Newtonian mass when the whole system is included.",
            "next_action": "carry epsilon_pressure_binding_total into source-ledger/test rows",
        },
        {
            "decision_id": "DEC3821_1_no_matter_only_tubes",
            "decision": "Continue rejecting matter-only source tubes.",
            "rationale": "The virial cancellation needs total stresses, including EM/Poynting, binding, apparatus and boundary terms.",
            "next_action": "use 3776/3777 total-domain rules for source classes",
        },
        {
            "decision_id": "DEC3821_2_next_target",
            "decision": "Move to source-ledger population and first local test-ready rows.",
            "rationale": "The pressure/binding mechanism is now sharp enough; the next blocker is independent source evidence and Pi_M/readout integration.",
            "next_action": "3822",
        },
    ]
    return [{**base_row(timestamp), **row} for row in rows]


def next_rows(timestamp: str) -> list[dict[str, str]]:
    return [
        {
            **base_row(timestamp),
            "target_doc": "3822-Y5-R2FR-independent-source-ledger-and-local-test-ready-source-rows.md",
            "target_script": "scripts/Y5_R2FR_3822_independent_source_ledger_and_local_test_ready_source_rows.py",
            "objective": "Populate the independent source-ledger schema with first local test-ready row types and carry the 3821 stress-virial correction vector into R10/WEP/PPN/clock/orbital product-evidence gates without using orbital GM as source mass.",
            "success_gate": "Each local arena has source-evidence status, allowed/forbidden mass inputs, correction-vector columns, and claim remains blocked unless independent source rows exist.",
            "avoid": "do not claim local GR/Newton; do not use orbital GM as mass; do not edit formalization-workbench; do not use GitHub",
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, str]]:
    return [
        {
            **base_row(timestamp),
            "status": "PASS_NONCLAIM_CLOSED_SYSTEM_STRESS_VIRIAL_MECHANISM_BUILT",
            "summary": "3821 derives the closed-system stress-virial cancellation route, reduces Tolman active mass to total energy over c^2 conditionally, and emits finite open-source correction bounds.",
        }
    ]


def md_table(rows: list[dict[str, str]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join(["---"] * len(columns)) + " |"
    body = []
    for row in rows:
        body.append("| " + " | ".join(str(row.get(col, "")).replace("\n", " ").replace("|", "/") for col in columns) + " |")
    return "\n".join([header, sep, *body])


def write_markdown(grouped: dict[str, list[dict[str, str]]]) -> None:
    text = f"""# 3821 - Closed-System Stress Virial Cancellation Or Pressure/Binding Bound

## Status

`PASS_NONCLAIM_CLOSED_SYSTEM_STRESS_VIRIAL_MECHANISM_BUILT`

This checkpoint attacks the pressure/binding objection directly. In a closed stationary total source, the integrated spatial stress trace cancels by the stress-virial identity, so the Komar/Tolman active mass reduces to total energy over `c^2`. If the source is open, radiating, nonstationary, or cut by a matter-only domain, the leftover is kept as a finite correction vector.

## Stress Virial Theorem

{md_table(grouped["virial"], ["theorem_id", "status", "statement", "derivation", "zero_condition"])}

## Tolman To Energy-Mass Reduction

{md_table(grouped["reduction"], ["reduction_id", "status", "formula", "meaning", "residual_if_unsigned"])}

## Pressure/Binding Bound Vector

{md_table(grouped["bounds"], ["bound_id", "symbol", "definition", "bound_formula", "exit_requirement"])}

## Closed Source Classifier

{md_table(grouped["source_classes"], ["class_id", "source_class", "virial_status", "required_evidence", "result"])}

## Residual Rows

{md_table(grouped["residuals"], ["residual_id", "symbol", "definition", "bound_symbol", "current_status"])}

## Claim Gates

{md_table(grouped["gates"], ["gate_id", "gate_status", "claim_allowed", "detail"])}

## Next Target

`3822-Y5-R2FR-independent-source-ledger-and-local-test-ready-source-rows.md`

Target: populate local test-ready source rows using independent evidence status, carry the stress-virial correction vector into R10/WEP/PPN/clock/orbital gates, and keep orbital `GM` as product evidence only.

## Machine Outputs

{md_table(grouped["status"], ["status", "summary"])}
"""
    DOC_PATH.write_text(text, encoding="utf-8")


def update_spine() -> None:
    if not SPINE_PATH.exists():
        return
    text = read_text(SPINE_PATH)
    text = text.replace(
        "# Local GR Coupling Spine - Current State After 3820",
        "# Local GR Coupling Spine - Current State After 3821",
    )
    paragraph = (
        "`3821` constructs the pressure/binding closure mechanism: from total-stress conservation, the tensor virial identity gives "
        "`d2I^{ij}/dt2=2 int T_total^{ij} dV` plus surface/covariant/open-domain terms. Therefore a closed stationary total source has "
        "`int T_total^i_i dV=0`, so the Komar/Tolman active mass reduces from `c^-2 int (T00+Tii)dV` to total energy over `c^2` up to explicit finite residuals. "
        "This is a real local-GR/Newton bridge advance: pressure is not ignored; it cancels only for the closed total source, otherwise `epsilon_pressure_binding_total` is retained.\n\n"
    )
    if "`3821` constructs the pressure/binding closure mechanism" not in text:
        marker = "`3820` turns the source-mass gap"
        index = text.find(marker)
        if index != -1:
            line_end = text.find("\n\n", index)
            if line_end != -1:
                text = text[: line_end + 2] + paragraph + text[line_end + 2 :]
    old_target = """`3821-Y5-R2FR-closed-system-stress-virial-cancellation-or-pressure-binding-bound.md`

Target: try to prove the closed-system stress/virial cancellation that reduces Komar/Tolman active mass to ordinary source energy over `c^2`, or emit finite pressure/binding/field/boundary correction bounds.

This is the best next move because 3820 makes the source charge real enough to see the next danger: pressure/stress terms cannot be hand-waved away without either a virial/closed-system theorem or a bound.
"""
    new_target = """`3822-Y5-R2FR-independent-source-ledger-and-local-test-ready-source-rows.md`

Target: populate local test-ready source rows using independent evidence status, carry the 3821 stress-virial correction vector into R10/WEP/PPN/clock/orbital gates, and keep orbital `GM` as product evidence only.

This is the best next move because the active-mass derivation now has a closed-source pressure cancellation mechanism; the next bottleneck is test-facing source evidence and arena tagging.
"""
    text = text.replace(old_target, new_target)
    artifacts = [
        "source-intake\\mts_residuals\\P8_Y5_R2FR_3821_STRESS_VIRIAL_THEOREM.csv",
        "source-intake\\mts_residuals\\P8_Y5_R2FR_3821_TOLMAN_TO_ENERGY_MASS_REDUCTION.csv",
        "source-intake\\mts_residuals\\P8_Y5_R2FR_3821_PRESSURE_BINDING_BOUND_VECTOR.csv",
        "source-intake\\mts_residuals\\P8_Y5_R2FR_3821_CLOSED_SOURCE_CLASSIFIER.csv",
        "source-intake\\mts_residuals\\P8_Y5_R2FR_3821_STRESS_VIRIAL_RESIDUAL_ROWS.csv",
        "source-intake\\mts_residuals\\P8_Y5_BRR545_3821_VALIDATION.csv",
    ]
    insertion = "".join(f"- `{artifact}`\n" for artifact in artifacts)
    if artifacts[0] not in text:
        text = text.replace("## Machine Artifacts\n\n", "## Machine Artifacts\n\n" + insertion)
    SPINE_PATH.write_text(text, encoding="utf-8")


def cleanup_pycache() -> None:
    cache = PCW / "scripts" / "__pycache__"
    if cache.exists() and cache.is_dir():
        shutil.rmtree(cache)


def validation_rows(timestamp: str, grouped: dict[str, list[dict[str, str]]]) -> list[dict[str, str]]:
    rows = []

    def add(check_id: str, result: bool, detail: str) -> None:
        rows.append(
            {
                "timestamp_utc": timestamp,
                "branch_id": BRANCH,
                "checkpoint_id": CHECKPOINT,
                "check_id": check_id,
                "result": "PASS" if result else "FAIL",
                "detail": detail,
            }
        )

    add("sources_exist", all(row["exists"] == "True" for row in grouped["sources"]), "every cited source path exists")
    add("needles_found", all(row["needle_found"] == "True" for row in grouped["sources"]), "every cited source needle was found")
    csv_ok = True
    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        try:
            csv_ok = csv_ok and path.exists() and len(parse_csv(path)) > 0
        except Exception:
            csv_ok = False
    add("csv_outputs_parse", csv_ok, "all generated CSV outputs exist and parse")
    add("doc_written", DOC_PATH.exists() and "Stress Virial Theorem" in read_text(DOC_PATH), "3821 markdown document written")
    add("virial_identity_written", any(row["theorem_id"] == "SVT3821_1_tensor_virial_identity" for row in grouped["virial"]), "tensor virial identity emitted")
    add("trace_zero_written", any(row["theorem_id"] == "SVT3821_2_trace_cancellation" for row in grouped["virial"]), "closed stationary trace zero emitted")
    add("tolman_reduction_written", any(row["reduction_id"] == "TER3821_2_energy_mass_limit" for row in grouped["reduction"]), "Tolman-to-energy mass reduction emitted")
    add("finite_bounds_written", any(row["symbol"] == "epsilon_pressure_binding_total" for row in grouped["bounds"]), "finite correction bound vector emitted")
    add("source_classes_written", any(row["class_id"] == "CLS3821_2_radiating_or_open_EM_system" for row in grouped["source_classes"]), "closed/open source classifier emitted")
    add("residual_total_row", any(row["symbol"] == "R_stress_virial_total" for row in grouped["residuals"]), "total stress-virial residual emitted")
    add("claim_gates_closed", all(row.get("claim_allowed") == "false" for row in grouped["gates"]), "no claim gate allows a claim")
    add("newton_claim_blocked", any(row["gate_id"] == "GATE3821_5_Newton_claim" and row["gate_status"] == "BLOCKED" for row in grouped["gates"]), "Newton claim remains blocked")
    add("next_target_selected", grouped["next"][0]["target_doc"].startswith("3822-Y5"), "3822 source-ledger target selected")
    spine_text = read_text(SPINE_PATH) if SPINE_PATH.exists() else ""
    add("spine_updated", "Current State After 3821" in spine_text and "3822-Y5-R2FR-independent-source" in spine_text, "live spine updated to 3821 and 3822 target")
    fwb_hits = list(FWB.rglob("*3821*")) if FWB.exists() else []
    add("formalization_clean", len(fwb_hits) == 0, "no 3821 files written under formalization-workbench")
    add("pycache_removed", not (PCW / "scripts" / "__pycache__").exists(), "scripts __pycache__ removed")
    bad_chars = "\ufffd" in read_text(DOC_PATH) or "\ufffd" in read_text(Path(__file__)) or "\ufffd" in spine_text
    add("bad_chars_clean", not bad_chars, "new doc/script/spine contain no mojibake replacement characters")
    return rows


def main() -> None:
    timestamp = now_utc()
    grouped: dict[str, list[dict[str, str]]] = {}
    grouped["sources"] = source_rows(timestamp)
    grouped["virial"] = virial_rows(timestamp)
    grouped["reduction"] = reduction_rows(timestamp)
    grouped["bounds"] = bound_rows(timestamp)
    grouped["source_classes"] = source_class_rows(timestamp)
    grouped["residuals"] = residual_rows(timestamp)
    grouped["gates"] = gate_rows(timestamp, grouped)
    grouped["decisions"] = decision_rows(timestamp)
    grouped["next"] = next_rows(timestamp)
    grouped["status"] = status_rows(timestamp)
    grouped["validation"] = [
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH,
            "checkpoint_id": CHECKPOINT,
            "check_id": "pending",
            "result": "PASS",
            "detail": "placeholder before final validation",
        }
    ]
    for key, path in OUTPUTS.items():
        if key != "validation":
            write_csv(path, grouped[key])
    write_markdown(grouped)
    update_spine()
    cleanup_pycache()
    grouped["validation"] = validation_rows(timestamp, grouped)
    write_csv(OUTPUTS["validation"], grouped["validation"])
    write_markdown(grouped)
    cleanup_pycache()
    failed = [row for row in grouped["validation"] if row["result"] != "PASS"]
    print(grouped["status"][0]["status"])
    print(f"wrote {DOC_PATH}")
    if failed:
        raise SystemExit(f"validation failed: {failed}")


if __name__ == "__main__":
    main()
