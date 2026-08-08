from __future__ import annotations

import csv
import hashlib
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
FW = REPO / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
PYCACHE = ROOT / "scripts" / "__pycache__"

DOC = ROOT / "3343-Y5-R2FR-epsilon-EM-public-Hodge-Poynting-zero-or-bound-under-AX1090.md"

SOURCES = [
    {
        "source_id": "SRC3343_0_3342_doc",
        "path": ROOT / "3342-Y5-R2FR-eta-species-no-spurion-zero-or-WEP-bound-under-AX1090.md",
        "role": "3342 handoff selecting epsilon_EM/Poynting next",
    },
    {
        "source_id": "SRC3343_1_3340_schema",
        "path": OUT / "P8_Y5_R2FR_3340_FINITE_RESIDUAL_VECTOR_SCHEMA.csv",
        "role": "FRV3340 epsilon_EM definition and bound formula",
    },
    {
        "source_id": "SRC3343_2_3341_contract",
        "path": OUT / "P8_Y5_R2FR_3341_COMPONENT_RUNNER_CONTRACT.csv",
        "role": "strict finite residual runner contract",
    },
    {
        "source_id": "SRC3343_3_3340_parent_evidence",
        "path": OUT / "P8_Y5_R2FR_3340_PARENT_CLAUSE_EVIDENCE_SCORE.csv",
        "role": "current public Maxwell/Hodge parent signature status",
    },
    {
        "source_id": "SRC3343_4_3117_alpha_priority",
        "path": OUT / "P8_Y5_R2FR_3117_EM_COUPLING_OWNER_ALPHA_PRIORITY.csv",
        "role": "alpha/current/Hodge residual priority split",
    },
    {
        "source_id": "SRC3343_5_3127_hilbert_em",
        "path": OUT / "P8_Y5_R2FR_3127_HILBERT_EM_WEIGHT_MEASURE_OUTPUT.csv",
        "role": "Hilbert EM stress measure and Poynting guard",
    },
    {
        "source_id": "SRC3343_6_3285_poynting_qbasic",
        "path": OUT / "P8_Y5_R2FR_3285_POYNTING_QBASIC_LEMMA.csv",
        "role": "Poynting q-basic lemma",
    },
    {
        "source_id": "SRC3343_7_3286_hodge_poynting",
        "path": OUT / "P8_Y5_R2FR_3286_HODGE_POYNTING_OWNER_THEOREM.csv",
        "role": "Hodge/Poynting owner theorem",
    },
    {
        "source_id": "SRC3343_8_3287_chi_reconstruction",
        "path": OUT / "P8_Y5_R2FR_3287_CHI_TO_HODGE_RECONSTRUCTION_THEOREM.csv",
        "role": "constitutive chi to metric Hodge reconstruction",
    },
    {
        "source_id": "SRC3343_9_3289_qbasic_zq",
        "path": OUT / "P8_Y5_R2FR_3289_QBASIC_ZQ_THEOREM.csv",
        "role": "Z_Q q-basic and alpha relation theorem",
    },
    {
        "source_id": "SRC3343_10_3290_no_hidden_zq",
        "path": OUT / "P8_Y5_R2FR_3290_NO_HIDDEN_ZQ_COEFFICIENT_THEOREM.csv",
        "role": "no-hidden Z_Q theorem and counterexample",
    },
    {
        "source_id": "SRC3343_11_3290_current",
        "path": OUT / "P8_Y5_R2FR_3290_SOURCE_CURRENT_UNIVERSALITY_THEOREM.csv",
        "role": "source-current universality theorem",
    },
    {
        "source_id": "SRC3343_12_3323_poynting_gate",
        "path": OUT / "P8_Y5_R2FR_3323_EM_POYNTING_SOURCE_GATE.csv",
        "role": "Poynting source discipline gate",
    },
    {
        "source_id": "SRC3343_13_3324_clean_route",
        "path": OUT / "P8_Y5_R2FR_3324_MAXWELL_EM_STRESS_CLEAN_ROUTE.csv",
        "role": "clean Maxwell EM stress route",
    },
    {
        "source_id": "SRC3343_14_3339_em_route",
        "path": OUT / "P8_Y5_R2FR_3339_MAXWELL_EM_STRESS_COUPLING_ROUTE.csv",
        "role": "3339 Maxwell EM stress coupling route",
    },
    {
        "source_id": "SRC3343_15_3339_parent_requirements",
        "path": OUT / "P8_Y5_R2FR_3339_PARENT_SIGNATURE_REQUIREMENTS.csv",
        "role": "public Maxwell/Hodge parent signature requirement",
    },
]

