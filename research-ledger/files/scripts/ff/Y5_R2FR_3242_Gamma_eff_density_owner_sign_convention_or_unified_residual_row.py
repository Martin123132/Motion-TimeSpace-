from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
FW = REPO / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
PYCACHE = ROOT / "scripts" / "__pycache__"

CHECKPOINT = "3242"
DOC = ROOT / "3242-Y5-R2FR-Gamma-eff-density-owner-sign-convention-or-unified-residual-row-under-AX1090.md"

OUTPUTS = {
    "sources": OUT / "P8_Y5_R2FR_3242_SOURCE_REGISTER.csv",
    "sign": OUT / "P8_Y5_R2FR_3242_SIGN_CONVENTION_LOCK.csv",
    "candidates": OUT / "P8_Y5_R2FR_3242_GAMMA_EFF_DENSITY_CANDIDATE_RANKING.csv",
    "contract": OUT / "P8_Y5_R2FR_3242_DENSITY_OWNER_CONTRACT.csv",
    "kmetric": OUT / "P8_Y5_R2FR_3242_KMETRIC_COMPONENT_READINESS.csv",
    "residual": OUT / "P8_Y5_R2FR_3242_UNIFIED_RESIDUAL_ROW_UPDATE.csv",
    "gates": OUT / "P8_Y5_R2FR_3242_CLAIM_GATES.csv",
    "decision": OUT / "P8_Y5_R2FR_3242_DECISION.csv",
    "next": OUT / "P8_Y5_R2FR_3242_NEXT_TARGET.csv",
    "validation": OUT / "P8_Y5_R2FR_3242_VALIDATION.csv",
}

RUN_UTC = datetime.now(timezone.utc).isoformat()


def bool_str(value: bool) -> str:
    return "true" if value else "false"


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key, "") for key in fieldnames})


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def csv_ok(path: Path) -> bool:
    try:
        if not path.exists():
            return False
        read_csv(path)
        return True
    except Exception:
        return False


def parse_ok(path: Path) -> bool:
    if not path.exists():
        return False
    return csv_ok(path) if path.suffix.lower() == ".csv" else True


def evidence(path: Path, needles: list[str], limit: int = 4) -> str:
    if not path.exists():
        return "MISSING_SOURCE"
    lowered = [needle.lower() for needle in needles]
    hits: list[str] = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8", errors="replace").splitlines(), start=1):
        haystack = line.lower()
        if any(needle in haystack for needle in lowered):
            hits.append(f"L{line_number}:{' '.join(line.strip().split())[:240]}")
        if len(hits) >= limit:
            break
    return " | ".join(hits) if hits else "NO_MATCH"


def under(path: Path, root: Path) -> bool:
    try:
        path.resolve().relative_to(root.resolve())
        return True
    except ValueError:
        return False


def md_escape(value: Any) -> str:
    return str(value).replace("\\", "\\\\").replace("|", "\\|").replace("\n", "<br>")


def md_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    body = ["| " + " | ".join(md_escape(row.get(column, "")) for column in columns) + " |" for row in rows]
    return "\n".join([header, separator, *body])


