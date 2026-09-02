const API = 'http://localhost:8000';

async function fetchWeather(city) {
    const el = document.getElementById('weather-content');
    el.innerHTML = '<div class="loader"></div>';
    try {
        const res = await fetch(`${API}/weather/${encodeURIComponent(city)}`);
        const data = await res.json();
        if (!res.ok) throw new Error(data.detail || 'Error');
        const d = data.data;
        el.innerHTML = `
            <div class="weather-info">
                <div class="weather-location">${d.city}, ${d.country}</div>
                <div class="weather-temp">${d.temperature.toFixed(1)}°C</div>
                <div class="weather-desc">${d.description}</div>
                <div class="weather-stats">
                    <div class="stat"><div class="stat-label">Feels Like</div><div class="stat-value">${d.feels_like.toFixed(1)}°C</div></div>
                    <div class="stat"><div class="stat-label">Humidity</div><div class="stat-value">${d.humidity}%</div></div>
                    <div class="stat"><div class="stat-label">Wind</div><div class="stat-value">${d.wind_speed} m/s</div></div>
                </div>
            </div>`;
    } catch(e) {
        el.innerHTML = `<p class="error-msg">${e.message}</p>`;
    }
}

async function fetchCrypto() {
    const el = document.getElementById('crypto-content');
    el.innerHTML = '<div class="loader"></div>';
    try {
        const res = await fetch(`${API}/crypto?coins=bitcoin,ethereum,dogecoin`);
        const data = await res.json();
        if (!res.ok) throw new Error(data.detail || 'Error');
        el.innerHTML = `<div class="crypto-list">${data.coins.map(c => `
            <div class="crypto-item">
                <div><div class="crypto-name">${c.name}</div></div>
                <div style="text-align:right">
                    <div class="crypto-price">$${c.current_price.toLocaleString('en-US', {minimumFractionDigits:2, maximumFractionDigits:2})}</div>
                    ${c.price_change_24h != null ? `<div class="crypto-change ${c.price_change_24h >= 0 ? 'positive' : 'negative'}">${c.price_change_24h >= 0 ? '+' : ''}${c.price_change_24h.toFixed(2)}%</div>` : ''}
                </div>
            </div>`).join('')}</div>`;
    } catch(e) {
        el.innerHTML = `<p class="error-msg">${e.message}</p>`;
    }
}

async function fetchNews(category) {
    const el = document.getElementById('news-content');
    el.innerHTML = '<div class="loader"></div>';
    try {
        const res = await fetch(`${API}/news?category=${category}&country=us`);
        const data = await res.json();
        if (!res.ok) throw new Error(data.detail || 'Error');
        const articles = data.articles.slice(0, 8);
        el.innerHTML = `<div class="news-list">${articles.map(a => `
            <div class="news-item">
                <a href="${a.url}" target="_blank" rel="noopener">${a.title}</a>
                <div class="news-meta">${a.source}${a.author ? ' · ' + a.author : ''} · ${new Date(a.published_at).toLocaleDateString()}</div>
            </div>`).join('')}</div>`;
    } catch(e) {
        el.innerHTML = `<p class="error-msg">${e.message}</p>`;
    }
}

document.getElementById('search-btn').addEventListener('click', () => {
    fetchWeather(document.getElementById('city-input').value.trim() || 'London');
});
document.getElementById('city-input').addEventListener('keydown', e => {
    if (e.key === 'Enter') fetchWeather(e.target.value.trim() || 'London');
});
document.getElementById('category-select').addEventListener('change', e => {
    fetchNews(e.target.value);
});

fetchWeather('London');
fetchCrypto();
fetchNews('general');
