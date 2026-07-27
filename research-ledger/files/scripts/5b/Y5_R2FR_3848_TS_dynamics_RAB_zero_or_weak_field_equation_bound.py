from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


CHECKPOINT = "3848"
BRANCH = "MTS_R2FR_Y5_TS_DYNAMICS_RAB_ZERO_WEAK_FIELD_BOUND_3848"

PCW = Path(__file__).resolve().parents[1]
ROOT = PCW.parent
FWB = ROOT / "formalization-workbench"
OUT = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "3848-Y5-R2FR-TS-dynamics-RAB-zero-or-weak-field-equation-bound.md"
SPINE_PATH = PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

P_3847 = PCW / "3847-Y5-R2FR-observer-coframe-completion-from-TS-or-metric-bridge-demotion.md"
P_10_OBSERVER = PCW / "10-observer-map-symplectic-contract.md"
P_04_CONTRACT = PCW / "04-vacuum-reciprocity-action-contract.md"
P_05_ATTEMPT = PCW / "05-reciprocity-theorem-attempt.md"
P_06_NEUTRALITY = PCW / "06-reciprocal-charge-source-neutrality.md"

CSV_3847_COFRAME = OUT / "P8_Y5_R2FR_3847_OBSERVER_COFRAME_COMPLETION.csv"
CSV_3847_DOMAIN = OUT / "P8_Y5_R2FR_3847_COFRAME_DOMAIN_AND_LIMITS.csv"
CSV_3847_UPDATE = OUT / "P8_Y5_R2FR_3847_METRIC_BRIDGE_UPDATE.csv"
CSV_3847_VALIDATION = OUT / "P8_Y5_BRR545_3847_VALIDATION.csv"
CSV_3818_POISSON = OUT / "P8_Y5_R2FR_3818_WEAK_FIELD_POISSON_DERIVATION.csv"
CSV_3828_ZERO = OUT / "P8_Y5_R2FR_3828_ZERO_CONDITION_THEOREM.csv"

OUTPUTS = {
    "sources": OUT / "P8_Y5_R2FR_3848_SOURCE_REGISTER.csv",
    "dynamics": OUT / "P8_Y5_R2FR_3848_TS_DYNAMICS_DERIVATION.csv",
    "rab_lemma": OUT / "P8_Y5_R2FR_3848_RAB_ZERO_OR_HAIR_LEMMA.csv",
    "weak_field": OUT / "P8_Y5_R2FR_3848_WEAK_FIELD_TS_MAP.csv",
    "ppn_update": OUT / "P8_Y5_R2FR_3848_PPN_IMPACT_UPDATE.csv",
    "gates": OUT / "P8_Y5_R2FR_3848_CLAIM_GATES.csv",
    "decisions": OUT / "P8_Y5_R2FR_3848_DECISION_ROWS.csv",
    "next": OUT / "P8_Y5_R2FR_3848_NEXT_TARGET.csv",
    "status": OUT / "P8_Y5_R2FR_3848_STATUS.csv",
    "validation": OUT / "P8_Y5_BRR545_3848_VALIDATION.csv",
}

SOURCE_SPECS = [
    ("SRC3848_0_3847_doc", P_3847, "static spherical coframe completion"),
    ("SRC3848_1_3847_coframe", CSV_3847_COFRAME, "OCF3847_3_metric"),
    ("SRC3848_2_3847_domain", CSV_3847_DOMAIN, "OCD3847_3_parent_owner"),
    ("SRC3848_3_3847_update", CSV_3847_UPDATE, "MBU3847_2_next_physics"),
    ("SRC3848_4_3847_validation", CSV_3847_VALIDATION, "PASS"),
    ("SRC3848_5_10_observer", P_10_OBSERVER, "R_AB = ln(T^2 S)"),
    ("SRC3848_6_04_contract", P_04_CONTRACT, "d/dr [ W(r,L,fields) dR_AB/dr ] = J_R"),
    ("SRC3848_7_05_attempt", P_05_ATTEMPT, "W R_AB' = Q_R"),
    ("SRC3848_8_06_neutrality", P_06_NEUTRALITY, "Pi_R = 0 -> Q_R = 0 -> R_AB = 0 -> AB = 1"),
    ("SRC3848_9_3818_poisson", CSV_3818_POISSON, "POI3818_0_linearized_00"),
    ("SRC3848_10_3828_ppn", CSV_3828_ZERO, "ZPPN3828_2_beta_lock"),
]

