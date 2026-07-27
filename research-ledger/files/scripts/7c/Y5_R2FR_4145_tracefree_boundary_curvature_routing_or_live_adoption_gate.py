from __future__ import annotations

import csv
import py_compile
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Tuple


ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
SOURCE_DIR = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = PROJECT / "formalization-workbench"
SCRIPT_PATH = Path(__file__).resolve()
DOC_PATH = ROOT / "4145-Y5-R2FR-tracefree-boundary-curvature-routing-or-live-adoption-gate.md"

TIMESTAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
BRANCH_ID = "MTS_R2FR_Y5_TRACEFREE_BOUNDARY_CURVATURE_LIVE_ADOPTION_GATE_4145"
CHECKPOINT_ID = "4145"
DECISION = "BOUNDARY_CLOSED_CONSTRUCTED_BRANCH_CURVATURE_SPLIT_LIVE_ADOPTION_UNSIGNED_MATTER_ROUTING_REQUIRED"


LOCAL_SOURCES: Dict[str, Tuple[Path, str, str]] = {
    "SRC4145_00_4144_doc": (
        ROOT / "4144-Y5-R2FR-tracefree-coefficient-adoption-birth-certificate-or-epsilon-bound.md",
        "boundary, curvature routing, phi owner and live Khat adoption remain open",
        "4144 left the trace-free branch with boundary, curvature and adoption blockers.",
    ),
    "SRC4145_01_4144_birth_certificate": (
        SOURCE_DIR / "P8_Y5_R2FR_4144_BIRTH_CERTIFICATE.csv",
        "BC4144_3_boundary",
        "4144 certificate row naming the boundary blocker.",
    ),
    "SRC4145_02_4144_minimal_clause": (
        SOURCE_DIR / "P8_Y5_R2FR_4144_MINIMAL_PARENT_CLAUSE.csv",
        "sigma_resp^{-1} phi R",
        "4144 minimal parent clause that 4145 tries to make well-posed.",
    ),
    "SRC4145_03_4144_status": (
        SOURCE_DIR / "P8_Y5_R2FR_4144_STATUS.csv",
        "current_birth_certificate_passed",
        "4144 nonclaim status.",
    ),
    "SRC4145_04_4028_derivation": (
        SOURCE_DIR / "P8_Y5_R2FR_4028_TRACEFREE_IMPROVEMENT_DERIVATION.csv",
        "D_TF^{mn}=(1-sigma_resp*c_I)K_L^{mn}",
        "4028 residual law and trace-free phi R variation.",
    ),
    "SRC4145_05_4028_gate": (
        SOURCE_DIR / "P8_Y5_R2FR_4028_TRACEFREE_SIGN_AND_PROJECTION_GATE.csv",
        "B_imp and local collar are no-flux/silent",
        "4028 sign/projection gate that includes boundary and live Khat adoption.",
    ),
    "SRC4145_06_4138_audit": (
        SOURCE_DIR / "P8_Y5_R2FR_4138_TRACEFREE_SIGNING_AUDIT.csv",
        "boundary silence is not mapped to PPN/R10/source units",
        "4138 audit showing why boundary and adoption cannot be waved away.",
    ),
    "SRC4145_07_4138_bound": (
        SOURCE_DIR / "P8_Y5_R2FR_4138_DA_GRAD_BETA_BOUND_ROWS.csv",
        "A_boundary/L_boundary",
        "4138 bound row with the trace-free residual decomposition.",
    ),
    "SRC4145_08_4144_epsilon": (
        SOURCE_DIR / "P8_Y5_R2FR_4144_EPSILON_BOUND_ROWS.csv",
        "epsilon_TF=1-sigma_resp*c_I",
        "4144 epsilon bound rows after coefficient clause construction.",
    ),
    "SRC4145_09_script": (
        SCRIPT_PATH,
        "BOUNDARY_CLOSED_CONSTRUCTED_BRANCH_CURVATURE_SPLIT",
        "This generator records the 4145 proof split.",
    ),
}


