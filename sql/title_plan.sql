INSERT INTO cf20821_math.title_plan (
    id,
    spec_id,
    profile,
    date_uchsovet,
    number_uchsovet,
    current_year,
    date_enter,
    date_fgos,
    number_fgos,
    department_id,
    included,
    created_at,
    updated_at
)
SELECT 
    NULL as id,   
    s.id as spec_id,
    s.profile as profile,
    t.ДатаУтверСоветом as date_uchsovet,
    t.НомПротокСовета as number_uchsovet,
    LEFT(t.УчебныйГод, 4) as current_year,
    t.ГодНачалаПодготовки as date_enter,
    t.ДатаГОСа as date_fgos,
    NULL as number_fgos,
    
    CASE 
        WHEN t.КодПрофКафедры = 64 THEN 2
        WHEN t.КодПрофКафедры = 65 THEN 1
        ELSE t.КодПрофКафедры
    END as department_id,
    
    NULL as included,
    NULL as created_at,
    NULL as updated_at
    
FROM transfer.edu_plan t
INNER JOIN cf20821_math.speciality s ON s.cod = t.Специальность
WHERE t.КодФакультета = 37