SOURCES = [
    {
        "source_id": "SRC3242_00_3241_doc",
        "path": ROOT / "3241-Y5-R2FR-public-EH-and-SGK-metric-response-unification-or-residual-vector-under-AX1090.md",
        "role": "3241 selects Gamma_eff density owner/sign convention as the next gate",
        "needles": ["GAMMA_EFF_DENSITY_OWNER", "E_res_GK", "NEXT3241_0_3242"],
    },
    {
        "source_id": "SRC3242_01_2975_doc",
        "path": ROOT / "2975-Y5-R2FR-GammaKhat-sign-convention-and-metric-response-certificate-or-DeltaK-bound-row-under-AX1090.md",
        "role": "canonical q_loc-positive sign convention and Delta_K definition",
        "needles": ["T_q^{mu nu}:=Gamma_eff", "Delta_K^{mu nu}:=K_hat", "q_loc-positive"],
    },
    {
        "source_id": "SRC3242_02_2976_doc",
        "path": ROOT / "2976-Y5-R2FR-Gamma-eff-scalar-density-owner-and-Kmetric-volume-component-or-DeltaK-first-bound-under-AX1090.md",
        "role": "response-doublet Gamma_eff density candidate and K_vol template",
        "needles": ["Gamma_eff = Gamma0", "K_vol", "DeltaK_vol"],
    },
    {
        "source_id": "SRC3242_03_3065_doc",
        "path": ROOT / "3065-Y5-R2FR-Gamma-eff-density-owner-and-Khat-metric-response-identity-or-DeltaK-input-fill-under-AX1090.md",
        "role": "modern density owner gate and live Khat metric-response failure",
        "needles": ["Gamma_eff Density Owner Gate", "K_hat = K_metric", "Delta_K = K_hat"],
    },
    {
        "source_id": "SRC3242_04_1188_doc",
        "path": ROOT / "1188-Y5-R10-Gamma-Khat-Ploc-profile-source-ledger-or-q_loc-demotion-row.md",
        "role": "earlier Gamma/Khat/P_loc profile source ledger and candidate formula ranking",
        "needles": ["Gamma_eff = Gamma0", "Gamma_eff = L_cg", "PROFILE_ROUTE_NOT_SCOREABLE"],
    },
    {
        "source_id": "SRC3242_05_candidate_action",
        "path": OUT / "P8_GAMMA_OWNER_CANDIDATE_ACTION.csv",
        "role": "candidate Gamma_eff owner action densities",
        "needles": ["GO516_A_response_doublet_quadratic_density", "GO516_B_positive_auxiliary_energy_density", "GO516_C_topological_boundary_density"],
    },
    {
        "source_id": "SRC3242_06_metric_contract",
        "path": OUT / "P8_GK_METRIC_RESPONSE_CONTRACT.csv",
        "role": "metric-response contract clauses",
        "needles": ["MR514_0_scalar_density", "MR514_1_Khat_metric_response", "MR514_4_fixed_point_subtraction"],
    },
    {
        "source_id": "SRC3242_07_2975_sign_csv",
        "path": OUT / "P8_Y5_R2FR_2975_GAMMAKHAT_SIGN_CONVENTION_LOCK.csv",
        "role": "machine-readable sign lock",
        "needles": ["SIGN2975_0_canonical", "SIGN2975_1_metric", "SIGN2975_2_DeltaK"],
    },
    {
        "source_id": "SRC3242_08_2976_gamma_csv",
        "path": OUT / "P8_Y5_R2FR_2976_GAMMA_EFF_SCALAR_DENSITY_OWNER_AUDIT.csv",
        "role": "machine-readable Gamma_eff owner audit",
        "needles": ["GAM2976_0_density_ansatz", "GAM2976_6_verdict", "MISSING_Z_BASIS_PHYSICAL_LOCK"],
    },
    {
        "source_id": "SRC3242_09_3065_gamma_csv",
        "path": OUT / "P8_Y5_R2FR_3065_GAMMA_EFF_DENSITY_OWNER_GATE.csv",
        "role": "modern machine-readable density owner gate",
        "needles": ["GDO3065_0_density_ansatz", "GDO3065_6_verdict", "NOT_PARENT_SIGNED"],
    },
]


def source_register() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source in SOURCES:
        path = source["path"]
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "source_id": source["source_id"],
                "source_path": str(path),
                "exists": bool_str(path.exists()),
                "parse_ok": bool_str(parse_ok(path)),
                "role": source["role"],
                "evidence_hits": evidence(path, source["needles"]),
                "valid_for_claim": "false",
                "generated_utc": RUN_UTC,
            }
        )
    return rows


