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

from Eprofile_source_shadow_gate import (  # noqa: E402
    evaluate_eprofile_bound_rows,
    evaluate_profile_zero_rows,
    read_csv,
    write_csv,
)


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4407"
CLAIM_ID = "L-248"
MARKER = "PPC4161_TRANSITION_DENSITY_PROFILE_OWNER_OR_EPROFILE_SOURCE_SHADOW_GATE_4407"
PACKET_MARKER = "PPC4161_PACKET_TRANSITION_DENSITY_PROFILE_OWNER_OR_EPROFILE_SOURCE_SHADOW_GATE_4407"
DECISION = "EPROFILE_SOURCE_SHADOW_GRAMMAR_AND_PROFILE_BOUND_GATE_READY_PARENT_ZERO_UNSIGNED_NONCLAIM"
NEXT_TARGET = "4408-Y5-R2FR-transition-affine-double-divergence-owner-or-first-real-density-profile-row.md"

FORMAL_PATH = FORMAL / "423-PPC4161-transition-density-profile-owner-or-Eprofile-source-shadow-gate.md"
DOC_PATH = POST / "4407-Y5-R2FR-transition-density-profile-owner-or-Eprofile-source-shadow-gate.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4407_VALIDATION.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
GATE_PATH = SCRIPT_DIR / "Eprofile_source_shadow_gate.py"

PROFILE_ZERO_INPUT = SOURCE_DIR / "P8_Y5_R2FR_4407_PROFILE_ZERO_INPUT.csv"
PROFILE_ZERO_OUTPUT = SOURCE_DIR / "P8_Y5_R2FR_4407_PROFILE_ZERO_OUTPUT.csv"
EPROFILE_BOUND_INPUT = SOURCE_DIR / "P8_Y5_R2FR_4407_EPROFILE_BOUND_INPUT.csv"
EPROFILE_BOUND_OUTPUT = SOURCE_DIR / "P8_Y5_R2FR_4407_EPROFILE_BOUND_OUTPUT.csv"

STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

NEXT_4406 = SOURCE_DIR / "P8_Y5_R2FR_4406_NEXT_TARGET.csv"
FORMAL_422 = FORMAL / "422-PPC4161-transition-source-charge-coupling-gate-import-or-epsilonGsrc-bound-runner.md"
FORMAL_391 = FORMAL / "391-PPC4161-transition-density-profile-owner-or-Emass-numeric-source-bound.md"
FORMAL_392 = FORMAL / "392-PPC4161-transition-source-shadow-ban-or-Eprofile-first-source-density-row.md"
FORMAL_393 = FORMAL / "393-PPC4161-transition-parent-grammar-no-source-shadow-or-topological-profile-equality.md"
FORMAL_402 = FORMAL / "402-PPC4161-transition-affine-annihilator-parent-signature-or-real-profile-row.md"
FORMAL_403 = FORMAL / "403-PPC4161-transition-double-divergence-improvement-parent-owner-or-boundary-row.md"

