from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


BRANCH_ID = "MTS_R2FR_PARENT_WEAK_FIELD_METRIC_RESPONSE_THEOREM_2477"
CHECKPOINT_ID = "2477"

ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = ROOT.parent
FORMALIZATION = PROJECT_ROOT / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"

DOC = ROOT / "2477-Y5-R2FR-parent-weak-field-metric-response-theorem-or-no-go.md"

OUTPUTS = {
    "source_register": OUT / "P8_Y5_WEAK_FIELD_RESPONSE_2477_SOURCE_REGISTER.csv",
    "theorem_attempt": OUT / "P8_Y5_WEAK_FIELD_RESPONSE_2477_THEOREM_ATTEMPT.csv",
    "cmetric_factorisation": OUT / "P8_Y5_WEAK_FIELD_RESPONSE_2477_CMETRIC_FACTORISATION.csv",
    "blocker_ledger": OUT / "P8_Y5_WEAK_FIELD_RESPONSE_2477_BLOCKER_LEDGER.csv",
    "claim_gates": OUT / "P8_Y5_WEAK_FIELD_RESPONSE_2477_CLAIM_GATES.csv",
    "decision_ledger": OUT / "P8_Y5_WEAK_FIELD_RESPONSE_2477_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_WEAK_FIELD_RESPONSE_2477_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_WEAK_FIELD_RESPONSE_2477_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2477_VALIDATION.csv",
}

COPY_TARGETS = {
    "cmetric_factorisation": LOCAL_BOUNDS / "Cmetric_factorisation_2477_NONCLAIM.csv",
    "blocker_ledger": LOCAL_BOUNDS / "Weak_field_metric_response_blocker_2477_NONCLAIM.csv",
    "acquisition_queue": QUEUE / "JR2477_RESIDUAL_SOURCE_NORM_GREEN_CERTIFICATE.csv",
}

