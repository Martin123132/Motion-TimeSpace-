from __future__ import annotations

import csv
import hashlib
import re
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


RUN_STARTED_AT = datetime.now(timezone.utc)
RUN_UTC = RUN_STARTED_AT.isoformat()
ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
PARENT_ACTION = ROOT / "source-intake" / "parent-action"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
FORMALIZATION = PROJECT / "formalization-workbench"
PYCACHE = ROOT / "scripts" / "__pycache__"

CHECKPOINT = "3100"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC = ROOT / "3100-Y5-R2FR-parent-Hessian-and-tauPPN-extraction-for-cg-under-AX1090.md"

SOURCES: dict[str, dict[str, Any]] = {
    "SRC3100_00_3099_next": {
        "path": RESIDUALS / "P8_Y5_R2FR_3099_NEXT_TARGET.csv",
        "needles": ["NEXT3099_0_primary", "parent-Hessian-and-tauPPN-extraction"],
        "role": "3099 selects parent Hessian and tau_PPN extraction.",
    },
    "SRC3100_01_3099_doc": {
        "path": ROOT / "3099-Y5-R2FR-canonical-X-normalization-and-range-gate-for-cg-under-AX1090.md",
        "needles": ["alpha_eff_PPN", "Z_X", "tau_PPN"],
        "role": "3099 derives the invariant PPN-facing coupling and missing-input verdict.",
    },
    "SRC3100_02_3099_zx_gate": {
        "path": RESIDUALS / "P8_Y5_R2FR_3099_ZX_MX2_TAUPPN_INPUT_GATE.csv",
        "needles": ["ZMG3099_7_verdict", "FAIL_CURRENT_CLAIM_NORMALIZATION_RANGE_MISSING"],
        "role": "3099 explicit normalization/range/tau input gate.",
    },
    "SRC3100_03_3099_bound": {
        "path": RESIDUALS / "P8_Y5_R2FR_3099_CG_NORMALIZED_BOUND_ROW.csv",
        "needles": ["NGB3099_2_raw_cg_formula", "MISSING_ZX_TAUPPN_SPPN"],
        "role": "3099 normalized c_g bound row remains nonclaim.",
    },
    "SRC3100_04_3093_doc": {
        "path": ROOT / "3093-Y5-R2FR-parent-Xhat-owner-and-Hessian-ZX-MX2-range-or-alpha-source-row-under-AX1090.md",
        "needles": ["Current verdict", "Z_X", "M_X^2"],
        "role": "3093 current AX1090 parent owner/Hessian audit.",
    },
    "SRC3100_05_3093_hessian": {
        "path": RESIDUALS / "P8_Y5_R2FR_3093_PARENT_HESSIAN_AUDIT.csv",
        "needles": ["PHA3093_1_ZX_positive", "PHA3093_2_MX2_positive"],
        "role": "3093 Hessian input checklist.",
    },
    "SRC3100_06_3093_locks": {
        "path": RESIDUALS / "P8_Y5_R2FR_3093_FIELD_NORMALIZATION_LOCKS.csv",
        "needles": ["FNL3093_1_canonical_metric", "CLEAN_CONTRACT_NOT_SIGNED"],
        "role": "3093 field-normalization lock status.",
    },
    "SRC3100_07_3094_doc": {
        "path": ROOT / "3094-Y5-R2FR-parent-metric-ZXfX2-beta-eigenvalue-or-source-zero-return-under-AX1090.md",
        "needles": ["FAIL_CURRENT_CLAIM", "Z_X f_X^2"],
        "role": "3094 parent metric/eigenvalue route status.",
    },
    "SRC3100_08_3094_beta": {
        "path": RESIDUALS / "P8_Y5_R2FR_3094_BETA_EIGENVALUE_ATTEMPT.csv",
        "needles": ["BE3094_4_verdict", "no parent-signed spectrum exists"],
        "role": "3094 beta/range eigenvalue ownership failure.",
    },
    "SRC3100_09_1030_doc": {
        "path": ROOT / "1030-Y5-R10-single-public-metric-parent-action-derivation-or-cg-provenance-gate.md",
        "needles": ["CPG1030_3_tau_PPN", "MISSING_PPN_RESPONSE_MATRIX"],
        "role": "1030 tau_PPN and single-public-metric zero-route provenance.",
    },
    "SRC3100_10_1030_provenance": {
        "path": RESIDUALS / "P8_Y5_R10_1030_CG_PROVENANCE_GATE_BINDING.csv",
        "needles": ["CPG1030_3_tau_PPN", "MISSING_PPN_RESPONSE_MATRIX"],
        "role": "1030 machine-readable tau_PPN provenance gate.",
    },
    "SRC3100_11_3098_assumptions": {
        "path": RESIDUALS / "P8_Y5_R2FR_3098_SCALAR_TENSOR_ASSUMPTION_GATE.csv",
        "needles": ["AST3098_5_verdict", "FAIL_CURRENT_CLAIM"],
        "role": "3098 scalar-tensor assumption gate.",
    },
}