def sign_rows() -> list[dict[str, Any]]:
    return [
        {
            "sign_id": "SGN3242_0_q_positive",
            "object": "canonical stress convention",
            "choice": "T_q^{mu nu}:=Gamma_eff g^{mu nu}-K_hat^{mu nu}",
            "derived_rule": "nabla_mu T_q^{mu nu}=nabla^nu Gamma_eff-nabla_mu K_hat^{mu nu}",
            "status": "INHERITED_FROM_2975",
            "claim_allowed": "false",
        },
        {
            "sign_id": "SGN3242_1_sigma",
            "object": "SGK action sign",
            "choice": "sigma_GK=+1",
            "derived_rule": "S_GK=-int sqrt(-g_pub) Gamma_eff gives T_GK=Gamma_eff g-K_metric in the q_loc-positive convention",
            "status": "LOCKED_AS_BOOKKEEPING_CONVENTION",
            "claim_allowed": "false",
        },
        {
            "sign_id": "SGN3242_2_Eres",
            "object": "EH residual sign",
            "choice": "E_res_GK^{mu nu}:=-kappa_* T_GK^{mu nu}",
            "derived_rule": "q_loc^nu=-(1/kappa_*)P_loc[nabla_mu E_res_GK^{mu nu}]-P_loc[nabla_mu Delta_K^{mu nu}]+defects",
            "status": "CONSISTENT_WITH_3241_IDENTITY",
            "claim_allowed": "false",
        },
        {
            "sign_id": "SGN3242_3_guard",
            "object": "mixed-sign cancellation ban",
            "choice": "opposite stress conventions are translated before comparison",
            "derived_rule": "no residual cancellation may be scored across un-translated sign conventions",
            "status": "GUARD_ACTIVE",
            "claim_allowed": "false",
        },
    ]


def candidate_rows() -> list[dict[str, Any]]:
    return [
        {
            "candidate_id": "GAM3242_0_response_doublet",
            "candidate_density": "Gamma_eff=Gamma0+1/2 M_AB Z^A Z^B+O(Z^4)",
            "why_useful": "best route to double-zero: Gamma0 can be subtracted and first derivative vanishes if Z=0 is the local branch",
            "blocking_gap": "M_AB owner, units, positivity, Z-basis physical lock, source-current silence, boundary convention",
            "ranking": "primary_formal_candidate",
            "current_status": "FORMAL_CANDIDATE_NOT_PARENT_SIGNED",
            "valid_for_claim": "false",
        },
        {
            "candidate_id": "GAM3242_1_memory_source",
            "candidate_density": "Gamma_eff=L_cg^{-2}F(m) or active split Gamma_eff=Lambda_loc+gamma_act",
            "why_useful": "has L^-2 units and an active/constant split that can remove background gradients",
            "blocking_gap": "source support, F/F' values, L_cg variation, metric dependence, boundary decay and parent branch rule",
            "ranking": "secondary_profile_candidate",
            "current_status": "FORMULA_SHAPE_EXISTS_PROFILE_NOT_CLAIM_GRADE",
            "valid_for_claim": "false",
        },
        {
            "candidate_id": "GAM3242_2_positive_auxiliary",
            "candidate_density": "Gamma_eff=V(Phi)+1/2 G_AB(Phi)nabla Phi^A nabla Phi^B",
            "why_useful": "could give positivity/no-hair and source-free local silence",
            "blocking_gap": "does not automatically match live Khat; needs field owner, boundary terms, and no hidden matter source",
            "ranking": "fallback_constructive_candidate",
            "current_status": "CANDIDATE_ACTION_NOT_MTS_PARENT_ADOPTED",
            "valid_for_claim": "false",
        },
        {
            "candidate_id": "GAM3242_3_topological_boundary",
            "candidate_density": "Gamma_eff from normalized boundary/topological density Q_B/Q_* or exact form",
            "why_useful": "can silence bulk variation if truly topological/exact",
            "blocking_gap": "weighted-Stokes/corner/harmonic/residual edge terms and M_H_ref/source projection remain open",
            "ranking": "boundary_zero_candidate",
            "current_status": "BOUNDARY_ROUTE_PRECISE_NOT_CLOSED",
            "valid_for_claim": "false",
        },
        {
            "candidate_id": "GAM3242_4_no_density",
            "candidate_density": "no accepted Gamma_eff density",
            "why_useful": "keeps theory honest if all density routes fail",
            "blocking_gap": "then q_loc remains empirical residual rather than a derived local-GR zero",
            "ranking": "discipline_fallback",
            "current_status": "UNIFIED_RESIDUAL_ROW_REQUIRED",
            "valid_for_claim": "false",
        },
    ]


