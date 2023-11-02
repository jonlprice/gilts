import io
import pandas as pd
import sys
import getopt
from datetime import datetime
import unicodedata
from pathlib import Path
import requests
import json
import re

class Gilt:
    def __init__(
        self,
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
    ):
        self.close_of_business_date = close_of_business_date
        self.instrument_type = instrument_type
        self.maturity_bracket = maturity_bracket
        self.instrument_name = instrument_name
        self.isin_code = isin_code
        self.redemption_date = datetime.fromisoformat(redemption_date)
        self.first_issue_date = first_issue_date
        self.dividend_dates = dividend_dates
        self.current_ex_div_date = current_ex_div_date
        self.total_amount_in_issue = total_amount_in_issue
        self.total_amount_including_il_uplift = total_amount_including_il_uplift
        self.coupon = self.calculate_coupon(self.instrument_name)
        self.days_to_redemption = self.calculate_days_to_redemtion(self.redemption_date)
        self.years_to_redemption = self.days_to_redemption / 365
        self.ticker = ""
        self.clean_price = 0
        self.dirty_price = 0
        self.tradeweb_yield = 0
        self.calculated_yield = 0

    def __str__(self) -> str:
        return f"{self.redemption_date.strftime('%b %d %Y')} \
                {self.instrument_name} {self.isin_code} | coupon {self.coupon} | days left \
                {divmod(self.days_to_redemption,365)} {self.clean_price:.2f} {self.dirty_price:.2f} \
                {self.tradeweb_yield:.2f} {self.calculated_yield:.2f}"

    def __repr__(self) -> str:
        return f"{self.redemption_date.strftime('%b %d %Y')} {self.instrument_name}"

    def __lt__(self, other):
        return self.coupon < other.coupon

    def calculate_coupon(self, instrument_name) -> float:
        """Calculate the coupon from the gilt name

        Gilts have the coupon embedded in the name so we need to extract it

        """

        coupon_text = instrument_name.split("%")
        coupon_text = coupon_text[0]

        if "/" in coupon_text:
            return self.coupon_convert_vulgar(coupon_text)
        else:
            return self.coupon_convert(coupon_text)

    def coupon_convert(self, text) -> float:
        """Convert the coupon string to a float

        Conver a string like 0¼% Index-linked Treasury Gilt 2052

        """

        coupon_chars = []

        coupon_integer = ""
        for char in text:
            if unicodedata.category(char) != "Nd":
                break
            coupon_integer = coupon_integer + char
        coupon_chars.append(int(coupon_integer))

        for char in text:
            match unicodedata.category(char):
                case "Nd":
                    pass

                case "No":
                    coupon_chars.append(unicodedata.numeric(char))

                case "Zs":
                    pass
        coupon = 0
        for coupon_chars in coupon_chars:
            coupon = coupon + coupon_chars
        return coupon

    def coupon_convert_vulgar(self, text) -> float:
        """Conver the coupon string to a float

        Convert a string like 0 1/8% Treasury Gilt 2028

        """

        c = text.split(" ")
        coupon_int = c[0]
        coupon_fraction = c[1]
        numerator, denominator = map(int, coupon_fraction.split("/"))
        coupon_fraction_float = numerator / denominator
        coupon = int(coupon_int) + coupon_fraction_float
        return coupon

    def calculate_days_to_redemtion(self, redemption_date) -> int:
        delta_date = redemption_date - datetime.now()
        return delta_date.days

    @staticmethod
    def calculate_yield(coupon, clean_price, years_to_redemption) -> float:
        """
        (C+ ((F-P)/n) ) / ( ((F+P) / 2) )

        C = Coupon/interest payment
        F = Face value
        P = Price
        n = Years to maturity_bracket
        """
        calculated_yield = (coupon + ((100 - clean_price) / years_to_redemption)) / (
            ((100 + clean_price) / 2)
        )
        calculated_yield = calculated_yield * 100
        return calculated_yield

    @staticmethod
    def lookup_ticker(isin):
        # Lookup url

        lseurl =f"https://api.londonstockexchange.com/api/gw/lse/search?worlds=issuers,quotes&q={isin}"

        x = requests.get(lseurl)
        data = json.loads(x.text)

        url = data['instruments'][0]['url']
        urlparts = re.split(r'/stock/', url)
        urlp = re.split(r'/', urlparts[1])

        print(f"Lookup {isin} -> {urlp[0]}")

        return urlp[0]


