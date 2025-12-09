const { app, BrowserWindow, dialog, ipcMain } = require('electron');

const { spawn } = require('child_process');
const path = require('path');
const fs = require("fs");


let backend;

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

function runEmbeddedPython(script, args = [], win) 
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

    const py = spawn(pythonExe, ["-u", scriptPath, ...args], { cwd: pythonDir });

    return py;
}

function createWindow() 
{
    const win = new BrowserWindow({
        width: 1280,
        height: 720,
        webPreferences: {
            zoomFactor: 0.9,
            nodeIntegration: false,
            contextIsolation: true,
            webSecurity: false,
            preload: __dirname + "/preload.js"
        }
    });

    // Loading UI
    let ui_file;
    if (app.isPackaged) ui_file = path.join(process.resourcesPath, "ui", "NumericLab.html");
    else ui_file = path.join(__dirname, "..", "UI", "NumericLab.html");

    win.loadFile(ui_file);

    // Running backend
    backend = runEmbeddedPython("Main.py", [], win);

    backend.stdout.on("data", data => {
        debugMessage(data.toString());

        const message = data.toString();

        let lines = message.split("\n");
        for (let i = 0; i < lines.length; i++)
            if (lines[i] !== "") win.webContents.send("fromPython", lines[i]);
    });

    backend.stderr.on("data", data => {
        debugMessage(data.toString());
    });

    backend.on("exit", code => {
        debugMessage(" exited with code:" + code.toString());
    });

    ipcMain.on("toPython", (_, msg) => {
        backend.stdin.write(JSON.stringify(msg) + "\n");
    });

    // User-data folder setup
    const userDataPath = app.getPath("userData");
    backend.stdin.write(JSON.stringify({"user_data_path" : userDataPath}) + "\n");

    // Setting up plot fetching pass through
    const htmlPath = path.join(app.getPath("userData"), "plot.html");
    ipcMain.handle("load-html", () => {
        return fs.readFileSync(htmlPath, "utf8");
    });

    const htmlOutputPath = path.join(app.getPath("userData"), "plot.html");
    ipcMain.handle("get-html-path", () => {
        return htmlOutputPath;
    });
}

app.whenReady().then(() => {
    createWindow();

    app.on("activate", () => {
        if (BrowserWindow.getAllWindows().length === 0) createWindow();
    });
});

app.on("window-all-closed", () => { app.quit(); });