SCAN_PATHS = [
    SOURCES["SRC3100_01_3099_doc"]["path"],
    SOURCES["SRC3100_02_3099_zx_gate"]["path"],
    SOURCES["SRC3100_03_3099_bound"]["path"],
    SOURCES["SRC3100_04_3093_doc"]["path"],
    SOURCES["SRC3100_05_3093_hessian"]["path"],
    SOURCES["SRC3100_06_3093_locks"]["path"],
    SOURCES["SRC3100_07_3094_doc"]["path"],
    SOURCES["SRC3100_08_3094_beta"]["path"],
    SOURCES["SRC3100_09_1030_doc"]["path"],
    SOURCES["SRC3100_10_1030_provenance"]["path"],
    SOURCES["SRC3100_11_3098_assumptions"]["path"],
]

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_3100_SOURCE_REGISTER.csv",
    "scan": RESIDUALS / "P8_Y5_R2FR_3100_PARENT_INPUT_EXTRACTION_SCAN.csv",
    "contract": RESIDUALS / "P8_Y5_R2FR_3100_PARENT_ACTION_CONTRACT_REQUIRED.csv",
    "tau_contract": RESIDUALS / "P8_Y5_R2FR_3100_TAUPPN_RESPONSE_CONTRACT.csv",
    "cg_status": RESIDUALS / "P8_Y5_R2FR_3100_CG_SOURCE_ROW_STATUS.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_3100_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_3100_NEXT_TARGET.csv",
    "copies": RESIDUALS / "P8_Y5_R2FR_3100_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_3100_VALIDATION.csv",
}

BRANCH_COPIES = {
    OUTPUTS["scan"]: PARENT_ACTION / "parent_Hessian_tauPPN_extraction_scan_3100_NO_SOURCE_VALUES.csv",
    OUTPUTS["contract"]: PARENT_ACTION / "parent_action_contract_required_for_cg_3100_NOT_SIGNED.csv",
    OUTPUTS["tau_contract"]: PARENT_ACTION / "tauPPN_response_contract_3100_NOT_SIGNED.csv",
    OUTPUTS["cg_status"]: LOCAL_BOUNDS / "cg_source_row_status_3100_NONCLAIM.csv",
    OUTPUTS["next"]: RAB_QUEUE / "JR3100_single_public_metric_or_finite_coupling_choice_NEXT_NONCLAIM.csv",
}

NUMERIC_PATTERNS = {
    "Z_X": re.compile(r"(?<![A-Za-z0-9_])Z_X\s*(?:=|:=)\s*([-+]?\d+(?:\.\d+)?(?:[eE][-+]?\d+)?)"),
    "M_X^2": re.compile(r"(?<![A-Za-z0-9_])M_X\^2\s*(?:=|:=)\s*([-+]?\d+(?:\.\d+)?(?:[eE][-+]?\d+)?)"),
    "tau_PPN": re.compile(r"(?<![A-Za-z0-9_])tau_PPN\s*(?:=|:=)\s*([-+]?\d+(?:\.\d+)?(?:[eE][-+]?\d+)?)"),
    "S_PPN": re.compile(r"(?<![A-Za-z0-9_])S_PPN\s*(?:=|:=)\s*([-+]?\d+(?:\.\d+)?(?:[eE][-+]?\d+)?)"),
}

REJECT_CONTEXT = [
    "ILLUSTRATIVE",
    "conditional scalar-tensor limit only",
    "if lambda_X",
    "not MTS claim",
    "not yet",
    "MISSING",
    "NOT_SIGNED",
    "FAIL_CURRENT_CLAIM",
    "lambda_X=infinity",
    "M_X^2=0 or",
    "massless",
]


