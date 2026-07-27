from __future__ import annotations

import csv
import math
import subprocess
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "962-Y5-R10-R2-fR-zero-clause-proof-or-scalar-mode-bound-source-acquisition.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
SCRIPT_START_UTC = datetime.now(timezone.utc)
HBAR_C_EV_M = 1.973269804e-7


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def flag(value: bool) -> str:
    return "true" if value else "false"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


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


def source_path(relative_path: str) -> Path:
    return ROOT / relative_path


def formalization_changed_after_start() -> int:
    if not FORMALIZATION.exists():
        return -1
    since = SCRIPT_START_UTC.astimezone().strftime("%Y-%m-%dT%H:%M:%S")
    literal = str(FORMALIZATION).replace("'", "''")
    command = (
        "$since=[datetime]::Parse('"
        + since
        + "'); "
        + "$count=(Get-ChildItem -LiteralPath '"
        + literal
        + "' -Recurse -File | Where-Object { $_.LastWriteTime -gt $since } | Measure-Object).Count; "
        + "Write-Output $count"
    )
    completed = subprocess.run(
        ["powershell", "-NoProfile", "-Command", command],
        capture_output=True,
        text=True,
        timeout=20,
        check=False,
    )
    try:
        return int(completed.stdout.strip().splitlines()[-1])
    except (IndexError, ValueError):
        return -2


def lambda_um_to_mass_ev(lambda_um: float) -> float:
    return HBAR_C_EV_M / (lambda_um * 1e-6)