OUTPUTS = {
    "sources": OUT / "P8_Y5_R2FR_3343_SOURCE_REGISTER.csv",
    "maxwell_derivation": OUT / "P8_Y5_R2FR_3343_PUBLIC_MAXWELL_ACTION_DERIVATION.csv",
    "hodge_poynting_zero": OUT / "P8_Y5_R2FR_3343_HODGE_POYNTING_ZERO_AUDIT.csv",
    "residual_decomposition": OUT / "P8_Y5_R2FR_3343_EPSILON_EM_RESIDUAL_DECOMPOSITION.csv",
    "partial_zero": OUT / "P8_Y5_R2FR_3343_PARTIAL_ZERO_CERTIFICATE.csv",
    "component_rows": OUT / "P8_Y5_R2FR_3343_FRV3340_EPSILON_EM_COMPONENT_ROWS.csv",
    "double_count_guard": OUT / "P8_Y5_R2FR_3343_POYNTING_DOUBLE_COUNT_GUARD.csv",
    "promotion_gates": OUT / "P8_Y5_R2FR_3343_PROMOTION_GATES.csv",
    "decision": OUT / "P8_Y5_R2FR_3343_DECISION_LEDGER.csv",
    "next": OUT / "P8_Y5_R2FR_3343_NEXT_TARGET.csv",
    "validation": OUT / "P8_Y5_BRR545_3343_VALIDATION.csv",
}

RUN_UTC = datetime.now(timezone.utc).isoformat()


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


def source_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source in SOURCES:
        path = source["path"]
        rows.append(
            {
                "source_id": source["source_id"],
                "path": str(path),
                "exists": bool_str(path.exists()),
                "parse_ok": bool_str(parse_ok(path)),
                "sha256_prefix": sha256_prefix(path),
                "role": source["role"],
                "valid_for_claim": "false",
            }
        )
    return rows


def parent_public_maxwell_signed() -> bool:
    evidence_path = OUT / "P8_Y5_R2FR_3340_PARENT_CLAUSE_EVIDENCE_SCORE.csv"
    if not evidence_path.exists():
        return False
    rows = read_csv(evidence_path)
    return any(
        row.get("clause_id") == "HSC3340_4_public_Maxwell_Hodge"
        and row.get("passes_parent_signature") == "true"
        for row in rows
    )


