const { contextBridge, ipcRenderer } = require("electron");

let pythonListeners = [];

ipcRenderer.on("fromPython", (_, msg) => {
    for (const fn of pythonListeners) fn(msg);
});

contextBridge.exposeInMainWorld("py", {
    send: (data) => ipcRenderer.send("toPython", data),
    receive: (fn) => {
        pythonListeners.push(fn);   // register but DO NOT add IPC listener repeatedly
    }
});

contextBridge.exposeInMainWorld("backend", {
    loadHtml: () => ipcRenderer.invoke("load-html"),
    getHtmlPath: () => ipcRenderer.invoke("get-html-path")
});

contextBridge.exposeInMainWorld("tabsAPI", {
    newTab: () => ipcRenderer.send("tabs:new"),
    closeTab: (index) => ipcRenderer.send("tabs:close", index),
    switchTab: (index) => ipcRenderer.send("tabs:switch", index),
    onUpdate: (callback) => ipcRenderer.on("tabs:update", (e, data) => callback(data)),
});