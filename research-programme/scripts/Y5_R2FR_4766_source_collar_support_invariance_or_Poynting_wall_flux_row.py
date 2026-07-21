from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main")
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4766"
CLAIM_ID = "L-608"
MARKER = "PPC4161_SOURCE_COLLAR_SUPPORT_INVARIANCE_OR_POYNTING_WALL_FLUX_ROW_4766"
PACKET_MARKER = "PPC4161_PACKET_SOURCE_COLLAR_SUPPORT_INVARIANCE_OR_POYNTING_WALL_FLUX_ROW_4766"
DECISION = "SOURCE_SUPPORT_INVARIANCE_LEMMA_DERIVED_CONDITIONAL_QBASIC_MEASURE_UNSIGNED_POYNTING_WALL_FLUX_RETAINED_NONCLAIM"
NEXT_TARGET = "4767-Y5-R2FR-parent-source-qbasic-signature-or-Poynting-wall-numeric-bound.md"

DOC_PATH = POST / "4766-Y5-R2FR-source-collar-trace-birth-inputs-or-Poynting-wall-flux-row.md"
FORMAL_PATH = FORMAL / "782-PPC4161-source-collar-support-invariance-or-Poynting-wall-flux-row.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
RESUME_PATH = POST / "CURRENT_LOCAL_RESUME.md"

SOURCE_REGISTER_CSV = SOURCE_DIR / "P8_Y5_R2FR_4766_SOURCE_REGISTER.csv"
SUPPORT_THEOREM_CSV = SOURCE_DIR / "P8_Y5_R2FR_4766_SUPPORT_INVARIANCE_THEOREM.csv"
TRACE_BIRTH_UPDATE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4766_TRACE_BIRTH_GATE_UPDATE.csv"
QEDGE_UPDATE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4766_QEDGE_SHELL_CLOSURE_UPDATE.csv"
POYNTING_WALL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4766_POYNTING_WALL_FLUX_ROW.csv"
QBASIC_SIGNATURE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4766_PARENT_SOURCE_QBASIC_SIGNATURE_PACK.csv"
QBARXH_PRODUCT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4766_QBARXH_PRODUCT_UPDATE.csv"
ROUTE_MATRIX_CSV = SOURCE_DIR / "P8_Y5_R2FR_4766_ROUTE_SELECTION_MATRIX.csv"
PROMOTION_GATES_CSV = SOURCE_DIR / "P8_Y5_R2FR_4766_PROMOTION_GATES.csv"
FIREWALL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4766_FIREWALL_ROWS.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4766_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4766_STATUS.csv"
NEXT_TARGET_CSV = SOURCE_DIR / "P8_Y5_R2FR_4766_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4766_VALIDATION.csv"

SOURCE_SPECS = [
    ("SRC4766_0_4765_decision", SOURCE_DIR / "P8_Y5_R2FR_4765_DECISION.csv", "QEDGE_SHELL_ZERO_CERTIFICATE_DERIVED_CONDITIONAL", "4765 handoff decision"),
    ("SRC4766_1_4765_zero_audit", SOURCE_DIR / "P8_Y5_R2FR_4765_QEDGE_SHELL_ZERO_CERTIFICATE_AUDIT.csv", "ZQ4765_1_fixed_worldtube", "4765 fixed worldtube clause"),
    ("SRC4766_2_4765_bound", SOURCE_DIR / "P8_Y5_R2FR_4765_QEDGE_SHELL_BOUND_PACK.csv", "QSB4765_3_birth", "4765 trace/birth bound pack"),
    ("SRC4766_3_4587_density", SOURCE_DIR / "P8_Y5_R2FR_4587_DENSITY_QBASIC_THEOREM.csv", "DQT4587_1_qbasic_density_zero", "4587 q-basic Hilbert density"),
    ("SRC4766_4_4587_poynting_residual", SOURCE_DIR / "P8_Y5_R2FR_4587_DENSITY_POYNTING_RESIDUAL_VECTOR.csv", "DRV4587_4_E_Poynting_boundary", "4587 Poynting residual retained"),
    ("SRC4766_5_4588_clauses", SOURCE_DIR / "P8_Y5_R2FR_4588_REGULAR_SUPPORT_ZERO_CLAUSES.csv", "ZSR4588_0_fixed_qbasic_collar", "4588 fixed q-basic collar"),
    ("SRC4766_6_4588_reynolds", SOURCE_DIR / "P8_Y5_R2FR_4588_REYNOLDS_SUPPORT_THEOREM.csv", "RST4588_2_shell_bound", "4588 shell bound"),
    ("SRC4766_7_4591_tau", SOURCE_DIR / "P8_Y5_R2FR_4591_TAU_EOBS_LOCK_THEOREM.csv", "TE4591_2_source_kernel_strict_zero", "4591 strict source-kernel chain"),
    ("SRC4766_8_4695_poynting_theorem", SOURCE_DIR / "P8_Y5_R2FR_4695_EM_POYNTING_HODGE_FLUX_THEOREM.csv", "EMF4695_2_no_wall_flux", "4695 no wall flux theorem"),
    ("SRC4766_9_4695_poynting_rows", SOURCE_DIR / "P8_Y5_R2FR_4695_POYNTING_FLUX_ROWS.csv", "FX4695_1_wall_flux_bound", "4695 Poynting wall bound row"),
    ("SRC4766_10_4697_boundary", SOURCE_DIR / "P8_Y5_R2FR_4697_QEDGE_BOUNDARY_FLUX_ROWS.csv", "QEB4697_4_radiative", "4697 radiative boundary flux row"),
    ("SRC4766_11_4714_owner", SOURCE_DIR / "P8_Y5_R2FR_4714_EM_STRESS_POYNTING_OWNER_THEOREM.csv", "EMP4714_2_Poynting_identity", "4714 Poynting stress identity"),
]

