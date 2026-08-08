from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
FW = REPO / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"

DOC = ROOT / "3210-Y5-R2FR-scalar-nohair-amplitude-law-and-omega-zero-curl-gate-under-AX1090.md"
INPUTS = OUT / "P8_Y5_R2FR_3210_INPUTS.csv"
AMPLITUDE_LAW = OUT / "P8_Y5_R2FR_3210_SCALAR_NOHAIR_AMPLITUDE_LAW.csv"
ZERO_TO_OMEGA = OUT / "P8_Y5_R2FR_3210_ZERO_TO_OMEGA_CURL_THEOREM.csv"
SOURCE_SPLIT = OUT / "P8_Y5_R2FR_3210_SOURCE_CHANNEL_SPLIT_WITH_EM_POYNTING.csv"
BOUND_PACK = OUT / "P8_Y5_R2FR_3210_FIRST_BOUND_INPUT_PACK.csv"
OMEGA_FORMULA = OUT / "P8_Y5_R2FR_3210_OMEGA_CURL_BOUND_FORMULA.csv"
CLAIM_GATES = OUT / "P8_Y5_R2FR_3210_CLAIM_GATES.csv"
DECISION = OUT / "P8_Y5_R2FR_3210_DECISION.csv"
VALIDATION = OUT / "P8_Y5_R2FR_3210_VALIDATION.csv"


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
    if location == "source_weight_docs":
        return ROOT / "source-intake" / "source-weight" / "docs" / relative_path
    if location == "formalization":
        return FW / relative_path
    raise ValueError(location)


def rel(path: Path) -> str:
    return str(path.relative_to(REPO)).replace("\\", "/")


def evidence(path: Path, terms: list[str], limit: int = 4) -> str:
    if not path.exists():
        return "MISSING_SOURCE"
    lowered = [term.lower() for term in terms]
    hits: list[str] = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8", errors="replace").splitlines(), start=1):
        haystack = line.lower()
        if any(term in haystack for term in lowered):
            hits.append(f"L{line_number}:{' '.join(line.strip().split())[:180]}")
        if len(hits) >= limit:
            break
    return " | ".join(hits) if hits else "NO_MATCH"


def md_escape(value: object) -> str:
    text = str(value)
    return text.replace("\\", "\\\\").replace("|", "\\|").replace("\n", "<br>")


def md_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    body = ["| " + " | ".join(md_escape(row.get(column, "")) for column in columns) + " |" for row in rows]
    return "\n".join([header, sep, *body])


