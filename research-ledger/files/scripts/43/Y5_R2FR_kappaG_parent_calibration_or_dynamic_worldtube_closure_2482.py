from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


BRANCH_ID = "MTS_R2FR_KAPPAG_PARENT_CALIBRATION_OR_DYNAMIC_WORLDTUBE_2482"
CHECKPOINT_ID = "2482"

ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = ROOT.parent
FORMALIZATION = PROJECT_ROOT / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"

DOC = ROOT / "2482-Y5-R2FR-kappaG-parent-calibration-or-dynamic-worldtube-closure.md"

OUTPUTS = {
    "source_register": OUT / "P8_Y5_KAPPAG_WORLD_2482_SOURCE_REGISTER.csv",
    "calibration_audit": OUT / "P8_Y5_KAPPAG_WORLD_2482_KAPPAG_CALIBRATION_AUDIT.csv",
    "dynamic_worldtube": OUT / "P8_Y5_KAPPAG_WORLD_2482_DYNAMIC_WORLDTUBE_AUDIT.csv",
    "enorm_components": OUT / "P8_Y5_KAPPAG_WORLD_2482_ENORM_COMPONENTS.csv",
    "claim_gates": OUT / "P8_Y5_KAPPAG_WORLD_2482_CLAIM_GATES.csv",
    "decision_ledger": OUT / "P8_Y5_KAPPAG_WORLD_2482_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_KAPPAG_WORLD_2482_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_KAPPAG_WORLD_2482_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2482_VALIDATION.csv",
}

COPY_TARGETS = {
    "calibration_audit": LOCAL_BOUNDS / "KappaG_parent_calibration_audit_2482_NONCLAIM.csv",
    "enorm_components": LOCAL_BOUNDS / "E_norm_component_retention_2482_NONCLAIM.csv",
    "acquisition_queue": QUEUE / "JR2482_PARENT_EH_COUPLING_OR_TAU_EXCHANGE_SOURCE.csv",
}

SOURCES = [
    {
        "source_id": "SRC2482_00_2481_doc",
        "source_path": ROOT / "2481-Y5-R2FR-Hilbert-worldtube-source-normalization-zero-certificate-or-Enorm-row.md",
        "needles": ["NEXT2481_0_selected", "e_kappaG", "VAL2481_OVERALL"],
        "role": "handoff selecting kappa/G calibration or dynamic worldtube closure",
    },
    {
        "source_id": "SRC2482_01_2404_poisson",
        "source_path": ROOT / "2404-Y5-R2FR-minimal-parent-action-first-variation-GR-Newton-gate-or-operator-residual-pack.md",
        "needles": ["kappa0=8 pi G_ref/c^4", "CANDIDATE_NOT_DERIVED", "REF2404_2_orbital_G_laundering"],
        "role": "candidate EH normalization and no orbital-G laundering",
    },
    {
        "source_id": "SRC2482_02_2467_exchange",
        "source_path": ROOT / "2467-Y5-R2FR-Hilbert-current-conservation-scale-and-clock-compatibility-gate.md",
        "needles": ["EXC2467_0_required_identity", "EXC2467_2_total_stress_route", "WTG2467_2_dynamic_surface"],
        "role": "dynamic exchange identity and worldtube drift blocker",
    },
    {
        "source_id": "SRC2482_03_2468_dynamic",
        "source_path": ROOT / "2468-Y5-R2FR-stationary-local-source-theorem-or-dynamic-exchange-current.md",
        "needles": ["DYN2468_1_exchange_required", "MISSING_PARENT_EXCHANGE", "SCP2468_0_parent_scale"],
        "role": "dynamic clock exchange and parent scale status",
    },
    {
        "source_id": "SRC2482_04_2477_metric_response",
        "source_path": ROOT / "2477-Y5-R2FR-parent-weak-field-metric-response-theorem-or-no-go.md",
        "needles": ["BLK2477_0_EH_origin", "CM2477_4_source_normalization", "GATE2477_3_local_GR"],
        "role": "EH origin/source-normalization blockers in metric response factorisation",
    },
    {
        "source_id": "SRC2482_05_2481_validation",
        "source_path": OUT / "P8_Y5_BRR545_2481_VALIDATION.csv",
        "needles": ["VAL2481_OVERALL", "PASS"],
        "role": "previous checkpoint validation",
    },
]


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def stamp(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "timestamp_utc": now(),
        "branch_id": BRANCH_ID,
        "checkpoint_id": CHECKPOINT_ID,
        **row,
    }


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8", newline="")
        return
    fieldnames = list(rows[0].keys())
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def csv_parses(path: Path) -> tuple[bool, int, str]:
    try:
        with path.open("r", encoding="utf-8", newline="") as handle:
            rows = list(csv.DictReader(handle))
        return True, len(rows), ""
    except Exception as exc:  # pragma: no cover
        return False, 0, str(exc)


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source in SOURCES:
        path = Path(source["source_path"])
        text = read_text(path)
        missing = [needle for needle in source["needles"] if needle not in text]
        rows.append(
            stamp(
                {
                    "source_id": source["source_id"],
                    "source_path": str(path),
                    "exists": path.exists(),
                    "missing_needles": ";".join(missing),
                    "source_pass": path.exists() and not missing,
                    "role": source["role"],
                }
            )
        )
    return rows


