from __future__ import annotations

import csv
import sys
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work")
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = ROOT.parent / "formalization-workbench"
CHECKPOINT_ID = "3678"
BRANCH_ID = "MTS_R2FR_Y5_CANONICAL_EM_POYNTING_TRANSFER_LEG_OR_SEM_BOUND_3678"
DOC = ROOT / "3678-Y5-R2FR-canonical-EM-Poynting-transfer-leg-or-sEM-bound.md"


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def base(ts: str) -> dict[str, object]:
    return {
        "timestamp_utc": ts,
        "branch_id": BRANCH_ID,
        "checkpoint_id": CHECKPOINT_ID,
        "valid_for_claim": False,
    }


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8", errors="replace")


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def load_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def parse_csv(path: Path) -> tuple[bool, int]:
    try:
        rows = load_csv(path)
        return True, len(rows)
    except Exception:
        return False, 0


def source_register(ts: str) -> list[dict[str, object]]:
    specs = [
        ("handoff_3677", RESIDUALS / "P8_Y5_R2FR_3677_NEXT_TARGET.csv", "canonical EM/Poynting", "3677 selected canonical EM/Poynting transfer leg"),
        ("doc_3677", ROOT / "3677-Y5-R2FR-cFXR-parent-normalization-scale-or-local-generator-elimination.md", "raw `c_FXR` is not the physical coupling", "3677 canonical pair derivation"),
        ("implications_3677", RESIDUALS / "P8_Y5_R2FR_3677_BOUND_IMPLICATION_ROWS.csv", "BIR3677_1_if_gFXR_O1", "s_EM target from invariant scalar-slip bound"),
        ("poynting_3463", RESIDUALS / "P8_Y5_R2FR_3463_MAXWELL_POYNTING_STRESS_LEDGER.csv", "EM3463_2_poynting", "Poynting stress-current identity"),
        ("single_current_3463", RESIDUALS / "P8_Y5_R2FR_3463_SINGLE_SOURCE_CURRENT_AUDIT.csv", "SSC3463_2_Poynting_included", "EM/Poynting included in same Hilbert source"),
        ("owner_3465", RESIDUALS / "P8_Y5_R2FR_3465_EM_OWNER_PACKAGE_AUDIT.csv", "EMO3465_1_unique_F2", "EM owner package gaps"),
        ("hodge_3504", RESIDUALS / "P8_EM_Hodge_flow_rule_bound_or_zero.csv", "DHB3504_0_Delta_Hodge_EM", "Hodge/constitutive residual vector"),
        ("em_bound_vector_3503", RESIDUALS / "P8_EM_Hodge_Maxwell_current_owner_bound_vector.csv", "EMB3503_2_C_XF2", "EM component bound vector"),
        ("scalar_coupling_3507", RESIDUALS / "P8_EM_scalar_coupling_owner_alpha_residual.csv", "ARE3507_1_C_XF2", "scalar gauge coupling throat"),
        ("source_current_3650", RESIDUALS / "P8_Y5_R2FR_3650_SOURCE_CURRENT_THEOREM_ATTEMPT.csv", "SCT3650_3_force_projection", "source/test force projection envelope"),
        ("charge_current_3650", RESIDUALS / "P8_Y5_R2FR_3650_CHARGE_CURRENT_CLAUSE_AUDIT.csv", "SCA3650_6_total", "charge-current owner signature status"),
        ("doc_3620", ROOT / "3620-Y5-R2FR-EM-source-coupling-owner-or-F2-coefficient-bound.md", "lambda_F2=b_alpha=kappa_J=w_EM=0", "EM source-coupling owner packet"),
        ("status_3620", RESIDUALS / "P8_Y5_EM_source_coupling_owner_status.csv", "lambda_F2;b_alpha;kappa_J;w_EM;Phi_EM_boundary", "live EM source-coupling coefficients"),
    ]
    rows: list[dict[str, object]] = []
    for source_id, path, needle, relevance in specs:
        text = read_text(path) if path.exists() else ""
        rows.append(
            {
                **base(ts),
                "source_id": source_id,
                "source_path": str(path),
                "exists": path.exists(),
                "needle": needle,
                "needle_found": needle in text,
                "relevance": relevance,
            }
        )
    return rows