SOURCES = [
    {
        "source_id": "SRC2477_00_2476_doc",
        "source_path": ROOT / "2476-Y5-R2FR-R10-kernel-and-Cmetric-source-map-or-blocker.md",
        "needles": ["NEXT2476_0_selected", "parent weak-field metric-response theorem", "FORBIDDEN_AS_PROOF", "VAL2476_OVERALL"],
        "role": "handoff selecting non-circular parent weak-field response",
    },
    {
        "source_id": "SRC2477_01_2404_field_equation",
        "source_path": ROOT / "2404-Y5-R2FR-minimal-parent-action-first-variation-GR-Newton-gate-or-operator-residual-pack.md",
        "needles": ["G_munu+Lambda g_munu+DeltaE_MTS+DeltaE_boundary", "nabla^2 U=4 pi G_ref rho_H", "CG2404_4_local_GR_Newton"],
        "role": "candidate first-variation and weak-field Poisson bridge",
    },
    {
        "source_id": "SRC2477_02_2405_residual_basis",
        "source_path": ROOT / "2405-Y5-R2FR-EH-dominance-and-MTS-residual-sector-silence-or-operator-bound-pack.md",
        "needles": ["DeltaE_MTS", "OPB2405_0_total_DeltaE_MTS", "CG2405_4_local_GR_Newton"],
        "role": "left-hand residual sector split and EH dominance blocker",
    },
    {
        "source_id": "SRC2477_03_2466_source_bridge",
        "source_path": ROOT / "2466-Y5-R2FR-matter-current-descent-and-worldtube-source-bridge.md",
        "needles": ["J_M^nu = ell_J T_matter", "MISSING_PARENT_SCALE", "fitted orbital GM"],
        "role": "Hilbert source bridge and no fitted-GM guardrail",
    },
    {
        "source_id": "SRC2477_04_2476_validation",
        "source_path": OUT / "P8_Y5_BRR545_2476_VALIDATION.csv",
        "needles": ["VAL2476_OVERALL", "PASS"],
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


def theorem_attempt_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "theorem_id": "THM2477_0_parent_candidate_equation",
            "step": "start from candidate parent first variation",
            "formula": "G_munu+Lambda*g_munu+DeltaE_MTS_munu+DeltaE_boundary_munu = kappa0*(T_H_munu+J_shadow_munu)",
            "result": "This gives a non-circular equation to linearize because the residuals remain explicit instead of assumed zero.",
            "status": "PASS_CONDITIONAL_INPUT",
            "missing_for_claim": "candidate parent action and EH dominance are not parent-signed",
            "claim_allowed": False,
        },
        {
            "theorem_id": "THM2477_1_linearized_00_lane",
            "step": "linearize the 00 component in weak field",
            "formula": "g_00=-(1+2U/c^2+O(c^-4)); G_00^(1)=2*nabla^2 U/c^2",
            "result": "The candidate equation has a clean Poisson lane once residual/source-shadow terms are tracked.",
            "status": "STANDARD_WEAK_FIELD_TEMPLATE_INSIDE_CANDIDATE",
            "missing_for_claim": "gauge, sign convention, and EH-leading-operator origin still need parent certificate",
            "claim_allowed": False,
        },
        {
            "theorem_id": "THM2477_2_residual_poisson_equation",
            "step": "isolate residual source",
            "formula": "nabla^2 U = 4*pi*G_ref*rho_H + S_res, with S_res=(c^2/2)*(kappa0*J_shadow_00-DeltaE_MTS_00-DeltaE_boundary_00-Lambda*g_00)+delta_G_source",
            "result": "Local Newton follows iff S_res=0 or is bounded below local-test thresholds.",
            "status": "CONDITIONAL_DERIVED_FACTOR",
            "missing_for_claim": "J_shadow, DeltaE_MTS, DeltaE_boundary, Lambda/local subtraction, and delta_G_source are not all zeroed or bounded",
            "claim_allowed": False,
        },
        {
            "theorem_id": "THM2477_3_metric_residual_green_bound",
            "step": "solve for metric residual",
            "formula": "nabla^2 deltaU=S_res; ||deltaU||_obs <= C_Green*C_obs*||S_res||_dual",
            "result": "This is the non-circular route to C_metric: derive a Green/norm bound for the residual source.",
            "status": "CONDITIONAL_GREEN_BOUND_SHAPE",
            "missing_for_claim": "domain, boundary conditions, gauge, norm, and observation functional are not certified",
            "claim_allowed": False,
        },
        {
            "theorem_id": "THM2477_4_Cmetric_factorisation",
            "step": "factor the coefficient needed by 2476",
            "formula": "If ||S_res||_dual <= C_res*E_GK_bound, then ||delta g_00||_obs <= (2/c^2)*C_obs*C_Green*C_res*E_GK_bound := C_metric*E_GK_bound",
            "result": "C_metric is not magic; it factorises into Green, observable, and residual-source coefficients.",
            "status": "FACTORISATION_DERIVED_CONDITIONALLY",
            "missing_for_claim": "C_res, C_Green, C_obs, E_GK_bound are not numeric/source-backed",
            "claim_allowed": False,
        },
        {
            "theorem_id": "THM2477_5_not_a_no_go",
            "step": "decide theorem/no-go outcome",
            "formula": "The theorem is not closed, but it is also not a no-go: the exact missing coefficient chain is now named.",
            "result": "The right next move is not R10 geometry first; it is residual-source norm plus Green/boundary certificate.",
            "status": "PARTIAL_THEOREM_NOT_PROMOTED",
            "missing_for_claim": "all coefficient factors remain unsigned",
            "claim_allowed": False,
        },
    ]
    return [stamp(row) for row in rows]