RAB = "R_AB=ln(T^2 S)=2 ln(J_q)"
RAB_EQUATION = "d/dr[W_R(r) dR_AB/dr]=J_R(r)"
RAB_BOUND = "B_RAB <= B_QR_hair + B_JR_source + B_inner_boundary + B_outer_reference + B_W_degeneracy"
WEAK_T = "U_T=(c_*^2/2)(1-T^2)"


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8-sig", errors="replace")


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(PCW))
    except ValueError:
        return str(path)


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    fieldnames = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def source_register_rows(timestamp: str) -> list[dict[str, object]]:
    rows = []
    for source_id, path, needle in SOURCE_SPECS:
        exists = path.exists()
        text = read_text(path) if exists else ""
        rows.append(
            {
                "source_id": source_id,
                "checkpoint": CHECKPOINT,
                "path": rel(path),
                "exists": exists,
                "needle": needle,
                "needle_found": needle in text,
                "role": "input_for_TS_dynamics_RAB_zero_or_bound",
                "claim_use": "nonclaim_derivation_and_residual_bound_only",
                "timestamp_utc": timestamp,
            }
        )
    return rows


def dynamics_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "derivation_id": "TSD3848_0_define_RAB",
            "object": "reciprocal observer-cell strain",
            "formula": RAB,
            "derivation": "from 10-observer-map: J_q=T sqrt(S), hence 2 ln(J_q)=ln(T^2 S)",
            "result": "R_AB is the scalar obstruction to reciprocal radial observer-cell preservation",
            "status": "EXACT_FROM_OBSERVER_CELL",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "derivation_id": "TSD3848_1_parent_variation_template",
            "object": "R_AB dynamics",
            "formula": "S_R=1/2 int dr W_R(r)(R_AB')^2 + int dr J_R(r) R_AB",
            "derivation": "vary R_AB with fixed endpoints or explicit boundary momentum",
            "result": RAB_EQUATION,
            "status": "EXACT_CONDITIONAL_EULER_LAGRANGE",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "derivation_id": "TSD3848_2_flux",
            "object": "reciprocal flux/charge",
            "formula": "Q_R(r)=W_R(r) R_AB'(r)",
            "derivation": "integrate the homogeneous equation when J_R=0",
            "result": "Q_R is conserved in source-free exterior annulus",
            "status": "EXACT_CONDITIONAL_FLUX_CHARGE",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "derivation_id": "TSD3848_3_zero_route",
            "object": "R_AB zero theorem",
            "formula": "J_R=0, Q_R=0, R_AB(infinity)=0, W_R>0 => R_AB=0",
            "derivation": "Q_R=0 gives R_AB'=0; outer normalization gives the constant zero",
            "result": "T^2 S=1 follows without fitting p if reciprocal charge neutrality is parent-derived",
            "status": "EXACT_CONDITIONAL_RAB_ZERO",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "derivation_id": "TSD3848_4_hair_route",
            "object": "R_AB finite hair",
            "formula": "R_AB(r)=-int_r^infty [Q_R(rho)/W_R(rho)] d rho; for W_R=r^2 and J_R=0, R_AB~Q_R/r",
            "derivation": "solve first-order flux equation with R_AB(infinity)=0",
            "result": "nonzero Q_R is a physical reciprocal-hair residual, not harmless notation",
            "status": "EXACT_CONDITIONAL_HAIR_SOLUTION",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "derivation_id": "TSD3848_5_current_verdict",
            "object": "current MTS T,S dynamics",
            "formula": RAB_BOUND,
            "derivation": "existing corpus supplies the equation/charge contract but not a parent-signed neutrality theorem",
            "result": "R_AB zero is not claimed; the residual is now finite and named",
            "status": "ZERO_NOT_CLAIMED_BOUND_RETAINED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def rab_lemma_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "lemma_id": "RZL3848_0_energy_identity",
            "claim": "positive reciprocal operator has no source-free zero-boundary mode",
            "conditions": "W_R(r)>0; R_AB(infinity)=0; regular inner boundary; J_R=0; Q_R=0",
            "proof": "int W_R(R_AB')^2 dr = [R_AB W_R R_AB']_boundary - int R_AB J_R dr = 0",
            "result": "R_AB'=0 and R_AB=0",
            "status": "EXACT_CONDITIONAL_NO_HAIR_LEMMA",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "lemma_id": "RZL3848_1_source_bound",
            "claim": "finite source/hair branch has an explicit bound",
            "conditions": "W_R>=W_min>0 on exterior interval and absolute source/hair norms exist",
            "proof": "integrate R_AB'=(Q_R+int J_R dr)/W_R and take absolute values",
            "result": "sup|R_AB| <= C_W(|Q_R|+int|J_R|dr+boundary residuals)",
            "status": "EXACT_BOUND_TEMPLATE_NONCLAIM",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "lemma_id": "RZL3848_2_failure_modes",
            "claim": "R_AB zero fails only through named channels",
            "conditions": "any of J_R, Q_R, boundary reference, W_R positivity, or endpoint normalization is unsigned/nonzero",
            "proof": "these are exactly the terms left in the integrated solution",
            "result": RAB_BOUND,
            "status": "FINITE_FAILURE_LEDGER",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def weak_field_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "map_id": "WFM3848_0_clock_potential",
            "target": "Newtonian clock potential",
            "formula": WEAK_T,
            "derivation": "using ds^2=-c_*^2 T^2 dt^2+..., slow-clock/load convention from 10 gives T^2=1-2U_T/c_*^2+O(U^2)",
            "result": "T supplies the Newtonian potential once source normalization is separately owned",
            "status": "EXACT_WEAK_FIELD_DEFINITION",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "map_id": "WFM3848_1_RAB_to_spatial",
            "target": "spatial radial factor",
            "formula": "S=exp(R_AB)/T^2",
            "derivation": "rearrange R_AB=ln(T^2 S)",
            "result": "if R_AB=0 and T^2=1-2U_T/c_*^2, then S=1+2U_T/c_*^2+O(U_T^2)",
            "status": "EXACT_WEAK_FIELD_RECIPROCAL_LOCK",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "map_id": "WFM3848_2_Newton",
            "target": "Newtonian limit",
            "formula": "nabla^2 U_T = 4*pi*G_ref*rho_H + residual_TS",
            "derivation": "combine 3818 Poisson bridge with U_T if the EH/source branch owns the same T potential",
            "result": "Newton needs T equation/source normalization, not R_AB alone",
            "status": "CONDITIONAL_FROM_3818_WITH_RESIDUAL",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "map_id": "WFM3848_3_gamma_lane",
            "target": "gamma/no-slip lane",
            "formula": "R_AB=0 locks radial reciprocal spatial response; finite R_AB enters gamma/readout residual",
            "derivation": "S=1/T^2 gives the GR-like reciprocal radial coefficient in the static exterior branch",
            "result": "gamma route is helped, but still needs gauge/readout/no-slip clauses from 3830-3836",
            "status": "CONDITIONAL_GAMMA_SUPPORT_NOT_FULL_PPN",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "map_id": "WFM3848_4_beta_guard",
            "target": "beta",
            "formula": "R_AB=0 does not imply B_t=C_t^2",
            "derivation": "beta is second-order temporal self-coupling, already isolated in 3837-3845",
            "result": "beta remains blocked by EH2/readout/boundary/source terms",
            "status": "NO_BETA_SHORTCUT",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def ppn_update_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "row_id": "PPNU3848_0_RAB_component",
            "observable": "gamma/readout residual",
            "formula": "B_gamma_RAB <= |R_AB|/|Phi_ref| + gauge/domain conversion residual",
            "status": "NEW_BOUND_COMPONENT_NONCLAIM",
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "PPNU3848_1_Newton_component",
            "observable": "Newtonian source equation",
            "formula": "residual_TS = residual_Poisson + residual_T_owner + residual_source_norm",
            "status": "SOURCE_NORMALIZATION_REMAINS_REQUIRED",
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "PPNU3848_2_beta_component",
            "observable": "beta-1",
            "formula": "beta remains controlled by 3843-3845 beta/EH2 ledger; R_AB zero is not a beta proof",
            "status": "BETA_GUARD_RETAINED",
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
    ]


