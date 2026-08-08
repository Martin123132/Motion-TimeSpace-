from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


BRANCH_ID = "MTS_R2FR_EH_BASELINE_PLUS_MTS_RESIDUAL_CURRENT_PACK_FOR_S_EQ_2446"
CHECKPOINT_ID = "2446"

ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = ROOT.parent
FORMALIZATION = PROJECT_ROOT / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
HAMILTONIAN = ROOT / "source-intake" / "hamiltonian-source"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"

DOC = ROOT / "2446-Y5-R2FR-EH-baseline-plus-MTS-residual-current-pack-for-S-Eq.md"

OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_2446_SOURCE_REGISTER.csv",
    "eh_baseline": OUT / "P8_Y5_PARENT_QLOC_2446_EH_BASELINE_SOURCE_CURRENT_COMPARATOR.csv",
    "residual_pack": OUT / "P8_Y5_PARENT_QLOC_2446_MTS_RESIDUAL_CURRENT_PACK_FOR_S_EQ.csv",
    "seq_envelope": OUT / "P8_Y5_PARENT_QLOC_2446_S_EQ_NO_CANCELLATION_ENVELOPE.csv",
    "residual_schema": OUT / "P8_Y5_PARENT_QLOC_2446_RESIDUAL_CURRENT_INPUT_SCHEMA.csv",
    "claim_gates": OUT / "P8_Y5_PARENT_QLOC_2446_CLAIM_GATES.csv",
    "decisions": OUT / "P8_Y5_PARENT_QLOC_2446_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_2446_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_PARENT_QLOC_2446_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2446_VALIDATION.csv",
}

COPY_TARGETS = {
    "queue_residual_pack": QUEUE / "JR2446_MTS_RESIDUAL_CURRENT_PACK_FOR_S_EQ_NONCLAIM.csv",
    "queue_residual_schema": QUEUE / "JR2446_RESIDUAL_CURRENT_INPUT_SCHEMA_NONCLAIM.csv",
    "hamiltonian_residual_pack": HAMILTONIAN / "MTS_residual_current_pack_for_S_Eq_2446_NONCLAIM.csv",
    "local_envelope": LOCAL_BOUNDS / "S_Eq_no_cancellation_envelope_2446_NONCLAIM.csv",
}

