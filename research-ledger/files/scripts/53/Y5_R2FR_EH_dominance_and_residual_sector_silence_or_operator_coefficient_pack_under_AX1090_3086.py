from __future__ import annotations

import csv
import hashlib
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


RUN_UTC = datetime.now(timezone.utc).isoformat()
ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
FORMALIZATION = PROJECT / "formalization-workbench"
PYCACHE = ROOT / "scripts" / "__pycache__"

CHECKPOINT = "3086"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"

DOC = ROOT / "3086-Y5-R2FR-EH-dominance-and-residual-sector-silence-or-operator-coefficient-pack-under-AX1090.md"
DOTG_TARGET = RESIDUALS / "P8_time_drift_residual_or_zero.csv"

SOURCE_PATHS = {
    "SRC3086_00_3085_doc": ROOT / "3085-Y5-R2FR-source-shadow-ban-or-tauWEP-direct-product-first-source-row-under-AX1090.md",
    "SRC3086_01_3085_next": RESIDUALS / "P8_Y5_R2FR_3085_NEXT_TARGET.csv",
    "SRC3086_02_3085_gr_handoff": RESIDUALS / "P8_Y5_R2FR_3085_GR_BRIDGE_HANDOFF.csv",
    "SRC3086_03_3085_normal_form": RESIDUALS / "P8_Y5_R2FR_3085_SOURCE_MAP_NORMAL_FORM_STATUS.csv",
    "SRC3086_04_1840_doc": ROOT / "1840-Y5-R2FR-EH-dominance-and-residual-sector-silence-or-operator-coefficient-pack.md",
    "SRC3086_05_1840_eh_attempt": RESIDUALS / "P8_Y5_PARENT_QLOC_1840_EH_DOMINANCE_THEOREM_ATTEMPT.csv",
    "SRC3086_06_1840_sector_audit": RESIDUALS / "P8_Y5_PARENT_QLOC_1840_RESIDUAL_SECTOR_SILENCE_AUDIT.csv",
    "SRC3086_07_1840_operator_pack": RESIDUALS / "P8_Y5_PARENT_QLOC_1840_OPERATOR_COEFFICIENT_PACK.csv",
    "SRC3086_08_1840_empirical_map": RESIDUALS / "P8_Y5_PARENT_QLOC_1840_EMPIRICAL_BOUND_MAP.csv",
    "SRC3086_09_1840_countermodels": RESIDUALS / "P8_Y5_PARENT_QLOC_1840_COUNTERMODEL_LEDGER.csv",
    "SRC3086_10_1840_bridge_status": RESIDUALS / "P8_Y5_PARENT_QLOC_1840_GR_BRIDGE_STATUS.csv",
    "SRC3086_11_1769_einstein_limit": RESIDUALS / "P8_Y5_PARENT_QLOC_1769_EINSTEIN_LEFT_HAND_LIMIT_ATTEMPT.csv",
    "SRC3086_12_1769_residual_pack": RESIDUALS / "P8_Y5_PARENT_QLOC_1769_OPERATOR_RESIDUAL_PACK.csv",
    "SRC3086_13_1770_eh_attempt": RESIDUALS / "P8_Y5_PARENT_QLOC_1770_EH_DOMINANCE_THEOREM_ATTEMPT.csv",
    "SRC3086_14_1770_sector_silence": RESIDUALS / "P8_Y5_PARENT_QLOC_1770_RESIDUAL_SECTOR_SILENCE_AUDIT.csv",
    "SRC3086_15_1770_operator_pack": RESIDUALS / "P8_Y5_PARENT_QLOC_1770_OPERATOR_COEFFICIENT_PACK.csv",
    "SRC3086_16_1770_empirical_map": RESIDUALS / "P8_Y5_PARENT_QLOC_1770_EMPIRICAL_BOUND_MAP.csv",
    "SRC3086_17_1768_normal_form": RESIDUALS / "P8_Y5_PARENT_QLOC_1768_PARENT_ACTION_NORMAL_FORM_SIGNATURE.csv",
    "SRC3086_18_1009_parent_contract": ROOT / "1009-Y5-R10-parent-current-chain-action-contract-or-sector-variation-runner.md",
    "SRC3086_19_1841_old_next": ROOT / "1841-Y5-R2FR-sector-action-variation-and-local-scaling-silence-or-operator-bounds.md",
    "SRC3086_20_dotg_target": DOTG_TARGET,
}

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_3086_SOURCE_REGISTER.csv",
    "eh_attempt": RESIDUALS / "P8_Y5_R2FR_3086_EH_DOMINANCE_THEOREM_ATTEMPT.csv",
    "sector_audit": RESIDUALS / "P8_Y5_R2FR_3086_RESIDUAL_SECTOR_SILENCE_AUDIT.csv",
    "operator_pack": RESIDUALS / "P8_Y5_R2FR_3086_OPERATOR_COEFFICIENT_PACK_NONCLAIM.csv",
    "empirical_map": RESIDUALS / "P8_Y5_R2FR_3086_EMPIRICAL_BOUND_MAP_NONCLAIM.csv",
    "countermodels": RESIDUALS / "P8_Y5_R2FR_3086_COUNTERMODEL_LEDGER.csv",
    "bridge_status": RESIDUALS / "P8_Y5_R2FR_3086_GR_BRIDGE_STATUS.csv",
    "corpus_gate": RESIDUALS / "P8_Y5_R2FR_3086_CURRENT_CORPUS_GATE.csv",
    "score_blockers": RESIDUALS / "P8_Y5_R2FR_3086_SCORE_BLOCKER_LEDGER.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_3086_DECISION_LEDGER.csv",
    "claim_status": RESIDUALS / "P8_Y5_R2FR_3086_CLAIM_STATUS.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_3086_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_3086_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_3086_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "sector_audit_copy": LOCAL_BOUNDS / "EH_residual_sector_silence_audit_3086_NONCLAIM.csv",
    "operator_pack_copy": LOCAL_BOUNDS / "EH_operator_coefficient_pack_3086_NONCLAIM.csv",
    "empirical_map_copy": LOCAL_BOUNDS / "EH_operator_empirical_bound_map_3086_NONCLAIM.csv",
    "bridge_status_copy": LOCAL_BOUNDS / "GR_bridge_status_3086_NONCLAIM.csv",
    "next_copy": RAB_QUEUE / "JR3086_sector_action_variation_local_scaling_NEXT_NONCLAIM.csv",
}

