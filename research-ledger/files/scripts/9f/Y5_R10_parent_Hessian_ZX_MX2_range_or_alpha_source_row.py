from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


STARTED = datetime.now(timezone.utc)
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "1025-Y5-R10-parent-Hessian-ZX-MX2-range-or-alpha-source-row.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def flag(value: object) -> bool:
    return str(value).strip().lower() == "true"


def source_path(path_text: str) -> Path:
    path = Path(path_text)
    if path.is_absolute():
        return path
    return ROOT / path


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        fieldnames = []
        for row in rows:
            for key in row:
                if key not in fieldnames:
                    fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key, "") for key in fieldnames})


def md_cell(value: object) -> str:
    return str(value).replace("\n", " ").replace("|", "\\|")


def md_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    if not rows:
        return "_No rows._\n"
    return "\n".join(
        [
            "| " + " | ".join(columns) + " |",
            "| " + " | ".join("---" for _ in columns) + " |",
            *["| " + " | ".join(md_cell(row.get(column, "")) for column in columns) + " |" for row in rows],
        ]
    ) + "\n"


def source_register_rows() -> list[dict[str, str]]:
    specs = [
        ("SRC1025_0_1024_next", "source-intake/mts_residuals/P8_Y5_R10_1024_NEXT_TARGET.csv", "1025-Y5-R10-parent-Hessian", "1024 handoff to parent Hessian and alpha source row."),
        ("SRC1025_1_1024_inputs", "source-intake/mts_residuals/P8_Y5_R10_1024_SCALAR_INPUT_ASSESSMENT.csv", "SIA1024_1_Z_X", "1024 scalar input gaps."),
        ("SRC1025_2_1024_alpha", "source-intake/mts_residuals/P8_Y5_R10_1024_ALPHA_COEFFICIENT_ROWS.csv", "ALPHA1024_0_bulk_operator", "1024 residual alpha coefficient blockers."),
        ("SRC1025_3_617_field_space", "source-intake/mts_residuals/P8_Y5_R10_617_FIELD_SPACE_NORMALIZATION_ATTEMPT.csv", "FS617_0_exact_second_variation", "617 conditional field-space law."),
        ("SRC1025_4_617_beta", "source-intake/mts_residuals/P8_Y5_R10_617_BETA_EIGENVALUE_CANDIDATE_LEDGER.csv", "BS617_1_beta3", "617 beta-eigenvalue candidate ledger."),
        ("SRC1025_5_616_vacuum", "source-intake/mts_residuals/P8_Y5_R10_616_VACUUM_OWNER_ATTEMPT.csv", "VO616_2_local_X_Hessian_identity", "616 Hessian-ratio blocker."),
        ("SRC1025_6_579_contract", "source-intake/mts_residuals/P8_Y5_R10_579_EXPLICIT_PARENT_X_BLOCK_CONTRACT.csv", "PXC579_1_positive_kinetic_residue", "579 parent X block contract."),
        ("SRC1025_7_580_candidates", "source-intake/mts_residuals/P8_Y5_R10_580_PARENT_BLOCK_CANDIDATES.csv", "PB580_2_positive_sourcefree_massive_X", "580 parent block candidates."),
        ("SRC1025_8_562_formula", "source-intake/mts_residuals/P8_Y5_R10_ZX_LAMBDA_PREFACtOR_FORMULA_REGISTER.csv", "PR562_2_canonical_mass_and_range", "562 conditional lambda/prefactor formula."),
        ("SRC1025_9_669_residual", "source-intake/mts_residuals/P8_Y5_R10_669_R10_R11_RESIDUAL_VECTOR.csv", "RV669_0_Z_X", "669 residual vector."),
        ("SRC1025_10_669_gates", "source-intake/mts_residuals/P8_Y5_R10_669_LX_OWNER_GATE_TESTS.csv", "G669_1_positive_kinetic", "669 owner gates."),
        ("SRC1025_11_670_nohair", "source-intake/mts_residuals/P8_Y5_R10_670_POSITIVE_SOURCEFREE_PROOF_CHAIN.csv", "PSF670_2_positive_kinetic", "670 positive source-free chain."),
        ("SRC1025_12_618_source_zero", "source-intake/mts_residuals/P8_Y5_R10_618_SOURCE_ZERO_CERTIFICATE_AUDIT.csv", "SZ618_0_qbar_XT_chain_rule", "618 source-zero certificate audit."),
        ("SRC1025_13_1019_schema", "source-intake/mts_residuals/P8_Y5_R10_1019_SOURCE_PACK_SCHEMA.csv", "SP1019_2_bulk_X_coefficients", "1019 source pack schema."),
    ]
    rows: list[dict[str, str]] = []
    for source_id, path_text, needle, role in specs:
        path = source_path(path_text)
        exists = path.exists()
        text = path.read_text(encoding="utf-8", errors="ignore") if exists else ""
        rows.append(
            {
                "source_id": source_id,
                "source_path": str(path),
                "exists": str(exists).lower(),
                "needle": needle,
                "needle_found": str(needle in text).lower(),
                "role": role,
                "valid_for_claim": "false",
                "generated_utc": stamp(),
            }
        )
    return rows