SOURCES = [
    {
        "source_id": "SRC2446_00_2445_doc",
        "source_path": ROOT / "2445-Y5-R2FR-Jq-source-current-extraction-from-parent-L-or-Htau-source-charge-certificate.md",
        "needles": ["NEXT2445_0_selected", "JQX2445_5_verdict", "SEQ2445_4_verdict", "VAL2445_OVERALL"],
        "role": "fresh handoff selecting EH baseline plus residual-current pack",
    },
    {
        "source_id": "SRC2446_01_2445_jq_csv",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_2445_JQ_SOURCE_CURRENT_EXTRACTION_ATTEMPT.csv",
        "needles": ["JQX2445_0_target", "JQX2445_5_verdict", "NOT_EXTRACTED_CERTIFICATE_REQUIRED"],
        "role": "current J_q extraction failure ledger",
    },
    {
        "source_id": "SRC2446_02_2445_seq_status",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_2445_S_EQ_STATUS_UPDATE.csv",
        "needles": ["SEQ2445_4_verdict", "NOT_OWNED", "product closure only"],
        "role": "current S_Eq product-only status",
    },
    {
        "source_id": "SRC2446_03_994_doc",
        "source_path": ROOT / "994-Y5-R10-EH-baseline-current-plus-MTS-residual-current-pack.md",
        "needles": ["EHB994_0_L_EH", "RC994_0_reference_boundary", "DEC994_2_next_target"],
        "role": "older EH baseline plus residual-current pack",
    },
    {
        "source_id": "SRC2446_04_994_baseline_csv",
        "source_path": OUT / "P8_Y5_R10_994_EH_BASELINE_CURRENT.csv",
        "needles": ["EHB994_0_L_EH", "EHB994_2_Qtau_EH", "EHB994_3_Poisson_Gauss"],
        "role": "machine-readable EH baseline comparator rows",
    },
    {
        "source_id": "SRC2446_05_994_residual_csv",
        "source_path": OUT / "P8_Y5_R10_994_MTS_RESIDUAL_CURRENT_PACK.csv",
        "needles": ["RC994_0_reference_boundary", "RC994_6_EM_clock_coupling_guard", "not_extracted"],
        "role": "machine-readable old residual-current pack",
    },
    {
        "source_id": "SRC2446_06_993_sector_csv",
        "source_path": OUT / "P8_Y5_R10_993_SECTOR_CURRENT_EXTRACTION_LEDGER.csv",
        "needles": ["SEC993_0_EH_core", "SEC993_3_extra_motion_time_memory", "SEC993_6_metric_readout_PiM"],
        "role": "sector current extraction status supporting residual split",
    },
    {
        "source_id": "SRC2446_07_992_residual_csv",
        "source_path": OUT / "P8_Y5_R10_992_CHARGE_CURRENT_RESIDUAL_LEDGER.csv",
        "needles": ["SCE992_Delta_frame", "SCE992_Delta_PiM", "SCE992_Delta_PPN"],
        "role": "charge-current residual names feeding source-leg residuals",
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


def eh_baseline_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "baseline_id": "EHS2446_0_pure_EH_qblind",
            "object": "S_E^q_EH_comparator",
            "reference_form": "pure EH plus q-independent minimally coupled matter has no independent q-source current, so J_q^EH=0 by construction",
            "what_it_buys": "clean target: MTS should reduce to no local q-source leg if all residual currents vanish",
            "allowed_use": "comparator for the desired GR/Newton source-current limit",
            "forbidden_use": "proof that MTS J_q or S_E^q is zero",
        },
        {
            "baseline_id": "EHS2446_1_EH_Htau",
            "object": "H_tau^EH",
            "reference_form": "standard EH covariant phase-space Hamiltonian charge with fixed boundary/reference and shared tau",
            "what_it_buys": "shape of source mass/Poisson/Gauss target after source equality closes",
            "allowed_use": "normalization comparator for H_tau certificate",
            "forbidden_use": "orbital GM substitution or total MTS H_tau claim",
        },
        {
            "baseline_id": "EHS2446_2_EH_weak_field",
            "object": "GR weak-field source law",
            "reference_form": "nabla^2 Phi=4*pi*G_ref rho and g_00=-1+2G_ref M/r+...",
            "what_it_buys": "downstream Newton target once MTS source charge is owned",
            "allowed_use": "later PPN/Newton comparator",
            "forbidden_use": "skipping residual-current pack",
        },
        {
            "baseline_id": "EHS2446_3_verdict",
            "object": "EH baseline",
            "reference_form": "comparator-only",
            "what_it_buys": "separates GR target from MTS residual debts",
            "allowed_use": "ruler",
            "forbidden_use": "smuggled derivation",
        },
    ]
    return [base_row(**row) for row in rows]


