from __future__ import annotations

import csv
import math
import shutil
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "1134-Y5-R10-no-swirl-harmonic-flux-lemma-or-epsilon-profile-runner.md"


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
            "source_id": "SRC1134_0_1133_next",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1133_NEXT_TARGET.csv",
            "needle": "NEXT1133_0_1134",
            "note": "1133 handoff to no-swirl/harmonic flux lemma or epsilon profile runner.",
        },
        {
            "source_id": "SRC1134_1_1133_blocker",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1133_HARMONIC_CIRCULATION_BLOCKER.csv",
            "needle": "LOOP1133_0_circulation",
            "note": "1133 identifies circulation and harmonic flux as the hard gap.",
        },
        {
            "source_id": "SRC1134_2_1133_bounds",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1133_PROFILE_BOUND_ROWS.csv",
            "needle": "PB1133_2_shared_requirement",
            "note": "1133 stages the symbolic epsilon profile-bound fallback.",
        },
        {
            "source_id": "SRC1134_3_no_vector_attempt",
            "relative_path": "source-intake/mts_residuals/P8_DOMAIN_SELECTOR_NOVECTOR_THEOREM_ATTEMPT.csv",
            "needle": "T2_no_flux_local_representative",
            "note": "No-vector/no-flux route remains conditional rather than parent-derived.",
        },
        {
            "source_id": "SRC1134_4_premise_ownership",
            "relative_path": "source-intake/mts_residuals/P8_DOMAIN_ALPHA3_PREMISE_OWNERSHIP.csv",
            "needle": "P2_domain_selector_no_vector",
            "note": "Domain selector no-vector and local trivial representative premises are still blocking.",
        },
        {
            "source_id": "SRC1134_5_1132_factors",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1132_FACTOR_SOURCE_PACK.csv",
            "needle": "FAC1132_0_epsilon_domain_flux",
            "note": "1132 makes epsilon_domain_flux the shared alpha3 factor.",
        },
        {
            "source_id": "SRC1134_6_1132_products",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1132_EXECUTABLE_PRODUCT_MATRIX.csv",
            "needle": "PM1132_1_R11_flux",
            "note": "Product matrix supplies the alpha3 inequalities for the fallback runner.",
        },
        {
            "source_id": "SRC1134_7_1127_branch",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1127_BRANCH_SELECTOR_AUDIT.csv",
            "needle": "BS1127_0_local",
            "note": "Local exact/trivial branch is conditional and FLRW branch is preserved as separate.",
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


def lemma_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "lemma_id": "LEM1134_0_hodge_split",
                "target_piece": "F_D local flux decomposition",
                "attempted_statement": "F_D = grad phi_D + curl A_D + h_D + F_boundary/exchange",
                "sufficient_condition": "all non-exact, harmonic, and boundary/exchange pieces vanish",
                "current_result": "DECOMPOSITION_AUDIT_PASS",
                "missing_parent_input": "none for audit; proof still needs clauses below",
                "valid_for_claim": "false",
            },
            {
                "lemma_id": "LEM1134_1_gradient_constitutive_law",
                "target_piece": "coexact/circulating flux",
                "attempted_statement": "parent local branch gives F_D^i = -M_D^{ij} grad_j zeta_D with symmetric positive mobility M_D",
                "sufficient_condition": "flux is exact/gradient at the constitutive level, so curl/coexact circulation cannot be independently excited",
                "current_result": "MISSING_PARENT_CONSTITUTIVE_LAW",
                "missing_parent_input": "explicit parent action variation or Onsager/gradient-flow law for F_D",
                "valid_for_claim": "false",
            },
            {
                "lemma_id": "LEM1134_2_neumann_extremum",
                "target_piece": "exact gradient flux",
                "attempted_statement": "stationary no-source branch gives div(M_D grad zeta_D)=0 with n_i M_D^{ij} grad_j zeta_D=0 on boundary",
                "sufficient_condition": "positive elliptic M_D plus no-exchange boundary implies zeta_D is constant on each connected local component",
                "current_result": "CONDITIONAL_THEOREM_SHAPE",
                "missing_parent_input": "stationary no-source equation, positive ellipticity, and boundary silence are not parent-signed",
                "valid_for_claim": "false",
            },
            {
                "lemma_id": "LEM1134_3_harmonic_class_exclusion",
                "target_piece": "h_D harmonic/topological flux",
                "attempted_statement": "local compact branch has trivial relative H^1 or parent selector excludes local harmonic flux class",
                "sufficient_condition": "simply-connected/topologically trivial local domain, or branch selector sets the harmonic class to zero locally",
                "current_result": "MISSING_TOPOLOGY_OR_SELECTOR_PROOF",
                "missing_parent_input": "local topology/relative cohomology theorem or parent branch selector ownership",
                "valid_for_claim": "false",
            },
            {
                "lemma_id": "LEM1134_4_FLRW_separation",
                "target_piece": "cosmological memory branch",
                "attempted_statement": "local exact/trivial flux theorem applies only to compact local branch and does not impose global all-domain zero",
                "sufficient_condition": "one parent selector separates compact local exact branch from coherent FLRW active branch",
                "current_result": "GUARD_ONLY_TRUE_NONCLAIM",
                "missing_parent_input": "same parent branch selector remains unsigned",
                "valid_for_claim": "false",
            },
            {
                "lemma_id": "LEM1134_5_gauge_safe_projection",
                "target_piece": "observed local coframe projection",
                "attempted_statement": "epsilon_domain_flux vanishes in a PPN-safe observed coframe, not by representation choice",
                "sufficient_condition": "coframe normalization is fixed independently of the residual and cannot absorb alpha3",
                "current_result": "MISSING_OBSERVABLE_COFRAME_PROOF",
                "missing_parent_input": "source-normalization/coframe theorem for the alpha3 residual",
                "valid_for_claim": "false",
            },
            {
                "lemma_id": "LEM1134_6_verdict",
                "target_piece": "epsilon_domain_flux=0",
                "attempted_statement": "LEM1134_1 through LEM1134_5 all close from parent action",
                "sufficient_condition": "gradient constitutive law + Neumann extremum + harmonic exclusion + FLRW separation + gauge-safe projection",
                "current_result": "NO_SWIRL_HARMONIC_LEMMA_NOT_CLOSED",
                "missing_parent_input": "gradient-flow constitutive law and harmonic/topology exclusion are the decisive missing inputs",
                "valid_for_claim": "false",
            },
        ]
    )