def cmetric_factorisation_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "factor_id": "CM2477_0_Cres",
            "symbol": "C_res",
            "definition": "||S_res||_dual <= C_res*E_GK_bound",
            "depends_on": "DeltaE_MTS, DeltaE_boundary, J_shadow, delta_G_source, Lambda subtraction",
            "status": "MISSING_SOURCE_NORM",
            "units_role": "converts residual operator norm into Poisson source units",
            "valid_for_claim": False,
        },
        {
            "factor_id": "CM2477_1_Cgreen",
            "symbol": "C_Green",
            "definition": "||deltaU|| <= C_Green*||S_res||_dual for the selected local domain",
            "depends_on": "gauge, boundary conditions, falloff, source collar, elliptic norm",
            "status": "MISSING_BOUNDARY_GAUGE_CERTIFICATE",
            "units_role": "Poisson inverse/operator norm",
            "valid_for_claim": False,
        },
        {
            "factor_id": "CM2477_2_Cobs",
            "symbol": "C_obs",
            "definition": "projection from deltaU or delta g_00 to the chosen observable",
            "depends_on": "R10 torsion signal, PPN gamma/beta, clock rate, orbital acceleration, WEP channel",
            "status": "MISSING_ARENA_PROJECTION",
            "units_role": "observable-specific dimensionless projection",
            "valid_for_claim": False,
        },
        {
            "factor_id": "CM2477_3_Cmetric",
            "symbol": "C_metric",
            "definition": "C_metric=(2/c^2)*C_obs*C_Green*C_res",
            "depends_on": "CM2477_0_Cres;CM2477_1_Cgreen;CM2477_2_Cobs",
            "status": "FORMAL_FACTORISATION_ONLY",
            "units_role": "maps E_GK_bound to observed metric residual",
            "valid_for_claim": False,
        },
        {
            "factor_id": "CM2477_4_source_normalization",
            "symbol": "delta_G_source",
            "definition": "difference between kappa0/G_ref/Hilbert mass normalization and the source charge used in Newton/R10 comparisons",
            "depends_on": "Hilbert current descent, ell_J, worldtube surface independence, no fitted GM",
            "status": "MISSING_PARENT_SOURCE_NORMALIZATION",
            "units_role": "prevents hidden orbital-G calibration",
            "valid_for_claim": False,
        },
    ]
    return [stamp(row) for row in rows]


def blocker_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "blocker_id": "BLK2477_0_EH_origin",
            "missing_object": "MTS-to-EH leading operator theorem",
            "why_it_blocks": "The linearized Einstein operator is present in the candidate, but its origin from deeper MTS primitives is not signed.",
            "next_action": "keep EH lane conditional until parent action normal form is promoted or replaced",
            "valid_for_claim": False,
        },
        {
            "blocker_id": "BLK2477_1_Cres",
            "missing_object": "residual-source norm C_res",
            "why_it_blocks": "DeltaE_MTS, boundary, source-shadow, and source-normalization residuals are not bounded by E_GK_bound.",
            "next_action": "derive sector residual norm inequalities or produce explicit coefficient rows",
            "valid_for_claim": False,
        },
        {
            "blocker_id": "BLK2477_2_Cgreen",
            "missing_object": "Green/gauge/boundary certificate",
            "why_it_blocks": "A Poisson residual only becomes a metric bound after domain, boundary, gauge, and norm choices are fixed.",
            "next_action": "write local collar Green theorem or blocker for the chosen exterior lab domain",
            "valid_for_claim": False,
        },
        {
            "blocker_id": "BLK2477_3_Cobs",
            "missing_object": "arena observable projection",
            "why_it_blocks": "R10, PPN, clocks, and orbits read different projections of the same metric residual.",
            "next_action": "only build K_R10 after C_metric's source and Green factors exist",
            "valid_for_claim": False,
        },
        {
            "blocker_id": "BLK2477_4_source_normalization",
            "missing_object": "Hilbert source charge and kappa0/G_ref calibration",
            "why_it_blocks": "Newton source mass cannot be defined by fitted orbital GM without circularity.",
            "next_action": "return to ell_J/worldtube surface independence if the residual norm route needs numeric normalization",
            "valid_for_claim": False,
        },
        {
            "blocker_id": "BLK2477_5_ppn_second_order",
            "missing_object": "spatial and second-order metric equations",
            "why_it_blocks": "A 00 Poisson lane is enough for Newton/R10 residual shape, not full GR/PPN beta/gamma.",
            "next_action": "after C_metric, extend to ij and O(c^-4) equations before claiming local GR",
            "valid_for_claim": False,
        },
    ]
    return [stamp(row) for row in rows]


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "gate_id": "GATE2477_0_factorisation",
            "claim": "C_metric has a non-circular formal factorisation.",
            "gate_status": "PASS_CONDITIONAL_NONCLAIM",
            "reason": "Derived from the candidate parent first variation with residual terms explicit.",
            "gate_pass": True,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE2477_1_numeric_Cmetric",
            "claim": "C_metric is numeric/source-backed.",
            "gate_status": "BLOCKED",
            "reason": "C_res, C_Green, C_obs and E_GK_bound remain missing.",
            "gate_pass": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE2477_2_Newton",
            "claim": "Newton inverse-square law is derived.",
            "gate_status": "BLOCKED",
            "reason": "Requires S_res=0/bounded plus source normalization and boundary conditions.",
            "gate_pass": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE2477_3_local_GR",
            "claim": "Local GR/PPN is derived.",
            "gate_status": "BLOCKED",
            "reason": "Need EH origin, residual silence/bounds, source normalization, and spatial/second-order equations.",
            "gate_pass": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE2477_4_R10",
            "claim": "R10 compatibility can be tested as an MTS prediction.",
            "gate_status": "BLOCKED",
            "reason": "C_metric is factorised but not numeric; K_R10 still downstream.",
            "gate_pass": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE2477_5_no_shortcuts",
            "claim": "No fitted-GM or assumed-GR shortcut is used.",
            "gate_status": "PASS_GUARDRAIL",
            "reason": "Source normalization and GR response remain explicit blockers.",
            "gate_pass": True,
            "claim_allowed": False,
        },
    ]
    return [stamp(row) for row in rows]


