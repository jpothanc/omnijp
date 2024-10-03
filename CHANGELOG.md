# Changelog

## [2.16.0] - 2024-10-03
### Added
- Disk caching now returns nice json formatted results as shown below
```json
{
  "start_time": "2024-10-04 03:23:32.234",
  "end_time": "2024-10-04 03:23:32.590",
  "host_name": "LAPTOP-UMF83CB2",
  "total_tables_dumped": 3,
  "total_rows_dumped": 31,
  "tables": [
    {
      "name": "webcounter",
      "row_count": 1,
      "time_taken": "331.003 ms"
    },
    {
      "name": "equities",
      "row_count": 5,
      "time_taken": "344.998 ms"
    },
    {
      "name": "student",
      "row_count": 25,
      "time_taken": "352.999 ms"
    }
  ]
}

```

### Fixed
- Logging implementation now uses the standard logging module