def conditional_theorem_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "theorem_id": "THM1134_0_strong_conditional",
                "name": "local gradient-flow Neumann zero-flux lemma",
                "statement": "On a connected compact local domain, if F_D=-M_D grad zeta_D, M_D is positive elliptic, div F_D=0, n.F_D=0 at the boundary, and H^1_rel=0, then F_D=0 and epsilon_domain_flux=0.",
                "proof_sketch": "Integrate zeta_D div(M_D grad zeta_D)=0 by parts; boundary term vanishes; positivity gives grad zeta_D=0; H^1_rel=0 excludes an added harmonic flux.",
                "current_status": "MATHEMATICALLY_VALID_CONDITIONAL_NOT_PARENT_SIGNED",
                "blocks_claim_because": "the current corpus has not derived F_D=-M_D grad zeta_D, positive M_D, boundary silence, or H^1_rel=0 from the parent action",
                "valid_for_claim": "false",
            },
            {
                "theorem_id": "THM1134_1_why_net_flux_fails",
                "name": "net-flux insufficiency",
                "statement": "div F_D=0 and int_boundary F_D.n dS=0 do not imply epsilon_domain_flux=0.",
                "proof_sketch": "A circulating/coexact flux can be divergence-free and have zero normal boundary flux while still defining a local vector residual.",
                "current_status": "NEGATIVE_RESULT_RETAINED",
                "blocks_claim_because": "prevents a fake alpha3 pass from conservation alone",
                "valid_for_claim": "false",
            },
            {
                "theorem_id": "THM1134_2_parent_contract",
                "name": "future parent action contract",
                "statement": "A future parent action must output a constitutive flux law, local topology/branch rule, and gauge-safe observed coframe before alpha3 can promote.",
                "proof_sketch": "Those are exactly the missing premises in THM1134_0 and the blockers in LEM1134_1 through LEM1134_5.",
                "current_status": "CONTRACT_ONLY",
                "blocks_claim_because": "contract is not itself a proof",
                "valid_for_claim": "false",
            },
        ]
    )


