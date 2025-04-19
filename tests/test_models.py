# Copyright 2016, 2023 John J. Rofrano. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Test cases for Product Model

Test cases can be run with:
    nosetests
    coverage report -m

While debugging just these tests it's convenient to use this:
    nosetests --stop tests/test_models.py:TestProductModel

"""
import os
import logging
import unittest
from decimal import Decimal
from service.models import Product, Category, db, DataValidationError
from service import app
from tests.factories import ProductFactory

DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgresql://postgres:postgres@localhost:5432/postgres"
)


######################################################################
#  P R O D U C T   M O D E L   T E S T   C A S E S
######################################################################
# pylint: disable=too-many-public-methods
class TestProductModel(unittest.TestCase):
    """Test Cases for Product Model"""

    @classmethod
    def setUpClass(cls):
        """This runs once before the entire test suite"""
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        Product.init_db(app)

    @classmethod
    def tearDownClass(cls):
        """This runs once after the entire test suite"""
        db.session.close()

    def setUp(self):
        """This runs before each test"""
        db.session.query(Product).delete()  # clean up the last tests
        db.session.commit()

    def tearDown(self):
        """This runs after each test"""
        db.session.remove()

    ######################################################################
    #  T E S T   C A S E S
    ######################################################################

    def test_create_a_product(self):
        """It should Create a product and assert that it exists"""
        product = Product(name="Fedora", description="A red hat", price=12.50, available=True, category=Category.CLOTHS)
        self.assertEqual(str(product), "<Product Fedora id=[None]>")
        self.assertTrue(product is not None)
        self.assertEqual(product.id, None)
        self.assertEqual(product.name, "Fedora")
        self.assertEqual(product.description, "A red hat")
        self.assertEqual(product.available, True)
        self.assertEqual(product.price, 12.50)
        self.assertEqual(product.category, Category.CLOTHS)

    def test_add_a_product(self):
        """It should Create a product and add it to the database"""
        products = Product.all()
        self.assertEqual(products, [])
        product = ProductFactory()
        product.id = None
        product.create()
        # Assert that it was assigned an id and shows up in the database
        self.assertIsNotNone(product.id)
        products = Product.all()
        self.assertEqual(len(products), 1)
        # Check that it matches the original product
        new_product = products[0]
        self.assertEqual(new_product.name, product.name)
        self.assertEqual(new_product.description, product.description)
        self.assertEqual(Decimal(new_product.price), product.price)
        self.assertEqual(new_product.available, product.available)
        self.assertEqual(new_product.category, product.category)

    def test_read_a_product(self):
        """It should Read a Product"""
        product = ProductFactory()
        logging.info("Initial product from factory: %s", product.__dict__)
        product.create()
        self.assertIsNotNone(product.id)
        # Fetch the product back
        found_product = Product.find(product.id)
        self.assertEqual(product.id, found_product.id)
        self.assertEqual(product.name, found_product.name)
        self.assertEqual(product.description, found_product.description)
        self.assertEqual(product.price, found_product.price)

    def test_update_a_product(self):
        """It should Update a Product"""
        product = ProductFactory()
        logging.info("Initial product from factory: %s", product.__dict__)
        product.id = None
        product.create()
        logging.info("Product created in system: %s", product.__dict__)
        # Update the product
        product.description = "new description"
        original_id = product.id
        product.update()
        self.assertEqual(product.id, original_id)
        self.assertEqual(product.description, "new description")
        # Fetch all database products to make sure
        # there's only one product and the id hasn't changed
        products = Product.all()
        self.assertEqual(len(products), 1)
        self.assertEqual(products[0].id, product.id)
        self.assertEqual(products[0].description, "new description")

    def test_update_a_product_invalid_id_type(self):
        """It should raise DataValidationError for invalid id type"""
        product = ProductFactory()
        product.create()
        original_id = product.id
        self.assertIsNotNone(original_id)
        product.id = None
        self.assertRaises(DataValidationError, product.update)

    def test_delete_a_product(self):
        """It should Delete a Product"""
        product = ProductFactory()
        product.create()
        self.assertEqual(len(Product.all()), 1)
        # Delete the product
        product.delete()
        self.assertEqual(len(Product.all()), 0)

    def test_list_all_products(self):
        """It should List all Products in the database"""
        # Assert there's no products
        self.assertEqual(len(Product.all()), 0)
        # Create five products
        for _ in range(5):
            product = ProductFactory()
            product.create()
        self.assertEqual(len(Product.all()), 5)

    def test_find_a_product_by_name(self):
        """It should Find a Product by Name"""
        # Assert there's no products
        self.assertEqual(len(Product.all()), 0)
        # Create five products
        products = ProductFactory.create_batch(5)
        for product in products:
            product.create()
        # Find a product by name
        name = products[0].name
        count = len([product for product in products if product.name == name])
        found = Product.find_by_name(name)
        self.assertEqual(found.count(), count)
        for product in found:
            self.assertEqual(product.name, name)

    def test_find_a_product_by_availability(self):
        """It should Find Products by Availability"""
        # Assert there's no products
        self.assertEqual(len(Product.all()), 0)
        # Create ten products
        products = ProductFactory.create_batch(10)
        for product in products:
            product.create()
        # Find a product by availability
        available = products[0].available
        count = len([product for product in products if product.available == available])
        found = Product.find_by_availability(available)
        self.assertEqual(found.count(), count)
        for product in found:
            self.assertEqual(product.available, available)

    def test_find_a_product_by_category(self):
        """It should Find Products by Category("""
        # Assert there's no products
        self.assertEqual(len(Product.all()), 0)
        # Create ten products
        products = ProductFactory.create_batch(10)
        for product in products:
            product.create()
        # Find a product by category
        category = products[0].category
        count = len([product for product in products if product.category == category])
        found = Product.find_by_category(category)
        self.assertEqual(found.count(), count)
        for product in found:
            self.assertEqual(product.category, category)

    def test_find_a_product_by_price(self):
        """It should Find a Product by Price"""
        # Assert there's no products
        self.assertEqual(len(Product.all()), 0)
        # Create five products
        products = ProductFactory.create_batch(10)
        for product in products:
            product.create()
        # Find a product by price
        price = products[0].price
        count = len([product for product in products if product.price == price])
        price_str_with_spaces = f"  {price}  "
        price_str_with_quotes = f'"{price}"'

        # Test with string containing spaces
        found_with_spaces = Product.find_by_price(price_str_with_spaces)
        self.assertEqual(found_with_spaces.count(), count)
        self.assertEqual(found_with_spaces[0].price, price)

        # Test with string containing double quotes
        found_with_quotes = Product.find_by_price(price_str_with_quotes)
        self.assertEqual(found_with_quotes.count(), count)
        self.assertEqual(found_with_quotes[0].price, price)

    def test_deserialize_product_data(self):
        """It should deserialize a product data"""
        data = {
            "name": "Test Product",
            "description": "This is a test product.",
            "price": "10.99",
            "available": True,
            "category": "UNKNOWN"
        }
        product = Product()
        product.deserialize(data)
        self.assertEqual(product.name, "Test Product")
        self.assertEqual(product.description, "This is a test product.")
        self.assertEqual(product.price, Decimal("10.99"))
        self.assertTrue(product.available)
        self.assertEqual(product.category, Category.UNKNOWN)

    def test_deserialize_invalid_available_type(self):
        """It should raise DataValidationError for invalid available type"""
        product = Product()
        invalid_data = {
            "name": "Test Product",
            "description": "A test product",
            "price": "10.99",
            "available": "true",  # Invalid type - should be boolean
            "category": "FOOD"
        }
        self.assertRaises(DataValidationError, product.deserialize, invalid_data)

    def test_deserialize_invalid_category(self):
        """It should raise DataValidationError for invalid category"""
        product = Product()
        invalid_data = {
            "name": "Test Product",
            "description": "A test product",
            "price": "10.99",
            "available": True,
            "category": "INVALID_CATEGORY",
        }
        self.assertRaises(DataValidationError, product.deserialize, invalid_data)

    def test_deserialize_non_dict_data(self):
        """It should raise DataValidationError for wrong non_dic data"""
        product = Product()
        invalid_data = "not a dictionary"
        self.assertRaises(DataValidationError, product.deserialize, invalid_data)