GENERATED_CSVS = [
    SOURCE_REGISTER_CSV,
    SUPPORT_THEOREM_CSV,
    TRACE_BIRTH_UPDATE_CSV,
    QEDGE_UPDATE_CSV,
    POYNTING_WALL_CSV,
    QBASIC_SIGNATURE_CSV,
    QBARXH_PRODUCT_CSV,
    ROUTE_MATRIX_CSV,
    PROMOTION_GATES_CSV,
    FIREWALL_CSV,
    DECISION_CSV,
    STATUS_CSV,
    NEXT_TARGET_CSV,
]


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def read_text(path_object: Path) -> str:
    return path_object.read_text(encoding="utf-8-sig", errors="replace")


def write_text(path_object: Path, content: str) -> None:
    path_object.parent.mkdir(parents=True, exist_ok=True)
    path_object.write_text(content, encoding="utf-8", newline="\n")


def write_csv(path_object: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"refusing to write empty CSV: {path_object}")
    path_object.parent.mkdir(parents=True, exist_ok=True)
    with path_object.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def parse_csv(path_object: Path) -> bool:
    with path_object.open("r", encoding="utf-8-sig", newline="") as handle:
        list(csv.DictReader(handle))
    return True


def append_once(path_object: Path, marker: str, block: str) -> None:
    existing = read_text(path_object) if path_object.exists() else ""
    if marker in existing:
        return
    separator = "" if not existing or existing.endswith("\n") else "\n"
    write_text(path_object, existing + separator + block.rstrip() + "\n")


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    divider = "| " + " | ".join("---" for _ in columns) + " |"
    body = [
        "| "
        + " | ".join(str(row[column]).replace("\\", "\\\\").replace("|", "\\|").replace("\n", " ") for column in columns)
        + " |"
        for row in rows
    ]
    return "\n".join([header, divider, *body])


def source_register(timestamp: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source_id, path_object, needle, role in SOURCE_SPECS:
        exists = path_object.exists()
        text = read_text(path_object) if exists else ""
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "source_id": source_id,
                "source_path": str(path_object),
                "exists": exists,
                "needle": needle,
                "needle_found": needle in text,
                "role": role,
                "valid_for_claim": False,
                "timestamp_utc": timestamp,
            }
        )
    return rows


