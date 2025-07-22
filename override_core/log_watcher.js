const fs = require('fs');
const chokidar = require('chokidar');

const LOG_DIR = '../logs';
const REGISTRY_MD = '../codex_registry.md';

function appendSummary(file){
  const time = new Date().toISOString();
  const row = `| summary | ${time} | ${file} | updated |`;
  fs.appendFileSync(REGISTRY_MD, row + '\n');
}

chokidar.watch(LOG_DIR).on('change', path=>{
  appendSummary(path);
});
