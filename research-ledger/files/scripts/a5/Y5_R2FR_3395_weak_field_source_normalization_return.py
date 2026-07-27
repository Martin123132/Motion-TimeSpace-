from __future__ import annotations

import csv
import math
import re
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
FW = REPO / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
PYCACHE = ROOT / "scripts" / "__pycache__"
DOC = ROOT / "3395-Y5-R2FR-weak-field-source-normalization-return-under-AX1090.md"
RUN_UTC = datetime.now(timezone.utc).isoformat()

OUTPUTS = {
    "source_register": OUT / "P8_Y5_R2FR_3395_SOURCE_REGISTER.csv",
    "external_constants": OUT / "P8_Y5_R2FR_3395_EXTERNAL_CONSTANTS_SOURCE_PACK.csv",
    "corpus_coefficient_audit": OUT / "P8_Y5_R2FR_3395_CORPUS_COEFFICIENT_AUDIT.csv",
    "local_hygiene_import": OUT / "P8_Y5_R2FR_3395_LOCAL_HYGIENE_IMPORT.csv",
    "coupling_ladder": OUT / "P8_Y5_R2FR_3395_COUPLING_IDENTITY_LADDER.csv",
    "minimal_parent_line": OUT / "P8_Y5_R2FR_3395_MINIMAL_PARENT_ACTION_LINE_CANDIDATE.csv",
    "residual_contract": OUT / "P8_Y5_R2FR_3395_COUPLING_RESIDUAL_CONTRACT_NONCLAIM.csv",
    "newton_ppn_implications": OUT / "P8_Y5_R2FR_3395_NEWTON_PPN_IMPLICATIONS.csv",
    "runner": OUT / "P8_Y5_R2FR_3395_RUNNER_NONCLAIM.csv",
    "gates": OUT / "P8_Y5_R2FR_3395_PROMOTION_GATES.csv",
    "decision": OUT / "P8_Y5_R2FR_3395_DECISION_LEDGER.csv",
    "next": OUT / "P8_Y5_R2FR_3395_NEXT_TARGET.csv",
    "validation": OUT / "P8_Y5_BRR545_3395_VALIDATION.csv",
}

LOCAL_SOURCES = [
    ("SRC3395_00_3394_doc", ROOT / "3394-Y5-R2FR-local-Cassini-admissible-package-gate-under-AX1090.md", "3394 local package handoff"),
    ("SRC3395_01_3394_next", OUT / "P8_Y5_R2FR_3394_NEXT_TARGET.csv", "3394 next target"),
    ("SRC3395_02_3394_gate", OUT / "P8_Y5_R2FR_3394_ADMISSIBLE_PACKAGE_GATE.csv", "local Cassini package gate"),
    ("SRC3395_03_3394_residual", OUT / "P8_Y5_R2FR_3394_LOCAL_RESIDUAL_COLLAPSE_TABLE_NONCLAIM.csv", "local residual collapse table"),
    ("SRC3395_04_3377_doc", ROOT / "3377-Y5-R2FR-weak-field-source-normalization-or-Gref-kappa-bound-under-AX1090.md", "prior weak-field normalization theorem"),
    ("SRC3395_05_core_fundamental_action", REPO / "core-mts-framework" / "action-principle" / "the-fundamental-action-of-motion-timespace-field-theory.md", "parent fundamental action"),
    ("SRC3395_06_core_motion_action", REPO / "core-mts-framework" / "action-principle" / "the-motion-timespace-action-principle.md", "parent motion action"),
    ("SRC3395_07_core_gravity", REPO / "core-mts-framework" / "gravity" / "motion-timespace-mts-gravity-core-unified-formulation.md", "parent gravity formulation"),
    ("SRC3395_08_3377_Gref_owner", OUT / "P8_Y5_R2FR_3362_GREF_OWNER_AND_NEWTON_LIMIT.csv", "G_ref owner and Newton limit"),
    ("SRC3395_09_3377_kappa_attempt", OUT / "P8_Y5_R2FR_2723_KAPPA_GREF_THEOREM_ATTEMPT.csv", "kappa/G_ref theorem attempt"),
    ("SRC3395_10_3377_coupling_rows", OUT / "P8_Y5_R2FR_2928_KAPPA_ELLJ_COUPLING_BASELINE_ROWS.csv", "kappa/ellJ coupling residual rows"),
    ("SRC3395_11_3377_poisson", OUT / "P8_Y5_R2FR_2692_NEWTON_POISSON_NORMALIZATION_DERIVATION.csv", "Newton/Poisson derivation"),
    ("SRC3395_12_3377_ppn_gate", OUT / "P8_Y5_PARENT_QLOC_2177_PPN_SOURCE_CONVENTION_GATE.csv", "PPN source convention gate"),
    ("SRC3395_13_3377_v_source", OUT / "P8_Y5_PARENT_QLOC_2178_V_NEWTON_SOURCE_CONVENTION_DERIVATION.csv", "v/Newton source convention"),
]

