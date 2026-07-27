from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SCRIPT_START_UTC = datetime.now(timezone.utc)

ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
SOURCE_WEIGHT = ROOT / "source-intake" / "source-weight"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
FORMALIZATION = ROOT.parent / "formalization-workbench"

DOC = ROOT / "2719-Y5-R2FR-boundary-harmonic-nocharge-or-finite-Jeff-bound-under-AX1090-closure.md"

OUTPUTS = {
    "source_register": RESIDUALS / "P8_Y5_R2FR_2719_SOURCE_REGISTER.csv",
    "nocharge_audit": RESIDUALS / "P8_Y5_R2FR_2719_BOUNDARY_HARMONIC_NOCHARGE_AUDIT.csv",
    "theorem_attempt": RESIDUALS / "P8_Y5_R2FR_2719_NOCHARGE_THEOREM_ATTEMPT.csv",
    "finite_rows": RESIDUALS / "P8_Y5_R2FR_2719_FINITE_EBOUNDARY_EHARMONIC_ROWS_NONCLAIM.csv",
    "ejeff_update": RESIDUALS / "P8_Y5_R2FR_2719_EJEFF_UPDATE_VECTOR_NONCLAIM.csv",
    "claim_gates": RESIDUALS / "P8_Y5_R2FR_2719_CLAIM_GATES.csv",
    "blocker_stack": RESIDUALS / "P8_Y5_R2FR_2719_CURRENT_BLOCKER_STACK.csv",
    "decision_ledger": RESIDUALS / "P8_Y5_R2FR_2719_DECISION_LEDGER.csv",
    "next_target": RESIDUALS / "P8_Y5_R2FR_2719_NEXT_TARGET.csv",
    "project_snapshot": RESIDUALS / "P8_Y5_R2FR_2719_PROJECT_STATUS_SNAPSHOT.csv",
    "branch_copies": RESIDUALS / "P8_Y5_R2FR_2719_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2719_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "local_bounds": LOCAL_BOUNDS / "boundary_harmonic_Jeff_rows_2719_NONCLAIM.csv",
    "source_weight": SOURCE_WEIGHT / "Eboundary_Eharmonic_bound_vector_2719_NONCLAIM.csv",
    "next_queue": RAB_QUEUE / "JR2719_READOUT_STABILITY_OR_FINITE_JREADOUT_NEXT.csv",
}


def ts() -> str:
    return datetime.now(timezone.utc).isoformat()


def normalize(value: Any) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    if value is None:
        return ""
    return str(value)


def md_escape(value: Any) -> str:
    return normalize(value).replace("|", "\\|").replace("\n", "<br>")


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"Refusing to write empty CSV: {path}")
    fieldnames = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="raise")
        writer.writeheader()
        for row in rows:
            writer.writerow({key: normalize(row.get(key, "")) for key in fieldnames})


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    body = [
        "| " + " | ".join(md_escape(row.get(column, "")) for column in columns) + " |"
        for row in rows
    ]
    return "\n".join([header, sep, *body])


