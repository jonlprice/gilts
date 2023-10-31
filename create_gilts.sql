

CREATE TABLE gilts (
	gilt_id bigserial PRIMARY KEY,
    close_of_business_date DATE NOT NULL,
    instrument_type VARCHAR ( 50 ) NOT NULL,
    maturity_bracket VARCHAR ( 50 ) NOT NULL,
    instrument_name VARCHAR ( 50 ) UNIQUE NOT NULL,
    isin_code VARCHAR ( 50 ) UNIQUE NOT NULL,
    ticker VARCHAR ( 20 ) UNIQUE NOT NULL,
    redemption_date DATE NOT NULL,
    first_issue_date DATE NOT NULL,
    dividend_dates VARCHAR ( 50 ) NOT NULL,
    current_ex_div_date DATE NOT NULL,
    total_amount_in_issue REAL NOT NULL,
    total_amount_including_il_uplift REAL NOT NULL,
    coupon REAL NOT NULL,
    days_to_redemption INTEGER NOT NULL,
    years_to_redemption REAL NOT NULL,
    clean_price  REAL NOT NULL,
    dirty_price REAL NOT NULL,
    tradeweb_yield REAL NOT NULL,
    calculated_yield REAL NOT NULL
);
