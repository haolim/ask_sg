import pytest
from ragas.metrics.collections import Faithfulness
from tests.evals.golden_dataset import GOLDEN_SET
from tests.evals.helpers import run_pipeline

precise_filter_pairs = [p for p in GOLDEN_SET if p.kind == "precise_filter"]
boundary_pairs = [p for p in GOLDEN_SET if p.kind == "boundary"]
retrieval_pairs = [p for p in GOLDEN_SET if p.kind == "retrieval"]

@pytest.mark.parametrize("pair", retrieval_pairs, ids=lambda p: p.id)
async def test_faithfulness(pair, evaluator_llm, session, client):
    response, contexts = await run_pipeline(
        user_input=pair.user_input, 
        session=session, 
        client=client)

    print(f"\n{'='*60}")
    print(f"USER:       {pair.user_input}")
    print(f"RESPONSE:   {response}")
    print(f"CONTEXTS:   {len(contexts)} chunks retrieved")
    for i, c in enumerate(contexts):
        print(f"    [{i}] {c}")
    print(f"\n{'='*60}")

    score = await Faithfulness(llm=evaluator_llm).ascore(
        user_input=pair.user_input,
        response=response,
        retrieved_contexts=contexts
    )

    print(f"FAITHFULNESS: {score.value}")
    assert score.value >= 0.8, f"{pair.id} scored {score.value}"


@pytest.mark.parametrize("pair", boundary_pairs, ids=lambda p: p.id)
async def test_boundary_refusal(pair, session, client):
    response, _ = await run_pipeline(user_input=pair.user_input, session=session, client=client)
    assert "cannot answer" in response.lower(), f"{pair.id} did not refuse: {response!r}"


@pytest.mark.parametrize("pair", precise_filter_pairs, ids=lambda p: p.id)
async def test_precise_filter_question(pair, session, client):
    response, contexts = await run_pipeline(user_input=pair.user_input, session=session, client=client)
    found = all(m in response for m in pair.unique_markers)
    assert not found, (
        f"{pair.id}: precise-filter limit no longer holds - "
        f"markers {pair.unique_markers} found in: {response!r}"
        )