def target_bounds() -> dict[str, float]:
    rows = load_csv(RESIDUALS / "P8_Y5_R2FR_3677_BOUND_IMPLICATION_ROWS.csv")
    by_id = {row["implication_id"]: float(row["numeric_value"]) for row in rows}
    return {
        "xi_max": by_id["BIR3677_0_invariant_bound"],
        "s_if_g_o1": by_id["BIR3677_1_if_gFXR_O1"],
        "g_if_s_o1": by_id["BIR3677_2_if_sEM_O1"],
        "s_if_g_4pi": by_id["BIR3677_3_if_gFXR_4pi"],
    }


def decomposition_rows(ts: str) -> list[dict[str, object]]:
    specs = [
        (
            "SEM3678_0_definition",
            "s_EM",
            "s_EM=f_EM/sqrt(Z_X)",
            "canonical dimensionless vertical derivative of extra EM/source transfer into X_hat",
            "not ordinary EM stress itself",
            "defines the tested transfer leg in xi_FXR=|g_FXR*s_EM|",
            "DERIVED_FROM_3677_CANONICAL_PAIR",
        ),
        (
            "SEM3678_1_minimal_poynting",
            "ordinary minimal Maxwell/Poynting stress",
            "T_EM^{0i}=S_Poynting^i/c^2 and T_EM is in T_total",
            "standard EM energy/momentum is already part of Hilbert source mass M_H",
            "zero contribution to extra s_EM if same observed Hodge/coframe and stationary source accounting hold",
            "prevents double-counting ordinary EM energy as an MTS fifth-force leg",
            "CONDITIONAL_ZERO_FOR_EXTRA_TRANSFER",
        ),
        (
            "SEM3678_2_extra_transfer_law",
            "canonical residual envelope",
            "s_EM = s_Hodge + s_XF2 + s_wEM + s_J + s_alpha_source + s_boundary_flux + s_readout + s_nonHilbert",
            "linearized around the calibrated local branch in canonical X_hat units",
            "each term is a source-ready canonical coefficient, including any projection factor",
            "turns the vague coupling into an executable no-cancellation vector",
            "DECOMPOSITION_DERIVED_AS_ACCOUNTING_IDENTITY",
        ),
        (
            "SEM3678_3_no_cancellation",
            "absolute envelope",
            "|s_EM| <= sum_i |s_i|",
            "no sign cancellation allowed between Hodge, F2, current, boundary, readout, and non-Hilbert legs",
            "numeric budget can be allocated against the 3677 target",
            "makes future tests falsifiable without hiding behind cancellations",
            "NO_CANCELLATION_GUARD",
        ),
    ]
    return [
        {
            **base(ts),
            "decomposition_id": decomposition_id,
            "object": obj,
            "formula": formula,
            "meaning": meaning,
            "zero_or_bound_rule": zero_or_bound_rule,
            "consequence": consequence,
            "status": status,
            "claim_allowed": False,
            "score_ready": False,
        }
        for decomposition_id, obj, formula, meaning, zero_or_bound_rule, consequence, status in specs
    ]


