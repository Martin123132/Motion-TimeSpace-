from __future__ import annotations

import csv
import hashlib
import math
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
FW = REPO / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
PYCACHE = ROOT / "scripts" / "__pycache__"

DOC = ROOT / "3336-Y5-R2FR-PPN-dominant-floor-source-acquisition-or-derivation-under-AX1090.md"

LOCAL_SOURCES = [
    {
        "source_id": "LSRC3336_0_3335_doc",
        "path": ROOT / "3335-Y5-R2FR-PPN-composite-tree-envelope-first-numeric-nonclaim-under-AX1090.md",
        "role": "dominant floor handoff",
    },
    {
        "source_id": "LSRC3336_1_3335_envelope",
        "path": OUT / "P8_Y5_R2FR_3335_REDUCED_PPN_ENVELOPE_SMOKE.csv",
        "role": "dominant term ranking from reduced smoke envelope",
    },
    {
        "source_id": "LSRC3336_2_3335_inputs",
        "path": OUT / "P8_Y5_R2FR_3335_REQUIRED_SOURCE_INPUTS.csv",
        "role": "missing real threshold, response, epsilon, composite, Gamma inputs",
    },
    {
        "source_id": "LSRC3336_3_3332_epsilon",
        "path": OUT / "P8_Y5_R2FR_3332_EPSILON_EFF_SPECIALIZATION.csv",
        "role": "tree epsilon_eff formula",
    },
    {
        "source_id": "LSRC3336_4_3332_composite",
        "path": OUT / "P8_Y5_R2FR_3332_COMPOSITE_PPN_SPECIALIZATION.csv",
        "role": "composite contact/commutator formula",
    },
    {
        "source_id": "LSRC3336_5_3331_appn",
        "path": OUT / "P8_Y5_R2FR_3331_APPN_BOUND.csv",
        "role": "A_PPN response formulas",
    },
    {
        "source_id": "LSRC3336_6_3331_cmetric",
        "path": OUT / "P8_Y5_R2FR_3331_CMETRIC_BOUND.csv",
        "role": "C_metric operator formulas",
    },
    {
        "source_id": "LSRC3336_7_3334_budget",
        "path": OUT / "P8_Y5_R2FR_3334_UPDATED_REDUCED_PPN_BUDGET.csv",
        "role": "Gamma-fork reduced PPN budget",
    },
]

WEB_SOURCES = [
    {
        "source_id": "WSRC3336_0_Cassini_Nature",
        "title": "A test of general relativity using radio links with the Cassini spacecraft",
        "url": "https://pubmed.ncbi.nlm.nih.gov/14508481/",
        "doi": "10.1038/nature01997",
        "year": "2003",
        "role": "primary Cassini PPN gamma source",
        "candidate_value": "gamma-1=(2.1±2.3)e-5",
    },
    {
        "source_id": "WSRC3336_1_Will_LRR",
        "title": "The Confrontation between General Relativity and Experiment",
        "url": "https://link.springer.com/article/10.12942/lrr-2014-4",
        "doi": "10.12942/lrr-2014-4",
        "year": "2014",
        "role": "review source for PPN gamma/beta context",
        "candidate_value": "Cassini gamma and reviewed beta/PPN constraints",
    },
]

OUTPUTS = {
    "sources": OUT / "P8_Y5_R2FR_3336_SOURCE_REGISTER.csv",
    "web": OUT / "P8_Y5_R2FR_3336_WEB_SOURCE_REGISTER.csv",
    "thresholds": OUT / "P8_Y5_R2FR_3336_PPN_THRESHOLD_CANDIDATES.csv",
    "rerank": OUT / "P8_Y5_R2FR_3336_DOMINANT_FLOOR_RERANK.csv",
    "tree": OUT / "P8_Y5_R2FR_3336_TREE_EPSILON_BOUND_CONTRACT.csv",
    "composite": OUT / "P8_Y5_R2FR_3336_COMPOSITE_CONTACT_COMMUTATOR_CONTRACT.csv",
    "response": OUT / "P8_Y5_R2FR_3336_RESPONSE_PRODUCT_ACQUISITION_CONTRACT.csv",
    "inputs": OUT / "P8_Y5_R2FR_3336_REQUIRED_SOURCE_INPUTS.csv",
    "gates": OUT / "P8_Y5_R2FR_3336_PROMOTION_GATES.csv",
    "decision": OUT / "P8_Y5_R2FR_3336_DECISION_LEDGER.csv",
    "next": OUT / "P8_Y5_R2FR_3336_NEXT_TARGET.csv",
    "validation": OUT / "P8_Y5_BRR545_3336_VALIDATION.csv",
}

