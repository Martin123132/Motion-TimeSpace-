from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


BRANCH_ID = "MTS_R2FR_NON_EGK_RESIDUAL_ZERO_CERTIFICATES_2480"
CHECKPOINT_ID = "2480"

ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = ROOT.parent
FORMALIZATION = PROJECT_ROOT / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"

DOC = ROOT / "2480-Y5-R2FR-non-EGK-residual-zero-certificates-or-extended-norm-vector.md"

OUTPUTS = {
    "source_register": OUT / "P8_Y5_NON_EGK_ZERO_2480_SOURCE_REGISTER.csv",
    "zero_certificate": OUT / "P8_Y5_NON_EGK_ZERO_2480_ZERO_CERTIFICATE_ATTEMPT.csv",
    "extended_norm": OUT / "P8_Y5_NON_EGK_ZERO_2480_EXTENDED_NORM_VECTOR.csv",
    "slot_decision": OUT / "P8_Y5_NON_EGK_ZERO_2480_SLOT_DECISION_LEDGER.csv",
    "claim_gates": OUT / "P8_Y5_NON_EGK_ZERO_2480_CLAIM_GATES.csv",
    "decision_ledger": OUT / "P8_Y5_NON_EGK_ZERO_2480_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_NON_EGK_ZERO_2480_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_NON_EGK_ZERO_2480_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2480_VALIDATION.csv",
}

COPY_TARGETS = {
    "zero_certificate": LOCAL_BOUNDS / "Non_EGK_zero_certificate_attempt_2480_NONCLAIM.csv",
    "extended_norm": LOCAL_BOUNDS / "Extended_local_residual_norm_vector_2480_NONCLAIM.csv",
    "acquisition_queue": QUEUE / "JR2480_SOURCE_NORMALIZATION_ZERO_CERTIFICATE_OR_ENORM_ROW.csv",
}

