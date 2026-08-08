from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
FW = REPO / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"

DOC = ROOT / "3220-Y5-R2FR-parent-source-root-for-EM-F2-or-finite-double-zero-coefficient-input-under-AX1090.md"
INPUTS = OUT / "P8_Y5_R2FR_3220_INPUTS.csv"
OWNERSHIP = OUT / "P8_Y5_R2FR_3220_EM_SOURCE_ROOT_OWNERSHIP_TEST.csv"
TRANSFER = OUT / "P8_Y5_R2FR_3220_GENERIC_DZ_TO_EM_F2_TRANSFER_AUDIT.csv"
COUNTER = OUT / "P8_Y5_R2FR_3220_EM_SOURCE_ROOT_COUNTERMODELS.csv"
FINITE = OUT / "P8_Y5_R2FR_3220_FINITE_DZ_INPUT_REQUIREMENTS.csv"
DECISION = OUT / "P8_Y5_R2FR_3220_DECISION.csv"
VALIDATION = OUT / "P8_Y5_R2FR_3220_VALIDATION.csv"


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def b(value: bool) -> str:
    return "true" if value else "false"


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def resolve(location: str, relative_path: str) -> Path:
    if location == "post_checkpoint":
        return ROOT / relative_path
    if location == "mts_residuals":
        return OUT / relative_path
    if location == "formalization":
        return FW / relative_path
    raise ValueError(location)


def evidence(path: Path, terms: list[str], limit: int = 4) -> str:
    if not path.exists():
        return "MISSING_SOURCE"
    lowered = [term.lower() for term in terms]
    hits: list[str] = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8", errors="replace").splitlines(), start=1):
        haystack = line.lower()
        if any(term in haystack for term in lowered):
            compact = " ".join(line.strip().split())[:190]
            hits.append(f"L{line_number}:{compact}")
        if len(hits) >= limit:
            break
    return " | ".join(hits) if hits else "NO_MATCH"


def md_escape(value: object) -> str:
    return str(value).replace("\\", "\\\\").replace("|", "\\|").replace("\n", "<br>")


def md_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    body = ["| " + " | ".join(md_escape(row.get(column, "")) for column in columns) + " |" for row in rows]
    return "\n".join([header, sep, *body])


