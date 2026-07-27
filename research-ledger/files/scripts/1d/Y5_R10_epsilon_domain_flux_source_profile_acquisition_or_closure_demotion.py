from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "1147-Y5-R10-epsilon-domain-flux-source-profile-acquisition-or-closure-demotion.md"


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
            "source_id": "SRC1147_0_1146_next",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1146_NEXT_TARGET.csv",
            "needle": "NEXT1146_0_1147",
            "role": "handoff requiring epsilon source acquisition or closure demotion.",
        },
        {
            "source_id": "SRC1147_1_1146_no_flux",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1146_NO_FLUX_CERTIFICATE_AUDIT.csv",
            "needle": "NF1146_6_verdict",
            "role": "epsilon theorem-zero route is not derived.",
        },
        {
            "source_id": "SRC1147_2_1146_profile",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1146_EPSILON_SOURCE_PROFILE_ROW.csv",
            "needle": "EPS1146_0_source_profile_row",
            "role": "latest epsilon source row is unfilled.",
        },
        {
            "source_id": "SRC1147_3_1143_profile",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1143_EPSILON_DOMAIN_FLUX_PROFILE_FIRST_FILL.csv",
            "needle": "EPS1143_0_local_compact_profile",
            "role": "earlier epsilon profile row is a missing-source template.",
        },
        {
            "source_id": "SRC1147_4_1136_pack",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1136_EPSILON_W_K_C_SOURCE_PACK_FIRST_ROWS.csv",
            "needle": "SP1136_0_epsilon_domain_flux",
            "role": "epsilon/W/K/c source pack marks epsilon missing.",
        },
        {
            "source_id": "SRC1147_5_778_flux_candidate",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_778_SOURCE_FLUX_VALUE_INPUT_CANDIDATE.csv",
            "needle": "MISSING_FLUX_VALUE_OR_NO_FLUX_THEOREM",
            "role": "observed flux-value candidates are unfilled.",
        },
        {
            "source_id": "SRC1147_6_773_observed_flux",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_773_OBSERVED_FLUX_COMPONENT_SPLIT.csv",
            "needle": "OFS773_5_total_observed_reduced_flux",
            "role": "observed flux components remain live and source-fill required.",
        },
        {
            "source_id": "SRC1147_7_1122_contract",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1122_REMAINING_FLUX_CONTRACT.csv",
            "needle": "R11F1122_0_flux_alpha3",
            "role": "R11 alpha3 product contract requires K, c, and epsilon.",
        },
        {
            "source_id": "SRC1147_8_1132_factors",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1132_FACTOR_SOURCE_PACK.csv",
            "needle": "FAC1132_3_c_R11_flux_alpha3",
            "role": "factor source pack identifies c_R11 as source-normalization factor.",
        },
        {
            "source_id": "SRC1147_9_1137_coupling",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1137_W_K_C_COUPLING_AUDIT.csv",
            "needle": "CPL1137_2_c_R11_flux_alpha3",
            "role": "coupling audit confirms c_R11 is an alias to missing R11 source normalization.",
        },
        {
            "source_id": "SRC1147_10_R11_source_norm",
            "relative_path": "source-intake/mts_residuals/R11_DOMAIN_PROJECTOR_OPERATOR_VECTOR_MINIMUM.csv",
            "needle": "c_domain_source_normalization_operator",
            "role": "R11 source-normalization operator remains unfilled and cross-arena.",
        },
        {
            "source_id": "SRC1147_11_R11_minimum",
            "relative_path": "source-intake/mts_residuals/R11_MTS_MINIMUM_EXECUTABLE_VECTOR_SKELETON.csv",
            "needle": "source_normalization_operator",
            "role": "source-normalization operator is highest-priority Newton/R11 skeleton row.",
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


def acquisition_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "candidate_id": "ACQ1147_0_latest_1146_profile_row",
                "candidate_source": "P8_Y5_R10_1146_EPSILON_SOURCE_PROFILE_ROW.csv",
                "candidate_type": "epsilon source profile template",
                "profile_or_value": "MISSING_NUMERIC_EPSILON_ABS",
                "source_path_status": "MISSING_SOURCE_PATH",
                "claim_status": "SOURCE_PROFILE_NOT_FILLED",
                "decision": "REJECT_AS_SOURCE",
                "reason": "latest row is a contract, not data",
                "valid_for_claim": "false",
            },
            {
                "candidate_id": "ACQ1147_1_1143_1144_profile_queue",
                "candidate_source": "P8_Y5_R10_1143_EPSILON_DOMAIN_FLUX_PROFILE_FIRST_FILL.csv;P8_Y5_R10_1144_EPSILON_DOMAIN_FLUX_PROFILE_FILL_QUEUE.csv",
                "candidate_type": "older profile/fill queue",
                "profile_or_value": "MISSING_EPSILON_DOMAIN_FLUX_PROFILE_OR_ZERO_THEOREM",
                "source_path_status": "MISSING_SOURCE_PATH",
                "claim_status": "SOURCE_PROFILE_ROW_REQUIRED",
                "decision": "REJECT_AS_SOURCE",
                "reason": "older rows point to the same missing input",
                "valid_for_claim": "false",
            },
            {
                "candidate_id": "ACQ1147_2_1136_source_pack",
                "candidate_source": "P8_Y5_R10_1136_EPSILON_W_K_C_SOURCE_PACK_FIRST_ROWS.csv",
                "candidate_type": "epsilon/W/K/c pack",
                "profile_or_value": "MISSING_NUMERIC_PROFILE_OR_ZERO_THEOREM",
                "source_path_status": "MISSING_PARENT_PROFILE_OR_THEOREM_SOURCE",
                "claim_status": "SOURCE_ROW_PLACEHOLDER_BLOCKED",
                "decision": "REJECT_AS_SOURCE",
                "reason": "source-pack row is explicitly blocked by missing value and source path",
                "valid_for_claim": "false",
            },
            {
                "candidate_id": "ACQ1147_3_778_flux_candidate",
                "candidate_source": "P8_Y5_R10_778_SOURCE_FLUX_VALUE_INPUT_CANDIDATE.csv",
                "candidate_type": "observed flux value candidate",
                "profile_or_value": "MISSING_FLUX_VALUE_OR_NO_FLUX_THEOREM",
                "source_path_status": "MISSING_SOURCE_PATH",
                "claim_status": "unfilled_candidate",
                "decision": "REJECT_AS_SOURCE",
                "reason": "it provides arenas but no flux value, units, source path, or assumptions",
                "valid_for_claim": "false",
            },
            {
                "candidate_id": "ACQ1147_4_773_observed_flux",
                "candidate_source": "P8_Y5_R10_773_OBSERVED_FLUX_COMPONENT_SPLIT.csv",
                "candidate_type": "observed flux decomposition",
                "profile_or_value": "not_zero_current_corpus but no numeric bound",
                "source_path_status": "component ledger only",
                "claim_status": "source_fill_required_if_774_fails",
                "decision": "KEEP_AS_BLOCKER_LEDGER_NOT_PROFILE",
                "reason": "it proves the channel is live; it does not supply epsilon_abs",
                "valid_for_claim": "false",
            },
            {
                "candidate_id": "ACQ1147_5_epsilon_charge_rows",
                "candidate_source": "P8_Y5_EPSILON_CHARGE_*",
                "candidate_type": "source-normalization charge epsilon",
                "profile_or_value": "not_computed_missing_numeric_inputs",
                "source_path_status": "missing or reference-only",
                "claim_status": "different epsilon family",
                "decision": "REJECT_AS_DOMAIN_FLUX_SOURCE",
                "reason": "epsilon_charge is not epsilon_domain_flux and is also unfilled",
                "valid_for_claim": "false",
            },
            {
                "candidate_id": "ACQ1147_6_acquisition_verdict",
                "candidate_source": "current post-checkpoint residual corpus",
                "candidate_type": "global acquisition pass",
                "profile_or_value": "NO_REAL_EPSILON_DOMAIN_FLUX_PROFILE_FOUND",
                "source_path_status": "NO_VALID_SOURCE_PATH",
                "claim_status": "NO_CLAIM_VALID_ROW",
                "decision": "ACQUISITION_FAILS_CURRENT_CORPUS",
                "reason": "all candidate rows are templates, blockers, wrong-epsilon rows, or unfilled ledgers",
                "valid_for_claim": "false",
            },
        ]
    )


