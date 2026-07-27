from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


BRANCH_ID = "MTS_R2FR_NOGAMMA_SLOT_MATTER_SOURCE_READOUT_AUDIT_2334"

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
FORMALIZATION = PROJECT / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
MICRO_RESIDUALS = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
BETA_DOCS = ROOT / "source-intake" / "beta-source" / "docs"

DOC = ROOT / "2334-Y5-R2FR-noGamma-slot-matter-source-readout-audit.md"

PATHS = {
    "2333_doc": ROOT / "2333-Y5-R2FR-noHypermomentum-LeviCivita-source-connection-or-P4-row.md",
    "2333_validation": OUT / "P8_Y5_BRR545_2333_VALIDATION.csv",
    "2333_next": OUT / "P8_Y5_PARENT_QLOC_2333_NEXT_TARGET.csv",
    "2333_proof": OUT / "P8_Y5_PARENT_QLOC_2333_NOHYPERMOMENTUM_LEVICIVITA_PROOF_AUDIT.csv",
    "2333_p4": OUT / "P8_Y5_PARENT_QLOC_2333_P4_HYPERMOMENTUM_RESIDUAL_ROW.csv",
    "2042_gamma_audit": OUT / "P8_Y5_PARENT_QLOC_2042_GAMMA_SLOT_AUDIT.csv",
    "2042_nohyper": OUT / "P8_Y5_PARENT_QLOC_2042_NO_HYPERMOMENTUM_THEOREM_ATTEMPT.csv",
    "2042_p4": OUT / "P8_Y5_PARENT_QLOC_2042_P4_CONNECTION_INTERFACE.csv",
    "1963_action": OUT / "P8_Y5_PARENT_QLOC_1963_MINIMAL_PARENT_ACTION_SIGNATURE.csv",
    "1963_no_gamma": OUT / "P8_Y5_PARENT_QLOC_1963_NO_GAMMA_THEOREM.csv",
    "2329_signature": OUT / "P8_Y5_PARENT_QLOC_2329_SOURCE_BLIND_FUNCTOR_SIGNATURE.csv",
    "2330_restriction": OUT / "P8_Y5_PARENT_QLOC_2330_PARENT_ACTION_RESTRICTION_DRAFT.csv",
    "2331_nonhilbert": OUT / "P8_Y5_PARENT_QLOC_2331_NONHILBERT_RESIDUAL_ROW.csv",
}

SOURCES = [
    ("SRC2334_00_2333_doc", "2333_doc", PATHS["2333_doc"], ["Next clean target", "independent `Gamma` slot"], "2333 handoff to no-Gamma slot audit"),
    ("SRC2334_01_2333_validation", "2333_validation", PATHS["2333_validation"], ["VAL2333_OVERALL", "PASS"], "2333 validation"),
    ("SRC2334_02_2333_next", "2333_next", PATHS["2333_next"], ["NEXT2333_0", "noGamma-slot"], "machine-readable 2334 target"),
    ("SRC2334_03_2333_proof", "2333_proof", PATHS["2333_proof"], ["NHL2333_6_verdict", "NOT_DERIVED_RETAIN_P4_ROW"], "no-hypermomentum not promoted"),
    ("SRC2334_04_2333_p4", "2333_p4", PATHS["2333_p4"], ["P4R2333_0_hypermomentum_total", "MISSING_DELTA_COMPONENT_VALUES"], "P4 fallback row"),
    ("SRC2334_05_2042_gamma_audit", "2042_gamma_audit", PATHS["2042_gamma_audit"], ["GSA2042_7_verdict", "FAIL_CURRENT_CORPUS"], "prior Gamma slot audit"),
    ("SRC2334_06_2042_nohyper", "2042_nohyper", PATHS["2042_nohyper"], ["NH2042_1_no_gamma_slot", "EXACT_CONDITIONAL_THEOREM"], "conditional no-hypermomentum theorem"),
    ("SRC2334_07_2042_p4", "2042_p4", PATHS["2042_p4"], ["P4C1960_5_hypermomentum", "MISSING_NO_GAMMA_MATTER_PROOF_OR_BOUND"], "P4 hypermomentum interface"),
    ("SRC2334_08_1963_action", "1963_action", PATHS["1963_action"], ["ACT1963_5_no_independent_Gamma_clause", "NO_GAMMA_BY_VARIABLE_SIGNATURE"], "candidate owned-coframe no-Gamma branch"),
    ("SRC2334_09_1963_no_gamma", "1963_no_gamma", PATHS["1963_no_gamma"], ["NGT1963_0_theorem", "CONDITIONAL_PROOF_VALID"], "no-Gamma theorem statement"),
    ("SRC2334_10_2329_signature", "2329_signature", PATHS["2329_signature"], ["SBF2329_1_source_blind_functor", "CORE_SIGNATURE_WRITTEN"], "source-blind matter functor"),
    ("SRC2334_11_2330_restriction", "2330_restriction", PATHS["2330_restriction"], ["PAR2330_3_no_hidden_return", "OPEN_PARALLEL_GATE"], "MUMC hidden-return caveat"),
    ("SRC2334_12_2331_nonhilbert", "2331_nonhilbert", PATHS["2331_nonhilbert"], ["NHR2331_1_spin_torsion", "NHR2331_3_readout_reentry"], "non-Hilbert residual leak paths"),
]

