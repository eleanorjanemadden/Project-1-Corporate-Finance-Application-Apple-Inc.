TARGET = {"name": "Asbury Automotive (ABG)", "price": 243.03, "diluted_eps": 21.50}

PEERS = [
    {"name": "AutoNation (AN)", "price": 169.84, "diluted_eps": 16.92},
    {"name": "Group 1 Automotive (GPI)", "price": 421.48, "diluted_eps": 36.81},
]


import math
from statistics import median


def positive_number(value):
    """Accept finite positive numbers, treating missing/invalid inputs as unusable."""
    if value is None or isinstance(value, bool):
        return None
    try:
        number = float(value)
    except (TypeError, ValueError, OverflowError):
        return None
    return number if math.isfinite(number) and number > 0 else None


def pe_ratio(company):
    price = positive_number(company.get("price"))
    eps = positive_number(company.get("diluted_eps"))
    if price is None or eps is None:
        return None
    return positive_number(price / eps)


def implied_price(multiple, eps):
    if eps is None:
        return None
    return positive_number(multiple * eps)


def money(value):
    return "not meaningful" if value is None else f"${value:,.2f}"


def main():
    target_key = TARGET["name"].strip().casefold()
    seen = {target_key}
    peers = []
    for peer in PEERS:
        key = peer["name"].strip().casefold()
        if key in seen:
            continue
        seen.add(key)
        peers.append(peer)

    target_eps = positive_number(TARGET.get("diluted_eps"))
    target_pe = pe_ratio(TARGET)
    print(f"Target: {TARGET['name']}")
    print("Target P/E: " + (
        "not meaningful" if target_pe is None else f"{target_pe:.6f}x"
    ))
    print("P/E uses price / diluted EPS; implied price uses peer P/E × target EPS.")
    print("Missing, nonpositive, or nonfinite inputs make affected calculations "
          "not meaningful. A missing target price does not prevent implied prices.")

    valid = []
    print("\nPeers (deduplicated; target excluded):")
    for index, peer in enumerate(peers):
        multiple = pe_ratio(peer)
        if multiple is None:
            print(f"  {peer['name']}: P/E and implied price not meaningful")
        else:
            valid.append((index, multiple))
            print(f"  {peer['name']}: {multiple:.6f}x; "
                  f"implied price {money(implied_price(multiple, target_eps))}")

    multiples = [multiple for _, multiple in valid]
    full_estimate = None
    if not multiples:
        print("\nNo usable peers; peer P/E statistics and implied prices "
              "not meaningful.")
    else:
        full_median = median(multiples)
        full_estimate = implied_price(full_median, target_eps)
        print(f"\nMedian peer P/E: {full_median:.6f}x")
        if len(multiples) == 1:
            print(f"Reference estimate: {money(full_estimate)} "
                  "(one valid peer; no range)")
        else:
            for label, multiple in (
                ("Minimum", min(multiples)),
                ("Median", full_median),
                ("Maximum", max(multiples)),
            ):
                print(f"{label}: {multiple:.6f}x; "
                      f"implied price {money(implied_price(multiple, target_eps))}")

    print("\nLeave-one-peer-out sensitivity (change from full-peer estimate):")
    if not peers:
        print("  No peers to remove.")
    for index, peer in enumerate(peers):
        remaining = [multiple for peer_index, multiple in valid
                     if peer_index != index]
        if not remaining:
            print(f"  Remove {peer['name']}: no estimate (no usable peers remain)")
            continue
        estimate = implied_price(median(remaining), target_eps)
        # Keep full floating-point precision throughout; round only for display.
        change = None if estimate is None or full_estimate is None else (
            estimate - full_estimate
        )
        change_text = "not meaningful" if change is None else f"{change:+,.2f} dollars"
        qualifier = " (reference estimate; one valid peer)" if len(remaining) == 1 else ""
        print(f"  Remove {peer['name']}: median-implied price {money(estimate)}; "
              f"change {change_text}{qualifier}")


if __name__ == "__main__":
    main()

