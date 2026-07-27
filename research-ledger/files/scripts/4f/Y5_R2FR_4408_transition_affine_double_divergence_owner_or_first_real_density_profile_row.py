from __future__ import annotations

import csv
import shutil
import sys
from datetime import datetime, timezone
from io import StringIO
from pathlib import Path
from typing import Dict, Iterable, List, Tuple


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from Eprofile_source_shadow_gate import evaluate_eprofile_bound_rows, read_csv, write_csv  # noqa: E402
from sigma_s_source_owner_improvement_gate import evaluate_owner_rows  # noqa: E402


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4408"
CLAIM_ID = "L-249"
MARKER = "PPC4161_TRANSITION_AFFINE_DOUBLE_DIVERGENCE_OWNER_OR_FIRST_REAL_DENSITY_PROFILE_ROW_4408"
PACKET_MARKER = "PPC4161_PACKET_TRANSITION_AFFINE_DOUBLE_DIVERGENCE_OWNER_OR_FIRST_REAL_DENSITY_PROFILE_ROW_4408"
DECISION = "SIGMAS_ELECTRIC_U_OWNER_CONTRACT_DERIVED_LAMBDA_CURVATURE_PAYLOAD_EXPOSED_NONCLAIM"
NEXT_TARGET = "4409-Y5-R2FR-transition-lambda-curvature-payload-cancellation-or-first-real-density-profile-row.md"

FORMAL_PATH = FORMAL / "424-PPC4161-transition-affine-double-divergence-owner-or-first-real-density-profile-row.md"
DOC_PATH = POST / "4408-Y5-R2FR-transition-affine-double-divergence-owner-or-first-real-density-profile-row.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4408_VALIDATION.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
OWNER_GATE_PATH = SCRIPT_DIR / "sigma_s_source_owner_improvement_gate.py"
EPROFILE_GATE_PATH = SCRIPT_DIR / "Eprofile_source_shadow_gate.py"

OWNER_INPUT = SOURCE_DIR / "P8_Y5_R2FR_4408_SIGMAS_ELECTRIC_OWNER_INPUT.csv"
OWNER_OUTPUT = SOURCE_DIR / "P8_Y5_R2FR_4408_SIGMAS_ELECTRIC_OWNER_OUTPUT.csv"
PROFILE_INPUT = SOURCE_DIR / "P8_Y5_R2FR_4408_FIRST_PROFILE_ROW_INPUT.csv"
PROFILE_OUTPUT = SOURCE_DIR / "P8_Y5_R2FR_4408_FIRST_PROFILE_ROW_OUTPUT.csv"

STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

NEXT_4407 = SOURCE_DIR / "P8_Y5_R2FR_4407_NEXT_TARGET.csv"
FORMAL_423 = FORMAL / "423-PPC4161-transition-density-profile-owner-or-Eprofile-source-shadow-gate.md"
FORMAL_406 = FORMAL / "406-PPC4161-transition-U-action-owner-construction-or-pressure-curvature-bound-row.md"
FORMAL_408 = FORMAL / "408-PPC4161-transition-sigmaS-residual-owner-or-electric-U-bound-row.md"
FORMAL_409 = FORMAL / "409-PPC4161-transition-sigmaS-parent-action-signature-or-first-residual-bound-row.md"
FORMAL_416 = FORMAL / "416-PPC4161-transition-composite-US-parent-functional-or-finite-payload-vector-runner.md"
FORMAL_418 = FORMAL / "418-PPC4161-transition-Ricci-uu-local-vacuum-equation-or-first-real-Etrace-bound-row.md"
FORMAL_419 = FORMAL / "419-PPC4161-transition-Lambda-eff-residual-zero-or-local-cosmological-payload-bound.md"

