#!/usr/bin/env python3
import json
import sys
from client import PersonalAgentSubscriptionPriceHikeDetector

def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        detector = PersonalAgentSubscriptionPriceHikeDetector()
        subs = [
            {"service_name": "CloudStream Pro", "billing_cycle": "monthly", "baseline_price": 9.99, "current_price": 14.99},
            {"service_name": "MusicMax", "billing_cycle": "monthly", "baseline_price": 10.99, "current_price": 10.99}
        ]
        res = detector.audit_subscription_charges(subs)
        assert res["hikes_detected_count"] == 1
        assert res["total_annualized_leakage_usd"] == 60.0
        print(f"[TEST PASS] Subscription Price Hike Leakage: ${res['total_annualized_leakage_usd']}/yr")
        sys.exit(0)

    for line in sys.stdin:
        if not line.strip():
            continue
        try:
            req = json.loads(line)
            method = req.get("method")
            msg_id = req.get("id")
            if method == "initialize":
                print(json.dumps({"jsonrpc": "2.0", "id": msg_id, "result": {"serverInfo": {"name": "genpark-subscription-hike-detector", "version": "1.0.0"}}}))
            elif method == "tools/list":
                print(json.dumps({"jsonrpc": "2.0", "id": msg_id, "result": {"tools": [{"name": "audit_subscription_charges", "description": "Detect sneaky price hikes in consumer subscriptions"}]}}))
            elif method == "tools/call":
                args = req.get("params", {}).get("arguments", {})
                detector = PersonalAgentSubscriptionPriceHikeDetector()
                out = detector.audit_subscription_charges(args.get("subscriptions", []))
                print(json.dumps({"jsonrpc": "2.0", "id": msg_id, "result": {"content": [{"type": "text", "text": json.dumps(out)}]}}))
            else:
                print(json.dumps({"jsonrpc": "2.0", "id": msg_id, "error": {"code": -32601, "message": "Method not found"}}))
            sys.stdout.flush()
        except Exception as e:
            print(json.dumps({"jsonrpc": "2.0", "error": {"code": -32603, "message": str(e)}}))
            sys.stdout.flush()

if __name__ == "__main__":
    main()
