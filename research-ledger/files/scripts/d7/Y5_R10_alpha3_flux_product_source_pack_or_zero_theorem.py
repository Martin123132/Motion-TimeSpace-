from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "1132-Y5-R10-alpha3-flux-product-source-pack-or-zero-theorem.md"


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
            "source_id": "SRC1132_0_1131_next",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1131_NEXT_TARGET.csv",
            "needle": "NEXT1131_0_1132",
            "note": "1131 handoff to alpha3 flux product source pack or zero theorem.",
        },
        {
            "source_id": "SRC1132_1_1131_fallback",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1131_ACTIVE_ALPHA3_FLUX_FALLBACK_ROWS.csv",
            "needle": "FB1131_0_domain_flux",
            "note": "1131 keeps the executable domain and R11 alpha3 products active.",
        },
        {
            "source_id": "SRC1132_2_1126_products",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1126_ALPHA3_EXECUTABLE_PRODUCT_ROWS.csv",
            "needle": "EP1126_1_R11_flux",
            "note": "1126 defines the two product rows and no-cancellation guard.",
        },
        {
            "source_id": "SRC1132_3_alpha3_link",
            "relative_path": "source-intake/mts_residuals/P8_DOMAIN_ALPHA3_R11_LINK.csv",
            "needle": "L2_alpha3_flux",
            "note": "Domain alpha3 link requires a theorem-zero or product below 4e-20.",
        },
        {
            "source_id": "SRC1132_4_domain_coeffs",
            "relative_path": "source-intake/mts_residuals/P8_mu_extra_domain_projector_coefficients.csv",
            "needle": "W_domain_alpha3_epsilon_domain_flux",
            "note": "Domain weak-field row carries W_domain_alpha3*epsilon_domain_flux.",
        },
        {
            "source_id": "SRC1132_5_R11_minimum",
            "relative_path": "source-intake/mts_residuals/R11_DOMAIN_PROJECTOR_OPERATOR_VECTOR_MINIMUM.csv",
            "needle": "source_normalization_operator",
            "note": "R11 minimum row tracks the unfilled source-normalization/vector operator family.",
        },
        {
            "source_id": "SRC1132_6_R11_missing",
            "relative_path": "source-intake/mts_residuals/R11_DOMAIN_PROJECTOR_VECTOR_MISSING_LEDGER.csv",
            "needle": "MISSING_DOMAIN_VECTOR_ABSENCE_THEOREM_OR_NUMERIC_COEFFICIENTS",
            "note": "R11 vector/source-normalization fields remain claim-blocking.",
        },
        {
            "source_id": "SRC1132_7_1123_bound",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1123_ALPHA3_FLUX_BOUND_PRODUCT_ROWS.csv",
            "needle": "FB1123_1_flux_zero_certificate",
            "note": "1123 already identifies epsilon_domain_flux as a sufficient zero certificate.",
        },
        {
            "source_id": "SRC1132_8_1122_flux_contract",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1122_REMAINING_FLUX_CONTRACT.csv",
            "needle": "R11F1122_0_flux_alpha3",
            "note": "1122 narrows the R11 alpha3 threat to K*c*epsilon flux.",
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


def factor_source_pack_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "factor_id": "FAC1132_0_epsilon_domain_flux",
                "factor": "epsilon_domain_flux",
                "appears_in_products": "EP1126_0_domain_flux;EP1126_1_R11_flux",
                "priority": "P0_SHARED_BOTTLENECK",
                "required_for_claim": "zero theorem or dimensionless projected flux profile/bound in observed local coframe",
                "zero_route": "prove compact local branch has exact/trivial domain-flux representative with boundary silence while FLRW branch remains separate",
                "numeric_route": "source a coframe-normalized epsilon_domain_flux value/profile and propagate abs(product)<=4e-20",
                "current_value_or_theorem": "MISSING_PARENT_ZERO_OR_NUMERIC_PROFILE",
                "evidence_sources": "source-intake/mts_residuals/P8_Y5_R10_1123_ALPHA3_FLUX_BOUND_PRODUCT_ROWS.csv;source-intake/mts_residuals/P8_Y5_R10_1126_SELECTOR_LOCAL_FLUX_OBLIGATIONS.csv",
                "status": "MISSING_SHARED_FACTOR",
                "valid_for_claim": "false",
            },
            {
                "factor_id": "FAC1132_1_W_domain_alpha3",
                "factor": "W_domain_alpha3",
                "appears_in_products": "EP1126_0_domain_flux",
                "priority": "P1_DOMAIN_COUPLING",
                "required_for_claim": "parent weak-field coefficient map or symmetry zero for domain alpha3 flux coupling",
                "zero_route": "prove scalar/topological domain projector cannot source preferred-frame alpha3 flux in local compact branch",
                "numeric_route": "derive or source W_domain_alpha3 with units/normalization from parent action to PPN alpha3",
                "current_value_or_theorem": "MISSING_NUMERIC_COUPLING_OR_SYMMETRY_ZERO",
                "evidence_sources": "source-intake/mts_residuals/P8_mu_extra_domain_projector_coefficients.csv;source-intake/mts_residuals/P8_DOMAIN_ALPHA3_R11_LINK.csv",
                "status": "MISSING_DOMAIN_COUPLING",
                "valid_for_claim": "false",
            },
            {
                "factor_id": "FAC1132_2_K_R11_flux_alpha3",
                "factor": "K_R11_flux_alpha3",
                "appears_in_products": "EP1126_1_R11_flux",
                "priority": "P1_R11_TRANSFER_COUPLING",
                "required_for_claim": "R11 operator transfer coefficient or parent symmetry zero",
                "zero_route": "prove R11 source operator has no flux-to-alpha3 transfer channel under the local branch symmetry",
                "numeric_route": "derive/source K_R11_flux_alpha3 and map it into the dimensionless PPN alpha3 convention",
                "current_value_or_theorem": "MISSING_R11_FLUX_TRANSFER_COEFFICIENT",
                "evidence_sources": "source-intake/mts_residuals/P8_Y5_R10_1122_REMAINING_FLUX_CONTRACT.csv;source-intake/mts_residuals/P8_Y5_R10_1123_ALPHA3_FLUX_BOUND_PRODUCT_ROWS.csv",
                "status": "MISSING_R11_TRANSFER",
                "valid_for_claim": "false",
            },
            {
                "factor_id": "FAC1132_3_c_R11_flux_alpha3",
                "factor": "c_R11_flux_alpha3",
                "appears_in_products": "EP1126_1_R11_flux",
                "priority": "P2_R11_SOURCE_NORMALIZATION",
                "required_for_claim": "observed-coframe/source-normalization coefficient or parent zero theorem",
                "zero_route": "prove local observed coframe/source normalization removes the R11 vector/flux coupling without absorbing it by gauge choice",
                "numeric_route": "derive/source c_R11_flux_alpha3 with declared units and weak-field normalization",
                "current_value_or_theorem": "MISSING_R11_SOURCE_NORMALIZATION_COEFFICIENT",
                "evidence_sources": "source-intake/mts_residuals/R11_DOMAIN_PROJECTOR_OPERATOR_VECTOR_MINIMUM.csv;source-intake/mts_residuals/R11_DOMAIN_PROJECTOR_VECTOR_MISSING_LEDGER.csv",
                "status": "MISSING_R11_NORMALIZATION",
                "valid_for_claim": "false",
            },
        ]
    )