def base_row() -> dict[str, Any]:
    return {
        "checkpoint": CHECKPOINT,
        "branch_id": BRANCH_ID,
        "timestamp_utc": RUN_UTC,
        "score_ready": False,
        "valid_prediction_row": False,
        "valid_for_claim": False,
        "claim_allowed": False,
    }


def with_base(row: dict[str, Any]) -> dict[str, Any]:
    merged = base_row()
    merged.update(row)
    return merged


def ensure_dirs() -> None:
    for path in [RESIDUALS, LOCAL_BOUNDS, PARENT_ACTION, RAB_QUEUE]:
        path.mkdir(parents=True, exist_ok=True)


def remove_pycache() -> None:
    if PYCACHE.exists():
        resolved = PYCACHE.resolve()
        if str(resolved).startswith(str(ROOT.resolve())):
            shutil.rmtree(resolved)


def sha256(path: Path) -> str:
    if not path.exists() or not path.is_file():
        return ""
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def csv_parses(path: Path) -> bool:
    try:
        csv_rows(path)
    except Exception:
        return False
    return True


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def source_register() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source_id, spec in SOURCES.items():
        path = Path(spec["path"])
        exists = path.exists()
        text = read_text(path) if exists else ""
        parses = csv_parses(path) if exists and path.suffix.lower() == ".csv" else exists
        missing = [needle for needle in spec["needles"] if needle not in text]
        rows.append(
            with_base(
                {
                    "source_id": source_id,
                    "path": str(path),
                    "exists": exists,
                    "parseable": parses,
                    "needles_found": not missing,
                    "missing_needles": ";".join(missing),
                    "sha256": sha256(path),
                    "role": spec["role"],
                }
            )
        )
    return rows


def line_contexts(token: str, pattern: re.Pattern[str] | None = None) -> tuple[int, list[str], list[str]]:
    symbolic_hits = 0
    accepted_numeric: list[str] = []
    rejected_numeric: list[str] = []
    for path in SCAN_PATHS:
        if not Path(path).exists():
            continue
        for line_no, line in enumerate(read_text(Path(path)).splitlines(), start=1):
            if token in line:
                symbolic_hits += line.count(token)
            if pattern is None:
                continue
            for match in pattern.finditer(line):
                context = f"{Path(path).name}:{line_no}:{line.strip()[:220]}"
                if any(marker in line for marker in REJECT_CONTEXT):
                    rejected_numeric.append(context)
                else:
                    accepted_numeric.append(context)
    return symbolic_hits, accepted_numeric, rejected_numeric


def scan_rows() -> list[dict[str, Any]]:
    specs = [
        {
            "scan_id": "EX3100_0_ZX",
            "target_input": "Z_X",
            "token": "Z_X",
            "requirement": "positive kinetic Hessian coefficient in the same parent Xhat normalization",
            "blocking_status": "MISSING_PARENT_NUMERIC_INPUT",
            "needed_for": "N_X=1/sqrt(Z_X) and raw c_g bound",
        },
        {
            "scan_id": "EX3100_1_MX2",
            "target_input": "M_X^2",
            "token": "M_X^2",
            "requirement": "signed mass/eigenvalue coefficient in the same parent Xhat Hessian",
            "blocking_status": "MISSING_PARENT_NUMERIC_INPUT",
            "needed_for": "lambda_X=sqrt(Z_X/M_X^2) range classification",
        },
        {
            "scan_id": "EX3100_2_tauPPN",
            "target_input": "tau_PPN",
            "token": "tau_PPN",
            "requirement": "weak-field response matrix mapping the MTS Xhat channel into measured PPN gamma",
            "blocking_status": "MISSING_PPN_RESPONSE_MATRIX",
            "needed_for": "turning alpha_eff_PPN into a c_g component bound",
        },
        {
            "scan_id": "EX3100_3_SPPN",
            "target_input": "S_PPN(lambda_X,environment)",
            "token": "S_PPN",
            "requirement": "range/screening/environment transfer function or unscreened long-range certificate",
            "blocking_status": "MISSING_RANGE_SCREENING_TRANSFER",
            "needed_for": "deciding Cassini vs R10/orbital arena",
        },
        {
            "scan_id": "EX3100_4_cross_sector_silence",
            "target_input": "cross-sector silence",
            "token": "cross-sector",
            "requirement": "disformal, non-Hilbert, boundary, support, and mixed Hessian terms zero or included in a vector envelope",
            "blocking_status": "MISSING_CROSS_SECTOR_SILENCE",
            "needed_for": "one-parameter c_g PPN claim",
        },
        {
            "scan_id": "EX3100_5_single_public_metric_zero",
            "target_input": "c_g=0 zero theorem",
            "token": "single-public-metric",
            "requirement": "parent action gives one public metric/coframe with no extra matter-frame slot",
            "blocking_status": "ZERO_ROUTE_TARGET_NOT_DERIVED",
            "needed_for": "silencing the local PPN coupling rather than bounding it",
        },
    ]
    rows: list[dict[str, Any]] = []
    for spec in specs:
        pattern = NUMERIC_PATTERNS.get(spec["token"])
        symbolic_hits, accepted_numeric, rejected_numeric = line_contexts(spec["token"], pattern)
        if accepted_numeric:
            status = "CANDIDATE_NUMERIC_HIT_REVIEW_REQUIRED"
        else:
            status = spec["blocking_status"]
        rows.append(
            with_base(
                {
                    "scan_id": spec["scan_id"],
                    "target_input": spec["target_input"],
                    "requirement": spec["requirement"],
                    "symbolic_hit_count": symbolic_hits,
                    "accepted_numeric_hit_count": len(accepted_numeric),
                    "accepted_numeric_contexts": " || ".join(accepted_numeric),
                    "rejected_numeric_hit_count": len(rejected_numeric),
                    "rejected_numeric_contexts": " || ".join(rejected_numeric),
                    "current_status": status,
                    "needed_for": spec["needed_for"],
                }
            )
        )
    return rows


