SELECT ph.*
FROM dbo.ПланыЧасы ph
INNER JOIN dbo.ПланыСтроки ps ON ph.КодСтроки = ps.Код
INNER JOIN dbo.Планы p ON ps.КодПлана = p.Код
WHERE p.КодФакультета = 37