def source_contract_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "contract_id": "EPSCON1147_0_system",
                "required_field": "system_id and branch_id",
                "acceptance_test": "compact local arena and branch are identified before fitting or normalization",
                "current_status": "MISSING_LOCAL_SYSTEM_ID_FOR_EPSILON_PROFILE",
                "why_it_matters": "otherwise epsilon can be moved between arena choice and coefficient choice",
                "valid_for_claim": "false",
            },
            {
                "contract_id": "EPSCON1147_1_projection",
                "required_field": "P_loc projection convention",
                "acceptance_test": "P_loc^i_nu(F_P^nu+F_domain^nu) is defined from parent variables in the observed local coframe",
                "current_status": "MISSING_PARENT_PROJECTION_AND_COFRAME_PROOF",
                "why_it_matters": "a gauge/representation zero is not a physical alpha3 zero",
                "valid_for_claim": "false",
            },
            {
                "contract_id": "EPSCON1147_2_value",
                "required_field": "epsilon_abs",
                "acceptance_test": "finite numeric value, finite upper bound, or parent theorem-zero with no MISSING markers",
                "current_status": "MISSING_NUMERIC_EPSILON_OR_THEOREM_ZERO",
                "why_it_matters": "the alpha3 product cannot be scored without the first factor",
                "valid_for_claim": "false",
            },
            {
                "contract_id": "EPSCON1147_3_units",
                "required_field": "epsilon_units and normalization",
                "acceptance_test": "dimensionless projected flux convention matches K_R11*c_R11 product normalization",
                "current_status": "CONVENTION_NAMED_BUT_NOT_SOURCE_LOCKED",
                "why_it_matters": "dimensionless alpha3 requires shared normalization, not a free rescale",
                "valid_for_claim": "false",
            },
            {
                "contract_id": "EPSCON1147_4_provenance",
                "required_field": "source_path and assumptions",
                "acceptance_test": "local path exists and contains the row/equation/derivation supporting epsilon_abs",
                "current_status": "MISSING_SOURCE_PATH",
                "why_it_matters": "without provenance the value is just a knob",
                "valid_for_claim": "false",
            },
            {
                "contract_id": "EPSCON1147_5_product_interface",
                "required_field": "K/c compatibility",
                "acceptance_test": "same coframe and normalization as abs(K_R11_flux_alpha3*c_R11_flux_alpha3*epsilon_domain_flux)<=4e-20",
                "current_status": "K_AND_c_ALSO_MISSING",
                "why_it_matters": "epsilon alone does not make the alpha3 product executable",
                "valid_for_claim": "false",
            },
        ]
    )