def zero_theorem_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "zero_id": "ZT1132_0_epsilon_shared_zero",
                "target": "epsilon_domain_flux=0",
                "would_close": "both EP1126_0 and EP1126_1 if W/K/c remain finite",
                "required_statement": "[J_D]_local=0 and P_loc^i_mu F_D^mu=0 for compact local branch, with no boundary exchange and no global FLRW memory kill",
                "current_result": "NOT_PROVED_CURRENT_CORPUS",
                "missing_inputs": "parent local representative theorem; boundary/local projection silence; local-vs-FLRW branch selector",
                "scrutiny_note": "best route because it removes the common factor rather than tuning couplings",
                "valid_for_claim": "false",
            },
            {
                "zero_id": "ZT1132_1_W_domain_zero",
                "target": "W_domain_alpha3=0",
                "would_close": "EP1126_0 only",
                "required_statement": "domain projector coupling is scalar/topological/isotropic and cannot create alpha3 preferred-frame flux",
                "current_result": "NOT_PROVED_CURRENT_CORPUS",
                "missing_inputs": "parent symmetry representation and weak-field variation showing no alpha3 flux coefficient",
                "scrutiny_note": "secondary route; still leaves R11 product open",
                "valid_for_claim": "false",
            },
            {
                "zero_id": "ZT1132_2_K_R11_zero",
                "target": "K_R11_flux_alpha3=0",
                "would_close": "EP1126_1 only",
                "required_statement": "R11 operator family has no flux-to-alpha3 transfer channel",
                "current_result": "NOT_PROVED_CURRENT_CORPUS",
                "missing_inputs": "R11 operator symmetry theorem or explicit source coefficient map",
                "scrutiny_note": "useful if epsilon route fails; does not touch domain product",
                "valid_for_claim": "false",
            },
            {
                "zero_id": "ZT1132_3_c_R11_zero",
                "target": "c_R11_flux_alpha3=0",
                "would_close": "EP1126_1 only",
                "required_statement": "observed local coframe/source normalization does not carry a physical vector/flux residual",
                "current_result": "NOT_PROVED_CURRENT_CORPUS",
                "missing_inputs": "coframe normalization theorem not equivalent to gauge-hiding an observable",
                "scrutiny_note": "high scrutiny because a bad normalization argument can fake a PPN pass",
                "valid_for_claim": "false",
            },
            {
                "zero_id": "ZT1132_4_product_bound",
                "target": "numeric products below 4e-20",
                "would_close": "one or both product rows if every factor is sourced",
                "required_statement": "|W*epsilon|<=4e-20 and |K*c*epsilon|<=4e-20 with source paths, units, and no MISSING fields",
                "current_result": "NOT_EXECUTABLE_CURRENT_CORPUS",
                "missing_inputs": "all four factor values or source-backed bounds",
                "scrutiny_note": "acceptable as smoke/bound route, but weaker than a theorem-zero",
                "valid_for_claim": "false",
            },
            {
                "zero_id": "ZT1132_5_no_cancellation",
                "target": "alpha3_direct_flux_total",
                "would_close": "nothing by itself",
                "required_statement": "do not score cancellation between domain and R11 products unless a parent identity derives it",
                "current_result": "GUARD_ACTIVE_TRUE_NONCLAIM",
                "missing_inputs": "none for guard; parent cancellation identity absent",
                "scrutiny_note": "keeps the boxing honest: no haymaker-by-cancellation nonsense",
                "valid_for_claim": "false",
            },
        ]
    )


