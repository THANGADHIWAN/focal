-- Create product status enum
CREATE TYPE product_status_enum AS ENUM ('NOT_STARTED', 'IN_PROGRESS', 'COMPLETED');

-- Create product table
CREATE TABLE IF NOT EXISTS product (
    id SERIAL PRIMARY KEY,
    product_code VARCHAR(50) NOT NULL UNIQUE,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    status product_status_enum NOT NULL DEFAULT 'NOT_STARTED',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Add product_id foreign key to sample table
ALTER TABLE sample ADD COLUMN IF NOT EXISTS product_id INTEGER REFERENCES product(id);

-- Add product_id foreign key to test table  
ALTER TABLE test ADD COLUMN IF NOT EXISTS product_id INTEGER REFERENCES product(id);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_sample_product_id ON sample(product_id);
CREATE INDEX IF NOT EXISTS idx_test_product_id ON test(product_id);
CREATE INDEX IF NOT EXISTS idx_product_status ON product(status);
CREATE INDEX IF NOT EXISTS idx_product_created_at ON product(created_at);