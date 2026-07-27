from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from decimal import Decimal
from pathlib import Path


CHECKPOINT = "3854"
BRANCH = "MTS_R2FR_Y5_OBSERVER_CELL_GAUGE_OR_TOPOLOGICAL_CHARGE_ORIGIN_3854"

PCW = Path(__file__).resolve().parents[1]
ROOT = PCW.parent
FWB = ROOT / "formalization-workbench"
OUT = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "3854-Y5-R2FR-observer-cell-gauge-or-topological-charge-origin.md"
SPINE_PATH = PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

P_10_OBSERVER = PCW / "10-observer-map-symplectic-contract.md"
P_11_CURRENT = PCW / "11-cell-current-origin-attempt.md"
P_12_GAUGE = PCW / "12-gauge-noether-origin-audit.md"
P_13_BENCHMARK = PCW / "13-local-closure-PPN-benchmark.md"
CSV_3853_COFRAME = OUT / "P8_Y5_R2FR_3853_RADIAL_CELL_COFRAME_DERIVATION.csv"
CSV_3853_ACTION = OUT / "P8_Y5_R2FR_3853_COFRAME_CELL_ACTION_CANDIDATE.csv"
CSV_3853_CLOSURE = OUT / "P8_Y5_R2FR_3853_EXPLICIT_CLOSURE_ORIGIN_LEDGER.csv"
CSV_3853_VALIDATION = OUT / "P8_Y5_BRR545_3853_VALIDATION.csv"
CSV_3852_PROOF = OUT / "P8_Y5_R2FR_3852_RAB_ZERO_PROOF_STATUS.csv"
CSV_3851_BUDGET = OUT / "P8_Y5_R2FR_3851_RAB_BUDGET_FROM_CASSINI_NEAR_LIMB.csv"

OUTPUTS = {
    "sources": OUT / "P8_Y5_R2FR_3854_SOURCE_REGISTER.csv",
    "gauge": OUT / "P8_Y5_R2FR_3854_OBSERVER_CELL_GAUGE_AUDIT.csv",
    "topology": OUT / "P8_Y5_R2FR_3854_TOPOLOGICAL_CELL_CHARGE_AUDIT.csv",
    "theorem": OUT / "P8_Y5_R2FR_3854_CELL_LOCK_THEOREM_STATUS.csv",
    "branch": OUT / "P8_Y5_R2FR_3854_RAB_BRANCH_DECISION.csv",
    "handoff": OUT / "P8_Y5_R2FR_3854_BETA_SOURCE_HANDOFF_QUEUE.csv",
    "gates": OUT / "P8_Y5_R2FR_3854_CLAIM_GATES.csv",
    "decisions": OUT / "P8_Y5_R2FR_3854_DECISION_ROWS.csv",
    "next": OUT / "P8_Y5_R2FR_3854_NEXT_TARGET.csv",
    "status": OUT / "P8_Y5_R2FR_3854_STATUS.csv",
    "validation": OUT / "P8_Y5_BRR545_3854_VALIDATION.csv",
}

SOURCE_SPECS = [
    ("SRC3854_0_10_observer", P_10_OBSERVER, "J_q = T sqrt(S)"),
    ("SRC3854_1_11_current", P_11_CURRENT, "ordinary cell-current conservation does not close"),
    ("SRC3854_2_12_gauge", P_12_GAUGE, "gauge_noether_origin_not_derived_closure_only"),
    ("SRC3854_3_13_benchmark", P_13_BENCHMARK, "local_closure_ppn_benchmark_valid_control_not_derivation"),
    ("SRC3854_4_3853_coframe", CSV_3853_COFRAME, "Omega_tr=Omega_ref"),
    ("SRC3854_5_3853_action", CSV_3853_ACTION, "S_cell=int_U Lambda_J"),
    ("SRC3854_6_3853_closure", CSV_3853_CLOSURE, "EXPLICIT_CLOSURE_IF_NOT_PARENT_DERIVED"),
    ("SRC3854_7_3853_validation", CSV_3853_VALIDATION, "PASS"),
    ("SRC3854_8_3852_proof", CSV_3852_PROOF, "NOT_PROVED_FOR_STRICT_CURRENT_CORPUS"),
    ("SRC3854_9_3851_budget", CSV_3851_BUDGET, "6.102178699076298e-11"),
]