def calibration_audit_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "audit_id": "KAP2482_0_candidate_relation",
            "object": "kappa0/G_ref relation",
            "attempt": "Use the candidate weak-field relation kappa0=8*pi*G_ref/c^4.",
            "result": "This is an internally consistent normalization inside the candidate first-variation bridge.",
            "status": "PASS_CONDITIONAL_DEFINITION",
            "retained_gap": "not derived from deeper MTS parent action normalization",
            "valid_for_claim": False,
        },
        {
            "audit_id": "KAP2482_1_parent_origin",
            "object": "EH-leading coefficient",
            "attempt": "Derive kappa0 from the MTS parent action leading operator rather than importing EH as a template.",
            "result": "current corpus has EH candidate/template but not a signed MTS-to-EH leading-operator theorem",
            "status": "BLOCKED_PARENT_EH_ORIGIN",
            "retained_gap": "e_kappaG",
            "valid_for_claim": False,
        },
        {
            "audit_id": "KAP2482_2_measurement_role",
            "object": "G_ref",
            "attempt": "Treat G_ref as a measured value of a parent coupling after the coupling exists.",
            "result": "allowed later, but not allowed as proof input for Newton/source normalization",
            "status": "PASS_GUARDRAIL",
            "retained_gap": "parent coupling not sourced",
            "valid_for_claim": False,
        },
        {
            "audit_id": "KAP2482_3_orbital_laundering",
            "object": "observed orbital GM",
            "attempt": "Use orbital fits to calibrate kappa0, G_ref or source mass.",
            "result": "forbidden because it uses Newtonian target behavior to prove Newton",
            "status": "REJECTED_CIRCULAR",
            "retained_gap": "no fitted-GM source equivalence",
            "valid_for_claim": False,
        },
        {
            "audit_id": "KAP2482_4_verdict",
            "object": "e_kappaG zero certificate",
            "attempt": "Close e_kappaG=0.",
            "result": "not closed; kappa/G remains a parent-coupling calibration component of E_norm",
            "status": "ZERO_NOT_PROMOTED",
            "retained_gap": "E_norm.e_kappaG",
            "valid_for_claim": False,
        },
    ]
    return [stamp(row) for row in rows]