for output_path in list(OUTPUTS.values()) + list(BRANCH_OUTPUTS.values()) + [DOC]:
    output_path.parent.mkdir(parents=True, exist_ok=True)


def remove_pycache() -> None:
    if PYCACHE.exists():
        shutil.rmtree(PYCACHE)


def file_hash(path: Path) -> str:
    if not path.exists():
        return "MISSING"
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def boolish(value: Any) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes", "y", "pass", "passed"}


def csv_ok(path: Path) -> bool:
    try:
        if not path.exists():
            return False
        with path.open("r", newline="", encoding="utf-8") as handle:
            list(csv.DictReader(handle))
        return True
    except Exception:
        return False


def source_parse_ok(path: Path) -> bool:
    if not path.exists():
        return False
    return csv_ok(path) if path.suffix.lower() == ".csv" else True


def row_count(path: Path) -> int:
    if not path.exists():
        return 0
    if path.suffix.lower() == ".csv":
        return len(rows(path))
    return len(path.read_text(encoding="utf-8").splitlines())


def write_csv(path: Path, output_rows: list[dict[str, Any]]) -> None:
    fieldnames: list[str] = []
    for output_row in output_rows:
        for key in output_row:
            if key not in fieldnames:
                fieldnames.append(key)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for output_row in output_rows:
            writer.writerow({key: output_row.get(key, "") for key in fieldnames})


def under(path: Path, root: Path) -> bool:
    try:
        path.resolve().relative_to(root.resolve())
        return True
    except ValueError:
        return False


def has_claim_true(input_rows: list[dict[str, Any]]) -> bool:
    claim_fields = {
        "valid_for_claim",
        "claim_allowed",
        "valid_prediction_row",
        "score_ready",
        "claim_active",
        "gate_pass",
        "score_allowed",
        "operator_ready",
        "bridge_claim",
        "local_gr_claim",
        "newton_claim",
        "ppn_claim",
    }
    for input_row in input_rows:
        for field in claim_fields:
            if field in input_row and boolish(input_row[field]):
                return True
    return False


def base(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "checkpoint": CHECKPOINT,
        "branch_id": BRANCH_ID,
        "timestamp_utc": RUN_UTC,
        "score_ready": "false",
        "valid_prediction_row": "false",
        "valid_for_claim": "false",
        "claim_allowed": "false",
        **row,
    }


def md_escape(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def md_table(table_rows: list[dict[str, Any]], columns: list[str]) -> str:
    if not table_rows:
        return "_No rows._"
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    lines = [header, separator]
    for table_row in table_rows:
        lines.append("| " + " | ".join(md_escape(table_row.get(column, "")) for column in columns) + " |")
    return "\n".join(lines)


def copy_csv(source_path: Path, destination_path: Path) -> None:
    destination_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source_path, destination_path)


remove_pycache()
dotg_hash_before = file_hash(DOTG_TARGET)

source_register = [
    base(
        {
            "source_id": source_id,
            "source_path": str(source_path),
            "exists": str(source_path.exists()),
            "parse_ok": str(source_parse_ok(source_path)),
            "row_count": row_count(source_path),
            "role": "EH_dominance_operator_bridge_evidence"
            if source_id != "SRC3086_20_dotg_target"
            else "append_guard_target",
            "status": "PRESENT" if source_path.exists() else "MISSING_SOURCE",
        }
    )
    for source_id, source_path in SOURCE_PATHS.items()
]

eh_attempt_rows = [
    base(
        {
            "attempt_id": "EHD3086_0_target",
            "claim_piece": "local Einstein-Hilbert dominance",
            "mathematical_form": "E_LHS = G_munu + Lambda g_munu + DeltaE_munu",
            "proof_route": "derive parent Euler-Lagrange operator, split EH piece from every retained MTS sector, and prove DeltaE_munu=0 or locally negligible",
            "current_result": "target sharpened but not parent-signed",
            "current_status": "TARGET_EXACT_NONCLAIM",
            "remaining_gap": "sector variation table and local scaling theorem are not complete",
        }
    ),
    base(
        {
            "attempt_id": "EHD3086_1_zero_theorem",
            "claim_piece": "residual-sector zero theorem",
            "mathematical_form": "for each retained i: delta S_i / delta e_obs | local = 0",
            "proof_route": "show the non-EH sector is topological, pure boundary, vertically silent, quotient-invisible, or not coupled to the observed coframe",
            "current_result": "available as theorem shape only",
            "current_status": "CONDITIONAL_ZERO_THEOREM_NOT_PROVED",
            "remaining_gap": "no sector-by-sector proof for higher-derivative, projector, boundary, nonminimal, memory/coframe, and source-normalization blocks",
        }
    ),
    base(
        {
            "attempt_id": "EHD3086_2_suppression_theorem",
            "claim_piece": "controlled nonzero residual suppression",
            "mathematical_form": "||DeltaE_i|| / ||G_munu|| <= epsilon_i(L_local,L_cg,coefficients)",
            "proof_route": "derive dimensions, coefficients and local scale hierarchy so every residual is below PPN/R10/clock/orbit tolerance",
            "current_result": "not available from current corpus",
            "current_status": "MISSING_SCALING_AND_COEFFICIENTS",
            "remaining_gap": "no signed coefficient normalization or tolerance conversion",
        }
    ),
    base(
        {
            "attempt_id": "EHD3086_3_Bianchi_noether",
            "claim_piece": "Bianchi/Noether compatibility",
            "mathematical_form": "nabla_mu(G^{mu nu}+Lambda g^{mu nu}+DeltaE^{mu nu})=0",
            "proof_route": "derive from one complete diffeomorphism-invariant parent action; do not drop terms after variation",
            "current_result": "conditional identity only",
            "current_status": "CONDITIONAL_PARENT_ACTION_IDENTITY",
            "remaining_gap": "1009 total parent action remains not_promoted and sector certificates are incomplete",
        }
    ),
    base(
        {
            "attempt_id": "EHD3086_4_Newton_limit",
            "claim_piece": "Newton/Poisson reduction after EH dominance",
            "mathematical_form": "G_00 -> 2 nabla^2 Phi/c^2 and nabla^2 Phi = 4 pi G rho",
            "proof_route": "EH dominance plus source normalization and weak-field slow-motion limit",
            "current_result": "blocked behind EH dominance and source normalization",
            "current_status": "CONDITIONAL_NOT_PROMOTED",
            "remaining_gap": "left-hand residuals and measured-G/source normalization remain open",
        }
    ),
    base(
        {
            "attempt_id": "EHD3086_5_current_verdict",
            "claim_piece": "current MTS local GR bridge",
            "mathematical_form": "DeltaE_munu=0 or bounded strongly enough for local GR/PPN",
            "proof_route": "zero theorem or coefficient-bound route",
            "current_result": "not proved; retain explicit residual coefficients",
            "current_status": "FAIL_CURRENT_PARENT_PROOF",
            "remaining_gap": "move to sector-action variation and local scaling, not public claim",
        }
    ),
]

