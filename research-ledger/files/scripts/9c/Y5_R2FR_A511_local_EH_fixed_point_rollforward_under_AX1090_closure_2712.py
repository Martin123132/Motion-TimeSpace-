from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CHECKPOINT = "2712"
BRANCH_ID = "Y5_R2FR_A511_LOCAL_EH_FIXED_POINT_ROLLFORWARD_UNDER_AX1090_CLOSURE_2712"
START_UTC = datetime.now(timezone.utc)

ROOT = Path(__file__).resolve().parents[1]
SOURCE_INTAKE = ROOT / "source-intake"
RESIDUALS = SOURCE_INTAKE / "mts_residuals"
LOCAL_BOUNDS = SOURCE_INTAKE / "local_bounds"
SOURCE_WEIGHT = SOURCE_INTAKE / "source-weight"
RAB_QUEUE = SOURCE_INTAKE / "rab-sector" / "acquisition-queue"
FORMALIZATION_WORKBENCH = ROOT.parent / "formalization-workbench"

DOC_PATH = ROOT / "2712-Y5-R2FR-A511-local-EH-fixed-point-rollforward-under-AX1090-closure.md"

OUTPUTS = {
    "source_register": RESIDUALS / "P8_Y5_R2FR_2712_SOURCE_REGISTER.csv",
    "a511_rollforward_spine": RESIDUALS / "P8_Y5_R2FR_2712_A511_ROLLFORWARD_SPINE.csv",
    "qloc_deltak_status": RESIDUALS / "P8_Y5_R2FR_2712_QLOC_DELTAK_STATUS.csv",
    "component_progress_ledger": RESIDUALS / "P8_Y5_R2FR_2712_COMPONENT_PROGRESS_LEDGER.csv",
    "current_blocker_stack": RESIDUALS / "P8_Y5_R2FR_2712_CURRENT_BLOCKER_STACK.csv",
    "claim_gates": RESIDUALS / "P8_Y5_R2FR_2712_CLAIM_GATES.csv",
    "decision_ledger": RESIDUALS / "P8_Y5_R2FR_2712_DECISION_LEDGER.csv",
    "next_target": RESIDUALS / "P8_Y5_R2FR_2712_NEXT_TARGET.csv",
    "project_status": RESIDUALS / "P8_Y5_R2FR_2712_PROJECT_STATUS_SNAPSHOT.csv",
    "branch_copies": RESIDUALS / "P8_Y5_R2FR_2712_BRANCH_COPIES.csv",
    "validation": RESIDUALS / f"P8_Y5_BRR545_{CHECKPOINT}_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "local_eh_gate": LOCAL_BOUNDS / "A511_local_EH_fixed_point_rollforward_2712_NONCLAIM.csv",
    "deltak_gate": SOURCE_WEIGHT / "DeltaK_component_gate_2712_NONCLAIM.csv",
    "rab_next": RAB_QUEUE / "JR2712_KL00_AMPLITUDE_OR_KMETRIC_DERIVATIVE_NEXT.csv",
}