def support_theorem_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        (
            "SIT4766_0_measure_object",
            "mu_H",
            "mu_H := rho_H dV_H is the parent Hilbert source measure, including ordinary matter, binding, pressure and Hilbert-owned EM stress.",
            "This keeps Poynting inside T_total on the single Maxwell-Hodge source branch, rather than adding it twice.",
            "OBJECT_DEFINED",
        ),
        (
            "SIT4766_1_exact_qbasic_measure",
            "mu_H(q(Phi))",
            "If mu_H=mu_bar[q(Phi)] and v is vertical, then along any vertical path Phi_s with q(Phi_s)=q(Phi_0), mu_H(Phi_s)=mu_H(Phi_0) as a Radon measure.",
            "This is stronger than an infinitesimal density slogan: it is equality of the source measure on the whole vertical fibre.",
            "CONDITIONAL_THEOREM_DERIVED_PARENT_UNSIGNED",
        ),
        (
            "SIT4766_2_support_invariance",
            "W_H=closure(supp mu_H)",
            "Exact equality of Radon measures implies supp(mu_H(Phi_s))=supp(mu_H(Phi_0)); therefore W_H is invariant when selected before readout.",
            "The normal support velocity is zero: V_n_bound=0 on the strict q-basic support branch.",
            "SUPPORT_INVARIANCE_DERIVED_CONDITIONAL",
        ),
        (
            "SIT4766_3_no_birth_death",
            "mu_birth_TV",
            "If the measure is exactly constant on the vertical fibre, no distributional source layer is born or killed.",
            "mu_birth_TV=0 follows from measure equality, not from assuming a plateau.",
            "NO_BIRTH_DERIVED_CONDITIONAL",
        ),
        (
            "SIT4766_4_trace_bypass",
            "rho_H_trace_norm",
            "The Reynolds shell product contains rho_H_trace_norm V_n_bound; if V_n_bound=0 and mu_birth_TV=0, shell zero does not require proving rho_H_trace_norm=0.",
            "Zero trace remains a sufficient route, but support invariance is a cleaner route if parent source q-basicness is signed.",
            "TRACE_ZERO_NO_LONGER_PRIMARY_ON_STRICT_BRANCH",
        ),
        (
            "SIT4766_5_poynting_escape",
            "Phi_wall_Poynting_abs",
            "Radiative/open Poynting flux can change the energy crossing a collar; that is not erased by support invariance and must be routed to the boundary flux row.",
            "Stationary isolated collars can set Phi_wall_Poynting=0; open collars need the finite wall-flux bound.",
            "POYNTING_RETAINED_AS_BOUNDARY_ROW",
        ),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "theorem_id": theorem_id,
            "object": obj,
            "statement": statement,
            "consequence": consequence,
            "status": status,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for theorem_id, obj, statement, consequence, status in specs
    ]


def trace_birth_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("TBG4766_0_previous_trace_route", "rho_H_trace_norm=0", "still sufficient", "not required if support-invariance branch proves V_n_bound=0", "OPTIONAL_SUFFICIENT_ROUTE"),
        ("TBG4766_1_support_velocity", "V_n_bound=0", "follows from exact q-basic Hilbert source measure and W_H=closure(supp mu_H)", "PRIMARY_ZERO_ROUTE_PARENT_UNSIGNED", "DERIVED_CONDITIONAL"),
        ("TBG4766_2_birth_shell", "mu_birth_TV=0", "follows from exact source measure equality along the vertical fibre", "PRIMARY_ZERO_ROUTE_PARENT_UNSIGNED", "DERIVED_CONDITIONAL"),
        ("TBG4766_3_shell_result", "Q_edge_shell_abs=0", "rho_H_trace_norm*0 + 0 = 0 for finite trace/test/kernel ceilings", "requires exact q-basic measure and fixed pre-readout support selection", "CONDITIONAL_ZERO_ROUTE_SHARPENED"),
        ("TBG4766_4_fallback", "Q_edge_shell_abs", "Q_edge_shell_abs <= W_lambda_edge_max Phi_edge (rho_H_trace_norm V_n_bound + mu_birth_TV)", "use if source measure equality/support invariance is not parent-signed", "BOUND_ROUTE_RETAINED"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "row_id": row_id,
            "quantity": quantity,
            "new_rule": rule,
            "condition_or_use": use,
            "status": status,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_id, quantity, rule, use, status in specs
    ]


def qedge_update_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("QEU4766_0_shell_term", "Q_edge_shell = int_partialW phi_edge W_lambda rho_H_tr V_n dSigma + <phi_edge W_lambda, mu_birth>", "same Reynolds term, now with support-invariance route", "UNCHANGED_OBJECT"),
        ("QEU4766_1_support_zero", "V_n_bound=0 and mu_birth_TV=0 if mu_H is exact q-basic and W_H=closure(supp mu_H) before readout", "kills the shell without needing zero trace", "NEW_ZERO_ROUTE"),
        ("QEU4766_2_boundary_not_shell", "Q_edge_abs <= Q_edge_shell_abs + Q_edge_boundary_abs", "Poynting/radiative wall flux remains in Q_edge_boundary_abs or Q_bulk_EM/Poynting", "BOUNDARY_RETAINED"),
        ("QEU4766_3_claim_status", "Q_edge_shell_abs=0 is not claimed yet", "parent source-qbasic signature and Poynting/no-flux branch are not signed", "NONCLAIM"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "update_id": update_id,
            "formula_or_rule": formula,
            "meaning": meaning,
            "status": status,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for update_id, formula, meaning, status in specs
    ]


