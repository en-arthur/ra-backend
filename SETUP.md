# Supabase Setup Guide

## 1. Create Supabase Project
1. Go to https://supabase.com and create a new project
2. Note your **Project URL** and **API keys** (Settings → API)

## 2. Run SQL Files (in order)
Go to Supabase Dashboard → SQL Editor and run each file:

1. `supabase-schema.sql` — creates tables, RLS policies, indexes
2. `storage.sql` — creates product-images storage bucket
3. `seed.sql` — migrates existing products + inventory
4. `admin-role.sql` — sets up admin JWT role (update email first!)

## 3. Set Admin Role
In `admin-role.sql`, replace `your-admin@email.com` with your email, then:
1. Sign up at your admin app first (so the user exists in auth.users)
2. Run the UPDATE query to assign the admin role
3. Register the `custom_access_token_hook` in:
   Dashboard → Authentication → Hooks → Custom Access Token Hook

## 4. Environment Variables
Copy these into both apps:

**admin/.env.local** and **refinedaspect/.env.local**:
```
NEXT_PUBLIC_SUPABASE_URL=https://your-project.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-anon-key
```

**admin/.env.local only** (never in storefront):
```
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key
```

## 5. Upload Product Images
Upload your product images to the `product-images` bucket in:
Dashboard → Storage → product-images

Keep the same paths used in seed.sql:
- `products/mark-front.jpg`
- `products/mark-back.jpg`
- etc.

Then update the image URLs in the products table to use the full Supabase Storage URL:
`https://your-project.supabase.co/storage/v1/object/public/product-images/products/mark-front.jpg`