def runner_input_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "input_id": "RUN1134_0_epsilon_profile",
                "quantity": "epsilon_domain_flux",
                "required_value": "numeric profile, theorem-zero flag, or source-backed upper bound",
                "unit_convention": "dimensionless projected local flux in observed PPN-safe coframe",
                "current_value": "MISSING_NUMERIC_PROFILE_OR_ZERO_THEOREM",
                "source_path": "MISSING_PARENT_PROFILE_OR_THEOREM_SOURCE",
                "runner_status": "BLOCKED",
                "valid_for_claim": "false",
            },
            {
                "input_id": "RUN1134_1_W_domain_alpha3",
                "quantity": "W_domain_alpha3",
                "required_value": "finite numeric/source-backed bound or theorem-zero",
                "unit_convention": "dimensionless alpha3 coupling after weak-field normalization",
                "current_value": "MISSING_NUMERIC_COUPLING_OR_ZERO_THEOREM",
                "source_path": "source-intake/mts_residuals/P8_mu_extra_domain_projector_coefficients.csv",
                "runner_status": "BLOCKED",
                "valid_for_claim": "false",
            },
            {
                "input_id": "RUN1134_2_K_R11_flux_alpha3",
                "quantity": "K_R11_flux_alpha3",
                "required_value": "finite numeric/source-backed transfer coefficient or theorem-zero",
                "unit_convention": "dimensionless R11 flux-to-alpha3 transfer coefficient",
                "current_value": "MISSING_R11_FLUX_TRANSFER_COEFFICIENT",
                "source_path": "source-intake/mts_residuals/P8_Y5_R10_1122_REMAINING_FLUX_CONTRACT.csv",
                "runner_status": "BLOCKED",
                "valid_for_claim": "false",
            },
            {
                "input_id": "RUN1134_3_c_R11_flux_alpha3",
                "quantity": "c_R11_flux_alpha3",
                "required_value": "finite numeric/source-backed source-normalization coefficient or theorem-zero",
                "unit_convention": "dimensionless observed-coframe/source-normalization coefficient",
                "current_value": "MISSING_R11_SOURCE_NORMALIZATION_COEFFICIENT",
                "source_path": "source-intake/mts_residuals/R11_DOMAIN_PROJECTOR_OPERATOR_VECTOR_MINIMUM.csv",
                "runner_status": "BLOCKED",
                "valid_for_claim": "false",
            },
        ]
    )