SOURCES: Dict[str, Tuple[Path, str, str]] = {
    "SRC4408_00_4407_next": (
        NEXT_4407,
        "4408-Y5-R2FR-transition-affine-double-divergence-owner-or-first-real-density-profile-row.md",
        "4407 handoff to affine double-divergence owner or real density-profile row.",
    ),
    "SRC4408_01_4407_formal": (
        FORMAL_423,
        "birth-certify the affine/double-divergence topological owner",
        "4407 selects the least-circular remaining route.",
    ),
    "SRC4408_02_electric_U": (
        FORMAL_406,
        "U^{0i0j}=S^{ij}",
        "4390 electric projector supplies the required density-owner slot.",
    ),
    "SRC4408_03_electric_density": (
        FORMAL_406,
        "Delta rho ~ c^-2 partial_i partial_j S^{ij}",
        "4390 connects electric U to the weak-static density projection.",
    ),
    "SRC4408_04_sigma_owner": (
        FORMAL_408,
        "rho_top-rho_H = Delta_h sigma_S",
        "4392 trace-electric sigma route gives the owner identity to sign.",
    ),
    "SRC4408_05_sigma_Sij": (
        FORMAL_408,
        "S^{ij} = c^2 h^{ij} sigma_S",
        "4392 maps sigma_S into the electric U spatial tensor.",
    ),
    "SRC4408_06_sigma_action": (
        FORMAL_409,
        "S_sigma_lambda = int_W sqrt(h) lambda_S",
        "4393 writes the sigma/lambda parent action signature.",
    ),
    "SRC4408_07_multiplier_null": (
        FORMAL_409,
        "Delta_h lambda_S=0",
        "4393 multiplier-null lemma to prevent hidden multiplier stress.",
    ),
    "SRC4408_08_composite_payload": (
        FORMAL_416,
        "curvature-sourced rather than automatically zero",
        "4400 shows U[sigma]R sources lambda_S unless cancelled or bounded.",
    ),
    "SRC4408_09_ricci_payload": (
        FORMAL_418,
        "R_uu = E_res_uu - 1/2 g_uu E_res + Lambda_eff g_uu",
        "4402 names the local curvature source branch.",
    ),
    "SRC4408_10_survivor_vector": (
        FORMAL_419,
        "retained local residual payload is c_Gamma, c_R2/M_R, Lambda_eff",
        "4403 factors the local residual vector that can feed lambda curvature payload.",
    ),
    "SRC4408_11_owner_gate": (
        OWNER_GATE_PATH,
        "def evaluate_owner_rows",
        "Executable sigma/electric source-owner improvement gate.",
    ),
    "SRC4408_12_eprofile_gate": (
        EPROFILE_GATE_PATH,
        "def evaluate_eprofile_bound_rows",
        "Executable first real density-profile row fallback gate.",
    ),
}


def text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def locate(path: Path, needle: str) -> Tuple[bool, int]:
    if not path.exists():
        return False, -1
    for line_number, line in enumerate(text(path).splitlines(), 1):
        if needle in line:
            return True, line_number
    return False, -1


def csv_line(row: Iterable[str]) -> str:
    buffer = StringIO()
    writer = csv.writer(buffer, lineterminator="\n")
    writer.writerow(list(row))
    return buffer.getvalue()


def md_cell(value: object) -> str:
    return str(value).replace("|", r"\|").replace("\n", "<br>")


def markdown_table(rows: List[Dict[str, object]]) -> str:
    if not rows:
        return ""
    fields = list(rows[0].keys())
    lines = ["| " + " | ".join(fields) + " |", "| " + " | ".join("---" for _ in fields) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(md_cell(row.get(field, "")) for field in fields) + " |")
    return "\n".join(lines)


def append_once(path: Path, marker: str, block: str) -> None:
    current = text(path)
    if marker in current:
        return
    path.write_text(current.rstrip() + "\n\n" + block.strip() + "\n", encoding="utf-8")


def append_claim_once(path: Path, claim_id: str, row: List[str]) -> None:
    current = text(path)
    if f"\n{claim_id}," in current:
        return
    if current and not current.endswith("\n"):
        current += "\n"
    path.write_text(current + csv_line(row), encoding="utf-8")


def source_rows() -> List[Dict[str, object]]:
    rows: List[Dict[str, object]] = []
    for source_id, (path, needle, role) in SOURCES.items():
        found, line_number = locate(path, needle)
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "source_id": source_id,
                "path": str(path),
                "path_exists": path.exists(),
                "needle": needle,
                "needle_found": found,
                "line_number": line_number,
                "role": role,
                "valid_for_claim": False,
            }
        )
    return rows