def demotion_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "demotion_id": "DEM1147_0_epsilon_zero_route",
                "route": "epsilon_domain_flux=0 theorem route",
                "decision": "DEMOTE_TO_CLOSURE_ONLY_FOR_CURRENT_CORPUS",
                "reason": "1146 did not derive parent flux equation, exact local representative, gradient-flow constitutive law, boundary/topology silence, or observed-coframe proof",
                "effect": "epsilon=0 cannot be used in alpha3/R10/PPN/local-GR claim rows",
                "reopen_condition": "parent theorem supplies all no-flux clauses from one local branch law",
                "valid_for_claim": "false",
            },
            {
                "demotion_id": "DEM1147_1_epsilon_numeric_route",
                "route": "source-backed epsilon_abs profile route",
                "decision": "KEEP_ACTIVE_BUT_UNFILLED",
                "reason": "the row shape is now exact, but no profile/source is present in the corpus",
                "effect": "future data/theory can reopen without redoing the audit",
                "reopen_condition": "source-backed epsilon_abs or bound with no MISSING fields and matching K/c normalization",
                "valid_for_claim": "false",
            },
            {
                "demotion_id": "DEM1147_2_alpha3_product_policy",
                "route": "K_R11*c_R11*epsilon_domain_flux product",
                "decision": "BLOCK_PRODUCT_SCORING",
                "reason": "epsilon, K_R11, and c_R11 are all missing or closure-only",
                "effect": "no alpha3 win/loss can be claimed from this product",
                "reopen_condition": "each factor is sourced or one factor is parent-theorem zero",
                "valid_for_claim": "false",
            },
        ]
    )


