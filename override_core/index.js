const express = require('express');
const fs = require('fs');
const crypto = require('crypto');
const chokidar = require('chokidar');
const fetch = require('node-fetch');

const PROJECT_NAME = 'MKWW_Override_Core';
const NGROK_ENDPOINT = 'https://32137bd707a1.ngrok-free.app';
const LOCAL_PORT = 80;
const DASHBOARD_PORT = 3333;
const LOG_FILE = 'logs/encrypted.log';
const REGISTRY_MD = '../codex_registry.md';
const REGISTRY_JSON = '../codex_registry.json';
const AUTH_HEADER = 'X-MKWW-Auth';

// Ensure registry files exist with headers
function initRegistry(){
  if(!fs.existsSync(REGISTRY_MD)){
    fs.writeFileSync(
      REGISTRY_MD,
      '# Athena Override Codex\n\n| Function | Timestamp | Origin IP | Status |\n|----------|-----------|-----------|--------|\n'
    );
  }
  if(!fs.existsSync(REGISTRY_JSON)){
    fs.writeFileSync(REGISTRY_JSON, '{}');
  }
}

// Simple encryption helper
const key = crypto.scryptSync('MKWW_master_key', 'salt', 24);
const iv = Buffer.alloc(16, 0);
function encrypt(data){
  const cipher = crypto.createCipheriv('aes-192-cbc', key, iv);
  let encrypted = cipher.update(data, 'utf8', 'hex');
  encrypted += cipher.final('hex');
  return encrypted;
}

// Log helper
function logEvent(msg){
  const time = new Date().toISOString();
  const entry = `${time} - ${msg}`;
fs.appendFileSync(LOG_FILE, encrypt(entry)+'\n');
}

initRegistry();
const overrides = {};
function registerOverride(name, fn){
  overrides[name] = fn;
  const time = new Date().toISOString();
  const mdRow = `| ${name} | ${time} | - | registered |`;
  fs.appendFileSync(REGISTRY_MD, mdRow+'\n');
  let json = {};
  if (fs.existsSync(REGISTRY_JSON)) { try { json = JSON.parse(fs.readFileSync(REGISTRY_JSON, "utf8")); } catch (e) { json = {}; } }
  json[name] = {registered: time};
  fs.writeFileSync(REGISTRY_JSON, JSON.stringify(json, null, 2));
}

// Example override function
function run_it(req, res){
  const ip = req.headers['x-forwarded-for'] || req.socket.remoteAddress || '-';
  logEvent(`run_it triggered from ${ip}`);
  res.set(AUTH_HEADER, 'token');
  res.json({status:'OK',owner:'MKWW',function:'run_it'});
}

registerOverride('run_it', run_it);

const app = express();
app.use((req,res,next)=>{
  res.set(AUTH_HEADER,'token');
  next();
});
app.get('/run_it', run_it);

const server = app.listen(LOCAL_PORT, ()=>{
  logEvent(`Server listening on ${LOCAL_PORT}`);
});

// Simple dashboard to stream log events
const dashboard = express();
dashboard.get('/events', (req, res)=>{
  res.setHeader('Content-Type','text/event-stream');
  res.setHeader('Cache-Control','no-cache');
  const stream = fs.createReadStream(LOG_FILE,{encoding:'utf8'});
  stream.on('data', chunk=>{
    res.write(`data: ${chunk}\n\n`);
  });
});
dashboard.get('/',(req,res)=>{
  res.send('<html><body><pre id="log"></pre><script>var s=new EventSource("/events");s.onmessage=function(e){document.getElementById("log").textContent+=e.data+"\n";};</script></body></html>');
});
dashboard.listen(DASHBOARD_PORT,()=>{
  logEvent(`Dashboard listening on ${DASHBOARD_PORT}`);
});

// Watcher for hot reload and log updates
chokidar.watch(['..','logs'], {ignored: /node_modules|\.git/}).on('change', path=>{
  logEvent(`File changed: ${path}`);
});

process.on('uncaughtException', err=>{
  logEvent(`Error: ${err.message}`);
});
