let currentBlob = null;
let stream = null;

const fileInput = document.getElementById('file');
const uploader = document.getElementById('uploader');
const analyzeBtn = document.getElementById('analyzeBtn');
const kInput = document.getElementById('k');
const mediaDiv = document.getElementById('media');
const previewImg = document.getElementById('preview');

function setBlob(blob){
  currentBlob = blob; analyzeBtn.disabled = false;
}

function showPreview(dataUrl){
  previewImg.src = dataUrl; previewImg.style.display = 'block';
}

async function postExtract(blob){
  const k = kInput.value || 6;
  let res;
  if (blob instanceof File) {
    const fd = new FormData();
    fd.append('image', blob, blob.name || 'upload.png');
    fd.append('k', k);
    res = await fetch('/api/extract', { method: 'POST', body: fd });
  } else {
    res = await fetch('/api/extract?k='+k, { method: 'POST', body: blob });
  }
  const js = await res.json();
  if(!res.ok){ alert(js.error || 'Hata'); return; }
  if(js.preview){ showPreview(js.preview); }
  renderPalette(js.colors || []);
}

function renderPalette(colors){
  const el = document.getElementById('palette');
  el.innerHTML = '';
  colors.forEach(c => {
    const wrap = document.createElement('div');
    wrap.className = 'swatch';
    const top = document.createElement('div');
    top.className = 'swatch-top';
    top.style.background = c.hex;
    const info = document.createElement('div');
    info.className = 'swatch-info';
    info.innerHTML = `
      <div class="flex" style="justify-content:space-between">
        <b>${c.hex}</b>
        <button onclick="navigator.clipboard.writeText('${c.hex}')">Kopyala</button>
      </div>
      <div class="small">RGB: ${c.rgb.join(', ')} · ${c.percent}%</div>
      <div class="hint">Tamamlayıcı</div>
      <div class="grid-2">
        ${c.complements.map(h=>`<span class='tag' style='background:${h};color:#000000AA'>${h}</span>`).join('')}
      </div>
      <div class="hint">Analoglar</div>
      <div class="grid-2">
        ${c.analogs.map(h=>`<span class='tag' style='background:${h};color:#000000AA'>${h}</span>`).join('')}
      </div>
    `;
    wrap.appendChild(top); wrap.appendChild(info); el.appendChild(wrap);
  });
}

fileInput.addEventListener('change', () => {
  const f = fileInput.files[0];
  if(!f) return;
  setBlob(f);
  const reader = new FileReader();
  reader.onload = () => showPreview(reader.result);
  reader.readAsDataURL(f);
});


['dragenter','dragover'].forEach(ev=>uploader.addEventListener(ev, e=>{e.preventDefault(); uploader.classList.add('drag');}));
['dragleave','drop'].forEach(ev=>uploader.addEventListener(ev, e=>{e.preventDefault(); uploader.classList.remove('drag');}));
uploader.addEventListener('drop', e=>{
  const f = e.dataTransfer.files[0];
  if(f){ setBlob(f); const reader=new FileReader(); reader.onload=()=>showPreview(reader.result); reader.readAsDataURL(f); }
});


const webcamBtn = document.getElementById('webcamBtn');
const snapBtn = document.getElementById('snapBtn');
webcamBtn.addEventListener('click', async ()=>{
  try{
    stream = await navigator.mediaDevices.getUserMedia({ video:true, audio:false });
    mediaDiv.innerHTML = '';
    const v = document.createElement('video'); v.autoplay = true; v.srcObject = stream; mediaDiv.appendChild(v);
    snapBtn.disabled = false; webcamBtn.textContent = 'Webcam Yeniden Başlat';
  }catch(err){ alert('Webcam açılamadı: '+err); }
});

snapBtn.addEventListener('click', ()=>{
  const v = mediaDiv.querySelector('video'); if(!v) return;
  const c = document.createElement('canvas'); c.width = v.videoWidth; c.height = v.videoHeight;
  const ctx = c.getContext('2d'); ctx.drawImage(v, 0, 0);
  c.toBlob(blob=>{ if(blob){ setBlob(blob); c.toDataURL && showPreview(c.toDataURL('image/jpeg',0.88)); } }, 'image/jpeg', 0.9);
});

// Analyze
analyzeBtn.addEventListener('click', ()=>{ if(currentBlob) postExtract(currentBlob); });