def maxwell_derivation_rows() -> list[dict[str, Any]]:
    return [
        {
            "derivation_id": "EMD3343_0_action",
            "claim_piece": "public Maxwell action",
            "formula": "S_EM[g_obs,A_Q]=-lambda_0/4 int sqrt(-g_obs) F_{mu nu}F^{mu nu} + int sqrt(-g_obs) A_mu J_Q^mu",
            "derivation": "The only metric/coframe dependence is public g_obs and lambda_0 is hidden-independent.",
            "result": "EM belongs in the same Hilbert-stress source sector as ordinary matter.",
            "status": "EXACT_CONDITIONAL_ACTION_FORM",
            "valid_for_claim": "false",
        },
        {
            "derivation_id": "EMD3343_1_metric_variation",
            "claim_piece": "Hilbert EM stress",
            "formula": "T_EM^{mu nu}=lambda_0(F^{mu alpha}F^nu_alpha - 1/4 g_obs^{mu nu}F_{alpha beta}F^{alpha beta})",
            "derivation": "Vary S_EM with respect to g_obs; no private Hodge or background-flow tensor is varied separately.",
            "result": "EM energy density, stress, pressure, and radiation flux are source terms through T_EM.",
            "status": "EXACT_CONDITIONAL_VARIATION",
            "valid_for_claim": "false",
        },
        {
            "derivation_id": "EMD3343_2_current_variation",
            "claim_piece": "Maxwell equation/current owner",
            "formula": "nabla_mu(lambda_0 F^{mu nu})=J_Q^nu",
            "derivation": "Vary A_Q; if J_Q is the same Noether current/readout lattice, delta_J=0.",
            "result": "A floating source/test charge normalization is not allowed in the clean branch.",
            "status": "EXACT_CONDITIONAL_CURRENT_ROUTE",
            "valid_for_claim": "false",
        },
        {
            "derivation_id": "EMD3343_3_poynting_balance",
            "claim_piece": "Poynting as flux of Hilbert stress",
            "formula": "dE_EM/dt = - surface_int S dot dA - int J dot E dV",
            "derivation": "Project nabla_mu T_EM^{mu nu}=-F^nu_mu J^mu onto an observer slice.",
            "result": "Poynting is not a separate MTS force in the clean route; it is the spatial energy-flux component of T_EM.",
            "status": "EXACT_CONDITIONAL_FLUX_LAW",
            "valid_for_claim": "false",
        },
        {
            "derivation_id": "EMD3343_4_vertical_zero",
            "claim_piece": "epsilon_EM theorem-zero condition",
            "formula": "L_v g_obs=L_v lambda_0=L_v J_Q=L_v chi_nonmetric=L_v(readout)=0 => epsilon_EM=0",
            "derivation": "Chain rule and Leibniz rule kill b_alpha, delta_J, delta_star, DeltaT_EM, and unclosed Poynting flux.",
            "result": "epsilon_EM is zero only if every EM coefficient/readout factor is q-basic or constant.",
            "status": "EXACT_CONDITIONAL_THEOREM_NOT_PARENT_SIGNED",
            "valid_for_claim": "false",
        },
    ]


def hodge_poynting_zero_rows() -> list[dict[str, Any]]:
    parent_signed = parent_public_maxwell_signed()
    return [
        {
            "audit_id": "HPZ3343_0_metric_hodge",
            "subterm": "delta_star",
            "zero_condition": "chi^{mu nu alpha beta}=lambda_0 sqrt(-g_obs)(g_obs^{mu alpha}g_obs^{nu beta}-g_obs^{mu beta}g_obs^{nu alpha}) with no nonmetric Delta_chi",
            "proof_piece": "metric Hodge specialization and reconstruction rows 3286/3287",
            "current_status": "EXACT_CONDITIONAL_NOT_PARENT_SIGNED",
            "parent_signed": bool_str(parent_signed),
            "valid_for_claim": "false",
        },
        {
            "audit_id": "HPZ3343_1_poynting",
            "subterm": "Phi_Poynting_unclosed",
            "zero_condition": "Poynting vector is read as S_EM^a=-h^a_mu T_EM^{mu nu}u_nu from same public Hodge/coframe and has zero or explicitly balanced boundary flux",
            "proof_piece": "Poynting q-basic lemma plus 3127 flux guard",
            "current_status": "EXACT_CONDITIONAL_WITH_BOUNDARY_GUARD",
            "parent_signed": bool_str(parent_signed),
            "valid_for_claim": "false",
        },
        {
            "audit_id": "HPZ3343_2_ZQ",
            "subterm": "b_alpha",
            "zero_condition": "Z_Q=lambda_0 is constant/q-basic and no hidden f_X, radiative readout drift, or F^2 counterterm survives",
            "proof_piece": "3289 q-basic Z_Q theorem and 3290 no-hidden Z_Q theorem",
            "current_status": "COUNTERMODEL_RETAINED",
            "parent_signed": "false",
            "valid_for_claim": "false",
        },
        {
            "audit_id": "HPZ3343_3_current",
            "subterm": "delta_J",
            "zero_condition": "J_Q is the same Noether current with fixed representation charge labels and no source/test current renormalization",
            "proof_piece": "3290 source-current universality theorem",
            "current_status": "EXACT_CONDITIONAL_NOT_PARENT_SIGNED",
            "parent_signed": "false",
            "valid_for_claim": "false",
        },
        {
            "audit_id": "HPZ3343_4_no_direct_vertex",
            "subterm": "direct EM-background force",
            "zero_condition": "no f(psi)F^2, psi J.A, or direct Poynting-background force term unless parent-derived and separately bounded",
            "proof_piece": "3323/3324 clean-route discipline",
            "current_status": "RECOMMENDED_DISCIPLINE_NOT_PARENT_EXCLUSION",
            "parent_signed": "false",
            "valid_for_claim": "false",
        },
    ]


