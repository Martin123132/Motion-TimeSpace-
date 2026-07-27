from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "932-Y5-R10-gamma-zero-parent-condition-or-beta-WEP-pivot.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
SCRIPT_START_UTC = datetime.now(timezone.utc)


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def bool_text(value: bool) -> str:
    return "true" if value else "false"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def md_cell(value: object) -> str:
    return str(value).replace("\n", " ").replace("|", "\\|")


def md_table(rows: list[dict[str, object]], fields: list[str]) -> str:
    if not rows:
        return "_No rows._"
    header = "| " + " | ".join(fields) + " |"
    separator = "| " + " | ".join("---" for _field in fields) + " |"
    body = []
    for row in rows:
        body.append("| " + " | ".join(md_cell(row.get(field, "")) for field in fields) + " |")
    return "\n".join([header, separator, *body])


def source_register() -> list[dict[str, str]]:
    specs = [
        {
            "source_id": "931_doc",
            "path": "931-Y5-R10-gamma-PPN-projection-coefficient-or-KBFH-bound-envelope.md",
            "role": "gamma projection and symbolic KBFH bound envelope",
            "needle": "C_gamma_FM = b_FM - a_FM",
        },
        {
            "source_id": "931_validation",
            "path": "source-intake/mts_residuals/P8_Y5_BRR545_931_VALIDATION.csv",
            "role": "proves 931 validation passed",
            "needle": "V931_9_validation_rows_ready",
        },
        {
            "source_id": "931_zero_conditions",
            "path": "source-intake/mts_residuals/P8_Y5_R10_931_GAMMA_ZERO_CONDITIONS.csv",
            "role": "a_FM=b_FM and no-anisotropic-stress conditions",
            "needle": "ZG931_0_equal_metric_response",
        },
        {
            "source_id": "228_no_slip",
            "path": "228-isotropic-response-condition-or-official-local-bound-runner.md",
            "role": "earlier isotropic/no-slip sufficient condition",
            "needle": "isotropic_no_slip_sufficient_condition_derived_parent_boundary_owner_open_no_PPN_promotion",
        },
        {
            "source_id": "229_scalar_owner",
            "path": "229-second-order-beta-or-boundary-scalar-owner.md",
            "role": "scalar boundary symmetry owner and beta reduction",
            "needle": "scalar_boundary_symmetry_owner_derived_sufficient_beta_reduced_to_vacuum_Einstein_gate_no_PPN_promotion",
        },
        {
            "source_id": "243_no_shear_gate",
            "path": "243-local-representative-selection-action-or-no-shear-gate.md",
            "role": "N2 no-shear gate and scalar-only boundary data",
            "needle": "Rloc_parent_selection_not_derived_N2_no_shear_sufficient_gate_locked_no_local_GR_promotion",
        },
        {
            "source_id": "908_ppn_vector",
            "path": "908-Y5-R10-projector-stress-Bianchi-fate-or-retained-PPN-vector.md",
            "role": "retained PPN/source vector if zero route remains unsigned",
            "needle": "retain_projector_Bianchi_residual",
        },
    ]
    rows = []
    for spec in specs:
        source_path = ROOT / spec["path"]
        exists = source_path.exists()
        needle_found = exists and spec["needle"] in read_text(source_path)
        rows.append(
            {
                **spec,
                "absolute_path": str(source_path),
                "exists": bool_text(exists),
                "needle_found": bool_text(needle_found),
                "valid_for_claim": "false",
                "generated_utc": stamp(),
            }
        )
    return rows


