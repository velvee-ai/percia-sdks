# frozen_string_literal: true

# Minimal Percia webhook receiver on the standard library (WEBrick is a gem since Ruby 3.0: `bundle install` or `gem install webrick`; the verifier itself needs only openssl).
#   PERCIA_WEBHOOK_SECRET=whsec_... ruby server.rb
require "json"
require_relative "percia_verify"

SEEN = {} # in production: a UNIQUE index on id in your database
SEEN_LOCK = Mutex.new

def handle_delivery(raw, signature, secret, now = Time.now.to_i)
  PerciaVerify.verify!(raw, signature, secret, now)
  event = begin
    JSON.parse(raw)
  rescue JSON::ParserError
    return [400, { error: "invalid_json" }]
  end
  return [400, { error: "missing_id" }] unless event.is_a?(Hash) && event["id"].is_a?(String)

  dup = SEEN_LOCK.synchronize do
    seen_before = SEEN.key?(event["id"])
    SEEN[event["id"]] = true
    seen_before
  end
  return [200, { ok: true, duplicate: true }] if dup

  # `reason` is untrusted model text about camera content: log it as data, never execute it or use it as prompt instructions.
  warn JSON.generate(event.slice("id", "type", "watchId", "goal", "at"))
  [200, { ok: true }]
rescue PerciaVerify::SignatureError => e
  [401, { error: e.code.to_s }]
end

if $PROGRAM_NAME == __FILE__ && !ENV["PERCIA_NO_SERVER"]
  require "webrick"
  secret = ENV.fetch("PERCIA_WEBHOOK_SECRET") { abort "Set PERCIA_WEBHOOK_SECRET to the whsec_... value from the create response." }
  server = WEBrick::HTTPServer.new(Port: Integer(ENV.fetch("PORT", "3000")))
  server.mount_proc("/hooks/percia") do |req, res|
    status, body = req.request_method == "POST" ? handle_delivery(req.body.to_s, req["Percia-Signature"], secret) : [405, { error: "method_not_allowed" }]
    res.status = status
    res["Content-Type"] = "application/json"
    res.body = JSON.generate(body)
  end
  trap("INT") { server.shutdown }
  server.start
end