OUTPUTS = {
    "sources": OUT / "P8_Y5_PARENT_QLOC_2334_SOURCE_REGISTER.csv",
    "slots": OUT / "P8_Y5_PARENT_QLOC_2334_GAMMA_SLOT_SECTOR_AUDIT.csv",
    "theorem": OUT / "P8_Y5_PARENT_QLOC_2334_NO_GAMMA_THEOREM_STACK.csv",
    "p4_queue": OUT / "P8_Y5_PARENT_QLOC_2334_P4_DELTA_COMPONENT_QUEUE.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_2334_DECISION_LEDGER.csv",
    "claims": OUT / "P8_Y5_PARENT_QLOC_2334_CLAIM_GATES.csv",
    "refusal": OUT / "P8_Y5_PARENT_QLOC_2334_REFUSAL_RUNNER.csv",
    "next": OUT / "P8_Y5_PARENT_QLOC_2334_NEXT_TARGET.csv",
    "copies": OUT / "P8_Y5_PARENT_QLOC_2334_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2334_VALIDATION.csv",
}

BRANCH_COPY_SPECS = [
    ("COPY2334_0_slots", OUTPUTS["slots"], BETA_DOCS / "NOGAMMA_SLOT_SECTOR_AUDIT_2334_NONCLAIM.csv"),
    ("COPY2334_1_p4_queue", OUTPUTS["p4_queue"], MICRO_RESIDUALS / "P4_delta_component_queue_2334_nonclaim.csv"),
    ("COPY2334_2_decision", OUTPUTS["decision"], RAB_QUEUE / "JR2334_NOGAMMA_SLOT_DECISION_LEDGER_NONCLAIM.csv"),
]


def timestamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def bool_text(value: bool) -> str:
    return "true" if value else "false"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        fieldnames = []
        for row in rows:
            for key in row:
                if key not in fieldnames:
                    fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def relative_path(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    body = []
    for row in rows:
        values = []
        for column in columns:
            value = str(row.get(column, ""))
            value = value.replace("|", "\\|").replace("\n", " ")
            values.append(value)
        body.append("| " + " | ".join(values) + " |")
    return "\n".join([header, separator, *body])


def build_sources() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row_id, source_key, path, needles, role in SOURCES:
        exists = path.exists()
        text = read_text(path) if exists else ""
        missing = [needle for needle in needles if needle not in text]
        rows.append(
            {
                "timestamp_utc": timestamp(),
                "branch_id": BRANCH_ID,
                "row_id": row_id,
                "source_key": source_key,
                "source_path": str(path),
                "exists": bool_text(exists),
                "required": "true",
                "needles": ";".join(needles),
                "needles_found": bool_text(exists and not missing),
                "missing_needles": ";".join(missing),
                "source_role": role,
                "valid_for_claim": "false",
            }
        )
    return rows


def build_slot_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "NGSA2334_0_stack_target",
            "sector": "total ordinary local branch",
            "slot_question": "Does S_total_ord contain an independent affine Gamma_ind argument anywhere in matter, source, clock, light, orbit, boundary or readout?",
            "conditional_zero_clause": "If every sector factors through q to e_obs/g_obs, omega_LC[e_obs], owned gauge fields and constants, then Delta_total/delta Gamma_ind is zero by variable absence.",
            "evidence_status": "EXACT_CONDITIONAL_THEOREM_STACK",
            "open_gap": "sector-by-sector parent argument list is not signed for source/readout/boundary/projective slots",
            "p4_component": "Delta_abs",
            "claim_effect": "would kill independent-connection hypermomentum without fitting",
            "parent_signed": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "NGSA2334_1_ordinary_matter",
            "sector": "ordinary matter",
            "slot_question": "Does ordinary matter use S_A[Psi_A,e_obs,omega_LC[e_obs],A_owned,theta_A] with no Gamma_ind?",
            "conditional_zero_clause": "delta S_matter/delta Gamma_ind = 0 when Gamma_ind is absent from the action domain.",
            "evidence_status": "CONDITIONAL_SUPPORTED_BY_1963_AND_MUMC",
            "open_gap": "candidate signature exists but is not canonical parent action; direct Xi/q_loc/representative dependence still needs exclusion",
            "p4_component": "Delta_matter",
            "claim_effect": "ordinary matter hypermomentum would vanish inside the adopted owned-coframe branch",
            "parent_signed": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "NGSA2334_2_spinor_transport",
            "sector": "spinor and spin transport",
            "slot_question": "Is the spin connection omega_LC[e_obs] coframe-owned rather than an independent torsionful connection?",
            "conditional_zero_clause": "spin variation is absorbed into coframe/Hilbert variation when omega=omega_LC[e_obs]; an Einstein-Cartan branch instead creates Delta_spin.",
            "evidence_status": "CONDITIONAL_SPIN_GUARD_NOT_GLOBAL",
            "open_gap": "spin/torsion/nonmetricity alternatives are not parent-excluded for every ordinary sector",
            "p4_component": "Delta_spin",
            "claim_effect": "blocks axial torsion current only inside the coframe-owned branch",
            "parent_signed": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "NGSA2334_3_EM_light",
            "sector": "EM and lightcone readout",
            "slot_question": "Does light/EM use owned gauge connection and metric null structure, not affine Gamma_ind?",
            "conditional_zero_clause": "A_Q is not affine Gamma; null/light readout is Gamma-free if it is constructed from g_obs/LC[e_obs] only.",
            "evidence_status": "PARTIAL_GAUGE_OWNER_NOT_FULL_READOUT",
            "open_gap": "optical, Shapiro, ray and detector readout maps have not all been written as downstream Gamma-free functionals",
            "p4_component": "Delta_light",
            "claim_effect": "would prevent affine connection leakage into light/clock tests",
            "parent_signed": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "NGSA2334_4_source_worldtube",
            "sector": "source mass and finite worldtube",
            "slot_question": "Does source support/GM/worldtube action contain no Gamma_ind, boundary torsion or source-only connection current?",
            "conditional_zero_clause": "delta S_source/delta Gamma_ind = 0 only if source support is a descended Hilbert/coframe functional plus downstream calibration.",
            "evidence_status": "UNSIGNED_PRIMARY_LEAK_PATH",
            "open_gap": "finite-source boundary and measured-GM support map can still re-enter as non-Hilbert source current",
            "p4_component": "Delta_source",
            "claim_effect": "would close the source side of Newton/GR matching",
            "parent_signed": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "NGSA2334_5_clock_readout",
            "sector": "clock and frequency readout",
            "slot_question": "Are clocks downstream matter/gauge functionals of e_obs/g_obs and theta, not independent Gamma probes?",
            "conditional_zero_clause": "delta S_clock/delta Gamma_ind = 0 when clock modeling is downstream of the same Gamma-free ordinary action.",
            "evidence_status": "UNSIGNED_READOUT_SLOT",
            "open_gap": "atomic clock, frequency transfer, synchronization and detector model argument lists are not parent-signed",
            "p4_component": "Delta_clock",
            "claim_effect": "would protect clock/redshift tests from connection residuals",
            "parent_signed": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "NGSA2334_6_orbital_readout",
            "sector": "test-body and orbital readout",
            "slot_question": "Is orbital motion derived from the same LC/coframe action rather than an independent autoparallel Gamma_ind law?",
            "conditional_zero_clause": "delta S_orbit/delta Gamma_ind = 0 if orbit readout is a downstream projection of Hilbert matter in g_obs.",
            "evidence_status": "UNSIGNED_READOUT_SLOT",
            "open_gap": "geodesic/autoparallel choice and finite-body marker map remain explicit parent clauses to sign",
            "p4_component": "Delta_orbit",
            "claim_effect": "would support Newtonian/test-body reduction without importing GR geodesics by hand",
            "parent_signed": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "NGSA2334_7_boundary_domain",
            "sector": "boundary/domain/improvement terms",
            "slot_question": "Are boundary, domain and improvement terms either exact/projected silent or Gamma-free?",
            "conditional_zero_clause": "no boundary contribution to Delta_abs if compact support and improvement currents vanish under the source projector.",
            "evidence_status": "UNSIGNED_PARALLEL_GATE",
            "open_gap": "worldtube flux, marker boundaries and improvement currents still need zero theorem or finite envelope",
            "p4_component": "Delta_boundary",
            "claim_effect": "would stop non-Hilbert current returning through integration by parts or finite-source cuts",
            "parent_signed": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "NGSA2334_8_projective_trace",
            "sector": "projective trace",
            "slot_question": "Is the projective mode gauge, fixed, or unobservable in all source/readout sectors?",
            "conditional_zero_clause": "Palatini LC can be promoted only after projective trace does not couple to source, spin, clock, light or orbit readout.",
            "evidence_status": "UNSIGNED_PARALLEL_CAVEAT",
            "open_gap": "projective certificate/policy remains outside this no-Gamma proof",
            "p4_component": "Delta_projective",
            "claim_effect": "would remove the last Palatini trace leakage caveat",
            "parent_signed": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "NGSA2334_9_verdict",
            "sector": "all sectors",
            "slot_question": "Can 2334 promote no-Gamma/no-hypermomentum for the whole local branch?",
            "conditional_zero_clause": "NGSA2334_1 through NGSA2334_8 would imply Delta_abs=0 if parent-signed.",
            "evidence_status": "NOT_PARENT_SIGNED_RETAIN_P4_COMPONENTS",
            "open_gap": "matter branch is promising, but source/readout/boundary/projective slots are still unsigned",
            "p4_component": "Delta_abs",
            "claim_effect": "no local-GR/Newton or WEP/clock/PPN pass is claimed",
            "parent_signed": "false",
            "valid_for_claim": "false",
        },
    ]