def second_variation_rows() -> list[dict[str, str]]:
    return [
        {
            "derivation_id": "SV1025_0_local_block",
            "step": "write the minimal local X block",
            "mathematical_statement": "S_X=int_A sqrt(h)[1/2 Z_X h^{ij} partial_i X partial_j X + 1/2 M_X^2 X^2 - J_X X] + boundary",
            "derived_result": "this is the smallest scalar block whose second variation can define the local finite-range channel",
            "status": "CONDITIONAL_ANSATZ_ONLY",
            "missing_for_claim": "same parent action must produce this block, field X, h_ij, Z_X, M_X^2, J_X, and boundary terms",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "derivation_id": "SV1025_1_euler_operator",
            "step": "vary X once",
            "mathematical_statement": "delta_X S_X -> O_X X = J_X with O_X=-nabla_i(Z_X nabla^i)+M_X^2",
            "derived_result": "the correct local operator is fixed once the parent block and boundary convention are owned",
            "status": "CONDITIONAL_OPERATOR_DERIVED",
            "missing_for_claim": "parent Euler expression, self-adjoint domain, and source split",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "derivation_id": "SV1025_2_Hessian_signs",
            "step": "vary X twice",
            "mathematical_statement": "delta_X^2 S_X=int_A sqrt(h)[Z_X |grad delta X|^2+M_X^2(delta X)^2]+boundary Hessian terms",
            "derived_result": "Z_X>0 and M_X^2>0 are the exact local stability requirements",
            "status": "EXACT_CONDITION_DERIVED_VALUES_MISSING",
            "missing_for_claim": "parent Hessian signs, mixed-sector Hessian control, and units",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "derivation_id": "SV1025_3_range_relation",
            "step": "canonicalize the static operator",
            "mathematical_statement": "mu_X^2=M_X^2/Z_X and lambda_X=sqrt(Z_X/M_X^2)",
            "derived_result": "lambda_X is exact if Z_X and M_X^2 are positive and come from the same normalized parent branch",
            "status": "EXACT_RELATION_DERIVED_NOT_OWNED",
            "missing_for_claim": "numeric or symbolic same-branch Z_X/M_X^2 with length units",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "derivation_id": "SV1025_4_field_rescaling_guard",
            "step": "block fake normalization wins",
            "mathematical_statement": "X->aX rescales Z_X and M_X^2 together; lambda_X and Z_X f_X^2 are the invariant objects",
            "derived_result": "field rescaling cannot be used to choose beta, lambda, or alpha after the fact",
            "status": "GUARDRAIL_PASS",
            "missing_for_claim": "parent field-space metric or Ward identity fixing the invariant normalization",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "derivation_id": "SV1025_5_sourcefree_nohair",
            "step": "connect Hessian to local silence",
            "mathematical_statement": "int_A[Z_X|grad X|^2+M_X^2 X^2]=int_A X J_X+boundary_flux_X",
            "derived_result": "if Z_X>0, M_X^2>0, J_X=0, and boundary_flux_X=0, then X=0 on the local exterior",
            "status": "CONDITIONAL_THEOREM_ONLY",
            "missing_for_claim": "J_X=0, boundary flux zero, and parent-signed positivity all together",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "derivation_id": "SV1025_6_verdict",
            "step": "decide whether 1025 owns the Hessian",
            "mathematical_statement": "parent_signed(delta_X^2 S_parent) -> Z_X,M_X^2,lambda_X,alpha source row",
            "derived_result": "1025 derives the exact contract but does not find a parent-signed Hessian in the current corpus",
            "status": "FAIL_CURRENT_CLAIM_CONTRACT_SHARPENED",
            "missing_for_claim": "explicit parent second variation and normalization ledger",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def parent_hessian_audit_rows() -> list[dict[str, str]]:
    return [
        {
            "audit_id": "PHA1025_0_branch_extremum",
            "object": "F_1=E_X|_{X=0}",
            "required_evidence": "parent Euler expression vanishes on the local branch before readout",
            "current_evidence": "PXC579_0 says not_parent_filled; 1024 keeps scalar branch nonclaim",
            "status": "MISSING_PARENT_EULER_ZERO",
            "if_missing": "X=0 is not proven to be a stationary local vacuum",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "audit_id": "PHA1025_1_ZX_positive",
            "object": "Z_X>0",
            "required_evidence": "positive gradient Hessian residue with field units and sign convention",
            "current_evidence": "PXC579_1 formula_only; RV669_0 MISSING_PARENT_INPUT; FS617 identifies normalization blocker",
            "status": "MISSING_PARENT_HESSIAN_SIGN",
            "if_missing": "ghost, anti-elliptic, or indefinite local residual must be retained",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "audit_id": "PHA1025_2_MX2_positive",
            "object": "M_X^2>0",
            "required_evidence": "positive local curvature Hessian in the same X normalization",
            "current_evidence": "PXC579_2 formula_only; RV669_1 MISSING_PARENT_INPUT; 617 beta eigenvalue not signed",
            "status": "MISSING_PARENT_MASS_GAP",
            "if_missing": "massless, tachyonic, or long-range branch remains possible",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "audit_id": "PHA1025_3_lambda_units",
            "object": "lambda_X=sqrt(Z_X/M_X^2)",
            "required_evidence": "same-branch Z_X and M_X^2 with compatible units, yielding meters",
            "current_evidence": "PR562_2 gives exact relation but values/units missing; 1024 refuses alpha row",
            "status": "RELATION_ONLY_VALUES_MISSING",
            "if_missing": "R10 interpolation cannot be a claim-grade comparison",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "audit_id": "PHA1025_4_cross_Hessian",
            "object": "mixed X-sector Hessian terms",
            "required_evidence": "cross terms with metric, trace, projector, boundary, and matter variables vanish or form a positive block",
            "current_evidence": "617 says nearby field metrics own pieces conditionally but not the full X metric or cross-term policy",
            "status": "MISSING_BLOCK_DIAGONAL_OR_POSITIVE_MATRIX_PROOF",
            "if_missing": "single-scalar Z_X/M_X^2 may be an invalid truncation",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "audit_id": "PHA1025_5_source_current",
            "object": "J_X=0 or J_X bound",
            "required_evidence": "delta_X S_matter plus hidden/source/domain terms vanish or are numerically bounded",
            "current_evidence": "SZ618_0 is conditional not parent signed; RV669_2 missing source-zero proof",
            "status": "MISSING_SOURCE_ZERO_OR_BOUND",
            "if_missing": "qbar_XT/source-coupling remains the live finite-force channel",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "audit_id": "PHA1025_6_boundary_flux",
            "object": "boundary_flux_X=0 or bound",
            "required_evidence": "self-adjoint boundary class, exact/proper gauge edge, or explicit flux bound",
            "current_evidence": "PSF670_5 and 1024 keep boundary flux missing",
            "status": "MISSING_BOUNDARY_LOCK",
            "if_missing": "edge residual can replace the silenced bulk channel",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "audit_id": "PHA1025_7_prefactor",
            "object": "K_X=s_X/(4*pi*Z_X*G_obs)",
            "required_evidence": "normalization convention, sign s_X, G_obs frame, and source/test charges",
            "current_evidence": "PR562_4 conditional; ALPHA1024_3 MISSING_ARENA_PROJECTION",
            "status": "MISSING_ALPHA_NORMALIZATION",
            "if_missing": "alpha(lambda) row remains smoke-only",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "audit_id": "PHA1025_8_verdict",
            "object": "parent Hessian ownership",
            "required_evidence": "PHA1025_0 through PHA1025_7 close from one parent branch",
            "current_evidence": "none of the parent-owned value/sign/source rows close",
            "status": "FAIL_CURRENT_CLAIM",
            "if_missing": "move to parent metric/eigenvalue theorem or source-zero return",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def normalization_lock_rows() -> list[dict[str, str]]:
    return [
        {
            "lock_id": "FNL1025_0_invariant",
            "target": "identify the physical finite-range invariant",
            "condition": "beta_eff=ell_vac^2 M_X^2/Z_X=U''(0) rho_vac^(1/2)/(Z_X f_X^2)",
            "current_status": "CONDITIONAL_INVARIANT_IDENTIFIED",
            "allowed_use": "theorem target and normalization guard",
            "forbidden_use": "claim that rho_vac alone predicts lambda_X",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "lock_id": "FNL1025_1_canonical_metric",
            "target": "make vacuum density set the field-space metric",
            "condition": "Z_X f_X^2=rho_vac^(1/2)",
            "current_status": "CLEAN_CONTRACT_NOT_SIGNED",
            "allowed_use": "parent Ward/metric theorem target",
            "forbidden_use": "normalization chosen after R10 pressure",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "lock_id": "FNL1025_2_beta3",
            "target": "low-scrutiny finite theorem target",
            "condition": "U''(0)=3 from a spatial trace/eigenvalue theorem",
            "current_status": "BEST_CONDITIONAL_TARGET_NOT_SIGNED",
            "allowed_use": "private derivation target",
            "forbidden_use": "predicted beta/lambda claim",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "lock_id": "FNL1025_3_direct_range",
            "target": "direct 38.6um backsolve",
            "condition": "beta=5.206677122050 chosen to hit lambda=38.6um",
            "current_status": "CLOSURE_ONLY_FORBIDDEN_AS_DERIVATION",
            "allowed_use": "sanity check only",
            "forbidden_use": "evidence or prediction",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "lock_id": "FNL1025_4_CX_tie",
            "target": "tie range normalization to source amplitude",
            "condition": "same parent normalization fixes lambda_X and C_X/K_X/qbar_XT/Qbar_XH",
            "current_status": "MISSING_COUPLING_NORMALIZATION_LEDGER",
            "allowed_use": "next source-row schema",
            "forbidden_use": "choose range and amplitude independently",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def alpha_source_rows() -> list[dict[str, str]]:
    return [
        {
            "row_id": "ASR1025_0_bulk_Hessian",
            "quantity": "Z_X;M_X2;lambda_X",
            "required_columns": "system_id;field_id;branch_id;Z_X;M_X2;lambda_X;Z_units;M_units;lambda_units;source_path;valid_for_claim",
            "formula": "lambda_X=sqrt(Z_X/M_X2)",
            "current_status": "MISSING_PARENT_INPUT",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_669_R10_R11_RESIDUAL_VECTOR.csv",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "row_id": "ASR1025_1_field_metric_beta",
            "quantity": "Z_X f_X^2;Upp0;beta_eff",
            "required_columns": "system_id;branch_id;ZX_fX2;Upp0;beta_eff;metric_units;source_path;valid_for_claim",
            "formula": "beta_eff=Upp0*rho_vac^(1/2)/(Z_X*f_X^2)",
            "current_status": "MISSING_PARENT_METRIC_AND_EIGENVALUE",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_617_FIELD_SPACE_NORMALIZATION_ATTEMPT.csv",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "row_id": "ASR1025_2_source_current",
            "quantity": "J_X or qbar_XT",
            "required_columns": "system_id;matter_sector;qbar_XT;J_X;J_X_bound;units;source_path;valid_for_claim",
            "formula": "J_X=delta_X S_matter + hidden/source/domain terms",
            "current_status": "MISSING_SOURCE_ZERO_OR_BOUND",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_618_SOURCE_ZERO_CERTIFICATE_AUDIT.csv",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "row_id": "ASR1025_3_Hamiltonian_projection",
            "quantity": "Qbar_XH",
            "required_columns": "system_id;source_body;Q_XH;Qbar_XH;projector;units;source_path;valid_for_claim",
            "formula": "Qbar_XH(lambda)=Pi_M^H[Q_X^H(lambda)]/M_H",
            "current_status": "MISSING_ARENA_PROJECTION",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1019_SOURCE_PACK_SCHEMA.csv",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "row_id": "ASR1025_4_green_prefactor",
            "quantity": "K_X",
            "required_columns": "system_id;K_X;s_X;Z_X;G_obs;normalization;units;source_path;valid_for_claim",
            "formula": "K_X=s_X/(4*pi*Z_X*G_obs)",
            "current_status": "MISSING_ALPHA_NORMALIZATION",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_ZX_LAMBDA_PREFACtOR_FORMULA_REGISTER.csv",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "row_id": "ASR1025_5_candidate_alpha",
            "quantity": "alpha_bulk(lambda_X)",
            "required_columns": "system_id;lambda_X;K_X;Qbar_XH;qbar_XT;alpha_bulk;alpha_bound;source_paths;valid_for_claim",
            "formula": "alpha_bulk(lambda_X)=K_X*Qbar_XH(lambda_X)*qbar_XT",
            "current_status": "SCHEMA_READY_VALUES_MISSING",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1024_ALPHA_COEFFICIENT_ROWS.csv",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def branch_verdict_rows() -> list[dict[str, str]]:
    return [
        {
            "verdict_id": "BV1025_0_Hessian_formula",
            "branch": "parent Hessian route",
            "status": "contract_derived_not_owned",
            "because": "the second-variation/range law is exact, but current files do not supply parent-signed Z_X, M_X^2, or units",
            "allowed_statement": "MTS has a precise Hessian contract for the local X route",
            "forbidden_statement": "MTS predicts lambda_X or passes R10/PPN from this route",
            "next_action": "derive parent field-space metric and Hessian eigenvalue, or return to source-zero/no-pole",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "verdict_id": "BV1025_1_beta3",
            "branch": "finite beta target",
            "status": "best_conditional_target_not_signed",
            "because": "beta=3 is a cleaner trace/eigenvalue target than direct range backsolve, but no parent spectrum theorem fixes it",
            "allowed_statement": "beta=3 is a private theorem target",
            "forbidden_statement": "beta=3 is a derived prediction",
            "next_action": "try to derive U''(0)=3 from a spatial trace parent block",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "verdict_id": "BV1025_2_alpha_source_row",
            "branch": "residual alpha fallback",
            "status": "schema_ready_values_missing",
            "because": "K_X, Qbar_XH, qbar_XT, Z_X, and lambda_X remain missing or unsigned",
            "allowed_statement": "fallback alpha rows are ready to receive sourced values",
            "forbidden_statement": "the fallback alpha row is evidence",
            "next_action": "fill only after parent metric/eigenvalue or source-current coefficients exist",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "verdict_id": "BV1025_3_coupling_gap",
            "branch": "coupling/source gap",
            "status": "still_live_and_now_localized",
            "because": "the missing coupling is the same place every route breaks: J_X/qbar_XT/Qbar_XH/K_X with one normalization",
            "allowed_statement": "the coupling gap is a concrete coefficient ledger problem",
            "forbidden_statement": "covariance or WEP alone silences the coupling",
            "next_action": "derive J_X=0 or source a bounded qbar_XT coefficient after Hessian owner attempt",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "verdict_id": "BV1025_4_next_target",
            "branch": "next target",
            "status": "parent_metric_or_source_zero",
            "because": "Z_X f_X^2 and U''(0) are the cleanest finite-route ownership objects; if they fail, source-zero is stronger",
            "allowed_statement": "1026 should attack the parent metric/eigenvalue theorem before any empirical alpha claim",
            "forbidden_statement": "run R10 as a claim before ownership rows exist",
            "next_action": "1026-Y5-R10-parent-metric-ZXfX2-beta-eigenvalue-or-source-zero-return.md",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def claim_gate_rows() -> list[dict[str, str]]:
    gates = [
        ("CG1025_0_sources_registered", "all cited source paths exist and expected needles are present", "true", "source register is intact", "false"),
        ("CG1025_1_second_variation_contract", "second-variation/range contract is written", "true", "the exact conditional law is derived", "false"),
        ("CG1025_2_parent_block_owned", "single parent action owns the X block", "false", "current sources are formula-only or conditional", "false"),
        ("CG1025_3_ZX_positive", "Z_X>0 is parent-signed", "false", "kinetic Hessian sign and units are missing", "false"),
        ("CG1025_4_MX2_positive", "M_X^2>0 is parent-signed", "false", "mass-gap/eigenvalue theorem is missing", "false"),
        ("CG1025_5_lambda_claim", "lambda_X is claim-grade", "false", "same-branch values and length units are missing", "false"),
        ("CG1025_6_alpha_source_claim", "alpha(lambda) row is claim-grade", "false", "K_X, Qbar_XH, qbar_XT, and bound comparison inputs are missing", "false"),
        ("CG1025_7_no_cancellation_guard", "no-cancellation guard active", "true", "unknown channels cannot cancel into a fake pass", "false"),
        ("CG1025_8_local_GR_claim", "local GR/Newton reduction is derived", "false", "Hessian/source/boundary/no-pole routes are still unsigned", "false"),
    ]
    return [
        {
            "gate_id": gate_id,
            "claim": claim,
            "gate_pass": gate_pass,
            "reason": reason,
            "claim_allowed": claim_allowed,
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
        for gate_id, claim, gate_pass, reason, claim_allowed in gates
    ]


def decision_rows() -> list[dict[str, str]]:
    return [
        {
            "decision_id": "DEC1025_0_exact_contract",
            "decision": "The exact scalar Hessian/range contract is now written.",
            "because": "second variation gives O_X, positivity conditions, and lambda_X=sqrt(Z_X/M_X^2).",
            "next_action": "do not re-derive the same formula; hunt the parent metric and eigenvalue owners",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC1025_1_no_claim",
            "decision": "Current MTS still does not own Z_X, M_X^2, lambda_X, or alpha.",
            "because": "all required values, signs, units, cross-term controls, and source coefficients are missing or conditional.",
            "next_action": "keep local R10/PPN/local-GR claims blocked",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC1025_2_beta3",
            "decision": "Beta=3 remains the cleanest finite theorem target, not evidence.",
            "because": "a spatial-trace eigenvalue route is less post-hoc than direct range backsolve.",
            "next_action": "derive U''(0)=3 and Z_X f_X^2=rho_vac^(1/2), or abandon finite-route promotion",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC1025_3_coupling",
            "decision": "The coupling gap is now a coefficient-normalization problem.",
            "because": "J_X, qbar_XT, Qbar_XH, and K_X all require the same parent normalization ledger.",
            "next_action": "after the metric/eigenvalue attempt, derive J_X=0 or fill a bounded qbar_XT row",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC1025_4_next_target",
            "decision": "Next target is parent metric/eigenvalue or source-zero return.",
            "because": "without Z_X f_X^2 and U''(0), the finite Hessian route cannot be promoted.",
            "next_action": "1026-Y5-R10-parent-metric-ZXfX2-beta-eigenvalue-or-source-zero-return.md",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def next_target_rows() -> list[dict[str, str]]:
    return [
        {
            "next_target": "1026-Y5-R10-parent-metric-ZXfX2-beta-eigenvalue-or-source-zero-return.md",
            "objective": "try to derive the parent field-space metric lock Z_X f_X^2=rho_vac^(1/2) and a beta eigenvalue, preferably U''(0)=3; if this cannot be signed, return to J_X/qbar_XT source-zero or bounded source rows",
            "include": "parent Ward/metric identity, X field-space norm, Hessian spectrum, beta=3 trace route, cross-Hessian block positivity, source-zero fallback, no-cancellation guard",
            "exclude": "direct range backsolve, rho_vac-alone lambda claim, placeholder alpha pass, WEP-only source-zero, R10/PPN/local-GR claim, GitHub action",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
    ]


def formalization_changed_after_start() -> list[Path]:
    if not FORMALIZATION.exists():
        return []
    changed = []
    for candidate in FORMALIZATION.rglob("*"):
        if candidate.is_file():
            modified = datetime.fromtimestamp(candidate.stat().st_mtime, timezone.utc)
            if modified >= STARTED:
                changed.append(candidate)
    return changed


def validation_rows(
    sources: list[dict[str, str]],
    derivation: list[dict[str, str]],
    hessian: list[dict[str, str]],
    locks: list[dict[str, str]],
    alpha: list[dict[str, str]],
    verdicts: list[dict[str, str]],
    gates: list[dict[str, str]],
    decisions: list[dict[str, str]],
    next_target: list[dict[str, str]],
) -> list[dict[str, str]]:
    changed = formalization_changed_after_start()
    derivation_required = {f"SV1025_{idx}_{name}" for idx, name in [
        (0, "local_block"),
        (1, "euler_operator"),
        (2, "Hessian_signs"),
        (3, "range_relation"),
        (4, "field_rescaling_guard"),
        (5, "sourcefree_nohair"),
        (6, "verdict"),
    ]}
    hessian_required = {f"PHA1025_{idx}_{name}" for idx, name in [
        (0, "branch_extremum"),
        (1, "ZX_positive"),
        (2, "MX2_positive"),
        (3, "lambda_units"),
        (4, "cross_Hessian"),
        (5, "source_current"),
        (6, "boundary_flux"),
        (7, "prefactor"),
        (8, "verdict"),
    ]}
    alpha_required = {f"ASR1025_{idx}_{name}" for idx, name in [
        (0, "bulk_Hessian"),
        (1, "field_metric_beta"),
        (2, "source_current"),
        (3, "Hamiltonian_projection"),
        (4, "green_prefactor"),
        (5, "candidate_alpha"),
    ]}
    checks = [
        ("V1025_0_sources_exist", all(flag(row["exists"]) and flag(row["needle_found"]) for row in sources), "all source paths exist and expected needles are present"),
        ("V1025_1_second_variation_complete", derivation_required.issubset({row["derivation_id"] for row in derivation}), "second-variation contract covers block, operator, signs, range, guard, no-hair, and verdict"),
        ("V1025_2_second_variation_nonclaim", all(row["valid_for_claim"] == "false" for row in derivation) and any(row["derivation_id"] == "SV1025_3_range_relation" and row["status"] == "EXACT_RELATION_DERIVED_NOT_OWNED" for row in derivation), "exact range law is derived but not promoted"),
        ("V1025_3_hessian_audit_complete", hessian_required.issubset({row["audit_id"] for row in hessian}), "parent Hessian audit covers extremum, signs, units, source, boundary, prefactor, and verdict"),
        ("V1025_4_hessian_claim_blocked", any(row["audit_id"] == "PHA1025_8_verdict" and row["status"] == "FAIL_CURRENT_CLAIM" for row in hessian), "parent Hessian ownership remains blocked"),
        ("V1025_5_normalization_locks_nonclaim", all(row["valid_for_claim"] == "false" for row in locks) and any(row["lock_id"] == "FNL1025_2_beta3" for row in locks), "field normalization locks retain beta3 as nonclaim target"),
        ("V1025_6_alpha_rows_nonclaim", alpha_required.issubset({row["row_id"] for row in alpha}) and all(row["valid_for_claim"] == "false" for row in alpha), "alpha source row schema is complete and nonclaim"),
        ("V1025_7_verdicts_complete", {"BV1025_0_Hessian_formula", "BV1025_1_beta3", "BV1025_2_alpha_source_row", "BV1025_3_coupling_gap", "BV1025_4_next_target"}.issubset({row["verdict_id"] for row in verdicts}), "branch verdicts are complete"),
        ("V1025_8_claim_gates_blocked", all(row["claim_allowed"] == "false" and row["valid_for_claim"] == "false" for row in gates), "all claim gates refuse promotion"),
        ("V1025_9_no_cancellation_guard", any(row["gate_id"] == "CG1025_7_no_cancellation_guard" and flag(row["gate_pass"]) for row in gates), "no-cancellation guard is active"),
        ("V1025_10_decision_written", any(row["decision_id"] == "DEC1025_4_next_target" for row in decisions), "1026 decision row is written"),
        ("V1025_11_next_target_written", len(next_target) == 1 and "1026-Y5-R10-parent-metric" in next_target[0]["next_target"], "1026 next target row is present"),
        ("V1025_12_formalization_untouched", len(changed) == 0, f"formalization-workbench modified-file count since script start is {len(changed)}"),
    ]
    rows = [{"check_id": check_id, "result": "pass" if passed else "fail", "detail": detail, "generated_utc": stamp()} for check_id, passed, detail in checks]
    rows.insert(0, {"check_id": "V1025_SUMMARY", "result": "pass" if all(row["result"] == "pass" for row in rows) else "fail", "detail": "1025 parent Hessian and alpha source row validation summary", "generated_utc": stamp()})
    return rows


def write_doc(
    sources: list[dict[str, str]],
    derivation: list[dict[str, str]],
    hessian: list[dict[str, str]],
    locks: list[dict[str, str]],
    alpha: list[dict[str, str]],
    verdicts: list[dict[str, str]],
    gates: list[dict[str, str]],
    decisions: list[dict[str, str]],
    next_target: list[dict[str, str]],
    validations: list[dict[str, str]],
) -> None:
    text = "\n".join(
        [
            "# 1025 Y5 R10 parent Hessian ZX MX2 range or alpha source row",
            "",
            "**Status:** The exact local second-variation contract is derived: the finite scalar route needs `Z_X>0`, `M_X^2>0`, `lambda_X=sqrt(Z_X/M_X^2)`, source control, and boundary control from one parent branch. Current MTS still does not own those Hessian signs, units, or coupling coefficients.",
            "",
            "**Claim ceiling:** no finite-range prediction, no alpha(lambda) pass, no R10/R11 pass, no PPN pass, and no local-GR/Newton reduction is allowed from 1025.",
            "",
            "## Source register",
            md_table(sources, ["source_id", "source_path", "exists", "needle_found", "role"]),
            "## Second variation derivation",
            md_table(derivation, ["derivation_id", "step", "mathematical_statement", "derived_result", "status", "missing_for_claim", "valid_for_claim"]),
            "## Parent Hessian audit",
            md_table(hessian, ["audit_id", "object", "required_evidence", "current_evidence", "status", "if_missing", "valid_for_claim"]),
            "## Field normalization locks",
            md_table(locks, ["lock_id", "target", "condition", "current_status", "allowed_use", "forbidden_use", "valid_for_claim"]),
            "## Alpha source row template",
            md_table(alpha, ["row_id", "quantity", "formula", "required_columns", "current_status", "source_path", "valid_for_claim"]),
            "## Branch verdicts",
            md_table(verdicts, ["verdict_id", "branch", "status", "because", "allowed_statement", "forbidden_statement", "next_action", "valid_for_claim"]),
            "## Claim gates",
            md_table(gates, ["gate_id", "claim", "gate_pass", "reason", "claim_allowed", "valid_for_claim"]),
            "## Decision ledger",
            md_table(decisions, ["decision_id", "decision", "because", "next_action", "valid_for_claim"]),
            "## Validation",
            md_table(validations, ["check_id", "result", "detail", "generated_utc"]),
            "## Next target",
            md_table(next_target, ["next_target", "objective", "include", "exclude", "valid_for_claim"]),
            "",
        ]
    )
    DOC.write_text(text, encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    sources = source_register_rows()
    derivation = second_variation_rows()
    hessian = parent_hessian_audit_rows()
    locks = normalization_lock_rows()
    alpha = alpha_source_rows()
    verdicts = branch_verdict_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_target = next_target_rows()
    validations = validation_rows(sources, derivation, hessian, locks, alpha, verdicts, gates, decisions, next_target)

    write_csv(OUT / "P8_Y5_R10_1025_SOURCE_REGISTER.csv", sources)
    write_csv(OUT / "P8_Y5_R10_1025_SECOND_VARIATION_DERIVATION.csv", derivation)
    write_csv(OUT / "P8_Y5_R10_1025_PARENT_HESSIAN_AUDIT.csv", hessian)
    write_csv(OUT / "P8_Y5_R10_1025_FIELD_NORMALIZATION_LOCKS.csv", locks)
    write_csv(OUT / "P8_Y5_R10_1025_ALPHA_SOURCE_ROW_TEMPLATE.csv", alpha)
    write_csv(OUT / "P8_Y5_R10_1025_BRANCH_VERDICTS.csv", verdicts)
    write_csv(OUT / "P8_Y5_R10_1025_CLAIM_GATES.csv", gates)
    write_csv(OUT / "P8_Y5_R10_1025_DECISION_LEDGER.csv", decisions)
    write_csv(OUT / "P8_Y5_R10_1025_NEXT_TARGET.csv", next_target)
    write_csv(OUT / "P8_Y5_BRR545_1025_VALIDATION.csv", validations)
    write_doc(sources, derivation, hessian, locks, alpha, verdicts, gates, decisions, next_target, validations)


if __name__ == "__main__":
    main()
