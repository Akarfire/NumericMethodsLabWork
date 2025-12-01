const { app, BrowserWindow, dialog } = require('electron');

const { spawn } = require('child_process');
const path = require('path');


let ui_backend;

function debugMessage(message)
{
    console.log("PYTHON:", message);
    // dialog.showMessageBox({
    //     type: 'info',
    //     title: 'PYTHON',
    //     message: message,
    //     buttons: ['OK']
    // });
}

function runEmbeddedPython(script, args = []) 
{
    let pythonExe, scriptPath, pythonDir;

    if (app.isPackaged) 
    {
        // Using packaged python file paths inside resources/
        pythonExe = path.join(process.resourcesPath, "python", "python.exe");
        scriptPath = path.join(process.resourcesPath, "python-src", script);
        pythonDir = path.join(process.resourcesPath, "python-src");
    } 

    else 
    {
        // Dev paths (../Source)
        pythonExe = path.join(__dirname, "python", "python.exe");
        scriptPath = path.join(__dirname, "..", "Source", script);
        pythonDir = path.join(__dirname, "..", "Source");
    }

    const py = spawn(pythonExe, [scriptPath, ...args], { shell: true, cwd: pythonDir });

    py.stdout.on("data", data => {
        debugMessage(data.toString());
    });

    py.stderr.on("data", data => {
        debugMessage(data.toString());
    });

    py.on("exit", code => {
        debugMessage(code.toString());
    });

    return py;
}

function createWindow() 
{
    const win = new BrowserWindow({
        width: 800,
        height: 600,
        webPreferences: {
            nodeIntegration: true,
            contextIsolation: false
        }
    });

    // Loading UI
    let ui_file;
    if (app.isPackaged) ui_file = path.join(process.resourcesPath, "ui", "NumericLab.html");
    else ui_file = path.join(__dirname, "..", "UI", "NumericLab.html");

    win.loadFile(ui_file);

    // Running Core
    ui_backend = runEmbeddedPython("Main.py");
}

app.whenReady().then(() => {
    createWindow();

    app.on("activate", () => {
        if (BrowserWindow.getAllWindows().length === 0) createWindow();
    });
});

app.on("window-all-closed", () => { app.quit(); });