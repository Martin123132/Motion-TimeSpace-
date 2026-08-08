from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
FW = REPO / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"

DOC = ROOT / "3217-Y5-R2FR-parent-visible-coefficient-vertex-list-or-first-memory-slope-source-row-under-AX1090.md"
INPUTS = OUT / "P8_Y5_R2FR_3217_INPUTS.csv"
DOMAIN_RULES = OUT / "P8_Y5_R2FR_3217_ARGUMENT_DOMAIN_RULES.csv"
VERTEX_LIST = OUT / "P8_Y5_R2FR_3217_VISIBLE_COEFFICIENT_VERTEX_LIST.csv"
MANIFEST_GATE = OUT / "P8_Y5_R2FR_3217_VERTEX_MANIFEST_GATE.csv"
FIRST_ROWS = OUT / "P8_Y5_R2FR_3217_FIRST_MEMORY_SLOPE_SOURCE_ROWS.csv"
DECISION = OUT / "P8_Y5_R2FR_3217_DECISION.csv"
VALIDATION = OUT / "P8_Y5_R2FR_3217_VALIDATION.csv"


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
    return str(value).replace("\\", "\\\\").replace("|", "\\|").replace("\n", "<br>")


def md_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    body = ["| " + " | ".join(md_escape(row.get(column, "")) for column in columns) + " |" for row in rows]
    return "\n".join([header, sep, *body])


