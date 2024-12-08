import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from unittest.mock import patch, MagicMock
from backend.stock import Stock, SumStrategy, AverageStrategy, CountStrategy

class TestStock(unittest.TestCase):

    def test_filter_data(self):
        data = [
            {"machine_id": 1, "product_name": "Product A", "quantity": 10, "quantity_category": "Low"},
            {"machine_id": 2, "product_name": "Product B", "quantity": 20, "quantity_category": "Medium"},
            {"machine_id": 1, "product_name": "Product C", "quantity": 30, "quantity_category": "High"},
            {"machine_id": 3, "product_name": "Product D", "quantity": 40, "quantity_category": "Low"}
        ]
        stock = Stock(data)

        # Test filtering by machine_id
        filtered_data = stock.filter_data(machine_id=1)
        self.assertEqual(len(filtered_data), 2)
        self.assertEqual(filtered_data[0]["machine_id"], 1)
        self.assertEqual(filtered_data[1]["machine_id"], 1)
        self.assertEqual(filtered_data[0]["product_name"], "Product A")
        self.assertEqual(filtered_data[1]["product_name"], "Product C")

        # Test filtering by product_name
        filtered_data = stock.filter_data(product_name="Product B")
        self.assertEqual(len(filtered_data), 1)
        self.assertEqual(filtered_data[0]["machine_id"], 2)
        self.assertEqual(filtered_data[0]["product_name"], "Product B")

        # Test filtering by quantity_category
        filtered_data = stock.filter_data(quantity_category="Low")
        self.assertEqual(len(filtered_data), 2)
        self.assertEqual(filtered_data[0]["machine_id"], 1)
        self.assertEqual(filtered_data[1]["machine_id"], 3)
        self.assertEqual(filtered_data[0]["product_name"], "Product A")
        self.assertEqual(filtered_data[1]["product_name"], "Product D")

    def test_aggregate(self):
        data = [
            {"machine_id": 1, "product_name": "Product A", "quantity": 10, "quantity_category": "Low", "location": "Location A"},
            {"machine_id": 2, "product_name": "Product B", "quantity": 20, "quantity_category": "Medium", "location": "Location B"},
            {"machine_id": 1, "product_name": "Product C", "quantity": 30, "quantity_category": "High", "location": "Location A"},
            {"machine_id": 3, "product_name": "Product D", "quantity": 40, "quantity_category": "Low", "location": "Location C"}
        ]
        stock = Stock(data)

        # Test aggregation with granularity "all" and strategy "sum"
        aggregated_data = stock.aggregate(granularity="all", strategy=SumStrategy())
        self.assertEqual(len(aggregated_data), 4)
        self.assertEqual(aggregated_data[0]["machine_id"], 1)
        self.assertEqual(aggregated_data[1]["machine_id"], 2)
        self.assertEqual(aggregated_data[2]["machine_id"], 1)
        self.assertEqual(aggregated_data[3]["machine_id"], 3)
        self.assertEqual(aggregated_data[0]["product_name"], "Product A")
        self.assertEqual(aggregated_data[1]["product_name"], "Product B")
        self.assertEqual(aggregated_data[2]["product_name"], "Product C")
        self.assertEqual(aggregated_data[3]["product_name"], "Product D")
        self.assertEqual(aggregated_data[0]["quantity"], 10)
        self.assertEqual(aggregated_data[1]["quantity"], 20)
        self.assertEqual(aggregated_data[2]["quantity"], 30)
        self.assertEqual(aggregated_data[3]["quantity"], 40)
        self.assertEqual(aggregated_data[0]["quantity_category"], "Low")
        self.assertEqual(aggregated_data[1]["quantity_category"], "Medium")
        self.assertEqual(aggregated_data[2]["quantity_category"], "High")
        self.assertEqual(aggregated_data[3]["quantity_category"], "Low")

        # Test aggregation with granularity "no_machine" and strategy "average"
        aggregated_data = stock.aggregate(granularity="no_machine", strategy=AverageStrategy())
        self.assertEqual(len(aggregated_data), 4)
        self.assertEqual(aggregated_data[0]["machine_id"], "Todos")
        self.assertEqual(aggregated_data[1]["machine_id"], "Todos")
        self.assertEqual(aggregated_data[2]["machine_id"], "Todos")
        self.assertEqual(aggregated_data[3]["machine_id"], "Todos")
        self.assertEqual(aggregated_data[0]["product_name"], "Product A")
        self.assertEqual(aggregated_data[1]["product_name"], "Product B")
        self.assertEqual(aggregated_data[2]["product_name"], "Product C")
        self.assertEqual(aggregated_data[3]["product_name"], "Product D")
        self.assertEqual(aggregated_data[0]["quantity"], 10)
        self.assertEqual(aggregated_data[1]["quantity"], 20)
        self.assertEqual(aggregated_data[2]["quantity"], 30)
        self.assertEqual(aggregated_data[3]["quantity"], 40)
        self.assertEqual(aggregated_data[0]["quantity_category"], "Low")
        self.assertEqual(aggregated_data[1]["quantity_category"], "Medium")
        self.assertEqual(aggregated_data[2]["quantity_category"], "High")
        self.assertEqual(aggregated_data[3]["quantity_category"], "Low")
        
        # Test aggregation with granularity "no_product" and strategy "count"
        aggregated_data = stock.aggregate(granularity="no_product", strategy=CountStrategy())
        self.assertEqual(len(aggregated_data), 3)
        self.assertEqual(aggregated_data[0]["machine_id"], 1)
        self.assertEqual(aggregated_data[1]["machine_id"], 2)
        self.assertEqual(aggregated_data[2]["machine_id"], 3)
        self.assertEqual(aggregated_data[0]["product_name"], "Todos")
        self.assertEqual(aggregated_data[1]["product_name"], "Todos")
        self.assertEqual(aggregated_data[2]["product_name"], "Todos")
        self.assertEqual(aggregated_data[0]["quantity"], 2)
        self.assertEqual(aggregated_data[1]["quantity"], 1)
        self.assertEqual(aggregated_data[2]["quantity"], 1)
        self.assertEqual(aggregated_data[0]["quantity_category"], "Low")
        self.assertEqual(aggregated_data[1]["quantity_category"], "Medium")
        self.assertEqual(aggregated_data[2]["quantity_category"], "Low")

if __name__ == '__main__':
    unittest.main()