def contract_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "contract_id": "PAC3100_0_same_variable_owner",
            "required_clause": "Declare a single parent field or quotient residual Xhat used by the Hessian, matter frame, source current, and local projection.",
            "minimal_formula": "Xhat = Xhat[Phi] with delta S_parent/dXhat, delta^2 S_parent/dXhat^2, and delta ln A_m/dXhat all referring to the same variable.",
            "current_status": "NOT_SIGNED",
            "why_it_matters": "prevents mixing a stability variable with a different coupling variable",
        },
        {
            "contract_id": "PAC3100_1_quadratic_hessian",
            "required_clause": "Give the local quadratic parent block with sign, units, and domain.",
            "minimal_formula": "S_X^(2)=(M_Pl^2/2) int sqrt(-g) [Z_X g^mn partial_m Xhat partial_n Xhat - M_X^2 Xhat^2] plus boundary terms",
            "current_status": "MISSING_ZX_MX2_VALUES",
            "why_it_matters": "fixes N_X and lambda_X without post-hoc fitting",
        },
        {
            "contract_id": "PAC3100_2_matter_frame_choice",
            "required_clause": "Choose either the zero route or the finite coupling route.",
            "minimal_formula": "zero: S_matter=Sbar[psi,e_pub(q(Phi))]; finite: g_m=A_g(Xhat)^2 g_E with c_g=d ln A_g/dXhat|0",
            "current_status": "CHOICE_NOT_PARENT_SIGNED",
            "why_it_matters": "determines whether c_g should vanish or be source-bounded",
        },
        {
            "contract_id": "PAC3100_3_source_current",
            "required_clause": "State whether J_X and boundary flux vanish, or provide source-normalized coefficient rows.",
            "minimal_formula": "delta_X S_matter = int sqrt(-g) J_X delta Xhat and boundary_X=0 or bounded",
            "current_status": "MISSING_SOURCE_CURRENT_OR_ZERO_THEOREM",
            "why_it_matters": "needed for no-hair/local-vacuum and fifth-force amplitude rows",
        },
        {
            "contract_id": "PAC3100_4_ppn_projection",
            "required_clause": "Define the weak-field response matrix from Xhat to PPN gamma/beta in a gauge and readout frame.",
            "minimal_formula": "delta gamma = M_gammaX delta Xhat_canonical + sum_i M_gammai delta u_i; tau_PPN := M_gammaX with no-cancellation envelope",
            "current_status": "MISSING_TAUPPN_RESPONSE_MATRIX",
            "why_it_matters": "needed to use Cassini as an MTS component bound",
        },
        {
            "contract_id": "PAC3100_5_range_transfer",
            "required_clause": "Provide S_PPN(lambda_X,environment) and arena transfer rules.",
            "minimal_formula": "S_PPN -> 1 for unscreened solar-long branch, Yukawa/finite-source kernel otherwise",
            "current_status": "MISSING_RANGE_SCREENING_TRANSFER",
            "why_it_matters": "prevents applying Cassini to a short-range or screened mode",
        },
        {
            "contract_id": "PAC3100_6_cross_sector_control",
            "required_clause": "Prove cross-Hessian/disformal/non-Hilbert/support/boundary terms are zero or include them in the PPN residual vector.",
            "minimal_formula": "alpha_eff_vector = (tau_X c_g/sqrt(Z_X), b_dis, q_nonH, Delta_support, Delta_boundary) with absolute envelope",
            "current_status": "MISSING_NO_CANCELLATION_VECTOR",
            "why_it_matters": "prevents hiding a failure or success in untracked components",
        },
        {
            "contract_id": "PAC3100_7_verdict",
            "required_clause": "All clauses above must be parent-signed before local-GR/PPN claims.",
            "minimal_formula": "claim_allowed = all(PAC3100_0..PAC3100_6 signed)",
            "current_status": "CONTRACT_REQUIRED_NOT_CURRENTLY_SIGNED",
            "why_it_matters": "sets the exact target for the next derivation attempt",
        },
    ]
    return [with_base(row) for row in rows]