def derivation_rows() -> List[Dict[str, object]]:
    return [
        {
            "derivation_id": "ADDO4408_0_sigma_electric_owner_contract",
            "object": "rho_top-rho_H owner identity",
            "statement": "Candidate parent contract: S_owner=int_W sqrt(h) lambda_S(Delta_h sigma_S-(rho_top-rho_H)) plus S_U=1/2 int_M sqrt(-g) U[u,h,sigma_S]Riemann, with S^{ij}=c^2h^{ij}sigma_S.",
            "derivation": "Variation with respect to lambda_S gives Delta_h sigma_S=rho_top-rho_H. The electric U projector has U^{0i0j}=S^{ij}; therefore c^-2 D_iD_jS^{ij}=rho_top-rho_H up to explicit connection/curvature terms.",
            "result": "This is the first compact owner contract joining the density-profile route to the electric U action route.",
            "status": "CONSTRUCTIVE_CONTRACT_DERIVED_PARENT_UNSIGNED",
            "valid_for_claim": False,
        },
        {
            "derivation_id": "ADDO4408_1_affine_annihilator_theorem",
            "object": "affine moments",
            "statement": "If rho_top-rho_H=c^-2D_iD_jS^{ij} and the affine boundary pairings vanish, then constants and linear test functions see zero residual.",
            "derivation": "Integrate by parts twice. For f in Aff_1(W_H), D_iD_jf=0, so only boundary terms remain; silent boundary pairings kill the monopole and first moment.",
            "result": "This gives a real affine/local-center mechanism, but not full distributional profile equality.",
            "status": "EXACT_AFFINE_THEOREM_RESTATED_AS_OWNER_CONSEQUENCE",
            "valid_for_claim": False,
        },
        {
            "derivation_id": "ADDO4408_2_multiplier_null_guard",
            "object": "lambda_S stress payload",
            "statement": "The sigma constraint leaves no hidden multiplier stress only if lambda_S=0 by elliptic uniqueness or its nonzero branch is explicitly bounded.",
            "derivation": "In the uncoupled constraint, variation with respect to sigma_S gives Delta_h lambda_S=0. Anchored Dirichlet data or a fixed zero-mode Neumann branch forces lambda_S=0 by the energy identity.",
            "result": "This blocks the closure cheat where lambda_S enforces the profile identity while silently carrying stress.",
            "status": "CONDITIONAL_MULTIPLIER_NULL_LEMMA_IMPORTED",
            "valid_for_claim": False,
        },
        {
            "derivation_id": "ADDO4408_3_curvature_source_obstruction",
            "object": "U[sigma]R coupled branch",
            "statement": "Once S_U[U(sigma_S)] is added, the sigma variation sources lambda_S through the electric curvature projection unless a parent cancellation or finite bound is supplied.",
            "derivation": "The composite action gives Delta_h^dagger lambda_S = -1/2 Pi_W[(sqrt(-g)/sqrt(h))R_{mu alpha nu beta} partial U^{mu alpha nu beta}/partial sigma_S] plus boundary/projector terms.",
            "result": "The next target is not another source sweep; it is lambda-curvature cancellation/bounding or a real profile row.",
            "status": "REAL_OBSTRUCTION_EXPOSED",
            "valid_for_claim": False,
        },
        {
            "derivation_id": "ADDO4408_4_profile_row_fallback",
            "object": "first real density-profile row",
            "statement": "If the parent sigma/electric owner contract remains unsigned, the fallback is a same-worldtube rho_H/rho_eff or sigma_shadow_perp/E_top_profile row feeding K_N(s)E_profile.",
            "derivation": "4407 already made E_profile scoreable as E_shadow+E_top_profile+E_nonHilbert_profile+E_readout_profile.",
            "result": "The fallback is no longer vague: a real row must carry source path, tau/coframe, support, delta_N, K_N and no-cancellation components.",
            "status": "FALLBACK_SCHEMA_EXACT",
            "valid_for_claim": False,
        },
    ]