SOURCES: Dict[str, Tuple[Path, str, str]] = {
    "SRC4407_00_4406_next": (
        NEXT_4406,
        "sigma_shadow_perp",
        "4406 routes the current source-coupling chain to density-profile ownership.",
    ),
    "SRC4407_01_4406_formal": (
        FORMAL_422,
        "The current obstruction is no longer generic coupling",
        "4406 names E_profile as the current obstruction after epsilon_Gsrc import.",
    ),
    "SRC4407_02_4375_profile_theorem": (
        FORMAL_391,
        "rho_eff(y)=rho_H(y) => E_profile=0",
        "4375 proves the conditional Hilbert-density profile theorem.",
    ),
    "SRC4407_03_4375_bound_gate": (
        FORMAL_391,
        "E_profile <= delta_N/K_N(s)",
        "4375 derives the finite E_profile score gate.",
    ),
    "SRC4407_04_4376_shadow": (
        FORMAL_392,
        "same-action Hilbert derivative + typed no-source-shadow grammar",
        "4376 assembles the source-shadow zero route and leaves it unsigned.",
    ),
    "SRC4407_05_4376_sigma": (
        FORMAL_392,
        "sigma_shadow_perp :=",
        "4376 defines the source-shadow profile row to fill if zero proof fails.",
    ),
    "SRC4407_06_4377_source_grammar": (
        FORMAL_393,
        "PG4377_1_no_source_shadow_type_error",
        "4377 makes the no-source-shadow theorem exact but conditional.",
    ),
    "SRC4407_07_4377_distribution": (
        FORMAL_393,
        "TPE4377_2_distributional_equality",
        "4377 converts topological equality into an all-test-function distributional gate.",
    ),
    "SRC4407_08_4377_envelope": (
        FORMAL_393,
        "E_profile <= E_shadow + E_top_profile + E_nonHilbert_profile + E_readout_profile",
        "4377 splits E_profile into no-cancellation components.",
    ),
    "SRC4407_09_4386_double_divergence": (
        FORMAL_402,
        "DD4386_4_parent_owner_contract",
        "4386 gives the exact double-divergence owner contract for affine profile silence.",
    ),
    "SRC4407_10_4387_birth_certificate": (
        FORMAL_403,
        "BCERT4387_0_residual_identity",
        "4387 shows the topological/Hilbert residual birth certificate is still missing.",
    ),
    "SRC4407_11_gate": (
        GATE_PATH,
        "def evaluate_eprofile_bound_rows",
        "Executable 4407 profile-zero and E_profile bound gate.",
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
    keys = list(rows[0].keys())
    lines = ["| " + " | ".join(keys) + " |", "| " + " | ".join("---" for _ in keys) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(md_cell(row.get(key, "")) for key in keys) + " |")
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
            "derivation_id": "EP4407_0_profile_owner_theorem",
            "object": "density-profile zero",
            "statement": "If the active local source density and the Hilbert/Hamiltonian source density are the same T_H(n,n)/c^2 functional on the same worldtube before readout, then rho_eff(y)=rho_H(y) pointwise and E_profile=0.",
            "result": "This is the right derivation target; total mass equality is only the monopole and is not enough.",
            "status": "EXACT_CONDITIONAL_THEOREM_IMPORTED",
            "valid_for_claim": False,
        },
        {
            "derivation_id": "EP4407_1_no_source_shadow_grammar",
            "object": "E_shadow",
            "statement": "A parent-adopted ordinary-source grammar with only Hilbert source density and no SourceOnly->Dens(W_H), non-Hilbert current, hidden Hom, or post-readout profile selector makes rho_shadow ill-typed.",
            "result": "The source-shadow component can go to zero only on a parent-signed grammar branch.",
            "status": "CONDITIONAL_ZERO_PARENT_SIGNATURE_MISSING",
            "valid_for_claim": False,
        },
        {
            "derivation_id": "EP4407_2_distributional_topological_gate",
            "object": "E_top_profile",
            "statement": "Topological/profile equality requires int_W f(rho_top-rho_H)dV_H=0 for every compact test function f, or an equivalent complete moment/profile hierarchy.",
            "result": "Same charge, same total mass, or same topological class does not prove profile equality.",
            "status": "TEST_FUNCTION_GATE_IMPORTED_NOT_CLOSED",
            "valid_for_claim": False,
        },
        {
            "derivation_id": "EP4407_3_no_cancellation_bound",
            "object": "finite E_profile",
            "statement": "E_profile <= E_shadow + E_top_profile + E_nonHilbert_profile + E_readout_profile and |delta a_profile|/|a_N| <= K_N(s)E_profile.",
            "result": "If the zero proof fails, the next row must source or bound those components rather than hiding them in E_mass.",
            "status": "EXECUTABLE_BOUND_GATE_BUILT",
            "valid_for_claim": False,
        },
        {
            "derivation_id": "EP4407_4_affine_route_scope",
            "object": "topological affine/double-divergence branch",
            "statement": "A parent-owned double divergence partial_i partial_j S^{ij} with affine-silent boundary pairings can kill monopole and first moment, but it is not full profile equality unless higher moments/profile norm are also controlled.",
            "result": "The double-divergence route is useful but must be birth-certified or replaced by real profile rows.",
            "status": "AFFINE_HELPFUL_NOT_FULL_EPROFILE_ZERO",
            "valid_for_claim": False,
        },
    ]