def source_register() -> list[dict[str, str]]:
    local_specs = [
        {
            "source_id": "961_doc",
            "source_type": "local",
            "path_or_url": "961-Y5-R10-priority-operator-parent-zero-clauses-or-bound-source-acquisition.md",
            "role": "handoff: R2/fR zero clause and scalar source rows",
            "needle": "PZ961_R2FR_0_operator_exclusion",
        },
        {
            "source_id": "961_zero_clauses",
            "source_type": "local",
            "path_or_url": "source-intake/mts_residuals/P8_Y5_R10_961_PARENT_ZERO_CLAUSES.csv",
            "role": "parent zero-clause input table",
            "needle": "PZ961_R2FR_1_trace_scalar_absence",
        },
        {
            "source_id": "961_bound_ledger",
            "source_type": "local",
            "path_or_url": "source-intake/mts_residuals/P8_Y5_R10_961_BOUND_SOURCE_ACQUISITION_LEDGER.csv",
            "role": "scalar bound source acquisition inputs",
            "needle": "BS961_R2FR_0_full_curve_Lee2020",
        },
        {
            "source_id": "960_doc",
            "source_type": "local",
            "path_or_url": "960-Y5-R10-R2-fR-scalar-mode-zero-or-bound-and-torsion-Levi-Civita-gate.md",
            "role": "R2/fR scalar-mode filter result",
            "needle": "R2/fR: filter works",
        },
        {
            "source_id": "959_doc",
            "source_type": "local",
            "path_or_url": "959-Y5-R10-local-second-order-metric-only-no-extra-field-clause-or-R11-priority-fill.md",
            "role": "local second-order metric-only no-extra-field clause",
            "needle": "no-extra-field theorem: not signed",
        },
        {
            "source_id": "506_doc",
            "source_type": "local",
            "path_or_url": "506-local-EH-reduction-and-extra-sector-silence-theorem.md",
            "role": "operator filter: zero/topological/redundant/bounded residual",
            "needle": "Curvature/operator terms beyond EH must be zero",
        },
        {
            "source_id": "R11_executable",
            "source_type": "local",
            "path_or_url": "source-intake/mts_residuals/R11_nonEH_operator_vector_executable.csv",
            "role": "R11 scalar-mode row requiring zero or bounds",
            "needle": "R2_fR_scalar_mode",
        },
        {
            "source_id": "700_EH_algebra",
            "source_type": "local",
            "path_or_url": "source-intake/mts_residuals/P8_Y5_R10_700_EH_POISSON_ALGEBRA_CERTIFICATE.csv",
            "role": "EH-to-Poisson coefficient conditional algebra",
            "needle": "ALG700_4_poisson_coefficient",
        },
    ]
    web_specs = [
        {
            "source_id": "ext_DeFeliceTsujikawa2010_fR",
            "source_type": "web",
            "path_or_url": "https://arxiv.org/abs/1002.4928",
            "role": "f(R) scalar degree, local-gravity constraints, scalar-tensor mapping review",
            "needle": "f(R) theories",
        },
        {
            "source_id": "ext_Lee2020_R10",
            "source_type": "web",
            "path_or_url": "https://arxiv.org/abs/2002.11761",
            "role": "modern Eot-Wash R10 source candidate",
            "needle": "New Test of the Gravitational 1/r^2 Law at Separations down to 52",
        },
        {
            "source_id": "ext_Kapner2007_R10",
            "source_type": "web",
            "path_or_url": "https://arxiv.org/abs/hep-ph/0611184",
            "role": "older Eot-Wash R10 anchor",
            "needle": "lambda = 56",
        },
        {
            "source_id": "ext_Will2014_PPN",
            "source_type": "web",
            "path_or_url": "https://arxiv.org/abs/1403.7377",
            "role": "PPN and solar-system test review",
            "needle": "The Confrontation between General Relativity and Experiment",
        },
        {
            "source_id": "ext_Cassini2003_gamma",
            "source_type": "web",
            "path_or_url": "https://pubmed.ncbi.nlm.nih.gov/14508481/",
            "role": "Cassini gamma anchor source",
            "needle": "gamma = 1 + (2.1 +/- 2.3) x 10(-5)",
        },
    ]
    rows = []
    for spec in local_specs:
        path = source_path(spec["path_or_url"])
        exists = path.exists()
        needle_found = exists and spec["needle"] in read_text(path)
        rows.append(
            {
                **spec,
                "absolute_path": str(path),
                "exists_or_recorded": flag(exists),
                "needle_or_url_recorded": flag(needle_found),
                "extraction_status": "local_needle_checked",
                "valid_for_claim": "false",
                "generated_utc": stamp(),
            }
        )
    for spec in web_specs:
        recorded = spec["path_or_url"].startswith("https://")
        rows.append(
            {
                **spec,
                "absolute_path": "",
                "exists_or_recorded": flag(recorded),
                "needle_or_url_recorded": flag(recorded),
                "extraction_status": "web_source_string_recorded_not_numeric_claim",
                "valid_for_claim": "false",
                "generated_utc": stamp(),
            }
        )
    return rows