def build_theorem_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "NGT2334_0_variational_absence",
            "lemma": "variable-absence lemma",
            "statement": "For an action S[y] whose domain excludes Gamma_ind, the functional derivative delta S / delta Gamma_ind is zero/vacuous in the reduced variable space.",
            "proof_status": "EXACT_MATH_CONDITIONAL",
            "missing_parent_input": "the sector action domain must actually exclude Gamma_ind",
            "use": "basis of no-hypermomentum route",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "NGT2334_1_coframe_chain_rule",
            "lemma": "coframe-owned connection lemma",
            "statement": "If omega_obs=omega_LC[e_obs], variation of omega is induced by variation of e_obs and is counted in the metric/coframe field equation, not an independent Gamma equation.",
            "proof_status": "EXACT_MATH_CONDITIONAL",
            "missing_parent_input": "spinor and transport sectors must be explicitly written with omega_LC[e_obs]",
            "use": "blocks spin/torsion shortcut error",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "NGT2334_2_sector_sum",
            "lemma": "sector-sum lemma",
            "statement": "If each sector derivative delta S_i/delta Gamma_ind vanishes, then Delta_abs is zero without cancellation because every summand is individually zero.",
            "proof_status": "EXACT_MATH_CONDITIONAL",
            "missing_parent_input": "all sector slots must be signed, not merely the ordinary matter slot",
            "use": "no-cancellation no-tuning structure",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "NGT2334_3_no_reentry",
            "lemma": "readout no-reentry lemma",
            "statement": "A readout map does not source Gamma if it is downstream of the variational problem and does not define an extra source-labelled action/current.",
            "proof_status": "CONDITIONAL_CONTRACT_NEEDED",
            "missing_parent_input": "clock, light, orbit, boundary and marker maps need explicit downstream/no-current clauses",
            "use": "prevents measurement protocol from becoming hidden coupling",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "NGT2334_4_result",
            "lemma": "2334 theorem result",
            "statement": "The no-Gamma theorem is mathematically sharp but remains a conditional branch until source/readout/boundary/projective slots are parent-signed or P4-bounded.",
            "proof_status": "CONDITIONAL_THEOREM_NOT_CORPUS_PROMOTED",
            "missing_parent_input": "source/readout argument-list certificate or P4 component map",
            "use": "selects next attack without overclaiming",
            "valid_for_claim": "false",
        },
    ]


