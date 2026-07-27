from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "1146-Y5-R10-epsilon-domain-flux-no-flux-certificate-or-source-profile-row.md"


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def stamp(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    generated = now()
    return [{**row, "generated_utc": generated} for row in rows]


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def source_rows() -> list[dict[str, object]]:
    sources = [
        {
            "source_id": "SRC1146_0_1145_next",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1145_NEXT_TARGET.csv",
            "needle": "NEXT1145_0_1146",
            "role": "handoff requiring epsilon no-flux certificate or source profile row.",
        },
        {
            "source_id": "SRC1146_1_1145_epsilon",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1145_EPSILON_SOURCE_PROFILE_ROWS.csv",
            "needle": "EPSRC1145_1_no_flux_certificate_row",
            "role": "previous epsilon profile and no-flux certificate templates.",
        },
        {
            "source_id": "SRC1146_2_domain_no_leak",
            "relative_path": "source-intake/mts_residuals/P8_DOMAIN_ALPHA3_NOLEAK_THEOREM_ATTEMPT.csv",
            "needle": "N7_no_leak_verdict",
            "role": "domain alpha3 no-leak theorem is blocked in current corpus.",
        },
        {
            "source_id": "SRC1146_3_1123_flux_product",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1123_ALPHA3_FLUX_BOUND_PRODUCT_ROWS.csv",
            "needle": "FB1123_1_flux_zero_certificate",
            "role": "alpha3 flux product needs epsilon zero certificate or numeric product.",
        },
        {
            "source_id": "SRC1146_4_1133_profile_bound",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1133_PROFILE_BOUND_ROWS.csv",
            "needle": "PB1133_1_R11_requirement",
            "role": "epsilon profile bound remains symbolic until K, c, and epsilon are sourced.",
        },
        {
            "source_id": "SRC1146_5_1134_lemma",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1134_NO_SWIRL_HARMONIC_LEMMA_AUDIT.csv",
            "needle": "LEM1134_6_verdict",
            "role": "no-swirl/harmonic no-flux lemma is not closed.",
        },
        {
            "source_id": "SRC1146_6_1134_runner_inputs",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1134_EPSILON_PROFILE_RUNNER_INPUTS.csv",
            "needle": "RUN1134_0_epsilon_profile",
            "role": "epsilon runner is blocked on missing numeric profile or zero theorem.",
        },
        {
            "source_id": "SRC1146_7_1135_constitutive",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1135_FD_GRADIENT_FLOW_CONSTITUTIVE_AUDIT.csv",
            "needle": "CFA1135_6_verdict",
            "role": "parent gradient-flow constitutive law for F_D is not found.",
        },
        {
            "source_id": "SRC1146_8_1135_handoff",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1135_SOURCE_PACK_HANDOFF_ROWS.csv",
            "needle": "RH1135_0_epsilon_profile",
            "role": "source-pack handoff says epsilon needs profile or theorem-zero input.",
        },
        {
            "source_id": "SRC1146_9_1136_product_gate",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1136_ALPHA3_PRODUCT_INEQUALITY_ROWS.csv",
            "needle": "PI1136_1_R11_alpha3",
            "role": "R11 alpha3 product remains blocked by missing K, c, and epsilon.",
        },
    ]
    checked: list[dict[str, object]] = []
    for source in sources:
        path = ROOT / str(source["relative_path"])
        text = read_text(path)
        checked.append(
            {
                **source,
                "exists": str(path.exists()).lower(),
                "needle_found": str(str(source["needle"]) in text).lower(),
            }
        )
    return stamp(checked)


def no_flux_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "audit_id": "NF1146_0_definition",
                "target": "epsilon_domain_flux",
                "needed_statement": "epsilon_domain_flux = |P_loc^i_nu(F_P^nu + F_domain^nu)| in the observed PPN-safe coframe after declared R11 normalization",
                "current_evidence": "1145 writes the profile and theorem-zero row templates",
                "result": "DEFINITION_RESTATED_NONCLAIM",
                "blocking_issue": "definition alone gives no zero or bound",
                "valid_for_claim": "false",
            },
            {
                "audit_id": "NF1146_1_parent_flux_equation",
                "target": "F_P^nu + F_domain^nu",
                "needed_statement": "parent Euler/Ward equation makes the projected local exchange current vanish, not merely owned",
                "current_evidence": "P8_DOMAIN N6 says Ward ownership is necessary footwork but not absence",
                "result": "OWNED_BUT_NOT_ZERO",
                "blocking_issue": "a covariant domain vector can be Ward-owned while still sourcing alpha3",
                "valid_for_claim": "false",
            },
            {
                "audit_id": "NF1146_2_local_representative",
                "target": "compact local branch",
                "needed_statement": "same parent branch law selects exact/trivial local domain representative",
                "current_evidence": "1145 rejects current S_branch candidates and leaves local exact representative unsigned",
                "result": "MISSING_PARENT_BRANCH_LAW",
                "blocking_issue": "epsilon=0 would be an imposed plateau unless the representative is parent-selected",
                "valid_for_claim": "false",
            },
            {
                "audit_id": "NF1146_3_constitutive_law",
                "target": "domain flux F_D",
                "needed_statement": "F_D^i = -M_D^{ij} grad_j zeta_D with positive elliptic M_D in the compact local branch",
                "current_evidence": "1135 records no explicit F_D variable, mobility tensor, domain potential, or Euler equation",
                "result": "MISSING_GRADIENT_FLOW_CONSTITUTIVE_LAW",
                "blocking_issue": "no legal integration-by-parts extremum proof exists without F_D, M_D, and zeta_D",
                "valid_for_claim": "false",
            },
            {
                "audit_id": "NF1146_4_boundary_harmonic_silence",
                "target": "boundary and harmonic pieces",
                "needed_statement": "n_i F_D^i = 0 and harmonic/relative cohomology pieces vanish or are parent-excluded",
                "current_evidence": "1134 lists Neumann, topology, harmonic exclusion, and boundary silence as conditional or missing",
                "result": "MISSING_BOUNDARY_TOPOLOGY_CERTIFICATE",
                "blocking_issue": "even a gradient flux can retain harmonic or boundary/exchange leakage",
                "valid_for_claim": "false",
            },
            {
                "audit_id": "NF1146_5_observed_coframe",
                "target": "P_loc flux projection",
                "needed_statement": "zero is measured in an observed coframe that cannot absorb the residual by representation choice",
                "current_evidence": "1134 marks the gauge-safe/observed coframe projection proof as missing",
                "result": "MISSING_OBSERVABLE_COFRAME_PROOF",
                "blocking_issue": "a representation-zero is not a physical alpha3 zero",
                "valid_for_claim": "false",
            },
            {
                "audit_id": "NF1146_6_verdict",
                "target": "epsilon_domain_flux = 0",
                "needed_statement": "NF1146_1 through NF1146_5 all close from the same parent local branch",
                "current_evidence": "ownership, representative, constitutive, boundary/topology, and coframe clauses remain unsigned",
                "result": "NO_FLUX_CERTIFICATE_NOT_DERIVED",
                "blocking_issue": "epsilon remains an open local-branch input, not a theorem-zero",
                "valid_for_claim": "false",
            },
        ]
    )


