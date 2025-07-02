const axios = require('axios');
const fs = require('fs');
const record = require('node-record-lpcm16');

async function captureAndSend() {
  const chunks = [];
  const rec = record.record();
  rec.stream().on('data', chunk => chunks.push(chunk));
  await new Promise(r => setTimeout(r, 1000));
  rec.stop();
  const wav = Buffer.concat(chunks);
  const audio_b64 = wav.toString('base64');
  const res = await axios.post('http://localhost:8000/stream', {
    audio_b64,
    lang: 'hinglish',
    session_id: 'demo'
  }, { responseType: 'stream' });
  res.data.on('data', d => process.stdout.write(d));
}

captureAndSend();