def dynamic_worldtube_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "world_id": "DYN2482_0_stationary_control",
            "identity_or_condition": "tau Killing/stationary, ell_J constant, compact support, side flux zero",
            "attempt": "Use the stationary Hilbert branch as local control.",
            "result": "surface-independent Hilbert mass remains a good conditional control branch",
            "status": "PASS_CONDITIONAL_CONTROL",
            "retained_gap": "not full dynamic closure",
            "valid_for_claim": False,
        },
        {
            "world_id": "DYN2482_1_exchange_identity",
            "identity_or_condition": "nabla_mu J_M^mu + I_tau + I_A = 0",
            "attempt": "Derive dynamic source conservation from tau/GK/matter parent equations.",
            "result": "required identity is known but not owned by a parent action/stress theorem",
            "status": "BLOCKED_PARENT_EXCHANGE",
            "retained_gap": "e_clock_exchange",
            "valid_for_claim": False,
        },
        {
            "world_id": "DYN2482_2_total_stress_route",
            "identity_or_condition": "nabla_mu(T_matter^{mu nu}+T_GK^{mu nu}+T_tau^{mu nu})=0",
            "attempt": "Use diffeomorphism/Noether identity of total parent action.",
            "result": "route is viable in principle but needs full parent stress tensor, including GK and tau sectors",
            "status": "PARENT_STRESS_REQUIRED",
            "retained_gap": "e_clock_exchange;e_hilbert_shadow",
            "valid_for_claim": False,
        },
        {
            "world_id": "DYN2482_3_jump_support",
            "identity_or_condition": "distributional jump conditions at worldtube boundary plus compact-support/falloff theorem",
            "attempt": "Prevent hidden source leakage through the worldtube boundary.",
            "result": "not derived; stationary theorem assumes it, dynamic closure needs it",
            "status": "BLOCKED_JUMP_SUPPORT",
            "retained_gap": "e_jump_support;e_surface_drift",
            "valid_for_claim": False,
        },
        {
            "world_id": "DYN2482_4_verdict",
            "identity_or_condition": "dynamic worldtube surface independence",
            "attempt": "Close dynamic source drift.",
            "result": "not closed; dynamic surface drift remains in E_norm",
            "status": "ZERO_NOT_PROMOTED",
            "retained_gap": "E_norm dynamic components",
            "valid_for_claim": False,
        },
    ]
    return [stamp(row) for row in rows]


