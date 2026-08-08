from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main")
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4745"
CLAIM_ID = "L-587"
MARKER = "PPC4161_ADJOINT_PRINCIPAL_SYMBOL_UCP_ELLIPTICITY_GATE_OR_CZEROMODE_BOUND_RUNNER_4745"
PACKET_MARKER = "PPC4161_PACKET_ADJOINT_PRINCIPAL_SYMBOL_UCP_ELLIPTICITY_GATE_OR_CZEROMODE_BOUND_RUNNER_4745"
DECISION = "ADJOINT_PRINCIPAL_SYMBOL_GATE_DERIVED_STATIC_ELLIPTIC_ROUTE_CONDITIONAL_LORENTZIAN_UCP_NOT_CLAIMED_CZEROMODE_BOUND_STAGED"
NEXT_TARGET = "4746-Y5-R2FR-static-PPN-elliptic-slice-gap-proof-or-lorentzian-energy-bound.md"

DOC_PATH = POST / "4745-Y5-R2FR-adjoint-principal-symbol-UCP-ellipticity-gate-or-CzeroMode-bound-runner.md"
FORMAL_PATH = FORMAL / "761-PPC4161-adjoint-principal-symbol-UCP-ellipticity-gate-or-CzeroMode-bound-runner.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
RESUME_PATH = POST / "CURRENT_LOCAL_RESUME.md"

SOURCE_REGISTER_CSV = SOURCE_DIR / "P8_Y5_R2FR_4745_SOURCE_REGISTER.csv"
SYMBOL_DERIVATION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4745_ADJOINT_PRINCIPAL_SYMBOL_DERIVATION.csv"
DN_ELLIPTIC_GATE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4745_DN_ELLIPTICITY_UCP_GATE.csv"
LORENTZIAN_AUDIT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4745_LORENTZIAN_CAUTION_AUDIT.csv"
PHYSICAL_KERNEL_AUDIT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4745_PHYSICAL_KERNEL_AUDIT.csv"
CZ_BOUND_RUNNER_CSV = SOURCE_DIR / "P8_Y5_R2FR_4745_CZEROMODE_BOUND_RUNNER.csv"
ROUTE_MATRIX_CSV = SOURCE_DIR / "P8_Y5_R2FR_4745_ROUTE_SELECTION_MATRIX.csv"
PROMOTION_GATES_CSV = SOURCE_DIR / "P8_Y5_R2FR_4745_PROMOTION_GATES.csv"
FIREWALL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4745_FIREWALL_ROWS.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4745_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4745_STATUS.csv"
NEXT_TARGET_CSV = SOURCE_DIR / "P8_Y5_R2FR_4745_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4745_VALIDATION.csv"

SOURCE_SPECS = [
    ("SRC4745_0_4744_doc", POST / "4744-Y5-R2FR-parent-boundary-trace-contract-or-CzeroMode-source-runner.md", "derive D_adj principal symbol and UCP/ellipticity gate", "4745 handoff"),
    ("SRC4745_1_4744_formal", FORMAL / "760-PPC4161-parent-boundary-trace-contract-or-CzeroMode-source-runner.md", "UCP(D_adj,W_loc)", "formal UCP target"),
    ("SRC4745_2_4744_contract", SOURCE_DIR / "P8_Y5_R2FR_4744_PARENT_BOUNDARY_TRACE_CONTRACT.csv", "PBC4744_1_admissible_class", "parent admissible multiplier contract"),
    ("SRC4745_3_4744_space", SOURCE_DIR / "P8_Y5_R2FR_4744_ADMISSIBLE_MULTIPLIER_SPACE.csv", "ADM4744_1_trace_domain", "H1_0 trace domain"),
    ("SRC4745_4_4744_exact", SOURCE_DIR / "P8_Y5_R2FR_4744_EXACT_BRANCH_AUDIT.csv", "EX4744_3_UCP", "UCP/gap unsigned row"),
    ("SRC4745_5_4744_czero", SOURCE_DIR / "P8_Y5_R2FR_4744_CZEROMODE_SOURCE_RUNNER.csv", "CZR4744_2_physical_kernel", "CzeroMode finite fallback"),
    ("SRC4745_6_4743_theorem", SOURCE_DIR / "P8_Y5_R2FR_4743_KERNEL_KILL_THEOREM.csv", "KKT4743_2_unique_continuation_kill", "kernel kill theorem"),
    ("SRC4745_7_4742_operator", SOURCE_DIR / "P8_Y5_R2FR_4742_ADJOINT_OPERATOR_SETUP.csv", "OP4742_2_operator", "D_adj operator setup"),
    ("SRC4745_8_4742_proof", SOURCE_DIR / "P8_Y5_R2FR_4742_SPECTRAL_GAP_COERCIVITY_PROOF.csv", "PROOF4742_4_exact_zero", "exact zero proof"),
    ("SRC4745_9_4740_action", SOURCE_DIR / "P8_Y5_R2FR_4740_PARENT_TFRI_OWNER_ACTION_BLOCK.csv", "S_TFRI = int sqrt|g|", "parent TFRI action"),
    ("SRC4745_10_4738_parent", SOURCE_DIR / "P8_Y5_R2FR_4738_PARENT_ACTION_OWNER_CONTRACT.csv", "PACT4738_0_owner_field", "parent owner precedent"),
    ("SRC4745_11_4138_tracefree", SOURCE_DIR / "P8_Y5_R2FR_4138_TRACEFREE_SIGNING_AUDIT.csv", "TF4138_1_parent_variation", "trace-free parent variation"),
]

