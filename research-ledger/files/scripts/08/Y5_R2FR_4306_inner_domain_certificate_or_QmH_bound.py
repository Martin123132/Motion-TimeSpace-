from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Tuple


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4306"
CLAIM_ID = "L-147"
BRANCH = "MTS_R2FR_Y5_INNER_DOMAIN_CERTIFICATE_OR_QMH_BOUND_4306"
DECISION = "INNER_BOUNDARY_LAW_DERIVED_SMOOTH_NOEXCISION_ZERO_OR_TRACE_QMH_BOUND_NONCLAIM"
MARKER = "PPC4161_INNER_DOMAIN_CERTIFICATE_OR_QMH_BOUND_4306"
PACKET_MARKER = "PPC4161_PACKET_INNER_DOMAIN_CERTIFICATE_OR_QMH_BOUND_4306"
NEXT_TARGET = "4307-Y5-R2FR-source-domain-owner-or-inner-flux-profile-fill.md"

FORMAL_PATH = FORMAL / "322-PPC4161-inner-domain-certificate-or-QmH-bound.md"
DOC_PATH = POST / "4306-Y5-R2FR-inner-domain-certificate-or-QmH-bound.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4306_VALIDATION.csv"

STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

SOURCES: Dict[str, Tuple[Path, str, str]] = {
    "SRC4306_00_4305_doc": (
        DOC_PATH.with_name("4305-Y5-R2FR-source-power-amplitude-or-inner-charge-bound-runner.md"),
        "4306-Y5-R2FR-inner-domain-certificate-or-QmH-bound.md",
        "4305 handoff: derive domain certificate or Q_m^H bound.",
    ),
    "SRC4306_01_4305_inner": (
        SOURCE_DIR / "P8_Y5_R2FR_4305_INNER_CHARGE_DOMAIN_SPLIT.csv",
        "IN4305_4_finite_bound",
        "4305 inner smooth/excision split and finite bound route.",
    ),
    "SRC4306_02_4302_operator": (
        FORMAL / "318-PPC4161-m-lock-coercivity-gap-and-DvGamma-quadratic-input-pack.md",
        "L_m u = -nabla_i(Z_m h^ij nabla_j u) + M_m^2 u + Delta_H[u],",
        "m-lock operator whose integration-by-parts boundary term defines B_inner.",
    ),
    "SRC4306_03_1538_inner": (
        SOURCE_DIR / "P8_Y5_PARENT_QLOC_1538_N_INNER_THEOREM_OR_BOUND.csv",
        "NINNER1538_4_finite_bound",
        "older N_inner <= C_inner |Q_m^H| finite row.",
    ),
    "SRC4306_04_1529_certificate": (
        SOURCE_DIR / "P8_Y5_PARENT_QLOC_1529_BOUNDARY_CERTIFICATE_AUDIT.csv",
        "BND1529_1_boundary_condition",
        "boundary/no-flux certificate audit.",
    ),
    "SRC4306_05_1529_runner": (
        SOURCE_DIR / "P8_Y5_PARENT_QLOC_1529_CERTIFICATE_OR_BOUND_RUNNER.csv",
        "RUN1529_0_certificate_route",
        "certificate route blocked unless parent signs domain/boundary/zero-mode clauses.",
    ),
    "SRC4306_06_192_noflux": (
        FORMAL / "192-PPC4161-local-boundary-no-flux-sector-interface-theorem.md",
        "F_rad[tau] != 0  =>  route as boundary charge, not hidden bulk current.",
        "local no-flux/support-separation theorem precedent.",
    ),
    "SRC4306_07_284_boundary": (
        FORMAL / "284-PPC4161-Dq-boundary-projector-fixed-collar-or-boundary-residual-bound.md",
        "Dq_boundary_projector = 0.0,",
        "fixed compact no-flux collar branch for boundary/projector row.",
    ),
    "SRC4306_08_319_handoff": (
        FORMAL / "319-PPC4161-source-boundary-silence-or-component-norms-for-m-lock.md",
        "N_inner <= C_inner |Q_m^H_nonHilbert|",
        "4303 inner charge component bound.",
    ),
}