def gate_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "gate_id": "GATE3848_0_RAB_equation",
            "gate": "R_AB equation/charge derivation",
            "status": "PASS_EXACT_CONDITIONAL_EQUATION",
            "claim_allowed": False,
            "reason": "variation of reciprocal-strain action gives d(W_R R_AB')/dr=J_R",
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "GATE3848_1_RAB_zero",
            "gate": "R_AB=0 theorem for current MTS",
            "status": "BLOCKED_QR_JR_PARENT_NEUTRALITY_REQUIRED",
            "claim_allowed": False,
            "reason": "Q_R=0 and J_R=0 are exact sufficient clauses but not parent-signed",
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "GATE3848_2_Newton",
            "gate": "Newtonian limit from T",
            "status": "BLOCKED_T_EQUATION_AND_SOURCE_NORMALIZATION_REQUIRED",
            "claim_allowed": False,
            "reason": "U_T is defined, but Poisson/source ownership still relies on 3818 chain",
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "GATE3848_3_gamma",
            "gate": "gamma/local spatial lock",
            "status": "PARTIAL_RAB_SUPPORT_NONCLAIM",
            "claim_allowed": False,
            "reason": "R_AB=0 supports reciprocal spatial lock but no-slip/gauge/readout rows remain active",
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "GATE3848_4_beta",
            "gate": "beta",
            "status": "BLOCKED_NO_BETA_SHORTCUT",
            "claim_allowed": False,
            "reason": "R_AB zero does not derive second-order temporal self-coupling",
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "GATE3848_5_next_action",
            "gate": "next target attacks reciprocal neutrality/source",
            "status": "PASS_ACTIONABLE_NEXT",
            "claim_allowed": False,
            "reason": "the exact remaining obstruction is Q_R/J_R, not the coframe or metric bridge",
            "timestamp_utc": timestamp,
        },
    ]