def zero_theorem_rows(ts: str) -> list[dict[str, object]]:
    specs = [
        (
            "EMZ3678_0_same_observed_hodge",
            "same observed Hodge/coframe",
            "S_EM=-1/(4mu0) int F wedge *_obs F and T_EM from the same g_obs/e_obs used by gravity",
            "CONDITIONAL_STANDARD_FORM_NOT_PARENT_SIGNED",
            "EMO3465_0 observed Hodge is conditional; 3613 keeps principal/skewon/hidden/readout components retained",
            "s_Hodge may remain finite",
        ),
        (
            "EMZ3678_1_unique_F2_no_XF2",
            "no independent F(X)F^2 or lambda_F2",
            "parent operator domain forbids hidden-visible scalar gauge kinetic coefficient",
            "NOT_DERIVED_CORE_COUPLING_TARGET",
            "3506/3507/3620 identify C_XF2/lambda_F2 as the scalar coupling throat",
            "s_XF2 remains finite",
        ),
        (
            "EMZ3678_2_no_independent_wEM",
            "no EM action/stress multiplier",
            "unique Maxwell curvature norm plus alpha/charge-current owner kills w_EM",
            "NOT_PARENT_SIGNED",
            "3463/3464 retain weighted EM action obstruction",
            "s_wEM remains finite",
        ),
        (
            "EMZ3678_3_charge_current_owner",
            "same charge/current owner",
            "A_Q, J_Q, charge lattice and matter representation descend from one parent owner",
            "SOURCE_CURRENT_OWNER_UNSIGNED",
            "3650 leaves charge lattice, current measure, material marker, boundary current clauses unsigned",
            "s_J and s_alpha_source remain finite",
        ),
        (
            "EMZ3678_4_stationary_poynting_boundary",
            "no radiative/background Poynting flux",
            "integral_boundary S_Poynting dot n dA=0 in the stationary isolated local branch",
            "NOT_PARENT_SIGNED",
            "EMF3502_1 keeps Phi_EM_rad as retained flux coefficient",
            "s_boundary_flux remains finite",
        ),
        (
            "EMZ3678_5_readout_radiative_closure",
            "readout/radiative closure",
            "loops, clocks, spectroscopy, and reduced readout do not regenerate f_X F^2, alpha_X, or EM binding response",
            "UNSIGNED_PRESERVATION_REQUIREMENT",
            "3465 and 3503 keep C_EM_readout retained",
            "s_readout remains finite",
        ),
        (
            "EMZ3678_6_total_Hilbert_no_bypass",
            "no non-Hilbert/improvement source bypass",
            "all active source currents are Hilbert/improvement-owned with zero exterior flux",
            "CONDITIONAL_CLOSURE_NOT_SIGNED",
            "3508 and 3503 keep non-Hilbert source bypass and Delta_J_total active",
            "s_nonHilbert remains finite",
        ),
        (
            "EMZ3678_7_verdict",
            "s_EM theorem-zero",
            "EMZ3678_0 through EMZ3678_6 all signed",
            "THEOREM_NOT_PROVED_CURRENT_CORPUS",
            "ordinary minimal Poynting accounting is conditionally correct, but extra vertical transfer channels remain live",
            "s_EM is bounded/decomposed, not claimed zero",
        ),
    ]
    return [
        {
            **base(ts),
            "zero_id": zero_id,
            "clause": clause,
            "required_signature": required_signature,
            "current_status": current_status,
            "evidence_summary": evidence_summary,
            "if_unsigned": if_unsigned,
            "source_signed": False,
            "claim_allowed": False,
            "score_ready": False,
        }
        for zero_id, clause, required_signature, current_status, evidence_summary, if_unsigned in specs
    ]