def enorm_component_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "component_id": "EN2482_0_e_kappaG",
            "component": "e_kappaG",
            "definition": "parent coupling calibration gap between kappa0 and measured G_ref",
            "status": "RETAIN",
            "zero_condition": "MTS parent action derives EH-leading coefficient and G_ref is only a later measurement",
            "next_action": "derive parent EH/coupling normalization or keep component in local residual budget",
            "valid_for_claim": False,
        },
        {
            "component_id": "EN2482_1_e_surface_drift",
            "component": "e_surface_drift",
            "definition": "worldtube source-charge drift between hypersurfaces",
            "status": "RETAIN",
            "zero_condition": "dynamic Gauss law closes with no side flux",
            "next_action": "derive dynamic worldtube side-flux cancellation or bound it",
            "valid_for_claim": False,
        },
        {
            "component_id": "EN2482_2_e_clock_exchange",
            "component": "e_clock_exchange",
            "definition": "clock/tau strain exchange needed for nabla.J_M conservation",
            "status": "RETAIN",
            "zero_condition": "parent tau/GK/matter equations produce I_tau+I_A=-nabla.J_M",
            "next_action": "derive tau exchange current from parent clock/coframe sector",
            "valid_for_claim": False,
        },
        {
            "component_id": "EN2482_3_e_jump_support",
            "component": "e_jump_support",
            "definition": "distributional worldtube jump/support leakage",
            "status": "RETAIN",
            "zero_condition": "source support theorem and jump conditions include all boundary layers",
            "next_action": "write worldtube distributional conservation ledger",
            "valid_for_claim": False,
        },
        {
            "component_id": "EN2482_4_e_hilbert_shadow",
            "component": "e_hilbert_shadow",
            "definition": "difference between Hilbert stress source and any non-Hilbert/source-shadow coupling",
            "status": "RETAIN",
            "zero_condition": "matter coupling descent proves no independent source-shadow survives",
            "next_action": "return to source-shadow/universal matter coupling after parent stress route",
            "valid_for_claim": False,
        },
        {
            "component_id": "EN2482_5_stationary_control",
            "component": "E_norm_stationary_control",
            "definition": "zero source-normalization gap under stationary compact-source hypotheses and declared kappa/G relation",
            "status": "CONTROL_ONLY",
            "zero_condition": "valid only inside stationary local theorem branch, not full dynamic theory",
            "next_action": "use as benchmark, not as claim",
            "valid_for_claim": False,
        },
    ]
    return [stamp(row) for row in rows]


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "gate_id": "GATE2482_0_kappa_relation",
            "claim": "kappa0=8*pi*G_ref/c^4 is written as conditional candidate relation.",
            "gate_status": "PASS_CONDITIONAL_NONCLAIM",
            "reason": "2404/2481 provide the weak-field relation inside the candidate branch.",
            "gate_pass": True,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE2482_1_parent_kappa",
            "claim": "kappa0/G_ref is parent-derived.",
            "gate_status": "BLOCKED",
            "reason": "MTS-to-EH leading operator/coupling theorem is not signed.",
            "gate_pass": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE2482_2_dynamic_worldtube",
            "claim": "dynamic worldtube source charge is surface-independent.",
            "gate_status": "BLOCKED",
            "reason": "exchange current, total stress route and jump/support theorem are missing.",
            "gate_pass": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE2482_3_Enorm_zero",
            "claim": "E_norm vanishes in the full theory.",
            "gate_status": "BLOCKED",
            "reason": "e_kappaG and dynamic worldtube components remain retained.",
            "gate_pass": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE2482_4_Newton_GR",
            "claim": "Newton/local-GR limit is derived.",
            "gate_status": "BLOCKED",
            "reason": "source-normalization full closure and residual-sector silence are still open.",
            "gate_pass": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE2482_5_no_shortcuts",
            "claim": "No GR shortcut, fitted GM, M_H_ref reuse, or plateau axiom is used.",
            "gate_status": "PASS_GUARDRAIL",
            "reason": "orbital-GM calibration and EH-import proof are explicitly rejected.",
            "gate_pass": True,
            "claim_allowed": False,
        },
    ]
    return [stamp(row) for row in rows]


def decision_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "decision_id": "DEC2482_0_kappa_status",
            "decision": "Retain e_kappaG.",
            "reason": "kappa0/G_ref is a consistent candidate normalization but not yet parent-derived.",
            "effect": "Newton source coupling stays nonclaim outside stationary control branch.",
        },
        {
            "decision_id": "DEC2482_1_dynamic_status",
            "decision": "Retain dynamic worldtube components.",
            "reason": "exchange current and jump/support theorem are missing.",
            "effect": "E_norm remains necessary for full theory bookkeeping.",
        },
        {
            "decision_id": "DEC2482_2_next",
            "decision": "Attack parent EH/coupling origin before arena kernels.",
            "reason": "The coupling normalization is upstream of R10/PPN observables.",
            "effect": "2483 selected.",
        },
    ]
    return [stamp(row) for row in rows]


def next_target_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "route_id": "NEXT2482_0_selected",
            "selection_status": "selected",
            "target_file": "2483-Y5-R2FR-parent-EH-coupling-origin-or-coupling-residual-row.md",
            "target_script": "scripts/Y5_R2FR_parent_EH_coupling_origin_or_coupling_residual_row_2483.py",
            "task": "attempt to derive the EH-leading operator and kappa0 coupling from the MTS parent action; if not possible, retain e_kappaG as an explicit coupling residual row",
            "acceptance_target": "parent action normalization audit, EH import rejection, kappa/G residual row, no fitted-GM guardrail, nonclaim validation",
            "guardrails": "no GR shortcut; no fitted GM; no M_H_ref reuse; no plateau axiom; no GitHub",
        }
    ]
    return [stamp(row) for row in rows]