def build_p4_queue_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "P4DQ2334_0_total",
            "component": "Delta_abs",
            "formal_definition": "||Delta_matter|| + ||Delta_spin|| + ||Delta_source|| + ||Delta_clock|| + ||Delta_light|| + ||Delta_orbit|| + ||Delta_boundary|| + ||Delta_projective||",
            "zero_switch": "all no-Gamma sector slots parent-signed",
            "status": "MISSING_COMPONENT_ZERO_PROOFS_OR_BOUNDS",
            "units": "hypermomentum norm or normalized arena-specific envelope",
            "next_input": "component basis, norm, projection kernels, arena bounds",
            "score_ready": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "P4DQ2334_1_matter",
            "component": "Delta_matter",
            "formal_definition": "||delta S_matter / delta Gamma_ind||",
            "zero_switch": "ordinary matter has no Gamma_ind slot",
            "status": "ZERO_IF_1963_MUMC_BRANCH_ADOPTED_ELSE_BOUND",
            "units": "hypermomentum norm",
            "next_input": "canonical parent action adoption or component coefficient",
            "score_ready": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "P4DQ2334_2_spin",
            "component": "Delta_spin",
            "formal_definition": "||spin/torsion/nonmetricity connection current||",
            "zero_switch": "spin connection is omega_LC[e_obs] and no EC/metric-affine branch is active",
            "status": "MISSING_SPIN_BRANCH_EXCLUSION_OR_BOUND",
            "units": "spin-current or normalized torsion envelope",
            "next_input": "spinor action branch, axial torsion coefficient, spin density bound",
            "score_ready": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "P4DQ2334_3_source",
            "component": "Delta_source",
            "formal_definition": "||delta S_source/worldtube/GM / delta Gamma_ind||",
            "zero_switch": "source support and GM calibration are downstream Hilbert/coframe functionals",
            "status": "MISSING_SOURCE_WORLDTUBE_ARGUMENT_LIST",
            "units": "source-current or normalized GM envelope",
            "next_input": "source/worldtube no-Gamma certificate or finite-source bound",
            "score_ready": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "P4DQ2334_4_clock",
            "component": "Delta_clock",
            "formal_definition": "||delta S_clock/readout / delta Gamma_ind||",
            "zero_switch": "clock model is downstream of Gamma-free matter/gauge action",
            "status": "MISSING_CLOCK_ARGUMENT_LIST",
            "units": "clock frequency residual envelope",
            "next_input": "clock readout contract and bound map",
            "score_ready": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "P4DQ2334_5_light",
            "component": "Delta_light",
            "formal_definition": "||delta S_light/ray/detector / delta Gamma_ind||",
            "zero_switch": "light propagation/readout uses owned EM and g_obs/LC null structure only",
            "status": "MISSING_LIGHT_READOUT_ARGUMENT_LIST",
            "units": "lightcone/Shapiro/deflection residual envelope",
            "next_input": "EM/light readout no-Gamma certificate and PPN/light bound",
            "score_ready": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "P4DQ2334_6_orbit",
            "component": "Delta_orbit",
            "formal_definition": "||delta S_orbit/test-body/readout / delta Gamma_ind||",
            "zero_switch": "orbital readout is Hilbert matter motion in g_obs, not independent autoparallel law",
            "status": "MISSING_ORBIT_ARGUMENT_LIST",
            "units": "orbital/PPN residual envelope",
            "next_input": "test-body reduction and finite-body marker contract",
            "score_ready": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "P4DQ2334_7_boundary_projective",
            "component": "Delta_boundary + Delta_projective",
            "formal_definition": "||boundary/improvement Gamma current|| + ||projective trace coupling||",
            "zero_switch": "compact support/improvement silence plus projective gauge/fixed/unobservable certificate",
            "status": "MISSING_BOUNDARY_AND_PROJECTIVE_CERTIFICATE",
            "units": "source-current or normalized projective envelope",
            "next_input": "boundary no-flux proof and projective trace policy",
            "score_ready": "false",
            "valid_for_claim": "false",
        },
    ]


def build_decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "DEC2334_0_theorem_result",
            "decision": "no-Gamma theorem is exact as a conditional sector-sum lemma",
            "reason": "variable absence plus coframe-owned connection gives zero hypermomentum without cancellation",
            "consequence": "this is the right derivation route, not a numerical patch",
            "status": "CONDITIONAL_MATH_READY",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DEC2334_1_no_promotion",
            "decision": "do not promote Levi-Civita/no-hypermomentum yet",
            "reason": "source, clock, light, orbit, boundary and projective slots are not parent-signed",
            "consequence": "retain P4 component queue and no public/local-GR claim",
            "status": "RETAIN_P4_COMPONENTS",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DEC2334_2_best_next",
            "decision": "write source/readout no-Gamma action-argument certificate next",
            "reason": "one explicit argument-list contract could close several leak paths at once",
            "consequence": "if certificate fails, fill P4 Delta_source/clock/light/orbit units and maps",
            "status": "SELECT_SOURCE_READOUT_ARGUMENT_LIST_NEXT",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DEC2334_3_public_policy",
            "decision": "no GitHub evidence update from this checkpoint",
            "reason": "2334 is a private derivation/fallback gate, not a publishable GR-reduction result",
            "consequence": "keep working in post-checkpoint-work",
            "status": "NO_GITHUB_EVIDENCE_UPDATE",
            "valid_for_claim": "false",
        },
    ]