SOURCE_SPECS: list[dict[str, Any]] = [
    {
        "source_id": "SRC2712_2711_AX1090_CLOSURE",
        "relative_path": "2711-Y5-R2FR-AX1090-parent-object-derivation-from-MTS-primitives-or-explicit-closure.md",
        "required_needles": ["AX1090_0_LC", "NEXT2711_0_selected", "VAL2711_OVERALL"],
        "purpose": "imports the explicit parent-object closure bridge and A511 rollforward target",
    },
    {
        "source_id": "SRC2712_511_A511_CONTRACT",
        "relative_path": "511-minimal-parent-action-local-GR-fixed-point-ansatz.md",
        "required_needles": ["A511_0_EH_core", "FP511_1_double_zero_nonEH_coupling", "D511_1"],
        "purpose": "imports the minimal local EH fixed-point contract and double-zero/mass-gap route",
    },
    {
        "source_id": "SRC2712_1277_EH_INHERITANCE",
        "relative_path": "1277-Y5-R10-RAB-local-EH-fixed-point-inheritance-or-explicit-closure-runner.md",
        "required_needles": ["EH_FIXED_POINT_NOT_INHERITED", "EHI1277_8_verdict", "APL1277_0_extra_silence"],
        "purpose": "imports the blocked A511 EH-inheritance audit and priority ladder",
    },
    {
        "source_id": "SRC2712_1279_EXTRA_SILENCE",
        "relative_path": "1279-Y5-R10-RAB-A511-extra-sector-silence-double-zero-or-residual-vector.md",
        "required_needles": ["EXTRA_SILENCE_NOT_CLOSED", "XRV1279_2_GK_q_loc", "NEXT1279_0_1280"],
        "purpose": "imports the extra-sector residual vector and GK/q_loc blocker",
    },
    {
        "source_id": "SRC2712_1283_PLOC_PROGRESS",
        "relative_path": "1283-Y5-R10-RAB-q_loc-profile-source-fill-or-P_loc-projector-owner.md",
        "required_needles": ["PLOC_OWNER_NOT_CLOSED_BUT_BOUNDABLE", "QPF1283_1_Gamma_eff", "NEXT1283_0_1284"],
        "purpose": "imports the projector identity/bound progress and Gamma/Khat owner target",
    },
    {
        "source_id": "SRC2712_1284_DELTAK_SPLIT",
        "relative_path": "1284-Y5-R10-RAB-Gamma-eff-Khat-owner-extraction-or-DeltaK-residual-ledger.md",
        "required_needles": ["K_hat = K_metric[Gamma_eff] + Delta_K", "DELTAK_RETAINED_SYMBOLIC_RESIDUAL", "NEXT1284_0_1285"],
        "purpose": "imports the Ward-owned plus DeltaK split",
    },
    {
        "source_id": "SRC2712_1285_CONJUGACY",
        "relative_path": "1285-Y5-R10-RAB-parent-response-displacement-conjugacy-or-DeltaK-bound-row.md",
        "required_needles": ["CONJUGACY_NOT_CONSTRUCTED", "DKB1285_0_DeltaK_divergence_bound_template", "NEXT1285_0_1286"],
        "purpose": "imports the failed parent response/displacement conjugacy and DeltaK bound template",
    },
    {
        "source_id": "SRC2712_1286_GAMMA_ROW",
        "relative_path": "1286-Y5-R10-RAB-first-DeltaK-component-profile-or-response-field-row.md",
        "required_needles": ["RFR1286_0_Gamma_memory_scalar_projection", "DELTAK_COMPONENT_NOT_FILLABLE_YET", "NEXT1286_0_1287"],
        "purpose": "imports the first source-backed nonclaim Gamma_eff scalar row",
    },
    {
        "source_id": "SRC2712_1287_KHAT_COMPONENT",
        "relative_path": "1287-Y5-R10-RAB-Khat-tracefree-longitudinal-first-component-or-Kmetric-variation.md",
        "required_needles": ["KTC1287_0_flat_Ricci_scalar_KL00", "KMC1287_0_volume_metric_response", "DELTAK_00_NOT_COMPUTABLE_YET", "NEXT1287_0_1288"],
        "purpose": "imports the first formal Khat tensor component and Kmetric volume subpiece",
    },
]


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def as_bool(value: bool) -> str:
    return "true" if value else "false"


def path_for(relative_path: str) -> Path:
    return ROOT / relative_path


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"Refusing to write empty CSV: {path}")
    fieldnames = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def parse_csv(path: Path) -> tuple[bool, int, str]:
    try:
        with path.open(newline="", encoding="utf-8") as handle:
            reader = csv.DictReader(handle)
            rows = list(reader)
            if not reader.fieldnames:
                return False, 0, "missing_header"
            return True, len(rows), "parsed"
    except Exception as exc:
        return False, 0, f"{type(exc).__name__}: {exc}"


def markdown_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "_No rows._"
    headers = list(rows[0].keys())
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    for row in rows:
        cells = [str(row.get(header, "")).replace("|", "\\|").replace("\n", "<br>") for header in headers]
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for spec in SOURCE_SPECS:
        path = path_for(spec["relative_path"])
        text = read_text(path)
        needles = list(spec["required_needles"])
        found = [needle for needle in needles if needle in text]
        missing = [needle for needle in needles if needle not in text]
        rows.append(
            {
                "source_id": spec["source_id"],
                "relative_path": spec["relative_path"],
                "absolute_path": str(path),
                "exists": as_bool(path.exists()),
                "required_needles": ";".join(needles),
                "found_needles": ";".join(found),
                "missing_needles": ";".join(missing),
                "purpose": spec["purpose"],
                "valid_for_claim": "false",
                "timestamp_utc": stamp(),
            }
        )
    return rows