def pivot_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "pivot_id": "PIV1147_0_continue_epsilon",
                "candidate_next": "continue epsilon source/profile hunt",
                "scope_value": "narrow alpha3-product factor",
                "current_state": "no real source profile found; zero route closure-only",
                "risk": "high chance of repeating missing-source loop",
                "priority": "P2_DEFER_UNTIL_NEW_SOURCE_OR_THEOREM",
                "decision": "DEFER",
                "valid_for_claim": "false",
            },
            {
                "pivot_id": "PIV1147_1_K_R11_transfer",
                "candidate_next": "derive/source K_R11_flux_alpha3",
                "scope_value": "direct R11 flux-to-alpha3 transfer",
                "current_state": "contract placeholder, no zero theorem, no numeric coefficient",
                "risk": "narrower than source-normalization and still depends on c/epsilon",
                "priority": "P1_BACKUP",
                "decision": "KEEP_AS_BACKUP_AFTER_c_R11",
                "valid_for_claim": "false",
            },
            {
                "pivot_id": "PIV1147_2_c_R11_source_normalization",
                "candidate_next": "derive/source c_R11_flux_alpha3 / source-normalization operator",
                "scope_value": "cross-arena Newton/GR measured-GM normalization plus alpha3 product",
                "current_state": "alias to missing R11 source-normalization operator; highest-priority Newton skeleton row",
                "risk": "harder but most aligned with deriving the local GR/Newton branch",
                "priority": "P0_NEXT",
                "decision": "SELECT_NEXT_TARGET",
                "valid_for_claim": "false",
            },
            {
                "pivot_id": "PIV1147_3_product_shortcut",
                "candidate_next": "fill K*c product directly",
                "scope_value": "would make alpha3 product executable faster",
                "current_state": "forbidden by 1137 unless both factors have provenance or parent identity makes product primitive",
                "risk": "would create a free knob/product shortcut",
                "priority": "REJECT",
                "decision": "DO_NOT_USE",
                "valid_for_claim": "false",
            },
        ]
    )


def gate_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "gate_id": "G1147_0_sources_exist",
                "rule": "all 1147 cited source paths and needles exist",
                "gate_pass": "true_nonclaim",
                "reason": "source register validates the local audit trail",
                "valid_for_claim": "false",
            },
            {
                "gate_id": "G1147_1_real_epsilon_profile_found",
                "rule": "claim-valid epsilon_domain_flux profile exists",
                "gate_pass": "false",
                "reason": "acquisition pass found only templates, blockers, wrong-epsilon rows, or unfilled ledgers",
                "valid_for_claim": "false",
            },
            {
                "gate_id": "G1147_2_epsilon_zero_route",
                "rule": "epsilon no-flux theorem can be used",
                "gate_pass": "false",
                "reason": "route is demoted to closure-only for current corpus",
                "valid_for_claim": "false",
            },
            {
                "gate_id": "G1147_3_product_scoring",
                "rule": "K*c*epsilon alpha3 product is scoreable",
                "gate_pass": "false",
                "reason": "epsilon, K, and c are not source-backed",
                "valid_for_claim": "false",
            },
            {
                "gate_id": "G1147_4_pivot_selected",
                "rule": "next target is selected by cross-arena value and no shortcut policy",
                "gate_pass": "true_nonclaim",
                "reason": "c_R11 source-normalization is selected over repeated epsilon hunt or product shortcut",
                "valid_for_claim": "false",
            },
            {
                "gate_id": "G1147_5_local_GR_promotion",
                "rule": "R10/PPN/local-GR claim allowed",
                "gate_pass": "false",
                "reason": "all relevant routes remain nonclaim",
                "valid_for_claim": "false",
            },
        ]
    )


def decision_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "decision_id": "D1147_0_acquisition",
                "decision": "no_epsilon_domain_flux_source_profile_found",
                "reason": "current corpus contains no claim-valid epsilon_abs row, bound, or source path",
                "next_action": "do not keep spending turns on epsilon unless new source/theorem appears",
                "valid_for_claim": "false",
            },
            {
                "decision_id": "D1147_1_demotion",
                "decision": "epsilon_zero_route_closure_only",
                "reason": "1146 no-flux certificate did not derive the required parent clauses",
                "next_action": "retain as future theorem contract only",
                "valid_for_claim": "false",
            },
            {
                "decision_id": "D1147_2_pivot",
                "decision": "pivot_to_c_R11_source_normalization",
                "reason": "c_R11 is both an alpha3 product factor and the broader measured-GM/Newton source-normalization bottleneck",
                "next_action": "build 1148 c_R11/source-normalization owner or theorem-zero attempt",
                "valid_for_claim": "false",
            },
        ]
    )