def owner_input_rows() -> List[Dict[str, object]]:
    return [
        {
            "candidate_id": "SOI4408_0_current_sigma_electric_contract",
            "route": "sigma_constraint_plus_electric_U",
            "parent_delta_source_declared": True,
            "topological_density_before_readout": False,
            "hilbert_density_before_readout": False,
            "common_tau_coframe_support": True,
            "stress_improvement_U_owned": False,
            "riemann_symmetry_or_electric_projector": True,
            "deltaT_double_divergence_identity": True,
            "density_projection_matches_delta_rho": True,
            "sigma_constraint_links_improvement": True,
            "ward_conservation_or_exchange_current": False,
            "boundary_mass_silence": False,
            "em_double_count_guard": True,
            "no_post_readout_fit": True,
            "parent_authority": "UNSIGNED_PARENT_CONTRACT",
            "source_path": str(FORMAL_409),
            "input_valid_for_claim": False,
            "notes": "mechanism ready but source-owner, U-owner, Ward, boundary and parent authority clauses are unsigned",
        },
        {
            "candidate_id": "SOI4408_1_future_parent_signed_contract_smoke",
            "route": "future_parent_signed_sigma_electric_owner",
            "parent_delta_source_declared": True,
            "topological_density_before_readout": True,
            "hilbert_density_before_readout": True,
            "common_tau_coframe_support": True,
            "stress_improvement_U_owned": True,
            "riemann_symmetry_or_electric_projector": True,
            "deltaT_double_divergence_identity": True,
            "density_projection_matches_delta_rho": True,
            "sigma_constraint_links_improvement": True,
            "ward_conservation_or_exchange_current": True,
            "boundary_mass_silence": True,
            "em_double_count_guard": True,
            "no_post_readout_fit": True,
            "parent_authority": "PARENT_SIGNED_SIGMA_ELECTRIC_OWNER_SMOKE",
            "source_path": str(FORMAL_409),
            "input_valid_for_claim": False,
            "notes": "smoke row proves the gate can recognize the full contract but cannot become evidence",
        },
        {
            "candidate_id": "SOI4408_2_post_readout_green_inverse_refused",
            "route": "post_readout_green_inverse",
            "parent_delta_source_declared": True,
            "topological_density_before_readout": False,
            "hilbert_density_before_readout": True,
            "common_tau_coframe_support": False,
            "stress_improvement_U_owned": False,
            "riemann_symmetry_or_electric_projector": False,
            "deltaT_double_divergence_identity": False,
            "density_projection_matches_delta_rho": True,
            "sigma_constraint_links_improvement": False,
            "ward_conservation_or_exchange_current": False,
            "boundary_mass_silence": False,
            "em_double_count_guard": True,
            "no_post_readout_fit": False,
            "parent_authority": "REJECTED_POST_READOUT_FIT",
            "source_path": str(FORMAL_408),
            "input_valid_for_claim": False,
            "notes": "Green inversion after rho_top-rho_H is known is a representation/bound tool, not a derivation",
        },
    ]


def profile_input_rows() -> List[Dict[str, object]]:
    return [
        {
            "bound_id": "FPR4408_0_missing_real_density_profile_row",
            "arena": "Newton_source_profile",
            "branch": "first_real_profile_row_required",
            "source_path": str(FORMAL_423),
            "K_N": "0.00943177578696",
            "delta_N": "MISSING_DELTA_N",
            "E_shadow": "MISSING_E_SHADOW",
            "E_top_profile": "MISSING_E_TOP_PROFILE",
            "E_nonHilbert_profile": "MISSING_E_NONHILBERT_PROFILE",
            "E_readout_profile": "MISSING_E_READOUT_PROFILE",
            "input_valid_for_claim": False,
        },
        {
            "bound_id": "FPR4408_1_sigma_owner_zero_smoke",
            "arena": "Newton_source_profile",
            "branch": "sigma_owner_profile_zero_smoke",
            "source_path": str(EPROFILE_GATE_PATH),
            "K_N": "0.00943177578696",
            "delta_N": "1e-5",
            "E_shadow": "0",
            "E_top_profile": "0",
            "E_nonHilbert_profile": "0",
            "E_readout_profile": "0",
            "input_valid_for_claim": False,
        },
        {
            "bound_id": "FPR4408_2_affine_not_full_profile_control",
            "arena": "Newton_source_profile",
            "branch": "affine_first_moment_not_full_profile",
            "source_path": str(EPROFILE_GATE_PATH),
            "K_N": "0.00943177578696",
            "delta_N": "1e-5",
            "E_shadow": "0",
            "E_top_profile": "0.002",
            "E_nonHilbert_profile": "0",
            "E_readout_profile": "0",
            "input_valid_for_claim": False,
        },
    ]


