-- Seed existing products from refinedaspect/lib/products.js
-- Run this AFTER supabase-schema.sql
-- Safe to re-run: uses ON CONFLICT DO NOTHING

INSERT INTO products (slug, name, price_ghs, price_usd, collection, colors, color_hex, description, care, sizes, sold_out, images, category, featured)
VALUES
  (
    'the-mark',
    'THE MARK',
    280, 22,
    'SF-01: ORIGIN',
    '["Bone White"]',
    '["#F5F3EF"]',
    'The foundation piece. Clean wordmark front, editorial illustration back. Dressed with intention.',
    '["Machine wash cold, gentle cycle","Do not bleach","Tumble dry low","Iron on low heat if needed","Do not dry clean"]',
    '["S","M","L","XL"]',
    '[]',
    '["/products/mark-front.jpg","/products/mark-back.jpg"]',
    'Tee',
    true
  ),
  (
    'the-origin',
    'THE ORIGIN',
    280, 22,
    'SF-01: ORIGIN',
    '["Void Black"]',
    '["#0A0A0A"]',
    'Rooted in coordinates. Meridian graphic front, barcode back. From here, everywhere.',
    '["Machine wash cold, gentle cycle","Do not bleach","Tumble dry low","Iron on low heat if needed","Do not dry clean"]',
    '["S","M","L","XL"]',
    '["S"]',
    '["/products/origin-front.jpg","/products/origin-back.jpg"]',
    'Tee',
    true
  ),
  (
    'the-statement',
    'THE STATEMENT',
    300, 24,
    'SF-01: ORIGIN',
    '["Dune Gold"]',
    '["#C8A96E"]',
    'The bold drop piece. Split vertical type front, editorial badge back. Limited.',
    '["Machine wash cold, gentle cycle","Do not bleach","Tumble dry low","Iron on low heat if needed","Do not dry clean"]',
    '["S","M","L","XL"]',
    '["XL"]',
    '["/products/statement-front.jpg","/products/statement-back.jpg"]',
    'Tee',
    true
  )
ON CONFLICT (slug) DO NOTHING;

-- Seed inventory (10 units per size, 0 for sold-out sizes)
-- ON CONFLICT DO NOTHING skips existing rows
INSERT INTO inventory (product_id, size, color, quantity)
SELECT p.id, s.size, p.colors->>0,
  CASE WHEN p.sold_out @> to_jsonb(s.size) THEN 0 ELSE 10 END
FROM products p
CROSS JOIN (VALUES ('S'), ('M'), ('L'), ('XL')) AS s(size)
ON CONFLICT (product_id, size, color) DO NOTHING;