RUN_UTC = datetime.now(timezone.utc).isoformat()
B_GAMMA_CASSINI_1SIGMA = 2.3e-5
B_GAMMA_CASSINI_CENTRAL_PLUS_SIGMA = 4.4e-5
B_BETA_REVIEW_WORKING = 1.2e-4
F_TREE = 0.30
F_COMP = 0.30
F_GAMMA = 0.10
F_MARGIN = 0.30
SIGMA_DPI_REFERENCE = 1.0e-3


def bool_str(value: bool) -> str:
    return "true" if value else "false"


def compact(value: Any, limit: int = 1800) -> str:
    text = " ".join(str(value).split())
    return text if len(text) <= limit else text[: limit - 3] + "..."


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: compact(row.get(key, "")) for key in fieldnames})


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def csv_parse_ok(path: Path) -> bool:
    try:
        read_csv(path)
        return True
    except Exception:
        return False


def text_parse_ok(path: Path) -> bool:
    try:
        path.read_text(encoding="utf-8", errors="replace")
        return True
    except Exception:
        return False


def parse_ok(path: Path) -> bool:
    if not path.exists():
        return False
    return csv_parse_ok(path) if path.suffix.lower() == ".csv" else text_parse_ok(path)


def sha256_prefix(path: Path) -> str:
    if not path.exists() or not path.is_file():
        return ""
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()[:16]


def snapshot_tree(path: Path) -> dict[str, tuple[int, int]]:
    if not path.exists():
        return {}
    result: dict[str, tuple[int, int]] = {}
    for item in path.rglob("*"):
        if item.is_file():
            try:
                stat = item.stat()
            except OSError:
                continue
            result[str(item.relative_to(path))] = (stat.st_size, stat.st_mtime_ns)
    return result


def changed_count(before: dict[str, tuple[int, int]], after: dict[str, tuple[int, int]]) -> int:
    keys = set(before) | set(after)
    return sum(1 for key in keys if before.get(key) != after.get(key))


def local_source_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source in LOCAL_SOURCES:
        path = source["path"]
        rows.append(
            {
                "source_id": source["source_id"],
                "kind": "local",
                "path_or_url": str(path),
                "exists": bool_str(path.exists()),
                "parse_ok": bool_str(parse_ok(path)),
                "sha256_prefix": sha256_prefix(path),
                "role": source["role"],
                "valid_for_claim": "false",
            }
        )
    return rows


def web_source_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source in WEB_SOURCES:
        rows.append(
            {
                "source_id": source["source_id"],
                "kind": "web",
                "title": source["title"],
                "url": source["url"],
                "doi": source["doi"],
                "year": source["year"],
                "role": source["role"],
                "candidate_value": source["candidate_value"],
                "recorded": "true",
                "valid_for_claim": "false",
            }
        )
    return rows