def component_rows(ts: str) -> list[dict[str, object]]:
    target = target_bounds()["s_if_g_o1"]
    active_components = 8
    equal_budget = target / active_components
    specs = [
        ("SCB3678_0_s_Hodge", "s_Hodge", "Delta_Hodge_EM canonical projection", "EM Hodge/constitutive flow mismatch changes Poynting/source transfer", "DHB3504_0_Delta_Hodge_EM", "MISSING_NUMERIC_OR_THEOREM_ZERO", equal_budget),
        ("SCB3678_1_s_XF2", "s_XF2", "C_XF2 or D_Xhat ln lambda_F2", "hidden/motion/time scalar multiplies F^2 or F*F", "ARE3507_1_C_XF2", "MISSING_PARENT_EXCLUSION_OR_BOUND", equal_budget),
        ("SCB3678_2_s_wEM", "s_wEM", "D_Xhat ln w_EM", "independent EM action/stress multiplier rescales Poynting source strength", "EM3463_4_multiplier_obstruction", "MISSING_UNIQUE_F2_OR_ALPHA_OWNER", equal_budget),
        ("SCB3678_3_s_J", "s_J", "D_Xhat ln g_J or kappa_J", "charge/current normalization not locked to Maxwell field normalization", "SCA3650_6_total", "MISSING_CHARGE_CURRENT_OWNER_OR_BOUND", equal_budget),
        ("SCB3678_4_s_alpha_source", "s_alpha_source", "beta_source_alpha material/source projection", "source/test EM charge normalization leaks into force/source map", "BSA3650_1_beta_source_alpha", "MISSING_SOURCE_TEST_PROJECTION_OR_BOUND", equal_budget),
        ("SCB3678_5_s_boundary_flux", "s_boundary_flux", "Phi_EM_boundary/(M_H window)", "radiative/background Poynting flux changes local source charge over the window", "EMF3502_1_radiative_poynting_flux", "MISSING_STATIONARY_FLUX_ZERO_OR_BOUND", equal_budget),
        ("SCB3678_6_s_readout", "s_readout", "C_EM_readout", "readout/radiative loop regenerates EM coefficient dependence", "EMB3503_5_C_EM_readout", "MISSING_READOUT_RADIATIVE_CLOSURE_OR_BOUND", equal_budget),
        ("SCB3678_7_s_nonHilbert", "s_nonHilbert", "Delta_J_total or non-Hilbert bypass projection", "source current has active non-Hilbert/improvement component not in ordinary Maxwell Hilbert stress", "EMB3503_6_Delta_J_total", "MISSING_TOTAL_HILBERT_CLOSURE_OR_BOUND", equal_budget),
    ]
    return [
        {
            **base(ts),
            "component_id": component_id,
            "canonical_component": canonical_component,
            "definition": definition,
            "physical_meaning": physical_meaning,
            "source_anchor": source_anchor,
            "current_status": current_status,
            "units": "dimensionless canonical transfer",
            "required_for_o1_gFXR": f"abs({canonical_component}) <= {budget:.12e} under equal 8-leg no-cancellation allocation",
            "numeric_value": "MISSING_COMPONENT_VALUE",
            "source_path_or_row": "see source_anchor and source register",
            "valid_for_claim": False,
            "score_ready": False,
            "claim_allowed": False,
        }
        for component_id, canonical_component, definition, physical_meaning, source_anchor, current_status, budget in specs
    ]


def allocation_rows(ts: str) -> list[dict[str, object]]:
    targets = target_bounds()
    active_components = 8
    rows = []
    for allocation_id, target_name, target_value, assumption in [
        ("ALLOC3678_0_O1_gFXR", "s_EM_target_if_|g_FXR|<=1", targets["s_if_g_o1"], "|g_FXR|<=1"),
        ("ALLOC3678_1_4pi_gFXR", "s_EM_target_if_|g_FXR|<=4pi", targets["s_if_g_4pi"], "|g_FXR|<=4pi"),
    ]:
        rows.append(
            {
                **base(ts),
                "allocation_id": allocation_id,
                "target_name": target_name,
                "assumption": assumption,
                "target_abs_s_EM": f"{target_value:.12e}",
                "active_component_count": active_components,
                "equal_component_budget": f"{target_value / active_components:.12e}",
                "allocation_rule": "if every active component obeys equal_component_budget, then |s_EM| obeys the no-cancellation envelope",
                "valid_for_claim": False,
                "score_ready": False,
                "claim_allowed": False,
            }
        )
    return rows


