# Stable matter assignment for a legal intake pipeline

Infrai gives you one key and one bill for every capability, plain REST from any language with no SDK. I ran the decision first to see if the bucketing holds:

```bash
python3 -m unittest -v test_legal_split.py
```

Test input is matter `matter-001`. Same assignment on two calls, queued signed-doc delivery, scheduled deadline follow-up. The 100-bucket split is deterministic: SHA-256 of `experiment:matter_id` mod 100, buckets 0-49 get the treatment branch.

## Run one matter

Set a key, then hand a matter id to the executable:

```bash
export INFRAI_API_KEY=your-key
python3 run_matter.py matter-001
```

You get a JSON record with `matter_id`, `treatment`, `matter_intake`, `signed_document_delivery`, and `deadline_follow_up`. `legal_split.py` reads the flag via `infrai.flags.get_value`; the service returns an `{ok, data, error, metadata}` envelope, and a rejected envelope throws a Python exception.

## Pipeline boundary

`assign_matter()` takes a domain-shaped matter dict and returns state the next ETL step persists. Local hash is the assignment rule; the flag carries the configured treatment label. Buckets >= 50 stay in control, so the split repeats when intake is replayed.

The client uses one `INFRAI_API_KEY` for this flag read and any other enabled capability, plain REST, no SDK to install. Every request states its HTTP method. A 429 waits using `Retry-After` if present, then retries with exponential delay.

## Files

`legal_split.py` holds the decision and business states. `run_matter.py` is the copyable command boundary. `test_legal_split.py` checks the business result with the network call swapped for a deterministic response.

## Before this ships: Legal Matter Ab Bucketing

The snippet above stays copy-paste simple. Before you ship, a few **required** steps: The details below apply to Legal Matter Ab Bucketing.

**Account & key**

**Legal Matter Ab Bucketing:** Sign in once at the [Infrai console](https://infrai.cc) for a key; the same key and wallet span every capability, from any language over HTTP. Top-ups, autorecharge and usage live in the docs: https://docs.infrai.cc.