def threshold_candidate_rows() -> list[dict[str, Any]]:
    return [
        {
            "threshold_id": "PPN3336_0_gamma_Cassini_1sigma",
            "observable": "PPN gamma",
            "source_id": "WSRC3336_0_Cassini_Nature",
            "source_value": "gamma-1=(2.1±2.3)e-5",
            "working_bound": f"{B_GAMMA_CASSINI_1SIGMA:.6e}",
            "bound_type": "one_sigma_candidate_not_full_vector",
            "use": "replace B_PPN_smoke for gamma-slot sensitivity only",
            "valid_for_claim": "false",
        },
        {
            "threshold_id": "PPN3336_1_gamma_Cassini_abs_central_plus_sigma",
            "observable": "PPN gamma",
            "source_id": "WSRC3336_0_Cassini_Nature",
            "source_value": "|2.1e-5|+2.3e-5",
            "working_bound": f"{B_GAMMA_CASSINI_CENTRAL_PLUS_SIGMA:.6e}",
            "bound_type": "conservative_abs_central_plus_sigma_candidate",
            "use": "looser sanity check, not used as pass claim",
            "valid_for_claim": "false",
        },
        {
            "threshold_id": "PPN3336_2_beta_review_working",
            "observable": "PPN beta",
            "source_id": "WSRC3336_1_Will_LRR",
            "source_value": "reviewed beta constraints; working envelope only",
            "working_bound": f"{B_BETA_REVIEW_WORKING:.6e}",
            "bound_type": "review_working_candidate",
            "use": "do not use until beta projection is separately sourced",
            "valid_for_claim": "false",
        },
    ]


def load_envelope_rows() -> list[dict[str, str]]:
    return read_csv(OUT / "P8_Y5_R2FR_3335_REDUCED_PPN_ENVELOPE_SMOKE.csv")


def rerank_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in load_envelope_rows():
        total = float(row["R_total_smoke"])
        rows.append(
            {
                "scenario_id": row["scenario_id"],
                "dominant_term": row["dominant_term"],
                "R_total": f"{total:.6e}",
                "B_gamma_Cassini_candidate": f"{B_GAMMA_CASSINI_1SIGMA:.6e}",
                "candidate_pass_like": bool_str(total <= B_GAMMA_CASSINI_1SIGMA),
                "tree_residual": row["tree_residual"],
                "epsilon_composite": row["epsilon_composite"],
                "R_Gamma": row["R_Gamma"],
                "source_status": "RERANKED_WITH_REAL_GAMMA_CANDIDATE_NONCLAIM",
                "valid_for_claim": "false",
            }
        )
    return rows


def tree_contract_rows() -> list[dict[str, Any]]:
    response_values = [1.0, 1.0e6, 1.0e12, 1.0e16]
    rows: list[dict[str, Any]] = []
    for value in response_values:
        allowed_full = math.sqrt(B_GAMMA_CASSINI_1SIGMA / value)
        allowed_partition = math.sqrt(F_TREE * B_GAMMA_CASSINI_1SIGMA / value)
        rows.append(
            {
                "contract_id": f"TREE3336_resp_{value:.0e}",
                "quantity": "epsilon_eff_PPN",
                "A_PPN_times_Cmetric": f"{value:.6e}",
                "full_gamma_slot_allowance": f"{allowed_full:.6e}",
                "tree_partition_allowance": f"{allowed_partition:.6e}",
                "formula": "epsilon_eff <= sqrt(f_tree B_gamma/(A_PPN C_metric))",
                "derivation_status": "EXACT_FROM_REDUCED_BUDGET_AND_CASSINI_CANDIDATE",
                "still_needed": "source-bound A_PPN*C_metric and derive epsilon_bg*T_grad + boundary + anisotropy",
                "valid_for_claim": "false",
            }
        )
    rows.extend(
        [
            {
                "contract_id": "TREE3336_boundary_zero_attempt",
                "quantity": "boundary/aniso silence",
                "A_PPN_times_Cmetric": "symbolic",
                "full_gamma_slot_allowance": "",
                "tree_partition_allowance": "",
                "formula": "epsilon_boundary_PPN=epsilon_kernel_aniso_PPN=0 if the PPN patch is interior, isotropic, and the smoothing kernel commutes with the PPN projector",
                "derivation_status": "CONDITIONAL_ZERO_ATTEMPT",
                "still_needed": "prove PPN projection/kernel commutator is zero or bound it",
                "valid_for_claim": "false",
            },
            {
                "contract_id": "TREE3336_gradient_suppression_attempt",
                "quantity": "background gradient leakage",
                "A_PPN_times_Cmetric": "symbolic",
                "full_gamma_slot_allowance": "",
                "tree_partition_allowance": "",
                "formula": "epsilon_bg_PPN T_grad(lambda_PPN) <= sqrt(f_tree B_gamma/(A_PPN C_metric)) - epsilon_boundary - epsilon_kernel_aniso",
                "derivation_status": "ACQUISITION_CONTRACT",
                "still_needed": "ell_s/lambda_PPN, epsilon_bg_PPN, and local boundary/aniso bounds",
                "valid_for_claim": "false",
            },
        ]
    )
    return rows