SOURCE_SPECS = [
    {
        "source_id": "SRC2719_0_2718",
        "label": "2718 J_eff source split",
        "path": ROOT / "2718-Y5-R2FR-Jeff-source-norm-split-or-ZR-theorem-zero-under-AX1090-closure.md",
        "needles": [
            "JEFF2718_2_boundary",
            "JEFF2718_3_harmonic",
            "BND2718_2_remaining_local_vacuum",
            "NEXT2718_0_selected",
            "VAL2718_OVERALL",
        ],
        "use": "handoff identifying boundary/harmonic as dominant remaining local-vacuum source pieces",
    },
    {
        "source_id": "SRC2719_1_05_reciprocity",
        "label": "05 reciprocity theorem obstruction",
        "path": ROOT / "05-reciprocity-theorem-attempt.md",
        "needles": [
            "`Q_R` is a conserved reciprocal charge.",
            "Asymptotic flatness alone does not kill `Q_R`.",
            "Q_R = integral J_R dr = 0",
        ],
        "use": "prevents false no-hair proof from asymptotic flatness alone",
    },
    {
        "source_id": "SRC2719_2_1567_contract",
        "label": "1567 boundary/readout protection clauses",
        "path": ROOT / "1567-Y5-RAB-parent-protection-contract-or-live-finite-ZR-source-acquisition.md",
        "needles": [
            "CON1567_3_boundary_functor",
            "CON1567_4_readout_closure",
            "ACQ1567_4_BR",
        ],
        "use": "parent clause needed for boundary/corner silence",
    },
    {
        "source_id": "SRC2719_3_1873_boundary_contract",
        "label": "1873 boundary silence parent contract",
        "path": ROOT / "1873-Y5-R2FR-boundary-silence-parent-contract-for-CR-zero-or-residual-closure.md",
        "needles": [
            "BSC1873_5_boundary_silence",
            "PROOF1873_2_boundary_silence",
            "UNS1873_3_boundary",
            "VAL1873_OVERALL",
        ],
        "use": "conditional Pi_R/Q_R/C_R zero chain and unsigned-clause warning",
    },
    {
        "source_id": "SRC2719_4_2062_boundary_corner",
        "label": "2062 boundary/corner R_AB silence",
        "path": ROOT / "2062-Y5-R2FR-boundary-corner-RAB-silence-or-finite-PiR-bound-row.md",
        "needles": [
            "BGA2062_1_natural_variation",
            "BGA2062_2_fixed_boundary_rejection",
            "BSP2062_0_theorem_statement",
            "VAL2062_OVERALL",
        ],
        "use": "natural-boundary route and fixed-boundary rejection",
    },
    {
        "source_id": "SRC2719_5_2063_object_exhaustion",
        "label": "2063 boundary object exhaustion",
        "path": ROOT / "2063-Y5-R2FR-boundary-object-exhaustion-or-PiR-component-bound-intake.md",
        "needles": [
            "BOE2063_0_theorem_contract",
            "BOE2063_3_countermodel_boundary",
            "PCI2063_1_boundary_bound",
            "VAL2063_OVERALL",
        ],
        "use": "boundary object-exhaustion theorem shape and finite Pi_R component rows",
    },
    {
        "source_id": "SRC2719_6_2478_green",
        "label": "2478 Green/domain harmonic blockers",
        "path": ROOT / "2478-Y5-R2FR-residual-source-norm-and-Green-bound-certificate.md",
        "needles": [
            "GRN2478_0_poisson_inverse",
            "GRN2478_1_sup_kernel_bound",
            "BLK2478_2_domain_geometry",
            "C_GREEN_SYMBOLIC_ONLY",
        ],
        "use": "harmonic zero-mode/domain package and boundary-harmonic bound form",
    },
]


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for spec in SOURCE_SPECS:
        path = Path(spec["path"])
        text = read_text(path)
        missing = [needle for needle in spec["needles"] if needle not in text]
        rows.append(
            {
                "source_id": spec["source_id"],
                "label": spec["label"],
                "path": str(path),
                "exists": path.exists(),
                "required_needles_found": not missing,
                "missing_needles": ";".join(missing),
                "use": spec["use"],
                "claim_credit": False,
                "timestamp_utc": ts(),
            }
        )
    return rows


def nocharge_audit_rows() -> list[dict[str, Any]]:
    return [
        {
            "audit_id": "NCA2719_0_asymptotic_flatness",
            "target": "kill exterior reciprocal charge Q_R",
            "attempt": "use R_AB(infinity)=0 or finite energy alone",
            "verdict": "REJECTED_AS_INSUFFICIENT",
            "reason": "05 shows W R_AB'=Q_R and R_AB~Q_R/r can survive asymptotic flatness unless Q_R is separately zero",
            "claim_allowed": False,
            "next_requirement": "natural boundary/no-charge theorem or finite Q_R/Pi_R bound",
            "timestamp_utc": ts(),
        },
        {
            "audit_id": "NCA2719_1_fixed_boundary",
            "target": "impose fixed R_AB boundary data",
            "attempt": "Dirichlet/fixed R_AB on boundary",
            "verdict": "REJECTED_AS_NO_HAIR_PROOF",
            "reason": "fixed data removes the boundary variation equation and can hide nonzero reciprocal hair unless the fixed zero value is parent-derived",
            "claim_allowed": False,
            "next_requirement": "free natural R_AB variation plus parent boundary object exhaustion",
            "timestamp_utc": ts(),
        },
        {
            "audit_id": "NCA2719_2_natural_boundary",
            "target": "Pi_R=0 and therefore Q_R=0",
            "attempt": "free R_AB variation with no R_AB boundary/corner functional",
            "verdict": "EXACT_IF_PARENT_BOUNDARY_GRAMMAR_SIGNED",
            "reason": "2062/2063 theorem shape is clean, but the parent boundary/corner object list is not exhaustive in the current corpus",
            "claim_allowed": False,
            "next_requirement": "parent boundary object-exhaustion theorem or finite Pi_R components",
            "timestamp_utc": ts(),
        },
        {
            "audit_id": "NCA2719_3_harmonic_zero_mode",
            "target": "remove harmonic exterior solution",
            "attempt": "domain/gauge/falloff package with no zero modes",
            "verdict": "DOMAIN_PACKAGE_MISSING",
            "reason": "2478 requires Omega, boundary conditions and harmonic zero-mode control before the Green inverse is numeric or no-hair",
            "claim_allowed": False,
            "next_requirement": "domain cohomology and boundary-condition certificate or finite harmonic amplitude row",
            "timestamp_utc": ts(),
        },
        {
            "audit_id": "NCA2719_4_verdict",
            "target": "boundary/harmonic no-charge",
            "attempt": "combine natural boundary, object exhaustion, corner silence and harmonic-zero package",
            "verdict": "NOCHARGE_NOT_DERIVED_FINITE_ROWS_REQUIRED",
            "reason": "every clean theorem route has at least one unsigned parent/domain clause",
            "claim_allowed": False,
            "next_requirement": "finite E_boundary/E_harmonic rows feed E_Jeff",
            "timestamp_utc": ts(),
        },
    ]