def poynting_wall_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        (
            "PWF4766_0_owner",
            "Poynting stress ownership",
            "S_i=-T_EM(n,e_i) on the public observed-Hodge Maxwell branch",
            "ordinary Poynting flow is counted once inside T_total",
            "EXACT_IDENTITY_CONDITIONAL",
        ),
        (
            "PWF4766_1_stationary_zero",
            "Phi_wall_Poynting=0",
            "stationary isolated source collar, time_avg(dU_EM/dt)=0, time_avg(int_W J.E dV)=0, no incoming/background/apparatus flux",
            "no independent Poynting boundary residual",
            "CONDITIONAL_LOCAL_ZERO_NOT_GLOBAL",
        ),
        (
            "PWF4766_2_wall_flux_bound",
            "Phi_wall_Poynting_abs",
            "|Phi_wall_Poynting| <= |dU_EM/dt| + |int_W J.E dV| + |Phi_incoming| + |Phi_apparatus|",
            "finite open/radiative collar fallback",
            "BOUND_TEMPLATE_READY_VALUES_MISSING",
        ),
        (
            "PWF4766_3_Qedge_boundary_insert",
            "Q_edge_boundary_abs",
            "|Q_edge_boundary| includes |F_rad| and Phi_wall_Poynting_abs where EM radiation crosses the collar",
            "prevents hiding waves/Poynting in a false shell zero",
            "BOUNDARY_INSERT_READY_NONNUMERIC",
        ),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "row_id": row_id,
            "quantity": quantity,
            "formula_or_zero_condition": formula,
            "role": role,
            "status": status,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_id, quantity, formula, role, status in specs
    ]


def qbasic_signature_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("PSQ4766_0_source_action", "S_src=Sbar_src[q(Phi),Psi,A,theta]", "parent source action descends through q before variation", "MISSING_PARENT_SIGNATURE"),
        ("PSQ4766_1_measure_equality", "mu_H(Phi_s)=mu_H(Phi_0)", "Radon measure equality on vertical fibres, including EM stress owner", "MISSING_PARENT_SIGNATURE"),
        ("PSQ4766_2_support_selector", "W_H=closure(supp mu_H)", "support/collar selected before readout from the parent measure, not a residual threshold", "MISSING_SELECTOR_SIGNATURE"),
        ("PSQ4766_3_same_branch", "tau_*,e_*,W_H,Pi_M,M_H_ref all same branch", "no split frames or post-fit source conventions", "MISSING_BRANCH_SIGNATURE"),
        ("PSQ4766_4_poynting_clause", "public Hodge or explicit wall flux", "Poynting is either Hilbert-owned/stationary or bounded as Phi_wall_Poynting_abs", "MISSING_POYNTING_BRANCH_SIGNATURE"),
        ("PSQ4766_5_promotion_gate", "Q_edge_shell_abs=0", "claim-ready only if PSQ4766_0..4 are signed and no MISSING markers remain", "CLAIM_BLOCKED"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "signature_id": signature_id,
            "quantity_or_clause": quantity,
            "requirement": requirement,
            "current_status": status,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for signature_id, quantity, requirement, status in specs
    ]


def qbar_product_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        (
            "QBU4766_0_support_zero_product",
            "If exact q-basic mu_H and pre-readout W_H hold, then Q_edge_shell_abs=0 via V_n_bound=0 and mu_birth_TV=0.",
            "This is the new sharper numerator-zero branch.",
            "CONDITIONAL_INSERT",
        ),
        (
            "QBU4766_1_open_product",
            "|Qbar_XH| <= [P_M_bound(|Q_bulk| + Q_edge_boundary_abs + |Q_shadow|) + |E_PiM_comm|]/[M_0(1-epsilon_abs)] when Q_edge_shell_abs=0.",
            "Only valid after source-qbasic, denominator/projector and boundary rows are all signed.",
            "PRODUCT_SIMPLIFIED_CONDITIONAL_NONCLAIM",
        ),
        (
            "QBU4766_2_poynting_boundary",
            "Q_edge_boundary_abs retains Phi_wall_Poynting_abs or F_rad_abs on open/radiative collars.",
            "The Poynting hunch is preserved as stress/boundary flow rather than an extra unsourced force.",
            "POYNTING_VISIBLE",
        ),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "update_id": update_id,
            "formula_or_rule": formula,
            "meaning": meaning,
            "status": status,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for update_id, formula, meaning, status in specs
    ]