SOURCES = [
    {
        "source_id": "SRC2480_00_2479_doc",
        "source_path": ROOT / "2479-Y5-R2FR-residual-sector-to-EGK-norm-map-or-coefficient-blocker.md",
        "needles": ["NEXT2479_0_selected", "e_HD,e_aux,e_tau,e_qspur,e_shadow,e_norm,e_bg", "VAL2479_OVERALL"],
        "role": "handoff selecting non-EGK zero certificates or extended norm",
    },
    {
        "source_id": "SRC2480_01_2405_shortcuts",
        "source_path": ROOT / "2405-Y5-R2FR-EH-dominance-and-MTS-residual-sector-silence-or-operator-bound-pack.md",
        "needles": ["constraint equation C=0", "DeltaE_MTS", "REF2405_2_conservation_as_zero"],
        "role": "zero-stress shortcut rejection and residual-sector basis",
    },
    {
        "source_id": "SRC2480_02_2406_sector_audit",
        "source_path": ROOT / "2406-Y5-R2FR-sector-by-sector-MTS-residual-variation-and-local-scaling-silence-or-operator-bounds.md",
        "needles": ["SVC2406_0_higher_derivative", "SVC2406_6_verdict", "VAL2406_03_no_sector_zero_claimed"],
        "role": "sector zero/silence status and exact obstructions",
    },
    {
        "source_id": "SRC2480_03_2466_source_norm",
        "source_path": ROOT / "2466-Y5-R2FR-matter-current-descent-and-worldtube-source-bridge.md",
        "needles": ["MISSING_PARENT_SCALE", "WT2466_2_surface_independence", "Do not define M_source by observed GM"],
        "role": "source normalization, worldtube bridge and no fitted-GM guardrail",
    },
    {
        "source_id": "SRC2480_04_2473_EGK",
        "source_path": ROOT / "2473-Y5-R2FR-GK-stress-bound-local-arena-projection-runner.md",
        "needles": ["E_GK_bound", "projector_leak", "MISSING_COEFFICIENTS"],
        "role": "current EGK basis and local runner block rule",
    },
    {
        "source_id": "SRC2480_05_2479_validation",
        "source_path": OUT / "P8_Y5_BRR545_2479_VALIDATION.csv",
        "needles": ["VAL2479_OVERALL", "PASS"],
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
    except Exception as exc:  # pragma: no cover - diagnostic path
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


def zero_certificate_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "slot_id": "ZERO2480_e_HD",
            "slot": "e_HD_curvature_operator",
            "zero_route": "parent action normal form excludes higher-derivative curvature operators, or makes retained curvature term topological in four dimensions",
            "attempt_result": "NOT_ZEROED_CURRENT_CORPUS",
            "reason": "2406 records the higher-derivative template as known but parent adoption/exclusion is unsigned.",
            "retain_or_zero": "RETAIN",
            "extended_norm_slot": "E_HD",
            "valid_for_claim": False,
        },
        {
            "slot_id": "ZERO2480_e_aux",
            "slot": "e_aux_constraint_stress",
            "zero_route": "first-class zero-boundary generator or second-class algebraic elimination with zero metric stress",
            "attempt_result": "ZERO_SHORTCUT_REJECTED",
            "reason": "C=0 does not imply zero metric stress; multiplier and auxiliary-elimination tails can survive.",
            "retain_or_zero": "RETAIN",
            "extended_norm_slot": "E_aux",
            "valid_for_claim": False,
        },
        {
            "slot_id": "ZERO2480_e_tau",
            "slot": "e_tau_clock_frame_leak",
            "zero_route": "terminal public coframe, current-chain vertical silence, and clock-compatible tau make memory/frame residual vanish",
            "attempt_result": "CONDITIONAL_NOT_SIGNED",
            "reason": "The current-chain/tau identity remains conditional and not a parent zero theorem.",
            "retain_or_zero": "RETAIN",
            "extended_norm_slot": "E_tau",
            "valid_for_claim": False,
        },
        {
            "slot_id": "ZERO2480_e_qspur",
            "slot": "e_q_weyl_spurion",
            "zero_route": "q is first-class/removed, has no Weyl/Ricci spurion, and exterior q charges vanish",
            "attempt_result": "NOT_ZEROED_WEYL_TAIL_DANGER",
            "reason": "2406 keeps q first-class/no-spurion status unsigned.",
            "retain_or_zero": "RETAIN",
            "extended_norm_slot": "E_qspur",
            "valid_for_claim": False,
        },
        {
            "slot_id": "ZERO2480_e_shadow",
            "slot": "e_species_shadow_or_zero",
            "zero_route": "universal Hilbert coupling makes non-Hilbert/source-shadow and species-dependent current exactly vanish",
            "attempt_result": "PROMISING_BUT_UNSIGNED",
            "reason": "Hilbert branch is preferred for WEP, but A/matter/source-shadow unification is not proved.",
            "retain_or_zero": "RETAIN",
            "extended_norm_slot": "E_shadow",
            "valid_for_claim": False,
        },
        {
            "slot_id": "ZERO2480_e_norm",
            "slot": "e_source_norm_gap",
            "zero_route": "ell_J, kappa0/G_ref and worldtube Hilbert charge define the same source before orbital fitting",
            "attempt_result": "CORE_BLOCKER",
            "reason": "parent scale ell_J and worldtube surface independence are missing; fitted GM is forbidden.",
            "retain_or_zero": "RETAIN",
            "extended_norm_slot": "E_norm",
            "valid_for_claim": False,
        },
        {
            "slot_id": "ZERO2480_e_bg",
            "slot": "e_background_subtraction",
            "zero_route": "choose local reference/background solution satisfying the Lambda/background field equation, then solve only perturbations around it",
            "attempt_result": "CONDITIONAL_ZERO_IF_REFERENCE_DECLARED",
            "reason": "This is mathematically clean, but the local reference/background subtraction convention must be explicitly declared.",
            "retain_or_zero": "CONDITIONAL_ZERO_OR_RETAIN",
            "extended_norm_slot": "E_bg",
            "valid_for_claim": False,
        },
    ]
    return [stamp(row) for row in rows]