def a511_rollforward_spine_rows() -> list[dict[str, Any]]:
    return [
        {
            "spine_id": "A511R2712_0_AX1090_bridge",
            "object": "AX1090_0_LC",
            "current_status": "EXPLICIT_CLOSURE_BRIDGE_NOT_PROOF",
            "what_it_allows": "organize A511 local EH fixed-point proof attempts without hiding the parent-object assumption",
            "what_it_does_not_allow": "local-GR/Newton/PPN/R10/WEP claim",
            "source_anchor": "2711 AX1090_0_LC",
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        },
        {
            "spine_id": "A511R2712_1_minimal_contract",
            "object": "A511_0..A511_6",
            "current_status": "COHERENT_CONTRACT_NOT_PARENT_SIGNED",
            "what_it_allows": "state the exact EH core, kappa, matter, extra-silence, projector, boundary, and readout clauses needed for GR reduction",
            "what_it_does_not_allow": "import EH merely because the action scaffold contains an EH block",
            "source_anchor": "511 and 1277",
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        },
        {
            "spine_id": "A511R2712_2_extra_silence",
            "object": "A511_3_extra_field_silence",
            "current_status": "BLOCKED_BY_GK_QLOC_AND_RESIDUAL_VECTOR",
            "what_it_allows": "retain explicit extra-sector residuals instead of hiding them behind closure",
            "what_it_does_not_allow": "EH fixed-point inheritance",
            "source_anchor": "1279 EXTRA_SILENCE_NOT_CLOSED",
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        },
        {
            "spine_id": "A511R2712_3_Ploc_progress",
            "object": "P_loc",
            "current_status": "BOUNDABLE_NOT_ZERO",
            "what_it_allows": "use projector identities and finite-domain curvature/splitting bounds once V^nu is sourced",
            "what_it_does_not_allow": "set q_loc to zero by projector label or quotient verticality alone",
            "source_anchor": "1283 PLOC_OWNER_NOT_CLOSED_BUT_BOUNDABLE",
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        },
        {
            "spine_id": "A511R2712_4_Gamma_scalar",
            "object": "Gamma_eff",
            "current_status": "FIRST_SOURCE_BACKED_FORMULA_SHAPE_NONCLAIM",
            "what_it_allows": "use Gamma_eff=L_cg^-2 F(m) and its gradient identity as scalar input to future Kmetric/q_loc work",
            "what_it_does_not_allow": "score q_loc or compute Delta_K without Khat and full Kmetric",
            "source_anchor": "1286 RFR1286_0_Gamma_memory_scalar_projection",
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        },
        {
            "spine_id": "A511R2712_5_Khat_first_component",
            "object": "K_L^{00}",
            "current_status": "FIRST_FORMAL_KHAT_COMPONENT_NONCLAIM",
            "what_it_allows": "stage an amplitude/response budget for a trace-free longitudinal tensor component",
            "what_it_does_not_allow": "declare current-MTS Khat matched or Delta_K^{00} computed",
            "source_anchor": "1287 KTC1287_0_flat_Ricci_scalar_KL00",
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        },
        {
            "spine_id": "A511R2712_6_verdict",
            "object": "A511 local EH fixed point",
            "current_status": "NOT_INHERITED_BUT_MORE_LOCALIZED",
            "what_it_allows": "move from broad A511 worries to a concrete KL00 amplitude/Kmetric derivative gate",
            "what_it_does_not_allow": "GR/Newton/PPN claim",
            "source_anchor": "2712 synthesis",
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        },
    ]


