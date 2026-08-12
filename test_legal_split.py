import unittest
from unittest.mock import patch

from legal_split import assign_matter, bucket


class MatterDecisionTest(unittest.TestCase):
    def test_matter_is_stable_and_enters_the_follow_up_pipeline(self):
        matter = {"matter_id": "matter-001", "document": "signed-order"}
        with patch("legal_split.infrai.flags.get_value", return_value={"value": "treatment"}):
            first = assign_matter(matter)
            second = assign_matter(matter)
        self.assertEqual(bucket("matter-001"), bucket("matter-001"))
        self.assertEqual(first, second)
        self.assertEqual(first["treatment"], "treatment" if bucket("matter-001") < 50 else "control")
        self.assertEqual(first["signed_document_delivery"], "queued")
        self.assertEqual(first["deadline_follow_up"], "scheduled")


if __name__ == "__main__":
    unittest.main()