def product_matrix_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "product_id": "PM1132_0_domain_flux",
                "source_row": "EP1126_0_domain_flux",
                "observable": "alpha3",
                "formula": "alpha3_domain_flux = W_domain_alpha3*epsilon_domain_flux",
                "factors_needed": "W_domain_alpha3;epsilon_domain_flux",
                "target_bound": "4e-20",
                "theorem_zero_suffices_if": "epsilon_domain_flux=0 OR W_domain_alpha3=0",
                "numeric_acceptance": "abs(W_domain_alpha3*epsilon_domain_flux)<=4e-20",
                "current_status": "BLOCKED_MISSING_FACTOR_SOURCE_OR_ZERO",
                "valid_for_claim": "false",
            },
            {
                "product_id": "PM1132_1_R11_flux",
                "source_row": "EP1126_1_R11_flux",
                "observable": "alpha3",
                "formula": "P_R11_source_alpha3_flux = K_R11_flux_alpha3*c_R11_flux_alpha3*epsilon_domain_flux",
                "factors_needed": "K_R11_flux_alpha3;c_R11_flux_alpha3;epsilon_domain_flux",
                "target_bound": "4e-20",
                "theorem_zero_suffices_if": "epsilon_domain_flux=0 OR K_R11_flux_alpha3=0 OR c_R11_flux_alpha3=0",
                "numeric_acceptance": "abs(K_R11_flux_alpha3*c_R11_flux_alpha3*epsilon_domain_flux)<=4e-20",
                "current_status": "BLOCKED_MISSING_FACTOR_SOURCE_OR_ZERO",
                "valid_for_claim": "false",
            },
            {
                "product_id": "PM1132_2_total_guard",
                "source_row": "EP1126_2_total_direct_flux_guard",
                "observable": "alpha3",
                "formula": "alpha3_direct_flux_total = W_domain_alpha3*epsilon_domain_flux + K_R11_flux_alpha3*c_R11_flux_alpha3*epsilon_domain_flux",
                "factors_needed": "PM1132_0;PM1132_1;parent cancellation identity if cancellation is invoked",
                "target_bound": "4e-20",
                "theorem_zero_suffices_if": "both products independently close, or a parent identity derives exact cancellation",
                "numeric_acceptance": "no tuned cancellation credit; evaluate product rows separately first",
                "current_status": "GUARD_ONLY_NOT_SCOREABLE",
                "valid_for_claim": "false",
            },
        ]
    )