sector_rows = [
    base(
        {
            "sector_id": "RSS3086_0_higher_derivative",
            "sector": "higher-curvature / higher-derivative geometry",
            "operator_form": "c_R2 R^2 + c_Ricci2 R_munu R^munu + c_boxR R box R",
            "zero_or_suppression_route": "absent from parent normal form, topological in the local branch, or suppressed by a high scale",
            "current_status": "MISSING_OPERATOR_BASIS_AND_SCALE",
            "coefficient_row": "OPC3086_1_higher_derivative",
            "next_requirement": "vary the candidate sector and derive coefficient dimensions/signs",
        }
    ),
    base(
        {
            "sector_id": "RSS3086_1_projector",
            "sector": "domain/projector/readout operator",
            "operator_form": "E_projector(Pi_M), [d,Pi_M]J_H, or local quotient residual",
            "zero_or_suppression_route": "Pi_M becomes identity or commutes in the local branch; otherwise it is a bounded residual",
            "current_status": "MISSING_PROJECTOR_VARIATION_AND_COMMUTATOR_ZERO",
            "coefficient_row": "OPC3086_2_projector",
            "next_requirement": "derive Pi_M local normal form and its variation",
        }
    ),
    base(
        {
            "sector_id": "RSS3086_2_boundary",
            "sector": "boundary/reference/improvement terms",
            "operator_form": "DeltaE_boundary, Q_boundary, reference counterterm or improvement stress",
            "zero_or_suppression_route": "fixed-before-readout reference plus local/falloff boundary silence",
            "current_status": "MISSING_BOUNDARY_SILENCE_AND_FIXED_REFERENCE",
            "coefficient_row": "OPC3086_3_boundary",
            "next_requirement": "prove boundary variation vanishes locally or keep explicit coefficient",
        }
    ),
    base(
        {
            "sector_id": "RSS3086_3_nonminimal",
            "sector": "nonminimal matter-geometry/MTS coupling",
            "operator_form": "f(X,Phi)L_m, A(X)J_m, curvature-matter coupling or hidden source-map channel",
            "zero_or_suppression_route": "forbidden by source-map normal form, or derived as real matter dynamics with a source-backed bound",
            "current_status": "MISSING_FORBID_OR_BOUND",
            "coefficient_row": "OPC3086_4_nonminimal",
            "next_requirement": "prove no representative-dependent matter coupling re-enters",
        }
    ),
    base(
        {
            "sector_id": "RSS3086_4_memory_coframe",
            "sector": "memory/coframe/current-chain residual",
            "operator_form": "DeltaE_mem(theta,Q_tau,C_tau) or coframe-memory stress",
            "zero_or_suppression_route": "closed current chain, exact/boundary-only theta, or small local memory projection",
            "current_status": "MISSING_CURRENT_CHAIN_CERTIFICATES",
            "coefficient_row": "OPC3086_5_memory_coframe",
            "next_requirement": "complete 1009 sector certificates and local scaling",
        }
    ),
    base(
        {
            "sector_id": "RSS3086_5_source_normalization",
            "sector": "measured-G/source normalization",
            "operator_form": "delta_G_source, M_H_ref, source-shadow or Hilbert-source normalization residual",
            "zero_or_suppression_route": "single Hilbert source plus measured-G normalization theorem",
            "current_status": "MISSING_SOURCE_NORMALIZATION_OWNER",
            "coefficient_row": "OPC3086_6_source_normalization",
            "next_requirement": "connect Hilbert source, measured G, and Poisson source without absorbing residuals",
        }
    ),
    base(
        {
            "sector_id": "RSS3086_6_verdict",
            "sector": "all non-EH residual sectors",
            "operator_form": "DeltaE_munu=sum_i c_i O_i_munu",
            "zero_or_suppression_route": "all sectors zero/suppressed/bounded",
            "current_status": "RESIDUAL_SECTORS_RETAINED_NONCLAIM",
            "coefficient_row": "OPC3086_0_total_DeltaE",
            "next_requirement": "3087 must vary sectors and derive local scalings before any GR claim",
        }
    ),
]

