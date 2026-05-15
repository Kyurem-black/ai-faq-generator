document.addEventListener('DOMContentLoaded', ()=>{
  const btn = document.getElementById('generateBtn')
  const output = document.getElementById('output')
  btn.addEventListener('click', async ()=>{
    const topic = document.getElementById('topic').value.trim()
    const content = document.getElementById('content').value.trim()
    if(!topic && !content){
      alert('Please provide a topic or some content to generate FAQs.')
      return
    }

    output.innerText = 'Generating...'
    try{
      const res = await fetch('/api/generate', {
        method:'POST',
        headers:{'Content-Type':'application/json'},
        body: JSON.stringify({topic, content})
      })
      if(!res.ok) throw new Error(await res.text())
      const data = await res.json()
      renderFAQs(data.faqs || [])
    }catch(err){
      output.innerText = 'Error: '+err.message
    }
  })

  function renderFAQs(faqs){
    if(!faqs.length){ output.innerText = 'No FAQs generated.'; return }
    output.innerHTML = ''
    faqs.forEach((f,idx)=>{
      const el = document.createElement('div'); el.className='faq'
      el.innerHTML = `<div class="question">${idx+1}. ${escapeHtml(f.question)}</div>`+
                     `<div class="answer">${escapeHtml(f.answer)}</div>`+
                     `<div class="actions"><button class="copy-btn" data-idx="${idx}">Copy</button></div>`
      output.appendChild(el)
    })

    output.querySelectorAll('.copy-btn').forEach(btn=>btn.addEventListener('click', e=>{
      const idx = +e.currentTarget.dataset.idx
      const f = faqs[idx]
      navigator.clipboard.writeText(`${f.question}\n\n${f.answer}`)
    }))
  }

  function escapeHtml(s){ return String(s).replace(/[&<>"']/g, c=>({
    '&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'
  }[c])) }
})