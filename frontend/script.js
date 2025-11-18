async function searchExperiences() {
    const input = document.getElementById('experienceInput').value.trim();
    const resultsDiv = document.getElementById('results');
    const loadingDiv = document.getElementById('loading');
    const searchBtn = document.getElementById('searchBtn');

    if (!input) {
        alert('Please describe your experience first');
        return;
    }

    // Show loading
    loadingDiv.style.display = 'block';
    resultsDiv.innerHTML = '';
    searchBtn.disabled = true;

    try {
        const response = await fetch('/api/search', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                query: input,
                top_k: 5
            })
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();

        // Hide loading
        loadingDiv.style.display = 'none';
        searchBtn.disabled = false;

        // Display results
        displayResults(data.matches);

    } catch (error) {
        loadingDiv.style.display = 'none';
        searchBtn.disabled = false;

        resultsDiv.innerHTML = `
            <div class="no-results">
                <h3>Error</h3>
                <p>Failed to search: ${error.message}</p>
                <p>Make sure the backend server is running.</p>
            </div>
        `;
    }
}

function displayResults(matches) {
    const resultsDiv = document.getElementById('results');

    if (!matches || matches.length === 0) {
        resultsDiv.innerHTML = `
            <div class="no-results">
                <h3>No matches found</h3>
                <p>Try describing your experience differently or be more specific.</p>
            </div>
        `;
        return;
    }

    resultsDiv.innerHTML = matches.map((match, index) => `
        <div class="result-card">
            <div class="result-header">
                <div class="result-person">${index + 1}. ${match.person}</div>
                <div class="result-similarity">${(match.similarity * 100).toFixed(1)}% match</div>
            </div>

            ${match.keywords && match.keywords.length > 0 ? `
                <div class="result-keywords">
                    ${match.keywords.map(keyword => `
                        <span class="keyword">${keyword}</span>
                    `).join('')}
                </div>
            ` : ''}

            <div class="result-text">${match.text}</div>

            ${match.source_url ? `
                <div class="result-source">
                    Source: <a href="${match.source_url}" target="_blank" rel="noopener noreferrer">${truncateUrl(match.source_url)}</a>
                </div>
            ` : ''}
        </div>
    `).join('');
}

function truncateUrl(url) {
    try {
        const urlObj = new URL(url);
        return urlObj.hostname + (urlObj.pathname.length > 30 ? urlObj.pathname.substring(0, 30) + '...' : urlObj.pathname);
    } catch {
        return url.length > 50 ? url.substring(0, 50) + '...' : url;
    }
}

// Allow Enter key to search (with Shift+Enter for new line)
document.getElementById('experienceInput').addEventListener('keydown', function(e) {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        searchExperiences();
    }
});

// Set example query
function setExample(text) {
    document.getElementById('experienceInput').value = text;
    document.getElementById('experienceInput').focus();
}