operator_rows = [
    base(
        {
            "row_id": "OPC3086_0_total_DeltaE",
            "quantity": "DeltaE_munu",
            "definition": "total left-hand non-Einstein operator residual",
            "symbolic_form": "DeltaE_munu=sum_i c_i O_i_munu",
            "units": "curvature_operator_units",
            "source_status": "MISSING_ZERO_THEOREM_OR_BOUNDED_COEFFICIENTS",
            "test_arenas": "PPN;R10;clocks;orbits;cosmology",
        }
    ),
    base(
        {
            "row_id": "OPC3086_1_higher_derivative",
            "quantity": "c_HD",
            "definition": "higher-curvature operator coefficient vector",
            "symbolic_form": "{c_R2,c_Ricci2,c_boxR,...}",
            "units": "length^2 or model-dependent inverse mass powers",
            "source_status": "MISSING_PARENT_VARIATION_AND_SCALE",
            "test_arenas": "PPN;short-range gravity;binary/orbital;cosmology",
        }
    ),
    base(
        {
            "row_id": "OPC3086_2_projector",
            "quantity": "c_projector",
            "definition": "operator strength from quotient/domain/projector residual",
            "symbolic_form": "c_Pi O_Pi_munu",
            "units": "curvature_operator_units after projection",
            "source_status": "MISSING_PROJECTOR_LOCAL_VARIATION",
            "test_arenas": "PPN;WEP;R10;clock/frame tests",
        }
    ),
    base(
        {
            "row_id": "OPC3086_3_boundary",
            "quantity": "c_boundary",
            "definition": "boundary/reference/improvement residual coefficient",
            "symbolic_form": "c_B O_B_munu",
            "units": "boundary-induced curvature_operator_units",
            "source_status": "MISSING_BOUNDARY_SILENCE_THEOREM",
            "test_arenas": "R10;orbital;clock;energy-conservation consistency",
        }
    ),
    base(
        {
            "row_id": "OPC3086_4_nonminimal",
            "quantity": "c_nonminimal",
            "definition": "nonminimal matter-geometry coupling residual",
            "symbolic_form": "c_NM O_NM_munu(T_H,X,Phi)",
            "units": "coupling-dependent curvature_operator_units",
            "source_status": "MISSING_NO_HIDDEN_STRESS_OR_BOUND",
            "test_arenas": "WEP;PPN;clocks;particle/EM side constraints",
        }
    ),
    base(
        {
            "row_id": "OPC3086_5_memory_coframe",
            "quantity": "c_memory",
            "definition": "memory/coframe/current-chain left-hand residual coefficient",
            "symbolic_form": "c_M O_M_munu(theta,Q_tau,C_tau)",
            "units": "current-chain induced curvature_operator_units",
            "source_status": "MISSING_CURRENT_CHAIN_LOCAL_SILENCE",
            "test_arenas": "clocks;cosmology growth;orbital drift;PPN preferred-frame",
        }
    ),
    base(
        {
            "row_id": "OPC3086_6_source_normalization",
            "quantity": "delta_G_source",
            "definition": "source-normalization mismatch in the Poisson/Newton bridge",
            "symbolic_form": "nabla^2 Phi = 4 pi G(1+delta_G_source) rho + residuals",
            "units": "dimensionless after measured-G normalization",
            "source_status": "MISSING_MEASURED_G_OWNER",
            "test_arenas": "Newton limit;orbital systems;laboratory G;PPN",
        }
    ),
]

empirical_rows = [
    base(
        {
            "map_id": "EBM3086_0_ppn_gamma_beta",
            "arena": "PPN gamma and beta",
            "residual_input": "DeltaE_munu,c_HD,c_projector,c_memory,c_nonminimal",
            "required_output": "derive gamma=beta=1 or bound gamma-1,beta-1 from the operator pack",
            "current_status": "MISSING_PPN_RESIDUAL_MAP",
        }
    ),
    base(
        {
            "map_id": "EBM3086_1_R10_Yukawa",
            "arena": "R10 short-range gravity",
            "residual_input": "operator coefficients projected to alpha(lambda)",
            "required_output": "alpha_predicted(lambda) with real source coefficients and real bound curve",
            "current_status": "MISSING_ALPHA_LAMBDA_PROJECTION",
        }
    ),
    base(
        {
            "map_id": "EBM3086_2_clocks",
            "arena": "clock/redshift/preferred-frame tests",
            "residual_input": "c_memory,c_projector,c_nonminimal",
            "required_output": "clock residual vector with units, signs and source paths",
            "current_status": "MISSING_CLOCK_RESIDUAL_VECTOR",
        }
    ),
    base(
        {
            "map_id": "EBM3086_3_orbits",
            "arena": "orbital systems and perihelion/binary constraints",
            "residual_input": "c_HD,c_boundary,delta_G_source",
            "required_output": "orbital residual coefficients after measured-G normalization",
            "current_status": "MISSING_ORBITAL_RESIDUAL_MAP",
        }
    ),
    base(
        {
            "map_id": "EBM3086_4_cosmology",
            "arena": "FLRW/cosmology bridge",
            "residual_input": "large-scale memory/coupling terms",
            "required_output": "keep cosmology separate from the local GR proof until local scaling is derived",
            "current_status": "HELD_SEPARATE_NONCLAIM",
        }
    ),
]

countermodel_rows = [
    base(
        {
            "countermodel_id": "CM3086_0_small_residual_tail",
            "obstruction": "DeltaE_munu is tiny but nonzero and produces a PPN/R10 tail",
            "why_survives": "no local scaling bound or exact zero theorem has been derived",
            "effect": "cannot claim exact GR; must score residual coefficient",
            "disposition": "RETAINED",
        }
    ),
    base(
        {
            "countermodel_id": "CM3086_1_cancellation",
            "obstruction": "two non-EH sectors cancel in one arena but not all arenas",
            "why_survives": "cancellations are not parent-signed symmetries",
            "effect": "cannot use one successful arena to infer universal silence",
            "disposition": "RETAINED",
        }
    ),
    base(
        {
            "countermodel_id": "CM3086_2_boundary_fit",
            "obstruction": "boundary/reference choice hides residuals in measured G",
            "why_survives": "fixed-before-readout and boundary silence are unsigned",
            "effect": "Newton/Poisson bridge remains conditional",
            "disposition": "RETAINED",
        }
    ),
    base(
        {
            "countermodel_id": "CM3086_3_source_normalization",
            "obstruction": "source normalization absorbs non-EH terms instead of deriving them away",
            "why_survives": "source-normalization owner remains missing",
            "effect": "measured-G route cannot promote local GR",
            "disposition": "RETAINED",
        }
    ),
    base(
        {
            "countermodel_id": "CM3086_4_verdict",
            "obstruction": "EH dominance is asserted by notation rather than derived from parent action",
            "why_survives": "current corpus still needs sector variations and local scaling",
            "effect": "3086 must hand off to 3087 derivation/bound route",
            "disposition": "RETAINED_AS_RED_TEAM_GUARD",
        }
    ),
]

