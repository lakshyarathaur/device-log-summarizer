# PROMPT_LOG.md

## AI tools used

- ChatGPT: Generated the initial Python chart script and assisted with reviewing and improving it.
- Claude: Used for other project files, as applicable.

## 1. Initial prompt

Write a Python script that loads summary.json (a list of objects with keys device_id, total_records, avg_temperature, error_count) and generates a bar chart of average temperature per device using matplotlib. Save it as a PNG.

## 2. Flaw identified in the first attempt

The initial script included a chart title, axis labels, rotated x-axis labels, and PNG saving. However, it did not display the numerical average temperature above each bar or explicitly handle missing and empty JSON input with clear error messages. These are omissions identified during code review, not runtime errors observed during execution.

## 3. Follow-up prompt used to fix it

Please improve the existing Python chart script. Add numerical value labels above each bar, handle missing files, invalid JSON, and empty JSON lists with clear error messages, keep the chart title and axis labels, rotate the x-axis labels by 45 degrees, use tight_layout(), and save the chart as a PNG without relying on plt.show(). Keep the code simple and explain the changes.

## 4. Final result

- Script: plot_chart.py
- Output: avg_temperature.png
- Improvements: value labels above bars, input validation, clear error messages, rotated x-axis labels, chart title and axis labels, and PNG output.
