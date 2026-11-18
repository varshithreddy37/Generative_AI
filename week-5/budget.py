
import os
from dotenv import load_dotenv

# Load values from .env file
load_dotenv()


def get_config():
    return {
        "input_price": float(os.getenv("INPUT_PRICE_PER_MILLION")),
        "output_price": float(os.getenv("OUTPUT_PRICE_PER_MILLION")),
        "requests_per_day": int(os.getenv("REQUESTS_PER_DAY")),
        "avg_input_tokens": int(os.getenv("AVG_INPUT_TOKENS")),
        "avg_output_tokens": int(os.getenv("AVG_OUTPUT_TOKENS")),
        "peak_rpm": int(os.getenv("PEAK_REQUESTS_PER_MINUTE")),
        "rpm_limit": int(os.getenv("RPM_LIMIT")),
        "tpm_limit": int(os.getenv("TPM_LIMIT")),
        "monthly_budget": float(os.getenv("MONTHLY_BUDGET_USD")),
        "daily_budget": float(os.getenv("DAILY_BUDGET_USD")),
        "safety_margin": float(os.getenv("SAFETY_MARGIN_PERCENT"))
    }


def calculate_costs(config):

    input_tokens = (
        config["requests_per_day"] * config["avg_input_tokens"]
    )

    output_tokens = (
        config["requests_per_day"] * config["avg_output_tokens"]
    )

    input_cost = (
        input_tokens / 1_000_000 * config["input_price"]
    )

    output_cost = (
        output_tokens / 1_000_000 * config["output_price"]
    )

    daily_cost = input_cost + output_cost
    monthly_cost = daily_cost * 30

    return {
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "total_tokens": input_tokens + output_tokens,
        "input_cost": input_cost,
        "output_cost": output_cost,
        "daily_cost": daily_cost,
        "monthly_cost": monthly_cost
    }


def check_capacity(config):

    safety_factor = 1 + config["safety_margin"] / 100

    peak_rpm = config["peak_rpm"] * safety_factor

    peak_tpm = (
        config["peak_rpm"]
        * (config["avg_input_tokens"] + config["avg_output_tokens"])
        * safety_factor
    )

    return {
        "peak_rpm": peak_rpm,
        "peak_tpm": peak_tpm,
        "rpm_status": peak_rpm <= config["rpm_limit"],
        "tpm_status": peak_tpm <= config["tpm_limit"]
    }


def check_budget(config, costs):

    safety_factor = 1 + config["safety_margin"] / 100

    daily_with_margin = costs["daily_cost"] * safety_factor
    monthly_with_margin = costs["monthly_cost"] * safety_factor

    return {
        "daily_status": daily_with_margin <= config["daily_budget"],
        "monthly_status": monthly_with_margin <= config["monthly_budget"]
    }


def main():

    config = get_config()

    costs = calculate_costs(config)

    capacity = check_capacity(config)

    budget = check_budget(config, costs)

    print("\nTOKEN ECONOMICS REPORT")
    print("=" * 35)

    print(f"Input tokens/day: {costs['input_tokens']:,}")
    print(f"Output tokens/day: {costs['output_tokens']:,}")
    print(f"Total tokens/day: {costs['total_tokens']:,}")

    print(f"Estimated daily cost: ${costs['daily_cost']:.2f}")
    print(f"Estimated monthly cost: ${costs['monthly_cost']:.2f}")

    print(f"Peak RPM with margin: {capacity['peak_rpm']:.0f}")
    print(f"Peak TPM with margin: {capacity['peak_tpm']:.0f}")

    print("\nCHECKS")
    print("=" * 35)

    print("RPM capacity:", "PASS" if capacity["rpm_status"] else "FAIL")
    print("TPM capacity:", "PASS" if capacity["tpm_status"] else "FAIL")
    print("Daily budget:", "PASS" if budget["daily_status"] else "FAIL")
    print("Monthly budget:", "PASS" if budget["monthly_status"] else "REVIEW")

    print("\nRecommendation: REVIEW assumptions, limits, or design before build.")


if __name__ == "__main__":
    main()
