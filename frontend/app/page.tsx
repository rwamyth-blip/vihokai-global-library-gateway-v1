'use client'
import { useState } from 'react'

export default function Home(){
  const [q,setQ]=useState('artificial intelligence')
  const [results,setResults]=useState<any[]>([])
  const [loading,setLoading]=useState(false)
  const [chat,setChat]=useState('')
  const [answer,setAnswer]=useState<any>(null)

  const search = async()=>{
    setLoading(true)
    const r = await fetch('http://localhost:8000/library/search',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({query:q,limit:12})})
    const j = await r.json()
    setResults(j.results||[])
    setLoading(false)
  }
  const ask = async()=>{
    setLoading(true)
    const r = await fetch('http://localhost:8000/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({message:chat, use_library:true, top_k:6})})
    const j = await r.json()
    setAnswer(j)
    setLoading(false)
  }

  return (
    <div style={{maxWidth:900,margin:'40px auto',fontFamily:'Inter, sans-serif',padding:20}}>
      <div style={{display:'flex',alignItems:'center',gap:12}}>
        <div style={{width:44,height:44,borderRadius:12,background:'linear-gradient(135deg,#2563eb,#7c3aed)',color:'#fff',display:'flex',alignItems:'center',justifyContent:'center',fontWeight:700,fontSize:18}}>VG</div>
        <div>
          <h1 style={{margin:0,fontSize:26}}>VihokAI <span style={{color:'#2563eb'}}>Global Library</span></h1>
          <p style={{margin:'4px 0 0',color:'#666',fontSize:14}}>Gateway V1 — ค้นหนังสือ/งานวิจัย/สื่อจากห้องสมุดทั่วโลก</p>
        </div>
      </div>
      <p style={{marginTop:16,color:'#888',fontSize:13}}>Open Library + Library of Congress + Crossref + NASA → FastAPI → Qdrant → RAG (Python เป็นตัวกลางสืบค้น, AI สรุปจาก context)</p>
      
      <div style={{display:'flex',gap:8,marginTop:20}}>
        <input value={q} onChange={e=>setQ(e.target.value)} style={{flex:1,padding:10}} placeholder="Search libraries..." />
        <button onClick={search} disabled={loading} style={{padding:'10px 20px'}}>Search</button>
      </div>

      <div style={{display:'grid',gridTemplateColumns:'repeat(2,1fr)',gap:12,marginTop:20}}>
        {results.map((r,i)=>(
          <div key={i} style={{border:'1px solid #ddd',borderRadius:12,padding:12}}>
            <b>{r.title}</b><br/>
            <small>{(r.authors||[]).join(', ')} | {r.year||''} | {r.source}</small><br/>
            {r.thumbnail && <img src={r.thumbnail} style={{width:'100%',maxHeight:150,objectFit:'cover',marginTop:8,borderRadius:8}} />}
            <div style={{marginTop:8}}><a href={r.source_url} target="_blank">Source</a></div>
          </div>
        ))}
      </div>

      <h2 style={{marginTop:40}}>Chat RAG</h2>
      <div style={{display:'flex',gap:8}}>
        <input value={chat} onChange={e=>setChat(e.target.value)} style={{flex:1,padding:10}} placeholder="อธิบายทฤษฎีหลุมดำ..." />
        <button onClick={ask} disabled={loading} style={{padding:'10px 20px'}}>Ask</button>
      </div>
      {answer && (
        <div style={{marginTop:20,whiteSpace:'pre-wrap',border:'1px solid #eee',padding:16,borderRadius:12,background:'#fafafa'}}>
          {answer.answer}
          <hr/>
          <b>Sources:</b>
          <ul>{(answer.citations||[]).map((c:any,i:number)=><li key={i}>{c.title} - {c.source} - <a href={c.url} target="_blank">{c.url}</a></li>)}</ul>
        </div>
      )}
    </div>
  )
}