def decision_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "decision_id": "DEC2477_0_partial_theorem",
            "decision": "Keep 2477 as a partial theorem, not a no-go.",
            "reason": "The parent candidate field equation gives a clean residual Poisson lane and C_metric factorisation.",
            "effect": "The local branch is sharper, but still nonclaim.",
        },
        {
            "decision_id": "DEC2477_1_do_not_jump_to_R10",
            "decision": "Do not build K_R10 next.",
            "reason": "An arena kernel without C_res and C_Green would float over an undefined metric response.",
            "effect": "R10 remains downstream of the metric response certificate.",
        },
        {
            "decision_id": "DEC2477_2_select_2478",
            "decision": "Select residual-source norm and Green certificate as next target.",
            "reason": "This is the shortest path from formal C_metric to a real local-bound input.",
            "effect": "2478 should attempt C_res and C_Green before any observable-specific kernel.",
        },
    ]
    return [stamp(row) for row in rows]


def next_target_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "route_id": "NEXT2477_0_selected",
            "selection_status": "selected",
            "target_file": "2478-Y5-R2FR-residual-source-norm-and-Green-bound-certificate.md",
            "target_script": "scripts/Y5_R2FR_residual_source_norm_and_Green_bound_certificate_2478.py",
            "task": "derive or block C_res and C_Green in C_metric=(2/c^2)*C_obs*C_Green*C_res, using the 2404/2477 residual Poisson lane",
            "acceptance_target": "residual norm inequality, local collar boundary/gauge certificate, source-normalization guardrail, explicit nonclaim if any coefficient remains symbolic",
            "guardrails": "no GR shortcut; no fitted GM; no M_H_ref reuse; no plateau axiom; no GitHub",
        }
    ]
    return [stamp(row) for row in rows]