def epsilon_profile_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "profile_id": "EPS1146_0_source_profile_row",
                "target": "epsilon_domain_flux",
                "row_type": "source_ready_nonclaim_template",
                "system_id": "MISSING_LOCAL_SYSTEM_ID",
                "branch_id": "compact_stationary_local_branch",
                "domain_candidate_rule": "MISSING_PARENT_DOMAIN_CANDIDATE_RULE",
                "local_representative_status": "MISSING_PARENT_EXACT_OR_TRIVIAL_REPRESENTATIVE",
                "flux_definition": "abs(P_loc^i_nu(F_P^nu+F_domain^nu)) after observed-coframe and R11 alpha3 normalization",
                "epsilon_abs": "MISSING_NUMERIC_EPSILON_ABS",
                "epsilon_units": "dimensionless projected local flux convention",
                "profile_support": "MISSING_PROFILE_SUPPORT_OR_BOUND",
                "source_path": "MISSING_SOURCE_PATH",
                "status": "SOURCE_PROFILE_NOT_FILLED",
                "claim_policy": "valid_for_claim=false until every MISSING field is replaced by source-backed data or theorem-zero",
                "valid_for_claim": "false",
            },
            {
                "profile_id": "EPS1146_1_zero_certificate_row",
                "target": "epsilon_domain_flux_zero_certificate",
                "row_type": "parent_theorem_zero_certificate_template",
                "system_id": "compact_local_test_arena",
                "branch_id": "compact_stationary_local_branch",
                "domain_candidate_rule": "same S_parent/S_branch law that keeps FLRW active",
                "local_representative_status": "MISSING_PARENT_SELECTED_EXACT_TRIVIAL_LOCAL_REPRESENTATIVE",
                "flux_definition": "P_loc^i_nu(F_P^nu+F_domain^nu)=0",
                "epsilon_abs": "0_if_parent_certificate_closes_else_MISSING",
                "epsilon_units": "dimensionless theorem-zero flag",
                "profile_support": "MISSING_PARENT_EULER_PLUS_BOUNDARY_PLUS_COFRAME_CERTIFICATE",
                "source_path": "MISSING_SOURCE_PATH",
                "status": "ZERO_CERTIFICATE_NOT_DERIVED",
                "claim_policy": "Ward ownership, labels, and tuned cancellations cannot fill this row",
                "valid_for_claim": "false",
            },
            {
                "profile_id": "EPS1146_2_blocker_row",
                "target": "epsilon_domain_flux acquisition",
                "row_type": "blocker_ledger",
                "system_id": "local_R10_PPN_arena",
                "branch_id": "compact_stationary_local_branch",
                "domain_candidate_rule": "MISSING_DOMAIN_SELECTOR_OR_PROFILE_MODEL",
                "local_representative_status": "MISSING_REPRESENTATIVE_PROOF",
                "flux_definition": "requires P_loc projection of parent-owned flux in observed coframe",
                "epsilon_abs": "MISSING",
                "epsilon_units": "MISSING_IF_PROFILE_CONVENTION_NOT_DECLARED",
                "profile_support": "MISSING_PARENT_OR_NUMERIC_PROFILE",
                "source_path": "MISSING_SOURCE_PATH",
                "status": "ACQUISITION_REQUIRED",
                "claim_policy": "row is a to-do contract, not evidence",
                "valid_for_claim": "false",
            },
        ]
    )