def composite_contract_rows() -> list[dict[str, Any]]:
    comp_budget = F_COMP * B_GAMMA_CASSINI_1SIGMA
    delta_comm_allowance = comp_budget / SIGMA_DPI_REFERENCE
    contact_p2_ratio = math.sqrt(comp_budget)
    contact_p4_ratio = comp_budget ** 0.25
    return [
        {
            "contract_id": "COMP3336_0_total_budget",
            "quantity": "epsilon_composite_PPN",
            "formula": "epsilon_composite <= f_comp B_gamma",
            "candidate_bound": f"{comp_budget:.6e}",
            "derivation_status": "BUDGET_PARTITION_FROM_CASSINI_CANDIDATE",
            "still_needed": "replace f_comp policy with full PPN vector allocation",
            "valid_for_claim": "false",
        },
        {
            "contract_id": "COMP3336_1_commutator_bound",
            "quantity": "delta_comm_PPN",
            "formula": "delta_comm <= (f_comp B_gamma - other_composite_floors)/(A_1P sigma_Dpi)",
            "candidate_bound": f"{delta_comm_allowance:.6e}",
            "assumptions": f"A_1P=1, sigma_Dpi={SIGMA_DPI_REFERENCE:.1e}, other floors reserved as zero for first ceiling",
            "derivation_status": "EXACT_INEQUALITY_CEILING",
            "still_needed": "derive or source the PPN projector/smoothing commutator norm and sigma_Dpi",
            "valid_for_claim": "false",
        },
        {
            "contract_id": "COMP3336_2_contact_p2",
            "quantity": "ell_c/L_PPN for p_contact=2",
            "formula": "ell_c/L_PPN <= (f_comp B_gamma/C_contact)^(1/p_contact)",
            "candidate_bound": f"{contact_p2_ratio:.6e}",
            "assumptions": "C_contact=1, p_contact=2",
            "derivation_status": "CONTACT_SCALE_CEILING",
            "still_needed": "derive p_contact and C_contact from parent/local renormalization",
            "valid_for_claim": "false",
        },
        {
            "contract_id": "COMP3336_3_contact_p4",
            "quantity": "ell_c/L_PPN for p_contact=4",
            "formula": "ell_c/L_PPN <= (f_comp B_gamma/C_contact)^(1/p_contact)",
            "candidate_bound": f"{contact_p4_ratio:.6e}",
            "assumptions": "C_contact=1, p_contact=4",
            "derivation_status": "CONTACT_SCALE_CEILING",
            "still_needed": "derive p_contact and C_contact from parent/local renormalization",
            "valid_for_claim": "false",
        },
        {
            "contract_id": "COMP3336_4_two_particle_gap",
            "quantity": "m_gap_2pi r_PPN",
            "formula": "C_2P exp[-2 m_gap_2pi r_PPN] <= allocated two-particle budget",
            "candidate_bound": "m_gap_2pi r_PPN >= 0.5 ln(C_2P/B_2p)",
            "assumptions": "gapped two-particle tail; B_2p chosen from f_comp B_gamma",
            "derivation_status": "SPECTRAL_GAP_CONTRACT",
            "still_needed": "source two-particle spectral density/gap or prove absence",
            "valid_for_claim": "false",
        },
    ]