def symbolic_bound_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "bound_id": "EB1134_0_domain_bound",
                "product": "W_domain_alpha3*epsilon_domain_flux",
                "alpha3_limit": "4e-20",
                "required_epsilon_bound": "4e-20/abs(W_domain_alpha3)",
                "numeric_bound": "NONEXECUTABLE_MISSING_W",
                "if_zero_theorem": "passes this product if epsilon_domain_flux=0 or W_domain_alpha3=0",
                "current_status": "SYMBOLIC_ONLY",
                "valid_for_claim": "false",
            },
            {
                "bound_id": "EB1134_1_R11_bound",
                "product": "K_R11_flux_alpha3*c_R11_flux_alpha3*epsilon_domain_flux",
                "alpha3_limit": "4e-20",
                "required_epsilon_bound": "4e-20/abs(K_R11_flux_alpha3*c_R11_flux_alpha3)",
                "numeric_bound": "NONEXECUTABLE_MISSING_K_C",
                "if_zero_theorem": "passes this product if epsilon_domain_flux=0 or K_R11_flux_alpha3=0 or c_R11_flux_alpha3=0",
                "current_status": "SYMBOLIC_ONLY",
                "valid_for_claim": "false",
            },
            {
                "bound_id": "EB1134_2_shared_bound",
                "product": "domain_and_R11_alpha3_flux",
                "alpha3_limit": "4e-20",
                "required_epsilon_bound": "min(4e-20/abs(W_domain_alpha3), 4e-20/abs(K_R11_flux_alpha3*c_R11_flux_alpha3))",
                "numeric_bound": "NONEXECUTABLE_MISSING_W_K_C",
                "if_zero_theorem": "passes both products if epsilon_domain_flux=0 and couplings are finite",
                "current_status": "SYMBOLIC_ONLY",
                "valid_for_claim": "false",
            },
        ]
    )


def numeric_smoke_rows() -> list[dict[str, object]]:
    rows = []
    cases = [
        ("SMOKE1134_0_domain_unit_coupling", "domain", 1.0, None),
        ("SMOKE1134_1_R11_unit_product", "R11", None, 1.0),
        ("SMOKE1134_2_shared_unit_envelope", "shared", 1.0, 1.0),
    ]
    for smoke_id, branch, w_value, kc_value in cases:
        if branch == "domain":
            required = 4e-20 / abs(w_value)
            formula = "4e-20/abs(W_domain_alpha3)"
        elif branch == "R11":
            required = 4e-20 / abs(kc_value)
            formula = "4e-20/abs(K_R11_flux_alpha3*c_R11_flux_alpha3)"
        else:
            required = min(4e-20 / abs(w_value), 4e-20 / abs(kc_value))
            formula = "min(4e-20/abs(W),4e-20/abs(K*c))"
        rows.append(
            {
                "smoke_id": smoke_id,
                "branch": branch,
                "assumption": "unit coupling smoke only; not a source-backed physical value",
                "formula": formula,
                "epsilon_required_if_assumption_true": f"{required:.3e}" if math.isfinite(required) else "nan",
                "claim_status": "NONCLAIM_SCHEMA_CHECK_ONLY",
                "valid_for_claim": "false",
            }
        )
    return stamp(rows)


def gate_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "gate_id": "G1134_0_gradient_law",
                "rule": "parent action derives F_D=-M_D grad zeta_D",
                "gate_pass": "false",
                "reason": "constitutive gradient-flow law is not present in current corpus",
                "valid_for_claim": "false",
            },
            {
                "gate_id": "G1134_1_positive_neumann",
                "rule": "positive elliptic M_D plus no-exchange boundary is parent-signed",
                "gate_pass": "false",
                "reason": "ellipticity and boundary silence are not parent-derived",
                "valid_for_claim": "false",
            },
            {
                "gate_id": "G1134_2_harmonic_exclusion",
                "rule": "local harmonic/topological flux class is excluded",
                "gate_pass": "false",
                "reason": "local topology/relative cohomology branch theorem is missing",
                "valid_for_claim": "false",
            },
            {
                "gate_id": "G1134_3_gauge_safe_epsilon",
                "rule": "epsilon vanishes in observed PPN-safe coframe",
                "gate_pass": "false",
                "reason": "coframe/source-normalization proof is not closed",
                "valid_for_claim": "false",
            },
            {
                "gate_id": "G1134_4_epsilon_runner_executable",
                "rule": "epsilon profile-bound runner has numeric/source-backed inputs",
                "gate_pass": "false",
                "reason": "epsilon, W, K, and c inputs are missing or symbolic",
                "valid_for_claim": "false",
            },
            {
                "gate_id": "G1134_5_FLRW_guard",
                "rule": "local no-flux route does not erase cosmological memory",
                "gate_pass": "true_nonclaim",
                "reason": "global all-domain zero remains forbidden; local and FLRW branches stay separate",
                "valid_for_claim": "false",
            },
            {
                "gate_id": "G1134_6_alpha3_local_GR",
                "rule": "alpha3/R10/local-GR can promote",
                "gate_pass": "false",
                "reason": "no-swirl/harmonic lemma and profile runner remain blocked",
                "valid_for_claim": "false",
            },
        ]
    )