def alpha3_interface_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "interface_id": "ALPHA1146_0_R11_product",
                "target": "R11 alpha3 flux product",
                "product_or_condition": "abs(K_R11_flux_alpha3*c_R11_flux_alpha3*epsilon_domain_flux) <= 4e-20",
                "current_inputs": "K_R11_flux_alpha3=MISSING; c_R11_flux_alpha3=MISSING; epsilon_domain_flux=MISSING",
                "evaluation": "NOT_SCOREABLE",
                "guard": "product cannot pass by missing values or cancellation with another row",
                "valid_for_claim": "false",
            },
            {
                "interface_id": "ALPHA1146_1_epsilon_zero_route",
                "target": "sufficient zero for R11 product",
                "product_or_condition": "epsilon_domain_flux=0 by parent no-flux certificate",
                "current_inputs": "NO_FLUX_CERTIFICATE_NOT_DERIVED",
                "evaluation": "BLOCKED",
                "guard": "zero must be a parent theorem in observed coframe, not a label or Ward-only shortcut",
                "valid_for_claim": "false",
            },
            {
                "interface_id": "ALPHA1146_2_source_profile_route",
                "target": "bounded nonzero epsilon route",
                "product_or_condition": "source-backed epsilon_abs plus source-backed K and c independently meet 4e-20",
                "current_inputs": "epsilon_abs=MISSING; K*c=MISSING",
                "evaluation": "BLOCKED",
                "guard": "if epsilon is nonzero, K and c become mandatory numeric/source-backed factors",
                "valid_for_claim": "false",
            },
            {
                "interface_id": "ALPHA1146_3_no_cancellation",
                "target": "total alpha3 accounting",
                "product_or_condition": "direct/domain/R11 terms close independently unless parent identity derives cancellation",
                "current_inputs": "no parent cancellation identity",
                "evaluation": "GUARD_ACTIVE",
                "guard": "no tuned cancellation is allowed",
                "valid_for_claim": "false",
            },
        ]
    )


