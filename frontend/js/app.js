const API = 'http://localhost:5000/api';

function escapeHtml(str){
  if(!str) return '';
  return String(str).replace(/[&<>"']/g, s => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'})[s]);
}

async function loadPosts(){
  const container = document.getElementById('posts');
  const loading = document.getElementById('loading');
  if(!container) return;
  try{
    const res = await fetch(`${API}/posts`);
    const posts = await res.json();
    loading && (loading.style.display = 'none');
    if(!posts || posts.length === 0){
      container.innerHTML = '<p class="loading">No posts yet. Be the first!</p>';
      return;
    }
    container.innerHTML = posts.map(p => `
      <a class="card" href="post.html?id=${p._id}">
        <h2>${escapeHtml(p.title)}</h2>
        <p class="meta">by ${escapeHtml(p.author || 'Anonymous')} · ${new Date(p.date).toLocaleString()}</p>
        <p class="excerpt">${escapeHtml((p.content || '').slice(0,160))}...</p>
      </a>
    `).join('');
  }catch(err){
    console.error(err);
    loading && (loading.innerText = 'Could not load posts.');
  }
}

async function loadPost(id){
  const container = document.getElementById('postContent');
  if(!id || !container) return;
  try{
    const res = await fetch(`${API}/posts/${id}`);
    if(!res.ok) throw new Error('Post not found');
    const p = await res.json();
    container.innerHTML = `
      <article class="card">
        <h1>${escapeHtml(p.title)}</h1>
        <p class="meta">by ${escapeHtml(p.author || 'Anonymous')} · ${new Date(p.date).toLocaleString()}</p>
        <div class="post-body">${escapeHtml(p.content).replace(/\n/g, '<br/>')}</div>
      </article>
    `;
  }catch(e){
    container.innerHTML = '<p class="loading">Could not load post.</p>';
  }
}

async function submitPost(e){
  e.preventDefault();
  const form = e.target;
  const data = {
    title: form.title.value.trim(),
    author: form.author.value.trim(),
    content: form.content.value.trim()
  };
  if(!data.title || !data.content) return alert('Title and content required');
  try{
    const res = await fetch(`${API}/posts`, {
      method:'POST',
      headers:{'Content-Type':'application/json'},
      body:JSON.stringify(data)
    });
    if(res.ok){
      location.href = 'index.html';
    } else alert('Error publishing post');
  }catch(err){
    console.error(err);
    alert('Network error');
  }
}
