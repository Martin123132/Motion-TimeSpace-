from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


BRANCH_ID = "MTS_R2FR_PARENT_EH_COUPLING_ORIGIN_2483"
CHECKPOINT_ID = "2483"

ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = ROOT.parent
FORMALIZATION = PROJECT_ROOT / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"

DOC = ROOT / "2483-Y5-R2FR-parent-EH-coupling-origin-or-coupling-residual-row.md"

OUTPUTS = {
    "source_register": OUT / "P8_Y5_EH_COUPLING_2483_SOURCE_REGISTER.csv",
    "origin_audit": OUT / "P8_Y5_EH_COUPLING_2483_ORIGIN_AUDIT.csv",
    "coupling_residual": OUT / "P8_Y5_EH_COUPLING_2483_COUPLING_RESIDUAL_ROW.csv",
    "route_matrix": OUT / "P8_Y5_EH_COUPLING_2483_ROUTE_MATRIX.csv",
    "claim_gates": OUT / "P8_Y5_EH_COUPLING_2483_CLAIM_GATES.csv",
    "decision_ledger": OUT / "P8_Y5_EH_COUPLING_2483_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_EH_COUPLING_2483_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_EH_COUPLING_2483_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2483_VALIDATION.csv",
}

COPY_TARGETS = {
    "origin_audit": LOCAL_BOUNDS / "Parent_EH_coupling_origin_audit_2483_NONCLAIM.csv",
    "coupling_residual": LOCAL_BOUNDS / "KappaG_coupling_residual_row_2483_NONCLAIM.csv",
    "acquisition_queue": QUEUE / "JR2483_PARENT_ACTION_NORMALIZATION_OWNER_OR_COUPLING_RESIDUAL.csv",
}

SOURCES = [
    {
        "source_id": "SRC2483_00_2482_doc",
        "source_path": ROOT / "2482-Y5-R2FR-kappaG-parent-calibration-or-dynamic-worldtube-closure.md",
        "needles": ["NEXT2482_0_selected", "e_kappaG", "VAL2482_OVERALL"],
        "role": "handoff selecting parent EH/coupling origin",
    },
    {
        "source_id": "SRC2483_01_2404_first_variation",
        "source_path": ROOT / "2404-Y5-R2FR-minimal-parent-action-first-variation-GR-Newton-gate-or-operator-residual-pack.md",
        "needles": ["S_min=S_EH", "CANDIDATE_NOT_DERIVED", "REF2404_1_EH_import"],
        "role": "candidate EH first variation and EH-import rejection",
    },
    {
        "source_id": "SRC2483_02_2405_EH_dominance",
        "source_path": ROOT / "2405-Y5-R2FR-EH-dominance-and-MTS-residual-sector-silence-or-operator-bound-pack.md",
        "needles": ["EHD2405_0_target", "EHD2405_4_current_verdict", "REF2405_0_EH_by_notation"],
        "role": "EH dominance and residual-silence blocker",
    },
    {
        "source_id": "SRC2483_03_2406_sector_residuals",
        "source_path": ROOT / "2406-Y5-R2FR-sector-by-sector-MTS-residual-variation-and-local-scaling-silence-or-operator-bounds.md",
        "needles": ["SVC2406_6_verdict", "CG2406_0_EH_dominance", "VAL2406_03_no_sector_zero_claimed"],
        "role": "residual-sector scoreboard showing EH dominance not proved",
    },
    {
        "source_id": "SRC2483_04_2477_metric_response",
        "source_path": ROOT / "2477-Y5-R2FR-parent-weak-field-metric-response-theorem-or-no-go.md",
        "needles": ["BLK2477_0_EH_origin", "THM2477_0_parent_candidate_equation", "GATE2477_3_local_GR"],
        "role": "weak-field metric response and EH-origin blocker",
    },
    {
        "source_id": "SRC2483_05_2482_validation",
        "source_path": OUT / "P8_Y5_BRR545_2482_VALIDATION.csv",
        "needles": ["VAL2482_OVERALL", "PASS"],
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


def origin_audit_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "audit_id": "EH2483_0_standard_variation",
            "object": "standard EH variation",
            "statement": "delta S_EH gives Einstein operator with coefficient kappa0 in the candidate branch",
            "current_result": "mathematically standard and usable as a conditional template",
            "status": "PASS_TEMPLATE",
            "missing_for_claim": "does not prove MTS parent action generates S_EH",
            "valid_for_claim": False,
        },
        {
            "audit_id": "EH2483_1_candidate_inclusion",
            "object": "S_min contains S_EH[e]",
            "statement": "private candidate action includes an EH term plus silent/residual sectors",
            "current_result": "first variation bridge is exact if candidate is accepted",
            "status": "PASS_CANDIDATE_NONCLAIM",
            "missing_for_claim": "candidate clauses are not derived from deeper MTS primitives",
            "valid_for_claim": False,
        },
        {
            "audit_id": "EH2483_2_parent_origin",
            "object": "MTS-to-EH leading operator theorem",
            "statement": "derive the unique local second-order diffeomorphism-invariant leading metric/coframe operator from MTS parent variables",
            "current_result": "not present in current corpus",
            "status": "BLOCKED_PARENT_ORIGIN",
            "missing_for_claim": "field list, symmetry principle, derivative-order grammar, coefficient owner, boundary convention",
            "valid_for_claim": False,
        },
        {
            "audit_id": "EH2483_3_coupling_owner",
            "object": "kappa0 coefficient owner",
            "statement": "derive or declare the coefficient multiplying the EH-leading term before empirical local tests",
            "current_result": "kappa0=8*pi*G_ref/c^4 is a conditional relation, not an MTS derivation",
            "status": "BLOCKED_COUPLING_OWNER",
            "missing_for_claim": "parent normalization constant or primitive scale/coupling source",
            "valid_for_claim": False,
        },
        {
            "audit_id": "EH2483_4_residual_dominance",
            "object": "EH dominance over DeltaE_MTS",
            "statement": "prove non-EH residual sectors vanish/silent/bounded below local thresholds",
            "current_result": "2405/2406 show finite residual owners remain live",
            "status": "BLOCKED_RESIDUAL_SILENCE",
            "missing_for_claim": "sector zero certificates or source-backed operator bounds",
            "valid_for_claim": False,
        },
        {
            "audit_id": "EH2483_5_no_import",
            "object": "EH import as proof",
            "statement": "do not use the fact GR works locally as proof that MTS derives GR",
            "current_result": "guardrail active",
            "status": "PASS_GUARDRAIL",
            "missing_for_claim": "derive, do not borrow",
            "valid_for_claim": False,
        },
    ]
    return [stamp(row) for row in rows]


