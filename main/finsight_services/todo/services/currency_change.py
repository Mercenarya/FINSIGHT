from massive import RESTClient

HTTPS = "https://api.massive.com/v3/reference/dividends?apiKey="
KEY = "dyFnozIdIS_LDrpXYUi5MxwrY4Pm_xan"
client = RESTClient(KEY)

aggs = []
for rate in client.list_aggs(
    "APPL",
    1,
    "minute",
    "2025-11-26",
    "2025-11-27",
    limit=1000,
): aggs.append(rate)
print(aggs)