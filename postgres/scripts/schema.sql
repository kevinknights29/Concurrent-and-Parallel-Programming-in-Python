--sql
CREATE TABLE IF NOT EXISTS prices(
    ticker VARCHAR(25) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    price_change VARCHAR(25),
    percentual_change VARCHAR(25),
    insertion_date TIMESTAMP NOT NULL DEFAULT NOW()
)