GENERATED_CSVS = [
    SOURCE_REGISTER_CSV,
    SYMBOL_DERIVATION_CSV,
    DN_ELLIPTIC_GATE_CSV,
    LORENTZIAN_AUDIT_CSV,
    PHYSICAL_KERNEL_AUDIT_CSV,
    CZ_BOUND_RUNNER_CSV,
    ROUTE_MATRIX_CSV,
    PROMOTION_GATES_CSV,
    FIREWALL_CSV,
    DECISION_CSV,
    STATUS_CSV,
    NEXT_TARGET_CSV,
]


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def read_text(path_object: Path) -> str:
    return path_object.read_text(encoding="utf-8-sig", errors="replace")


def write_text(path_object: Path, content: str) -> None:
    path_object.parent.mkdir(parents=True, exist_ok=True)
    path_object.write_text(content, encoding="utf-8", newline="\n")


def write_csv(path_object: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"refusing to write empty CSV: {path_object}")
    path_object.parent.mkdir(parents=True, exist_ok=True)
    with path_object.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def append_once(path_object: Path, marker: str, block: str) -> None:
    existing = read_text(path_object) if path_object.exists() else ""
    if marker in existing:
        return
    separator = "" if not existing or existing.endswith("\n") else "\n"
    write_text(path_object, existing + separator + block.rstrip() + "\n")


def parse_csv(path_object: Path) -> bool:
    with path_object.open("r", encoding="utf-8-sig", newline="") as handle:
        list(csv.DictReader(handle))
    return True


def source_register(timestamp: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source_id, path_object, needle, role in SOURCE_SPECS:
        exists = path_object.exists()
        text = read_text(path_object) if exists else ""
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "source_id": source_id,
                "source_path": str(path_object),
                "exists": exists,
                "needle": needle,
                "needle_found": needle in text,
                "role": role,
                "valid_for_claim": False,
                "timestamp_utc": timestamp,
            }
        )
    return rows