def qloc_deltak_status_rows() -> list[dict[str, Any]]:
    return [
        {
            "status_id": "QDK2712_0_vector_shell",
            "object": "q_loc^nu",
            "equation": "q_loc^nu=P_loc(nabla^nu Gamma_eff-nabla_mu K_hat^{mu nu})",
            "current_status": "FORMULA_SHELL_ONLY",
            "blocking_gap": "full Khat and Kmetric comparison remain missing",
            "next_repair": "complete KL00 amplitude/response row or Kmetric derivative/domain/boundary term",
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        },
        {
            "status_id": "QDK2712_1_ward_split",
            "object": "Ward-owned piece",
            "equation": "K_hat=K_metric[Gamma_eff]+Delta_K; T_metric^{mu nu}=Gamma_eff g^{mu nu}-K_metric^{mu nu}",
            "current_status": "STRUCTURAL_SPLIT_WRITTEN",
            "blocking_gap": "Ward piece needs action/Euler/source-zero/boundary gates",
            "next_repair": "keep Ward piece separate from Delta_K residual branch",
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        },
        {
            "status_id": "QDK2712_2_DeltaK",
            "object": "Delta_K^{mu nu}",
            "equation": "Delta_K^{mu nu}=K_hat^{mu nu}-K_metric^{mu nu}[Gamma_eff]",
            "current_status": "DELTAK_00_NOT_COMPUTABLE_YET",
            "blocking_gap": "formal KL00 row exists and Kmetric volume subpiece exists, but full Kmetric/current-Khat match is missing",
            "next_repair": "build KL00 amplitude response or compute Kmetric derivative/domain/boundary terms",
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        },
        {
            "status_id": "QDK2712_3_EH_impact",
            "object": "A511 local EH inheritance",
            "equation": "EH inheritance requires q_loc, Delta_K, extra stress, source, boundary, matter, and readout gates silent or bounded",
            "current_status": "LOCAL_EH_STILL_BLOCKED",
            "blocking_gap": "Delta_K and KL00 response are not bounded; q_loc profile remains nonclaim",
            "next_repair": "no EH promotion until component response/bound rows exist",
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        },
    ]


def component_progress_ledger_rows() -> list[dict[str, Any]]:
    return [
        {
            "component_id": "COMP2712_0_Gamma_eff_scalar",
            "component": "Gamma_eff=L_cg^-2 F(m)",
            "source": "1286 RFR1286_0",
            "progress": "first response-field scalar formula shape and gradient identity are source-backed",
            "remaining_debt": "F units, F_prime values, m/L_cg profiles, local domain, support powers, boundary decay",
            "claim_effect": "nonclaim input row only",
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        },
        {
            "component_id": "COMP2712_1_KL00",
            "component": "K_L^{00}=2 nabla^0 nabla^0 phi - (1/2) g^{00} Box phi",
            "source": "1287 KTC1287_0",
            "progress": "first formal trace-free longitudinal Khat component exists",
            "remaining_debt": "parent origin for phi/A^nu, Green inverse, boundary conditions, amplitude, domain classifier, current-MTS Khat match",
            "claim_effect": "formal nonclaim tensor row only",
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        },
        {
            "component_id": "COMP2712_2_Kmetric_volume",
            "component": "Kmetric volume subpiece",
            "source": "1287 KMC1287_0",
            "progress": "first Kmetric metric-proportional volume contribution is staged",
            "remaining_debt": "derivative terms, projector/domain terms, boundary/reference terms, G_AB dependence, comparison to Khat",
            "claim_effect": "subpiece only; Delta_K cannot be computed",
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        },
        {
            "component_id": "COMP2712_3_DeltaK00",
            "component": "Delta_K^{00}",
            "source": "1287 DKS1287_2",
            "progress": "comparison target is named",
            "remaining_debt": "full Kmetric^{00} and current-MTS Khat^{00} matching",
            "claim_effect": "not computable yet",
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        },
    ]


def current_blocker_stack_rows() -> list[dict[str, Any]]:
    return [
        {
            "rank": "1",
            "blocker_id": "BLK2712_0_KL00_amplitude_response",
            "blocker": "K_L^{00} amplitude/response is not bounded",
            "why_it_matters": "a divergence-cancelling tensor can still gravitate and fail Newton/PPN",
            "repair": "stage source-backed amplitude, units, domain, and PPN/Newton response row",
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        },
        {
            "rank": "2",
            "blocker_id": "BLK2712_1_Kmetric_derivative",
            "blocker": "Kmetric[Gamma_eff] derivative/domain/boundary terms missing",
            "why_it_matters": "Delta_K cannot be computed from volume term alone",
            "repair": "compute first derivative/domain/boundary variation term from Gamma_eff=L_cg^-2 F(m)",
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        },
        {
            "rank": "3",
            "blocker_id": "BLK2712_2_current_Khat_match",
            "blocker": "formal KL00 component is not signed as current-MTS Khat",
            "why_it_matters": "candidate tensor could be a compensator branch rather than the physical current-MTS tensor",
            "repair": "derive parent origin or source equation for KL branch",
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        },
        {
            "rank": "4",
            "blocker_id": "BLK2712_3_A511_EH_inheritance",
            "blocker": "A511 remains non-inherited",
            "why_it_matters": "GR/Newton reduction requires every extra/source/readout/boundary residual silent or bounded",
            "repair": "keep local EH branch blocked until q_loc/DeltaK and remaining A511 lanes close",
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        },
    ]


