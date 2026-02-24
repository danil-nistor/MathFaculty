const mammoth = require("mammoth");
const fs = require("fs");
const path = require("path");

// Имена файлов
const inputFile = path.join(__dirname, "test.docx");
const outputFile = path.join(__dirname, "test.html");

// Проверка наличия входного файла
if (!fs.existsSync(inputFile)) {
    console.error(`❌ Файл ${inputFile} не найден!`);
    process.exit(1);
}

// Конвертация
mammoth.convertToHtml({ path: inputFile })
    .then(function(result) {
        // Запись HTML в файл
        fs.writeFileSync(outputFile, result.value);
        console.log("✅ Конвертация успешна!");
        console.log(`📄 Файл сохранен: ${outputFile}`);
        
        // Вывод предупреждений (если есть)
        if (result.messages.length > 0) {
            console.log("⚠️ Предупреждения:", result.messages);
        }
    })
    .catch(function(err) {
        console.error("❌ Ошибка конвертации:", err);
        process.exit(1);
    });