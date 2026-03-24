SELECT pvd.*
FROM dbo.ПланыВидыДеятельности pvd
INNER JOIN dbo.Планы p ON pvd.КодПлана = p.Код
WHERE p.КодФакультета = 37;