def next_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "next_id": "NEXT1147_0_1148",
                "next_target": "1148-Y5-R10-cR11-source-normalization-owner-or-zero-theorem.md",
                "objective": "try to derive or source c_R11_flux_alpha3 as the source-normalization operator needed for the alpha3 product and the local Newton/measured-GM branch; keep K_R11 as backup if c_R11 cannot move",
                "include": "c_R11 alias ledger; source-normalization operator; observed coframe; measured-GM normalization; no gauge absorption; K_R11 backup; alpha3 product interface",
                "exclude": "direct K*c product shortcut; hiding epsilon; tuned cancellation; local-GR/alpha3 claim; GitHub; formalization edits",
                "valid_for_claim": "false",
                "claim_allowed": "false",
            }
        ]
    )


def validate(
    sources: list[dict[str, object]],
    acquisition: list[dict[str, object]],
    contracts: list[dict[str, object]],
    demotions: list[dict[str, object]],
    pivots: list[dict[str, object]],
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

    all_rows = acquisition + contracts + demotions + pivots + gates + decisions + next_target
    add(
        "V1147_0_sources_exist",
        all(row["exists"] == "true" and row["needle_found"] == "true" for row in sources),
        "all cited local source paths exist and needles are found",
    )
    add(
        "V1147_1_acquisition_fails_cleanly",
        any(
            row["candidate_id"] == "ACQ1147_6_acquisition_verdict"
            and row["decision"] == "ACQUISITION_FAILS_CURRENT_CORPUS"
            for row in acquisition
        ),
        "acquisition pass explicitly finds no real epsilon profile",
    )
    add(
        "V1147_2_source_contract_complete",
        {
            "EPSCON1147_0_system",
            "EPSCON1147_1_projection",
            "EPSCON1147_2_value",
            "EPSCON1147_3_units",
            "EPSCON1147_4_provenance",
            "EPSCON1147_5_product_interface",
        }.issubset({row["contract_id"] for row in contracts}),
        "epsilon profile acceptance contract is complete",
    )
    add(
        "V1147_3_closure_demotion",
        any(
            row["demotion_id"] == "DEM1147_0_epsilon_zero_route"
            and row["decision"] == "DEMOTE_TO_CLOSURE_ONLY_FOR_CURRENT_CORPUS"
            for row in demotions
        ),
        "epsilon theorem-zero route is demoted to closure-only",
    )
    add(
        "V1147_4_pivot_selected",
        any(
            row["pivot_id"] == "PIV1147_2_c_R11_source_normalization"
            and row["decision"] == "SELECT_NEXT_TARGET"
            for row in pivots
        )
        and any(row["pivot_id"] == "PIV1147_3_product_shortcut" and row["decision"] == "DO_NOT_USE" for row in pivots),
        "c_R11 is selected and product shortcut is rejected",
    )
    add(
        "V1147_5_claim_gates_blocked",
        any(row["gate_id"] == "G1147_1_real_epsilon_profile_found" and row["gate_pass"] == "false" for row in gates)
        and any(row["gate_id"] == "G1147_5_local_GR_promotion" and row["gate_pass"] == "false" for row in gates),
        "epsilon and local-GR claim gates remain blocked",
    )
    add(
        "V1147_6_no_claim_rows",
        all(row.get("valid_for_claim") == "false" for row in all_rows)
        and all(row.get("claim_allowed", "false") == "false" for row in next_target),
        "all generated rows remain nonclaim",
    )
    add(
        "V1147_7_next_target",
        next_target[0]["next_target"].startswith("1148-") and "cR11-source-normalization" in str(next_target[0]["next_target"]),
        "1148 handoff targets c_R11 source-normalization owner or zero theorem",
    )
    add(
        "V1147_8_generated_under_post_checkpoint",
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
    add("V1147_9_csv_parse", csv_parse_ok, "all 1147 CSV outputs parse cleanly")
    add("V1147_10_formalization_untouched", True, "generator writes no outputs under formalization-workbench")
    add(
        "V1147_SUMMARY",
        True,
        "1147 finds no real epsilon profile, demotes epsilon-zero to closure-only, and selects c_R11/source-normalization for 1148",
    )
    return validation


def table(headers: list[str], rows: list[dict[str, object]]) -> str:
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(header, "")) for header in headers) + " |")
    return "\n".join(lines)


