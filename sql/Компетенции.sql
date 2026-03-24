SELECT DISTINCT c.*
FROM dbo.Компетенции c
INNER JOIN dbo.ПланыСтроки ps ON c.КодООП = ps.КодООП  
INNER JOIN dbo.Планы p ON ps.КодПлана = p.Код
WHERE p.КодФакультета = 37 -- код факультета математики и компьтерных наук