def contract_rows() -> list[dict[str, Any]]:
    return [
        {
            "contract_id": "DOC3242_0_scalar_density",
            "required_clause": "sqrt(-g_pub) Gamma_eff is a parent scalar-density term before readout",
            "must_include": "field content, branch domain, metric dependence, derivative order, units and boundary/reference convention",
            "current_status": "NOT_PARENT_SIGNED",
            "failure_row": "epsilon_Gamma_owner",
            "valid_for_claim": "false",
        },
        {
            "contract_id": "DOC3242_1_background",
            "required_clause": "Gamma0/background part is constant, absorbed into Lambda_*, or subtracted before q_loc readout",
            "must_include": "fixed subtraction rule compatible with EH Lambda and boundary convention",
            "current_status": "BACKGROUND_SUBTRACTION_NOT_PARENT_SIGNED",
            "failure_row": "epsilon_Gamma_background",
            "valid_for_claim": "false",
        },
        {
            "contract_id": "DOC3242_2_response_basis",
            "required_clause": "Z^A is the actual physical quotient/local residual basis",
            "must_include": "map from Z^A to q_loc/Delta_K/PPN components and gauge/constraint removal",
            "current_status": "MISSING_Z_BASIS_PHYSICAL_LOCK",
            "failure_row": "epsilon_Z_lock",
            "valid_for_claim": "false",
        },
        {
            "contract_id": "DOC3242_3_hessian",
            "required_clause": "M_AB is parent-owned with units, positivity and same branch metric dependence",
            "must_include": "source path for M_AB, positivity domain, units, and variation with respect to g_pub",
            "current_status": "MISSING_MAB_OWNER_UNITS_POSITIVITY",
            "failure_row": "epsilon_MAB_owner",
            "valid_for_claim": "false",
        },
        {
            "contract_id": "DOC3242_4_evenness",
            "required_clause": "exchange/readout/source sectors are even so no linear Z source re-enters",
            "must_include": "J_Z=0, B_Z=0 and no source/readout odd channel",
            "current_status": "CONDITIONAL_TEMPLATE_ONLY",
            "failure_row": "epsilon_linear_Gamma",
            "valid_for_claim": "false",
        },
        {
            "contract_id": "DOC3242_5_metric_response",
            "required_clause": "K_metric can be computed and compared to live Khat component-by-component",
            "must_include": "K_vol, K_deltaM, K_deltaZ, K_derivative, K_boundary, tensor slot and volume convention",
            "current_status": "KMETRIC_FORMAL_KHAT_MATCH_UNSIGNED",
            "failure_row": "Delta_K",
            "valid_for_claim": "false",
        },
    ]


def kmetric_rows() -> list[dict[str, Any]]:
    return [
        {
            "component_id": "KM3242_0_Kvol",
            "component": "K_vol^{mu nu}",
            "formula": "Gamma_eff g^{mu nu}",
            "readiness": "BOOKKEEPING_TEMPLATE_LOCKED",
            "missing": "Gamma_eff parent density and live Khat_vol match",
            "valid_for_claim": "false",
        },
        {
            "component_id": "KM3242_1_KdeltaM",
            "component": "K_deltaM^{mu nu}",
            "formula": "metric variation of M_AB in 1/2 M_AB Z^A Z^B",
            "readiness": "MISSING_MAB_METRIC_DEPENDENCE",
            "missing": "M_AB source, units and metric/coframe dependence",
            "valid_for_claim": "false",
        },
        {
            "component_id": "KM3242_2_KdeltaZ",
            "component": "K_deltaZ^{mu nu}",
            "formula": "metric variation of the Z^A basis and projector/domain map",
            "readiness": "MISSING_Z_METRIC_DEPENDENCE",
            "missing": "Z physical lock and metric/coframe dependence",
            "valid_for_claim": "false",
        },
        {
            "component_id": "KM3242_3_Kderivative",
            "component": "K_deriv^{mu nu}",
            "formula": "derivative/principal-symbol terms after integration by parts",
            "readiness": "MISSING_DERIVATIVE_ORDER_AND_IBP_CONVENTION",
            "missing": "derivative order, boundary convention and local domain",
            "valid_for_claim": "false",
        },
        {
            "component_id": "KM3242_4_Kboundary",
            "component": "K_boundary^{mu nu}",
            "formula": "boundary/improvement/symplectic/corner terms",
            "readiness": "MISSING_BOUNDARY_REFERENCE_OWNER",
            "missing": "B_GK, weighted-Stokes/corner/harmonic terms, no-flux theorem or source-backed bound",
            "valid_for_claim": "false",
        },
        {
            "component_id": "KM3242_5_verdict",
            "component": "K_metric[Gamma_eff]",
            "formula": "sum of all Kmetric components",
            "readiness": "NOT_COMPUTABLE_FOR_LIVE_CLAIM",
            "missing": "Gamma_eff density owner plus all component metric variations",
            "valid_for_claim": "false",
        },
    ]