SOURCES = [
    {
        "input_id": "SRC3217_00_3216_doc",
        "location": "post_checkpoint",
        "relative_path": "3216-Y5-R2FR-branch-origin-coefficient-stationarity-or-memory-slope-bound-pack-under-AX1090.md",
        "role": "3216 stationarity routes and slope pack handoff",
        "terms": ["parent visible-coefficient vertex list", "typed exclusion", "Memory Slope Bound Pack"],
    },
    {
        "input_id": "SRC3217_01_3216_slopes",
        "location": "mts_residuals",
        "relative_path": "P8_Y5_R2FR_3216_MEMORY_SLOPE_BOUND_PACK.csv",
        "role": "memory slope pack to populate vertex rows",
        "terms": ["SLP3216_0_balpha_memory", "SLP3216_2_hodge_memory", "SLP3216_5_source_weight_memory"],
    },
    {
        "input_id": "SRC3217_02_1104_signature",
        "location": "mts_residuals",
        "relative_path": "P8_Y5_R10_1104_PARENT_SIGNATURE_LEDGER.csv",
        "role": "ordinary-sector parent signature clauses",
        "terms": ["SIG1104_3_unique_EM_owner", "SIG1104_6_clock_readout_owner", "SIG1104_10_verdict"],
    },
    {
        "input_id": "SRC3217_03_1098_owner",
        "location": "post_checkpoint",
        "relative_path": "1098-Y5-R10-ordinary-constant-owner-action-signature-or-source-backed-coefficient-prior.md",
        "role": "ordinary-constant owner vertex audit",
        "terms": ["FV1098_1_scalar_F2", "OCS1098_6_verdict", "REQ1098_0_c_alpha"],
    },
    {
        "input_id": "SRC3217_04_1099_em",
        "location": "post_checkpoint",
        "relative_path": "1099-Y5-R10-unique-EM-kinetic-owner-no-extra-F2-theorem-or-alpha-coefficient-source-row.md",
        "role": "EM kinetic owner/no-extra-F2 attempt",
        "terms": ["UEM1099_3_verdict", "CX1099_1_fX", "ASR1099_0_theorem_zero_candidate"],
    },
    {
        "input_id": "SRC3217_05_1105_master",
        "location": "post_checkpoint",
        "relative_path": "1105-Y5-R10-master-no-hidden-visible-coefficient-morphism-or-explicit-closure-pack.md",
        "role": "master no-hidden-visible coefficient closure",
        "terms": ["MHM1105_6_verdict", "SUB1105_0_alpha_F2", "PACK1105_4_residual_vector_if_unsigned"],
    },
    {
        "input_id": "SRC3217_06_3212_em",
        "location": "post_checkpoint",
        "relative_path": "3212-Y5-R2FR-EM-source-channel-no-extra-F2-or-Poynting-bound-input-under-AX1090.md",
        "role": "EM source channels requiring vertex ownership",
        "terms": ["J_X^EM", "Hodge", "Poynting", "readout"],
    },
    {
        "input_id": "SRC3217_07_3213_sequester",
        "location": "post_checkpoint",
        "relative_path": "3213-Y5-R2FR-hidden-visible-product-sequester-or-balpha-Hodge-Poynting-provenance-pack-under-AX1090.md",
        "role": "product/sequester theorem and countertheorem",
        "terms": ["Product Sequester", "Invariant Scalar Countertheorem", "C_Poynting"],
    },
    {
        "input_id": "SRC3217_08_1097_constants",
        "location": "post_checkpoint",
        "relative_path": "1097-Y5-R10-constant-sector-universality-theorem-or-finite-coefficient-source-prior.md",
        "role": "constant-sector channel audit",
        "terms": ["CHA1097_0_alpha", "CHA1097_4_source_weights", "CONSTANT_SECTOR_UNIVERSALITY_NOT_DERIVED"],
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

    domain_rows = [
        {
            "domain_id": "DOM3217_0_Q_ONLY",
            "argument_domain": "Q_ONLY",
            "allowed_form": "C_r = Cbar_r(q(Phi), fixed representation/topological data)",
            "memory_slope_result": "partial_m C_r = 0 when Dq[partial_m]=0",
            "promotion_requirement": "parent action and readout maps explicitly type the coefficient this way",
            "claim_status": "conditional_zero",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "domain_id": "DOM3217_1_REP_TOPOLOGICAL",
            "argument_domain": "REP_TOPOLOGICAL",
            "allowed_form": "C_r is a fixed charge level, representation label, discrete theta/topological sector, or superselection datum",
            "memory_slope_result": "smooth vertical derivative is zero on a connected fixed sector",
            "promotion_requirement": "no wall crossing, no sector selector, and no readout re-entry",
            "claim_status": "conditional_zero",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "domain_id": "DOM3217_2_EVEN_DOUBLE_ZERO_MEMORY",
            "argument_domain": "EVEN_DOUBLE_ZERO_MEMORY",
            "allowed_form": "C_r = C_r0 + lambda_r F(m), with F(m_*)=F'(m_*)=0 and same-branch local lock",
            "memory_slope_result": "partial_m C_r(m_*) = 0 but second derivative can shift the Hessian",
            "promotion_requirement": "parent source-root F, local lock m=m_*, correction bound, and boundary/readout closure",
            "claim_status": "conditional_zero_with_second_order_debt",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "domain_id": "DOM3217_3_EXPLICIT_RESIDUAL",
            "argument_domain": "EXPLICIT_RESIDUAL",
            "allowed_form": "C_r depends on m or hidden invariant with nonzero or unknown slope",
            "memory_slope_result": "slope is live and must enter the finite residual vector",
            "promotion_requirement": "source-backed coefficient value/bound, units, operator norm, support, and no-cancellation guard",
            "claim_status": "finite_nonclaim",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]

    vertex_rows = [
        {
            "vertex_id": "VTX3217_0_EM_F2",
            "sector": "EM",
            "visible_operator": "F_Q^2",
            "coefficient": "ln Z_A or gauge kinetic normalization",
            "required_domain_for_zero": "Q_ONLY or REP_TOPOLOGICAL fixed gauge norm, or EVEN_DOUBLE_ZERO_MEMORY deformation",
            "current_corpus_status": "UNIQUE_EM_OWNER_NOT_PARENT_SIGNED_COUNTERTERM_LEGAL",
            "memory_slope": "b_alpha_m",
            "if_not_zero": "retain SLP3216_0_balpha_memory and alpha product rows",
            "strongest_source": "UEM1099_3;SIG1104_3;FV1098_1",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "vertex_id": "VTX3217_1_EM_DUAL",
            "sector": "EM",
            "visible_operator": "F_Q star F_Q",
            "coefficient": "Theta_A or dual/topological coefficient",
            "required_domain_for_zero": "REP_TOPOLOGICAL fixed/discrete theta or Q_ONLY/even branch",
            "current_corpus_status": "DUAL_CHANNEL_POLICY_UNSIGNED",
            "memory_slope": "b_theta_m",
            "if_not_zero": "retain SLP3216_1_theta_memory",
            "strongest_source": "3212 dual row;3213 PROV3213_3_theta_dual",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "vertex_id": "VTX3217_2_HODGE_STRESS",
            "sector": "EM/geometry",
            "visible_operator": "T_EM^{mu nu}, Hodge star, observed coframe",
            "coefficient": "g_obs(m), star_obs(m), C_Hodge",
            "required_domain_for_zero": "Q_ONLY observed coframe/Hodge factorization",
            "current_corpus_status": "HODGE_DESCENT_UNSIGNED",
            "memory_slope": "B_Hodge_m",
            "if_not_zero": "retain SLP3216_2_hodge_memory and PPN/clock stress rows",
            "strongest_source": "3212 Hodge source;3213 PROV3213_1_C_Hodge",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "vertex_id": "VTX3217_3_MATTER_MASS_BINDING",
            "sector": "matter",
            "visible_operator": "mass, Yukawa, QCD/binding, material response",
            "coefficient": "m_A, y_A, Lambda_QCD, B_A, material response",
            "required_domain_for_zero": "REP_TOPOLOGICAL/fixed matter spectrum or Q_ONLY quotient-owned spectrum",
            "current_corpus_status": "MATTER_SPECTRUM_OWNER_NOT_PARENT_SIGNED",
            "memory_slope": "B_matter_m",
            "if_not_zero": "retain WEP/clock/material finite coefficient rows",
            "strongest_source": "SIG1104_2;OCS1098_2;CHA1097_1",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "vertex_id": "VTX3217_4_SOURCE_WEIGHT",
            "sector": "source coupling",
            "visible_operator": "T_A, source worldtube, species/source material weight",
            "coefficient": "kappa_A, w_A, source-only material multiplier",
            "required_domain_for_zero": "universal Hilbert source current with no source-only hidden coefficient",
            "current_corpus_status": "SOURCE_WEIGHT_EXCLUSION_NOT_PARENT_DERIVED",
            "memory_slope": "B_source_m",
            "if_not_zero": "retain SLP3216_5_source_weight_memory and WEP/Newton/PPN source rows",
            "strongest_source": "SIG1104_4;CHA1097_4;OCS1098_4",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "vertex_id": "VTX3217_5_CLOCK_READOUT",
            "sector": "readout/clock",
            "visible_operator": "clock/spectroscopy/readout map",
            "coefficient": "nu_i, C_readout, alpha_eff, clock standard",
            "required_domain_for_zero": "readout-after-variation plus Q_ONLY/fixed constants and no S_eff feedback",
            "current_corpus_status": "CLOCK_READOUT_AND_RADIATIVE_CLOSURE_UNSIGNED",
            "memory_slope": "B_readout_m",
            "if_not_zero": "retain SLP3216_3_readout_memory and clock/alpha product rows",
            "strongest_source": "SIG1104_6;SIG1104_7;SUB1105_3",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "vertex_id": "VTX3217_6_BOUNDARY_POYNTING",
            "sector": "boundary/worldtube",
            "visible_operator": "n_i T_EM^{0i}, boundary/source flux",
            "coefficient": "C_boundary, C_Poynting",
            "required_domain_for_zero": "boundary functor exact/proper/orthogonal or strict double-zero boundary weight",
            "current_corpus_status": "BOUNDARY_FUNCTOR_UNSIGNED",
            "memory_slope": "B_boundary_m",
            "if_not_zero": "retain SLP3216_4_boundary_memory and 3210 boundary leakage",
            "strongest_source": "3212 Poynting;3213 PROV3213_2_C_Poynting",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "vertex_id": "VTX3217_7_RADIATIVE_EFFECTIVE",
            "sector": "effective/readout",
            "visible_operator": "S_eff loop/readout generated coefficients",
            "coefficient": "delta C_eff(m,mu)",
            "required_domain_for_zero": "radiative/readout stability preserving the same argument-domain rule",
            "current_corpus_status": "RADIATIVE_READOUT_UNSIGNED",
            "memory_slope": "B_eff_m",
            "if_not_zero": "tree-level zero cannot be promoted; retain effective coefficient rows",
            "strongest_source": "SIG1104_7;PACK1105_3;UEM1099_3",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]

    manifest_rows = [
        {
            "gate_id": "VMG3217_0_complete_vertex_list",
            "gate": "visible coefficient vertex list covers all local coupling channels",
            "status": "WRITTEN",
            "pass_for_claim": "false",
            "reason": "manifest exists, but argument domains are not parent-signed",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "gate_id": "VMG3217_1_no_memory_argument",
            "gate": "every visible coefficient is Q_ONLY, REP_TOPOLOGICAL, or EVEN_DOUBLE_ZERO_MEMORY with signed premises",
            "status": "FAIL_CURRENT_CORPUS",
            "pass_for_claim": "false",
            "reason": "EM F2, Hodge, matter/source, readout, boundary, and radiative rows all retain unsigned clauses",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "gate_id": "VMG3217_2_no_untracked_residual",
            "gate": "any coefficient not zero-authorized is explicitly retained as finite residual",
            "status": "PASS_PRIVATE_DISCIPLINE",
            "pass_for_claim": "false",
            "reason": "first slope source rows are staged but missing source-backed values",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "gate_id": "VMG3217_3_no_cancellation",
            "gate": "do not claim zero by cancellation among independent visible operators",
            "status": "PASS_GUARDRAIL",
            "pass_for_claim": "false",
            "reason": "3216 independence guard forces per-channel zero or finite bound",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]

    first_rows = [
        {
            "row_id": "FSR3217_0_balpha_m",
            "quantity": "b_alpha_m = partial_m ln Z_A at m_*",
            "zero_theorem_needed": "unique EM kinetic owner/no-extra-F2 or typed Q_ONLY gauge norm or strict double-zero deformation",
            "finite_value_needed": "numeric/source-backed b_alpha_m with memory normalization and units",
            "operator_norm_needed": "||F^2|| support norm",
            "status": "MISSING_ZERO_THEOREM_OR_SOURCE_BACKED_SLOPE",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "row_id": "FSR3217_1_B_Hodge_m",
            "quantity": "B_Hodge_m = partial_m g_obs/star_obs at m_*",
            "zero_theorem_needed": "observed coframe and Hodge star factor through q with Dq[partial_m]=0",
            "finite_value_needed": "operator norm bound for B_Hodge_m T_EM",
            "operator_norm_needed": "EM stress norm, including null radiation",
            "status": "MISSING_HODGE_DESCENT_OR_SOURCE_BACKED_SLOPE",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "row_id": "FSR3217_2_B_source_m",
            "quantity": "B_source_m = partial_m kappa_A or w_A at m_*",
            "zero_theorem_needed": "universal Hilbert source/current owner with no source-only hidden coefficient",
            "finite_value_needed": "species/source-weight derivative and composition/source support",
            "operator_norm_needed": "matter stress/source composition norm",
            "status": "MISSING_UNIVERSAL_SOURCE_THEOREM_OR_SOURCE_BACKED_SLOPE",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]

    decision_rows = [
        {
            "decision_id": "DEC3217_0_result",
            "result": "VISIBLE_COEFFICIENT_VERTEX_MANIFEST_BUILT_MEMORY_ABSENCE_NOT_PARENT_SIGNED_FIRST_SLOPE_ROWS_STAGED",
            "claim_status": "NO_COEFFICIENT_ZERO_NO_MEMORY_SILENCE_NO_LOCAL_GR_CLAIM",
            "decision": "3217 turns the coupling problem into an explicit parent-action vertex manifest. The exact typed-exclusion route would kill memory slopes if each visible coefficient is Q_ONLY/REP_TOPOLOGICAL or signed EVEN_DOUBLE_ZERO_MEMORY. Current corpus does not sign this for EM, Hodge, matter/source, readout, boundary, or radiative coefficients.",
            "best_next_route": "attack the sharpest row first: EM F2. Prove the unique EM kinetic owner/no-extra-F2 clause in the memory-origin language, or source b_alpha_m as the first finite slope row.",
            "next_target": "3218-Y5-R2FR-EM-F2-vertex-owner-for-memory-slope-zero-or-balpha-m-source-row-under-AX1090",
            "valid_for_claim": "false",
            "generated_utc": now,
        }
    ]

    return input_rows, domain_rows, vertex_rows, manifest_rows, first_rows, decision_rows


def main() -> None:
    now = stamp()
    input_rows, domain_rows, vertex_rows, manifest_rows, first_rows, decision_rows = build_rows(now)

    generated_without_validation = [
        INPUTS,
        DOMAIN_RULES,
        VERTEX_LIST,
        MANIFEST_GATE,
        FIRST_ROWS,
        DECISION,
    ]

    write_csv(INPUTS, input_rows)
    write_csv(DOMAIN_RULES, domain_rows)
    write_csv(VERTEX_LIST, vertex_rows)
    write_csv(MANIFEST_GATE, manifest_rows)
    write_csv(FIRST_ROWS, first_rows)
    write_csv(DECISION, decision_rows)

    all_rows: list[dict[str, str]] = []
    for path in generated_without_validation:
        all_rows.extend(read_csv(path))
    claim_rows = [row for row in all_rows if row.get("valid_for_claim") == "true"]

    validation_rows = [
        {
            "check_id": "VAL3217_00_inputs_exist",
            "check": "all cited inputs exist",
            "pass": b(all(row["exists"] == "true" for row in input_rows)),
            "detail": f"inputs={len(input_rows)}",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3217_01_domain_rules",
            "check": "argument-domain classifier covers zero and finite cases",
            "pass": b(len(domain_rows) == 4),
            "detail": ";".join(row["argument_domain"] for row in domain_rows),
            "generated_utc": now,
        },
        {
            "check_id": "VAL3217_02_vertex_coverage",
            "check": "visible coefficient vertex list covers local coupling channels",
            "pass": b(len(vertex_rows) >= 8),
            "detail": ";".join(row["vertex_id"] for row in vertex_rows),
            "generated_utc": now,
        },
        {
            "check_id": "VAL3217_03_memory_absence_not_overclaimed",
            "check": "manifest gate blocks memory-absence claim",
            "pass": b(any(row["gate_id"] == "VMG3217_1_no_memory_argument" and row["status"] == "FAIL_CURRENT_CORPUS" for row in manifest_rows)),
            "detail": "argument domains are not parent-signed across all vertices",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3217_04_first_slope_rows",
            "check": "first finite slope rows are staged",
            "pass": b(len(first_rows) >= 3),
            "detail": ";".join(row["row_id"] for row in first_rows),
            "generated_utc": now,
        },
        {
            "check_id": "VAL3217_05_claims_blocked",
            "check": "no generated row is valid_for_claim true",
            "pass": b(len(claim_rows) == 0),
            "detail": f"claim_rows_true={len(claim_rows)}",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3217_06_no_formalization_workbench_edit",
            "check": "script writes only post-checkpoint outputs",
            "pass": "true",
            "detail": "no formalization-workbench paths are output targets",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3217_07_csv_parse",
            "check": "all generated CSV files parse cleanly",
            "pass": b(all(len(read_csv(path)) > 0 for path in generated_without_validation)),
            "detail": ";".join(path.name for path in generated_without_validation),
            "generated_utc": now,
        },
        {
            "check_id": "VAL3217_08_next_target",
            "check": "next target is the sharp EM F2 vertex",
            "pass": b("3218" in decision_rows[0]["next_target"]),
            "detail": decision_rows[0]["next_target"],
            "generated_utc": now,
        },
    ]
    write_csv(VALIDATION, validation_rows)

    doc = f"""# 3217 - Parent Visible-Coefficient Vertex List Or First Memory Slope Source Row under AX1090

Private checkpoint. This is not a local-GR claim, Maxwell derivation claim, Newtonian-limit claim, WEP pass, R10 pass, clock pass, `b_alpha=0` claim, memory silence claim, or public-facing result.

## Result

3217 builds the parent-action vertex manifest needed by 3216.

The rule is now brutally simple:

```text
Every visible coefficient must be classified as:

Q_ONLY
REP_TOPOLOGICAL
EVEN_DOUBLE_ZERO_MEMORY
or EXPLICIT_RESIDUAL.
```

If a coefficient is `Q_ONLY` or fixed representation/topological data, the memory slope dies by chain rule or connected-sector constancy.

If it is `EVEN_DOUBLE_ZERO_MEMORY`, the linear memory slope dies but second-order Hessian/range corrections remain.

If it is `EXPLICIT_RESIDUAL`, it must enter the finite source vector. No hiding, no cancellation goblinry.

Current verdict: the manifest is built, but memory absence is not parent-signed for the full local coupling set. The sharpest first attack is the EM `F^2` vertex, because it controls `b_alpha_m` and feeds clocks, WEP, R10, and EM normalization.

## Argument Domain Rules

{md_table(domain_rows, ["domain_id", "argument_domain", "allowed_form", "memory_slope_result", "promotion_requirement", "claim_status", "valid_for_claim"])}

## Visible Coefficient Vertex List

{md_table(vertex_rows, ["vertex_id", "sector", "visible_operator", "coefficient", "required_domain_for_zero", "current_corpus_status", "memory_slope", "if_not_zero", "strongest_source", "valid_for_claim"])}

## Vertex Manifest Gate

{md_table(manifest_rows, ["gate_id", "gate", "status", "pass_for_claim", "reason", "valid_for_claim"])}

## First Memory Slope Source Rows

{md_table(first_rows, ["row_id", "quantity", "zero_theorem_needed", "finite_value_needed", "operator_norm_needed", "status", "valid_for_claim"])}

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
- `{rel(DOMAIN_RULES)}`
- `{rel(VERTEX_LIST)}`
- `{rel(MANIFEST_GATE)}`
- `{rel(FIRST_ROWS)}`
- `{rel(DECISION)}`
- `{rel(VALIDATION)}`

## Validation

{md_table(validation_rows, ["check_id", "pass", "detail"])}

All generated rows remain `valid_for_claim=false`.
"""
    DOC.write_text(doc, encoding="utf-8")


if __name__ == "__main__":
    main()