def symbol_derivation_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        (
            "SYM4745_0_multiplier_vector",
            "m=(lambda_nu,eta,rho_mn,xi_nu,chi_nu)",
            "Collects the TFRI, DeltaK and quarantine owner multipliers.",
            "DEFINED",
        ),
        (
            "SYM4745_1_R_block",
            "E_R[m] = rho_{mu nu}+eta g_{mu nu}-sym_0(nabla_mu lambda_nu)+lower",
            "Variation of the constrained TFRI block with respect to R_T gives an algebraic/first-order adjoint equation.",
            "SCHEMATIC_FROM_PARENT_ACTION",
        ),
        (
            "SYM4745_2_Gamma_block",
            "E_Gamma[m] = -nabla_nu lambda^nu + lower",
            "Variation of the Gamma_eff channel gives the divergence of lambda.",
            "SCHEMATIC_FROM_PARENT_ACTION",
        ),
        (
            "SYM4745_3_phi_block",
            "E_phi[m] = H_T^dagger rho = nabla_mu nabla_nu rho^{mu nu}-(1/4)Box tr(rho)+lower",
            "Variation of H_T[phi] gives the second-order trace-free Hessian adjoint.",
            "SCHEMATIC_FROM_TRACEFREE_OPERATOR",
        ),
        (
            "SYM4745_4_principal_symbols",
            "sigma_R(k)m = rho+eta g-i sym_0(k tensor lambda); sigma_Gamma(k)m=-i k.lambda; sigma_phi(k)m=(k_mu k_nu-(1/4)g_mn k^2)rho^{mn}",
            "This is the minimal TFRI principal-symbol spine; TT/quarantine blocks still require their own parent components.",
            "MINIMAL_SYMBOL_DERIVED",
        ),
        (
            "SYM4745_5_DN_weights",
            "Use Douglis-Nirenberg weights so algebraic rho/eta terms and first/second derivative blocks are judged together.",
            "The system is mixed-order; ordinary single-order ellipticity is the wrong test.",
            "DN_WEIGHTING_REQUIRED",
        ),
        (
            "SYM4745_6_missing_full_owner_symbol",
            "sigma_TT(k;xi) and sigma_quar(k;chi) are MISSING_PARENT_COMPONENTS",
            "Full D_adj ellipticity cannot be claimed from the TFRI sub-block alone.",
            "MISSING_PARENT_COMPONENTS",
        ),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "symbol_id": symbol_id,
            "formula": formula,
            "meaning": meaning,
            "status": status,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for symbol_id, formula, meaning, status in specs
    ]


def dn_gate_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        (
            "DN4745_0_static_slice",
            "STATIC_PPN_ELLIPTIC_SLICE_ONLY",
            "Replace Lorentzian wave operator by the parent-specified spatial/static local response operator on W_loc^space.",
            "REQUIRED_FOR_SPECTRAL_GAP_ROUTE",
        ),
        (
            "DN4745_1_symbol_injectivity",
            "ker sigma_DN(D_adj)(x,k) cap M_adm = {0} for every spatial k != 0",
            "This is the ellipticity/UCP gate for the static branch.",
            "CONDITIONAL_UNSIGNED",
        ),
        (
            "DN4745_2_complementing_boundary",
            "H^1_0 or strong compact-support boundary data satisfy the complementing condition for the chosen static operator",
            "Boundary trace alone is insufficient unless it is compatible with the principal symbol.",
            "CONDITIONAL_UNSIGNED",
        ),
        (
            "DN4745_3_UCP",
            "DN ellipticity + regular coefficients + connected collar => UCP(D_adj,W_loc^space)",
            "This would make gamma_boundary m=0 kill the static kernel.",
            "THEOREM_ROUTE_CONDITIONAL",
        ),
        (
            "DN4745_4_gap",
            "compact W_loc^space + elliptic self-adjoint L_adj + kernel projected out => lambda_1^adj>0",
            "This supplies the gap used in the 4742 amplitude law.",
            "THEOREM_ROUTE_CONDITIONAL",
        ),
        (
            "DN4745_5_full_owner_gate",
            "TFRI block plus sigma_TT plus sigma_quar must all pass symbol injectivity",
            "Passing the minimal TFRI symbol is not enough for a local-GR claim.",
            "CLOSED_UNTIL_FULL_SYMBOL",
        ),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "gate_id": gate_id,
            "condition": condition,
            "meaning": meaning,
            "status": status,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for gate_id, condition, meaning, status in specs
    ]


def lorentzian_audit_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        (
            "LOR4745_0_null_cone",
            "g^{mu nu}k_mu k_nu=0 has nonzero real k on a Lorentzian collar",
            "Full spacetime principal symbols are characteristic on the null cone.",
            "LORENTZIAN_NOT_UNIFORMLY_ELLIPTIC",
        ),
        (
            "LOR4745_1_no_gap_claim",
            "Do not infer lambda_1^adj>0 from a Lorentzian wave-type operator without converting to an elliptic/static or hyperbolic energy problem.",
            "The spectral-gap proof is not automatically valid for full dynamical GR.",
            "NO_LORENTZIAN_GAP_CLAIM",
        ),
        (
            "LOR4745_2_hyperbolic_route",
            "Use energy estimate on a time slab: E_m(t2) <= E_m(t1)+int source+boundary flux",
            "Dynamical branch should be bounded by hyperbolic energy, not elliptic UCP.",
            "ALTERNATIVE_ROUTE_STAGED",
        ),
        (
            "LOR4745_3_static_tests",
            "PPN/R10/clock/orbital static limits may use the elliptic spatial branch if the parent specifies the reduction before scoring.",
            "This keeps the local test route alive without overclaiming full dynamics.",
            "STATIC_LOCAL_TEST_ROUTE_ALLOWED_CONDITIONALLY",
        ),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "audit_id": audit_id,
            "condition": condition,
            "meaning": meaning,
            "status": status,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for audit_id, condition, meaning, status in specs
    ]