def residual_pack_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "residual_id": "RCS2446_0_reference_boundary",
            "residual_current_piece": "J_q^boundary + partial_q(B_ref) + q-sensitive boundary/corner flux",
            "feeds_S_Eq_through": "H_tau source-charge sensitivity and deltaH integrability",
            "old_basis": "RC994_0_reference_boundary; SCE992_Delta_symp; SCE992_Delta_ref",
            "current_status": "NOT_PARENT_FIXED",
            "required_zero_or_bound": "fixed B_ref plus exact/cohomology/nohair boundary theorem, or source-backed boundary residual row",
            "blocks_if_open": "S_E^q via H_tau and source mass normalization",
        },
        {
            "residual_id": "RCS2446_1_extra_nonEH",
            "residual_current_piece": "J_q^extra from motion/time/domain/memory/range/non-EH sectors",
            "feeds_S_Eq_through": "direct q-current and non-EH source charge",
            "old_basis": "RC994_1_extra_nonEH; SEC993_3_extra_motion_time_memory; SCE992_Delta_extra",
            "current_status": "NOT_EXTRACTED",
            "required_zero_or_bound": "sector-by-sector no-source/topological/proper-gauge theorem or executable coefficient vector",
            "blocks_if_open": "EH-only/local-GR reduction and finite-range source tests",
        },
        {
            "residual_id": "RCS2446_2_projector_domain",
            "residual_current_piece": "J_q^projector + [d,Pi_M]J_H + delta Pi_M source terms",
            "feeds_S_Eq_through": "mass/source projection and radial/source stability",
            "old_basis": "RC994_2_projector_domain; SCE992_Delta_PiM; SCE992_Delta_flux",
            "current_status": "NOT_EXTRACTED",
            "required_zero_or_bound": "parent-owned Pi_M/P_loc chain map, covariant constancy, domain/homology rule, or commutator bound",
            "blocks_if_open": "source-current closure and Newton source normalization",
        },
        {
            "residual_id": "RCS2446_3_matter_source_glue",
            "residual_current_piece": "J_q^matter/source glue from coframe, worldtube denominator, Hilbert-current equality and source composition",
            "feeds_S_Eq_through": "direct WEP/R10 source current and observed source equality",
            "old_basis": "RC994_3_matter_source_glue; SCE992_Delta_frame; SCE992_Delta_cal",
            "current_status": "CONDITIONAL_NOT_GLUED",
            "required_zero_or_bound": "same observed coframe, parent matter functor, Hilbert/source equality, worldtube denominator theorem",
            "blocks_if_open": "observed mass/GM equality and local product isolation",
        },
        {
            "residual_id": "RCS2446_4_coupling_constant",
            "residual_current_piece": "partial_q G_eff/kappa/source-normalization drift",
            "feeds_S_Eq_through": "common source normalization, Gdot, range/species/frame dependence",
            "old_basis": "RC994_4_coupling_constant; SCE992_Delta_G; SEC993_1_kappa_topological",
            "current_status": "NOT_PARENT_DERIVED",
            "required_zero_or_bound": "constant universal G_ref/kappa theorem or sourced Gdot/range/species/frame bounds",
            "blocks_if_open": "Newtonian normalization and local tests across arenas",
        },
        {
            "residual_id": "RCS2446_5_readout_PPN_tail",
            "residual_current_piece": "J_q^readout + second-order PPN/source-response tail",
            "feeds_S_Eq_through": "metric/readout source leg and PPN vector",
            "old_basis": "RC994_5_readout_PPN_tail; SEC993_6_metric_readout_PiM; SCE992_Delta_PPN",
            "current_status": "DOWNSTREAM_NOT_READY",
            "required_zero_or_bound": "weak-field/PPN response matrix from same source charge and metric readout",
            "blocks_if_open": "local-GR/PPN claim even after first-order source charge improves",
        },
        {
            "residual_id": "RCS2446_6_EM_clock_mass_coupling_guard",
            "residual_current_piece": "J_q^visible_coefficients from alpha, mass, binding, clock and source-weight leakage",
            "feeds_S_Eq_through": "WEP/R10/clock product rows S_E^q*b_i and source-weight products",
            "old_basis": "RC994_6_EM_clock_coupling_guard; 2441-2445 b_alpha/b_mhat/b_nuc/source leg chain",
            "current_status": "GUARD_ONLY_RETAINED",
            "required_zero_or_bound": "EM-lock/mass-owner/source-scalar/readout theorem-zero or finite product rows",
            "blocks_if_open": "composition/readout leakage in source-current proof",
        },
        {
            "residual_id": "RCS2446_7_verdict",
            "residual_current_piece": "J_q^MTS - J_q^EH",
            "feeds_S_Eq_through": "all local source-leg products",
            "old_basis": "994 residual pack translated to S_Eq",
            "current_status": "PACK_COMPLETE_NONCLAIM",
            "required_zero_or_bound": "every residual family zero or source-backed bounded",
            "blocks_if_open": "S_E^q derivation and isolated local coefficient tests",
        },
    ]
    return [base_row(**row) for row in rows]


def seq_envelope_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "envelope_id": "SEQE2446_0_definition",
            "expression": "|S_E^q| <= |S_E^q_EH_comparator| + sum_i |P_arena[G_q RCS2446_i]/N_E|",
            "status": "DEFINITION_ONLY",
            "why_nonclaim": "all residual current values are missing and EH comparator cannot be imported as MTS proof",
            "required_exit": "numeric/theorem-zero rows for every residual-current family with shared projection and positive normalization",
        },
        {
            "envelope_id": "SEQE2446_1_EH_target",
            "expression": "S_E^q_EH_comparator=0 only in pure EH/q-blind matter comparator",
            "status": "COMPARATOR_ONLY",
            "why_nonclaim": "MTS contains extra/source/readout/coupling sectors not shown q-blind",
            "required_exit": "prove all RCS2446_i vanish or are bounded",
        },
        {
            "envelope_id": "SEQE2446_2_no_cancellation",
            "expression": "residuals add as absolute values unless a signed material/readout model proves cancellation",
            "status": "ACTIVE_GUARD",
            "why_nonclaim": "guard prevents fake source-leg silence",
            "required_exit": "component rows with units/source paths",
        },
        {
            "envelope_id": "SEQE2446_3_product_closure",
            "expression": "local observable rows use products S_E^q*b_i or projected source-current products until envelope is closed",
            "status": "PRODUCT_ONLY",
            "why_nonclaim": "S_E^q is not isolated",
            "required_exit": "J_q/H_tau certificate and residual-current closure",
        },
    ]
    return [base_row(**row, score_ready=False) for row in rows]


