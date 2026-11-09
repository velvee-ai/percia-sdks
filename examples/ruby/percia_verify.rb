# frozen_string_literal: true

# Verify a Percia webhook. Standard library only. Contract: docs/integrators/webhooks.md.
#
#   Percia-Signature: t=<unix seconds>,v1=<hex HMAC-SHA256(secret, "<t>.<raw body>")>
#
#   PerciaVerify.verify!(raw_body, request.env["HTTP_PERCIA_SIGNATURE"], ENV["PERCIA_WEBHOOK_SECRET"])
#
# Pass the RAW request body (request.body.read), before any JSON parsing.
require "openssl"

module PerciaVerify
  TOLERANCE_S = 300

  # `code` is :malformed, :stale_timestamp or :mismatch.
  class SignatureError < StandardError
    attr_reader :code

    def initialize(code)
      @code = code
      super(code.to_s)
    end
  end

  module_function

  def verify!(raw_body, header, secret, now = Time.now.to_i)
    t = nil
    candidates = []
    header.to_s.split(",").each do |part|
      key, sep, value = part.partition("=")
      next if sep.empty?

      key = key.strip
      value = value.strip
      if key == "t" && value.match?(/\A[0-9]{1,12}\z/)
        t = value.to_i
      elsif key == "v1" && !value.empty?
        candidates << value
      end
    end
    raise SignatureError, :malformed if t.nil? || candidates.empty?
    raise SignatureError, :stale_timestamp if (now - t).abs > TOLERANCE_S

    expected = OpenSSL::HMAC.hexdigest("SHA256", secret.to_s, "#{t}.".b + raw_body.to_s.b)
    ok = candidates.any? { |c| c.bytesize == expected.bytesize && OpenSSL.fixed_length_secure_compare(c, expected) }
    raise SignatureError, :mismatch unless ok

    true
  end

  def valid?(*args)
    verify!(*args)
  rescue SignatureError
    false
  end
end
