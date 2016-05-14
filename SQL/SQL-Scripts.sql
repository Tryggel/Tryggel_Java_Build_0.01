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