def profile_zero_input_rows() -> List[Dict[str, object]]:
    base = {
        "same_action_hilbert_derivative": False,
        "no_source_only_functional": False,
        "no_nonhilbert_current": False,
        "no_hidden_source_label_hom": False,
        "variation_before_readout": False,
        "same_worldtube": False,
        "topological_distributional_equality": False,
        "rest_bulk_metric_nullity": False,
        "boundary_projection_silent": False,
        "readout_profile_silent": False,
        "parent_signed": False,
        "public_authority": False,
        "input_valid_for_claim": False,
    }
    current = dict(base)
    current.update(
        {
            "profile_zero_id": "PZ4407_0_current_parent_grammar_open",
            "branch": "current_same_action_profile_owner_open",
            "source_path": str(FORMAL_393),
            "same_action_hilbert_derivative": True,
            "no_hidden_source_label_hom": True,
            "variation_before_readout": True,
            "same_worldtube": True,
        }
    )
    future = dict(base)
    future.update(
        {
            "profile_zero_id": "PZ4407_1_future_full_profile_zero_smoke",
            "branch": "future_all_clauses_signed_smoke",
            "source_path": str(FORMAL_393),
            "same_action_hilbert_derivative": True,
            "no_source_only_functional": True,
            "no_nonhilbert_current": True,
            "no_hidden_source_label_hom": True,
            "variation_before_readout": True,
            "same_worldtube": True,
            "topological_distributional_equality": True,
            "rest_bulk_metric_nullity": True,
            "boundary_projection_silent": True,
            "readout_profile_silent": True,
        }
    )
    affine_partial = dict(base)
    affine_partial.update(
        {
            "profile_zero_id": "PZ4407_2_affine_double_divergence_partial",
            "branch": "affine_double_divergence_partial_profile_silence",
            "source_path": str(FORMAL_402),
            "same_action_hilbert_derivative": True,
            "no_source_only_functional": True,
            "no_nonhilbert_current": True,
            "no_hidden_source_label_hom": True,
            "variation_before_readout": True,
            "same_worldtube": True,
            "boundary_projection_silent": False,
        }
    )
    return [current, future, affine_partial]


def eprofile_bound_input_rows() -> List[Dict[str, object]]:
    return [
        {
            "bound_id": "EP4407_0_missing_live_profile_components",
            "arena": "Newton_source_profile",
            "branch": "real_live_row_required",
            "source_path": str(FORMAL_392),
            "K_N": "0.00943177578696",
            "delta_N": "MISSING_DELTA_N",
            "E_shadow": "MISSING_E_SHADOW",
            "E_top_profile": "MISSING_E_TOP_PROFILE",
            "E_nonHilbert_profile": "MISSING_E_NONHILBERT_PROFILE",
            "E_readout_profile": "MISSING_E_READOUT_PROFILE",
            "input_valid_for_claim": False,
        },
        {
            "bound_id": "EP4407_1_zero_profile_smoke",
            "arena": "Newton_source_profile",
            "branch": "zero_profile_schema_smoke",
            "source_path": str(GATE_PATH),
            "K_N": "0.00943177578696",
            "delta_N": "1e-5",
            "E_shadow": "0",
            "E_top_profile": "0",
            "E_nonHilbert_profile": "0",
            "E_readout_profile": "0",
            "input_valid_for_claim": False,
        },
        {
            "bound_id": "EP4407_2_small_profile_pass_smoke",
            "arena": "Newton_source_profile",
            "branch": "small_profile_component_smoke",
            "source_path": str(GATE_PATH),
            "K_N": "0.00943177578696",
            "delta_N": "1e-5",
            "E_shadow": "1e-7",
            "E_top_profile": "1e-7",
            "E_nonHilbert_profile": "1e-7",
            "E_readout_profile": "1e-7",
            "input_valid_for_claim": False,
        },
        {
            "bound_id": "EP4407_3_profile_shadow_fail_control",
            "arena": "Newton_source_profile",
            "branch": "source_shadow_failure_control",
            "source_path": str(GATE_PATH),
            "K_N": "0.00943177578696",
            "delta_N": "1e-5",
            "E_shadow": "0.002",
            "E_top_profile": "0",
            "E_nonHilbert_profile": "0",
            "E_readout_profile": "0",
            "input_valid_for_claim": False,
        },
    ]


def claim_gate_rows() -> List[Dict[str, object]]:
    return [
        {
            "gate_id": "G4407_0_density_profile_zero",
            "gate": "rho_eff_equals_rho_H",
            "claim_allowed": False,
            "reason": "source-shadow grammar, topological distributional equality, rest/boundary/readout profile silence are not parent-signed together.",
        },
        {
            "gate_id": "G4407_1_Eprofile_bound",
            "gate": "finite_Eprofile_source_shadow_score",
            "claim_allowed": False,
            "reason": "real same-worldtube source-density rows or theorem-zero certificates are missing.",
        },
        {
            "gate_id": "G4407_2_affine_double_divergence",
            "gate": "topological_affine_silence",
            "claim_allowed": False,
            "reason": "double-divergence owner and boundary pairings are useful but not yet birth-certified or full-profile complete.",
        },
        {
            "gate_id": "G4407_3_local_GR_Newton",
            "gate": "local_GR_Newton_PPN_R10",
            "claim_allowed": False,
            "reason": "E_profile is only one retained E_mass component and still nonclaim.",
        },
    ]