def copy_branch_outputs() -> list[dict[str, Any]]:
    copy_map = {
        "calibration_audit": OUTPUTS["calibration_audit"],
        "enorm_components": OUTPUTS["enorm_components"],
        "acquisition_queue": OUTPUTS["next_target"],
    }
    rows: list[dict[str, Any]] = []
    for key, source in copy_map.items():
        target = COPY_TARGETS[key]
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
        rows.append(
            stamp(
                {
                    "copy_id": f"COPY2482_{key}",
                    "source_path": str(source),
                    "target_path": str(target),
                    "source_exists": source.exists(),
                    "target_exists": target.exists(),
                }
            )
        )
    return rows


def validation_rows(data: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    def add(check_id: str, passed: bool, notes: str, detail: str = "") -> None:
        rows.append(
            stamp(
                {
                    "check_id": check_id,
                    "status": "PASS" if passed else "FAIL",
                    "notes": notes,
                    "detail": detail,
                }
            )
        )

    add("VAL2482_00_sources_exist", all(row["source_pass"] is True for row in data["sources"]), "all cited local source paths exist and needles are present")
    add(
        "VAL2482_01_kappa_blocked",
        any(row["audit_id"] == "KAP2482_4_verdict" and row["status"] == "ZERO_NOT_PROMOTED" for row in data["calibration"]),
        "e_kappaG zero certificate remains blocked",
    )
    add(
        "VAL2482_02_dynamic_blocked",
        any(row["world_id"] == "DYN2482_4_verdict" and row["status"] == "ZERO_NOT_PROMOTED" for row in data["worldtube"]),
        "dynamic worldtube closure remains blocked",
    )
    add(
        "VAL2482_03_Enorm_components_retained",
        all(row["valid_for_claim"] is False for row in data["enorm"]),
        "all E_norm components remain nonclaim",
    )
    add("VAL2482_04_claim_gates_safe", all(row["claim_allowed"] is False for row in data["gates"]), "no gate allows Newton/local-GR/R10 claim")
    add(
        "VAL2482_05_next_target_written",
        any(row["route_id"] == "NEXT2482_0_selected" for row in data["next"]),
        "2483 parent EH/coupling origin target selected",
    )
    add("VAL2482_06_branch_copies", all(row["source_exists"] is True and row["target_exists"] is True for row in data["copies"]), "nonclaim branch copies exist")

    formalization_artifacts = []
    if FORMALIZATION.exists():
        for pattern in ("*2482*", "*P8_Y5_KAPPAG_WORLD_2482*", "*JR2482*"):
            formalization_artifacts.extend(FORMALIZATION.rglob(pattern))
    add("VAL2482_07_no_formalization_artifacts", not formalization_artifacts, "no 2482 artifacts were written to formalization-workbench", ";".join(str(path) for path in formalization_artifacts))

    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        parsed, count, error = csv_parses(path)
        add(f"VAL2482_CSV_{path.stem}", parsed and count > 0, f"CSV parses with {count} rows", error)
    for key, path in COPY_TARGETS.items():
        parsed, count, error = csv_parses(path)
        add(f"VAL2482_COPY_CSV_{key}", parsed and count > 0, f"copy CSV parses with {count} rows", error)

    overall = all(row["status"] == "PASS" for row in rows)
    add(
        "VAL2482_OVERALL",
        overall,
        "2482 keeps kappa/G and dynamic worldtube closure nonclaim, retains E_norm components, and selects parent EH/coupling origin next",
    )
    return rows


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    body = []
    for row in rows:
        values = []
        for column in columns:
            value = str(row.get(column, ""))
            value = value.replace("|", "\\|").replace("\n", " ")
            values.append(value)
        body.append("| " + " | ".join(values) + " |")
    return "\n".join([header, sep, *body])


def write_doc(data: dict[str, list[dict[str, Any]]]) -> None:
    sections = [
        "# 2482 Y5 R2FR KappaG Parent Calibration Or Dynamic Worldtube Closure",
        "",
        "**Status:** no full closure. `kappa0=8*pi*G_ref/c^4` remains a consistent candidate-branch normalization, not a parent-derived MTS theorem. Dynamic worldtube surface independence also remains blocked by missing exchange/jump/support identities.",
        "",
        "**Main result:** the stationary Hilbert/worldtube branch survives as a control lane, but the full source-normalization residual `E_norm` stays alive. The next most upstream target is the EH-leading operator and coupling origin: if MTS can derive the EH coefficient, `e_kappaG` can shrink; if not, it must remain an explicit coupling residual.",
        "",
        "## Source Register",
        markdown_table(data["sources"], ["source_id", "source_path", "exists", "missing_needles", "source_pass", "role"]),
        "",
        "## Kappa/G Calibration Audit",
        markdown_table(data["calibration"], ["audit_id", "object", "attempt", "result", "status", "retained_gap", "valid_for_claim"]),
        "",
        "## Dynamic Worldtube Audit",
        markdown_table(data["worldtube"], ["world_id", "identity_or_condition", "attempt", "result", "status", "retained_gap", "valid_for_claim"]),
        "",
        "## E_norm Components",
        markdown_table(data["enorm"], ["component_id", "component", "definition", "status", "zero_condition", "next_action", "valid_for_claim"]),
        "",
        "## Claim Gates",
        markdown_table(data["gates"], ["gate_id", "claim", "gate_status", "reason", "gate_pass", "claim_allowed"]),
        "",
        "## Decision Ledger",
        markdown_table(data["decisions"], ["decision_id", "decision", "reason", "effect"]),
        "",
        "## Next Target",
        markdown_table(data["next"], ["route_id", "selection_status", "target_file", "target_script", "task", "acceptance_target", "guardrails"]),
        "",
        "## Branch Copies",
        markdown_table(data["copies"], ["copy_id", "source_path", "target_path", "source_exists", "target_exists"]),
        "",
        "## Validation",
        markdown_table(data["validations"], ["check_id", "status", "notes", "detail"]),
        "",
    ]
    DOC.write_text("\n".join(sections), encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    LOCAL_BOUNDS.mkdir(parents=True, exist_ok=True)
    QUEUE.mkdir(parents=True, exist_ok=True)
    data = {
        "sources": source_register_rows(),
        "calibration": calibration_audit_rows(),
        "worldtube": dynamic_worldtube_rows(),
        "enorm": enorm_component_rows(),
        "gates": claim_gate_rows(),
        "decisions": decision_rows(),
        "next": next_target_rows(),
    }
    write_csv(OUTPUTS["source_register"], data["sources"])
    write_csv(OUTPUTS["calibration_audit"], data["calibration"])
    write_csv(OUTPUTS["dynamic_worldtube"], data["worldtube"])
    write_csv(OUTPUTS["enorm_components"], data["enorm"])
    write_csv(OUTPUTS["claim_gates"], data["gates"])
    write_csv(OUTPUTS["decision_ledger"], data["decisions"])
    write_csv(OUTPUTS["next_target"], data["next"])
    data["copies"] = copy_branch_outputs()
    write_csv(OUTPUTS["branch_copies"], data["copies"])
    data["validations"] = validation_rows(data)
    write_csv(OUTPUTS["validation"], data["validations"])
    write_doc(data)
    print(f"wrote {DOC}")
    for key, path in OUTPUTS.items():
        print(f"wrote {key}: {path}")
    for key, path in COPY_TARGETS.items():
        print(f"copied {key}: {path}")


if __name__ == "__main__":
    main()
