from openpyxl import load_workbook
from pcip.utils.time import now_sgt_str


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

                "job_id": row[0],
                "company": row[1],
                "title": row[2],
                "score": row[5],
                "url": row[6],
                "status": row[9] or "",
                "applied_date": row[10] or "",
                "notes": row[11] or ""

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

text-align:left;

}}


.score {{

font-weight:bold;

}}


input, select {{

padding:8px;

margin-right:10px;

margin-bottom:15px;

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
{now_sgt_str()}
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


<input 
type="text"
id="search"
placeholder="Search Job ID / Company / Title"
onkeyup="filterTable()"
>


<select id="scoreFilter" onchange="filterTable()">

<option value="all">
All Scores
</option>

<option value="75">
>=75
</option>

<option value="85">
>=85
</option>

<option value="90">
>=90
</option>

</select>



<select id="statusFilter" onchange="filterTable()">

<option value="all">
All Status
</option>

<option value="To Review">
To Review
</option>

<option value="Applied">
Applied
</option>

<option value="Interview">
Interview
</option>

<option value="Rejected">
Rejected
</option>

<option value="Offer">
Offer
</option>

</select>



<table id="jobTable">


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
Pipeline Status
</th>

<th>
Applied Date
</th>

<th>
Notes
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
<br>
<small>{job['job_id']}</small>
</td>


<td>
{job['status']}
</td>


<td>
{job['applied_date']}
</td>


<td>
{job['notes']}
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


<script>


function filterTable() {


let search =
document.getElementById("search").value.toLowerCase();


let scoreFilter =
document.getElementById("scoreFilter").value;


let statusFilter =
document.getElementById("statusFilter").value;


let table =
document.getElementById("jobTable");


let rows =
table.getElementsByTagName("tr");



for (let i = 1; i < rows.length; i++) {


let row =
rows[i];


let text =
row.innerText.toLowerCase();


let score =
parseInt(row.cells[0].innerText);


let status =
row.cells[3].innerText;



let matchSearch =
text.includes(search);


let matchScore =
scoreFilter === "all"
||
score >= parseInt(scoreFilter);



let matchStatus =
statusFilter === "all"
||
status === statusFilter;



if (
matchSearch
&&
matchScore
&&
matchStatus
)

{

row.style.display="";

}

else

{

row.style.display="none";

}


}


}


</script>


</body>


</html>

"""


    with open(
        output_path,
        "w",
        encoding="utf-8"
    ) as f:

        f.write(html)
