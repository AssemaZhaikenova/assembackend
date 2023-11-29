from django.test import TestCase
from app3.models import Product, Category, Order


class ProductTestCase(TestCase):
    def setUp(self):
        Product.objects.create(name="Test Product", price=100)

    def test_product_price(self):
        product = Product.objects.get(name="Test Product")
        self.assertEqual(product.price, -1)

    def test_product_name_length(self):
        product = Product.objects.get(name="Test Product")
        max_length = product._meta.get_field('name').max_length
        self.assertLessEqual(len(product.name), max_length)

    def test_product_addition(self):
        initial_count = Product.objects.count()
        Product.objects.create(name="New Product", price=150)
        new_count = Product.objects.count()
        self.assertEqual(new_count, initial_count + 1)


class CategoryTestCase(TestCase):
    def setUp(self):
        Category.objects.create(name="Test Category")

    def test_category_name(self):
        category = Category.objects.get(name="Test Category")
        self.assertEqual(category.name, "Test Category")

    def test_category_name_unique(self):
        with self.assertRaises(Exception):
            Category.objects.create(name="Test Category")

    def test_category_str_representation(self):
        category = Category.objects.get(name="Test Category")
        self.assertEqual(str(category), "Test Category")


class OrderTestCase(TestCase):
    def setUp(self):
        product = Product.objects.create(name="Test Product", price=100)
        category = Category.objects.create(name="Test Category")
        order = Order.objects.create(customer_name="Test Customer")
        order.products.add(product)
        order.save()

    def test_order_customer_name(self):
        order = Order.objects.get(customer_name="Test Customer")
        self.assertEqual(order.customer_name, "Test Customer")

    def test_order_products(self):
        order = Order.objects.get(customer_name="Test Customer")
        self.assertEqual(order.products.count(), 1)

    def test_order_str_representation(self):
        order = Order.objects.get(customer_name="Test Customer")
        self.assertEqual(
            str(order),
            f"Order #{order.id} - {order.customer_name}"
        )