def coupling_residual_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "residual_id": "KRES2483_0_e_kappaG",
            "symbol": "e_kappaG",
            "definition": "dimensionless parent-coupling residual between candidate kappa0 and the coupling that would be measured as G_ref",
            "formal_row": "e_kappaG := |kappa_MTS - kappa_ref|/kappa_ref or symbolic KAPPA_OWNER_MISSING when kappa_MTS is not parent-derived",
            "status": "RETAIN_NONCLAIM",
            "zero_condition": "parent action derives EH-leading coefficient kappa_MTS and G_ref is treated only as later measurement",
            "valid_for_claim": False,
        },
        {
            "residual_id": "KRES2483_1_kappa_MTS",
            "symbol": "kappa_MTS",
            "definition": "coefficient of the parent-derived EH-leading operator",
            "formal_row": "S_parent -> (1/(2*kappa_MTS))*int sqrt(-g) R + residual sectors",
            "status": "MISSING_PARENT_COEFFICIENT",
            "zero_condition": "MTS parent action normal form supplies this coefficient before tests",
            "valid_for_claim": False,
        },
        {
            "residual_id": "KRES2483_2_G_parent",
            "symbol": "G_parent",
            "definition": "G_parent:=kappa_MTS*c^4/(8*pi) once kappa_MTS exists",
            "formal_row": "definition allowed only after kappa_MTS is parent-owned",
            "status": "DOWNSTREAM_DEFINITION_ONLY",
            "zero_condition": "G_ref measures G_parent, not vice versa",
            "valid_for_claim": False,
        },
        {
            "residual_id": "KRES2483_3_EH_import_residual",
            "symbol": "e_EH_import",
            "definition": "logic residual incurred if EH is inserted as a template instead of derived from MTS primitives",
            "formal_row": "e_EH_import=0 only if parent-origin theorem closes",
            "status": "RETAIN_LOGIC_GUARDRAIL",
            "zero_condition": "MTS-to-EH leading-operator theorem with field/symmetry/derivative grammar",
            "valid_for_claim": False,
        },
    ]
    return [stamp(row) for row in rows]


