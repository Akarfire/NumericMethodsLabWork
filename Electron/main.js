const { app, BrowserWindow, WebContentsView, dialog, ipcMain } = require('electron');

const { spawn } = require('child_process');
const path = require('path');
const fs = require("fs");


let backend;

let mainWindow;
let tabs = [];
let activeTab = -1;


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
    mainWindow = new BrowserWindow({
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

    // Handle resize to reposition active view
    mainWindow.on('resize', () => {
        if (activeTab >= 0) layoutActiveView();
    });

    const win = mainWindow;

    // Loading UI
    let ui_file;
    if (app.isPackaged) ui_file = path.join(process.resourcesPath, "ui", "Tabs.html");
    else ui_file = path.join(__dirname, "..", "UI", "Tabs.html");

    win.loadFile(ui_file);

    // Running backend
    backend = runEmbeddedPython("Main.py", [], win);

    backend.stdout.on("data", data => {

        debugMessage(data.toString());
        if (activeTab >= 0 && activeTab < tabs.length)
        {
            const message = data.toString();

            let lines = message.split("\n");
            for (let i = 0; i < lines.length; i++)
                if (lines[i] !== "") tabs[activeTab].webContents.send("fromPython", lines[i]);
        }
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


function createTab() 
{
    const view = new WebContentsView({
        webPreferences: {
            zoomFactor: 0.9,
            nodeIntegration: false,
            contextIsolation: true,
            webSecurity: false,
            preload: __dirname + "/preload.js"
        }
    });

    view.setBackgroundColor('rgba(0, 0, 0, 1)');

    let ui_file;
    if (app.isPackaged) ui_file = path.join(process.resourcesPath, 'ui', 'NumericLab.html');
    else ui_file = path.join(__dirname, '..', 'UI', 'NumericLab.html');

    view.webContents.loadFile(ui_file);

    tabs.push(view);
    switchTab(tabs.length - 1);
    sendTabListToRenderer();
}

function switchTab(index) 
{
    if (index === activeTab) return;
    if(index < 0 || index >= tabs.length) return;

    const prev = tabs[activeTab];

    if (prev) 
    {
        mainWindow.contentView.removeChildView(prev);
    }

    activeTab = index;
    const view = tabs[activeTab];
    mainWindow.contentView.addChildView(view);

    layoutActiveView();
    sendTabListToRenderer();
}

function closeTab(index) 
{
    if (tabs.length === 1) return;

    const view = tabs[index];
    if (!view) return;

    if (index === activeTab) 
    {
        mainWindow.contentView.removeChildView(view);
    }

    view.webContents.destroy();
    tabs.splice(index, 1);

    if (index === activeTab) 
    {
        activeTab = Math.max(0, index - 1);
        const newView = tabs[activeTab];
        mainWindow.contentView.addChildView(newView);
        layoutActiveView();
    } 

    else if (index < activeTab) 
    {
        activeTab--;
    }

    sendTabListToRenderer();
}

function layoutActiveView() 
{
    const tabBarHeight = 45;

    const [w, h] = mainWindow.getSize();    // width, height array
    const view = tabs[activeTab];
    view.setBounds({
        x: 0, 
        y: tabBarHeight,
        width: w,
        height: h - tabBarHeight
    });
}

function sendTabListToRenderer() 
{
    mainWindow.webContents.send('tabs:update', {
        tabs: tabs.map((_, i) => ({ id: i })),
        active: activeTab
    });
}

// IPC handlers
ipcMain.on('tabs:new', () => createTab());
ipcMain.on('tabs:switch', (_, index) => switchTab(index));
ipcMain.on('tabs:close', (_, index) => closeTab(index));