from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


BRANCH_ID = "MTS_R2FR_JQ_SOURCE_CURRENT_EXTRACTION_OR_HTAU_CERTIFICATE_2445"
CHECKPOINT_ID = "2445"

ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = ROOT.parent
FORMALIZATION = PROJECT_ROOT / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
HAMILTONIAN = ROOT / "source-intake" / "hamiltonian-source"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"

DOC = ROOT / "2445-Y5-R2FR-Jq-source-current-extraction-from-parent-L-or-Htau-source-charge-certificate.md"

OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_2445_SOURCE_REGISTER.csv",
    "jq_extraction": OUT / "P8_Y5_PARENT_QLOC_2445_JQ_SOURCE_CURRENT_EXTRACTION_ATTEMPT.csv",
    "htau_certificate": OUT / "P8_Y5_PARENT_QLOC_2445_HTAU_SOURCE_CHARGE_CERTIFICATE_AUDIT.csv",
    "certificate_schema": OUT / "P8_Y5_PARENT_QLOC_2445_SOURCE_CURRENT_CERTIFICATE_SCHEMA.csv",
    "seq_status": OUT / "P8_Y5_PARENT_QLOC_2445_S_EQ_STATUS_UPDATE.csv",
    "claim_gates": OUT / "P8_Y5_PARENT_QLOC_2445_CLAIM_GATES.csv",
    "decisions": OUT / "P8_Y5_PARENT_QLOC_2445_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_2445_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_PARENT_QLOC_2445_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2445_VALIDATION.csv",
}

COPY_TARGETS = {
    "queue_jq_extraction": QUEUE / "JR2445_JQ_SOURCE_CURRENT_EXTRACTION_ATTEMPT_NONCLAIM.csv",
    "queue_certificate_schema": QUEUE / "JR2445_SOURCE_CURRENT_CERTIFICATE_SCHEMA_NONCLAIM.csv",
    "hamiltonian_certificate": HAMILTONIAN / "Jq_or_Htau_source_charge_certificate_2445_NONCLAIM.csv",
    "local_seq_status": LOCAL_BOUNDS / "S_Eq_status_update_2445_NONCLAIM.csv",
}