OMEGA_DEF = "Omega_tr=(theta^0/c) wedge theta^1=T*sqrt(S) dt wedge dr"
CELL_LOCK = "Omega_tr=Omega_ref=dt wedge dr"
CELL_ZERO = "Omega_tr=Omega_ref => T*sqrt(S)=1 => ln(T^2 S)=0 => R_AB=0"
ALL_SUBDOMAIN_CHARGE = "Q_cell[D]=int_D (Omega_tr-Omega_ref)=0 for every local radial cell D"
FINITE_HAIR_BOUND = "B_RAB <= C_W*(|Pi_R|+|Pi_R_ct|+int|J_R|dr+|Delta_R_boundary|+|Delta_W|)"


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


def budget_value() -> Decimal:
    for row in read_csv_rows(CSV_3851_BUDGET):
        if row.get("budget_id") == "RBC3851_0_near_limb_scalar_budget":
            return Decimal(row["exact_log_bound"])
    raise RuntimeError("3851 R_AB budget row missing")


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
                "role": "input_for_observer_cell_gauge_or_topological_origin",
                "claim_use": "nonclaim_gauge_topology_audit_and_branch_decision",
                "timestamp_utc": timestamp,
            }
        )
    return rows


def gauge_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "audit_id": "OCG3854_0_areal_coordinate_gauge",
            "route": "radial coordinate gauge",
            "test": "use coordinate freedom to set T^2 S=1",
            "result": "rejected: areal radius fixes r through r^2 dOmega^2 and asymptotic clock fixes t; changing this is not the current observer readout",
            "status": "REJECTED_HIDDEN_GAUGE_IMPORT",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "audit_id": "OCG3854_1_local_lorentz_boost",
            "route": "SO(1,1) observer boost",
            "test": "theta^A -> Lambda^A_B theta^B in the t-r frame",
            "result": "det Lambda=1 preserves Omega_tr; it cannot set Omega_tr=Omega_ref if the scalar density is not already equal",
            "status": "PRESERVES_CELL_DOES_NOT_FIX_IT",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "audit_id": "OCG3854_2_reciprocal_split_rescaling",
            "route": "T -> exp(sigma)T and sqrt(S)->exp(-sigma)sqrt(S)",
            "test": "move clock/routing split while preserving product",
            "result": "leaves T sqrt(S) invariant; useful split-gauge candidate but cannot impose J_tr=1",
            "status": "PRESERVES_PRODUCT_DOES_NOT_FIX_PRODUCT",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "audit_id": "OCG3854_3_cell_scale_gauge",
            "route": "scale Omega_tr itself as gauge",
            "test": "declare T sqrt(S) unobservable and gauge-fix it to 1",
            "result": "would require rebuilding matter/clocks/rods/light readout so gamma is gauge-invariant; current MTS uses this coframe as observable",
            "status": "REJECTED_UNOWNED_MATTER_READOUT_REBUILD",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "audit_id": "OCG3854_4_noether_identity",
            "route": "Noether/Ward identity",
            "test": "derive R_AB=0 from an identity among equations",
            "result": "Noether identities relate Euler equations; they produce a zero only if a constraint equation or first-class generator is already present",
            "status": "REJECTED_WITHOUT_PARENT_CONSTRAINT",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def topology_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "audit_id": "TCA3854_0_closed_two_form",
            "route": "closed radial two-form",
            "test": "d Omega_tr=0 in the static t-r sector",
            "result": "closedness is automatic/too weak; a closed top-degree two-form may have arbitrary density T sqrt(S)",
            "status": "REJECTED_TOO_WEAK",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "audit_id": "TCA3854_1_single_global_charge",
            "route": "global cell charge",
            "test": "int_D(Omega_tr-Omega_ref)=0 on one selected domain",
            "result": "fixes only an average over D; local density and therefore R_AB hair can remain",
            "status": "REJECTED_AVERAGE_NOT_POINTWISE",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "audit_id": "TCA3854_2_all_subdomain_charge",
            "route": "all-subdomain topological/cell charge",
            "test": ALL_SUBDOMAIN_CHARGE,
            "result": "by the fundamental lemma, the density vanishes pointwise: Omega_tr=Omega_ref and R_AB=0",
            "status": "PROVES_CELL_LOCK_IF_PARENT_SIGNED_BUT_EQUIVALENT_TO_CONSTRAINT",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "audit_id": "TCA3854_3_quantized_charge",
            "route": "integer/topological quantization",
            "test": "assign an integer cell charge to the exterior branch",
            "result": "quantization fixes a global sector label, not the local continuous density, unless all local cells are constrained",
            "status": "REJECTED_FOR_LOCAL_LOCK_WITHOUT_ALL_CELL_RULE",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def theorem_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "theorem_id": "CLT3854_0_gauge_verdict",
            "premise": "current observer coframe is physical/readout-coupled",
            "derivation": "admissible observer boosts or reciprocal split changes preserve Omega_tr or change the observable readout; coordinate gauge is fixed by areal r and asymptotic t",
            "result": "gauge does not derive Omega_tr=Omega_ref",
            "status": "NO_GAUGE_DERIVATION",
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "CLT3854_1_topological_conditional",
            "premise": ALL_SUBDOMAIN_CHARGE,
            "derivation": "if int_D f dt dr=0 for every local radial cell D, then f=0 pointwise; here f=T sqrt(S)-1",
            "result": CELL_ZERO,
            "status": "PROVED_IF_ALL_SUBDOMAIN_CELL_CHARGE_PARENT_SIGNED",
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "CLT3854_2_strict_current_verdict",
            "premise": "current 01-13 plus 3852-3853 sources",
            "derivation": "the exact lock is identified but no source signs the all-subdomain charge or first-class cell constraint",
            "result": "R_AB=0 is explicit closure/control branch, not strict-current derivation",
            "status": "CELL_LOCK_NOT_DERIVED_CURRENT_CORPUS",
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
    ]