def theorem_attempt() -> list[dict[str, str]]:
    return [
        {
            "theorem_id": "GZ932_0_metric_split",
            "premise_or_step": "start from 931 weak-field split",
            "mathematical_form": "C_gamma_FM = b_FM - a_FM",
            "derived_result": "gamma is silent at first order iff a_FM=b_FM",
            "status": "derived_in_931",
            "missing_for_claim": "none for projection algebra; parent response still missing",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "theorem_id": "GZ932_1_no_slip_equation",
            "premise_or_step": "use trace-free weak-field constraint",
            "mathematical_form": "D_ij(Phi-Psi) = 8*pi*G*pi_ij^TF",
            "derived_result": "if residual trace-free anisotropic stress pi_ij^TF vanishes and homogeneous l>=2 modes are absent, then Phi-Psi=0",
            "status": "standard_local_constraint_written_as_MTS_gate",
            "missing_for_claim": "parent proof that MTS residual has no trace-free spatial stress",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "theorem_id": "GZ932_2_scalar_boundary_variation",
            "premise_or_step": "import 228/229/243 scalar boundary route",
            "mathematical_form": "S_boundary=int_boundary sqrt(|gamma|) F(Y_scalar); tau_AB=-(2/sqrt(|gamma|)) delta S_boundary/delta gamma^AB = tau gamma_AB",
            "derived_result": "scalar-only compact boundary data supplies trace-only boundary stress and no tangential shear channel",
            "status": "conditional_sufficient_owner",
            "missing_for_claim": "parent action must derive Y_scalar and forbid trace-free/tangential channels",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "theorem_id": "GZ932_3_equal_response",
            "premise_or_step": "translate no-slip to 931 coefficients",
            "mathematical_form": "Phi=Psi after measured-GM calibration => a_FM=b_FM",
            "derived_result": "C_gamma_FM=0 at O(epsilon_FM)",
            "status": "conditional_gamma_zero_theorem",
            "missing_for_claim": "same-source calibration, no incoming l>=2 mode, and scalar-only boundary owner are not parent-signed",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "theorem_id": "GZ932_4_bound_fallback",
            "premise_or_step": "if equal response is not parent-signed",
            "mathematical_form": "|K_BF_H| <= 2.3e-05/(|C_gamma_FM| X_FM)",
            "derived_result": "retain gamma as symbolic KBFH bound envelope",
            "status": "fallback_retained",
            "missing_for_claim": "numeric C_gamma_FM and X_FM",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def parent_signature_audit() -> list[dict[str, str]]:
    specs = [
        (
            "SIG932_0_scalar_variable_set",
            "parent action allows only scalar compact boundary variables Y_scalar",
            "needed to make tau_AB trace-only",
            "not_parent_signed",
            "derive allowed boundary data from MTS parent fields",
        ),
        (
            "SIG932_1_no_tracefree_shell",
            "trace-free shell curvature K_TF_AB and tangential memory shear vanish",
            "needed to remove pi_ij^TF and l>=2 slip source",
            "conditional_only",
            "prove no trace-free/tangential channel or retain response coefficient",
        ),
        (
            "SIG932_2_same_source_calibration",
            "g_00 calibration and spatial curvature use same Hilbert/worldtube source charge",
            "needed to prevent a hidden source-frame split in gamma",
            "not_parent_signed",
            "use Hilbert-worldtube/PiM source equality route",
        ),
        (
            "SIG932_3_regular_compact_matching",
            "no incoming homogeneous l>=2 slip modes on the compact exterior",
            "needed so D_ij(Phi-Psi)=0 implies Phi-Psi=0",
            "boundary_condition_contract_only",
            "derive local representative/boundary condition from parent quotient",
        ),
        (
            "SIG932_4_XFM_source_owned",
            "X_FM finite and source-owned, not chosen per experiment",
            "needed if gamma-zero fails and bound envelope is scored",
            "missing",
            "derive A_M, dPiMJ, B_zero_flux, N_FM, N_B inputs",
        ),
    ]
    rows = []
    for signature_id, clause, why_needed, current_status, next_action in specs:
        rows.append(
            {
                "signature_id": signature_id,
                "parent_clause": clause,
                "why_needed": why_needed,
                "current_status": current_status,
                "promotion_allowed_now": "false",
                "next_action": next_action,
                "valid_for_claim": "false",
                "generated_utc": stamp(),
            }
        )
    return rows


def pivot_decisions() -> list[dict[str, str]]:
    return [
        {
            "decision_id": "DEC932_0_gamma_zero_status",
            "decision": "conditional_gamma_zero_route_found",
            "reason": "no-slip plus scalar-only boundary stress gives a_FM=b_FM and C_gamma_FM=0",
            "consequence": "gamma can be structurally safe if the parent signs the N2/no-shear clauses",
            "next_action": "derive scalar-only boundary owner from current parent variables",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC932_1_no_public_gamma_pass",
            "decision": "do_not_promote_gamma_pass",
            "reason": "the scalar boundary owner and same-source calibration are not parent-derived for current MTS",
            "consequence": "gamma remains conditional; KBFH bound envelope remains symbolic",
            "next_action": "retain claim gates false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC932_2_beta_WEP_pivot",
            "decision": "beta_is_next_after_gamma_zero_attempt",
            "reason": "229 already reduced beta to exterior vacuum-Einstein/no-hair once gamma/slip is trace-only; WEP is stronger but requires species/source-charge map",
            "consequence": "beta is the cleaner next local-GR coefficient; WEP remains a later harder arena",
            "next_action": "933-Y5-R10-scalar-boundary-owner-or-beta-vacuum-Einstein-gate.md",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def claim_gates() -> list[dict[str, str]]:
    return [
        {
            "gate_id": "CGATE932_0_gamma_zero",
            "claim": "C_gamma_FM=0 is derived for current MTS",
            "evidence": "conditional theorem exists but parent scalar-boundary owner and source calibration are unsigned",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CGATE932_1_gamma_bound_numeric",
            "claim": "gamma row gives numeric KBFH bound",
            "evidence": "C_gamma_FM and X_FM remain symbolic",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CGATE932_2_beta_pass",
            "claim": "beta=1 follows after gamma zero",
            "evidence": "beta still needs exterior vacuum-Einstein/no-hair gate",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CGATE932_3_WEP_pass",
            "claim": "WEP/source-charge safety follows",
            "evidence": "species/source-charge projection remains harder and not derived",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def formalization_changed_after_start() -> int:
    if not FORMALIZATION.exists():
        return -1
    changed_count = 0
    for candidate_path in FORMALIZATION.rglob("*"):
        if not candidate_path.is_file():
            continue
        modified_time = datetime.fromtimestamp(candidate_path.stat().st_mtime, timezone.utc)
        if modified_time > SCRIPT_START_UTC:
            changed_count += 1
    return changed_count


def validation(
    sources: list[dict[str, str]],
    theorem_rows: list[dict[str, str]],
    signature_rows: list[dict[str, str]],
    decision_rows: list[dict[str, str]],
    gate_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    rows = []

    def add(check_id: str, passed: bool, detail: str) -> None:
        rows.append({"check_id": check_id, "result": "pass" if passed else "fail", "detail": detail, "generated_utc": stamp()})

    sources_ok = all(row["exists"] == "true" and row["needle_found"] == "true" for row in sources)
    prior_validation = read_csv(OUT / "P8_Y5_BRR545_931_VALIDATION.csv")
    prior_clean = prior_validation and all(row.get("result") == "pass" for row in prior_validation)
    conditional_zero_written = any(
        row["theorem_id"] == "GZ932_3_equal_response" and "C_gamma_FM=0" in row["derived_result"]
        for row in theorem_rows
    )
    fallback_retained = any(row["theorem_id"] == "GZ932_4_bound_fallback" for row in theorem_rows)
    signature_blocked = signature_rows and all(row["promotion_allowed_now"] == "false" for row in signature_rows)
    beta_selected = any("933-Y5-R10-scalar-boundary-owner" in row["next_action"] for row in decision_rows)
    no_claims = all(row["valid_for_claim"] == "false" for row in theorem_rows + signature_rows + decision_rows + gate_rows)
    gates_false = gate_rows and all(row["claim_allowed"] == "false" for row in gate_rows)
    formalization_changed = formalization_changed_after_start()

    add("V932_0_sources_exist_and_needles", sources_ok, "all source paths exist and needles are present" if sources_ok else "missing source path or needle")
    add("V932_1_prior_931_clean", prior_clean, "P8_Y5_BRR545_931_VALIDATION.csv clean")
    add("V932_2_conditional_gamma_zero_written", conditional_zero_written, "C_gamma_FM=0 conditional theorem written")
    add("V932_3_gamma_bound_fallback_retained", fallback_retained, "symbolic gamma KBFH envelope retained")
    add("V932_4_parent_signature_blocked", signature_blocked, "parent signature audit forbids promotion now")
    add("V932_5_beta_next_selected", beta_selected, "933 scalar-boundary/beta gate selected")
    add("V932_6_no_claims_promoted", no_claims, "all generated rows are nonclaim")
    add("V932_7_claim_gates_false", gates_false, "all claim gates remain false")
    add("V932_8_formalization_workbench_untouched", formalization_changed == 0, f"formalization_changed_after_start={formalization_changed}")
    add("V932_9_validation_rows_ready", True, "validation table constructed")
    return rows


def write_doc(
    sources: list[dict[str, str]],
    theorem_rows: list[dict[str, str]],
    signature_rows: list[dict[str, str]],
    decision_rows: list[dict[str, str]],
    gate_rows: list[dict[str, str]],
    validation_rows: list[dict[str, str]],
) -> None:
    text = f"""# 932 - Y5/R10 Gamma Zero Parent Condition Or Beta/WEP Pivot

Generated: `{stamp()}`

Status: `Y5_R10_932_conditional_gamma_zero_theorem_found_parent_signature_missing_beta_next`

Claim ceiling: `conditional_no_slip_gamma_zero_only_no_numeric_KBFH_no_gamma_beta_WEP_or_local_GR_pass`

## Result

This is a useful one.

The `931` gamma projection says:

```text
C_gamma_FM = b_FM - a_FM.
```

The older no-slip branch gives the exact sufficient condition for killing it:

```text
D_ij(Phi-Psi) = 8*pi*G*pi_ij^TF,
pi_ij^TF = 0,
no incoming homogeneous l>=2 slip mode
=> Phi=Psi
=> a_FM=b_FM
=> C_gamma_FM=0.
```

So the gamma row has a respectable **conditional zero route**, not just a bound route. But it is not a current MTS claim, because the parent action still has to derive the scalar-only compact boundary variable set, same-source calibration, no trace-free/tangential channel, and regular compact matching.

If that parent signature cannot be closed, the retained fallback is still:

```text
|K_BF_H| <= 2.3e-05/(|C_gamma_FM| X_FM).
```

The next clean target is beta, not WEP: beta follows the same local-GR spine via exterior vacuum-Einstein/no-hair, while WEP needs the harder species/source-charge map.

## Source Register

{md_table(sources, ["source_id", "path", "role", "needle_found", "valid_for_claim"])}

## Gamma-Zero Theorem Attempt

{md_table(theorem_rows, ["theorem_id", "premise_or_step", "mathematical_form", "derived_result", "status", "valid_for_claim"])}

## Parent Signature Audit

{md_table(signature_rows, ["signature_id", "parent_clause", "why_needed", "current_status", "promotion_allowed_now", "next_action"])}

## Decision Ledger

{md_table(decision_rows, ["decision_id", "decision", "reason", "consequence", "next_action", "valid_for_claim"])}

## Claim Gates

{md_table(gate_rows, ["gate_id", "claim", "evidence", "claim_allowed", "valid_for_claim"])}

## Validation

{md_table(validation_rows, ["check_id", "result", "detail", "generated_utc"])}

## Next Target

`933-Y5-R10-scalar-boundary-owner-or-beta-vacuum-Einstein-gate.md`

Try to parent-sign the scalar-only boundary owner. If that remains unsigned, use the beta vacuum-Einstein/no-hair gate as the next retained local-GR coefficient route.
"""
    DOC.write_text(text, encoding="utf-8")


def main() -> None:
    sources = source_register()
    theorem_rows = theorem_attempt()
    signature_rows = parent_signature_audit()
    decision_rows = pivot_decisions()
    gate_rows = claim_gates()
    validation_rows = validation(sources, theorem_rows, signature_rows, decision_rows, gate_rows)

    write_csv(
        OUT / "P8_Y5_R10_932_SOURCE_REGISTER.csv",
        sources,
        ["source_id", "path", "absolute_path", "role", "needle", "exists", "needle_found", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_R10_932_GAMMA_ZERO_THEOREM_ATTEMPT.csv",
        theorem_rows,
        ["theorem_id", "premise_or_step", "mathematical_form", "derived_result", "status", "missing_for_claim", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_R10_932_PARENT_SIGNATURE_AUDIT.csv",
        signature_rows,
        ["signature_id", "parent_clause", "why_needed", "current_status", "promotion_allowed_now", "next_action", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_R10_932_DECISION_LEDGER.csv",
        decision_rows,
        ["decision_id", "decision", "reason", "consequence", "next_action", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_R10_932_CLAIM_GATE.csv",
        gate_rows,
        ["gate_id", "claim", "evidence", "claim_allowed", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_R10_932_NEXT_TARGET.csv",
        [
            {
                "next_target": "933-Y5-R10-scalar-boundary-owner-or-beta-vacuum-Einstein-gate.md",
                "objective": "parent-sign scalar-only boundary/no-shear owner or move to beta exterior vacuum-Einstein/no-hair gate",
                "include": "Y_scalar parent variable set, no trace-free/tangential channels, same-source calibration, beta vacuum-Einstein/no-hair fallback",
                "exclude": "gamma pass claim, beta pass claim, WEP source-charge claim, numeric KBFH without Cgamma/XFM, GitHub action, formalization-workbench edits",
                "valid_for_claim": "false",
                "generated_utc": stamp(),
            }
        ],
        ["next_target", "objective", "include", "exclude", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_BRR545_932_VALIDATION.csv",
        validation_rows,
        ["check_id", "result", "detail", "generated_utc"],
    )
    write_doc(sources, theorem_rows, signature_rows, decision_rows, gate_rows, validation_rows)

    failures = [row for row in validation_rows if row["result"] != "pass"]
    if failures:
        raise SystemExit(f"validation failed: {failures}")
    print("Y5_R10_932_conditional_gamma_zero_theorem_found_parent_signature_missing_beta_next")
    print(f"wrote {DOC}")
    print("next target: 933-Y5-R10-scalar-boundary-owner-or-beta-vacuum-Einstein-gate.md")


if __name__ == "__main__":
    main()