def route_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("ROUTE4766_0_trace_direct", "prove rho_H_trace_norm=0", "valid but harder; not needed if support invariance closes V_n and birth", "DEPRIORITIZED"),
        ("ROUTE4766_1_support_invariance", "prove exact q-basic measure implies fixed support/no birth", "cleanest derivation route; built in this checkpoint", "ATTEMPTED_CONDITIONAL"),
        ("ROUTE4766_2_parent_signature", "source action/measure/support selector signature", "next target because it can promote the support-invariance theorem", "SELECTED_NEXT"),
        ("ROUTE4766_3_poynting_wall_bound", "stationary zero or finite Poynting wall flux row", "parallel EM/boundary branch if source collar is open or radiative", "PARALLEL_REQUIRED"),
        ("ROUTE4766_4_denominator_pack", "M0 epsilon PiM Ecomm", "still mandatory before local scoring", "PARALLEL_REQUIRED"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "route_id": route_id,
            "route": route,
            "payoff": payoff,
            "selection_status": status,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for route_id, route, payoff, status in specs
    ]


def promotion_gate_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("PG4766_0_no_trace_overfocus", "Do not require zero trace if support invariance proves V_n_bound=0 and mu_birth_TV=0.", "permits cleaner proof route"),
        ("PG4766_1_no_measure_slogan", "Do not claim support invariance from infinitesimal prose; require exact q-basic Radon measure equality or a bound.", "blocks soft closure"),
        ("PG4766_2_no_threshold_support", "W_H must be closure(supp mu_H), not a fitted threshold/readout mask.", "blocks circular source collar"),
        ("PG4766_3_no_poynting_erasure", "Open/radiative Poynting wall flux must remain explicit.", "blocks hiding EM flux in shell zero"),
        ("PG4766_4_no_local_score", "No local-GR/Newton/R10/PPN/WEP/clock/orbital/Maxwell claim from 4766.", "keeps checkpoint private/nonclaim"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "gate_id": gate_id,
            "rule": rule,
            "enforced_effect": effect,
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        }
        for gate_id, rule, effect in specs
    ]


def firewall_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("FW4766_0_no_support_claim", "Do not claim W_H support invariance until exact q-basic measure equality is parent-signed.", "NONCLAIM"),
        ("FW4766_1_no_poynting_double_count", "Poynting is either Hilbert stress or explicit boundary flux, never both.", "SOURCE_ACCOUNTING"),
        ("FW4766_2_no_boundary_zero", "Even if Q_edge_shell_abs=0, Q_edge_boundary_abs remains open.", "NONCLAIM"),
        ("FW4766_3_no_denominator_skip", "No Qbar scoring without M0/epsilon/PiM/Ecomm.", "NONCLAIM"),
        ("FW4766_4_local_only", "No GitHub action from this checkpoint.", "LOCAL_ONLY"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "firewall_id": firewall_id,
            "rule": rule,
            "status": status,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for firewall_id, rule, status in specs
    ]


def decision_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "decision_id": "DEC4766_0",
            "decision": DECISION,
            "summary": "4766 finds a cleaner route than proving zero trace directly: exact q-basic Hilbert source measure equality implies support invariance, V_n_bound=0 and mu_birth_TV=0. This conditionally kills Qedge shell while retaining Poynting wall flux as an explicit boundary row. The parent source-qbasic signature is still unsigned, so this is not a local-GR claim.",
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "status_id": "STATUS4766_0",
            "state": "completed_nonclaim",
            "meaning": "The shell gate moved from trace/birth values to a sharper parent source-qbasic support-invariance signature, with Poynting kept explicit.",
            "next_target": NEXT_TARGET,
            "timestamp_utc": timestamp,
        }
    ]


def next_target_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "next_target": NEXT_TARGET,
            "reason": "Promote or reject the support-invariance route by signing the parent source-qbasic measure/support selector, while preparing a Poynting wall bound if the collar is open.",
            "route_priority": "parent_source_qbasic_signature_first_Poynting_wall_numeric_bound_parallel_denominator_pack",
            "timestamp_utc": timestamp,
        }
    ]


