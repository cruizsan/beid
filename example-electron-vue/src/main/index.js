import { ipcMain, app, BrowserWindow } from 'electron'
var child_process = require('child_process');
const fs = require('fs');
var uniqueFilename = require('unique-filename')

/**
 * Set `__static` path to static files in production
 * https://simulatedgreg.gitbooks.io/electron-vue/content/en/using-static-assets.html
 */
if (process.env.NODE_ENV !== 'development') {
  global.__static = require('path').join(__dirname, '/static').replace(/\\/g, '\\\\')
}

let mainWindow
const winURL = process.env.NODE_ENV === 'development'
  ? `http://localhost:9080`
  : `file://${__dirname}/index.html`

function createWindow () {
  /**
   * Initial window options
   */
  mainWindow = new BrowserWindow({
    height: 563,
    useContentSize: true,
    width: 1000
  })

  mainWindow.loadURL(winURL)

  mainWindow.on('closed', () => {
    mainWindow = null
  })
}

app.on('ready', createWindow)

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit()
  }
})

app.on('activate', () => {
  if (mainWindow === null) {
    createWindow()
  }
})

let child = null;
let client = null;

/**
 * BEID READER
 * launch script python3 who wait for a card
 * open a pipe VueJs <-> beid-wait-card
 */
ipcMain.on('beid-read', (event, data) => {
  client = event;
  child = child_process.spawn('python3 bin/beid-wait-card.py', {shell: true}, {});
  console.log('child process launched');
  child.stdout.on('data', function (data) {
      event.sender.send('beid-read', data);
  });
})
