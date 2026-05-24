#!/usr/bin/env python3

from __future__ import annotations

import argparse
import math


def floor_to_step(value: float, step: float) -> float:
    if step <= 0:
        raise ValueError("lot step must be greater than 0")
    return math.floor(value / step) * step


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Calculate Forex position size from balance, risk %, and stop loss."
    )
    parser.add_argument("--balance", type=float, required=True, help="Current account balance in USD")
    parser.add_argument("--risk-percent", type=float, required=True, help="Risk per trade in percent")
    parser.add_argument("--stop-loss-pips", type=float, required=True, help="Stop loss distance in pips")
    parser.add_argument(
        "--pip-value-per-standard-lot",
        type=float,
        default=10.0,
        help="Pip value for 1.00 standard lot, default is 10 USD",
    )
    parser.add_argument(
        "--lot-step",
        type=float,
        default=0.01,
        help="Minimum lot increment supported by broker, default is 0.01",
    )
    parser.add_argument(
        "--rr",
        type=float,
        default=2.0,
        help="Risk to reward ratio target, default is 2.0",
    )
    return parser


def validate_args(args: argparse.Namespace) -> None:
    if args.balance <= 0:
        raise ValueError("balance must be greater than 0")
    if args.risk_percent <= 0:
        raise ValueError("risk percent must be greater than 0")
    if args.stop_loss_pips <= 0:
        raise ValueError("stop loss pips must be greater than 0")
    if args.pip_value_per_standard_lot <= 0:
        raise ValueError("pip value per standard lot must be greater than 0")
    if args.rr <= 0:
        raise ValueError("RR must be greater than 0")


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    validate_args(args)

    risk_amount = args.balance * (args.risk_percent / 100.0)
    exact_lot = risk_amount / (args.stop_loss_pips * args.pip_value_per_standard_lot)
    rounded_lot = floor_to_step(exact_lot, args.lot_step)
    rounded_risk_amount = rounded_lot * args.stop_loss_pips * args.pip_value_per_standard_lot
    rounded_risk_percent = (rounded_risk_amount / args.balance) * 100.0
    take_profit_pips = args.stop_loss_pips * args.rr
    win_amount = rounded_risk_amount * args.rr

    print("Forex Position Size Calculator")
    print(f"Balance:                {args.balance:.2f} USD")
    print(f"Risk %:                 {args.risk_percent:.2f}%")
    print(f"Risk amount:            {risk_amount:.2f} USD")
    print(f"Stop loss:              {args.stop_loss_pips:.2f} pips")
    print(f"Pip value / 1.00 lot:   {args.pip_value_per_standard_lot:.2f} USD")
    print(f"Exact lot size:         {exact_lot:.4f}")
    print(f"Rounded lot size:       {rounded_lot:.4f}")
    print(f"Actual risk after round:{rounded_risk_amount:8.2f} USD ({rounded_risk_percent:.2f}%)")
    print(f"Target RR:              1:{args.rr:.2f}")
    print(f"Take profit distance:   {take_profit_pips:.2f} pips")
    print(f"Potential win amount:   {win_amount:.2f} USD")

    if rounded_lot <= 0:
        print("\nWarning: rounded lot size is 0.0000.")
        print("Your broker lot step may be too large for this balance/risk/stop combination.")
    elif rounded_risk_percent > args.risk_percent:
        print("\nWarning: actual risk is above your requested risk after lot rounding.")
        print("Consider a smaller lot step, tighter stop, or lower risk percent.")
    elif rounded_risk_percent < args.risk_percent * 0.75:
        print("\nNote: actual risk is materially below target after lot rounding.")
        print("This is safer, but growth may be slower than your compounding plan.")


if __name__ == "__main__":
    main()