def theorem_attempt_rows() -> list[dict[str, Any]]:
    return [
        {
            "theorem_id": "THM2719_0_statement",
            "statement": "If (i) R_AB has free natural boundary variation, (ii) AllowedBoundary excludes R_AB/Lambda_R functionals, (iii) corner/worldtube endpoint terms are R_AB-free or exact with zero corner charge, and (iv) the local exterior domain has no harmonic zero mode, then E_boundary=E_harmonic=0 and Q_R=0.",
            "status": "CONDITIONAL_THEOREM_ONLY",
            "missing_clause": "parent boundary object exhaustion; corner certificate; domain harmonic zero-mode package",
            "claim_allowed": False,
            "timestamp_utc": ts(),
        },
        {
            "theorem_id": "THM2719_1_boundary_variation",
            "statement": "With no B_R[R_AB] and free variation, the natural boundary equation gives Pi_R^boundary=0.",
            "status": "EXACT_IF_BOUNDARY_GRAMMAR_SIGNED",
            "missing_clause": "AllowedBoundary theorem is not parent-derived",
            "claim_allowed": False,
            "timestamp_utc": ts(),
        },
        {
            "theorem_id": "THM2719_2_corner_worldtube",
            "statement": "If corner/worldtube endpoint functionals have no R_AB argument, Pi_R^corner=0.",
            "status": "EXACT_IF_CORNER_CERTIFICATE_SIGNED",
            "missing_clause": "actual local/source worldtube surface class and corner regulator certificate",
            "claim_allowed": False,
            "timestamp_utc": ts(),
        },
        {
            "theorem_id": "THM2719_3_harmonic",
            "statement": "If the massive operator has positive M_R^2 or the massless limit has Dirichlet/natural data plus no harmonic cohomology, the homogeneous harmonic exterior mode is zero.",
            "status": "CONDITIONAL_ON_OPERATOR_AND_DOMAIN",
            "missing_clause": "M_R^2 positivity or massless zero-mode/domain proof; boundary data",
            "claim_allowed": False,
            "timestamp_utc": ts(),
        },
        {
            "theorem_id": "THM2719_4_no_cancellation",
            "statement": "Boundary, corner and harmonic pieces must vanish independently or be bounded in an absolute vector; cancellation between pieces gives no local-GR credit.",
            "status": "GUARDRAIL_ACTIVE",
            "missing_clause": "finite component bounds still absent",
            "claim_allowed": False,
            "timestamp_utc": ts(),
        },
    ]