def copy_branch_outputs() -> list[dict[str, Any]]:
    copy_map = {
        "cmetric_factorisation": OUTPUTS["cmetric_factorisation"],
        "blocker_ledger": OUTPUTS["blocker_ledger"],
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
                    "copy_id": f"COPY2477_{key}",
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

    add("VAL2477_00_sources_exist", all(row["source_pass"] is True for row in data["sources"]), "all cited local source paths exist and needles are present")
    add(
        "VAL2477_01_factorisation_written",
        any(row["theorem_id"] == "THM2477_4_Cmetric_factorisation" for row in data["theorems"]),
        "C_metric factorisation row exists",
    )
    add(
        "VAL2477_02_factorisation_nonclaim",
        all(row["claim_allowed"] is False for row in data["theorems"]),
        "theorem rows remain nonclaim",
    )
    add(
        "VAL2477_03_Cmetric_factors_blocked",
        all(row["valid_for_claim"] is False for row in data["factors"]),
        "all C_metric factors remain nonclaim",
    )
    add(
        "VAL2477_04_blockers_present",
        len(data["blockers"]) >= 5 and all(row["valid_for_claim"] is False for row in data["blockers"]),
        "blocker ledger covers EH origin, C_res, C_Green, C_obs and normalization",
    )
    add(
        "VAL2477_05_claim_gates_safe",
        all(row["claim_allowed"] is False for row in data["gates"]),
        "no gate allows Newton/local-GR/R10 claim",
    )
    add(
        "VAL2477_06_next_target_written",
        any(row["route_id"] == "NEXT2477_0_selected" for row in data["next"]),
        "2478 residual-source norm and Green certificate selected",
    )
    add(
        "VAL2477_07_branch_copies",
        all(row["source_exists"] is True and row["target_exists"] is True for row in data["copies"]),
        "nonclaim branch copies exist",
    )
    formalization_artifacts = []
    if FORMALIZATION.exists():
        for pattern in ("*2477*", "*P8_Y5_WEAK_FIELD_RESPONSE_2477*", "*JR2477*"):
            formalization_artifacts.extend(FORMALIZATION.rglob(pattern))
    add("VAL2477_08_no_formalization_artifacts", not formalization_artifacts, "no 2477 artifacts were written to formalization-workbench", ";".join(str(path) for path in formalization_artifacts))

    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        parsed, count, error = csv_parses(path)
        add(f"VAL2477_CSV_{path.stem}", parsed and count > 0, f"CSV parses with {count} rows", error)
    for key, path in COPY_TARGETS.items():
        parsed, count, error = csv_parses(path)
        add(f"VAL2477_COPY_CSV_{key}", parsed and count > 0, f"copy CSV parses with {count} rows", error)

    overall = all(row["status"] == "PASS" for row in rows)
    add(
        "VAL2477_OVERALL",
        overall,
        "2477 derives a conditional non-circular C_metric factorisation and selects C_res/C_Green as the next closure target",
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
        "# 2477 Y5 R2FR Parent Weak-field Metric Response Theorem Or No-go",
        "",
        "**Status:** partial theorem, not a no-go and not a claim. The candidate parent field equation gives a non-circular weak-field residual Poisson lane, so `C_metric` can be factorised rather than guessed.",
        "",
        "**Main result:** if the residual Poisson source obeys `||S_res|| <= C_res E_GK_bound`, then the local metric residual obeys `||delta g_00||_obs <= C_metric E_GK_bound` with `C_metric=(2/c^2) C_obs C_Green C_res`. The missing work is now `C_res`, `C_Green`, `C_obs`, and source normalization, not vague coupling fog.",
        "",
        "## Source Register",
        markdown_table(data["sources"], ["source_id", "source_path", "exists", "missing_needles", "source_pass", "role"]),
        "",
        "## Theorem Attempt",
        markdown_table(data["theorems"], ["theorem_id", "step", "formula", "result", "status", "missing_for_claim", "claim_allowed"]),
        "",
        "## C_metric Factorisation",
        markdown_table(data["factors"], ["factor_id", "symbol", "definition", "depends_on", "status", "units_role", "valid_for_claim"]),
        "",
        "## Blocker Ledger",
        markdown_table(data["blockers"], ["blocker_id", "missing_object", "why_it_blocks", "next_action", "valid_for_claim"]),
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
        "theorems": theorem_attempt_rows(),
        "factors": cmetric_factorisation_rows(),
        "blockers": blocker_rows(),
        "gates": claim_gate_rows(),
        "decisions": decision_rows(),
        "next": next_target_rows(),
    }
    write_csv(OUTPUTS["source_register"], data["sources"])
    write_csv(OUTPUTS["theorem_attempt"], data["theorems"])
    write_csv(OUTPUTS["cmetric_factorisation"], data["factors"])
    write_csv(OUTPUTS["blocker_ledger"], data["blockers"])
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