SOURCES = [
    {
        "source_id": "SRC2445_00_2444_doc",
        "source_path": ROOT / "2444-Y5-R2FR-source-leg-S-Eq-owner-from-parent-current-or-local-product-closure.md",
        "needles": ["NEXT2444_0_selected", "SLC2444_0_definition", "PCA2444_6_verdict", "VAL2444_OVERALL"],
        "role": "fresh handoff selecting J_q or H_tau certificate",
    },
    {
        "source_id": "SRC2445_01_2444_contract_csv",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_2444_SOURCE_LEG_DERIVATION_CONTRACT.csv",
        "needles": ["SLC2444_0_definition", "SLC2444_4_verdict", "EXACT_CONTRACT_INPUTS_MISSING"],
        "role": "machine-readable S_E^q source-leg contract",
    },
    {
        "source_id": "SRC2445_02_992_doc",
        "source_path": ROOT / "992-Y5-R10-Hamiltonian-PiM-source-current-descent-or-FB5540-component-bound-pack.md",
        "needles": ["SCD992_0_parent_action_current", "BPK992_0_current_extraction", "DEC992_2_next_target"],
        "role": "older Hamiltonian source-current descent attempt",
    },
    {
        "source_id": "SRC2445_03_993_doc",
        "source_path": ROOT / "993-Y5-R10-parent-Lagrangian-current-extraction-theta-Qtau-or-deltaH-curl-input.md",
        "needles": ["CEG993_4_verdict", "SEC993_0_EH_core", "DEC993_0_extraction_attempt"],
        "role": "older parent Lagrangian current extraction attempt",
    },
    {
        "source_id": "SRC2445_04_992_theorem_csv",
        "source_path": OUT / "P8_Y5_R10_992_SOURCE_CURRENT_DESCENT_THEOREM_GATE.csv",
        "needles": ["SCD992_0_parent_action_current", "blocked_by_991_HPT991_0", "SCD992_6_verdict"],
        "role": "machine-readable source-current descent gate",
    },
    {
        "source_id": "SRC2445_05_993_current_gate_csv",
        "source_path": OUT / "P8_Y5_R10_993_CURRENT_EXTRACTION_GATE.csv",
        "needles": ["CEG993_0_action_inventory", "CEG993_4_verdict", "not_promoted"],
        "role": "machine-readable current extraction gate",
    },
    {
        "source_id": "SRC2445_06_993_sector_ledger_csv",
        "source_path": OUT / "P8_Y5_R10_993_SECTOR_CURRENT_EXTRACTION_LEDGER.csv",
        "needles": ["SEC993_0_EH_core", "SEC993_2_universal_matter", "SEC993_7_EM_charge_coupling"],
        "role": "sector-by-sector current extraction status",
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


def jq_extraction_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "attempt_id": "JQX2445_0_target",
            "candidate_object": "J_q^A",
            "candidate_formula": "J_q^A := delta S_matter,A / delta q, evaluated before readout/projector reduction and then projected into the shared local arena",
            "current_result": "TARGET_DEFINED_NOT_EXTRACTED",
            "why": "explicit q-dependence of S_matter,A is not supplied by a parent Lagrangian term",
            "exit_requirement": "sector-by-sector parent L terms with q dependence and source paths",
        },
        {
            "attempt_id": "JQX2445_1_EH_baseline",
            "candidate_object": "theta_EH and Q_tau^EH",
            "candidate_formula": "standard EH covariant phase-space current and Noether charge",
            "current_result": "REFERENCE_ONLY",
            "why": "EH baseline gives GR charge shape, not the MTS q-source current or extra-sector silence",
            "exit_requirement": "do not promote EH current into total MTS Q_tau",
        },
        {
            "attempt_id": "JQX2445_2_universal_matter",
            "candidate_object": "Hilbert source current J_H",
            "candidate_formula": "T_H^{mu nu}=2/sqrt(-g_obs) delta S_matter/delta g_obs_mu_nu; J_H[tau]=T_H^{mu nu} tau_nu dSigma_mu",
            "current_result": "CONDITIONAL_STANDARD_IDENTITY_ONLY",
            "why": "Hilbert current is not automatically the q-source current and still needs matter functor/source readout ownership",
            "exit_requirement": "derive map from J_H to J_q or prove q-blind matter action",
        },
        {
            "attempt_id": "JQX2445_3_qblind_zero_route",
            "candidate_object": "J_q^A=0",
            "candidate_formula": "if S_matter,A=Sbar_matter[q-independent representation data,g_obs] and no q-source/readout term exists, then delta S_matter,A/delta q=0",
            "current_result": "EXACT_CONDITIONAL_NOT_SIGNED",
            "why": "source-scalar exclusion and matter-spectrum owner are conditional, not parent-derived",
            "exit_requirement": "parent object-language rule proving no q-dependent source/current slots",
        },
        {
            "attempt_id": "JQX2445_4_visible_coefficient_route",
            "candidate_object": "J_q^A from visible coefficient drift",
            "candidate_formula": "J_q^A contains (partial theta_i/partial q) O_i,A for alpha/mass/binding/source-weight operators",
            "current_result": "RETAINED_RESIDUAL_ROUTE",
            "why": "b_alpha, b_mhat, b_nuc and source-weight rows remain live unless theorem-zero closes them",
            "exit_requirement": "explicit coefficient slopes and operators, or theorem-zero owner",
        },
        {
            "attempt_id": "JQX2445_5_verdict",
            "candidate_object": "J_q^A source current",
            "candidate_formula": "J_q^A is not extractable from the current corpus beyond a contract and EH comparator",
            "current_result": "NOT_EXTRACTED_CERTIFICATE_REQUIRED",
            "why": "full parent Lagrangian sector currents are not available",
            "exit_requirement": "build certificate schema and residual-current pack",
        },
    ]
    return [base_row(**row) for row in rows]


def htau_certificate_rows() -> list[dict[str, Any]]:
    rows = [
        ("HTC2445_0_Htau_owner", "H_tau source charge exists", "delta H_tau=int_S(delta Q_tau-i_tau theta_total)", "BLOCKED", "theta_total and Q_tau^MTS not extracted", False),
        ("HTC2445_1_integrability", "H_tau is integrable", "delta^2 H_tau=0 on allowed solution space", "BLOCKED", "deltaH curl not evaluable", False),
        ("HTC2445_2_reference_lock", "B_ref is fixed before readout", "H_tau=surface charge-B_ref with parent-owned boundary/reference class", "BLOCKED", "reference can absorb source normalization", False),
        ("HTC2445_3_tau_lock", "same tau_obs is used across source, orbit, clock, PPN and R10", "one observed generator and denominator convention", "BLOCKED", "tau/frame denominator certificate missing", False),
        ("HTC2445_4_source_equality", "H_tau equals observed/source current before orbital GM", "M_H_tau=M_eff[Pi_M J_H]+zero_or_bounded_residuals", "BLOCKED", "charge-current residual vector unbounded", False),
        ("HTC2445_5_S_Eq_derivative", "S_E^q=partial ln H_tau/partial q", "valid after HTC2445_0 through HTC2445_4", "BLOCKED", "H_tau certificate missing", False),
        ("HTC2445_6_verdict", "H_tau certificate isolates S_E^q", "all Hamiltonian source-charge clauses pass", "NOT_CERTIFIED", "local source leg remains product-only", False),
    ]
    return [
        base_row(
            certificate_id=certificate_id,
            clause=clause,
            required_form=required_form,
            current_status=status,
            blocker=blocker,
            gate_pass=gate_pass,
        )
        for certificate_id, clause, required_form, status, blocker, gate_pass in rows
    ]