def physical_kernel_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("PK4745_0_tracefree_algebraic", "rho+eta g algebraic kernel", "controlled by E_R if DN weighting and trace constraints are parent-fixed", "CONDITIONAL"),
        ("PK4745_1_lambda_killing", "lambda Killing/vector kernel", "killed by H^1_0 boundary trace plus UCP on static branch", "CONDITIONAL"),
        ("PK4745_2_harmonic_tracefree", "rho harmonic tracefree kernel", "requires H_T^dagger symbol injectivity or finite C_phys_kernel", "UNSIGNED"),
        ("PK4745_3_TT_owner", "xi TT/superpotential kernel", "MISSING_PARENT_COMPONENTS until sigma_TT is written", "MISSING_PARENT_COMPONENTS"),
        ("PK4745_4_quarantine_owner", "chi quarantine kernel", "MISSING_PARENT_COMPONENTS until sigma_quar is written", "MISSING_PARENT_COMPONENTS"),
        ("PK4745_5_physical_bound", "C_phys_kernel", "finite source row required if any physical kernel survives", "MISSING_SOURCE_VALUE"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "kernel_id": kernel_id,
            "mode_family": mode_family,
            "test_or_bound": test_or_bound,
            "status": status,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for kernel_id, mode_family, test_or_bound, status in specs
    ]


def czeromode_bound_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        (
            "CZG4745_0_static_exact_case",
            "if STATIC_PPN_ELLIPTIC_SLICE_ONLY and DN gate passes and C_phys_kernel=0 then C_zeroMode=0",
            "Exact static/local-test kernel kill condition.",
            "CONDITIONAL_EXACT",
        ),
        (
            "CZG4745_1_full_dynamic_case",
            "if Lorentzian branch only then C_zeroMode_dynamic is bounded by hyperbolic energy data, not set to zero",
            "Prevents smuggling elliptic logic into dynamical spacetime.",
            "BOUND_REQUIRED",
        ),
        (
            "CZG4745_2_finite_runner",
            "C_zeroMode <= C_static_fail + C_phys_kernel + C_TT_kernel + C_quar_kernel + C_hyp_energy",
            "Finite fallback if any gate remains unsigned.",
            "NOT_SCORE_READY",
        ),
        (
            "CZG4745_3_amplitude_insert",
            "A_m <= sqrt(C_zeroMode^2 + (C_Dadj^2 + C_boundary)/lambda_1^adj)",
            "Carries the 4745 result back into the 4742 multiplier amplitude law.",
            "SYMBOLIC_NONCLAIM",
        ),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "bound_id": bound_id,
            "formula": formula,
            "meaning": meaning,
            "status": status,
            "score_ready": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for bound_id, formula, meaning, status in specs
    ]


def route_matrix_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("ROUTE4745_0_static_PPN_gap", "derive static spatial elliptic operator and lambda_1^adj lower bound", "best_next_route", "directly targets local PPN/R10/clock/orbital tests"),
        ("ROUTE4745_1_full_owner_symbol", "write sigma_TT and sigma_quar parent components", "parallel_required_route", "needed before claiming full owner D_adj ellipticity"),
        ("ROUTE4745_2_hyperbolic_energy", "derive Lorentzian time-slab energy bound", "dynamic_fallback_route", "needed for full local-GR dynamics"),
        ("ROUTE4745_3_score_now", "score local tests now", "rejected", "operator/gap/kernel components remain unsigned"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "route_id": route_id,
            "route": route,
            "status": status,
            "reason_or_next_requirement": requirement,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for route_id, route, status, requirement in specs
    ]


