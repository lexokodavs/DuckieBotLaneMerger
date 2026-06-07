from .base import render_template

_CONTENT = '''
    <div class="container">

        <!-- Left: debug grid only -->
        <div class="video-section" style="flex-direction:column;">
            <div style="font-size:11px;color:var(--text-muted);text-transform:uppercase;
                        letter-spacing:.05em;margin-bottom:6px;">Debug view</div>
            <img src="/debug_frame" class="stream" id="debugStream">
        </div>

        <!-- Right: controls sidebar -->
        <div class="controls-section">

            <!-- Status card -->
            <div class="card">
                <div class="card-header">
                    Status
                    <span id="statusDot" style="width:8px;height:8px;border-radius:50%;
                        background:var(--accent-green);display:inline-block;"></span>
                </div>
                <div id="statusTable" style="font-size:12px;">
                    <div style="color:var(--text-muted);text-align:center;padding:12px 0;">
                        Waiting for data...
                    </div>
                </div>
            </div>

            <!-- HSV bounds card (red detection) -->
            <div class="card">
                <div class="card-header">Red HSV Bounds</div>

                <div style="font-size:11px;color:var(--text-muted);margin-bottom:10px;">
                    Range 1 (hue 0-10)
                </div>
                <div id="hsv-lo1" style="margin-bottom:14px;">
                    <div style="font-size:11px;color:var(--text-secondary);margin-bottom:6px;">Lower bound</div>
                    <div class="hsv-row" data-key="lo1" data-idx="0" data-label="H lo1"></div>
                    <div class="hsv-row" data-key="lo1" data-idx="1" data-label="S lo1"></div>
                    <div class="hsv-row" data-key="lo1" data-idx="2" data-label="V lo1"></div>
                </div>
                <div id="hsv-hi1" style="margin-bottom:14px;">
                    <div style="font-size:11px;color:var(--text-secondary);margin-bottom:6px;">Upper bound</div>
                    <div class="hsv-row" data-key="hi1" data-idx="0" data-label="H hi1"></div>
                    <div class="hsv-row" data-key="hi1" data-idx="1" data-label="S hi1"></div>
                    <div class="hsv-row" data-key="hi1" data-idx="2" data-label="V hi1"></div>
                </div>

                <div style="font-size:11px;color:var(--text-muted);margin-bottom:10px;
                            border-top:1px solid var(--border-color);padding-top:10px;">
                    Range 2 (hue 170-180)
                </div>
                <div id="hsv-lo2" style="margin-bottom:14px;">
                    <div style="font-size:11px;color:var(--text-secondary);margin-bottom:6px;">Lower bound</div>
                    <div class="hsv-row" data-key="lo2" data-idx="0" data-label="H lo2"></div>
                    <div class="hsv-row" data-key="lo2" data-idx="1" data-label="S lo2"></div>
                    <div class="hsv-row" data-key="lo2" data-idx="2" data-label="V lo2"></div>
                </div>
                <div id="hsv-hi2" style="margin-bottom:10px;">
                    <div style="font-size:11px;color:var(--text-secondary);margin-bottom:6px;">Upper bound</div>
                    <div class="hsv-row" data-key="hi2" data-idx="0" data-label="H hi2"></div>
                    <div class="hsv-row" data-key="hi2" data-idx="1" data-label="S hi2"></div>
                    <div class="hsv-row" data-key="hi2" data-idx="2" data-label="V hi2"></div>
                </div>

                <div id="hsvStatus" class="status"></div>
            </div>

            <!-- HSV bounds card (yellow + white lane detection) -->
            <div class="card">
                <div class="card-header">Lane HSV Bounds</div>

                <div style="font-size:11px;color:var(--text-muted);margin-bottom:10px;">
                    Yellow lane
                </div>
                <div style="margin-bottom:14px;">
                    <div style="font-size:11px;color:var(--text-secondary);margin-bottom:6px;">Lower bound</div>
                    <div class="lane-hsv-row" data-lanekey="yellow_lower" data-idx="0"></div>
                    <div class="lane-hsv-row" data-lanekey="yellow_lower" data-idx="1"></div>
                    <div class="lane-hsv-row" data-lanekey="yellow_lower" data-idx="2"></div>
                </div>
                <div style="margin-bottom:14px;">
                    <div style="font-size:11px;color:var(--text-secondary);margin-bottom:6px;">Upper bound</div>
                    <div class="lane-hsv-row" data-lanekey="yellow_upper" data-idx="0"></div>
                    <div class="lane-hsv-row" data-lanekey="yellow_upper" data-idx="1"></div>
                    <div class="lane-hsv-row" data-lanekey="yellow_upper" data-idx="2"></div>
                </div>

                <div style="font-size:11px;color:var(--text-muted);margin-bottom:10px;
                            border-top:1px solid var(--border-color);padding-top:10px;">
                    White lane
                </div>
                <div style="margin-bottom:14px;">
                    <div style="font-size:11px;color:var(--text-secondary);margin-bottom:6px;">Lower bound</div>
                    <div class="lane-hsv-row" data-lanekey="white_lower" data-idx="0"></div>
                    <div class="lane-hsv-row" data-lanekey="white_lower" data-idx="1"></div>
                    <div class="lane-hsv-row" data-lanekey="white_lower" data-idx="2"></div>
                </div>
                <div style="margin-bottom:10px;">
                    <div style="font-size:11px;color:var(--text-secondary);margin-bottom:6px;">Upper bound</div>
                    <div class="lane-hsv-row" data-lanekey="white_upper" data-idx="0"></div>
                    <div class="lane-hsv-row" data-lanekey="white_upper" data-idx="1"></div>
                    <div class="lane-hsv-row" data-lanekey="white_upper" data-idx="2"></div>
                </div>

                <div id="laneHsvStatus" class="status"></div>
            </div>

            <!-- Send command card -->
            <div class="card">
                <div class="card-header">Send Command</div>
                <div style="display:flex;flex-direction:column;gap:8px;">
                    <div style="display:flex;gap:6px;">
                        <input id="cmdKey" type="text" placeholder="key"
                            style="flex:1;padding:6px 8px;background:var(--bg-sidebar);
                                   border:1px solid var(--border-color);border-radius:4px;
                                   color:var(--text-primary);font-size:13px;">
                        <input id="cmdValue" type="text" placeholder="value"
                            style="flex:2;padding:6px 8px;background:var(--bg-sidebar);
                                   border:1px solid var(--border-color);border-radius:4px;
                                   color:var(--text-primary);font-size:13px;">
                    </div>
                    <button class="button" onclick="sendCommand()">Send</button>
                    <div id="cmdStatus" class="status"></div>
                </div>
            </div>

        </div>
    </div>
'''