def extended_norm_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "norm_id": "ENORM2480_0_current_EGK",
            "norm_symbol": "E_GK_bound",
            "definition": "C_B*boundary_flux + C_S*source_tail + C_X*negative_mode_defect + C_H*topology_hair_amplitude + C_P*projector_leak",
            "role": "existing GK stress-bound basis",
            "status": "RETAIN_BASE_NONCLAIM",
            "valid_for_claim": False,
        },
        {
            "norm_id": "ENORM2480_1_extended",
            "norm_symbol": "E_local_res",
            "definition": "E_GK_bound + E_HD + E_aux + E_tau + E_qspur + E_shadow + E_norm + E_bg",
            "role": "minimal honest norm vector after failed zero-certificate sweep",
            "status": "PROPOSED_EXTENDED_NORM_NONCLAIM",
            "valid_for_claim": False,
        },
        {
            "norm_id": "ENORM2480_2_Cres_ext",
            "norm_symbol": "C_res_ext",
            "definition": "||S_res|| <= C_res_ext*E_local_res",
            "role": "replacement for invalid C_res*E_GK_bound full-source claim",
            "status": "FORMAL_ONLY_UNTIL_SLOT_COEFFICIENTS_SOURCED",
            "valid_for_claim": False,
        },
        {
            "norm_id": "ENORM2480_3_Cmetric_ext",
            "norm_symbol": "C_metric_ext",
            "definition": "C_metric_ext=(2/c^2)*C_obs*C_Green*C_res_ext",
            "role": "future local-test bridge if every norm slot is zeroed or sourced",
            "status": "DOWNSTREAM_NONCLAIM",
            "valid_for_claim": False,
        },
    ]
    return [stamp(row) for row in rows]


def slot_decision_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "decision_id": "SDEC2480_0_all_zero_test",
            "question": "Can all non-EGK slots be zeroed now?",
            "answer": "NO",
            "evidence": "six retained slots plus one conditional-background slot remain unsigned",
            "effect": "local-GR/Newton proof remains blocked",
            "valid_for_claim": False,
        },
        {
            "decision_id": "SDEC2480_1_background",
            "question": "Can e_bg be treated differently?",
            "answer": "YES_CONDITIONALLY",
            "evidence": "background/Lambda can be subtracted by solving perturbations around a declared local reference solution",
            "effect": "write explicit background-reference certificate later; do not count as a local-GR pass",
            "valid_for_claim": False,
        },
        {
            "decision_id": "SDEC2480_2_priority",
            "question": "Which retained slot should be attacked next?",
            "answer": "e_source_norm_gap",
            "evidence": "source normalization is central to Newton reduction and cannot be hidden inside GK stress",
            "effect": "2481 should target Hilbert/worldtube source normalization before arena kernels",
            "valid_for_claim": False,
        },
    ]
    return [stamp(row) for row in rows]


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "gate_id": "GATE2480_0_zero_sweep_done",
            "claim": "All non-EGK residual slots were audited for zero certificates.",
            "gate_status": "PASS_STRUCTURE_NONCLAIM",
            "reason": "e_HD,e_aux,e_tau,e_qspur,e_shadow,e_norm,e_bg each has a zero/retain decision.",
            "gate_pass": True,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE2480_1_all_zero",
            "claim": "All non-EGK slots are zero.",
            "gate_status": "BLOCKED",
            "reason": "No retained slot has a parent-signed zero theorem.",
            "gate_pass": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE2480_2_extended_norm",
            "claim": "Extended E_local_res norm is source-backed.",
            "gate_status": "BLOCKED",
            "reason": "The norm vector is formally defined but all new slot coefficients remain unsourced.",
            "gate_pass": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE2480_3_source_norm",
            "claim": "Source normalization gap is closed.",
            "gate_status": "BLOCKED",
            "reason": "ell_J/worldtube surface independence and no-fitted-GM source equivalence remain open.",
            "gate_pass": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE2480_4_Newton_GR",
            "claim": "Newton/local-GR limit is derived.",
            "gate_status": "BLOCKED",
            "reason": "Residual slots are retained and C_res_ext is formal only.",
            "gate_pass": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE2480_5_R10",
            "claim": "R10/PPN local-test predictions can run.",
            "gate_status": "BLOCKED",
            "reason": "C_metric_ext, C_Green, C_obs and arena kernels remain nonnumeric.",
            "gate_pass": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE2480_6_no_shortcuts",
            "claim": "No GR shortcut, fitted GM, M_H_ref reuse, or plateau axiom is used.",
            "gate_status": "PASS_GUARDRAIL",
            "reason": "All shortcut routes remain explicit blockers.",
            "gate_pass": True,
            "claim_allowed": False,
        },
    ]
    return [stamp(row) for row in rows]


