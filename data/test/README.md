These are small scale data used for testing. Execute the following query in the SQL Terminal to get a copy of `climbing-log-outdoor.csv`: 

```sql
SELECT *
FROM boulders
WHERE date_ >= '2020-10-25'
  AND location_type = 'outdoor'
ORDER BY date_ ASC
;
```

