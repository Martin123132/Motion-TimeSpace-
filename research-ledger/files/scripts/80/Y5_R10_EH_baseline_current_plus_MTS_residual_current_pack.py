from __future__ import annotations

import csv
import os
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "994-Y5-R10-EH-baseline-current-plus-MTS-residual-current-pack.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
SCRIPT_START_UTC = datetime.now(timezone.utc)


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def flag(value: bool) -> str:
    return "true" if value else "false"


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def md_cell(value: object) -> str:
    return str(value).replace("\n", "<br>").replace("|", "\\|")


def md_table(rows: list[dict[str, str]], columns: list[str]) -> str:
    if not rows:
        return "_No rows._"
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    body = [
        "| " + " | ".join(md_cell(row.get(column, "")) for column in columns) + " |"
        for row in rows
    ]
    return "\n".join([header, separator, *body])


def source_path(relative_path: str) -> Path:
    return ROOT / relative_path


def source_register() -> list[dict[str, str]]:
    specs = [
        {
            "source_id": "993_doc",
            "path": "993-Y5-R10-parent-Lagrangian-current-extraction-theta-Qtau-or-deltaH-curl-input.md",
            "role": "immediate handoff selecting EH baseline plus residual current pack",
            "needle": "DEC993_2_next_target",
        },
        {
            "source_id": "993_sector_ledger",
            "path": "source-intake/mts_residuals/P8_Y5_R10_993_SECTOR_CURRENT_EXTRACTION_LEDGER.csv",
            "role": "sector current extraction ledger",
            "needle": "SEC993_0_EH_core",
        },
        {
            "source_id": "993_qtau_ledger",
            "path": "source-intake/mts_residuals/P8_Y5_R10_993_QTAU_DECOMPOSITION_LEDGER.csv",
            "role": "Q_tau decomposition ledger",
            "needle": "QDEC993_5_total",
        },
        {
            "source_id": "993_EH_credit",
            "path": "source-intake/mts_residuals/P8_Y5_R10_993_EH_BASELINE_CREDIT_LEDGER.csv",
            "role": "EH baseline credit limits",
            "needle": "EHC993_0_EH_current_shape",
        },
        {
            "source_id": "992_residuals",
            "path": "source-intake/mts_residuals/P8_Y5_R10_992_CHARGE_CURRENT_RESIDUAL_LEDGER.csv",
            "role": "charge-current residual ledger",
            "needle": "SCE992_Delta_PiM",
        },
        {
            "source_id": "991_component_gate",
            "path": "source-intake/mts_residuals/P8_Y5_R10_991_FB5540_CONSOLIDATED_COMPONENT_GATE.csv",
            "role": "FB554_0 component gate",
            "needle": "FB991_2_symplectic_boundary_flux",
        },
        {
            "source_id": "min_local_GR_blocks",
            "path": "source-intake/mts_residuals/P8_MIN_PARENT_LOCAL_GR_ACTION_BLOCKS.csv",
            "role": "minimal local-GR action block map",
            "needle": "A511_0_EH_core",
        },
        {
            "source_id": "min_local_GR_chain",
            "path": "source-intake/mts_residuals/P8_MIN_PARENT_LOCAL_GR_DERIVED_CHAIN.csv",
            "role": "minimal local-GR derived chain",
            "needle": "DC511_3",
        },
        {
            "source_id": "min_local_GR_residuals",
            "path": "source-intake/mts_residuals/P8_MIN_PARENT_LOCAL_GR_RESIDUAL_VECTOR.csv",
            "role": "local-GR residual vector",
            "needle": "AR511_5_PiM_variation",
        },
        {
            "source_id": "768_requirements",
            "path": "source-intake/mts_residuals/P8_Y5_R10_768_GR_NEWTON_REQUIREMENT_MAP.csv",
            "role": "GR/Newton requirement map",
            "needle": "GN768_3_HPiM_integrability",
        },
        {
            "source_id": "770_certificate",
            "path": "source-intake/mts_residuals/P8_Y5_R10_770_PARENT_ACTION_CERTIFICATE_AUDIT.csv",
            "role": "parent action certificate audit",
            "needle": "HIC770_5_LX_boundary_policy",
        },
        {
            "source_id": "brr545_parent_clause_tests",
            "path": "source-intake/mts_residuals/P8_Y5_BRR545_PARENT_ACTION_CLAUSE_TESTS.csv",
            "role": "BRR545 parent action clause tests",
            "needle": "CT552_7_no_cheat_policy",
        },
    ]
    rows: list[dict[str, str]] = []
    for spec in specs:
        path = source_path(spec["path"])
        text = read_text(path)
        rows.append(
            {
                "source_id": spec["source_id"],
                "role": spec["role"],
                "path": spec["path"],
                "exists": flag(path.exists()),
                "needle_found": flag(spec["needle"] in text),
                "needle": spec["needle"],
                "valid_for_claim": "false",
            }
        )
    return rows