def decision_rows() -> List[Dict[str, object]]:
    return [
        {
            "decision_id": "DEC4407_0",
            "decision": DECISION,
            "summary": "4407 turns the E_profile obstruction into an executable fork. The clean proof requires one same-worldtube Hilbert source density, no source-only functional/current/hidden-Hom slot, variation before readout, topological distributional equality, rest metric-nullity, boundary projection silence, and readout profile silence. Current evidence closes only the conditional grammar pieces, not the full parent-signed zero. The finite branch is now scoreable as K_N(s)(E_shadow+E_top_profile+E_nonHilbert_profile+E_readout_profile)<=delta_N. The next target is the least-circular remaining route: birth-certify the affine/double-divergence topological owner or fill the first real density-profile row.",
            "claim_allowed": False,
            "valid_for_claim": False,
        }
    ]


def status_rows() -> List[Dict[str, object]]:
    return [
        {
            "status_id": "STAT4407_0",
            "item": "profile owner theorem",
            "status": "EXACT_CONDITIONAL_IMPORTED",
            "notes": "same Hilbert T00 density on the same worldtube gives rho_eff=rho_H and E_profile=0.",
        },
        {
            "status_id": "STAT4407_1",
            "item": "source-shadow zero",
            "status": "PRIVATE_CONDITIONAL_NOT_PARENT_SIGNED",
            "notes": "no-source-shadow grammar is sharp but still conditional.",
        },
        {
            "status_id": "STAT4407_2",
            "item": "finite E_profile bound",
            "status": "RUNNER_READY",
            "notes": "E_shadow/E_top/E_nonHilbert/E_readout components now score through K_N(s).",
        },
        {
            "status_id": "STAT4407_3",
            "item": "next target",
            "status": "AFFINE_OWNER_OR_REAL_PROFILE_ROW",
            "notes": NEXT_TARGET,
        },
    ]


def next_target_rows() -> List[Dict[str, object]]:
    return [
        {
            "next_id": "NT4407_0",
            "target": NEXT_TARGET,
            "question": "Can rho_top-rho_H be parent-owned as a double-divergence/affine-annihilator with silent boundary pairings, or must a real density-profile row be imported?",
            "preferred_route": "derive the birth certificate that the parent action identifies rho_top-rho_H with partial_i partial_j S^{ij} before readout and proves affine boundary silence.",
            "fallback_route": "fill a real same-worldtube rho_H/rho_eff or sigma_shadow_perp/E_top_profile row and score it through the Eprofile gate.",
            "avoid": "claiming full E_profile=0 from same total mass, generic superpotential language, synthetic smoke rows, or affine first-moment silence alone.",
            "valid_for_claim": False,
        }
    ]


