CREATE TABLE customer_orders (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  phone TEXT NOT NULL,
  order_id UUID REFERENCES orders(id) ON DELETE CASCADE,
  viewed BOOLEAN DEFAULT false,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_customer_orders_phone ON customer_orders(phone);
CREATE INDEX idx_customer_orders_order_id ON customer_orders(order_id);