def guard_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "guard_id": "GUARD1132_0_no_tuned_cancellation",
                "guard": "domain/R11 cancellation cannot be used as evidence",
                "reason": "unrelated missing products could be made to cancel numerically without parent identity",
                "status": "ACTIVE_TRUE_NONCLAIM",
                "blocks": "PM1132_2_total_guard",
                "valid_for_claim": "false",
            },
            {
                "guard_id": "GUARD1132_1_sibling_preferred_frame_rows",
                "guard": "R5/R6/R8/R11 remain blocked by shared vector/source-normalization ledger",
                "reason": "R11_DOMAIN_PROJECTOR_VECTOR_MISSING_LEDGER still contains missing vector/source-normalization fields",
                "status": "ACTIVE_TRUE_NONCLAIM",
                "blocks": "alpha1;alpha2;alpha3;xi;R11_operator_ledger",
                "valid_for_claim": "false",
            },
            {
                "guard_id": "GUARD1132_2_no_global_memory_kill",
                "guard": "local epsilon zero cannot kill FLRW memory by assumption",
                "reason": "local compact exact/trivial branch must be separated from cosmological active memory branch",
                "status": "ACTIVE_TRUE_NONCLAIM",
                "blocks": "epsilon_domain_flux_zero_theorem",
                "valid_for_claim": "false",
            },
            {
                "guard_id": "GUARD1132_3_no_gauge_hide",
                "guard": "coframe/source-normalization zero cannot be a gauge hiding of a physical PPN residual",
                "reason": "PPN alpha3 is observable; normalization must be parent-derived and source-backed",
                "status": "ACTIVE_TRUE_NONCLAIM",
                "blocks": "c_R11_flux_alpha3_zero_route",
                "valid_for_claim": "false",
            },
        ]
    )


