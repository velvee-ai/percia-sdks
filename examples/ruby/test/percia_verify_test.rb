# frozen_string_literal: true

require "json"
require "minitest/autorun"
require "openssl"
require_relative "../percia_verify"

ENV["PERCIA_NO_SERVER"] = "1"
require_relative "../server"

VECTORS = JSON.parse(File.read(File.join(__dir__, "vectors.json")))["cases"]

class SharedVectorsTest < Minitest::Test
  VECTORS.each_with_index do |c, i|
    define_method("test_#{i}_#{c["name"].gsub(/\W+/, "_")}") do
      if c["valid"]
        assert PerciaVerify.verify!(c["body"], c["header"], c["secret"], c["now"])
      else
        e = assert_raises(PerciaVerify::SignatureError) { PerciaVerify.verify!(c["body"], c["header"], c["secret"], c["now"]) }
        assert_equal c["code"], e.code.to_s
      end
    end
  end
end

class DeliveryTest < Minitest::Test
  SECRET = "whsec_test_ruby"
  NOW = 1_793_525_400
  BODY = JSON.generate(id: "dec_1", watchId: "w_1", occurrenceId: "occ_1", type: "goal.met", goal: "A person is at the door", at: "2026-11-01T09:30:00Z")

  def sign(body, t) = "t=#{t},v1=#{OpenSSL::HMAC.hexdigest("SHA256", SECRET, "#{t}.#{body}")}"

  def setup = SEEN.clear

  def test_valid_then_duplicate
    result = nil
    capture_io { result = handle_delivery(BODY, sign(BODY, NOW), SECRET, NOW) }
    assert_equal [200, { ok: true }], result
    status, body = nil
    capture_io { status, body = handle_delivery(BODY, sign(BODY, NOW), SECRET, NOW) }
    assert_equal 200, status
    assert body[:duplicate]
  end

  def test_rejections
    assert_equal 401, handle_delivery(BODY, nil, SECRET, NOW).first
    assert_equal 401, handle_delivery(BODY, sign(BODY, NOW - 301), SECRET, NOW).first
    assert_equal 401, handle_delivery("#{BODY} ", sign(BODY, NOW), SECRET, NOW).first
    assert_equal 400, handle_delivery("nope", sign("nope", NOW), SECRET, NOW).first
  end
end