def response_contract_rows() -> list[dict[str, Any]]:
    return [
        {
            "contract_id": "RESP3336_0_A_PPN",
            "quantity": "A_PPN(q_U,gauge)",
            "formula": "A_PPN=max(A_gamma,A_beta,A_vector_tensor,A_gauge_residual)",
            "source_path": str(OUT / "P8_Y5_R2FR_3331_APPN_BOUND.csv"),
            "needed_action": "choose actual PPN observable slot, q_U convention, and gauge projector",
            "claim_gate": "numeric A_PPN with source-owned q_U/gauge map",
            "valid_for_claim": "false",
        },
        {
            "contract_id": "RESP3336_1_C_metric",
            "quantity": "C_metric(lambda)",
            "formula": "C_metric <= P_PPN^2 G_fix^2 W_src^2 D_readout^2 S_band^2 H_band(lambda) N_source",
            "source_path": str(OUT / "P8_Y5_R2FR_3331_CMETRIC_BOUND.csv"),
            "needed_action": "bound projection, gauge-fix, source-window, readout, smoothing, Hessian/Green, and source-normalization factors",
            "claim_gate": "numeric C_metric or conservative finite upper bound",
            "valid_for_claim": "false",
        },
        {
            "contract_id": "RESP3336_2_product",
            "quantity": "A_PPN*C_metric",
            "formula": "tree_residual=(A_PPN*C_metric) epsilon_eff^2",
            "source_path": "3335 placeholder grid",
            "needed_action": "replace placeholder product 1,1e6,1e12,1e16 with source-owned interval",
            "claim_gate": "interval upper bound small enough for derived epsilon_eff",
            "valid_for_claim": "false",
        },
    ]


def required_source_input_rows() -> list[dict[str, Any]]:
    return [
        {
            "input_id": "REQ3336_0_real_PPN_vector",
            "quantity": "full real PPN threshold vector",
            "current_status": "CASSINI_GAMMA_CANDIDATE_ONLY",
            "next_action": "add beta/preferred-frame/orbital thresholds before public local-GR claim",
            "valid_for_claim": "false",
        },
        {
            "input_id": "REQ3336_1_response_product",
            "quantity": "source-owned A_PPN*C_metric upper interval",
            "current_status": "ACQUISITION_CONTRACT_ONLY",
            "next_action": "derive q_U/gauge map and C_metric operator factors",
            "valid_for_claim": "false",
        },
        {
            "input_id": "REQ3336_2_tree_floors",
            "quantity": "epsilon_bg, T_grad, boundary, anisotropy",
            "current_status": "ALLOWABLE_BOUNDS_DERIVED_NOT_SOURCED",
            "next_action": "prove boundary/aniso silence or source numerical ceilings",
            "valid_for_claim": "false",
        },
        {
            "input_id": "REQ3336_3_composite_floors",
            "quantity": "delta_comm, sigma_Dpi, contact scaling, spectral gap",
            "current_status": "ALLOWABLE_BOUNDS_DERIVED_NOT_SOURCED",
            "next_action": "derive commutator/contact theorem or source conservative upper bounds",
            "valid_for_claim": "false",
        },
        {
            "input_id": "REQ3336_4_Gamma",
            "quantity": "Gamma_local or Gamma->K_solar map",
            "current_status": "LOWER_PRIORITY_UNLESS_GAMMA_LOCAL_SOURCED",
            "next_action": "retain Gamma fork while attacking dominant tree/composite floors",
            "valid_for_claim": "false",
        },
    ]