_EXTRA_CSS = '''
/* Status table rows */
#statusTable .row {
    display: flex;
    justify-content: space-between;
    padding: 6px 0;
    border-bottom: 1px solid var(--border-color);
    align-items: baseline;
}
#statusTable .row:last-child { border-bottom: none; }
#statusTable .key  { color: var(--text-secondary); font-size: 12px; }
#statusTable .val  { color: var(--text-primary); font-weight: 500; font-size: 13px; font-family: monospace; }

/* State badge colour */
.state-badge {
    display: inline-block;
    padding: 2px 8px;
    border-radius: 10px;
    font-size: 12px;
    font-weight: 600;
    font-family: monospace;
    text-transform: uppercase;
}
.state-convoying { background: rgba(31,111,235,.2); color: var(--accent-blue); }
.state-waiting   { background: rgba(210,153,34,.2); color: var(--accent-orange); }
.state-turning   { background: rgba(163,113,247,.2); color: var(--accent-purple); }
.state-finishing { background: rgba(63,185,80,.2);  color: var(--accent-green); }
.state-unknown   { background: rgba(110,118,129,.2); color: var(--text-muted); }

/* HSV slider rows */
.hsv-row, .lane-hsv-row {
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 6px;
}
.hsv-label {
    width: 40px;
    font-size: 11px;
    color: var(--text-muted);
    text-transform: uppercase;
    flex-shrink: 0;
}
'''