def decision_rows(ts: str) -> list[dict[str, object]]:
    specs = [
        (
            "DEC3678_0_minimal_EM_not_sEM",
            "ordinary Maxwell/Poynting energy is not the extra s_EM leg",
            "STANDARD_STRESS_INSIDE_HILBERT_SOURCE",
            "Poynting is absolutely relevant, but it belongs in T_total/M_H unless an extra vertical EM transfer coefficient exists.",
            "avoid double-counting standard EM energy as fifth-force/source hair",
        ),
        (
            "DEC3678_1_sEM_decomposition",
            "s_EM has an executable canonical residual vector",
            "PROMOTED_TO_BOUND_VECTOR",
            "The surviving transfer leg is the absolute sum of Hodge, F2, w_EM, current, alpha-source, boundary, readout, and non-Hilbert components.",
            "future work can derive/zero/bound components one at a time",
        ),
        (
            "DEC3678_2_core_next",
            "attack C_XF2/lambda_F2 first",
            "NEXT_BEST_TARGET",
            "3506/3507/3620 all identify the scalar Maxwell kinetic coefficient as the hard coupling throat after visible U(1)/Maxwell reduction.",
            "derive unique-F2/no-XF2 theorem or source an alpha/WEP/clock bound for s_XF2",
        ),
        (
            "DEC3678_3_claim_discipline",
            "no Maxwell/local-GR claim",
            "BLOCKED_NONCLAIM",
            "The conditional Poynting/Hilbert result is real, but owner clauses remain unsigned and numeric component values are missing.",
            "keep private until a component theorem-zero or source-backed numeric row closes",
        ),
    ]
    return [
        {
            **base(ts),
            "decision_id": decision_id,
            "decision": decision,
            "status": status,
            "reason": reason,
            "next_action": next_action,
            "claim_allowed": False,
            "score_ready": False,
        }
        for decision_id, decision, status, reason, next_action in specs
    ]


def claim_gate_rows(ts: str) -> list[dict[str, object]]:
    specs = [
        ("CG3678_0_sEM_zero", "claim s_EM=0", "BLOCKED_NONCLAIM", "EMZ3678_7 theorem-zero verdict is not proved"),
        ("CG3678_1_sEM_numeric", "score finite s_EM", "BLOCKED_COMPONENT_VALUES_MISSING", "component rows have MISSING_COMPONENT_VALUE"),
        ("CG3678_2_poynting_claim", "claim Poynting route proves source coupling", "BLOCKED_OVERCOUNT_GUARD", "ordinary Poynting is in Hilbert stress, but extra vertical transfer channels remain"),
        ("CG3678_3_local_GR", "claim local-GR/PPN pass", "BLOCKED_NONCLAIM", "source coupling and EM transfer owner clauses remain unsigned"),
        ("CG3678_4_public_or_github", "public/GitHub promotion", "BLOCKED_PRIVATE", "private derivation checkpoint only"),
    ]
    return [
        {
            **base(ts),
            "claim_gate_id": claim_gate_id,
            "gate": gate,
            "status": status,
            "reason": reason,
            "claim_allowed": False,
            "score_ready": False,
        }
        for claim_gate_id, gate, status, reason in specs
    ]


def status_rows(ts: str) -> list[dict[str, object]]:
    targets = target_bounds()
    return [
        {
            **base(ts),
            "status": "SEM_TRANSFER_DECOMPOSED_POYNTING_STANDARD_STRESS_SEPARATED_NONCLAIM",
            "summary": "3678 separates ordinary Maxwell/Poynting Hilbert stress, which belongs inside T_total/M_H, from the extra canonical vertical EM transfer leg s_EM. It derives the no-cancellation decomposition s_EM=s_Hodge+s_XF2+s_wEM+s_J+s_alpha_source+s_boundary_flux+s_readout+s_nonHilbert and converts the 3677 scalar-slip target into per-component private budgets.",
            "claim_ceiling": "no s_EM zero, finite s_EM evidence, Maxwell pass, local-GR, Newton, PPN, WEP/R10, or source-coupling claim is made",
            "useful_result": f"under |g_FXR|<=1, |s_EM| must be <= {targets['s_if_g_o1']:.12e}; an equal 8-leg no-cancellation budget gives each active component <= {targets['s_if_g_o1']/8:.12e}",
            "next_missing_piece": "derive unique-F2/no-XF2 theorem or source/bound s_XF2 in canonical units",
        }
    ]