def certificate_schema_rows() -> list[dict[str, Any]]:
    rows = [
        ("SCS2445_0_parent_L_term", "sector; L_parent_term; q_dependence; source_path", "required for J_q extraction", "MISSING", False),
        ("SCS2445_1_current_term", "sector; J_q_term; theta_term; Q_tau_term; constraint_term", "required to compute source current or Hamiltonian charge", "MISSING", False),
        ("SCS2445_2_projection_term", "arena; source_worldtube; kernel_Gq; P_arena; q_normalization; units", "required to convert J_q into S_E^q", "MISSING", False),
        ("SCS2445_3_zero_theorem", "theorem_id; qblind_clause; no_source_scalar_clause; readout_closure; proof_source", "required to set J_q=0 or S_E^q=0", "MISSING", False),
        ("SCS2445_4_product_row", "arena; retained_product; value_or_bound; units; source_path; zero_premises; valid_for_claim", "fallback if current extraction fails", "SCHEMA_READY_NONCLAIM", False),
        ("SCS2445_5_promotion_gate", "all fields numeric or theorem-zero; no MISSING markers; no unity shortcut; no orbital-GM substitution", "required for any future claim", "ACTIVE_GUARD", False),
    ]
    return [
        base_row(
            schema_id=schema_id,
            required_columns=columns,
            purpose=purpose,
            current_status=status,
            ready_for_claim=ready,
        )
        for schema_id, columns, purpose, status, ready in rows
    ]


def seq_status_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "status_id": "SEQ2445_0_definition",
            "source_leg": "S_E^q",
            "current_status": "DEFINED_BY_2444_CONTRACT",
            "allowed_use": "symbolic product-closure factor",
            "forbidden_use": "standalone numeric source charge or unity value",
            "next_requirement": "J_q extraction or H_tau certificate",
        },
        {
            "status_id": "SEQ2445_1_WEP",
            "source_leg": "S_E^q*b_mhat; S_E^q*b_alpha; S_E^q*b_nuc",
            "current_status": "PRODUCT_ONLY",
            "allowed_use": "nonclaim smoke/envelope rows",
            "forbidden_use": "isolated b_i bounds",
            "next_requirement": "source current plus material/nuclear response matrix",
        },
        {
            "status_id": "SEQ2445_2_R10",
            "source_leg": "G_q(lambda) J_q^source J_q^test",
            "current_status": "SCHEMA_ONLY",
            "allowed_use": "source/test current placeholder with claim false",
            "forbidden_use": "Yukawa alpha(lambda) prediction",
            "next_requirement": "kernel, source/test qbar, real bound curve",
        },
        {
            "status_id": "SEQ2445_3_GR_Newton",
            "source_leg": "partial ln H_tau/partial q",
            "current_status": "HAMILTONIAN_CERTIFICATE_MISSING",
            "allowed_use": "bridge target to source mass",
            "forbidden_use": "orbital GM substitution",
            "next_requirement": "theta/Q_tau extraction and source equality",
        },
        {
            "status_id": "SEQ2445_4_verdict",
            "source_leg": "shared local source leg",
            "current_status": "NOT_OWNED",
            "allowed_use": "product closure only",
            "forbidden_use": "local-GR/WEP/R10/PPN claim",
            "next_requirement": "sector residual-current pack",
        },
    ]
    return [base_row(**row, valid_for_claim=False, score_ready=False) for row in rows]


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("CG2445_0_Jq_contract", "J_q extraction target is precisely specified", "PASS_NONCLAIM", "formula and certificate schema are written", True),
        ("CG2445_1_Jq_extracted", "J_q is extracted from parent L", "BLOCKED", "no sector-by-sector parent L current extraction", False),
        ("CG2445_2_Htau_certificate", "H_tau source charge certifies S_E^q", "BLOCKED", "integrability/reference/tau/source equality remain open", False),
        ("CG2445_3_S_Eq_numeric", "S_E^q is numeric or theorem-zero", "BLOCKED", "source leg remains product-only", False),
        ("CG2445_4_local_tests", "WEP/R10/clock/PPN tests are score-ready", "BLOCKED", "source current and projection are missing", False),
        ("CG2445_5_GR_Newton", "GR/Newton source reduction is derived", "BLOCKED", "Hamiltonian source charge and weak-field readout are downstream", False),
    ]
    return [
        base_row(claim_id=claim_id, claim=claim, gate_status=status, reason=reason, gate_pass=gate_pass)
        for claim_id, claim, status, reason, gate_pass in rows
    ]


