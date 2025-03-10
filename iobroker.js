
// SEHR EINFACHE Version eines iobroker JS zum setzen des Status eines Ambientika Lüfters
// basierend auf einer Anwesenheitsvariable
const { exec } = require('child_process');

// ID der Anwesenheitsvariable
const anwesenheitID = 'javascript.0.script.Anwesenheit';

// Funktion zum Ausführen eines Python-Skripts
function runPythonScript(scriptPath) {
    exec(`python3 ${scriptPath}`, (error, stdout, stderr) => {
        if (error) {
            console.error(`Fehler beim Ausführen des Python-Skripts: ${error.message}`);
            return;
        }
        console.log(`Python-Skript ausgeführt: ${scriptPath}`);
        if (stderr) {
            console.error(`Fehlerausgabe des Python-Skripts: ${stderr}`);
        }
    });
}

// Überwachung der Anwesenheitsvariable
on({ id: anwesenheitID, change: 'any' }, function (obj) {
    if (obj.state.val) {
        // Wenn Anwesenheit = true
        runPythonScript('/home/iobroker/setWohnzimmerOff.py');
    } else {
        // Wenn Anwesenheit = false
        runPythonScript('/home/iobroker/setWohnzimmerAwayhome.py');
    }
});

console.log('Anwesenheitssteuerung gestartet');