def decision_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "decision_id": "DEC3848_0",
            "decision": "R_AB zero is derivable conditionally, not currently claimed",
            "consequence": "do not call reciprocal routing an axiom; pursue Q_R/J_R neutrality",
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "DEC3848_1",
            "decision": "Newton and gamma get partial structural support",
            "consequence": "T defines a potential and R_AB=0 would lock S=1/T^2, but source normalization/no-slip remain separate gates",
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "DEC3848_2",
            "decision": "beta remains separate",
            "consequence": "continue to keep the EH2/beta ledger active; no shortcut from AB=1 to beta=1",
            "timestamp_utc": timestamp,
        },
    ]


def next_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "next_id": "NEXT3848_0",
            "next_checkpoint": "3849-Y5-R2FR-reciprocal-charge-neutrality-source-bound-or-RAB-hair-row.md",
            "script": "scripts/Y5_R2FR_3849_reciprocal_charge_neutrality_source_bound_or_RAB_hair_row.py",
            "objective": "try to prove Q_R=0 and J_R=0 from parent source/boundary neutrality; if not, emit a strict finite R_AB hair/source row for PPN projection",
            "reason": "3848 shows R_AB=0 follows exactly from reciprocal neutrality, so the real next target is the neutrality/source theorem",
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH,
            "status": "PASS_NONCLAIM_RAB_ZERO_OR_HAIR_DYNAMICS",
            "claim": "no R_AB zero, Newton, gamma, beta, local-GR, or PPN claim",
            "next": "3849 reciprocal charge neutrality source bound or R_AB hair row",
            "timestamp_utc": timestamp,
        }
    ]


def markdown_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    body = []
    for row in rows:
        vals = [str(row.get(col, "")).replace("\n", " ").replace("|", "\\|") for col in columns]
        body.append("| " + " | ".join(vals) + " |")
    return "\n".join([header, sep, *body])