def r2_fr_zero_proof_attempt() -> list[dict[str, str]]:
    rows = [
        {
            "step_id": "R2Z962_0_target",
            "claim_attempted": "derive c_R2=c_fR=0",
            "mathematical_step": "Let the local metric-only curvature sector contain L=sqrt(-g) f(R) with f(R)=a0+a1 R+a2 R^2+O(R^3).",
            "test": "Does the parent local exterior branch permit a nonlinear f(R) scalar tower?",
            "result": "setup",
            "would_close_if": "a2=0 and all higher f^(n>=2)(R0)=0 by parent theorem",
            "blocking_input": "parent has not yet signed exact local second-order metric-only dynamics",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "step_id": "R2Z962_1_variation_filter",
            "claim_attempted": "nonlinear f(R) violates second-order metric equation",
            "mathematical_step": "Metric variation gives f_R R_mn - (1/2) f g_mn + (g_mn Box - nabla_m nabla_n) f_R = kappa T_mn.",
            "test": "If f_R depends on R, the last term contains derivatives of R and therefore higher derivatives of g.",
            "result": "relative_theorem_step_pass",
            "would_close_if": "f_R is constant on the tested branch for arbitrary local perturbations",
            "blocking_input": "constant f_R for arbitrary branch is equivalent to f_RR=0 locally, not yet parent-signed",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "step_id": "R2Z962_2_trace_scalar_pole",
            "claim_attempted": "nonlinear f(R) carries scalar trace mode",
            "mathematical_step": "Trace gives 3 Box f_R + f_R R - 2 f = kappa T; for R+a R^2 around flat space, (Box - 1/(6a)) delta R = -kappa T/(6a).",
            "test": "A finite nonzero a produces a finite-mass scalaron/Yukawa branch.",
            "result": "relative_theorem_step_pass",
            "would_close_if": "a=0, m_s->infinity, or scalar pole is proved gauge/topological/redundant",
            "blocking_input": "no parent proof that a=0 and no sourced scalaron mass/coupling row",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "step_id": "R2Z962_3_topological_escape",
            "claim_attempted": "R2/fR is harmless topological curvature",
            "mathematical_step": "In 4D the Gauss-Bonnet combination is topological, but isolated R^2 or generic f(R) is not the Gauss-Bonnet density.",
            "test": "Can the current R2/fR row be reclassified as pure topological zero-variation?",
            "result": "escape_fails_current_row",
            "would_close_if": "parent supplies exact GB combination with zero boundary/local flux or a topological certificate",
            "blocking_input": "current operator row is scalar R2/fR, not sourced GB/topological combination",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "step_id": "R2Z962_4_field_redefinition_escape",
            "claim_attempted": "R2/fR is removable without observables",
            "mathematical_step": "A field redefinition can reshuffle perturbative curvature-squared terms, but it must not move leakage into matter couplings, source normalization, clocks, or PPN readout.",
            "test": "Can this checkpoint certify field-redefinition redundancy for MTS observables?",
            "result": "escape_not_certified",
            "would_close_if": "source/readout equivalence and boundary terms are explicitly invariant under the redefinition",
            "blocking_input": "no invariant observable/readout certificate for the redefinition",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "step_id": "R2Z962_5_relative_zero_theorem",
            "claim_attempted": "conditional proof of c_R2=c_fR=0",
            "mathematical_step": "If the parent local exterior action is exactly 4D, local, diffeo-invariant, metric-only, second-order in equations for arbitrary compact exterior perturbations, and no extra scalar field is retained, then f_RR=0 on the branch and the R2/fR scalar-mode coefficient is zero.",
            "test": "Does the theorem close as a relative implication?",
            "result": "RELATIVE_THEOREM_PROVEN_PARENT_PREMISE_UNSIGNED",
            "would_close_if": "parent signs exact second-order/no-extra-scalar premise",
            "blocking_input": "absolute MTS proof still needs parent operator-selection signature",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]
    return rows


def trace_scalar_pole_test() -> list[dict[str, str]]:
    lambda_lee = 38.6
    lambda_kapner = 56.0
    return [
        {
            "test_id": "SP962_0_metric_fR_map",
            "model_branch": "metric_fR_unscreened_linear",
            "input_assumption": "f(R)=R+aR^2 locally; matter couples to g_obs; no screening/chameleon suppression supplied",
            "derived_quantity": "scalaron_mass_squared",
            "formula": "m_s^2=1/(6a) for flat-background R+aR^2 normalization; general f(R) uses m_s^2=(f_R-R f_RR)/(3 f_RR)",
            "numeric_value": "MISSING_a_OR_fRR",
            "units": "inverse_length_squared_or_eV_squared_after_hbar_c",
            "status": "formula_ready_parent_input_missing",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "test_id": "SP962_1_yukawa_map",
            "model_branch": "metric_fR_unscreened_linear",
            "input_assumption": "no screening and one scalar pole survives",
            "derived_quantity": "Yukawa_potential_shape",
            "formula": "Phi(r)=-G M/r [1 + alpha_s exp(-r/lambda_s)] with alpha_s often 1/3 in the simplest unscreened metric f(R) scalar limit",
            "numeric_value": "alpha_s=1/3_if_unscreened_simple_metric_fR",
            "units": "dimensionless_alpha; lambda_s=1/m_s",
            "status": "map_ready_but_screening_and_parent_normalization_missing",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "test_id": "SP962_2_Lee2020_anchor_mass",
            "model_branch": "R10_anchor_conversion",
            "input_assumption": "Lee2020 gravitational-strength anchor lambda=38.6 micrometer is used only as anchor, not full curve",
            "derived_quantity": "mass_eV_from_lambda",
            "formula": "m_eV=(hbar c)/lambda",
            "numeric_value": f"{lambda_um_to_mass_ev(lambda_lee):.6g}",
            "units": "eV",
            "status": "positive_conversion_nonclaim",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "test_id": "SP962_3_Kapner2007_anchor_mass",
            "model_branch": "R10_anchor_conversion",
            "input_assumption": "Kapner2007 alpha<=1 at lambda=56 micrometer is used only as older continuity anchor",
            "derived_quantity": "mass_eV_from_lambda",
            "formula": "m_eV=(hbar c)/lambda",
            "numeric_value": f"{lambda_um_to_mass_ev(lambda_kapner):.6g}",
            "units": "eV",
            "status": "positive_conversion_nonclaim",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "test_id": "SP962_4_claim_screen",
            "model_branch": "MTS_R2FR_scalar_mode",
            "input_assumption": "MTS parent coefficient not supplied",
            "derived_quantity": "claim_readiness",
            "formula": "claim_allowed only if zero theorem is parent-signed OR c_R2/c_fR, units, m_s, alpha_s(lambda), screening status, and bound curve are all sourced",
            "numeric_value": "false",
            "units": "boolean",
            "status": "claim_blocked",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def scalar_bound_fallback_rows() -> list[dict[str, str]]:
    return [
        {
            "bound_id": "R2B962_0_parent_zero_route",
            "operator_family": "R2_fR_scalar_mode",
            "route": "derived_zero_if_parent_second_order_signed",
            "source_url": "local:962_relative_zero_theorem",
            "required_parent_inputs": "parent exact local second-order metric-only no-extra-scalar action signature",
            "alpha_value": "0_if_signed_else_MISSING",
            "lambda_value_um": "not_applicable_if_zero",
            "mass_eV": "infinite_if_zero_signed",
            "extraction_method": "theorem_zero_candidate",
            "status": "relative_theorem_ready_absolute_parent_signature_missing",
            "ready_for_runner": "false",
            "valid_for_claim": "false",
            "reason_blocked": "parent premise unsigned",
            "generated_utc": stamp(),
        },
        {
            "bound_id": "R2B962_1_fR_unscreened_map",
            "operator_family": "R2_fR_scalar_mode",
            "route": "finite_scalar_mode_formula",
            "source_url": "https://arxiv.org/abs/1002.4928",
            "required_parent_inputs": "c_R2_or_fRR; normalization; screening flag; source coupling",
            "alpha_value": "1/3_if_simple_unscreened_metric_fR",
            "lambda_value_um": "MISSING_FROM_PARENT_SCALAR_MASS",
            "mass_eV": "MISSING_FROM_PARENT_SCALAR_MASS",
            "extraction_method": "formula_map_not_bound",
            "status": "formula_ready_missing_parent_input",
            "ready_for_runner": "false",
            "valid_for_claim": "false",
            "reason_blocked": "no MTS scalar mass/coupling supplied",
            "generated_utc": stamp(),
        },
        {
            "bound_id": "R2B962_2_Lee2020_anchor",
            "operator_family": "R2_fR_scalar_mode",
            "route": "R10_anchor_only",
            "source_url": "https://arxiv.org/abs/2002.11761",
            "required_parent_inputs": "full alpha(lambda) curve plus MTS alpha/lambda prediction",
            "alpha_value": "1_anchor_only",
            "lambda_value_um": "38.6",
            "mass_eV": f"{lambda_um_to_mass_ev(38.6):.6g}",
            "extraction_method": "anchor_only_non_curve",
            "status": "source_backed_anchor_not_claim_curve",
            "ready_for_runner": "false",
            "valid_for_claim": "false",
            "reason_blocked": "no full curve and alpha=1 anchor does not score alpha=1/3 without interpolation",
            "generated_utc": stamp(),
        },
        {
            "bound_id": "R2B962_3_Kapner2007_anchor",
            "operator_family": "R2_fR_scalar_mode",
            "route": "older_R10_anchor_only",
            "source_url": "https://arxiv.org/abs/hep-ph/0611184",
            "required_parent_inputs": "same as R2B962_2",
            "alpha_value": "abs(alpha)<=1_anchor",
            "lambda_value_um": "56",
            "mass_eV": f"{lambda_um_to_mass_ev(56.0):.6g}",
            "extraction_method": "anchor_only_non_curve",
            "status": "source_backed_anchor_not_claim_curve",
            "ready_for_runner": "false",
            "valid_for_claim": "false",
            "reason_blocked": "older anchor is regression/sanity evidence only",
            "generated_utc": stamp(),
        },
        {
            "bound_id": "R2B962_4_Cassini_gamma_anchor",
            "operator_family": "R2_fR_scalar_mode",
            "route": "PPN_gamma_anchor",
            "source_url": "https://pubmed.ncbi.nlm.nih.gov/14508481/",
            "required_parent_inputs": "gamma(alpha_s,m_s,screening,solar-system regime) map",
            "alpha_value": "not_Yukawa_alpha",
            "lambda_value_um": "solar_system_regime",
            "mass_eV": "MISSING_REGIME_MAP",
            "extraction_method": "PPN_anchor_not_scalar_runner_row",
            "status": "source_identified_anchor_not_mapped",
            "ready_for_runner": "false",
            "valid_for_claim": "false",
            "reason_blocked": "no MTS scalar-mode PPN projection",
            "generated_utc": stamp(),
        },
    ]


def claim_gates() -> list[dict[str, str]]:
    return [
        {
            "gate_id": "CGATE962_0_relative_theorem",
            "claim": "R2/fR must vanish if parent local branch is exact second-order metric-only with no scalar",
            "required_condition": "mathematical implication established",
            "current_evidence": "variation and trace-pole filter establish the relative implication",
            "gate_pass": "true",
            "claim_allowed": "conditional_only",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CGATE962_1_absolute_MTS_zero",
            "claim": "MTS parent sets c_R2=c_fR=0",
            "required_condition": "parent signs exact second-order/no-extra-scalar action signature or equivalent zero coefficient",
            "current_evidence": "parent premise remains unsigned",
            "gate_pass": "false",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CGATE962_2_scalar_bound_runner",
            "claim": "finite R2/fR scalar mode passes R10/PPN bounds",
            "required_condition": "numeric MTS c_R2/fRR, mass, coupling/screening, full bound curve or mapped PPN bound",
            "current_evidence": "formula and anchor rows only; full curve and parent numeric inputs missing",
            "gate_pass": "false",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CGATE962_3_EH_local_GR",
            "claim": "EH/local-GR branch can promote",
            "required_condition": "R2/fR zero plus connection/torsion gate plus source normalization/GM gates",
            "current_evidence": "R2/fR relative theorem helps but absolute gate and connection gate remain open",
            "gate_pass": "false",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def decisions() -> list[dict[str, str]]:
    return [
        {
            "decision_id": "DEC962_0_R2FR_result",
            "topic": "R2/fR zero proof",
            "result": "relative_theorem_proven_absolute_parent_signature_missing",
            "reason": "nonlinear f(R) generically introduces higher metric derivatives/scalar trace pole, so exact second-order metric-only parent dynamics kills it",
            "next_action": "prove the parent exact second-order/no-extra-scalar signature, not just the R2/fR filter",
            "claim_allowed": "conditional_only",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC962_1_bound_route",
            "topic": "scalar-mode empirical fallback",
            "result": "formula_and_anchor_rows_ready_nonclaim",
            "reason": "De Felice/Tsujikawa map plus Eot-Wash/Cassini anchors define the right plumbing but parent coefficient and full curve are missing",
            "next_action": "do not digitize full R10 curve until parent leaves finite scalar mode alive or user asks for empirical plumbing first",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC962_2_best_next_target",
            "topic": "next derivation hinge",
            "result": "attack_parent_second_order_signature",
            "reason": "this could kill R2/fR by theorem and strengthen EH/Lovelock route; curve digitization only bounds a leak after admitting it survives",
            "next_action": "963 should audit whether MTS parent action really forbids higher-curvature scalar modes by construction",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def next_target() -> list[dict[str, str]]:
    return [
        {
            "next_target": "963-Y5-R10-parent-second-order-signature-or-R2FR-bound-runner.md",
            "objective": "try to parent-sign the exact local second-order/no-extra-scalar action signature that makes the 962 R2/fR zero theorem absolute; if it fails, convert the scalar-mode rows into a nonclaim R10/PPN runner spec",
            "include": "parent derivative-order audit; Ostrogradsky/scalar-pole exclusion; quotient/locality conditions; R2/fR coefficient owner; optional R10 full-curve acquisition plan",
            "exclude": "torsion full proof, EH/local-GR claim, invented coefficients, GitHub action, formalization-workbench edits",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
    ]


def validation(
    sources: list[dict[str, str]],
    proof_rows: list[dict[str, str]],
    pole_rows: list[dict[str, str]],
    bound_rows: list[dict[str, str]],
    claim_rows: list[dict[str, str]],
    decision_rows: list[dict[str, str]],
    target_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    local_sources_ok = all(
        source["exists_or_recorded"] == "true" and source["needle_or_url_recorded"] == "true"
        for source in sources
        if source["source_type"] == "local"
    )
    web_sources_ok = all(
        source["exists_or_recorded"] == "true" and source["needle_or_url_recorded"] == "true"
        for source in sources
        if source["source_type"] == "web"
    )
    relative_theorem_present = any(row["result"] == "RELATIVE_THEOREM_PROVEN_PARENT_PREMISE_UNSIGNED" for row in proof_rows)
    absolute_claim_blocked = any(row["gate_id"] == "CGATE962_1_absolute_MTS_zero" and row["gate_pass"] == "false" for row in claim_rows)
    pole_values_positive = all(
        float(row["numeric_value"]) > 0
        for row in pole_rows
        if row["test_id"] in {"SP962_2_Lee2020_anchor_mass", "SP962_3_Kapner2007_anchor_mass"}
    )
    bound_rows_nonclaim = all(row["valid_for_claim"] == "false" and row["ready_for_runner"] == "false" for row in bound_rows)
    no_bound_row_smuggles_curve = all(
        not (row["status"] == "source_backed_anchor_not_claim_curve" and row["valid_for_claim"] == "true")
        for row in bound_rows
    )
    claim_gates_safe = all(row["valid_for_claim"] == "false" for row in claim_rows) and all(
        row["claim_allowed"] != "true" for row in claim_rows
    )
    no_formalization_edits = formalization_changed_after_start() == 0
    outputs_inside_root = all(
        str(path.resolve()).startswith(str(ROOT.resolve()))
        for path in [
            DOC,
            OUT / "P8_Y5_R10_962_SOURCE_REGISTER.csv",
            OUT / "P8_Y5_R10_962_R2FR_ZERO_PROOF_ATTEMPT.csv",
            OUT / "P8_Y5_R10_962_TRACE_SCALAR_POLE_TEST.csv",
            OUT / "P8_Y5_R10_962_SCALAR_BOUND_FALLBACK_ROWS.csv",
            OUT / "P8_Y5_R10_962_CLAIM_GATE.csv",
            OUT / "P8_Y5_R10_962_DECISION_LEDGER.csv",
            OUT / "P8_Y5_R10_962_NEXT_TARGET.csv",
            OUT / "P8_Y5_BRR545_962_VALIDATION.csv",
        ]
    )
    checks = [
        ("V962_0_local_sources_checked", local_sources_ok, "all cited local source paths exist and needles were found"),
        ("V962_1_web_sources_recorded", web_sources_ok, "all cited web source strings recorded"),
        ("V962_2_relative_theorem_present", relative_theorem_present, "R2/fR relative zero theorem row present"),
        ("V962_3_absolute_claim_blocked", absolute_claim_blocked, "absolute MTS c_R2/c_fR zero claim remains blocked"),
        ("V962_4_anchor_mass_positive", pole_values_positive, "lambda-to-mass anchor conversions are positive"),
        ("V962_5_bound_rows_nonclaim", bound_rows_nonclaim, "all scalar bound fallback rows are nonclaim and not runner-ready"),
        ("V962_6_no_curve_smuggle", no_bound_row_smuggles_curve, "anchor-only rows are not treated as full curves"),
        ("V962_7_claim_gates_safe", claim_gates_safe, "claim gates do not permit an absolute pass"),
        ("V962_8_decisions_ready", len(decision_rows) == 3, "decision ledger has three rows"),
        ("V962_9_next_target_ready", len(target_rows) == 1, "next target row written"),
        ("V962_10_formalization_untouched", no_formalization_edits, "formalization-workbench modified-file count since script start is zero"),
        ("V962_11_outputs_inside_post_checkpoint", outputs_inside_root, "all outputs resolve inside post-checkpoint-work"),
    ]
    rows = [
        {
            "check_id": check_id,
            "result": "pass" if passed else "fail",
            "detail": detail,
            "generated_utc": stamp(),
        }
        for check_id, passed, detail in checks
    ]
    rows.append(
        {
            "check_id": "V962_12_validation_rows_ready",
            "result": "pass" if all(row["result"] == "pass" for row in rows) else "fail",
            "detail": "962 validation pack assembled",
            "generated_utc": stamp(),
        }
    )
    return rows


def write_doc(
    sources: list[dict[str, str]],
    proof_rows: list[dict[str, str]],
    pole_rows: list[dict[str, str]],
    bound_rows: list[dict[str, str]],
    claim_rows: list[dict[str, str]],
    decision_rows: list[dict[str, str]],
    target_rows: list[dict[str, str]],
    validation_rows: list[dict[str, str]],
) -> None:
    doc = f"""# 962 Y5 R10: R2/fR Zero Clause Proof Or Scalar-Mode Bound Source Acquisition

Status: `Y5_R10_962_R2FR_relative_zero_theorem_proven_absolute_parent_signature_missing_nonclaim`

Claim ceiling: no EH, R10, PPN, Newton, measured-GM, or local-GR claim is made. This checkpoint proves a conditional theorem and keeps the empirical fallback nonclaim.

## Readout

This is a useful win, but not the final win. The `R2/fR` leak is now mathematically boxed: a nonlinear `f(R)` term generically brings either higher metric derivatives or a finite scalar trace pole. Therefore, if the parent MTS local exterior branch is exactly metric-only, local, diffeo-invariant, second-order, and has no retained scalar, then `c_R2=c_fR=0`.

What is still missing is the parent signature saying that MTS really has that exact second-order/no-extra-scalar local action. So: relative theorem proven, absolute MTS claim still blocked. That is good progress, not a bluff.

## Source Register

{md_table(sources, ["source_id", "source_type", "path_or_url", "role", "exists_or_recorded", "needle_or_url_recorded", "extraction_status"])}

## R2/fR Zero Proof Attempt

{md_table(proof_rows, ["step_id", "claim_attempted", "result", "mathematical_step", "blocking_input"])}

## Trace Scalar Pole Test

{md_table(pole_rows, ["test_id", "model_branch", "derived_quantity", "formula", "numeric_value", "units", "status"])}

## Scalar Bound Fallback Rows

{md_table(bound_rows, ["bound_id", "route", "source_url", "alpha_value", "lambda_value_um", "mass_eV", "status", "valid_for_claim"])}

## Claim Gate

{md_table(claim_rows, ["gate_id", "claim", "current_evidence", "gate_pass", "claim_allowed"])}

## Decision Ledger

{md_table(decision_rows, ["decision_id", "topic", "result", "reason", "next_action"])}

## Validation

{md_table(validation_rows, ["check_id", "result", "detail", "generated_utc"])}

## Next Target

{md_table(target_rows, ["next_target", "objective", "include", "exclude", "valid_for_claim"])}
"""
    DOC.write_text(doc, encoding="utf-8")


def main() -> None:
    sources = source_register()
    proof_rows = r2_fr_zero_proof_attempt()
    pole_rows = trace_scalar_pole_test()
    bound_rows = scalar_bound_fallback_rows()
    claim_rows = claim_gates()
    decision_rows = decisions()
    target_rows = next_target()
    validation_rows = validation(sources, proof_rows, pole_rows, bound_rows, claim_rows, decision_rows, target_rows)

    write_csv(
        OUT / "P8_Y5_R10_962_SOURCE_REGISTER.csv",
        sources,
        [
            "source_id",
            "source_type",
            "path_or_url",
            "role",
            "needle",
            "absolute_path",
            "exists_or_recorded",
            "needle_or_url_recorded",
            "extraction_status",
            "valid_for_claim",
            "generated_utc",
        ],
    )
    write_csv(
        OUT / "P8_Y5_R10_962_R2FR_ZERO_PROOF_ATTEMPT.csv",
        proof_rows,
        [
            "step_id",
            "claim_attempted",
            "mathematical_step",
            "test",
            "result",
            "would_close_if",
            "blocking_input",
            "valid_for_claim",
            "generated_utc",
        ],
    )
    write_csv(
        OUT / "P8_Y5_R10_962_TRACE_SCALAR_POLE_TEST.csv",
        pole_rows,
        ["test_id", "model_branch", "input_assumption", "derived_quantity", "formula", "numeric_value", "units", "status", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_R10_962_SCALAR_BOUND_FALLBACK_ROWS.csv",
        bound_rows,
        [
            "bound_id",
            "operator_family",
            "route",
            "source_url",
            "required_parent_inputs",
            "alpha_value",
            "lambda_value_um",
            "mass_eV",
            "extraction_method",
            "status",
            "ready_for_runner",
            "valid_for_claim",
            "reason_blocked",
            "generated_utc",
        ],
    )
    write_csv(
        OUT / "P8_Y5_R10_962_CLAIM_GATE.csv",
        claim_rows,
        ["gate_id", "claim", "required_condition", "current_evidence", "gate_pass", "claim_allowed", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_R10_962_DECISION_LEDGER.csv",
        decision_rows,
        ["decision_id", "topic", "result", "reason", "next_action", "claim_allowed", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_R10_962_NEXT_TARGET.csv",
        target_rows,
        ["next_target", "objective", "include", "exclude", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_BRR545_962_VALIDATION.csv",
        validation_rows,
        ["check_id", "result", "detail", "generated_utc"],
    )
    write_doc(sources, proof_rows, pole_rows, bound_rows, claim_rows, decision_rows, target_rows, validation_rows)


if __name__ == "__main__":
    main()