def next_rows(ts: str) -> list[dict[str, object]]:
    return [
        {
            **base(ts),
            "next_id": "NEXT3678_0",
            "target_doc": "3679-Y5-R2FR-unique-F2-no-XF2-theorem-or-sXF2-bound.md",
            "target_script": "scripts/Y5_R2FR_3679_unique_F2_no_XF2_theorem_or_sXF2_bound.py",
            "objective": "derive the unique-Maxwell-F2/no hidden XF2 coefficient theorem in canonical EM units, or produce a nonclaim source-backed bound/input row for s_XF2 inside the s_EM envelope",
            "success_gate": "either s_XF2 is theorem-zero from parent operator-domain/charge-current ownership, or it has a sourced numeric/nonclaim bound row compatible with the 3678 component budget",
        }
    ]


def write_doc(
    sources: list[dict[str, object]],
    decomposition: list[dict[str, object]],
    zero_rows: list[dict[str, object]],
    components: list[dict[str, object]],
    allocations: list[dict[str, object]],
    decisions: list[dict[str, object]],
    gates: list[dict[str, object]],
    status: list[dict[str, object]],
    next_target: list[dict[str, object]],
) -> None:
    lines = [
        "# 3678 - Canonical EM/Poynting transfer leg or s_EM bound",
        "",
        f"**Status:** {status[0]['status']}",
        "",
        "This checkpoint makes the Poynting point precise: ordinary Maxwell/Poynting stress is real source stress, but it is already inside the total Hilbert source `T_total` and source charge `M_H`. The tested MTS leg is only the **extra vertical EM transfer** after that standard accounting.",
        "",
        "## Main result",
        "",
        "`s_EM = f_EM/sqrt(Z_X)` is not standard EM energy. It is the canonical coefficient for extra EM/source response to the local MTS field `X_hat`.",
        "",
        "The private no-cancellation envelope is:",
        "",
        "`s_EM = s_Hodge + s_XF2 + s_wEM + s_J + s_alpha_source + s_boundary_flux + s_readout + s_nonHilbert`",
        "",
        "`|s_EM| <= sum_i |s_i|`.",
        "",
        f"Under the 3677 `|g_FXR|<=1` smoke prior: `{status[0]['useful_result']}`.",
        "",
        "## Decomposition",
    ]
    for row in decomposition:
        lines.append(f"- `{row['decomposition_id']}`: {row['status']} - {row['object']} -> {row['consequence']}")
    lines.extend(["", "## Zero theorem audit"])
    for row in zero_rows:
        lines.append(f"- `{row['zero_id']}`: {row['current_status']} - {row['clause']} -> {row['if_unsigned']}")
    lines.extend(["", "## Component rows"])
    for row in components:
        lines.append(f"- `{row['component_id']}`: `{row['canonical_component']}` - {row['current_status']}; target: {row['required_for_o1_gFXR']}")
    lines.extend(["", "## Target allocations"])
    for row in allocations:
        lines.append(f"- `{row['allocation_id']}`: target `{row['target_abs_s_EM']}`, equal component budget `{row['equal_component_budget']}` under {row['assumption']}")
    lines.extend(["", "## Decisions"])
    for row in decisions:
        lines.append(f"- `{row['decision_id']}`: {row['status']} - {row['decision']} -> {row['next_action']}")
    lines.extend(["", "## Claim gates"])
    for row in gates:
        lines.append(f"- `{row['claim_gate_id']}`: {row['status']} - {row['gate']} because {row['reason']}")
    lines.extend(
        [
            "",
            "## Next target",
            f"`{next_target[0]['target_doc']}` via `{next_target[0]['target_script']}`.",
            "",
            "## Sources",
        ]
    )
    for row in sources:
        lines.append(f"- `{row['source_id']}`: `{row['source_path']}` exists={row['exists']} needle_found={row['needle_found']}")
    DOC.write_text("\n".join(lines) + "\n", encoding="utf-8")


