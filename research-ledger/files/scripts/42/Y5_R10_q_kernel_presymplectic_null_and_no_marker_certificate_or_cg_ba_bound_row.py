from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds" / "local_bound_claims.csv"
DOC = ROOT / "946-Y5-R10-q-kernel-presymplectic-null-and-no-marker-certificate-or-cg-ba-bound-row.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
SCRIPT_START_UTC = datetime.now(timezone.utc)


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def flag(value: bool) -> str:
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


def local_bound(row_id: str) -> dict[str, str]:
    for row in read_csv(LOCAL_BOUNDS):
        if row.get("row_id") == row_id:
            return row
    return {}


def source_register() -> list[dict[str, str]]:
    specs = [
        {
            "source_id": "945_doc",
            "path": "945-Y5-R10-parent-q-map-Obs-e-functor-construction-or-first-frame-leak-bound-pack.md",
            "role": "handoff selecting q-kernel null/no-marker certificate",
            "needle": "ker(Dq_candidate) is presymplectic-null",
        },
        {
            "source_id": "945_validation",
            "path": "source-intake/mts_residuals/P8_Y5_BRR545_945_VALIDATION.csv",
            "role": "previous checkpoint validation",
            "needle": "V945_12_validation_rows_ready",
        },
        {
            "source_id": "945_kernel",
            "path": "source-intake/mts_residuals/P8_Y5_R10_945_KERNEL_TEST.csv",
            "role": "candidate q-kernel test rows",
            "needle": "KT945_6_total_kernel",
        },
        {
            "source_id": "945_bound_rows",
            "path": "source-intake/mts_residuals/P8_Y5_R10_945_FIRST_FRAME_LEAK_BOUND_ROWS.csv",
            "role": "first frame-leak bound-row schemas",
            "needle": "BND945_0_cg_value",
        },
        {
            "source_id": "272_quotient_principle",
            "path": "272-quotient-configuration-principle-from-topological-projector.md",
            "role": "conditional presymplectic quotient route",
            "needle": "Cperp exactness",
        },
        {
            "source_id": "341_cell_quotient",
            "path": "341-indistinguishable-cell-quotient-parent-action-gate.md",
            "role": "finite-cell quotient marker hazard",
            "needle": "Marker Extension Hazard",
        },
        {
            "source_id": "415_local_class",
            "path": "415-local-trivial-class-selector-theorem-attempt.md",
            "role": "local trivial class selector obstruction",
            "needle": "physical_local_class_selector_derived",
        },
        {
            "source_id": "710_frame_guard",
            "path": "710-Y5-R10-scalar-class-zero-premise-parent-action-clause-or-frame-transfer-guard.md",
            "role": "scalar/class frame-transfer guard",
            "needle": "DPC710_9_verdict",
        },
        {
            "source_id": "boundary_672",
            "path": "source-intake/mts_residuals/P8_Y5_R10_672_BOUNDARY_EXACTNESS_ATTEMPT.csv",
            "role": "boundary exactness and edge-charge obstruction",
            "needle": "BE672_6_verdict",
        },
        {
            "source_id": "boundary_890",
            "path": "source-intake/mts_residuals/P8_Y5_R10_890_BOUNDARY_NO_TAIL_THEOREM_ATTEMPT.csv",
            "role": "boundary no-tail theorem attempt",
            "needle": "NT890_5_no_tail_corollary",
        },
        {
            "source_id": "marker_736",
            "path": "source-intake/mts_residuals/P8_Y5_R10_736_MATTER_NO_MARKER_CONTRACT.csv",
            "role": "matter no-marker contract",
            "needle": "NMC736_0_allowed_functor_domain",
        },
        {
            "source_id": "marker_763",
            "path": "source-intake/mts_residuals/P8_Y5_R10_763_NO_MARKER_SPURION_THEOREM_ATTEMPT.csv",
            "role": "no-marker/no-spurion theorem attempt",
            "needle": "NMS763_6_verdict",
        },
        {
            "source_id": "cokernel_897",
            "path": "source-intake/mts_residuals/P8_Y5_R10_897_SOURCE_COKERNEL_PROOF_ATTEMPT.csv",
            "role": "source-cokernel proof attempt",
            "needle": "SCA897_4_verdict",
        },
        {
            "source_id": "cokernel_903",
            "path": "source-intake/mts_residuals/P8_Y5_R10_903_SOURCE_COKERNEL_PAIRING_TEST.csv",
            "role": "source-cokernel pairing test",
            "needle": "SCP903_5_verdict",
        },
        {
            "source_id": "local_bounds",
            "path": "source-intake/local_bounds/local_bound_claims.csv",
            "role": "local empirical bound anchors for fallback interface",
            "needle": "MICROSCOPE_final_TiPt",
        },
    ]
    rows = []
    for spec in specs:
        path = ROOT / spec["path"]
        exists = path.exists()
        needle_found = exists and spec["needle"] in read_text(path)
        rows.append(
            {
                **spec,
                "absolute_path": str(path),
                "exists": flag(exists),
                "needle_found": flag(needle_found),
                "valid_for_claim": "false",
                "generated_utc": stamp(),
            }
        )
    return rows