def residual_decomposition_rows() -> list[dict[str, Any]]:
    return [
        {
            "term_id": "EEM3343_0_b_alpha",
            "component": "b_alpha",
            "definition": "vertical/readout drift of alpha_EM or Z_Q",
            "zero_route": "q-basic/constant Z_Q and q-basic hbar,c,readout",
            "finite_route": "alpha drift, clock products, spectra, R10 alpha products",
            "current_status": "NOT_NUMERIC_FULL_COMPONENT",
            "valid_for_claim": "false",
        },
        {
            "term_id": "EEM3343_1_delta_J",
            "component": "delta_J",
            "definition": "source/test current or charge normalization drift",
            "zero_route": "same Noether current and fixed representation charge lattice",
            "finite_route": "WEP/R10 source-current rows; 3127 has one nonclaim smoke reproduction",
            "current_status": "PARTIAL_NONCLAIM_SMOKE_ONLY",
            "valid_for_claim": "false",
        },
        {
            "term_id": "EEM3343_2_delta_star",
            "component": "delta_star",
            "definition": "hidden Hodge/coframe/constitutive drift",
            "zero_route": "metric Hodge from public g_obs and constant Z_Q",
            "finite_route": "constitutive/birefringence/stress projection bounds",
            "current_status": "DERIVED_CONDITIONAL_NEEDS_PROJECTION_BOUND",
            "valid_for_claim": "false",
        },
        {
            "term_id": "EEM3343_3_delta_TEM",
            "component": "||P_EM DeltaT_EM||/||T_EM||",
            "definition": "non-Hilbert EM stress tensor mismatch",
            "zero_route": "T_EM is metric variation of the public Maxwell action",
            "finite_route": "EM stress/light propagation residual projection",
            "current_status": "EXACT_CONDITIONAL_NOT_PARENT_SIGNED",
            "valid_for_claim": "false",
        },
        {
            "term_id": "EEM3343_4_poynting",
            "component": "Phi_Poynting_unclosed",
            "definition": "unbalanced EM energy flux or double-counted wave/Poynting channel",
            "zero_route": "flux is the spatial component of Hilbert T_EM with closed or explicitly balanced boundary",
            "finite_route": "radiative flux/readout coefficient separate from static ADM source coefficient",
            "current_status": "GUARD_DERIVED_BOUNDARY_NOT_FILLED",
            "valid_for_claim": "false",
        },
    ]