def write_doc(
    sources: list[dict[str, object]],
    dynamics: list[dict[str, object]],
    rab_lemma: list[dict[str, object]],
    weak_field: list[dict[str, object]],
    ppn_update: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    timestamp: str,
) -> None:
    text = f"""# 3848 - T,S Dynamics R_AB Zero Or Weak-Field Equation Bound

Private checkpoint. This attacks the dynamics behind the 3847 coframe: can `T(r),S(r)` derive reciprocal routing and weak-field GR structure, or does `R_AB` remain a finite hair? It does not claim local GR.

Generated: `{timestamp}`

## Result

The observer-cell strain is:

`{RAB}`.

The exact conditional dynamics are:

`{RAB_EQUATION}`.

If `J_R=0`, `Q_R=W_R R_AB'=0`, `R_AB(infinity)=0`, and `W_R>0`, then:

`R_AB=0`, hence `T^2 S=1`.

If neutrality fails, the honest residual is:

`{RAB_BOUND}`.

This is progress: the next obstruction is not vague. It is the reciprocal charge/source pair `Q_R,J_R`.

## Source Register

{markdown_table(sources, ["source_id", "path", "exists", "needle_found", "role"])}

## T,S Dynamics

{markdown_table(dynamics, ["derivation_id", "object", "formula", "status", "result"])}

## R_AB Zero Or Hair Lemma

{markdown_table(rab_lemma, ["lemma_id", "claim", "conditions", "status", "result"])}

## Weak-Field Map

{markdown_table(weak_field, ["map_id", "target", "formula", "status", "result"])}

## PPN Impact Update

{markdown_table(ppn_update, ["row_id", "observable", "formula", "status"])}

## Claim Gates

{markdown_table(gates, ["gate_id", "status", "claim_allowed", "reason"])}

## Decisions

{markdown_table(decisions, ["decision_id", "decision", "consequence"])}

## Bottom Line

The route is alive and sharper. We can now say exactly what must be proved: parent neutrality must kill `Q_R` and `J_R`. If it does, `T^2S=1` follows. If it does not, `R_AB` becomes a finite PPN/readout hair row rather than a hidden closure assumption. Newton still needs the `T` source equation; gamma gets support from reciprocal locking; beta remains a separate second-order self-coupling gate.

Next target: `3849-Y5-R2FR-reciprocal-charge-neutrality-source-bound-or-RAB-hair-row.md`.
"""
    DOC_PATH.write_text(text, encoding="utf-8")