def decision_rows() -> list[dict[str, Any]]:
    rows = [
        ("DEC2445_0_Jq", "DO_NOT_PROMOTE_JQ_EXTRACTION", "existing 992/993 evidence only supplies EH comparator and contracts, not full MTS source current", "S_E^q stays product-only"),
        ("DEC2445_1_Htau", "DO_NOT_PROMOTE_HTAU_CERTIFICATE", "Hamiltonian charge integrability/reference/tau/source equality remain unsigned", "no Newton source claim"),
        ("DEC2445_2_schema", "CERTIFICATE_SCHEMA_ACCEPTED", "future source claims now have exact required columns and promotion gate", "use schema for any future current rows"),
        ("DEC2445_3_next", "BUILD_SECTOR_RESIDUAL_CURRENT_PACK_NEXT", "the concrete way forward is to split EH baseline from all missing MTS residual current pieces", "select 2446"),
        ("DEC2445_4_public", "NO_GITHUB_ACTION", "private nonclaim derivation checkpoint", "continue privately"),
    ]
    return [
        base_row(decision_id=decision_id, decision=decision, rationale=rationale, consequence=consequence)
        for decision_id, decision, rationale, consequence in rows
    ]


def next_target_rows() -> list[dict[str, Any]]:
    row = {
        "route_id": "NEXT2445_0_selected",
        "selection_status": "selected",
        "target_file": "2446-Y5-R2FR-EH-baseline-plus-MTS-residual-current-pack-for-S-Eq.md",
        "target_script": "scripts/Y5_R2FR_EH_baseline_plus_MTS_residual_current_pack_for_S_Eq_2446.py",
        "task": "write the EH source-current baseline as comparator and build an MTS residual-current pack for extra/projector/boundary/readout/coupling pieces feeding S_E^q",
        "acceptance_target": "all non-EH current pieces are named residual rows with zero-theorem or source-bound requirements, and no local coefficient test is promoted",
        "guardrails": "do not import EH as proof of MTS; do not set residual currents to zero by taste; do not substitute orbital GM; do not claim WEP/R10/PPN/local GR; do not edit formalization-workbench; do not push GitHub",
    }
    return [base_row(**row)]


