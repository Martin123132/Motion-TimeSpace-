from __future__ import annotations

import csv
import io
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Mapping, Sequence


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from deltaktf_shell_profile_gate import read_csv, write_csv  # noqa: E402


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4516"
CLAIM_ID = "L-358"
MARKER = "PPC4161_SOURCE_FUNCTOR_PARENT_SIGNATURE_OR_FIRST_Y5_COEFFICIENT_FILL_4516"
PACKET_MARKER = "PPC4161_PACKET_SOURCE_FUNCTOR_PARENT_SIGNATURE_OR_FIRST_Y5_COEFFICIENT_FILL_4516"
DECISION = "LOCAL_STATIONARY_HILBERT_SOURCE_SUBTHEOREM_DERIVED_Y5_SUBSET_CONDITIONALLY_CLOSED_NONCLAIM"
NEXT_TARGET = "4517-Y5-R2FR-domain-bulk-species-source-tail-or-coefficient-fill.md"

FORMAL_PATH = FORMAL / "532-PPC4161-source-functor-parent-signature-or-first-Y5-coefficient-fill.md"
DOC_PATH = POST / "4516-Y5-R2FR-source-functor-parent-signature-or-first-Y5-coefficient-fill.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4516_VALIDATION.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4516_SOURCE_REGISTER.csv"
STATIONARY_THEOREM = SOURCE_DIR / "P8_Y5_R2FR_4516_STATIONARY_HILBERT_SOURCE_SUBTHEOREM.csv"
Y5_CLOSURE_MAP = SOURCE_DIR / "P8_Y5_R2FR_4516_Y5_PARTIAL_CLOSURE_MAP.csv"
POYNTING_GUARD = SOURCE_DIR / "P8_Y5_R2FR_4516_EM_POYNTING_STATIONARY_WORLDTUBE_GUARD.csv"
REMAINING_DEBT = SOURCE_DIR / "P8_Y5_R2FR_4516_REMAINING_SOURCE_DEBT.csv"
PARENT_AUDIT = SOURCE_DIR / "P8_Y5_R2FR_4516_PARENT_SIGNATURE_AUDIT.csv"
CLAIM_GATES = SOURCE_DIR / "P8_Y5_R2FR_4516_CLAIM_GATES.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4516_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4516_NEXT_TARGET.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4516_DECISION.csv"

FORMAL_531 = FORMAL / "531-PPC4161-Y5-Y6-source-trace-tail-or-Cmem-Jmem-source-coupling-vector.md"
POST_4515 = POST / "4515-Y5-R2FR-Y5-Y6-source-trace-tail-or-Cmem-Jmem-source-coupling-vector.md"
THEOREM_4515 = SOURCE_DIR / "P8_Y5_R2FR_4515_SOURCE_FUNCTOR_DESCENT_THEOREM.csv"
Y5_4515 = SOURCE_DIR / "P8_Y5_R2FR_4515_Y5_SOURCE_TRACE_VECTOR.csv"
COUPLING_4515 = SOURCE_DIR / "P8_Y5_R2FR_4515_CMEM_JMEM_COUPLING_VECTOR.csv"
JZ_1354 = SOURCE_DIR / "P8_Y5_R10_1354_Y5Y6_JZ_COEFFICIENT_FILL.csv"
SRC_CURRENT = SOURCE_DIR / "P8_source_current_Ward_universality_CONTRACT.csv"
SRC_OWNER = SOURCE_DIR / "P8_source_owner_parent_action_terms_CONTRACT.csv"
HILBERT_DIV = SOURCE_DIR / "P8_Y5_HILBERT_CURRENT_2467_DIVERGENCE_IDENTITY.csv"
HILBERT_EXCHANGE = SOURCE_DIR / "P8_Y5_HILBERT_CURRENT_2467_EXCHANGE_CURRENT_IDENTITY.csv"
HILBERT_VERDICT = SOURCE_DIR / "P8_Y5_HILBERT_CURRENT_2467_PROMOTION_VERDICT.csv"
EM_FLUX = SOURCE_DIR / "P8_Y5_I_matter_EM_flux_status.csv"
EM_JQ = SOURCE_DIR / "P8_Y5_Jq_matter_EM_Poynting_subcomponent_status.csv"
JOINT_OWNER = SOURCE_DIR / "P8_Y5_joint_TQ_NQ_JQ_owner_packet_status.csv"
SN_AUDIT = SOURCE_DIR / "P8_SOURCE_NORMALIZATION_CHANNEL_AUDIT.csv"
SN_FILL = SOURCE_DIR / "P8_SOURCE_NORMALIZATION_COEFFICIENT_FILL.csv"

STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="ignore")


def write_text(path: Path, body: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(body, encoding="utf-8")


def line_of(path: Path, needle: str) -> int:
    if not path.exists() or not needle:
        return 0
    for line_number, line in enumerate(text(path).splitlines(), start=1):
        if needle in line:
            return line_number
    return 0


def md(value: object) -> str:
    return str(value).replace("\n", " ").replace("|", "\\|")


def table(rows: Sequence[Mapping[str, object]]) -> str:
    if not rows:
        return ""
    headers = list(rows[0].keys())
    output = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    for row in rows:
        output.append("| " + " | ".join(md(row.get(header, "")) for header in headers) + " |")
    return "\n".join(output)


def csv_line(values: Sequence[object]) -> str:
    buffer = io.StringIO(newline="")
    writer = csv.writer(buffer)
    writer.writerow(values)
    return buffer.getvalue().strip("\r\n")


def source_rows() -> List[Dict[str, object]]:
    specs = [
        ("SRC4516_00_formal531", "4515 formal handoff", FORMAL_531, "PPC4161_Y5Y6_SOURCE_TRACE_TAIL_OR_CMEM_JMEM_SOURCE_COUPLING_VECTOR_4515", "source-coupling theorem handoff"),
        ("SRC4516_01_post4515", "4515 post handoff", POST_4515, "NT4515_0", "declares source-functor signature/coefficient target"),
        ("SRC4516_02_theorem4515", "4515 source-functor theorem", THEOREM_4515, "SFT4515_1_single_source_functor_zero", "common zero theorem"),
        ("SRC4516_03_y5_4515", "4515 Y5 vector", Y5_4515, "Y5V4515_8_total", "Y5 finite vector"),
        ("SRC4516_04_coupling4515", "4515 Cmem/Jmem vector", COUPLING_4515, "SCV4515_2_Jmem_EM_Poynting", "Poynting guard in Jmem"),
        ("SRC4516_05_jz1354", "1354 raw Y5 rows", JZ_1354, "JZ1354_Y5_6_time_drift", "time drift source-normalization row"),
        ("SRC4516_06_current_contract", "source-current Ward contract", SRC_CURRENT, "SC6_closed_calibrated_mass_projector", "mass projector gate"),
        ("SRC4516_07_owner_contract", "source-owner parent action contract", SRC_OWNER, "A4_mass_flux_projector", "mass-flux projector action"),
        ("SRC4516_08_hilbert_div", "Hilbert current divergence", HILBERT_DIV, "DIV2467_1_full_divergence", "exact product-rule divergence"),
        ("SRC4516_09_hilbert_killing", "Hilbert current Killing route", HILBERT_DIV, "DIV2467_4_Killing_clock", "stationary clock current closure"),
        ("SRC4516_10_hilbert_exchange", "Hilbert current exchange", HILBERT_EXCHANGE, "EXC2467_3_local_stationary_escape", "local stationary escape"),
        ("SRC4516_11_hilbert_verdict", "Hilbert current verdict", HILBERT_VERDICT, "PV2467_2_worldtube", "worldtube mass surface independence"),
        ("SRC4516_12_em_flux", "EM/Poynting flux", EM_FLUX, "CONDITIONAL_ZERO_ELSE_FLUX_BOUND_READY", "no-radiation/flux guard"),
        ("SRC4516_13_em_jq", "EM/Poynting Jq", EM_JQ, "JQ_MATTER_EM_POYNTING_SUBCOMPONENT_BOUND_FILLED", "Poynting finite residual source"),
        ("SRC4516_14_joint_owner", "joint owner packet", JOINT_OWNER, "lambda_F2;b_alpha;kappa_J;w_EM;Phi_EM_boundary", "remaining Poynting owner coefficients"),
        ("SRC4516_15_sn_audit", "source normalization audit", SN_AUDIT, "C1_domain_projector", "remaining hard source channels"),
        ("SRC4516_16_sn_fill", "source normalization coefficient fill", SN_FILL, "F0_c_domain_source_normalization_operator", "first remaining coefficient fill"),
    ]
    rows: List[Dict[str, object]] = []
    for source_id, role, path, needle, note in specs:
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "source_id": source_id,
                "role": role,
                "path": str(path),
                "exists": path.exists(),
                "needle": needle,
                "needle_found": needle in text(path),
                "line": line_of(path, needle),
                "note": note,
                "valid_for_claim": False,
            }
        )
    return rows


