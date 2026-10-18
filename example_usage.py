from client import PersonalAgentSubscriptionPriceHikeDetector

def main():
    detector = PersonalAgentSubscriptionPriceHikeDetector()
    items = [
        {"service_name": "DevAI Copilot", "billing_cycle": "monthly", "baseline_price": 20.0, "current_price": 29.0},
        {"service_name": "Gym Pass", "billing_cycle": "monthly", "baseline_price": 50.0, "current_price": 65.0}
    ]
    res = detector.audit_subscription_charges(items)
    print("--- Subscription Hike Audit ---")
    print(f"Hikes Detected: {res['hikes_detected_count']} | Total Annual Leakage: ${res['total_annualized_leakage_usd']}")
    for f in res['flagged_subscriptions']:
        print(f"* {f['service_name']}: +${f['hike_amount']} (+{f['hike_percentage']}%)")
        print(f"  Negotiation Script: {f['dispute_negotiation_script'][:80]}...")

if __name__ == "__main__":
    main()