def tau_contract_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "tau_id": "TRC3100_0_background",
            "required_piece": "background and perturbation variables",
            "equation": "g_mn=eta_mn+h_mn, Xhat=Xhat_0+delta Xhat, other residuals delta u_i",
            "current_status": "NOT_ASSEMBLED",
        },
        {
            "tau_id": "TRC3100_1_gauge_readout",
            "required_piece": "PPN gauge and measured-frame convention",
            "equation": "identify gamma from spatial curvature per unit Newtonian potential in the matter readout frame",
            "current_status": "NOT_ASSEMBLED",
        },
        {
            "tau_id": "TRC3100_2_response_matrix",
            "required_piece": "linearized response matrix",
            "equation": "delta gamma = M_gammaX delta Xhat_canonical + M_gammadis b_dis + M_gammanonH q_nonH + ...",
            "current_status": "MISSING_PPN_RESPONSE_MATRIX",
        },
        {
            "tau_id": "TRC3100_3_component_projection",
            "required_piece": "component projection for c_g",
            "equation": "tau_PPN := M_gammaX after canonical normalization and range transfer",
            "current_status": "MISSING_TAUPPN",
        },
        {
            "tau_id": "TRC3100_4_no_cancellation",
            "required_piece": "absolute envelope or zero proofs for every other component",
            "equation": "|delta gamma| <= |tau_X alpha_X| + |tau_dis b_dis| + |tau_nonH q_nonH| + ...",
            "current_status": "MISSING_NO_CANCELLATION_ENVELOPE",
        },
        {
            "tau_id": "TRC3100_5_verdict",
            "required_piece": "tau_PPN usable in a c_g bound",
            "equation": "requires TRC3100_0 through TRC3100_4",
            "current_status": "FAIL_CURRENT_CLAIM",
        },
    ]
    return [with_base(row) for row in rows]


def cg_status_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "row_id": "CGS3100_0_alpha_proxy_benchmark",
            "quantity": "alpha_PPN_proxy",
            "current_value": "0.005788015401465051",
            "source_status": "SOURCE_BACKED_BENCHMARK_FROM_3098",
            "claim_status": "BENCHMARK_ONLY_NONCLAIM",
            "next_action": "retain as comparator once tau/Z/range are sourced",
        },
        {
            "row_id": "CGS3100_1_ZX",
            "quantity": "Z_X",
            "current_value": "MISSING_SOURCE_BACKED_VALUE",
            "source_status": "symbolic formulas only",
            "claim_status": "BLOCKS_CG_BOUND",
            "next_action": "derive from parent Hessian or declare closure requirement",
        },
        {
            "row_id": "CGS3100_2_MX2",
            "quantity": "M_X^2",
            "current_value": "MISSING_SOURCE_BACKED_VALUE",
            "source_status": "symbolic formulas only",
            "claim_status": "BLOCKS_RANGE_CLASSIFICATION",
            "next_action": "derive from parent Hessian/eigenvalue spectrum or demote finite-range branch",
        },
        {
            "row_id": "CGS3100_3_tauPPN",
            "quantity": "tau_PPN",
            "current_value": "MISSING_RESPONSE_MATRIX",
            "source_status": "1030 provenance gate rejects tau_PPN",
            "claim_status": "BLOCKS_PPN_COMPONENT_BOUND",
            "next_action": "derive PPN residual vector or zero theorem",
        },
        {
            "row_id": "CGS3100_4_SPPN",
            "quantity": "S_PPN(lambda_X,environment)",
            "current_value": "MISSING_TRANSFER_FUNCTION",
            "source_status": "branch not range-classified",
            "claim_status": "BLOCKS_ARENA_SELECTION",
            "next_action": "derive lambda_X first, then screening/finite-source transfer",
        },
        {
            "row_id": "CGS3100_5_verdict",
            "quantity": "c_g local branch",
            "current_value": "NO_SOURCE_BACKED_COMPONENT_BOUND",
            "source_status": "contract written, inputs absent",
            "claim_status": "CLOSURE_ONLY_UNTIL_PARENT_ACTION_SIGNED",
            "next_action": "choose no-shadow zero theorem route or finite-coupling parent action route",
        },
    ]
    return [with_base(row) for row in rows]