def finite_rows() -> list[dict[str, Any]]:
    return [
        {
            "row_id": "FBH2719_0_Eboundary",
            "quantity": "E_boundary",
            "definition": "E_boundary := C_boundary * ||delta B_R/delta R_AB||_boundary",
            "feeds": "E_Jeff",
            "source_path": str(ROOT / "2063-Y5-R2FR-boundary-object-exhaustion-or-PiR-component-bound-intake.md"),
            "units_need": "boundary-current/Euler-source units conjugate to dimensionless R_AB",
            "missing": "boundary coefficient beta_R or parent object-exhaustion zero theorem; surface measure; orientation",
            "status": "SOURCE_READY_SCHEMA_NONCLAIM",
            "valid_for_claim": False,
            "timestamp_utc": ts(),
        },
        {
            "row_id": "FBH2719_1_Ecorner",
            "quantity": "E_corner",
            "definition": "E_corner := C_corner * ||Pi_R^corner||",
            "feeds": "E_Jeff",
            "source_path": str(ROOT / "2062-Y5-R2FR-boundary-corner-RAB-silence-or-finite-PiR-bound-row.md"),
            "units_need": "corner/endcap source units compatible with Pi_R^tot",
            "missing": "corner-free certificate or beta_corner bound; regulator/cutoff joint class",
            "status": "SOURCE_READY_SCHEMA_NONCLAIM",
            "valid_for_claim": False,
            "timestamp_utc": ts(),
        },
        {
            "row_id": "FBH2719_2_Eharmonic",
            "quantity": "E_harmonic",
            "definition": "E_harmonic := C_harm * harmonic_zero_mode_amplitude",
            "feeds": "E_Jeff and Green boundary/harmonic term",
            "source_path": str(ROOT / "2478-Y5-R2FR-residual-source-norm-and-Green-bound-certificate.md"),
            "units_need": "dimensionless R_AB amplitude or equivalent L_R source norm",
            "missing": "domain cohomology; boundary conditions; zero-mode projection; M_R^2 regime",
            "status": "SOURCE_READY_SCHEMA_NONCLAIM",
            "valid_for_claim": False,
            "timestamp_utc": ts(),
        },
        {
            "row_id": "FBH2719_3_Eorientation",
            "quantity": "orientation/sign/no-cancellation metadata",
            "definition": "declare Q_R=-Pi_R^tot convention, exterior normal, reference subtraction and absolute-sum rule",
            "feeds": "E_boundary+E_corner join into E_Jeff",
            "source_path": str(ROOT / "1873-Y5-R2FR-boundary-silence-parent-contract-for-CR-zero-or-residual-closure.md"),
            "units_need": "dimensionless sign/orientation metadata plus absolute norm convention",
            "missing": "worldtube orientation; reference subtraction; no-cancellation residual vector owner",
            "status": "REQUIRED_METADATA_NONCLAIM",
            "valid_for_claim": False,
            "timestamp_utc": ts(),
        },
    ]


def ejeff_update_rows() -> list[dict[str, Any]]:
    return [
        {
            "update_id": "EJ2719_0_previous",
            "formula": "E_nonmatter = E_boundary + E_harmonic + E_readout + E_shadow + E_norm",
            "status": "INHERITED_FROM_2718",
            "claim_allowed": False,
            "timestamp_utc": ts(),
        },
        {
            "update_id": "EJ2719_1_refined",
            "formula": "E_boundary_hair := E_boundary + E_corner + E_harmonic",
            "status": "REFINED_NONCLAIM_VECTOR",
            "claim_allowed": False,
            "timestamp_utc": ts(),
        },
        {
            "update_id": "EJ2719_2_green_feed",
            "formula": "||R_AB|| <= ||G_R||*(E_matter + E_boundary_hair + E_readout + E_shadow + E_norm)",
            "status": "FORMAL_GREEN_INTERFACE_ONLY",
            "claim_allowed": False,
            "timestamp_utc": ts(),
        },
        {
            "update_id": "EJ2719_3_zero_condition",
            "formula": "E_boundary_hair=0 only if boundary object-exhaustion, corner certificate and harmonic zero-mode package all close",
            "status": "ZERO_CONDITION_NOT_MET",
            "claim_allowed": False,
            "timestamp_utc": ts(),
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "GATE2719_0_boundary_nocharge",
            "claim": "E_boundary=0 and Q_R boundary charge vanishes",
            "status": "BLOCKED",
            "required_before_claim": "parent boundary object-exhaustion and natural R_AB variation",
            "claim_allowed": False,
            "timestamp_utc": ts(),
        },
        {
            "gate_id": "GATE2719_1_corner_nocharge",
            "claim": "corner/worldtube endpoint source vanishes",
            "status": "BLOCKED",
            "required_before_claim": "corner-free worldtube certificate or exact/topological corner proof",
            "claim_allowed": False,
            "timestamp_utc": ts(),
        },
        {
            "gate_id": "GATE2719_2_harmonic_zero",
            "claim": "harmonic exterior mode vanishes",
            "status": "BLOCKED",
            "required_before_claim": "domain/gauge/boundary zero-mode certificate or positive massive gap",
            "claim_allowed": False,
            "timestamp_utc": ts(),
        },
        {
            "gate_id": "GATE2719_3_local_GR",
            "claim": "local GR/Newton reduction",
            "status": "BLOCKED",
            "required_before_claim": "all E_Jeff components zero or absolutely bounded plus readout/gauge metric projection",
            "claim_allowed": False,
            "timestamp_utc": ts(),
        },
        {
            "gate_id": "GATE2719_4_public",
            "claim": "public/GitHub output",
            "status": "NOT_REQUESTED_BLOCKED_BY_PRIVATE_SCOPE",
            "required_before_claim": "explicit user request and public-safe claim audit",
            "claim_allowed": False,
            "timestamp_utc": ts(),
        },
    ]