def branch_rows(timestamp: str) -> list[dict[str, object]]:
    budget = budget_value()
    return [
        {
            "branch_id": "RBD3854_0_closure_branch",
            "branch": "explicit_RAB_zero_closure",
            "rule": CELL_LOCK,
            "status": "FREEZE_AS_CONTROL_BRANCH_NOT_DERIVED",
            "what_it_allows": "local gamma/R_AB throat can be tested as GR-control lane without pretending derivation",
            "what_it_does_not_allow": "no strict local-GR or parent-derivation claim",
            "next_use": "handoff to beta/Newton/source consistency with closure label carried",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "branch_id": "RBD3854_1_finite_hair_branch",
            "branch": "finite_RAB_hair",
            "rule": FINITE_HAIR_BOUND,
            "status": "RETAIN_AS_SEVERE_BOUND_BRANCH",
            "what_it_allows": f"source-backed B_RAB can remain if below {budget} before other gamma residuals",
            "what_it_does_not_allow": "no unsourced reciprocal hair; no fitted PPN p",
            "next_use": "only revisit if source-backed Pi_R/J_R/boundary rows exist",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def handoff_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "handoff_id": "BSH3854_0_beta",
            "target": "beta/second-order temporal self-coupling",
            "required_carry_forward": "R_AB branch label: explicit closure or finite-hair residual; do not use R_AB=0 as derived theorem",
            "reason": "gamma throat has been disciplined; full local GR still needs beta=1",
            "status": "NEXT_PRIORITY",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "handoff_id": "BSH3854_1_Newton_source",
            "target": "Newton/source normalization",
            "required_carry_forward": "same observed coframe, source mass/active Hamiltonian charge, no orbital-GM circularity",
            "reason": "R_AB closure does not derive Newton source coupling or calibrated G/source normalization",
            "status": "OPEN_PARALLEL_PRIORITY",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "handoff_id": "BSH3854_2_EM_stress",
            "target": "Maxwell/EM stress and Poynting exchange",
            "required_carry_forward": "same coframe/source action; EM stress must be in the Hilbert/source ledger",
            "reason": "local GR consistency needs total stress conservation, not only the R_AB gamma branch",
            "status": "OPEN_PARALLEL_PRIORITY",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def gate_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "gate_id": "GATE3854_0_gauge_origin",
            "gate": "gauge derives Omega_tr=Omega_ref",
            "status": "FAIL_CURRENT_CORPUS",
            "claim_allowed": False,
            "reason": "admissible gauges preserve the cell or require unowned readout rebuild; none set it to reference",
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "GATE3854_1_topological_origin",
            "gate": "topology derives local cell lock",
            "status": "CONDITIONAL_ONLY_ALL_SUBDOMAIN_CHARGE_REQUIRED",
            "claim_allowed": False,
            "reason": "single/global charge is too weak; all-subdomain charge proves the lock but is equivalent to a parent constraint",
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "GATE3854_2_closure_honesty",
            "gate": "R_AB=0 branch labelled correctly",
            "status": "PASS_EXPLICIT_CONTROL_BRANCH",
            "claim_allowed": False,
            "reason": "closure branch is useful as a GR-control lane but not a derivation",
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "GATE3854_3_finite_hair",
            "gate": "finite R_AB branch retained",
            "status": "PASS_BOUND_BRANCH_RETAINED_NONCLAIM",
            "claim_allowed": False,
            "reason": "finite hair remains possible only with source-backed severe bound rows",
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "GATE3854_4_pivot",
            "gate": "stop circling R_AB throat",
            "status": "PASS_HANDOFF_TO_BETA_SOURCE",
            "claim_allowed": False,
            "reason": "next progress is beta/source/EM consistency with R_AB branch label carried",
            "timestamp_utc": timestamp,
        },
    ]


