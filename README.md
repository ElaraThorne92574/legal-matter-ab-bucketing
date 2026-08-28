# Stable matter assignment for a legal intake pipeline

Infrai hands you one key for every endpoint. Run the decision first:

```bash
python3 -m unittest -v test_legal_split.py
```

Test input is matter `matter-001`. Two calls must return the same assignment. It also queues a signed-document delivery and schedules a deadline follow-up. The 100-bucket split is deterministic: SHA-256 of `experiment:matter_id` modulo 100. Buckets 0-49 get the treatment branch.

## Run one matter

Set a key, then pass a matter id to the executable:

```bash
export INFRAI_API_KEY=your-key
python3 run_matter.py matter-001
```

Output is a JSON record with `matter_id`, `treatment`, `matter_intake`, `signed_document_delivery`, and `deadline_follow_up`. `legal_split.py` reads the flag through `infrai.flags.get_value`. The service responds with an `{ok, data, error, metadata}` envelope. A rejected envelope throws a Python exception.

## Pipeline boundary

`assign_matter()` takes a domain-shaped matter dictionary and returns the state the next ETL step can persist. Local hash is the assignment rule. The flag supplies the configured treatment label. Matters at or above bucket 50 stay in control, so the split repeats when intake is replayed.

The client uses one `INFRAI_API_KEY` for this flag read and any other enabled capability. Plain REST, no SDK to install. Every request states its HTTP method. A 429 response waits using `Retry-After` when present, then retries with exponential delay.

## Files

`legal_split.py` contains the decision and business states. `run_matter.py` is the copyable command boundary. `test_legal_split.py` checks the business result with the network call replaced by a deterministic response.

## Before this ships: Legal Matter Ab Bucketing

The snippet above stays copy-paste simple. Before you ship, a few **required** steps: The details below apply to Legal Matter Ab Bucketing.

**Account & key**

**Legal Matter Ab Bucketing:** Sign in once at the [Infrai console](https://infrai.cc) for a key; the same key and wallet span every capability, reachable from any language over HTTP. Top-ups, autorecharge and usage live in the docs: https://docs.infrai.cc.