def write_formal_doc(
    sources: List[Dict[str, object]],
    derivations: List[Dict[str, object]],
    profile_zero_output: List[Dict[str, object]],
    eprofile_bound_output: List[Dict[str, object]],
    gates: List[Dict[str, object]],
    decisions: List[Dict[str, object]],
    next_targets: List[Dict[str, object]],
) -> None:
    FORMAL_PATH.write_text(
        f"""# 423 PPC4161 transition density profile owner or Eprofile source-shadow gate

Marker: `{MARKER}`

Generated UTC: `{STAMP}`

Decision: `{DECISION}`

## Claim Status

Private nonclaim. This checkpoint does not prove public local GR, Newtonian mechanics, Maxwell/EM closure, calibrated `G_N`, R10, PPN, clock, orbital, WEP, or full local-vacuum safety.

## Result

4407 makes the current gap executable instead of leaving it as prose.

The clean zero branch is:

```text
rho_eff(y) = rho_H(y) on W_H
=> E_profile = 0
```

but this fires only if the same branch supplies:

```text
same-action Hilbert derivative,
no source-only functional,
no non-Hilbert current,
no hidden/source-label Hom,
variation before readout,
same worldtube,
topological distributional equality,
rest bulk metric-nullity,
boundary projection silence,
readout profile silence.
```

The finite branch is:

```text
E_profile <= E_shadow + E_top_profile + E_nonHilbert_profile + E_readout_profile,
|delta a_profile|/|a_N| <= K_N(s) E_profile,
K_N(s)(E_shadow+E_top_profile+E_nonHilbert_profile+E_readout_profile) <= delta_N.
```

So the project did move: the problem is no longer "maybe coupling"; it is now a named source-density profile owner gate with a bounded fallback.

## Source Register

{markdown_table(sources)}

## Derivation Rows

{markdown_table(derivations)}

## Profile-Zero Gate Output

{markdown_table(profile_zero_output)}

## Eprofile Bound Gate Output

{markdown_table(eprofile_bound_output)}

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
        f"""# 4407 transition density-profile owner or Eprofile source-shadow gate

Marker: `{MARKER}`

## Private outcome

4407 converts the live source-density gap into a real gate.

The route is now:

```text
prove rho_eff(y)=rho_H(y) on W_H,
or bound E_profile = E_shadow + E_top_profile + E_nonHilbert_profile + E_readout_profile.
```

The current branch remains nonclaim because the parent-signed source-shadow/topological/rest/boundary/readout profile-zero clauses are not all closed.

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
        f"""## 4407 local spine update: Eprofile source-shadow gate

Marker: `{MARKER}`

Spine update: the source-coupling route has narrowed to density-profile ownership. The clean target is `rho_eff(y)=rho_H(y)` on the same worldtube before readout. The finite target is now executable as `K_N(s)(E_shadow+E_top_profile+E_nonHilbert_profile+E_readout_profile)<=delta_N`. The current route is promising because it is sharply localized, but it remains nonclaim until source-shadow grammar, topological distributional equality, rest/boundary/readout profile silence, or real profile rows are supplied.
""",
    )


def update_packet() -> None:
    append_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""## 4407 packet update: Eprofile source-density gate

Marker: `{PACKET_MARKER}`