def partial_zero_rows() -> list[dict[str, Any]]:
    return [
        {
            "zero_id": "PZ3343_0_constant_lambda0",
            "claim_piece": "constant lambda_0 does not create a local EM residual",
            "deduction": "L_v lambda_0=0, so lambda_0 can calibrate alpha/Z_Q without producing b_alpha.",
            "still_missing": "parent must forbid hidden f_X(I_hid), radiative/readout alpha drift, or current normalization drift",
            "status": "PARTIAL_ZERO_DERIVED",
            "valid_for_claim": "false",
        },
        {
            "zero_id": "PZ3343_1_poynting_inside_TEM",
            "claim_piece": "Poynting is safe if kept inside Hilbert T_EM",
            "deduction": "S_EM^a=-h^a_mu T_EM^{mu nu}u_nu is q-basic when T_EM,h,u are q-basic.",
            "still_missing": "worldtube/boundary flux balance and public coframe/readout signature",
            "status": "PARTIAL_ZERO_DERIVED",
            "valid_for_claim": "false",
        },
        {
            "zero_id": "PZ3343_2_direct_background_force_forbidden",
            "claim_piece": "direct Poynting-background force is not the clean route",
            "deduction": "Adding Poynting again outside T_EM double-counts EM flux unless a distinct parent vertex is derived.",
            "still_missing": "formal parent exclusion of f(psi)F^2 and psi J.A terms",
            "status": "DISCIPLINE_DERIVED_NOT_PARENT_SIGNED",
            "valid_for_claim": "false",
        },
    ]


def component_rows() -> list[dict[str, Any]]:
    return [
        {
            "candidate_id": "CAND3343_FRV3340_4_epsilon_EM_theorem_zero_unsigned",
            "component_id": "FRV3340_4_epsilon_EM",
            "symbol": "epsilon_EM",
            "mode": "public_Maxwell_Hodge_Poynting_theorem_zero",
            "theorem_zero": "true",
            "zero_authority": "CONDITIONAL_PUBLIC_MAXWELL_NOT_PARENT_SIGNED",
            "component_value": "0.000000e+00",
            "response_factor": "1.000000e+00",
            "component_units": "dimensionless_fractional_EM_residual",
            "source_path": str(OUTPUTS["maxwell_derivation"]),
            "equation_ref": "EMD3343_4_vertical_zero",
            "arena": "Maxwell_EM_stress_Poynting",
            "no_cancellation_guard": "ABS_SUM_NO_CANCELLATION",
            "runner_acceptance": "false",
            "valid_for_claim": "false",
            "claim_blocker": "3341 accepts theorem-zero only with PARENT_SIGNED_HSC3340; HSC3340_4 remains unsigned.",
        },
        {
            "candidate_id": "CAND3343_FRV3340_4_epsilon_EM_finite_incomplete",
            "component_id": "FRV3340_4_epsilon_EM",
            "symbol": "epsilon_EM",
            "mode": "finite_residual_decomposition_nonclaim",
            "theorem_zero": "false",
            "zero_authority": "NONE",
            "component_value": "MISSING_B_ALPHA_DELTA_J_DELTA_STAR_POYNTING_NUMERIC_SUM",
            "response_factor": "1.000000e+00",
            "component_units": "dimensionless_fractional_EM_residual",
            "source_path": str(OUTPUTS["residual_decomposition"]),
            "equation_ref": "epsilon_EM <= |b_alpha| + |delta_J| + |delta_star| + ||P_EM DeltaT_EM||/||T_EM|| + |Phi_Poynting_unclosed|",
            "arena": "Maxwell_EM_stress_Poynting",
            "no_cancellation_guard": "ABS_SUM_NO_CANCELLATION",
            "runner_acceptance": "false",
            "valid_for_claim": "false",
            "claim_blocker": "finite numeric source-backed values for every residual subterm are not filled.",
        },
    ]


