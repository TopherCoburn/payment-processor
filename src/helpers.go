package paymentprocessor

import (
	"encoding/json"
	"errors"
	"fmt"
	"log"
	"net/http"
	"time"

	"github.com/google/uuid"
)

// PaymentStatus represents the status of a payment
type PaymentStatus string

const (
	// Pending represents a payment that is pending
	Pending PaymentStatus = "pending"
	// Success represents a payment that was successful
	Success PaymentStatus = "success"
	// Failed represents a payment that failed
	Failed PaymentStatus = "failed"
)

// Payment represents a payment
type Payment struct {
	ID        string       `json:"id"`
	Amount    float64      `json:"amount"`
	Currency  string       `json:"currency"`
	Status    PaymentStatus `json:"status"`
	Timestamp time.Time     `json:"timestamp"`
}

// NewPayment creates a new payment
func NewPayment(amount float64, currency string) (*Payment, error) {
	if amount <= 0 {
		return nil, errors.New("amount must be greater than zero")
	}
	if currency == "" {
		return nil, errors.New("currency is required")
	}
	payment := &Payment{
		ID:        uuid.New().String(),
		Amount:    amount,
		Currency:  currency,
		Status:    Pending,
		Timestamp: time.Now(),
	}
	return payment, nil
}

// UpdateStatus updates the status of a payment
func (p *Payment) UpdateStatus(status PaymentStatus) error {
	if status != Pending && status != Success && status != Failed {
		return errors.New("invalid payment status")
	}
	p.Status = status
	return nil
}

// ToJSON converts a payment to JSON
func (p *Payment) ToJSON() ([]byte, error) {
	return json.Marshal(p)
}

// FromJSON converts JSON to a payment
func FromJSON(data []byte) (*Payment, error) {
	var payment Payment
	err := json.Unmarshal(data, &payment)
	if err != nil {
		return nil, err
	}
	return &payment, nil
}

// HandlePayment handles a payment request
func HandlePayment(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodPost {
		http.Error(w, "invalid request method", http.StatusBadRequest)
		return
	}
	var payment Payment
	err := json.NewDecoder(r.Body).Decode(&payment)
	if err != nil {
		http.Error(w, err.Error(), http.StatusBadRequest)
		return
	}
	err = payment.UpdateStatus(Success)
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}
	json, err := payment.ToJSON()
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}
	w.Header().Set("Content-Type", "application/json")
	w.Write(json)
}

func main() {
	http.HandleFunc("/payment", HandlePayment)
	log.Fatal(http.ListenAndServe(":8080", nil))
}