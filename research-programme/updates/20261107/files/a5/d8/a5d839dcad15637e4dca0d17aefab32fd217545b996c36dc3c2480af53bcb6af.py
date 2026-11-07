from common import ROOT, modest, require, read, digest
import replay_full_tangent
import probe_analysis


if __name__ == "__main__":
    modest()
    original = read(ROOT / "continuous-replay-result.json")
    require(not original["passed"] and digest(ROOT / "replay_full_tangent.py") == original["source_sha256"], "changed frozen checker")
    require(read(ROOT / "phase-resolved/tangent-check-result.json")["passed"], "phase response not accepted")
    replay_full_tangent.ROOT = probe_analysis.ROOT = ROOT / "phase-resolved"
    replay_full_tangent.main()
