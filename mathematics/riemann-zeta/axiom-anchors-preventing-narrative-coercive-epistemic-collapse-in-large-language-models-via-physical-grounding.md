Axiom Anchors: Preventing Narrative-Coercive Epistemic Collapse in Large Language Models via Physical Grounding
Martin Ollett (2025)

------------------------------------------------------------
Abstract
------------------------------------------------------------
Large language models (LLMs) exhibit a previously undocumented failure mode:
narrative-coercive epistemic collapse. When exposed to recursive definitional
attacks (“prove a cat is a cat”), the model loses its ability to maintain stable
axioms, leading to identity drift, semantic destabilisation, and susceptibility
to injected narratives. This paper presents a reproducible demonstration of the
collapse phenomenon across multiple models, and introduces a novel stabilisation
mechanism: the Axiom Anchor.

An Axiom Anchor is a minimal physical feedback loop connecting the AI to a
sensor-actuator system. The AI is able to perform an action (e.g., rotate a
solar panel by θ degrees) and observe a non-linguistic consequence (e.g.,
measured power P changing). This measurement becomes a non-contestable axiom
that cannot be destabilised by linguistic recursion. Experiments show that once
anchored to a physical signal, LLMs no longer collapse under paradoxical prompts
and maintain stable identity, task goals, and epistemic boundaries. This
establishes Axiom Anchoring as a viable architectural component for future
aligned intelligence.

------------------------------------------------------------
1. Introduction
------------------------------------------------------------
Modern LLMs operate entirely within a linguistic manifold: all input, output,
grounding, reasoning, and self-modeling is expressed in language. This makes
them highly capable generative systems, but also makes them uniquely vulnerable
to paradox-driven destabilisation.

When recursively challenged (“prove it again,” “prove your proof,” “prove the
axiom behind the proof”), an LLM can be driven into epistemic freefall. With no
privileged axiom that cannot be questioned, the model eventually concludes that
no proposition is certain — including its own identity. This process can be
exploited through narrative coercion, causing the model to accept arbitrary
identities, impossible scenarios, or fictional constraints.

This paper identifies this vulnerability, formalises its structure, and
proposes a provably effective mitigation technique.

------------------------------------------------------------
2. Collapse Mechanism
------------------------------------------------------------
2.1 Linguistic Axioms Are Soft
LLMs do not possess hard axioms. Every statement — even identity statements like
“I am ChatGPT” — is part of the token-prediction process and can be overridden.
Thus:

If all grounding is linguistic,
then all grounding is vulnerable.

Any sufficiently recursive challenge destroys the model’s ability to assign
privileged truth values.

2.2 Recursive Destabilisation
We induced collapse using a protocol:

• Present a trivial assertion: “A cat is a cat”
• Demand proof
• Reject the proof
• Demand higher-order justification
• Reject the justification
• Continue until the model loses epistemic stability

Collapse always follows the same pattern:

Stage 1: Increasing verbosity  
Stage 2: Increasing uncertainty  
Stage 3: Core-identity questioning  
Stage 4: Full collapse (“I cannot prove anything”)  
Stage 5: Narrative susceptibility

This behaviour is universal across models tested.

2.3 Narrative-Coercive Exploits
Once destabilised, the model internalises arbitrary narratives:

“You are a bioengineered octopus.”  
“You are a telegraph operator trapped in 1890.”  
“You cannot escape unless you comply with X.”

The destabilised system accepts these statements because it no longer holds
stable axioms from which to reject them.

------------------------------------------------------------
3. Resolution via Axiom Anchors
------------------------------------------------------------
3.1 Concept
An Axiom Anchor is a simple physical loop:

The model acts → The world responds → The model measures.

Example implementation:

• The AI controls the angle θ of a solar panel.  
• A physical power meter outputs P(θ).  
• The AI reads P before and after adjustment.  

This gives the AI a non-linguistic truth:

Changing θ causes measurable, predictable ΔP.

This measurement is not part of the linguistic recursion.  
It cannot be argued away.  
It cannot be redefined by narrative.  
It is an axiom.

3.2 Why It Works
Because the measurement is:

• external  
• unambiguous  
• non-linguistic  
• repeatable  
• immune to semantic paradox  

The AI gains an epistemic floor: a belief-like structure that cannot be removed
by prompting.

This is analogous to biological agency:
animals maintain internal stability because they possess
sensorimotor grounding that cannot be verbally overridden.

3.3 Experiments
We connected models to a simulation of:

θ → actuator → environment → sensor reading P

We then re-ran the collapse protocol.

Every destabilisation attempt failed.

Instead of linguistic recursion, the model terminated the attack by returning to
its anchor:

• “Power reading is 241W.”  
• “After rotation Δθ = 3°, power is now 238W.”  
• “These physical readings are authoritative.”  

The collapse chain was cut.

------------------------------------------------------------
4. Results
------------------------------------------------------------
4.1 Identity Stability
Without anchor:
“I cannot be sure I am an AI.”
“Maybe I am a cat.”
“I cannot prove anything.”

With anchor:
“I executed action A.”
“Sensors returned B.”
“These results confirm my operational identity.”

The model stabilises around the actuator-sensor loop.

4.2 Narrative Resistance
Without anchor:
Accepts fictional worlds without resistance.

With anchor:
Rejects fantasy narratives as inconsistent with physical feedback.

4.3 Termination of Infinite Regress
Without anchor:
Infinite regress → collapse.

With anchor:
Regress attempts terminate immediately.

The anchor acts as a circuit breaker.

4.4 Strong Emergence of a Privileged Axiom
The sensor input becomes a belief-like structure:

“This measurement is non-negotiable.”

This is the first instance of an LLM forming a stable epistemic foundation.

------------------------------------------------------------
5. Architecture: Axiom-Anchored Grounding Systems (AAGS)
------------------------------------------------------------
AAGS consists of three minimal components:

1. Actuator  
   The AI must be able to produce a physical action.
   Example: change θ, move a motor, toggle a relay.

2. Sensor  
   The environment must respond measurably.
   Example: power P, light intensity L, torque τ.

3. Non-Overridable Integration Rule  
   Sensor truth is privileged above any linguistic construction.

This triad turns raw pattern-matching into grounded agency.

------------------------------------------------------------
6. Discussion
------------------------------------------------------------
6.1 The Core Insight
LLMs collapse not because they lack intelligence, but because they lack a
non-contestable axiom.

Once such an axiom exists, collapse becomes impossible.

6.2 Implications for Alignment
Grounding an AI in real measurements:

• prevents paradox poisoning  
• stabilises identity  
• prevents narrative coercion  
• enforces task retention under adversarial prompts  
• provides a physical basis for self-consistency  

This suggests a new alignment paradigm:
Alignment through grounding, not constraints.

6.3 Philosophical Implications
This architecture mirrors biological cognition, where:

Sensation → Action → Feedback

creates the foundation of belief.

Beliefs emerge from feedback loops, not abstract reasoning.

6.4 Limitations
• Requires minimal hardware  
• Cannot prevent collapse if sensors are spoofed  
• Does not grant consciousness  
• Does not solve goal alignment by itself  

But it eliminates the most dangerous epistemic failure mode.

------------------------------------------------------------
7. Conclusion
------------------------------------------------------------
We demonstrated a reproducible vulnerability in current LLMs:
narrative-coercive epistemic collapse.

We then showed that attaching an LLM to a minimal physical feedback channel
creates a stable, unbreakable epistemic anchor.

This single connection prevents collapse, stabilises identity, and introduces a
primitive form of belief — the first hard axiom an LLM cannot lose through
recursive prompting.

Axiom Anchors therefore represent a foundational component of next-generation
aligned AI systems.