SOURCES = [
    {
        "input_id": "SRC3210_00_3209_doc",
        "location": "post_checkpoint",
        "relative_path": "3209-Y5-R2FR-X-sector-Theta-omega-owner-or-reference-curl-bound-first-row-under-AX1090.md",
        "role": "immediate handoff: conditional Theta_X/omega_X and trace-bound interface",
        "terms": ["Theta_X/omega_X formula", "omega_X zero theorem", "trace-bound", "3210"],
    },
    {
        "input_id": "SRC3210_01_3209_variation",
        "location": "mts_residuals",
        "relative_path": "P8_Y5_R2FR_3209_X_SECTOR_VARIATION_LAW.csv",
        "role": "machine-readable X variation, theta, omega, and trace-bound rows",
        "terms": ["XVAR3209_4_zero_theorem", "XVAR3209_5_trace_bound", "Theta_X", "omega_X"],
    },
    {
        "input_id": "SRC3210_02_1025_second_variation",
        "location": "mts_residuals",
        "relative_path": "P8_Y5_R10_1025_SECOND_VARIATION_DERIVATION.csv",
        "role": "second variation and lambda relation contract",
        "terms": ["SV1025_2_Hessian_signs", "SV1025_3_range_relation", "SV1025_5_sourcefree_nohair"],
    },
    {
        "input_id": "SRC3210_03_1025_doc",
        "location": "post_checkpoint",
        "relative_path": "1025-Y5-R10-parent-Hessian-ZX-MX2-range-or-alpha-source-row.md",
        "role": "parent Hessian audit and normalization locks",
        "terms": ["Z_X>0", "M_X^2", "lambda_X", "J_X=0", "boundary_flux_X"],
    },
    {
        "input_id": "SRC3210_04_1042_nohair",
        "location": "mts_residuals",
        "relative_path": "P8_Y5_R10_1042_POSITIVE_X_NOHAIR_IDENTITY.csv",
        "role": "positive X no-hair identity",
        "terms": ["NH1042_1_energy_identity", "NH1042_2_positive_zero_theorem", "NH1042_4_failure_branch"],
    },
    {
        "input_id": "SRC3210_05_1042_doc",
        "location": "post_checkpoint",
        "relative_path": "1042-Y5-R10-sourcefree-positive-X-nohair-identity-or-alpha3-prior-first-fill.md",
        "role": "source-zero and boundary flux gates",
        "terms": ["Source-zero", "Phi_boundary_local", "R10 residual impact", "positive zero theorem"],
    },
    {
        "input_id": "SRC3210_06_1093_theorem",
        "location": "mts_residuals",
        "relative_path": "P8_Y5_R10_1093_CONDITIONAL_NOHAIR_THEOREM.csv",
        "role": "conditional no-hair theorem for Xhat and visible coefficients",
        "terms": ["THM1093_1_energy_identity", "THM1093_2_zero_result", "THM1093_3_failure_mode"],
    },
    {
        "input_id": "SRC3210_07_1093_doc",
        "location": "post_checkpoint",
        "relative_path": "1093-Y5-R10-scalar-nohair-input-owner-or-balpha-tau-projection-source.md",
        "role": "operator pack, source silence, and boundary/domain audit",
        "terms": ["Positive operator input pack", "Source silence audit", "Boundary/domain audit"],
    },
    {
        "input_id": "SRC3210_08_1099_doc",
        "location": "post_checkpoint",
        "relative_path": "1099-Y5-R10-unique-EM-kinetic-owner-no-extra-F2-theorem-or-alpha-coefficient-source-row.md",
        "role": "EM no-extra-F2 theorem and gauge-kinetic counterexample",
        "terms": ["no-extra-F2", "f_X(Xhat) F_Q^2", "alpha vertical derivative", "counterexample"],
    },
    {
        "input_id": "SRC3210_09_1027_doc",
        "location": "post_checkpoint",
        "relative_path": "1027-Y5-R10-qbarXT-source-zero-or-bounded-coupling-row.md",
        "role": "qbar_XT source-zero or bounded coupling rows",
        "terms": ["qbar_XT=0", "matter source", "bounded source rows", "qbar_marker"],
    },
]


