SELECT ps.*
FROM dbo.ПланыСтроки ps
INNER JOIN dbo.Планы p ON ps.КодПлана = p.Код
WHERE p.КодФакультета = 37