def eh_baseline_rows() -> list[dict[str, str]]:
    return [
        {
            "baseline_id": "EHB994_0_L_EH",
            "object": "Einstein-Hilbert local exterior Lagrangian",
            "reference_form": "L_EH=(16*pi*G_ref)^-1 (R[g_obs]-2Lambda0) epsilon + dB_GHY/reference",
            "what_it_buys": "known covariant phase-space current and standard local GR comparison target",
            "allowed_use": "comparator for Q_tau, theta, constraints, weak-field source coefficient",
            "forbidden_use": "substitute for MTS parent current or source equality",
            "valid_for_claim": "false",
        },
        {
            "baseline_id": "EHB994_1_theta_EH",
            "object": "EH symplectic potential",
            "reference_form": "theta_EH(g,delta g) is the standard boundary 3-form from delta(sqrt(-g)R)",
            "what_it_buys": "baseline omega_EH and Hamiltonian variation shape",
            "allowed_use": "compare MTS theta_s residuals against the EH term",
            "forbidden_use": "declare theta_total=theta_EH while extra sectors remain unvaried",
            "valid_for_claim": "false",
        },
        {
            "baseline_id": "EHB994_2_Qtau_EH",
            "object": "EH Noether/Hamiltonian charge",
            "reference_form": "J_tau^EH=theta_EH(L_tau g)-i_tau L_EH=dQ_tau^EH+C_tau^EH",
            "what_it_buys": "baseline mass-charge operator and constraint split",
            "allowed_use": "target shape for Q_tau^MTS decomposition",
            "forbidden_use": "claim Q_tau^MTS=Q_tau^EH without residual-current proof",
            "valid_for_claim": "false",
        },
        {
            "baseline_id": "EHB994_3_Poisson_Gauss",
            "object": "weak-field GR source comparison",
            "reference_form": "g_00=-1+2G_ref M/r+O(r^-2), nabla^2 Phi=4*pi*G_ref rho",
            "what_it_buys": "Newtonian target after source charge closes",
            "allowed_use": "downstream comparison after M_H_tau is parent-owned",
            "forbidden_use": "import orbital GM before source-current equality",
            "valid_for_claim": "false",
        },
    ]