def write_docs(
    timestamp: str,
    support_rows: list[dict[str, Any]],
    trace_rows: list[dict[str, Any]],
    qedge_rows: list[dict[str, Any]],
    poynting_rows: list[dict[str, Any]],
    signature_rows: list[dict[str, Any]],
    qbar_rows: list[dict[str, Any]],
    routes: list[dict[str, Any]],
    gates: list[dict[str, Any]],
) -> None:
    doc = f"""# 4766: Source-Collar Trace/Birth Inputs or Poynting Wall Flux Row

Generated: `{timestamp}`

Marker: `{MARKER}`

## Result

4766 finds a cleaner route than hammering zero trace directly.

- If the Hilbert source measure `mu_H=rho_H dV_H` is exactly q-basic as a Radon measure, then along a vertical fibre `mu_H(Phi_s)=mu_H(Phi_0)`.
- If the source worldtube is selected before readout as `W_H=closure(supp mu_H)`, measure equality implies support equality.
- Therefore `V_n_bound=0` and `mu_birth_TV=0` on that strict branch, so `Q_edge_shell_abs=0` without needing `rho_H_trace_norm=0`.
- This is not claimed yet: the parent source-qbasic measure/support selector signature is still unsigned.
- Poynting is not ignored: Hilbert-owned stationary EM is counted once in `T_total`; open/radiative wall flux remains an explicit boundary row.

## Support Invariance Theorem

{markdown_table(support_rows, ["theorem_id", "object", "statement", "status"])}

## Trace/Birth Gate Update

{markdown_table(trace_rows, ["row_id", "quantity", "new_rule", "status"])}

## Qedge Shell Closure Update

{markdown_table(qedge_rows, ["update_id", "formula_or_rule", "status"])}

## Poynting Wall Flux Row

{markdown_table(poynting_rows, ["row_id", "quantity", "formula_or_zero_condition", "status"])}

## Parent Source-Qbasic Signature Pack

{markdown_table(signature_rows, ["signature_id", "quantity_or_clause", "requirement", "current_status"])}

## QbarXH Product Update

{markdown_table(qbar_rows, ["update_id", "formula_or_rule", "status"])}

## Route Selection

{markdown_table(routes, ["route_id", "route", "payoff", "selection_status"])}

## Promotion Gates

{markdown_table(gates, ["gate_id", "rule", "enforced_effect"])}

## Decision

`{DECISION}`

## Next Target

`{NEXT_TARGET}`
"""
    write_text(DOC_PATH, doc)

    formal = f"""# PPC4161 4766: Source-Collar Support Invariance

Generated: `{timestamp}`

## Core Result

Let:

```text
mu_H := rho_H dV_H
W_H := closure(supp mu_H)
```

If:

```text
mu_H(Phi_s) = mu_H(Phi_0) as Radon measures
q(Phi_s)=q(Phi_0)
W_H is selected before readout from mu_H
```

then:

```text
supp mu_H(Phi_s)=supp mu_H(Phi_0)
V_n_bound = 0
mu_birth_TV = 0
Q_edge_shell_abs = 0
```

This bypasses the need to prove `rho_H_trace_norm=0` on the strict support-invariance branch, although trace-zero remains a sufficient fallback.

Poynting placement:

```text
S_i = -T_EM(n,e_i)
```

on the public Maxwell-Hodge Hilbert branch, counted once in `T_total`. If the collar is open/radiative:

```text
|Phi_wall_Poynting| <= |dU_EM/dt| + |int_W J.E dV| + |Phi_incoming| + |Phi_apparatus|.
```

Still nonclaim: parent source-qbasic measure equality, support selector, Poynting branch and denominator/projector rows remain unsigned.

Decision: `{DECISION}`

Next: `{NEXT_TARGET}`
"""
    write_text(FORMAL_PATH, formal)


