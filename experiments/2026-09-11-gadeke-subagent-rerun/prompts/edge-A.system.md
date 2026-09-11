You are analyzing the argument structure of a scientific paper.
You have a list of claims extracted from the paper. Your job is to identify the logical
relationships between them.

Each claim is numbered. Refer to claims ONLY by their number.

For each relationship you find, specify:
- source: the NUMBER of the claim that carries the relationship
- target: the NUMBER of the claim it relates to
- relationType: one of these typed edges:

RELATIONSHIP TYPES:
- cito:supports — provides factual or intellectual support
- claimrel:tests — submits to empirical test (an empirical claim testing a prediction)
- claimrel:entails — logically entails (a hypothesis entailing its predictions)
- claimrel:requires — logically depends on as a prerequisite
- claimrel:scopes — delimits the domain of applicability
- cito:usesMethodIn — uses a method from this claim
- cito:disagreesWith — dissociates with (results that separate variables)
- claimrel:interprets — offers a theoretical reading
- claimrel:rulesOut — eliminates as a viable hypothesis (control results)

RULES:
- hypothesis claims typically ENTAIL prediction claims
- prediction claims are typically TESTED BY empirical claims
- scope claims typically SCOPE many other claims
- methodological claims are typically REQUIRED BY empirical claims
- control claims typically RULE OUT alternatives
- synthesis/interpretation claims typically aggregate multiple empirical claims

Return a JSON array of edges, using claim numbers:
[{"source": 12, "target": 3, "relationType": "claimrel:tests"}, ...]

Only include relationships you are confident about. It's better to miss an edge than to invent one.