def main(argv):
    row = ""
    col = ""
    opts, args = getopt.getopt(argv, "hr:c:", ["row=", "col="])
    for opt, arg in opts:
        if opt == "-h":
            print("ex.py -r <row> -c <column>")
            sys.exit()
        elif opt in ("-r", "--row"):
            row = arg
        elif opt in ("-c", "--col"):
            col = arg
    print("row is ", row)
    print("col is ", col)

    with open("gilts.xml", "r") as f:
        xml = f.read()

    df = pd.read_xml(io.StringIO(xml))

    # computing number of rows
    rows = len(df.axes[0])

    # computing number of columns
    cols = len(df.axes[1])

    print(df)
    print("Number of Rows: ", rows)
    print("Number of Columns: ", cols)

    with open("Tradeweb_FTSE_ClosePrices.csv", "r") as f:
        csv = f.read()

    twdf = pd.read_csv(io.StringIO(csv))

    # computing number of rows
    rows = len(twdf.axes[0])

    # computing number of columns
    cols = len(twdf.axes[1])

    print(twdf)
    print("Tradeweb Number of Rows: ", rows)
    print("Tradeweb Number of Columns: ", cols)

    # data_top = list(df.columns)

    #   for col in df.columns:
    #       print(col.lower())

    gilt_list = []

    for ind in df.index:
        gilt_list.append(
            Gilt(
                df["CLOSE_OF_BUSINESS_DATE"][ind],
                df["INSTRUMENT_TYPE"][ind],
                df["MATURITY_BRACKET"][ind],
                df["INSTRUMENT_NAME"][ind],
                df["ISIN_CODE"][ind],
                df["REDEMPTION_DATE"][ind],
                df["FIRST_ISSUE_DATE"][ind],
                df["DIVIDEND_DATES"][ind],
                df["CURRENT_EX_DIV_DATE"][ind],
                df["TOTAL_AMOUNT_IN_ISSUE"][ind],
                df["TOTAL_AMOUNT_INCLUDING_IL_UPLIFT"][ind],
            )
        )

    gilt_list.sort()

    for g in gilt_list:
        result = twdf.loc[twdf["ISIN"] == g.isin_code]
        g.clean_price = result["Clean Price"].values[0]
        g.dirty_price = result["Dirty Price"].values[0]
        g.tradeweb_yield = result["Yield"].values[0]

        # (C+ ((F-P)/n) ) / ( ((F+P) / 2) )

        g.calculated_yield = Gilt.calculate_yield(
            g.coupon, g.clean_price, g.years_to_redemption
        )
        g.ticker = Gilt.lookup_ticker(g.isin_code)

    for g in gilt_list:
        print(g)

    data = [
        {
            "close_of_business_date": g.close_of_business_date,
            "instrument_type": g.instrument_type,
            "maturity_bracket": g.maturity_bracket,
            "instrument_name": g.instrument_name,
            "isin_code": g.isin_code,
            "ticker": g.ticker,
            "redemption_date": g.redemption_date,
            "first_issue_date": g.first_issue_date,
            "dividend_dates": g.dividend_dates,
            "current_ex_div_date": g.current_ex_div_date,
            "total_amount_in_issue": g.total_amount_in_issue,
            "total_amount_including_il_uplift": g.total_amount_including_il_uplift,
            "coupon": g.coupon,
            "days_to_redemption": g.days_to_redemption,
            "years_to_redemption": g.years_to_redemption,
            "clean_price": g.clean_price,
            "dirty_price": g.dirty_price,
            "tradeweb_yield": g.tradeweb_yield,
            "calculated_yield": g.calculated_yield,
        }
        for g in gilt_list
    ]

    print(data)

    newdf = pd.DataFrame(data)
    # computing number of rows
    rows = len(newdf.axes[0])

    # computing number of columns
    cols = len(newdf.axes[1])

    print("Out number of Rows: ", rows)
    print("Out number of Columns: ", cols)
    print("newdf")
    print(newdf.head())

    filepath = Path("./out.csv")
    newdf.to_csv(filepath, index=True)


if __name__ == "__main__":
    main(sys.argv[1:])
