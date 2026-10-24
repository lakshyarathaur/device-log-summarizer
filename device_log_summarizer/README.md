Device Log Summarizer

A small command-line project that cleans sensor data, summarizes device telemetry from a CSV file, and plots the results. It was built for the Software Engineering Intern technical assessment and is split into three parts.

What's in the folder
File	What it does
sanitize.py	Section 1. Cleans a list of mixed sensor readings and includes a few unit tests.
summarize.py	Section 2. Reads the CSV, groups by device, and saves a JSON summary.
plot_chart.py	Section 3. Draws a bar chart of average temperature per device.
device_telemetry.csv	Sample input data.
summary.json	Sample output from summarize.py.
avg_temperature.png	Sample chart from plot_chart.py.
PROMPT_LOG.md	Notes on how I used AI tools.
How to run it

You need Python 3 and, for the chart only, matplotlib (pip install matplotlib). Run these from inside the project folder:

python -m unittest sanitize.py -v
python summarize.py
python plot_chart.py

Run summarize.py before plot_chart.py, since the chart reads the summary.json file it creates.

summarize.py also takes options if you want to use a different file or threshold:

python summarize.py --input my_data.csv --output my_summary.json --max-avg-temp 75
How each part works

Section 1: cleaning readings. clean_readings() tries to turn every item into a float. It drops None, text that isn't a number, NaN values and negatives, then caps anything over 500.0 at 500.0. An empty list, a list of only bad values, or None just returns an empty list instead of crashing.

Section 2: summarizing the CSV. For each device the script counts the records, averages the temperature and counts how many have the status ERROR. Devices whose average is above 80.0 are left out. The results are saved to summary.json and printed as a table in the terminal.

Section 3: charting. The script loads summary.json and saves a bar chart with a title, axis labels, value labels on the bars, and a dashed line at the 80.0 threshold.

Handling bad input
Rows with a missing device ID or a temperature that isn't a number are skipped, and the script prints how many it skipped.
A missing file, an empty CSV, or missing columns gives a clear error message instead of a traceback.
The chart script does the same if summary.json is missing, broken or empty.
Sample data

The sample CSV has a few deliberately broken rows to test the error handling. DEV_B is removed from the results because its average temperature (about 91) is above 80.