def build_claim_rows() -> list[dict[str, Any]]:
    return [
        {"branch_id": BRANCH_ID, "row_id": "CG2334_0_no_gamma_active", "gate": "no-Gamma branch parent-signed for all sectors", "passed": "false", "claim_effect": "conditional theorem only", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "CG2334_1_no_hypermomentum", "gate": "Delta_lambda^{mu nu}=0 for ordinary local branch", "passed": "false", "claim_effect": "source/readout slots unsigned", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "CG2334_2_Levi_Civita", "gate": "Gamma_obs=LC(g_obs), T=0, Q=0 derived", "passed": "false", "claim_effect": "needs no-Gamma plus EH/Palatini/projective closure", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "CG2334_3_P4_score", "gate": "P4 Delta components have numeric units/maps/bounds", "passed": "false", "claim_effect": "component queue only", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "CG2334_4_local_GR_Newton", "gate": "local GR/Newton recovery derived", "passed": "false", "claim_effect": "connection and EH/GM gates still open", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "CG2334_5_github_public_update", "gate": "safe to push as public evidence", "passed": "false", "claim_effect": "private checkpoint only", "valid_for_claim": "false"},
    ]


def build_refusal_rows() -> list[dict[str, Any]]:
    return [
        {"branch_id": BRANCH_ID, "row_id": "REF2334_0_conditional_as_active", "claim": "the no-Gamma theorem is now active in MTS", "allowed": "false", "reason": "2334 proves the theorem shape but not the parent-signed sector argument list", "blocking_rows": "NGSA2334_9_verdict;CG2334_0_no_gamma_active", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "REF2334_1_matter_closes_readout", "claim": "ordinary matter no-Gamma automatically closes clocks, light and orbits", "allowed": "false", "reason": "readout maps can re-enter as source-labelled currents unless explicitly downstream/Gamma-free", "blocking_rows": "NGSA2334_5_clock_readout;NGSA2334_6_orbital_readout", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "REF2334_2_ignore_source_worldtube", "claim": "source/worldtube Gamma slot can be ignored", "allowed": "false", "reason": "Newton/GM matching depends on source support and finite-boundary behavior", "blocking_rows": "NGSA2334_4_source_worldtube;P4DQ2334_3_source", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "REF2334_3_p4_as_pass", "claim": "the P4 queue is an empirical pass", "allowed": "false", "reason": "P4 rows still lack component values, units, projection kernels and arena bounds", "blocking_rows": "P4DQ2334_0_total;CG2334_3_P4_score", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "REF2334_4_github", "claim": "publish this as GR reduction evidence", "allowed": "false", "reason": "2334 is a private structural audit; it does not close local GR/Newton", "blocking_rows": "CG2334_4_local_GR_Newton;CG2334_5_github_public_update", "valid_for_claim": "false"},
    ]


def build_next_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "NEXT2334_0",
            "next_target": "2335-Y5-R2FR-source-readout-noGamma-action-argument-certificate.md",
            "why": "highest leverage derivation route: explicitly list source, clock, light, orbit, boundary and readout arguments and prove none contain Gamma_ind.",
            "claim_status": "private_derivation_next_step",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "NEXT2334_1",
            "next_target": "2335b-Y5-R2FR-P4-Delta-component-values-units-map.md",
            "why": "fallback if any source/readout slot remains open: convert Delta_source/clock/light/orbit/boundary into sourced, unit-normalized P4 rows.",
            "claim_status": "fallback_nonclaim",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "NEXT2334_2",
            "next_target": "2335c-Y5-R2FR-projective-trace-certificate-or-policy.md",
            "why": "Palatini/metric-affine route still needs a trace gauge/fixed/unobservable certificate.",
            "claim_status": "parallel_nonclaim",
            "valid_for_claim": "false",
        },
    ]


def copy_branch_outputs() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row_id, src, dest in BRANCH_COPY_SPECS:
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(src, dest)
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "row_id": row_id,
                "source_csv": relative_path(src),
                "branch_copy_path": str(dest),
                "copy_exists": bool_text(dest.exists()),
                "row_count": str(len(read_csv_rows(dest))),
                "valid_for_claim": "false",
            }
        )
    return rows


