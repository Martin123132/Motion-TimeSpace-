from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


BRANCH_ID = "MTS_R2FR_PARENT_EH_COUPLING_ORIGIN_2569"
CHECKPOINT_ID = "2569"

ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = ROOT.parent
FORMALIZATION = PROJECT_ROOT / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"

DOC = ROOT / "2569-Y5-R2FR-parent-EH-coupling-origin-or-coupling-residual-row.md"

OUTPUTS = {
    "source_register": OUT / "P8_Y5_EH_COUPLING_2569_SOURCE_REGISTER.csv",
    "origin_audit": OUT / "P8_Y5_EH_COUPLING_2569_ORIGIN_AUDIT.csv",
    "coupling_residual": OUT / "P8_Y5_EH_COUPLING_2569_COUPLING_RESIDUAL_ROW.csv",
    "route_matrix": OUT / "P8_Y5_EH_COUPLING_2569_ROUTE_MATRIX.csv",
    "claim_gates": OUT / "P8_Y5_EH_COUPLING_2569_CLAIM_GATES.csv",
    "decision_ledger": OUT / "P8_Y5_EH_COUPLING_2569_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_EH_COUPLING_2569_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_EH_COUPLING_2569_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2569_VALIDATION.csv",
}

COPY_TARGETS = {
    "origin_audit": LOCAL_BOUNDS / "Parent_EH_coupling_origin_audit_2569_NONCLAIM.csv",
    "coupling_residual": LOCAL_BOUNDS / "KappaG_ellJ_coupling_residual_row_2569_NONCLAIM.csv",
    "acquisition_queue": QUEUE / "JR2569_PARENT_NORMAL_FORM_FIELD_SYMMETRY_DERIVATIVE_GRAMMAR.csv",
}

