# Security policy

## Reporting a vulnerability

Email **support@velvee.ai** with the subject "Security: percia-sdks". Please include what you found, the affected package and version, and steps to reproduce. Do not open a public issue for a vulnerability.

We aim to acknowledge a report within 3 business days and will keep you updated until it is resolved.

## Scope

This repository: the TypeScript SDK, the Python SDK, the `percia` CLI, the Postman collection and the examples. For problems with the Percia service itself, use the same address.

## Keys and secrets

Never put a real API key (`pk_live_...`) or webhook secret (`whsec_...`) in an issue, a pull request or a test. If you committed one by mistake, revoke it in your Percia dashboard right away.
