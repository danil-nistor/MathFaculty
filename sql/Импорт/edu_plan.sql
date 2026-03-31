CREATE TEMPORARY  TABLE code_block_map (
    code_index varchar(15),
    block_id bigint
);

INSERT INTO code_block_map(
    ('Б1.О', 1),
    ('Б1.В', 2),
    ('Б2.О', 3),
    ('Б2.В', 4),
    ('Б3', 13),
    ('ФТД', 11);
)

insert into cf20821_math.edu_plan (
    id,
    block_id,
    subject_id,
    code_subject,
    department_id,
    title_plan_id,
    created_at,
    updated_at
)
SELECT(
    NULL as id,
    m.bloc_id as block_id,
    s.id as subject_id,
    edstr.ДисциплинаКод as code_subject,
    
    CASE 
        WHEN edstr.КодКафедры = 64 THEN 2
        WHEN edstr.КодКафедры = 65 THEN 1
        ELSE edstr.КодКафедры 
        -- Есть дргуие каедры но для них я не составил соотвествие. 
        -- Не все кафедры записанные у нас называются также или есть в записях в шахтинской БД
    END as department_id,
    
    t.id as title_plan_id,
    NULL as created_at,
    NULL as supdated_at
)
FROM cf20821_math.edu_plan edpl
INNER JOIN transfer.edu_str edstr ON 
INNER JOIN code_block_map m ON LEFT(edstr.ЦиклКод, 4) = m.code_index
INNER JOIN cf20821_math.subject sb ON edstr.Дисциплина = sb.title

-- 3. Цепочка связи с Планом (как вы задумали)
INNER JOIN transfer.edu_plan AS p 
    ON p.Код = edstr.КодПлана           -- Строка -> План

INNER JOIN cf20821_math.specialty AS s 
    ON s.cod = p.Специальность      -- План -> Специальность

INNER JOIN cf20821_math.title_plan AS tp 
    ON tp.specialty_id = s.id
    and tp.date_enter = p.ГодНачалаПодготовки    


--dbo.ПланыСтроки.КодПлана -> dbo.Планы.Код, dbo.Планы.Специальность -> edu_specilty.cod, edu_specilty.id -> title_plan