def residual_current_rows() -> list[dict[str, str]]:
    return [
        {
            "residual_id": "RC994_0_reference_boundary",
            "residual_current_piece": "Q_boundary + delta B_ref + C_ref",
            "maps_to": "Delta_ref, Delta_symp, SCE992_Delta_symp",
            "current_status": "not_parent_fixed",
            "required_zero_or_bound": "fixed B_ref plus exact/cohomology/nohair boundary theorem or sourced boundary flux row",
            "blocks_if_open": "FB554_0 and Hamiltonian source-mass integrability",
            "valid_for_claim": "false",
        },
        {
            "residual_id": "RC994_1_extra_nonEH",
            "residual_current_piece": "Q_extra + C_extra from motion/time/domain/memory/range/non-EH sectors",
            "maps_to": "Delta_nonEH, Delta_extra, AR511_0, AR511_1, AR511_3",
            "current_status": "not_extracted",
            "required_zero_or_bound": "sector-by-sector no-source positive operator/topological/proper-gauge theorem or executable coefficient vector",
            "blocks_if_open": "EH-only/local-GR reduction and R11/R10/PPN residual scoring",
            "valid_for_claim": "false",
        },
        {
            "residual_id": "RC994_2_projector_domain",
            "residual_current_piece": "C_projector + [d,Pi_M]J_H + delta Pi_M terms",
            "maps_to": "SCE992_Delta_PiM, SCE992_Delta_flux, AR511_4, AR511_5",
            "current_status": "not_extracted",
            "required_zero_or_bound": "parent-owned Pi_M/P_loc chain map, covariant constancy, domain/homology rule, or finite commutator bound",
            "blocks_if_open": "source-current closure, radial stability, Newton source normalization",
            "valid_for_claim": "false",
        },
        {
            "residual_id": "RC994_3_matter_source_glue",
            "residual_current_piece": "C_matter[J_H] + worldtube source-measure glue residual",
            "maps_to": "SCE992_Delta_frame, SCE992_Delta_cal, QDEC993_4_matter_source",
            "current_status": "conditional_not_glued",
            "required_zero_or_bound": "same observed coframe, parent matter functor, Hilbert/source equality, worldtube denominator theorem",
            "blocks_if_open": "observed mass/GM equality and orbital calibration",
            "valid_for_claim": "false",
        },
        {
            "residual_id": "RC994_4_coupling_constant",
            "residual_current_piece": "C_Geff + C_kappa + source-normalization drift",
            "maps_to": "SCE992_Delta_G, SEC993_1_kappa_topological",
            "current_status": "not_parent_derived",
            "required_zero_or_bound": "constant universal G_ref/kappa theorem or sourced Gdot/range/species/frame bounds",
            "blocks_if_open": "Newtonian normalization, clocks, R10, Gdot, WEP/source tests",
            "valid_for_claim": "false",
        },
        {
            "residual_id": "RC994_5_readout_PPN_tail",
            "residual_current_piece": "C_readout + second-order PPN source-response tail",
            "maps_to": "SCE992_Delta_PPN, AR511_7, SEC993_6_metric_readout_PiM",
            "current_status": "downstream_not_ready",
            "required_zero_or_bound": "weak-field/PPN response matrix from same source charge and metric readout",
            "blocks_if_open": "local-GR/PPN claim even if first-order source charge improves",
            "valid_for_claim": "false",
        },
        {
            "residual_id": "RC994_6_EM_clock_coupling_guard",
            "residual_current_piece": "C_EM/clock/source readout leakage",
            "maps_to": "SEC993_7_EM_charge_coupling and 987-989 alpha/EM-lock route",
            "current_status": "guard_only",
            "required_zero_or_bound": "EM-lock/no-alpha/source-normalization owner or finite clock/WEP/source residual bounds",
            "blocks_if_open": "prevents hidden composition/readout leakage in source-current proof",
            "valid_for_claim": "false",
        },
    ]


def deltaH_envelope_rows() -> list[dict[str, str]]:
    return [
        {
            "envelope_id": "DHE994_0_definition",
            "expression": "|deltaH_curl|/M_H_ref <= |EH_baseline_curl|/M_H_ref + sum_i |RC994_i|/M_H_ref",
            "status": "definition_only",
            "why_nonclaim": "EH baseline curl can vanish under GR conditions, but residual-current terms are not sourced",
            "required_exit": "all residual-current pieces zero or source-backed bounded with positive M_H_ref",
            "valid_for_claim": "false",
        },
        {
            "envelope_id": "DHE994_1_no_cancellation",
            "expression": "residuals enter as absolute values; no cancellation credit",
            "status": "policy_pass",
            "why_nonclaim": "policy prevents fake zero but supplies no values",
            "required_exit": "component rows with units/source paths",
            "valid_for_claim": "false",
        },
        {
            "envelope_id": "DHE994_2_EH_limit",
            "expression": "if every RC994_i=0 and EH boundary/reference/tau assumptions hold, Q_tau^MTS -> Q_tau^EH",
            "status": "conditional_limit_only",
            "why_nonclaim": "premise is exactly what remains unproved",
            "required_exit": "sector extraction or zero theorem for every residual current",
            "valid_for_claim": "false",
        },
    ]