def claim_gates_rows() -> list[dict[str, Any]]:
    gates = [
        ("CG2712_0_A511_EH_fixed_point", "A511 local EH fixed point inherited", "BLOCKED", "KL00/DeltaK/q_loc and other A511 residual lanes remain unsigned"),
        ("CG2712_1_q_loc_zero", "q_loc^nu parent-zero", "BLOCKED", "Delta_K^{00} not computable and Ward-owned branch not closed"),
        ("CG2712_2_DeltaK_bound", "Delta_K component bound live", "BLOCKED", "KL00 amplitude/response or full Kmetric derivative term missing"),
        ("CG2712_3_local_GR_Newton_PPN", "local GR/Newton/PPN claim", "BLOCKED", "A511 inheritance and residual bounds not closed"),
        ("CG2712_4_public_or_github", "public/GitHub action", "BLOCKED", "private checkpoint only"),
    ]
    return [
        {
            "gate_id": gate_id,
            "claim": claim,
            "current_status": status,
            "reason": reason,
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        }
        for gate_id, claim, status, reason in gates
    ]


def decision_ledger_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC2712_0_A511_result",
            "decision": "Do not promote A511 local EH fixed point under AX1090_0_LC.",
            "because": "closure labels the parent object but does not sign A511 blocks, extra-sector silence, q_loc, DeltaK, readout, boundary, or matter descent.",
            "next_action": "work the concrete KL00/Kmetric derivative gate instead of retreading broad EH inheritance.",
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        },
        {
            "decision_id": "DEC2712_1_progress_result",
            "decision": "Carry forward two real nonclaim component gains.",
            "because": "Gamma_eff scalar row and K_L^{00} formal tensor row are now sourced/formal enough to attack amplitude/response and Kmetric terms.",
            "next_action": "turn component rows into bounded residuals or compute missing variation terms.",
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        },
        {
            "decision_id": "DEC2712_2_next_route",
            "decision": "Select KL00 amplitude/response row or Kmetric derivative/domain term as next R2FR target.",
            "because": "Delta_K^{00} cannot be computed until one of those tensor-side debts is filled.",
            "next_action": "create 2713 as the current-spine counterpart of 1288.",
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT2712_0_selected",
            "status": "selected_primary",
            "target_doc": "2713-Y5-R2FR-KL00-amplitude-response-or-Kmetric-derivative-under-AX1090-closure.md",
            "target_script": "scripts/Y5_R2FR_KL00_amplitude_response_or_Kmetric_derivative_under_AX1090_closure_2713.py",
            "purpose": "use the filled K_L^{00} formal component to stage a Newton/PPN amplitude-response bound, or compute the first derivative/domain/boundary term in Kmetric[Gamma_eff]",
            "acceptance_condition": "K_L^{00} gets a source-backed nonclaim amplitude/response row, or Kmetric derivative/domain terms are explicitly blocked with required inputs; no DeltaK/q_loc/local-GR claim",
            "forbidden_shortcuts": "treat flat divergence cancellation as GR recovery; compute Delta_K without full Kmetric/current-Khat comparison; use closure to claim local GR; edit formalization-workbench; GitHub action",
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        }
    ]


def project_status_rows() -> list[dict[str, Any]]:
    return [
        {
            "status_id": "STAT2712_0_overall",
            "area": "local GR route",
            "status": "blocked but sharper",
            "meaning": "we are no longer arguing about a vague plateau; the live wall is tensor-side Delta_K/Kmetric/Khat response",
            "risk": "the component rows remain nonclaim until amplitude, units, domains, and response maps exist",
            "next_action": "quantify KL00 or compute Kmetric derivative/domain terms",
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        },
        {
            "status_id": "STAT2712_1_good_news",
            "area": "derivation spine",
            "status": "component-level traction",
            "meaning": "Gamma_eff scalar and a first formal Khat component are on the table with source anchors",
            "risk": "source anchors are not full parent signatures",
            "next_action": "turn formula shapes into bounded or zeroed residual rows",
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        },
        {
            "status_id": "STAT2712_2_claim_ceiling",
            "area": "claims",
            "status": "no local-GR/Newton/PPN claim",
            "meaning": "A511 EH fixed point is not inherited under closure alone",
            "risk": "overclaiming the formal KL tensor would be a false win",
            "next_action": "keep all branches nonclaim until the component gates close",
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        },
    ]


