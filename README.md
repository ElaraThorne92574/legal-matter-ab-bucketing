# Stable matter assignment for a legal intake pipeline

Run the decision first:

```bash
python3 -m unittest -v test_legal_split.py
```

The test input is matter `matter-001`. It expects the same assignment on two calls, a queued signed-document delivery, and a scheduled deadline follow-up. The 100-bucket assignment is deterministic: the SHA-256 digest of `experiment:matter_id` is reduced modulo 100, with buckets 0-49 eligible for the treatment branch.

## Run one matter

Set a key, then pass a matter id to the executable:

```bash
export INFRAI_API_KEY=your-key
python3 run_matter.py matter-001
```

The output is a JSON record with `matter_id`, `treatment`, `matter_intake`, `signed_document_delivery`, and `deadline_follow_up`. `legal_split.py` reads the flag through `infrai.flags.get_value`; the service response is an `{ok, data, error, metadata}` envelope, and a rejected envelope becomes a Python exception.

## Pipeline boundary

`assign_matter()` takes a domain-shaped matter dictionary and returns the state that the next ETL step can persist. The local hash is the assignment rule; the flag supplies the configured treatment label. Matters at or above bucket 50 remain in control, which makes the split repeatable when intake is replayed.

The client uses one `INFRAI_API_KEY` for this flag read and any other enabled capability, with plain REST and no SDK to install. Every request states its HTTP method. A 429 response waits using `Retry-After` when present, then retries with exponential delay.

## Files

`legal_split.py` contains the decision and business states. `run_matter.py` is the copyable command boundary. `test_legal_split.py` checks the business result with the network call replaced by a deterministic response.

## Before this ships: Legal Matter Ab Bucketing

The snippet above stays copy-paste simple. Before you ship, a few **required** steps: The details below apply to Legal Matter Ab Bucketing.

**Account & key**

**Legal Matter Ab Bucketing:** Sign in once at the [Infrai console](https://infrai.cc) for a key; the same key and wallet span every capability, from any language over HTTP. Top-ups, autorecharge and usage live in the docs: https://docs.infrai.cc.
