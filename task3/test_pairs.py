import pytest
from pyspark.sql import SparkSession

from pyspark_pairs import product_category_pairs

@pytest.fixture(scope="session")
def spark():
    spark = (
        SparkSession.builder
        .master("local[2]")
        .appName("pairs_tests")
        .getOrCreate()
    )
    yield spark
    spark.stop()

def to_set(rows):
    return {(r["product_name"], r["category_name"]) for r in rows}

def test_basic_pairs(spark):
    products = spark.createDataFrame([
        {"id": 1, "name": "Phone"},
        {"id": 2, "name": "Laptop"},
        {"id": 3, "name": "Chair"},
        {"id": 4, "name": "Table"},   
    ])

    categories = spark.createDataFrame([
        {"id": 10, "name": "Electronics"},
        {"id": 11, "name": "Furniture"},
        {"id": 12, "name": "Portable"},  
    ])

    product_categories = spark.createDataFrame([
        {"product_id": 1, "category_id": 10},
        {"product_id": 1, "category_id": 12},  
        {"product_id": 2, "category_id": 10},
        {"product_id": 3, "category_id": 11},
    ])

    df = product_category_pairs(products, categories, product_categories)
    rows = df.collect()

    expected = {
        ("Phone",  "Electronics"),
        ("Phone",  "Portable"),
        ("Laptop", "Electronics"),
        ("Chair",  "Furniture"),
        ("Table",  None),
    }
    assert to_set(rows) == expected

def test_duplicates_removed(spark):
    products = spark.createDataFrame([
        {"id": 1, "name": "Phone"},
    ])
    categories = spark.createDataFrame([
        {"id": 10, "name": "Electronics"},
    ])
    product_categories = spark.createDataFrame([
        {"product_id": 1, "category_id": 10},
        {"product_id": 1, "category_id": 10},
    ])

    df = product_category_pairs(products, categories, product_categories)
    rows = df.collect()
    assert len(rows) == 1
    assert rows[0]["product_name"] == "Phone"
    assert rows[0]["category_name"] == "Electronics"

def test_all_without_categories(spark):
    products = spark.createDataFrame([
        {"id": 1, "name": "A"},
        {"id": 2, "name": "B"},
    ])
    categories = spark.createDataFrame([
        {"id": 10, "name": "X"},
    ])
    product_categories = spark.createDataFrame([], schema="product_id INT, category_id INT")

    df = product_category_pairs(products, categories, product_categories)
    rows = df.collect()
    assert to_set(rows) == {("A", None), ("B", None)}