def promotion_gate_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("GATE4745_0_sources", "All cited 4745 source anchors exist and contain expected text.", "pass_internal", False),
        ("GATE4745_1_symbol_spine", "Minimal TFRI principal symbol spine is written.", "conditional_pass", False),
        ("GATE4745_2_static_branch", "Elliptic/UCP/gap route is allowed only for parent-specified static/spatial local response.", "conditional_open", False),
        ("GATE4745_3_lorentzian_branch", "Full Lorentzian local-GR branch cannot use uniform elliptic gap; needs hyperbolic energy bound.", "closed_unsigned", False),
        ("GATE4745_4_full_owner_symbol", "sigma_TT and sigma_quar remain missing parent components.", "closed_unsigned", False),
        ("GATE4745_5_CzeroMode", "CzeroMode remains finite/nonclaim unless static DN gate plus physical-kernel absence close.", "closed_unsigned", False),
        ("GATE4745_6_no_claim", "No local-GR, Newton, PPN, R10, WEP, clock or orbital claim from 4745.", "closed_firewall", False),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "gate_id": gate_id,
            "gate": gate,
            "status": status,
            "valid_for_claim": valid_for_claim,
            "timestamp_utc": timestamp,
        }
        for gate_id, gate, status, valid_for_claim in specs
    ]


def firewall_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("FW4745_0_no_elliptic_smuggle", "Do not use static elliptic UCP to claim full Lorentzian local GR."),
        ("FW4745_1_no_subblock_claim", "Do not claim full D_adj ellipticity from the TFRI sub-block without TT/quarantine symbols."),
        ("FW4745_2_no_kernel_erasure", "Physical kernels remain as C_phys_kernel unless the symbol/gap proof removes them."),
        ("FW4745_3_no_posthoc_static_slice", "The static/PPN reduction must be parent-specified before scoring."),
        ("FW4745_4_no_github_action", "No GitHub action is performed by this local checkpoint."),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "firewall_id": firewall_id,
            "firewall": firewall,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for firewall_id, firewall in specs
    ]


def decision_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "marker": MARKER,
            "claim_id": CLAIM_ID,
            "decision": DECISION,
            "summary": "4745 derives the minimal TFRI adjoint principal-symbol spine and splits the proof route: static/PPN local tests may use a parent-specified spatial elliptic DN/UCP/gap route, while full Lorentzian dynamics cannot claim uniform elliptic gap and must use a hyperbolic energy bound or finite CzeroMode runner. TT/quarantine owner symbols remain required.",
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "status_id": "STATUS4745_0_local_only",
            "status": "local_only_private_checkpoint",
            "detail": "Generated local post-checkpoint and formalization files only; no GitHub action.",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "status_id": "STATUS4745_1_science_verdict",
            "status": "static_elliptic_route_separated_from_lorentzian_dynamic_route",
            "detail": "The principal-symbol gate prevents elliptic logic from being smuggled into full Lorentzian local GR while preserving a real static local-test route.",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def next_target_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "next_target": NEXT_TARGET,
            "why": "4745 shows the next clean proof fork is static PPN elliptic gap versus Lorentzian hyperbolic energy bound.",
            "preferred_route": "Build the static/spatial local response operator and try to prove a DN elliptic gap for PPN/R10/clock/orbital arenas.",
            "fallback_route": "For full Lorentzian dynamics, derive an energy estimate and carry C_hyp_energy/CzeroMode as finite residuals.",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def bullet(rows: list[dict[str, Any]], id_key: str, text_key: str) -> str:
    return "\n".join(f"- `{row[id_key]}`: {row[text_key]}" for row in rows)