SOURCES = [
    {
        "input_id": "SRC3220_00_3219_doc",
        "location": "post_checkpoint",
        "relative_path": "3219-Y5-R2FR-EM-F2-strict-double-zero-source-root-or-balpha-m-finite-bound-under-AX1090.md",
        "role": "3219 strict EM F2 double-zero handoff",
        "terms": ["Z_A(m)", "b_alpha_m", "G_eff", "parent-signed EM source-root"],
    },
    {
        "input_id": "SRC3220_01_3218_doc",
        "location": "post_checkpoint",
        "relative_path": "3218-Y5-R2FR-EM-F2-vertex-owner-for-memory-slope-zero-or-balpha-m-source-row-under-AX1090.md",
        "role": "EM F2 coefficient decomposition and countermodels",
        "terms": ["Z_A =", "f_m(m)", "BAM3218_3_double_zero_subroute", "CEX3218_0_fm_linear"],
    },
    {
        "input_id": "SRC3220_02_1099_doc",
        "location": "post_checkpoint",
        "relative_path": "1099-Y5-R10-unique-EM-kinetic-owner-no-extra-F2-theorem-or-alpha-coefficient-source-row.md",
        "role": "unique EM kinetic owner/no-extra-F2 theorem attempt",
        "terms": ["UEM1099_2_counterterm", "f_X(Xhat)F_Q^2", "no-extra-F2"],
    },
    {
        "input_id": "SRC3220_03_1100_doc",
        "location": "post_checkpoint",
        "relative_path": "1100-Y5-R10-parent-TQ-owner-fixed-charge-lattice-and-gauge-norm-signature.md",
        "role": "TQ/gauge norm signature failure",
        "terms": ["TQS1100_3_unique_curvature_norm", "lambda_A", "TQ_GAUGE_NORM_SIGNATURE_NOT_DERIVED"],
    },
    {
        "input_id": "SRC3220_04_1101_doc",
        "location": "post_checkpoint",
        "relative_path": "1101-Y5-R10-gauge-fibre-level-index-monopole-Ward-owner-or-alpha-product-route.md",
        "role": "gauge norm owner hunt",
        "terms": ["GNO1101_0_fixed_fibre_metric", "GAUGE_NORM_OWNER_NOT_DERIVED", "Ward"],
    },
    {
        "input_id": "SRC3220_05_1291_strict",
        "location": "mts_residuals",
        "relative_path": "P8_Y5_R10_1291_STRICT_DOUBLE_ZERO_PARENT_CLAUSE.csv",
        "role": "generic strict double-zero clause",
        "terms": ["SDZ1291_1_strict_F_form", "SDZ1291_5_parent_clause_verdict"],
    },
    {
        "input_id": "SRC3220_06_1533_contract",
        "location": "mts_residuals",
        "relative_path": "P8_Y5_PARENT_QLOC_1533_PARENT_ACTION_DOUBLE_ZERO_CONTRACT.csv",
        "role": "local parent action double-zero contract",
        "terms": ["VAC1533_1_potential_source", "VAC1533_4_local_lock", "VAC1533_6_verdict"],
    },
    {
        "input_id": "SRC3220_07_2141_theorem",
        "location": "mts_residuals",
        "relative_path": "P8_Y5_PARENT_QLOC_2141_DOUBLE_ZERO_THEOREM.csv",
        "role": "generic pointwise double-zero theorem",
        "terms": ["DZ2141_1_K_first_derivative", "DZ2141_6_verdict"],
    },
    {
        "input_id": "SRC3220_08_2817_coeffkill",
        "location": "mts_residuals",
        "relative_path": "P8_Y5_R2FR_2817_STRICT_DOUBLE_ZERO_COEFFICIENT_KILL.csv",
        "role": "generic coefficient kill transfer warning",
        "terms": ["CK2817_1_exact_double_zero", "CK2817_2_local_lock_dependency", "CK2817_4_verdict"],
    },
    {
        "input_id": "SRC3220_09_3071_root",
        "location": "mts_residuals",
        "relative_path": "P8_Y5_R2FR_3071_SOURCE_ROOT_DOUBLE_ZERO_ROUTE_AUDIT.csv",
        "role": "generic source-root/off-root fallback",
        "terms": ["SR3071_2_double_zero", "SR3071_3_finite_displacement"],
    },
    {
        "input_id": "SRC3220_10_3210_amp",
        "location": "post_checkpoint",
        "relative_path": "3210-Y5-R2FR-scalar-nohair-amplitude-law-and-omega-zero-curl-gate-under-AX1090.md",
        "role": "finite displacement amplitude fallback",
        "terms": ["Y_X", "source/boundary leakage", "||X||_H1"],
    },
    {
        "input_id": "SRC3220_11_3215_nohair",
        "location": "post_checkpoint",
        "relative_path": "3215-Y5-R2FR-memory-scalar-nohair-or-coefficient-typing-theorem-for-balpha-Hodge-under-AX1090.md",
        "role": "corrected Hessian/nohair guard",
        "terms": ["positive memory no-hair", "corrected Hessian", "source stationarity"],
    },
]