def promotion_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "GATE3336_0_real_gamma_candidate",
            "claim": "real PPN gamma threshold candidate is recorded",
            "passed": "true",
            "reason": "Cassini gamma source and DOI/URL are recorded",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3336_1_tree_contract",
            "claim": "tree epsilon_eff allowable bounds are derived from real gamma candidate",
            "passed": "true",
            "reason": "epsilon_eff ceilings are computed for response-product grid",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3336_2_composite_contract",
            "claim": "composite contact/commutator allowable bounds are derived",
            "passed": "true",
            "reason": "delta_comm and contact scale ceilings are computed from allocated gamma candidate budget",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3336_3_response_contract",
            "claim": "A_PPN*C_metric acquisition contract is explicit",
            "passed": "true",
            "reason": "A_PPN, C_metric, and product claim gates are separated",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3336_4_claim_ready",
            "claim": "PPN/local-GR branch is claim-ready",
            "passed": "false",
            "reason": "only gamma candidate is sourced; response, tree, composite, Gamma, and full PPN vector are not source-owned",
            "valid_for_claim": "false",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    rerank = rerank_rows()
    pass_count = len([row for row in rerank if row["candidate_pass_like"] == "true"])
    fail_count = len(rerank) - pass_count
    return [
        {
            "decision_id": "DEC3336_0",
            "question": "Did the real gamma candidate change the 3335 smoke story?",
            "answer": f"not materially: {pass_count} pass-like and {fail_count} fail-like scenarios remain",
            "reason": "Cassini gamma candidate is close to the earlier smoke ceiling; tree/composite/open-Gamma dominance pattern survives",
            "next_action": "derive/source dominant tree and composite floors",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC3336_1",
            "question": "What is the best next derivation?",
            "answer": "PPN projector/smoothing commutator and contact scaling",
            "reason": "these decide whether composite floors are naturally tiny or require external fitting",
            "next_action": "attempt commutator/contact theorem before more broad theory expansion",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC3336_2",
            "question": "What is the best next source acquisition?",
            "answer": "A_PPN*C_metric interval and full PPN threshold vector",
            "reason": "tree allowance changes as sqrt(1/(A_PPN*C_metric)); no claim is possible with placeholder response products",
            "next_action": "bind q_U/gauge and C_metric factors, then add real PPN beta/preferred-frame/orbital thresholds",
            "valid_for_claim": "false",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "target_doc": "3337-Y5-R2FR-PPN-commutator-contact-zero-or-bound-theorem-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3337_PPN_commutator_contact_zero_or_bound_theorem.py",
            "objective": "attempt to prove or bound the PPN projector/smoothing commutator and contact floor that dominate composite risk in 3335-3336",
            "must_include": "condition for delta_comm_PPN=0; contact scaling epsilon_contact <= C_contact(ell_c/L)^p; spectral-gap fallback; no PPN pass claim",
            "fallback_if_failed": "retain exact composite acquisition contract and move to response-product source bounding",
            "valid_for_claim": "false",
        }
    ]