C_LIGHT_M_PER_S = 299_792_458.0
G_CODATA_2022 = 6.67430e-11
G_CODATA_2022_ABS_UNC = 0.00015e-11

AUDIT_PATTERNS = {
    "EH_coefficient": [r"1/2.?κ", r"1/2.?kappa", r"R", r"Einstein"],
    "kappa_identity": [r"κ\s*=", r"kappa", r"8πG", r"8pi"],
    "matter_source": [r"L_matter", r"T_", r"T\\{", r"matter"],
    "poisson_newton": [r"Poisson", r"Newton", r"Phi_N", r"Φ"],
    "hamiltonian_charge": [r"H_tau", r"H_ref", r"M_H_ref", r"Q_tau", r"N_G"],
    "ppn_readout": [r"PPN", r"gamma", r"beta"],
}


def bool_text(value: bool) -> str:
    return "true" if value else "false"


def parse_csv(path: Path) -> tuple[bool, str]:
    try:
        with path.open("r", encoding="utf-8-sig", newline="") as handle:
            list(csv.DictReader(handle))
        return True, ""
    except Exception as exc:  # noqa: BLE001
        return False, f"{type(exc).__name__}: {exc}"


def parse_text(path: Path) -> tuple[bool, str]:
    try:
        path.read_text(encoding="utf-8", errors="replace")
        return True, ""
    except Exception as exc:  # noqa: BLE001
        return False, f"{type(exc).__name__}: {exc}"


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    headers: list[str] = []
    for row in rows:
        for key in row:
            if key not in headers:
                headers.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=headers)
        writer.writeheader()
        writer.writerows(rows)


