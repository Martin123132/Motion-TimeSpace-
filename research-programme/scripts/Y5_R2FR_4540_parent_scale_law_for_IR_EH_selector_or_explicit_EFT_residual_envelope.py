from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SCRIPT_DIR = Path(__file__).resolve().parent
ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4540"
CLAIM_ID = "L-382"
BRANCH_ID = "MTS_R2FR_Y5_PARENT_SCALE_LAW_IR_EH_SELECTOR_OR_EFT_ENVELOPE_4540"
MARKER = "PPC4161_PARENT_SCALE_LAW_FOR_IR_EH_SELECTOR_OR_EXPLICIT_EFT_RESIDUAL_ENVELOPE_4540"
PACKET_MARKER = "PPC4161_PACKET_PARENT_SCALE_LAW_FOR_IR_EH_SELECTOR_OR_EXPLICIT_EFT_RESIDUAL_ENVELOPE_4540"
DECISION = "IR_EH_SELECTOR_THEOREM_CONDITIONAL_PARENT_SCALE_LAW_MISSING_EXPLICIT_EFT_RESIDUAL_ENVELOPE_ACTIVATED"
NEXT_TARGET = "4541-Y5-R2FR-same-coframe-kappa-memory-triple-zero-under-effective-local-branch-or-projection-bound.md"

FORMAL_PATH = FORMAL / "556-PPC4161-parent-scale-law-for-IR-EH-selector-or-explicit-EFT-residual-envelope.md"
DOC_PATH = POST / "4540-Y5-R2FR-parent-scale-law-for-IR-EH-selector-or-explicit-EFT-residual-envelope.md"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4540_SOURCE_REGISTER.csv"
NORMAL_FORM_CSV = SOURCE_DIR / "P8_Y5_R2FR_4540_IR_NORMAL_FORM_THEOREM.csv"
SCALE_LAW_AUDIT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4540_PARENT_SCALE_LAW_AUDIT.csv"
EFT_ENVELOPE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4540_EFT_RESIDUAL_ENVELOPE.csv"
ARENA_PROJECTION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4540_ARENA_PROJECTION_REQUIREMENTS.csv"
CLAIM_GATES_CSV = SOURCE_DIR / "P8_Y5_R2FR_4540_CLAIM_GATES.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4540_DECISION.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4540_NEXT_TARGET.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4540_STATUS.csv"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4540_VALIDATION.csv"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def b(value: bool) -> str:
    return "True" if value else "False"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def markdown_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "\n"
    headers: list[str] = []
    for row in rows:
        for key in row:
            if key not in headers:
                headers.append(key)
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(header, "")).replace("\n", "<br>") for header in headers) + " |")
    return "\n".join(lines) + "\n"


