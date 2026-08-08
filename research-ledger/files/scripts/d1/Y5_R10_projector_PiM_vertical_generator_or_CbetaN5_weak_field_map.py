from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds" / "local_bound_claims.csv"
DOC = ROOT / "939-Y5-R10-projector-PiM-vertical-generator-or-CbetaN5-weak-field-map.md"
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


def source_register() -> list[dict[str, str]]:
    specs = [
        {
            "source_id": "938_doc",
            "path": "938-Y5-R10-extra-omega-vertical-degeneracy-or-CbetaN5-source-row.md",
            "role": "handoff selecting projector-PiM vertical generator",
            "needle": "projector-PiM vertical generator",
        },
        {
            "source_id": "938_validation",
            "path": "source-intake/mts_residuals/P8_Y5_BRR545_938_VALIDATION.csv",
            "role": "previous checkpoint validation",
            "needle": "V938_15_validation_rows_ready",
        },
        {
            "source_id": "454_doc",
            "path": "454-PiM-parent-symplectic-projector-algebra-attempt.md",
            "role": "conditional PiM projector algebra",
            "needle": "conditional_symplectic_projector_theorem",
        },
        {
            "source_id": "456_doc",
            "path": "456-PiM-projector-variation-stress-ledger.md",
            "role": "projector variation stress warning",
            "needle": "projector_variation_chain_rule",
        },
        {
            "source_id": "500_doc",
            "path": "500-topological-PiM-current-parent-clause-or-radial-bound-runner.md",
            "role": "topological PiM current clause",
            "needle": "But it does not yet prove Pi_M J_H = J_M_top.",
        },
        {
            "source_id": "521_doc",
            "path": "521-Y5-PiM-projector-owner-or-radial-bound-runner.md",
            "role": "PiM owner fork",
            "needle": "Pi_M J = ell_M(J) omega_M_top",
        },
        {
            "source_id": "914_doc",
            "path": "914-Y5-R10-topological-absolute-PiM-parent-clause-or-projector-source-bound-pack.md",
            "role": "topological absolute PiM parent clause audit",
            "needle": "topological absolute `Pi_M` route remains",
        },
        {
            "source_id": "920_doc",
            "path": "920-Y5-R10-PiM-current-offshell-closure-and-holonomy-zero-or-FM-force-bound.md",
            "role": "off-shell closure factorization",
            "needle": "d(Pi_M J_H) = Pi_M dJ_H + [d,Pi_M] J_H.",
        },
        {
            "source_id": "660_commutator",
            "path": "source-intake/mts_residuals/P8_Y5_R10_660_COMMUTATOR_ZERO_AUDIT.csv",
            "role": "commutator zero clauses",
            "needle": "CZ660_3_chain_map_property",
        },
        {
            "source_id": "908_ppn_vector",
            "path": "source-intake/mts_residuals/P8_Y5_R10_908_RETAINED_PPN_SOURCE_VECTOR.csv",
            "role": "retained projector PPN/source vector",
            "needle": "RPV908_0_metric_projector_stress",
        },
        {
            "source_id": "913_projector_rows",
            "path": "source-intake/mts_residuals/P8_Y5_R10_913_RETAINED_PROJECTOR_SOURCE_ROWS.csv",
            "role": "projector source residual rows",
            "needle": "PSR913_0_Delta_symp_projector",
        },
        {
            "source_id": "local_beta_bound",
            "path": "source-intake/local_bounds/local_bound_claims.csv",
            "role": "R4 beta observation row",
            "needle": "R4_beta",
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


def vertical_generator_contract() -> list[dict[str, str]]:
    specs = [
        (
            "PVC939_0_fixed_exterior_class",
            "parent fixes oriented local exterior and S2 class before readout",
            "Sigma_ext ~= S2 x I; delta[S2]=0; L_xi[S2]=0",
            "keeps Pi_M from becoming a moving source boundary",
            "not_parent_signed",
        ),
        (
            "PVC939_1_absolute_charge_map",
            "Pi_M is an absolute cohomology/Hamiltonian charge map, not Hodge/readout",
            "Pi_M J = ell_M(J) omega_M_top; delta_g ell_M=0; delta_g omega_M_top=0",
            "would make delta_g Pi_M=0 in the compact bulk",
            "conditional_shape_available_not_parent_signed",
        ),
        (
            "PVC939_2_metric_free_parent_block",
            "source-normalization block uses only wedge/class/orientation data",
            "S_PiM contains no star_g, Delta_g, Green_g, DeWitt metric, or fitted P_read",
            "prevents hidden projector stress from metric variation",
            "not_parent_signed",
        ),
        (
            "PVC939_3_chain_map_domain",
            "Pi_M commutes with d on the allowed Hilbert source-current complex",
            "[d,Pi_M]J_H=0 and J_H,dJ_H in Dom(Pi_M)",
            "kills the product-rule commutator leakage",
            "not_parent_signed",
        ),
        (
            "PVC939_4_Hilbert_topological_equality",
            "closed topological/Hamiltonian mass current equals observed projected Hilbert source",
            "J_M^top = Pi_M J_H + dB_zero or Pi_M^H J_H = Pi_M^top J_H + dB_zero",
            "prevents closing the wrong current",
            "not_parent_signed_key_blocker",
        ),
        (
            "PVC939_5_zero_flux_and_holonomy",
            "exact representative and flat mass gauge carry no compact boundary/holonomy tail",
            "int_boundary dB_zero=0; A_M=d lambda_M on admissible local domain",
            "prevents boundary/source drift and fifth-force leakage",
            "not_parent_signed",
        ),
        (
            "PVC939_6_measured_source_calibration",
            "the charge equals measured Newtonian source mass in the same frame",
            "M_H[S,tau]=M_eff[Pi_M J_H]; mu_obs=G_eff M_eff",
            "connects vertical PiM to Newton/PPN rather than a formal conserved label",
            "not_parent_signed",
        ),
        (
            "PVC939_7_total_verdict",
            "if PVC939_0 through PVC939_6 hold, Pi_M variation is vertical/stress-silent",
            "delta_g Pi_M=0, [d,Pi_M]J_H=0, Delta_symp_projector=0",
            "this would solve the N5 projector obstruction at the root",
            "conditional_theorem_not_current_claim",
        ),
    ]
    return [
        {
            "clause_id": clause_id,
            "statement": statement,
            "mathematical_form": mathematical_form,
            "why_needed": why_needed,
            "current_status": current_status,
            "parent_signed": "false",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
        for clause_id, statement, mathematical_form, why_needed, current_status in specs
    ]


def route_audit() -> list[dict[str, str]]:
    specs = [
        (
            "PRA939_0_topological_absolute",
            "absolute topological Pi_M",
            "Pi_M J=ell_M(J) omega_M_top with fixed class and metric-free action",
            "best_route_conditional",
            "metric variation and commutator can vanish if equality/source clauses close",
            "Hilbert/topological equality, chain-map domain, zero flux, and measured-GM calibration remain unsigned",
            "selected_derivation_route",
        ),
        (
            "PRA939_1_Hamiltonian_charge",
            "Hamiltonian/covariant-phase-space Pi_M^H",
            "Pi_M inherited from H_tau mass charge and same-source calibration",
            "promising_downstream_route",
            "would tie Pi_M to GR-like charge if integrability and source frame are derived",
            "Delta_symp/source equality/reference/tau frame remain open",
            "kept_as_parallel_support",
        ),
        (
            "PRA939_2_Hodge_DeWitt",
            "Hodge/DeWitt/Green orthogonal projector",
            "Pi_H(g) uses star_g, Delta_g, Green_g, DeWitt/source-space metric",
            "rejected_as_zero_safe",
            "canonical algebra is possible",
            "metric variation generically creates T_PiM and must be retained or bounded",
            "do_not_use_for_free_GR",
        ),
        (
            "PRA939_3_boundary_only",
            "boundary-only projector stress",
            "delta S_PiM localized on boundary/corner/reference data",
            "conditional_but_open",
            "could be harmless if class-only and derivative-silent",
            "no boundary no-hair/no-flux theorem",
            "retained_if_used",
        ),
        (
            "PRA939_4_readout_mask",
            "post-fit/readout Pi_M",
            "Pi_M chosen after solving/scoring to isolate desired monopole",
            "forbidden_as_derivation",
            "can be useful as analysis readout only",
            "cannot enter parent action or earn theorem credit",
            "rejected",
        ),
    ]
    return [
        {
            "route_id": route_id,
            "route": route,
            "mathematical_form": mathematical_form,
            "status": status,
            "positive_part": positive_part,
            "blocker": blocker,
            "decision": decision,
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
        for route_id, route, mathematical_form, status, positive_part, blocker, decision in specs
    ]


def weak_field_cbeta_map() -> list[dict[str, str]]:
    beta_bound = ""
    beta_source = ""
    for row in read_csv(LOCAL_BOUNDS):
        if row.get("row_id") == "R4_beta":
            beta_bound = row.get("upper_bound", "")
            beta_source = row.get("reference_path_or_url", "")
            break
    specs = [
        (
            "WFM939_0_PPN_beta_definition",
            "beta_minus_one",
            "g_00 = -1 + 2U - 2 beta U^2 + O(v^6)",
            "dimensionless",
            "PPN definition",
            "definition_loaded",
            "false",
        ),
        (
            "WFM939_1_N5_metric_response",
            "delta_g00_N5_4",
            "delta g_00^(4)|_N5 := response of EH weak-field solver to retained Pi_M/projector stress/source residual",
            "dimensionless_metric_component",
            "MISSING_PROJECTOR_STRESS_MAP_OR_SOURCE_PROFILE",
            "missing_prediction",
            "false",
        ),
        (
            "WFM939_2_C_beta_N5",
            "C_beta_N5",
            "C_beta_N5 := - delta g_00^(4)|_N5 / (2 U^2 X_N5) on the GR exterior comparison branch",
            "dimensionless",
            "MISSING_SECOND_ORDER_WEAK_FIELD_SOLVER",
            "formal_definition_only",
            "false",
        ),
        (
            "WFM939_3_X_N5",
            "X_N5",
            "X_N5 := |Delta_projector + I_commutator + B_P_flux + Delta_HPiM + Delta_cal| normalized by M_ref",
            "dimensionless",
            "MISSING_NUMERIC_RESIDUAL_PROFILE",
            "formal_definition_only",
            "false",
        ),
        (
            "WFM939_4_beta_bound",
            "R4_beta_bound",
            beta_bound,
            "dimensionless",
            beta_source,
            "source_bound_loaded",
            "false",
        ),
        (
            "WFM939_5_score_gate",
            "beta_score_gate",
            "|C_beta_N5 X_N5| <= 7.8e-05, with no prior-edge/source-placeholder flags",
            "dimensionless",
            "derived_schema_no_numeric_prediction",
            "score_blocked_until_C_and_X_numeric",
            "false",
        ),
    ]
    return [
        {
            "map_id": map_id,
            "symbol": symbol,
            "definition_or_formula": definition_or_formula,
            "units": units,
            "source_or_missing_input": source_or_missing_input,
            "status": status,
            "score_ready": score_ready,
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
        for map_id, symbol, definition_or_formula, units, source_or_missing_input, status, score_ready in specs
    ]


def residual_rows() -> list[dict[str, str]]:
    specs = [
        (
            "RES939_0_Delta_symp_projector",
            "Delta_symp_projector",
            "|int_S i_tau omega_projector|/M_ref",
            "MISSING_PROJECTOR_OMEGA_ZERO_OR_COEFFICIENT",
            "symplectic obstruction",
        ),
        (
            "RES939_1_c_PiM_g",
            "c_PiM_g",
            "T_projector^{mu nu}/T_EH_scale or route-specific dimensionless normalization",
            "MISSING_PROJECTOR_STRESS_MAP",
            "metric response coefficient",
        ),
        (
            "RES939_2_I_commutator",
            "I_commutator",
            "int_A [d,Pi_M]J_H/M_ref",
            "MISSING_CHAIN_MAP_DOMAIN_PROOF_OR_NUMERIC_INTEGRAL",
            "source-current commutator",
        ),
        (
            "RES939_3_R_eq",
            "R_eq",
            "Pi_M J_H - J_M^top - dB_zero",
            "MISSING_HILBERT_TOPOLOGICAL_EQUALITY",
            "wrong-current/equality residual",
        ),
        (
            "RES939_4_B_P_flux",
            "B_P_flux",
            "int_boundary Pi_M K_owner/M_ref",
            "MISSING_BOUNDARY_NO_FLUX_INPUT",
            "boundary/corner flux",
        ),
        (
            "RES939_5_Delta_HPiM",
            "Delta_HPiM",
            "Pi_M^top - Pi_M^H plus reference/source-frame mismatch",
            "MISSING_HAMILTONIAN_PIM_INTEGRABILITY_AND_SOURCE_FRAME",
            "Hamiltonian/topological dictionary residual",
        ),
    ]
    return [
        {
            "residual_id": residual_id,
            "symbol": symbol,
            "formula": formula,
            "missing_before_score": missing_before_score,
            "role": role,
            "score_ready": "false",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
        for residual_id, symbol, formula, missing_before_score, role in specs
    ]


def decisions() -> list[dict[str, str]]:
    return [
        {
            "decision_id": "DEC939_0_vertical_generator",
            "decision": "PiM_vertical_generator_not_proved",
            "reason": "topological/Hamiltonian route is sharp, but chain-map domain, Hilbert equality, zero flux, and measured-source calibration remain unsigned",
            "consequence": "Delta_symp_projector and N5 beta safety remain retained residuals",
            "next_action": "attack chain-map plus Hilbert/topological equality jointly",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC939_1_best_route",
            "decision": "topological_absolute_route_selected_over_Hodge",
            "reason": "topological PiM can make delta_g Pi_M=0 if parent-owned; Hodge/DeWitt PiM generically creates projector stress",
            "consequence": "do not use Hodge projector as free-GR proof",
            "next_action": "prove fixed-domain chain map and equality to Hilbert source",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC939_2_Cbeta_map",
            "decision": "weak_field_Cbeta_map_defined_but_not_numeric",
            "reason": "C_beta_N5 can be defined from the PPN g00 fourth-order response, but no projector stress profile/operator solution exists",
            "consequence": "beta fallback is cleaner but still not scoreable",
            "next_action": "derive C_beta_N5 operator only if equality route fails",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def claim_gates() -> list[dict[str, str]]:
    return [
        {
            "gate_id": "CGATE939_0_delta_g_PiM_zero",
            "claim": "delta_g Pi_M=0 is parent-derived",
            "blocker": "absolute topological/Hamiltonian PiM is conditional but not parent-signed",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CGATE939_1_commutator_zero",
            "claim": "[d,Pi_M]J_H=0 on allowed source-current complex",
            "blocker": "chain-map domain and off-shell Hilbert current closure are not derived",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CGATE939_2_projector_vertical",
            "claim": "Pi_M/projector variation is an owned vertical generator",
            "blocker": "Hilbert/topological equality, zero flux, and measured-GM calibration remain missing",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CGATE939_3_Cbeta_score",
            "claim": "C_beta_N5 beta fallback is numeric and scoreable",
            "blocker": "C_beta_N5 and X_N5 are formal definitions without weak-field operator/profile",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CGATE939_4_local_GR",
            "claim": "local GR/Newton/PPN follows from PiM verticality",
            "blocker": "PiM verticality, source calibration, and beta/PPN residual score remain open",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def next_target() -> list[dict[str, str]]:
    return [
        {
            "next_target": "940-Y5-R10-chain-map-Hilbert-equality-or-CbetaN5-operator-source.md",
            "objective": "prove [d,Pi_M]J_H=0 together with Hilbert/topological source equality, or source the weak-field C_beta_N5 operator",
            "include": "fixed source-current complex, chain-map proof, J_M^top=Pi_M J_H+dB_zero, zero boundary flux, off-shell closure, fallback second-order PPN operator",
            "exclude": "assuming equality, assuming commutator zero, Hodge projector free-GR proof, beta pass claim, local-GR claim, GitHub action, formalization-workbench edits",
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
    contract_rows: list[dict[str, str]],
    route_rows: list[dict[str, str]],
    cbeta_rows: list[dict[str, str]],
    residual_rows_: list[dict[str, str]],
    decision_rows: list[dict[str, str]],
    claim_rows: list[dict[str, str]],
    target_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    rows = []

    def add(check_id: str, passed: bool, detail: str) -> None:
        rows.append({"check_id": check_id, "result": "pass" if passed else "fail", "detail": detail, "generated_utc": stamp()})

    prior = read_csv(OUT / "P8_Y5_BRR545_938_VALIDATION.csv")
    prior_clean = prior and all(row.get("result") == "pass" for row in prior)
    sources_ok = all(row["exists"] == "true" and row["needle_found"] == "true" for row in sources)
    total_conditional = any(row["clause_id"] == "PVC939_7_total_verdict" and row["current_status"] == "conditional_theorem_not_current_claim" for row in contract_rows)
    contract_no_claim = all(row["claim_allowed"] == "false" and row["valid_for_claim"] == "false" for row in contract_rows)
    topological_selected = any(row["route_id"] == "PRA939_0_topological_absolute" and row["decision"] == "selected_derivation_route" for row in route_rows)
    hodge_rejected = any(row["route_id"] == "PRA939_2_Hodge_DeWitt" and row["decision"] == "do_not_use_for_free_GR" for row in route_rows)
    readout_rejected = any(row["route_id"] == "PRA939_4_readout_mask" and row["decision"] == "rejected" for row in route_rows)
    cbeta_defined = any(row["map_id"] == "WFM939_2_C_beta_N5" and row["status"] == "formal_definition_only" for row in cbeta_rows)
    cbeta_bound_loaded = any(row["map_id"] == "WFM939_4_beta_bound" and row["definition_or_formula"] == "7.8e-05" for row in cbeta_rows)
    residuals_blocked = residual_rows_ and all(row["score_ready"] == "false" and row["claim_allowed"] == "false" for row in residual_rows_)
    decisions_nonclaim = all(row["valid_for_claim"] == "false" for row in decision_rows)
    claims_false = all(row["claim_allowed"] == "false" and row["valid_for_claim"] == "false" for row in claim_rows)
    next_selected = any(row["next_target"].startswith("940-Y5-R10-chain-map-Hilbert-equality") for row in target_rows)
    no_claims = all(
        row.get("valid_for_claim") == "false"
        for row in sources + contract_rows + route_rows + cbeta_rows + residual_rows_ + decision_rows + claim_rows + target_rows
    )
    formalization_changed = formalization_changed_after_start()

    add("V939_0_sources_exist_and_needles", sources_ok, "all 939 source paths exist and needles are present" if sources_ok else "missing source path or needle")
    add("V939_1_prior_938_clean", prior_clean, "P8_Y5_BRR545_938_VALIDATION.csv clean")
    add("V939_2_vertical_theorem_conditional", total_conditional, "PiM vertical theorem remains conditional only")
    add("V939_3_contract_no_claim", contract_no_claim, "no vertical contract clause promoted")
    add("V939_4_topological_route_selected", topological_selected, "topological absolute route selected as best derivation route")
    add("V939_5_hodge_rejected_free_GR", hodge_rejected, "Hodge/DeWitt projector rejected as free-GR route")
    add("V939_6_readout_rejected", readout_rejected, "readout PiM rejected as derivation")
    add("V939_7_Cbeta_defined", cbeta_defined, "C_beta_N5 weak-field definition written")
    add("V939_8_beta_bound_loaded", cbeta_bound_loaded, "R4 beta bound 7.8e-05 loaded")
    add("V939_9_residuals_blocked", residuals_blocked, "all retained residual rows remain non-scoreable")
    add("V939_10_decisions_nonclaim", decisions_nonclaim, "decision ledger remains nonclaim")
    add("V939_11_claim_gates_false", claims_false, "all claim gates remain false")
    add("V939_12_next_target_selected", next_selected, "940 chain-map/Hilbert-equality target selected")
    add("V939_13_no_claims_promoted", no_claims, "all generated rows are valid_for_claim=false")
    add("V939_14_formalization_workbench_untouched", formalization_changed == 0, f"formalization_changed_after_start={formalization_changed}")
    add("V939_15_validation_rows_ready", True, "validation table constructed")
    return rows


def write_doc(
    sources: list[dict[str, str]],
    contract_rows: list[dict[str, str]],
    route_rows: list[dict[str, str]],
    cbeta_rows: list[dict[str, str]],
    residual_rows_: list[dict[str, str]],
    decision_rows: list[dict[str, str]],
    claim_rows: list[dict[str, str]],
    target_rows: list[dict[str, str]],
    validation_rows: list[dict[str, str]],
) -> None:
    text = f"""# 939 - Y5/R10 Projector PiM Vertical Generator Or CbetaN5 Weak Field Map

Generated: `{stamp()}`

Status: `Y5_R10_939_PiM_vertical_generator_not_proved_topological_route_selected_CbetaN5_defined_nonclaim`

Claim ceiling: `PiM_vertical_contract_and_CbetaN5_definition_only_no_projector_zero_no_beta_score_no_local_GR_pass`

## Result

The best route is still the clean one:

```text
Pi_M J = ell_M(J) omega_M_top,
delta_g Pi_M = 0,
[d,Pi_M]J_H = 0,
Pi_M J_H = J_M^top + dB_zero,
int_boundary dB_zero = 0.
```

If the parent action signs those clauses, `Pi_M` becomes an owned vertical/topological/Hamiltonian generator rather than a projector mask. That would kill the N5 projector stress at the root.

But 939 does **not** prove it. The route remains conditional because the chain-map/source-current domain, Hilbert/topological equality, zero-flux representative, and measured-GM calibration are still unsigned.

The Hodge/DeWitt route is rejected as a free-GR proof: it may give nice projector algebra, but metric variation generically creates `T_PiM` unless explicitly retained or cancelled.

The fallback weak-field beta map is now precise but nonnumeric:

```text
g_00 = -1 + 2U - 2 beta U^2 + O(v^6),
C_beta_N5 := - delta g_00^(4)|_N5 / (2 U^2 X_N5),
score only if |C_beta_N5 X_N5| <= 7.8e-05.
```

`C_beta_N5` and `X_N5` still need either a second-order weak-field solver or parent-signed zero theorem, so beta remains unscored.

## Source Register

{md_table(sources, ["source_id", "path", "role", "needle_found", "valid_for_claim"])}

## PiM Vertical Generator Contract

{md_table(contract_rows, ["clause_id", "statement", "mathematical_form", "current_status", "claim_allowed"])}

## Route Audit

{md_table(route_rows, ["route_id", "route", "mathematical_form", "status", "blocker", "decision"])}

## Weak-Field Cbeta Map

{md_table(cbeta_rows, ["map_id", "symbol", "definition_or_formula", "source_or_missing_input", "status", "score_ready"])}

## Retained Residual Rows

{md_table(residual_rows_, ["residual_id", "symbol", "formula", "missing_before_score", "role", "score_ready"])}

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
    contract_rows = vertical_generator_contract()
    route_rows = route_audit()
    cbeta_rows = weak_field_cbeta_map()
    residual_rows_ = residual_rows()
    decision_rows = decisions()
    claim_rows = claim_gates()
    target_rows = next_target()
    validation_rows = validation(sources, contract_rows, route_rows, cbeta_rows, residual_rows_, decision_rows, claim_rows, target_rows)

    output_specs = [
        (
            OUT / "P8_Y5_R10_939_SOURCE_REGISTER.csv",
            sources,
            ["source_id", "path", "absolute_path", "role", "needle", "exists", "needle_found", "valid_for_claim", "generated_utc"],
        ),
        (
            OUT / "P8_Y5_R10_939_PIM_VERTICAL_GENERATOR_CONTRACT.csv",
            contract_rows,
            ["clause_id", "statement", "mathematical_form", "why_needed", "current_status", "parent_signed", "claim_allowed", "valid_for_claim", "generated_utc"],
        ),
        (
            OUT / "P8_Y5_R10_939_ROUTE_AUDIT.csv",
            route_rows,
            ["route_id", "route", "mathematical_form", "status", "positive_part", "blocker", "decision", "claim_allowed", "valid_for_claim", "generated_utc"],
        ),
        (
            OUT / "P8_Y5_R10_939_WEAK_FIELD_CBETA_MAP.csv",
            cbeta_rows,
            ["map_id", "symbol", "definition_or_formula", "units", "source_or_missing_input", "status", "score_ready", "claim_allowed", "valid_for_claim", "generated_utc"],
        ),
        (
            OUT / "P8_Y5_R10_939_RETAINED_RESIDUAL_ROWS.csv",
            residual_rows_,
            ["residual_id", "symbol", "formula", "missing_before_score", "role", "score_ready", "claim_allowed", "valid_for_claim", "generated_utc"],
        ),
        (
            OUT / "P8_Y5_R10_939_DECISION_LEDGER.csv",
            decision_rows,
            ["decision_id", "decision", "reason", "consequence", "next_action", "valid_for_claim", "generated_utc"],
        ),
        (
            OUT / "P8_Y5_R10_939_CLAIM_GATE.csv",
            claim_rows,
            ["gate_id", "claim", "blocker", "claim_allowed", "valid_for_claim", "generated_utc"],
        ),
        (
            OUT / "P8_Y5_R10_939_NEXT_TARGET.csv",
            target_rows,
            ["next_target", "objective", "include", "exclude", "valid_for_claim", "generated_utc"],
        ),
        (
            OUT / "P8_Y5_BRR545_939_VALIDATION.csv",
            validation_rows,
            ["check_id", "result", "detail", "generated_utc"],
        ),
    ]

    for path, rows, fieldnames in output_specs:
        write_csv(path, rows, fieldnames)

    ensure_csv_roundtrip([path for path, _rows, _fieldnames in output_specs])
    write_doc(sources, contract_rows, route_rows, cbeta_rows, residual_rows_, decision_rows, claim_rows, target_rows, validation_rows)

    failures = [row for row in validation_rows if row["result"] != "pass"]
    if failures:
        raise SystemExit(f"validation failed: {failures}")

    print("Y5_R10_939_PiM_vertical_generator_not_proved_topological_route_selected_CbetaN5_defined_nonclaim")
    print(f"wrote {DOC}")
    print("next target: 940-Y5-R10-chain-map-Hilbert-equality-or-CbetaN5-operator-source.md")


if __name__ == "__main__":
    main()
