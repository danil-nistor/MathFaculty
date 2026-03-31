SELECT pps.*
FROM dbo.ПланыПрофСтандарты pps
INNER JOIN dbo.Планы p ON pps.КодПлана = p.Код
WHERE p.КодФакультета = 37;