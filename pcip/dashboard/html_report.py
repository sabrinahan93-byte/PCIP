from openpyxl import load_workbook
from datetime import datetime


def generate_html_dashboard(
    excel_path,
    output_path="docs/index.html"
):

    wb = load_workbook(
        excel_path,
        data_only=True
    )


    ws = wb["Jobs"]


    jobs = []


    for row in ws.iter_rows(
        min_row=2,
        values_only=True
    ):

        if row[0]:

            jobs.append({

                "company": row[1],
                "title": row[2],
                "location": row[3],
                "score": row[5],
                "url": row[6],
                "status": row[9]

            })


    jobs = sorted(
        jobs,
        key=lambda x: x["score"] or 0,
        reverse=True
    )


    high_match = [
        j for j in jobs
        if j["score"]
        and j["score"] >= 75
    ]



    html = f"""

<!DOCTYPE html>

<html>

<head>

<meta charset="UTF-8">

<title>
PCIP Job Dashboard
</title>


<style>

body {{

font-family: Arial;

margin:40px;

background:#f5f5f5;

}}


.card {{

background:white;

padding:20px;

margin-bottom:20px;

border-radius:10px;

}}


table {{

width:100%;

border-collapse:collapse;

}}


td,th {{

padding:10px;

border-bottom:1px solid #ddd;

}}


.score {{

font-weight:bold;

}}

</style>


</head>


<body>


<h1>
PCIP Daily Job Dashboard
</h1>


<div class="card">

<h2>
Summary
</h2>


<p>
Last Update:
{datetime.now()}
</p>


<p>
Total Jobs:
{len(jobs)}
</p>


<p>
High Match Jobs:
{len(high_match)}
</p>


</div>



<div class="card">


<h2>
Match Score >=75
</h2>


<table>


<tr>

<th>
Score
</th>

<th>
Company
</th>

<th>
Job Title
</th>

<th>
Location
</th>

<th>
Link
</th>


</tr>


"""


    for job in high_match:


        html += f"""

<tr>

<td class="score">

{job['score']}

</td>


<td>

{job['company']}

</td>


<td>

{job['title']}

</td>


<td>

{job['location']}

</td>


<td>

<a href="{job['url']}">

Open

</a>

</td>


</tr>

"""


    html += """

</table>


</div>


</body>


</html>

"""


    with open(
        output_path,
        "w",
        encoding="utf-8"
    ) as f:

        f.write(html)