def kernel_certificate_audit() -> list[dict[str, str]]:
    specs = [
        (
            "KCERT946_0_bulk_presymplectic_null",
            "i_v Omega_parent=0 for candidate kernel directions",
            "conditional support for exact/topological Cperp shifts only",
            "partial_conditional_not_total",
            "Cperp exactness, finite-cell origin, local class, and scalar/class directions are not all null-certified",
        ),
        (
            "KCERT946_1_boundary_primitive_zero",
            "i_v Theta_parent=dB_v and int_boundary dB_v=0",
            "proper compact variations have conditional support",
            "not_parent_signed",
            "measured edge/source boundary flux and exact primitive are not proved",
        ),
        (
            "KCERT946_2_no_marker",
            "no matter-visible marker/spurion survives in ker(Dq_candidate)",
            "no-marker contracts exist",
            "contract_only",
            "marker constants, species weights, clock constants, and non-Hilbert currents remain unclassified",
        ),
        (
            "KCERT946_3_matter_invisibility",
            "Lie_v S_matter=0 for all ordinary matter/readout standards",
            "source-cokernel chain rule is valid conditionally",
            "conditional_not_parent_signed",
            "q_loc verticality, matter descent, geometry stack, constants, and no-tail are unsigned",
        ),
        (
            "KCERT946_4_local_trivial_class",
            "local relative/domain class has no physical compact generator",
            "fixed-class/zero-class theorem shape exists",
            "not_derived",
            "domain selector, topology/no-defect premise, and boundary exchange no-hair remain open",
        ),
        (
            "KCERT946_5_no_frame_transfer",
            "no F(sigma)R, A_g(X), B_A(sigma), clock/readout transfer survives",
            "frame-transfer guard exists",
            "not_parent_signed",
            "Einstein-frame-style rewrites can hide matter/clock/source couplings",
        ),
        (
            "KCERT946_6_total",
            "ker(Dq_candidate) is gauge/null, marker-free, matter-invisible, and boundary-silent",
            "all certificates KCERT946_0 through KCERT946_5 close",
            "certificate_failed_current_corpus",
            "q_candidate cannot be promoted to physical parent quotient",
        ),
    ]
    return [
        {
            "certificate_id": certificate_id,
            "required_statement": required_statement,
            "best_evidence": best_evidence,
            "current_status": current_status,
            "remaining_gap": remaining_gap,
            "passes_certificate": "false",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
        for certificate_id, required_statement, best_evidence, current_status, remaining_gap in specs
    ]


def partial_positive_register() -> list[dict[str, str]]:
    specs = [
        (
            "POS946_0_chain_rule",
            "If S_matter descends through q and v in ker(Dq), then the matter pairing vanishes.",
            "Lie_v S_matter=<Dq[v],dSbar/dq>=0",
            "valid_conditional_theorem",
            "useful but not parent ownership",
        ),
        (
            "POS946_1_proper_boundary",
            "Proper compact-local kernel variations can have zero edge charge.",
            "epsilon|boundary=0 or exact boundary form on closed shell",
            "conditional_support",
            "does not kill measured/improper edge modes",
        ),
        (
            "POS946_2_no_marker_contract",
            "No-shadow/no-marker rules give the correct anti-cheat taxonomy.",
            "visible marker is absent, gauge, Q-only, zero-projection auxiliary, or retained",
            "contract_shape_good",
            "classification not parent-derived",
        ),
        (
            "POS946_3_source_cokernel",
            "Source-cokernel criterion is mathematically exact.",
            "J_A in Range(Dq)^* and v in ker(Dq) => <v,J_A>=0",
            "valid_conditional_theorem",
            "q verticality and matter descent not signed",
        ),
        (
            "POS946_4_bound_interface",
            "Local empirical anchors already exist for WEP, clocks, PPN, Gdot, and symbolic R10.",
            "local_bound_claims.csv provides source URLs and upper bounds",
            "source_anchors_available",
            "not enough without MTS coefficient and arena projection",
        ),
    ]
    return [
        {
            "positive_id": positive_id,
            "statement": statement,
            "mathematical_form": mathematical_form,
            "status": status,
            "limit": limit,
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
        for positive_id, statement, mathematical_form, status, limit in specs
    ]


def cg_ba_bound_interface() -> list[dict[str, str]]:
    row_specs = [
        (
            "CGB946_0_cg_R10",
            "c_g",
            "R10_fifth_force",
            "representative Weyl/common-frame coefficient projected into Yukawa alpha(lambda)",
            "alpha_R10(lambda)=K_X(lambda) Qbar_XH tau_R10 c_g",
            "MISSING_PARENT_CG_AND_TAU_R10",
        ),
        (
            "CGB946_1_cg_PPN_gamma",
            "c_g",
            "R3_gamma",
            "common-frame coefficient projected into PPN gamma residual",
            "gamma_minus_1 ~ M_gamma(lambda,profile) tau_PPN c_g",
            "MISSING_PARENT_CG_AND_PPN_PROJECTION",
        ),
        (
            "CGB946_2_cg_PPN_beta",
            "c_g",
            "R4_beta",
            "common-frame coefficient projected into second-order beta residual",
            "beta_minus_1 ~ M_beta(lambda,profile) tau_beta c_g",
            "MISSING_PARENT_CG_AND_BETA_KERNEL",
        ),
        (
            "CGB946_3_bA_WEP",
            "b_A-b_B",
            "R1_WEP_source_charge",
            "species/material mass-constant derivative projected into Eotvos eta",
            "eta_AB ~ P_WEP(profile)(b_A-b_B)",
            "MISSING_SPECIES_CONSTANT_DESCENT_OR_NUMERIC_BA",
        ),
        (
            "CGB946_4_bA_clock",
            "b_A;b_alpha",
            "R2_clock_redshift",
            "clock/constant sensitivity to representative label",
            "delta_clock ~ S_alpha b_alpha + S_mass b_A",
            "MISSING_CLOCK_CONSTANT_DESCENT_OR_NUMERIC_SENSITIVITY",
        ),
    ]
    rows = []
    for row_id, symbol, bound_row_id, meaning, formula, status in row_specs:
        bound = local_bound(bound_row_id)
        rows.append(
            {
                "interface_id": row_id,
                "symbol": symbol,
                "bound_row_id": bound_row_id,
                "meaning": meaning,
                "score_formula": formula,
                "bound_value_or_curve": bound.get("upper_bound", ""),
                "bound_units": bound.get("units", ""),
                "bound_source": bound.get("reference_path_or_url", ""),
                "bound_anchor_loaded": flag(bool(bound)),
                "current_status": status,
                "source_path": "MISSING_PARENT_SOURCE",
                "numeric_value": "MISSING_PARENT_INPUT",
                "arena_projection": "MISSING_ARENA_PROJECTION",
                "score_ready": "false",
                "claim_allowed": "false",
                "valid_for_claim": "false",
                "generated_utc": stamp(),
            }
        )
    return rows


def decisions() -> list[dict[str, str]]:
    return [
        {
            "decision_id": "DEC946_0_kernel_certificate",
            "decision": "q_kernel_certificate_failed_current_corpus",
            "reason": "bulk null, boundary zero, no-marker, matter invisibility, local trivial class, and frame-transfer guards are each conditional or unsigned",
            "consequence": "q_candidate remains useful notation/target but not a physical parent quotient proof",
            "next_action": "do not promote quotient descent or frame-leak zero",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC946_1_partial_positives",
            "decision": "partial_conditional_theorems_preserved",
            "reason": "chain-rule source-cokernel, proper-boundary silence, and no-marker taxonomy are mathematically useful when their premises are signed",
            "consequence": "the route remains worth pursuing, but only as parent-signature work or labelled closure",
            "next_action": "target the weakest missing certificate or source coefficients",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC946_2_bound_interface",
            "decision": "cg_ba_bound_interface_written_nonclaim",
            "reason": "local empirical anchors exist, but MTS coefficients and arena projections are missing",
            "consequence": "first data-facing rows for c_g and b_A are ready as schemas, not evidence",
            "next_action": "947-Y5-R10-cg-ba-bound-interface-projection-fill-or-no-marker-kernel-repair.md",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def claim_gates() -> list[dict[str, str]]:
    return [
        {
            "gate_id": "CGATE946_0_q_kernel",
            "claim": "ker(Dq_candidate) is a physical gauge/null kernel",
            "blocker": "total certificate failed; multiple kernel directions are only conditional or explicit counterexamples",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CGATE946_1_frame_leak_zero",
            "claim": "c_g=b_A=b_dis=q_nonH=0",
            "blocker": "no-marker/matter descent/frame-transfer certificates are not parent-signed",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CGATE946_2_bound_score",
            "claim": "c_g/b_A rows can be scored against local bounds",
            "blocker": "parent coefficients and arena projections are MISSING even when empirical bound anchors exist",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CGATE946_3_worldtube_selector",
            "claim": "same observed source worldtube is parent-derived",
            "blocker": "q-kernel and matter descent remain unsigned, so W_source=supp(J_H) is still conditional",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CGATE946_4_local_GR",
            "claim": "local GR/Newton/PPN reduction is derived",
            "blocker": "q-kernel ownership, frame-leak zero/bounds, source glue, measured-GM calibration, and PPN stability remain open",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def next_target() -> list[dict[str, str]]:
    return [
        {
            "next_target": "947-Y5-R10-cg-ba-bound-interface-projection-fill-or-no-marker-kernel-repair.md",
            "objective": "either fill real arena projections for the nonclaim c_g/b_A bound interface, or attack the no-marker/kernel repair certificate that would make those coefficients theorem-zero",
            "include": "tau_R10, tau_PPN, WEP material projection, clock sensitivity, c_g and b_A source paths, no-marker constants theorem, boundary no-tail, source-cokernel owner",
            "exclude": "claiming q-kernel pass, treating local bounds as MTS evidence without coefficients, hiding marker/frame leaks, local-GR claim, GitHub action, formalization-workbench edits",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
    ]


def formalization_changed_after_start() -> int:
    if not FORMALIZATION.exists():
        return -1
    changed = 0
    for path in FORMALIZATION.rglob("*"):
        if not path.is_file():
            continue
        modified = datetime.fromtimestamp(path.stat().st_mtime, timezone.utc)
        if modified > SCRIPT_START_UTC:
            changed += 1
    return changed


def validation(
    sources: list[dict[str, str]],
    certificate_rows: list[dict[str, str]],
    positive_rows: list[dict[str, str]],
    interface_rows: list[dict[str, str]],
    decision_rows: list[dict[str, str]],
    claim_rows: list[dict[str, str]],
    target_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    rows = []

    def add(check_id: str, passed: bool, detail: str) -> None:
        rows.append({"check_id": check_id, "result": "pass" if passed else "fail", "detail": detail, "generated_utc": stamp()})

    prior = read_csv(OUT / "P8_Y5_BRR545_945_VALIDATION.csv")
    prior_clean = prior and all(row.get("result") == "pass" for row in prior)
    sources_ok = all(row["exists"] == "true" and row["needle_found"] == "true" for row in sources)
    total_failed = any(row["certificate_id"] == "KCERT946_6_total" and row["current_status"] == "certificate_failed_current_corpus" for row in certificate_rows)
    no_certificate_pass = all(row["passes_certificate"] == "false" for row in certificate_rows)
    partials_present = len(positive_rows) >= 5 and all(row["valid_for_claim"] == "false" for row in positive_rows)
    bounds_anchored = any(row["interface_id"] == "CGB946_3_bA_WEP" and row["bound_anchor_loaded"] == "true" for row in interface_rows) and any(row["interface_id"] == "CGB946_0_cg_R10" and row["bound_anchor_loaded"] == "true" for row in interface_rows)
    bounds_blocked = interface_rows and all(row["score_ready"] == "false" and row["claim_allowed"] == "false" for row in interface_rows)
    decisions_nonclaim = all(row["valid_for_claim"] == "false" for row in decision_rows)
    claims_false = all(row["claim_allowed"] == "false" and row["valid_for_claim"] == "false" for row in claim_rows)
    next_selected = any(row["next_target"].startswith("947-Y5-R10-cg-ba-bound-interface") for row in target_rows)
    no_claims = all(
        row.get("valid_for_claim") == "false"
        for row in sources + certificate_rows + positive_rows + interface_rows + decision_rows + claim_rows + target_rows
    )
    formalization_changed = formalization_changed_after_start()

    add("V946_0_sources_exist_and_needles", sources_ok, "all 946 source paths exist and needles are present" if sources_ok else "missing source path or needle")
    add("V946_1_prior_945_clean", prior_clean, "P8_Y5_BRR545_945_VALIDATION.csv clean")
    add("V946_2_kernel_certificate_failed", total_failed, "q-kernel total certificate failed in current corpus")
    add("V946_3_no_certificate_pass", no_certificate_pass, "no certificate row promoted")
    add("V946_4_partial_positives_retained", partials_present, "conditional positives recorded without claim promotion")
    add("V946_5_bound_anchors_loaded", bounds_anchored, "R10 and WEP local bound anchors loaded")
    add("V946_6_bound_rows_blocked", bounds_blocked, "c_g/b_A interface rows remain non-scoreable")
    add("V946_7_decisions_nonclaim", decisions_nonclaim, "decision ledger remains nonclaim")
    add("V946_8_claim_gates_false", claims_false, "all claim gates remain false")
    add("V946_9_next_target_selected", next_selected, "947 c_g/b_A projection or no-marker repair target selected")
    add("V946_10_no_claims_promoted", no_claims, "all generated rows are valid_for_claim=false")
    add("V946_11_formalization_workbench_untouched", formalization_changed == 0, f"formalization_changed_after_start={formalization_changed}")
    add("V946_12_validation_rows_ready", True, "validation table constructed")
    return rows


def write_doc(
    sources: list[dict[str, str]],
    certificate_rows: list[dict[str, str]],
    positive_rows: list[dict[str, str]],
    interface_rows: list[dict[str, str]],
    decision_rows: list[dict[str, str]],
    claim_rows: list[dict[str, str]],
    target_rows: list[dict[str, str]],
    validation_rows: list[dict[str, str]],
) -> None:
    text = f"""# 946 - Y5/R10 q-Kernel Presymplectic Null And No-Marker Certificate Or c_g/b_A Bound Row

Generated: `{stamp()}`

Status: `Y5_R10_946_q_kernel_certificate_failed_partial_conditionals_retained_cg_ba_bound_interface_written_nonclaim`

Claim ceiling: `q_kernel_certificate_gate_only_no_frame_leak_zero_no_bound_score_no_local_GR_pass`

## Result

946 tests the actual certificate behind the candidate quotient map:

```text
ker(Dq_candidate) must be presymplectic-null,
i_v Theta_parent = dB_v with zero compact flux,
Lie_v S_matter = 0,
and no matter-visible marker/Weyl/disformal/mass channel may survive.
```

The total certificate fails in the current corpus. There are useful partial positives: the source-cokernel chain rule is valid conditionally, proper compact boundary variations can be silent, and the no-marker taxonomy is the right anti-cheat rule. But none of those signs the full parent kernel.

So `q_candidate` remains a good theorem target, not a GR proof. The retained empirical fallback is now clearer:

```text
c_g -> R10/PPN/clock/WEP projections,
b_A -> WEP/clock/composition projections.
```

Local bound anchors exist, but the MTS coefficients and arena projections are still missing. Therefore the bound rows are data-interface scaffolding, not evidence.

## Source Register

{md_table(sources, ["source_id", "path", "role", "needle_found", "valid_for_claim"])}

## Kernel Certificate Audit

{md_table(certificate_rows, ["certificate_id", "required_statement", "best_evidence", "current_status", "remaining_gap", "passes_certificate"])}

## Partial Positive Register

{md_table(positive_rows, ["positive_id", "statement", "mathematical_form", "status", "limit"])}

## c_g/b_A Bound Interface

{md_table(interface_rows, ["interface_id", "symbol", "bound_row_id", "score_formula", "bound_value_or_curve", "bound_anchor_loaded", "current_status", "score_ready"])}

## Decision Ledger

{md_table(decision_rows, ["decision_id", "decision", "reason", "consequence", "next_action", "valid_for_claim"])}

## Claim Gates

{md_table(claim_rows, ["gate_id", "claim", "blocker", "claim_allowed", "valid_for_claim"])}

## Validation

{md_table(validation_rows, ["check_id", "result", "detail", "generated_utc"])}

## Next Target

{md_table(target_rows, ["next_target", "objective", "include", "exclude", "valid_for_claim"])}
"""
    DOC.write_text(text, encoding="utf-8")


def ensure_csv_roundtrip(paths: list[Path]) -> None:
    for path in paths:
        rows = read_csv(path)
        if rows and any(None in row for row in rows):
            raise SystemExit(f"malformed CSV row in {path}")


def main() -> None:
    sources = source_register()
    certificate_rows = kernel_certificate_audit()
    positive_rows = partial_positive_register()
    interface_rows = cg_ba_bound_interface()
    decision_rows = decisions()
    claim_rows = claim_gates()
    target_rows = next_target()
    validation_rows = validation(sources, certificate_rows, positive_rows, interface_rows, decision_rows, claim_rows, target_rows)

    output_specs = [
        (
            OUT / "P8_Y5_R10_946_SOURCE_REGISTER.csv",
            sources,
            ["source_id", "path", "absolute_path", "role", "needle", "exists", "needle_found", "valid_for_claim", "generated_utc"],
        ),
        (
            OUT / "P8_Y5_R10_946_KERNEL_CERTIFICATE_AUDIT.csv",
            certificate_rows,
            ["certificate_id", "required_statement", "best_evidence", "current_status", "remaining_gap", "passes_certificate", "claim_allowed", "valid_for_claim", "generated_utc"],
        ),
        (
            OUT / "P8_Y5_R10_946_PARTIAL_POSITIVE_REGISTER.csv",
            positive_rows,
            ["positive_id", "statement", "mathematical_form", "status", "limit", "valid_for_claim", "generated_utc"],
        ),
        (
            OUT / "P8_Y5_R10_946_CG_BA_BOUND_INTERFACE.csv",
            interface_rows,
            ["interface_id", "symbol", "bound_row_id", "meaning", "score_formula", "bound_value_or_curve", "bound_units", "bound_source", "bound_anchor_loaded", "current_status", "source_path", "numeric_value", "arena_projection", "score_ready", "claim_allowed", "valid_for_claim", "generated_utc"],
        ),
        (
            OUT / "P8_Y5_R10_946_DECISION_LEDGER.csv",
            decision_rows,
            ["decision_id", "decision", "reason", "consequence", "next_action", "valid_for_claim", "generated_utc"],
        ),
        (
            OUT / "P8_Y5_R10_946_CLAIM_GATE.csv",
            claim_rows,
            ["gate_id", "claim", "blocker", "claim_allowed", "valid_for_claim", "generated_utc"],
        ),
        (
            OUT / "P8_Y5_R10_946_NEXT_TARGET.csv",
            target_rows,
            ["next_target", "objective", "include", "exclude", "valid_for_claim", "generated_utc"],
        ),
        (
            OUT / "P8_Y5_BRR545_946_VALIDATION.csv",
            validation_rows,
            ["check_id", "result", "detail", "generated_utc"],
        ),
    ]

    for path, rows, fieldnames in output_specs:
        write_csv(path, rows, fieldnames)

    ensure_csv_roundtrip([path for path, _rows, _fieldnames in output_specs])
    write_doc(sources, certificate_rows, positive_rows, interface_rows, decision_rows, claim_rows, target_rows, validation_rows)

    failures = [row for row in validation_rows if row["result"] != "pass"]
    if failures:
        raise SystemExit(f"validation failed: {failures}")

    print("Y5_R10_946_q_kernel_certificate_failed_partial_conditionals_retained_cg_ba_bound_interface_written_nonclaim")
    print(f"wrote {DOC}")
    print("next target: 947-Y5-R10-cg-ba-bound-interface-projection-fill-or-no-marker-kernel-repair.md")


if __name__ == "__main__":
    main()