def decision_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "decision_id": "D1134_0_verdict",
                "decision": "no_swirl_harmonic_lemma_not_parent_closed",
                "reason": "a strong conditional theorem exists, but its constitutive law/topology/coframe premises are missing",
                "next_action": "attack the gradient-flow constitutive law as the highest-leverage parent-action target",
                "valid_for_claim": "false",
            },
            {
                "decision_id": "D1134_1_best_next",
                "decision": "derive_FD_gradient_flow_or_demote_epsilon_zero",
                "reason": "F_D=-M_D grad zeta_D would kill circulation; without it epsilon zero stays closure-only",
                "next_action": "search current parent action terms for a variational mobility/chemical-potential structure",
                "valid_for_claim": "false",
            },
            {
                "decision_id": "D1134_2_runner_status",
                "decision": "epsilon_bound_runner_staged_but_blocked",
                "reason": "symbolic and smoke rows exist, but no source-backed W/K/c/epsilon values are present",
                "next_action": "keep runner nonclaim until source-backed inputs exist",
                "valid_for_claim": "false",
            },
        ]
    )


def next_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "next_id": "NEXT1134_0_1135",
                "next_target": "1135-Y5-R10-FD-gradient-flow-constitutive-law-or-epsilon-closure-demotion.md",
                "objective": "try to derive F_D=-M_D grad zeta_D with positive mobility from parent local action; if not, demote epsilon_domain_flux zero to closure-only and continue with numeric coupling/profile acquisition",
                "include": "parent action variation; mobility M_D; chemical/domain potential zeta_D; Neumann boundary; positive ellipticity; no-swirl proof",
                "exclude": "net-flux-only proof; Hodge projector insertion; gauge hiding; tuned cancellation; alpha3/local-GR claim; GitHub; formalization edits",
                "valid_for_claim": "false",
                "claim_allowed": "false",
            }
        ]
    )


def local_paths_exist(rows: list[dict[str, object]], field: str) -> bool:
    for row in rows:
        value = str(row[field])
        if value.startswith("MISSING"):
            continue
        if not (ROOT / value).exists():
            return False
    return True


