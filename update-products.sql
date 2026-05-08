-- Update existing products: new prices, collection name, sizes (M/L/XL only)
UPDATE products SET
  price_ghs = 320,
  collection = 'RA-01: ORIGIN',
  sizes = '["M","L","XL"]',
  sold_out = '[]'
WHERE slug = 'the-mark';

UPDATE products SET
  price_ghs = 320,
  collection = 'RA-01: ORIGIN',
  sizes = '["M","L","XL"]',
  sold_out = '[]'
WHERE slug = 'the-origin';

UPDATE products SET
  price_ghs = 360,
  price_usd = 24,
  collection = 'RA-01: ORIGIN',
  sizes = '["M","L","XL"]',
  sold_out = '[]'
WHERE slug = 'the-statement';

-- Remove S inventory rows, keep only M/L/XL
DELETE FROM inventory WHERE size = 'S';
DELETE FROM inventory WHERE size = 'XXL';

-- Add any missing M/L/XL rows
INSERT INTO inventory (product_id, size, color, quantity)
SELECT p.id, s.size, p.colors->>0, 10
FROM products p
CROSS JOIN (VALUES ('M'), ('L'), ('XL')) AS s(size)
ON CONFLICT (product_id, size, color) DO NOTHING;