def branch_copy_rows() -> list[dict[str, Any]]:
    return [
        {
            "copy_id": key,
            "path": str(path),
            "relative_path": str(path.relative_to(ROOT)),
            "exists_after_run": as_bool(path.exists()),
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        }
        for key, path in BRANCH_OUTPUTS.items()
    ]


def formalization_recent_change_count() -> int:
    if not FORMALIZATION_WORKBENCH.exists():
        return 0
    threshold = START_UTC.timestamp() - 2.0
    changed_count = 0
    for path in FORMALIZATION_WORKBENCH.rglob("*"):
        try:
            if path.is_file() and path.stat().st_mtime >= threshold:
                changed_count += 1
        except OSError:
            continue
    return changed_count


def validate(generated_paths: dict[str, Path], rows_by_name: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    def add(check_id: str, passed: bool, detail: str) -> None:
        rows.append({"check_id": check_id, "passed": as_bool(passed), "detail": detail, "timestamp_utc": stamp()})

    sources = rows_by_name["source_register"]
    add("VAL2712_0_sources_exist", all(row["exists"] == "true" for row in sources), "all cited local source paths exist")
    add("VAL2712_1_needles_found", all(not row["missing_needles"] for row in sources), "all required source needles were found")

    spine = rows_by_name["a511_rollforward_spine"]
    add("VAL2712_2_A511_not_inherited", any(row["spine_id"] == "A511R2712_6_verdict" and row["current_status"] == "NOT_INHERITED_BUT_MORE_LOCALIZED" for row in spine), "A511 verdict is blocked but localized")
    add("VAL2712_3_nonclaim_spine", all(row["valid_for_claim"] == "false" and row["claim_allowed"] == "false" for row in spine), "rollforward spine remains nonclaim")

    qloc = rows_by_name["qloc_deltak_status"]
    add("VAL2712_4_DeltaK_not_computable", any(row["status_id"] == "QDK2712_2_DeltaK" and row["current_status"] == "DELTAK_00_NOT_COMPUTABLE_YET" for row in qloc), "DeltaK00 remains not computable")

    components = rows_by_name["component_progress_ledger"]
    add("VAL2712_5_component_progress", any(row["component_id"] == "COMP2712_0_Gamma_eff_scalar" for row in components) and any(row["component_id"] == "COMP2712_1_KL00" for row in components), "Gamma scalar and KL00 component gains are recorded")
    add("VAL2712_6_blocker_stack", any(row["blocker_id"] == "BLK2712_0_KL00_amplitude_response" for row in rows_by_name["current_blocker_stack"]), "KL00 amplitude/response selected as top blocker")
    add("VAL2712_7_claims_blocked", all(row["valid_for_claim"] == "false" and row["claim_allowed"] == "false" for row in rows_by_name["claim_gates"]), "all claim gates remain blocked")
    add("VAL2712_8_next_2713", any(row["next_id"] == "NEXT2712_0_selected" and "2713" in row["target_doc"] for row in rows_by_name["next_target"]), "2713 target selected")
    add("VAL2712_9_no_formalization_outputs", not any("formalization-workbench" in str(path).lower() for path in generated_paths.values()), "no output path points into formalization-workbench")
    add("VAL2712_10_no_formalization_recent_changes", formalization_recent_change_count() == 0, f"formalization_recent_changed_count={formalization_recent_change_count()}")
    add("VAL2712_11_no_github_outputs", not any(".git" in str(path).lower() or "github" in str(path).lower() for path in generated_paths.values()), "no GitHub/public-output path was written")

    for key, path in generated_paths.items():
        ok, count, detail = parse_csv(path)
        add(f"VAL2712_PARSE_{key}", ok and count > 0, f"{detail}; rows={count}")

    core = [row for row in rows if not row["check_id"].startswith("VAL2712_PARSE_validation")]
    add(
        "VAL2712_OVERALL",
        all(row["passed"] == "true" for row in core),
        "2712 rolls A511 through AX1090 closure, keeps local EH inheritance blocked, records Gamma_eff and KL00 component progress, keeps DeltaK00/q_loc unclaimed, and selects KL00 amplitude/Kmetric derivative work for 2713",
    )
    return rows


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    sections = [
        ("A511 Rollforward Spine", rows_by_name["a511_rollforward_spine"]),
        ("q_loc and DeltaK Status", rows_by_name["qloc_deltak_status"]),
        ("Component Progress Ledger", rows_by_name["component_progress_ledger"]),
        ("Current Blocker Stack", rows_by_name["current_blocker_stack"]),
        ("Decision Ledger", rows_by_name["decision_ledger"]),
        ("Source Register", rows_by_name["source_register"]),
        ("Claim Gates", rows_by_name["claim_gates"]),
        ("Next Target", rows_by_name["next_target"]),
        ("Project Status", rows_by_name["project_status"]),
        ("Validation", rows_by_name["validation"]),
    ]
    lines = [
        "# 2712: A511 Local EH Fixed Point Rollforward Under AX1090 Closure",
        "",
        f"**Branch:** `{BRANCH_ID}`",
        "",
        "## Private Verdict",
        "",
        "2712 does not promote the A511 local EH fixed point. `AX1090_0_LC` lets us organize the local branch honestly, but it does not sign the A511 action blocks or make GR/Newton follow. The old A511 chain has, however, produced real narrowing: `Gamma_eff=L_cg^-2 F(m)` is now a source-backed nonclaim scalar formula shape, and a first formal trace-free longitudinal `K_L^{00}` tensor component is written.",
        "",
        "The live wall is now tensor-side: `Delta_K^{00}` is still not computable because the full `Kmetric[Gamma_eff]` derivative/domain/boundary terms and current-MTS `K_hat` match remain missing. So the next useful target is not another broad EH audit; it is `K_L^{00}` amplitude/response or the first missing `Kmetric` derivative term.",
        "",
        "## Bottom Line",
        "",
        "- A511 is still blocked as a derived local-GR route.",
        "- The blocker is sharper: `q_loc` now depends on concrete `Gamma_eff`, `K_hat`, `Kmetric`, and `Delta_K` component rows.",
        "- Real progress exists: source-backed `Gamma_eff` shape plus formal nonclaim `K_L^{00}`/Kmetric-volume rows.",
        "- No claim is allowed until amplitude, units, domains, response maps, and full tensor comparison close.",
        "",
    ]
    for title, rows in sections:
        lines.extend([f"## {title}", "", markdown_table(rows), ""])
    DOC_PATH.write_text("\n".join(lines), encoding="utf-8")


def build_rows() -> dict[str, list[dict[str, Any]]]:
    return {
        "source_register": source_register_rows(),
        "a511_rollforward_spine": a511_rollforward_spine_rows(),
        "qloc_deltak_status": qloc_deltak_status_rows(),
        "component_progress_ledger": component_progress_ledger_rows(),
        "current_blocker_stack": current_blocker_stack_rows(),
        "claim_gates": claim_gates_rows(),
        "decision_ledger": decision_ledger_rows(),
        "next_target": next_target_rows(),
        "project_status": project_status_rows(),
    }


def main() -> None:
    rows_by_name = build_rows()
    for name, path in OUTPUTS.items():
        if name in {"validation", "branch_copies"}:
            continue
        write_csv(path, rows_by_name[name])

    write_csv(BRANCH_OUTPUTS["local_eh_gate"], rows_by_name["a511_rollforward_spine"])
    write_csv(BRANCH_OUTPUTS["deltak_gate"], rows_by_name["qloc_deltak_status"])
    write_csv(BRANCH_OUTPUTS["rab_next"], rows_by_name["next_target"])

    rows_by_name["branch_copies"] = branch_copy_rows()
    write_csv(OUTPUTS["branch_copies"], rows_by_name["branch_copies"])

    generated_paths = {name: path for name, path in OUTPUTS.items() if name != "validation"}
    generated_paths.update(BRANCH_OUTPUTS)
    validation = validate(generated_paths, rows_by_name)
    rows_by_name["validation"] = validation
    write_csv(OUTPUTS["validation"], validation)

    write_doc(rows_by_name)

    print(f"wrote {DOC_PATH}")
    print(f"wrote {OUTPUTS['validation']}")
    print(f"overall={validation[-1]['passed']}")


if __name__ == "__main__":
    main()