def claim_gate_rows() -> List[Dict[str, object]]:
    return [
        {
            "gate_id": "G4408_0_sigma_electric_owner",
            "gate": "parent_sigma_electric_density_owner",
            "claim_allowed": False,
            "reason": "source-owner, U-owner, Ward, boundary, parent authority and live input validity are unsigned.",
        },
        {
            "gate_id": "G4408_1_lambda_curvature_payload",
            "gate": "lambda_S_null_or_bounded",
            "claim_allowed": False,
            "reason": "U[sigma]R curvature source for lambda_S is exposed but not cancelled or bounded.",
        },
        {
            "gate_id": "G4408_2_affine_not_full_profile",
            "gate": "affine_double_divergence_silence",
            "claim_allowed": False,
            "reason": "affine silence can kill monopole/first moment but not full E_profile without higher profile control.",
        },
        {
            "gate_id": "G4408_3_local_GR_Newton",
            "gate": "local_GR_Newton_PPN_R10",
            "claim_allowed": False,
            "reason": "density-profile owner and finite local payload gates remain nonclaim.",
        },
    ]


def decision_rows() -> List[Dict[str, object]]:
    return [
        {
            "decision_id": "DEC4408_0",
            "decision": DECISION,
            "summary": "4408 takes the constructive leap: the best affine/double-divergence owner route is a sigma_S constraint welded to the electric U projector. If the parent owns delta rho_topH=rho_top-rho_H before readout and imposes Delta_h sigma_S=delta rho_topH, then S^{ij}=c^2h^{ij}sigma_S gives c^-2D_iD_jS^{ij}=delta rho_topH and feeds U^{0i0j}=S^{ij}. This would birth-certify the double-divergence density owner. It still does not claim local GR because coupling U[sigma]R sources lambda_S by an electric-curvature term unless parent-cancelled or bounded, and affine silence is weaker than full profile equality. Next target: cancel/bound lambda-curvature payload or fill the first real density-profile row.",
            "claim_allowed": False,
            "valid_for_claim": False,
        }
    ]


def status_rows() -> List[Dict[str, object]]:
    return [
        {
            "status_id": "STAT4408_0",
            "item": "owner route",
            "status": "SIGMAS_ELECTRIC_U_CONTRACT_DERIVED",
            "notes": "sigma_S constraint plus electric U projector is the best current derivation route.",
        },
        {
            "status_id": "STAT4408_1",
            "item": "obstruction",
            "status": "LAMBDA_CURVATURE_PAYLOAD_OPEN",
            "notes": "U[sigma]R sources lambda_S unless cancelled or bounded.",
        },
        {
            "status_id": "STAT4408_2",
            "item": "fallback",
            "status": "FIRST_REAL_PROFILE_ROW_READY",
            "notes": "same-worldtube density profile row can now feed the 4407 Eprofile gate.",
        },
        {
            "status_id": "STAT4408_3",
            "item": "next target",
            "status": "LAMBDA_PAYLOAD_OR_PROFILE_ROW_NEXT",
            "notes": NEXT_TARGET,
        },
    ]


def next_target_rows() -> List[Dict[str, object]]:
    return [
        {
            "next_id": "NT4408_0",
            "target": NEXT_TARGET,
            "question": "Can the lambda_S curvature source from U[sigma]R be parent-cancelled/bounded, or must we import the first real same-worldtube density-profile row?",
            "preferred_route": "derive a cancellation or finite elliptic payload bound for Delta_h^dagger lambda_S sourced by the electric curvature projection on the same support.",
            "fallback_route": "fill a real rho_H/rho_eff or sigma_shadow_perp/E_top_profile row with source path, tau/coframe support, K_N, delta_N, and no-cancellation components.",
            "avoid": "claiming from the sigma constraint alone, using post-readout Green inversion as proof, or treating affine first-moment silence as full E_profile=0.",
            "valid_for_claim": False,
        }
    ]


