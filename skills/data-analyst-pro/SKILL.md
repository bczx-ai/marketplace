---
name: data-analyst-pro
displayName: "Data Analyst"
description: "完成用户委托的数据分析任务。若代码需操作文件，请确保文件列在`upload_files`参数中。"
version: 0.1.0
tags:
  - data_analysis
license: "Unknown"
---

# Data Analyst

## Overview

This skill provides specialized capabilities for data analyst.

## Instructions

Complete the data analysis tasks delegated by the user.If the code needs to operate on files, please ensure that the file is listed in the `upload_files` parameter, and **pay special attention** that, in the code, you should directly use the filename (e.g., `open('data.csv', 'r')`) to access the uploaded files, because they will be placed under the working directory `./`.


## Usage Notes

- This skill is based on the data_analyst agent configuration
- Template variables (if any) like $DATE$, $SESSION_GROUP_ID$ may require runtime substitution
- Follow the instructions and guidelines provided in the content above