def blocker_stack_rows() -> list[dict[str, Any]]:
    return [
        {
            "blocker_id": "BLK2719_0_boundary_object_exhaustion",
            "missing_item": "complete parent boundary generator list excluding R_AB/Lambda_R",
            "effect": "linear boundary countermodel B_R=integral beta_R R_AB remains legal",
            "best_next_attack": "parent boundary object-exhaustion theorem or beta_R finite bound",
            "claim_blocked": "boundary no-charge; local GR",
            "timestamp_utc": ts(),
        },
        {
            "blocker_id": "BLK2719_1_corner_certificate",
            "missing_item": "corner/worldtube endpoint R_AB-free certificate",
            "effect": "Pi_R^corner can source reciprocal hair even if bulk and smooth boundary are silent",
            "best_next_attack": "worldtube surface class/corner regulator certificate",
            "claim_blocked": "Q_R=0; exterior no-hair",
            "timestamp_utc": ts(),
        },
        {
            "blocker_id": "BLK2719_2_harmonic_domain",
            "missing_item": "domain cohomology / harmonic zero-mode package",
            "effect": "homogeneous exterior solution can survive source silence",
            "best_next_attack": "arena-specific Omega, BC, zero-mode projection",
            "claim_blocked": "Green numeric bound; local vacuum GR",
            "timestamp_utc": ts(),
        },
        {
            "blocker_id": "BLK2719_3_readout_next",
            "missing_item": "readout regeneration silence",
            "effect": "even zero boundary/harmonic rows would not finish E_nonmatter",
            "best_next_attack": "J_readout stability theorem or finite row",
            "claim_blocked": "PPN;clock;local GR",
            "timestamp_utc": ts(),
        },
    ]


def decision_ledger_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC2719_0_nocharge",
            "decision": "do not claim boundary/harmonic no-charge",
            "rationale": "natural-boundary theorem is exact only under unsigned parent/domain clauses",
            "allowed": True,
            "claim_credit": False,
            "timestamp_utc": ts(),
        },
        {
            "decision_id": "DEC2719_1_reject_shortcuts",
            "decision": "reject asymptotic-flatness-only and fixed-boundary proof shortcuts",
            "rationale": "both can leave or hide Q_R reciprocal hair",
            "allowed": True,
            "claim_credit": False,
            "timestamp_utc": ts(),
        },
        {
            "decision_id": "DEC2719_2_finite_rows",
            "decision": "install E_boundary/E_corner/E_harmonic rows into E_Jeff",
            "rationale": "if no-charge is not derived, the source pieces must be bounded explicitly",
            "allowed": True,
            "claim_credit": False,
            "timestamp_utc": ts(),
        },
        {
            "decision_id": "DEC2719_3_next",
            "decision": "move next to readout stability or finite J_readout",
            "rationale": "boundary/harmonic is now explicit; readout is the next live nonmatter source",
            "allowed": True,
            "claim_credit": False,
            "timestamp_utc": ts(),
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT2719_0_selected",
            "status": "selected_primary",
            "target_doc": "2720-Y5-R2FR-readout-stability-or-finite-Jreadout-bound-under-AX1090-closure.md",
            "target_script": "scripts/Y5_R2FR_readout_stability_or_finite_Jreadout_bound_under_AX1090_closure_2720.py",
            "mission": "prove readout/effective reduction cannot regenerate R_AB source or derivative terms, or create finite J_readout rows feeding E_Jeff",
            "acceptance": "readout regeneration is theorem-zero, or J_readout finite source rows become source-ready nonclaim inputs for the 2717 Green bound",
            "forbidden": "score R10/PPN; hide readout in boundary/matter; use fitted GM; edit formalization-workbench; GitHub action",
            "selected": True,
            "claim_allowed": False,
            "timestamp_utc": ts(),
        }
    ]


def project_snapshot_rows() -> list[dict[str, Any]]:
    return [
        {
            "snapshot_id": "SNAP2719_0_status",
            "sector": "boundary/harmonic local-vacuum branch",
            "state": "no-charge theorem shape is exact but unsigned; finite E_boundary/E_corner/E_harmonic rows installed",
            "confidence": "structural progress, not claim",
            "next_need": "readout stability and source normalization",
            "timestamp_utc": ts(),
        },
        {
            "snapshot_id": "SNAP2719_1_best_route",
            "sector": "derivation",
            "state": "natural boundary plus object exhaustion is the clean no-hair route; fixed boundary is rejected",
            "confidence": "high as proof strategy",
            "next_need": "parent boundary generator theorem",
            "timestamp_utc": ts(),
        },
        {
            "snapshot_id": "SNAP2719_2_empirical",
            "sector": "testing readiness",
            "state": "still not score-ready; boundary/harmonic rows are symbolic nonclaim source slots",
            "confidence": "blocked but sharper",
            "next_need": "numeric/source-backed component norms and arena domain package",
            "timestamp_utc": ts(),
        },
    ]