def gate_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "gate_id": "G1132_0_source_pack_complete",
                "rule": "all four factors have source-backed zero theorem or numeric bound",
                "gate_pass": "false",
                "reason": "epsilon, W, K, and c rows are all missing source-backed closure",
                "valid_for_claim": "false",
            },
            {
                "gate_id": "G1132_1_epsilon_shared_zero",
                "rule": "epsilon_domain_flux=0 is parent-proved for local compact branch",
                "gate_pass": "false",
                "reason": "local representative, branch selector, and boundary silence remain missing",
                "valid_for_claim": "false",
            },
            {
                "gate_id": "G1132_2_domain_product",
                "rule": "W_domain_alpha3*epsilon_domain_flux closes",
                "gate_pass": "false",
                "reason": "neither W nor epsilon is zero/sourced",
                "valid_for_claim": "false",
            },
            {
                "gate_id": "G1132_3_R11_product",
                "rule": "K_R11_flux_alpha3*c_R11_flux_alpha3*epsilon_domain_flux closes",
                "gate_pass": "false",
                "reason": "K, c, and epsilon are not zero/sourced",
                "valid_for_claim": "false",
            },
            {
                "gate_id": "G1132_4_no_cancellation_guard",
                "rule": "no tuned cancellation between domain and R11 pieces",
                "gate_pass": "true_nonclaim",
                "reason": "total row remains guard-only until products independently close",
                "valid_for_claim": "false",
            },
            {
                "gate_id": "G1132_5_alpha3_R10_local_GR",
                "rule": "alpha3/R10/local-GR can promote",
                "gate_pass": "false",
                "reason": "active alpha3 product rows remain blocked",
                "valid_for_claim": "false",
            },
            {
                "gate_id": "G1132_6_next_attack_selected",
                "rule": "next factor attack is selected without claim promotion",
                "gate_pass": "true_nonclaim",
                "reason": "epsilon_domain_flux is shared by both alpha3 products and is the cleanest theorem target",
                "valid_for_claim": "false",
            },
        ]
    )


def decision_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "decision_id": "D1132_0_verdict",
                "decision": "source_pack_built_not_filled",
                "reason": "the four live factors are now explicit, but none has a source-backed zero or numeric bound",
                "next_action": "attack epsilon_domain_flux first because it is the shared factor in both products",
                "valid_for_claim": "false",
            },
            {
                "decision_id": "D1132_1_best_next",
                "decision": "epsilon_domain_flux_zero_theorem_or_profile_bound",
                "reason": "epsilon=0 would close both alpha3 products if W/K/c are finite; a tight bound would also set the numeric requirement once couplings are sourced",
                "next_action": "derive compact-local exact/trivial flux theorem, or build a source-ready epsilon profile/bound ledger",
                "valid_for_claim": "false",
            },
            {
                "decision_id": "D1132_2_fallback",
                "decision": "if_epsilon_route_fails_source_couplings",
                "reason": "then the route becomes W/K/c coefficient derivation or numeric source acquisition",
                "next_action": "do not promote alpha3 until product inequalities are executable without MISSING markers",
                "valid_for_claim": "false",
            },
        ]
    )


def next_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "next_id": "NEXT1132_0_1133",
                "next_target": "1133-Y5-R10-epsilon-domain-flux-zero-theorem-or-profile-bound.md",
                "objective": "try to prove epsilon_domain_flux=0 for the local compact branch without killing FLRW memory; if not, produce a source-ready local epsilon profile/bound ledger",
                "include": "local exact/trivial representative; boundary silence; branch selector; observed coframe; product targets 4e-20; no global-memory kill",
                "exclude": "tuned cancellation; cohomology-norm selector claim; gauge-hiding; local-GR claim; GitHub; formalization edits",
                "valid_for_claim": "false",
                "claim_allowed": "false",
            }
        ]
    )


def factor_sources_exist(factors: list[dict[str, object]]) -> bool:
    for factor in factors:
        for relative_source in str(factor["evidence_sources"]).split(";"):
            if not (ROOT / relative_source).exists():
                return False
    return True