def write_docs(
    timestamp: str,
    symbols: list[dict[str, Any]],
    dn_gates: list[dict[str, Any]],
    lorentzian: list[dict[str, Any]],
    kernels: list[dict[str, Any]],
    bounds: list[dict[str, Any]],
    routes: list[dict[str, Any]],
    gates: list[dict[str, Any]],
) -> None:
    doc = f"""# 4745 Y5 R2FR: Adjoint Principal Symbol UCP Ellipticity Gate Or CzeroMode Bound Runner

Generated: `{timestamp}`

## Summary

- Work is local-only and private.
- This checkpoint derives the minimal TFRI adjoint principal-symbol spine and blocks a common mistake.
- Static local tests may use an elliptic spatial/UCP/gap route **only** if that static reduction is parent-specified before scoring.
- Full Lorentzian dynamics is not uniformly elliptic because of the null cone, so it needs a hyperbolic energy route or a finite residual bound.
- Full owner ellipticity still needs the missing `sigma_TT` and `sigma_quar` parent components.

## Minimal TFRI Principal Symbol

```text
E_R[m] = rho_{{mu nu}} + eta g_{{mu nu}} - sym_0(nabla_mu lambda_nu) + lower
E_Gamma[m] = -nabla_nu lambda^nu + lower
E_phi[m] = H_T^dagger rho
         = nabla_mu nabla_nu rho^{{mu nu}} - (1/4)Box tr(rho) + lower

sigma_R(k)m = rho + eta g - i sym_0(k tensor lambda)
sigma_Gamma(k)m = -i k.lambda
sigma_phi(k)m = (k_mu k_nu - (1/4)g_mn k^2)rho^{{mn}}
```

Because this is mixed order, the correct test is Douglis-Nirenberg symbol injectivity on the admissible multiplier space.

## Symbol Rows

{bullet(symbols, "symbol_id", "formula")}

## DN Ellipticity / UCP Gate

{bullet(dn_gates, "gate_id", "condition")}

## Lorentzian Caution Audit

{bullet(lorentzian, "audit_id", "condition")}

## Physical Kernel Audit

{bullet(kernels, "kernel_id", "mode_family")}

## CzeroMode Bound Runner

{bullet(bounds, "bound_id", "formula")}

## Route Matrix

{bullet(routes, "route_id", "route")}

## Promotion Gates

{bullet(gates, "gate_id", "status")}

## Decision

`{DECISION}`

## Next Target

`{NEXT_TARGET}`
"""
    write_text(DOC_PATH, doc)

    formal = f"""# 761 PPC4161: Adjoint Principal Symbol UCP Ellipticity Gate Or CzeroMode Bound Runner

Generated: `{timestamp}`

## Principal-Symbol Gate

4745 writes the minimal TFRI adjoint symbol:

```text
sigma_R(k)m = rho + eta g - i sym_0(k tensor lambda)
sigma_Gamma(k)m = -i k.lambda
sigma_phi(k)m = (k_mu k_nu - (1/4)g_mn k^2)rho^mn.
```

The correct exact-zero route is a Douglis-Nirenberg ellipticity/UCP/gap theorem on a parent-specified **static spatial** local collar. This can support PPN/R10/clock/orbital local tests if fixed before scoring.

The full Lorentzian branch is different:

```text
g^{{mu nu}}k_mu k_nu=0
```

has nonzero null covectors, so no uniform elliptic gap is claimed for full dynamical local GR. That branch needs a hyperbolic energy estimate or a finite `CzeroMode`/`C_hyp_energy` bound.

Decision: `{DECISION}`

Next: `{NEXT_TARGET}`

Marker: `{MARKER}`
"""
    write_text(FORMAL_PATH, formal)


def update_spine_packet_resume(timestamp: str) -> None:
    spine_block = f"""

## {MARKER}

Generated: `{timestamp}`

- 4745 derives the minimal TFRI adjoint principal-symbol spine: `sigma_R`, `sigma_Gamma`, and `sigma_phi`.
- Because the system is mixed-order, the exact route uses a Douglis-Nirenberg ellipticity/UCP/gap gate on the admissible multiplier space.
- Static PPN/R10/clock/orbital tests may use a parent-specified spatial elliptic route.
- Full Lorentzian local-GR dynamics cannot borrow that elliptic gap; it needs hyperbolic energy control or finite `CzeroMode`.
- `sigma_TT` and `sigma_quar` remain missing parent components before any full owner-operator claim.
- Decision: `{DECISION}`.
"""
    append_once(SPINE_PATH, MARKER, spine_block)

    packet_block = f"""

## {PACKET_MARKER}

Generated: `{timestamp}`

4745 local packet update: the adjoint symbol gate separates the static elliptic local-test route from full Lorentzian dynamics. Next is a static PPN elliptic gap proof or Lorentzian energy bound.

Next: `{NEXT_TARGET}`.
"""
    append_once(PACKET_PATH, PACKET_MARKER, packet_block)

    resume = f"""# Current Local Resume

Updated: `{timestamp}`

## Latest completed checkpoint

`4745-Y5-R2FR-adjoint-principal-symbol-UCP-ellipticity-gate-or-CzeroMode-bound-runner.md`

## Decision

`{DECISION}`

## What moved forward

- Derived the minimal TFRI adjoint principal-symbol spine: `sigma_R`, `sigma_Gamma`, and `sigma_phi`.
- Identified Douglis-Nirenberg mixed-order ellipticity as the correct static/local-test gate.
- Split the proof route: static PPN/R10/clock/orbital can pursue spatial elliptic UCP/gap; full Lorentzian local-GR dynamics needs a hyperbolic energy bound.
- Kept `sigma_TT`, `sigma_quar`, physical kernels, and `CzeroMode` as unsigned/nonclaim components.

## Current target

`{NEXT_TARGET}`

## Local-only note

No GitHub action was performed by this checkpoint.
"""
    write_text(RESUME_PATH, resume)