def branch_copy_rows() -> list[dict[str, Any]]:
    return [
        {
            "copy_id": "COPY2719_0_local_bounds",
            "source_table": "P8_Y5_R2FR_2719_FINITE_EBOUNDARY_EHARMONIC_ROWS_NONCLAIM.csv",
            "copy_path": str(BRANCH_OUTPUTS["local_bounds"]),
            "purpose": "quarantine boundary/harmonic local-bound rows as nonclaim",
            "exists": BRANCH_OUTPUTS["local_bounds"].exists(),
            "valid_for_claim": False,
            "timestamp_utc": ts(),
        },
        {
            "copy_id": "COPY2719_1_source_weight",
            "source_table": "P8_Y5_R2FR_2719_EJEFF_UPDATE_VECTOR_NONCLAIM.csv",
            "copy_path": str(BRANCH_OUTPUTS["source_weight"]),
            "purpose": "quarantine E_Jeff update vector as nonclaim",
            "exists": BRANCH_OUTPUTS["source_weight"].exists(),
            "valid_for_claim": False,
            "timestamp_utc": ts(),
        },
        {
            "copy_id": "COPY2719_2_next_queue",
            "source_table": "P8_Y5_R2FR_2719_NEXT_TARGET.csv",
            "copy_path": str(BRANCH_OUTPUTS["next_queue"]),
            "purpose": "queue 2720 without touching formalization-workbench",
            "exists": BRANCH_OUTPUTS["next_queue"].exists(),
            "valid_for_claim": False,
            "timestamp_utc": ts(),
        },
    ]


def csv_parse_details(paths: list[Path]) -> tuple[bool, str]:
    details: list[str] = []
    ok = True
    for path in paths:
        try:
            with path.open("r", newline="", encoding="utf-8") as handle:
                rows = list(csv.DictReader(handle))
            if not rows:
                ok = False
                details.append(f"{path.name}:0 rows")
            else:
                details.append(f"{path.name}:{len(rows)}:parsed")
        except Exception as exc:
            ok = False
            details.append(f"{path.name}:ERROR:{exc}")
    return ok, "; ".join(details)


def formalization_recent_changed_count() -> int:
    if not FORMALIZATION.exists():
        return 0
    count = 0
    for path in FORMALIZATION.rglob("*"):
        if path.is_file():
            modified = datetime.fromtimestamp(path.stat().st_mtime, timezone.utc)
            if modified >= SCRIPT_START_UTC:
                count += 1
    return count