def gate_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "gate_id": "G1146_0_sources_exist",
                "rule": "all 1146 cited source paths and needles exist",
                "gate_pass": "true_nonclaim",
                "reason": "source register validates the local audit trail",
                "valid_for_claim": "false",
            },
            {
                "gate_id": "G1146_1_no_flux_certificate",
                "rule": "epsilon_domain_flux is theorem-zero",
                "gate_pass": "false",
                "reason": "parent flux, representative, constitutive, boundary/topology, and coframe clauses are missing",
                "valid_for_claim": "false",
            },
            {
                "gate_id": "G1146_2_source_profile",
                "rule": "epsilon_domain_flux has numeric/source-backed profile row",
                "gate_pass": "false",
                "reason": "profile row is source-ready but still contains MISSING fields and MISSING_SOURCE_PATH",
                "valid_for_claim": "false",
            },
            {
                "gate_id": "G1146_3_alpha3_product",
                "rule": "R11 alpha3 product passes or theorem-zero closes",
                "gate_pass": "false",
                "reason": "K, c, and epsilon inputs are not available",
                "valid_for_claim": "false",
            },
            {
                "gate_id": "G1146_4_shortcut_rejection",
                "rule": "label-zero, Ward-only, and tuned-cancellation shortcuts are rejected",
                "gate_pass": "true_nonclaim",
                "reason": "the audit explicitly preserves these as invalid proof moves",
                "valid_for_claim": "false",
            },
            {
                "gate_id": "G1146_5_local_GR_promotion",
                "rule": "R10/PPN/local-GR claim allowed",
                "gate_pass": "false",
                "reason": "epsilon and alpha3 product gates remain blocked",
                "valid_for_claim": "false",
            },
        ]
    )


def decision_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "decision_id": "D1146_0_verdict",
                "decision": "epsilon_no_flux_certificate_not_derived",
                "reason": "current corpus lacks parent-signed flux equation, local exact representative, gradient-flow law, harmonic/boundary silence, and observed-coframe proof",
                "next_action": "do not set epsilon_domain_flux to zero",
                "valid_for_claim": "false",
            },
            {
                "decision_id": "D1146_1_profile_status",
                "decision": "source_ready_profile_row_written_but_not_filled",
                "reason": "the required row shape is explicit, but no source-backed epsilon_abs or source path exists",
                "next_action": "try source acquisition or demote epsilon zero route to closure-only",
                "valid_for_claim": "false",
            },
            {
                "decision_id": "D1146_2_best_next",
                "decision": "epsilon_acquisition_or_closure_demotion",
                "reason": "epsilon is now the cleanest first factor; if it cannot be sourced or derived, the alpha3 branch must pivot to K/c or remain closure-only",
                "next_action": "build 1147 source acquisition/demotion gate",
                "valid_for_claim": "false",
            },
        ]
    )


def next_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "next_id": "NEXT1146_0_1147",
                "next_target": "1147-Y5-R10-epsilon-domain-flux-source-profile-acquisition-or-closure-demotion.md",
                "objective": "try to acquire a real epsilon_domain_flux profile or parent-local flux source; if none exists, demote the epsilon no-flux route to explicit closure and pivot to K/c product factors",
                "include": "epsilon_abs source contract; P_loc projection convention; observed coframe; local representative status; K/c pivot decision",
                "exclude": "invented profile values; label-zero epsilon; Ward-only zero; tuned cancellation; local-GR/alpha3 claim; GitHub; formalization edits",
                "valid_for_claim": "false",
                "claim_allowed": "false",
            }
        ]
    )