def add_claim_once(timestamp: str) -> None:
    existing = read_text(CLAIMS_PATH) if CLAIMS_PATH.exists() else ""
    if CLAIM_ID in existing:
        return
    row = [
        CLAIM_ID,
        "local_gr_newton_bridge",
        "4745 derives the minimal TFRI adjoint principal-symbol gate and separates static elliptic local-test proof from full Lorentzian dynamics.",
        "Generated source register, principal-symbol derivation, DN ellipticity/UCP gate, Lorentzian caution audit, physical kernel audit, CzeroMode bound runner, route matrix, gates, firewalls, decision, status, next target and validation.",
        "principal_symbol_gate_static_elliptic_conditional_lorentzian_nonclaim",
        NEXT_TARGET,
        "Using static elliptic UCP to overclaim full Lorentzian local GR, or claiming full owner ellipticity without TT/quarantine symbols.",
        "local_gr",
        str(DOC_PATH),
        NEXT_TARGET,
        "Need static spatial gap proof or Lorentzian hyperbolic energy bound, plus sigma_TT/sigma_quar and physical kernel handling.",
        "Adjoint principal symbol UCP ellipticity gate or CzeroMode bound runner",
        f"{MARKER}; {DECISION}; generated {timestamp}",
    ]
    with CLAIMS_PATH.open("a", encoding="utf-8", newline="") as handle:
        csv.writer(handle).writerow(row)