def update_spine(timestamp: str) -> None:
    if not SPINE_PATH.exists():
        return
    text = read_text(SPINE_PATH)
    text = text.replace("Current State After 3847", "Current State After 3848", 1)
    text = "\n".join(
        line for line in text.splitlines() if not line.startswith("<!-- Generated by 3848 at ")
    )
    paragraph = (
        "`3848` derives the exact conditional dynamics of the reciprocal observer-cell strain. "
        "`R_AB=ln(T^2S)=2ln(J_q)` obeys `d/dr[W_R R_AB']=J_R` if the reciprocal-strain sector is parent-owned. "
        "With `J_R=0`, `Q_R=W_R R_AB'=0`, `R_AB(infinity)=0`, and `W_R>0`, the no-hair lemma gives `R_AB=0` and therefore `T^2S=1`; if not, the retained residual is "
        "`B_RAB <= B_QR_hair+B_JR_source+B_inner_boundary+B_outer_reference+B_W_degeneracy`. "
        "This supports the Newton/gamma route by defining `U_T=(c_*^2/2)(1-T^2)` and locking `S=1/T^2` when `R_AB=0`, but it does not prove beta. "
        "The next bottleneck is now sharply `Q_R,J_R` reciprocal neutrality/source ownership.\n\n"
    )
    anchor = "`3847` completes"
    if paragraph not in text and anchor in text:
        text = text.replace(anchor, paragraph + anchor, 1)
    old_gate = """`3848-Y5-R2FR-TS-dynamics-RAB-zero-or-weak-field-equation-bound.md`

Target: derive the dynamics/constraint for `T(r),S(r)`, especially `R_AB=ln(T^2S)=0` or weak-field equations needed for Newton/gamma/beta.

This is the best next move because 3847 completes the static spherical coframe; the missing step is now dynamics, not metric existence."""
    new_gate = """`3849-Y5-R2FR-reciprocal-charge-neutrality-source-bound-or-RAB-hair-row.md`

Target: prove `Q_R=0` and `J_R=0` from parent source/boundary neutrality, or emit a strict finite `R_AB` hair/source row for PPN projection.

This is the best next move because 3848 shows `R_AB=0` follows exactly from reciprocal neutrality, making `Q_R,J_R` the real obstruction."""
    if old_gate in text:
        text = text.replace(old_gate, new_gate, 1)
    artifact_anchor = "## Machine Artifacts\n\n"
    artifact_block = (
        "- `source-intake\\mts_residuals\\P8_Y5_R2FR_3848_TS_DYNAMICS_DERIVATION.csv`\n"
        "- `source-intake\\mts_residuals\\P8_Y5_R2FR_3848_RAB_ZERO_OR_HAIR_LEMMA.csv`\n"
        "- `source-intake\\mts_residuals\\P8_Y5_R2FR_3848_WEAK_FIELD_TS_MAP.csv`\n"
        "- `source-intake\\mts_residuals\\P8_Y5_BRR545_3848_VALIDATION.csv`\n"
    )
    if artifact_anchor in text and "P8_Y5_R2FR_3848_TS_DYNAMICS_DERIVATION.csv" not in text:
        text = text.replace(artifact_anchor, artifact_anchor + artifact_block, 1)
    text = text.rstrip() + f"\n\n<!-- Generated by 3848 at {timestamp} -->\n"
    SPINE_PATH.write_text(text, encoding="utf-8")


def validation_rows(
    sources: list[dict[str, object]],
    dynamics: list[dict[str, object]],
    rab_lemma: list[dict[str, object]],
    weak_field: list[dict[str, object]],
    ppn_update: list[dict[str, object]],
    gates: list[dict[str, object]],
    timestamp: str,
) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []

    def add(check_id: str, check: str, passed: bool, detail: str) -> None:
        rows.append(
            {
                "check_id": check_id,
                "check": check,
                "status": "PASS" if passed else "FAIL",
                "detail": detail,
                "timestamp_utc": timestamp,
            }
        )

    all_text = " ".join(str(row) for row in dynamics + rab_lemma + weak_field + ppn_update + gates)
    add(
        "VAL3848_0_sources",
        "all cited local source paths exist and needles are found",
        all(row["exists"] and row["needle_found"] for row in sources),
        f"{sum(1 for row in sources if row['exists'] and row['needle_found'])}/{len(sources)} sources resolved",
    )
    add(
        "VAL3848_1_RAB_definition",
        "R_AB observer-cell definition is present",
        RAB in all_text,
        "R_AB=ln(T^2 S)=2ln(J_q) present",
    )
    add(
        "VAL3848_2_equation",
        "R_AB dynamics equation is present",
        RAB_EQUATION in all_text and "W_R(r) R_AB'(r)" in all_text,
        "reciprocal-strain equation and charge present",
    )
    add(
        "VAL3848_3_zero_lemma",
        "zero/no-hair lemma is present",
        "R_AB=0" in all_text and "J_R=0" in all_text and "Q_R=0" in all_text and "W_R>0" in all_text,
        "R_AB zero conditions present",
    )
    add(
        "VAL3848_4_hair_bound",
        "finite R_AB hair bound is present",
        RAB_BOUND in all_text and "R_AB~Q_R/r" in all_text,
        "R_AB residual and hair solution present",
    )
    add(
        "VAL3848_5_weak_field",
        "weak-field T/S map is present",
        WEAK_T in all_text and "S=1/T^2" in all_text,
        "U_T and reciprocal weak-field lock present",
    )
    add(
        "VAL3848_6_beta_guard",
        "beta shortcut is blocked",
        "NO_BETA_SHORTCUT" in all_text and "R_AB=0 does not imply B_t=C_t^2" in all_text,
        "beta guard present",
    )
    add(
        "VAL3848_7_nonclaim",
        "all 3848 rows remain nonclaim",
        all(not bool(row.get("valid_for_claim", row.get("claim_allowed", False))) for row in dynamics + rab_lemma + weak_field + ppn_update + gates),
        "valid_for_claim/claim_allowed false throughout",
    )
    add(
        "VAL3848_8_next_neutrality",
        "next target attacks Q_R/J_R neutrality",
        DOC_PATH.exists() and "3849-Y5-R2FR-reciprocal-charge-neutrality-source-bound-or-RAB-hair-row" in read_text(DOC_PATH),
        "3849 reciprocal neutrality target visible",
    )
    for key, output_path in OUTPUTS.items():
        if key == "validation":
            continue
        parsed = False
        detail = rel(output_path)
        if output_path.suffix == ".csv" and output_path.exists():
            count = len(read_csv_rows(output_path))
            parsed = count > 0
            detail += f" rows={count}"
        add(f"VAL3848_9_parse_{key}", f"{key} CSV parses cleanly", parsed, detail)
    add(
        "VAL3848_10_doc",
        "markdown checkpoint document exists",
        DOC_PATH.exists() and "reciprocal charge/source pair" in read_text(DOC_PATH),
        rel(DOC_PATH),
    )
    fwb_hits = []
    if FWB.exists():
        for pattern in ("P8_Y5_R2FR_3848*", "P8_Y5_BRR545_3848*", "*Y5_R2FR_3848*", "3848-Y5-R2FR*"):
            fwb_hits.extend(path for path in FWB.rglob(pattern) if path.is_file())
    add(
        "VAL3848_11_formalization_clean",
        "formalization-workbench has no generated 3848 project files",
        len(fwb_hits) == 0,
        "; ".join(str(path) for path in fwb_hits) if fwb_hits else "no generated 3848 project file hits under formalization-workbench",
    )
    pycache_hits = list((PCW / "scripts").rglob("__pycache__"))
    add(
        "VAL3848_12_pycache_removed",
        "scripts __pycache__ removed",
        len(pycache_hits) == 0,
        "; ".join(str(path) for path in pycache_hits) if pycache_hits else "no __pycache__ directories",
    )
    return rows