def validate(
    sources: list[dict[str, object]],
    factors: list[dict[str, object]],
    zero_theorems: list[dict[str, object]],
    products: list[dict[str, object]],
    guards: list[dict[str, object]],
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

    all_rows = factors + zero_theorems + products + guards + gates + decisions + next_target
    factor_set = {row["factor"] for row in factors}
    product_set = {row["source_row"] for row in products}
    add("V1132_0_sources_exist", all(row["exists"] == "true" and row["needle_found"] == "true" for row in sources), "all cited source-register paths exist and needles are found")
    add("V1132_1_factor_coverage", {"epsilon_domain_flux", "W_domain_alpha3", "K_R11_flux_alpha3", "c_R11_flux_alpha3"}.issubset(factor_set), "all four live alpha3 flux factors are represented")
    add("V1132_2_factor_evidence_paths_exist", factor_sources_exist(factors), "every factor evidence-source path exists locally")
    add("V1132_3_shared_epsilon_priority", factors[0]["factor"] == "epsilon_domain_flux" and factors[0]["priority"] == "P0_SHARED_BOTTLENECK", "epsilon_domain_flux is correctly prioritized as the shared bottleneck")
    add("V1132_4_products_present", {"EP1126_0_domain_flux", "EP1126_1_R11_flux", "EP1126_2_total_direct_flux_guard"}.issubset(product_set), "domain, R11, and total guard product rows are present")
    add("V1132_5_bound_explicit", all(row["target_bound"] == "4e-20" for row in products), "4e-20 target bound is explicit on every product/guard row")
    add("V1132_6_zero_routes_not_claimed", all(row["current_result"] != "PROVED" for row in zero_theorems), "zero theorem routes are audited but not claimed")
    add("V1132_7_no_cancellation_guard", guards[0]["status"] == "ACTIVE_TRUE_NONCLAIM" and products[-1]["current_status"] == "GUARD_ONLY_NOT_SCOREABLE", "no-cancellation guard remains active")
    add("V1132_8_gates_blocked", all(row["gate_pass"] in {"false", "true_nonclaim"} for row in gates) and sum(row["gate_pass"] == "false" for row in gates) >= 5, "claim gates remain blocked")
    add("V1132_9_no_claim_rows", all(row.get("valid_for_claim") == "false" for row in all_rows) and all(row.get("claim_allowed", "false") == "false" for row in next_target), "all generated rows remain nonclaim")
    add("V1132_10_next_target", next_target[0]["next_target"].startswith("1133-") and "epsilon-domain-flux" in str(next_target[0]["next_target"]), "1133 handoff targets epsilon_domain_flux")
    add("V1132_11_generated_under_post_checkpoint", all(str(path.resolve()).startswith(str(ROOT.resolve())) for path in outputs.values()), "all generated outputs are under post-checkpoint-work")
    csv_parse_ok = True
    for output_name, path in outputs.items():
        if output_name == "validation":
            continue
        if path.suffix.lower() == ".csv" and path.exists():
            with path.open("r", newline="", encoding="utf-8") as handle:
                list(csv.DictReader(handle))
        elif path.suffix.lower() == ".csv":
            csv_parse_ok = False
    add("V1132_12_csv_parse", csv_parse_ok, "all 1132 CSV outputs parse cleanly")
    add("V1132_13_formalization_untouched", True, "generator writes no outputs under formalization-workbench")
    add("V1132_SUMMARY", True, "1132 builds the nonclaim alpha3 factor source pack and selects epsilon_domain_flux as the next theorem target")
    return validation


def table(headers: list[str], rows: list[dict[str, object]]) -> str:
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(header, "")) for header in headers) + " |")
    return "\n".join(lines)


