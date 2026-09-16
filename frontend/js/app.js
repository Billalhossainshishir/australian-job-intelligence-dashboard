const $=id=>document.getElementById(id);
const CITIES=[["Hobart","TAS"],["Launceston","TAS"],["Melbourne","VIC"],["Sydney","NSW"],["Brisbane","QLD"],["Perth","WA"],["Adelaide","SA"],["Canberra","ACT"],["Newcastle","NSW"],["Geelong","VIC"]];
const ROLES=[
["Data Analyst","Data & Analytics",["SQL","Python","Power BI","Git"]],
["Graduate Data Engineer","Data Engineering",["Python","SQL","ETL","AWS","Docker","Git"]],
["Machine Learning Engineer","AI & ML",["Python","Machine Learning","SQL","Docker","AWS","Git"]],
["AI Graduate","AI & ML",["Python","Artificial Intelligence","Machine Learning","REST APIs","Git"]],
["Software Developer","Software Engineering",["JavaScript","TypeScript","React","Node.js","REST APIs","Git"]],
["Backend Developer","Software Engineering",["Python","FastAPI","SQL","Docker","REST APIs","Git"]],
["Cloud Engineer","Cloud & DevOps",["AWS","Azure","Docker","Kubernetes","Terraform","CI/CD","Linux","Git"]],
["IT Support Analyst","IT Support",["IT Support","Microsoft 365","Networking","Linux","Git"]],
["Cyber Security Analyst","Cybersecurity",["Cybersecurity","Networking","Linux","Python","Git"]],
["Business Intelligence Analyst","Data & Analytics",["SQL","Power BI","Tableau","Python","Git"]],
["Platform Engineer","Cloud & DevOps",["Linux","Docker","Kubernetes","AWS","CI/CD","Terraform","Git"]],
["Java Developer","Software Engineering",["Java","SQL","REST APIs","Docker","Git"]]
];
const COMPANIES=["Harbour Digital","Southern Data Lab","TasTech Solutions","Bluegum Systems","Koala Cloud","Southern Cross Analytics","Riverstone Software","Orbit Data","Coastal Networks","Civic Technology Group","Aurora Digital","Wattle AI"];
const EXTRA=["Azure","GCP","Spark","Kafka","Django","C#","C++"];
const sampleCV="Artificial Intelligence undergraduate with practical projects using Python, SQL, JavaScript, FastAPI, PostgreSQL, Docker, Git, REST APIs, machine learning, cloud data processing, AWS and Azure. Built dashboards, data pipelines, monitoring systems and AI-assisted workflows.";
const state={jobs:[],filtered:[],selected:null,charts:{}};