def copy_outputs() -> list[dict[str, Any]]:
    copy_specs = {
        "queue_jq_extraction": (OUTPUTS["jq_extraction"], COPY_TARGETS["queue_jq_extraction"], "J_q extraction attempt queue"),
        "queue_certificate_schema": (OUTPUTS["certificate_schema"], COPY_TARGETS["queue_certificate_schema"], "source-current certificate schema queue"),
        "hamiltonian_certificate": (OUTPUTS["htau_certificate"], COPY_TARGETS["hamiltonian_certificate"], "H_tau source charge certificate audit"),
        "local_seq_status": (OUTPUTS["seq_status"], COPY_TARGETS["local_seq_status"], "S_E^q local status update"),
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

    add("VAL2445_00_sources_exist", all(row["path_exists"] for row in data["source_register"]), "all cited source paths exist")
    add("VAL2445_01_source_needles", all(row["needles_found"] for row in data["source_register"]), "all cited source needles are present")
    add(
        "VAL2445_02_Jq_target_defined",
        any(row["attempt_id"] == "JQX2445_0_target" and "delta S_matter" in row["candidate_formula"] for row in data["jq_extraction"]),
        "J_q extraction target is defined",
    )
    add(
        "VAL2445_03_Jq_not_extracted",
        any(row["attempt_id"] == "JQX2445_5_verdict" and row["current_result"] == "NOT_EXTRACTED_CERTIFICATE_REQUIRED" for row in data["jq_extraction"]),
        "J_q extraction is not promoted",
    )
    add(
        "VAL2445_04_Htau_not_certified",
        any(row["certificate_id"] == "HTC2445_6_verdict" and row["current_status"] == "NOT_CERTIFIED" for row in data["htau_certificate"]),
        "H_tau source charge certificate is not promoted",
    )
    add(
        "VAL2445_05_schema_present",
        {"SCS2445_0_parent_L_term", "SCS2445_1_current_term", "SCS2445_2_projection_term", "SCS2445_5_promotion_gate"} <= {row["schema_id"] for row in data["certificate_schema"]},
        "certificate schema rows are present",
    )
    add(
        "VAL2445_06_SEq_product_only",
        any(row["status_id"] == "SEQ2445_4_verdict" and row["current_status"] == "NOT_OWNED" for row in data["seq_status"]),
        "S_E^q remains not owned and product-only",
    )
    add(
        "VAL2445_07_claim_gates_safe",
        all((row["claim_id"] == "CG2445_0_Jq_contract" and row["gate_status"] == "PASS_NONCLAIM") or row["gate_status"] == "BLOCKED" for row in data["claim_gates"]),
        "only the contract/schema passes as nonclaim; claims stay blocked",
    )
    add(
        "VAL2445_08_next_target_written",
        len(data["next_target"]) == 1 and data["next_target"][0]["route_id"] == "NEXT2445_0_selected",
        "2446 residual-current pack target selected",
    )
    add(
        "VAL2445_09_branch_copies",
        all(row["source_exists"] and row["target_exists"] for row in data["branch_copies"]),
        "branch copies exist",
    )
    formalization_hits: list[Path] = []
    if FORMALIZATION.exists():
        for path in FORMALIZATION.rglob("*"):
            name = path.name
            if any(marker in name for marker in ("2445-", "_2445", "2445_", "P8_Y5_PARENT_QLOC_2445", "P8_Y5_BRR545_2445")):
                formalization_hits.append(path)
    add(
        "VAL2445_10_no_formalization_artifacts",
        len(formalization_hits) == 0,
        "no 2445 artifacts were written to formalization-workbench",
        "; ".join(str(path) for path in formalization_hits),
    )

    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        ok, count, detail = csv_parses(path)
        add(f"VAL2445_CSV_{path.stem}", ok, f"CSV parses with {count} rows", detail)

    overall = all(row["status"] == "PASS" for row in rows)
    add(
        "VAL2445_OVERALL",
        overall,
        "2445 attempts J_q/H_tau extraction, does not promote it, creates a source-current certificate schema, and selects residual-current packing next",
    )
    return rows


def write_doc(data: dict[str, list[dict[str, Any]]]) -> None:
    content = f"""# 2445 - Y5/R2FR Jq Source Current Extraction From Parent L Or Htau Source Charge Certificate

## Result
- 2445 tries to extract the source current behind `S_E^q`.
- The target is now exact: `J_q^A := delta S_matter,A / delta q`, evaluated before readout/projector reduction.
- The extraction does not promote. Existing 992/993 evidence gives an EH comparator and source-current contract, but not a full MTS parent current.
- The Hamiltonian variant also does not promote: `S_E^q = partial ln H_tau[E]/partial q` needs integrability, fixed reference, tau lock, and source equality first.
- Output is therefore a certificate schema and a hard rule: `S_E^q` remains product-only until a real `J_q` or `H_tau` certificate exists.

## Source Register
{table(["source_id", "source_path", "path_exists", "needles_found", "role"], data["source_register"])}

## Jq Source Current Extraction Attempt
{table(["attempt_id", "candidate_object", "candidate_formula", "current_result", "why", "exit_requirement", "valid_for_claim"], data["jq_extraction"])}

## Htau Source Charge Certificate Audit
{table(["certificate_id", "clause", "required_form", "current_status", "blocker", "gate_pass", "valid_for_claim"], data["htau_certificate"])}

## Source Current Certificate Schema
{table(["schema_id", "required_columns", "purpose", "current_status", "ready_for_claim", "valid_for_claim"], data["certificate_schema"])}

## S_Eq Status Update
{table(["status_id", "source_leg", "current_status", "allowed_use", "forbidden_use", "next_requirement", "score_ready", "valid_for_claim"], data["seq_status"])}

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
        "jq_extraction": jq_extraction_rows(),
        "htau_certificate": htau_certificate_rows(),
        "certificate_schema": certificate_schema_rows(),
        "seq_status": seq_status_rows(),
        "claim_gates": claim_gate_rows(),
        "decisions": decision_rows(),
        "next_target": next_target_rows(),
    }

    for key in [
        "source_register",
        "jq_extraction",
        "htau_certificate",
        "certificate_schema",
        "seq_status",
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