def stationary_theorem_rows() -> List[Dict[str, object]]:
    return [
        {
            "theorem_id": "SHS4516_0_current_definition",
            "object": "Hilbert mass current",
            "statement": "Use the 2467 current as the local source-functor candidate in a stationary collar.",
            "formula": "J_M^nu = ell_J T_matter^{nu rho} tau_rho",
            "conditions": "single observed coframe; Hilbert stress; fixed clock one-form tau",
            "result": "candidate measured-mass current",
            "status": "IMPORTED_DERIVED_INPUT",
            "valid_for_claim": False,
        },
        {
            "theorem_id": "SHS4516_1_divergence_identity",
            "object": "current divergence",
            "statement": "The exact product rule isolates the only stationary-collar leakage terms.",
            "formula": "nabla_nu J_M^nu = (nabla_nu ell_J)T^{nu rho}tau_rho + ell_J(nabla_nu T^{nu rho})tau_rho + ell_J T^{nu rho}nabla_(nu tau_rho)",
            "conditions": "none beyond differentiability and symmetric Hilbert stress for the final tau-strain form",
            "result": "leakage is scale drift, stress nonconservation or clock strain",
            "status": "DERIVED",
            "valid_for_claim": False,
        },
        {
            "theorem_id": "SHS4516_2_stationary_zero",
            "object": "stationary current conservation",
            "statement": "In a local stationary collar, constant scale plus matter shell plus Killing clock makes the Hilbert mass current conserved.",
            "formula": "nabla ell_J=0; nabla_mu T^{mu nu}=0; nabla_(mu tau_nu)=0 => nabla_nu J_M^nu=0",
            "conditions": "stationary local collar; parent scale not drifting; no unowned exchange force",
            "result": "J_M has no local divergence in the collar",
            "status": "EXACT_CONDITIONAL_LOCAL_THEOREM",
            "valid_for_claim": False,
        },
        {
            "theorem_id": "SHS4516_3_mass_flux_surface_lock",
            "object": "measured mass flux",
            "statement": "With a q-basic fixed mass projector, the measured monopole is surface/time independent inside the stationary no-flux collar.",
            "formula": "D Pi_M=0 and nabla.(Pi_M J_M)=0 and int_wall n.Pi_M J_M=0 => d M_eff(S_r)/dr = d M_eff/dt = 0",
            "conditions": "fixed Pi_M; no wall flux; compact exterior; no radiative or material current crossing",
            "result": "kills radial M_eff hair and time-drift source-normalization in this local branch",
            "status": "EXACT_CONDITIONAL_LOCAL_THEOREM",
            "valid_for_claim": False,
        },
        {
            "theorem_id": "SHS4516_4_scope_guard",
            "object": "what this does not close",
            "statement": "The stationary Hilbert theorem does not close domain projector mass, finite-range/bulk X, non-EH source operators, species source charge, or absolute calibration by itself.",
            "formula": "Y5_2,Y5_3,Y5_4,Y5_5,Y5_7 remain live unless their own parent clauses close",
            "conditions": "do not upgrade local stationary flux lock into full dynamic source-functor proof",
            "result": "partial closure only",
            "status": "SCOPE_GUARD",
            "valid_for_claim": False,
        },
    ]