def double_count_guard_rows() -> list[dict[str, Any]]:
    return [
        {
            "guard_id": "DCG3343_0_clean_route",
            "rule": "EM waves and Poynting flux are counted through Hilbert T_EM in the clean public Maxwell branch.",
            "allowed": "true",
            "forbidden": "false",
            "why": "This preserves local GR/Maxwell stress coupling and avoids a new fifth-force channel.",
            "valid_for_claim": "false",
        },
        {
            "guard_id": "DCG3343_1_double_count",
            "rule": "Do not add a second Poynting/background-force source if the same EM flux is already included in T_EM.",
            "allowed": "false",
            "forbidden": "true",
            "why": "The same energy flux would source curvature twice unless a separate parent vertex and subtraction rule are derived.",
            "valid_for_claim": "false",
        },
        {
            "guard_id": "DCG3343_2_direct_vertex",
            "rule": "Any f(psi)F^2, psi J.A, or nonmetric constitutive term is a named epsilon_EM residual, not a quiet improvement.",
            "allowed": "conditional_parent_derived_and_bounded",
            "forbidden": "as_unlabelled_closure",
            "why": "It opens clocks, WEP, optical propagation, R10, and source-current tests.",
            "valid_for_claim": "false",
        },
    ]


def promotion_gate_rows() -> list[dict[str, Any]]:
    parent_signed = parent_public_maxwell_signed()
    return [
        {
            "gate_id": "GATE3343_0_public_action_derivation",
            "claim": "public Maxwell action gives Hilbert EM stress and Poynting flux law",
            "passed": "true",
            "reason": "3343 records the action, metric variation, current variation, and Poynting balance identities.",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3343_1_poynting_double_count_guard",
            "claim": "Poynting is routed through T_EM, not added as a second force",
            "passed": "true",
            "reason": "double-count guard forbids separate Poynting-background source unless parent-derived and bounded.",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3343_2_parent_signed_epsilon_zero",
            "claim": "epsilon_EM=0 is parent-signed for MTS",
            "passed": bool_str(parent_signed),
            "reason": "HSC3340_4_public_Maxwell_Hodge remains conditional with hidden F2/Hodge/current closure unsigned." if not parent_signed else "HSC3340_4 is signed.",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3343_3_finite_numeric_epsilon_bound",
            "claim": "finite numeric epsilon_EM row is score-ready",
            "passed": "false",
            "reason": "b_alpha, delta_J, delta_star, DeltaT_EM, and Poynting subterms do not yet have a complete source-backed absolute-sum vector.",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3343_4_local_GR_claim",
            "claim": "local-GR source-coupling branch is claim-ready",
            "passed": "false",
            "reason": "epsilon_EM theorem-zero is conditional only and other FRV3340 components remain open.",
            "valid_for_claim": "false",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3343_0",
            "question": "Should Poynting be treated as the missing separate background field force?",
            "answer": "no, not on the least-scrutiny route",
            "reason": "If EM is public Maxwell, Poynting is already a component/flux of T_EM. Adding it again double-counts unless a new parent vertex is explicitly derived.",
            "next_action": "Keep Poynting inside Hilbert EM stress and attack the hidden Z_Q/current/Hodge clauses.",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC3343_1",
            "question": "Did 3343 close epsilon_EM?",
            "answer": "not yet",
            "reason": "It derives the zero theorem shape, but parent ownership of Z_Q, current lattice, Hodge/readout, and boundary flux is still unsigned.",
            "next_action": "Try no-hidden-Z_Q first because it controls b_alpha and alpha-readout drift without needing to predict the numerical value of alpha.",
            "valid_for_claim": "false",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "target_id": "3344-Y5-R2FR-no-hidden-ZQ-or-alpha-drift-bound-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3344_no_hidden_ZQ_or_alpha_drift_bound.py",
            "objective": "prove Z_Q is q-basic/constant on the local branch, or stage source-backed alpha-drift/readout bounds for b_alpha without claiming epsilon_EM closure",
            "why_next": "b_alpha is the first residual in epsilon_EM and 3289/3290 already isolate the exact hidden coefficient obstruction.",
            "valid_for_claim": "false",
        },
        {
            "target_id": "3344b-Y5-R2FR-source-current-universality-or-deltaJ-bound.md",
            "target_script": "scripts/Y5_R2FR_3344b_source_current_universality_or_deltaJ_bound.py",
            "objective": "prove fixed Noether charge/current lattice or turn existing WEP/R10 current-normalization rows into a source-backed delta_J component",
            "why_next": "delta_J is second EM residual and directly links EM charge/current to WEP/R10 source-coupling tests.",
            "valid_for_claim": "false",
        },
    ]


