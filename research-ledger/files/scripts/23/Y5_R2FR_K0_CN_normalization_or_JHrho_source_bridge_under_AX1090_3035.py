from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


RUN_UTC = datetime.now(timezone.utc).isoformat()
ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
PARENT_ACTION = ROOT / "source-intake" / "parent-action"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
FORMALIZATION = PROJECT / "formalization-workbench"
PYCACHE = ROOT / "scripts" / "__pycache__"

CHECKPOINT = "3035"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"

DOC = ROOT / "3035-Y5-R2FR-K0-CN-normalization-or-JHrho-source-bridge-under-AX1090.md"

SOURCE_PATHS = {
    "SRC3035_00_3034_doc": ROOT / "3034-Y5-R2FR-Hcore-source-vertex-normalization-or-CpsiH-first-value-under-AX1090.md",
    "SRC3035_01_3034_tuple": RESIDUALS / "P8_Y5_R2FR_3034_CPSIH_COMPONENT_TUPLE_ROWS.csv",
    "SRC3035_02_3034_norm": RESIDUALS / "P8_Y5_R2FR_3034_HCORE_SOURCE_VERTEX_NORMALIZATION_AUDIT.csv",
    "SRC3035_03_3034_sign": RESIDUALS / "P8_Y5_R2FR_3034_SIGN_CONVENTION_AUDIT.csv",
    "SRC3035_04_3024_ansatz": RESIDUALS / "P8_Y5_R2FR_3024_MINIMAL_HCORE_ANSATZ.csv",
    "SRC3035_05_3026_extraction": RESIDUALS / "P8_Y5_R2FR_3026_SIGMAH_FPSI_EXTRACTION_CONTRACT.csv",
    "SRC3035_06_3027_template": RESIDUALS / "P8_Y5_R2FR_3027_PARAMETERIZED_KSCR_SOURCE_ROW_TEMPLATE.csv",
    "SRC3035_07_3029_K0": RESIDUALS / "P8_Y5_R2FR_3029_FIRST_COMPONENT_VALUE_ATTEMPT.csv",
    "SRC3035_08_3017_ward": RESIDUALS / "P8_Y5_R2FR_3017_SOURCE_CURRENT_WARD_OWNER_ATTEMPT.csv",
    "SRC3035_09_3008_coupling": RESIDUALS / "P8_Y5_R2FR_3008_COUPLING_GUARD_ROWS.csv",
    "SRC3035_10_2921_pg": RESIDUALS / "P8_Y5_R2FR_2921_POISSON_GAUSS_ORBITAL_BRIDGE_AUDIT.csv",
    "SRC3035_11_2921_mass": RESIDUALS / "P8_Y5_R2FR_2921_PARENT_SOURCE_MASS_IDENTITY_AUDIT.csv",
    "SRC3035_12_1720_JH": RESIDUALS / "P8_Y5_PARENT_QLOC_1720_JH_CURRENT_DEFINITION_THEOREM.csv",
    "SRC3035_13_2180_glue": RESIDUALS / "P8_Y5_PARENT_QLOC_2180_PIM_JH_MASS_CURRENT_GLUE_AUDIT.csv",
    "SRC3035_14_2584_flux": RESIDUALS / "P8_Y5_PIM_JH_FLUX_2584_EXACT_OBSTRUCTION_VECTOR.csv",
}

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_3035_SOURCE_REGISTER.csv",
    "ratio_proof": RESIDUALS / "P8_Y5_R2FR_3035_RATIO_PROOF_ATTEMPT.csv",
    "normalization_reduction": RESIDUALS / "P8_Y5_R2FR_3035_K0_CN_NORMALIZATION_REDUCTION_AUDIT.csv",
    "source_bridge": RESIDUALS / "P8_Y5_R2FR_3035_JHRHO_SOURCE_BRIDGE_AUDIT.csv",
    "countermodels": RESIDUALS / "P8_Y5_R2FR_3035_RATIO_COUNTERMODEL_LEDGER.csv",
    "finite_contract": RESIDUALS / "P8_Y5_R2FR_3035_XIH_FINITE_RESIDUAL_CONTRACT.csv",
    "gates": RESIDUALS / "P8_Y5_R2FR_3035_PROMOTION_GATES.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_3035_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_3035_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_3035_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_3035_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "ratio_copy": PARENT_ACTION / "XiH_ratio_proof_attempt_3035_NOT_SIGNED.csv",
    "normalization_copy": PARENT_ACTION / "K0_CN_normalization_reduction_3035_NONCLAIM.csv",
    "source_bridge_copy": LOCAL_BOUNDS / "JHrho_source_bridge_audit_3035_NONCLAIM.csv",
    "finite_contract_copy": LOCAL_BOUNDS / "XiH_finite_residual_contract_3035_NONCLAIM.csv",
    "queue_copy": RAB_QUEUE / "JR3035_SOURCE_READOUT_LOCK_OR_XIH_FINITE_ROW_NEXT_NONCLAIM.csv",
}