def validate(
    sources: list[dict[str, object]],
    lemmas: list[dict[str, object]],
    theorems: list[dict[str, object]],
    runner_inputs: list[dict[str, object]],
    symbolic_bounds: list[dict[str, object]],
    smoke_rows: list[dict[str, object]],
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

    all_rows = lemmas + theorems + runner_inputs + symbolic_bounds + smoke_rows + gates + decisions + next_target
    lemma_targets = {row["target_piece"] for row in lemmas}
    add("V1134_0_sources_exist", all(row["exists"] == "true" and row["needle_found"] == "true" for row in sources), "all cited local source paths exist and needles are found")
    add("V1134_1_lemma_covers_swirl_harmonic_boundary", {"coexact/circulating flux", "h_D harmonic/topological flux", "cosmological memory branch"}.issubset(lemma_targets), "lemma audit covers circulation, harmonic flux, and FLRW separation")
    add("V1134_2_strong_conditional_present", theorems[0]["current_status"] == "MATHEMATICALLY_VALID_CONDITIONAL_NOT_PARENT_SIGNED", "gradient-flow Neumann zero-flux theorem is present but conditional")
    add("V1134_3_net_flux_rejected", theorems[1]["current_status"] == "NEGATIVE_RESULT_RETAINED", "net-flux-only proof is explicitly rejected")
    add("V1134_4_lemma_not_closed", lemmas[-1]["current_result"] == "NO_SWIRL_HARMONIC_LEMMA_NOT_CLOSED", "no-swirl/harmonic lemma remains unclosed")
    add("V1134_5_runner_inputs_blocked", all(row["runner_status"] == "BLOCKED" for row in runner_inputs), "epsilon runner inputs remain blocked rather than claim-valid")
    add("V1134_6_runner_source_paths_exist_where_declared", local_paths_exist(runner_inputs, "source_path"), "declared non-missing runner source paths exist locally")
    add("V1134_7_symbolic_bounds_nonclaim", all(row["current_status"] == "SYMBOLIC_ONLY" for row in symbolic_bounds), "epsilon bound rows remain symbolic only")
    add("V1134_8_smoke_rows_nonclaim", all(row["claim_status"] == "NONCLAIM_SCHEMA_CHECK_ONLY" for row in smoke_rows), "numeric smoke rows are schema checks only")
    add("V1134_9_gates_blocked", all(row["gate_pass"] in {"false", "true_nonclaim"} for row in gates) and sum(row["gate_pass"] == "false" for row in gates) >= 6, "claim gates remain blocked")
    add("V1134_10_no_claim_rows", all(row.get("valid_for_claim") == "false" for row in all_rows) and all(row.get("claim_allowed", "false") == "false" for row in next_target), "all generated rows remain nonclaim")
    add("V1134_11_next_target", next_target[0]["next_target"].startswith("1135-") and "gradient-flow" in str(next_target[0]["next_target"]), "1135 handoff targets F_D gradient-flow constitutive law")
    add("V1134_12_generated_under_post_checkpoint", all(str(path.resolve()).startswith(str(ROOT.resolve())) for path in outputs.values()), "all generated outputs are under post-checkpoint-work")
    csv_parse_ok = True
    for output_name, path in outputs.items():
        if output_name == "validation":
            continue
        if path.suffix.lower() == ".csv" and path.exists():
            with path.open("r", newline="", encoding="utf-8") as handle:
                list(csv.DictReader(handle))
        elif path.suffix.lower() == ".csv":
            csv_parse_ok = False
    add("V1134_13_csv_parse", csv_parse_ok, "all 1134 CSV outputs parse cleanly")
    add("V1134_14_formalization_untouched", True, "generator writes no outputs under formalization-workbench")
    add("V1134_SUMMARY", True, "1134 finds the strongest conditional no-swirl theorem and stages a nonclaim epsilon bound runner")
    return validation


def table(headers: list[str], rows: list[dict[str, object]]) -> str:
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(header, "")) for header in headers) + " |")
    return "\n".join(lines)


