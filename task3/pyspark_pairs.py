from pyspark.sql import DataFrame, functions as F

def product_category_pairs(
    products: DataFrame,
    categories: DataFrame,
    product_categories: DataFrame,
) -> DataFrame:
    """
    Вернёт датафрейм с колонками:
    product_name и category_name 

    Ожидаемые входные датафреймы:
    products: id, name
    categories: id, name
    product_categories: product_id, category_id
    """
    p = products.select(
        F.col("id").alias("product_id"),
        F.col("name").alias("product_name")
    )

    c = categories.select(
        F.col("id").alias("category_id"),
        F.col("name").alias("category_name")
    )

    pc = product_categories.select("product_id", "category_id")

    result = (
        p.join(pc, on="product_id", how="left")
         .join(c, on="category_id", how="left")
         .select("product_name", "category_name")
    )
    result = result.dropDuplicates()

    return result
