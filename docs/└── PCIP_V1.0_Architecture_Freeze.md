# PCIP V1.0 Architecture Freeze

## Job Dashboard Data Model & System Design Decision

Version: V1.0  
Status: Frozen  
Date: 2026-08-02
Design Principles
Principle 1

Database 与 Notification 分离
Database
    ↓
Change Detection
    ↓
Run Detail
    ↓
Notification
Principle 2

系统字段与人工字段隔离。

System Fields:

程序维护。

Manual Fields:

用户维护。

程序不得覆盖。
Principle 3

配置驱动。

规则放：

config/

代码不写死。
3. Excel Architecture

文件名：

Job_Dashboard.xlsx

固定。
Sheet 1: Jobs

字段冻结：

Field
Job ID
Company
Job Title
Location
Work Mode
Match Score
Job URL
Last Seen
Last Notified
Pipeline Status
Applied Date
Notes
ob ID Rule

格式：

JOB-YYYYMMDD-0001

Example:

JOB-20260802-0001

规则：

日期 = PCIP首次发现日期
序列号 = 当日新增岗位顺序
一旦生成永久不变
Manual Fields

以下字段：

用户维护：

Pipeline Status
Applied Date
Notes
程序禁止修改。
Sheet 2: Companies

字段：

Company
Enabled
Tier
Career URL
Last Scan
Scan Status
Notes
Sheet 3: Run_Log

字段：

Run Time
Companies Scanned
New Jobs
Updated Jobs
Closed Jobs
Failed Companies
Duration
Result
Sheet 4: Run_Detail

字段：

Run Time
Change Type
Company
Job Title
Match Score
Job URL

Change Type:

NEW
UPDATED
CLOSED
REOPENED
4. Job Lifecycle

记录：

New Job Found

↓

Generate Job ID

↓

Write Jobs Sheet

↓

Evaluate Match Score

↓

Generate Run_Detail

↓

Notify if Required

↓

Future Scan

    Existing
        ↓
    Update Last Seen

    Changed
        ↓
    UPDATED

    Missing
        ↓
    CLOSED
    5. Development Rules

后续代码必须遵守：

不改变 Excel Schema
不覆盖人工字段
不重复通知
不硬编码规则
所有规则进入 config