bridge_status_rows = [
    base(
        {
            "status_id": "BGS3086_0_source_side",
            "object": "Hilbert/source side",
            "current_status": "NARROWED_NOT_CLAIMED",
            "evidence": "3085 source-shadow classification and WEP sidecar",
            "next_requirement": "do not reopen WEP scoring until left-hand operator and source normalization are stable",
            "bridge_claim": "false",
        }
    ),
    base(
        {
            "status_id": "BGS3086_1_EH_left_hand",
            "object": "Einstein-Hilbert local LHS",
            "current_status": "PRIMARY_BLOCKER",
            "evidence": "EHD3086_5_current_verdict",
            "next_requirement": "prove residual-sector zero/suppression or keep explicit coefficient rows",
            "bridge_claim": "false",
        }
    ),
    base(
        {
            "status_id": "BGS3086_2_Newton_Poisson",
            "object": "Newton/Poisson limit",
            "current_status": "CONDITIONAL_BEHIND_EH_AND_SOURCE_NORMALIZATION",
            "evidence": "EHD3086_4_Newton_limit;OPC3086_6_source_normalization",
            "next_requirement": "derive weak-field EH limit and measured-G/source owner",
            "bridge_claim": "false",
        }
    ),
    base(
        {
            "status_id": "BGS3086_3_empirical_route",
            "object": "PPN/R10/clock/orbit empirical branch",
            "current_status": "COEFFICIENT_PACK_STAGED_NONCLAIM",
            "evidence": "OPC3086 rows; EBM3086 rows",
            "next_requirement": "convert residual operators into source-backed arena coefficients",
            "bridge_claim": "false",
        }
    ),
    base(
        {
            "status_id": "BGS3086_4_next",
            "object": "best next derivation",
            "current_status": "SECTOR_ACTION_VARIATION_AND_LOCAL_SCALING_SILENCE_IS_NEXT",
            "evidence": "RSS3086 residual-sector audit",
            "next_requirement": "3087 should vary each non-EH action block and derive scaling/bounds",
            "bridge_claim": "false",
        }
    ),
]

corpus_gate_rows = [
    base(
        {
            "gate_id": "CG3086_0_EH_dominance",
            "claim": "parent LHS is EH-dominated in the local branch",
            "gate_pass": "false",
            "reason": "sector zero/suppression theorem is not parent-signed",
        }
    ),
    base(
        {
            "gate_id": "CG3086_1_residual_silence",
            "claim": "all non-EH residual sectors vanish locally",
            "gate_pass": "false",
            "reason": "higher-derivative, projector, boundary, nonminimal, memory and source-normalization routes remain open",
        }
    ),
    base(
        {
            "gate_id": "CG3086_2_PPN",
            "claim": "MTS passes local PPN as GR",
            "gate_pass": "false",
            "reason": "PPN residual vector is not derived from operator coefficients",
        }
    ),
    base(
        {
            "gate_id": "CG3086_3_Newton",
            "claim": "MTS derives Newton/Poisson limit like GR derives Newton",
            "gate_pass": "false",
            "reason": "EH dominance and source normalization remain conditional",
        }
    ),
    base(
        {
            "gate_id": "CG3086_4_local_GR_promotion",
            "claim": "local GR/Newton branch is promoted",
            "gate_pass": "false",
            "reason": "3086 is a residual operator checkpoint, not a pass claim",
        }
    ),
]

score_blocker_rows = [
    base(
        {
            "blocker_id": "SBL3086_0_sector_variations",
            "blocks": "EH dominance",
            "missing": "variation certificate for each retained non-EH sector",
            "status": "BLOCKS_SCORE",
            "score_allowed": "false",
        }
    ),
    base(
        {
            "blocker_id": "SBL3086_1_local_scaling",
            "blocks": "residual suppression branch",
            "missing": "coefficient dimensions, local scale hierarchy and tolerance conversion",
            "status": "BLOCKS_SCORE",
            "score_allowed": "false",
        }
    ),
    base(
        {
            "blocker_id": "SBL3086_2_arena_maps",
            "blocks": "PPN/R10/clock/orbit empirical branch",
            "missing": "projection from operator coefficients to observable residual vectors",
            "status": "BLOCKS_SCORE",
            "score_allowed": "false",
        }
    ),
    base(
        {
            "blocker_id": "SBL3086_3_source_normalization",
            "blocks": "Newton/Poisson bridge",
            "missing": "measured-G/source-normalization owner",
            "status": "BLOCKS_SCORE",
            "score_allowed": "false",
        }
    ),
]

decision_rows = [
    base(
        {
            "decision_id": "DEC3086_0_EH_result",
            "decision": "EH_DOMINANCE_NOT_PARENT_PROVED",
            "reason": "the theorem shape is exact but each non-EH sector still needs a variation/silence/scaling certificate",
            "next_action": "retain DeltaE_munu operator pack",
        }
    ),
    base(
        {
            "decision_id": "DEC3086_1_operator_pack",
            "decision": "OPERATOR_COEFFICIENT_PACK_STAGED_NONCLAIM",
            "reason": "residual sectors are now explicit enough to become PPN/R10/clock/orbit rows once coefficients are sourced",
            "next_action": "derive sector variations before numeric scoring",
        }
    ),
    base(
        {
            "decision_id": "DEC3086_2_countermodels",
            "decision": "COUNTERMODELS_RETAINED",
            "reason": "small residuals, cancellations, boundary choices and source normalization can fake a GR pass if not controlled",
            "next_action": "use red-team guards in 3087",
        }
    ),
    base(
        {
            "decision_id": "DEC3086_3_best_next",
            "decision": "SECTOR_ACTION_VARIATION_AND_LOCAL_SCALING_SILENCE_IS_NEXT",
            "reason": "the least-handwavy route is to vary every retained non-EH action block and either silence it or derive its local scaling",
            "next_action": "3087-Y5-R2FR-sector-action-variation-and-local-scaling-silence-or-operator-bounds-under-AX1090.md",
        }
    ),
]