SOURCES = [
    {
        "source_id": "SRC2569_00_2568_doc",
        "source_path": ROOT / "2568-Y5-R2FR-Hilbert-worldtube-source-normalization-zero-certificate-or-Enorm-row.md",
        "needles": ["NEXT2568_0_selected", "ENORM2568_1_e_kappaG", "ENORM2568_2_e_ellJ_owner", "VAL2568_OVERALL"],
        "role": "active handoff selecting EH/coupling origin and naming e_kappaG/e_ellJ_owner",
    },
    {
        "source_id": "SRC2569_01_2404_first_variation",
        "source_path": ROOT / "2404-Y5-R2FR-minimal-parent-action-first-variation-GR-Newton-gate-or-operator-residual-pack.md",
        "needles": ["S_min=S_EH", "CANDIDATE_NOT_DERIVED", "REF2404_1_EH_import"],
        "role": "candidate EH first variation and EH-import rejection",
    },
    {
        "source_id": "SRC2569_02_2483_precedent",
        "source_path": ROOT / "2483-Y5-R2FR-parent-EH-coupling-origin-or-coupling-residual-row.md",
        "needles": ["EH2483_2_parent_origin", "KRES2483_0_e_kappaG", "VAL2483_OVERALL"],
        "role": "earlier EH/coupling origin audit and kappa residual precedent",
    },
    {
        "source_id": "SRC2569_03_2484_uniqueness",
        "source_path": ROOT / "2484-Y5-R2FR-EH-uniqueness-hypotheses-or-parent-normal-form-blocker.md",
        "needles": ["HYP2484_6_coefficient_owner", "NFB2484_5_EH_coefficient_owner", "VAL2484_OVERALL"],
        "role": "EH uniqueness hypothesis contract and coefficient-owner blocker",
    },
    {
        "source_id": "SRC2569_04_2485_normal_form",
        "source_path": ROOT / "2485-Y5-R2FR-parent-normal-form-field-symmetry-derivative-grammar.md",
        "needles": ["NF2485_0_parent_action_skeleton", "CS2485_0_a1_kappa", "VAL2485_OVERALL"],
        "role": "parent normal-form skeleton and coefficient slot ledger",
    },
    {
        "source_id": "SRC2569_05_2405_EH_dominance",
        "source_path": ROOT / "2405-Y5-R2FR-EH-dominance-and-MTS-residual-sector-silence-or-operator-bound-pack.md",
        "needles": ["EHD2405_0_target", "EHD2405_4_current_verdict", "REF2405_0_EH_by_notation"],
        "role": "EH dominance and residual silence blocker",
    },
    {
        "source_id": "SRC2569_06_2406_sector_residuals",
        "source_path": ROOT / "2406-Y5-R2FR-sector-by-sector-MTS-residual-variation-and-local-scaling-silence-or-operator-bounds.md",
        "needles": ["SVC2406_6_verdict", "CG2406_0_EH_dominance", "VAL2406_OVERALL"],
        "role": "live non-EH residual sectors blocking local GR/Newton",
    },
    {
        "source_id": "SRC2569_07_2568_validation",
        "source_path": OUT / "P8_Y5_BRR545_2568_VALIDATION.csv",
        "needles": ["VAL2568_OVERALL", "PASS"],
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
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def csv_parses(path: Path) -> tuple[bool, int, str]:
    try:
        with path.open("r", encoding="utf-8", newline="") as handle:
            rows = list(csv.DictReader(handle))
        return True, len(rows), ""
    except Exception as exc:
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
            "audit_id": "EH2569_0_standard_variation",
            "object": "standard EH variation",
            "statement": "delta S_EH gives Einstein operator with coefficient kappa0 inside the candidate branch",
            "current_result": "mathematically standard and usable as a conditional template",
            "status": "PASS_TEMPLATE",
            "missing_for_claim": "does not prove MTS parent action generates the EH-leading term",
            "valid_for_claim": False,
        },
        {
            "audit_id": "EH2569_1_candidate_inclusion",
            "object": "S_min contains S_EH[e]",
            "statement": "private candidate action includes EH term plus silent/residual sectors",
            "current_result": "first variation bridge is exact if candidate is accepted",
            "status": "PASS_CANDIDATE_NONCLAIM",
            "missing_for_claim": "candidate clauses are not derived from deeper MTS primitives",
            "valid_for_claim": False,
        },
        {
            "audit_id": "EH2569_2_parent_origin",
            "object": "MTS-to-EH leading operator theorem",
            "statement": "derive the unique local two-derivative diffeomorphism-invariant metric/coframe operator from MTS parent variables",
            "current_result": "not present in current corpus; 2484/2485 only write the hypothesis/normal-form contracts",
            "status": "BLOCKED_PARENT_ORIGIN",
            "missing_for_claim": "typed field list, quotient map, symmetry generator, derivative-order grammar, coefficient owner, boundary class",
            "valid_for_claim": False,
        },
        {
            "audit_id": "EH2569_3_coupling_owner",
            "object": "kappa0 coefficient owner",
            "statement": "derive the coefficient multiplying the EH-leading term before empirical local tests",
            "current_result": "kappa0=8*pi*G_ref/c^4 remains a conditional relation, not an MTS derivation",
            "status": "BLOCKED_COUPLING_OWNER",
            "missing_for_claim": "parent normalization constant, primitive scale/coupling source, or accepted empirical-coupling declaration",
            "valid_for_claim": False,
        },
        {
            "audit_id": "EH2569_4_ellJ_owner",
            "object": "ell_J source-current scale owner",
            "statement": "tie ell_J to the same parent normalization/scale ledger as kappa_MTS, or declare it a separate universal source-current coupling",
            "current_result": "ell_J cancels in stationary mass readout but not in q_loc/current amplitude; parent ownership is unsigned",
            "status": "BLOCKED_SOURCE_SCALE_OWNER",
            "missing_for_claim": "parent scale, parent gap, tau-normalization theorem, or explicit universal coupling declaration before tests",
            "valid_for_claim": False,
        },
        {
            "audit_id": "EH2569_5_residual_dominance",
            "object": "EH dominance over DeltaE_MTS",
            "statement": "prove non-EH residual sectors vanish, are silent, or are bounded below local thresholds",
            "current_result": "2405/2406 and 2567 keep finite residual owners live",
            "status": "BLOCKED_RESIDUAL_SILENCE",
            "missing_for_claim": "sector zero certificates or source-backed operator bounds in the 2567 E_local_res basis",
            "valid_for_claim": False,
        },
        {
            "audit_id": "EH2569_6_no_import",
            "object": "EH/GR import as proof",
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
            "residual_id": "KRES2569_0_e_kappaG",
            "symbol": "e_kappaG",
            "definition": "dimensionless residual between candidate kappa0 and the parent coupling that would be measured as G_ref",
            "formal_row": "e_kappaG := |kappa_MTS-kappa_ref|/kappa_ref, or KAPPA_OWNER_MISSING while kappa_MTS is absent",
            "status": "RETAIN_NONCLAIM",
            "zero_condition": "parent action derives EH-leading coefficient kappa_MTS and G_ref is only later measurement",
            "valid_for_claim": False,
        },
        {
            "residual_id": "KRES2569_1_kappa_MTS",
            "symbol": "kappa_MTS",
            "definition": "coefficient of the parent-derived EH-leading operator",
            "formal_row": "S_parent -> (1/(2*kappa_MTS))*int sqrt(-g) R[e] + residual sectors",
            "status": "MISSING_PARENT_COEFFICIENT",
            "zero_condition": "MTS parent normal form supplies this coefficient before local/cosmology tests",
            "valid_for_claim": False,
        },
        {
            "residual_id": "KRES2569_2_G_parent",
            "symbol": "G_parent",
            "definition": "G_parent:=kappa_MTS*c^4/(8*pi) once kappa_MTS exists",
            "formal_row": "definition allowed only after kappa_MTS is parent-owned",
            "status": "DOWNSTREAM_DEFINITION_ONLY",
            "zero_condition": "G_ref measures G_parent, not vice versa",
            "valid_for_claim": False,
        },
        {
            "residual_id": "KRES2569_3_e_EH_import",
            "symbol": "e_EH_import",
            "definition": "logic residual incurred if EH is inserted as a template instead of derived from MTS primitives",
            "formal_row": "e_EH_import=0 only if parent-origin theorem closes",
            "status": "RETAIN_LOGIC_GUARDRAIL",
            "zero_condition": "MTS-to-EH leading-operator theorem with signed field/symmetry/derivative grammar",
            "valid_for_claim": False,
        },
        {
            "residual_id": "KRES2569_4_e_ellJ_owner",
            "symbol": "e_ellJ_owner",
            "definition": "source-current scale ownership residual for ell_J in J_M^nu=ell_J T_H^{nu rho} tau_rho",
            "formal_row": "e_ellJ_owner := ELLJ_PARENT_OWNER_MISSING unless ell_J is fixed by parent scale/gap/tau normalization before tests",
            "status": "RETAIN_NONCLAIM",
            "zero_condition": "ell_J is parent-owned or declared as a universal coupling independent of fitted GM/H0/M_H_ref",
            "valid_for_claim": False,
        },
        {
            "residual_id": "KRES2569_5_a1_ellJ_relation",
            "symbol": "a1_vs_ellJ",
            "definition": "possible relation between EH coefficient a1=1/(2*kappa_MTS) and source-current scale ell_J",
            "formal_row": "UNSIGNED: a1 and ell_J may share a parent scale, or may be independent universal constants; neither route is signed",
            "status": "RELATION_UNSIGNED",
            "zero_condition": "parent normal form shows whether kappa_MTS and ell_J derive from the same primitive scale or from independent coupling slots",
            "valid_for_claim": False,
        },
    ]
    return [stamp(row) for row in rows]