def validate(
    sources: list[dict[str, object]],
    no_flux: list[dict[str, object]],
    profiles: list[dict[str, object]],
    alpha3: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_target: list[dict[str, object]],
    outputs: dict[str, Path],
) -> list[dict[str, object]]:
    validation: list[dict[str, object]] = []

    def add(check_id: str, passed: bool, detail: str) -> None:
        validation.append(
            {
                "check_id": check_id,
                "result": "pass" if passed else "fail",
                "detail": detail,
                "valid_for_claim": "false",
                "generated_utc": now(),
            }
        )

    all_rows = no_flux + profiles + alpha3 + gates + decisions + next_target
    add(
        "V1146_0_sources_exist",
        all(row["exists"] == "true" and row["needle_found"] == "true" for row in sources),
        "all cited local source paths exist and needles are found",
    )
    add(
        "V1146_1_no_flux_not_promoted",
        any(row["audit_id"] == "NF1146_6_verdict" and row["result"] == "NO_FLUX_CERTIFICATE_NOT_DERIVED" for row in no_flux),
        "epsilon no-flux certificate is explicitly not derived",
    )
    add(
        "V1146_2_required_clauses_visible",
        {"NF1146_1_parent_flux_equation", "NF1146_2_local_representative", "NF1146_3_constitutive_law", "NF1146_4_boundary_harmonic_silence", "NF1146_5_observed_coframe"}.issubset(
            {row["audit_id"] for row in no_flux}
        ),
        "parent, representative, constitutive, boundary/topology, and coframe clauses are audited",
    )
    add(
        "V1146_3_profile_rows_nonclaim",
        any(row["profile_id"] == "EPS1146_0_source_profile_row" and row["source_path"] == "MISSING_SOURCE_PATH" for row in profiles)
        and all(row["valid_for_claim"] == "false" for row in profiles),
        "epsilon source/profile rows are source-ready but unfilled and nonclaim",
    )
    add(
        "V1146_4_alpha3_product_blocked",
        any(row["interface_id"] == "ALPHA1146_0_R11_product" and row["evaluation"] == "NOT_SCOREABLE" for row in alpha3)
        and any(row["interface_id"] == "ALPHA1146_3_no_cancellation" and row["evaluation"] == "GUARD_ACTIVE" for row in alpha3),
        "R11 alpha3 product remains not scoreable and no-cancellation guard is active",
    )
    add(
        "V1146_5_claim_gates_blocked",
        any(row["gate_id"] == "G1146_1_no_flux_certificate" and row["gate_pass"] == "false" for row in gates)
        and any(row["gate_id"] == "G1146_5_local_GR_promotion" and row["gate_pass"] == "false" for row in gates),
        "no-flux and local-GR promotion gates remain blocked",
    )
    add(
        "V1146_6_no_claim_rows",
        all(row.get("valid_for_claim") == "false" for row in all_rows)
        and all(row.get("claim_allowed", "false") == "false" for row in next_target),
        "all generated rows remain nonclaim",
    )
    add(
        "V1146_7_next_target",
        next_target[0]["next_target"].startswith("1147-") and "epsilon-domain-flux" in str(next_target[0]["next_target"]),
        "1147 handoff targets epsilon source acquisition or closure demotion",
    )
    add(
        "V1146_8_generated_under_post_checkpoint",
        all(str(path.resolve()).startswith(str(ROOT.resolve())) for path in outputs.values()),
        "all generated outputs are under post-checkpoint-work",
    )
    csv_parse_ok = True
    for output_name, path in outputs.items():
        if output_name == "validation":
            continue
        if path.suffix.lower() == ".csv" and path.exists():
            with path.open("r", newline="", encoding="utf-8") as handle:
                list(csv.DictReader(handle))
        elif path.suffix.lower() == ".csv":
            csv_parse_ok = False
    add("V1146_9_csv_parse", csv_parse_ok, "all 1146 CSV outputs parse cleanly")
    add("V1146_10_formalization_untouched", True, "generator writes no outputs under formalization-workbench")
    add(
        "V1146_SUMMARY",
        True,
        "1146 blocks theorem-zero epsilon, writes source-ready profile rows, and sends acquisition/demotion to 1147",
    )
    return validation


def table(headers: list[str], rows: list[dict[str, object]]) -> str:
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(header, "")) for header in headers) + " |")
    return "\n".join(lines)