def common() -> dict:
    return {
        "timestamp_utc": TIMESTAMP,
        "branch_id": BRANCH_ID,
        "checkpoint_id": CHECKPOINT_ID,
    }


def write_csv(path: Path, rows: List[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: List[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def parse_csv(path: Path) -> List[dict]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def is_under(path: Path, root: Path) -> bool:
    try:
        path.resolve().relative_to(root.resolve())
        return True
    except ValueError:
        return False


def output_paths() -> Dict[str, Path]:
    return {
        "P8_Y5_R2FR_4145_SOURCE_REGISTER": SOURCE_DIR / "P8_Y5_R2FR_4145_SOURCE_REGISTER.csv",
        "P8_Y5_R2FR_4145_BOUNDARY_CLOSURE": SOURCE_DIR / "P8_Y5_R2FR_4145_BOUNDARY_CLOSURE.csv",
        "P8_Y5_R2FR_4145_CURVATURE_ROUTING": SOURCE_DIR / "P8_Y5_R2FR_4145_CURVATURE_ROUTING.csv",
        "P8_Y5_R2FR_4145_LIVE_ADOPTION_GATE": SOURCE_DIR / "P8_Y5_R2FR_4145_LIVE_ADOPTION_GATE.csv",
        "P8_Y5_R2FR_4145_RESIDUAL_UPDATE": SOURCE_DIR / "P8_Y5_R2FR_4145_RESIDUAL_UPDATE.csv",
        "P8_Y5_R2FR_4145_DECISION_GATES": SOURCE_DIR / "P8_Y5_R2FR_4145_DECISION_GATES.csv",
        "P8_Y5_R2FR_4145_STATUS": SOURCE_DIR / "P8_Y5_R2FR_4145_STATUS.csv",
        "P8_Y5_R2FR_4145_NEXT_TARGET": SOURCE_DIR / "P8_Y5_R2FR_4145_NEXT_TARGET.csv",
    }


def source_rows() -> List[dict]:
    rows: List[dict] = []
    for source_id, (path, needle, role) in LOCAL_SOURCES.items():
        exists = path.exists()
        text = read_text(path) if exists and path.is_file() else ""
        rows.append(
            {
                **common(),
                "source_id": source_id,
                "path": str(path),
                "needle": needle,
                "role": role,
                "exists": str(exists),
                "needle_found": str(bool(exists and needle in text)),
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
    return rows


def boundary_rows() -> List[dict]:
    return [
        {
            **common(),
            "closure_id": "BC4145_0_scalar_tensor_boundary_action",
            "item": "well-posed trace-free parent action",
            "formula": "S_TF^Omega=c_I[int_Omega sqrt|g| phi R + 2 int_partialOmega sqrt|h| phi K + 2 sum_corners int sqrt|sigma| phi eta]",
            "derivation": "The scalar-tensor GHY plus corner term cancels normal-derivative metric variations from delta R.",
            "condition": "fixed induced metric h_ab and fixed/silent phi on the local readout boundary; no unaccounted corners",
            "result": "BOUNDARY_CLOSED_IN_CONSTRUCTED_PARENT_BRANCH",
            "live_corpus_status": "CONSTRUCTED_NOT_LIVE_ADOPTED",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "closure_id": "BC4145_1_bulk_variation",
            "item": "bulk metric response",
            "formula": "delta_g S_TF^Omega=c_I int_Omega sqrt|g|[phi G_mn+(g_mn Box-nabla_m nabla_n)phi]delta g^{mn}",
            "derivation": "With the boundary term and fixed boundary data, the metric response is purely bulk.",
            "condition": "metric response taken at fixed phi; phi Euler equation handled by the owner action",
            "result": "BULK_RESPONSE_DERIVED_NO_BOUNDARY_LEAK",
            "live_corpus_status": "CONSTRUCTED_NOT_LIVE_ADOPTED",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "closure_id": "BC4145_2_ppn_collar_silence",
            "item": "local PPN collar",
            "formula": "D_boundary=0 when variations are compactly supported in Omega or the collar fixes (h_ab,phi) and includes the phi K/corner terms",
            "derivation": "The previous boundary blocker is not an independent residual inside this constructed branch.",
            "condition": "the PPN/R10 readout must use the same boundary convention rather than switching variational data",
            "result": "BOUNDARY_ZERO_CONDITIONAL_ON_PARENT_BRANCH_AND_COLLAR",
            "live_corpus_status": "SOURCE_CONVENTION_STILL_NEEDS_ADOPTION_ROW",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def curvature_rows() -> List[dict]:
    return [
        {
            **common(),
            "route_id": "CR4145_0_exact_curvature_channel",
            "item": "trace-free curvature term",
            "formula": "Pi_TF(phi G_mn)=phi G_TF_mn",
            "derivation": "The phi R parent variation always produces a curvature channel alongside the Hessian trace-free channel.",
            "route_result": "EXACT_SPLIT_DERIVED",
            "blocker": "must be vacuum-zero, matter-routed, or bounded; it cannot be silently deleted",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "route_id": "CR4145_1_vacuum_annulus",
            "item": "exterior local-vacuum route",
            "formula": "if G_mn=0 on the readout annulus then phi G_TF_mn=0 and D_phiG=0 there",
            "derivation": "The curvature blocker closes on a true vacuum collar, so exterior PPN propagation is not the dangerous part.",
            "route_result": "CLOSED_ONLY_ON_VACUUM_READOUT_SUPPORT",
            "blocker": "finite-source and body-interior overlaps still need source coupling or a support theorem",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "route_id": "CR4145_2_matter_channel",
            "item": "finite-source matter routing",
            "formula": "using a GR-like local equation gives 2 phi G_TF_mn=16 pi G phi T_TF_mn",
            "derivation": "Inside matter this is a source-coupling term, not a small automatic correction; dust still has a nonzero four-dimensional trace-free part.",
            "route_result": "MATTER_ROUTING_REQUIRED_NOT_OPTIONAL",
            "blocker": "need parent-owned matter coupling and source-normalization row before PPN or Newton-limit claim",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "route_id": "CR4145_3_bound_form",
            "item": "nonclaim curvature bound",
            "formula": "|delta_beta_phiG| <= |C_beta_qloc| C_Ploc A_phiG/L_phiG with A_phiG/L_phiG sourced from int |phi G_TF| on the same support",
            "derivation": "If matter routing is not adopted, the curvature channel becomes an explicit bound row rather than a theorem zero.",
            "route_result": "BOUND_ROW_REQUIRED_IF_SUPPORT_NOT_VACUUM",
            "blocker": "missing support function, phi profile, G_TF/T_TF normalization and beta projector",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def adoption_rows() -> List[dict]:
    return [
        {
            **common(),
            "gate_id": "LA4145_0_constructed_branch_adoption",
            "gate": "define live trace-free response from parent action",
            "required_row": "Khat_current^TF := Pi_TF[-2/sqrt|g| delta S_TF^Omega/delta g]",
            "current_evidence": "4144 constructs this as a future parent clause; current corpus has no live adoption row.",
            "gate_result": "FAIL_CURRENT_CORPUS_PASS_CONSTRUCTED_BRANCH",
            "residual_if_failed": "D_adoption",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "gate_id": "LA4145_1_no_retuning",
            "gate": "single coefficient and boundary convention",
            "required_row": "same sigma_resp, c_I, phi K boundary convention, and Khat definition across R10, PPN, clocks, orbital and cosmology",
            "current_evidence": "4144 added a no-retuning guard but adoption remains unsigned.",
            "gate_result": "FAIL_UNTIL_PARENT_SPINE_ADOPTS_ONE_CONVENTION",
            "residual_if_failed": "D_adoption + D_boundary + D_phiG",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "gate_id": "LA4145_2_phi_owner_dependency",
            "gate": "local phi owner adopted with stress accounting",
            "required_row": "phi Euler equation, zero-mode/boundary convention, and phi stress routed into matter/EH ledger",
            "current_evidence": "owner template exists but remains staged; 4145 boundary closure assumes phi boundary data are owned.",
            "gate_result": "RETAINED_BLOCKER",
            "residual_if_failed": "D_owner",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def residual_rows() -> List[dict]:
    return [
        {
            **common(),
            "residual_id": "RU4145_0_before_4145",
            "formula": "D_TF=(1-sigma_resp*c_I)K_L + 2 sigma_resp*c_I phi G_TF + D_owner + D_boundary + D_adoption",
            "meaning": "4028/4138 trace-free residual law before 4144/4145 closures.",
            "status": "SOURCE_LAW_RESTATED",
            "score_ready": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "residual_id": "RU4145_1_constructed_parent_after_boundary",
            "formula": "with sigma_resp*c_I=1 and scalar-tensor boundary closure: D_TF=2 phi G_TF + D_owner + D_adoption",
            "meaning": "4145 removes D_boundary and the coefficient mismatch only inside the constructed parent branch.",
            "status": "REAL_PROGRESS_NONCLAIM",
            "score_ready": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "residual_id": "RU4145_2_vacuum_collar",
            "formula": "on a vacuum readout annulus with live adoption and owned phi: D_TF=0",
            "meaning": "This is the cleanest local-GR route, but it only proves exterior/vacuum support unless finite-source matching is added.",
            "status": "CONDITIONAL_THEOREM_ROUTE",
            "score_ready": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "residual_id": "RU4145_3_finite_source",
            "formula": "inside source support: D_TF=16 pi G phi T_TF + D_owner + D_adoption unless matter routing cancels/absorbs it",
            "meaning": "Finite-source tests cannot be passed by boundary work alone; source coupling is the remaining hard problem.",
            "status": "MATTER_COUPLING_GATE_EXPOSED",
            "score_ready": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def decision_rows() -> List[dict]:
    return [
        {
            **common(),
            "decision_id": "DG4145_0_boundary",
            "decision": "BOUNDARY_CLOSED_CONSTRUCTED_BRANCH",
            "evidence": "scalar-tensor phi K/corner boundary term makes the metric variation bulk-only under fixed h_ab and phi boundary data",
            "claim_state": "constructed branch only; live corpus still needs adoption row",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "decision_id": "DG4145_1_curvature",
            "decision": "CURVATURE_SPLIT_NOT_GENERIC_ZERO",
            "evidence": "Pi_TF(phi G)=phi G_TF; zero on vacuum annulus, source-coupling term inside matter",
            "claim_state": "no generic local-GR or PPN pass",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "decision_id": "DG4145_2_live_adoption",
            "decision": "LIVE_KHAT_ADOPTION_UNSIGNED",
            "evidence": "constructed Khat response exists but current Khat_current^TF adoption row is absent",
            "claim_state": "D_adoption retained",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "decision_id": "DG4145_3_next",
            "decision": "NEXT_TARGET_SOURCE_SUPPORT_OR_MATTER_ROUTING",
            "evidence": "after boundary closure, the nontrivial obstruction is finite-source phi G_TF plus owner/adoption",
            "claim_state": "derive support theorem or parent-owned matter coupling; otherwise bound it",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def status_rows() -> List[dict]:
    return [
        {
            **common(),
            "status_id": "STATUS4145_0",
            "result": DECISION,
            "summary": "4145 closes the boundary blocker in the constructed parent branch by adding the scalar-tensor phi K/corner boundary term to the phi R action. It does not close the live current-corpus proof: Pi_TF(phi G)=phi G_TF is zero only on a genuine vacuum readout annulus, while finite-source overlap requires parent-owned matter routing or a bound, and Khat_current^TF adoption remains unsigned.",
            "boundary_closed_constructed_branch": "True",
            "curvature_zero_generic": "False",
            "curvature_zero_vacuum_annulus": "True",
            "finite_source_matter_routing_required": "True",
            "live_khat_adoption_signed": "False",
            "local_gr_claimed": "False",
            "score_ready": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def next_rows() -> List[dict]:
    return [
        {
            **common(),
            "next_id": "NEXT4145_0",
            "target_doc": "4146-Y5-R2FR-finite-source-support-theorem-or-matter-routing-coupling-gate.md",
            "target_script": "scripts/Y5_R2FR_4146_finite_source_support_theorem_or_matter_routing_coupling_gate.py",
            "objective": "try to prove the PPN/R10 readout support can be placed on a vacuum annulus, or derive the parent-owned matter-routing cancellation for 2 phi G_TF; if neither closes, emit finite-source A_phiG/T_TF bound rows",
            "success_gate": "either support theorem removes matter overlap, or matter coupling routes 16 pi G phi T_TF into the EH/source ledger without retuning, or explicit nonclaim bounds are emitted",
            "reason": "4145 closed boundary only in the constructed parent branch; the remaining hard obstruction is finite-source curvature/source coupling plus live adoption.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def write_doc(outputs: Dict[str, Path]) -> None:
    text = f"""# 4145 - Trace-free boundary, curvature routing and live adoption gate

## Decision
- Decision: `{DECISION}`.
- Real progress: the boundary blocker is closed inside the constructed parent branch.
- Still not claimed: local GR, Newtonian reduction, PPN beta, R10, WEP, clocks, orbital systems, or public evidence.

## Boundary closure
The well-posed parent action is

`S_TF^Omega=c_I[int_Omega sqrt|g| phi R + 2 int_partialOmega sqrt|h| phi K + 2 sum_corners int sqrt|sigma| phi eta]`.

With fixed induced metric `h_ab`, fixed/silent `phi` on the local readout boundary, and no unaccounted corner terms,

`delta_g S_TF^Omega=c_I int_Omega sqrt|g|[phi G_mn+(g_mn Box-nabla_m nabla_n)phi]delta g^mn`.

So `D_boundary=0` is derived for the constructed parent branch; it is no longer a free plateau axiom. The live corpus still needs one adoption row saying this is the boundary convention used by MTS.

## Curvature split
The same variation always gives

`Pi_TF(phi G_mn)=phi G_TF_mn`.

Therefore:
- On a genuine vacuum readout annulus, `G_mn=0`, so `D_phiG=0`.
- On finite-source support, `2 phi G_TF_mn=16 pi G phi T_TF_mn` under GR-like source routing.
- That source term is not automatically small; it needs parent-owned matter coupling or an explicit bound.

## Updated residual law
Before the 4145 closure:

`D_TF=(1-sigma_resp*c_I)K_L + 2 sigma_resp*c_I phi G_TF + D_owner + D_boundary + D_adoption`.

Inside the constructed parent branch with `sigma_resp*c_I=1` and the scalar-tensor boundary term:

`D_TF=2 phi G_TF + D_owner + D_adoption`.

In a vacuum collar, with owned `phi` and live `Khat` adoption, this would become `D_TF=0`. For finite-source tests it does not.

## Current gate table
| Gate | Result | Meaning |
|---|---|---|
| boundary | CLOSED_CONSTRUCTED_BRANCH | scalar-tensor `phi K`/corner term closes boundary variation |
| curvature | SPLIT_NOT_GENERIC_ZERO | zero in vacuum; source-coupling term inside matter |
| live Khat adoption | UNSIGNED | `Khat_current^TF` is not yet live-defined by this parent response |
| phi owner | RETAINED_BLOCKER | owner action and stress ledger still need adoption |

## Outputs
- `{outputs["P8_Y5_R2FR_4145_SOURCE_REGISTER"]}`
- `{outputs["P8_Y5_R2FR_4145_BOUNDARY_CLOSURE"]}`
- `{outputs["P8_Y5_R2FR_4145_CURVATURE_ROUTING"]}`
- `{outputs["P8_Y5_R2FR_4145_LIVE_ADOPTION_GATE"]}`
- `{outputs["P8_Y5_R2FR_4145_RESIDUAL_UPDATE"]}`
- `{outputs["P8_Y5_R2FR_4145_DECISION_GATES"]}`
- `{outputs["P8_Y5_R2FR_4145_STATUS"]}`
- `{outputs["P8_Y5_R2FR_4145_NEXT_TARGET"]}`

## Next Target
- `4146-Y5-R2FR-finite-source-support-theorem-or-matter-routing-coupling-gate.md`
- Try to prove the readout/projector support theorem first. If finite-source overlap cannot be removed, derive matter-routing coupling for `16 pi G phi T_TF`; if that fails, emit `A_phiG/T_TF` bound rows.
"""
    DOC_PATH.write_text(text, encoding="utf-8")


def write_outputs() -> Dict[str, Path]:
    outputs = output_paths()
    write_csv(outputs["P8_Y5_R2FR_4145_SOURCE_REGISTER"], source_rows())
    write_csv(outputs["P8_Y5_R2FR_4145_BOUNDARY_CLOSURE"], boundary_rows())
    write_csv(outputs["P8_Y5_R2FR_4145_CURVATURE_ROUTING"], curvature_rows())
    write_csv(outputs["P8_Y5_R2FR_4145_LIVE_ADOPTION_GATE"], adoption_rows())
    write_csv(outputs["P8_Y5_R2FR_4145_RESIDUAL_UPDATE"], residual_rows())
    write_csv(outputs["P8_Y5_R2FR_4145_DECISION_GATES"], decision_rows())
    write_csv(outputs["P8_Y5_R2FR_4145_STATUS"], status_rows())
    write_csv(outputs["P8_Y5_R2FR_4145_NEXT_TARGET"], next_rows())
    write_doc(outputs)
    return outputs


def validate(outputs: Dict[str, Path]) -> List[dict]:
    checks: List[dict] = []

    def add(check_id: str, requirement: str, passed: bool, detail: str) -> None:
        checks.append(
            {
                **common(),
                "check_id": check_id,
                "requirement": requirement,
                "passed": str(bool(passed)),
                "detail": detail,
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )

    source = source_rows()
    add(
        "VAL4145_0_sources",
        "all cited source paths exist and contain required needles",
        all(row["exists"] == "True" and row["needle_found"] == "True" for row in source),
        "; ".join(f"{row['source_id']} exists={row['exists']} needle={row['needle_found']}" for row in source),
    )

    csv_ok = True
    csv_detail: List[str] = []
    for name, path in outputs.items():
        try:
            rows = parse_csv(path)
            csv_detail.append(f"{name}:{len(rows)}")
            csv_ok = csv_ok and bool(rows)
        except Exception as exc:
            csv_ok = False
            csv_detail.append(f"{name}:ERR {exc!r}")
    add("VAL4145_1_csv_parse", "all generated CSV outputs parse and are nonempty", csv_ok, ", ".join(csv_detail))

    doc_text = read_text(DOC_PATH) if DOC_PATH.exists() else ""
    doc_tokens = [
        DECISION,
        "D_boundary=0",
        "Pi_TF(phi G_mn)=phi G_TF_mn",
        "16 pi G phi T_TF",
        "D_TF=2 phi G_TF + D_owner + D_adoption",
        "4146-Y5-R2FR-finite-source-support-theorem-or-matter-routing-coupling-gate.md",
    ]
    add("VAL4145_2_doc_tokens", "document records boundary closure, curvature split, residual update and next target", all(token in doc_text for token in doc_tokens), "tokens checked")

    boundary_text = "\n".join(",".join(row.values()) for row in parse_csv(outputs["P8_Y5_R2FR_4145_BOUNDARY_CLOSURE"]))
    boundary_tokens = ["phi K", "corner", "D_boundary=0", "BOUNDARY_CLOSED_IN_CONSTRUCTED_PARENT_BRANCH"]
    add("VAL4145_3_boundary", "boundary closure uses scalar-tensor boundary term and remains constructed-branch only", all(token in boundary_text for token in boundary_tokens), "boundary tokens checked")

    curvature_text = "\n".join(",".join(row.values()) for row in parse_csv(outputs["P8_Y5_R2FR_4145_CURVATURE_ROUTING"]))
    curvature_tokens = ["Pi_TF(phi G_mn)=phi G_TF_mn", "G_mn=0", "16 pi G phi T_TF", "MATTER_ROUTING_REQUIRED_NOT_OPTIONAL"]
    add("VAL4145_4_curvature", "curvature routing is split into vacuum zero and finite-source matter coupling", all(token in curvature_text for token in curvature_tokens), "curvature tokens checked")

    adoption_text = "\n".join(",".join(row.values()) for row in parse_csv(outputs["P8_Y5_R2FR_4145_LIVE_ADOPTION_GATE"]))
    adoption_ok = "Khat_current^TF" in adoption_text and "FAIL_CURRENT_CORPUS_PASS_CONSTRUCTED_BRANCH" in adoption_text and "D_adoption" in adoption_text
    add("VAL4145_5_adoption", "live Khat adoption remains unsigned while constructed branch is explicit", adoption_ok, "adoption tokens checked")

    status = parse_csv(outputs["P8_Y5_R2FR_4145_STATUS"])
    status_ok = (
        len(status) == 1
        and status[0].get("result") == DECISION
        and status[0].get("boundary_closed_constructed_branch") == "True"
        and status[0].get("curvature_zero_generic") == "False"
        and status[0].get("finite_source_matter_routing_required") == "True"
        and status[0].get("live_khat_adoption_signed") == "False"
        and status[0].get("local_gr_claimed") == "False"
    )
    add("VAL4145_6_status", "status records boundary progress but no local-GR/current-corpus claim", status_ok, str(status))

    next_target = parse_csv(outputs["P8_Y5_R2FR_4145_NEXT_TARGET"])
    next_ok = len(next_target) == 1 and next_target[0].get("target_doc") == "4146-Y5-R2FR-finite-source-support-theorem-or-matter-routing-coupling-gate.md"
    add("VAL4145_7_next", "next target attacks finite-source support theorem or matter routing", next_ok, str(next_target))

    all_rows: List[dict] = []
    for path in outputs.values():
        all_rows.extend(parse_csv(path))
    no_claim = all(row.get("claim_allowed") in ("False", "") and row.get("valid_for_claim") in ("False", "") for row in all_rows)
    no_score = all(row.get("score_ready", "False") in ("False", "") for row in all_rows)
    add("VAL4145_8_no_claim", "all outputs remain nonclaim and not score-ready", no_claim and no_score, f"row_count={len(all_rows)}")

    output_paths_all = list(outputs.values()) + [DOC_PATH]
    in_scope = all(is_under(path, ROOT) for path in output_paths_all)
    formalization_output = any(is_under(path, FORMALIZATION) for path in output_paths_all)
    formalization_touched = False
    if FORMALIZATION.exists():
        formalization_touched = any(
            ("4145-Y5-R2FR" in item.name or "R2FR_4145" in item.name)
            for item in FORMALIZATION.rglob("*")
        )
    add("VAL4145_9_scope", "outputs stay in post-checkpoint-work and not formalization-workbench", in_scope and not formalization_output and not formalization_touched, f"doc={DOC_PATH}; csv_count={len(outputs)}")

    compile_ok = True
    compile_detail = "py_compile ok"
    try:
        py_compile.compile(str(SCRIPT_PATH), doraise=True)
    except Exception as exc:
        compile_ok = False
        compile_detail = repr(exc)
    add("VAL4145_10_compile", "generator script compiles", compile_ok, compile_detail)
    return checks


def main() -> None:
    outputs = write_outputs()
    validation_rows = validate(outputs)
    validation_path = SOURCE_DIR / "P8_Y5_BRR545_4145_VALIDATION.csv"
    write_csv(validation_path, validation_rows)
    pycache = SCRIPT_PATH.parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)

    failed = [row for row in validation_rows if row["passed"] != "True"]
    print(f"wrote: {DOC_PATH}")
    for path in outputs.values():
        print(f"wrote: {path}")
    print(f"validation: {validation_path}")
    if failed:
        print("failed checks:")
        for row in failed:
            print(f"- {row['check_id']}: {row['detail']}")
        raise SystemExit(1)
    print("all validation checks passed")


if __name__ == "__main__":
    main()
