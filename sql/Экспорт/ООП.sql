SELECT oop.[Код]
      ,[КодРодительскогоООП]
      ,[Название]
  FROM [Деканат].[dbo].[ООП] oop
  inner join dbo.Планы pl on oop.Код = pl.КодАктивногоООП
WHERE 
	pl.КодФакультета = 37
	AND oop.[КодРодительскогоООП] IS NOT NULL