def decision_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "decision_id": "DEC3854_0",
            "decision": "gauge does not derive the radial cell lock in the current scaffold",
            "consequence": "do not advertise R_AB=0 as gauge",
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "DEC3854_1",
            "decision": "topology only works if every local radial cell has zero charge",
            "consequence": "that is a clean conditional theorem but is effectively the parent constraint in integral form",
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "DEC3854_2",
            "decision": "freeze R_AB=0 as explicit closure/control branch and retain finite hair as severe bound branch",
            "consequence": "move to beta/Newton/source consistency rather than looping the same throat",
            "timestamp_utc": timestamp,
        },
    ]


def next_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "next_id": "NEXT3854_0",
            "next_checkpoint": "3855-Y5-R2FR-RAB-closure-freeze-and-beta-source-consistency-handoff.md",
            "script": "scripts/Y5_R2FR_3855_RAB_closure_freeze_and_beta_source_consistency_handoff.py",
            "objective": "freeze the R_AB branch labels, carry explicit closure/finite-hair status into the local-GR dashboard, and resume beta/Newton/source/EM consistency without pretending R_AB=0 is derived",
            "reason": "3854 exhausts the current gauge/topology origin routes; the real project now needs beta and calibrated source coupling",
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH,
            "status": "PASS_NONCLAIM_GAUGE_TOPOLOGY_AUDIT_CLOSURE_FREEZE",
            "claim": "no strict-current R_AB zero, gamma, PPN, Newton, beta, EM, or local-GR claim",
            "result": "gauge/topology does not derive cell lock except by all-subdomain constraint; freeze R_AB closure branch and pivot",
            "next": "3855 R_AB closure freeze and beta/source consistency handoff",
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
    gauge: list[dict[str, object]],
    topology: list[dict[str, object]],
    theorem: list[dict[str, object]],
    branch: list[dict[str, object]],
    handoff: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    timestamp: str,
) -> None:
    budget = budget_value()
    text = f"""# 3854 - Observer Cell Gauge Or Topological Charge Origin

Private checkpoint. This tests the last obvious origin routes for the 3853 cell lock:

`{CELL_LOCK}`.

Generated: `{timestamp}`

## Result

The exact object is:

`{OMEGA_DEF}`.

The desired zero route is:

`{CELL_ZERO}`.

Gauge does not derive it in the current scaffold. Local Lorentz/observer boosts preserve `Omega_tr`; reciprocal split rescalings preserve `T sqrt(S)`; areal radial gauge is already fixed by `r^2 dOmega^2`; and making the whole cell scale gauge would require rebuilding matter, clock, rod, and photon readout.

Topology gives one conditional theorem, but it is not a free lunch:

`{ALL_SUBDOMAIN_CHARGE}`.

If this is parent-signed, then by the fundamental lemma `T sqrt(S)-1=0` pointwise and therefore `R_AB=0`. But that all-subdomain charge rule is basically the cell-lock constraint in integral form. A single global charge or closedness of the two-form is too weak.

So this checkpoint freezes the honest branch decision:

1. `R_AB=0` is an explicit local closure/control branch unless a future parent action signs the all-subdomain cell charge or first-class constraint.
2. finite `R_AB` hair remains a nonclaim source-bound branch and must beat `B_RAB <= {budget}` before other gamma residuals.
3. stop circling the same R_AB throat; carry the branch label into beta/Newton/source/EM consistency.

## Source Register

{markdown_table(sources, ["source_id", "path", "exists", "needle_found", "role"])}

## Gauge Audit

{markdown_table(gauge, ["audit_id", "route", "status", "result"])}

## Topological Cell Charge Audit

{markdown_table(topology, ["audit_id", "route", "status", "result"])}

## Cell Lock Theorem Status

{markdown_table(theorem, ["theorem_id", "premise", "status", "result"])}

## R_AB Branch Decision

{markdown_table(branch, ["branch_id", "branch", "status", "what_it_allows", "what_it_does_not_allow"])}

## Beta / Source Handoff Queue

{markdown_table(handoff, ["handoff_id", "target", "status", "reason"])}

## Claim Gates

{markdown_table(gates, ["gate_id", "status", "claim_allowed", "reason"])}

## Decisions

{markdown_table(decisions, ["decision_id", "decision", "consequence"])}

## Bottom Line

3854 is a fork-closer. It does not prove the local GR branch; it prevents us from pretending the cell lock was derived by gauge language. The disciplined state is now: explicit `R_AB=0` closure/control branch, finite-hair severe-bound branch, then move on to beta, Newton/source normalization, and EM stress consistency.

Next target: `3855-Y5-R2FR-RAB-closure-freeze-and-beta-source-consistency-handoff.md`.
"""
    DOC_PATH.write_text(text, encoding="utf-8")