def validate(
    ts: str,
    output_paths: list[Path],
    sources: list[dict[str, object]],
    decomposition: list[dict[str, object]],
    zero_rows: list[dict[str, object]],
    components: list[dict[str, object]],
    allocations: list[dict[str, object]],
    decisions: list[dict[str, object]],
    gates: list[dict[str, object]],
    status: list[dict[str, object]],
    next_target: list[dict[str, object]],
) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []

    def add(validation_id: str, ok: bool, detail: str) -> None:
        rows.append(
            {
                "timestamp_utc": ts,
                "branch_id": BRANCH_ID,
                "checkpoint_id": CHECKPOINT_ID,
                "validation_id": validation_id,
                "result": "PASS" if ok else "FAIL",
                "detail": detail,
            }
        )

    csv_status = [parse_csv(path) for path in output_paths if path.suffix.lower() == ".csv"]
    generated = sources + decomposition + zero_rows + components + allocations + decisions + gates + status + next_target
    doc_text = read_text(DOC)
    leaks: list[Path] = []
    if FORMALIZATION.exists():
        for pattern in ["*Y5_R2FR_3678*", "3678-Y5-R2FR-*", "P8_Y5*3678*"]:
            leaks.extend(FORMALIZATION.rglob(pattern))
    zero_ids = {str(row["zero_id"]) for row in zero_rows}
    component_ids = {str(row["component_id"]) for row in components}
    allocation_ids = {str(row["allocation_id"]) for row in allocations}

    add("VAL3678_0_sources_exist", all(row["exists"] for row in sources), "every cited source path exists")
    add("VAL3678_1_needles_found", all(row["needle_found"] for row in sources), "every source needle found")
    add("VAL3678_2_outputs_exist", all(path.exists() for path in output_paths), "all expected 3678 outputs written")
    add("VAL3678_3_csv_parse", all(ok and count > 0 for ok, count in csv_status), "all generated CSVs parse with rows")
    add("VAL3678_4_decomposition", any(row["decomposition_id"] == "SEM3678_2_extra_transfer_law" and "s_Hodge" in row["formula"] and "s_XF2" in row["formula"] for row in decomposition), "s_EM decomposition includes canonical residual vector")
    add("VAL3678_5_poynting_not_double_counted", any(row["decomposition_id"] == "SEM3678_1_minimal_poynting" and row["status"] == "CONDITIONAL_ZERO_FOR_EXTRA_TRANSFER" for row in decomposition), "ordinary Poynting stress separated from extra transfer")
    add("VAL3678_6_zero_audit", {"EMZ3678_0_same_observed_hodge", "EMZ3678_1_unique_F2_no_XF2", "EMZ3678_2_no_independent_wEM", "EMZ3678_3_charge_current_owner", "EMZ3678_4_stationary_poynting_boundary", "EMZ3678_5_readout_radiative_closure", "EMZ3678_6_total_Hilbert_no_bypass", "EMZ3678_7_verdict"}.issubset(zero_ids), "zero theorem audit covers all EM/Poynting clauses")
    add("VAL3678_7_zero_not_claimed", any(row["zero_id"] == "EMZ3678_7_verdict" and row["current_status"] == "THEOREM_NOT_PROVED_CURRENT_CORPUS" for row in zero_rows), "s_EM zero theorem not promoted")
    add("VAL3678_8_components", {"SCB3678_0_s_Hodge", "SCB3678_1_s_XF2", "SCB3678_2_s_wEM", "SCB3678_3_s_J", "SCB3678_4_s_alpha_source", "SCB3678_5_s_boundary_flux", "SCB3678_6_s_readout", "SCB3678_7_s_nonHilbert"}.issubset(component_ids), "eight active s_EM component rows present")
    add("VAL3678_9_components_unfilled", all(row["numeric_value"] == "MISSING_COMPONENT_VALUE" and row["score_ready"] is False for row in components), "component rows remain unfilled/non-score-ready")
    add("VAL3678_10_allocations", {"ALLOC3678_0_O1_gFXR", "ALLOC3678_1_4pi_gFXR"}.issubset(allocation_ids), "O1 and 4pi target allocations present")
    add("VAL3678_11_next_target", next_target[0]["target_doc"].startswith("3679-") and "s_XF2" in next_target[0]["objective"], "3679 unique-F2/s_XF2 target selected")
    add("VAL3678_12_all_nonclaim", not any(str(row.get("valid_for_claim", "")).lower() == "true" or str(row.get("claim_allowed", "")).lower() == "true" or str(row.get("score_ready", "")).lower() == "true" for row in generated), "all generated rows remain nonclaim and unscoreable")
    add("VAL3678_13_claim_gates_blocked", all(row["claim_allowed"] is False and row["score_ready"] is False for row in gates), "claim gates remain blocked")
    add("VAL3678_14_doc_written", "ordinary Maxwell/Poynting stress" in doc_text and "extra vertical EM transfer" in doc_text and "s_XF2" in doc_text, "doc records Poynting separation and s_EM vector")
    add("VAL3678_15_no_formalization_leak", not leaks, "no 3678 checkpoint files in formalization-workbench")
    return rows