def markdown_table(rows: list[dict[str, Any]], limit: int = 20) -> str:
    if not rows:
        return "_No rows._"
    fieldnames: list[str] = []
    for row in rows[:limit]:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    lines = [
        "| " + " | ".join(fieldnames) + " |",
        "| " + " | ".join("---" for _ in fieldnames) + " |",
    ]
    for row in rows[:limit]:
        values = [compact(row.get(key, ""), 260).replace("|", "\\|") for key in fieldnames]
        lines.append("| " + " | ".join(values) + " |")
    if len(rows) > limit:
        lines.append(f"\n_Truncated in markdown: showing {limit} of {len(rows)} rows._")
    return "\n".join(lines)


def render_doc() -> str:
    return "\n\n".join(
        [
            "# 3343 — epsilon_EM Public Hodge/Poynting Zero Or Bound Under AX1090",
            f"Generated: `{RUN_UTC}`",
            "## Summary\n"
            "- The clean EM route is now explicit: use the public Maxwell action, vary it with respect to the observed metric, and count Poynting as EM Hilbert-stress flux.\n"
            "- This gives an exact conditional zero theorem for `epsilon_EM`, but not a promoted MTS claim because hidden `Z_Q`, current lattice, Hodge/readout, and boundary flux ownership are not parent-signed.\n"
            "- The least-scrutiny discipline is to **not** add Poynting as a separate background force unless a new parent vertex is derived and bounded.\n"
            "- No local-GR, Maxwell, alpha, WEP, R10, or source-coupling claim is made.",
            "## Public Maxwell Action Derivation\n" + markdown_table(maxwell_derivation_rows()),
            "## Hodge/Poynting Zero Audit\n" + markdown_table(hodge_poynting_zero_rows()),
            "## epsilon_EM Residual Decomposition\n" + markdown_table(residual_decomposition_rows()),
            "## Partial Zero Certificate\n" + markdown_table(partial_zero_rows()),
            "## FRV3340 epsilon_EM Component Rows\n" + markdown_table(component_rows()),
            "## Poynting Double-Count Guard\n" + markdown_table(double_count_guard_rows()),
            "## Promotion Gates\n" + markdown_table(promotion_gate_rows()),
            "## Decision Ledger\n" + markdown_table(decision_rows()),
            "## Next Target\n" + markdown_table(next_target_rows()),
        ]
    ) + "\n"