def residual_rows() -> list[dict[str, Any]]:
    return [
        {
            "residual_id": "GUR3242_0_epsilon_Gamma_owner",
            "quantity": "epsilon_Gamma_owner",
            "formula": "norm(K_metric[candidate Gamma_eff]-K_metric[parent Gamma_eff]) or direct density-owner defect",
            "status": "NEW_EXPLICIT_RESIDUAL_ROW",
            "feeds": "E_res_GK;Delta_K;q_loc;PPN/R10/clock/orbit bounds",
            "valid_for_claim": "false",
        },
        {
            "residual_id": "GUR3242_1_sigma_GK",
            "quantity": "sigma_GK",
            "formula": "+1 in q_loc-positive convention",
            "status": "LOCKED_BOOKKEEPING_CONVENTION",
            "feeds": "E_res_GK sign and q_loc divergence bridge",
            "valid_for_claim": "false",
        },
        {
            "residual_id": "GUR3242_2_Gamma_candidate",
            "quantity": "Gamma_eff_candidate",
            "formula": "primary formal candidate Gamma0+1/2 M_AB Z^A Z^B+O(Z^4)",
            "status": "FORMAL_ONLY_NOT_PARENT_SIGNED",
            "feeds": "Kmetric attempt and double-zero route",
            "valid_for_claim": "false",
        },
        {
            "residual_id": "GUR3242_3_DeltaK",
            "quantity": "Delta_K^{mu nu}",
            "formula": "Khat_live^{mu nu}-K_metric^{mu nu}[Gamma_eff]",
            "status": "RETAINED_OFFICIAL_METRIC_RESPONSE_DEFECT",
            "feeds": "q_loc bound and local PPN residual vector",
            "valid_for_claim": "false",
        },
        {
            "residual_id": "GUR3242_4_HGK",
            "quantity": "H_GK",
            "formula": "Helmholtz obstruction for live Gamma_eff/Khat stress",
            "status": "RETAINED_ACTION_EXISTENCE_DEFECT",
            "feeds": "rejects bookkeeping stress claim until zero/bound",
            "valid_for_claim": "false",
        },
    ]


def gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "CG3242_0_sigma",
            "claim": "sigma_GK sign convention is fixed for the unified residual ledger",
            "gate_pass": "true",
            "reason": "2975 q_loc-positive stress fixes sigma_GK=+1 in the 3241 identity",
            "claim_allowed": "false",
        },
        {
            "gate_id": "CG3242_1_density_owner",
            "claim": "Gamma_eff is parent-owned as live scalar-density",
            "gate_pass": "false",
            "reason": "only formal candidates exist; field content, units, Z/M_AB owners and boundary convention are unsigned",
            "claim_allowed": "false",
        },
        {
            "gate_id": "CG3242_2_kmetric",
            "claim": "K_metric[Gamma_eff] is computable for live component comparison",
            "gate_pass": "false",
            "reason": "only K_vol template is isolated; K_deltaM/K_deltaZ/derivative/boundary components are missing",
            "claim_allowed": "false",
        },
        {
            "gate_id": "CG3242_3_khat_match",
            "claim": "Khat_live equals K_metric[Gamma_eff]",
            "gate_pass": "false",
            "reason": "live Khat component source list and tensor-slot certificate remain missing",
            "claim_allowed": "false",
        },
        {
            "gate_id": "CG3242_4_local_gr",
            "claim": "local GR/Newton branch is derived",
            "gate_pass": "false",
            "reason": "Gamma owner, Delta_K, H_GK, boundary/projector and GM transfer remain open",
            "claim_allowed": "false",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3242_0_sign",
            "decision": "LOCK_SIGMA_GK_PLUS_ONE_FOR_CURRENT_BRANCH",
            "because": "it is the only sign consistent with T_q=Gamma_eff g-Khat and the q_loc-positive divergence bridge",
            "next_action": "all future E_res_GK and Delta_K rows inherit this convention",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC3242_1_density",
            "decision": "PRIMARY_GAMMA_DENSITY_REMAINS_RESPONSE_DOUBLET_BUT_NOT_CLAIM",
            "because": "it is the best double-zero candidate but lacks M_AB, Z-basis, units, positivity, source-current and boundary owners",
            "next_action": "attack M_AB/Z/source-current/boundary lock rather than broad Gamma hunting",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC3242_2_residual",
            "decision": "ADD_EPSILON_GAMMA_OWNER_TO_UNIFIED_RESIDUAL_VECTOR",
            "because": "a formal candidate density cannot be silently substituted for a parent density",
            "next_action": "carry epsilon_Gamma_owner alongside Delta_K and H_GK until density ownership closes",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC3242_3_best_next",
            "decision": "MAB_Z_BASIS_SOURCE_CURRENT_BOUNDARY_LOCK_IS_NEXT",
            "because": "that is the first non-handwavy way to make Gamma_eff a real density and Kmetric computable",
            "next_action": "build 3243 response-doublet owner lock or demote Gamma_eff to residual profile row",
            "valid_for_claim": "false",
        },
    ]


def next_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT3242_0_3243",
            "next_checkpoint": "3243-Y5-R2FR-response-doublet-MAB-Zbasis-source-current-boundary-lock-or-Gamma-owner-residual-under-AX1090.md",
            "mission": "try to parent-sign the response-doublet density by deriving M_AB, Z^A physical lock, units/positivity, J_Z=0, B_Z=0 and background subtraction together; otherwise retain Gamma_eff as an explicit residual profile",
            "starting_equation": "Gamma_eff=Gamma0+1/2 M_AB Z^A Z^B+O(Z^4)",
            "success_if": "M_AB and Z^A are parent-owned in the public quotient branch with units, positivity, metric dependence, source-current silence and boundary convention",
            "fallback_if_fail": "promote no claim; keep epsilon_Gamma_owner, Delta_K and H_GK as no-cancellation residual rows",
            "claim_policy": "no local-GR/Newton/PPN/R10/clock/orbit claim from response-doublet notation alone",
            "valid_for_claim": "false",
        }
    ]


