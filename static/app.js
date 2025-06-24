document.getElementById('login').addEventListener('click', async () => {
    const res = await fetch('/login');
    const data = await res.json();
    window.location = data.auth_url;
});

async function checkAuth() {
    const res = await fetch('/profile');
    if (res.ok) {
        document.getElementById('login').style.display = 'none';
        document.getElementById('loggedin').style.display = 'block';
    }
}

checkAuth();

document.getElementById('setVibe').addEventListener('click', async () => {
    const vibe = document.getElementById('vibeInput').value;
    const res = await fetch('/vibe?vibe=' + encodeURIComponent(vibe), {method: 'POST'});
    if (res.ok) {
        const data = await res.json();
        document.getElementById('status').textContent = 'Vibe set to: ' + data.vibe;
    } else {
        document.getElementById('status').textContent = 'Failed to set vibe';
    }
});

document.getElementById('createPlaylist').addEventListener('click', async () => {
    const res = await fetch('/playlist', {method: 'POST'});
    if (res.ok) {
        const data = await res.json();
        document.getElementById('status').innerHTML = '<a href="' + data.playlist_url + '" target="_blank">Open Playlist</a>';
    } else {
        const err = await res.json();
        document.getElementById('status').textContent = err.detail || 'Error creating playlist';
    }
});
