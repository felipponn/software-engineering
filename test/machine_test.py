import unittest
from src.machine import Machine

class TestMachine(unittest.TestCase):
    def setUp(self):
        """
        Setup method to create machine objects for testing.
        """
        self.machine1 = Machine(
            machine_id=1,
            location="Café do Prédio Principal",
            products=["Café", "Chá", "Biscoitos"],
            status=True,
            last_serviced_at="2024-10-15 10:00:00",
            installed_at="2021-09-01 12:00:00"
        )
        self.machine2 = Machine(
            machine_id=2,
            location="Biblioteca",
            products=["Água", "Suco", "Salgados"],
            status=False,
            last_serviced_at="2024-10-01 15:30:00",
            installed_at="2022-12-01 18:40:00"
        )
        self.machines = [self.machine1, self.machine2]
        
    def test_machine_creation(self):
        """
        Test the creation of machine objects.
        """
        self.assertEqual(self.machine1.machine_id, 1)
        self.assertEqual(self.machine1.location, "Café do Prédio Principal")
        self.assertEqual(self.machine1.products, ["Café", "Chá", "Biscoitos"])
        self.assertTrue(self.machine1.status)
        self.assertEqual(self.machine1.last_serviced_at, "2024-10-15 10:00:00")
        self.assertEqual(self.machine1.installed_at, "2021-09-01 12:00:00")
        
        self.assertEqual(self.machine2.machine_id, 2)
        self.assertEqual(self.machine2.location, "Biblioteca")
        self.assertEqual(self.machine2.products, ["Água", "Suco", "Salgados"])
        self.assertFalse(self.machine2.status)
        self.assertEqual(self.machine2.last_serviced_at, "2024-10-01 15:30:00")
        self.assertEqual(self.machine2.installed_at, "2022-12-01 18:40:00")
        
    def test_get_machines(self):
        """
        Test if the get_machines method returns a list of machine ids.
        """
        machines = Machine.get_machines(self.machines)
        self.assertIsInstance(machines, list)
        self.assertEqual(machines, [1, 2])
        self.assertEqual(len(machines), 2)
        
if __name__ == '__main__':
    unittest.main()