def build_rows(now: str) -> tuple[list[dict[str, object]], ...]:
    input_rows: list[dict[str, object]] = []
    for source in SOURCES:
        path = resolve(source["location"], source["relative_path"])
        input_rows.append(
            {
                **source,
                "path": str(path),
                "exists": b(path.exists()),
                "evidence_hits": evidence(path, source["terms"]),
                "valid_for_claim": "false",
                "generated_utc": now,
            }
        )

    ownership_rows = [
        {
            "test_id": "ROOT3220_0_target",
            "needed_clause": "parent EM source-root coefficient",
            "mathematical_form": "S_EM = -1/4 int [Z_0 + lambda_F F_EM(m)] F_Q^2 with F_EM(m_*)=F_EM'(m_*)=0",
            "what_would_prove_it": "a parent-action source row naming F_EM as the scalar multiplying the observed EM F_Q^2 coefficient",
            "current_evidence": "3218/3219 define the target; 1291/1533/2141/2817/3071 prove generic double-zero algebra only",
            "result": "TARGET_NOT_PARENT_SIGNED",
            "missing_for_claim": "EM-specific parent vertex owner for F_EM; same-branch m_* lock; no readout/radiative re-entry",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "test_id": "ROOT3220_1_same_memory_branch",
            "needed_clause": "same m controls local nohair and EM kinetic coefficient",
            "mathematical_form": "m in F_EM(m) is the same locally locked memory scalar used in the R2FR/local branch",
            "what_would_prove_it": "source path tying the EM coefficient variable to the same Euler/fixed-point branch, not a separately fitted scalar",
            "current_evidence": "3210/3215 provide amplitude/nohair language; no EM coefficient ownership row ties that m to Z_A",
            "result": "UNSIGNED",
            "missing_for_claim": "same-branch identity map m_EM=m_local with normalization and source path",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "test_id": "ROOT3220_2_double_zero_shape",
            "needed_clause": "strict source-root shape",
            "mathematical_form": "F_EM(m)=(m-m_*)^2 H_EM(m), H_EM smooth and finite near m_*",
            "what_would_prove_it": "parent source-root row for the EM coefficient, including H_EM regularity and no inverse-zero factors",
            "current_evidence": "1291 gives the generic F=(m-m_*)^2 H form; it is not attached to EM F_Q^2",
            "result": "GENERIC_FORM_AVAILABLE_EM_ATTACHMENT_MISSING",
            "missing_for_claim": "H_EM definition and EM coefficient source path",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "test_id": "ROOT3220_3_no_multiplier_cheat",
            "needed_clause": "not a post-hoc selector",
            "mathematical_form": "F_EM is a composite/even parent scalar in the action, not a Lagrange multiplier or readout switch",
            "what_would_prove_it": "operator-domain or construction proof excluding independent selector stress and fitted per-system roots",
            "current_evidence": "1291 has the guard; 3218 retains lambda_A/f_m/readout countermodels",
            "result": "GUARD_WRITTEN_NOT_EM_CLOSED",
            "missing_for_claim": "operator-domain exhaustion or parent construction of F_EM",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "test_id": "ROOT3220_4_local_lock",
            "needed_clause": "local exterior sits at m_*",
            "mathematical_form": "m=m_* up to controlled Delta m on the local vacuum/worldtube branch",
            "what_would_prove_it": "positive operator/nohair plus boundary/readout silence after EM Hessian correction",
            "current_evidence": "3215 says positive memory nohair alone does not kill EM coupling; 3219 keeps Hessian debt",
            "result": "UNSIGNED",
            "missing_for_claim": "G_eff positivity after EM F2 correction; boundary/projection silence",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "test_id": "ROOT3220_5_hessian_floor",
            "needed_clause": "second-order EM correction remains harmless",
            "mathematical_form": "G_eff >= G_mem - eta_EM > 0 with eta_EM >= (1/4)|lambda_F F_EM''| ||F_Q^2||_op plus corrections",
            "what_would_prove_it": "finite numeric or parent-bounded lambda_F, F_EM'', field support norm, and G_mem floor",
            "current_evidence": "3219 derives the exact Hessian guard; no finite inputs are sourced",
            "result": "MISSING_FINITE_INPUTS",
            "missing_for_claim": "lambda_F; F_EM''; Z_min; ||F_Q^2||; G_mem; readout/radiative correction bound",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "test_id": "ROOT3220_6_wave_stress_channel",
            "needed_clause": "EM wave/Poynting channel is not silently ignored",
            "mathematical_form": "F_Q^2=0 for null waves does not imply T_EM=0 or Poynting flux=0",
            "what_would_prove_it": "separate Hodge/current/stress-energy descent or bound for EM radiation channels",
            "current_evidence": "3219 records the null-wave guard; no stress/Poynting source-root owner is signed here",
            "result": "SEPARATE_CHANNEL_RETAINED",
            "missing_for_claim": "Hodge-star/readout/current stress descent or finite Poynting-channel residual rows",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "test_id": "ROOT3220_7_verdict",
            "needed_clause": "promote EM F2 source-root",
            "mathematical_form": "ROOT3220_0 through ROOT3220_6 all close on one parent branch",
            "what_would_prove_it": "all rows parent-signed and Hessian/stress channels bounded",
            "current_evidence": "no source row found in current corpus that attaches the strict source-root specifically to EM F_Q^2",
            "result": "EM_F2_SOURCE_ROOT_NOT_PARENT_SIGNED",
            "missing_for_claim": "parent EM source-root owner or finite coefficient pack",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]

    transfer_rows = [
        {
            "transfer_id": "TR3220_0_conditional_transfer_theorem",
            "claim_piece": "generic double-zero can transfer to any coefficient only after ownership",
            "statement": "If a coefficient C_i(m)=C_i0+lambda_i F_i(m) and F_i(m_*)=F_i'(m_*)=0, then partial_m C_i|m_*=0.",
            "status": "EXACT_CONDITIONAL_THEOREM",
            "why_it_matters": "the algebra is real; the open issue is attaching i=EM F2 to the parent source-root",
            "blocks_or_allows": "allows EM route only if F_i=F_EM is source-backed",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "transfer_id": "TR3220_1_generic_root_not_enough",
            "claim_piece": "generic Kmetric/Gamma/L_cg source-root cannot be imported into Z_A",
            "statement": "F_GR(m) multiplying a metric or L_cg chain coefficient gives no theorem for partial_m Z_A unless the action identifies F_GR=F_EM in the EM kinetic vertex.",
            "status": "NO_TRANSFER_WITHOUT_VERTEX_IDENTITY",
            "why_it_matters": "prevents smuggling local-GR silence into alpha/EM silence",
            "blocks_or_allows": "blocks b_alpha_m=0 claim",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "transfer_id": "TR3220_2_hidden_counterterm_survives",
            "claim_piece": "legal scalar EM counterterm remains a countermodel",
            "statement": "Z_A=Z_0+epsilon m or Z_A=Z_0+epsilon(m-m_*) remains covariant and U(1)-gauge invariant unless operator-domain/sequester rules forbid it.",
            "status": "COUNTERMODEL_ACTIVE",
            "why_it_matters": "ordinary covariance cannot do the coupling work",
            "blocks_or_allows": "forces finite b_alpha_m row or source-root proof",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "transfer_id": "TR3220_3_null_wave_not_F2_proof",
            "claim_piece": "F2 source-root is not full EM stress silence",
            "statement": "For radiation, F_Q^2 can vanish while the Maxwell stress tensor and Poynting vector do not; therefore F2-coupling silence must be paired with Hodge/current/stress descent.",
            "status": "SEPARATE_GUARD",
            "why_it_matters": "keeps the user's wave/Poynting concern inside the gate instead of sweeping it away",
            "blocks_or_allows": "blocks Maxwell/local-GR claim from F2 source-root alone",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]

    counter_rows = [
        {
            "counter_id": "CEX3220_0_linear_EM_coefficient",
            "countermodel": "Z_A(m)=Z_0+epsilon(m-m_*)",
            "why_allowed_now": "scalar coefficient times F_Q^2 is diffeomorphism scalar and U(1) gauge invariant in the current operator ledger",
            "effect": "b_alpha_m=epsilon/Z_0 at m_*",
            "kills": "EM_F2_SOURCE_ROOT_CLAIM",
            "needed_to_remove": "no-extra-F2 theorem, exact shift/sequester, or parent EM source-root with F_EM'=0",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "counter_id": "CEX3220_1_generic_root_elsewhere",
            "countermodel": "metric chain has F_GR=(m-m_*)^2H_GR but EM has Z_A=Z_0+epsilon m",
            "why_allowed_now": "existing double-zero rows do not identify the EM kinetic coefficient with the generic local source-root",
            "effect": "local metric chain may be quiet while alpha/EM source remains live",
            "kills": "TRANSFER_FROM_LOCAL_GR_ROOT_TO_EM",
            "needed_to_remove": "same parent vertex identity F_GR=F_EM or unique visible-operator domain",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "counter_id": "CEX3220_2_readout_reentry",
            "countermodel": "bare Z_A has double-zero but alpha_eff=alpha_0 exp(epsilon m) after readout",
            "why_allowed_now": "radiative/readout closure remains unsigned in 1099/3218",
            "effect": "observed clocks/spectra see alpha drift even if the bare F2 vertex is locally stationary",
            "kills": "OBSERVED_ALPHA_SILENCE",
            "needed_to_remove": "effective-action/readout functor preserving the same source-root or Q_ONLY rule",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "counter_id": "CEX3220_3_wave_stress_escape",
            "countermodel": "null EM wave has F_Q^2=0 but nonzero T_EM and Poynting vector",
            "why_allowed_now": "the F2 coefficient gate does not own the full Maxwell stress/Hodge/current channel",
            "effect": "bulk scalar F2 source-root cannot be used as full EM stress-energy descent proof",
            "kills": "MAXWELL_STRESS_SILENCE_FROM_F2_ONLY",
            "needed_to_remove": "separate stress/current/Hodge descent theorem or finite wave-channel bound",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]

    finite_rows = [
        {
            "input_id": "FIN3220_0_lambda_F",
            "quantity": "lambda_F",
            "definition": "coefficient amplitude multiplying the EM source-root in Z_A=Z_0+lambda_F F_EM(m)",
            "units": "same as Z_A divided by F_EM units",
            "needed_for": "b_alpha_m off-root bound and Hessian correction",
            "current_value": "MISSING_PARENT_OR_NUMERIC_INPUT",
            "source_path": "MISSING_SOURCE_PATH",
            "status": "REQUIRED_NONCLAIM",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "input_id": "FIN3220_1_FEM_second_derivative",
            "quantity": "F_EM''(m_*)",
            "definition": "second derivative of the EM source-root at the local memory root",
            "units": "F_EM units per m^2",
            "needed_for": "eta_EM and off-root alpha residual",
            "current_value": "MISSING_PARENT_OR_NUMERIC_INPUT",
            "source_path": "MISSING_SOURCE_PATH",
            "status": "REQUIRED_NONCLAIM",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "input_id": "FIN3220_2_delta_m",
            "quantity": "Delta m local amplitude",
            "definition": "controlled displacement from m_* on the local branch/worldtube",
            "units": "m units",
            "needed_for": "|b_alpha_m| <= |lambda_F F_EM''| |Delta m|/Z_min + O(Delta m^2)",
            "current_value": "MISSING_LOCAL_LOCK_AMPLITUDE",
            "source_path": "3210 amplitude machinery exists but not EM-attached",
            "status": "REQUIRED_NONCLAIM",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "input_id": "FIN3220_3_Z_min",
            "quantity": "Z_min",
            "definition": "positive lower bound for Z_A near m_*",
            "units": "EM kinetic normalization units",
            "needed_for": "denominator guard for b_alpha_m and alpha residual",
            "current_value": "MISSING_POSITIVE_DENOMINATOR_SOURCE",
            "source_path": "MISSING_SOURCE_PATH",
            "status": "REQUIRED_NONCLAIM",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "input_id": "FIN3220_4_FQ2_norm",
            "quantity": "||F_Q^2||_op_or_support",
            "definition": "worst-case local support/operator norm for the EM invariant entering the Hessian correction",
            "units": "field-strength squared norm",
            "needed_for": "eta_EM >= (1/4)|lambda_F F_EM''| ||F_Q^2||",
            "current_value": "MISSING_ARENA_SUPPORT_NORM",
            "source_path": "MISSING_SOURCE_PATH",
            "status": "REQUIRED_NONCLAIM",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "input_id": "FIN3220_5_G_mem_floor",
            "quantity": "G_mem lower spectral/coercivity floor",
            "definition": "positive floor of the memory Hessian before EM F2 correction",
            "units": "memory operator units",
            "needed_for": "G_eff >= G_mem - eta_EM > 0",
            "current_value": "MISSING_PARENT_OR_NUMERIC_INPUT",
            "source_path": "3215 has theorem shape but not the EM-corrected finite value",
            "status": "REQUIRED_NONCLAIM",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "input_id": "FIN3220_6_readout_radiative_bound",
            "quantity": "eta_readout/radiative",
            "definition": "extra correction from effective-action/readout regeneration of the alpha coefficient",
            "units": "same operator correction units as eta_EM or dimensionless alpha slope bound",
            "needed_for": "observed alpha and clock/spectroscopy silence",
            "current_value": "MISSING_CLOSURE_BOUND",
            "source_path": "1099/3218 retain readout/radiative countermodels",
            "status": "REQUIRED_NONCLAIM",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "input_id": "FIN3220_7_Poynting_stress_bound",
            "quantity": "EM wave/current stress residual",
            "definition": "bound or theorem for Maxwell stress/Poynting channel not controlled by F_Q^2 alone",
            "units": "stress-energy/current flux units",
            "needed_for": "full Maxwell/EM stress descent rather than F2 coefficient silence only",
            "current_value": "MISSING_STRESS_CHANNEL_INPUT",
            "source_path": "MISSING_HODGE_CURRENT_STRESS_DESCENT_SOURCE",
            "status": "REQUIRED_NONCLAIM",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]

    decision_rows = [
        {
            "decision_id": "DEC3220_0_result",
            "decision": "EM_F2_SOURCE_ROOT_NOT_PARENT_SIGNED_FINITE_DZ_INPUTS_STAGED",
            "because": "the strict double-zero algebra is valid, but the current corpus does not attach F_EM(m) specifically to the EM F_Q^2 coefficient on the same locally locked branch",
            "claim_status": "NO_BALPHA_M_ZERO_CLAIM_NO_LOCAL_GR_CLAIM_NO_MAXWELL_STRESS_CLAIM",
            "next_action": "hunt a parent EM source-root owner or promote finite input acquisition for lambda_F, F_EM'', Delta m, Z_min, ||F_Q^2||, G_mem, readout, and Poynting/stress residuals",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "decision_id": "DEC3220_1_best_next",
            "decision": "3221-Y5-R2FR-EM-source-root-owner-hunt-or-finite-coefficient-row-promotion-under-AX1090",
            "because": "one more targeted owner hunt can still move the theory; if it fails, the branch should stop repeating zero attempts and become finite coefficient acquisition",
            "claim_status": "PRIVATE_NEXT_TARGET",
            "next_action": "test whether parent action, phase/current, Hodge, or operator-domain rows can supply the EM-specific vertex owner",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]

    return input_rows, ownership_rows, transfer_rows, counter_rows, finite_rows, decision_rows


def validation_rows(
    now: str,
    input_rows: list[dict[str, object]],
    ownership_rows: list[dict[str, object]],
    transfer_rows: list[dict[str, object]],
    counter_rows: list[dict[str, object]],
    finite_rows: list[dict[str, object]],
    decision_rows: list[dict[str, object]],
) -> list[dict[str, object]]:
    out_paths = [INPUTS, OWNERSHIP, TRANSFER, COUNTER, FINITE, DECISION]
    all_source_paths_exist = all(row["exists"] == "true" for row in input_rows)
    verdict = next(row for row in ownership_rows if row["test_id"] == "ROOT3220_7_verdict")
    generic_block = any(row["transfer_id"] == "TR3220_1_generic_root_not_enough" for row in transfer_rows)
    poynting_guard = any(row["test_id"] == "ROOT3220_6_wave_stress_channel" for row in ownership_rows) and any(
        row["counter_id"] == "CEX3220_3_wave_stress_escape" for row in counter_rows
    )
    finite_requirement_count = len(finite_rows)
    claim_true_count = 0
    for rows in [input_rows, ownership_rows, transfer_rows, counter_rows, finite_rows, decision_rows]:
        for row in rows:
            if str(row.get("valid_for_claim", "")).lower() == "true":
                claim_true_count += 1
    no_fw_outputs = all(FW not in [path, *path.parents] for path in out_paths + [DOC])

    csv_parse_detail: list[str] = []
    csv_parse_ok = True
    for path in out_paths:
        try:
            parsed = read_csv(path)
            if not parsed:
                csv_parse_ok = False
            csv_parse_detail.append(path.name)
        except Exception as exc:
            csv_parse_ok = False
            csv_parse_detail.append(f"{path.name}:{exc}")

    return [
        {
            "check_id": "VAL3220_00_inputs_exist",
            "pass": b(all_source_paths_exist),
            "detail": f"inputs={len(input_rows)}",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3220_01_target_verdict_written",
            "pass": b(verdict["result"] == "EM_F2_SOURCE_ROOT_NOT_PARENT_SIGNED"),
            "detail": str(verdict["result"]),
            "generated_utc": now,
        },
        {
            "check_id": "VAL3220_02_generic_transfer_blocked",
            "pass": b(generic_block),
            "detail": "generic double-zero cannot transfer to EM F2 without vertex identity",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3220_03_countermodels_retained",
            "pass": b(len(counter_rows) >= 4),
            "detail": ";".join(row["counter_id"] for row in counter_rows),
            "generated_utc": now,
        },
        {
            "check_id": "VAL3220_04_poynting_wave_guard",
            "pass": b(poynting_guard),
            "detail": "F2 silence does not equal Maxwell stress/Poynting silence",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3220_05_finite_inputs_staged",
            "pass": b(finite_requirement_count >= 8),
            "detail": f"finite_rows={finite_requirement_count}",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3220_06_claims_blocked",
            "pass": b(claim_true_count == 0),
            "detail": f"claim_rows_true={claim_true_count}",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3220_07_no_formalization_workbench_edit",
            "pass": b(no_fw_outputs),
            "detail": "no formalization-workbench paths are output targets",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3220_08_csv_parse",
            "pass": b(csv_parse_ok),
            "detail": ";".join(csv_parse_detail),
            "generated_utc": now,
        },
        {
            "check_id": "VAL3220_09_next_target",
            "pass": b(decision_rows[-1]["decision"].startswith("3221-")),
            "detail": str(decision_rows[-1]["decision"]),
            "generated_utc": now,
        },
    ]


def write_doc(
    input_rows: list[dict[str, object]],
    ownership_rows: list[dict[str, object]],
    transfer_rows: list[dict[str, object]],
    counter_rows: list[dict[str, object]],
    finite_rows: list[dict[str, object]],
    decision_rows: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    text = f"""# 3220 - Parent Source-Root For EM F2 Or Finite Double-Zero Coefficient Input under AX1090

Private checkpoint. This is not a local-GR claim, Maxwell derivation claim, Newtonian-limit claim, WEP pass, R10 pass, clock pass, `b_alpha_m=0` claim, EM-lock claim, or public-facing result.

## Result

3220 tries the real leap, not another vibes audit:

```text
Can the strict double-zero source-root be attached to the EM kinetic coefficient itself?

S_EM = -1/4 int [Z_0 + lambda_F F_EM(m)] F_Q^2
F_EM(m_*) = 0
F_EM'(m_*) = 0
```

The answer from the current corpus is **no, not yet**. The algebra is solid: if the parent action owns that exact `F_EM` coefficient, then `partial_m Z_A|m_* = 0` and the linear `b_alpha_m` source dies. But the available double-zero rows are generic/local-chain rows. They do not yet prove that the same source-root multiplies the observed EM `F_Q^2` vertex.

That means the route is still alive, but only as one of two disciplined branches:

```text
Branch A: prove parent EM source-root ownership.
Branch B: stop claiming zero and source finite bounds for lambda_F, F_EM'', Delta m, Z_min, ||F_Q^2||, G_mem, readout, and EM stress/Poynting residuals.
```

Important wave guard: `F_Q^2=0` for null radiation does **not** mean the Maxwell stress tensor or Poynting vector vanishes. So an EM `F^2` double-zero can silence one scalar bulk coefficient, but it is not by itself a full Maxwell stress-energy descent theorem.

Current verdict: `EM_F2_SOURCE_ROOT_NOT_PARENT_SIGNED_FINITE_DZ_INPUTS_STAGED`.

## EM Source-Root Ownership Test

{md_table(ownership_rows, ["test_id", "needed_clause", "mathematical_form", "result", "missing_for_claim", "valid_for_claim"])}

## Generic Double-Zero To EM F2 Transfer Audit

{md_table(transfer_rows, ["transfer_id", "claim_piece", "statement", "status", "blocks_or_allows", "valid_for_claim"])}

## EM Source-Root Countermodels

{md_table(counter_rows, ["counter_id", "countermodel", "why_allowed_now", "effect", "kills", "needed_to_remove", "valid_for_claim"])}

## Finite DZ Input Requirements

{md_table(finite_rows, ["input_id", "quantity", "definition", "needed_for", "current_value", "source_path", "status", "valid_for_claim"])}

## Decision

{md_table(decision_rows, ["decision_id", "decision", "because", "claim_status", "next_action", "valid_for_claim"])}

## Generated Evidence

- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3220_INPUTS.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3220_EM_SOURCE_ROOT_OWNERSHIP_TEST.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3220_GENERIC_DZ_TO_EM_F2_TRANSFER_AUDIT.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3220_EM_SOURCE_ROOT_COUNTERMODELS.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3220_FINITE_DZ_INPUT_REQUIREMENTS.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3220_DECISION.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3220_VALIDATION.csv`

## Source Register

{md_table(input_rows, ["input_id", "relative_path", "exists", "role", "evidence_hits", "valid_for_claim"])}

## Validation

{md_table(validation, ["check_id", "pass", "detail"])}

All generated rows remain `valid_for_claim=false`.
"""
    DOC.write_text(text, encoding="utf-8")


def main() -> None:
    now = stamp()
    rows = build_rows(now)
    input_rows, ownership_rows, transfer_rows, counter_rows, finite_rows, decision_rows = rows
    for path, rowset in [
        (INPUTS, input_rows),
        (OWNERSHIP, ownership_rows),
        (TRANSFER, transfer_rows),
        (COUNTER, counter_rows),
        (FINITE, finite_rows),
        (DECISION, decision_rows),
    ]:
        write_csv(path, rowset)
    validation = validation_rows(now, input_rows, ownership_rows, transfer_rows, counter_rows, finite_rows, decision_rows)
    write_csv(VALIDATION, validation)
    write_doc(input_rows, ownership_rows, transfer_rows, counter_rows, finite_rows, decision_rows, validation)
    print(f"wrote {DOC}")
    print(f"wrote {VALIDATION}")


if __name__ == "__main__":
    main()