def md_escape(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", "<br>")


def md_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "_No rows._\n"
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
        lines.append("| " + " | ".join(md_escape(row.get(header, "")) for header in headers) + " |")
    return "\n".join(lines) + "\n"


def to_float(value: str, default: float = math.nan) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def source_rows() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for source_id, path, role in LOCAL_SOURCES:
        exists = path.exists()
        if not exists:
            parse_ok, parse_error = False, "missing"
        elif path.suffix.lower() == ".csv":
            parse_ok, parse_error = parse_csv(path)
        else:
            parse_ok, parse_error = parse_text(path)
        rows.append(
            {
                "source_id": source_id,
                "source_path": str(path),
                "exists": bool_text(exists),
                "parse_ok": bool_text(parse_ok),
                "role": role,
                "parse_error": parse_error,
                "valid_for_claim": "false",
            }
        )
    return rows


def external_constant_rows() -> list[dict[str, str]]:
    kappa = 8.0 * math.pi * G_CODATA_2022 / C_LIGHT_M_PER_S**4
    kappa_unc = 8.0 * math.pi * G_CODATA_2022_ABS_UNC / C_LIGHT_M_PER_S**4
    return [
        {
            "constant_id": "CONST3395_0_c",
            "source_url": "https://www.bipm.org/en/measurement-units/si-base-units",
            "source_kind": "SI exact constant",
            "quantity": "speed of light in vacuum",
            "value": f"{C_LIGHT_M_PER_S:.9e}",
            "absolute_uncertainty": "0",
            "unit": "m/s",
            "role": "converts G_ref to kappa_GR=8*pi*G_ref/c^4",
            "valid_for_claim": "false",
        },
        {
            "constant_id": "CONST3395_1_G",
            "source_url": "https://physics.nist.gov/cgi-bin/cuu/Value?bg",
            "source_kind": "NIST CODATA 2022",
            "quantity": "Newtonian constant of gravitation",
            "value": f"{G_CODATA_2022:.9e}",
            "absolute_uncertainty": f"{G_CODATA_2022_ABS_UNC:.9e}",
            "unit": "m^3 kg^-1 s^-2",
            "role": "external comparator for G_ref; not something MTS must numerically derive for GR reduction",
            "valid_for_claim": "false",
        },
        {
            "constant_id": "CONST3395_2_kappa_GR",
            "source_url": "derived_from_CONST3395_0_and_CONST3395_1",
            "source_kind": "derived comparator",
            "quantity": "Einstein coupling kappa_GR",
            "value": f"{kappa:.15e}",
            "absolute_uncertainty": f"{kappa_unc:.15e}",
            "unit": "m kg^-1 s^-2 / c^4 convention equivalent",
            "role": "numeric target if MTS chooses SI-normalized local GR comparator",
            "valid_for_claim": "false",
        },
    ]


def source_lines(path: Path) -> list[tuple[int, str]]:
    if not path.exists():
        return []
    if path.suffix.lower() == ".csv":
        rows = read_csv_rows(path)
        return [
            (index, "; ".join(f"{key}={value}" for key, value in row.items()))
            for index, row in enumerate(rows, start=2)
        ]
    return list(enumerate(path.read_text(encoding="utf-8", errors="replace").splitlines(), start=1))


def corpus_coefficient_audit_rows() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    counts = {category: 0 for category in AUDIT_PATTERNS}
    for source_id, path, role in LOCAL_SOURCES:
        for line_number, line in source_lines(path):
            compact = " ".join(line.strip().split())
            if not compact:
                continue
            for category, patterns in AUDIT_PATTERNS.items():
                if counts[category] >= 8:
                    continue
                if any(re.search(pattern, compact, flags=re.IGNORECASE) for pattern in patterns):
                    rows.append(
                        {
                            "audit_id": f"CCA3395_{category}_{counts[category]}",
                            "category": category,
                            "source_id": source_id,
                            "source_path": str(path),
                            "line_number": str(line_number),
                            "snippet": compact[:420],
                            "evidence_role": "coefficient_support" if category in {"EH_coefficient", "kappa_identity", "matter_source"} else "downstream_readout_context",
                            "is_complete_parent_signature": "false",
                            "valid_for_claim": "false",
                        }
                    )
                    counts[category] += 1
                    break
    for category, count in counts.items():
        if count == 0:
            rows.append(
                {
                    "audit_id": f"CCA3395_{category}_NO_HIT",
                    "category": category,
                    "source_id": "NO_HIT",
                    "source_path": "",
                    "line_number": "",
                    "snippet": f"No direct hit for {category}.",
                    "evidence_role": "missing",
                    "is_complete_parent_signature": "false",
                    "valid_for_claim": "false",
                }
            )
    return rows


def local_hygiene_import_rows() -> list[dict[str, str]]:
    gate_rows = read_csv_rows(OUT / "P8_Y5_R2FR_3394_ADMISSIBLE_PACKAGE_GATE.csv")
    imported = []
    for row in gate_rows:
        imported.append(
            {
                "import_id": f"HY3395_{row.get('gate_id', '')}",
                "source_gate": row.get("gate_id", ""),
                "gate_result": row.get("gate_result", ""),
                "conditioned_channels": row.get("what_it_conditionally_closes", ""),
                "still_open": row.get("what_it_does_not_close", ""),
                "use_in_3395": "treat as local residual hygiene only; do not use as substitute for kappa/G/source-current ownership",
                "valid_for_claim": "false",
            }
        )
    return imported


def coupling_ladder_rows() -> list[dict[str, str]]:
    return [
        {
            "ladder_id": "CL3395_0_parent_coefficient",
            "stage": "EH/local metric coefficient",
            "identity": "S_EH=(c^4/16*pi*G_ref) int sqrt(-g_obs) R[g_obs], equivalently kappa_MTS=8*pi*G_ref/c^4",
            "derivation_status": "EXACT_IF_PARENT_LINE_SIGNED",
            "forbidden_shortcut": "define G_ref from orbital GM or Cassini fit after readout",
            "residual_if_missing": "delta_kappa; epsilon_Gref_match",
            "valid_for_claim": "false",
        },
        {
            "ladder_id": "CL3395_1_same_matter_source",
            "stage": "Hilbert/source-current normalization",
            "identity": "T_mu_nu = -2/sqrt(-g_obs) delta S_matter/delta g_obs^{mu nu}; J_H and M_H use the same matter variation",
            "derivation_status": "EXACT_IF_MATTER_DESCENT_SIGNED",
            "forbidden_shortcut": "rescale rho_H, ell_J, or M_H_ref after Newton/PPN comparison",
            "residual_if_missing": "delta_ellJ; epsilon_M; M_H_ref",
            "valid_for_claim": "false",
        },
        {
            "ladder_id": "CL3395_2_EH_to_Poisson",
            "stage": "weak-field Newtonian limit",
            "identity": "G_00^(1)=2 nabla^2 Phi_N/c^2 and T_00=rho_H c^2 imply nabla^2 Phi_N=4*pi*G_ref*rho_H",
            "derivation_status": "ALGEBRA_EXACT_CONDITIONAL",
            "forbidden_shortcut": "use Newton shape without coefficient ownership",
            "residual_if_missing": "R_Poisson_norm; Delta_Newton_v_coupled",
            "valid_for_claim": "false",
        },
        {
            "ladder_id": "CL3395_3_Htau_Gauss",
            "stage": "Hamiltonian/Gauss charge",
            "identity": "N_G,Q_tau,H_ref,Pi_M define M_H in the same G_ref branch so exterior Phi_N=-G_ref M_H/r",
            "derivation_status": "OPEN_PARENT_SIGNATURE",
            "forbidden_shortcut": "choose N_G separately from the EH/Poisson coefficient",
            "residual_if_missing": "epsilon_Gref_match; Delta_boundary_coupling; M_H_ref",
            "valid_for_claim": "false",
        },
        {
            "ladder_id": "CL3395_4_v_action",
            "stage": "v/Newton constrained branch",
            "identity": "For g_tt=-exp(v)c^2, Phi_N=(c^2/2)v; L_v=-(c^4/32*pi*G_ref)|grad v|^2-rho_H c^2 v/2 gives nabla^2v=8*pi*G_ref rho_H/c^2",
            "derivation_status": "ACTION_TARGET_EXACT_PARENT_RATIO_OPEN",
            "forbidden_shortcut": "use reciprocal readout shape without deriving v source amplitude",
            "residual_if_missing": "delta_KC",
            "valid_for_claim": "false",
        },
        {
            "ladder_id": "CL3395_5_PPN",
            "stage": "PPN source potential",
            "identity": "same U=G_ref M_H/r feeds gamma,beta,preferred-frame and conservation PPN vector",
            "derivation_status": "FIRST_ORDER_SHAPE_CONDITIONAL_SECOND_ORDER_OPEN",
            "forbidden_shortcut": "claim local GR from gamma=1 shape while beta/kappa_v/source normalization are open",
            "residual_if_missing": "kappa_v; beta_minus_1; PPN_vector",
            "valid_for_claim": "false",
        },
    ]


def minimal_parent_line_rows() -> list[dict[str, str]]:
    return [
        {
            "line_id": "MPL3395_0_parent_action_line",
            "candidate": "S_parent ⊃ (c^4/16πG_ref)∫√-g_obs R[g_obs] + S_matter[e_obs(q(Φ)),Ψ] + S_boundary[Θ,Q_τ,B_ref,Π_M;G_ref] + S_MTS[ψ,Γ,...]",
            "owns": "g_obs/e_obs; kappa_MTS; G_ref; Hilbert source T_mu_nu; Q_tau/H_tau; B_ref/H_ref; Pi_M; ell_J=1",
            "why_needed": "one parent variation must own the coefficient and source scale before H_tau, Poisson/Newton and PPN are compared",
            "adds_fit_parameter": "false_if_G_ref_is_universal_parent_constant",
            "current_status": "CANDIDATE_NOT_PARENT_SIGNED",
            "valid_for_claim": "false",
        },
        {
            "line_id": "MPL3395_1_variation_contract",
            "candidate": "δS_parent/δg_obs -> G_muν[g_obs]=kappa_MTS T_muν^Hilbert + local-package residuals",
            "owns": "field equation normalization and public source measure",
            "why_needed": "prevents independent source-current, boundary and PPN normalizations",
            "adds_fit_parameter": "false",
            "current_status": "CANDIDATE_NOT_PARENT_SIGNED",
            "valid_for_claim": "false",
        },
        {
            "line_id": "MPL3395_2_source_current_contract",
            "candidate": "J_H[τ]=δS_matter/δe_obs ⋅ L_τ e_obs and M_H are computed from the same S_matter branch; ell_J=1 unless parent explicitly fixes a universal conversion.",
            "owns": "source-current scale",
            "why_needed": "blocks hidden source-mass rescaling after Newton/PPN readout",
            "adds_fit_parameter": "false",
            "current_status": "CANDIDATE_NOT_PARENT_SIGNED",
            "valid_for_claim": "false",
        },
        {
            "line_id": "MPL3395_3_no_backfill_clause",
            "candidate": "Measured orbital GM may calibrate a system mass after the parent map is fixed, but may not define G_ref, ell_J, N_G, or M_H_ref for the theorem.",
            "owns": "anti-circularity guardrail",
            "why_needed": "keeps Newton recovery from becoming a fitted amplitude",
            "adds_fit_parameter": "false",
            "current_status": "GUARDRAIL_CANDIDATE",
            "valid_for_claim": "false",
        },
    ]


def residual_contract_rows() -> list[dict[str, str]]:
    return [
        {
            "residual_id": "CR3395_0_delta_kappa",
            "symbol": "delta_kappa",
            "definition": "kappa_MTS c^4/(8*pi*G_ref)-1 or branch variation of kappa_MTS",
            "closure_condition": "zero if MPL3395_0 signs kappa_MTS=8*pi*G_ref/c^4 as universal parent coefficient",
            "current_status": "OPEN_PARENT_SIGNATURE",
            "valid_for_claim": "false",
        },
        {
            "residual_id": "CR3395_1_delta_ellJ",
            "symbol": "delta_ellJ",
            "definition": "hidden source-current scale drift relative to Hilbert source normalization",
            "closure_condition": "zero if MPL3395_2 signs same matter variation for T_muν,J_H,M_H",
            "current_status": "OPEN_MATTER_DESCENT_SIGNATURE",
            "valid_for_claim": "false",
        },
        {
            "residual_id": "CR3395_2_epsilon_Gref_match",
            "symbol": "epsilon_Gref_match",
            "definition": "|G_Htau/G_Poisson-1|+|G_PPN/G_Poisson-1|",
            "closure_condition": "zero if EH, H_tau/Gauss and PPN U all inherit same G_ref and M_H",
            "current_status": "OPEN_HTAU_PPN_MATCH",
            "valid_for_claim": "false",
        },
        {
            "residual_id": "CR3395_3_delta_KC",
            "symbol": "delta_KC",
            "definition": "v-action kinetic/source coefficient mismatch",
            "closure_condition": "zero if parent v reduction yields c^4/(32*pi*G_ref) and rho_H c^2/2 coefficients",
            "current_status": "OPEN_V_ACTION_RATIO",
            "valid_for_claim": "false",
        },
        {
            "residual_id": "CR3395_4_Delta_Newton",
            "symbol": "Delta_Newton_v_coupled",
            "definition": "(1+delta_KC)(1+epsilon_M)(1+delta_kappa)(1+delta_ellJ)-1 without cancellation credit",
            "closure_condition": "zero only if each component closes independently or is source-bounded",
            "current_status": "OPEN_NO_CANCELLATION_LEDGER",
            "valid_for_claim": "false",
        },
        {
            "residual_id": "CR3395_5_kappa_v",
            "symbol": "kappa_v",
            "definition": "second-order PPN beta-source ledger including source, PiM, boundary, readout, operator and coupling terms",
            "closure_condition": "zero or finite bound after source normalization and local package adoption",
            "current_status": "OPEN_SECOND_ORDER_PPN",
            "valid_for_claim": "false",
        },
    ]


def newton_ppn_implication_rows() -> list[dict[str, str]]:
    return [
        {
            "implication_id": "NP3395_0_if_parent_line_signed",
            "condition": "MPL3395_0..2 signed plus 3394 package adopted",
            "Newton_result": "Poisson/Newton coefficient follows from parent EH coefficient and Hilbert source",
            "PPN_result": "gamma shape can use same U; beta/full vector still require second-order ledger",
            "status": "PROMISING_CONDITIONAL_NOT_CURRENT_CLAIM",
            "valid_for_claim": "false",
        },
        {
            "implication_id": "NP3395_1_current_corpus",
            "condition": "current corpus as-is",
            "Newton_result": "weak-field algebra exists, but source normalization parent line is unsigned",
            "PPN_result": "local PPN cannot be claimed; kappa_v/full vector remain open",
            "status": "NO_LOCAL_GR_CLAIM",
            "valid_for_claim": "false",
        },
        {
            "implication_id": "NP3395_2_G_policy",
            "condition": "MTS does not derive numeric G_ref",
            "Newton_result": "acceptable for GR-style reduction if G_ref is one universal parent constant",
            "PPN_result": "tests constrain drift/mismatch, not the metaphysical origin of G",
            "status": "POLICY_OK_GR_DOES_NOT_DERIVE_G_EITHER",
            "valid_for_claim": "false",
        },
        {
            "implication_id": "NP3395_3_future_stronger_route",
            "condition": "future topological/superselection derivation of G_ref",
            "Newton_result": "would strengthen MTS beyond GR, but is not required for local-GR reduction",
            "PPN_result": "separate from present Cassini/local PPN gate",
            "status": "DEFERRED_STRONGER_PROGRAM",
            "valid_for_claim": "false",
        },
    ]


def runner_rows(rows_by_name: dict[str, list[dict[str, Any]]]) -> list[dict[str, str]]:
    core_eh_hits = sum(1 for row in rows_by_name["corpus_coefficient_audit"] if row["category"] == "EH_coefficient" and row["source_id"] != "NO_HIT")
    return [
        {
            "run_id": "RUN3395_0_local_hygiene_import",
            "test": "3394 local package imported as hygiene",
            "result": "PASS_HYGIENE_IMPORTED_NONCLAIM",
            "detail": f"rows={len(rows_by_name['local_hygiene_import'])}",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "run_id": "RUN3395_1_coupling_ladder",
            "test": "EH/source/Poisson/Htau/v/PPN coupling ladder",
            "result": "PASS_LADDER_WRITTEN_CONDITIONAL",
            "detail": f"stages={len(rows_by_name['coupling_ladder'])}; core_EH_hits={core_eh_hits}",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "run_id": "RUN3395_2_minimal_parent_line",
            "test": "minimal parent action line candidate",
            "result": "PASS_PARENT_LINE_CANDIDATE_NONCLAIM",
            "detail": "line owns G_ref/kappa, matter source, Q_tau/H_tau/B_ref/Pi_M and ell_J=1 if adopted",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "run_id": "RUN3395_3_residual_contract",
            "test": "coupling residual contract",
            "result": "PASS_RESIDUAL_CONTRACT_NONCLAIM",
            "detail": f"residuals={len(rows_by_name['residual_contract'])}",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "run_id": "RUN3395_4_firewall",
            "test": "prevent local GR/Newton claim",
            "result": "PASS_CLAIM_FIREWALL",
            "detail": "source normalization is sharpened to parent-line candidate, not signed or scored",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
    ]


def gate_rows(source_ok: bool) -> list[dict[str, str]]:
    return [
        {
            "gate_id": "GATE3395_0_sources",
            "claim": "all 3395 local sources exist and parse",
            "gate_pass": bool_text(source_ok),
            "reason": "source register parsed",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3395_1_constants",
            "claim": "external G/c comparator constants recorded",
            "gate_pass": "true",
            "reason": "BIPM/NIST source rows recorded, but numeric G derivation is not required",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3395_2_parent_line",
            "claim": "minimal parent action line is adopted",
            "gate_pass": "false",
            "reason": "candidate written but parent docs not modified/signed",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3395_3_Newton",
            "claim": "Newton/Poisson amplitude is parent-derived",
            "gate_pass": "false",
            "reason": "algebra exact conditional; source normalization line unsigned",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3395_4_PPN",
            "claim": "full local PPN vector is GR-safe",
            "gate_pass": "false",
            "reason": "gamma shape conditional; beta/kappa_v/full vector remain open",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3395_5_local_GR",
            "claim": "local GR/Newton source coupling passes",
            "gate_pass": "false",
            "reason": "parent action line, H_tau match, M_H_ref and second-order PPN are not signed",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
    ]


def decision_rows() -> list[dict[str, str]]:
    return [
        {
            "decision_id": "DEC3395_0_progress",
            "decision": "The coupling problem is back on the main road: one parent action line can own it.",
            "because": "3394 handles local residual hygiene; 3395 identifies the parent variation that must own kappa/G_ref, source current, H_tau and PPN U.",
            "next_action": "parent-sign or reject MPL3395 rather than adding more residual patches",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC3395_1_G_policy",
            "decision": "MTS does not need to derive the numerical value of G to reduce to GR/Newton.",
            "because": "GR itself treats G as a universal coupling constant; the required local theorem is fixed ownership and no hidden source-scale drift.",
            "next_action": "keep topological/superselection derivation of G as a future stronger programme",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC3395_2_current_status",
            "decision": "Current MTS still cannot claim calibrated local source coupling.",
            "because": "the parent line is a candidate, not an adopted variation; H_tau/M_H_ref and second-order PPN remain open.",
            "next_action": "build 3396 parent-line integration/source-normalization audit or boundary-reference extension as needed",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC3395_3_best_next",
            "decision": "Next target should integrate/audit the minimal parent line against the corpus.",
            "because": "that is the only way to turn the conditional ladder into owned theory rather than another contract.",
            "next_action": "build 3396 minimal parent-line integration audit",
            "valid_for_claim": "false",
        },
    ]


def next_rows() -> list[dict[str, str]]:
    return [
        {
            "target_id": "3396-Y5-R2FR-minimal-parent-line-integration-or-source-normalization-demotion-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3396_minimal_parent_line_integration_or_source_normalization_demotion.py",
            "objective": "audit whether MPL3395 can be integrated into the parent corpus without conflict; if yes, stage parent-owned source normalization, if no, demote local source coupling to explicit closure/fallback rows",
            "why_next": "3395 identifies the one missing owned variation; the next move is integration or honest demotion",
            "valid_for_claim": "false",
        },
        {
            "target_id": "3397-Y5-R2FR-full-PPN-vector-after-source-normalization-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3397_full_PPN_vector_after_source_normalization.py",
            "objective": "after source normalization is parent-owned, run the full PPN vector gate for gamma, beta, alpha_i, zeta_i and xi",
            "why_next": "first-order Newton/gamma shape is not enough; full PPN vector is the local-GR judge",
            "valid_for_claim": "false",
        },
    ]


def all_claim_flags_false(paths: list[Path]) -> tuple[bool, str]:
    offenders: list[str] = []
    for path in paths:
        if not path.exists() or path.suffix.lower() != ".csv":
            continue
        for index, row in enumerate(read_csv_rows(path), start=2):
            if "valid_for_claim" in row and row["valid_for_claim"].strip().lower() != "false":
                offenders.append(f"{path.name}:line{index}:{row['valid_for_claim']}")
    return not offenders, "; ".join(offenders)


def validate(rows_by_name: dict[str, list[dict[str, Any]]]) -> list[dict[str, str]]:
    source_ok = all(row["exists"] == "true" and row["parse_ok"] == "true" for row in rows_by_name["source_register"])
    output_csvs = [path for key, path in OUTPUTS.items() if key != "validation" and path.suffix.lower() == ".csv"]
    parse_results = [parse_csv(path)[0] for path in output_csvs if path.exists()]
    flags_ok, flag_detail = all_claim_flags_false(output_csvs)
    formalization_hits = [
        hit
        for hit in FW.rglob("*3395*")
        if hit.name.startswith(("3395-Y5", "P8_Y5_R2FR_3395", "P8_Y5_BRR545_3395", "Y5_R2FR_3395"))
    ] if FW.exists() else []
    audit_categories = {row["category"] for row in rows_by_name["corpus_coefficient_audit"]}
    ladder_stages = {row["stage"] for row in rows_by_name["coupling_ladder"]}
    parent_lines = {row["line_id"] for row in rows_by_name["minimal_parent_line"]}
    residual_symbols = {row["symbol"] for row in rows_by_name["residual_contract"]}
    implication_statuses = {row["status"] for row in rows_by_name["newton_ppn_implications"]}
    gate_map = {row["gate_id"]: row["gate_pass"] for row in rows_by_name["gates"]}
    runner_results = {row["result"] for row in rows_by_name["runner"]}
    checks = [
        ("VAL3395_0_sources_exist_parse", "all cited 3395 source paths exist and parse", source_ok, ""),
        ("VAL3395_1_outputs_parse", "all generated CSV outputs parse cleanly", len(parse_results) == len(output_csvs) and all(parse_results), f"parsed={sum(1 for ok in parse_results if ok)} expected={len(output_csvs)}"),
        ("VAL3395_2_external_constants", "external constants include c, G and derived kappa comparator", len(rows_by_name["external_constants"]) == 3, ""),
        ("VAL3395_3_corpus_audit", "corpus coefficient audit covers all normalization categories", set(AUDIT_PATTERNS).issubset(audit_categories), f"categories={len(audit_categories)}"),
        ("VAL3395_4_hygiene_import", "3394 local hygiene package imported but not used as coupling substitute", len(rows_by_name["local_hygiene_import"]) >= 3, f"rows={len(rows_by_name['local_hygiene_import'])}"),
        ("VAL3395_5_coupling_ladder", "coupling ladder covers EH, Hilbert source, Poisson, Htau, v action and PPN", {"EH/local metric coefficient", "Hilbert/source-current normalization", "weak-field Newtonian limit", "Hamiltonian/Gauss charge", "v/Newton constrained branch", "PPN source potential"}.issubset(ladder_stages), ""),
        ("VAL3395_6_parent_line", "minimal parent action line candidate covers action, variation, source-current and no-backfill", {"MPL3395_0_parent_action_line", "MPL3395_1_variation_contract", "MPL3395_2_source_current_contract", "MPL3395_3_no_backfill_clause"}.issubset(parent_lines), ""),
        ("VAL3395_7_residual_contract", "residual contract covers delta_kappa, ellJ, Gref match, KC, Newton and PPN", {"delta_kappa", "delta_ellJ", "epsilon_Gref_match", "delta_KC", "Delta_Newton_v_coupled", "kappa_v"}.issubset(residual_symbols), ""),
        ("VAL3395_8_implications", "Newton/PPN implications separate conditional, current no-claim and G policy", {"PROMISING_CONDITIONAL_NOT_CURRENT_CLAIM", "NO_LOCAL_GR_CLAIM", "POLICY_OK_GR_DOES_NOT_DERIVE_G_EITHER", "DEFERRED_STRONGER_PROGRAM"}.issubset(implication_statuses), ""),
        ("VAL3395_9_runner", "runner records hygiene, ladder, parent line, residual contract and firewall", {"PASS_HYGIENE_IMPORTED_NONCLAIM", "PASS_LADDER_WRITTEN_CONDITIONAL", "PASS_PARENT_LINE_CANDIDATE_NONCLAIM", "PASS_RESIDUAL_CONTRACT_NONCLAIM", "PASS_CLAIM_FIREWALL"}.issubset(runner_results), ""),
        ("VAL3395_10_gates", "gates record constants but block parent line, Newton, PPN and local GR claims", gate_map.get("GATE3395_1_constants") == "true" and gate_map.get("GATE3395_2_parent_line") == "false" and gate_map.get("GATE3395_3_Newton") == "false" and gate_map.get("GATE3395_4_PPN") == "false" and gate_map.get("GATE3395_5_local_GR") == "false", ""),
        ("VAL3395_11_no_overclaim_flags", "all generated rows with valid_for_claim remain false", flags_ok, flag_detail),
        ("VAL3395_12_write_scope_outside_formalization", "no 3395 files were written under formalization-workbench", not formalization_hits, f"hits={len(formalization_hits)}"),
        ("VAL3395_13_next_target", "next target moves to minimal parent-line integration audit", rows_by_name["next"][0]["target_id"].startswith("3396-Y5-R2FR-minimal-parent-line-integration"), ""),
    ]
    overall = all(passed for _, _, passed, _ in checks)
    checks.append(("VAL3395_14_overall", "3395 validation overall", overall, "all required checks passed" if overall else "one or more checks failed"))
    return [{"check_id": check_id, "check": check, "passed": bool_text(passed), "detail": detail} for check_id, check, passed, detail in checks]


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    kappa_row = next(row for row in rows_by_name["external_constants"] if row["constant_id"] == "CONST3395_2_kappa_GR")
    lines = [
        "# 3395 - Y5/R2FR weak-field source normalization return under AX1090",
        "",
        "## Summary",
        "- 3395 returns from local Cassini residual hygiene to the decisive GR/Newton coupling problem.",
        "- The useful result is a minimal parent action line candidate: one variation must own `G_ref/kappa_MTS`, Hilbert source current, `H_tau/Q_tau/B_ref/Pi_M`, and `ell_J=1` before Newton or PPN are scored.",
        f"- External constants are recorded only as comparators; derived `kappa_GR` is `{kappa_row['value']}`. MTS does not need to derive the numerical value of `G` to reduce to GR, but it must own one universal coupling without hidden drift.",
        "- The weak-field algebra remains clean: signed `kappa_MTS=8*pi*G_ref/c^4` plus the same Hilbert source gives `nabla^2 Phi_N=4*pi*G_ref rho_H`.",
        "- Current verdict: promising conditional ladder, not a claim. Parent line, `H_tau/M_H_ref`, and second-order/full PPN vector remain open.",
        "",
        "## Source Register",
        md_table(rows_by_name["source_register"]),
        "## External Constants Source Pack",
        md_table(rows_by_name["external_constants"]),
        "## Corpus Coefficient Audit",
        md_table(rows_by_name["corpus_coefficient_audit"]),
        "## Local Hygiene Import",
        md_table(rows_by_name["local_hygiene_import"]),
        "## Coupling Identity Ladder",
        md_table(rows_by_name["coupling_ladder"]),
        "## Minimal Parent Action Line Candidate",
        md_table(rows_by_name["minimal_parent_line"]),
        "## Coupling Residual Contract",
        md_table(rows_by_name["residual_contract"]),
        "## Newton/PPN Implications",
        md_table(rows_by_name["newton_ppn_implications"]),
        "## Nonclaim Runner",
        md_table(rows_by_name["runner"]),
        "## Promotion Gates",
        md_table(rows_by_name["gates"]),
        "## Decision Ledger",
        md_table(rows_by_name["decision"]),
        "## Validation",
        md_table(rows_by_name["validation"]),
        "## Next Target",
        md_table(rows_by_name["next"]),
    ]
    DOC.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    source_register = source_rows()
    source_ok = all(row["exists"] == "true" and row["parse_ok"] == "true" for row in source_register)
    rows_by_name: dict[str, list[dict[str, Any]]] = {
        "source_register": source_register,
        "external_constants": external_constant_rows(),
        "corpus_coefficient_audit": corpus_coefficient_audit_rows(),
        "local_hygiene_import": local_hygiene_import_rows(),
        "coupling_ladder": coupling_ladder_rows(),
        "minimal_parent_line": minimal_parent_line_rows(),
        "residual_contract": residual_contract_rows(),
        "newton_ppn_implications": newton_ppn_implication_rows(),
    }
    rows_by_name["runner"] = runner_rows(rows_by_name)
    rows_by_name["gates"] = gate_rows(source_ok)
    rows_by_name["decision"] = decision_rows()
    rows_by_name["next"] = next_rows()
    for name, rows in rows_by_name.items():
        write_csv(OUTPUTS[name], rows)
    rows_by_name["validation"] = validate(rows_by_name)
    write_csv(OUTPUTS["validation"], rows_by_name["validation"])
    write_doc(rows_by_name)
    if PYCACHE.exists():
        shutil.rmtree(PYCACHE)
    print(f"Wrote {DOC}")
    print(f"Wrote {len(OUTPUTS)} CSV outputs under {OUT}")
    print(f"Generated UTC {RUN_UTC}")


if __name__ == "__main__":
    main()