def route_matrix_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "route_id": "ROUTE2483_A_lovelock_like",
            "route": "symmetry/derivative-order uniqueness",
            "attempt": "show local branch has diffeomorphism invariance, metric/coframe field, second-order equations, no extra local tensors, then EH is unique up to Lambda/boundary",
            "strength": "least arbitrary if MTS can supply hypotheses",
            "current_status": "HYPOTHESES_UNSIGNED",
            "next_input": "field list, derivative-order ban, residual-sector zero certificates",
            "valid_for_claim": False,
        },
        {
            "route_id": "ROUTE2483_B_integrate_out",
            "route": "integrate out MTS auxiliaries",
            "attempt": "start from parent MTS variables, eliminate auxiliary/projector/q/tau sectors, recover EH leading term plus controlled residuals",
            "strength": "most genuinely MTS-derived",
            "current_status": "PARENT_ACTION_NOT_COMPLETE",
            "next_input": "explicit parent action normal form and Hessian/constraint ownership",
            "valid_for_claim": False,
        },
        {
            "route_id": "ROUTE2483_C_effective_field_theory",
            "route": "EFT leading operator",
            "attempt": "treat EH as the leading low-energy operator and keep all non-EH terms as residual coefficients",
            "strength": "honest effective-theory route, less fundamental",
            "current_status": "AVAILABLE_AS_EFFECTIVE_NONCLAIM",
            "next_input": "bounds/priors for residual coefficients and parent reason for leading-order hierarchy",
            "valid_for_claim": False,
        },
        {
            "route_id": "ROUTE2483_D_import_GR",
            "route": "import GR because it works",
            "attempt": "use standard GR local success as proof of MTS local reduction",
            "strength": "invalid shortcut",
            "current_status": "REJECTED",
            "next_input": "none; forbidden route",
            "valid_for_claim": False,
        },
    ]
    return [stamp(row) for row in rows]


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "gate_id": "GATE2483_0_EH_template",
            "claim": "Standard EH variation is available as a conditional template.",
            "gate_status": "PASS_CONDITIONAL_NONCLAIM",
            "reason": "2404 already exposes the candidate field equation.",
            "gate_pass": True,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE2483_1_parent_EH",
            "claim": "MTS parent action derives the EH-leading operator.",
            "gate_status": "BLOCKED",
            "reason": "field/symmetry/derivative grammar and coefficient owner are unsigned.",
            "gate_pass": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE2483_2_kappa",
            "claim": "kappa0/G_ref is parent-derived.",
            "gate_status": "BLOCKED",
            "reason": "kappa_MTS is not parent-owned; G_ref cannot be used as proof input.",
            "gate_pass": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE2483_3_EH_dominance",
            "claim": "EH dominates all MTS residual sectors locally.",
            "gate_status": "BLOCKED",
            "reason": "DeltaE_MTS sector owners remain live from 2405/2406.",
            "gate_pass": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE2483_4_Newton_GR",
            "claim": "Newton/local-GR limit is derived.",
            "gate_status": "BLOCKED",
            "reason": "parent EH origin, coupling, residual silence and source normalization remain open.",
            "gate_pass": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE2483_5_no_shortcuts",
            "claim": "No GR shortcut, fitted GM, M_H_ref reuse, or plateau axiom is used.",
            "gate_status": "PASS_GUARDRAIL",
            "reason": "EH import and orbital-GM laundering are explicitly rejected.",
            "gate_pass": True,
            "claim_allowed": False,
        },
    ]
    return [stamp(row) for row in rows]


def decision_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "decision_id": "DEC2483_0_status",
            "decision": "Retain e_kappaG and e_EH_import.",
            "reason": "EH/coupling are conditional candidate ingredients, not parent-derived theorem outputs.",
            "effect": "local-GR/Newton remains blocked but sharply localized.",
        },
        {
            "decision_id": "DEC2483_1_best_route",
            "decision": "Prefer Lovelock-like hypotheses plus parent-action normal-form ownership next.",
            "reason": "This is the least hand-wavy way to derive EH without simply importing GR.",
            "effect": "2484 should audit the exact hypotheses needed for EH uniqueness/origin.",
        },
        {
            "decision_id": "DEC2483_2_effective_backup",
            "decision": "Keep EFT-leading-operator route as fallback only.",
            "reason": "It may be publishable as an effective framework, but it is weaker than deriving GR from MTS primitives.",
            "effect": "do not overclaim fundamental derivation.",
        },
    ]
    return [stamp(row) for row in rows]


def next_target_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "route_id": "NEXT2483_0_selected",
            "selection_status": "selected",
            "target_file": "2484-Y5-R2FR-EH-uniqueness-hypotheses-or-parent-normal-form-blocker.md",
            "target_script": "scripts/Y5_R2FR_EH_uniqueness_hypotheses_or_parent_normal_form_blocker_2484.py",
            "task": "audit whether MTS can supply the hypotheses needed for EH-leading uniqueness: local diffeomorphism invariance, metric/coframe field, second-order field equations, no extra local tensors, boundary class, and coefficient owner",
            "acceptance_target": "hypothesis table, pass/fail per clause, retained e_EH_import/e_kappaG if any clause unsigned, no local-GR claim",
            "guardrails": "no GR shortcut; no fitted GM; no M_H_ref reuse; no plateau axiom; no GitHub",
        }
    ]
    return [stamp(row) for row in rows]