def cleanup_pycache() -> None:
    pycache = POST / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def validation_rows(
    sources: list[dict[str, Any]],
    symbols: list[dict[str, Any]],
    dn_gates: list[dict[str, Any]],
    lorentzian: list[dict[str, Any]],
    kernels: list[dict[str, Any]],
    bounds: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    timestamp: str,
) -> list[dict[str, Any]]:
    checks: list[tuple[str, str, bool, str]] = []
    checks.append(("VAL4745_0_sources_exist", "all cited source paths exist", all(row["exists"] for row in sources), "source register"))
    checks.append(("VAL4745_1_needles_found", "all source needles found", all(row["needle_found"] for row in sources), "source register"))
    for csv_path in GENERATED_CSVS:
        checks.append((f"VAL4745_csv_{csv_path.stem}", f"{csv_path.name} parses", csv_path.exists() and parse_csv(csv_path), str(csv_path)))
    checks.append(("VAL4745_2_symbol_rows", "symbol rows include sigma_R, sigma_phi, sigma_Gamma", all(any(token in row["formula"] for row in symbols) for token in ["sigma_R", "sigma_phi", "sigma_Gamma"]), str(SYMBOL_DERIVATION_CSV)))
    checks.append(("VAL4745_3_DN_gate", "DN gate contains static elliptic route and full owner gate", any(row["condition"] == "STATIC_PPN_ELLIPTIC_SLICE_ONLY" for row in dn_gates) and any("sigma_TT" in row["condition"] for row in dn_gates), str(DN_ELLIPTIC_GATE_CSV)))
    checks.append(("VAL4745_4_lorentzian_caution", "Lorentzian audit blocks uniform elliptic claim", any(row["status"] == "LORENTZIAN_NOT_UNIFORMLY_ELLIPTIC" for row in lorentzian), str(LORENTZIAN_AUDIT_CSV)))
    checks.append(("VAL4745_5_missing_owner_symbols", "physical kernel audit keeps TT/quarantine symbols missing", all(any(owner in row["mode_family"] and row["status"] == "MISSING_PARENT_COMPONENTS" for row in kernels) for owner in ["TT", "quarantine"]), str(PHYSICAL_KERNEL_AUDIT_CSV)))
    checks.append(("VAL4745_6_CzeroMode_bound", "CzeroMode runner splits static and Lorentzian cases", any("STATIC_PPN_ELLIPTIC_SLICE_ONLY" in row["formula"] for row in bounds) and any("Lorentzian" in row["formula"] for row in bounds), str(CZ_BOUND_RUNNER_CSV)))
    checks.append(("VAL4745_7_gates_nonclaim", "promotion gates keep claim closed", all(row["valid_for_claim"] is False for row in gates), str(PROMOTION_GATES_CSV)))
    checks.append(("VAL4745_8_docs_exist", "post and formal docs exist", DOC_PATH.exists() and FORMAL_PATH.exists(), f"{DOC_PATH}; {FORMAL_PATH}"))
    checks.append(("VAL4745_9_spine_marker", "spine marker appended", MARKER in read_text(SPINE_PATH), str(SPINE_PATH)))
    checks.append(("VAL4745_10_packet_marker", "packet marker appended", PACKET_MARKER in read_text(PACKET_PATH), str(PACKET_PATH)))
    checks.append(("VAL4745_11_claim_row", "claim row L-587 present", CLAIM_ID in read_text(CLAIMS_PATH), str(CLAIMS_PATH)))
    resume_text = read_text(RESUME_PATH)
    checks.append(("VAL4745_12_resume", "resume points from 4745 to 4746", "4745-Y5" in resume_text and "4746-Y5" in resume_text, str(RESUME_PATH)))
    checks.append(("VAL4745_13_pycache_absent", "scripts __pycache__ removed", not (POST / "scripts" / "__pycache__").exists(), str(POST / "scripts")))
    overall = all(item[2] for item in checks)
    rows = [
        {
            "checkpoint": CHECKPOINT,
            "validation_id": validation_id,
            "check": check,
            "status": "PASS" if passed else "FAIL",
            "detail": detail,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for validation_id, check, passed, detail in checks
    ]
    rows.append(
        {
            "checkpoint": CHECKPOINT,
            "validation_id": "VAL4745_OVERALL",
            "check": "all 4745 local generation and nonclaim checks pass",
            "status": "PASS" if overall else "FAIL",
            "detail": DECISION,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    )
    return rows


def main() -> None:
    timestamp = now()
    sources = source_register(timestamp)
    symbols = symbol_derivation_rows(timestamp)
    dn_gates = dn_gate_rows(timestamp)
    lorentzian = lorentzian_audit_rows(timestamp)
    kernels = physical_kernel_rows(timestamp)
    bounds = czeromode_bound_rows(timestamp)
    routes = route_matrix_rows(timestamp)
    gates = promotion_gate_rows(timestamp)
    firewalls = firewall_rows(timestamp)
    decisions = decision_rows(timestamp)
    statuses = status_rows(timestamp)
    next_targets = next_target_rows(timestamp)

    write_csv(SOURCE_REGISTER_CSV, sources)
    write_csv(SYMBOL_DERIVATION_CSV, symbols)
    write_csv(DN_ELLIPTIC_GATE_CSV, dn_gates)
    write_csv(LORENTZIAN_AUDIT_CSV, lorentzian)
    write_csv(PHYSICAL_KERNEL_AUDIT_CSV, kernels)
    write_csv(CZ_BOUND_RUNNER_CSV, bounds)
    write_csv(ROUTE_MATRIX_CSV, routes)
    write_csv(PROMOTION_GATES_CSV, gates)
    write_csv(FIREWALL_CSV, firewalls)
    write_csv(DECISION_CSV, decisions)
    write_csv(STATUS_CSV, statuses)
    write_csv(NEXT_TARGET_CSV, next_targets)
    write_docs(timestamp, symbols, dn_gates, lorentzian, kernels, bounds, routes, gates)
    update_spine_packet_resume(timestamp)
    add_claim_once(timestamp)
    cleanup_pycache()
    write_csv(VALIDATION_CSV, validation_rows(sources, symbols, dn_gates, lorentzian, kernels, bounds, gates, timestamp))


if __name__ == "__main__":
    main()