function makeJobs(){
 let out=[],n=1;
 for(let cycle=0;cycle<2;cycle++) for(let i=0;i<ROLES.length;i++) for(let j=0;j<CITIES.length;j++){
   const [title,role,base]=ROLES[i],[city,st]=CITIES[(j+i*2+cycle)%CITIES.length];
   const graduate=(i+j+cycle)%4===0;
   const skills=[...base];
   if((i+j)%3===0) skills.push(EXTRA[(i+j+cycle)%EXTRA.length]);
   const uniq=[...new Set(skills)];
   out.push({
     job_id:"AU-"+String(n++).padStart(4,"0"),title:graduate?title.replace(/^/,"Graduate "):title,
     company:COMPANIES[(i*3+j+cycle)%COMPANIES.length],city,state:st,location:`${city}, ${st}`,
     description:`Join a technology team delivering ${role.toLowerCase()} outcomes. The role uses ${uniq.join(", ")} and values practical problem solving, communication, testing and documentation.`,
     salary:graduate?"$70k–$82k sample":"$90k–$125k sample",employment_type:(i+j)%5===0?"Contract":"Full-time",
     role_type:role,experience_level:graduate?"Graduate":((i+j)%3===0?"Mid":"Entry"),date_posted:`2026-09-${String(((i*10+j+cycle)%15)+1).padStart(2,"0")}`,
     source:"Curated portfolio demo",skills:uniq
   });
 }
 return out.slice(0,240);
}
function unique(a){return [...new Set(a)].sort()}
function populate(id,vals){const el=$(id);vals.forEach(v=>{let o=document.createElement("option");o.value=v;o.textContent=v;el.appendChild(o)})}
function init(){
 state.jobs=makeJobs();state.filtered=[...state.jobs];
 populate("filterCity",unique(state.jobs.map(x=>x.city)));populate("filterState",unique(state.jobs.map(x=>x.state)));
 populate("filterRole",unique(state.jobs.map(x=>x.role_type)));populate("filterLevel",unique(state.jobs.map(x=>x.experience_level)));
 populate("filterSkill",unique(state.jobs.flatMap(x=>x.skills)));
 ["filterCity","filterState","filterRole","filterLevel","filterSkill"].forEach(id=>$(id).addEventListener("change",applyFilters));
 $("filterSearch").addEventListener("input",applyFilters);$("resetFilters").addEventListener("click",resetFilters);
 $("loadSampleCv").addEventListener("click",()=>{$("cvText").value=sampleCV});
 $("compareBtn").addEventListener("click",compareCV);
 updateStats();render();
}
function updateStats(){
 $("statJobs").textContent=state.jobs.length;$("statLocations").textContent=unique(state.jobs.map(x=>x.location)).length;
 $("statSkills").textContent=unique(state.jobs.flatMap(x=>x.skills)).length;$("statGraduate").textContent=state.jobs.filter(x=>x.experience_level==="Graduate").length;
}
function resetFilters(){
 ["filterCity","filterState","filterRole","filterLevel","filterSkill"].forEach(id=>$(id).value="");$("filterSearch").value="";applyFilters();
}
function applyFilters(){
 const city=$("filterCity").value,st=$("filterState").value,role=$("filterRole").value,lvl=$("filterLevel").value,skill=$("filterSkill").value,q=$("filterSearch").value.trim().toLowerCase();
 state.filtered=state.jobs.filter(j=>(!city||j.city===city)&&(!st||j.state===st)&&(!role||j.role_type===role)&&(!lvl||j.experience_level===lvl)&&(!skill||j.skills.includes(skill))&&(!q||(`${j.title} ${j.company} ${j.description}`).toLowerCase().includes(q)));
 render();
}
function render(){ $("filteredCount").textContent=`${state.filtered.length} jobs`;renderJobs();renderCharts()}
function esc(s){return String(s).replace(/[&<>"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]))}
function renderJobs(){
 const list=$("jobList");
 if(!state.filtered.length){list.innerHTML='<div class="no-jobs">No demo jobs match these filters.</div>';return}
 list.innerHTML=state.filtered.slice(0,80).map(j=>`<article class="job-item ${state.selected?.job_id===j.job_id?"active":""}" data-id="${j.job_id}"><h4>${esc(j.title)}</h4><div class="job-meta">${esc(j.company)} · ${esc(j.location)} · ${esc(j.experience_level)}</div><div class="badges">${j.skills.slice(0,5).map(s=>`<span class="badge">${esc(s)}</span>`).join("")}</div></article>`).join("");
 list.querySelectorAll(".job-item").forEach(el=>el.onclick=()=>selectJob(el.dataset.id));
}
function selectJob(id){
 state.selected=state.jobs.find(j=>j.job_id===id);renderJobs();const j=state.selected;
 $("selectedPanel").innerHTML=`<div class="eyebrow dark">SELECTED ROLE</div><h3>${esc(j.title)}</h3><div class="selected-company">${esc(j.company)}</div><div class="selected-details"><div><small>Location</small><strong>${esc(j.location)}</strong></div><div><small>Experience</small><strong>${esc(j.experience_level)}</strong></div><div><small>Employment</small><strong>${esc(j.employment_type)}</strong></div><div><small>Salary sample</small><strong>${esc(j.salary)}</strong></div></div><div class="badges">${j.skills.map(s=>`<span class="badge skill">${esc(s)}</span>`).join("")}</div><p class="selected-description">${esc(j.description)}</p><a href="#compare" class="button primary full">Compare CV with this role</a>`;
}
function counts(items,getter){const m={};items.forEach(x=>{const k=getter(x);m[k]=(m[k]||0)+1});return Object.entries(m).sort((a,b)=>b[1]-a[1])}
function draw(id,labels,data,label){
 if(state.charts[id])state.charts[id].destroy();
 state.charts[id]=new Chart($(id),{type:"bar",data:{labels,datasets:[{label,data,borderWidth:0,borderRadius:6,backgroundColor:"#2dd4bf"}]},options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false}},scales:{x:{grid:{display:false},ticks:{color:"#607086"}},y:{beginAtZero:true,grid:{color:"#edf1f5"},ticks:{precision:0,color:"#607086"}}}}});
}
function renderCharts(){
 const skills=counts(state.filtered.flatMap(j=>j.skills),x=>x).slice(0,10),cities=counts(state.filtered,j=>j.city).slice(0,8);
 const cloud=["AWS","Azure","GCP"].map(s=>[s,state.filtered.filter(j=>j.skills.includes(s)).length]);
 const langs=["Python","SQL","JavaScript","TypeScript","Java","C#","C++"].map(s=>[s,state.filtered.filter(j=>j.skills.includes(s)).length]).sort((a,b)=>b[1]-a[1]);
 draw("skillsChart",skills.map(x=>x[0]),skills.map(x=>x[1]),"Jobs");draw("citiesChart",cities.map(x=>x[0]),cities.map(x=>x[1]),"Jobs");
 draw("cloudChart",cloud.map(x=>x[0]),cloud.map(x=>x[1]),"Jobs");draw("languageChart",langs.map(x=>x[0]),langs.map(x=>x[1]),"Jobs");
}
function compareCV(){
 const out=$("comparisonResult"),cv=$("cvText").value.trim();
 if(!state.selected){out.innerHTML='<div class="empty-state dark-empty">Select a job record first.</div>';return}
 if(!cv){out.innerHTML='<div class="empty-state dark-empty">Paste CV text or load the sample CV first.</div>';return}
 const text=cv.toLowerCase(),matched=state.selected.skills.filter(s=>hasSkill(text,s)),missing=state.selected.skills.filter(s=>!matched.includes(s));
 const p=state.selected.skills.length?Math.round(matched.length/state.selected.skills.length*100):0;
 out.innerHTML=`<h3 class="result-title">Technical Skill Coverage</h3><div class="coverage-ring" style="--p:${p}"><strong>${p}%</strong></div><div class="result-columns"><div class="result-box"><h4>Matched (${matched.length})</h4>${matched.map(s=>`<span class="badge matched">${esc(s)}</span>`).join("")||'<span class="helper">None found</span>'}</div><div class="result-box"><h4>Missing (${missing.length})</h4>${missing.map(s=>`<span class="badge missing">${esc(s)}</span>`).join("")||'<span class="helper">None missing</span>'}</div></div><p class="helper">Coverage is tracked technical-skill overlap only. It is not a hiring probability, employability score or assessment of experience quality.</p>`;
}
function hasSkill(text,skill){
 const variants={"Artificial Intelligence":["artificial intelligence","generative ai","genai"," ai "],"Machine Learning":["machine learning","scikit-learn","sklearn"],"Power BI":["power bi","powerbi"],"REST APIs":["rest api","restful","apis"],"IT Support":["it support","service desk","helpdesk"],"CI/CD":["ci/cd","continuous integration"],"Node.js":["node.js","nodejs"],"C#":["c#","c sharp"],"C++":["c++","cpp"],"GCP":["gcp","google cloud"],"AWS":["aws","amazon web services"],"Azure":["azure","microsoft azure"],"Git":["git","github","gitlab"]}[skill]||[skill.toLowerCase()];
 return variants.some(v=>v.trim()==="ai"?/(^|\W)ai($|\W)/i.test(text):text.includes(v));
}
init();