for path in list(OUTPUTS.values()) + list(BRANCH_OUTPUTS.values()) + [DOC]:
    path.parent.mkdir(parents=True, exist_ok=True)


def rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def as_str(value: Any) -> str:
    return "" if value is None else str(value)


def boolish(value: Any) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes", "pass", "passed"}


def under(path: Path, parent: Path) -> bool:
    try:
        path.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


def base(row: dict[str, Any]) -> dict[str, Any]:
    return {
        **row,
        "checkpoint": CHECKPOINT,
        "branch_id": BRANCH_ID,
        "control_only": True,
        "score_ready": False,
        "valid_prediction_row": False,
        "valid_for_claim": False,
        "claim_allowed": False,
        "generated_utc": RUN_UTC,
    }


def write_csv(path: Path, output_rows: list[dict[str, Any]]) -> None:
    fieldnames: list[str] = []
    for output_row in output_rows:
        for key in output_row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(output_rows)


def csv_ok(path: Path) -> bool:
    try:
        rows(path)
        return True
    except Exception:
        return False


def md_table(output_rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    divider = "| " + " | ".join("---" for _ in columns) + " |"
    table_lines = [header, divider]
    for output_row in output_rows:
        cells = [
            as_str(output_row.get(column, "")).replace("\n", " ").replace("|", "\\|")
            for column in columns
        ]
        table_lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(table_lines)


source_roles = {
    "SRC3035_00_3034_doc": "3034 handoff: C_psiH formula sharpened, tuple unsigned",
    "SRC3035_01_3034_tuple": "JHrho, C_N, K0 and sign tuple rows",
    "SRC3035_02_3034_norm": "source-inclusive Hcore variation",
    "SRC3035_03_3034_sign": "relative sign blockers",
    "SRC3035_04_3024_ansatz": "conditional Hcore source block",
    "SRC3035_05_3026_extraction": "K0 definition through kinetic trace",
    "SRC3035_06_3027_template": "parameterized Hcore density template",
    "SRC3035_07_3029_K0": "K0 absorption convention attempt",
    "SRC3035_08_3017_ward": "source-current Ward owner attempt",
    "SRC3035_09_3008_coupling": "coupling guard rows",
    "SRC3035_10_2921_pg": "conditional Poisson/Gauss coefficient",
    "SRC3035_11_2921_mass": "parent source-mass identity audit",
    "SRC3035_12_1720_JH": "observed Hilbert current definition theorem attempt",
    "SRC3035_13_2180_glue": "PiM/JH mass-current glue audit",
    "SRC3035_14_2584_flux": "exact measured-GM obstruction vector",
}

source_register = [
    base(
        {
            "source_id": source_id,
            "local_path": str(path),
            "exists": path.exists(),
            "role": source_roles[source_id],
            "status": "PRESENT" if path.exists() else "MISSING_LOCAL_SOURCE",
        }
    )
    for source_id, path in SOURCE_PATHS.items()
]

ratio_rows = [
    base(
        {
            "ratio_id": "RATIO3035_0_define_XiH",
            "claim_piece": "physical Hcore source ratio",
            "formal_statement": "Xi_H := -JHrho/(C_N K0)",
            "result": "DEFINED_FROM_3034",
            "derivation_status": "FORMULA_SHARP_NONCLAIM",
            "missing_for_claim": "MISSING_JHrho; MISSING_C_N_K0_PRODUCT; MISSING_SIGN; MISSING_UNITS",
            "source_path": str(SOURCE_PATHS["SRC3035_01_3034_tuple"]),
        }
    ),
    base(
        {
            "ratio_id": "RATIO3035_1_rewrite_Asource",
            "claim_piece": "A_source coefficient ratio",
            "formal_statement": "A_source = Xi_H/C_WH + residual_boundary_source terms",
            "result": "REDUCES_TO_RATIO_PLUS_RESIDUALS",
            "derivation_status": "CONDITIONAL_ON_3031_3034",
            "missing_for_claim": "MISSING_C_WH_PARENT_OWNER; MISSING_RESIDUAL_ZERO_OR_BOUND",
            "source_path": str(SOURCE_PATHS["SRC3035_10_2921_pg"]),
        }
    ),
    base(
        {
            "ratio_id": "RATIO3035_2_unity_condition",
            "claim_piece": "local-GR first-order source normalization",
            "formal_statement": "A_source=1 iff Xi_H=C_WH, i.e. JHrho = -C_N K0 C_WH up to sign convention",
            "result": "EXACT_CONDITION_NOT_THEOREM",
            "derivation_status": "EQUIVALENCE_ONLY",
            "missing_for_claim": "MISSING_PARENT_ACTION_NORMALIZATION_THEOREM",
            "source_path": str(SOURCE_PATHS["SRC3035_00_3034_doc"]),
        }
    ),
    base(
        {
            "ratio_id": "RATIO3035_3_readout_lock",
            "claim_piece": "field rescaling guard",
            "formal_statement": "psi_N=-log(N) fixes the physical field scale, so Xi_H cannot be set to C_WH by a free psi rescaling unless the readout map is changed too",
            "result": "GAUGE_SHORTCUT_REJECTED",
            "derivation_status": "READOUT_LOCK_REQUIRED",
            "missing_for_claim": "MISSING_PARENT_READOUT_LOCK_TO_OBSERVED_LAPSE",
            "source_path": str(SOURCE_PATHS["SRC3035_04_3024_ansatz"]),
        }
    ),
    base(
        {
            "ratio_id": "RATIO3035_4_K0_absorption",
            "claim_piece": "K0/C_N redundancy",
            "formal_statement": "if K0>0 is branch-constant, define C_H0:=C_N K0 and write Xi_H=-JHrho/C_H0",
            "result": "REDUCES_COMPONENT_COUNT_NOT_RATIO",
            "derivation_status": "CONDITIONAL_NORMALIZATION_SIMPLIFICATION",
            "missing_for_claim": "MISSING_K0_POSITIVITY_AND_CONSTANCY; MISSING_C_H0_OWNER",
            "source_path": str(SOURCE_PATHS["SRC3035_07_3029_K0"]),
        }
    ),
    base(
        {
            "ratio_id": "RATIO3035_5_source_current_route",
            "claim_piece": "JHrho source bridge",
            "formal_statement": "J_H=JHrho rho_H must be the same ordinary Hilbert/source current used by Poisson/Gauss, with no source-only prefactor",
            "result": "ROUTE_IDENTIFIED_NOT_CLOSED",
            "derivation_status": "BLOCKED_BY_3017_1720_2180",
            "missing_for_claim": "MISSING_NO_SOURCE_PREFACTOR; MISSING_PARENT_MATTER_FUNCTOR; MISSING_WORLDTUBE_GLUE",
            "source_path": str(SOURCE_PATHS["SRC3035_08_3017_ward"]),
        }
    ),
    base(
        {
            "ratio_id": "RATIO3035_6_verdict",
            "claim_piece": "parent-owned Xi_H=C_WH theorem",
            "formal_statement": "same source current plus same boundary charge plus fixed readout would force Xi_H=C_WH",
            "result": "THEOREM_PACKAGE_VISIBLE_BUT_UNSIGNED",
            "derivation_status": "NOT_CLOSED",
            "missing_for_claim": "MISSING_SOURCE_READOUT_LOCK; MISSING_HAMILTONIAN_CHARGE_NORMALIZATION; MISSING_OMEGA_GM_ZERO",
            "source_path": str(SOURCE_PATHS["SRC3035_13_2180_glue"]),
        }
    ),
]

normalization_rows = [
    base(
        {
            "normalization_id": "NORM3035_0_C_H0_product",
            "object": "C_H0",
            "definition": "C_H0:=C_N K0",
            "status": "PRODUCT_TARGET_DEFINED",
            "gain": "moves arbitrary kinetic normalization into one product",
            "still_missing": "MISSING_C_H0_PARENT_VALUE_OR_UNITS",
        }
    ),
    base(
        {
            "normalization_id": "NORM3035_1_K0_convention",
            "object": "K0",
            "definition": "K0_norm=1 only after K0 positive, finite and branch-constant",
            "status": "CONVENTION_NOT_PHYSICAL_DERIVATION",
            "gain": "prevents double-counting K0 and C_N as independent physics",
            "still_missing": "MISSING_K0_POSITIVITY_AND_CONSTANCY",
        }
    ),
    base(
        {
            "normalization_id": "NORM3035_2_C_N_rescaling",
            "object": "C_N",
            "definition": "C_N absorbs K0 but cannot absorb JHrho once psi_N=-log(N) is the fixed physical readout",
            "status": "READOUT_LOCK_BLOCKS_GAUGE_FIX",
            "gain": "rejects the fake route C_N=JHrho by convention",
            "still_missing": "MISSING_PARENT_READOUT_LOCK",
        }
    ),
    base(
        {
            "normalization_id": "NORM3035_3_ratio_only",
            "object": "Xi_H",
            "definition": "Xi_H=-JHrho/C_H0",
            "status": "ONLY_RATIO_IS_LOCAL_NEWTON_INPUT",
            "gain": "3036 can attack one ratio instead of three loose components",
            "still_missing": "MISSING_RATIO_THEOREM_OR_FINITE_ROW",
        }
    ),
]

source_bridge_rows = [
    base(
        {
            "bridge_id": "JHB3035_0_Hilbert_current",
            "needed_clause": "J_H is the observed Hilbert current of ordinary matter",
            "current_evidence": "conditional definition only",
            "current_status": "NOT_PARENT_SIGNED",
            "blocks": "JHrho source-density bridge",
            "source_path": str(SOURCE_PATHS["SRC3035_12_1720_JH"]),
            "missing_for_claim": "MISSING_PARENT_MATTER_FUNCTOR; MISSING_OBSERVED_COFREFRAME_DESCENT",
        }
    ),
    base(
        {
            "bridge_id": "JHB3035_1_no_prefactor",
            "needed_clause": "no source-only/species prefactor can alter active source weight",
            "current_evidence": "countermodel survives",
            "current_status": "BLOCKED",
            "blocks": "universal JHrho",
            "source_path": str(SOURCE_PATHS["SRC3035_08_3017_ward"]),
            "missing_for_claim": "MISSING_NO_SOURCE_PREFACTOR_PARENT_CLAUSE",
        }
    ),
    base(
        {
            "bridge_id": "JHB3035_2_worldtube_glue",
            "needed_clause": "same compact source worldtube feeds Hcore and W/c^2",
            "current_evidence": "worldtube source glue missing",
            "current_status": "BLOCKED",
            "blocks": "same rho_H in both equations",
            "source_path": str(SOURCE_PATHS["SRC3035_13_2180_glue"]),
            "missing_for_claim": "MISSING_WORLDTUBE_SOURCE_GLUE",
        }
    ),
    base(
        {
            "bridge_id": "JHB3035_3_flux_closure",
            "needed_clause": "projected Hilbert mass flux closes in the compact exterior",
            "current_evidence": "Omega_GM obstruction retained",
            "current_status": "BLOCKED",
            "blocks": "constant measured-GM source denominator",
            "source_path": str(SOURCE_PATHS["SRC3035_14_2584_flux"]),
            "missing_for_claim": "MISSING_OMEGA_GM_ZERO_OR_BOUND",
        }
    ),
    base(
        {
            "bridge_id": "JHB3035_4_Gref_owner",
            "needed_clause": "G_ref is induced by parent charge normalization, not inserted from comparator GR",
            "current_evidence": "Poisson coefficient is conditional from EH-only premises",
            "current_status": "BLOCKED",
            "blocks": "claim Xi_H=C_WH",
            "source_path": str(SOURCE_PATHS["SRC3035_10_2921_pg"]),
            "missing_for_claim": "MISSING_PARENT_POISSON_GAUSS_BRIDGE; MISSING_NO_EH_IMPORT_CERTIFICATE",
        }
    ),
]

countermodel_rows = [
    base(
        {
            "countermodel_id": "CM3035_0_source_prefactor",
            "surviving_model": "S_source contains (1+epsilon_H) J_H psi_N while ordinary matter equations remain same",
            "effect_on_ratio": "Xi_H -> (1+epsilon_H) Xi_H",
            "why_not_excluded": "no-source-prefactor parent clause still missing",
            "source_path": str(SOURCE_PATHS["SRC3035_09_3008_coupling"]),
        }
    ),
    base(
        {
            "countermodel_id": "CM3035_1_readout_rescale",
            "surviving_model": "rescale psi_N in the action without proving the same rescaling in N=exp(-psi_N)",
            "effect_on_ratio": "apparent C_psiH can be changed by convention while observables do not follow",
            "why_not_excluded": "parent readout lock not signed",
            "source_path": str(SOURCE_PATHS["SRC3035_04_3024_ansatz"]),
        }
    ),
    base(
        {
            "countermodel_id": "CM3035_2_flux_obstruction",
            "surviving_model": "Pi_M J_H has compact-exterior flux or boundary/reference anomaly",
            "effect_on_ratio": "measured GM differs from Hcore source mass",
            "why_not_excluded": "Omega_GM zero/bound not filled",
            "source_path": str(SOURCE_PATHS["SRC3035_14_2584_flux"]),
        }
    ),
    base(
        {
            "countermodel_id": "CM3035_3_imported_Gref",
            "surviving_model": "use GR/EH Poisson coefficient as calibration while Hcore coupling remains independently weighted",
            "effect_on_ratio": "can force-looking A_source=1 by comparator import",
            "why_not_excluded": "no parent Poisson/Gauss coefficient owner",
            "source_path": str(SOURCE_PATHS["SRC3035_10_2921_pg"]),
        }
    ),
]

finite_rows = [
    base(
        {
            "contract_id": "XIH3035_0_XiH",
            "quantity": "Xi_H",
            "definition": "-JHrho/(C_N K0)",
            "needed_input": "finite source-backed ratio with units and sign",
            "current_value": "MISSING_RATIO_VALUE",
            "promotion_rule": "valid only if JHrho/C_H0 is parent-signed or externally source-backed with no hidden convention",
            "status": "NONCLAIM_INPUT_ROW_REQUIRED",
        }
    ),
    base(
        {
            "contract_id": "XIH3035_1_delta_Xi",
            "quantity": "delta_XiH",
            "definition": "Xi_H/(4*pi*G_ref/c^2)-1",
            "needed_input": "G_ref owner plus Xi_H row",
            "current_value": "MISSING_DELTA_VALUE",
            "promotion_rule": "score local GR only if delta_XiH=0 theorem or finite below arena bounds",
            "status": "NONCLAIM_RESIDUAL_ROW_REQUIRED",
        }
    ),
    base(
        {
            "contract_id": "XIH3035_2_Omega_GM",
            "quantity": "Omega_GM",
            "definition": "-Pi_M dJ_extra + [d,Pi_M]J_H + A_parent + tails",
            "needed_input": "theorem-zero or finite compact-exterior measured-GM obstruction",
            "current_value": "MISSING_ZERO_OR_BOUND",
            "promotion_rule": "must be zero/bounded before Xi_H can be compared to measured Newton mass",
            "status": "RETAINED_OBSTRUCTION",
        }
    ),
    base(
        {
            "contract_id": "XIH3035_3_source_readout_lock",
            "quantity": "source_readout_lock",
            "definition": "same parent source current, observed lapse readout and W/c^2 source density",
            "needed_input": "single parent clause or finite mismatch row",
            "current_value": "MISSING_LOCK",
            "promotion_rule": "without this, A_source=1 is a convention/calibration choice rather than a derivation",
            "status": "NEXT_TARGET",
        }
    ),
]

gates = [
    base(
        {
            "gate_id": "GATE3035_0_sources",
            "gate": "all cited source paths exist",
            "result": all(path.exists() for path in SOURCE_PATHS.values()),
            "notes": "3035 is source-backed to existing private corpus rows",
        }
    ),
    base(
        {
            "gate_id": "GATE3035_1_ratio_defined",
            "gate": "Xi_H ratio is defined",
            "result": any(row["formal_statement"] == "Xi_H := -JHrho/(C_N K0)" for row in ratio_rows),
            "notes": "ratio is defined but not claim-valid",
        }
    ),
    base(
        {
            "gate_id": "GATE3035_2_K0_CN_reduced",
            "gate": "K0 and C_N are reduced to C_H0 product",
            "result": any(row["object"] == "C_H0" for row in normalization_rows),
            "notes": "reduces loose components without fixing physics",
        }
    ),
    base(
        {
            "gate_id": "GATE3035_3_gauge_shortcut_rejected",
            "gate": "field-rescaling shortcut is explicitly rejected",
            "result": any(row["result"] == "GAUGE_SHORTCUT_REJECTED" for row in ratio_rows),
            "notes": "psi_N=-log(N) readout must be parent-locked",
        }
    ),
    base(
        {
            "gate_id": "GATE3035_4_source_bridge_closed",
            "gate": "JHrho bridge is parent-signed",
            "result": False,
            "notes": "blocked by source-prefactor, Hilbert current, worldtube and flux clauses",
        }
    ),
    base(
        {
            "gate_id": "GATE3035_5_no_claim_rows",
            "gate": "all generated rows remain nonclaim",
            "result": True,
            "notes": "no local-GR or Newton claim is made",
        }
    ),
]

decision_rows = [
    base(
        {
            "decision_id": "DEC3035_0_best_result",
            "question": "did 3035 derive the local source normalization?",
            "answer": "NO",
            "reason": "it reduces the target to Xi_H=-JHrho/(C_N K0), but the source bridge and readout/boundary normalization remain unsigned",
            "next_action": "attack the source-readout lock directly or fill a finite Xi_H residual row",
        }
    ),
    base(
        {
            "decision_id": "DEC3035_1_not_circling",
            "question": "what changed compared with 3034?",
            "answer": "the independent component hunt is demoted",
            "reason": "K0 and C_N only matter through C_H0, and the real physics is the single ratio Xi_H plus measured-GM obstruction",
            "next_action": "3036 should not re-audit K0 alone; it should prove the lock or quantify the mismatch",
        }
    ),
]

next_rows = [
    base(
        {
            "next_id": "NEXT3035_0_3036",
            "next_checkpoint": "3036-Y5-R2FR-source-readout-lock-or-XiH-finite-residual-under-AX1090.md",
            "script_stub": "scripts/Y5_R2FR_source_readout_lock_or_XiH_finite_residual_under_AX1090_3036.py",
            "mission": "prove that the same parent source current fixes psi_N=-log(N), W/c^2 and rho_H normalization, or stage finite nonclaim Xi_H/delta_XiH/Omega_GM rows",
            "starting_equation": "Xi_H=-JHrho/(C_N K0); A_source=Xi_H/C_WH plus residuals",
            "avoid_repeating": "do not re-run K0-only or JH-norm-only gates; use them as blockers and attack the source-readout lock",
            "claim_policy": "no local-GR/Newton/PPN claim until Xi_H=C_WH and Omega_GM=0 are parent-signed or bounded",
        }
    )
]

for output_key, output_rows in {
    "sources": source_register,
    "ratio_proof": ratio_rows,
    "normalization_reduction": normalization_rows,
    "source_bridge": source_bridge_rows,
    "countermodels": countermodel_rows,
    "finite_contract": finite_rows,
    "gates": gates,
    "decision": decision_rows,
    "next": next_rows,
}.items():
    write_csv(OUTPUTS[output_key], output_rows)

shutil.copyfile(OUTPUTS["ratio_proof"], BRANCH_OUTPUTS["ratio_copy"])
shutil.copyfile(OUTPUTS["normalization_reduction"], BRANCH_OUTPUTS["normalization_copy"])
shutil.copyfile(OUTPUTS["source_bridge"], BRANCH_OUTPUTS["source_bridge_copy"])
shutil.copyfile(OUTPUTS["finite_contract"], BRANCH_OUTPUTS["finite_contract_copy"])
shutil.copyfile(OUTPUTS["next"], BRANCH_OUTPUTS["queue_copy"])

branch_rows = [
    base(
        {
            "branch_copy_id": output_key,
            "path": str(path),
            "exists": path.exists(),
            "role": "branch-scoped nonclaim copy for source-readout-lock route",
            "status": "PRESENT_NONCLAIM_COPY" if path.exists() else "MISSING_BRANCH_COPY",
        }
    )
    for output_key, path in BRANCH_OUTPUTS.items()
]
write_csv(OUTPUTS["branches"], branch_rows)

if PYCACHE.exists():
    shutil.rmtree(PYCACHE)

csv_outputs = [path for output_key, path in OUTPUTS.items() if output_key != "validation"]
branch_outputs = list(BRANCH_OUTPUTS.values())
all_generated_paths = csv_outputs + branch_outputs + [DOC]
all_rows = (
    source_register
    + ratio_rows
    + normalization_rows
    + source_bridge_rows
    + countermodel_rows
    + finite_rows
    + gates
    + decision_rows
    + next_rows
    + branch_rows
)

validation_rows = [
    base(
        {
            "validation_id": "VAL3035_00_sources_exist",
            "passed": all(path.exists() for path in SOURCE_PATHS.values()),
            "requirement": "all cited source paths exist",
            "evidence": OUTPUTS["sources"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3035_01_csv_parse",
            "passed": all(csv_ok(path) for path in csv_outputs + branch_outputs),
            "requirement": "all generated CSV and branch-copy rows parse cleanly",
            "evidence": "csv.DictReader over generated outputs",
        }
    ),
    base(
        {
            "validation_id": "VAL3035_02_XiH_defined",
            "passed": any(row["formal_statement"] == "Xi_H := -JHrho/(C_N K0)" for row in ratio_rows),
            "requirement": "Xi_H ratio is explicitly defined",
            "evidence": OUTPUTS["ratio_proof"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3035_03_K0_CN_product",
            "passed": any(row["definition"] == "C_H0:=C_N K0" for row in normalization_rows),
            "requirement": "K0 and C_N reduced to C_H0 product",
            "evidence": OUTPUTS["normalization_reduction"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3035_04_gauge_shortcut_blocked",
            "passed": any(row["result"] == "GAUGE_SHORTCUT_REJECTED" for row in ratio_rows),
            "requirement": "field-rescaling/gauge shortcut is rejected",
            "evidence": OUTPUTS["ratio_proof"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3035_05_source_bridge_blockers",
            "passed": all(
                any(row["bridge_id"] == bridge_id and row["current_status"] in {"BLOCKED", "NOT_PARENT_SIGNED"} for row in source_bridge_rows)
                for bridge_id in ["JHB3035_0_Hilbert_current", "JHB3035_1_no_prefactor", "JHB3035_2_worldtube_glue", "JHB3035_3_flux_closure"]
            ),
            "requirement": "source bridge blockers remain explicit",
            "evidence": OUTPUTS["source_bridge"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3035_06_countermodels_retained",
            "passed": len(countermodel_rows) >= 4,
            "requirement": "live countermodels are retained instead of erased",
            "evidence": OUTPUTS["countermodels"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3035_07_finite_contract",
            "passed": all(
                any(row["quantity"] == quantity for row in finite_rows)
                for quantity in ["Xi_H", "delta_XiH", "Omega_GM", "source_readout_lock"]
            ),
            "requirement": "finite residual contract covers Xi_H, delta_XiH, Omega_GM and lock mismatch",
            "evidence": OUTPUTS["finite_contract"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3035_08_no_claim_rows",
            "passed": all(not boolish(row.get("valid_for_claim")) and not boolish(row.get("claim_allowed")) for row in all_rows),
            "requirement": "no 3035 row is valid for claim",
            "evidence": "generated row flags",
        }
    ),
    base(
        {
            "validation_id": "VAL3035_09_branch_copies",
            "passed": all(path.exists() and csv_ok(path) for path in branch_outputs),
            "requirement": "branch copies exist and parse",
            "evidence": OUTPUTS["branches"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3035_10_output_scope",
            "passed": all(under(path, ROOT) for path in all_generated_paths),
            "requirement": "all generated outputs are inside post-checkpoint-work",
            "evidence": str(ROOT),
        }
    ),
    base(
        {
            "validation_id": "VAL3035_11_formalization_untouched",
            "passed": sum(1 for path in all_generated_paths if under(path, FORMALIZATION)) == 0,
            "requirement": "formalization-workbench modified-file target count remains 0",
            "evidence": "formalization_output_hits=0",
        }
    ),
    base(
        {
            "validation_id": "VAL3035_12_next_target",
            "passed": bool(next_rows) and next_rows[0]["next_checkpoint"].startswith("3036-"),
            "requirement": "next target selected without repeating K0-only gate",
            "evidence": OUTPUTS["next"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3035_13_pycache_removed",
            "passed": not PYCACHE.exists(),
            "requirement": "scripts __pycache__ removed",
            "evidence": str(PYCACHE),
        }
    ),
]
write_csv(OUTPUTS["validation"], validation_rows)

doc = f"""# 3035 - K0-CN Normalization Or JHrho Source Bridge under AX1090

Status: `Y5_R2FR_3035_XiH_ratio_defined_source_readout_lock_unsigned_3036_next`

## Verdict

3035 tries to stop the coupling problem from splitting into three arbitrary knobs. The right target is not separately `JHrho`, `C_N`, and `K0`; it is the single physical ratio

`Xi_H := -JHrho/(C_N K0)`.

With `C_WH=4*pi*G_ref/c^2` on the conditional Poisson/Gauss branch,

`A_source = Xi_H/C_WH + residuals`.

So local Newton/GR first-order recovery needs `Xi_H=C_WH`, plus zero or bounded measured-GM/source-readout residuals.

This checkpoint does **not** prove that equality. It does prove something useful: `K0` can only be demoted to convention if it is positive and branch-constant, and even then `C_N K0` remains as the product `C_H0`. Also, `psi_N=-log(N)` blocks the fake shortcut where one rescales the field to force `A_source=1`; the readout scale is physical unless the parent action changes the lapse readout too.

The next bottleneck is therefore a source-readout lock: the same parent clause must own the Hcore source current, the observed lapse readout, the W/c^2 Poisson source density, and the measured-GM boundary normalization.

## Ratio Proof Attempt

{md_table(ratio_rows, ["ratio_id", "claim_piece", "formal_statement", "result", "derivation_status", "missing_for_claim"])}

## K0-CN Normalization Reduction

{md_table(normalization_rows, ["normalization_id", "object", "definition", "status", "gain", "still_missing"])}

## JHrho Source Bridge Audit

{md_table(source_bridge_rows, ["bridge_id", "needed_clause", "current_status", "blocks", "missing_for_claim"])}

## Live Countermodels

{md_table(countermodel_rows, ["countermodel_id", "surviving_model", "effect_on_ratio", "why_not_excluded"])}

## Finite Residual Contract

{md_table(finite_rows, ["contract_id", "quantity", "definition", "needed_input", "current_value", "status"])}

## Promotion Gates

{md_table(gates, ["gate_id", "gate", "result", "notes"])}

## Decision Ledger

{md_table(decision_rows, ["decision_id", "question", "answer", "reason", "next_action"])}

## Next Target

{md_table(next_rows, ["next_id", "next_checkpoint", "mission", "starting_equation", "avoid_repeating", "claim_policy"])}

## Source Register

{md_table(source_register, ["source_id", "exists", "role", "status"])}

## Validation

{md_table(validation_rows, ["validation_id", "passed", "requirement", "evidence"])}
"""

DOC.write_text(doc, encoding="utf-8")

print(f"Wrote {DOC}")
print(f"Wrote validation {OUTPUTS['validation']}")
print("3035 verdict: Xi_H ratio is now the target; source-readout lock remains unsigned.")
