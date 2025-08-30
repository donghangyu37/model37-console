async function runToday(){
  const t = getToken(); if(!t) return;
  setMsg("正在运行今天预测...");
  const res = await fetch("/run/today",{method:"POST", headers:{Authorization: "Bearer "+t}});
  if(!res.ok){ setMsg("运行失败："+res.status); return; }
  const j = await res.json();
  setMsg("已触发。共筛选："+j.count+" 场；已生成："+j.report);
}

async function loadToday(){
  const t = getToken(); if(!t) return;
  setMsg("加载今日价值比赛...");
  const res = await fetch("/value-picks/today",{headers:{Authorization: "Bearer "+t}});
  if(!res.ok){ setMsg("加载失败："+res.status); return; }
  const rows = await res.json();
  renderTable(rows);
  setMsg("已加载，共 "+rows.length+" 条。"); 
}

async function downloadCSV(){
  const t = getToken(); if(!t) return;
  const res = await fetch("/report/today.csv");
  if(!res.ok){ setMsg("下载失败："+res.status); return; }
  const blob = await res.blob();
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = "today.csv";
  a.click();
  URL.revokeObjectURL(url);
}

function getToken(){
  const t = document.getElementById("token").value.trim();
  if(!t){ setMsg("请先输入访问令牌（.env 的 API_TOKEN）"); return null; }
  (function injectToken(){
    const _fetch = window.fetch;
    window.fetch = (input, init={})=>{
      init.headers = init.headers || {};
      init.headers.Authorization = init.headers.Authorization || "Bearer "+t;
      return _fetch(input, init);
    };
  })();
  return t;
}

function setMsg(s){ document.getElementById("msg").innerText = s; }

function renderTable(rows){
  if(!rows || rows.length===0){ document.getElementById("table").innerHTML = "<p>暂无数据。</p>"; return; }
  const cols = Object.keys(rows[0]);
  let html = "<table><thead><tr>"+cols.map(c=>"<th>"+c+"</th>").join("")+"</tr></thead><tbody>";
  for(const r of rows){
    html += "<tr>"+cols.map(c=>"<td>"+(r[c]??"")+"</td>").join("")+"</tr>";
  }
  html += "</tbody></table>";
  document.getElementById("table").innerHTML = html;
}
