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


document.getElementById('createPlaylist').addEventListener('click', async () => {
    const vibe = document.getElementById('vibeInput').value;
    const spinner = document.getElementById('spinner');
    spinner.style.display = 'inline-block';
    const res = await fetch('/playlist?vibe=' + encodeURIComponent(vibe), {method: 'POST'});
    spinner.style.display = 'none';
    if (res.ok) {
        const data = await res.json();
        document.getElementById('status').innerHTML = '<a href="' + data.playlist_url + '" target="_blank">Open Playlist</a>';
    } else {
        const err = await res.json();
        document.getElementById('status').textContent = err.detail || 'Error creating playlist';
    }
});