_EXTRA_JS = '''
/* ── Status polling ── */
function refreshStatus() {
    fetch('/status')
        .then(r => r.json())
        .then(data => {
            const table = document.getElementById('statusTable');
            const state = (data.state || 'unknown').toLowerCase();
            const badgeClass = 'state-' + state;
            let rows = `<div class="row">
                <span class="key">state</span>
                <span class="val"><span class="state-badge ${badgeClass}">${state}</span></span>
            </div>`;
            Object.keys(data).filter(k => k !== 'state').forEach(k => {
                rows += `<div class="row">
                    <span class="key">${k}</span>
                    <span class="val">${JSON.stringify(data[k])}</span>
                </div>`;
            });
            table.innerHTML = rows;
            document.getElementById('statusDot').style.background = 'var(--accent-green)';
        })
        .catch(() => {
            document.getElementById('statusDot').style.background = 'var(--accent-red)';
        });
}

/* ── Debug frame refresh ── */
function refreshDebugFrame() {
    const img = document.getElementById('debugStream');
    img.src = '/debug_frame?t=' + Date.now();
}

/* ── Red HSV sliders ── */
const HSV_MAX = { H: 180, S: 255, V: 255 };
const HSV_IDX_LABEL = ['H', 'S', 'V'];

const hsvState = { lo1: [0,120,100], hi1: [10,255,255], lo2: [170,120,100], hi2: [180,255,255] };

function buildHsvSliders() {
    document.querySelectorAll('.hsv-row').forEach(row => {
        const key = row.dataset.key;
        const idx = parseInt(row.dataset.idx);
        const ch  = HSV_IDX_LABEL[idx];
        const max = HSV_MAX[ch];
        const id  = `hsv-${key}-${idx}`;
        const val = hsvState[key][idx];
        row.innerHTML = `
            <span class="hsv-label">${ch}</span>
            <input type="range" class="slider" id="${id}"
                   min="0" max="${max}" value="${val}" style="flex:1;">
            <input type="number" class="input-box" id="${id}-input"
                   min="0" max="${max}" value="${val}" style="width:46px;">
        `;
        syncSliderInput(id, () => sendHsv(key, idx, parseInt(document.getElementById(id).value)));
    });
}

let hsvSendTimeout = null;
function sendHsv(key, idx, value) {
    hsvState[key][idx] = value;
    clearTimeout(hsvSendTimeout);
    hsvSendTimeout = setTimeout(() => {
        postJSON('/hsv', { lo1: hsvState.lo1, hi1: hsvState.hi1, lo2: hsvState.lo2, hi2: hsvState.hi2 })
            .then(() => showStatus('hsvStatus', 'Saved', 'success'))
            .catch(e => showStatus('hsvStatus', 'Error: ' + e, 'error'));
    }, 150);
}

function loadHsvBounds() {
    fetch('/hsv')
        .then(r => r.json())
        .then(data => {
            ['lo1','hi1','lo2','hi2'].forEach(k => {
                if (data[k]) {
                    hsvState[k] = data[k];
                    [0,1,2].forEach(i => setSliderValue(`hsv-${k}-${i}`, data[k][i]));
                }
            });
        });
}

/* ── Lane HSV sliders (yellow + white) ── */
const laneHsvState = {
    yellow_lower: [5,  80,  100],
    yellow_upper: [35, 192, 250],
    white_lower:  [0,  0,   180],
    white_upper:  [179, 80, 255],
};

function buildLaneHsvSliders() {
    document.querySelectorAll('.lane-hsv-row').forEach(row => {
        const key = row.dataset.lanekey;
        const idx = parseInt(row.dataset.idx);
        const ch  = HSV_IDX_LABEL[idx];
        const max = HSV_MAX[ch];
        const id  = `lane-${key}-${idx}`;
        const val = laneHsvState[key][idx];
        row.innerHTML = `
            <span class="hsv-label">${ch}</span>
            <input type="range" class="slider" id="${id}"
                   min="0" max="${max}" value="${val}" style="flex:1;">
            <input type="number" class="input-box" id="${id}-input"
                   min="0" max="${max}" value="${val}" style="width:46px;">
        `;
        syncSliderInput(id, () => sendLaneHsv(key, idx, parseInt(document.getElementById(id).value)));
    });
}

let laneHsvSendTimeout = null;
function sendLaneHsv(key, idx, value) {
    laneHsvState[key][idx] = value;
    clearTimeout(laneHsvSendTimeout);
    laneHsvSendTimeout = setTimeout(() => {
        postJSON('/hsv/lane', {
            yellow_lower: laneHsvState.yellow_lower,
            yellow_upper: laneHsvState.yellow_upper,
            white_lower:  laneHsvState.white_lower,
            white_upper:  laneHsvState.white_upper,
        })
            .then(() => showStatus('laneHsvStatus', 'Saved', 'success'))
            .catch(e => showStatus('laneHsvStatus', 'Error: ' + e, 'error'));
    }, 150);
}

function loadLaneHsvBounds() {
    fetch('/hsv/lane')
        .then(r => r.json())
        .then(data => {
            // server returns flat keys: yellow_lower_h, yellow_lower_s, etc.
            ['yellow_lower','yellow_upper','white_lower','white_upper'].forEach(key => {
                ['h','s','v'].forEach((ch, i) => {
                    const val = data[`${key}_${ch}`];
                    if (val !== undefined) {
                        laneHsvState[key][i] = val;
                        setSliderValue(`lane-${key}-${i}`, val);
                    }
                });
            });
        });
}

/* ── Send command ── */
function sendCommand() {
    const key   = document.getElementById('cmdKey').value.trim();
    const value = document.getElementById('cmdValue').value.trim();
    if (!key) { showStatus('cmdStatus', 'Key cannot be empty', 'error'); return; }
    postJSON('/command', {key, value})
        .then(r => showStatus('cmdStatus', r.status === 'ok' ? 'Sent' : r.message,
                              r.status === 'ok' ? 'success' : 'error'))
        .catch(e => showStatus('cmdStatus', 'Error: ' + e, 'error'));
}

document.getElementById('cmdValue').addEventListener('keydown', e => {
    if (e.key === 'Enter') sendCommand();
});

/* ── Boot ── */
buildHsvSliders();
loadHsvBounds();
buildLaneHsvSliders();
loadLaneHsvBounds();
refreshStatus();
refreshDebugFrame();
setInterval(refreshStatus,     500);
setInterval(refreshDebugFrame, 250);
'''


def get_template(title='Project', subtitle='Real Duckiebot'):
    return render_template(
        title=title,
        subtitle=subtitle,
        content_html=_CONTENT,
        extra_css=_EXTRA_CSS,
        extra_js=_EXTRA_JS,
    )