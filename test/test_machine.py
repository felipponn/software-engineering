import unittest
from ..src.machine import Machine
from ..utils.connect_db import execute_query  # Certifique-se de que está importando corretamente as funções de conexão

class TestMachine(unittest.TestCase):
    def setUp(self):
        """
        Setup method to create machine objects for testing and prepare the database.
        """
        # Cria máquinas fictícias
        self.machine1 = Machine(
            machine_id=None,  # O ID será atribuído ao salvar no banco
            location="Café do Prédio Principal",
            status="operational",
            last_serviced_at='2024-09-01',
            installed_at= '2023-01-15'
        )
        self.machine2 = Machine(
            machine_id=None,  # O ID será atribuído ao salvar no banco
            location="Biblioteca",
            status="under maintenance",
            last_serviced_at='2024-10-01',
            installed_at='2022-07-20'
        )

        # Insere os dados no banco de dados antes de cada teste
        self.machine1.save_db()
        self.machine2.save_db()

    def tearDown(self):
        """
        Cleanup method to remove test data from the database after each test.
        """
        # Remove as máquinas do banco após os testes
        query = "DELETE FROM Machines WHERE location IN ('Café do Prédio Principal', 'Biblioteca');"
        execute_query(query)

    def test_machine_creation(self):
        """
        Test the creation and saving of machine objects to the database.
        """
        # Verifica se os dados da máquina foram corretamente atribuídos
        self.assertEqual(self.machine1.location, "Café do Prédio Principal")
        self.assertTrue(self.machine1.status)
        self.assertEqual(self.machine1.last_serviced_at, '2024-09-01')
        self.assertEqual(self.machine1.installed_at, '2023-01-15')

        self.assertEqual(self.machine2.location, "Biblioteca")
        self.assertFalse(self.machine2.status)
        self.assertEqual(self.machine2.last_serviced_at, '2024-10-01')
        self.assertEqual(self.machine2.installed_at, '2022-07-20')

    def test_get_machines_from_db(self):
        """
        Test the retrieval of machines from the database.
        """
        machines = Machine.get_machines()
        self.assertIsInstance(machines, list)
        self.assertGreaterEqual(len(machines), 2)  # Verifica se pelo menos as 2 máquinas de teste estão presentes

        # Verifica as propriedades da primeira máquina
        machine1_db = next(m for m in machines if m.location == "Café do Prédio Principal")
        self.assertEqual(machine1_db.location, self.machine1.location)
        self.assertTrue(machine1_db.status)

        # Verifica as propriedades da segunda máquina
        machine2_db = next(m for m in machines if m.location == "Biblioteca")
        self.assertEqual(machine2_db.location, self.machine2.location)
        self.assertFalse(machine2_db.status)
        
if __name__ == '__main__':
    unittest.main()