def decision_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "decision_id": "DEC2480_0_gain",
            "decision": "Accept the zero-certificate sweep as narrowing progress.",
            "reason": "It proves which non-EGK slots survive the clean route and prevents hiding them under E_GK_bound.",
            "effect": "The theory branch becomes more honest and more derivable.",
        },
        {
            "decision_id": "DEC2480_1_extend_norm",
            "decision": "Define E_local_res as a nonclaim fallback norm.",
            "reason": "All-zero proof fails in the current corpus, so the retained slots need a named home.",
            "effect": "Future tests must use E_local_res or prove slots zero first.",
        },
        {
            "decision_id": "DEC2480_2_next_source_norm",
            "decision": "Attack e_source_norm_gap next.",
            "reason": "It is central to Newton's source and cannot be replaced by R10/PPN arena work.",
            "effect": "2481 selected.",
        },
    ]
    return [stamp(row) for row in rows]


def next_target_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "route_id": "NEXT2480_0_selected",
            "selection_status": "selected",
            "target_file": "2481-Y5-R2FR-Hilbert-worldtube-source-normalization-zero-certificate-or-Enorm-row.md",
            "target_script": "scripts/Y5_R2FR_Hilbert_worldtube_source_normalization_zero_certificate_or_Enorm_row_2481.py",
            "task": "derive or block e_source_norm_gap=0 by closing ell_J, kappa0/G_ref, Hilbert worldtube charge, surface independence, and no fitted-GM source equivalence",
            "acceptance_target": "source-normalization theorem attempt, worldtube Gauss/surface-independence gate, no-fitted-GM guardrail, E_norm retained if unsigned",
            "guardrails": "no GR shortcut; no fitted GM; no M_H_ref reuse; no plateau axiom; no GitHub",
        }
    ]
    return [stamp(row) for row in rows]