def residual_input_schema_rows() -> list[dict[str, str]]:
    base = "source-intake/mts_residuals"
    return [
        {
            "schema_id": "RIS994_0_EH_baseline_terms",
            "target": "theta_EH_Qtau_EH_baseline",
            "candidate_artifact": f"{base}/P8_Y5_R10_994_EH_BASELINE_CURRENT_INPUT_CANDIDATE.csv",
            "required_columns": "term_id;formula;normalization;boundary_condition;tau_id;source_path;valid_for_claim",
            "current_status": "MISSING_BASELINE_DETAIL_ROWS",
            "valid_for_claim": "false",
        },
        {
            "schema_id": "RIS994_1_residual_current_values",
            "target": "RC994_i numeric_or_theorem rows",
            "candidate_artifact": f"{base}/P8_Y5_R10_994_RESIDUAL_CURRENT_INPUT_CANDIDATE.csv",
            "required_columns": "residual_id;zero_theorem_or_bound;value;units;M_H_ref;source_path;assumptions;valid_for_claim",
            "current_status": "MISSING_RESIDUAL_CURRENT_VALUES",
            "valid_for_claim": "false",
        },
        {
            "schema_id": "RIS994_2_deltaH_envelope_values",
            "target": "deltaH_curl_envelope_over_MHref",
            "candidate_artifact": f"{base}/P8_Y5_R10_994_DELTAH_ENVELOPE_INPUT_CANDIDATE.csv",
            "required_columns": "system_id;surface_id;sum_abs_residuals;EH_baseline_curl;M_H_ref;units;source_path;valid_for_claim",
            "current_status": "MISSING_DELTAH_ENVELOPE_VALUES",
            "valid_for_claim": "false",
        },
    ]


def claim_gate_rows() -> list[dict[str, str]]:
    return [
        {
            "gate_id": "CG994_0_EH_import",
            "claim": "MTS current equals EH current",
            "gate_pass": "false",
            "claim_allowed": "false",
            "why_not": "residual-current pieces are named but not zeroed or bounded",
        },
        {
            "gate_id": "CG994_1_deltaH_curl",
            "claim": "deltaH curl vanishes or is bounded",
            "gate_pass": "false",
            "claim_allowed": "false",
            "why_not": "residual current values and M_H_ref are missing",
        },
        {
            "gate_id": "CG994_2_FB5540_source_mass",
            "claim": "FB554_0 or Hamiltonian source mass is closed",
            "gate_pass": "false",
            "claim_allowed": "false",
            "why_not": "reference, boundary, projector, source-glue, coupling, and PPN tails remain open",
        },
        {
            "gate_id": "CG994_3_Newton_PPN_local_GR",
            "claim": "Newton, PPN, R10, R11, Gdot, orbit, or local-GR pass",
            "gate_pass": "false",
            "claim_allowed": "false",
            "why_not": "downstream empirical gates need source charge plus weak-field operator ownership",
        },
    ]


def decision_rows() -> list[dict[str, str]]:
    return [
        {
            "decision_id": "DEC994_0_baseline_pack",
            "decision": "accept EH as explicit comparator only",
            "reason": "it provides the target current shape while preserving the nonclaim guard",
            "effect": "future rows can say whether MTS residuals vanish relative to EH",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC994_1_residual_pack",
            "decision": "stage seven residual-current families",
            "reason": "these cover every current piece 993 could not extract",
            "effect": "derivation work has exact targets instead of a vague parent-action gap",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC994_2_next_target",
            "decision": "attack the first residual family: boundary/reference current",
            "reason": "RC994_0 blocks deltaH integrability and is already isolated by BRR545/545 contracts",
            "effect": "try zero theorem first, then source-bound row if it fails",
            "valid_for_claim": "false",
        },
    ]


def next_target_rows() -> list[dict[str, str]]:
    return [
        {
            "next_target": "995-Y5-R10-boundary-reference-current-zero-theorem-or-residual-bound-row.md",
            "objective": "derive or bound the boundary/reference residual current RC994_0 that feeds Delta_ref and Delta_symp",
            "include": "B_ref lock, GHY/reference comparator, exact/cohomology boundary forms, no vector/tensor/radial boundary hair, source-backed residual row if theorem fails",
            "exclude": "FB554_0 pass, Newton/PPN/R10/local-GR pass, orbital GM substitution, hidden EH import, GitHub action, formalization-workbench edits",
            "valid_for_claim": "false",
        }
    ]