claim_rows = [
    base(
        {
            "claim_id": "CLAIM3086_0_EH_dominance",
            "claim": "local LHS is Einstein-Hilbert dominated",
            "claim_active": "false",
            "status": "NOT_CLAIMED",
            "reason": "non-EH sector zero/suppression theorem is missing",
        }
    ),
    base(
        {
            "claim_id": "CLAIM3086_1_Newton",
            "claim": "Newton/Poisson limit is derived",
            "claim_active": "false",
            "status": "NOT_CLAIMED",
            "reason": "EH dominance and source normalization remain conditional",
        }
    ),
    base(
        {
            "claim_id": "CLAIM3086_2_PPN_R10",
            "claim": "local PPN/R10/clock/orbit scores can run",
            "claim_active": "false",
            "status": "NOT_CLAIMED",
            "reason": "operator-to-observable residual maps are missing",
        }
    ),
    base(
        {
            "claim_id": "CLAIM3086_3_local_GR",
            "claim": "local GR/Newton recovery follows",
            "claim_active": "false",
            "status": "NOT_CLAIMED",
            "reason": "left-hand residuals and measured-G/source owner remain open",
        }
    ),
]

next_rows = [
    base(
        {
            "next_id": "NEXT3086_0_3087",
            "next_checkpoint": "3087-Y5-R2FR-sector-action-variation-and-local-scaling-silence-or-operator-bounds-under-AX1090.md",
            "script": "scripts/Y5_R2FR_sector_action_variation_and_local_scaling_silence_or_operator_bounds_under_AX1090_3087.py",
            "mission": "vary each retained non-EH sector and derive local zero/suppression conditions; otherwise convert it into a source-backed operator-bound row",
            "starting_equation": "DeltaE_munu=sum_i c_i O_i_munu with i in {higher_derivative, projector, boundary, nonminimal, memory_coframe, source_normalization}",
            "claim_policy": "no GR/Newton/PPN/R10 claim until every residual sector is parent-silent, scale-suppressed, or carried forward as a valid nonclaim coefficient with units and arena projection",
        }
    )
]

write_csv(OUTPUTS["sources"], source_register)
write_csv(OUTPUTS["eh_attempt"], eh_attempt_rows)
write_csv(OUTPUTS["sector_audit"], sector_rows)
write_csv(OUTPUTS["operator_pack"], operator_rows)
write_csv(OUTPUTS["empirical_map"], empirical_rows)
write_csv(OUTPUTS["countermodels"], countermodel_rows)
write_csv(OUTPUTS["bridge_status"], bridge_status_rows)
write_csv(OUTPUTS["corpus_gate"], corpus_gate_rows)
write_csv(OUTPUTS["score_blockers"], score_blocker_rows)
write_csv(OUTPUTS["decision"], decision_rows)
write_csv(OUTPUTS["claim_status"], claim_rows)
write_csv(OUTPUTS["next"], next_rows)

copy_csv(OUTPUTS["sector_audit"], BRANCH_OUTPUTS["sector_audit_copy"])
copy_csv(OUTPUTS["operator_pack"], BRANCH_OUTPUTS["operator_pack_copy"])
copy_csv(OUTPUTS["empirical_map"], BRANCH_OUTPUTS["empirical_map_copy"])
copy_csv(OUTPUTS["bridge_status"], BRANCH_OUTPUTS["bridge_status_copy"])
copy_csv(OUTPUTS["next"], BRANCH_OUTPUTS["next_copy"])

branch_rows = [
    base(
        {
            "copy_id": copy_id,
            "source_path": str(source_path),
            "copy_path": str(copy_path),
            "copy_exists": str(copy_path.exists()),
            "copy_parse_ok": str(csv_ok(copy_path)),
            "status": "BRANCH_COPY_READY_NONCLAIM" if copy_path.exists() else "BRANCH_COPY_MISSING",
        }
    )
    for copy_id, source_path, copy_path in [
        ("BR3086_0_sector_audit", OUTPUTS["sector_audit"], BRANCH_OUTPUTS["sector_audit_copy"]),
        ("BR3086_1_operator_pack", OUTPUTS["operator_pack"], BRANCH_OUTPUTS["operator_pack_copy"]),
        ("BR3086_2_empirical_map", OUTPUTS["empirical_map"], BRANCH_OUTPUTS["empirical_map_copy"]),
        ("BR3086_3_bridge_status", OUTPUTS["bridge_status"], BRANCH_OUTPUTS["bridge_status_copy"]),
        ("BR3086_4_next", OUTPUTS["next"], BRANCH_OUTPUTS["next_copy"]),
    ]
]
write_csv(OUTPUTS["branches"], branch_rows)

DOC.write_text("# 3086 - EH Dominance and Operator Residuals\n\nPreparing validation.\n", encoding="utf-8")