def residual_schema_rows() -> list[dict[str, Any]]:
    rows = [
        ("RIS2446_0_residual_current", "residual_id; sector; J_q_residual_formula; zero_theorem_or_bound; value; units; source_path; valid_for_claim", "source-current residual rows", "MISSING_VALUES", False),
        ("RIS2446_1_projection", "arena; kernel_Gq; P_arena; source_worldtube; normalization_N; q_units; source_path; valid_for_claim", "project residual currents into S_E^q", "MISSING_PROJECTION", False),
        ("RIS2446_2_EH_comparator", "EH_term; formula; normalization; boundary_condition; tau_id; source_path; comparator_only", "explicit EH baseline detail rows", "REFERENCE_SCHEMA_READY", False),
        ("RIS2446_3_envelope", "arena; sum_abs_residuals; EH_comparator_value; S_Eq_bound; units; assumptions; valid_for_claim", "future no-cancellation runner input", "MISSING_ENVELOPE_VALUES", False),
        ("RIS2446_4_promotion_gate", "all residuals zero/bounded; no MISSING markers; no EH import; no cancellation; no orbital GM substitution", "claim promotion guard", "ACTIVE_GUARD", False),
    ]
    return [
        base_row(schema_id=schema_id, required_columns=columns, purpose=purpose, current_status=status, ready_for_claim=ready)
        for schema_id, columns, purpose, status, ready in rows
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("CG2446_0_EH_comparator", "EH baseline comparator is written", "PASS_NONCLAIM", "allowed as ruler only", True),
        ("CG2446_1_residual_pack", "MTS residual-current families are named", "PASS_NONCLAIM", "pack is complete but nonnumeric/nonclaim", True),
        ("CG2446_2_residual_zero", "all MTS residual currents vanish or are bounded", "BLOCKED", "no residual value/theorem rows exist yet", False),
        ("CG2446_3_SEq_closed", "S_E^q is derived or bounded", "BLOCKED", "residual-current envelope has missing values/projection", False),
        ("CG2446_4_local_tests", "local tests isolate coefficients", "BLOCKED", "S_E^q remains product-only", False),
        ("CG2446_5_GR_Newton", "GR/Newton local reduction is derived", "BLOCKED", "source charge plus weak-field/PPN readout remain downstream", False),
    ]
    return [
        base_row(claim_id=claim_id, claim=claim, gate_status=status, reason=reason, gate_pass=gate_pass)
        for claim_id, claim, status, reason, gate_pass in rows
    ]


def decision_rows() -> list[dict[str, Any]]:
    rows = [
        ("DEC2446_0_EH_policy", "EH_BASELINE_ACCEPTED_AS_COMPARATOR_ONLY", "EH gives the GR/Newton target shape without proving MTS current ownership", "keep EH as ruler, not proof"),
        ("DEC2446_1_residual_pack", "S_EQ_RESIDUAL_CURRENT_PACK_ACCEPTED", "seven residual families cover the current pieces missing from 993 and the local coupling chain", "attack residuals one by one"),
        ("DEC2446_2_envelope", "S_EQ_NO_CANCELLATION_ENVELOPE_REQUIRED", "residual-current cancellation would fake local source-leg silence", "future runner uses absolute envelope"),
        ("DEC2446_3_next", "TARGET_BOUNDARY_REFERENCE_RESIDUAL_FIRST", "boundary/reference residual blocks Hamiltonian integrability and was already selected by 994", "select 2447"),
        ("DEC2446_4_public", "NO_GITHUB_ACTION", "private nonclaim derivation checkpoint", "continue privately"),
    ]
    return [
        base_row(decision_id=decision_id, decision=decision, rationale=rationale, consequence=consequence)
        for decision_id, decision, rationale, consequence in rows
    ]