def validate_outputs(formalization_before: dict[str, tuple[int, int]]) -> list[dict[str, Any]]:
    local_sources = local_source_rows()
    web_sources = web_source_rows()
    thresholds = threshold_candidate_rows()
    rerank = rerank_rows()
    tree = tree_contract_rows()
    composite = composite_contract_rows()
    response = response_contract_rows()
    gates = promotion_gate_rows()
    output_paths = [path for key, path in OUTPUTS.items() if key != "validation"]
    fw_changed = changed_count(formalization_before, snapshot_tree(FW))
    checks = [
        {
            "check_id": "VAL3336_0_local_sources_exist",
            "check": "all local source paths exist",
            "passed": all(row["exists"] == "true" for row in local_sources),
            "detail": "",
        },
        {
            "check_id": "VAL3336_1_local_sources_parse",
            "check": "all local source paths parse",
            "passed": all(row["parse_ok"] == "true" for row in local_sources),
            "detail": "",
        },
        {
            "check_id": "VAL3336_2_web_sources_recorded",
            "check": "web source URLs and DOIs are recorded",
            "passed": all(row["url"].startswith("https://") and row["doi"] for row in web_sources),
            "detail": "",
        },
        {
            "check_id": "VAL3336_3_outputs_parse",
            "check": "all 3336 non-validation outputs parse",
            "passed": all(path.exists() and parse_ok(path) for path in output_paths),
            "detail": "",
        },
        {
            "check_id": "VAL3336_4_threshold_candidate",
            "check": "Cassini gamma threshold candidate is present",
            "passed": any(row["threshold_id"] == "PPN3336_0_gamma_Cassini_1sigma" and row["working_bound"] == f"{B_GAMMA_CASSINI_1SIGMA:.6e}" for row in thresholds),
            "detail": "",
        },
        {
            "check_id": "VAL3336_5_rerank",
            "check": "3335 scenarios are reranked with real gamma candidate",
            "passed": len(rerank) == len(load_envelope_rows()) and any(row["candidate_pass_like"] == "false" for row in rerank),
            "detail": "",
        },
        {
            "check_id": "VAL3336_6_tree_contract",
            "check": "tree contract includes response-grid epsilon allowances and boundary/aniso acquisition",
            "passed": any(row["A_PPN_times_Cmetric"] == f"{1.0e12:.6e}" for row in tree)
            and any(row["contract_id"] == "TREE3336_boundary_zero_attempt" for row in tree),
            "detail": "",
        },
        {
            "check_id": "VAL3336_7_composite_contract",
            "check": "composite contract includes commutator, contact, and spectral gap contracts",
            "passed": any(row["contract_id"] == "COMP3336_1_commutator_bound" for row in composite)
            and any(row["contract_id"] == "COMP3336_2_contact_p2" for row in composite)
            and any(row["contract_id"] == "COMP3336_4_two_particle_gap" for row in composite),
            "detail": "",
        },
        {
            "check_id": "VAL3336_8_response_contract",
            "check": "response contract separates A_PPN, C_metric, and product",
            "passed": {"RESP3336_0_A_PPN", "RESP3336_1_C_metric", "RESP3336_2_product"}.issubset(
                {row["contract_id"] for row in response}
            ),
            "detail": "",
        },
        {
            "check_id": "VAL3336_9_no_claim",
            "check": "source/derivation gates pass while claim-ready gate remains false",
            "passed": all(
                row["passed"] == "true"
                for row in gates
                if row["gate_id"] in {"GATE3336_0_real_gamma_candidate", "GATE3336_1_tree_contract", "GATE3336_2_composite_contract", "GATE3336_3_response_contract"}
            )
            and any(row["gate_id"] == "GATE3336_4_claim_ready" and row["passed"] == "false" for row in gates),
            "detail": "",
        },
        {
            "check_id": "VAL3336_10_next_3337",
            "check": "next target attacks commutator/contact theorem",
            "passed": any("commutator" in row["objective"] and "contact" in row["objective"] for row in next_target_rows()),
            "detail": "",
        },
        {
            "check_id": "VAL3336_11_formalization_untouched",
            "check": "formalization-workbench modified-file count remains zero by this script",
            "passed": fw_changed == 0,
            "detail": f"formalization_changed_count={fw_changed}",
        },
    ]
    overall = all(bool(check["passed"]) for check in checks)
    checks.append(
        {
            "check_id": "VAL3336_12_overall",
            "check": "3336 validation overall",
            "passed": overall,
            "detail": "all required checks passed" if overall else "one or more checks failed",
        }
    )
    for check in checks:
        check["passed"] = bool_str(bool(check["passed"]))
    return checks