dotg_hash_after = file_hash(DOTG_TARGET)
generated_csvs = list(OUTPUTS.values()) + list(BRANCH_OUTPUTS.values())
generated_rows = (
    source_register
    + eh_attempt_rows
    + sector_rows
    + operator_rows
    + empirical_rows
    + countermodel_rows
    + bridge_status_rows
    + corpus_gate_rows
    + score_blocker_rows
    + decision_rows
    + claim_rows
    + next_rows
    + branch_rows
)
formalization_output_count = sum(1 for output_path in generated_csvs + [DOC] if under(output_path, FORMALIZATION))
required_attempt_ids = {
    "EHD3086_0_target",
    "EHD3086_1_zero_theorem",
    "EHD3086_2_suppression_theorem",
    "EHD3086_3_Bianchi_noether",
    "EHD3086_4_Newton_limit",
    "EHD3086_5_current_verdict",
}
required_sector_ids = {
    "RSS3086_0_higher_derivative",
    "RSS3086_1_projector",
    "RSS3086_2_boundary",
    "RSS3086_3_nonminimal",
    "RSS3086_4_memory_coframe",
    "RSS3086_5_source_normalization",
    "RSS3086_6_verdict",
}
required_operator_ids = {
    "OPC3086_0_total_DeltaE",
    "OPC3086_1_higher_derivative",
    "OPC3086_2_projector",
    "OPC3086_3_boundary",
    "OPC3086_4_nonminimal",
    "OPC3086_5_memory_coframe",
    "OPC3086_6_source_normalization",
}
required_empirical_ids = {
    "EBM3086_0_ppn_gamma_beta",
    "EBM3086_1_R10_Yukawa",
    "EBM3086_2_clocks",
    "EBM3086_3_orbits",
    "EBM3086_4_cosmology",
}
required_gate_ids = {
    "CG3086_0_EH_dominance",
    "CG3086_1_residual_silence",
    "CG3086_2_PPN",
    "CG3086_3_Newton",
    "CG3086_4_local_GR_promotion",
}
eh_verdict = next(row for row in eh_attempt_rows if row["attempt_id"] == "EHD3086_5_current_verdict")
sector_verdict = next(row for row in sector_rows if row["sector_id"] == "RSS3086_6_verdict")

