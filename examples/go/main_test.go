package main

import (
	"crypto/hmac"
	"crypto/sha256"
	"encoding/hex"
	"encoding/json"
	"fmt"
	"net/http"
	"net/http/httptest"
	"os"
	"strings"
	"testing"
	"time"
)

type vector struct {
	Name   string  `json:"name"`
	Secret string  `json:"secret"`
	Body   string  `json:"body"`
	Now    int64   `json:"now"`
	Header string  `json:"header"`
	Valid  bool    `json:"valid"`
	Code   *string `json:"code"`
}

func TestSharedVectors(t *testing.T) {
	raw, err := os.ReadFile("testdata/vectors.json")
	if err != nil {
		t.Fatal(err)
	}
	var f struct{ Cases []vector }
	if err := json.Unmarshal(raw, &f); err != nil {
		t.Fatal(err)
	}
	if len(f.Cases) == 0 {
		t.Fatal("no vectors")
	}
	for _, c := range f.Cases {
		t.Run(c.Name, func(t *testing.T) {
			err := Verify(c.Secret, c.Header, []byte(c.Body), c.Now)
			if c.Valid {
				if err != nil {
					t.Fatalf("want valid, got %v", err)
				}
				return
			}
			if err == nil || err.Error() != *c.Code {
				t.Fatalf("want %s, got %v", *c.Code, err)
			}
		})
	}
}

const secret = "whsec_test_go"

var now = time.Unix(1793525400, 0)

func sign(body string, ts int64) string {
	m := hmac.New(sha256.New, []byte(secret))
	fmt.Fprintf(m, "%d.%s", ts, body)
	return fmt.Sprintf("t=%d,v1=%s", ts, hex.EncodeToString(m.Sum(nil)))
}

func send(h http.Handler, body, sig string) *httptest.ResponseRecorder {
	req := httptest.NewRequest(http.MethodPost, "/hooks/percia", strings.NewReader(body))
	if sig != "" {
		req.Header.Set("Percia-Signature", sig)
	}
	rec := httptest.NewRecorder()
	h.ServeHTTP(rec, req)
	return rec
}

const body = `{"id":"dec_1","watchId":"w_1","occurrenceId":"occ_1","type":"goal.met","goal":"A person is at the door","at":"2026-11-01T09:30:00Z"}`

func TestReceiver(t *testing.T) {
	got := make(chan Event, 4)
	r := &Receiver{Secret: secret, Now: func() time.Time { return now }, OnEvent: func(e Event) { got <- e }}

	if rec := send(r, body, sign(body, now.Unix())); rec.Code != 200 {
		t.Fatalf("valid: %d", rec.Code)
	}
	select {
	case e := <-got:
		if e.ID != "dec_1" {
			t.Fatal(e)
		}
	case <-time.After(time.Second):
		t.Fatal("handler not called")
	}
	rec := send(r, body, sign(body, now.Unix()))
	if rec.Code != 200 || !strings.Contains(rec.Body.String(), "duplicate") {
		t.Fatalf("duplicate: %d %s", rec.Code, rec.Body)
	}
	select {
	case <-got:
		t.Fatal("handler ran twice")
	case <-time.After(50 * time.Millisecond):
	}
}

func TestRejections(t *testing.T) {
	r := &Receiver{Secret: secret, Now: func() time.Time { return now }}
	for name, rec := range map[string]*httptest.ResponseRecorder{
		"missing header": send(r, body, ""),
		"stale":          send(r, body, sign(body, now.Unix()-301)),
		"tampered":       send(r, body+" ", sign(body, now.Unix())),
		"bad mac":        send(r, body, fmt.Sprintf("t=%d,v1=%s", now.Unix(), strings.Repeat("0", 64))),
	} {
		if rec.Code != 401 {
			t.Errorf("%s: want 401, got %d", name, rec.Code)
		}
	}
	if rec := send(r, "nope", sign("nope", now.Unix())); rec.Code != 400 {
		t.Errorf("not json: %d", rec.Code)
	}
}