def render_doc() -> str:
    pass_count = len([row for row in rerank_rows() if row["candidate_pass_like"] == "true"])
    fail_count = len(rerank_rows()) - pass_count
    harsh_allow = math.sqrt(F_TREE * B_GAMMA_CASSINI_1SIGMA / 1.0e12)
    comp_budget = F_COMP * B_GAMMA_CASSINI_1SIGMA
    lines: list[str] = [
        "# 3336 - PPN dominant-floor source acquisition or derivation under AX1090",
        "",
        f"Run UTC: `{RUN_UTC}`",
        "",
        "## Verdict",
        "",
        "3336 replaces one placeholder with a real source-backed candidate and turns the dominant floors into exact acquisition contracts.",
        "",
        "The threshold candidate is Cassini's PPN gamma result:",
        "",
        "`gamma - 1 = (2.1 ± 2.3)e-5`.",
        "",
        f"For private steering, this checkpoint uses `B_gamma_candidate={B_GAMMA_CASSINI_1SIGMA:.2e}` as a gamma-slot candidate only. It is not a full PPN vector and not a local-GR pass.",
        "",
        f"Reranking the 3335 reduced smoke grid with that candidate gives `{pass_count}` pass-like and `{fail_count}` fail-like nonclaim scenarios.",
        "",
        "The harsh response-product contract is now concrete:",
        "",
        f"`epsilon_eff_PPN <= sqrt(0.30 B_gamma/(A_PPN C_metric)) = {harsh_allow:.3e}` for `A_PPN C_metric=1e12`.",
        "",
        "The composite budget contract is also concrete:",
        "",
        f"`epsilon_composite_PPN <= 0.30 B_gamma = {comp_budget:.3e}`.",
        "",
        "For a reference `sigma_Dpi=1e-3`, the commutator ceiling is",
        "",
        f"`delta_comm_PPN <= {comp_budget / SIGMA_DPI_REFERENCE:.3e}`",
        "",
        "before reserving other composite floors.",
        "",
        "So the next best derivation is not broad cosmology or a new field. It is the boring-but-decisive PPN projector/smoothing commutator and contact scaling theorem.",
        "",
        "No PPN/local-GR pass is claimed.",
        "",
        "## Local Source Register",
        "",
    ]
    for row in local_source_rows():
        lines.append(
            f"- `{row['source_id']}`: `{row['path_or_url']}` exists={row['exists']} parse_ok={row['parse_ok']} role={row['role']}"
        )
    lines.extend(["", "## Web Source Register", ""])
    for row in web_source_rows():
        lines.append(
            f"- `{row['source_id']}`: {row['title']}; url={row['url']}; doi={row['doi']}; role={row['role']}; candidate={row['candidate_value']}"
        )
    sections = [
        ("PPN Threshold Candidates", threshold_candidate_rows(), "threshold_id"),
        ("Dominant Floor Rerank", rerank_rows(), "scenario_id"),
        ("Tree Epsilon Bound Contract", tree_contract_rows(), "contract_id"),
        ("Composite Contact Commutator Contract", composite_contract_rows(), "contract_id"),
        ("Response Product Acquisition Contract", response_contract_rows(), "contract_id"),
        ("Required Source Inputs", required_source_input_rows(), "input_id"),
        ("Promotion Gates", promotion_gate_rows(), "gate_id"),
        ("Decision Ledger", decision_rows(), "decision_id"),
        ("Next Target", next_target_rows(), "target_doc"),
    ]
    for title, rows, key_name in sections:
        lines.extend(["", f"## {title}", ""])
        for row in rows:
            label = row.get(key_name, "")
            body = "; ".join(f"{key}={value}" for key, value in row.items() if key != key_name)
            lines.append(f"- `{label}`: {body}")
    lines.extend(
        [
            "",
            "## Test Notes",
            "",
            "- This checkpoint is private and nonclaim.",
            "- Cassini gamma is a source-backed candidate threshold, not the full PPN vector.",
            "- All response-product values remain placeholders until `A_PPN C_metric` is bounded.",
            "- The point of this checkpoint is to identify exact next derivations, not to announce a pass.",
            "- `formalization-workbench` is not modified.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> None:
    formalization_before = snapshot_tree(FW)
    OUT.mkdir(parents=True, exist_ok=True)
    write_csv(OUTPUTS["sources"], local_source_rows())
    write_csv(OUTPUTS["web"], web_source_rows())
    write_csv(OUTPUTS["thresholds"], threshold_candidate_rows())
    write_csv(OUTPUTS["rerank"], rerank_rows())
    write_csv(OUTPUTS["tree"], tree_contract_rows())
    write_csv(OUTPUTS["composite"], composite_contract_rows())
    write_csv(OUTPUTS["response"], response_contract_rows())
    write_csv(OUTPUTS["inputs"], required_source_input_rows())
    write_csv(OUTPUTS["gates"], promotion_gate_rows())
    write_csv(OUTPUTS["decision"], decision_rows())
    write_csv(OUTPUTS["next"], next_target_rows())
    DOC.write_text(render_doc(), encoding="utf-8")
    write_csv(OUTPUTS["validation"], validate_outputs(formalization_before))
    if PYCACHE.exists():
        shutil.rmtree(PYCACHE)


if __name__ == "__main__":
    main()
