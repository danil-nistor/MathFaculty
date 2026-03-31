SELECT DISTINCT pss.*
FROM [dbo].[псСтандарты] pss
inner join dbo.ПланыПрофСтандарты pps on pss.КодГруппы = pps.КодГруппыПС
inner join dbo.Планы p on pps.КодПлана = p.Код
where p.КодФакультета = 37;



-- псСтандарты -> ПланыПрофСтандарты -> Планы