def copy_branch_outputs() -> list[dict[str, Any]]:
    copy_map = {
        "zero_certificate": OUTPUTS["zero_certificate"],
        "extended_norm": OUTPUTS["extended_norm"],
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
                    "copy_id": f"COPY2480_{key}",
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

    required_slots = {
        "e_HD_curvature_operator",
        "e_aux_constraint_stress",
        "e_tau_clock_frame_leak",
        "e_q_weyl_spurion",
        "e_species_shadow_or_zero",
        "e_source_norm_gap",
        "e_background_subtraction",
    }
    found_slots = {row["slot"] for row in data["zeros"]}

    add("VAL2480_00_sources_exist", all(row["source_pass"] is True for row in data["sources"]), "all cited local source paths exist and needles are present")
    add("VAL2480_01_required_slots", required_slots <= found_slots, "all non-EGK residual slots have zero/retain rows", ";".join(sorted(found_slots)))
    add(
        "VAL2480_02_no_false_zero",
        not any(row["retain_or_zero"] == "ZERO" and row["valid_for_claim"] is True for row in data["zeros"]),
        "no slot is promoted to claim-ready zero",
    )
    add(
        "VAL2480_03_extended_norm_written",
        any(row["norm_symbol"] == "E_local_res" for row in data["norms"]),
        "extended local residual norm vector is written",
    )
    add(
        "VAL2480_04_source_norm_priority",
        any(row["route_id"] == "NEXT2480_0_selected" for row in data["next"]),
        "2481 source-normalization target selected",
    )
    add("VAL2480_05_claim_gates_safe", all(row["claim_allowed"] is False for row in data["gates"]), "no gate allows Newton/local-GR/R10 claim")
    add("VAL2480_06_branch_copies", all(row["source_exists"] is True and row["target_exists"] is True for row in data["copies"]), "nonclaim branch copies exist")

    formalization_artifacts = []
    if FORMALIZATION.exists():
        for pattern in ("*2480*", "*P8_Y5_NON_EGK_ZERO_2480*", "*JR2480*"):
            formalization_artifacts.extend(FORMALIZATION.rglob(pattern))
    add("VAL2480_07_no_formalization_artifacts", not formalization_artifacts, "no 2480 artifacts were written to formalization-workbench", ";".join(str(path) for path in formalization_artifacts))

    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        parsed, count, error = csv_parses(path)
        add(f"VAL2480_CSV_{path.stem}", parsed and count > 0, f"CSV parses with {count} rows", error)
    for key, path in COPY_TARGETS.items():
        parsed, count, error = csv_parses(path)
        add(f"VAL2480_COPY_CSV_{key}", parsed and count > 0, f"copy CSV parses with {count} rows", error)

    overall = all(row["status"] == "PASS" for row in rows)
    add(
        "VAL2480_OVERALL",
        overall,
        "2480 audits non-EGK zero certificates, retains unsigned slots in E_local_res, and selects source-normalization closure next",
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
        "# 2480 Y5 R2FR Non-EGK Residual Zero Certificates Or Extended Norm Vector",
        "",
        "**Status:** zero-certificate sweep completed, but no zero theorem is promoted. The clean all-zero route does not close in the current corpus, so the retained slots are placed in an explicit extended norm vector `E_local_res` rather than hidden inside `E_GK_bound`.",
        "",
        "**Main result:** the local branch now has an honest fork. Either prove the retained non-EGK slots zero, or carry them explicitly as `E_local_res = E_GK_bound + E_HD + E_aux + E_tau + E_qspur + E_shadow + E_norm + E_bg`. The highest-value next slot is `E_norm`, because source normalization is the bridge from field equation to Newtonian mass without fitted orbital GM.",
        "",
        "## Source Register",
        markdown_table(data["sources"], ["source_id", "source_path", "exists", "missing_needles", "source_pass", "role"]),
        "",
        "## Zero Certificate Attempt",
        markdown_table(data["zeros"], ["slot_id", "slot", "zero_route", "attempt_result", "reason", "retain_or_zero", "extended_norm_slot", "valid_for_claim"]),
        "",
        "## Extended Norm Vector",
        markdown_table(data["norms"], ["norm_id", "norm_symbol", "definition", "role", "status", "valid_for_claim"]),
        "",
        "## Slot Decision Ledger",
        markdown_table(data["slots"], ["decision_id", "question", "answer", "evidence", "effect", "valid_for_claim"]),
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
        "zeros": zero_certificate_rows(),
        "norms": extended_norm_rows(),
        "slots": slot_decision_rows(),
        "gates": claim_gate_rows(),
        "decisions": decision_rows(),
        "next": next_target_rows(),
    }
    write_csv(OUTPUTS["source_register"], data["sources"])
    write_csv(OUTPUTS["zero_certificate"], data["zeros"])
    write_csv(OUTPUTS["extended_norm"], data["norms"])
    write_csv(OUTPUTS["slot_decision"], data["slots"])
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