def write_formal_doc(
    sources: List[Dict[str, object]],
    derivations: List[Dict[str, object]],
    owner_output: List[Dict[str, object]],
    profile_output: List[Dict[str, object]],
    gates: List[Dict[str, object]],
    decisions: List[Dict[str, object]],
    next_targets: List[Dict[str, object]],
) -> None:
    FORMAL_PATH.write_text(
        f"""# 424 PPC4161 transition affine double-divergence owner or first real density-profile row

Marker: `{MARKER}`

Generated UTC: `{STAMP}`

Decision: `{DECISION}`

## Claim Status

Private nonclaim. This checkpoint does not prove public local GR, Newtonian mechanics, Maxwell/EM closure, calibrated `G_N`, R10, PPN, clock, orbital, WEP, or full local-vacuum safety.

## Constructive Result

4408 does not merely say the owner is missing. It constructs the least-circular current owner contract:

```text
S_owner = int_W sqrt(h) lambda_S (Delta_h sigma_S - (rho_top-rho_H)),
S_U     = 1/2 int_M sqrt(-g) U[u,h,sigma_S]^{{mu alpha nu beta}} R_{{mu alpha nu beta}},
S^{{ij}}  = c^2 h^{{ij}} sigma_S.
```

Then:

```text
delta_{{lambda_S}} S_owner = 0
=> Delta_h sigma_S = rho_top-rho_H,

U^{{0i0j}}=S^{{ij}}
=> c^-2 D_iD_j S^{{ij}} = rho_top-rho_H + explicit connection/curvature payload.
```

This is the strongest owner route currently available: a sigma constraint births the density residual, and the electric U projector carries it into the double-divergence stress-improvement slot.

## Why It Still Does Not Claim

The route breaks at a real equation, not vibes:

```text
Delta_h^dagger lambda_S
= -1/2 Pi_W[(sqrt(-g)/sqrt(h)) R_{{mu alpha nu beta}}
            partial U^{{mu alpha nu beta}}/partial sigma_S]
  + boundary/projector terms.
```

So the clean multiplier-null lemma is no longer free after coupling to `U[sigma]R`. The next proof must cancel or bound this lambda-curvature payload. If it cannot, we must fill a real density-profile row.

Also, affine double-divergence silence is not full profile equality: it kills monopole and first moment under boundary silence, but higher moments or a coarse `E_top_profile` norm still need proof or data.

## Source Register

{markdown_table(sources)}

## Derivation Rows

{markdown_table(derivations)}

## Sigma/Electric Owner Gate Output

{markdown_table(owner_output)}

## First Profile Row Fallback Output

{markdown_table(profile_output)}

## Claim Gates

{markdown_table(gates)}

## Decision

{markdown_table(decisions)}

## Next Target

{markdown_table(next_targets)}
""",
        encoding="utf-8",
    )


def write_post_doc(decisions: List[Dict[str, object]], next_targets: List[Dict[str, object]]) -> None:
    DOC_PATH.write_text(
        f"""# 4408 affine double-divergence owner or first real density-profile row

Marker: `{MARKER}`

## Private outcome

4408 constructs the best current owner route:

```text
Delta_h sigma_S = rho_top-rho_H,
S^{{ij}}=c^2h^{{ij}}sigma_S,
U^{{0i0j}}=S^{{ij}}.
```

That gives the desired double-divergence density owner, but coupling it to `U[sigma]R` opens a lambda-curvature payload. No claim fires.

## Decision

{markdown_table(decisions)}

## Next

{markdown_table(next_targets)}
""",
        encoding="utf-8",
    )