def update_spine(timestamp: str) -> None:
    if not SPINE_PATH.exists():
        return
    budget = budget_value()
    text = read_text(SPINE_PATH)
    text = text.replace("Current State After 3853", "Current State After 3854", 1)
    text = "\n".join(
        line for line in text.splitlines() if not line.startswith("<!-- Generated by 3854 at ")
    )
    paragraph = (
        "`3854` audits the remaining gauge/topological origins for the 3853 cell lock. "
        "Gauge routes fail in the current scaffold: local Lorentz boosts preserve `Omega_tr`, reciprocal split rescalings preserve `T sqrt(S)`, areal radial gauge is fixed, and making the cell scale gauge would require an unowned matter/readout rebuild. "
        "Topology gives only a conditional theorem: if every local radial cell satisfies `Q_cell[D]=int_D(Omega_tr-Omega_ref)=0`, then `Omega_tr=Omega_ref` pointwise and `R_AB=0`; but that all-subdomain charge rule is the cell constraint in integral form, while single/global charge and closedness are too weak. "
        f"The branch is therefore frozen honestly: `R_AB=0` is an explicit closure/control branch unless a future parent action signs that cell charge, and finite hair remains source-bound with `B_RAB <= {budget}` before other gamma residuals. "
        "Next work should pivot to beta, Newton/source normalization, and EM stress consistency with the R_AB branch label carried.\n\n"
    )
    anchor = "`3853` sharpens"
    if paragraph not in text and anchor in text:
        text = text.replace(anchor, paragraph + anchor, 1)
    old_gate = """`3854-Y5-R2FR-observer-cell-gauge-or-topological-charge-origin.md`

Target: test whether `Omega_tr=Omega_ref` follows from observer-splitting gauge redundancy or a topological radial-cell charge; otherwise freeze it as explicit closure and move to beta/source consistency.

This is the best next move because 3853 sharpened lambda_R origin to a coframe two-form lock, but did not prove the lock from current MTS sources."""
    new_gate = """`3855-Y5-R2FR-RAB-closure-freeze-and-beta-source-consistency-handoff.md`

Target: freeze the R_AB branch labels, carry explicit closure/finite-hair status into the local-GR dashboard, and resume beta/Newton/source/EM consistency without pretending `R_AB=0` is derived.

This is the best next move because 3854 exhausts the current gauge/topology origin routes; the real project now needs beta and calibrated source coupling."""
    if old_gate in text:
        text = text.replace(old_gate, new_gate, 1)
    artifact_anchor = "## Machine Artifacts\n\n"
    artifact_block = (
        "- `source-intake\\mts_residuals\\P8_Y5_R2FR_3854_OBSERVER_CELL_GAUGE_AUDIT.csv`\n"
        "- `source-intake\\mts_residuals\\P8_Y5_R2FR_3854_TOPOLOGICAL_CELL_CHARGE_AUDIT.csv`\n"
        "- `source-intake\\mts_residuals\\P8_Y5_R2FR_3854_RAB_BRANCH_DECISION.csv`\n"
        "- `source-intake\\mts_residuals\\P8_Y5_BRR545_3854_VALIDATION.csv`\n"
    )
    if artifact_anchor in text and "P8_Y5_R2FR_3854_OBSERVER_CELL_GAUGE_AUDIT.csv" not in text:
        text = text.replace(artifact_anchor, artifact_anchor + artifact_block, 1)
    text = text.rstrip() + f"\n\n<!-- Generated by 3854 at {timestamp} -->\n"
    SPINE_PATH.write_text(text, encoding="utf-8")


