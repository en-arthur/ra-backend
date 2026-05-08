-- Storage bucket for product images
-- FastAPI uploads directly to Supabase Storage using the service role key,
-- so no RLS policies are needed here.

INSERT INTO storage.buckets (id, name, public)
VALUES ('product-images', 'product-images', true)
ON CONFLICT (id) DO NOTHING;
