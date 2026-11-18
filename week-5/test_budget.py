
import unittest

from budget import get_config, calculate_costs, check_capacity, check_budget


class TestFeatureBudget(unittest.TestCase):

    def setUp(self):
        self.config = get_config()
        self.costs = calculate_costs(self.config)

    def test_config_values(self):
        self.assertGreater(self.config["input_price"], 0)
        self.assertGreater(self.config["output_price"], 0)

    def test_cost_estimate(self):
        self.assertGreater(self.costs["daily_cost"], 0)
        self.assertGreater(self.costs["monthly_cost"], 0)

    def test_monthly_budget_fails(self):
        result = check_budget(self.config, self.costs)
        self.assertFalse(result["monthly_status"])

    def test_rpm_limit_fails(self):
        config = self.config.copy()
        config["rpm_limit"] = 10

        result = check_capacity(config)
        self.assertFalse(result["rpm_status"])


if __name__ == "__main__":
    unittest.main()
