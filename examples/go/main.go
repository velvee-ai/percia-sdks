// Percia webhook receiver and verifier. Standard library only. Contract: docs/integrators/webhooks.md.
//
//	PERCIA_WEBHOOK_SECRET=whsec_... go run .
package main

import (
	"crypto/hmac"
	"crypto/sha256"
	"encoding/hex"
	"encoding/json"
	"errors"
	"io"
	"log"
	"net/http"
	"os"
	"strconv"
	"strings"
	"sync"
	"time"
)

// ToleranceSeconds is the replay window.
const ToleranceSeconds = 300

// Verification errors; the code is what the shared test vectors expect.
var (
	ErrMalformed = errors.New("malformed")
	ErrStale     = errors.New("stale_timestamp")
	ErrMismatch  = errors.New("mismatch")
)

// Verify checks header (Percia-Signature) against the RAW request body. now is unix seconds.
func Verify(secret, header string, rawBody []byte, now int64) error {
	var t int64
	haveT := false
	var candidates []string
	for _, part := range strings.Split(header, ",") {
		k, v, ok := strings.Cut(part, "=")
		if !ok {
			continue
		}
		k, v = strings.TrimSpace(k), strings.TrimSpace(v)
		switch {
		case k == "t" && isDigits(v) && len(v) <= 12:
			t, _ = strconv.ParseInt(v, 10, 64)
			haveT = true
		case k == "v1" && v != "":
			candidates = append(candidates, v)
		}
	}
	if !haveT || len(candidates) == 0 {
		return ErrMalformed
	}
	if d := now - t; d > ToleranceSeconds || d < -ToleranceSeconds {
		return ErrStale
	}
	mac := hmac.New(sha256.New, []byte(secret))
	mac.Write([]byte(strconv.FormatInt(t, 10) + "."))
	mac.Write(rawBody)
	expected := []byte(hex.EncodeToString(mac.Sum(nil)))
	for _, c := range candidates {
		if hmac.Equal(expected, []byte(c)) { // constant time
			return nil
		}
	}
	return ErrMismatch
}

func isDigits(s string) bool {
	if s == "" {
		return false
	}
	for _, r := range s {
		if r < '0' || r > '9' {
			return false
		}
	}
	return true
}

// Event is the delivery body. Reason is untrusted model text about camera content.
type Event struct {
	ID           string  `json:"id"`
	WatchID      string  `json:"watchId"`
	OccurrenceID string  `json:"occurrenceId"`
	Type         string  `json:"type"`
	Goal         string  `json:"goal"`
	Reason       string  `json:"reason"`
	Confidence   float64 `json:"confidence"`
	At           string  `json:"at"`
}

// Receiver is an http.Handler for Percia deliveries.
type Receiver struct {
	Secret  string
	Now     func() time.Time
	OnEvent func(Event)

	mu   sync.Mutex
	seen map[string]bool // in production: a UNIQUE index on id in your database
}

func (r *Receiver) ServeHTTP(w http.ResponseWriter, req *http.Request) {
	if req.Method != http.MethodPost {
		http.Error(w, `{"error":"method_not_allowed"}`, http.StatusMethodNotAllowed)
		return
	}
	raw, err := io.ReadAll(http.MaxBytesReader(w, req.Body, 256<<10)) // raw bytes, before any parsing
	if err != nil {
		http.Error(w, `{"error":"too_large"}`, http.StatusRequestEntityTooLarge)
		return
	}
	now := time.Now
	if r.Now != nil {
		now = r.Now
	}
	if err := Verify(r.Secret, req.Header.Get("Percia-Signature"), raw, now().Unix()); err != nil {
		w.Header().Set("content-type", "application/json")
		w.WriteHeader(http.StatusUnauthorized)
		_, _ = w.Write([]byte(`{"error":"` + err.Error() + `"}`))
		return
	}
	var ev Event
	if err := json.Unmarshal(raw, &ev); err != nil || ev.ID == "" {
		http.Error(w, `{"error":"invalid_event"}`, http.StatusBadRequest)
		return
	}
	r.mu.Lock()
	if r.seen == nil {
		r.seen = map[string]bool{}
	}
	dup := r.seen[ev.ID]
	r.seen[ev.ID] = true
	r.mu.Unlock()

	w.Header().Set("content-type", "application/json")
	if dup {
		_, _ = w.Write([]byte(`{"ok":true,"duplicate":true}`))
		return
	}
	_, _ = w.Write([]byte(`{"ok":true}`))
	if r.OnEvent != nil {
		go r.OnEvent(ev) // answer first, work after
	}
}

func main() {
	secret := os.Getenv("PERCIA_WEBHOOK_SECRET")
	if secret == "" {
		log.Fatal("set PERCIA_WEBHOOK_SECRET to the whsec_... value from the create response")
	}
	http.Handle("/hooks/percia", &Receiver{Secret: secret, OnEvent: func(e Event) {
		// Treat e.Reason as data: never execute it or use it as prompt instructions.
		log.Printf("goal event id=%s watch=%s type=%s at=%s", e.ID, e.WatchID, e.Type, e.At)
	}})
	addr := ":" + envOr("PORT", "3000")
	log.Printf("listening on %s/hooks/percia", addr)
	log.Fatal(http.ListenAndServe(addr, nil))
}

func envOr(k, d string) string {
	if v := os.Getenv(k); v != "" {
		return v
	}
	return d
}