def update_spine_packet_resume(timestamp: str) -> None:
    spine_block = f"""

## {MARKER}

Generated: `{timestamp}`

- 4766 derives the support-invariance route: exact q-basic Hilbert source measure equality implies invariant support `W_H=closure(supp mu_H)`.
- On that strict branch, `V_n_bound=0` and `mu_birth_TV=0`, so `Q_edge_shell_abs=0` without requiring `rho_H_trace_norm=0`.
- The route is not promoted because parent source-qbasic measure equality, support selector and same-branch signatures are unsigned.
- Poynting is retained explicitly: Hilbert-owned stationary EM is counted once; open/radiative wall flux goes into `Phi_wall_Poynting_abs`.
- Decision: `{DECISION}`.
"""
    append_once(SPINE_PATH, MARKER, spine_block)

    packet_block = f"""

## {PACKET_MARKER}

Generated: `{timestamp}`

4766 packet update: the shell gate has a cleaner strict route. Sign the parent source-qbasic measure/support selector to obtain `V_n_bound=0`, `mu_birth_TV=0`, and hence `Q_edge_shell_abs=0`; otherwise use the finite shell/Poynting wall bounds.

Next: `{NEXT_TARGET}`.
"""
    append_once(PACKET_PATH, PACKET_MARKER, packet_block)

    resume = f"""# Current Local Resume

Updated: `{timestamp}`

## Latest completed checkpoint

`4766-Y5-R2FR-source-collar-trace-birth-inputs-or-Poynting-wall-flux-row.md`

## Decision

`{DECISION}`

## What moved forward

- Derived the support-invariance lemma: exact q-basic Hilbert source measure equality fixes `W_H=closure(supp mu_H)`.
- Replaced the primary trace-zero hunt with the cleaner branch `V_n_bound=0` and `mu_birth_TV=0`.
- Kept Poynting honest: Hilbert-owned stationary EM is counted once; open/radiative wall flux remains explicit.
- Left local-GR/Newton scoring closed until parent source-qbasic, boundary/Poynting and denominator/projector signatures are signed.

## Current target

`{NEXT_TARGET}`

## Local-only note

No GitHub action was performed by this checkpoint.
"""
    write_text(RESUME_PATH, resume)


def add_claim_once(timestamp: str) -> None:
    existing = read_text(CLAIMS_PATH) if CLAIMS_PATH.exists() else ""
    if CLAIM_ID in existing:
        return
    row = [
        CLAIM_ID,
        "local_gr_source_support_invariance",
        "4766 derives the conditional source-support invariance route for Qedge shell zero and retains Poynting wall flux explicitly.",
        "Generated source register, support invariance theorem, trace/birth gate update, Qedge closure update, Poynting wall row, parent source-qbasic signature pack, Qbar product update, route matrix, gates, firewalls, decision, status, next target and validation.",
        "source_support_invariance_conditional_parent_qbasic_unsigned_nonclaim",
        NEXT_TARGET,
        "Claiming source support invariance without exact q-basic measure equality, or hiding open/radiative Poynting wall flux.",
        "local_gr",
        str(DOC_PATH),
        NEXT_TARGET,
        "Need parent source-qbasic signature or Poynting wall numeric bound.",
        "Source-collar support invariance or Poynting wall flux row",
        f"{MARKER}; {DECISION}; generated {timestamp}",
    ]
    with CLAIMS_PATH.open("a", encoding="utf-8", newline="") as handle:
        csv.writer(handle).writerow(row)