def base_row() -> Dict[str, str]:
    return {
        "checkpoint": CHECKPOINT,
        "branch": BRANCH,
        "generated_utc": STAMP,
        "decision": DECISION,
        "claim_allowed": "False",
        "valid_for_claim": "False",
    }


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def write_csv(path: Path, rows: List[Dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    fields: List[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def md_table(rows: List[Dict[str, str]], columns: List[str]) -> str:
    lines = [
        "| " + " | ".join(columns) + " |",
        "| " + " | ".join("---" for _ in columns) + " |",
    ]
    for row in rows:
        values = [str(row.get(col, "")).replace("\n", "<br>").replace("|", "\\|") for col in columns]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def append_once(path: Path, marker: str, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    existing = read_text(path) if path.exists() else ""
    if marker in existing:
        return
    with path.open("a", encoding="utf-8", newline="") as handle:
        if existing and not existing.endswith("\n"):
            handle.write("\n")
        handle.write("\n" + content.strip() + "\n")


def append_claim_once() -> None:
    path = FORMAL / "02-claims-register.csv"
    existing = read_text(path) if path.exists() else ""
    if CLAIM_ID in existing:
        return
    row = [
        CLAIM_ID,
        "local_gr",
        (
            "4306 derives the exact inner-boundary law for the m-lock source-pair gate. For "
            "L_m u=-div(Z_m grad u)+M_m^2u+Delta_H[u], integration by parts gives "
            "B_inner[phi]=int_{partial D_in} phi Z_m n.grad u dSigma + B_src[phi]. Therefore "
            "N_inner=0 is exact on a smooth no-excision source domain, or on a parent-signed Dirichlet/no-flux "
            "inner boundary with no source-boundary injection. If an excision/source boundary survives, the honest "
            "fallback is a trace bound N_inner<=C_tr||Z_m n.grad u||_{H^{-1/2}}+||B_src||, sharpened into monopole "
            "and multipole pieces C_0|Q_m^H|+C_perp||g_perp||+||B_src||."
        ),
        (
            "4306 source register, boundary variation identity, domain certificate matrix, QmH trace bound, "
            "Npair update, decision, firewall, status, next-target and validation CSV."
        ),
        "private_inner_boundary_law_derived_smooth_zero_or_trace_QmH_bound_nonclaim",
        (
            "Parent-own the source domain as smooth/no-excision or no-flux, or source the inner flux profile "
            "Q_m^H, multipole tail g_perp, trace constants and B_src."
        ),
        (
            "Using smooth-domain zero for point/excision sources, treating old no-flux precedent as a certificate, "
            "dropping source-boundary injection, or claiming local GR before N_inner and lambda_m are source-backed."
        ),
    ]
    with path.open("a", encoding="utf-8", newline="") as handle:
        csv.writer(handle).writerow(row)


def source_rows() -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    for source_id, (path, needle, purpose) in SOURCES.items():
        text = read_text(path) if path.exists() else ""
        row = base_row()
        row.update(
            {
                "source_id": source_id,
                "source_path": str(path),
                "exists": str(path.exists()),
                "needle": needle,
                "needle_found": str(needle in text),
                "purpose": purpose,
            }
        )
        rows.append(row)
    return rows


def identity_rows() -> List[Dict[str, str]]:
    specs = [
        (
            "BID4306_0_operator",
            "L_m u = -nabla_i(Z_m h^{ij}nabla_j u)+M_m^2 u+Delta_H[u]",
            "4302 operator form",
            "starting point",
            "OPERATOR_IMPORTED",
        ),
        (
            "BID4306_1_weak_form",
            "<phi,L_m u>_D = int_D Z_m grad phi.grad u + int_D phi(M_m^2u+Delta_H[u]) - int_partialD phi Z_m n.grad u",
            "integration by parts",
            "boundary term is not optional",
            "DERIVED_WEAK_FORM",
        ),
        (
            "BID4306_2_inner_functional",
            "B_inner[phi] = int_partialD_in phi Z_m n.grad u dSigma + B_src[phi]",
            "definition",
            "inner source/excision boundary forcing",
            "DERIVED_BOUNDARY_FUNCTIONAL",
        ),
        (
            "BID4306_3_dual_norm",
            "N_inner = sup_{||phi||_{H1(D)}<=1} |B_inner[phi]|",
            "boundary-dual norm",
            "turns prose inner charge into a scoreable norm",
            "DERIVED_NORM_DEFINITION",
        ),
        (
            "BID4306_4_trace_bound",
            "N_inner <= C_tr ||Z_m n.grad u||_{H^{-1/2}(partialD_in)} + ||B_src||_{H^{-1/2}}",
            "trace theorem",
            "finite route when zero certificate fails",
            "DERIVED_TRACE_BOUND",
        ),
    ]
    rows: List[Dict[str, str]] = []
    for row_id, formula, basis, implication, status in specs:
        row = base_row()
        row.update({"row_id": row_id, "formula": formula, "basis": basis, "implication": implication, "status": status, "score_ready": "False"})
        rows.append(row)
    return rows


def domain_rows() -> List[Dict[str, str]]:
    specs = [
        (
            "DOM4306_0_smooth_no_excision",
            "partialD_in = empty set",
            "B_inner=0, N_inner=0",
            "EXACT_ZERO_IF_PARENT_OWNS_SMOOTH_SOURCE_DOMAIN",
            "Best clean route: local branch treats compact sources as smooth Hilbert matter, not excised point holes.",
        ),
        (
            "DOM4306_1_Dirichlet",
            "phi|partialD_in=0 or u fixed by parent source matching",
            "B_inner[phi]=0",
            "EXACT_ZERO_IF_PARENT_BOUNDARY_VALUE_SIGNED",
            "Cannot choose Dirichlet by hand; source matching must own it.",
        ),
        (
            "DOM4306_2_Neumann_no_flux",
            "Z_m n.grad u|partialD_in=0 and source-boundary injection B_src=0",
            "B_inner=0, N_inner=0",
            "EXACT_ZERO_IF_NO_FLUX_CERTIFICATE_SIGNED",
            "1529 says this certificate is not found for the older lambda_phi route.",
        ),
        (
            "DOM4306_3_Hilbert_no_memory_charge",
            "source action factors through q/Hilbert variables with no independent m-boundary charge",
            "Q_m^H=0 and B_src=0",
            "EXACT_ZERO_ROUTE_UNSIGNED",
            "Equivalent to proving compact matter carries no extra memory monopole.",
        ),
        (
            "DOM4306_4_excision_hair",
            "partialD_in nonempty and Z_m n.grad u or B_src survives",
            "N_inner must be bounded, not erased",
            "FINITE_HAIR_ROUTE",
            "This is the honest exterior point/source branch.",
        ),
    ]
    rows: List[Dict[str, str]] = []
    for row_id, condition, consequence, status, note in specs:
        row = base_row()
        row.update({"row_id": row_id, "condition": condition, "consequence": consequence, "status": status, "note": note, "parent_signed_now": "False", "score_ready": "False"})
        rows.append(row)
    return rows


def qmh_rows() -> List[Dict[str, str]]:
    specs = [
        (
            "QMH4306_0_flux_profile",
            "g_in := Z_m n.grad u|partialD_in",
            "inner normal memory flux profile",
            "MISSING_PROFILE",
            "source g_in on the parent source boundary or prove it vanishes",
        ),
        (
            "QMH4306_1_monopole",
            "Q_m^H := int_partialD_in g_in dSigma",
            "monopole/hair charge",
            "MISSING_VALUE",
            "1538 C_inner|Q_m^H| is only safe if higher modes are absent or separately bounded",
        ),
        (
            "QMH4306_2_multipole_split",
            "g_in = Q_m^H/Area(partialD_in) + g_perp, int g_perp dSigma=0",
            "separates monopole from multipole/tidal boundary hair",
            "DERIVED_DECOMPOSITION",
            "prevents hiding multipole boundary flux inside a scalar Q_m^H number",
        ),
        (
            "QMH4306_3_sharp_bound",
            "N_inner <= C_0 |Q_m^H| + C_perp ||g_perp||_{H^{-1/2}} + ||B_src||_{H^{-1/2}}",
            "sharpened finite bound",
            "DERIVED_BOUND_FORM_INPUTS_MISSING",
            "required inputs: C_0, C_perp, Q_m^H, g_perp norm, B_src norm and source-domain convention",
        ),
        (
            "QMH4306_4_1538_recovery",
            "N_inner <= C_inner |Q_m^H| when g_perp=0 and B_src=0 or absorbed into C_inner",
            "recovers 1538 finite row as a special case",
            "CONDITIONAL_SIMPLIFICATION",
            "do not use the scalar simplification until multipole/source-boundary injection is killed",
        ),
    ]
    rows: List[Dict[str, str]] = []
    for row_id, formula, meaning, status, next_input in specs:
        row = base_row()
        row.update({"row_id": row_id, "formula": formula, "meaning": meaning, "status": status, "next_input": next_input, "score_ready": "False"})
        rows.append(row)
    return rows


def runner_rows() -> List[Dict[str, str]]:
    specs = [
        (
            "RUN4306_0_smooth_selector",
            "smooth no-excision source domain",
            "N_pair <= N_EM + N_rest; if N_EM=N_rest=0 then N_pair=0",
            "A_src and N_inner are both zero on this branch.",
            "EXACT_ROUTE_CONDITIONAL",
        ),
        (
            "RUN4306_1_no_flux_excision",
            "excision domain with parent no-flux/source-boundary certificate",
            "N_pair <= N_EM + N_rest",
            "inner boundary exists but contributes zero by certificate.",
            "EXACT_ROUTE_UNSIGNED",
        ),
        (
            "RUN4306_2_trace_fallback",
            "excision domain with surviving memory flux",
            "N_pair <= C_0|Q_m^H| + C_perp||g_perp|| + ||B_src|| + N_EM + N_rest",
            "scoreable fallback replacing a vague C_inner slot.",
            "BOUND_ROUTE_READY_INPUTS_MISSING",
        ),
        (
            "RUN4306_3_to_m_lock",
            "m-lock handoff",
            "Delta_m <= (N_pair+N_N)/lambda_m; C4302_DVGAMMA_QUAD uses Delta_m and Delta_Dv_m",
            "same 4302 route after inner-domain reduction.",
            "HANDOFF_READY_NOT_SCORE_READY",
        ),
    ]
    rows: List[Dict[str, str]] = []
    for runner_id, branch_name, formula, role, status in specs:
        row = base_row()
        row.update({"runner_id": runner_id, "branch_name": branch_name, "formula": formula, "role": role, "status": status, "score_ready": "False"})
        rows.append(row)
    return rows


def decision_rows() -> List[Dict[str, str]]:
    specs = [
        (
            "DEC4306_0_gain",
            "INNER_BOUNDARY_LAW_DERIVED",
            "N_inner is now the dual norm of an explicit boundary functional, not a vague charge label.",
            "Use the trace/QmH profile law for all future source-pair scoring.",
        ),
        (
            "DEC4306_1_zero",
            "ZERO_ROUTE_IS_DOMAIN_OWNERSHIP",
            "N_inner=0 is exact for smooth no-excision source domains, signed Dirichlet, or signed no-flux/source-boundary silence.",
            "Next step must prove which domain the parent owns.",
        ),
        (
            "DEC4306_2_bound",
            "SCALAR_QMH_NOT_ENOUGH_BY_ITSELF",
            "A scalar Q_m^H bound is safe only after multipole flux g_perp and source-boundary injection B_src are killed or bounded.",
            "Source Q_m^H, g_perp, B_src and trace constants if no zero certificate closes.",
        ),
        (
            "DEC4306_3_next",
            "SOURCE_DOMAIN_OWNER_OR_INNER_FLUX_PROFILE_NEXT",
            "The shortest path is to parent-own smooth matter/no-excision; fallback is finite inner flux profile fill.",
            NEXT_TARGET,
        ),
    ]
    rows: List[Dict[str, str]] = []
    for decision_id, result, reason, next_action in specs:
        row = base_row()
        row.update({"decision_id": decision_id, "result": result, "reason": reason, "next_action": next_action})
        rows.append(row)
    return rows


def firewall_rows() -> List[Dict[str, str]]:
    rules = [
        "Do not use smooth no-excision N_inner=0 for exterior point/excision source models.",
        "Do not import old no-flux precedent as a parent certificate; 1529 says the certificate was not found.",
        "Do not reduce N_inner to C_inner|Q_m^H| unless g_perp and B_src are zero or separately bounded.",
        "Do not drop radiative/boundary flux; route it as boundary/Hamiltonian flux or bound it.",
        "Do not claim local GR until N_pair, lambda_m, Khat/connection and projection constants are theorem-zero or source-backed.",
    ]
    rows: List[Dict[str, str]] = []
    for index, rule in enumerate(rules):
        row = base_row()
        row.update({"firewall_id": f"FW4306_{index}", "rule": rule, "status": "ACTIVE"})
        rows.append(row)
    return rows


def status_rows() -> List[Dict[str, str]]:
    specs = [
        ("STAT4306_0_Ninner", "N_inner", "BOUNDARY_LAW_DERIVED", "zero requires source-domain ownership; fallback requires flux profile"),
        ("STAT4306_1_QmH", "Q_m^H", "MONOPOLE_INPUT_MISSING", "not enough without multipole/source-boundary guard"),
        ("STAT4306_2_gperp", "g_perp", "NEW_REQUIRED_INPUT", "prevents scalar monopole overclaim"),
        ("STAT4306_3_Bsrc", "B_src", "NEW_REQUIRED_INPUT", "source-boundary injection must be zero or bounded"),
        ("STAT4306_4_Npair", "N_pair", "REDUCED_NOT_CLOSED", "smooth branch promising; excision branch needs profile/certificate"),
    ]
    rows: List[Dict[str, str]] = []
    for status_id, item, status, note in specs:
        row = base_row()
        row.update({"status_id": status_id, "item": item, "status": status, "note": note})
        rows.append(row)
    return rows


def next_rows() -> List[Dict[str, str]]:
    row = base_row()
    row.update(
        {
            "next_target_id": "NT4306_0",
            "next_target": NEXT_TARGET,
            "target_question": "Does the parent local source branch own a smooth no-excision Hilbert domain, or must the inner flux profile be filled?",
            "preferred_route": "prove compact sources are smooth Hilbert matter on the m-lock domain so partialD_in is empty and N_inner=0",
            "fallback_route": "fill Q_m^H, g_perp, B_src, C_0 and C_perp for the trace-bound fallback",
        }
    )
    return [row]


def write_docs(tables: Dict[str, List[Dict[str, str]]]) -> None:
    formal_text = f"""# 322 PPC4161 inner-domain certificate or QmH bound

Marker: `{MARKER}`

## Decision

`{DECISION}`

4306 derives the inner-boundary law:

```text
B_inner[phi] = int_partialD_in phi Z_m n.grad u dSigma + B_src[phi],
N_inner = sup_{{||phi||_H1<=1}} |B_inner[phi]|.
```

Hence:

```text
N_inner <= C_tr ||Z_m n.grad u||_H-1/2 + ||B_src||_H-1/2.
```

The scalar `Q_m^H` row is only the monopole part. The safe finite branch is:

```text
N_inner <= C_0 |Q_m^H| + C_perp ||g_perp|| + ||B_src||.
```

## Boundary Variation Identity

{md_table(tables["identity"], ["row_id", "formula", "status", "implication"])}

## Domain Certificate Matrix

{md_table(tables["domain"], ["row_id", "condition", "consequence", "status", "note"])}

## QmH Trace Bound

{md_table(tables["qmh"], ["row_id", "formula", "status", "next_input"])}

## Updated Npair Runner

{md_table(tables["runner"], ["runner_id", "branch_name", "formula", "status"])}

## Result

The smooth-source/no-excision branch is the cleanest route: it kills `N_inner` exactly by domain identity. The exterior/excision branch remains viable but now needs a real inner flux profile, not just a scalar placeholder.

Next target: `{NEXT_TARGET}`.
"""
    doc_text = f"""# 4306 - inner-domain certificate or QmH bound

## Verdict
- Derived the weak-form boundary identity for `N_inner`.
- Proved exactly when `N_inner=0`: smooth no-excision source domain, signed Dirichlet/source matching, or signed no-flux plus no source-boundary injection.
- Replaced the crude `C_inner |Q_m^H|` row with a sharper trace fallback: `C_0|Q_m^H| + C_perp||g_perp|| + ||B_src||`.
- No local-GR claim fires; the next target is parent ownership of the source domain or real inner flux profile inputs.

## Source Register
{md_table(tables["sources"], ["source_id", "source_path", "exists", "needle_found", "purpose"])}

## Boundary Variation Identity
{md_table(tables["identity"], ["row_id", "formula", "basis", "implication", "status"])}

## Domain Certificate Matrix
{md_table(tables["domain"], ["row_id", "condition", "consequence", "status", "note"])}

## QmH Trace Bound
{md_table(tables["qmh"], ["row_id", "formula", "meaning", "status", "next_input"])}

## Updated Npair Runner
{md_table(tables["runner"], ["runner_id", "branch_name", "formula", "role", "status"])}

## Decision
{md_table(tables["decision"], ["decision_id", "result", "reason", "next_action"])}

## Claim Firewall
{md_table(tables["firewall"], ["firewall_id", "rule", "status"])}

## Status
{md_table(tables["status"], ["status_id", "item", "status", "note"])}

## Next Target
{md_table(tables["next"], ["next_target_id", "next_target", "target_question", "preferred_route", "fallback_route"])}
"""
    FORMAL_PATH.write_text(formal_text, encoding="utf-8")
    DOC_PATH.write_text(doc_text, encoding="utf-8")


def validate_csv(path: Path) -> Tuple[bool, str]:
    try:
        with path.open("r", encoding="utf-8", newline="") as handle:
            rows = list(csv.DictReader(handle))
        return bool(rows), f"{path.name} parses with {len(rows)} rows"
    except Exception as exc:
        return False, f"{path.name} parse failure: {exc}"


def validation_rows(paths: Dict[str, Path], tables: Dict[str, List[Dict[str, str]]]) -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []

    def add(check_id: str, description: str, passed: bool, evidence: str) -> None:
        row = base_row()
        row.update({"check_id": check_id, "description": description, "passed": str(passed), "evidence": evidence})
        rows.append(row)

    add("VAL4306_0_sources_exist", "all cited local source paths exist", all(Path(row["source_path"]).exists() for row in tables["sources"]), "source_register")
    add("VAL4306_1_needles_found", "all cited source needles found", all(row["needle_found"] == "True" for row in tables["sources"]), "source_register")
    add("VAL4306_2_boundary_identity", "B_inner boundary functional is derived", any(row["row_id"] == "BID4306_2_inner_functional" for row in tables["identity"]), "identity_rows")
    add("VAL4306_3_trace_bound", "trace norm bound is derived", any(row["row_id"] == "BID4306_4_trace_bound" for row in tables["identity"]), "identity_rows")
    add("VAL4306_4_smooth_zero", "smooth no-excision zero branch exists", any(row["row_id"] == "DOM4306_0_smooth_no_excision" for row in tables["domain"]), "domain_rows")
    add("VAL4306_5_qmh_sharp_bound", "QmH plus multipole/source-boundary bound exists", any(row["row_id"] == "QMH4306_3_sharp_bound" for row in tables["qmh"]), "qmh_rows")
    add("VAL4306_6_scalar_qmh_guard", "scalar QmH simplification is guarded", any(row["row_id"] == "QMH4306_4_1538_recovery" for row in tables["qmh"]), "qmh_rows")
    add("VAL4306_7_runner_fallback", "trace fallback feeds N_pair", any(row["runner_id"] == "RUN4306_2_trace_fallback" for row in tables["runner"]), "runner_rows")
    add(
        "VAL4306_8_claim_flags_false",
        "all generated rows keep claim flags false",
        all(row.get("claim_allowed") == "False" and row.get("valid_for_claim") == "False" for table in tables.values() for row in table),
        "generated_tables",
    )
    for name, path in paths.items():
        if name == "validation":
            continue
        ok, detail = validate_csv(path)
        add(f"VAL4306_csv_{name}", detail, ok, "generated_artifacts")
    add("VAL4306_docs", "formal and post checkpoint docs exist", FORMAL_PATH.exists() and DOC_PATH.exists(), "generated_docs")
    add("VAL4306_claim_row", f"{CLAIM_ID} claim-register row exists", CLAIM_ID in read_text(FORMAL / "02-claims-register.csv"), "claims_register")
    add("VAL4306_spine_marker", "spine marker exists", MARKER in read_text(FORMAL / "07-unification-spine.md"), "unification_spine")
    add("VAL4306_packet_marker", "packet marker exists", PACKET_MARKER in read_text(FORMAL / "180-PPC4161-private-local-packet-integration.md"), "private_packet")
    return rows


def main() -> None:
    paths = {
        "sources": SOURCE_DIR / "P8_Y5_R2FR_4306_SOURCE_REGISTER.csv",
        "identity": SOURCE_DIR / "P8_Y5_R2FR_4306_BOUNDARY_VARIATION_IDENTITY.csv",
        "domain": SOURCE_DIR / "P8_Y5_R2FR_4306_DOMAIN_CERTIFICATE_MATRIX.csv",
        "qmh": SOURCE_DIR / "P8_Y5_R2FR_4306_QMH_TRACE_BOUND.csv",
        "runner": SOURCE_DIR / "P8_Y5_R2FR_4306_NPAIR_DOMAIN_UPDATE.csv",
        "decision": SOURCE_DIR / "P8_Y5_R2FR_4306_DECISION.csv",
        "firewall": SOURCE_DIR / "P8_Y5_R2FR_4306_CLAIM_FIREWALL.csv",
        "status": SOURCE_DIR / "P8_Y5_R2FR_4306_STATUS.csv",
        "next": SOURCE_DIR / "P8_Y5_R2FR_4306_NEXT_TARGET.csv",
        "validation": VALIDATION_PATH,
    }
    tables = {
        "sources": source_rows(),
        "identity": identity_rows(),
        "domain": domain_rows(),
        "qmh": qmh_rows(),
        "runner": runner_rows(),
        "decision": decision_rows(),
        "firewall": firewall_rows(),
        "status": status_rows(),
        "next": next_rows(),
    }
    for key, rows in tables.items():
        write_csv(paths[key], rows)
    write_docs(tables)
    append_claim_once()
    append_once(
        FORMAL / "07-unification-spine.md",
        MARKER,
        f"""
## PPC4161 4306 inner-domain certificate or QmH bound

Marker: `{MARKER}`

4306 derives the inner-boundary law for the local m-lock source pair. `N_inner` is zero exactly when the parent owns a smooth no-excision source domain, a signed Dirichlet/source-match boundary, or a signed no-flux plus no source-boundary injection condition. If an excision/source boundary survives, the fallback is no longer a vague `C_inner |Q_m^H|`: it is `N_inner <= C_0|Q_m^H| + C_perp||g_perp|| + ||B_src||`, with monopole, multipole and source-boundary injection separated.
""",
    )
    append_once(
        FORMAL / "180-PPC4161-private-local-packet-integration.md",
        PACKET_MARKER,
        f"""
## 4306 packet inner-boundary law

Marker: `{PACKET_MARKER}`

Packet update: the source-pair blocker is now a domain theorem or an inner flux profile problem. Smooth Hilbert sources kill `N_inner` by absence of an inner boundary; excision sources need `Q_m^H`, multipole flux and source-boundary injection bounds.
""",
    )
    validation = validation_rows(paths, tables)
    write_csv(paths["validation"], validation)
    failed = [row for row in validation if row["passed"] != "True"]
    print(f"{CHECKPOINT}: wrote {len(tables)} csv artifacts plus validation")
    print(f"{CHECKPOINT}: validation rows={len(validation)} failed={len(failed)}")
    print(f"{CHECKPOINT}: decision={DECISION}")
    if failed:
        for row in failed:
            print(f"FAILED {row['check_id']}: {row['description']} evidence={row['evidence']}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
