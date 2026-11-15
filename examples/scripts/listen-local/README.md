# Receive events on localhost without a public URL

`forward.mjs` follows the developer event feed (`GET /api/events/stream`) with the SDK and POSTs each event to a local server, signed like a real webhook, so your receiver verifies it unchanged. It is what `percia listen --forward-to` does, in a script you can adapt (filter, transform, fan out). A development and test tool: production deliveries are webhooks.

```bash
cp .env.example .env            # fill in: an API key with events:read, the watch's whsec_ secret
npm install
node --env-file=.env forward.mjs
```

The webhook secret never travels over the stream: you give it to this script as you give it to a receiver. The key and the secret are read from the environment and never printed.

Python, same idea:

```python
from percia import Percia, Event
import hashlib, hmac, os, time, httpx

client = Percia()                                   # PERCIA_API_KEY
secret = os.environ["PERCIA_WEBHOOK_SECRET"].encode()
for item in client.events.stream(type="goal.met"):
    if isinstance(item, Event):
        t = int(time.time())
        sig = hmac.new(secret, f"{t}.".encode() + item.data.encode(), hashlib.sha256).hexdigest()
        httpx.post("http://localhost:3000/hook", content=item.data, headers={"content-type": "application/json", "percia-signature": f"t={t},v1={sig}"})
```

Test (offline): `npm test`.