def next_target_rows() -> list[dict[str, Any]]:
    row = {
        "route_id": "NEXT2446_0_selected",
        "selection_status": "selected",
        "target_file": "2447-Y5-R2FR-boundary-reference-source-current-zero-theorem-or-S-Eq-residual-bound-row.md",
        "target_script": "scripts/Y5_R2FR_boundary_reference_source_current_zero_theorem_or_S_Eq_residual_bound_row_2447.py",
        "task": "try to prove the boundary/reference source-current residual RCS2446_0 vanishes through fixed B_ref, exact/cohomology/nohair boundary control, or stage a source-backed residual bound row",
        "acceptance_target": "RCS2446_0 is theorem-zero under a parent-signed boundary/reference contract, or remains an explicit nonclaim residual with units/source/projection blockers",
        "guardrails": "do not import EH boundary terms as MTS proof; do not tune B_ref to source mass; do not set boundary flux to zero by taste; do not claim S_Eq/WEP/PPN/local GR; do not edit formalization-workbench; do not push GitHub",
    }
    return [base_row(**row)]


def copy_outputs() -> list[dict[str, Any]]:
    copy_specs = {
        "queue_residual_pack": (OUTPUTS["residual_pack"], COPY_TARGETS["queue_residual_pack"], "S_Eq residual-current pack queue"),
        "queue_residual_schema": (OUTPUTS["residual_schema"], COPY_TARGETS["queue_residual_schema"], "residual-current input schema queue"),
        "hamiltonian_residual_pack": (OUTPUTS["residual_pack"], COPY_TARGETS["hamiltonian_residual_pack"], "Hamiltonian/source residual-current pack"),
        "local_envelope": (OUTPUTS["seq_envelope"], COPY_TARGETS["local_envelope"], "S_Eq no-cancellation envelope for local bounds"),
    }
    rows: list[dict[str, Any]] = []
    for copy_id, (source, target, notes) in copy_specs.items():
        target.parent.mkdir(parents=True, exist_ok=True)
        if source.exists():
            shutil.copyfile(source, target)
        rows.append(base_row(copy_id=copy_id, source_path=source, target_path=target, source_exists=source.exists(), target_exists=target.exists(), notes=notes))
    return rows