def source_rows() -> list[dict[str, Any]]:
    specs = [
        {
            "source_id": "SRC4540_00_4539_status",
            "label": "4539 status",
            "path": SOURCE_DIR / "P8_Y5_R2FR_4539_STATUS.csv",
            "needle": "primary_live_residual",
            "role": "4539 freezes effective local GR and selects E_EH_IR as primary residual",
        },
        {
            "source_id": "SRC4540_01_4539_handoff",
            "label": "4539 residual handoff",
            "path": SOURCE_DIR / "P8_Y5_R2FR_4539_RESIDUAL_HANDOFF_MATRIX.csv",
            "needle": "RH4539_0_EH_IR",
            "role": "EH/IR selector is next target",
        },
        {
            "source_id": "SRC4540_02_4184_status",
            "label": "4184 IR selector status",
            "path": SOURCE_DIR / "P8_Y5_R2FR_4184_STATUS.csv",
            "needle": "selector_assumptions_parent_derived",
            "role": "IR selector theorem is conditional and not parent-derived",
        },
        {
            "source_id": "SRC4540_03_4184_axioms",
            "label": "4184 selector axiom set",
            "path": SOURCE_DIR / "P8_Y5_R2FR_4184_IR_SELECTOR_AXIOM_SET.csv",
            "needle": "SEL4184_2_IR_order",
            "role": "IR order and no-extra-light-mode assumptions",
        },
        {
            "source_id": "SRC4540_04_4184_normal",
            "label": "4184 normal form classification",
            "path": SOURCE_DIR / "P8_Y5_R2FR_4184_NORMAL_FORM_CLASSIFICATION.csv",
            "needle": "NFC4184_0_EC_Palatini",
            "role": "EC/Palatini is selected only if selector clauses hold",
        },
        {
            "source_id": "SRC4540_05_4184_EFT",
            "label": "4184 EFT bound ledger",
            "path": SOURCE_DIR / "P8_Y5_R2FR_4184_RESIDUAL_EFT_BOUND_LEDGER.csv",
            "needle": "RB4184_1_cR2",
            "role": "EFT residual coefficient families after failed selector",
        },
        {
            "source_id": "SRC4540_06_4185_coefficients",
            "label": "4185 coefficient arena map",
            "path": SOURCE_DIR / "P8_Y5_R2FR_4185_RESIDUAL_COEFFICIENT_ARENA_MAP.csv",
            "needle": "RC4185_2_cGamma",
            "role": "coefficient-to-arena projection map",
        },
        {
            "source_id": "SRC4540_07_4185_scale_candidates",
            "label": "4185 parent zero/scale candidates",
            "path": SOURCE_DIR / "P8_Y5_R2FR_4185_PARENT_ZERO_SCALE_LAW_CANDIDATES.csv",
            "needle": "PSL4185_4_higher_derivative_scale",
            "role": "candidate parent zero/scale laws",
        },
        {
            "source_id": "SRC4540_08_4185_bounds",
            "label": "4185 bound interface matrix",
            "path": SOURCE_DIR / "P8_Y5_R2FR_4185_BOUND_INTERFACE_MATRIX.csv",
            "needle": "BI4185_0_PPN",
            "role": "arena interfaces for residual coefficient bounds",
        },
        {
            "source_id": "SRC4540_09_packet",
            "label": "packet 4539 freeze",
            "path": PACKET_PATH,
            "needle": "PPC4161_PACKET_PARENT_ADOPT_GR_PARITY_HQNP_SELECTOR_OR_FREEZE_EFFECTIVE_LOCAL_GR_BRANCH_4539",
            "role": "effective local GR branch freeze is installed",
        },
    ]
    rows: list[dict[str, Any]] = []
    for spec in specs:
        path = Path(spec["path"])
        exists = path.exists()
        text = read_text(path) if exists else ""
        needle = str(spec["needle"])
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "source_id": spec["source_id"],
                "label": spec["label"],
                "path": str(path),
                "exists": b(exists),
                "needle": needle,
                "needle_found": b(exists and needle in text),
                "role": spec["role"],
                "valid_for_claim": "False",
            }
        )
    return rows