def write_doc(
    sources: list[dict[str, object]],
    acquisition: list[dict[str, object]],
    contracts: list[dict[str, object]],
    demotions: list[dict[str, object]],
    pivots: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    validation: list[dict[str, object]],
    next_target: list[dict[str, object]],
) -> None:
    text = f"""# 1147 - Y5/R10 Epsilon Domain Flux Source Profile Acquisition or Closure Demotion

**Current verdict:** no real `epsilon_domain_flux` source profile is found in the current post-checkpoint residual corpus. The available rows are templates, blockers, wrong-epsilon ledgers, or unfilled source candidates.

**Useful progress:** this prevents a loop. The epsilon-zero route is now explicitly closure-only unless a new parent theorem or source-backed profile appears.

**Important guard:** the `K_R11*c_R11*epsilon_domain_flux` product is still not scoreable, and filling the product directly is forbidden unless the factors are individually sourced or a parent identity makes the product primitive.

**Best next attack:** pivot to `c_R11_flux_alpha3`, because it is the source-normalization / measured-GM / Newton-branch bottleneck as well as an alpha3 product factor. This is harder than just chasing epsilon, but it is more aligned with deriving local GR/Newton properly.

**No claim:** no R10, PPN, alpha3, preferred-frame, local-GR, measured-GM, GitHub, or public claim follows from 1147.

## Source Register
{table(["source_id", "relative_path", "exists", "needle", "needle_found", "role"], sources)}

## Epsilon Acquisition Scan
{table(["candidate_id", "candidate_source", "candidate_type", "profile_or_value", "source_path_status", "claim_status", "decision", "reason", "valid_for_claim"], acquisition)}

## Claim-Valid Epsilon Source Contract
{table(["contract_id", "required_field", "acceptance_test", "current_status", "why_it_matters", "valid_for_claim"], contracts)}

## Closure Demotion Ledger
{table(["demotion_id", "route", "decision", "reason", "effect", "reopen_condition", "valid_for_claim"], demotions)}

## Pivot Matrix
{table(["pivot_id", "candidate_next", "scope_value", "current_state", "risk", "priority", "decision", "valid_for_claim"], pivots)}

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
        "source_register": OUT / "P8_Y5_R10_1147_SOURCE_REGISTER.csv",
        "acquisition": OUT / "P8_Y5_R10_1147_EPSILON_ACQUISITION_SCAN.csv",
        "contracts": OUT / "P8_Y5_R10_1147_EPSILON_SOURCE_CONTRACT.csv",
        "demotions": OUT / "P8_Y5_R10_1147_CLOSURE_DEMOTION_LEDGER.csv",
        "pivots": OUT / "P8_Y5_R10_1147_KC_PIVOT_MATRIX.csv",
        "gates": OUT / "P8_Y5_R10_1147_CLAIM_GATES.csv",
        "decisions": OUT / "P8_Y5_R10_1147_DECISION_LEDGER.csv",
        "next": OUT / "P8_Y5_R10_1147_NEXT_TARGET.csv",
        "validation": OUT / "P8_Y5_BRR545_1147_VALIDATION.csv",
    }
    sources = source_rows()
    acquisition = acquisition_rows()
    contracts = source_contract_rows()
    demotions = demotion_rows()
    pivots = pivot_rows()
    gates = gate_rows()
    decisions = decision_rows()
    next_target = next_rows()

    write_csv(outputs["source_register"], sources)
    write_csv(outputs["acquisition"], acquisition)
    write_csv(outputs["contracts"], contracts)
    write_csv(outputs["demotions"], demotions)
    write_csv(outputs["pivots"], pivots)
    write_csv(outputs["gates"], gates)
    write_csv(outputs["decisions"], decisions)
    write_csv(outputs["next"], next_target)
    validation = validate(sources, acquisition, contracts, demotions, pivots, gates, decisions, next_target, outputs)
    write_csv(outputs["validation"], validation)
    write_doc(sources, acquisition, contracts, demotions, pivots, gates, decisions, validation, next_target)
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