def validation_rows(data: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    def add(check_id: str, ok: bool, notes: str, detail: str = "") -> None:
        rows.append({"check_id": check_id, "status": "PASS" if ok else "FAIL", "notes": notes, "detail": detail})

    add("VAL2446_00_sources_exist", all(row["path_exists"] for row in data["source_register"]), "all cited source paths exist")
    add("VAL2446_01_source_needles", all(row["needles_found"] for row in data["source_register"]), "all cited source needles are present")
    add(
        "VAL2446_02_EH_comparator_only",
        any(row["baseline_id"] == "EHS2446_3_verdict" and row["forbidden_use"] == "smuggled derivation" for row in data["eh_baseline"]),
        "EH baseline is comparator-only",
    )
    residual_ids = {row["residual_id"] for row in data["residual_pack"]}
    required_ids = {f"RCS2446_{index}_{suffix}" for index, suffix in [
        (0, "reference_boundary"),
        (1, "extra_nonEH"),
        (2, "projector_domain"),
        (3, "matter_source_glue"),
        (4, "coupling_constant"),
        (5, "readout_PPN_tail"),
        (6, "EM_clock_mass_coupling_guard"),
    ]}
    add("VAL2446_03_residual_families_present", required_ids <= residual_ids, "all seven residual-current families are present")
    add(
        "VAL2446_04_envelope_product_only",
        any(row["envelope_id"] == "SEQE2446_3_product_closure" and row["status"] == "PRODUCT_ONLY" for row in data["seq_envelope"]),
        "S_Eq envelope keeps local tests product-only",
    )
    add(
        "VAL2446_05_schema_fail_closed",
        all(not row["ready_for_claim"] for row in data["residual_schema"]),
        "residual schemas are nonclaim and fail closed",
    )
    add(
        "VAL2446_06_claim_gates_safe",
        all(row["gate_status"] in {"PASS_NONCLAIM", "BLOCKED"} and not row["valid_for_claim"] for row in data["claim_gates"]),
        "claim gates are safe and nonclaim",
    )
    add(
        "VAL2446_07_next_target_written",
        len(data["next_target"]) == 1 and data["next_target"][0]["route_id"] == "NEXT2446_0_selected",
        "2447 boundary/reference residual target selected",
    )
    add(
        "VAL2446_08_branch_copies",
        all(row["source_exists"] and row["target_exists"] for row in data["branch_copies"]),
        "branch copies exist",
    )
    formalization_hits: list[Path] = []
    if FORMALIZATION.exists():
        for path in FORMALIZATION.rglob("*"):
            name = path.name
            if any(marker in name for marker in ("2446-", "_2446", "2446_", "P8_Y5_PARENT_QLOC_2446", "P8_Y5_BRR545_2446")):
                formalization_hits.append(path)
    add("VAL2446_09_no_formalization_artifacts", len(formalization_hits) == 0, "no 2446 artifacts were written to formalization-workbench", "; ".join(str(path) for path in formalization_hits))

    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        ok, count, detail = csv_parses(path)
        add(f"VAL2446_CSV_{path.stem}", ok, f"CSV parses with {count} rows", detail)

    overall = all(row["status"] == "PASS" for row in rows)
    add(
        "VAL2446_OVERALL",
        overall,
        "2446 writes EH as comparator-only, stages the MTS residual-current pack for S_Eq, and selects boundary/reference residual next",
    )
    return rows


def write_doc(data: dict[str, list[dict[str, Any]]]) -> None:
    content = f"""# 2446 - Y5/R2FR EH Baseline Plus MTS Residual Current Pack For S_Eq

## Result
- 2446 separates the ruler from the theory: EH is allowed only as the source-current comparator, never as proof that MTS has reduced to GR.
- In the pure EH/q-blind comparator, `J_q^EH=0`; that is the local-source target, not an MTS result.
- The MTS side is now a seven-family residual-current pack feeding `S_E^q`: boundary/reference, extra non-EH, projector/domain, matter/source glue, coupling drift, readout/PPN tail, and EM/clock/mass/source-weight leakage.
- `S_E^q` therefore remains product-only until every residual family is theorem-zero or source-backed bounded under one shared local projection.
- Next target is the first residual: boundary/reference source-current leakage, because it blocks Hamiltonian integrability and fixed source mass.

## Source Register
{table(["source_id", "source_path", "path_exists", "needles_found", "role"], data["source_register"])}

## EH Baseline Source Current Comparator
{table(["baseline_id", "object", "reference_form", "what_it_buys", "allowed_use", "forbidden_use", "valid_for_claim"], data["eh_baseline"])}

## MTS Residual Current Pack For S_Eq
{table(["residual_id", "residual_current_piece", "feeds_S_Eq_through", "old_basis", "current_status", "required_zero_or_bound", "blocks_if_open", "valid_for_claim"], data["residual_pack"])}

## S_Eq No-Cancellation Envelope
{table(["envelope_id", "expression", "status", "why_nonclaim", "required_exit", "score_ready", "valid_for_claim"], data["seq_envelope"])}

## Residual Current Input Schema
{table(["schema_id", "required_columns", "purpose", "current_status", "ready_for_claim", "valid_for_claim"], data["residual_schema"])}

## Claim Gates
{table(["claim_id", "claim", "gate_status", "reason", "gate_pass", "valid_for_claim"], data["claim_gates"])}

## Decision Ledger
{table(["decision_id", "decision", "rationale", "consequence", "valid_for_claim"], data["decisions"])}

## Next Target
{table(["route_id", "selection_status", "target_file", "target_script", "task", "acceptance_target", "guardrails"], data["next_target"])}

## Branch Copies
{table(["copy_id", "source_path", "target_path", "source_exists", "target_exists", "notes"], data["branch_copies"])}

## Validation
{table(["check_id", "status", "notes", "detail"], data["validation"])}
"""
    DOC.write_text(content, encoding="utf-8")


def main() -> None:
    data: dict[str, list[dict[str, Any]]] = {
        "source_register": source_register_rows(),
        "eh_baseline": eh_baseline_rows(),
        "residual_pack": residual_pack_rows(),
        "seq_envelope": seq_envelope_rows(),
        "residual_schema": residual_schema_rows(),
        "claim_gates": claim_gate_rows(),
        "decisions": decision_rows(),
        "next_target": next_target_rows(),
    }

    for key in [
        "source_register",
        "eh_baseline",
        "residual_pack",
        "seq_envelope",
        "residual_schema",
        "claim_gates",
        "decisions",
        "next_target",
    ]:
        write_csv(OUTPUTS[key], data[key])

    data["branch_copies"] = copy_outputs()
    write_csv(OUTPUTS["branch_copies"], data["branch_copies"])

    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)

    data["validation"] = validation_rows(data)
    write_csv(OUTPUTS["validation"], data["validation"])
    write_doc(data)


if __name__ == "__main__":
    main()