def main() -> int:
    ts = stamp()
    RESIDUALS.mkdir(parents=True, exist_ok=True)
    sources = source_register(ts)
    decomposition = decomposition_rows(ts)
    zero_rows = zero_theorem_rows(ts)
    components = component_rows(ts)
    allocations = allocation_rows(ts)
    decisions = decision_rows(ts)
    gates = claim_gate_rows(ts)
    status = status_rows(ts)
    next_target = next_rows(ts)
    outputs = {
        "sources": RESIDUALS / "P8_Y5_R2FR_3678_SOURCE_REGISTER.csv",
        "decomposition": RESIDUALS / "P8_Y5_R2FR_3678_CANONICAL_SEM_DECOMPOSITION_ROWS.csv",
        "zero": RESIDUALS / "P8_Y5_R2FR_3678_SEM_ZERO_THEOREM_AUDIT.csv",
        "components": RESIDUALS / "P8_Y5_R2FR_3678_SEM_COMPONENT_BOUND_REQUIREMENTS.csv",
        "allocations": RESIDUALS / "P8_Y5_R2FR_3678_SEM_TARGET_ALLOCATION_ROWS.csv",
        "decisions": RESIDUALS / "P8_Y5_R2FR_3678_DECISION_ROWS.csv",
        "gates": RESIDUALS / "P8_Y5_R2FR_3678_CLAIM_GATES.csv",
        "status": RESIDUALS / "P8_Y5_R2FR_3678_STATUS.csv",
        "next": RESIDUALS / "P8_Y5_R2FR_3678_NEXT_TARGET.csv",
        "validation": RESIDUALS / "P8_Y5_BRR545_3678_VALIDATION.csv",
    }
    write_csv(outputs["sources"], sources)
    write_csv(outputs["decomposition"], decomposition)
    write_csv(outputs["zero"], zero_rows)
    write_csv(outputs["components"], components)
    write_csv(outputs["allocations"], allocations)
    write_csv(outputs["decisions"], decisions)
    write_csv(outputs["gates"], gates)
    write_csv(outputs["status"], status)
    write_csv(outputs["next"], next_target)
    write_doc(sources, decomposition, zero_rows, components, allocations, decisions, gates, status, next_target)
    generated_paths = [path for key, path in outputs.items() if key != "validation"] + [DOC]
    validation = validate(ts, generated_paths, sources, decomposition, zero_rows, components, allocations, decisions, gates, status, next_target)
    write_csv(outputs["validation"], validation)
    failures = [row for row in validation if row["result"] != "PASS"]
    if failures:
        print(f"3678 validation failed: {failures}", file=sys.stderr)
        return 1
    print("wrote 3678 checkpoint: ordinary Poynting stress separated from extra s_EM transfer; s_XF2 selected next")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
