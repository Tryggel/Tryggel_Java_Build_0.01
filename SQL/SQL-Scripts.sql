
--Select last different tokens with different pod_ids from table mess_all.koll_token
--http://stackoverflow.com/questions/7306082/mysql-using-group-by-and-desc
SELECT refresh_token, pod_id, ID FROM mess_all.koll_token t
WHERE ID = (SELECT max(ID) FROM mess_all.koll_token WHERE t.pod_id = pod_id)

--Same solution, but should be not so effitient.
SELECT refresh_token, pod_id, ID FROM (SELECT * FROM mess_all.koll_token ORDER BY ID DESC) AS t GROUP BY pod_id


SELECT koll_all.datetime, LEAST(koll_all.w,1) FROM mess_all.koll_all
WHERE (koll_all.SensorID = 341933 OR koll_all.SensorID = 341932) AND datetime > "2016-05-01 00:00:00" 



SELECT koll_all.datetime, LEAST(koll_all.w,1) FROM mess_all.koll_all
WHERE koll_all.SensorID = 341933  AND datetime > "2016-05-05 20:00:00" and koll_all.w > 0
GROUP BY 
day(datetime),
HOUR(datetime),
minute(datetime),
round(second(datetime)/60)



SELECT koll_all.datetime, LEAST(koll_all.w,1) FROM mess_all.koll_all
WHERE koll_all.SensorID = 101177  AND koll_all.datetime >= ( CURDATE() - INTERVAL 2 DAY )
GROUP BY 
day(datetime),
HOUR(datetime),
minute(datetime),
round(second(datetime)/60)

SELECT idnew_table, new_tablecol FROM mess_all.neurio_1
WHERE id = 101177  AND idnew_table >= ( CURDATE() - INTERVAL 90 DAY ) and new_tablecol >0
GROUP BY 
day(datetime),
HOUR(datetime),
minute(datetime),
round(second(datetime)/60)

round(HOUR(datetime)/4)

HOUR(idnew_table),
minute(idnew_table),
round(second(idnew_table)/60)

SELECT * FROM mess_all.fibaro
WHERE SensorID = 103 and datetime > "2016-06-20 00:00:00" 


SELECT refresh_token FROM mess_all.koll_token
where pod_id=9078
GROUP by pod_id
ORDER BY ID DESC
LIMIT 1