def build_validation_rows(source_rows: list[dict[str, Any]], branch_copy_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    def add(row_id: str, passed: bool, detail: str) -> None:
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "row_id": row_id,
                "status": "PASS" if passed else "FAIL",
                "detail": detail,
                "valid_for_claim": "false",
            }
        )

    generated_paths = [path for key, path in OUTPUTS.items() if key != "validation"]
    generated_paths += [Path(row["branch_copy_path"]) for row in branch_copy_rows]
    required_sources = [row for row in source_rows if row["required"] == "true"]

    add("VAL2334_00_required_sources_exist", all(row["exists"] == "true" for row in required_sources), "every required source path exists")
    add("VAL2334_01_required_needles_found", all(row["needles_found"] == "true" for row in required_sources), "all required source needles were found")
    theorem_rows = read_csv_rows(OUTPUTS["theorem"])
    add("VAL2334_02_conditional_theorem_stack", any(row.get("row_id") == "NGT2334_4_result" and row.get("proof_status") == "CONDITIONAL_THEOREM_NOT_CORPUS_PROMOTED" for row in theorem_rows), "conditional theorem result recorded without promotion")
    slot_rows = read_csv_rows(OUTPUTS["slots"])
    required_slot_ids = {
        "NGSA2334_1_ordinary_matter",
        "NGSA2334_4_source_worldtube",
        "NGSA2334_5_clock_readout",
        "NGSA2334_6_orbital_readout",
        "NGSA2334_7_boundary_domain",
        "NGSA2334_9_verdict",
    }
    present_slot_ids = {row.get("row_id") for row in slot_rows}
    add("VAL2334_03_sector_slots_present", required_slot_ids.issubset(present_slot_ids), "major matter/source/readout slots present")
    add("VAL2334_04_no_promotion", any(row.get("row_id") == "NGSA2334_9_verdict" and row.get("evidence_status") == "NOT_PARENT_SIGNED_RETAIN_P4_COMPONENTS" for row in slot_rows), "no-Gamma branch not promoted")
    p4_rows = read_csv_rows(OUTPUTS["p4_queue"])
    required_p4 = {"Delta_matter", "Delta_source", "Delta_clock", "Delta_light", "Delta_orbit", "Delta_boundary + Delta_projective"}
    present_p4 = {row.get("component") for row in p4_rows}
    add("VAL2334_05_p4_components_present", required_p4.issubset(present_p4), "P4 component queue covers matter/source/readout/boundary")
    add("VAL2334_06_p4_nonready", all(row.get("score_ready") == "false" for row in p4_rows), "P4 rows remain non-score-ready")
    decision_rows = read_csv_rows(OUTPUTS["decision"])
    add("VAL2334_07_next_certificate_selected", any(row.get("row_id") == "DEC2334_2_best_next" and row.get("status") == "SELECT_SOURCE_READOUT_ARGUMENT_LIST_NEXT" for row in decision_rows), "source/readout argument-list certificate selected next")
    claim_rows = read_csv_rows(OUTPUTS["claims"])
    add("VAL2334_08_local_claims_block", any(row.get("row_id") == "CG2334_4_local_GR_Newton" and row.get("passed") == "false" for row in claim_rows), "local GR/Newton claim gate remains false")
    add("VAL2334_09_github_blocked", any(row.get("row_id") == "CG2334_5_github_public_update" and row.get("passed") == "false" for row in claim_rows), "public GitHub update not recommended from 2334")
    refusal_rows = read_csv_rows(OUTPUTS["refusal"])
    add("VAL2334_10_refusals_block", all(row.get("allowed") == "false" for row in refusal_rows), "refusal runner blocks shortcut claims")
    add("VAL2334_11_branch_copies_parse", all(Path(row["branch_copy_path"]).exists() and int(row["row_count"]) > 0 for row in branch_copy_rows), "branch copies exist and parse")

    claim_flags: list[str] = []
    for path in generated_paths:
        for index, row in enumerate(read_csv_rows(path), start=2):
            if str(row.get("valid_for_claim", "")).lower() == "true":
                claim_flags.append(f"{path.name}:{index}")
    add("VAL2334_12_no_claim_flags", not claim_flags, "no generated row is valid_for_claim=true" if not claim_flags else ";".join(claim_flags))

    formalization_hits: list[Path] = []
    if FORMALIZATION.exists():
        for pattern in ("*2334*.csv", "*2334*.md", "*NOGAMMA*2334*", "*P4*2334*"):
            formalization_hits.extend(FORMALIZATION.rglob(pattern))
    add("VAL2334_13_formalization_untouched_by_2334", not formalization_hits, "no 2334 checkpoint output appears in formalization-workbench" if not formalization_hits else ";".join(str(path) for path in formalization_hits[:5]))
    add("VAL2334_OVERALL", all(row["status"] == "PASS" for row in rows), "2334 sharpens the no-Gamma theorem into a sector-sum audit, refuses to promote it while source/readout slots are unsigned, keeps P4 Delta components queued, and selects the source/readout action-argument certificate next.")
    return rows