validation_rows = [
    base(
        {
            "validation_id": "VAL3086_00_sources_exist",
            "passed": str(all(row["exists"] == "True" for row in source_register)),
            "requirement": "all cited source paths exist",
            "evidence": OUTPUTS["sources"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3086_01_sources_parse",
            "passed": str(all(row["parse_ok"] == "True" for row in source_register)),
            "requirement": "all cited CSV sources parse and markdown sources exist",
            "evidence": OUTPUTS["sources"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3086_02_csv_parse",
            "passed": str(all(csv_ok(output_path) for output_path in generated_csvs if output_path != OUTPUTS["validation"])),
            "requirement": "all generated and branch-copy CSVs parse cleanly before validation write",
            "evidence": "csv.DictReader parse check",
        }
    ),
    base(
        {
            "validation_id": "VAL3086_03_EH_attempt_complete",
            "passed": str(required_attempt_ids.issubset({row["attempt_id"] for row in eh_attempt_rows}) and not has_claim_true(eh_attempt_rows)),
            "requirement": "EH target, zero theorem, suppression theorem, Bianchi/Noether, Newton limit and verdict rows are present and nonclaim",
            "evidence": OUTPUTS["eh_attempt"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3086_04_EH_not_promoted",
            "passed": str(eh_verdict["current_status"] == "FAIL_CURRENT_PARENT_PROOF"),
            "requirement": "EH dominance remains unproved/nonclaim",
            "evidence": OUTPUTS["eh_attempt"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3086_05_residual_sectors_retained",
            "passed": str(required_sector_ids.issubset({row["sector_id"] for row in sector_rows}) and sector_verdict["current_status"] == "RESIDUAL_SECTORS_RETAINED_NONCLAIM"),
            "requirement": "all residual sectors are retained as nonclaim",
            "evidence": OUTPUTS["sector_audit"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3086_06_operator_pack_nonclaim",
            "passed": str(required_operator_ids.issubset({row["row_id"] for row in operator_rows}) and not has_claim_true(operator_rows)),
            "requirement": "operator coefficient pack covers total DeltaE and all retained sectors as nonclaim rows",
            "evidence": OUTPUTS["operator_pack"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3086_07_empirical_map_nonclaim",
            "passed": str(required_empirical_ids.issubset({row["map_id"] for row in empirical_rows}) and not has_claim_true(empirical_rows)),
            "requirement": "PPN, R10, clock, orbit and cosmology empirical maps remain nonclaim",
            "evidence": OUTPUTS["empirical_map"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3086_08_countermodels_retained",
            "passed": str(len(countermodel_rows) == 5 and not has_claim_true(countermodel_rows)),
            "requirement": "EH-dominance countermodel/red-team guard is retained",
            "evidence": OUTPUTS["countermodels"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3086_09_bridge_status_next",
            "passed": str(any(row["status_id"] == "BGS3086_4_next" and row["current_status"] == "SECTOR_ACTION_VARIATION_AND_LOCAL_SCALING_SILENCE_IS_NEXT" for row in bridge_status_rows)),
            "requirement": "GR bridge status selects sector variation/local scaling next",
            "evidence": OUTPUTS["bridge_status"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3086_10_current_gates_block",
            "passed": str(required_gate_ids.issubset({row["gate_id"] for row in corpus_gate_rows}) and all(row["gate_pass"] == "false" for row in corpus_gate_rows) and not has_claim_true(corpus_gate_rows)),
            "requirement": "all current corpus gates remain blocked/nonclaim",
            "evidence": OUTPUTS["corpus_gate"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3086_11_score_blockers_active",
            "passed": str(not has_claim_true(score_blocker_rows) and all(row["status"] == "BLOCKS_SCORE" for row in score_blocker_rows)),
            "requirement": "sector variation, local scaling, arena map and source-normalization blockers remain active",
            "evidence": OUTPUTS["score_blockers"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3086_12_no_claim_promoted",
            "passed": str(not has_claim_true(generated_rows)),
            "requirement": "no local GR, Newton, PPN, R10, clock, orbital or cosmology claim is promoted",
            "evidence": "claim field scan",
        }
    ),
    base(
        {
            "validation_id": "VAL3086_13_next_target_selected",
            "passed": str(next_rows[0]["next_checkpoint"].startswith("3087-Y5-R2FR-sector-action-variation")),
            "requirement": "next target selected",
            "evidence": OUTPUTS["next"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3086_14_branch_copies_exist",
            "passed": str(all(row["copy_exists"] == "True" and row["copy_parse_ok"] == "True" for row in branch_rows)),
            "requirement": "branch copies exist and parse",
            "evidence": OUTPUTS["branches"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3086_15_dotg_unchanged",
            "passed": str(dotg_hash_before == dotg_hash_after),
            "requirement": "P8_time_drift_residual_or_zero.csv is not modified",
            "evidence": f"{dotg_hash_before}->{dotg_hash_after}",
        }
    ),
    base(
        {
            "validation_id": "VAL3086_16_outputs_under_post_checkpoint",
            "passed": str(all(under(output_path, ROOT) for output_path in generated_csvs + [DOC])),
            "requirement": "all outputs are under post-checkpoint-work",
            "evidence": "path containment check",
        }
    ),
    base(
        {
            "validation_id": "VAL3086_17_no_formalization_outputs",
            "passed": str(formalization_output_count == 0),
            "requirement": "formalization-workbench modified-file count for 3086 outputs remains zero",
            "evidence": f"formalization_3086_output_paths={formalization_output_count}",
        }
    ),
    base(
        {
            "validation_id": "VAL3086_18_pycache_absent",
            "passed": str(not PYCACHE.exists()),
            "requirement": "scripts __pycache__ is absent at generator completion",
            "evidence": str(PYCACHE),
        }
    ),
    base(
        {
            "validation_id": "VAL3086_19_doc_written",
            "passed": str(DOC.exists()),
            "requirement": "checkpoint markdown document is written",
            "evidence": str(DOC),
        }
    ),
]

write_csv(OUTPUTS["validation"], validation_rows)

doc_text = f"""# 3086 - EH Dominance and Residual-Sector Silence or Operator Coefficient Pack

Status: `Y5_R2FR_3086_EH_dominance_not_proved_operator_pack_nonclaim`

Generated: `{RUN_UTC}`

## Verdict

3086 attacks the real GR-left-hand problem. Source-side cleanup is not enough: the parent field equation must reduce locally to Einstein-Hilbert plus controlled residuals.

The exact bridge form is:

`E_LHS = G_munu + Lambda g_munu + DeltaE_munu`

The current corpus does **not** parent-prove `DeltaE_munu = 0`, and it does not yet bound `DeltaE_munu` strongly enough for local GR, Newton, PPN, R10, clocks, or orbits. Therefore no local-GR/Newton claim is promoted.

The useful result is that the residual operator debt is now finite: higher-derivative, projector, boundary/reference, nonminimal, memory/coframe, and source-normalization sectors. Each must be varied and either theorem-silenced, scale-suppressed, or carried forward as a coefficient row.

## EH Dominance Theorem Attempt

{md_table(eh_attempt_rows, ["attempt_id", "claim_piece", "mathematical_form", "current_status", "remaining_gap"])}

## Residual-Sector Silence Audit

{md_table(sector_rows, ["sector_id", "sector", "operator_form", "current_status", "next_requirement"])}

## Operator Coefficient Pack

{md_table(operator_rows, ["row_id", "quantity", "symbolic_form", "source_status", "test_arenas"])}

## Empirical Bound Map

{md_table(empirical_rows, ["map_id", "arena", "residual_input", "required_output", "current_status"])}

## Countermodel Ledger

{md_table(countermodel_rows, ["countermodel_id", "obstruction", "effect", "disposition"])}

## GR Bridge Status

{md_table(bridge_status_rows, ["status_id", "object", "current_status", "next_requirement", "bridge_claim"])}

## Current Corpus Gate

{md_table(corpus_gate_rows, ["gate_id", "claim", "gate_pass", "reason"])}

## Score Blockers

{md_table(score_blocker_rows, ["blocker_id", "blocks", "missing", "status"])}

## Decision

{md_table(decision_rows, ["decision_id", "decision", "reason", "next_action"])}

## Claim Status

{md_table(claim_rows, ["claim_id", "claim", "claim_active", "status", "reason"])}

## Next Target

{md_table(next_rows, ["next_id", "next_checkpoint", "mission", "starting_equation", "claim_policy"])}

## Validation

{md_table(validation_rows, ["validation_id", "passed", "requirement", "evidence"])}

## Files

- Source register: `{OUTPUTS["sources"]}`
- EH dominance attempt: `{OUTPUTS["eh_attempt"]}`
- Residual-sector audit: `{OUTPUTS["sector_audit"]}`
- Operator coefficient pack: `{OUTPUTS["operator_pack"]}`
- Empirical bound map: `{OUTPUTS["empirical_map"]}`
- Countermodel ledger: `{OUTPUTS["countermodels"]}`
- GR bridge status: `{OUTPUTS["bridge_status"]}`
- Current corpus gate: `{OUTPUTS["corpus_gate"]}`
- Score blockers: `{OUTPUTS["score_blockers"]}`
- Claim status: `{OUTPUTS["claim_status"]}`
- Next target: `{OUTPUTS["next"]}`
- Validation: `{OUTPUTS["validation"]}`
- Branch copy: `{BRANCH_OUTPUTS["sector_audit_copy"]}`
- Branch copy: `{BRANCH_OUTPUTS["operator_pack_copy"]}`
- Branch copy: `{BRANCH_OUTPUTS["empirical_map_copy"]}`
- Branch copy: `{BRANCH_OUTPUTS["bridge_status_copy"]}`
- Branch copy: `{BRANCH_OUTPUTS["next_copy"]}`
"""

DOC.write_text(doc_text, encoding="utf-8")
remove_pycache()

print(f"Wrote {DOC}")
print(f"Wrote {OUTPUTS['validation']}")
print(f"Validation passed {sum(1 for row in validation_rows if row['passed'] == 'True')}/{len(validation_rows)}")
