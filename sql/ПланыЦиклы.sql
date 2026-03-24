SELECT pc.*
FROM dbo.ПланыЦиклы pc
INNER JOIN dbo.Планы p ON pc.КодПлана = p.Код
WHERE p.КодФакультета = 37;