def route_matrix_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "route_id": "ROUTE2569_A_lovelock_like",
            "route": "symmetry/derivative-order uniqueness",
            "attempt": "supply public metric/coframe, local diffeomorphism symmetry, two-derivative leading equations, no extra local tensors, then EH is unique up to Lambda/boundary",
            "strength": "least arbitrary if MTS can sign the hypotheses",
            "current_status": "HYPOTHESES_UNSIGNED",
            "next_input": "field list, quotient map, symmetry generator, derivative grammar, residual zero/bound certificates",
            "valid_for_claim": False,
        },
        {
            "route_id": "ROUTE2569_B_parent_normal_form",
            "route": "one parent action inventory",
            "attempt": "use the 2485 skeleton to assign owner slots for a0, a1/kappa_MTS, ell_J, matter descent, q/tau/projector/boundary residuals",
            "strength": "best practical route because it turns coupling fog into named slots",
            "current_status": "SKELETON_WRITTEN_NOT_PARENT_SIGNED",
            "next_input": "typed field/sort table, quotient map q_parent, ker(Dq), symmetry generator and coefficient owner",
            "valid_for_claim": False,
        },
        {
            "route_id": "ROUTE2569_C_effective_field_theory",
            "route": "EFT leading operator fallback",
            "attempt": "treat EH as the leading low-energy operator and keep all non-EH/source-normalization terms as residual coefficients",
            "strength": "honest and publishable as effective framework, but weaker than a fundamental derivation",
            "current_status": "AVAILABLE_AS_EFFECTIVE_NONCLAIM",
            "next_input": "residual coefficient priors/bounds and explicit language that EH is not yet derived",
            "valid_for_claim": False,
        },
        {
            "route_id": "ROUTE2569_D_import_GR",
            "route": "import GR because it works",
            "attempt": "use standard local success of GR as proof of MTS local reduction",
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
            "gate_id": "GATE2569_0_EH_template",
            "claim": "Standard EH variation is available as a conditional template.",
            "gate_status": "PASS_CONDITIONAL_NONCLAIM",
            "reason": "2404 exposes the candidate field equation and weak-field Poisson lane.",
            "gate_pass": True,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE2569_1_parent_EH",
            "claim": "MTS parent action derives the EH-leading operator.",
            "gate_status": "BLOCKED",
            "reason": "field/symmetry/derivative grammar and coefficient owner are unsigned.",
            "gate_pass": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE2569_2_kappa_owner",
            "claim": "kappa0/G_ref is parent-derived.",
            "gate_status": "BLOCKED",
            "reason": "kappa_MTS is not parent-owned; G_ref cannot be used as proof input.",
            "gate_pass": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE2569_3_ellJ_owner",
            "claim": "ell_J is parent-derived or universally declared before tests.",
            "gate_status": "BLOCKED",
            "reason": "stationary mass readout cancels ell_J, but q_loc/current amplitude still needs source-scale ownership.",
            "gate_pass": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE2569_4_EH_dominance",
            "claim": "EH dominates all MTS residual sectors locally.",
            "gate_status": "BLOCKED",
            "reason": "DeltaE_MTS sector owners remain live from 2405/2406 and the 2567 E_local_res basis.",
            "gate_pass": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE2569_5_Newton_GR",
            "claim": "Newton/local-GR limit is derived.",
            "gate_status": "BLOCKED",
            "reason": "parent EH origin, kappa/ell_J ownership, residual silence and source normalization remain open.",
            "gate_pass": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE2569_6_no_shortcuts",
            "claim": "No GR shortcut, EH import proof, fitted GM, M_H_ref reuse, plateau axiom or GitHub/public step is used.",
            "gate_status": "PASS_GUARDRAIL",
            "reason": "EH import and orbital-GM laundering are explicit residuals/forbidden routes.",
            "gate_pass": True,
            "claim_allowed": False,
        },
    ]
    return [stamp(row) for row in rows]