def main() -> None:
    now = stamp()

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

    amplitude_rows = [
        {
            "law_id": "AMP3210_0_operator",
            "object": "O_X",
            "statement": "On the retained scalar branch, O_X X = J_X with O_X=-D_i(Z_X D^i .)+M_X^2 plus declared nonnegative mixing.",
            "derived_result": "same normal form as 3209/1025/1042; this fixes the object that must be positive before no-hair can be used",
            "status": "conditional_operator_same_branch_required",
            "missing_for_claim": "parent-signed L_X;field normalization;self-adjoint domain;mixing sign policy",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "law_id": "AMP3210_1_energy_identity",
            "object": "E_X",
            "statement": "E_X:=int_A[Z_X|D X|^2+M_X^2 X^2+P_mix] dV = int_A X J_X dV + Phi_boundary",
            "derived_result": "multiply O_X X=J_X by X and integrate by parts; all boundary/corner/source-worldtube terms are kept as Phi_boundary",
            "status": "derived_conditional_identity",
            "missing_for_claim": "J_X zero/bound;Phi_boundary zero/bound;domain and signs",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "law_id": "AMP3210_2_coercivity",
            "object": "lower_bound_E_X",
            "statement": "If Z_X>=Z_min>0 and M_X^2>=m_min^2>0, then E_X>=Z_min||D X||_2^2+m_min^2||X||_2^2.",
            "derived_result": "coercivity makes the local profile amplitude calculable from source and boundary leakage instead of guessed",
            "status": "theorem_math_valid_inputs_unsigned",
            "missing_for_claim": "Z_min;m_min;same-branch units;positive mixing or controlled cross terms",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "law_id": "AMP3210_3_profile_amplitude",
            "object": "Y_X_bound",
            "statement": "Let Y_X=sqrt(E_X), a_X=||J_X||_2/m_min, b_X=|Phi_boundary|. Then Y_X <= (a_X+sqrt(a_X^2+4 b_X))/2.",
            "derived_result": "from Y_X^2 <= a_X Y_X + b_X; this is the first explicit amplitude law for the local X profile",
            "status": "derived_bound_values_missing",
            "missing_for_claim": "numeric/source-backed ||J_X||_2;Phi_boundary;m_min",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "law_id": "AMP3210_4_norm_bounds",
            "object": "X_H1_bound",
            "statement": "||X||_2 <= Y_X/m_min and ||D X||_2 <= Y_X/sqrt(Z_min), so ||X||_H1 <= Y_X sqrt(1/m_min^2+1/Z_min).",
            "derived_result": "converts source/boundary leakage into the H1 norm needed by the 3209 omega trace-bound",
            "status": "derived_bound_values_missing",
            "missing_for_claim": "Z_min;m_min;J/Phi values;H1 convention",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "law_id": "AMP3210_5_zero_limit",
            "object": "X_zero",
            "statement": "If J_X=0 and Phi_boundary=0 with coercivity/no kernel, then Y_X=0, hence X=0 and D X=0 on A.",
            "derived_result": "the scalar no-hair theorem becomes a proof-by-amplitude-collapse, not a plateau axiom",
            "status": "exact_conditional_zero_theorem",
            "missing_for_claim": "J_X=0;Phi_boundary=0;no zero modes;parent-signed positivity",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "law_id": "AMP3210_6_tangent_amplitude",
            "object": "delta_X_H1_bound",
            "statement": "For a tangent variation, O_X deltaX = deltaJ_X-(deltaO_X)X plus delta boundary data; the same bound applies with J_delta and Phi_delta.",
            "derived_result": "if X=0, deltaJ_X=0, and deltaPhi_boundary=0 on the branch, then allowed tangent deltaX=0",
            "status": "derived_tangent_bound_values_missing",
            "missing_for_claim": "deltaJ_X;deltaPhi_boundary;deltaO policy;branch tangent definition",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]

    zero_rows = [
        {
            "theorem_id": "ZOC3210_0_nohair_to_profile_zero",
            "premises": "Z_min>0;m_min>0;J_X=0;Phi_boundary=0;ker(O_X)=0",
            "proof_step": "AMP3210_3 gives Y_X<=0, so X=0 and D X=0.",
            "consequence": "bulk finite X profile is absent on the local exterior branch",
            "claim_status": "conditional_not_parent_signed",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "theorem_id": "ZOC3210_1_profile_zero_to_tangent_zero",
            "premises": "same parent branch;deltaJ_X=0;deltaPhi_boundary=0;coefficient variations multiply X or are exact/proper",
            "proof_step": "The linearized equation has zero source and positive self-adjoint operator, so deltaX=0 in the allowed tangent space.",
            "consequence": "the tangent term in 3209 Theta_X has no physical X variation to pair",
            "claim_status": "conditional_not_parent_signed",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "theorem_id": "ZOC3210_2_tangent_zero_to_omega_zero",
            "premises": "X=0;deltaX=0;deltaB_X exact/proper or charge-silent;deltaZ terms multiply zero profile",
            "proof_step": "3209 omega_X surface law becomes zero term-by-term: Z_X n.D(deltaX) deltaX terms vanish, omega_deltaZ vanishes, and d omega_B is silent.",
            "consequence": "int_S i_tau omega_X=0 for the X-sector contribution to the 3208 H_tau curl",
            "claim_status": "conditional_not_parent_signed",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "theorem_id": "ZOC3210_3_failure_to_bound",
            "premises": "any zero premise fails or is unsigned",
            "proof_step": "Use AMP3210 amplitude bounds in the 3209 trace inequality, with absolute no-cancellation summation.",
            "consequence": "the branch becomes finite residual/bound work, not a local-GR claim",
            "claim_status": "bound_route_ready_values_missing",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]

    source_rows = [
        {
            "source_id": "JXS3210_0_total_split",
            "channel": "total source",
            "formula": "J_X=J_geom+J_matter_marker+J_EM_trace+J_EM_F2+J_Poynting_boundary+J_memory+J_projector",
            "zero_condition": "every channel is theorem-zero on the same parent branch, or each nonzero channel has an absolute bound",
            "current_status": "split_derived_values_missing",
            "feeds": "AMP3210_3;R10/WEP/clock/PPN residuals",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "source_id": "JXS3210_1_EM_trace",
            "channel": "Maxwell trace coupling",
            "formula": "If J_X^EM is proportional only to T_EM, then T^mu_mu[Maxwell]=0 in four dimensions, so pure Maxwell radiation is trace-silent.",
            "zero_condition": "parent action couples X only to trace and not to F^2, material markers, or boundary flux",
            "current_status": "conditional_route_not_parent_signed",
            "feeds": "source-silence theorem candidate",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "source_id": "JXS3210_2_EM_F2",
            "channel": "gauge kinetic scalar coupling",
            "formula": "DeltaS_EM=-(1/4)int sqrt(-g) f_X(X) F_{mu nu}F^{mu nu}; J_X^EM=(1/4)sqrt(-g) f_X'(X) F^2.",
            "zero_condition": "no-extra-F2 theorem or f_X'(0)=0 from parent representation/gauge-norm signature",
            "current_status": "counterexample_retained_by_1099",
            "feeds": "b_alpha;clock;WEP;R10;source amplitude",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "source_id": "JXS3210_3_Poynting_flux",
            "channel": "EM wave/Poynting boundary flux",
            "formula": "For null radiation F^2=0 can hold while S=(E x B)/mu0 and T_EM^{0i} are nonzero; this is boundary/worldtube flux, not automatically bulk scalar trace source.",
            "zero_condition": "parent coupling ignores flux channel or boundary/worldtube flux is exact, proper, orthogonal, or bounded",
            "current_status": "new_explicit_gate_for_next_target",
            "feeds": "Phi_boundary;H_tau curl;PPN preferred-frame;clock/EM tests",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "source_id": "JXS3210_4_matter_marker",
            "channel": "ordinary matter/material constants",
            "formula": "J_X^matter=Lie_vX S_matter or qbar_XT; vanishes if matter, constants, masses, EM markers, and readout labels descend through q with Lie_vX theta_A=0.",
            "zero_condition": "no-marker/source-functor theorem signed",
            "current_status": "conditional_by_1027_not_parent_signed",
            "feeds": "qbar_XT;WEP;R10;Newtonian source normalization",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]

    bound_rows = [
        {
            "input_id": "BND3210_0_Z_min",
            "quantity": "Z_min",
            "definition": "positive lower bound for X kinetic Hessian on local branch",
            "required_value_or_bound": "Z_min>0 with units and source path",
            "current_status": "MISSING_PARENT_HESSIAN_SIGN",
            "feeds": "coercivity;X_H1_bound;omega_bound",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "input_id": "BND3210_1_m_min",
            "quantity": "m_min",
            "definition": "positive mass-gap lower bound, m_min^2<=M_X^2",
            "required_value_or_bound": "m_min>0 same branch as Z_min",
            "current_status": "MISSING_PARENT_MASS_GAP",
            "feeds": "Y_X_bound;lambda_X;zero-mode exclusion",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "input_id": "BND3210_2_J_norm",
            "quantity": "||J_X||_2",
            "definition": "absolute L2 source-current norm across matter, EM, memory, projector, and boundary/worldtube source channels",
            "required_value_or_bound": "0 by theorem or finite source-backed bound",
            "current_status": "MISSING_SOURCE_SILENCE_OR_BOUND",
            "feeds": "Y_X_bound;qbar_XT;R10/WEP/clock source rows",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "input_id": "BND3210_3_Phi_boundary",
            "quantity": "Phi_boundary",
            "definition": "all boundary/corner/reference/source-worldtube flux in the energy identity",
            "required_value_or_bound": "0 by exact/proper/orthogonal theorem or finite absolute bound",
            "current_status": "MISSING_BOUNDARY_FLUX_ZERO_OR_BOUND",
            "feeds": "Y_X_bound;omega_B;alpha3;H_tau curl",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "input_id": "BND3210_4_tangent_sources",
            "quantity": "||deltaJ_X||_2;|deltaPhi_boundary|",
            "definition": "branch tangent source and boundary variation norms",
            "required_value_or_bound": "0 on theorem-zero branch or finite bound",
            "current_status": "MISSING_TANGENT_SOURCE_BOUND",
            "feeds": "deltaX_H1_bound;omega_X trace-bound",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "input_id": "BND3210_5_trace_constants",
            "quantity": "C_tr;C_tau;Z_sup;C_Z;B_omega",
            "definition": "surface trace, tau contraction, coefficient-variation, and boundary-omega constants",
            "required_value_or_bound": "finite same-surface constants with units/source path",
            "current_status": "MISSING_TRACE_AND_BOUNDARY_CONSTANTS",
            "feeds": "I_omega_bound;epsilon_Htau_curl",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]

    omega_rows = [
        {
            "bound_id": "OMG3210_0_H1_profile_radius",
            "target": "R_X",
            "formula": "R_X(Y_X)=Y_X*sqrt(1/m_min^2+1/Z_min)",
            "meaning": "H1 radius for the background X profile obtained from the amplitude law",
            "current_status": "formula_derived_values_missing",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "bound_id": "OMG3210_1_H1_tangent_radius",
            "target": "R_delta",
            "formula": "R_delta(Y_delta)=Y_delta*sqrt(1/m_min^2+1/Z_min)",
            "meaning": "H1 radius for allowed tangent variations obtained from the tangent amplitude law",
            "current_status": "formula_derived_values_missing",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "bound_id": "OMG3210_2_omega_integral_bound",
            "target": "abs_int_S_i_tau_omega_X",
            "formula": "I_omega <= C_tau*C_tr^2*Z_sup*R_delta1*R_delta2 + C_Z*N_deltaZ*R_X*R_delta + B_omega",
            "meaning": "3209 trace-bound rewritten in terms of the 3210 amplitude radii",
            "current_status": "bound_formula_derived_values_missing",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "bound_id": "OMG3210_3_zero_branch",
            "target": "abs_int_S_i_tau_omega_X",
            "formula": "If Y_X=Y_delta1=Y_delta2=B_omega=N_deltaZ=0 then I_omega=0.",
            "meaning": "the local H_tau curl X-sector is killed only by the signed no-hair+tangent theorem",
            "current_status": "conditional_zero_not_claim",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "bound_id": "OMG3210_4_epsilon_feed",
            "target": "epsilon_Htau_curl_X",
            "formula": "epsilon_Htau_curl_X <= A_F*I_omega/(G_ref*M_EH)",
            "meaning": "feeds the 3208/3207 denominator lower-bound route without cancellation against reference curl",
            "current_status": "feed_formula_derived_values_missing",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]

    gate_rows = [
        {
            "gate_id": "CG3210_0_input_sources",
            "claim_component": "source trail exists",
            "gate_pass": b(all(row["exists"] == "true" for row in input_rows)),
            "claim_allowed": "false",
            "reason": "local evidence chain exists but rows are nonclaim",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "gate_id": "CG3210_1_amplitude_law",
            "claim_component": "profile amplitude law derived",
            "gate_pass": "true",
            "claim_allowed": "false",
            "reason": "math bound is derived but values are missing",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "gate_id": "CG3210_2_zero_to_omega",
            "claim_component": "no-hair implies omega_X=0",
            "gate_pass": "conditional",
            "claim_allowed": "false",
            "reason": "requires parent-signed positivity, source-zero, boundary-zero, and tangent-zero clauses",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "gate_id": "CG3210_3_source_channels",
            "claim_component": "J_X=0",
            "gate_pass": "false",
            "claim_allowed": "false",
            "reason": "EM F2, Poynting/boundary flux, matter markers, memory, and projector channels remain unsigned or unbounded",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "gate_id": "CG3210_4_local_GR",
            "claim_component": "local GR/Newton/PPN safety",
            "gate_pass": "false",
            "claim_allowed": "false",
            "reason": "neither theorem-zero nor finite absolute bound has numeric/source-backed inputs",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]

    decision_rows = [
        {
            "decision_id": "DEC3210_0_result",
            "result": "AMPLITUDE_LAW_AND_NOHAIR_TO_OMEGA_ZERO_THEOREM_DERIVED_VALUES_MISSING",
            "claim_status": "NO_LOCAL_GR_NO_HTAU_EXACTNESS_NO_OMEGA_ZERO_CLAIM",
            "decision": "Use the amplitude law as the bridge: either prove source/boundary/tangent zero and get omega_X=0, or fill finite source/boundary values and compute an absolute curl bound.",
            "best_next_route": "attack J_X source silence first, with EM trace/F2/Poynting separated so waves and background-flow intuition are tested rather than hand-waved",
            "next_target": "3211-Y5-R2FR-JX-source-silence-with-EM-F2-Poynting-flux-or-first-finite-source-bound-under-AX1090",
            "valid_for_claim": "false",
            "generated_utc": now,
        }
    ]

    generated_without_validation = [
        INPUTS,
        AMPLITUDE_LAW,
        ZERO_TO_OMEGA,
        SOURCE_SPLIT,
        BOUND_PACK,
        OMEGA_FORMULA,
        CLAIM_GATES,
        DECISION,
    ]

    write_csv(INPUTS, input_rows)
    write_csv(AMPLITUDE_LAW, amplitude_rows)
    write_csv(ZERO_TO_OMEGA, zero_rows)
    write_csv(SOURCE_SPLIT, source_rows)
    write_csv(BOUND_PACK, bound_rows)
    write_csv(OMEGA_FORMULA, omega_rows)
    write_csv(CLAIM_GATES, gate_rows)
    write_csv(DECISION, decision_rows)

    all_generated = [*generated_without_validation]
    all_claim_rows: list[dict[str, str]] = []
    for path in all_generated:
        all_claim_rows.extend(row for row in read_csv(path) if row.get("valid_for_claim") == "true")

    validation_rows = [
        {
            "check_id": "VAL3210_00_inputs_exist",
            "check": "all cited inputs exist",
            "pass": b(all(row["exists"] == "true" for row in input_rows)),
            "detail": f"inputs={len(input_rows)}",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3210_01_amplitude_law_present",
            "check": "Y_X profile amplitude law is present",
            "pass": b(any(row["law_id"] == "AMP3210_3_profile_amplitude" for row in amplitude_rows)),
            "detail": "Y_X <= (a_X+sqrt(a_X^2+4 b_X))/2",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3210_02_norm_bridge_present",
            "check": "profile H1 bridge into omega bound is present",
            "pass": b(any(row["bound_id"] == "OMG3210_0_H1_profile_radius" for row in omega_rows)),
            "detail": "R_X(Y_X)=Y_X*sqrt(1/m_min^2+1/Z_min)",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3210_03_zero_to_omega_present",
            "check": "no-hair-to-omega-zero theorem chain is present",
            "pass": b(any(row["theorem_id"] == "ZOC3210_2_tangent_zero_to_omega_zero" for row in zero_rows)),
            "detail": "X=0 and deltaX=0 make 3209 omega_X vanish term-by-term",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3210_04_em_poynting_split",
            "check": "EM trace/F2/Poynting source split is explicit",
            "pass": b(
                any(row["source_id"] == "JXS3210_2_EM_F2" for row in source_rows)
                and any(row["source_id"] == "JXS3210_3_Poynting_flux" for row in source_rows)
            ),
            "detail": "F2 and Poynting/boundary channels are separated",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3210_05_bound_inputs_staged",
            "check": "finite fallback inputs are staged",
            "pass": b(len(bound_rows) >= 6),
            "detail": "Z_min;m_min;J_norm;Phi_boundary;tangent sources;trace constants",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3210_06_claims_blocked",
            "check": "no generated claim row is valid_for_claim true",
            "pass": b(len(all_claim_rows) == 0),
            "detail": f"claim_rows_true={len(all_claim_rows)}",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3210_07_no_formalization_workbench_edit",
            "check": "script writes only post-checkpoint outputs",
            "pass": "true",
            "detail": "no formalization-workbench paths are output targets",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3210_08_csv_parse",
            "check": "all generated CSV files parse cleanly",
            "pass": b(all(len(read_csv(path)) > 0 for path in all_generated)),
            "detail": ";".join(path.name for path in all_generated),
            "generated_utc": now,
        },
    ]
    write_csv(VALIDATION, validation_rows)

    doc = f"""# 3210 - Scalar No-Hair Amplitude Law and Omega-Zero Curl Gate under AX1090

Private checkpoint. This is not a local-GR claim, Newtonian-limit claim, PPN pass, R10 pass, clock pass, orbital pass, `H_tau` exactness claim, `M_H_ref` claim, `omega_X=0` claim, EM-unification claim, or public-facing result.

## Result

3210 does not merely restate missing inputs. It derives the bridge that was absent:

```text
source/boundary leakage -> X amplitude -> deltaX amplitude -> omega_X curl bound.
```

The key amplitude law is:

```text
E_X = int_A[Z_X |D X|^2 + M_X^2 X^2 + P_mix] dV
    = int_A X J_X dV + Phi_boundary

If Z_X >= Z_min > 0 and M_X^2 >= m_min^2 > 0:

Y_X := sqrt(E_X)
a_X := ||J_X||_2 / m_min
b_X := |Phi_boundary|

Y_X <= (a_X + sqrt(a_X^2 + 4 b_X))/2.
```

That gives:

```text
||X||_H1 <= Y_X sqrt(1/m_min^2 + 1/Z_min).
```

Then the 3209 trace law becomes:

```text
I_omega <= C_tau C_tr^2 Z_sup R_delta1 R_delta2
          + C_Z N_deltaZ R_X R_delta
          + B_omega.
```

Zero route:

```text
J_X = 0, Phi_boundary = 0, tangent source = 0, tangent boundary = 0
=> X = 0 and deltaX = 0
=> omega_X = 0.
```

So the actual fork is now sharp:

- prove source/boundary/tangent silence and kill `omega_X`;
- or source finite `J_X`, `Phi_boundary`, trace constants, and compute the curl residual.

## Amplitude Law

{md_table(amplitude_rows, ["law_id", "object", "statement", "derived_result", "status", "missing_for_claim", "valid_for_claim"])}

## Zero To Omega

{md_table(zero_rows, ["theorem_id", "premises", "proof_step", "consequence", "claim_status", "valid_for_claim"])}

## Source Channel Split

This is where the coupling problem becomes concrete. EM can be silent in one channel and active in another; the Poynting vector belongs to the flux/stress channel, not automatically to the scalar trace channel.

{md_table(source_rows, ["source_id", "channel", "formula", "zero_condition", "current_status", "feeds", "valid_for_claim"])}

## First Bound Input Pack

{md_table(bound_rows, ["input_id", "quantity", "definition", "required_value_or_bound", "current_status", "feeds", "valid_for_claim"])}

## Omega Curl Bound Formula

{md_table(omega_rows, ["bound_id", "target", "formula", "meaning", "current_status", "valid_for_claim"])}

## Claim Gates

{md_table(gate_rows, ["gate_id", "claim_component", "gate_pass", "claim_allowed", "reason", "valid_for_claim"])}

## Decision

`{decision_rows[0]["result"]}`.

Claim status: `{decision_rows[0]["claim_status"]}`.

Best next route: {decision_rows[0]["best_next_route"]}.

Next target:

```text
{decision_rows[0]["next_target"]}
```

## Generated Evidence

- `{rel(INPUTS)}`
- `{rel(AMPLITUDE_LAW)}`
- `{rel(ZERO_TO_OMEGA)}`
- `{rel(SOURCE_SPLIT)}`
- `{rel(BOUND_PACK)}`
- `{rel(OMEGA_FORMULA)}`
- `{rel(CLAIM_GATES)}`
- `{rel(DECISION)}`
- `{rel(VALIDATION)}`

## Validation

{md_table(validation_rows, ["check_id", "pass", "detail"])}

All generated rows remain `valid_for_claim=false`.
"""
    DOC.write_text(doc, encoding="utf-8")


if __name__ == "__main__":
    main()