def decision_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "decision_id": "DEC3100_0_no_numeric_extraction",
            "decision": "no parent-owned numeric/source row was extracted for Z_X, M_X^2, tau_PPN, or S_PPN",
            "rationale": "scanned current AX1090 gates contain symbolic laws and missing-input statuses only",
            "status": "adopted",
        },
        {
            "decision_id": "DEC3100_1_keep_cg_nonclaim",
            "decision": "do not promote direct c_g, PPN pass, or local-GR/Newton reduction",
            "rationale": "normalization, range, response, and cross-sector gates remain unsigned",
            "status": "adopted",
        },
        {
            "decision_id": "DEC3100_2_next_route_choice",
            "decision": "next attack should choose between c_g=0 no-shadow/public-metric theorem and finite-coupling parent action",
            "rationale": "this is the fork where local GR either emerges cleanly or the theory must own a fifth-force coupling",
            "status": "selected",
        },
    ]
    return [with_base(row) for row in rows]


def next_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "route_id": "NEXT3100_0_primary",
            "next_checkpoint": "3101-Y5-R2FR-single-public-metric-or-finite-coupling-parent-action-choice-under-AX1090.md",
            "script": "scripts/Y5_R2FR_single_public_metric_or_finite_coupling_parent_action_choice_under_AX1090_3101.py",
            "objective": "attempt the low-scrutiny zero route first: prove ordinary matter has only one public metric/coframe and no extra A_g(Xhat) slot; if not, require finite-coupling parent action rows",
            "selection_status": "selected",
            "success_condition": "either c_g=0/tau_PPN=0 is parent-signed, or finite c_g is explicitly demoted to source-row closure until Z_X/M_X^2/tau/S are supplied",
        },
        {
            "route_id": "NEXT3100_1_parallel",
            "next_checkpoint": "3101b-Y5-R2FR-PPN-residual-vector-no-cancellation-envelope-under-AX1090.md",
            "script": "scripts/Y5_R2FR_PPN_residual_vector_no_cancellation_envelope_under_AX1090_3101b.py",
            "objective": "build absolute PPN residual vector over c_g, disformal, non-Hilbert, support, boundary, and readout terms",
            "selection_status": "held",
            "success_condition": "Cassini/PPN can be applied as a vector envelope without cancellation assumptions",
        },
    ]
    return [with_base(row) for row in rows]


def copy_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source, target in BRANCH_COPIES.items():
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
        rows.append(
            with_base(
                {
                    "copy_id": f"COPY3100_{len(rows)}",
                    "source": str(source),
                    "target": str(target),
                    "target_exists": target.exists(),
                    "target_sha256": sha256(target),
                    "purpose": "nonclaim parent-action handoff copy",
                }
            )
        )
    return rows