def y5_partial_closure_rows() -> List[Dict[str, object]]:
    closure = {
        "JZ1354_Y5_0_radial_Meff_hair": (
            "CONDITIONAL_LOCAL_STATIONARY_ZERO",
            "SHS4516_3 proves dM_eff(S_r)/dr=0 in a q-basic stationary no-flux collar",
            "promote only for local stationary exterior branch; dynamic/range/domain hair still open",
        ),
        "JZ1354_Y5_6_time_drift": (
            "CONDITIONAL_LOCAL_STATIONARY_ZERO",
            "SHS4516_3 proves dM_eff/dt=0 in a stationary no-flux collar",
            "promote only for local stationary exterior branch; global Gdot/time sector still open",
        ),
    }
    rows: List[Dict[str, object]] = []
    for source in read_csv(JZ_1354):
        if source.get("sector") != "Y5_source_normalization":
            continue
        status, route, guard = closure.get(
            source["coefficient_id"],
            (
                "REMAINS_LIVE",
                "not touched by stationary Hilbert mass-flux theorem",
                "needs dedicated domain/bulk/nonEH/species/calibration proof or coefficient fill",
            ),
        )
        rows.append(
            {
                "coefficient_id": source["coefficient_id"],
                "symbol": source["symbol"],
                "old_status": source["current_status"],
                "new_local_status": status,
                "route_or_reason": route,
                "scope_guard": guard,
                "observable_link": source["observable_link"],
                "accepted_for_scoring": False,
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def poynting_guard_rows() -> List[Dict[str, object]]:
    return [
        {
            "guard_id": "EPG4516_0_hilbert_owned",
            "component": "EM/Poynting energy flow",
            "zero_condition": "same Hodge, same current owner, EM stress included in T_tot, stationary tau and no radiation/current flux across the worldtube",
            "finite_fallback": "|J_EM_flux| <= |Phi_EM_rad|+|W_public_exchange|+|C_EM_surface_gauge|",
            "effect": "J_mem does not double-count ordinary EM stress if Hilbert-owned; otherwise Poynting remains explicit",
            "status": "CONDITIONAL_ZERO_ELSE_BOUND_IMPORTED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "guard_id": "EPG4516_1_remaining_coefficients",
            "component": "Poynting owner coefficients",
            "zero_condition": "lambda_F2=b_alpha=kappa_J=w_EM=Phi_EM_boundary=0 or parent-owned",
            "finite_fallback": "retain lambda_F2,b_alpha,kappa_J,w_EM,Phi_EM_boundary as absolute J_mem pieces",
            "effect": "prevents hiding wave/Poynting leakage inside fitted G or measured mass",
            "status": "OWNER_COEFFICIENTS_UNSIGNED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def remaining_debt_rows() -> List[Dict[str, object]]:
    return [
        {
            "debt_id": "RSD4516_0_domain_projector",
            "component": "Y5_2 domain/projector mass",
            "why_remaining": "stationary current conservation does not prove the domain/projector is q-basic or stress-free",
            "next_action": "derive C1/F0 domain projector source-normalization zero or fill coefficient products",
            "valid_for_claim": False,
        },
        {
            "debt_id": "RSD4516_1_bulk_range",
            "component": "Y5_3 bulk X/Yukawa",
            "why_remaining": "stationary mass flux does not kill finite-range bulk source hair",
            "next_action": "derive bulk mass-gap/no-source theorem or source alpha(lambda) row",
            "valid_for_claim": False,
        },
        {
            "debt_id": "RSD4516_2_nonEH",
            "component": "Y5_4 non-EH source operator",
            "why_remaining": "Hilbert current conservation does not remove retained R2/fR/nonEH operators",
            "next_action": "prove EH-only/nonEH coefficient zero or fill R11 operator vector",
            "valid_for_claim": False,
        },
        {
            "debt_id": "RSD4516_3_species",
            "component": "Y5_5 species/material source charge",
            "why_remaining": "stationary conservation does not prove selector-blind source action",
            "next_action": "derive source-label forgetting or fill species charge vector",
            "valid_for_claim": False,
        },
        {
            "debt_id": "RSD4516_4_calibration",
            "component": "Y5_7 absolute calibration",
            "why_remaining": "constant ell_J inside a collar does not derive the absolute universal calibration scale",
            "next_action": "derive parent-selected kappa/G calibration or retain offset",
            "valid_for_claim": False,
        },
        {
            "debt_id": "RSD4516_5_boundary",
            "component": "Y5_1 boundary/source-reference shift",
            "why_remaining": "no wall flux is not yet the same as source-functional boundary reference zero",
            "next_action": "same-branch boundary source-charge theorem or coefficient row",
            "valid_for_claim": False,
        },
    ]


def parent_audit_rows() -> List[Dict[str, object]]:
    return [
        {
            "audit_id": "PA4516_0_divergence",
            "clause": "Hilbert current stationary divergence",
            "status": "DERIVED_CONDITIONALLY",
            "reason": "2467 product rule closes under constant scale, matter shell and Killing clock",
            "valid_for_claim": False,
        },
        {
            "audit_id": "PA4516_1_mass_flux",
            "clause": "radial/time measured-mass flux lock",
            "status": "DERIVED_CONDITIONALLY",
            "reason": "q-basic fixed projector plus no wall flux makes M_eff surface/time independent",
            "valid_for_claim": False,
        },
        {
            "audit_id": "PA4516_2_parent_scale",
            "clause": "ell_J/kappa absolute calibration",
            "status": "NOT_PARENT_DERIVED",
            "reason": "constant within local collar is not full universal calibration derivation",
            "valid_for_claim": False,
        },
        {
            "audit_id": "PA4516_3_remaining_Y5",
            "clause": "domain/bulk/nonEH/species/boundary/calibration Y5 rows",
            "status": "RETAINED",
            "reason": "not killed by stationary Hilbert current theorem",
            "valid_for_claim": False,
        },
        {
            "audit_id": "PA4516_4_public_claim",
            "clause": "local GR/Newton/PPN/R10",
            "status": "NOT_CLAIMED",
            "reason": "partial local stationary closure is not full source-functor parent signature",
            "valid_for_claim": False,
        },
    ]


def claim_gate_rows() -> List[Dict[str, object]]:
    return [
        {
            "gate_id": "CG4516_0_Y5_radial_time",
            "claim": "Y5_0 radial hair and Y5_6 time drift closed in local stationary collar",
            "passed": False,
            "blocker": "conditional local branch only; parent scale/projector/no-flux hypotheses not live-signed",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4516_1_all_Y5",
            "claim": "all Y5 source-normalization tails vanish",
            "passed": False,
            "blocker": "domain, bulk/range, nonEH, species, boundary and absolute calibration rows remain live",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4516_2_Jmem",
            "claim": "J_mem vanishes",
            "passed": False,
            "blocker": "non-Hilbert source current and Poynting owner coefficients remain unsigned",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4516_3_local_GR",
            "claim": "local GR/Newton/PPN/R10 pass",
            "passed": False,
            "blocker": "source-functor closure is partial and nonclaim",
            "valid_for_claim": False,
        },
    ]


def status_rows() -> List[Dict[str, object]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "marker": MARKER,
            "claim_id": CLAIM_ID,
            "decision": DECISION,
            "derived": "stationary Hilbert mass-current divergence theorem; q-basic mass-flux surface/time lock; conditional local closure for Y5 radial M_eff hair and time drift; Poynting no-flux guard",
            "not_derived": "full source-functor parent signature, domain/bulk/nonEH/species/boundary/calibration Y5 rows, live Poynting owner coefficients, public local-GR claim",
            "claim_status": "PRIVATE_NONCLAIM",
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated": STAMP,
        }
    ]


def decision_rows() -> List[Dict[str, object]]:
    return [
        {
            "decision_id": "DEC4516_0",
            "decision": DECISION,
            "because": "4515 exposed the single source-functor route; 4516 proves the stationary Hilbert-current subtheorem and uses it to conditionally close two Y5 rows instead of re-auditing all source tails",
            "effect": "the live source fight is now narrowed to domain/projector, bulk/range, nonEH, species, boundary and absolute calibration rows",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def next_rows() -> List[Dict[str, object]]:
    return [
        {
            "next_id": "NT4516_0",
            "target_file": NEXT_TARGET,
            "task": "attack the remaining Y5 rows in the least fragile order: domain/projector first, then bulk/range, nonEH, species, boundary/calibration",
            "success_condition": "one remaining source-normalization coefficient becomes theorem-zero or source-backed finite, without using fitted G as a hiding place",
            "avoid": "upgrading stationary Hilbert current conservation into full dynamic source-functor closure",
            "valid_for_claim": False,
        }
    ]


def validate(all_rows: Mapping[str, Sequence[Mapping[str, object]]]) -> List[Dict[str, object]]:
    csv_paths = [
        SOURCE_REGISTER,
        STATIONARY_THEOREM,
        Y5_CLOSURE_MAP,
        POYNTING_GUARD,
        REMAINING_DEBT,
        PARENT_AUDIT,
        CLAIM_GATES,
        STATUS_CSV,
        NEXT_CSV,
        DECISION_CSV,
    ]
    details = []
    parsed_ok = True
    for path in csv_paths:
        try:
            details.append(f"{path.name}:{len(read_csv(path))}")
        except Exception as exc:  # pragma: no cover
            parsed_ok = False
            details.append(f"{path.name}:FAIL:{exc}")

    sources_ok = all(row["exists"] and row["needle_found"] for row in all_rows["sources"])
    theorem_ok = any(row["theorem_id"] == "SHS4516_3_mass_flux_surface_lock" for row in all_rows["theorem"])
    y5_radial_ok = any(row["coefficient_id"] == "JZ1354_Y5_0_radial_Meff_hair" and row["new_local_status"] == "CONDITIONAL_LOCAL_STATIONARY_ZERO" for row in all_rows["y5"])
    y5_time_ok = any(row["coefficient_id"] == "JZ1354_Y5_6_time_drift" and row["new_local_status"] == "CONDITIONAL_LOCAL_STATIONARY_ZERO" for row in all_rows["y5"])
    remaining_ok = len(all_rows["debt"]) == 6
    poynting_ok = any(row["guard_id"] == "EPG4516_0_hilbert_owned" for row in all_rows["poynting"])
    gates_blocked = all(str(row.get("passed")) == "False" for row in all_rows["gates"])
    flags_false = True
    for rows in all_rows.values():
        for row in rows:
            for key in ("valid_for_claim", "claim_allowed", "accepted_for_scoring"):
                if key in row and str(row[key]).lower() != "false":
                    flags_false = False
    pycache_absent = not (SCRIPT_DIR / "__pycache__").exists()

    checks = [
        ("VAL4516_00_sources", sources_ok, "all source paths exist and source needles are found"),
        ("VAL4516_01_theorem", theorem_ok, "stationary mass-flux surface lock theorem exists"),
        ("VAL4516_02_y5_radial", y5_radial_ok, "Y5 radial M_eff row conditionally closed in local stationary branch"),
        ("VAL4516_03_y5_time", y5_time_ok, "Y5 time-drift row conditionally closed in local stationary branch"),
        ("VAL4516_04_remaining_debt", remaining_ok, "six remaining source debts recorded"),
        ("VAL4516_05_poynting", poynting_ok, "Poynting stationary worldtube guard exists"),
        ("VAL4516_06_claims_blocked", gates_blocked, "all claim gates remain blocked"),
        ("VAL4516_07_nonclaim_flags", flags_false, "all generated claim/scoring flags remain false"),
        ("VAL4516_08_csv_parse", parsed_ok, ";".join(details)),
        ("VAL4516_09_next_target", all_rows["next"][0]["target_file"] == NEXT_TARGET, NEXT_TARGET),
        ("VAL4516_10_pycache_absent", pycache_absent, "scripts __pycache__ absent after cleanup"),
    ]
    rows = [
        {
            "validation_id": check_id,
            "status": "PASS" if ok else "FAIL",
            "detail": detail,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for check_id, ok, detail in checks
    ]
    rows.append(
        {
            "validation_id": "VAL4516_OVERALL",
            "status": "PASS" if all(row["status"] == "PASS" for row in rows) else "FAIL",
            "detail": "4516 source-functor parent signature or first Y5 coefficient fill",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    )
    return rows


def append_once(path: Path, marker: str, body: str) -> None:
    existing = text(path)
    if marker in existing:
        return
    path.write_text(existing.rstrip() + "\n\n" + body.strip() + "\n", encoding="utf-8")


def append_claim_once() -> None:
    existing = text(CLAIMS_PATH)
    if CLAIM_ID in existing or MARKER in existing:
        return
    row = csv_line(
        [
            CLAIM_ID,
            "local_gr_newton_r2fr_stationary_source_subset",
            "4516 derives a local stationary Hilbert-current subtheorem. From J_M^nu=ell_J T^{nu rho} tau_rho, the exact divergence vanishes when ell_J is constant, matter stress is on shell and tau is Killing. With a q-basic fixed mass projector and no worldtube flux, M_eff is surface/time independent, conditionally closing the Y5 radial M_eff hair and time-drift rows in the local stationary branch. Domain/projector, bulk/range, non-EH, species, boundary, absolute calibration and Poynting owner coefficients remain unsigned.",
            "4516 source register, stationary Hilbert source subtheorem, Y5 partial closure map, Poynting worldtube guard, remaining source debt, parent audit, claim gates, status and validation.",
            "private_stationary_Hilbert_source_subset_nonclaim",
            NEXT_TARGET,
            "claiming full source-functor closure or local GR from a stationary-collar partial theorem.",
            "local_gr_newton_r2fr_stationary_source_subset",
            str(FORMAL_PATH),
            NEXT_TARGET,
            "attack remaining Y5 domain/bulk/nonEH/species/boundary/calibration source tails or fill coefficient rows.",
        ]
    )
    CLAIMS_PATH.write_text(existing.rstrip() + "\n" + row + "\n", encoding="utf-8")


def build_doc(
    sources: Sequence[Mapping[str, object]],
    theorem: Sequence[Mapping[str, object]],
    y5: Sequence[Mapping[str, object]],
    poynting: Sequence[Mapping[str, object]],
    debt: Sequence[Mapping[str, object]],
    parent: Sequence[Mapping[str, object]],
    gates: Sequence[Mapping[str, object]],
    status: Sequence[Mapping[str, object]],
    decisions: Sequence[Mapping[str, object]],
    next_target: Sequence[Mapping[str, object]],
    validation: Sequence[Mapping[str, object]],
) -> str:
    return f"""# 4516 - Source-Functor Parent Signature Or First Y5 Coefficient Fill

Marker: `{MARKER}`  
Claim: `{CLAIM_ID}`  
Decision: `{DECISION}`  
Generated: `{STAMP}`

## Verdict

4516 gets a real partial closure rather than another missing-list pass.

Start with the 2467 Hilbert mass current:

`J_M^nu = ell_J T_matter^(nu rho) tau_rho`.

The exact divergence is:

`nabla_nu J_M^nu = (nabla_nu ell_J)T^(nu rho)tau_rho + ell_J(nabla_nu T^(nu rho))tau_rho + ell_J T^(nu rho)nabla_(nu tau_rho)`.

Therefore, in a local stationary collar:

`nabla ell_J=0; nabla_mu T^(mu nu)=0; nabla_(mu tau_nu)=0 => nabla_nu J_M^nu=0`.

If the mass projector is q-basic and fixed, and no flux crosses the worldtube wall, then:

`D Pi_M=0 and nabla.(Pi_M J_M)=0 and int_wall n.Pi_M J_M=0 => d M_eff(S_r)/dr = d M_eff/dt = 0`.

That conditionally closes two Y5 source-normalization rows in the local stationary branch:

- `JZ1354_Y5_0_radial_Meff_hair`
- `JZ1354_Y5_6_time_drift`

It does **not** close the full source-functor theorem. Domain/projector mass, bulk/range source hair, non-EH source operators, species source charge, boundary/source-reference shifts and absolute calibration remain live. EM/Poynting is guarded: Hilbert-owned no-flux Poynting is not separate `J_mem`; otherwise it remains a finite source current.

## Source Register

{table(sources)}

## Stationary Hilbert Source Subtheorem

{table(theorem)}

## Y5 Partial Closure Map

{table(y5)}

## EM/Poynting Stationary Worldtube Guard

{table(poynting)}

## Remaining Source Debt

{table(debt)}

## Parent Signature Audit

{table(parent)}

## Claim Gates

{table(gates)}

## Status

{table(status)}

## Decision

{table(decisions)}

## Next Target

{table(next_target)}

## Validation

{table(validation)}
"""


def main() -> None:
    sources = source_rows()
    theorem = stationary_theorem_rows()
    y5 = y5_partial_closure_rows()
    poynting = poynting_guard_rows()
    debt = remaining_debt_rows()
    parent = parent_audit_rows()
    gates = claim_gate_rows()
    status = status_rows()
    decisions = decision_rows()
    next_target = next_rows()

    all_rows = {
        "sources": sources,
        "theorem": theorem,
        "y5": y5,
        "poynting": poynting,
        "debt": debt,
        "parent": parent,
        "gates": gates,
        "status": status,
        "decisions": decisions,
        "next": next_target,
    }

    write_csv(SOURCE_REGISTER, sources)
    write_csv(STATIONARY_THEOREM, theorem)
    write_csv(Y5_CLOSURE_MAP, y5)
    write_csv(POYNTING_GUARD, poynting)
    write_csv(REMAINING_DEBT, debt)
    write_csv(PARENT_AUDIT, parent)
    write_csv(CLAIM_GATES, gates)
    write_csv(STATUS_CSV, status)
    write_csv(NEXT_CSV, next_target)
    write_csv(DECISION_CSV, decisions)

    shutil.rmtree(SCRIPT_DIR / "__pycache__", ignore_errors=True)
    validation = validate(all_rows)
    write_csv(VALIDATION_PATH, validation)

    doc = build_doc(sources, theorem, y5, poynting, debt, parent, gates, status, decisions, next_target, validation)
    write_text(FORMAL_PATH, doc)
    write_text(DOC_PATH, doc)
    append_claim_once()
    append_once(
        SPINE_PATH,
        MARKER,
        f"""
## 4516 Source-Functor Parent Signature Or First Y5 Coefficient Fill

Marker: `{MARKER}`  
4516 derives a local stationary Hilbert-current subtheorem. In a stationary no-flux collar, `J_M^nu=ell_J T^(nu rho) tau_rho` has zero divergence when `ell_J` is constant, matter stress is on shell and `tau` is Killing. With a q-basic mass projector this makes `M_eff` surface/time independent, conditionally closing the Y5 radial effective-mass hair and time-drift rows in the local stationary branch. This is not a full source-functor/local-GR claim; domain/projector, bulk/range, non-EH, species, boundary/reference and absolute calibration rows remain live.
""",
    )
    append_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""
## 4516 Packet Integration

Marker: `{PACKET_MARKER}`  
The private packet now contains the first concrete Y5 partial closure: stationary Hilbert mass-flux kills radial `M_eff` hair and time drift in the local collar, while leaving the real remaining source tails exposed for 4517.
""",
    )
    shutil.rmtree(SCRIPT_DIR / "__pycache__", ignore_errors=True)
    print(f"wrote {FORMAL_PATH}")
    print(f"wrote {DOC_PATH}")
    print(f"wrote {VALIDATION_PATH}")
    print(f"decision {DECISION}")


if __name__ == "__main__":
    main()