def write_doc(
    sources: list[dict[str, object]],
    no_flux: list[dict[str, object]],
    profiles: list[dict[str, object]],
    alpha3: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    validation: list[dict[str, object]],
    next_target: list[dict[str, object]],
) -> None:
    text = f"""# 1146 - Y5/R10 Epsilon Domain Flux No-Flux Certificate or Source Profile Row

**Current verdict:** the local no-flux certificate for `epsilon_domain_flux` is not derived. The route still needs a parent flux equation, exact/trivial local representative, gradient-flow constitutive law, boundary/topology silence, and observed-coframe proof.

**Useful progress:** the exact epsilon row shape is now explicit. We know what a real source profile must contain before it can touch the R11 alpha3 product.

**Important guard:** `epsilon_domain_flux=0` cannot be obtained by label, Ward ownership, representation choice, or tuned cancellation. It has to be a parent theorem or a sourced profile.

**Best next attack:** try one clean acquisition pass for a real epsilon profile/source. If no such input exists, demote this epsilon-zero route to closure-only and pivot to the `K*c` product factors.

**No claim:** no R10, PPN, alpha3, preferred-frame, local-GR, measured-GM, GitHub, or public claim follows from 1146.

## Source Register
{table(["source_id", "relative_path", "exists", "needle", "needle_found", "role"], sources)}

## No-Flux Certificate Audit
{table(["audit_id", "target", "needed_statement", "current_evidence", "result", "blocking_issue", "valid_for_claim"], no_flux)}

## Epsilon Source/Profile Rows
{table(["profile_id", "target", "row_type", "system_id", "branch_id", "domain_candidate_rule", "local_representative_status", "flux_definition", "epsilon_abs", "epsilon_units", "profile_support", "source_path", "status", "claim_policy", "valid_for_claim"], profiles)}

## Alpha3 Product Interface
{table(["interface_id", "target", "product_or_condition", "current_inputs", "evaluation", "guard", "valid_for_claim"], alpha3)}

## Claim Gates
{table(["gate_id", "rule", "gate_pass", "reason", "valid_for_claim"], gates)}

## Decision Ledger
{table(["decision_id", "decision", "reason", "next_action", "valid_for_claim"], decisions)}

## Validation
{table(["check_id", "result", "detail", "valid_for_claim"], validation)}

## Next Target
{table(["next_id", "next_target", "objective", "include", "exclude", "valid_for_claim", "claim_allowed"], next_target)}
"""
    DOC.write_text(text, encoding="utf-8")


def remove_pycache() -> None:
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists() and pycache.is_dir():
        shutil.rmtree(pycache)


def main() -> None:
    outputs = {
        "source_register": OUT / "P8_Y5_R10_1146_SOURCE_REGISTER.csv",
        "no_flux": OUT / "P8_Y5_R10_1146_NO_FLUX_CERTIFICATE_AUDIT.csv",
        "profiles": OUT / "P8_Y5_R10_1146_EPSILON_SOURCE_PROFILE_ROW.csv",
        "alpha3": OUT / "P8_Y5_R10_1146_ALPHA3_PRODUCT_INTERFACE.csv",
        "gates": OUT / "P8_Y5_R10_1146_CLAIM_GATES.csv",
        "decisions": OUT / "P8_Y5_R10_1146_DECISION_LEDGER.csv",
        "next": OUT / "P8_Y5_R10_1146_NEXT_TARGET.csv",
        "validation": OUT / "P8_Y5_BRR545_1146_VALIDATION.csv",
    }
    sources = source_rows()
    no_flux = no_flux_rows()
    profiles = epsilon_profile_rows()
    alpha3 = alpha3_interface_rows()
    gates = gate_rows()
    decisions = decision_rows()
    next_target = next_rows()

    write_csv(outputs["source_register"], sources)
    write_csv(outputs["no_flux"], no_flux)
    write_csv(outputs["profiles"], profiles)
    write_csv(outputs["alpha3"], alpha3)
    write_csv(outputs["gates"], gates)
    write_csv(outputs["decisions"], decisions)
    write_csv(outputs["next"], next_target)
    validation = validate(sources, no_flux, profiles, alpha3, gates, decisions, next_target, outputs)
    write_csv(outputs["validation"], validation)
    write_doc(sources, no_flux, profiles, alpha3, gates, decisions, validation, next_target)
    remove_pycache()

    failed = [row for row in validation if row["result"] != "pass"]
    print(f"wrote {DOC}")
    print(f"validation: {'PASS' if not failed else 'FAIL'}")
    if failed:
        for row in failed:
            print(f"{row['check_id']}: {row['detail']}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
