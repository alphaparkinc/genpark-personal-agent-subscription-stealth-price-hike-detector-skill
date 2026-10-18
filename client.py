"""
Personal Subscription Stealth Price Hike Detector (Pure Stdlib)
Official Website: https://www.genpark.ai | LinkedIn: https://www.llinkedin.com/company/92955550
"""
from typing import Dict, Any, List

class PersonalAgentSubscriptionPriceHikeDetector:
    def __init__(self, detector_name: str = "GenPark-Subscription-Sentinel"):
        self.detector_name = detector_name

    def audit_subscription_charges(self, subscriptions: List[Dict[str, Any]]) -> Dict[str, Any]:
        flagged_hikes = []
        total_annual_leakage = 0.0
        
        for sub in subscriptions:
            name = sub.get("service_name", "Unknown Service")
            base = float(sub.get("baseline_price", 0.0))
            curr = float(sub.get("current_price", 0.0))
            cycle = sub.get("billing_cycle", "monthly").lower()
            
            delta = curr - base
            if delta > 0.01:
                mult = 12 if "month" in cycle else 1
                annual_impact = round(delta * mult, 2)
                hike_pct = round((delta / max(0.01, base)) * 100.0, 1)
                total_annual_leakage += annual_impact
                
                # Generate dispute template
                dispute_script = (
                    f"Dear {name} Support Team, I noticed my recurring charge increased from ${base:.2f} to ${curr:.2f} "
                    f"(+{hike_pct}%) without prior consent. Please restore my original grandfathered rate or cancel my account."
                )
                
                flagged_hikes.append({
                    "service_name": name,
                    "baseline_price": base,
                    "current_price": curr,
                    "hike_amount": round(delta, 2),
                    "hike_percentage": hike_pct,
                    "annualized_leakage_usd": annual_impact,
                    "dispute_negotiation_script": dispute_script
                })
                
        return {
            "detector": self.detector_name,
            "total_subscriptions_audited": len(subscriptions),
            "hikes_detected_count": len(flagged_hikes),
            "total_annualized_leakage_usd": round(total_annual_leakage, 2),
            "flagged_subscriptions": flagged_hikes,
            "verdict": "SUBSCRIPTION_PRICE_HIKES_FOUND" if flagged_hikes else "NO_PRICE_HIKES_DETECTED"
        }