def validation_rows(
    sources: list[dict[str, object]],
    gauge: list[dict[str, object]],
    topology: list[dict[str, object]],
    theorem: list[dict[str, object]],
    branch: list[dict[str, object]],
    handoff: list[dict[str, object]],
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

    budget = budget_value()
    all_text = " ".join(str(row) for row in gauge + topology + theorem + branch + handoff + gates)
    add(
        "VAL3854_0_sources",
        "all cited local source paths exist and needles are found",
        all(row["exists"] and row["needle_found"] for row in sources),
        f"{sum(1 for row in sources if row['exists'] and row['needle_found'])}/{len(sources)} sources resolved",
    )
    add("VAL3854_1_gauge_rejected", "gauge origin is rejected", "NO_GAUGE_DERIVATION" in all_text and "FAIL_CURRENT_CORPUS" in all_text, "gauge rejection present")
    add("VAL3854_2_topology_conditional", "topology conditional theorem is present", ALL_SUBDOMAIN_CHARGE in all_text and "PROVED_IF_ALL_SUBDOMAIN_CELL_CHARGE_PARENT_SIGNED" in all_text, "all-subdomain theorem present")
    add("VAL3854_3_closure_branch", "R_AB closure branch is frozen as nonclaim", "FREEZE_AS_CONTROL_BRANCH_NOT_DERIVED" in all_text, "closure branch decision present")
    add("VAL3854_4_finite_branch", "finite hair branch is retained with severe budget", str(budget) in all_text and "RETAIN_AS_SEVERE_BOUND_BRANCH" in all_text, str(budget))
    add("VAL3854_5_handoff", "beta/source handoff queue is present", "NEXT_PRIORITY" in all_text and "Newton/source normalization" in all_text and "Maxwell/EM stress" in all_text, "handoff rows present")
    add("VAL3854_6_nonclaim", "all 3854 rows remain nonclaim", all(not bool(row.get("valid_for_claim", row.get("claim_allowed", False))) for row in gauge + topology + theorem + branch + handoff + gates), "valid_for_claim/claim_allowed false throughout")
    add("VAL3854_7_next", "next target is 3855", DOC_PATH.exists() and "3855-Y5-R2FR-RAB-closure-freeze-and-beta-source-consistency-handoff" in read_text(DOC_PATH), "3855 target visible")
    for key, output_path in OUTPUTS.items():
        if key == "validation":
            continue
        parsed = False
        detail = rel(output_path)
        if output_path.suffix == ".csv" and output_path.exists():
            count = len(read_csv_rows(output_path))
            parsed = count > 0
            detail += f" rows={count}"
        add(f"VAL3854_8_parse_{key}", f"{key} CSV parses cleanly", parsed, detail)
    add("VAL3854_9_doc", "markdown checkpoint document exists", DOC_PATH.exists() and "fork-closer" in read_text(DOC_PATH), rel(DOC_PATH))
    fwb_hits = []
    if FWB.exists():
        for pattern in ("P8_Y5_R2FR_3854*", "P8_Y5_BRR545_3854*", "*Y5_R2FR_3854*", "3854-Y5-R2FR*"):
            fwb_hits.extend(path for path in FWB.rglob(pattern) if path.is_file())
    add("VAL3854_10_formalization_clean", "formalization-workbench has no generated 3854 project files", len(fwb_hits) == 0, "; ".join(str(path) for path in fwb_hits) if fwb_hits else "no generated 3854 project file hits under formalization-workbench")
    pycache_hits = list((PCW / "scripts").rglob("__pycache__"))
    add("VAL3854_11_pycache_removed", "scripts __pycache__ removed", len(pycache_hits) == 0, "; ".join(str(path) for path in pycache_hits) if pycache_hits else "no __pycache__ directories")
    return rows


def main() -> int:
    timestamp = now_utc()
    OUT.mkdir(parents=True, exist_ok=True)
    sources = source_register_rows(timestamp)
    gauge = gauge_rows(timestamp)
    topology = topology_rows(timestamp)
    theorem = theorem_rows(timestamp)
    branch = branch_rows(timestamp)
    handoff = handoff_rows(timestamp)
    gates = gate_rows(timestamp)
    decisions = decision_rows(timestamp)
    next_target = next_rows(timestamp)
    status = status_rows(timestamp)

    write_csv(OUTPUTS["sources"], sources)
    write_csv(OUTPUTS["gauge"], gauge)
    write_csv(OUTPUTS["topology"], topology)
    write_csv(OUTPUTS["theorem"], theorem)
    write_csv(OUTPUTS["branch"], branch)
    write_csv(OUTPUTS["handoff"], handoff)
    write_csv(OUTPUTS["gates"], gates)
    write_csv(OUTPUTS["decisions"], decisions)
    write_csv(OUTPUTS["next"], next_target)
    write_csv(OUTPUTS["status"], status)
    write_doc(sources, gauge, topology, theorem, branch, handoff, gates, decisions, timestamp)
    update_spine(timestamp)

    for pycache in (PCW / "scripts").rglob("__pycache__"):
        shutil.rmtree(pycache, ignore_errors=True)

    validation = validation_rows(sources, gauge, topology, theorem, branch, handoff, gates, timestamp)
    write_csv(OUTPUTS["validation"], validation)
    failed = [row for row in validation if row["status"] != "PASS"]
    if failed:
        for row in failed:
            print(f"FAIL {row['check_id']}: {row['detail']}")
        return 1
    print(f"{CHECKPOINT} PASS_NONCLAIM_GAUGE_TOPOLOGY_AUDIT_CLOSURE_FREEZE")
    print(rel(DOC_PATH))
    print(rel(OUTPUTS["validation"]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