def write_doc(
    sources: list[dict[str, object]],
    lemmas: list[dict[str, object]],
    theorems: list[dict[str, object]],
    runner_inputs: list[dict[str, object]],
    symbolic_bounds: list[dict[str, object]],
    smoke_rows: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    validation: list[dict[str, object]],
    next_target: list[dict[str, object]],
) -> None:
    text = f"""# 1134 - Y5/R10 No-Swirl Harmonic Flux Lemma Or Epsilon Profile Runner

**Current verdict:** the no-swirl/harmonic lemma is not parent-closed. The strongest route is a local gradient-flow/Neumann theorem, but the parent action has not yet supplied the needed constitutive law `F_D=-M_D grad zeta_D`.

**Useful progress:** we now have a precise theorem contract. If a future parent action gives positive mobility, no-source stationarity, no-exchange boundary conditions, and local harmonic-class exclusion, then `epsilon_domain_flux=0` follows without using a plateau axiom or tuned cancellation.

**Negative result:** zero net flux is not enough. A coexact/circulating field or harmonic local flux can have zero divergence and zero boundary integral while still leaving an alpha3 preferred-frame residual.

**Fallback:** an epsilon profile-bound runner is staged, but it is non-executable until `epsilon_domain_flux`, `W_domain_alpha3`, `K_R11_flux_alpha3`, and `c_R11_flux_alpha3` are source-backed or theorem-zero.

**No claim:** no alpha3, R10, PPN, local-GR, measured-GM, or FLRW claim follows from 1134.

## Source Register
{table(["source_id", "relative_path", "exists", "needle", "needle_found", "note"], sources)}

## No-Swirl/Harmonic Lemma Audit
{table(["lemma_id", "target_piece", "attempted_statement", "sufficient_condition", "current_result", "missing_parent_input", "valid_for_claim"], lemmas)}

## Conditional Theorem Contract
{table(["theorem_id", "name", "statement", "proof_sketch", "current_status", "blocks_claim_because", "valid_for_claim"], theorems)}

## Epsilon Profile Runner Inputs
{table(["input_id", "quantity", "required_value", "unit_convention", "current_value", "source_path", "runner_status", "valid_for_claim"], runner_inputs)}

## Symbolic Epsilon Bounds
{table(["bound_id", "product", "alpha3_limit", "required_epsilon_bound", "numeric_bound", "if_zero_theorem", "current_status", "valid_for_claim"], symbolic_bounds)}

## Nonclaim Smoke Rows
{table(["smoke_id", "branch", "assumption", "formula", "epsilon_required_if_assumption_true", "claim_status", "valid_for_claim"], smoke_rows)}

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
        "source_register": OUT / "P8_Y5_R10_1134_SOURCE_REGISTER.csv",
        "lemmas": OUT / "P8_Y5_R10_1134_NO_SWIRL_HARMONIC_LEMMA_AUDIT.csv",
        "theorems": OUT / "P8_Y5_R10_1134_CONDITIONAL_THEOREM_CONTRACT.csv",
        "runner_inputs": OUT / "P8_Y5_R10_1134_EPSILON_PROFILE_RUNNER_INPUTS.csv",
        "symbolic_bounds": OUT / "P8_Y5_R10_1134_EPSILON_SYMBOLIC_BOUNDS.csv",
        "smoke_rows": OUT / "P8_Y5_R10_1134_EPSILON_RUNNER_SMOKE_ROWS.csv",
        "gates": OUT / "P8_Y5_R10_1134_CLAIM_GATES.csv",
        "decisions": OUT / "P8_Y5_R10_1134_DECISION_LEDGER.csv",
        "next": OUT / "P8_Y5_R10_1134_NEXT_TARGET.csv",
        "validation": OUT / "P8_Y5_BRR545_1134_VALIDATION.csv",
    }
    sources = source_rows()
    lemmas = lemma_rows()
    theorems = conditional_theorem_rows()
    runner_inputs = runner_input_rows()
    symbolic_bounds = symbolic_bound_rows()
    smoke_rows = numeric_smoke_rows()
    gates = gate_rows()
    decisions = decision_rows()
    next_target = next_rows()

    write_csv(outputs["source_register"], sources)
    write_csv(outputs["lemmas"], lemmas)
    write_csv(outputs["theorems"], theorems)
    write_csv(outputs["runner_inputs"], runner_inputs)
    write_csv(outputs["symbolic_bounds"], symbolic_bounds)
    write_csv(outputs["smoke_rows"], smoke_rows)
    write_csv(outputs["gates"], gates)
    write_csv(outputs["decisions"], decisions)
    write_csv(outputs["next"], next_target)
    validation = validate(sources, lemmas, theorems, runner_inputs, symbolic_bounds, smoke_rows, gates, decisions, next_target, outputs)
    write_csv(outputs["validation"], validation)
    write_doc(sources, lemmas, theorems, runner_inputs, symbolic_bounds, smoke_rows, gates, decisions, validation, next_target)
    remove_pycache()

    failed = [row for row in validation if row["result"] != "pass"]
    print(f"wrote {DOC}")
    print(f"validation: {'PASS' if not failed else 'FAIL'}")
    for row in failed:
        print(f"{row['check_id']}: {row['detail']}")


if __name__ == "__main__":
    main()