def main() -> int:
    timestamp = now_utc()
    OUT.mkdir(parents=True, exist_ok=True)
    sources = source_register_rows(timestamp)
    dynamics = dynamics_rows(timestamp)
    rab_lemma = rab_lemma_rows(timestamp)
    weak_field = weak_field_rows(timestamp)
    ppn_update = ppn_update_rows(timestamp)
    gates = gate_rows(timestamp)
    decisions = decision_rows(timestamp)
    next_target = next_rows(timestamp)
    status = status_rows(timestamp)

    write_csv(OUTPUTS["sources"], sources)
    write_csv(OUTPUTS["dynamics"], dynamics)
    write_csv(OUTPUTS["rab_lemma"], rab_lemma)
    write_csv(OUTPUTS["weak_field"], weak_field)
    write_csv(OUTPUTS["ppn_update"], ppn_update)
    write_csv(OUTPUTS["gates"], gates)
    write_csv(OUTPUTS["decisions"], decisions)
    write_csv(OUTPUTS["next"], next_target)
    write_csv(OUTPUTS["status"], status)
    write_doc(sources, dynamics, rab_lemma, weak_field, ppn_update, gates, decisions, timestamp)
    update_spine(timestamp)

    for pycache in (PCW / "scripts").rglob("__pycache__"):
        shutil.rmtree(pycache, ignore_errors=True)

    validation = validation_rows(sources, dynamics, rab_lemma, weak_field, ppn_update, gates, timestamp)
    write_csv(OUTPUTS["validation"], validation)
    failed = [row for row in validation if row["status"] != "PASS"]
    if failed:
        for row in failed:
            print(f"FAIL {row['check_id']}: {row['detail']}")
        return 1
    print(f"{CHECKPOINT} PASS_NONCLAIM_RAB_ZERO_OR_HAIR_DYNAMICS")
    print(rel(DOC_PATH))
    print(rel(OUTPUTS["validation"]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