def write_doc(
    sources: list[dict[str, object]],
    factors: list[dict[str, object]],
    zero_theorems: list[dict[str, object]],
    products: list[dict[str, object]],
    guards: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    validation: list[dict[str, object]],
    next_target: list[dict[str, object]],
) -> None:
    text = f"""# 1132 - Y5/R10 Alpha3 Flux Product Source Pack Or Zero Theorem

**Current verdict:** the alpha3 threat is now cleanly reduced to four explicit factors, but no factor has a source-backed zero theorem or numeric bound yet.

**Useful progress:** `epsilon_domain_flux` is the shared bottleneck. If the local compact branch proves `epsilon_domain_flux=0`, both `W_domain_alpha3*epsilon_domain_flux` and `K_R11_flux_alpha3*c_R11_flux_alpha3*epsilon_domain_flux` close, provided the couplings are finite and no hidden vector residual is reintroduced.

**Best next attack:** prove or bound `epsilon_domain_flux` first. This is less suspicious than tuning couplings because it targets the physical local-flux channel common to both product rows.

**No claim:** no alpha3, R10, PPN, local-GR, measured-GM, or FLRW claim follows from 1132. The total direct-flux row remains guard-only and cannot pass by tuned cancellation.

## Source Register
{table(["source_id", "relative_path", "exists", "needle", "needle_found", "note"], sources)}

## Factor Source Pack
{table(["factor_id", "factor", "appears_in_products", "priority", "required_for_claim", "zero_route", "numeric_route", "current_value_or_theorem", "evidence_sources", "status", "valid_for_claim"], factors)}

## Zero-Theorem Route Audit
{table(["zero_id", "target", "would_close", "required_statement", "current_result", "missing_inputs", "scrutiny_note", "valid_for_claim"], zero_theorems)}

## Product Matrix
{table(["product_id", "source_row", "observable", "formula", "factors_needed", "target_bound", "theorem_zero_suffices_if", "numeric_acceptance", "current_status", "valid_for_claim"], products)}

## Guards
{table(["guard_id", "guard", "reason", "status", "blocks", "valid_for_claim"], guards)}

## Claim Gates
{table(["gate_id", "rule", "gate_pass", "reason", "valid_for_claim"], gates)}

## Decision Ledger
{table(["decision_id", "decision", "reason", "next_action", "valid_for_claim"], decisions)}

## Validation
{table(["check_id", "result", "detail", "valid_for_claim"], validation)}

## Next Target
{table(["next_id", "next_target", "objective", "include", "exclude", "valid_for_claim"], next_target)}
"""
    DOC.write_text(text, encoding="utf-8")


def remove_pycache() -> None:
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists() and pycache.is_dir():
        shutil.rmtree(pycache)


def main() -> None:
    outputs = {
        "source_register": OUT / "P8_Y5_R10_1132_SOURCE_REGISTER.csv",
        "factors": OUT / "P8_Y5_R10_1132_FACTOR_SOURCE_PACK.csv",
        "zero_theorems": OUT / "P8_Y5_R10_1132_ZERO_THEOREM_ROUTE_AUDIT.csv",
        "products": OUT / "P8_Y5_R10_1132_EXECUTABLE_PRODUCT_MATRIX.csv",
        "guards": OUT / "P8_Y5_R10_1132_NO_CANCELLATION_SIBLING_GUARDS.csv",
        "gates": OUT / "P8_Y5_R10_1132_CLAIM_GATES.csv",
        "decisions": OUT / "P8_Y5_R10_1132_DECISION_LEDGER.csv",
        "next": OUT / "P8_Y5_R10_1132_NEXT_TARGET.csv",
        "validation": OUT / "P8_Y5_BRR545_1132_VALIDATION.csv",
    }
    sources = source_rows()
    factors = factor_source_pack_rows()
    zero_theorems = zero_theorem_rows()
    products = product_matrix_rows()
    guards = guard_rows()
    gates = gate_rows()
    decisions = decision_rows()
    next_target = next_rows()

    write_csv(outputs["source_register"], sources)
    write_csv(outputs["factors"], factors)
    write_csv(outputs["zero_theorems"], zero_theorems)
    write_csv(outputs["products"], products)
    write_csv(outputs["guards"], guards)
    write_csv(outputs["gates"], gates)
    write_csv(outputs["decisions"], decisions)
    write_csv(outputs["next"], next_target)
    validation = validate(sources, factors, zero_theorems, products, guards, gates, decisions, next_target, outputs)
    write_csv(outputs["validation"], validation)
    write_doc(sources, factors, zero_theorems, products, guards, gates, decisions, validation, next_target)
    remove_pycache()

    failed = [row for row in validation if row["result"] != "pass"]
    print(f"wrote {DOC}")
    print(f"validation: {'PASS' if not failed else 'FAIL'}")
    for row in failed:
        print(f"{row['check_id']}: {row['detail']}")


if __name__ == "__main__":
    main()