def formalization_changed_after_start() -> int:
    if not FORMALIZATION.exists():
        return 0
    count = 0
    start_timestamp = SCRIPT_START_UTC.timestamp()
    for dirpath, _, filenames in os.walk(FORMALIZATION):
        for filename in filenames:
            path = Path(dirpath) / filename
            try:
                if path.stat().st_mtime > start_timestamp:
                    count += 1
            except OSError:
                count += 1
    return count


def validation_rows(
    sources: list[dict[str, str]],
    eh: list[dict[str, str]],
    residuals: list[dict[str, str]],
    envelope: list[dict[str, str]],
    schemas: list[dict[str, str]],
    claims: list[dict[str, str]],
    decisions: list[dict[str, str]],
    next_target: list[dict[str, str]],
) -> list[dict[str, str]]:
    sources_ok = all(row["exists"] == "true" and row["needle_found"] == "true" for row in sources)
    eh_ok = all(row["valid_for_claim"] == "false" and row["forbidden_use"] for row in eh)
    residuals_ok = len(residuals) >= 7 and all(row["valid_for_claim"] == "false" for row in residuals)
    envelope_ok = all(row["valid_for_claim"] == "false" for row in envelope) and any(row["envelope_id"] == "DHE994_1_no_cancellation" for row in envelope)
    schemas_ok = all(row["valid_for_claim"] == "false" and "MISSING" in row["current_status"] for row in schemas)
    claims_ok = all(row["gate_pass"] == "false" and row["claim_allowed"] == "false" for row in claims)
    decision_ok = any(row["decision_id"] == "DEC994_2_next_target" for row in decisions)
    next_ok = bool(next_target) and next_target[0]["valid_for_claim"] == "false"
    formalization_count = formalization_changed_after_start()
    checks = [
        {"check_id": "V994_0_sources", "result": "pass" if sources_ok else "fail", "detail": "all cited local source files exist and expected needles are found"},
        {"check_id": "V994_1_EH_baseline_limited", "result": "pass" if eh_ok else "fail", "detail": "EH baseline is comparator-only and nonclaim"},
        {"check_id": "V994_2_residual_pack_complete", "result": "pass" if residuals_ok else "fail", "detail": "residual-current pack contains seven nonclaim families"},
        {"check_id": "V994_3_envelope_safe", "result": "pass" if envelope_ok else "fail", "detail": "deltaH envelope uses no-cancellation policy and remains nonclaim"},
        {"check_id": "V994_4_schema_fail_closed", "result": "pass" if schemas_ok else "fail", "detail": "future input schemas remain MISSING and valid_for_claim=false"},
        {"check_id": "V994_5_claim_gates_safe", "result": "pass" if claims_ok else "fail", "detail": "EH import, deltaH, FB5540, and local-GR claims are blocked"},
        {"check_id": "V994_6_next_decision", "result": "pass" if decision_ok else "fail", "detail": "boundary/reference residual selected next"},
        {"check_id": "V994_7_next_target_written", "result": "pass" if next_ok else "fail", "detail": "995 target row is present and nonclaim"},
        {"check_id": "V994_8_formalization_untouched", "result": "pass" if formalization_count == 0 else "fail", "detail": f"formalization-workbench modified-file count since script start is {formalization_count}"},
    ]
    ready = all(row["result"] == "pass" for row in checks)
    return [
        {**row, "generated_utc": stamp()}
        for row in checks
    ] + [
        {
            "check_id": "V994_READY",
            "result": "pass" if ready else "fail",
            "detail": "994 checkpoint pack validation summary",
            "generated_utc": stamp(),
        }
    ]


