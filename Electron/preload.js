const { contextBridge, ipcRenderer } = require("electron");

contextBridge.exposeInMainWorld("py", {
    send: (data) => ipcRenderer.send("toPython", data),
    receive: (fn) => ipcRenderer.on("fromPython", (_, msg) => fn(JSON.parse(msg)))
});