def write_doc(
    source_rows: list[dict[str, Any]],
    slot_rows: list[dict[str, Any]],
    theorem_rows: list[dict[str, Any]],
    p4_queue_rows: list[dict[str, Any]],
    decision_rows: list[dict[str, Any]],
    claim_rows: list[dict[str, Any]],
    refusal_rows: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    branch_copy_rows: list[dict[str, Any]],
    validation_rows: list[dict[str, Any]],
) -> None:
    content = f"""# 2334 - noGamma Slot Matter Source Readout Audit

## Summary

2334 tries the clean derivation route after 2333: do not assume Levi-Civita, prove there is no independent `Gamma`
slot in the ordinary local branch.

The result is useful but not yet claim-grade:

1. The no-Gamma theorem is exact as a conditional variational statement.
2. Ordinary matter and spin are clean inside the owned-coframe / MUMC branch.
3. Source/worldtube, clock, light, orbit, boundary and projective trace are still unsigned.
4. Therefore `Delta_abs=0`, Levi-Civita, local GR and Newton recovery are not promoted here.

The next best target is a source/readout action-argument certificate: list every source, clock, light, orbit, boundary
and readout argument and prove none contains `Gamma_ind`. If that fails, the same rows become P4 component bounds.

## Source Register

{markdown_table(source_rows, ["row_id", "source_key", "source_path", "exists", "required", "needles_found", "source_role", "valid_for_claim"])}

## Gamma Slot Sector Audit

{markdown_table(slot_rows, ["row_id", "sector", "slot_question", "evidence_status", "open_gap", "p4_component", "parent_signed", "valid_for_claim"])}

## no-Gamma Theorem Stack

{markdown_table(theorem_rows, ["row_id", "lemma", "statement", "proof_status", "missing_parent_input", "use", "valid_for_claim"])}

## P4 Delta Component Queue

{markdown_table(p4_queue_rows, ["row_id", "component", "formal_definition", "zero_switch", "status", "units", "score_ready", "valid_for_claim"])}

## Decision Ledger

{markdown_table(decision_rows, ["row_id", "decision", "reason", "consequence", "status", "valid_for_claim"])}

## Claim Gates

{markdown_table(claim_rows, ["row_id", "gate", "passed", "claim_effect", "valid_for_claim"])}

## Refusal Runner

{markdown_table(refusal_rows, ["row_id", "claim", "allowed", "reason", "blocking_rows", "valid_for_claim"])}

## Next Target

{markdown_table(next_rows, ["row_id", "next_target", "why", "claim_status", "valid_for_claim"])}

## Branch Copies

{markdown_table(branch_copy_rows, ["row_id", "source_csv", "branch_copy_path", "copy_exists", "row_count", "valid_for_claim"])}

## Validation

{markdown_table(validation_rows, ["row_id", "status", "detail", "valid_for_claim"])}
"""
    DOC.write_text(content, encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    rows_by_output = {
        "sources": build_sources(),
        "slots": build_slot_rows(),
        "theorem": build_theorem_rows(),
        "p4_queue": build_p4_queue_rows(),
        "decision": build_decision_rows(),
        "claims": build_claim_rows(),
        "refusal": build_refusal_rows(),
        "next": build_next_rows(),
    }
    for key, rows in rows_by_output.items():
        write_csv(OUTPUTS[key], rows)
    branch_copy_rows = copy_branch_outputs()
    write_csv(OUTPUTS["copies"], branch_copy_rows)
    validation_rows = build_validation_rows(rows_by_output["sources"], branch_copy_rows)
    write_csv(OUTPUTS["validation"], validation_rows)
    write_doc(
        rows_by_output["sources"],
        rows_by_output["slots"],
        rows_by_output["theorem"],
        rows_by_output["p4_queue"],
        rows_by_output["decision"],
        rows_by_output["claims"],
        rows_by_output["refusal"],
        rows_by_output["next"],
        branch_copy_rows,
        validation_rows,
    )
    failed = [row for row in validation_rows if row["status"] != "PASS"]
    if failed:
        raise SystemExit("2334 validation failed: " + "; ".join(row["row_id"] for row in failed))
    print(f"wrote {DOC}")
    print(f"wrote {OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