Packet update: 4407 replaces generic `E_mass` fog with an explicit density-profile gate. Clean branch: same Hilbert source density gives `E_profile=0`. Fallback branch: source or bound `E_shadow`, `E_top_profile`, `E_nonHilbert_profile`, and `E_readout_profile` through the `K_N(s)` score.
""",
    )


def update_claims() -> None:
    append_claim_once(
        CLAIMS_PATH,
        CLAIM_ID,
        [
            CLAIM_ID,
            "local_gr",
            "4407 turns the E_profile obstruction into an executable density-profile gate. The clean branch requires rho_eff(y)=rho_H(y) on the same worldtube from a parent-signed Hilbert source-density grammar plus topological distributional equality, rest metric-nullity, boundary projection silence, and readout profile silence. The finite branch now scores K_N(s)(E_shadow+E_top_profile+E_nonHilbert_profile+E_readout_profile)<=delta_N. Current evidence is conditional/private and no local-GR/Newton/PPN/R10/clock/orbital claim fires.",
            "4407 source register, derivation rows, profile-zero gate, Eprofile bound gate, claim gates, decision, status, next target and validation CSV.",
            "Eprofile_source_shadow_profile_zero_and_bound_gate_ready_nonclaim",
            "Birth-certify the affine/double-divergence topological owner or fill the first real same-worldtube density-profile row.",
            "Claiming E_profile=0 from total mass, generic superpotential language, synthetic smoke rows, or affine first-moment silence alone.",
        ],
    )


def validation_rows(csv_paths: List[Path]) -> List[Dict[str, object]]:
    sources = read_csv(SOURCE_DIR / "P8_Y5_R2FR_4407_SOURCE_REGISTER.csv")
    derivations = read_csv(SOURCE_DIR / "P8_Y5_R2FR_4407_DERIVATIONS.csv")
    profile_zero = read_csv(PROFILE_ZERO_OUTPUT)
    eprofile_bound = read_csv(EPROFILE_BOUND_OUTPUT)
    gates = read_csv(SOURCE_DIR / "P8_Y5_R2FR_4407_CLAIM_GATES.csv")
    rows: List[Dict[str, object]] = []

    def add(check_id: str, passed: bool, detail: str) -> None:
        rows.append({"checkpoint": CHECKPOINT, "check_id": check_id, "passed": passed, "detail": detail})

    add("VAL4407_0_sources_exist", all(row["path_exists"] == "True" for row in sources), "every cited source exists")
    add("VAL4407_1_needles_found", all(row["needle_found"] == "True" for row in sources), "every cited source needle resolves")
    add("VAL4407_2_derivations_written", len(derivations) >= 5, "derivation rows written")
    add("VAL4407_3_current_profile_zero_blocks", any(row["profile_zero_id"] == "PZ4407_0_current_parent_grammar_open" and row["current_status"] == "EPROFILE_ZERO_BLOCKED" for row in profile_zero), "current profile-zero row blocks")
    add("VAL4407_4_future_profile_zero_nonclaim", any(row["profile_zero_id"] == "PZ4407_1_future_full_profile_zero_smoke" and row["private_profile_zero"] == "True" and row["claim_allowed"] == "False" for row in profile_zero), "future full zero branch computes but remains nonclaim")
    add("VAL4407_5_missing_bound_blocks", any(row["bound_id"] == "EP4407_0_missing_live_profile_components" and row["current_status"] == "EPROFILE_BOUND_BLOCKED" for row in eprofile_bound), "missing live Eprofile row blocks")
    add("VAL4407_6_zero_bound_passes_nonclaim", any(row["bound_id"] == "EP4407_1_zero_profile_smoke" and row["within_bound"] == "True" and row["claim_allowed"] == "False" for row in eprofile_bound), "zero Eprofile smoke passes but remains nonclaim")
    add("VAL4407_7_failure_control_detected", any(row["bound_id"] == "EP4407_3_profile_shadow_fail_control" and row["current_status"] == "EPROFILE_BOUND_FAILS" for row in eprofile_bound), "profile-shadow failure control detected")
    add("VAL4407_8_claim_gates_false", all(row["claim_allowed"] == "False" for row in gates), "claim gates false")
    add("VAL4407_9_formal_marker", MARKER in text(FORMAL_PATH), "formal marker present")
    add("VAL4407_10_post_marker", MARKER in text(DOC_PATH), "post marker present")
    add("VAL4407_11_spine_marker", MARKER in text(SPINE_PATH), "spine marker present")
    add("VAL4407_12_packet_marker", PACKET_MARKER in text(PACKET_PATH), "packet marker present")
    add("VAL4407_13_claim_row", f"\n{CLAIM_ID}," in text(CLAIMS_PATH), "claim row present")
    add("VAL4407_14_csv_parse", all(len(read_csv(path)) > 0 for path in csv_paths), "all generated CSVs parse")
    add("VAL4407_15_generated_nonclaim", all(row.get("valid_for_claim", "False") == "False" for path in csv_paths for row in read_csv(path)), "generated rows stay nonclaim")
    add("VAL4407_16_gate_exists", GATE_PATH.exists() and "def evaluate_eprofile_bound_rows" in text(GATE_PATH), "Eprofile gate script exists")
    add("VAL4407_17_pycache_absent", not (SCRIPT_DIR / "__pycache__").exists(), "scripts __pycache__ absent")
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
        "P8_Y5_R2FR_4407_SOURCE_REGISTER.csv": sources,
        "P8_Y5_R2FR_4407_DERIVATIONS.csv": derivations,
        "P8_Y5_R2FR_4407_CLAIM_GATES.csv": gates,
        "P8_Y5_R2FR_4407_DECISION.csv": decisions,
        "P8_Y5_R2FR_4407_STATUS.csv": statuses,
        "P8_Y5_R2FR_4407_NEXT_TARGET.csv": next_targets,
    }
    for filename, rows in csv_payloads.items():
        path = SOURCE_DIR / filename
        write_csv(path, rows)
        csv_paths.append(path)

    write_csv(PROFILE_ZERO_INPUT, profile_zero_input_rows())
    profile_zero_output = evaluate_profile_zero_rows(PROFILE_ZERO_INPUT)
    write_csv(PROFILE_ZERO_OUTPUT, profile_zero_output)
    csv_paths.extend([PROFILE_ZERO_INPUT, PROFILE_ZERO_OUTPUT])

    write_csv(EPROFILE_BOUND_INPUT, eprofile_bound_input_rows())
    eprofile_bound_output = evaluate_eprofile_bound_rows(EPROFILE_BOUND_INPUT)
    write_csv(EPROFILE_BOUND_OUTPUT, eprofile_bound_output)
    csv_paths.extend([EPROFILE_BOUND_INPUT, EPROFILE_BOUND_OUTPUT])

    write_formal_doc(sources, derivations, profile_zero_output, eprofile_bound_output, gates, decisions, next_targets)
    write_post_doc(decisions, next_targets)
    update_spine()
    update_packet()
    update_claims()
    remove_pycache()
    write_csv(VALIDATION_PATH, validation_rows(csv_paths))


if __name__ == "__main__":
    main()