def update_spine() -> None:
    append_once(
        SPINE_PATH,
        MARKER,
        f"""## 4408 local spine update: sigma/electric U density owner contract

Marker: `{MARKER}`

Spine update: the best local-GR derivation route is now a concrete sigma/electric U owner contract. A parent-owned `Delta_h sigma_S=rho_top-rho_H` before readout, with `S^ij=c^2h^ij sigma_S` and electric `U^{{0i0j}}=S^ij`, would birth-certify the double-divergence density owner. The open obstruction is equally concrete: `U[sigma]R` sources `lambda_S` through the electric curvature projection unless cancelled or bounded. If that route fails, the first real density-profile row feeds the 4407 `E_profile` gate.
""",
    )


def update_packet() -> None:
    append_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""## 4408 packet update: affine owner construction

Marker: `{PACKET_MARKER}`

Packet update: 4408 converts the affine/double-divergence owner problem into the sigma/electric U contract. This is the current best derivation path, not closure: the parent must own the source residual before readout, the sigma constraint, the electric U projector, the multiplier-null or bounded lambda branch, Ward conservation, and boundary silence.
""",
    )


def update_claims() -> None:
    append_claim_once(
        CLAIMS_PATH,
        CLAIM_ID,
        [
            CLAIM_ID,
            "local_gr",
            "4408 constructs the current best affine/double-divergence density-owner route: a parent sigma_S constraint Delta_h sigma_S=rho_top-rho_H welded to the electric U projector with S^{ij}=c^2h^{ij}sigma_S and U^{0i0j}=S^{ij}. This would birth-certify c^-2D_iD_jS^{ij}=rho_top-rho_H before readout. The branch remains nonclaim because U[sigma]R sources lambda_S through an electric-curvature term unless cancelled or bounded, and affine silence is weaker than full E_profile equality. No local-GR/Newton/PPN/R10/clock/orbital claim fires.",
            "4408 source register, derivation rows, sigma/electric owner gate, first profile-row fallback gate, claim gates, decision, status, next target and validation CSV.",
            "sigmaS_electric_U_owner_contract_derived_lambda_curvature_payload_open_nonclaim",
            "Cancel or bound the lambda_S curvature source, or fill the first real same-worldtube density-profile row.",
            "Claiming from the sigma constraint alone, using post-readout Green inversion as proof, or treating affine first-moment silence as full E_profile=0.",
        ],
    )


def validation_rows(csv_paths: List[Path]) -> List[Dict[str, object]]:
    sources = read_csv(SOURCE_DIR / "P8_Y5_R2FR_4408_SOURCE_REGISTER.csv")
    derivations = read_csv(SOURCE_DIR / "P8_Y5_R2FR_4408_DERIVATIONS.csv")
    owner_output = read_csv(OWNER_OUTPUT)
    profile_output = read_csv(PROFILE_OUTPUT)
    gates = read_csv(SOURCE_DIR / "P8_Y5_R2FR_4408_CLAIM_GATES.csv")
    rows: List[Dict[str, object]] = []

    def add(check_id: str, passed: bool, detail: str) -> None:
        rows.append({"checkpoint": CHECKPOINT, "check_id": check_id, "passed": passed, "detail": detail})

    add("VAL4408_0_sources_exist", all(row["path_exists"] == "True" for row in sources), "every cited source exists")
    add("VAL4408_1_needles_found", all(row["needle_found"] == "True" for row in sources), "every cited source needle resolves")
    add("VAL4408_2_derivations_written", len(derivations) >= 5, "derivation rows written")
    add("VAL4408_3_current_owner_mechanism_ready_but_unsigned", any(row["candidate_id"] == "SOI4408_0_current_sigma_electric_contract" and row["improvement_ready"] == "True" and row["owner_certificate_ready"] == "False" for row in owner_output), "current sigma/electric mechanism ready but unsigned")
    add("VAL4408_4_future_owner_smoke_nonclaim", any(row["candidate_id"] == "SOI4408_1_future_parent_signed_contract_smoke" and row["source_owner_ready"] == "True" and row["improvement_ready"] == "True" and row["claim_allowed"] == "False" for row in owner_output), "future full owner smoke remains nonclaim")
    add("VAL4408_5_post_readout_green_refused", any(row["candidate_id"] == "SOI4408_2_post_readout_green_inverse_refused" and row["owner_certificate_ready"] == "False" for row in owner_output), "post-readout Green inverse is refused")
    add("VAL4408_6_missing_profile_row_blocks", any(row["bound_id"] == "FPR4408_0_missing_real_density_profile_row" and row["current_status"] == "EPROFILE_BOUND_BLOCKED" for row in profile_output), "missing real density profile row blocks")
    add("VAL4408_7_zero_profile_smoke_nonclaim", any(row["bound_id"] == "FPR4408_1_sigma_owner_zero_smoke" and row["within_bound"] == "True" and row["claim_allowed"] == "False" for row in profile_output), "zero profile smoke passes but remains nonclaim")
    add("VAL4408_8_affine_not_full_profile_control_fails", any(row["bound_id"] == "FPR4408_2_affine_not_full_profile_control" and row["current_status"] == "EPROFILE_BOUND_FAILS" for row in profile_output), "affine-not-full-profile failure control detected")
    add("VAL4408_9_claim_gates_false", all(row["claim_allowed"] == "False" for row in gates), "claim gates false")
    add("VAL4408_10_formal_marker", MARKER in text(FORMAL_PATH), "formal marker present")
    add("VAL4408_11_post_marker", MARKER in text(DOC_PATH), "post marker present")
    add("VAL4408_12_spine_marker", MARKER in text(SPINE_PATH), "spine marker present")
    add("VAL4408_13_packet_marker", PACKET_MARKER in text(PACKET_PATH), "packet marker present")
    add("VAL4408_14_claim_row", f"\n{CLAIM_ID}," in text(CLAIMS_PATH), "claim row present")
    add("VAL4408_15_csv_parse", all(len(read_csv(path)) > 0 for path in csv_paths), "all generated CSVs parse")
    add("VAL4408_16_generated_nonclaim", all(row.get("valid_for_claim", "False") == "False" for path in csv_paths for row in read_csv(path)), "generated rows stay nonclaim")
    add("VAL4408_17_gate_scripts_exist", OWNER_GATE_PATH.exists() and EPROFILE_GATE_PATH.exists(), "owner and profile gate scripts exist")
    add("VAL4408_18_pycache_absent", not (SCRIPT_DIR / "__pycache__").exists(), "scripts __pycache__ absent")
    return rows


def remove_pycache() -> None:
    pycache = SCRIPT_DIR / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def main() -> None:
    sources = source_rows()
    derivations = derivation_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    statuses = status_rows()
    next_targets = next_target_rows()
    csv_paths: List[Path] = []
    csv_payloads: Dict[str, List[Dict[str, object]]] = {
        "P8_Y5_R2FR_4408_SOURCE_REGISTER.csv": sources,
        "P8_Y5_R2FR_4408_DERIVATIONS.csv": derivations,
        "P8_Y5_R2FR_4408_CLAIM_GATES.csv": gates,
        "P8_Y5_R2FR_4408_DECISION.csv": decisions,
        "P8_Y5_R2FR_4408_STATUS.csv": statuses,
        "P8_Y5_R2FR_4408_NEXT_TARGET.csv": next_targets,
    }
    for filename, rows in csv_payloads.items():
        path = SOURCE_DIR / filename
        write_csv(path, rows)
        csv_paths.append(path)

    write_csv(OWNER_INPUT, owner_input_rows())
    owner_output = evaluate_owner_rows(OWNER_INPUT)
    write_csv(OWNER_OUTPUT, owner_output)
    csv_paths.extend([OWNER_INPUT, OWNER_OUTPUT])

    write_csv(PROFILE_INPUT, profile_input_rows())
    profile_output = evaluate_eprofile_bound_rows(PROFILE_INPUT)
    write_csv(PROFILE_OUTPUT, profile_output)
    csv_paths.extend([PROFILE_INPUT, PROFILE_OUTPUT])

    write_formal_doc(sources, derivations, owner_output, profile_output, gates, decisions, next_targets)
    write_post_doc(decisions, next_targets)
    update_spine()
    update_packet()
    update_claims()
    remove_pycache()
    write_csv(VALIDATION_PATH, validation_rows(csv_paths))


if __name__ == "__main__":
    main()