def md_escape(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def md_table(rows: list[dict[str, Any]], columns: list[str]) -> list[str]:
    lines = [
        "| " + " | ".join(columns) + " |",
        "| " + " | ".join("---" for _ in columns) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(md_escape(row.get(column, "")) for column in columns) + " |")
    return lines


def validation_rows() -> list[dict[str, Any]]:
    validations: list[dict[str, Any]] = []

    def add(validation_id: str, check_pass: bool, detail: str, artifact: Path | str) -> None:
        validations.append(
            with_base(
                {
                    "validation_id": validation_id,
                    "check_pass": bool(check_pass),
                    "detail": detail,
                    "artifact": str(artifact),
                }
            )
        )

    sources = csv_rows(OUTPUTS["sources"])
    scan = csv_rows(OUTPUTS["scan"])
    contract = csv_rows(OUTPUTS["contract"])
    tau_contract = csv_rows(OUTPUTS["tau_contract"])
    cg_status = csv_rows(OUTPUTS["cg_status"])
    decisions = csv_rows(OUTPUTS["decision"])
    next_targets = csv_rows(OUTPUTS["next"])

    add("VAL3100_00_sources_csv", OUTPUTS["sources"].exists(), "source register exists", OUTPUTS["sources"])
    add("VAL3100_01_sources_exist", all(row["exists"] == "True" for row in sources), "every cited source path exists", OUTPUTS["sources"])
    add("VAL3100_02_sources_parse", all(row["parseable"] == "True" for row in sources), "every cited csv source parses", OUTPUTS["sources"])
    add("VAL3100_03_sources_needles", all(row["needles_found"] == "True" for row in sources), "all source needles found", OUTPUTS["sources"])
    add("VAL3100_04_doc_exists", DOC.exists(), "checkpoint doc exists", DOC)
    add("VAL3100_05_scan_parses", csv_parses(OUTPUTS["scan"]), "extraction scan parses", OUTPUTS["scan"])
    add("VAL3100_06_no_accepted_numeric_inputs", all(row["accepted_numeric_hit_count"] == "0" for row in scan if row["target_input"] in ["Z_X", "M_X^2", "tau_PPN", "S_PPN(lambda_X,environment)"]), "no accepted source-backed numeric parent inputs found", OUTPUTS["scan"])
    add("VAL3100_07_symbolic_hits_present", any(int(row["symbolic_hit_count"]) > 0 for row in scan if row["target_input"] == "Z_X") and any(int(row["symbolic_hit_count"]) > 0 for row in scan if row["target_input"] == "tau_PPN"), "symbolic structure was actually searched and found", OUTPUTS["scan"])
    add("VAL3100_08_tau_missing", any(row["target_input"] == "tau_PPN" and row["current_status"] == "MISSING_PPN_RESPONSE_MATRIX" for row in scan), "tau_PPN remains missing", OUTPUTS["scan"])
    add("VAL3100_09_contract_parses", csv_parses(OUTPUTS["contract"]), "parent action contract parses", OUTPUTS["contract"])
    add("VAL3100_10_contract_verdict", any(row["contract_id"] == "PAC3100_7_verdict" and row["current_status"] == "CONTRACT_REQUIRED_NOT_CURRENTLY_SIGNED" for row in contract), "parent action contract verdict blocks claim", OUTPUTS["contract"])
    add("VAL3100_11_tau_contract_parses", csv_parses(OUTPUTS["tau_contract"]), "tau_PPN contract parses", OUTPUTS["tau_contract"])
    add("VAL3100_12_tau_contract_verdict", any(row["tau_id"] == "TRC3100_5_verdict" and row["current_status"] == "FAIL_CURRENT_CLAIM" for row in tau_contract), "tau contract verdict blocks claim", OUTPUTS["tau_contract"])
    add("VAL3100_13_cg_status_parses", csv_parses(OUTPUTS["cg_status"]), "c_g source status parses", OUTPUTS["cg_status"])
    add("VAL3100_14_cg_status_nonclaim", any(row["row_id"] == "CGS3100_5_verdict" and row["claim_status"] == "CLOSURE_ONLY_UNTIL_PARENT_ACTION_SIGNED" for row in cg_status), "c_g verdict remains closure-only", OUTPUTS["cg_status"])
    add("VAL3100_15_all_cg_rows_nonclaim", all(row["valid_for_claim"] == "False" and row["claim_allowed"] == "False" for row in cg_status), "all c_g status rows are nonclaim", OUTPUTS["cg_status"])
    add("VAL3100_16_decision_selected", any(row["decision_id"] == "DEC3100_2_next_route_choice" and row["status"] == "selected" for row in decisions), "next route decision selected", OUTPUTS["decision"])
    add("VAL3100_17_next_primary", any(row["route_id"] == "NEXT3100_0_primary" and row["selection_status"] == "selected" for row in next_targets), "primary next target selected", OUTPUTS["next"])
    add("VAL3100_18_branch_copies_exist", all(target.exists() for target in BRANCH_COPIES.values()), "all branch copies exist", OUTPUTS["copies"])
    add("VAL3100_19_branch_copies_parse", all(csv_parses(target) for target in BRANCH_COPIES.values()), "all branch copies parse", OUTPUTS["copies"])
    fw_hits = []
    if FORMALIZATION.exists():
        fw_hits = [
            path
            for path in FORMALIZATION.rglob("*3100*")
            if datetime.fromtimestamp(path.stat().st_mtime, timezone.utc) >= RUN_STARTED_AT
        ]
    add("VAL3100_20_formalization_untouched", len(fw_hits) == 0, "no formalization-workbench 3100 artifacts modified by this run", FORMALIZATION)
    add("VAL3100_21_pycache_removed", not PYCACHE.exists(), "scripts __pycache__ absent after run", PYCACHE)
    return validations


def write_doc(data: dict[str, list[dict[str, Any]]]) -> None:
    lines = [
        "# 3100 - Y5 R2FR parent Hessian and tau_PPN extraction for c_g under AX1090",
        "",
        "**Progress:** 3100 performs the extraction attempt selected by 3099. It scans the current AX1090 branch for parent-owned `Z_X`, `M_X^2`, `tau_PPN`, and `S_PPN` source values rather than treating symbolic formulas as claim-grade inputs.",
        "",
        "**Current verdict:** no source-backed numeric parent inputs were extracted. The corpus contains the right symbolic socket, but not the parent-signed coefficients or PPN response matrix needed to bind raw `c_g` or claim local GR/PPN success.",
        "",
        "**Claim ceiling:** no direct `c_g` component bound, PPN pass, local-GR/Newton reduction, R10 pass, GitHub action, or `formalization-workbench` edit is allowed from 3100.",
        "",
        "## Source Register",
        *md_table(data["sources"], ["source_id", "path", "exists", "parseable", "needles_found", "missing_needles", "role"]),
        "",
        "## Parent Input Extraction Scan",
        *md_table(data["scan"], ["scan_id", "target_input", "symbolic_hit_count", "accepted_numeric_hit_count", "rejected_numeric_hit_count", "current_status", "needed_for"]),
        "",
        "## Parent Action Contract Required",
        *md_table(data["contract"], ["contract_id", "required_clause", "minimal_formula", "current_status", "why_it_matters"]),
        "",
        "## tau_PPN Response Contract",
        *md_table(data["tau_contract"], ["tau_id", "required_piece", "equation", "current_status"]),
        "",
        "## c_g Source Row Status",
        *md_table(data["cg_status"], ["row_id", "quantity", "current_value", "source_status", "claim_status", "next_action"]),
        "",
        "## Decision Ledger",
        *md_table(data["decision"], ["decision_id", "decision", "rationale", "status"]),
        "",
        "## Next Target",
        *md_table(data["next"], ["route_id", "next_checkpoint", "script", "objective", "selection_status", "success_condition"]),
        "",
        "## Branch Copies",
        *md_table(data["copies"], ["copy_id", "source", "target", "target_exists", "purpose"]),
        "",
        "## Validation",
        *md_table(data["validation"], ["validation_id", "check_pass", "detail", "artifact"]),
        "",
    ]
    DOC.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    ensure_dirs()
    remove_pycache()

    data = {
        "sources": source_register(),
        "scan": scan_rows(),
        "contract": contract_rows(),
        "tau_contract": tau_contract_rows(),
        "cg_status": cg_status_rows(),
        "decision": decision_rows(),
        "next": next_rows(),
    }

    write_csv(OUTPUTS["sources"], data["sources"])
    write_csv(OUTPUTS["scan"], data["scan"])
    write_csv(OUTPUTS["contract"], data["contract"])
    write_csv(OUTPUTS["tau_contract"], data["tau_contract"])
    write_csv(OUTPUTS["cg_status"], data["cg_status"])
    write_csv(OUTPUTS["decision"], data["decision"])
    write_csv(OUTPUTS["next"], data["next"])

    data["copies"] = copy_rows()
    write_csv(OUTPUTS["copies"], data["copies"])

    remove_pycache()
    data["validation"] = []
    write_doc(data)
    data["validation"] = validation_rows()
    write_csv(OUTPUTS["validation"], data["validation"])
    write_doc(data)
    remove_pycache()

    passed = sum(1 for row in data["validation"] if row["check_pass"])
    total = len(data["validation"])
    print(f"3100 parent Hessian/tau_PPN extraction checkpoint written: {passed}/{total} validation checks passed")
    print(DOC)
    print(OUTPUTS["validation"])


if __name__ == "__main__":
    main()
