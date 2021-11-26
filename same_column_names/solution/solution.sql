SELECT product.description, product_code.description
FROM product,
     product_code
WHERE product.product_code = prod_code;