def validate_outputs(formalization_before: dict[str, tuple[int, int]]) -> list[dict[str, Any]]:
    sources = source_rows()
    derivation = maxwell_derivation_rows()
    residuals = residual_decomposition_rows()
    components = component_rows()
    guards = double_count_guard_rows()
    gates = promotion_gate_rows()
    output_paths = [path for key, path in OUTPUTS.items() if key != "validation"]
    formalization_changed = changed_count(formalization_before, snapshot_tree(FW))
    checks = [
        {
            "check_id": "VAL3343_0_sources_exist",
            "check": "all cited local source paths exist",
            "passed": all(row["exists"] == "true" for row in sources),
            "detail": "",
        },
        {
            "check_id": "VAL3343_1_sources_parse",
            "check": "all cited local source paths parse",
            "passed": all(row["parse_ok"] == "true" for row in sources),
            "detail": "",
        },
        {
            "check_id": "VAL3343_2_outputs_parse",
            "check": "all 3343 non-validation outputs parse",
            "passed": all(path.exists() and parse_ok(path) for path in output_paths),
            "detail": "",
        },
        {
            "check_id": "VAL3343_3_derivation_coverage",
            "check": "Maxwell action, metric variation, current variation, Poynting law, and vertical zero rows exist",
            "passed": {row["derivation_id"] for row in derivation}
            == {"EMD3343_0_action", "EMD3343_1_metric_variation", "EMD3343_2_current_variation", "EMD3343_3_poynting_balance", "EMD3343_4_vertical_zero"},
            "detail": "",
        },
        {
            "check_id": "VAL3343_4_residual_terms_complete",
            "check": "epsilon_EM residual decomposition covers b_alpha, delta_J, delta_star, DeltaT_EM, and Poynting",
            "passed": {row["component"] for row in residuals}
            == {"b_alpha", "delta_J", "delta_star", "||P_EM DeltaT_EM||/||T_EM||", "Phi_Poynting_unclosed"},
            "detail": "",
        },
        {
            "check_id": "VAL3343_5_component_rows_nonclaim",
            "check": "component rows are runner-shaped but not claim accepted",
            "passed": all(row["valid_for_claim"] == "false" and row["runner_acceptance"] == "false" for row in components),
            "detail": "",
        },
        {
            "check_id": "VAL3343_6_double_count_guard",
            "check": "Poynting double-counting is explicitly forbidden",
            "passed": any(row["guard_id"] == "DCG3343_1_double_count" and row["forbidden"] == "true" for row in guards),
            "detail": "",
        },
        {
            "check_id": "VAL3343_7_no_claim",
            "check": "epsilon_EM parent-zero, finite numeric bound, and local-GR gates remain false",
            "passed": all(
                row["passed"] == "false"
                for row in gates
                if row["gate_id"] in {"GATE3343_2_parent_signed_epsilon_zero", "GATE3343_3_finite_numeric_epsilon_bound", "GATE3343_4_local_GR_claim"}
            ),
            "detail": "",
        },
        {
            "check_id": "VAL3343_8_next_target",
            "check": "next target attacks no-hidden Z_Q and source-current universality",
            "passed": any("Z_Q" in row["objective"] for row in next_target_rows())
            and any("current" in row["objective"] for row in next_target_rows()),
            "detail": "",
        },
        {
            "check_id": "VAL3343_9_formalization_untouched",
            "check": "formalization-workbench modified-file count remains zero by this script",
            "passed": formalization_changed == 0,
            "detail": f"formalization_changed_count={formalization_changed}",
        },
    ]
    overall = all(bool(check["passed"]) for check in checks)
    checks.append(
        {
            "check_id": "VAL3343_10_overall",
            "check": "3343 validation overall",
            "passed": overall,
            "detail": "all required checks passed" if overall else "one or more checks failed",
        }
    )
    for check in checks:
        check["passed"] = bool_str(bool(check["passed"]))
    return checks


def main() -> None:
    formalization_before = snapshot_tree(FW)
    OUT.mkdir(parents=True, exist_ok=True)
    write_csv(OUTPUTS["sources"], source_rows())
    write_csv(OUTPUTS["maxwell_derivation"], maxwell_derivation_rows())
    write_csv(OUTPUTS["hodge_poynting_zero"], hodge_poynting_zero_rows())
    write_csv(OUTPUTS["residual_decomposition"], residual_decomposition_rows())
    write_csv(OUTPUTS["partial_zero"], partial_zero_rows())
    write_csv(OUTPUTS["component_rows"], component_rows())
    write_csv(OUTPUTS["double_count_guard"], double_count_guard_rows())
    write_csv(OUTPUTS["promotion_gates"], promotion_gate_rows())
    write_csv(OUTPUTS["decision"], decision_rows())
    write_csv(OUTPUTS["next"], next_target_rows())
    DOC.write_text(render_doc(), encoding="utf-8")
    write_csv(OUTPUTS["validation"], validate_outputs(formalization_before))
    if PYCACHE.exists():
        shutil.rmtree(PYCACHE)


if __name__ == "__main__":
    main()
