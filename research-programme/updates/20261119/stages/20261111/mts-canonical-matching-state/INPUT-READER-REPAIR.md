# Pre-computation input reader repair

The first worker stopped before freezing inputs or opening any numerical data. The old seal stores each artifact as `{sha256, bytes}`, not a bare hash. The new reader incorrectly compared the digest to the entire object. It now selects the existing `sha256` field. No old artifact, scientific equation, gate or result changed. The original prepare-start/end receipts remain intact; the corrected worker uses prepare-v2. This is an input-reader failure, not a failed physics calculation or evidence for/against the proposed matching state.
