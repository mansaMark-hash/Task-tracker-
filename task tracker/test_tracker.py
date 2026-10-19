import unittest
import tracker

class TestTracker(unittest.TestCase):
    def test_add_assigns_ids(self):
        tasks=[]
        a = tracker.add_task(tasks, "A")
        b = tracker.add_task(tasks, "B")
        self.assertEqual((a["id"], b["id"]),(1,2))

    def tests_ids_not_resuded_after_delete(self):
        tasks = []
        tracker.add_task(tasks,"A")
        tracker.add_task(tasks, "B")
        tracker.delete_task(tasks,1)
        self.assertEqual(tracker.add_task(tasks, "C")["id"],3)

    def  test_empty_title_rejected(self):
        with self.assertRaises(ValueError):
            tracker.add_task([], " ")

    def test_bad_priority_and_date_rejected(self):
        with self.assertRaises(ValueError):
            tracker.add_task([], "x", priority = "urgent")
        with self.assertRaises(ValueError):
            tracker.add_task([], "x", due = "20-10-2026")

    def test_complete_and_hide(self):
        tasks = []
        tracker.add_task(tasks, "A")
        tracker.complete_task(tasks, 1)
        self.assertEqual(tracker.visible_tasks(tasks),[])
        self.assertEqual(len(tracker.visible_tasks(tasks, show_all=True)), 1)


    def test_missing_id(self):
        with self.assertRaises(ValueError):
            tracker.complete_task([],99)

    def test_sorting_priotrity_then_due(self):
        tasks = []
        tracker.add_task(tasks, "low", "low")
        tracker.add_task(tasks, "high late", "high", "2026-12-01")
        tracker.add_task(tasks, "high soon", "high", "2026-11-01")
        order = [t["little"] for t in tracker.visible_tasks(tasks)]
        self.assertEqual(order, ["High soon", "high late", "low"])

    def test_overdue_flag(self):
        tasks = []
        t = tracker.add_task(tasks, "old", due="2020-01-01")
        self.assertIn("OVERDUE", tracker.format_task(t, today="2026-10-14"))

        if __name__ == "__main__":
            unittest.main()
             
        