def validation_rows(source_rows: list[dict[str, Any]], generated_csvs: list[Path]) -> list[dict[str, Any]]:
    no_missing_sources = all(row["exists"] == "true" and row["parse_ok"] == "true" for row in source_rows)
    no_no_match = all("MISSING_SOURCE" not in row["evidence_hits"] and "NO_MATCH" not in row["evidence_hits"] for row in source_rows)
    outputs = [DOC, *generated_csvs]
    outputs_under_pcw = all(under(path, ROOT) for path in outputs)
    no_fw_outputs = all(not under(path, FW) for path in outputs)
    csvs_parse = all(csv_ok(path) for path in generated_csvs)
    claim_true = 0
    for path in generated_csvs:
        for row in read_csv(path):
            for key in ("valid_for_claim", "claim_allowed", "claim_active"):
                if str(row.get(key, "")).strip().lower() == "true":
                    claim_true += 1
    sign_locked = any(row["sign_id"] == "SGN3242_1_sigma" and row["choice"] == "sigma_GK=+1" for row in read_csv(OUTPUTS["sign"]))
    epsilon_gamma = any(row["residual_id"] == "GUR3242_0_epsilon_Gamma_owner" for row in read_csv(OUTPUTS["residual"]))
    next_specific = any("response-doublet-MAB-Zbasis" in row["next_checkpoint"] for row in read_csv(OUTPUTS["next"]))
    return [
        {
            "validation_id": "VAL3242_00_sources_exist_parse",
            "passed": bool_str(no_missing_sources),
            "requirement": "all cited source paths exist and parse",
            "evidence": str(OUTPUTS["sources"]),
        },
        {
            "validation_id": "VAL3242_01_evidence_hits",
            "passed": bool_str(no_no_match),
            "requirement": "source register has direct evidence hits",
            "evidence": str(OUTPUTS["sources"]),
        },
        {
            "validation_id": "VAL3242_02_sigma_locked",
            "passed": bool_str(sign_locked),
            "requirement": "sigma_GK is locked to +1 for the q_loc-positive branch",
            "evidence": str(OUTPUTS["sign"]),
        },
        {
            "validation_id": "VAL3242_03_epsilon_gamma_row",
            "passed": bool_str(epsilon_gamma),
            "requirement": "epsilon_Gamma_owner is added to the unified residual vector",
            "evidence": str(OUTPUTS["residual"]),
        },
        {
            "validation_id": "VAL3242_04_next_specific",
            "passed": bool_str(next_specific),
            "requirement": "next target is M_AB/Z/source-current/boundary lock, not broad Gamma hunting",
            "evidence": str(OUTPUTS["next"]),
        },
        {
            "validation_id": "VAL3242_05_claims_blocked",
            "passed": bool_str(claim_true == 0),
            "requirement": "no local-GR/Newton/PPN/R10/clock/orbit claim is promoted",
            "evidence": f"claim_true={claim_true}",
        },
        {
            "validation_id": "VAL3242_06_csv_parse",
            "passed": bool_str(csvs_parse),
            "requirement": "all generated CSV files parse cleanly",
            "evidence": ";".join(str(path) for path in generated_csvs),
        },
        {
            "validation_id": "VAL3242_07_outputs_under_post_checkpoint",
            "passed": bool_str(outputs_under_pcw),
            "requirement": "all outputs stay inside post-checkpoint-work",
            "evidence": str(ROOT),
        },
        {
            "validation_id": "VAL3242_08_no_formalization_outputs",
            "passed": bool_str(no_fw_outputs),
            "requirement": "formalization-workbench is not modified",
            "evidence": str(FW),
        },
        {
            "validation_id": "VAL3242_09_pycache_absent",
            "passed": bool_str(not PYCACHE.exists()),
            "requirement": "scripts __pycache__ removed",
            "evidence": str(PYCACHE),
        },
        {
            "validation_id": "VAL3242_10_doc_written",
            "passed": bool_str(DOC.exists()),
            "requirement": "checkpoint markdown document written",
            "evidence": str(DOC),
        },
    ]