def decision_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "decision_id": "DEC2569_0_status",
            "decision": "Retain e_kappaG, e_ellJ_owner and e_EH_import.",
            "reason": "EH/coupling are conditional candidate ingredients, not parent-derived theorem outputs.",
            "effect": "local-GR/Newton remains blocked but the coupling problem is now split into owned residual rows.",
        },
        {
            "decision_id": "DEC2569_1_best_route",
            "decision": "Prefer parent normal form over another arena-bound pass.",
            "reason": "R10/PPN kernels are downstream; they cannot establish the parent coefficient owner.",
            "effect": "next checkpoint should sign or split the field/sort and quotient map owners.",
        },
        {
            "decision_id": "DEC2569_2_effective_fallback",
            "decision": "Keep EFT-leading-operator route as fallback language only.",
            "reason": "It may become respectable public scaffolding, but it is not the same as deriving GR from MTS primitives.",
            "effect": "do not claim fundamental GR reduction until parent normal-form gates close.",
        },
    ]
    return [stamp(row) for row in rows]


def next_target_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "route_id": "NEXT2569_0_selected",
            "selection_status": "selected",
            "target_file": "2570-Y5-R2FR-parent-field-sort-and-quotient-map-signature-or-residual-owner-split.md",
            "target_script": "scripts/Y5_R2FR_parent_field_sort_and_quotient_map_signature_or_residual_owner_split_2570.py",
            "task": "try to sign the typed parent field list and quotient map q_parent, including ker(Dq) vertical generators, matter descent, constants owner, and readout order; if not, split every unsigned variable into explicit residual owners",
            "acceptance_target": "field-sort/quotient theorem attempt, Dq/vertical generator ledger, matter-descent gate, coefficient-owner implications for kappa_MTS and ell_J, no local-GR claim",
            "guardrails": "no EH import; no fitted GM; no declaring variables vertical without Dq/Omega proof; no no-derivative-by-taste; no GitHub",
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
                    "copy_id": f"COPY2569_{key}",
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
        rows.append(stamp({"check_id": check_id, "status": "PASS" if passed else "FAIL", "notes": notes, "detail": detail}))

    output_paths = [DOC, *OUTPUTS.values(), *COPY_TARGETS.values()]
    residual_symbols = {row["symbol"] for row in data["residuals"]}
    add("VAL2569_00_sources_exist", all(row["source_pass"] is True for row in data["sources"]), "all cited local source paths exist and required needles are present")
    add("VAL2569_01_parent_EH_blocked", any(row["audit_id"] == "EH2569_2_parent_origin" and row["status"] == "BLOCKED_PARENT_ORIGIN" for row in data["audits"]), "parent EH-origin theorem remains blocked")
    add("VAL2569_02_kappa_residual_retained", "e_kappaG" in residual_symbols, "e_kappaG residual row is retained")
    add("VAL2569_03_ellJ_residual_retained", "e_ellJ_owner" in residual_symbols, "e_ellJ_owner residual row is retained")
    add("VAL2569_04_invalid_import_rejected", any(row["route_id"] == "ROUTE2569_D_import_GR" and row["current_status"] == "REJECTED" for row in data["routes"]), "GR/EH import route is rejected")
    add("VAL2569_05_claim_gates_safe", all(row["claim_allowed"] is False for row in data["gates"]), "no gate allows Newton/local-GR/R10 claim")
    add("VAL2569_06_next_target_written", any(row["route_id"] == "NEXT2569_0_selected" for row in data["next"]), "2570 parent field-sort/quotient target selected")
    add("VAL2569_07_branch_copies", all(row["source_exists"] is True and row["target_exists"] is True for row in data["copies"]), "nonclaim branch copies exist")
    add("VAL2569_08_no_formalization_targets", all(FORMALIZATION not in path.parents and path != FORMALIZATION for path in output_paths), "all generated target paths are outside formalization-workbench")

    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        parsed, count, error = csv_parses(path)
        add(f"VAL2569_CSV_{path.stem}", parsed and count > 0, f"CSV parses with {count} rows", error)
    for key, path in COPY_TARGETS.items():
        parsed, count, error = csv_parses(path)
        add(f"VAL2569_COPY_CSV_{key}", parsed and count > 0, f"copy CSV parses with {count} rows", error)

    overall = all(row["status"] == "PASS" for row in rows)
    add(
        "VAL2569_OVERALL",
        overall,
        "2569 keeps EH/coupling as conditional candidate structure, retains e_kappaG/e_ellJ_owner/e_EH_import, rejects GR import, and selects field-sort/quotient signature next",
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
        "# 2569 Y5 R2FR Parent EH Coupling Origin Or Coupling Residual Row",
        "",
        "**Status:** EH/coupling origin is not derived yet. The standard EH variation and candidate first-variation bridge are valid conditional mathematics, but they do not prove that MTS itself generates the EH-leading operator or owns `kappa0`, `G_parent`, or `ell_J`.",
        "",
        "**Main result:** separate four layers: standard EH template, candidate EH inclusion, parent-derived EH origin, and source-current scale ownership. The first two exist; the latter two are still blocked. Therefore `e_kappaG`, `e_ellJ_owner`, and `e_EH_import` remain explicit nonclaim residuals until MTS supplies the parent normal-form field/symmetry/derivative grammar and coefficient owners.",
        "",
        "## Source Register",
        markdown_table(data["sources"], ["source_id", "source_path", "exists", "missing_needles", "source_pass", "role"]),
        "",
        "## Origin Audit",
        markdown_table(data["audits"], ["audit_id", "object", "statement", "current_result", "status", "missing_for_claim", "valid_for_claim"]),
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
        "audits": origin_audit_rows(),
        "residuals": coupling_residual_rows(),
        "routes": route_matrix_rows(),
        "gates": claim_gate_rows(),
        "decisions": decision_rows(),
        "next": next_target_rows(),
    }
    write_csv(OUTPUTS["source_register"], data["sources"])
    write_csv(OUTPUTS["origin_audit"], data["audits"])
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