def copy_branch_outputs() -> list[dict[str, Any]]:
    copy_map = {
        "origin_audit": OUTPUTS["origin_audit"],
        "coupling_residual": OUTPUTS["coupling_residual"],
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
                    "copy_id": f"COPY2483_{key}",
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

    add("VAL2483_00_sources_exist", all(row["source_pass"] is True for row in data["sources"]), "all cited local source paths exist and needles are present")
    add(
        "VAL2483_01_parent_EH_blocked",
        any(row["audit_id"] == "EH2483_2_parent_origin" and row["status"] == "BLOCKED_PARENT_ORIGIN" for row in data["audit"]),
        "parent EH-origin theorem remains blocked",
    )
    add(
        "VAL2483_02_kappa_residual_retained",
        any(row["symbol"] == "e_kappaG" and row["status"] == "RETAIN_NONCLAIM" for row in data["residuals"]),
        "e_kappaG residual row is retained",
    )
    add(
        "VAL2483_03_invalid_import_rejected",
        any(row["route_id"] == "ROUTE2483_D_import_GR" and row["current_status"] == "REJECTED" for row in data["routes"]),
        "GR import route is rejected",
    )
    add("VAL2483_04_claim_gates_safe", all(row["claim_allowed"] is False for row in data["gates"]), "no gate allows Newton/local-GR/R10 claim")
    add(
        "VAL2483_05_next_target_written",
        any(row["route_id"] == "NEXT2483_0_selected" for row in data["next"]),
        "2484 EH uniqueness/normal-form target selected",
    )
    add("VAL2483_06_branch_copies", all(row["source_exists"] is True and row["target_exists"] is True for row in data["copies"]), "nonclaim branch copies exist")

    formalization_artifacts = []
    if FORMALIZATION.exists():
        for pattern in ("*2483*", "*P8_Y5_EH_COUPLING_2483*", "*JR2483*"):
            formalization_artifacts.extend(FORMALIZATION.rglob(pattern))
    add("VAL2483_07_no_formalization_artifacts", not formalization_artifacts, "no 2483 artifacts were written to formalization-workbench", ";".join(str(path) for path in formalization_artifacts))

    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        parsed, count, error = csv_parses(path)
        add(f"VAL2483_CSV_{path.stem}", parsed and count > 0, f"CSV parses with {count} rows", error)
    for key, path in COPY_TARGETS.items():
        parsed, count, error = csv_parses(path)
        add(f"VAL2483_COPY_CSV_{key}", parsed and count > 0, f"copy CSV parses with {count} rows", error)

    overall = all(row["status"] == "PASS" for row in rows)
    add(
        "VAL2483_OVERALL",
        overall,
        "2483 keeps EH/coupling as conditional candidate structure, retains e_kappaG/e_EH_import, rejects GR import, and selects EH uniqueness hypotheses next",
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
        "# 2483 Y5 R2FR Parent EH Coupling Origin Or Coupling Residual Row",
        "",
        "**Status:** EH/coupling origin is not derived yet. The standard EH variation and candidate first-variation bridge are valid conditional mathematics, but they do not prove that MTS itself generates the EH-leading operator or owns `kappa0`.",
        "",
        "**Main result:** separate the three layers: standard EH template, candidate EH inclusion, and parent-derived EH origin. The first two exist; the third is still blocked. Therefore `e_kappaG` and `e_EH_import` remain explicit nonclaim residuals until MTS supplies EH uniqueness/normal-form hypotheses and a coefficient owner.",
        "",
        "## Source Register",
        markdown_table(data["sources"], ["source_id", "source_path", "exists", "missing_needles", "source_pass", "role"]),
        "",
        "## Origin Audit",
        markdown_table(data["audit"], ["audit_id", "object", "statement", "current_result", "status", "missing_for_claim", "valid_for_claim"]),
        "",
        "## Coupling Residual Rows",
        markdown_table(data["residuals"], ["residual_id", "symbol", "definition", "formal_row", "status", "zero_condition", "valid_for_claim"]),
        "",
        "## Route Matrix",
        markdown_table(data["routes"], ["route_id", "route", "attempt", "strength", "current_status", "next_input", "valid_for_claim"]),
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
        "audit": origin_audit_rows(),
        "residuals": coupling_residual_rows(),
        "routes": route_matrix_rows(),
        "gates": claim_gate_rows(),
        "decisions": decision_rows(),
        "next": next_target_rows(),
    }
    write_csv(OUTPUTS["source_register"], data["sources"])
    write_csv(OUTPUTS["origin_audit"], data["audit"])
    write_csv(OUTPUTS["coupling_residual"], data["residuals"])
    write_csv(OUTPUTS["route_matrix"], data["routes"])
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