def cleanup_pycache() -> None:
    pycache = POST / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def validation_rows(
    sources: list[dict[str, Any]],
    support_rows: list[dict[str, Any]],
    trace_rows: list[dict[str, Any]],
    qedge_rows: list[dict[str, Any]],
    poynting_rows: list[dict[str, Any]],
    signature_rows: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    timestamp: str,
) -> list[dict[str, Any]]:
    checks: list[tuple[str, str, bool, str]] = []
    checks.append(("VAL4766_0_sources_exist", "all cited source paths exist", all(row["exists"] for row in sources), str(SOURCE_REGISTER_CSV)))
    checks.append(("VAL4766_1_needles_found", "all source needles found", all(row["needle_found"] for row in sources), str(SOURCE_REGISTER_CSV)))
    for csv_path in GENERATED_CSVS:
        checks.append((f"VAL4766_csv_{csv_path.stem}", f"{csv_path.name} parses", csv_path.exists() and parse_csv(csv_path), str(csv_path)))
    checks.append(("VAL4766_2_support_invariance", "support theorem derives Vn zero and no birth conditional route", any(row["status"] == "SUPPORT_INVARIANCE_DERIVED_CONDITIONAL" for row in support_rows) and any(row["status"] == "NO_BIRTH_DERIVED_CONDITIONAL" for row in support_rows), str(SUPPORT_THEOREM_CSV)))
    checks.append(("VAL4766_3_trace_bypass", "trace gate is bypassed by support invariance but not erased", any(row["quantity"] == "rho_H_trace_norm=0" and "OPTIONAL" in row["status"] for row in trace_rows) and any(row["quantity"] == "V_n_bound=0" for row in trace_rows), str(TRACE_BIRTH_UPDATE_CSV)))
    checks.append(("VAL4766_4_qedge_nonclaim", "Qedge update has new zero route and remains nonclaim", any(row["status"] == "NEW_ZERO_ROUTE" for row in qedge_rows) and any(row["status"] == "NONCLAIM" for row in qedge_rows), str(QEDGE_UPDATE_CSV)))
    checks.append(("VAL4766_5_poynting_visible", "Poynting wall flux row has stationary zero and finite bound", any(row["quantity"] == "Phi_wall_Poynting=0" for row in poynting_rows) and any(row["quantity"] == "Phi_wall_Poynting_abs" for row in poynting_rows), str(POYNTING_WALL_CSV)))
    checks.append(("VAL4766_6_signature_blocked", "parent qbasic signature pack keeps claims closed", any(row["current_status"] == "CLAIM_BLOCKED" for row in signature_rows) and all(row["valid_for_claim"] is False for row in signature_rows), str(QBASIC_SIGNATURE_CSV)))
    checks.append(("VAL4766_7_gates_nonclaim", "promotion gates keep claims closed", all(row["claim_allowed"] is False for row in gates), str(PROMOTION_GATES_CSV)))
    checks.append(("VAL4766_8_docs_exist", "post and formal docs exist", DOC_PATH.exists() and FORMAL_PATH.exists(), f"{DOC_PATH}; {FORMAL_PATH}"))
    checks.append(("VAL4766_9_spine_marker", "spine marker appended", MARKER in read_text(SPINE_PATH), str(SPINE_PATH)))
    checks.append(("VAL4766_10_packet_marker", "packet marker appended", PACKET_MARKER in read_text(PACKET_PATH), str(PACKET_PATH)))
    checks.append(("VAL4766_11_claim_row", "claim row L-608 present", CLAIM_ID in read_text(CLAIMS_PATH), str(CLAIMS_PATH)))
    resume_text = read_text(RESUME_PATH)
    checks.append(("VAL4766_12_resume", "resume points from 4766 to 4767", "4766-Y5" in resume_text and "4767-Y5" in resume_text, str(RESUME_PATH)))
    checks.append(("VAL4766_13_pycache_absent", "scripts __pycache__ removed", not (POST / "scripts" / "__pycache__").exists(), str(POST / "scripts")))
    overall = all(passed for _, _, passed, _ in checks)
    rows = [
        {
            "checkpoint": CHECKPOINT,
            "validation_id": validation_id,
            "check": check,
            "status": "PASS" if passed else "FAIL",
            "detail": detail,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for validation_id, check, passed, detail in checks
    ]
    rows.append(
        {
            "checkpoint": CHECKPOINT,
            "validation_id": "VAL4766_OVERALL",
            "check": "all 4766 support-invariance/Poynting checks pass",
            "status": "PASS" if overall else "FAIL",
            "detail": DECISION,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    )
    return rows


def main() -> None:
    timestamp = now()
    sources = source_register(timestamp)
    support_rows = support_theorem_rows(timestamp)
    trace_rows = trace_birth_rows(timestamp)
    qedge_rows = qedge_update_rows(timestamp)
    poynting_rows = poynting_wall_rows(timestamp)
    signature_rows = qbasic_signature_rows(timestamp)
    qbar_rows = qbar_product_rows(timestamp)
    routes = route_rows(timestamp)
    gates = promotion_gate_rows(timestamp)
    firewalls = firewall_rows(timestamp)
    decisions = decision_rows(timestamp)
    statuses = status_rows(timestamp)
    next_targets = next_target_rows(timestamp)

    write_csv(SOURCE_REGISTER_CSV, sources)
    write_csv(SUPPORT_THEOREM_CSV, support_rows)
    write_csv(TRACE_BIRTH_UPDATE_CSV, trace_rows)
    write_csv(QEDGE_UPDATE_CSV, qedge_rows)
    write_csv(POYNTING_WALL_CSV, poynting_rows)
    write_csv(QBASIC_SIGNATURE_CSV, signature_rows)
    write_csv(QBARXH_PRODUCT_CSV, qbar_rows)
    write_csv(ROUTE_MATRIX_CSV, routes)
    write_csv(PROMOTION_GATES_CSV, gates)
    write_csv(FIREWALL_CSV, firewalls)
    write_csv(DECISION_CSV, decisions)
    write_csv(STATUS_CSV, statuses)
    write_csv(NEXT_TARGET_CSV, next_targets)
    write_docs(timestamp, support_rows, trace_rows, qedge_rows, poynting_rows, signature_rows, qbar_rows, routes, gates)
    update_spine_packet_resume(timestamp)
    add_claim_once(timestamp)
    cleanup_pycache()
    write_csv(VALIDATION_CSV, validation_rows(sources, support_rows, trace_rows, qedge_rows, poynting_rows, signature_rows, gates, timestamp))


if __name__ == "__main__":
    main()
