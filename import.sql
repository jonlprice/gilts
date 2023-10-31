COPY gilts(
    close_of_business_date,
    instrument_type,
    maturity_bracket,
    instrument_name,
    isin_code,
    redemption_date,
    first_issue_date,
    dividend_dates,
    current_ex_div_date,
    total_amount_in_issue,
    total_amount_including_il_uplift,
    coupon,
    days_to_redemption,
    years_to_redemption,
    clean_price,
    dirty_price,
    tradeweb_yield,
    calculated_yield)
FROM '/Users/jonprice/projects/pythonvenv/gilts/out.csv'
DELIMITER ','
CSV HEADER;
