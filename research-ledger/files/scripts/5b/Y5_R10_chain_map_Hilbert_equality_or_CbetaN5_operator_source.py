from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds" / "local_bound_claims.csv"
DOC = ROOT / "940-Y5-R10-chain-map-Hilbert-equality-or-CbetaN5-operator-source.md"
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
            "source_id": "939_doc",
            "path": "939-Y5-R10-projector-PiM-vertical-generator-or-CbetaN5-weak-field-map.md",
            "role": "handoff selecting chain-map plus Hilbert equality",
            "needle": "940-Y5-R10-chain-map-Hilbert-equality-or-CbetaN5-operator-source.md",
        },
        {
            "source_id": "939_validation",
            "path": "source-intake/mts_residuals/P8_Y5_BRR545_939_VALIDATION.csv",
            "role": "previous checkpoint validation",
            "needle": "V939_15_validation_rows_ready",
        },
        {
            "source_id": "915_doc",
            "path": "915-Y5-R10-Hilbert-topological-mass-current-equality-or-projector-bound-pack-fill.md",
            "role": "equality route and Delta_HT_current",
            "needle": "Delta_HT_current :=",
        },
        {
            "source_id": "920_doc",
            "path": "920-Y5-R10-PiM-current-offshell-closure-and-holonomy-zero-or-FM-force-bound.md",
            "role": "off-shell closure factorization",
            "needle": "d(Pi_M J_H) = Pi_M dJ_H + [d,Pi_M] J_H.",
        },
        {
            "source_id": "501_doc",
            "path": "501-topological-Hilbert-current-equality-or-radial-bound-runner.md",
            "role": "older topological-Hilbert equality attempt",
            "needle": "The equality theorem is not derived.",
        },
        {
            "source_id": "661_doc",
            "path": "661-Y5-R10-topological-Hilbert-current-equality-or-projector-stress-fill.md",
            "role": "same-worldtube route and equality residual",
            "needle": "Pi_M J_H = J_M_top + dB_zero + R_eq.",
        },
        {
            "source_id": "662_doc",
            "path": "662-Y5-R10-Hilbert-worldtube-source-measure-glue-or-equality-residual-bound.md",
            "role": "worldtube source-measure glue theorem",
            "needle": "R_glue :=",
        },
        {
            "source_id": "663_doc",
            "path": "663-Y5-R10-minimal-parent-action-source-current-Euler-Ward-test-or-residual-input-fill.md",
            "role": "minimal Euler/Ward and Hamiltonian PiM repair",
            "needle": "(4*pi*G_ref)^-1 int_S Pi_M J_H",
        },
        {
            "source_id": "660_commutator",
            "path": "source-intake/mts_residuals/P8_Y5_R10_660_COMMUTATOR_ZERO_AUDIT.csv",
            "role": "commutator zero clauses",
            "needle": "CZ660_3_chain_map_property",
        },
        {
            "source_id": "662_proof_chain",
            "path": "source-intake/mts_residuals/P8_Y5_R10_662_PROOF_CHAIN.csv",
            "role": "worldtube proof chain",
            "needle": "P662_5_PiM_chain_map",
        },
        {
            "source_id": "662_parent_clause_audit",
            "path": "source-intake/mts_residuals/P8_Y5_R10_662_PARENT_CLAUSE_AUDIT.csv",
            "role": "parent clause audit for worldtube glue",
            "needle": "CL662_4_action_owned_PiM_chain_map",
        },
        {
            "source_id": "939_cbeta_map",
            "path": "source-intake/mts_residuals/P8_Y5_R10_939_WEAK_FIELD_CBETA_MAP.csv",
            "role": "weak-field Cbeta definition",
            "needle": "WFM939_2_C_beta_N5",
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


def chain_equality_proof_stack() -> list[dict[str, str]]:
    specs = [
        (
            "CES940_0_same_frame_current",
            "Hilbert source current is defined in the observed frame before readout",
            "J_H[tau] := delta S_matter/delta e_obs contracted with tau",
            "same-frame measure required before any topological/Hamiltonian equality can mean measured source mass",
            "same_frame_measure_unsigned",
        ),
        (
            "CES940_1_parent_worldtube",
            "compact source worldtube and linking surfaces are parent-selected",
            "W_source=supp(J_H[tau]); S_1,S_2 link the same W_source",
            "stops Pi_M from being retuned per radius/system",
            "worldtube_selector_unsigned",
        ),
        (
            "CES940_2_chain_map",
            "Pi_M is action-owned and commutes with d on the Hilbert source-current complex",
            "[d,Pi_M]J_H=0 and J_H,dJ_H in Dom(Pi_M)",
            "kills the commutator piece in d(Pi_M J_H)",
            "not_parent_signed",
        ),
        (
            "CES940_3_same_worldtube_topology",
            "topological current is Poincare-dual to the same Hilbert source worldtube",
            "J_M^top := Q_H[W] PD(W_source), not Q_independent omega_independent",
            "prevents the conserved topological current from being the wrong object",
            "not_parent_signed_key_blocker",
        ),
        (
            "CES940_4_equality_and_zero_flux",
            "Hilbert/topological equality holds up to exact zero-flux term",
            "J_M^top = Pi_M J_H + dB_zero and int_boundary dB_zero=0",
            "then d(Pi_M J_H)=dJ_M^top=0 and no boundary monopole is hidden",
            "not_parent_signed",
        ),
        (
            "CES940_5_no_hidden_exchange",
            "extra/domain/boundary/memory sectors carry no independent projected mass charge",
            "Pi_M dJ_extra=0 and Delta_extra_vector=0 or source-backed below locks",
            "keeps total Ward conservation from hiding mass exchange",
            "not_parent_signed",
        ),
        (
            "CES940_6_measured_GM_calibration",
            "closed charge calibrates to inverse-square measured GM and second-order PPN source",
            "mu_obs=G_eff M_eff[Pi_M J_H]; g_00=-1+2G_eff M/r+O(r^-2)",
            "turns source closure into Newton/local-GR relevance",
            "not_reached",
        ),
        (
            "CES940_7_total_verdict",
            "if CES940_0 through CES940_6 hold, chain-map/equality closes the PiM branch",
            "[d,Pi_M]J_H=0; R_glue=0; d(Pi_M J_H)=0; Delta_symp_projector=0",
            "would be a real GR-facing source-normalization derivation",
            "conditional_theorem_not_current_claim",
        ),
    ]
    return [
        {
            "step_id": step_id,
            "needed_statement": needed_statement,
            "mathematical_form": mathematical_form,
            "why_needed": why_needed,
            "current_status": current_status,
            "parent_signed": "false",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
        for step_id, needed_statement, mathematical_form, why_needed, current_status in specs
    ]


def equality_route_audit() -> list[dict[str, str]]:
    specs = [
        (
            "ERA940_0_same_worldtube_PD",
            "same-worldtube topological route",
            "Q_H[W]=parent Hilbert source charge; J_M^top=Q_H[W]PD(W_source)",
            "best_derivation_route",
            "makes topology and Hilbert source born as the same object",
            "parent worldtube selector, source measure, and same-object proof are still unsigned",
            "selected_next",
        ),
        (
            "ERA940_1_Ward_Killing",
            "Ward/Killing Hilbert current",
            "nabla_mu T_H^{mu nu}=0 plus tau/Killing gives d(Pi_M J_H)=0 only if exchange flux vanishes",
            "conditional_support_only",
            "standard GR-like support",
            "does not isolate Pi_M channel or hidden exchange by itself",
            "not_enough",
        ),
        (
            "ERA940_2_Hamiltonian_boundary",
            "Hamiltonian boundary dictionary",
            "B_xi/G_ref = M_eff[Pi_M J_H]",
            "powerful_crosscheck_downstream",
            "connects to GR charge language",
            "integrability, fixed reference, source frame, and Gauss/PPN readout remain open",
            "deferred",
        ),
        (
            "ERA940_3_glue_multiplier",
            "late equality multiplier",
            "S_glue=int Lambda_eq wedge(Pi_M J_H-J_M^top-dB_zero)",
            "rejected_as_derivation_unless_independently_owned",
            "would impose the desired equality",
            "without gauge/topological/Ward origin it is a dressed closure axiom",
            "rejected",
        ),
        (
            "ERA940_4_retained_residual",
            "retain R_glue and PiM residual vector",
            "R_glue=Pi_M J_H-J_M^top-dB_zero=sum R_i",
            "fallback_ready_not_filled",
            "keeps branch falsifiable if theorem stalls",
            "needs numeric/source-backed profiles or theorem-zero component rows",
            "active_fallback",
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


def residual_decomposition() -> list[dict[str, str]]:
    specs = [
        (
            "RGL940_0_R_worldtube",
            "R_worldtube",
            "failure of W_source and linking surfaces to be fixed by parent Hilbert support before readout",
            "MISSING_PARENT_WORLDTUBE_SELECTOR",
            "domain/orbital/R10 sensitivity",
        ),
        (
            "RGL940_1_R_measure",
            "R_measure;Delta_frame",
            "same-frame Hilbert measure/coframe/source-current ownership failure",
            "MISSING_SAME_FRAME_MEASURE_PROOF",
            "WEP/clock/preferred-frame sensitivity",
        ),
        (
            "RGL940_2_R_PiM",
            "R_PiM;I_commutator;T_PiM",
            "Pi_M chain-map, commutator, or projector-stress failure",
            "MISSING_PIM_CHAIN_MAP_OR_BOUND",
            "PPN gamma/beta/source-normalization sensitivity",
        ),
        (
            "RGL940_3_R_top",
            "R_top;R_eq",
            "topological representative is not same Hilbert worldtube object",
            "MISSING_TOPOLOGICAL_SAME_OBJECT_PROOF",
            "wrong-conserved-object risk",
        ),
        (
            "RGL940_4_R_boundary",
            "R_boundary;B_zero_flux;Delta_symp",
            "reference/background/exact improvement flux shifts compact charge",
            "MISSING_BOUNDARY_ZERO_PROOF_OR_BOUND",
            "measured GM/boundary hair",
        ),
        (
            "RGL940_5_R_extra",
            "R_extra;Delta_extra_vector",
            "non-EH/domain/memory/range/connection/source channels carry compact mass charge",
            "MISSING_EXTRA_SECTOR_SILENCE_OR_COEFFICIENTS",
            "local-GR/PPN/R10 hidden-channel risk",
        ),
        (
            "RGL940_6_R_readout",
            "Delta_cal;Delta_PPN",
            "closed dressed source charge does not calibrate to orbital GM or second-order PPN",
            "NOT_REACHED_UNTIL_GLUE_CLOSES",
            "Newton/PPN/local-GR readout",
        ),
    ]
    return [
        {
            "residual_id": residual_id,
            "symbol": symbol,
            "definition": definition,
            "missing_before_score": missing_before_score,
            "observable_link": observable_link,
            "score_ready": "false",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
        for residual_id, symbol, definition, missing_before_score, observable_link in specs
    ]


def cbeta_operator_source() -> list[dict[str, str]]:
    beta_bound = ""
    beta_source = ""
    for row in read_csv(LOCAL_BOUNDS):
        if row.get("row_id") == "R4_beta":
            beta_bound = row.get("upper_bound", "")
            beta_source = row.get("reference_path_or_url", "")
            break
    specs = [
        (
            "CBS940_0_operator_definition",
            "L_EH^{(4)}[delta g_00_N5]",
            "linearized second-order EH/PPN operator mapping retained N5 source vector to g_00^(4)",
            "MISSING_SECOND_ORDER_WEAK_FIELD_SOLVER",
            "operator_not_sourced",
        ),
        (
            "CBS940_1_source_vector",
            "S_N5",
            "S_N5 := {T_PiM, I_commutator, R_glue, B_zero_flux, Delta_extra, Delta_cal}",
            "MISSING_NUMERIC_SOURCE_VECTOR",
            "source_vector_not_numeric",
        ),
        (
            "CBS940_2_C_beta_N5",
            "C_beta_N5",
            "C_beta_N5 := - delta g_00^(4)|_N5/(2 U^2 X_N5)",
            "MISSING_OPERATOR_SOLUTION_AND_PROFILE",
            "formal_definition_only",
        ),
        (
            "CBS940_3_X_N5",
            "X_N5",
            "X_N5 := component-sum-normalized |R_glue + projector + boundary + extra|/M_ref",
            "MISSING_COMPONENT_INPUTS",
            "formal_definition_only",
        ),
        (
            "CBS940_4_R4_beta_bound",
            "beta_bound",
            beta_bound,
            beta_source,
            "source_bound_loaded",
        ),
        (
            "CBS940_5_score_gate",
            "score_gate",
            "|C_beta_N5 X_N5| <= 7.8e-05 with all components source-backed or theorem-zero",
            "derived_gate_no_numeric_prediction",
            "score_blocked",
        ),
    ]
    return [
        {
            "operator_id": operator_id,
            "symbol": symbol,
            "definition_or_formula": definition_or_formula,
            "source_or_missing_input": source_or_missing_input,
            "status": status,
            "score_ready": "false",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
        for operator_id, symbol, definition_or_formula, source_or_missing_input, status in specs
    ]


def decisions() -> list[dict[str, str]]:
    return [
        {
            "decision_id": "DEC940_0_chain_equality",
            "decision": "chain_map_Hilbert_equality_not_proved",
            "reason": "same-frame current, parent worldtube selector, chain-map domain, same-worldtube topological representative, zero flux, and calibration remain unsigned",
            "consequence": "d(Pi_M J_H)=0 and local-GR source normalization cannot be claimed",
            "next_action": "target Hilbert worldtube/source-measure same-object glue",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC940_1_best_route",
            "decision": "same_worldtube_PD_route_selected",
            "reason": "it avoids a late equality multiplier by making Q_H and J_M^top the same parent Hilbert worldtube object",
            "consequence": "next proof should attack worldtube selector and source measure directly",
            "next_action": "941-Y5-R10-Hilbert-worldtube-same-object-glue-or-CbetaN5-operator-fill.md",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC940_2_Cbeta_operator",
            "decision": "Cbeta_operator_schema_written_not_sourced",
            "reason": "beta operator needs second-order weak-field solver and source vector; equality route has not supplied theorem-zero components",
            "consequence": "beta fallback remains nonnumeric and nonclaim",
            "next_action": "source weak-field operator only if same-worldtube glue stalls",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def claim_gates() -> list[dict[str, str]]:
    return [
        {
            "gate_id": "CGATE940_0_commutator_zero",
            "claim": "[d,Pi_M]J_H=0",
            "blocker": "action-owned PiM chain map and fixed source-current domain are not parent-signed",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CGATE940_1_Hilbert_topological_equality",
            "claim": "J_M^top=Pi_M J_H+dB_zero",
            "blocker": "same-worldtube topological representative and equality theorem are not derived",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CGATE940_2_closed_projected_flux",
            "claim": "d(Pi_M J_H)=0",
            "blocker": "commutator zero, equality, zero boundary flux, and hidden exchange silence remain unsigned",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CGATE940_3_Cbeta_score",
            "claim": "C_beta_N5 operator/source row is numeric and scoreable",
            "blocker": "second-order weak-field solver and source vector are missing",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CGATE940_4_local_GR",
            "claim": "Newton/local-GR/PPN branch is derived",
            "blocker": "source equality and measured-GM calibration are not closed",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def next_target() -> list[dict[str, str]]:
    return [
        {
            "next_target": "941-Y5-R10-Hilbert-worldtube-same-object-glue-or-CbetaN5-operator-fill.md",
            "objective": "prove the topological charge and Hilbert source charge are the same parent worldtube object, or fill the first C_beta_N5 operator/source row",
            "include": "W_source=supp(J_H), Q_H[W], J_M^top=Q_H[W]PD(W_source), fixed linking surfaces, same observed source frame, zero B_zero flux, fallback weak-field operator inputs",
            "exclude": "late equality multiplier, independent topological label, assuming commutator zero, beta pass claim, local-GR claim, GitHub action, formalization-workbench edits",
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
    stack_rows: list[dict[str, str]],
    route_rows: list[dict[str, str]],
    residual_rows: list[dict[str, str]],
    cbeta_rows: list[dict[str, str]],
    decision_rows: list[dict[str, str]],
    claim_rows: list[dict[str, str]],
    target_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    rows = []

    def add(check_id: str, passed: bool, detail: str) -> None:
        rows.append({"check_id": check_id, "result": "pass" if passed else "fail", "detail": detail, "generated_utc": stamp()})

    prior = read_csv(OUT / "P8_Y5_BRR545_939_VALIDATION.csv")
    prior_clean = prior and all(row.get("result") == "pass" for row in prior)
    sources_ok = all(row["exists"] == "true" and row["needle_found"] == "true" for row in sources)
    total_conditional = any(row["step_id"] == "CES940_7_total_verdict" and row["current_status"] == "conditional_theorem_not_current_claim" for row in stack_rows)
    stack_no_claim = all(row["claim_allowed"] == "false" and row["valid_for_claim"] == "false" for row in stack_rows)
    same_worldtube_selected = any(row["route_id"] == "ERA940_0_same_worldtube_PD" and row["decision"] == "selected_next" for row in route_rows)
    multiplier_rejected = any(row["route_id"] == "ERA940_3_glue_multiplier" and row["decision"] == "rejected" for row in route_rows)
    residuals_blocked = residual_rows and all(row["score_ready"] == "false" and row["claim_allowed"] == "false" for row in residual_rows)
    cbeta_blocked = any(row["operator_id"] == "CBS940_2_C_beta_N5" and row["status"] == "formal_definition_only" for row in cbeta_rows) and any(row["operator_id"] == "CBS940_5_score_gate" and row["status"] == "score_blocked" for row in cbeta_rows)
    beta_bound_loaded = any(row["operator_id"] == "CBS940_4_R4_beta_bound" and row["definition_or_formula"] == "7.8e-05" for row in cbeta_rows)
    decisions_nonclaim = all(row["valid_for_claim"] == "false" for row in decision_rows)
    claims_false = all(row["claim_allowed"] == "false" and row["valid_for_claim"] == "false" for row in claim_rows)
    next_selected = any(row["next_target"].startswith("941-Y5-R10-Hilbert-worldtube-same-object-glue") for row in target_rows)
    no_claims = all(
        row.get("valid_for_claim") == "false"
        for row in sources + stack_rows + route_rows + residual_rows + cbeta_rows + decision_rows + claim_rows + target_rows
    )
    formalization_changed = formalization_changed_after_start()

    add("V940_0_sources_exist_and_needles", sources_ok, "all 940 source paths exist and needles are present" if sources_ok else "missing source path or needle")
    add("V940_1_prior_939_clean", prior_clean, "P8_Y5_BRR545_939_VALIDATION.csv clean")
    add("V940_2_total_theorem_conditional", total_conditional, "chain/equality theorem remains conditional only")
    add("V940_3_stack_no_claim", stack_no_claim, "no proof-stack row promoted")
    add("V940_4_same_worldtube_selected", same_worldtube_selected, "same-worldtube PD route selected")
    add("V940_5_multiplier_rejected", multiplier_rejected, "late equality multiplier rejected as derivation")
    add("V940_6_residuals_blocked", residuals_blocked, "R_glue component rows remain non-scoreable")
    add("V940_7_Cbeta_operator_blocked", cbeta_blocked, "C_beta_N5 operator/source remains formal and blocked")
    add("V940_8_beta_bound_loaded", beta_bound_loaded, "R4 beta bound 7.8e-05 loaded")
    add("V940_9_decisions_nonclaim", decisions_nonclaim, "decision ledger remains nonclaim")
    add("V940_10_claim_gates_false", claims_false, "all claim gates remain false")
    add("V940_11_next_target_selected", next_selected, "941 Hilbert-worldtube same-object glue selected")
    add("V940_12_no_claims_promoted", no_claims, "all generated rows are valid_for_claim=false")
    add("V940_13_formalization_workbench_untouched", formalization_changed == 0, f"formalization_changed_after_start={formalization_changed}")
    add("V940_14_validation_rows_ready", True, "validation table constructed")
    return rows


def write_doc(
    sources: list[dict[str, str]],
    stack_rows: list[dict[str, str]],
    route_rows: list[dict[str, str]],
    residual_rows: list[dict[str, str]],
    cbeta_rows: list[dict[str, str]],
    decision_rows: list[dict[str, str]],
    claim_rows: list[dict[str, str]],
    target_rows: list[dict[str, str]],
    validation_rows: list[dict[str, str]],
) -> None:
    text = f"""# 940 - Y5/R10 Chain Map Hilbert Equality Or CbetaN5 Operator Source

Generated: `{stamp()}`

Status: `Y5_R10_940_chain_map_Hilbert_equality_not_proved_same_worldtube_route_selected_Cbeta_operator_schema_nonclaim`

Claim ceiling: `chain_map_and_Hilbert_equality_gate_only_no_closed_PiM_flux_no_beta_score_no_local_GR_pass`

## Result

The joint proof target is now:

```text
[d,Pi_M]J_H = 0,
J_M^top = Pi_M J_H + dB_zero,
int_boundary dB_zero = 0,
dJ_M^top = 0
=> d(Pi_M J_H)=0.
```

The clean route is not a late multiplier. It is to make the topological current the Poincare-dual representative of the **same parent Hilbert source worldtube**:

```text
W_source = supp(J_H[tau]),
Q_H[W] = parent dressed Hilbert/Noether charge,
J_M^top = Q_H[W] PD(W_source).
```

That would make topology and Hilbert source charge the same object instead of closing a conserved wrong object.

But 940 does **not** prove it. The same-frame source current, parent worldtube selector, action-owned PiM chain map, same-worldtube topological representative, zero boundary flux, hidden exchange silence, and measured-GM calibration remain unsigned.

So `[d,Pi_M]J_H=0`, `R_glue=0`, `d(Pi_M J_H)=0`, beta safety, and local-GR reduction are still nonclaims.

The fallback `C_beta_N5` operator is now explicit but still not sourced:

```text
L_EH^(4)[delta g_00_N5] = source(T_PiM, I_commutator, R_glue, B_zero_flux, Delta_extra, Delta_cal),
C_beta_N5 := -delta g_00_N5^(4)/(2 U^2 X_N5),
score only if |C_beta_N5 X_N5| <= 7.8e-05.
```

## Source Register

{md_table(sources, ["source_id", "path", "role", "needle_found", "valid_for_claim"])}

## Chain Equality Proof Stack

{md_table(stack_rows, ["step_id", "needed_statement", "mathematical_form", "current_status", "claim_allowed"])}

## Equality Route Audit

{md_table(route_rows, ["route_id", "route", "mathematical_form", "status", "blocker", "decision"])}

## Residual Decomposition

{md_table(residual_rows, ["residual_id", "symbol", "definition", "missing_before_score", "observable_link", "score_ready"])}

## Cbeta Operator Source

{md_table(cbeta_rows, ["operator_id", "symbol", "definition_or_formula", "source_or_missing_input", "status", "score_ready"])}

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
    stack_rows = chain_equality_proof_stack()
    route_rows = equality_route_audit()
    residual_rows = residual_decomposition()
    cbeta_rows = cbeta_operator_source()
    decision_rows = decisions()
    claim_rows = claim_gates()
    target_rows = next_target()
    validation_rows = validation(sources, stack_rows, route_rows, residual_rows, cbeta_rows, decision_rows, claim_rows, target_rows)

    output_specs = [
        (
            OUT / "P8_Y5_R10_940_SOURCE_REGISTER.csv",
            sources,
            ["source_id", "path", "absolute_path", "role", "needle", "exists", "needle_found", "valid_for_claim", "generated_utc"],
        ),
        (
            OUT / "P8_Y5_R10_940_CHAIN_EQUALITY_PROOF_STACK.csv",
            stack_rows,
            ["step_id", "needed_statement", "mathematical_form", "why_needed", "current_status", "parent_signed", "claim_allowed", "valid_for_claim", "generated_utc"],
        ),
        (
            OUT / "P8_Y5_R10_940_EQUALITY_ROUTE_AUDIT.csv",
            route_rows,
            ["route_id", "route", "mathematical_form", "status", "positive_part", "blocker", "decision", "claim_allowed", "valid_for_claim", "generated_utc"],
        ),
        (
            OUT / "P8_Y5_R10_940_RESIDUAL_DECOMPOSITION.csv",
            residual_rows,
            ["residual_id", "symbol", "definition", "missing_before_score", "observable_link", "score_ready", "claim_allowed", "valid_for_claim", "generated_utc"],
        ),
        (
            OUT / "P8_Y5_R10_940_CBETA_OPERATOR_SOURCE.csv",
            cbeta_rows,
            ["operator_id", "symbol", "definition_or_formula", "source_or_missing_input", "status", "score_ready", "claim_allowed", "valid_for_claim", "generated_utc"],
        ),
        (
            OUT / "P8_Y5_R10_940_DECISION_LEDGER.csv",
            decision_rows,
            ["decision_id", "decision", "reason", "consequence", "next_action", "valid_for_claim", "generated_utc"],
        ),
        (
            OUT / "P8_Y5_R10_940_CLAIM_GATE.csv",
            claim_rows,
            ["gate_id", "claim", "blocker", "claim_allowed", "valid_for_claim", "generated_utc"],
        ),
        (
            OUT / "P8_Y5_R10_940_NEXT_TARGET.csv",
            target_rows,
            ["next_target", "objective", "include", "exclude", "valid_for_claim", "generated_utc"],
        ),
        (
            OUT / "P8_Y5_BRR545_940_VALIDATION.csv",
            validation_rows,
            ["check_id", "result", "detail", "generated_utc"],
        ),
    ]

    for path, rows, fieldnames in output_specs:
        write_csv(path, rows, fieldnames)

    ensure_csv_roundtrip([path for path, _rows, _fieldnames in output_specs])
    write_doc(sources, stack_rows, route_rows, residual_rows, cbeta_rows, decision_rows, claim_rows, target_rows, validation_rows)

    failures = [row for row in validation_rows if row["result"] != "pass"]
    if failures:
        raise SystemExit(f"validation failed: {failures}")

    print("Y5_R10_940_chain_map_Hilbert_equality_not_proved_same_worldtube_route_selected_Cbeta_operator_schema_nonclaim")
    print(f"wrote {DOC}")
    print("next target: 941-Y5-R10-Hilbert-worldtube-same-object-glue-or-CbetaN5-operator-fill.md")


if __name__ == "__main__":
    main()