def build_doc(
    source_rows: list[dict[str, Any]],
    sign: list[dict[str, Any]],
    candidates: list[dict[str, Any]],
    contract: list[dict[str, Any]],
    kmetric: list[dict[str, Any]],
    residual: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> str:
    return "\n\n".join(
        [
            "# 3242 - Gamma_eff Density Owner, Sign Convention, or Unified Residual Row under AX1090",
            "Private checkpoint. This is not a local-GR, Newton, PPN, R10, WEP, clock, orbital, Maxwell, or public-facing claim.",
            "## Result",
            (
                "3242 locks the sign convention needed by the `3241` EH/SGK bridge: in the existing q_loc-positive convention, "
                "`sigma_GK=+1`. With this sign, `S_GK=-int sqrt(-g_pub) Gamma_eff` gives "
                "`T_GK=Gamma_eff g-K_metric`, and `E_res_GK=-kappa_* T_GK` feeds the exact divergence identity already written in `3241`."
            ),
            (
                "The density owner itself does not close. The strongest current candidate remains the response-doublet density "
                "`Gamma_eff=Gamma0+1/2 M_AB Z^A Z^B+O(Z^4)`, because it is the best route to a double-zero local branch. "
                "But it is still only formal: `M_AB`, `Z^A`, units, positivity, source-current silence, background subtraction, and boundary convention are not parent-signed together."
            ),
            (
                "The useful new discipline is that `epsilon_Gamma_owner` is now an explicit member of the unified residual vector. "
                "A candidate `Gamma_eff` cannot be quietly substituted for a parent density; it either becomes parent-owned or it remains a no-cancellation residual alongside `Delta_K` and `H_GK`."
            ),
            "## Sign Convention Lock",
            md_table(sign, ["sign_id", "object", "choice", "derived_rule", "status", "claim_allowed"]),
            "## Gamma_eff Density Candidate Ranking",
            md_table(
                candidates,
                ["candidate_id", "candidate_density", "why_useful", "blocking_gap", "ranking", "current_status", "valid_for_claim"],
            ),
            "## Density Owner Contract",
            md_table(
                contract,
                ["contract_id", "required_clause", "must_include", "current_status", "failure_row", "valid_for_claim"],
            ),
            "## Kmetric Component Readiness",
            md_table(kmetric, ["component_id", "component", "formula", "readiness", "missing", "valid_for_claim"]),
            "## Unified Residual Row Update",
            md_table(residual, ["residual_id", "quantity", "formula", "status", "feeds", "valid_for_claim"]),
            "## Claim Gates",
            md_table(gates, ["gate_id", "claim", "gate_pass", "reason", "claim_allowed"]),
            "## Decision",
            md_table(decisions, ["decision_id", "decision", "because", "next_action", "valid_for_claim"]),
            "## Next Target",
            md_table(
                next_target,
                [
                    "next_id",
                    "next_checkpoint",
                    "mission",
                    "starting_equation",
                    "success_if",
                    "fallback_if_fail",
                    "claim_policy",
                    "valid_for_claim",
                ],
            ),
            "## Source Register",
            md_table(source_rows, ["source_id", "source_path", "exists", "parse_ok", "role", "evidence_hits", "valid_for_claim"]),
            "## Validation",
            md_table(validation, ["validation_id", "passed", "requirement", "evidence"]),
            "## Generated Evidence",
            "\n".join(f"- `{path}`" for path in OUTPUTS.values()),
        ]
    )


def main() -> None:
    for path in OUTPUTS.values():
        path.parent.mkdir(parents=True, exist_ok=True)
    DOC.parent.mkdir(parents=True, exist_ok=True)

    source_rows = source_register()
    sign = sign_rows()
    candidates = candidate_rows()
    contract = contract_rows()
    kmetric = kmetric_rows()
    residual = residual_rows()
    gates = gate_rows()
    decisions = decision_rows()
    next_target = next_rows()

    write_csv(OUTPUTS["sources"], source_rows)
    write_csv(OUTPUTS["sign"], sign)
    write_csv(OUTPUTS["candidates"], candidates)
    write_csv(OUTPUTS["contract"], contract)
    write_csv(OUTPUTS["kmetric"], kmetric)
    write_csv(OUTPUTS["residual"], residual)
    write_csv(OUTPUTS["gates"], gates)
    write_csv(OUTPUTS["decision"], decisions)
    write_csv(OUTPUTS["next"], next_target)

    if PYCACHE.exists():
        shutil.rmtree(PYCACHE)

    generated_csvs = [
        OUTPUTS["sources"],
        OUTPUTS["sign"],
        OUTPUTS["candidates"],
        OUTPUTS["contract"],
        OUTPUTS["kmetric"],
        OUTPUTS["residual"],
        OUTPUTS["gates"],
        OUTPUTS["decision"],
        OUTPUTS["next"],
    ]
    validation = validation_rows(source_rows, generated_csvs)
    write_csv(OUTPUTS["validation"], validation)
    DOC.write_text(
        build_doc(source_rows, sign, candidates, contract, kmetric, residual, gates, decisions, next_target, validation),
        encoding="utf-8",
    )
    validation = validation_rows(source_rows, generated_csvs)
    write_csv(OUTPUTS["validation"], validation)
    DOC.write_text(
        build_doc(source_rows, sign, candidates, contract, kmetric, residual, gates, decisions, next_target, validation),
        encoding="utf-8",
    )

    if PYCACHE.exists():
        shutil.rmtree(PYCACHE)

    failed = [row for row in validation if row["passed"] != "true"]
    if failed:
        raise SystemExit(f"3242 validation failed: {failed}")


if __name__ == "__main__":
    main()