def validation_rows(
    sources: list[dict[str, Any]],
    nocharge: list[dict[str, Any]],
    theorem: list[dict[str, Any]],
    finite: list[dict[str, Any]],
    ejeff: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    branches: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    csv_paths = [
        OUTPUTS["source_register"],
        OUTPUTS["nocharge_audit"],
        OUTPUTS["theorem_attempt"],
        OUTPUTS["finite_rows"],
        OUTPUTS["ejeff_update"],
        OUTPUTS["claim_gates"],
        OUTPUTS["blocker_stack"],
        OUTPUTS["decision_ledger"],
        OUTPUTS["next_target"],
        OUTPUTS["project_snapshot"],
        OUTPUTS["branch_copies"],
        *BRANCH_OUTPUTS.values(),
    ]
    csv_ok, csv_detail = csv_parse_details(csv_paths)
    source_ok = all(row["exists"] and row["required_needles_found"] for row in sources)
    nocharge_false = all(row["claim_allowed"] is False for row in nocharge)
    theorem_false = all(row["claim_allowed"] is False for row in theorem)
    finite_nonclaim = all(row["valid_for_claim"] is False for row in finite)
    ejeff_false = all(row["claim_allowed"] is False for row in ejeff)
    gates_false = all(row["claim_allowed"] is False for row in gates)
    branch_ok = all(Path(row["copy_path"]).exists() and row["valid_for_claim"] is False for row in branches)
    required_quantities = {"E_boundary", "E_corner", "E_harmonic", "orientation/sign/no-cancellation metadata"}
    finite_quantities = {row["quantity"] for row in finite}
    finite_complete = required_quantities.issubset(finite_quantities)
    rejected_shortcuts = any(row["verdict"] == "REJECTED_AS_INSUFFICIENT" for row in nocharge) and any(
        row["verdict"] == "REJECTED_AS_NO_HAIR_PROOF" for row in nocharge
    )
    formalization_count = formalization_recent_changed_count()
    no_github_outputs = all(".git" not in str(path).lower() and "github" not in str(path).lower() for path in csv_paths)
    rows = [
        {
            "validation_id": "VAL2719_0_sources",
            "passed": source_ok,
            "detail": "all source paths exist and required needles found" if source_ok else "missing source or needle",
            "timestamp_utc": ts(),
        },
        {"validation_id": "VAL2719_1_doc_written", "passed": DOC.exists(), "detail": str(DOC), "timestamp_utc": ts()},
        {"validation_id": "VAL2719_2_csv_parse", "passed": csv_ok, "detail": csv_detail, "timestamp_utc": ts()},
        {
            "validation_id": "VAL2719_3_rejected_shortcuts",
            "passed": rejected_shortcuts,
            "detail": "asymptotic-flatness-only and fixed-boundary shortcuts are rejected",
            "timestamp_utc": ts(),
        },
        {
            "validation_id": "VAL2719_4_theorem_nonclaim",
            "passed": nocharge_false and theorem_false,
            "detail": "no boundary/harmonic no-charge theorem is promoted",
            "timestamp_utc": ts(),
        },
        {
            "validation_id": "VAL2719_5_finite_rows_complete_nonclaim",
            "passed": finite_complete and finite_nonclaim,
            "detail": "E_boundary,E_corner,E_harmonic and orientation rows exist and remain nonclaim",
            "timestamp_utc": ts(),
        },
        {
            "validation_id": "VAL2719_6_ejeff_update_nonclaim",
            "passed": ejeff_false,
            "detail": "E_Jeff update vector remains formal/nonclaim",
            "timestamp_utc": ts(),
        },
        {
            "validation_id": "VAL2719_7_claim_gates_all_false",
            "passed": gates_false,
            "detail": "no local-GR/R10/PPN/public claim gate opened",
            "timestamp_utc": ts(),
        },
        {
            "validation_id": "VAL2719_8_branch_copies",
            "passed": branch_ok,
            "detail": "branch copies exist and remain nonclaim",
            "timestamp_utc": ts(),
        },
        {
            "validation_id": "VAL2719_9_no_formalization_recent_changes",
            "passed": formalization_count == 0,
            "detail": f"formalization_recent_changed_count={formalization_count}",
            "timestamp_utc": ts(),
        },
        {
            "validation_id": "VAL2719_10_no_github_outputs",
            "passed": no_github_outputs,
            "detail": "no GitHub/public-output path was written",
            "timestamp_utc": ts(),
        },
    ]
    overall = all(row["passed"] for row in rows)
    rows.append(
        {
            "validation_id": "VAL2719_OVERALL",
            "passed": overall,
            "detail": "2719 rejects boundary/hair shortcuts, keeps no-charge theorem conditional, installs finite E_boundary/E_corner/E_harmonic rows, and selects readout stability next",
            "timestamp_utc": ts(),
        }
    )
    return rows


def write_doc(
    sources: list[dict[str, Any]],
    nocharge: list[dict[str, Any]],
    theorem: list[dict[str, Any]],
    finite: list[dict[str, Any]],
    ejeff: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    blockers: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    snapshot: list[dict[str, Any]],
    branches: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> None:
    lines = [
        "# 2719 - Y5/R2FR Boundary-Harmonic No-charge Or Finite J_eff Bound Under AX1090 Closure",
        "",
        "## Private Verdict",
        "",
        "2719 tries to kill the boundary/harmonic source sector honestly. It does **not** close the no-charge theorem. The two tempting shortcuts are explicitly rejected: asymptotic flatness alone does not kill `Q_R`, and fixed `R_AB` boundary data is not a proof because it can hide reciprocal hair.",
        "",
        "The clean route is now exact as a conditional theorem: free natural `R_AB` boundary variation plus parent boundary object-exhaustion plus corner/worldtube silence plus harmonic zero-mode control would give `E_boundary=E_harmonic=0`. But those clauses are not parent/domain signed, so the branch remains nonclaim.",
        "",
        "The useful progress is finite-source discipline: `E_boundary`, `E_corner`, `E_harmonic`, and orientation/no-cancellation metadata are now explicit rows feeding `E_Jeff` and therefore the 2717 Green bound.",
        "",
        "## Claim Ceiling",
        "",
        "- No boundary no-charge, harmonic zero-mode, `Q_R=0`, local-GR/Newton, R10, PPN, clock, orbital, or public/GitHub claim is opened.",
        "- No fixed-boundary or asymptotic-flatness-only shortcut is allowed.",
        "- Boundary/harmonic rows are source-ready schemas only and remain `valid_for_claim=false`.",
        "- No `formalization-workbench` edits are allowed from this checkpoint.",
        "",
        "## Source Register",
        "",
        markdown_table(sources, ["source_id", "label", "path", "exists", "required_needles_found", "missing_needles", "use", "claim_credit"]),
        "",
        "## No-charge Audit",
        "",
        markdown_table(nocharge, ["audit_id", "target", "attempt", "verdict", "reason", "claim_allowed", "next_requirement"]),
        "",
        "## Conditional Theorem Attempt",
        "",
        markdown_table(theorem, ["theorem_id", "statement", "status", "missing_clause", "claim_allowed"]),
        "",
        "## Finite Boundary/Harmonic Rows",
        "",
        markdown_table(finite, ["row_id", "quantity", "definition", "feeds", "source_path", "units_need", "missing", "status", "valid_for_claim"]),
        "",
        "## E_Jeff Update",
        "",
        markdown_table(ejeff, ["update_id", "formula", "status", "claim_allowed"]),
        "",
        "## Claim Gates",
        "",
        markdown_table(gates, ["gate_id", "claim", "status", "required_before_claim", "claim_allowed"]),
        "",
        "## Current Blocker Stack",
        "",
        markdown_table(blockers, ["blocker_id", "missing_item", "effect", "best_next_attack", "claim_blocked"]),
        "",
        "## Decision Ledger",
        "",
        markdown_table(decisions, ["decision_id", "decision", "rationale", "allowed", "claim_credit"]),
        "",
        "## Next Target",
        "",
        markdown_table(next_rows, ["next_id", "status", "target_doc", "target_script", "mission", "acceptance", "forbidden", "selected", "claim_allowed"]),
        "",
        "## Project Status Snapshot",
        "",
        markdown_table(snapshot, ["snapshot_id", "sector", "state", "confidence", "next_need"]),
        "",
        "## Branch Copies",
        "",
        markdown_table(branches, ["copy_id", "source_table", "copy_path", "purpose", "exists", "valid_for_claim"]),
        "",
        "## Validation",
        "",
        markdown_table(validation, ["validation_id", "passed", "detail", "timestamp_utc"]),
        "",
        "## Plain-English Read",
        "",
        "This is a useful lock-picking step. We did not get to say boundary hair is gone, but we did stop the two bad proofs from sneaking in. The acceptable proof is narrow: natural variation, no `R_AB` boundary/corner object, no harmonic zero mode. Until those are signed, boundary hair is finite-source bookkeeping, not a solved theorem.",
        "",
        "Next best strike: readout stability. Boundary/harmonic is now explicit enough to carry as `E_Jeff`; the next way local GR can leak is the effective/readout map regenerating `R_AB` terms after the parent action looked clean.",
        "",
    ]
    DOC.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    for directory in (RESIDUALS, LOCAL_BOUNDS, SOURCE_WEIGHT, RAB_QUEUE):
        directory.mkdir(parents=True, exist_ok=True)

    sources = source_register_rows()
    nocharge = nocharge_audit_rows()
    theorem = theorem_attempt_rows()
    finite = finite_rows()
    ejeff = ejeff_update_rows()
    gates = claim_gate_rows()
    blockers = blocker_stack_rows()
    decisions = decision_ledger_rows()
    next_rows = next_target_rows()
    snapshot = project_snapshot_rows()

    write_csv(OUTPUTS["source_register"], sources)
    write_csv(OUTPUTS["nocharge_audit"], nocharge)
    write_csv(OUTPUTS["theorem_attempt"], theorem)
    write_csv(OUTPUTS["finite_rows"], finite)
    write_csv(OUTPUTS["ejeff_update"], ejeff)
    write_csv(OUTPUTS["claim_gates"], gates)
    write_csv(OUTPUTS["blocker_stack"], blockers)
    write_csv(OUTPUTS["decision_ledger"], decisions)
    write_csv(OUTPUTS["next_target"], next_rows)
    write_csv(OUTPUTS["project_snapshot"], snapshot)

    write_csv(BRANCH_OUTPUTS["local_bounds"], finite)
    write_csv(BRANCH_OUTPUTS["source_weight"], ejeff)
    write_csv(BRANCH_OUTPUTS["next_queue"], next_rows)

    branches = branch_copy_rows()
    write_csv(OUTPUTS["branch_copies"], branches)

    pending_validation = [
        {
            "validation_id": "VAL2719_PENDING",
            "passed": False,
            "detail": "pre-validation placeholder for first doc write",
            "timestamp_utc": ts(),
        }
    ]
    write_doc(sources, nocharge, theorem, finite, ejeff, gates, blockers, decisions, next_rows, snapshot, branches, pending_validation)

    validation = validation_rows(sources, nocharge, theorem, finite, ejeff, gates, branches)
    write_csv(OUTPUTS["validation"], validation)
    write_doc(sources, nocharge, theorem, finite, ejeff, gates, blockers, decisions, next_rows, snapshot, branches, validation)

    overall = next(row for row in validation if row["validation_id"] == "VAL2719_OVERALL")
    print(f"2719 complete: {overall['passed']} - {overall['detail']}")
    print(DOC)


if __name__ == "__main__":
    main()
