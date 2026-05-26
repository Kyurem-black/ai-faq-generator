document.addEventListener('DOMContentLoaded', ()=>{
  const btn = document.getElementById('generateBtn')
  const output = document.getElementById('output')
  btn.addEventListener('click', async ()=>{
    const topic = document.getElementById('topic').value.trim()
    const content = document.getElementById('content').value.trim()
    const num = parseInt(document.getElementById('num').value, 10) || 5
    if(!topic && !content){
      alert('Please provide a topic or some content to generate FAQs.')
      return
    }

    // UI: loading state
    btn.disabled = true
    btn.textContent = 'Generating...'
    output.innerHTML = '<div class="loading">Generating FAQs…</div>'
    try{
      const res = await fetch('/api/generate', {
        method:'POST',
        headers:{'Content-Type':'application/json'},
        body: JSON.stringify({topic, content, num})
      })
      if(!res.ok){
        let errText
        try{ const j = await res.json(); errText = j.error || JSON.stringify(j) }catch(e){ errText = await res.text() }
        throw new Error(errText || 'Server error')
      }
      const data = await res.json()
      renderFAQs(data.faqs || [])
    }catch(err){
      output.innerHTML = `<div class="error">Error: ${escapeHtml(err.message || String(err))}</div>`
      window._lastFaqs = []
    }finally{
      btn.disabled = false
      btn.textContent = 'Generate FAQs'
    }
  })

    function renderFAQs(faqs){
    if(!faqs.length){ output.innerText = 'No FAQs generated.'; return }
    output.innerHTML = ''
      window._lastFaqs = faqs
    // render cards
    const grid = document.createElement('div'); grid.className = 'faq-grid'
    faqs.forEach((f,idx)=>{
      const el = document.createElement('div'); el.className='faq-card'
      el.innerHTML = `
        <div class="faq-head"><div class="question">${idx+1}. ${escapeHtml(f.question)}</div></div>
        <div class="answer">${escapeHtml(f.answer)}</div>
        <div class="actions"><button class="copy-btn" data-idx="${idx}">Copy</button></div>
      `
      grid.appendChild(el)
    })
    output.innerHTML = ''
    output.appendChild(grid)

    output.querySelectorAll('.copy-btn').forEach(btn=>btn.addEventListener('click', e=>{
      const idx = +e.currentTarget.dataset.idx
      const f = faqs[idx]
      navigator.clipboard.writeText(`${f.question}\n\n${f.answer}`)
    }))
  }

  // Copy All and Export JSON
  const copyAllBtn = document.getElementById('copyAllBtn')
  const exportJsonBtn = document.getElementById('exportJsonBtn')
  copyAllBtn.addEventListener('click', ()=>{
    const faqs = window._lastFaqs || []
    if(!faqs.length) return alert('No FAQs to copy')
    const text = faqs.map((f,i)=>`${i+1}. ${f.question}\n\n${f.answer}`).join('\n\n')
    navigator.clipboard.writeText(text)
  })

  exportJsonBtn.addEventListener('click', ()=>{
    const faqs = window._lastFaqs || []
    if(!faqs.length) return alert('No FAQs to export')
    const blob = new Blob([JSON.stringify(faqs, null, 2)], {type:'application/json'})
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url; a.download = 'faqs.json'; document.body.appendChild(a); a.click(); a.remove(); URL.revokeObjectURL(url)
  })


  function escapeHtml(s){ return String(s).replace(/[&<>"']/g, c=>({
    '&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'
  }[c])) }
})