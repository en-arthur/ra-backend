-- Fix product image URLs to use Supabase Storage
-- Replace YOUR_PROJECT_REF with your actual Supabase project ref (phhkhqkpdddxyqcoxkrq)

UPDATE products SET images = '[
  "https://phhkhqkpdddxyqcoxkrq.supabase.co/storage/v1/object/public/product-images/products/mark-front.jpg",
  "https://phhkhqkpdddxyqcoxkrq.supabase.co/storage/v1/object/public/product-images/products/mark-back.jpg"
]' WHERE slug = 'the-mark';

UPDATE products SET images = '[
  "https://phhkhqkpdddxyqcoxkrq.supabase.co/storage/v1/object/public/product-images/products/origin-front.jpg",
  "https://phhkhqkpdddxyqcoxkrq.supabase.co/storage/v1/object/public/product-images/products/origin-back.jpg"
]' WHERE slug = 'the-origin';

UPDATE products SET images = '[
  "https://phhkhqkpdddxyqcoxkrq.supabase.co/storage/v1/object/public/product-images/products/statement-front.jpg",
  "https://phhkhqkpdddxyqcoxkrq.supabase.co/storage/v1/object/public/product-images/products/statement-back.jpg"
]' WHERE slug = 'the-statement';