def normal_form_rows() -> list[dict[str, Any]]:
    return [
        {
            "theorem_id": "NFT4540_0_derivative_expansion",
            "claim": "A parent-owned local covariant derivative expansion with a mass gap selects the lowest-derivative bulk invariants first.",
            "condition": "There exists Lambda_* such that L_test Lambda_* >> 1 and all operators with more than one curvature/two derivatives are suppressed by powers of (L_test Lambda_*)^-1.",
            "consequence": "curvature-square and higher-derivative terms become EFT residuals rather than principal local gravity",
            "current_status": "conditional_parent_scale_law_missing",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "NFT4540_1_EC_Palatini_selection",
            "claim": "Under locality, Lorentz/diffeomorphism covariance, parity-even classical sector, one observed coframe, and one-curvature IR order, the unsuppressed bulk gravity term is EC/Palatini plus vacuum term.",
            "condition": "A_MF variables e,omega are admitted; parity-odd terms are topological/bounded; no second metric/disformal owner; no extra light torsion/scalar/vector mode.",
            "consequence": "epsilon_ABCD e^A wedge e^B wedge R^CD[omega] gives EH after torsion/nonmetricity silence",
            "current_status": "conditional_true_selector_assumptions_not_parent_derived",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "NFT4540_2_current_failure",
            "claim": "The current corpus does not derive the parent scale/gap law needed to promote the IR selector.",
            "condition": "Need parent-owned Lambda_*, no-extra-light-mode theorem, same-coframe functor and local memory screening.",
            "consequence": "EH remains effective/local branch principal block, not a first-principles parent theorem",
            "current_status": "proved_from_current_audit",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def scale_law_audit_rows() -> list[dict[str, Any]]:
    return [
        {
            "scale_law_id": "SLA4540_0_IR_gap",
            "law_needed": "parent mass/length hierarchy Lambda_* with L_local Lambda_* >> 1",
            "would_zero_or_suppress": "c_R2, higher derivative curvature tails",
            "current_evidence": "4184/4185 require parent scale or R10/orbital bound",
            "verdict": "missing_parent_scale",
            "next_action": "derive Lambda_* from MTS primitives or retain c_R2/M_R envelope",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "scale_law_id": "SLA4540_1_no_light_modes",
            "law_needed": "no unscreened local torsion/scalar/vector/disformal modes",
            "would_zero_or_suppress": "c_T, c_D, preferred-frame and clock/WEP tails",
            "current_evidence": "4184 selector assumption; 4185 maps c_T/c_D to local arenas",
            "verdict": "missing_parent_mode_gap",
            "next_action": "prove same-coframe and torsion algebraic/heavy laws or bound them",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "scale_law_id": "SLA4540_2_same_coframe",
            "law_needed": "q-owned single observed coframe functor",
            "would_zero_or_suppress": "c_D",
            "current_evidence": "private selector exists; global parent adoption open",
            "verdict": "private_not_global",
            "next_action": "4541 triple-zero route begins with c_D",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "scale_law_id": "SLA4540_3_kappa_source",
            "law_needed": "topological kappa lock plus Hilbert source-measure descent",
            "would_zero_or_suppress": "delta_kappa",
            "current_evidence": "private branch closed; numeric G calibrated; global adoption open",
            "verdict": "private_not_global",
            "next_action": "4541 triple-zero route carries delta_kappa",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "scale_law_id": "SLA4540_4_memory_silence",
            "law_needed": "local support projector/screens Gamma_mem from compact local collar",
            "would_zero_or_suppress": "c_Gamma",
            "current_evidence": "4185 central MTS-specific open debt",
            "verdict": "open_core_MTS_risk",
            "next_action": "4541 triple-zero route carries c_Gamma",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "scale_law_id": "SLA4540_5_boundary_route",
            "law_needed": "boundary/topological pieces exact, fixed or Hamiltonian-routed",
            "would_zero_or_suppress": "c_bdy",
            "current_evidence": "private no-flux exists; global adoption open",
            "verdict": "open_global_boundary",
            "next_action": "retain boundary envelope until sector interface theorem",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def eft_envelope_rows() -> list[dict[str, Any]]:
    return [
        {
            "envelope_id": "EFT4540_0_master",
            "quantity": "E_IR_local(A)",
            "envelope": "|R_A| <= |J_A^D c_D| + |J_A^k delta_kappa| + |J_A^G c_Gamma| + |J_A^T c_T| + |J_A^R c_R2/M_R^2| + |J_A^B c_bdy|",
            "meaning": "until the scale law is derived, each local arena A receives explicit coefficient projections instead of a hidden closure assumption",
            "status": "ACTIVE_NONCLAIM_ENVELOPE",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "envelope_id": "EFT4540_1_cD",
            "quantity": "c_D",
            "envelope": "same-coframe failure; projects first to WEP, clocks, EM propagation and Poynting/Hilbert stress",
            "meaning": "zero if q-owned single coframe is parent-signed; otherwise needs source-backed bound",
            "status": "PRIORITY_1_ZERO_OR_BOUND",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "envelope_id": "EFT4540_2_deltaKappa",
            "quantity": "delta_kappa",
            "envelope": "coupling/source-measure drift; projects to Gdot/G, orbital GM consistency, clock/local-G and WEP",
            "meaning": "zero if topological kappa plus Hilbert source lock is parent-signed; otherwise measured-G/LLR/orbital envelope",
            "status": "PRIORITY_1_ZERO_OR_BOUND",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "envelope_id": "EFT4540_3_cGamma",
            "quantity": "c_Gamma",
            "envelope": "MTS-specific local memory hair; projects to PPN, clocks, R10 and local-G variation",
            "meaning": "zero/suppressed only with a parent local memory support law",
            "status": "PRIORITY_1_ZERO_OR_BOUND",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "envelope_id": "EFT4540_4_cT",
            "quantity": "c_T",
            "envelope": "torsion-square/torsion mode residual; projects to preferred-frame, spin/contact, R10",
            "meaning": "zero/heavy if EC torsion algebraic silence or torsion mass gap is parent-signed",
            "status": "SECONDARY_ZERO_OR_BOUND",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "envelope_id": "EFT4540_5_cR2",
            "quantity": "c_R2/M_R^2",
            "envelope": "curvature-square finite-range tail; projects to R10 Yukawa, orbital precession and cosmology consistency",
            "meaning": "suppressed by parent IR scale or bounded by R10/orbital data",
            "status": "SECONDARY_ZERO_OR_BOUND",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "envelope_id": "EFT4540_6_cBdy",
            "quantity": "c_bdy",
            "envelope": "unrouted boundary/edge charge; projects to source mass leakage, radiation reaction and clock/source drift",
            "meaning": "zero in bulk only if boundary is exact/fixed/topological/Hamiltonian-routed",
            "status": "SECONDARY_ZERO_OR_BOUND",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def arena_projection_rows() -> list[dict[str, Any]]:
    return [
        {
            "projection_id": "APR4540_0_PPN",
            "arena": "PPN_vector",
            "required_projection": "J_PPN = d(gamma,beta,alpha_i,xi,zeta_i,Gdot/G)/d(c_D,delta_kappa,c_Gamma,c_T,c_R2,c_bdy)",
            "current_status": "projection_coefficients_missing",
            "next_action": "derive zero law first for c_D, delta_kappa, c_Gamma",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "projection_id": "APR4540_1_WEP_clock_EM",
            "arena": "WEP_clock_EM",
            "required_projection": "J_WCE for c_D, delta_kappa and c_Gamma into eta, clock redshift, EM propagation and Poynting ownership",
            "current_status": "projection_coefficients_missing",
            "next_action": "same-coframe/source-memory triple-zero or bounds",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "projection_id": "APR4540_2_R10",
            "arena": "short_range_R10",
            "required_projection": "J_R10 for c_R2,c_T,c_Gamma into alpha(lambda), with real bound curve",
            "current_status": "defer_until_projection_and_curve",
            "next_action": "do not score R10 from placeholders",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "projection_id": "APR4540_3_orbital",
            "arena": "orbital_ephemeris",
            "required_projection": "J_orb for delta_kappa,c_R2,c_bdy,c_Gamma into perihelion, inverse-square and Gdot envelopes",
            "current_status": "projection_coefficients_missing",
            "next_action": "analytic envelope before raw ephemeris",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "claim_gate_id": "CG4540_0_conditional_IR_theorem",
            "gate": "IR normal-form theorem",
            "status": "PASS_CONDITIONAL",
            "meaning": "EH/Palatini follows if parent scale/gap/no-light-mode conditions hold",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "claim_gate_id": "CG4540_1_parent_scale_law",
            "gate": "current parent scale law",
            "status": "FAIL_MISSING_PARENT_DERIVATION",
            "meaning": "no parent-owned Lambda_* or no-extra-light-mode theorem exists yet",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "claim_gate_id": "CG4540_2_EFT_envelope",
            "gate": "explicit EFT residual envelope",
            "status": "ACTIVE",
            "meaning": "extra invariants are now kept as named coefficient projections rather than hidden closures",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "claim_gate_id": "CG4540_3_public_GR_derivation",
            "gate": "public GR derivation",
            "status": "BLOCKED_NONCLAIM",
            "meaning": "effective local branch remains useful but parent EH origin is not proved",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC4540_0",
            "decision": DECISION,
            "meaning": "4540 derives the correct IR normal-form fork: with a parent scale/gap law, EH/Palatini is selected; without it, every extra invariant must be carried as an explicit EFT residual envelope. Current evidence chooses the envelope branch.",
            "next_action": NEXT_TARGET,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def next_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NT4540_0",
            "target": NEXT_TARGET,
            "objective": "try to zero the priority triple c_D, delta_kappa and c_Gamma before scoring finite-range tails",
            "derive_first": "same-coframe functor, kappa/source lock and local memory support projector",
            "fallback": "if any coefficient remains finite, write projection-bound rows into WEP/clock/PPN/orbital arenas before R10",
            "avoid": "jumping to R10 alpha(lambda) before projection coefficients exist",
            "valid_for_claim": "False",
        }
    ]


def status_rows() -> list[dict[str, Any]]:
    return [
        {
            "timestamp_utc": utc_now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT,
            "result": DECISION,
            "conditional_IR_EH_selector_theorem_written": "True",
            "parent_scale_law_derived": "False",
            "EFT_residual_envelope_active": "True",
            "public_local_GR_claim_allowed": "False",
            "numeric_G_predicted": "False",
            "priority_coefficients": "c_D;delta_kappa;c_Gamma",
            "next_target": NEXT_TARGET,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def validate(
    sources: list[dict[str, Any]],
    normal_form: list[dict[str, Any]],
    scale_laws: list[dict[str, Any]],
    envelope: list[dict[str, Any]],
    projections: list[dict[str, Any]],
    gates: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    checks: list[dict[str, Any]] = []
    source_ok = all(row["exists"] == "True" and row["needle_found"] == "True" for row in sources)
    checks.append({"validation_id": "VAL4540_00_sources", "status": "PASS" if source_ok else "FAIL", "detail": "all source paths exist and needles found" if source_ok else "source path or needle missing"})

    theorem_ok = any(row["theorem_id"] == "NFT4540_1_EC_Palatini_selection" for row in normal_form) and any(row["theorem_id"] == "NFT4540_2_current_failure" for row in normal_form)
    checks.append({"validation_id": "VAL4540_01_normal_form", "status": "PASS" if theorem_ok else "FAIL", "detail": "conditional EC/Palatini selector and current failure are explicit"})

    scale_fail_ok = any(row["scale_law_id"] == "SLA4540_0_IR_gap" and row["verdict"] == "missing_parent_scale" for row in scale_laws)
    checks.append({"validation_id": "VAL4540_02_scale_law_audit", "status": "PASS" if scale_fail_ok else "FAIL", "detail": "parent scale law remains missing rather than silently assumed"})

    envelope_ids = {row["envelope_id"] for row in envelope}
    envelope_ok = all(eid in envelope_ids for eid in ["EFT4540_1_cD", "EFT4540_2_deltaKappa", "EFT4540_3_cGamma", "EFT4540_4_cT", "EFT4540_5_cR2", "EFT4540_6_cBdy"])
    checks.append({"validation_id": "VAL4540_03_envelope", "status": "PASS" if envelope_ok else "FAIL", "detail": "all named EFT residual coefficients are in the active envelope"})

    projection_ok = len(projections) >= 4 and all(row["claim_allowed"] == "False" for row in projections)
    checks.append({"validation_id": "VAL4540_04_projection_requirements", "status": "PASS" if projection_ok else "FAIL", "detail": "arena projection requirements recorded as nonclaim"})

    gates_ok = all(row["claim_allowed"] == "False" and row["valid_for_claim"] == "False" for row in gates)
    parent_fail = any(row["claim_gate_id"] == "CG4540_1_parent_scale_law" and row["status"] == "FAIL_MISSING_PARENT_DERIVATION" for row in gates)
    checks.append({"validation_id": "VAL4540_05_claim_firewall", "status": "PASS" if gates_ok and parent_fail else "FAIL", "detail": "parent scale law fails and all gates remain nonclaim"})

    csv_paths = [SOURCE_REGISTER, NORMAL_FORM_CSV, SCALE_LAW_AUDIT_CSV, EFT_ENVELOPE_CSV, ARENA_PROJECTION_CSV, CLAIM_GATES_CSV, DECISION_CSV, NEXT_CSV, STATUS_CSV]
    csv_ok = True
    details: list[str] = []
    for path in csv_paths:
        try:
            if not read_csv(path):
                csv_ok = False
                details.append(f"{path.name}:empty")
        except Exception as exc:
            csv_ok = False
            details.append(f"{path.name}:{exc}")
    checks.append({"validation_id": "VAL4540_06_csv_parse", "status": "PASS" if csv_ok else "FAIL", "detail": "all generated CSV files parse and have rows" if csv_ok else ";".join(details)})

    pycache_absent = not (SCRIPT_DIR / "__pycache__").exists()
    checks.append({"validation_id": "VAL4540_07_pycache_absent", "status": "PASS" if pycache_absent else "FAIL", "detail": "scripts __pycache__ absent after cleanup" if pycache_absent else "scripts __pycache__ still present"})

    overall = all(row["status"] == "PASS" for row in checks)
    checks.append({"validation_id": "VAL4540_OVERALL", "status": "PASS" if overall else "FAIL", "detail": "4540 parent scale-law fork and EFT residual envelope"})
    return checks


def build_doc(
    sources: list[dict[str, Any]],
    normal_form: list[dict[str, Any]],
    scale_laws: list[dict[str, Any]],
    envelope: list[dict[str, Any]],
    projections: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
    status: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> str:
    return f"""# 4540 - parent scale law for IR EH selector or explicit EFT residual envelope

Generated: `{utc_now()}`  
Marker: `{MARKER}`  
Decision: `{DECISION}`  
Claim: `{CLAIM_ID}` remains private, conditional and nonclaim.

## What Moved

4539 froze `PPC4161-GP-HQNP` as an effective local-GR branch because the parent action has not yet signed the EH/IR selector. 4540 attacks that root.

The clean theorem is:

```text
local covariant parent action
+ parent scale/gap hierarchy
+ no extra light local modes
+ same coframe and q-natural descent
=> EC/Palatini is the unique unsuppressed parity-even linear-curvature local bulk term
=> EH local metric block after torsion/nonmetricity silence.
```

That theorem is useful but conditional. Current MTS evidence does not yet derive the needed scale/gap law. Therefore the honest branch is not “EH is fully derived”; it is:

```text
E_IR_local(A)
 <= |J_A^D c_D|
  + |J_A^k delta_kappa|
  + |J_A^G c_Gamma|
  + |J_A^T c_T|
  + |J_A^R c_R2/M_R^2|
  + |J_A^B c_bdy|.
```

This is a move forward: every non-EH local invariant now has a named coefficient, arena projection requirement and zero-or-bound route. The priority next attack is the root triple `c_D`, `delta_kappa`, `c_Gamma`; R10 finite-range scoring waits until projection coefficients exist.

## IR Normal Form Theorem

{markdown_table(normal_form)}

## Parent Scale-Law Audit

{markdown_table(scale_laws)}

## EFT Residual Envelope

{markdown_table(envelope)}

## Arena Projection Requirements

{markdown_table(projections)}

## Claim Gates

{markdown_table(gates)}

## Decision

{markdown_table(decisions)}

## Next Target

{markdown_table(next_target)}

## Status

{markdown_table(status)}

## Source Register

{markdown_table(sources)}

## Validation

{markdown_table(validation)}
"""


def append_once(path: Path, marker: str, text: str) -> None:
    existing = read_text(path) if path.exists() else ""
    if marker in existing:
        return
    with path.open("a", encoding="utf-8", newline="") as handle:
        if existing and not existing.endswith("\n"):
            handle.write("\n")
        handle.write(text.strip() + "\n")


def append_claim_once() -> None:
    existing = read_text(CLAIMS_PATH) if CLAIMS_PATH.exists() else ""
    if f"{CLAIM_ID}," in existing:
        return
    row = {
        "claim_id": CLAIM_ID,
        "domain": "local_gr_ir_selector",
        "claim": "4540 derives the conditional IR normal-form theorem that would select EC/Palatini/EH from a parent scale/gap law, but current MTS evidence lacks that law; all extra local invariants are therefore kept in an explicit EFT residual envelope.",
        "current_evidence": "Generated source register, IR normal-form theorem, parent scale-law audit, EFT residual envelope, arena projection requirements, claim gates, status and validation CSVs.",
        "status": "conditional_IR_EH_selector_parent_scale_law_missing_EFT_envelope_active_nonclaim",
        "next_test": NEXT_TARGET,
        "key_risk": "Assuming a parent IR scale/gap or no-extra-light-mode theorem that has not been derived.",
        "sector": "local_gr",
        "evidence": str(DOC_PATH),
        "next_action": NEXT_TARGET,
        "risk": "c_D, delta_kappa and c_Gamma remain priority local risks; c_T/c_R2/c_bdy remain secondary EFT envelopes.",
    }
    file_exists = CLAIMS_PATH.exists() and CLAIMS_PATH.stat().st_size > 0
    with CLAIMS_PATH.open("a", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(row.keys()))
        if not file_exists:
            writer.writeheader()
        writer.writerow(row)


def main() -> None:
    sources = source_rows()
    normal_form = normal_form_rows()
    scale_laws = scale_law_audit_rows()
    envelope = eft_envelope_rows()
    projections = arena_projection_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_target = next_rows()
    status = status_rows()

    write_csv(SOURCE_REGISTER, sources)
    write_csv(NORMAL_FORM_CSV, normal_form)
    write_csv(SCALE_LAW_AUDIT_CSV, scale_laws)
    write_csv(EFT_ENVELOPE_CSV, envelope)
    write_csv(ARENA_PROJECTION_CSV, projections)
    write_csv(CLAIM_GATES_CSV, gates)
    write_csv(DECISION_CSV, decisions)
    write_csv(NEXT_CSV, next_target)
    write_csv(STATUS_CSV, status)

    shutil.rmtree(SCRIPT_DIR / "__pycache__", ignore_errors=True)
    validation = validate(sources, normal_form, scale_laws, envelope, projections, gates)
    write_csv(VALIDATION_PATH, validation)

    body = build_doc(sources, normal_form, scale_laws, envelope, projections, gates, decisions, next_target, status, validation)
    FORMAL_PATH.write_text(body, encoding="utf-8")
    DOC_PATH.write_text(body, encoding="utf-8")

    append_claim_once()
    append_once(
        SPINE_PATH,
        MARKER,
        f"""
## 4540 Parent Scale Law For IR EH Selector Or Explicit EFT Residual Envelope

Marker: `{MARKER}`  
4540 derives the correct IR fork. If the parent action supplies a scale/gap hierarchy, no extra light modes, same coframe and q-natural descent, EC/Palatini is the selected local principal block and gives EH after torsion/nonmetricity silence. Current evidence does not derive that parent scale law, so the effective local-GR branch remains nonclaim and all extra invariants are carried in an explicit EFT residual envelope with priority coefficients `c_D`, `delta_kappa`, and `c_Gamma`. Next target: `{NEXT_TARGET}`.
""",
    )
    append_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""
## 4540 Packet Integration - IR EH Selector Fork

Marker: `{PACKET_MARKER}`  
The packet now treats EH/Palatini selection as conditional on a parent scale/gap law. Because that law is not derived, the local branch carries an active EFT residual envelope instead of hiding extra invariants. Priority zero-or-bound coefficients are `c_D`, `delta_kappa`, and `c_Gamma`.
""",
    )

    shutil.rmtree(SCRIPT_DIR / "__pycache__", ignore_errors=True)
    print(f"wrote {FORMAL_PATH}")
    print(f"wrote {DOC_PATH}")
    print(f"wrote {VALIDATION_PATH}")
    print(f"decision {DECISION}")


if __name__ == "__main__":
    main()