def write_doc(
    sources: list[dict[str, str]],
    eh: list[dict[str, str]],
    residuals: list[dict[str, str]],
    envelope: list[dict[str, str]],
    schemas: list[dict[str, str]],
    claims: list[dict[str, str]],
    decisions: list[dict[str, str]],
    validation: list[dict[str, str]],
    next_target: list[dict[str, str]],
) -> None:
    lines = [
        "# 994 Y5 R10: EH Baseline Current Plus MTS Residual-Current Pack",
        "",
        "Status: `Y5_R10_994_EH_baseline_current_comparator_written_MTS_residual_current_pack_staged_nonclaim`",
        "",
        "Claim ceiling: no EH import proof, no `deltaH` curl zero/bound, no `FB554_0=0`, no Newton/PPN/R10/R11/Gdot/orbit/local-GR pass.",
        "",
        "## Readout",
        "",
        "994 separates the honest GR target from the unproved MTS pieces. The EH current is allowed as the comparator because it tells us what the GR/Newton limit should look like. It is not allowed to become a smuggled proof.",
        "",
        "The MTS side is now a residual-current pack: boundary/reference, non-EH extra sectors, projector/domain terms, matter/source glue, coupling-constant drift, PPN/readout tail, and EM/clock coupling guard. The next derivation can attack these one by one rather than wrestling a fog monster.",
        "",
        "## Source Register",
        "",
        md_table(sources, ["source_id", "role", "exists", "needle_found", "path"]),
        "",
        "## EH Baseline Current",
        "",
        md_table(eh, ["baseline_id", "object", "reference_form", "what_it_buys", "allowed_use", "forbidden_use", "valid_for_claim"]),
        "",
        "## MTS Residual-Current Pack",
        "",
        md_table(residuals, ["residual_id", "residual_current_piece", "maps_to", "current_status", "required_zero_or_bound", "blocks_if_open", "valid_for_claim"]),
        "",
        "## DeltaH No-Cancellation Envelope",
        "",
        md_table(envelope, ["envelope_id", "expression", "status", "why_nonclaim", "required_exit", "valid_for_claim"]),
        "",
        "## Residual Input Schemas",
        "",
        md_table(schemas, ["schema_id", "target", "candidate_artifact", "required_columns", "current_status", "valid_for_claim"]),
        "",
        "## Claim Gates",
        "",
        md_table(claims, ["gate_id", "claim", "gate_pass", "claim_allowed", "why_not"]),
        "",
        "## Decision Ledger",
        "",
        md_table(decisions, ["decision_id", "decision", "reason", "effect", "valid_for_claim"]),
        "",
        "## Validation",
        "",
        md_table(validation, ["check_id", "result", "detail", "generated_utc"]),
        "",
        "## Next Target",
        "",
        md_table(next_target, ["next_target", "objective", "include", "exclude", "valid_for_claim"]),
        "",
    ]
    DOC.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    sources = source_register()
    eh = eh_baseline_rows()
    residuals = residual_current_rows()
    envelope = deltaH_envelope_rows()
    schemas = residual_input_schema_rows()
    claims = claim_gate_rows()
    decisions = decision_rows()
    next_target = next_target_rows()
    validation = validation_rows(sources, eh, residuals, envelope, schemas, claims, decisions, next_target)

    write_csv(OUT / "P8_Y5_R10_994_SOURCE_REGISTER.csv", sources)
    write_csv(OUT / "P8_Y5_R10_994_EH_BASELINE_CURRENT.csv", eh)
    write_csv(OUT / "P8_Y5_R10_994_MTS_RESIDUAL_CURRENT_PACK.csv", residuals)
    write_csv(OUT / "P8_Y5_R10_994_DELTAH_NO_CANCELLATION_ENVELOPE.csv", envelope)
    write_csv(OUT / "P8_Y5_R10_994_RESIDUAL_INPUT_SCHEMAS.csv", schemas)
    write_csv(OUT / "P8_Y5_R10_994_CLAIM_GATE.csv", claims)
    write_csv(OUT / "P8_Y5_R10_994_DECISION_LEDGER.csv", decisions)
    write_csv(OUT / "P8_Y5_R10_994_NEXT_TARGET.csv", next_target)
    write_csv(OUT / "P8_Y5_BRR545_994_VALIDATION.csv", validation)
    write_doc(sources, eh, residuals, envelope, schemas, claims, decisions, validation, next_target)


if __name__ == "__main__":
    main()
